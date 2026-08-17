"""
ca_gravity.py — the gravity field element of the main model (F64 → mainline).

STATUS (2026-06-29, F178): canonical gravity is now the full-tensor induced
Einstein equation G_mu_nu = 8 pi G T_mu_nu.  This dielectric is the
VACUUM / WEAK-FIELD REPRESENTATION of that law (lensing, PPN beta=gamma=1,
redshift) and is correct where T_mu_nu -> 0 or p << rho c^2.  It is NOT the
field equation inside matter: a single scalar forces anisotropic stress (F173),
so the relativistic interior uses full Einstein / TOV (see ca_stellar.py,
theory='gr').  The exact vacuum solution is Schwarzschild; the exponential
K = e^{2u} below is the PPN-order approximation (F178 decision note).

2026-06-06 - 18:20

Gravity in this model is NOT a sourced metric with its own substance: it is a
single impedance-matched lattice **dielectric** K(x,t) renormalising the
(E,B)/spinor rotation rule (F64), canonical form

    K = e^{2u},   u = -Phi/c^2,   A = 1/K,  B = K   (AB ≡ 1 exactly)

which is PPN GR-identical (beta = gamma = 1, D-EM9).  This module promotes the
F64 fork (`forks/gr_fork_F64_em_connection.py`) into the main model structure:

  * the canonical dielectric maps (K_canonical, dielectric_from_phi);
  * the D-EM8 **dynamical field**: Phi obeys its own wave equation
        Box Phi = c_g^{-2} d^2_t Phi - lap Phi = -(4 pi G / c^2) T00,
    leapfrog-stepped (phi_wave_step) — causal, energy-carrying gravity
    (the static limit is exactly the Poisson well);
  * the **F106 sourcing law** — the matter field sources its own dielectric
    through its energy density, with NO free coupling:
        lap ln K = -(8 pi G / c^4) T00[psi] = -(a^2 c_lat / hbar c) T00[psi].
    In lattice natural units (a = tau = hbar = 1, where the SI light speed is
    numerically c = c_lat = 1/sqrt(3) cells/tick) the coefficient is EXACTLY 1:
        lap ln K = -T00          (lattice units)
    equivalently Newton's constant in lattice units is the structural
        G_LATTICE = c_lat^4 / (8 pi) = 1/(72 pi) = 0.0044209...
    (F79 closed form G = a^2 c^3/(8 pi sqrt(3) hbar) evaluated in lattice
    units; identical algebra to F106-E1, exactness row #181);
  * the matter-side coupling: the F62 sign-corrected **local lapse mix**
    (lapse_mix_half) — the rest leg of a massive Dirac state is rescaled by
    sqrt(A(x)) per site around the audited spectral kinetic step
    (Strang: Mix(-dm dt/2) o Kinetic(m0) o Mix(-dm dt/2)), which is the
    free-fall / redshift coupling (F62-D2a/D2b; kinetic-leg c_eff variation
    remains fork-only — the spectral BCC kernels are homogeneous).

Everything here is plain numpy (no scipy), real coefficients, exactly-unitary
matter-side operators.  The fork remains the test bed for the full dynamic
battery (16/16); this module is the production element the casim channel layer
wraps (`casim.engine.core.channels.GravityDielectricChannel`, dynamic mode).

Provenance: F64 (dielectric, D-EM5/8/9), F79 (structural G), F106 (psi->K
sourcing), F62 (lapse-mix sign convention).
"""
from __future__ import annotations

import numpy as np
from casim.constants import (  # noqa: E501
    c_lat,
    F106_COEFF_LATTICE as _F106_COEFF,
    G_LATTICE as _G_LATTICE,
)
from casim.numerics import fft as _fft  # roadmap C1.3: route FFTs through casim.numerics

# ---------------------------------------------------------------------------
# Structural constants (F26 / F79 / F106)
# ---------------------------------------------------------------------------
C_LAT_BCC = c_lat                       # F26: rotation rate, d=3 BCC

#: F106 sourcing coefficient  8 pi G / c^4  in lattice units (a=tau=hbar=1):
#: 8 pi G/c^4 = a^2 c_lat/(hbar c) -> 1 exactly (F106-E1, row #181).
F106_COEFF_LATTICE = _F106_COEFF

