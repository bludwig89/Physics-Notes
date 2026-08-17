"""F311 — completeness gap #5: the three numbers no report had re-derived.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.derive_gap5_adjudication.check_gap5` (record
`F311-gap5-adjudication`, tier gate), so this file deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F311-gap5-adjudication
    casim test --id F311-gap5-adjudication --param two_loop_control=True   # red
    casim test --id F311-gap5-adjudication --param volatile_control=True   # red

`docs/status/completeness-2026-08-07.md` gap #5 listed three items, each on its
third consecutive report with nothing recorded against it.  **All three turned
out to be instrument or bookkeeping artifacts rather than physics defects**, and
that common shape is the result -- the individual legs are each smaller than it.

  A1     B9's Delta_alpha(M_Z) is UNTOUCHED by S12-F277, proved by reinstating
         the removed refold rather than by reading the call graph: Pi4
         (`leptonic_running`, the analytic one-loop sum, which is where B9's
         number comes from) returns a bit-identical payload, while Pi3
         (`lattice_b0_consistency`, which is what F277 actually fixed) moves its
         spread by three orders.  S12 is a PARTIAL supersession.

  A2/A3  And the 0.24 % is not an error -- it is the two-loop leptonic term the
         one-loop formula omits by construction.  Kallen-Sabry gives 0.77568e-4
         against a measured residual of 0.77072e-4 (100.6 % of it) and the
         published 0.77621e-4 (0.07 %).  Adding it takes B9 from 0.245 % to
         0.00158 %, a 155x improvement at zero fitted parameters.

  B1     Three of the ten `candidate` baselines were permanently red because
         `casim.baselines._VOLATILE_RE` did not admit a LEADING UNDERSCORE, so
         `_seconds` -- pure wall-clock -- was diffed as physics.  That regex had
         already been patched twice for this same class (`total_elapsed_s`,
         `wall_seconds`, both in its own comments); this is the third instance.
         Fixed, and F182/F184/F200 now report "reproduced HEAD exactly".

  B2/B3  All ten re-run and disposed: 5 clean, 3 timing, 1 float-floor churn,
         1 undeclared input dependency.  **Zero regressions, zero
         supersessions** -- every `candidate` entry blamed physics for an
         instrument defect.

  C      The two Lambda pictures are SEQUENTIAL, not parallel.  F192 (04:50)
         records "all four candidate cancellations remain underived"; F193
         (17:35, the same day) closes candidate (i), and F196 then derived the
         p=2 exponent F193 named as its obstruction.  F192's V3 was true when
         written and has been false since that afternoon.  Its w = -1 sign
         result is not contradicted but VACUOUS under F193 (rho_vac = 0 exactly
         makes w = p/rho a 0/0), and its 1e121 overshoot double-counts the very
         mode sum F79 uses to induce 1/G.

Three things this file will NOT assert, each deliberate:

  * **that leg C derives anything.**  It is an adjudication between two existing
    findings plus one structural argument; Omega_Lambda ~ 0.685 is untouched and
    stays exactly where F241 left it.
  * **that the two-loop formula is derived here.**  It is the standard
    Kallen-Sabry leading form, cited.  What is new is the identification of the
    model's own residual with it.
  * **that the ten baselines' physics is correct.**  B measures ten artifacts;
    it says nothing about the findings inside them.

Run standalone:  python3 tests/findings/test_F311_gap5_adjudication.py
"""

from __future__ import annotations

import json

from casim.engine.interactions.derive_gap5_adjudication import check_gap5


def main() -> dict:
    res = check_gap5()
    print(json.dumps(res["checks"], indent=2, sort_keys=False))
    print(f"\n{sum(res['checks'].values())}/{res['n_checks']} PASS")

    a1, a23 = res["A1_refold_independence"], res["A23_two_loop"]
    b23, c = res["B23_baseline_triage"], res["C_lambda_adjudication"]
    print(f"\nA1  Pi4 payload identical under the reinstated refold: "
          f"{a1['pi4_whole_payload_identical']};  Pi3 spread x"
          f"{a1['pi3_spread_ratio']:.0f}")
    print(f"A2  two-loop {a23['two_loop_total']:.6e} vs residual "
          f"{a23['residual_after_one_loop']:.6e}  = "
          f"{100*a23['two_loop_over_residual']:.1f} % of it "
          f"(lit. agreement {100*a23['two_loop_vs_literature_rel']:.3f} %)")
    print(f"A3  B9: {100*a23['one_loop_rel_err']:.3f} % -> "
          f"{100*a23['two_loop_rel_err']:.5f} %   ({a23['improvement_factor']:.0f}x)")
    print(f"B   {b23['n_candidates']} candidates: {b23['counts']};  "
          f"regressions {b23['n_regressions']}, supersessions {b23['n_supersessions']}")
    print(f"C   F193 postdates F192 by {c['hours_between']:.2f} h; "
          f"F192 V3 stale = {c['f192_V3_is_stale']}; entails {c['entails']}; "
          f"double-count gap {c['dex_between']:.2f} dex")

    # This file carries its own failure mode rather than delegating all of it to
    # the entry, so it is in neither delta of `audit_tests --ratchet`.
    assert res["all_pass"], (
        f"only {sum(res['checks'].values())}/{res['n_checks']} legs passed")
    assert a1["pi4_whole_payload_identical"], \
        "A1: the B9 number must be provably untouched by S12-F277"
    assert 0.95 < a23["two_loop_over_residual"] < 1.05, \
        "A2: the two-loop term must account for the one-loop residual"
    assert a23["improvement_factor"] > 100.0, \
        "A3: adding two loops must improve B9 by more than 100x"
    assert b23["zero_regressions"] and b23["n_candidates"] == 10, \
        "B: all ten candidates disposed, and none of them a regression"
    assert c["entails"] == "F193/F196/F241" and c["f192_V3_is_stale"], \
        "C: the adopted F178 law must entail exactly one Lambda picture"
    return res


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    result = main()
    out = results_path("F311_gap5_adjudication.json")
    with open(out, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote", out)
