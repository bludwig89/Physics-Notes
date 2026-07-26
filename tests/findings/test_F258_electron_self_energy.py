#!/usr/bin/env python3
"""
test_F258_electron_self_energy.py — F258: the one-loop QED electron self-energy
Sigma(p), the mass shift delta m, the wavefunction renormalisation Z2, and the
differential Ward-Takahashi identity that PROVES Z1 = Z2 between the computed
Sigma (this session) and the F252 vertex Lambda. Completes the one-loop 1PI set
{Z3 (Pi, F251), Z2 (Sigma, F258), Z1 (Lambda, F252)}.

Gates (exactness first):
  S0  numerator contraction gamma^m(kslash+m)gamma_m = -2kslash+4m   exact (sympy)
  S1  delta m = (3 alpha/4pi) m ln(Lambda^2/m^2)  coefficient 3/4pi  exact (sympy)
  S2  Z2 = 1 - (alpha/4pi) ln(Lambda^2/m^2); Z1 shares -alpha/4pi     exact (sympy)
  S3  differential WT  dSigma/dp_m = -Lambda^m(p,p)  => Z1 = Z2       exact (sympy)
  S4  renormalised S_R^{-1} = pslash - m, residue 1, no divergence    exact (sympy)
  S5  lattice = continuum (subtracted A,B coeffs P-flat)              convergent

Run:  python3 tests/findings/test_F258_electron_self_energy.py --json out.json
Test: pytest -q tests/findings/test_F258_electron_self_energy.py
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

import ca_electron_self_energy as se  # noqa: E402


def run_all():
    s0 = se.contraction_identity_symbolic()
    s1 = se.delta_m_coefficient_symbolic()
    s2 = se.z2_coefficient_symbolic()
    s3 = se.differential_ward_identity_symbolic()
    s4 = se.renormalized_propagator_symbolic()
    s5 = se.lattice_consistency(n=20)

    checks = {
        "S0_contraction": {
            "quantity": "gamma^m(kslash+m)gamma_m = -2 kslash + 4 m (d=4)",
            "tier": "exact", "clifford": s0["clifford_2eta"],
            "pass": bool(s0["gate_pass"]),
        },
        "S1_delta_m": {
            "quantity": "delta m = (3 alpha/4pi) m ln(Lambda^2/m^2)",
            "parametric_integral": s1["parametric_integral_4m2x"],
            "coeff": s1["delta_m_over_alpha_ln_symbolic"],
            "target": s1["target_3_over_4pi"], "tier": "exact",
            "pass": bool(s1["gate_pass"]),
        },
        "S2_z2": {
            "quantity": "Z2 = 1 - (alpha/4pi) ln(Lambda^2/m^2); Z1=Z2 log coeff",
            "parametric_integral": s2["parametric_integral_m2x"],
            "coeff": s2["z2_minus_1_over_alpha_ln_symbolic"],
            "Z1_equals_Z2_log_coeff": s2["Z1_equals_Z2_log_coeff"], "tier": "exact",
            "pass": bool(s2["gate_pass"] and s2["Z1_equals_Z2_log_coeff"]),
        },
        "S3_differential_wt": {
            "quantity": "dSigma/dp_m = -Lambda^m(p,p)  => Z1 = Z2 (computed)",
            "vertex_insertion": s3["vertex_insertion_ok"],
            "propagator_identity": s3["propagator_identity_ok"],
            "Z1_equals_Z2_derived": s3["Z1_equals_Z2_derived"], "tier": "exact",
            "pass": bool(s3["gate_pass"]),
        },
        "S4_renormalized_propagator": {
            "quantity": "S_R^{-1} = pslash - m, residue 1, no leftover divergence",
            "pole": s4["renorm_inverse_at_pole"], "residue": s4["renorm_residue"],
            "divergence_absorbed": s4["divergence_absorbed"], "tier": "exact",
            "pass": bool(s4["gate_pass"]),
        },
        "S5_lattice_consistency": {
            "quantity": "lattice = continuum (subtracted A,B coeffs P-flat)",
            "dA_spread": s5["dA_spread"], "dB_spread": s5["dB_spread"],
            "tier": "convergent",
            "pass": bool(s5["coeff_propagator_independent"]),
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F258",
        "title": "One-loop QED electron self-energy: delta m, Z2, and Z1=Z2 proven",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "verdict": ("delta m = (3 alpha/4pi) m ln(Lambda^2/m^2) and the Z2 log "
                    "coefficient -alpha/4pi are algebraically exact; the "
                    "differential Ward-Takahashi identity dSigma/dp_m = "
                    "-Lambda^m(p,p) is derived from the loop integrand, turning "
                    "Z1=Z2 into a computed identity; lattice = continuum after "
                    "subtraction. Completes the one-loop 1PI set {Z3,Z2,Z1}."),
    }
    return {"summary": summary,
            "detail": {"s0": s0, "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5},
            "checks": checks}


def test_F258_electron_self_energy():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"
    d = res["detail"]
    assert d["s1"]["parametric_integral_4m2x"] == "3"
    assert d["s1"]["delta_m_over_alpha_ln_symbolic"] == "3/(4*pi)"
    assert d["s2"]["parametric_integral_m2x"] == "-1"
    assert d["s2"]["Z1_equals_Z2_log_coeff"] is True
    assert d["s3"]["Z1_equals_Z2_derived"] is True
    assert d["s4"]["renorm_residue"] == "1"


def _print(res):
    s = res["summary"]
    print("=" * 74)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 74)
    for name, c in res["checks"].items():
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {name:28s} {c['quantity']}")
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
