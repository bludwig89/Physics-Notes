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

KINDS = {"superseded", "reclassified", "demoted", "deprecated"}
STATUSES = {"fully_superseded", "partially_superseded", "historical_baseline",
            "live"}
BANNER_RE = re.compile(
    r"\A\[(SUPERSEDED|PARTIALLY SUPERSEDED|HISTORICAL BASELINE|"
    r"PRE-DECISION FRAMING)\b[^\]]*\]")

_BANNER_FOR = {
    "fully_superseded": "SUPERSEDED",
    "partially_superseded": "PARTIALLY SUPERSEDED",
    "historical_baseline": "HISTORICAL BASELINE",
}


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
        for f in list(rec["by"]) + list(rec.get("superseded") or []):
            assert re.fullmatch(r"F\d+", f), f"{rid}: malformed finding id {f!r}"
        for e in rec.get("tests") or []:
            assert e["status"] in STATUSES, f"{rid}: bad status {e['status']!r}"


@pytest.mark.exact
def test_every_ledger_path_exists():
    """A ledger that cites a moved file is a ledger nobody can trust."""
    missing = []
    for rec in _ledger()["supersessions"]:
        for key in ("tests", "code"):
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
def test_every_finding_referenced_has_a_finding_file():
    findings_dir = os.path.join(_REPO, "findings")
    have = {m.group(0) for f in os.listdir(findings_dir)
            if (m := re.match(r"F\d+", f))}
    missing = []
    for rec in _ledger()["supersessions"]:
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
def test_no_orphan_banners():
    """A tombstone the ledger does not know about is a lie with a timestamp."""
    known = {e["path"] for _, e in _entries()}
    # Files may also be stamped from the `code:` lists (e.g. the pre-decision
    # framing note on a derive script); those are legitimate.
    for rec in _ledger()["supersessions"]:
        for item in rec.get("code") or []:
            known.add(item["path"])

    orphans = []
    for root in ("tests", "ca-simulation", "src"):
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
        ("summary", test_supersession_summary_is_reported),
    ]
    for rec, e in _entries():
        if e["status"] == "live":
            continue
        checks.append((
            f"banner {os.path.basename(e['path'])}",
            lambda p=e["path"], s=e["status"]: test_classified_file_carries_its_banner(p, s),
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
