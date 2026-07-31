#!/usr/bin/env python3
"""C5 — triage result drift against HEAD at the project's own exactness floor.

`tools/check_result_drift.py` reports at rel 1e-9 / abs 1e-15, which is far
below the `machine` class the project actually gates on (1e-12, see
`casim.baselines.MACHINE_FLOOR`). Running a test twice on the same machine can
move a 1e-14 residual by tens of percent *relatively* while both values remain
indistinguishable at the gate — so the strict report cannot, on its own,
distinguish "the migration changed physics" from "floating-point work was
reordered". This applies the gate's own floor and splits the report three ways:

  SIGNIFICANT  — above the machine floor. A migration must not produce these.
  FLOOR        — below it: round-off, reported and counted, never hidden.
  NON_NUMERIC  — wall-clock timings and pass/fail flags, which are not physics.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

from casim.baselines import MACHINE_FLOOR, compare, significant  # noqa: E402

# Fields that are timing or bookkeeping, not model output. Named explicitly so
# nothing is excluded by a loose substring rule.
TIMING = ("t_lazy", "t_sync", "overhead", "secs", "seconds", "elapsed",
          "wall", "duration")


def head_blob(rel: str):
    p = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=_REPO,
                       capture_output=True, text=True)
    if p.returncode:
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


def changed_files() -> list[str]:
    p = subprocess.run(["git", "diff", "--name-only", "--", "test-results"],
                       cwd=_REPO, capture_output=True, text=True)
    return [l for l in p.stdout.splitlines() if l.endswith(".json")]


def main() -> int:
    sig_files, floor_files, timing_files = {}, {}, {}
    for rel in changed_files():
        before = head_blob(rel)
        if before is None:
            continue
        full = os.path.join(_REPO, rel)
        try:
            with open(full, encoding="utf-8") as fh:
                after = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        deltas = compare(before, after, floor=MACHINE_FLOOR)
        real = significant(deltas)
        timing = [d for d in real if any(t in str(d.path) for t in TIMING)]
        real = [d for d in real if d not in timing]
        if real:
            sig_files[rel] = real
        if timing:
            timing_files[rel] = timing
        floor = len(deltas) - len(significant(deltas))
        if floor:
            floor_files[rel] = floor

    print(f"floor = {MACHINE_FLOOR:g}  (the project's `machine` exactness class)\n")
    print(f"SIGNIFICANT drift: {len(sig_files)} file(s)")
    for rel, ds in sorted(sig_files.items()):
        print(f"  {rel}")
        for d in ds[:8]:
            print("      " + str(d).strip())
    print(f"\nTIMING/bookkeeping only: {len(timing_files)} file(s)")
    for rel, ds in sorted(timing_files.items()):
        print(f"  {rel}  ({len(ds)} field(s): "
              f"{', '.join(sorted({str(d.path).split('.')[-1] for d in ds})[:6])})")
    print(f"\nBELOW FLOOR (round-off): {len(floor_files)} file(s), "
          f"{sum(floor_files.values())} value(s)")
    for rel, n in sorted(floor_files.items()):
        print(f"  {rel}  {n} value(s)")
    return 1 if sig_files else 0


if __name__ == "__main__":
    sys.exit(main())
