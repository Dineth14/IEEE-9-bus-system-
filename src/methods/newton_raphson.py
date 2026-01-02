"""
Full Newton-Raphson Load Flow Program for IEEE 9-Bus System
============================================================
This program implements the Full Newton-Raphson method for solving power flow equations.
All matrices (Y-bus, Jacobian submatrices J1-J4) are constructed from first principles.

Assignment: EE-354 Power Engineering - Load Flow Analysis
Deadline: February 6, 2026

Line Number References (for Flowchart):
- Lines 1-100: Imports, Data Input, and Y-bus Construction
- Lines 101-300: Newton-Raphson Algorithm Core
- Lines 301-400: Results Calculation (Line Flows, Losses)
- Lines 401-500: Main Program and Output Display

Author: [E/21/291]
Date: January 2026
"""

import numpy as np
import time

# ==========================================
# LINES 25-100: DATA INPUT AND Y-BUS CONSTRUCTION
# ==========================================

def get_ieee_9_bus_data():
    """
    Returns IEEE 9-Bus system data.
    
    Returns:
    --------
    num_buses : int
    bus_types : array (0=Slack, 1=PQ, 2=PV)
    P_specified : array (pu)
    Q_specified : array (pu)
    V_init : complex array (flat start voltages)
    branch_data : list of tuples
    
    Flowchart Box 1: Data Input
    Line Numbers: 25-80
    """
    num_buses = 9
    
    # Bus Types: 0=Slack, 1=PQ, 2=PV
    # Bus 1: Slack (Reference Bus)
    # Buses 2, 3: PV (Generator Buses)
    # Buses 4-9: PQ (Load Buses)
    bus_types = np.array([0, 2, 2, 1, 1, 1, 1, 1, 1])
    
    # Specified P and Q in per unit (pu)
    # Positive values = Generation, Negative values = Load
    P_specified = np.zeros(num_buses)
    Q_specified = np.zeros(num_buses)
    
    # Generators (Generation is positive)
    P_specified[1] = 1.63  # Bus 2: 163 MW
    P_specified[2] = 0.85  # Bus 3: 85 MW
    
    # Loads (Load is negative)
    P_specified[4] = -1.25  # Bus 5: 125 MW load
    Q_specified[4] = -0.50  # Bus 5: 50 MVAr load
    P_specified[5] = -0.90  # Bus 6: 90 MW load
    Q_specified[5] = -0.30  # Bus 6: 30 MVAr load
    P_specified[7] = -1.00  # Bus 8: 100 MW load
    Q_specified[7] = -0.35  # Bus 8: 35 MVAr load
    
    # Initial Voltages (Flat Start as per Assignment Requirements)
    # All buses start at 1.0 pu magnitude and 0 degrees angle
    # Except: Slack and PV buses have specified voltage magnitudes
    V_init = np.ones(num_buses, dtype=complex)
    V_init[0] = 1.04 + 0j   # Bus 1 (Slack): 1.04 pu
    V_init[1] = 1.025 + 0j  # Bus 2 (PV): 1.025 pu
    V_init[2] = 1.025 + 0j  # Bus 3 (PV): 1.025 pu
    
    # Branch Data: (From_Bus, To_Bus, R, X, B)
    # R = Resistance (pu), X = Reactance (pu), B = Total Line Charging (pu)
    # Note: For transformers, B = 0
    branch_data = [
        # Lines (with charging susceptance)
        (4, 5, 0.0100, 0.0850, 0.1760),  # Line 4-5
        (4, 6, 0.0170, 0.0920, 0.1580),  # Line 4-6
        (5, 7, 0.0320, 0.1610, 0.3060),  # Line 5-7
        (6, 9, 0.0390, 0.1700, 0.3580),  # Line 6-9
        (7, 8, 0.0085, 0.0720, 0.1490),  # Line 7-8
        (8, 9, 0.0119, 0.1008, 0.2090),  # Line 8-9
        # Transformers (B=0, no charging)
        (1, 4, 0.0, 0.0576, 0.0),        # Transformer 1-4
        (2, 7, 0.0, 0.0625, 0.0),        # Transformer 2-7
        (3, 9, 0.0, 0.0586, 0.0)         # Transformer 3-9
    ]
    
    return num_buses, bus_types, P_specified, Q_specified, V_init, branch_data


