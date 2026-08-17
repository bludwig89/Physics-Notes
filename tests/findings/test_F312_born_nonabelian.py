"""F312 — A6: Gleason's premises on SU(2)_L and SU(3)_c, and the Schur reduction.

Human-readable driver.  The CONTRACT is the registry entry
`casim.engine.interactions.qi_born_nonabelian.check_born_nonabelian` (record
`F312-born-nonabelian`, tier gate), so this file deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from file
collection so nothing runs twice under two contracts.

    casim test --id F312-born-nonabelian
    casim test --id F312-born-nonabelian --param abelian_control=True       # red
    casim test --id F312-born-nonabelian --param break_singlet=True         # red
    casim test --id F312-born-nonabelian --param contextual_coupling=True   # red

Rubric row **A6** was downgraded `EXACT -> PARTIAL` on F304's own residual 3:
non-contextuality, a *premise* of the Born-rule derivation, was proved for the
U(1) wrap generator only, and "the SU(2)_L and SU(3)_c commutators are not
written out".  This closes that seam -- and closes it with **one theorem** rather
than two more special cases, because the reason the internal index cannot
disturb Gleason is Schur's lemma, which does not know which group it was handed.

The legs that matter for reading the result:

  G1/G2  The commutator, written out: [J^a(x), J^b(y)] = i delta_xy f^abc J^c(x).
         Two facts, and the SECOND is load-bearing.  The algebra closes (SU(2)
         residual literally 0.0, f = Levi-Civita literally 0.0; SU(3) 1.1e-16,
         f_123 = 1, f_458 = sqrt3/2).  And `delta_xy` holds **exactly** -- the
         off-site commutator is literally 0.0 for both groups, so the entire
         non-Abelian structure is INTRA-SITE.  A measurement context is a choice
         of basis on the pointer factor, which is an inter-site object; the
         structure constants never leave one site, so they cannot reach it.

  G3     The record is a gauge singlet: [J^a(x), n_hat(y)] = 0 literally, for
         every generator, site pair and group.  n_hat is the internal TRACE --
         occupation is what a cell holds, not what colour it holds -- so the
         pointer and gauge algebras commute elementwise by construction rather
         than by coincidence.

  G4/G5  F304's B2 measurement re-run with the sector genuinely present: five
         contexts sharing a ray, on Hilbert spaces of dimension 64 (SU(2)) and
         96 (SU(3)).  Weight spread literally **0.0** in both.

  G6     The general theorem.  sum_a T^a T^a is a multiple of the identity
         (deviation 0.0 and 2.2e-16) with the exact value (N^2-1)/2N = 3/4 and
         4/3, so an invariant frame function on H_p (x) V factorises and
         F304 sec.5's dichotomy applies unchanged -- for ANY compact group.

  G7     And the internal factor CLOSES F304's d=2 hole: dim = d_p * N, so
         **SU(3)_c clears Gleason's d >= 3 with no reference to the pointer at
         all**.  The qubit exception is unreachable in any charged sector.

  G8/G9  Two premises the U(1) case never had to check, because a phase is a
         scalar: that the link step is linear and unitary on V, and that a local
         gauge ROTATION is not a context.  Both machine-zero.

Three things this file will NOT assert, each deliberate:

  * **that Gleason's theorem is proved here.**  It is F304 sec.5's; this supplies
    its premises on the two non-Abelian factors plus the reduction that makes the
    internal index irrelevant to it.
  * **that A6's other residual is closed.**  The Cooke-Keane-Moran regularity
    lemma (F304 sec.5.5) is untouched and stays named.
  * **that coloured superposition is an asymptotic observable.**  Physical
    asymptotic states are colour singlets (F86/F110); G8 is a statement about the
    rule's linearity on V.

Run standalone:  python3 tests/findings/test_F312_born_nonabelian.py
"""

from __future__ import annotations

import json

from casim.engine.interactions.qi_born_nonabelian import check_born_nonabelian


def main() -> dict:
    res = check_born_nonabelian()
    print(json.dumps(res["checks"], indent=2, sort_keys=False))
    print(f"\n{sum(res['checks'].values())}/{res['n_checks']} PASS")

    g1, g2 = res["G1_su2_current_algebra"], res["G2_su3_current_algebra"]
    g6, g7 = res["G6_schur_reduction"], res["G7_dimension_premise"]
    print(f"\nG1  SU(2)_L closure {g1['closure_residual']:.1e}, off-site "
          f"{g1['offsite_commutator_max']:.1e}, f == Levi-Civita "
          f"{g1['f_equals_levi_civita_residual']:.1e}")
    print(f"G2  SU(3)_c closure {g2['closure_residual']:.1e}, off-site "
          f"{g2['offsite_commutator_max']:.1e}, f_123 = {g2['f_123']:.6f}, "
          f"f_458 = {g2['f_458']:.10f} (sqrt3/2 = {g2['f_458_exact']:.10f})")
    print("G3  [J^a(x), n_hat(y)] = "
          + ", ".join(f"{k} {v['max_commutator']:.1e}"
                      for k, v in res["G3_singlet_record"].items()))
    for tag in ("G4_context_blindness_su2", "G5_context_blindness_su3"):
        v = res[tag]
        print(f"{v['leg']}  {v['group']}: weight spread {v['weight_spread']:.1e} "
              f"over {v['n_contexts']} contexts, dim {v['hilbert_dim']}")
    print("G6  Casimir "
          + ", ".join(f"{k} = {v['C2_value']:.6f} (exact {v['C2_exact']:.6f}, "
                      f"dev {v['deviation_from_multiple_of_identity']:.1e})"
                      for k, v in g6["per_group"].items()))
    print(f"G7  SU(3)_c clears d>=3 alone: "
          f"{g7['per_group']['SU(3)_c']['clears_gleason_d3_alone']}; "
          f"d=2 hole reachable when charged: "
          f"{g7['d2_hole_reachable_in_a_charged_sector']}")

    # This file carries its own failure mode rather than delegating all of it to
    # the entry, so it is in neither delta of `audit_tests --ratchet`.
    assert res["all_pass"], (
        f"only {sum(res['checks'].values())}/{res['n_checks']} legs passed")
    assert g1["delta_xy_holds"] and g2["delta_xy_holds"], \
        "G1/G2: the off-site commutator must vanish EXACTLY — that is the delta_xy"
    assert all(v["max_commutator"] < 1e-14 for v in res["G3_singlet_record"].values()), \
        "G3: the record observable must be a gauge singlet"
    assert (res["G4_context_blindness_su2"]["context_blind"]
            and res["G5_context_blindness_su3"]["context_blind"]), \
        "G4/G5: the weight must be blind to the context with the sector present"
    assert g6["all_schur"], \
        "G6: the Schur reduction is what makes this a theorem rather than two cases"
    assert g7["per_group"]["SU(3)_c"]["clears_gleason_d3_alone"], \
        "G7: colour alone must clear Gleason's dimension premise"
    return res


if __name__ == "__main__":                          # pragma: no cover
    from casim.engine.particles._results_path import results_path

    result = main()
    out = results_path("F312_born_nonabelian.json")
    with open(out, "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote", out)
