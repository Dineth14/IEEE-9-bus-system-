# IEEE 9-Bus System — Newton-Raphson Load Flow Analysis

**Student:** E/21/291  
**Course:** EE-354 Power Engineering  

## Repository Structure

```
├── E21291_LoadFlow.py          # Main NR solver (standalone, self-contained)
├── data/
│   └── Ieee_9_bus.raw          # PSS/E raw data file for verification
├── scripts/
│   ├── produce_task2_plots.py  # Generate PSS/E comparison plots
│   ├── produce_task3_remediation.py  # Sensitivity analysis runner
│   ├── create_screenshot.py    # Generate execution proof image
│   └── generate_flowchart.py   # Generate algorithm flowchart
├── Report/
│   ├── E21291_LoadFlow_Report.tex  # LaTeX report
│   ├── code_appendix/          # Source files included in report appendix
│   ├── flowchart.png           # Algorithm flowchart
│   ├── execution_proof.png     # Convergence proof screenshot
│   └── *.png                   # Figures referenced by the report
├── docs/
│   ├── PSSE_*.txt              # PSS/E validation results
│   ├── PSSE_Validation.md      # Detailed PSS/E comparison
│   └── ASSIGNMENT_GUIDE.md     # Assignment requirements reference
├── outputs/
│   └── tables/                 # Generated CSV data
├── legacy/                     # Old/superseded implementations
└── README.md
```

## Quick Start

```bash
# Run the Newton-Raphson solver
python E21291_LoadFlow.py

# Generate comparison plots (Task 2)
python scripts/produce_task2_plots.py

# Run sensitivity analysis (Task 3)
python scripts/produce_task3_remediation.py

# Generate flowchart
python scripts/generate_flowchart.py
```

## Results

- **Convergence:** 4 iterations (tolerance = 1×10⁻⁴ pu)
- **Validation:** Voltage magnitudes match PSS/E to 4 decimal places
- **Weakest Bus:** Bus 5 (lowest voltage, highest ∂V/∂Q sensitivity)
