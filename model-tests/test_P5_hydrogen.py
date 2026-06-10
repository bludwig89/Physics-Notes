#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_P5_hydrogen.py
===================

P5 of roadmap-matter-binding.md — the ATOM: an electron bound to a nucleus by
the electromagnetic (U(1), F69 paired-spinor photon) channel.  Hydrogen, with
positronium as the clean two-body validation, and the relativistic fine
structure from the DIRAC kinetic operator.

Engine reuse:
  • ca_atom.py — the attractive-1/r analogue of the F74 contact solver: a real
    symmetric tridiagonal radial Coulomb eigenproblem (non-relativistic), plus
    the exact Dirac-Coulomb (Sommerfeld) spectrum and a hand-rolled numerical
    radial-Dirac integrator (RK4 inward+outward matching) that reproduces it.

Parts
-----
  A  POSITRONIUM (two-body de-risk, run FIRST): the e+e- relative-coordinate
     reduction with mu=m_e/2 gives EXACTLY half the m_e-reduced-mass hydrogen
     spectrum; ground state ≈ -6.803 eV; its own 1/n^2 series.       (machine + quant)
  B  Rydberg series: E_n[Ry] = -1/n^2 for n=1..5 to the grid floor.   (grid)
  C  Coulomb l-degeneracy: equal-n, different-l levels coincide.      (grid)
  D  ABSOLUTE SCALE (headline): Ry = (1/2) mu c^2 alpha^2 from the model's own
     m_e (P0) and the EM coupling alpha gives the hydrogen ground state at
     -13.6 eV with NO further input.                                  (quantitative)
  E  Wavefunction: 1s is nodeless ~ x e^{-x}; <r>_1s = 1.5 a0; node count
     equals n-l-1 across the series.                                  (quantitative)
  F  FINE STRUCTURE (exact Dirac): Sommerfeld closed form == its O((Za)^4)
     series; 1s_{1/2} == CODATA Rydberg.                              (machine + quant)
  G  Numerical radial-Dirac == Sommerfeld for 1s_{1/2}, 2p_{1/2}, 2p_{3/2}: the
     fine structure is a genuine solve, not just the closed form.     (quantitative)
  H  The 2p_{3/2}-2p_{1/2} splitting is the measured 10.95 GHz / 45.3 ueV, and
     it scales as alpha^4 absolute (alpha^2 relative to the binding) — the
     defining signature of fine structure.                           (quantitative)
  I  In pure Dirac-Coulomb 2s_{1/2} and 2p_{1/2} are EXACTLY degenerate; the
     2s-2p Lamb shift is a beyond-Dirac QED effect (open QFT-4).      (machine)
  J  Grid convergence of the NR ground state.                         (quantitative)

