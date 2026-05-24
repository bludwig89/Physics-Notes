"""
ca_dirac_bcc.py  —  Dirac CA on the 3D BCC lattice  (exact-QCA form)
=====================================================================
Massive 4-component Dirac spinor in the Weyl/chiral representation on
the body-centred-cubic (BCC) 3D lattice.

State per cell: Ψ = (η_↑, η_↓, χ_↑, χ_↓) — four complex numbers.
  η = (η_↑, η_↓)   left-handed Weyl 2-spinor
  χ = (χ_↑, χ_↓)   right-handed Weyl 2-spinor

Direct 3D analog of `ca_dirac.dirac_step_2d_splitstep` (Finding 9), using
the BCC Weyl unitary of `ca_bcc.bcc_unitary` (Paper 1 Eq. 15) in place
of the 2D `ce.exact2d_unitary` (Paper 1 Eq. 16).

Single-tick unitary
-------------------

    D_k = [[ n · A_k,    im · I    ],
           [ im · I,     n · A_k†  ]],   with  n = √(1 − m²),   n² + m² = 1.

where A_k is the 3D BCC Weyl-QCA unitary (default sign '+'), A_k† its
Hermitian conjugate, m the dimensionless mass.  The off-diagonal closure
A_-^block = A_+^† is forced by unitarity of the full 4×4 D_k — the same
argument used in the 2D case (see `ca_dirac` module docstring).

Eigenvalues of D_k are e^{±iω_k}, each 2-fold degenerate, with

    ω_k = arccos( n · u(k) ),     u(k) = c_x c_y c_z + s_x s_y s_z,
                                   c_i = cos(k_i / √3),
                                   s_i = sin(k_i / √3).

This is the 3D-BCC analog of Paper 4's exact dispersion.  Small-(k, m)
expansion along an arbitrary unit direction k̂:

    u(k) ≈ 1 − |k|² / 6 + O(|k|⁴),
    cos ω ≈ n − n|k|²/6,
    ω² ≈ m² + (1 − m²) |k|² / 3 + O(|k|⁴).

reproducing the continuum-Dirac dispersion E² = m² + (c·k)² with
c_lat = 1/√3 at leading order — the lattice light speed of the BCC
Weyl QCA.

Spectral interpolation for arbitrary dt:

    U_D(k, dt) = cos(ω · dt) · I  +  (sin(ω · dt) / sin(ω)) · (D_k − cos(ω) · I).

At ω → 0 the limit (L'Hôpital) sin(ω·dt)/sin(ω) → dt and
D_k − cos(ω)·I → 0, so U_D → I bit-for-bit.  dt = 1 recovers D_k.

Observable shifts vs the 2D square-lattice Dirac:
  - Lattice light speed:  c_lat = 1/√3 (was 1/√2).
  - Zitterbewegung frequency:  ω_Z = 2·arcsin(m)   (unchanged — set by m only).
  - Continuum-SR gap at finite |k|:  scales as (v_g / c_lat)²; coefficient
    differs from 2D by the new c_lat normalisation.
"""

import numpy as np
import ca_bcc as bcc
import ca_fft as _fft          # multi-core FFT backend
from ca_lattice import make_kgrid_3d as _kgrid3d


# ══════════════════════════════════════════════════════════════════
#  Internal helpers — exact-QCA 4×4 propagator pieces
# ══════════════════════════════════════════════════════════════════

C_LAT_3D = 1.0 / np.sqrt(3.0)   # BCC Weyl-QCA lattice light speed


def _check_mass(m):
    """Validate |m| ≤ 1 (the QCA admissibility constraint n²+m²=1)."""
    if abs(float(m)) > 1.0 + 1e-15:
        raise ValueError(
            f"|m| must be ≤ 1 under the QCA admissibility constraint "
            f"n² + m² = 1 (got m = {m}).  See Finding 9 / Paper 1 Eq. 23."
        )


def _kinetic_n(m):
    """n = √(1 − m²), the kinetic-block coefficient."""
    return float(np.sqrt(max(0.0, 1.0 - m * m)))


def bcc_dirac_dispersion(KX, KY, KZ, m, sign='+'):
    """
    ω_k = arccos( n · u(k) )   on the BCC 3D lattice (Paper 1 Eq. 23 +
    Eq. 15).  Returns a real ndarray of the same shape as KX, KY, KZ.
    """
    n = _kinetic_n(m)
    u, _, _, _ = bcc._bcc_uvec(KX, KY, KZ, sign=sign)
    return np.arccos(np.clip(n * u, -1.0, 1.0))


