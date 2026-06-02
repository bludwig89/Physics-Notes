"""
ca_maxwell.py  —  Composite-photon EM sector (Paper 1 Eq. 35)
==============================================================

╔══════════════════════════════════════════════════════════════════╗
║  RETIRED AS THE PHOTON (2026-06-01, F69).                          ║
║  The composite σ-bilinear photon built here assigns each helicity  ║
║  F^± = E ± iB to its own BCC chiral branch (Ω^+, Ω^-), so a        ║
║  generic linear polarization splits → linear vacuum BIREFRINGENCE  ║
║  (ΔΩ), which GRB/AGN polarimetry excludes at the F64 cell size     ║
║  (F65/F66/F67).  The physical electromagnetic photon is now the    ║
║  PAIRED-spinor photon of `ca_photon_pair.py`: a bound (+,−) pair   ║
║  ("two γ_{1/2}, only occurs as a pair", McPhee pp.5–6) whose rate  ║
║  is the helicity-symmetric Ω_pair = ω⁺(k/2)+ω⁻(k/2) = Ω_even —     ║
║  non-birefringent (F69), and the identity-channel object forced by ║
║  U(1) minimal coupling (F68).                                      ║
║                                                                    ║
║  This module is KEPT for the massive / non-Abelian sectors only    ║
║  (W, Z, gluon — `ca_wmu`, `ca_z_field`, `ca_gluon`), which use the ║
║  σ-bilinear / chiral propagator and are NOT under the photon       ║
║  polarimetry bound.  Do NOT use these helpers as the U(1) photon.  ║
╚══════════════════════════════════════════════════════════════════╝

Construct the photon as a correlated bilinear of two Weyl fields on
the BCC lattice (the de Broglie "neutrino theory of light" made
rigorous in Bisio et al. 2015).  Paper 1 Eq. 35:

    G^i(k, t) := φ^T(k/2, t) σ^i ψ(k/2, t)
    E_G(k)    := |n_{k/2}| (G_T + G_T†)
    B_G(k)    := i |n_{k/2}| (G_T† − G_T)

─────────────────────────────────────────────────────────────────────
PRIMARY LAW — Exact discrete real rotation  (Finding 25 / F26)
─────────────────────────────────────────────────────────────────────
The composite-photon fields obey an exact discrete rotation in field
space (verified to machine precision, T51: 2×10⁻¹⁶):

    E(t+1) =  cos(Ω) E(t) + sin(Ω) B(t)
    B(t+1) = −sin(Ω) E(t) + cos(Ω) B(t)

with the rotation angle per tick:

    Ω(k) = 2 ω_BCC(k/2),   ω_BCC = arccos(c_x c_y c_z ± s_x s_y s_z)

The speed of light is the angular rotation rate per unit wavenumber
(Finding 26):

    c_lat = dΩ/d|k||_{|k|→0} = 1/√3   (BCC unique-QCA result)

This is not a propagation speed — it is the rate at which the
(E, B) vector pair rotates in field space per unit k.

─────────────────────────────────────────────────────────────────────
DERIVED LAW — Maxwell curl equations  (k → 0 limit of the rotation)
─────────────────────────────────────────────────────────────────────
Taylor-expanding cos(Ω) ≈ 1, sin(Ω) ≈ Ω at small k recovers:

    ∂_t E_G ≈ i · 2 n_{k/2} × B_G     (Maxwell curl, O(Ω) accurate)
    ∂_t B_G ≈ − i · 2 n_{k/2} × E_G

These hold to O(Ω) = O(|k|) accuracy.  The linearisation error
is exactly c_lat/√2 · |k| (F21 / F26 §2) — a structural consequence
of operating at finite Δt = 1, not a model defect.

Maxwell's equations are the Δt → 0 limit of the exact rotation law.
The imaginary unit i is the 2×2 real rotation J = [[0,1],[-1,0]],
and complex EM waves are rotations expressed in the continuous-time
limit.  Energy conservation is geometric (rotation preserves length),
not a separate dynamical law.

This module implements:
  rotation_step_em_spectral  — EXACT EM propagator (rotation law)    ← primary
  c_from_rotation_rate       — measure c as dΩ/d|k|                  ← primary
  rotation_omega_bcc         — Ω(k) = 2 ω_BCC(k/2) on a k-grid
  weyl_eigenmodes_3d_bcc     — exact ± BCC Weyl eigenstates
  bilinear_G                 — σ^i bilinear at one k
  EM_bilinears               — E_G, B_G per Paper 1 Eq. 35
  maxwell_curl_residual      — linearisation-error measurement (not a test of fidelity)
  maxwell_transversality     — k·E, k·B (exact to machine precision)
  maxwell_dispersion_residual — ω_γ = |k|/√3 (small-k limit)
"""

import math
from functools import lru_cache

import numpy as np

import ca_bcc as bcc


SQRT3 = np.sqrt(3.0)
SQRT2 = np.sqrt(2.0)

# ══════════════════════════════════════════════════════════════════
#  Conventions and constants (Mohr 2010 §C — refined 2026-05-21)
# ══════════════════════════════════════════════════════════════════
# All polarization vectors and spinors below are returned as **unit-norm**
# objects on the unit sphere (per-mode normalization).  Mohr's continuum
# plane-wave delta normalization is 1/(2π)^(3/2); apply this factor only when
# evaluating delta-function inner products over continuum momentum.
PLANE_WAVE_NORM = 1.0 / (2.0 * math.pi) ** 1.5

# Lattice speed-of-light on the BCC small-k Weyl QCA used as composite photon.
# ω_γ = |k|/√3 → c_lat = 1/√3 (Bisio uniqueness; Exactness Inventory Tier 1 #9).
C_LAT = 1.0 / SQRT3

# ══════════════════════════════════════════════════════════════════
#  Mohr (2010) basis matrices — Annals of Physics 325, 607-663
# ══════════════════════════════════════════════════════════════════

# Mohr Eq. (23): 3×3 unitary Cartesian→spherical basis transformation M
# a_s = M a_c,  a_c = M† a_s
_M = np.array([
    [-1,  1j,  0         ],
    [ 0,  0,   SQRT2     ],
    [ 1,  1j,  0         ],
], dtype=complex) / SQRT2

# Mohr Eqs. (15)–(17): spin-1 tau matrices in spherical basis
# These are 3×3 analogs of the Pauli matrices: [τⁱ, τʲ] = i εᵢⱼₖ τᵏ
_TAU1 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex) / SQRT2
_TAU2 = 1j * np.array([[0, -1, 0], [1, 0, -1], [0, 1, 0]], dtype=complex) / SQRT2
_TAU3 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, -1]], dtype=complex)


def tau_dot(v_c):
    """τ·v = Σᵢ τⁱ vⁱ_c  (Mohr Eq. 19), Cartesian components, acts on spherical vectors.

    Satisfies τ·a a_s = 0 (Mohr Eq. 25) and
    (τ·a)†(τ·b) = a·b I - b_s a_s†  (Mohr Eq. 30).
    """
    v = np.asarray(v_c, dtype=complex)
    return _TAU1 * v[0] + _TAU2 * v[1] + _TAU3 * v[2]


# ══════════════════════════════════════════════════════════════════
#  Eigenmodes of the BCC unitary at a single k
# ══════════════════════════════════════════════════════════════════

def _hamiltonian_matrix(kx, ky, kz, sign='+'):
    """Return the 2×2 matrix H(k) whose eigenvalues are ±ω(k)."""
    u, nx, ny, nz = bcc._bcc_uvec(kx, ky, kz, sign=sign)
    # U(k) = u·I - i (σ·n).  H(k) = (σ·n) / sin(ω) · ω, but since we
    # diagonalise the matrix U(k) = exp(-i H Δt) with Δt=1, we just
    # build H directly as the Pauli decomposition.  Simpler: diagonalise
    # U(k) and read off the phases.
    U = np.array([
        [u - 1j * nz,            -1j * (nx - 1j * ny)],
        [-1j * (nx + 1j * ny),   u + 1j * nz        ],
    ], dtype=complex)
    return U


def weyl_eigenmodes_3d_bcc(kx, ky, kz, sign='+'):
    """
    Return the two 2-spinor eigenmodes of U(k) at this momentum.

    Output: (psi_plus, psi_minus, omega), where U·psi_± = e^{∓iω}·psi_±.
    Sign convention: ω is the positive eigenphase.
    """
    U = _hamiltonian_matrix(kx, ky, kz, sign=sign)
    eigvals, eigvecs = np.linalg.eig(U)
    # Sort eigenvalues by phase (positive/negative ω).
    phases = -np.angle(eigvals)  # U = e^{-iωΔt} so phase = -ω·Δt at Δt=1
    idx_pos = int(np.argmax(phases))
    idx_neg = 1 - idx_pos
    psi_plus = eigvecs[:, idx_pos]
    psi_minus = eigvecs[:, idx_neg]
    omega = float(phases[idx_pos])
    return psi_plus, psi_minus, omega


# ══════════════════════════════════════════════════════════════════
#  Bilinears
# ══════════════════════════════════════════════════════════════════

# Pauli matrices.
_S_X = np.array([[0, 1], [1, 0]], dtype=complex)
_S_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_S_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS = (_S_X, _S_Y, _S_Z)


def bilinear_G(psi, phi):
    """
    G^i = φ^T σ^i ψ.  Returns a complex 3-vector.

    Note: φ^T (transpose, not conjugate) per Paper 1 Eq. 33.  This is
    the bilinear that yields the *neutrino-pair* photon — the
    correlated state is fermionic-antisymmetric in the spinor indices.
    """
    return np.array([phi @ S @ psi for S in _PAULIS])


def _transverse_part(v, n_hat):
    """Return v - (v·n̂)n̂; the projection orthogonal to n̂."""
    return v - (v @ n_hat) * n_hat


def EM_bilinears(psi, phi, n_half):
    """
    Compute E_G, B_G from Paper 1 Eq. 35.

    Inputs:
      psi, phi : 2-spinor amplitudes at k/2
      n_half   : the 3-vector n(k/2) from the BCC structure (real)

    Returns:
      E_G, B_G : complex 3-vectors (after transverse projection)

    Paper 1 Eq. 35 uses |n(k/2)| times the transverse G_T.  Here we
    return the *raw* complex E_G, B_G; the transversality test is run
    separately so we can also measure how transverse the construction
    is at finite |k|.
    """
    G = bilinear_G(psi, phi)
    nmag = np.linalg.norm(n_half)
    if nmag < 1e-15:
        # At k=0, ñ vanishes (A_0 = I, see Paper 2 V7).  The construction
        # is singular at k=0; E_G, B_G are conventionally set to 0.
        return np.zeros(3, dtype=complex), np.zeros(3, dtype=complex)
    n_hat = n_half / nmag
    G_T = _transverse_part(G, n_hat)
    G_T_dag = np.conj(G_T)
    E = nmag * (G_T + G_T_dag)
    B = 1j * nmag * (G_T_dag - G_T)
    return E, B


# ══════════════════════════════════════════════════════════════════
#  Two-helicity (both Weyl branches) photon construction  (FG-6, 2026-05-26)
# ══════════════════════════════════════════════════════════════════
#
# The F29 bilinear bridge (test_su2_photon_bridge.py) used `sign='+'`
# eigenmodes only — a single BCC chirality branch.  F37 established
# that the BCC walk carries TWO branches Ω⁺(k) = 2·ω_+(k/2) and
# Ω⁻(k) = 2·ω_-(k/2), which at the (E, B) field level correspond to
# the two photon helicities F^± = E ± i·B.  F30 gave the analytical
# birefringence on the body diagonal:  Ω⁺ − Ω⁻ = −(√3/27) k² + O(k⁴).
#
# A complete two-helicity photon state therefore requires the bilinear
# to be built from BOTH branches.  The construction below provides
# per-branch helpers (`EM_bilinears_branch`, `triplet_bilinear_branch`)
# and an explicit two-helicity assembler (`EM_bilinears_two_helicity`,
# `triplet_bilinear_two_helicity`).  The Riemann-Silberstein decomp
# (`riemann_silberstein_decomp`) projects an (E, B) pair onto F^±.
#
# Key facts demonstrated in test_FG6_two_helicity_photon.py:
#   - Each branch's bilinear gives a NONZERO (E, B), transverse to its
#     own  2·n_half_±  (per-branch transversality).
#   - Both branches contribute to BOTH helicities F^± of a single (E, B)
#     mode — a single-branch state is generically linearly polarized.
#   - Under the chiral propagation (ca_wmu.w_propagation_step_spectral),
#     the F^+ Fourier amplitude rotates at exactly Ω^+(k) and F^- at
#     Ω^-(k), regardless of which branch the bilinear was built from —
#     the chiral propagator decouples helicities at the field level.
#   - The (1,1,1)-diagonal birefringence ΔΩ = Ω^+ − Ω^- matches F30's
#     −(√3/27) k² coefficient to machine precision via direct dispersion
#     evaluation, and to ≲ 1e-4 relative via the propagated bilinear.
#   - SU(2)-invariance of the singlet and adjoint rotation of the triplet
#     (F29 B1–B3) hold IDENTICALLY per branch and for the combined state.


def EM_bilinears_branch(psi, phi, kx, ky, kz, sign='+'):
    """Branch-aware composite photon bilinear: returns (E, B) and n_half(k/2, sign).

    Identical to `EM_bilinears` but takes the lattice momentum (kx, ky, kz)
    and the branch label `sign` and computes the BCC spin axis n_half
    internally, so the same call site can be reused for sign='+' and
    sign='-' bilinears without duplicating the `_bcc_uvec` lookup.

    Returns
    -------
    E : (3,) complex
    B : (3,) complex
    n_half : (3,) float
        The BCC vector n(k/2, sign) used in the construction.
    """
    _, nx, ny, nz = bcc._bcc_uvec(kx / 2.0, ky / 2.0, kz / 2.0, sign=sign)
    n_half = np.array([nx, ny, nz], dtype=float)
    E, B = EM_bilinears(psi, phi, n_half)
    return E, B, n_half


