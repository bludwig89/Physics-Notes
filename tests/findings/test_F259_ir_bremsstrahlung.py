#!/usr/bin/env python3
"""
test_F259_ir_bremsstrahlung.py — F259: the IR sector of QED — soft real-photon
emission (bremsstrahlung) and the Bloch-Nordsieck / KLN cancellation of IR
divergences between the virtual (F252 vertex F_1 + Z_2) and real contributions.

Gates (exactness first):
  B1  eikonal factor  e(p'.eps/p'.k - p.eps/p.k)  from the F87 vertex   exact (sympy)
  B2  k.J = 0 (literal) + pol-sum collapse -J.J   (F250 transverse 2-pol) exact (sympy)
  B4  soft omega-integral = ln(DeltaE/mu) (IR log); c_lat drops out       exact (sympy)
  Q1  f_IR(q^2) angular integral vs closed ln(-q^2/m^2)-1                 quantitative
  B3  Bloch-Nordsieck: coeff of ln(mu^2) in virtual+soft = 0             exact (sympy)
  Q2  finite mu-independent O(alpha) Sudakov observable                  quantitative

Run:  python3 tests/findings/test_F259_ir_bremsstrahlung.py --json out.json
Test: pytest -q tests/findings/test_F259_ir_bremsstrahlung.py
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

import ca_ir_bremsstrahlung as ir  # noqa: E402


def run_all():
    b1 = ir.eikonal_factor_symbolic()
    b2 = ir.eikonal_current_conservation_symbolic()
    b4 = ir.ir_log_coefficient_symbolic()
    q1 = ir.eikonal_ir_function()
    b3 = ir.bloch_nordsieck_cancellation_symbolic()
    q2 = ir.sudakov_observable()

    checks = {
        "B1_eikonal_factor": {
            "quantity": "M_rad -> e M_0 (p'.eps/p'.k - p.eps/p.k) from F87 vertex",
            "spinor_identity_exact": b1["spinor_identity_exact"],
            "tier": "exact", "pass": bool(b1["gate_pass"]),
        },
        "B2_current_conservation": {
            "quantity": "k.J = 0 (literal); pol-sum collapse -J.J (F250 2-pol)",
            "k_dot_J": b2["k_dot_J"], "collapse": b2["polsum_collapse_exact"],
            "tier": "exact", "pass": bool(b2["gate_pass"]),
        },
        "B4_ir_log_coefficient": {
            "quantity": "soft omega-integral = ln(DeltaE/mu); c_lat drops out",
            "omega_log_integral": b4["omega_log_integral"],
            "c_lat_independent": b4["c_lat_independent_coeff"],
            "tier": "exact", "pass": bool(b4["gate_pass"]),
        },
        "Q1_ir_function": {
            "quantity": "f_IR(q^2) angular integral vs closed ln(-q^2/m^2)-1",
            "f_IR_numeric": q1["f_IR_numeric"],
            "f_IR_closed": q1["f_IR_closed_hi_E_ln_minus1"],
            "rel_err_vs_closed": q1["rel_err_vs_closed"],
            "tier": "quantitative",
            "pass": bool(q1["rel_err_vs_closed"] < 5e-3),
        },
        "B3_bloch_nordsieck": {
            "quantity": "coeff of ln(mu^2) in sigma_virtual+sigma_soft = 0",
            "mu_independent": b3["mu_independent"],
            "finite_form_exact": b3["finite_form_exact"],
            "finite_sum": b3["finite_sum"],
            "tier": "exact", "pass": bool(b3["gate_pass"]),
        },
        "Q2_sudakov": {
            "quantity": "finite mu-independent O(alpha) Sudakov correction",
            "O_alpha_correction": q2["O_alpha_correction"],
            "sudakov_exponentiated": q2["sudakov_exponentiated"],
            "mu_independent": q2["mu_independent"],
            "tier": "quantitative",
            "pass": bool(q2["mu_independent"] and q2["O_alpha_correction"] < 0.0
                         and q2["sudakov_exponentiated"] < 1.0),
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F259",
        "title": "IR sector: soft bremsstrahlung + Bloch-Nordsieck cancellation",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "verdict": ("Eikonal factor reproduced from the F87 vertex; k.J=0 and the "
                    "F250 2-pol collapse exact; the soft IR log cancels the "
                    "virtual (F252 F_1 + F258 Z_2) IR log so the O(alpha) "
                    "inclusive "
                    "rate is mu-independent (Bloch-Nordsieck); finite Sudakov "
                    "observable quoted."),
    }
    return {"summary": summary,
            "detail": {"b1": b1, "b2": b2, "b4": b4, "q1": q1, "b3": b3, "q2": q2},
            "checks": checks}


def test_F259_ir_bremsstrahlung():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"
    # hard exact-gate assertions
    assert res["detail"]["b1"]["spinor_identity_exact"] is True
    assert res["detail"]["b2"]["k_dot_J"] == "0"
    assert res["detail"]["b2"]["polsum_collapse_exact"] is True
    assert res["detail"]["b3"]["mu_independent"] is True
    assert res["detail"]["b3"]["finite_form_exact"] is True


def _print(res):
    s = res["summary"]
    print("=" * 74)
    print(f"  {s['finding']}: {s['title']}")
    print("=" * 74)
    for name, c in res["checks"].items():
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"  [{mark}] {name:24s} {c['quantity']}")
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
