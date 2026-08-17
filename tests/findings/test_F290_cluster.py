"""F290 — cluster decomposition and exact no-signalling (row A10).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_cluster.check_cluster` (record
`F290-cluster-decomposition`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F290-cluster-decomposition
    casim test --id F290-cluster-decomposition --param locality=nonlocal  # red
    casim test --id F290-cluster-decomposition --param cone_slack=-1      # red
    casim test --id F290-cluster-decomposition --param mass=0.0           # red

The ten checks:

  C1   a local operation on A leaves rho_B EXACTLY unchanged, on product,
       Bell/GHZ and generic entangled states, over twelve local unitaries.
  C1b  a NON-local unitary does move rho_B (control) -- so C1 is a statement
       about locality and not about partial traces.
  C2   outside the causal cone the reduced state at B is bit-for-bit identical.
  C2b  inside it, it is not (control).
  C2c  a generic Lieb-Robinson bound evaluated at the SAME points is nonzero.
       This is the CA-specific content: a generic spin system has an
       exponential tail outside the cone, an automaton has exactly zero.
  C2d  the cone is TIGHT -- measured at exactly 1 site per brick-wall layer,
       not quoted conservatively -- and reconciles numerically with F227's
       r > 4t (2 offsets per tick x 2 Heisenberg-evolved operators).
  C3   in the gapped ground state correlations decay exponentially.
  C3b  xi ~ Delta^-1: the MEASURED exponent is -0.93 over an 8x gap range with
       R^2 = 0.9994.  The continuum value is -1; the ~7% shortfall is a lattice
       correction this measurement does not resolve, and pushing to smaller
       mass makes it WORSE (-0.85) because xi then exceeds what a finite chain
       resolves.  The number quoted is the number measured.
  C3d  both sublattices give the same xi (the staggered mass makes |C(r)|
       alternate between two branches sharing a decay rate).
  C3c  the GAPLESS point is power-law, not exponential (control) -- so the
       exponential fit is discriminating between the two cases.

Run standalone:  python3 tests/findings/test_F290_cluster.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_cluster as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_cluster()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F290 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    controls = [
        ({"locality": "nonlocal"}, ("C1",)),
        ({"cone_slack": -1}, ("C2",)),
        ({"mass": 0.0}, ("C3", "C3b", "C3d")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_cluster(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    no-signalling residual             {s['A10_no_signalling_residual']:.2e}")
    print(f"    nonlocal control                   {s['A10_nonlocal_control']:.4f}")
    print(f"    max delta OUTSIDE the cone         {s['A10_max_delta_outside_cone']:.2e}")
    print(f"    Lieb-Robinson at the same points   {s['A10_lieb_robinson_at_same_points']:.4f}")
    print(f"    xi vs gap exponent                 {s['A10_xi_gap_exponent']:.4f}")
    print(f"    gapless: power r2 vs exp r2        {s['A10_gapless_power_fit_r2']:.4f} vs {s['A10_gapless_exp_fit_r2']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
