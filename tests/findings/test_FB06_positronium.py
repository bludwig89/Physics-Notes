#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_FB06_positronium.py
========================

FB06 — Positronium levels are exactly half hydrogen.

Tier-B falsification: certifies the two-body -> relative-coordinate reduction
that underpins FB04/FB05 (and F125 §A).  The e+e- problem reduces, in the
relative coordinate, to the SAME attractive-1/r radial solver used for hydrogen
(FB04 / F125 / ca_atom.py), but with reduced mass mu = m_e/2.

Because the physical Rydberg scales linearly with the reduced mass,
    Ry = (1/2) mu c^2 (Z alpha)^2   =>   Ry(Ps)/Ry(H_inf) = (m_e/2)/m_e = 1/2,
every positronium level must be EXACTLY half the infinite-mass hydrogen value.
The dimensionless radial solver supplies the shared -1/n^2 eigenvalues; they
cancel in the ratio, so the 0.5 identity is analytic (machine precision), while
the -1/n^2 series itself is a grid-floor prediction.

Engine reuse: src/casim/engine/particles/atom.py  (the FB04/F125 1/r radial Coulomb
solver).  All arithmetic is REAL — the eigenproblem is a real symmetric
tridiagonal matrix (scipy.linalg.eigh_tridiagonal); no complex/chiral
transforms are involved, so the numpy/scipy CLAUDE.md caveat does not bite.
We additionally cross-check the scipy eigen-solve against a hand-rolled
real-arithmetic inverse-iteration / Sturm-bisection ground-state solve.

Gate (FB06):
  PASS if  Ry(Ps)/Ry(H_inf) = 1/2 to 1e-9,  ground state -6.803 eV,
           clean -1/n^2 series.
  FALSIFIED if the ratio departs from 1/2 beyond machine precision, or the
           -1/n^2 series fails.

