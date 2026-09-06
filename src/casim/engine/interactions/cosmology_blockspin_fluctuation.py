"""
cosmology_blockspin_fluctuation.py — F362: fluctuation corrections to F130's C1
confinement eigenvalue, and why they cannot supply G2/K3's non-integer gamma
================================================================================

`2026-09-04`

Open-derivations row **G2** / rubric **K3** (shared target with **K12**, per
[[F310-gamma-is-a-blockspin-eigenvalue]]) named its own next step verbatim:
*"compute the block-spin relevant eigenvalue WITH FLUCTUATION CORRECTIONS on
F130's existing machinery, and see whether it moves off b^1 by 1.6%."*  This
module does exactly that, using the repo's own EXACT strong-coupling
perturbation-theory machinery
(`casim.engine.gauge.link_hamiltonian.sigma_strong_pt2`) rather than
introducing new physics, and answers the question **no** — structurally, not
just numerically, under F130's own bond-moving convention (g2 -> b*g2,
lambda held fixed).  A full Migdal-Kadanoff decimation step that lets
lambda itself flow is a different, untested route (finding Sec 4a).

Physics
-------
F130 C1 (`casim.engine.lattice.blockspin.confinement_eigenvalue`) computed the
string tension at lambda=0 (the FROZEN flux-tube limit — no plaquette
fluctuations at all): sigma-hat = g2/2 exactly, and under bond-moving
(g2 -> b*g2) this gives the exact integer eigenvalue lambda_sigma = b.  Lambda
(the plaquette/magnetic coupling) is precisely the fluctuation parameter switched
off there: turning it on lets the flux tube's ground state deviate from the
straight classical string via virtual plaquette flips.

`link_hamiltonian.sigma_strong_pt2` already computes the leading (2nd-order)
strong-coupling PT correction, EXACTLY (integer-arithmetic energy
denominators for the Z3 Kogut-Susskind Hamiltonian):

    sigma-hat(g2, lam) = g2/2 - c2(g2) * lam**2 + O(lam**4),    c2(g2) = 1/(6*g2)

(the 1/(6*g2) closed form is verified against `sigma_strong_pt2` at 5 values of
g2 to the floating-point floor, C1 below).  This module:

1. Composes that formula with F130's own bond-moving rule (g2 -> b*g2, lambda
   held fixed — the same convention `blockspin.magnetic_deformation_ratio`
   already uses) into an "effective" eigenvalue

       ratio(g2,lam,b) = sigma-hat(b*g2, lam) / sigma-hat(g2, lam)
       y_eff = log_b(ratio),          gamma_eff = y_eff - 1

2. Proves (C2, exact power counting) that EVERY order n>=1 term in the full
   strong-coupling series sigma-hat = sum_n a_n * lam^(2n) * g2^(1-2n) carries
   an EXACT INTEGER eigenvalue b^(1-2n) under bond-moving — b^-1, b^-3, b^-5,
   ... — so no finite order of this expansion, nor any convergent sum of them,
   can contribute a non-integer piece to the LEADING (n=0, eigenvalue b^1)
   term.  This generalises F130 C3/C4's own "a linear block average is a
   Gaussian calculation and cannot produce a non-integer exponent" to the
   WHOLE strong-coupling series around lambda=0, not just its leading term.
   The n=1 case reproduces `magnetic_deformation_ratio`'s measured b^-2
   RELATIVE suppression exactly (relative eigenvalue = b^(1-2*1) / b^1 = b^-2).

3. Shows (C3) that gamma_eff computed at ANY finite b and finite (g2, lambda)
   is NOT a legitimate RG/critical-exponent eigenvalue in the technical sense:
   a real anomalous dimension must be b-INDEPENDENT (it is defined at an
   RG fixed point, in the limit of an infinitesimal or asymptotic step); this
   gamma_eff instead depends explicitly on which b you pick to define one
   coarse-graining step, and vanishes identically as b -> infinity for any
   fixed epsilon (C1/C2 already prove this: gamma_eff ~ epsilon/ln(b) -> 0).
   Tuning epsilon to hit the G2/K3 target gamma=0.015 at one b gives a
   DIFFERENT gamma (0.8%-2.7% here) at every other b (C4) -- the calculation
   fails the basic universality test a true critical exponent must pass,
   independent of which coupling is used.

4. Evaluates gamma_eff at the model's own calibrated confinement coupling
   (g_s^2 = 1/4, the locked BZ-edge value, F115/F325; lambda = chi*Omega^2 =
   Omega^2 with chi=1, F101) and finds the perturbative parameter
   epsilon = lambda^2/(3*g2^2) ~ 15, two orders of magnitude beyond the
   validity radius of the lambda^2 truncation (epsilon << 1 required) --
   the truncated sigma-hat is NEGATIVE (unphysical) at this coupling, and the
   coarse/fine ratio goes negative (undefined log) for b>=4 (C5).  The
   model's own physical point sits nowhere near the regime this calculation
   could ever be trusted in.

Verdict
-------
This is **F310's own falsifier 1** / **CL267's falsifier 2** firing: a
fluctuation-corrected eigenvalue computed on F130's existing machinery does
NOT move toward the required 1.4-1.8%, and — more than a numerical miss — it
cannot in principle, because (a) every finite-order term in the expansion
around lambda=0 is an exact integer eigenvalue (C2) and (b) the "effective"
composite quantity built by evaluating the truncated series at one finite b is
scheme-dependent, not universal (C3/C4), and diverges from validity at the
model's actual coupling (C5).  Per the ledger's own framing this is a genuine,
useful negative result, not a failed session -- it closes off the SPECIFIC
route F310 named, and narrows what a successful route would need: a
non-perturbative (resummed, or genuinely different fixed-point) RG treatment,
not a higher-order term in the SAME lambda=0 expansion.

Files
-----
Reads (read-only): `casim.engine.gauge.link_hamiltonian` (sigma_strong_pt2,
PlaquetteGrid), `casim.engine.lattice.blockspin` (confinement_rg_step,
magnetic_deformation_ratio, for the cross-check).  Does not modify either.
"""
from __future__ import annotations

