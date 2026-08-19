#!/usr/bin/env python3
"""Finding coverage — is every finding joined to its tests and its claim?

``check_finding_records.py`` (D9) answers a narrower question: *when a finding
declares a test record, does that record exist at the tier it claims?* It is
green on 317 findings. It is green partly because only **34** findings declare a
record at all; a finding that declares nothing is not checked, and cannot fail.

The join it does not check runs the other way, and it is not sound:

1. **``findings:`` on a test record is inferred, not asserted.**
   ``gen_test_registry.py`` fills it from ``FINDING_RE`` applied to the test's
   filename plus its docstring. So "F26 is covered by 32 records" means 32 files
   *mention the string F26*, not that 32 tests go red if F26 is wrong. 67
   findings have no record whose filename or id names them — their entire
   association is a prose mention.

2. **There is no way to say a finding has no test.** A finding with zero
   records and a finding awaiting one are indistinguishable, so the absence
   cannot be reviewed or ratcheted. Fixed by a declaration in the finding's own
   header, ``**Test record:** none — no-test (<reason>)``, with the closed
   vocabulary in ``NO_TEST_REASONS`` below — of which ``awaiting-test`` is the
   one that means debt.

3. **Nothing checks that a record's ``findings:`` ids are real.**
   ``check_claims.py`` enforces exactly this for claim cards (rule 3); the test
   registry had no equivalent, and 53 records named 48 ids with no
   ``findings/F*.md``. Cleared to 8 on 2026-08-19 — 40 brief ids moved to
   ``briefs:`` and ``F219`` (a collision blank) was removed from two records —
   and the check below is what keeps them out.

4. **Finding to claim is unenforced.** Cards name their findings; nothing
   requires a finding to be named by a card *or* to declare that it makes no
   claim. Ten findings are in neither state. Findings and cards are **not** 1:1
   and were never meant to be — one card routinely rests on six findings, and an
   infrastructure finding asserts nothing a card should hold. What has to be
   distinguishable is *absent* from *triaged and absent*.

The two debt states, and why they are not an escape hatch
---------------------------------------------------------
``awaiting-test`` and ``**Claim:** pending`` are honest answers: the work is
owed. They clear ``weak_only`` / ``claim_unset``, because the finding has stopped
being silent. They do **not** clear ``untested`` / ``unclaimed``, which hold the
sum. So relabelling a mention-only finding as debt moves it between two counters
and leaves the number that matters exactly where it was — which is the only
reason the 66-finding drain cannot be "finished" in an afternoon with
find-and-replace.

This tool measures all four. It writes a report and, with ``--check``, fails on
violations against a ratchet ceiling so it can be wired into ``make gate``
without turning the tree red on day one.

    python3 tools/audit_finding_coverage.py                  # summary
    python3 tools/audit_finding_coverage.py --report PATH    # markdown triage
    python3 tools/audit_finding_coverage.py --json PATH      # machine-readable
    python3 tools/audit_finding_coverage.py --check          # gate mode
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_FINDINGS = os.path.join(_REPO, "findings")
_REGISTRY = os.path.join(_REPO, "tests", "registry")
_CLAIMS = os.path.join(_REPO, "docs", "claims", "registry.yaml")

# Ratchet ceilings. These may fall, never rise.
#
# `dangling` was 53 on 2026-08-19 and is 8 the same afternoon: 40 brief ids moved
# to the `briefs:` field and F219 was cleared from two records. The 8 that remain
# were one problem, not eight: F2/F3/F4/F7/F10/F12 belong to the
# `findings/F01-F15-findings.md` bundle and F16 was retired to
# `deprecated/findings/`. Closed the same day (rollout step 3b) — the bundle
# declares the range it covers, so its members resolve, and F16 came out of the
# one record that cited it. Both are now ceiling 0 and should stay there.
#
# 2026-08-19 - 13:35, rollout section 4 BUCKET 1 (the F1-F50 era, 24 findings):
# weak_only/untested re-armed 66 -> 30. Two separable causes, both measured:
#   -4   the NAME test became case- and suffix-aware (`_NAME_ID`). Pure regex
#        artefacts: `f26-rotation-law` IS F26's record and `F26b-spin-axis-
#        scalar-contamination` IS F26b's; neither was ever mention-only.
#   -32  the two-sided DECLARED join now counts. 20 bucket-1 findings gained a
#        `**Test record:** record `X`` header this pass and 12 already had one;
#        11 records gained the finding on their side of the join.
# `claim_unset`/`unclaimed` read 2 as of this run but are NOT re-armed here: a
# concurrent session owns rollout section 6 and is mid-pass on those cards.
CEILINGS = {
    "unjoined": 0,        # findings with no record and no no-test declaration
    "weak_only": 30,      # findings whose only records are prose mentions
    "untested": 30,       # weak_only + awaiting-test: the number that must fall
    "dangling": 0,        # records naming a finding id that resolves to nothing
    "blank": 0,           # records naming a collision-vacated number — never ok
    "retired": 0,         # records naming a finding retired to deprecated/
    "briefs_in_findings": 0,   # brief ids in `findings:` — never ok
    "bad_declaration": 0,      # a no-test/claim header outside the vocabulary
    "claim_unset": 10,    # findings in no card, declaring no claim state
    "unclaimed": 10,      # claim_unset + pending: the claim-side equivalent
}

# The neighbouring id space: falsification briefs in tests/falsification/ and
# first-generation tags. Real, referable, and NOT findings — they live in
# `briefs:`. See casim.tests.registry's docstring.
_BRIEF_RE = re.compile(r"^F[A-Z]{1,2}\d{1,3}[a-z]?$")
_NUMBERS = os.path.join(_REPO, "docs", "design", "finding-numbers.yaml")
_DEPRECATED = os.path.join(_REPO, "deprecated", "findings")

# A bundle file declares the id range it is the home of, so membership is DATA
# rather than a filename parsed as a range:
#
#     **Covers:** F1–F15
#
# `findings/F01-F15-findings.md` is the only one today. Findings 1-15 predate
# the one-file-per-finding convention, so `findings/F7-*.md` does not exist and
# is not missing — six records cite ids in that range and every one of them was
# reported as dangling until this was declared.
_COVERS = re.compile(r"^\*\*Covers:\*\*\s*F(\d+)\s*[–—-]\s*F(\d+)", re.M)

# Same regex the generator uses, so "what it inferred" is reproducible here.
_FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")
_FILE_ID = re.compile(r"^(F\d+[a-z]?)")

# The NAME test, which is a different question from the generator's. `_FINDING_RE`
# reproduces what `gen_test_registry.py` INFERRED, so it must not change. This one
# asks "is this record NAMED for that finding?", and it has to be case- and
# suffix-aware or it reports false negatives that are pure regex artefacts:
#
#     f26-rotation-law                       is F26's record; lowercase `f` -> missed
#     F26b-spin-axis-scalar-contamination    is F26b's; `F26` != `F26b` -> missed
#
# Both were counted mention-only on 2026-08-19 while being the finding's own,
# correctly-curated record. The letter suffix is captured, matching `_FILE_ID`.
_NAME_ID = re.compile(r"(?<![A-Za-z0-9])([Ff][A-Za-z]{0,2}\d{1,3}[a-z]?)(?![0-9])")


def named_ids(*texts: str) -> set:
    """The finding ids a record's path and id NAME, normalised to `F<n><suffix>`."""
    out = set()
    for t in texts:
        for hit in _NAME_ID.findall(t or ""):
            out |= finding_aliases("F" + hit[1:])
    return out

