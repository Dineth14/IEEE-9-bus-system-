# Newton-Raphson Load Flow Algorithm - Flowchart Reference
## Line Number Mapping for Flowchart Creation

---

## Assignment Requirement
Create a flowchart of your load flow program with each box indicating the respective code line number(s) for reference.

---

## FLOWCHART STRUCTURE

### BOX 1: START
**Line Numbers:** 610-632  
**Description:** Program initialization  
**Code Reference:**
```python
# Lines 610-625: Print header and student info
# Lines 626-632: Load IEEE 9-bus system data
```
**Actions:**
- Display program title
- Load system data (buses, branches, loads, generators)
- Initialize variables

---

### BOX 2: INPUT DATA
**Line Numbers:** 25-100  
**Description:** System data definition  
**Code Reference:**
```python
# Lines 25-80: get_ieee_9_bus_data() function
# Returns: num_buses, bus_types, P_specified, Q_specified, V_init, branch_data
```
**Data Includes:**
- Number of buses (9)
- Bus types (Slack, PV, PQ)
- Generator and load specifications
- Branch parameters (R, X, B)
- Initial voltage estimates (flat start)

---

### BOX 3: CONSTRUCT Y-BUS MATRIX
**Line Numbers:** 103-145  
**Description:** Build admittance matrix from branch data  
**Code Reference:**
```python
# Lines 103-145: build_y_bus() function
# Line 635: Y_bus = build_y_bus(num_buses, branch_data)
```
**Algorithm:**
1. Initialize Y_bus as zeros (num_buses × num_buses)
2. For each branch:
   - Calculate series admittance: y = 1/(R + jX)
   - Calculate shunt admittance: y_shunt = jB/2
   - Update Y_bus[i,i] += y + y_shunt
   - Update Y_bus[j,j] += y + y_shunt
   - Update Y_bus[i,j] -= y
   - Update Y_bus[j,i] -= y

---

### BOX 4: INITIALIZE VOLTAGES
**Line Numbers:** 215  
**Description:** Set initial voltage phasors (flat start)  
**Code Reference:**
```python
# Line 215: V = np.array(V_init, copy=True)
```
**Initial Values:**
- Slack bus: 1.04∠0° pu
- PV buses: 1.025∠0° pu
- PQ buses: 1.0∠0° pu

---

### BOX 5: IDENTIFY BUS TYPES
**Line Numbers:** 218-225  
**Description:** Classify buses for equation formulation  
**Code Reference:**
```python
# Lines 218-225
slack_bus = np.where(bus_types == 0)[0][0]
pq_buses = np.where(bus_types == 1)[0]
pv_buses = np.where(bus_types == 2)[0]
non_slack_buses = np.sort(np.concatenate((pq_buses, pv_buses)))
```
**Classification:**
- Slack (Type 0): Bus 1
- PV (Type 2): Buses 2, 3
- PQ (Type 1): Buses 4-9

---

### BOX 6: START ITERATION LOOP
**Line Numbers:** 242-245  
**Description:** Begin iterative solution (iteration = 1, 2, 3, ...)  
**Code Reference:**
```python
# Line 242: for iteration in range(max_iter):
```
**Loop Control:**
- Maximum iterations: 100
- Current iteration counter

---

### BOX 7: CALCULATE POWER INJECTIONS
**Line Numbers:** 248-253  
**Description:** Compute P and Q at all buses  
**Code Reference:**
```python
# Lines 248-253
S_calc = V * np.conj(Y_bus @ V)
P_calc = np.real(S_calc)
Q_calc = np.imag(S_calc)
```
**Formula:**
- S_i = V_i * conj(∑ Y_ij * V_j)
- P_calc = Real(S)
- Q_calc = Imag(S)

---

### BOX 8: CALCULATE MISMATCHES
**Line Numbers:** 254-262  
**Description:** Compute power mismatches (ΔP, ΔQ)  
**Code Reference:**
```python
# Lines 254-262
dP = P_specified[non_slack_buses] - P_calc[non_slack_buses]
dQ = Q_specified[pq_buses] - Q_calc[pq_buses]
mismatch = np.concatenate((dP, dQ))
max_mismatch = np.max(np.abs(mismatch))
```
**Formulas:**
- ΔP = P_specified - P_calculated (for PV and PQ buses)
- ΔQ = Q_specified - Q_calculated (for PQ buses only)

---

### BOX 9: CHECK CONVERGENCE
**Line Numbers:** 286-292  
**Description:** Test if max|mismatch| < tolerance  
**Code Reference:**
```python
# Lines 286-292
if max_mismatch < tol:
    print("CONVERGED in {iteration + 1} iterations!")
    return V, P_calc, Q_calc, iteration_data
```
**Convergence Criterion:**
- If max|ΔP, ΔQ| < 1e-4 pu → CONVERGED (GO TO BOX 15)
- Else → CONTINUE TO BOX 10

---

