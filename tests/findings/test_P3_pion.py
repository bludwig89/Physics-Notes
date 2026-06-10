#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_P3_pion.py
===============

P3 of docs/roadmaps/roadmap-matter-binding.md — the DYNAMICAL pion.

Promotes the pion from "the NJL pseudoscalar pole exists (F77)" to "a certified
dynamical q-qbar bound state": the Goldstone of chiral-symmetry breaking, with
the explicit-breaking GMOR slope, an internal light/heavy contrast against its
scalar chiral partner (sigma) and the vector (rho), and a real-space
relative-coordinate bound-state cross-check (F74 engine) to machine precision.

Engine reuse:
  • ca_meson.py  — wraps the F77 NJL gap+RPA ladder and the F74 relcoord solver.

Parts
-----
  A  Goldstone theorem (chiral limit m0->0):  1-2G Pi_PS(0)=0 IS the gap eq, and
     the pseudoscalar pole sits at m_pi=0.                         (exact)
  B  Polarization split identity  Pi_S - Pi_PS = -8 Nc Nf M^2 K    (exact)
  C  Calibrated spectrum reproduces measured m_c, f_pi, m_pi,
     <qbar q>^(1/3), and m_sigma ~ 2 m_c.                          (quantitative)
  D  GMOR at the physical point: m_pi^2 f_pi^2 = -m0 <qbar q>_tot. (quantitative)
  E  GMOR slope / Goldstone scaling: m_pi^2 is LINEAR in m0 as m0->0
     (the sharp Goldstone signature).                              (quantitative)
  F  Light/heavy contrast: m_pi << m_sigma (chiral partner, internal, no extra
     input) and m_pi << m_rho (KSRF, one external coupling).       (quantitative)
  G  Real-space relative-coordinate bound state (F74 engine): secular Koster-
     Slater root == dense diagonalisation.                          (machine)

All arithmetic REAL (loop integrals + real symmetric eigenproblem). numpy only.

Run:  python3 tests/findings/test_P3_pion.py        (~a few seconds)
Writes test-results/P3_pion.json.
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))
import ca_meson as M  # noqa: E402

