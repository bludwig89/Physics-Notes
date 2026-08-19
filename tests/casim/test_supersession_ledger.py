"""Roadmap P0.3/P0.4 — the supersession ledger gate.

`docs/theory/supersessions.yaml` is only useful if it stays true. This file
asserts that it does:

  * every finding, code path, and test path it names exists;
  * every file it classifies carries the matching docstring banner;
  * no file carries a banner the ledger does not know about (the reverse
    direction — a stray tombstone is as misleading as a missing one);
  * the schema is well formed and the vocabularies are closed.

The thing this deliberately does NOT do is enforce a pytest marker on
partially-superseded files. An earlier audit proposed marking ~14 files
superseded; on inspection exactly one was. Marking the other twelve would have
retired a large amount of live, load-bearing coverage — F62's lapse-mix sign
convention is production code, F52's factor-2 discriminator is still canonical
under F178, and F179's 3*delta* = Q check is now the model's own falsification
handle. So the unit of supersession here is a CHECK, named in the ledger and
restated in the banner, not a file.
"""
from __future__ import annotations

import ast
import os
import re
import sys

import yaml

try:
    import pytest
except ModuleNotFoundError:                                # pragma: no cover
    from test_constants_consistency import pytest         # type: ignore

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
_LEDGER_PATH = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")

sys.path.insert(0, os.path.join(_REPO, "tools"))

# `methodology` was added at roadmap C9 for the D2 -> D6 reversal. It is a
# separate kind rather than an overload of `superseded` because it has no
# findings on either side: `by:` and `superseded:` name DECISIONS (D-ids). The
# finding-existence assertion below therefore skips it.
KINDS = {"superseded", "reclassified", "demoted", "deprecated", "methodology",
         "retracted_by_review"}
DECISION_KINDS = {"methodology"}
# `retracted_by_review` (2026-08-04): a claim inside a finding withdrawn by an
# independent review rather than replaced by a successor finding. `superseded:`
# is legitimately EMPTY on such a record -- nothing took the claim's place --
# so the per-file `findings:` entry carries the dead/live split instead.
BASELINE_STATUSES = {"stale_by_design", "candidate", "live"}
STATUSES = {"fully_superseded", "partially_superseded", "historical_baseline",
            "sub_claim_superseded", "live"}

# A `methodology` record's `by:` names a decision -- usually a D-number, but
# sometimes a ROADMAP PHASE, because some decisions were taken at a phase
# boundary and never got a D-id (S14 retired the vispy viewer at P5.1). The
# pattern accepted both from 2026-08-04; before that S14 was red, which the
# 2026-08-04 triage recorded as an already-red baseline rather than a new break.
_DECISION_ID_RE = r"D\d+|[PC]\d+(?:\.\d+)?"
_FINDING_ID_RE = r"F\d+[a-z]?"
BANNER_RE = re.compile(
    r"\A\[(SUPERSEDED|PARTIALLY SUPERSEDED|HISTORICAL BASELINE|"
    r"PRE-DECISION FRAMING)\b[^\]]*\]")

_BANNER_FOR = {
    "fully_superseded": "SUPERSEDED",
    "partially_superseded": "PARTIALLY SUPERSEDED",
    "historical_baseline": "HISTORICAL BASELINE",
    "sub_claim_superseded": "SUB-CLAIM SUPERSEDED",
}

# Markdown banner (findings/, deprecated/findings/) -- the same labels, rendered
# as a blockquote after the H1. Added 2026-08-04 with the tool's markdown path.
MD_BANNER_RE = re.compile(
    r"\A> \*\*\[(SUPERSEDED|PARTIALLY SUPERSEDED|HISTORICAL BASELINE|"
    r"SUB-CLAIM SUPERSEDED)\b[^\]]*\]\*\*")


