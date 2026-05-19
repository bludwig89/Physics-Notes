"""
ca_dirac.py  —  Dirac CA on a flat lattice  (Phase D1) — exact-QCA form
==========================================================================
Massive 4-component Dirac spinor in the Weyl/chiral representation.

State per cell: Ψ = (η_↑, η_↓, χ_↑, χ_↓) — four complex numbers.
  η = (η_↑, η_↓)   left-handed Weyl spinor
  χ = (χ_↑, χ_↓)   right-handed Weyl spinor

Refactor (Finding 9, 2026-05-17).  This module now implements the *exact*
QCA Dirac propagator of Paper 1 Eq. 23 (single-tick unitary) combined with
the unique non-trivial 2D Weyl QCA of Paper 1 Eq. 16 (see
`ca_core_exact.exact2d_unitary`).  The previous linearized Hamiltonian
form `H_D = c·α·k + m·β` is retired; the kinetic coefficient is no longer
a free parameter — the QCA admissibility constraint n² + m² = 1 fixes
n = √(1 − m²).  The `c` argument that used to live on every stepper
signature has been removed everywhere.

Single-tick unitary

    D_k = [[ n·W_k,    im·I    ],
           [ im·I,     n·W'_k  ]]    with  n = √(1−m²),  n² + m² = 1.

where W_k is the left-chirality Weyl QCA (`exact2d_unitary` at k) and
W'_k = W_k† is the opposite-chirality block.  The W' = W† choice is
*forced* by unitarity of D_k:

    (D†D)_{12} = n W† (im I) + (−im I)(n W')  =  imn (W† − W'),

and this off-diagonal must vanish, so W' = W†.  (Finding 9 paraphrased
the QCA literature's "W_k* = W_k(−k)" statement, but element-wise complex
conjugation of the explicit 2D Eq. 16 unitary differs from the Hermitian
conjugate; the form that closes the unitarity algebra is W' = W†.)
With that choice:

    (D†D)_{11} = n² W†W + m² I = (n² + m²) I = I.

Eigenvalues of D_k are e^{±iω_k}, each 2-fold degenerate, with

    ω_k = arccos(n · c_x · c_y),       c_i = cos(k_i / √2).

This is Paper 4's exact dispersion.  Small-(k, m) expansion:

    ω_k² ≈ m² + (1 − m²)·|k|²/2,

reproducing the continuum-Dirac dispersion E² = m² + (c·k)² with the
identification c = 1/√2 (lattice unit) at leading order in k.

Spectral interpolation for arbitrary dt:

    U_D(k, dt) = cos(ω·dt)·I  +  (sin(ω·dt)/sin(ω)) · (D_k − cos(ω)·I).

At ω → 0 the limit (L'Hôpital) sin(ω·dt)/sin(ω) → dt and
D_k − cos(ω)·I → 0, so U_D → I bit-for-bit.  dt = 1 recovers D_k.

Observable shift vs the old linearized convention (Finding 9):

  - Zitterbewegung frequency:  ω_Z = 2·arcsin(m)   (was 2m).
    At m = 0.5 the new target is π/3 ≈ 1.04720 (was 1.000).
  - Dispersion at finite |k|:  ω = arccos(√(1−m²)·c_x·c_y),
    BZ-periodic, bounded by π, vs the unbounded continuum √((c·k)² + m²).
"""

import numpy as np
import ca_core_exact as ce


# ══════════════════════════════════════════════════════════════════
#  Internal helpers — exact-QCA 4×4 propagator pieces
# ══════════════════════════════════════════════════════════════════

def _check_mass(m):
    """Validate |m| ≤ 1 (the QCA admissibility constraint n²+m²=1)."""
    if abs(float(m)) > 1.0 + 1e-15:
        raise ValueError(
            f"|m| must be ≤ 1 under the QCA admissibility constraint "
            f"n² + m² = 1 (got m = {m}).  See Finding 9 / Paper 1 Eq. 23."
        )


def _kinetic_n(m):
    """n = √(1 − m²), the kinetic-block coefficient.  Used to be `c`."""
    return float(np.sqrt(max(0.0, 1.0 - m * m)))


