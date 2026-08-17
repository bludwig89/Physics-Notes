#!/usr/bin/env python3
"""D12 acceptance — the claim cards in ``docs/claims/`` are well-formed and true.

A **claim card** is the project's present-tense assertion (see
``docs/claims/README.md``). This checker is what makes the layer worth having:
without it a card is just another markdown file that can drift from the tree.

What it enforces, and why each rule exists:

1. **Closed vocabularies.** ``tier kind status domain exactness falsifier
   review_state`` each draw from a fixed set. An open vocabulary is how
   "overstated" became unsayable in the prose summary — a status field that can
   hold anything cannot be counted.
2. **Identity.** ``id`` unique, ``CL{NNN}`` contiguous from CL001 (gaps must be
   declared, like finding numbers), filename == ``{id}-{slug}.md``, and
   ``slug`` == the front-matter slug. A card whose filename and id disagree is a
   card two tools will disagree about.
3. **Referential integrity.** Every ``findings:`` entry resolves to a real
   ``findings/F{N}-*.md``; every ``rolls_up_to`` resolves to a real card; every
   ``supersessions:`` id exists in ``docs/theory/supersessions.yaml``; every
   repo-relative path in ``## Sources`` exists on disk.
4. **THE rule — a live claim standing on wholly superseded ground.** A card with
   ``status: live`` **fails** when *every* finding it rests on is named in a
   ``superseded:`` list in the ledger. This is the machine-checkable form of
   "overstated", and it is the check that revisions 2 and 3 of
   ``papers/Claims-and-Falsifiers-Summary.md`` would have tripped months before a
   human noticed.

   It deliberately does **not** fire on a *partial* supersession. The standing
   lesson of this repo — ``deprecated/README.md``, and the 2026-08-04 header
   triage — is that almost nothing here is superseded wholesale: of 14 test files
   one audit called superseded, exactly one was. A check that flagged partials
   would train people to ignore it, which is worse than not having it.
5. **Ratchets.** ``exactness: unset``, ``falsifier: unset`` and
   ``review_state: unreviewed-seed`` are declared debt with a ceiling in
   ``_CEILINGS``. They may fall, never rise. ``--ratchet-update`` rewrites the
   ceiling downward only.

Exit 0 clean, 1 on any violation.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS_DIR = os.path.join(_REPO, "docs", "claims")
FINDINGS_DIR = os.path.join(_REPO, "findings")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")
GAPS = os.path.join(CLAIMS_DIR, "claim-numbers.yaml")

# --------------------------------------------------------------------------
# Closed vocabularies — docs/claims/README.md is the human-readable copy.
# --------------------------------------------------------------------------
TIERS = {"headline", "supporting"}
KINDS = {"derivation", "deviation", "reinterpretation", "prediction",
         "no_go", "non_claim"}
STATUSES = {"live", "narrowed", "contingent", "open", "withdrawn", "not_claimed"}
DOMAINS = {"QM", "SM", "GR", "SR", "QFT", "QCD", "cosmology",
           "condensed-matter", "none"}
# Same closed set as casim.constants.EXACTNESS_CLASSES + `unset` (debt).
EXACTNESS = {"exact", "machine", "quantitative", "bracketed", "external", "unset"}
FALSIFIER = {"stated", "none", "unset"}
REVIEW_STATE = {"authored", "unreviewed-seed"}
PROVENANCE = {"authored", "extracted"}
CONFIDENCE = {"high", "medium", "low"}

# Declared debt, baselined 2026-08-04 at the counts the seeding pass produced.
# These may only FALL: `--ratchet-update` writes `min(measured, ceiling)` and so
# can never loosen the gate. Raising one is a hand edit, and should carry a
# reason in `docs/status/changelog.md` — the point of the ratchet is that adding
# debt is a decision someone has to make in writing.
#
#   falsifier_unset  = 223 seeds + CL003, CL006, CL010 (the three authored cards
#                      whose source states no threshold and where this session
#                      declined to invent one — see the consolidation plan §4/Q4)
#   unreviewed_seed  = the 223 mechanically extracted cards
#   exactness_unset  = seeds whose finding's own status line named no exactness
#                      class in words the extractor could read
_CEILINGS = {
    "exactness_unset": 63,
    "falsifier_unset": 226,
    "unreviewed_seed": 223,
}

_LIST_FIELDS = ("domain", "findings", "tests", "modules", "constants",
                "supersessions", "reviews")
_REQUIRED = ("id", "title", "slug", "tier", "kind", "status", "domain",
             "exactness", "falsifier", "first_issued", "last_verified",
             "provenance", "review_state", "confidence")
_SECTIONS = ("## Statement", "## What it extends", "## Evidence",
             "## Falsifier", "## Status & history", "## Sources")

_ID_RE = re.compile(r"^CL(\d{3})$")
_PATH_RE = re.compile(r"`((?:findings|docs|papers|src|tests|tools|scenarios|"
                      r"references|test-results|deprecated)/[^`\s]+)`")


# --------------------------------------------------------------------------
# A deliberately small front-matter reader.
#
# The repo vendors PyYAML, but this checker runs inside `make gate` before the
# vendored path is necessarily active, and a card's front matter is a flat
# scalar/inline-list mapping by construction (`render()` in the generator emits
# nothing else). Parsing it here keeps the gate check dependency-free; the
# generated `registry.yaml` is the artifact anything else should read.
# --------------------------------------------------------------------------
def _strict_yaml_check(raw: str, path: str, errs: list) -> None:
    """Front matter must ALSO parse under a real YAML parser.

    The reader below is deliberately small and forgiving, which is what lets the
    gate run without the vendored path active. But forgiving is exactly the
    failure mode: 28 of the first 251 cards carried a LaTeX title inside a
    DOUBLE-quoted scalar (`"…\\dim(E_g)…"`), which is an invalid-escape parse
    error in YAML — and this reader read them happily while PyYAML, and every
    editor and tool that uses it, could not. The cards are now single-quoted
    (literal, only '' escapes), and this check is what stops the class of bug
    returning: if PyYAML is importable, it must agree that the front matter is
    YAML. When it is not importable the check is skipped rather than faked.
    """
    try:
        import yaml                                   # noqa: PLC0415
    except ModuleNotFoundError:                       # pragma: no cover
        return
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        first = str(exc).splitlines()[0]
        errs.append(f"{path}: front matter is not valid YAML ({first}). "
                    "Quote scalars with SINGLE quotes — a double-quoted YAML "
                    "scalar processes escapes, so LaTeX is a parse error.")
        return
    if not isinstance(parsed, dict):
        errs.append(f"{path}: front matter is not a mapping")


def parse_front_matter(text: str, path: str, errs: list) -> dict:
    if not text.startswith("---\n"):
        errs.append(f"{path}: no YAML front matter")
        return {}
    end = text.find("\n---\n", 3)
    if end < 0:
        errs.append(f"{path}: unterminated front matter")
        return {}
    _strict_yaml_check(text[4:end], path, errs)
    fm = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errs.append(f"{path}: unparsable front-matter line {line!r}")
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [x.strip().strip('"').strip("'")
                     for x in inner.split(",") if x.strip()]
        elif v in ("null", "~", ""):
            fm[k] = None
        else:
            fm[k] = v.strip('"').strip("'")
    fm["_body"] = text[end + 5:]
    return fm


def load_ledger_supersessions():
    """Return (record_ids, superseded_findings).

    `superseded_findings` is the set of F-numbers named in ANY `superseded:`
    list. Read textually for the same dependency reason as above; the ledger's
    `superseded:` blocks are flat inline or dashed lists of F-ids.
    """
    ids, dead = set(), set()
    if not os.path.exists(LEDGER):
        return ids, dead
    text = open(LEDGER, encoding="utf-8").read()
    ids |= set(re.findall(r"^\s*-?\s*id:\s*([A-Za-z0-9_.-]+)", text, re.M))
    for m in re.finditer(r"^(\s*)superseded:\s*(.*)$", text, re.M):
        indent, inline = m.group(1), m.group(2).strip()
        if inline.startswith("["):
            dead |= set(re.findall(r"F\d+", inline))
            continue
        rest = text[m.end():]
        for line in rest.splitlines():
            if not line.strip():
                continue
            if not line.startswith(indent + " ") and not line.strip().startswith("-"):
                break
            if re.match(r"^\s*-\s", line):
                dead |= set(re.findall(r"F\d+", line))
            elif len(line) - len(line.lstrip()) <= len(indent):
                break
    return ids, dead


def declared_gaps() -> set:
    if not os.path.exists(GAPS):
        return set()
    return set(re.findall(r"^\s*-?\s*(?:id:\s*)?(CL\d{3})",
                          open(GAPS, encoding="utf-8").read(), re.M))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratchet-update", action="store_true",
                    help="rewrite the debt ceilings downward to the measured counts")
    args = ap.parse_args()

    if not os.path.isdir(CLAIMS_DIR):
        print("[claims] docs/claims/ does not exist")
        return 1

    files = sorted(f for f in os.listdir(CLAIMS_DIR)
                   if f.startswith("CL") and f.endswith(".md"))
    if not files:
        print("[claims] no claim cards found in docs/claims/")
        return 1

    findings_on_disk = {}
    for fn in os.listdir(FINDINGS_DIR):
        m = re.match(r"(F\d+[a-z]?)-", fn)
        if m and fn.endswith(".md"):
            findings_on_disk.setdefault(m.group(1), fn)

    ledger_ids, dead_findings = load_ledger_supersessions()

    errs, warns, cards = [], [], {}

    for fn in files:
        path = os.path.join(CLAIMS_DIR, fn)
        rel = f"docs/claims/{fn}"
        fm = parse_front_matter(open(path, encoding="utf-8").read(), rel, errs)
        if not fm:
            continue

        for k in _REQUIRED:
            if k not in fm or fm[k] in (None, ""):
                errs.append(f"{rel}: missing required field `{k}`")
        for k in _LIST_FIELDS:
            fm.setdefault(k, [])
            if not isinstance(fm[k], list):
                errs.append(f"{rel}: `{k}` must be a list")
                fm[k] = []

        cid = fm.get("id", "")
        if not _ID_RE.match(cid or ""):
            errs.append(f"{rel}: id {cid!r} is not CL###")
            continue
        if cid in cards:
            errs.append(f"{rel}: duplicate id {cid} (also {cards[cid]['_file']})")
        fm["_file"] = rel
        cards[cid] = fm

        expected = f"{cid}-{fm.get('slug')}.md"
        if fn != expected:
            errs.append(f"{rel}: filename disagrees with id+slug (expected {expected})")

        for field, vocab in (("tier", TIERS), ("kind", KINDS),
                             ("status", STATUSES), ("exactness", EXACTNESS),
                             ("falsifier", FALSIFIER),
                             ("review_state", REVIEW_STATE),
                             ("provenance", PROVENANCE),
                             ("confidence", CONFIDENCE)):
            v = fm.get(field)
            if v is not None and v not in vocab:
                errs.append(f"{rel}: {field}={v!r} not in {sorted(vocab)}")
        for d in fm["domain"]:
            if d not in DOMAINS:
                errs.append(f"{rel}: domain {d!r} not in {sorted(DOMAINS)}")
        if not fm["domain"]:
            errs.append(f"{rel}: `domain` may not be empty (use [none])")

        for h in _SECTIONS:
            if h not in fm["_body"]:
                errs.append(f"{rel}: missing section `{h}`")

        # A `falsifier: stated` card must actually state one.
        m = re.search(r"## Falsifier\n(.*?)(?=\n## |\Z)", fm["_body"], re.S)
        ftext = (m.group(1).strip() if m else "")
        if fm.get("falsifier") == "stated" and len(ftext) < 40:
            errs.append(f"{rel}: falsifier: stated but the section is empty/stub")
        if fm.get("falsifier") == "none" and len(ftext) < 40:
            errs.append(f"{rel}: falsifier: none must say WHY (README: "
                        "'structural is a reason only when the structure is named')")

        for f in fm["findings"]:
            if not re.match(r"^F\d+[a-z]?$", f):
                errs.append(f"{rel}: findings entry {f!r} is not an F-number")
            elif f not in findings_on_disk:
                errs.append(f"{rel}: findings entry {f} has no findings/{f}-*.md")

        for s in fm["supersessions"]:
            if ledger_ids and s not in ledger_ids:
                errs.append(f"{rel}: supersession {s!r} not in supersessions.yaml")

        for p in _PATH_RE.findall(fm["_body"]):
            if not os.path.exists(os.path.join(_REPO, p)):
                errs.append(f"{rel}: referenced path does not exist: {p}")

        # A withdrawn card must keep its retraction record.
        if fm.get("status") == "withdrawn":
            m = re.search(r"## Status & history\n(.*?)(?=\n## |\Z)", fm["_body"], re.S)
            if not m or len(m.group(1).strip()) < 80:
                errs.append(f"{rel}: status: withdrawn — `## Status & history` IS the "
                            "retraction record and may not be a stub")

    # ---- cross-card ------------------------------------------------------
    gaps = declared_gaps()
    nums = sorted(int(_ID_RE.match(c).group(1)) for c in cards)
    for n in range(1, (max(nums) if nums else 0) + 1):
        if n not in nums and f"CL{n:03d}" not in gaps:
            errs.append(f"claim number CL{n:03d} is a gap — declare it in "
                        "docs/claims/claim-numbers.yaml with a reason")

    for cid, fm in cards.items():
        up = fm.get("rolls_up_to")
        if up and up not in cards:
            errs.append(f"{fm['_file']}: rolls_up_to={up} is not a card")
        if up == cid:
            errs.append(f"{fm['_file']}: rolls_up_to points at itself")

    # ---- THE rule --------------------------------------------------------
    overstated = []
    for cid, fm in sorted(cards.items()):
        if fm.get("status") != "live":
            continue
        fs = fm["findings"]
        if fs and all(f in dead_findings for f in fs):
            overstated.append((cid, fm["_file"], fs))

    # ---- ratchets --------------------------------------------------------
    counts = {
        "exactness_unset": sum(1 for f in cards.values() if f.get("exactness") == "unset"),
        "falsifier_unset": sum(1 for f in cards.values() if f.get("falsifier") == "unset"),
        "unreviewed_seed": sum(1 for f in cards.values()
                               if f.get("review_state") == "unreviewed-seed"),
    }
    for k, n in counts.items():
        if n > _CEILINGS[k]:
            errs.append(f"debt ratchet `{k}`: {n} > ceiling {_CEILINGS[k]} — "
                        "these may fall, never rise")

    if args.ratchet_update:
        src = open(os.path.abspath(__file__), encoding="utf-8").read()
        for k, n in counts.items():
            new = min(n, _CEILINGS[k])
            src = re.sub(rf'"{k}": \d+', f'"{k}": {new}', src)
        open(os.path.abspath(__file__), "w", encoding="utf-8").write(src)
        print(f"[claims] ceilings updated to {counts}")

    # ---- report ----------------------------------------------------------
    for c, f, fs in overstated:
        errs.append(f"{f}: status: live but EVERY supporting finding is "
                    f"superseded ({', '.join(fs)}) — narrow, withdraw, or add "
                    "a finding that survives")

    if errs:
        print(f"[claims] {len(errs)} problem(s):")
        for e in errs:
            print(f"    {e}")
        return 1

    by_status = {}
    for f in cards.values():
        by_status[f["status"]] = by_status.get(f["status"], 0) + 1
    print(f"[claims] {len(cards)} cards, CL001–CL{max(nums):03d}; "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())))
    print(f"[claims] debt: " + ", ".join(f"{k}={v}/{_CEILINGS[k]}"
                                         for k, v in sorted(counts.items())))
    for w in warns:
        print(f"    note: {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
