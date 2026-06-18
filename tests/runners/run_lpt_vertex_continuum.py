"""
run_lpt_vertex_continuum.py — NATIVE large-L continuum-limit validation of the
3-gluon vertex extractor (ca_lpt_vertex), to run outside the 45 s sandbox.

The in-sandbox checks already PASS (machine precision, convention-free):
  * propagator_check   — quadratic term reproduces the gluon propagator K_hat
  * bose_antisymmetry  — colour swap flips the sign (f^{abc})
  * bose_full_symmetry — full (momentum+Lorentz+colour) leg exchange leaves V

What needs LARGE L (small lattice momentum, where the point-splitting form
factors cos(k_mu/2) -> 1) is the continuum-MAGNITUDE check: the volume-normalised
contracted amplitude divided by the continuum tensor contraction,
(amp/Vol)/continuum, must approach a SINGLE constant as k -> 0. The smallest
momentum on an L^4 lattice is k_min = 2 sin(pi/L), so only large L reaches the
clean continuum regime (L=8 -> k=0.77 is too coarse; L=32 -> k=0.196).

Usage (native):
    python3 tests/runners/run_lpt_vertex_continuum.py \
        --L 12 16 20 24 28 32 --out test-results/lpt_vertex_continuum.json

Reads back: if ratio(L) flattens to a constant as L grows, the vertex carries
the correct continuum tensor structure AND form factors -> the extractor is
fully validated and ready to fold with the rule's Omega_even propagator + ghost
loop for the d1 / q* integral.

Cost (vectorised SU(2), 4D, 8 action evals per L):
    L=16 -> 65k sites, seconds;  L=24 -> 332k, ~1 min;  L=32 -> 1.05M, a few min
    and a few GB transient. Drop the largest L if memory-limited; the TREND
    (ratio flattening) is the signal, not any single L.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))

import ca_lpt_vertex as vtx   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, nargs="+", default=[12, 16, 20, 24])
    ap.add_argument("--g", type=float, default=0.3)
    ap.add_argument("--out", default="test-results/lpt_vertex_continuum.json")
    args = ap.parse_args()

    rows = []
    for L in args.L:
        t0 = time.time()
        pt = vtx.continuum_scaling_point(L, g=args.g)
        pt["secs"] = round(time.time() - t0, 1)
        rows.append(pt)
        print(f"  L={L:3d}  k={pt['kmag']:.4f}  (amp/Vol)/cont={pt['ratio']}"
              f"  ({pt['secs']}s)", flush=True)

    # convergence diagnostic: relative change of the ratio over the last two L
    ratios = [r["ratio"] for r in rows if r["ratio"] is not None]
    flattening = None
    if len(ratios) >= 2 and abs(ratios[-1]) > 1e-30:
        flattening = abs(ratios[-1] - ratios[-2]) / abs(ratios[-1])

    report = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "rows": rows,
        "last_step_rel_change": flattening,
        "interpretation": "ratio (amp/Vol)/continuum should approach a CONSTANT "
                          "as k->0; a shrinking last_step_rel_change with growing "
                          "L = the vertex carries the correct continuum tensor + "
                          "form factors (continuum-magnitude validation).",
        "structural_checks_in_sandbox": {
            "propagator": "PASS (machine)", "colour_antisymmetry": "PASS (machine)",
            "bose_full_symmetry": "PASS (machine)"},
        "next": "if flattened: fold this vertex with the rule Omega_even "
                "propagator + ghost loop -> d1 -> q* (ca_gluon_self_energy).",
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nwrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