def _dirac_dispersion(KX, KY, m):
    """
    ω_k = arccos(n · c_x · c_y) on the 2D square lattice (Paper 1 Eq. 23
    + Eq. 16).  Returns a real ndarray of the same shape as KX, KY.
    """
    n = _kinetic_n(m)
    inv_root2 = 1.0 / np.sqrt(2.0)
    cx = np.cos(KX * inv_root2)
    cy = np.cos(KY * inv_root2)
    return np.arccos(np.clip(n * cx * cy, -1.0, 1.0))


def _weyl_blocks(KX, KY):
    """
    Return (W, W_prime) where each is the 4-tuple (ff, fg, gf, gg) of
    2×2 Weyl-QCA unitary entries.  W is the Paper 1 Eq. 16 unitary at k;
    W' = W† is the Hermitian conjugate (the choice forced by unitarity
    of the full 4×4 D_k — see module docstring and Finding 9).

    For a 2×2 matrix [[a, b],[c, d]] the Hermitian conjugate is
    [[ā, c̄],[b̄, d̄]] — i.e. swap off-diagonals and conjugate.
    """
    W_ff, W_fg, W_gf, W_gg = ce.exact2d_unitary(KX, KY)
    W  = (W_ff, W_fg, W_gf, W_gg)
    Wp = (np.conj(W_ff), np.conj(W_gf), np.conj(W_fg), np.conj(W_gg))
    return W, Wp


def _apply_D_k(EU, ED, CU, CD, n, im_val, W, Wp):
    """
    Apply the single-tick D_k once in Fourier space.

      D_k = [[n·W_k,   im·I  ],
             [im·I,    n·W'_k]]

    on Ψ = (η_↑, η_↓, χ_↑, χ_↓).
    """
    W_ff, W_fg, W_gf, W_gg = W
    Wp_ff, Wp_fg, Wp_gf, Wp_gg = Wp

    EU_new = n * W_ff * EU + n * W_fg * ED + im_val * CU
    ED_new = n * W_gf * EU + n * W_gg * ED + im_val * CD
    CU_new = im_val * EU + n * Wp_ff * CU + n * Wp_fg * CD
    CD_new = im_val * ED + n * Wp_gf * CU + n * Wp_gg * CD
    return EU_new, ED_new, CU_new, CD_new


# ══════════════════════════════════════════════════════════════════
#  Dirac propagator (2D, with kz = 0)
# ══════════════════════════════════════════════════════════════════

def dirac_step_2d_splitstep(eta_u, eta_d, chi_u, chi_d, m=0.0, dt=1.0):
    """
    One step of the *exact-QCA* 2D Dirac CA in Fourier space.

    Parameters
    ----------
    eta_u, eta_d : complex ndarrays  shape (Lx, Ly)
        Left-handed Weyl spinor components (η_↑, η_↓).
    chi_u, chi_d : complex ndarrays  shape (Lx, Ly)
        Right-handed Weyl spinor components (χ_↑, χ_↓).
    m : float
        Dimensionless mass with |m| ≤ 1.  The kinetic coefficient
        n = √(1 − m²) is derived internally — n² + m² = 1 is the QCA
        admissibility constraint (Paper 1 Eq. 23).
    dt : float
        Time step.  dt = 1 applies D_k once.  Other values use the
        spectral interpolation U_D(dt) = cos(ω·dt)·I + sin(ω·dt)/sin(ω)
        · (D_k − cos(ω)·I) at each Fourier mode.

    Returns
    -------
    eta_u_new, eta_d_new, chi_u_new, chi_d_new : updated arrays
    """
    _check_mass(m)
    Lx, Ly = eta_u.shape
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')

    n     = _kinetic_n(m)
    im_v  = 1j * m
    W, Wp = _weyl_blocks(KX, KY)

    EU = np.fft.fft2(eta_u);  ED = np.fft.fft2(eta_d)
    CU = np.fft.fft2(chi_u);  CD = np.fft.fft2(chi_d)

    # Apply D_k once → (D_k Ψ) in Fourier space
    DEU, DED, DCU, DCD = _apply_D_k(EU, ED, CU, CD, n, im_v, W, Wp)

    if dt == 1.0:
        EU_new, ED_new, CU_new, CD_new = DEU, DED, DCU, DCD
    else:
        omega   = _dirac_dispersion(KX, KY, m)
        cos_w   = np.cos(omega)
        sin_w   = np.sin(omega)
        cos_wdt = np.cos(omega * dt)
        # scale = sin(ω·dt)/sin(ω);  L'Hôpital limit dt at ω → 0.
        sin_safe = np.where(sin_w == 0.0, 1.0, sin_w)
        scale    = np.sin(omega * dt) / sin_safe
        scale    = np.where(sin_w == 0.0, dt, scale)
        # U(dt) Ψ = cos(ω·dt) Ψ + scale · (D_k Ψ − cos(ω) Ψ)
        EU_new = cos_wdt * EU + scale * (DEU - cos_w * EU)
        ED_new = cos_wdt * ED + scale * (DED - cos_w * ED)
        CU_new = cos_wdt * CU + scale * (DCU - cos_w * CU)
        CD_new = cos_wdt * CD + scale * (DCD - cos_w * CD)

    return (np.fft.ifft2(EU_new), np.fft.ifft2(ED_new),
            np.fft.ifft2(CU_new), np.fft.ifft2(CD_new))


