"""F303 — is F144's bare coupling centre-normalised?  No argument exists, and three candidates are closed.

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.derive_coupling_normalisation.check_coupling_normalisation`
(record `F303-coupling-normalisation`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven records
from file collection so nothing runs twice under two contracts.

    casim test --id F303-coupling-normalisation
    casim test --id F303-coupling-normalisation --param assume_three_bond_loop=True  # must go red
    casim test --id F303-coupling-normalisation --param scheme_residual=20.0         # must go red

WHAT THIS SETTLES AND WHAT IT DOES NOT.  F299 moved the open item from F110 to
F144: either an argument for why the model's bare coupling is centre-normalised
while its running is SU(N_c), or acceptance that 1/(16 pi) is a coincidence.
This finding looks for that argument and does not find one.  What it DOES
deliver is three closed candidates and a located break: F144 steps 1-2 survive
(the circularity lemma is group-blind), step 3 breaks (reading the rotor's E^2
spectrum as integer m^2 rather than C_2(R)).  It does NOT decide between "F144's
0.083% is a coincidence" and "the colour sector is not SU(N_c)-normalised".

  N1   the rotor lemma's residual factorises as (r-1) x sine with r = a/b, so
       orthogonality at generic t holds iff a = b whatever the scale.  The lemma
       constrains a RATIO and carries no representation content -- which is why
       chi = 1 survives H1/H2 and step 3 is the step that breaks.
  N2   at N=3 the model's integer ladder and the SU(3) ladder are EXACTLY
       proportional with constant C_F = 4/3, so the dispute is one rational
       number and not a matter of interpretation.
  N3   CANDIDATE CLOSED (geometry): the only reconciliation keeping both
       g_s = 1/2 and the Casimir is a plaquette with n links where n C_F = 4,
       i.e. n = 3.  The BCC nearest-neighbour graph has NO closed 3-bond loop --
       each component of a sum of three (+-1,+-1,+-1) hops is odd -- verified by
       parity AND by exhaustive enumeration (0 of 8^3 triples close, 216 of 8^4
       quadruples do).  n = 4 is derived geometry and cannot be traded.
  N3b  ... and the n it needed was exactly 3, which at n = 3 would even have
       forced N_c = 3 UNIQUELY (other root -1/3).  Recorded as closed so it is
       not re-derived as live.
  N4   CANDIDATE CLOSED (scheme): the Casimir shifts 1/alpha_0 by 16.755, which
       is 26x F144's entire MEASURED A4 residual of 0.64, and demands
       Lambda_scheme/Lambda_rule = 3.4e6 against 1.78 measured and 28.81 for the
       Wilson action.  Not a scheme constant.
  N5   CANDIDATE CLOSED (Cartan): every weight of the SU(3) fundamental has
       |lambda|^2 = 1/3 exactly, giving alpha_0 = 3/(16 pi) and a Landau pole
       ABOVE M_Z.  Excluded outright, and in the opposite direction.
  N6   H1 lands alpha_s(M_Z) = 0.1186 (+0.5% at one loop) and H2 gives 0.0397
       (-66.4%).  This is falsification-grade, not a tension.
  N7   the data demands chi = 1.000828 -- the DERIVED chi = 1 to 0.083% -- where
       the Casimir reading's chi = 1/C_F = 0.75 misses by 33%.

Run standalone:  python3 tests/findings/test_F303_coupling_normalisation.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import derive_coupling_normalisation as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_coupling_normalisation()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F303 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"assume_three_bond_loop": True}, ("N3",)),
        ({"scheme_residual": 20.0}, ("N4",)),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_coupling_normalisation(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<38} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    argument found                   {s['F303_argument_found']}")
    for c in s["F303_candidates_closed"]:
        print(f"      closed: {c}")
    print(f"    chi required by the data         {s['F303_chi_required']:.6f}")
    print(f"    chi derived (circularity)        {s['F303_chi_derived']:.6f}")
    print(f"    chi under the Casimir reading    {s['F303_chi_casimir_reading']:.6f}")
    print(f"    alpha_s(M_Z)  H1 / H2            {s['F303_alpha_s_MZ_H1']:.5f} / {s['F303_alpha_s_MZ_H2']:.5f}")
    print(f"    Casimir shift in 1/alpha_0       {s['F303_casimir_shift_inv_alpha']:.4f}")
    print(f"      vs F144 A4 residual 0.64       {s['F303_scheme_ratio']:.1f}x")
    print(f"      Lambda ratio demanded          {s['F303_lambda_ratio_demanded']:.3e}")
    print(f"    closed 3-bond BCC loops          {s['F303_n_closed_3_bond_loops']}")
    print(f"    minimal gauge loop (bonds)       {s['F303_minimal_loop_bonds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
