"""
casim — cellular-automaton particle-physics model ("universe in a bottle").
===========================================================================

This package is the standalone-program layer described in
``roadmap-standalone-program.md`` (Phases A-C).  It is a *refactor, not a
rewrite*: the audited physics kernels in the repository's ``ca-simulation/``
directory remain the single source of truth.  ``casim`` adds the layer above
them — a simulation engine, channel registry (F91 propagator classification),
observers, scenario/YAML configuration, a result writer, and a CLI.

Design note (2026-06-04)
------------------------
The original flat ``ca_*.py`` modules are kept untouched so the ~95 existing
``run_*``/``test_*`` scripts and all internal ``import ca_bcc``-style imports
keep working verbatim.  On import, ``casim`` locates the sibling
``ca-simulation/`` directory and places it on ``sys.path``; the structured
sub-packages (``casim.lattice``, ``casim.fields.*``, ``casim.gravity``) are
thin re-export shims over those kernels.  Genuinely new code (engine, io,
analysis, cli) lives natively in the package.
"""
from __future__ import annotations

import os
import sys

__version__ = "0.1.0"


def _locate_legacy() -> str:
    """Return the absolute path to the repo's ``ca-simulation`` directory.

    Walk up from this file (``src/casim/__init__.py``) looking for a sibling
    ``ca-simulation`` folder.  Works for editable installs run from the repo.
    An override is available via the ``CASIM_LEGACY_DIR`` environment variable.
    """
    env = os.environ.get("CASIM_LEGACY_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(6):
        cand = os.path.join(cur, "ca-simulation")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise ImportError(
        "casim could not locate the legacy 'ca-simulation' directory. "
        "Set the CASIM_LEGACY_DIR environment variable to its path."
    )


LEGACY_DIR = _locate_legacy()
if LEGACY_DIR not in sys.path:
    sys.path.insert(0, LEGACY_DIR)
# The forks/ sub-directory hosts logical forks (e.g. F64 gravity fork).
_FORKS = os.path.join(LEGACY_DIR, "forks")
if os.path.isdir(_FORKS) and _FORKS not in sys.path:
    sys.path.insert(0, _FORKS)

__all__ = ["__version__", "LEGACY_DIR"]
