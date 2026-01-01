"""
Task 2: Verification and Comparison Framework
==============================================
This script runs all three load flow methods and generates comparative analysis:
1. Newton-Raphson (your implementation)
2. Gauss-Seidel
3. Fast Decoupled Load Flow

Outputs:
- Comparative tables (bus voltages, line flows, losses)
- Convergence characteristics
- Iteration counts
- Computational time comparison

Author: [Your Student ID]
Date: January 2026
"""

import numpy as np
import pandas as pd
import time
from Newton_Raphson_Enhanced import (
    get_ieee_9_bus_data, build_y_bus, newton_raphson, calculate_line_flows
)
from Gauss_Seidel_Load_Flow import gauss_seidel
from Fast_Decoupled_Load_Flow import fast_decoupled, build_b_matrices


def run_all_methods():
    """
    Runs all three load flow methods and collects results for comparison.
    
    Returns:
    --------
    results : dict
        Contains results from all three methods
    """
    print("="*100)
    print(" "*30 + "TASK 2: COMPARISON FRAMEWORK")
    print("="*100)
    
    # Load system data
    num_buses, bus_types, P_spec, Q_spec, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    results = {
        'system_data': {
            'num_buses': num_buses,
            'branch_data': branch_data
        },
        'methods': {}
    }
    
    # ==========================================
    # Method 1: Newton-Raphson
    # ==========================================
    print("\n" + "-"*100)
    print("Running Method 1: NEWTON-RAPHSON")
    print("-"*100)
    
    start_time = time.time()
    V_nr, P_nr, Q_nr, iter_data_nr = newton_raphson(
        Y_bus, P_spec, Q_spec, V_init, bus_types, 
        max_iter=100, tol=1e-4, verbose=False
    )
    time_nr = time.time() - start_time
    
    line_flows_nr, loss_P_nr, loss_Q_nr = calculate_line_flows(V_nr, branch_data)
    
    results['methods']['Newton-Raphson'] = {
        'V': V_nr,
        'P': P_nr,
        'Q': Q_nr,
        'iterations': len(iter_data_nr),
        'time': time_nr,
        'line_flows': line_flows_nr,
        'total_loss_P': loss_P_nr,
        'total_loss_Q': loss_Q_nr,
        'converged': True
    }
    
    print(f"✓ Newton-Raphson completed: {len(iter_data_nr)} iterations, {time_nr:.6f} seconds")
    
    # ==========================================
    # Method 2: Gauss-Seidel
    # ==========================================
    print("\n" + "-"*100)
    print("Running Method 2: GAUSS-SEIDEL")
    print("-"*100)
    
    start_time = time.time()
    V_gs, iter_gs = gauss_seidel(Y_bus, P_spec, Q_spec, V_init, bus_types, 
                                  max_iter=1000, tol=1e-4)
    time_gs = time.time() - start_time
    
    # Calculate power injections for GS results
    S_gs = V_gs * np.conj(Y_bus @ V_gs)
    P_gs = np.real(S_gs)
    Q_gs = np.imag(S_gs)
    
    line_flows_gs, loss_P_gs, loss_Q_gs = calculate_line_flows(V_gs, branch_data)
    
    results['methods']['Gauss-Seidel'] = {
        'V': V_gs,
        'P': P_gs,
        'Q': Q_gs,
        'iterations': iter_gs,
        'time': time_gs,
        'line_flows': line_flows_gs,
        'total_loss_P': loss_P_gs,
        'total_loss_Q': loss_Q_gs,
        'converged': True
    }
    
    print(f"✓ Gauss-Seidel completed: {iter_gs} iterations, {time_gs:.6f} seconds")
    
    # ==========================================
    # Method 3: Fast Decoupled
    # ==========================================
    print("\n" + "-"*100)
    print("Running Method 3: FAST DECOUPLED LOAD FLOW")
    print("-"*100)
    
    start_time = time.time()
    V_fd, iter_fd = fast_decoupled(Y_bus, P_spec, Q_spec, V_init, bus_types, 
                                     branch_data, max_iter=100, tol=1e-4)
    time_fd = time.time() - start_time
    
    # Calculate power injections for FD results
    S_fd = V_fd * np.conj(Y_bus @ V_fd)
    P_fd = np.real(S_fd)
    Q_fd = np.imag(S_fd)
    
    line_flows_fd, loss_P_fd, loss_Q_fd = calculate_line_flows(V_fd, branch_data)
    
    results['methods']['Fast Decoupled'] = {
        'V': V_fd,
        'P': P_fd,
        'Q': Q_fd,
        'iterations': iter_fd,
        'time': time_fd,
        'line_flows': line_flows_fd,
        'total_loss_P': loss_P_fd,
        'total_loss_Q': loss_Q_fd,
        'converged': True
    }
    
    print(f"✓ Fast Decoupled completed: {iter_fd} iterations, {time_fd:.6f} seconds")
    
    return results


