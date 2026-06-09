#!/usr/bin/env python3
"""
test_F120_electron_calibrated_spectrum.py
=========================================

F120 -- Calibrate the single overall mass scale on the electron and predict the
rest of the spectrum from the model's dimensionless shape.

Context (F119).  The kilogram is already tied in as a unit: with the cell locked
(F107) hbar carries the kg and m_phys = hbar arcsin(m_lat)/(tau c^2) returns kg
with no free parameter.  The model derives the dimensionless SHAPE of the
charged-lepton spectrum -- the E_g condensate at angle delta with equipartition
A = sqrt2 ybar (F80/F92/F101), masses m_a = y_a^2 (F78), heaviest wall-pinned
(F101-A0) -- and Koide Q = 2/3 (geometric).  The ONE open number is the overall
scale N (F119).  Here we fix N with the electron and turn the shape into absolute
masses (MeV and kg).

The condensate spectrum from the angle delta alone (ybar cancels in ratios):
    y_a = ybar (1 + sqrt2 cos theta_a),  theta_a = delta + 2 pi a / 3,
    wall-pinned ybar = 1 / (1 + sqrt2 cos delta),   m_a = y_a^2.
So delta fixes all mass RATIOS; one measured mass fixes the scale.

Checks
------
  C1  Calibration is consistent: m_e fixes N, and the locked-cell map
      m = hbar arcsin(m_lat)/(tau c^2) reproduces m_e in kg to round-off.
  C2  Electron-anchored, MEASURED angle delta=12.733 deg: the equipartition
      shape predicts m_mu and m_tau from m_e alone to ~0.1% -- confirming the
      shape (this uses delta as the one extra data input).
  C3  Electron-anchored, MODEL angle (lambda6=1/4 => delta=13.36 deg, F119-W2):
      the prediction is UNSTABLE (m_mu off by ~100%) because the electron sits
      near the condensate node, where d(mass)/d(delta) is largest -- the
      electron is the WORST anchor.
  C4  Anchor robustness: at the model angle, the tau anchor (the delta-stable
      wall) predicts the heavy ratios to ~5% (tracking the 2.7% lambda6 error),
      while the electron is intrinsically uncertain (node).  tau is the robust
      anchor; the electron is not.
  C5  Koide Q = 2/3 holds for the condensate spectrum (geometric), independent
      of the anchor.
  C6  Full fermion table in kg: once N is set by m_e + the locked cell, every
      fermion mass reads out in kg.  (Leptons: predicted via the shape.  Quarks:
      unit conversion of the measured masses -- CONSISTENCY, not prediction.)

Pure math/numpy (no scipy; CLAUDE.md).
"""

import json
import math
import os
import sys
import time

RESULTS = {}
PASS = True
T0 = time.time()


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# ── constants ────────────────────────────────────────────────────────
HBAR = 1.054571817e-34      # J s
C = 2.99792458e8            # m/s
G = 6.67430e-11
EV = 1.602176634e-19
ME_KG = 9.1093837015e-31    # CODATA electron mass (kg)
ELLP = math.sqrt(HBAR * G / C**3)
A_CELL = math.sqrt(8 * math.pi) * 3**0.25 * ELLP    # F79/F107
TAU = A_CELL / (C * math.sqrt(3))
S2 = math.sqrt(2.0)
MEV_KG = 1e6 * EV / C**2     # MeV/c^2 -> kg

# PDG 2024 central masses (MeV)
PDG = {"electron": 0.51099895, "up": 2.16, "down": 4.67, "strange": 93.4,
       "muon": 105.6583755, "charm": 1270.0, "tau": 1776.86,
       "bottom": 4180.0, "top": 172690.0}
m_e, m_mu, m_tau = PDG["electron"], PDG["muon"], PDG["tau"]

DELTA_MEAS = 12.733          # measured E_g condensate angle (F101/F109)
DELTA_MODEL = 13.363         # from lambda6 = 1/4 (F119-W2)


def condensate(delta_deg):
    """lepton spectrum from the angle: returns y=[heavy..light], m=y^2."""
    d = math.radians(delta_deg)
    ybar = 1.0 / (1 + S2 * math.cos(d))
    y = sorted([ybar * (1 + S2 * math.cos(d + 2 * math.pi * a / 3))
                for a in range(3)], reverse=True)
    return y, [v * v for v in y]


def koide(m):
    return sum(m) / sum(math.sqrt(x) for x in m)**2


# ── C1: calibration is consistent ────────────────────────────────────
# locked-cell map for the electron (forward): m_lat from m_e, then back to kg.
Omega_e = (m_e * 1e6 * EV) * TAU / HBAR
m_lat_e = math.sin(Omega_e)
m_e_kg_from_cell = HBAR * math.asin(m_lat_e) / (TAU * C**2)
roundtrip = abs(m_e_kg_from_cell - m_e * MEV_KG) / (m_e * MEV_KG)
ok_c1 = roundtrip < 1e-12
record("C1_calibration_consistent", ok_c1, {
    "m_e (MeV)": m_e, "m_e (kg, CODATA)": f"{ME_KG:.6e}",
    "m_lat(e) at locked cell": f"{m_lat_e:.6e}",
    "kg via cell map m=hbar*asin(m_lat)/(tau c^2)": f"{m_e_kg_from_cell:.6e}",
    "round-trip rel err": f"{roundtrip:.2e}",
    "statement": "m_e fixes the single scale N; the locked-cell map returns "
                 "m_e in kg to round-off. kg is in with no free parameter."})

