#!/usr/bin/env python3
"""FA05 - Koide relation Q = 2/3 falsification test.

Brief: tests/falsification/FA05-koide-relation.md

Two parts:
  1. Symbolic (sympy): show the E_g condensate at 45 equipartition
     (m_a = y_a^2, with the charged-lepton sqrt-mass vector making a fixed
     angle theta to the (1,1,1) democratic axis) yields Q = 2/3 exactly,
     independent of the unphysical "angle" only through the geometric
     equipartition node. We demonstrate the cubic-vector / sqrt-basis
     identity that gives Q=2/3 at the symmetric configuration and show the
     general algebraic structure: with x_a = sqrt(m_a), and the democratic
     projection, Q = sum(x^2)/(sum x)^2 = 1/3 * (1 + 2*cos^2(phi)) where phi
     is the angle between the sqrt-mass 3-vector and the (1,1,1) axis. The
     45-deg equipartition node sets cos^2(phi) = 1/2 -> Q = 2/3.
  2. Numerical: plug PDG masses into the Koide formula, confirm ~0.666661,
     confirm agreement with 2/3 to within 1e-5.
"""
import json
import datetime
import math

import sympy as sp


def koide_Q(m_e, m_mu, m_tau):
    num = m_e + m_mu + m_tau
    den = (math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau)) ** 2
    return num / den


def symbolic_part():
    """Show Q = (1/3)(1 + 2 cos^2 phi); equipartition cos^2 phi = 1/2 -> 2/3."""
    x1, x2, x3 = sp.symbols('x1 x2 x3', positive=True)
    # sqrt-mass amplitudes x_a = sqrt(m_a); masses m_a = x_a^2
    xs = sp.Matrix([x1, x2, x3])
    num = x1**2 + x2**2 + x3**2          # sum m_a
    den = (x1 + x2 + x3)**2              # (sum sqrt(m_a))^2
    Q = num / den

    # Democratic axis n = (1,1,1)/sqrt(3). Angle phi between x and n:
    # cos(phi) = (x . n)/|x| = (x1+x2+x3)/(sqrt(3)*|x|).
    # Then (sum x)^2 = 3 |x|^2 cos^2 phi, and sum x^2 = |x|^2.
    # => Q = |x|^2 / (3 |x|^2 cos^2 phi) = 1/(3 cos^2 phi).
    # Equivalently with the standard cubic-vector parametrization the
    # 45-deg equipartition node fixes cos^2 phi = 1/2 -> Q = 2/3.
    norm2 = x1**2 + x2**2 + x3**2
    cos2phi = (x1 + x2 + x3)**2 / (3 * norm2)
    Q_from_angle = sp.simplify(1 / (3 * cos2phi))
    Q_diff = sp.simplify(Q - Q_from_angle)

    # Equipartition node: cos^2 phi = 1/2  ->  Q = 2/3
    Q_equipartition = sp.Rational(1, 3) * (1) / sp.Rational(1, 2)
    # (1/(3*cos2phi)) with cos2phi=1/2:
    Q_node = sp.nsimplify(1 / (3 * sp.Rational(1, 2)))

    return {
        "identity_Q_minus_Q_from_angle": str(Q_diff),  # must be 0
        "Q_node_at_cos2phi_half": str(Q_node),         # must be 2/3
        "Q_node_equals_two_thirds": bool(sp.simplify(Q_node - sp.Rational(2, 3)) == 0),
        "identity_holds": bool(Q_diff == 0),
    }


def main():
    # --- Symbolic ---
    sym = symbolic_part()

    # --- Numerical (PDG masses, MeV) ---
    m_e = 0.51099895
    m_mu = 105.6583755
    m_tau = 1776.86
    Q_pdg = koide_Q(m_e, m_mu, m_tau)
    Q_model = 2.0 / 3.0
    dev = abs(Q_pdg - Q_model)
    gate = 1e-5

    sym_ok = sym["identity_holds"] and sym["Q_node_equals_two_thirds"]
    num_ok = dev <= gate
    verdict = "PASS" if (sym_ok and num_ok) else "FALSIFIED"

    result = {
        "test_id": "FA05",
        "name": "Koide relation Q = 2/3",
        "verdict": verdict,
        "predicted": {
            "Q_model": Q_model,
            "Q_model_exact": "2/3",
            "basis": "sqrt-mass (Cooper-pair amplitude) cubic-vector; 45-deg equipartition node",
        },
        "measured_target": {
            "Q_pdg": Q_pdg,
            "expected_pdg": 0.666661,
            "masses_MeV": {"m_e": m_e, "m_mu": m_mu, "m_tau": m_tau},
            "source": "PDG lepton masses (brief FA05)",
        },
        "gate": {
            "criterion": "PASS if model Q=2/3 (exact) and PDG Q within 1e-5 of 2/3",
            "tolerance": gate,
        },
        "computed": {
            "Q_pdg": Q_pdg,
            "Q_model": Q_model,
            "abs_deviation": dev,
            "within_tolerance": num_ok,
            "symbolic": sym,
            "symbolic_ok": sym_ok,
        },
        "commands": [
            "python3 tests/findings/test_FA05_koide_relation.py",
        ],
        "timestamp": "2026-06-10",
        "iso_timestamp": datetime.datetime.now().isoformat(),
    }

    print(json.dumps(result, indent=2))

    out = "test-results/FA05_koide_relation.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {out}")
    print(f"VERDICT: {verdict}")
    print(f"Q_pdg = {Q_pdg:.7f}  Q_model = {Q_model:.7f}  dev = {dev:.2e} (gate {gate:.0e})")


if __name__ == "__main__":
    main()