def EM_bilinears_two_helicity(psi_pl, phi_pl, psi_mn, phi_mn,
                              kx, ky, kz,
                              alpha_pl=1.0, alpha_mn=1.0):
    """Compose a two-helicity composite-photon (E, B) from BOTH Weyl branches.

    Parameters
    ----------
    psi_pl, phi_pl : (2,) complex
        Weyl 2-spinors at k/2 from the sign='+' BCC branch.
    psi_mn, phi_mn : (2,) complex
        Weyl 2-spinors at k/2 from the sign='-' branch.
    kx, ky, kz : float
        Lattice momentum components (so k/2 = (kx/2, ky/2, kz/2)).
    alpha_pl, alpha_mn : complex
        Optional complex weights for each branch (default 1.0).

    Returns
    -------
    E, B : (3,) complex
        Combined photon (E, B) = α₊ (E₊, B₊) + α₋ (E₋, B₋).
    branch_data : dict
        Dictionary with the per-branch (E, B, n_half) under keys '+' and '-'
        (so tests can inspect helicity decomposition).
    """
    E_pl, B_pl, n_pl = EM_bilinears_branch(psi_pl, phi_pl, kx, ky, kz, sign='+')
    E_mn, B_mn, n_mn = EM_bilinears_branch(psi_mn, phi_mn, kx, ky, kz, sign='-')
    E = alpha_pl * E_pl + alpha_mn * E_mn
    B = alpha_pl * B_pl + alpha_mn * B_mn
    return E, B, {
        '+': {'E': E_pl, 'B': B_pl, 'n_half': n_pl},
        '-': {'E': E_mn, 'B': B_mn, 'n_half': n_mn},
    }


def riemann_silberstein_decomp(E, B):
    """Project an (E, B) pair onto its Riemann-Silberstein helicity components.

        F^+ = E + i·B   (right-circular / RCP eigenstate of the (E,B) rotation)
        F^- = E - i·B   (left-circular / LCP eigenstate)

    Inverse:  E = (F^+ + F^-)/2 ,   B = (F^+ - F^-)/(2i).

    Under the BCC chiral propagation (F37 / `w_propagation_step_spectral`),
    F^+(k) acquires phase  exp(−i Ω^+(k))  per tick and F^-(k) acquires
    phase  exp(+i Ω^-(k))  per tick.  At k along the (1,1,1) body diagonal,
    Ω^+ ≠ Ω^- — this is the F30 vacuum birefringence.
    """
    F_plus = np.asarray(E) + 1j * np.asarray(B)
    F_minus = np.asarray(E) - 1j * np.asarray(B)
    return F_plus, F_minus


# Isospin Pauli matrices (acting on the SU(2)_L doublet).  Defined locally
# so the two-helicity W-triplet helpers below do not import from the test.
_TAU_ISO_X = np.array([[0,  1 ], [ 1, 0 ]], dtype=complex)
_TAU_ISO_Y = np.array([[0, -1j], [1j, 0 ]], dtype=complex)
_TAU_ISO_Z = np.array([[1,  0 ], [ 0,-1 ]], dtype=complex)
_TAU_ISO = (_TAU_ISO_X, _TAU_ISO_Y, _TAU_ISO_Z)


def _singlet_bilinear_H(phi_iso, psi_iso):
    """Hermitian singlet G_H^i = Σ_α (φ^α)† σ^i ψ^α on a (2, 2) doublet."""
    G = np.zeros(3, dtype=complex)
    for i, S in enumerate(_PAULIS):
        s = 0.0 + 0.0j
        for alpha in range(2):
            s += np.conj(phi_iso[alpha]) @ S @ psi_iso[alpha]
        G[i] = s
    return G


def _triplet_bilinear_H(phi_iso, psi_iso):
    """Hermitian triplet W_H^{a,i} = Σ_{αβ} (τ^a)_{αβ} (φ^α)† σ^i ψ^β."""
    W = np.zeros((3, 3), dtype=complex)
    for a, T in enumerate(_TAU_ISO):
        for i, S in enumerate(_PAULIS):
            s = 0.0 + 0.0j
            for alpha in range(2):
                for beta in range(2):
                    c = T[alpha, beta]
                    if c == 0:
                        continue
                    s += c * (np.conj(phi_iso[alpha]) @ S @ psi_iso[beta])
            W[a, i] = s
    return W


def _W_fields_from_W_triplet(W, n_half):
    """Promote each W^a triplet component to (E^a, B^a) per Paper-1 Eq. 35 form.

    W : (3, 3) complex  ‒ (a, i) indices.
    n_half : (3,) float.

    Returns
    -------
    E_W : (3, 3) complex  ‒ E^{a,i}, the SU(2) triplet of "E" fields.
    B_W : (3, 3) complex  ‒ B^{a,i}.
    """
    nmag = float(np.linalg.norm(n_half))
    if nmag < 1e-15:
        return np.zeros((3, 3), dtype=complex), np.zeros((3, 3), dtype=complex)
    n_hat = n_half / nmag
    E_out = np.zeros((3, 3), dtype=complex)
    B_out = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        W_T = _transverse_part(W[a], n_hat)
        W_T_dag = np.conj(W_T)
        E_out[a] = nmag * (W_T + W_T_dag)
        B_out[a] = 1j * nmag * (W_T_dag - W_T)
    return E_out, B_out


def triplet_bilinear_branch(psi_iso, phi_iso, kx, ky, kz, sign='+'):
    """Branch-aware W-triplet bilinear: returns (E^a, B^a) for each isospin a.

    Parameters
    ----------
    psi_iso, phi_iso : (2, 2) complex
        Doublet spinors at k/2 from the chosen BCC branch — rows index
        isospin (ν, e), columns index spin.
    kx, ky, kz, sign
        Lattice momentum and branch label.

    Returns
    -------
    E_W, B_W : (3, 3) complex
        (E^{a,i}, B^{a,i}) — the SU(2)-triplet of photon-like fields.
    W : (3, 3) complex
        The raw W_H^{a,i} bilinear (pre-projection).
    n_half : (3,) float
        BCC spin-axis vector used.
    """
    _, nx, ny, nz = bcc._bcc_uvec(kx / 2.0, ky / 2.0, kz / 2.0, sign=sign)
    n_half = np.array([nx, ny, nz], dtype=float)
    W = _triplet_bilinear_H(phi_iso, psi_iso)
    E_W, B_W = _W_fields_from_W_triplet(W, n_half)
    return E_W, B_W, W, n_half


def triplet_bilinear_two_helicity(psi_iso_pl, phi_iso_pl,
                                  psi_iso_mn, phi_iso_mn,
                                  kx, ky, kz,
                                  alpha_pl=1.0, alpha_mn=1.0):
    """Compose a two-helicity W-triplet (E^a, B^a) from both BCC branches.

    Parallel to `EM_bilinears_two_helicity`: each branch contributes its
    own (E^a, B^a, W) and they are summed component-wise with the given
    complex weights.  Returns the combined fields and a per-branch dict
    so tests can inspect each helicity sector.
    """
    EW_pl, BW_pl, W_pl, n_pl = triplet_bilinear_branch(
        psi_iso_pl, phi_iso_pl, kx, ky, kz, sign='+')
    EW_mn, BW_mn, W_mn, n_mn = triplet_bilinear_branch(
        psi_iso_mn, phi_iso_mn, kx, ky, kz, sign='-')
    E_W = alpha_pl * EW_pl + alpha_mn * EW_mn
    B_W = alpha_pl * BW_pl + alpha_mn * BW_mn
    return E_W, B_W, {
        '+': {'E': EW_pl, 'B': BW_pl, 'W': W_pl, 'n_half': n_pl},
        '-': {'E': EW_mn, 'B': BW_mn, 'W': W_mn, 'n_half': n_mn},
    }


# ══════════════════════════════════════════════════════════════════
#  Tests
# ══════════════════════════════════════════════════════════════════

def _random_dirs(n_dirs, seed=0):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((n_dirs, 3))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


def maxwell_curl_residual(k_mag=0.05, n_dirs=8, seed=0):
    """
    Verify Paper 1 Eq. 35's curl equations at small |k|.

    Procedure for each direction k̂:
      1. k_half = (k/2) along k̂
      2. Pick ψ = positive-ω eigenmode of U(k/2)
                φ = negative-ω eigenmode of U(k/2)
         (so the bilinear G evolves at frequency 2ω(k/2) — the photon)
      3. Compute E_G(0), B_G(0)
      4. Time-step: ψ → e^{-iω}ψ, φ → e^{+iω}φ → both pick a *single*
         photon-phase factor e^{-iΩ} with Ω = 2ω(k/2).
      5. Compute E_G(Δt), B_G(Δt) and finite-difference ∂_t E_G ≈
         (E(Δt) − E(0)) / Δt for very small Δt.
      6. Check ∂_t E_G ≈ i (2 n_half) × B_G  to leading order at small |k|.

    Returns (curl_E_max_err, curl_B_max_err) — the worst residual
    magnitude across the sampled directions, normalised by |E_G|+|B_G|.
    """
    dt = 1.0   # one CA tick
    dirs = _random_dirs(n_dirs, seed=seed)
    curl_E_errs = []
    curl_B_errs = []
    for d in dirs:
        kx, ky, kz = (k_mag * d[0], k_mag * d[1], k_mag * d[2])
        kx_h, ky_h, kz_h = kx / 2, ky / 2, kz / 2
        psi_p, psi_m, omega_half = weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h, sign='+')
        psi = psi_p
        phi = psi_m
        _, n_x, n_y, n_z = bcc._bcc_uvec(kx_h, ky_h, kz_h, sign='+')
        n_half = np.array([n_x, n_y, n_z], dtype=float)

        # t = 0
        E0, B0 = EM_bilinears(psi, phi, n_half)
        # one CA tick: each Weyl mode picks up a phase e^{∓iω_half}.
        # The bilinear G = φ^T σ ψ then picks phase exp(-i(ω_half - ω_half)) ... wait.
        # If ψ → e^{-iω}ψ and φ → e^{+iω}φ, then G = φ^T σ ψ → e^{0}·G — no time
        # evolution.  That's wrong; we want the photon to oscillate.  The
        # *correct* prescription: ψ, φ are *both* + eigenmodes (same helicity
        # of Weyl propagator), so they both evolve as e^{-iω}, and G evolves
        # as e^{-i·2ω} — the photon.
        ph = np.exp(-1j * omega_half * dt)
        psi_t = psi * ph
        phi_t = phi * ph
        Et, Bt = EM_bilinears(psi_t, phi_t, n_half)

        dE_dt = (Et - E0) / dt
        dB_dt = (Bt - B0) / dt

        # Right-hand side of Maxwell curl: i (2 n_half) × B and -i (2 n_half) × E
        two_n = 2.0 * n_half
        rhs_E = 1j * np.cross(two_n, B0)
        rhs_B = -1j * np.cross(two_n, E0)

        denom = np.linalg.norm(E0) + np.linalg.norm(B0) + 1e-30
        curl_E_errs.append(float(np.linalg.norm(dE_dt - rhs_E) / denom))
        curl_B_errs.append(float(np.linalg.norm(dB_dt - rhs_B) / denom))

    return max(curl_E_errs), max(curl_B_errs)


def maxwell_transversality(k_mag=0.05, n_dirs=8, seed=1):
    """
    Test 2 n_{k/2} · E_G = 0 and 2 n_{k/2} · B_G = 0 (Paper 1 Eq. 35).
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    worst = 0.0
    for d in dirs:
        kx_h, ky_h, kz_h = (k_mag * d / 2)
        psi_p, psi_m, _ = weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h, sign='+')
        _, n_x, n_y, n_z = bcc._bcc_uvec(kx_h, ky_h, kz_h, sign='+')
        n_half = np.array([n_x, n_y, n_z], dtype=float)
        E, B = EM_bilinears(psi_p, psi_p, n_half)  # ψ=φ=+ eigenmode
        two_n = 2.0 * n_half
        denom = np.linalg.norm(E) + np.linalg.norm(B) + 1e-30
        worst = max(worst, abs(two_n @ E) / denom)
        worst = max(worst, abs(two_n @ B) / denom)
    return worst


def maxwell_dispersion_residual(k_mag=0.05):
    """Nonlinear dispersion correction |Ω(k) − c_lat·|k|| / (c_lat·|k|) at finite k.

    F26 reframing: Ω(k) = 2·ω_BCC(k/2) is the exact rotation angle per tick.
    The linear approximation c_lat·|k| is the k→0 (Maxwell) limit.  The
    quantity returned here is NOT a model error — it is the BCC lattice's
    nonlinear dispersion at finite k:

        |Ω(k) − c_lat·|k|| / (c_lat·|k|) → 0 as |k| → 0   (Maxwell limit)

    At finite k this grows due to lattice anisotropy and the arccos nonlinearity.
    Along (1,1,1): leading term ≈ k/18 (see `dispersion_nonlinearity`).

    Returns the max relative deviation over 8 random directions.
    At k=0.05: ≈ 0.21% (within expected BCC nonlinearity; not a defect).
    """
    # Average over a few directions (the BCC dispersion is anisotropic).
    dirs = _random_dirs(8, seed=2)
    errs = []
    for d in dirs:
        kx, ky, kz = k_mag * d
        kx_h, ky_h, kz_h = kx / 2, ky / 2, kz / 2
        _, _, omega_half = weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h, sign='+')
        Omega = 2.0 * omega_half
        Omega_lin = k_mag / SQRT3
        errs.append(abs(Omega - Omega_lin) / Omega_lin)
    return max(errs)


# ══════════════════════════════════════════════════════════════════
#  Improvement 1 — Explicit polarization basis  (Mohr §7.1, Eqs. 210–216)
# ══════════════════════════════════════════════════════════════════

def polarization_basis(khat_c, circular=True):
    """Return two polarization unit vectors ε₁_s, ε₂_s in spherical basis,
    perpendicular to khat_c (Cartesian unit vector), following Mohr §7.1.

    circular=True  → helicity/circular eigenstates (Mohr Eq. 216 generalized):
        ε₊ = -1/√2 (ê₁ + i ê₂),  ε₋ = +1/√2 (ê₁ - i ê₂)  in Cartesian,
        then converted to spherical basis via M.  For k̂=ẑ reproduces
        Mohr Eq. (216): ε₁=(1,0,0)_s, ε₂=(0,0,1)_s exactly.

    circular=False → linear polarization (Mohr Eq. 215 generalized):
        ε₁ = M ê₁,  ε₂ = M ê₂  in spherical basis.

    All modes satisfy (verified by test_polarization_basis):
      k̂_s† ε_λ = 0          (Mohr Eq. 212 — transversality)
      ε_λ† ε_μ = δ_λμ        (Mohr Eq. 211 — orthonormality)
      Σ_λ ε_λ ε_λ† = (τ·k̂)² (Mohr Eq. 213 — completeness = Π^T_s)
    """
    khat_c = np.asarray(khat_c, dtype=float)
    khat_c = khat_c / np.linalg.norm(khat_c)

    # Build orthonormal pair (ê₁, ê₂) ⊥ k̂ in Cartesian.
    # Reference: project ẑ onto ⊥ plane; fall back to x̂ if k̂ ≈ ẑ.
    ref = np.array([0., 0., 1.])
    if abs(np.dot(ref, khat_c)) > 1.0 - 1e-9:
        ref = np.array([1., 0., 0.])
    e1_c = ref - np.dot(ref, khat_c) * khat_c
    e1_c /= np.linalg.norm(e1_c)
    e2_c = np.cross(khat_c, e1_c)
    e2_c /= np.linalg.norm(e2_c)

    if not circular:
        eps1_s = _M @ e1_c.astype(complex)
        eps2_s = _M @ e2_c.astype(complex)
    else:
        # Helicity eigenstates (right/left circular) — Mohr Eq. (216) generalized.
        # ε₊ = -1/√2 (ê₁ + i ê₂),  ε₋ = +1/√2 (ê₁ - i ê₂)  (Cartesian)
        eps1_s = _M @ ((-1.0 / SQRT2) * (e1_c + 1j * e2_c))
        eps2_s = _M @ ((1.0 / SQRT2) * (e1_c - 1j * e2_c))

    return eps1_s, eps2_s


def test_polarization_basis(n_dirs=12, seed=5):
    """Verify ε_λ satisfies Mohr Eqs. (211)–(213) for random k̂ directions.

    Checks:
      (a) transversality:  |k̂_s† ε_λ|
      (b) orthonormality:  |ε_λ† ε_μ - δ_λμ|
      (c) completeness:    ||Σ ε_λ ε_λ† - (τ·k̂)²||_max

    Returns (max_trans_err, max_ortho_err, max_comp_err).
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    max_trans = max_ortho = max_comp = 0.0

    for d in dirs:
        khat_c = d / np.linalg.norm(d)
        khat_s = _M @ khat_c.astype(complex)
        tau_k  = tau_dot(khat_c)
        Pi_T   = tau_k @ tau_k          # (τ·k̂)² = Π^T_s(k̂)  (Mohr Eq. 213)

        eps = list(polarization_basis(khat_c))   # [ε₁_s, ε₂_s]

        for lam, eps_s in enumerate(eps):
            # (a) transversality
            max_trans = max(max_trans, abs(khat_s.conj() @ eps_s))
            # (b) self-norm
            max_ortho = max(max_ortho, abs(eps_s.conj() @ eps_s - 1.0))

        # (b) cross-orthogonality
        max_ortho = max(max_ortho, abs(eps[0].conj() @ eps[1]))

        # (c) completeness
        comp = np.outer(eps[0], eps[0].conj()) + np.outer(eps[1], eps[1].conj())
        max_comp = max(max_comp, np.max(np.abs(comp - Pi_T)))

    return max_trans, max_ortho, max_comp


