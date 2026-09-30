"""F395 -- Part D of docs/roadmaps/photon-fermion-coupling-rerun-prompt.md:
re-run Stage 5 (docs/roadmaps/photon-fermion-coupling.md) against F392's
fixed (circular) beam, re-measure F390's m_index=4 anomaly and off-axis
breakdown BEFORE theorising, and restate the roadmap's claim 1 per the
audit (docs/audits/2026-09-16-photon-fermion-momentum-investigation.md)
Sec.6.2: a lattice has only discrete translation symmetry, so a continuum-
style momentum conservation law is not achievable by any scheme -- what IS
exact is (A) charge conservation, (B) crystal-momentum translation
covariance, (C) a matched-order approach to the continuum.

Does NOT edit F384-F391. Does NOT re-derive Part C's curl symbol (deferred,
F394). F390's own gate record is untouched (verified bit-identical, both
functions keep beam_polarization="linear" as their default).

This file is the human-readable driver. The CONTRACT is the registry entry
`casim.engine.core.photon_fermion_push.check_stage5_circular_beam_rerun`
(record `F395-stage5-circular-beam-rerun`, tier gate), so this module
deliberately defines no `test_*` functions.

    casim test --id F395-stage5-circular-beam-rerun
    casim test --id F395-stage5-circular-beam-rerun --param beam_polarization=linear   # red (1/6 legs)

Six legs (see `photon_fermion_push.check_stage5_circular_beam_rerun`'s own
docstring for the full derivation):

    default_direction_still_confirmed          claim 2 re-confirmed with the
                                                fixed beam, on-axis default
    m4_anomaly_persists                        the m_index=4 sign flip is
                                                NOT explained by the beam fix
                                                (matter-side, per F391 Sec.3)
    offaxis_correlation_changes_with_circular_beam
                                                NEW: unlike F390/F391 (both
                                                linear-type beams, ~0
                                                correlation), the genuinely
                                                circular beam gives a
                                                nonzero, axis-dependent
                                                off-axis correlation
    target_A_charge_not_exact_but_bounded      claim 1 restated (A): NOT
                                                exact under the existing
                                                bridged architecture
    target_B_translation_covariance_exact      claim 1 restated (B): exact
                                                to machine precision
    target_C_order_still_mismatched            claim 1 restated (C): still
                                                O(g) vs O(g^2)-shaped, for a
                                                different reason than F389's
                                                self-sourced case (see
                                                finding)
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
    res = m.check_stage5_circular_beam_rerun()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(json.dumps({k: v for k, v in res.items() if k != "checks"}, indent=2))

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F395_stage5_circular_beam_rerun.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F395 gate failed: " + json.dumps(res["checks"], default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