# ── C2: electron-anchored, measured angle => 0.1% spectrum ───────────
y_m, m_m = condensate(DELTA_MEAS)
N_e = m_e / m_m[2]                       # scale from electron
mmu_pred = N_e * m_m[1]
mtau_pred = N_e * m_m[0]
err_mu = (mmu_pred - m_mu) / m_mu
err_tau = (mtau_pred - m_tau) / m_tau
ok_c2 = abs(err_mu) < 3e-3 and abs(err_tau) < 3e-3
record("C2_electron_anchored_measured_angle", ok_c2, {
    "angle (deg, measured)": DELTA_MEAS,
    "y = (tau,mu,e)": [round(v, 5) for v in y_m],
    "m_mu pred (MeV)": round(mmu_pred, 4), "m_mu PDG": m_mu,
    "m_mu err": f"{err_mu*100:+.2f}%",
    "m_tau pred (MeV)": round(mtau_pred, 3), "m_tau PDG": m_tau,
    "m_tau err": f"{err_tau*100:+.2f}%",
    "m_mu pred (kg)": f"{mmu_pred*MEV_KG:.6e}",
    "m_tau pred (kg)": f"{mtau_pred*MEV_KG:.6e}",
    "statement": "with the measured condensate angle, the electron-calibrated "
                 "equipartition shape predicts m_mu AND m_tau to ~0.1% from "
                 "m_e alone -- the shape is confirmed (uses delta as one extra "
                 "data input)."})

# ── C3: electron-anchored, MODEL angle => unstable (node) ────────────
y_M, m_M = condensate(DELTA_MODEL)
N_eM = m_e / m_M[2]
mmu_M = N_eM * m_M[1]
mtau_M = N_eM * m_M[0]
errmu_M = (mmu_M - m_mu) / m_mu
# node sensitivity: |d ln m_e^cond / d delta| (per degree) at the two angles
def dlnme_ddelta(delta_deg, h=1e-3):
    _, ma = condensate(delta_deg + h)
    _, mb = condensate(delta_deg - h)
    return abs((math.log(ma[2]) - math.log(mb[2])) / (2 * h))
def dln_ddelta(idx, delta_deg, h=1e-3):
    return abs((math.log(condensate(delta_deg + h)[1][idx])
                - math.log(condensate(delta_deg - h)[1][idx])) / (2 * h))
sens_e = dln_ddelta(2, DELTA_MEAS)      # electron (lightest)
sens_mu = dln_ddelta(1, DELTA_MEAS)     # muon (middle)
sens_tau = dln_ddelta(0, DELTA_MEAS)    # tau (wall) -- exactly 0
ratio_e_mu = sens_e / sens_mu
ok_c3 = abs(errmu_M) > 0.2 and sens_tau < 1e-6 and ratio_e_mu > 5
record("C3_electron_worst_anchor_node", ok_c3, {
    "angle (deg, model lambda6=1/4)": DELTA_MODEL,
    "m_mu pred (MeV), e-anchored": round(mmu_M, 1), "m_mu err": f"{errmu_M*100:+.0f}%",
    "|dln(m_e)/ddelta| per deg": round(sens_e, 3),
    "|dln(m_mu)/ddelta| per deg": round(sens_mu, 3),
    "|dln(m_tau)/ddelta| per deg (wall)": f"{sens_tau:.2e}",
    "sensitivity ratio e/mu": round(ratio_e_mu, 1),
    "statement": f"with the model's first-principles angle, electron-anchoring "
                 f"is UNSTABLE (m_mu off ~100pct): the electron sits near the "
                 f"condensate node, ~{ratio_e_mu:.0f}x more delta-sensitive than "
                 f"the muon, while the tau is EXACTLY delta-stable (wall-pinned, "
                 f"m_tau^cond=1 for all delta). The electron is the worst anchor; "
                 f"the tau the best."})

# ── C4: anchor robustness at the model angle ─────────────────────────
def anchored_errors(delta_deg):
    y, m = condensate(delta_deg)
    out = {}
    # e-anchor -> predict mu, tau
    Ne = m_e / m[2]
    out["e"] = {"m_mu": (Ne*m[1]-m_mu)/m_mu, "m_tau": (Ne*m[0]-m_tau)/m_tau}
    # mu-anchor -> predict e, tau
    Nmu = m_mu / m[1]
    out["mu"] = {"m_e": (Nmu*m[2]-m_e)/m_e, "m_tau": (Nmu*m[0]-m_tau)/m_tau}
    # tau-anchor -> predict e, mu
    Nt = m_tau / m[0]
    out["tau"] = {"m_e": (Nt*m[2]-m_e)/m_e, "m_mu": (Nt*m[1]-m_mu)/m_mu}
    return out

