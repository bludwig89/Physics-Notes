"""
derive_dielectric_noconfine.py — Why the colour-dielectric tension does NOT
map onto F86's exact σ = 2π v² n (F142 Q1)
============================================================================

Created: 2026-06-11

Question (F139 §6 open edge): can the longitudinal colour-dielectric
(Friedberg-Lee) flux tube of F139 — ε_c(f)=1−f², quartic bag (1/4ξ²)(f²−1)² —
be mapped onto the exact topological string tension σ = 2π v² n of F86's
magnetic ANO vortex with *algebraic* exactness?

This script shows the answer is **no**, and exactly why:

  1. DICTIONARY + BAG BOUND.  Under the dual-superconductor dictionary
        B = e²v⁴/4 ,   Φ = 2π n / e ,   λ = ξ = 1/(ev)  (BPS),
     the thin-wall bag tension of the *electric* tube is
        σ_FL = Φ √(2B) = (1/√2)·2π v² n,
     i.e. the right *scaling* (∝ v² n) but prefactor 1/√2, not 1.

  2. NO-GO (the real obstruction).  The continuum ε_c=1−f² electric functional
     does NOT confine.  The "spread-thin" configuration — uniform f=1−δ over
     transverse area A — has
        σ_spread(A) ∝ A^(−1/3)  →  0  as A → ∞,
     so there is no finite continuum tension to match.  F139's "constant
     tension" is a finite-box + ε-floor regulator effect.  Verified two ways:
     (a) the analytic A^(−1/3) law; (b) a direct gradient-flow minimisation
     whose tension falls as L^(−2/3) as the box grows.

  3. STRUCTURAL REASON.  σ = 2π v² n is the *topological* charge of the
     magnetic ANO vortex: the condensate phase winds n times and f→v is pinned
     at infinity by topology, forbidding the spread.  The electric dielectric
     model carries the flux as a *source charge* with no winding — f is not
     topologically pinned — so the flux escapes.  The exactness lives in the
     winding, which the dielectric tube does not have.

The map that IS algebraically exact already exists: F99's centre-twist
Lagrange multiplier  σ_k = −ln s_k  (sympy-exact), whose small-σ Abelian-BPS
limit is σ_k = 2π v² k with 2π v² := σ_1.  See findings/F142.

Pure numpy (CLAUDE.md).
"""
from __future__ import annotations
from fractions import Fraction

import numpy as np

__all__ = ["bag_dictionary", "spread_tension", "tube_tension_box",
           "su3_casimir_ratios", "su_n_k_string_ratios",
           "check_dielectric_noconfine", "main"]


def bag_dictionary(v=1.0, e=1.0, n=1):
    """Dual-superconductor dictionary at the BPS point.  Returns
    (B, Phi, sigma_ANO, sigma_bag_thinwall)."""
    B = e ** 2 * v ** 4 / 4.0          # bag constant = potential at melted core
    Phi = 2.0 * np.pi * n / e          # quantised colour-electric flux
    sigma_ano = 2.0 * np.pi * v ** 2 * n
    sigma_bag = Phi * np.sqrt(2.0 * B)  # thin-wall MIT-bag tube tension
    return B, Phi, sigma_ano, sigma_bag


def spread_tension(Phi, B, A, bag_power=2):
    """Tension of the uniform 'spread-thin' configuration f=1−δ over area A.

    field+bag = Φ²/(4Aδ) + 4Bδ^p A ;  minimised at δ^(p+1) = Φ²/(16 p B A²),
    which for the F139 quartic bag (p = 2) is δ³ = Φ²/(32 B A²) and gives
    σ ∝ A^(−(p−1)/(p+1)) = A^(−1/3) → 0: the spreading no-go.

    `bag_power` is the exponent of the bag potential in the conductivity
    δ = (1−f²)/2.  It exists so the no-go can be CONTROLLED: at p = 1 the
    potential is linear in the conductivity, the exponent is 0, and the
    spreading mode closes.  Section 5 of the finding names exactly that
    alternative; nothing had ever evaluated it.
    """
    A = np.asarray(A, float)
    p = float(bag_power)
    delta = (Phi ** 2 / (16.0 * p * B * A ** 2)) ** (1.0 / (p + 1.0))
    return Phi ** 2 / (4.0 * A * delta) + 4.0 * B * delta ** p * A, delta