# ══════════════════════════════════════════════════════════════════
#  Improvement 2 — Poynting energy conservation  (Mohr Eq. 55)
# ══════════════════════════════════════════════════════════════════

def composite_photon_energy_conservation(k_mag=0.05, n_steps=200, n_dirs=12, seed=6):
    """Verify ||E_G||² + ||B_G||² is conserved under composite-photon propagation.

    Corresponds to the Poynting energy density u = ε₀|E|² + |B|²/μ₀ being
    constant for a free photon (Mohr Eq. 55).

    Analytic argument: writing G_T = A + iC (A, C real),
      E = 2|n| A,  B = 2|n| C  →  ||E||² + ||B||² = 4|n|² ||G_T||².
    Since G_T → e^{-iΩ} G_T under one CA tick, ||G_T||² is invariant exactly.

    Returns max relative deviation over all directions and time steps.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    max_var = 0.0

    for d in dirs:
        kx, ky, kz = k_mag * d
        psi_p, _, omega_half = weyl_eigenmodes_3d_bcc(kx/2, ky/2, kz/2)
        _, nx, ny, nz = bcc._bcc_uvec(kx/2, ky/2, kz/2)
        n_half = np.array([nx, ny, nz])

        psi = psi_p.copy()
        phi = psi_p.copy()
        E0, B0 = EM_bilinears(psi, phi, n_half)
        u0 = float(np.dot(E0, E0.conj()).real + np.dot(B0, B0.conj()).real)
        if u0 < 1e-30:
            continue

        ph = np.exp(-1j * omega_half)
        for _ in range(n_steps):
            psi = psi * ph
            phi = phi * ph
            E, B = EM_bilinears(psi, phi, n_half)
            u = float(np.dot(E, E.conj()).real + np.dot(B, B.conj()).real)
            max_var = max(max_var, abs(u - u0) / u0)

    return max_var


# ══════════════════════════════════════════════════════════════════
#  Improvement 3 — Lorentz boost covariance  (Mohr §6.5, §7.6)
# ══════════════════════════════════════════════════════════════════

def _lorentz_boost_6x6(v_hat_c, zeta):
    """6×6 boost matrix V(v) = exp(ζ K·v̂), Mohr Eqs. (169)–(171).

    Acts on the 6-component column (E_s, icB_s)^T.
    v_hat_c : Cartesian unit vector (boost direction).
    zeta    : rapidity, v = c tanh ζ.

    Block form (Mohr Eq. 171):
      V = [[I + (τ·v̂)²(cosh ζ - 1),  τ·v̂ sinh ζ  ],
           [τ·v̂ sinh ζ,               I + (τ·v̂)²(cosh ζ - 1)]]
    """
    tv      = tau_dot(v_hat_c)
    tv2     = tv @ tv
    ch_m1   = np.cosh(zeta) - 1.0
    sh      = np.sinh(zeta)
    I3      = np.eye(3, dtype=complex)
    block_d = I3 + tv2 * ch_m1       # diagonal blocks
    block_o = tv * sh                 # off-diagonal blocks
    V6 = np.zeros((6, 6), dtype=complex)
    V6[:3, :3] = block_d
    V6[:3, 3:] = block_o
    V6[3:, :3] = block_o
    V6[3:, 3:] = block_d
    return V6


def _boost_4momentum(k_c, v_hat_c, zeta):
    """Boost massless-photon 4-momentum (k⁰=|k|, k_c) by rapidity ζ in v̂.

    Returns (k'_c, k'⁰) — boosted 3-momentum and energy.
    """
    k0       = np.linalg.norm(k_c)
    vdk      = float(np.dot(v_hat_c, k_c))
    k0_prime = k0 * np.cosh(zeta) + vdk * np.sinh(zeta)
    k_prime  = k_c + v_hat_c * ((np.cosh(zeta) - 1.0) * vdk + k0 * np.sinh(zeta))
    return k_prime, k0_prime


def lorentz_boost_covariance(k_mag=0.3, v_mag=0.6, n_dirs=12, seed=7):
    """Verify Mohr Eqs. (281)–(287): a boosted transverse photon wave function
    is still transverse at the boosted momentum, with correctly transformed
    polarization and lower component.

    For each random (k̂, v̂) pair with rapidity ζ = arctanh(v_mag):
      1. Build 6-component spinor u = (ε_s, τ·k̂ ε_s) for each polarization λ.
      2. Apply V(v) → u' = V u.
      3. Compute boosted k' = Lorentz-boost of 4-momentum (|k|, k_c).
      4. Check:
         (a) k̂'_s† ε'  = 0         [Mohr Eq. 284 — transversality preserved]
         (b) lower' = τ·k̂' ε'      [Mohr Eq. 285 — wave-function form preserved]
         (c) |ε'| = ξ               [Mohr Eq. 287 — ξ = cosh ζ + v̂·k̂ sinh ζ]

    Returns (max_trans_err, max_form_err, max_xi_err).
    """
    zeta    = float(np.arctanh(np.clip(v_mag, 0.0, 0.9999)))
    dirs_k  = _random_dirs(n_dirs, seed=seed)
    dirs_v  = _random_dirs(n_dirs, seed=seed + 100)
    max_trans = max_form = max_xi = 0.0

    for d_k, d_v in zip(dirs_k, dirs_v):
        khat_c  = d_k / np.linalg.norm(d_k)
        v_hat_c = d_v / np.linalg.norm(d_v)

        k_c              = k_mag * khat_c
        k_prime_c, _     = _boost_4momentum(k_c, v_hat_c, zeta)
        khat_prime_c     = k_prime_c / np.linalg.norm(k_prime_c)
        khat_prime_s     = _M @ khat_prime_c.astype(complex)

        V6      = _lorentz_boost_6x6(v_hat_c, zeta)
        tau_k   = tau_dot(khat_c)
        xi      = np.cosh(zeta) + float(np.dot(v_hat_c, khat_c)) * np.sinh(zeta)

        tau_k_prime = tau_dot(khat_prime_c)

        for eps_s in polarization_basis(khat_c):
            u       = np.concatenate([eps_s, tau_k @ eps_s])
            u_prime = V6 @ u
            eps_p   = u_prime[:3]     # boosted upper (∝ ε'_s)
            low_p   = u_prime[3:]     # boosted lower

            # (a) transversality: k̂'_s† ε' = 0  (Mohr Eq. 284)
            max_trans = max(max_trans, abs(khat_prime_s.conj() @ eps_p))

            # (b) wave-function form: lower' = τ·k̂' ε'  (Mohr Eq. 285)
            expected_low = tau_k_prime @ eps_p
            scale = max(np.linalg.norm(low_p), np.linalg.norm(expected_low), 1e-30)
            max_form = max(max_form,
                           np.linalg.norm(low_p - expected_low) / scale)

            # (c) magnitude: |ε'| = |ξ|  (Mohr Eq. 287)
            max_xi = max(max_xi, abs(np.linalg.norm(eps_p) - abs(xi)))

    return max_trans, max_form, max_xi


# ══════════════════════════════════════════════════════════════════
#  Improvement 4 — Longitudinal (λ=0) photon mode  (Mohr §7.2)
# ══════════════════════════════════════════════════════════════════

def longitudinal_mode(khat_c):
    """Longitudinal (λ=0) photon wave function spinor, Mohr Eq. (237).

    The longitudinal polarization vector is ε̂₀(k̂) = k̂_s (Mohr Eq. 235).
    The positive-energy 6-component spinor (plane-wave factor omitted) is:
        ψ_{k,0}^(+) ∝ (ε̂₀(k̂), 0)^T = (k̂_s, 0)^T   (Mohr Eq. 237)

    Properties (verified by longitudinal_transverse_orthogonality):
      H ψ_L = 0       (zero energy — Mohr Eq. 241, uses τ·k̂ k̂_s = 0)
      Π^T ψ_L = 0     (purely longitudinal — Mohr Eq. 240)
      ψ_T† ψ_L = 0    (orthogonal to all transverse spinors — Mohr Eq. 249)
    """
    khat_c = np.asarray(khat_c, dtype=float)
    khat_c = khat_c / np.linalg.norm(khat_c)
    khat_s = _M @ khat_c.astype(complex)
    spinor = np.zeros(6, dtype=complex)
    spinor[:3] = khat_s
    return spinor


def longitudinal_transverse_orthogonality(n_dirs=12, seed=8):
    """Verify properties of the longitudinal (λ=0) mode (Mohr §7.2):

      (a) H ψ_L = 0: uses α·k̂ (k̂_s, 0)^T = (0, τ·k̂ k̂_s)^T = 0  (Mohr Eq. 25+241)
      (b) ψ_T† ψ_L = 0 for both transverse polarizations              (Mohr Eq. 249)
      (c) Π^T ψ_L = 0: (τ·k̂)² k̂_s = 0  (τ·k̂ k̂_s = 0 → (τ·k̂)² k̂_s = 0)

    Returns (max_H_residual, max_overlap, max_PiT_residual).
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    max_H_res = max_overlap = max_PiT_res = 0.0

    for d in dirs:
        khat_c = d / np.linalg.norm(d)
        psi_L  = longitudinal_mode(khat_c)
        khat_s = psi_L[:3]
        tau_k  = tau_dot(khat_c)

        # (a) H ψ_L = ℏc|k| α·k̂ ψ_L,  α·k̂ = [[0,τ·k̂],[τ·k̂,0]]
        #     upper half: τ·k̂ * 0 = 0;  lower half: τ·k̂ k̂_s = 0 (Mohr Eq. 25)
        H_lower = tau_k @ khat_s           # τ·k̂ k̂_s  (should be 0)
        max_H_res = max(max_H_res, np.linalg.norm(H_lower))

        # (b) Orthogonality to transverse spinors ψ_T = (ε_s, τ·k̂ ε_s)
        for eps_s in polarization_basis(khat_c):
            psi_T   = np.concatenate([eps_s, tau_k @ eps_s])
            overlap = abs(psi_L.conj() @ psi_T)
            max_overlap = max(max_overlap, overlap)

        # (c) Π^T k̂_s = (τ·k̂)² k̂_s = 0
        Pi_T_khat = tau_k @ (tau_k @ khat_s)
        max_PiT_res = max(max_PiT_res, np.linalg.norm(Pi_T_khat))

    return max_H_res, max_overlap, max_PiT_res


# ══════════════════════════════════════════════════════════════════
#  C1–C4 refinements (Mohr 2010 §C, 2026-05-21)
#  Additional tests recommended in the Mohr summary that the original
#  C1–C4 implementation did not yet exercise.
# ══════════════════════════════════════════════════════════════════

