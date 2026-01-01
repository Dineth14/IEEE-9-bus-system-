"""
Task 3: Voltage Sensitivity Analysis
=====================================
This script performs voltage sensitivity analysis on the IEEE 9-bus system
by varying load P and Q values and analyzing voltage responses.

For each load bus:
1. Vary P and Q by -10%, 0%, and +10% independently
2. Record voltage magnitudes at all buses
3. Calculate variance and standard deviation
4. Identify which load has the highest influence on system voltages

Author: [Your Student ID]
Date: January 2026
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from methods.newton_raphson import (
    get_ieee_9_bus_data, build_y_bus, newton_raphson
)


def perform_sensitivity_analysis():
    """
    Performs voltage sensitivity analysis for all load buses.
    
    Returns:
    --------
    sensitivity_results : dict
        Complete sensitivity analysis results
    """
    print("="*100)
    print(" "*30 + "TASK 3: VOLTAGE SENSITIVITY ANALYSIS")
    print("="*100)
    
    # Load base case data
    num_buses, bus_types, P_base, Q_base, V_init, branch_data = get_ieee_9_bus_data()
    Y_bus = build_y_bus(num_buses, branch_data)
    
    # Identify load buses (PQ buses)
    load_buses = np.where(bus_types == 1)[0]
    load_bus_numbers = load_buses + 1  # Convert to 1-based numbering
    
    print(f"\nBase case configuration:")
    print(f"  Total buses: {num_buses}")
    print(f"  Load buses: {load_bus_numbers}")
    print(f"  Variation levels: -10%, 0%, +10%")
    
    # Variation percentages
    variations = [-0.10, 0.00, 0.10]
    
    # Storage for results
    sensitivity_results = {
        'num_buses': num_buses,
        'load_buses': load_bus_numbers,
        'variations': variations,
        'load_analysis': {}
    }
    
    # Run base case first
    print("\n" + "-"*100)
    print("Running BASE CASE (no load variations)")
    print("-"*100)
    
    V_base, P_calc_base, Q_calc_base, _ = newton_raphson(
        Y_bus, P_base, Q_base, V_init, bus_types, 
        max_iter=100, tol=1e-4, verbose=False
    )
    
    base_voltages = np.abs(V_base)
    print(f"✓ Base case completed")
    print(f"  Base case voltages (pu): {base_voltages}")
    
    # ==========================================
    # Analyze each load bus
    # ==========================================
    for load_bus_idx in load_buses:
        load_bus_num = load_bus_idx + 1
        
        print("\n" + "="*100)
        print(f"ANALYZING LOAD BUS {load_bus_num}")
        print("="*100)
        
        # Get base load values
        P_load_base = P_base[load_bus_idx]
        Q_load_base = Q_base[load_bus_idx]
        
        print(f"Base load: P = {P_load_base:.4f} pu, Q = {Q_load_base:.4f} pu")
        
        # Storage for this load bus
        voltage_results = []
        
        # Vary P and Q
        for p_var in variations:
            for q_var in variations:
                # Create modified load scenario
                P_modified = P_base.copy()
                Q_modified = Q_base.copy()
                
                P_modified[load_bus_idx] = P_load_base * (1 + p_var)
                Q_modified[load_bus_idx] = Q_load_base * (1 + q_var)
                
                # Run load flow with modified loads
                try:
                    V_result, _, _, _ = newton_raphson(
                        Y_bus, P_modified, Q_modified, V_init, bus_types,
                        max_iter=100, tol=1e-4, verbose=False
                    )
                    
                    # Store voltage magnitudes
                    voltage_mags = np.abs(V_result)
                    
                    voltage_results.append({
                        'P_variation': p_var * 100,
                        'Q_variation': q_var * 100,
                        'P_load': P_modified[load_bus_idx],
                        'Q_load': Q_modified[load_bus_idx],
                        'voltages': voltage_mags
                    })
                    
                    print(f"  ΔP = {p_var*100:+5.1f}%, ΔQ = {q_var*100:+5.1f}%  →  V_min = {np.min(voltage_mags):.6f} pu")
                    
                except Exception as e:
                    print(f"  ΔP = {p_var*100:+5.1f}%, ΔQ = {q_var*100:+5.1f}%  →  FAILED: {str(e)}")
        
        # Calculate statistics for this load bus
        all_voltages = np.array([result['voltages'] for result in voltage_results])
        
        # Calculate variance and standard deviation for each bus
        voltage_variance = np.var(all_voltages, axis=0)
        voltage_std = np.std(all_voltages, axis=0)
        voltage_mean = np.mean(all_voltages, axis=0)
        
        # Overall sensitivity metric (average variance across all buses)
        avg_variance = np.mean(voltage_variance)
        max_variance = np.max(voltage_variance)
        
        sensitivity_results['load_analysis'][load_bus_num] = {
            'voltage_results': voltage_results,
            'voltage_variance': voltage_variance,
            'voltage_std': voltage_std,
            'voltage_mean': voltage_mean,
            'avg_variance': avg_variance,
            'max_variance': max_variance,
            'all_voltages': all_voltages
        }
        
        print(f"\n  Statistics for load bus {load_bus_num}:")
        print(f"    Average voltage variance: {avg_variance:.8f} pu²")
        print(f"    Maximum voltage variance: {max_variance:.8f} pu²")
        print(f"    Average voltage std dev: {np.mean(voltage_std):.8f} pu")
    
    return sensitivity_results


def generate_sensitivity_tables(results):
    """
    Generates formatted tables for Task 3 report.
    """
    print("\n" + "="*100)
    print(" "*30 + "SENSITIVITY ANALYSIS TABLES")
    print("="*100)
    
    num_buses = results['num_buses']
    load_buses = results['load_buses']
    
    # ==========================================
    # Table 1: Voltage Variance by Bus
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 1: VOLTAGE VARIANCE FOR EACH BUS DUE TO LOAD VARIATIONS (pu²)")
    print("-"*100)
    
    variance_data = []
    for bus in range(num_buses):
        row = {'Bus': bus + 1}
        for load_bus in load_buses:
            variance = results['load_analysis'][load_bus]['voltage_variance'][bus]
            row[f'Load {load_bus}'] = variance
        variance_data.append(row)
    
    df_variance = pd.DataFrame(variance_data)
    print(df_variance.to_string(index=False, float_format=lambda x: f'{x:.8f}'))
    
    # ==========================================
    # Table 2: Voltage Standard Deviation by Bus
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 2: VOLTAGE STANDARD DEVIATION FOR EACH BUS DUE TO LOAD VARIATIONS (pu)")
    print("-"*100)
    
    std_data = []
    for bus in range(num_buses):
        row = {'Bus': bus + 1}
        for load_bus in load_buses:
            std = results['load_analysis'][load_bus]['voltage_std'][bus]
            row[f'Load {load_bus}'] = std
        std_data.append(row)
    
    df_std = pd.DataFrame(std_data)
    print(df_std.to_string(index=False, float_format=lambda x: f'{x:.8f}'))
    
    # ==========================================
    # Table 3: Sensitivity Ranking
    # ==========================================
    print("\n" + "-"*100)
    print("TABLE 3: LOAD BUS SENSITIVITY RANKING")
    print("-"*100)
    
    ranking_data = []
    for load_bus in load_buses:
        analysis = results['load_analysis'][load_bus]
        ranking_data.append({
            'Load Bus': load_bus,
            'Average Variance (pu²)': analysis['avg_variance'],
            'Maximum Variance (pu²)': analysis['max_variance'],
            'Average Std Dev (pu)': np.mean(analysis['voltage_std']),
            'Maximum Std Dev (pu)': np.max(analysis['voltage_std'])
        })
    
    df_ranking = pd.DataFrame(ranking_data)
    df_ranking = df_ranking.sort_values('Average Variance (pu²)', ascending=False)
    df_ranking['Rank'] = range(1, len(df_ranking) + 1)
    
    # Reorder columns
    df_ranking = df_ranking[['Rank', 'Load Bus', 'Average Variance (pu²)', 
                              'Maximum Variance (pu²)', 'Average Std Dev (pu)', 
                              'Maximum Std Dev (pu)']]
    
    print(df_ranking.to_string(index=False, float_format=lambda x: f'{x:.8f}'))
    
    # Identify most influential load
    most_influential = df_ranking.iloc[0]
    print("\n" + "="*100)
    print(f"MOST INFLUENTIAL LOAD: Bus {int(most_influential['Load Bus'])}")
    print(f"  Average Variance: {most_influential['Average Variance (pu²)']:.8f} pu²")
    print(f"  Maximum Variance: {most_influential['Maximum Variance (pu²)']:.8f} pu²")
    print("="*100)
    
    return df_variance, df_std, df_ranking


def generate_voltage_profile_table(results, load_bus):
    """
    Generates detailed voltage profile table for a specific load bus.
    """
    print("\n" + "-"*100)
    print(f"DETAILED VOLTAGE PROFILES FOR LOAD BUS {load_bus} VARIATIONS")
    print("-"*100)
    
    analysis = results['load_analysis'][load_bus]
    voltage_results = analysis['voltage_results']
    num_buses = results['num_buses']
    
    # Create table with all scenarios
    table_data = []
    for result in voltage_results:
        row = {
            'ΔP (%)': result['P_variation'],
            'ΔQ (%)': result['Q_variation'],
            'P_load (pu)': result['P_load'],
            'Q_load (pu)': result['Q_load']
        }
        for bus in range(num_buses):
            row[f'V{bus+1} (pu)'] = result['voltages'][bus]
        table_data.append(row)
    
    df_profile = pd.DataFrame(table_data)
    df_profile = df_profile.sort_values(['ΔP (%)', 'ΔQ (%)'])
    print(df_profile.to_string(index=False, float_format=lambda x: f'{x:.6f}'))
    
    return df_profile


def plot_sensitivity_results(results):
    """
    Creates visualization plots for sensitivity analysis.
    """
    print("\n" + "-"*100)
    print("GENERATING PLOTS...")
    print("-"*100)
    
    num_buses = results['num_buses']
    load_buses = results['load_buses']
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    
    # ==========================================
    # Plot 1: Voltage Variance Heatmap
    # ==========================================
    ax1 = plt.subplot(2, 2, 1)
    variance_matrix = np.zeros((num_buses, len(load_buses)))
    for j, load_bus in enumerate(load_buses):
        variance_matrix[:, j] = results['load_analysis'][load_bus]['voltage_variance']
    
    im1 = ax1.imshow(variance_matrix, aspect='auto', cmap='YlOrRd')
    ax1.set_xlabel('Load Bus Varied')
    ax1.set_ylabel('Bus Number')
    ax1.set_title('Voltage Variance Heatmap (pu²)')
    ax1.set_xticks(range(len(load_buses)))
    ax1.set_xticklabels(load_buses)
    ax1.set_yticks(range(num_buses))
    ax1.set_yticklabels(range(1, num_buses + 1))
    plt.colorbar(im1, ax=ax1)
    
    # ==========================================
    # Plot 2: Sensitivity Ranking Bar Chart
    # ==========================================
    ax2 = plt.subplot(2, 2, 2)
    avg_variances = [results['load_analysis'][lb]['avg_variance'] for lb in load_buses]
    ax2.bar(range(len(load_buses)), avg_variances, color='steelblue')
    ax2.set_xlabel('Load Bus')
    ax2.set_ylabel('Average Voltage Variance (pu²)')
    ax2.set_title('Load Bus Sensitivity Ranking')
    ax2.set_xticks(range(len(load_buses)))
    ax2.set_xticklabels(load_buses)
    ax2.grid(axis='y', alpha=0.3)
    
    # ==========================================
    # Plot 3: Voltage Profiles for Most Influential Load
    # ==========================================
    ax3 = plt.subplot(2, 2, 3)
    most_influential_bus = load_buses[np.argmax(avg_variances)]
    analysis = results['load_analysis'][most_influential_bus]
    
    for result in analysis['voltage_results']:
        label = f"ΔP={result['P_variation']:+.0f}%, ΔQ={result['Q_variation']:+.0f}%"
        ax3.plot(range(1, num_buses + 1), result['voltages'], marker='o', label=label)
    
    ax3.set_xlabel('Bus Number')
    ax3.set_ylabel('Voltage Magnitude (pu)')
    ax3.set_title(f'Voltage Profiles - Load Bus {most_influential_bus} Varied')
    ax3.legend(fontsize=6, ncol=2)
    ax3.grid(True, alpha=0.3)
    ax3.set_xticks(range(1, num_buses + 1))
    
    # ==========================================
    # Plot 4: Standard Deviation Comparison
    # ==========================================
    ax4 = plt.subplot(2, 2, 4)
    for load_bus in load_buses:
        std = results['load_analysis'][load_bus]['voltage_std']
        ax4.plot(range(1, num_buses + 1), std, marker='s', label=f'Load Bus {load_bus}')
    
    ax4.set_xlabel('Bus Number')
    ax4.set_ylabel('Voltage Std Dev (pu)')
    ax4.set_title('Voltage Standard Deviation at Each Bus')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xticks(range(1, num_buses + 1))
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig('sensitivity_analysis_plots.png', dpi=300, bbox_inches='tight')
    print("✓ Plots saved to 'sensitivity_analysis_plots.png'")
    
    plt.show()
    
    return fig


def save_sensitivity_results(results):
    """
    Saves sensitivity analysis results to CSV files.
    """
    import os
    
    if not os.path.exists('../outputs/tables/sensitivity_results'):
        os.makedirs('../outputs/tables/sensitivity_results')
    
    num_buses = results['num_buses']
    load_buses = results['load_buses']
    
    # Save variance data
    variance_data = []
    for bus in range(num_buses):
        row = {'Bus': bus + 1}
        for load_bus in load_buses:
            variance = results['load_analysis'][load_bus]['voltage_variance'][bus]
            std = results['load_analysis'][load_bus]['voltage_std'][bus]
            row[f'Load{load_bus}_Variance'] = variance
            row[f'Load{load_bus}_StdDev'] = std
        variance_data.append(row)
    
    df_variance = pd.DataFrame(variance_data)
    df_variance.to_csv('../outputs/tables/sensitivity_results/voltage_variance.csv', index=False)
    
    # Save detailed results for each load bus
    for load_bus in load_buses:
        analysis = results['load_analysis'][load_bus]
        detailed_data = []
        for result in analysis['voltage_results']:
            row = {
                'P_variation_%': result['P_variation'],
                'Q_variation_%': result['Q_variation'],
                'P_load_pu': result['P_load'],
                'Q_load_pu': result['Q_load']
            }
            for bus in range(num_buses):
                row[f'V{bus+1}_pu'] = result['voltages'][bus]
            detailed_data.append(row)
        
        df_detailed = pd.DataFrame(detailed_data)
        df_detailed.to_csv(f'../outputs/tables/sensitivity_results/load_bus_{load_bus}_detailed.csv', index=False)
    
    # Save ranking
    ranking_data = []
    for load_bus in load_buses:
        analysis = results['load_analysis'][load_bus]
        ranking_data.append({
            'Load_Bus': load_bus,
            'Avg_Variance': analysis['avg_variance'],
            'Max_Variance': analysis['max_variance'],
            'Avg_StdDev': np.mean(analysis['voltage_std']),
            'Max_StdDev': np.max(analysis['voltage_std'])
        })
    
    df_ranking = pd.DataFrame(ranking_data)
    df_ranking = df_ranking.sort_values('Avg_Variance', ascending=False)
    df_ranking.to_csv('../outputs/tables/sensitivity_results/sensitivity_ranking.csv', index=False)
    
    print("\n" + "="*100)
    print("Sensitivity results saved to CSV files in 'outputs/tables/sensitivity_results/' directory:")
    print("  - voltage_variance.csv")
    print("  - sensitivity_ranking.csv")
    for load_bus in load_buses:
        print(f"  - load_bus_{load_bus}_detailed.csv")
    print("="*100)


def print_discussion_guidelines():
    """
    Prints guidelines for Task 3 discussion section.
    """
    print("\n" + "="*100)
    print(" "*30 + "DISCUSSION GUIDELINES FOR TASK 3")
    print("="*100)
    
    discussion = """
    