def _ledger() -> dict:
    with open(_LEDGER_PATH, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _module_docstring(rel_path: str) -> str | None:
    with open(os.path.join(_REPO, rel_path), "r", encoding="utf-8") as fh:
        try:
            tree = ast.parse(fh.read(), filename=rel_path)
        except SyntaxError:
            return None
    return ast.get_docstring(tree, clean=False)


def _entries():
    for rec in _ledger()["supersessions"]:
        for e in rec.get("tests") or []:
            yield rec, e


def _finding_entries():
    """The `findings:` blocks — markdown, blockquote banner.

    Separate from `_entries()` because the two carry DIFFERENT banner syntaxes
    in different file types, and collapsing them is how the original mechanism
    ended up reading `tests:` only.
    """
    for rec in _ledger()["supersessions"]:
        for e in rec.get("findings") or []:
            yield rec, e


def _md_head(rel_path: str) -> str:
    """Everything after the H1 — where a markdown banner lives."""
    with open(os.path.join(_REPO, rel_path), "r", encoding="utf-8") as fh:
        src = fh.read()
    m = re.match(r"\A(?:\ufeff)?(#[^\n]*\n)", src)
    return src[m.end():].lstrip("\n") if m else src.lstrip("\n")


# ---------------------------------------------------------------------------
@pytest.mark.exact
def test_ledger_schema_is_well_formed():
    led = _ledger()
    assert led["version"] == 1
    ids = set()
    for rec in led["supersessions"]:
        rid = rec["id"]
        assert rid not in ids, f"duplicate ledger id {rid}"
        ids.add(rid)
        assert rec["kind"] in KINDS, f"{rid}: unknown kind {rec['kind']!r}"
        assert rec["by"], f"{rid}: nothing supersedes it"
        assert rec.get("scope", "").strip(), f"{rid}: no scope"
        assert rec.get("reason", "").strip() or rec["kind"] == "deprecated", \
            f"{rid}: no reason given"
        pat = (_DECISION_ID_RE if rec["kind"] in DECISION_KINDS
               else _FINDING_ID_RE)
        for f in list(rec["by"]) + list(rec.get("superseded") or []):
            assert re.fullmatch(pat, f), \
                f"{rid}: malformed {'decision' if pat[0] == 'D' else 'finding'}" \
                f" id {f!r}"
        for e in (list(rec.get("tests") or [])
                  + list(rec.get("findings") or [])):
            assert e["status"] in STATUSES, f"{rid}: bad status {e['status']!r}"
        # `baselines:` — artifact provenance (2026-07-31). Validated by
        # casim.tests.ledger so the rules live with the code that reads them.
        for e in rec.get("baselines") or []:
            assert e["status"] in BASELINE_STATUSES, \
                f"{rid}: bad baseline status {e['status']!r}"


@pytest.mark.exact
def test_every_ledger_path_exists():
    """A ledger that cites a moved file is a ledger nobody can trust."""
    missing = []
    for rec in _ledger()["supersessions"]:
        for key in ("tests", "code", "baselines", "findings"):
            for item in rec.get(key) or []:
                if not os.path.exists(os.path.join(_REPO, item["path"])):
                    missing.append(f"{rec['id']} -> {item['path']}")
        for e in rec.get("tests") or []:
            r = e.get("replacement")
            if r and not os.path.exists(os.path.join(_REPO, r)):
                missing.append(f"{rec['id']} -> replacement {r}")
    assert not missing, "ledger cites paths that do not exist:\n  " + \
                        "\n  ".join(missing)


@pytest.mark.exact
def test_baseline_provenance_is_well_formed():
    """Every `baselines:` entry names a real artifact and can be cleared.

    The teeth are in casim.tests.ledger.validate: a `stale_by_design` or
    `candidate` entry with no `clears_by:` is a permanent excuse, and a `live`
    entry with no `accepted_by:` is a re-blessing with no author.
    """
    import sys as _sys
    _sys.path.insert(0, os.path.join(_REPO, "src"))
    from casim.tests import ledger
    errs = ledger.validate(_REPO)
    assert not errs, "baseline provenance errors:\n  " + "\n  ".join(errs)


@pytest.mark.exact
def test_a_candidate_baseline_never_suppresses_a_failure():
    """`candidate` must not excuse drift — only a decided entry may.

    This is the one property of the whole baseline-provenance mechanism that can
    quietly rot. If `candidate` ever started suppressing failures, the category
    would become a place to park inconvenient reds, which is exactly the failure
    mode P0.4 documented for file-level supersession claims.
    """
    import sys as _sys
    _sys.path.insert(0, os.path.join(_REPO, "src"))
    from casim.tests import ledger
    for b in ledger.candidates(_REPO):
        assert not b.suppresses_drift, (
            f"{b.path}: a `candidate` entry is suppressing drift")
    for b in ledger.stale_by_design(_REPO):
        assert b.suppresses_drift, f"{b.path}: stale_by_design does not suppress"
    # And the all-or-nothing rule: a mixed set is not stale.
    stale = [b.path for b in ledger.stale_by_design(_REPO)]
    cand = [b.path for b in ledger.candidates(_REPO)]
    if stale and cand:
        assert not ledger.all_stale(stale + cand[:1], _REPO), (
            "all_stale() accepted a mixed set — an undeclared drifted artifact "
            "must keep the record red")


@pytest.mark.exact
def test_every_finding_referenced_has_a_finding_file():
    """A finding the ledger names must exist as a file — live or retired.

    ``deprecated/findings/`` was added 2026-08-03 when F16-F19 were retired
    (see that directory's acceptance rule in ``deprecated/README.md``). A
    retirement MOVES a finding, it does not delete it, so the invariant this
    test defends — the ledger never names a finding that cannot be read — is
    unchanged; only the search path widened. Checking `findings/` alone would
    have made the ledger's own supersession entries the thing that broke it,
    which is backwards: naming a superseded finding is the point of the record.
    """
    have = set()
    for d in ("findings", os.path.join("deprecated", "findings")):
        full = os.path.join(_REPO, d)
        if not os.path.isdir(full):
            continue
        have |= {m.group(0) for f in os.listdir(full)
                 if (m := re.match(r"F\d+", f))}
    missing = []
    for rec in _ledger()["supersessions"]:
        if rec["kind"] in DECISION_KINDS:
            continue                      # names decisions (D6…), not findings
        for f in (list(rec["by"]) + list(rec.get("superseded") or [])
                  + list(rec.get("reclassified") or [])
                  + list(rec.get("demoted") or [])):
            if f not in have:
                missing.append(f"{rec['id']} -> {f}")
    assert not missing, "ledger names findings with no findings/F*.md:\n  " + \
                        "\n  ".join(missing)


@pytest.mark.exact
@pytest.mark.parametrize(
    "path,status",
    [(e["path"], e["status"]) for _, e in _entries() if e["status"] != "live"],
    ids=[f"{os.path.basename(e['path'])}:{e['status']}"
         for _, e in _entries() if e["status"] != "live"],
)
def test_classified_file_carries_its_banner(path, status):
    doc = _module_docstring(path)
    assert doc is not None, f"{path} has no module docstring to carry a banner"
    m = BANNER_RE.match(doc.lstrip("\n"))
    assert m, (
        f"{path} is classified {status!r} in the ledger but carries no banner. "
        f"Run `python3 tools/apply_supersession_banners.py`.")
    assert m.group(1) == _BANNER_FOR[status], (
        f"{path} carries a {m.group(1)!r} banner but the ledger says "
        f"{status!r}. One of the two is wrong.")


@pytest.mark.exact
@pytest.mark.parametrize(
    "path,status",
    [(e["path"], e["status"]) for _, e in _finding_entries()
     if e["status"] != "live"],
    ids=[f"{os.path.basename(e['path'])}:{e['status']}"
         for _, e in _finding_entries() if e["status"] != "live"],
)
def test_classified_finding_carries_its_banner(path, status):
    """The half of the mechanism that did not exist until 2026-08-04.

    `findings/` is where a *reader* meets a superseded result, and it was the
    one directory with no banner enforcement at all — the tool returned
    `no-docstring` for markdown and never read `findings:`.
    """
    head = _md_head(path)
    m = MD_BANNER_RE.match(head)
    assert m, (
        f"{path} is classified {status!r} in the ledger but carries no banner "
        f"after its H1. Run `python3 tools/apply_supersession_banners.py`.")
    assert m.group(1) == _BANNER_FOR[status], (
        f"{path} carries a {m.group(1)!r} banner but the ledger says "
        f"{status!r}. One of the two is wrong.")


@pytest.mark.exact
def test_no_orphan_banners():
    """A tombstone the ledger does not know about is a lie with a timestamp."""
    known = {e["path"] for _, e in _entries()}
    # Files may also be stamped from the `code:` lists (e.g. the pre-decision
    # framing note on a derive script); those are legitimate.
    for rec in _ledger()["supersessions"]:
        for item in rec.get("code") or []:
            known.add(item["path"])

    known |= {e["path"] for _, e in _finding_entries()}

    orphans = []
    for root in ("tests", "src"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(_REPO, root)):
            dirnames[:] = [d for d in dirnames
                           if d not in ("__pycache__", ".pytest_cache")]
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), _REPO)
                rel = rel.replace(os.sep, "/")
                if rel in known:
                    continue
                doc = _module_docstring(rel)
                if doc and BANNER_RE.match(doc.lstrip("\n")):
                    orphans.append(rel)

    # findings/ and deprecated/findings/ — the directories this sweep did not
    # walk until 2026-08-04, and the ones where four orphan tombstones (F20,
    # F22, F64, F176b) had been sitting since May. Only GENERATED banners count:
    # a finding may still carry hand-written editorial notes as blockquotes, and
    # flagging those would make the check noise.
    for d in ("findings", "deprecated/findings"):
        full = os.path.join(_REPO, d)
        if not os.path.isdir(full):
            continue
        for fn in sorted(os.listdir(full)):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            rel = f"{d}/{fn}"
            if rel in known:
                continue
            if MD_BANNER_RE.match(_md_head(rel)):
                orphans.append(rel)

    assert not orphans, (
        "files carry a supersession banner but are absent from the ledger:\n  "
        + "\n  ".join(orphans) +
        "\n\nEither add them to docs/theory/supersessions.yaml or remove the banner.")


