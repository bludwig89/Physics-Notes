"""Results compare (P5.4) — finding F275.

*Created 2026-07-31 - 23:00.*

``casim compare`` must agree with the project's own notion of "moved": it reuses
``casim.baselines.compare`` (the numeric diff behind ``_diff_against_head`` and
``check_result_drift``), so a change above the 1e-12 machine floor is reported
and a difference below it, on both sides, is classified as noise rather than
drift.  These checks pin exactly that.
"""
from __future__ import annotations

from casim.analysis.compare import compare_runs, format_comparison


def test_identical_payloads_report_no_change():
    a = {"observers": {"o": {"records": [{"x": 1.0}]}}}
    res = compare_runs(a, dict(a))
    assert res["identical"] and res["n_significant"] == 0


def test_a_real_change_is_reported():
    a = {"seed": 5, "observers": {"o": {"records": [{"drift": 1.0}]}}}
    b = {"seed": 5, "observers": {"o": {"records": [{"drift": 2.0}]}}}
    res = compare_runs(a, b)
    assert res["n_significant"] == 1
    d = res["significant"][0]
    assert d["before"] == 1.0 and d["after"] == 2.0
    assert "drift" in d["path"]


def test_subfloor_difference_is_noise_not_change():
    # Both sides below the 1e-12 machine floor, but a large *relative* gap
    # (5e-13 -> 1e-13): a naive relative diff would scream 80%; the floor
    # classifier calls it noise, which is the whole point.
    a = {"r": 5e-13}
    b = {"r": 1e-13}
    res = compare_runs(a, b)
    assert res["n_significant"] == 0
    assert res["n_floor"] == 1
    # strict_floor promotes it to a real change
    strict = compare_runs(a, b, strict_floor=True)
    assert strict["n_significant"] == 1


def test_volatile_keys_are_ignored():
    # timestamps / paths must not count as drift.
    a = {"timestamp": 111, "value": 1.0, "out_path": "/a"}
    b = {"timestamp": 999, "value": 1.0, "out_path": "/b"}
    assert compare_runs(a, b)["identical"]


def test_formatter_renders_without_error():
    a = {"value": 1.0}
    b = {"value": 2.0}
    txt = format_comparison("A", "B", compare_runs(a, b))
    assert "moved" in txt and "value" in txt


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
