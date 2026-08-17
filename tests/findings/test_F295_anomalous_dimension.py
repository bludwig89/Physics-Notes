"""F295 — The tilt is an anomalous dimension, not a second scale.

Eight checks. A1 is exact-algebraic and re-derived here with sympy
INDEPENDENTLY of the module; it is the correction to F286's framing and so is
the load-bearing one.

  A1a (exact)  A constant anomalous dimension gamma gives Delta^2 ~ k^(-2gamma),
      whose log-slope is -2gamma and whose SECOND log-derivative — the running —
      is identically zero. So dn_s/dlnk = 0 EXACTLY, with no second scale.

  A1b (exact)  p = 0 lies inside F286 T1's own allowed band |p| < 0.32, so this
      is a correction to F286's READING, not to its algebra. Asserted against
      F286's live number so the two findings cannot drift apart.

  A2  (computed)  The two sub-classes are distinguishable: constant-gamma gives
      0, F286's log class gives -2.62e-4. Both consistent with Planck today.

  A3a (computed)  Freeing alpha does not help: reaching alpha = g_eff needs a
      scale ~68 decades ABOVE the model's own lattice cutoff.

  A3b (exact+computed)  Freeing G does not help: its coupling is a POWER (p=2),
      excluded by T1 on shape, and 115 decades short on magnitude.

  A4a (structural)  Three registered constants equal 2/9, and they are separate
      constants by decree — a mechanism must PICK one.

  A4b (discipline)  The finding must NOT claim the value is significant. This
      check asserts the module still defers to F286's look-elsewhere count and
      still flags itself as not-a-derivation. It exists so a later edit cannot
      quietly promote the coincidence.

  A5  (consistency)  gamma_required = (1-n_s)/2, and g_eff = 2 pi (1-n_s), are
      mutually consistent and match F286's tilt.

Real arithmetic only (CLAUDE.md).
"""
from __future__ import annotations

import math

import sympy as sp

from casim.constants import c_fierz_colour, delta_star_f, sin2_thetaW_onshell
from casim.engine.interactions import cosmology_anomalous_dimension as ad
from casim.engine.interactions import cosmology_second_scale as ss


def check_A1a_constant_gamma_has_zero_running():
    """Delta^2 ~ k^(-2 gamma) => running is identically 0, from scratch."""
    k, gamma, A = sp.symbols("k gamma A", positive=True)
    Delta2 = A * k ** (-2 * gamma)
    slope = sp.simplify(k * sp.diff(sp.log(Delta2), k))
    assert sp.simplify(slope + 2 * gamma) == 0            # n_s - 1 = -2 gamma
    running = sp.simplify(k * sp.diff(slope, k))
    assert running == 0                                    # literal zero

    got = ad.anomalous_dimension_branch()
    assert got["p_zero_is_trivial"] is False
    assert got["dns_dlnk_exact_zero"] is True
    assert got["needs_a_second_scale"] is False
    assert got["sits_on_F285_D3_fixed_line"] is True
    return got


def check_A1b_p_zero_is_inside_F286_band():
    """The correction is to F286's READING; its algebra is reused unchanged."""
    bound = ss.classification_theorem()["observed_bound_on_log_derivative"]
    assert 0.0 < bound                                     # p = 0 is inside
    assert abs(0.0) < bound
    # and F286's own power-law log-derivative is still exactly p
    assert ss.classification_theorem()["power_law_log_derivative"] == "p"
    return {"F286_bound": bound, "p_zero_allowed": True}


def check_A2_subclass_discriminator():
    got = ad.subclass_discriminator()
    assert got["constant_gamma_dns_dlnk"] == 0.0
    assert abs(got["log_class_dns_dlnk"] + 2.62e-4) < 5e-6
    assert got["both_consistent_today"] is True
    assert got["beyond_CMB_S4"] is True
    # the log class number must be F286's, not a re-derivation
    assert abs(got["log_class_dns_dlnk"]
               - ss.running_prediction()["dns_dlnk_predicted"]) < 1e-15
    return got