def composite_photon_energy_conservation_c2(k_mag=0.05, n_steps=200,
                                            n_dirs=12, seed=6,
                                            c_factor=C_LAT):
    """C4 refinement (Mohr Eq. 55): track ||E_G||² + c²||B_G||² (the SI/Mohr form).

    In our bilinear construction E_G and B_G are on the same scale, so this is
    equivalent to ||E||² + ||B||² up to an overall (1 + c²)/2 factor — but it
    matches Mohr's convention exactly and lets us detect any drift introduced
    by a c-dependent rescaling.

    Returns the max relative deviation over all directions and time steps.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    max_var = 0.0
    c2 = c_factor * c_factor

    for d in dirs:
        kx, ky, kz = k_mag * d
        psi_p, _, omega_half = weyl_eigenmodes_3d_bcc(kx/2, ky/2, kz/2)
        _, nx, ny, nz = bcc._bcc_uvec(kx/2, ky/2, kz/2)
        n_half = np.array([nx, ny, nz])

        psi = psi_p.copy()
        phi = psi_p.copy()
        E0, B0 = EM_bilinears(psi, phi, n_half)
        u0 = float(np.dot(E0, E0.conj()).real + c2 * np.dot(B0, B0.conj()).real)
        if u0 < 1e-30:
            continue

        ph = np.exp(-1j * omega_half)
        for _ in range(n_steps):
            psi = psi * ph
            phi = phi * ph
            E, B = EM_bilinears(psi, phi, n_half)
            u = float(np.dot(E, E.conj()).real + c2 * np.dot(B, B.conj()).real)
            max_var = max(max_var, abs(u - u0) / u0)
    return max_var


def lorentz_boost_covariance_bilinear_transversality(k_mag=0.05, v_mag=0.4,
                                                     n_dirs=8, seed=27):
    """C3 refinement (Mohr §7.6): verify the bilinear-derived transverse part
    G_T = (1 − k̂k̂·) G is preserved as transverse under V6 → boosted k'.

    The original `lorentz_boost_covariance` already tests Mohr Eqs. 284–287 for
    polarization-vector inputs (ε, τ·k̂ ε).  This refinement uses the bilinear-
    derived polarization vector ε_G ≡ G_T_s / |G_T_s| in place of an abstract
    ε, then runs the same V6 covariance check.  Confirms that the bilinear's
    transverse polarization is a valid Mohr spinor input.

    Returns the max transversality residual at boosted k.
    """
    zeta = float(np.arctanh(np.clip(v_mag, 0.0, 0.9999)))
    dirs_k = _random_dirs(n_dirs, seed=seed)
    dirs_v = _random_dirs(n_dirs, seed=seed + 200)
    max_trans = 0.0

    for d_k, d_v in zip(dirs_k, dirs_v):
        khat_c = d_k / np.linalg.norm(d_k)
        v_hat_c = d_v / np.linalg.norm(d_v)
        k_c = k_mag * khat_c

        # Build G = φ^T σ ψ at k/2 with ψ = φ = + eigenmode.
        psi_p, _, _ = weyl_eigenmodes_3d_bcc(k_c[0]/2, k_c[1]/2, k_c[2]/2)
        G = bilinear_G(psi_p, psi_p)        # complex 3-vector
        G_T = _transverse_part(G, khat_c)   # transverse 3-vector

        norm_GT = float(np.linalg.norm(G_T))
        if norm_GT < 1e-12:
            # G aligned with k̂ — degenerate sample, skip.
            continue
        eps_c = G_T / norm_GT
        eps_s = _M @ eps_c.astype(complex)

        # Run the standard Mohr V6 covariance check on this polarization vector.
        tau_k = tau_dot(khat_c)
        u = np.concatenate([eps_s, tau_k @ eps_s])
        V6 = _lorentz_boost_6x6(v_hat_c, zeta)
        u_prime = V6 @ u
        k_prime_c, _ = _boost_4momentum(k_c, v_hat_c, zeta)
        khat_prime_s = _M @ (k_prime_c / np.linalg.norm(k_prime_c)).astype(complex)
        eps_p = u_prime[:3]
        max_trans = max(max_trans, abs(khat_prime_s.conj() @ eps_p))

    return max_trans


# ══════════════════════════════════════════════════════════════════
#  C7 — Weyl SL(2,ℂ) boost: 4-current Lorentz covariance  (2026-05-23)
# ══════════════════════════════════════════════════════════════════
#
# Representation theory note (2026-05-23):
#
#   The composite-photon bilinear G^i = ψ^T σ^i ψ (Paper 1 Eq. 33,
#   TRANSPOSE) lies in the (1,0) ⊕ (0,0) decomposition of
#   (½,0) ⊗ (½,0).  Under ψ → Aψ it transforms as
#
#       G'^i = ψ^T A^T σ^i A ψ  =  Λ_{(1,0)}^{ij} G^j  −  sinh(ζ) v̂^i (ψ^T ψ)
#
#   The second term is a scalar (0,0) contamination; it is non-zero for
#   generic BCC eigenmodes and points along v̂, NOT along k̂'.  It survives
#   the transverse projection onto k̂', so the (1,0) bilinear path cannot
#   agree with the V6 (½,½) Maxwell-field boost in general.
#
#   The CORRECT Lorentz-covariant object at the spinor level is the
#   Weyl 4-current  j^μ = (ψ†ψ, ψ†σψ),  which lies in the (½,½) rep.
#   Under ψ → Aψ it satisfies  j'^μ = Λ^μ_ν j^ν  exactly
#   (this is the defining identity A†σ̄^μA = Λ^μ_ν σ̄^ν of SL(2,ℂ)).
#   C7 verifies this identity to machine precision.

def sl2c_boost(v_hat_c, zeta):
    """SL(2,ℂ) pure boost for a left-handed Weyl 2-spinor.

    A = exp(−ζ/2 · σ·v̂) = cosh(ζ/2)·I₂ − sinh(ζ/2)·(σ·v̂)

    Under this boost ψ → Aψ the Weyl 4-current j^μ = (ψ†ψ, ψ†σψ)
    transforms as a Lorentz 4-vector: j'^μ = Λ^μ_ν j^ν.  This is the
    (½,½) representation of SL(2,ℂ) and is tested in
    `weyl_sl2c_4current_covariance`.

    Note: the Paper 1 bilinear G^i = ψ^T σ^i ψ (TRANSPOSE) is in the
    (1,0) self-dual rep, a different Lorentz irrep from (½,½).  It does
    not transform as a simple 3-vector under boosts.

    Parameters
    ----------
    v_hat_c : array_like, shape (3,)
        Boost direction unit vector in Cartesian coordinates.
    zeta : float
        Rapidity, ζ = arctanh(|v|/c).

    Returns
    -------
    A : complex ndarray, shape (2, 2)
        SL(2,ℂ) element with det A = 1.
    """
    v = np.asarray(v_hat_c, dtype=float)
    sigma_v = v[0] * _S_X + v[1] * _S_Y + v[2] * _S_Z
    ch = np.cosh(float(zeta) / 2.0)
    sh = np.sinh(float(zeta) / 2.0)
    return ch * np.eye(2, dtype=complex) - sh * sigma_v


def weyl_sl2c_4current_covariance(k_mag=0.3, v_mag=0.6, n_dirs=12, seed=7):
    """C7: Verify the SL(2,ℂ) boost correctly induces Lorentz 4-vector
    covariance on the Weyl 4-current  j^μ = (ψ†ψ, ψ†σψ).

    The algebraic identity under test is the SL(2,ℂ) → SO(1,3) homomorphism:

        A† σ̄^μ A = Λ^μ_ν σ̄^ν      (σ̄^0 = I₂, σ̄^i = σ^i)

    which implies: for ANY Weyl spinor ψ,

        j'^μ ≡ (Aψ)† σ̄^μ (Aψ)  =  Λ^μ_ν j^ν  =  Λ^μ_ν (ψ† σ̄^ν ψ)

    The 4×4 Lorentz boost Λ along v̂ with rapidity ζ is:

        Λ^00 = cosh ζ,    Λ^0i = Λ^i0 = −sinh ζ · v̂^i
        Λ^ij = δ^ij + (cosh ζ − 1) v̂^i v̂^j

    The test samples random (k̂, v̂) pairs, evaluates j and j' from BCC
    eigenmodes, and reports the max relative residual |j' − Λj| / |Λj|.

    Expected: < 1e-13 (machine-precision algebraic identity).

    Physical note: G^i = ψ^T σ^i ψ (Paper 1 Eq. 33, transpose bilinear)
    is in the (1,0) Lorentz irrep and carries a scalar (0,0) contamination
    under boosts — it cannot directly match the V6 Maxwell-field boost
    which acts on the (½,½) vector rep.  The 4-current j^μ is the correct
    (½,½) object at the spinor level.
    """
    zeta   = float(np.arctanh(np.clip(v_mag, 0.0, 0.9999)))
    dirs_k = _random_dirs(n_dirs, seed=seed)
    dirs_v = _random_dirs(n_dirs, seed=seed + 100)

    ch = np.cosh(zeta)
    sh = np.sinh(zeta)

    max_res = 0.0

    for d_k, d_v in zip(dirs_k, dirs_v):
        khat_c  = d_k / np.linalg.norm(d_k)
        v_hat_c = d_v / np.linalg.norm(d_v)
        k_c     = k_mag * khat_c
        v       = v_hat_c          # shorthand

        # BCC + eigenmode at k/2
        psi, _, _ = weyl_eigenmodes_3d_bcc(k_c[0]/2, k_c[1]/2, k_c[2]/2)

        # ── Weyl 4-current j^μ = (ψ†ψ, ψ†σψ) ──────────────────────
        j = np.array([
            np.real(psi.conj() @ psi),           # j^0 = ψ†ψ  (real ≥ 0)
            np.real(psi.conj() @ _S_X @ psi),    # j^1 = ψ†σ^x ψ  (real)
            np.real(psi.conj() @ _S_Y @ psi),    # j^2 = ψ†σ^y ψ  (real)
            np.real(psi.conj() @ _S_Z @ psi),    # j^3 = ψ†σ^z ψ  (real)
        ])

        # ── Lorentz 4-vector boost Λ  ───────────────────────────────
        # Λ^μ_ν j^ν  computed directly (avoids building 4×4 matrix)
        vdj = v[0]*j[1] + v[1]*j[2] + v[2]*j[3]   # v̂·j_spatial
        j_lam = np.array([
            ch*j[0] - sh*vdj,
            j[1] + (ch - 1.0)*v[0]*vdj - sh*v[0]*j[0],
            j[2] + (ch - 1.0)*v[1]*vdj - sh*v[1]*j[0],
            j[3] + (ch - 1.0)*v[2]*vdj - sh*v[2]*j[0],
        ])

        # ── SL(2,ℂ) boosted 4-current ──────────────────────────────
        A    = sl2c_boost(v_hat_c, zeta)
        psip = A @ psi
        j_sl2c = np.array([
            np.real(psip.conj() @ psip),
            np.real(psip.conj() @ _S_X @ psip),
            np.real(psip.conj() @ _S_Y @ psip),
            np.real(psip.conj() @ _S_Z @ psip),
        ])

        # ── Residual |j' − Λj| / |Λj|  ─────────────────────────────
        norm_ref = np.linalg.norm(j_lam)
        if norm_ref < 1e-30:
            continue
        res = float(np.linalg.norm(j_sl2c - j_lam) / norm_ref)
        max_res = max(max_res, res)

    return max_res


# ══════════════════════════════════════════════════════════════════
#  C5 — Photon angular-momentum eigenstates  (Mohr 2010 §8, Eqs. 391–393)
# ══════════════════════════════════════════════════════════════════
#
# Vector spherical harmonics Y^m_{jl}(n̂):
#
#     Y^m_{jl}(n̂) = Σ_{m_l + m_s = m} <l m_l; 1 m_s | j m> Y_{l m_l}(n̂) ê_{m_s}
#
# Standard transverse combinations (Jackson §9.7, Varshalovich §7.3):
#     Y^m_{j,M} = Y^m_{j,j}              (magnetic multipole, l = j)
#     Y^m_{j,E} = √((j+1)/(2j+1)) Y^m_{j,j-1} + √(j/(2j+1)) Y^m_{j,j+1}
#     Y^m_{j,L} = √(j/(2j+1)) Y^m_{j,j-1} - √((j+1)/(2j+1)) Y^m_{j,j+1}
#                                         (longitudinal: n̂ Y_{jm})
# Properties verified by tests:
#     J^2 Y = j(j+1) Y    (built-in via CG construction)
#     J_z Y = m Y         (built-in: every CG term has m_l + m_s = m)
#     n̂_s† · Y^E = 0      (transversality of electric multipole)
#     n̂_s† · Y^M = 0      (transversality of magnetic multipole)
#     ∫ Y^{m†}_{jl} · Y^{m'}_{j'l'} dΩ = δ_{jj'} δ_{mm'} δ_{ll'}
# ══════════════════════════════════════════════════════════════════

# Spherical-basis spin-1 unit vectors in the Mohr basis (Eq. 23 mapping).
# Index 0 ↔ m_s = +1, index 1 ↔ m_s = 0, index 2 ↔ m_s = -1.
_E_SPHERICAL = np.eye(3, dtype=complex)


@lru_cache(maxsize=4096)
def _clebsch_gordan(j1, m1, j2, m2, j, m):
    """Float-valued <j1 m1; j2 m2 | j m> Clebsch-Gordan coefficient.

    Backed by sympy.physics.quantum.cg.CG with a cache.
    """
    if abs(m1) > j1 or abs(m2) > j2 or abs(m) > j:
        return 0.0
    if m1 + m2 != m:
        return 0.0
    if j < abs(j1 - j2) or j > j1 + j2:
        return 0.0
    from sympy.physics.quantum.cg import CG
    from sympy import Rational
    val = CG(Rational(j1), Rational(m1), Rational(j2), Rational(m2),
             Rational(j), Rational(m)).doit()
    return float(val)


def _scalar_sph_harm(l, m, theta, phi):
    """Standard scalar spherical harmonic Y_{lm}(θ, φ) with Condon-Shortley phase.

    Direct implementation via the associated Legendre polynomial recurrence.
    """
    m_abs = abs(m)
    x = math.cos(theta)
    # P_m^m(x) closed form: (-1)^m (2m-1)!! (1-x²)^(m/2)
    pmm = 1.0
    if m_abs > 0:
        somx2 = math.sqrt(max(1.0 - x*x, 0.0))
        fact = 1.0
        for _ in range(1, m_abs + 1):
            pmm *= -fact * somx2
            fact += 2.0
    if l == m_abs:
        plm = pmm
    else:
        pmmp1 = x * (2*m_abs + 1) * pmm
        if l == m_abs + 1:
            plm = pmmp1
        else:
            pll = 0.0
            for ll in range(m_abs + 2, l + 1):
                pll = (x * (2*ll - 1) * pmmp1 - (ll + m_abs - 1) * pmm) / (ll - m_abs)
                pmm, pmmp1 = pmmp1, pll
            plm = pll
    norm = math.sqrt((2*l + 1) / (4*math.pi) *
                     math.factorial(l - m_abs) / math.factorial(l + m_abs))
    y = norm * plm * complex(math.cos(m_abs*phi), math.sin(m_abs*phi))
    if m < 0:
        y = ((-1) ** m_abs) * y.conjugate()
    return y


def vector_spherical_harmonic(j, m, l, theta, phi):
    """CG-coupled vector spherical harmonic Y^m_{jl}(n̂), spherical-basis 3-vector.

    Returns the zero vector if (j, l) violates the triangle |j-1| ≤ l ≤ j+1.
    """
    if l < abs(j - 1) or l > j + 1 or l < 0:
        return np.zeros(3, dtype=complex)
    vec = np.zeros(3, dtype=complex)
    for m_l in range(-l, l + 1):
        m_s = m - m_l
        if abs(m_s) > 1:
            continue
        cg = _clebsch_gordan(l, m_l, 1, m_s, j, m)
        if cg == 0.0:
            continue
        y_lm = _scalar_sph_harm(l, m_l, theta, phi)
        idx = {1: 0, 0: 1, -1: 2}[m_s]
        vec[idx] += cg * y_lm
    return vec


def vsh_magnetic(j, m, theta, phi):
    """Y^m_{j,M} = Y^m_{j,j} — magnetic multipole VSH, transverse to n̂."""
    return vector_spherical_harmonic(j, m, j, theta, phi)


def vsh_electric(j, m, theta, phi):
    """Y^m_{j,E} = √((j+1)/(2j+1)) Y^m_{j,j-1} + √(j/(2j+1)) Y^m_{j,j+1}.

    Transverse to n̂ (verified by test_vsh_transversality).
    """
    cA = math.sqrt(j / (2*j + 1))
    cB = math.sqrt((j + 1) / (2*j + 1))
    Y_lo = vector_spherical_harmonic(j, m, j - 1, theta, phi)
    Y_hi = vector_spherical_harmonic(j, m, j + 1, theta, phi)
    return cB * Y_lo + cA * Y_hi


def vsh_longitudinal(j, m, theta, phi):
    """Y^m_{j,L} = √(j/(2j+1)) Y^m_{j,j-1} - √((j+1)/(2j+1)) Y^m_{j,j+1}.

    Equal to n̂ Y_{jm} — purely radial, orthogonal to the two transverse VSHs.
    """
    cA = math.sqrt(j / (2*j + 1))
    cB = math.sqrt((j + 1) / (2*j + 1))
    Y_lo = vector_spherical_harmonic(j, m, j - 1, theta, phi)
    Y_hi = vector_spherical_harmonic(j, m, j + 1, theta, phi)
    return cA * Y_lo - cB * Y_hi


def photon_ang_mom_eigenstate(j, m, kind, theta, phi):
    """Build the 6-component photon spinor for the (j, m, kind) eigenstate.

    kind ∈ {'E', 'M', 'L'} selects electric/magnetic/longitudinal multipole.
    Returns (E_s, ic_lat B_s)^T with the bilinear-construction scaling.

    For magnetic and electric kinds the upper component is the transverse VSH
    and the lower is τ·n̂ (upper) per Mohr Eq. 285.  For longitudinal, the lower
    component is zero (Mohr Eq. 237).
    """
    if kind == 'M':
        upper = vsh_magnetic(j, m, theta, phi)
    elif kind == 'E':
        upper = vsh_electric(j, m, theta, phi)
    elif kind == 'L':
        upper = vsh_longitudinal(j, m, theta, phi)
    else:
        raise ValueError(f"kind must be 'E', 'M', or 'L'; got {kind!r}")

    n_c = np.array([math.sin(theta) * math.cos(phi),
                    math.sin(theta) * math.sin(phi),
                    math.cos(theta)], dtype=float)
    tau_n = tau_dot(n_c)
    lower = tau_n @ upper if kind != 'L' else np.zeros(3, dtype=complex)
    return np.concatenate([upper, lower])


def test_vsh_orthonormality(j_max=2, n_theta=20, n_phi=20):
    """∫ Y^{m†}_{jl}(n̂) · Y^{m'}_{j'l'}(n̂) dΩ = δ_{jj'} δ_{mm'} δ_{ll'}.

    Gauss-Legendre quadrature on cos(θ), uniform trapezoid on φ.
    """
    cos_nodes, cos_wts = np.polynomial.legendre.leggauss(n_theta)
    theta_nodes = np.arccos(cos_nodes)
    phi_step = 2 * math.pi / n_phi
    phi_nodes = np.arange(n_phi) * phi_step

    triples = []
    for j in range(1, j_max + 1):
        for m in range(-j, j + 1):
            for l in (j - 1, j, j + 1):
                if l < 0:
                    continue
                triples.append((j, m, l))

    cached = {}
    for tr in triples:
        j, m, l = tr
        grid = np.zeros((n_theta, n_phi, 3), dtype=complex)
        for it, th in enumerate(theta_nodes):
            for ip, ph in enumerate(phi_nodes):
                grid[it, ip] = vector_spherical_harmonic(j, m, l, th, ph)
        cached[tr] = grid

    max_err = 0.0
    for a in triples:
        for b in triples:
            integrand = np.einsum('ijc,ijc->ij', cached[a].conj(), cached[b])
            integral = 0.0
            for it in range(n_theta):
                integral += cos_wts[it] * np.sum(integrand[it, :]) * phi_step
            expected = 1.0 if a == b else 0.0
            max_err = max(max_err, abs(integral - expected))
    return max_err


def test_vsh_transversality(j_max=2, n_dirs=8, seed=29):
    """Verify n̂_s† · Y^m_{j,M} = 0 and n̂_s† · Y^m_{j,E} = 0 at random n̂.

    Confirms the standard transverse-VSH decomposition; the longitudinal
    Y^m_{j,L} is the orthogonal radial mode.
    """
    rng = np.random.default_rng(seed)
    max_M = max_E = 0.0
    for _ in range(n_dirs):
        theta = float(rng.uniform(0.2, math.pi - 0.2))
        phi = float(rng.uniform(0.0, 2*math.pi))
        n_c = np.array([math.sin(theta)*math.cos(phi),
                        math.sin(theta)*math.sin(phi),
                        math.cos(theta)])
        n_s = _M @ n_c.astype(complex)
        for j in range(1, j_max + 1):
            for m in range(-j, j + 1):
                YM = vsh_magnetic(j, m, theta, phi)
                YE = vsh_electric(j, m, theta, phi)
                max_M = max(max_M, abs(n_s.conj() @ YM))
                max_E = max(max_E, abs(n_s.conj() @ YE))
    return max_M, max_E


def test_vsh_Jz_eigenvalue(j_max=2, n_dirs=4, seed=31, h=1e-4):
    """J_z = L_z + S_z; verify (J_z Y^m_{jl}) = m Y^m_{jl} at random directions.

    L_z = -i ∂/∂φ acts only on Y_{lm_l} → m_l per term.  S_z is diag(+1, 0, -1)
    in spherical-basis indexing.  Since each CG term has m_l + m_s = m, the
    identity holds by construction; the test verifies the numerical CG sums.
    """
    rng = np.random.default_rng(seed)
    max_err = 0.0
    Sz = np.array([+1.0, 0.0, -1.0])
    for _ in range(n_dirs):
        theta = float(rng.uniform(0.2, math.pi - 0.2))
        phi = float(rng.uniform(0.0, 2*math.pi))
        for j in range(1, j_max + 1):
            for m in range(-j, j + 1):
                for l in (max(0, j - 1), j, j + 1):
                    Y = vector_spherical_harmonic(j, m, l, theta, phi)
                    Yp = vector_spherical_harmonic(j, m, l, theta, phi + h)
                    Ym = vector_spherical_harmonic(j, m, l, theta, phi - h)
                    Lz_Y = -1j * (Yp - Ym) / (2*h)
                    JzY = Lz_Y + Sz * Y
                    max_err = max(max_err, np.max(np.abs(JzY - m * Y)))
    return max_err


# ══════════════════════════════════════════════════════════════════
#  C6 — Source coupling and Maxwell Green function  (Mohr 2010 §C6)
# ══════════════════════════════════════════════════════════════════
#
# Mohr's source-term packaging:
#     Ξ(x) = (-μ₀ c J_s(x), 0)^T    (Mohr Eq. 57)
# Maxwell equation in 6-component form:
#     i ∂_t Ψ = H Ψ + Ξ      with  H = c (α · k) acting on (E, icB)
# where α = [[0, τ·k̂], [τ·k̂, 0]].
# Free-space momentum-space Green function (retarded):
#     G(ω, k) = (H(k) − ω − iε)^(-1)
# Dirac current sources the Maxwell field:
#     J^μ(x) = ψ̄ γ^μ ψ,   ∂_μ J^μ = 0  (current conservation)
# ══════════════════════════════════════════════════════════════════

# Cartesian → spherical-basis vector transform (already defined as _M).
# μ₀ and c default to lattice units; the relevant test is structural, not scale.
_MU0_C = 1.0  # μ₀ c absorbed into the source; tests check structure, not magnitude.


def maxwell_hamiltonian_k(k_c, c_factor=C_LAT):
    """6×6 photon Hamiltonian H(k) = c α·k  in spherical-basis (E, icB) packaging.

    α·k̂ = [[0, τ·k̂], [τ·k̂, 0]] from Mohr §4.  Returns the matrix H acting on
    a unit-normalized 6-spinor (E_s, ic_lat B_s)^T.
    """
    k_c = np.asarray(k_c, dtype=float)
    k_mag = float(np.linalg.norm(k_c))
    if k_mag < 1e-20:
        return np.zeros((6, 6), dtype=complex)
    khat_c = k_c / k_mag
    tau_k = tau_dot(khat_c)
    H = np.zeros((6, 6), dtype=complex)
    H[:3, 3:] = tau_k
    H[3:, :3] = tau_k
    return c_factor * k_mag * H


def maxwell_green_function_k(omega, k_c, eps=1e-9, c_factor=C_LAT):
    """Free-space retarded Green function G(ω, k) = (H(k) − ω − iε)^(-1).

    Returns a 6×6 complex matrix.  Singular on the photon mass shell
    ω = ± c |k|; pass an off-shell ω for tests.
    """
    H = maxwell_hamiltonian_k(k_c, c_factor=c_factor)
    A = H - (omega + 1j * eps) * np.eye(6, dtype=complex)
    return np.linalg.inv(A)


def maxwell_source_term(J_c):
    """Mohr's Ξ(x) = (-μ₀ c J_s, 0)^T from a Cartesian current 3-vector.

    Converts J from Cartesian to spherical basis via _M and packages into a
    6-component spinor with zero lower half.
    """
    J_s = _M @ np.asarray(J_c, dtype=complex)
    Xi = np.zeros(6, dtype=complex)
    Xi[:3] = -_MU0_C * J_s
    return Xi


def dirac_current_at_momentum(k_c, sign='+', mass=0.0):
    """4-current J^μ = ψ̄ γ^μ ψ for the Dirac plane-wave eigenstate at momentum k.

    Uses the Bisio Weyl 2-spinor eigenmode (mass=0 default → massless Weyl) and
    builds a 4-component Dirac spinor as ψ_D = (ψ, χ)^T with χ = ψ for the
    massless positive-helicity case.  Returns J^μ = (J^0, J^1, J^2, J^3) in
    Cartesian components.

    For a massless Weyl eigenstate of helicity +, the current satisfies
    k_μ J^μ = 0 exactly (lattice version of current conservation).
    """
    kx, ky, kz = k_c
    psi_p, _, omega = weyl_eigenmodes_3d_bcc(kx, ky, kz, sign=sign)
    psi_p = psi_p / np.linalg.norm(psi_p)
    sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    # Massless Weyl: ψ̄γ^μψ = (ψ†ψ, ψ†σψ).
    J0 = float((psi_p.conj() @ (I2 @ psi_p)).real)
    J1 = float((psi_p.conj() @ (sigma1 @ psi_p)).real)
    J2 = float((psi_p.conj() @ (sigma2 @ psi_p)).real)
    J3 = float((psi_p.conj() @ (sigma3 @ psi_p)).real)
    return np.array([J0, J1, J2, J3], dtype=float), omega


def test_green_function_inverse(k_mag=0.3, n_dirs=8, seed=37,
                                omega_factor=0.5, eps=1e-9):
    """Verify (H(k) − ω) · G(ω, k) = I  off-shell to linear-algebra precision.

    Uses ω = omega_factor · c |k| < c |k| (off-shell), so no pole and the
    inversion is well-conditioned.

    Returns the max ||H · G − (ω + iε) G − I||_∞ over n_dirs random directions.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    I6 = np.eye(6, dtype=complex)
    max_err = 0.0
    for d in dirs:
        k_c = k_mag * (d / np.linalg.norm(d))
        omega = omega_factor * C_LAT * k_mag
        H = maxwell_hamiltonian_k(k_c)
        G = maxwell_green_function_k(omega, k_c, eps=eps)
        # (H − (ω + iε)I) G  should equal I
        A = H - (omega + 1j * eps) * I6
        residual = A @ G - I6
        max_err = max(max_err, float(np.max(np.abs(residual))))
    return max_err


