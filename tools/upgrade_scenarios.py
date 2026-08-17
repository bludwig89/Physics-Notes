#!/usr/bin/env python3
"""Migrate v1 scenario YAMLs to v2 — roadmap P4.

A v2 scenario is one that carries ``version: 2`` and validates strictly
(`casim.io.schema`).  This converter is deliberately minimal and
comment-preserving: it inserts a single ``version: 2`` line immediately before
the first top-level ``name:`` key (or at the top of the file if there is none),
leaving every comment, ordering and value untouched.  It is idempotent — a file
that already declares a ``version:`` is skipped — and it validates each file
after editing, refusing to leave a scenario that does not pass strict v2.

    python3 tools/upgrade_scenarios.py            # migrate scenarios/*.yaml
    python3 tools/upgrade_scenarios.py --check    # report only, exit 1 if any v1
    python3 tools/upgrade_scenarios.py path.yaml  # one file
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

from casim.io import validate_scenario_file  # noqa: E402

_NAME_RE = re.compile(r"^name:", re.MULTILINE)
_VERSION_RE = re.compile(r"^version:\s*\d+\s*$", re.MULTILINE)


def upgrade_text(text: str) -> tuple[str, bool]:
    """Return (new_text, changed).  No-op if a version: line already exists."""
    if _VERSION_RE.search(text):
        return text, False
    m = _NAME_RE.search(text)
    line = "version: 2\n"
    if m:
        return text[:m.start()] + line + text[m.start():], True
    return line + text, True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*",
                    help="scenario files (default scenarios/*.yaml)")
    ap.add_argument("--check", action="store_true",
                    help="report only; exit 1 if any file is still v1")
    args = ap.parse_args()

    paths = args.paths or sorted(glob.glob(os.path.join(_REPO, "scenarios",
                                                        "*.yaml")))
    changed = 0
    still_v1 = 0
    invalid = 0
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        new, will_change = upgrade_text(text)
        rel = os.path.relpath(p, _REPO)
        if args.check:
            if will_change:
                still_v1 += 1
                print(f"  v1  {rel}")
            continue
        if will_change:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(new)
            changed += 1
        errs = validate_scenario_file(p)
        if errs:
            invalid += 1
            print(f"  INVALID  {rel}")
            for e in errs[:6]:
                print(f"           {e}")

    if args.check:
        print(f"\n{len(paths)} scenario(s), {still_v1} still v1")
        return 1 if still_v1 else 0
    print(f"\n{len(paths)} scenario(s): {changed} migrated, "
          f"{invalid} invalid after migration")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
