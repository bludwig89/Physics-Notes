#!/usr/bin/env python3
"""
test_F261_twoloop_ae_amu.py — F261: two-loop QED. The electron anomalous moment
coefficient A2 (Sommerfield-Petermann), the two-loop running of alpha, and the
muon a_mu with the lepton-universality gate.

Gates (exactness first):
  T1  equal-mass VP piece = 119/36 - pi^2/3  (MODEL-DERIVED from F251 Pi)   <1e-6
  T2  A2 = -0.328478965 (model VP + literature vertex constant)   exact closed form
  BETA two-loop alpha coefficient 1/2 (alpha^3/pi^2), b1=1        exact (sympy)
  T3  a_e through two loops vs measured                            quantitative ~1e-5
  U1  universality: mass-independent A1,A2 identical for e and mu  exact identity
  U2  A2^{VP}(e in mu) = 1.0942583 (leading log, from F251 Pi)     quantitative
  U3  A2(mu) = 0.765857410 and a_mu^{QED} (2 loops)                quantitative

Run:  python3 tests/findings/test_F261_twoloop_ae_amu.py --json out.json
Test: pytest -q tests/findings/test_F261_twoloop_ae_amu.py
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

import ca_twoloop_ae as tl  # noqa: E402
import ca_amu as amu        # noqa: E402


def run_all():
    t1 = tl.equal_mass_vp_gate()
    t2 = tl.A2_assembly_symbolic()
    beta = tl.two_loop_beta_symbolic()
    t3 = tl.a_e_two_loop()
    u1 = amu.universality_gate()
    u2 = amu.vp_e_in_mu()
    u3 = amu.a_mu_two_loop()

    checks = {
        "T1_equal_mass_vp": {
            "quantity": "equal-mass VP insertion = 119/36 - pi^2/3 (from F251 Pi)",
            "model": t1["A2_vp_equal_mass_model"], "exact": t1["A2_vp_equal_mass_exact"],
            "abs_err": t1["abs_err"], "tier": "model-derived (exact target)",
            "pass": bool(t1["gate_pass"]),
        },
        "T2_A2_assembly": {
            "quantity": "A2 = -0.328478965 (Sommerfield-Petermann)",
            "A2_numeric": t2["A2_numeric"], "A2_target": t2["A2_target"],
            "abs_err": t2["abs_err_vs_target"],
            "group_sum_identity": t2["A2_group_sum_equals_canonical"],
            "tier": "exact (closed form)",
            "pass": bool(t2["gate_pass"]),
        },
        "BETA_two_loop": {
            "quantity": "two-loop QED beta coeff 1/2 (alpha^3/pi^2), b1=1",
            "two_loop_coeff": beta["two_loop_coeff_symbolic"],
            "b0": beta["b0_QED_F251"], "b1": beta["b1_QED"],
            "tier": "exact (sympy)",
            "pass": bool(beta["gate_pass"]),
        },
        "T3_a_e_two_loop": {
            "quantity": "a_e through two loops vs measured",
            "a_e_two_loop": t3["a_e_two_loop"], "a_e_measured": t3["a_e_measured"],
            "rel_err_one_loop": t3["rel_err_one_loop"],
            "rel_err_two_loop": t3["rel_err_two_loop"],
            "tier": "quantitative",
            "pass": bool(t3["rel_err_two_loop"] < 5e-5
                         and t3["rel_err_two_loop"] < t3["rel_err_one_loop"]),
        },
        "U1_universality": {
            "quantity": "mass-independent A1,A2 identical for e and mu",
            "A1_identical": u1["A1_identical"],
            "A2_identical": u1["A2_massindep_identical"],
            "tier": "exact identity",
            "pass": bool(u1["gate_pass"]),
        },
        "U2_vp_e_in_mu": {
            "quantity": "A2^{VP}(e in mu) leading source of a_mu - a_e",
            "model": u2["A2_vp_e_in_mu_model"], "known": u2["A2_vp_e_in_mu_known"],
            "leading_log": u2["leading_log_13_ln_mmu_me_minus_2536"],
            "reverse_decoupled": u2["A2_vp_mu_in_e_reverse_decoupled"],
            "tier": "quantitative",
            "pass": bool(u2["gate_pass"]),
        },
        "U3_a_mu_two_loop": {
            "quantity": "A2(mu) = 0.765857410 and a_mu^{QED} (2 loops)",
            "A2_muon_total": u3["A2_muon_total"], "A2_muon_known": u3["A2_muon_known"],
            "A2_muon_abs_err": u3["A2_muon_abs_err"],
            "a_mu_two_loop_QED": u3["a_mu_two_loop_QED"],
            "tier": "quantitative (QED only; had/EW deferred)",
            "pass": bool(u3["gate_pass"]),
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F261",
        "title": "Two-loop QED: A2 = -0.328478965, two-loop beta, and a_mu universality",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "verdict": ("A2 = -0.328478966 reproduced (VP piece 119/36-pi^2/3 from the "
                    "model's own F251 Pi + established vertex constant); two-loop "
                    "beta coeff 1/2 (b1=1) sympy-exact; universality exact (e,mu "
                    "share A1,A2); A2^{VP}(e in mu) = 1.0942583 gives A2(mu) = "
                    "0.765857410 and a_mu^{QED}. Hadronic/EW explicitly deferred."),
    }
    return {"summary": summary,
            "detail": {"t1": t1, "t2": t2, "beta": beta, "t3": t3,
                       "u1": u1, "u2": u2, "u3": u3},
            "checks": checks}


def test_F261_two_loop_ae():
    res = run_all()
    d = res["detail"]
    # exact / near-exact gates
    assert d["t1"]["abs_err"] < 1e-6                       # model VP = 119/36-pi^2/3
    assert d["t2"]["A2_group_sum_equals_canonical"] is True
    assert d["t2"]["abs_err_vs_target"] < 1e-6            # A2 = -0.328478965
    assert d["beta"]["two_loop_coeff_symbolic"] == "1/(2*pi**2)"
    assert d["beta"]["b1_QED"] == "1"


def test_F261_universality_and_amu():
    res = run_all()
    d = res["detail"]
    assert d["u1"]["A1_identical"] is True
    assert d["u1"]["A2_massindep_identical"] is True      # exact universality
    assert abs(d["u2"]["A2_vp_e_in_mu_model"] - 1.0942583) < 1e-3
    assert abs(d["u3"]["A2_muon_total"] - 0.76585741) < 1e-4
    # a_mu > a_e driven by light-in-heavy vs heavy-in-light asymmetry
    assert d["u2"]["A2_vp_e_in_mu_model"] > 1e5 * d["u2"]["A2_vp_mu_in_e_reverse_decoupled"]


def test_F261_all_checks_pass():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"


def _print(res):
    s = res["summary"]
    print("=" * 78)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 78)
    for name, c in res["checks"].items():
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {name:20s} {c['quantity']}")
    print("-" * 78)
    print(f"  {s['passed']}/{s['checks']} pass   |   {s['verdict']}")
    print("=" * 78)


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
