"""
ca_maxwell_2d.py  —  Composite-photon bilinear on the 2D square QCA
====================================================================
Port of `ca_maxwell.py` to the 2D-square Weyl QCA in `ca_core_exact.py`
(Paper 1 Eq. 16).  Purpose: discriminating test for the geometric origin
of the curl-residual constant 1/√6 measured on the BCC lattice
(`findings.md` Finding 7).

The 2D Weyl QCA carries a 2-spinor on a 2D lattice but the unitary has
a non-zero σ_z component (from s_x·s_y), so the bilinear G^i is still
a 3-vector in σ-space.  The cross-product structure of the Maxwell
curl equation is therefore unchanged — only the n(k/2) profile differs.

Predictions for the curl-residual constant `curl/k = C + O(k)`:

  Candidate A — 1/√C(z, 2) with z=4 nearest neighbors:  C = 1/√6 ≈ 0.408
  Candidate B — 1/(√2 · √d) with d=2:                     C = 1/2    = 0.500
  Candidate C — geometric tetrahedral half-angle:         n/a in 2D

A measured C ≈ 0.408 confirms Candidate A (the constant is set by the
*neighbour-pair count*, independent of lattice dimensionality).
A measured C ≈ 0.500 confirms Candidate B (the constant scales with
lattice dimensionality, not with neighbour count).
Anything else falsifies both.

This module mirrors `ca_maxwell.py` API:
  weyl_eigenmodes_2d_square(kx, ky, sign='+')   exact ± energy eigenstates
  bilinear_G(psi, phi)                          σ^i bilinear, returns 3-vec
  EM_bilinears(psi, phi, n_half)                E_G, B_G per Paper 1 Eq. 35
  maxwell_curl_residual_2d                      curl-equation test at small |k|
  maxwell_transversality_2d                     k·E, k·B test
  maxwell_dispersion_residual_2d                ω_γ = |k|/√2 test
"""

import numpy as np

import ca_core_exact as exact


SQRT2 = np.sqrt(2.0)


# ══════════════════════════════════════════════════════════════════
#  Eigenmodes of the 2D-square unitary at a single k
# ══════════════════════════════════════════════════════════════════

def _hamiltonian_matrix_2d(kx, ky):
    """Return the 2×2 matrix U(k) for the 2D-square QCA."""
    u, nx, ny, nz = exact._arccos_2d_uvec(kx, ky)
    U = np.array([
        [u - 1j * nz,            -1j * (nx - 1j * ny)],
        [-1j * (nx + 1j * ny),   u + 1j * nz],
    ], dtype=complex)
    return U


def weyl_eigenmodes_2d_square(kx, ky):
    """
    Return the two 2-spinor eigenmodes of U(k) at this momentum.
    Output: (psi_plus, psi_minus, omega), where U·psi_± = e^{∓iω}·psi_±.
    """
    U = _hamiltonian_matrix_2d(kx, ky)
    eigvals, eigvecs = np.linalg.eig(U)
    phases = -np.angle(eigvals)
    idx_pos = int(np.argmax(phases))
    idx_neg = 1 - idx_pos
    return eigvecs[:, idx_pos], eigvecs[:, idx_neg], float(phases[idx_pos])


# ══════════════════════════════════════════════════════════════════
#  Bilinears (identical to 3D BCC version — operates on σ-space, not k-space)
# ══════════════════════════════════════════════════════════════════

_S_X = np.array([[0, 1], [1, 0]], dtype=complex)
_S_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_S_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_PAULIS = (_S_X, _S_Y, _S_Z)


def bilinear_G(psi, phi):
    """G^i = φ^T σ^i ψ.  Returns a complex 3-vector."""
    return np.array([phi @ S @ psi for S in _PAULIS])


def _transverse_part(v, n_hat):
    return v - (v @ n_hat) * n_hat


def EM_bilinears(psi, phi, n_half):
    """E_G, B_G per Paper 1 Eq. 35.  `n_half` is a real 3-vector
    (with n_z possibly nonzero from the σ_z component of the 2D unitary).
    """
    G = bilinear_G(psi, phi)
    nmag = np.linalg.norm(n_half)
    if nmag < 1e-15:
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

def _random_dirs_2d(n_dirs, seed=0):
    """Random unit vectors in the (x,y) plane; z-component zero."""
    rng = np.random.default_rng(seed)
    thetas = rng.uniform(0.0, 2.0 * np.pi, n_dirs)
    v = np.zeros((n_dirs, 3))
    v[:, 0] = np.cos(thetas)
    v[:, 1] = np.sin(thetas)
    return v


