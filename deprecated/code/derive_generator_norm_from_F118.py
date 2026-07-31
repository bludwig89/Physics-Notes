# ===== deprecated/code backup =====================================
# source     : ca-simulation/derive_generator_norm_from_F118.py
# migrated   : 2026-07-30 - 16:06
# target     : src/casim/engine/particles/derive_generator_norm.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: derive_generator_norm_from_F118.py)
# stripped   : (nothing)
# reason     : S6-F253-weight-as-phase — Pre-decision framing. Its R=1 derivation is the F255 content and stands; its VER
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
#!/usr/bin/env python3
"""[PRE-DECISION FRAMING 2026-07-16 — ledger S6-F253-weight-as-phase]

  This script predates the weight-as-phase DECISION and its VERDICT section
  below is stated in the pre-decision frame. Read it with that in mind.

  STILL LIVE — and load-bearing: PART (a), the Schur-isotropy proof that the
    E_g irrep metric is isotropic and therefore R = 1 is FORCED. That is the
    F255 content, it is derived rather than posited, and it is what removed
    F253's 'free R' escape hatch. Nothing here supersedes it.

  SUPERSEDED — the framing, not the algebra: the VERDICT's conclusion that
    "E1 does not close" and that deriving 2/9 from lambda_6 is CIRCULAR was
    correct as an argument about the DYNAMICAL route, and F256 subsequently
    proved that route cannot close in principle (B and C are independent O(1)
    objects with no locking relation). The 2026-07-16 decision closes E1 a
    different way: by ADOPTING delta* = 2/9 as a founding principle, which
    makes lambda_6 = |B|/(2 e^6 cos(2/3)) an OUTPUT rather than an input. So
    the circularity this script identifies is real and is precisely WHY the
    arrow was reversed — not an open defect.

  Do not read "lambda6 ... value is un-pinned except through delta*" below as
  a live open problem. That IS the adopted structure.

  See docs/theory/supersessions.yaml and docs/theory/key-decisions.md.

E1 follow-up: does the F118/F234 self-consistent (W,v,c) solve implicitly fix
the E_g generator normalization R (the 'POSIT-N' of F253)?

F253 reduced E1 to one posit:
    POSIT-N = (a) the E_g phase is a genuine radian (generator norm R=1), AND
              (b) that radian equals the E_g weight 2/9.
This script checks whether the F118 functional supplies (a) and/or (b).

F118 functional (2nd-shell flavour):
    E(y) = (3k0/2) ybar^2 + (kE/2) e^2 + sum g(y_a)
           + W (sum p_a^3)^2 + v sum y_a^4 + c e^4
    p_a = y_a - ybar,   e^2 = sum p_a^2 (the E_g magnitude),
    delta = arg of the E_g doublet (the angular coordinate).
Landau angular part:  F(delta) = B cos3d + C cos^2 3d,  cos3d* = -B/(2C),
    B derived (F95, sea loop) = -0.0569 ;  C = lambda6 e^6  (open).

All exact/real arithmetic; no chiral transforms.
"""
import json
import numpy as np
import sympy as sp
from casim.constants import (
    B_sea_cubic as _B_sea_cubic,
    delta_star_f as _delta_star_f,
    lambda_6 as _lambda_6,
)

R = {}

# PDG charged-lepton sqrt-mass amplitudes -> Koide y_a
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
s = np.sqrt(np.array([mtau, mmu, me]))     # order heavy->light (tau wall-pinned)
ybar = s.mean()
p = s - ybar                                # deviations
e_amp = np.linalg.norm(p)                   # e = |p|

# ---------------------------------------------------------------------------
# PART (a) -- is delta a GENUINE radian in the deviation simplex? (R=1 test)
# ---------------------------------------------------------------------------
# The deviation vector p must lie in the E_g plane, orthogonal to (1,1,1).
perp = abs(p @ np.ones(3)) / (np.linalg.norm(p))    # should be ~0
# E_g plane orthonormal basis (perp to (1,1,1)):
u1 = np.array([2, -1, -1], float); u1 /= np.linalg.norm(u1)
u2 = np.array([0,  1, -1], float); u2 -= (u2@u1)*u1; u2 /= np.linalg.norm(u2)
# angle of p in this plane = the GEOMETRIC E_g phase (a genuine radian, R=1):
a1, a2 = p @ u1, p @ u2
delta_geom = np.arctan2(a2, a1)
# fold into the C3 fundamental domain [0, 2pi/3) so 3*delta is the Landau phase
delta_geom_folded = delta_geom % (2*np.pi/3)

