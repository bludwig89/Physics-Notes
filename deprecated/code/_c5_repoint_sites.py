#!/usr/bin/env python3
"""C5 — repoint `casim.constants` Site() paths at the migrated particles targets.

A `Site("ca-simulation/ca_nuclear.py", "G_A", kind="import")` record asserts
*that file imports G_A from the registry*. After migration the assertion is
false at the old path — `ca-simulation/ca_nuclear.py` is a shim that imports
nothing from `casim.constants` — and true at the new one. C3, C4 and C6 each
repointed their own sector's records the same way (see the `src/casim/engine/...`
Site paths already in `constants/*.py`); this does the particles sector.

Only paths belonging to a **migrated particles record** are touched, so it
cannot disturb another live session's sector.
"""
from __future__ import annotations

import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
CONST_DIR = os.path.join(_REPO, "src", "casim", "constants")


def main() -> int:
    dry = "--dry-run" in sys.argv
    m = yaml.safe_load(open(MANIFEST, encoding="utf-8"))
    moves = {r["source"]: r["target"] for r in m["modules"]
             if r["sector"] == "particles" and r.get("migrated")}
    if not moves:
        print("no migrated particles records")
        return 1

    total = 0
    for fn in sorted(os.listdir(CONST_DIR)):
        if not fn.endswith(".py"):
            continue
        path = os.path.join(CONST_DIR, fn)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        new = text
        n = 0
        for src, tgt in moves.items():
            # Only inside a Site("...") literal — never a prose mention.
            pat = re.compile(r'(Site\(\s*")' + re.escape(src) + r'(")')
            new, k = pat.subn(lambda mo: mo.group(1) + tgt + mo.group(2), new)
            n += k
        if n:
            total += n
            print(f"  {'dry ' if dry else 'ok  '} {fn:<20s} {n} Site path(s)")
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
    print(f"\n  {total} Site path(s) repointed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