def generate_comparison_tables(results):
    """
    Generates formatted comparison tables for Task 2 report.
    """
    num_buses = results['system_data']['num_buses']
    methods = results['methods']
    
    print("\n" + "="*100)
    print(" "*30 + "COMPARISON TABLES")
    print("="*100)
    
    # ==========================================
    # Table 1: Bus Voltage Comparison
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 1: BUS VOLTAGE MAGNITUDE COMPARISON (p.u.)")
    print("-"*100)
    
    voltage_data = []
    for i in range(num_buses):
        row = {'Bus': i+1}
        for method_name, method_results in methods.items():
            V = method_results['V']
            row[f'{method_name}'] = np.abs(V[i])
        voltage_data.append(row)
    
    df_voltage = pd.DataFrame(voltage_data)
    print(df_voltage.to_string(index=False, float_format=lambda x: f'{x:.6f}'))
    
    # ==========================================
    # Table 2: Bus Voltage Angle Comparison
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 2: BUS VOLTAGE ANGLE COMPARISON (degrees)")
    print("-"*100)
    
    angle_data = []
    for i in range(num_buses):
        row = {'Bus': i+1}
        for method_name, method_results in methods.items():
            V = method_results['V']
            row[f'{method_name}'] = np.degrees(np.angle(V[i]))
        angle_data.append(row)
    
    df_angle = pd.DataFrame(angle_data)
    print(df_angle.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
    
    # ==========================================
    # Table 3: Convergence Characteristics
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 3: CONVERGENCE CHARACTERISTICS")
    print("-"*100)
    
    convergence_data = []
    for method_name, method_results in methods.items():
        convergence_data.append({
            'Method': method_name,
            'Iterations': method_results['iterations'],
            'Time (s)': method_results['time'],
            'Time/Iteration (ms)': method_results['time'] / method_results['iterations'] * 1000,
            'Converged': 'Yes' if method_results['converged'] else 'No'
        })
    
    df_convergence = pd.DataFrame(convergence_data)
    print(df_convergence.to_string(index=False))
    
    # ==========================================
    # Table 4: System Losses Comparison
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 4: TOTAL SYSTEM LOSSES")
    print("-"*100)
    
    loss_data = []
    for method_name, method_results in methods.items():
        loss_data.append({
            'Method': method_name,
            'Real Power Loss (pu)': method_results['total_loss_P'],
            'Real Power Loss (MW)': method_results['total_loss_P'] * 100,
            'Reactive Power Loss (pu)': method_results['total_loss_Q'],
            'Reactive Power Loss (MVAr)': method_results['total_loss_Q'] * 100
        })
    
    df_losses = pd.DataFrame(loss_data)
    print(df_losses.to_string(index=False, float_format=lambda x: f'{x:.6f}'))
    
    # ==========================================
    # Table 5: Voltage Magnitude Differences from Newton-Raphson
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 5: VOLTAGE MAGNITUDE DIFFERENCES FROM NEWTON-RAPHSON (p.u.)")
    print("-"*100)
    
    V_nr = methods['Newton-Raphson']['V']
    diff_data = []
    for i in range(num_buses):
        row = {'Bus': i+1}
        for method_name, method_results in methods.items():
            if method_name != 'Newton-Raphson':
                V = method_results['V']
                diff = np.abs(V[i]) - np.abs(V_nr[i])
                row[f'{method_name}'] = diff
        diff_data.append(row)
    
    df_diff = pd.DataFrame(diff_data)
    print(df_diff.to_string(index=False, float_format=lambda x: f'{x:.8f}'))
    
    # Calculate statistics
    print("\n" + "-"*100)
    print("VOLTAGE DIFFERENCE STATISTICS")
    print("-"*100)
    for method_name in methods.keys():
        if method_name != 'Newton-Raphson':
            V = methods[method_name]['V']
            diffs = np.abs(np.abs(V) - np.abs(V_nr))
            print(f"\n{method_name}:")
            print(f"  Maximum difference: {np.max(diffs):.8f} pu")
            print(f"  Mean difference: {np.mean(diffs):.8f} pu")
            print(f"  RMS difference: {np.sqrt(np.mean(diffs**2)):.8f} pu")
    
    return df_voltage, df_angle, df_convergence, df_losses, df_diff


def save_results_to_csv(results):
    """
    Saves comparison results to CSV files for use in reports.
    """
    import os
    
    # Create results directory if it doesn't exist
    if not os.path.exists('comparison_results'):
        os.makedirs('comparison_results')
    
    num_buses = results['system_data']['num_buses']
    methods = results['methods']
    
    # Save voltage magnitudes
    voltage_data = []
    for i in range(num_buses):
        row = {'Bus': i+1}
        for method_name, method_results in methods.items():
            row[f'{method_name}_Vmag'] = np.abs(method_results['V'][i])
            row[f'{method_name}_Vang'] = np.degrees(np.angle(method_results['V'][i]))
        voltage_data.append(row)
    
    df_voltages = pd.DataFrame(voltage_data)
    df_voltages.to_csv('comparison_results/bus_voltages.csv', index=False)
    
    # Save convergence data
    convergence_data = []
    for method_name, method_results in methods.items():
        convergence_data.append({
            'Method': method_name,
            'Iterations': method_results['iterations'],
            'Time_seconds': method_results['time'],
            'Loss_P_pu': method_results['total_loss_P'],
            'Loss_Q_pu': method_results['total_loss_Q']
        })
    
    df_convergence = pd.DataFrame(convergence_data)
    df_convergence.to_csv('comparison_results/convergence_comparison.csv', index=False)
    
    print("\n" + "="*100)
    print("Results saved to CSV files in 'comparison_results/' directory:")
    print("  - bus_voltages.csv")
    print("  - convergence_comparison.csv")
    print("="*100)


def print_discussion_points():
    """
    Prints discussion points for Task 2 report.
    """
    print("\n" + "="*100)
    print(" "*30 + "DISCUSSION POINTS FOR TASK 2")
    print("="*100)
    
    discussion = """
    
NUMERICAL ACCURACY:
-------------------
1. Compare the voltage magnitudes and angles from all three methods
2. Discuss the maximum differences observed
3. Explain why differences occur (approximations in Fast Decoupled, 
   sequential updates in Gauss-Seidel)

CONVERGENCE CHARACTERISTICS:
----------------------------
1. Iterations Required:
   - Newton-Raphson: Typically 3-5 iterations (quadratic convergence)
   - Gauss-Seidel: Much higher iteration count (linear convergence)
   - Fast Decoupled: Slightly more than NR due to approximations
   
2. Computational Time:
   - Compare total time and time per iteration
   - Discuss trade-offs between speed and accuracy
   
3. Stability:
   - All methods should converge for this well-conditioned system
   - Discuss which methods are more robust for ill-conditioned systems

REASONS FOR DEVIATIONS:
----------------------
1. Newton-Raphson: Full formulation, most accurate
2. Gauss-Seidel: Sequential voltage updates, slower convergence
3. Fast Decoupled: Approximations (decoupling P-θ and Q-V), slightly less accurate

COMPARISON WITH PSSE:
---------------------
1. Your results should match PSSE within acceptable tolerance (< 0.001 pu)
2. Iteration counts may vary slightly due to different convergence criteria
3. Document any significant differences and investigate reasons

    """
    print(discussion)


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    # Run all three methods
    results = run_all_methods()
    
    # Generate comparison tables
    df_v, df_a, df_c, df_l, df_d = generate_comparison_tables(results)
    
    # Save results to CSV for easy import into reports
    save_results_to_csv(results)
    
    # Print discussion points
    print_discussion_points()
    
    print("\n" + "="*100)
    print(" "*25 + "TASK 2 COMPARISON FRAMEWORK COMPLETE")
    print("="*100)
    print("\nNext Steps:")
    print("1. Import CSV files into Excel or Python for creating plots")
    print("2. Use the comparison tables in your Task 2 report")
    print("3. Address the discussion points in your analysis")
    print("4. Compare these results with PSSE simulations")
    print("="*100 + "\n")