# The finding-side header fields. Mirrors check_finding_records._HEADER so the
# two tools cannot disagree about what a declaration looks like.
_HEADER = re.compile(r"^(\*\*Tests?\b[^*]*\*\*)(.*)$", re.M | re.I)
_RECORD_ID = re.compile(r"record[s]?\s+`([^`]+)`")
_ANY_TICKED = re.compile(r"`([^`]+)`")
_ENTRY_TOKEN = re.compile(r"entry\s+`([^`]+)`")

# ---------------------------------------------------------------------------
# The two declarations a finding can make about itself.
#
#     **Test record:** none — no-test (analysis-only)
#     **Claim:** none — infrastructure; asserts no physics a card would carry
#
# Both are CLOSED and both REQUIRE A REASON, because the failure mode of an open
# vocabulary here is not a typo — it is that "no test" and "no test yet" collapse
# back into one another, which is the exact state this whole rollout exists to
# remove. An unrecognised reason, or a bare `none` with nothing after it, is a
# violation with its own ratchet at zero.
# ---------------------------------------------------------------------------
NO_TEST = re.compile(r"no[-_]test\s*\(\s*([a-z-]*)\s*\)", re.I)
# A header that opens with `none` — with or without a well-formed reason after.
_NONE_HEADER = re.compile(r"^\*\*Tests?\b[^*]*\*\*\s*none\b", re.M | re.I)

