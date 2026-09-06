"""
qed_uv_completion.py — the UV sector reconciled: a physical cutoff AND a
counterterm program  (completeness row A11; F116/F164/F264/F284)
=============================================================================

Created: 2026-08-16 - 17:10

**The contradiction this closes.**  Completeness row A11 has read ``PARTIAL``
and "unmoved for three reports" with a one-line diagnosis:

    The BZ edge is a *physical* cutoff, yet F264 runs the full renormalisation
    program with counterterms on top.  F284 sec.5 sharpens the first picture
    without reconciling it with the second.  Both individually sound, nowhere
    reconciled.

They are reconciled by the Wilsonian dictionary, which this tree has never
written down: ``grep -ri "wilson"`` in this repo returns the Wilson gauge
*action* and the Wilson lattice-to-MSbar constant, never Wilson's
renormalisation group.  The dictionary in one line:

    On a physical cutoff there are no divergences, so a counterterm is not a
    subtraction of an infinity.  It is the FINITE map from bare lattice
    parameters to measured ones.  F264's theorem -- ``D = 4 - (3/2)E_f -
    E_gamma`` with ``dD/dV = dD/dL = 0`` -- is unchanged; what changes is what
    it MEANS.  In the continuum it says "finitely many counterterms absorb the
    infinities".  Here it says "finitely many operator coefficients carry the
    cutoff", which is a strictly stronger and entirely finite statement.

That much is a re-reading.  The content is what the re-reading then forces, and
two of the results were not previously in the tree:

U5  **The model's leading irrelevant operator is dimension-6, and its
    coefficient is an exact rational.**  For the F69 paired photon,

        [Omega_pair(k) - c_lat|k|] / (c_lat|k|)
             = -(1 - sum_i nhat_i^4)/144 * |k|^2  -  (nhat_x nhat_y nhat_z)^2/24 * |k|^2
               + O(|k|^4)

    verified to 1.1e-20 over nine directions in 60-digit arithmetic.  There is
    **no O(|k|) term**: the model has no dimension-5 Lorentz-violating photon
    operator at all, which is the one that GRB/AGN polarimetry bounds at the
    1e-30 level.  The coefficient is bounded exactly, |.| <= |k|^2/162, with
    equality along <111> and identically zero along <100> (where the dispersion
    is linear to all orders -- F301's 3.5e-46).

U8  **The Lambda^4 and Lambda^2 Sakharov sectors are not independently
    tunable, and that EXCLUDES F164's own leading cancellation channel.**
    F164 offers three candidate resolutions of its 120.8-order cosmological-
    constant overshoot and calls channel (i) -- "the CA ontic vacuum has zero
    zero-point energy, so the bare CC is 0" -- the leading, elegant-design-
    preferred one.  But F59 assembles ``1/(16 pi G)`` from
    ``int d3k/(2 omega)`` and F164 assembles ``rho_vac`` from
    ``int d3k omega/2`` **over the same modes, the same measure and the same
    factor of 1/2**.  They are two moments of one zero-point sum.  Weight that
    sum by a uniform ``lambda`` and BOTH move.  Demanding the model reproduce
    the measured G and the measured rho_Lambda is then a 2x2 system in
    ``(lambda, a)`` with a unique solution:

        a*      = a_0 * sqrt(rho_vac/rho_Lambda) = 2.56e26 m   (~8.3 Gpc)
        lambda* = rho_vac/rho_Lambda             = 5.8e120

    A lattice cell 0.58x the comoving radius of the observable universe, and a
    zero-point weight 121 orders above the canonical 1/2.  The uniform channel
    is excluded -- not disfavoured, over-determined into absurdity.  Note the
    SIGN: lambda* is an *enhancement*.  Suppressing the mode sum to fix the CC
    makes G worse, and re-fixing G by shrinking ``a`` makes the CC worse again,
    because rho_vac ~ lambda/a^4 while 1/G ~ lambda/a^2.  The two sectors pull
    opposite ways.

    What survives is the ORDER-SELECTIVITY requirement, and it is the honest
    statement of what A11 still owes:  a viable mechanism must suppress the
    heat-kernel ``a_0`` coefficient by >= 121 decades while perturbing ``a_1``
    by <= 2.2e-5 (CODATA's relative uncertainty on G) -- a relative
    selectivity between two ADJACENT heat-kernel coefficients of >= 1e116.
    Channel (ii) (sequestering) is order-selective by construction and is
    promoted to sole survivor; channel (iii) was already only a consistency
    statement.  This REORDERS F164's own candidate list on the model's own
    arithmetic.

The remaining legs are the dictionary made checkable.

U1  The lattice loop is finite; the continuum one is not.  Same integrand.
U2  The lattice-vs-continuum scheme difference is IR-INDEPENDENT (drift 3.1e-11
    over the last decade of m).  That is exactly the property that licenses one
    regulator's counterterm to absorb the other's -- and therefore the property
    that makes F264 legitimate on top of a physical cutoff.
U3  The log coefficient 1/(16 pi^2) is universal across four schemes (BZ
    lattice, hard sphere, Pauli-Villars, dimensional) -- scheme-INdependent,
    which is why b_0 = 4/3 (F251) is physics and the constant is not.
U4  Two lattice schemes differ by a constant computable at literally m = 0,
    because the difference integrand decays as t^-2 with no regulator needed.
U6  Decoupling, quantified at the scales anyone measures.
U7  The whole domain of the theory is perturbative; the Landau pole is 258.9
    decades outside it (re-verifies F264 R8 against the constants registry).
U9  The Lambda-sensitivity ledger: exactly TWO coefficients have no free
    parameter to absorb them, and they are the two Sakharov sectors.  The model
    gets one right (G, F79/F107) and one wrong by 120.8 orders (rho_vac).
    A11's residual is therefore ONE NUMBER, and it is named.

--------------------------------------------------------------------------
Numerics note
--------------------------------------------------------------------------
The one-loop log-divergent scalar structure is evaluated in the Schwinger
representation, which turns a 4-D BZ integral into a 1-D one:

    I_lat(m) = int_0^inf dt t e^{-t m^2} D(t)^4,
    D(t)     = int_{-pi}^{pi} dk/(2pi) exp(-t khat^2(k))

``D`` is computed by the periodic trapezoid, which is spectrally accurate on a
smooth periodic integrand -- it reproduces the closed form ``e^{-2t} I_0(2t)``
for the Wilson symbol to 2.2e-16 without importing ``scipy.special`` (D8: this
module imports numerics only through ``casim.numerics``).  The t-integral is
truncated at ``T_MAX``; the neglected tail is bounded analytically inside
``_tail_bound`` and reported in the payload rather than assumed small.
"""
from __future__ import annotations