# ---- direct transverse minimisation of the longitudinal dielectric tube ----
def _lap(f):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0)
            + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4.0 * f)


def _grad2(f):
    gx = 0.5 * (np.roll(f, -1, 0) - np.roll(f, 1, 0))
    gy = 0.5 * (np.roll(f, -1, 1) - np.roll(f, 1, 1))
    return gx * gx + gy * gy


def tube_tension_box(Phi, L, B=0.25, dtau=0.02, nit=40000, bag_power=2):
    """Minimise σ[f] = Σ[(∇f)² + B(1−f²)^p] + Φ²/(2 Σ(1−f²)) on an L×L box,
    Dirichlet f=1 at the edge (the only thing that localises the flux).
    Returns (sigma, f_core).  p = `bag_power` = 2 is the F139 quartic bag."""
    f = np.ones((L, L))
    c = L // 2
    X, Y = np.meshgrid(np.arange(L) - c, np.arange(L) - c, indexing="ij")
    f *= (1.0 - 0.9 * np.exp(-(X * X + Y * Y) / 50.0))   # melted-core seed

    def pin(g):
        g[0, :] = 1; g[-1, :] = 1; g[:, 0] = 1; g[:, -1] = 1
        return np.clip(g, 1e-4, 1.0)

    f = pin(f)
    for _ in range(nit):
        I = max(float((1.0 - f * f).sum()), 1e-9)
        Ec = Phi / I
        f = pin(f + dtau * (2.0 * _lap(f)
                            + 2.0 * bag_power * B * f
                            * (1.0 - f * f) ** (bag_power - 1)
                            - Ec * Ec * f))
    I = max(float((1.0 - f * f).sum()), 1e-9)
    sigma = (float((_grad2(f) + B * (1.0 - f * f) ** bag_power).sum())
             + Phi * Phi / (2.0 * I))
    return sigma, float(f.min())


# ---------------------------------------------------------------------------
#  T3 / T4 — the centre-algebra content (exact group theory).  The finding
#  tabulates both and says "all assertions in derive_dielectric_noconfine.py
#  pass"; no assertion for either was ever written.  These two functions and
#  the check entry below are that arithmetic, in rationals.
# ---------------------------------------------------------------------------
def su3_casimir_ratios():
    """sigma_R / sigma_F = C2(R) / C2(F) for the SU(3) reps F142 N3 tabulates.

    Quadratic Casimirs in the normalisation C2(fund) = (N^2-1)/(2N) = 4/3.
    Returned as exact Fractions, so the residual against the tabulated
    1, 9/4, 5/2, 9/2 is identically zero rather than 1e-16.
    """
    c2 = {"3": Fraction(4, 3), "3bar": Fraction(4, 3), "8": Fraction(3, 1),
          "6": Fraction(10, 3), "10": Fraction(6, 1)}
    cf = c2["3"]
    return {r: c / cf for r, c in c2.items()}


def su_n_k_string_ratios(N=3):
    """(Casimir-law, sine-law) sigma_k/sigma_1 for k = 1..N-1.

    Casimir law  sigma_k ∝ k(N-k);  sine law  sigma_k ∝ sin(k pi / N).
    F142 N4: for N = 3 both give sigma_2/sigma_1 = 1 exactly, because the
    k = 2 string is the antifundamental — the model fixes the SU(3) spectrum
    and cannot distinguish the two laws.  They split at N >= 4, which is what
    makes the SU(3) statement a fact about N = 3 and not an identity.
    """
    cas = [Fraction(k * (N - k), 1 * (N - 1)) for k in range(1, N)]
    sine = [np.sin(k * np.pi / N) / np.sin(np.pi / N) for k in range(1, N)]
    return cas, [float(x) for x in sine]


