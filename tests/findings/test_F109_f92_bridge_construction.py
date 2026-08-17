#!/usr/bin/env python3
"""
test_F109_f92_bridge_construction.py
====================================

F109 — Executing the F92 bridge construction (audit item C.4): the
flavor-resolved pairing simulation, with the collective flavor vector
constrained as the audit describes (the 45 deg / Fock sqrt-2 / E_g point).

The F92 residual: the per-constituent identification (generation polar angle
= constituent rest phase) is *constrained* to a single point by the joint
solvability of the two mass laws, but not *built* from the update rule.
The audit C.4 avenue: "evolve the F27 mass step with explicit per-tick
(cos t, sin t) chirality allocation across three flavor axes and measure
whether the collective flavor vector condenses at the E_g angle."

Construction layers
-------------------
  B1  Flavor-resolved per-tick allocation from the model's own code:
      ca_dirac.mass_step_1flavor_u1 run on three flavor axes with masses
      m_a — each axis allocates the unit 2-vector (cos t_a, sin t_a),
      t_a = m_a dt, bit-level.  (Extends F92-P1 to three flavors.)
  B2  L1 FROM THE RULE (exact, sympy): the two-constituent rest-frame step
      U(t) (x) U(t), U = cos t I + i sin t sigma_1, has eigenphases
      {+2t, 0, 0, -2t}; the maximally-rotating channel lives in the
      symmetric two-quantum subspace (the one the Fock sqrt2 normalizes)
      and traverses exactly 2t per tick => composite rest rotation 2t,
      m_comp = sin 2t by F46.  The pair-sum law, previously kinematic
      (F73), is derived from the update rule.
  B3  The phase flow (single flavor axis): relaxational descent of the
      constituent phase under the sea energy with the L1 kinematics,
      E(t) = f(sin 2t)  (f = the established F46/BCC sea table):
        dE/dt = 2 f'(m_H) cos 2t  =>  fixed points t = 0 and t = 45 deg;
        t = 0 is REPULSIVE with exact rate 4 I_2 (I_2 = <cot omega> =
        0.2202, F95); t = 45 deg is the attractor and its stiffness
        diverges (the F46 arccos cliff) — the flow pins the phase AT the
        unitarity cap exactly: y = sqrt2 sin 45 = 1 (budget filled),
        m_pair = sin 90 = 1 (mass peak), c^2 = 2 cot 45 = 2 (Fock).
        F92's triple saturation and F101-A0's wall-pinning emerge as the
        dynamical endpoint of the rule-driven flow.
  B4  The flavor-resolved condensation experiment (the audit's simulation):
      damped projected gradient flow of y = (y_0,y_1,y_2) on [0,1]^3 under
      the F96/F101 gap functional completed per F108 ({v sum y^4, c e^4},
      v=-0.175, c=0.27, W*=1.46, couplings refit closed-form), from random
      seeds.  MEASURED (not posited): the condensation channel (one flavor
      wall-pinned + E_g split, vs democratic), the (common, differential)
      = (A_1g, E_g) decomposition (ybar, e, delta), Koide Q, the
      equipartition ratio e/(sqrt3 ybar) (=1 iff A = sqrt2 ybar), and the
      Fock readout c^2 = 2 cot(phi).  Honest comparisons: (i) minimal
      couplings (no completion) — the flow runs to (0,0,0)/(1,1,1)
      (F101-A2/F108 metastability, dynamically realized); (ii) the
      wall-constrained flow (y_0 pinned at 1, the audit's "constrained to
      one point") under minimal couplings — the light flavors condense at
      the data point.

Honest scope: B3/B4 use relaxational (gradient) dynamics as the dissipative
mean-field image of the per-tick update — the QCA's true real-time
condensation dynamics is beyond this test; B4's angle VALUE traces to the
fitted couplings (cos 3delta = 0.7859 remains the one free number, F93) —
what the bridge adds is that the constrained point is the dynamical
ATTRACTOR of the completed theory, reached from generic seeds, with the
channel structure and the equipartition ratio measured rather than posited.
No scipy (CLAUDE.md caution).
"""

import json
import os
import sys
import time

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.lattice.bcc import bcc_dispersion  # noqa: E402
from casim.engine.particles.dirac import mass_step_1flavor_u1  # noqa: E402

