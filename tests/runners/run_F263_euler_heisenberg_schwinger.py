#!/usr/bin/env python3
"""
run_F263_euler_heisenberg_schwinger.py — standalone runner for the F263 nonlinear
/ non-perturbative QED sector. Emits a JSON result file (per CLAUDE.md:
sandbox-timeout-safe path for Claude to read). Runs the full ca_euler_heisenberg
and ca_schwinger_pair reports plus the test-battery summary.

Usage:
    python3 tests/runners/run_F263_euler_heisenberg_schwinger.py [--json PATH]
"""
from __future__ import annotations
import os, sys, json, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (
    os.path.join(_HERE, "..", "..", "ca-simulation"),
    os.path.join(_HERE, "..", "ca-simulation"),
):
    _cand = os.path.abspath(_cand)
    if os.path.isdir(_cand) and _cand not in sys.path:
        sys.path.insert(0, _cand)
# allow importing the test-battery summary
sys.path.insert(0, os.path.join(_HERE, "..", "findings"))

import ca_euler_heisenberg as eh   # noqa: E402
import ca_schwinger_pair as sc     # noqa: E402
import test_F263_euler_heisenberg_schwinger as t263   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(
        _HERE, "..", "..", "test-results", "F263_euler_heisenberg_schwinger.json"))
    args = ap.parse_args()

    # Schwinger rate across a field sweep (dimensionless R = sum 1/n^2 e^{-n pi Ec/E})
    field_sweep = {f"E_over_Ecrit_{x}": sc.pair_production_rate(x)
                   for x in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0)}

    out = {
        "finding": "F263",
        "title": "Nonlinear/non-perturbative QED: Euler-Heisenberg, light-by-light, "
                 "vacuum birefringence, Schwinger pair production",
        "euler_heisenberg": eh.report(),
        "schwinger": sc.report(),
        "schwinger_field_sweep": field_sweep,
        "test_battery": t263.run_all(),
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
    with open(args.json, "w") as f:
        json.dump(out, f, indent=2, default=str)
    tb = out["test_battery"]
    print(f"F263: {tb['n_pass']}/{tb['n_total']} checks pass -> {args.json}")


if __name__ == "__main__":
    main()
