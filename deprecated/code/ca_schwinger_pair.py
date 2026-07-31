# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_schwinger_pair.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qed_schwinger_pair.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_schwinger_pair.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_schwinger_pair.py — Schwinger pair production (F263): the non-perturbative
rate of e+ e- creation from a strong static electric field.

This is the imaginary part of the constant-field one-loop effective action of
ca_euler_heisenberg.py, evaluated for a PURE ELECTRIC background. The same
electron determinant that gives the (real) Euler-Heisenberg Lagrangian develops
an IMAGINARY part in an electric field, because the proper-time integrand
e E s cot(e E s) has poles on the positive real axis at s_n = n pi/(e E). Each
pole is a Dirac-sea tunnelling channel: the vacuum decays into n-pair states.
Physically this is the Sauter-Schwinger tunnelling of the F27/F46 Dirac sea in a
background E-field (the CA fermion tilted by the field).

WHAT THIS MODULE ESTABLISHES (explicit scope)
=============================================
EXACT (symbolic, sympy):

  SC1  schwinger_exponent_symbolic():  the residue of the proper-time integrand
       at the pole s_n = n pi/(e E) gives, term by term,

         Im L = sum_{n>=1} (e E)^2 / (8 pi^3 n^2) exp( - n pi m^2 / (e E) ),

       so the vacuum pair-creation probability per unit volume-time is

         w = 2 Im L = (e E)^2/(4 pi^3) sum_{n>=1} (1/n^2) exp(- n pi m^2/(e E)).

       The tunnelling exponent pi m^2/(e E) and the 1/n^2 weight both fall out of
       the residue (sympy-exact). The exponent is - n pi E_crit/E with the
       critical field E_crit = m^2/e.

QUANTITATIVE (numeric):
  SC2  critical_field():  E_crit = m_e^2 c^3/(e hbar) = 1.323e18 V/m and the
       companion B_crit = m_e^2 c^2/(e hbar) = 4.414e9 T, from CODATA constants.

  SC3  pair_production_rate():  the convergent instanton sum w(E), dominated by
       the n=1 term exp(-pi E_crit/E); at E = E_crit the exponent is -pi and the
       rate is O((eE)^2/4pi^3) * 0.0437. Below E_crit the rate is exponentially
       (non-perturbatively) suppressed — no Taylor series in E reproduces it.

sympy (exact residue) + numeric constants/series. No np.linalg.eig on chiral
matrices (CLAUDE.md): the rate is the analytic Im L route (residues), and the
Dirac-sea tunnelling picture is described, not diagonalised.

