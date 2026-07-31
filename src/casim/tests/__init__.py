"""casim.tests — the test registry (roadmap C7, decision **D9**).

A test in this project is **a parameter setting run through CASIM**, not a
standalone script. This package owns that idea:

  * :mod:`casim.tests.registry` — the record format, the loader, and the
    validation that gives a record teeth (a record cannot declare *no* failure
    mode unless it declares itself debt).
  * :mod:`casim.tests.runner`   — the one executor. ``casim test`` and ``pytest``
    both drive *this*, so they cannot diverge.

Usage
-----
    from casim.tests import registry as treg

    treg.get("F234-Wvc-triple-closure")
    treg.select(sector="particles", kind="assertion")
    treg.check_coverage()          # () when every test file has a record
"""
from __future__ import annotations

from . import registry, runner   # noqa: F401  (re-export for `casim.tests.registry`)

__all__ = ["registry", "runner"]
