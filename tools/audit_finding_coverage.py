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
   cannot be reviewed or ratcheted.

3. **Nothing checks that a record's ``findings:`` ids are real.**
   ``check_claims.py`` enforces exactly this for claim cards (rule 3); the test
   registry had no equivalent, and 53 records named 48 ids with no
   ``findings/F*.md``. Cleared to 8 on 2026-08-19 — 40 brief ids moved to
   ``briefs:`` and ``F219`` (a collision blank) was removed from two records —
   and the check below is what keeps them out.

4. **Finding to claim is unenforced.** Cards name their findings; nothing
   requires a finding to be named by a card *or* to declare that it makes no
   claim. Ten findings are in neither state.

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
# are one problem, not eight — F2/F3/F4/F7/F10/F12/F16 all belong to the
# `findings/F01-F15-findings.md` bundle, whose id space is still unruled
# (`docs/roadmaps/finding-coverage-rollout.md` step 3b). Do not re-arm this
# number without reading that.
CEILINGS = {
    "unjoined": 0,        # findings with no record and no no-test declaration
    "weak_only": 67,      # findings whose only records are prose mentions
    "dangling": 8,        # records naming a finding id with no file
    "blank": 0,           # records naming a collision-vacated number — never ok
    "briefs_in_findings": 0,   # brief ids in `findings:` — never ok
    "claim_unset": 10,    # findings in no card and declaring no `claim: none`
}

# The neighbouring id space: falsification briefs in tests/falsification/ and
# first-generation tags. Real, referable, and NOT findings — they live in
# `briefs:`. See casim.tests.registry's docstring.
_BRIEF_RE = re.compile(r"^F[A-Z]{1,2}\d{1,3}[a-z]?$")
_NUMBERS = os.path.join(_REPO, "docs", "design", "finding-numbers.yaml")

# Same regex the generator uses, so "what it inferred" is reproducible here.
_FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")
_FILE_ID = re.compile(r"^(F\d+[a-z]?)")

# The finding-side header fields. Mirrors check_finding_records._HEADER so the
# two tools cannot disagree about what a declaration looks like.
_HEADER = re.compile(r"^(\*\*Tests?\b[^*]*\*\*)(.*)$", re.M | re.I)
_RECORD_ID = re.compile(r"record[s]?\s+`([^`]+)`")
_ANY_TICKED = re.compile(r"`([^`]+)`")
_ENTRY_TOKEN = re.compile(r"entry\s+`([^`]+)`")

# Proposed vocabulary for the finding-side no-test declaration:
#     **Test record:** none — no-test (analysis-only)
NO_TEST = re.compile(r"no[-_]test\s*\(([a-z-]+)\)", re.I)
NO_TEST_REASONS = {
    "analysis-only": "closed-form arithmetic in the finding itself; nothing to run",
    "narrative-bundle": "a bundle/index file, not a single testable finding",
    "superseded": "fully superseded per docs/theory/supersessions.yaml",
    "awaiting-test": "DEBT: a test is owed. Counted by the ratchet.",
}

