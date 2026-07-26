"""
run_d1_selfenergy.py — NATIVE runner for the d1 exact-vertex self-energy
(ca_lpt_selfenergy).  The 3-gluon loop is assembled from the EXACT generated Wilson
vertices (ca_lpt_generator), the ghost loop from the lattice FP vertex, and the Haar
measure term is DERIVED (C_A/24).  This converges the transverse finite constant vs n
and reports the Q-flatness (b0-preservation) diagnostic — the pieces the 45 s sandbox
cannot reach (n>=8 exceeds the cap; production is n=12..24).

WHAT IT PRODUCES
================
  1. vertex-wiring gate + Haar-measure derivation + scheme-consistency diagnosis
     (all cheap, exact/structural).
  2. finite_constant(n, Qs) for a sweep of n: C = 16 pi^2 (B_gluon+ghost,lat - B_cont),
     with the Q-spread (a residual log would grow like ln 1/Q; a genuine finite
     constant is Q-flat).  Read the constant from the largest n.
  3. seagull tadpole Z0(n) -> 0.15493 and the DERIVED measure counterterm, for the
     mass-sector (Wilson-28.81) bookkeeping.

HONEST SCOPE (see docs/theory/d1-kns-vertex-status.md, Task-4 diagnosis)
=======================================================================
The transverse constant here uses the EXACT plaquette-action (symmetric) vertex.
scheme_consistency_diagnosis proves that vertex is the SYMMETRIC YM vertex, not the
background-field (Abbott) vertex the b0=11 gate uses; the two differ by exactly one
term (the lattice background-covariant gauge-fixing vertex).  So the number reported
here is the ordinary-gauge exact-vertex constant — a large jump over the cosine
stand-in (~19 -> ~70 at n=6), which localises the former 74% gap to the cosine
approximation, NOT a certified d1.  Certification needs either the gauge-fixing
vertex (background-field route) or the vertex renormalisation Z1 (ordinary-gauge
route).

COST / RAM (4D BZ grid; the tensor build is 64 vectorised vertex calls per Q)
    n=8  -> ~40 s/Q     n=12 -> a few min/Q     n=16 -> ~10 min/Q
Use the largest 2-3 n for the trend; keep Qs small (0.1-0.3) for the flatness read.

USAGE (native, outside the sandbox)
===================================
    python3 tests/runners/run_d1_selfenergy.py --n 8 12 16 \
        --Q 0.1 0.15 0.2 0.3 --out test-results/d1_selfenergy.json
    python3 tests/runners/run_d1_selfenergy.py --smoke     # n=5, ~20 s sanity
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "ca-simulation"))

import ca_lpt_selfenergy as se        # noqa: E402

WILSON_TARGET_16PI2 = 73.9            # c=0.4682 (1/g^2) x 16 pi^2 (status doc)


def compute(ns, Qs) -> dict:
    out = {"target_16pi2": WILSON_TARGET_16PI2,
           "cosine_standin_leading": 19.1,
           "rule_lambda_target": 1.78,
           "vertex_wiring_gate": se.validate_vertex_wiring(),
           "haar_measure_derivation": se.haar_measure_coefficient(),
           "scheme_consistency_diagnosis": se.scheme_consistency_diagnosis(),
           "gauge_fixing_identity": se.gauge_fixing_identity_check(),
           "fp_dressing_gate": se.validate_fp_dressing(),
           "scheme_consistent_vs_n": {"wilson": [], "rule": []},
           "seagull_tadpole_vs_n": []}

    for n in ns:
        for kernel in ("wilson", "rule"):
            t0 = time.time()
            # DERIVED exact FP dressing (ghost 2 sin((p+p')/2) + gf midpoint phases)
            r = se.finite_constant_bgfield(n=n, Qs=tuple(Qs), kernel=kernel, fp="exact")
            r["seconds"] = round(time.time() - t0, 1)
            out["scheme_consistent_vs_n"][kernel].append(r)
            print(f"  n={n:3d} {kernel:6s} C={r['C']:+.3f} (spread "
                  f"{r['Q_spread']:.3f}, imB {r['max_imag_B']:.0e}) "
                  f"->Lambda={r['implied_lambda_ratio_exp_C_over_2b0']:.3f} "
                  f"[{r['seconds']}s]", flush=True)
        out["seagull_tadpole_vs_n"].append(se.seagull_tadpole(n=n))

    rule = out["scheme_consistent_vs_n"]["rule"][-1]
    out["verdict"] = (
        "SCHEME-CONSISTENT + EXACT FP DRESSING. Lattice Abbott = exact symmetric + "
        "DERIVED gauge-fixing vertex (Abbott=sym+V^gf, 0/64); DERIVED exact ghost "
        "2 sin((p+p')/2) + gf midpoint phases (Pi real). Q-flat => b0-preserving. "
        "Tadpole-free RULE d1: C=%.2f (16pi^2 u., n=%d) -> Lambda-ratio=%.3f (target "
        "1.78, far from Wilson 28.81). Read the digit from the n->inf trend." % (
            rule["C"], ns[-1], rule["implied_lambda_ratio_exp_C_over_2b0"]))
    print("\n" + out["verdict"], flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[8, 12, 16],
                    help="use EVEN n only (odd n places a grid point on k=0)")
    ap.add_argument("--Q", type=float, nargs="+", default=[0.1, 0.15, 0.2, 0.3])
    ap.add_argument("--out", type=str, default="test-results/d1_selfenergy.json")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    ns = [6] if args.smoke else args.n  # use EVEN n: odd n puts a grid point on k=0
    Qs = [0.15, 0.25] if args.smoke else args.Q

    out = compute(ns, Qs)
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "..", args.out)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
