"""
Full Newton-Raphson Load Flow Program for IEEE 9-Bus System
============================================================
Student Name: PERERA J.D.T.
Student ID: E/21/291
Date: February 14, 2026

This program implements the Full Newton-Raphson method for solving power flow equations.
All matrices (Y-bus, Jacobian submatrices J1-J4) are constructed from first principles.
"""

import numpy as np
import time
import pandas as pd
import os
from datetime import datetime

# ==========================================
# DATA INPUT AND Y-BUS CONSTRUCTION
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
    """
    num_buses = 9
    
    # Bus Types: 0=Slack, 1=PQ, 2=PV
    bus_types = np.array([0, 2, 2, 1, 1, 1, 1, 1, 1])
    
    # Specified P and Q in per unit (pu)
    P_specified = np.zeros(num_buses)
    Q_specified = np.zeros(num_buses)
    
    # Generators (Generation is positive)
    P_specified[1] = 1.63  # Bus 2
    P_specified[2] = 0.85  # Bus 3
    
    # Loads (Load is negative)
    P_specified[4] = -1.25  # Bus 5
    Q_specified[4] = -0.50
    P_specified[5] = -0.90  # Bus 6
    Q_specified[5] = -0.30
    P_specified[7] = -1.00  # Bus 8
    Q_specified[7] = -0.35
    
    # Initial Voltages
    V_init = np.ones(num_buses, dtype=complex)
    V_init[0] = 1.04 + 0j   # Slack
    V_init[1] = 1.025 + 0j  # PV
    V_init[2] = 1.025 + 0j  # PV
    
    # Branch Data: (From, To, R, X, B)
    branch_data = [
        (4, 5, 0.0100, 0.0850, 0.1760),
        (4, 6, 0.0170, 0.0920, 0.1580),
        (5, 7, 0.0320, 0.1610, 0.3060),
        (6, 9, 0.0390, 0.1700, 0.3580),
        (7, 8, 0.0085, 0.0720, 0.1490),
        (8, 9, 0.0119, 0.1008, 0.2090),
        (1, 4, 0.0, 0.0576, 0.0),
        (2, 7, 0.0, 0.0625, 0.0),
        (3, 9, 0.0, 0.0586, 0.0)
    ]
    
    return num_buses, bus_types, P_specified, Q_specified, V_init, branch_data


def build_y_bus(num_buses, branch_data):
    """
    Constructs the Y-bus admittance matrix from branch data.
    """
    Y_bus = np.zeros((num_buses, num_buses), dtype=complex)
    
    for branch in branch_data:
        f, t, r, x, b = branch
        i = int(f) - 1
        j = int(t) - 1
        
        z = complex(r, x)
        y_series = 1 / z
        y_shunt = complex(0, b / 2)
        
        Y_bus[i, i] += y_series + y_shunt
        Y_bus[j, j] += y_series + y_shunt
        Y_bus[i, j] -= y_series
        Y_bus[j, i] -= y_series
        
    return Y_bus

# ==========================================
# NEWTON-RAPHSON ALGORITHM
# ==========================================

def newton_raphson(Y_bus, P_specified, Q_specified, V_init, bus_types, 
                   max_iter=100, tol=1e-4, verbose=True):
    """
    Solves power flow equations using Full Newton-Raphson method.
    """
    num_buses = len(Y_bus)
    V = np.array(V_init, copy=True)
    
    slack_bus = np.where(bus_types == 0)[0][0]
    pq_buses = np.where(bus_types == 1)[0]
    pv_buses = np.where(bus_types == 2)[0]
    non_slack_buses = np.sort(np.concatenate((pq_buses, pv_buses)))
    
    iteration_data = []
    
    if verbose:
        print("\n" + "="*80)
        print("STARTING NEWTON-RAPHSON LOAD FLOW ANALYSIS")
        print("="*80)
    
    for iteration in range(max_iter):
        if verbose:
            print(f"\n--- ITERATION {iteration + 1} ---")
        
        S_calc = V * np.conj(Y_bus @ V)
        P_calc = np.real(S_calc)
        Q_calc = np.imag(S_calc)
        
        dP = P_specified[non_slack_buses] - P_calc[non_slack_buses]
        dQ = Q_specified[pq_buses] - Q_calc[pq_buses]
        
        mismatch = np.concatenate((dP, dQ))
        max_mismatch = np.max(np.abs(mismatch))
        
        if verbose:
            print(f"Maximum power mismatch: {max_mismatch:.6f} pu")
        
        iteration_data.append({
            'iteration': iteration + 1,
            'V': V.copy(),
            'P_calc': P_calc.copy(),
            'Q_calc': Q_calc.copy(),
            'dP': dP.copy(),
            'dQ': dQ.copy(),
            'max_mismatch': max_mismatch
        })
        
        if max_mismatch < tol:
            if verbose:
                print(f"\n{'='*80}")
                print(f"CONVERGED in {iteration + 1} iterations!")
                print(f"{'='*80}")
            return V, P_calc, Q_calc, iteration_data
        
        n_non_slack = len(non_slack_buses)
        n_pq = len(pq_buses)
        
        J1 = np.zeros((n_non_slack, n_non_slack))
        J2 = np.zeros((n_non_slack, n_pq))
        J3 = np.zeros((n_pq, n_non_slack))
        J4 = np.zeros((n_pq, n_pq))
        
        # J1 and J3
        for r, i in enumerate(non_slack_buses):
            for c, k in enumerate(non_slack_buses):
                if i == k:
                    J1[r, c] = -Q_calc[i] - np.imag(Y_bus[i, i]) * np.abs(V[i])**2
                else:
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J1[r, c] = np.abs(V[i] * V[k]) * (np.real(y_ik) * np.sin(delta_ik) - np.imag(y_ik) * np.cos(delta_ik))
        
        for r, i in enumerate(pq_buses):
            for c, k in enumerate(non_slack_buses):
                if i == k:
                    J3[r, c] = P_calc[i] - np.real(Y_bus[i, i]) * np.abs(V[i])**2
                else:
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J3[r, c] = -np.abs(V[i] * V[k]) * (np.real(y_ik) * np.cos(delta_ik) + np.imag(y_ik) * np.sin(delta_ik))
        
        # J2 and J4
        for r, i in enumerate(non_slack_buses):
            for c, k in enumerate(pq_buses):
                if i == k:
                    J2[r, c] = P_calc[i] / np.abs(V[i]) + np.real(Y_bus[i, i]) * np.abs(V[i])
                else:
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J2[r, c] = np.abs(V[i]) * (np.real(y_ik) * np.cos(delta_ik) + np.imag(y_ik) * np.sin(delta_ik))
        
        for r, i in enumerate(pq_buses):
            for c, k in enumerate(pq_buses):
                if i == k:
                    J4[r, c] = Q_calc[i] / np.abs(V[i]) - np.imag(Y_bus[i, i]) * np.abs(V[i])
                else:
                    y_ik = Y_bus[i, k]
                    delta_ik = np.angle(V[i]) - np.angle(V[k])
                    J4[r, c] = np.abs(V[i]) * (np.real(y_ik) * np.sin(delta_ik) - np.imag(y_ik) * np.cos(delta_ik))
        
        J = np.block([[J1, J2], [J3, J4]])
        dx = np.linalg.solve(J, mismatch)
        
        d_angle = dx[:n_non_slack]
        d_vmag = dx[n_non_slack:]
        
        current_angles = np.angle(V)
        current_angles[non_slack_buses] += d_angle
        
        current_mags = np.abs(V)
        current_mags[pq_buses] += d_vmag
        
        V = current_mags * np.exp(1j * current_angles)
    
    return V, P_calc, Q_calc, iteration_data


def calculate_line_flows(V, branch_data):
    """
    Calculates power flows and losses.
    """
    line_flows = []
    total_loss_P = 0
    total_loss_Q = 0
    
    for branch in branch_data:
        f, t, r, x, b = branch
        i = int(f) - 1
        j = int(t) - 1
        
        z = complex(r, x)
        y_series = 1 / z
        y_shunt = complex(0, b / 2)
        
        I_ij = (V[i] - V[j]) * y_series + V[i] * y_shunt
        S_ij = V[i] * np.conj(I_ij)
        
        I_ji = (V[j] - V[i]) * y_series + V[j] * y_shunt
        S_ji = V[j] * np.conj(I_ji)
        
        S_loss = S_ij + S_ji
        total_loss_P += np.real(S_loss)
        total_loss_Q += np.imag(S_loss)
        
        line_flows.append({
            'from': f, 'to': t,
            'P_ij': np.real(S_ij), 'Q_ij': np.imag(S_ij),
            'P_ji': np.real(S_ji), 'Q_ji': np.imag(S_ji),
            'P_loss': np.real(S_loss), 'Q_loss': np.imag(S_loss)
        })
    
    return line_flows, total_loss_P, total_loss_Q


def print_results(V, P_calc, Q_calc, line_flows, total_loss_P, total_loss_Q, num_buses):
    """
    Prints results to console.
    """
    print("\n" + "="*80)
    print("FINAL RESULTS - BUS DATA")
    print("="*80)
    print(f"{'Bus':<6} {'V (pu)':<12} {'Angle (°)':<12} {'P (pu)':<12} {'Q (pu)':<12}")
    print("-"*80)
    
    for i in range(num_buses):
        print(f"{i+1:<6} {np.abs(V[i]):<12.6f} {np.degrees(np.angle(V[i])):<12.4f} {P_calc[i]:<12.6f} {Q_calc[i]:<12.6f}")
    
    print("\n" + "="*80)
    print("LINE FLOWS AND LOSSES")
    print("="*80)
    print(f"{'From':<6} {'To':<6} {'P_flow':<12} {'Q_flow':<12} {'P_loss':<12} {'Q_loss':<12}")
    print("-"*80)
    
    for flow in line_flows:
        print(f"{flow['from']:<6} {flow['to']:<6} {flow['P_ij']:<12.6f} {flow['Q_ij']:<12.6f} {flow['P_loss']:<12.6f} {flow['Q_loss']:<12.6f}")
    
    print("-"*80)
    print(f"{'TOTAL SYSTEM LOSSES:':<24} {total_loss_P:<12.6f} {total_loss_Q:<12.6f}")
    print("="*80)


def save_results_to_csv(V, P_calc, Q_calc, line_flows, total_loss_P, total_loss_Q, num_buses):
    """
    Saves results to CSV (for reporting graphs).
    """
    if not os.path.exists('outputs/tables'):
        os.makedirs('outputs/tables')
        
    bus_data = []
    for i in range(num_buses):
        bus_data.append({
            'Bus': i + 1,
            'Voltage_pu': np.abs(V[i]),
            'Angle_deg': np.degrees(np.angle(V[i])),
            'P_pu': P_calc[i],
            'Q_pu': Q_calc[i]
        })
    pd.DataFrame(bus_data).to_csv('outputs/tables/bus_results.csv', index=False)
    
    pd.DataFrame(line_flows).to_csv('outputs/tables/line_flows.csv', index=False)
    
    with open('outputs/tables/system_losses.txt', 'w') as f:
        f.write(f"Total Active Power Loss: {total_loss_P:.6f} pu\n")
        f.write(f"Total Reactive Power Loss: {total_loss_Q:.6f} pu\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("FULL NEWTON-RAPHSON LOAD FLOW PROGRAM (Single File Submission)")
    print("="*80)
    print(f"Student ID: E/21/291")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*80)
    
    num_buses, bus_types, P_spec, Q_spec, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    V_final, P_final, Q_final, iter_data = newton_raphson(
        Y_bus, P_spec, Q_spec, V_init, bus_types, verbose=True
    )
    
    line_flows, total_loss_P, total_loss_Q = calculate_line_flows(V_final, branch_data)
    
    print_results(V_final, P_final, Q_final, line_flows, total_loss_P, total_loss_Q, num_buses)
    save_results_to_csv(V_final, P_final, Q_final, line_flows, total_loss_P, total_loss_Q, num_buses)