def build_y_bus(num_buses, branch_data):
    """
    Constructs the Y-bus admittance matrix from branch data.
    
    The Y-bus matrix represents the network admittances:
    - Diagonal elements (Y_ii): Sum of all admittances connected to bus i
    - Off-diagonal elements (Y_ij): Negative of admittance between buses i and j
    
    Parameters:
    -----------
    num_buses : int
        Total number of buses in the system
    branch_data : list of tuples
        Each tuple: (from_bus, to_bus, R, X, B)
    
    Returns:
    --------
    Y_bus : complex numpy array (num_buses x num_buses)
        Admittance matrix
    
    Flowchart Box 2: Y-bus Construction
    Line Numbers: 103-145
    """
    # Initialize Y-bus matrix as complex zeros
    Y_bus = np.zeros((num_buses, num_buses), dtype=complex)
    
    # Build Y-bus by processing each branch
    for branch in branch_data:
        f, t, r, x, b = branch
        # Convert 1-based bus numbering to 0-based array indexing
        i = int(f) - 1
        j = int(t) - 1
        
        # Calculate series admittance: y = 1/z = 1/(r + jx)
        z = complex(r, x)
        y_series = 1 / z
        
        # Calculate shunt admittance (half of total line charging at each end)
        y_shunt = complex(0, b / 2)
        
        # Update Y-bus matrix elements
        # Diagonal elements: self-admittance of each bus
        Y_bus[i, i] += y_series + y_shunt
        Y_bus[j, j] += y_series + y_shunt
        
        # Off-diagonal elements: mutual admittance (negative)
        Y_bus[i, j] -= y_series
        Y_bus[j, i] -= y_series
        
    return Y_bus


# ==========================================
# LINES 148-350: NEWTON-RAPHSON ALGORITHM
# ==========================================