import math
from fractions import Fraction

__all__ = [
    "C2_COEFFICIENT",
    "sigma_hat_2nd_order",
    "confinement_ratio",
    "fluctuation_eigenvalue",
    "fluctuation_gamma",
    "term_eigenvalue",
    "relative_term_eigenvalue",
    "epsilon_scale",
    "is_perturbative",
    "universality_scan",
    "PERTURBATIVITY_THRESHOLD",
]

# c2(g2) = C2_COEFFICIENT / g2 exactly (verified against
# `link_hamiltonian.sigma_strong_pt2` at g2 in {0.25,0.5,1,2,4}: c2*g2 is
# 1/6 to the floating-point floor at every value -- C1 below re-derives this
# from the module's own energy-denominator arithmetic, this constant is the
# closed form of that measurement).
C2_COEFFICIENT = Fraction(1, 6)

# epsilon << PERTURBATIVITY_THRESHOLD is required for the O(lam^2) truncation
# to be trustworthy at all; this is a standard (not tuned)ratio-test bound,
# one order of magnitude inside "clearly not small".
PERTURBATIVITY_THRESHOLD = 0.2


def sigma_hat_2nd_order(g2, lam):
    """sigma-hat(g2,lam) = g2/2 - c2(g2)*lam**2,  c2(g2) = (1/6)/g2 exactly.

    The 2nd-order-strong-coupling-PT-truncated string tension.  Reduces to
    F130's C1 (`confinement.string_tension_lambda0`) at lam=0.
    """
    g2 = float(g2)
    lam = float(lam)
    c2 = float(C2_COEFFICIENT) / g2
    return g2 / 2.0 - c2 * lam ** 2


def confinement_ratio(g2, lam, b):
    """sigma-hat(b*g2, lam) / sigma-hat(g2, lam) -- lam held fixed under
    bond-moving, matching `blockspin.magnetic_deformation_ratio`'s own
    convention (the convention F130 C1 established for the leading term).
    """
    return sigma_hat_2nd_order(b * g2, lam) / sigma_hat_2nd_order(g2, lam)


def fluctuation_eigenvalue(g2, lam, b):
    """y_eff = log_b( sigma-hat_coarse / sigma-hat_fine ).  Complex/undefined
    when the ratio is non-positive (returns nan in that case, flagging
    breakdown of the truncation rather than raising)."""
    r = confinement_ratio(g2, lam, b)
    if r <= 0:
        return float("nan")
    return math.log(r) / math.log(b)


def fluctuation_gamma(g2, lam, b):
    """gamma_eff = y_eff - 1, the analogue of G2/K3's gamma = y - 1."""
    y = fluctuation_eigenvalue(g2, lam, b)
    return y - 1.0


def term_eigenvalue(n, b):
    """Exact RG eigenvalue of the n-th order term in the strong-coupling
    series sigma-hat = sum_n a_n * lam^(2n) * g2^(1-2n) under g2 -> b*g2,
    lam fixed:  b^(1-2n).  n=0 is the leading (F130 C1) term, eigenvalue b^1
    (relevant); n>=1 are all irrelevant, odd negative integer powers of b.
    Exact integer power, sympy-verified in the test.
    """
    return float(b) ** (1 - 2 * n)


