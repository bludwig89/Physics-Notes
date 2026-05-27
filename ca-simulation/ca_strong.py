"""
ca_strong.py  —  SU(3)_color strong-force gauge sector  (Phase E3)
==================================================================
Link-variable lattice SU(3) acting on a three-flavour (u, d, s)
colour-triplet Dirac quark field.  Implements the design in
`reference-research/ca-strong-design.md` (2026-05-21).

State per cell
--------------
    Quark field q^{f,c}(x) = (eta_up, eta_dn, chi_up, chi_dn)
      flavour f ∈ {u, d, s}      (3)
      colour  c ∈ {r, g, b}      (3)
      Dirac   d ∈ {η↑, η↓, χ↑, χ↓}  (4)
    Total: 36 complex per cell.

    Link field U_μ(x) ∈ SU(3) for each forward direction μ.
    In 2D square: 2 link directions, so 2 × (3×3) = 18 complex per cell.

Gauge transformation (local SU(3)):
    q(x)      →  V(x) q(x)
    U_μ(x)    →  V(x) U_μ(x) V†(x+μ̂)

The covariant lattice derivative D_μ q(x) = U_μ(x) q(x+μ̂) − q(x)
rotates as V(x) D_μ q(x) — covariant.

Test gate V13 (Noether current conservation).  See `ca-strong-design.md` §6.
The colour current  J^a_μ = q̄ γ_μ T^a q,  with T^a = λ^a / 2,  is locally
conserved on the lattice.  This module exposes:

  noether_charge_density(q)              → J^a_0(x) at every cell, every a
  noether_charge_total(q)                → Q^a = Σ_x J^a_0(x)
  lattice_4divergence(J0, J1, J2)        → (∂_μ J^a_μ)(x) by central differences
  adjoint_rotation(V)                    → 8×8 V^{ab}_{adj} = 2 Tr(T^a V T^b V†)

Coexistence with the rest of v2
-------------------------------
  - Cold links (U_μ ≡ I) ⇒ the quark kinetic step reduces *bit-for-bit*
    to three independent copies of the existing colourless Dirac step
    from `ca_dirac.py` (one per colour, per flavour).
  - The link-multiplication step is the only colour-mixing operator in
    the cold-link → frozen-link → dynamical-gluon chain.
  - V13 freezes the links; V15 (future) adds the Kogut-Susskind link
    update.  No change to `ca_dirac.py`, `ca_weak.py`, `ca_maxwell.py`,
    `ca_higgs.py`, `ca_curved.py`, or `ca_emqg.py` is required.

References
----------
  `reference-research/ca-strong-design.md` (the full design)
  Wilson, K. (1974) "Confinement of quarks." Phys. Rev. D 10, 2445.
  Kogut, J. & Susskind, L. (1975) "Hamiltonian formulation of Wilson's
  lattice gauge theories." Phys. Rev. D 11, 395.
"""

import numpy as np

import ca_dirac as cdir


# ══════════════════════════════════════════════════════════════════
#  Gell-Mann generators of SU(3)
# ══════════════════════════════════════════════════════════════════

SQRT3 = np.sqrt(3.0)

