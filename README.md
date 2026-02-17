# IEEE 9-Bus System — Newton-Raphson Load Flow Analysis

**Student:** E/21/291  
**Course:** EE-354 Power Engineering  
**Date:** February 17, 2026

## Project Overview

This repository contains a full implementation of the **Newton-Raphson Load Flow** method applied to the standard IEEE 9-bus test system. It is designed to meet the requirements of the EE-354 assignment, including:

1.  **Newton-Raphson Solver:** A robust, from-scratch Python implementation (`src/E21291_LoadFlow.py`) that converges in 4 iterations.
2.  **Method Comparison:** Validation against PSS/E results (Gauss-Seidel, Fast Decoupled, and Newton-Raphson).
3.  **Sensitivity Analysis:** A study of voltage sensitivity to active (P) and reactive (Q) power variations.
4.  **Documentation:** A comprehensive LaTeX report and algorithm flowchart.

## Repository Structure

```
├── src/
│   └── E21291_LoadFlow.py    # Main NR solver (standalone)
├── scripts/
│   ├── run_task2.py          # Generates PSS/E comparison plots
│   └── run_task3.py          # Runs sensitivity analysis and plotting
├── data/
│   └── Ieee_9_bus.raw        # PSS/E raw data file (reference)
├── Report/
│   ├── E21291_LoadFlow_Report.pdf  # Final Report
│   └── E21291_LoadFlow_Report.tex  # LaTeX Source
├── docs/
│   └── ASSIGNMENT_GUIDE.md   # Detailed assignment tasks
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Setup & Execution

### 1. Prerequisites
Ensure you have Python 3.8+ installed. Install the required libraries:

```bash
pip install -r requirements.txt
```

### 2. Run the Main Solver (Task 1)
To execute the load flow analysis and see the convergence report:

```bash
python src/E21291_LoadFlow.py
```
*Output will be saved to `outputs/tables/`.*

### 3. Verification & Comparison (Task 2)
To generate the validation plots comparing this solver against PSS/E:

```bash
python scripts/run_task2.py
```
*Plots are saved to `Report/`.*

### 4. Sensitivity Analysis (Task 3)
To run the remediation study (voltage sensitivity to P/Q changes):

```bash
python scripts/run_task3.py
```
*Results are saved to `outputs/tables/` and plots to `Report/`.*

## Key Results

-   **Convergence:** The solver achieves a mismatch tolerance of $10^{-4}$ pu in **4 iterations**, matching PSS/E's quadratic convergence profile.
-   **Validation:** Voltage magnitudes match PSS/E results to **4 decimal places**.
-   **Weakest Point:** **Bus 5** is identified as the most critical bus, exhibiting the lowest voltage modulus (0.9956 pu) and highest sensitivity to reactive power changes ($dV/dQ$).

## Documentation

-   **[Final Report](Report/E21291_LoadFlow_Report.pdf):** Full theoretical background, derivations, and discussion.
-   **[Flowchart](Report/flowchart.png):** Detailed algorithm logic.
-   **[Assignment Guide](docs/ASSIGNMENT_GUIDE.md):** Detailed breakdown of the assignment tasks.