NO_TEST_REASONS = {
    "analysis-only": "closed-form arithmetic in the finding itself; nothing to run",
    "narrative-bundle": "a bundle/index file, not a single testable finding",
    "superseded": "fully superseded per docs/theory/supersessions.yaml",
    "awaiting-test": "DEBT: a test is owed. Counted by the `untested` ratchet.",
}
# The one reason that is debt rather than a resolution. It removes a finding from
# `weak_only` — it has answered the question — but it does NOT reduce `untested`,
# so declaring debt is neutral, never free. Without that, the drain in §4 of the
# rollout could be "finished" in an afternoon by relabelling all 66.
DEBT_REASON = "awaiting-test"

# `pending` is the claim-side equivalent of `awaiting-test`: this finding does
# carry a claim, the card is simply not written. Same treatment — it clears
# `claim_unset` and is held by `unclaimed`.
CLAIM_DECL = re.compile(
    r"^\*\*Claims?:\*\*[^\S\n]*(none|pending)\b[^\S\n]*(?:[—–-][^\S\n]*(\S.*))?$",
    re.M | re.I)
CLAIM_DEBT = "pending"
CLAIM_ID = re.compile(r"\bCL\d{3}\b")


# ---------------------------------------------------------------------------
def load_records() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(_REGISTRY, "*.yaml"))):
        for rec in (yaml.safe_load(open(path, encoding="utf-8")) or {}).get("tests") or []:
            rec["_source"] = os.path.basename(path)
            out[rec["id"]] = rec
    return out


def load_claims() -> list[dict]:
    return (yaml.safe_load(open(_CLAIMS, encoding="utf-8")) or {}).get("claims") or []


def blank_numbers(known: set[str]) -> set[str]:
    """Numbers abandoned after a collision — a blank, never a valid citation.

    Two filters, both load-bearing:

    * ``status: resolved`` covers two sub-cases and only one is a blank.
      F111/F127/F285 are "resolved" because the gap was CLOSED by recovering the
      file, and those findings exist. Requiring *and no file exists* separates
      them, so this never reports a live finding as vacant.
    * ``status: retired`` is excluded. A retired number had a real write-up that
      moved to ``deprecated/findings/`` (F16-F19); citing it is stale, not
      false, and it is a different conversation from a number that never held
      anything. Those surface in D3 instead.
    """
    doc = yaml.safe_load(open(_NUMBERS, encoding="utf-8")) or {}
    return {f"F{n}" for n, e in (doc.get("gaps") or {}).items()
            if (e or {}).get("status") == "resolved" and f"F{n}" not in known}


