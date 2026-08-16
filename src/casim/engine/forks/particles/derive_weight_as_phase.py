#!/usr/bin/env python3
"""
E1 attack: derive the 'weight-as-phase' principle behind delta* = 2/9 rad.

The number 2/9 is derived (F175): the exact E_g representation weight
    2/9 = dim(E_g) / dim(T_1u (x) T_1u)  (O_h projection).
The OPEN residual: why does the SATURATED CONDENSATE PHASE (in radians)
equal that dimensionless weight?  (F230 sharpened it to a dimensional
no-go: a radian != a pure ratio without a scale.)

This script attempts the two routes named in the E1 prompt:
  (A) saturation equipartition (F92 route)
  (B) BCC 2nd-shell topological-moment (holonomy / Berry-phase) computation

All arithmetic is exact (sympy Rational / algebraic) or real float; no chiral
transforms, so numpy is safe where used.  Emits a JSON result file.
"""

import json, itertools
import numpy as np
import sympy as sp
from casim.constants import (
    delta_star as _delta_star,
    delta_star_f as _delta_star_f,
    e_saturation as _e_saturation,
)

RESULTS = {}

# ---------------------------------------------------------------------------
# PART A0 -- Verify the group theory: 2/9 is the E_g weight (reproduces F175 D1)
# ---------------------------------------------------------------------------
# O_h proper rotation subgroup O (24 elements) is enough for the reduction of
# T_1u (x) T_1u restricted to the rotation content (parity is g x g regardless).
# Character of T_1u = vector rep on the rotation classes of O:
#   classes: E(1), 8 C3, 6 C2', 6 C4, 3 C2(=C4^2)
# chi_vector: E=3, C3=0, C2'=-1, C4=1, C2=-1
# T_1u(x)T_1u character = chi_vector^2:
cls = {"E":1, "C3":8, "C2p":6, "C4":6, "C2":3}          # class sizes, |O|=24
chi_vec = {"E":3, "C3":0, "C2p":-1, "C4":1, "C2":-1}     # T_1u ~ vector
chi_prod = {k: chi_vec[k]**2 for k in cls}               # T_1u (x) T_1u

# irreps of O and their characters (A1,A2,E,T1,T2)
irr = {
 "A1": {"E":1,"C3":1,"C2p":1,"C4":1,"C2":1},
 "A2": {"E":1,"C3":1,"C2p":-1,"C4":-1,"C2":1},
 "E":  {"E":2,"C3":-1,"C2p":0,"C4":0,"C2":2},
 "T1": {"E":3,"C3":0,"C2p":-1,"C4":1,"C2":-1},
 "T2": {"E":3,"C3":0,"C2p":1,"C4":-1,"C2":-1},
}
mult = {}
for name, ch in irr.items():
    m = sp.Rational(sum(cls[k]*chi_prod[k]*ch[k] for k in cls), 24)
    mult[name] = m
dims = {"A1":1,"A2":1,"E":2,"T1":3,"T2":3}
total = sum(mult[n]*dims[n] for n in irr)          # should be 9
Eg_weight = sp.Rational(dims["E"]*mult["E"], total)  # 2/9

RESULTS["A0_group_theory"] = {
    "decomposition": {n:int(mult[n]) for n in irr},
    "total_dim": int(total),
    "mult_E": int(mult["E"]),
    "Eg_weight": str(Eg_weight),
    "equals_2_9": bool(Eg_weight == _delta_star),
}
print("A0  T1u(x)T1u =", {n:int(mult[n]) for n in irr},
      " total", int(total), " E_g weight", Eg_weight)

# ---------------------------------------------------------------------------
# The measured lepton azimuth, for reference
# ---------------------------------------------------------------------------
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86  # MeV, PDG
s = [np.sqrt(x) for x in (me,mmu,mtau)]
Q = (me+mmu+mtau)/ (sum(s)**2 )
# Koide circulant fit: sqrt(m_a) = mu (1 + r cos(delta + 2 pi a /3)), r=sqrt2
# solve delta from the three sqrt-masses (least-squares over a-labelling)
def fit_delta():
    sbar = np.mean(s)
    # amplitude vector components
    c = np.array([ (s[a]/sbar - 1) for a in range(3)])   # = r cos(delta+2pi a/3)
    # project onto cos/sin basis
    a_idx = np.arange(3)
    C = np.sum(c*np.cos(2*np.pi*a_idx/3))
    S = np.sum(c*np.sin(2*np.pi*a_idx/3))
    delta = np.arctan2(-S, C)   # phase
    return delta % (2*np.pi/3)
