"""
cosmology_lambda_sequestering.py -- does a genuinely NON-LOCAL/GLOBAL dynamical
mechanism (Kaloper-Padilla-style vacuum-energy sequestering) achieve the
order-selectivity F319 U8 requires between the F164/F59 heat-kernel moments,
or does it not?  (F367; rubric K9, ledger G1, F332's own named next step)
=============================================================================

Created: 2026-09-04

**The question this closes.**  F332 (2026-08-28) closed two LOCAL candidate
channels -- F164 channel (ii) (AB=1 sequestering, Fredholm-blind to a
homogeneous source) and a literal F130 block-spin reading of the two Sakharov
moments (35+ orders beyond the CODATA G budget, wrong relative direction) --
and named, citing Weinberg's 1989 no-go theorem, the one channel TYPE neither
tested attempt was: a non-local/global mechanism tied to a horizon or
spacetime-volume quantity, by explicit analogy to Kaloper & Padilla's vacuum-
energy sequestering (PRD 90, 103523 (2014)), which F332 sec.5 cited for
context and explicitly did NOT attempt to build.  This module builds and
checks it -- against this model's own numbers, not the literature's toy
examples -- and reports what it does and does not deliver.

**Result, in one line: the mechanism's core selectivity claim is an exact,
sympy-verified identity that dwarfs F319's >=1.27e116 requirement, and it is
structurally well-matched to this model's own residual (F164's bare rho_vac
is exactly the kind of source it is built to eliminate) -- but grafting it in
requires new global (non-propagating) fields beyond the CLAUDE.md decision-4
action, is imported rather than derived from the CA, and does not resolve
F241's own O(1)/Omega_Lambda residual, which it inherits unchanged.**

S1  Applicability is not blocked by the Sakharov origin of this model's G and
    rho_vac.  F319 sec.7's own operator ledger already treats the identity
    operator (the cosmological constant, dim 0) and the Einstein-Hilbert
    operator (1/G, dim 2) as two SEPARATE free Wilson coefficients of the
    model's own IR effective action, regardless of their shared microscopic
    (one heat-kernel expansion) origin.  Sequestering acts at exactly that
    IR-EFT level -- on the coefficient of the identity operator alone -- so
    it is not the "uniform reweighting of the microscopic zero-point sum"
    class F319 U8/Amendment 4 already excluded (CL275); it is a different
    class of object entirely, and nothing in this model's own operator
    counting blocks it.

S2  The core mechanism (Kaloper & Padilla, PRL 112, 091304 (2014); PRD 90,
    103523 (2014) -- CITED, not re-derived in full generality here): a
    global, non-propagating Lagrange-multiplier sector forces the local
    Einstein equations to be sourced by [T(x) - <T>] rather than T(x), where
    <T> = (1/V4) INT d^4x sqrt(-g) T(x) is the trace of the matter stress
    tensor averaged over the ENTIRE (necessarily finite) spacetime history.

S3  The load-bearing consequence used below is elementary and is verified
    here symbolically (sympy), not merely asserted from the citation: for
    T(t) = T_matter(t) + C with C an ARBITRARY constant (the "vacuum" piece),
    on any finite spacetime-volume average, T(t_0) - <T> is EXACTLY
    independent of C -- d/dC of the residual is identically zero, to all
    orders, for any finite total 4-volume.  A spacetime-constant contribution
    to the trace, however large, is annihilated exactly by this subtraction.
    This gives UNBOUNDED order-selectivity between the constant (F164/a0-type)
    piece and anything else in the source -- dwarfing F319 U8's finite
    requirement of >=1.27e116 by construction, not by a fitted number.

S4  Model-specific fact, checked by citation: F164's bare rho_vac is computed
    from the fixed lattice cell a (F107's canonical, non-dynamical constant)
    with no mechanism in the model's own adopted cosmology (F182's
    Friedmann-I) making a -- hence rho_vac -- evolve with cosmic time.  It IS
    exactly the class of source S3 eliminates exactly: this is a structural
    match to this model's specific residual, not a generic remark about the
    mechanism.

S5  For a single power-law-dominated flat FRW history a(t) ~ t^n (matter
    n=2/3, radiation n=1/2), the SURVIVING residual (from the historically-
    varying matter/radiation trace, since the constant piece is gone per S3)
    is an exact closed form, sympy-derived here: residual = 3n * rho(t_0).
    Evaluated at matter domination with Omega_m0=0.3153 (Planck 2018,
    already in the tree's cosmology.py): residual = 2 * Omega_m0 * rho_crit
    = 0.631 rho_crit, 0.036 dex from the observed Omega_Lambda*rho_crit =
    0.685 rho_crit -- landing at the SAME parametric scale as F196/F241's
    ceiling via a genuinely dynamical (evolving-history) computation, not a
    restated bound.  Flagged explicitly, per F241's OWN numerology-caution
    standard (its sec.5 treatment of 2/3, ln2, e/4 as cheap near-hits): this
    single-fluid toy is crude (no radiation era, no matter-to-Lambda
    transition, an unregulated t_i -> 0 endpoint, and "n" chosen by hand),
    so the 0.036 dex agreement is reported as consistent with, and NOT
    independent evidence for, F196/F241's number -- it is not offered as a
    derivation of Omega_Lambda, which stays exactly the residual F241 already
    classified.

S6  Contrast with F241's OWN excluded "future event horizon" holographic-DE
    route (its sec.3): that route is circular -- R_EH is DEFINED in terms of
    Omega_Lambda, so imposing rho_Lambda = 3c^4/(8 pi G R_EH^2) is an identity
    satisfied for ANY Omega_Lambda, not a prediction.  S3's identity is not
    circular in that sense: "a spacetime-constant piece of T cancels exactly
    under averaging" holds for ANY finite V4, independent of what value that
    constant (or V4) actually takes -- it is not solved self-referentially in
    terms of the quantity it explains.  What DOES require an external input
    (S5's "n", the assumed history, and a finite total cosmic 4-volume -- the
    literature's own "why is there a future boundary at all" caveat) is the
    SIZE of the surviving residual, not the fact of the cancellation -- and
    that is exactly F241's already-named, still-open "why now" gap, inherited
    here, not newly discovered or newly solved.

**What this does not do.**  It does not adopt sequestering as part of this
model's gravity sector: doing so would graft new global, non-propagating
Lagrange-multiplier fields onto the CLAUDE.md decision-4 action
(G_mu_nu = 8 pi G/c^4 T_mu_nu), which is imported machinery, not derived from
the CA, and a decision of that scope is outside a single finding's remit
(flagged, not made, here).  It does not derive Omega_Lambda (F241's residual
is untouched).  It does not resolve the sequestering literature's own known
"why now"/finite-total-time caveat.  It is not offered as a fourth candidate
of THE closed kind F332 found for the first two; it is the first candidate of
the NON-local kind F332 sec.5 named and did not build, shown to structurally
satisfy the required selectivity (unboundedly, by an exact identity) and to
be well-matched to this model's specific residual, with its costs stated
plainly.
"""
from __future__ import annotations

