"""
ca_core_exact.py  —  Exact-arccos 2D Weyl QCA (Paper 1 Eq. 16)
==============================================================
The 2D analog of `ca_bcc.py`.  Implements the *unique* non-trivial
s=2 Weyl QCA on the 2D square lattice:

  u(k)     = c_x c_y
  ñ_x(k)   = s_x c_y
  ñ_y(k)   = c_x s_y
  ñ_z(k)   = s_x s_y
  ω(k)     = arccos(c_x c_y)
  c_i      = cos(k_i / √2),   s_i = sin(k_i / √2)

Unitary U(k) = u·I − i·(σ_x ñ_x + σ_y ñ_y + σ_z ñ_z).  By construction
u² + |ñ|² = c_x²c_y² + s_x²c_y² + c_x²s_y² + s_x²s_y²
         = (c_x²+s_x²)(c_y²+s_y²) = 1.

In the small-|k| limit the dispersion reduces to ω = |k|/√2 — the 2D
Weyl Hamiltonian H_W = (1/√2) σ·k.  The lattice gives a frequency-
dependent correction at finite |k|, which is the 2D analog of Paper 4
Eq. 23's prediction Δc/c ∼ k/√d at the Planck scale.

Coexistence with the existing `weyl_step_2d_splitstep`:
  - `weyl_step_2d_splitstep` uses ω = c|k| (linear dispersion).  Exact
    only at |k|→0; for finite |k| it does not match Paper 1's QCA.
  - `weyl_step_2d_arccos_splitstep` (this file) uses the exact arccos
    dispersion.  Reduces to the linear stepper at |k|→0 by inspection.
"""

import numpy as np
import ca_fft as _fft
from ca_lattice import make_kgrid_2d as _kgrid2d


SQRT2 = np.sqrt(2.0)


def _arccos_2d_uvec(kx, ky):
    """Compute (u, n_x, n_y, n_z) per Paper 1 Eq. 16."""
    inv_root2 = 1.0 / SQRT2
    cx, cy = np.cos(kx * inv_root2), np.cos(ky * inv_root2)
    sx, sy = np.sin(kx * inv_root2), np.sin(ky * inv_root2)
    u  = cx * cy
    nx = sx * cy
    ny = cx * sy
    nz = sx * sy
    return u, nx, ny, nz


def exact2d_dispersion(kx, ky):
    """Analytic ω(k) = arccos(c_x c_y) per Paper 1 Eq. 16."""
    u, _, _, _ = _arccos_2d_uvec(kx, ky)
    return np.arccos(np.clip(u, -1.0, 1.0))


def exact2d_unitary(kx, ky):
    """The 2×2 unitary U(k); returns U_ff, U_fg, U_gf, U_gg."""
    u, nx, ny, nz = _arccos_2d_uvec(kx, ky)
    U_ff = u - 1j * nz
    U_fg = -1j * (nx - 1j * ny)
    U_gf = -1j * (nx + 1j * ny)
    U_gg = u + 1j * nz
    return U_ff, U_fg, U_gf, U_gg


def weyl_step_2d_arccos_splitstep(f, g):
    """
    Exact 2D BCC-equivalent Weyl QCA step (Paper 1 Eq. 16).

    One CA tick is one application of U(k).  Diagonal in Fourier space,
    so norm is conserved by construction.
    """
    KX, KY = _kgrid2d(*f.shape)
    U_ff, U_fg, U_gf, U_gg = exact2d_unitary(KX, KY)
    F = _fft.fft2(f)
    G = _fft.fft2(g)
    F_new = U_ff * F + U_fg * G
    G_new = U_gf * F + U_gg * G
    return _fft.ifft2(F_new), _fft.ifft2(G_new)


# ══════════════════════════════════════════════════════════════════
#  Verification utilities
# ══════════════════════════════════════════════════════════════════

