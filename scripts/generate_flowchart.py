import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart():
    # Create figure with dark background to match user aesthetic preferences potentially, 
    # but standard white is better for printing/reports. User didn't specify dark mode for this, 
    # but usually flowcharts are on white. I will use white background.
    fig, ax = plt.subplots(figsize=(12, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Common box styles
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#e1f5fe', edgecolor='#01579b', linewidth=1.5)
    decision_props = dict(boxstyle='round4,pad=0.5', facecolor='#fff9c4', edgecolor='#fbc02d', linewidth=1.5)
    start_end_props = dict(boxstyle='round4,pad=0.5', facecolor='#ffccbc', edgecolor='#ff5722', linewidth=1.5)
    io_props = dict(boxstyle='round,pad=0.5', facecolor='#e0f2f1', edgecolor='#00695c', linewidth=1.5) # Using round for IO but different color

    def draw_node(x, y, text, lines="", equations="", style=box_props, width=None):
        content = f"{text}"
        if lines:
            content += f"\n(Lines: {lines})"
        if equations:
            content += f"\n{equations}"
        
        # We rely on bbox to size it, so we just place text
        t = ax.text(x, y, content, ha='center', va='center', bbox=style, fontsize=10, family='sans-serif', wrap=True)
        return t

    # --- Draw Nodes ---
    
    # 1. Start (Top, Center)
    draw_node(5, 11.5, "Start", "", "", style=start_end_props)
    
    # 2. Input Data
    draw_node(5, 10.3, "Input System Data", "22-75", r"Returns: $N_{bus}, Types, P_{spec}, Q_{spec}, V_{init}, BranchData$", style=io_props)
    
    # 3. Build Y-Bus
    draw_node(5, 9.1, "Construction of Y-Bus Matrix", "78-98", r"$Y_{ii} = \sum y_{ik} + y_{sh}$" + "\n" + r"$Y_{ij} = -y_{ij}$", style=box_props)
    
    # 4. Initialize NR
    draw_node(5, 7.9, "Initialize Newton-Raphson", "104-122", r"Set $V = V_{init}$" + "\n" + r"Iteration $k=0$", style=box_props)
    
    # 5. Mismatch Calculation (Loop Start Point)
    draw_node(5, 6.7, "Calculate Power Mismatches", "128-133", r"$\Delta P = P_{spec} - P_{calc}(V, \delta)$" + "\n" + r"$\Delta Q = Q_{spec} - Q_{calc}(V, \delta)$", style=box_props)
    
    # 6. Convergence Check
    draw_node(5, 5.2, "Check Convergence", "136-156", r"Is $\max(|\Delta P|, |\Delta Q|) < \epsilon$?", style=decision_props)
    
    # 7. Jacobian (If No) - Placed to the right
    draw_node(8.5, 5.2, "Compute Jacobian Matrix", "167-212", r"$J = \begin{bmatrix} \frac{\partial P}{\partial \delta} & \frac{\partial P}{\partial |V|} \\ \frac{\partial Q}{\partial \delta} & \frac{\partial Q}{\partial |V|} \end{bmatrix}$", style=box_props)
    
    # 8. Update State (If No)
    draw_node(8.5, 3.8, "Solve & Update", "213-224", r"$\begin{bmatrix}\Delta \delta \\ \Delta |V|\end{bmatrix} = J^{-1} \begin{bmatrix}\Delta P \\ \Delta Q\end{bmatrix}$" + "\n" + r"$V^{k+1} = V^k + \Delta V$", style=box_props)
    
    # 9. Calc Flows (If Yes)
    draw_node(5, 3.2, "Calculate Line Flows & Losses", "229-263", r"$I_{ij} = (V_i - V_j)y_{ij} + V_i y_{sh}$" + "\n" + r"$S_{ij} = V_i I_{ij}^*$", style=box_props)
    
    # 10. Output Results
    draw_node(5, 1.8, "Output Results", "266-316", "Print Tables, Save CSV", style=io_props)
    
    # 11. End
    draw_node(5, 0.8, "End", "336", "", style=start_end_props)
    
    # --- Draw Connections (Arrows) ---
    arrow_props = dict(arrowstyle='->', lw=1.5, color='black')
    
    def connect(xy1, xy2):
        ax.annotate('', xy=xy2, xytext=xy1, arrowprops=arrow_props)
        
    # Start -> Input
    connect((5, 11.2), (5, 10.6))
    # Input -> YBus
    connect((5, 10.0), (5, 9.5))
    # YBus -> Init
    connect((5, 8.7), (5, 8.3))
    # Init -> Mismatch
    connect((5, 7.5), (5, 7.1))
    # Mismatch -> Convergence
    connect((5, 6.3), (5, 5.8))
    
    # Convergence -> Line Flows (YES)
    ax.annotate('Yes', xy=(5, 3.7), xytext=(5, 4.6), arrowprops=arrow_props, ha='center', fontsize=10, bbox=dict(fc='white', ec='none'))
    
    # Convergence -> Jacobian (NO)
    ax.annotate('No', xy=(7.4, 5.2), xytext=(6.2, 5.2), arrowprops=arrow_props, va='center', fontsize=10, bbox=dict(fc='white', ec='none'))
    
    # Jacobian -> Update
    connect((8.5, 4.7), (8.5, 4.3))
    
    # Update -> Mismatch (Loop Back)
    # Draw path: Update(8.5, 3.4) -> Down a bit? No, Up is better or around.
    # Let's go from bottom of Update to right, up, and back to Mismatch top?
    # Or just simply: Update(8.5, 3.3) -> line to (8.5, 7.3) -> (5, 7.3) -> Mismatch(5, 7.1)
    # Wait, Mismatch input is at 7.1 (top of box at 6.7 + pad).
    # Let's draw a line.
    
    # Path coordinates
    path_update_mismatch_x = [8.5, 8.5, 5, 5]
    path_update_mismatch_y = [3.3, 7.3, 7.3, 7.1] # 3.3 is below Update box? 
    # Update box center is 3.8. Height approx 1.0. Bottom approx 3.3.
    # Actually let's go from Top of Update to Top of Mismatch? No, Update happens, then we go back to mismatch.
    # So output of Update -> Mismatch.
    # Update center 3.8. Let's exit from Right or Bottom?
    # Let's exit from Right of Update (9.5, 3.8) -> Up to (9.5, 7.3) -> Left to (5, 7.3) -> Down to (5, 7.1)
    
    ax.plot([9.6, 9.6, 5, 5], [3.8, 7.3, 7.3, 7.1], zorder=0, **dict(lw=1.5, color='black'))
    # Arrow head at the end
    ax.annotate('', xy=(5, 7.0), xytext=(5, 7.2), arrowprops=arrow_props)
    
    # Line Flows -> Output
    connect((5, 2.7), (5, 2.1))
    
    # Output -> End
    connect((5, 1.5), (5, 1.0))

    # Title
    plt.title("Flowchart: Full Newton-Raphson Load Flow (E21291_LoadFlow.py)", fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('Report/flowchart.png')
    print("Flowchart saved successfully to 'Report/flowchart.png'")

if __name__ == "__main__":
    draw_flowchart()