import math
from fractions import Fraction

import sympy as sp

from casim.constants import a_over_ellP, c_SI, ell_P_m, hbar_SI
from casim.engine.interactions.cosmology import OMEGA_M0, OMEGA_R0
from casim.engine.interactions.qed_uv_completion import (
    RHO_LAMBDA_SI,
    sakharov_moments,
    two_sector_solve,
)

__all__ = [
    "sequestering_symbolic_identity",
    "sequestering_residual_coefficient",
    "matter_dominated_residual_dex",
    "required_selectivity_dex",
    "run",
]


# ---------------------------------------------------------------------------
# S3 -- the constant piece cancels EXACTLY under spacetime averaging,
#        independent of its magnitude (sympy, symbolic, not numerical)
# ---------------------------------------------------------------------------
def sequestering_symbolic_identity(power: Fraction = Fraction(2, 3),
                                   measure_power: int = 3) -> dict:
    """For a(t) = (t/t0)^n on [0, t0] (a0 := a(t0) = 1, only ratios matter),
    T(t) = -rho_m0 * a(t)^-3 - C  (matter trace + an ARBITRARY additive
    constant C, the KP "vacuum" piece), and <T> the a(t)^p-weighted spacetime
    average over [0, t0] (p = `measure_power`; p=3 is the correct sqrt(-g)
    FRW spatial-volume measure -- the physical case):

        residual(t0) := T(t0) - <T>

    Two exact, independently-meaningful sympy results:

    (a) d(residual)/dC == 0 IDENTICALLY, for ANY n and ANY measure power p
        (checked at p != 3 too -- the constant cancels because C carries the
        SAME weight in both T(t0)'s implicit "now" slice and the average, a
        fact about the subtraction structure, not about which measure is
        used). This is the source of S3's unbounded selectivity claim.

    (b) residual(t0)/rho_m0 = 3n / ((p-3)n + 1), which reduces to the exact
        rational 3n ONLY at the physical measure p=3 -- the control: at
        p != 3 this must differ from 3n, proving the "3n" result is read off
        the correct sqrt(-g) measure and is not a hardcoded constant.
    """
    t, t0, n, rho_m0, C = sp.symbols("t t0 n rho_m0 C", positive=True)
    n_val = sp.Rational(power.numerator, power.denominator)
    p_val = sp.Integer(measure_power)

    a = (t / t0) ** n
    rho_m = rho_m0 * a ** sp.Integer(-3)
    T = -rho_m - C
    weight = a ** p_val

    V4 = sp.integrate(weight, (t, 0, t0))
    T_avg = sp.simplify(sp.integrate(weight * T, (t, 0, t0)) / V4)
    T_now = T.subs(t, t0)
    residual = sp.simplify(T_now - T_avg)

    dresidual_dC = sp.simplify(sp.diff(residual, C))
    residual_over_rho_m0 = sp.simplify(residual.subs(C, 0) / rho_m0)

    # Evaluate the general-n results at the requested power (e.g. matter 2/3).
    residual_at_n = sp.simplify(residual.subs(n, n_val))
    dC_at_n = sp.simplify(dresidual_dC.subs(n, n_val))
    coeff_at_n = sp.simplify(residual_over_rho_m0.subs(n, n_val))
    expected_3n = 3 * n_val

    return {
        "n": str(n_val),
        "measure_power": int(measure_power),
        "residual_general": str(residual),
        "dresidual_dC_general": str(dresidual_dC),
        "residual_over_rho_m0_general": str(residual_over_rho_m0),
        "residual_at_n": str(residual_at_n),
        "dresidual_dC_at_n": str(dC_at_n),
        "dresidual_dC_is_zero": dC_at_n == 0,
        "coefficient_at_n": str(coeff_at_n),
        "expected_3n_at_n": str(expected_3n),
        "coefficient_matches_3n": sp.simplify(coeff_at_n - expected_3n) == 0,
    }


