"""
run_l6_native_sweep.py — NATIVE runner for F337's ledger-d1 / L6 native sweep.

The ledger (docs/status/open-derivations.md, row d1) called for "a native
sweep at n=28-40 on the repaired path" to close S3 (the quotability gate of
`lpt_d1_action_consistent.delta_loops`). The UNCHUNKED path OOMs at n=32 on a
4 GB machine (measured: SIGKILL, peak RSS 3.79 GB, ~7 s wall clock -- the full
(n,n,n,n,N,N,N) vertex tensors are the culprit, ~2 GB each at n=28). This
runner uses `lpt_d1_action_consistent.pi_loop_chunked`, verified bit-identical
to the unchunked `pi_loop` (see tests/findings/test_F337_l6_decision.py),
which streams over the grid's first axis and peaks under 1 GB through n=40.

WHAT IT PRODUCES
================
Per (n, branch) in {phys, raw} x {28,32,36,40}, and the Wilson ("sc") side:
b0_recovery, and the slope-/analytic-normalised dLoops = C_hat(rule) -
C_hat(wilson). Writes incrementally (JSON checkpoint keyed by "{n}_{label}_{qi}",
one entry per momentum point) so a run split across several shorter
invocations resumes rather than restarting -- this machine's shell has a
short per-call wall-clock limit; the full sweep took a total of roughly
15-20 minutes of wall time spread over many such calls, 2026-08-30.

HONEST SCOPE
============
The finding this feeds (F337) does NOT report S3 as closed: the native sweep
SHARPENS the tension rather than resolving it -- see findings/F337-*.md
Sec.4-5 for the diagnosis (the analytic-normalised series converges cleanly,
sub-1/n^2; the slope-normalised series' increments do not shrink through
n=40; the two together push the implied Lambda_MSbar/Lambda_rule to ~31,
outside F280's own [1, 7.98] bracket -- read as non-convergence, per F307's
own standing caution, not as a falsification).

USAGE (native, outside the sandbox)
====================================
    python3 tests/runners/run_l6_native_sweep.py \
        --out test-results/F337_l6_native_sweep_raw_per_Q.json \
        --deadline-sec 100
    # re-run the same command repeatedly; it resumes from the checkpoint.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

from casim.engine.gauge.lpt_d1_action_consistent import transverse_B_chunked
from casim.engine.gauge.lpt_d1_subtracted import CELL_RATIOS

NS = (28, 32, 36, 40)
BRANCHES = {"sc": ("sc", "phys"), "phys": ("bcc", "phys"), "raw": ("bcc", "raw")}


def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save(path, d):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="test-results/F337_l6_native_sweep_raw_per_Q.json")
    ap.add_argument("--deadline-sec", type=float, default=1e9)
    ap.add_argument("--ns", type=int, nargs="+", default=list(NS))
    args = ap.parse_args()

    data = load(args.out)
    deadline = time.time() + args.deadline_sec

    for n in args.ns:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        for label, (action, branch) in BRANCHES.items():
            for qi, Q in enumerate(Qs):
                key = f"{n}_{label}_{qi}"
                if key in data:
                    continue
                if time.time() > deadline:
                    print("STOPPING before deadline; re-run to resume", flush=True)
                    save(args.out, data)
                    return
                t0 = time.time()
                B = transverse_B_chunked(action, Q, n, branch)
                dt = round(time.time() - t0, 1)
                data[key] = {"n": n, "label": label, "Q": Q, "B": B, "sec": dt}
                save(args.out, data)
                print("DONE", key, "sec", dt, "B", B, flush=True)

    print("ALL DONE", flush=True)


if __name__ == "__main__":  # pragma: no cover
    main()
