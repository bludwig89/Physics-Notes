"""
F60 — Reconciling the two induced-G channels:
      F58-Q3a (clock-rate stiffness, 1/G ~ c_lat^2 = 1/d)  vs
      F59/F56 (Sakharov loop,        1/G ~ 1/c_lat = sqrt d).

Thesis
------
They are NOT the same object. F58's "stiffness" is the |k|^2 coefficient of the
*bare* 6-neighbour wave operator, for which c_lat = sqrt(stiffness) identically
-- i.e. "stiffness = c_lat^2" is the kinematic identity  omega^2 = c_lat^2 |k|^2
of a TREE-LEVEL operator. F59's 1/(16 pi G) is the graviton kinetic stiffness
INDUCED by the matter loop (Sakharov), which scales as 1/c_lat. The two differ
by exactly c_lat^3 -- the tree-vs-loop gap. In the project's emergent-gravity
ontology (F52/F55/F57: gravity has NO fundamental kinetic term, it is generated
by matter back-reaction), the physical graviton stiffness is the induced one,
so 1/G ~ sqrt d and the F59 selection power d^(1/4) stands. F58-Q3a's c_lat^2 is
a correct statement about the bare operator, not about the physical coupling.

Checks (all on a common hopping/c_lat footing)
  (A) bare tree operator:   stiffness S_bare(J) and c_lat(J)  ->  S_bare = c_lat^2 exactly.
  (B) induced loop stiffness B(c_lat) = INT d3k/(2pi)^3 /(2 omega), omega=c_lat|k|
                                      ->  B ~ 1/c_lat (sqrt d).
  (C) gap B / S_bare ~ 1/c_lat^3  (= d^(3/2)) : tree-vs-loop.
  (D) convention-free clincher: the induced channel yields a dimensionless
      ell_P/a (= sqrt(1/(2 pi eta g_* )) d^(-1/4)); the bare-stiffness channel
      yields only an operator normalization, not a dimensionless coupling.

Real arithmetic only (arccos / linear dispersions) -> numpy safe per CLAUDE.md.
"""
from __future__ import annotations
import json, os
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))


# ---- (A) F58 bare tree-level wave-operator stiffness, common hopping J -------
def bare_stiffness_and_clat(J, kmax=1e-3, n=8, direction=(1, 1, 1)):
    """6-neighbour wave operator symbol  sym(k) = 4 J sum_i sin^2(k_i/2) ~ S |k|^2.
    The wave dispersion is omega = sqrt(sym) = sqrt(S)|k|, so c_lat = sqrt(S).
    Returns (S_bare, c_lat) for hopping J."""
    v = np.asarray(direction, float); v /= np.linalg.norm(v)
    ks = np.linspace(kmax/n, kmax, n)
    sym = np.array([4.0*J*sum(np.sin(kk*vi/2)**2 for vi in v) for kk in ks])
    S = float(np.polyfit(ks**2, sym, 1)[0])
    return S, float(np.sqrt(S))


# ---- (B) induced loop graviton stiffness, tunable c_lat ---------------------
def induced_stiffness(c_lat, Lam=0.8*np.pi, n=120):
    """B(c_lat) = INT_{|k|<Lam} d3k/(2pi)^3 * 1/(2 omega),  omega = c_lat |k|.
    Analytic: Lam^2/(8 pi^2 c_lat).  This is the F56/F59 induced 1/(16 pi G) weight."""
    g = np.linspace(-Lam, Lam, n, endpoint=False) + Lam/n
    KX, KY, KZ = np.meshgrid(g, g, g, indexing="ij")
    kk = np.sqrt(KX**2+KY**2+KZ**2)
    om = c_lat*kk
    integ = np.where((kk < Lam) & (om > 1e-12), 1.0/(2.0*om), 0.0)
    dk = g[1]-g[0]
    return float(integ.sum()*dk**3/(2*np.pi)**3)


def fit_power(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(np.abs(ys)), 1)[0])


