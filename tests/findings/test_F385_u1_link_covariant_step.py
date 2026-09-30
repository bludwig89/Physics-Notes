"""F385 — the per-link U(1) covariant BCC Weyl step, and its unitarity/
momentum-transfer fork adjudication (Stage 2, docs/roadmaps/
photon-fermion-coupling.md).

This file is the human-readable driver. The CONTRACT is the registry entry
`casim.engine.forks.gauge.u1_link_unitarity_forks.check_u1_link_forks`
(record `F385-u1-link-covariant-step`, tier gate), so this module
deliberately defines no `test_*` functions -- `tests/conftest.py` hides
entry-driven records from file collection so nothing runs twice under two
contracts.

    casim test --id F385-u1-link-covariant-step
    casim test --id F385-u1-link-covariant-step --param corrupt_a0=true   # red

Ten legs (see `u1_link_unitarity_forks.check_u1_link_forks`'s own docstring
and `findings/F385-u1-link-covariant-step.md` for the full derivation):

    reduces_to_free_{a,b,d}            A==0 -> bit-identical to weyl_step_3d_bcc
                                        for all three forks (W1.2 precedent)
    uniform_A_exact_unitary            spatially uniform A -> exact rigid
                                        k-shift, exactly unitary (analytic
                                        special case, verified bit-for-bit)
    ward_global_exact                  constant (global) gauge transform
                                        leaves the step exactly covariant
    ward_local_shrinks_with_wavelength local Ward residual grows with the
                                        gauge function's wavenumber (O(a)
                                        precedent, matching W1.4)
    norm_drift_is_O_qA                 fork (a)'s norm drift scales linearly
                                        with |qA| (log-log slope in [0.5,1.5])
    fork_d_exactly_conserves_norm      fork (d) (per-site renormalisation)
                                        conserves norm to machine precision
                                        for any A
    momentum_transfer_nonzero_all_forks  all three forks genuinely transfer
                                        matter momentum (the actual push)
    fork_d_preserves_momentum_signal   fork (d)'s exact norm conservation
                                        does not kill the momentum-transfer
                                        signal (same order of magnitude as
                                        fork a)
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.forks.gauge import u1_link_unitarity_forks as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_u1_link_forks()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  norm_drift_slope_fork_a={res['norm_drift_slope_fork_a']:.3f}  "
          f"ward_m1={res['ward_m1']:.3e}  ward_m4={res['ward_m4']:.3e}")
    print(f"  momentum_transfer_mag={res['momentum_transfer_mag']}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F385_u1_link_covariant_step.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F385 gate failed: " + json.dumps(res["checks"],
                                                         default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