def declared_records(label: str, line: str) -> list[str]:
    """Record ids a finding's header names. Same reading as D9's checker."""
    entries = set(_ENTRY_TOKEN.findall(line))
    ids = [i for i in _RECORD_ID.findall(line) if i not in entries]
    if not ids and "record" in label.lower():
        for tok in _ANY_TICKED.findall(line):
            if tok in entries or "/" in tok or tok.endswith((".json", ".py", ".yaml")):
                continue
            if tok.lower().startswith("none"):
                continue
            return [tok]
    return ids


def finding_aliases(fid: str) -> set[str]:
    """`F01` and `F1` are the same finding. The tree writes both."""
    stem = fid[1:].rstrip("abcdefghijklmnopqrstuvwxyz")
    suffix = fid[1 + len(stem):]
    out = {fid}
    if stem.isdigit():
        out.add("F" + str(int(stem)) + suffix)
        out.add("F" + stem.zfill(2) + suffix)
    return out


def covered_range(text: str) -> set[str]:
    """The ids a `**Covers:** Fn–Fm` declaration claims for a bundle file.

    Ids that have a dedicated file of their own are subtracted by the caller —
    a promotion out of the bundle takes the id with it.
    """
    hit = _COVERS.search(text)
    if not hit:
        return set()
    lo, hi = int(hit.group(1)), int(hit.group(2))
    out: set[str] = set()
    for n in range(lo, hi + 1):
        out |= {f"F{n}", f"F{n:02d}"}
    return out


def retired_findings() -> set[str]:
    """Ids whose write-up moved to `deprecated/findings/` (F16-F19 today).

    Retired is not vacant and not missing: the write-up exists, it is simply no
    longer live. Citing one in `findings:` is therefore its own defect — the
    record cannot go red on a finding that has been withdrawn — and it gets its
    own bucket so the fix ("move the pointer to `notes:`") is unambiguous.
    """
    out: set[str] = set()
    for path in glob.glob(os.path.join(_DEPRECATED, "F*.md")):
        m = _FILE_ID.match(os.path.basename(path))
        if m:
            out |= finding_aliases(m.group(1))
    return out


