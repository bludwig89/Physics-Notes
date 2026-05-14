"""
live_display.py  —  Real-time 3D Weyl CA  (point-cloud renderer)
=================================================================
Displays the Weyl spinor CA as a glowing 3D point cloud.  The top
N% of density voxels are rendered as coloured points whose size and
colour encode |ψ|².  Works on any OpenGL-capable GPU without needing
volume-rendering shader support.

Based on physics notebook pages 35-39, Mark Ludwig (2007-08).

Run
---
    python3 live_display.py

Controls
--------
    Space       Pause / resume
    R           Reset to initial condition
    + / =       Increase lattice speed c  (+0.05)
    -           Decrease lattice speed c  (-0.05)
    H           Cycle helicity: left → right → mixed
    ] / [       More / fewer visible points (density threshold)
    Q / Esc     Quit

Camera
------
    Left-drag   Orbit      Right-drag / scroll   Zoom
"""

import sys
import os
import subprocess

# ── Auto-install vispy if missing ─────────────────────────────────
try:
    import vispy
except ImportError:
    print("Installing vispy...")
    for _pkg in ['vispy PyQt6', 'vispy PyQt5', 'vispy PySide6']:
        if subprocess.call(
                [sys.executable, '-m', 'pip', 'install']
                + _pkg.split() + ['--quiet']) == 0:
            break
    import vispy

# ── Pick a GUI backend ────────────────────────────────────────────
for _b in ('pyqt6', 'pyqt5', 'pyside6', 'pyside2', 'pyglet', 'glfw'):
    try:
        vispy.use(_b)
        print(f"Backend: {_b}")
        break
    except Exception:
        continue

from vispy import app, scene
from vispy.color import Colormap
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ca_core as ca


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Parameters                                                     ║
# ╚══════════════════════════════════════════════════════════════════╝
N               = 48      # grid size per axis (N³ cells)
SIGMA           = 4.5     # initial pulse width (lattice units)
C               = 0.50    # lattice speed factor
STEPS_PER_FRAME = 5       # CA steps per rendered frame
FPS             = 30      # target frame rate
DENSITY_PCTILE  = 92.0    # percentile threshold — only top (100-X)% shown
                           # raise to see fewer, brighter points
                           # lower to see more, dimmer points
POINT_SIZE      = 4.0     # base marker size in pixels
HELICITY_CYCLE  = ['left', 'right', 'mixed']

helicity = 'left'
paused   = False
step     = 0


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Colourmap  (density → RGBA colour)                             ║
# ╚══════════════════════════════════════════════════════════════════╝
_CMAP = Colormap(['#000010', '#0a0aff', '#00ddff', '#ffaa00', '#ffffff'])


def density_to_rgba(values, vmax):
    """Map density values to RGBA colours.  Higher = brighter + more opaque."""
    if vmax < 1e-12:
        return np.zeros((len(values), 4), dtype=np.float32)
    t      = np.clip(values / vmax, 0.0, 1.0).astype(np.float32)
    rgba   = _CMAP[t].rgba.astype(np.float32)
    # Alpha scales with density so dim points fade out
    rgba[:, 3] = np.clip(t ** 0.5, 0.1, 1.0)
    return rgba


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Simulation state                                               ║
# ╚══════════════════════════════════════════════════════════════════╝
def make_initial():
    return ca.gaussian_spinor_3d((N, N, N), sigma=SIGMA, helicity=helicity)

f0, g0 = make_initial()
f,  g  = f0.copy(), g0.copy()


def get_point_cloud(pctile):
    """Return (coords, colours) for voxels above the density threshold."""
    density   = (np.abs(f)**2 + np.abs(g)**2).real
    threshold = np.percentile(density, pctile)
    mask      = density > threshold
    coords    = np.argwhere(mask).astype(np.float32)   # shape (M, 3)
    values    = density[mask]
    colours   = density_to_rgba(values, density.max())
    return coords, colours, density.max(), density.sum()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Canvas and scene                                               ║
# ╚══════════════════════════════════════════════════════════════════╝
canvas = scene.SceneCanvas(
    title='Weyl Spinor CA — 3D',
    keys='interactive',
    size=(960, 720),
    show=True,
    bgcolor='#04040c',
)
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(
    fov=38,
    azimuth=30,
    elevation=22,
    distance=N * 2.6,
)

