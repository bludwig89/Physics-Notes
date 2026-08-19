#!/usr/bin/env python3
"""The public summary is a VIEW of the claim register, and a view can go stale silently.

WHY THIS EXISTS
===============
`docs/claims/` is the register: one card per claim, each carrying a present-tense
`status`. `papers/Claims-and-Falsifiers-Summary.md` is the document the outside world
actually reads, and until this file existed nothing connected the two. A card could be
withdrawn and replaced while the summary went on publishing the retracted position,
and every check stayed green -- `check_claims.py` grades cards against findings,
`check_superseded_citations.py` grades grading documents against the ledger, and
neither of them opens `papers/`.

That is not hypothetical. On 2026-08-16 **F320** derived $m_W$ and $m_Z$ absolutely
(cards **CL276**, **CL277**), and **CL016** -- "the absolute masses are not predicted"
-- moved to `status: withdrawn` the same day. The summary's Scope section went on
saying "the model predicts their **ratio**; $v$ is an anchor, not an output" for two
days, under a heading whose entire purpose is that *absence is not read as a
prediction*. The register was right and the public document was wrong, which is the
worse way round.

THE RULE
========
Every unit of the summary that stands on a claim carries an ANCHOR naming the cards it
stands on **and the status it is recording them at**:

    <!-- claims: CL276=live, CL277=live -->

The anchor is an assertion, not a cross-reference. Three ways to fail it:

  * the id does not exist in `docs/claims/`;
  * the card's current `status` is not what the anchor says it is -- this is the
    F320/CL016 catch, and it fires on ANY status change (a `live` claim narrowed, an
    `open` tension resolved), not just withdrawal;
  * the unit names a superseded finding without its replacement or an acknowledgement
    -- the `check_superseded_citations.py` rule, applied to the summary's units.

Those three are held at ZERO. Anchors are HTML comments so they do not reach the PDF.

A "unit" is one markdown block (contiguous non-blank lines), except that a table row
is its own unit -- the same deliberately small unit `check_superseded_citations.py`
uses, and for the same reason: an acknowledgement 300 lines from the sentence that
gets it wrong is not an acknowledgement.

COVERAGE IS A RATCHET, NOT A FLAT FAIL
======================================
A headline-tier card that the summary never mentions is a different failure: the
summary is not wrong, it is behind. Holding that at zero would mean a public document
that cannot be issued until every new headline result has been written up for a lay
reader in the same session -- so it is a counted, falling ceiling instead, and
`--ratchet-update` banks it. Supporting-tier cards are not counted at all; the summary
is a summary.

Usage:
    python3 tools/check_summary_claims.py [--ratchet-update] [--verbose]

Exit 0 clean, 1 on any violation or a ratchet rise.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_superseded_citations import _FN, _unit_ok, load_ledger  # noqa: E402

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS_DIR = os.path.join(_REPO, "docs", "claims")
SUMMARY = os.path.join(_REPO, "papers", "Claims-and-Falsifiers-Summary.md")

# Declared debt: headline cards the summary does not yet mention. May fall, never
# rise (`--ratchet-update` rewrites downward).
_CEILINGS = {
    "headline_cards_unmentioned": 0,
}

_ANCHOR = re.compile(r"<!--\s*claims:\s*(.*?)\s*-->")
_ENTRY = re.compile(r"\b(CL\d{3})\s*=\s*([a-z_]+)")


def load_cards(claims_dir: str = CLAIMS_DIR) -> dict[str, dict]:
    """``{CL id -> {"status", "tier", "title"}}`` from the card front matter."""
    cards: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(claims_dir, "CL*.md"))):
        text = open(path, encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue                          # check_claims.py owns malformed fm
        cid = str(fm.get("id") or "")
        if not cid:
            continue
        cards[cid] = {"status": str(fm.get("status") or ""),
                      "tier": str(fm.get("tier") or ""),
                      "title": str(fm.get("title") or "")}
    return cards


def parse_units(text: str) -> list[tuple[int, str]]:
    """``[(first line number, unit text)]``.

    A table row is its own unit; otherwise a unit is a block of contiguous
    non-blank lines. Fenced code is skipped -- it is illustration, not assertion.
    """
    units: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 0
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not line.strip() or line.lstrip().startswith("|"):
            if buf:
                units.append((start, "\n".join(buf)))
                buf = []
            if line.lstrip().startswith("|"):
                units.append((n, line))
            continue
        if not buf:
            start = n
        buf.append(line)
    if buf:
        units.append((start, "\n".join(buf)))
    return units


def check_unit(unit: str, cards: dict[str, dict], dead: dict) -> list[str]:
    """Every way one unit can be wrong. Pure: the selftest drives this directly."""
    errs: list[str] = []
    anchored: set[str] = set()
    for anchor in _ANCHOR.findall(unit):
        entries = _ENTRY.findall(anchor)
        if not entries:
            errs.append(f"anchor `{anchor}` names no CL id in `CLnnn=status` form")
        for cid, recorded in entries:
            anchored.add(cid)
            card = cards.get(cid)
            if card is None:
                errs.append(f"{cid} is anchored here but has no card in docs/claims/")
            elif card["status"] != recorded:
                errs.append(f"{cid} is recorded as `{recorded}` but the card says "
                            f"`{card['status']}` — {card['title'][:70]}")
    cited = set(_FN.findall(unit))
    for f in sorted(cited & dead.keys()):
        if not _unit_ok(cited, unit, f, dead):
            errs.append(f"cites {f} without naming what replaced it "
                        f"({', '.join(sorted(dead[f]['by'])) or 'no by:'}) "
                        f"or acknowledging the supersession")
    return errs


def selftest(dead_fixture: dict | None = None) -> bool:
    """The F320/CL016 regression, as a fixture. This check exists because of it.

    Reproduces the Scope bullet exactly as it stood on 2026-08-17 -- anchored at the
    status CL016 used to have -- and requires the matcher to FIRE on it, then to fall
    silent once the anchor records the withdrawal and points at the successor. Case 3
    carries the inherited superseded-finding rule. A checker that cannot be shown
    failing is not evidence.
    """
    cards = {"CL016": {"status": "withdrawn", "tier": "headline",
                       "title": "m_W and m_Z in absolute terms are not predicted"},
             "CL276": {"status": "live", "tier": "headline",
                       "title": "m_W and m_Z are predicted absolutely"}}
    dead = dead_fixture if dead_fixture is not None else {
        "F115": {"by": {"F138", "F231"}, "records": {"S20-x"}}}
    stale = ("- **$m_W$ and $m_Z$ in absolute terms.** The model predicts their "
             "**ratio**. <!-- claims: CL016=not_claimed -->")
    fixed = ("- ~~**$m_W$ and $m_Z$ in absolute terms.**~~ Moved to core claim 12. "
             "<!-- claims: CL016=withdrawn, CL276=live -->")
    bare = "| B9 | running of alpha | F115 |"
    named = "| B9 | running of alpha | F138, F231, F115 |"
    cases = [("stale anchor fires", stale, False),
             ("corrected anchor clears", fixed, True),
             ("bare superseded citation fires", bare, False),
             ("replacement named clears", named, True)]
    ok = True
    for label, text, want_clean in cases:
        got_clean = not check_unit(text, cards, dead)
        if got_clean is not want_clean:
            print(f"  [selftest FAIL] {label}: expected clean={want_clean}, "
                  f"got {got_clean}")
            ok = False
    print(f"  [selftest] {'PASS' if ok else 'FAIL'} — {len(cases)} cases "
          f"(stale status fires, corrected anchor clears, "
          f"superseded-finding rule inherited)")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratchet-update", action="store_true",
                    help="rewrite the ceiling to the current count, downward only")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    cards = load_cards()
    dead = load_ledger()
    text = open(SUMMARY, encoding="utf-8").read()
    rel = os.path.relpath(SUMMARY, _REPO)

    errs: list[str] = []
    anchored: set[str] = set()
    for n, unit in parse_units(text):
        for cid, _ in _ENTRY.findall(" ".join(_ANCHOR.findall(unit))):
            anchored.add(cid)
        for e in check_unit(unit, cards, dead):
            errs.append(f"    {rel}:{n} — {e}")

    headline = {c for c, v in cards.items() if v["tier"] == "headline"}
    missing = sorted(headline - anchored)

    print(f"[summary-claims] {rel}: {len(anchored)} card(s) anchored, "
          f"{len(headline)} headline card(s) in the register")

    if not selftest():
        errs.insert(0, "  selftest failed — the matcher does not fire on the "
                       "F320/CL016 regression it exists to catch")

    if errs:
        errs.insert(0, "  the summary records a claim at a status the register "
                       "does not agree with:")

    ceiling = _CEILINGS["headline_cards_unmentioned"]
    print(f"[summary-claims] headline cards unmentioned: {len(missing)} "
          f"(ceiling {ceiling}, declared debt)")
    if args.verbose or len(missing) > ceiling:
        for cid in missing:
            print(f"    {cid} [{cards[cid]['status']}] {cards[cid]['title'][:88]}")
    if len(missing) > ceiling:
        errs.append(f"  headline-card debt ROSE {ceiling} -> {len(missing)}; a new "
                    f"headline claim must reach the public summary, or the ceiling "
                    f"must be raised deliberately in this file")
    elif len(missing) < ceiling:
        print(f"[summary-claims] debt FELL {ceiling} -> {len(missing)}; "
              f"run --ratchet-update to bank it")
        if args.ratchet_update:
            src = open(__file__, encoding="utf-8").read()
            src = src.replace(f'"headline_cards_unmentioned": {ceiling},',
                              f'"headline_cards_unmentioned": {len(missing)},')
            open(__file__, "w", encoding="utf-8").write(src)
            print(f"[summary-claims] ceiling rewritten to {len(missing)}")

    if errs:
        print(f"\n[summary-claims] FAILED — {len(errs)} problem(s):")
        for e in errs:
            print(e)
        return 1
    print("[summary-claims] ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
