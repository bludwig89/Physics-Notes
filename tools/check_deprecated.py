#!/usr/bin/env python3
"""Enforce the `deprecated/` acceptance rules — roadmap C0.5.

`deprecated/code/` and `deprecated/tests/` each publish a rule in their README.
Without enforcement a README is a suggestion, and the whole point of those two
directories is that a file cannot be quietly parked in one.

The rules, restated:

  * **`deprecated/code/`** — every `.py` here must either be the `source` of a
    record in `docs/design/module-migration-manifest.yaml`, or be named in
    `docs/theory/supersessions.yaml`.
  * **`deprecated/tests/`** — every `.py` here must be named in the ledger with
    `status: fully_superseded`. Nothing else qualifies. P0.4 found that of 14
    files an audit called superseded, exactly **one** was; eleven were a dead
    verdict wrapped around live algebra, and moving them would have silently
    retired working coverage.
  * A migrated backup must still carry its `# ===== deprecated/code backup`
    header, so the original content can be recovered by
    `migrate_module.py --rollback`.

Usage:
    python3 tools/check_deprecated.py
    python3 tools/check_deprecated.py --verbose
"""
from __future__ import annotations

import argparse
import os
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(_REPO, "deprecated", "code")
TESTS_DIR = os.path.join(_REPO, "deprecated", "tests")
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")

BACKUP_MARK = "# ===== deprecated/code backup"


def _yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="store_true")
    args = ap.parse_args()

    manifest = _yaml(MANIFEST)
    ledger = _yaml(LEDGER)

    by_basename = {os.path.basename(r["source"]): r
                   for r in manifest.get("modules", [])}
    ledger_names = set()
    fully_superseded = set()
    for rec in ledger.get("supersessions", []):
        for c in rec.get("code", []) or []:
            if c.get("path"):
                ledger_names.add(os.path.basename(c["path"]))
        for t in rec.get("tests", []) or []:
            if t.get("path"):
                ledger_names.add(os.path.basename(t["path"]))
                if t.get("status") == "fully_superseded":
                    fully_superseded.add(os.path.basename(t["path"]))

    errs: list[str] = []
    checked = 0

    for fn in sorted(os.listdir(CODE_DIR) if os.path.isdir(CODE_DIR) else []):
        if not fn.endswith(".py"):
            continue
        checked += 1
        rec = by_basename.get(fn)
        if rec is None and fn not in ledger_names:
            errs.append(
                f"deprecated/code/{fn}: no manifest record and not named in "
                f"the supersession ledger. Add one, or it does not belong here.")
            continue
        with open(os.path.join(CODE_DIR, fn), encoding="utf-8",
                  errors="replace") as fh:
            head = fh.read(200)
        if rec is not None and not head.startswith(BACKUP_MARK):
            errs.append(
                f"deprecated/code/{fn}: missing the migration header. "
                f"`migrate_module.py --rollback` splits on it to recover the "
                f"original, so without it the backup cannot be restored.")
        if rec is not None and not rec.get("migrated"):
            errs.append(
                f"deprecated/code/{fn}: a backup exists but the manifest "
                f"record has `migrated: null`. Either the migration aborted "
                f"without rolling back, or the stamp was lost.")
        if args.verbose:
            print(f"  ok  deprecated/code/{fn}")

    for fn in sorted(os.listdir(TESTS_DIR) if os.path.isdir(TESTS_DIR) else []):
        if not fn.endswith(".py"):
            continue
        checked += 1
        if fn not in fully_superseded:
            errs.append(
                f"deprecated/tests/{fn}: not recorded as `fully_superseded` "
                f"in the ledger. Partially-superseded files stay in tests/ "
                f"with a banner — their live checks are load-bearing.")
        elif args.verbose:
            print(f"  ok  deprecated/tests/{fn}")

    if errs:
        print(f"deprecated/ INVALID ({len(errs)}):")
        for e in errs:
            print(f"  - {e}")
        return 1
    print(f"deprecated/ is accounted for — {checked} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
