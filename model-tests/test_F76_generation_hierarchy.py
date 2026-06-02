#!/usr/bin/env python3
"""
test_F76_generation_hierarchy.py
================================

F76 — Mass hierarchy of the three generations from a crystal-field splitting
of the F75 T1u triplet.  Follow-up to F75 (which fixed the *count* at three).

F75 left the three generations DEGENERATE (a protected T1u triplet at the
fully O_h-symmetric point).  A hierarchy m_e << m_mu << m_tau requires a
symmetry-lowering ("crystal-field") perturbation that splits T1u.  This script
asks what splitting the cubic geometry allows, and whether the observed
charged-lepton masses fit it.

Checks
------
  C1  Splitting pattern by subgroup (explicit degeneracy counting on the 3x3
      T1u mass operator):
        cubic O_h        ->  [3]      (degenerate, F75)
        tetragonal D_4h  ->  [2,1]    (one axis singled out)
        orthorhombic D_2h->  [1,1,1]  (three inequivalent axes)
      ==> three DISTINCT masses require breaking all the way to three
          inequivalent axes; T1u -> B1u (+) B2u (+) B3u.  This is a
          structural prediction: the 3 generations <-> the 3 orthorhombic
          axes (the T1u = vector components x,y,z).

  C2  LINEAR crystal field ruled out.  A perturbative split
      m_a = m0 + lambda*eps_a (Sum eps_a = 0) fit to the lepton masses needs
      |split|/mean of order 1 -- not a perturbation.  A linear (in m)
      crystal field CANNOT make the observed ratios.

  C3  The cubic-vector structure lives in sqrt(m), not m: the charged leptons
      satisfy Koide's relation Q = (Sum m)/(Sum sqrt m)^2 = 2/3 to ~1e-5.

  C4  Q = 2/3 is exactly "equipartition": sqrt(m) splits into an A1g cubic
      scalar M0*(1,1,1) plus a traceless T1u triplet of EQUAL length
      (angle 45 deg to the (1,1,1) democratic axis; cos^2 = 1/(3Q) = 1/2).

  C5  Falsifiable prediction.  Enforcing Q = 2/3 and using two measured
      masses predicts the third.  Predict m_tau from (m_e, m_mu) and m_e
      from (m_mu, m_tau); compare to PDG.

  C6  Z3 (cube threefold) parametrisation.  sqrt(m_a) = M0[1 + r cos(delta +
      2 pi a/3)] with r = sqrt(2) (the Q=2/3 amplitude).  Fit (M0, delta) to
      (m_e, m_mu); reconstruct all three; residual on m_tau.

Honest scope (see finding §Limitations): C1/C4 are exact structure; C3/C5/C6
are the empirical Koide content re-read in the model's cubic language.  The
amplitude sqrt(2) (i.e. Q=2/3) and the phase delta are NOT derived from the
QCA rule here -- they are the one constant + one angle the construction still
takes as input.  Quark / neutrino sectors are NOT fit by this (charged
leptons are the clean case); flagged, not claimed.
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


def degeneracies(diag, tol=1e-12):
    ev = np.sort(np.array(diag, float))
    groups = []
    for e in ev:
        if groups and abs(e - groups[-1][0]) < tol:
            groups[-1].append(e)
        else:
            groups.append([e])
    return sorted(len(g) for g in groups)


# ════════════════════════════════════════════════════════════════════
#  C1  Which symmetry lowering fully lifts the T1u triplet?
#  The T1u mass operator is a real-symmetric 3x3 acting on (x,y,z).
#  An O_h-symmetric field -> scalar (m0 I).  A field that singles out
#  axes adds diag pieces.  Count distinct levels for each subgroup.
# ════════════════════════════════════════════════════════════════════
m0 = 1.0
cubic = [m0, m0, m0]                       # O_h
tetragonal = [m0 + 0.3, m0 + 0.3, m0 - 0.6]  # D_4h: z-axis singled out
orthorhombic = [m0 + 0.3, m0 - 0.1, m0 - 0.2]  # D_2h: all axes inequivalent

dc, dt, do = degeneracies(cubic), degeneracies(tetragonal), degeneracies(orthorhombic)
record("C1_splitting_pattern",
       dc == [3] and dt == [1, 2] and do == [1, 1, 1],
       {"O_h_cubic": dc, "D4h_tetragonal": dt, "D2h_orthorhombic": do,
        "conclusion": "3 distinct masses require orthorhombic (3 inequivalent "
                      "axes): T1u -> B1u+B2u+B3u; generations <-> axes x,y,z"})


# ════════════════════════════════════════════════════════════════════
#  PDG charged-lepton masses (MeV)
# ════════════════════════════════════════════════════════════════════
m_e, m_mu, m_tau = 0.51099895069, 105.6583755, 1776.86
s_tau_unc = 0.12  # PDG uncertainty on m_tau (MeV)
masses = np.array([m_e, m_mu, m_tau])
sqrt_m = np.sqrt(masses)


# ════════════════════════════════════════════════════════════════════
#  C2  Linear-in-m crystal field is non-perturbative -> ruled out
#  m_a = m0 + lambda eps_a, Sum eps_a = 0  =>  m0 = mean(m), splits = m - mean
# ════════════════════════════════════════════════════════════════════
mean_m = masses.mean()
splits = masses - mean_m
rel = np.abs(splits) / mean_m
max_rel = float(rel.max())
record("C2_linear_crystal_field_ruled_out",
       max_rel > 0.5,   # splitting comparable to / larger than the mean
       {"mean_mass_MeV": float(mean_m),
        "splits_MeV": splits.round(3).tolist(),
        "max_|split|/mean": round(max_rel, 4),
        "verdict": "splitting >= mean -> NOT a perturbation; linear (in m) "
                   "crystal field cannot produce the observed ratios"})


# ════════════════════════════════════════════════════════════════════
#  C3  Koide relation  Q = (Sum m)/(Sum sqrt m)^2 = 2/3
# ════════════════════════════════════════════════════════════════════
Q = masses.sum() / (sqrt_m.sum() ** 2)
# propagate the dominant uncertainty (m_tau)
dQ_dmtau = (1 / sqrt_m.sum() ** 2) * (1 - 2 * masses.sum() / (sqrt_m.sum() * (2 * math.sqrt(m_tau))))
Q_unc = abs(dQ_dmtau) * s_tau_unc
record("C3_koide_two_thirds",
       abs(Q - 2 / 3) < 1e-4,
       {"Q": float(Q), "2/3": 2 / 3,
        "|Q-2/3|": float(abs(Q - 2 / 3)),
        "Q_uncertainty_from_m_tau": float(Q_unc),
        "n_sigma_from_2/3": float(abs(Q - 2 / 3) / Q_unc) if Q_unc else None})


# ════════════════════════════════════════════════════════════════════
#  C4  Q=2/3 <=> equipartition: sqrt(m) at 45 deg to the (1,1,1) axis.
#  cos^2(theta) = (sum sqrt m)^2 / (3 * sum m) = 1/(3Q).
#  Decompose sqrt(m) = parallel (A1g) + perp (traceless T1u triplet);
#  Q=2/3 means |parallel| = |perp|.
# ════════════════════════════════════════════════════════════════════
n_hat = np.ones(3) / math.sqrt(3)
par = (sqrt_m @ n_hat) * n_hat          # A1g component
perp = sqrt_m - par                      # traceless T1u triplet
cos2 = float((par @ par) / (sqrt_m @ sqrt_m))
angle_deg = math.degrees(math.acos(math.sqrt(cos2)))
equipart = float((par @ par) / (perp @ perp))   # = 1 when Q = 2/3
record("C4_equipartition_45deg",
       abs(angle_deg - 45.0) < 0.02 and abs(equipart - 1.0) < 1e-3,
       {"angle_sqrt_m_to_(1,1,1)_deg": round(angle_deg, 5),
        "cos^2 (=1/(3Q))": round(cos2, 8),
        "|A1g|^2 / |T1u-triplet|^2 (=1 at Q=2/3)": round(equipart, 6),
        "reading": "the cubic-scalar (A1g) and symmetry-breaking (T1u) parts "
                   "of sqrt(m) carry EQUAL weight"})


# ════════════════════════════════════════════════════════════════════
#  C5  Falsifiable prediction: enforce Q=2/3, use 2 masses, predict the 3rd.
#  x = sqrt(m_unknown):  x^2 - 4 S x + (3P - 2 S^2) = 0,  S=sum of known
#  sqrt-masses, P = sum of their squares.  Two roots; pick the physical one.
# ════════════════════════════════════════════════════════════════════
def koide_predict(known_two):
    s = np.sqrt(np.array(known_two, float))
    S, P = s.sum(), (s ** 2).sum()
    disc = 6 * S * S - 3 * P
    roots = [2 * S + math.sqrt(disc), 2 * S - math.sqrt(disc)]
    return [r ** 2 for r in roots]


tau_roots = koide_predict([m_e, m_mu])         # predict m_tau (heavy root)
m_tau_pred = max(tau_roots)
e_roots = koide_predict([m_mu, m_tau])         # predict m_e (light root)
m_e_pred = min([r for r in e_roots if r > 0])

err_tau = abs(m_tau_pred - m_tau) / m_tau
err_e = abs(m_e_pred - m_e) / m_e
record("C5_mass_prediction",
       err_tau < 2e-3,   # famous Koide tau prediction ~0.01-0.1%
       {"m_tau_predicted_MeV": round(m_tau_pred, 3),
        "m_tau_PDG_MeV": m_tau,
        "m_tau_rel_error": round(err_tau, 6),
        "m_tau_PDG_uncertainty_MeV": s_tau_unc,
        "m_e_predicted_MeV": round(m_e_pred, 6),
        "m_e_PDG_MeV": m_e,
        "m_e_rel_error": round(err_e, 6)})


# ════════════════════════════════════════════════════════════════════
#  C6  Z3 (cube threefold) parametrisation:
#  sqrt(m_a) = M0 [ 1 + sqrt(2) cos(delta + 2 pi a/3) ],  a = 0,1,2
#  Fit (M0, delta) to (m_e, m_mu); reconstruct all three; residual on m_tau.
# ════════════════════════════════════════════════════════════════════
def model_sqrt(M0, delta):
    return np.array([M0 * (1 + math.sqrt(2) * math.cos(delta + 2 * math.pi * a / 3))
                     for a in range(3)])


# brute-force fit on (M0, delta) to the two light masses (robust, no scipy)
target = np.array([math.sqrt(m_e), math.sqrt(m_mu)])
best = None
for delta in np.linspace(0, 2 * math.pi, 200001):
    cvals = np.array([1 + math.sqrt(2) * math.cos(delta + 2 * math.pi * a / 3)
                      for a in range(3)])
    # which two components are the two lightest? order by value
    order = np.argsort(cvals)
    # M0 from least-squares to the two lightest sqrt-masses
    c2 = cvals[order[:2]]
    if np.all(c2 > 0):
        M0 = float((c2 @ target) / (c2 @ c2))
        pred2 = M0 * c2
        resid = np.sum((pred2 - target) ** 2)
        if best is None or resid < best[0]:
            best = (resid, M0, delta, order)

_, M0_fit, delta_fit, order = best
sqrt_pred = np.sort(model_sqrt(M0_fit, delta_fit))
m_pred_all = np.sort(sqrt_pred ** 2)
m_tau_recon = m_pred_all[-1]
err_tau_recon = abs(m_tau_recon - m_tau) / m_tau
record("C6_Z3_cube_parametrisation",
       err_tau_recon < 5e-3,
       {"M0_fit": round(M0_fit, 6), "delta_fit_rad": round(delta_fit, 6),
        "reconstructed_masses_MeV": [round(x, 4) for x in m_pred_all.tolist()],
        "m_tau_reconstructed_MeV": round(m_tau_recon, 3),
        "m_tau_rel_error": round(err_tau_recon, 6),
        "note": "sqrt(m) = M0[1 + sqrt2 cos(delta+2pi a/3)] -- the cube's "
                "threefold (Z3 body-diagonal) phase structure; sqrt2<=>Q=2/3"})


# ════════════════════════════════════════════════════════════════════
#  Context: quarks & neutrinos do NOT obey Q=2/3 cleanly (honesty check)
# ════════════════════════════════════════════════════════════════════
up = np.array([2.16, 1270.0, 172690.0])      # u,c,t (MeV), PDG ~
down = np.array([4.67, 93.4, 4180.0])        # d,s,b (MeV), PDG ~
Q_up = up.sum() / (np.sqrt(up).sum() ** 2)
Q_down = down.sum() / (np.sqrt(down).sum() ** 2)
RESULTS["context_quark_Q"] = {"Q_up_type": float(Q_up), "Q_down_type": float(Q_down),
                              "note": "not 2/3 -> charged leptons are the special "
                                      "clean case; quark/neutrino fit is OPEN"}
print("[ctx] quark Q_up =", round(Q_up, 4), " Q_down =", round(Q_down, 4),
      "(not 2/3 -- leptons special)")


print("\nOVERALL:", "PASS" if PASS else "FAIL")
RESULTS["_overall"] = "PASS" if PASS else "FAIL"
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F76_generation_hierarchy.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("wrote", os.path.join(outdir, "F76_generation_hierarchy.json"))