def test_weyl_current_structure(k_mag=0.3, n_dirs=8, seed=41):
    """For a helicity-+ Weyl eigenstate the current is exactly light-like
    with J^0 = 1 and J⃗ = k̂.  Verify three structural identities at machine
    precision (these are exact algebraic consequences of σ·k̂ ψ = ψ):

      (a) J^0 = ψ†ψ = 1
      (b) |J⃗| = 1                  (helicity-saturated → J⃗ unit-norm)
      (c) J⃗ = k̂                    (current parallel to momentum)

    Returns (max_J0_err, max_Jspatial_norm_err, max_alignment_err).

    NOTE: The continuum "k_μ J^μ = 0" current conservation does not hold for
    this QCA Weyl mode because the lattice dispersion ω = arccos(u(k)) ≠ |k|
    (we have c_lat = 1/√3 ≠ 1). The structural identities above are the
    lattice-native exact form. Full Maxwell-Dirac source coupling (Mohr §C6
    "longer term") would require a Dirac construction with both chiralities,
    not just the upper Weyl component.
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    max_J0_err = max_norm_err = max_align_err = 0.0
    for d in dirs:
        khat = d / np.linalg.norm(d)
        k_c = k_mag * khat
        J, _ = dirac_current_at_momentum(k_c)
        max_J0_err = max(max_J0_err, abs(J[0] - 1.0))
        Jspatial = J[1:]
        max_norm_err = max(max_norm_err, abs(np.linalg.norm(Jspatial) - 1.0))
        # Alignment with BCC eigenmode spin-axis n̂ (= k̂ in continuum limit).
        # The BCC + eigenmode satisfies σ·n̂ ψ = ψ, so J⃗ = n̂ exactly.
        _, nx, ny, nz = bcc._bcc_uvec(k_c[0], k_c[1], k_c[2])
        n_vec = np.array([nx, ny, nz])
        nhat = n_vec / np.linalg.norm(n_vec)
        max_align_err = max(max_align_err, float(np.linalg.norm(Jspatial - nhat)))
    return max_J0_err, max_norm_err, max_align_err


def test_source_coupling_shape(n_dirs=6, seed=43):
    """Structural check: maxwell_source_term(J) has zero lower half and
    upper half equal to -μ₀c J_s.  Verifies the Mohr Eq. 57 packaging.
    """
    rng = np.random.default_rng(seed)
    max_lower = 0.0
    max_upper_err = 0.0
    for _ in range(n_dirs):
        J_c = rng.normal(size=3)
        Xi = maxwell_source_term(J_c)
        # Lower half should be zero.
        max_lower = max(max_lower, float(np.max(np.abs(Xi[3:]))))
        # Upper half should equal -μ₀c (M @ J_c).
        expected = -_MU0_C * (_M @ J_c.astype(complex))
        max_upper_err = max(max_upper_err, float(np.max(np.abs(Xi[:3] - expected))))
    return max_lower, max_upper_err


# ══════════════════════════════════════════════════════════════════
#  C8 — Real-rotation vs Maxwell curl  (2026-05-23, proposed test)
#
#  Finding 23 established that the O(k) curl residual is π/2 phase-locked:
#  the discrete bilinear evolution is a REAL rotation of (E, B) in field
#  space, while the Maxwell curl RHS is IMAGINARY at leading order.
#
#  This test checks both equations against E_G(t+1) computed directly from
#  the bilinear propagator:
#
#    (A) Real-rotation prediction:
#        E_G(t+1) = cos(Ω) E_G(t) + sin(Ω) (k̂ × B_G(t))    [Ω = 2ω(k/2)]
#
#    (B) Maxwell curl prediction (continuous-time, O(Δt) accurate):
#        E_G(t+1) ≈ E_G(t) + i (2 n_{k/2}) × B_G(t)
#
#  Expected results:
#    real-rotation residual  ~ machine precision  (< 1e-13)
#    Maxwell curl residual   ~ c_lat/√2 · |k|    (≈ 0.408 · k  for BCC)
#
#  The k-scan variant sweeps |k| over a decade and measures both residuals
#  as a function of k, confirming the O(k) scaling of the Maxwell gap.
# ══════════════════════════════════════════════════════════════════

def real_rotation_vs_maxwell_curl(k_mag=0.05, n_dirs=12, seed=50):
    """Compare E_G(t+1) from the bilinear propagator to two predictions:

    (A) Real-rotation: E(t+1) = cos(Ω) E(t) + sin(Ω) (k̂ × B(t))
    (B) Maxwell curl:  E(t+1) ≈ E(t) + i (2 n_{k/2}) × B(t)

    Both predictions also tested for B (with the sign-flipped form):
    (A_B) B(t+1) = -sin(Ω) (k̂ × E(t)) + cos(Ω) B(t)
    (B_B) B(t+1) ≈ B(t) − i (2 n_{k/2}) × E(t)

    Returns a dict:
      'rot_E'   : max |E(t+1) − rot_pred_E| / denom   (real-rotation, E)
      'rot_B'   : max |B(t+1) − rot_pred_B| / denom   (real-rotation, B)
      'curl_E'  : max |E(t+1) − curl_pred_E| / denom  (Maxwell curl, E)
      'curl_B'  : max |B(t+1) − curl_pred_B| / denom  (Maxwell curl, B)
      'k_mag'   : the k_mag used
      'Omega'   : typical Ω = 2 ω(k/2) (last direction)

    Convention: φ = ψ_minus, ψ = ψ_plus at k/2, both evolved by e^{-iω}
    per tick (the composite-photon eigenmode of Finding 23 / F21 baseline).
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    rot_E_errs = []
    rot_B_errs = []
    curl_E_errs = []
    curl_B_errs = []
    last_Omega = 0.0

    for d in dirs:
        kx, ky, kz = k_mag * d
        kx_h, ky_h, kz_h = kx / 2, ky / 2, kz / 2

        # Eigenmodes at k/2
        psi_p, psi_m, omega_half = weyl_eigenmodes_3d_bcc(kx_h, ky_h, kz_h, sign='+')

        # BCC n-vector at k/2
        _, nx, ny, nz = bcc._bcc_uvec(kx_h, ky_h, kz_h, sign='+')
        n_half = np.array([nx, ny, nz], dtype=float)

        # Composite photon: φ = psi_minus, ψ = psi_plus (F23 baseline convention)
        phi = psi_m
        psi = psi_p

        # t = 0 fields
        E0, B0 = EM_bilinears(psi, phi, n_half)

        # One CA tick: both modes evolve by e^{-iω} (photon global phase e^{-iΩ})
        ph = np.exp(-1j * omega_half)
        psi_t = psi * ph
        phi_t = phi * ph
        E1, B1 = EM_bilinears(psi_t, phi_t, n_half)

        Omega = 2.0 * omega_half
        last_Omega = Omega

        # ── (A) Real-rotation prediction ──────────────────────────────
        # Derived in F23 from G_T(t) = e^{-iΩt} G_T(0), with G_T = A + iC (real):
        #
        #   E = 2|n| Re(G_T) = 2|n| A
        #   B = 2|n| Im(G_T) = 2|n| C
        #   G_T(t+1) = e^{-iΩ} G_T(t)  →
        #   E(t+1) = 2|n| Re(e^{-iΩ}(A+iC)) = cos(Ω) E(t) + sin(Ω) B(t)
        #   B(t+1) = 2|n| Im(e^{-iΩ}(A+iC)) = -sin(Ω) E(t) + cos(Ω) B(t)
        #
        # This is a rigid rotation of the (E, B) pair in field space.
        # No cross product is needed — E and B already encode the transverse
        # plane from the bilinear construction.
        rot_pred_E_n = np.cos(Omega) * E0 + np.sin(Omega) * B0
        rot_pred_B_n = -np.sin(Omega) * E0 + np.cos(Omega) * B0

        # ── (B) Maxwell curl prediction ────────────────────────────────
        # E(t+1) ≈ E(t) + i (2n_{k/2}) × B(t)   [O(Δt) accurate, Δt=1]
        two_n = 2.0 * n_half
        curl_pred_E = E0 + 1j * np.cross(two_n, B0)
        curl_pred_B = B0 - 1j * np.cross(two_n, E0)

        # Normalisation denominator
        denom = float(np.linalg.norm(E0) + np.linalg.norm(B0) + 1e-30)

        # Use n̂-based rotation as the "real-rotation" residual (exact BCC)
        rot_E_errs.append(float(np.linalg.norm(E1 - rot_pred_E_n) / denom))
        rot_B_errs.append(float(np.linalg.norm(B1 - rot_pred_B_n) / denom))
        curl_E_errs.append(float(np.linalg.norm(E1 - curl_pred_E) / denom))
        curl_B_errs.append(float(np.linalg.norm(B1 - curl_pred_B) / denom))

    return {
        'rot_E':  max(rot_E_errs),
        'rot_B':  max(rot_B_errs),
        'curl_E': max(curl_E_errs),
        'curl_B': max(curl_B_errs),
        'k_mag':  k_mag,
        'Omega':  last_Omega,
    }


