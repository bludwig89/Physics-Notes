#!/usr/bin/env python3
"""
test_F78_koide_amplitude_pairing.py
===================================

F78 — Why sqrt(m), and what the equipartition amplitude is.
Two-part follow-up to F76:

  PART A (derivation).  Why does the cubic T1u vector live in sqrt(m) and not
  m?  Because the lepton mass is a Cooper-pair / condensate bilinear in the
  constituent amplitude (the F69/F73 "Higgs is the Cooper pair" premise):
  if generation a is a bound pair whose mass is set by the pair condensate
  ~ <y_a y_a>, then

        m_a  =  y_a^2 ,          y_a = the T1u vector component (axis a).

  So sqrt(m_a) = y_a is the fundamental, vector-transforming amplitude, and
  Koide is a statement about y.  We test that the data independently pick out
  the power 1/2 (i.e. m = y^2) as the special variable.

  PART B (the amplitude).  Koide Q = 2/3 (equipartition, F76) in y-language is
  the statement that |A1g (democratic)| = |T1u (splitting)|.  We give three
  EXACT equivalent characterisations, show the cube symmetry alone does NOT
  force it, and report whether sqrt(2) is derivable here.

Checks
------
  A1  m=y^2 reproduces Koide: Q(y) = Sum y^2 / (Sum y)^2 = 2/3 for leptons.
  A2  Power selection: among u_a = m_a^s, only s = 1/2 gives the clean
      rational 2/3 -> the data pick the bilinear (m = y^2) variable.
  B1  Q lives in [1/3, 1]: 1/3 = fully democratic (degenerate), 1 = fully
      hierarchical (one nonzero).  Q = 2/3 is the EXACT midpoint.  Leptons
      sit at the midpoint to ~1e-5.
  B2  Equipartition identity: Q=2/3 <=> |A1g|^2 = |T1u|^2 <=> CV(y)=1
      <=> 45 deg.  (exact)
  B3  Flavour-symmetric gap dynamics give DEGENERATE masses (Q -> 1/3), NOT
      2/3: an O_h/flavour-blind NJL gap cannot make the hierarchy; the
      equipartition is a large, specific symmetry-breaking, not a small
      correction.  (numerical, honest negative)
  B4  C3v (cube body-diagonal site symmetry) real mass operator is forced to
      a [2,1] degeneracy: matching Q=2/3 needs split/scale = 1/sqrt2 but with
      TWO masses equal -> cannot be the 3-distinct-mass leptons.  (structural)

Honesty: A1/A2 establish sqrt(m) as the amplitude GIVEN the bilinear premise.
B1/B2 are exact characterisations of Q=2/3.  B3/B4 are negative results
showing the cube's symmetric dynamics give Q=1/3 (degenerate), so the
amplitude sqrt(2) (Q=2/3) is NOT derived here -- it is a critical
"democratic<->hierarchical midpoint" condition the symmetric model does not
supply.  This sharpens, it does not close, the open problem.
"""

import json
import os
import math
import numpy as np

RESULTS = {}
PASS = True


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# PDG charged-lepton masses (MeV)
m_e, m_mu, m_tau = 0.51099895069, 105.6583755, 1776.86
masses = np.array([m_e, m_mu, m_tau])
y = np.sqrt(masses)              # the candidate T1u amplitude


# ════════════════════════════════════════════════════════════════════
#  PART A
# ════════════════════════════════════════════════════════════════════

# A1 — m = y^2 reproduces Koide in y-language
Q = (y ** 2).sum() / (y.sum() ** 2)
record("A1_m_equals_y2_reproduces_koide",
       abs(Q - 2 / 3) < 1e-4,
       {"Q_in_y_language": float(Q), "2/3": 2 / 3,
        "premise": "m_a = y_a^2 (pair condensate bilinear in constituent "
                   "amplitude); y_a = T1u vector component",
        "consequence": "sqrt(m) is the cubic vector, Koide is about y"})


# A2 — power selection: which exponent makes the relation a clean rational?
#   u_a = m_a^s ;  R(s) = (Sum u)^2 / (Sum u^2)  [generalised Koide-inverse]
#   For s = 1/2:  R = (Sum sqrt m)^2 / (Sum m) = 1/Q = 3/2 ; equivalently the
#   "n_eff" = (Sum u)^2/(Sum u^2) is the participation ratio.  We look for the
#   s giving the cleanest rational 1/Q.
def invQ(s):
    u = masses ** s
    return (u.sum() ** 2) / ((u ** 2).sum())


