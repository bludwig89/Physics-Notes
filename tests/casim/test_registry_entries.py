"""Run the gate-tier registry entry points under pytest — roadmap C7.3 (**D9**).

A record that names an ``entry:`` is not a file pytest collects; it is a
callable the registry points at, with declared ``params:`` and an ``expect:``
block. This module is how those records reach ``pytest``, so that

    pytest
    casim test --tier gate

execute the **same objects**. ``tests/conftest.py`` hides the underlying files
from collection precisely so nothing runs twice under two contracts.

Nothing happens at import (C7.4): the parametrisation is built in
``pytest_generate_tests``, which runs at collection, and the entry point's
module is imported only when the record is actually run.
"""
from __future__ import annotations

from casim.tests import registry as treg
from casim.tests import runner as trunner


def pytest_generate_tests(metafunc):
    """Parametrise over gate-tier records that name an entry point."""
    if "rec" not in metafunc.fixturenames:
        return
    recs = [r for r in treg.select(tier="gate") if r.entry]
    metafunc.parametrize("rec", recs, ids=[r.id for r in recs])


def test_registry_entry(rec):
    res = trunner.run_record(rec)
    assert res.status in ("PASS", "SKIP"), (
        f"{rec.id} [{rec.kind}] -> {res.status}: {res.detail}")


def test_entry_driven_records_are_hidden_from_file_collection():
    """No record may be both a pytest file and a registry entry point.

    If a file both defines `test_*` functions and is named as an `entry:`
    record, the conftest hides the file — but the registry should not be
    ambiguous in the first place, because the two contracts can disagree about
    what "pass" means.
    """
    ambiguous = [r.id for r in treg.all_records()
                 if r.entry and r.evidence.get("pytest_funcs")
                 and r.kind == "assertion"]
    assert not ambiguous, (
        f"records that are both a pytest file and an entry point: {ambiguous}. "
        f"Pick one contract.")
