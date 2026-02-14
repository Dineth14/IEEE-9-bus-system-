"""
Newton-Raphson Load Flow Flowchart — E21291_LoadFlow.py (328 lines)
Compact single-column layout designed for A4 page embedding.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Canvas setup ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 10.5))
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')

# ── Layout constants ────────────────────────────────────────────
CX = 5.0           # centre x for main column
RX = 11.5          # centre x for YES branch
BW = 5.0           # box width
BH = 1.15          # box height
DIA = 1.1          # diamond half-height
GAP = 0.35         # gap between boxes (arrow length)
EDGE_C = '#37474F'

# Colours
C_START = '#66BB6A'
C_END   = '#66BB6A'
C_PROC  = '#64B5F6'
C_DEC   = '#FFF176'
C_IO    = '#CE93D8'

# Text styles
def _ts(size, bold=False, mono=False):
    return dict(fontsize=size, fontweight='bold' if bold else 'normal',
                fontfamily='monospace' if mono else 'sans-serif',
                ha='center', va='center')

T_TITLE = _ts(9, bold=True)
T_SUB   = _ts(7, mono=True)
T_REF   = {**_ts(7), 'color': '#555', 'style': 'italic'}
T_LBL   = _ts(8.5, bold=True)

# ── Drawing primitives ──────────────────────────────────────────
def _label(cx, cy, title, sub=None, ref=None):
    gap = 0.28
    n = 1 + (sub is not None) + (ref is not None)
    y = cy + (n - 1) * gap / 2
    ax.text(cx, y, title, **T_TITLE, color='#111')
    if sub:
        y -= gap
        ax.text(cx, y, sub, **T_SUB, color='#333')
    if ref:
        y -= gap
        ax.text(cx, y, ref, **T_REF)

def rounded_box(cx, cy, title, sub=None, ref=None, w=BW, h=BH, fc=C_PROC):
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.1', fc=fc, ec=EDGE_C, lw=1.2))
    _label(cx, cy, title, sub, ref)

def oval(cx, cy, title, ref=None, w=BW, h=BH, fc=C_START):
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.3', fc=fc, ec=EDGE_C, lw=1.3))
    _label(cx, cy, title, ref=ref)

def parallelogram(cx, cy, title, ref=None, w=BW, h=BH, fc=C_IO):
    sk = 0.4
    pts = np.array([[cx-w/2+sk, cy+h/2], [cx+w/2+sk, cy+h/2],
                     [cx+w/2-sk, cy-h/2], [cx-w/2-sk, cy-h/2]])
    ax.add_patch(plt.Polygon(pts, closed=True, fc=fc, ec=EDGE_C, lw=1.2))
    _label(cx, cy, title, ref=ref)

def diamond(cx, cy, title, ref=None, w_ext=1.8, h_ext=DIA):
    pts = np.array([[cx, cy+h_ext], [cx+w_ext, cy],
                     [cx, cy-h_ext], [cx-w_ext, cy]])
    ax.add_patch(plt.Polygon(pts, closed=True, fc=C_DEC, ec=EDGE_C, lw=1.2))
    _label(cx, cy, title, ref=ref)

# ── Arrow helpers ───────────────────────────────────────────────
_AP = dict(arrowstyle='->', lw=1.2, color=EDGE_C, mutation_scale=12)

def varrow(x, y1, y2):
    ax.annotate('', xy=(x, y2), xytext=(x, y1), arrowprops=_AP)

def harrow(x1, y, x2):
    ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=_AP)

def vline(x, y1, y2):
    ax.plot([x, x], [y1, y2], color=EDGE_C, lw=1.2)

def hline(x1, x2, y):
    ax.plot([x1, x2], [y, y], color=EDGE_C, lw=1.2)

# ── Compute row Y positions (top-down) ──────────────────────────
# Each row: y_centre.  Spacing = BH + GAP normally, larger for diamond.
rows = []
y = 13.0  # starting y

# Row 0: START
rows.append(y); y -= (BH + GAP)
# Row 1: Read Data
rows.append(y); y -= (BH + GAP)
# Row 2: Build Y-bus
rows.append(y); y -= (BH + GAP)
# Row 3: Classify & Init
rows.append(y); y -= (BH + GAP)
# Row 4: Compute P,Q
rows.append(y); y -= (BH + GAP)
# Row 5: Mismatches
rows.append(y); y -= (BH/2 + 0.15 + DIA)
# Row 6: Decision diamond
rows.append(y); y -= (DIA + 0.15 + BH/2)
# Row 7: Build Jacobian
rows.append(y); y -= (BH + GAP)
# Row 8: Solve
rows.append(y); y -= (BH + GAP)
# Row 9: Update
rows.append(y)

# Right column rows (YES branch) — aligned with rows 6,7,8,9
ry6 = rows[6]
ry7 = rows[7]
ry8 = rows[8]
ry9 = rows[9]

# ═══════════════════════════════════════════════════════════════
# DRAW FLOWCHART
# ═══════════════════════════════════════════════════════════════

# R0 — START
oval(CX, rows[0], 'START', 'Line 309', h=0.85)
varrow(CX, rows[0] - 0.85/2, rows[1] + BH/2)

# R1 — Read Data (I/O)
parallelogram(CX, rows[1], 'Read IEEE 9-Bus Data',
              'get_ieee_9_bus_data()  L22–75')
varrow(CX, rows[1] - BH/2, rows[2] + BH/2)

# R2 — Build Y-bus
rounded_box(CX, rows[2], 'Build Y-bus Matrix',
            ref='build_y_bus()  L78–98')
varrow(CX, rows[2] - BH/2, rows[3] + BH/2)

# R3 — Classify & Init V
rounded_box(CX, rows[3], 'Classify Buses & Init V',
            sub='Slack / PV / PQ ; flat start',
            ref='L109–116')
varrow(CX, rows[3] - BH/2, rows[4] + BH/2)

# R4 — Compute P,Q  (loop re-entry point)
rounded_box(CX, rows[4], 'Compute P_calc, Q_calc',
            sub='S = V · conj(Y·V)',
            ref='L128–130')
varrow(CX, rows[4] - BH/2, rows[5] + BH/2)

# R5 — Mismatches
rounded_box(CX, rows[5], 'Compute ΔP, ΔQ Mismatches',
            sub='ΔP = P_spec − P_calc',
            ref='L132–136')
varrow(CX, rows[5] - BH/2, rows[6] + DIA)

# R6 — Convergence decision
diamond(CX, rows[6], 'max|Δ| < ε ?', 'ε = 1×10⁻⁴  (L151)')

# ---- YES branch → right column ----
harrow(CX + 1.8, ry6, RX - BW/2)
ax.text(CX + 2.0, ry6 + 0.3, 'YES', color='#2E7D32', **T_LBL)

rounded_box(RX, ry6, 'Return V, P, Q', ref='L156', h=0.85)
varrow(RX, ry6 - 0.85/2, ry7 + BH/2)

rounded_box(RX, ry7, 'Calculate Line Flows',
            ref='calculate_line_flows()  L221–255')
varrow(RX, ry7 - BH/2, ry8 + BH/2)

parallelogram(RX, ry8, 'Print & Save Results',
              'print_results() L258  /  save_csv() L285')
varrow(RX, ry8 - BH/2, ry9 + 0.85/2)

oval(RX, ry9, 'END', 'Line 328', h=0.85, fc=C_END)

# ---- NO branch → continue down main column ----
varrow(CX, rows[6] - DIA, rows[7] + BH/2)
ax.text(CX + 0.2, rows[6] - DIA - 0.12, 'NO', color='#C62828', **T_LBL)

# R7 — Build Jacobian
rounded_box(CX, rows[7], 'Build Jacobian [J]',
            sub='J1, J2, J3, J4 sub-matrices',
            ref='L158–204')
varrow(CX, rows[7] - BH/2, rows[8] + BH/2)

# R8 — Solve
rounded_box(CX, rows[8], 'Solve [J]·Δx = mismatch',
            sub='np.linalg.solve()',
            ref='L205')
varrow(CX, rows[8] - BH/2, rows[9] + BH/2)

# R9 — Update voltages
rounded_box(CX, rows[9], 'Update δ and |V|',
            sub='δ += Δδ  ;  |V| += Δ|V|',
            ref='L207–216')

# ---- Loop-back arrow ----
loop_bottom = rows[9] - BH/2 - 0.25
loop_left   = CX - BW/2 - 0.7

vline(CX, rows[9] - BH/2, loop_bottom)
hline(loop_left, CX, loop_bottom)
vline(loop_left, loop_bottom, rows[4])
harrow(loop_left, rows[4], CX - BW/2)

# "iterate" label
ax.text(loop_left - 0.1, (loop_bottom + rows[4]) / 2, 'iterate',
        fontsize=7, fontweight='bold', color='#C62828',
        ha='right', va='center', rotation=90, fontfamily='sans-serif')

# ── Crop tightly ────────────────────────────────────────────────
ax.set_xlim(loop_left - 0.8, RX + BW/2 + 0.5)
ax.set_ylim(loop_bottom - 0.6, rows[0] + 0.85/2 + 0.5)

plt.tight_layout(pad=0.05)
plt.savefig('flowchart.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Done — flowchart.png (300 DPI)')