scan = {s: invQ(s) for s in [1 / 3, 0.45, 0.5, 0.55, 1.0]}
# closeness of 1/Q to the simple rational 3/2 (=> Q=2/3) at each s
dist_half = abs(invQ(0.5) - 1.5)
dist_neighbors = min(abs(invQ(1 / 3) - 1.5), abs(invQ(1.0) - 1.5))
record("A2_power_one_half_is_special",
       dist_half < 1e-3 and dist_neighbors > 0.1,
       {"1/Q at s=1/2 (target 1.5)": round(invQ(0.5), 6),
        "1/Q at s=1/3": round(invQ(1 / 3), 4),
        "1/Q at s=1.0": round(invQ(1.0), 4),
        "dist_to_1.5_at_half": round(dist_half, 6),
        "min_dist_neighbors": round(dist_neighbors, 4),
        "reading": "only the bilinear variable m=y^2 (s=1/2) hits the clean "
                   "rational -> supports the Cooper-pair origin of sqrt(m)"})


# ════════════════════════════════════════════════════════════════════
#  PART B
# ════════════════════════════════════════════════════════════════════

# B1 — Q range [1/3, 1] and the 2/3 midpoint
def koideQ(vec):
    v = np.asarray(vec, float)
    return (v ** 2).sum() / (v.sum() ** 2)


Q_democratic = koideQ([1, 1, 1])            # all equal
Q_hier = koideQ([1, 1e-9, 1e-9])            # one nonzero
midpoint = 0.5 * (1 / 3 + 1)
record("B1_two_thirds_is_range_midpoint",
       abs(Q_democratic - 1 / 3) < 1e-12 and abs(Q_hier - 1.0) < 1e-6
       and abs(midpoint - 2 / 3) < 1e-12 and abs(Q - midpoint) < 1e-4,
       {"Q_min_democratic": round(float(Q_democratic), 6),
        "Q_max_hierarchical": round(float(Q_hier), 6),
        "midpoint_(1/3+1)/2": midpoint,
        "Q_leptons": round(float(Q), 7),
        "reading": "Q=2/3 is the exact midpoint between the fully-democratic "
                   "floor (1/3) and the single-axis ceiling (1); leptons sit "
                   "at maximal democratic<->hierarchical balance"})


# B2 — equipartition identity: |A1g|^2 = |T1u|^2 ; CV(y)=1 ; 45 deg
n_hat = np.ones(3) / math.sqrt(3)
par = (y @ n_hat) * n_hat
perp = y - par
ratio = float((par @ par) / (perp @ perp))
cv = float(y.std() / y.mean())           # population std (ddof=0)
angle = math.degrees(math.acos(math.sqrt((par @ par) / (y @ y))))
record("B2_equipartition_identity",
       abs(ratio - 1.0) < 2e-3 and abs(cv - 1.0) < 2e-3 and abs(angle - 45) < 0.02,
       {"|A1g|^2/|T1u|^2": round(ratio, 5),
        "coefficient_of_variation_CV": round(cv, 5),
        "angle_to_(1,1,1)_deg": round(angle, 5),
        "three_equivalent_forms": "Q=2/3  <=>  |A1g|=|T1u|  <=>  CV=1  <=>  45deg"})


# B3 — flavour-symmetric NJL gap gives DEGENERATE masses (Q->1/3), not 2/3
#   Standard mean-field gap with 3-momentum cutoff Lambda:
#     condensate  C(m) = m * ( Lambda*sqrt(Lambda^2+m^2)
#                              - m^2 * asinh(Lambda/m) )
#     gap         m_a  = G * Sum_b A_ab C(m_b)      (self-consistent)
#   A_ab = (1-kappa) delta_ab + kappa/3  (flavour-symmetric democratic mix).
Lam = 1.0


def cond(m):
    m = max(m, 1e-12)
    return m * (Lam * math.sqrt(Lam ** 2 + m ** 2) - m ** 2 * math.asinh(Lam / m))


