"""F393 -- Part B of docs/roadmaps/photon-fermion-coupling-rerun-prompt.md:
the missing curl(grad phi)=0 gate leg for `charge_coupling.bcc_curl_symbol`.

Discrete exterior calculus gives two identities from d.d=0: div(curl A)=0
(VACUOUS -- true for any vector field C under a cross product; this is what
the codebase's existing no-monopole gate, i*Chat.B=0, already tests) and
curl(grad phi)=0 (the one that actually constrains C, requiring C parallel
to G; this was never tested before this finding). bcc_curl_symbol fails the
second identity maximally: mean |CxG|/(|C||G|) ~ 0.74 against either
gradient symbol tested.

This finding does NOT fix bcc_curl_symbol (that is Part C's decision,
possibly a separate session) -- it makes the defect visible and monitored.
The asserted numbers are the MEASURED, DEFECTIVE values, not a target: a
future change to this leg's numbers means the symbol's defect changed
shape, not that a working curl broke.

This file is the human-readable driver. The CONTRACT is the registry entry
`casim.engine.gauge.charge_coupling.check_curl_grad_identity_diagnostic`
(record `F393-curl-grad-identity-diagnostic`, tier gate), so this module
deliberately defines no `test_*` functions.

    casim test --id F393-curl-grad-identity-diagnostic
    casim test --id F393-curl-grad-identity-diagnostic --param curl_symbol=true   # red (5/7 legs)

Seven legs (see `charge_coupling.check_curl_grad_identity_diagnostic`'s own
docstring for the full derivation):

    matches_known_defect_spectral_max        |CxG|/(|C||G|) max = 1.000000,
                                              G = k (spectral gradient)
    matches_known_defect_spectral_mean       same, mean = 0.741692
    matches_known_defect_forward_diff_max    max = 1.000000, G_j = e^{ik_j}-1
    matches_known_defect_forward_diff_mean   mean = 0.707173
    onaxis_reflection_x_plus_one              Chat(k).khat = +1 on x, all m
    onaxis_reflection_y_minus_one              Chat(k).khat = -1 on y, all m
    onaxis_reflection_z_plus_one              Chat(k).khat = +1 on z, all m
"""
import json
import os
import sys


def _bootstrap():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "src"))
    from casim.engine.gauge import charge_coupling as m
    return m


def main() -> int:
    m = _bootstrap()
    res = m.check_curl_grad_identity_diagnostic()
    for name, ok in res["checks"].items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n  {res['n_pass']}/{res['n_checks']} PASS")
    print(f"  measured={json.dumps(res['measured'])}")

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "test-results",
        "F393_curl_grad_identity_diagnostic.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2, default=str)
    print(f"  wrote {out}")

    assert res["ok"], "F393 gate failed: " + json.dumps(res["checks"], default=str)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
