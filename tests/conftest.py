"""pytest configuration for the casim suite (roadmap Phase F).

Registers the exactness markers and, after a run, regenerates the casim-scoped
exactness inventory from the same canonical checks the tests assert on.
"""
from __future__ import annotations

import os
import sys

# Make the src-layout package importable when running pytest from the repo root
# without an editable install.
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(os.path.dirname(_HERE), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)


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
