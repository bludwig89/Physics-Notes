"""F296 — Holographic cosmology names the operator and validates F286 T1.

Seven checks. L2 is the load-bearing one: it tests OUR instrument (F286 T1)
against an INDEPENDENT published case, so it is asserted against F286's live
bound rather than a copied constant.

  L1  (structural)  The framework exists, has no inflaton, and computes the
      spectrum from <TT>. Recorded so the placement cannot silently drift.

  L2a (computed)  T1's diagnostic on HC's own fitted spectrum is 0.675 —
      over T1's LIVE bound by ~2.1x. Asserted against F286's module, not a
      hard-coded 0.32, so the two findings cannot diverge.

  L2b (computed)  The implied running is +0.015, ~2.9 sigma from Planck, the
      same sign and size as the published 2.2 sigma global disfavour.

  L3  (structural)  HC's branch has a dimensionful coupling (p = -1); the
      model's constant-gamma needs p = 0, the f1 = 0 conformal branch the PRL
      footnotes as unanalysed.

  L4  (structural)  The named operator, and gamma = (1-n_s)/2 consistent with
      F295's own number.

  L5a (computed)  The model's field content read as the dual gives r = 0.32
      (conformal) to 0.97 (minimal), both EXCLUDED by BK18's r < 0.036.

  L5b (discipline)  Guard: this finding must not claim the model IS
      holographic. Asserts the naive reading is flagged excluded and that the
      operator identification carries its caveat.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

from casim.engine.interactions import cosmology_anomalous_dimension as ad
from casim.engine.interactions import cosmology_holographic as hc
from casim.engine.interactions import cosmology_second_scale as ss


def check_L1_framework_recorded():
    got = hc.run()["L1_framework"]
    assert got["no_inflaton"] is True
    assert "stress-tensor trace" in got["spectrum_from"]
    assert got["fitted_to_planck"] is True
    assert got["global_disfavour_sigma"] == 2.2
    return got


def check_L2a_t1_flags_hc():
    """T1's diagnostic on HC, against F286's LIVE bound."""
    got = hc.t1_retrodiction()
    live_bound = ss.classification_theorem()["observed_bound_on_log_derivative"]
    # the finding must use F286's own bound, not a copy that could drift
    assert abs(got["t1_bound"] - live_bound) < 0.01, (got["t1_bound"], live_bound)
    assert got["hc_coupling_is_dimensionful"] is True
    assert got["hc_power_p_nominal"] == -1
    # the retrodiction itself
    assert 0.6 < got["hc_log_derivative"] < 0.75
    assert got["hc_log_derivative"] > live_bound
    assert 1.8 < got["over_bound_factor"] < 2.5
    assert got["t1_flags_hc"] is True
    return got


def check_L2b_running_tension_matches_published():
    got = hc.t1_retrodiction()
    # same SIGN as HC's known problem and the right size
    assert got["hc_implied_dns_dlnk"] > 0.0
    assert 0.01 < got["hc_implied_dns_dlnk"] < 0.02
    assert 2.0 < got["tension_sigma"] < 4.0
    # and it brackets the published global disfavour rather than replacing it
    assert got["published_global_disfavour_sigma"] == 2.2
    assert got["retrodiction_agrees"] is True
    return got


def check_L3_branch_is_unanalysed():
    got = hc.branch_identification()
    assert got["hc_tilt_shape_p"] == -1
    assert got["model_tilt_shape_p"] == 0
    assert got["literature_analyses_model_branch"] is False
    assert "f1 = 0" in got["prl_footnote"] or "f1 != 0" in got["prl_footnote"]
    # the model's p = 0 is F295's branch
    assert ad.anomalous_dimension_branch()["p_zero_is_trivial"] is False
    return got


def check_L4_operator_named():
    got = hc.named_operator()
    assert "stress tensor" in got["operator"]
    assert got["answers_F295_open_question"] is True
    # gamma must agree with F295's own number
    assert abs(got["gamma_required"]
               - ad.anomalous_dimension_branch()["gamma_from_data"]) < 1e-15
    # and it must carry its caveat
    assert "does not establish" in got["caveat"]
    return got


def check_L5a_model_content_excluded_by_r():
    got = hc.tensor_ratio_from_model_content()
    assert got["n_weyl_fermions"] == 48
    assert got["n_real_scalars"] == 2
    for case in got["cases"].values():
        assert case["excluded"] is True
        assert case["r"] > got["r_BK18_bound"]
        assert case["over_BK18_factor"] > 5.0
    # conformal is the most generous case and still fails by ~9x
    assert 8.0 < got["cases"]["conformal"]["over_BK18_factor"] < 10.0
    assert 25.0 < got["cases"]["minimal"]["over_BK18_factor"] < 29.0
    # and the scalar count needed is far beyond the model's
    assert got["n_phi_needed_for_bound"] > 700.0
    assert got["shortfall_factor"] > 300.0
    return got


def check_L5b_does_not_claim_the_model_is_holographic():
    """Guard: placement is not a claim of duality."""
    got = hc.tensor_ratio_from_model_content()
    assert got["naive_holographic_reading_excluded"] is True
    op = hc.named_operator()
    assert op["caveat"]                       # the identification is caveated
    # the verdict must carry the exclusion, not bury it
    assert "EXCLUDED" in hc.run()["verdict"]
    return {"claims_duality": False, "naive_reading_excluded": True}


CHECKS = (
    ("L1_framework_recorded", check_L1_framework_recorded),
    ("L2a_t1_flags_hc", check_L2a_t1_flags_hc),
    ("L2b_running_tension", check_L2b_running_tension_matches_published),
    ("L3_branch_unanalysed", check_L3_branch_is_unanalysed),
    ("L4_operator_named", check_L4_operator_named),
    ("L5a_r_excludes_model_content", check_L5a_model_content_excluded_by_r),
    ("L5b_no_duality_claim", check_L5b_does_not_claim_the_model_is_holographic),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "F286 T1 validated by retrodicting holographic cosmology's published "
        "tension; the operator is named; the model's branch is unanalysed; the "
        "naive field-content reading is excluded by r"
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