FINDINGS TO DISCUSS (2-3 pages):
---------------------------------

1. VOLTAGE SENSITIVITY PATTERNS:
   - Which load bus has the highest influence on system voltages?
   - Why does this particular load have more influence?
   - Consider: electrical distance from generators, network topology, load magnitude

2. BUS-SPECIFIC OBSERVATIONS:
   - Which buses show highest voltage variations?
   - Are buses near the varied load more affected?
   - How do PV buses respond differently from PQ buses?

3. P vs Q SENSITIVITY:
   - Compare sensitivity to P variations vs Q variations
   - Which has greater impact on voltage magnitudes?
   - Explain based on power flow theory (P-θ and Q-V relationships)

4. SYSTEM IMPLICATIONS:
   - What do these results mean for system operation?
   - Which loads should be monitored more carefully?
   - Implications for voltage stability and control

5. VARIANCE AND STANDARD DEVIATION:
   - Interpret the variance values
   - What does low/high variance indicate?
   - Use statistics to quantify sensitivity

6. NETWORK TOPOLOGY EFFECTS:
   - How does network structure affect sensitivity?
   - Role of line impedances and transformer connections
   - Discuss weakest points in the system

SUGGESTED ANALYSIS STRUCTURE:
------------------------------
1. Introduction (0.5 pages)
   - Objective of sensitivity analysis
   - Methodology overview