# ══════════════════════════════════════════════════════════════════
#  Initial conditions
# ══════════════════════════════════════════════════════════════════

def gaussian_dirac_2d(shape, center=None, sigma=3.0, chirality='left'):
    """
    Gaussian Dirac wave-packet initial condition.

    chirality='left'   → η_↑ = G, others 0   (pure left chirality)
    chirality='right'  → χ_↑ = G, others 0   (pure right chirality)
    chirality='mixed'  → η_↑ = χ_↑ = G/√2    (equal mix; mass will oscillate)
    """
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx // 2, Ly // 2)
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    G = np.exp(-(X**2 + Y**2) / (2.0 * sigma**2)).astype(complex)

    z = np.zeros_like(G)
    if chirality == 'left':
        return G.copy(), z.copy(), z.copy(), z.copy()
    elif chirality == 'right':
        return z.copy(), z.copy(), G.copy(), z.copy()
    else:
        return G / np.sqrt(2.0), z.copy(), G / np.sqrt(2.0), z.copy()


def dirac_norm(eta_u, eta_d, chi_u, chi_d):
    """Total probability norm of the 4-spinor field."""
    return float(np.sum(
        np.abs(eta_u)**2 + np.abs(eta_d)**2 +
        np.abs(chi_u)**2 + np.abs(chi_d)**2))


# ══════════════════════════════════════════════════════════════════
#  Dispersion verification
# ══════════════════════════════════════════════════════════════════

def _dirac_4x4_at_k(kx, ky, m):
    """Build the explicit 4×4 D_k as a dense matrix at a single scalar k."""
    n = _kinetic_n(m)
    KX = np.array([[kx]]); KY = np.array([[ky]])
    W, Wp = _weyl_blocks(KX, KY)
    W_ff, W_fg, W_gf, W_gg = (x[0, 0] for x in W)
    Wp_ff, Wp_fg, Wp_gf, Wp_gg = (x[0, 0] for x in Wp)
    im_v = 1j * m
    D = np.array([
        [n * W_ff,  n * W_fg,  im_v,      0.0      ],
        [n * W_gf,  n * W_gg,  0.0,       im_v     ],
        [im_v,      0.0,       n * Wp_ff, n * Wp_fg],
        [0.0,       im_v,      n * Wp_gf, n * Wp_gg],
    ], dtype=complex)
    return D


def _dirac_plus_eigenvector(kx, ky, m):
    """
    + ω eigenvector of D_k at the scalar wavevector (kx, ky).  In the
    Schrödinger convention D_k |ψ⟩ = e^{−iE·1} |ψ⟩, so the +ω state has
    D_k eigenvalue e^{−iω_k}.  Returns a unit-norm 4-vector.
    """
    D = _dirac_4x4_at_k(kx, ky, m)
    evals, evecs = np.linalg.eig(D)
    omega = float(_dirac_dispersion(np.array(kx), np.array(ky), m))
    target = np.exp(-1j * omega)
    idx = int(np.argmin(np.abs(evals - target)))
    v = evecs[:, idx]
    v = v / np.linalg.norm(v)
    return v