#: Newton's constant in lattice units — structural, not a knob:
#: G = a^2 c^3/(8 pi sqrt(3) hbar)  [F79]  ->  c_lat^4/(8 pi) = 1/(72 pi).
G_LATTICE = _G_LATTICE


# ---------------------------------------------------------------------------
# Canonical dielectric maps (F64, D-EM5/D-EM9)
# ---------------------------------------------------------------------------
def K_canonical(u):
    """Canonical dielectric index K = e^{2u} (u = GM/rc^2 = -Phi/c^2).

    AB = 1 exact, PPN beta = gamma = 1 (D-EM9; Mercury-selected nonlinear
    completion of the impedance-matched linear dielectric)."""
    return np.exp(2.0 * np.asarray(u, dtype=np.float64))


def dielectric_from_phi(phi, c0):
    """Map the potential Phi to the canonical dielectric.

    Returns (A, B, K):  u = -Phi/c0^2, K = e^{2u}, A = 1/K, B = K.
    Identical to the fork's `AB_from_phi_dielectric` plus K."""
    u = -np.asarray(phi, dtype=np.float64) / (c0 * c0)
    K = np.exp(2.0 * u)
    return 1.0 / K, K, K


# ---------------------------------------------------------------------------
# F106 source — the matter field's energy density
# ---------------------------------------------------------------------------
def T00_dirac_rest(eta_u, eta_d, chi_u, chi_d, m, sqrtA=1.0):
    """Rest-leg energy density of a massive Dirac state (F106-E5).

    T00 = sqrt(A(x)) * m * |Psi|^2 — exact for a rest eigenstate, the
    leading (nonrelativistic) source for a slow packet.  See
    :func:`T00_dirac_kinetic` for the D-EM3 kinetic leg.

    **Roadmap P3.4 / blocker B5, fixed 2026-07-31 - 23:10.**  This function did
    not sum a leading component axis, while ``T00_field_energy`` thirteen lines
    below always did.  A colour-carrying spinor — a ``quark_dirac`` named in a
    ``gravity_dielectric`` channel's ``sources:`` — has shape ``(3, L, L, L)``,
    so the returned density kept its colour axis, broadcast against the ``(L, L,
    L)`` potential, and **silently promoted the entire gravity state to rank 4**.
    The run did not crash: it produced a three-copy gravitational field, one per
    colour, and reported success.  Colour is not a spatial index and a quark
    does not gravitate three times; the axis is summed, which is the same
    contraction ``T00_field_energy`` performs for the (8,L,L,L) gluon.

    Real states are untouched (a rank-3 input has nothing to sum), so no
    existing result moves — the bug could only fire in a configuration that had
    never been run, which is exactly why it survived.
    """
    d = (np.abs(eta_u) ** 2 + np.abs(eta_d) ** 2
         + np.abs(chi_u) ** 2 + np.abs(chi_d) ** 2)
    d = np.asarray(d, dtype=np.float64)
    while d.ndim > 3:                       # colour / component axes (P3.4)
        d = d.sum(axis=0)
    return sqrtA * float(m) * d


