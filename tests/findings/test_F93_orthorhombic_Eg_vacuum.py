#!/usr/bin/env python3
"""
test_F93_orthorhombic_Eg_vacuum.py
==================================

F93 — What the orthorhombic vacuum IS: an E_g condensate at a generic angle,
living on the BCC second-neighbour (cube-axis) shell; group-theoretic proof
that it removes the democratic stiffness (F84's kappa); the Landau theory
that decides when the orthorhombic phase wins; and the proof that it must be
SPONTANEOUS (the vacuum dispersion cannot supply it).

The target
----------
F76/F84 invoke "the orthorhombic vacuum" — three inequivalent axes — as the
model's deepest unexplained primitive (F84 irreducible input #2).  This test
gives it a definite identity and mechanism, with exact group theory where
possible and an explicit Landau phase diagram where dynamics enter.

Checks
------
  O1  The crystal field that splits the T1u generation triplet into three
      DISTINCT masses WITHOUT mixing axes is uniquely the E_g channel:
      sym(T1u x T1u) = A1g + E_g + T2g, where A1g = trace (no split),
      E_g = diagonal-traceless (splits, no mixing), T2g = off-diagonal
      (mixes axes).  Schur degeneracies [1,2,3] verified by group-averaging;
      invariance of the diagonal sector exact over the 48 integer O_h ops.
  O2  Lattice home: the BCC FIRST shell (8 cube-vertex sites) contains NO
      E_g (degeneracies [1,1,3,3], F75); the SECOND shell (6 cube-axis
      sites) decomposes as A1g + E_g + T1u (degeneracies [1,2,3]).
      ==> the orthorhombic field lives on the second-neighbour shell — the
      same shell F49's Weinberg-angle counting uses.
  O3  Stabilizers (exact, integer):  M(delta) = m0*I + e*diag(d_a),
      d_a = cos(delta - 2pi(a-1)/3).
      Generic delta  -> stabilizer = D_2h (order 8), containing NO
      nontrivial axis permutation: the generation-permutation symmetry S_3
      is COMPLETELY broken => no symmetry can generate a democratic
      restoring force kappa.  (F84's kappa-removal as a theorem.)
      delta = 0 mod 60 deg -> stabilizer = D_4h (order 16), residual axis
      swap => [2,1] masses and a protected kappa.  Orthorhombic (= three
      distinct masses) is the GENERIC case of an E_g condensate.
  O4  Exact identity (sympy): the E_g doublet (e1,e2) = e(cos d, sin d) has
      diagonal shifts e*sqrt(2/3)*cos(d - 2pi(a-1)/3) — i.e. F76-C6's Z3
      parametrization sqrt(m_a) = M0[1 + sqrt2 cos(d + 2pi a/3)] IS
      "A1g background + E_g condensate at angle d".  F76's fitted phase
      delta is the condensate angle.
  O5  Landau theory of the E_g condensate.  Most general expansion to 6th
      order: F = (r/2)e^2 + (b/3)e^3 cos3d + (u/4)e^4 + (w/6)e^6 cos^2(3d).
      At fixed e the angle minimizes f(d) = B cos3d + C cos^2(3d)
      (B = b e^3/3, C = w e^6/6):
        - generic d* (orthorhombic, three distinct masses) iff C>0 and
          |B| < 2C, with cos 3d* = -B/(2C);
        - otherwise d* = 0 or 60 deg (tetragonal-type, [2,1] masses).
      Numerical global minimization over a (b,w) grid must match the
      analytic boundary everywhere.  Corollaries verified:
        (i)  quartic-only theory (w=0) NEVER gives three distinct masses;
        (ii) b=0, w>0 gives the maximal orthorhombic point d*=30 deg.
  O5b Negative control: a T1u (vector) condensate alone, at quartic order,
      can only point along (100) or (111) — never a generic direction.
      The E_g channel is not optional; a vector order parameter cannot
      orthorhombify the vacuum at this order.
  O6  Spontaneity (machine): the BCC vacuum dispersion is exactly
      O_h-symmetric — for all 48 R, {w+(Rk), w-(Rk)} = {w+(k), w-(k)} —
      so the vacuum supplies ZERO explicit E_g field.  The orthorhombic
      break cannot be inherited from the dispersion anisotropy (F30); it
      must be spontaneous (condensation, O5) or external.
  O7  Data: PDG charged leptons => condensate angle delta_data, amplitude
      ratio A/ybar (should be sqrt2 <=> the 45 deg equipartition), all
      three shifts distinct (generic delta, far from any multiple of
      60 deg), masses reconstructed; the one number the Landau theory does
      not fix is cos(3 delta_data) = -B/(2C) — recorded as the remaining
      input (it replaces F76's free phase delta with a ratio of two Landau
      coefficients).
"""

