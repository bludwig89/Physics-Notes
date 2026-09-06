"""F347 -- do the LITERATURE-FAVOURED mixed-generation-type Koide quark tuples carry
F175/F92's charged-lepton E_g/T_1u shape mechanism? (ledger row E6, direct follow-up to
F346's review, Attack 11 -- docs/reviews/F346-review-2026-09-02.md)

F346 tested only same-generation-type quark triplets (up-type u,c,t; down-type d,s,b)
and found a leaning no-go. But the literature has repeatedly proposed MIXED-generation
-type triplets instead: Harari, Haut & Weyers (1978, Phys. Lett. B 78, 459) on (u,d,s)
with a massless up quark; Rodejohann & Zhang (arXiv:1101.5525) extending the claim to
(c,b,t); Rivero (arXiv:1111.7232) proposing a THIRD, signed-square-root tuple (s,c,b)
that uses a different ansatz this module does not fit (noted, not tested).

This record re-checks (u,d,s) and (c,b,t) against CURRENT PDG 2024 masses -- not the
historical/assumed values those papers used -- first via the plain Koide Q, then via
the identical circulant-fit-vs-single-irrep-O_h-weight pipeline F346 already validated,
with the measurement-precision vs. range-based-look-elsewhere distinction built in
correctly from the start (F346's Attack 7 found and fixed a bug from conflating them;
this module never merges them to begin with).

  C1  (u,d,s)'s Koide Q is NOT close to 2/3 with current, nonzero-m_u PDG 2024 data
      (>10% off) -- the 1978 near-hit relied on a since-superseded m_u=0 assumption.
      (c,b,t)'s Koide Q IS close to 2/3 (<1%) -- Rodejohann-Zhang's claim still holds
      today. The algebraic identity Q = 1/3 + eta^2/6 (delta-independent) is checked
      exactly for both tuples -- Q says nothing about the phase F175's stronger claim
      also needs.
  C2  (c,b,t)'s fitted phase delta (mod 2*pi/3) is incompatible (>50 sigma, measurement
      precision) with every single-irrep O_h weight the same T_1u x T_1u decomposition
      offers.
  C3  that same phase proximity is NOT numerically unusual in absolute terms either
      (range-based look-elsewhere p > 5%) -- the Q~2/3 coincidence carries no
      accompanying phase/shape coincidence.
  C4  (c,b,t)'s eta^2 sits within ~0.8% of the lepton's derived eta^2=2 (F92) in
      relative terms, but PDG's precision on c,b,t is tight enough that this is a
      many-sigma EXCLUDED value at measurement precision -- "looks close" and "is
      close" are different claims here, same as F346's review had to separate for
      its down-type near-hit.
  C5  (u,d,s) fails both axes too (phase and amplitude), independent of its already-
      failed Q check -- not merely "Q is far."
  C6  lepton-sector self-check: the identical fitting code recovers F175's 2/9 and
      F92's sqrt(2) from the PDG lepton masses.
"""

import math

from casim.engine.particles import derive_quark_mixed_koide_probe as mod


# ---------------------------------------------------------------------------
# C1 -- Koide Q against the two literature claims, checked with current data
# ---------------------------------------------------------------------------

def test_C1_uds_Q_not_close_to_two_thirds_with_current_data():
    out = mod.c1_fit_both_tuples()
    assert out["uds_Q_vs_two_thirds_rel_diff"] > 0.10, out["uds_Q_vs_two_thirds_rel_diff"]
    assert abs(out["uds"]["Q"] - 0.5667) < 1e-3


def test_C1_cbt_Q_close_to_two_thirds_with_current_data():
    out = mod.c1_fit_both_tuples()
    assert out["cbt_Q_vs_two_thirds_rel_diff"] < 0.01, out["cbt_Q_vs_two_thirds_rel_diff"]
    assert abs(out["cbt"]["Q"] - 0.6692) < 1e-3


def test_C1_Q_equals_one_third_plus_eta2_over_six_exactly():
    out = mod.c1_fit_both_tuples()
    for name in ("uds", "cbt"):
        t = out[name]
        assert abs(t["Q"] - (1.0 / 3.0 + t["eta2"] / 6.0)) < 1e-9


def test_C1_circulant_fit_reconstructs_input_masses_exactly():
    out = mod.c1_fit_both_tuples()
    assert out["uds"]["max_reconstruction_residual"] < 1e-8
    assert out["cbt"]["max_reconstruction_residual"] < 1e-8


