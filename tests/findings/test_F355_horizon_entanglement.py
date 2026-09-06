"""F355 — E9: the boundary entanglement entropy of the BCC vacuum, computed.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.horizon_entanglement.check_e9` (record
`F355-horizon-entanglement`, tier gate), so this file deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F355-horizon-entanglement
    casim test --id F355-horizon-entanglement --param flat_control=True    # red
    casim test --id F355-horizon-entanglement --param random_control=True  # red

What this finding is, in one line: F190 POSITED that each horizon cell carries
2 pi sqrt3 = 10.8828 nats; this record COMPUTES what the model's own vacuum puts
there, and the two disagree -- by a factor that is BRACKETED 0.79 to 3.18, not a
single number.

Four checks carry the result:

  E9-1    the Peschel correlation-matrix formula reproduces a brute-force
          many-body reduced density matrix to machine precision.  Nothing
          downstream is worth reading if this fails, which is why it is first.
  E9-8    S/A is flat while the enclosed volume grows.  This is the area law
          itself, measured rather than assumed -- and it is what the
          `random_control` destroys.
  E9-10   the walk has FOUR gapless points, Berry charges -1,+1,+1,-1 summing to
          zero.  So one walk is NOT one Weyl field, and F278 section 6 leaves the
          omega = pi doubler question undecided.  This is why the per-cell number
          is a bracket (12 / 24 / 48 walks) and the record's expect.exactness is
          `bracketed`.
  E9-11   S = A/4 is missed under EVERY counting in that bracket -- the closest
          still misses by 21%.  The MISMATCH is the deliverable; WHICH counting
          applies is not decided, here or anywhere in the tree.

Three things this file will NOT assert, and each is deliberate:

  * **that 2 pi sqrt3 is wrong.**  It is what S = A/4 requires given the F107
    ruler, and F190 derived it correctly.
  * **that this tests Bekenstein-Hawking.**  It does not.  F79's G is itself
    INDUCED (no bare kinetic term, eta = 1/12 Seeley-DeWitt over the same
    content), so what is graded is two of the model's own computations of the
    same induced 1/G.  See finding section 2.
  * **that the mismatch factor is pi.**  At the 48-walk counting it is 3.1795,
    1.21% above pi -- but that is 1.2 sigma, and 2^(5/3) = 3.17480 is CLOSER.
    An earlier draft claimed 5.7 sigma on a sigma 4.7x too small; that exclusion
    is withdrawn.  `pi_proximity()` records both under the D7 `coincidence`
    discipline.

Note on E9-11 under the random control: it stays GREEN there, and for the wrong
reason -- white noise gives a VOLUME law, so every ratio is enormous and "every
ratio misses 1" is satisfied trivially.  E9-8 is what reds under that control,
and the pair is what makes the ledger honest.  Do not read E9-11 alone.

Reviewed 2026-09-03: docs/reviews/F355-review-2026-09-03.md (verdict OVERSTATED
against the first draft; remediated in-session).

Run standalone:  python3 tests/findings/test_F355_horizon_entanglement.py
Full scale (minutes, writes the results JSON):
                 python3 -m casim.engine.interactions.horizon_entanglement full
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    # Inside the function, not at module scope: a module-level sys.path preamble
    # is what `tools/audit_tests.py` counts as import-time work.
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import horizon_entanglement as m
    return m


def main() -> int:
    m = _bootstrap()

    res = m.check_e9()
    print("F355 / E9 — boundary entanglement entropy vs 2 pi sqrt3\n")
    for c in res["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:7s} {c['desc']}")
    assert res["all_pass"], f"only {res['n_pass']}/{res['n_total']} passed"

    controls = [
        ({"flat_control": True}, ("E9-5", "E9-7", "E9-8", "E9-11")),
        ({"random_control": True}, ("E9-5", "E9-7", "E9-8")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_e9(**kwargs)
        red = [c["id"] for c in r["checks"] if not c["pass"]]
        assert not r["all_pass"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<30} RED: {', '.join(red)}")

    led = res["ledger"]
    print("\n  headline numbers:")
    print(f"    c per BCC walk            {led['c_walk_per_a2']:.5f}"
          f" +- {led['c_walk_sigma']:.4f} nats / a^2")
    print(f"    required (closed form)    {led['c_required_closed_form']:.7f}"
          f"   = {led['c_required_expression']}")
    print(f"    ratio (g_*-independent)   {led['ratio_at_fixed_counting']:.4f}"
          f" +- {led['ratio_sigma']:.4f}")
    print(f"    required per cell         {led['s_cell_required']:.4f}   (2 pi sqrt3)")
    print("    node-counting bracket (F278 section 6, undecided):")
    for k, v in led["node_counting_bracket"].items():
        print(f"      {k:26s} s_cell={v['s_cell']:8.4f}  ratio={v['ratio']:.4f}")
    print("\n  orientation dependence (nats / a^2, one walk):")
    for k, v in res["planes"].items():
        print(f"    {k:12s} {v:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