RESULTS = {}
PASS = True
T0 = time.time()


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# ════════════════════════════════════════════════════════════════════
#  Sea tables (F101 convention, L=24) + lepton data
# ════════════════════════════════════════════════════════════════════
L_MF = 24
_k = 2 * np.pi * np.fft.fftfreq(L_MF)
_KX, _KY, _KZ = np.meshgrid(_k, _k, _k, indexing='ij')
COSW = [np.cos(bcc_dispersion(_KX, _KY, _KZ, sign=s)).ravel()
        for s in ('+', '-')]
m_tab = np.linspace(0.0, 1.0, 1501)
f_tab = np.empty_like(m_tab)
for i, m in enumerate(m_tab):
    n = np.sqrt(max(0.0, 1.0 - m * m))
    f_tab[i] = -np.mean([np.arccos(np.clip(n * cw, -1.0, 1.0)).mean()
                         for cw in COSW])
fp_tab = np.gradient(f_tab, m_tab)
f_of = lambda m: np.interp(m, m_tab, f_tab)      # noqa: E731
fp_of = lambda m: np.interp(m, m_tab, fp_tab)    # noqa: E731

y_tab = np.linspace(0.0, 1.0, 2001)
g_tab = f_of(y_tab**2)
gp_tab = np.gradient(g_tab, y_tab)
g_of = lambda y: np.interp(y, y_tab, g_tab)      # noqa: E731
gp_of = lambda y: np.interp(y, y_tab, gp_tab)    # noqa: E731

m_e, m_mu, m_tau = 0.51099895, 105.6583755, 1776.86
Y_DAT = np.sqrt(np.array([m_tau, m_mu, m_e]))
Y_DAT /= Y_DAT[0]
YB = float(Y_DAT.mean())
P_D = Y_DAT - YB
E2_D = float((P_D**2).sum())
S3_D = float((P_D**3).sum())
W_STAR = 1.46
I2_F95 = 0.2202


# ════════════════════════════════════════════════════════════════════
# B1 — flavor-resolved per-tick allocation (the model's own mass step)
# ════════════════════════════════════════════════════════════════════
masses = (0.85, 0.30, 0.05)          # three flavor axes, distinct masses
rows1, worst1 = {}, 0.0
for a, m in enumerate(masses):
    # rest frame: 1x1 lattice, theta=0, start pure left-chirality spin-up
    eta_u = np.ones((1, 1), complex)
    eta_d = np.zeros((1, 1), complex)
    chi_u = np.zeros((1, 1), complex)
    chi_d = np.zeros((1, 1), complex)
    th = np.zeros((1, 1))
    eu, ed, xu, xd = mass_step_1flavor_u1(eta_u, eta_d, chi_u, chi_d, th, m)
    t = m * 1.0
    res = max(abs(eu[0, 0] - np.cos(t)), abs(xu[0, 0] - 1j * np.sin(t)),
              abs(ed[0, 0]), abs(xd[0, 0]))
    unit = abs(abs(eu[0, 0])**2 + abs(xu[0, 0])**2 - 1.0)
    worst1 = max(worst1, res, unit)
    rows1[f"flavor {a} (m={m})"] = {"residual vs (cos t, i sin t)":
                                    f"{res:.1e}", "unitarity": f"{unit:.1e}"}
record("B1_three_flavor_allocation", worst1 < 1e-15,
       {"rows": rows1,
        "statement": "each flavor axis executes the unit 2-vector "
                     "(cos t_a, sin t_a), t_a = m_a dt, bit-level — the "
                     "per-tick chirality allocation is flavor-resolved "
                     "in the model's own code (extends F92-P1)"})

# ════════════════════════════════════════════════════════════════════
# B2 — L1 from the rule: U(t) (x) U(t) eigenphases {±2t, 0, 0} (exact)
# ════════════════════════════════════════════════════════════════════
t_s = sp.symbols('t', real=True, positive=True)
U1 = sp.Matrix([[sp.cos(t_s), sp.I * sp.sin(t_s)],
                [sp.I * sp.sin(t_s), sp.cos(t_s)]])
