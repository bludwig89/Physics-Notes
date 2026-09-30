"""F392 -- the beam-polarization fix (Part A of docs/roadmaps/photon-fermion-
coupling-rerun-prompt.md, implementing docs/audits/2026-09-16-photon-fermion-
momentum-investigation.md §2/§8 step 1).

`gauge.photon.build_beam_packet` originally placed E and B in the SAME
Cartesian component (E and B share `pol_axis`), so E||B pointwise and the
Poynting momentum Sigma E x B vanished identically -- F390's entire momentum-
conservation test ran against a field with no momentum to give. This finding
adds a `polarization="circular"` option (complex circular polarization,
e_hat = (e1 + i*e2)/sqrt(2)) that makes F = E + iB a genuine null Riemann-
Silberstein field (F.F=0, i.e. |E|=|B| and E _|_ B -- references/lattice-
conservation-laws-research-review.md Sec.8), while the default
`polarization="linear"` stays bit-identical to every existing call site
(verified against git HEAD).

This file is the human-readable driver. The CONTRACT is the registry entry
`casim.engine.gauge.photon.check_beam_polarization_fix` (record
`F392-beam-polarization-null-fix`, tier gate), so this module deliberately
defines no `test_*` functions -- `tests/conftest.py` hides entry-driven
records from file collection so nothing runs twice under two contracts.

    casim test --id F392-beam-polarization-null-fix
    casim test --id F392-beam-polarization-null-fix --param null_check_polarization=linear   # red (4/6 legs)

Six legs (see `photon.check_beam_polarization_fix`'s own docstring for the
full derivation of each):

    null_condition_holds                    |E.B|/(||E||*||B||) < 1e-12
    equal_magnitude_holds                    |E|-|B||/|E| < 1e-12
    momentum_nonzero_and_aligned             |Sigma ExB| > 0, cos(P,khat) > 0.99
    default_config_magnitude_matches_audit   |Sigma ExB| = 75.126 at the
                                              audit's own L=16, sigma=3.0,
                                              axis=0, m=2 configuration
    momentum_conserved_under_free_propagator rel. drift < 5e-15 over 40
                                              ticks of photon_step_spectral
    linear_mode_bit_identical_to_default     the unchanged default mode is
                                              untouched by this fix
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import photon as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_beam_polarization_fix()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  worst_null_condition_ratio={res['worst_null_condition_ratio']:.3e}  "
          f"worst_magnitude_diff_ratio={res['worst_magnitude_diff_ratio']:.3e}  "
          f"worst_cos_P_khat={res['worst_cos_P_khat']:.6f}  "
          f"default_config_momentum_magnitude={res['default_config_momentum_magnitude']:.6f}  "
          f"momentum_drift_40_ticks={res['momentum_drift_40_ticks']:.3e}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F392_beam_polarization_null_fix.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F392 gate failed: " + json.dumps(res["checks"], default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
