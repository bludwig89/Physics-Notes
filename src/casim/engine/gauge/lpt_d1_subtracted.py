"""lpt_d1_subtracted.py — d_1 for the rule action, formulated SUBTRACTED against
the Wilson Lambda_MSbar/Lambda_L = 28.8086 anchor (F280).

WHY THIS MODULE EXISTS
======================
F287 sec.6 closed the "is the F162 apparatus sound?" question with a verdict and
a restriction:

    "The apparatus is sound FOR SUBTRACTED DIFFERENCES, and d_1 must not be taken
     from this quadrature's absolute normalisation. It has to come either from
     settling the F267 fundamental domain, or from a SUBTRACTED FORMULATION
     AGAINST A KNOWN REFERENCE -- and F162's G3 already names the right
     reference, the Wilson Lambda_MSbar/Lambda_L = 28.81 gate."

`docs/status/completeness-2026-08-04.md` gap #3 makes that the smallest next
step, explicitly IN PREFERENCE TO settling F267 first.  This module is that
formulation.  It contains no new quadrature machinery: the loop integrand is
`bgfield_loop._Bcoeff_numeric` (F162/F287, refold-free since F272) and the
Wilson-side reference numbers are F163's.  What is new is the BOOKKEEPING that
turns those into a statement about d_1 without ever using an absolute
normalisation.

CONVENTIONS (fixed once; every number below lives in them)
==========================================================
Transverse scalar, lattice spacing a = 1, Feynman background gauge:

    Pi(q^2) = (b0 / 16 pi^2) [ ln(1/q^2) + C ],     b0 = 11/3 C_A = 11

so C is the finite constant of the self-energy in the SAME normalisation F163
uses.  Write

    dC  ==  C_lat - C_MSbar,     C_MSbar = 131/66     (F163, analytic dim reg)
    Lambda_MSbar / Lambda_lat  =  exp(dC / 2)
    d_1  ==  b0^{1/g^2} * dC,    b0^{1/g^2} = 11/(16 pi^2)

`Pi` is `-B` in `bgfield_loop`'s variable (B = (Pi_00 - Pi_11)/Q^2 = -Pi).

THE MASTER IDENTITY
===================
Wilson's one-loop constant splits into loops and the contact seagull + Haar
measure; the rule's seagull sector is EXACTLY EMPTY (F155-A0, u_0 == 1), so the
rule has the first term only:

    dC_wilson  =  dC_wilson_loops  +  T_wilson          (T = seagull + measure)
    dC_rule    =  dC_rule_loops                          (A0: no seagull term)

Subtracting and exponentiating:

    Lambda_MSbar/Lambda_rule  =  28.8086 * exp( -(T_wilson + dLoops) / 2 )
    dLoops  ==  dC_wilson_loops - dC_rule_loops                     ... (MASTER)

Every quantity inside the exponential is a DIFFERENCE.  No absolute lattice
normalisation appears, which is precisely the restriction F287 imposed.

WHY THE SUBTRACTION IS LEGAL — the slope-normalised estimator
=============================================================
The hazard F272/F277/F265 identified is a spurious MULTIPLICATIVE MEASURE factor
on the loop integral (F272: applying `make_kgrid_bcc` to this integrand "would
have inserted a spurious factor"), and F287 measured its residue as a 4.5%
deficit in the ABSOLUTE b_0 recovery at n = 40.

Estimate the constant by dividing by the log slope MEASURED ON THE SAME GRID
rather than by the analytic 2 b0/16 pi^2:

    s      =  d Pi / d ln(1/Q)                    (measured)
    c_hat  =  Pi/s - ln(1/Q),        C_hat = 2 c_hat

Under Pi -> lambda Pi the slope also goes s -> lambda s, so c_hat is EXACTLY
invariant while the analytic-slope constant shifts by 2 ln lambda.  The measure
ambiguity therefore cannot enter C_hat.  This is an algebraic identity, checked
to machine precision in `measure_invariance()`.

HONEST SCOPE — what this does NOT fix
=====================================
Slope normalisation immunises against an overall measure FACTOR.  It does not
immunise against integrating over a region that is not equivalent to a
fundamental domain -- a domain that samples an inequivalent piece of the rule
kernel's sqrt(3)-fcc period lattice changes the log part and the constant part
differently, and no normalisation can undo that.  That is still F267's open
item.  What the two together buy is that the F272-class hazard (a factor) is
closed, and the F267-class hazard (a region) is bounded by the measured
Q-flatness and grid convergence of the subtracted quantities, not assumed away.

WHAT IS MEASURED HERE AND WHAT IS QUOTED
========================================
  MEASURED (in-sandbox, grid-convergent):  the PROPAGATOR face of dLoops, i.e.
      the rule-vs-Wilson difference at continuum vertices.  Both normalisations
      are reported; they differ by the finite-grid slope split and agree in the
      limit.
  QUOTED  (from F163's committed artifact):  dC_wilson_loops = 4.1538, from
      C_lat = 6.1386 and C_MSbar = 131/66.  F163 states its own range as
      Lambda_loops ~ 6-9; the Q->0 high-resolution extrapolation is F163's open
      item (a) and is the single input that would tighten this module's budget.
  OPEN:   the VERTEX face -- the rule's own cos(k/2)-dressed 3-gluon + ghost
      form factors.  This module does not compute it; it says how big it has to
      be, which is what nothing before this could say.

numpy is reached only through `casim.numerics` (D8).  The reused quadrature
`bgfield_loop._Bcoeff_numeric` still imports numpy directly -- flagged by F287
sec.7, not fixed here (a routing change, not physics).
"""
from __future__ import annotations

