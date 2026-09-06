"""F331 — cluster decomposition, interacting 3-D BCC theory (completeness
row A10, closing F290's residual 1).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_cluster_interacting_3d.check_cluster_interacting_3d`
(record `F331-cluster-interacting-3d`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F331-cluster-interacting-3d
    casim test --id F331-cluster-interacting-3d --param use_correct_bz=false  # red (C1)
    casim test --id F331-cluster-interacting-3d --param g_above_gc=2.5        # red (C2, C3)

WHAT IS AND IS NOT CLAIMED.  F290 closed no-signalling (exact) and the
free-field causal cone (strict, machine precision) -- both untouched here.
Its residual 1 was that cluster decomposition itself was shown only for the
1-D, free-fermion case.  This module closes that residual in two honestly
separate pieces: (1) the free-fermion 3-D correlation length along the
(100)/(110) BCC axes, exact closed form, validated against the model's own
`bcc_dirac_dispersion` using the CORRECT reciprocal-lattice sampling (F267's
own generators -- the naive cubic FFT grid is the wrong Brillouin zone and
is demonstrated, not just asserted, to give a bad answer); and (2) a
lattice-native self-consistent NJL gap equation giving a dynamically
generated mass m*, with cluster decomposition in the INTERACTING theory
demonstrated at that m*.  The interacting piece is MEAN-FIELD (Hartree-type
self-consistency), the same scope F77 already carries for the continuum
NJL model -- not a full non-perturbative correlator, and not claimed as one.

Run standalone:  python3 tests/findings/test_F331_cluster_interacting_3d.py
"""
from __future__ import annotations

import json
import math
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_cluster_interacting_3d as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_cluster_interacting_3d()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F331 gate failed: " + json.dumps(res["checks"],
                                                             default=str)

    controls = [
        ({"use_correct_bz": False}, ("C1",)),
        ({"g_above_gc": 2.5}, ("C2", "C3")),
    ]
    print("\n  controls (each must go RED, and only where it should):")
    for kwargs, expect in controls:
        r = m.check_cluster_interacting_3d(**kwargs)
        red = [c["name"].split()[0] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red"
        assert set(red) == set(expect), \
            f"control {kwargs} went red at {red}, expected {list(expect)}"
        print(f"    {str(kwargs):<28} RED: {', '.join(red)}")

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    kappa_100 exact @ m=0.5             {s['F331_axis100_kappa_exact_at_m_free']:.4f}")
    print(f"    kappa_100 measured @ m=0.5           {s['F331_axis100_kappa_measured_at_m_free']:.4f}")
    print(f"    ratio                                {s['F331_axis100_ratio_at_m_free']:.4f}")
    print(f"    kappa_110 exact @ m=0.5              {s['F331_axis110_kappa_exact_at_m_free']:.4f}")
    print(f"    NJL coupling g                       {s['F331_gap_equation_coupling']:.4f}")
    print(f"    dynamical mass m*                    {s['F331_gap_equation_m_star']:.4f}")
    print(f"    interacting kappa_100(m*) exact       {s['F331_interacting_kappa_exact_at_m_star']:.4f}")
    print(f"    interacting kappa_100(m*) ratio       {s['F331_interacting_kappa_ratio_at_m_star']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
