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


# ══════════════════════════════════════════════════════════════════
#  F26 — Exact rotation-law EM propagator (2D square lattice)
#
#  Primary law (F25 / F26):
#    Ê(k,t+1) =  cos(Ω) Ê(k,t) + sin(Ω) B̂(k,t)
#    B̂(k,t+1) = -sin(Ω) Ê(k,t) + cos(Ω) B̂(k,t)
#
#  where  Ω(k) = 2 · ω_2D(k/2),   ω_2D(k) = arccos(cos(kx/√2)·cos(ky/√2))
#  c_lat = dΩ/d|k||_{k→0} = 1/√2 for the 2D square QCA.
#
#  Maxwell's curl equations are the k→0 linearisation of this rotation.
# ══════════════════════════════════════════════════════════════════

def rotation_omega_2d(KX, KY):
    """Ω(k) = 2·ω_2D(k/2) on a 2D k-grid (arrays broadcastable).

    ω_2D is the 2D square QCA dispersion: arccos(cos(kx/√2)·cos(ky/√2)).
    c_lat = dΩ/d|k||_{k→0} = 1/√2.
    """
    return 2.0 * exact.exact2d_dispersion(KX / 2.0, KY / 2.0)


def rotation_step_em_spectral_2d(E_field, B_field):
    """Full-lattice exact EM propagator for the 2D square QCA (one tick, Δt=1).

    Implements the exact discrete real rotation (F26):
        Ê(k,t+1) =  cos(Ω) Ê(k,t) + sin(Ω) B̂(k,t)
        B̂(k,t+1) = -sin(Ω) Ê(k,t) + cos(Ω) B̂(k,t)

    Parameters
    ----------
    E_field, B_field : ndarray, shape (Lx, Ly, 3)
        Real (or complex) electromagnetic field arrays on the 2D lattice.

    Returns
    -------
    E_new, B_new : ndarray, shape (Lx, Ly, 3)
    """
    Lx, Ly = E_field.shape[:2]
    kx = np.fft.fftfreq(Lx) * 2.0 * np.pi
    ky = np.fft.fftfreq(Ly) * 2.0 * np.pi
    KX, KY = np.meshgrid(kx, ky, indexing='ij')

    Omega = rotation_omega_2d(KX, KY)           # shape (Lx, Ly)
    cosO  = np.cos(Omega)[..., np.newaxis]       # shape (Lx, Ly, 1)
    sinO  = np.sin(Omega)[..., np.newaxis]

    axes = (0, 1)
    E_k = np.fft.fftn(E_field, axes=axes)
    B_k = np.fft.fftn(B_field, axes=axes)

    E_k_new =  cosO * E_k + sinO * B_k
    B_k_new = -sinO * E_k + cosO * B_k

    E_new = np.fft.ifftn(E_k_new, axes=axes)
    B_new = np.fft.ifftn(B_k_new, axes=axes)

    if np.isrealobj(E_field):
        E_new = E_new.real
    if np.isrealobj(B_field):
        B_new = B_new.real

    return E_new, B_new


def c_from_rotation_rate_2d(eps=1e-5, n_dirs=8, seed=42):
    """Measure c_lat = dΩ/d|k| at |k|→0 for the 2D square QCA.

    Finite-difference Ω(ε·k̂)/ε along n_dirs random directions in the xy plane.
    Expected: c_lat = 1/√2 ≈ 0.70711.

    Returns
    -------
    dict with keys:
        c_measured  — mean of per-direction estimates
        c_analytic  — 1/√2
        residual    — |c_measured - c_analytic|
        per_dir     — list of per-direction estimates
    """
    rng = np.random.default_rng(seed)
    thetas = rng.uniform(0.0, 2.0 * np.pi, n_dirs)
    c_vals = []
    for th in thetas:
        kx = eps * np.cos(th)
        ky = eps * np.sin(th)
        Omega_p = float(rotation_omega_2d(np.array([[kx]]), np.array([[ky]]))[0, 0])
        c_vals.append(Omega_p / eps)

    c_meas = float(np.mean(c_vals))
    c_anal = 1.0 / np.sqrt(2.0)
    return {
        'c_measured': c_meas,
        'c_analytic': c_anal,
        'residual': abs(c_meas - c_anal),
        'per_dir': c_vals,
    }