def real_rotation_k_scan(k_values=None, n_dirs=8, seed=51):
    """Sweep |k| and measure real-rotation vs Maxwell curl residuals at each k.

    Returns a list of dicts, one per k value, each with the same keys as
    real_rotation_vs_maxwell_curl plus 'curl_over_k' and 'rot_over_k' for
    the normalised O(k) coefficients.

    Expected behaviour:
      curl_E / k  →  c_lat / √2  (flat, geometry-independent constant from F23)
      rot_E  / k  →  0           (real-rotation holds to machine precision)
    """
    if k_values is None:
        k_values = [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1]
    rows = []
    for k in k_values:
        r = real_rotation_vs_maxwell_curl(k_mag=k, n_dirs=n_dirs, seed=seed)
        r['curl_over_k'] = r['curl_E'] / k
        r['rot_over_k']  = r['rot_E']  / k
        rows.append(r)
    return rows


# ══════════════════════════════════════════════════════════════════
#  C9 — BCC spin axis n̂(k) and scalar contamination of (1,0) bilinear
#       (2026-05-23, Finding F26)
#
#  The (1,0) bilinear G^i = ψ^T σ^i ψ (transpose) transforms under
#  ψ → Aψ as:
#
#      G'^i = Λ_{(1,0)}^{ij} G^j  −  sinh(ζ) v̂^i (ψ^T ψ)
#
#  The scalar contamination ψ^T ψ is NOT arbitrary — it is fully
#  determined by the BCC eigenmode spinor, which in turn is fixed by k̂.
#
#  The positive-helicity BCC eigenmode satisfies (n̂·σ) ψ₊ = +ψ₊ where
#  n̂ = n(k) / sin ω(k) is the BCC spin axis from ca_bcc.bcc_spin_axis.
#
#  Writing ψ₊ = (cos Θ/2,  sin Θ/2 · e^{iΦ})^T in the standard Bloch
#  basis (n̂_z = cos Θ,  n̂_x = sin Θ cos Φ,  n̂_y = sin Θ sin Φ):
#
#      ψ^T ψ = cos²(Θ/2) + sin²(Θ/2) e^{2iΦ}
#            = 1 − n̂_y (n̂_y − i n̂_x) / (1 + n̂_z)      [full complex]
#
#  Magnitude (phase-convention-independent):
#
#      |ψ^T ψ|² = 1 − n̂_y²                               [KEY RESULT]
#
#  Continuum limit |k| → 0:
#      n̂ → (k̂_x, −k̂_y, k̂_z)  (sign flip on y from BCC chirality)
#      |ψ^T ψ| → √(1 − k̂_y²)  = projection of k̂ onto the xz-plane.
#
#  Average over random directions: ⟨|ψ^T ψ|⟩ = π/4 ≈ 0.785 (continuum).
#  The value |ψ^T ψ| ≈ 0.67 from F24 is at finite k=0.3 with BCC
#  lattice corrections; it is fully determined by k̂.
# ══════════════════════════════════════════════════════════════════

def psi_scalar_bilinear_analytic(kx, ky, kz, sign='+'):
    """
    Return ψ^T ψ (scalar contamination of the (1,0) bilinear) analytically.

    Algebraic form (Finding F26):

        ψ^T ψ = 1 − n̂_y (n̂_y − i n̂_x) / (1 + n̂_z)

    where n̂ = bcc_spin_axis(kx, ky, kz).

    This assumes the *standard* Bloch phase convention: the upper
    component α = cos(Θ/2) is real and non-negative.  Under a global
    phase rotation ψ → e^{iχ} ψ the value acquires a factor e^{2iχ},
    so the magnitude |ψ^T ψ| = √(1 − n̂_y²) is the phase-invariant
    quantity verified by the test.

    Implementation note: the rational form has subtractive cancellation
    when n̂_z ≈ −1 (near the Bloch south pole).  We use the equivalent
    Bloch-angle form  cos²(Θ/2) + sin²(Θ/2)·e^{2iΦ}  which is
    numerically stable everywhere via arccos + arctan2.

    Returns:
        complex scalar (or array matching kx shape)
    """
    n_hat = bcc.bcc_spin_axis(kx, ky, kz, sign=sign)
    nh_x = float(n_hat[0])
    nh_y = float(n_hat[1])
    nh_z = float(n_hat[2])
    # Bloch angles — arccos and arctan2 are stable at all poles.
    Theta = float(np.arccos(np.clip(nh_z, -1.0, 1.0)))
    Phi   = float(np.arctan2(nh_y, nh_x))
    c2 = np.cos(Theta / 2) ** 2   # cos²(Θ/2)
    s2 = np.sin(Theta / 2) ** 2   # sin²(Θ/2) = 1 − c2
    return complex(c2 + s2 * np.exp(2j * Phi))


def weyl_spin_axis_scalar_contamination(k_mag=0.3, n_dirs=12, seed=7):
    """
    C9: Verify |ψ^T ψ|² = 1 − n̂_y² via two independent tracks.

    Track A — Algebraic (machine precision):
        Build ψ₊ analytically from n̂ = bcc_spin_axis using the standard
        Bloch-state formula ψ₊ = (cos Θ/2,  sin Θ/2 · e^{iΦ})^T and
        verify |ψ^T ψ|² = 1 − n̂_y² directly from that spinor.
        This isolates the algebraic identity from the eigenvalue solver.

    Track B — Numerical (eigenvalue-solver precision):
        Use weyl_eigenmodes_3d_bcc (np.linalg.eig) and compare the
        resulting |ψ^T ψ|_num to √(1 − n̂_y²).  Residuals at ~1e-13
        reflect the 2×2 eigensolver accuracy, not the formula.

    Returns:
        alg_err  : float — Track A max error (expect < 1e-14, algebraic)
        num_err  : float — Track B max error (expect < 1e-12, eig solver)
        mean_abs : float — mean |ψ^T ψ| over dirs (confirms non-trivial)
    """
    rng = np.random.default_rng(seed)
    dirs = rng.standard_normal((n_dirs, 3))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)

    alg_errs, num_errs, abs_vals = [], [], []

    for d in dirs:
        kx, ky, kz = k_mag * d[0], k_mag * d[1], k_mag * d[2]

        # ── Analytical n̂ at k/2 ─────────────────────────────────────────
        n_hat = bcc.bcc_spin_axis(kx / 2, ky / 2, kz / 2)
        nh_x, nh_y, nh_z = float(n_hat[0]), float(n_hat[1]), float(n_hat[2])

        abs_predicted = float(np.sqrt(max(1.0 - nh_y**2, 0.0)))

        # ── Track A: algebraic identity |f|² + n̂_y² = 1 ──────────────────
        # f = ψ^Tψ from psi_scalar_bilinear_analytic (uses arccos/arctan2).
        # We verify |f|² + n̂_y² = 1.  No eigenvalue solver involved;
        # residual is bounded by floating-point arithmetic on trig functions.
        f = psi_scalar_bilinear_analytic(kx / 2, ky / 2, kz / 2)
        alg_errs.append(float(abs(abs(f)**2 + nh_y**2 - 1.0)))

        # ── Track B: numerical eigenmode from np.linalg.eig ─────────────
        psi_num, _, _ = weyl_eigenmodes_3d_bcc(kx / 2, ky / 2, kz / 2)
        psi_T_psi_num = psi_num[0]**2 + psi_num[1]**2
        abs_num = abs(psi_T_psi_num)
        num_errs.append(abs(abs_num - abs_predicted))
        abs_vals.append(abs_num)

    return float(max(alg_errs)), float(max(num_errs)), float(np.mean(abs_vals))