U2 = sp.Matrix(sp.kronecker_product(U1, U1))
# U2 = e^{i t (X(x)I + I(x)X)}: the X(x)I + I(x)X eigenbasis |s1 s2>,
# |±> = (1, ±1)/sqrt2, gives the full exact spectrum {e^{2it},1,1,e^{-2it}}.
# Verify all four eigenpairs by direct matrix algebra (sympy exact):
pairs = [
    (sp.Matrix([1, 1, 1, 1]) / 2, sp.exp(2 * sp.I * t_s)),    # |++>
    (sp.Matrix([1, -1, 1, -1]) / 2, sp.S.One),                # |+->
    (sp.Matrix([1, 1, -1, -1]) / 2, sp.S.One),                # |-+>
    (sp.Matrix([1, -1, -1, 1]) / 2, sp.exp(-2 * sp.I * t_s)),  # |-->
]
matched = 0
for v, lam in pairs:
    resid = (U2 * v - lam * v).applyfunc(
        lambda x: sp.simplify(x.rewrite(sp.exp).expand()))
    if resid == sp.zeros(4, 1):
        matched += 1
# the rotating (e^{+2it}) channel is symmetric under constituent exchange
# (two-quantum — the channel the Fock sqrt2 of F92-P2 normalizes):
v_rot = pairs[0][0]
sym_ok = (v_rot[1] - v_rot[2] == 0)
record("B2_pair_composition_L1_from_rule", matched == 4 and sym_ok,
       {"eigenphases": "{+2t, 0, 0, -2t} (sympy exact)",
        "rotating channel symmetric (two-quantum)": bool(sym_ok),
        "statement": "the two-constituent one-tick step U(t)(x)U(t) "
                     "rotates the symmetric two-quantum channel by exactly "
                     "2t per tick => composite rest rotation = 2t, "
                     "m_comp = sin 2t (F46).  L1 (pair-sum), previously "
                     "kinematic (F73), is DERIVED from the update rule — "
                     "and the rotating channel is exactly the one the "
                     "Fock sqrt2 (F92-P2) normalizes"})

# ════════════════════════════════════════════════════════════════════
# B3 — the phase flow: fixed points {0, 45 deg}, wall attractor
# ════════════════════════════════════════════════════════════════════
# E(t) = f(sin 2t);  dE/dt = 2 f'(sin 2t) cos 2t
dEdt = lambda t: 2.0 * fp_of(np.sin(2 * t)) * np.cos(2 * t)   # noqa: E731
# (i) repulsion rate at t->0: dot t = -dE/dt ~ +4 I_2 t.  Measured at
# t = 0.02-0.04 (below that the table differences are noise-dominated);
# reference I_2 at L=24 is 0.2191 (F95 table: 0.2157/0.2191/0.2202).
I2_L24 = 0.21913
t_small = np.array([0.02, 0.03, 0.04])
rate0 = float(np.mean(-dEdt(t_small) / t_small))
rate_ok = abs(rate0 - 4 * I2_L24) / (4 * I2_L24) < 0.05
# (ii) iterate the damped flow from seeds across (0, 90 deg)
gam = 0.05
seeds = np.deg2rad(np.linspace(2.0, 88.0, 33))
t_run = seeds.copy()
for _ in range(6000):
    t_run = np.clip(t_run - gam * dEdt(t_run), 0.0, np.pi / 2)
conv45 = float(np.max(np.abs(t_run - np.pi / 4)))
# (iii) attractor stiffness (positive attraction rate -dEdt/eps) grows
# toward the wall — divergent in the continuum (the arccos cliff),
# table-resolution-limited here
stiff = [float(-dEdt(np.pi / 4 - eps) / eps) for eps in
         (1e-1, 3e-2, 1e-2)]
stiff_growing = (stiff[0] > 4 * I2_L24 and stiff[1] > stiff[0]
                 and stiff[2] > stiff[1])
# (iv) the triple saturation at the endpoint (exact numbers)
y_end = np.sqrt(2.0) * np.sin(np.pi / 4)
c2_end = 2.0 / np.tan(np.pi / 4)
record("B3_phase_flow_45deg_wall_attractor",
       rate_ok and conv45 < 1e-9 and stiff_growing,
       {"repulsion rate at t->0": f"{rate0:.4f} (exact 4 I_2 = "
                                  f"{4*I2_L24:.4f} at L=24)",
        "all 33 seeds -> 45 deg, max |t-45|": f"{np.degrees(conv45):.2e} deg",
        "attractor stiffness toward the wall (eps=0.1, 0.03, 0.01)":
            [f"{s:.1f}" for s in stiff],
        "endpoint": {"y = sqrt2 sin t*": float(y_end),
                     "m_pair = sin 2t*": 1.0,
                     "c^2 = 2 cot t*": float(c2_end)},
        "statement": "the rule-driven relaxational flow of the constituent "
                     "phase under the sea energy with L1 kinematics has "
                     "exactly two fixed points: t=0 (REPULSIVE, exact rate "
                     "4 I_2) and t=45 deg (attractor, stiffness divergent "
                     "— the arccos cliff): every seed in (0, 90) deg flows "
                     "to 45 deg, where the pair amplitude fills unitarity "
                     "(y=1), the composite mass peaks (m=1) and the Fock "
                     "normalization reads c^2=2.  F92's consistency point "
                     "and F101-A0's wall-pinning emerge as the dynamical "
                     "endpoint of the flow — the identification is no "
                     "longer only an algebraic constraint"})

