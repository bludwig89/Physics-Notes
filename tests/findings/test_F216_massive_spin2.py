"""Test wrapper for F216 — massive spin-2 / second-polarization dark-sector fork.

Runs the self-contained real-arithmetic battery in
ca-simulation/forks/gr_fork_F216_massive_spin2.py and asserts all checks pass.
"""
import importlib.util, os, json

HERE = os.path.dirname(__file__)
FORK = os.path.abspath(os.path.join(
    HERE, "..", "..", "ca-simulation", "forks", "gr_fork_F216_massive_spin2.py"))


def _run():
    spec = importlib.util.spec_from_file_location("gr_fork_F216", FORK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.RESULTS


def test_F216_all_checks_pass():
    res = _run()
    failed = [c["check"] for c in res["checks"] if not c["pass"]]
    assert not failed, f"F216 checks failed: {failed}"
    assert res["summary"]["n_pass"] == res["summary"]["n_total"] == 7


def test_F216_metric_graviton_has_no_native_massive_mode():
    res = _run()
    s = res["summary"]
    assert s["massless_graviton_dof"] == 2
    assert s["metric_graviton_massless"] is True
    assert s["native_massive_spin2_in_metric"] is False


def test_F216_massive_spin2_is_cold_collisionless():
    res = _run()
    s = res["summary"]
    assert s["massive_spin2_dof"] == 5
    assert s["helicity_split"] == "2+2+1"
    assert s["cold_equation_of_state_w"] < 1e-5   # dust / CDM
    assert s["collisionless"] is True