# Koide circulant delta (independent parametrization y_a=ybar(1+ r cos(d+2pi a/3))):
c_dev = s/ybar - 1.0
a = np.arange(3)
Cc = np.sum(c_dev*np.cos(2*np.pi*a/3)); Ss = np.sum(c_dev*np.sin(2*np.pi*a/3))
delta_koide = (np.arctan2(-Ss, Cc)) % (2*np.pi/3)
# fold into [0, pi/3] via the C3v reflection (delta and 2pi/3-delta are equivalent)
delta_koide = min(delta_koide, 2*np.pi/3 - delta_koide)
delta_geom_folded = min(delta_geom_folded, 2*np.pi/3 - delta_geom_folded)

# radial amplitude ratio r = A/ybar (F92 equipartition predicts sqrt2)
r_ratio = e_amp/ybar   # since e=|p|=A here (p_a = A cos(...), |p|=A*sqrt(3/2)?) -> check

R["A_generator_norm"] = {
    "p_perp_to_111 (should be ~0)": float(perp),
    "delta_geometric_rad": float(delta_geom_folded),
    "delta_koide_rad": float(delta_koide),
    "geom_equals_koide": bool(abs(delta_geom_folded - delta_koide) < 1e-9
                              or abs(delta_geom_folded - delta_koide) < 1e-6),
    "delta_vs_2_9_pct": float(abs(delta_koide - _delta_star_f)/(_delta_star_f)*100),
    "r_ratio_A_over_ybar": float(r_ratio),
    "verdict_a": ("delta is the literal arg of the E_g doublet in the deviation "
                  "simplex (p perp (1,1,1)) -> a GENUINE radian with NO free scale. "
                  "The F118 functional therefore FIXES the generator norm to R=1 "
                  "GEOMETRICALLY (not posited): POSIT-N part (a) is supplied by the solve."),
}
print("A  p.(111)=%.2e  delta_geom=%.6f  delta_koide=%.6f  2/9=%.6f  (%.3f%%)"
      % (perp, delta_geom_folded, delta_koide, _delta_star_f, abs(delta_koide-_delta_star_f)/(_delta_star_f)*100))

# Schur check: the E_g invariant metric is proportional to identity, so the
# E_g-plane angle is CANONICAL (a genuine radian) -- overall scale is the only
# freedom and it does not affect angles. Build the O rotation reps on the E_g
# doublet and average g = sum_R D(R)^T D(R); Schur => g proportional to I.
def eg_doublet_reps():
    # E_g basis (d_z2, d_x2-y2) evaluated -> use the 6 axis-site construction
    sites = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
    u = np.array([2*z*z-x*x-y*y for (x,y,z) in sites],float)
    w = np.array([x*x-y*y       for (x,y,z) in sites],float)
    u/=np.linalg.norm(u); w/=np.linalg.norm(w)
    gens = {
        "C3_111": lambda v:(v[2],v[0],v[1]),
        "C4_z":   lambda v:(-v[1],v[0],v[2]),
        "C2_x":   lambda v:(v[0],-v[1],-v[2]),
    }
    Ds=[]
    for f in gens.values():
        perm=[sites.index(f(v)) for v in sites]
        uP,wP=u[perm],w[perm]
        Ds.append(np.array([[uP@u,wP@u],[uP@w,wP@w]]))
    return Ds
Ds = eg_doublet_reps()
# average over the group generated is hard; instead test each generator is
# orthogonal (D^T D = I) -> the standard metric is already invariant (isotropic)
iso = max(np.max(np.abs(D.T@D - np.eye(2))) for D in Ds)
R["A_schur_isotropy"] = {
    "max|D^T D - I|": float(iso),
    "E_g_metric_isotropic": bool(iso < 1e-9),
    "note": ("E_g is a 2D irrep of O_h; by Schur its invariant bilinear is unique "
             "up to overall scale (here the generators act orthogonally, D^T D=I). "
             "Overall scale does not change angles => the E_g-plane phase delta is "
             "CANONICAL, a genuine radian. R=1 is FORCED by representation theory, "
             "not a free normalization (this upgrades F253's POSIT-N part (a))."),
}
print("A' Schur isotropy max|D^T D - I| = %.2e -> E_g angle is canonical (R=1 forced)" % iso)