delta_meas = fit_delta()
RESULTS["A0b_measured"] = {
    "Q": Q, "3delta_meas": 3*delta_meas, "delta_meas": delta_meas,
    "delta_vs_2_9_pct": abs(delta_meas - _delta_star_f)/(_delta_star_f)*100,
    "3delta_vs_2_3_pct": abs(3*delta_meas - 2/3)/(2/3)*100,
}
print("A0b Q =", round(Q,6), " delta_meas =", round(delta_meas,6),
      " 2/9 =", round(_delta_star_f,6), " (%%err %.3f)" % (abs(delta_meas-_delta_star_f)/(_delta_star_f)*100))

# ---------------------------------------------------------------------------
# PART A -- Saturation-equipartition route
# ---------------------------------------------------------------------------
# Model the order parameter as a UNIT vector Psi in the 9-dim T1u(x)T1u space,
# with an orthogonal decomposition into channels of dim {A1:1,Eg:2,T1g:3,T2g:3}
# (this is the *symmetric+antisymmetric* Hermitian bilinear, 9 real dof, per
# F175 fn.8).  "Saturation" = maximal democracy: |Psi_i|^2 = 1/9 on each basis
# state (max entropy on the 9-simplex).  Then the E_g channel carries weight
#   w_Eg = (dim E_g)/9 = 2/9   [derived above]
#
# The 'weight-as-phase' claim is delta* = w_Eg *in radians*.  We test WHAT
# additional input turns the dimensionless weight into a radian, and whether
# any natural in-model normalization supplies it *without* a free scale.

delta_var, R = sp.symbols('delta R', positive=True)

# Landau angular energy (F93/F95/F118): F(delta)=B cos3d + C cos^2 3d
B = sp.Symbol('B', real=True)      # derived negative (F95)
C = sp.Symbol('C', positive=True)  # = lambda6 e^6  (open)
F = B*sp.cos(3*delta_var) + C*sp.cos(3*delta_var)**2
dF = sp.diff(F, delta_var)
# stationary interior: cos3delta = -B/(2C)   (F230 dynamical relation)
crit = sp.solve(sp.Eq(sp.cos(3*delta_var), -B/(2*C)), delta_var)
RESULTS["A1_landau"] = {
    "dF": str(sp.simplify(dF)),
    "interior_relation": "cos(3*delta) = -B/(2C)  (one eqn, two unknowns delta & C)",
    "note": "Q is delta-blind (F199): Q=1/3+r^2/6 has dQ/ddelta=0, so no 2nd kinematic eqn.",
}

# Equipartition principle, stated precisely as a testable identity:
#   POSIT-N (normalization): the full-bilinear democratic phase budget = 1 rad,
#   i.e. the E_g rotation generator L_Eg is normalized so a unit-amplitude
#   (R=1) democratic condensate sweeps unit arc-length per unit weight.
# Under POSIT-N, arc swept by E_g channel = (weight)*(R) = (2/9)*1 = 2/9 rad.
#
# We check the two logical branches:
#   (i)  WITH POSIT-N and R=1: delta = weight * R = 2/9  -> matches 2/9 exactly.
#   (ii) WITHOUT POSIT-N: delta = weight * R  with R free -> delta unconstrained.
weight = _delta_star
delta_withN = weight*1
delta_general = weight*R   # R = generator-norm / amplitude ratio, a free scale
RESULTS["A2_equipartition"] = {
    "posit_N": "E_g generator unit-normalized: democratic phase budget = 1 rad",
    "delta_with_posit": str(delta_withN),
    "delta_with_posit_float": float(delta_withN),
    "matches_2_9": bool(delta_withN == _delta_star),
    "delta_without_posit": str(delta_general)+"  (R free => delta free)",
    "verdict": ("Given POSIT-N (+unit amplitude), delta*=2/9 rad EXACTLY. "
                "Without it delta=weight*R is scale-degenerate. So equipartition "
                "reduces E1 to the SINGLE posit that the E_g generator norm =1 "
                "(equivalently the democratic phase budget = 1 rad)."),
}
print("A2  equipartition: with POSIT-N  delta* =", delta_withN,
      "=", float(delta_withN), " | matches 2/9:", delta_withN==_delta_star)

