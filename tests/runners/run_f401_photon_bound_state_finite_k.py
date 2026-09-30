#!/usr/bin/env python3
"""F401 runner — emit the finite-k threshold-repair result artifact.

Writes `test-results/F401_photon_bound_state_finite_k.json`. The axis
identity is exact (sympy); the L-convergence and g_c(k) sweep are
quantitative finite-L numerics (no floats where an exact statement is made).

    PYTHONPATH=src python3 tests/runners/run_f401_photon_bound_state_finite_k.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Put src/ and tests/findings/ on sys.path and return what this runner needs.

    Inside a call, not at module scope — see F291's own runner for why.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "..", "..", "src"),
              os.path.join(here, "..", "findings")):
        if p not in sys.path:
            sys.path.insert(0, p)
    from casim.engine.particles._results_path import results_path
    from test_F401_photon_bound_state_finite_k import check_all
    return results_path, check_all


def _assert_verdict(out: dict) -> None:
    assert out["A1_axis_identity_exact"]["identity_exact"] is True
    assert out["B1_closed_form_converges_monotonically"][
        "closed_monotonic"] is True
    assert out["B1_closed_form_converges_monotonically"][
        "grid_monotonic"] is False
    b2 = out["B2_dense_scan_quantified_improvement"]
    assert b2["closed_max_backslide"] < b2["grid_max_backslide"] / 2.0
    assert b2["closed_n_violations"] > 0
    assert out["B3_gc_k_sweep_decreasing"][
        "111_and_311_monotonically_decreasing"] is True
    assert out["B3_gc_k_sweep_decreasing"]["210_is_a_counterexample"] is True
    assert int(out["n_checks"]) == 5, out["n_checks"]


def main() -> int:
    results_path, check_all = _bootstrap()
    out = check_all()
    _assert_verdict(out)
    dest = results_path("F401_photon_bound_state_finite_k.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True, default=str)
    print(f"wrote {dest}")
    print(f"  checks                : {out['n_checks']}")
    print(f"  axis identity exact   : "
          f"{out['A1_axis_identity_exact']['identity_exact']}")
    b2 = out["B2_dense_scan_quantified_improvement"]
    print(f"  dense-scan backslide  : grid {b2['grid_max_backslide']:.4f} "
          f"vs closed {b2['closed_max_backslide']:.4f}")
    b3 = out["B3_gc_k_sweep_decreasing"]
    print(f"  gc(k=0)               : {b3['gc_k0']:.4f}")
    print(f"  gc(k) sweep along 111 : {b3['gc_sweep_111']}")
    print(f"  gc(k) sweep along 210 (counterexample): {b3['gc_sweep_210']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
