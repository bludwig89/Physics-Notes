#!/usr/bin/env python3
"""Triage drifting baselines against the supersession ledger (2026-07-31).

The question this answers
------------------------
The C7.5 arming pass left 26 records failing on numeric drift. Some of those
numbers are wrong because something broke; others are wrong because the model
*improved* and the committed value was never re-blessed. Those two look identical
in a diff, and treating them the same is how a project learns to ignore its own
baseline checks.

So: for each drifting record, does the supersession ledger name any of the
findings its test claims? If it does, the drift is a **supersession candidate** —
the physics under it moved on purpose. If it does not, the drift is a
**regression candidate** and wants a code answer, not a bookkeeping one.

This tool only *proposes*. Writing a `baselines:` entry into
`docs/theory/supersessions.yaml` is a human decision, and `candidate` entries do
not suppress a failure — see `casim.tests.ledger` for why that asymmetry matters.

Usage
-----
    python3 tools/triage_baselines.py               # the report
    python3 tools/triage_baselines.py --yaml        # paste-ready ledger entries
    python3 tools/triage_baselines.py --undeclared  # only the not-yet-recorded
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

JOURNAL = os.path.join(_REPO, "test-results", "arming-journal.json")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")


def _committed(rel: str) -> str:
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                         cwd=_REPO, capture_output=True, text=True)
    return out.stdout.strip() or "?"


def triage() -> list[dict]:
    from casim.tests import registry as treg
    from casim.tests import ledger as led

    with open(JOURNAL, encoding="utf-8") as fh:
        journal = json.load(fh)["records"]
    with open(LEDGER, encoding="utf-8") as fh:
        ledger_doc = yaml.safe_load(fh) or {}
    records = [(r.get("id", ""), str(r)) for r in ledger_doc.get("supersessions") or []]
    idx = {r.id: r for r in treg.all_records()}

    rows: list[dict] = []
    for rid, entry in sorted(journal.items()):
        if entry.get("status") not in ("FAIL", "STALE"):
            continue
        rec = idx.get(rid)
        findings = list(rec.findings) if rec else []
        # Which ledger records mention any finding this test claims?
        hits = [lid for lid, blob in records
                if any(re.search(rf"\b{f}\b", blob) for f in findings)]
        artifacts = entry.get("results") or []
        declared = [led.status_of(a) for a in artifacts]
        rows.append({
            "id": rid,
            "artifacts": artifacts,
            "committed": _committed(artifacts[0]) if artifacts else "?",
            "findings": findings,
            "ledger_records": hits,
            "declared": [d.status if d else None for d in declared],
            "status": entry["status"],
            "detail": entry.get("detail", "")[:120],
        })
    return rows


_YAML_TEMPLATE = """      - path: {path}
        status: candidate
        committed: {committed}
        reason: "TRIAGE {ledger}: the test claims {findings}, which this record
                 touches, and a real run drifts. Reason not yet written — replace
                 this line with the physics before promoting to stale_by_design."
        clears_by: "Read the drifted values and decide: superseded by this record
                    (-> stale_by_design) or a regression (-> fix the code)."
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaml", action="store_true",
                    help="emit paste-ready `baselines:` entries for the "
                         "undeclared supersession candidates")
    ap.add_argument("--undeclared", action="store_true",
                    help="only rows with no ledger `baselines:` entry yet")
    args = ap.parse_args()

    if not os.path.exists(JOURNAL):
        print("no arming journal — run tools/arm_test_registry.py first",
              file=sys.stderr)
        return 2

    rows = triage()
    if args.undeclared:
        rows = [r for r in rows if not any(r["declared"])]

    if args.yaml:
        by_ledger: dict[str, list[dict]] = {}
        for r in rows:
            if not r["ledger_records"] or any(r["declared"]):
                continue
            by_ledger.setdefault(r["ledger_records"][0], []).append(r)
        for lid, rs in sorted(by_ledger.items()):
            print(f"# --- add under {lid} ---\n    baselines:")
            for r in rs:
                print(_YAML_TEMPLATE.format(
                    path=r["artifacts"][0], committed=r["committed"],
                    ledger=lid, findings=" ".join(r["findings"][:4]) or "—"))
        return 0

    sup = [r for r in rows if r["ledger_records"]]
    reg = [r for r in rows if not r["ledger_records"]]
    print(f"\nbaseline triage   {len(rows)} drifting record(s)")
    print(f"  supersession candidates   {len(sup)}  (a ledger record names their "
          f"findings)")
    print(f"  regression candidates     {len(reg)}  (no ledger link — suspect the "
          f"code)")

    print("\nsupersession candidates")
    print(f"  {'record':40s} {'committed':11s} {'declared':16s} ledger")
    for r in sup:
        d = ", ".join(x for x in r["declared"] if x) or "—"
        print(f"  {r['id']:40s} {r['committed']:11s} {d:16s} "
              f"{','.join(x.split('-')[0] for x in r['ledger_records'])}")

    print("\nregression candidates")
    for r in reg:
        print(f"  {r['id']:40s} {r['committed']:11s} {r['detail'][:70]}")

    undeclared = [r for r in sup if not any(r["declared"])]
    if undeclared:
        print(f"\n{len(undeclared)} supersession candidate(s) have no ledger "
              f"entry yet — `--yaml` emits templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
