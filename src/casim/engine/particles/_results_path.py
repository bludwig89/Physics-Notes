"""Locate `test-results/` from inside `casim.engine.particles` — roadmap C5.

Three migrated derivation scripts (`derive_generator_norm`,
`derive_lambda6_sextic`, `derive_weight_as_phase`) wrote their JSON to the
literal path ``"../test-results/<name>.json"``. That is relative to the
**working directory**, not to the file, so it only ever resolved when the script
was run from inside `ca-simulation/`; from the repo root it wrote outside the
repo, and after C5 moved the files four levels deeper it raised
``FileNotFoundError`` on import. The move exposed the bug rather than causing
it, and a path that depends on where you happened to `cd` is not something to
carry into `src/`.

Deliberately does not import `casim.suite.runner.find_repo_root`: an engine
kernel importing the suite layer inverts the dependency direction the C-roadmap
is trying to establish. This walks up from its own location instead, so it is
correct regardless of working directory and regardless of how deep the package
sits.
"""
from __future__ import annotations

import os

__all__ = ["results_path", "results_dir"]


def _find_results_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        candidate = os.path.join(here, "test-results")
        if os.path.isdir(candidate):
            return candidate
        parent = os.path.dirname(here)
        if parent == here:                       # reached the filesystem root
            raise RuntimeError(
                "cannot locate test-results/ above " + os.path.abspath(__file__))
        here = parent


_CACHE: str | None = None


def results_dir() -> str:
    """Absolute path to `test-results/`, resolved on first use and cached.

    Resolved lazily on purpose. Doing it at module scope would make importing
    this module — and therefore the three derivations that use it — raise
    `RuntimeError` anywhere the repo tree is absent, e.g. from an installed
    wheel (`pyproject.toml` is src-layout, so `casim` is installable). A helper
    that writes result files has no business refusing to import.
    """
    global _CACHE
    if _CACHE is None:
        _CACHE = _find_results_dir()
    return _CACHE


def results_path(name: str) -> str:
    """Absolute path to `test-results/<name>`."""
    return os.path.join(results_dir(), name)
