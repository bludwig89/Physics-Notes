#!/usr/bin/env python3
"""C5 — make `deprecated/code/README.md`'s Reason column tell the truth.

`migrate_module.index_backup` writes "moved unchanged" whenever it stripped no
`dead_symbols`, which conflates two different things: the file was copied
byte-identically (true for every particles record) and the file that LANDED at
the target is byte-identical (not true — 11 carry import rewrites, 3 carry a
results-path fix and a `__main__` guard). The Reason column is the audit trail
a future reader will trust, so it should say which.

Only rewrites rows whose target is a migrated `sector: particles` record.
"""
from __future__ import annotations

import difflib
import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
README = os.path.join(_REPO, "deprecated", "code", "README.md")
MARK = "# ==================================================================\n"


def classify(rec) -> str:
    backup = os.path.join(_REPO, "deprecated", "code",
                          os.path.basename(rec["source"]))
    target = os.path.join(_REPO, rec["target"])
    if not (os.path.exists(backup) and os.path.exists(target)):
        return "moved unchanged"
    body = open(backup, encoding="utf-8").read().split(MARK, 1)[1]
    landed = open(target, encoding="utf-8").read()
    if body == landed:
        return "copied byte-identically; no symbols stripped"
    hunks = [l for l in difflib.unified_diff(body.splitlines(),
                                             landed.splitlines(), n=0)
             if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    changed = [l[1:].strip() for l in hunks]
    only_imports = all(c.startswith(("import ", "from ", "#")) or not c
                       for c in changed)
    note = ("no symbols stripped; imports repointed to their `casim.engine` "
            "paths (same objects — the shim re-exports by identity)")
    if not only_imports:
        note += "; results path made location-independent + `__main__`-guarded"
    return note


def main() -> int:
    dry = "--dry-run" in sys.argv
    m = yaml.safe_load(open(MANIFEST, encoding="utf-8"))
    recs = {r["target"]: r for r in m["modules"]
            if r["sector"] == "particles" and r.get("migrated")}
    text = open(README, encoding="utf-8").read()
    out, n = [], 0
    for line in text.splitlines(keepends=True):
        mo = re.match(r"^\|([^|]*)\|([^|]*)\|\s*`([^`]+)`\s*\|([^|]*)\|\s*$", line)
        if mo and mo.group(3) in recs:
            reason = classify(recs[mo.group(3)])
            new = (f"|{mo.group(1)}|{mo.group(2)}| `{mo.group(3)}` "
                   f"| {reason} |\n")
            if new != line:
                n += 1
                line = new
        out.append(line)
    print(f"  {n} row(s) corrected")
    if not dry and n:
        open(README, "w", encoding="utf-8").write("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
