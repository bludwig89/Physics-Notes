#!/usr/bin/env python3
"""
test_F260_qed_scattering.py — F260: the tree-level QED S-matrix on the model's
fields + the positron / antiparticle (charge-conjugation + crossing) sector.

Extends the F249 battery (which stops at Thomson) to the full tree S-matrix:
Compton/Klein-Nishina, Moller, Bhabha, e+e- -> gamma gamma (Dirac annihilation),
and e+e- -> mu+mu-. Establishes the positron as the charge-conjugate v-spinor.

Gates (exactness first):
  G1  C gamma^mu C^{-1} = -(gamma^mu)^T ; C^T=-C, C^2=-1        exact (sympy)
  G2  positron v = C ubar^T ; (pslash+m)v=0 ; sum v vbar=pslash-m  machine (no eig)
  G3  crossing: Bhabha=Moller|_{s<->u}; annih=-Compton|_{a->-a}  exact (sympy)
  C1  Compton |M|^2 (trace) = Klein-Nishina Mandelstam form      machine precision
  C2  Ward: k_mu M^{mu nu} = k'_nu M^{mu nu} = 0                 machine precision
  C3  Klein-Nishina total sigma(x) vs closed form; -> Thomson    quantitative (F249 A5)
  M1  Moller |M|^2 vs textbook                                   machine precision
  M2  Bhabha |M|^2 vs textbook                                   machine precision
  M3  Moller/Bhabha differential cross sections                  quantitative
  A1  annihilation |M|^2 + Bose + Ward(both) + total sigma       machine + quantitative
  U1  e+e- -> mu+mu-: |M|^2 + total sigma -> 4 pi a^2/3s         machine + quantitative

Run:  python3 tests/findings/test_F260_qed_scattering.py --json out.json
Test: pytest -q tests/findings/test_F260_qed_scattering.py
"""
from __future__ import annotations
import os, sys, json, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.interactions import qed_scattering as q  # noqa: E402


def run_all():
    detail = q.report()
    checks = {}
    labels = {
        "G1_charge_conjugation": "C gamma^mu C^-1 = -(gamma^mu)^T (positron/crossing)",
        "G2_positron_completeness": "v = C ubar^T; sum v vbar = pslash - m (no eig)",
        "G3_crossing": "Bhabha=Moller|s<->u; annih=-Compton|a->-a",
        "C1_compton_M2": "Compton |M|^2 (trace) = Klein-Nishina Mandelstam form",
        "C2_compton_ward": "Ward k_mu M^{mu nu} = 0 (gauge invariance)",
        "C3_klein_nishina": "KN total sigma(x) vs closed; -> Thomson sigma_T (F249 A5)",
        "M1_moller": "Moller |M|^2 vs textbook",
        "M2_bhabha": "Bhabha |M|^2 vs textbook",
        "M3_moller_bhabha_diff": "Moller/Bhabha differential cross sections",
        "A1_annihilation": "e+e- -> gamma gamma: |M|^2, Bose, Ward, total sigma",
        "U1_mupair": "e+e- -> mu+mu-: |M|^2, total sigma -> 4 pi a^2/3s",
    }
    for key, d in detail.items():
        checks[key] = {"quantity": labels.get(key, key),
                       "statement": d.get("statement", ""),
                       "pass": bool(d.get("gate_pass"))}
    n_pass = sum(1 for c in checks.values() if c["pass"])
    summary = {
        "finding": "F260",
        "title": "Tree-level QED S-matrix + positron/crossing sector",
        "checks": len(checks), "passed": n_pass, "failed": len(checks) - n_pass,
        "alpha_inv_used": q.ALPHA_INV,
        "m_e_MeV": q.M_E_MEV, "m_mu_MeV": q.M_MU_MEV,
        "verdict": ("Positron sector established (C exact, v=C ubar^T completeness); "
                    "Klein-Nishina reproduced and reducing to Thomson; Moller, "
                    "Bhabha, Dirac annihilation and e+e- -> mu+mu- cross sections "
                    "reproduced vs textbook closed forms; Ward identities and "
                    "crossing exact. The model's QED has a working tree S-matrix."),
    }
    return {"summary": summary, "detail": detail, "checks": checks}


def test_F260_qed_scattering():
    res = run_all()
    fails = [k for k, c in res["checks"].items() if not c["pass"]]
    assert not fails, f"failed checks: {fails}"
    d = res["detail"]
    # hard exact-gate assertions
    assert d["G1_charge_conjugation"]["C_gamma_Cinv_eq_minus_gammaT"] is True
    assert d["G1_charge_conjugation"]["C_squared_minus1"] is True
    assert d["G3_crossing"]["moller_to_bhabha_s_u_crossing"] is True
    assert d["G3_crossing"]["compton_to_annihilation_crossing"] is True
    assert d["C1_compton_M2"]["worst_rel_err"] < 1e-10
    assert d["C2_compton_ward"]["worst_k_dot_M_incoming"] < 1e-12
    assert d["A1_annihilation"]["ward_both_photons_worst"] < 1e-12
    assert d["A1_annihilation"]["bose_symmetry_worst_rel"] < 1e-10
    assert res["summary"]["passed"] == res["summary"]["checks"]


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
