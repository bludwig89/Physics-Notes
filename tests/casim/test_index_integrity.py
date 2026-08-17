"""`casim index` is idempotent, complete, and able to say no — roadmap C8.

The four acceptance criteria of C8, as assertions rather than a session note:

1. **Idempotent.** Regenerating on a clean tree produces a zero diff. Every
   generated file is timestamp-free by construction, so this is a byte
   comparison; the only exclusions are `manifest.json`'s `generated` and
   `git_sha`, the two keys its own builder has always excluded.
2. **No empty cell the registry could fill.** `tests-index.md`'s Results column
   was 104-of-339 empty under the old filename-prefix heuristic. It is now the
   record's declared `results:`, so a row is empty only when the record declares
   nothing — never because a matcher missed.
3. **The exactness inventory is not behind its own tree.** The hand-typed header
   was 125 findings stale and nothing said so; the header is generated now, so
   the metric reads 0 or the index has not been run.
4. **Finding numbers are audited.** Ten numbers are currently used twice — all
   declared in `docs/design/finding-numbers.yaml`. An *undeclared* collision
   fails, which is the point: three of them happened invisibly.

Nothing runs at import (the P1.3 / C7.4 rule); each test builds what it needs.
"""
from __future__ import annotations

import os


def _repo() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))


def test_index_is_idempotent():
    from casim import index as cindex
    res = cindex.check()
    assert not res["errors"], f"index generation errored: {res['errors']}"
    assert not res["stale"], (
        f"`casim index` is not idempotent — stale target(s): {res['stale']}. "
        f"Run `make indexes`.")


def test_every_generated_target_is_covered():
    from casim import index as cindex
    res = cindex.check()
    assert set(res["targets"]) == set(cindex.TARGETS), (
        f"targets missing from the build: "
        f"{set(cindex.TARGETS) - set(res['targets'])}")


def test_tests_index_has_no_cell_the_registry_could_fill():
    """A declared baseline must appear in the index — the C8.1 criterion."""
    from casim.index import tests as itests
    from casim.tests import registry as treg

    rel, text, _ = itests.render(_repo())
    for r in treg.all_records():
        if not r.results:
            continue
        assert f"`{r.id}`" in text, f"{r.id} is missing from {rel}"
        for p in r.results:
            assert os.path.basename(p) in text, (
                f"{rel} omits {p}, which record {r.id} declares as a baseline")


def test_inventory_is_not_behind_the_tree():
    from casim.index import exactness
    st = exactness.staleness(_repo())
    assert st["generated_header"], (
        "the inventory has no generated header block — run `casim index`")
    assert st["findings_behind"] == 0, (
        f"exactness inventory header says {st['header_finding']} but the newest "
        f"finding is {st['newest_finding']} ({st['findings_behind']} behind)")


def test_inventory_coverage_is_complete_and_reported_per_rule():
    from casim.index import exactness
    rows, stats = exactness.harvest(_repo())
    assert stats["with_residual"] > 0
    assert len(rows) == stats["with_residual"], (
        f"{stats['with_residual'] - len(rows)} residual-bearing entries are "
        f"invisible in the generated tables")
    # The three rules must add up. If they ever do not, a row was classified by
    # something that is not one of the three, which is the failure mode P1.5's
    # partial existed to avoid.
    assert (stats["declared"] + stats["record"] + stats["signature"]
            == len(rows)), "row count does not match the per-rule tallies"
    coverage = len(rows) / stats["with_residual"]
    assert coverage >= 0.95, f"inventory coverage {coverage:.1%} < 95%"


def test_finding_numbers_are_declared():
    from casim.index import findings
    a = findings.audit_numbers(_repo())
    assert not a["undeclared_duplicates"], (
        f"finding number(s) used twice with no entry in "
        f"docs/design/finding-numbers.yaml: {a['undeclared_duplicates']}")
    assert not a["undeclared_gaps"], (
        f"undeclared finding-number gap(s): {a['undeclared_gaps']}")
    assert not a["undeclared_unnumbered"], (
        f"finding file(s) with no F<number>- prefix and no declaration: "
        f"{a['undeclared_unnumbered']}")
    assert not a["stale_declared_duplicates"], (
        f"finding-numbers.yaml declares duplicates that no longer exist "
        f"{a['stale_declared_duplicates']} — a stale exception silently re-arms "
        f"the next collision")
    # The gaps-side twin, live since 2026-08-05. Under block reservation a gap
    # was permanent and a gap entry could not go stale; under one-at-a-time
    # allocation `status: free` MEANS "the next finding spends this", so an
    # entry naming a number whose file now exists is a spent number still
    # advertising itself as available — which hands the same number to two
    # sessions. Deleting the entry is the act of spending it.
    assert not a["stale_declared_gaps"], (
        f"finding-numbers.yaml still marks {a['stale_declared_gaps']} "
        f"`status: free` but the file(s) now exist — delete the entry; "
        f"deleting it IS the act of spending the number")
    # And the allocator must hand back a number nobody wrote at. If this ever
    # points at an existing file the backlog logic has inverted and the next
    # session is being told to create a duplicate.
    assert a["next_free"] not in a["numbers_used"], (
        f"NEXT FREE NUMBER F{a['next_free']} already has a finding file")


def test_module_registry_reaches_the_code_index():
    """The C8.1 upgrade: code-index carries registry fields, not a docstring."""
    from casim.engine import registry as mreg
    from casim.index import code

    _, text, _ = code.render(_repo())
    for m in mreg.all_modules()[:25]:          # a sample keeps the gate fast
        assert f"`{m.name}`" in text, f"{m.name} missing from code-index.md"
    assert "| Module | Sector | Status | Reach |" in text, (
        "code-index.md lost its registry columns")


if __name__ == "__main__":                     # reduced-mode gate
    import sys
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  PASS {name}")
            except AssertionError as exc:
                failures += 1
                print(f"  FAIL {name}: {exc}")
            except Exception as exc:           # noqa: BLE001
                failures += 1
                print(f"  ERROR {name}: {type(exc).__name__}: {exc}")
    sys.exit(1 if failures else 0)