### BOX 10: BUILD JACOBIAN MATRIX
**Line Numbers:** 296-390  
**Description:** Construct 4 Jacobian submatrices  
**Code Reference:**
```python
# Lines 303-309: Initialize J1, J2, J3, J4
# Lines 314-340: Fill J1 (∂P/∂δ)
# Lines 342-367: Fill J3 (∂Q/∂δ)
# Lines 350-368: Fill J2 (∂P/∂|V|)
# Lines 370-388: Fill J4 (∂Q/∂|V|)
# Line 391: J = np.block([[J1, J2], [J3, J4]])
```
**Jacobian Structure:**
```
J = [J1  J2]   = [∂P/∂δ    ∂P/∂|V| ]
    [J3  J4]     [∂Q/∂δ    ∂Q/∂|V| ]
```
**Dimensions:**
- J1: (n_PV + n_PQ) × (n_PV + n_PQ)
- J2: (n_PV + n_PQ) × n_PQ
- J3: n_PQ × (n_PV + n_PQ)
- J4: n_PQ × n_PQ

---

### BOX 11: SOLVE LINEAR SYSTEM
**Line Numbers:** 394  
**Description:** Solve J * Δx = Δmismatch for corrections  
**Code Reference:**
```python
# Line 394: dx = np.linalg.solve(J, mismatch)
```
**Linear System:**
- J * [Δδ, Δ|V|]^T = [ΔP, ΔQ]^T
- Solve for voltage corrections

---

### BOX 12: EXTRACT CORRECTIONS
**Line Numbers:** 397-399  
**Description:** Separate angle and magnitude corrections  
**Code Reference:**
```python
# Lines 397-399
d_angle = dx[:n_non_slack]  # Angle corrections
d_vmag = dx[n_non_slack:]   # Magnitude corrections
```

---

### BOX 13: UPDATE VOLTAGES
**Line Numbers:** 402-413  
**Description:** Apply corrections to voltage phasors  
**Code Reference:**
```python
# Lines 402-413
current_angles = np.angle(V)
current_angles[non_slack_buses] += d_angle

current_mags = np.abs(V)
current_mags[pq_buses] += d_vmag

V = current_mags * np.exp(1j * current_angles)
```
**Update Equations:**
- δ_new = δ_old + Δδ (for non-slack buses)
- |V|_new = |V|_old + Δ|V| (for PQ buses only)
- V = |V| * e^(jδ)

---

### BOX 14: INCREMENT ITERATION COUNTER
**Line Numbers:** 242 (loop continues)  
**Description:** iteration = iteration + 1  
**Action:** Return to BOX 6 for next iteration

---

### BOX 15: CONVERGENCE ACHIEVED
**Line Numbers:** 286-292  
**Description:** Solution converged  
**Output:** Final voltage phasors V, P_calc, Q_calc

---

### BOX 16: CALCULATE LINE FLOWS
**Line Numbers:** 420-520  
**Description:** Compute power flows in all branches  
**Code Reference:**
```python
# Lines 420-520: calculate_line_flows() function
# Line 667: line_flows, total_loss_P, total_loss_Q = calculate_line_flows(V_final, branch_data)
```
**Formulas:**
For each branch i-j:
- I_ij = (V_i - V_j) * y_series + V_i * y_shunt
- S_ij = V_i * conj(I_ij)
- S_loss = S_ij + S_ji

---

### BOX 17: PRINT RESULTS
**Line Numbers:** 520-600  
**Description:** Display formatted results  
**Code Reference:**
```python
# Lines 520-600: print_results() function
# Line 674: print_results(...)
```
**Output Includes:**
- Bus voltages (magnitude and angle)
- Real and reactive power at each bus
- Line power flows
- Total system losses
- Second iteration details (Task 1 requirement)

---

### BOX 18: END
**Line Numbers:** 678-695  
**Description:** Program termination  
**Code Reference:**
```python
# Lines 678-695: Print final statistics
# - Number of iterations
# - Computation time
# - Final mismatch
```

---

## FLOWCHART VISUAL LAYOUT

