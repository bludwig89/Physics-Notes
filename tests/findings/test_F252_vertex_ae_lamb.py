#!/usr/bin/env python3
"""
test_F252_vertex_ae_lamb.py — F252: the one-loop QED vertex correction
Lambda^m(p,p'), the electron anomalous moment a_e, and the hydrogen Lamb shift.

Gates (exactness first):
  V1  Ward-Takahashi  q_m Lambda^m = S^{-1}(p') - S^{-1}(p)   exact (sympy), Z1=Z2
  V2  a_e = F_2(0) = alpha/2pi (Schwinger)                    exact param integral
  V3  Uehling coefficient -4/15 from the F251 bubble low-q     exact (sympy)
  V4  Lamb shift 2s_{1/2}-2p_{1/2} lifted toward 1057.845 MHz  quantitative

Run:  python3 tests/findings/test_F252_vertex_ae_lamb.py --json out.json
Test: pytest -q tests/findings/test_F252_vertex_ae_lamb.py
"""
from __future__ import annotations
import os, sys, json, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.interactions import qed_vertex_loop as vx  # noqa: E402


def run_all():
    wt = vx.wt_identity_symbolic()
    ae = vx.ae_schwinger_symbolic()
    ueh = vx.uehling_coefficient_symbolic()
    lamb = vx.lamb_shift()

    checks = {
        "V1_ward_takahashi": {
            "quantity": "q_m Lambda^m = S^{-1}(p') - S^{-1}(p) (fixes Z1=Z2)",
            "tier": "exact", "clifford": wt["clifford_2eta"],
            "pass": bool(wt["gate_pass"]),
        },
        "V2_ae_schwinger": {
            "quantity": "a_e = F_2(0) = alpha/2pi",
            "parametric_integral": ae["parametric_integral"],
            "F2_0_over_alpha": ae["F2_0_over_alpha_symbolic"],
            "a_e_model": ae["a_e_schwinger"], "a_e_measured": ae["a_e_measured"],
            "rel_err_leading": ae["rel_err_leading"], "tier": "exact",
            "pass": bool(ae["gate_pass"] and ae["rel_err_leading"] < 2e-3),
        },
        "V3_uehling_coefficient": {
            "quantity": "Uehling S-state coefficient from F251 bubble low-q",
            "moment": ueh["moment_x2_1mx2"],
            "uehling_coeff": ueh["uehling_S_state_coeff"], "tier": "exact",
            "pass": ueh["uehling_S_state_coeff"] == "-4/15",
        },
        "V4_lamb_shift": {
            "quantity": "2s_{1/2}-2p_{1/2} Lamb shift (degeneracy lifted)",
            "dirac_degenerate": lamb["dirac_degenerate"],
            "self_energy_MHz": lamb["self_energy_2s_minus_2p_MHz"],
            "vacuum_pol_MHz": lamb["vacuum_pol_uehling_MHz"],
            "total_MHz": lamb["total_lamb_MHz"],
            "measured_MHz": lamb["measured_MHz"],
            "fraction_of_measured": lamb["fraction_of_measured"],
            "tier": "quantitative",
            "pass": bool(lamb["degeneracy_lifted"]
                         and 0.98 < lamb["fraction_of_measured"] < 1.02),
            "note": "leading order; residual ~5.6 MHz is higher-order QED.",
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F252",
        "title": "One-loop QED vertex: a_e = alpha/2pi and the Lamb shift",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "verdict": ("Ward-Takahashi and a_e=alpha/2pi exact; Uehling coefficient "
                    "derived from F251; Lamb shift lifts the Dirac degeneracy to "
                    "99.5% of the measured 1057.845 MHz (leading order)."),
    }
    return {"summary": summary,
            "detail": {"wt": wt, "ae": ae, "uehling": ueh, "lamb": lamb},
            "checks": checks}


def test_F252_vertex_ae_lamb():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"
    assert res["detail"]["ae"]["parametric_integral"] == "1"
    assert res["detail"]["wt"]["wt_residual_zero"] is True


def _print(res):
    s = res["summary"]
    print("=" * 74)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 74)
    for name, c in res["checks"].items():
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {name:26s} {c['quantity']}")
    print("-" * 74)
    print(f"  {s['passed']}/{s['checks']} pass   |   {s['verdict']}")
    print("=" * 74)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    res = run_all()
    _print(res)
    if args.json:
        with open(args.json, "w") as f:
            json.dump(res, f, indent=2, default=str)
        print(f"\nwrote {args.json}")