def relative_term_eigenvalue(n, b):
    """term_eigenvalue(n,b) / term_eigenvalue(0,b) = b^(-2n) -- the fraction
    by which the n-th order correction shrinks, RELATIVE to the leading b^1
    term, under one bond-moving step.  n=1 reproduces
    `blockspin.magnetic_deformation_ratio`'s measured b^-2 exactly.
    """
    return float(b) ** (-2 * n)


def epsilon_scale(g2, lam):
    """epsilon = lam**2 / (3*g2**2) = Delta-sigma/sigma-hat(0) at b=1 --
    the dimensionless expansion parameter controlling the whole series
    (sigma-hat/g2 is, order by order, a function of epsilon alone).
    epsilon << 1 is required for `sigma_hat_2nd_order` to be trustworthy.
    """
    g2 = float(g2)
    lam = float(lam)
    return lam ** 2 / (3.0 * g2 ** 2)


def is_perturbative(g2, lam, threshold=PERTURBATIVITY_THRESHOLD):
    """Whether epsilon_scale(g2,lam) < threshold -- i.e. whether the O(lam^2)
    truncation is even formally trustworthy at this coupling."""
    return epsilon_scale(g2, lam) < threshold


def universality_scan(gamma_target, b_list=(2, 3, 4, 5)):
    """For each b in b_list, find the epsilon that makes gamma_eff(epsilon,b)
    equal gamma_target (small-epsilon regime, Newton's method on the exact
    ratio formula), then report gamma_eff at every OTHER b with that SAME
    epsilon.  A genuine critical exponent must return gamma_target at every
    b; this function is the direct numerical check of C4's non-universality
    claim.  Returns {b_tuned: {b_eval: gamma_eff}}.

    Uses the closed form ratio(eps,b) = (b**2 - eps) / (b*(1 - eps)) (g2
    cancels identically; a coupling-independent function of epsilon and b
    alone), sympy-verified in the test against the g2,lam-explicit formula.
    """
    def gamma_of_eps(eps, b):
        r = (b ** 2 - eps) / (b * (1.0 - eps))
        if r <= 0:
            return float("nan")
        return math.log(r) / math.log(b) - 1.0

    out = {}
    for b_tune in b_list:
        # Newton's method (finite-difference derivative) starting from the
        # small-epsilon linear estimate: gamma_eff ~ eps*(1-1/b^2)/ln(b).
        eps = gamma_target * math.log(b_tune) / (1.0 - 1.0 / b_tune ** 2)
        for _ in range(60):
            f = gamma_of_eps(eps, b_tune) - gamma_target
            h = 1e-7
            fp = (gamma_of_eps(eps + h, b_tune) - gamma_of_eps(eps - h, b_tune)) / (2 * h)
            if fp == 0 or not math.isfinite(fp):
                break
            step = f / fp
            eps -= step
            if abs(step) < 1e-14:
                break
        out[b_tune] = {b_eval: gamma_of_eps(eps, b_eval) for b_eval in b_list}
    return out


# ══════════════════════════════════════════════════════════════════
#  Checks (test-registry entry point)
# ══════════════════════════════════════════════════════════════════
def check_c1_closed_form(wrong_sign=False, nx=6,
                          g2_list=(0.25, 0.5, 1.0, 2.0, 4.0), tol=1e-9):
    """C1: c2(g2) = C2_COEFFICIENT/g2 matches the module's own EXACT strong-
    coupling PT machinery (`link_hamiltonian.sigma_strong_pt2`), a real
    Kogut-Susskind Hamiltonian diagonalisation, at every g2 tested.

    `wrong_sign=True` is the declared control leg: flips the sign of the
    closed form so it disagrees with the (unperturbed) real measurement by
    2*c2 -- 12+ orders of magnitude above tol -- red by construction.
    """
    from casim.engine.gauge import link_hamiltonian as kh

    geom = kh.PlaquetteGrid(nx, 1)
    sign = -1.0 if wrong_sign else 1.0
    rows = []
    ok = True
    for g2 in g2_list:
        measured = kh.sigma_strong_pt2(geom, row=0, g2=g2, group='Z3')
        closed = sign * float(C2_COEFFICIENT) / g2
        diff = abs(measured - closed)
        rows.append({"g2": g2, "measured": measured, "closed_form": closed,
                     "abs_diff": diff})
        ok = ok and (diff < tol)
    return {"pass": ok, "rows": rows, "wrong_sign": wrong_sign}