if __name__ == "__main__":
    res = {}

    # (A) bare tree operator: sweep J, confirm S_bare = c_lat^2
    Js = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
    A_rows = []
    for J in Js:
        S, c = bare_stiffness_and_clat(J)
        A_rows.append({"J": float(J), "S_bare": S, "c_lat": c,
                       "S_over_clat2": S/c**2})
    res["A_bare"] = {"rows": A_rows,
                     "S_eq_clat2_spread": float(np.ptp([r["S_over_clat2"] for r in A_rows])),
                     "p_S_vs_clat": fit_power([r["c_lat"] for r in A_rows],
                                              [r["S_bare"] for r in A_rows])}
    print("(A) bare TREE operator:  S_bare = c_lat^%.4f ; S/c_lat^2 spread = %.2e"
          % (res["A_bare"]["p_S_vs_clat"], res["A_bare"]["S_eq_clat2_spread"]))

    # (B) induced loop stiffness: sweep c_lat, confirm B ~ 1/c_lat
    cs = np.array([1/np.sqrt(4), 1/np.sqrt(3), 1/np.sqrt(2), 1/np.sqrt(1.5), 1.0])
    Bs = np.array([induced_stiffness(c) for c in cs])
    res["B_induced"] = {"c_lat": [float(x) for x in cs], "B": [float(x) for x in Bs],
                        "p_B_vs_clat": fit_power(cs, Bs),
                        "B_times_clat": [float(b*c) for b, c in zip(Bs, cs)]}
    print("(B) induced LOOP stiffness: B = c_lat^%.4f ; B*c_lat const = %.6f"
          % (res["B_induced"]["p_B_vs_clat"], np.mean(res["B_induced"]["B_times_clat"])))

    # (C) the gap: B / S_bare vs c_lat  ->  exponent -3 (tree-vs-loop)
    #     evaluate both at common c_lat (use bare with J chosen so c_lat matches)
    gap_rows = []
    for c in cs:
        Jc = c**2                         # since c_lat = sqrt(J) for the bare op
        S, cc = bare_stiffness_and_clat(Jc)
        B = induced_stiffness(c)
        gap_rows.append({"c_lat": float(c), "S_bare": S, "B": B, "ratio_B_over_S": B/S})
    res["C_gap"] = {"rows": gap_rows,
                    "p_ratio_vs_clat": fit_power([r["c_lat"] for r in gap_rows],
                                                 [r["ratio_B_over_S"] for r in gap_rows])}
    print("(C) gap  B/S_bare = c_lat^%.4f   (expect -3 = tree-vs-loop, = d^{3/2})"
          % res["C_gap"]["p_ratio_vs_clat"])

    # (D) convention-free clincher: dimensionless a/ell_P vs d from each channel.
    #     induced:  a/ell_P = sqrt(2 pi eta g_*) d^(1/4)        (well-defined coupling)
    #     bare:     1/G ~ c_lat^2 = 1/d  =>  a/ell_P ~ d^(-1/4)  (if read as a coupling)
    eta, g_star = 1/12, 2
    P = np.sqrt(2*np.pi*eta*g_star)
    res["D_selection"] = {
        "induced_channel": {"law": "a/ellP = sqrt(2 pi eta g_*) d^(1/4)",
                            "d2": P*2**0.25, "d3": P*3**0.25, "d4": P*4**0.25},
        "bare_channel":    {"law": "a/ellP ~ d^(-1/4) (if 1/G = c_lat^2 read as coupling)",
                            "d2": P*2**-0.25, "d3": P*3**-0.25, "d4": P*4**-0.25},
    }
    print("(D) selection power: induced a/ellP ~ d^(+1/4); bare 'coupling' a/ellP ~ d^(-1/4)")
    print("    induced d=3: a=%.3f ellP   bare d=3: a=%.3f ellP"
          % (res["D_selection"]["induced_channel"]["d3"],
             res["D_selection"]["bare_channel"]["d3"]))

    with open(os.path.join(OUT, "f60_results.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("wrote f60_results.json")