def T00_dirac_kinetic(eta_u, eta_d, chi_u, chi_d, c0=C_LAT_BCC, sqrtA=1.0):
    """Kinetic-leg energy density of a Dirac state (D-EM3, roadmap P3.4).

    The gradient energy the rest leg omits:

    .. math:: u_\\text{kin} = \\sqrt{A}\\,\\frac{c^2}{2}\\sum_\\text{comp}
              |\\nabla\\psi|^2

    evaluated with the same centred difference the lattice Laplacian
    (:func:`lap_nd`) uses, so the two agree on the same field at the same order
    and a gradient energy cannot disagree with the potential it sources.

    Why this matters and is not cosmetic: ``T00_dirac_rest``'s own docstring
    flagged the kinetic term as "fork-level, not yet in the production source",
    and **D-EM3 demands that a fast packet gravitate by its total energy**.  With
    only the rest leg, a packet boosted to relativistic momentum sources exactly
    the same gravity as one at rest — the equivalence of mass and energy is
    absent from the production gravity source.  This restores it.

    The leg is additive: ``T00_dirac_rest(...) + T00_dirac_kinetic(...)`` is the
    total.  It is supplied as a separate function rather than folded into the
    rest leg so every committed rest-leg result stays reproducible and the two
    can be compared, which is what makes the D-EM3 claim testable.
    """
    out = None
    for comp in (eta_u, eta_d, chi_u, chi_d):
        psi = np.asarray(comp)
        if psi.size == 0:
            continue
        acc = np.zeros(psi.shape, dtype=np.float64)
        for ax in range(psi.ndim):
            d = 0.5 * (np.roll(psi, -1, ax) - np.roll(psi, 1, ax))
            acc = acc + np.abs(d) ** 2
        out = acc if out is None else out + acc
    if out is None:
        return 0.0
    while out.ndim > 3:                     # colour / component axes
        out = out.sum(axis=0)
    return sqrtA * 0.5 * float(c0) ** 2 * out


def T0i_dirac(eta_u, eta_d, chi_u, chi_d, c0=C_LAT_BCC):
    """Momentum density :math:`T^{0i} = c\\,\\mathrm{Im}(\\psi^\\dagger\\partial_i\\psi)`.

    Roadmap P3.4 asks for "momentum density :math:`T^{0i}` at minimum, since a
    scalar :math:`\\Phi` cannot represent a moving source" — a static potential
    sourced from :math:`T^{00}` alone knows a packet's *location* but not its
    *motion*, so frame-dragging and the gravitomagnetic sector are structurally
    absent rather than small.

    Returns an array with a leading axis of length ``ndim`` (the spatial index
    :math:`i`), each component a real density on the lattice.  Component and
    colour axes are summed, as everywhere else in this module.
    """
    comps = [np.asarray(c) for c in (eta_u, eta_d, chi_u, chi_d)
             if np.asarray(c).size]
    if not comps:
        return np.zeros((3,))
    ndim = min(c.ndim for c in comps)
    spatial = min(ndim, 3)
    legs = []
    for ax in range(spatial):
        acc = None
        for psi in comps:
            a = psi.ndim - spatial + ax     # spatial axes are trailing
            d = 0.5 * (np.roll(psi, -1, a) - np.roll(psi, 1, a))
            t = np.imag(np.conj(psi) * d)
            acc = t if acc is None else acc + t
        acc = np.asarray(acc, dtype=np.float64)
        while acc.ndim > 3:
            acc = acc.sum(axis=0)
        legs.append(float(c0) * acc)
    return np.asarray(legs)