def newton_raphson(Y_bus, P_specified, Q_specified, V_init, bus_types, 
                   max_iter=100, tol=1e-4, verbose=True):
    """
    Solves power flow equations using Full Newton-Raphson method.
    
    The Newton-Raphson method iteratively solves:
    [ΔP]   [J1  J2] [Δδ]
    [ΔQ] = [J3  J4] [ΔV]
    
    Where:
    - ΔP, ΔQ = Power mismatches
    - J1, J2, J3, J4 = Jacobian submatrices
    - Δδ = Angle corrections
    - ΔV = Voltage magnitude corrections
    
    Parameters:
    -----------
    Y_bus : complex array
        Bus admittance matrix
    P_specified : array
        Specified real power (pu)
    Q_specified : array
        Specified reactive power (pu)
    V_init : complex array
        Initial voltage phasors
    bus_types : array
        Bus type codes (0=Slack, 1=PQ, 2=PV)
    max_iter : int
        Maximum iterations
    tol : float
        Convergence tolerance (pu)
    verbose : bool
        Print iteration details
    
    Returns:
    --------
    V : complex array
        Final voltage phasors
    P_calc : array
        Calculated real power
    Q_calc : array
        Calculated reactive power
    iteration_data : list
        Data from each iteration (for Task 1 requirement)
    
    Flowchart Box 3-7: Iterative Solution
    Line Numbers: 148-350
    """
    num_buses = len(Y_bus)
    
    # LINE 215: Initialize voltage phasors
    V = np.array(V_init, copy=True)
    
    # LINES 218-225: Identify bus types
    slack_bus = np.where(bus_types == 0)[0][0]
    pq_buses = np.where(bus_types == 1)[0]
    pv_buses = np.where(bus_types == 2)[0]
    non_slack_buses = np.sort(np.concatenate((pq_buses, pv_buses)))
    
    # Storage for iteration data (for Task 1: 2nd iteration output)
    iteration_data = []
    
    if verbose:
        print("\n" + "="*80)
        print("STARTING NEWTON-RAPHSON LOAD FLOW ANALYSIS")
        print("="*80)
        print(f"Number of buses: {num_buses}")
        print(f"Slack bus: {slack_bus + 1}")
        print(f"PV buses: {pv_buses + 1}")
        print(f"PQ buses: {pq_buses + 1}")
        print(f"Convergence tolerance: {tol} pu")
        print(f"Maximum iterations: {max_iter}")
        print("="*80)
    
    # LINES 242-345: Main iteration loop
    for iteration in range(max_iter):
        if verbose:
            print(f"\n--- ITERATION {iteration + 1} ---")
        
        # LINE 248: Calculate power injections at all buses
        # S = V * conj(I) = V * conj(Y_bus * V)
        S_calc = V * np.conj(Y_bus @ V)
        P_calc = np.real(S_calc)
        Q_calc = np.imag(S_calc)
        
        # LINES 254-257: Calculate power mismatches
        # ΔP = P_specified - P_calculated (for non-slack buses)
        # ΔQ = Q_specified - Q_calculated (for PQ buses only)
        dP = P_specified[non_slack_buses] - P_calc[non_slack_buses]
        dQ = Q_specified[pq_buses] - Q_calc[pq_buses]
        
        # Combine mismatches into single vector
        mismatch = np.concatenate((dP, dQ))
        
        # Calculate maximum mismatch for convergence check
        max_mismatch = np.max(np.abs(mismatch))
        
        if verbose:
            print(f"Maximum power mismatch: {max_mismatch:.6f} pu")
            print(f"Bus voltages (pu):")
            for i in range(num_buses):
                print(f"  Bus {i+1}: {np.abs(V[i]):.4f} ∠ {np.degrees(np.angle(V[i])):7.3f}°")
        
        # Store iteration data (especially for 2nd iteration output requirement)
        iteration_data.append({
            'iteration': iteration + 1,
            'V': V.copy(),
            'P_calc': P_calc.copy(),
            'Q_calc': Q_calc.copy(),
            'dP': dP.copy(),
            'dQ': dQ.copy(),
            'max_mismatch': max_mismatch
        })
        
        # LINE 286: Check for convergence
        if max_mismatch < tol:
            if verbose:
                print(f"\n{'='*80}")
                print(f"CONVERGED in {iteration + 1} iterations!")
                print(f"Maximum mismatch: {max_mismatch:.8f} pu < {tol} pu")
                print(f"{'='*80}")
            return V, P_calc, Q_calc, iteration_data
        
        # LINES 296-340: Build Jacobian Matrix
        # Jacobian structure:
        #     [J1  J2]     [∂P/∂δ   ∂P/∂|V|]
        # J = [J3  J4]  =  [∂Q/∂δ   ∂Q/∂|V|]
        
        n_non_slack = len(non_slack_buses)
        n_pq = len(pq_buses)
        
        # Initialize Jacobian submatrices
        J1 = np.zeros((n_non_slack, n_non_slack))  # ∂P/∂δ
        J2 = np.zeros((n_non_slack, n_pq))         # ∂P/∂|V|
        J3 = np.zeros((n_pq, n_non_slack))         # ∂Q/∂δ
        J4 = np.zeros((n_pq, n_pq))                # ∂Q/∂|V|
        
        # LINES 314-325: Fill J1 and J3 (derivatives w.r.t. angles)
        for r, i in enumerate(non_slack_buses):
            for c, k in enumerate(non_slack_buses):
                if i == k:
                    # Diagonal elements
                    J1[r, c] = -Q_calc[i] - np.imag(Y_bus[i, i]) * np.abs(V[i])**2
                else:
                    # Off-diagonal elements
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J1[r, c] = np.abs(V[i] * V[k]) * (
                        np.real(y_ik) * np.sin(delta_ik) - 
                        np.imag(y_ik) * np.cos(delta_ik)
                    )
        
        for r, i in enumerate(pq_buses):
            for c, k in enumerate(non_slack_buses):
                if i == k:
                    # Diagonal elements
                    J3[r, c] = P_calc[i] - np.real(Y_bus[i, i]) * np.abs(V[i])**2
                else:
                    # Off-diagonal elements
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J3[r, c] = -np.abs(V[i] * V[k]) * (
                        np.real(y_ik) * np.cos(delta_ik) + 
                        np.imag(y_ik) * np.sin(delta_ik)
                    )
        
        # LINES 350-370: Fill J2 and J4 (derivatives w.r.t. voltage magnitudes)
        for r, i in enumerate(non_slack_buses):
            for c, k in enumerate(pq_buses):
                if i == k:
                    # Diagonal elements
                    J2[r, c] = P_calc[i] / np.abs(V[i]) + np.real(Y_bus[i, i]) * np.abs(V[i])
                else:
                    # Off-diagonal elements
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J2[r, c] = np.abs(V[i]) * (
                        np.real(y_ik) * np.cos(delta_ik) + 
                        np.imag(y_ik) * np.sin(delta_ik)
                    )
        
        for r, i in enumerate(pq_buses):
            for c, k in enumerate(pq_buses):
                if i == k:
                    # Diagonal elements
                    J4[r, c] = Q_calc[i] / np.abs(V[i]) - np.imag(Y_bus[i, i]) * np.abs(V[i])
                else:
                    # Off-diagonal elements
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J4[r, c] = np.abs(V[i]) * (
                        np.real(y_ik) * np.sin(delta_ik) - 
                        np.imag(y_ik) * np.cos(delta_ik)
                    )
        
        # LINE 391: Assemble full Jacobian matrix
        J = np.block([[J1, J2], [J3, J4]])
        
        # LINE 394: Solve linear system: J * dx = mismatch
        dx = np.linalg.solve(J, mismatch)
        
        # LINES 397-405: Extract corrections and update voltages
        d_angle = dx[:n_non_slack]  # Angle corrections
        d_vmag = dx[n_non_slack:]    # Magnitude corrections
        
        # Update voltage angles
        current_angles = np.angle(V)
        current_angles[non_slack_buses] += d_angle
        
        # Update voltage magnitudes (PQ buses only)
        current_mags = np.abs(V)
        current_mags[pq_buses] += d_vmag
        
        # Reconstruct voltage phasor: V = |V| * e^(jθ)
        V = current_mags * np.exp(1j * current_angles)
    
    # If we reach here, convergence was not achieved
    print(f"\nWARNING: Newton-Raphson did not converge within {max_iter} iterations.")
    print(f"Final maximum mismatch: {max_mismatch:.6f} pu")
    return V, P_calc, Q_calc, iteration_data


