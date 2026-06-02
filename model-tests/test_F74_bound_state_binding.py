#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_F74_bound_state_binding.py
===============================

F74 — Dynamical two-constituent bound state: the binding depth that F73 left
as the one missing input.

F73 proved the spin-0 bound pair's *kinematics* exactly (m_H = sin(asin m1 +
asin m2) -> 2 m_c sqrt(1-m_c^2)), but the *mass value* needs the binding
dynamics. This script builds a real two-body bound-state solver and produces
the binding depth E_b as an explicit function of the interaction strength.

MODEL
-----
Rest-frame (total momentum zero) two-body problem -> one-body problem in the
relative coordinate on a 3D cubic lattice, reduced mass mu = m_c/2, hopping t,
plus the minimal attractive channel: a single-site contact well of depth g (the
lattice realisation of the NJL / BCS "Cooper" contact that pairs two spin-1/2
constituents into a spin-0 singlet).

    H_rel = -t sum_<ij> |i><j|  -  g |0><0|              (band bottom shifted to 0)
    eps(k) = 2t sum_i (1 - cos k_i),   eps in [0, 12t]

The contact is rank-1, so the bound state below the band is the EXACT root of
the secular (Koster-Slater) equation

    1 = g * < 1 / (eps(k) + E_b) >_BZ ,     E_b > 0  (binding energy)        (*)

and the binding ONSET is the 3D critical coupling

    g_c = 1 / < 1/eps(k) >_BZ                                                (**)

which is FINITE in 3D (the Watson integral) -> a genuine minimum strength to
bind, unlike 1D/2D. We:

  A. compute g_c by BZ quadrature and check it against the Watson constant;
  B. solve (*) for E_b(g) over a range g > g_c;
  C. cross-check E_b on a finite lattice TWO independent ways
     (secular root vs full dense diagonalisation) -> machine precision;
  D. map the depth to the composite mass M = 2 m_c - E_b and show M -> 2 m_c at
     threshold (dynamically recovering the F73 ceiling);
  E. estimate the gauge-exchange (positronium-like) binding the model's own
     sector actually supplies, and state the honest verdict.

All arithmetic here is REAL (lattice tight-binding + real symmetric eigenvalue
problem); no chiral/complex transforms, so the CLAUDE.md numpy caveat does not
bite. numpy only (no scipy dependency).

