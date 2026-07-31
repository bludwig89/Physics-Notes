#!/usr/bin/env python3
"""C5 — migrate the `sector: particles` records, byte-faithfully.

Why this exists instead of a plain loop over `tools/migrate_module.py`:
the sandbox mount **refuses `unlink`**, so `migrate_module.py`'s journal
cannot roll back — an abort would orphan the backup and the target and leave
the next attempt refusing on "target already exists". C4 hit the same wall
and took the same route (see `docs/status/C4-completion-overview.md`).

So this driver performs migrate_module.py's steps 2-5 and 7 using
**migrate_module.py's own templates, imported not copied**, and does only
overwrite-and-create operations — never a delete. Step 6 (re-run + diff) is
lifted out and done once per sector afterwards, because `ca_dirac.py` alone
names 29 test files and the per-module loop would blow the shell timeout.

The safety argument for skipping the per-module diff is not "trust me": every
one of the 21 records has `dead_symbols: []`, so the cleaned copy is
**byte-identical to the original**. Nothing is stripped, nothing is rewritten;
only the import path changes. Drift from the move itself is impossible by
construction, and this script asserts that byte-identity per file.
"""
from __future__ import annotations

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from migrate_module import (  # noqa: E402  — the templates, imported not copied
    BACKUP_DIR,
    BACKUP_HEADER,
    SHIM,
    _REPO,
    _now,
    dotted_of,
    index_backup,
    load_manifest,
    stamp,
    strip_symbols,
)

SECTOR = "particles"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def main() -> int:
    dry = "--dry-run" in sys.argv
    m = load_manifest()
    recs = [r for r in m["modules"] if r["sector"] == SECTOR]
    claim = (m.get("claims") or {}).get(SECTOR)
    if not claim:
        print(f"REFUSING: sector {SECTOR!r} is not claimed in the manifest. "
              f"The roadmap's concurrency rule is not optional.")
        return 1
    print(f"claim: {claim['session']} / {claim['phase']} / {claim['claimed']}")
    print(f"{len(recs)} record(s) in sector {SECTOR}\n")

    done, skipped, failed = [], [], []
    for rec in recs:
        src = os.path.join(_REPO, rec["source"])
        tgt = os.path.join(_REPO, rec["target"])
        backup = os.path.join(BACKUP_DIR, os.path.basename(rec["source"]))
        dead = list(rec.get("dead_symbols") or [])
        protected = set(rec.get("protected_symbols") or [])

        if rec.get("migrated"):
            print(f"  skip  {rec['id']:<38s} already migrated {rec['migrated']}")
            skipped.append(rec["id"])
            continue
        if not os.path.exists(src):
            print(f"  FAIL  {rec['id']:<38s} source missing")
            failed.append(rec["id"])
            continue
        clash = sorted(set(dead) & protected)
        if clash:
            print(f"  FAIL  {rec['id']:<38s} accepted-dead ∩ ledger-retained: {clash}")
            failed.append(rec["id"])
            continue

        with open(src, encoding="utf-8") as fh:
            original = fh.read()
        if original.lstrip().startswith('"""DEPRECATED shim'):
            print(f"  FAIL  {rec['id']:<38s} source is already a shim — refusing "
                  f"to back up a shim over the original")
            failed.append(rec["id"])
            continue

        cleaned, stripped = strip_symbols(original, dead, rec["source"])
        # The invariant this driver rests on. If a future record accepts a dead
        # symbol, the byte-identity argument evaporates and that record must go
        # through migrate_module.py with its own baseline diff instead.
        if not dead and cleaned != original:
            print(f"  FAIL  {rec['id']:<38s} no dead_symbols but content changed")
            failed.append(rec["id"])
            continue
        if dead:
            print(f"  FAIL  {rec['id']:<38s} accepts {len(dead)} dead symbol(s) — "
                  f"use migrate_module.py so the baselines are diffed")
            failed.append(rec["id"])
            continue

        when = _now()
        header = BACKUP_HEADER.format(
            source=rec["source"], when=when, target=rec["target"], mid=rec["id"],
            stripped="(nothing)",
            reason=(rec["ledger"][0]["record"] + " — " + rec["ledger"][0]["note"][:80])
            if rec["ledger"] else "D6 consolidation; no symbols removed")
        shim = SHIM.format(dotted=dotted_of(rec["target"]),
                           source=rec["source"], phase=rec["phase"])

        if dry:
            print(f"  dry   {rec['id']:<38s} -> {rec['target']}")
            continue

        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        for path, content in ((backup, header + original),
                              (tgt, cleaned),
                              (src, shim)):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)

        # Prove the three writes landed as intended before stamping.
        with open(tgt, encoding="utf-8") as fh:
            landed = fh.read()
        with open(backup, encoding="utf-8") as fh:
            backed = fh.read()
        if landed != original:
            print(f"  FAIL  {rec['id']:<38s} target is NOT byte-identical")
            failed.append(rec["id"])
            continue
        if not backed.endswith(original):
            print(f"  FAIL  {rec['id']:<38s} backup does not end in the original")
            failed.append(rec["id"])
            continue

        stamp(rec["id"], when)
        index_backup(rec, when, stripped)
        print(f"  ok    {rec['id']:<38s} -> {rec['target']}  [{sha(original)}]")
        done.append(rec["id"])

    print(f"\n  migrated {len(done)}   skipped {len(skipped)}   failed {len(failed)}")
    if failed:
        print("  FAILED: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
