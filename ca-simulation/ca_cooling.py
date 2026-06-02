"""
ca_cooling.py — SU(3) Wilson gradient flow and cooling driver  (FG-7b, 2026-06-01)
==================================================================================

Closes the open follow-up item flagged in F43 (FG-7) and the
`first-gen-completeness.md` §5.1 FG-7 row:

    "The linear-confinement regime requires real-time link evolution from
     a near-identity start (gradient flow / cooling)."

This module implements the smoothing half of that program: a correctly
implemented Wilson **gradient flow** (Lüscher 2010) and **cooling** on the
2D-square SU(3) link field of `ca_strong.py`.  The confinement *measurement*
(static potential, string tension, Creutz ratio) lives in `ca_confinement.py`;
this module supplies the gauge-covariant smoother those tests cross-check
against.

Wilson gradient flow (continuum):
    d/dt V_μ(x) = Z_μ(V) · V_μ(x),     V_μ(0) = U_μ(x),
    Z_μ(x) = -[ V_μ(x) Σ_μ†(x) ]_TA           (traceless anti-Hermitian part)

where Σ_μ(x) is the sum of the 2(d−1) staples attached to the link.  The flow
is gradient descent on the Wilson action S_W, so
    dS_W/dt = -Σ_{x,μ} ‖Z_μ(x)‖²  ≤  0
— the action is monotonically non-increasing, the cold configuration is a
fixed point, and the flow commutes with gauge transformations.  All four
properties are verified in `model-tests/test_FG7b_gradient_flow.py`.

Conventions match `ca_strong.py`:
    U : ndarray (n_dir=2, Lx, Ly, 3, 3) complex,  U[0]=+x, U[1]=+y links.
    T^a = λ^a/2 (Gell-Mann),  Tr(T^a T^b) = ½ δ^{ab}.

References
----------
  Lüscher, M. (2010) "Properties and uses of the Wilson flow in lattice QCD."
    JHEP 1008:071.
  Wilson, K. (1974) Phys. Rev. D 10, 2445.
  F43 — dynamical SU(3) gluon sector (Wilson-loop primitives).
"""

import numpy as np

import ca_strong as cstr


# ══════════════════════════════════════════════════════════════════
#  Small matrix helpers (per-site batched 3×3)
# ══════════════════════════════════════════════════════════════════

def _mm(A, B):
    """Batched matrix product A·B over trailing 3×3 blocks."""
    return np.einsum('...ij,...jk->...ik', A, B)


def _dag(A):
    """Batched Hermitian conjugate over trailing 3×3 blocks."""
    return np.conj(np.swapaxes(A, -1, -2))


def ta_project(M):
    """
    Traceless anti-Hermitian projection of a batched 3×3 field:

        TA(M) = ½(M − M†) − (1/2N) Tr(M − M†) · I,   N = 3.

    The result lives in the su(3) Lie algebra (anti-Hermitian, traceless).
    """
    A = 0.5 * (M - _dag(M))
    tr = np.trace(A, axis1=-2, axis2=-1)
    eye = np.eye(3, dtype=M.dtype)
    return A - (tr / 3.0)[..., None, None] * eye


def su3_exp_algebra(X):
    """
    Exponentiate a batched anti-Hermitian traceless field X ∈ su(3):
        exp(X),  with X = i H,  H Hermitian  →  exp(iH) via eigh.

    Returns an SU(3) field of the same batch shape.  X=0 → I bit-for-bit.
    """
    H = -1j * X                       # Hermitian
    w, V = np.linalg.eigh(H)          # H = V diag(w) V†
    phase = np.exp(1j * w)            # exp(iH) eigenvalues
    Vd = _dag(V)
    return _mm(V * phase[..., None, :], Vd)


def su3_unitarity_residual(U):
    """max_{μ,x} ‖U U† − I‖_∞ over a 2D link field (n_dir, Lx, Ly, 3, 3)."""
    UUd = _mm(U, _dag(U))
    eye = np.eye(3, dtype=U.dtype)
    return float(np.max(np.abs(UUd - eye)))


def su3_det_residual(U):
    """max_{μ,x} |det U − 1| over a 2D link field."""
    return float(np.max(np.abs(np.linalg.det(U) - 1.0)))


def su3_project(M):
    """
    Project a batched general 3×3 field to the nearest SU(3) matrix.

    Polar/SVD unitarisation  M = W Σ Vh → U = W·Vh, then remove the residual
    determinant phase so det = 1.  Used by cooling (the SU(3) element that
    maximises Re Tr[U Σ†] is the unitary part of the staple Σ).
    """
    W, _, Vh = np.linalg.svd(M)
    U = _mm(W, Vh)
    det = np.linalg.det(U)
    # divide out det^{1/3} (principal cube root) to land in SU(3)
    phase = det ** (1.0 / 3.0)
    return U / phase[..., None, None]