def verify_dirac_dispersion_2d(L=32, n_steps=20, m=0.3, dt=1.0,
                                k_indices=None):
    """
    Verify the exact-QCA 2D Dirac propagator reproduces the dispersion
        ω = arccos(√(1−m²)·c_x·c_y),       c_i = cos(k_i/√2)
    at machine precision (Finding 9).

    Method: build a plane-wave Ψ with the +ω eigenvector of D_k at
    wavevector k, propagate n_steps, extract per-step phase from
    ⟨Ψ_0, Ψ_N⟩ / ⟨Ψ_0, Ψ_0⟩.
    """
    if k_indices is None:
        k_indices = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 2), (1, 4)]

    xs = np.arange(L)
    X, Y = np.meshgrid(xs, xs, indexing='ij')

    results = []
    for ix, iy in k_indices:
        kx = 2.0 * np.pi * ix / L
        ky = 2.0 * np.pi * iy / L
        kappa = float(np.sqrt(kx**2 + ky**2))
        omega_analytic = float(_dirac_dispersion(
            np.array(kx), np.array(ky), m))

        psi = _dirac_plus_eigenvector(kx, ky, m)
        phase_field = np.exp(1j * (kx * X + ky * Y))

        eu0 = psi[0] * phase_field
        ed0 = psi[1] * phase_field
        cu0 = psi[2] * phase_field
        cd0 = psi[3] * phase_field

        ip0 = np.sum(np.conj(eu0)*eu0 + np.conj(ed0)*ed0 +
                     np.conj(cu0)*cu0 + np.conj(cd0)*cd0)

        eu, ed, cu, cd = eu0.copy(), ed0.copy(), cu0.copy(), cd0.copy()
        for _ in range(n_steps):
            eu, ed, cu, cd = dirac_step_2d_splitstep(
                eu, ed, cu, cd, m=m, dt=dt)

        ip = np.sum(np.conj(eu0)*eu + np.conj(ed0)*ed +
                    np.conj(cu0)*cu + np.conj(cd0)*cd) / ip0

        ratio = ip * np.exp(1j * omega_analytic * n_steps * dt)
        delta_omega = float(np.angle(ratio) / (n_steps * dt))
        omega_numeric = float(omega_analytic + delta_omega)
        residual = float(abs(delta_omega))

        results.append({
            'kx': kx, 'ky': ky, 'kappa': kappa,
            'omega_numeric':  omega_numeric,
            'omega_analytic': omega_analytic,
            'residual':       residual,
        })
    return results


def measure_zitterbewegung_freq_2d(L=64, n_steps=400, m=0.5, dt=0.5,
                                    sigma=8.0):
    """
    Initialize a pure-η (left-chirality only) Dirac wave packet and track
    the chirality imbalance ρ_η(t) − ρ_χ(t) over time.

    At each Fourier mode k, a pure-η state is split equally between the
    +ω(k) and −ω(k) eigenstates of D_k.  Their interference produces
    oscillation of the chirality population at angular frequency 2·ω(k).

    For a wide (small-k) Gaussian packet the dominant frequency is
    2·ω(k=0) = 2·arccos(n) = 2·arcsin(m) — Paper 4's exact zitterbewegung
    target (Finding 9).  This is *not* the same as the linearized 2m
    target; at m = 0.5 the new value is π/3 ≈ 1.0472 (vs old 1.0000).

    Returns
    -------
    t : array of time values
    rho_diff : array of normalized chirality imbalance ρ_η − ρ_χ over time
    freq_numeric  : float — angular frequency of the dominant FFT peak
    freq_analytic : float — 2·arcsin(m) (zero-k limit, exact-QCA target)
    """
    shape = (L, L)
    nu, nd, xu, xd = gaussian_dirac_2d(shape, sigma=sigma, chirality='left')

    rho_diff = []
    for step in range(n_steps + 1):
        n_eta = float(np.sum(np.abs(nu)**2 + np.abs(nd)**2))
        n_chi = float(np.sum(np.abs(xu)**2 + np.abs(xd)**2))
        total = n_eta + n_chi
        rho_diff.append((n_eta - n_chi) / total if total > 0 else 0.0)
        if step < n_steps:
            nu, nd, xu, xd = dirac_step_2d_splitstep(nu, nd, xu, xd,
                                                     m=m, dt=dt)

    rho_diff = np.array(rho_diff)
    t = np.arange(n_steps + 1) * dt

    sig = rho_diff - rho_diff.mean()
    fft = np.fft.fft(sig)
    freqs = np.fft.fftfreq(len(sig), d=dt) * 2.0 * np.pi
    mag = np.abs(fft)
    pos = freqs > 0
    freq_numeric  = float(freqs[pos][np.argmax(mag[pos])])
    freq_analytic = 2.0 * float(np.arcsin(m))

    return t, rho_diff, freq_numeric, freq_analytic


