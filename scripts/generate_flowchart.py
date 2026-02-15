import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def generate_flowchart_v4_fix():
    # A4 Portrait: 8.3 x 11.7 inches
    FIG_W, FIG_H = 8.3, 11.7
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # ─── Style Constants ──────────────────────────────────────────────
    BOX_W = 4.0   
    BOX_H = 1.0
    DIA_W = 2.5
    DIA_H = 1.2
    
    Y_START = 12.5
    DY = 1.25  
    
    C_START = '#C8E6C9'  # Green 100
    C_PROC  = '#BBDEFB'  # Blue 100
    C_DEC   = '#FFF9C4'  # Yellow 100
    C_IO    = '#E1BEE7'  # Purple 100
    C_END   = '#FFCDD2'  # Red 100
    EDGE    = '#37474F'
    
    def get_text_style(size=9, weight='normal', style='normal', color='black'):
        return {'fontsize': size, 'fontweight': weight, 'fontstyle': style, 'color': color, 'ha': 'center', 'va': 'center'}

    # ─── Helper Functions ─────────────────────────────────────────────
    def draw_box(x, y, title, math=None, line_ref=None, w=BOX_W, h=BOX_H, fc='#FFFFFF', shape='rect'):
        if shape == 'oval':
            patch = mpatches.BoxStyle.Round(pad=0.3)
            p = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle=patch, fc=fc, ec=EDGE, lw=1.2)
        elif shape == 'rect':
            patch = mpatches.BoxStyle.Round(pad=0.1, rounding_size=0.15)
            # Increase height for multi-line math
            if math and '\n' in math: h += 0.4
            elif math: h += 0.2
            p = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle=patch, fc=fc, ec=EDGE, lw=1.2)
        elif shape == 'parallelogram':
            skew = 0.4
            pts = [[x-w/2+skew, y-h/2], [x+w/2+skew, y-h/2], [x+w/2-skew, y+h/2], [x-w/2-skew, y+h/2]]
            p = plt.Polygon(pts, fc=fc, ec=EDGE, lw=1.2)
        elif shape == 'diamond':
            pts = [[x, y-h/2], [x+w/2, y], [x, y+h/2], [x-w/2, y]]
            p = plt.Polygon(pts, fc=fc, ec=EDGE, lw=1.2)
        
        ax.add_patch(p)
        
        # Text placement
        if math and line_ref:
            ax.text(x, y+0.25, title, **get_text_style(9, 'bold'))
            ax.text(x, y-0.05, math, **get_text_style(8.5, color='#004D40')) 
            ax.text(x, y-0.40, line_ref, **get_text_style(7, 'normal', 'normal', '#424242'))
        elif math:
            ax.text(x, y+0.15, title, **get_text_style(9, 'bold'))
            ax.text(x, y-0.20, math, **get_text_style(8.5, color='#004D40'))
        elif line_ref:
            ax.text(x, y+0.12, title, **get_text_style(9, 'bold'))
            ax.text(x, y-0.18, line_ref, **get_text_style(7.5, 'normal', 'normal', '#424242'))
        else:
            ax.text(x, y, title, **get_text_style(9, 'bold'))
            
        return h 

    def draw_arrow(x1, y1, x2, y2, text=None):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=EDGE, lw=1.2, mutation_scale=12))
        if text:
            mid_x = (x1+x2)/2
            mid_y = (y1+y2)/2
            t = ax.text(mid_x, mid_y, text, fontsize=8, fontweight='bold', color='#B71C1C', ha='center', va='center')
            t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    # ─── MAIN COLUMN (X=0) ──────────────────────────────────────────────
    
    y = Y_START
    
    # 1. Start
    draw_box(0, y, "START", w=2.0, h=0.8, fc=C_START, shape='oval')
    prev_y = y - 0.4
    y -= DY

    # 2. Read Data
    draw_box(0, y, "Read Bus & Branch Data", line_ref="(L22-75)", fc=C_IO, shape='parallelogram')
    draw_arrow(0, prev_y, 0, y + BOX_H/2)
    prev_y = y - BOX_H/2
    y -= DY

    # 3. Y-Bus
    # Replaced \sum with \Sigma if needed, but \sum works. Removed \quad.
    h_used = draw_box(0, y, "Build Y-Bus Matrix", 
                     math=r"$Y_{ij} = -y_{ij}$" "\n" r"$Y_{ii} = \sum y_{ik} + y_{shunt}$", 
                     line_ref="(L78-98)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    prev_y = y - h_used/2
    y -= DY + 0.2
    
    # 4. Init
    h_used = draw_box(0, y, "Initialize Voltages", 
             math=r"$V_i^{(0)} = 1.0 \angle 0^\circ$ (Flat Start)", 
             line_ref="(L110-116)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    prev_y = y - h_used/2
    y -= DY
    
    # 5. Calc P,Q
    y_loop_top = y
    # Used \left( \right) which is supported
    h_used = draw_box(0, y, "Compute Power Injection", 
                     math=r"$S_i = V_i \left(\sum Y_{ik} V_k\right)^*$", 
                     line_ref="(L128-130)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    prev_y = y - h_used/2
    y -= DY + 0.2
    
    # 6. Mismatches
    h_used = draw_box(0, y, "Calculate Mismatches", 
                     math=r"$\Delta P_i = P_i^{spec} - P_i^{calc}$", 
                     line_ref="(L132-136)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    prev_y = y - h_used/2
    y -= 1.6 
    
    # 7. Convergence Check
    y_diamond = y
    draw_box(0, y, "Converged?", 
             math=r"$\max|\Delta| < \epsilon$", 
             line_ref="(L151)", w=DIA_W, h=DIA_H, fc=C_DEC, shape='diamond')
    draw_arrow(0, prev_y, 0, y + DIA_H/2)
    
    y -= 1.6
    draw_arrow(0, y_diamond - DIA_H/2, 0, y + BOX_H/2 + 0.4, text="NO")
    
    # 8. Jacobian
    # Removed bmatrix. Using simplified notation.
    # Using \partial
    math_jac = r"$J_1=\partial P/\partial\delta, J_2=\partial P/\partial|V|$" "\n" r"$J_3=\partial Q/\partial\delta, J_4=\partial Q/\partial|V|$"
    h_used = draw_box(0, y, "Build Jacobian [J]", 
                     math=math_jac, 
                     line_ref="(L161-210)", fc=C_PROC)
    prev_y = y - h_used/2
    y -= DY + 0.4
    
    # 9. Solve
    # Simplified vector notation
    h_used = draw_box(0, y, "Solve System", 
                     math=r"$[J] \cdot [\Delta \delta, \Delta |V|]^T = [\Delta M]$", 
                     line_ref="(L212-213)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    prev_y = y - h_used/2
    y -= DY + 0.2
    
    # 10. Update
    y_update = y
    h_used = draw_box(0, y, "Update State", 
                     math=r"$\delta^{(k+1)} = \delta^{(k)} + \Delta \delta$" "\n" r"$|V|^{(k+1)} = |V|^{(k)} + \Delta |V|$", 
                     line_ref="(L218-224)", fc=C_PROC)
    draw_arrow(0, prev_y, 0, y + h_used/2)
    
    # ─── LOOP BACK ────────────────────────────────────────────────────
    
    loop_x = -3.5
    y_update_edge = y_update
    
    ax.plot([0 - BOX_W/2, loop_x], [y_update_edge, y_update_edge], color=EDGE, lw=1.2)
    ax.plot([loop_x, loop_x], [y_update_edge, y_loop_top], color=EDGE, lw=1.2)
    draw_arrow(loop_x, y_loop_top, 0 - BOX_W/2, y_loop_top)
    
    ax.text(loop_x - 0.2, (y_update + y_loop_top)/2, "Iterate (k = k+1)", 
            rotation=90, va='center', ha='right', fontsize=8, fontweight='bold', color='#B71C1C')

    # ─── EXIT BRANCH ──────────────────────────────────────────────────
    
    exit_x = 3.5
    
    draw_arrow(0 + DIA_W/2, y_diamond, exit_x - BOX_W/2 - 0.2, y_diamond, text="YES")
    
    # 11. Line Flows
    draw_box(exit_x, y_diamond, "Calc Line Flows", 
             math=r"$S_{ij} = V_i (V_i^* - V_j^*) Y_{ij}^*$", 
             line_ref="(L229-263)", w=BOX_W, h=BOX_H+0.4, fc=C_PROC)
    prev_y_exit = y_diamond - (BOX_H+0.4)/2
    y_exit = y_diamond - DY - 0.8
    
    # 12. Print Results
    draw_box(exit_x, y_exit, "Save & Print Results", 
             line_ref="(L266-315)", fc=C_IO, shape='parallelogram')
    draw_arrow(exit_x, prev_y_exit, exit_x, y_exit + BOX_H/2) 
    prev_y_exit = y_exit - BOX_H/2
    y_exit -= DY
    
    # 13. End
    draw_box(exit_x, y_exit, "END", w=2.0, h=0.8, fc=C_END, shape='oval')
    draw_arrow(exit_x, prev_y_exit, exit_x, y_exit + 0.4) 
    
    
    # ─── FINAL ────────────────────────────────────────────────────────
    
    ax.set_xlim(-4.8, 6.2) 
    ax.set_ylim(-1, 13)
    
    plt.tight_layout()
    plt.savefig('Report/flowchart.png', dpi=300, bbox_inches='tight')
    print("Flowchart generated: Report/flowchart.png (V4 Fix)")

if __name__ == "__main__":
    generate_flowchart_v4_fix()