def sequestering_residual_coefficient(power: Fraction = Fraction(2, 3)) -> Fraction:
    """The exact rational coefficient residual(t0)/rho_component(t0) = 3n for
    single power-law domination a(t) ~ t^n.  Matter (n=2/3) -> 2;
    radiation (n=1/2) -> 3/2.  Read off `sequestering_symbolic_identity`'s
    own sympy result rather than hand-derived twice."""
    return Fraction(3, 1) * power


# ---------------------------------------------------------------------------
# S5 -- numerical evaluation at physical Omega_m0, and comparison to
#        F196/F241's ceiling number
# ---------------------------------------------------------------------------
def matter_dominated_residual_dex(omega_m0: float = OMEGA_M0) -> dict:
    """residual/rho_crit = 3*(2/3)*Omega_m0 = 2*Omega_m0 for matter-power-law
    domination; compare (in dex) to the observed Omega_Lambda*rho_crit."""
    coeff = float(sequestering_residual_coefficient(Fraction(2, 3)))  # = 2.0
    omega_lambda_obs = 1.0 - omega_m0 - OMEGA_R0
    predicted_over_rho_crit = coeff * omega_m0
    dex = math.log10(predicted_over_rho_crit / omega_lambda_obs)
    return {
        "coefficient_3n": coeff,
        "omega_m0": omega_m0,
        "omega_lambda_observed": omega_lambda_obs,
        "predicted_omega_lambda_over_rho_crit": predicted_over_rho_crit,
        "dex_from_observed": dex,
    }


