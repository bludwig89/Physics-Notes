"""
ca_lpt_ward.py — the 3-gluon vertex closed form + the Ward-Takahashi identity,
verified SYMBOLICALLY (sympy). The rigorous structural validation that the
numerical extractor (ca_lpt_vertex) could only partly reach, and the gauge
identity the one-loop self-energy assembly depends on.

Result (verified here, exactly, for all Lorentz components in d=4):
  the colour-stripped 3-gluon vertex (all momenta incoming, p1+p2+p3=0)
      Gamma_{m1 m2 m3}(p1,p2,p3) = d_{m1m2}(p1-p2)_{m3}
                                 + d_{m2m3}(p2-p3)_{m1}
                                 + d_{m3m1}(p3-p1)_{m2}
  satisfies the Ward-Takahashi identity
      p1^{m1} Gamma_{m1 m2 m3}(p1,p2,p3) = Dinv_{m2 m3}(p3) - Dinv_{m2 m3}(p2),
  with the transverse inverse propagator  Dinv_{ab}(p) = p^2 d_{ab} - p_a p_b.

This ties the vertex to the propagator (already validated, ca_lpt_wilson /
ca_lpt_vertex). On the lattice the same identity holds with the continuum
momenta/propagator replaced by their lattice forms (k_hat etc.) plus the
point-splitting cosine form factors; the continuum identity verified here is the
a->0 limit and the gauge-invariance backbone of the d1 computation.

IMPORTANT scoping note for the loop (honest):
  Extracting b0 = 11/3 C_A (the validation gate for the self-energy) requires the
  BACKGROUND-FIELD formalism, where the coupling renormalisation comes from the
  background self-energy alone (Z_g = Z_A^{-1/2}). In ordinary Feynman gauge the
  gluon vacuum polarisation is NOT transverse by itself and does NOT give b0
  without the vertex correction — so the loop must be assembled with the
  background-field vertices, not the plain ones. That is the precise remaining
  step (see docs/design/qstar-gluon-d1-computation-plan.md).

sympy only.
"""
from __future__ import annotations

import sympy as sp


def _gamma(p1, p2, p3, d):
    """Colour-stripped continuum 3-gluon vertex tensor (list-of-lists)."""
    def dl(i, j):
        return 1 if i == j else 0
    G = [[[dl(m1, m2) * (p1[m3] - p2[m3])
           + dl(m2, m3) * (p2[m1] - p3[m1])
           + dl(m3, m1) * (p3[m2] - p1[m2])
           for m3 in range(d)] for m2 in range(d)] for m1 in range(d)]
    return G


def _dinv(p, a, b, d):
    p2 = sum(p[i] ** 2 for i in range(d))
    return p2 * (1 if a == b else 0) - p[a] * p[b]


def ward_identity_symbolic(d: int = 4) -> dict:
    """Verify p1.Gamma = Dinv(p3) - Dinv(p2) for ALL (m2,m3), exactly."""
    a = sp.symbols(f"a0:{d}")
    b = sp.symbols(f"b0:{d}")
    p1 = list(a)
    p2 = list(b)
    p3 = [-(a[i] + b[i]) for i in range(d)]
    G = _gamma(p1, p2, p3, d)
    mism = []
    for m2 in range(d):
        for m3 in range(d):
            lhs = sp.expand(sum(p1[m1] * G[m1][m2][m3] for m1 in range(d)))
            rhs = sp.expand(_dinv(p3, m2, m3, d) - _dinv(p2, m2, m3, d))
            if sp.simplify(lhs - rhs) != 0:
                mism.append((m2, m3))
    return {"d": d, "all_components_hold": len(mism) == 0,
            "n_components": d * d, "mismatches": mism,
            "statement": "p1.Gamma = Dinv(p3)-Dinv(p2) verified exactly for all "
                         f"{d*d} components (sympy) — vertex structure + gauge "
                         "identity validated; ties vertex to the propagator"}


def bose_symmetry_symbolic(d: int = 4) -> dict:
    """The colour-stripped Gamma is ANTI-symmetric under simultaneous
    (Lorentz+momentum) exchange of two legs:
        Gamma_{m2m1m3}(p2,p1,p3) = - Gamma_{m1m2m3}(p1,p2,p3).
    The full vertex V = f^{abc} Gamma is then Bose-SYMMETRIC, because f^{abc} is
    antisymmetric (the two signs cancel). Verify the antisymmetry exactly."""
    a = sp.symbols(f"a0:{d}"); b = sp.symbols(f"b0:{d}")
    p1 = list(a); p2 = list(b); p3 = [-(a[i] + b[i]) for i in range(d)]
    G = _gamma(p1, p2, p3, d)
    Gs = _gamma(p2, p1, p3, d)        # swap legs 1<->2 (Lorentz+momentum)
    bad = []
    for m1 in range(d):
        for m2 in range(d):
            for m3 in range(d):
                if sp.simplify(Gs[m2][m1][m3] + G[m1][m2][m3]) != 0:
                    bad.append((m1, m2, m3))
    return {"all_hold": len(bad) == 0, "mismatches": bad,
            "statement": "colour-stripped Gamma antisymmetric under leg 1<->2 "
                         "exchange => full vertex f^{abc}Gamma is Bose-symmetric "
                         "(verified symbolically)"}


def report() -> dict:
    return {"ward_identity": ward_identity_symbolic(),
            "bose_symmetry": bose_symmetry_symbolic()}


if __name__ == "__main__":
    import json
    print(json.dumps(report(), indent=2, default=str))
