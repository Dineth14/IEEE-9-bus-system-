# Assignment Completion Guide
## EE-354 Power Engineering - Load Flow Analysis
### Deadline: February 6, 2026

---

## 🎯 Quick Start (5 Minutes to Run Everything)

### Option 1: Run Everything at Once (Recommended)
```bash
python RUN_ALL_TASKS.py
```
This will:
- Execute all three tasks sequentially
- Generate all tables and CSV files
- Create all plots
- Display comprehensive results

### Option 2: Run Tasks Individually
```bash
# Task 1: Newton-Raphson (5-10 seconds)
python Newton_Raphson_Enhanced.py

# Task 2: Method Comparison (10-15 seconds)
python Task2_Comparison_Framework.py

# Task 3: Sensitivity Analysis (30-60 seconds)
python Task3_Sensitivity_Analysis.py

# Generate all plots
python Visualization_Tools.py
```

---

## 📋 What You Have Now

### ✅ Code Files (Ready to Submit)
1. **Newton_Raphson_Enhanced.py** - Your main NR implementation
   - Full Newton-Raphson from scratch
   - Y-bus construction
   - Jacobian computation
   - Line-by-line comments
   - 2nd iteration output
   - All Task 1 requirements met

2. **Gauss_Seidel_Load_Flow.py** - GS method
3. **Fast_Decoupled_Load_Flow.py** - FD method
4. **Task2_Comparison_Framework.py** - Comparison analysis
5. **Task3_Sensitivity_Analysis.py** - Sensitivity study
6. **Visualization_Tools.py** - Plotting functions
7. **RUN_ALL_TASKS.py** - Master execution script

### ✅ Documentation Files
1. **Flowchart_Reference.md** - Complete line-by-line mapping for flowchart
2. **README.md** - Comprehensive project documentation
3. **ASSIGNMENT_GUIDE.md** - This file

