"""F346 -- does the charged-lepton E_g/T_1u SHAPE mechanism have a quark-sector face?
(ledger row E6, docs/status/open-derivations.md)

E6 grades the six quark (current) masses ABSENT x6: F121 is explicit that the numbers
attached to them today are "the measured values converted to kg -- a CONSISTENCY
readout," not a derivation, and F123's constituent m_c=309.5 MeV is a DIFFERENT
quantity that must not be quoted as covering this row. No route had been proposed. E6
names its own smallest first question: does the E_g/T_1u machinery that gives the
charged-lepton SHAPE to 0.007% (F175, F92) have ANY quark-sector face, using F80-D4's
already-flagged Koide-Q mismatch (0.849, 0.731 vs the lepton 2/3) as the starting
evidence for "lepton-only."

This record runs that question on the SAME 3-parameter circulant ansatz F175 used
(sqrt(m_a) = mu*(1+eta*cos(delta+2*pi*a/3))), inverted exactly on the up-type (u,c,t)
and down-type (d,s,b) PDG 2024 current-quark mass triplets, and compares the fitted
delta (mod 2*pi/3) against the three single-irrep O_h weights available in the SAME
T_1u x T_1u = A_1g + E_g + T_1g + T_2g decomposition (F175 Sec. 2) that supplies the
lepton's 2/9.

Revised after the F346 review (docs/reviews/F346-review-2026-09-02.md, Attack 7 --
perturbation sweep): the first draft's C3/C4 conflated two different statistical
questions under one "sigma"/"p" pair -- measurement-precision compatibility (is the
candidate excluded by current data) versus a range-based look-elsewhere estimate (is
the central value's proximity to a nice fraction unusual for a generic number). A
perturbation test (force a synthetic triplet exactly onto a candidate with tight
uncertainty) showed the original single formula would have called an increasingly
PRECISE, essentially-confirmed match "not significant" -- the wrong direction. C2/C3
below now answer the measurement-compatibility question only; C4 is a separate,
correctly-scaled look-elsewhere calculation:

  C1  the independently-recomputed Koide Q for both quark sectors reproduces F80-D4's
      already-recorded values (0.849, 0.731) -- the new angle-level computation rests
      on the same, previously-checked mass inputs.
  C2  up-type's fitted angle is incompatible (>50 sigma, measurement precision) with
      every single-irrep O_h weight -- a clean, decisive miss.
  C3  down-type's fitted angle is NOT excluded (<3 sigma, measurement precision) from
      the A_1g weight 1/9 -- current data cannot rule this out (a weaker statement
      than "confirmed").
  C4  under a range-based (uniform-domain [0, 2*pi/3)) look-elsewhere estimate, the
      down-type proximity is a real but modest coincidence (roughly 0.1-5%), neither
      vanishingly rare nor common -- correcting an earlier claim that it was ~62%
      likely by pure chance, which used the wrong (measurement-precision) scale for
      this question.
  C5  neither quark sector's fitted eta^2 is anywhere near the lepton's derived
      eta^2=2 (F92) -- consistent with F80's claim that only the EM-coupled,
      colour-free charged leptons reach the saturation/equipartition point.
  C6  a lepton-sector self-check: the IDENTICAL fitting code recovers F175's own
      delta*=2/9 (to <0.01%) and F92's eta=sqrt(2) (to <1e-3) from the PDG charged-
      lepton masses -- confirming the quark-sector null result is not a fitting
      artefact.

What this record does NOT claim: that no quark-sector mechanism can ever reproduce a
lepton-like shape (only that the DIRECT transplant of F175/F92's specific values
fails), or that the down-type 1/9 proximity is meaningless or "just chance" (C4 shows
it is not common under a naive uniform-domain null). The "flagged, not adopted"
verdict rests instead on two things C4 cannot supply: no independent theoretical
motivation for the A_1g weight in the down-type sector (unlike the lepton's E_g, which
has F80's charge/colour selection story), and no matching behaviour in the up-type
sector. See findings/F346-*.md for the full writeup and for the separate (not computed
here) discussion of the generation-COUNT question, which F75's charge-blind mechanism
may already answer independently of this shape-level result.
"""

import math

from casim.engine.particles import derive_quark_shape_probe as mod


# ---------------------------------------------------------------------------
# C1 -- pipeline sanity: recomputed Koide Q matches F80-D4's recorded values
# ---------------------------------------------------------------------------

def test_C1_koide_Q_matches_F80_D4_recorded_values():
    out = mod.c1_fit_both_sectors()
    assert abs(out["up_type"]["Q"] - 0.849) < 1e-3
    assert abs(out["down_type"]["Q"] - 0.731) < 1e-3
    # both quark sectors sit far from the lepton critical point Q=2/3
    assert abs(out["up_type"]["Q"] - 2 / 3) > 0.1
    assert abs(out["down_type"]["Q"] - 2 / 3) > 0.05


def test_C1_circulant_fit_reconstructs_input_masses_exactly():
    out = mod.c1_fit_both_sectors()
    assert out["up_type"]["max_reconstruction_residual"] < 1e-8
    assert out["down_type"]["max_reconstruction_residual"] < 1e-8


# ---------------------------------------------------------------------------
# C2 -- up-type: decisive miss, incompatible with every candidate
# ---------------------------------------------------------------------------

def test_C2_up_type_far_from_every_single_irrep_weight():
    out = mod.c2_c3_candidate_distances()
    up = out["up_type"]
    assert up["nearest_sigma"] > 50.0, (
        f"expected a decisive (>50 sigma) miss, got {up['nearest_sigma']}"
    )
    # sanity: the fitted angle itself should not be numerically close (in
    # absolute radians) to any candidate either -- this is not just a tiny
    # uncertainty inflating the sigma count.
    for cname, d in up["distances"].items():
        assert d["abs_diff_rad"] > 0.02, (cname, d)