# ---------------------------------------------------------------------------
# PART (b) -- does the solve fix the ANGLE = 2/9 without ASSUMING 2/9? (circularity)
# ---------------------------------------------------------------------------
B = _B_sea_cubic                       # derived cubic (F95)
# F234 back-solve: assume delta*=2/9 -> pin C, lambda6
delta_star = _delta_star_f
cos3d = np.cos(3*delta_star)      # = cos(2/3)
C_req = abs(B)/(2*cos3d)          # F234 C2
# e^6 at the saturation amplitude (F92/F118 e~0.733); back out from lambda6=0.243
lam6_F234 = _lambda_6
e6_implied = C_req/lam6_F234
e_implied = e6_implied**(1/6)

# Forward test: if lambda6 = 1/4 (the F115 rotor value g_s^2 chi), what delta?
def delta_from_lambda6(lam6, e6):
    C = lam6*e6
    x = -B/(2*C)
    if abs(x) > 1: return None
    return np.arccos(x)/3
d_quarter = delta_from_lambda6(0.25, e6_implied)
d_0243    = delta_from_lambda6(_lambda_6, e6_implied)

R["B_angle_identity_circular"] = {
    "cos3delta_at_2_9": float(cos3d),
    "C_req_from_assuming_2_9": float(C_req),         # 0.0362 (F118/F234)
    "e6_implied": float(e6_implied), "e_implied": float(e_implied),
    "delta_if_lambda6_eq_0.243": None if d_0243 is None else float(d_0243),
    "delta_if_lambda6_eq_1/4":   None if d_quarter is None else float(d_quarter),
    "lambda6_quarter_gives_2_9_pct":
        None if d_quarter is None else float(abs(d_quarter-_delta_star_f)/(_delta_star_f)*100),
    "verdict_b": ("cos3d*=-B/2C fixes delta ONLY given C (i.e. lambda6). F234 gets "
                  "lambda6=0.243 by ASSUMING delta*=2/9 -> using it to derive 2/9 is "
                  "CIRCULAR. The suggestive lambda6=1/4 (F115 rotor) gives delta~0.250, "
                  "a ~12.5% miss from 2/9, so 1/4 does NOT independently reproduce the "
                  "weight. POSIT-N part (b) is NOT supplied by the solve."),
}
print("B  C_req(assume 2/9)=%.4f  e_implied=%.4f  lambda6=1/4 -> delta=%.4f (%.1f%% off 2/9)"
      % (C_req, e_implied, d_quarter, abs(d_quarter-_delta_star_f)/(_delta_star_f)*100))

# Independent-lambda6 check: does F118 offer ANY lambda6 constraint not using 2/9?
# F118 B1/B2: sea-loop sextic is wrong-SIGN at saturation (anti-brake) and wrong
# SCALING at small amplitude -> the loop CANNOT source the positive brake C.
# So lambda6 is localized to an O(1) E_g clock coupling but its VALUE is un-pinned
# except through delta*.
R["B2_independent_lambda6"] = {
    "sea_loop_can_source_C": False,
    "reason": "F118 B1: C_loop(sat)=-0.018<0 (anti-brake); B2: C_loop~ybar^7 wrong scaling",
    "independent_value_of_lambda6": "none (only pinned via delta*=2/9, F234) -> circular",
}

# ---------------------------------------------------------------------------
# VERDICT
# ---------------------------------------------------------------------------
R["VERDICT"] = {
    "does_solve_fix_generator_norm_R": ("YES for the NORMALIZATION (R=1): the F118 "
        "angle delta is the genuine arg of the E_g doublet in the deviation simplex "
        "(p perp (1,1,1)), a true radian with no free scale. This REMOVES F253's "
        "'free R' escape hatch -- the weight->radian bridge is not a free normalization."),
    "does_solve_close_E1": ("NO. The remaining half of POSIT-N -- that this genuine "
        "radian EQUALS the weight 2/9 -- is set dynamically by cos3d*=-B/2C, i.e. by "
        "lambda6. F234 fixes lambda6 FROM 2/9 (circular); F118 B1/B2 show the sea loop "
        "cannot source it; lambda6=1/4 (rotor) misses by ~12.5%. So E1 does not close."),
    "net_refinement": ("E1's residual SHARPENS and MOVES: no longer 'a normalization "
        "(R) + an identity', but the SINGLE coupling lambda6 = C/e^6 = 0.243 -- the "
        "E_g sextic clock self-interaction. The generator-norm question is ANSWERED "
        "(R=1, geometric). E1 = 'derive lambda6=0.243 (~1/4) independently, or a reason "
        "the genuine dynamical E_g angle lands on the weight 2/9'."),
}

with open("../test-results/generator_norm_from_F118.json","w") as f:
    json.dump(R, f, indent=2, default=str)
print("\nwrote ../test-results/generator_norm_from_F118.json")
print("VERDICT:", R["VERDICT"]["net_refinement"])
