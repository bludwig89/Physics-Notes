"""`findings-index.md` + the finding-number audit — roadmap C8.1 / **C8.2**.

Two jobs.

**The index** is the P0.3 upgrade the old scraper never got: each row now carries
the supersession annotation from ``docs/theory/supersessions.yaml`` and the count
of registry records that verify the finding, so a reader can see at a glance
whether a finding is live, partially superseded, or has no test at all.

**The audit (C8.2)** is the one this project has earned. Finding numbers have
collided three times across concurrent sessions (F110, F129, F262 by the
roadmap's count) and the tree currently holds **ten** numbers used twice. A
`casim index` that cannot see that is decorative, so:

* every collision and every gap must be declared in
  ``docs/design/finding-numbers.yaml`` with a reason;
* anything undeclared **fails the check** — which is how the fourth collision
  becomes loud instead of archaeological;
* declared-but-``unreviewed`` entries are counted and printed on every run. They
  are not silently blessed: the file records both titles and asks a physics owner
  to decide. Detecting a collision is not the same as resolving one, and this
  module deliberately does not pretend otherwise.
"""
from __future__ import annotations

import os
import re

import yaml

from .common import HEADER_NOTE, clean, esc, read_head, truncate

FINDING_FILE_RE = re.compile(r"^F(\d+)([a-z]?)-")
NUMBERS_FILE = os.path.join("docs", "design", "finding-numbers.yaml")


# ---------------------------------------------------------------------------
def _extract_summary(content: str, fname: str) -> str:
    title_m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if title_m:
        title = clean(title_m.group(1))
        parts = re.split(r'\s*[—–]\s*|:\s+', title, maxsplit=1)
        if len(parts) > 1 and parts[1].strip():
            return truncate(parts[1].strip())
        if title:
            return truncate(title)
    sum_m = re.search(r'##\s+Summary\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if sum_m:
        text = clean(sum_m.group(1))
        if text:
            return truncate(re.split(r'(?<=[.!?])\s', text)[0])
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '**', '`', '>', '-', '|', '$',
                                        '!', '*', '=', '[')):
            continue
        if re.match(r'^\d{4}-\d{2}-\d{2}', line):
            continue
        return truncate(clean(line))
    return fname


def _ledger_finding_status(repo: str) -> dict[str, tuple[str, str]]:
    """{finding id -> (kind, ledger record id)} from the supersession ledger.

    A finding named as a record's ``superseded`` subject is annotated; a finding
    that *does* the superseding is annotated too, in the other direction, because
    both facts change how a reader should treat the file.
    """
    path = os.path.join(repo, "docs", "theory", "supersessions.yaml")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        led = yaml.safe_load(fh) or {}
    out: dict[str, tuple[str, str]] = {}
    for rec in led.get("supersessions") or []:
        rid = rec.get("id", "")
        for f in rec.get("superseded_findings") or rec.get("superseded") or ():
            if isinstance(f, str):
                out[f.upper()] = ("superseded", rid)
        for f in rec.get("superseding_findings") or rec.get("superseding") or ():
            if isinstance(f, str):
                out.setdefault(f.upper(), ("supersedes", rid))
        # The schema in use names findings inside `finding:`/`by:` too.
        sub, by = rec.get("finding"), rec.get("by")
        if isinstance(sub, str):
            out[sub.upper()] = ("superseded", rid)
        if isinstance(by, str):
            out.setdefault(by.upper(), ("supersedes", rid))
    return out


def _tests_per_finding() -> dict[str, int]:
    try:
        from casim.tests import registry as treg
    except Exception:                                        # pragma: no cover
        return {}
    counts: dict[str, int] = {}
    for r in treg.all_records():
        for f in r.findings:
            counts[f.upper()] = counts.get(f.upper(), 0) + 1
    return counts