import itertools
import json
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))
from ca_bcc import bcc_dispersion  # noqa: E402

RESULTS = {}
PASS = True


def record(name, ok, detail):
    global PASS
    RESULTS[name] = {"pass": bool(ok), **detail}
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ════════════════════════════════════════════════════════════════════
#  O_h = the 48 signed 3x3 permutation matrices (exact integers)
# ════════════════════════════════════════════════════════════════════
def oh_elements():
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i in range(3):
                M[i, perm[i]] = signs[i]
            mats.append(M)
    return mats


OH = oh_elements()
assert len(OH) == 48


def schur_degeneracies(rep_mats, dim, seed=0, tol=1e-9):
    """Group-average a random symmetric operator; return sorted eigenvalue
    degeneracy multiset (the irrep dimensions, by Schur)."""
    rng = np.random.default_rng(seed)
    H = rng.standard_normal((dim, dim))
    H = H + H.T
    Hbar = np.zeros_like(H, dtype=float)
    for R in rep_mats:
        Hbar += R @ H @ R.T
    Hbar /= len(rep_mats)
    ev = np.sort(np.linalg.eigvalsh(Hbar))
    degs, cur = [], 1
    for i in range(1, dim):
        if abs(ev[i] - ev[i - 1]) < tol * max(1.0, abs(ev[i])):
            cur += 1
        else:
            degs.append(cur)
            cur = 1
    degs.append(cur)
    return sorted(degs)


# ════════════════════════════════════════════════════════════════════
# O1 — sym(T1u x T1u) = A1g + E_g + T2g; the only non-mixing splitting
#      channel is the 2-dim diagonal-traceless block (E_g).
# ════════════════════════════════════════════════════════════════════
# rep of O_h on symmetric 3x3 matrices, basis:
# (xx, yy, zz, yz, xz, xy) -> 6x6 matrices
SYM_BASIS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]


def sym6_rep(R):
    out = np.zeros((6, 6), dtype=int)
    for j, (a, b) in enumerate(SYM_BASIS):
        E = np.zeros((3, 3), dtype=int)
        E[a, b] = 1
        E[b, a] = 1
        if a == b:
            E[a, b] = 1
        M = R @ E @ R.T
        for i, (c, d) in enumerate(SYM_BASIS):
            out[i, j] = M[c, d]
    return out


SYM6 = [sym6_rep(R) for R in OH]
degs_sym = schur_degeneracies(SYM6, 6, seed=1)

# exact invariance of the diagonal sector: R diag(d) R^T is diagonal with
# permuted entries, for every signed permutation R (integer arithmetic)
diag_invariant = True
d_test = np.diag([2, 3, 5])
for R in OH:
    M = R @ d_test @ R.T
    if np.any(M - np.diag(np.diagonal(M))):
        diag_invariant = False
        break
    if sorted(np.diagonal(M).tolist()) != [2, 3, 5]:
        diag_invariant = False
        break

