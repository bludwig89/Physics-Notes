"""F407 -- FORK: the minimal pseudo-mass quark fit (derivation three of the
2026-09-24 flavour research report) -- one real degree of freedom, spent on
nothing.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.forks.particles.koide_pseudomass_minimal.check_koide_pseudomass_minimal`
(record `F407-koide-pseudomass-minimal`, tier gate), so this module
deliberately defines no `test_*` functions.

    casim test --id F407-koide-pseudomass-minimal
    casim test --id F407-koide-pseudomass-minimal --param scheme=MZ
    casim test --id F407-koide-pseudomass-minimal --param t1g=False             # red (M2 x3)
    casim test --id F407-koide-pseudomass-minimal --param force_positive=True   # red (M2 x3)

Run standalone:  python3 tests/findings/test_F407_koide_pseudomass_minimal.py
(the heavy delta-landscape and m_s-profile scans are written by
`python3 src/casim/engine/forks/particles/koide_pseudomass_minimal.py --scans`).
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.forks.particles import koide_pseudomass_minimal as m
    return m


def main() -> int:
    m = _bootstrap()
    ok = True
    for scheme in ("mixed", "MZ"):
        res = m.check_koide_pseudomass_minimal(scheme=scheme)
        for name, c in res["checks"].items():
            print(f"  [{scheme}] [{'PASS' if c['pass'] else 'FAIL'}] {name}")
        ok = ok and res["pass"]
    print(f"\n  OVERALL: {'PASS' if ok else 'FAIL'}")
    assert ok
    return 0


if __name__ == "__main__":
    sys.exit(main())