# ---------------------------------------------------------------------------
def audit_numbers(repo: str) -> dict:
    """Collisions and gaps in `findings/`, against the declared exceptions."""
    fdir = os.path.join(repo, "findings")
    by_num: dict[int, list[str]] = {}
    unnumbered: list[str] = []
    variants: dict[str, list[str]] = {}          # F34b-style letter suffixes
    for fname in sorted(os.listdir(fdir)):
        if not fname.endswith(".md"):
            continue
        m = FINDING_FILE_RE.match(fname)
        if not m:
            unnumbered.append(fname)
            continue
        if m.group(2):
            # `F34b-...` is a follow-on to F34, NOT a second use of the number.
            # Folding it into 34 would invent a duplicate; ignoring it would
            # hide the file. It gets its own key.
            variants.setdefault(f"{int(m.group(1))}{m.group(2)}", []).append(fname)
            continue
        by_num.setdefault(int(m.group(1)), []).append(fname)

    declared_path = os.path.join(repo, NUMBERS_FILE)
    declared = {}
    if os.path.exists(declared_path):
        with open(declared_path, encoding="utf-8") as fh:
            declared = yaml.safe_load(fh) or {}
    dup_declared = {int(k): v for k, v in
                    (declared.get("duplicates") or {}).items()}
    gap_declared = {int(k): v for k, v in (declared.get("gaps") or {}).items()}
    range_declared = declared.get("gap_ranges") or []

    def _gap_explained(n: int) -> str | None:
        if n in gap_declared:
            return gap_declared[n].get("reason", "declared")
        for rng in range_declared:
            if int(rng["from"]) <= n <= int(rng["to"]):
                return rng.get("reason", "declared range")
        return None

    nums = sorted(by_num)
    duplicates = {n: v for n, v in by_num.items() if len(v) > 1}
    gaps = [n for n in range(min(nums), max(nums) + 1) if n not in by_num] \
        if nums else []

    undeclared_dups = sorted(n for n in duplicates if n not in dup_declared)
    undeclared_gaps = sorted(n for n in gaps if _gap_explained(n) is None)
    unreviewed = sorted(n for n, v in dup_declared.items()
                        if (v or {}).get("status") == "unreviewed"
                        and n in duplicates)
    declared_unnumbered = declared.get("unnumbered") or {}
    undeclared_unnumbered = sorted(f for f in unnumbered
                                   if f not in declared_unnumbered)
    # A declared duplicate that no longer exists is stale bookkeeping: it means
    # someone renumbered and left the exception behind, which quietly re-arms
    # the collision it was hiding.
    stale_dups = sorted(n for n in dup_declared if n not in duplicates)

    return {
        "max": max(nums) if nums else 0,
        "files": sum(len(v) for v in by_num.values()) + len(unnumbered)
        + sum(len(v) for v in variants.values()),
        "numbers": len(nums),
        "variants": variants,
        "unnumbered": unnumbered,
        "duplicates": duplicates,
        "gaps": gaps,
        "undeclared_duplicates": undeclared_dups,
        "undeclared_gaps": undeclared_gaps,
        "undeclared_unnumbered": undeclared_unnumbered,
        "stale_declared_duplicates": stale_dups,
        "unreviewed_duplicates": unreviewed,
        "declared_gap_reasons": {n: _gap_explained(n) for n in gaps},
    }


# ---------------------------------------------------------------------------
def render(repo: str) -> tuple[str, str, int]:
    fdir = os.path.join(repo, "findings")
    ledger = _ledger_finding_status(repo)
    test_counts = _tests_per_finding()
    audit = audit_numbers(repo)

    rows = []
    for fname in sorted(os.listdir(fdir)):
        if not fname.endswith(".md"):
            continue
        content = read_head(os.path.join(fdir, fname), 2000)
        m = FINDING_FILE_RE.match(fname)
        fnum = f"F{int(m.group(1))}{m.group(2)}" if m else "?"
        summary = _extract_summary(content, fname)
        test_m = re.search(r'(\d+)/(\d+)\s*PASS', content)
        tests = f"{test_m.group(1)}/{test_m.group(2)} PASS" if test_m else ""
        # C8.1: annotations the old scraper could not produce.
        marks = []
        kind_rid = ledger.get(fnum.upper())
        if kind_rid:
            marks.append(f"{'SUPERSEDED' if kind_rid[0] == 'superseded' else 'supersedes'}"
                         f" ({kind_rid[1]})")
        n_tests = test_counts.get(fnum.upper(), 0)
        marks.append(f"{n_tests} test rec" if n_tests else "**no test record**")
        if m and int(m.group(1)) in audit["duplicates"]:
            marks.append("number reused")
        rows.append((fnum, fname.replace('.md', ''), summary, tests,
                     "; ".join(marks)))

    lines = [
        "# Findings Index", "", HEADER_NOTE,
        "*One line per finding; full files in `findings/`. `Status` joins the "
        "supersession ledger and the test registry (D9): how many registry "
        "records verify the finding, whether the ledger touches it, and whether "
        "its number is shared with another file (see "
        "`docs/design/finding-numbers.yaml`).*", "",
        "| # | File | Summary | Tests | Status |",
        "|---|------|---------|-------|--------|",
    ]
    for fnum, slug, summary, tests, marks in rows:
        lines.append(f"| {fnum} | `{slug}` | {esc(summary)} | {tests} | "
                     f"{esc(marks)} |")
    lines += [
        "",
        f"*{len(rows)} finding file(s) over {audit['numbers']} distinct numbers; "
        f"max F{audit['max']}. {len(audit['duplicates'])} number(s) used twice, "
        f"{len(audit['gaps'])} gap(s) — all declared in "
        f"`docs/design/finding-numbers.yaml`; `casim index --check` fails on any "
        f"that is not.*",
        "",
    ]
    return "findings-index.md", "\n".join(lines), len(rows)