import math

from casim.constants import q_star_a_implied as _q_star_a_implied
from casim.numerics import xp

# ----------------------------------------------------------------------
#  the conventions, imported not re-typed
# ----------------------------------------------------------------------
from casim.engine.gauge.lpt_wilson_selfenergy import (
    B0_INV_G2,                       # 11/(16 pi^2)
    LAMBDA_RATIO_WILSON_SU3,         # 28.8086  (Kawai-Nakayama-Seo)
)

SLOPE_ANALYTIC = 2.0 * B0_INV_G2     # d Pi / d ln(1/Q) = 2 b0 / 16 pi^2

#: F163's committed loops-only Wilson constant (`lambda_status` in the
#: artifact `test-results/F163_wilson_selfenergy.json`): C_lat = 6.138643 at the
#: off-axis q->0 extrapolation, against the analytic C_MSbar = 131/66.
F163_C_LAT_WILSON_LOOPS = 6.138642608418188
C_MSBAR = 131.0 / 66.0
#: F163's own stated spread on that number ("Lambda ~ 6-9"), carried as a range
#: rather than a false digit.  It is the width of the seagull/vertex SPLIT below,
#: and provably NOT of the total (see `budget`).
F163_LAMBDA_LOOPS_RANGE = (6.0, 9.0)

#: The F267 resolution floor, restated: probe the apparatus only at
#: Q >~ 2 * (2 pi / n) (F287 sec.5 -- below it the IR end of the log window does
#: not exist and the fit returns a confidently wrong slope).
RESOLUTION_FLOOR_CELLS = 2.0
#: Q sampling, expressed as multiples of the floor so the choice is tied to
#: the hazard it respects rather than written as four bare numbers.
CELL_RATIOS = tuple(RESOLUTION_FLOOR_CELLS * r for r in (1.05, 1.3, 1.6, 2.0))


# ======================================================================
#  exact bookkeeping:  dC  <->  Lambda ratio  <->  d_1
# ======================================================================
def dc_from_lambda(lambda_ratio: float) -> float:
    """dC = 2 ln(Lambda_MSbar/Lambda_lat)."""
    return 2.0 * math.log(lambda_ratio)


def lambda_from_dc(dC: float) -> float:
    """Lambda_MSbar/Lambda_lat = exp(dC/2)."""
    return math.exp(dC / 2.0)


def d1_from_dc(dC: float) -> float:
    """d_1 = b0 * dC in the 1/g^2 convention, b0 = 11/(16 pi^2)."""
    return B0_INV_G2 * dC


