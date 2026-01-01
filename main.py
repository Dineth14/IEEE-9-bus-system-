#!/usr/bin/env python3
"""
IEEE 9-Bus System Load Flow Analysis
Main Entry Point

This script provides a convenient way to run all analysis tasks.
For detailed implementation, see src/run_all.py

Student ID: [REPLACE WITH YOUR ID]
Course: EE-354 Power Engineering
Assignment: Load Flow Analysis on IEEE 9-Bus System
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    print("=" * 100)
    print("IEEE 9-BUS SYSTEM LOAD FLOW ANALYSIS".center(100))
    print("=" * 100)
    print()
    print("This is the main entry point for the IEEE 9-Bus Load Flow Analysis.")
    print()
    print("Available options:")
    print("  1. Run all tasks               : python main.py --all")
    print("  2. Run Task 1 (Newton-Raphson) : python src/methods/newton_raphson.py")
    print("  3. Run Task 2 (Comparison)     : python src/tasks/task2_comparison.py")
    print("  4. Run Task 3 (Sensitivity)    : python src/tasks/task3_sensitivity.py")
    print("  5. Run complete suite          : python src/run_all.py")
    print()
    print("=" * 100)
    
    # Check if --all flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        print("\nRunning complete analysis suite...\n")
        from run_all import main as run_all_main
        run_all_main()
    else:
        print("\nFor complete analysis, run: python main.py --all")
        print("=" * 100)