# Proposed finding-side claim declaration: **Claim:** none — makes no claim.
CLAIM_NONE = re.compile(r"^\*\*Claims?:\*\*\s*none\b", re.M | re.I)
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

    findings = []
    known_ids: set[str] = set()
    for path in sorted(glob.glob(os.path.join(_FINDINGS, "F*.md"))):
        name = os.path.basename(path)
        m = _FILE_ID.match(name)
        fid = m.group(1) if m else name[:-3]
        aliases = finding_aliases(fid)
        known_ids |= aliases
        text = open(path, encoding="utf-8").read()

        declared, no_test = [], None
        for label, line in _HEADER.findall(text):
            declared += declared_records(label, line)
            hit = NO_TEST.search(line)
            if hit:
                no_test = hit.group(1).lower()

        backlinks = sorted({r for a in aliases for r in back.get(a, [])})
        strong, weak = [], []
        for rid in backlinks:
            base = os.path.basename(records[rid].get("path") or "")
            named = set(_FINDING_RE.findall(base)) | set(_FINDING_RE.findall(rid))
            (strong if named & aliases else weak).append(rid)

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
            "claim_none": bool(CLAIM_NONE.search(text)),
            "cl_in_prose": sorted(set(CLAIM_ID.findall(text))),
        })

    blanks = blank_numbers(known_ids)
    dangling: dict[str, list[str]] = collections.defaultdict(list)
    blank_hits: dict[str, list[str]] = collections.defaultdict(list)
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
            else:
                dangling[f].append(rid)             # a finding id with no file

    counts = {
        "findings": len(findings),
        "records": len(records),
        "claims": len(claims),
        "unjoined": sum(1 for f in findings
                        if not f["strong"] and not f["weak"] and not f["no_test"]),
        "weak_only": sum(1 for f in findings if not f["strong"] and not f["no_test"]),
        "debt_only": sum(1 for f in findings if f["debt_only"]),
        "no_test_declared": sum(1 for f in findings if f["no_test"]),
        "dangling": len({r for ids in dangling.values() for r in ids}),
        "dangling_ids": len(dangling),
        "blank": len({r for ids in blank_hits.values() for r in ids}),
        "briefs_in_findings": len({r for ids in briefs_in_findings.values() for r in ids}),
        "records_with_briefs": sum(1 for r in records.values() if r.get("briefs")),
        "claim_unset": sum(1 for f in findings
                           if not f["claims"] and not f["claim_none"]),
        "empty_findings_field": sum(1 for r in records.values() if not r.get("findings")),
    }
    return {"counts": counts, "findings": findings,
            "blanks": {k: sorted(v) for k, v in sorted(blank_hits.items())},
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
        f"| Findings backed only by `legacy_script` debt | {c['debt_only']} | — |",
        f"| Records naming a finding id with no file | {c['dangling']} | {CEILINGS['dangling']} |",
        f"| Distinct dangling finding ids | {c['dangling_ids']} | — |",
        f"| Records naming a collision-vacated blank | {c['blank']} | {CEILINGS['blank']} |",
        f"| Records with a brief id in `findings:` | {c['briefs_in_findings']} | {CEILINGS['briefs_in_findings']} |",
        f"| Records carrying `briefs:` | {c['records_with_briefs']} | — |",
        f"| Records with an empty `findings:` | {c['empty_findings_field']} | — |",
        f"| Findings in no card and declaring no `claim: none` | {c['claim_unset']} | {CEILINGS['claim_unset']} |",
        f"| Findings with a no-test declaration | {c['no_test_declared']} | — |",
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

    L += ["", "### D3 — finding ids with no file", "", "| Id | Records |", "|---|---|"]
    for fid, rids in data["dangling"].items():
        L.append(f"| {fid} | {len(rids)}: {', '.join('`%s`' % r for r in rids[:3])}"
                 f"{' …' if len(rids) > 3 else ''} |")

    L += ["", "## E — findings named by no claim card", "",
          "A finding need not carry a claim. Each of these needs reading once to "
          "confirm it asserts nothing a card should hold, then an explicit "
          "`**Claim:** none — <reason>` so the state is declared rather than absent.",
          ""]
    L += [f"- **{f['id']}** — `{f['file']}`"
          f"{' (mentions ' + ', '.join(f['cl_in_prose']) + ' in prose)' if f['cl_in_prose'] else ''}"
          for f in F if not f["claims"] and not f["claim_none"]] or ["*(none)*"]
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
    print(f"[coverage]   {'debt_only':<19} {c['debt_only']:>4}   "
          f"{'no_test_declared':<17} {c['no_test_declared']}")

    if args.check:
        over = [k for k in CEILINGS if c[k] > CEILINGS[k]]
        if over:
            print(f"[coverage] FAIL — above ceiling: {', '.join(over)}", file=sys.stderr)
            return 1
        print("[coverage] within every ceiling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