# ---------------------------------------------------------------------------
# C2/C3 -- cbt phase: decisively excluded by data, AND not numerically
# unusual in absolute terms -- both true at once, and both checked.
# ---------------------------------------------------------------------------

def test_C2_cbt_phase_decisively_excluded_from_every_weight():
    out = mod.c2_c3_phase_analysis()
    cbt = out["cbt"]
    assert cbt["nearest_sigma_measurement_precision"] > 50.0, cbt["nearest_sigma_measurement_precision"]
    for cname, d in cbt["distances"].items():
        assert d["abs_diff_rad"] > 0.02, (cname, d)


def test_C3_cbt_phase_not_numerically_unusual_in_absolute_terms():
    out = mod.c2_c3_phase_analysis()
    p = out["cbt"]["p_uniform_domain_lookelsewhere"]
    assert p > 0.05, p


def test_C3_uds_phase_also_not_numerically_unusual():
    out = mod.c2_c3_phase_analysis()
    p = out["uds"]["p_uniform_domain_lookelsewhere"]
    assert p > 0.05, p


# ---------------------------------------------------------------------------
# C4 -- the "close but excluded" duality for cbt's eta^2
# ---------------------------------------------------------------------------

def test_C4_cbt_eta2_close_in_percent_but_excluded_at_measurement_precision():
    out = mod.c4_cbt_eta2_vs_lepton()
    assert out["relative_diff"] < 0.02, out["relative_diff"]
    assert out["sigma_measurement_precision"] > 5.0, out["sigma_measurement_precision"]


# ---------------------------------------------------------------------------
# C5 -- uds fails independently of its Q mismatch
# ---------------------------------------------------------------------------

def test_C5_uds_amplitude_and_phase_both_far_from_lepton():
    c5 = mod.c5_uds_completeness_check()
    assert c5["eta2_diff_from_lepton_target"] > 0.3, c5["eta2_diff_from_lepton_target"]
    cc = mod.c2_c3_phase_analysis()
    assert cc["uds"]["nearest_sigma_measurement_precision"] > 5.0


# ---------------------------------------------------------------------------
# C6 -- method validation
# ---------------------------------------------------------------------------

def test_C6_method_recovers_F175_delta_and_F92_eta_on_leptons():
    out = mod.c6_lepton_selfcheck()
    assert out["delta_relative_error"] < 1e-4, out["delta_relative_error"]
    assert out["eta_absolute_error"] < 1e-3, out["eta_absolute_error"]
    assert abs(out["delta_mod_2pi_over_3"] - 2 / 9) < 1e-4
    assert abs(out["eta"] - math.sqrt(2)) < 1e-3


# ---------------------------------------------------------------------------
# Regression guard: this pipeline must be ABLE to report a genuine hit, not
# just decisive misses -- forcing cbt's masses exactly onto A_1g=1/9 with a
# tight synthetic precision must flip both C2 and C3's characterization.
# ---------------------------------------------------------------------------

def test_pipeline_would_flag_a_hypothetical_exact_precise_phase_match():
    orig_mev, orig_sig = mod.MIXED_CBT_MEV, mod.MIXED_CBT_SIGMA_MEV
    try:
        mu, eta, delta = 172.0, 1.42, 1.0 / 9.0
        forced = tuple(
            round((mu * (1 + eta * math.cos(delta + 2 * math.pi * a / 3))) ** 2, 6)
            for a in range(3)
        )
        mod.MIXED_CBT_MEV = forced
        mod.MIXED_CBT_SIGMA_MEV = (0.01, 0.01, 0.1)
        cc = mod.c2_c3_phase_analysis()
        assert cc["cbt"]["nearest_sigma_measurement_precision"] < 5.0
        assert cc["cbt"]["p_uniform_domain_lookelsewhere"] < 1e-4
        checks = mod.check_quark_mixed_koide_probe_result()["checks"]
        assert checks["C2_cbt_phase_decisively_excluded"] is False
        assert checks["C3_cbt_phase_not_numerically_unusual"] is False
    finally:
        mod.MIXED_CBT_MEV = orig_mev
        mod.MIXED_CBT_SIGMA_MEV = orig_sig


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def test_verdict_leaning_no_go_all_checks_pass():
    out = mod.check_quark_mixed_koide_probe_result()
    assert out["pass"] is True, out["checks"]
    assert "leaning no-go" in out["verdict"].lower()
    assert "not a full closure" in out["verdict"].lower()
