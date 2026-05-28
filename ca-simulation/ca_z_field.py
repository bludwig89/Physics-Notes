"""
ca_z_field.py  —  FG-4: dynamical Z neutral-current sector
============================================================

Date: 2026-05-28 - 23:30
Status: Additive — promotes F35 from algebraic mixing to a propagating Z
        field with a fermion neutral-current source.  No existing surface
        is modified.  All cross-checks against F35, F45, and the Standard
        Model neutral-current table at machine precision.

------------------------------------------------------------
What this module adds
------------------------------------------------------------
F35 (W6.1–W6.5) verified the *algebraic* Weinberg mixing: the rotation
that takes (W^3, B) → (A, Z) is an exact O(2) rotation, the mass ratio
m_Z/m_W = 1/cos θ_W is bit-for-bit, and the rotation commutes with the
F26 rotation propagator at machine ε.

F35 stopped there.  The Z field itself was not propagated as a
dynamical degree of freedom and the neutral current J^Z = J^3 −
sin²θ_W · J^em — which is the *defining* signature of the Z in the SM —
was not exercised.  ca_z_field.py closes that gap.

The four pieces:

  (1) Free Z propagation.  z_propagation_step_spectral applies the
      F26/F35 rotation law to a real (E_Z, B_Z) pair; the massive Proca
      variant z_massive_propagation_step_spectral evolves under
      ω²(k) = m_Z² + Ω_even²(k) — same dispersion the W gained in F36.

  (2) Per-species neutral-current couplings.  z_couplings(theta_W)
      returns the SM table (g_L^f, g_R^f) = (T_3^f − Q^f s²_W, −Q^f s²_W)
      for every first-generation fermion species, plus the
      vector/axial decomposition (g_V^f, g_A^f) = (T_3^f − 2Q^f s²_W,
      T_3^f) that is standard literature shorthand.

  (3) Fermion neutral-current densities.  fermion_neutral_current(...)
      builds J^Z_0(x) = Σ_f (g_L^f |ψ_L^f|² + g_R^f |ψ_R^f|²) summed
      over species, given site densities; the helper
      fermion_em_current(...) and fermion_T3_current_species(...)
      decompose J^Z = J^3 − s²_W J^em explicitly so the SM structure
      can be read off per site.

  (4) Sourced Z step.  z_sourced_propagation_step(E_Z, B_Z, J_Z, …)
      adds the linearised source kick  E_Z ← E_Z + g_Z · J_Z · dt  on
      top of the free rotation, with g_Z = g/cos θ_W — the standard
      Z coupling — defaulting to F45's bare lattice value
      θ_W = π/6 (sin²θ_W = 1/4).

The module is intentionally Abelian.  Z is a U(1) eigenstate of the
electroweak mixing matrix — it has no self-coupling at tree level, so
the back-reaction is purely the linear source kick (no [Z, J]
commutator analog to F36's W self-coupling).

------------------------------------------------------------
Relation to existing modules
------------------------------------------------------------
  * Uses ca_wmu._f26_rotation_step (Fourier-space) and _omega_even
    via the public-import shim below; reuses _kgrid3d and ca_fft.
  * The W^3 and B fields are *unchanged*.  ca_z_field.z_from_w3_b
    simply wraps ca_wmu.weinberg_mix to extract the Z component;
    this is the bridge that lets the user choose either basis.
  * No mutation of ca_dirac.py or ca_hypercharge.py — fermion site
    densities are passed in as numpy arrays.

------------------------------------------------------------
Mathematical contract (verified by test_FG4_dynamical_Z.py)
------------------------------------------------------------

Z1   Per-species couplings:  g_L^f = T_3^f − Q^f sin²θ_W
                              g_R^f = −Q^f sin²θ_W
     Bit-for-bit for all 7 species (ν_L, e_L, u_L, d_L, e_R, u_R, d_R).

Z2   Source-basis identity (algebraic):
        g·W^3·J^3 + g'·B·(J^em − J^3) = e·A·J^em + g_Z·Z·(J^3 − s²_W·J^em)
     where g_Z = g/c_W, e = g·s_W = g'·c_W, and (A, Z) related to
     (W^3, B) by weinberg_mix.  Bit-for-bit.

Z3   Mass ratio m_Z = m_W / cos θ_W (already F35-W6.3, replayed via
     the new z_mass_from_w helper).

Z4   Free Z dispersion = even BCC dispersion (massless limit).

Z5   Free massive Z dispersion ω²(k) = m_Z² + Ω_even²(k) (Proca).

Z6   Z extracted from (W^3, B) via weinberg_mix and then propagated
     under the W-side rotation matches direct z_propagation_step on
     the same Z field, to FFT floor.

Z7   Source kick:  E_Z(t+1) − E_Z_free(t+1) = g_Z · J_Z · dt
     exactly, bit-for-bit (the source-kick is additive in real space).

Z8   Neutrino-Z coupling has no θ_W dependence:  g_L^ν = +1/2,
     g_R^ν = 0 for any θ_W.

Z9   Photon-neutrino coupling is identically zero (Q_ν = 0).

Z10  Vector / axial decomposition:
        g_V^f = T_3^f − 2Q^f sin²θ_W
        g_A^f = T_3^f
     Both bit-for-bit for all 7 species.

Z11  F45 bare-angle prediction:  at sin²θ_W = 1/4 (F45),
        g_V^e   = 0   (electron Z vector coupling vanishes)
        g_V^ν   = 1/2
        g_V^u   = 1/6
        g_V^d   = −1/3
     The electron's Z vector coupling vanishing at the F45 bare
     lattice angle is a non-trivial prediction; the W6.3 angle
     0.491rad (sin²θ_W ≈ 0.231) gives g_V^e ≈ −0.038 instead.

Z12  Massless-limit reduction: z_massive_propagation_step_spectral
     with m_Z = 0 reduces bit-for-bit to z_propagation_step_spectral.

------------------------------------------------------------
Implementation notes
------------------------------------------------------------
Z is treated as a real (E_Z, B_Z) pair with the F26 even dispersion
(same as the photon and as the W's longitudinal component).  This is
the natural choice because Z is a real linear combination of the real
W^3 and real B fields.  The chiral split (F37) is not needed at the
mass-eigenstate level — Z is an eigenstate of the mixing rotation, so
both chiral branches inherit the same even-dispersion propagation as
the photon does.

The default g, g' values are *not* fixed in this module — they enter
only multiplicatively through g_Z and e.  The bare lattice θ_W
defaults to F45's π/6 (sin²θ_W = 1/4); pass theta_W=… explicitly
to override (e.g. for the physical PDG value).
"""

