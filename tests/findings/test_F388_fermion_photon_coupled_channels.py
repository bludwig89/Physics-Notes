"""F388 -- the coupled em_photon/fermion_em channels (Stage 4,
docs/roadmaps/photon-fermion-coupling.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.core.coupled.check_fermion_photon_backreaction` (record
`F388-fermion-photon-coupled-channels`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F388-fermion-photon-coupled-channels
    casim test --id F388-fermion-photon-coupled-channels --param q=0                     # red
    casim test --id F388-fermion-photon-coupled-channels --param use_naive_sourcing=true # red

Seven legs (see `coupled.check_fermion_photon_backreaction`'s own docstring
for the full description of each):

    channels_registered                        em_photon/fermion_em both
                                                registered
    photon_pair_accepts_bcc                    the topology-tag fix
    ordering_pretick_posttick_exact            registration-order contract
    self_sourced_field_momentum_trivially_zero P_field=0 by construction,
                                                current-only source
    seeded_photon_gives_sustained_push         a real, non-oscillating push
    norm_drift_bounded                         stability sanity floor
    no_monopole_fix_holds_with_dynamical_current
                                                F387's split-sourcing fix,
                                                now verified under a LIVE
                                                (not static) current
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.core import coupled as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_fermion_photon_backreaction()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  matter_push_end={res['matter_push_end']:.3e}  "
          f"gauss_for_b_residual_seeded={res['gauss_for_b_residual_seeded']:.3e}  "
          f"norm_drift={res['norm_drift']:.3e}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F388_fermion_photon_coupled_channels.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F388 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
