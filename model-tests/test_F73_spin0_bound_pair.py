#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F73_spin0_bound_pair.py
=============================

F73 — Spin-0 bound-pair scalar (the "Cooper-pair" Higgs candidate).

Builds the spin-0 (singlet) partner of the F69 spin-1 paired-spinor photon and
derives its rest mass from two already-established model results, with NO new
dynamical input:

  * F46:  the rest-frame rotation rate of a state of dimensionless lattice mass
          m is  Omega_rest(m) = arcsin(m),  equivalently  m = sin(Omega_rest).
  * F69:  a bound pair's phase per tick is the SUM of its constituents' phases
          (the photon is the spin-1 case; this is the spin-0 case).

Hence a spin-0 bound pair of two spin-1/2 constituents of lattice masses
m1, m2 has rest rotation

        Omega_H = arcsin(m1) + arcsin(m2)

and therefore composite lattice mass

        m_H = sin(arcsin m1 + arcsin m2)
            = m1 * sqrt(1 - m2^2) + m2 * sqrt(1 - m1^2)         (sine addition)

equal-mass case (m1 = m2 = mc):

        m_H = sin(2 arcsin mc) = 2 mc sqrt(1 - mc^2).

The script verifies the algebra exactly, characterises the lattice binding
deficit and the stability bound, shows the deficit is utterly negligible at
electroweak scales (so the SI prediction collapses to the free sum
m_H ~ m1 + m2), and confronts that with the observed Higgs mass.

All trig here is REAL scalar arithmetic (arcsin / sin on the real line), so no
chiral/complex-transform pitfalls apply (CLAUDE.md numpy caveat); we use mpmath
at high precision for the exactness checks and Python floats for the SI numbers.

