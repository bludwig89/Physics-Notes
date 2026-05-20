"""
poisson_open.py  —  Open-boundary 3D Poisson solver
====================================================
Date: 2026-05-19

Implements the James/Hockney zero-padded FFT trick to solve

    ∇² φ(x) = 4π G ρ(x)        with  φ → 0 as |x| → ∞

on a *non-periodic* cubic domain.  The price is 8× memory (doubled grid in
each dimension); the benefit is the correct free-space Green's function
$G(r) = -1/(4\pi r)$ instead of the periodic-cell sum.

Method
------
1. Pad the source ρ from shape (L, L, L) to (2L, 2L, 2L) with zeros.
2. Build the free-space Green's function on the doubled grid:
       G(r) = -1/(4π r)    for r > 0,
       G(0) = -1/(4π · h_self)  (self-interaction smoothed; h_self ≈ 0.5
                                  for a unit-spacing cell, chosen so the
                                  Coulomb sum converges to the correct
                                  near-source potential).
3. FFT both ρ_pad and G on the doubled grid.
4. φ_pad_k = -4π G · ρ_pad_k · G_k   (Convolution theorem; signs work out
   so the prefactor is +1.)
5. Inverse FFT, crop the central (L, L, L) region.

This recovers the free-space Newtonian potential φ(x) = -G·∫ρ(y)/|x-y| dy
to machine precision, in O(L³ log L) time.

The "self" cell (r=0) needs care: the discrete Green's function at the
source cell can't be literally -1/(4π·0).  A common choice is to set
G(0) = -1/(4π · (3/(4π))^(1/3)) ≈ -0.2247, the sphere-equivalent radius
for a unit-volume cell.  Different choices shift the absolute potential
at the source by a constant; far-field gradients (which is what matters
for lensing) are unaffected.

For this implementation we use the simpler r_min = 0.5 (half-cell radius)
which gives smooth potential at the source.  At distances r ≫ 1 the
solver recovers exact 1/r to machine precision.
"""

import numpy as np


