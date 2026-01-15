# Project Organization Guide

## 📂 Directory Structure


### `/src/` - Source Code
All Python implementation files are organized here:

- **`/src/methods/`** - Load flow algorithm implementations
  - `newton_raphson.py` - Full Newton-Raphson method (Task 1)
  - `__init__.py` - Package initialization

- **`/src/tasks/`** - Assignment task implementations
  - `task2_comparison.py` - Comparative analysis of all methods
  - `task3_sensitivity.py` - Voltage sensitivity analysis
  - `__init__.py` - Package initialization

- **`/src/visualization.py`** - Plotting and visualization functions
- **`/src/run_all.py`** - Master script to execute all tasks sequentially

### `/docs/` - Documentation
Comprehensive documentation and guides:

- `ASSIGNMENT_GUIDE.md` - Step-by-step completion guide
- `Flowchart_Reference.md` - Algorithm flowchart with line numbers
- `PSSE_Validation.md` - Validation against PSSE software
- `PSSE_Report_Tables.md` - Copy-paste ready tables for reports
- `QUICK_REFERENCE.md` - Quick reference cheat sheet

### `/data/` - Input Data
System configuration and input files:

- `Ieee_9_bus.raw` - IEEE 9-Bus system data

### `/outputs/` - Generated Outputs
All generated files are saved here:

- **`/outputs/figures/`** - High-quality plots for reports
  - `report_voltage_comparison.png`
  - `report_convergence_comparison.png`
  - `report_voltage_difference_heatmap.png`
  - `report_power_loss_comparison.png`
  - `report_sensitivity_comprehensive.png`

- **`/outputs/tables/`** - CSV data files
  - `/comparison_results/` - Task 2 outputs
    - `bus_voltages.csv`
    - `convergence_comparison.csv`
  - `/sensitivity_results/` - Task 3 outputs
    - `voltage_variance.csv`
    - `sensitivity_ranking.csv`
    - `load_bus_X_detailed.csv` (one per load bus)

### `/legacy/` - Original Implementations
Reference implementations from initial development:

- `Newton_raphson_method.py` - Original NR implementation
- `Gauss_Seidel_Load_Flow.py` - Original GS implementation
- `Fast_Decoupled_Load_Flow.py` - Original FD implementation

### Root Files
- `main.py` - Primary entry point (run with `--all` flag)
- `README.md` - Project overview and instructions
- `.gitignore` - Git ignore rules
- `.git/` - Git repository data

---

## 🚀 Running the Code

### Method 1: Using Main Entry Point (Recommended)
```bash
python main.py --all
```

### Method 2: Using Master Script
```bash
python src/run_all.py
```

### Method 3: Individual Tasks
```bash
# Task 1 - Newton-Raphson
python src/methods/newton_raphson.py

# Task 2 - Comparison
python src/tasks/task2_comparison.py

# Task 3 - Sensitivity Analysis
python src/tasks/task3_sensitivity.py

# Generate All Plots
python src/visualization.py
```

---

## 📝 Import Structure

The codebase uses relative imports within the `src/` package:

```python
# In src/tasks/task2_comparison.py
from methods.newton_raphson import newton_raphson

# In src/run_all.py
from tasks.task2_comparison import run_all_methods
from tasks.task3_sensitivity import perform_sensitivity_analysis
```

All scripts are designed to be run from the **repository root directory**.

---




## 🔄 Updating Your Student ID

Search for `[REPLACE WITH YOUR ID]` in all Python files and replace with your actual student ID:

```bash
# On Windows PowerShell:
Get-ChildItem -Path src -Filter *.py -Recurse | ForEach-Object {
    (Get-Content $_.FullName) -replace '\[REPLACE WITH YOUR ID\]', 'E/21/XXX' | 
    Set-Content $_.FullName
}
```

---


*Last Updated: January 1, 2026*