def dielectric_mix_half(E, B, K, omega0, dt=1.0):
    """Half-step eikonal dielectric mix for an (E,B) pair — roadmap P3.6.

    **SUPERSEDED (F271, 2026-08-01) for the photon channel** by
    ``casim.engine.gauge.photon.photon_step_dielectric``, which resolves
    Omega(k)/K(x) mode by mode instead of about a single stated rate omega0,
    has NO free parameter, is EXACT for a uniform K, and converges at second
    order. Retained as the comparison object and because it is exactly
    orthogonal pointwise, which the k-resolved form is only convergently —
    that makes it a useful control, not a fallback. Do not wire it into a new
    channel.

    The gauge-sector counterpart of :func:`lapse_mix_half`.  The F64 dielectric
    renormalises the *local* rotation rate of the real (E,B) pair: where K > 1
    the pair turns more slowly, which is what makes a ray bend.  This applies
    the accumulated rate difference as a **rotation in the (E,B) plane**

    .. math:: \\begin{pmatrix}E\\\\B\\end{pmatrix} \\leftarrow
              \\begin{pmatrix}\\cos\\delta & -\\sin\\delta\\\\
                              \\sin\\delta & \\cos\\delta\\end{pmatrix}
              \\begin{pmatrix}E\\\\B\\end{pmatrix},\\qquad
              \\delta(x) = \\tfrac{\\Delta t}{2}\\,\\omega_0
              \\left(\\tfrac{1}{K(x)} - 1\\right)

    used Strang-wise around the homogeneous spectral step, exactly as
    :func:`lapse_mix_half` is used around the spectral kinetic step for the
    fermion rest leg (F62-D2a/D2b).

    Two properties are worth stating because they are what make it safe:

    * **Exactly norm-preserving.**  The mix is a real orthogonal rotation at
      every site, so :math:`E^2+B^2` is conserved *pointwise*, not just in sum.
      The dielectric therefore cannot manufacture or leak field energy, and the
      P3.5 ``TotalEnergy`` gate stays meaningful with gravity switched on.
    * **Exactly the identity at K ≡ 1.**  :math:`\\delta \\equiv 0`, so a
      scenario with no gravity partner — or a flat one — is bit-identical to the
      pre-P3.6 engine.  No committed result moves.

    **This is the eikonal (leading-order) coupling, and it is labelled as such
    deliberately.**  :math:`\\omega_0` is a single representative rotation rate,
    so the mix is exact only in the geometric-optics limit where the packet is
    narrow in k.  The rate difference is genuinely k-dependent
    (:math:`\\Omega(k)/K` versus :math:`\\Omega(k)`), and a position-dependent,
    k-dependent rate cannot be applied by one homogeneous FFT — which is exactly
    why the spectral BCC kernels were called homogeneous and the deflection was
    left fork-only.  The exact treatment needs either a variable-c stepper of
    the ``weyl_step_2d_varc_strang`` kind lifted to 3-D (E,B), or a multiplicative
    operator split with a k-resolved local rate; **that derivation is open and
    is not claimed here.**  What is claimed is narrower and checkable: the
    production engine now closes the loop at eikonal order, deflection is
    measurable outside the fork, and the coupling is unitary.

    ``omega0`` is required, not defaulted, because a silently-chosen central
    rate is a fitted parameter wearing a default's clothing.
    """
    K = np.asarray(K, dtype=np.float64)
    delta = 0.5 * float(dt) * float(omega0) * (1.0 / K - 1.0)
    c, s = np.cos(delta), np.sin(delta)
    E = np.asarray(E)
    B = np.asarray(B)
    if E.ndim > K.ndim:                 # (components, L, L, L) against (L,L,L)
        c = c[None, ...]
        s = s[None, ...]
    return c * E - s * B, s * E + c * B


def T00_field_energy(E, B):
    """Energy density of an (E,B) field state: u = (E^2+B^2)/2, summed over
    leading component axes if present (the D-EM3 radiation source)."""
    E = np.asarray(E, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)
    u = 0.5 * (E * E + B * B)
    while u.ndim > 3:
        u = u.sum(axis=0)
    return u


def phi_source(T00, c0, coupling=F106_COEFF_LATTICE):
    """RHS of the Poisson/wave equation for Phi from the F106 law.

    lap ln K = -coupling * T00  with  ln K = -2 Phi/c0^2  gives
    lap Phi = (coupling * c0^2 / 2) * T00.

    `coupling` is the F106 coefficient 8 pi G/c^4; in lattice units it is
    exactly 1 (structural).  Passing another value is a *scenario scaling
    choice* (weak-field demos on small lattices), not free physics."""
    return (float(coupling) * c0 * c0 / 2.0) * np.asarray(T00, dtype=np.float64)


# ---------------------------------------------------------------------------
# Static (Poisson) and dynamical (D-EM8) field equations
# ---------------------------------------------------------------------------
def lap_nd(P):
    """6/4/2-neighbour Laplacian (unit spacing), any dimension, periodic."""
    out = -2.0 * P.ndim * P
    for ax in range(P.ndim):
        out = out + np.roll(P, 1, ax) + np.roll(P, -1, ax)
    return out


