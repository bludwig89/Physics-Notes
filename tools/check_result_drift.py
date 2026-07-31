#!/usr/bin/env python3
"""Report numeric drift in result artifacts against git — roadmap P1.2.

This is the failure mode the ~70 unfalsifiable tests never had. They already
write their numbers to `test-results/*.json`; those files are already in git;
so re-running one and comparing gives it a way to fail, without touching the
test.

Typical use, after re-running some physics:

    python3 tools/check_result_drift.py                 # what moved?
    python3 tools/check_result_drift.py --tol 1e-6      # ignore small wobble
    python3 tools/check_result_drift.py --only F107     # one finding

Exit codes: 0 = no drift, 1 = drift found, 2 = usage/environment problem.

Accepting a change is deliberate and uses the workflow that already exists:
read the report, then `git add` the result file. Nothing here rewrites
baselines for you — a tool that silently re-blesses its own output is not a
baseline system.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

from casim.baselines import (                              # noqa: E402
    DEFAULT_ABS, DEFAULT_REL, drift_report,
)


def _changed_result_files(ref: str) -> list[str]:
    """Tracked result JSONs that differ from `ref` in the working tree."""
    proc = subprocess.run(
        ["git", "diff", "--name-only", ref, "--", "test-results"],
        cwd=_REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        print("error: not a git repository, or git is unavailable.",
              file=sys.stderr)
        return []
    return [p for p in proc.stdout.split("\n")
            if p.endswith(".json") and not p.endswith("manifest.json")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="HEAD", help="git ref to compare against")
    ap.add_argument("--tol", type=float, default=DEFAULT_REL,
                    help=f"relative tolerance (default {DEFAULT_REL:g})")
    ap.add_argument("--abs", dest="abs_", type=float, default=DEFAULT_ABS,
                    help=f"absolute floor (default {DEFAULT_ABS:g})")
    ap.add_argument("--only", default=None,
                    help="substring filter on the result path")
    ap.add_argument("--quiet", action="store_true",
                    help="counts only, no per-value detail")
    ap.add_argument("--max-per-file", type=int, default=12)
    args = ap.parse_args()

    paths = _changed_result_files(args.ref)
    if args.only:
        paths = [p for p in paths if args.only in p]

    if not paths:
        print(f"no tracked result JSONs differ from {args.ref} — nothing to check")
        return 0

    report = drift_report(paths, ref=args.ref, cwd=_REPO,
                          rel=args.tol, abs_=args.abs_)

    text_only = len(paths) - len(report)
    if not report:
        print(f"{len(paths)} result file(s) changed, but no NUMERIC drift vs "
              f"{args.ref} (rel {args.tol:g}). The edits are timestamps or "
              f"formatting.")
        return 0

    print(f"\nnumeric drift vs {args.ref}  (rel {args.tol:g}, abs {args.abs_:g})")
    print("=" * 68)
    total = 0
    for path, deltas in sorted(report.items()):
        changed = sum(1 for d in deltas if d.kind == "changed")
        added = sum(1 for d in deltas if d.kind == "added")
        removed = sum(1 for d in deltas if d.kind == "removed")
        total += len(deltas)
        bits = [f"{changed} changed"]
        if added:
            bits.append(f"{added} added")
        if removed:
            bits.append(f"{removed} removed")
        print(f"\n  {path}   ({', '.join(bits)})")
        if args.quiet:
            continue
        for d in deltas[:args.max_per_file]:
            print(d)
        if len(deltas) > args.max_per_file:
            print(f"    … {len(deltas) - args.max_per_file} more")

    print("\n" + "=" * 68)
    print(f"  {len(report)} file(s) with numeric drift, {total} value(s)")
    if text_only:
        print(f"  {text_only} file(s) changed with no numeric drift "
              f"(timestamps/formatting)")
    print("\n  If a change is correct, accept it deliberately:  git add <file>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
