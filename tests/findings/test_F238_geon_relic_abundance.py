"""Test wrapper for F238 -- can the F223/F228 geon relic abundance be derived?

Prompt D3.  Runs the self-contained real-arithmetic battery in
ca-simulation/forks/gr_fork_F238_geon_relic_abundance.py and asserts the derivation
attempt and its HONEST NEGATIVE RESULT:

  * (S1) the geon side is fully pinned (reuse F228 M_rem + entropy-conserved yield);
         the only unpinned quantity is beta(M_form).
  * (S2) inverting the F228 beta band via Press-Schechter needs a small-scale
         amplitude sigma ~ 0.06-0.08.
  * (S3) THE ACCEPTANCE TEST: the only tuning-free spectrum (scale-invariant, n_s=1,
         at the CMB amplitude) does NOT land Omega_DM h^2 in the Planck band
         [0.117, 0.123] -- it under-produces by ~2e7 orders. => abundance is not
         derivable non-tunably from that channel.
  * (S4) reaching 0.12 needs a ~1e6 spectral boost (an inflaton input).
  * (S5) beta(sigma) has no attractor.
  * (S6) the model has no inflaton / primordial-spectrum sector.
  * (S7) VERDICT: abundance remains a free cosmological initial condition.
"""
import importlib.util, os

HERE = os.path.dirname(__file__)
FORK = os.path.abspath(os.path.join(
    HERE, "..", "..", "ca-simulation", "forks", "gr_fork_F238_geon_relic_abundance.py"))

PLANCK_BAND = (0.117, 0.123)   # Omega_DM h^2 = 0.120 +- ~0.003 (Planck 2018)


def _run():
    spec = importlib.util.spec_from_file_location("gr_fork_F238", FORK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RESULTS


def test_F238_all_checks_pass():
    res = _run()
    failed = [c["check"] for c in res["checks"] if not c["pass"]]
    assert not failed, f"F238 checks failed: {failed}"
    assert res["summary"]["n_pass"] == res["summary"]["n_total"] == 7


def test_F238_geon_side_pinned_only_beta_free():
    res = _run()
    s = res["step1_geon_side"]
    # exact-algebraic one-cell remnant mass (F190/F107), reused from F228
    assert abs(s["M_rem_over_Mpl"] - (3.0**0.5 / 2.0) ** 0.5) < 1e-12
    # beta is the sole residual: a small, un-excluded number for each formation mass
    for k, v in s["beta_band"].items():
        assert 0.0 < v["beta_required"] < 1.0, k


def test_F238_acceptance_scale_invariant_misses_planck_band():
    """ACCEPTANCE TEST: the tuning-free (scale-invariant) channel must NOT hit the
    Planck band -- i.e. abundance is not derivable non-tunably from it."""
    res = _run()
    s3 = res["step3_scale_invariant"]
    # produced Omega from the scale-invariant spectrum is ~10^(-2e7): its log10 is
    # astronomically below the (log10 of the) Planck band, so it misses by a huge margin.
    import math
    log10_lo, log10_hi = math.log10(PLANCK_BAND[0]), math.log10(PLANCK_BAND[1])
    log10_Omega_HZ = s3["log10_Omega_HZ"]
    assert log10_Omega_HZ < log10_lo            # far below the band
    assert s3["underproduces_by_orders"] > 1e6  # by >1e6 orders


def test_F238_required_spectral_boost_is_an_external_input():
    res = _run()
    s2 = res["step2_required_sigma"]
    s4 = res["step4_required_boost"]
    # required small-scale sigma is O(0.06-0.08), far above the CMB sqrt(A_s) ~ 4.6e-5
    sigs = [v["sigma_required"] for v in s2.values()]
    assert all(0.03 < x < 0.2 for x in sigs)
    # => power must be boosted by ~1e6 (an inflaton-potential input)
    assert s4["boost_lo"] > 1e5


def test_F238_no_beta_attractor():
    res = _run()
    s5 = res["step5_no_attractor"]
    assert s5["strictly_increasing"] is True     # monotone, no fixed point


def test_F238_no_inflaton_sector():
    res = _run()
    s6 = res["step6_missing_sector"]
    assert s6["inflaton_findings"] == []
    assert s6["inflaton_modules"] == []


def test_F238_verdict_free_input():
    res = _run()
    ans = res["summary"]["answer"].lower()
    assert "free" in ans and "no" in ans
    assert res["summary"]["relation_to_F228"].lower().startswith("extends f228")