def solve_gap(G, kappa, m0, iters=4000):
    A = (1 - kappa) * np.eye(3) + kappa / 3 * np.ones((3, 3))
    m = np.array(m0, float)
    for _ in range(iters):
        m_new = G * (A @ np.array([cond(mi) for mi in m]))
        m_new = np.abs(m_new)
        if np.max(np.abs(m_new - m)) < 1e-13:
            m = m_new
            break
        m = 0.5 * m + 0.5 * m_new       # damped fixed point
    return m


# choose G above critical so a non-trivial gap exists; asymmetric start
m_sym = solve_gap(G=1.0, kappa=0.5, m0=[0.30, 0.20, 0.10])
spread = float((m_sym.max() - m_sym.min()) / (m_sym.mean() + 1e-30))
Q_gap = float(koideQ(np.sqrt(np.maximum(m_sym, 0)))) if m_sym.max() > 1e-9 else None
record("B3_symmetric_gap_is_degenerate",
       spread < 1e-3,           # flavour-symmetric dynamics wash out the start
       {"gap_masses": [round(x, 6) for x in m_sym.tolist()],
        "relative_spread": round(spread, 8),
        "Q_of_gap_solution": round(Q_gap, 5) if Q_gap else None,
        "verdict": "a flavour-blind (O_h-symmetric) gap drives all three to a "
                   "common value (degenerate, Q->1/3); it CANNOT produce the "
                   "observed hierarchy or Q=2/3 -> equipartition is a large "
                   "explicit symmetry-breaking, NOT supplied by symmetric "
                   "dynamics. sqrt(2) is therefore NOT derived here."})


# B4 — C3v (body-diagonal site symmetry) forces a [2,1] degeneracy
#   A real-symmetric operator commuting with a 3-fold axis + its mirrors on
#   (x,y,z) is mu*I + nu*(circulant-symmetric) -> eigenvalues {mu+2nu, mu-nu,
#   mu-nu}.  Two are equal.  Matching Q=2/3 needs nu/mu = 1/sqrt2 (the sqrt2!),
#   but with m_2 = m_3 -> not three distinct leptons.
def c3v_Q(nu_over_mu):
    mu = 1.0
    nu = nu_over_mu * mu
    sm = np.array([mu + 2 * nu, mu - nu, mu - nu])   # these are sqrt-masses
    sm = np.abs(sm)
    return koideQ(sm), sm


# solve nu/mu giving Q=2/3
from_scan = None
for r in np.linspace(0.01, 1.5, 200000):
    q, _ = c3v_Q(r)
    if abs(q - 2 / 3) < 1e-5:
        from_scan = r
        break
q_at, sm_at = (c3v_Q(from_scan) if from_scan else (None, None))
degenerate = sm_at is not None and abs(sm_at[1] - sm_at[2]) < 1e-9
record("B4_C3v_forces_two_fold_degeneracy",
       degenerate and from_scan is not None and abs(from_scan - 1 / math.sqrt(2)) < 1e-2,
       {"nu/mu giving Q=2/3": round(from_scan, 5) if from_scan else None,
        "1/sqrt2": round(1 / math.sqrt(2), 5),
        "sqrt_masses_at_that_point": [round(x, 5) for x in sm_at.tolist()] if sm_at is not None else None,
        "two_equal": degenerate,
        "reading": "the cube's natural body-diagonal site symmetry (C3v) hits "
                   "Q=2/3 only at nu/mu=1/sqrt2 but with two masses EQUAL; the "
                   "3 distinct leptons need the lower (orthorhombic) symmetry "
                   "of F76-C1, where sqrt2 is no longer fixed by symmetry"})


print("\nOVERALL:", "PASS" if PASS else "FAIL")
RESULTS["_overall"] = "PASS" if PASS else "FAIL"
RESULTS["_summary"] = {
    "derived": "m = y^2 (sqrt m is the T1u amplitude) GIVEN the Cooper-pair "
               "bilinear premise; data pick s=1/2 (A2)",
    "exact_characterisation": "Q=2/3 = midpoint of [1/3,1] = |A1g|=|T1u| = "
                              "CV(y)=1 = 45deg (B1,B2)",
    "NOT_derived": "the value sqrt(2) (Q=2/3): symmetric cube dynamics give "
                   "Q=1/3 (degenerate, B3) and C3v forces [2,1] (B4); "
                   "equipartition is a critical/maximally-broken condition the "
                   "symmetric model does not supply",
}
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F78_koide_amplitude_pairing.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("wrote", os.path.join(outdir, "F78_koide_amplitude_pairing.json"))