```
┌─────────────┐
│   START     │ (Lines 610-625)
└──────┬──────┘
       │
       v
┌─────────────┐
│ INPUT DATA  │ (Lines 25-100)
└──────┬──────┘
       │
       v
┌─────────────────┐
│ BUILD Y-BUS     │ (Lines 103-145)
└─────┬───────────┘
      │
      v
┌──────────────────┐
│ INITIALIZE V     │ (Lines 215)
└─────┬────────────┘
      │
      v
┌──────────────────┐
│ IDENTIFY BUSES   │ (Lines 218-225)
└─────┬────────────┘
      │
      v
┌──────────────────┐ <────────────┐
│ START ITERATION  │ (Line 242)   │
└─────┬────────────┘              │
      │                           │
      v                           │
┌──────────────────┐              │
│ CALC P, Q        │ (Lines 248-253)
└─────┬────────────┘              │
      │                           │
      v                           │
┌──────────────────┐              │
│ CALC MISMATCHES  │ (Lines 254-262)
└─────┬────────────┘              │
      │                           │
      v                           │
   ┌─────┐                        │
   │ ΔP  │                        │
   │ ΔQ  │                        │
   └──┬──┘                        │
      │                           │
      v                           │
   ╔═══════════╗                  │
   ║ CONVERGED?║ (Lines 286-292)  │
   ╚═══╤═══╤═══╝                  │
   NO  │   │ YES                  │
   ────┘   └────> GO TO BOX 16    │
       │                          │
       v                          │
┌──────────────────┐              │
│ BUILD JACOBIAN   │ (Lines 296-391)
└─────┬────────────┘              │
      │                           │
      v                           │
┌──────────────────┐              │
│ SOLVE J*Δx = Δf  │ (Line 394)   │
└─────┬────────────┘              │
      │                           │
      v                           │
┌──────────────────┐              │
│ EXTRACT Δδ, Δ|V|│ (Lines 397-399)
└─────┬────────────┘              │
      │                           │
      v                           │
┌──────────────────┐              │
│ UPDATE VOLTAGES  │ (Lines 402-413)
└─────┬────────────┘              │
      │                           │
      └───────────────────────────┘
      
(After Convergence)
      │
      v
┌──────────────────┐
│ CALC LINE FLOWS  │ (Lines 420-520)
└─────┬────────────┘
      │
      v
┌──────────────────┐
│ PRINT RESULTS    │ (Lines 520-600)
└─────┬────────────┘
      │
      v
┌──────────────────┐
│   END            │ (Lines 678-695)
└──────────────────┘
```

---

## DECISION BOXES

### Decision 1: Convergence Check (BOX 9)
**Line:** 286  
**Condition:** `if max_mismatch < tol:`  
**True:** → BOX 15 (Convergence achieved)  
**False:** → BOX 10 (Continue iteration)

### Decision 2: Max Iterations Check
**Line:** 415  
**Condition:** Implicit in loop (Line 242: `for iteration in range(max_iter)`)  
**If not converged after max_iter:** → Print warning and return

---

## KEY EQUATIONS REFERENCED IN FLOWCHART

### Box 7 - Power Injection Equations:
```
P_i = |V_i| * Σ |V_k| * |Y_ik| * cos(θ_ik - δ_i + δ_k)
Q_i = |V_i| * Σ |V_k| * |Y_ik| * sin(θ_ik - δ_i + δ_k)
```

### Box 10 - Jacobian Elements:
```
J1 (∂P/∂δ):
  - Diagonal: -Q_i - |V_i|² * Im(Y_ii)
  - Off-diagonal: |V_i||V_k|(G_ik*sin(δ_ik) - B_ik*cos(δ_ik))

J2 (∂P/∂|V|):
  - Diagonal: P_i/|V_i| + |V_i|*Re(Y_ii)
  - Off-diagonal: |V_i|(G_ik*cos(δ_ik) + B_ik*sin(δ_ik))

J3 (∂Q/∂δ):
  - Diagonal: P_i - |V_i|² * Re(Y_ii)
  - Off-diagonal: -|V_i||V_k|(G_ik*cos(δ_ik) + B_ik*sin(δ_ik))

J4 (∂Q/∂|V|):
  - Diagonal: Q_i/|V_i| - |V_i|*Im(Y_ii)
  - Off-diagonal: |V_i|(G_ik*sin(δ_ik) - B_ik*cos(δ_ik))
```

---

## NOTES FOR FLOWCHART CREATION

1. **Use Standard Flowchart Symbols:**
   - Oval: Start/End
   - Rectangle: Process/Calculation
   - Diamond: Decision
   - Parallelogram: Input/Output

2. **Color Coding Suggestion:**
   - Green: Data input/initialization (Boxes 1-5)
   - Blue: Iteration loop (Boxes 6-14)
   - Orange: Jacobian construction (Box 10)
   - Red: Decision points (Box 9)
   - Purple: Post-processing (Boxes 15-17)

3. **Annotations:**
   - Add line numbers prominently in each box
   - Include key variable names
   - Show data flow with arrows

4. **Tools for Creating Flowchart:**
   - Microsoft Visio
   - Draw.io (free, online)
   - Lucidchart
   - PowerPoint (with shapes)
   - LaTeX (with tikz package)

---

## SAMPLE OUTPUT FOR 2ND ITERATION (Task 1 Requirement)

The code captures data from the 2nd iteration (Lines 276-285) and displays it (Lines 593-607).

**What to show:**
- Iteration number: 2
- Voltage magnitudes and angles at all 9 buses
- Power mismatches (ΔP, ΔQ)
- Maximum mismatch value

This data is stored in `iteration_data[1]` (0-indexed, so 2nd iteration)

---

**END OF FLOWCHART REFERENCE DOCUMENT**
