"""F379 — the emergent continuous SO(3) is the wrong kind of object for
Postulate 1 (completeness row A9, continuing F330).

This file is the human-readable driver. The CONTRACT is the registry entry
`casim.engine.interactions.qi_so3_kinematic_gap.check_so3_kinematic_gap`
(record `F379-so3-kinematic-gap`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F379-so3-kinematic-gap
    casim test --id F379-so3-kinematic-gap --param use_uncorrelated_rotor=true  # red

WHAT IS AND IS NOT CLAIMED. F330 abandoned a lattice-native belt-trick
derivation because the finite point group O_h "carries no fundamental-group
content" that could stand in for pi_1(SO(3)). This module tests the one route
F330 left open: does the model's own EMERGENT CONTINUOUS SO(3) -- F129/F130's
block-spin RG isotropy (rubric A12), or F344's exact leading-order covariance
of the BCC Weyl walk under all 48 elements of O_h -- succeed where the
discrete O_h failed?

It does NOT derive Postulate 1. K1-K3 machine-verify that the model's
continuum limit really does supply a genuine, exact continuous SO(3) acting
jointly on (momentum, spin) via the SAME rotor object F289/F330 use for the
spin-statistics argument itself -- a real, additive extension of F344 (which
checked only 48 discrete elements) to the full continuous group. What CLOSES
the row is a structural argument, grounded in Anastopoulos's own paper
(quant-ph/0110169, fetched and read directly this session): Postulate 1 is
stated at the PREQUANTISATION level -- a transitive symplectic G-action on
the CLASSICAL PHASE SPACE, with no Hamiltonian anywhere in its three
conditions -- while K1-K3 are all facts about the model's DYNAMICS (the Weyl
Hamiltonian's own covariance under rotation). Since Postulate 1 sits logically
prior to any choice of Hamiltonian, no dynamical fact -- however large,
however exactly or emergently derived -- can supply it. This generalises
F330's "O_h is finite" diagnosis: it is not that this model's emergent
symmetry is the wrong SIZE, it is that any dynamical symmetry, of any size,
is the wrong KIND of object.

    K1   the idealised Weyl Hamiltonian H_W = k.sigma/sqrt(3) is covariant
         under the FULL continuous SO(3) (Rodrigues rotations, not merely
         O_h's 48 elements), via su2_rotor -- F289/F330's own rotor function
         -- at the round-off floor.
    K2   the ACTUAL shipped BCC dispersion (bcc._bcc_uvec) obeys the same
         covariance law at leading order, for a GENERIC continuous rotation,
         with the defect shrinking linearly in |k| (decade ratio -> 10),
         extending F344's leg C8 (checked only for the discrete C3 rotation).
    K3   CONTROL: transporting spin via an UNCORRELATED rotation breaks K1's
         identity at O(1) -- confirming the check is a real "same rotation"
         statement (Postulate 1's own "rather than some other, uncorrelated
         unitary"), not a tautology of SU(2) closure.

Run standalone:  python3 tests/findings/test_F379_so3_kinematic_gap.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_so3_kinematic_gap as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_so3_kinematic_gap()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F379 gate failed: " + json.dumps(res["checks"],
                                                             default=str)

    controls = [
        ({"use_uncorrelated_rotor": True}, ("K1",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_so3_kinematic_gap(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<32} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    idealised H_W worst residual (continuous SO(3))  "
          f"{s['F379_idealized_worst_residual']:.2e}")
    print(f"    idealised checks swept                            "
          f"{s['F379_idealized_n_checked']}")
    print(f"    shipped-walk decade ratios, branch '+' (-> 10)      "
          f"{['%.3f' % v for v in s['F379_shipped_decade_ratios_plus']]}")
    print(f"    shipped-walk decade ratios, branch '-' (-> 10)      "
          f"{['%.3f' % v for v in s['F379_shipped_decade_ratios_minus']]}")
    print(f"    control: correct rotor                            "
          f"{s['F379_control_correct_rotor']:.2e}")
    print(f"    control: uncorrelated rotor (should be O(1))      "
          f"{s['F379_control_uncorrelated_rotor']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