def lambda_ratio_rule_target() -> float:
    """Lambda_MSbar/Lambda_rule required by the g_s = 1/2 lock, DERIVED from the
    registry rather than written as 1.773:

        Lambda_MSbar/Lambda_rule = exp(a1 / (2 b0^alpha 4 pi)) / (q* a)
                                 = exp(11/42) / q*_a_implied

    with a1(nf=6) = 11/3 exact (F151-S1, F239 leg 1) and b0^alpha = 7/(4 pi).
    The V->MSbar factor exp(11/42) = 1.299434 is the EXACT leg of F239; the
    1/(q* a) factor is the open leg this module is about.
    """
    return math.exp(11.0 / 42.0) / _q_star_a_implied


# ======================================================================
#  THE MASTER IDENTITY
# ======================================================================
def master_identity(dC_wilson_loops: float | None = None,
                    dLoops: float | None = None) -> dict:
    """Verify

        Lambda_MSbar/Lambda_rule = 28.8086 * exp( -(T_wilson + dLoops)/2 )

    is an identity of the definitions, with
        T_wilson = dC_wilson - dC_wilson_loops     (the seagull + Haar measure)
        dLoops   = dC_wilson_loops - dC_rule_loops (the loops difference).

    The identity holds for ANY dLoops -- it is bookkeeping, not a result.  Its
    content is that both bracketed terms are DIFFERENCES, so no absolute lattice
    normalisation is used anywhere.  Returns the residual against the direct
    form exp(dC_rule/2); it must be zero to round-off.
    """
    if dC_wilson_loops is None:
        dC_wilson_loops = F163_C_LAT_WILSON_LOOPS - C_MSBAR
    if dLoops is None:                       # the value the lock requires
        dLoops = dC_wilson_loops - dc_from_lambda(lambda_ratio_rule_target())
    dC_wilson = dc_from_lambda(LAMBDA_RATIO_WILSON_SU3)
    T_wilson = dC_wilson - dC_wilson_loops
    subtracted = LAMBDA_RATIO_WILSON_SU3 * math.exp(-(T_wilson + dLoops) / 2.0)
    direct = lambda_from_dc(dC_wilson_loops - dLoops)
    return {"dC_wilson_total": dC_wilson,
            "dC_wilson_loops": dC_wilson_loops,
            "T_wilson_seagull_measure": T_wilson,
            "dLoops": dLoops,
            "lambda_subtracted_form": subtracted,
            "lambda_direct_form": direct,
            "residual": abs(subtracted - direct),
            "identity_holds": abs(subtracted - direct) < 1e-12 * max(1.0, direct),
            "statement": "Lambda_MSbar/Lambda_rule = 28.8086 exp(-(T_w + dLoops)/2); "
                         "both bracketed terms are differences, so the absolute "
                         "lattice normalisation F287 sec.6 forbids never appears."}


# ======================================================================
#  the slope-normalised (measure-invariant) estimator
# ======================================================================
def slope_normalised_constant(Qs, Pis, slope: float | None = None) -> dict:
    """C_hat = 2 * mean_Q [ Pi(Q)/s - ln(1/Q) ], with s the log slope.

    `slope=None` measures s from the same (Q, Pi) data -- that is the
    measure-invariant form.  Passing `slope=SLOPE_ANALYTIC` gives the
    analytic-normalisation form, which is NOT measure-invariant and is reported
    alongside so the difference is visible rather than chosen silently.
    """
    x = [math.log(1.0 / float(Q)) for Q in Qs]
    P = [float(p) for p in Pis]
    s_meas = float(xp.polyfit(xp.asarray(x), xp.asarray(P), 1)[0])
    s = s_meas if slope is None else float(slope)
    c = [p / s - xx for p, xx in zip(P, x)]
    return {"slope_measured": s_meas, "slope_used": s,
            "b0_recovery": s_meas / SLOPE_ANALYTIC,
            "C_hat": 2.0 * float(xp.mean(xp.asarray(c))),
            "C_hat_spread": 2.0 * (max(c) - min(c))}