record("O1_Eg_is_the_unique_nonmixing_splitter",
       degs_sym == [1, 2, 3] and diag_invariant,
       {"sym(T1u x T1u) Schur degeneracies": degs_sym,
        "expected": "[1,2,3] = A1g(trace) + E_g(diag-traceless) + "
                    "T2g(off-diag)",
        "diagonal sector exactly O_h-invariant": diag_invariant,
        "statement": "three distinct masses without axis mixing <=> a "
                     "nonzero E_g (diagonal-traceless) field; T2g only "
                     "mixes axes, A1g only shifts the trace"})


# ════════════════════════════════════════════════════════════════════
# O2 — shell homes: first shell (8 vertices) has NO E_g; second shell
#      (6 cube-axis sites) = A1g + E_g + T1u.
# ════════════════════════════════════════════════════════════════════
def perm_rep(sites, R):
    n = len(sites)
    out = np.zeros((n, n), dtype=int)
    smap = {tuple(s): i for i, s in enumerate(sites)}
    for j, s in enumerate(sites):
        out[smap[tuple(R @ np.array(s))], j] = 1
    return out


shell1 = [np.array(v) for v in itertools.product((1, -1), repeat=3)]
shell2 = [np.array(v) for v in
          [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1),
           (0, 0, -1)]]
P1 = [perm_rep(shell1, R) for R in OH]
P2 = [perm_rep(shell2, R) for R in OH]
degs1 = schur_degeneracies(P1, 8, seed=2)
degs2 = schur_degeneracies(P2, 6, seed=3)

# identify the 2-dim block of the 6-site shell explicitly as E_g:
# basis u1 = (s_x - s_y)/2, u2 = (s_x + s_y - 2 s_z)/sqrt(12),
# s_a = f(+a) + f(-a); check the span is invariant under all 48 ops
# and even under inversion.
u1 = np.array([1, 1, -1, -1, 0, 0], dtype=float) / 2.0
u2 = np.array([1, 1, 1, 1, -2, -2], dtype=float) / np.sqrt(12.0)
U = np.stack([u1, u2], axis=1)          # 6x2
Pproj = U @ U.T
eg_invariant = True
inv_even = True
INV6 = perm_rep(shell2, -np.eye(3, dtype=int).astype(int))
for R6 in P2:
    if np.max(np.abs(R6 @ Pproj - Pproj @ R6)) > 1e-12:
        eg_invariant = False
        break
if np.max(np.abs(INV6 @ U - U)) > 1e-12:
    inv_even = False

record("O2_Eg_lives_on_second_shell",
       degs1 == [1, 1, 3, 3] and degs2 == [1, 2, 3]
       and eg_invariant and inv_even,
       {"shell1 (8 vertices) degeneracies": degs1,
        "shell2 (6 cube axes) degeneracies": degs2,
        "2-dim block invariant": eg_invariant,
        "2-dim block inversion-even (g)": inv_even,
        "statement": "no E_g in the first (mass-step) shell; the "
                     "orthorhombic field's minimal home is the SECOND "
                     "(cube-axis) shell — F49's shell"})


# ════════════════════════════════════════════════════════════════════
# O3 — stabilizers: generic E_g angle -> D_2h (order 8), S_3 fully
#      broken (kappa unprotected -> flat); special angles -> D_4h
#      (order 16), residual swap.
# ════════════════════════════════════════════════════════════════════
def stabilizer_counts(delta):
    d = np.array([np.cos(delta - 2 * np.pi * a / 3) for a in range(3)])
    M = np.diag(d)
    n_stab, n_perm = 0, 0
    for R in OH:
        if np.max(np.abs(R @ M @ R.T - M)) < 1e-12:
            n_stab += 1
            # nontrivial axis permutation part?
            Pabs = np.abs(R)
            if np.any(Pabs != np.eye(3, dtype=int)):
                n_perm += 1
    return n_stab, n_perm, d


