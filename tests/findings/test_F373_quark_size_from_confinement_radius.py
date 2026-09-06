#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F373_quark_size_from_confinement_radius.py
================================================

F373 — G6 (nuclear binding): is the OBE quark-size regulator b=0.55 fm
(F113/F126/F128/F240) a free/independently-tuned parameter, or is it
consistent with an already-derived model scale?

WHAT THIS CHECKS
-----------------
F146 computed a "single-constituent confinement radius" from the model's own
3D SU(3) gauge dynamics + block-spin binding solver, entirely independent of
the nuclear sector:

    R_conf = 1.11 / sqrt(sigma)   (dimensionless coefficient 1.11, F146 W3/4b)

Using the SAME sqrt(sigma)=0.42 GeV anchor the nuclear sector's own P6 debt
already shares (F123 Sec.5; also F122's own quoted anchor, reused verbatim by
F372), R_conf = 0.5215 fm -- 5.5% BELOW the value F126/F128/F240 tuned
(b=0.55 fm) to reproduce the deuteron.

This script does NOT just compare the two numbers -- it re-solves the full
derived-OBE deuteron (F104 pi tensor + F113 core + F126 sigma + F128/F240
omega, via ca_nuclear.solve_deuteron) with b replaced by R_conf, holding every
OTHER model-derived quantity fixed (g_cm, bare sigma coupling, m_sigma,
m_omega), re-bisecting ONLY the still-bracketed omega coupling (F240's own
open item -- not this finding's target) to the physical E_b, and reports
whether r_d, P_D and the omega coupling stay in the same physical/OBE
ballpark as at the independently-tuned b=0.55 fm. A companion candidate --
the P2 (F122) three-body ECG solver's own single-quark RMS spread about the
baryon centre of mass at its baseline point -- is checked too, and shown to
be a WORSE match, so the R_conf agreement is not "any model number will do".

HONEST SCOPE: this is a consistency/insensitivity check, not an algebraic
elimination of b. R_conf is measured on a 3D simple-cubic SU(3) action F265
flagged as blind to 1/3 of the curvature content (not yet redone on the
model's genuine BCC action, per docs/theory/supersessions.yaml S-list "F146
3D cubic"), and the omega coupling stays the bracketed [5-11] Tier-B number
F240 already left open. What this finding adds: b is no longer an
independently-tuned nuclear-only number -- a completely different sector
(pure SU(3) gauge dynamics, zero nuclear-force input) predicts a value 5.5%
away, and the deuteron's physical observables are insensitive to substituting
it.

Numerology caveat (review-finding Attack 5): R_conf's building block
hbar*c/sqrt(sigma) = 0.470 fm is itself a generic hadronic length in this
model (the same sqrt(sigma)=0.42 GeV that sets confinement everywhere else),
so the comparison is not "any O(1)-coefficient times a QCD scale matches" --
a coefficient landing within 10% of the tuned b=0.55 fm needs to sit in
[1.054, 1.288]  (a ~23%-wide window out of an O(1) range), and F146's
coefficient 1.11 was fixed by the SU(3) lattice Monte Carlo BEFORE this
comparison was run (F146 predates this finding), so it is not tuned to land
there. The independent literature value for this same quark-cluster-model
regulator (Oka-Yazaki / RGM quark models) is ~0.5-0.6 fm, i.e. this model's
1.11 coefficient is landing in a range other approaches to the same physics
also occupy -- consistent with, not proof against, "this scale is generic."

Route A boundary (found during the review-finding pass): route A (core +
sigma + omega, the full three-meson exchange) only has a solution at
POSITIVE g_omega^2/4pi for b below ~0.68 fm (Sec. D2/D3) -- beyond that the
required coupling goes negative, i.e. unphysical, and route A cannot bind
the deuteron there at all via a real omega coupling. Every b value actually
compared in this finding (b_P2=0.41, R_conf=0.52, b_tuned=0.55 fm) sits
comfortably below that edge (D3), so the finding's own comparisons are not
near this boundary -- but a future correction to R_conf (e.g. from the BCC
re-derivation F265 flags as owed) that pushed it much higher could approach
it, and that boundary was invisible before this review pass because the
original bisect_bind() silently returned a garbage root outside its narrow
hard-coded bracket instead of reporting "no solution" (see find_root_gomega).

NUMERICS: all real (real-space Schrodinger + real Yukawa folds + real ECG
matrix elements); no chiral/complex transforms, so the CLAUDE.md numpy caveat
does not bite.

Run:  python3 tests/findings/test_F373_quark_size_from_confinement_radius.py
Writes test-results/F373_quark_size_from_confinement_radius.json
"""

import os
import sys
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))

from casim.engine.particles import nuclear as nuc                       # noqa: E402
from casim.engine.particles import baryon_dynamics as bd                # noqa: E402
from casim.constants import sqrt_sigma_GeV                              # noqa: E402

HBARC = 197.32698  # MeV fm

results = {"finding": "F373",
           "title": "Is the OBE quark-size regulator b=0.55 fm consistent with "
                     "a derived model scale (F146 R_conf), or independently tuned?",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                                "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:66s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 80)
print("F373 -- quark-size regulator b vs the F146 gauge-derived confinement radius")
print("=" * 80)

B_TUNED = 0.55  # fm, F126/F128/F240's independently-tuned "physical" value
M_OMEGA = nuc.M_OMEGA_DEFAULT
gS = nuc.SIGMA_G2_4PI_BARE

# ---------------------------------------------------------------------------
# A. R_conf from F146 (SU(3) gauge dynamics + block-spin binding, zero nuclear
#    input): dimensionless R_conf*sqrt(sigma) = 1.11 (F146 Sec.4a/4b), physical
#    units via the SAME sqrt(sigma)=0.42 GeV anchor the nuclear sector's own
#    P6 debt already shares (F123 Sec.5; reused verbatim by F372).
# ---------------------------------------------------------------------------
print("\nA  R_conf (F146) vs the tuned b")
R_CONF_COEFF = 1.11              # dimensionless R_conf*sqrt(sigma), F146 Sec.4a
sqrt_sigma_MeV = sqrt_sigma_GeV * 1000.0
R_conf_fm = R_CONF_COEFF * HBARC / sqrt_sigma_MeV
rel_dev_Rconf = abs(B_TUNED - R_conf_fm) / R_conf_fm
record("A1 R_conf (F146) within 10% of the tuned b=0.55 fm",
       rel_dev_Rconf, 0.10, "quantitative", rel_dev_Rconf < 0.10,
       extra={"R_conf_fm": R_conf_fm, "b_tuned_fm": B_TUNED,
              "sqrt_sigma_GeV": sqrt_sigma_GeV})
results["derived"]["R_conf_fm"] = R_conf_fm
results["derived"]["b_tuned_fm"] = B_TUNED
results["derived"]["rel_dev_Rconf_vs_b_tuned"] = rel_dev_Rconf

# ---------------------------------------------------------------------------
# B. Companion candidate: the P2 (F122/baryon_dynamics) ECG solver's own
#    single-quark RMS spread about the baryon centre of mass, at the baseline
#    point (m_q=0.785, sigma=1, alpha_s=0.5) F122/F372 already use.  For 3
#    equal masses, symmetric configuration: sum_{i<j} r_ij^2 = 3 sum_i rho_i^2
#    => <rho^2> = <r_pair^2>/3.
# ---------------------------------------------------------------------------
print("\nB  companion candidate: P2 (F122) three-body single-quark spread")


def pair_r2(c0, basis):
    n = len(basis)
    out, norm = {}, 0.0
    for p, w in bd.PAIR_W.items():
        acc = 0.0
        for i in range(n):
            for j in range(n):
                C = basis[i] + basis[j]
                Sij = bd._overlap(C)
                beta = float(w @ np.linalg.inv(C) @ w)
                acc += c0[i] * c0[j] * (3.0 * beta) * Sij
        out[p] = acc
    for i in range(n):
        for j in range(n):
            norm += c0[i] * c0[j] * bd._overlap(basis[i] + basis[j])
    return {p: out[p] / norm for p in out}


m_q_baseline, sigma_baseline, alpha_s_baseline = 0.785, 1.0, 0.5
basis0 = bd.make_basis()
_, c0, basis2, _, _ = bd.spectrum_and_ground_vector(
    m_q_baseline, sigma_baseline, alpha_s_baseline, basis=basis0)
r2p = pair_r2(c0, basis2)
r2_common = list(r2p.values())[0]
spread = max(r2p.values()) - min(r2p.values())
record("B0 P2 ground state is S3-symmetric (three pair <r^2> equal)",
       spread / r2_common, 1e-8, "machine", spread / r2_common < 1e-8)

rho_rms_stringunits = math.sqrt(r2_common / 3.0)
unit_fm = HBARC / sqrt_sigma_MeV
b_P2_fm = rho_rms_stringunits * unit_fm
rel_dev_P2 = abs(B_TUNED - b_P2_fm) / b_P2_fm
record("B1 P2-ECG single-quark spread vs tuned b (companion candidate, "
       "INFORMATIONAL, not required to pass)",
       rel_dev_P2, 0.10, "quantitative", True,
       extra={"b_P2_fm": b_P2_fm,
              "note": ("documents the weaker candidate; NOT required to pass "
                       "-- residual 33.8% shows R_conf (A1, 5.5%) is the "
                       "clearly better match, not that any model number works"),
              "raw_residual_uncapped": rel_dev_P2})
results["derived"]["b_P2_ECG_fm"] = b_P2_fm
results["derived"]["rel_dev_P2_vs_b_tuned"] = rel_dev_P2
worse = rel_dev_P2 > rel_dev_Rconf
record("B2 R_conf (F146) is the CLOSER of the two candidates to the tuned b",
       0.0 if worse else 1.0, 0.5, "quantitative", worse)

# ---------------------------------------------------------------------------
# C. Physics-tested check: swap b -> R_conf in the FULL derived-OBE deuteron
#    solver (F104 pi tensor + F113 core + F126 sigma + F128/F240 omega),
#    holding g_cm, bare sigma, m_sigma, m_omega FIXED (all independently
#    model-derived elsewhere), re-bisecting ONLY the still-bracketed omega
#    coupling (F240's own open Tier-B item) to the physical E_b=2.224 MeV --
#    exactly as F240 itself does at b=0.55.  Report r_d, P_D, and whether the
#    required omega coupling stays in the empirical OBE/SU(6) window (F128:
#    5-9; F240 bracket [5.4,11.1]) rather than blowing up or going negative.
# ---------------------------------------------------------------------------
print("\nC  full derived-OBE deuteron: b=0.55 (tuned) vs b=R_conf (F146)")

E_B_PHYS = 2.224
R_D_PHYS = 1.97


def solve(b, gw, g_cm, N=900, vec=True):
    return nuc.solve_deuteron(core="derived", b=b, g_cm=g_cm, N=N, sigma=True,
                               sigma_g2_4pi=gS, omega=True, omega_g2_4pi=gw,
                               m_omega=M_OMEGA, vectors=vec)


def find_root_gomega(b, g_cm, lo0=-5.0, hi0=30.0, step=0.5, N=500):
    """Adaptive-bracket root find for the omega coupling giving E_b=E_B_PHYS.

    FIX (2026-09-05 review-finding pass, Attack 7): the original bisect_bind()
    bisected a FIXED bracket without ever checking that f(lo)*f(hi) <= 0 --
    outside the bracket's true root window it silently returned a garbage
    midpoint with no error or warning (verified: at b=0.4111 fm, the old
    [2,9] bracket for route A returned E_b=14.03 MeV, r_d=0.94 fm -- nonsense
    -- while reporting no failure). This version scans coarsely for an actual
    sign change first and returns (None, False) -- not a number -- when none
    exists in the scanned range, so a caller cannot mistake "no physical
    solution found" for a real root.
    """
    def f(g):
        return nuc.solve_deuteron(core="derived", b=b, g_cm=g_cm, N=N,
                                   sigma=True, sigma_g2_4pi=gS, omega=True,
                                   omega_g2_4pi=g, m_omega=M_OMEGA,
                                   vectors=False)["E_b"] - E_B_PHYS

    n_steps = int(round((hi0 - lo0) / step))
    prev_x, prev_v = lo0, f(lo0)
    bracket = None
    for i in range(1, n_steps + 1):
        x = lo0 + i * step
        v = f(x)
        if prev_v == 0.0:
            bracket = (prev_x, prev_x)
            break
        if (prev_v < 0) != (v < 0):
            bracket = (prev_x, x)
            break
        prev_x, prev_v = x, v
    if bracket is None:
        return None, False
    lo, hi = bracket
    flo = f(lo)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (flo < 0) != (fm < 0):
            hi = mid
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi), True


def solve_route(b_test, g_cm, lo0, hi0, step=0.5, vec=True):
    gw, ok = find_root_gomega(b_test, g_cm, lo0=lo0, hi0=hi0, step=step)
    if not ok:
        return None, False
    d = solve(b_test, gw, g_cm, vec=vec)
    return {"g_omega2_4pi": gw, "E_b_MeV": d["E_b"], "r_d_fm": d["r_d"],
            "P_D": d["P_D"]}, True


routes = {}
route_bracket_ok = {}
for b_test, label in [(B_TUNED, "tuned"), (R_conf_fm, "R_conf")]:
    rA, okA = solve_route(b_test, 18.31, -5.0, 30.0, step=1.0)
    rB, okB = solve_route(b_test, 0.0, -5.0, 30.0, step=1.0)
    routes[label] = {"b_fm": b_test,
                      "routeA_core_sigma_omega": rA,
                      "routeB_sigma_omega_only": rB}
    route_bracket_ok[label] = {"routeA": okA, "routeB": okB}
results["derived"]["routes"] = routes
results["derived"]["route_bracket_ok"] = route_bracket_ok

# C0: both routes actually found a real root (bracket_ok) at both b values
# compared in this finding's headline claim -- if this fails, C1-C4 below are
# resting on the same silent-garbage failure mode the review pass caught.
c0_ok = all(route_bracket_ok[lbl]["routeA"] and route_bracket_ok[lbl]["routeB"]
            for lbl in ("tuned", "R_conf"))
record("C0 route-A and route-B root search actually bracketed a real root "
       "(not a silent-garbage bisection) at both b=tuned and b=R_conf",
       0.0 if c0_ok else 1.0, 0.5, "integrity", c0_ok,
       extra={"route_bracket_ok": route_bracket_ok})

rA_tuned, rA_conf = routes["tuned"]["routeA_core_sigma_omega"], routes["R_conf"]["routeA_core_sigma_omega"]
rB_tuned, rB_conf = routes["tuned"]["routeB_sigma_omega_only"], routes["R_conf"]["routeB_sigma_omega_only"]

# C1: route A r_d stays within 5% of physical at R_conf (same bar F240 used)
okA_rd = abs(rA_conf["r_d_fm"] - R_D_PHYS) / R_D_PHYS < 0.05
record("C1 route A r_d within 5% of 1.97 fm AT b=R_conf",
       abs(rA_conf["r_d_fm"] - R_D_PHYS) / R_D_PHYS, 0.05, "Tier-B", okA_rd,
       extra=rA_conf)
# C2: route A required omega coupling stays in the OBE/SU(6) empirical window
okA_gw = 3.0 <= rA_conf["g_omega2_4pi"] <= 12.0
record("C2 route A required g_omega^2/4pi stays in the OBE/SU(6) window [3,12]",
       0.0 if okA_gw else 1.0, 0.5, "Tier-B", okA_gw, extra=rA_conf)
# C3: route B r_d stays within 8% of physical at R_conf (same bar F240 used)
okB_rd = abs(rB_conf["r_d_fm"] - R_D_PHYS) / R_D_PHYS < 0.08
record("C3 route B r_d within 8% of 1.97 fm AT b=R_conf",
       abs(rB_conf["r_d_fm"] - R_D_PHYS) / R_D_PHYS, 0.08,
       "Tier-B", okB_rd, extra=rB_conf)
# C4: outputs move by <10% between the tuned b and R_conf (insensitivity)
shift_rd_A = abs(rA_conf["r_d_fm"] - rA_tuned["r_d_fm"]) / rA_tuned["r_d_fm"]
shift_rd_B = abs(rB_conf["r_d_fm"] - rB_tuned["r_d_fm"]) / rB_tuned["r_d_fm"]
shift_gwA = abs(rA_conf["g_omega2_4pi"] - rA_tuned["g_omega2_4pi"]) / rA_tuned["g_omega2_4pi"]
shift_gwB = abs(rB_conf["g_omega2_4pi"] - rB_tuned["g_omega2_4pi"]) / rB_tuned["g_omega2_4pi"]
insensitive = max(shift_rd_A, shift_rd_B) < 0.10
record("C4 r_d shifts <10% between b=0.55 (tuned) and b=R_conf (insensitivity)",
       max(shift_rd_A, shift_rd_B), 0.10, "Tier-B", insensitive,
       extra={"shift_rd_routeA": shift_rd_A, "shift_rd_routeB": shift_rd_B,
              "shift_gomega_routeA": shift_gwA, "shift_gomega_routeB": shift_gwB})

# ---------------------------------------------------------------------------
# D. Stress test: the P2-ECG candidate (b_P2, the weaker of the two
#    candidates per B1/B2) under BOTH routes, now that the bracket fix (C0)
#    makes route A honestly testable there. The original version of this
#    script only ran route B at b_P2 -- route A's OLD fixed [2,9] bracket
#    silently returned garbage at b_P2=0.4111 fm (E_b=14.03 MeV, r_d=0.94 fm)
#    and that failure was never surfaced. With the adaptive bracket it is not
#    garbage: route A has a real, physical (non-negative coupling) root at
#    b_P2 too -- see D1 below. Also locates the b at which route A's required
#    coupling crosses zero (the genuine physical edge of route A, distinct
#    from the old bracket artifact) and checks it sits well clear of every b
#    value this finding actually compares.
# ---------------------------------------------------------------------------
print("\nD  stress check: the weaker P2-ECG candidate under both routes, "
      "and route A's true physical range")

rA_P2, okA_P2 = solve_route(b_P2_fm, 18.31, -5.0, 30.0, step=1.0)
rB_P2, okB_P2 = solve_route(b_P2_fm, 0.0, -5.0, 30.0, step=1.0)
results["derived"]["routeA_at_b_P2"] = rA_P2
results["derived"]["routeB_at_b_P2"] = rB_P2
results["derived"]["b_P2_bracket_ok"] = {"routeA": okA_P2, "routeB": okB_P2}
if okA_P2:
    print(f"  route A at b_P2={b_P2_fm:.4f} fm: g_omega2/4pi={rA_P2['g_omega2_4pi']:.3f} "
          f"r_d={rA_P2['r_d_fm']:.4f} P_D={rA_P2['P_D']*100:.2f}%")
if okB_P2:
    print(f"  route B at b_P2={b_P2_fm:.4f} fm: g_omega2/4pi={rB_P2['g_omega2_4pi']:.3f} "
          f"r_d={rB_P2['r_d_fm']:.4f} P_D={rB_P2['P_D']*100:.2f}%")

# D1: route A at b_P2 is bracket-valid (the old script's silent failure point)
record("D1 route A finds a real (bracket-valid) root at b_P2, the one value "
       "the old fixed-bracket bisect_bind() silently broke on",
       0.0 if okA_P2 else 1.0, 0.5, "integrity", okA_P2,
       extra=(rA_P2 if okA_P2 else {}))

# D2: locate the b at which route A's required g_omega^2/4pi crosses zero --
# the genuine physical edge of route A (a positive-coupling solution stops
# existing beyond it). Cheap version: a coarse linear scan in b (few points,
# narrow g_omega bracket, small N) followed by linear interpolation for the
# zero-crossing -- this only needs to locate the edge to the nearest ~0.01 fm
# for the honest-scope caveat, not machine precision.
def gwA_of_b(b_val, N=300):
    gw, ok = find_root_gomega(b_val, 18.31, lo0=-6.0, hi0=6.0, step=1.0, N=N)
    return gw if ok else float("nan")


b_scan_pts = [0.60, 0.63, 0.66, 0.69, 0.72, 0.75]
gw_scan_pts = [gwA_of_b(bv) for bv in b_scan_pts]
b_crossover = float("nan")
for i in range(len(b_scan_pts) - 1):
    g0, g1 = gw_scan_pts[i], gw_scan_pts[i + 1]
    if g0 == g0 and g1 == g1 and (g0 < 0) != (g1 < 0):
        b0, b1 = b_scan_pts[i], b_scan_pts[i + 1]
        b_crossover = b0 + (b1 - b0) * (0.0 - g0) / (g1 - g0)  # linear interpolation
        break
results["derived"]["routeA_physical_crossover_b_fm"] = b_crossover
results["derived"]["routeA_gw_vs_b_scan"] = dict(zip(b_scan_pts, gw_scan_pts))

# D3: every b this finding actually compares (b_P2, R_conf, b_tuned) sits at
# least 15% below that crossover -- i.e. well inside route A's physical
# window, not near its edge.
margin_ok = False
if b_crossover == b_crossover:
    worst_margin = 1.0 - max(b_P2_fm, R_conf_fm, B_TUNED) / b_crossover
    margin_ok = worst_margin > 0.15
record("D3 every compared b (b_P2, R_conf, b_tuned) sits >=15% below route A's "
       "physical (non-negative coupling) crossover, found near b~0.68 fm",
       (1.0 - max(b_P2_fm, R_conf_fm, B_TUNED) / b_crossover) if b_crossover == b_crossover else 1.0,
       0.15, "integrity", margin_ok,
       extra={"b_crossover_fm": b_crossover})

print(f"\n{'PASS' if PASS else 'FAIL (see above)'}  -- {sum(1 for c in results['checks'].values() if c['status']=='PASS')}/"
      f"{len(results['checks'])} checks")

out_path = os.path.join(HERE, "..", "..", "test-results",
                        "F373_quark_size_from_confinement_radius.json")
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)
print(f"\nWrote {out_path}")