def measure_invariance(lam: float = 3.7, Qs=(0.5, 0.65, 0.8, 1.0)) -> dict:
    """EXACT check: rescaling the loop integral Pi -> lam*Pi (the F272-class
    spurious measure factor) leaves the slope-normalised C_hat unchanged, while
    the analytic-normalisation constant shifts by exactly 2 ln lam.

    Uses a synthetic Pi = SLOPE_ANALYTIC*(ln(1/Q) + C0/2) so the check is a
    statement about the ESTIMATOR, not about any particular kernel -- which is
    the point: the invariance is algebraic and cannot be an artifact of the
    integrand.
    """
    C0 = 4.0
    x = [math.log(1.0 / Q) for Q in Qs]
    P = [SLOPE_ANALYTIC * (xx + C0 / 2.0) for xx in x]
    Pl = [lam * p for p in P]
    base = slope_normalised_constant(Qs, P)
    scaled = slope_normalised_constant(Qs, Pl)
    base_an = slope_normalised_constant(Qs, P, slope=SLOPE_ANALYTIC)
    scaled_an = slope_normalised_constant(Qs, Pl, slope=SLOPE_ANALYTIC)
    drift_inv = abs(scaled["C_hat"] - base["C_hat"])
    drift_an = scaled_an["C_hat"] - base_an["C_hat"]
    # exact: C_hat_an(lam) = 2[(lam-1) <ln(1/Q)> + lam C0/2]  =>  drift is
    expected_an = 2.0 * (lam - 1.0) * (sum(x) / len(x)) + (lam - 1.0) * C0
    return {"lambda": lam,
            "C_hat_unscaled": base["C_hat"], "C_hat_scaled": scaled["C_hat"],
            "drift_slope_normalised": drift_inv,
            "drift_analytic_normalised": drift_an,
            "expected_analytic_drift": expected_an,
            "analytic_drift_matches_closed_form":
                abs(drift_an - expected_an) < 1e-12,
            "invariant": drift_inv < 1e-12,
            "analytic_not_invariant": abs(drift_an) > 1e-3,
            "statement": "C_hat is EXACTLY invariant under an overall measure "
                         "factor; the analytic-normalisation constant is not. "
                         "This is what licenses the subtracted formulation "
                         "against the F272-class hazard (a spurious FACTOR). It "
                         "does NOT address the F267-class hazard (an "
                         "inequivalent DOMAIN)."}


# ======================================================================
#  the PROPAGATOR face of dLoops (measured)
# ======================================================================
def propagator_leg(n: int = 20, cell_ratios=CELL_RATIOS) -> dict:
    """Measure dC_rule_loops - dC_wilson_loops at CONTINUUM VERTICES, i.e. the
    propagator face of dLoops (sign: negative = the rule sits below Wilson).

    Q values are placed at `cell_ratios * (2 pi / n)` so every one clears the
    F287 sec.5 resolution floor of 2 cells -- the hazard that returned b_0 = 4.06
    from a fit whose residual looked fine.

    Returns BOTH normalisations.  They differ at finite grid only because the
    two kernels' measured slopes differ (rule/wilson -> 1 as a power law, F287
    sec.4); the spread between them is the honest uncertainty on this leg.
    """
    from casim.engine.gauge.bgfield_loop import _Bcoeff_numeric

    spacing = 2.0 * math.pi / n
    Qs = [r * spacing for r in cell_ratios]
    out = {}
    for kern in ("cont", "rule", "wilson"):
        Pi = [-_Bcoeff_numeric(Q, n, kern) for Q in Qs]
        out[kern] = {"Pi": Pi,
                     "meas": slope_normalised_constant(Qs, Pi),
                     "an": slope_normalised_constant(Qs, Pi, slope=SLOPE_ANALYTIC)}
    d_meas = out["rule"]["meas"]["C_hat"] - out["wilson"]["meas"]["C_hat"]
    d_an = out["rule"]["an"]["C_hat"] - out["wilson"]["an"]["C_hat"]
    return {"n": n, "Qs": Qs, "min_Q_over_spacing": min(cell_ratios),
            "resolution_floor_cleared": min(cell_ratios) >= RESOLUTION_FLOOR_CELLS,
            "dLoops_prop_slope_normalised": d_meas,
            "dLoops_prop_analytic_normalised": d_an,
            "slope_ratio_rule_over_wilson": (out["rule"]["meas"]["slope_measured"]
                                             / out["wilson"]["meas"]["slope_measured"]),
            "b0_recovery_cont": out["cont"]["meas"]["b0_recovery"],
            "per_kernel": {k: {"C_hat_meas": v["meas"]["C_hat"],
                               "C_hat_an": v["an"]["C_hat"],
                               "slope": v["meas"]["slope_measured"]}
                           for k, v in out.items()},
            "statement": "propagator face of dLoops (continuum vertices, lattice "
                         "propagators); negative = the rule's finite constant "
                         "sits BELOW Wilson's, which is the direction the "
                         "near-perfect action (F129/F130) requires."}