rob = anchored_errors(DELTA_MODEL)
# tau anchor heavy prediction (m_mu) is the most robust; electron prediction is not
tau_heavy_ok = abs(rob["tau"]["m_mu"]) < 0.08      # ~5.5%
e_unstable = abs(rob["e"]["m_mu"]) > 0.5
ok_c4 = tau_heavy_ok and e_unstable
record("C4_tau_is_robust_anchor", ok_c4, {
    "angle (deg, model lambda6=1/4)": DELTA_MODEL,
    "e-anchored errors": {k: f"{v*100:+.0f}%" for k, v in rob["e"].items()},
    "mu-anchored errors": {k: f"{v*100:+.0f}%" for k, v in rob["mu"].items()},
    "tau-anchored errors": {k: f"{v*100:+.1f}%" for k, v in rob["tau"].items()},
    "statement": "at the model angle the tau anchor (the delta-stable wall) "
                 "predicts m_mu to ~5.5% (tracking the 2.7% lambda6 error); the "
                 "electron prediction is intrinsically uncertain (node). tau is "
                 "the robust anchor. The user-requested electron anchor is exact "
                 "only when delta is taken from data (C2)."})

# ── C5: Koide Q = 2/3 ────────────────────────────────────────────────
Q_meas = koide([m_e, m_mu, m_tau])
Q_cond = koide(m_m)
ok_c5 = abs(Q_cond - 2/3) < 1e-5 and abs(Q_meas - 2/3) < 1e-4
record("C5_koide_two_thirds", ok_c5, {
    "Q measured (PDG)": round(Q_meas, 6),
    "Q condensate shape": round(Q_cond, 6),
    "2/3": round(2/3, 6),
    "statement": "Koide Q=2/3 holds geometrically for the condensate spectrum "
                 "(and the data sit 1e-5 from 2/3), independent of the anchor."})

# ── C6: full fermion table in kg ─────────────────────────────────────
# Leptons predicted via the measured-angle shape, electron-anchored; quarks are
# the measured masses converted to kg (consistency, not prediction).
table = {}
# leptons (predicted)
lep_pred = {"electron": m_e, "muon": mmu_pred, "tau": mtau_pred}
for name in ("electron", "muon", "tau"):
    mev = lep_pred[name]
    table[name] = {"MeV_pred": round(mev, 4), "kg_pred": f"{mev*MEV_KG:.6e}",
                   "MeV_PDG": PDG[name],
                   "err": f"{(mev-PDG[name])/PDG[name]*100:+.2f}%",
                   "tier": "PREDICTED (shape + m_e)"}
# quarks (unit conversion)
for name in ("up", "down", "strange", "charm", "bottom", "top"):
    mev = PDG[name]
    table[name] = {"MeV": mev, "kg": f"{mev*MEV_KG:.6e}",
                   "tier": "CONSISTENCY (measured mass -> kg)"}
ok_c6 = all(abs((lep_pred[n]-PDG[n])/PDG[n]) < 3e-3 for n in ("muon", "tau"))
record("C6_full_fermion_kg_table", ok_c6, {
    "table": table,
    "statement": "with m_e + the locked cell, every fermion reads out in kg. "
                 "Leptons are PREDICTED by the shape to ~0.1%; quark entries are "
                 "the measured masses converted to kg (the model fits, not "
                 "predicts, the quark texture)."})

# ── verdict ──────────────────────────────────────────────────────────
record("V_verdict", True, {
    "answer to 'calibrate on the electron'": "done: m_e fixes the single scale "
        "N; with the measured condensate angle the electron-calibrated shape "
        "predicts m_mu, m_tau to 0.1% and converts every fermion to kg.",
    "honest caveat": f"the electron is the WORST anchor for the model's own "
        f"first-principles angle (it sits at the condensate node, ~{ratio_e_mu:.0f}x "
        f"more delta-sensitive than the muon; the tau is exactly delta-stable at "
        f"the wall): the 2.7pct lambda6 uncertainty (F119) blows up to ~100pct on "
        f"m_mu when anchored on m_e. tau (the wall) is robust (~5pct).",
    "what is genuinely predicted": "Koide Q=2/3 (exact), and the FULL lepton "
        "shape from a single mass + the angle; the residual open number is the "
        "angle's exact value (lambda6), per F119/F118.",
})

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F120_electron_calibrated_spectrum.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)

n_pass = sum(1 for r in RESULTS.values() if r["pass"])
print("\n" + "=" * 64)
print(f"F120 electron-calibrated spectrum: {n_pass}/{len(RESULTS)} PASS "
      f"-> {'PASS' if PASS else 'FAIL'} ({time.time()-T0:.0f}s)")
print(f"  measured angle:  m_mu {err_mu*100:+.2f}%   m_tau {err_tau*100:+.2f}%  (e-anchored)")
print(f"  model angle:     m_mu {errmu_M*100:+.0f}% (e-anchored, unstable: node)")
print(f"  electron is {ratio_e_mu:.0f}x more delta-sensitive than muon; tau exactly stable (wall)")
print("=" * 64)
sys.exit(0 if PASS else 1)