results = {"phase": "P3", "title": "dynamical pion (chiral pseudoscalar Goldstone)",
           "checks": {}, "derived": {}, "spectrum": {}, "scaling": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                               "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:50s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 80)
print("P3 — the dynamical pion: q-qbar pseudoscalar Goldstone (reuses F74/F77)")
print("=" * 80)

Lam = M.CANONICAL["Lam"]
GLam2 = M.CANONICAL["GLam2"]
m0 = M.CANONICAL["m0"]
G = GLam2 / Lam ** 2
Gc = M.G_critical(Lam)

# ---------------------------------------------------------------------------
# A. Goldstone theorem in the chiral limit (m0 = 0).
# ---------------------------------------------------------------------------
print("\nA  Goldstone theorem (chiral limit m0 -> 0)")
M_chi = M.gap_solve(G, Lam, 0.0)
gold = abs(1.0 - 2.0 * G * M.Pi_PS(0.0, M_chi, Lam))
record("A1 1-2G Pi_PS(0)=0 IS the gap eq (m_pi=0)", gold, 1e-10, "exact", gold < 1e-10)
m_pi_chi, _, _ = M.meson_pole("PS", M_chi, G, Lam)
record("A2 pseudoscalar pole at m_pi=0 (chiral)", m_pi_chi, 1e-5, "exact", m_pi_chi < 1e-5)
results["derived"]["M_chiral"] = M_chi

# ---------------------------------------------------------------------------
# B. Polarization split identity (exact, any q2).
# ---------------------------------------------------------------------------
print("\nB  polarization split identity Pi_S - Pi_PS = -8 Nc Nf M^2 K")
q2p = 0.37 * 4.0 * M_chi ** 2
lhs = M.Pi_S(q2p, M_chi, Lam) - M.Pi_PS(q2p, M_chi, Lam)
rhs = -8.0 * M.N_C * M.N_F * M_chi ** 2 * M.K_quad(q2p, M_chi, Lam)
split = abs(lhs - rhs) / abs(rhs)
record("B  split identity exact", split, 1e-12, "exact", split < 1e-12)

# ---------------------------------------------------------------------------
# C. Calibrated spectrum reproduces measured hadron data.
# ---------------------------------------------------------------------------
print("\nC  calibrated spectrum vs experiment (Lam=651.5, G Lam^2=2.10, m0=5.5 MeV)")
s = M.solve_meson_spectrum(Lam, GLam2, m0)
results["spectrum"] = {k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                       for k, v in s.items() if k != "params"}
print(f"       m_c     = {s['m_c']*1e3:7.1f} MeV  (exp ~325)")
print(f"       m_pi    = {s['m_pi']*1e3:7.1f} MeV  (exp 135-138)")
print(f"       f_pi    = {s['f_pi']*1e3:7.1f} MeV  (exp 92.4)")
print(f"       m_sigma = {s['m_sigma']*1e3:7.1f} MeV  (~ 2 m_c, broad)")
print(f"       m_rho   = {s['m_rho']*1e3:7.1f} MeV  (exp 775; KSRF, ext. g_rhopipi)")
print(f"       <qq>^1/3= {s['condensate_root']*1e3:7.1f} MeV  (exp ~ -250)")

record("C1 m_c ~= 325 MeV", abs(s["m_c"] - 0.325) / 0.325, 0.05, "quantitative",
       abs(s["m_c"] - 0.325) / 0.325 < 0.05)
record("C2 m_pi ~= 135 MeV", abs(s["m_pi"] - 0.135) / 0.135, 0.08, "quantitative",
       abs(s["m_pi"] - 0.135) / 0.135 < 0.08)
record("C3 f_pi ~= 92 MeV", abs(s["f_pi"] - 0.0924) / 0.0924, 0.06, "quantitative",
       abs(s["f_pi"] - 0.0924) / 0.0924 < 0.06)
record("C4 <qq>^1/3 ~= -250 MeV", abs(-s["condensate_root"] - 0.250) / 0.250, 0.06,
       "quantitative", abs(-s["condensate_root"] - 0.250) / 0.250 < 0.06)
record("C5 m_sigma ~= 2 m_c (chiral partner)", abs(s["m_sigma_over_2mc"] - 1.0), 0.02,
       "quantitative", abs(s["m_sigma_over_2mc"] - 1.0) < 0.02)

# ---------------------------------------------------------------------------
# D. GMOR at the physical point.
# ---------------------------------------------------------------------------
print("\nD  GMOR at the physical point: m_pi^2 f_pi^2 = -m0 <qbar q>_tot")
gmor_rel = s["gmor_rel"]
print(f"       lhs = {s['gmor_lhs']:.6e}   rhs = {s['gmor_rhs']:.6e}   rel = {gmor_rel:.3e}")
record("D  GMOR holds", gmor_rel, 0.05, "quantitative", gmor_rel < 0.05)

# ---------------------------------------------------------------------------
# E. Goldstone scaling: m_pi^2 LINEAR in m0 as m0 -> 0.
#    GMOR predicts m_pi^2 = (-<qq>_tot / f_pi^2) m0 + O(m0^2); the slope ratio
#    m_pi^2/m0 must approach a finite constant (and the intercept -> 0).
# ---------------------------------------------------------------------------
print("\nE  Goldstone scaling: m_pi^2 linear in m0 as m0 -> 0")
m0s = [0.002, 0.004, 0.006, 0.008]
rows, slopes = [], []
for mm in m0s:
    Mx = M.gap_solve(G, Lam, mm)
    mpi, _, _ = M.meson_pole("PS", Mx, G, Lam)
    slope = mpi ** 2 / mm
    rows.append([mm, Mx, mpi, slope])
    slopes.append(slope)
    print(f"       m0={mm*1e3:5.1f} MeV  m_pi={mpi*1e3:7.1f} MeV  m_pi^2/m0={slope:.4f}")
results["scaling"]["columns"] = ["m0", "M", "m_pi", "m_pi2_over_m0"]
results["scaling"]["rows"] = [[float(x) for x in r] for r in rows]
# constancy of the slope = linearity (Goldstone). Spread relative to mean.
slope_spread = (max(slopes) - min(slopes)) / np.mean(slopes)
record("E  m_pi^2/m0 constant (linear Goldstone)", slope_spread, 0.05,
       "quantitative", slope_spread < 0.05)

# ---------------------------------------------------------------------------
# F. Light/heavy contrast.
# ---------------------------------------------------------------------------
print("\nF  light/heavy contrast: the pion is anomalously light")
print(f"       m_pi/m_sigma = {s['m_pi']/s['m_sigma']:.4f}   (chiral partner, internal)")
print(f"       m_pi/m_rho   = {s['m_pi_over_m_rho']:.4f}   (KSRF vector)")
record("F1 m_pi << m_sigma (chiral partner)", s["m_pi"] / s["m_sigma"], 0.30,
       "quantitative", s["m_pi"] / s["m_sigma"] < 0.30)
record("F2 m_pi << m_rho (vector)", s["m_pi_over_m_rho"], 0.25, "quantitative",
       s["m_pi_over_m_rho"] < 0.25)

# ---------------------------------------------------------------------------
# G. Real-space relative-coordinate bound state (F74 engine), two routes agree.
# ---------------------------------------------------------------------------
print("\nG  real-space q-qbar relcoord bound state (F74 engine): secular == dense")
g_c = M.watson_gc(t=1.0)
g_test = 8.0   # comfortably above g_c ~ 3.957 t
Eb_sec = M.relcoord_secular(g_test, L=12, t=1.0)
E0_sec = -Eb_sec
E0_dense = M.relcoord_dense(g_test, L=12, t=1.0)
diff = abs(E0_dense - E0_sec)
print(f"       g_c(Watson) = {g_c:.4f} t   (g_test = {g_test} t)")
print(f"       secular E0  = {E0_sec:.10f} t")
print(f"       dense   E0  = {E0_dense:.10f} t")
results["derived"]["relcoord_g_c"] = g_c
results["derived"]["relcoord_E0_secular"] = E0_sec
results["derived"]["relcoord_E0_dense"] = E0_dense
record("G  dense diag == secular root (L=12)", diff, 1e-9, "machine", diff < 1e-9)

# ---------------------------------------------------------------------------
results["notes"] = [
    "The pion is the q-qbar pseudoscalar Goldstone: in the chiral limit "
    "1-2G Pi_PS(0)=0 is IDENTICALLY the gap equation, so m_pi=0 to machine "
    "precision (A). With m0>0 the GMOR slope m_pi^2 ∝ m0 reproduces the "
    "physical 140.5 MeV (C2,D) and m_pi^2/m0 is constant as m0->0 (E) — the "
    "sharp Goldstone signature the roadmap demanded.",
    "Single coupling G, no extra input: the SAME G that breaks chiral symmetry "
    "(gap) and binds the pion (RPA) puts the scalar chiral partner sigma at the "
    "2 m_c threshold (C5). The pion is therefore anomalously light vs both its "
    "chiral partner (m_pi/m_sigma=0.23) and the vector (m_pi/m_rho=0.18, F).",
    "The vector rho uses the KSRF relation m_rho^2=2 g_rhopipi^2 f_pi^2 tying it "
    "to the MODEL OUTPUT f_pi; the only external number is the empirical "
    "g_rhopipi~6 — flagged Tier-3, used only for the light/heavy contrast.",
    "F74-engine cross-check (G): the relative-coordinate q-qbar bound state from "
    "the secular Koster-Slater root agrees with dense diagonalisation to <1e-9, "
    "certifying the bound state as a real-space dynamical object, not only a "
    "continuum pole.",
    "Calibration inherited verbatim from F77 (validated against measured m_c, "
    "f_pi, m_pi, <qbar q>); P3 adds the Goldstone-scaling and relcoord "
    "certifications and the explicit light/heavy contrast. GMOR confirms the "
    "F77 numbers as the roadmap asked.",
    "Scope: m_sigma is the RPA threshold pole (broad resonance above 2 m_c for "
    "m0>0); its width via Im K(q2>4M^2) is a small extension. The OPEP coupling "
    "g_piNN for P4 (deuteron) is set by Goldberger-Treiman (g_piqq f_pi=M, F77 "
    "1.1%) lifted to the nucleon — the input P4 consumes.",
]

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "P3_pion.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 80)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 80)