# ── Axis lines (x=red, y=green, z=blue) for orientation ──────────
_half = N / 2
_ax_pos = np.array([
    [0, _half, _half], [N, _half, _half],   # x axis
    [_half, 0, _half], [_half, N, _half],   # y axis
    [_half, _half, 0], [_half, _half, N],   # z axis
], dtype=np.float32)
_ax_col = np.array([
    [1, 0.2, 0.2, 0.5], [1, 0.2, 0.2, 0.5],
    [0.2, 1, 0.2, 0.5], [0.2, 1, 0.2, 0.5],
    [0.3, 0.5, 1, 0.5], [0.3, 0.5, 1, 0.5],
], dtype=np.float32)
scene.visuals.Line(
    pos=_ax_pos, color=_ax_col,
    connect=np.array([[0, 1], [2, 3], [4, 5]]),
    parent=view.scene,
)

# ── Initial point cloud ───────────────────────────────────────────
coords, colours, dmax, norm = get_point_cloud(DENSITY_PCTILE)

markers = scene.visuals.Markers(parent=view.scene)
markers.set_data(
    coords,
    edge_color=None,
    face_color=colours,
    size=POINT_SIZE,
    edge_width=0,
)
markers.antialias = 1


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Animation timer                                                ║
# ╚══════════════════════════════════════════════════════════════════╝
def on_timer(event):
    global f, g, step

    if paused:
        return

    for _ in range(STEPS_PER_FRAME):
        f, g  = ca.weyl_step_3d_splitstep(f, g, C)
        step += 1

    coords, colours, dmax, norm = get_point_cloud(DENSITY_PCTILE)

    if len(coords) > 0:
        markers.set_data(
            coords,
            edge_color=None,
            face_color=colours,
            size=POINT_SIZE,
            edge_width=0,
        )

    canvas.title = (
        f'Weyl CA 3D  |  t={step}  c={C:.2f}  '
        f'helicity={helicity}  '
        f'norm={norm:.2f}  peak={dmax:.5f}  '
        f'pts={len(coords)}'
    )
    canvas.update()


timer = app.Timer(interval=1.0 / FPS, connect=on_timer, start=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Keyboard controls                                              ║
# ╚══════════════════════════════════════════════════════════════════╝
@canvas.events.key_press.connect
def on_key(event):
    global f, g, step, paused, C, helicity, f0, g0, DENSITY_PCTILE

    k = event.key.name if hasattr(event.key, 'name') else str(event.key)

    if k == 'Space':
        paused = not paused
        print(f"{'Paused' if paused else 'Resumed'} at t={step}")

    elif k == 'R':
        f0, g0 = make_initial()
        f,  g  = f0.copy(), g0.copy()
        step   = 0
        print(f"Reset  helicity={helicity}  c={C:.2f}")

    elif k in ('+', '='):
        C = round(min(C + 0.05, 1.0), 2)
        print(f"c → {C}")

    elif k == '-':
        C = round(max(C - 0.05, 0.05), 2)
        print(f"c → {C}")

    elif k == 'H':
        helicity = HELICITY_CYCLE[(HELICITY_CYCLE.index(helicity) + 1) % 3]
        f0, g0   = make_initial()
        f,  g    = f0.copy(), g0.copy()
        step     = 0
        print(f"Helicity → {helicity}")

    elif k == ']':
        DENSITY_PCTILE = min(DENSITY_PCTILE + 1.0, 99.5)
        print(f"Threshold → {DENSITY_PCTILE:.1f}th percentile  (fewer points)")

    elif k == '[':
        DENSITY_PCTILE = max(DENSITY_PCTILE - 1.0, 50.0)
        print(f"Threshold → {DENSITY_PCTILE:.1f}th percentile  (more points)")

    elif k in ('Q', 'Escape'):
        timer.stop()
        app.quit()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  Entry point                                                    ║
# ╚══════════════════════════════════════════════════════════════════╝
if __name__ == '__main__':
    print("=" * 56)
    print("  Weyl Spinor CA — 3D Point Cloud")
    print(f"  Grid: {N}³  |  c={C}  |  helicity={helicity}")
    print(f"  Showing top {100 - DENSITY_PCTILE:.0f}% of density voxels")
    print("=" * 56)
    print("Controls: Space=pause  R=reset  +/-=c  H=helicity")
    print("          [ / ]=density threshold  Q=quit")
    app.run()
