"""
MASTER SCRIPT - RUN ALL ASSIGNMENT TASKS
=========================================
This script runs all three tasks sequentially and generates all outputs
needed for the EE-354 Power Engineering Load Flow Analysis assignment.

Tasks:
1. Newton-Raphson Load Flow (with 2nd iteration output)
2. Comparison of all three methods
3. Voltage Sensitivity Analysis

Author: [E/21/291]
Date: January 2026
"""

import sys
import time

def print_banner():
    """Prints the assignment banner."""
    print("\n" + "="*100)
    print("=" * 100)
    print("=" + " "*98 + "=")
    print("=" + " "*20 + "EE-354 POWER ENGINEERING - LOAD FLOW ANALYSIS" + " "*33 + "=")
    print("=" + " "*98 + "=")
    print("=" + " "*30 + "IEEE 9-BUS TEST SYSTEM" + " "*47 + "=")
    print("=" + " "*98 + "=")
    print("=" + " "*25 + "COMPREHENSIVE ASSIGNMENT SOLUTION" + " "*40 + "=")
    print("=" + " "*98 + "=")
    print("=" * 100)
    print("="*100)
    print("\nDeadline: February 6, 2026")
    print("Student ID: [E/21/291]")
    print("\n" + "="*100 + "\n")


def run_task1():
    """Runs Task 1: Newton-Raphson Load Flow"""
    print("\n" + "*"*100)
    print("*" + " "*40 + "TASK 1: NEWTON-RAPHSON" + " "*37 + "*")
    print("*"*100 + "\n")
    
    print("Executing: Newton_Raphson_Enhanced.py")
    print("Expected outputs:")
    print("  - Y-bus matrix")
    print("  - Iteration details")
    print("  - 2nd iteration output (REQUIRED)")
    print("  - Final voltages and angles")
    print("  - Line flows and losses")
    print("  - Convergence statistics")
    print("\n" + "-"*100 + "\n")
    
    try:
        from Newton_Raphson_Enhanced import (
            get_ieee_9_bus_data, build_y_bus, newton_raphson,
            calculate_line_flows, print_results
        )
        
        # Load data
        num_buses, bus_types, P_spec, Q_spec, V_init, branch_data = get_ieee_9_bus_data()
        
        # Build Y-bus
        Y_bus = build_y_bus(num_buses, branch_data)
        
        # Run Newton-Raphson
        start_time = time.time()
        V_final, P_final, Q_final, iter_data = newton_raphson(
            Y_bus, P_spec, Q_spec, V_init, bus_types,
            max_iter=100, tol=1e-4, verbose=True
        )
        comp_time = time.time() - start_time
        
        # Calculate line flows
        line_flows, loss_P, loss_Q = calculate_line_flows(V_final, branch_data)
        
        # Print results
        print_results(V_final, P_final, Q_final, line_flows, loss_P, loss_Q,
                     iter_data, num_buses)
        
        print("\n" + "="*100)
        print("✓ TASK 1 COMPLETED SUCCESSFULLY")
        print(f"  Converged in {len(iter_data)} iterations")
        print(f"  Computation time: {comp_time:.6f} seconds")
        print(f"  Total losses: P = {loss_P:.6f} pu, Q = {loss_Q:.6f} pu")
        print("="*100)
        
        return True
        
    except Exception as e:
        print(f"\n✗ TASK 1 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_task2():
    """Runs Task 2: Comparison Framework"""
    print("\n" + "*"*100)
    print("*" + " "*30 + "TASK 2: METHOD COMPARISON" + " "*44 + "*")
    print("*"*100 + "\n")
    
    print("Executing: Task2_Comparison_Framework.py")
    print("Expected outputs:")
    print("  - Comparison tables (voltages, angles, losses)")
    print("  - Convergence characteristics")
    print("  - Voltage difference analysis")
    print("  - CSV files in comparison_results/")
    print("  - Discussion points")
    print("\n" + "-"*100 + "\n")
    
    try:
        from Task2_Comparison_Framework import (
            run_all_methods, generate_comparison_tables,
            save_results_to_csv, print_discussion_points
        )
        
        # Run all methods
        results = run_all_methods()
        
        # Generate tables
        df_v, df_a, df_c, df_l, df_d = generate_comparison_tables(results)
        
        # Save to CSV
        save_results_to_csv(results)
        
        # Print discussion points
        print_discussion_points()
        
        print("\n" + "="*100)
        print("✓ TASK 2 COMPLETED SUCCESSFULLY")
        print("  All three methods executed and compared")
        print("  Comparative tables generated")
        print("  Results saved to CSV files")
        print("="*100)
        
        return True
        
    except Exception as e:
        print(f"\n✗ TASK 2 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_task3():
    """Runs Task 3: Voltage Sensitivity Analysis"""
    print("\n" + "*"*100)
    print("*" + " "*25 + "TASK 3: VOLTAGE SENSITIVITY ANALYSIS" + " "*38 + "*")
    print("*"*100 + "\n")
    
    print("Executing: Task3_Sensitivity_Analysis.py")
    print("Expected outputs:")
    print("  - Voltage variance tables")
    print("  - Standard deviation analysis")
    print("  - Sensitivity ranking")
    print("  - Detailed voltage profiles")
    print("  - CSV files in sensitivity_results/")
    print("  - Discussion guidelines")
    print("\n" + "-"*100 + "\n")
    
    try:
        from Task3_Sensitivity_Analysis import (
            perform_sensitivity_analysis, generate_sensitivity_tables,
            generate_voltage_profile_table, save_sensitivity_results,
            print_discussion_guidelines
        )
        
        # Perform sensitivity analysis
        results = perform_sensitivity_analysis()
        
        # Generate tables
        df_var, df_std, df_rank = generate_sensitivity_tables(results)
        
        # Generate detailed profile for most influential load
        most_influential = int(df_rank.iloc[0]['Load Bus'])
        df_profile = generate_voltage_profile_table(results, most_influential)
        
        # Save results
        save_sensitivity_results(results)
        
        # Print discussion guidelines
        print_discussion_guidelines()
        
        print("\n" + "="*100)
        print("✓ TASK 3 COMPLETED SUCCESSFULLY")
        print(f"  Sensitivity analysis completed for {len(results['load_buses'])} load buses")
        print(f"  Most influential load: Bus {most_influential}")
        print("  Results saved to CSV files")
        print("="*100)
        
        return True
        
    except Exception as e:
        print(f"\n✗ TASK 3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def generate_plots():
    """Generates all plots for the report"""
    print("\n" + "*"*100)
    print("*" + " "*30 + "GENERATING REPORT PLOTS" + " "*47 + "*")
    print("*"*100 + "\n")
    
    print("Executing: Visualization_Tools.py")
    print("Expected outputs:")
    print("  - Voltage comparison plots")
    print("  - Convergence comparison plots")
    print("  - Voltage difference heatmap")
    print("  - Power loss comparison")
    print("  - Sensitivity analysis plots")
    print("\n" + "-"*100 + "\n")
    
    try:
        from Visualization_Tools import create_all_plots_for_report
        
        create_all_plots_for_report()
        
        print("\n" + "="*100)
        print("✓ PLOT GENERATION COMPLETED SUCCESSFULLY")
        print("  All report-quality plots generated")
        print("  Use these plots in your assignment report")
        print("="*100)
        
        return True
        
    except Exception as e:
        print(f"\n✗ PLOT GENERATION FAILED: {str(e)}")
        print("Note: Plots are optional. You can generate them separately.")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results):
    """Prints final summary of all tasks"""
    print("\n" + "="*100)
    print("="*100)
    print("=" + " "*98 + "=")
    print("=" + " "*35 + "EXECUTION SUMMARY" + " "*47 + "=")
    print("=" + " "*98 + "=")
    print("="*100)
    print("="*100 + "\n")
    
    task_names = ["Task 1: Newton-Raphson", "Task 2: Method Comparison",
                  "Task 3: Sensitivity Analysis", "Plot Generation"]
    
    for i, (task, success) in enumerate(zip(task_names, results)):
        status = "✓ PASSED" if success else "✗ FAILED"
        color = "GREEN" if success else "RED"
        print(f"{task:<35} {status}")
    
    print("\n" + "="*100)
    
    if all(results):
        
        print("\nGenerated outputs:")
        print("  📁 comparison_results/ - Task 2 CSV files")
        print("  📁 sensitivity_results/ - Task 3 CSV files")
        print("  📊 Multiple PNG plot files")
        print("  📄 Flowchart_Reference.md - For flowchart creation")
        print("\nNext steps:")
      
    else:
        print("⚠️  SOME TASKS FAILED")
        print("\nPlease check error messages above and:")
        print("  1. Verify all required packages are installed")
        print("  2. Check that all .py files are in the same directory")
        print("  3. Run failed tasks individually for detailed debugging")
    
    print("\n" + "="*100)
    print("="*100 + "\n")


def main():
    """Main execution function"""
    print_banner()
    
    print("This script will run all three assignment tasks sequentially.")
    print("Estimated time: 2-5 minutes depending on your system.")
    print("\nPress Ctrl+C to cancel, or")
    input("Press Enter to start execution...")
    
    results = []
    
    # Task 1
    results.append(run_task1())
    time.sleep(1)
    
    # Task 2
    results.append(run_task2())
    time.sleep(1)
    
    # Task 3
    results.append(run_task3())
    time.sleep(1)
    
    # Generate plots
    results.append(generate_plots())
    
    # Print summary
    print_summary(results)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution cancelled by user.")
        print("You can run individual task files separately:")
        print("  - python Newton_Raphson_Enhanced.py")
        print("  - python Task2_Comparison_Framework.py")
        print("  - python Task3_Sensitivity_Analysis.py")
        print("  - python Visualization_Tools.py")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
