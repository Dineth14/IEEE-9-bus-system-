import numpy as np
import time

# ==========================================
# Data Section (IEEE 9-Bus System)
# ==========================================

def get_ieee_9_bus_data():
    num_buses = 9
    
    # Bus Types: 0=Slack, 1=PQ, 2=PV
    # Bus 1: Slack, Bus 2,3: PV, Others: PQ
    bus_types = np.array([0, 2, 2, 1, 1, 1, 1, 1, 1])
    
    # Specified P and Q (p.u.)
    P_specified = np.zeros(num_buses)
    Q_specified = np.zeros(num_buses)
    
    # Generators (Generation is positive)
    P_specified[1] = 1.63  # Bus 2
    P_specified[2] = 0.85  # Bus 3
    
    # Loads (Load is negative)
    P_specified[4] = -1.25 # Bus 5
    Q_specified[4] = -0.50
    P_specified[5] = -0.90 # Bus 6
    Q_specified[5] = -0.30
    P_specified[7] = -1.00 # Bus 8
    Q_specified[7] = -0.35
    
    # Initial Voltages (Flat Start)
    V_init = np.ones(num_buses, dtype=complex)
    V_init[0] = 1.04 + 0j  # Bus 1 (Slack)
    V_init[1] = 1.025 + 0j # Bus 2 (PV)
    V_init[2] = 1.025 + 0j # Bus 3 (PV)
    
    # Branch Data: (From, To, R, X, B)
    branch_data = [
        (4, 5, 0.0100, 0.0850, 0.1760),
        (4, 6, 0.0170, 0.0920, 0.1580),
        (5, 7, 0.0320, 0.1610, 0.3060),
        (6, 9, 0.0390, 0.1700, 0.3580),
        (7, 8, 0.0085, 0.0720, 0.1490),
        (8, 9, 0.0119, 0.1008, 0.2090),
        # Transformers (B=0)
        (1, 4, 0.0, 0.0576, 0.0),
        (2, 7, 0.0, 0.0625, 0.0),
        (3, 9, 0.0, 0.0586, 0.0)
    ]
    
    return num_buses, bus_types, P_specified, Q_specified, V_init, branch_data

def build_y_bus(num_buses, branch_data):
    Y_bus = np.zeros((num_buses, num_buses), dtype=complex)
    for branch in branch_data:
        f, t, r, x, b = branch
        i, j = int(f) - 1, int(t) - 1
        z = complex(r, x)
        y = 1 / z
        b_shunt = complex(0, b / 2)
        Y_bus[i, i] += y + b_shunt
        Y_bus[j, j] += y + b_shunt
        Y_bus[i, j] -= y
        Y_bus[j, i] -= y
    return Y_bus

# ==========================================
# Method: Fast Decoupled Load Flow
# ==========================================

def build_b_matrices(num_buses, branch_data, bus_types):
    slack_bus = np.where(bus_types == 0)[0][0]
    pq_buses = np.where(bus_types == 1)[0]
    pv_buses = np.where(bus_types == 2)[0]
    non_slack = np.sort(np.concatenate((pq_buses, pv_buses)))
    
    map_ns = {bus: i for i, bus in enumerate(non_slack)}
    map_pq = {bus: i for i, bus in enumerate(pq_buses)}
    
    n_ns = len(non_slack)
    n_pq = len(pq_buses)
    
    B_prime = np.zeros((n_ns, n_ns))
    B_dprime = np.zeros((n_pq, n_pq))
    
    for branch in branch_data:
        f, t, r, x, b = branch
        i, j = int(f) - 1, int(t) - 1
        b_val = -1.0 / x
        
        if i in map_ns and j in map_ns:
            idx_i, idx_j = map_ns[i], map_ns[j]
            B_prime[idx_i, idx_j] -= b_val
            B_prime[idx_j, idx_i] -= b_val
        if i in map_ns: B_prime[map_ns[i], map_ns[i]] += b_val
        if j in map_ns: B_prime[map_ns[j], map_ns[j]] += b_val
            
        if i in map_pq and j in map_pq:
            idx_i, idx_j = map_pq[i], map_pq[j]
            B_dprime[idx_i, idx_j] -= b_val
            B_dprime[idx_j, idx_i] -= b_val
        if i in map_pq: B_dprime[map_pq[i], map_pq[i]] += b_val
        if j in map_pq: B_dprime[map_pq[j], map_pq[j]] += b_val
            
    return B_prime, B_dprime, non_slack, pq_buses

def fast_decoupled(Y_bus, P_spec, Q_spec, V_init, bus_types, branch_data, max_iter=100, tol=1e-4):
    V = np.array(V_init, copy=True)
    B_prime, B_dprime, non_slack, pq_buses = build_b_matrices(len(V), branch_data, bus_types)
    
    for it in range(max_iter):
        S_calc = V * np.conj(Y_bus @ V)
        P_calc = np.real(S_calc)
        dP = P_spec[non_slack] - P_calc[non_slack]
        dP_norm = dP / np.abs(V[non_slack])
        
        if np.max(np.abs(dP)) < tol:
            Q_calc = np.imag(S_calc)
            dQ = Q_spec[pq_buses] - Q_calc[pq_buses]
            if np.max(np.abs(dQ)) < tol: return V, it + 1
        
        dTheta = np.linalg.solve(B_prime, dP_norm)
        V_ang = np.angle(V)
        V_ang[non_slack] += dTheta
        V = np.abs(V) * np.exp(1j * V_ang)
        
        S_calc = V * np.conj(Y_bus @ V)
        Q_calc = np.imag(S_calc)
        dQ = Q_spec[pq_buses] - Q_calc[pq_buses]
        dQ_norm = dQ / np.abs(V[pq_buses])
        
        dV_mag = np.linalg.solve(B_dprime, dQ_norm)
        V_mag = np.abs(V)
        V_mag[pq_buses] += dV_mag
        V = V_mag * np.exp(1j * np.angle(V))
        
        if np.max(np.abs(dP)) < tol and np.max(np.abs(dQ)) < tol: return V, it + 1
            
    return V, max_iter

if __name__ == "__main__":
    print("Fast Decoupled Load Flow Analysis")
    print("=================================")
    num_buses, bus_types, P_spec, Q_spec, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    start_time = time.time()
    V_fd, iter_fd = fast_decoupled(Y_bus, P_spec, Q_spec, V_init, bus_types, branch_data)
    end_time = time.time()
    
    print(f"\nConverged in {iter_fd} iterations.")
    print(f"Time taken: {end_time - start_time:.6f} seconds.")
    print("\nBus Voltages:")
    print(f"{'Bus':<5} | {'Magnitude (p.u.)':<18} | {'Angle (deg)':<12}")
    print("-" * 45)
    for i in range(num_buses):
        print(f"{i+1:<5} | {np.abs(V_fd[i]):<18.4f} | {np.degrees(np.angle(V_fd[i])):<12.4f}")