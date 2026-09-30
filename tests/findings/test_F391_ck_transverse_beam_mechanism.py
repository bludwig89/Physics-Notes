"""F391 -- resolving F390's two structural gaps: does a genuinely Ĉ(k)-
transverse beam-construction helper fix the direction/anti-alignment
breakdown, and is Stage 5's Thomson-limit stretch goal now well-posed?
(docs/roadmaps/photon-fermion-coupling.md; docs/reviews/F390-review-
2026-09-15.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.em_photon_sourcing.check_ck_transverse_beam_mechanism`
(record `F391-ck-transverse-beam-mechanism`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F391-ck-transverse-beam-mechanism
    casim test --id F391-ck-transverse-beam-mechanism --param use_ck_beam=false   # red (2 legs)

Nine legs (see `em_photon_sourcing.check_ck_transverse_beam_mechanism`'s own
docstring and `findings/F391-ck-transverse-beam-mechanism.md` for the full
derivation of each):

    beam_exactly_ck_transverse                  the new beam has ~0
                                                 no-monopole residual
    beam_near_zero_longitudinal_leak            vs ~27.5% for F390's
                                                 original beam recipe
    curl_y_axis_antiparallel_180deg             Ĉ(k) is exactly *anti*-
                                                 parallel to k̂ along the
                                                 lattice's y-axis -- new,
                                                 not in F387's own table
    curl_z_axis_parallel_0deg                   contrast: z-axis (like x)
                                                 stays exactly aligned
    curl_y_axis_antiparallel_stable_with_L      a continuum-limit property,
                                                 not a finite-lattice artifact
    onaxis_correlation_holds_with_both_beams    F390's on-axis result
                                                 survives the fix unchanged
    m4_sign_flip_persists_with_both_beams       so does the m_index=4 flip
    offaxis_decorrelation_persists_with_both_beams
                                                 so does the off-axis
                                                 decorrelation -- the fix
                                                 does NOT close F390's gap
    push_direction_sensitive_to_fermion_spin_state
                                                 informational: the actual
                                                 candidate mechanism this
                                                 finding identifies but does
                                                 not derive
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import em_photon_sourcing as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_ck_transverse_beam_mechanism()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  longitudinal_leak_fraction={res['longitudinal_leak_fraction']:.6f}  "
          f"cos_beam_onaxis_new={res['cos_beam_onaxis_new']:.5f}  "
          f"cos_beam_m4_new={res['cos_beam_m4_new']:.5f}  "
          f"cos_beam_offaxis_new={res['cos_beam_offaxis_new']:.5f}  "
          f"spin_state_push_cos={res['spin_state_push_cos']:.5f}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F391_ck_transverse_beam_mechanism.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F391 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
