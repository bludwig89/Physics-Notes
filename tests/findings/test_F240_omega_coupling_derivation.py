#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F240_omega_coupling_derivation.py
======================================

F240 — Deriving the isoscalar-vector (ω) NN coupling from the model's
vector-meson sector (KSFR + universality + baryon-number coherence), and
confronting it with the full OBE deuteron.

WHAT Q3 ASKED
-------------
Target F126 §"room left for the vector (ω)". Derive g_ω and m_ω from the model's
vector-meson sector (NOT fit to NN), add V_ω = +(g²/4π) m_ω [folded e^{-m r}/r]
to the full OBE (F104 π tail + F126 σ + F113 core + ω), run the F104 deuteron
solver with no tuned hard core, and report B_d (2.224 MeV) and r_d (~1.97 fm),
plus the ~-50..-100 MeV residual well.

WHAT F128 ALREADY DID (and what is new here)
--------------------------------------------
F128 built the ω channel into ca_nuclear (`omega_exchange_potential`,
`solve_deuteron(omega=...)`), derived the SIGN (Tier-1) and m_ω=m_ρ (Tier-1),
and FIT g_ω²/4π = 5.39 by rebinding E_b (Tier-B consistency, not a prediction).
F240 goes to the question F128 left open: can g_ω be DERIVED independently, and
does the derived value bind? We use the model's own vector-dominance chain:

    KSFR (model f_π):        g_ρππ  = m_ρ / (√2 f_π)                    [Tier-1]
    vector universality:     g_ρNN  = g_ρππ                            [VMD posit]
    baryon-number coherence: g_ωNN  = 3 g_ρNN   (F128 B, exact ×3)     [Tier-1]

  => g_ωNN²/4π (strict universality) = 9 (m_ρ/√2 f_π)² / 4π .

We then confront this DERIVED number with the deuteron via the F104 solver:
  - Route A: full OBE the F128 way = F113 quark-Pauli core + σ(bare) + ω.
  - Route B: pure meson OBE = σ(bare) + ω, no F113 core (core=g_cm 0), which is
             the textbook σ/ω decomposition the "residual well" refers to.
Honest outcome: strict universality OVERSHOOTS (deuteron unbinds); the NN data
require a ~0.43 quench of g_ωNN — numerically the SAME quench (0.45) F126 needed
on the bare scalar coupling. So the ω absolute coupling stays a one-number
bracket [5.4 (with core), 11.1 (pure OBE)] below the universality ceiling 25.9,
while its sign, its m_ω, and the g_ωNN/g_ρNN=3 ratio are Tier-1 derived. The
residual σ+ω well reaches -81 MeV (in the -50..-100 MeV target) at g_ω²/4π≈8.

NUMERICS: all real (real-space Schrödinger + real Yukawa folds); no chiral/complex
transforms, so the CLAUDE.md numpy caveat does not bite. Reuses the F104/F126/F128
deuteron solver (ca_nuclear).

