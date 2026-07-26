#!/usr/bin/env python3
"""
test_F263_euler_heisenberg_schwinger.py — F263: the nonlinear / non-perturbative
corner of QED. Euler-Heisenberg effective Lagrangian, light-by-light scattering,
strong-field vacuum birefringence, and Schwinger pair production.

Gates (exactness ladder):
  EH1  L_EH coefficient 2 alpha^2/45 and invariant weight 7      exact (sympy)
  EH2  light-by-light sigma = (973/10125 pi) alpha^4 omega^6/m^8 exact (sympy)
  EH3  Ward on all four photon legs + Bose symmetry              exact (sympy)
  EH4  field-induced birefringence ratio 7:4                     exact (sympy)
  SC1  Schwinger exponent pi m^2/eE and 1/n^2 weights            exact (sympy)
  SC2  critical field E_crit = m^2/e = 1.32e18 V/m               quantitative
  SC3  non-perturbative: exp(-pi E_crit/E) has zero Taylor series exact (sympy)

Run:  python3 tests/findings/test_F263_euler_heisenberg_schwinger.py --json out.json
Test: pytest -q tests/findings/test_F263_euler_heisenberg_schwinger.py
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

import ca_euler_heisenberg as eh   # noqa: E402
import ca_schwinger_pair as sc     # noqa: E402


def run_all():
    eh1 = eh.eh_coefficients_symbolic()
    eh2 = eh.light_by_light_cross_section()
    eh3 = eh.ward_and_bose_gates()
    eh4 = eh.birefringence_ratio_symbolic()
    sc1 = sc.schwinger_exponent_symbolic()
    sc2 = sc.critical_field()
    sc4 = sc.non_perturbative_check()

    checks = {
        "EH1_coefficients": {
            "quantity": "L_EH = (2 alpha^2/45 m^4)[(E^2-B^2)^2 + 7(E.B)^2]",
            "prefactor": eh1["coeff_EmB2_over_a2m4"], "weight": eh1["invariant_weight"],
            "invariant_basis": eh1["invariant_basis_ratio"],
            "tier": "exact (sympy)", "pass": bool(eh1["gate_pass"]),
        },
        "EH2_light_by_light": {
            "quantity": "sigma(gg->gg) low-energy coefficient",
            "coeff_times_pi": eh2["coeff_times_pi"], "target": eh2["coeff_target"],
            "scaling": eh2["scaling"],
            "tier": "exact (sympy)", "pass": bool(eh2["gate_pass"]),
        },
        "EH3_ward_bose": {
            "quantity": "gauge invariance (Ward, 4 legs) + Bose symmetry",
            "ward_all_legs_zero": eh3["ward_all_legs_zero"],
            "bose_1_2": eh3["bose_1_2_invariant"], "bose_3_4": eh3["bose_3_4_invariant"],
            "tier": "exact (sympy)", "pass": bool(eh3["gate_pass"]),
        },
        "EH4_birefringence": {
            "quantity": "(n_par-1):(n_perp-1)",
            "coeff_parallel": eh4["coeff_parallel"], "coeff_perp": eh4["coeff_perp"],
            "ratio": eh4["ratio_par_perp"],
            "tier": "exact (sympy)", "pass": bool(eh4["gate_pass"]),
        },
        "SC1_schwinger_exponent": {
            "quantity": "Im L per n = (eE)^2/(8 pi^3 n^2) exp(-n pi m^2/eE)",
            "ImL_n": sc1["ImL_n"], "exponent_n1": sc1["exponent_n1"],
            "tier": "exact (sympy)", "pass": bool(sc1["gate_pass"]),
        },
        "SC2_critical_field": {
            "quantity": "E_crit = m^2/e, B_crit = m^2/e",
            "E_crit_V_per_m": sc2["E_crit_V_per_m"], "B_crit_T": sc2["B_crit_T"],
            "rel_err_E": sc2["rel_err_E"], "rel_err_B": sc2["rel_err_B"],
            "tier": "quantitative", "pass": bool(sc2["gate_pass"]),
        },
        "SC3_nonperturbative": {
            "quantity": "exp(-pi E_crit/E) Taylor series about E=0",
            "taylor": sc4["taylor_about_E0"],
            "tier": "exact (sympy)", "pass": bool(sc4["gate_pass"]),
        },
    }
    n_pass = sum(1 for c in checks.values() if c["pass"])
    return {
        "finding": "F263",
        "title": "Nonlinear/non-perturbative QED: Euler-Heisenberg, "
                 "light-by-light, birefringence, Schwinger pair production",
        "checks": checks,
        "n_pass": n_pass, "n_total": len(checks),
        "all_pass": n_pass == len(checks),
    }


# --------------------------- pytest entry points ---------------------------
def test_eh1_coefficients():
    assert eh.eh_coefficients_symbolic()["gate_pass"]


def test_eh2_light_by_light():
    assert eh.light_by_light_cross_section()["gate_pass"]


def test_eh3_ward_bose():
    assert eh.ward_and_bose_gates()["gate_pass"]


def test_eh4_birefringence():
    assert eh.birefringence_ratio_symbolic()["gate_pass"]


def test_sc1_schwinger_exponent():
    assert sc.schwinger_exponent_symbolic()["gate_pass"]


def test_sc2_critical_field():
    assert sc.critical_field()["gate_pass"]


def test_sc3_nonperturbative():
    assert sc.non_perturbative_check()["gate_pass"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    out = run_all()
    print(json.dumps(out, indent=2, default=str))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(out, f, indent=2, default=str)
    sys.exit(0 if out["all_pass"] else 1)
