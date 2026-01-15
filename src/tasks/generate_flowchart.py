import matplotlib.pyplot as plt

def create_detailed_flowchart():
    # Setup figure with A4 aspect ratio (8.27 x 11.69)
    # We use a coordinate system of approx 12x17 to match this ratio (12/17 ~ 0.705)
    fig, ax = plt.figure(figsize=(8.27, 11.69)), plt.gca()
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 17.5) # Reduced from 20 to tighten vertical spacing relative to width
    ax.axis('off')
    
    # Define box styles
    style_start = {'boxstyle': 'round,pad=0.5', 'facecolor': '#ffcccc', 'edgecolor': 'black'}
    style_input = {'boxstyle': 'round4,pad=0.5', 'facecolor': '#ccffcc', 'edgecolor': 'black'}  # Green for data
    style_proc = {'boxstyle': 'square,pad=0.5', 'facecolor': '#cce5ff', 'edgecolor': 'black'}   # Blue for process
    style_dec = {'boxstyle': 'square,pad=0.3', 'facecolor': '#ffcc99', 'edgecolor': 'black'}    # Standard box, annotated as decision
    style_res = {'boxstyle': 'round4,pad=0.5', 'facecolor': '#e5ccff', 'edgecolor': 'black'}    # Purple for results

    # Helper to draw box
    def draw_box(x, y, text, style):
        ax.text(x, y, text, ha='center', va='center', bbox=style, fontsize=9, family='sans-serif')

    # Helper for arrow
    def arrow(x1, y1, x2, y2, text=None):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', lw=1.5))
        if text:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=9)

    # Main Column (x = 6)
    # BOX 1: START
    draw_box(6, 17.0, "1. START\n(Lines 610-632)", style_start)
    arrow(6, 16.6, 6, 16.1)

    # BOX 2: INPUT DATA
    draw_box(6, 15.7, "2. INPUT DATA\n(Lines 25-100)\nGet System Data", style_input)
    arrow(6, 15.3, 6, 14.8)

    # BOX 3: CONSTRUCT Y-BUS
    draw_box(6, 14.4, "3. BUILD Y-BUS\n(Lines 103-145)\nCompute Admittance Matrix", style_input)
    arrow(6, 14.0, 6, 13.5)

    # BOX 4: INITIALIZE VOLTAGES
    draw_box(6, 13.1, "4. INITIALIZE V\n(Line 215)\nFlat Start: 1.0<0 pu", style_input)
    arrow(6, 12.7, 6, 12.2)

    # BOX 5: IDENTIFY BUS TYPES
    draw_box(6, 11.8, "5. IDENTIFY BUSES\n(Lines 218-225)\nSlack, PV, PQ Lists", style_input)
    arrow(6, 11.4, 6, 10.9)

    # BOX 6: START ITERATION (Loop Entry)
    draw_box(6, 10.5, "6. START ITERATION k\n(Line 242)", style_proc)
    arrow(6, 10.1, 6, 9.6)

    # BOX 7: CALCULATE P, Q
    draw_box(6, 9.2, "7. CALC P, Q INJECTIONS\n(Lines 248-253)\nUsing Power Flow Eq", style_proc)
    arrow(6, 8.8, 6, 8.3)

    # BOX 8: CALCULATE MISMATCHES
    draw_box(6, 7.9, "8. CALC MISMATCHES\n(Lines 254-262)\nDelta P, Delta Q", style_proc)
    arrow(6, 7.5, 6, 6.9) # Adjusted endpoint to touch box 9

    # BOX 9: CONVERGENCE CHECK (Decision)
    draw_box(6, 6.5, "9. CONVERGED?\n(Lines 286-292)\nMax Mismatch < Tol?", style_dec)

    # YES PATH (Right -> Down)
    # Start from right edge of Box 9 (approx x=7.3) to x=9
    ax.annotate('YES', xy=(9, 5.3), xytext=(7.3, 6.5), 
                arrowprops=dict(arrowstyle='->', lw=1.5, connectionstyle="angle,angleA=0,angleB=90,rad=0"),
                ha='left', va='bottom', fontsize=9)

    # NO PATH (Left -> Down)
    # Start from left edge of Box 9 (approx x=4.7) to x=3.5
    ax.annotate('NO', xy=(3.5, 5.9), xytext=(4.7, 6.5), 
                arrowprops=dict(arrowstyle='->', lw=1.5, connectionstyle="angle,angleA=180,angleB=90,rad=0"),
                ha='right', va='bottom', fontsize=9)

    # RESUME Main Column for Box 16, 17, 18
    # BOX 16: CALC FLOWS (Post convergence)
    draw_box(9, 4.9, "16. CALC LINE FLOWS\n(Lines 420-520)", style_res)
    arrow(9, 4.5, 9, 4.0)

    # BOX 17: PRINT RESULTS
    draw_box(9, 3.6, "17. PRINT RESULTS\n(Lines 520-600)", style_res)
    arrow(9, 3.2, 9, 2.7)

    # BOX 18: END
    draw_box(9, 2.3, "18. END\n(Lines 678-695)", style_start)

    # BOX 10: BUILD JACOBIAN
    draw_box(3.5, 5.5, "10. BUILD JACOBIAN\n(Lines 296-391)\nJ1, J2, J3, J4", style_proc)
    arrow(3.5, 5.1, 3.5, 4.9)

    # BOX 11: SOLVE LINEAR SYSTEM
    draw_box(3.5, 4.5, "11. SOLVE SYSTEM\n(Line 394)\nJ * dx = Mismatch", style_proc)
    arrow(3.5, 4.1, 3.5, 3.9)

    # BOX 12: EXTRACT CORRECTIONS
    draw_box(3.5, 3.5, "12. EXTRACT CORRECTIONS\n(Lines 397-399)\nGet dAngle, dVmag", style_proc)
    arrow(3.5, 3.1, 3.5, 2.9)

    # BOX 13: UPDATE VOLTAGES
    draw_box(3.5, 2.5, "13. UPDATE VOLTAGES\n(Lines 402-413)\nV_new = V_old + dx", style_proc)
    arrow(3.5, 2.1, 3.5, 1.9)

    # BOX 14: INCREMENT ITERATION
    draw_box(3.5, 1.5, "14. NEXT ITERATION\n(Implicit Loop)", style_proc)
    
    # Loop back line
    # From Box 14 (3.5, 1.5) back to Box 6 (6, 10.5)
    # Path: Down -> Left -> Up -> Right
    ax.plot([3.5, 3.5], [1.1, 0.5], color='black', lw=1.5) # Down
    ax.plot([3.5, 1.0], [0.5, 0.5], color='black', lw=1.5) # Left
    ax.plot([1.0, 1.0], [0.5, 10.5], color='black', lw=1.5) # Up long way
    ax.annotate('', xy=(4.9, 10.5), xytext=(1.0, 10.5), arrowprops=dict(arrowstyle='->', lw=1.5)) # Right into Box 6

    plt.tight_layout()
    plt.savefig('flowchart.png', dpi=300, bbox_inches='tight')
    print("Detailed flowchar generated: flowchart.png")

if __name__ == "__main__":
    create_detailed_flowchart()