References: Schwinger Phys.Rev. 82, 664 (1951); Sauter Z.Phys. 69, 742 (1931);
Heisenberg-Euler Z.Phys. 98, 714 (1936); Dunne hep-th/0406216 (review).
"""
from __future__ import annotations

import math
from casim.constants import c_SI as _c_SI, hbar_SI as _hbar_SI

# CODATA 2022
M_E_KG = 9.1093837015e-31
C_LIGHT = _c_SI
E_CHARGE = 1.602176634e-19
HBAR = _hbar_SI

E_CRIT_TARGET = 1.32e18        # V/m (order-of-magnitude target)
B_CRIT_TARGET = 4.41e9         # T


# ======================================================================
#  SC1 — the Schwinger exponent and instanton weights (exact residue)
# ======================================================================
def schwinger_exponent_symbolic() -> dict:
    """Extract Im L from the poles of the pure-electric proper-time integrand.

    L = -(1/8 pi^2) int_0^inf ds/s^3 e^{-m^2 s}[ e E s cot(e E s) - 1 + (e E s)^2/3 ].
    Only the e E s cot(e E s) term has poles on the positive real s-axis, at
    s_n = n pi/(e E). The imaginary part is pi times the sum of residues there.
    This returns the per-n term and checks it equals (eE)^2/(8 pi^3 n^2)
    exp(-n pi m^2/eE), so w = 2 Im L reproduces the Schwinger series with exponent
    pi m^2/(e E)."""
    import sympy as sp

    s = sp.symbols("s", positive=True)
    eE, m = sp.symbols("E m", positive=True)   # eE = e*E product
    n = sp.symbols("n", positive=True, integer=True)
    s_n = n * sp.pi / eE

    # integrand prefactor multiplying cot(eE s): -(1/8pi^2)(1/s^3)e^{-m^2 s}(eE s)
    pref = -sp.Rational(1, 8) / sp.pi ** 2 * (1 / s ** 3) * sp.exp(-m ** 2 * s) * (eE * s)
    residue = sp.limit((s - s_n) * pref * sp.cot(eE * s), s, s_n)
    ImL_n = sp.simplify(-sp.pi * residue)       # sign -> positive rate

    target = eE ** 2 / (8 * sp.pi ** 3 * n ** 2) * sp.exp(-n * sp.pi * m ** 2 / eE)
    gate = sp.simplify(ImL_n / target) == 1

    # the exponent and critical-field identity
    exponent = sp.simplify(-sp.log(sp.exp(-n * sp.pi * m ** 2 / eE)))  # n pi m^2/eE
    return {
        "ImL_n": str(ImL_n),
        "ImL_n_target": str(target),
        "w_n": "2*ImL_n = (eE)^2/(4 pi^3 n^2) exp(-n pi m^2/eE)",
        "exponent_n": str(exponent),                 # n*pi*m^2/E
        "exponent_n1": "pi m^2/(e E) = pi E_crit/E, with E_crit = m^2/e",
        "pole_location": "s_n = n pi/(e E)",
        "gate_pass": bool(gate),
        "statement": "the Schwinger tunnelling exponent pi m^2/(e E) and the 1/n^2 "
                     "instanton weights are the residues of the proper-time "
                     "integrand at s_n = n pi/(e E); w = 2 Im L = "
                     "(eE)^2/(4 pi^3) sum 1/n^2 exp(-n pi m^2/eE), exact.",
    }


# ======================================================================
#  SC2 — critical field (SI, numeric)
# ======================================================================
def critical_field() -> dict:
    """E_crit = m^2 c^3/(e hbar), B_crit = m^2 c^2/(e hbar) from CODATA."""
    E_crit = M_E_KG ** 2 * C_LIGHT ** 3 / (E_CHARGE * HBAR)
    B_crit = M_E_KG ** 2 * C_LIGHT ** 2 / (E_CHARGE * HBAR)
    rel_E = abs(E_crit - E_CRIT_TARGET) / E_CRIT_TARGET
    rel_B = abs(B_crit - B_CRIT_TARGET) / B_CRIT_TARGET
    return {
        "E_crit_V_per_m": E_crit,
        "E_crit_target": E_CRIT_TARGET,
        "B_crit_T": B_crit,
        "B_crit_target": B_CRIT_TARGET,
        "rel_err_E": rel_E,
        "rel_err_B": rel_B,
        "gate_pass": bool(rel_E < 5e-3 and rel_B < 5e-3),
        "statement": "critical (Schwinger) field E_crit = m_e^2 c^3/(e hbar) = "
                     "1.323e18 V/m; companion B_crit = 4.414e9 T. Above E_crit "
                     "the exponent -pi E_crit/E is O(1) and pair creation is "
                     "unsuppressed.",
    }


# ======================================================================
#  SC3 — the pair-production rate (convergent instanton sum)
# ======================================================================
def pair_production_rate(E_over_Ecrit: float = 1.0, n_terms: int = 100) -> dict:
    """Dimensionless rate factor R(E) = sum_{n>=1} (1/n^2) exp(-n pi E_crit/E),
    so w = (eE)^2/(4 pi^3) R. Dominated by n=1: exp(-pi E_crit/E)."""
    x = E_over_Ecrit
    terms = [math.exp(-n * math.pi / x) / n ** 2 for n in range(1, n_terms + 1)]
    R = sum(terms)
    n1 = terms[0]
    return {
        "E_over_Ecrit": x,
        "R_sum": R,
        "n1_term": n1,
        "n1_fraction_of_sum": n1 / R,
        "converged": bool(abs(terms[-1]) < 1e-15 * max(R, 1e-300)),
        "statement": "instanton sum converges geometrically; the n=1 term "
                     "exp(-pi E_crit/E) dominates. The rate is non-perturbative "
                     "in E (essential singularity at E=0): no power series in the "
                     "coupling reproduces exp(-pi E_crit/E).",
    }


def non_perturbative_check() -> dict:
    """Confirm the rate is a genuine essential singularity: all E-derivatives of
    exp(-pi E_crit/E) vanish as E->0, so the Taylor series about E=0 is identically
    zero — the effect is invisible to any finite order of perturbation theory."""
    import sympy as sp
    E, Ec = sp.symbols("E E_c", positive=True)
    f = sp.exp(-sp.pi * Ec / E)
    taylor = sp.series(f, E, 0, 6).removeO()
    return {
        "taylor_about_E0": str(taylor),      # 0
        "all_derivatives_vanish": bool(sp.simplify(taylor) == 0),
        "gate_pass": bool(sp.simplify(taylor) == 0),
        "statement": "exp(-pi E_crit/E) has a vanishing Taylor series about E=0 "
                     "(essential singularity): Schwinger production is invisible "
                     "to perturbation theory — genuinely non-perturbative.",
    }


def report() -> dict:
    return {
        "SC1_exponent": schwinger_exponent_symbolic(),
        "SC2_critical_field": critical_field(),
        "SC3_rate_at_Ecrit": pair_production_rate(1.0),
        "SC3b_rate_below": pair_production_rate(0.1),
        "SC4_nonperturbative": non_perturbative_check(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