def check_dielectric_noconfine(Phi=12.0, v=1.0, e=1.0, n=1,
                               box_sizes=(61, 91, 141), nit=8000,
                               bag_power=2, B_box=0.25):
    """F142 gate entry — the dielectric tube cannot carry 2 pi v^2 n.

    F142 is a no-go plus a scope theorem, and it carried **no test record** in
    ``findings-index.md``: its module was "self-checking" through a printing
    ``main()``, which no runner reads and which two of the finding's five
    tabulated checks (T3, T4) were never written into at all.  This entry is
    the record, and it closes that gap — the finding's section 4 table now has
    an executable row for every line.

    Five legs:

    ``T1_bag_prefactor``
        Under the BPS dictionary B = e^2 v^4/4, Phi = 2 pi n/e, the thin-wall
        tension is Phi sqrt(2B) = (1/sqrt 2) . 2 pi v^2 n.  Right scaling in
        v^2 n, prefactor 1/sqrt2 — not 1.
    ``T2a_spread_exponent``
        The spread-thin minimiser gives sigma ∝ A^(-1/3): the analytic decade
        ratio is 10^(1/3) to 1e-6.  This is the no-go in closed form.
    ``T2b_box_tension_falls``
        A direct gradient-flow minimisation at fixed flux in a GROWING box:
        sigma must fall, and track L^(-2/3) to under 2 %.  A confining
        functional gives an L-independent sigma; this one does not.
    ``T3_casimir_ratios``
        sigma_R/sigma_F = C2(R)/C2(F) = 1, 9/4, 5/2, 9/2 for 3, 8, 6, 10, in
        exact rationals.
    ``T4_k_string_degeneracy``
        For SU(3) the Casimir and sine laws BOTH give sigma_2/sigma_1 = 1, and
        for SU(4) they do NOT agree — so the degeneracy is a property of N = 3,
        which is the whole content of N4.

    ``bag_power=1`` is the control, and it is the alternative the finding's own
    section 5 names: a potential LINEAR in the conductivity.  The cost per unit
    conductivity then stays bounded below, the spreading mode closes, the
    analytic exponent goes to 0 and the box tension stops falling — so both T2
    legs must go red while T1, T3 and T4, which never touch the bag exponent,
    stay green.  Without it, "the functional does not confine" is a statement
    about one numerical sweep rather than about the exponent.
    """
    Bc, Phi_dict, sigma_ano, sigma_bag = bag_dictionary(v=v, e=e, n=n)
    prefactor = sigma_bag / sigma_ano

    A = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
    s_spread, _ = spread_tension(Phi_dict, Bc, A, bag_power=bag_power)
    decade_ratio = float(np.mean(s_spread[:-1] / s_spread[1:]))
    expected_ratio = 10.0 ** ((bag_power - 1.0) / (bag_power + 1.0))

    sig, cores = [], []
    for L in box_sizes:
        sg, fc = tube_tension_box(Phi, L, B=B_box, nit=nit,
                                  bag_power=bag_power)
        sig.append(float(sg))
        cores.append(float(fc))
    Ls = np.asarray(box_sizes, float)
    pred = sig[0] * (Ls[0] / Ls) ** (2.0 / 3.0)
    box_rel = float(np.max(np.abs(np.asarray(sig) - pred) / pred))
    falls = bool(np.all(np.diff(sig) < 0.0))

    ratios = su3_casimir_ratios()
    want = {"3": Fraction(1, 1), "3bar": Fraction(1, 1), "8": Fraction(9, 4),
            "6": Fraction(5, 2), "10": Fraction(9, 2)}
    casimir_exact = all(ratios[k] == want[k] for k in want)

    cas3, sine3 = su_n_k_string_ratios(3)
    cas4, sine4 = su_n_k_string_ratios(4)
    su3_degenerate = (cas3[1] == Fraction(1, 1)
                      and abs(sine3[1] - 1.0) < 1e-15)
    su4_splits = abs(float(cas4[1]) - sine4[1]) > 0.05

    res = {
        "bag_power": int(bag_power),
        "dictionary": {"B": float(Bc), "Phi": float(Phi_dict),
                       "sigma_ANO_2pi_v2_n": float(sigma_ano),
                       "sigma_bag_thinwall": float(sigma_bag)},
        "bag_prefactor": float(prefactor),
        "one_over_sqrt2": float(1.0 / np.sqrt(2.0)),
        "spread_decade_ratio": decade_ratio,
        "spread_decade_ratio_expected": float(expected_ratio),
        "box_sizes": [int(L) for L in box_sizes],
        "box_sigma": sig,
        "box_f_core": cores,
        "box_Lminus2_3_max_rel": box_rel,
        "box_sigma_falls": falls,
        "su3_casimir_ratios": {k: str(v) for k, v in ratios.items()},
        "su3_k_string_casimir": [str(x) for x in cas3],
        "su3_k_string_sine": sine3,
        "su4_k_string_casimir": [str(x) for x in cas4],
        "su4_k_string_sine": sine4,
    }
    # bool(), not numpy.bool_: casim.tests.runner's leg extractor keys on
    # isinstance(v, bool), and np.bool_ is not a bool — a numpy truth value here
    # silently drops the leg and the control can never be judged against it.
    res["checks"] = {
        "T1_bag_prefactor": bool(abs(prefactor - 1.0 / np.sqrt(2.0)) < 1e-12),
        "T2a_spread_exponent": bool(
            abs(decade_ratio - 10.0 ** (1.0 / 3.0)) < 1e-6),
        "T2b_box_tension_falls": bool(falls and box_rel < 0.02),
        "T3_casimir_ratios": bool(casimir_exact),
        "T4_k_string_degeneracy": bool(su3_degenerate and su4_splits),
    }
    res["n_pass"] = int(sum(res["checks"].values()))
    res["n_checks"] = len(res["checks"])
    res["ok"] = res["n_pass"] == res["n_checks"]
    return res