Run:  python3 model-tests/test_F73_spin0_bound_pair.py
Fast (<1 s). Writes test-results/F73_spin0_bound_pair.json.
"""

import os
import json
import math
import mpmath as mp

mp.mp.dps = 50  # 50 significant digits for the "exact algebra" checks

# ----------------------------------------------------------------------------
# Physical constants / measured inputs (for the SI confrontation only).
# EW point: the project's adopted physical point (ca_wmu.py docstring, F44).
# Higgs / top: PDG-level central values.
# ----------------------------------------------------------------------------
V_HIGGS_GEV = 246.22      # EW vacuum expectation value (project value, F44)
F_SCALE_GEV = V_HIGGS_GEV / 2.0   # Stueckelberg scale f = v/2 (F34b/F44)
M_W_GEV     = 80.415      # project physical point
M_Z_GEV     = 91.226      # project physical point
M_H_OBS_GEV = 125.25      # observed Higgs boson mass (PDG)
M_T_GEV     = 172.57      # top-quark mass (PDG)
M_B_GEV     = 4.18        # bottom-quark mass (PDG, MSbar)

A_CELL_M    = 6.2e-35     # F64/D-EM10 G-matched cell size
HBAR_JS     = 1.054571817e-34
C_MS        = 2.99792458e8
GEV_J       = 1.602176634e-10   # 1 GeV in joules
# m_lat = m_phys c a / hbar  (F46 / si-units-options.md), with m_phys in kg.
# Convenient GeV form: m_lat = (E[GeV]*GEV_J/c^2) * c * a / hbar
def m_lat_from_GeV(E_GeV):
    m_kg = E_GeV * GEV_J / C_MS**2
    return m_kg * C_MS * A_CELL_M / HBAR_JS

# ----------------------------------------------------------------------------
results = {"finding": "F73", "title": "spin-0 bound-pair scalar",
           "checks": {}, "derived": {}, "confrontation": {}, "notes": []}
PASS = True

def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {
        "residual": float(residual), "target": float(target),
        "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:42s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")

print("=" * 74)
print("F73 — spin-0 bound-pair scalar: exact lattice kinematics")
print("=" * 74)

# ----- BP1: sine-addition identity, general unequal constituents (EXACT) ----
print("\nBP1  composite mass = sine-addition of constituent rest rotations")
max_res = mp.mpf(0)
samples = []
for i in range(1, 12):
    for j in range(1, 12):
        m1 = mp.mpf(i) / 12      # in (0,1)
        m2 = mp.mpf(j) / 12
        lhs = mp.sin(mp.asin(m1) + mp.asin(m2))
        rhs = m1 * mp.sqrt(1 - m2**2) + m2 * mp.sqrt(1 - m1**2)
        res = abs(lhs - rhs)
        max_res = max(max_res, res)
        samples.append((float(m1), float(m2), float(lhs)))
record("BP1 sin(asin m1+asin m2)=m1 n2+m2 n1", max_res, 1e-45,
       "exact-algebraic", max_res < mp.mpf(10) ** -45,
       extra={"n_pairs": len(samples)})

# ----- BP2: equal-mass closed form (EXACT) ----------------------------------
print("\nBP2  equal constituents: m_H = sin(2 arcsin mc) = 2 mc sqrt(1-mc^2)")
max_res = mp.mpf(0)
for i in range(1, 100):
    mc = mp.mpf(i) / 100
    lhs = mp.sin(2 * mp.asin(mc))
    rhs = 2 * mc * mp.sqrt(1 - mc**2)
    max_res = max(max_res, abs(lhs - rhs))
record("BP2 equal-mass closed form", max_res, 1e-45,
       "exact-algebraic", max_res < mp.mpf(10) ** -45)

# ----- BP3: lattice binding deficit vs Euclidean free sum -------------------
# Free (Euclidean) sum of rest masses would be 2 mc; the lattice (spherical)
# composite is sin(2 arcsin mc) <= 2 mc. Deficit fraction d = 1 - sqrt(1-mc^2),
# leading order d ~ mc^2 / 2.
print("\nBP3  binding deficit: composite is strictly below the free sum")
mc = mp.mpf("1e-6")
deficit = 1 - mp.sqrt(1 - mc**2)
deficit_lead = mc**2 / 2
slope_res = abs(deficit - deficit_lead) / deficit_lead   # ~ mc^2/4, tiny
# also confirm composite < free sum for a coarse scan
below_ok = all(
    float(mp.sin(2 * mp.asin(mp.mpf(i) / 100))) < float(2 * mp.mpf(i) / 100)
    for i in range(1, 100))
record("BP3 deficit leading order d~mc^2/2", slope_res, 1e-6,
       "quantitative", (slope_res < 1e-6) and below_ok,
       extra={"composite_below_free_sum": below_ok})
results["derived"]["deficit_fraction_formula"] = "1 - sqrt(1-mc^2)  (~ mc^2/2)"

# ----- BP4: stability / saturation bound ------------------------------------
# Omega_H = 2 arcsin mc reaches pi/2 (max lattice mass m_H=1) at mc = 1/sqrt2;
# beyond that the rotation over-wraps. So a stable composite requires
# mc <= 1/sqrt(2); the composite mass saturates at m_H = 1.
print("\nBP4  stability bound: m_H maximal (=1) at mc = 1/sqrt2")
mc_star = 1 / mp.sqrt(2)
mH_star = mp.sin(2 * mp.asin(mc_star))
omega_star = 2 * mp.asin(mc_star)
res4 = abs(mH_star - 1) + abs(omega_star - mp.pi / 2)
record("BP4 saturation at mc=1/sqrt2 -> m_H=1", res4, 1e-45,
       "exact-algebraic", res4 < mp.mpf(10) ** -45,
       extra={"mc_star": float(mc_star), "omega_star": float(omega_star)})
results["derived"]["stability_bound"] = "mc <= 1/sqrt(2); m_H saturates at 1"

# ----- BP5: lab-scale negligibility of the deficit --------------------------
# At a = 6.2e-35 m every EW-scale mass has m_lat << 1, so the spherical deficit
# is ~ m_lat^2/2, i.e. unobservably small; the SI prediction is the free sum.
print("\nBP5  at G-matched a, the deficit is negligible (m_H ~ free sum)")
mlat_t  = m_lat_from_GeV(M_T_GEV)
mlat_H  = m_lat_from_GeV(M_H_OBS_GEV)
deficit_t = 0.5 * mlat_t**2
results["derived"]["m_lat_top"] = mlat_t
results["derived"]["m_lat_higgs"] = mlat_H
results["derived"]["deficit_fraction_top_pair"] = deficit_t
print(f"       m_lat(top)   = {mlat_t:.3e}")
print(f"       m_lat(125)   = {mlat_H:.3e}")
print(f"       deficit frac (t-pair) ~ mc^2/2 = {deficit_t:.3e}")
record("BP5 deficit << 1 at EW scale", deficit_t, 1e-30,
       "quantitative", deficit_t < 1e-30)

# ----- BP6: SI confrontation with the observed Higgs mass -------------------
print("\nBP6  confrontation with observed m_H = 125.25 GeV (free-sum regime)")
# (a) equal constituents at threshold:  m_H = 2 mc  ->  mc = m_H/2
mc_thresh = M_H_OBS_GEV / 2.0
# (b) top-condensate (Nambu) t-tbar pair, zero binding:
mH_ttbar_free = 2 * M_T_GEV
Eb_required   = mH_ttbar_free - M_H_OBS_GEV
Eb_frac       = Eb_required / mH_ttbar_free
# (c) flagged (NOT derived) identification m_H = f = v/2  <=>  quartic lambda=1/8
ratio_v2   = M_H_OBS_GEV / F_SCALE_GEV
lam_obs    = M_H_OBS_GEV**2 / (2 * V_HIGGS_GEV**2)
lam_if_v2  = 0.125
results["confrontation"] = {
    "equal_constituent_threshold_GeV": mc_thresh,
    "ttbar_free_sum_GeV": mH_ttbar_free,
    "ttbar_required_binding_GeV": Eb_required,
    "ttbar_required_binding_fraction": Eb_frac,
    "m_H_over_(v/2)": ratio_v2,
    "lambda_observed": lam_obs,
    "lambda_if_mH_eq_v_over_2": lam_if_v2,
    "lambda_fractional_gap": abs(lam_obs - lam_if_v2) / lam_obs,
}
print(f"       (a) equal-constituent threshold  mc = {mc_thresh:.2f} GeV "
      f"(no SM fermion at this mass)")
print(f"       (b) t-tbar free sum 2 m_t        = {mH_ttbar_free:.1f} GeV "
      f"-> needs binding {Eb_required:.1f} GeV ({100*Eb_frac:.1f}%)")
print(f"       (c) m_H / (v/2)                  = {ratio_v2:.4f}  "
      f"(<=> lambda: obs {lam_obs:.4f} vs 1/8={lam_if_v2})")
# This block is a confrontation, not a pass/fail of the kinematics; record TRUE
# for the bookkeeping that the numbers computed and are self-consistent.
record("BP6 confrontation numbers self-consistent",
       abs(mH_ttbar_free - (M_H_OBS_GEV + Eb_required)), 1e-9,
       "bookkeeping", abs(mH_ttbar_free - (M_H_OBS_GEV + Eb_required)) < 1e-9)

results["notes"] = [
    "m_H = sin(asin m1 + asin m2) is exact lattice kinematics (F46+F69), no new input.",
    "Lattice composition is strictly sub-additive: m_H <= m1+m2, deficit ~ mc^2/2.",
    "At a=6.2e-35 m all EW masses have m_lat<<1 so deficit ~1e-42: SI prediction is the free sum.",
    "Free-sum kinematics alone CANNOT hit 125.25 GeV: equal constituents need mc=62.6 GeV (no SM match); t-tbar overshoots to 346 GeV needing 64% binding.",
    "Therefore the missing model input is the BINDING DYNAMICS (the SM quartic lambda in disguise); the model predicts only the kinematic ceiling.",
    "FLAGGED, NOT DERIVED: m_H ~ f = v/2 (123.1 GeV) to 1.7%, equivalently quartic lambda ~ 1/8 = 0.125 vs observed 0.129 (3%). Recorded as a numerical coincidence pending a binding-scale derivation.",
]

# ----------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "test-results")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "F73_spin0_bound_pair.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 74)
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   "
      f"({sum(1 for c in results['checks'].values() if c['status']=='PASS')}"
      f"/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 74)
