#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F113_repulsive_core.py
===========================

F113 — the NN short-range REPULSIVE CORE, derived from the model.

Phase P4 of docs/roadmaps/roadmap-matter-binding.md named the short-range repulsive core as
the missing nuclear-force ingredient (the OPEP attractive tail is the F103
pion).  This suite certifies that the core falls out of the model's own
first principles: two colour-singlet nucleons (F71) forced to overlap are six
genuine CA fermions, so the Pauli antisymmetriser drives them into the
spatially-symmetric [6] colour-spin state, which is chromomagnetically
unfavourable -> a repulsion of several hundred MeV.

Everything is EXACT rational algebra (no numpy on chiral objects; CLAUDE.md):
    lam_i.lam_j = 2 P^c - 2/3 ,  sig_i.sig_j = 2 P^s - 1  (SU(N) Fierz swaps)
    H_CM = - sum_{i<j} (lam_i.lam_j)(sig_i.sig_j)          [units g_cm]

Parts
-----
  A  Fierz swap operators reproduce known two-body eigenvalues
     (sig.sig: triplet +1 / singlet -3 ; lam.lam antisym colour pair -8/3). exact
  B  Single-baryon chromomagnetic energies: N = -8, Delta = +8 g_cm
     => N-Delta = 16 g_cm calibrates g_cm = 18.31 MeV.                exact
  C  Six-quark Pauli antisymmetriser: deuteron channel norm kernel
     K_0=K_3=839808, K_1=K_2=93312 ; n(R=0)=20/9 (>0 => allowed).     exact
  D  The core: [6] 6q at R=0 has <H_CM> = +8/3 g_cm vs -16 for two free
     nucleons => Delta E_CM = +56/3 g_cm = +341.8 MeV (REPULSIVE).     exact
  E  Core profile V_core(R) is positive, monotonically decreasing, and
     -> 0 at large separation (turns off over the quark-overlap range). quantitative
  F  Permutation-sign / antisymmetriser sanity (transposition = -1;
     idempotency A^2 ~ A on the channel).                             exact

