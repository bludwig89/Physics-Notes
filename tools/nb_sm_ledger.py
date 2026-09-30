#!/usr/bin/env python3
"""Notebook x Standard Model cross-check -- ledger and readiness tool.

Reads the (concurrently edited) reconstruction ledger
``docs/theory/notebook-reconstruction-index.md`` read-only, and maintains
``docs/theory/notebook-sm-crosscheck-ledger.md``: one row per page-group
section, with readiness computed from the reconstruction's build statuses and
the cross-check verdict columns preserved across refreshes.

Protocol: ``docs/theory/notebook-sm-crosscheck-protocol.md``.

Usage (from the repo root):
    python3 tools/nb_sm_ledger.py --refresh          # (re)build the ledger, keep verdicts
    python3 tools/nb_sm_ledger.py --status           # print readiness per batch, next up
    python3 tools/nb_sm_ledger.py --set pp.62-72 --relation CONFLICTS-DATA \
        --field EXCLUDED --writeup notebook-sm-crosscheck-06-....md
                                                     # record a checked section

Readiness values:
    BLOCKED(n)  n builds in the section are not yet disposed by the reconstruction
    READY       all builds disposed; not yet cross-checked
    CHECKED     cross-checked against the current reconstruction statuses
    STALE       cross-checked, but a build status has since changed -> re-run
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import hashlib
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
THEORY = os.path.join(REPO, "docs", "theory")
INDEX = os.path.join(THEORY, "notebook-reconstruction-index.md")
LEDGER = os.path.join(THEORY, "notebook-sm-crosscheck-ledger.md")

NOT_DISPOSED = ("PENDING", "IN-PROGRESS", "CONTAMINATED-DEFER-TO-SUBAGENT")
COLS = ["Key", "Section", "NB-IDs", "Batch", "Readiness", "Checked-against",
        "SM relation", "Field status", "Write-up", "Date"]
KEEP = ["Checked-against", "SM relation", "Field status", "Write-up", "Date"]

_SEC = re.compile(r"^##\s+(Pages?)\s+([0-9][0-9–\-]*)\s+—\s+(.*?)\s*$")
_ROW = re.compile(r"^\|\s*(NB-\d{3})\s*\|(.*)\|\s*$")


def _key(pages: str) -> str:
    return "pp." + pages.replace("–", "-")


def parse_index(path: str = INDEX):
    """Return list of sections: dict(key, title, builds=[(id, status)])."""
    sections, cur = [], None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = _SEC.match(line)
            if m:
                cur = {"key": _key(m.group(2)), "title": m.group(3).strip(),
                       "builds": []}
                sections.append(cur)
                continue
            if line.startswith("## ") and cur is not None and not _SEC.match(line):
                cur = None  # Summary / Errata / etc. end the section tables
                continue
            r = _ROW.match(line.rstrip("\n"))
            if r and cur is not None:
                cells = [c.strip() for c in r.group(2).split("|")]
                cur["builds"].append((r.group(1), cells[-1]))
    return [s for s in sections if s["builds"]]


def batch_map():
    """NB-ID -> batch label, from the '## NB-xxx' headings of each batch write-up."""
    out = {}
    for f in sorted(glob.glob(os.path.join(THEORY, "notebook-reconstruction-[0-9]*.md"))):
        label = re.match(r"notebook-reconstruction-(\d+[a-z]?)", os.path.basename(f)).group(1)
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("## ") or line.startswith("### "):
                    for a, b in re.findall(r"NB-(\d{3})(?:\s*[–\-/]\s*(?:NB-)?(\d{3}))?", line):
                        lo = int(a)
                        hi = int(b) if b else lo
                        for n in range(lo, hi + 1):
                            out.setdefault(f"NB-{n:03d}", label)
    return out


def disposed(status: str) -> bool:
    return not any(status.upper().startswith(p) for p in NOT_DISPOSED)


def status_hash(builds) -> str:
    s = ";".join(f"{i}:{st}" for i, st in builds)
    return hashlib.sha1(s.encode()).hexdigest()[:8]


def id_range(builds) -> str:
    ids = [b[0] for b in builds]
    return ids[0] if len(ids) == 1 else f"{ids[0]}–{ids[-1][3:]}"


def read_ledger():
    rows = {}
    if not os.path.exists(LEDGER):
        return rows
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("| pp."):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) == len(COLS):
                    rows[cells[0]] = dict(zip(COLS, cells))
    return rows


def build_rows():
    old = read_ledger()
    bmap = batch_map()
    rows = []
    for s in parse_index():
        b = s["builds"]
        pend = sum(1 for _, st in b if not disposed(st))
        tally = {}
        for i, _ in b:
            if i in bmap:
                tally[bmap[i]] = tally.get(bmap[i], 0) + 1
        # a batch that merely mentions one or two of a large section's builds in a
        # heading (a back-reference) is not where the section was disposed
        batches = sorted(k for k, v in tally.items() if v >= 0.25 * len(b)) or ["—"]
        h = status_hash(b)
        prev = old.get(s["key"], {})
        row = {"Key": s["key"], "Section": s["title"], "NB-IDs": id_range(b),
               "Batch": ",".join(batches)}
        for k in KEEP:
            row[k] = prev.get(k, "") or ""
        chk = row["Checked-against"]
        if pend:
            row["Readiness"] = f"BLOCKED({pend})"
        elif chk and chk != h:
            row["Readiness"] = "STALE"
        elif chk:
            row["Readiness"] = "CHECKED"
        else:
            row["Readiness"] = "READY"
        row["_hash"] = h
        rows.append(row)
    return rows


HEADER = """# Notebook × SM Cross-Check — Ledger

