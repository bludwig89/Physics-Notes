"""
viz.py  —  Visualization helpers for the Weyl CA simulation
============================================================
All functions save PNG files and print the saved path.
Requires: matplotlib, numpy
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ── helpers ──────────────────────────────────────────────────────

def _ensure(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)


def _save(fig, path, dpi=130):
    _ensure(path)
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {path}")


# ══════════════════════════════════════════════════════════════════
#  Stage 1 — Scalar wave instability grid
# ══════════════════════════════════════════════════════════════════

def save_scalar_instability(snapshots_dict, filename):
    """
    snapshots_dict : {label: [array_t0, array_t1, ...]}
    Each row = one c value; each column = one time snapshot.
    """
    labels   = list(snapshots_dict.keys())
    n_rows   = len(labels)
    n_cols   = len(list(snapshots_dict.values())[0])

    fig, axes = plt.subplots(n_rows, n_cols,
                             figsize=(3.2 * n_cols, 3.2 * n_rows))
    # Normalise axes to always be 2-D array
    if n_rows == 1:
        axes = axes[np.newaxis, :]
    if n_cols == 1:
        axes = axes[:, np.newaxis]

    for row, label in enumerate(labels):
        frames = snapshots_dict[label]
        vmax   = max(np.abs(f).max() for f in frames)
        vmax   = max(vmax, 1e-9)           # avoid vmax=0 on empty frames
        for col, frame in enumerate(frames):
            ax = axes[row, col]
            ax.imshow(np.clip(frame, -vmax, vmax).T,
                      origin='lower', cmap='RdBu_r',
                      vmin=-vmax, vmax=vmax, aspect='equal',
                      interpolation='nearest')
            ax.set_title(f't = {col * 5}', fontsize=8)
            ax.axis('off')
        # Row label on the left-most column
        axes[row, 0].set_ylabel(label, fontsize=8, rotation=0,
                                ha='right', labelpad=4)

    fig.suptitle('Stage 1 — Scalar Wave CA (Page 37)\n'
                 'Divergence without CFL-safe c; stability with c = 0.5',
                 fontsize=10)
    plt.tight_layout()
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 2 — Spinor density snapshots
# ══════════════════════════════════════════════════════════════════

def save_density_snapshots(frames, times, title, filename, cmap='inferno'):
    """
    frames : list of 2D arrays (probability density |ψ|²)
    times  : list of ints (step numbers, used as column titles)
    """
    n   = len(frames)
    fig, axes = plt.subplots(1, n, figsize=(3.5 * n, 3.5))
    if n == 1:
        axes = [axes]

    vmax = max(f.max() for f in frames)
    vmax = max(vmax, 1e-9)

    for ax, frame, t in zip(axes, frames, times):
        im = ax.imshow(frame.T, origin='lower', cmap=cmap,
                       vmin=0, vmax=vmax, aspect='equal',
                       interpolation='nearest')
        ax.set_title(f't = {t}', fontsize=9)
        ax.axis('off')
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle(title, fontsize=10)
    plt.tight_layout()
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 2 — Norm conservation
# ══════════════════════════════════════════════════════════════════

def save_norm_curve(norms_dict, filename):
    """
    norms_dict : {label_str: np.array of norms over time}
    Plots each series normalised to its initial value.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    colors  = plt.cm.plasma(np.linspace(0.15, 0.85, len(norms_dict)))

    for (label, norms), color in zip(norms_dict.items(), colors):
        n0 = norms[0] if norms[0] > 0 else 1.0
        ax.plot(norms / n0, label=label, color=color, linewidth=1.8)

    ax.axhline(1.0, color='gray', linestyle='--', linewidth=1, alpha=0.6,
               label='Perfect unitarity')
    ax.set_xlabel('Time step', fontsize=11)
    ax.set_ylabel('||ψ||² / ||ψ₀||²', fontsize=11)
    ax.set_title('Stage 2 — Norm conservation\n'
                 '(Deviation from 1.0 = truncation error)', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 3 — CFL stability curve
# ══════════════════════════════════════════════════════════════════

def save_cfl_curve(results, filename, analytic_cfl=None):
    """
    results : list of (c, peak_amplitude, diverged_flag)
    """
    c_vals   = [r[0] for r in results]
    amps     = [min(r[1], 8.0) for r in results]   # clip for readability
    diverged = [r[2] for r in results]

    colors = ['#e74c3c' if d else '#27ae60' for d in diverged]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(c_vals, amps, c=colors, zorder=5, s=60, edgecolors='k',
               linewidths=0.4)
    ax.plot(c_vals, amps, 'k-', alpha=0.2, linewidth=1)

    if analytic_cfl is not None:
        ax.axvline(analytic_cfl, color='royalblue', linestyle='--',
                   linewidth=1.6,
                   label=f'Analytic CFL bound ≈ {analytic_cfl:.3f}')

    ax.axvline(0.43, color='darkorange', linestyle=':', linewidth=1.6,
               label='Notebook observation  c ≈ 0.43  (page 39, 3D)')

    # Patch legend for colours
    from matplotlib.patches import Patch
    handles, labels_ = ax.get_legend_handles_labels()
    handles += [Patch(color='#27ae60', label='Stable'),
                Patch(color='#e74c3c', label='Diverged')]
    ax.legend(handles=handles, fontsize=8.5)

    ax.set_xlabel('c  (lattice speed factor)', fontsize=11)
    ax.set_ylabel('Peak |ψ|²  after N steps  (clipped at 8)', fontsize=11)
    ax.set_title('Stage 3 — CFL Stability Sweep\n'
                 'Reproducing the page 39 numerical observation', fontsize=10)
    ax.set_ylim(0, 8.5)
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 4 — Graph topology comparison
# ══════════════════════════════════════════════════════════════════

def save_topology_figure(spacetime_1d, snapshots_2d, snap_times, filename):
    """
    spacetime_1d : 2D array (time × cell), the 1D-ring spacetime diagram
    snapshots_2d : list of 2D density arrays at snap_times
    snap_times   : list of ints
    """
    n_snaps = len(snapshots_2d)
    fig = plt.figure(figsize=(4 + 3.5 * n_snaps, 7))
    gs  = gridspec.GridSpec(2, 1 + n_snaps, figure=fig,
                            hspace=0.35, wspace=0.3)

    # ── 1D ring spacetime diagram (spans full top row) ──
    ax_st = fig.add_subplot(gs[0, :])
    ax_st.imshow(spacetime_1d.T, origin='lower', aspect='auto',
                 cmap='inferno', interpolation='nearest')
    ax_st.set_xlabel('Time step', fontsize=9)
    ax_st.set_ylabel('Cell index', fontsize=9)
    ax_st.set_title('1D ring  (2-connection)\nSpacetime diagram', fontsize=9)

    # ── 2D grid snapshots (bottom row) ──
    vmax = max(s.max() for s in snapshots_2d)
    vmax = max(vmax, 1e-9)
    for col, (snap, t) in enumerate(zip(snapshots_2d, snap_times)):
        ax = fig.add_subplot(gs[1, col])
        ax.imshow(snap.T, origin='lower', cmap='inferno',
                  vmin=0, vmax=vmax, aspect='equal',
                  interpolation='nearest')
        ax.set_title(f'2D grid  (4-connection)\nt = {t}', fontsize=9)
        ax.axis('off')

    fig.suptitle('Stage 4 — Page 36: Dimensionality from Connection Number',
                 fontsize=11, y=1.01)
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 6 — 3D Weyl CA cross-section snapshots
# ══════════════════════════════════════════════════════════════════

def save_3d_slices(density_frames, snap_times, filename, cmap='inferno'):
    """
    Visualise a 3D spinor density field via three orthogonal central slices
    (XY, XZ, YZ) at each snapshot time.

    density_frames : list of 3D arrays, shape (Lx, Ly, Lz), |f|²+|g|²
    snap_times     : list of int (step numbers)
    """
    n_t  = len(density_frames)
    n_ax = 3          # XY, XZ, YZ

    fig, axes = plt.subplots(n_ax, n_t,
                             figsize=(3.6 * n_t, 3.6 * n_ax),
                             squeeze=False)

    slice_labels = ['XY  (z = centre)', 'XZ  (y = centre)', 'YZ  (x = centre)']

    # Global colour scale across all frames and all slices
    vmax = max(d.max() for d in density_frames)
    vmax = max(vmax, 1e-12)

    for col, (dens, t) in enumerate(zip(density_frames, snap_times)):
        Lx, Ly, Lz = dens.shape
        slices = [
            dens[:, :, Lz // 2],   # XY plane at z = centre
            dens[:, Ly // 2, :],   # XZ plane at y = centre
            dens[Lx // 2, :, :],   # YZ plane at x = centre
        ]

        for row, (sl, label) in enumerate(zip(slices, slice_labels)):
            ax = axes[row, col]
            im = ax.imshow(sl.T, origin='lower', cmap=cmap,
                           vmin=0, vmax=vmax, aspect='equal',
                           interpolation='nearest')
            if row == 0:
                ax.set_title(f't = {t}', fontsize=9, pad=4)
            if col == 0:
                ax.set_ylabel(label, fontsize=8)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.suptitle(
        'Stage 6 — 3D Weyl CA  |ψ|²  (split-step, 6-connection cubic lattice)\n'
        'Rows: XY / XZ / YZ cross-sections through the grid centre',
        fontsize=10, y=1.01)
    plt.tight_layout()
    _save(fig, filename)


# ══════════════════════════════════════════════════════════════════
#  Stage 5 — Reversibility bar chart
# ══════════════════════════════════════════════════════════════════

def save_reversibility_chart(c_values, residuals, filename):
    """
    Bar chart: time-reversal residual per c value.
    Near-machine-epsilon bars confirm approximate unitarity.
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    x_pos   = np.arange(len(c_values))

    bars = ax.bar(x_pos, residuals, color='steelblue', edgecolor='navy',
                  linewidth=0.6, zorder=3)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'c = {c}' for c in c_values], fontsize=10)

    # Annotate each bar with its value
    for bar, res in zip(bars, residuals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 1.5,
                f'{res:.1e}',
                ha='center', va='bottom', fontsize=8)

    ax.axhline(1e-14, color='crimson', linestyle='--', linewidth=1.2,
               label='~Machine epsilon  (float64 ≈ 1e-16)')
    ax.set_xlabel('Lattice speed factor  c', fontsize=11)
    ax.set_ylabel('Relative residual\n||ψ_reversed − ψ₀|| / ||ψ₀||',
                  fontsize=10)
    ax.set_title('Stage 5 — Time-Reversal Residual\n'
                 '(Fredkin reversibility: negate c and run backward)',
                 fontsize=10)
    ax.set_yscale('log')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25, axis='y', zorder=0)
    plt.tight_layout()
    _save(fig, filename)