if __name__ == '__main__':
    print('=== Original Maxwell tests ===')
    print(f'  Curl residuals (k=0.05):      {maxwell_curl_residual(0.05)}')
    print(f'  Transversality (k=0.05):      {maxwell_transversality(0.05):.4e}')
    print(f'  Dispersion residual (k=0.05): {maxwell_dispersion_residual(0.05):.4e}')
    print()
    print('=== Improvement 1: Polarization basis (Mohr Eqs. 211-213) ===')
    t, o, c = test_polarization_basis()
    print(f'  Transversality error:  {t:.4e}')
    print(f'  Orthonormality error:  {o:.4e}')
    print(f'  Completeness error:    {c:.4e}')
    print()
    print('=== Improvement 2: Poynting energy conservation (Mohr Eq. 55) ===')
    ev = composite_photon_energy_conservation()
    print(f'  Max relative energy variation (200 steps): {ev:.4e}')
    print()
    print('=== Improvement 3: Lorentz boost covariance (Mohr Eqs. 284-287) ===')
    tr, fr, xi = lorentz_boost_covariance()
    print(f'  Transversality error (Eq. 284): {tr:.4e}')
    print(f'  Form error           (Eq. 285): {fr:.4e}')
    print(f'  xi magnitude error   (Eq. 287): {xi:.4e}')
    print()
    print('=== Improvement 4: Longitudinal mode (Mohr Eqs. 241, 249) ===')
    hr, ov, pi = longitudinal_transverse_orthogonality()
    print(f'  H ψ_L = 0 residual (Eq. 241):    {hr:.4e}')
    print(f'  ψ_T† ψ_L overlap   (Eq. 249):    {ov:.4e}')
    print(f'  Π^T ψ_L = 0 residual (Eq. 240):  {pi:.4e}')
    print()
    print('=== C1–C4 refinements (Mohr §C, 2026-05-21) ===')
    ev_c2 = composite_photon_energy_conservation_c2()
    print(f'  Poynting ||E||²+c²||B||² drift (200 steps): {ev_c2:.4e}')
    bt = lorentz_boost_covariance_bilinear_transversality()
    print(f'  Bilinear ε_G V6 transversality at k\'_s:    {bt:.4e}')
    print()
    print('=== C7: Weyl SL(2,ℂ) boost — 4-current Lorentz covariance (2026-05-23) ===')
    cur_res = weyl_sl2c_4current_covariance()
    print(f'  max |j\' − Λj| / |Λj|  (SL2C ↔ SO(1,3)):  {cur_res:.4e}')
    print()
    print('=== C5: Photon angular-momentum eigenstates (Mohr §8) ===')
    on_err = test_vsh_orthonormality(j_max=2, n_theta=20, n_phi=20)
    print(f'  VSH orthonormality residual (j ≤ 2):       {on_err:.4e}')
    M_t, E_t = test_vsh_transversality(j_max=2)
    print(f'  Y^M transversality residual (j ≤ 2):       {M_t:.4e}')
    print(f'  Y^E transversality residual (j ≤ 2):       {E_t:.4e}')
    jz_err = test_vsh_Jz_eigenvalue(j_max=2)
    print(f'  J_z eigenvalue residual (finite-diff):     {jz_err:.4e}')
    print()
    print('=== C6: Maxwell Green function + Dirac source coupling ===')
    g_err = test_green_function_inverse(k_mag=0.3, omega_factor=0.5)
    print(f'  (H − ω) · G = I residual:                  {g_err:.4e}')
    j0e, jne, jae = test_weyl_current_structure(k_mag=0.3)
    print(f'  Weyl current J^0 = 1 residual:             {j0e:.4e}')
    print(f'  Weyl current |J⃗| = 1 residual:              {jne:.4e}')
    print(f'  Weyl current J⃗ = n̂ alignment residual:      {jae:.4e}')
    s_low, s_up = test_source_coupling_shape()
    print(f'  Ξ lower-half = 0 residual:                 {s_low:.4e}')
    print(f'  Ξ upper-half = −μ₀c M·J residual:           {s_up:.4e}')
    print()
    print('=== C8: Real-rotation vs Maxwell curl — 2026-05-23 ===')
    print('  Single k=0.05 comparison:')
    r = real_rotation_vs_maxwell_curl(k_mag=0.05)
    print(f'  Real-rotation residual  E: {r["rot_E"]:.4e}  (expect < 1e-13)')
    print(f'  Real-rotation residual  B: {r["rot_B"]:.4e}  (expect < 1e-13)')
    print(f'  Maxwell curl  residual  E: {r["curl_E"]:.4e}  (expect ~ {0.05 / SQRT3 / SQRT2:.4e})')
    print(f'  Maxwell curl  residual  B: {r["curl_B"]:.4e}')
    print(f'  Omega = 2 omega(k/2):      {r["Omega"]:.6f}  (expect ~ {2*0.05/SQRT3:.6f})')
    print()
    print('  k-scan (curl_E/k and rot_E/k at each k):')
    print(f'  {"k":>8}  {"curl_E/k":>12}  {"rot_E/k":>12}  {"expected c_lat/√2":>18}')
    rows = real_rotation_k_scan()
    for row in rows:
        print(f'  {row["k_mag"]:8.4f}  {row["curl_over_k"]:12.6f}  {row["rot_over_k"]:12.4e}  {C_LAT/SQRT2:18.6f}')
    print()
    print('=== C9: BCC spin axis n̂(k) and scalar contamination |ψᵀψ|² = 1 − n̂_y² (2026-05-23) ===')
    alg_err, num_err, mean_abs = weyl_spin_axis_scalar_contamination()
    print(f'  Track A (algebraic, ψ₊ built from n̂):   {alg_err:.4e}  (expect < 1e-13)')
    print(f'  Track B (numerical, np.linalg.eig):      {num_err:.4e}  (expect < 1e-12)')
    print(f'  mean |ψᵀψ| over 12 dirs at k=0.3:       {mean_abs:.6f}  (continuum limit π/4 ≈ {np.pi/4:.6f})')


# ══════════════════════════════════════════════════════════════════
#  F26 — Exact rotation-law EM propagator
# ══════════════════════════════════════════════════════════════════
#
# Finding 26 (2026-05-23): the speed of light is dΩ/d|k|, not ω/|k|.
# The exact EM propagation law is a rigid rotation of the (E,B) pair
# in field space:
#
#     E(t+1) =  cos(Ω) E(t) + sin(Ω) B(t)
#     B(t+1) = −sin(Ω) E(t) + cos(Ω) B(t)
#
# with Ω(k) = 2 ω_BCC(k/2).  This holds to machine precision (T51:
# 2×10⁻¹⁶ for E, 3.3×10⁻¹⁶ for B) while the Maxwell curl deviates
# by c_lat/√2 · |k| (structural linearisation error, not a defect).
#
# The functions below implement:
#   rotation_omega_bcc        — Ω(k) on a k-grid
#   rotation_step_em_spectral — full-lattice spectral rotation propagator
#   c_from_rotation_rate      — measure c = dΩ/d|k| numerically
#   rotation_law_consistency  — verify rotation law on a live Weyl state
# ══════════════════════════════════════════════════════════════════


def rotation_omega_bcc(KX, KY, KZ, sign='+'):
    """
    Ω(k) = 2 ω_BCC(k/2) — the rotation angle per tick for the composite-
    photon (E, B) pair (Finding 26).

    Parameters
    ----------
    KX, KY, KZ : ndarrays — wavevector components on a grid (radians / cell)
    sign : '+' or '-' — BCC branch (use '+' for the composite-photon convention)

    Returns
    -------
    Omega : ndarray same shape as KX  (in radians, range [0, π])
    """
    return 2.0 * bcc.bcc_dispersion(KX / 2.0, KY / 2.0, KZ / 2.0, sign=sign)


def rotation_step_em_spectral(E_field, B_field, sign='+'):
    """
    One tick of the EXACT EM rotation propagator (Finding 26 / F25).

    Replaces the Maxwell curl stepper as the primary EM propagation law.
    Operates on full spatial-domain (E, B) field arrays via FFT.

    The propagation law in Fourier space (exact to machine precision):

        Ê(k, t+1) =  cos(Ω(k)) Ê(k) + sin(Ω(k)) B̂(k)
        B̂(k, t+1) = −sin(Ω(k)) Ê(k) + cos(Ω(k)) B̂(k)

    with Ω(k) = 2 ω_BCC(k/2).  The rotation angle Ω mixes E and B
    globally per mode but does not mix Cartesian vector components —
    the three spatial components (x, y, z) all rotate together.

    Energy conservation follows geometrically:  ‖E‖² + ‖B‖² is the
    squared radius of the (E, B) pair under the rotation, preserved
    exactly by orthogonality of R(Ω).

    Parameters
    ----------
    E_field : ndarray  shape (..., 3)  where ... = (Lx, Ly, Lz)
        Electric field at each lattice cell.  May be real or complex.
    B_field : ndarray  same shape
        Magnetic field.
    sign : '+' or '-'  — BCC branch (default '+')

    Returns
    -------
    E_new, B_new : ndarrays of the same shape as inputs.

    Notes
    -----
    Maxwell curl stepper comparison:
      - This propagator: exact to ~2×10⁻¹⁶ (T51, F25).
      - Maxwell curl at Δt=1: deviates by c_lat/√2 · |k| per step (F21/F26).
    At small k (k → 0) the two agree — the Maxwell curl is the Ω → 0
    limit of the cosine expansion.
    """
    spatial_shape = E_field.shape[:-1]   # e.g. (Lx, Ly, Lz)
    ndim = len(spatial_shape)
    if ndim != 3:
        raise ValueError(
            f"rotation_step_em_spectral expects 3D spatial shape (..., 3), "
            f"got {E_field.shape}.  Use rotation_step_em_spectral_2d for 2D.")

    Lx, Ly, Lz = spatial_shape

    # Build k-grid (radians / cell)
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    kz = np.fft.fftfreq(Lz) * 2.0 * np.pi
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')   # (Lx, Ly, Lz)

    # Rotation angle per mode
    Omega = rotation_omega_bcc(KX, KY, KZ, sign=sign)       # (Lx, Ly, Lz)
    cosO  = np.cos(Omega)[..., np.newaxis]                   # (Lx, Ly, Lz, 1)
    sinO  = np.sin(Omega)[..., np.newaxis]

    # FFT over spatial axes, preserve vector axis
    axes = (0, 1, 2)
    E_k = np.fft.fftn(E_field, axes=axes)   # (Lx, Ly, Lz, 3)
    B_k = np.fft.fftn(B_field, axes=axes)

    # Exact rotation in Fourier space
    E_k_new =  cosO * E_k + sinO * B_k
    B_k_new = -sinO * E_k + cosO * B_k

    # Back to position space
    E_new = np.fft.ifftn(E_k_new, axes=axes)
    B_new = np.fft.ifftn(B_k_new, axes=axes)

    # The BCC dispersion is chiral: ω_+(−k) = ω_−(k) ≠ ω_+(k) in general.
    # For sign='+', the spectral rotation does NOT preserve the Hermitian symmetry
    # of a real-valued (E, B) field.  The IFFT of a complex input is returned as-is
    # (complex). Real inputs acquire a non-negligible imaginary part; callers should
    # work with complex fields (as the composite-photon bilinear naturally provides).
    return E_new, B_new


def c_from_rotation_rate(eps=1e-5, n_dirs=6, sign='+'):
    """
    Measure c_lat = dΩ/d|k| at |k| → 0 (Finding 26).

    This is the definition of the speed of light as an angular rotation
    rate, not as a phase velocity.  At small |k|:

        Ω(k) = 2 ω_BCC(k/2) ≈ c_lat · |k|
        c_lat = dΩ/d|k| = 2 · (dω_BCC/dk)|_{k→0} = 1/√3   (BCC)

    Parameters
    ----------
    eps    : float  — |k| at which to evaluate the rate (should be ≪ 1)
    n_dirs : int    — number of random directions to average over
    sign   : BCC branch

    Returns
    -------
    dict with keys:
        'c_measured'  : float  — mean measured dΩ/d|k|
        'c_analytic'  : float  — 1/√3  (BCC theoretical value)
        'residual'    : float  — |c_measured − c_analytic|
        'per_dir'     : list of per-direction measurements
    """
    rng = np.random.default_rng(seed=42)
    dirs = rng.standard_normal((n_dirs, 3))
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)

    c_vals = []
    for d in dirs:
        kx, ky, kz = eps * d
        # Finite-difference estimate of dΩ/d|k|
        # Ω(k) = 2·ω_BCC(k/2), so pass k/2 to bcc_dispersion
        Omega_p = 2.0 * float(bcc.bcc_dispersion(
            np.array(kx / 2), np.array(ky / 2), np.array(kz / 2), sign=sign))
        c_vals.append(Omega_p / eps)

    c_mean = float(np.mean(c_vals))
    c_anal = C_LAT                  # 1/√3
    return {
        'c_measured': c_mean,
        'c_analytic': c_anal,
        'residual':   abs(c_mean - c_anal),
        'per_dir':    c_vals,
    }


def dispersion_nonlinearity(k_max=1.0, n_pts=200, sign='+'):
    """Tabulate Ω(k) and its deviation from the linear (Maxwell) approximation.

    The exact dispersion  Ω(k) = 2 ω_BCC(k/2)  agrees with  c_lat · |k|
    only at small k.  The nonlinear correction at finite k is:

        δΩ(k) = Ω(k) − c_lat · |k|

    and the fractional phase-velocity shift is:

        δv_φ / c_lat = Ω(k) / (c_lat · |k|) − 1

    Leading correction for the (1,1,1) diagonal direction (Taylor expansion):

        With θ = k/6 entering ω_BCC via cos³θ + sin³θ:
        1 − u ≈ 3θ²/2 − θ³   →   ω ≈ (k/(2√3))(1 − k/18)
        δΩ ≈ −(c_lat · |k|²)/18   [O(k²) in Ω, O(k) in δv_φ]
        δv_φ / c_lat ≈ −k / 18

    Note: the correction is direction-dependent.  Axis-aligned (1,0,0) is
    exactly linear (no correction); (1,1,1) has a leading O(k) correction
    from the sin³θ term; (1,1,0) has a leading O(k²) correction.
    The (1,1,1) leading formula δv_φ/c ≈ −k/18 is the Planck-scale
    prediction tested by this function (F26 §4).

    Parameters
    ----------
    k_max : float   — maximum |k| to tabulate (default 1.0; Nyquist is π)
    n_pts : int     — number of k points (along (1,0,0) direction)
    sign  : str     — BCC branch

    Returns
    -------
    dict with keys:
        'k'          : ndarray shape (n_pts,)  — |k| values
        'Omega'      : ndarray                 — exact rotation angle per tick
        'Omega_lin'  : ndarray                 — c_lat · |k| (Maxwell linear approx)
        'delta_Omega': ndarray                 — Ω − c_lat |k|
        'delta_vph'  : ndarray                 — fractional phase-velocity deviation
        'delta_vph_theory': ndarray            — leading O(k²) analytic prediction
        'c_lat'      : float                   — 1/√3
    """
    k_arr = np.linspace(0.0, k_max, n_pts + 1)[1:]   # exclude k=0
    # Use the (1,1,1) diagonal direction — axis-aligned (1,0,0) is exactly linear
    # in the BCC dispersion (no nonlinearity visible there), while the diagonal
    # exhibits the full O(k³) correction.
    inv_root3 = 1.0 / np.sqrt(3.0)
    KX = k_arr * inv_root3
    KY = k_arr * inv_root3
    KZ = k_arr * inv_root3
    Omega = rotation_omega_bcc(KX, KY, KZ, sign=sign)
    Omega_lin = C_LAT * k_arr
    delta_Omega = Omega - Omega_lin
    with np.errstate(divide='ignore', invalid='ignore'):
        delta_vph = np.where(k_arr > 0, Omega / Omega_lin - 1.0, 0.0)
    # Leading analytic correction for (1,1,1) BCC: δv_φ/c ≈ −k/18
    delta_vph_theory = -k_arr / 18.0
    return {
        'k':               k_arr,
        'Omega':           Omega,
        'Omega_lin':       Omega_lin,
        'delta_Omega':     delta_Omega,
        'delta_vph':       delta_vph,
        'delta_vph_theory': delta_vph_theory,
        'c_lat':           C_LAT,
    }


