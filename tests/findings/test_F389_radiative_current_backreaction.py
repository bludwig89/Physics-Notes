"""F389 -- does the fixed current let the fermion<->photon loop (Stage 4,
docs/roadmaps/photon-fermion-coupling.md) genuinely radiate and recoil?

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.core.coupled.check_radiative_current_backreaction` (record
`F389-radiative-current-backreaction`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F389-radiative-current-backreaction
    casim test --id F389-radiative-current-backreaction --param use_radiative_current=false   # red

Four legs (see `coupled.check_radiative_current_backreaction`'s own
docstring for the full description of each):

    field_momentum_genuinely_nonzero
        ||dP_field|| > 1e-8 in the self-sourced-only scenario -- F388's own
        current made this machine zero always; this is the direct
        demonstration the fix breaks that triviality.
    no_monopole_holds
        F387's split-sourcing fix still holds with the new current.
    momentum_partially_but_not_exactly_conserved
        0.01 < ||dP_field||/||dP_matter|| < 0.9 -- a genuine, bounded,
        DISCLOSED-AS-PARTIAL recovery, not exact conservation.
    matter_push_scales_linearly_field_push_scales_quadratically
        the measured, quantified order-mismatch (O(g_lat) vs O(g_lat^2))
        that is the reason exact conservation is not achieved here.
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.core import coupled as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_radiative_current_backreaction()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  dP_matter_norm={res['dP_matter_norm']:.3e}  "
          f"dP_field_norm={res['dP_field_norm']:.3e}  "
          f"recovered_fraction={res['recovered_fraction']:.4f}  "
          f"dPm_doubling_ratio={res['dPm_doubling_ratio']:.3f}  "
          f"dPf_doubling_ratio={res['dPf_doubling_ratio']:.3f}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F389_radiative_current_backreaction.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F389 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