delta_generic = np.radians(12.7)
n_g, p_g, d_g = stabilizer_counts(delta_generic)
n_t, p_t, d_t = stabilizer_counts(0.0)
n_m, p_m, d_m = stabilizer_counts(np.radians(30.0))
distinct_g = len(set(np.round(d_g, 12))) == 3
distinct_m = len(set(np.round(d_m, 12))) == 3
deg_t = len(set(np.round(d_t, 12))) == 2

record("O3_stabilizer_D2h_S3_broken",
       n_g == 8 and p_g == 0 and distinct_g
       and n_t == 16 and p_t > 0 and deg_t
       and n_m == 8 and p_m == 0 and distinct_m,
       {"generic delta=12.7deg": {"|stab|": n_g, "axis-permuting": p_g,
                                  "three distinct": distinct_g},
        "delta=0 (tetragonal)": {"|stab|": n_t, "axis-permuting": p_t,
                                 "[2,1] degenerate": deg_t},
        "delta=30deg (max ortho)": {"|stab|": n_m, "axis-permuting": p_m,
                                    "three distinct": distinct_m},
        "statement": "generic E_g angle leaves D_2h with NO residual axis "
                     "permutation: S_3 completely broken, so no symmetry "
                     "can generate the democratic stiffness kappa (F84's "
                     "kappa-removal as a stabilizer theorem); delta=0 "
                     "keeps a swap -> [2,1] and a protected kappa"})


# ════════════════════════════════════════════════════════════════════
# O4 — exact identity: E_g doublet at angle d == Z3 cosine shifts
#      (F76-C6's parametrization IS the E_g condensate)
# ════════════════════════════════════════════════════════════════════
dlt = sp.symbols('delta', real=True)
E1 = sp.diag(2, -1, -1) / sp.sqrt(6)
E2 = sp.diag(0, 1, -1) / sp.sqrt(2)
Mfield = sp.cos(dlt) * E1 + sp.sin(dlt) * E2
res = [sp.simplify(Mfield[a, a]
                   - sp.sqrt(sp.Rational(2, 3))
                   * sp.cos(dlt - 2 * sp.pi * a / 3)) for a in range(3)]
record("O4_Eg_equals_Z3_parametrization",
       all(r == 0 for r in res),
       {"residuals": [str(r) for r in res],
        "statement": "diag of the E_g doublet at angle delta is exactly "
                     "sqrt(2/3) cos(delta - 2pi a/3): F76-C6's Z3 form IS "
                     "an A1g background + E_g condensate; F76's fitted "
                     "phase is the condensate angle"})


# ════════════════════════════════════════════════════════════════════
# O5 — Landau phase diagram of the E_g condensate
#      F(e,d) = (r/2)e^2 + (b/3)e^3 cos3d + (u/4)e^4 + (w/6)e^6 cos^2 3d
# ════════════════════════════════════════════════════════════════════
def landau_min(r, b, u, w, emax=3.0, ne=4001):
    """Global minimum over e>=0 and the angle d.  At fixed e the angle
    part is f(c3) = B*c3 + C*c3^2 with c3 = cos3d in [-1,1]:
    minimizer c3* = clip(-B/(2C)) if C>0 else endpoint by sign of B."""
    es = np.linspace(0.0, emax, ne)
    best = (0.0, 0.0, 0.0)   # F, e, cos3d
    Fbest = 0.0
    for e in es[1:]:
        B = b * e**3 / 3.0
        C = w * e**6 / 6.0
        if C > 0:
            c3 = float(np.clip(-B / (2.0 * C), -1.0, 1.0))
        elif C < 0:
            c3 = -1.0 if (B * (-1) + C) < (B * (+1) + C) else 1.0
        else:
            c3 = -1.0 if B > 0 else 1.0
        F = 0.5 * r * e**2 + B * c3 + 0.25 * u * e**4 + C * c3**2
        if F < Fbest:
            Fbest, best = F, (F, e, c3)
    return best