### ✅ Output Files (Generated When You Run)
1. **comparison_results/** folder with CSV files
2. **sensitivity_results/** folder with CSV files  
3. **Multiple PNG plot files** for your report

---

## 📝 What You Need to Do

### Before Running Code
1. **Install required packages:**
   ```bash
   pip install numpy pandas matplotlib seaborn
   ```

2. **Update Student ID** in all Python files:
   - Search for `[REPLACE WITH YOUR ID]` or `[Your Student ID]`
   - Replace with your actual student ID
   - Files to update: All .py files

3. **Verify file structure:**
   ```
   All .py files should be in the same directory
   ```

### After Running Code

#### For Task 1 Deliverables:

1. **✅ Source Code** - Already done
   - File: `Newton_Raphson_Enhanced.py`
   - Has detailed comments
   - Captures 2nd iteration output

2. **📊 Create Flowchart** (30-60 minutes)
   - Open `Flowchart_Reference.md`
   - Use the line numbers and descriptions provided
   - Create flowchart using:
     - Microsoft Visio, OR
     - Draw.io (free: https://draw.io), OR
     - Lucidchart, OR
     - PowerPoint with shapes
   - Each box should reference line numbers
   - Follow the structure in Flowchart_Reference.md

3. **📄 2nd Iteration Output** - Already captured
   - Automatically printed when you run the code
   - Copy from terminal output
   - Include in your report

#### For Task 2 Deliverables:

1. **✅ Run Comparison** - Automated
   ```bash
   python Task2_Comparison_Framework.py
   ```

2. **📊 Create Comparison Plots**
   - Run `Visualization_Tools.py`
   - Use generated PNG files in report

3. **📝 Write Discussion** (1-2 pages)
   - Use the discussion points printed by the script
   - Compare numerical accuracy
   - Discuss convergence characteristics
   - Explain deviations between methods
   - Compare with PSSE (if available)

#### For Task 3 Deliverables:

1. **✅ Run Sensitivity Analysis** - Automated
   ```bash
   python Task3_Sensitivity_Analysis.py
   ```

2. **📊 Use Generated Plots and Tables**
   - Voltage variance tables
   - Sensitivity ranking
   - Voltage profile graphs

3. **📝 Write Discussion (2-3 pages)** - IMPORTANT!
   Use the guidelines printed by the script:
   
   **Section 1: Introduction (0.5 pages)**
   - Objective of sensitivity analysis
   - Methodology overview
   - Load buses studied (5, 6, 8)
   - Variation levels (-10%, 0%, +10%)

   **Section 2: Results Presentation (1 page)**
   - Present tables from CSV files
   - Show voltage profile plots
   - Display sensitivity ranking
   - Key numerical findings

   **Section 3: Discussion (1-1.5 pages)**
   Answer these questions:
   - Which load has highest influence? Why?
   - Which buses show highest voltage variations?
   - Are nearby buses more affected?
   - P sensitivity vs Q sensitivity - which is greater?
   - What does this mean for system operation?
   - Network topology effects
   - Weakest points in the system

   **Section 4: Conclusions (0.5 pages)**
   - Summary of key findings
   - Most influential load identified
   - Recommendations for system operators
   - Implications for voltage control

---

## 📊 Understanding Your Results

### Task 1: Expected Newton-Raphson Results
- **Iterations:** 3-5 (typically 4)
- **Convergence tolerance:** < 1e-4 pu
- **Computation time:** < 0.02 seconds
- **Total losses:** ~0.046 pu (4.6 MW)

### Task 2: Expected Comparisons
| Method | Iterations | Time |
|--------|-----------|------|
| Newton-Raphson | 3-5 | Fastest per iteration |
| Gauss-Seidel | 50-100+ | Slowest overall |
| Fast Decoupled | 4-7 | Good compromise |

**Voltage differences should be < 0.001 pu between methods**

### Task 3: Expected Sensitivity Results
- Load Bus 5 or 8 typically most influential (highest variance)
- Nearby buses show higher voltage variations
- Q variations affect voltages more than P variations
- Variance values: typically 1e-5 to 1e-4 pu²

---

## 🎨 Creating Your Report

### Report Structure

**Cover Page**
- Assignment title
- Student name and ID
- Course code (EE-354)
- Date
- Institution

**Table of Contents**

**Task 1: Newton-Raphson Implementation (8-10 pages)**
1. Introduction
2. Methodology
   - Power flow equations
   - Newton-Raphson formulation
   - Y-bus construction
   - Jacobian computation
3. Implementation
   - Code structure
   - Key functions
   - Flowchart with line numbers
4. Results
   - 2nd iteration output
   - Final voltages and angles
   - Line flows
   - System losses
   - Convergence statistics
5. Discussion

**Task 2: Method Comparison (5-7 pages)**
1. Introduction
2. Methodology
3. Results
   - Comparative tables
   - Voltage comparison plots
   - Convergence comparison
   - Loss comparison
4. Discussion
   - Numerical accuracy
   - Convergence characteristics
   - Reasons for deviations
   - PSSE comparison (if available)
5. Conclusions

**Task 3: Sensitivity Analysis (4-6 pages)**
1. Introduction (0.5 pages)
2. Results (1 page)
   - Tables and graphs
3. Discussion (2-3 pages)
   - Address all discussion points
4. Conclusions (0.5 pages)

**Overall Conclusions (1 page)**

**References**

**Appendices**
- Complete code listings (optional)
- Additional data tables

### Tips for Report Writing

1. **Use Professional Formatting**
   - Clear section headings
   - Numbered figures and tables
   - Consistent fonts and spacing
   - Page numbers

2. **Include All Plots**
   - Label axes clearly
   - Add legends
   - Reference in text
   - Use captions

3. **Present Tables Properly**
   - Clear column headers
   - Appropriate precision (4-6 decimal places)
   - Units specified
   - Reference in text

4. **Write Technical Discussion**
   - Explain why, not just what
   - Connect to theory
   - Use technical terminology correctly
   - Support claims with data

5. **Proofread**
   - Check calculations
   - Verify plot labels
   - Fix typos
   - Ensure consistency

---

## 🔍 Verification Checklist

### Before Submission

**Code Verification**
- [ ] All code files run without errors
- [ ] Student ID updated in all files
- [ ] Comments are clear and detailed
- [ ] 2nd iteration output is captured
- [ ] All CSV files generated
- [ ] All plots generated

**Task 1 Checklist**
- [ ] Newton-Raphson converges in 3-5 iterations
- [ ] Y-bus constructed programmatically
- [ ] Jacobian computed from formulas
- [ ] Flat start implemented (1.0∠0° for PQ buses)
- [ ] Line flows calculated
- [ ] System losses computed
- [ ] 2nd iteration output shown
- [ ] Flowchart created with line numbers
- [ ] All functions have docstrings

**Task 2 Checklist**
- [ ] All three methods run successfully
- [ ] Voltage differences < 0.001 pu
- [ ] Convergence comparison complete
- [ ] Loss comparison included
- [ ] Discussion addresses all points
- [ ] PSSE comparison done (if available)
- [ ] Comparative plots included

**Task 3 Checklist**
- [ ] All load buses analyzed (5, 6, 8)
- [ ] All 9 scenarios per load (3×3)
- [ ] Variance calculated correctly
- [ ] Standard deviation computed
- [ ] Sensitivity ranking created
- [ ] Most influential load identified
- [ ] 2-3 page discussion written
- [ ] Discussion addresses all guidelines
- [ ] Plots and tables included

**Report Checklist**
- [ ] All sections complete
- [ ] Figures numbered and labeled
- [ ] Tables formatted properly
- [ ] References included
- [ ] Page numbers added
- [ ] Proofread for errors
- [ ] PDF format for submission
- [ ] File size reasonable (<10 MB)

---

## ❓ Troubleshooting

### Common Issues and Solutions

**Issue:** "ModuleNotFoundError: No module named 'numpy'"
```bash
Solution: pip install numpy pandas matplotlib seaborn
```

**Issue:** "ImportError: cannot import name 'get_ieee_9_bus_data'"
```bash
Solution: Ensure all .py files are in the same directory
```

**Issue:** Code runs but no CSV files generated
```bash
Solution: Check that folders comparison_results/ and sensitivity_results/ are created
The scripts should create them automatically, but you can create manually if needed
```

**Issue:** Plots not displaying
```bash
Solution: If running on server, plots will still save as PNG files
You don't need to see them interactively - just use the PNG files
```

**Issue:** Convergence failure
```bash
Solution: Check input data, verify flat start initialization
Should not happen with provided IEEE 9-bus data
```

**Issue:** Results don't match PSSE exactly
```bash
Solution: Small differences (< 0.001 pu) are acceptable
Different convergence criteria and numerical precision
Document the differences and discuss reasons
```

---

## 📚 Key Concepts to Understand

### For Task 1

1. **Y-bus Matrix**
   - Represents network admittances
   - Diagonal: self-admittance
   - Off-diagonal: mutual admittance
   - Complex matrix (conductance + susceptance)

2. **Newton-Raphson Method**
   - Solves nonlinear equations iteratively
   - Uses Jacobian (partial derivatives)
   - Quadratic convergence
   - Most widely used in practice

3. **Power Flow Equations**
   - Real power: P = f(V, θ)
   - Reactive power: Q = f(V, θ)
   - Nonlinear algebraic equations
   - Solved iteratively

4. **Bus Types**
   - Slack: V and θ specified, P and Q calculated
   - PV: P and V specified, Q and θ calculated
   - PQ: P and Q specified, V and θ calculated

### For Task 2

1. **Gauss-Seidel**
   - Sequential updates
   - Linear convergence (slow)
   - Simple implementation
   - Still used for small systems

2. **Fast Decoupled**
   - Exploits P-θ and Q-V decoupling
   - Approximations in Jacobian
   - Faster than GS, slightly slower than full NR
   - Good for large systems

3. **Convergence Comparison**
   - NR: fastest (quadratic)
   - GS: slowest (linear)
   - FD: middle ground

### For Task 3

1. **Voltage Sensitivity**
   - How voltages respond to load changes
   - Important for voltage stability
   - Identifies weak buses
   - Guides reactive power placement

2. **Variance and Standard Deviation**
   - Statistical measures of variability
   - Higher variance = more sensitive
   - Quantifies voltage fluctuations

3. **Load Influence**
   - Depends on location
   - Network topology
   - Electrical distance from generation
   - Load magnitude

---



## 📞 Support

If you encounter issues:

1. **Check this guide** for solutions
2. **Review code comments** - they explain everything
3. **Read error messages** carefully
4. **Check file paths** and directory structure
5. **Verify package installation**



*Last updated: January 2026*
*Version 1.0*