# ══════════════════════════════════════════════════════════════════
#  Staples and the Wilson action on the 2D-square lattice
# ══════════════════════════════════════════════════════════════════

def staple_sum_2d(U):
    """
    Sum of the two staples attached to each link, both directions.

    Returns Sigma : (2, Lx, Ly, 3, 3) complex with
        Σ_μ(x) = Σ⁺_μ(x) + Σ⁻_μ(x)
    such that  Σ_{p∋U_μ(x)} Re Tr U_p = Re Tr[ U_μ(x) Σ_μ†(x) ].
    """
    Ux, Uy = U[0], U[1]

    def rollp(A, ax):   # shift so that result[x] = A[x + ê_ax]
        return np.roll(A, -1, axis=ax)

    def rollm(A, ax):   # shift so that result[x] = A[x − ê_ax]
        return np.roll(A, +1, axis=ax)

    # ---- μ = x (axis 0), plane ν = y (axis 1) ----
    # Σ⁺ = U_y(x) U_x(x+ŷ) U_y†(x+x̂)
    Sx_p = _mm(_mm(Uy, rollp(Ux, 1)), _dag(rollp(Uy, 0)))
    # Σ⁻ = U_y†(x−ŷ) U_x(x−ŷ) U_y(x+x̂−ŷ)
    Uy_xm_y = rollm(rollp(Uy, 0), 1)         # U_y(x + x̂ − ŷ)
    Sx_m = _mm(_mm(_dag(rollm(Uy, 1)), rollm(Ux, 1)), Uy_xm_y)
    Sx = Sx_p + Sx_m

    # ---- μ = y (axis 1), plane ν = x (axis 0) ----
    # Σ⁺ = U_x(x) U_y(x+x̂) U_x†(x+ŷ)
    Sy_p = _mm(_mm(Ux, rollp(Uy, 0)), _dag(rollp(Ux, 1)))
    # Σ⁻ = U_x†(x−x̂) U_y(x−x̂) U_x(x+ŷ−x̂)
    Ux_ym_x = rollm(rollp(Ux, 1), 0)         # U_x(x + ŷ − x̂)
    Sy_m = _mm(_mm(_dag(rollm(Ux, 0)), rollm(Uy, 0)), Ux_ym_x)
    Sy = Sy_p + Sy_m

    return np.stack([Sx, Sy], axis=0)


def mean_plaquette_2d(U):
    """⟨(1/N) Re Tr U_□⟩ averaged over all plaquettes (N=3)."""
    P = cstr.plaquette_trace(U, mu=0, nu=1)
    return float(np.mean(np.real(P)) / 3.0)


def wilson_action_2d(U, beta=1.0):
    """Wilson action S = β Σ_□ (1 − (1/N) Re Tr U_□)  (single xy plane)."""
    P = cstr.plaquette_trace(U, mu=0, nu=1)
    return float(beta * np.sum(1.0 - np.real(P) / 3.0))


# ══════════════════════════════════════════════════════════════════
#  Wilson gradient flow
# ══════════════════════════════════════════════════════════════════

def wilson_flow_force_2d(U):
    """
    Flow force Z_μ(x) = −[ U_μ(x) Σ_μ†(x) ]_TA   for both directions.

    Returns Z : (2, Lx, Ly, 3, 3) anti-Hermitian traceless (∈ su(3)).
    Cold links (Σ_μ = 2·I, U_μ = I) → U Σ† = 2I → TA(2I) = 0 bit-for-bit.
    """
    Sigma = staple_sum_2d(U)
    Z = np.empty_like(U)
    for mu in range(2):
        Omega = _mm(U[mu], _dag(Sigma[mu]))
        Z[mu] = -ta_project(Omega)
    return Z


def wilson_flow_step_euler_2d(U, eps=0.01):
    """
    One explicit-Euler Wilson-flow step of size eps:
        U_μ(x) ← exp(eps · Z_μ(x)) · U_μ(x).
    """
    Z = wilson_flow_force_2d(U)
    U_new = np.empty_like(U)
    for mu in range(2):
        U_new[mu] = _mm(su3_exp_algebra(eps * Z[mu]), U[mu])
    return U_new