def main():
    print("F142 Q1 — colour-dielectric tube vs F86 σ = 2π v² n\n")
    B, Phi, s_ano, s_bag = bag_dictionary(v=1.0, e=1.0, n=1)
    print("Dictionary (v=e=1, n=1, BPS):  B=%.4f  Φ=%.4f" % (B, Phi))
    print("  ANO topological  σ = 2π v² n      = %.4f" % s_ano)
    print("  thin-wall bag    σ = Φ√(2B)       = %.4f  (= %.4f · 2πv²n)"
          % (s_bag, s_bag / s_ano))
    assert abs(s_bag / s_ano - 1 / np.sqrt(2)) < 1e-12, "bag prefactor"

    print("\nSpread-thin config (analytic): σ ∝ A^(−1/3) → 0")
    A = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
    s, _ = spread_tension(Phi, B, A)
    ratios = s[:-1] / s[1:]
    print("  A:", A)
    print("  σ:", np.round(s, 4))
    print("  decade ratio σ(A)/σ(10A) = %.4f (10^(1/3)=%.4f)"
          % (ratios.mean(), 10 ** (1 / 3)))
    assert abs(ratios.mean() - 10 ** (1 / 3)) < 1e-6, "A^(-1/3) law"

    print("\nDirect minimisation (Φ=12, growing box): σ falls as L^(−2/3)")
    Ls = [61, 91, 141, 201]
    sig = []
    for L in Ls:
        sg, fc = tube_tension_box(12.0, L)
        sig.append(sg)
        print("  L=%3d  σ=%.4f  f_core=%.3f" % (L, sg, fc))
    # check decreasing and tracks L^(-2/3)
    pred = sig[0] * (Ls[0] / np.array(Ls, float)) ** (2.0 / 3.0)
    print("  L^(-2/3) prediction:", np.round(pred, 4))
    assert all(np.diff(sig) < 0), "tension must fall with box size (non-confining)"
    print("\n=> No-go confirmed: continuum ε=1−f² electric tube does not confine;")
    print("   F139's constant tension is a regulator effect; 2πv²n is the ANO")
    print("   vortex's topological charge, absent here.  Exact map: F99 centre route.")


if __name__ == "__main__":
    main()