Run:  python3 model-tests/test_F74_bound_state_binding.py     (~a few seconds)
Writes test-results/F74_bound_state_binding.json.
"""

import os
import json
import numpy as np

results = {"finding": "F74", "title": "two-constituent bound-state binding depth",
           "checks": {}, "derived": {}, "curve": {}, "confrontation": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                               "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:44s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 76)
print("F74 — dynamical two-constituent bound state: binding depth E_b(g)")
print("=" * 76)

t = 1.0  # set the hopping as the energy unit

# ---------------------------------------------------------------------------
# A. Critical coupling g_c (binding onset) by BZ quadrature, vs Watson.
#    Watson:  W3 = (1/(2pi)^3) \int_BZ d^3k / [ sum_i (1 - cos k_i) ] = 0.5054620...
#    With eps = 2t sum(1-cos k_i):  <1/eps> = W3 / (2t);  g_c = 1/<1/eps> = 2t / W3.
# ---------------------------------------------------------------------------
print("\nA  critical coupling g_c (3D binding onset) vs Watson integral")
WATSON3 = 0.5054620197   # standard simple-cubic Watson integral

def bz_average(func, n=64):
    """Midpoint BZ average of func(eps_grid); midpoint rule skips the k=0 node."""
    idx = (np.arange(n) + 0.5) * 2.0 * np.pi / n          # midpoints in [0,2pi)
    cx = np.cos(idx)
    # eps = 2t * (3 - cos kx - cos ky - cos kz); separable accumulation
    s = cx[:, None, None] + cx[None, :, None] + cx[None, None, :]
    eps = 2.0 * t * (3.0 - s)
    return np.mean(func(eps))

# The 1/eps singularity at k=0 makes a single uniform grid converge only as
# O(1/n); a two-grid Richardson 1/n extrapolation removes the leading error.
_a1 = bz_average(lambda e: 1.0 / e, n=128)
_a2 = bz_average(lambda e: 1.0 / e, n=256)
inv_eps_avg = (256.0 * _a2 - 128.0 * _a1) / (256.0 - 128.0)   # 1/n extrapolation
g_c = 1.0 / inv_eps_avg
g_c_watson = 2.0 * t / WATSON3
rel = abs(g_c - g_c_watson) / g_c_watson
results["derived"]["g_c"] = g_c
results["derived"]["g_c_watson"] = g_c_watson
print(f"       <1/eps> quadrature = {inv_eps_avg:.6f} / t   -> g_c = {g_c:.5f} t")
print(f"       Watson prediction  g_c = 2t/W3 = {g_c_watson:.5f} t")
record("A  g_c matches Watson integral", rel, 1e-4, "quantitative", rel < 1e-4)

# ---------------------------------------------------------------------------
# B. Binding-depth curve E_b(g) in the thermodynamic limit (secular root).
# ---------------------------------------------------------------------------
print("\nB  binding depth E_b(g) from the secular equation (thermodynamic limit)")

# precompute a fine eps grid once
_n = 80
_idx = (np.arange(_n) + 0.5) * 2.0 * np.pi / _n
_c = np.cos(_idx)
_S = _c[:, None, None] + _c[None, :, None] + _c[None, None, :]
EPS = (2.0 * t * (3.0 - _S)).ravel()

def secular_lhs(E_b, g):
    return g * np.mean(1.0 / (EPS + E_b)) - 1.0

def solve_Eb(g, lo=1e-9, hi=1e6):
    # f(E_b) = g<1/(eps+E_b)> - 1 ; decreasing in E_b. Root if g>g_c.
    if secular_lhs(lo, g) <= 0:
        return 0.0  # no bound state (g <= g_c)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if secular_lhs(mid, g) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

gammas = [1.0, 1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0]   # g / g_c
curve = []
for gam in gammas:
    g = gam * g_c
    Eb = solve_Eb(g)
    curve.append((gam, g, Eb, Eb / t))
    print(f"       g/g_c = {gam:5.2f}   g = {g:6.3f} t   E_b = {Eb:9.4f} t")
results["curve"]["columns"] = ["g_over_gc", "g_in_t", "E_b_in_t"]
results["curve"]["rows"] = [[r[0], r[1], r[2]] for r in curve]

# monotonic increasing, and E_b -> 0 as gamma -> 1+
mono = all(curve[i][2] < curve[i + 1][2] for i in range(len(curve) - 1))
Eb_at_threshold = curve[0][2]
record("B1 E_b increases monotonically with g", 0.0 if mono else 1.0, 0.5,
       "quantitative", mono)
record("B2 E_b -> 0 at threshold g=g_c", Eb_at_threshold, 1e-3,
       "quantitative", Eb_at_threshold < 1e-3)

# ---------------------------------------------------------------------------
# C. Finite-lattice cross-check: secular root vs full dense diagonalisation.
#    Same operator, two computational routes -> must agree to round-off.
# ---------------------------------------------------------------------------
print("\nC  finite-lattice cross-check: secular root vs dense eigh (L=12)")
L = 12
g_test = 8.0 * t   # comfortably above g_c

# finite k-grid eps (periodic, includes k=0 with eps=0)
kk = 2.0 * np.pi * np.arange(L) / L
ck = np.cos(kk)
Sf = ck[:, None, None] + ck[None, :, None] + ck[None, None, :]
eps_f = (2.0 * t * (3.0 - Sf)).ravel()    # length L^3, contains a 0 at k=0

# (1) secular root on the finite grid:  1 = (g/N) sum_k 1/(eps_k + E_b)
def secular_finite(E_b):
    return g_test * np.mean(1.0 / (eps_f + E_b)) - 1.0
lo, hi = 1e-9, 1e6
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if secular_finite(mid) > 0:
        lo = mid
    else:
        hi = mid
Eb_secular = 0.5 * (lo + hi)
E0_secular = -Eb_secular

# (2) dense real-space Hamiltonian on L^3, lowest eigenvalue
N = L ** 3
def site(x, y, z):
    return (x % L) * L * L + (y % L) * L + (z % L)
H = np.zeros((N, N))
for x in range(L):
    for y in range(L):
        for z in range(L):
            i = site(x, y, z)
            H[i, i] += 6.0 * t                  # band-bottom shift: eps in [0,12t]
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                               (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                H[i, site(x + dx, y + dy, z + dz)] += -t
H[site(0, 0, 0), site(0, 0, 0)] += -g_test       # contact well at origin
evals = np.linalg.eigvalsh(H)
E0_dense = evals[0]

diff = abs(E0_dense - E0_secular)
results["derived"]["E0_dense_L12"] = float(E0_dense)
results["derived"]["E0_secular_L12"] = float(E0_secular)
print(f"       dense eigh  E0 = {E0_dense:.10f} t")
print(f"       secular     E0 = {E0_secular:.10f} t")
record("C  dense diag == secular root (L=12)", diff, 1e-9,
       "machine", diff < 1e-9)

# ---------------------------------------------------------------------------
# D. Map to composite mass and recover the F73 ceiling at threshold.
#    M = 2 m_c - E_b ;  binding fraction beta = E_b / (2 m_c).
#    The lattice <-> rest-mass link (F46): m_lat = m_c c a / hbar, and the NR
#    hopping is t = hbar^2 / (m_c a^2) so t/(m_c c^2) = 1/m_lat^2. Hence
#        beta = E_b/(2 m_c c^2) = (E_b/t) * m_lat^2 / 2.
#    A PHYSICAL bound state needs 0 < beta < 1.
# ---------------------------------------------------------------------------
print("\nD  composite mass M = 2 m_c - E_b, and the F73 ceiling at threshold")
# at threshold beta = 0 -> M = 2 m_c (F73). report beta(gamma) for a sample m_lat.
m_lat_sample = 3.935e-17    # EW-scale constituent at a = 6.2e-35 m (from F73)
betas = [(gam, (Eb_t) * m_lat_sample ** 2 / 2.0) for (gam, _, _, Eb_t) in curve]
results["derived"]["m_lat_sample"] = m_lat_sample
print(f"       at threshold (g->g_c): E_b->0  =>  M -> 2 m_c   (F73 ceiling recovered)")
print(f"       beta = E_b/(2 m_c) for m_lat={m_lat_sample:.2e}:")
for gam, b in betas:
    print(f"          g/g_c={gam:5.2f}  ->  beta = {b:.3e}")
# the window 0<beta<1 (physical, sub-threshold binding) is parametrically narrow:
# beta=O(1) needs E_b/t = O(1/m_lat^2) i.e. gamma tuned to ~ m_lat^2 above 1.
tuning = m_lat_sample ** 2
results["derived"]["criticality_tuning_for_physical_binding"] = tuning
record("D  ceiling M=2m_c recovered at threshold", Eb_at_threshold, 1e-3,
       "quantitative", Eb_at_threshold < 1e-3)

# ---------------------------------------------------------------------------
# E. Confrontation + gauge-binding estimate + verdict.
# ---------------------------------------------------------------------------
print("\nE  confrontation with 125.25 GeV and the model's own binding strength")
M_H = 125.25
M_T = 172.57
ALPHA = 1.0 / 137.036
# required binding fraction for a t-tbar composite:
beta_required_ttbar = 1.0 - M_H / (2.0 * M_T)
# gauge (positronium-like) binding the model actually supplies: E_b ~ alpha^2 m_c/4
beta_gauge = ALPHA ** 2 / 8.0   # E_b/(2 m_c) = (alpha^2 m_c/4)/(2 m_c) = alpha^2/8
results["confrontation"] = {
    "beta_required_ttbar": beta_required_ttbar,
    "beta_from_gauge_exchange": beta_gauge,
    "shortfall_factor": beta_required_ttbar / beta_gauge,
}
print(f"       required for 125 GeV from t-tbar:  beta = {beta_required_ttbar:.3f}")
print(f"       supplied by gauge exchange (~a^2): beta = {beta_gauge:.3e}")
print(f"       shortfall: gauge binding is {beta_required_ttbar/beta_gauge:.2e}x too weak")
record("E  gauge binding << required (ceiling robust)",
       beta_gauge, beta_required_ttbar, "quantitative", beta_gauge < beta_required_ttbar)

results["notes"] = [
    "RIGOROUS CORE: a 3D lattice contact attraction has a finite binding threshold g_c=3.957t (=2t/Watson); below it NO bound state. Verified vs Watson and by dense-vs-secular agreement to <1e-9.",
    "Binding depth E_b(g) rises continuously from 0 at g_c; at threshold the composite sits at M=2m_c, dynamically reproducing the F73 kinematic ceiling.",
    "INTERPRETATION (flagged): with the Planck-scale cell (F46 mapping), a PHYSICAL sub-threshold binding (0<beta<1) needs the coupling tuned to within ~m_lat^2 of critical -- the hierarchy problem surfacing in the model's language; the binding scale is UV-sensitive.",
    "The model's own gauge sector binds only at beta~alpha^2/8~7e-6 -- ~1e5 too weak to deform M from 2m_c. So a naturally-bound pair stays at the ceiling.",
    "VERDICT: the binding machinery is built and E_b(g) produced; the derivation is complete UP TO one external number -- the contact coupling -- which the model's gauge sector does not supply. 125 GeV requires either criticality fine-tuning or strong new contact dynamics + a relativistic deep-binding (Bethe-Salpeter) treatment, which is the precise remaining gap.",
    "SCOPE: the NR contact solver is quantitative near threshold (beta<<1); the deep-binding regime (beta~0.6 for t-tbar) is relativistic and beyond NR validity -- flagged as the next build.",
]

# ---------------------------------------------------------------------------
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "F74_bound_state_binding.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 76)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 76)
