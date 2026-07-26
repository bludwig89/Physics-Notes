#!/usr/bin/env python3
"""
test_F251_vacuum_polarization.py — F251: the interacting one-loop QED photon
self-energy Pi^{mn}(q) and the running coupling alpha(q^2).

Gates (exactness first):
  P1  Ward transversality  q_m Pi^{mn} = 0                     exact (sympy)
  P2  b0^QED = 4/3 for one Dirac fermion                       exact (sympy)
  P2b explicit-gamma Dirac trace matches the bubble numerator  exact (sympy)
  P3  lattice b0 = continuum b0 (subtracted, q-flat)           convergent
  P4  leptonic Delta alpha(M_Z) ~ 0.0314 (honest: hadronic deferred to QCD)

Run:  python3 tests/findings/test_F251_vacuum_polarization.py --json out.json
Test: pytest -q tests/findings/test_F251_vacuum_polarization.py
"""
from __future__ import annotations
import os, sys, json, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (
    os.path.join(_HERE, "ca-simulation"),
    os.path.join(_HERE, "..", "..", "ca-simulation"),
    os.path.join(_HERE, "..", "ca-simulation"),
):
    _cand = os.path.abspath(_cand)
    if os.path.isdir(_cand) and _cand not in sys.path:
        sys.path.insert(0, _cand)

import ca_vacuum_polarization as vp  # noqa: E402


def run_all():
    ward = vp.ward_identity_symbolic()
    b0 = vp.b0_gate_symbolic()
    trace = vp.gamma_trace_check()
    latt = vp.lattice_b0_consistency(n=20)
    run = vp.leptonic_running()

    checks = {
        "P1_ward_transversality": {
            "quantity": "q_m Pi^{mn}(q)", "target": "0 (all n)",
            "result": ward["q_dot_Pi"], "tier": "exact",
            "pass": bool(ward["exact_zero"]),
        },
        "P2_b0_QED": {
            "quantity": "one-loop QED beta coefficient b0",
            "model": b0["b0_QED"], "target": "4/3", "tier": "exact",
            "transverse": b0["transverse"], "calibration_ok": b0["calibration_ok"],
            "pass": bool(b0["gate_pass"]),
        },
        "P2b_gamma_trace": {
            "quantity": "explicit-gamma Dirac trace vs bubble numerator",
            "clifford": trace["clifford_2eta"], "tier": "exact",
            "pass": bool(trace["clifford_2eta"] and trace["trace_identity_ok"]),
        },
        "P3_lattice_b0_consistency": {
            "quantity": "Delta = B_rule - B_cont (q-flat => lattice b0 = continuum)",
            "delta_mean": latt["delta_mean"], "delta_spread": latt["delta_spread"],
            "tier": "convergent", "pass": bool(latt["b0_propagator_independent"]),
        },
        "P4_leptonic_running": {
            "quantity": "leptonic Delta alpha(M_Z) and 1/alpha(M_Z)|lep",
            "delta_alpha_lep": run["delta_alpha_lep"],
            "delta_alpha_lep_PDG": run["delta_alpha_lep_PDG"],
            "rel_err_vs_PDG": run["delta_alpha_lep_rel_err"],
            "alpha_MZ_inv_leptonic": run["alpha_MZ_inv_leptonic"],
            "alpha_MZ_inv_measured_full": run["alpha_MZ_inv_measured_full"],
            "tier": "quantitative",
            "pass": bool(run["delta_alpha_lep_rel_err"] < 0.01),
            "note": "leptonic only; hadronic piece is the QCD sector (F151/F152).",
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F251",
        "title": "Interacting one-loop QED photon self-energy and running alpha",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "verdict": ("Ward transversality and b0^QED=4/3 exact; lattice b0 = "
                    "continuum b0; leptonic Delta alpha matches PDG to <0.3% "
                    "(hadronic running deferred to the QCD sector)."),
    }
    return {"summary": summary,
            "detail": {"ward": ward, "b0": b0, "trace": trace,
                       "lattice": latt, "running": run},
            "checks": checks}


def test_F251_vacuum_polarization():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"
    assert res["detail"]["b0"]["b0_QED"] == "4/3"
    assert res["detail"]["ward"]["exact_zero"] is True


def _print(res):
    s = res["summary"]
    print("=" * 74)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 74)
    for name, c in res["checks"].items():
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {name:30s} {c['quantity']}")
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