import json
import math
import os
from fractions import Fraction

from casim.numerics import xp as np

from casim.constants import (c_lat, a_over_ellP, ell_P_m, hbar_SI, c_SI,
                             J_per_GeV, m_e_GeV)

__all__ = [
    "bz_factor", "I_lattice", "I_continuum_sphere", "scheme_constant",
    "dispersion_excess", "dispersion_excess_closed_form",
    "dispersion_excess_mp", "closed_form_mp",
    "sakharov_moments", "two_sector_solve",
    "run", "check_uv_completion",
]

# ---------------------------------------------------------------------------
# housekeeping
# ---------------------------------------------------------------------------
INV16PI2 = 1.0 / (16.0 * math.pi ** 2)
NK_DEFAULT = 8192          # periodic-trapezoid points for the 1-D BZ factor
T_MAX = 1.0e4              # Schwinger cut; the residual past it is CORRECTED
                           # analytically and the correction's own error measured
NT_DEFAULT = 4000          # log-grid points in t


def _results_path(name: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        cand = os.path.join(here, "test-results")
        if os.path.isdir(cand):
            return os.path.join(cand, name)
        parent = os.path.dirname(here)
        if parent == here:
            raise RuntimeError("cannot locate test-results/ above " + __file__)
        here = parent


# ---------------------------------------------------------------------------
# U1-U4 : the one-loop log structure in four regularisation schemes
# ---------------------------------------------------------------------------
def bz_factor(t, scheme: str = "wilson", nk: int = NK_DEFAULT):
    """``D(t) = int dk/(2pi) exp(-t khat^2)`` for one lattice direction.

    ``wilson``   khat^2 = 4 sin^2(k/2)                     (closed form e^-2t I_0(2t))
    ``symanzik`` khat^2 = khat^2_W + khat^4_W / 12         (tree-level improved)

    Both approach ``k^2`` as ``k -> 0``, so both carry the SAME 1/(4 pi t)^(1/2)
    large-t asymptotics and therefore the same universal log.  They differ at
    O(k^4), which is precisely a scheme choice.
    """
    k = -math.pi + 2.0 * math.pi * np.arange(nk) / nk
    kh2 = 4.0 * np.sin(k / 2.0) ** 2
    if scheme == "wilson":
        sym = kh2
    elif scheme == "symanzik":
        sym = kh2 + kh2 * kh2 / 12.0
    else:
        raise ValueError(f"unknown lattice scheme {scheme!r}")
    t_arr = np.atleast_1d(np.asarray(t, dtype=float))
    out = np.array([float(np.mean(np.exp(-tv * sym))) for tv in t_arr])
    return out if np.ndim(t) else float(out[0])


def _t_grid(nt: int = NT_DEFAULT, t_min: float = 1.0e-8, t_max: float = T_MAX):
    return np.exp(np.linspace(math.log(t_min), math.log(t_max), nt))


def _asymptotic_defect(t_max: float, scheme: str, nk: int) -> float:
    """``eps(T) = P(T) (4 pi T)^2 - 1`` -- how far the kernel still is from its
    continuum asymptote at the Schwinger cut.

    MEASURED, not assumed.  An earlier draft of this module hard-coded
    ``eps = 1e-7`` calibrated off the Symanzik kernel; the Wilson kernel is
    2500x further from its asymptote at the same ``t`` (it is the unimproved
    action, so it approaches as ``0.25/t`` rather than ``1/t^2``), and the
    resulting 1.6e-6 truncation error showed up as a disagreement between U4's
    two independent routes.  That disagreement is why this is measured.
    """
    P = float(bz_factor(t_max, scheme=scheme, nk=nk)) ** 4
    return P * (4.0 * math.pi * t_max) ** 2 - 1.0


def _tail_correction(t_max: float, m2: float, scheme: str, nk: int) -> float:
    """The Schwinger mass past ``t_max``, added analytically.

    Past the cut the PV-subtracted integrand is ``eps(t)/(16 pi^2 t)`` (the
    leading ``1/(16 pi^2 t)`` cancels against PV identically).  ``eps`` falls as
    ``1/t``, so writing ``eps(t) = eps(T) T/t`` gives

        int_T^inf eps(T) T /(16 pi^2 t^2) dt = eps(T)/(16 pi^2),

    modulated by ``e^{-T m^2}`` which is 1 for every ``m`` used here.
    """
    eps = _asymptotic_defect(t_max, scheme, nk)
    return eps * INV16PI2 * math.exp(-t_max * m2)


def I_lattice_minus_pv(m2: float, scheme: str = "wilson", M2_pv: float = 1.0,
                       nt: int = NT_DEFAULT, nk: int = NK_DEFAULT):
    """``I_lat(m) - I_PV(m, M)`` -- the lattice scheme constant, PV-referenced.

    ``I_PV(m,M) = ln(M^2/m^2)/(16 pi^2)`` EXACTLY, so with ``M = 1`` this returns
    ``lim I_lat(m) + ln(m^2)/(16 pi^2)``: the constant the counterterm carries.

    The subtracted integrand is finite at both ends -- ``t P(t) -> t`` at small
    ``t`` while the PV kernel tends to ``(M^2-m^2)/16 pi^2``; at large ``t`` the
    ``1/(16 pi^2 t)`` pieces cancel identically.  That is the whole point: the
    difference between a compact-BZ regulator and a continuum one is a
    convergent integral, hence a finite number.
    """
    t = _t_grid(nt, t_max=T_MAX)
    P = bz_factor(t, scheme=scheme, nk=nk) ** 4
    integrand = t * np.exp(-t * m2) * P \
        - (np.exp(-t * m2) - np.exp(-t * M2_pv)) * INV16PI2 / t
    # trapezoid in ln t
    lt = np.log(t)
    val = float(np.trapezoid(integrand * t, lt))
    # small-t remainder below t_min: integrand -> t - (M2-m2)/(16 pi^2), analytic
    t0 = float(t[0])
    val += 0.5 * t0 * t0 - (M2_pv - m2) * INV16PI2 * t0
    corr = _tail_correction(T_MAX, m2, scheme, nk)
    # residual after the correction: the 1/t model is itself good to ~eps, so
    # what is left is second order in eps.
    resid = abs(corr) * abs(_asymptotic_defect(T_MAX, scheme, nk))
    return val + corr, resid


def I_lattice(m2: float, scheme: str = "wilson", **kw):
    """``I_lat(m)`` itself, via the PV-referenced constant plus the exact PV log."""
    const, bound = I_lattice_minus_pv(m2, scheme=scheme, **kw)
    return const + INV16PI2 * math.log(1.0 / m2), bound


def I_continuum_sphere(m2: float, Lam2: float) -> float:
    """Hard 4-sphere cutoff, closed form.  Diverges logarithmically in Lam."""
    return (math.log((Lam2 + m2) / m2) - Lam2 / (Lam2 + m2)) * INV16PI2


def scheme_constant(scheme_a: str = "wilson", scheme_b: str = "symanzik",
                    nt: int = NT_DEFAULT, nk: int = NK_DEFAULT) -> float:
    """``lim_{m->0} [I_a(m) - I_b(m)]``, computed at LITERALLY m = 0.

    Both kernels share the leading ``(4 pi t)^-2``, so the difference integrand
    decays as ``t^-2`` and the integral converges with no IR regulator at all.
    This is the sharpest form of "the scheme dependence is IR-blind": it is not
    that the m-dependence cancels to some tolerance, it is that m never appears.
    """
    t = _t_grid(nt, t_max=T_MAX)
    Pa = bz_factor(t, scheme=scheme_a, nk=nk) ** 4
    Pb = bz_factor(t, scheme=scheme_b, nk=nk) ** 4
    lt = np.log(t)
    val = float(np.trapezoid(t * (Pa - Pb) * t, lt))
    t0 = float(t[0])
    val += 0.5 * t0 * t0 * float(Pa[0] - Pb[0])
    # analytic tail: t(Pa-Pb) -> C/t^2, so int_T^inf = C/T with C = T^3 (Pa-Pb)
    C = T_MAX ** 3 * float(Pa[-1] - Pb[-1])
    return val + C / T_MAX


def log_coefficient(scheme: str = "wilson", t_probe: float = 1.0e5,
                    nk: int = NK_DEFAULT) -> float:
    """The coefficient of ``ln(1/m^2)``, read off WITHOUT integrating over t.

    ``I(m) = int dt t e^{-t m^2} P(t)``, so the log comes entirely from the
    large-``t`` tail: if ``P(t) -> c/t^2`` then ``I -> c ln(1/m^2)``.  So the
    coefficient IS ``lim_{t->inf} t^2 P(t)``, and it can be read directly off
    the kernel.

    This is the whole universality argument in one line: ``t^2 P(t)`` depends
    only on ``D(t) -> (4 pi t)^{-1/2}``, which is fixed by ``khat^2 -> k^2`` as
    ``k -> 0``.  EVERY regulator in the class has that limit -- that is what
    makes it a regulator -- so every one of them returns ``1/(16 pi^2)``.  The
    log coefficient is scheme-INdependent (hence ``b_0`` is physics, F251); the
    constant is scheme-dependent (hence it is a counterterm, F264).

    Reading it off the kernel rather than the integral also removes the
    truncation the t-integral would need: no cut, no tail, no model.
    """
    P = float(bz_factor(t_probe, scheme=scheme, nk=nk)) ** 4
    return t_probe ** 2 * P


# ---------------------------------------------------------------------------
# U5-U6 : the leading irrelevant operator of the photon sector
# ---------------------------------------------------------------------------
def _unit(nvec):
    v = np.asarray(nvec, dtype=float)
    return v / math.sqrt(float(np.sum(v * v)))


def dispersion_excess_closed_form(nvec) -> float:
    """The derived coefficient of ``|k|^2`` in ``dOmega/Omega`` along ``nhat``.

        -(1 - S4)/144 - T2/24,     S4 = sum nhat_i^4,  T2 = (nx ny nz)^2

    Cubic-harmonic content: a degree-4 invariant (S4) and a degree-6 one (T2).
    Range is exactly ``[-1/162, 0]`` -- 0 along <100>, -1/162 along <111>.
    """
    n = _unit(nvec)
    S4 = float(np.sum(n ** 4))
    T2 = float((n[0] * n[1] * n[2]) ** 2)
    return -(1.0 - S4) / 144.0 - T2 / 24.0


def dispersion_excess(nvec, kmag: float, linear_control: bool = False) -> float:
    """Measured ``[Omega_pair - c_lat|k|]/(c_lat|k|) / |k|^2`` from the engine.

    Uses the canonical paired-spinor photon (F67-F69), i.e. the propagator the
    model actually runs, not a model of it.
    """
    from casim.engine.gauge.photon import pair_dispersion
    n = _unit(nvec)
    if linear_control:
        return 0.0
    k = kmag * n
    Om = float(pair_dispersion(float(k[0]), float(k[1]), float(k[2])))
    lin = float(c_lat) * kmag
    return (Om - lin) / lin / kmag ** 2


def closed_form_mp(nvec, dps: int = 60) -> "object":
    """``-(1 - S4)/144 - T2/24`` evaluated in ``dps`` digits.

    Needed because the float64 evaluation of the closed form is itself good to
    only a few ulp (1.7e-18 on a 3.5e-3 quantity), which would otherwise be
    mistaken for a defect in the derivation.  Exact is compared against exact.
    """
    import mpmath as mp
    with mp.workdps(dps):
        v = [mp.mpf(int(x)) for x in nvec]
        nrm = mp.sqrt(sum(x * x for x in v))
        n = [x / nrm for x in v]
        S4 = sum(x ** 4 for x in n)
        T2 = (n[0] * n[1] * n[2]) ** 2
        return -(1 - S4) / mp.mpf(144) - T2 / mp.mpf(24)


def dispersion_excess_mp(nvec, kmag: str = "1e-10", dps: int = 60) -> float:
    """The same excess in ``dps``-digit arithmetic, reimplementing the F26 BCC
    symbol from its definition.

    Why this leg exists.  The shipped ``pair_dispersion`` is float64 and
    ``arccos`` is badly conditioned near argument 1: at ``|k| = 1e-2`` the
    excess being measured is 6e-7 of a quantity of order 1e-2, and the
    derivative ``d arccos/du ~ 200`` turns the last bit of ``u`` into ~7e-8 of
    coefficient error.  So the float route can confirm the closed form to about
    1e-7 and no further, and that is a property of the PROBE, not of the
    physics.  This route removes the probe: it reproduces the engine's exact
    convention (``cos(k_i c_lat)``, argument ``k/2`` from the pair) and lands
    the same closed form to 1.1e-20 over nine directions.

    The two legs together say: the closed form is exact (this), and the module
    that ships is faithful to it at float precision (the other).
    """
    import mpmath as mp
    with mp.workdps(dps):
        r3 = mp.sqrt(3)
        v = [mp.mpf(int(x)) for x in nvec]
        nrm = mp.sqrt(sum(x * x for x in v))
        n = [x / nrm for x in v]
        km = mp.mpf(kmag)
        tot = mp.mpf(0)
        for sgn in (1, -1):
            q = [km * x / (2 * r3) for x in n]      # pair: k/2 ; F26: k * c_lat
            c = [mp.cos(x) for x in q]
            sn = [mp.sin(x) for x in q]
            tot += mp.acos(c[0] * c[1] * c[2] + sgn * sn[0] * sn[1] * sn[2])
        lin = km / r3
        return (tot - lin) / lin / km ** 2


def lambda_uv_GeV() -> float:
    """``Lambda_UV = hbar c / a`` at the F107 canonical cell, in GeV."""
    a_m = float(a_over_ellP) * float(ell_P_m)
    joule_per_GeV = float(J_per_GeV)
    return float(hbar_SI) * float(c_SI) / a_m / joule_per_GeV


# ---------------------------------------------------------------------------
# U8 : the two Sakharov moments and the over-determination
# ---------------------------------------------------------------------------
def sakharov_moments(n: int = 90, sign: str = "+"):
    """The two Sakharov BZ moments of ONE zero-point sum, on the F26 dispersion.

    ``I_cc = <omega/2>``   sources rho_vac  (the Lambda^4 / heat-kernel a_0 sector, F164)
    ``I_g  = <1/(2 omega)>`` sources 1/G    (the Lambda^2 / heat-kernel a_1 sector, F59)

    The point of computing them together, in one function, over one grid, is
    that it makes the shared factor of 1/2 impossible to overlook: any mechanism
    acting on "the zero-point 1/2" acts on both moments by the same factor.
    """
    from casim.engine.lattice.bcc import bcc_dispersion
    L = 2.0 * math.pi * math.sqrt(3.0)          # period in the code's k convention
    g = (np.arange(n) + 0.5) / n * L - L / 2.0
    kx, ky, kz = np.meshgrid(g, g, g, indexing="ij")
    w = bcc_dispersion(kx, ky, kz, sign)
    dv = (L / n) ** 3 / (2.0 * math.pi) ** 3
    I_cc = float(np.sum(w / 2.0) * dv)
    inv = np.where(w > 1e-12, 1.0 / (2.0 * np.maximum(w, 1e-300)), 0.0)
    I_g = float(np.sum(inv) * dv)
    return I_cc, I_g


RHO_LAMBDA_SI = 6.0e-10        # observed dark-energy density, J/m^3 (Planck 2018)
G_REL_UNCERTAINTY = 2.2e-5     # CODATA 2018 relative uncertainty on G


def two_sector_solve(zero_point_weight: float = 1.0, g_star: float = 2.0,
                     n: int = 90):
    """Solve for the ``(lambda, a)`` that would reproduce BOTH G and rho_Lambda.

    With a uniform weight ``lambda`` on the zero-point sum,

        1/(16 pi G) ~ lambda / a^2          (F59 Part C, the Lambda^2 sector)
        rho_vac     ~ lambda / a^4          (F164 Part A, the Lambda^4 sector)

    Fixing G pins ``lambda/a^2``; fixing rho_vac pins ``lambda/a^4``.  Two
    equations, two unknowns, ONE solution -- and it is absurd.  Because the two
    sectors carry different powers of ``a``, they cannot be satisfied together
    by any uniform reweighting; that is the exclusion.
    """
    I_cc, I_g = sakharov_moments(n=n)
    a0 = float(a_over_ellP) * float(ell_P_m)
    hbarc = float(hbar_SI) * float(c_SI)
    rho0 = zero_point_weight * g_star * math.sqrt(3.0) * I_cc * hbarc / a0 ** 4
    R = rho0 / RHO_LAMBDA_SI                      # the overshoot
    a_star = a0 * math.sqrt(R)                    # from lambda/a^2 and lambda/a^4
    lambda_star = R
    return {
        "I_cc": I_cc, "I_g": I_g, "a0_m": a0,
        "rho_vac_SI": rho0, "rho_Lambda_SI": RHO_LAMBDA_SI,
        "overshoot": R, "log10_overshoot": math.log10(R),
        "a_star_m": a_star, "a_star_Gpc": a_star / 3.0856775814913673e25,
        "lambda_star": lambda_star,
        # order-selectivity the surviving mechanism must supply
        "required_a0_suppression_decades": math.log10(R),
        "allowed_a1_perturbation": G_REL_UNCERTAINTY,
        "required_selectivity": R * G_REL_UNCERTAINTY,
        "log10_required_selectivity": math.log10(R * G_REL_UNCERTAINTY),
    }


# ---------------------------------------------------------------------------
# U9 : the Lambda-sensitivity ledger
# ---------------------------------------------------------------------------
#  (operator, mass dim, superficial D, free parameter available?, disposition)
UV_LEDGER = (
    ("identity  (cosmological constant)", 0, 4, False,
     "UNABSORBABLE -- no CC parameter exists; F164's 120.8-order overshoot"),
    ("R  (Einstein-Hilbert, 1/16 pi G)", 2, 2, False,
     "UNABSORBABLE -- G is structural (F79); the induced value IS the "
     "prediction, and it lands (F107)"),
    ("psi_bar i gamma.d psi   (Z_2)", 4, 0, True, "absorbed (F264 R2/R3)"),
    ("e psi_bar gamma.A psi   (Z_1)", 4, 0, True, "absorbed (F264 R2/R3)"),
    ("m psi_bar psi           (dm)", 4, 0, True, "absorbed (F264 R2/R3)"),
    ("F_munu F^munu           (Z_3)", 4, 0, True, "absorbed (F264 R2/R3)"),
    ("A_mu A^mu  (photon mass)", 2, 2, False,
     "FORBIDDEN, not unabsorbable -- q_mu Pi^munu = 0 exactly (F251/Pi1)"),
    ("dimension >= 6", 6, -2, True,
     "IRRELEVANT -- suppressed by (E/Lambda_UV)^2; U5/U6 measure the "
     "coefficient and it is exactly rational"),
)


def superficial_degree():
    """Re-derive ``D = 4 - (3/2) E_f - E_gamma`` and its V/L-independence.

    F264 R1 owns this; it is re-verified here because U9 REINTERPRETS it, and a
    reinterpretation that quietly assumed its own premise would be worthless.
    """
    import sympy as sp
    L, If, Ig, V, Ef, Eg = sp.symbols("L I_f I_g V E_f E_gamma")
    sol = sp.solve([sp.Eq(L, If + Ig - V + 1),
                    sp.Eq(2 * V, 2 * If + Ef),
                    sp.Eq(V, 2 * Ig + Eg)], [L, If, Ig], dict=True)[0]
    D = sp.simplify((4 * L - If - 2 * Ig).subs(sol))
    dV = sp.simplify(sp.diff(D, V))
    dL = sp.simplify(sp.diff(sp.expand(D), L))
    return D, dV, dL


# ---------------------------------------------------------------------------
# the record entry point
# ---------------------------------------------------------------------------
def check_uv_completion(zero_point_weight: float = 1.0,
                        linear_control: bool = False,
                        scheme_b: str = "symanzik",
                        break_universality: float = 1.0,
                        n_bz: int = 90,
                        nt: int = NT_DEFAULT,
                        nk: int = NK_DEFAULT) -> dict:
    """Every leg.  Returns a payload whose ``checks`` map is {leg -> passed}.

    Control parameters (each reddens a declared, disjoint set of legs):
      ``zero_point_weight``  uniform lambda on the zero-point sum      -> U8
      ``linear_control``     replace Omega_pair by exactly c_lat|k|    -> U5, U6
      ``scheme_b``           set to "wilson" so both schemes coincide  -> U4
      ``break_universality`` rescale the measured log coefficient      -> U3
    """
    import sympy as sp
    legs = {}
    out = {}

    # ---- U1 : the lattice loop is finite, the continuum one is not --------
    m2 = 1.0e-2
    I_lat, tail = I_lattice(m2, scheme="wilson", nt=nt, nk=nk)
    cont = {str(Lam): I_continuum_sphere(m2, Lam ** 2)
            for Lam in (math.pi, 10.0, 1.0e3, 1.0e6)}
    growth = cont["1000000.0"] - cont["1000.0"]
    out["U1"] = {"m2": m2, "I_lattice": I_lat, "tail_bound": tail,
                 "I_continuum_vs_Lambda": cont,
                 "continuum_growth_per_3_decades": growth,
                 "expected_growth": 2.0 * math.log(1e3) * INV16PI2}
    legs["U1-lattice-finite"] = math.isfinite(I_lat) and tail < 1e-9
    legs["U1-continuum-unbounded"] = abs(
        growth / (2.0 * math.log(1e3) * INV16PI2) - 1.0) < 1e-6

    # ---- U2 : the scheme difference is IR-independent ---------------------
    ladder = []
    for m in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        c, b = I_lattice_minus_pv(m * m, scheme="wilson", nt=nt, nk=nk)
        ladder.append({"m": m, "scheme_constant": c, "tail_bound": b})
    drift = abs(ladder[-1]["scheme_constant"] - ladder[-2]["scheme_constant"])
    out["U2"] = {"ladder": ladder, "last_decade_drift": drift}
    legs["U2-ir-independent"] = drift < 1e-9

    # ---- U3 : the log coefficient is universal ----------------------------
    meas_w = break_universality * log_coefficient("wilson", nk=nk)
    meas_s = break_universality * log_coefficient("symanzik", nk=nk)
    # Both closed forms are linear in L = ln(1/m^2); differentiate wrt L.
    Lsym = sp.Symbol("L", real=True)                 # L = ln(1/m^2)
    M = sp.Symbol("M", positive=True)
    epsd = sp.Symbol("epsilon", positive=True)
    gE = sp.Symbol("gamma_E", real=True)
    pv_expr = (sp.log(M ** 2) + Lsym) / (16 * sp.pi ** 2)
    dr_expr = (2 / epsd - gE + sp.log(4 * sp.pi) + Lsym) / (16 * sp.pi ** 2)
    pv_coeff = sp.simplify(sp.diff(pv_expr, Lsym))
    dimreg = sp.simplify(sp.diff(dr_expr, Lsym))
    out["U3"] = {"lattice_wilson": meas_w, "lattice_symanzik": meas_s,
                 "target": INV16PI2,
                 "rel_err_wilson": meas_w / INV16PI2 - 1.0,
                 "rel_err_symanzik": meas_s / INV16PI2 - 1.0,
                 "pauli_villars_closed_form": str(pv_coeff),
                 "dimreg_closed_form": str(dimreg),
                 "closed_forms_agree":
                     bool(sp.simplify(pv_coeff - dimreg) == 0)
                     and bool(sp.simplify(pv_coeff - sp.Rational(1, 16) / sp.pi ** 2) == 0)}
    legs["U3-log-universal-wilson"] = abs(meas_w / INV16PI2 - 1.0) < 1e-5
    legs["U3-log-universal-symanzik"] = abs(meas_s / INV16PI2 - 1.0) < 1e-8
    legs["U3-closed-forms-agree"] = out["U3"]["closed_forms_agree"]

    # ---- U4 : scheme dependence is a constant, computed at m = 0 ----------
    d0 = scheme_constant("wilson", scheme_b, nt=nt, nk=nk)
    # m^2 = 1e-12, not 1e-6: at 1e-6 the e^{-t m^2} factor still suppresses
    # part of the scheme difference over t in [1e2, 1e4] and the two routes
    # separate at 1.9e-8, which is a finite-m residual of the ladder route and
    # not a disagreement about the constant.
    cw, _ = I_lattice_minus_pv(1e-12, scheme="wilson", nt=nt, nk=nk)
    cs, _ = I_lattice_minus_pv(1e-12, scheme=scheme_b, nt=nt, nk=nk)
    out["U4"] = {"scheme_b": scheme_b, "delta_at_m_zero": d0,
                 "delta_from_m_ladder": cw - cs,
                 "agreement": abs(d0 - (cw - cs))}
    legs["U4-two-routes-agree"] = abs(d0 - (cw - cs)) < 1e-9
    legs["U4-scheme-constant-nonzero"] = abs(d0) > 1e-6

    # ---- U5 : the leading irrelevant operator, exact rational -------------
    dirs = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (3, 2, 1),
            (1, 2, 2), (5, 3, 1), (7, 4, 2), (9, 5, 4)]
    rows, worst_mp, worst_engine = [], 0.0, 0.0
    for nh in dirs:
        pred = dispersion_excess_closed_form(nh)
        pred_mp = closed_form_mp(nh)
        hi = 0.0 if linear_control else dispersion_excess_mp(nh)
        got = dispersion_excess(nh, 1e-2, linear_control=linear_control)
        worst_mp = max(worst_mp, abs(float(hi - pred_mp)))
        worst_engine = max(worst_engine, abs(got - pred))
        rows.append({"dir": list(nh), "closed_form": pred,
                     "mpmath_60dps": float(hi), "engine_float64": got})
    # No dimension-5 operator: the excess must scale as |k|^2, not |k|^1.
    # Measure the EXPONENT rather than asserting a small number -- a small
    # number at one |k| is consistent with a small dim-5 coefficient, whereas
    # an exponent of 2 excludes the operator outright.
    if linear_control:
        p_exp = float("nan")
    else:
        from casim.engine.gauge.photon import pair_dispersion
        n111 = _unit((1, 1, 1))
        rel = []
        for km in (1e-1, 1e-2):
            k = km * n111
            Om = float(pair_dispersion(float(k[0]), float(k[1]), float(k[2])))
            rel.append(abs((Om - float(c_lat) * km) / (float(c_lat) * km)))
        p_exp = math.log(rel[0] / rel[1]) / math.log(10.0)
    out["U5"] = {
        "closed_form": "-(1 - sum n_i^4)/144 - (nx ny nz)^2/24",
        "rows": rows,
        "worst_abs_err_mpmath": worst_mp,
        "worst_abs_err_engine_float64": worst_engine,
        "bound_exact": str(Fraction(-1, 162)),
        "at_111": dispersion_excess_closed_form((1, 1, 1)),
        "at_100": dispersion_excess_closed_form((1, 0, 0)),
        "scaling_exponent": p_exp,
        "engine_float64_note": "arccos conditioning, not physics -- see "
                               "dispersion_excess_mp docstring",
    }
    legs["U5-closed-form-exact"] = worst_mp < 1e-18
    legs["U5-engine-faithful"] = worst_engine < 5e-7
    legs["U5-no-dim5"] = abs(p_exp - 2.0) < 1e-4
    legs["U5-bound-at-111"] = abs(
        dispersion_excess_closed_form((1, 1, 1)) + 1.0 / 162.0) < 1e-15
    legs["U5-zero-along-100"] = abs(
        dispersion_excess_closed_form((1, 0, 0))) < 1e-15

    # ---- U6 : decoupling at the measured scales ---------------------------
    Lam = lambda_uv_GeV()
    scales = {"m_e": float(m_e_GeV), "M_Z": 91.1876,
              "LHC_13TeV": 1.3e4, "LHAASO_1.4PeV": 1.4e6}
    dec = {}
    for nm, E in scales.items():
        kl = E / Lam
        dec[nm] = {"E_GeV": E, "k_lattice": kl, "max_frac_deviation": kl ** 2 / 162.0}
    out["U6"] = {"Lambda_UV_GeV": Lam, "scales": dec}
    legs["U6-decoupled-at-LHC"] = dec["LHC_13TeV"]["max_frac_deviation"] < 1e-28

    # ---- U7 : the perturbative domain -------------------------------------
    me, alpha = float(m_e_GeV), 1.0 / 137.035999177
    log10_mu_L = math.log10(me) + (3.0 * math.pi / (2.0 * alpha)) / math.log(10.0)
    inv_alpha_uv = 1.0 / alpha - (2.0 / (3.0 * math.pi)) * math.log(Lam / me)
    out["U7"] = {"log10_Landau_GeV": log10_mu_L,
                 "log10_Lambda_UV_GeV": math.log10(Lam),
                 "gap_decades": log10_mu_L - math.log10(Lam),
                 "alpha_at_Lambda_UV": 1.0 / inv_alpha_uv}
    legs["U7-landau-outside-domain"] = log10_mu_L - math.log10(Lam) > 250.0
    legs["U7-perturbative-throughout"] = 1.0 / inv_alpha_uv < 0.1

    # ---- U8 : the two-sector over-determination ---------------------------
    ts = two_sector_solve(zero_point_weight=zero_point_weight, n=n_bz)
    out["U8"] = ts
    legs["U8-reproduces-F164"] = abs(ts["log10_overshoot"] - 120.76) < 0.02
    legs["U8-uniform-channel-excluded"] = ts["a_star_m"] > 1e20
    legs["U8-selectivity-required"] = ts["log10_required_selectivity"] > 110.0

    # ---- U9 : the ledger --------------------------------------------------
    D, dV, dL = superficial_degree()
    unabsorbable = [r for r in UV_LEDGER if r[2] >= 0 and not r[3]
                    and "FORBIDDEN" not in r[4]]
    out["U9"] = {
        "D": str(D), "dD_dV": str(dV), "dD_dL": str(dL),
        "ledger": [{"operator": o, "mass_dim": d, "D": dd,
                    "free_parameter": fp, "disposition": disp}
                   for o, d, dd, fp, disp in UV_LEDGER],
        "n_unabsorbable": len(unabsorbable),
        "unabsorbable": [r[0] for r in unabsorbable],
    }
    legs["U9-D-order-independent"] = (dV == 0 and dL == 0)
    legs["U9-exactly-two-unabsorbable"] = len(unabsorbable) == 2

    # key is `checks`, not `legs`: casim.tests.runner.leg_map reads exactly
    # {"checks": {...}} and a control declaring legs it cannot find is INVALID.
    out["checks"] = legs
    out["n_pass"] = sum(1 for v in legs.values() if v)
    out["n_total"] = len(legs)
    out["verdict"] = "PASS" if all(legs.values()) else "FAIL"
    # `all_pass` is the runner's verdict key (casim.tests.runner._overall).  It
    # must be a RETURNED bool rather than a raised AssertionError: under a
    # declared control the run is SUPPOSED to go red, and the control checker
    # needs the payload -- with the reddened legs in it -- to judge WHICH legs
    # went red.  An entry that raises hands back `payload=None` and every
    # control is scored INVALID for naming legs that "do not exist".
    out["all_pass"] = all(legs.values())
    out["params"] = {"zero_point_weight": zero_point_weight,
                     "linear_control": linear_control, "scheme_b": scheme_b,
                     "break_universality": break_universality,
                     "n_bz": n_bz, "nt": nt, "nk": nk}
    return out


def run(**kw) -> dict:
    """Registry entry point.  Returns the payload; `all_pass` carries the verdict.

    Deliberately does not raise.  See the note on `all_pass` above: the D9/H2
    control checker reads the leg map out of the RETURNED payload, so an entry
    that raises makes every declared control unjudgeable.
    """
    return check_uv_completion(**kw)


if __name__ == "__main__":
    r = run()
    assert r["all_pass"], [k for k, v in r["checks"].items() if not v]
    path = _results_path("F319_uv_completion.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2, sort_keys=True, default=str)
    print(f"{r['verdict']} {r['n_pass']}/{r['n_total']} -> {path}")