# ══════════════════════════════════════════════════════════════════
#  Phase E1 — U(1) electromagnetic gauge
# ══════════════════════════════════════════════════════════════════
#
# Minimal coupling:  ∂_μ → ∂_μ − iq A_μ
# On the lattice, the scalar potential A_0 appears as a per-cell phase
# factor exp(−i·q·A_0·dt) in position space, applied as a Strang-symmetric
# half-step around the (exact-QCA) kinetic propagator.  Spatial components
# of A_μ would require Peierls phases on the QCA hopping links; the
# current static-A_0 tests rely on the half-step phase only.
# ══════════════════════════════════════════════════════════════════

def dirac_step_u1_2d_splitstep(eta_u, eta_d, chi_u, chi_d,
                                A0, Ax=None, Ay=None,
                                m=0.0, q=1.0, dt=1.0):
    """
    One step of the exact-QCA Dirac CA with U(1) gauge coupling.

    A0 : real array (Lx, Ly) — scalar potential at each cell.
    Ax, Ay : optional vector potential components.  Implemented as a
             uniform phase shift placeholder only; proper Peierls phases
             on the QCA links are not yet in this stepper.

    Strang split:  half-phase(dt/2)  →  kinetic(dt)  →  half-phase(dt/2)
    """
    phase_half = np.exp(-1j * q * A0 * dt * 0.5)
    eu = eta_u * phase_half
    ed = eta_d * phase_half
    xu = chi_u * phase_half
    xd = chi_d * phase_half

    if Ax is not None or Ay is not None:
        # Placeholder for Peierls phases on the QCA hopping links.  Static
        # A_0 tests don't exercise this; left as a no-op so the API stays
        # stable for future work.
        _ = (Ax, Ay)

    eu, ed, xu, xd = dirac_step_2d_splitstep(eu, ed, xu, xd, m=m, dt=dt)

    eu = eu * phase_half
    ed = ed * phase_half
    xu = xu * phase_half
    xd = xd * phase_half

    return eu, ed, xu, xd


# ══════════════════════════════════════════════════════════════════
#  Variable-mass Dirac stepper  (Phase F prerequisite)
# ══════════════════════════════════════════════════════════════════
#
# For position-dependent mass m(x), split the full Dirac generator:
#
#     D_full(k, x; m(x)) ≈ Mix_half(δm(x))  ∘  Kinetic(m_0, dt)  ∘  Mix_half(δm(x))
#
# where  m_0 = mean(m_field)   and   δm(x) = m_field(x) − m_0.
#
# The per-cell Mix step is the exact unitary rotation  exp(−i·β·δm·dt)
# on the (η, χ) chirality sub-block.  In the exact-QCA convention the
# off-diagonal block of D_k carries `im` with *no* `c²` factor (the
# kinetic block carries n = √(1−m²)), so the per-cell Strang generator
# is the same  δm·dt  rotation as in the old linearized form — the only
# change is that the kinetic baseline now uses  n_0 = √(1−m_0²).
#
# Leading Strang error  O(m_0²·δm·dt²)  (Finding 9 item 5) — for the
# F1/F4 contracts where δm = 0 this is exactly zero, and the unified
# evolution matches a constant-m Dirac reference bit-for-bit.
# ══════════════════════════════════════════════════════════════════


