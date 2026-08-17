"""F286 — What could supply the 3.5% spectral tilt on a rigid lattice?

Seven checks. T1 is exact-algebraic and is re-derived here with sympy
INDEPENDENTLY of the module; T5 is a pre-registered frequentist count whose
conclusion the test asserts in BOTH directions (see check_T5).

  T1a (exact)  For n_s - 1 = F(k xi), dn_s/dlnk = x F'(x), so the observed
      ratio bounds |dlnF/dlnx| < 0.32. A power law gives exactly p; a log
      gives 1/L. Re-derived symbolically.

  T1b (structural)  A length enters at integer power (p >= 1, and p = 2 for
      the leading lattice correction), so EVERY length scale is excluded by
      shape. The log route at 1/L = 0.0075 survives.

  T2  (computed)  The whole log class predicts dn_s/dlnk = -(1-n_s)/L with
      L from F285, and it must be consistent with Planck but NOT yet testable.

  T3  (computed)  C = (1-n_s) L is O(1) — the tilt is not unnaturally small.

  T4  (structural)  No coupling in the inventory works, and G's failure is
      DOWNSTREAM of F284's own Gdot/G = 0 prediction.

  T5  (statistical)  The look-elsewhere count. Asserts the family is large,
      that MORE THAN ONE expression hits the window, and that the resulting
      p-value is unremarkable — i.e. it asserts the coincidence is REJECTED.
      Also asserts the identity delta*/(2pi) == 1/(9 pi) holds exactly, so a
      future reader cannot mistake the rejection for an arithmetic error.

  T6  (consistency)  F286 reuses F285's decade count and F284's rigidity
      rather than reintroducing either.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.constants import delta_star_f
from casim.engine.interactions import cosmology_initial_conditions as ic
from casim.engine.interactions import cosmology_second_scale as ss


def check_T1a_classification_exact():
    """|dlnF/dlnx| = p for a power law, 1/L for a log — from scratch."""
    x, p, C, L = sp.symbols("x p C L", positive=True)
    F = C * x ** p
    assert sp.simplify(x * sp.diff(F, x) / F - p) == 0
    Flog = C / L
    assert sp.simplify(L * sp.diff(Flog, L) / Flog + 1) == 0

    got = ss.classification_theorem()
    assert got["power_law_log_derivative"] == "p"
    return got


def check_T1b_lengths_excluded():
    got = ss.classification_theorem()
    b = got["observed_bound_on_log_derivative"]
    assert 0.25 < b < 0.40                       # the Planck-derived bound
    # a length enters at integer power; the leading lattice term is p = 2
    assert got["leading_lattice_correction_p"] == 2
    assert got["length_scales_excluded"] is True
    # the log route survives, and by a wide margin
    assert got["log_type_allowed"] is True
    assert got["log_type_value"] < b / 10.0
    return got


def check_T2_class_prediction():
    got = ss.running_prediction()
    assert abs(got["dns_dlnk_predicted"] + 2.62e-4) < 5e-6
    # consistent with Planck, but far from testable today
    assert got["consistent_with_planck"] is True
    assert got["testable_today"] is False
    assert got["sigma_below_current_error"] > 20.0
    # L is F285's number, not a new input
    assert abs(got["decades"] - ic.required_non_genericity()["decades_below_BZ"]) < 1e-9
    return got


def check_T3_coefficient_is_natural():
    got = ss.required_coefficient()
    assert got["is_order_unity"] is True
    assert 4.0 < got["C"] < 6.0
    # the point: the tilt is NOT a fine-tuning problem
    assert got["C"] > 1.0
    return got


def check_T4_no_coupling_works():
    got = ss.coupling_inventory()
    assert got["any_candidate_works"] is False
    assert got["alpha_em"]["shortfall_factor"] > 10.0
    assert got["alpha_s"]["decades_below_Lambda_QCD"] > 30.0
    # G's failure is downstream of F284's own prediction, not an assumption
    assert got["G"]["runs"] is False
    assert got["G"]["Gdot_over_G"] == 0.0
    assert got["blockspin"]["tilt_is_marginal"] is True
    return got


def check_T5_coincidence_rejected():
    """The look-elsewhere count REJECTS the near-miss. Asserted both ways."""
    got = ss.coincidence_look_elsewhere()
    # the arithmetic identity is exact — the rejection is not a slip
    assert got["equals_one_over_9pi"] is True
    assert abs(delta_star_f / (2 * math.pi) - 1.0 / (9 * math.pi)) < 1e-15
    # the family is large and was fixed before looking
    assert got["candidates"] > 300
    # MORE THAN ONE hit => being closest is unremarkable
    assert got["distinct_hits"] > 1
    assert got["survives_look_elsewhere"] is False
    # and the p-value is nowhere near significant
    assert got["p_at_least_one_by_chance"] > 0.05
    # sanity: the best hit really is the delta*/2pi one, and really is close
    assert abs(got["best"]["sigma"]) < 0.2
    return got


def check_T6_consistent_with_F284_F285():
    ss_L = ss.running_prediction()["decades"]
    ic_L = ic.required_non_genericity()["decades_below_BZ"]
    assert abs(ss_L - ic_L) < 1e-9
    # F285's marginality is what rules block-spin out here — same claim, once
    assert ic.blockspin_tilt_marginality()["exponent_is_marginal"] is True
    assert ss.coupling_inventory()["blockspin"]["tilt_is_marginal"] is True
    return {"L_decades": ss_L, "single_source_of_truth": True}


CHECKS = (
    ("T1a_classification_exact", check_T1a_classification_exact),
    ("T1b_lengths_excluded", check_T1b_lengths_excluded),
    ("T2_class_prediction", check_T2_class_prediction),
    ("T3_coefficient_is_natural", check_T3_coefficient_is_natural),
    ("T4_no_coupling_works", check_T4_no_coupling_works),
    ("T5_coincidence_rejected", check_T5_coincidence_rejected),
    ("T6_consistent_with_F284_F285", check_T6_consistent_with_F284_F285),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "a second scale must be a log, not a length; the class predicts "
        "dn_s/dlnk = -2.6e-4; the coefficient is a natural O(1); no model "
        "coupling supplies the log; the delta*/(2pi) coincidence is rejected"
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
