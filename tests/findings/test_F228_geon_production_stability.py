"""Test wrapper for F228 — how is the F223 geon produced, and is it stable?

Runs the self-contained real-arithmetic battery in
src/casim/engine/forks/gravity/gr_fork_F228_geon_production_stability.py and asserts all checks
pass, plus the physics verdicts: (Step 0) stable as the F190/F107 one-cell Planck-mass
BH remnant; (Step 1) PBH remnants are the only viable route, all field-theoretic
channels exponentially forbidden, with the hand-rolled Bogoliubov integrator validated
against the exact Bernard-Duncan model; (Step 2) F182/F188 cosmology preserved;
(Step 3) geon == Planck relic (same object).
"""
import importlib.util, os

HERE = os.path.dirname(__file__)
FORK = os.path.abspath(os.path.join(
    HERE, "..", "..", "src", "casim", "engine", "forks", "gravity", "gr_fork_F228_geon_production_stability.py"))


def _run():
    spec = importlib.util.spec_from_file_location("gr_fork_F228", FORK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RESULTS


def test_F228_all_checks_pass():
    res = _run()
    failed = [c["check"] for c in res["checks"] if not c["pass"]]
    assert not failed, f"F228 checks failed: {failed}"
    assert res["summary"]["n_pass"] == res["summary"]["n_total"] == 9


def test_F228_stability_gate_one_cell_remnant():
    res = _run()
    st = res["step0_stability"]
    # remnant sits at exactly one F107 cell: M_rem = (sqrt3/2)^(1/2) M_Pl ~ 0.9306 M_Pl
    assert abs(st["M_rem_over_Mpl"] - (3.0**0.5 / 2.0) ** 0.5) < 1e-12
    assert abs(st["one_cell_check_N"] - 1.0) < 1e-10
    assert 0.9 < st["M_rem_over_Mpl"] < 0.94


def test_F228_bogoliubov_integrator_validated():
    res = _run()
    # hand-rolled real 2-component RK4 reproduces the exact Bernard-Duncan |beta|^2
    v = res["step1_channels"]["bogoliubov_validation"]
    assert v["rel_err"] < 5e-3
    assert abs(v["wronskian"] - 1.0) < 1e-3          # |alpha|^2 - |beta|^2 = 1 (bosonic)


def test_F228_field_channels_all_forbidden():
    res = _run()
    ch = res["step1_channels"]
    # every gravitational / thermal channel is astronomically suppressed
    assert ch["cgpp_log10_suppression"] < -1e4
    assert ch["uv_freezein_log10_suppression"] < -1e4
    assert ch["graviton_coalescence_log10_suppression"] < -1e4


def test_F228_pbh_remnant_is_viable_and_pre_bbn():
    res = _run()
    band = res["step1_channels"]["pbh_remnant_band"]
    # a small, un-excluded beta<1 for each M_form, all evaporating before BBN
    for k, v in band.items():
        assert 0.0 < v["beta_required"] < 1.0, k
        assert v["pre_BBN"] is True, k
    assert res["step1_channels"]["viable_channel"].startswith("PBH remnants")


def test_F228_cosmology_preserved():
    res = _run()
    c = res["step2_cosmology"]
    assert abs(c["z_eq"] - 3430.0) < 20.0
    assert abs(c["age_gyr"] - 13.8) < 0.2
    assert c["Omega_c"] < 0.3153                     # fits inside Omega_m, no overclosure
    assert c["dNeff"] < 0.1


def test_F228_ontology_same_object():
    res = _run()
    o = res["step3_ontology"]
    # mu_geon = sqrt2 M_Pl and M_rem ~ 0.93 M_Pl agree within the O(1) virial => same object
    assert abs(o["mu_geon_over_Mpl"] - 2.0**0.5) < 1e-12
    assert 1.0 < o["ratio"] < 3.0
    assert "same object" in o["verdict"].lower()