def rotation_law_consistency_2d(k_mag=0.05, n_dirs=8, n_steps=20, seed=60):
    """Verify the exact rotation law over multiple ticks on live 2D Weyl states.

    For each direction: build a single-k EM state, propagate n_steps ticks using
    the exact rotation, measure the residual vs the rotation prediction.  Also
    computes the Maxwell curl residual for comparison.

    Returns
    -------
    dict with keys:
        max_rot_E   — max rotation-law residual on E  (expect ~2e-16, machine precision)
        max_rot_B   — max rotation-law residual on B
        max_curl_E  — max Maxwell curl residual        (expect ~c_lat·k, O(k) error)
    """
    rng = np.random.default_rng(seed)
    thetas = rng.uniform(0.0, 2.0 * np.pi, n_dirs)

    rot_E_errs = []
    rot_B_errs = []
    curl_E_errs = []

    for th in thetas:
        kx = k_mag * np.cos(th)
        ky = k_mag * np.sin(th)
        kx_h, ky_h = kx / 2.0, ky / 2.0

        psi_p, _, omega_half = weyl_eigenmodes_2d_square(kx_h, ky_h)
        n_half = n_half_2d(kx_h, ky_h)
        E0, B0 = EM_bilinears(psi_p, psi_p, n_half)
        E0, B0 = np.real(E0), np.real(B0)

        Omega = 2.0 * omega_half

        # Propagate n_steps with the Weyl unitary
        psi = psi_p.copy()
        E_prev, B_prev = E0.copy(), B0.copy()

        max_re = 0.0
        max_rb = 0.0
        max_ce = 0.0
        for _ in range(n_steps):
            ph = np.exp(-1j * omega_half)
            psi_next = psi * ph
            n_h = n_half_2d(kx_h, ky_h)
            E_next, B_next = EM_bilinears(psi_next, psi_next, n_h)
            E_next, B_next = np.real(E_next), np.real(B_next)

            # Rotation prediction from (E_prev, B_prev)
            cosO, sinO = np.cos(Omega), np.sin(Omega)
            E_rot =  cosO * E_prev + sinO * B_prev
            B_rot = -sinO * E_prev + cosO * B_prev

            denom = np.linalg.norm(E_prev) + np.linalg.norm(B_prev) + 1e-30
            max_re = max(max_re, np.linalg.norm(E_next - E_rot) / denom)
            max_rb = max(max_rb, np.linalg.norm(B_next - B_rot) / denom)

            # Maxwell curl residual: dE/dt vs curl B
            dE_dt = E_next - E_prev
            two_n = 2.0 * n_half
            rhs_E = np.real(1j * np.cross(two_n, B_prev))
            max_ce = max(max_ce, np.linalg.norm(dE_dt - rhs_E) / denom)

            psi = psi_next
            E_prev, B_prev = E_next, B_next

        rot_E_errs.append(max_re)
        rot_B_errs.append(max_rb)
        curl_E_errs.append(max_ce)

    return {
        'max_rot_E': max(rot_E_errs),
        'max_rot_B': max(rot_B_errs),
        'max_curl_E': max(curl_E_errs),
    }


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
    print()
    print('=== F26 — Exact rotation law (2D) ===')
    cr = c_from_rotation_rate_2d()
    print(f'  c_lat measured:  {cr["c_measured"]:.8f}')
    print(f'  c_lat analytic:  {cr["c_analytic"]:.8f}  (1/√2)')
    print(f'  residual:        {cr["residual"]:.2e}')
    rl = rotation_law_consistency_2d(k_mag=0.05, n_steps=20)
    print(f'  Rotation law residual E: {rl["max_rot_E"]:.3e}  (expect ~2e-16)')
    print(f'  Rotation law residual B: {rl["max_rot_B"]:.3e}  (expect ~2e-16)')
    print(f'  Maxwell curl residual:   {rl["max_curl_E"]:.3e}  (expect ~{0.05/np.sqrt(2):.4f})')
