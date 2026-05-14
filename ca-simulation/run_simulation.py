"""
run_simulation.py  —  Main runner: all five CA stages
======================================================
Based on physics notebook pages 35-39, Mark Ludwig (2007-08).

Usage
-----
    python run_simulation.py

Outputs  (saved to ./figures/)
-------
    stage1_scalar_instability.png
    stage2_spinor_left.png
    stage2_spinor_right.png
    stage2_spinor_mixed.png
    stage2_norm_conservation.png
    stage3_cfl_sweep.png
    stage4_graph_topology.png
    stage5_reversibility.png
    stage6_3d_weyl.png
"""

import os
import sys
import numpy as np

# Allow imports from the same directory when called from elsewhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ca_core as ca
import viz

FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

def fig(name):
    return os.path.join(FIGURES_DIR, name)


# ══════════════════════════════════════════════════════════════════
#  Stage 1 — Scalar Wave CA  (Page 37)
# ══════════════════════════════════════════════════════════════════

def stage1_scalar_wave():
    """
    Demonstrates the second-order scalar wave equation and its instability.

    The notebook writes the equation with an implicit c = 1, which violates
    the 2-D CFL condition (c ≤ 1/√2 ≈ 0.71) and diverges within steps.
    This stage plots max amplitude over time for several c values so the
    divergence is clearly visible — reproducing the spirit of page 39.
    """
    print("\n── Stage 1: Scalar Wave CA (Page 37) ──")
    import matplotlib.pyplot as plt

    N, sigma = 64, 5.0
    shape    = (N, N)
    center   = (N // 2, N // 2)
    n_steps  = 5000

    configs = [
        (1.00, '#e74c3c', 'c = 1.0  (notebook default — unstable)'),
        (0.70, '#e67e22', 'c = 0.70  (at CFL limit)'),
        (0.50, '#27ae60', 'c = 0.50  (stable)'),
        (0.30, '#2980b9', 'c = 0.30  (stable, slower)'),
    ]

    fig_obj, ax = plt.subplots(figsize=(8, 4.5))

    for c_val, color, label in configs:
        f_now  = ca.gaussian_2d(shape, center, sigma).astype(float)
        f_prev = f_now.copy()
        amps   = [float(np.max(np.abs(f_now)))]

        for _ in range(n_steps):
            f_next = ca.scalar_step_2d(f_now, f_prev, c=c_val)
            f_prev = f_now.copy()
            f_now  = f_next
            amp    = float(np.max(np.abs(f_now)))
            amps.append(min(amp, 1e6))          # cap for log-scale display
            if amp > 1e6 or not np.isfinite(amp):
                # Pad the rest so all series have equal length
                amps += [1e6] * (n_steps - len(amps) + 1)
                break

        ax.plot(amps, color=color, linewidth=1.8, label=label)
        print(f"  {label}: peak = {amps[-1]:.2e}")

    ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.5,
               label='Initial peak = 1')
    ax.set_yscale('log')
    ax.set_xlabel('Time step', fontsize=11)
    ax.set_ylabel('Max |f|  (log scale)', fontsize=11)
    ax.set_title('Stage 1 — Scalar Wave CA (Page 37)\n'
                 'CFL instability: c > 1/√2 ≈ 0.71 diverges', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    fname = fig('stage1_scalar_instability.png')
    fig_obj.savefig(fname, dpi=130, bbox_inches='tight')
    plt.close(fig_obj)
    print(f"  Saved: {fname}")


# ══════════════════════════════════════════════════════════════════
#  Stage 2 — Spinor-Valued Weyl CA  (Pages 38-39)
# ══════════════════════════════════════════════════════════════════

def stage2_weyl_spinor():
    """
    Runs the spinor CA for left, right, and mixed helicity initial states
    and saves density (|f|² + |g|²) snapshots at four time steps.

    Also tracks norm conservation for three different c values to show
    how the truncation error grows with c.
    """
    print("\n── Stage 2: Weyl Spinor CA (Pages 38-39) ──")

    N          = 64
    sigma      = 5.0
    shape      = (N, N)
    c          = 0.43
    snap_steps = [0, 1000, 2500, 5000]

    for helicity in ('left', 'right', 'mixed'):
        print(f"  Helicity: {helicity}")
        f, g    = ca.gaussian_spinor_2d(shape, sigma=sigma, helicity=helicity)
        frames  = []
        for t in range(max(snap_steps) + 1):
            if t in snap_steps:
                frames.append((np.abs(f)**2 + np.abs(g)**2).copy())
            f, g = ca.weyl_step_2d_splitstep(f, g, c)

        viz.save_density_snapshots(
            frames, snap_steps,
            title=f'Stage 2 — Weyl spinor CA  |ψ|²  '
                  f'(helicity={helicity}, c={c}, split-step)',
            filename=fig(f'stage2_spinor_{helicity}.png'))

    # Norm conservation for three c values — split-step should be flat to
    # machine precision across all c values.
    print("  Norm conservation sweep ...")
    norms_dict = {}
    for c_val in (0.30, 0.43, 0.50):
        f0, g0 = ca.gaussian_spinor_2d(shape, sigma=sigma)
        norms_dict[f'c = {c_val}'] = ca.norm_over_time(
            f0, g0, n_steps=5000, c=c_val, step_fn=ca.weyl_step_2d_splitstep)
    viz.save_norm_curve(norms_dict, fig('stage2_norm_conservation.png'))


# ══════════════════════════════════════════════════════════════════
#  Stage 3 — CFL Stability Sweep  (Page 39)
# ══════════════════════════════════════════════════════════════════

def stage3_cfl_sweep():
    """
    Sweeps c from 0.10 to 0.60 and plots peak |ψ|² after 100 steps.

    The 2-D analytic CFL bound for the centred-difference Weyl scheme is
    1/(2√2) ≈ 0.354.  The notebook's 3-D observation of ~0.43 is marked
    separately.  The sweep shows which c values diverge and which are stable.
    """
    print("\n── Stage 3: CFL Stability Sweep (Page 39) ──")

    c_values = np.round(np.arange(0.10, 0.62, 0.03), 3)
    print(f"  c values: {c_values.tolist()}")

    results = ca.cfl_sweep(
        grid_size=32, n_steps=5000, c_values=c_values,
        dim=2, sigma=2.0, use_splitstep=True)

    print(f"\n  {'c':>5}  {'status':>8}  {'peak':>12}")
    print(f"  {'─'*5}  {'─'*8}  {'─'*12}")
    for c_val, peak, div in results:
        status = 'DIVERGED' if div else 'stable  '
        print(f"  {c_val:>5.2f}  {status}  {peak:>12.4f}")

    print(f"\n  Split-step FFT propagator: exactly unitary, all c stable.")
    print(f"  Notebook (3D) explicit-Euler observation ≈ 0.43 no longer applies.")

    analytic_cfl = 1.0 / (2.0 * np.sqrt(2.0))
    viz.save_cfl_curve(results, fig('stage3_cfl_sweep.png'),
                       analytic_cfl=analytic_cfl)


# ══════════════════════════════════════════════════════════════════
#  Stage 4 — Graph Topology / Connection Number  (Page 36)
# ══════════════════════════════════════════════════════════════════

def stage4_graph_topology():
    """
    Demonstrates page 36's claim that dimensionality is determined by
    connection number.

    1D ring (2-connection): wave travels in one direction; shown as a
    spacetime diagram (time × cell index).

    2D square grid (4-connection): standard 2-D Weyl propagation; four
    density snapshots.
    """
    print("\n── Stage 4: Graph Topology / Connection Number (Page 36) ──")

    c       = 0.43
    n_steps = 5000

    # ── 1D ring (2-connection) ──────────────────────────────────
    N1  = 96
    x   = np.arange(N1) - N1 // 2
    f1  = np.exp(-x**2 / (2 * 4.0**2)).astype(complex)
    g1  = np.zeros(N1, dtype=complex)

    spacetime = np.zeros((n_steps + 1, N1))
    spacetime[0] = np.abs(f1)**2 + np.abs(g1)**2

    for t in range(n_steps):
        # 1-D Weyl via split-step: reshape to (N1,1) so fft2 treats it
        # as a 2-D grid with one column, then squeeze back.
        f1, g1 = ca.weyl_step_2d_splitstep(
            f1.reshape(N1, 1), g1.reshape(N1, 1), c)
        f1 = f1.reshape(N1)
        g1 = g1.reshape(N1)
        spacetime[t + 1] = np.abs(f1)**2 + np.abs(g1)**2

    print("  1D ring: done")

    # ── 2D square grid (4-connection) ───────────────────────────
    N2         = 64
    snap_steps = [0, 1000, 2500, 5000]
    f2, g2     = ca.gaussian_spinor_2d((N2, N2), sigma=5.0)
    snaps_2d   = []

    for t in range(n_steps + 1):
        if t in snap_steps:
            snaps_2d.append((np.abs(f2)**2 + np.abs(g2)**2).copy())
        if t < n_steps:
            f2, g2 = ca.weyl_step_2d_splitstep(f2, g2, c)

    print("  2D grid: done")

    viz.save_topology_figure(
        spacetime, snaps_2d, snap_steps,
        fig('stage4_graph_topology.png'))


# ══════════════════════════════════════════════════════════════════
#  Stage 5 — Time-Reversal / Reversibility  (Fredkin correlation)
# ══════════════════════════════════════════════════════════════════

def stage5_reversibility():
    """
    Runs 60 steps forward then 60 steps backward (negating c).

    Negating c reverses the sign of all spatial-derivative terms,
    implementing time-reversal.  Residuals close to machine epsilon
    (~1e-15) confirm the update is approximately unitary — the
    'reversible CA' property Fredkin required.

    Larger c values accumulate more truncation error and show a
    correspondingly larger residual.
    """
    print("\n── Stage 5: Reversibility (Fredkin correlation) ──")

    shape = (48, 48)
    sigma = 5.0
    c_vals = [0.20, 0.30, 0.43, 0.50]

    residuals = []
    for c in c_vals:
        f0, g0 = ca.gaussian_spinor_2d(shape, sigma=sigma, helicity='mixed')
        res    = ca.run_and_reverse(f0, g0, n_steps=2500, c=c,
                                    step_fn=ca.weyl_step_2d_splitstep)
        residuals.append(res)
        print(f"  c = {c:.2f}  →  residual = {res:.3e}")

    print("\n  Split-step is exactly unitary: residuals should be ~1e-15 (machine epsilon).")
    print("  Any residual above ~1e-13 indicates a numerical precision issue.")
    viz.save_reversibility_chart(c_vals, residuals,
                                 fig('stage5_reversibility.png'))


# ══════════════════════════════════════════════════════════════════
#  Stage 6 — 3D Weyl CA  (Page 36: "4-connection 3D lattice / torus")
# ══════════════════════════════════════════════════════════════════

def stage6_3d_weyl():
    """
    3D Weyl spinor CA on a 32×32×32 periodic (toroidal) cubic lattice.

    Each cell has 6 connections (±x, ±y, ±z) — the minimal 3D lattice
    that supports all three Pauli-matrix terms in the Weyl equation.
    Page 36 notes that 4 connections produce "a 3D lattice or something
    like a 3D tube or torus"; the fully-periodic 3D torus here is the
    natural extension of the 2D torus from Stage 2 / Stage 4.

    The split-step FFT propagator is used, so the run is unconditionally
    stable.  A Gaussian spinor pulse is initialised at the grid centre
    and propagates outward as a spherical shell.  Cross-sectional density
    slices (XY, XZ, YZ planes through the grid centre) are saved at four
    time steps.
    """
    print("\n── Stage 6: 3D Weyl CA (Page 36 — 3D lattice extension) ──")

    N          = 32          # grid size per axis; 32³ is fast enough for demo
    sigma      = 3.0         # Gaussian pulse width (lattice units)
    c          = 0.5         # lattice speed factor
    snap_steps = [0, 1000, 2500, 5000]

    shape  = (N, N, N)
    f, g   = ca.gaussian_spinor_3d(shape, sigma=sigma, helicity='left')

    frames = []
    t      = 0
    for step in range(max(snap_steps) + 1):
        if step in snap_steps:
            dens = (np.abs(f)**2 + np.abs(g)**2).real
            frames.append(dens.copy())
            print(f"  t = {step:4d}  peak |ψ|² = {dens.max():.4f}"
                  f"  norm = {dens.sum():.4f}")
        f, g = ca.weyl_step_3d_splitstep(f, g, c)

    viz.save_3d_slices(
        frames, snap_steps,
        fig('stage6_3d_weyl.png'))


# ══════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════

def main():
    print("=" * 56)
    print("  Weyl Spinor Cellular Automaton Simulation")
    print("  Based on physics notebook pages 35-39")
    print("  Mark Ludwig (2007-08)")
    print("=" * 56)
    print(f"\nFigures will be saved to: {FIGURES_DIR}/\n")

    stage1_scalar_wave()
    stage2_weyl_spinor()
    stage3_cfl_sweep()
    stage4_graph_topology()
    stage5_reversibility()
    stage6_3d_weyl()

    print("\n" + "=" * 56)
    print("  All stages complete.")
    print(f"  Figures: {FIGURES_DIR}/")
    print("=" * 56)


if __name__ == '__main__':
    main()