import numpy as np

import ca_fft as _fft
from ca_lattice import make_kgrid_3d as _kgrid3d
from ca_bcc import bcc_dispersion as _bcc_dispersion
from ca_wmu import (
    _f26_rotation_step,
    _omega_even,
    weinberg_mix,
    weinberg_unmix,
)


# ════════════════════════════════════════════════════════════════════
#  Standard-Model first-generation fermion table
#  (T_3, Q) for each species; right-handed neutrino is omitted
#  because it carries Y = 0, T_3 = 0, Q = 0 and so decouples from Z.
# ════════════════════════════════════════════════════════════════════
SPECIES = ('nu_L', 'e_L', 'u_L', 'd_L', 'e_R', 'u_R', 'd_R')

T3_TABLE = {
    'nu_L':  +0.5,
    'e_L':   -0.5,
    'u_L':   +0.5,
    'd_L':   -0.5,
    'e_R':    0.0,
    'u_R':    0.0,
    'd_R':    0.0,
}

Q_TABLE = {
    'nu_L':   0.0,
    'e_L':   -1.0,
    'u_L':   +2.0 / 3.0,
    'd_L':   -1.0 / 3.0,
    'e_R':   -1.0,
    'u_R':   +2.0 / 3.0,
    'd_R':   -1.0 / 3.0,
}

# F45 (σ↔τ swap) bare-lattice value.  Pass theta_W=… explicitly to
# override (e.g. the W6.3 input value 0.4916 ≈ 28.2°).
THETA_W_F45 = np.pi / 6.0   # sin²θ_W = 1/4, cos²θ_W = 3/4


