#!/usr/bin/env python3
"""Stamp supersession banners into the files docs/theory/supersessions.yaml names.

Roadmap P0.4. Idempotent: re-running updates an existing banner in place rather
than stacking a second one.

Why a docstring banner rather than a pytest marker? Because 166 of the 272
finding tests have no `def test_` at all — they are standalone scripts that
`casim test` classifies by scraping stdout. A marker would be invisible to
exactly the files that most need labelling. A banner in the module docstring is
readable by a human opening the file, greppable, parseable by the runner, and
works identically for both styles. Markers are added ON TOP where a `def test_`
exists, not instead.

Usage:
    python3 tools/apply_supersession_banners.py [--check]

`--check` reports what would change and exits 1 if anything is missing; that is
the mode the gate runs.
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")

# The banner ends with an explicit sentinel line so re-detection is exact.
# Matching "indented lines until something else" is not safe here: plenty of
# these docstrings are themselves indented, and an over-greedy pattern would
# silently swallow real content on the second run.
SENTINEL = "  See docs/theory/supersessions.yaml for the full record."

BANNER_RE = re.compile(
    r"\A\[(?:SUPERSEDED|PARTIALLY SUPERSEDED|HISTORICAL BASELINE)[^\]]*\]\n"
    r".*?" + re.escape(SENTINEL) + r"\n\n",
    re.DOTALL,
)
BANNER_START_RE = re.compile(
    r"\A\[(?:SUPERSEDED|PARTIALLY SUPERSEDED|HISTORICAL BASELINE)\b")

_LABEL = {
    "fully_superseded": "SUPERSEDED",
    "partially_superseded": "PARTIALLY SUPERSEDED",
    "historical_baseline": "HISTORICAL BASELINE",
}


def _wrap(text: str, width: int = 74, indent: str = "  ") -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(indent + cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(indent + cur)
    return lines


def build_banner(record: dict, entry: dict) -> str:
    """The banner text block, without trailing blank line."""
    label = _LABEL[entry["status"]]
    by = ", ".join(record["by"])
    head = (f"[{label} {record['date']} by {by} — ledger {record['id']}]"
            if entry["status"] != "historical_baseline"
            else f"[{label} {record['date']} — ledger {record['id']}]")
    out = [head]
    if entry.get("dead"):
        out += ["", "  DEAD:"] + _wrap(entry["dead"], indent="    ")
    if entry.get("live"):
        out += ["", "  STILL LIVE:"] + _wrap(entry["live"], indent="    ")
    if entry.get("replacement"):
        out += ["", f"  REPLACED BY: {entry['replacement']}"]
    if entry.get("note"):
        out += ["", "  NOTE:"] + _wrap(entry["note"], indent="    ")
    out += ["", SENTINEL, "", ""]
    return "\n".join(out)


def _docstring_span(src: str, path: str) -> tuple[int, int] | None:
    """Character span of the module docstring's CONTENT, or None."""
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError:
        return None
    if not tree.body:
        return None
    node = tree.body[0]
    if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)):
        return None
    lines = src.splitlines(keepends=True)
    offsets = [0]
    for ln in lines:
        offsets.append(offsets[-1] + len(ln))
    raw_start = offsets[node.lineno - 1] + node.col_offset
    raw_end = offsets[node.end_lineno - 1] + node.end_col_offset
    raw = src[raw_start:raw_end]
    quote = '"""' if raw.lstrip("rbuRBU").startswith('"""') else "'''"
    if quote not in raw:
        return None
    inner_start = raw_start + raw.index(quote) + 3
    inner_end = raw_end - 3
    if inner_end < inner_start:
        return None
    return inner_start, inner_end


def apply_to_file(path: str, banner: str, check: bool) -> str:
    """Returns one of: 'ok', 'added', 'updated', 'would-add', 'no-docstring'."""
    full = os.path.join(_REPO, path)
    with open(full, "r", encoding="utf-8") as fh:
        src = fh.read()

    span = _docstring_span(src, path)
    if span is None:
        return "no-docstring"
    start, end = span
    body = src[start:end]

    stripped = body.lstrip("\n")
    lead = body[:len(body) - len(stripped)]

    if BANNER_START_RE.match(stripped):
        m = BANNER_RE.match(stripped)
        if not m:                               # malformed; do not guess
            return "malformed-banner"
        if stripped[:m.end()] == banner:
            return "ok"
        new_body = lead + banner + stripped[m.end():]
        verb = "updated"
    else:
        new_body = lead + banner + stripped
        verb = "added"

    if check:
        return "would-add" if verb == "added" else "would-update"

    new_src = src[:start] + new_body + src[end:]
    try:
        ast.parse(new_src, filename=path)
    except SyntaxError as e:
        raise SystemExit(f"REFUSING to write {path}: banner broke parsing ({e})")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(new_src)
    return verb


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report only; exit 1 if any banner is missing or stale")
    args = ap.parse_args()

    with open(LEDGER, "r", encoding="utf-8") as fh:
        ledger = yaml.safe_load(fh)

    results: list[tuple[str, str]] = []
    for record in ledger["supersessions"]:
        for entry in record.get("tests") or []:
            if entry["status"] == "live":
                continue
            banner = build_banner(record, entry)
            results.append((entry["path"], apply_to_file(entry["path"], banner,
                                                         args.check)))

    counts: dict[str, int] = {}
    for path, status in sorted(results):
        counts[status] = counts.get(status, 0) + 1
        if status != "ok":
            print(f"  {status:18s} {path}")
    print(f"[supersessions] {len(results)} files: " +
          ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))

    stale = [s for _, s in results if s not in ("ok", "added", "updated")]
    if args.check and stale:
        print("\nRun `python3 tools/apply_supersession_banners.py` to fix.")
        return 1
    if stale and not args.check:
        print("\nSome files could not be stamped automatically (see above).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
