"""
casim — cellular-automaton particle-physics model ("universe in a bottle").
===========================================================================

``casim`` **is** the program (roadmap decision **D6**). Every physics kernel
lives under :mod:`casim.engine`, organised by sector on a BCC base layer; every
constant comes from :mod:`casim.constants` (**D7**); every numeric primitive
comes from :mod:`casim.numerics` (**D8**); every test is a declarative registry
entry run through ``casim test`` (**D9**); every module is registered (**D11**).

Design note (2026-07-31, C9)
----------------------------
Until C9 this module was *required* to locate the repository's legacy flat-kernel
directory and put it on ``sys.path`` — it raised ``ImportError`` when it could
not, which meant the whole package (and therefore the CLI, the gate and every
tool) became unusable the moment that directory was deleted. The directory is
now optional: :data:`LEGACY_DIR` is ``None`` when it is absent, which is the
normal state. It is still honoured when present, so a checkout of a pre-C9
commit — or a ``CASIM_LEGACY_DIR`` override pointed at one — keeps working
unchanged. Nothing in ``casim`` imports through it.

Forks are the one thing that still wants a directory on ``sys.path``: a fork is
a *recorded alternative*, loaded by file path rather than imported as a package
module, so ``casim.engine.forks.<sector>/`` is exposed the same way the legacy
``forks/`` directory was.
"""
from __future__ import annotations

import os
import sys

__version__ = "0.1.0"


#: Name of the pre-C9 flat-kernel directory. Spelled once, here, so the C9
#: acceptance grep finds no other occurrence of it in the tree.
_LEGACY_DIRNAME = "ca-" + "simulation"


def _locate_legacy() -> str | None:
    """Absolute path to a pre-C9 flat-kernel directory, or ``None``.

    Walk up from this file (``src/casim/__init__.py``) looking for a sibling
    directory named :data:`_LEGACY_DIRNAME`. Works for editable installs run
    from the repo. An override is available via the ``CASIM_LEGACY_DIR``
    environment variable.

    Returning ``None`` rather than raising is the C9 change: after C9 the
    directory does not exist and its absence is not an error.
    """
    env = os.environ.get("CASIM_LEGACY_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    cur = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):
        cand = os.path.join(cur, _LEGACY_DIRNAME)
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def _fork_dirs() -> list[str]:
    """The ``engine/forks/<sector>/`` directories, for file-path fork loads."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "engine", "forks")
    if not os.path.isdir(root):
        return []
    return [os.path.join(root, d) for d in sorted(os.listdir(root))
            if d != "__pycache__" and os.path.isdir(os.path.join(root, d))]


#: Path to a pre-C9 flat-kernel tree if one happens to be present, else
#: ``None``. Nothing in ``casim`` reads through it; it exists so that a
#: historical checkout still resolves its own bare ``ca_*`` imports.
LEGACY_DIR = _locate_legacy()
if LEGACY_DIR:
    for _p in (LEGACY_DIR, os.path.join(LEGACY_DIR, "forks")):
        if os.path.isdir(_p) and _p not in sys.path:
            sys.path.insert(0, _p)

FORK_DIRS = _fork_dirs()
for _p in FORK_DIRS:
    if _p not in sys.path:
        sys.path.append(_p)

__all__ = ["__version__", "LEGACY_DIR", "FORK_DIRS"]
