#!/usr/bin/env python3
"""
run_lpt_wilson_selfenergy.py — NATIVE high-resolution driver for the full Wilson
lattice background-field gluon self-energy (F163). Exceeds the sandbox 45 s cap;
run on the host to push the BZ resolution to n = 64..128 and attempt the Q->0
plateau of the transverse finite constant -> Lambda_MSbar/Lambda_L vs 28.8086.

Usage:
    python3 tests/runners/run_lpt_wilson_selfenergy.py \
        --ns 48 64 96 128 --qs 0.15 0.2 0.3 0.45 0.6 \
        --out test-results/F163_wilson_selfenergy_highres.json

Memory: the self-energy quadrature is now CHUNKED over the first momentum axis
(ca_lpt_wilson_selfenergy._pi_chunked), so peak RAM is ~n^3, NOT n^4 — this fixes
the earlier 'zsh: killed' OOM. Cost is CPU-bound: ~n^4 total work (n=48 ~9 s per
(n,Q); n=96 ~2-3 min; n=128 ~8-10 min per point). Start small and scale:
    --ns 32 48 64    (minutes total)
then push --ns 96 128 overnight if a plateau is forming.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import os as _os, sys as _sys  # noqa: E401
_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "src"))

from casim.engine.gauge import lpt_wilson_selfenergy as se  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[32, 48, 64])
    ap.add_argument("--qs", type=float, nargs="+",
                    default=[0.15, 0.2, 0.3, 0.45, 0.6])
    ap.add_argument("--out", type=str,
                    default="test-results/F163_wilson_selfenergy_highres.json")
    args = ap.parse_args()

    t0 = time.time()
    res = se.highres(ns=tuple(args.ns), Qs=tuple(args.qs))
    res["wall_seconds"] = round(time.time() - t0, 1)
    res["ns"] = args.ns
    res["qs"] = args.qs

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(res, f, indent=2, default=float)
    print(json.dumps(res, indent=2, default=float))
    print(f"\nwrote {args.out}  ({res['wall_seconds']} s)")
    print("Interpretation: a Q-plateau in C_transv that is stable across n gives "
          "the finite constant; Lambda = exp(C_transv * 16 pi^2 / 22). Compare to "
          "28.8086. NB: the transverse readout omits the tadpole/measure "
          "transversality restoration (delta_mn sector) — add it before claiming "
          "the digit.")


if __name__ == "__main__":
    main()