Run:  python3 tests/findings/test_F240_omega_coupling_derivation.py
Writes test-results/F240_omega_coupling_derivation.json
"""

import os
import sys
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "ca-simulation"))
import ca_nuclear as nuc  # noqa: E402

results = {"finding": "F240",
           "title": "Deriving the omega NN coupling from the vector-meson sector; full-OBE deuteron",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                               "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:56s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 80)
print("F240 — omega NN coupling from the vector-meson sector; full-OBE deuteron")
print("=" * 80)

# model-native constants
F_PI = nuc.F_PI_DEFAULT        # 92.07 MeV (F77/P3 output)
M_OMEGA = nuc.M_OMEGA_DEFAULT  # 782.66 MeV (= m_rho by rho-omega degeneracy, F128)
M_RHO = 782.66                 # MeV, degenerate with omega (F128 Tier-1)
b = 0.55                       # fm, physical quark size (F126/F128)
gS = nuc.SIGMA_G2_4PI_BARE     # bare 3-quark sigma coupling (F126) = 8.18

# ---------------------------------------------------------------------------
# A. DERIVE g_omegaNN from the model's vector-meson sector (no NN fit).
#    KSFR: g_rhopipi = m_rho/(sqrt2 f_pi)  ->  universality g_rhoNN = g_rhopipi
#    -> baryon-number coherence g_omegaNN = 3 g_rhoNN.
# ---------------------------------------------------------------------------
print("\nA  derive g_omegaNN: KSFR x universality x baryon-number coherence")

g_rhopipi = M_RHO / (math.sqrt(2.0) * F_PI)          # KSFR, model f_pi -> Tier-1
g_rho_2_4pi = g_rhopipi ** 2 / (4.0 * math.pi)
# KSFR self-consistency check: m_rho^2 = 2 g^2 f_pi^2 must reproduce m_rho
m_rho_ksfr = math.sqrt(2.0) * g_rhopipi * F_PI
record("A1 KSFR closes: m_rho = sqrt2 g_rhopipi f_pi", abs(m_rho_ksfr - M_RHO) / M_RHO,
       1e-12, "exact", abs(m_rho_ksfr - M_RHO) / M_RHO < 1e-12,
       extra={"g_rhopipi": g_rhopipi, "g_rhoNN2_4pi": g_rho_2_4pi})

# baryon-number coherence (F128 B): g_omegaNN = 3 g_rhoNN, exact factor 3
g_omegaNN = 3.0 * g_rhopipi
g_omega_2_4pi_universal = g_omegaNN ** 2 / (4.0 * math.pi)
record("A2 baryon-number coherence g_omegaNN = 3 g_rhoNN (exact x3)",
       abs((g_omegaNN / g_rhopipi) - 3.0), 1e-15, "exact",
       abs((g_omegaNN / g_rhopipi) - 3.0) < 1e-15)
record("A3 => strict-universality g_omegaNN^2/4pi = 9 g_rhoNN^2/4pi",
       abs(g_omega_2_4pi_universal - 9.0 * g_rho_2_4pi), 1e-9, "exact",
       abs(g_omega_2_4pi_universal - 9.0 * g_rho_2_4pi) < 1e-9,
       extra={"g_omegaNN2_4pi_universal": g_omega_2_4pi_universal})
results["derived"]["g_rhopipi_KSFR"] = g_rhopipi
results["derived"]["g_rhoNN2_4pi_universality"] = g_rho_2_4pi
results["derived"]["g_omegaNN2_4pi_strict_universality"] = g_omega_2_4pi_universal
results["derived"]["m_omega_MeV"] = M_OMEGA

# ---------------------------------------------------------------------------
# B. The strict-universality coupling OVERSHOOTS: with bare sigma + core it
#    unbinds the deuteron.  (Honest negative result.)
# ---------------------------------------------------------------------------
print("\nB  confront: strict-universality g_omega overshoots (unbinds)")


def solve(gw, g_cm, N=700, vec=True):
    return nuc.solve_deuteron(core="derived", b=b, g_cm=g_cm, N=N, sigma=True,
                              sigma_g2_4pi=gS, omega=True, omega_g2_4pi=gw,
                              m_omega=M_OMEGA, vectors=vec)


d_univ = solve(g_omega_2_4pi_universal, 18.31, N=600, vec=True)
unbound = not d_univ["bound"]
record("B1 strict-universality g_omega (25.9) UNBINDS the deuteron",
       0.0 if unbound else 1.0, 0.5, "Tier-B", unbound,
       extra={"g_omega2_4pi": g_omega_2_4pi_universal, "E_b_MeV": d_univ["E_b"],
              "bound": d_univ["bound"]})

# ---------------------------------------------------------------------------
# C. What the deuteron actually needs: bracket g_omega by binding it two ways.
#    Route A (F128): F113 core (g_cm=18.31) + bare sigma + omega.
#    Route B: pure meson OBE (no core, g_cm=0): bare sigma + omega.
# ---------------------------------------------------------------------------
print("\nC  bracket g_omega by binding the deuteron (full derived OBE, no tuned wall)")


def bisect_bind(g_cm, lo, hi, N=500):
    f = lambda g: solve(g, g_cm, N=N, vec=False)["E_b"] - 2.224
    flo = f(lo)
    for _ in range(34):
        mid = 0.5 * (lo + hi)
        if flo * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
            flo = f(lo)
    return 0.5 * (lo + hi)


gwA = bisect_bind(18.31, 4.5, 6.0)
dA = solve(gwA, 18.31, N=800, vec=True)
gwB = bisect_bind(0.0, 10.5, 12.0)
dB = solve(gwB, 0.0, N=800, vec=True)

results["derived"]["route_A_core_plus_omega"] = {
    "g_omega2_4pi": gwA, "E_b_MeV": dA["E_b"], "r_d_fm": dA["r_d"],
    "P_D": dA["P_D"], "bound": dA["bound"]}
results["derived"]["route_B_pure_sigma_omega_OBE"] = {
    "g_omega2_4pi": gwB, "E_b_MeV": dB["E_b"], "r_d_fm": dB["r_d"],
    "P_D": dB["P_D"], "bound": dB["bound"]}

okA = abs(dA["E_b"] - 2.224) < 0.02 and dA["bound"]
record("C1 route A (F113 core + sigma + omega) binds E_b=2.224",
       abs(dA["E_b"] - 2.224), 2e-2, "Tier-B", okA,
       extra={"g_omega2_4pi": gwA, "E_b_MeV": dA["E_b"], "r_d_fm": dA["r_d"], "P_D": dA["P_D"]})
okA_rd = abs(dA["r_d"] - 1.97) / 1.97 < 0.05
record("C2 route A r_d within 5% of 1.97 fm", abs(dA["r_d"] - 1.97) / 1.97, 0.05,
       "Tier-B", okA_rd, extra={"r_d_fm": dA["r_d"]})

okB = abs(dB["E_b"] - 2.224) < 0.02 and dB["bound"]
record("C3 route B (pure sigma+omega OBE, no core) binds E_b=2.224",
       abs(dB["E_b"] - 2.224), 2e-2, "Tier-B", okB,
       extra={"g_omega2_4pi": gwB, "E_b_MeV": dB["E_b"], "r_d_fm": dB["r_d"], "P_D": dB["P_D"]})
okB_rd = abs(dB["r_d"] - 1.97) / 1.97 < 0.08
record("C4 route B r_d within 8% of 1.97 fm", abs(dB["r_d"] - 1.97) / 1.97, 0.08,
       "Tier-B", okB_rd, extra={"r_d_fm": dB["r_d"]})

# ---------------------------------------------------------------------------
# D. The vector quench mirrors the scalar quench: g_omega(needed)/g_omega(univ)
#    ~ 0.43, numerically the SAME as F126's scalar 0.45.  Internal consistency.
# ---------------------------------------------------------------------------
print("\nD  vector quench = scalar quench (internal consistency)")
quench_vector = gwB / g_omega_2_4pi_universal      # pure-OBE required / universality
quench_scalar = 3.69 / gS                          # F126 effective/bare = 0.45
results["derived"]["quench_vector_pureOBE_over_universality"] = quench_vector
results["derived"]["quench_scalar_F126"] = quench_scalar
# both ~0.43-0.45: agree to ~5%
agree = abs(quench_vector - quench_scalar) / quench_scalar < 0.10
record("D1 vector quench ~= scalar quench (both ~0.43-0.45, agree <10%)",
       abs(quench_vector - quench_scalar) / quench_scalar, 0.10, "Tier-B", agree,
       extra={"quench_vector": quench_vector, "quench_scalar_F126": quench_scalar})

# ---------------------------------------------------------------------------
# E. The residual (sigma+omega) OBE well reaches -50..-100 MeV.
# ---------------------------------------------------------------------------
print("\nE  residual sigma+omega well hits the -50..-100 MeV target")
rr = np.linspace(0.3, 2.5, 60)


def well(gw):
    return (nuc.sigma_exchange_potential(rr, b=b, g2_4pi=gS)
            + nuc.omega_exchange_potential(rr, b=b, g2_4pi=gw, m_omega=M_OMEGA))


well8 = float(well(8.0).min())
record("E1 sigma+omega residual well in [-100,-50] MeV at g_omega2/4pi=8",
       0.0 if (-100.0 <= well8 <= -50.0) else 1.0, 0.5, "Tier-B",
       (-100.0 <= well8 <= -50.0),
       extra={"well_min_MeV": well8, "g_omega2_4pi": 8.0})
results["derived"]["residual_well_min_MeV_at_g8"] = well8

# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
n_tot = len(results["checks"])
results["summary"] = {"pass": n_pass, "total": n_tot, "all_pass": PASS}
results["notes"] = [
    "m_omega and g_omegaNN/g_rhoNN=3 and the repulsive sign are Tier-1 model-derived.",
    "STRICT universality g_omegaNN^2/4pi=25.9 OVERSHOOTS: deuteron unbinds (B1).",
    "Deuteron binds at g_omega^2/4pi=5.39 (with F113 core) or 11.15 (pure OBE).",
    "Vector absolute coupling stays a one-number bracket [5.4,11.1] below the 25.9 ceiling.",
    "The required 0.43 quench of the bare vector coupling matches F126's 0.45 scalar quench.",
    "Residual sigma+omega well = -81 MeV at g_omega^2/4pi=8 (in the -50..-100 MeV target)."]
print(f"RESULT: {n_pass}/{n_tot} checks PASS   (overall {'PASS' if PASS else 'FAIL'})")
print("=" * 80)

outdir = os.path.join(HERE, "..", "..", "test-results")
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, "F240_omega_coupling_derivation.json")
with open(outpath, "w") as f:
    json.dump(results, f, indent=2)
print(f"wrote {outpath}")

sys.exit(0 if PASS else 1)
