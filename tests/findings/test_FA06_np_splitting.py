#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_FA06_np_splitting.py
=========================

FA06 falsification brief — Neutron-proton mass splitting (sign AND magnitude,
no QCD scale anchor).

Hypothesis (parameter-free):
    m_n - m_p = (m_d - m_u)  +  (delta_em_n - delta_em_p)
              = (+2.51 MeV strong, neutron-heavier) + (-1.00 MeV EM)
              = +1.51 MeV   (sign POSITIVE).
Measured (PDG): +1.29333 MeV.

The decomposition is plain real arithmetic (no chiral/Dirac transforms), so the
CLAUDE.md numpy/scipy caveat does not apply here; we still route through the
audited engine `ca-simulation/ca_baryon_dynamics.neutron_minus_proton` (the same
channel CASIM's `njl_nucleon` scenario reads) so the test exercises shipped code.

Gate (from the brief):
  PASS  : model gives +1.51 MeV, correct (positive) sign, within ~0.25 MeV of
          PDG +1.293.
  FALSIFIED: wrong sign, or magnitude off beyond the EM-self-energy uncertainty.

Standalone run also dumps test-results/FA06_np.json.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
for sub in ("ca-simulation", "src"):
    p = os.path.join(REPO, sub)
    if p not in sys.path:
        sys.path.insert(0, p)

import ca_baryon_dynamics as BAR  # noqa: E402

# F40 / PDG current masses (MeV). m_d/m_u ~ 2 is consistent with the F40 quark-Y
# down-up gap; EM self-energies are the external P5 inputs (proton's two +2/3
# quarks give the larger Coulomb self-energy).
M_U = 2.16
M_D = 4.67
DELTA_EM_P = 1.00
DELTA_EM_N = 0.0

PRED_STRONG = 2.51   # m_d - m_u, neutron heavier
PRED_EM = -1.00      # delta_em_n - delta_em_p
PRED_TOTAL = 1.51    # MeV
PDG = 1.29333        # MeV
GATE_TOL = 0.25      # MeV


def compute():
    res = BAR.neutron_minus_proton(
        m_u=M_U, m_d=M_D, sigma=1.0, alpha_s=0.5,
        delta_em_p=DELTA_EM_P, delta_em_n=DELTA_EM_N,
    )
    return res


def evaluate(res):
    strong = res["m_d_minus_m_u"]
    em = res["em_term"]
    total = res["m_n_minus_m_p"]
    sign_ok = total > 0.0
    abs_dev = abs(total - PDG)
    within_tol = abs_dev <= GATE_TOL
    verdict = "PASS" if (sign_ok and within_tol) else "FALSIFIED"
    return {
        "strong": strong, "em": em, "total": total,
        "sign_positive": sign_ok, "abs_dev_from_PDG": abs_dev,
        "within_tol": within_tol, "verdict": verdict,
    }


def test_FA06_sign_positive():
    ev = evaluate(compute())
    assert ev["sign_positive"], "n-p splitting must be positive (neutron heavier)"


def test_FA06_strong_term():
    res = compute()
    assert abs(res["m_d_minus_m_u"] - PRED_STRONG) < 1e-9


def test_FA06_em_term():
    res = compute()
    assert abs(res["em_term"] - PRED_EM) < 1e-9


def test_FA06_total_prediction():
    res = compute()
    assert abs(res["m_n_minus_m_p"] - PRED_TOTAL) < 1e-9


def test_FA06_within_gate():
    ev = evaluate(compute())
    assert ev["within_tol"], (
        f"|{ev['total']:.3f} - {PDG}| = {ev['abs_dev_from_PDG']:.3f} MeV "
        f"exceeds {GATE_TOL} MeV gate"
    )
    assert ev["verdict"] == "PASS"


def main():
    res = compute()
    ev = evaluate(res)
    out = {
        "test_id": "FA06",
        "title": "Neutron-proton mass splitting (sign and magnitude, no QCD anchor)",
        "verdict": ev["verdict"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": "2026-06-10",
        "predicted": {
            "np_strong_term_MeV": PRED_STRONG,
            "np_em_term_MeV": PRED_EM,
            "n_minus_p_MeV": PRED_TOTAL,
            "n_minus_p_sign_positive": True,
            "decomposition": "(m_d - m_u) + (delta_em_n - delta_em_p)",
        },
        "computed": {
            "m_d_minus_m_u_MeV": res["m_d_minus_m_u"],
            "em_term_MeV": res["em_term"],
            "n_minus_p_MeV": res["m_n_minus_m_p"],
            "n_minus_p_sign_positive": res["sign_positive"],
            "abs_dev_from_PDG_MeV": ev["abs_dev_from_PDG"],
            "rel_high_pct": 100.0 * (res["m_n_minus_m_p"] - PDG) / PDG,
        },
        "inputs_MeV": {
            "m_u": M_U, "m_d": M_D,
            "delta_em_p": DELTA_EM_P, "delta_em_n": DELTA_EM_N,
        },
        "measured_target": {"n_minus_p_MeV": PDG, "source": "PDG (m_n - m_p = +1.29333 MeV)"},
        "gate": {
            "pass_if": "total +1.51 MeV, sign positive, within ~0.25 MeV of PDG +1.293",
            "tolerance_MeV": GATE_TOL,
        },
        "commands": [
            "casim run scenarios/njl_nucleon.yaml --out test-results/FA06_np.json",
            "python3 tests/findings/test_FA06_np_splitting.py",
            "pytest tests/findings/test_FA06_np_splitting.py",
        ],
        "engine": "ca-simulation/ca_baryon_dynamics.neutron_minus_proton "
                  "(via scenarios/njl_nucleon.yaml -> casim njl_nucleon channel)",
        "provenance": "F123 H3 (sharpest matter prediction), F40 (quark Y / down-up gap), "
                      "F122 (dynamical baryon three-body)",
        "caveat_check": "Pure real arithmetic; no chiral/Dirac numpy transforms involved.",
    }
    dest = os.path.join(REPO, "test-results", "FA06_np.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nWrote {dest}")
    return 0 if ev["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