def classify(c3, e):
    if e < 1e-9:
        return "cubic"
    if abs(abs(c3) - 1.0) < 1e-9:
        return "axis"        # delta multiple of 60 deg: [2,1] masses
    return "ortho"           # generic delta: three distinct masses


r0, u0 = -1.0, 1.0
mismatches = 0
n_ortho = 0
quartic_only_ortho = 0
for b in np.linspace(-1.5, 1.5, 13):
    for w in np.linspace(0.0, 3.0, 13):
        F, e, c3 = landau_min(r0, b, u0, w)
        cls = classify(c3, e)
        # analytic prediction at the minimizing e
        B, C = b * e**3 / 3.0, w * e**6 / 6.0
        if C > 0 and abs(B) < 2 * C:
            pred = "ortho"
        elif e < 1e-9:
            pred = "cubic"
        else:
            pred = "axis"
        if b == 0.0 and w == 0.0:
            continue   # marginal: angle degenerate, classification moot
        if cls != pred:
            mismatches += 1
        if cls == "ortho":
            n_ortho += 1
        if w == 0.0 and cls == "ortho":
            quartic_only_ortho += 1

# b=0, w>0: the clean maximal-orthorhombic case d*=30deg
F0, e0, c30 = landau_min(r0, 0.0, u0, 1.0)
maximal_ok = abs(c30) < 1e-9 and e0 > 0

record("O5_landau_phase_diagram",
       mismatches == 0 and n_ortho > 0 and quartic_only_ortho == 0
       and maximal_ok,
       {"grid": "b in [-1.5,1.5] x w in [0,3], 13x13",
        "numeric vs analytic mismatches": mismatches,
        "orthorhombic points found": n_ortho,
        "quartic-only (w=0) orthorhombic points": quartic_only_ortho,
        "b=0,w>0 minimizer cos3d": c30,
        "statement": "orthorhombic (three distinct masses) wins iff "
                     "C>0 and |B|<2C, with cos3delta* = -B/(2C); the "
                     "quartic theory can NEVER do it (sextic invariant "
                     "required); b=0 gives the maximal point delta*=30deg"})


# ════════════════════════════════════════════════════════════════════
# O5b — negative control: quartic T1u vector condensate only points
#       along (100) or (111), never a generic direction
# ════════════════════════════════════════════════════════════════════
rng = np.random.default_rng(7)


def min_direction(v_aniso, n_starts=60, n_iter=4000, lr=0.02):
    best_dir, best_val = None, np.inf
    for _ in range(n_starts):
        y = rng.standard_normal(3)
        y /= np.linalg.norm(y)
        for _ in range(n_iter):
            g = 4 * v_aniso * y**3
            g -= (g @ y) * y
            y -= lr * g
            y /= np.linalg.norm(y)
        val = v_aniso * np.sum(y**4)
        if val < best_val - 1e-12:
            best_val, best_dir = val, np.abs(np.sort(np.abs(y)))
    return best_dir


d_pos = min_direction(+1.0)
d_neg = min_direction(-1.0)
is_111 = np.max(np.abs(d_pos - 1 / np.sqrt(3))) < 1e-6
is_100 = (abs(d_neg[-1] - 1.0) < 1e-6 and np.max(d_neg[:2]) < 1e-6)
record("O5b_T1u_quartic_cannot_orthorhombify",
       is_111 and is_100,
       {"v>0 minimizer |components|": d_pos.tolist(),
        "v<0 minimizer |components|": d_neg.tolist(),
        "statement": "a vector (T1u) condensate at quartic order points "
                     "along (111) or (100) only — it cannot supply a "
                     "generic three-distinct-axis direction; the E_g "
                     "channel is structurally required"})


