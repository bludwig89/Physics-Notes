"""F384 — the U(1) EM current the BCC Weyl walk actually conserves
(Stage 1, docs/roadmaps/photon-fermion-coupling.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.em_current.check_conserved_current` (record
`F384-conserved-em-current`, tier gate), so this module deliberately defines
no `test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F384-conserved-em-current
    casim test --id F384-conserved-em-current --param use_naive_for_construction=true   # red

Four legs (see `em_current.check_conserved_current`'s own docstring for the
full description of each):

    construction_closes           the derived current's masked continuity
                                   residual is < 1e-10 (FFT round-off)
    naive_current_much_worse      the continuum ψ†σψ current's full residual
                                   is > 100x the derived current's, same packet
    naive_shrinks_with_lower_k0   the naive current's residual falls at lower
                                   momentum -- the O(k·a) discretisation
                                   signature, not a fixed disagreement
    global_charge_conserved       Sigma_x rho(t+1) = Sigma_x rho(t) exactly
                                   (unitarity floor, independent of J)
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import em_current as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_conserved_current()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  construction_residual={res['construction_residual']:.3e}  "
          f"naive_residual_full={res['naive_residual_full']:.3e}  "
          f"exact_residual_full={res['exact_residual_full']:.3e}  "
          f"nyquist_gap={res['nyquist_gap']:.3e}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F384_conserved_em_current.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F384 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