def _bcc_weyl_blocks(KX, KY, KZ, sign='+'):
    """
    Return (A, Ap) where each is the 4-tuple (ff, fg, gf, gg) of 2×2
    BCC-Weyl-QCA unitary entries.  A is the Paper 1 Eq. 15 unitary at
    k (chosen helicity); Ap = A† is the Hermitian conjugate (the choice
    forced by unitarity of the full 4×4 D_k).

    For a 2×2 matrix [[a, b],[c, d]] the Hermitian conjugate is
    [[ā, c̄],[b̄, d̄]] — i.e. swap off-diagonals and conjugate.
    """
    A_ff, A_fg, A_gf, A_gg = bcc.bcc_unitary(KX, KY, KZ, sign=sign)
    A  = (A_ff, A_fg, A_gf, A_gg)
    Ap = (np.conj(A_ff), np.conj(A_gf), np.conj(A_fg), np.conj(A_gg))
    return A, Ap


def _apply_D_k(EU, ED, CU, CD, n, im_val, A, Ap):
    """
    Apply the single-tick D_k once in Fourier space.

      D_k = [[ n · A_k,    im · I  ],
             [ im · I,     n · A_k†]]

    on Ψ = (η_↑, η_↓, χ_↑, χ_↓).  All inputs are 3D Fourier-space arrays.
    """
    A_ff, A_fg, A_gf, A_gg = A
    Ap_ff, Ap_fg, Ap_gf, Ap_gg = Ap

    EU_new = n * A_ff * EU + n * A_fg * ED + im_val * CU
    ED_new = n * A_gf * EU + n * A_gg * ED + im_val * CD
    CU_new = im_val * EU + n * Ap_ff * CU + n * Ap_fg * CD
    CD_new = im_val * ED + n * Ap_gf * CU + n * Ap_gg * CD
    return EU_new, ED_new, CU_new, CD_new


# ══════════════════════════════════════════════════════════════════
#  Dirac propagator (3D BCC)
# ══════════════════════════════════════════════════════════════════

def dirac_step_3d_bcc_splitstep(eta_u, eta_d, chi_u, chi_d,
                                m=0.0, dt=1.0, sign='+'):
    """
    One step of the *exact-QCA* 3D BCC Dirac CA in Fourier space.

    Parameters
    ----------
    eta_u, eta_d : complex ndarrays  shape (Lx, Ly, Lz)
        Left-handed Weyl spinor components (η_↑, η_↓).
    chi_u, chi_d : complex ndarrays  shape (Lx, Ly, Lz)
        Right-handed Weyl spinor components (χ_↑, χ_↓).
    m : float
        Dimensionless mass with |m| ≤ 1.  The kinetic coefficient
        n = √(1 − m²) is derived internally (QCA admissibility, Paper 1
        Eq. 23).
    dt : float
        Time step.  dt = 1 applies D_k once.  Other values use the
        spectral interpolation U_D(dt) = cos(ω·dt)·I + sin(ω·dt)/sin(ω)
        · (D_k − cos(ω)·I) at each Fourier mode.
    sign : '+' or '-'
        Helicity choice for the BCC Weyl block (Paper 1's two
        unitarily-inequivalent solutions).

    Returns
    -------
    eta_u_new, eta_d_new, chi_u_new, chi_d_new : updated arrays
    """
    _check_mass(m)
    KX, KY, KZ = _kgrid3d(*eta_u.shape)

    n     = _kinetic_n(m)
    im_v  = 1j * m
    A, Ap = _bcc_weyl_blocks(KX, KY, KZ, sign=sign)

    EU = _fft.fftn(eta_u);  ED = _fft.fftn(eta_d)
    CU = _fft.fftn(chi_u);  CD = _fft.fftn(chi_d)

    # Apply D_k once → (D_k Ψ) in Fourier space
    DEU, DED, DCU, DCD = _apply_D_k(EU, ED, CU, CD, n, im_v, A, Ap)

    if dt == 1.0:
        EU_new, ED_new, CU_new, CD_new = DEU, DED, DCU, DCD
    else:
        omega   = bcc_dirac_dispersion(KX, KY, KZ, m, sign=sign)
        cos_w   = np.cos(omega)
        cos_wdt = np.cos(omega * dt)
        sin_w   = np.sin(omega)
        # scale = sin(ω·dt)/sin(ω);  L'Hôpital limit dt at ω → 0.
        sin_safe = np.where(sin_w == 0.0, 1.0, sin_w)
        scale    = np.sin(omega * dt) / sin_safe
        scale    = np.where(sin_w == 0.0, dt, scale)
        # U(dt) Ψ = cos(ω·dt) Ψ + scale · (D_k Ψ − cos(ω) Ψ)
        EU_new = cos_wdt * EU + scale * (DEU - cos_w * EU)
        ED_new = cos_wdt * ED + scale * (DED - cos_w * ED)
        CU_new = cos_wdt * CU + scale * (DCU - cos_w * CU)
        CD_new = cos_wdt * CD + scale * (DCD - cos_w * CD)

    return (_fft.ifftn(EU_new), _fft.ifftn(ED_new),
            _fft.ifftn(CU_new), _fft.ifftn(CD_new))


# ══════════════════════════════════════════════════════════════════
#  4×4 D_k matrix builder for analytic / eigen-decomposition use
# ══════════════════════════════════════════════════════════════════