def n_half_2d(kx, ky):
    """The 3-vector (n_x, n_y, n_z) of the 2D unitary at one k.
    The z-component is nonzero from s_x·s_y."""
    _, nx, ny, nz = exact._arccos_2d_uvec(kx, ky)
    return np.array([nx, ny, nz], dtype=float)


def maxwell_curl_residual_2d(k_mag=0.05, n_dirs=8, seed=0):
    """
    Same procedure as `ca_maxwell.maxwell_curl_residual` but on the
    2D-square QCA.  k is restricted to the xy plane (kz = 0).
    """
    dt = 1.0
    dirs = _random_dirs_2d(n_dirs, seed=seed)
    curl_E_errs = []
    curl_B_errs = []
    for d in dirs:
        kx, ky = k_mag * d[0], k_mag * d[1]
        kx_h, ky_h = kx / 2, ky / 2
        psi_p, psi_m, omega_half = weyl_eigenmodes_2d_square(kx_h, ky_h)
        psi = psi_p
        phi = psi_p  # same eigenmode, photon evolves at 2·omega_half
        n_half = n_half_2d(kx_h, ky_h)

        E0, B0 = EM_bilinears(psi, phi, n_half)
        ph = np.exp(-1j * omega_half * dt)
        psi_t = psi * ph
        phi_t = phi * ph
        Et, Bt = EM_bilinears(psi_t, phi_t, n_half)

        dE_dt = (Et - E0) / dt
        dB_dt = (Bt - B0) / dt

        two_n = 2.0 * n_half
        rhs_E = 1j * np.cross(two_n, B0)
        rhs_B = -1j * np.cross(two_n, E0)

        denom = np.linalg.norm(E0) + np.linalg.norm(B0) + 1e-30
        curl_E_errs.append(float(np.linalg.norm(dE_dt - rhs_E) / denom))
        curl_B_errs.append(float(np.linalg.norm(dB_dt - rhs_B) / denom))

    return max(curl_E_errs), max(curl_B_errs)


def maxwell_transversality_2d(k_mag=0.05, n_dirs=8, seed=1):
    """Test 2n_{k/2}·E_G = 0 and 2n_{k/2}·B_G = 0 for the 2D construction."""
    dirs = _random_dirs_2d(n_dirs, seed=seed)
    worst = 0.0
    for d in dirs:
        kx_h, ky_h = k_mag * d[0] / 2, k_mag * d[1] / 2
        psi_p, _, _ = weyl_eigenmodes_2d_square(kx_h, ky_h)
        n_half = n_half_2d(kx_h, ky_h)
        E, B = EM_bilinears(psi_p, psi_p, n_half)
        two_n = 2.0 * n_half
        denom = np.linalg.norm(E) + np.linalg.norm(B) + 1e-30
        worst = max(worst, abs(two_n @ E) / denom)
        worst = max(worst, abs(two_n @ B) / denom)
    return worst


def maxwell_dispersion_residual_2d(k_mag=0.05):
    """Composite-photon dispersion Ω_γ = 2·ω(k/2), expected → |k|/√2 at small k."""
    dirs = _random_dirs_2d(8, seed=2)
    errs = []
    for d in dirs:
        kx, ky = k_mag * d[0], k_mag * d[1]
        _, _, omega_half = weyl_eigenmodes_2d_square(kx / 2, ky / 2)
        Omega = 2.0 * omega_half
        Omega_lin = k_mag / SQRT2
        errs.append(abs(Omega - Omega_lin) / Omega_lin)
    return max(errs)


if __name__ == '__main__':
    print('=== 2D-square composite-photon bilinear ===')
    print(f'  Dispersion residual (k=0.05):   {maxwell_dispersion_residual_2d(0.05):.4e}')
    print(f'  Transversality (k=0.05):        {maxwell_transversality_2d(0.05):.4e}')
    eE, eB = maxwell_curl_residual_2d(0.05)
    print(f'  Curl residual E (k=0.05):       {eE:.4e}  curl/k = {eE/0.05:.6f}')
    print(f'  Curl residual B (k=0.05):       {eB:.4e}  curl/k = {eB/0.05:.6f}')
    print()
    print('Predictions:')
    print(f'  Candidate A (1/√C(4,2) = 1/√6): {1/np.sqrt(6):.6f}')
    print(f'  Candidate B (1/√(2·2) = 1/2):   {0.500000:.6f}')