def green_freespace_3d(L_pad, r_min=0.5):
    """
    Construct the free-space Newtonian Green's function on a (L_pad)^3 grid,
    centered at index 0 (so that the FFT convolution is correctly aligned).

    The grid is interpreted as periodic for FFT purposes but the *output*
    after cropping is the free-space convolution.

    Parameters
    ----------
    L_pad : int
        Total grid size (must be ≥ 2L for the zero-pad to work).
    r_min : float
        Cutoff radius for the self-cell (r=0 origin) to avoid the singular
        1/0.  Default 0.5 — half-cell distance.  Far-field unaffected.

    Returns
    -------
    G : ndarray of shape (L_pad, L_pad, L_pad)
        G(i, j, k) = -1 / (4π r),  r = min-image distance from origin
                                       on a doubled box.
    """
    # Build periodic indices that give the *minimum-image* distance.  On
    # an L_pad × L_pad × L_pad torus, the cell at index i sits at
    #     x = i        if  i ≤ L_pad/2
    #     x = i - L_pad if  i >  L_pad/2
    # Min-image distance from origin: x = min(i, L_pad - i)
    idx = np.arange(L_pad)
    # Use signed offsets so that origin is at index 0:
    offs = np.where(idx <= L_pad // 2, idx, idx - L_pad).astype(np.float64)
    X, Y, Z = np.meshgrid(offs, offs, offs, indexing='ij')
    r = np.sqrt(X**2 + Y**2 + Z**2)
    r = np.maximum(r, r_min)
    G = -1.0 / (4.0 * np.pi * r)
    return G


def solve_poisson_3d_open(rho, G_N=1.0, r_min=0.5):
    """
    Solve the 3-D Newtonian Poisson equation with open (free-space) boundary
    conditions:

        ∇²φ = 4π G_N ρ,   φ → 0 at infinity.

    Implementation: zero-padded FFT convolution with the free-space Green
    function -1/(4π r).

    Parameters
    ----------
    rho : real ndarray, shape (L, L, L)
        Mass density on a periodic-cell-friendly cubic grid.  The output is
        the *free-space* potential — i.e., it does NOT contain image-mass
        contributions from the surrounding tile of repeated cells.
    G_N : float
        Newton's constant (lattice units).
    r_min : float
        Self-cell regularisation radius; see `green_freespace_3d`.

    Returns
    -------
    phi : real ndarray, shape (L, L, L)
        Potential satisfying ∇²φ = 4π G_N ρ to discretisation precision.
        At |x| ≫ source extent, φ → -G_N M_tot / r (correct 1/r tail).
    """
    L = rho.shape[0]
    assert rho.shape == (L, L, L), 'rho must be cubic'
    L_pad = 2 * L
    # Zero-pad
    rho_pad = np.zeros((L_pad, L_pad, L_pad), dtype=rho.dtype)
    rho_pad[:L, :L, :L] = rho
    # Free-space Green's function on the doubled grid
    G = green_freespace_3d(L_pad, r_min=r_min)
    # FFT convolution.  Solving ∇²φ = 4π G_N ρ with the Green's function
    # G(r) = -1/(4π r) (which satisfies ∇² G(r) = δ(r) in 3D) gives
    #     φ(x) = 4π G_N · ∫ G(x-y) ρ(y) dy
    #          = -G_N · ∫ ρ(y) / |x-y| dy.
    # That's the attractive Newtonian potential.  In Fourier:
    #     φ_k = 4π G_N · ρ_k · G_k.
    rho_k = np.fft.rfftn(rho_pad)
    G_k   = np.fft.rfftn(G)
    phi_k = 4.0 * np.pi * G_N * rho_k * G_k
    phi_pad = np.fft.irfftn(phi_k, s=(L_pad, L_pad, L_pad),
                              axes=(0, 1, 2))
    # Crop the central (L, L, L) region.  The convolution shifts the
    # origin: ρ_pad is at indices [0, L), G is centered at index 0, so
    # the output corresponds to integer shifts in x ∈ [0, L_pad).  The
    # physical "free-space" potential at cell i_source = (a, b, c) in
    # ρ is phi_pad[a, b, c].
    return phi_pad[:L, :L, :L]


def gaussian_mass_3d(L, M=1.0, sigma=3.0, center=None):
    """Gaussian-smoothed point mass at center, total integrated mass M."""
    if center is None:
        center = (L//2, L//2, L//2)
    x = np.arange(L) - center[0]
    y = np.arange(L) - center[1]
    z = np.arange(L) - center[2]
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    rho = np.exp(-(X**2 + Y**2 + Z**2) / (2*sigma**2))
    rho *= M / rho.sum()
    return rho


# ══════════════════════════════════════════════════════════════════
#  Verification
# ══════════════════════════════════════════════════════════════════

def test_point_mass_far_field():
    """
    Verify φ(r) → -G_N M / r at distances r ≫ source width.

    Returns relative error |φ_numerical / φ_analytic - 1| at a few far cells.
    """
    L = 96
    M = 1.0
    sigma = 3.0
    G_N = 1.0
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi = solve_poisson_3d_open(rho, G_N=G_N)

    cx = L // 2
    print(f'  Far-field test (L={L}, sigma={sigma}, M={M}, G_N={G_N}):')
    print(f'  {"r":>6} {"phi_num":>16} {"phi_analytic":>16} {"rel_err":>12}')
    rel_errs = []
    for r in [10, 15, 20, 25, 30, 35, 40]:
        phi_num = phi[cx + r, cx, cx]
        phi_analytic = -G_N * M / r
        rel_err = abs(phi_num / phi_analytic - 1.0)
        rel_errs.append(rel_err)
        print(f'  {r:>6} {phi_num:>16.6e} {phi_analytic:>16.6e} {rel_err:>12.4e}')
    return rel_errs


def test_consistency_with_periodic():
    """Compare open-BC vs periodic FFT-Poisson at small r (near source) —
    should give similar values near the source where image effects are
    small; should diverge at large r where periodic image effects accumulate."""
    L = 64
    sigma = 3.0
    M = 1.0
    G_N = 1.0
    rho = gaussian_mass_3d(L, M=M, sigma=sigma)
    phi_open = solve_poisson_3d_open(rho, G_N=G_N)

    # Periodic FFT-Poisson (the old solver, for comparison)
    kx = np.fft.fftfreq(L) * 2 * np.pi
    ky = np.fft.fftfreq(L) * 2 * np.pi
    kz = np.fft.fftfreq(L) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    k2 = KX**2 + KY**2 + KZ**2
    k2[0, 0, 0] = 1.0
    rho_k = np.fft.fftn(rho)
    phi_k = -4.0 * np.pi * G_N * rho_k / k2
    phi_k[0, 0, 0] = 0.0
    phi_periodic = np.fft.ifftn(phi_k).real

    cx = L // 2
    print(f'  Open vs Periodic potential (L={L}):')
    print(f'  {"r":>6} {"phi_open":>16} {"phi_periodic":>16} {"diff/open":>12}')
    for r in [5, 10, 15, 20, 25, 30]:
        po = phi_open[cx + r, cx, cx]
        pp = phi_periodic[cx + r, cx, cx]
        diff = abs(po - pp) / abs(po)
        print(f'  {r:>6} {po:>16.6e} {pp:>16.6e} {diff:>12.4e}')


if __name__ == '__main__':
    print('=' * 70)
    print('Open-boundary 3D Poisson solver — verification')
    print('=' * 70)
    print()
    print('Test 1: Far-field 1/r recovery')
    print('-' * 70)
    rel_errs = test_point_mass_far_field()
    print(f'  Max rel err (far field): {max(rel_errs):.4e}')
    print()
    print('Test 2: Open-BC vs Periodic comparison')
    print('-' * 70)
    test_consistency_with_periodic()