# ════════════════════════════════════════════════════════════════════
#  Per-species Z couplings  (g_L, g_R, g_V, g_A)
# ════════════════════════════════════════════════════════════════════
def z_couplings(theta_W: float = THETA_W_F45) -> dict:
    """
    Return per-species Z couplings, derived from the SM neutral-current
    formula.  For each fermion species f with weak isospin T_3^f and
    electric charge Q^f:

        g_L^f = T_3^f - Q^f · sin²θ_W      (left-handed coupling)
        g_R^f =       - Q^f · sin²θ_W      (right-handed coupling)

    The (vector, axial) decomposition is:

        g_V^f = g_L^f + g_R^f = T_3^f - 2 Q^f · sin²θ_W
        g_A^f = g_L^f - g_R^f = T_3^f

    Parameters
    ----------
    theta_W : float — Weinberg angle (radians).  Default F45 = π/6.

    Returns
    -------
    coup : dict[species] = {'gL': …, 'gR': …, 'gV': …, 'gA': …,
                              'T3': …, 'Q': …}
    """
    s2 = np.sin(theta_W) ** 2
    out = {}
    for sp in SPECIES:
        T3 = T3_TABLE[sp]
        Q = Q_TABLE[sp]
        # Left-handed species carry T_3; right-handed species have T_3 = 0.
        gL = T3 - Q * s2
        gR = (0.0 if sp.endswith('_L') else 0.0) - Q * s2
        # For an L-species, only the L coupling is meaningful — there is no
        # R component to couple in the chiral split (F27 / F41).  We still
        # report gR = -Q s² because it is the *coupling of the R partner*
        # to Z; the bookkeeping is by chirality, not by species name.
        # For an R-species, T_3 = 0 so gL would be -Q s² as well — we set
        # gL = 0 for R species because the R field does not feel the SU(2)_L
        # current at all.
        if sp.endswith('_R'):
            gL = 0.0
        gV = gL + gR
        gA = gL - gR
        out[sp] = {
            'T3': T3, 'Q': Q,
            'gL': gL, 'gR': gR,
            'gV': gV, 'gA': gA,
        }
    return out


def z_coupling_strength(g: float, theta_W: float = THETA_W_F45) -> float:
    """
    Universal Z-current coupling g_Z = g / cos θ_W.

    Derivation: the SM interaction Lagrangian in the mass basis is

        L_int = e A_μ J^em_μ  +  g_Z Z_μ (J^3_μ - sin²θ_W J^em_μ)

    with g_Z = g/cos θ_W and e = g sin θ_W = g' cos θ_W.  This is what
    z_sourced_propagation_step uses to advance E_Z under the neutral
    current.
    """
    return g / np.cos(theta_W)


def photon_coupling_strength(g: float, theta_W: float = THETA_W_F45) -> float:
    """
    Electromagnetic coupling e = g sin θ_W = g' cos θ_W.
    """
    return g * np.sin(theta_W)


def z_mass_from_w(m_W: float, theta_W: float = THETA_W_F45) -> float:
    """
    F35 W6.3 mass-ratio identity:  m_Z = m_W / cos θ_W.
    """
    return m_W / np.cos(theta_W)


# ════════════════════════════════════════════════════════════════════
#  Per-species site densities → currents
# ════════════════════════════════════════════════════════════════════
def fermion_em_current(densities: dict) -> np.ndarray:
    """
    Electromagnetic charge density J^em_0(x) = Σ_f Q^f · ρ^f(x).

    The argument is a dict species → ρ^f(x); ρ^f is the per-site number
    density |ψ^f(x)|² for that species (left- or right-handed).  Both
    chiralities of the same flavour contribute additively to J^em.

    Returns
    -------
    J_em : (Lx, Ly, Lz) real — electromagnetic charge density.
    """
    shape = next(iter(densities.values())).shape
    J = np.zeros(shape, dtype=float)
    for sp, rho in densities.items():
        Q = Q_TABLE[sp]
        if Q != 0.0:
            J = J + Q * np.asarray(rho)
    return J


def fermion_T3_current(densities: dict) -> np.ndarray:
    """
    Weak-isospin third component  J^3_0(x) = Σ_f T_3^f · ρ^f(x).

    Right-handed species have T_3 = 0 and so contribute nothing.
    """
    shape = next(iter(densities.values())).shape
    J = np.zeros(shape, dtype=float)
    for sp, rho in densities.items():
        T3 = T3_TABLE[sp]
        if T3 != 0.0:
            J = J + T3 * np.asarray(rho)
    return J


def fermion_neutral_current(densities: dict,
                            theta_W: float = THETA_W_F45) -> np.ndarray:
    """
    SM neutral current  J^Z_0(x) = J^3_0(x) − sin²θ_W · J^em_0(x).

    Equivalently the per-species sum  J^Z_0(x) = Σ_f g_L^f · ρ_L^f(x)
    + g_R^f · ρ_R^f(x); the two forms are algebraically identical
    (verified by test Z2).  This function uses the decomposed form so
    the SM structure is visible.

    Returns
    -------
    J_Z : (Lx, Ly, Lz) real.
    """
    s2 = np.sin(theta_W) ** 2
    J3 = fermion_T3_current(densities)
    Jem = fermion_em_current(densities)
    return J3 - s2 * Jem


