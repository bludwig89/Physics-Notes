"""F386 -- the A-field convention Stage 2's per-link U(1) step reads
(Stage 3, docs/roadmaps/photon-fermion-coupling.md).

This file is the human-readable driver.  The CONTRACT is the registry entry
`casim.engine.gauge.a_field_convention.check_a_field_convention` (record
`F386-a-field-convention`, tier gate), so this module deliberately defines no
`test_*` functions -- `tests/conftest.py` hides entry-driven records from
file collection so nothing runs twice under two contracts.

    casim test --id F386-a-field-convention
    casim test --id F386-a-field-convention --param use_accumulate_for_solve_check=true   # red

Seven legs (see `a_field_convention.check_a_field_convention`'s own docstring
for the full description of each):

    solve_is_purely_transverse                the Coulomb-gauge solve's A has
                                               zero C(k)-longitudinal content
    solve_curl_recovers_B                     i C x A_solve = B_T to FFT
                                               round-off (masked, F384-style)
    accumulate_inherits_longitudinal_content  A+=E, sourced only by F384's
                                               (purely longitudinal) current,
                                               ends up almost entirely
                                               longitudinal
    accumulate_longitudinal_content_grows_with_ticks
    solve_gives_zero_A_for_pure_charge_source the decisive contrast: with no
                                               real photon (B=0), solve
                                               correctly returns A=0 exactly
    ward_global_exact_for_pure_gradient       F385's own Ward mechanism,
                                               reused: a constant gauge
                                               function is exact
    ward_local_grows_with_wavelength_matches_F385
                                               a purely-longitudinal A (built
                                               as grad(chi)) shows the SAME
                                               already-disclosed O(a)
                                               local-Ward growth F385 found
                                               for a general A -- not a new,
                                               distinct physical push
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import a_field_convention as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_a_field_convention()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  solve_longitudinal_fraction={res['solve_longitudinal_fraction']:.3e}  "
          f"solve_curl_residual_masked={res['solve_curl_residual_masked']:.3e}  "
          f"accumulate_longitudinal_fraction_charge_only="
          f"{res['accumulate_longitudinal_fraction_charge_only']:.6f}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F386_a_field_convention.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F386 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