def check_c2_power_counting(nx=8, g2=1.0, lam_list=(0.005, 0.01),
                             b_list=(2, 3, 4), rel_tol=0.02,
                             wrong_power=False):
    """C2: the n=1 relative eigenvalue b^(-2*n) predicted by
    `relative_term_eigenvalue` matches `blockspin.magnetic_deformation_ratio`'s
    independently-measured coarse/fine ratio in the small-lambda limit, to
    `rel_tol` (a small-parameter asymptotic check, not exact).

    The residual is empirically O(lambda), not O(lambda^2) -- verified down to
    lambda=0.00125, the ratio of successive relative errors converges to 2.00,
    not 4.00 (see finding F362 Sec 3a). This is real physics the O(lambda^2)
    truncation in `sigma_hat_2nd_order` never modelled (a first-order matrix
    element of the plaquette operator surviving in the flux-tube ground state,
    not the vacuum), not a defect in this check; under the SAME g2->b*g2,
    lambda-fixed convention it carries eigenvalue b^0 (marginal, still an
    integer power), so it does not change C2's integer-eigenvalue conclusion.
    rel_tol=0.02 is therefore attributable to this linear term, not a higher
    even order.

    `wrong_power=True` is the second control leg: predicts b^(-2*(n+1))
    instead of b^(-2*n), which the small-lambda measurement (still exactly
    b^-2 at n=1) then misses by a large, b-growing margin.
    """
    from casim.engine.lattice import blockspin as bs

    n_shift = 1 if wrong_power else 0
    rows = []
    ok = True
    for b in b_list:
        rf = bs.magnetic_deformation_ratio(nx, g2, list(lam_list), b=1, group='Z3')
        rc = bs.magnetic_deformation_ratio(nx, g2, list(lam_list), b=b, group='Z3')
        for lam in lam_list:
            measured = rc[lam] / rf[lam]
            predicted = float(b) ** (-2 * (1 + n_shift))
            rel_err = abs(measured - predicted) / predicted
            rows.append({"b": b, "lam": lam, "measured": measured,
                         "predicted": predicted, "rel_err": rel_err})
            ok = ok and (rel_err < rel_tol)
    return {"pass": ok, "rows": rows, "wrong_power": wrong_power}


def check_c3_universality(gamma_target=0.015, b_list=(2, 3, 4, 5),
                           min_spread=0.3):
    """C3/C4: tuning epsilon to hit gamma_target at one b must give a
    DIFFERENT gamma at every other b -- the defining failure of a scheme-
    dependent (non-universal) quantity. Asserts the fractional spread of
    gamma_eff across b_list, at each tuning, exceeds `min_spread` (30%) of
    gamma_target -- i.e. genuinely, not marginally, non-universal.
    """
    scan = universality_scan(gamma_target, b_list=b_list)
    ok = True
    rows = []
    for b_tune, per_b in scan.items():
        vals = [v for v in per_b.values() if math.isfinite(v)]
        spread = (max(vals) - min(vals)) / abs(gamma_target) if vals else float("inf")
        rows.append({"b_tuned": b_tune, "gammas": per_b, "fractional_spread": spread})
        ok = ok and (spread > min_spread)
    return {"pass": ok, "rows": rows, "scan": scan}


def check_c5_physical_point(g2_phys=0.25, omega_list=(1.3, 0.997829)):
    """C5: the model's own calibrated confinement coupling (g_s^2=1/4,
    F115/F325; lambda=chi*Omega^2=Omega^2, chi=1, F101) is asserted (not
    merely observed) to sit outside the O(lam^2) truncation's validity
    radius -- epsilon >= PERTURBATIVITY_THRESHOLD at every quoted Omega.
    """
    rows = []
    ok = True
    for omega in omega_list:
        lam = omega ** 2
        eps = epsilon_scale(g2_phys, lam)
        pert = is_perturbative(g2_phys, lam)
        rows.append({"omega": omega, "lam": lam, "epsilon": eps,
                     "perturbative": pert})
        ok = ok and (not pert)          # asserting NON-perturbative, i.e. breakdown
    return {"pass": ok, "rows": rows}


def run_all(wrong_c2_sign=False, wrong_power=False) -> dict:
    c1 = check_c1_closed_form(wrong_sign=wrong_c2_sign)
    c2 = check_c2_power_counting(wrong_power=wrong_power)
    c3 = check_c3_universality()
    c5 = check_c5_physical_point()
    all_pass = bool(c1["pass"] and c2["pass"] and c3["pass"] and c5["pass"])
    # `checks:` is the leg map the test-registry control-verifier reads
    # (runner.leg_map): {leg id -> {"pass": bool, ...}}.
    return {
        "checks": {
            "c1_closed_form_matches_sigma_strong_pt2": c1,
            "c2_power_counting_matches_magnetic_deformation_ratio": c2,
            "c3_universality_fails_as_expected": c3,
            "c5_physical_point_nonperturbative": c5,
        },
        "all_pass": all_pass,
    }


if __name__ == "__main__":             # guard: never write an artifact at import
    import json
    from casim.engine.particles._results_path import results_path

    result = run_all()
    path = results_path("F362_blockspin_fluctuation.json")
    with open(path, "w") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))