# ==========================================
# LINES 420-520: LINE FLOWS AND LOSSES CALCULATION
# ==========================================

def calculate_line_flows(V, branch_data):
    """
    Calculates power flows and losses in all transmission lines and transformers.
    
    For each branch from bus i to bus j:
    - Current: I_ij = (V_i - V_j) * y_series + V_i * y_shunt
    - Power flow: S_ij = V_i * conj(I_ij)
    - Loss: S_loss = S_ij + S_ji
    
    Parameters:
    -----------
    V : complex array
        Final voltage phasors
    branch_data : list
        Branch parameters
    
    Returns:
    --------
    line_flows : list of dicts
        Power flows and losses for each line
    total_loss_P : float
        Total system real power loss (pu)
    total_loss_Q : float
        Total system reactive power loss (pu)
    
    Flowchart Box 8: Post-Processing
    Line Numbers: 420-520
    """
    line_flows = []
    total_loss_P = 0
    total_loss_Q = 0
    
    for branch in branch_data:
        f, t, r, x, b = branch
        i = int(f) - 1
        j = int(t) - 1
        
        # Calculate branch admittances
        z = complex(r, x)
        y_series = 1 / z
        y_shunt = complex(0, b / 2)
        
        # Current from i to j
        I_ij = (V[i] - V[j]) * y_series + V[i] * y_shunt
        S_ij = V[i] * np.conj(I_ij)
        
        # Current from j to i
        I_ji = (V[j] - V[i]) * y_series + V[j] * y_shunt
        S_ji = V[j] * np.conj(I_ji)
        
        # Branch loss
        S_loss = S_ij + S_ji
        
        total_loss_P += np.real(S_loss)
        total_loss_Q += np.imag(S_loss)
        
        line_flows.append({
            'from': f,
            'to': t,
            'P_ij': np.real(S_ij),
            'Q_ij': np.imag(S_ij),
            'P_ji': np.real(S_ji),
            'Q_ji': np.imag(S_ji),
            'P_loss': np.real(S_loss),
            'Q_loss': np.imag(S_loss)
        })
    
    return line_flows, total_loss_P, total_loss_Q


def print_results(V, P_calc, Q_calc, line_flows, total_loss_P, total_loss_Q, 
                  iteration_data, num_buses):
    """
    Prints formatted results for the load flow analysis.
    
    Flowchart Box 9: Output Display
    Line Numbers: 520-600
    """
    print("\n" + "="*80)
    print("FINAL RESULTS - BUS DATA")
    print("="*80)
    print(f"{'Bus':<6} {'V (pu)':<12} {'Angle (°)':<12} {'P (pu)':<12} {'Q (pu)':<12}")
    print("-"*80)
    
    for i in range(num_buses):
        v_mag = np.abs(V[i])
        v_ang = np.degrees(np.angle(V[i]))
        print(f"{i+1:<6} {v_mag:<12.6f} {v_ang:<12.4f} {P_calc[i]:<12.6f} {Q_calc[i]:<12.6f}")
    
    print("\n" + "="*80)
    print("LINE FLOWS AND LOSSES")
    print("="*80)
    print(f"{'From':<6} {'To':<6} {'P_flow':<12} {'Q_flow':<12} {'P_loss':<12} {'Q_loss':<12}")
    print(f"{'Bus':<6} {'Bus':<6} {'(pu)':<12} {'(pu)':<12} {'(pu)':<12} {'(pu)':<12}")
    print("-"*80)
    
    for flow in line_flows:
        print(f"{flow['from']:<6} {flow['to']:<6} {flow['P_ij']:<12.6f} "
              f"{flow['Q_ij']:<12.6f} {flow['P_loss']:<12.6f} {flow['Q_loss']:<12.6f}")
    
    print("-"*80)
    print(f"{'TOTAL SYSTEM LOSSES:':<24} {total_loss_P:<12.6f} {total_loss_Q:<12.6f}")
    print("="*80)
    
    # Print 2nd iteration details (Task 1 requirement)
    if len(iteration_data) >= 2:
        print("\n" + "="*80)
        print("SECOND ITERATION DETAILS (Task 1 Requirement)")
        print("="*80)
        iter2 = iteration_data[1]
        print(f"Iteration: {iter2['iteration']}")
        print(f"Maximum Mismatch: {iter2['max_mismatch']:.8f} pu")
        print(f"\nVoltage Profile:")
        for i in range(num_buses):
            print(f"  Bus {i+1}: {np.abs(iter2['V'][i]):.6f} ∠ {np.degrees(np.angle(iter2['V'][i])):8.4f}°")
        print(f"\nPower Mismatches:")
        print(f"  ΔP (non-slack buses): {iter2['dP']}")
        print(f"  ΔQ (PQ buses): {iter2['dQ']}")
        print("="*80)