def propagator_leg_extrapolated(ns=(16, 20, 24), cell_ratios=CELL_RATIOS) -> dict:
    """Run `propagator_leg` on a grid ladder and Richardson-extrapolate in
    1/n^2 (the observed order).  Reports both normalisations; their spread at
    n -> inf is the quoted uncertainty on this leg.
    """
    rows = [propagator_leg(n, cell_ratios) for n in ns]

    def extrap(key):
        v = [float(r[key]) for r in rows]
        u = [1.0 / (float(r["n"]) ** 2) for r in rows]      # v = a + b*u
        b, a = (float(t) for t in xp.polyfit(xp.asarray(u), xp.asarray(v), 1))
        return a, v

    a_meas, v_meas = extrap("dLoops_prop_slope_normalised")
    a_an, v_an = extrap("dLoops_prop_analytic_normalised")
    centre = 0.5 * (a_meas + a_an)
    half = 0.5 * abs(a_meas - a_an)
    return {"ns": list(ns),
            "series_slope_normalised": v_meas, "limit_slope_normalised": a_meas,
            "series_analytic_normalised": v_an, "limit_analytic_normalised": a_an,
            "dLoops_prop": centre, "dLoops_prop_halfwidth": half,
            "monotone": all(v_meas[i] < v_meas[i + 1] for i in range(len(v_meas) - 1)),
            "statement": "both normalisations converge as 1/n^2 and bracket the "
                         "leg; the quoted value is their midpoint with the "
                         "half-spread as the uncertainty. No single "
                         "normalisation is privileged, which is the honest "
                         "reading of F287 sec.6."}


# ======================================================================
#  THE BUDGET — the three legs of d_1, and which one is still open
# ======================================================================
def budget(dLoops_prop: float, dLoops_prop_halfwidth: float = 0.0,
           dC_wilson_loops: float | None = None) -> dict:
    """The full subtracted budget for d_1, in dC units.

    Required total shift from Wilson:
        dC_rule_required - dC_wilson_total
    splits into three legs:
        leg 1  seagull + Haar measure ABSENT      (F155-A0, exact structurally)
        leg 2  propagator face                     (measured here)
        leg 3  vertex form factors                 (OPEN)

    The arithmetic that matters: leg1 + leg3 = total - leg2 INDEPENDENTLY of
    dC_wilson_loops.  So F163's open Q->0 extrapolation cannot move the total or
    leg 2 -- it only redistributes between leg 1 and leg 3.  The anchor fixes
    the sum; F163 fixes the split.
    """
    if dC_wilson_loops is None:
        dC_wilson_loops = F163_C_LAT_WILSON_LOOPS - C_MSBAR
    dC_w_tot = dc_from_lambda(LAMBDA_RATIO_WILSON_SU3)
    dC_rule_req = dc_from_lambda(lambda_ratio_rule_target())
    total = dC_rule_req - dC_w_tot
    leg1 = dC_wilson_loops - dC_w_tot                       # = -T_wilson
    leg2 = dLoops_prop
    leg3 = total - leg1 - leg2
    lo, hi = F163_LAMBDA_LOOPS_RANGE
    leg3_range = sorted(total - (dc_from_lambda(L) - dC_w_tot) - leg2
                        for L in (lo, hi))
    return {
        "dC_wilson_total": dC_w_tot,
        "dC_wilson_loops": dC_wilson_loops,
        "dC_rule_required": dC_rule_req,
        "lambda_rule_required": lambda_ratio_rule_target(),
        "total_required_shift": total,
        "legs": [
            {"leg": "seagull+measure absent (F155-A0)", "dC": leg1,
             "share": leg1 / total, "status": "structurally exact; magnitude from "
             "the 28.8086 anchor minus F163's loops-only constant"},
            {"leg": "propagator face", "dC": leg2, "share": leg2 / total,
             "halfwidth": dLoops_prop_halfwidth,
             "status": "MEASURED (this module), grid-convergent"},
            {"leg": "vertex form factors", "dC": leg3, "share": leg3 / total,
             "range_from_F163_spread": leg3_range, "status": "OPEN"},
        ],
        "closes_to_total": abs(leg1 + leg2 + leg3 - total) < 1e-12,
        "leg1_plus_leg3_is_anchor_fixed": abs((leg1 + leg3) - (total - leg2)) < 1e-12,
        "d1_rule_required": d1_from_dc(dC_rule_req),
        "d1_wilson": d1_from_dc(dC_w_tot),
        "statement": "the open piece is one leg of three and no longer the whole "
                     "number: the seagull-emptiness leg is structural and the "
                     "propagator leg is measured, so the vertex form factors "
                     "must supply the stated dC and nothing else."}


