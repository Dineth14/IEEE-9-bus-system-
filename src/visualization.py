"""
Visualization and Plotting Tools for Load Flow Analysis
========================================================
This script provides comprehensive plotting functions for:
- Voltage profile comparisons
- Convergence characteristics
- Sensitivity analysis results
- Line flow diagrams

Author: [E/21/291]
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def plot_voltage_comparison(results_dict, save_path='voltage_comparison.png'):
    """
    Creates voltage magnitude and angle comparison plots for all methods.
    
    Parameters:
    -----------
    results_dict : dict
        Dictionary containing results from different methods
        Format: {'Method Name': {'V': voltage_array, ...}, ...}
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Extract data
    num_buses = len(list(results_dict.values())[0]['V'])
    buses = np.arange(1, num_buses + 1)
    
    # Plot voltage magnitudes
    for method_name, method_data in results_dict.items():
        V = method_data['V']
        magnitudes = np.abs(V)
        ax1.plot(buses, magnitudes, marker='o', linewidth=2, label=method_name)
    
    ax1.set_xlabel('Bus Number', fontsize=12)
    ax1.set_ylabel('Voltage Magnitude (p.u.)', fontsize=12)
    ax1.set_title('Bus Voltage Magnitude Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(buses)
    
    # Add voltage limits
    ax1.axhline(y=1.05, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Upper Limit (1.05 pu)')
    ax1.axhline(y=0.95, color='r', linestyle='--', linewidth=1, alpha=0.5, label='Lower Limit (0.95 pu)')
    
    # Plot voltage angles
    for method_name, method_data in results_dict.items():
        V = method_data['V']
        angles = np.degrees(np.angle(V))
        ax2.plot(buses, angles, marker='s', linewidth=2, label=method_name)
    
    ax2.set_xlabel('Bus Number', fontsize=12)
    ax2.set_ylabel('Voltage Angle (degrees)', fontsize=12)
    ax2.set_title('Bus Voltage Angle Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(buses)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Voltage comparison plot saved to '{save_path}'")
    plt.show()
    
    return fig


def plot_convergence_comparison(results_dict, save_path='convergence_comparison.png'):
    """
    Creates bar charts comparing convergence characteristics.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    methods = list(results_dict.keys())
    iterations = [results_dict[m]['iterations'] for m in methods]
    times = [results_dict[m]['time'] for m in methods]
    
    # Iterations comparison
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    bars1 = ax1.bar(methods, iterations, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_ylabel('Number of Iterations', fontsize=12)
    ax1.set_title('Convergence: Iterations Required', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Time comparison
    bars2 = ax2.bar(methods, times, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_ylabel('Computation Time (seconds)', fontsize=12)
    ax2.set_title('Convergence: Computation Time', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Convergence comparison plot saved to '{save_path}'")
    plt.show()
    
    return fig


def plot_voltage_difference_heatmap(results_dict, reference_method='Newton-Raphson',
                                     save_path='voltage_difference_heatmap.png'):
    """
    Creates heatmap showing voltage differences from reference method.
    """
    num_buses = len(results_dict[reference_method]['V'])
    V_ref = results_dict[reference_method]['V']
    
    # Calculate differences
    methods = [m for m in results_dict.keys() if m != reference_method]
    diff_matrix = np.zeros((num_buses, len(methods)))
    
    for j, method in enumerate(methods):
        V = results_dict[method]['V']
        diff_matrix[:, j] = np.abs(np.abs(V) - np.abs(V_ref)) * 1000  # Convert to per mille
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(diff_matrix, aspect='auto', cmap='RdYlGn_r', interpolation='nearest')
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(methods)))
    ax.set_yticks(np.arange(num_buses))
    ax.set_xticklabels(methods)
    ax.set_yticklabels([f'Bus {i+1}' for i in range(num_buses)])
    
    # Rotate x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Voltage Magnitude Difference (×10⁻³ pu)', rotation=270, labelpad=20)
    
    # Add text annotations
    for i in range(num_buses):
        for j in range(len(methods)):
            text = ax.text(j, i, f'{diff_matrix[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    ax.set_title(f'Voltage Magnitude Differences from {reference_method} (×10⁻³ pu)',
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Method', fontsize=12)
    ax.set_ylabel('Bus Number', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Voltage difference heatmap saved to '{save_path}'")
    plt.show()
    
    return fig


def plot_power_loss_comparison(results_dict, save_path='power_loss_comparison.png'):
    """
    Creates comparison plot for system power losses.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    methods = list(results_dict.keys())
    p_losses = [results_dict[m]['total_loss_P'] for m in methods]
    q_losses = [results_dict[m]['total_loss_Q'] for m in methods]
    
    x = np.arange(len(methods))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, p_losses, width, label='Real Power Loss (P)', 
                   color='#E63946', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, q_losses, width, label='Reactive Power Loss (Q)', 
                   color='#457B9D', alpha=0.8, edgecolor='black')
    
    ax.set_xlabel('Method', fontsize=12)
    ax.set_ylabel('Power Loss (p.u.)', fontsize=12)
    ax.set_title('System Power Losses Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.6f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Power loss comparison plot saved to '{save_path}'")
    plt.show()
    
    return fig


def plot_sensitivity_analysis_comprehensive(sensitivity_results, 
                                            save_path='sensitivity_comprehensive.png'):
    """
    Creates comprehensive sensitivity analysis visualization.
    """
    num_buses = sensitivity_results['num_buses']
    load_buses = sensitivity_results['load_buses']
    
    # Calculate required rows: 1 row for heatmap/ranking + ceil(n_loads/2) rows for voltage profiles
    n_profile_rows = (len(load_buses) + 1) // 2  # Ceiling division
    total_rows = 1 + n_profile_rows
    
    fig = plt.figure(figsize=(18, 4 + 4*n_profile_rows))
    gs = fig.add_gridspec(total_rows, 3, hspace=0.3, wspace=0.3)
    
    # ==========================================
    # Plot 1: Voltage Variance Heatmap
    # ==========================================
    ax1 = fig.add_subplot(gs[0, :2])
    variance_matrix = np.zeros((num_buses, len(load_buses)))
    for j, load_bus in enumerate(load_buses):
        variance_matrix[:, j] = sensitivity_results['load_analysis'][load_bus]['voltage_variance']
    
    im1 = ax1.imshow(variance_matrix, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    ax1.set_xlabel('Load Bus Varied', fontsize=11)
    ax1.set_ylabel('Bus Number', fontsize=11)
    ax1.set_title('Voltage Variance Heatmap (pu²)', fontsize=13, fontweight='bold')
    ax1.set_xticks(range(len(load_buses)))
    ax1.set_xticklabels(load_buses)
    ax1.set_yticks(range(num_buses))
    ax1.set_yticklabels(range(1, num_buses + 1))
    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label('Variance (pu²)', rotation=270, labelpad=15)
    
    # ==========================================
    # Plot 2: Sensitivity Ranking
    # ==========================================
    ax2 = fig.add_subplot(gs[0, 2])
    avg_variances = [sensitivity_results['load_analysis'][lb]['avg_variance'] for lb in load_buses]
    bars = ax2.barh(range(len(load_buses)), avg_variances, color='steelblue', alpha=0.8, edgecolor='black')
    ax2.set_yticks(range(len(load_buses)))
    ax2.set_yticklabels(load_buses)
    ax2.set_xlabel('Avg Variance (pu²)', fontsize=10)
    ax2.set_ylabel('Load Bus', fontsize=10)
    ax2.set_title('Sensitivity Ranking', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height()/2., 
                f'{width:.2e}', ha='left', va='center', fontsize=8)
    
    # ==========================================
    # Plots 3-5: Voltage Profiles for Each Load Bus
    # ==========================================
    for idx, load_bus in enumerate(load_buses):
        ax = fig.add_subplot(gs[1 + idx//2, idx%2])
        analysis = sensitivity_results['load_analysis'][load_bus]
        
        # Plot only a subset of scenarios for clarity
        scenarios_to_plot = [
            (-10, -10), (-10, 0), (-10, 10),
            (0, -10), (0, 0), (0, 10),
            (10, -10), (10, 0), (10, 10)
        ]
        
        for result in analysis['voltage_results']:
            p_var = result['P_variation']
            q_var = result['Q_variation']
            if (p_var, q_var) in scenarios_to_plot:
                label = f"({p_var:+.0f},{q_var:+.0f})"
                ax.plot(range(1, num_buses + 1), result['voltages'], 
                       marker='o', linewidth=1.5, markersize=4, label=label, alpha=0.7)
        
        ax.set_xlabel('Bus Number', fontsize=10)
        ax.set_ylabel('Voltage (pu)', fontsize=10)
        ax.set_title(f'Load Bus {load_bus} Varied', fontsize=11, fontweight='bold')
        ax.legend(fontsize=7, ncol=3, title='(ΔP%,ΔQ%)')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(1, num_buses + 1))
        ax.axhline(y=1.0, color='k', linestyle='--', linewidth=1, alpha=0.3)
    
    # ==========================================
    # Plot 6: Standard Deviation Comparison
    # ==========================================
    ax_std = fig.add_subplot(gs[2, 2])
    for load_bus in load_buses:
        std = sensitivity_results['load_analysis'][load_bus]['voltage_std']
        ax_std.plot(range(1, num_buses + 1), std, marker='s', 
                   linewidth=2, markersize=6, label=f'Load {load_bus}')
    
    ax_std.set_xlabel('Bus Number', fontsize=10)
    ax_std.set_ylabel('Voltage Std Dev (pu)', fontsize=10)
    ax_std.set_title('Voltage Std Dev at Each Bus', fontsize=11, fontweight='bold')
    ax_std.legend(fontsize=9)
    ax_std.grid(True, alpha=0.3)
    ax_std.set_xticks(range(1, num_buses + 1))
    
    plt.suptitle('Comprehensive Voltage Sensitivity Analysis', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Comprehensive sensitivity analysis plot saved to '{save_path}'")
    plt.show()
    
    return fig


def create_all_plots_for_report():
    """
    Master function to create all plots needed for the assignment report.
    """
    print("="*100)
    print(" "*30 + "GENERATING ALL PLOTS FOR REPORT")
    print("="*100)
    
    # Import necessary modules
    from Task2_Comparison_Framework import run_all_methods
    from Task3_Sensitivity_Analysis import perform_sensitivity_analysis
    
    try:
        # Generate Task 2 plots
        print("\n--- Generating Task 2 Comparison Plots ---")
        task2_results = run_all_methods()
        
        plot_voltage_comparison(task2_results['methods'], 'report_voltage_comparison.png')
        plot_convergence_comparison(task2_results['methods'], 'report_convergence_comparison.png')
        plot_voltage_difference_heatmap(task2_results['methods'], 'Newton-Raphson', 
                                       'report_voltage_difference_heatmap.png')
        plot_power_loss_comparison(task2_results['methods'], 'report_power_loss_comparison.png')
        
        # Generate Task 3 plots
        print("\n--- Generating Task 3 Sensitivity Analysis Plots ---")
        task3_results = perform_sensitivity_analysis()
        plot_sensitivity_analysis_comprehensive(task3_results, 'report_sensitivity_comprehensive.png')
        
        print("\n" + "="*100)
        print("ALL PLOTS GENERATED SUCCESSFULLY!")
        print("="*100)
        print("\nGenerated files:")
        print("  1. report_voltage_comparison.png")
        print("  2. report_convergence_comparison.png")
        print("  3. report_voltage_difference_heatmap.png")
        print("  4. report_power_loss_comparison.png")
        print("  5. report_sensitivity_comprehensive.png")
        print("\nUse these high-quality plots in your assignment report.")
        print("="*100)
        
    except Exception as e:
        print(f"\nError generating plots: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n")
    print("*"*100)
    print("*" + " "*30 + "VISUALIZATION AND PLOTTING TOOLS" + " "*38 + "*")
    print("*"*100)
    print("\nThis script provides plotting functions for your assignment.")
    print("\nOptions:")
    print("  1. Run create_all_plots_for_report() to generate all plots")
    print("  2. Use individual plot functions with your own data")
    print("\nGenerating all plots...")
    print("*"*100 + "\n")
    
    create_all_plots_for_report()