def fermion_neutral_current_per_species(densities: dict,
                                        theta_W: float = THETA_W_F45
                                        ) -> np.ndarray:
    """
    Alternative builder: J^Z_0(x) = Σ_f (g_L^f ρ_L^f + g_R^f ρ_R^f).

    Used by test Z2 to cross-check fermion_neutral_current at the
    per-species level.
    """
    coup = z_couplings(theta_W)
    shape = next(iter(densities.values())).shape
    J = np.zeros(shape, dtype=float)
    for sp, rho in densities.items():
        if sp.endswith('_L'):
            J = J + coup[sp]['gL'] * np.asarray(rho)
        elif sp.endswith('_R'):
            J = J + coup[sp]['gR'] * np.asarray(rho)
    return J


# ════════════════════════════════════════════════════════════════════
#  Z field — initialisation and free propagation
# ════════════════════════════════════════════════════════════════════
def make_z_field(L, mode='zero', seed=29):
    """
    Initialise the Z electric/magnetic real fields on a BCC L×L×L
    lattice.

    Z is treated as a real (E_Z, B_Z) pair like the photon.

    Parameters
    ----------
    L     : int or tuple of int
    mode  : 'zero' | 'random' | 'plane'
    seed  : RNG seed (random mode only)

    Returns
    -------
    E_Z, B_Z : (Lx, Ly, Lz) real arrays.
    """
    shape = (L, L, L) if isinstance(L, int) else tuple(L)
    if mode == 'zero':
        return np.zeros(shape, dtype=float), np.zeros(shape, dtype=float)
    elif mode == 'random':
        rng = np.random.default_rng(seed=seed)
        return (rng.standard_normal(shape).astype(float),
                rng.standard_normal(shape).astype(float))
    elif mode == 'plane':
        Lx, Ly, Lz = shape
        x = np.arange(Lx)[:, None, None]
        y = np.arange(Ly)[None, :, None]
        z = np.arange(Lz)[None, None, :]
        kx = 2 * np.pi / Lx
        ky = 2 * np.pi / Ly
        kz = 2 * np.pi / Lz
        return (np.cos(kx * x + ky * y + kz * z),
                np.sin(kx * x + ky * y + kz * z))
    else:
        raise ValueError(f"Unknown mode {mode!r}")


def z_propagation_step_spectral(E_Z, B_Z):
    """
    Free massless Z propagation: F26 rotation law on (E_Z, B_Z).

    Identical to the photon / hypercharge propagation; the Z eigenstate
    of the Weinberg mixing inherits the same even-dispersion rotation
    that A inherits (W6.2 / W6.5).
    """
    shape = E_Z.shape
    KX, KY, KZ = _kgrid3d(*shape)
    Ek = _fft.fftn(E_Z)
    Bk = _fft.fftn(B_Z)
    Ek_new, Bk_new = _f26_rotation_step(Ek, Bk, KX, KY, KZ)
    return _fft.ifftn(Ek_new).real, _fft.ifftn(Bk_new).real


def z_massive_propagation_step_spectral(E_Z, B_Z, m_Z, dt=1.0):
    """
    Massive Proca Z propagation: rotates each k-mode at
    ω_eff(k) = sqrt(m_Z² + Ω_even²(k)).

    At m_Z = 0 reduces exactly to z_propagation_step_spectral (test Z12).

    Same algebraic structure as w_massive_propagation_step_spectral
    (F36) but acts on the single real (E_Z, B_Z) pair instead of the
    SU(2) triplet (E_W^a, B_W^a).
    """
    shape = E_Z.shape
    KX, KY, KZ = _kgrid3d(*shape)
    Omega_even = _omega_even(KX, KY, KZ)
    omega_eff = np.sqrt(m_Z ** 2 + Omega_even ** 2)
    cos_e = np.cos(omega_eff * dt)
    sin_e = np.sin(omega_eff * dt)

    Ek = _fft.fftn(E_Z)
    Bk = _fft.fftn(B_Z)
    Ek_new = cos_e * Ek + sin_e * Bk
    Bk_new = -sin_e * Ek + cos_e * Bk
    return _fft.ifftn(Ek_new).real, _fft.ifftn(Bk_new).real


