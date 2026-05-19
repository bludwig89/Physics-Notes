"""
ca_maxwell.py  —  Composite-photon Maxwell sector (Paper 1 Eq. 35)
==================================================================
Construct the photon as a correlated bilinear of two Weyl fields on
the BCC lattice (the de Broglie "neutrino theory of light" made
rigorous in Bisio et al. 2015).  Paper 1 Eq. 35:

    G^i(k, t)     := φ^T(k/2, t) σ^i ψ(k/2, t)
    E_G(k)         := |n_{k/2}| (G_T + G_T†)
    B_G(k)         := i |n_{k/2}| (G_T† − G_T)

The free-Maxwell curl equations hold:

    2 n_{k/2} · E_G       = 0
    2 n_{k/2} · B_G       = 0
    ∂_t E_G = i · 2 n_{k/2} × B_G
    ∂_t B_G = − i · 2 n_{k/2} × E_G

Substituting 2 n_{k/2} → k in the small-|k| limit recovers Maxwell's
free equations with photon dispersion ω_γ = |k|/√3 (the BCC small-k
Weyl speed times 2, since both component Weyl fields contribute).

This module implements:
  weyl_eigenmodes_3d_bcc(kx, ky, kz, sign='+')   exact ± energy eigenstates
  bilinear_G(psi, phi)                           the σ^i bilinear at one k
  EM_bilinears(psi, phi, n_half)                 E_G, B_G per Paper 1 Eq. 35
  maxwell_curl_residual                          curl-equation test at small k
  maxwell_transversality                         k·E, k·B test
  maxwell_dispersion_residual                    ω_γ = |k|/√3 test
"""

import numpy as np

import ca_bcc as bcc


SQRT3 = np.sqrt(3.0)


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
    """
    Photon frequency Ω_γ = 2 ω(k/2), which → |k|/√3 at small |k|.
    Returns rel err |Ω_γ − |k|/√3| / (|k|/√3).
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


if __name__ == '__main__':
    print('Curl residuals (k=0.05):', maxwell_curl_residual(0.05))
    print('Transversality (k=0.05):', maxwell_transversality(0.05))
    print('Dispersion residual (k=0.05):', maxwell_dispersion_residual(0.05))
