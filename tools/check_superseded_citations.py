#!/usr/bin/env python3
"""A supersession must reach the documents that CITE the finding, not just the finding.

WHY THIS EXISTS
===============
`docs/theory/supersessions.yaml` records supersessions and
`apply_supersession_banners.py` propagates each one INTO the superseded file, where
`test_no_orphan_banners` keeps the two in step. That machinery is sound and it is
also only half the loop: nothing propagated a supersession OUTWARD, into the rubric
rows, ledgers and claim cards that cite the finding as evidence. So a document could
go on grading a row against a reading that had been replaced months earlier, and
every check stayed green.

That is not hypothetical. Completeness rubric row B9 ("running of alpha, EW
couplings") cited **F115** as its electroweak evidence for three consecutive reports
(2026-08-02, -04, -07) while **F138** (2026-06-11) and **F231** (2026-07-02) had
superseded that reading. Two independent failures stacked:

  1. F115 had no ledger entry at all, so there was no banner and nothing for
     `test_no_orphan_banners` to find. Fixed by S20 (2026-08-17).
  2. Even once it existed, nothing looked at the citing side. `check_claims.py`
     rule 4 fires only when a `live` card rests on WHOLLY superseded ground, and
     deliberately not on partials -- correct for that rule, and it means the
     common case (a partial supersession, cited without its replacement) has no
     owner. This file is that owner.

THE RULE
========
A citation unit that names a superseded finding must ALSO name what replaced it,
or acknowledge the supersession explicitly. Three ways to satisfy it:

  * name a replacement from the record's `by:` list in the same unit;
  * carry an acknowledgement marker in the same unit -- the established convention
    is a warning sign next to the F-number, e.g. "F251 (superseded)", or the
    ledger id "S12-..."; or
  * (claim cards only) name the ledger record in `supersessions:` front matter.

A "unit" is deliberately small so the check means something: one markdown TABLE ROW
for rubric and ledger documents, and the front-matter block for a claim card. Whole
files are not units -- a supersession acknowledged in a footnote 400 lines from the
row that gets it wrong is not an acknowledgement, and that is precisely how B9 read.

WHY A RATCHET AND NOT A FLAT FAIL
=================================
The rubric/ledger surface is held at ZERO and fails hard: those are the documents
that grade the model, they were the ones that got it wrong, and there were only five
occurrences to clear. The claim-card surface carries a counted, falling ceiling: 17
cards cite a superseded finding without its replacement, and most are `open` or
`withdrawn` cards where the citation is a historical record rather than a live
grade. Blocking on all 17 at once would mean either a rushed sweep or a disabled
check, and the repo has learned which of those actually happens.

Usage:
    python3 tools/check_superseded_citations.py [--ratchet-update] [--verbose]

Exit 0 clean, 1 on any violation or a ratchet rise.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")
CLAIMS_DIR = os.path.join(_REPO, "docs", "claims")

# Rubric/ledger documents: held at zero. Add new grading documents here.
#
# Only the CURRENT completeness report is graded. Superseded reports are frozen
# records of what a past sweep concluded -- rewriting one to satisfy a check
# invented afterwards would be falsifying the history the audit trail exists to
# preserve, the same reason `supersessions.yaml` never rewrites a finding. The
# newest report is resolved by filename date so this follows the next sweep
# without an edit.
ROW_DOCS_GLOB_NEWEST = "docs/status/completeness-*.md"
ROW_DOCS = (
    "docs/status/open-derivations.md",
)

# Declared debt. May fall, never rise (`--ratchet-update` rewrites downward).
_CEILINGS = {
    "claim_cards_uncited_replacement": 17,
}

_FN = re.compile(r"\bF\d{1,3}[a-z]?\b")
# The acknowledgement vocabulary. Kept deliberately small and explicit: a unit
# either points at the successor or says the word.
_ACK = re.compile(r"⚠|supersed|superced|retract|deprecat|\bS\d{1,2}-")


def load_ledger(path: str = LEDGER) -> dict:
    """``{superseded finding -> {"by": {...}, "records": {...}}}``.

    Parsed with yaml rather than by regex: this file is the authority, a
    mis-parse here silently disarms the check, and it is already valid yaml that
    `test_supersession_ledger.py` gates.
    """
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    dead: dict[str, dict] = {}
    for rec in doc.get("supersessions") or []:
        for f in rec.get("superseded") or []:
            if not _FN.fullmatch(str(f)):
                continue                      # D-ids: methodology records
            e = dead.setdefault(f, {"by": set(), "records": set()})
            e["by"] |= {str(b) for b in (rec.get("by") or []) if _FN.fullmatch(str(b))}
            e["records"].add(rec["id"])
    return dead


def _unit_ok(cited: set[str], text: str, f: str, dead: dict,
             declared: set[str] | None = None) -> bool:
    e = dead[f]
    if e["by"] & cited:
        return True
    if declared and e["records"] & declared:
        return True
    return bool(_ACK.search(text))


def scan_rows(dead: dict) -> list[tuple[str, int, str, list[str]]]:
    """Markdown table rows in the grading documents."""
    newest = sorted(glob.glob(os.path.join(_REPO, ROW_DOCS_GLOB_NEWEST)))[-1:]
    paths = newest + [os.path.join(_REPO, p) for p in ROW_DOCS]
    out = []
    for path in paths:
        for path in [path]:
            rel = os.path.relpath(path, _REPO)
            with open(path, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if not line.lstrip().startswith("|"):
                        continue
                    cited = set(_FN.findall(line))
                    for f in sorted(cited & dead.keys()):
                        if not _unit_ok(cited, line, f, dead):
                            out.append((rel, n, f, sorted(dead[f]["by"])))
    return out


def scan_claim_cards(dead: dict) -> list[tuple[str, int, str, list[str]]]:
    """Claim-card front matter: `findings:` against `supersessions:`."""
    out = []
    for path in sorted(glob.glob(os.path.join(CLAIMS_DIR, "CL*.md"))):
        rel = os.path.relpath(path, _REPO)
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue                          # check_claims.py owns malformed fm
        cited = {str(x) for x in (fm.get("findings") or [])}
        declared = {str(x) for x in (fm.get("supersessions") or [])}
        for f in sorted(cited & dead.keys()):
            if not _unit_ok(cited, m.group(1), f, dead, declared):
                out.append((rel, 1, f, sorted(dead[f]["by"])))
    return out


def selftest() -> bool:
    """The B9 regression, as a fixture. This check exists because of this row.

    Reproduces the shape completeness-2026-08-07 carried for three reports -- row
    B9 citing F115 with neither F138 nor F231 and no acknowledgement -- and
    requires the matcher to FIRE on it, then to fall silent once the replacement
    is named. A checker that cannot be shown failing is not evidence.
    """
    dead = {"F115": {"by": {"F138", "F231"}, "records": {"S20-x"}}}
    bad = "| B9 | Running of $\\alpha$, EW couplings | QUANT | F251, F261, F115 |"
    good = "| B9 | Running of $\\alpha$, EW couplings | QUANT | F261, F138, F231, F115 |"
    ackd = "| B9 | ... | F115 (superseded, see S20) |"
    cases = [(bad, False), (good, True), (ackd, True)]
    ok = True
    for text, want in cases:
        got = _unit_ok(set(_FN.findall(text)), text, "F115", dead)
        if got is not want:
            print(f"  [selftest FAIL] expected ok={want}, got {got}: {text[:60]}")
            ok = False
    print(f"  [selftest] {'PASS' if ok else 'FAIL'} — 3 cases "
          f"(bare citation fires, replacement named clears, marker clears)")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratchet-update", action="store_true",
                    help="rewrite the ceiling to the current count, downward only")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    dead = load_ledger()
    rows = scan_rows(dead)
    cards = scan_claim_cards(dead)
    errs: list[str] = []

    print(f"[superseded-citations] {len(dead)} superseded finding(s) in the ledger; "
          f"grading documents held at zero, claim cards ratcheted")

    if not selftest():
        errs.append("selftest failed — the matcher does not fire on the B9 "
                    "regression it exists to catch")

    if rows:
        errs.append(f"{len(rows)} grading-document row(s) cite a superseded "
                    f"finding without its replacement or an acknowledgement:")
        for rel, n, f, by in rows:
            errs.append(f"    {rel}:{n} cites {f} — replaced by "
                        f"{', '.join(by) or '(no by:)'}")

    ceiling = _CEILINGS["claim_cards_uncited_replacement"]
    print(f"[superseded-citations] claim cards: {len(cards)} "
          f"(ceiling {ceiling}, declared debt)")
    if args.verbose or len(cards) > ceiling:
        for rel, _n, f, by in cards:
            print(f"    {rel} cites {f} — replaced by {', '.join(by)}")
    if len(cards) > ceiling:
        errs.append(f"claim-card debt ROSE {ceiling} -> {len(cards)}; a new card "
                    f"may not cite a superseded finding without naming what "
                    f"replaced it or declaring the ledger record in "
                    f"`supersessions:`")
    elif len(cards) < ceiling:
        print(f"[superseded-citations] debt FELL {ceiling} -> {len(cards)}; "
              f"run --ratchet-update to bank it")
        if args.ratchet_update:
            src = open(__file__, encoding="utf-8").read()
            src = src.replace(f'"claim_cards_uncited_replacement": {ceiling},',
                              f'"claim_cards_uncited_replacement": {len(cards)},')
            open(__file__, "w", encoding="utf-8").write(src)
            print(f"[superseded-citations] ceiling rewritten to {len(cards)}")

    if errs:
        print(f"\n[superseded-citations] FAILED — {len(errs)} problem(s):")
        for e in errs:
            print(f"  {e}" if e.startswith("    ") else f"  {e}")
        return 1
    print("[superseded-citations] ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