@pytest.mark.exact
def test_banners_are_current():
    """The stamped banner text must match what the ledger would generate now.

    Without this, editing the ledger silently leaves stale tombstones behind.
    """
    from apply_supersession_banners import main as _stamp_main   # noqa: E402

    argv = sys.argv[:]
    sys.argv = ["apply_supersession_banners.py", "--check"]
    try:
        rc = _stamp_main()
    finally:
        sys.argv = argv
    assert rc == 0, ("supersession banners are stale. Run "
                     "`python3 tools/apply_supersession_banners.py`.")


def test_supersessions_reach_the_documents_that_cite_them():
    """The other half of the loop: banners go INTO the superseded file, and this
    goes OUT to the rubric rows and claim cards that cite it.

    Added 2026-08-17 with ledger record S20. Completeness row B9 graded its
    electroweak leg against F115 for three consecutive reports while F138 and
    F231 had superseded that reading since June and July, and every check here
    stayed green -- because F115 had no ledger entry (so no banner, so nothing
    for `test_no_orphan_banners` to find) and because `check_claims.py` rule 4
    fires only on a WHOLLY superseded card, never on a partial. A partial
    supersession cited without its replacement had no owner. It has one now.
    """
    from check_superseded_citations import main as _cite_main    # noqa: E402

    argv = sys.argv[:]
    sys.argv = ["check_superseded_citations.py"]
    try:
        rc = _cite_main()
    finally:
        sys.argv = argv
    assert rc == 0, ("a grading document cites a superseded finding without "
                     "naming what replaced it. Add the replacement F-number to "
                     "the same table row, or say `superseded` / name the ledger "
                     "record in it. Run `make citations V=1` for the list.")


