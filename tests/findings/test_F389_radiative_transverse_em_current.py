"""F389 -- fixing F384's declared-open transverse gauge freedom with the
continuum Noether current's own transverse projection (Sec.2,
docs/roadmaps/photon-fermion-coupling.md Stage 5 residual surfaced by the
F388 review).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.em_current.check_full_current` (record
`F389-radiative-transverse-current`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F389-radiative-transverse-current
    casim test --id F389-radiative-transverse-current --param longitudinal_only=true   # red

Three legs (see `em_current.check_full_current`'s own docstring for the full
description of each):

    continuity_untouched                   the transverse addition cannot
                                            perturb continuity -- measured,
                                            not assumed
    transverse_current_genuinely_nonzero   the fix does something (not the
                                            ~2e-16 noise F384/F388 measured)
    longitudinal_sector_unchanged          the fix adds content, it does not
                                            alter F384's own Coulomb sector
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
    res = m.check_full_current()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  transverse_fraction={res['transverse_fraction']:.4f}  "
          f"continuity_diff={res['continuity_diff']:.3e}  "
          f"longitudinal_sector_max_diff={res['longitudinal_sector_max_diff']:.3e}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F389_radiative_transverse_current.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F389 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
