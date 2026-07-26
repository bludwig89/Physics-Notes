"""Test wrapper for F223 — does the F216 massive spin-2 DM bound state form?

Runs the self-contained real-arithmetic battery in
ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py and asserts all checks pass,
plus the physics verdicts (graviton-graviton binds at mu~sqrt2 M_Pl; nu_R nu_R no-go;
gravitational production under-produces).
"""
import importlib.util, os

HERE = os.path.dirname(__file__)
FORK = os.path.abspath(os.path.join(
    HERE, "..", "..", "ca-simulation", "forks", "gr_fork_F223_spin2_binding_relic.py"))


def _run():
    spec = importlib.util.spec_from_file_location("gr_fork_F223", FORK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RESULTS


def test_F223_all_checks_pass():
    res = _run()
    failed = [c["check"] for c in res["checks"] if not c["pass"]]
    assert not failed, f"F223 checks failed: {failed}"
    assert res["summary"]["n_pass"] == res["summary"]["n_total"] == 6


def test_F223_graviton_graviton_binds_at_planck():
    res = _run()
    s = res["summary"]
    assert s["graviton_graviton_binds"] is True
    # geon virial mass = sqrt(2) M_Pl
    assert abs(s["mu_geon_over_Mpl"] - 2.0**0.5) < 1e-12
    assert 1e19 < s["mu_geon_GeV"] < 2e19          # WIMPzilla / Planckian


def test_F223_nuR_nuR_is_a_nogo():
    res = _run()
    # every sub-Planckian M_R gives negligible gravitational binding
    assert all(v["frac_binding"] < 1e-15 for v in res["nuR_channel"].values())


def test_F223_gravitational_production_underproduces():
    res = _run()
    # every point on the (H_inf, T_RH) grid stays far below Omega~0.12
    assert all(logO < -30 for logO in res["cgpp_band_log10_Omega"].values())


def test_F223_data_battery_all_pass():
    res = _run()
    # S6 encodes cold + collisionless + non-fuzzy + dNeff~0
    s6 = next(c for c in res["checks"] if c["check"] == "S6_data_battery_vs_mu")
    assert s6["pass"] is True
