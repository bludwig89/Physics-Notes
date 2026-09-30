"""F390 -- the photon-fermion push scenario and the roadmap's physics claims
(Stage 5, docs/roadmaps/photon-fermion-coupling.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.core.photon_fermion_push.check_photon_fermion_push` (record
`F390-photon-fermion-push`, tier gate), so this module deliberately defines
no `test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F390-photon-fermion-push
    casim test --id F390-photon-fermion-push --param use_radiative_current=false  # red (3 legs)
    casim test --id F390-photon-fermion-push --param q=0                          # red (all legs)

Eight legs (see `photon_fermion_push.check_photon_fermion_push`'s own
docstring for the full description of each):

    push_direction_aligned_with_beam            claim 2, ON-AXIS ONLY
    field_momentum_zero_at_zero_coupling        claim 1's zero-coupling floor
    field_gains_real_momentum_when_radiative_current_on
                                                 F389's current genuinely radiates
    field_and_matter_momentum_nearly_antiparallel
                                                 a positive partial result, ON-AXIS ONLY
    momentum_conservation_not_exact_at_default_coupling
                                                 claim 1: honestly NOT achieved
    closure_residual_has_interior_minimum       a reproducible (not universal) minimum
    direction_correlation_breaks_down_off_axis  disclosed limitation, gated not hidden
    antiparallel_result_inverts_off_axis        disclosed limitation, gated not hidden

Claim 3 (magnitude, Delta p = Delta E / c) and claim 4 (the Thomson-limit
stretch goal) are NOT gated here -- see findings/F390-photon-fermion-push-
scenario.md Sec.4-5 for why, and what was measured instead. Found in review
(2026-09-15): the on-axis "direction confirmed" and "nearly anti-parallel"
results do NOT generalize off-axis -- both collapse to no correlation or
INVERT sign for an off-axis beam, plausibly traced to F387's documented
C(k) axis anisotropy. This is now gated explicitly (the last two legs
above) rather than left an undisclosed gap.
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.core import photon_fermion_push as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_photon_fermion_push()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  matter_push_norm={res['matter_push_norm']:.5f}  "
          f"field_push_norm={res['field_push_norm']:.5f}  "
          f"cos_beam_direction={res['cos_beam_direction']:.4f}  "
          f"cos_matter_field={res['cos_matter_field']:.4f}  "
          f"conservation_residual={res['conservation_residual']:.4f}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F390_photon_fermion_push.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F390 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