def exact2d_unitarity_residual(kx, ky):
    """||U†U − I||_F per mode."""
    U_ff, U_fg, U_gf, U_gg = exact2d_unitary(kx, ky)
    a = np.conj(U_ff) * U_ff + np.conj(U_gf) * U_gf
    b = np.conj(U_ff) * U_fg + np.conj(U_gf) * U_gg
    c = np.conj(U_fg) * U_ff + np.conj(U_gg) * U_gf
    d = np.conj(U_fg) * U_fg + np.conj(U_gg) * U_gg
    return np.sqrt(np.abs(a - 1) ** 2 + np.abs(b) ** 2 +
                   np.abs(c) ** 2 + np.abs(d - 1) ** 2)


def exact2d_a0_check():
    """At k=0, U should be the identity."""
    U = exact2d_unitary(0.0, 0.0)
    return tuple(complex(np.asarray(x)) for x in U)


def exact2d_freq_dependent_c(k_mag=0.5, direction=(1.0, 1.0)):
    """
    For a chosen direction k̂, compute the group velocity |v_g(k)| at
    |k| = k_mag and return |v_g| − 1/√2 (the lattice-corrected deviation
    from the small-k speed).  Paper 4 Eq. 23 predicts a leading O(k)
    correction in 3D; in 2D the correction is O(k²) at the special
    direction (1,1) and zero at (1,0).
    """
    direction = np.asarray(direction, dtype=float)
    direction /= np.linalg.norm(direction)
    kx, ky = k_mag * direction[0], k_mag * direction[1]
    # Numerical gradient of ω with respect to (kx, ky)
    eps = 1e-5
    w0   = exact2d_dispersion(kx, ky)
    wpx  = exact2d_dispersion(kx + eps, ky)
    wmx  = exact2d_dispersion(kx - eps, ky)
    wpy  = exact2d_dispersion(kx, ky + eps)
    wmy  = exact2d_dispersion(kx, ky - eps)
    vgx = (wpx - wmx) / (2 * eps)
    vgy = (wpy - wmy) / (2 * eps)
    vmag = float(np.sqrt(vgx ** 2 + vgy ** 2))
    return vmag - 1.0 / SQRT2


def exact2d_smallk_residual(k_mag=0.01):
    """
    Compare exact dispersion to linear ω = |k|/√2 at small |k|.
    Returns max relative error over 8 directions.
    Expected O(k²).
    """
    thetas = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    errs = []
    for t in thetas:
        kx, ky = k_mag * np.cos(t), k_mag * np.sin(t)
        w_ex = float(exact2d_dispersion(kx, ky))
        w_lin = k_mag / SQRT2
        errs.append(abs(w_ex - w_lin) / w_lin)
    return max(errs)


def exact2d_norm_drift(L=32, n_steps=200, seed=0):
    """Random initial state; measure norm drift after n_steps."""
    rng = np.random.default_rng(seed)
    f = (rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))).astype(np.complex128)
    g = (rng.standard_normal((L, L)) + 1j * rng.standard_normal((L, L))).astype(np.complex128)
    n0 = float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))
    for _ in range(n_steps):
        f, g = weyl_step_2d_arccos_splitstep(f, g)
    n1 = float(np.sum(np.abs(f) ** 2 + np.abs(g) ** 2))
    return n1 / n0 - 1.0


if __name__ == '__main__':
    K = np.linspace(-np.pi * SQRT2, np.pi * SQRT2, 32, endpoint=False)
    KX, KY = np.meshgrid(K, K, indexing='ij')
    print('Unitarity max residual:', float(exact2d_unitarity_residual(KX, KY).max()))
    print('A_0 at k=0:', exact2d_a0_check())
    print('Δc/c at |k|=0.5 along (1,1):', exact2d_freq_dependent_c(0.5, (1, 1)))
    print('Δc/c at |k|=0.5 along (1,0):', exact2d_freq_dependent_c(0.5, (1, 0)))
    print('Small-|k| residual (k=0.01):', exact2d_smallk_residual(0.01))
    print('Norm drift (32×32, 200 steps):', exact2d_norm_drift())