def check_A3a_alpha_does_not_help():
    got = ad.alpha_inverse_problem()
    assert got["excluded"] is True
    assert got["decades_above_cutoff"] > 50.0
    assert got["factor_required"] > 25.0
    # the cutoff it is measured against is the model's own (F282)
    assert 18.0 < got["log10_lattice_cutoff_GeV"] < 20.0
    return got


def check_A3b_gravity_does_not_help():
    got = ad.gravity_inverse_problem()
    # shape first: p = 2 vs T1's 0.32
    assert got["power_p"] == 2
    assert got["excluded_on_shape"] is True
    assert got["power_p"] > got["T1_bound_on_p"]
    # magnitude second, and only as a corroboration
    assert got["excluded_on_magnitude"] is True
    assert got["shortfall_decades"] > 100.0
    return got


def check_A4a_three_registered_two_ninths():
    two_ninths = 2.0 / 9.0
    assert abs(delta_star_f - two_ninths) < 1e-12
    assert abs(float(sin2_thetaW_onshell) - two_ninths) < 1e-12
    assert abs(float(c_fierz_colour) - two_ninths) < 1e-12
    got = ad.representation_weight_target()
    assert len(got["registered_constants_equal_to_2_9"]) == 3
    assert abs(got["deviation_sigma"]) < 0.2
    return got


def check_A4b_does_not_claim_significance():
    """Guard: this finding must NOT promote the coincidence. Asserted."""
    got = ad.representation_weight_target()
    assert got["still_not_a_derivation"] is True
    assert "look_elsewhere" in " ".join(got.keys())
    # F286's rejection must still stand and be reachable from here
    le = ss.coincidence_look_elsewhere()
    assert le["survives_look_elsewhere"] is False
    assert le["distinct_hits"] > 1
    assert le["p_at_least_one_by_chance"] > 0.05
    return {"significance_claimed": False, "F286_rejection_intact": True}


def check_A5_internal_consistency():
    tilt = 1.0 - ad.NS_OBS
    got_branch = ad.anomalous_dimension_branch()
    got_rep = ad.representation_weight_target()
    assert abs(got_branch["gamma_from_data"] - tilt / 2.0) < 1e-15
    assert abs(got_rep["g_eff"] - 2 * math.pi * tilt) < 1e-15
    # same tilt as F286
    assert abs(tilt - (1.0 - 0.9649)) < 1e-15
    return {"gamma": got_branch["gamma_from_data"], "g_eff": got_rep["g_eff"]}


CHECKS = (
    ("A1a_constant_gamma_zero_running", check_A1a_constant_gamma_has_zero_running),
    ("A1b_p_zero_inside_F286_band", check_A1b_p_zero_is_inside_F286_band),
    ("A2_subclass_discriminator", check_A2_subclass_discriminator),
    ("A3a_alpha_does_not_help", check_A3a_alpha_does_not_help),
    ("A3b_gravity_does_not_help", check_A3b_gravity_does_not_help),
    ("A4a_three_registered_two_ninths", check_A4a_three_registered_two_ninths),
    ("A4b_does_not_claim_significance", check_A4b_does_not_claim_significance),
    ("A5_internal_consistency", check_A5_internal_consistency),
)


def check_all():
    """Registry entry point. Returns the full result dict."""
    out = {name: fn() for name, fn in CHECKS}
    out["n_checks"] = len(CHECKS)
    out["verdict"] = (
        "freeing alpha/G does not help; the tilt is a scale-free anomalous "
        "dimension with dn_s/dlnk = 0 exactly; geometry supplies the right "
        "KIND of object but not a derivation"
    )
    return out


if __name__ == "__main__":                             # pragma: no cover
    import json
    print(json.dumps(check_all(), indent=2, sort_keys=True, default=str))
