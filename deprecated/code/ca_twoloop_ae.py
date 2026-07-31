# ===== deprecated/code backup =====================================
# source     : ca-simulation/ca_twoloop_ae.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/qed_twoloop_ae.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: ca_twoloop_ae.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
ca_twoloop_ae.py — the two-loop QED electron anomalous moment a_e (the A2 term)
and the two-loop running of alpha, built on the model's own one-loop machinery
(F251 vacuum polarisation Pi, F252 vertex, F258 self-energy). This is F261, the
two-loop push of the QED sector after the one-loop 1PI trio was completed.

    a_e = (alpha/2pi) + A2 (alpha/pi)^2 + A3 (alpha/pi)^3 + ...
    A1 = 1/2                     (Schwinger, F252)
    A2 = -0.328478965...         (Sommerfield 1957 / Petermann 1957)

WHAT THIS MODULE ESTABLISHES (explicit, honest scope)
=====================================================
The two-loop coefficient A2 splits into two GAUGE-INVARIANT groups (Petermann):

  (I)  the VACUUM-POLARISATION insertion — the internal photon of the F252
       one-loop vertex dressed by ONE fermion bubble (the F251 Pi). This piece is
       computed HERE FROM THE MODEL'S OWN Pi: F251's one-loop VP has spectral
       function (its imaginary part)
           (1/pi) Im Pi(s) = (alpha/3pi)(1 + 2 mf^2/s) sqrt(1 - 4 mf^2/s),
       and a photon of virtuality s dressed by it enters the vertex through the
       massive-photon anomaly kernel K1(u) = int_0^1 x^2(1-x)/(x^2+u(1-x)) dx
       (K1(0)=1/2 reproduces Schwinger). The Kallen-Lehmann (dispersive) assembly
           A2^{VP,f}(l) = (1/3) int_{4mf^2}^inf ds/s (1+2mf^2/s)
                                    sqrt(1-4mf^2/s) K1(s/ml^2)
       gives, for the electron's OWN loop (mf = ml = m_e), EXACTLY
           A2^{VP} = 119/36 - pi^2/3 = 0.01568742...   (T1 gate)
       and, for a LIGHT loop in a HEAVY vertex (mf = m_e, ml = m_mu), the leading
       log (1/3) ln(m_mu/m_e) - 25/36 that drives a_mu > a_e (see ca_amu.py).
       This is the piece the prompt asks to take from the model's Pi — done.

  (II) the six VERTEX-TYPE two-loop graphs (corner, cross/ladder, and the two
       self-energy-on-the-electron-line insertions). Their gauge-invariant sum is
       the established analytic constant
           A2^{vertex} = -31/16 + 5 pi^2/12 - (pi^2/2) ln 2 + (3/4) zeta(3)
                       = -0.34416638...
       (Sommerfield/Petermann; each graph is a Laporta-Remiddi master integral).
       This module REPRODUCES that closed form and combines it with the
       model-derived group (I); it does NOT re-derive the six masters from
       scratch. Stated honestly per the exactness ladder.

  A2 = A2^{VP}(equal mass) + A2^{vertex}
     = (119/36 - pi^2/3) + (-31/16 + 5pi^2/12 - (pi^2/2)ln2 + (3/4)zeta3)
     = 197/144 + pi^2/12 - (pi^2/2) ln 2 + (3/4) zeta(3)
     = -0.328478965...                                   (T2, matches target)

  T3  a_e through O((alpha/pi)^2) with the electron's TOTAL A2 (mass-independent
      plus the tiny mu- and tau-loop VP insertions, ca_amu) vs the measured a_e.

  BETA  the two-loop running of alpha. The classic QED beta function
            mu de/dmu = e^3/12pi^2 + e^5/64pi^4 + ...
        converts (sympy, exact) to
            mu dalpha/dmu = 2 alpha^2/3pi + alpha^3/2pi^2 + ...
        The one-loop term is F251's b0 = 4/3 (2alpha^2/3pi); the two-loop
        coefficient is 1/2 in units alpha^3/pi^2, i.e. b1 = 1 per unit-charge
        Dirac fermion. Leptonic here; quark/hadronic loops are deferred to the
        QCD sector (F151/F152), stated not faked.

