"""
tick_heatmap.py  —  T1.B visualization of the per-cell tick field N(x)
=========================================================================
Render the emergent-time tick counter as a 2D heatmap.  Used by T1.B
(plain Weyl / Φ–Dirac propagation), T5.A (vacuum freezing), and
T5.C (asymmetric tick clocks).

The colormap convention is fixed for cross-test consistency:
  - viridis on log10(1 + N)  → captures both the vacuum sea (N=0, dark)
    and the matter-dense interior (large N, bright)
  - aspect-equal grid, origin='lower' (x→right, y→up)
  - title carries the test ID + maximum N for quick visual gating.

Companion module to `ca_lazy.py`.  Imports kept light (numpy + matplotlib)
so this script is callable from `run_emergent_time_tests.py` without
dragging in the FFT propagators.
"""

import os
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# ══════════════════════════════════════════════════════════════════
#  Public API
# ══════════════════════════════════════════════════════════════════

def tick_heatmap(N_field, title='', outpath=None, vacuum_overlay=False,
                 prob_density=None, show=False):
    """
    Render N(x) as a heatmap.

    Parameters
    ----------
    N_field : 2D int64 ndarray — tick counts per cell.
    title : str — figure title.
    outpath : str or None — write PNG to this path if given.
    vacuum_overlay : bool — if True, overlay a translucent red mask on
        cells whose N == 0 (the "vacuum sea").  Used in T5.A.
    prob_density : 2D float ndarray or None — if given, plot |ψ|²
        contours on top of the tick field (for visual correlation of
        proper-time accumulation with matter density).
    show : bool — call plt.show() (Agg backend ignores this).

    Returns
    -------
    fig, ax : matplotlib objects.
    """
    if N_field.ndim != 2:
        raise ValueError("tick_heatmap expects a 2D N field; got "
                         f"shape {N_field.shape}")

    N_plot = np.log10(1.0 + N_field.astype(np.float64))
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(N_plot.T, origin='lower', cmap='viridis',
                   aspect='equal', interpolation='nearest')
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$\log_{10}(1 + N(\mathbf{x}))$')

    if vacuum_overlay:
        vac = (N_field == 0).astype(np.float64)
        ax.imshow(np.ma.masked_where(vac == 0, vac).T,
                  origin='lower', cmap='Reds', alpha=0.25,
                  aspect='equal', interpolation='nearest')

    if prob_density is not None:
        # 3 evenly spaced contour levels at the high end of |ψ|²
        pd = prob_density
        pmax = float(np.max(pd))
        if pmax > 0:
            lvls = [0.1 * pmax, 0.3 * pmax, 0.6 * pmax]
            ax.contour(pd.T, levels=lvls, colors='white',
                       linewidths=0.7, alpha=0.7)

    Nmax = int(N_field.max())
    occ = int(np.count_nonzero(N_field))
    ax.set_title(f'{title}\nmax N = {Nmax}, occupied = '
                 f'{occ}/{N_field.size}')
    ax.set_xlabel('x (cells)')
    ax.set_ylabel('y (cells)')

    fig.tight_layout()
    if outpath is not None:
        os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
        fig.savefig(outpath, dpi=120)
    if show:
        plt.show()
    plt.close(fig)
    return fig, ax


def tick_heatmap_with_phi(N_field, phi_field, title='', outpath=None,
                          show=False):
    """
    Two-panel plot: N(x) (left) and φ(x) (right) side-by-side.  Used in
    T5.C to visualize gravitational time dilation as a direct lattice
    measurement against the underlying EMQG potential.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    Nlog = np.log10(1.0 + N_field.astype(np.float64))
    im0 = axes[0].imshow(Nlog.T, origin='lower', cmap='viridis',
                         aspect='equal', interpolation='nearest')
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04,
                 label=r'$\log_{10}(1 + N)$')
    axes[0].set_title('Tick field $N(\\mathbf{x})$')
    axes[0].set_xlabel('x'); axes[0].set_ylabel('y')

    im1 = axes[1].imshow(phi_field.T, origin='lower', cmap='RdBu_r',
                         aspect='equal', interpolation='nearest')
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04,
                 label=r'$\phi(\mathbf{x})$')
    axes[1].set_title('EMQG potential $\\phi(\\mathbf{x})$')
    axes[1].set_xlabel('x'); axes[1].set_ylabel('y')

    fig.suptitle(title)
    fig.tight_layout()
    if outpath is not None:
        os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
        fig.savefig(outpath, dpi=120)
    if show:
        plt.show()
    plt.close(fig)
    return fig, axes


if __name__ == '__main__':
    # Smoke test: synthetic tick field with a Gaussian "matter" region.
    L = 64
    x = np.arange(L) - L // 2
    y = np.arange(L) - L // 2
    X, Y = np.meshgrid(x, y, indexing='ij')
    fake_N = (50.0 * np.exp(-(X * X + Y * Y) / (2.0 * 8 ** 2))).astype(np.int64)
    here = os.path.dirname(os.path.abspath(__file__))
    tick_heatmap(fake_N, title='tick_heatmap.py smoke',
                 outpath=os.path.join(here, 'figures',
                                       'ticks_smoke.png'))
    print('wrote ticks_smoke.png')