2. Results Presentation (1 page)
   - Tables and plots
   - Key numerical findings
   - Sensitivity ranking

3. Discussion (1-1.5 pages)
   - Address points above
   - Connect findings to power system theory
   - Engineering implications

4. Conclusions (0.5 pages)
   - Summary of key findings
   - Recommendations for system operation

    """
    print(discussion)


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    # Perform sensitivity analysis
    results = perform_sensitivity_analysis()
    
    # Generate tables
    df_var, df_std, df_rank = generate_sensitivity_tables(results)
    
    # Generate detailed profile for most influential load
    most_influential = int(df_rank.iloc[0]['Load Bus'])
    df_profile = generate_voltage_profile_table(results, most_influential)
    
    # Create plots
    try:
        fig = plot_sensitivity_results(results)
    except Exception as e:
        print(f"Warning: Could not generate plots: {str(e)}")
    
    # Save results
    save_sensitivity_results(results)
    
    # Print discussion guidelines
    print_discussion_guidelines()
    
    print("\n" + "="*100)
    print(" "*25 + "TASK 3 SENSITIVITY ANALYSIS COMPLETE")
    print("="*100)
    print("\nNext Steps:")
    print("1. Review the generated plots and tables")
    print("2. Write 2-3 page discussion addressing the guidelines above")
    print("3. Include plots and tables in your report")
    print("4. Connect findings to power system theory")
    print("="*100 + "\n")