Run:  python3 tests/findings/test_FB06_positronium.py
Writes test-results/FB06_positronium.json.
"""

import os
import sys
import json
import numpy as np

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))
from casim.engine.particles import atom as atom  # noqa: E402

N_GRID = 6000
PS_GROUND_MEASURED_EV = -6.8028   # 1/4 Ry_inf, the equal-mass reduction (measured ~ -6.8 eV)

print("=" * 84)
print("FB06 — positronium = exactly half of hydrogen (two-body 1/r reduction, mu=m_e/2)")
print("=" * 84)

checks = []
PASS = True


def record(name, value, target, tier, ok):
    global PASS
    checks.append({"name": name, "value": float(value), "target": float(target),
                   "tier": tier, "status": "PASS" if ok else "FAIL"})
    PASS = PASS and bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:50s} val={float(value):.3e}  "
          f"(target {float(target):.0e}, {tier})")


# ---------------------------------------------------------------------------
# Masses.  Infinite-nucleus hydrogen reference uses mu = m_e; positronium mu=m_e/2.
# ---------------------------------------------------------------------------
mu_e = atom.M_E_MEV
mu_Ps = atom.M_E_MEV / 2.0
print(f"   m_e c^2 = {atom.M_E_MEV} MeV (model P0 anchor),  alpha = {atom.ALPHA:.9f} (EM coupling)")
print(f"   mu(H_inf) = {mu_e:.6f} MeV   mu(Ps) = {mu_Ps:.6f} MeV")

# ---------------------------------------------------------------------------
# 1.  The Ry(Ps)/Ry(H_inf) = 1/2 identity, from the SAME 1/r solver.
# ---------------------------------------------------------------------------
Ps = atom.hydrogen_spectrum(n_max=5, mu_MeV=mu_Ps, N=N_GRID)
H_inf = atom.hydrogen_spectrum(n_max=5, mu_MeV=mu_e, N=N_GRID)

ry_ratio = Ps["Ry_eV"] / H_inf["Ry_eV"]
dev_half = abs(ry_ratio - 0.5)
print(f"\n   Ry(Ps)    = {Ps['Ry_eV']:.9f} eV")
print(f"   Ry(H_inf) = {H_inf['Ry_eV']:.9f} eV")
print(f"   ratio     = {ry_ratio:.12f}   |ratio - 1/2| = {dev_half:.3e}")
record("Ry(Ps)/Ry(H_inf) = 1/2", dev_half, 1e-9, "machine", dev_half < 1e-9)

# ---------------------------------------------------------------------------
# 2.  Positronium ground state ~ -6.803 eV.
#     (= -1/4 * Ry_inf in the equal-mass reduction.)
# ---------------------------------------------------------------------------
ps_ground = Ps["levels"][(1, 0)]
dev_ground = abs(ps_ground - PS_GROUND_MEASURED_EV)
print(f"\n   positronium ground (1s) = {ps_ground:.6f} eV   (known {PS_GROUND_MEASURED_EV:+.4f} eV)")
record("positronium ground ~ -6.803 eV", dev_ground, 5e-3, "quantitative", dev_ground < 5e-3)

# ---------------------------------------------------------------------------
# 3.  Clean -1/n^2 series for positronium (n = 1..5, s-states).
# ---------------------------------------------------------------------------
print("\n   positronium Rydberg series E_n[Ry] = -1/n^2:")
worst_series = 0.0
series = {}
for n in range(1, 6):
    ery = Ps["levels_Ry"][(n, 0)]
    dev = abs(ery + 1.0 / n ** 2)
    worst_series = max(worst_series, dev)
    series[n] = {"E_Ry": float(ery), "minus_1_over_n2": -1.0 / n ** 2, "dev": float(dev)}
    print(f"       n={n}:  E[Ry]={ery:+.6f}   -1/n^2={-1.0/n**2:+.6f}   dev={dev:.2e}")
record("positronium -1/n^2 series (n=1..5)", worst_series, 1e-3, "grid", worst_series < 1e-3)

# ---------------------------------------------------------------------------
# 4.  Independent verification of the scipy eigen-solve.
#     CLAUDE.md: verify scipy; hand-roll if it looks wrong.  We rebuild the
#     SAME real symmetric tridiagonal Coulomb matrix (l=0) and find the ground
#     eigenvalue by Sturm-sequence bisection (count sign agreements of the
#     leading-minor recurrence) — pure real arithmetic, no library eigensolver.
# ---------------------------------------------------------------------------
def coulomb_tridiag(l=0, x_max=None, N=N_GRID, n_levels=5):
    # Mirror ca_atom.radial_coulomb_levels' grid EXACTLY so the cross-check
    # compares solvers, not grids.
    if x_max is None:
        n_top = l + n_levels
        x_max = max(60.0, 6.0 * n_top * n_top)
    h = x_max / (N + 1)
    x = np.arange(1, N + 1) * h
    diag = 1.0 / h ** 2 + l * (l + 1) / (2.0 * x ** 2) - 1.0 / x
    off = -0.5 / h ** 2  # constant off-diagonal
    return diag, off


def sturm_count_below(diag, off, lam):
    """Number of eigenvalues < lam, via the symmetric-tridiagonal Sturm
    sequence (count of negative pivots in the LDL^T of (T - lam I))."""
    off2 = off * off
    d = diag[0] - lam
    neg = 1 if d < 0.0 else 0
    for k in range(1, diag.size):
        if d == 0.0:
            d = 1e-300
        d = (diag[k] - lam) - off2 / d
        if d < 0.0:
            neg += 1
    return neg


def ground_eig_bisection(diag, off, lo, hi, tol=1e-12):
    # ground state = smallest eigenvalue: find lam with count_below(lam) crossing 0->1
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if sturm_count_below(diag, off, mid) >= 1:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


diag0, off0 = coulomb_tridiag(l=0, x_max=None, N=N_GRID, n_levels=5)
eps_ground = ground_eig_bisection(diag0, off0, lo=-1.2, hi=0.0)  # eps in dimensionless units
E_ground_Ry_handrolled = 2.0 * eps_ground
E_ground_Ry_scipy = Ps["levels_Ry"][(1, 0)]
dev_solver = abs(E_ground_Ry_handrolled - E_ground_Ry_scipy)
print(f"\n   ground E[Ry]: scipy eigh_tridiagonal = {E_ground_Ry_scipy:+.8f}")
print(f"                 hand-rolled Sturm bisect = {E_ground_Ry_handrolled:+.8f}")
print(f"                 |difference| = {dev_solver:.2e}  (same matrix, real arithmetic)")
record("scipy == hand-rolled real solve", dev_solver, 1e-5, "verification", dev_solver < 1e-5)

# ---------------------------------------------------------------------------
# Verdict + JSON.
# ---------------------------------------------------------------------------
verdict = "PASS" if PASS else "FALSIFIED"

result = {
    "test_id": "FB06",
    "name": "Positronium levels are exactly half hydrogen",
    "verdict": verdict,
    "predicted": {
        "Ry_ratio_Ps_over_Hinf": 0.5,
        "positronium_ground_eV": -6.803,
        "series": "E_n[Ry] = -1/n^2",
        "basis": "Ry proportional to mu; mu(Ps)=m_e/2 => ratio = 1/2 (analytic)",
    },
    "measured_target": {
        "positronium_ground_eV": -6.8,
        "note": "measured Ps ground ~ -6.8 eV; -6.8028 eV = 1/4 Ry_inf equal-mass reduction",
    },
    "gate": {
        "ratio_eq_half_tol": 1e-9,
        "ground_eV": -6.803,
        "ground_tol_eV": 5e-3,
        "series_tol_Ry": 1e-3,
        "pass_if": "ratio = 1/2 to 1e-9 AND ground ~ -6.803 eV AND clean -1/n^2 series",
    },
    "computed": {
        "Ry_Ps_eV": Ps["Ry_eV"],
        "Ry_Hinf_eV": H_inf["Ry_eV"],
        "Ry_ratio": ry_ratio,
        "ratio_dev_from_half": dev_half,
        "positronium_ground_eV": ps_ground,
        "ground_dev_eV": dev_ground,
        "series": series,
        "series_worst_dev_Ry": worst_series,
        "ground_Ry_scipy": E_ground_Ry_scipy,
        "ground_Ry_handrolled": E_ground_Ry_handrolled,
        "solver_crosscheck_dev_Ry": dev_solver,
        "mu_Ps_MeV": mu_Ps,
        "mu_Hinf_MeV": mu_e,
        "alpha": atom.ALPHA,
        "N_grid": N_GRID,
        "checks": checks,
    },
    "commands": ["python3 tests/findings/test_FB06_positronium.py"],
    "timestamp": "2026-06-16",
}

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "FB06_positronium.json")
with open(out_path, "w") as fh:
    json.dump(result, fh, indent=2)

print("\n" + "=" * 84)
n_pass = sum(1 for c in checks if c["status"] == "PASS")
print(f"VERDICT: {verdict}   ({n_pass}/{len(checks)} checks)")
print(f"results -> {out_path}")
print("=" * 84)

sys.exit(0 if PASS else 1)
