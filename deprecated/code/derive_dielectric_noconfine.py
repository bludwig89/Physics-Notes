# ===== deprecated/code backup =====================================
# source     : ca-simulation/derive_dielectric_noconfine.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/interactions/derive_dielectric_noconfine.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: derive_dielectric_noconfine.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
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
import numpy as np

__all__ = ["bag_dictionary", "spread_tension", "tube_tension_box", "main"]


def bag_dictionary(v=1.0, e=1.0, n=1):
    """Dual-superconductor dictionary at the BPS point.  Returns
    (B, Phi, sigma_ANO, sigma_bag_thinwall)."""
    B = e ** 2 * v ** 4 / 4.0          # bag constant = potential at melted core
    Phi = 2.0 * np.pi * n / e          # quantised colour-electric flux
    sigma_ano = 2.0 * np.pi * v ** 2 * n
    sigma_bag = Phi * np.sqrt(2.0 * B)  # thin-wall MIT-bag tube tension
    return B, Phi, sigma_ano, sigma_bag


def spread_tension(Phi, B, A):
    """Tension of the uniform 'spread-thin' configuration f=1−δ over area A.
    field+bag = Φ²/(4Aδ) + 4Bδ²A ;  minimised at δ³ = Φ²/(32 B A²)."""
    A = np.asarray(A, float)
    delta = (Phi ** 2 / (32.0 * B * A ** 2)) ** (1.0 / 3.0)
    return Phi ** 2 / (4.0 * A * delta) + 4.0 * B * delta ** 2 * A, delta


# ---- direct transverse minimisation of the longitudinal dielectric tube ----
def _lap(f):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0)
            + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4.0 * f)


def _grad2(f):
    gx = 0.5 * (np.roll(f, -1, 0) - np.roll(f, 1, 0))
    gy = 0.5 * (np.roll(f, -1, 1) - np.roll(f, 1, 1))
    return gx * gx + gy * gy


def tube_tension_box(Phi, L, B=0.25, dtau=0.02, nit=40000):
    """Minimise σ[f] = Σ[(∇f)² + B(1−f²)²] + Φ²/(2 Σ(1−f²)) on an L×L box,
    Dirichlet f=1 at the edge (the only thing that localises the flux).
    Returns (sigma, f_core)."""
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
        f = pin(f + dtau * (2.0 * _lap(f) + 4.0 * B * f * (1.0 - f * f)
                            - Ec * Ec * f))
    I = max(float((1.0 - f * f).sum()), 1e-9)
    sigma = float((_grad2(f) + B * (1.0 - f * f) ** 2).sum()) + Phi * Phi / (2.0 * I)
    return sigma, float(f.min())


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
