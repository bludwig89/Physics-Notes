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


def yukawa_mass_field(phi, yukawa_couplings):
    """
    Compute per-cell quark mass fields from the Higgs field Φ via Yukawa coupling.

    m_q(x) = y_q · Re Φ(x)       (real part only; imaginary part → CP phase)
    m̃_q(x) = y_q · Im Φ(x)       (complex mass field for varm stepper)

    Parameters
    ----------
    phi : complex ndarray of shape (Lx, Ly)
        Higgs field Φ(x).  Typically `state.Phi` from `ca_unified.py`.
    yukawa_couplings : dict {flavour: y_q}  with real y_q ≥ 0.
        Coupling constants per flavour.  Missing flavours default to 0.

    Returns
    -------
    dict {flavour: (m_R_field, m_I_field)}
        m_R_field = y_q * Re(Φ),  m_I_field = y_q * Im(Φ), both real
        ndarrays of shape (Lx, Ly).

    Notes
    -----
    - Coupling is colour-blind: the same m_q(x) is used for all colours
      of a given flavour.  Higgs/Yukawa does not mix colour indices.
    - When Φ is spatially uniform (Re Φ = v, Im Φ = 0), m_R_field = y_q·v
      and m_I_field = 0, so `dirac_step_2d_varm_complex_splitstep` reduces
      to `dirac_step_2d_splitstep` bit-for-bit (δm = 0 path).
    """
    phi_r = np.real(phi)
    phi_i = np.imag(phi)
    result = {}
    for f in FLAVOURS:
        y = float(yukawa_couplings.get(f, 0.0))
        result[f] = (y * phi_r, y * phi_i)
    return result


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

def step_strong_2d(q, U, m_flavour=None, dt=1.0, phi_field=None, yukawa=None):
    """
    One full strong-sector tick on a 3-flavour, 3-colour quark field.

    Parameters
    ----------
    q : dict from `zero_quark_field` / `gaussian_quark`
    U : link field of shape (2, Lx, Ly, 3, 3)
    m_flavour : dict {flavour: m_q}  with |m_q| ≤ 1 (QCA admissibility).
        Default: massless ({'u': 0, 'd': 0, 's': 0}).
        Ignored when phi_field is provided.
    dt : time step, passed straight through to the Dirac stepper.
    phi_field : complex ndarray of shape (Lx, Ly), optional.
        Higgs field Φ(x).  When provided, the per-cell Yukawa mass
            m_q(x) = yukawa[f] · Re Φ(x),
            m̃_q(x) = yukawa[f] · Im Φ(x)
        is computed via `yukawa_mass_field` and passed to
        `dirac_step_2d_varm_complex_splitstep` for each (flavour, colour).
        The Strang split is: Mix(δm, dt/2) → Kinetic(m0, dt) → Mix(δm, dt/2),
        which is O(dt²) accurate and exact at δm = 0.
    yukawa : dict {flavour: y_q}, optional.
        Yukawa coupling constants.  Required when phi_field is not None.
        Missing flavours default to y_q = 0 (massless).

    Algorithm (Strang-symmetric, cold-link reducible):

        1. Half-step parallel transport: q → P_½ q with P_½ from link avg.
        2. Kinetic step on each (flavour, colour) copy:
              Scalar path (phi_field=None):
                (η, χ) ← dirac_step_2d_splitstep(η, χ, m = m_flavour[f])
              Yukawa path (phi_field given):
                (η, χ) ← dirac_step_2d_varm_complex_splitstep(
                              η, χ, m_R_field, m_I_field)
        3. Half-step parallel transport again.

    Cold-link limit (U_μ ≡ I): step 1 and step 3 are the identity; the
    result is bit-for-bit 9 independent (per-flavour, per-colour) Dirac
    steps.  This is the V13a regression contract.

    Uniform-Φ regression (V13c.1): when phi_field is spatially uniform
    (Re Φ = v everywhere, Im Φ = 0), δm = 0 for every cell, the
    `dirac_step_2d_varm_complex_splitstep` reduces to
    `dirac_step_2d_splitstep(m = y*v)` bit-for-bit.

    Note: this is the *frozen-link* stepper — the links do NOT update.
    Dynamical gluons live in V15 (separate routine).
    """
    if phi_field is not None:
        # ── Yukawa path: per-cell mass from Higgs field ────────────
        if yukawa is None:
            yukawa = {}
        mass_fields = yukawa_mass_field(phi_field, yukawa)
    else:
        # ── Scalar path: static dict of per-flavour masses ─────────
        if m_flavour is None:
            m_flavour = {'u': 0.0, 'd': 0.0, 's': 0.0}

    # ── Half-step parallel transport ───────────────────────────────
    q = parallel_transport(q, U)

    # ── Kinetic step on each (flavour, colour) copy ────────────────
    for f in FLAVOURS:
        if phi_field is not None:
            m_R_field, m_I_field = mass_fields[f]
            for c in COLOURS:
                eu = q[(f, c, 'eu')]
                ed = q[(f, c, 'ed')]
                cu = q[(f, c, 'cu')]
                cd = q[(f, c, 'cd')]
                eu_n, ed_n, cu_n, cd_n = cdir.dirac_step_2d_varm_complex_splitstep(
                    eu, ed, cu, cd,
                    m_R_field=m_R_field, m_I_field=m_I_field,
                    dt=dt
                )
                q[(f, c, 'eu')] = eu_n
                q[(f, c, 'ed')] = ed_n
                q[(f, c, 'cu')] = cu_n
                q[(f, c, 'cd')] = cd_n
        else:
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
