"""The test registry is complete, valid, and identical to what pytest runs.

Roadmap C7 acceptance, decision **D9**. Four claims, each of which was a real
defect before C7:

1. **Coverage.** Every test file has a record. A file with no record is a test
   nothing can see — the same failure mode the migration manifest closed for
   modules (C0.3) and the module registry closed for engine code (C3.2).
2. **Validity.** Every record validates: closed vocabularies for kind, tier,
   sector and exactness, and — the one with teeth — *a record that claims a real
   kind must declare a failure mode.* A test may be debt (``legacy_script``) or
   it may be falsifiable. It may not be neither, which is the state 70 files
   were in when P1 measured them.
3. **pytest ≡ registry.** The set of files bare ``pytest`` collects is exactly
   the registry's ``gate`` tier. If the two ever drift, the project has two
   answers to "what runs on every change", which is how it got here.
4. **The ledger is honoured.** Exactly the ``fully_superseded`` files sit at
   ``tier: archive``; partially-superseded files stay live, because P0.4 found
   11 of 14 "superseded" test files were a dead verdict wrapped around live,
   load-bearing algebra.
"""
from __future__ import annotations

import os

import pytest
import yaml

from casim.tests import registry as treg


def _repo() -> str:
    """Repo root. A function, not a module constant, so this file does no work
    at import — the C7.4 / P1.3 rule, which its own ratchet counts."""
    return os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))


def _ledger_path() -> str:
    return os.path.join(_repo(), "docs", "theory", "supersessions.yaml")


def test_every_test_file_has_a_record():
    missing = treg.check_coverage()
    assert not missing, (
        f"{len(missing)} test file(s) with no registry record: "
        f"{missing[:5]}{' …' if len(missing) > 5 else ''}. "
        f"Run tools/gen_test_registry.py.")


def test_every_record_validates():
    errs = treg.validate_all(treg.all_records())
    assert not errs, "registry validation errors:\n  " + "\n  ".join(errs[:10])


def test_no_migrated_record_lacks_a_failure_mode():
    """The structural closure of P1's `RAN` limbo.

    A record with no failure mode is *only* allowed to exist as declared debt.
    This is the assertion that makes the C7 ratchet meaningful: the debt cannot
    hide inside a record that looks migrated.
    """
    offenders = [r.id for r in treg.all_records()
                 if not r.has_failure_mode and r.kind != "legacy_script"]
    assert not offenders, (
        f"{len(offenders)} record(s) claim a real kind but cannot fail: "
        f"{offenders[:10]}")


def test_pytest_default_scope_equals_the_gate_tier():
    """Bare `pytest` (testpaths = tests/casim) IS the registry's gate tier."""
    on_disk = {p for p in treg.test_files() if p.startswith("tests/casim/")}
    index = {r.path: r for r in treg.all_records() if r.path}
    # what pytest will actually collect: the conftest hides archive + entry-driven
    collected = {p for p in on_disk
                 if not (index[p].tier == "archive" or index[p].entry)}
    gate = {r.path for r in treg.select(tier="gate")
            if r.path and not r.entry}
    assert collected == gate, (
        "pytest's default scope and the registry's gate tier disagree.\n"
        f"  pytest-only: {sorted(collected - gate)}\n"
        f"  registry-only: {sorted(gate - collected)}")


def test_gate_tier_records_are_fast_and_asserting():
    """A gate-tier record must be able to fail quickly, or it is not a gate."""
    for r in treg.select(tier="gate"):
        assert r.has_failure_mode, f"{r.id}: gate tier with no failure mode"
        assert r.kind != "legacy_script", (
            f"{r.id}: legacy_script cannot sit in the gate tier — it has no "
            f"failure mode by definition")


def _ledger_statuses() -> dict[str, str]:
    if not os.path.exists(_ledger_path()):
        return {}
    with open(_ledger_path(), encoding="utf-8") as fh:
        led = yaml.safe_load(fh) or {}
    out: dict[str, str] = {}
    for rec in led.get("supersessions") or []:
        for entry in rec.get("tests") or []:
            if entry.get("path"):
                out[entry["path"]] = entry.get("status", "live")
    return out


def test_archive_tier_is_exactly_the_fully_superseded_set():
    statuses = _ledger_statuses()
    if not statuses:
        pytest.skip("no supersession ledger")
    fully = {p for p, s in statuses.items() if s == "fully_superseded"}
    index = {r.path: r for r in treg.all_records() if r.path}
    archived = {r.path for r in treg.all_records()
                if r.tier == "archive" and r.path}
    # A retired file leaves tests/ for deprecated/tests/ (C7.6), so a
    # fully-superseded path only has to be archived while it is still present.
    still_present = {p for p in fully if p in index}
    assert archived == still_present, (
        f"archive tier {sorted(archived)} != still-present fully-superseded "
        f"{sorted(still_present)}")
    partial = {p for p, s in statuses.items()
               if s in ("partially_superseded", "historical_baseline")}
    wrongly_archived = sorted(p for p in partial if index.get(p)
                              and index[p].tier == "archive")
    assert not wrongly_archived, (
        f"partially-superseded files archived (P0.4's lesson — they carry live "
        f"algebra): {wrongly_archived}")


def test_declared_baselines_exist():
    """A `results:` path that does not exist is not a baseline."""
    bad = [(r.id, p) for r in treg.all_records() for p in r.results
           if not os.path.exists(os.path.join(_repo(), p))]
    assert not bad, f"records naming missing baselines: {bad[:10]}"


if __name__ == "__main__":                               # reduced-mode gate
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
            except Exception as exc:                     # noqa: BLE001
                if type(exc).__name__ == "Skipped":
                    print(f"  skip {name}")
                    continue
                failures += 1
                print(f"  ERROR {name}: {type(exc).__name__}: {exc}")
    c = treg.counts()
    print(f"\nregistry: {c['records']} records, {c['legacy_script']} legacy_script, "
          f"{c['gate']} gate tier")
    sys.exit(1 if failures else 0)