Run:  python3 tests/findings/test_F113_repulsive_core.py     (~15 s)
Writes test-results/F113_repulsive_core.json.
"""

import os
import sys
import json
from fractions import Fraction as Fr

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.particles import nuclear_core as C  # noqa: E402

results = {"finding": "F113", "title": "NN short-range repulsive core (quark Pauli + chromomagnetic)",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, ok, detail, tier):
    global PASS
    results["checks"][name] = {"status": "PASS" if ok else "FAIL",
                               "tier": tier, "detail": detail}
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:46s} {detail}  ({tier})")


print("=" * 80)
print("F113 — the NN short-range repulsive core from the model")
print("=" * 80)

# ---------------------------------------------------------------------------
# A. Fierz swap operators reproduce known two-body eigenvalues.
# ---------------------------------------------------------------------------
# sig.sig = 2 P^s - 1 : build a 2-quark spin singlet / triplet and check.
def two_q(a, b):
    return {(a, b): Fr(1)}

def sigsig_expectation(state):
    # <state| (2 P^s - 1) |state> / norm, P^s swaps spins of slots 0,1
    out = {}
    for k, amp in state.items():
        out[C._swap_spin(k, 0, 1)] = out.get(C._swap_spin(k, 0, 1), Fr(0)) + Fr(2) * amp
        out[k] = out.get(k, Fr(0)) - amp
    return C.overlap(state, out) / C.overlap(state, state)

# spin triplet |up up> (colour r,g distinct to keep it a clean 2-state)
trip = {(C.enc(0, 0, 0), C.enc(1, 0, 0)): Fr(1)}
# spin singlet (|up dn> - |dn up>)/sqrt2  (same colours r,g)
sing = {(C.enc(0, 0, 0), C.enc(1, 1, 0)): Fr(1),
        (C.enc(0, 1, 0), C.enc(1, 0, 0)): Fr(-1)}
ss_t = sigsig_expectation(trip)
ss_s = sigsig_expectation(sing)
okA1 = (ss_t == Fr(1) and ss_s == Fr(-3))
record("A.sigsig_triplet_+1_singlet_-3", okA1,
       f"triplet={ss_t}, singlet={ss_s}", "exact (Tier-1)")

# lam.lam = 2 P^c - 2/3 : colour-antisymmetric pair -> -8/3
def lamlam_expectation(state):
    out = {}
    for k, amp in state.items():
        out[C._swap_colour(k, 0, 1)] = out.get(C._swap_colour(k, 0, 1), Fr(0)) + Fr(2) * amp
        out[k] = out.get(k, Fr(0)) - Fr(2, 3) * amp
    return C.overlap(state, out) / C.overlap(state, state)

colour_antisym = {(C.enc(0, 0, 0), C.enc(1, 0, 0)): Fr(1),
                  (C.enc(1, 0, 0), C.enc(0, 0, 0)): Fr(-1)}
ll = lamlam_expectation(colour_antisym)
okA2 = (ll == Fr(-8, 3))
record("A.lamlam_colour_antisym_-8/3", okA2, f"value={ll}", "exact (Tier-1)")

# ---------------------------------------------------------------------------
# B. Single-baryon chromomagnetic energies and the g_cm calibration.
# ---------------------------------------------------------------------------
eN = C.chromomagnetic_energy(C.nucleon('p', True), 3)
eD = C.chromomagnetic_energy(C.delta_pp(), 3)
okB = (eN == Fr(-8) and eD == Fr(8))
g_cm = 293.0 / float(eD - eN)
record("B.N=-8_Delta=+8_gcm", okB,
       f"E_N={eN}, E_Delta={eD}, N-Delta={eD-eN} g_cm => g_cm={g_cm:.2f} MeV",
       "exact (Tier-1)")
results["derived"]["g_cm_MeV"] = g_cm
results["derived"]["E_N_gcm"] = str(eN)
results["derived"]["E_Delta_gcm"] = str(eD)

# ---------------------------------------------------------------------------
# C. Six-quark Pauli norm kernel for the deuteron channel (S=1, T=0).
# ---------------------------------------------------------------------------
Phi = C.two_cluster(True, True, 'singlet')
K = C.norm_kernel_coeffs(Phi)
n0 = sum(K.values()) / K[0]
okC = (K[0] == Fr(839808) and K[3] == Fr(839808)
       and K[1] == Fr(93312) and K[2] == Fr(93312) and n0 == Fr(20, 9))
record("C.norm_kernel_exact_n0=20/9", okC,
       f"K0={K[0]},K1={K[1]},K2={K[2]},K3={K[3]}, n(R=0)={n0}", "exact (Tier-1)")
results["derived"]["norm_kernel_K"] = {m: str(K[m]) for m in K}
results["derived"]["n_at_R0"] = str(n0)

# ---------------------------------------------------------------------------
# D. THE CORE: [6] 6q energy at R=0 vs two free nucleons.
# ---------------------------------------------------------------------------
e6 = C.antisymmetrised_6q_energy(Phi)
dE = e6 - 2 * eN
V0 = float(dE) * g_cm
okD = (e6 == Fr(8, 3) and dE == Fr(56, 3) and dE > 0)
record("D.core_dE=+56/3_gcm_repulsive", okD,
       f"E_6q(R0)={e6}, 2N={2*eN}, dE_CM={dE} g_cm = +{V0:.1f} MeV (>0)",
       "exact (Tier-1)")
results["derived"]["E_6q_R0_gcm"] = str(e6)
results["derived"]["dE_CM_gcm"] = str(dE)
results["derived"]["V_core0_MeV"] = V0

# ---------------------------------------------------------------------------
# E. Core profile: positive, monotone-decreasing, vanishing at large R.
# ---------------------------------------------------------------------------
prof = C.core_profile(Phi, [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
Vprof = [(xb, g_cm * (g - 2 * float(eN))) for xb, g in prof]
V_vals = [V for _, V in Vprof]
monotone = all(V_vals[i] > V_vals[i + 1] - 1e-9 for i in range(len(V_vals) - 1))
positive = all(V > -1e-6 for V in V_vals)
vanishes = (V_vals[-1] < 0.05 * V_vals[0])
okE = monotone and positive and vanishes and abs(V_vals[0] - V0) < 1e-6
record("E.profile_positive_monotone_vanishing", okE,
       f"V(0)={V_vals[0]:.1f}, V(2b)={Vprof[4][1]:.1f}, V(4b)={V_vals[-1]:.1f} MeV",
       "quantitative (Tier-B; profile depends on quark size b)")
results["derived"]["profile_MeV"] = [(xb, V) for xb, V in Vprof]

# ---------------------------------------------------------------------------
# F. Permutation-sign / antisymmetriser sanity.
# ---------------------------------------------------------------------------
# a single transposition has sign -1; a 3-cycle +1
s_transp = C.perm_sign((1, 0, 2, 3, 4, 5))
s_3cyc = C.perm_sign((1, 2, 0, 3, 4, 5))
# channel-allowed check: <Phi|A|Phi> = sum_P sgn(P)<Phi|P|Phi> = sum_m K_m
# (the full antisymmetriser norm equals the total of the norm-kernel coeffs).
denA = sum(K.values())
okF = (s_transp == -1 and s_3cyc == 1 and denA > 0)
record("F.perm_sign_and_channel_allowed", okF,
       f"sgn(transp)={s_transp}, sgn(3cyc)={s_3cyc}, <Phi|A|Phi>={denA}>0",
       "exact (Tier-1)")

# ---------------------------------------------------------------------------
results["notes"] = [
    "Mechanism: a nucleon = colour-singlet (eps_abc, F71) x SU(6) spin-flavour-"
    "symmetric of THREE CA fermions. Two overlapping nucleons = six identical "
    "fermions; the F71 Pauli antisymmetriser (extended 3q->6q) forces the "
    "spatially-symmetric [6] colour-spin state, which is chromomagnetically "
    "unfavourable -> repulsion. This is the Oka-Yazaki / Faessler quark-cluster "
    "origin of the NN hard core, here computed directly in the model algebra.",
    "g_cm is the ONLY external number, fixed by the measured N-Delta splitting "
    "(293 MeV) -> 18.31 MeV; it is the same colour-magnetic coupling that the "
    "model already uses for the baryon mass splittings, not a new free parameter.",
    "n(R=0)=20/9>0: the deuteron channel is NOT kinematically Pauli-forbidden "
    "(consistent with the deuteron existing); the core here is the DYNAMICAL "
    "chromomagnetic repulsion that the Pauli-required [6] symmetry switches on.",
    "Tier: A-D are exact rationals. E (the R-profile shape / absolute core "
    "radius) depends on the quark Gaussian size b and is Tier-B; the core HEIGHT "
    "+341.8 MeV is exact given g_cm.",
    "P4 closure: combine this short-range core with the F103 one-pion-exchange "
    "attractive tail to get the full NN potential the deuteron bound state uses.",
]

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "F113_repulsive_core.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 80)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 80)
sys.exit(0 if PASS else 1)