def wilson_flow_step_rk3_2d(U, eps=0.05):
    """
    One Lüscher (2010) 3-stage Runge–Kutta Wilson-flow step.  Third-order
    accurate in eps; the canonical 'correct' integrator for the Wilson flow.

        W0 = U
        W1 = exp(¼ Z0)               W0
        W2 = exp(8/9 Z1 − 17/36 Z0)  W1
        W3 = exp(¾ Z2 − 8/9 Z1 + 17/36 Z0)  W2
    with Zi = eps · Z(Wi).
    """
    def force(V):
        return eps * wilson_flow_force_2d(V)

    W0 = U
    Z0 = force(W0)
    W1 = np.empty_like(U)
    for mu in range(2):
        W1[mu] = _mm(su3_exp_algebra(0.25 * Z0[mu]), W0[mu])
    Z1 = force(W1)
    W2 = np.empty_like(U)
    for mu in range(2):
        arg = (8.0 / 9.0) * Z1[mu] - (17.0 / 36.0) * Z0[mu]
        W2[mu] = _mm(su3_exp_algebra(arg), W1[mu])
    Z2 = force(W2)
    W3 = np.empty_like(U)
    for mu in range(2):
        arg = (3.0 / 4.0) * Z2[mu] - (8.0 / 9.0) * Z1[mu] + (17.0 / 36.0) * Z0[mu]
        W3[mu] = _mm(su3_exp_algebra(arg), W2[mu])
    return W3


def run_wilson_flow_2d(U, eps=0.05, n_steps=20, integrator='rk3', record=True):
    """
    Integrate the Wilson flow for n_steps and (optionally) record the
    action history.  Returns (U_flowed, history) where history is a list of
    (flow_time, wilson_action, mean_plaquette) tuples (empty if record=False).
    """
    step = wilson_flow_step_rk3_2d if integrator == 'rk3' else wilson_flow_step_euler_2d
    hist = []
    if record:
        hist.append((0.0, wilson_action_2d(U), mean_plaquette_2d(U)))
    V = U
    for n in range(n_steps):
        V = step(V, eps)
        if record:
            hist.append(((n + 1) * eps, wilson_action_2d(V), mean_plaquette_2d(V)))
    return V, hist


# ══════════════════════════════════════════════════════════════════
#  Cooling (checkerboard, maximises local action per link)
# ══════════════════════════════════════════════════════════════════

def cooling_step_2d(U):
    """
    One checkerboard cooling sweep.  For each site parity and each direction,
    replace U_μ(x) by the SU(3) projection of its current staple sum Σ_μ(x)
    — the SU(3) element that maximises Re Tr[U_μ Σ_μ†], i.e. locally minimises
    the Wilson action.  Neighbour staples are recomputed between sub-sweeps so
    even/odd updates stay consistent.

    Cooling is the ε→∞ (infinite-step) limit of the flow per link; it removes
    short-range disorder fastest but, like the flow, leaves the cold config
    invariant and reduces the action monotonically.
    """
    Lx, Ly = U.shape[1:3]
    ix = np.arange(Lx)[:, None]
    iy = np.arange(Ly)[None, :]
    parity = (ix + iy) % 2                      # (Lx, Ly) checkerboard mask
    Uc = U.copy()
    for par in (0, 1):
        mask = (parity == par)
        for mu in range(2):
            Sigma = staple_sum_2d(Uc)[mu]       # recompute with latest links
            proj = su3_project(Sigma)
            Uc[mu][mask] = proj[mask]
    return Uc


def run_cooling_2d(U, n_steps=20, record=True):
    """Apply n_steps cooling sweeps; return (U_cooled, history) like the flow."""
    hist = []
    if record:
        hist.append((0, wilson_action_2d(U), mean_plaquette_2d(U)))
    V = U.copy()
    for n in range(n_steps):
        V = cooling_step_2d(V)
        if record:
            hist.append((n + 1, wilson_action_2d(V), mean_plaquette_2d(V)))
    return V, hist


# ══════════════════════════════════════════════════════════════════
#  Configuration builders
# ══════════════════════════════════════════════════════════════════

def near_identity_links_2d(shape, eps=0.1, seed=7):
    """
    Cold lattice perturbed by exp(i ε θ^a T^a) with small Gaussian θ — a
    near-identity start for the smoothing / diffusion tests.
    """
    rng = np.random.default_rng(seed=seed)
    Lx, Ly = shape
    U = np.zeros((2, Lx, Ly, 3, 3), dtype=complex)
    for mu in range(2):
        theta = eps * rng.standard_normal((Lx, Ly, 8))
        H = np.einsum('xya,aij->xyij', theta, cstr.T_GEN)
        U[mu] = su3_exp_algebra(1j * H)        # exp(i H)
    return U


def hot_links_2d(shape, seed=11):
    """Haar-random SU(3) on every link (fully disordered, β→0 ensemble member)."""
    return cstr.random_su3_links_2d(shape, rng=np.random.default_rng(seed=seed))
