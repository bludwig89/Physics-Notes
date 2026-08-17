"""F281 — the measurement problem on the lattice (completeness-2026-08-04 row A8,
with row A6's Born rule as a by-product).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_measurement.check_measurement` (record
`F281-measurement-pointer-born-rg`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven records
from file collection so nothing runs twice under two contracts.

    casim test --id F281-measurement-pointer-born-rg
    casim test --id F281-measurement-pointer-born-rg --param coupling=nonminimal
    casim test --id F281-measurement-pointer-born-rg --param flip_angle_over_pi=1.0
    casim test --id F281-measurement-pointer-born-rg --param block_b=1

Each of those three perturbations must go RED, on a different leg; they are
verified in `main()` below rather than being asserted only in prose.

The seventeen checks, by leg:

  M1  the pointer basis is FORCED by the model's own minimal coupling.
      M1a  [H_int, n̂(y)] = 0 exactly -- the U(1) wrap generator
           (u1_wrap_weyl_step_3d_bcc: psi(x) -> e^{-i q alpha(x)} psi(x)) is
           diagonal in site occupation, so einselection has no freedom left.
      M1b  the Zurek predictability sieve minimises AT the site basis, with
           zero entropy production there.
      M1c  spin is NOT einselected (control) -- correct physics: a spin
           superposition survives until amplified into a position difference.
      M1d  the kinetic term does NOT commute, so the quantum-measurement limit
           is stated rather than assumed.
      M1e  the decoherence factor has the closed form prod_j cos(g_j t).

  M2  the Born rule, on two independent legs.
      M2a  only ell^2 is conserved by a genuine BCC Weyl tick.
      M2b  the permutation control conserves every ell^p, so M2a is a statement
           about mixing rather than about ell^p.
      M2c  the "swap" is a genuine flip and not a global phase.  This is the
           defect the first draft of this module actually had, and it made two
           checks pass vacuously; it is now asserted.
      M2d  equal amplitudes are envariant under a native swap/counter-swap.
      M2e  UNEQUAL amplitudes are NOT envariant (control) -- max over every
           u_E of the overlap is 2 c0 c1 < 1.  This is the crux.
      M2f  fine-graining into M equal branches gives p_k = |c_k|^2.
      M2g  the same over Q, with a uniform-fine-graining control that fails.

  M3  classicality as a block-spin RG statement.
      M3a  the closed-form Dirichlet eigenvalue matches the model's own R_b.
      M3b  populations are MARGINAL: lambda(k=0) = 1, coarse charge exact.
      M3c  coherence at generic k is suppressed.
      M3d  the RG exponent is -2 per dimension, -6 in 3-D -- the same leading
           order as the F130 LIV operators.
      M3e  long-wavelength coherence SURVIVES (control), so R_b is selective
           rather than destructive.

Run standalone:  python3 tests/findings/test_F281_measurement.py
"""
from __future__ import annotations

import json
import os
import sys


def _bootstrap():
    """Path preamble + import, INSIDE a function on purpose (see F280's note:
    `tools/audit_tests.py` counts any module-level call as import-time work)."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.interactions import qi_measurement as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_measurement()
    for c in res["checks"]:
        print(f"  [{'PASS' if c['ok'] else 'FAIL'}] {c['name']}  -> {c['value']}")
    print(f"\n  {res['n_pass']}/{res['n_total']} PASS")
    assert res["passed"], "F281 gate failed: " + json.dumps(res["checks"],
                                                            default=str)

    # ------------------------------------------------------------------
    # The three declared controls MUST go red, each on its own leg (D9).
    # A record whose verification cannot fail is not a test.
    # ------------------------------------------------------------------
    controls = [
        ({"coupling": "nonminimal"}, "M1"),
        ({"flip_angle_over_pi": 1.0}, "M2"),
        ({"block_b": 1}, "M3"),
    ]
    print("\n  controls (each must go RED on its own leg):")
    for kwargs, leg in controls:
        r = m.check_measurement(**kwargs)
        red = [c["name"] for c in r["checks"] if not c["ok"]]
        assert not r["passed"], f"control {kwargs} did NOT go red -- the {leg} " \
                                "checks cannot fail, which makes them worthless"
        assert all(nm.startswith(leg) for nm in red), \
            f"control {kwargs} went red outside {leg}: {red}"
        print(f"    {str(kwargs):<32} RED on {len(red)} {leg} check(s): "
              + ", ".join(nm.split()[0] for nm in red))

    s = res["summary"]
    print("\n  headline numbers:")
    print(f"    pointer commutator                  {s['M1_minimal_coupling_commutator']}")
    print(f"    sieve entropy at the site basis     {s['M1_sieve_S_at_site_basis']:.2e}")
    print(f"    ell^2 change under a real BCC tick  {s['M2_lp2_bcc_step_change']}")
    print(f"    p_k - |c_k|^2                       {s['M2_p_minus_born']:.2e}")
    print(f"    coherence RG exponent (3-D)         {s['M3_exponent_3d']}")
    print(f"    log10 recurrence, a mole of cells   {s['M1_recurrence_log10_ticks_mole']:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