# ==========================================
# LINES 610-700: MAIN PROGRAM
# ==========================================

if __name__ == "__main__":
    print("\n")
    print("*"*80)
    print("*" + " "*78 + "*")
    print("*" + " "*15 + "FULL NEWTON-RAPHSON LOAD FLOW PROGRAM" + " "*27 + "*")
    print("*" + " "*78 + "*")
    print("*" + " "*20 + "IEEE 9-Bus Test System" + " "*37 + "*")
    print("*" + " "*78 + "*")
    print("*" + " "*15 + "EE-354 Power Engineering Assignment" + " "*29 + "*")
    print("*" + " "*78 + "*")
    print("*"*80)
    
    # LINE 625: Student Information
    print("\nStudent ID: [REPLACE WITH YOUR ID]")  # REPLACE THIS
    print("Date: January 2026")
    
    # LINE 629-632: Load system data
    print("\n--- Loading IEEE 9-Bus System Data ---")
    num_buses, bus_types, P_spec, Q_spec, V_init, branch_data = get_ieee_9_bus_data()
    print(f"System loaded: {num_buses} buses, {len(branch_data)} branches")
    
    # LINE 635-638: Build Y-bus matrix
    print("\n--- Constructing Y-Bus Matrix ---")
    start_time = time.time()
    Y_bus = build_y_bus(num_buses, branch_data)
    print(f"Y-bus matrix constructed: {Y_bus.shape}")
    print(f"Time taken: {time.time() - start_time:.6f} seconds")
    
    # Optional: Display Y-bus matrix
    print("\nY-Bus Matrix (first 3x3 elements shown):")
    for i in range(min(3, num_buses)):
        row_str = "  "
        for j in range(min(3, num_buses)):
            row_str += f"{Y_bus[i,j].real:7.3f}{Y_bus[i,j].imag:+7.3f}j  "
        print(row_str)
    print("  ...")
    
    # LINE 652-656: Run Newton-Raphson load flow
    print("\n--- Running Newton-Raphson Load Flow ---")
    start_time = time.time()
    V_final, P_final, Q_final, iter_data = newton_raphson(
        Y_bus, P_spec, Q_spec, V_init, bus_types, 
        max_iter=100, tol=1e-4, verbose=True
    )
    computation_time = time.time() - start_time
    
    # LINE 664-668: Calculate line flows and losses
    print("\n--- Calculating Line Flows and Losses ---")
    line_flows, total_loss_P, total_loss_Q = calculate_line_flows(V_final, branch_data)
    
    # LINE 671-675: Display results
    print_results(V_final, P_final, Q_final, line_flows, total_loss_P, 
                  total_loss_Q, iter_data, num_buses)
    
    # LINE 678-685: Summary statistics
    print("\n" + "="*80)
    print("COMPUTATIONAL STATISTICS")
    print("="*80)
    print(f"Number of iterations to convergence: {len(iter_data)}")
    print(f"Final maximum mismatch: {iter_data[-1]['max_mismatch']:.10f} pu")
    print(f"Total computation time: {computation_time:.6f} seconds")
    print(f"Average time per iteration: {computation_time/len(iter_data):.6f} seconds")
    print("="*80)
    
    print("\n" + "*"*80)
    print("*" + " "*25 + "LOAD FLOW ANALYSIS COMPLETE" + " "*28 + "*")
    print("*"*80 + "\n")