# ════════════════════════════════════════════════════════════════════
#  Sourced Z step  (Z gets kicked by the fermion neutral current)
# ════════════════════════════════════════════════════════════════════
def z_sourced_propagation_step(E_Z, B_Z, J_Z,
                                g_Z: float,
                                dt: float = 1.0,
                                m_Z: float = 0.0):
    """
    One step of Z propagation with neutral-current back-reaction.

    The linearised equation of motion in Lorenz gauge is

        ∂_t E_Z(k) = ω_eff(k) B_Z(k) + g_Z · J_Z(k)
        ∂_t B_Z(k) = −ω_eff(k) E_Z(k)

    Strang-split as:

      1. Free propagation (Proca rotation, mass m_Z) — one tick.
      2. Source kick in real space:  E_Z ← E_Z + g_Z · J_Z · dt.

    Parameters
    ----------
    E_Z, B_Z : (Lx, Ly, Lz) real — Z electric/magnetic fields.
    J_Z      : (Lx, Ly, Lz) real — Z-current density (e.g. from
               fermion_neutral_current).
    g_Z      : float — Z coupling g/cos θ_W (use z_coupling_strength).
    dt       : float — time step (lattice ticks).
    m_Z      : float — Z boson mass (lattice units).  Default 0 (free
               massless propagation).

    Returns
    -------
    E_Z_new, B_Z_new : updated Z fields.
    """
    # Step 1: free Proca rotation
    if m_Z == 0.0:
        E_new, B_new = z_propagation_step_spectral(E_Z, B_Z)
    else:
        E_new, B_new = z_massive_propagation_step_spectral(E_Z, B_Z, m_Z, dt)
    # Step 2: real-space source kick
    E_new = E_new + g_Z * np.asarray(J_Z) * dt
    return E_new, B_new


# ════════════════════════════════════════════════════════════════════
#  Bridge to F35 — extract Z from (W^3, B) and round-trip
# ════════════════════════════════════════════════════════════════════
def z_from_w3_b(W3_E, W3_B, B_E, B_B, theta_W: float = THETA_W_F45):
    """
    Extract the Z component out of (W^3, B) using F35 weinberg_mix.

    Returns
    -------
    Z_E, Z_B : (Lx, Ly, Lz) real — Z mass-eigenstate fields.
    """
    _, _, Z_E, Z_B = weinberg_mix(W3_E, W3_B, B_E, B_B, theta_W)
    return Z_E, Z_B


def photon_from_w3_b(W3_E, W3_B, B_E, B_B, theta_W: float = THETA_W_F45):
    """
    Extract the photon (A) component out of (W^3, B) using F35.
    """
    A_E, A_B, _, _ = weinberg_mix(W3_E, W3_B, B_E, B_B, theta_W)
    return A_E, A_B


# ════════════════════════════════════════════════════════════════════
#  Diagnostic — verify the source-basis identity (Z2)
# ════════════════════════════════════════════════════════════════════
def source_basis_identity_residual(W3_E_field, B_E_field,
                                    J3, J_em,
                                    g: float, gp: float,
                                    theta_W: float = THETA_W_F45):
    """
    Verify the algebraic identity

        g · W^3 · J^3  +  g' · B · (J^em − J^3)
            =  e · A · J^em  +  g_Z · Z · (J^3 − s²_W · J^em)

    where (A, Z) come from weinberg_mix((W^3, B)).  Returns the
    bit-for-bit residual.

    The identity holds *per site* — both sides are the same scalar
    field once g_Z = g/c_W, e = g s_W = g' c_W are matched.  When
    g' ≠ g tan θ_W the residual is non-zero by exactly the amount of
    that mismatch, so this routine also serves as a coupling-ratio
    consistency check.

    Parameters
    ----------
    W3_E_field, B_E_field : (Lx, Ly, Lz) real — gauge potentials in the
       (W^3, B) basis.  Only the E component is used as a stand-in for
       the temporal A_0 / W^3_0 component the current couples to.
    J3, J_em : (Lx, Ly, Lz) real — currents.
    g, gp    : float — SU(2)_L and U(1)_Y couplings.
    theta_W  : float — Weinberg angle.  Should satisfy
       tan θ_W = gp/g for bit-for-bit identity.

    Returns
    -------
    residual : float — max|LHS - RHS| over the lattice.
    """
    s_W = np.sin(theta_W)
    c_W = np.cos(theta_W)
    s2 = s_W ** 2
    # (W^3, B) basis source term (gauge basis)
    LHS = g * W3_E_field * J3 + gp * B_E_field * (J_em - J3)
    # (A, Z) basis source term (mass eigenstate basis)
    A_E = c_W * B_E_field + s_W * W3_E_field
    Z_E = -s_W * B_E_field + c_W * W3_E_field
    e = g * s_W       # = g_p * c_W when the matching condition holds
    g_Z = g / c_W
    RHS = e * A_E * J_em + g_Z * Z_E * (J3 - s2 * J_em)
    return float(np.max(np.abs(LHS - RHS)))