def _mix_eta_chi(eu, ed, xu, xd, theta):
    """
    Per-cell rotation exp(−i·β·θ) with β = [[0,I],[I,0]].
    θ can be a scalar or per-cell array.  Real-mass version.
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    eu_n = cos_t * eu - 1j * sin_t * xu
    ed_n = cos_t * ed - 1j * sin_t * xd
    xu_n = cos_t * xu - 1j * sin_t * eu
    xd_n = cos_t * xd - 1j * sin_t * ed
    return eu_n, ed_n, xu_n, xd_n


def _mix_eta_chi_complex(eu, ed, xu, xd, m_R, m_I, factor):
    """
    Per-cell exact-unitary rotation for a *complex* mass.

    Implements   U = exp(−i·factor·[[0, M·I],[M*·I, 0]])
                with M = m_R + i·m_I (real, real ndarrays),
                     factor = dt    (scalar; no c² under the exact-QCA
                                     convention — Finding 9).

    Derivation.  The 2×2 block [[0, M],[M*, 0]] has eigenvalues ±|M|
    with eigenvectors (1, ±M*/|M|)/√2, so

        U = cos(|M|·factor)·I  −  i·(sin(|M|·factor)/|M|)·[[0, M·I],[M*·I, 0]]

    The combination sin(θ)/|M| (with θ = |M|·factor) is well-defined at
    |M|=0 via L'Hôpital (sin(θ)/θ → 1, so sin(θ)/|M| → factor).  When
    the entire mass field is zero the rotation is identity.

    Reduces to `_mix_eta_chi(theta = m_R·factor)` when m_I ≡ 0.
    """
    abs_M    = np.sqrt(m_R * m_R + m_I * m_I)
    theta    = abs_M * factor
    cos_t    = np.cos(theta)
    abs_safe = np.where(abs_M == 0.0, 1.0, abs_M)
    sinc_M   = np.sin(theta) / abs_safe
    sinc_M   = np.where(abs_M == 0.0, factor, sinc_M)
    coeff_eta = -1j * sinc_M * (m_R + 1j * m_I)    # acts on χ to update η
    coeff_chi = -1j * sinc_M * (m_R - 1j * m_I)    # acts on η to update χ
    eu_n = cos_t * eu + coeff_eta * xu
    ed_n = cos_t * ed + coeff_eta * xd
    xu_n = cos_t * xu + coeff_chi * eu
    xd_n = cos_t * xd + coeff_chi * ed
    return eu_n, ed_n, xu_n, xd_n


def dirac_step_2d_varm_splitstep(eta_u, eta_d, chi_u, chi_d,
                                  m_field, m0=None, dt=1.0):
    """
    One step of the exact-QCA Dirac CA with position-dependent (real)
    mass m(x).  Strang split:

        Mix(δm, dt/2)  →  Kinetic(m_0, dt)  →  Mix(δm, dt/2)

    where Mix is the per-cell exp(−i·β·δm·dt) rotation and the kinetic
    step is the exact-QCA propagator at the baseline mass m_0 (default
    mean(m_field)).  Each half is exactly unitary; the composition has
    O(dt²) Strang error.

    Contract.  When m_field is uniform (δm = 0), the per-cell mix is
    identity and the kinetic step matches dirac_step_2d_splitstep at
    m = m_0 bit-for-bit — F1 vacuum regression preserved.
    """
    if m0 is None:
        m0 = float(m_field.mean())
    _check_mass(m0)
    dm = m_field - m0
    theta_half = dm * dt * 0.5     # no c² (exact-QCA convention)

    eu, ed, xu, xd = _mix_eta_chi(eta_u, eta_d, chi_u, chi_d, theta_half)
    eu, ed, xu, xd = dirac_step_2d_splitstep(eu, ed, xu, xd,
                                              m=m0, dt=dt)
    eu, ed, xu, xd = _mix_eta_chi(eu, ed, xu, xd, theta_half)
    return eu, ed, xu, xd


def dirac_step_2d_varm_complex_splitstep(eta_u, eta_d, chi_u, chi_d,
                                          m_R_field, m_I_field,
                                          m0=None, dt=1.0):
    """
    Exact-QCA Dirac CA step with *complex* position-dependent mass
    M(x) = m_R(x) + i·m_I(x).

    Split as

        D_full ≈ Mix_complex(δm, dt/2)  ∘  Kinetic(m_0, dt)  ∘  Mix_complex(δm, dt/2)

    where m_0 = mean(m_R_field) is the real baseline and δm(x) =
    M(x) − m_0 is the per-cell complex residual.  The mass term in the
    exact-QCA Dirac block has coefficient `im` (no c² factor — Finding 9
    item 5), so the Mix generator is δm·dt with no c² either.

    Contracts.
      F1 — When m_R_field is uniform and m_I_field ≡ 0, δm = 0, the mix
           is identity, and the kinetic step matches the constant-m
           reference bit-for-bit.
      F4 — When the entire mass field is zero, m_0 = 0, n_0 = 1, the
           kinetic step is the exact-QCA D_k(m=0) = diag(W_k, W'_k),
           i.e. two decoupled exact-QCA Weyl propagators on η and χ.

    Parameters
    ----------
    m_R_field, m_I_field : real ndarrays, shape (Lx, Ly)
        Real and imaginary parts of the per-cell mass.  Standard-Model
        Yukawa with scalar Φ gives M(x) = y·Φ(x), so m_R = y·Re(Φ),
        m_I = y·Im(Φ).

    Returns
    -------
    eu, ed, xu, xd : updated arrays
    """
    if m0 is None:
        m0 = float(m_R_field.mean())
    _check_mass(m0)
    dm_R = m_R_field - m0
    dm_I = m_I_field
    factor_half = dt * 0.5     # no c² (exact-QCA convention)

    eu, ed, xu, xd = _mix_eta_chi_complex(eta_u, eta_d, chi_u, chi_d,
                                           dm_R, dm_I, factor_half)
    eu, ed, xu, xd = dirac_step_2d_splitstep(eu, ed, xu, xd,
                                              m=m0, dt=dt)
    eu, ed, xu, xd = _mix_eta_chi_complex(eu, ed, xu, xd,
                                           dm_R, dm_I, factor_half)
    return eu, ed, xu, xd


def aharonov_bohm_test(L=64, n_steps=100, m=0.0, q=1.0, dt=1.0,
                        flux=np.pi, sigma=6.0):
    """
    Run a Dirac plane wave through a region with a static A_0 step.

    Compares the accumulated phase pickup against the analytic prediction
    Δφ = −q · A_0 · t.  Confirms the minimal-coupling implementation under
    the exact-QCA kinetic step.
    """
    shape = (L, L)
    A0 = np.full(shape, flux / (q * n_steps * dt))   # so total phase = flux

    nu0, nd0, xu0, xd0 = gaussian_dirac_2d(shape, sigma=sigma,
                                            chirality='left')
    n_initial = dirac_norm(nu0, nd0, xu0, xd0)

    nu_a, nd_a, xu_a, xd_a = nu0.copy(), nd0.copy(), xu0.copy(), xd0.copy()
    for _ in range(n_steps):
        nu_a, nd_a, xu_a, xd_a = dirac_step_2d_splitstep(
            nu_a, nd_a, xu_a, xd_a, m=m, dt=dt)

    nu_b, nd_b, xu_b, xd_b = nu0.copy(), nd0.copy(), xu0.copy(), xd0.copy()
    for _ in range(n_steps):
        nu_b, nd_b, xu_b, xd_b = dirac_step_u1_2d_splitstep(
            nu_b, nd_b, xu_b, xd_b, A0=A0, m=m, q=q, dt=dt)

    overlap = np.sum(np.conj(nu_a) * nu_b + np.conj(nd_a) * nd_b +
                     np.conj(xu_a) * xu_b + np.conj(xd_a) * xd_b)
    overlap /= n_initial
    measured_phase = float(-np.angle(overlap))
    analytic_phase = q * A0[0, 0] * n_steps * dt

    return {
        'measured_phase': measured_phase,
        'analytic_phase': float(analytic_phase),
        'overlap_magnitude': float(np.abs(overlap)),
        'norm_with_A0': float(dirac_norm(nu_b, nd_b, xu_b, xd_b)),
        'norm_no_A0':   float(dirac_norm(nu_a, nd_a, xu_a, xd_a)),
        'initial_norm': float(n_initial),
    }