# Is POSIT-N derivable?  Test the natural candidate:  the E_g generator norm is
# fixed by the *saturation amplitude* e (F92, e=0.733...) and the F92 pair
# factor sqrt2.  We check whether e, sqrt2, or any O(1) combination equals the
# value needed to make R=1.  R needed = 1 exactly.  Candidate norms:
e_sat = _e_saturation   # F92/F234 saturation amplitude
cands = {
    "1 (bare)": 1.0,
    "e_sat": e_sat,
    "1/e_sat": 1/e_sat,
    "sqrt2*e_sat^2 (=y unitarity)": np.sqrt(2)*e_sat**2,
    "e_sat^2": e_sat**2,
}
RESULTS["A3_posit_N_derivable"] = {
    "R_needed": 1.0,
    "candidates": {k: v for k,v in cands.items()},
    "any_forces_R1_exactly": any(abs(v-1.0) < 1e-9 for v in cands.values()),
    "verdict": ("No O(1) saturation combination equals 1 exactly except the bare "
                "'set generator norm =1' choice itself -> POSIT-N is an assumption, "
                "not derived.  This is F230's 'missing dynamical scale', now named "
                "concretely as the E_g generator normalization."),
}
print("A3  R needed = 1;  candidate norms:", {k:round(v,4) for k,v in cands.items()})

# ---------------------------------------------------------------------------
# PART B -- BCC 2nd-shell topological-moment / holonomy computation
# ---------------------------------------------------------------------------
# A topological moment (winding number / holonomy) is INTRINSICALLY a phase
# (arc/radius), so if 2/9 rad arises as a genuine holonomy it would close E1
# WITHOUT an external scale.  We test the natural candidates on the BCC 2nd
# shell (6 axis sites +-x,+-y,+-z), whose perm rep is A1g (+) E_g (+) T1u.

# E_g real basis on the 6 axis sites (d_z2, d_x2-y2), normalized columns:
sites = [( 1,0,0),(-1,0,0),(0, 1,0),(0,-1,0),(0,0, 1),(0,0,-1)]
def dz2(v): x,y,z=v; return (2*z*z - x*x - y*y)   # ~ 3z^2 - r^2
def dx2y2(v): x,y,z=v; return (x*x - y*y)
u = np.array([dz2(v)  for v in sites], float)
w = np.array([dx2y2(v) for v in sites], float)
u /= np.linalg.norm(u); w /= np.linalg.norm(w)
RESULTS["B0_Eg_basis"] = {"u_dz2": u.tolist(), "w_dx2y2": w.tolist(),
                          "orthonormal": bool(abs(u@w)<1e-12 and abs(u@u-1)<1e-12)}

# C3 about the body diagonal (1,1,1): cyclic x->y->z->x on the sites.
def c3(v): x,y,z=v; return (z,x,y)
perm = [sites.index(c3(v)) for v in sites]
# action on the E_g plane: project the permuted basis back onto (u,w)
def eg_matrix_of_perm(P):
    uP = u[P]; wP = w[P]
    M = np.array([[uP@u, wP@u],[uP@w, wP@w]])
    return M
M_c3 = eg_matrix_of_perm(perm)
theta_c3 = np.arctan2(M_c3[1,0], M_c3[0,0])   # rotation angle in E_g plane
RESULTS["B1_C3_on_Eg"] = {
    "matrix": M_c3.tolist(),
    "rotation_angle_rad": float(theta_c3),
    "as_fraction_of_2pi": float(theta_c3/(2*np.pi)),
    "expected_2pi/3": float(2*np.pi/3),
    "note": "C3 acts on E_g doublet as rotation by 2pi/3 => Landau invariant cos(3 delta). "
            "This is a rational multiple of pi (allowed 'winding' kind); it does NOT single "
            "out 2/9 rad.",
}
print("B1  C3 on E_g rotates by", round(theta_c3,6),
      "rad =", round(theta_c3/(2*np.pi),4), "* 2pi  (=2pi/3 =", round(2*np.pi/3,6), ")")