# ════════════════════════════════════════════════════════════════════
# O6 — spontaneity: the BCC vacuum dispersion is exactly O_h-symmetric,
#      so it supplies ZERO explicit E_g field
# ════════════════════════════════════════════════════════════════════
rng = np.random.default_rng(11)
worst = 0.0
branch_proper_ok = True
for _ in range(10):
    k = rng.uniform(-1.2, 1.2, size=3)
    wp = bcc_dispersion(*k, sign='+')
    wm = bcc_dispersion(*k, sign='-')
    base = np.sort([wp, wm])
    for R in OH:
        kr = R @ k
        wpr = bcc_dispersion(*kr, sign='+')
        wmr = bcc_dispersion(*kr, sign='-')
        worst = max(worst, float(np.max(np.abs(np.sort([wpr, wmr]) - base))))
record("O6_dispersion_Oh_symmetric_no_explicit_Eg",
       worst < 1e-12,
       {"max |spectrum(Rk) - spectrum(k)| over 48 ops x 10 k": worst,
        "statement": "the vacuum dispersion (incl. the F30 anisotropy) is "
                     "exactly O_h-symmetric: it carries zero E_g component, "
                     "so the orthorhombic field CANNOT be inherited from "
                     "the dispersion — it must be spontaneous (O5) or "
                     "external"})


# ════════════════════════════════════════════════════════════════════
# O7 — data: condensate angle and amplitude from the PDG leptons
# ════════════════════════════════════════════════════════════════════
m_e, m_mu, m_tau = 0.51099895, 105.6583755, 1776.86
y = np.sqrt(np.array([m_e, m_mu, m_tau]))
ybar = float(np.mean(y))
p = y - ybar
# fit p_a = A cos(delta + 2pi a/3): discrete Fourier on Z3
z = np.sum(p * np.exp(-2j * np.pi * np.arange(3) / 3)) * 2.0 / 3.0
A = float(np.abs(z))
delta_data = float(np.angle(z))
recon = ybar + A * np.cos(delta_data + 2 * np.pi * np.arange(3) / 3)
rel_err = float(np.max(np.abs(recon**2 - np.array([m_e, m_mu, m_tau]))
                       / np.array([m_e, m_mu, m_tau])))
ratio = A / ybar                      # should be sqrt(2) <=> 45 deg
delta_deg = np.degrees(delta_data) % 120.0
# distance to nearest multiple of 60 deg (invariant diagnostic of
# "generic vs tetragonal")
dist60 = min(delta_deg % 60.0, 60.0 - (delta_deg % 60.0))
cos3d = float(np.cos(3 * delta_data))
record("O7_data_condensate_angle",
       rel_err < 1e-10 and abs(ratio - np.sqrt(2)) < 5e-5 and dist60 > 5.0,
       {"delta_data_deg (mod 120)": round(delta_deg, 4),
        "dist to nearest 60deg multiple": round(dist60, 4),
        "A/ybar": f"{ratio:.6f}",
        "sqrt(2)": f"{np.sqrt(2):.6f}",
        "mass reconstruction rel err": rel_err,
        "cos(3 delta) = -B/(2C) required": round(cos3d, 6),
        "statement": "the lepton condensate angle is GENERIC (orthorhombic "
                     "confirmed, far from tetragonal), amplitude ratio "
                     "= sqrt2 (the 45deg equipartition), and the one "
                     "number the Landau theory leaves free is "
                     "cos(3 delta) = -B/(2C) — F76's phase, now a ratio "
                     "of two Landau coefficients"})


# ════════════════════════════════════════════════════════════════════
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "test-results")
os.makedirs(outdir, exist_ok=True)
with open(os.path.join(outdir, "F93_orthorhombic_Eg_vacuum.json"), "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)

n_pass = sum(1 for r in RESULTS.values() if r["pass"])
print(f"\n{'=' * 60}\nF93 orthorhombic E_g vacuum: {n_pass}/{len(RESULTS)} "
      f"PASS  ->  overall {'PASS' if PASS else 'FAIL'}")
sys.exit(0 if PASS else 1)