CALIBRATION / INPUTS (honest accounting)
----------------------------------------
  • m_e c^2 = 0.510999 MeV : the electron mass — a MODEL anchor (P0 / F120-F121).
  • alpha   = 1/137.036    : the electromagnetic coupling — the one EMPIRICAL EM
                             number (P5 analogue of P4's g_A); fine structure is
                             a PREDICTION once alpha is fixed.
  • m_p     = 938.272 MeV  : sets the e-p reduced mass (a 0.05% shift off the
                             infinite-mass Rydberg).
The PREDICTIONS are the -1/n^2 series, the Coulomb l-degeneracy, the absolute
13.6 eV from (m_e, alpha), the alpha^2 fine structure and the 2s-2p Dirac
degeneracy — not any new empirical input.

All arithmetic REAL.  numpy + scipy.linalg.eigh_tridiagonal.

Run:  python3 model-tests/test_P5_hydrogen.py     (~15 s)
Writes test-results/P5_hydrogen.json.
"""

import os
import sys
import json
import math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ca-simulation"))
import ca_atom as atom  # noqa: E402

results = {"phase": "P5", "title": "hydrogen atom — Coulomb bound state, Rydberg series, Dirac fine structure",
           "checks": {}, "derived": {}, "notes": []}
PASS = True


def record(name, residual, target, tier, ok, extra=None):
    global PASS
    results["checks"][name] = {"residual": float(residual), "target": float(target),
                               "tier": tier, "status": "PASS" if ok else "FAIL"}
    if extra:
        results["checks"][name].update(extra)
    PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL':4s}] {name:54s} "
          f"resid={float(residual):.3e}  (target {float(target):.0e}, {tier})")


print("=" * 84)
print("P5 — the hydrogen atom: electron bound by EM (Coulomb 1/r), reuses the F74 solver")
print("=" * 84)

N_GRID = 6000
mu_H = atom.reduced_mass_MeV(atom.M_E_MEV, atom.M_P_MEV)
mu_e = atom.M_E_MEV                       # infinite-nucleus reference mass
mu_Ps = atom.M_E_MEV / 2.0
print(f"   inputs: m_e c^2={atom.M_E_MEV} MeV (model P0), alpha={atom.ALPHA:.9f} (EM coupling, ext),"
      f"\n           m_p c^2={atom.M_P_MEV} MeV -> mu(e-p)={mu_H:.6f} MeV")
results["derived"].update({"m_e_MeV": atom.M_E_MEV, "alpha": atom.ALPHA,
                           "m_p_MeV": atom.M_P_MEV, "mu_H_MeV": mu_H})

# ---------------------------------------------------------------------------
# A. Positronium two-body validation (FIRST).
# ---------------------------------------------------------------------------
print("\nA  positronium (two-body reduction, mu=m_e/2): exactly half of hydrogen(m_e)")
Ps = atom.hydrogen_spectrum(n_max=3, mu_MeV=mu_Ps, N=N_GRID)
H_inf = atom.hydrogen_spectrum(n_max=3, mu_MeV=mu_e, N=N_GRID)
ry_ratio = Ps["Ry_eV"] / H_inf["Ry_eV"]
print(f"       Ry(Ps)={Ps['Ry_eV']:.6f} eV   Ry(H_inf)={H_inf['Ry_eV']:.6f} eV   ratio={ry_ratio:.10f}")
record("A1 Ry(Ps)/Ry(H_inf) = 1/2 (reduced mass)", abs(ry_ratio - 0.5), 1e-9, "machine",
       abs(ry_ratio - 0.5) < 1e-9)
eb_ps = Ps["levels"][(1, 0)]
print(f"       positronium ground state = {eb_ps:.5f} eV   (known -6.8028 eV)")
record("A2 positronium ground ≈ -6.803 eV", abs(eb_ps + 6.8028), 5e-3, "quantitative",
       abs(eb_ps + 6.8028) < 5e-3)
# its own 1/n^2 series (n=1,2,3)
ps_series_ok = all(abs(Ps["levels_Ry"][(n, 0)] + 1.0 / n ** 2) < 5e-4 for n in (1, 2, 3))
record("A3 positronium 1/n^2 series (n=1..3)",
       max(abs(Ps["levels_Ry"][(n, 0)] + 1.0 / n ** 2) for n in (1, 2, 3)),
       5e-4, "grid", ps_series_ok)
results["derived"]["Ry_Ps_eV"] = Ps["Ry_eV"]
results["derived"]["positronium_ground_eV"] = eb_ps

# ---------------------------------------------------------------------------
# B. Hydrogen Rydberg series E_n[Ry] = -1/n^2.
# ---------------------------------------------------------------------------
print("\nB  hydrogen Rydberg series E_n = -Ry/n^2 (dimensionless E[Ry] = -1/n^2)")
H = atom.hydrogen_spectrum(n_max=5, mu_MeV=mu_H, N=N_GRID)
worst = 0.0
for n in range(1, 6):
    ery = H["levels_Ry"][(n, 0)]          # use the s-state of each n
    dev = abs(ery + 1.0 / n ** 2)
    worst = max(worst, dev)
    print(f"       n={n}: E[Ry]={ery:+.6f}   -1/n^2={-1.0/n**2:+.6f}   dev={dev:.2e}")
record("B  E_n[Ry] = -1/n^2 for n=1..5", worst, 1e-3, "grid", worst < 1e-3)
results["derived"]["series_worst_dev_Ry"] = worst

# ---------------------------------------------------------------------------
# C. Coulomb l-degeneracy (accidental SO(4) degeneracy).
# ---------------------------------------------------------------------------
print("\nC  Coulomb l-degeneracy: equal-n levels coincide across l")
deg_worst = 0.0
for n in (2, 3, 4, 5):
    e_ls = [H["levels_Ry"][(n, l)] for l in range(n)]
    spread = max(e_ls) - min(e_ls)
    deg_worst = max(deg_worst, spread)
    print(f"       n={n}: l-spread = {spread:.2e} Ry   ({n} sublevels)")
record("C  l-degeneracy (spread within n)", deg_worst, 2e-3, "grid", deg_worst < 2e-3)
results["derived"]["l_degeneracy_worst_Ry"] = deg_worst

# ---------------------------------------------------------------------------
# D. Absolute scale: 13.6 eV from (m_e, alpha) alone.
# ---------------------------------------------------------------------------
print("\nD  absolute scale: Ry = (1/2) mu c^2 alpha^2 from the model's m_e and alpha")
Ry_H = H["Ry_eV"]
Ry_reduced_codata = atom.RY_EV_CODATA * mu_H / atom.M_E_MEV   # CODATA Ry x reduced-mass factor
print(f"       Ry(H) = {Ry_H:.6f} eV   (CODATA reduced-mass {Ry_reduced_codata:.6f} eV)")
record("D1 Ry(H) matches reduced-mass CODATA", abs(Ry_H - Ry_reduced_codata) / Ry_reduced_codata,
       1e-5, "quantitative", abs(Ry_H - Ry_reduced_codata) / Ry_reduced_codata < 1e-5)
E_ground = H["levels"][(1, 0)]
print(f"       hydrogen ground state = {E_ground:.5f} eV   (measured -13.5983 eV)")
record("D2 ground state ≈ -13.6 eV", abs(E_ground + 13.5983) / 13.5983, 1e-3,
       "quantitative", abs(E_ground + 13.5983) / 13.5983 < 1e-3)
print(f"       a0(H) = {H['a0_nm']:.6f} nm   (Bohr radius, measured 0.052918 nm)")
record("D3 Bohr radius ≈ 0.0529 nm", abs(H["a0_nm"] - 0.0529177) / 0.0529177, 1e-3,
       "quantitative", abs(H["a0_nm"] - 0.0529177) / 0.0529177 < 1e-3)
results["derived"].update({"Ry_H_eV": Ry_H, "E_ground_eV": E_ground, "a0_nm": H["a0_nm"]})

# ---------------------------------------------------------------------------
# E. Wavefunction structure: 1s shape, <r>, node count.
# ---------------------------------------------------------------------------
print("\nE  wavefunctions: 1s ~ x e^{-x}, <r>_1s = 1.5 a0, node count = n-l-1")
E1s, x, u = atom.radial_coulomb_levels(0, n_levels=1, N=N_GRID)
u1s = u[:, 0]
h = x[1] - x[0]
# <r> in Bohr units: integral x |u|^2 dx  (u normalised to sum|u|^2 dx = 1)
r_exp = float(np.sum(x * u1s ** 2) * h)
print(f"       <r>_1s = {r_exp:.5f} a0   (exact 1.5)")
record("E1 <r>_1s = 1.5 a0", abs(r_exp - 1.5), 5e-3, "quantitative", abs(r_exp - 1.5) < 5e-3)
# 1s reduced radial function ∝ x e^{-x}: fit ln(u/x) slope = -1
mask = (x > 0.5) & (x < 6.0)
slope = np.polyfit(x[mask], np.log(np.abs(u1s[mask]) / x[mask]), 1)[0]
print(f"       1s ln(u/x) slope = {slope:.5f}   (exact -1)")
record("E2 1s ~ x e^{-x} (slope -1)", abs(slope + 1.0), 5e-3, "quantitative", abs(slope + 1.0) < 5e-3)
# node counting across the series


def count_nodes(uvec):
    s = np.sign(uvec)
    s = s[s != 0]
    return int(np.sum(s[1:] * s[:-1] < 0))


node_ok = True
node_report = {}
for l in range(0, 3):
    Es, xx, uu = atom.radial_coulomb_levels(l, n_levels=3, N=N_GRID)
    for k in range(3):
        n = l + 1 + k
        nodes = count_nodes(uu[:, k])
        node_report[f"{n}{'spd'[l]}"] = nodes
        if nodes != n - l - 1:
            node_ok = False
print(f"       nodes (n,l): {node_report}  (expect n-l-1)")
record("E3 node count = n-l-1", 0.0 if node_ok else 1.0, 0.5, "structural", node_ok)
results["derived"].update({"r_exp_1s_a0": r_exp, "slope_1s": float(slope), "nodes": node_report})

# ---------------------------------------------------------------------------
# F. Exact Dirac-Coulomb (Sommerfeld) vs its O((Za)^4) series; 1s == CODATA.
# ---------------------------------------------------------------------------
print("\nF  Dirac-Coulomb (Sommerfeld) fine structure: closed form vs O((Za)^4) series")
worst_series = 0.0
for (n, l, jh, j, lbl) in [(1, 0, True, 0.5, "1s_1/2"), (2, 0, True, 0.5, "2s_1/2"),
                           (2, 1, False, 0.5, "2p_1/2"), (2, 1, True, 1.5, "2p_3/2")]:
    kap = atom.kappa_of(l, jh)
    eb_exact = atom.sommerfeld_binding_eV(n, kap)
    lead, corr = atom.fine_structure_series_eV(n, j)
    eb_series = lead + corr
    dev = abs(eb_exact - eb_series) / abs(eb_exact)
    worst_series = max(worst_series, dev)
    print(f"       {lbl:7s} exact={eb_exact:.7f}  series(O(a^4))={eb_series:.7f}  rel={dev:.2e}")
record("F1 Sommerfeld == O((Za)^4) series", worst_series, 1e-6, "quantitative", worst_series < 1e-6)
# 1s_1/2 binding == CODATA Rydberg (infinite-mass Dirac, leading)
eb_1s = atom.sommerfeld_binding_eV(1, -1)
print(f"       1s_1/2 binding = {eb_1s:.6f} eV   (CODATA Ry = -{atom.RY_EV_CODATA:.6f}; Dirac shifts by O(a^4))")
record("F2 1s_1/2 ≈ -13.6057 eV", abs(eb_1s + atom.RY_EV_CODATA) / atom.RY_EV_CODATA, 1e-4,
       "quantitative", abs(eb_1s + atom.RY_EV_CODATA) / atom.RY_EV_CODATA < 1e-4)
results["derived"]["E_1s_dirac_eV"] = eb_1s

# ---------------------------------------------------------------------------
# G. Numerical radial-Dirac == Sommerfeld (genuine solve).
# ---------------------------------------------------------------------------
print("\nG  numerical radial-Dirac (RK4 matching) reproduces Sommerfeld")
worst_num = 0.0
for (n, kap, lbl) in [(1, -1, "1s_1/2"), (2, +1, "2p_1/2"), (2, -2, "2p_3/2")]:
    Enum = atom.numerical_dirac_energy(n, kap)
    Esom = atom.sommerfeld_energy(n, kap)
    rel = abs(Enum - Esom) / abs(1.0 - Esom)     # relative to the binding
    worst_num = max(worst_num, rel)
    print(f"       {lbl:7s} num={Enum:.12f}  som={Esom:.12f}  rel(binding)={rel:.2e}")
record("G  numerical Dirac == Sommerfeld (rel binding)", worst_num, 1e-4, "quantitative",
       worst_num < 1e-4)
results["derived"]["dirac_num_worst_rel"] = worst_num

# ---------------------------------------------------------------------------
# H. The 2p splitting: value AND alpha^2 (relative) / alpha^4 (absolute) scaling.
# ---------------------------------------------------------------------------
print("\nH  2p_{3/2}-2p_{1/2} fine-structure splitting: value + alpha-scaling")
split_eV = (atom.sommerfeld_binding_eV(2, atom.kappa_of(1, True))
            - atom.sommerfeld_binding_eV(2, atom.kappa_of(1, False)))
split_GHz = split_eV / 4.135667696e-15 / 1e9   # E = h nu, h = 4.1357e-15 eV·s
print(f"       Delta E(2p3/2-2p1/2) = {split_eV*1e6:.4f} ueV = {split_GHz:.4f} GHz "
      f"(measured ≈ 10.969 GHz)")
record("H1 splitting ≈ 10.95 GHz", abs(split_GHz - 10.969) / 10.969, 5e-3, "quantitative",
       abs(split_GHz - 10.969) / 10.969 < 5e-3)
# alpha-scaling: vary alpha, fit log-log slope of the absolute splitting (expect 4)
alphas = atom.ALPHA * np.array([0.5, 0.7, 1.0, 1.4, 2.0])
splits = np.array([abs(atom.sommerfeld_binding_eV(2, atom.kappa_of(1, True), alpha=a)
                       - atom.sommerfeld_binding_eV(2, atom.kappa_of(1, False), alpha=a))
                   for a in alphas])
slope_abs = np.polyfit(np.log(alphas), np.log(splits), 1)[0]
# relative to the binding (∝ alpha^2): slope should be ~2
binds = np.array([abs(atom.sommerfeld_binding_eV(2, atom.kappa_of(1, False), alpha=a)) for a in alphas])
slope_rel = np.polyfit(np.log(alphas), np.log(splits / binds), 1)[0]
print(f"       d ln(split)/d ln(alpha) = {slope_abs:.4f} (expect 4, absolute)")
print(f"       d ln(split/binding)/d ln(alpha) = {slope_rel:.4f} (expect 2, relative)")
record("H2 splitting ∝ alpha^4 (absolute)", abs(slope_abs - 4.0), 0.1, "quantitative",
       abs(slope_abs - 4.0) < 0.1)
record("H3 splitting/binding ∝ alpha^2 (relative)", abs(slope_rel - 2.0), 0.1, "quantitative",
       abs(slope_rel - 2.0) < 0.1)
results["derived"].update({"split_2p_ueV": split_eV * 1e6, "split_2p_GHz": split_GHz,
                           "alpha_slope_abs": float(slope_abs), "alpha_slope_rel": float(slope_rel)})

# ---------------------------------------------------------------------------
# I. Dirac 2s_{1/2} == 2p_{1/2} exactly (Lamb shift is beyond Dirac).
# ---------------------------------------------------------------------------
print("\nI  pure Dirac-Coulomb: 2s_{1/2} and 2p_{1/2} EXACTLY degenerate (Lamb = QED, F-QFT4)")
e_2s = atom.sommerfeld_energy(2, atom.kappa_of(0, True))   # kappa=-1
e_2p12 = atom.sommerfeld_energy(2, atom.kappa_of(1, False))  # kappa=+1
deg = abs(e_2s - e_2p12)
print(f"       |E(2s_1/2) - E(2p_1/2)| = {deg:.3e} (m_e c^2)   -> Lamb shift needs QED")
record("I  2s_1/2 == 2p_1/2 (same |kappa|)", deg, 1e-14, "machine", deg < 1e-14)
results["derived"]["dirac_2s_2p_degeneracy"] = float(deg)

# ---------------------------------------------------------------------------
# J. Grid convergence of the NR ground state toward E[Ry] = -1.
# ---------------------------------------------------------------------------
print("\nJ  grid convergence of the NR ground state (E[Ry] -> -1 as N grows)")
e_lo = atom.radial_coulomb_levels(0, n_levels=1, N=3000)[0][0]
e_hi = atom.radial_coulomb_levels(0, n_levels=1, N=8000)[0][0]
print(f"       E_1s[Ry]: N=3000 -> {e_lo:.6f}   N=8000 -> {e_hi:.6f}   (exact -1)")
improved = abs(e_hi + 1.0) < abs(e_lo + 1.0)
record("J1 ground state converges toward -1 Ry", abs(e_hi + 1.0), 5e-4, "grid",
       abs(e_hi + 1.0) < 5e-4)
record("J2 finer grid is more accurate", 0.0 if improved else 1.0, 0.5, "structural", improved)
results["derived"].update({"E1s_N3000_Ry": float(e_lo), "E1s_N8000_Ry": float(e_hi)})

# ---------------------------------------------------------------------------
results["notes"] = [
    "HEADLINE (D): the hydrogen ground state comes out at -13.60 eV from the "
    "model's own electron mass m_e (P0/F120-F121) and the electromagnetic "
    "coupling alpha alone — Ry = (1/2) mu c^2 alpha^2 — with no further input. "
    "The Bohr radius (0.0529 nm) and the full -Ry/n^2 Rydberg series follow.",
    "ENGINE: ca_atom.py is the attractive-1/r analogue of the F74 contact "
    "two-body solver — a real symmetric tridiagonal radial Coulomb eigenproblem. "
    "It reproduces E_n[Ry]=-1/n^2 (B) with the exact Coulomb l-degeneracy (C, the "
    "accidental SO(4) symmetry) to the grid floor, and the correct 1s shape, "
    "<r>=1.5 a0, and n-l-1 node structure (E).",
    "POSITRONIUM (A): the e+e- two-body problem reduces in the relative "
    "coordinate to the same 1/r solver with mu=m_e/2, giving EXACTLY half the "
    "infinite-mass hydrogen spectrum (ratio 0.5 to 1e-9) and a ground state of "
    "-6.803 eV. This de-risks the two-body reduction before the heavy proton.",
    "FINE STRUCTURE (F,G,H): the relativistic splitting is a PREDICTION of the "
    "DIRAC (not Schrödinger) kinetic operator. The exact Dirac-Coulomb "
    "(Sommerfeld) spectrum matches its O((Za)^4) expansion (F) and is reproduced "
    "by a hand-rolled numerical radial-Dirac integrator (G), so the splitting is "
    "a genuine solve. The 2p_{3/2}-2p_{1/2} gap is the measured 10.95 GHz / "
    "45.3 ueV (H1) and scales as alpha^4 absolute / alpha^2 relative to the "
    "binding (H2,H3) — the defining fine-structure signature.",
    "LAMB SHIFT IS BEYOND DIRAC (I): in pure Dirac-Coulomb 2s_{1/2} and 2p_{1/2} "
    "(same |kappa|=1) are EXACTLY degenerate (to 1e-14). The observed 2s-2p Lamb "
    "shift is a radiative QED effect (vacuum polarisation + self-energy) — the "
    "open QFT-4 item in first-gen-completeness.md §5.4 — not part of the "
    "one-body Dirac problem solved here.",
    "CALIBRATION (honest): m_e is a model anchor (P0/F120-F121); alpha is the one "
    "empirical EM coupling (the P5 analogue of P4's g_A); m_p sets the 0.05% "
    "reduced-mass shift. Everything else — the 1/n^2 series, l-degeneracy, the "
    "absolute 13.6 eV, the alpha^2 fine structure, and the Dirac 2s-2p degeneracy "
    "— is a prediction. P5 is independent of the QCD chain (needs only P0 + EM).",
    "LATTICE CAVEAT (roadmap): a full 3D real-space lattice Coulomb solve has "
    "known short-distance 1/r regularisation issues and the bound-state energy "
    "leans on the lattice spacing a (P6); the partial-wave-reduced radial solver "
    "used here is the standard, accurate route and sidesteps that — the "
    "positronium-first check confirms the two-body reduction is faithful.",
]

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-results"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "P5_hydrogen.json")
results["overall"] = "PASS" if PASS else "FAIL"
with open(out_path, "w") as fh:
    json.dump(results, fh, indent=2)

print("\n" + "=" * 84)
n_pass = sum(1 for c in results["checks"].values() if c["status"] == "PASS")
print(f"OVERALL: {'PASS' if PASS else 'FAIL'}   ({n_pass}/{len(results['checks'])} checks)")
print(f"results -> {out_path}")
print("=" * 84)
