"""
Generate Newton-Raphson Load Flow Flowchart with correct line numbers.
Line numbers reference E21291_LoadFlow.py (341 lines).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(11, 16))
ax.set_xlim(0, 11)
ax.set_ylim(0, 16)
ax.axis('off')
fig.patch.set_facecolor('white')

# ---- Styling ----
COLORS = {
    'start':    '#d5f5d5',  # green
    'process':  '#ddeeff',  # blue
    'decision': '#fff4cc',  # yellow
    'io':       '#e8d5f5',  # purple
    'loop':     '#ffe0cc',  # orange
}
FONT = {'fontsize': 7.5, 'fontweight': 'bold', 'ha': 'center', 'va': 'center', 'family': 'monospace'}
FONT_SM = {**FONT, 'fontsize': 6.5, 'fontweight': 'normal'}

def box(ax, cx, cy, w, h, text, sub, color, style='round'):
    fancy = mpatches.FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                     boxstyle=f"round,pad=0.08" if style == 'round' else f"square,pad=0.04",
                                     facecolor=color, edgecolor='#333333', linewidth=1.2)
    ax.add_patch(fancy)
    ax.text(cx, cy + 0.12, text, **FONT)
    ax.text(cx, cy - 0.12, sub, **FONT_SM)

def diamond(ax, cx, cy, w, h, text, sub):
    pts = [(cx, cy + h/2), (cx + w/2, cy), (cx, cy - h/2), (cx - w/2, cy)]
    poly = plt.Polygon(pts, facecolor=COLORS['decision'], edgecolor='#333333', linewidth=1.2)
    ax.add_patch(poly)
    ax.text(cx, cy + 0.08, text, **{**FONT, 'fontsize': 7})
    ax.text(cx, cy - 0.14, sub, **{**FONT_SM, 'fontsize': 6})

def arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.3))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label, fontsize=7, fontweight='bold', color='#555')

# ---- Layout (top to bottom) ----
# Column positions
CX_MAIN = 5.5   # main flow column
CX_LEFT = 2.2   # left branch (Jacobian etc.)
CX_RIGHT = 8.8  # right branch (post-convergence)

# Row positions (top = 15.5, bottom = 0.5)
Y = [15.3, 14.2, 13.1, 12.0, 10.9, 9.8, 8.7, 7.6, 6.3,  # 0-8: main flow
     5.0, 4.0, 3.0, 2.0, 1.0,   # 9-13: left branch
     5.0, 3.8, 2.4, 1.0]        # 14-17: right branch

BW, BH = 2.6, 0.55  # box width, height

# ===== MAIN FLOW =====
box(ax, CX_MAIN, Y[0], BW, BH, '1. START', '(Line 322)', COLORS['start'])
arrow(ax, CX_MAIN, Y[0]-BH/2, CX_MAIN, Y[1]+BH/2)

box(ax, CX_MAIN, Y[1], BW, BH, '2. INPUT DATA', '(Lines 22-77)', COLORS['process'])
arrow(ax, CX_MAIN, Y[1]-BH/2, CX_MAIN, Y[2]+BH/2)

box(ax, CX_MAIN, Y[2], BW, BH, '3. BUILD Y-BUS', '(Lines 80-102)', COLORS['process'])
arrow(ax, CX_MAIN, Y[2]-BH/2, CX_MAIN, Y[3]+BH/2)

box(ax, CX_MAIN, Y[3], BW, BH, '4. INITIALIZE V', '(Lines 59-62, 116)', COLORS['process'])
arrow(ax, CX_MAIN, Y[3]-BH/2, CX_MAIN, Y[4]+BH/2)

box(ax, CX_MAIN, Y[4], BW, BH, '5. IDENTIFY BUSES', '(Lines 118-121)', COLORS['process'])
arrow(ax, CX_MAIN, Y[4]-BH/2, CX_MAIN, Y[5]+BH/2)

box(ax, CX_MAIN, Y[5], BW, BH, '6. START ITERATION k', '(Line 131)', COLORS['loop'])
arrow(ax, CX_MAIN, Y[5]-BH/2, CX_MAIN, Y[6]+BH/2)

box(ax, CX_MAIN, Y[6], BW, BH, '7. CALC P, Q INJECTIONS', '(Lines 135-137)', COLORS['process'])
arrow(ax, CX_MAIN, Y[6]-BH/2, CX_MAIN, Y[7]+BH/2)

box(ax, CX_MAIN, Y[7], BW, BH, '8. CALC MISMATCHES', '(Lines 139-142)', COLORS['process'])
arrow(ax, CX_MAIN, Y[7]-BH/2, CX_MAIN, Y[8]+0.35)

# Diamond
diamond(ax, CX_MAIN, Y[8], 2.8, 0.7, '9. CONVERGED?', '(Line 158)')

# ===== LEFT BRANCH (NO) =====
# Arrow from diamond left
ax.annotate('', xy=(CX_LEFT + BW/2, Y[9]+BH/2), xytext=(CX_MAIN - 1.4, Y[8]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.3))
ax.text(CX_MAIN - 1.6, Y[8] + 0.15, 'NO', fontsize=8, fontweight='bold', color='#cc3333')

box(ax, CX_LEFT, Y[9], BW, BH, '10. BUILD JACOBIAN', '(Lines 168-210)', COLORS['process'])
arrow(ax, CX_LEFT, Y[9]-BH/2, CX_LEFT, Y[10]+BH/2)

box(ax, CX_LEFT, Y[10], BW, BH, '11. SOLVE SYSTEM', '(Line 212)', COLORS['process'])
arrow(ax, CX_LEFT, Y[10]-BH/2, CX_LEFT, Y[11]+BH/2)

box(ax, CX_LEFT, Y[11], BW, BH, '12. EXTRACT CORRECTIONS', '(Lines 214-215)', COLORS['process'])
arrow(ax, CX_LEFT, Y[11]-BH/2, CX_LEFT, Y[12]+BH/2)

box(ax, CX_LEFT, Y[12], BW, BH, '13. UPDATE VOLTAGES', '(Lines 217-223)', COLORS['process'])
arrow(ax, CX_LEFT, Y[12]-BH/2, CX_LEFT, Y[13]+BH/2)

box(ax, CX_LEFT, Y[13], BW-0.2, BH, '14. NEXT ITERATION', '(Loop back to 6)', COLORS['loop'])

# Loop-back arrow from box 14 → box 6
ax.annotate('', xy=(CX_MAIN - BW/2, Y[5]),
            xytext=(CX_LEFT - BW/2, Y[13]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.3,
                           connectionstyle='arc3,rad=0.4'))

# ===== RIGHT BRANCH (YES) =====
ax.annotate('', xy=(CX_RIGHT - BW/2, Y[14]+BH/2), xytext=(CX_MAIN + 1.4, Y[8]),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.3))
ax.text(CX_MAIN + 1.15, Y[8] + 0.15, 'YES', fontsize=8, fontweight='bold', color='#339933')

box(ax, CX_RIGHT, Y[14], BW, BH, '15. RETURN V', '(Line 163)', COLORS['io'])
arrow(ax, CX_RIGHT, Y[14]-BH/2, CX_RIGHT, Y[15]+BH/2)

box(ax, CX_RIGHT, Y[15], BW, BH, '16. CALC LINE FLOWS', '(Lines 228-264)', COLORS['process'])
arrow(ax, CX_RIGHT, Y[15]-BH/2, CX_RIGHT, Y[16]+BH/2)

box(ax, CX_RIGHT, Y[16], BW, BH, '17. PRINT RESULTS', '(Lines 267-293)', COLORS['io'])
arrow(ax, CX_RIGHT, Y[16]-BH/2, CX_RIGHT, Y[17]+BH/2)

box(ax, CX_RIGHT, Y[17], BW-0.4, BH, '18. END', '(Line 341)', COLORS['start'])

# Title
ax.text(5.5, 15.85, 'Newton-Raphson Load Flow — Program Flowchart', 
        fontsize=12, fontweight='bold', ha='center', va='center', color='#222')
ax.text(5.5, 15.6, 'Line numbers reference E21291_LoadFlow.py', 
        fontsize=8, ha='center', va='center', color='#666', style='italic')

plt.tight_layout()
plt.savefig('flowchart.png', dpi=200, bbox_inches='tight', facecolor='white')
print("Saved flowchart.png")
