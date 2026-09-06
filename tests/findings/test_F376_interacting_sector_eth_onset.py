"""F376 -- G10 residual: does an interacting extension of the free-fermion
lattice sector break the F300/F309 GGE toward genuine (ETH) thermalisation?

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.thermodynamics_interacting.check_f375` (record
`F376-interacting-sector-eth-onset`, tier gate), so this file deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F376-interacting-sector-eth-onset
    casim test --id F376-interacting-sector-eth-onset --param v2_control=True   # red

Two things this file will NOT assert, and each is deliberate (see the finding,
sec8):

  * that this IS F110's link Hamiltonian coupled to dynamical matter.  It is
    not -- F110 sec5 says that coupling is not built, and this module does
    not attempt it.  This is the smallest interacting extension of the
    free-fermion machinery instead: an OBC single-band chain, not the model's
    own 3D two-branch BCC lattice.
  * that a nearest-neighbour interaction alone breaks integrability.  It does
    not (t-V is Jordan-Wigner-dual to XXZ, Bethe-ansatz integrable for every
    V1) -- which is why the finding needs a second (next-nearest-neighbour)
    term, and reports the comparison between the two as the actual result.

Run standalone:  python3 tests/findings/test_F376_interacting_sector_eth_onset.py
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import thermodynamics_interacting as m
    return m


def main() -> int:
    m = _bootstrap()

    res = m.check_f375()
    print("F376 / G10 residual -- interacting-sector ETH onset\n")
    for c in res["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:4s} {c['desc']}")
    assert res["all_pass"], f"only {res['n_pass']}/{res['n_total']} passed"

    print("\n  control (must go RED, and only at the regime-separation checks):")
    rc = m.check_f375(v2_control=True)
    red = [c["id"] for c in rc["checks"] if not c["pass"]]
    expect_red = {"C3", "C4", "C5", "C6"}
    assert not rc["all_pass"], "v2_control=True did NOT go red"
    assert set(red) == expect_red, f"control went red at {red}, expected {sorted(expect_red)}"
    print(f"    v2_control=True   RED: {', '.join(red)}")

    by_L = res["by_L"]
    print("\n  headline numbers (L=14):")
    for r in by_L["14"]:
        print(f"    {r['tag']:15s} r_mean={r['r_mean']:.4f}+-{r['r_err']:.4f}  "
              f"frac_ceiling={r['frac_ceiling']:.4f}  ETH_sA_std={r['ETH_sA_std']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
