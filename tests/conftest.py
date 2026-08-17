"""pytest configuration for the whole tests/ tree.

Subtrees: casim/ (package suite), findings/ (test_F*.py finding verifications),
priority/ (GR/QM/QFT priority battery), runners/ (standalone run_* scripts),
falsification/ (spec briefs, no collectable tests).

Registers the exactness markers, puts src/ on sys.path so every subtree imports
without an editable install, and after a run regenerates the casim-scoped
exactness inventory. (Before C9 this also added the legacy kernel tree;
that tree is gone and every test imports from `casim.engine`.)

Roadmap C7.3 — **pytest delegates to the test registry.**
--------------------------------------------------------
``tests/registry/*.yaml`` is the single specification of what runs. pytest does
not get its own opinion:

  * a record at ``tier: archive`` is not collected (it replaces the P0
    ``superseded`` marker with a registry field);
  * a record that names an ``entry:`` is not collected **as a file** — it is
    executed as a registry entry point by ``tests/casim/test_registry_entries.py``,
    so it cannot run twice under two different contracts;
  * ``tests/casim/test_registry_integrity.py`` asserts the converse — that every
    file pytest *does* collect has a record, and that the registry's ``gate``
    tier is exactly the default ``pytest`` scope.

That is what makes "``pytest`` and ``casim test --tier gate`` produce identical
pass/fail sets" a structural property rather than a coincidence to re-check.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
_p = os.path.join(_REPO, "src")
if _p not in sys.path:
    sys.path.insert(0, _p)


def _registry_index():
    """{repo-relative path -> TestRecord}, or {} if the registry is unavailable.

    Never raises: a broken registry must fail in
    ``test_registry_integrity.py`` with a readable assertion, not by making
    collection explode for the whole tree.
    """
    try:
        from casim.tests import registry as treg
        return {r.path: r for r in treg.all_records() if r.path}
    except Exception:                                    # pragma: no cover
        return {}


def pytest_ignore_collect(collection_path, config):      # noqa: ARG001
    """Registry-driven collection (C7.3). See the module docstring."""
    path = str(collection_path)
    if not path.endswith(".py"):
        return None
    rel = os.path.relpath(path, _REPO).replace(os.sep, "/")
    rec = _registry_index().get(rel)
    if rec is None:
        return None                                      # unknown: let pytest look
    if rec.tier == "archive":
        return True                                      # superseded per the ledger
    if rec.entry:
        return True                                      # run as a registry entry
    return None


def pytest_configure(config):
    config.addinivalue_line("markers", "exact: residual is algebraically zero")
    config.addinivalue_line("markers",
                            "machine_precision: holds to the float/FFT floor")
    config.addinivalue_line("markers", "slow: long run, excluded by default")
    config.addinivalue_line(
        "markers", "superseded: every claim in this file has been replaced "
                   "(docs/theory/supersessions.yaml); excluded from the gate")
    config.addinivalue_line(
        "markers", "historical_baseline: retains a superseded object as the "
                   "standing exclusion record; runs, but is not live canon")


def pytest_sessionfinish(session, exitstatus):
    """Regenerate the exactness inventory after the suite runs."""
    try:
        from casim.analysis.inventory import generate
        path = generate()
        print(f"\n[casim] regenerated exactness inventory: {path}")
    except Exception as e:  # pragma: no cover
        print(f"\n[casim] inventory generation skipped: {e}")