def audit() -> dict:
    records = load_records()
    claims = load_claims()

    back = collections.defaultdict(list)
    for rid, rec in records.items():
        for f in rec.get("findings") or []:
            back[str(f).strip()].append(rid)

    claim_back = collections.defaultdict(list)
    for card in claims:
        for f in card.get("findings") or []:
            claim_back[str(f).strip()].append(card["id"])

    # Two passes, because a dedicated file OUTRANKS a bundle's declared range.
    # F15 was promoted out of the F1-F15 bundle into its own file, so `F15`
    # resolves there; letting the bundle absorb it would hand the bundle F15's
    # records and its claim card, which is a false attribution in the direction
    # that looks like progress.
    paths = sorted(glob.glob(os.path.join(_FINDINGS, "F*.md")))
    texts = {p: open(p, encoding="utf-8").read() for p in paths}
    primary: dict[str, set[str]] = {}
    for path in paths:
        m = _FILE_ID.match(os.path.basename(path))
        primary[path] = finding_aliases(m.group(1) if m
                                        else os.path.basename(path)[:-3])
    owned = {a for al in primary.values() for a in al}

    findings = []
    known_ids: set[str] = set()
    for path in paths:
        name = os.path.basename(path)
        m = _FILE_ID.match(name)
        fid = m.group(1) if m else name[:-3]
        text = texts[path]
        aliases = primary[path] | (covered_range(text) - owned)
        known_ids |= aliases

        declared, no_test, bad = [], None, []
        for label, line in _HEADER.findall(text):
            declared += declared_records(label, line)
            hit = NO_TEST.search(line)
            if hit:
                reason = hit.group(1).lower()
                if reason in NO_TEST_REASONS:
                    no_test = reason
                else:
                    bad.append(
                        f"no-test reason {reason or '(empty)'!r} is not in the "
                        f"closed vocabulary "
                        f"({', '.join(sorted(NO_TEST_REASONS))})")
        # `**Test record:** none` with no `no-test (<reason>)` after it is the
        # silence this rollout removes, wearing the word "none".
        if not no_test and not bad and _NONE_HEADER.search(text):
            bad.append("header declares `none` but names no no-test reason; "
                       "write `none — no-test (<reason>)`")

        claim_state = claim_reason = None
        hit = CLAIM_DECL.search(text)
        if hit:
            claim_state, claim_reason = hit.group(1).lower(), (hit.group(2) or "").strip()
            if not claim_reason:
                bad.append(f"`**Claim:** {claim_state}` gives no reason; a claim "
                           f"state nobody can review is not a declaration")
                claim_state = None

        backlinks = sorted({r for a in aliases for r in back.get(a, [])})
        declared_set = set(declared)
        strong, weak = [], []
        for rid in backlinks:
            base = os.path.basename(records[rid].get("path") or "")
            # A join is STRONG two ways, and the second is the stronger evidence.
            #
            #   NAMED    — the record's file or id carries the finding number. The
            #              convention from ~F150 on; free, and what the original
            #              audit measured.
            #   DECLARED — the finding's own header says `**Test record:** record
            #              `X`` AND record X's human-owned `findings:` names the
            #              finding back. Both ends asserted by a person, and
            #              check_finding_records.py already verifies that X exists
            #              at the tier claimed.
            #
            # Without the second, rollout section 4's bucket-1 recipe cannot move
            # this number: steps 1-4 rewrite `findings:` and never rename a file,
            # so a correctly curated pre-convention finding (`wmu-phase1` for F31,
            # `hypercharge` for F41, `F306-curl-closes-at-k3` for F21/F23/F25)
            # would still report as a prose mention. That is the measurement
            # failing, not the coverage.
            if named_ids(base, rid) & aliases or rid in declared_set:
                strong.append(rid)
            else:
                weak.append(rid)

        cards = sorted({c for a in aliases for c in claim_back.get(a, [])})
        findings.append({
            "id": fid,
            "file": name,
            "declared": declared,
            "no_test": no_test,
            "strong": strong,
            "weak": weak,
            "gate": sorted(r for r in backlinks if records[r].get("tier") == "gate"),
            "debt_only": bool(backlinks) and all(
                records[r].get("kind") == "legacy_script" for r in backlinks),
            "claims": cards,
            "claim_state": claim_state,
            "claim_reason": claim_reason,
            "bad": bad,
            "cl_in_prose": sorted(set(CLAIM_ID.findall(text))),
        })

    blanks = blank_numbers(known_ids)
    retired = retired_findings() - known_ids
    dangling: dict[str, list[str]] = collections.defaultdict(list)
    blank_hits: dict[str, list[str]] = collections.defaultdict(list)
    retired_hits: dict[str, list[str]] = collections.defaultdict(list)
    briefs_in_findings: dict[str, list[str]] = collections.defaultdict(list)
    for rid, rec in records.items():
        for raw in rec.get("findings") or []:
            f = str(raw).strip()
            if f in known_ids:
                continue
            if _BRIEF_RE.match(f):
                briefs_in_findings[f].append(rid)   # belongs in `briefs:`
            elif f in blanks:
                blank_hits[f].append(rid)           # a collision blank, never valid
            elif f in retired:
                retired_hits[f].append(rid)         # withdrawn to deprecated/
            else:
                dangling[f].append(rid)             # resolves to nothing at all

    weak_only = sum(1 for f in findings if not f["strong"] and not f["no_test"])
    awaiting = sum(1 for f in findings if f["no_test"] == DEBT_REASON)
    claim_unset = sum(1 for f in findings
                      if not f["claims"] and not f["claim_state"])
    pending = sum(1 for f in findings if f["claim_state"] == CLAIM_DEBT)
    counts = {
        "findings": len(findings),
        "records": len(records),
        "claims": len(claims),
        "unjoined": sum(1 for f in findings
                        if not f["strong"] and not f["weak"] and not f["no_test"]),
        "weak_only": weak_only,
        "awaiting_test": awaiting,
        # The number that actually has to fall. Relabelling a mention-only
        # finding as `awaiting-test` moves it between the two above and leaves
        # this one alone, which is the point.
        "untested": weak_only + awaiting,
        "debt_only": sum(1 for f in findings if f["debt_only"]),
        "no_test_declared": sum(1 for f in findings if f["no_test"]),
        "bad_declaration": sum(1 for f in findings if f["bad"]),
        "dangling": len({r for ids in dangling.values() for r in ids}),
        "dangling_ids": len(dangling),
        "blank": len({r for ids in blank_hits.values() for r in ids}),
        "retired": len({r for ids in retired_hits.values() for r in ids}),
        "briefs_in_findings": len({r for ids in briefs_in_findings.values() for r in ids}),
        "records_with_briefs": sum(1 for r in records.values() if r.get("briefs")),
        "claim_unset": claim_unset,
        "claims_pending": pending,
        "unclaimed": claim_unset + pending,
        "claim_none_declared": sum(1 for f in findings if f["claim_state"] == "none"),
        "empty_findings_field": sum(1 for r in records.values() if not r.get("findings")),
    }
    return {"counts": counts, "findings": findings,
            "blanks": {k: sorted(v) for k, v in sorted(blank_hits.items())},
            "retired": {k: sorted(v) for k, v in sorted(retired_hits.items())},
            "briefs_in_findings": {k: sorted(v)
                                   for k, v in sorted(briefs_in_findings.items())},
            "dangling": {k: sorted(v) for k, v in sorted(dangling.items())}}


