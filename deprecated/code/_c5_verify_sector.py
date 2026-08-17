#!/usr/bin/env python3
"""C5 — run the particles sector's tests and diff their result artifacts.

This is `migrate_module.py` step 6, lifted out of the per-module loop and run
once over the sector (see `tools/_c5_migrate_particles.py` for why). Snapshot
every artifact the sector's records name, run the tests the way
`migrate_module.how_to_run` says each must be run, diff, then **restore the
snapshot** so a verification run never leaves drift behind.

    python3 tools/_c5_verify_sector.py --slice 0 4     # tests 0..(len/4)
"""
from __future__ import annotations

import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml  # noqa: E402

from migrate_module import (  # noqa: E402
    _REPO,
    check_drift,
    load_manifest,
    run_tests,
)

SECTOR = "particles"
STATE = "/tmp/c5_verify_state.json"


def sector_records():
    m = load_manifest()
    return [r for r in m["modules"] if r["sector"] == SECTOR]


def main() -> int:
    recs = sector_records()
    tests = sorted({t for r in recs for t in r["tests"]})
    arts = sorted({b for r in recs for b in r["baselines"]})

    lo, n = 0, 1
    if "--slice" in sys.argv:
        i = sys.argv.index("--slice")
        lo, n = int(sys.argv[i + 1]), int(sys.argv[i + 2])
    size = (len(tests) + n - 1) // n
    chunk = tests[lo * size:(lo + 1) * size]
    timeout = int(sys.argv[sys.argv.index("--timeout") + 1]) \
        if "--timeout" in sys.argv else 120

    print(f"sector {SECTOR}: {len(tests)} test(s), {len(arts)} artifact(s)")
    print(f"slice {lo + 1}/{n} -> {len(chunk)} test(s), per-test timeout {timeout}s\n")

    # Snapshot into a temp dir we own, so the restore is independent of the
    # journal's lifetime (and survives this process being killed by a timeout).
    snapdir = "/tmp/c5_snap"
    os.makedirs(snapdir, exist_ok=True)
    snapshot = {}
    for rel in arts:
        full = os.path.join(_REPO, rel)
        if not os.path.exists(full):
            continue
        dst = os.path.join(snapdir, rel.replace("/", "__"))
        if not os.path.exists(dst):          # first slice wins; later slices reuse
            shutil.copy2(full, dst)
        snapshot[rel] = dst

    fails, ran, skipped = run_tests(chunk, timeout)
    drift, n_floor = check_drift(snapshot)

    # Restore, always — a verify must not leave the tree dirty.
    for rel, snap in snapshot.items():
        shutil.copy2(snap, os.path.join(_REPO, rel))

    out = {"slice": lo, "ran": ran, "fails": fails,
           "skipped": skipped, "drift": drift, "floor": n_floor}
    prev = {}
    if os.path.exists(STATE):
        with open(STATE) as fh:
            prev = json.load(fh)
    prev[str(lo)] = out
    with open(STATE, "w") as fh:
        json.dump(prev, fh, indent=1)

    print(f"\n  ran {ran}, skipped {len(skipped)}, failed {len(fails)}, "
          f"drift {len(drift)} file(s)"
          + (f", {n_floor} round-off-floor move(s)" if n_floor else ""))
    for f in fails:
        print("  FAIL " + f)
    for d in drift:
        print("  DRIFT " + d)
    return 1 if (fails or drift) else 0


if __name__ == "__main__":
    sys.exit(main())
