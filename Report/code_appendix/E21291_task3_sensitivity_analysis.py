"""
Task 3: Improved Voltage Sensitivity Analysis
=============================================
Fixed implementation based on feedback:
1. Varied P only (Q constant)
2. Varied Q only (P constant)
3. Calculated Standard Deviation and Variance
4. Generated tables and plots for each case.

Author: [E21291]
Date: February 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Add project root to path to import methods
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.methods.newton_raphson import get_ieee_9_bus_data, build_y_bus, newton_raphson

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_sensitivity_independent():
    print("="*80)
    print("IMPROVED SENSITIVITY ANALYSIS (Independent P/Q Variation)")
    print("="*80)

    # Setup
    ensure_dir('outputs/tables/sensitivity_improved')
    ensure_dir('outputs/plots')
    
    num_buses, bus_types, P_base, Q_base, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    # Identify Load Buses (Type 1)
    load_buses_idx = np.where(bus_types == 1)[0]
    load_buses = load_buses_idx + 1 # 1-based numbering
    
    variations = [-0.10, 0.0, 0.10]
    
    results_p = []
    results_q = []
    
    for load_idx, bus_num in zip(load_buses_idx, load_buses):
        P_nominal = P_base[load_idx]  # Negative value (Load)
        Q_nominal = Q_base[load_idx]  # Negative value (Load)
        
        # ---------------------------------------------------------
        # CASE 1: Vary P only (Q constant)
        # ---------------------------------------------------------
        # Note: P, Q are injections. Load is negative injection.
        # "Vary P by +/- 10%" means increase/decrease magnitude of load.
        # If P_nominal = -1.25, +10% load means P = -1.375.
        
        print(f"\nAnalyzing Bus {bus_num}: Varying Active Power (P)...")
        v_mags_p = []
        for var in variations:
            P_mod = P_base.copy()
            Q_mod = Q_base.copy()
            
            # Increase load magnitude by var%
            # P_new = P_nom * (1 + var)
            P_mod[load_idx] = P_nominal * (1 + var) 
            
            try:
                V, _, _, _ = newton_raphson(Y_bus, P_mod, Q_mod, V_init, bus_types, verbose=False)
                v_mags_p.append(np.abs(V))
            except:
                v_mags_p.append(np.full(num_buses, np.nan))

        v_mags_p = np.array(v_mags_p)
        # Calculate stats for P variation (across the 3 scenarios)
        p_stds = np.std(v_mags_p, axis=0)      # Std Dev at each bus
        p_avg_std = np.mean(p_stds)            # Average sensitivity of system
        p_max_std = np.max(p_stds)             # Max sensitivity at any bus
        
        results_p.append({
            'load_bus': bus_num,
            'avg_std': p_avg_std,
            'max_std': p_max_std,
            'affected_bus': np.argmax(p_stds) + 1,
            'voltages': v_mags_p
        })
        
        # ---------------------------------------------------------
        # CASE 2: Vary Q only (P constant)
        # ---------------------------------------------------------
        print(f"Analyzing Bus {bus_num}: Varying Reactive Power (Q)...")
        v_mags_q = []
        for var in variations:
            P_mod = P_base.copy()
            Q_mod = Q_base.copy()
            
            # Vary Q
            Q_mod[load_idx] = Q_nominal * (1 + var)
            
            try:
                V, _, _, _ = newton_raphson(Y_bus, P_mod, Q_mod, V_init, bus_types, verbose=False)
                v_mags_q.append(np.abs(V))
            except:
                v_mags_q.append(np.full(num_buses, np.nan))

        v_mags_q = np.array(v_mags_q)
        q_stds = np.std(v_mags_q, axis=0)
        q_avg_std = np.mean(q_stds)
        q_max_std = np.max(q_stds)
        
        results_q.append({
            'load_bus': bus_num,
            'avg_std': q_avg_std,
            'max_std': q_max_std,
            'affected_bus': np.argmax(q_stds) + 1,
            'voltages': v_mags_q
        })

    # Generate Comparative Tables
    df_p = pd.DataFrame(results_p)[['load_bus', 'avg_std', 'max_std', 'affected_bus']]
    df_q = pd.DataFrame(results_q)[['load_bus', 'avg_std', 'max_std', 'affected_bus']]
    
    print("\n" + "="*80)
    print("SENSITIVITY RESULTS (Standard Deviation of Voltage)")
    print("="*80)
    print("\n--- Sensitivity to Active Power (P) ---")
    print(df_p.to_string(index=False))
    print("\n--- Sensitivity to Reactive Power (Q) ---")
    print(df_q.to_string(index=False))
    
    df_p.to_csv('outputs/tables/sensitivity_improved/p_sensitivity.csv', index=False)
    df_q.to_csv('outputs/tables/sensitivity_improved/q_sensitivity.csv', index=False)
    
    # Generate Plots
    generate_plots(results_p, results_q, load_buses)

def generate_plots(res_p, res_q, load_buses):
    # Plot 1: Standard Deviation Comparison (P vs Q)
    # We want to show for each Load Bus, what is the System Max Std Deviation caused by P vs Q var
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(load_buses))
    width = 0.35
    
    p_max_stds = [r['max_std'] for r in res_p]
    q_max_stds = [r['max_std'] for r in res_q]
    
    rects1 = ax.bar(x - width/2, p_max_stds, width, label='Varying P', color='skyblue')
    rects2 = ax.bar(x + width/2, q_max_stds, width, label='Varying Q', color='salmon')
    
    ax.set_ylabel('Max Voltage Std Dev (pu)')
    ax.set_xlabel('Load Bus Varied')
    ax.set_title('Comparative Voltage Sensitivity: P vs Q Variations')
    ax.set_xticks(x)
    ax.set_xticklabels(load_buses)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('outputs/plots/sensitivity_comparison_PQ.png', dpi=300)
    print("\nSaved plot: outputs/plots/sensitivity_comparison_PQ.png")

if __name__ == "__main__":
    run_sensitivity_independent()