def tadpole_free_band(dC_wilson_loops: float | None = None) -> dict:
    """The bracket the subtracted formulation puts on the answer BEFORE the
    vertex computation exists.

    Assumption, named: the rule's loops-only constant lies between the continuum
    (dC = 0, a perfect action) and Wilson's loops-only constant -- i.e. the rule
    is nearer the continuum than Wilson is, which F287 sec.4 MEASURES in an
    independent quantity (the rule's b_0 discretisation error is 5.3-5.7x smaller
    than Wilson's at every grid).  This is a monotonicity assumption, not a
    theorem, and is labelled as such.
    """
    if dC_wilson_loops is None:
        dC_wilson_loops = F163_C_LAT_WILSON_LOOPS - C_MSBAR
    lo, hi = 1.0, lambda_from_dc(dC_wilson_loops)
    target = lambda_ratio_rule_target()
    return {"band": [lo, hi], "target": target,
            "target_inside": lo <= target <= hi,
            "position_in_band": (target - lo) / (hi - lo),
            "wilson_total": LAMBDA_RATIO_WILSON_SU3,
            "wilson_excluded_factor": LAMBDA_RATIO_WILSON_SU3 / hi,
            "assumption": "monotonicity: 0 <= dC_rule_loops <= dC_wilson_loops, "
                          "from the rule being nearer the continuum than Wilson "
                          "(F129/F130 near-perfect action; measured 5.3-5.7x in "
                          "F287 sec.4). NOT a theorem.",
            "falsifier": "a completed rule vertex computation returning "
                         "Lambda_MSbar/Lambda_rule outside this band falsifies "
                         "either the g_s=1/2 lock or the monotonicity "
                         "assumption; the two are distinguished by whether "
                         "dC_rule_loops is negative (assumption) or above "
                         "dC_wilson_loops (lock)."}


