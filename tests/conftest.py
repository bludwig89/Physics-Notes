"""pytest configuration for the whole tests/ tree.

Subtrees: casim/ (package suite), findings/ (test_F*.py finding verifications),
priority/ (GR/QM/QFT priority battery), runners/ (standalone run_* scripts),
falsification/ (spec briefs, no collectable tests).

Registers the exactness markers, puts src/ and ca-simulation/ on sys.path so
every subtree imports without an editable install, and after a run regenerates
the casim-scoped exactness inventory.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
for _p in (os.path.join(_REPO, "src"), os.path.join(_REPO, "ca-simulation")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def pytest_configure(config):
    config.addinivalue_line("markers", "exact: residual is algebraically zero")
    config.addinivalue_line("markers",
                            "machine_precision: holds to the float/FFT floor")
    config.addinivalue_line("markers", "slow: long run, excluded by default")


def pytest_sessionfinish(session, exitstatus):
    """Regenerate the exactness inventory after the suite runs."""
    try:
        from casim.analysis.inventory import generate
        path = generate()
        print(f"\n[casim] regenerated exactness inventory: {path}")
    except Exception as e:  # pragma: no cover
        print(f"\n[casim] inventory generation skipped: {e}")