# ---------------------------------------------------------------------------
def write_report(data: dict, path: str) -> None:
    c, F = data["counts"], data["findings"]
    L = [
        "# Finding coverage audit",
        "",
        f"*Generated by `tools/audit_finding_coverage.py`. "
        f"{c['findings']} findings, {c['records']} test records, {c['claims']} claim cards.*",
        "",
        "## Summary",
        "",
        "| Gap | Count | Ceiling |",
        "|-----|-------|---------|",
        f"| Findings joined to no record and declaring no no-test | {c['unjoined']} | {CEILINGS['unjoined']} |",
        f"| Findings whose only records are prose mentions | {c['weak_only']} | {CEILINGS['weak_only']} |",
        f"| Findings declaring `no-test (awaiting-test)` — DEBT | {c['awaiting_test']} | — |",
        f"| **Untested** = the two above; relabelling does not move it | **{c['untested']}** | {CEILINGS['untested']} |",
        f"| Findings backed only by `legacy_script` debt | {c['debt_only']} | — |",
        f"| Records naming a finding id with no file | {c['dangling']} | {CEILINGS['dangling']} |",
        f"| Distinct dangling finding ids | {c['dangling_ids']} | — |",
        f"| Records naming a collision-vacated blank | {c['blank']} | {CEILINGS['blank']} |",
        f"| Records naming a retired finding | {c['retired']} | {CEILINGS['retired']} |",
        f"| Records with a brief id in `findings:` | {c['briefs_in_findings']} | {CEILINGS['briefs_in_findings']} |",
        f"| Records carrying `briefs:` | {c['records_with_briefs']} | — |",
        f"| Records with an empty `findings:` | {c['empty_findings_field']} | — |",
        f"| Findings in no card, declaring no claim state | {c['claim_unset']} | {CEILINGS['claim_unset']} |",
        f"| Findings declaring `**Claim:** pending` — DEBT | {c['claims_pending']} | — |",
        f"| **Unclaimed** = the two above | **{c['unclaimed']}** | {CEILINGS['unclaimed']} |",
        f"| Findings declaring `**Claim:** none` | {c['claim_none_declared']} | — |",
        f"| Findings with a no-test declaration | {c['no_test_declared']} | — |",
        f"| Malformed no-test / claim declarations | {c['bad_declaration']} | {CEILINGS['bad_declaration']} |",
        "",
        "## The two declarations",
        "",
        "```markdown",
        "**Test record:** none — no-test (analysis-only)",
        "**Claim:** none — infrastructure; asserts no physics a card would carry",
        "```",
        "",
        "Both reasons are required and the no-test reason is closed:",
        "",
    ] + [f"- `{k}` — {v}" for k, v in sorted(NO_TEST_REASONS.items())] + [
        "",
        "`**Claim:**` takes `none` or `pending`, each with a free-text reason after "
        "an em dash. `awaiting-test` and `pending` are the two debt states: they "
        "answer the question, so they clear `weak_only`/`claim_unset`, but they are "
        "held by `untested`/`unclaimed` so relabelling is never a way to finish.",
        "",
        "## A — unjoined findings",
        "",
        "No test record names them and they declare no no-test reason.",
        "",
    ]
    rows = [f for f in F if not f["strong"] and not f["weak"] and not f["no_test"]]
    L += [f"- **{f['id']}** — `{f['file']}`" for f in rows] or ["*(none)*"]

    L += ["", "## B — association is a prose mention only", "",
          "Every record listing these findings does so because `FINDING_RE` hit the "
          "docstring, not because the test file is named for the finding. Each needs "
          "one decision: name the record that can actually go red, or declare no-test.",
          "", "| Finding | Mention-only records | Gate-tier? | Claim |", "|---|---|---|---|"]
    for f in sorted((f for f in F if not f["strong"] and not f["no_test"]),
                    key=lambda f: -len(f["weak"])):
        L.append(f"| {f['id']} | {len(f['weak'])}: "
                 f"{', '.join('`%s`' % r for r in f['weak'][:4])}"
                 f"{' …' if len(f['weak']) > 4 else ''} | "
                 f"{'yes' if f['gate'] else 'no'} | "
                 f"{', '.join(f['claims']) or '—'} |")

    L += ["", "## C — over-claimed findings (≥10 records)", "",
          "Large counts are the regex, not coverage. Prune `findings:` to the records "
          "that can go red on this finding.", "",
          "| Finding | Records | of which filename-matched |", "|---|---|---|"]
    for f in sorted(F, key=lambda f: -(len(f["strong"]) + len(f["weak"]))):
        n = len(f["strong"]) + len(f["weak"])
        if n < 10:
            break
        L.append(f"| {f['id']} | {n} | {len(f['strong'])} |")

    L += ["", "## D — ids in `findings:` that resolve to nothing", "",
          "Split three ways, because they are three different defects.", ""]

    L += ["### D1 — brief ids (belong in `briefs:`)", ""]
    if data["briefs_in_findings"]:
        L += ["| Id | Records |", "|---|---|"] + [
            f"| {k} | {len(v)}: {', '.join('`%s`' % r for r in v[:3])}"
            f"{' …' if len(v) > 3 else ''} |"
            for k, v in data["briefs_in_findings"].items()]
    else:
        L.append("*(none — cleared 2026-08-19; 40 ids moved to `briefs:`)*")

    L += ["", "### D2 — collision blanks (never valid in `findings:`)", "",
          "A number `docs/design/finding-numbers.yaml` declares abandoned after a "
          "concurrent-session collision. No file exists and none is coming, so the "
          "citation points at the collision rather than at physics.", ""]
    if data["blanks"]:
        L += ["| Id | Records |", "|---|---|"] + [
            f"| {k} | {len(v)}: {', '.join('`%s`' % r for r in v)} |"
            for k, v in data["blanks"].items()]
    else:
        L.append("*(none — F219 cleared from 2 records 2026-08-19)*")

    L += ["", "### D3 — retired findings (withdrawn to `deprecated/findings/`)", "",
          "The write-up exists; it is just no longer live, so no record can go red on "
          "it. Move the pointer to `notes:`.", ""]
    if data["retired"]:
        L += ["| Id | Records |", "|---|---|"] + [
            f"| {k} | {len(v)}: {', '.join('`%s`' % r for r in v)} |"
            for k, v in data["retired"].items()]
    else:
        L.append("*(none — F16 cleared from `FC01-mercury-perihelion` 2026-08-19)*")

    L += ["", "### D4 — ids that resolve to nothing at all", "",
          "Not a brief, not a declared blank, not retired, and no file. If a bundle "
          "file is the home of the id, say so there with `**Covers:** Fn–Fm`.", ""]
    if data["dangling"]:
        L += ["| Id | Records |", "|---|---|"] + [
            f"| {fid} | {len(rids)}: {', '.join('`%s`' % r for r in rids[:3])}"
            f"{' …' if len(rids) > 3 else ''} |"
            for fid, rids in data["dangling"].items()]
    else:
        L.append("*(none — the F1–F15 bundle declares its range as of 2026-08-19)*")

    L += ["", "## E — findings named by no claim card", "",
          "A finding need not carry a claim. Each of these needs reading once to "
          "confirm it asserts nothing a card should hold, then an explicit "
          "`**Claim:** none — <reason>` so the state is declared rather than absent.",
          ""]
    L += [f"- **{f['id']}** — `{f['file']}`"
          f"{' (mentions ' + ', '.join(f['cl_in_prose']) + ' in prose)' if f['cl_in_prose'] else ''}"
          for f in F if not f["claims"] and not f["claim_state"]] or ["*(none)*"]

    L += ["", "## F — malformed declarations", "",
          "A `no-test` reason outside the closed vocabulary, a bare `none` header "
          "with no reason, or a `**Claim:**` state with nothing after the dash. "
          "Ceiling 0 — an unreviewable declaration is worse than none, because it "
          "counts as an answer.", ""]
    L += [f"- **{f['id']}** — {b}" for f in F for b in f["bad"]] or ["*(none)*"]

    L += ["", "## G — declared states", "", "| Finding | Test | Claim |", "|---|---|---|"]
    rows = [f for f in F if f["no_test"] or f["claim_state"]]
    for f in rows:
        L.append(f"| {f['id']} | {('no-test (' + f['no_test'] + ')') if f['no_test'] else '—'} "
                 f"| {(f['claim_state'] + ' — ' + f['claim_reason'][:70]) if f['claim_state'] else '—'} |")
    if not rows:
        L.append("| *(none yet)* | | |")
    L.append("")
    open(path, "w", encoding="utf-8").write("\n".join(L))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", help="write the markdown triage report here")
    ap.add_argument("--json", dest="json_path", help="write the raw audit here")
    ap.add_argument("--check", action="store_true", help="fail above the ceilings")
    args = ap.parse_args()

    data = audit()
    c = data["counts"]
    if args.report:
        write_report(data, args.report)
        print(f"[coverage] report -> {args.report}")
    if args.json_path:
        json.dump(data, open(args.json_path, "w", encoding="utf-8"), indent=1)
        print(f"[coverage] json   -> {args.json_path}")

    print(f"[coverage] {c['findings']} findings / {c['records']} records / "
          f"{c['claims']} claims")
    for k in CEILINGS:
        flag = "OVER" if c[k] > CEILINGS[k] else "ok"
        print(f"[coverage]   {k:<19} {c[k]:>4}  (ceiling {CEILINGS[k]}) {flag}")
    print(f"[coverage]   {'declared':<19} "
          f"no-test {c['no_test_declared']} (of which debt {c['awaiting_test']})  "
          f"claim-none {c['claim_none_declared']} (pending {c['claims_pending']})  "
          f"legacy-debt-only {c['debt_only']}")
    for f in data["findings"]:
        for b in f["bad"]:
            print(f"[coverage]   BAD {f['id']}: {b}", file=sys.stderr)

    if args.check:
        over = [k for k in CEILINGS if c[k] > CEILINGS[k]]
        if over:
            print(f"[coverage] FAIL — above ceiling: {', '.join(over)}", file=sys.stderr)
            return 1
        print("[coverage] within every ceiling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