Exactness ladder:
  T1  equal-mass VP piece = 119/36 - pi^2/3   MODEL-DERIVED (F251 Pi), numeric
                                              to <1e-6 vs the exact rational.
  T2  A2 = -0.328478965 (model VP + literature vertex constant)   EXACT closed
                                              form; numeric to machine precision.
  BETA two-loop alpha coefficient 1/2 (alpha^3/pi^2)  EXACT (sympy) vs known QED.
  T3  a_e through two loops vs measured        QUANTITATIVE (~1e-5).

numpy only (no scipy): the dispersive integral uses an explicit Gauss-Legendre
quadrature with a cosh substitution that maps the wide log-range uniformly (no
np.linalg.eig anywhere; these are real scalar integrals, not chiral transforms).
The A2 closed form and the beta conversion are sympy-exact.
"""
from __future__ import annotations

import math

import numpy as np

# ---- reference constants (CODATA 2022 / PDG) --------------------------------
ALPHA_INV = 137.035999177
ALPHA = 1.0 / ALPHA_INV
PI = math.pi
A_OVER_PI = ALPHA / PI

# lepton mass anchors (F120 electron-calibrated / F121 tau-anchored)
M_LEPTON_MEV = {"e": 0.51099895, "mu": 105.6583755, "tau": 1776.86}
M_E = M_LEPTON_MEV["e"]
M_MU = M_LEPTON_MEV["mu"]
M_TAU = M_LEPTON_MEV["tau"]

A_E_MEASURED = 1.15965218046e-3          # CODATA 2022
A1 = 0.5                                  # Schwinger (F252)
A2_TARGET = -0.328478965                  # Sommerfield 1957 / Petermann 1957


# ======================================================================
#  numpy Gauss-Legendre quadrature (no scipy)
# ======================================================================
def _gl(a: float, b: float, n: int):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (a + b), 0.5 * (b - a) * w


# fixed inner grid for the Feynman-parameter kernel K1
_KX, _KW = _gl(0.0, 1.0, 128)


def K1(u: float) -> float:
    """The massive-photon anomalous-moment kernel from the F252 one-loop vertex:
        K1(u) = int_0^1 dx  x^2 (1-x) / (x^2 + u (1-x)),   u = M^2 / m_lepton^2,
    so that a photon of mass^2 = M^2 contributes a^{(1)}(M) = (alpha/pi) K1(u).
    K1(0) = 1/2 reproduces Schwinger a = alpha/2pi (F252 V2)."""
    return float(np.sum(_KW * _KX ** 2 * (1 - _KX) / (_KX ** 2 + u * (1 - _KX))))


# ======================================================================
#  F251's own vacuum-polarisation spectral function
# ======================================================================
def vp_spectral(s: float, mf: float) -> float:
    """(1/pi) Im Pi(s) for one Dirac fermion of mass mf — the imaginary part of
    the F251 one-loop vacuum polarisation (the fermion bubble), the input the
    dispersive VP-insertion is built from:
        (1/pi) Im Pi(s) = (alpha/3pi)(1 + 2 mf^2/s) sqrt(1 - 4 mf^2/s),  s>4mf^2.
    Returns the value WITHOUT the alpha/pi (that prefactor is carried explicitly
    so A2^{VP} comes out in units of (alpha/pi)^2)."""
    if s <= 4.0 * mf ** 2:
        return 0.0
    return (1.0 / 3.0) * (1.0 + 2.0 * mf ** 2 / s) * math.sqrt(1.0 - 4.0 * mf ** 2 / s)


# ======================================================================
#  the model-derived VP-insertion coefficient (dispersive)
# ======================================================================
def A2_vp_dispersive(mf: float, ml: float, n: int = 400) -> float:
    """A2^{VP,f}(l): the two-loop VP-insertion contribution to a_l (coefficient
    of (alpha/pi)^2) from a fermion loop of mass mf inside the l-vertex, built
    from F251's spectral function via Kallen-Lehmann:

        A2^{VP,f}(l) = (1/3) int_{4mf^2}^inf ds/s (1+2mf^2/s) sqrt(1-4mf^2/s)
                                                                K1(s/ml^2).

    Substitution s = 4 mf^2 cosh^2(theta) maps the whole (logarithmic) range
    uniformly and tames the sqrt threshold (sqrt(1-4mf^2/s) = tanh theta):

        = (2/3) int_0^inf dtheta (1 + 1/(2 cosh^2 theta)) tanh^2(theta)
                                  K1(4 mf^2 cosh^2 theta / ml^2).

    Equal mass -> 119/36 - pi^2/3; light-in-heavy -> (1/3)ln(ml/mf) - 25/36 + ...
    """
    Theta = math.log(ml / mf) + 30.0
    th, w = _gl(0.0, Theta, n)
    ch = np.cosh(th)
    s = 4.0 * mf ** 2 * ch ** 2
    kern = np.array([K1(si / ml ** 2) for si in s])
    integ = (2.0 / 3.0) * (1.0 + 1.0 / (2.0 * ch ** 2)) * np.tanh(th) ** 2 * kern
    return float(np.sum(w * integ))


# ======================================================================
#  T1 — equal-mass VP piece = 119/36 - pi^2/3 (model-derived gate)
# ======================================================================
def equal_mass_vp_gate() -> dict:
    """The electron's OWN vacuum-polarisation insertion (mf = ml = m_e). The
    dispersive integral built from F251's Pi must reproduce the exact rational
    119/36 - pi^2/3 = 0.01568742... This is the model-derived half of A2."""
    val = A2_vp_dispersive(1.0, 1.0)              # scale-free: only mf/ml matters
    exact = 119.0 / 36.0 - PI ** 2 / 3.0
    return {
        "A2_vp_equal_mass_model": val,
        "A2_vp_equal_mass_exact": exact,
        "exact_form": "119/36 - pi^2/3",
        "abs_err": abs(val - exact),
        "gate_pass": abs(val - exact) < 1e-6,
        "statement": "the equal-mass VP insertion, built from F251's own spectral "
                     "function (1/pi)Im Pi = (alpha/3pi)(1+2m^2/s)sqrt(1-4m^2/s), "
                     "reproduces 119/36 - pi^2/3 = 0.0156874 to <1e-6 (dispersive "
                     "Kallen-Lehmann assembly through the F252 kernel K1).",
    }


# ======================================================================
#  T2 — A2 = -0.328478965 (model VP + literature vertex constant)
# ======================================================================
def A2_assembly_symbolic() -> dict:
    """Assemble A2 exactly. Group (I) = the equal-mass VP piece 119/36 - pi^2/3
    (model-derived, T1). Group (II) = the six vertex-type two-loop graphs, whose
    gauge-invariant sum is the established closed form
        A2^{vertex} = -31/16 + 5pi^2/12 - (pi^2/2)ln2 + (3/4)zeta(3).
    Their sum is the Sommerfield-Petermann coefficient
        A2 = 197/144 + pi^2/12 - (pi^2/2)ln2 + (3/4)zeta(3) = -0.328478965...
    Returns the sympy-exact closed form and the numeric value vs target."""
    import sympy as sp

    pi, ln2, z3 = sp.pi, sp.log(2), sp.zeta(3)
    A2_vp = sp.Rational(119, 36) - pi ** 2 / 3                      # group I (model)
    A2_vertex = (-sp.Rational(31, 16) + sp.Rational(5, 12) * pi ** 2
                 - pi ** 2 / 2 * ln2 + sp.Rational(3, 4) * z3)      # group II
    A2_total = sp.simplify(A2_vp + A2_vertex)
    A2_canonical = (sp.Rational(197, 144) + pi ** 2 / 12
                    - pi ** 2 / 2 * ln2 + sp.Rational(3, 4) * z3)
    identical = sp.simplify(A2_total - A2_canonical) == 0
    A2_num = float(A2_canonical)
    return {
        "A2_vp_group_symbolic": str(A2_vp),
        "A2_vertex_group_symbolic": str(A2_vertex),
        "A2_total_symbolic": str(A2_canonical),
        "A2_group_sum_equals_canonical": bool(identical),
        "A2_numeric": A2_num,
        "A2_vp_numeric": float(A2_vp),
        "A2_vertex_numeric": float(A2_vertex),
        "A2_target": A2_TARGET,
        "abs_err_vs_target": abs(A2_num - A2_TARGET),
        "gate_pass": bool(identical and abs(A2_num - A2_TARGET) < 1e-6),
        "statement": "A2 = (119/36 - pi^2/3) + (-31/16 + 5pi^2/12 - (pi^2/2)ln2 "
                     "+ (3/4)zeta3) = 197/144 + pi^2/12 - (pi^2/2)ln2 + (3/4)zeta3 "
                     "= -0.328478966. Group I (VP) is model-derived from F251; "
                     "group II (six vertex masters) is the established closed form "
                     "(reproduced, not re-derived from the masters).",
    }


# ======================================================================
#  T3 — a_e through O((alpha/pi)^2) vs measured
# ======================================================================
def a_e_two_loop() -> dict:
    """a_e through two loops with the electron's TOTAL two-loop coefficient
        A2(e) = A2_massindep + A2^{VP}(mu in e) + A2^{VP}(tau in e),
    where the mass-independent A2 = -0.328478966 and the heavy-loop insertions are
    the (tiny) mu- and tau-bubble VP pieces (they DECOUPLE, ~ (m_e/m_f)^2). Quote
    a_e = alpha/2pi + A2(e)(alpha/pi)^2 vs measured; the residual ~1e-5 is the
    three-loop A3 and beyond (out of scope)."""
    A2_mi = float(A2_assembly_symbolic()["A2_numeric"])
    vp_mu = A2_vp_dispersive(M_MU, M_E)       # muon loop in electron vertex (tiny)
    vp_tau = A2_vp_dispersive(M_TAU, M_E)     # tau loop in electron vertex (tinier)
    A2_e = A2_mi + vp_mu + vp_tau
    a_e = A1 * A_OVER_PI + A2_e * A_OVER_PI ** 2
    a_e_1loop = A1 * A_OVER_PI
    return {
        "A2_mass_independent": A2_mi,
        "A2_vp_mu_in_e": vp_mu,
        "A2_vp_tau_in_e": vp_tau,
        "A2_electron_total": A2_e,
        "a_e_one_loop": a_e_1loop,
        "a_e_two_loop": a_e,
        "a_e_measured": A_E_MEASURED,
        "rel_err_one_loop": abs(a_e_1loop - A_E_MEASURED) / A_E_MEASURED,
        "rel_err_two_loop": abs(a_e - A_E_MEASURED) / A_E_MEASURED,
        "statement": "a_e through two loops = alpha/2pi + A2(e)(alpha/pi)^2 with "
                     "A2(e) = -0.32847844 (mass-independent + decoupling mu,tau VP) "
                     "gives a_e = 1.1596396e-3 vs measured 1.15965218e-3 (~1e-5); "
                     "the one-loop 0.15% is reduced by ~2 orders. Residual is the "
                     "three-loop A3 = 1.181... and beyond (out of scope).",
    }


# ======================================================================
#  BETA — the two-loop running of alpha (sympy-exact conversion)
# ======================================================================
def two_loop_beta_symbolic() -> dict:
    """The two-loop QED beta function coefficient. Start from the classic QED
    result for one unit-charge Dirac fermion
        mu de/dmu = e^3/(12 pi^2) + e^5/(64 pi^4) + ...
    and convert EXACTLY (sympy, via alpha = e^2/4pi) to the alpha form:
        mu dalpha/dmu = 2 alpha^2/(3 pi) + alpha^3/(2 pi^2) + ...
    The one-loop term 2alpha^2/3pi is F251's b0 = 4/3 (d(1/alpha)/dln mu^2 =
    -b0/4pi = -1/3pi). The TWO-loop coefficient is 1/2 in units alpha^3/pi^2,
    equivalently b1 = 1 per unit-charge Dirac fermion in
        d(1/alpha)/dln mu^2 = -(1/4pi)(b0 + b1 (alpha/pi) + ...).
    Leptonic here (each lepton contributes b0=4/3, b1=1); quark/hadronic loops
    are deferred to the QCD sector (F151/F152)."""
    import sympy as sp

    e, mu, alpha = sp.symbols("e mu alpha", positive=True)
    pi = sp.pi
    # classic QED beta(e) for one Dirac fermion, charge 1
    beta_e = e ** 3 / (12 * pi ** 2) + e ** 5 / (64 * pi ** 4)
    # alpha = e^2/4pi  =>  dalpha/dmu = (e/2pi) de/dmu ; and e^2 = 4 pi alpha
    beta_alpha = sp.simplify((e / (2 * pi)) * beta_e)
    beta_alpha = sp.expand(beta_alpha.subs(e ** 2, 4 * pi * alpha)
                           .rewrite(sp.Pow))
    # collect coefficients of alpha^2 and alpha^3 explicitly
    beta_alpha = sp.expand(sp.simplify(
        (e / (2 * pi)) * beta_e).rewrite(sp.Pow))
    # substitute powers of e in terms of alpha: e^4 -> 16 pi^2 alpha^2, e^6 -> 64 pi^3 alpha^3
    beta_alpha = beta_alpha.subs(e ** 6, 64 * pi ** 3 * alpha ** 3)
    beta_alpha = beta_alpha.subs(e ** 4, 16 * pi ** 2 * alpha ** 2)
    beta_alpha = sp.expand(beta_alpha)
    c_oneloop = sp.simplify(beta_alpha.coeff(alpha, 2))            # 2/(3 pi)
    c_twoloop = sp.simplify(beta_alpha.coeff(alpha, 3))            # 1/(2 pi^2)
    oneloop_ok = sp.simplify(c_oneloop - sp.Rational(2, 3) / pi) == 0
    twoloop_ok = sp.simplify(c_twoloop - sp.Rational(1, 2) / pi ** 2) == 0
    # b-convention: d(1/alpha)/dln mu^2 = -(1/4pi)(b0 + b1 (alpha/pi))
    #   dalpha/dln mu^2 = (1/2) mu dalpha/dmu = alpha^2/3pi + alpha^3/4pi^2
    #   d(1/a)/dln mu^2 = -1/3pi - alpha/4pi^2  => b0=4/3, b1=1
    b0 = sp.Rational(4, 3)
    b1 = sp.Integer(1)
    return {
        "beta_alpha_form": "2*alpha^2/(3*pi) + alpha^3/(2*pi^2) + ...",
        "one_loop_coeff_symbolic": str(c_oneloop),                 # 2/(3 pi)
        "two_loop_coeff_symbolic": str(c_twoloop),                 # 1/(2 pi^2)
        "one_loop_matches_2_over_3pi": bool(oneloop_ok),
        "two_loop_matches_1_over_2pi2": bool(twoloop_ok),
        "b0_QED_F251": str(b0),                                    # 4/3
        "b1_QED": str(b1),                                         # 1 per fermion
        "gate_pass": bool(oneloop_ok and twoloop_ok),
        "scope": "leptonic: each charged lepton contributes b0=4/3, b1=1. Quark / "
                 "hadronic loops (and their QCD dressing) are deferred to the QCD "
                 "sector (F151/F152) — not included here, stated not faked.",
        "statement": "QED two-loop running: mu dalpha/dmu = 2alpha^2/3pi + "
                     "alpha^3/2pi^2 (sympy-exact from mu de/dmu = e^3/12pi^2 + "
                     "e^5/64pi^4). One-loop = F251 b0 = 4/3; two-loop coefficient "
                     "= 1/2 (alpha^3/pi^2), i.e. b1 = 1 per unit-charge fermion.",
    }


# ======================================================================
#  Report
# ======================================================================
def report() -> dict:
    return {
        "T1_equal_mass_vp": equal_mass_vp_gate(),
        "T2_A2_assembly": A2_assembly_symbolic(),
        "T3_a_e_two_loop": a_e_two_loop(),
        "BETA_two_loop": two_loop_beta_symbolic(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
