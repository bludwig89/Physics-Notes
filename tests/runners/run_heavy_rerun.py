#!/usr/bin/env python3
"""run_heavy_rerun.py — the two suite items too slow for the in-session sandbox.

Created 2026-06-02 alongside the full non-superseded suite rerun. Everything else
in the suite completed in-session; these two exceed the ~45 s sandbox call cap:

  1. test_F64_em_connection.py   — D-EM11 co-evolving self-redshift is a 120x120
                                    Cayley-solver evolution (220 steps x 2 packets),
                                    several minutes. D-EM1..D-EM10 already re-confirmed
                                    PASS in-session; D-EM11 was PASS in the prior run
                                    (test-results/F64_em_connection.json, 16/16, 2026-05-31).
  2. run_phase_tests.py          — Phases A-E; visualization-heavy (renders matplotlib
                                    frames from Phase A2 on). Numeric core overlaps
                                    run_phase2_f26_tests.py (17/17 PASS in-session).

Run from the repo root or anywhere:
    python3 tests/runners/run_heavy_rerun.py
Writes a machine-readable summary to test-results/heavy_rerun_<date>.json.
"""
import os, sys, json, time, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "src")
# Forks are loaded by file path, not as package modules (see D6/C6), so their
# sector directories go on PYTHONPATH the way the legacy forks/ dir used to.
_FORK_ROOT = os.path.join(SRC, "casim", "engine", "forks")
FORKS = [os.path.join(_FORK_ROOT, d) for d in sorted(os.listdir(_FORK_ROOT))
         if os.path.isdir(os.path.join(_FORK_ROOT, d)) and d != "__pycache__"]

env = dict(os.environ)
env["MPLBACKEND"] = "Agg"
env["PYTHONDONTWRITEBYTECODE"] = "1"
env["PYTHONPATH"] = os.pathsep.join(
    [SRC, HERE, *FORKS, env.get("PYTHONPATH", "")])

ITEMS = [
    os.path.join(HERE, "test_F64_em_connection.py"),
    os.path.join(HERE, "run_phase_tests.py"),
]

results = []
for path in ITEMS:
    name = os.path.basename(path)
    print(f"\n{'='*70}\nRUNNING {name}\n{'='*70}", flush=True)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-u", path], cwd=HERE, env=env)
    dt = time.time() - t0
    results.append(dict(test=name, exit=p.returncode, seconds=round(dt, 1)))
    print(f"\n--> {name}: exit {p.returncode} in {dt:.1f}s", flush=True)

out = os.path.join(ROOT, "test-results",
                   f"heavy_rerun_{datetime.date.today().isoformat()}.json")
with open(out, "w") as f:
    json.dump({"timestamp": datetime.datetime.now().strftime("%Y-%m-%d - %H:%M"),
               "results": results}, f, indent=2)
print("\nwrote", out)