# ---------------------------------------------------------------------------
# C3 -- down-type: not excluded by current measurement precision
# ---------------------------------------------------------------------------

def test_C3_down_type_nearest_candidate_is_A1g_but_not_decisively():
    out = mod.c2_c3_candidate_distances()
    down = out["down_type"]
    assert down["nearest_candidate"] == "A_1g (1/9)"
    assert 0.5 < down["nearest_sigma"] < 3.0, (
        "expected a nominal, not-decisive proximity (0.5-3 sigma), got "
        f"{down['nearest_sigma']}"
    )


# ---------------------------------------------------------------------------
# C4 -- the CORRECTED range-based look-elsewhere estimate
# ---------------------------------------------------------------------------

def test_C4_lookelsewhere_probability_is_modest_not_common():
    c4 = mod.c4_lookelsewhere_context()
    p = c4["p_at_least_one_of_2_sectors_this_extreme_by_chance"]
    # Correcting the retracted ~62% claim: the properly-scaled (uniform
    # domain) estimate puts this in the roughly-percent range, not "more
    # likely than not".
    assert 1e-4 < p < 0.05, p
    assert c4["per_sector"]["down_type"]["p_uniform_domain_single_sector"] < 0.02


def test_C4_up_type_lookelsewhere_probability_is_not_extreme_either():
    """Sanity: even up-type's absolute (radian) miss is not vanishingly
    improbable under the range-based null -- the >200-sigma exclusion in C2
    is a MEASUREMENT-PRECISION statement, not a claim that up-type's central
    value is an absurdly unusual number in absolute terms. Keeping this
    distinction explicit is the whole point of separating C2/C3 from C4."""
    c4 = mod.c4_lookelsewhere_context()
    p_up = c4["per_sector"]["up_type"]["p_uniform_domain_single_sector"]
    assert 0.01 < p_up < 0.5, p_up


# ---------------------------------------------------------------------------
# C5 -- neither quark sector reaches the lepton's equipartition amplitude
# ---------------------------------------------------------------------------

def test_C5_quark_amplitudes_do_not_match_lepton_equipartition():
    out = mod.c1_fit_both_sectors()
    # F92's derived lepton value is eta^2 = 2 (eta = sqrt(2)).
    assert abs(out["up_type"]["eta2"] - 2.0) > 0.5
    assert abs(out["down_type"]["eta2"] - 2.0) > 0.2
    # the two quark sectors also disagree with EACH OTHER -- no single
    # universal quark eta emerges either.
    assert abs(out["up_type"]["eta2"] - out["down_type"]["eta2"]) > 0.3


# ---------------------------------------------------------------------------
# C6 -- method validation: the identical fit recovers F175/F92 on leptons
# ---------------------------------------------------------------------------

def test_C6_method_recovers_F175_delta_and_F92_eta_on_leptons():
    out = mod.c5_lepton_selfcheck()
    assert out["delta_relative_error"] < 1e-4, out["delta_relative_error"]
    assert out["eta_absolute_error"] < 1e-3, out["eta_absolute_error"]
    assert abs(out["delta_mod_2pi_over_3"] - 2 / 9) < 1e-4
    assert abs(out["eta"] - math.sqrt(2)) < 1e-3


# ---------------------------------------------------------------------------
# Regression test for the Attack-7 bug: a check phrased only as
# "sigma < threshold" must NOT also call an increasingly precise, essentially
# exact match "not excluded/not significant" in a way that hides a real hit.
# We do not have such a measurement today, so this is a synthetic check of
# the FUNCTION's behaviour under a hypothetical future precise measurement
# landing exactly on a candidate -- it must show up as a striking (not
# "modest") look-elsewhere probability.
# ---------------------------------------------------------------------------

def test_C4_flags_a_hypothetical_exact_precise_match_as_not_modest():
    orig_mev, orig_sig = mod.DOWN_TYPE_MEV, mod.DOWN_TYPE_SIGMA_MEV
    try:
        mu, eta, delta = 25.5, 1.5, 1.0 / 9.0
        forced = tuple(
            round((mu * (1 + eta * math.cos(delta + 2 * math.pi * a / 3))) ** 2, 8)
            for a in range(3)
        )
        mod.DOWN_TYPE_MEV = forced
        mod.DOWN_TYPE_SIGMA_MEV = (0.001, 0.01, 0.1)  # hypothetical tight future precision
        c4 = mod.c4_lookelsewhere_context()
        p_down = c4["per_sector"]["down_type"]["p_uniform_domain_single_sector"]
        # An essentially exact hit must register as a STRIKING (small)
        # look-elsewhere probability, not the "modest, 0.1-5%" band this
        # record's real data lands in.
        assert p_down < 1e-4, (
            "an exact, tightly-measured match should be flagged as a "
            f"striking coincidence, not a modest one; got p={p_down}"
        )
        checks = mod.check_quark_shape_probe_leaning_null_result()["checks"]
        assert checks["C4_lookelsewhere_not_overwhelming_but_not_dismissible"] is False, (
            "the 'modest, not dismissible' characterization must NOT hold "
            "for an essentially exact match -- that would be a confirmed "
            "hit requiring different treatment, not this finding's verdict"
        )
    finally:
        mod.DOWN_TYPE_MEV = orig_mev
        mod.DOWN_TYPE_SIGMA_MEV = orig_sig


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def test_verdict_leaning_no_go_all_legs_pass():
    out = mod.check_quark_shape_probe_leaning_null_result()
    assert out["pass"] is True, out["checks"]
    assert "leaning no-go" in out["verdict"].lower()
    assert "not a full closure" in out["verdict"].lower()
