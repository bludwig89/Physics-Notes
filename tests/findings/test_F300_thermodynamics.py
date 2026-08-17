"""F300 — G10: lattice-native thermodynamics.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.thermodynamics.check_g10` (record
`F300-lattice-thermodynamics`, tier gate), so this file deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F300-lattice-thermodynamics
    casim test --id F300-lattice-thermodynamics --param linear_control=True     # red
    casim test --id F300-lattice-thermodynamics --param nonunitary_control=True # red

The fifteen checks are listed in the finding (F300 section 6).  The three that
matter for reading the result:

  G10-4   1/3 - w = (16 pi^2/1323) Theta^2, closed form vs Brillouin-zone
          quadrature.  This is the check that grades F297: the continuum
          radiation equation of state is a THEOREM of the derived dispersion,
          not an assumption, and the correction at the BBN bottleneck is 1e-44.
  G10-11  S_A(-t) rises exactly as S_A(+t) does.  The second law on this lattice
          is a statement about the initial condition and the coarse-graining --
          NOT about the dynamics.  Do not let a later citation strengthen it.
  G10-12  2 pi sqrt3 is neither ln(integer) nor n ln 2, so F190's own named next
          step ("show a cell carries e^(2 pi sqrt3) states") is impossible as
          written.  E9's grade does not move; its target does.

Two things this file will NOT assert, and each is deliberate:

  * **that the lattice thermalises.**  It does not, in the free sector, and
    G10-8/G10-10 are the proof (2N conserved branch occupations -> GGE).  The
    equation of state is the Gibbs measure ON the derived dispersion; reaching
    it dynamically needs F110's interacting sector.
  * **a Brillouin-zone shape.**  The paired photon's zone is an open geometric
    question.  G10-6b sidesteps it by measurement -- the radial cut is set by
    the Bose tail, not the zone -- and that is legitimate at Theta << 1 and
    nowhere else.

Run standalone:  python3 tests/findings/test_F300_thermodynamics.py
"""
from __future__ import annotations

import os
import sys


def _bootstrap():
    # Inside the function, not at module scope: a module-level sys.path preamble
    # is what `tools/audit_tests.py` counts as import-time work.
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import thermodynamics as m
    return m


def main() -> int:
    m = _bootstrap()

    res = m.check_g10()
    print("F300 / G10 — lattice-native thermodynamics\n")
    for c in res["checks"]:
        print(f"  {'PASS' if c['pass'] else 'FAIL'}  {c['id']:8s} {c['desc']}")
    assert res["all_pass"], f"only {res['n_pass']}/{res['n_total']} passed"

    controls = [
        ({"linear_control": True}, ("G10-3", "G10-4", "G10-5", "G10-6")),
        ({"nonunitary_control": True}, ("G10-7", "G10-9", "G10-10")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_g10(**kwargs)
        red = [c["id"] for c in r["checks"] if not c["pass"]]
        assert not r["all_pass"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<32} RED: {', '.join(red)}")

    e, sc, cc = res["eos"], res["scales"], res["cell"]
    mg = res["margins"]
    print("\n  headline numbers:")
    print(f"    C_u  closed 40 pi^2/441   {e['Cu_exact']:.7f}  measured {e['Cu_meas']:.7f}")
    print(f"    C_w  closed 16 pi^2/1323  {e['Cw_exact']:.7f}  measured {e['Cw_meas']:.7f}")
    print(f"    C_s  closed  4 pi^2/49    {e['Cs_exact']:.7f}  measured {e['Cs_meas']:.7f}")
    print(f"    ratio C_u/C_w = 15/2      {e['ratio_meas']:.6f}")
    print(f"    T_lattice                 {sc['T_lattice_K']:.4g} K "
          f"(tau = {sc['tau_s']:.4g} s)")
    print(f"    1/3 - w at BBN 1 MeV      {mg['BBN, 1 MeV (1.1605e10 K)']['third_minus_w']:.3g}")
    print(f"    w within 1% below         {mg['_T_at_1pc_softening_K']:.3g} K")
    print(f"    GGE approach              "
          f"{[round(r['plateau_over_GGE'], 4) for r in res['entropy']['B3_regions']]}")
    print(f"    time-reversal gap         "
          f"{res['entropy']['B4_time_reversal']['rel_gap']:.2g}")
    print(f"    2 pi sqrt3 -> W           {cc['implied_W']:.3f} "
          f"(distance to integer {cc['W_distance_to_integer']:.3f})")
    print(f"    capacity / requirement    {cc['capacity_over_requirement']:.3f}x")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
