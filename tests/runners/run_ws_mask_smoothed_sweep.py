"""run_ws_mask_smoothed_sweep.py -- checkpointed runner for the F337 Sec.4/6
smoothed-mask re-run of the native n=28-40 dLoops sweep (this session's
finding). Mirrors F337's own ``run_l6_native_sweep.py`` checkpoint pattern:
each invocation computes whatever (n, action, branch, Q) points are still
missing from the checkpoint JSON, in order, until a wall-clock budget is
hit, then exits -- safe to re-run repeatedly until complete.

Usage: PYTHONPATH=src python3 tests/runners/run_ws_mask_smoothed_sweep.py [budget_seconds]
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

PYTHONPATH_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "src")
sys.path.insert(0, os.path.abspath(PYTHONPATH_ROOT))

from casim.engine.gauge import lpt_d1_action_consistent as m  # noqa: E402
from casim.engine.gauge import lpt_ws_mask_cutcell as wsm  # noqa: E402
from casim.engine.gauge.lpt_d1_subtracted import CELL_RATIOS  # noqa: E402

CKPT = os.path.join(os.path.dirname(__file__), "..", "..",
                     "test-results", "smoothed_ws_mask_sweep_checkpoint_v2.json")
NS = (12, 16, 20, 24, 28, 32, 36, 40)


def _load():
    if os.path.exists(CKPT):
        with open(CKPT) as f:
            return json.load(f)
    return {}


def _save(d):
    tmp = CKPT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1)
    os.replace(tmp, CKPT)


def _key(n, action, branch, qi):
    return f"n={n}|action={action}|branch={branch}|qi={qi}"


def main(budget_seconds=150.0):
    t0 = time.time()
    data = _load()
    n_done_this_run = 0
    for n in NS:
        sp = 2 * math.pi / n
        Qs = [r * sp for r in CELL_RATIOS]
        mask_grid, n_amb = wsm.smoothed_ws_mask(n, depth_max=5)
        for action, branch in (("sc", "phys"), ("bcc", "phys"), ("bcc", "raw")):
            mg = mask_grid if action == "bcc" else None
            for qi, Q in enumerate(Qs):
                key = _key(n, action, branch, qi)
                if key in data:
                    continue
                if time.time() - t0 > budget_seconds:
                    print(f"budget exhausted, {n_done_this_run} points this run, "
                          f"checkpoint has {len(data)} points")
                    return
                tB0 = time.time()
                B = m.transverse_B_chunked(action, Q, n, branch, mask_grid=mg)
                data[key] = {"n": n, "action": action, "branch": branch,
                             "qi": qi, "Q": Q, "B": B, "n_ambiguous": n_amb,
                             "wall_s": time.time() - tB0}
                _save(data)
                n_done_this_run += 1
                print(f"done {key} B={B:.6f} ({time.time()-tB0:.1f}s)")
    print(f"ALL DONE, {len(data)} points total")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 150.0)