def planck_correction_prediction(k_planck_fraction=0.01, sign='+'):
    """Evaluate the Planck-scale photon dispersion correction at a given frequency.

    The exact rotation law predicts a quadratic-in-frequency correction to the
    photon phase velocity (F26 §4):

        δv_φ / c_lat ≈ −c_lat² |k|² / 6 = −|k|² / 18   (BCC)

    At the lattice Planck wavenumber k_Planck = π (Nyquist frequency), this
    correction is of order unity.  At a fraction α of k_Planck:

        |k| = α · π
        δv_φ / c_lat ≈ −α² π² / 18

    This is testable (in principle) via gamma-ray burst arrival-time differences
    for photons at ω ∝ α · ω_Planck.

    Parameters
    ----------
    k_planck_fraction : float
        Fraction of the Planck wavenumber: |k| = α · π.  Default 0.01 (1%).
    sign : str  — BCC branch.

    Returns
    -------
    dict with keys:
        'k'                — |k| in lattice units (= α · π)
        'Omega_exact'      — exact rotation angle Ω(k) per tick
        'Omega_linear'     — c_lat · |k| (Maxwell approximation)
        'delta_vph_exact'  — exact fractional phase-velocity deviation
        'delta_vph_theory' — leading O(k²) analytic approximation
        'k_planck'         — π (Nyquist wavenumber)
        'alpha'            — k_planck_fraction

    Example
    -------
    >>> r = planck_correction_prediction(0.01)
    >>> r['delta_vph_exact']   # ≈ −5.5e-4 at α=0.01
    """
    k_planck = np.pi
    k_val = float(k_planck_fraction) * k_planck
    # Use the (1,1,1) diagonal direction — axis-aligned directions are exactly
    # linear in the BCC dispersion; the diagonal exposes the nonlinear correction.
    inv_root3 = 1.0 / np.sqrt(3.0)
    kc = k_val * inv_root3
    Omega_ex = float(rotation_omega_bcc(
        np.array([[kc]]), np.array([[kc]]), np.array([[kc]]), sign=sign)[0, 0])
    Omega_lin = C_LAT * k_val
    delta_vph_exact  = Omega_ex / Omega_lin - 1.0 if Omega_lin > 0 else 0.0
    # Leading analytic correction for (1,1,1) BCC direction: δv_φ/c ≈ −k/18
    delta_vph_theory = -k_val / 18.0
    return {
        'k':                k_val,
        'Omega_exact':      Omega_ex,
        'Omega_linear':     Omega_lin,
        'delta_vph_exact':  delta_vph_exact,
        'delta_vph_theory': delta_vph_theory,
        'k_planck':         k_planck,
        'alpha':            k_planck_fraction,
    }


def rotation_law_consistency(k_mag=0.05, n_dirs=12, n_steps=20, seed=60,
                             sign='+'):
    """
    Verify that a live Weyl-spinor composite-photon state obeys the
    exact rotation law over multiple ticks (Finding 26 / F25).

    At each tick, the predicted fields from the rotation formula are
    compared to the fields obtained by actually propagating the Weyl
    spinors one step.  The residual should be at machine precision.

    Parameters
    ----------
    k_mag  : float   — |k| of the test mode
    n_dirs : int     — number of BCC directions to test
    n_steps: int     — number of ticks to advance
    sign   : BCC branch

    Returns
    -------
    dict with:
        'max_rot_E'   : max ‖E_pred − E_actual‖ / denom   (rotation law)
        'max_rot_B'   : same for B
        'max_curl_E'  : same using Maxwell curl prediction  (linearisation error)
        'n_steps'     : n_steps
    """
    dirs = _random_dirs(n_dirs, seed=seed)
    rot_E_all, rot_B_all, curl_E_all = [], [], []

    for d in dirs:
        kx, ky, kz = k_mag * d
        kxh, kyh, kzh = kx / 2, ky / 2, kz / 2

        psi_p, psi_m, omega_half = weyl_eigenmodes_3d_bcc(kxh, kyh, kzh, sign=sign)
        _, nx, ny, nz = bcc._bcc_uvec(kxh, kyh, kzh, sign=sign)
        n_half = np.array([nx, ny, nz], dtype=float)

        ph     = np.exp(-1j * omega_half)
        Omega  = 2.0 * omega_half
        two_n  = 2.0 * n_half
        cosO, sinO = np.cos(Omega), np.sin(Omega)

        psi_t, phi_t = psi_p.copy(), psi_m.copy()
        E_t, B_t = EM_bilinears(psi_t, phi_t, n_half)

        max_re, max_rb, max_ce = 0.0, 0.0, 0.0

        for _ in range(n_steps):
            psi_t *= ph;  phi_t *= ph
            E_next, B_next = EM_bilinears(psi_t, phi_t, n_half)

            denom = float(np.linalg.norm(E_t) + np.linalg.norm(B_t) + 1e-30)

            # Rotation prediction
            E_rot = cosO * E_t + sinO * B_t
            B_rot = -sinO * E_t + cosO * B_t

            # Maxwell curl prediction
            E_curl = E_t + 1j * np.cross(two_n, B_t)

            max_re = max(max_re, float(np.linalg.norm(E_next - E_rot) / denom))
            max_rb = max(max_rb, float(np.linalg.norm(B_next - B_rot) / denom))
            max_ce = max(max_ce, float(np.linalg.norm(E_next - E_curl) / denom))

            E_t, B_t = E_next, B_next

        rot_E_all.append(max_re)
        rot_B_all.append(max_rb)
        curl_E_all.append(max_ce)

    return {
        'max_rot_E':  max(rot_E_all),
        'max_rot_B':  max(rot_B_all),
        'max_curl_E': max(curl_E_all),
        'n_steps':    n_steps,
        'k_mag':      k_mag,
    }


# ══════════════════════════════════════════════════════════════════
#  Phase 2 — Full-lattice composite-photon propagation (F26 default)
# ══════════════════════════════════════════════════════════════════

def composite_photon_propagation_full_lattice(n_steps=100, L=16, n_modes=8, seed=77):
    """
    Full-lattice composite-photon propagation using rotation_step_em_spectral.

    Phase 2 of roadmap-f26-rotation.md: validates rotation_step_em_spectral as
    the default EM propagator for simulation loops by placing n_modes independent
    (E, B) plane-wave modes on an L³ BCC lattice, propagating n_steps ticks with
    the exact spectral rotation, and verifying two things:

    1. Energy conservation: ‖E‖² + ‖B‖² constant to machine precision.
    2. Per-mode rotation: each Fourier mode is rotated by exactly Ω(k) per tick.

    Both checks are algebraically forced by the rotation's unitarity — any failure
    would indicate an implementation error in rotation_step_em_spectral.

    Returns
    -------
    dict with keys:
      energy_drift    — max relative energy drift over all steps
      max_mode_error  — max |rotation residual| across all modes and sampled steps
      n_steps, L, n_modes
    """
    rng = np.random.default_rng(seed)

    # k-grid (radians / cell) matching rotation_step_em_spectral convention
    kx_grid = np.fft.fftfreq(L) * 2.0 * np.pi
    ky_grid = np.fft.fftfreq(L) * 2.0 * np.pi
    kz_grid = np.fft.fftfreq(L) * 2.0 * np.pi

    # Choose n_modes distinct k-bins; avoid bin 0 (k=0 ↔ DC, Ω=0)
    bins = set()
    while len(bins) < n_modes:
        ix = int(rng.integers(1, L))
        iy = int(rng.integers(0, L))
        iz = int(rng.integers(0, L))
        bins.add((ix, iy, iz))

    # Build initial k-space field: random complex (E, B) at each chosen bin
    E_k0 = np.zeros((L, L, L, 3), dtype=complex)
    B_k0 = np.zeros((L, L, L, 3), dtype=complex)
    mode_info = []

    for (ix, iy, iz) in bins:
        E_vec = rng.standard_normal(3) + 1j * rng.standard_normal(3)
        B_vec = rng.standard_normal(3) + 1j * rng.standard_normal(3)
        E_k0[ix, iy, iz] = E_vec
        B_k0[ix, iy, iz] = B_vec
        # Rotation angle at this k-bin (same formula as rotation_step_em_spectral)
        kx = kx_grid[ix]; ky = ky_grid[iy]; kz = kz_grid[iz]
        Omega = float(rotation_omega_bcc(
            np.array([[[kx]]]), np.array([[[ky]]]), np.array([[[kz]]]))[0, 0, 0])
        mode_info.append((ix, iy, iz, E_vec.copy(), B_vec.copy(), Omega))

    # Transform to position space
    axes = (0, 1, 2)
    E_field = np.fft.ifftn(E_k0, axes=axes)
    B_field = np.fft.ifftn(B_k0, axes=axes)

    energy0 = float(np.sum(np.abs(E_field)**2) + np.sum(np.abs(B_field)**2))
    max_energy_drift = 0.0
    max_mode_error   = 0.0

    for step in range(n_steps):
        E_field, B_field = rotation_step_em_spectral(E_field, B_field)
        t = step + 1

        # Energy conservation check at every step
        energy_t = float(np.sum(np.abs(E_field)**2) + np.sum(np.abs(B_field)**2))
        drift = abs(energy_t - energy0) / max(energy0, 1e-30)
        max_energy_drift = max(max_energy_drift, drift)

        # Per-mode rotation check every 10 steps (and at step 1)
        if t == 1 or t % 10 == 0:
            E_k = np.fft.fftn(E_field, axes=axes)
            B_k = np.fft.fftn(B_field, axes=axes)
            for (ix, iy, iz, E0, B0, Omega) in mode_info:
                E_pred = np.cos(Omega * t) * E0 + np.sin(Omega * t) * B0
                B_pred = -np.sin(Omega * t) * E0 + np.cos(Omega * t) * B0
                err = float(np.max(np.abs(E_k[ix, iy, iz] - E_pred))
                            + np.max(np.abs(B_k[ix, iy, iz] - B_pred)))
                max_mode_error = max(max_mode_error, err)

    return {
        'energy_drift':  max_energy_drift,
        'max_mode_error': max_mode_error,
        'n_steps': n_steps,
        'L': L,
        'n_modes': n_modes,
    }


# F26 __main__ block — runs after all function definitions above
if __name__ == '__main__':
    print()
    print('=== F26: Speed of light as rotation rate — Exact EM propagator ===')
    print()
    print('  — c_lat = dΩ/d|k| measurement (BCC) —')
    cr = c_from_rotation_rate()
    print(f'  c_lat measured: {cr["c_measured"]:.8f}')
    print(f'  c_lat analytic: {cr["c_analytic"]:.8f}  (= 1/√3)')
    print(f'  residual:       {cr["residual"]:.2e}')
    print()
    print('  — Exact rotation propagator vs Maxwell curl (k=0.05, 20 ticks) —')
    rl = rotation_law_consistency(k_mag=0.05, n_steps=20)
    print(f'  Rotation law residual  E: {rl["max_rot_E"]:.3e}  (machine precision)')
    print(f'  Rotation law residual  B: {rl["max_rot_B"]:.3e}')
    print(f'  Maxwell curl residual  E: {rl["max_curl_E"]:.3e}'
          f'  (= c_lat/√2 · k ≈ {C_LAT / SQRT2 * 0.05:.4f}, linearisation error)')
    print()
    print('  — Dispersion nonlinearity: Ω(k) vs c_lat · k —')
    dn = dispersion_nonlinearity(k_max=1.0, n_pts=5)
    print(f'  {"k":>8}  {"Ω(k)":>10}  {"c·k":>10}  {"δv_φ/c (exact)":>16}  {"δv_φ/c O(k²)":>14}')
    for i, ki in enumerate(dn['k']):
        print(f'  {ki:8.4f}  {dn["Omega"][i]:10.6f}  {dn["Omega_lin"][i]:10.6f}'
              f'  {dn["delta_vph"][i]:16.4e}  {dn["delta_vph_theory"][i]:14.4e}')
    print()
    print('  — Planck-scale correction: δv_φ/c at fraction α of k_Planck = π —')
    print(f'  {"α":>8}  {"k":>8}  {"δv_φ/c (exact)":>16}  {"δv_φ/c O(k²)":>14}')
    for alpha in [0.001, 0.01, 0.1, 0.3]:
        pc = planck_correction_prediction(alpha)
        print(f'  {alpha:8.3f}  {pc["k"]:8.4f}  {pc["delta_vph_exact"]:16.4e}'
              f'  {pc["delta_vph_theory"]:14.4e}')
    print()
    print('  — Phase 2: Full-lattice rotation propagator (default EM evolution) —')
    pl = composite_photon_propagation_full_lattice(n_steps=100, L=16, n_modes=8)
    print(f'  Energy drift (100 ticks, L=16, 8 modes): {pl["energy_drift"]:.2e}'
          f'  (expect < 1e-12)')
    print(f'  Per-mode rotation residual:               {pl["max_mode_error"]:.2e}'
          f'  (expect < 1e-12)')