# λ^1 … λ^8 in the standard order (Gell-Mann 1962).
_LAMBDA = np.zeros((8, 3, 3), dtype=complex)
_LAMBDA[0] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
_LAMBDA[1] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
_LAMBDA[2] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
_LAMBDA[3] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
_LAMBDA[4] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
_LAMBDA[5] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
_LAMBDA[6] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
_LAMBDA[7] = (1.0 / SQRT3) * np.array(
    [[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex
)

# T^a = λ^a / 2  with  Tr(T^a T^b) = ½ δ^{ab}.
T_GEN = _LAMBDA / 2.0
N_GEN = 8


def gell_mann(a):
    """Return λ^a, 1 ≤ a ≤ 8 (one-indexed for readability)."""
    if not 1 <= a <= 8:
        raise ValueError(f"Gell-Mann index a must be in 1..8 (got {a})")
    return _LAMBDA[a - 1].copy()


def T(a):
    """Return T^a = λ^a / 2, 1 ≤ a ≤ 8."""
    if not 1 <= a <= 8:
        raise ValueError(f"Generator index a must be in 1..8 (got {a})")
    return T_GEN[a - 1].copy()


def verify_normalization():
    """Tr(T^a T^b) = ½ δ^{ab}.  Returns max residual."""
    M = np.zeros((N_GEN, N_GEN), dtype=complex)
    for a in range(N_GEN):
        for b in range(N_GEN):
            M[a, b] = np.trace(T_GEN[a] @ T_GEN[b])
    return float(np.max(np.abs(M - 0.5 * np.eye(N_GEN))))


# ══════════════════════════════════════════════════════════════════
#  SU(3) exponential and Haar-random sampling
# ══════════════════════════════════════════════════════════════════

def su3_exp(theta):
    """
    Build V = exp(i Σ_a θ^a T^a) ∈ SU(3) from 8 real angles θ.

    Uses NumPy's Hermitian eigendecomposition: for H = Σ θ^a T^a
    (Hermitian by construction since the T^a are Hermitian and θ is
    real), write H = U diag(λ) U†, then exp(iH) = U diag(e^{iλ}) U†.
    Unitary by construction; bit-for-bit close to I for small θ.
    """
    theta = np.asarray(theta, dtype=float)
    if theta.shape != (8,):
        raise ValueError(f"theta must have shape (8,), got {theta.shape}")
    H = sum(theta[a] * T_GEN[a] for a in range(N_GEN))
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T


def su3_haar(rng=None):
    """
    Draw one Haar-random SU(3) matrix.

    Recipe: draw Z = (A + iB) / √2 with A, B real-Gaussian N(0,1) 3×3;
    QR-decompose Z = Q R; rephase Q so that det Q = 1.  This is the
    standard QR-based Haar recipe restricted to SU(N).
    """
    if rng is None:
        rng = np.random.default_rng()
    A = rng.normal(size=(3, 3))
    B = rng.normal(size=(3, 3))
    Z = (A + 1j * B) / np.sqrt(2.0)
    Q, R = np.linalg.qr(Z)
    # Mezzadri (2007) fix-up: enforce uniform measure.
    diagR = np.diag(R)
    phase = diagR / np.abs(diagR)
    Q = Q * phase[np.newaxis, :]
    # Now Q is Haar-U(3).  Project to SU(3) by removing the overall det phase.
    det = np.linalg.det(Q)
    Q = Q * np.conj(det) ** (1.0 / 3.0)
    return Q


def is_su3(U, tol=1e-12):
    """Check that U is in SU(3): U U† = I and det U = 1."""
    U = np.asarray(U, dtype=complex)
    err_unitary = np.max(np.abs(U @ U.conj().T - np.eye(3)))
    err_det = abs(np.linalg.det(U) - 1.0)
    return (err_unitary < tol) and (err_det < tol)


# ══════════════════════════════════════════════════════════════════
#  Quark state container
# ══════════════════════════════════════════════════════════════════

FLAVOURS = ('u', 'd', 's')
COLOURS = ('r', 'g', 'b')
DIRAC = ('eu', 'ed', 'cu', 'cd')   # η_↑, η_↓, χ_↑, χ_↓


# yukawa_mass_field was REMOVED 2026-05-26 together with the
# Higgs-driven per-cell mass field. The adopted quark mass mechanism
# is now the F27 chiral-SU(2) complex mass via `quark_mass_step_f27` /
# `step_strong_2d_complex_mass` (see F40 / FG-2). The variable-mass
# Dirac primitive `dirac_step_2d_varm_complex_splitstep` in ca_dirac.py
# remains available for any future per-cell mass usage (e.g. Klein-
# paradox-style mass barriers) but is no longer wired to a Higgs Φ
# field at the quark-sector level.


def zero_quark_field(shape, dtype=complex):
    """
    Allocate a zero quark field with shape (Lx, Ly).

    Returns a dict[(flavour, colour, dirac)] → ndarray(shape) of zeros.
    """
    out = {}
    z = np.zeros(shape, dtype=dtype)
    for f in FLAVOURS:
        for c in COLOURS:
            for d in DIRAC:
                out[(f, c, d)] = z.copy()
    return out


def quark_norm(q):
    """Total probability norm Σ |q^{f,c,d}(x)|²."""
    return float(sum(np.sum(np.abs(v) ** 2) for v in q.values()))


def gaussian_quark(shape, flavour='u', colour='r', sigma=4.0, center=None,
                   chirality='left'):
    """
    Single Gaussian packet in one (flavour, colour) channel.

    chirality='left'  → η_↑ = G, others 0  (pure left-handed quark)
    chirality='right' → χ_↑ = G            (pure right-handed quark)
    """
    Lx, Ly = shape
    cx, cy = center if center is not None else (Lx // 2, Ly // 2)
    x = np.arange(Lx) - cx
    y = np.arange(Ly) - cy
    X, Y = np.meshgrid(x, y, indexing='ij')
    G = np.exp(-(X ** 2 + Y ** 2) / (2.0 * sigma ** 2)).astype(complex)

    q = zero_quark_field(shape)
    if chirality == 'left':
        q[(flavour, colour, 'eu')] = G
    elif chirality == 'right':
        q[(flavour, colour, 'cu')] = G
    else:
        raise ValueError(f"chirality must be 'left' or 'right', got {chirality}")
    return q


# Per-cell colour-3 view -------------------------------------------------------

def _colour_triplet(q, f, d):
    """
    Return a (Lx, Ly, 3) complex array stacking the colour components of
    flavour f, Dirac component d.  Order is (r, g, b).
    """
    return np.stack([q[(f, c, d)] for c in COLOURS], axis=-1)


def _set_colour_triplet(q, f, d, triplet):
    """Inverse of _colour_triplet: write the (Lx, Ly, 3) array back."""
    for i, c in enumerate(COLOURS):
        q[(f, c, d)] = triplet[..., i].copy()


# ══════════════════════════════════════════════════════════════════
#  Link variables and gauge transforms
# ══════════════════════════════════════════════════════════════════

def cold_links_2d(shape):
    """
    Cold-start link field on 2D square lattice.

    Returns U with shape (n_dir=2, Lx, Ly, 3, 3) where U[0] is +x link,
    U[1] is +y link.  Every link is the identity in SU(3).
    """
    Lx, Ly = shape
    U = np.zeros((2, Lx, Ly, 3, 3), dtype=complex)
    U[..., 0, 0] = 1.0
    U[..., 1, 1] = 1.0
    U[..., 2, 2] = 1.0
    return U


def random_su3_links_2d(shape, rng=None):
    """Independent Haar-random SU(3) on every link of the 2D square lattice."""
    if rng is None:
        rng = np.random.default_rng()
    Lx, Ly = shape
    U = np.zeros((2, Lx, Ly, 3, 3), dtype=complex)
    for mu in range(2):
        for i in range(Lx):
            for j in range(Ly):
                U[mu, i, j] = su3_haar(rng)
    return U


def gauge_transform_quark(q, Vfield):
    """
    Apply local SU(3) gauge transformation q(x) → V(x) q(x).

    Vfield: complex ndarray of shape (Lx, Ly, 3, 3).
    Acts identically on every flavour and every Dirac component.
    """
    q_out = {}
    for f in FLAVOURS:
        for d in DIRAC:
            triplet = _colour_triplet(q, f, d)            # (Lx, Ly, 3)
            rotated = np.einsum('xyij,xyj->xyi', Vfield, triplet)
            for i, c in enumerate(COLOURS):
                q_out[(f, c, d)] = rotated[..., i]
    return q_out


def gauge_transform_links(U, Vfield):
    """
    Apply local SU(3) gauge transformation
      U_μ(x) → V(x) U_μ(x) V†(x+μ̂)
    """
    Lx, Ly = Vfield.shape[:2]
    U_out = np.empty_like(U)
    Vdag = np.conj(np.transpose(Vfield, (0, 1, 3, 2)))   # V†(x)

    # μ = +x: shift V† by +x to get V†(x + x̂)
    Vdag_shift_x = np.roll(Vdag, -1, axis=0)
    Vdag_shift_y = np.roll(Vdag, -1, axis=1)
    U_out[0] = np.einsum('xyij,xyjk,xykl->xyil', Vfield, U[0], Vdag_shift_x)
    U_out[1] = np.einsum('xyij,xyjk,xykl->xyil', Vfield, U[1], Vdag_shift_y)
    return U_out


# ══════════════════════════════════════════════════════════════════
#  Parallel transport on a quark field
# ══════════════════════════════════════════════════════════════════

def parallel_transport(q, U):
    """
    Half-step covariant kinetic transport — apply the link variables.

    For cold links (U_μ ≡ I) this is the identity.  For general U_μ it
    rotates the colour triplet of every (flavour, Dirac component) at
    every cell by an O(1) SU(3) phase determined by the local link.

    This is the operator that distinguishes the gauge-invariant
    parallel-transported quark step from the colour-blind Dirac step.
    The shift / FFT kinetic step itself is unchanged.

    Strang convention: this routine multiplies q(x) by an x-dependent
    SU(3) matrix that is the half-step's symmetric average of the
    forward link rotations.  In the cold-link limit it reduces to the
    identity, and the V13a regression contract holds bit-for-bit.
    """
    # For V13 the link multiplication is folded into the kinetic step
    # via covariant shifts.  See covariant_shift below.  This standalone
    # routine is the diagnostic / per-cell action; in the V13a cold-link
    # regression it must be the identity.
    Vfield = np.zeros(U.shape[1:], dtype=complex)
    # Build V(x) = symmetric Hermitianised average of forward links.
    # For cold links this is exactly I.
    n_dir = U.shape[0]
    for mu in range(n_dir):
        Vfield += U[mu]
    Vfield /= n_dir
    # Project to nearest unitary by polar decomposition (gauge-invariant).
    # For cold links the average is already I, so the projection is exact.
    # For random non-cold links we do a per-cell polar projection.
    Lx, Ly = Vfield.shape[:2]
    Vfield_proj = np.empty_like(Vfield)
    for i in range(Lx):
        for j in range(Ly):
            X = Vfield[i, j]
            U_, _, Vh = np.linalg.svd(X)
            Vfield_proj[i, j] = U_ @ Vh
    return gauge_transform_quark(q, Vfield_proj)


def covariant_shift(q, U, mu, direction='+'):
    """
    Parallel-transported shift  q(x) ← U_μ(x) q(x+μ̂)   (direction='+')
                  or            q(x) ← U_{-μ}(x) q(x-μ̂) (direction='-')

    where U_{-μ}(x) = U_μ†(x - μ̂).  Used inside the covariant
    kinetic step.

    For cold links this is exactly the colourless shift on each
    colour copy independently — the V13a regression statement.
    """
    if direction == '+':
        shift_axis = mu
        roll = -1
        Ulink = U[mu]                                  # U_μ(x)
    elif direction == '-':
        shift_axis = mu
        roll = +1
        # U_{-μ}(x) = U_μ†(x - μ̂)
        Ulink = np.conj(np.transpose(np.roll(U[mu], +1, axis=mu),
                                     (0, 1, 3, 2)))
    else:
        raise ValueError("direction must be '+' or '-'")

    q_out = {}
    for f in FLAVOURS:
        for d in DIRAC:
            triplet = _colour_triplet(q, f, d)         # (Lx, Ly, 3)
            shifted = np.roll(triplet, roll, axis=shift_axis)
            transported = np.einsum('xyij,xyj->xyi', Ulink, shifted)
            for i, c in enumerate(COLOURS):
                q_out[(f, c, d)] = transported[..., i]
    return q_out


# ══════════════════════════════════════════════════════════════════
#  Strong-sector stepper (cold and frozen-link cases)
# ══════════════════════════════════════════════════════════════════

def step_strong_2d(q, U, m_flavour=None, dt=1.0):
    """
    One full strong-sector tick on a 3-flavour, 3-colour quark field.

    Parameters
    ----------
    q : dict from `zero_quark_field` / `gaussian_quark`
    U : link field of shape (2, Lx, Ly, 3, 3)
    m_flavour : dict {flavour: m_q}  with |m_q| ≤ 1 (QCA admissibility).
        Default: massless ({'u': 0, 'd': 0, 's': 0}).
    dt : time step, passed straight through to the Dirac stepper.

    Algorithm (Strang-symmetric, cold-link reducible):

        1. Half-step parallel transport: q → P_½ q with P_½ from link avg.
        2. Kinetic step on each (flavour, colour) copy:
                (η, χ) ← dirac_step_2d_splitstep(η, χ, m = m_flavour[f])
        3. Half-step parallel transport again.

    Cold-link limit (U_μ ≡ I): step 1 and step 3 are the identity; the
    result is bit-for-bit 9 independent (per-flavour, per-colour) Dirac
    steps. This is the V13a regression contract.

    Note: this is the *frozen-link* stepper — the links do NOT update.
    Dynamical gluons live in V15 (separate routine).

    History — Higgs–Yukawa path removed 2026-05-26
    -----------------------------------------------
    The `phi_field` / `yukawa` per-cell-mass branch that previously
    sat inside this function was retired in the F40/F41 cleanup. The
    project's adopted quark mass mechanism is now Ludwig's F27 chiral
    complex mass via `quark_mass_step_f27` / `step_strong_2d_complex_mass`
    (see F40 / FG-2). For any test that needs a position-dependent
    mass profile (e.g. a Klein-paradox-style mass barrier), call the
    primitive `cdir.dirac_step_2d_varm_complex_splitstep` directly.
    """
    if m_flavour is None:
        m_flavour = {'u': 0.0, 'd': 0.0, 's': 0.0}

    # ── Half-step parallel transport ───────────────────────────────
    q = parallel_transport(q, U)

    # ── Kinetic step on each (flavour, colour) copy ────────────────
    for f in FLAVOURS:
        m = m_flavour.get(f, 0.0)
        for c in COLOURS:
            eu = q[(f, c, 'eu')]
            ed = q[(f, c, 'ed')]
            cu = q[(f, c, 'cu')]
            cd = q[(f, c, 'cd')]
            eu_n, ed_n, cu_n, cd_n = cdir.dirac_step_2d_splitstep(
                eu, ed, cu, cd, m=m, dt=dt
            )
            q[(f, c, 'eu')] = eu_n
            q[(f, c, 'ed')] = ed_n
            q[(f, c, 'cu')] = cu_n
            q[(f, c, 'cd')] = cd_n

    # ── Second half-step parallel transport ────────────────────────
    q = parallel_transport(q, U)
    return q


# ══════════════════════════════════════════════════════════════════
#  Colour current  J^a_μ = q̄ γ_μ T^a q
# ══════════════════════════════════════════════════════════════════

def _quark_color_matrix(q, f, d):
    """
    Build a (Lx, Ly, 3) array of the colour vector for flavour f, Dirac d.
    Equivalent to _colour_triplet — exposed under a separate name for
    clarity in current expressions.
    """
    return _colour_triplet(q, f, d)


def noether_charge_density(q):
    """
    Compute the colour-current time-component  J^a_0(x) = q†(x) T^a q(x).

    Sum is over flavour and Dirac components (the trivial direct-sum
    on which T^a acts as I).

    Returns a (8, Lx, Ly) real ndarray.  J^a_0 is real because T^a is
    Hermitian.
    """
    sample = next(iter(q.values()))
    Lx, Ly = sample.shape
    J0 = np.zeros((N_GEN, Lx, Ly), dtype=complex)

    for f in FLAVOURS:
        for d in DIRAC:
            triplet = _colour_triplet(q, f, d)                   # (Lx, Ly, 3)
            for a in range(N_GEN):
                # q† T^a q  contracted over the colour index
                Tq = np.einsum('ij,xyj->xyi', T_GEN[a], triplet)
                J0[a] += np.sum(np.conj(triplet) * Tq, axis=-1)
    # Hermiticity of T^a ⇒ J^a_0 is real up to round-off.
    return np.real(J0)


def noether_charge_total(q):
    """Q^a = Σ_x J^a_0(x).  Returns a length-8 real ndarray."""
    J0 = noether_charge_density(q)
    return np.sum(J0, axis=(1, 2))


def noether_current_spatial(q):
    """
    Spatial colour-current components  J^a_i(x) = q† α_i T^a q  for i ∈ {x, y},
    where α_i are the Dirac alpha matrices in the chiral (Weyl)
    representation:
        α_x = σ_x ⊗ τ_3,    α_y = σ_y ⊗ τ_3
    on the 4-spinor (η_↑, η_↓, χ_↑, χ_↓).
    Concretely:
        α_x mixes η_↑ ↔ η_↓ (with a sign on the χ block)
        α_y mixes η_↑ ↔ η_↓ with an i

    Returns a (2, 8, Lx, Ly) real ndarray  J[mu, a, :, :].
    The chirality sign ensures the spatial current is real.
    """
    sample = next(iter(q.values()))
    Lx, Ly = sample.shape
    Jspat = np.zeros((2, N_GEN, Lx, Ly), dtype=complex)

    # α_x: in the chiral Weyl representation,
    #   α_x = diag(σ_x, -σ_x) acting on (η_↑, η_↓, χ_↑, χ_↓)
    # i.e. η_↑ ↔ η_↓ swap, χ_↑ ↔ -χ_↓ swap.
    # α_y: η_↑ ↔ -i η_↓ (+); χ_↑ ↔ +i χ_↓ (-).
    for f in FLAVOURS:
        eu = _colour_triplet(q, f, 'eu')
        ed = _colour_triplet(q, f, 'ed')
        cu = _colour_triplet(q, f, 'cu')
        cd = _colour_triplet(q, f, 'cd')

        # α_x q: (ed, eu, -cd, -cu)
        ax_eu, ax_ed, ax_cu, ax_cd = ed, eu, -cd, -cu
        # α_y q: (-i ed, i eu, +i cd, -i cu)
        ay_eu = -1j * ed
        ay_ed = +1j * eu
        ay_cu = +1j * cd
        ay_cd = -1j * cu

        # Build α_x q and α_y q as 4 colour-triplets; then contract
        # with q† T^a for each generator.
        for a in range(N_GEN):
            T_eu = np.einsum('ij,xyj->xyi', T_GEN[a], ax_eu)
            T_ed = np.einsum('ij,xyj->xyi', T_GEN[a], ax_ed)
            T_cu = np.einsum('ij,xyj->xyi', T_GEN[a], ax_cu)
            T_cd = np.einsum('ij,xyj->xyi', T_GEN[a], ax_cd)
            Jspat[0, a] += (
                np.sum(np.conj(eu) * T_eu, axis=-1)
                + np.sum(np.conj(ed) * T_ed, axis=-1)
                + np.sum(np.conj(cu) * T_cu, axis=-1)
                + np.sum(np.conj(cd) * T_cd, axis=-1)
            )
            Ty_eu = np.einsum('ij,xyj->xyi', T_GEN[a], ay_eu)
            Ty_ed = np.einsum('ij,xyj->xyi', T_GEN[a], ay_ed)
            Ty_cu = np.einsum('ij,xyj->xyi', T_GEN[a], ay_cu)
            Ty_cd = np.einsum('ij,xyj->xyi', T_GEN[a], ay_cd)
            Jspat[1, a] += (
                np.sum(np.conj(eu) * Ty_eu, axis=-1)
                + np.sum(np.conj(ed) * Ty_ed, axis=-1)
                + np.sum(np.conj(cu) * Ty_cu, axis=-1)
                + np.sum(np.conj(cd) * Ty_cd, axis=-1)
            )
    return np.real(Jspat)


def lattice_3divergence(J0_t_minus, J0_t_plus, Jspat, dt=1.0):
    """
    Central-difference lattice 4-divergence:

      (∂_μ J^a_μ)(x) ≈ (J^a_0(x, t+dt) − J^a_0(x, t-dt)) / (2 dt)
                   + Σ_i (J^a_i(x+î) − J^a_i(x-î)) / 2

    Parameters
    ----------
    J0_t_minus : (8, Lx, Ly)  current density at time t - dt
    J0_t_plus  : (8, Lx, Ly)  current density at time t + dt
    Jspat      : (2, 8, Lx, Ly) spatial currents at time t
    dt         : time step

    Returns (8, Lx, Ly) residual.  In the free (cold-link) limit this is
    bounded by the FFT round-off floor of the kinetic step.
    """
    time_deriv = (J0_t_plus - J0_t_minus) / (2.0 * dt)
    div_x = (np.roll(Jspat[0], -1, axis=1) - np.roll(Jspat[0], +1, axis=1)) / 2.0
    div_y = (np.roll(Jspat[1], -1, axis=2) - np.roll(Jspat[1], +1, axis=2)) / 2.0
    return time_deriv + div_x + div_y


# ══════════════════════════════════════════════════════════════════
#  Adjoint representation
# ══════════════════════════════════════════════════════════════════

def adjoint_rotation(V):
    """
    Compute the 8×8 adjoint matrix
        V^{ab}_{adj} = 2 Tr(T^a V T^b V†)
    so that  Q^a → V^{ab}_{adj} Q^b  under  q → V q.

    Useful for testing global gauge invariance:
       Q'(after q → V q) ?= V_adj @ Q.
    """
    V = np.asarray(V, dtype=complex)
    Vdag = V.conj().T
    Vadj = np.zeros((N_GEN, N_GEN), dtype=float)
    for a in range(N_GEN):
        TaV = T_GEN[a] @ V
        for b in range(N_GEN):
            Vadj[a, b] = 2.0 * np.real(np.trace(TaV @ T_GEN[b] @ Vdag))
    return Vadj


# ══════════════════════════════════════════════════════════════════
#  Wilson plaquette (for V15; provided here as a diagnostic)
# ══════════════════════════════════════════════════════════════════

def plaquette_trace(U, mu=0, nu=1):
    """
    Tr U_□_{μν}(x) for every cell x on the 2D square lattice.
    Returns a (Lx, Ly) complex array.
    """
    Umu = U[mu]                               # U_μ(x)
    Unu_shift = np.roll(U[nu], -1, axis=mu)   # U_ν(x + μ̂)
    Umu_shift_nu = np.roll(U[mu], -1, axis=nu) # U_μ(x + ν̂)
    Unu = U[nu]                               # U_ν(x)
    Umu_shift_nu_dag = np.conj(np.transpose(Umu_shift_nu, (0, 1, 3, 2)))
    Unu_dag = np.conj(np.transpose(Unu, (0, 1, 3, 2)))
    Uplaq = np.einsum('xyij,xyjk,xykl,xylm->xyim',
                       Umu, Unu_shift, Umu_shift_nu_dag, Unu_dag)
    return np.trace(Uplaq, axis1=2, axis2=3)


def wilson_action(U, beta_s=6.0, n_c=3):
    """
    Wilson plaquette action  S_g = β_s Σ_□ (1 − (1/N_c) Re Tr U_□).
    Returns a real scalar (sum over all plaquettes and direction pairs).
    """
    n_dir = U.shape[0]
    S = 0.0
    for mu in range(n_dir):
        for nu in range(mu + 1, n_dir):
            P = plaquette_trace(U, mu=mu, nu=nu)
            S += np.sum(1.0 - np.real(P) / n_c)
    return float(beta_s * S)


# ══════════════════════════════════════════════════════════════════
#  F27 complex-mass adoption for the quark sector
#  (added 2026-05-26; mirrors the F27 lepton structure in ca_dirac.py)
# ══════════════════════════════════════════════════════════════════
#
# Motivation (from first-gen-completeness-review.md §2.1 / §3 item 2):
# the project's adopted mass mechanism is Ludwig's chiral-SU(2) complex
# mass (F27 / Kunimasa–Goto Stueckelberg), but `step_strong_2d` still
# carries the Higgs–Yukawa path through `dirac_step_2d_varm_complex_splitstep`.
# This section adds the F27 mass mechanism per flavour, per colour, with
# natural up/down/strange mass splitting via per-flavour m_f and θ_f(x).
#
# Public API
# ----------
#   chirality_split_quark(q, flavour=None)
#   make_theta_field_quark(shape, mode='zero', seed=42)
#   quark_mass_step_f27(q, theta_flavour, m_flavour, dt=1.0)
#   step_strong_2d_complex_mass(q, U, theta_flavour=None, m_flavour=None, dt=1.0)
#   quark_u1_gauge_transform_f27(q, phi_chi, flavour)
#   quark_doublet_mass_step_su2(q, U_a, U_b, m_doublet, dt=1.0)
#   quark_doublet_su2_transform_chiral(q, V_a, V_b, U_a, U_b)


def chirality_split_quark(q, flavour=None):
    """
    Return (N_L, N_R) total probability in each chirality sector.

    If `flavour` is given, restrict the sum to that flavour. Otherwise
    sum over all flavours and colours.

    η ↔ left-handed = (eu, ed); χ ↔ right-handed = (cu, cd).
    """
    flavours = (flavour,) if flavour is not None else FLAVOURS
    N_L = 0.0
    N_R = 0.0
    for f in flavours:
        for c in COLOURS:
            N_L += float(np.sum(np.abs(q[(f, c, 'eu')]) ** 2))
            N_L += float(np.sum(np.abs(q[(f, c, 'ed')]) ** 2))
            N_R += float(np.sum(np.abs(q[(f, c, 'cu')]) ** 2))
            N_R += float(np.sum(np.abs(q[(f, c, 'cd')]) ** 2))
    return N_L, N_R


def make_theta_field_quark(shape, mode='zero', seed=42):
    """
    Per-flavour β-gauge θ(x) field used by the F27 1-flavour mass step.

    mode = 'zero'   →  θ ≡ 0
    mode = 'random' →  θ uniform in [0, 2π)
    mode = 'plane'  →  θ ≡ π/3 (constant non-zero)
    """
    Lx, Ly = shape
    if mode == 'zero':
        return np.zeros((Lx, Ly), dtype=float)
    if mode == 'random':
        rng = np.random.default_rng(seed=seed)
        return rng.uniform(0.0, 2.0 * np.pi, size=(Lx, Ly))
    if mode == 'plane':
        return np.full((Lx, Ly), np.pi / 3.0, dtype=float)
    raise ValueError(f"Unknown θ mode: {mode!r}")


def quark_mass_step_f27(q, theta_flavour, m_flavour, dt=1.0):
    """
    F27 1-flavour β-gauge complex-mass step on the quark field — per
    (flavour, colour), apply `ca_dirac.mass_step_1flavor_u1`.

    For each flavour f the per-cell unitary is

        M(θ_f) = [[c_m I,            i s_m e^{iθ_f} I ],
                  [i s_m e^{-iθ_f} I,  c_m I          ]]

    with c_m = cos(m_f·dt), s_m = sin(m_f·dt). Color is preserved: the
    mass term is proportional to I_3 in colour space (SM-faithful — only
    the SU(3) gauge link mixes colours).

    Parameters
    ----------
    q              : quark field dict
    theta_flavour  : dict {flavour: (Lx,Ly) real} — β-gauge θ_f(x)
    m_flavour      : dict {flavour: float}        — mass m_f (|m| ≤ 1)
    dt             : float

    Returns
    -------
    Updated quark field dict (new arrays).
    """
    q_out = {k: v.copy() for k, v in q.items()}
    sample = next(iter(q.values()))
    zero_theta = np.zeros(sample.shape, dtype=float)
    for f in FLAVOURS:
        m = float(m_flavour.get(f, 0.0))
        theta = theta_flavour.get(f, zero_theta) if isinstance(theta_flavour, dict) else theta_flavour
        for c in COLOURS:
            eu_n, ed_n, cu_n, cd_n = cdir.mass_step_1flavor_u1(
                q[(f, c, 'eu')], q[(f, c, 'ed')],
                q[(f, c, 'cu')], q[(f, c, 'cd')],
                theta, m, dt)
            q_out[(f, c, 'eu')] = eu_n
            q_out[(f, c, 'ed')] = ed_n
            q_out[(f, c, 'cu')] = cu_n
            q_out[(f, c, 'cd')] = cd_n
    return q_out


def step_strong_2d_complex_mass(q, U, theta_flavour=None, m_flavour=None, dt=1.0):
    """
    One full strong-sector tick using the F27 complex-mass kinetic step.

    Strang split (per flavour, per colour):

        parallel_transport(U)
        → ca_dirac.dirac_step_complex_mass_1flavor(θ_f, m_f, dt)
        → parallel_transport(U)

    The kinetic step is the exact-QCA Weyl half-step from
    `ca_dirac._weyl_half_step_2c`, applied per (flavour, colour);
    the mass step is the F27 1-flavour β-gauge mixing.

    Compared to `step_strong_2d`, this replaces the Higgs–Yukawa /
    constant-mass Dirac unitary with the F27 chiral complex-mass
    mechanism. Up/down/strange mass splitting is intrinsic (each
    flavour has its own m_f).

    Cold-link, θ ≡ 0 regression: reduces bit-for-bit to N_F × N_C
    independent copies of `dirac_step_complex_mass_1flavor` — i.e. the
    F27 mechanism is color-blind and flavour-independent at the mass
    level, exactly as required.
    """
    if m_flavour is None:
        m_flavour = {'u': 0.0, 'd': 0.0, 's': 0.0}
    if theta_flavour is None:
        sample = next(iter(q.values()))
        zero_theta = np.zeros(sample.shape, dtype=float)
        theta_flavour = {f: zero_theta for f in FLAVOURS}

    # Half-step SU(3) parallel transport
    q = parallel_transport(q, U)

    # F27 complex-mass kinetic step per (flavour, colour)
    sample = next(iter(q.values()))
    zero_theta = np.zeros(sample.shape, dtype=float)
    for f in FLAVOURS:
        m = float(m_flavour.get(f, 0.0))
        theta = theta_flavour.get(f, zero_theta)
        for c in COLOURS:
            eu_n, ed_n, cu_n, cd_n = cdir.dirac_step_complex_mass_1flavor(
                q[(f, c, 'eu')], q[(f, c, 'ed')],
                q[(f, c, 'cu')], q[(f, c, 'cd')],
                theta, m, dt)
            q[(f, c, 'eu')] = eu_n
            q[(f, c, 'ed')] = ed_n
            q[(f, c, 'cu')] = cu_n
            q[(f, c, 'cd')] = cd_n

    # Half-step SU(3) parallel transport
    q = parallel_transport(q, U)
    return q


def quark_u1_gauge_transform_f27(q, phi_chi, flavour):
    """
    F27 1-flavour β-gauge U(1) transform on the χ sector of one flavour:

        (η_f, χ_f, θ_f) → (η_f, e^{iφ} χ_f, θ_f − φ)

    This is the U(1) Ward identity of the F27 mass step (Tier-1 #56 in
    the lepton sector). Only the χ components of the given flavour are
    transformed; the caller is responsible for the θ_f shift.

    Note: the χ sector here is the FULL right-handed Dirac sector for
    that flavour — i.e. (cu, cd). The mass step T4 identity is

        mass(η, e^{iφ} χ, θ − φ) = (η_new, e^{iφ} χ_new)

    so applying U(1)·χ in / U(1)·χ out + the θ shift maps the mass step
    to itself bit-for-bit.
    """
    q_out = {k: v.copy() for k, v in q.items()}
    ph = np.exp(1j * phi_chi).astype(complex)
    for c in COLOURS:
        q_out[(flavour, c, 'cu')] = ph * q[(flavour, c, 'cu')]
        q_out[(flavour, c, 'cd')] = ph * q[(flavour, c, 'cd')]
    return q_out


def quark_doublet_mass_step_su2(q, U_a, U_b, m_doublet, dt=1.0):
    """
    F27 SU(2)_L doublet complex-mass step applied to the (u, d) quark
    doublet, per colour. Strange (s) is left untouched.

    Treats (u_L, d_L) as the upper / lower components of an SU(2)_L
    isospin doublet, with a SHARED mass m_doublet (degenerate doublet).
    For each colour c, this is `ca_dirac.mass_step_doublet_su2` applied
    to:

        (u → ν,  d → e)  in the lepton-named slots.

    Used to verify the F27 SU(2)_L Ward identity in the quark sector
    (Q9). The physical mass splitting m_u ≠ m_d is intentionally not
    supported here — it explicitly breaks SU(2)_L at the mass level
    (Q10). The proper splitting requires the Stueckelberg-column
    structure with separate u_R, d_R singlets, which lives in the
    electroweak wiring (Phase 4).
    """
    q_out = {k: v.copy() for k, v in q.items()}
    for c in COLOURS:
        eu_u, ed_u = q[('u', c, 'eu')], q[('u', c, 'ed')]
        eu_d, ed_d = q[('d', c, 'eu')], q[('d', c, 'ed')]
        cu_u, cd_u = q[('u', c, 'cu')], q[('u', c, 'cd')]
        cu_d, cd_d = q[('d', c, 'cu')], q[('d', c, 'cd')]
        (eu_u_n, ed_u_n, eu_d_n, ed_d_n,
         cu_u_n, cd_u_n, cu_d_n, cd_d_n) = cdir.mass_step_doublet_su2(
            eu_u, ed_u, eu_d, ed_d,
            cu_u, cd_u, cu_d, cd_d,
            U_a, U_b, m_doublet, dt)
        q_out[('u', c, 'eu')] = eu_u_n
        q_out[('u', c, 'ed')] = ed_u_n
        q_out[('d', c, 'eu')] = eu_d_n
        q_out[('d', c, 'ed')] = ed_d_n
        q_out[('u', c, 'cu')] = cu_u_n
        q_out[('u', c, 'cd')] = cd_u_n
        q_out[('d', c, 'cu')] = cu_d_n
        q_out[('d', c, 'cd')] = cd_d_n
    return q_out


def quark_doublet_su2_transform_chiral(q, V_a, V_b, U_a, U_b):
    """
    Apply chiral SU(2)_L gauge transformation to the (u, d) quark doublet.

        (η_u, η_d) → V · (η_u, η_d)           [left-handed transforms]
        (χ_u, χ_d) → (χ_u, χ_d)               [right-handed unchanged]
        U          → V · U                    [Stueckelberg field compensates]

    where V = [[Va, -Vb*],[Vb, Va*]] ∈ SU(2). Strange (s) is unchanged.
    Acts identically on every colour (V is colour-blind).

    Returns
    -------
    (q_new, U_a_new, U_b_new).
    """
    q_out = {k: v.copy() for k, v in q.items()}
    Vbc = np.conj(V_b)
    Vac = np.conj(V_a)

    for c in COLOURS:
        eu_u = q[('u', c, 'eu')]; ed_u = q[('u', c, 'ed')]
        eu_d = q[('d', c, 'eu')]; ed_d = q[('d', c, 'ed')]
        q_out[('u', c, 'eu')] = V_a * eu_u - Vbc * eu_d
        q_out[('u', c, 'ed')] = V_a * ed_u - Vbc * ed_d
        q_out[('d', c, 'eu')] = V_b * eu_u + Vac * eu_d
        q_out[('d', c, 'ed')] = V_b * ed_u + Vac * ed_d
        # χ unchanged (chiral SU(2)_L)

    U_a_new = V_a * U_a - Vbc * U_b
    U_b_new = V_b * U_a + Vac * U_b
    return q_out, U_a_new, U_b_new


# ══════════════════════════════════════════════════════════════════
#  Phase 4 — Electroweak wiring of the quark doublet (2D analog of F34)
#  (added 2026-05-26)
#
#  Triggered by FG-2 Q11: the spectral kinetic step on the (u, d) quark
#  doublet does not satisfy local SU(2)_L Ward identity without a W_μ
#  link field. This section adds the 2D-square analog of F31 / F34:
#
#    • W-link field W_μ(x) ∈ SU(2) on the 2D square lattice (2 dirs)
#    • Site-centred U_eff(x) from the link average (mirrors ca_wmu)
#    • Covariant quark doublet kinetic step that rotates the (u_L, d_L)
#      isospin index by U_eff(x) before the spectral 2D Weyl step
#    • Full covariant doublet step (kinetic ½ → mass → kinetic ½)
#    • W-link gauge transformation U_μ → V(x)·U_μ·V†(x+μ̂)
#
#  Properties (mirror W1 / F34):
#    • Cold W-links: reduces bit-for-bit to (F27 mass step) ∘ (per-(f,c)
#      free Weyl kinetic half-steps).
#    • Constant V(x): SU(2)_L Ward identity exact to machine ε
#      (V commutes with the spectral kinetic step since V acts on isospin).
#    • Varying V(x): O(a)·|∇V|·L residual (W1.4 status).
#    • Right-handed χ at m=0: bit-for-bit decoupled from W_μ (F34 W4.3).
# ══════════════════════════════════════════════════════════════════


def make_w_link_field_2d(shape, mode='identity', seed=42):
    """
    Initialise an SU(2) W_μ(x) link field on a 2D-square lattice.

    Returns
    -------
    W_links : list of 2 elements (μ = x, y); each is (W_a, W_b) with
              W_μ(x) = [[W_a, −conj(W_b)],[W_b, conj(W_a)]] ∈ SU(2),
              W_a, W_b complex arrays of shape (Lx, Ly).
    """
    Lx, Ly = shape
    rng = np.random.default_rng(seed=seed)

    if mode == 'identity':
        W_links = [(np.ones(shape, dtype=complex),
                    np.zeros(shape, dtype=complex))
                   for _ in range(2)]
    elif mode == 'random':
        W_links = []
        for _ in range(2):
            raw = rng.standard_normal(shape + (4,))
            raw /= np.linalg.norm(raw, axis=-1, keepdims=True)
            Wa = raw[..., 0] + 1j * raw[..., 3]
            Wb = raw[..., 2] + 1j * raw[..., 1]
            W_links.append((Wa, Wb))
    elif mode == 'pure_gauge':
        raw = rng.standard_normal(shape + (4,))
        raw /= np.linalg.norm(raw, axis=-1, keepdims=True)
        Va = raw[..., 0] + 1j * raw[..., 3]
        Vb = raw[..., 2] + 1j * raw[..., 1]
        W_links = []
        for mu in range(2):
            Va_shift = np.roll(Va, -1, axis=mu)
            Vb_shift = np.roll(Vb, -1, axis=mu)
            # U_μ(x) = V(x+μ̂) · V(x)†
            Wa_pg = Va_shift * np.conj(Va) + np.conj(Vb_shift) * Vb
            Wb_pg = Vb_shift * np.conj(Va) - np.conj(Va_shift) * Vb
            W_links.append((Wa_pg, Wb_pg))
    else:
        raise ValueError(f"Unknown W-link mode: {mode!r}")
    return W_links


def w_link_unitarity_residual_2d(W_links):
    """max_{μ,x} | |W_a|² + |W_b|² − 1 |."""
    return float(max(np.max(np.abs(np.abs(Wa) ** 2 + np.abs(Wb) ** 2 - 1.0))
                     for (Wa, Wb) in W_links))


def u_eff_from_w_links_2d(W_links):
    """
    Site-centred SU(2) effective gauge field from the 2D W-link field —
    average over the two link directions at each site, then re-unitarise.

    Mirrors ca_wmu._u_eff_from_links. For W_links = identity → U_eff = I
    bit-for-bit (cold-link regression).
    """
    Wa_sum = sum(Wa for (Wa, _) in W_links)
    Wb_sum = sum(Wb for (_, Wb) in W_links)
    norm = np.sqrt(np.abs(Wa_sum) ** 2 + np.abs(Wb_sum) ** 2)
    norm = np.where(norm > 1e-14, norm, 1.0)
    return Wa_sum / norm, Wb_sum / norm


def w_link_gauge_transform_2d(W_links, V_a, V_b):
    """
    Apply local SU(2) gauge transformation to the W-link field:

        W_μ(x) → V(x) · W_μ(x) · V†(x + μ̂)

    SU(2) product formula: (a1, b1) · (a2, b2) =
        (a1·a2 − conj(b1)·b2,  b1·a2 + conj(a1)·b2).

    The inverse of an SU(2) element (a, b) is (conj(a), −b), so
        V†(x + μ̂) ↔ (conj(V_a_shift), −V_b_shift).

    Returns a new W_links list (does not mutate the input).
    """
    Vbc = np.conj(V_b)
    Vac = np.conj(V_a)
    out = []
    for mu, (Wa, Wb) in enumerate(W_links):
        Va_shift = np.roll(V_a, -1, axis=mu)
        Vb_shift = np.roll(V_b, -1, axis=mu)
        Va_shift_c = np.conj(Va_shift)
        # Step 1:  A = V(x) · W
        A_a = V_a * Wa - Vbc * Wb
        A_b = V_b * Wa + Vac * Wb
        # Step 2:  result = A · V†(x+μ̂)
        # B = V†(x+μ̂) has (a, b) = (Va_shift_c, −Vb_shift)
        B_a = Va_shift_c
        B_b = -Vb_shift
        Wa_new = A_a * B_a - np.conj(A_b) * B_b
        Wb_new = A_b * B_a + np.conj(A_a) * B_b
        out.append((Wa_new, Wb_new))
    return out


def covariant_quark_doublet_step_2d(q, U_color, W_links,
                                    U_a_mass, U_b_mass,
                                    m_doublet, dt=1.0,
                                    m_strange=0.0,
                                    theta_strange=None):
    """
    Full SU(2)_L-covariant Dirac doublet step for the (u, d) quarks on
    the 2D-square lattice with colour SU(3) parallel transport, W_μ
    SU(2)_L link field, and F27 SU(2) doublet complex-mass coupling.

    Strang split per colour:
        K_W(dt/2)  →  M_F27(dt)  →  K_W(dt/2)

    where K_W is the W-covariant kinetic half-step:
        η_doublet → U_eff_W · η_doublet  (isospin rotation, left-handed only)
        χ_doublet → χ_doublet            (right-handed: SU(2)_L singlet)
        each (flavour × isospin) component → _weyl_half_step_2c (spectral)

    and M_F27 is `quark_doublet_mass_step_su2` (SU(2) Stueckelberg mass).

    Strange (s) is treated as an SU(2)_L singlet and gets the F27
    1-flavour mass step (m_strange, optional θ_s field) plus a colour
    parallel transport. This keeps strange propagating without polluting
    the (u, d) Ward-identity tests.

    Properties (verified in test_FG3_quark_electroweak.py):
        • W = I, U = I, m_strange = 0: bit-for-bit equivalent to
          (free Weyl half-steps per (f,c)) ∘ (doublet mass) ∘ (half-steps).
        • Constant V(x) for both ψ and W: SU(2)_L Ward identity exact
          to machine ε (V commutes with FFT and U_eff at each site).
        • Varying V(x): O(a) Ward residual — W1.4 status.
        • m_doublet = 0: right-handed χ exactly decoupled from W (F34 W4.3).
    """
    # ─ Helper: build site-centred U_eff_W once per call ─
    UWa, UWb = u_eff_from_w_links_2d(W_links)
    UWa_c = np.conj(UWa)
    UWb_c = np.conj(UWb)

    # ─ Half kinetic step ─────────────────────────────────────────────
    def apply_kinetic_half(q_in, dt_half):
        q_o = {k: v.copy() for k, v in q_in.items()}
        for c in COLOURS:
            # (u, d) left-handed doublet: rotate isospin by U_eff_W, then
            # per-component spectral half-step.
            for spin in ('eu', 'ed'):
                eu = q_in[('u', c, spin)]
                ed = q_in[('d', c, spin)]
                # U_eff_W · (eu, ed)
                eu_rot = UWa * eu - UWb_c * ed
                ed_rot = UWb * eu + UWa_c * ed
                # Spectral half-step per flavour: needs a (f, g) pair —
                # here we use a "spinor-up" trick: pair (eu, ed) is
                # actually (spin-↑, spin-↓) of one isospin component, not
                # two components of one Weyl. So we must apply the half
                # step to (η_u_↑, η_u_↓) and (η_d_↑, η_d_↓) separately,
                # NOT to (η_u, η_d). Loop over flavour, not spin.
                # → fall back to a flavour-major loop below.
                pass
        # Flavour-major loop: rotate isospin per spin, then half-step per
        # (flavour, colour) using the 2-component (↑, ↓) pair.
        for c in COLOURS:
            # Apply U_eff_W to isospin index of left-handed (η_u, η_d)
            # for each spin component, then half-step each spinor (η_↑, η_↓)
            eu_u = q_in[('u', c, 'eu')]
            ed_u = q_in[('u', c, 'ed')]
            eu_d = q_in[('d', c, 'eu')]
            ed_d = q_in[('d', c, 'ed')]
            # Isospin rotate at fixed spin
            eu_u_r = UWa * eu_u - UWb_c * eu_d
            eu_d_r = UWb * eu_u + UWa_c * eu_d
            ed_u_r = UWa * ed_u - UWb_c * ed_d
            ed_d_r = UWb * ed_u + UWa_c * ed_d
            # Spectral 2D half-step on each flavour (Weyl 2-component)
            u_eu_new, u_ed_new = cdir._weyl_half_step_2c(eu_u_r, ed_u_r, dt_half)
            d_eu_new, d_ed_new = cdir._weyl_half_step_2c(eu_d_r, ed_d_r, dt_half)
            q_o[('u', c, 'eu')] = u_eu_new
            q_o[('u', c, 'ed')] = u_ed_new
            q_o[('d', c, 'eu')] = d_eu_new
            q_o[('d', c, 'ed')] = d_ed_new

            # Right-handed (χ_u, χ_d): SU(2)_L singlet — identity isospin
            # → just per-flavour spectral half-step, no rotation.
            cu_u_new, cd_u_new = cdir._weyl_half_step_2c(
                q_in[('u', c, 'cu')], q_in[('u', c, 'cd')], dt_half)
            cu_d_new, cd_d_new = cdir._weyl_half_step_2c(
                q_in[('d', c, 'cu')], q_in[('d', c, 'cd')], dt_half)
            q_o[('u', c, 'cu')] = cu_u_new
            q_o[('u', c, 'cd')] = cd_u_new
            q_o[('d', c, 'cu')] = cu_d_new
            q_o[('d', c, 'cd')] = cd_d_new
        # Strange — full 4-component complex-mass-1flavor step (kinetic+mass
        # together; m_strange may be zero). Keeps s propagating but as an
        # SU(2)_L singlet. Performed once (not split) inside the kinetic
        # half if dt_half is the FULL step; here we use a half-step trick:
        # apply the kinetic half-step to each chirality independently.
        for c in COLOURS:
            s_eu_new, s_ed_new = cdir._weyl_half_step_2c(
                q_in[('s', c, 'eu')], q_in[('s', c, 'ed')], dt_half)
            s_cu_new, s_cd_new = cdir._weyl_half_step_2c(
                q_in[('s', c, 'cu')], q_in[('s', c, 'cd')], dt_half)
            q_o[('s', c, 'eu')] = s_eu_new
            q_o[('s', c, 'ed')] = s_ed_new
            q_o[('s', c, 'cu')] = s_cu_new
            q_o[('s', c, 'cd')] = s_cd_new
        return q_o

    # ─ Mass step ─────────────────────────────────────────────────────
    def apply_mass(q_in, dt_full):
        # Doublet mass on (u, d)
        q_o = quark_doublet_mass_step_su2(q_in, U_a_mass, U_b_mass,
                                          m_doublet, dt=dt_full)
        # F27 1-flavour mass on strange (SU(2)_L singlet)
        if theta_strange is None:
            sample = next(iter(q_in.values()))
            theta_s = np.zeros(sample.shape, dtype=float)
        else:
            theta_s = theta_strange
        for c in COLOURS:
            eu_n, ed_n, cu_n, cd_n = cdir.mass_step_1flavor_u1(
                q_o[('s', c, 'eu')], q_o[('s', c, 'ed')],
                q_o[('s', c, 'cu')], q_o[('s', c, 'cd')],
                theta_s, m_strange, dt_full)
            q_o[('s', c, 'eu')] = eu_n
            q_o[('s', c, 'ed')] = ed_n
            q_o[('s', c, 'cu')] = cu_n
            q_o[('s', c, 'cd')] = cd_n
        return q_o

    # ─ Optional colour parallel transport at the start/end ──────────
    # The SU(3) and SU(2)_L gauge sectors are independent; we apply the
    # SU(3) transport before/after the doublet step exactly as in
    # step_strong_2d.
    if U_color is not None:
        q = parallel_transport(q, U_color)

    # ─ Strang: K(dt/2) → M(dt) → K(dt/2) ─
    q = apply_kinetic_half(q, 0.5 * dt)
    q = apply_mass(q, dt)
    q = apply_kinetic_half(q, 0.5 * dt)

    if U_color is not None:
        q = parallel_transport(q, U_color)
    return q
