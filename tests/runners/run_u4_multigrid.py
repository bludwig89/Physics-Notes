#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_u4_multigrid.py — U4 block-spin two-grid multigrid, PRODUCTION run.

The sandbox in-test (test_F159) validates the U4 mechanism at small L/short
relaxation (trends + exact charge conservation).  This runner does the
ACCURATE, large-L job that exceeds the sandbox timeout, and writes a JSON for
Claude to read back:

  A. ABSOLUTE accuracy — the dimensionless point-charge hydrogen ground state
     converges to the exact E0 = −0.5 Hartree, a0 = 1 as L (box+resolution)
     grows.  (Validates the coarse-grid electron solver quantitatively.)
  B. INVARIANCE — the physical ground state is invariant under the coarse
     spacing a_c = b·a_f over a wide b sweep (R_b commutes with the orbit
     binding; the multigrid licensing).
  C. POINT-vs-RESOLVED — the binding gap → 0 as a0/r_p grows, at large L.
  D. PHYSICAL SCALE SEPARATION — the two-grid atom at the physical hydrogen
     ratio a0/r_p ≈ 6.3e4 (≈4.8 decades): the block factor b carries it while
     both lattices stay tractable.

Usage (Claude Code, native, longer than the sandbox cap):
    python tests/runners/run_u4_multigrid.py            # default (heavy)
    python tests/runners/run_u4_multigrid.py --quick    # lighter
    python tests/runners/run_u4_multigrid.py --L 96 --relax 6000

Writes: test-results/u4_multigrid.json
"""
from __future__ import annotations
import os, sys, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "ca-simulation"))
for p in ("ca-simulation", "../ca-simulation", "../../ca-simulation"):
    if os.path.isdir(p):
        sys.path.insert(0, p)
import ca_multigrid as mg          # noqa: E402

R_P_PHYS_FM = 0.84                 # proton charge radius (CODATA)
A0_PHYS_FM = 5.29177e4            # Bohr radius in fm
PHYS_RATIO = A0_PHYS_FM / R_P_PHYS_FM   # ≈ 6.3e4


def converge_absolute(Ls, relax, dtau):
    """A: point-ish-charge hydrogen E0,⟨r⟩ vs L.

    Convergence to the continuum (-0.5 Ha, ⟨r⟩=1.5 a0) needs the BOX to grow,
    not just the resolution — the earlier 'a=8/L' parametrization held box=8 a0
    fixed, so box-truncation bias was L-independent and E0/⟨r⟩ plateaued
    (~-0.508 / ~1.618), NOT a convergence (a discretization artifact, not
    rounding).  Here the spacing is FIXED fine (a=0.15 a0) and L grows, so the
    box = L·a grows; a small soft-core nucleus (0.1 a0 ≪ a0) tames the Coulomb
    cusp.  E0→-0.5, ⟨r⟩→1.5 from above as the box opens up.
    """
    a = 0.15                        # fixed fine spacing (a0 units)
    rows = []
    for L in Ls:
        box = L * a
        t0 = time.time()
        r = mg.solve_hydrogen(L, a, m=1.0, k=1.0, src_rms_cells=0.5,
                              relax_steps=relax, dtau=dtau)
        rows.append({"L": L, "a": a, "box_a0": box, "E0": r["E0"],
                     "mean_r": r["a0"], "E0_err_vs_-0.5": abs(r["E0"] + 0.5),
                     "mean_r_err_vs_1.5": abs(r["a0"] - 1.5),
                     "secs": round(time.time() - t0, 1)})
        print(f"  [A] L={L:3d} box={box:4.1f}a0 E0={r['E0']:.5f} (exact -0.5) "
              f"<r>={r['a0']:.5f} (exact 1.5) {rows[-1]['secs']}s", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--L", type=int, default=None)
    ap.add_argument("--relax", type=int, default=None)
    args = ap.parse_args()

    if args.quick:
        Ls = [32, 48, 64]; relax = 2500; dtau = 0.02; big_L = 80
        b_sweep = [1, 2, 4, 8]
    else:
        Ls = [48, 64, 96, 128]; relax = args.relax or 8000; dtau = 0.01
        big_L = args.L or 160
        b_sweep = [1, 2, 4, 8, 16]

    out = {"meta": {"phys_ratio_a0_over_rp": PHYS_RATIO,
                    "r_p_phys_fm": R_P_PHYS_FM, "a0_phys_fm": A0_PHYS_FM,
                    "Ls": Ls, "relax": relax, "big_L": big_L},
           "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    t_all = time.time()

    print("[A] absolute accuracy (point-charge hydrogen → E0=-0.5, a0=1):", flush=True)
    out["A_absolute"] = converge_absolute(Ls, relax, dtau)

    print("[B] invariance under coarse spacing a_c=b·a_f:", flush=True)
    inv = mg.invariance_under_b(L=big_L, a_f=8.0 / big_L, b_list=b_sweep,
                                relax_steps=relax, dtau=dtau)
    out["B_invariance"] = inv
    print(f"  [B] E0 rel-spread over b={b_sweep}: {inv['E0_rel_spread']:.4f}", flush=True)

    print("[C] point-vs-resolved binding (large L):", flush=True)
    bc = mg.binding_commutes(L=big_L, a=8.0 / big_L,
                             r_p_list=(8.0, 4.0, 2.0, 1.0),
                             relax_steps=relax, dtau=dtau)
    out["C_point_vs_resolved"] = bc
    for r in bc["resolved"]:
        print(f"  [C] a0/r_p={r['a0_over_rp']:6.1f} dE_vs_point={r['dE_vs_point']:.5f}",
              flush=True)

    print("[D] physical scale separation (two-grid atom at b → 6.3e4 ratio):", flush=True)
    rows = []
    for b in [1e3, 1e4, 6.3e4, 1e5]:
        atom = mg.MultigridAtom(b=int(b), L_fine=24, r_p_fine=3.0,
                                L_coarse=big_L, relax_steps=relax).run()
        rows.append({"b": int(b),
                     "represented_a0_over_rp": atom["represented_a0_over_rp"],
                     "represented_decades": atom["represented_decades"],
                     "charge_conserved": atom["proton_charge_conserved"],
                     "electron_bound": atom["electron_bound"],
                     "E0": atom["electron_E0"]})
        print(f"  [D] b={int(b):>7d} ratio={atom['represented_a0_over_rp']:.3e} "
              f"({atom['represented_decades']:.2f} dec) bound={atom['electron_bound']}",
              flush=True)
    out["D_scale_separation"] = rows
    # the b that reproduces the physical hydrogen ratio
    out["D_physical_b"] = next((r for r in rows if abs(r["b"] - 63000) < 5000), None)

    out["elapsed_secs"] = round(time.time() - t_all, 1)
    out["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    dest = os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))), "test-results",
        "u4_multigrid.json")
    with open(dest, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(dest)}  ({out['elapsed_secs']}s)", flush=True)


if __name__ == "__main__":
    main()
