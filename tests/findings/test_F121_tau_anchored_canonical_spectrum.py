#!/usr/bin/env python3
"""
test_F121_tau_anchored_canonical_spectrum.py
============================================

F121 -- Adopt the tau as the canonical mass-scale anchor (it is wall-pinned, so
exactly delta-stable) and produce the standard mass-sector readout.

Why tau, not the electron (F120).  The lepton shape is the E_g condensate at
angle delta with equipartition A = sqrt2 ybar (F101), masses m_a = y_a^2 (F78),
heaviest wall-pinned (F101-A0): m_tau^cond = 1 for ALL delta.  So anchoring the
scale on the tau contributes ZERO angle sensitivity -- N_tau = m_tau(measured) --
and every prediction's error is purely the angle's error, not amplified by the
anchor.  The electron sits at the condensate node (~10x more delta-sensitive than
the muon, F120-C3), so it is the worst anchor.  This script makes tau the
standard and tabulates the canonical spectrum in MeV and kg.

    y_a = ybar (1 + sqrt2 cos theta_a),  theta_a = delta + 2 pi a/3,
    ybar = 1/(1 + sqrt2 cos delta)  (wall: y_tau = 1),   m_a = y_a^2,
    N_tau = m_tau^measured  =>  m_a^phys = N_tau * y_a^2.

Checks
------
  T1  Canonical tau-anchored lepton spectrum at the MEASURED angle
      (delta=12.733): predict m_mu, m_e in MeV and kg; both within ~0.1%.
  T2  Anchor stability: the tau contributes EXACTLY zero scale sensitivity
      (m_tau^cond=1 for all delta), so the prediction band is set only by the
      angle.  Quantify with the model angle (lambda6=1/4): m_mu to ~5%, while
      the same data anchored on the electron is off ~100% (F120) -- tau is the
      robust anchor.
  T3  Full fermion table in kg, tau-anchored (leptons predicted; quarks =
      measured-mass unit conversion, consistency).
  T4  Koide Q = 2/3 (anchor-independent geometric check).

Pure math (no scipy; CLAUDE.md).
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


# constants
EV = 1.602176634e-19
C = 2.99792458e8
MEV_KG = 1e6 * EV / C**2
S2 = math.sqrt(2.0)

PDG = {"electron": 0.51099895, "up": 2.16, "down": 4.67, "strange": 93.4,
       "muon": 105.6583755, "charm": 1270.0, "tau": 1776.86,
       "bottom": 4180.0, "top": 172690.0}
m_e, m_mu, m_tau = PDG["electron"], PDG["muon"], PDG["tau"]
DELTA_MEAS = 12.733
DELTA_MODEL = 13.363       # lambda6 = 1/4 (F119/F120)


def condensate(delta_deg):
    d = math.radians(delta_deg)
    ybar = 1.0 / (1 + S2 * math.cos(d))
    y = sorted([ybar * (1 + S2 * math.cos(d + 2 * math.pi * a / 3))
                for a in range(3)], reverse=True)        # [tau, mu, e]
    return y, [v * v for v in y]


def koide(m):
    return sum(m) / sum(math.sqrt(x) for x in m)**2


# ── T1: canonical tau-anchored spectrum (measured angle) ─────────────
y_m, m_m = condensate(DELTA_MEAS)
N_tau = m_tau / m_m[0]                 # m_m[0] == 1 (wall) -> N_tau = m_tau
mmu_pred = N_tau * m_m[1]
me_pred = N_tau * m_m[2]
err_mu = (mmu_pred - m_mu) / m_mu
err_e = (me_pred - m_e) / m_e
ok_t1 = abs(err_mu) < 3e-3 and abs(err_e) < 3e-3 and abs(m_m[0] - 1.0) < 1e-9
record("T1_canonical_tau_anchored_spectrum", ok_t1, {
    "angle (deg, measured)": DELTA_MEAS,
    "N_tau = m_tau (MeV)": m_tau, "m_tau^cond (wall)": round(m_m[0], 9),
    "m_mu pred (MeV)": round(mmu_pred, 4), "m_mu PDG": m_mu,
    "m_mu err": f"{err_mu*100:+.2f}%", "m_mu pred (kg)": f"{mmu_pred*MEV_KG:.6e}",
    "m_e pred (MeV)": round(me_pred, 5), "m_e PDG": m_e,
    "m_e err": f"{err_e*100:+.2f}%", "m_e pred (kg)": f"{me_pred*MEV_KG:.6e}",
    "statement": "tau-anchored canonical readout: from m_tau plus the measured "
                 "angle the equipartition shape gives m_mu to <0.1% and m_e to "
                 "~0.1%. The tau anchor adds zero scale error (m_tau^cond=1)."})

# ── T2: anchor stability — tau is exactly delta-stable ───────────────
def dln_ddelta(idx, delta_deg, h=1e-3):
    return abs((math.log(condensate(delta_deg + h)[1][idx])
                - math.log(condensate(delta_deg - h)[1][idx])) / (2 * h))
sens_tau = dln_ddelta(0, DELTA_MEAS)        # ~ 0 (wall)
sens_e = dln_ddelta(2, DELTA_MEAS)
# model-angle robustness, tau-anchored
yM, mM = condensate(DELTA_MODEL)
NtM = m_tau / mM[0]
errmu_model = (NtM * mM[1] - m_mu) / m_mu
# same data, electron-anchored (for contrast, F120)
NeM = m_e / mM[2]
errmu_e_model = (NeM * mM[1] - m_mu) / m_mu
ok_t2 = sens_tau < 1e-6 and abs(errmu_model) < 0.08 and abs(errmu_e_model) > 0.5
record("T2_tau_anchor_is_delta_stable", ok_t2, {
    "|dln(m_tau)/ddelta| (wall)": f"{sens_tau:.2e}",
    "|dln(m_e)/ddelta| (node)": round(sens_e, 3),
    "model-angle m_mu err, TAU-anchored": f"{errmu_model*100:+.1f}%",
    "model-angle m_mu err, electron-anchored (F120)": f"{errmu_e_model*100:+.0f}%",
    "statement": "the tau is EXACTLY delta-stable (m_tau^cond=1 for all delta), "
                 "so the anchor adds no error; with the model angle it predicts "
                 "m_mu to ~5% (the angle's error), vs ~100% when anchored on the "
                 "node-sitting electron. tau is the robust canonical anchor."})

# ── T3: full fermion table in kg (tau-anchored) ──────────────────────
table = {}
lep_pred = {"tau": m_tau, "muon": mmu_pred, "electron": me_pred}
for name in ("electron", "muon", "tau"):
    mev = lep_pred[name]
    e = (mev - PDG[name]) / PDG[name]
    table[name] = {"MeV_pred": round(mev, 5), "kg_pred": f"{mev*MEV_KG:.6e}",
                   "MeV_PDG": PDG[name], "err": ("anchor" if name == "tau"
                                                 else f"{e*100:+.2f}%"),
                   "tier": "ANCHOR" if name == "tau" else "PREDICTED (shape + m_tau)"}
for name in ("up", "down", "strange", "charm", "bottom", "top"):
    mev = PDG[name]
    table[name] = {"MeV": mev, "kg": f"{mev*MEV_KG:.6e}",
                   "tier": "CONSISTENCY (measured -> kg)"}
ok_t3 = abs((me_pred - m_e) / m_e) < 3e-3 and abs(err_mu) < 3e-3
record("T3_full_fermion_kg_table_tau_anchored", ok_t3, {
    "table": table,
    "statement": "canonical kg readout anchored on the tau: leptons predicted "
                 "by the shape (<=0.1% at the measured angle); quarks are the "
                 "measured masses converted to kg (consistency)."})

# ── T4: Koide ────────────────────────────────────────────────────────
ok_t4 = abs(koide(m_m) - 2/3) < 1e-5
record("T4_koide_two_thirds", ok_t4, {
    "Q condensate": round(koide(m_m), 6), "Q data (PDG)": round(koide([m_e, m_mu, m_tau]), 6),
    "statement": "Koide Q=2/3 holds geometrically, independent of the anchor."})

record("V_verdict", True, {
    "canonical anchor": "tau (wall-pinned, m_tau^cond=1, exactly delta-stable) "
        "-- adopted as the standard mass-scale anchor in place of the electron.",
    "canonical lepton readout (measured angle)": {
        "m_e (MeV)": round(me_pred, 5), "m_mu (MeV)": round(mmu_pred, 4),
        "m_tau (MeV)": m_tau},
    "open inputs (unchanged, F119)": "the overall scale N (=m_tau here) and the "
        "angle lambda6; everything else (ratios, Koide) is the derived shape.",
})

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "test-results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F121_tau_anchored_canonical_spectrum.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)

n_pass = sum(1 for r in RESULTS.values() if r["pass"])
print("\n" + "=" * 64)
print(f"F121 tau-anchored canonical spectrum: {n_pass}/{len(RESULTS)} PASS "
      f"-> {'PASS' if PASS else 'FAIL'} ({time.time()-T0:.0f}s)")
print(f"  canonical (measured angle, tau-anchored):")
print(f"    m_e  = {me_pred:.5f} MeV  ({err_e*100:+.2f}%)   = {me_pred*MEV_KG:.4e} kg")
print(f"    m_mu = {mmu_pred:.4f} MeV ({err_mu*100:+.2f}%)   = {mmu_pred*MEV_KG:.4e} kg")
print(f"    m_tau= {m_tau:.2f} MeV  (anchor)        = {m_tau*MEV_KG:.4e} kg")
print(f"  model-angle robustness: m_mu {errmu_model*100:+.1f}% (tau) vs {errmu_e_model*100:+.0f}% (electron)")
print("=" * 64)
sys.exit(0 if PASS else 1)
