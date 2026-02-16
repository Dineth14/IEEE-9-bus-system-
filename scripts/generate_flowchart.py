"""
Flowchart Generator for E21291_LoadFlow.py  (Newton-Raphson Load Flow)
=====================================================================
Standard Symbols:  Capsule=Terminal, Parallelogram=I/O,
                   Rectangle=Process, Diamond=Decision
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# ── Colour palette ──────────────────────────────────────────────
COL_TERM = '#FFE0B2'   # terminal  (warm peach)
COL_IO   = '#C8E6C9'   # I/O       (soft green)
COL_PROC = '#BBDEFB'   # process   (light blue)
COL_DEC  = '#FFF9C4'   # decision  (pale yellow)
COL_EDGE = '#37474F'   # lines     (dark blue-grey)
COL_BG   = '#FFFFFF'

# ── Typography ──────────────────────────────────────────────────
FONT     = 'Consolas'
FS_BODY  = 8.0
FS_HEAD  = 9.0
FS_YN    = 9.0
LW       = 1.3


# ═══════════════════  Shape primitives  ═════════════════════════

def _text(ax, x, y, txt, fs=FS_BODY, bold=False):
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs,
            fontfamily=FONT, fontweight='bold' if bold else 'normal',
            color='#212121', zorder=5)


def _multiline(ax, cx, cy, lines, h, fs=None):
    """Draw multiple lines of text, vertically centred in height *h*."""
    if fs is None:
        fs = FS_BODY
    n = len(lines)
    gap = min(h / (n + 0.8), 0.26)
    top = cy + (n - 1) * gap / 2
    for i, ln in enumerate(lines):
        _text(ax, cx, top - i * gap, ln,
              fs=FS_HEAD if i == 0 else fs, bold=(i == 0))


def capsule(ax, cx, cy, w, h, label):
    p = patches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle=f'round,pad=0,rounding_size={h/2.2}',
        fc=COL_TERM, ec=COL_EDGE, lw=LW, zorder=2)
    ax.add_patch(p)
    _text(ax, cx, cy, label, fs=FS_HEAD, bold=True)


def parallelogram(ax, cx, cy, w, h, lines):
    s = 0.40
    verts = [(cx - w/2 + s, cy + h/2),
             (cx + w/2 + s, cy + h/2),
             (cx + w/2 - s, cy - h/2),
             (cx - w/2 - s, cy - h/2)]
    ax.add_patch(patches.Polygon(verts, closed=True,
                 fc=COL_IO, ec=COL_EDGE, lw=LW, zorder=2))
    _multiline(ax, cx, cy, lines, h)


def rectangle(ax, cx, cy, w, h, lines):
    ax.add_patch(patches.Rectangle(
        (cx - w/2, cy - h/2), w, h,
        fc=COL_PROC, ec=COL_EDGE, lw=LW, zorder=2))
    _multiline(ax, cx, cy, lines, h)


def diamond(ax, cx, cy, w, h, lines):
    verts = [(cx, cy + h/2), (cx + w/2, cy),
             (cx, cy - h/2), (cx - w/2, cy)]
    ax.add_patch(patches.Polygon(verts, closed=True,
                 fc=COL_DEC, ec=COL_EDGE, lw=LW, zorder=2))
    _multiline(ax, cx, cy, lines, h, fs=FS_BODY - 0.3)


# ── Connectors ──────────────────────────────────────────────────

def arrow_v(ax, x, y1, y2):
    """Vertical arrow from (x,y1) to (x,y2)."""
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='->', lw=LW, color=COL_EDGE))


def arrow_h(ax, x1, y, x2):
    """Horizontal arrow."""
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', lw=LW, color=COL_EDGE))


def label(ax, x, y, txt):
    ax.text(x, y, txt, fontsize=FS_YN, fontweight='bold', ha='center',
            va='center', color=COL_EDGE,
            bbox=dict(fc='white', ec='none', alpha=0.9, pad=1.5))


# ═══════════════════  MAIN DRAWING  ════════════════════════════

def draw():
    fig, ax = plt.subplots(figsize=(12, 24))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.3, 23.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COL_BG)

    # ── Layout constants ────────────────────────
    XL  = 4.0       # left column centre  (main flow)
    XR  = 9.2       # right column centre (iteration branch)
    WL  = 5.0       # left-column block width
    WR  = 4.2       # right-column block width

    # ────────────────────────────────────────────
    #  1.  START
    # ────────────────────────────────────────────
    y1 = 22.8
    capsule(ax, XL, y1, 2.6, 0.7, 'START')

    # ────────────────────────────────────────────
    #  2.  READ DATA  (I/O)
    # ────────────────────────────────────────────
    y2 = 21.3
    parallelogram(ax, XL, y2, WL, 1.2,
        ['Read IEEE 9-Bus Data  (L22\u201375)',
         'bus_types,  P_spec,  Q_spec',
         'V_init,  branch_data (R, X, B)'])

    # ────────────────────────────────────────────
    #  3.  BUILD Y-BUS
    # ────────────────────────────────────────────
    y3 = 19.3
    rectangle(ax, XL, y3, WL, 1.6,
        ['Build Y-bus Admittance Matrix  (L78\u201398)',
         'z_k = R_k + j\u00b7X_k',
         'y_k = 1 / z_k   (series admittance)',
         'Y_ii  +=  y_k  +  j\u00b7B_k / 2',
         'Y_ij   =  \u2212 y_k'])

    # ────────────────────────────────────────────
    #  4.  INITIALISE
    # ────────────────────────────────────────────
    y4 = 17.0
    rectangle(ax, XL, y4, WL, 1.8,
        ['Initialise  (L104\u2013122)',
         'Slack bus : |V| = 1.04,  \u03b4 = 0\u00b0',
         'PV buses  : |V| = V_spec, \u03b4 = 0\u00b0',
         'PQ buses  : |V| = 1.0,    \u03b4 = 0\u00b0',
         'k = 0  ,  max_iter = 100',
         'tol = 1\u00d710\u207b\u2074'])

    # ────────────────────────────────────────────
    #  5.  SET  k = k + 1
    # ────────────────────────────────────────────
    y5 = 14.8
    rectangle(ax, XL, y5, 3.0, 0.65,
        ['k  =  k + 1   (L124)'])

    # ────────────────────────────────────────────
    #  6.  COMPUTE MISMATCHES
    # ────────────────────────────────────────────
    y6 = 13.3
    rectangle(ax, XL, y6, WL, 1.6,
        ['Compute Power Mismatches  (L128\u2013136)',
         'S_calc = V \u00b7 conj( Y_bus \u00b7 V )',
         '\u0394P = P_spec  \u2212  Re( S_calc )',
         '\u0394Q = Q_spec  \u2212  Im( S_calc )',
         'mismatch = [ \u0394P ; \u0394Q ]'])

    # ────────────────────────────────────────────
    #  7.  CONVERGENCE CHECK  (Decision)
    # ────────────────────────────────────────────
    y7 = 11.0
    DW, DH = 4.8, 2.2
    diamond(ax, XL, y7, DW, DH,
        ['Converged ?',
         'max | mismatch | < tol',
         '(L151\u2013156)'])

    # ────────────────────────────────────────────
    #  8.  BUILD JACOBIAN  (branch column)
    # ────────────────────────────────────────────
    y8 = y7
    rectangle(ax, XR, y8, WR, 2.0,
        ['Build Jacobian  [J]  (L167\u2013212)',
         'J1 = \u2202P/\u2202\u03b4    J2 = \u2202P/\u2202|V|',
         'J3 = \u2202Q/\u2202\u03b4    J4 = \u2202Q/\u2202|V|',
         '',
         'J = [ J1  J2 ]',
         '    [ J3  J4 ]'])

    # ────────────────────────────────────────────
    #  9.  SOLVE & UPDATE  (branch column)
    # ────────────────────────────────────────────
    y9 = 7.8
    rectangle(ax, XR, y9, WR, 2.0,
        ['Solve & Update  (L213\u2013224)',
         '\u0394x  =  J\u207b\u00b9 \u00b7 [ \u0394P ; \u0394Q ]',
         '\u03b4  \u2190  \u03b4  +  \u0394\u03b4',
         '|V|  \u2190  |V|  +  \u0394|V|',
         'V  =  |V| \u00b7 e^(j\u00b7\u03b4)'])

    # ────────────────────────────────────────────
    #  10.  k \u2265 max_iter ?  (branch decision)
    # ────────────────────────────────────────────
    y10 = 5.5
    DW2, DH2 = 4.0, 1.6
    diamond(ax, XR, y10, DW2, DH2,
        ['k \u2265 max_iter ?',
         '(L124)'])

    # ────────────────────────────────────────────
    #  11.  CALC LINE FLOWS  (main column)
    # ────────────────────────────────────────────
    y11 = 7.4
    rectangle(ax, XL, y11, WL, 1.6,
        ['Calc Line Flows & Losses  (L229\u2013263)',
         'I_ij = (Vi \u2212 Vj)\u00b7y_ser + Vi\u00b7y_sh',
         'S_ij = Vi \u00b7 conj( I_ij )',
         'S_loss = S_ij + S_ji'])

    # ────────────────────────────────────────────
    #  12.  PRINT & SAVE  (I/O)
    # ────────────────────────────────────────────
    y12 = 5.2
    parallelogram(ax, XL, y12, WL, 1.3,
        ['Print & Save Results  (L266\u2013316)',
         'Bus:  |V|, \u03b4, P, Q  \u2192  console',
         'Line flows, losses  \u2192  CSV files'])

    # ────────────────────────────────────────────
    #  13.  NOT CONVERGED  (terminal)
    # ────────────────────────────────────────────
    y13 = 3.5
    capsule(ax, XR, y13, 3.2, 0.7, 'NOT CONVERGED')

    # ────────────────────────────────────────────
    #  14.  END
    # ────────────────────────────────────────────
    y14 = 3.5
    capsule(ax, XL, y14, 2.6, 0.7, 'END')

    # ═══════════════════════════════════════════
    #  ARROWS — main trunk (left column)
    # ═══════════════════════════════════════════
    arrow_v(ax, XL, y1  - 0.35, y2  + 0.60)    # START → Read Data
    arrow_v(ax, XL, y2  - 0.60, y3  + 0.80)    # Read Data → Y-bus
    arrow_v(ax, XL, y3  - 0.80, y4  + 0.90)    # Y-bus → Init
    arrow_v(ax, XL, y4  - 0.90, y5  + 0.325)   # Init → k=k+1
    arrow_v(ax, XL, y5  - 0.325, y6 + 0.80)    # k=k+1 → Mismatches
    arrow_v(ax, XL, y6  - 0.80, y7  + DH/2)    # Mismatches → Converged?

    # YES — Converged → Line Flows
    arrow_v(ax, XL, y7  - DH/2,  y11 + 0.80)
    label(ax, XL - 0.5, y7 - DH/2 - 0.35, 'Yes')

    # Line Flows → Print
    arrow_v(ax, XL, y11 - 0.80,  y12 + 0.65)

    # Print → END
    arrow_v(ax, XL, y12 - 0.65,  y14 + 0.35)

    # ═══════════════════════════════════════════
    #  ARROWS — branch (right column)
    # ═══════════════════════════════════════════

    # NO — Converged → Jacobian  (horizontal)
    dia_r = XL + DW/2
    jac_l = XR - WR/2
    arrow_h(ax, dia_r, y7,  jac_l)
    label(ax, (dia_r + jac_l)/2, y7 + 0.35, 'No')

    # Jacobian → Solve & Update
    arrow_v(ax, XR, y8  - 1.00, y9  + 1.00)

    # Solve & Update → k ≥ max_iter?
    arrow_v(ax, XR, y9  - 1.00, y10 + DH2/2)

    # NO from k ≥ max_iter → loop back to k=k+1
    # Route: RIGHT from diamond, up to y5 level, left into k=k+1 block
    km_right = XR + DW2/2       # right edge of diamond
    loop_x   = 11.8             # far-right margin for the loop line
    kb_top   = y5               # k=k+1 block y-centre
    kb_right = XL + 1.5         # right edge of k=k+1 block

    ax.plot([km_right, loop_x], [y10, y10],
            color=COL_EDGE, lw=LW, solid_capstyle='round')
    label(ax, km_right + 0.3, y10 + 0.3, 'No')
    ax.plot([loop_x, loop_x, kb_right + 0.15],
            [y10, kb_top, kb_top],
            color=COL_EDGE, lw=LW, solid_capstyle='round')
    arrow_h(ax, kb_right + 0.15, kb_top, kb_right)

    # YES from k ≥ max_iter → NOT CONVERGED
    arrow_v(ax, XR, y10 - DH2/2, y13 + 0.35)
    label(ax, XR + 0.6, y10 - DH2/2 - 0.3, 'Yes')

    # ── Save ────────────────────────────────────
    os.makedirs('Report', exist_ok=True)
    fig.savefig('Report/flowchart.png', bbox_inches='tight',
                dpi=300, facecolor=COL_BG)
    plt.close(fig)
    print('Flowchart saved -> Report/flowchart.png')


if __name__ == '__main__':
    draw()