*Tracker for `notebook-sm-crosscheck-protocol.md`. One row per page-group section of
`notebook-reconstruction-index.md`. **Generated** by `tools/nb_sm_ledger.py --refresh`, which
recomputes Key/Section/NB-IDs/Batch/Readiness from the reconstruction ledger and **preserves**
the verdict columns. Edit verdict columns by hand or with `--set`; do not hand-edit Readiness.*

*Readiness: `BLOCKED(n)` = n builds not yet disposed by the reconstruction · `READY` = can be
cross-checked · `CHECKED` = done against current statuses · `STALE` = a build status changed
since the check (re-run). `Checked-against` is a hash of the section's build statuses at check
time. SM relation / Field status vocabulary: protocol §4.*

"""


def write_ledger(rows):
    now = _dt.datetime.now().strftime("%Y-%m-%d - %H:%M")
    counts = {}
    for r in rows:
        k = re.sub(r"\(.*\)", "", r["Readiness"])
        counts[k] = counts.get(k, 0) + 1
    tally = " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    lines = [HEADER, f"Last refreshed: {now} — {len(rows)} sections — {tally}", "",
             "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
    for r in rows:
        lines.append("| " + " | ".join(r[c] for c in COLS) + " |")
    with open(LEDGER, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def cmd_status(rows):
    by_batch = {}
    for r in rows:
        by_batch.setdefault(r["Batch"], []).append(r)
    print(f"{'batch':>6}  {'sections':>8}  readiness")
    nxt = None
    for b in sorted(by_batch, key=lambda x: (x == "—", x)):
        rs = by_batch[b]
        states = [r["Readiness"] for r in rs]
        print(f"{b:>6}  {len(rs):>8}  {', '.join(sorted(set(states)))}")
        if nxt is None and b != "—" and all(s in ("READY", "STALE", "CHECKED") for s in states) \
                and any(s in ("READY", "STALE") for s in states):
            nxt = b
    stale = [r["Key"] for r in rows if r["Readiness"] == "STALE"]
    if stale:
        print(f"\nSTALE (re-run first): {', '.join(stale)}")
    if nxt:
        keys = [r["Key"] for r in by_batch[nxt] if r["Readiness"] in ("READY", "STALE")]
        print(f"\nnext run: batch {nxt} -> sections {', '.join(keys)}")
    else:
        print("\nnext run: none ready")


def cmd_set(rows, key, relation, field, writeup):
    for r in rows:
        if r["Key"] == key:
            r["Checked-against"] = r["_hash"]
            r["Readiness"] = "CHECKED"
            if relation:
                r["SM relation"] = relation
            if field:
                r["Field status"] = field
            if writeup:
                r["Write-up"] = f"[{writeup.replace('notebook-sm-crosscheck-', '')}]({writeup})"
            r["Date"] = _dt.date.today().isoformat()
            return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--set", metavar="KEY", help="section key, e.g. pp.62-72")
    ap.add_argument("--relation")
    ap.add_argument("--field")
    ap.add_argument("--writeup")
    a = ap.parse_args(argv)
    rows = build_rows()
    if a.set:
        if not cmd_set(rows, a.set, a.relation, a.field, a.writeup):
            sys.exit(f"no section with key {a.set!r}")
        write_ledger(rows)
    elif a.refresh:
        write_ledger(rows)
    if a.status or not (a.set or a.refresh):
        cmd_status(rows)


if __name__ == "__main__":
    main()
