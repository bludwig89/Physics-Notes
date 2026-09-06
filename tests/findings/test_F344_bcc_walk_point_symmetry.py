"""F344 -- what is the EXACT point-group covariance of the adopted BCC
free-Weyl walk (Paper 1 Eq. 15, `casim.engine.lattice.bcc._bcc_uvec`)?

Answer: D_4h (16 of the 48 elements of O_h), not O_h.  O_h holds exactly in
the |k| -> 0 limit and is broken at O(k^2) by the T_2g term of n, with a
closed-form defect; and NO admissible sign/branch convention of Eq. 15 can do
better, because unitarity and C_3 covariance of the T_2g sector are mutually
exclusive.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.lattice.bcc_point_symmetry.check_bcc_walk_point_symmetry`
(record `F344-bcc-walk-point-symmetry`, tier gate), so this module
deliberately defines no `test_*` functions.

    casim test --id F344-bcc-walk-point-symmetry
    casim test --id F344-bcc-walk-point-symmetry --param expansion_order=leading      # red
    casim test --id F344-bcc-walk-point-symmetry --param coefficient_source=cyclic    # red

WHAT IS AND IS NOT CLAIMED.  F30's dispersion anisotropy (a statement about u
alone) is NOT re-attacked -- closed, and independent of everything here, since
u is untouched by the spin structure.  The O_h monomial classification of u
and n (the {1; x,y,z; yz,zx,xy; xyz} basis) is NOT re-attacked -- it is
correct as polynomial bookkeeping.  What this finding adds is that the
bookkeeping does not license an O_h REPRESENTATION reading of the walk's
O(k^2) term: the full spin+orbital law is not O_h-covariant, so its "T_2g
content" is not a T_2g tensor of O_h, and no O_h RG-relevance argument can be
built on it (which closes the free walk as a candidate for F342's condition-(i)
escape hatch, rubric C1).

Run standalone:  python3 tests/findings/test_F344_bcc_walk_point_symmetry.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.lattice import bcc_point_symmetry as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_bcc_walk_point_symmetry()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    d = res["detail"]
    print(f"\n  |L| = {d['L_order']} (closed={d['L_closed']}, proper={d['L_proper_elements']}, "
          f"4-fold axis={d['L_invariant_axes']}), unitarily implementable = "
          f"{d['unitary_subgroup_order']}")
    print(f"  max |L| over all {d['admissible_conventions']} unitary conventions = "
          f"{d['max_L_over_conventions']}; conventions admitting a body-diagonal "
          f"C_3 = {d['conventions_admitting_a_C3']}/{d['admissible_conventions']}")
    print(f"  O(k) truncation: |L| = {d['L_order_leading']}/48")
    print(f"  shipped-code residual on L = {d['max_residual_on_L_shipped_code']:.3e}; "
          f"C_3 floor {d['C3_residual_floor_k0.1']:.4f} -> "
          f"{d['C3_residual_floor_k0.01']:.5f} (slope {d['C3_residual_slope']:.2f}, "
          f"linear in |k|)")
    print(f"\n  OVERALL: {'PASS' if res['all_pass'] else 'FAIL'} "
          f"({res['n_pass']}/{res['n_total']})")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F344_bcc_walk_point_symmetry.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["all_pass"], "F344 gate failed: " + json.dumps(res["checks"], default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