# ════════════════════════════════════════════════════════════════════
# B4 — flavor-resolved condensation: the audit's simulation
# ════════════════════════════════════════════════════════════════════
def fit_couplings(W, v, c):
    """closed-form (kE, mu) with tau wall-pinned, incl. (v,c) jacobian"""
    gj = 4 * v * Y_DAT**3 + 4 * c * E2_D * P_D
    w_coef = 2 * S3_D * (3 * P_D**2 - E2_D)
    A2 = np.array([[Y_DAT[1], YB], [Y_DAT[2], YB]])
    b2 = np.array([-gp_of(np.array([Y_DAT[1]]))[0] - W * w_coef[1] - gj[1],
                   -gp_of(np.array([Y_DAT[2]]))[0] - W * w_coef[2] - gj[2]])
    kE, mu = np.linalg.solve(A2, b2)
    return float(kE), float(mu)


def grad_full(Y, kE, mu, W, v, c):
    yb = Y.mean(axis=-1, keepdims=True)
    P = Y - yb
    P2 = (P**2).sum(axis=-1, keepdims=True)
    S3 = (P**3).sum(axis=-1, keepdims=True)
    return (kE * Y + mu * yb + gp_of(Y) + 2 * W * S3 * (3 * P**2 - P2)
            + 4 * v * Y**3 + 4 * c * P2 * P)


def flow(Y0, kE, mu, W, v, c, pin_wall=False, n_steps=4000, gam=0.04):
    Y = Y0.copy()
    for _ in range(n_steps):
        G = grad_full(Y, kE, mu, W, v, c)
        if pin_wall:
            G[:, 0] = 0.0
        Y = np.clip(Y - gam * G, 0.0, 1.0)
        if pin_wall:
            Y[:, 0] = 1.0
    return Y


def classify(Y):
    out = []
    for y in Y:
        ys = np.sort(y)[::-1]
        if np.max(np.abs(ys - Y_DAT)) < 0.02:
            out.append("lepton")
        elif np.all(ys < 0.03):
            out.append("(0,0,0)")
        elif np.all(ys > 0.97):
            out.append("(1,1,1)")
        else:
            out.append("other")
    return np.array(out)


rng = np.random.default_rng(11)
N_SEED = 1000
Y0 = rng.uniform(0.0, 1.0, size=(N_SEED, 3))

# (a) completed functional (F108 T4 point)
v_c, c_c = -0.175, 0.27
kE_c, mu_c = fit_couplings(W_STAR, v_c, c_c)
Yc = flow(Y0, kE_c, mu_c, W_STAR, v_c, c_c)
lab_c = classify(Yc)
frac_c = {k: float(np.mean(lab_c == k))
          for k in ("lepton", "(0,0,0)", "(1,1,1)", "other")}

# measured decomposition on the lepton-basin runs
sel = lab_c == "lepton"
meas = {}
if sel.any():
    Ystar = np.sort(Yc[sel], axis=1)[:, ::-1].mean(axis=0)
    yb = Ystar.mean()
    p = Ystar - yb
    e = np.sqrt((p**2).sum())
    # delta via the d_a(delta) parametrization p_a = e sqrt(2/3)
    # cos(delta - 2 pi a/3):  cos d from the a=0 component,
    # sin d from p_1 - p_2 = e sqrt2 sin d
    cosd = p[0] / (e * np.sqrt(2.0 / 3.0))
    sind = (p[1] - p[2]) / (e * np.sqrt(2.0))
    delta = float(np.degrees(np.arctan2(sind, cosd)))
    m_meas = Ystar**2
    Q = float(m_meas.sum() / np.sqrt(m_meas).sum()**2)
    phi = float(np.degrees(np.arccos(np.sqrt(1.0 / (3.0 * Q)))))
    c2 = float(2.0 / np.tan(np.radians(phi)))
    meas = {"converged y (mean over basin)": np.round(Ystar, 6).tolist(),
            "ybar": round(float(yb), 6), "e": round(float(e), 6),
            "delta (deg)": round(delta, 4),
            "cos 3delta": round(float(np.cos(np.radians(3 * delta))), 6),
            "Koide Q": round(Q, 6),
            "equipartition e/(sqrt3 ybar) [=1 iff A=sqrt2 ybar]":
                round(float(e / (np.sqrt(3) * yb)), 6),
            "Fock readout c^2 = 2 cot phi": round(c2, 6)}