def solve_phi_poisson(src, stencil=True):
    """Static limit: solve lap Phi = src (zero-mean source) by FFT.

    With ``stencil=True`` (default) the inverted operator is the exact
    symbol of `lap_nd` (the 2d-neighbour stencil), -4 sum_i sin^2(k_i/2),
    so the returned Phi is the EXACT static fixed point of `phi_wave_step`
    (lap_nd(Phi) == src to round-off).  ``stencil=False`` inverts the
    continuum -k^2 (the F58 4 pi Green's-function limit).  Periodic,
    zero-mean.  For an open-boundary 1/r field use
    `poisson_open.solve_poisson_3d_open` (the casim static lens path)."""
    src = np.asarray(src, dtype=np.float64)
    src = src - src.mean()
    k = [np.fft.fftfreq(n) * 2.0 * np.pi for n in src.shape]
    KK = np.meshgrid(*k, indexing="ij")
    if stencil:
        k2 = sum(4.0 * np.sin(K / 2.0) ** 2 for K in KK)
    else:
        k2 = sum(K * K for K in KK)
    k2.flat[0] = 1.0
    Pk = -_fft.fftn(src) / k2
    Pk.flat[0] = 0.0
    phi = np.real(_fft.ifftn(Pk))
    return phi - phi.mean()


def phi_wave_step(phi, phi_prev, src, c_g, dt):
    """One D-EM8 leapfrog tick of  d^2_t Phi = c_g^2 (lap Phi - src).

    Static fixed point: lap Phi = src (the Poisson well that sources K).
    Free disturbances propagate causally at c_g; the free field conserves
    E = 1/2 sum (d_t Phi)^2 + 1/2 c_g^2 sum |grad Phi|^2  (D-EM8, F64).
    Returns (phi_new, phi)  — the caller keeps (phi, phi_prev) rolling."""
    phi_new = (2.0 * phi - phi_prev
               + (c_g * dt) ** 2 * (lap_nd(phi) - np.asarray(src)))
    return phi_new, phi


def phi_field_energy(phi, phi_prev, c_g, dt):
    """Free-field energy of the dynamical Phi (D-EM8 diagnostic)."""
    vel = (phi - phi_prev) / dt
    e = 0.5 * np.sum(vel * vel)
    for ax in range(phi.ndim):
        g = 0.5 * (np.roll(phi, -1, ax) - np.roll(phi, 1, ax))
        e += 0.5 * c_g * c_g * np.sum(g * g)
    return float(e)


# ---------------------------------------------------------------------------
# Matter-side coupling — the F62 sign-corrected local lapse mix
# ---------------------------------------------------------------------------
def lapse_mix_half(eta_u, eta_d, chi_u, chi_d, sqrtA, m, dt=1.0):
    """Half-tick local rest-leg lapse rescaling for a massive Dirac state.

    Strang leg:  Mix(theta) with theta = -dm*dt/2,  dm(x) = (sqrtA(x)-1)*m,
    so the effective site mass is M(x) = m + dm = sqrt(A(x))*m while the
    audited spectral kinetic step keeps the baseline m.  SIGN: the exact-QCA
    kinetic block carries the mass as +i*m (generator -m*beta), so dm must
    enter with the matching sign — theta = -dm*dt/2 — or a mass gradient
    repels (the latent `dirac_step_2d_varm_splitstep` sign error F62
    uncovered).  Exactly unitary per cell (a rotation); sqrtA == 1 returns
    the state bit-for-bit (cos 0 = 1, sin 0 = 0 exactly in IEEE).

    Apply once before and once after the audited Dirac step.
    """
    theta = -((np.asarray(sqrtA, dtype=np.float64) - 1.0) * float(m)) * dt * 0.5
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    eu = cos_t * eta_u - 1j * sin_t * chi_u
    ed = cos_t * eta_d - 1j * sin_t * chi_d
    xu = cos_t * chi_u - 1j * sin_t * eta_u
    xd = cos_t * chi_d - 1j * sin_t * eta_d
    return eu, ed, xu, xd


__all__ = [
    "C_LAT_BCC", "F106_COEFF_LATTICE", "G_LATTICE",
    "K_canonical", "dielectric_from_phi", "dielectric_mix_half",
    "T00_dirac_rest", "T00_dirac_kinetic", "T0i_dirac",
    "T00_field_energy", "phi_source",
    "lap_nd", "solve_phi_poisson", "phi_wave_step", "phi_field_energy",
    "lapse_mix_half",
]
