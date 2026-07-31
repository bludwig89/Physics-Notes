"""casim.engine.registry — the module registry (roadmap C3, decision **D11**).

Mirrors ``casim.constants``: where that registry owns the model's *constants*,
this one owns the model's *modules* — for every engine module, the sector it
belongs to, the findings it implements, its exactness class, its reachability,
and the tests and result artifacts that depend on it.

Two sources, one registry:

  * **Migrated kernels** (``origin="manifest"``) are read from
    ``docs/design/module-migration-manifest.yaml`` — the C0 product that C1–C9
    execute. A kernel appears here the moment its ``target`` file lands under
    ``src/casim/engine/``, so the registry stays in lock-step with the
    migration instead of being a second thing to keep in sync.
  * **The engine spine** (``origin="spine"``) — ``core.channel``,
    ``core.simulation`` and the rest — was already ``src/`` code, not a
    migrated ``ca-simulation`` kernel, so it has no manifest record and is
    declared here by hand. Small, stable list.

This is the data ``casim index`` consumes at C8, and the field that answers
P6's "67 of 106 kernels are unreachable" question as a *query* rather than a
survey: ``[m.name for m in all_modules() if m.reach != "driven"]``.

Usage
-----
    from casim.engine import registry as reg

    reg.get("lattice.bcc").findings          # ('F41', 'F175', 'F264')
    [m.name for m in reg.all_modules("lattice")]
    reg.check_coverage()                     # () when every engine module is registered
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Iterable

import yaml

from casim.constants import EXACTNESS_CLASSES

__all__ = [
    "Module", "MODULE_SECTORS", "register",
    "get", "all_modules", "by_sector", "by_finding",
    "engine_module_files", "unregistered_modules", "check_coverage",
]

# The seven sectors of the target tree (roadmap §4) plus the two homes that are
# not engine subpackages (`numerics` is `casim.numerics`; `forks` land under
# `engine/forks/` at C6).  Kept identical to the manifest's `sector` vocabulary.
MODULE_SECTORS = (
    "core", "lattice", "gauge", "particles", "interactions", "forks", "numerics",
)

_HERE = os.path.dirname(os.path.abspath(__file__))          # .../src/casim/engine
_SRC = os.path.dirname(os.path.dirname(_HERE))              # .../src
_REPO = os.path.dirname(_SRC)                              # repo root
_MANIFEST = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")
_ENGINE_REL = os.path.join("src", "casim", "engine")


# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Module:
    """One engine module. ``name`` is the dotted path below ``casim.engine``."""

    name: str                                   # e.g. "lattice.bcc"
    path: str                                   # repo-relative .py path
    sector: str
    findings: tuple[str, ...] = ()
    exactness: str | None = None                # None until C8.4 classifies it
    reach: str = "unknown"                      # driven | unreferenced | derive | ...
    reachable_from: tuple[str, ...] = ()        # channels; filled at C6
    tests: tuple[str, ...] = ()
    results: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    role: str = "kernel"                        # kernel | spine | fork | viz
    origin: str = "manifest"                    # manifest | spine
    # C6: the manifest's migration status, carried through so a fork's standing
    # is a QUERY and not a footnote. `fork_unclaimed` is not a defect — it is a
    # recorded alternative that was tested and rejected (roadmap §8), which is
    # exactly why C6 migrates forks instead of dropping them.
    status: str = "live"                        # live | partial | dead_candidate
    #                                           # | fork_live | fork_unclaimed


MODULES: dict[str, Module] = {}


def register(m: Module) -> Module:
    if m.sector not in MODULE_SECTORS:
        raise ValueError(
            f"module {m.name!r}: sector {m.sector!r} not one of {MODULE_SECTORS}")
    if m.exactness is not None and m.exactness not in EXACTNESS_CLASSES:
        raise ValueError(
            f"module {m.name!r}: exactness {m.exactness!r} not in "
            f"{sorted(EXACTNESS_CLASSES)}")
    MODULES[m.name] = m
    return m


# ---------------------------------------------------------------------------
# Queries
def get(name: str) -> Module:
    return MODULES[name]


def all_modules(sector: str | None = None) -> list[Module]:
    ms = sorted(MODULES.values(), key=lambda m: m.name)
    return [m for m in ms if sector is None or m.sector == sector]


def by_sector(sector: str) -> list[Module]:
    return all_modules(sector)


def by_finding(fid: str) -> list[Module]:
    return [m for m in all_modules() if fid in m.findings]


# ---------------------------------------------------------------------------
# Coverage — the acceptance gate for C3.2.  Every real module under
# `src/casim/engine/` must have a record.  A "real module" is any `.py` inside
# a sector subpackage; the top-level `engine/*.py` files are the C3 flat shims
# and `registry.py`/`__init__.py`, none of which is a physics module.
def engine_module_files() -> list[str]:
    """Repo-relative paths of the real engine modules (sector subpackages only).

    Walks the sector tree rather than listing one level, because C6's forks land
    a level deeper — ``engine/forks/<subsector>/<fork>.py`` — and a one-level
    listing would have reported full coverage while seeing none of the 46 forks.
    Coverage that cannot see a file cannot vouch for it.
    """
    out: list[str] = []
    for sub in MODULE_SECTORS:
        d = os.path.join(_HERE, sub)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames
                           if x not in ("__pycache__", ".pytest_cache")]
            for fn in sorted(filenames):
                if not fn.endswith(".py") or fn == "__init__.py":
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), _HERE)
                out.append(os.path.join(_ENGINE_REL, rel))
    return sorted(out)


def _dotted_of(rel_path: str) -> str:
    """`src/casim/engine/lattice/bcc.py` -> `lattice.bcc`."""
    rel = rel_path.split(_ENGINE_REL + os.sep, 1)[-1]
    rel = rel[:-3] if rel.endswith(".py") else rel
    return rel.replace(os.sep, ".")


def unregistered_modules() -> list[str]:
    """Engine module files on disk with no registry record. () means full coverage."""
    registered = {m.path.replace("/", os.sep) for m in MODULES.values()}
    missing = []
    for rel in engine_module_files():
        if rel.replace("/", os.sep) not in registered:
            missing.append(rel)
    return missing


def check_coverage() -> list[str]:
    """Alias kept for the gate script and C8; identical to unregistered_modules()."""
    return unregistered_modules()


# ---------------------------------------------------------------------------
# Population
def _register_from_manifest() -> None:
    """Register every migrated kernel whose target file exists under engine/."""
    if not os.path.exists(_MANIFEST):
        return
    with open(_MANIFEST, encoding="utf-8") as fh:
        recs = (yaml.safe_load(fh) or {}).get("modules", [])
    for r in recs:
        tgt = r.get("target", "")
        if _ENGINE_REL.replace(os.sep, "/") not in tgt.replace(os.sep, "/"):
            continue
        if not os.path.exists(os.path.join(_REPO, tgt)):
            continue                                    # not migrated yet
        name = _dotted_of(tgt)
        if name in MODULES:
            continue                                    # spine wins if pre-declared
        role = r.get("role", "kernel")
        if os.path.basename(tgt).startswith("_viz_"):
            role = "viz"
        register(Module(
            name=name,
            path=tgt,
            sector=r.get("sector", "core"),
            findings=tuple(r.get("findings") or ()),
            reach=r.get("reach", "unknown"),
            reachable_from=tuple(r.get("reachable_from") or ()),
            tests=tuple(r.get("tests") or ()),
            results=tuple(r.get("baselines") or ()),
            role=role,
            status=r.get("status", "live"),
            origin="manifest",
        ))


# The pre-existing engine spine — src/ code that predates the migration, so it
# carries no manifest record.  Sector "core"; declared by hand (D11).
_SPINE: tuple[Module, ...] = (
    Module("core.channel", "src/casim/engine/core/channel.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.observers", "src/casim/engine/core/observers.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.simulation", "src/casim/engine/core/simulation.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.channels", "src/casim/engine/core/channels.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.coupled", "src/casim/engine/core/coupled.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.tier3", "src/casim/engine/core/tier3.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.spectral_matter", "src/casim/engine/core/spectral_matter.py", "core",
           reach="driven", role="spine", origin="spine"),
    Module("core.blockspin", "src/casim/engine/core/blockspin.py", "core",
           findings=("F130", "F133", "F134"), reach="driven",
           role="spine", origin="spine"),
    Module("core.entanglement_register",
           "src/casim/engine/core/entanglement_register.py", "core",
           findings=("F212", "F214"), reach="driven",
           role="spine", origin="spine"),
    # Roadmap C5. Not a migrated kernel and carries no physics: it resolves
    # `test-results/` from the package's own location, replacing the
    # working-directory-relative `"../test-results/..."` that the three
    # migrated lepton-shape derivations wrote to.
    Module("particles._results_path",
           "src/casim/engine/particles/_results_path.py", "particles",
           exactness=None, reach="package-only",
           role="spine", origin="spine"),
)


def _register_spine() -> None:
    for m in _SPINE:
        register(m)


_register_spine()
_register_from_manifest()