# Candidate topological invariants that could be 2/9:
#   (a) full C3 holonomy of E_g / 2pi = (2pi/3)/2pi = 1/3   -> not 2/9
#   (b) E_g weight in the perm rep of the 6 sites = dim E_g / 6 = 2/6 = 1/3 -> not 2/9
#   (c) E_g weight in the *bilinear* T1u(x)T1u = 2/9  (this is the F175 count,
#       but it is a REPRESENTATION MULTIPLICITY, not a holonomy: it carries no
#       intrinsic radian scale -> same obstruction as Part A).
holonomy_over_2pi = float(theta_c3/(2*np.pi))          # 1/3
perm_weight = sp.Rational(2,6)                          # 1/3
RESULTS["B2_candidates"] = {
    "C3_holonomy_over_2pi": holonomy_over_2pi,   # 1/3
    "Eg_weight_in_6site_perm": str(perm_weight), # 1/3
    "Eg_weight_in_bilinear": "2/9 (multiplicity, not holonomy)",
    "finding": ("The only genuine HOLONOMY the BCC 2nd shell supplies in the E_g "
                "channel is 2pi/3 (=> 1/3 of a turn), a rational multiple of pi. "
                "2/9 appears ONLY as a representation MULTIPLICITY (dim ratio), which "
                "is scale-free and therefore cannot BE a radian without the same "
                "POSIT-N normalization. No lattice holonomy = 2/9 rad exists."),
}
print("B2  holonomy/2pi =", holonomy_over_2pi, " 6-site E_g weight =", perm_weight,
      " | genuine holonomy is 2pi/3, NOT 2/9 rad")

# B3 -- is 2/9 rad any symmetry-quantized holonomy 2*pi*p/q?  (small q sweep)
tol = 1e-6
hits = []
for q in range(1, 25):
    for p in range(1, q):
        if abs(2*np.pi*p/q - _delta_star_f) < 1e-3:
            hits.append((p, q, 2*np.pi*p/q))
RESULTS["B3_quantized_phase_sweep"] = {
    "target_2_9_rad": _delta_star_f,
    "matches_2pi_p_over_q_within_1e-3": hits,
    "verdict": ("2/9 rad = 0.2222 is not close to any low-order quantized phase "
                "2*pi*p/q (the smallest, 2*pi/28=0.2244, is neither symmetry-natural "
                "nor equal). Confirms 2/9 rad is NOT a lattice holonomy. A ZIP "
                "'difference of moments' is likewise a dimensionless integer/rational "
                "and would still need POSIT-N to become a radian."),
}
print("B3  2/9 rad vs quantized 2pi*p/q within 1e-3:", hits, "(none symmetry-natural)")

# ---------------------------------------------------------------------------
# Overall verdict
# ---------------------------------------------------------------------------
RESULTS["VERDICT"] = {
    "route_A_equipartition": ("REDUCES E1 to ONE named posit (POSIT-N: E_g generator "
        "unit-normalized so the democratic phase budget = 1 rad). Given it, "
        "delta*=2/9 rad exactly. Not independently derivable from saturation."),
    "route_B_topological": ("NEGATIVE: the only genuine E_g holonomy on the BCC 2nd "
        "shell is 2pi/3 (rational-multiple-of-pi). 2/9 is a representation "
        "multiplicity, not a holonomy; it has no intrinsic radian scale."),
    "net": ("E1 does NOT close positive. But it SHARPENS: the F230 'missing dynamical "
        "scale' is now identified concretely as POSIT-N -- the E_g order-parameter "
        "generator normalization. The whole EW/lepton open frontier reduces to this "
        "single normalization constant (weight->radian bridge). A topological "
        "(scale-free) origin is excluded: lattice holonomies are multiples of pi/3, "
        "not 2/9."),
}

# Roadmap C5. The WRITE is guarded; the derivation above is not. As a
# `ca-simulation/` script this only ever ran when invoked, so an unguarded
# write was harmless. Inside the package it is not: anything that imports the
# module recursively — `pkgutil.walk_packages`, pytest collecting `src/`,
# coverage, `casim index` at C8 — would silently overwrite a COMMITTED baseline
# artifact, which is one of the files `make drift` compares against HEAD. The
# guard keeps `python3 -m casim.engine.particles.derive_weight_as_phase`
# working while making an import unable to touch the baseline.
if __name__ == "__main__":
    from casim.engine.particles._results_path import results_path

    _out = results_path("weight_as_phase_E1.json")
    with open(_out, "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    print("\nwrote", _out)

print("VERDICT:", RESULTS["VERDICT"]["net"])
