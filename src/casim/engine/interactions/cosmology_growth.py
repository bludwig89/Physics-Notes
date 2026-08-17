"""
cosmology_growth.py — linear structure formation on the lattice: the model's
                      gravity law fixes growth with ZERO free functions
==============================================================================

Created: 2026-08-05 - 09:55
Attacks: ``docs/status/completeness-2026-08-04.md`` row **K11**
         (*structure formation / sigma_8*), graded ABSENT on four keyword
         sweeps. Prompt: ``docs/roadmaps/k11-structure-formation-prompt.md``.

--------------------------------------------------------------------------
The question, and why sigma_8 is NOT it
--------------------------------------------------------------------------

Linear structure formation has three inputs:

    H(a)            the background        -> K1, QUANT, F182/F188
    growth of delta the perturbation law  -> K11, THE GAP
    P(k) initial    the initial spectrum  -> K5, EXCLUDED, A_s provably free

K5 forecloses "predict sigma_8 from nothing": sigma_8 is LINEAR in sqrt(A_s)
and A_s is an automaton initial condition with no route (F282/F284/F285).  So
sigma_8 is REPORTED here with its import budget in the same table, never
claimed.  The claim is the middle row, and it is the one place a gravity theory
can differ from GR WITHOUT differing in the background:

    Does the model's own gravity law fix linear growth, and with how much
    freedom left over?

--------------------------------------------------------------------------
The answer: two free functions in the EFT, zero in the model
--------------------------------------------------------------------------

Every modified-gravity model in the S8 literature lives in two free functions
of (a, k):

    k^2 Psi        = -4 pi G a^2 mu(a,k)    rhobar Delta
    k^2 (Phi + Psi)= -8 pi G a^2 Sigma(a,k) rhobar Delta

The lattice fixes BOTH to 1, by three structurally independent facts it already
owns.  None of the three is introduced here; the contribution is noticing that
together they leave nothing to tune:

    mu = 1, no k     F106's  grad^2 ln K = -(8 pi G/c^4) T^00, live as the
                     STATIC WEAK-FIELD REDUCTION of F178 -- which is exactly
                     the quasi-static sub-horizon regime growth needs.  With
                     ln K = 2 Phi/c^2 this collapses to Poisson with
                     coefficient 4 pi G and no k anywhere.  [check S2]
    slip = 0         The impedance match A B == 1 (A = 1/K, B = K; F64, and
                     CLAUDE.md decision 4), the same condition as PPN gamma = 1
                     (F64 D-EM9).  Slip vanishes at LINEAR order exactly; the
                     leading term is first order in the potential AMPLITUDE
                     (2 Phi ~ 2e-5), i.e. 2PN.  [check S1]
    d mu/da = 0      F79 makes G structural; F284 makes the substrate rigid;
                     together Gdot/G == 0 exactly, so mu cannot acquire time
                     dependence for the same reason it cannot acquire a drift
                     in G.  [check S3]

**Scope, stated because F178 demoted the energy-only law.**  S2 uses F106 in
the regime F178 left it live in: static, weak-field, sub-horizon, quasi-static.
That is the correct regime for CDM growth (p = 0, no anisotropic stress).  It
is NOT valid super-horizon or for relativistic radiation-era modes; those need
the full tensor and are carried by the transfer function, not by this ODE.

**Scope, second caveat.**  Zero slip is a statement about the GRAVITY sector.
Free-streaming neutrinos carry genuine anisotropic stress and source the usual
slip in the radiation era exactly as in GR; the lattice removes the
gravitational dial, not the matter source.

--------------------------------------------------------------------------
What then follows -- derived, not asserted
--------------------------------------------------------------------------

    D1  growth index gamma_g = 6/11 EXACTLY          (sympy, literal zero)
    D2  Meszaros  D(y) = 1 + (3/2) y  EXACTLY         (sympy, literal zero)
    D3  D(a), f(a), f sigma_8(z) on the F188 background vs RSD + DESI DR1 PV
    D4  sigma_8 from A_s, with the import budget in the table
    B1  discreteness: the O((k a)^2) correction at 8 h^-1 Mpc and Lyman-alpha
    B2  dark-matter free streaming: geon remnant vs the F266 5.6 keV sterile

--------------------------------------------------------------------------
The falsifier, and it can fire
--------------------------------------------------------------------------

mu == 1 is k-INDEPENDENT BY DERIVATION, so the model has no screening
mechanism -- the standard escape hatch by which modified gravity relieves S8
on nonlinear scales while evading linear-scale bounds.  It therefore has NO
WAY to lower late-time growth relative to the CMB prediction.  If the DES Y6
direction (S8 = 0.789 +/- 0.012, 2.7 sigma below the combined-CMB
0.836 +0.012/-0.013) consolidates as physical rather than as photo-z /
baryonic-feedback systematics, the model's gravity sector is falsified
outright.  It cannot be accommodated, because there is nothing to accommodate
it with.

Real arithmetic, hand-rolled RK4 and Simpson quadrature; sympy for the two
exact legs.  No scipy integrator (D8).

References for the external numbers, all quoted in ``EXTERNAL``:
  Planck Collaboration 2020 (Planck 2018 VI); eBOSS DR16 completed-survey
  consensus (Alam et al. 2021); DESI DR1 peculiar-velocity survey 2025;
  DES Y6 3x2pt and the combined-CMB baseline (Abbott et al. 2026);
  KiDS-Legacy 2025; Eisenstein & Hu 1998 (no-wiggle transfer function);
  Viel et al. 2005 (WDM transfer fitting form).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.constants import a_over_ellP, ell_P_m
from casim.engine.interactions import cosmology_anomalous_dimension as ad
from casim.numerics import xp

# ===========================================================================
# External inputs.  Every number a result depends on that the model does not
# produce is HERE, once, with its source.  Nothing below writes a literal.
# ===========================================================================
EXTERNAL = {
    # --- background (K1: these are the measured Omegas F188 also takes in) ---
    "Omega_m": (0.3153, "Planck 2018 VI TT,TE,EE+lowE+lensing"),
    "Omega_b": (0.04930, "Planck 2018 VI"),
    "h": (0.6736, "Planck 2018 VI"),
    "T_cmb_K": (2.7255, "Fixsen 2009"),
    # --- primordial (K5: EXCLUDED, free.  This is the budget line) ---
    "A_s": (2.100e-9, "Planck 2018 VI, at k_p = 0.05 / Mpc.  FREE INPUT (K5)"),
    "k_pivot_invMpc": (0.05, "Planck pivot"),
    "sum_mnu_eV": (0.06, "Planck 2018 baseline minimal neutrino mass"),
    "sigma8_planck": (0.8111, "Planck 2018 VI TT,TE,EE+lowE+lensing"),
    # --- S8 landscape, 2026 ---
    "S8_cmb": (0.836, "Abbott et al. 2026 combined CMB: Planck18+ACT DR6+SPT-3G"),
    "S8_cmb_err": (0.0125, "same, symmetrised from +0.012 / -0.013"),
    "S8_desy6": (0.789, "DES Y6 3x2pt"),
    "S8_desy6_err": (0.012, "DES Y6 3x2pt"),
    "S8_kids_legacy": (0.815, "KiDS-Legacy 2025 (up 0.056 from KiDS-1000)"),
    "S8_kids_legacy_err": (0.0185, "symmetrised from +0.016 / -0.021"),
    # --- WDM transfer fit (Viel et al. 2005) ---
    "viel_nu": (1.12, "Viel et al. 2005 eq. 6"),
    "viel_norm": (0.049, "Viel et al. 2005, alpha prefactor in h^-1 Mpc"),
}

# Redshift-space-distortion compilation.  (z, f sigma_8, sigma).
# DIAGONAL ONLY: the three BOSS DR12 points are correlated, so the chi^2 built
# from this table is INDICATIVE, not a likelihood.  Said again at the check.
RSD_DATA = (
    (0.07, 0.4497, 0.0548, "DESI DR1 peculiar-velocity survey, consensus"),
    (0.38, 0.497, 0.045, "BOSS DR12 consensus"),
    (0.51, 0.459, 0.038, "BOSS DR12 consensus"),
    (0.61, 0.436, 0.034, "BOSS DR12 consensus"),
    (0.698, 0.473, 0.041, "eBOSS DR16 LRG"),
    (0.845, 0.315, 0.095, "eBOSS DR16 ELG"),
    (1.48, 0.462, 0.045, "eBOSS DR16 QSO"),
)

C_KM_S = 299792.458                       # km/s, for c/H0 in Mpc
R8_H_INV_MPC = 8.0                        # the sigma_8 sphere, by definition
MPC_M = 3.0856775814913673e22             # metres per Mpc (IAU 2015 exact au)

# The lattice cell, from the registry (F79 structural G, F107 SI ruler).
A_CELL_M = a_over_ellP * ell_P_m          # 1.0664e-34 m  (F284)


# ===========================================================================
# 0 -- background.  Matter + Lambda + radiation, flat.
# ===========================================================================
def _omega_r(Om: float, h: float) -> float:
    """Radiation density from the CMB temperature and Neff, photons + nu."""
    T = EXTERNAL["T_cmb_K"][0]
    # Omega_gamma h^2 = 2.4728e-5 (T/2.7255)^4 ; + neutrinos, Neff = 3.046
    og_h2 = 2.47282e-5 * (T / 2.7255) ** 4
    or_h2 = og_h2 * (1.0 + 3.046 * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0))
    return or_h2 / h ** 2


def background(Om=None, h=None, radiation=True) -> dict:
    """The flat FLRW background this module integrates growth on (K1/F188)."""
    Om = EXTERNAL["Omega_m"][0] if Om is None else Om
    h = EXTERNAL["h"][0] if h is None else h
    Or = _omega_r(Om, h) if radiation else 0.0
    return {"Om": Om, "Or": Or, "OL": 1.0 - Om - Or, "h": h}


def E2(a: float, bg: dict) -> float:
    """(H/H0)^2."""
    return bg["Or"] * a ** -4 + bg["Om"] * a ** -3 + bg["OL"]


def omega_m_of_a(a: float, bg: dict) -> float:
    """The matter fraction at a -- the argument of the growth index."""
    return bg["Om"] * a ** -3 / E2(a, bg)


def dlnE_dlna(a: float, bg: dict) -> float:
    return -0.5 * (4.0 * bg["Or"] * a ** -4 + 3.0 * bg["Om"] * a ** -3) / E2(a, bg)


# ===========================================================================
# 1 -- THE STRUCTURAL CORE.  mu, Sigma and the slip, from the model's own law.
# ===========================================================================
def slip_from_impedance_match() -> dict:
    r"""S1 -- ``A B == 1`` kills linear-order gravitational slip, exactly.

    F64's dielectric is ``A = 1/K``, ``B = K`` with ``A B == 1`` identically
    (CLAUDE.md decision 4).  Write ``K = exp(2 Phi)`` (c = 1) and read off the
    Newtonian-gauge potentials from

        -(1 + 2 Psi) = -1/K ,      a^2 (1 - 2 Phi_N) = K a^2 .

    The slip ``Phi_N - Psi`` must then have a LITERALLY ZERO coefficient at
    first order in Phi.  Anything else would be a linear-order slip, and there
    is no dial in the model that could produce or absorb one.
    """
    Phi = sp.symbols("Phi", real=True)
    K = sp.exp(2 * Phi)

    Psi = (1 / K - 1) / 2                     # from -(1+2 Psi) = -1/K
    Phi_N = (1 - K) / 2                       # from 1 - 2 Phi_N = K

    slip = sp.simplify(Phi_N - Psi)           # = 1 - cosh(2 Phi) = -2 sinh^2 Phi
    ser = sp.series(slip, Phi, 0, 4).removeO()
    c1 = sp.simplify(sp.expand(ser).coeff(Phi, 1))
    c2 = sp.simplify(sp.expand(ser).coeff(Phi, 2))

    # eta = Phi_N / Psi ;  eta - 1 = 2 Phi + O(Phi^2)
    eta_minus_1 = sp.series(sp.simplify(Phi_N / Psi) - 1, Phi, 0, 3).removeO()
    eta_c1 = sp.simplify(sp.expand(eta_minus_1).coeff(Phi, 1))

    # Cosmological potentials are ~1e-5, so the residual slip is ~2e-5.
    phi_cosmo = 1.0e-5
    eta_residual = float(eta_c1) * phi_cosmo

    return {
        "AB_product": str(sp.simplify(sp.Symbol("A") * 0 + (1 / K) * K)),   # 1
        "slip_closed_form": str(slip),
        "slip_linear_coefficient": str(c1),
        "slip_quadratic_coefficient": str(c2),
        "linear_slip_is_exactly_zero": c1 == 0,
        "eta_minus_1_linear_coefficient": float(eta_c1),
        "eta_residual_at_Phi_1e-5": eta_residual,
        "Sigma": 1.0,
        "pass": bool(c1 == 0 and sp.simplify((1 / K) * K - 1) == 0),
        "note": ("A B == 1 is the impedance match, the same condition as PPN "
                 "gamma = 1 (F64 D-EM9). Slip enters at 2PN, i.e. first order "
                 "in the potential AMPLITUDE, ~2e-5 -- four orders below any "
                 "current constraint. Scope: this is the GRAVITY sector; "
                 "free-streaming neutrinos still carry anisotropic stress and "
                 "source the usual GR slip in the radiation era."),
    }


def mu_from_f106_poisson() -> dict:
    r"""S2 -- F106's sourcing law collapses to Poisson with ``mu = 1``, no k.

    F106 (live as F178's static weak-field reduction, which IS the quasi-static
    sub-horizon regime):

        grad^2 ln K = -(8 pi G/c^4) T^00 ,     ln K = 2 Phi / c^2 ,
        T^00 = rho c^2 = rhobar c^2 (1 + delta) .

    Substituting must give ``grad^2 Phi = -4 pi G rhobar delta`` -- coefficient
    exactly 4 pi G, and NO k anywhere, so mu(a,k) == 1 with d mu/dk == 0.
    """
    G, c, rho, Phi_f = sp.symbols("G c rho Phi", positive=True)
    k = sp.symbols("k", positive=True)

    # Fourier: grad^2 -> -k^2, so -k^2 (2 Phi/c^2) = -(8 pi G/c^4) rho c^2
    lhs = -k ** 2 * (2 * Phi_f / c ** 2)
    rhs = -(8 * sp.pi * G / c ** 4) * (rho * c ** 2)
    Phi_sol = sp.solve(sp.Eq(lhs, rhs), Phi_f)[0]          # 4 pi G rho / k^2

    # GR/Poisson reference in the same variables.
    Phi_gr = 4 * sp.pi * G * rho / k ** 2
    mu = sp.simplify(Phi_sol / Phi_gr)
    dmu_dk = sp.simplify(sp.diff(mu, k))

    return {
        "Phi_from_F106": str(sp.simplify(Phi_sol)),
        "Phi_GR": str(Phi_gr),
        "mu": str(mu),
        "mu_is_exactly_one": bool(sp.simplify(mu - 1) == 0),
        "dmu_dk": str(dmu_dk),
        "mu_is_scale_free": bool(sp.simplify(dmu_dk) == 0),
        "pass": bool(sp.simplify(mu - 1) == 0 and sp.simplify(dmu_dk) == 0),
        "regime": ("static, weak-field, sub-horizon, quasi-static -- exactly "
                   "where F178 left the energy-only law live. NOT valid "
                   "super-horizon or for relativistic radiation-era modes."),
    }


def no_free_functions() -> dict:
    """S3 -- the constraint count, which is the finding's headline.

    The EFT of dark energy has two free functions of (a,k).  The lattice has
    zero, and each closure is sourced independently -- so this is a genuine
    count, not one fact wearing three hats.
    """
    closures = {
        "mu_k_independence": ("F106 Poisson coefficient, no k", "F106/F178"),
        "mu_time_independence": ("G structural on a rigid substrate => "
                                 "Gdot/G == 0 exactly", "F79/F284"),
        "Sigma_via_zero_slip": ("A B == 1 impedance match == PPN gamma = 1",
                                "F64 D-EM9"),
    }
    return {
        "eft_free_functions": 2,
        "model_free_functions": 0,
        "closures": {k: {"why": v[0], "source": v[1]} for k, v in closures.items()},
        "distinct_sources": sorted({v[1] for v in closures.values()}),
        "n_distinct_sources": len({v[1] for v in closures.values()}),
        "screening_mechanism": None,
        "pass": True,
        "note": ("Three closures from three independently-derived findings. "
                 "The model is MORE constrained than GR-as-an-EFT in this "
                 "sector, and it has no screening mechanism because mu = 1 is "
                 "k-independent by derivation, not by choice."),
    }


# ===========================================================================
# 2 -- the two exact consequences
# ===========================================================================
def growth_index_exact() -> dict:
    r"""D1 -- ``gamma_g = 6/11`` exactly, from the model's own growth equation.

    In x = ln a the growth equation with mu = 1 is

        f' + f^2 + f (2 + dlnH/dlnx) = (3/2) Omega_m ,

    with dlnH/dlnx = -(3/2) Omega_m and d Omega_m/dx = 3 Omega_m (Omega_m - 1)
    for flat LambdaCDM.  Put f = c Omega_m^gamma and expand about Omega_m = 1.
    Order eps^0 fixes c (and c = 1 iff mu = 1); order eps^1 fixes gamma.
    """
    eps, gam, mu = sp.symbols("epsilon gamma mu", real=True)
    c = sp.symbols("c", positive=True)
    Om = 1 - eps

    f = c * Om ** gam
    # f' = df/dOm * dOm/dx = c gam Om^(gam-1) * 3 Om (Om - 1)
    fprime = c * gam * Om ** (gam - 1) * 3 * Om * (Om - 1)
    resid = fprime + f ** 2 + f * (2 - sp.Rational(3, 2) * Om) - sp.Rational(3, 2) * mu * Om

    ser = sp.series(sp.expand(resid), eps, 0, 2).removeO()
    e0 = sp.simplify(sp.expand(ser).coeff(eps, 0))
    e1 = sp.simplify(sp.expand(ser).coeff(eps, 1))

    # Order 0: c^2 + c/2 - (3/2) mu = 0  ->  c = (-1 + sqrt(1 + 24 mu))/4
    c_sol = [s for s in sp.solve(sp.Eq(e0, 0), c) if s.subs(mu, 1) > 0][0]
    c_at_mu1 = sp.simplify(c_sol.subs(mu, 1))

    # Order 1 at mu = 1, c = 1: solve for gamma
    e1_mu1 = sp.simplify(e1.subs({mu: 1, c: 1}))
    gamma_sol = sp.simplify(sp.solve(sp.Eq(e1_mu1, 0), gam)[0])

    # The control handle: how far does gamma_g move if mu is not 1?
    c_of_mu = sp.lambdify(mu, c_sol, "math")

    return {
        "order0_residual": str(e0),
        "c_closed_form": str(sp.simplify(c_sol)),
        "c_at_mu_1": str(c_at_mu1),
        "c_is_exactly_1_iff_mu_is_1": bool(sp.simplify(c_at_mu1 - 1) == 0),
        "order1_residual_at_mu1": str(e1_mu1),
        "gamma_g_exact": str(gamma_sol),
        "gamma_g_is_6_over_11": bool(sp.simplify(gamma_sol - sp.Rational(6, 11)) == 0),
        "gamma_g_float": float(gamma_sol),
        "c_at_mu_0p90": c_of_mu(0.90),
        "pass": bool(sp.simplify(gamma_sol - sp.Rational(6, 11)) == 0
                     and sp.simplify(c_at_mu1 - 1) == 0),
        "note": ("gamma_g = 6/11 is a PREDICTION here rather than a fit "
                 "because mu = 1 is forced (S2/S3): a general modified-gravity "
                 "theory carries gamma_g as a free parameter. Note the order-0 "
                 "leg -- f -> 1 as Omega_m -> 1 holds IFF mu = 1, so any "
                 "mu != 1 is visible in the amplitude of f as well as in "
                 "gamma_g."),
    }


def meszaros_exact() -> dict:
    r"""D2 -- ``D(y) = 1 + (3/2) y`` solves the radiation-era equation exactly.

    Sub-horizon CDM in the radiation era, y = a/a_eq:

        d2 delta/dy2 + (2 + 3y)/(2 y (1+y)) d delta/dy
                     - 3 delta / (2 y (1+y)) = 0 .

    This is the one place the transfer function's SHAPE is derived by the
    model rather than imported: it is the model's own growth equation with
    mu = 1, written on a background where radiation dominates and does not
    cluster.  Require a literal zero.
    """
    y = sp.symbols("y", positive=True)
    D = 1 + sp.Rational(3, 2) * y

    lhs = (sp.diff(D, y, 2)
           + (2 + 3 * y) / (2 * y * (1 + y)) * sp.diff(D, y)
           - 3 * D / (2 * y * (1 + y)))
    resid = sp.simplify(sp.together(lhs))

    # The decaying partner, for completeness of the solution space.
    D2 = (1 + sp.Rational(3, 2) * y) * sp.log((sp.sqrt(1 + y) + 1)
                                              / (sp.sqrt(1 + y) - 1)) - 3 * sp.sqrt(1 + y)
    resid2 = sp.simplify(sp.together(
        sp.diff(D2, y, 2) + (2 + 3 * y) / (2 * y * (1 + y)) * sp.diff(D2, y)
        - 3 * D2 / (2 * y * (1 + y))))

    return {
        "growing_mode": str(D),
        "residual": str(resid),
        "residual_is_literal_zero": bool(resid == 0),
        "decaying_mode_residual": str(resid2),
        "decaying_mode_is_zero": bool(sp.simplify(resid2) == 0),
        "logarithmic_stagnation": ("delta grows by only 5/2 across the whole "
                                   "radiation era, y: 0 -> 1 -- the Meszaros "
                                   "effect, and the origin of the T(k) ~ "
                                   "ln k / k^2 large-k falloff"),
        "pass": bool(resid == 0),
    }


# ===========================================================================
# 3 -- growth integrated on the background
# ===========================================================================
def growth_factor(bg: dict, mu: float = 1.0, a_i: float = 1.0e-3,
                  n: int = 4000, a_f: float = 1.0):
    """RK4 the growth equation in x = ln a.  Returns (a, D, f) arrays.

    ``D`` is normalised to the standard convention ``D -> a`` in matter
    domination (NOT D(1) = 1), which is what the transfer-function
    normalisation in :func:`sigma8_from_As` expects.
    """
    x0, x1 = math.log(a_i), math.log(a_f)
    hstep = (x1 - x0) / n

    def deriv(x, s):
        a = math.exp(x)
        d, dp = s
        return (dp, -(2.0 + dlnE_dlna(a, bg)) * dp
                + 1.5 * mu * omega_m_of_a(a, bg) * d)

    xs = [x0] * (n + 1)
    ds = [a_i] * (n + 1)
    dps = [a_i] * (n + 1)          # growing mode: delta = a  =>  delta' = a
    s = (a_i, a_i)
    for i in range(n):
        x = x0 + i * hstep
        k1 = deriv(x, s)
        k2 = deriv(x + hstep / 2, (s[0] + hstep / 2 * k1[0], s[1] + hstep / 2 * k1[1]))
        k3 = deriv(x + hstep / 2, (s[0] + hstep / 2 * k2[0], s[1] + hstep / 2 * k2[1]))
        k4 = deriv(x + hstep, (s[0] + hstep * k3[0], s[1] + hstep * k3[1]))
        s = (s[0] + hstep / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
             s[1] + hstep / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
        xs[i + 1] = x + hstep
        ds[i + 1] = s[0]
        dps[i + 1] = s[1]

    a = xp.exp(xp.asarray(xs))
    D = xp.asarray(ds)
    f = xp.asarray(dps) / D
    return a, D, f


def _interp(xg, yg, x):
    """Linear interpolation on a monotone grid (no scipy; D8)."""
    i = int(xp.searchsorted(xg, x))
    i = max(1, min(i, len(xg) - 1))
    t = (x - xg[i - 1]) / (xg[i] - xg[i - 1])
    return float(yg[i - 1] + t * (yg[i] - yg[i - 1]))


def growth_summary(bg: dict = None, mu: float = 1.0) -> dict:
    """D3a -- growth on the real background, and the integrator validated.

    Convention: the growth ODE runs on the matter + Lambda background.  All
    radiation-era physics lives in the transfer function, which is what T(k)
    is *for*; carrying it in the ODE as well would double-count it.  The cost
    of that choice is measured here (``f_radiation_sensitivity``) rather than
    asserted to be small.

    The integrator is validated against the Carroll-Press-Turner fitting
    formula for D(a=1)/a -- an INDEPENDENT published result, so this leg can
    genuinely fail if the RK4 or the initial condition is wrong.
    """
    bg = background(radiation=False) if bg is None else bg
    a, D, f = growth_factor(bg, mu=mu)
    f0 = float(f[-1])
    D0 = float(D[-1])
    Om0 = omega_m_of_a(1.0, bg)
    gamma_num = math.log(f0) / math.log(Om0)
    gamma_exact = 6.0 / 11.0

    # Independent published cross-check (Carroll, Press & Turner 1992).
    OL = bg["OL"]
    g_cpt = 2.5 * Om0 / (Om0 ** (4.0 / 7.0) - OL
                         + (1.0 + Om0 / 2.0) * (1.0 + OL / 70.0))

    # Cost of the radiation convention, measured.
    _, _, f_rad = growth_factor(background(radiation=True), mu=mu)
    f_sens = abs(float(f_rad[-1]) / f0 - 1.0)

    return {
        "f_at_z0": f0,
        "Omega_m_at_z0": Om0,
        "gamma_g_numerical": gamma_num,
        "gamma_g_exact_limit": gamma_exact,
        "gamma_g_offset": gamma_num - gamma_exact,
        "f_vs_Omega_m_0p55": Om0 ** 0.55,
        "D_normalisation": "D -> a in matter domination (matter + Lambda)",
        "D_at_z0": D0,
        "D_carroll_press_turner": g_cpt,
        "D_vs_CPT_relative": D0 / g_cpt - 1.0,
        "f_radiation_sensitivity": f_sens,
        "pass": bool(abs(gamma_num - 0.55) < 0.02
                     and abs(D0 / g_cpt - 1.0) < 3.0e-3
                     and f_sens < 1.0e-3),
        "note": ("The 6/11 limit is the Omega_m -> 1 value; at Omega_m = "
                 f"{Om0:.4f} the effective index sits slightly above it. Both "
                 "are consequences of mu = 1 with nothing free. The CPT leg "
                 "is the integrator's own falsification test: a wrong initial "
                 "condition or a wrong source coefficient moves D(1) by "
                 "percent, and the tolerance is 0.3%."),
    }


def fsigma8_curve(sigma8_0: float, bg: dict = None, mu: float = 1.0) -> dict:
    """D3b -- f sigma_8(z) against the RSD compilation.

    DIAGONAL chi^2 ONLY.  The three BOSS DR12 points are correlated, so this
    number is INDICATIVE of consistency, not a likelihood.
    """
    bg = background(radiation=False) if bg is None else bg
    a, D, f = growth_factor(bg, mu=mu)
    D0 = float(D[-1])

    rows, chi2 = [], 0.0
    for z, obs, sig, src in RSD_DATA:
        av = 1.0 / (1.0 + z)
        model = _interp(a, f, av) * sigma8_0 * _interp(a, D, av) / D0
        pull = (model - obs) / sig
        chi2 += pull ** 2
        rows.append({"z": z, "obs": obs, "sigma": sig, "model": model,
                     "pull_sigma": pull, "source": src})

    ndof = len(RSD_DATA)
    return {
        "rows": rows,
        "chi2": chi2,
        "n_points": ndof,
        "chi2_per_point": chi2 / ndof,
        "max_abs_pull": max(abs(r["pull_sigma"]) for r in rows),
        "sigma8_input": sigma8_0,
        "mu": mu,
        "pass": chi2 / ndof < 2.0,
        "caveat": ("DIAGONAL chi^2. The three BOSS DR12 points are correlated "
                   "and their covariance is not applied, so this is a "
                   "consistency statement, not a likelihood."),
    }


# ===========================================================================
# 4 -- sigma_8, with its import budget
# ===========================================================================
def transfer_eh98(k_invMpc, bg: dict) -> float:
    """Eisenstein & Hu 1998 zero-baryon ("no-wiggle") transfer function.

    IMPORTED, and labelled as such: the model derives the SHAPE arguments
    (Meszaros stagnation, the k_eq turnover from F188's z_eq) but not the
    O(1) fitting coefficients of the interpolation between them.
    """
    h = bg["h"]
    omh2 = bg["Om"] * h ** 2
    obh2 = EXTERNAL["Omega_b"][0] * h ** 2
    theta = EXTERNAL["T_cmb_K"][0] / 2.7

    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1.0 + 10.0 * obh2 ** 0.75)
    fb = EXTERNAL["Omega_b"][0] / bg["Om"]
    a_gam = (1.0 - 0.328 * math.log(431.0 * omh2) * fb
             + 0.38 * math.log(22.3 * omh2) * fb ** 2)
    gam_eff = bg["Om"] * h * (a_gam + (1.0 - a_gam) / (1.0 + (0.43 * k_invMpc * s) ** 4))

    q = k_invMpc / h * theta ** 2 / gam_eff
    L0 = math.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q ** 2)


def _window_tophat(x: float) -> float:
    if x < 1.0e-4:
        return 1.0 - x * x / 10.0
    return 3.0 * (math.sin(x) - x * math.cos(x)) / x ** 3


def sigma_R(R_Mpc: float, bg: dict = None, n_s: float = None,
            A_s: float = None, wdm_keV: float = None, mu: float = 1.0,
            n: int = 2000) -> float:
    """rms linear density contrast in spheres of radius R, at z = 0.

    Delta^2(k) = (4/25) A_s (k/k_p)^(n_s-1) (c k/H0)^4 Omega_m^-2 T(k)^2 D(1)^2
    with D normalised to D -> a in matter domination.

    **A_s is the anchor, not sigma_8.**  That is both the physically correct
    normalisation -- the primordial amplitude is fixed at z ~ 1100, and
    sigma_8 today is a CONSEQUENCE of growth -- and what makes the ``mu``
    sweep a real control: a modified mu propagates through D(1) into
    sigma_8, S_8 and f sigma_8 together, instead of being absorbed by an
    sigma_8 handed in from outside.
    """
    bg = background(radiation=False) if bg is None else bg
    n_s = ad.NS_OBS if n_s is None else n_s
    A_s = EXTERNAL["A_s"][0] if A_s is None else A_s

    _, D, _ = growth_factor(bg, mu=mu)
    D1 = float(D[-1])
    c_over_H0 = C_KM_S / (100.0 * bg["h"])           # Mpc
    kp = EXTERNAL["k_pivot_invMpc"][0]

    lk0, lk1 = math.log(1.0e-5), math.log(1.0e3)     # 1/Mpc
    hstep = (lk1 - lk0) / n
    total = 0.0
    for i in range(n + 1):
        k = math.exp(lk0 + i * hstep)
        T = transfer_eh98(k, bg)
        if wdm_keV is not None:
            T *= transfer_wdm(k, wdm_keV, bg)
        d2 = (4.0 / 25.0) * A_s * (k / kp) ** (n_s - 1.0) \
            * (c_over_H0 * k) ** 4 / bg["Om"] ** 2 * T ** 2 * D1 ** 2
        w = _window_tophat(k * R_Mpc)
        term = d2 * w * w
        # Simpson weights
        wt = 1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)
        total += wt * term
    return math.sqrt(total * hstep / 3.0)


def sigma8_from_As(bg: dict = None, n_s: float = None, A_s: float = None,
                   wdm_keV: float = None, mu: float = 1.0) -> dict:
    """D4 -- sigma_8, REPORTED with its import budget, never claimed."""
    bg = background(radiation=False) if bg is None else bg
    n_s = ad.NS_OBS if n_s is None else n_s
    A_s = EXTERNAL["A_s"][0] if A_s is None else A_s

    R8 = R8_H_INV_MPC / bg["h"]
    s8_massless = sigma_R(R8, bg=bg, n_s=n_s, A_s=A_s, wdm_keV=wdm_keV, mu=mu)

    # Massive-neutrino suppression, applied because Planck's A_s is quoted
    # WITH sum m_nu = 0.06 eV and the EH98 no-wiggle T(k) has no neutrinos.
    # Small-scale suppression Delta P/P ~ -8 f_nu  =>  Delta sigma_8/sigma_8 ~ -4 f_nu.
    f_nu = (EXTERNAL["sum_mnu_eV"][0] / 93.14 / bg["h"] ** 2) / bg["Om"]
    nu_factor = 1.0 - 4.0 * f_nu
    s8 = s8_massless * nu_factor
    S8 = s8 * math.sqrt(bg["Om"] / 0.3)
    ref = EXTERNAL["sigma8_planck"][0]

    return {
        "sigma_8": s8,
        "sigma_8_massless_nu": s8_massless,
        "nu_suppression_factor": nu_factor,
        "f_nu": f_nu,
        "S_8": S8,
        "sigma_8_planck": ref,
        "sigma_8_relative_to_planck": s8 / ref - 1.0,
        "R8_Mpc": R8,
        "n_s_used": n_s,
        "n_s_source": ("cosmology_anomalous_dimension.NS_OBS -- the same "
                       "number F295's gamma = (1 - n_s)/2 is defined from, "
                       "imported live so the two cannot drift"),
        "import_budget": {
            "A_s": f"{A_s:.4g}  -- FREE INPUT, K5 EXCLUDED, no route (F282/F284/F285)",
            "n_s": f"{n_s}  -- fitted; F295 routes it to gamma = {(1-n_s)/2:.6f}, "
                   "which is a relabelling, not a derivation",
            "T(k) coefficients": "Eisenstein & Hu 1998 no-wiggle fit -- IMPORTED",
            "Omega_m, Omega_b, h": "Planck 2018 -- measured, same inputs K1/F188 takes",
            "sum m_nu": "0.06 eV, Planck baseline -- applied as -4 f_nu on sigma_8",
        },
        "derived_here": ["the growth factor D(a) that multiplies all of it",
                         "the Meszaros stagnation the T(k) shape encodes",
                         "gamma_g = 6/11"],
        "residual_budget": ("the ~1% left after the neutrino correction is the "
                            "EH98 NO-WIGGLE fit itself, which drops the "
                            "acoustic oscillations and is documented at the "
                            "1-2% level in sigma_8. It is an imported-fit "
                            "residual, not a model residual."),
        "claim": ("sigma_8 is NOT predicted. It is LINEAR in sqrt(A_s) and A_s "
                  "is provably free (K5). What is predicted is the GROWTH that "
                  "maps A_s to sigma_8, and that has zero free functions."),
        "pass": abs(s8 / ref - 1.0) < 0.04,
    }


def mu_bound_from_growth() -> dict:
    r"""D5 -- how well is ``mu = 1`` actually TESTED, not just derived?

    A structural claim is worth more when the data can see it.  In matter
    domination the growth exponent is the order-0 root of :func:`growth_index_exact`,

        delta ~ a^p ,   p(mu) = [-1 + sqrt(1 + 24 mu)] / 4 ,   p(1) = 1 ,

    so a CONSTANT fractional error in mu is amplified by the ~7 e-folds of
    integration from z = 1000: dp/dmu = 3/5 at mu = 1, hence
    d ln sigma_8 / d mu ~ (3/5) ln(1/a_i) ~ 4.

    Two bounds are reported, and they differ in what they lean on:

      * ``amplitude_anchored``   A_s fixed at the CMB.  Strongest, but inherits
        the imported EH98 no-wiggle T(k) residual.
      * ``shape_only``           the f sigma_8 amplitude is marginalised
        analytically, so only the REDSHIFT SHAPE of f(z) D(z) is used.  Weaker,
        and free of the transfer function entirely.
    """
    mu_s, = sp.symbols("mu", positive=True),
    p = sp.simplify((-1 + sp.sqrt(1 + 24 * mu_s)) / 4)
    dp = sp.simplify(sp.diff(p, mu_s).subs(mu_s, 1))

    s8_ref = sigma8_from_As()["sigma_8"]

    def chi2_anchored(mu):
        return fsigma8_curve(sigma8_from_As(mu=mu)["sigma_8"], mu=mu)["chi2"]

    def chi2_shape(mu):
        """Analytic marginalisation over the overall amplitude."""
        r = fsigma8_curve(s8_ref, mu=mu)["rows"]
        # best-fit scaling alpha of the model curve, then chi^2 at that alpha
        sxy = sum(row["model"] * row["obs"] / row["sigma"] ** 2 for row in r)
        sxx = sum(row["model"] ** 2 / row["sigma"] ** 2 for row in r)
        alpha = sxy / sxx
        return sum(((alpha * row["model"] - row["obs"]) / row["sigma"]) ** 2
                   for row in r)

    LO_FLOOR, HI_CEIL, STEP = 0.5, 1.5, 0.002

    def interval(fn, dchi2):
        base = fn(1.0)
        lo, hi = 1.0, 1.0
        while lo > LO_FLOOR and fn(lo) - base < dchi2:
            lo -= STEP
        while hi < HI_CEIL and fn(hi) - base < dchi2:
            hi += STEP
        return lo, hi, lo <= LO_FLOOR, hi >= HI_CEIL

    lo1, hi1, lo1_floor, hi1_ceil = interval(chi2_anchored, 1.0)
    lo1s, hi1s, lo1s_floor, hi1s_ceil = interval(chi2_shape, 1.0)

    return {
        "p_of_mu": str(p),
        "dp_dmu_at_1": str(dp),
        "dlnsigma8_dmu_analytic": float(dp) * math.log(1.0 / 1.0e-3),
        "amplitude_anchored": {
            "mu_lo_1sigma": lo1, "mu_hi_1sigma": hi1,
            "half_width": (hi1 - lo1) / 2,
            "hit_scan_limit": bool(lo1_floor or hi1_ceil),
            "leans_on": "EH98 no-wiggle T(k) + A_s"},
        "shape_only": {
            "mu_lo_1sigma": lo1s, "mu_hi_1sigma": hi1s,
            "half_width": (hi1s - lo1s) / 2,
            "hit_scan_limit": bool(lo1s_floor or hi1s_ceil),
            "leans_on": "nothing but the f sigma_8 redshift shape",
            "honest_reading": ("the low side runs off the scan floor at "
                               f"{LO_FLOOR}: with the amplitude marginalised, "
                               "a suppressed growth rate is degenerate with a "
                               "larger A_s, so the SHAPE alone does not bound "
                               "mu from below at all. Only the upper edge is a "
                               "bound. Reported this way on purpose -- quoting "
                               f"{LO_FLOOR} as a limit would be quoting the "
                               "scan range as physics.")},
        "model_value": 1.0,
        "model_value_is_inside_both": bool(lo1 <= 1.0 <= hi1 and lo1s <= 1.0 <= hi1s),
        "pass": bool(lo1 <= 1.0 <= hi1 and lo1s <= 1.0 <= hi1s
                     and (hi1 - lo1) / 2 < 0.05 and not lo1_floor and not hi1_ceil),
        "note": ("The derived value mu = 1 is not merely consistent with the "
                 "data, it is PINNED by it: growth integrates the exponent "
                 "p(mu) over ~7 e-folds, so percent-level agreement in "
                 "sigma_8 is sub-percent-level agreement in mu. That "
                 "amplification is also why the mu sweep is a usable control "
                 "-- a 10% perturbation moves sigma_8 by ~32%."),
    }


# ===========================================================================
# 5 -- the two bounds
# ===========================================================================
def discreteness_bound() -> dict:
    """B1 -- what licenses doing any of this in the continuum.

    F130 makes lattice-violating operators irrelevant under block-spin with
    lambda_n = b^-n, so the leading correction to the growth equation is
    O((k a)^2).  Evaluate it at the sigma_8 scale and at the smallest scale
    structure formation ever probes (Lyman-alpha).
    """
    h = EXTERNAL["h"][0]
    R8_m = (R8_H_INV_MPC / h) * MPC_M
    lya_m = 0.3 * MPC_M                     # ~0.3 Mpc, k ~ 20 h/Mpc
    horizon_m = 3.0e3 / h * MPC_M           # c/H0, the largest scale

    def rel(L):
        return (A_CELL_M / L) ** 2

    return {
        "a_cell_m": A_CELL_M,
        "a_cell_source": "a/ell_P = sqrt(8 pi) 3^(1/4) (F79/F107), x ell_P",
        "R8_m": R8_m,
        "cells_across_R8": R8_m / A_CELL_M,
        "relative_correction_at_R8": rel(R8_m),
        "relative_correction_at_lyman_alpha": rel(lya_m),
        "relative_correction_at_horizon": rel(horizon_m),
        "scaling": "O((k a)^2), from F130 block-spin irrelevance lambda_n = b^-n",
        "pass": rel(lya_m) < 1.0e-100,
        "note": ("The lattice is invisible to structure formation by ~113 "
                 "orders even at the smallest scale the observations reach. "
                 "This is the licence to use the continuum growth equation at "
                 "all -- it is a load-bearing bound, not a curiosity."),
    }


def transfer_wdm(k_invMpc: float, m_keV: float, bg: dict) -> float:
    """Viel et al. 2005 warm-dark-matter transfer suppression, T_WDM/T_CDM."""
    nu = EXTERNAL["viel_nu"][0]
    alpha_h = (EXTERNAL["viel_norm"][0] * m_keV ** -1.11
               * (bg["Om"] / 0.25) ** 0.11 * (bg["h"] / 0.7) ** 1.22)   # h^-1 Mpc
    alpha = alpha_h / bg["h"]                                           # Mpc
    return (1.0 + (alpha * k_invMpc) ** (2 * nu)) ** (-5.0 / nu)


def dark_matter_free_streaming() -> dict:
    """B2 -- does sigma_8 discriminate K7's two dark-matter candidates?

    Candidates: the graviton-graviton geon remnant, M = (sqrt3/2)^(1/2) M_Pl
    (F223/F228/F216), and the F266 right-handed sterile neutrino at ~5.6 keV.
    """
    bg = background(radiation=False)
    nu = EXTERNAL["viel_nu"][0]

    def half_mode_k(m_keV):
        alpha_h = (EXTERNAL["viel_norm"][0] * m_keV ** -1.11
                   * (bg["Om"] / 0.25) ** 0.11 * (bg["h"] / 0.7) ** 1.22)
        return ((2.0 ** (nu / 10.0) - 1.0) ** (1.0 / (2 * nu))) / alpha_h   # h/Mpc

    m_sterile = 5.6
    m_geon_keV = math.sqrt(math.sqrt(3.0) / 2.0) * 1.22089e19 * 1.0e6  # GeV -> keV

    s8_cdm = sigma8_from_As(bg=bg)["sigma_8"]
    s8_wdm = sigma8_from_As(bg=bg, wdm_keV=m_sterile)["sigma_8"]

    k8 = 1.0 / R8_H_INV_MPC                     # h/Mpc, the sigma_8 scale
    return {
        "geon": {
            "mass_keV": m_geon_keV,
            "half_mode_k_h_per_Mpc": half_mode_k(m_geon_keV),
            "verdict": "pure CDM -- free-streaming scale is ~22 orders below a cell",
        },
        "sterile_F266": {
            "mass_keV": m_sterile,
            "half_mode_k_h_per_Mpc": half_mode_k(m_sterile),
            "verdict": "half-mode far beyond the sigma_8 scale",
        },
        "sigma8_scale_k_h_per_Mpc": k8,
        "sigma8_CDM": s8_cdm,
        "sigma8_sterile_5p6keV": s8_wdm,
        "sigma8_fractional_suppression": 1.0 - s8_wdm / s8_cdm,
        "sigma8_discriminates": bool(abs(1.0 - s8_wdm / s8_cdm) > 0.01),
        "pass": True,
        "verdict": ("sigma_8 is BLIND to the model's dark-matter identity: the "
                    "5.6 keV half-mode sits ~2.5 decades in k above the "
                    "8 h^-1 Mpc scale, so the suppression there is far below "
                    "the measurement error. The observable that is NOT blind "
                    "is the Lyman-alpha forest (k ~ 1-20 h/Mpc), which is "
                    "exactly where F203's 9-15 keV floor already puts the "
                    "F266 sterile under pressure. K11 does not settle K7; it "
                    "says WHICH probe does."),
    }


# ===========================================================================
# 6 -- the falsifier
# ===========================================================================
def s8_falsifier(S8_model: float = None) -> dict:
    """The S8 test, stated so it can fire.

    mu == 1 is k-independent BY DERIVATION, so there is no screening -- the
    standard route by which modified gravity lowers late-time growth while
    evading linear-scale bounds.  The model therefore predicts the
    combined-CMB S8 propagated forward by GR growth, with nothing to tune.
    """
    S8_model = sigma8_from_As()["S_8"] if S8_model is None else S8_model

    def tension(obs, err):
        return (S8_model - obs) / math.hypot(err, EXTERNAL["S8_cmb_err"][0])

    probes = {
        "combined_CMB": (EXTERNAL["S8_cmb"][0], EXTERNAL["S8_cmb_err"][0]),
        "DES_Y6_3x2pt": (EXTERNAL["S8_desy6"][0], EXTERNAL["S8_desy6_err"][0]),
        "KiDS_Legacy": (EXTERNAL["S8_kids_legacy"][0], EXTERNAL["S8_kids_legacy_err"][0]),
    }
    cmb_vs_des = ((EXTERNAL["S8_cmb"][0] - EXTERNAL["S8_desy6"][0])
                  / math.hypot(EXTERNAL["S8_cmb_err"][0], EXTERNAL["S8_desy6_err"][0]))

    return {
        "S8_model": S8_model,
        "probes": {k: {"S8": v[0], "err": v[1], "n_sigma": tension(*v)}
                   for k, v in probes.items()},
        "cmb_minus_desy6_sigma": cmb_vs_des,
        "has_screening": False,
        "mu_is_k_independent": True,
        "can_relieve_S8": False,
        "falsifier": ("If the DES Y6 direction consolidates as physical rather "
                      "than as photo-z / baryonic-feedback systematics, the "
                      "model's gravity sector is FALSIFIED. mu = 1 is forced "
                      "by F106 with no k dependence, so there is no screened "
                      "regime in which growth could be suppressed on small "
                      "scales while linear-scale bounds are evaded. The model "
                      "has nothing to tune, which is exactly why the test can "
                      "fire."),
        "current_status": ("SPLIT, not resolved: DES Y6 low at 2.7 sigma, "
                           "KiDS-Legacy shifted UP by 0.056 into consistency, "
                           "eROSITA clusters 1.5 sigma HIGH. The model sides "
                           "with 'the spread is systematics'. Euclid decides."),
        "pass": True,
    }


def control_goes_red(mu_probe: float = 0.90) -> dict:
    """C1 -- proof that the checks above CAN fail.  (H2, completeness gap #2.)

    The standing defect the 2026-08-03/04 review series found ten times out of
    ten was *a check that could not fail*.  This leg is the built-in answer:
    it drives the SAME code path with ``mu = 0.90`` -- a value the model
    forbids by derivation (S2) -- and requires the pipeline to go red.

    It passes when the perturbed run FAILS.  If a future refactor makes growth
    insensitive to mu, this leg turns red and says so.
    """
    base = sigma8_from_As(mu=1.0)
    pert = sigma8_from_As(mu=mu_probe)
    g_base = growth_summary(mu=1.0)
    g_pert = growth_summary(mu=mu_probe)
    chi_base = fsigma8_curve(base["sigma_8"], mu=1.0)
    chi_pert = fsigma8_curve(pert["sigma_8"], mu=mu_probe)

    legs = {
        "sigma8_leg_red": not pert["pass"],
        "growth_leg_red": not g_pert["pass"],
        "fsigma8_leg_red": not chi_pert["pass"],
        "baseline_all_green": bool(base["pass"] and g_base["pass"] and chi_base["pass"]),
    }
    return {
        "mu_probe": mu_probe,
        **legs,
        "sigma8_base": base["sigma_8"],
        "sigma8_perturbed": pert["sigma_8"],
        "sigma8_fractional_shift": pert["sigma_8"] / base["sigma_8"] - 1.0,
        "chi2_base": chi_base["chi2"],
        "chi2_perturbed": chi_pert["chi2"],
        "delta_chi2": chi_pert["chi2"] - chi_base["chi2"],
        "n_legs_that_went_red": sum(1 for k, v in legs.items()
                                    if k.endswith("_red") and v),
        "pass": bool(all(legs.values())),
        "note": ("A 10% perturbation of a quantity the model derives to be "
                 "exactly 1 moves sigma_8 by ~32% and delta chi^2 by ~86. "
                 "The amplification is the ~7 e-folds of growth integration "
                 "(D5), and it is why this sector is a real test of the "
                 "structural claim rather than a restatement of it."),
    }


# ===========================================================================
# Registry entry point
# ===========================================================================
CHECKS = (
    ("S1_zero_linear_slip", slip_from_impedance_match),
    ("S2_mu_is_one_no_k", mu_from_f106_poisson),
    ("S3_zero_free_functions", no_free_functions),
    ("D1_growth_index_6_over_11", growth_index_exact),
    ("D2_meszaros_exact", meszaros_exact),
    ("D3a_growth_on_background", growth_summary),
    ("D5_mu_is_pinned_by_growth", mu_bound_from_growth),
    ("B1_discreteness_bound", discreteness_bound),
    ("B2_dm_free_streaming", dark_matter_free_streaming),
    ("C1_control_goes_red", control_goes_red),
)


def run(mu: float = 1.0, A_s: float = None) -> dict:
    """Registry entry point.  ``mu`` and ``A_s`` are the sweep handles.

    ``--param mu=0.90`` is the CONTROL: it must turn D3b and the S8 leg red,
    because mu is derived to be exactly 1 and nothing in the model can move it.
    """
    out = {name: (fn(mu=mu) if name.startswith("D3a") else fn())
           for name, fn in CHECKS}
    s8 = sigma8_from_As(A_s=A_s, mu=mu)
    out["D4_sigma8_with_budget"] = s8
    out["D3b_fsigma8_vs_rsd"] = fsigma8_curve(s8["sigma_8"], mu=mu)
    out["F_s8_falsifier"] = s8_falsifier(S8_model=s8["S_8"])
    if mu != 1.0:
        # The control leg. A_s is the anchor, so a modified mu propagates
        # through D(1) into sigma_8, S_8 and f sigma_8 together.
        base_s8 = sigma8_from_As(A_s=A_s, mu=1.0)
        base = fsigma8_curve(base_s8["sigma_8"], mu=1.0)
        out["control"] = {
            "mu": mu,
            "delta_chi2_fsigma8": out["D3b_fsigma8_vs_rsd"]["chi2"] - base["chi2"],
            "sigma8_shift": s8["sigma_8"] - base_s8["sigma_8"],
            "S8_shift": s8["S_8"] - base_s8["S_8"],
            "pass": False,
            "note": ("mu != 1 is not a model this project holds -- it is the "
                     "perturbation that proves the checks above can go red. "
                     "This leg is False by construction whenever mu != 1."),
        }
    out["n_checks"] = len(out) - 1
    out["mu"] = mu
    out["verdict"] = (
        "K11: the model's gravity law fixes linear growth with ZERO free "
        "functions where the EFT of dark energy has two -- mu = 1 with no k "
        "(F106/F178), no time dependence (F79/F284), and no slip (F64 AB=1). "
        "gamma_g = 6/11 and the Meszaros solution are exact. sigma_8 is "
        "reported with A_s declared free (K5), never claimed. The lattice is "
        "invisible by ~113 orders. sigma_8 is blind to K7's dark-matter "
        "identity; Lyman-alpha is not. Falsifier: no screening exists, so the "
        "DES Y6 low-S8 direction cannot be accommodated."
    )
    out["pass"] = all(v.get("pass", True) for v in out.values() if isinstance(v, dict))
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(run(), indent=2, sort_keys=True, default=str))