def test_the_citation_matcher_actually_fires():
    """The negative control, and it is the B9 row itself.

    A checker nobody has seen fail is not evidence. This pins the three
    behaviours the rule depends on against the exact row shape that went wrong.
    """
    from check_superseded_citations import _unit_ok, _FN          # noqa: E402

    dead = {"F115": {"by": {"F138", "F231"}, "records": {"S20-x"}}}
    bare = "| B9 | Running of alpha, EW couplings | QUANT | F251, F261, F115 |"
    named = "| B9 | Running of alpha, EW couplings | QUANT | F261, F138, F231, F115 |"
    marked = "| B9 | ... | F115 (superseded, see S20) |"

    assert not _unit_ok(set(_FN.findall(bare)), bare, "F115", dead), (
        "the matcher does NOT fire on the exact row completeness-2026-08-07 "
        "carried for three reports — it would have caught nothing")
    assert _unit_ok(set(_FN.findall(named)), named, "F115", dead), (
        "naming the replacement must clear the row, or the check is unusable")
    assert _unit_ok(set(_FN.findall(marked)), marked, "F115", dead), (
        "an explicit acknowledgement must clear the row")


@pytest.mark.exact
def test_supersession_summary_is_reported():
    counts: dict[str, int] = {}
    for _, e in _entries():
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    recs = len(_ledger()["supersessions"])
    print(f"\n[supersessions] {recs} records; test classifications: "
          + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    assert counts.get("fully_superseded", 0) >= 1


# ---------------------------------------------------------------------------
def _run_standalone() -> int:
    checks = [
        ("schema_is_well_formed", test_ledger_schema_is_well_formed),
        ("every_ledger_path_exists", test_every_ledger_path_exists),
        ("every_finding_has_a_file", test_every_finding_referenced_has_a_finding_file),
        ("no_orphan_banners", test_no_orphan_banners),
        ("banners_are_current", test_banners_are_current),
        ("citations_reach_citing_docs",
         test_supersessions_reach_the_documents_that_cite_them),
        ("citation_matcher_fires", test_the_citation_matcher_actually_fires),
        ("summary", test_supersession_summary_is_reported),
    ]
    for rec, e in _entries():
        if e["status"] == "live":
            continue
        checks.append((
            f"banner {os.path.basename(e['path'])}",
            lambda p=e["path"], s=e["status"]: test_classified_file_carries_its_banner(p, s),
        ))
    for rec, e in _finding_entries():
        if e["status"] == "live":
            continue
        checks.append((
            f"md banner {os.path.basename(e['path'])}",
            lambda p=e["path"], s=e["status"]: test_classified_finding_carries_its_banner(p, s),
        ))
    failures = []
    for label, fn in checks:
        try:
            fn()
        except AssertionError as exc:
            failures.append(f"{label}: {exc}")
            print(f"FAIL  {label}")
    print(f"\n[supersessions] {len(checks) - len(failures)} PASS, "
          f"{len(failures)} FAIL")
    for f in failures:
        print(f"\n--- FAIL {f}")
    return 1 if failures else 0


if __name__ == "__main__":                                 # pragma: no cover
    sys.exit(_run_standalone())