def build_D_k_matrix(kx, ky, kz, m, sign='+'):
    """
    Build the explicit 4×4 D_k matrix at a single k-point.  Useful for
    eigen-decomposition (e.g. constructing positive-frequency eigenmodes
    in test_SR2_3D_time_dilation.py).

    Returns a (4,4) complex ndarray.
    """
    _check_mass(m)
    n = _kinetic_n(m)
    A_ff, A_fg, A_gf, A_gg = bcc.bcc_unitary(kx, ky, kz, sign=sign)
    # Wrap each scalar entry in an array → cast to complex scalar
    A = np.array([[complex(A_ff), complex(A_fg)],
                  [complex(A_gf), complex(A_gg)]], dtype=complex)
    Ad = A.conj().T

    D = np.zeros((4, 4), dtype=complex)
    D[0:2, 0:2] = n * A
    D[2:4, 2:4] = n * Ad
    D[0:2, 2:4] = 1j * m * np.eye(2)
    D[2:4, 0:2] = 1j * m * np.eye(2)
    return D


# ══════════════════════════════════════════════════════════════════
#  Verification utilities
# ══════════════════════════════════════════════════════════════════

def verify_dirac_dispersion_3d_bcc(L=16, n_modes=8, m=0.3, sign='+',
                                   seed=0):
    """
    For a set of random k-values, build D_k explicitly, diagonalise, and
    compare the principal eigenvalue phase to the analytic ω_k.

    Returns max |ω_measured − ω_analytic| across the sampled modes.
    Expected: machine precision (1e-15 ish) from numpy.linalg.eig.
    """
    rng = np.random.default_rng(seed)
    # Restrict to safely inside the BCC BZ (|k_i / √3| ≤ 0.6)
    k_max = 0.6 * np.sqrt(3.0)
    kvals = rng.uniform(-k_max, k_max, size=(n_modes, 3))

    max_err = 0.0
    for kx_v, ky_v, kz_v in kvals:
        D = build_D_k_matrix(kx_v, ky_v, kz_v, m, sign=sign)
        eigvals, _ = np.linalg.eig(D)
        # Principal-branch ω_k: phase of eigenvalue closest to e^{+iω_ana}.
        w_ana = float(bcc_dirac_dispersion(
            np.array(kx_v), np.array(ky_v), np.array(kz_v), m, sign=sign))
        target = np.exp(1j * w_ana)
        idx = int(np.argmin(np.abs(eigvals - target)))
        w_meas = float(np.angle(eigvals[idx]))
        err = abs(w_meas - w_ana)
        max_err = max(max_err, err)
    return max_err


def verify_unitarity_3d_bcc(n_modes=64, m=0.3, sign='+', seed=0):
    """
    For random k, build D_k and measure ||D†D − I||_F.  Should be at
    machine precision (~1e-15) — the unitarity closure n²+m²=1 with
    A_-^block = A_+† is exact.
    """
    rng = np.random.default_rng(seed)
    k_max = 0.6 * np.sqrt(3.0)
    kvals = rng.uniform(-k_max, k_max, size=(n_modes, 3))
    max_res = 0.0
    for kx_v, ky_v, kz_v in kvals:
        D = build_D_k_matrix(kx_v, ky_v, kz_v, m, sign=sign)
        res = D.conj().T @ D - np.eye(4)
        max_res = max(max_res, float(np.linalg.norm(res, ord='fro')))
    return max_res


def norm_drift_3d_bcc(L=16, n_steps=200, m=0.2, sign='+', seed=0,
                     dt=1.0):
    """Random 4-spinor field, run n_steps and return norm(t)/norm(0)−1."""
    rng = np.random.default_rng(seed)
    eu = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    ed = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    cu = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    cd = (rng.standard_normal((L, L, L)) +
          1j * rng.standard_normal((L, L, L))).astype(np.complex128)
    n0 = float(np.sum(np.abs(eu)**2 + np.abs(ed)**2 +
                      np.abs(cu)**2 + np.abs(cd)**2))
    for _ in range(n_steps):
        eu, ed, cu, cd = dirac_step_3d_bcc_splitstep(
            eu, ed, cu, cd, m=m, dt=dt, sign=sign)
    n1 = float(np.sum(np.abs(eu)**2 + np.abs(ed)**2 +
                      np.abs(cu)**2 + np.abs(cd)**2))
    return n1 / n0 - 1.0


if __name__ == '__main__':
    print("3D BCC Dirac CA — smoke test")
    print(f"  unitarity (64 modes, m=0.3):     "
          f"{verify_unitarity_3d_bcc():.3e}")
    print(f"  dispersion (8 modes, m=0.3):     "
          f"{verify_dirac_dispersion_3d_bcc():.3e}")
    print(f"  norm drift (16³, 200 steps, m=0.2):  "
          f"{norm_drift_3d_bcc():.3e}")
    print(f"  A_0 = I at k=0 (m=0):  "
          f"{build_D_k_matrix(0, 0, 0, 0.0)[:2, :2].diagonal()} "
          f"{build_D_k_matrix(0, 0, 0, 0.0)[2:, 2:].diagonal()}")