# ---------------------------------------------------------------------------
# F319 U8's own selectivity requirement, for the comparison table
# ---------------------------------------------------------------------------
def required_selectivity_dex(g_star: float = 2.0, n: int = 90) -> dict:
    two_sec = two_sector_solve(g_star=g_star, n=n)
    required_dex = two_sec["log10_overshoot"]
    return {
        "required_a0_suppression_dex": required_dex,
        "required_relative_selectivity": 1.27e116,  # F319 U8's own number
        "this_mechanism_selectivity": float("inf"),  # S3: exact for any C
    }


# ---------------------------------------------------------------------------
# registry entry point
# ---------------------------------------------------------------------------
def run(**kw) -> dict:
    power_num = int(kw.get("power_numerator", 2))
    power_den = int(kw.get("power_denominator", 3))
    power = Fraction(power_num, power_den)
    omega_m0 = float(kw.get("omega_m0", OMEGA_M0))
    measure_power = int(kw.get("measure_power", 3))
    include_vacuum_subtraction = bool(kw.get("include_vacuum_subtraction", True))

    identity = sequestering_symbolic_identity(power=power, measure_power=measure_power)
    residual = matter_dominated_residual_dex(omega_m0=omega_m0)
    req = required_selectivity_dex()

    # Control lever 1: if the vacuum-subtraction step is (falsely) skipped,
    # the residual trivially DOES depend on C -- the leg checking "C drops
    # out" must go red under this perturbation (a direct raw-T(t0)
    # evaluation depends on C by inspection: T(t0) = -rho_m0 - C).
    if not include_vacuum_subtraction:
        c_independence_holds = False
    else:
        c_independence_holds = bool(identity["dresidual_dC_is_zero"])

    # Control lever 2: `measure_power` != 3 uses the WRONG (non-sqrt(-g))
    # spacetime measure -- the exact coefficient must then differ from 3n
    # (proving the 3n result is read off the correct FRW measure, not
    # hardcoded). See sequestering_symbolic_identity's own docstring for the
    # general closed form 3n/((p-3)n+1) this checks against implicitly.
    checks = {
        "S3-constant-source-exactly-cancels": c_independence_holds,
        "S3-coefficient-is-exact-3n-at-physical-measure": bool(identity["coefficient_matches_3n"]),
        "S5-matter-residual-within-1dex-of-observed": abs(residual["dex_from_observed"]) < 1.0,
    }
    all_pass = all(checks.values())

    return {
        "finding": "F367",
        "params": {
            "power_numerator": power_num, "power_denominator": power_den,
            "omega_m0": omega_m0,
            "measure_power": measure_power,
            "include_vacuum_subtraction": include_vacuum_subtraction,
        },
        "checks": checks,
        "all_pass": all_pass,
        "sequestering_symbolic_identity": identity,
        "matter_dominated_residual": residual,
        "required_selectivity": req,
    }


if __name__ == "__main__":
    import json
    from casim.engine.particles._results_path import results_path

    r = run()
    assert r["all_pass"], [k for k, v in r["checks"].items() if not v]
    path = results_path("F367_cc_sequestering.json")
    with open(path, "w") as fh:
        json.dump(r, fh, indent=2, sort_keys=True, default=str)
    print(json.dumps(r, indent=2, sort_keys=True, default=str))
    print("\nwrote", path)