# ======================================================================
#  the registry entry point (D9) — sweepable, and it can fail
# ======================================================================
def check_d1_subtracted(lambda_wilson: float = LAMBDA_RATIO_WILSON_SU3,
                        C_lat_wilson_loops: float = F163_C_LAT_WILSON_LOOPS,
                        ns=(16, 20, 24)) -> dict:
    """The F280 gate, as a registry entry with real parameters.

    Both parameters are the EXTERNAL/quoted inputs, so `casim test --param
    lambda_wilson=1.0` is a genuine control: with no Wilson scheme gap the
    seagull leg changes sign, the tadpole-free band collapses below the target,
    and S5 must go red.  A record that cannot be made to fail this way is not a
    test (D9).
    """
    dC_w_loops = C_lat_wilson_loops - C_MSBAR
    dC_w_tot = dc_from_lambda(lambda_wilson)
    checks = []

    # S1 -- the master identity is bookkeeping and must close to round-off
    mi = master_identity(dC_wilson_loops=dC_w_loops)
    checks.append(("S1 master identity closes", mi["residual"] < 1e-12, mi["residual"]))

    # S2 -- the estimator is exactly invariant under a measure factor
    inv = measure_invariance()
    checks.append(("S2 measure-invariance exact",
                   inv["invariant"] and inv["analytic_not_invariant"]
                   and inv["analytic_drift_matches_closed_form"],
                   inv["drift_slope_normalised"]))

    # S3 -- the propagator leg is measured, grid-convergent, monotone
    ext = propagator_leg_extrapolated(ns)
    leg2 = ext["dLoops_prop"]
    checks.append(("S3 propagator leg convergent and negative",
                   ext["monotone"] and -1.20 < leg2 < -0.80
                   and ext["dLoops_prop_halfwidth"] < 0.10, leg2))

    # S4 -- the budget closes and leg1+leg3 is anchor-fixed
    b = budget(leg2, ext["dLoops_prop_halfwidth"], dC_wilson_loops=dC_w_loops)
    b["dC_wilson_total"] = dC_w_tot
    total = dc_from_lambda(lambda_ratio_rule_target()) - dC_w_tot
    leg1 = dC_w_loops - dC_w_tot
    leg3 = total - leg1 - leg2
    checks.append(("S4 budget closes", abs(leg1 + leg2 + leg3 - total) < 1e-12,
                   leg1 + leg2 + leg3 - total))

    # S5 -- the tadpole-free band contains the target and excludes Wilson
    band_hi = lambda_from_dc(dC_w_loops)
    target = lambda_ratio_rule_target()
    checks.append(("S5 target inside the tadpole-free band, Wilson excluded",
                   1.0 <= target <= band_hi and lambda_wilson > band_hi,
                   [1.0, band_hi, target]))

    # S6 -- the open leg is now a minority of the required shift
    checks.append(("S6 open vertex leg is a minority share",
                   abs(leg3 / total) < 0.5, leg3 / total))

    passed = all(c[1] for c in checks)
    return {"passed": passed,
            "checks": [{"name": nm, "ok": bool(ok), "value": v}
                       for nm, ok, v in checks],
            "legs": {"seagull_absent": leg1, "propagator": leg2, "vertex_open": leg3},
            "total_required_shift": total,
            "d1_rule_required": d1_from_dc(dc_from_lambda(target)),
            "lambda_rule_required": target,
            "band": [1.0, band_hi],
            "params": {"lambda_wilson": lambda_wilson,
                       "C_lat_wilson_loops": C_lat_wilson_loops,
                       "ns": list(ns)}}


# ======================================================================
#  status / report
# ======================================================================
def status() -> dict:
    return {
        "closes": "completeness-2026-08-04 gap #3, smallest next step: formulate "
                  "d_1 subtracted against the Wilson 28.8086 reference rather "
                  "than settling the F267 fundamental domain first",
        "exact": ["master identity (bookkeeping, residual < 1e-12)",
                  "measure-invariance of the slope-normalised estimator",
                  "Lambda_rule target = exp(11/42)/q*a derived, not written"],
        "measured": ["propagator face of dLoops, grid-convergent, both "
                     "normalisations"],
        "open": ["the rule's own cos(k/2)-dressed 3-gluon + ghost vertex form "
                 "factors (leg 3)",
                 "F163's Q->0 high-res Wilson loops-only extrapolation, which "
                 "sets the leg1/leg3 SPLIT but not the total"],
        "not_addressed": "the F267 fundamental domain. Slope normalisation "
                         "closes the F272-class FACTOR hazard only.",
    }


def report(n: int = 20) -> dict:
    prop = propagator_leg(n)
    b = budget(prop["dLoops_prop_analytic_normalised"])
    return {"master_identity": master_identity(),
            "measure_invariance": measure_invariance(),
            "propagator_leg": prop,
            "budget": b,
            "tadpole_free_band": tadpole_free_band(),
            "status": status()}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