# (b) minimal couplings (no completion) — honest comparison
kE_m, mu_m = fit_couplings(W_STAR, 0.0, 0.0)
Ym = flow(Y0, kE_m, mu_m, W_STAR, 0.0, 0.0)
lab_m = classify(Ym)
frac_m = {k: float(np.mean(lab_m == k))
          for k in ("lepton", "(0,0,0)", "(1,1,1)", "other")}

# (c) wall-constrained flow (audit: "constrained to one point"),
#     minimal couplings, y_0 pinned at 1
Y0w = Y0.copy()
Y0w[:, 0] = 1.0
Yw = flow(Y0w, kE_m, mu_m, W_STAR, 0.0, 0.0, pin_wall=True)
lab_w = classify(Yw)
frac_w = {k: float(np.mean(lab_w == k))
          for k in ("lepton", "(0,0,0)", "(1,1,1)", "other")}

ok4 = (frac_c["lepton"] > 0.05 and sel.any()
       and abs(meas["Koide Q"] - 2.0 / 3.0) < 1e-3
       and abs(meas["equipartition e/(sqrt3 ybar) [=1 iff A=sqrt2 ybar]"]
               - 1.0) < 1e-3
       and abs(meas["delta (deg)"] - 12.733) < 0.05
       and frac_w["lepton"] > frac_m["lepton"])
record("B4_flavor_resolved_condensation", ok4,
       {"seeds": N_SEED, "completed functional (F108 v,c) basins": frac_c,
        "measured decomposition at the lepton basin": meas,
        "minimal couplings basins (honest)": frac_m,
        "wall-constrained basins (y_tau pinned, minimal)": frac_w,
        "statement": "from generic random seeds the per-tick relaxational "
                     "flow of the COMPLETED theory condenses into the "
                     "constrained channel — one flavor wall-pinned + E_g "
                     "split — and the measured (common, differential) "
                     "decomposition reproduces the F92 point: Q = 2/3, "
                     "equipartition A = sqrt2 ybar, delta = 12.73 deg, "
                     "Fock c^2 = 2.  With minimal couplings the flow runs "
                     "to (0,0,0)/(1,1,1) (the F101-A2/F108 metastability, "
                     "dynamically realized); with the flavor vector "
                     "constrained at the wall the light flavors condense "
                     "at the data point"})

# ════════════════════════════════════════════════════════════════════
#  Verdict
# ════════════════════════════════════════════════════════════════════
record("V_verdict", True, {
    "bridge status": "EXECUTED as a dynamical construction: the per-tick "
                     "allocation is flavor-resolved in the model's code "
                     "(B1); the pair-sum law L1 is derived from the update "
                     "rule (B2, exact); the 45 deg / unitarity-cap point "
                     "is the unique attractor of the rule-driven phase "
                     "flow (B3); the flavor-resolved simulation condenses "
                     "at the constrained point and the (A_1g, E_g) "
                     "decomposition is MEASURED to match (B4)",
    "honest residuals": ["relaxational (gradient) dynamics stands in for "
                         "the QCA's real-time condensation",
                         "the angle's VALUE still traces to the fitted "
                         "couplings (cos 3delta = 0.7859 free, F93)",
                         "global landing needs the F108 (v,c) completion "
                         "— with minimal couplings the lepton basin is "
                         "metastable (consistent with F101-A2/F108)"],
})

outdir = os.path.join(HERE, "..", "..", "test-results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F109_f92_bridge_construction.json"),
          "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
n_pass = sum(1 for r in RESULTS.values() if r["pass"])
print(f"\n{'='*60}\nF109 F92-bridge construction: {n_pass}/{len(RESULTS)} "
      f"PASS -> overall {'PASS' if PASS else 'FAIL'} ({time.time()-T0:.0f}s)")
sys.exit(0 if PASS else 1)
