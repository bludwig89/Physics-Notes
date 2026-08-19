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
    migrated legacy kernel, so it has no manifest record and is
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

import json
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
_GRAPH = os.path.join(_REPO, "docs", "design", "module-graph.json")


def _graph_reach() -> dict:
    """``{repo-relative path: reach}`` from the module graph, if it exists.

    **V7.4 (audit V).** The graph computes reachability from one import closure
    per channel module and types four categories — ``driven``, ``package-only``,
    ``test-only``, ``unreferenced``, plus ``entry-script``.  The C0 manifest
    carries a *frozen string* that predates most of the migration, takes only
    two values across 181 records, and disagrees with the graph on the driven
    count.  ``code-index.md`` renders the registry's column, so a reader was
    being pointed at the less informative of two sources that should be one.

    Degrades quietly: if the graph is absent or unreadable the manifest value
    stands, so the registry never hard-depends on a generated artifact.
    """
    try:
        with open(_GRAPH, encoding="utf-8") as fh:
            nodes = (json.load(fh) or {}).get("nodes", {})
    except (OSError, ValueError):
        return {}
    return {p: n["reach"] for p, n in nodes.items()
            if isinstance(n, dict) and n.get("reach")}


def _register_from_manifest() -> None:
    """Register every migrated kernel whose target file exists under engine/."""
    if not os.path.exists(_MANIFEST):
        return
    graph_reach = _graph_reach()
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
            # V7.4 (audit V, 2026-08-01): the module GRAPH is the authority on
            # reachability, not the frozen manifest string. Before this, every
            # record carried whatever `reach` the C0 manifest happened to hold,
            # which collapsed the graph's four categories into two and disagreed
            # with the graph on the driven count (49 vs 52). The manifest value
            # is kept as the fallback for anything the graph does not type.
            reach=graph_reach.get(tgt.replace(os.sep, "/"),
                                  r.get("reach", "unknown")),
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
    # Roadmap P3.1's spike, F267. Answers the one item F265 §9 left explicitly
    # open: the fermion walk's periodicity in k is sqrt3*fcc, so the cubic FFT
    # cube is 4/(3*sqrt3) of ONE zone — not a fundamental domain and not an
    # integer number of copies, so the gauge side's "divide by 4" does not
    # transfer. Crucially it introduces no doubler (1 omega=0 per branch, no
    # omega=pi), which is why D1 does not re-open.
    Module("lattice.derive_walk_bz_measure",
           "src/casim/engine/lattice/derive_walk_bz_measure.py", "lattice",
           findings=("F267", "F265", "F250"), exactness="exact",
           reach="entry-script", role="derivation", origin="spine",
           tests=("tests/findings/test_F267_walk_bz_measure.py",),
           results=("test-results/F267_walk_bz_measure.json",)),
    # Roadmap P3.2 (blocker B2) — the engine's physical clock. Before this the
    # engine had a tick counter and nine private `dt` config lookups across
    # seven channel classes meaning four different things; 18 of 46 scenarios
    # were desynchronised and nothing said so. F268.
    Module("core.clock", "src/casim/engine/core/clock.py", "core",
           findings=("F268",), exactness="exact", reach="driven",
           reachable_from=("simulation",), role="spine", origin="spine",
           tests=("tests/casim/test_engine_clock.py",)),
    # Roadmap P3.3 (blocker B3) — the typed exchange bus. Replaces
    # registration-order Gauss-Seidel with a declared dependency graph, and a
    # dangling coupling name with a build-time error. F269.
    Module("core.graph", "src/casim/engine/core/graph.py", "core",
           findings=("F269",), exactness="exact", reach="driven",
           reachable_from=("simulation",), role="spine", origin="spine",
           tests=("tests/casim/test_exchange_bus.py",)),
    # F271 — the k-resolved dielectric photon propagator lives in the existing
    # gauge.photon module (manifest-registered); recorded here as a spine entry
    # only if the manifest record cannot carry the finding. See F271.
    # F282 — the primordial-sector no-go (completeness-2026-08-02 gap #1, K4).
    # An analytical kernel, not a channel: it evaluates slow-roll parameters
    # against the model's own potentials and shows every candidate fails by
    # O(10) because a/ell_reduced = 3^(1/4) puts the cutoff below M_Pl.
    Module("interactions.cosmology_primordial",
           "src/casim/engine/interactions/cosmology_primordial.py",
           "interactions",
           findings=("F282",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F282_primordial_sector_nogo.py",),
           results=("test-results/F282_primordial_sector_nogo.json",)),
    # F283/F284 — can the lattice be elastic, and if not what is expansion?
    # Companion analytical kernel to cosmology_primordial: proves the F282
    # obstruction is invariant under a -> s*a (correcting F282 falsifier #5),
    # bounds elasticity by Gdot/G and GW170817, and fixes the first resolvable
    # epoch H_max = 3^(-3/4) M_Pl on the rigid substrate that leaves.
    Module("interactions.cosmology_lattice_elasticity",
           "src/casim/engine/interactions/cosmology_lattice_elasticity.py",
           "interactions",
           findings=("F283", "F284"), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F283_F284_lattice_elasticity.py",),
           results=("test-results/F283_F284_lattice_elasticity.json",)),
    # F285 — executes the three initial-condition directions F284 handed on.
    # Via the model's own F106 Poisson law the primordial index IS the initial
    # density slope, and every natural measure gives 0, 4 or exactly 1.
    Module("interactions.cosmology_initial_conditions",
           "src/casim/engine/interactions/cosmology_initial_conditions.py",
           "interactions",
           findings=("F285",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F285_initial_condition_measure.py",),
           results=("test-results/F285_initial_condition_measure.json",)),
    # F286 — what could supply the 3.5% tilt. Uses Planck's RUNNING (not just
    # the index) to prove a second scale must enter logarithmically, extracts
    # the log class's one parameter-free prediction, and rejects the
    # delta*/(2pi) near-miss on a pre-registered look-elsewhere count.
    Module("interactions.cosmology_second_scale",
           "src/casim/engine/interactions/cosmology_second_scale.py",
           "interactions",
           findings=("F286",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F286_second_scale.py",),
           results=("test-results/F286_second_scale.json",)),
    # F295 — Ben's alpha/G test question, which exposed that F286 mis-read its
    # own T1: the allowed p = 0 branch is a scale-free ANOMALOUS DIMENSION, not
    # the trivial case. No second scale needed; dn_s/dlnk = 0 exactly.
    Module("interactions.cosmology_anomalous_dimension",
           "src/casim/engine/interactions/cosmology_anomalous_dimension.py",
           "interactions",
           findings=("F295",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F295_anomalous_dimension.py",),
           results=("test-results/F295_anomalous_dimension.json",)),
    # F288 — K11: linear structure formation. The model's own gravity law
    # fixes growth with ZERO free functions (mu = 1 with no k from F106/F178,
    # no time dependence from F79/F284, no slip from F64 AB=1) where the EFT
    # of dark energy has two. gamma_g = 6/11 and the Meszaros solution exact.
    Module("interactions.cosmology_growth",
           "src/casim/engine/interactions/cosmology_growth.py",
           "interactions",
           findings=("F288",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F288_structure_formation.py",),
           results=("test-results/F288_structure_formation.json",)),
    # F296 — literature placement: holographic cosmology computes n_s-1 from a
    # 3D QFT with no inflaton. Retrodicts HC's published tension with F286 T1
    # (validating the instrument), names the operator, and excludes the naive
    # field-content reading by the tensor-to-scalar ratio.
    Module("interactions.cosmology_holographic",
           "src/casim/engine/interactions/cosmology_holographic.py",
           "interactions",
           findings=("F296",), exactness="quantitative", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F296_holographic.py",),
           results=("test-results/F296_holographic.json",)),
    # F310 — G2/K3: the in-repo answer to "does the model claim a 3D dual?".
    # No, and it needs none: the t=0 state of a rigid 3D automaton IS a 3D
    # Euclidean measure, so F296's operator is present by construction. Gives
    # n_s = 3 - 2y and gamma == y - 1 identically, so gamma is the anomalous
    # part of the model's OWN block-spin eigenvalue; F130's measured spectrum
    # is all-integer, which is why no earlier route could produce one. Predicts
    # n_t = 2 exactly and r ~ 1e-118, repairing F296 L5's exclusion.
    Module("interactions.cosmology_critical_measure",
           "src/casim/engine/interactions/cosmology_critical_measure.py",
           "interactions",
           findings=("F310",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F310_critical_measure.py",),
           results=("test-results/F310_critical_measure.json",)),
    # F311 — completeness gap #5: the three numbers no report had re-derived.
    # (a) B9's Delta_alpha(M_Z) is proved untouched by S12-F277 by REINSTATING
    # the refold (Pi4 bit-identical, Pi3 moves 3 orders) and its 0.24 % residual
    # is identified as the two-loop leptonic term (100.6 % of it), closing the
    # gap 155x. (b) All ten `candidate` baselines re-run: zero regressions; the
    # three permanent reds were one hole in casim.baselines._VOLATILE_RE, fixed
    # here. (c) The two Lambda pictures are SEQUENTIAL not parallel -- F193
    # postdates F192 by 13 h and closes its candidate (i).
    Module("interactions.derive_gap5_adjudication",
           "src/casim/engine/interactions/derive_gap5_adjudication.py",
           "interactions",
           findings=("F311",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F311_gap5_adjudication.py",),
           results=("test-results/F311_gap5_adjudication.json",)),
    # F312 — A6: Gleason's premises on the two non-Abelian factors, closing
    # F304's residual 3. Writes out [J^a(x),J^b(y)] = i delta_xy f^abc J^c(x)
    # (off-site commutator literally 0 for both groups, so the whole non-Abelian
    # structure is intra-site), proves the record observable is a gauge singlet,
    # and reduces the frame condition by Schur so the internal index drops out
    # for ANY compact group. SU(3)_c also clears Gleason's d>=3 alone.
    Module("interactions.qi_born_nonabelian",
           "src/casim/engine/interactions/qi_born_nonabelian.py",
           "interactions",
           findings=("F312",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F312_born_nonabelian.py",),
           results=("test-results/F312_born_nonabelian.json",)),
    # F297 — K2: Big-Bang nucleosynthesis. The first module in the tree that
    # COMPUTES a light-element abundance rather than quoting a BBN bound. The
    # expansion side is entirely model-native (structural G from F79/F107, the
    # F178 source law, Gdot/G = 0 from F284, N_eff = 3.044 from the model's own
    # content); eta_b is external by construction (F238/K8). Excludes the
    # demoted energy-only law at 17.6 sigma in Y_p, and bounds m_n - m_p to
    # +-0.0056 MeV, where F122's own check used +-1 MeV.
    Module("interactions.cosmology_bbn",
           "src/casim/engine/interactions/cosmology_bbn.py",
           "interactions",
           findings=("F297",), exactness="quantitative", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F297_bbn.py",),
           results=("test-results/F297_bbn_light_elements.json",)),
    # F300 — G10: lattice-native thermodynamics. The partition function on the
    # DERIVED paired-spinor dispersion, not a continuum ansatz. Closed-form EoS
    # corrections (40 pi^2/441, 16 pi^2/1323, 4 pi^2/49, ratio 15/2 exact);
    # F297's continuum p = rho/3 assumption graded and safe by 44 orders at BBN.
    # Fine-grained entropy conserved, coarse-grained rises TIME-SYMMETRICALLY,
    # and the free sector reaches a GGE, not Gibbs (2N conserved charges).
    Module("interactions.thermodynamics",
           "src/casim/engine/interactions/thermodynamics.py",
           "interactions",
           findings=("F300",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F300_thermodynamics.py",),
           results=("test-results/F300_lattice_thermodynamics.json",)),
    # F309 — K2/G10: g_*(T) and g_*s(T) from the model's OWN content, closing
    # completeness gap #4 and F300's next step #1. The fermionic BZ sums with
    # the branch-odd term KEPT (it does not cancel; squared, it carries 3/7 of
    # the coefficient): C_u^F = 310 pi^2/441 = (31/4) C_u^gamma, and C_u/C_w
    # = 15/2 survives, so the ratio is degree-3 homogeneity and not statistics.
    # The BBN-window content is derived, not imported, and the one non-null
    # substitution — the model's own m_e (F121) — moves Y_p by +0.032 sigma.
    Module("interactions.thermodynamics_gstar",
           "src/casim/engine/interactions/thermodynamics_gstar.py",
           "interactions",
           findings=("F309",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F309_gstar.py",),
           results=("test-results/F309_gstar_model_content.json",)),
    # F15 — the closed-form SR-2 Lorentz-violation coefficients. Declared HERE,
    # in the spine, deliberately: the frozen C0 manifest carries this file as
    # `status=dead_candidate, reach=package-only, tests=(), findings=(),
    # exactness=None`, and spine wins over manifest (see _register_from_manifest).
    # It is not dead. It is the sole implementation of an exact algebraic result
    # that backs four rows of docs/status/exactness-inventory.md and had no test
    # of any kind until 2026-08-03 — defect 1 of
    # docs/reviews/F01-F15-review-2026-08-03.md, whose blind agent re-derived
    # all four coefficients by an independent route and confirmed them.
    # `reach="standalone"`: an analytical kernel, not wired to a channel.
    Module("interactions.derive_beta_LV",
           "src/casim/engine/interactions/derive_beta_LV.py",
           "interactions",
           findings=("F12", "F15"), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F15_closed_form_beta_LV.py",),
           results=("test-results/F15_closed_form_beta_LV.json",)),
    # Same shape, same reason, one finding later. The frozen C0 manifest also
    # carries derive_velocity_addition as `status=dead_candidate, findings=()`
    # (manifest:4289-4299) — and `code-index.md` consequently attributed it to
    # F15 rather than to F22, which is how F22 came to have no test coverage at
    # all. Promoted here by the F22 remediation (review 2026-08-04, verdict
    # OVERSTATED). exactness="exact" applies to the rho identity ONLY: F22's
    # claim that the SR boost acts exactly on (omega, k) is false at O(vk) and
    # its retraction is escalated -- see the finding's Corrections table.
    Module("interactions.derive_velocity_addition",
           "src/casim/engine/interactions/derive_velocity_addition.py",
           "interactions",
           findings=("F15", "F22"), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F22_rho_identity.py",),
           results=("test-results/F22_rho_identity_and_offshell.json",)),
    # ------------------------------------------------------------------
    # Gap #5 of docs/status/completeness-2026-08-02.md — the dead_candidate
    # and unreferenced-module pass, executed 2026-08-03.
    #
    # The frozen C0 manifest carries ten modules as `status=dead_candidate,
    # findings=(), tests=(), exactness=None`. The pass re-read every one
    # against the findings, the exactness inventory and the open-derivations
    # ledger. Exactly ONE was dead (core._viz_live_display, now in
    # deprecated/code/, ledger S14). One was a tested-and-rejected branch, so
    # it is a FORK, not dead code (S15). The other eight were never dead —
    # they were never WIRED, and five of them back live exactness-inventory
    # rows while their findings were cited as CLOSED. `dead_candidate` was
    # measuring "nothing imports this", which for an analytical derivation
    # kernel is its normal condition, not a verdict.
    #
    # Spine wins over manifest (see _register_from_manifest), so these records
    # are the correction. The manifest stays frozen, per CLAUDE.md.
    # Full reasoning: docs/audits/module-disposition-2026-08-03.md.
    # ------------------------------------------------------------------

    # F245 (open-derivation L1). Backs four exactness-inventory rows. Its
    # verify() only PRINTED, which is why the claim could not fail; the pass
    # added check_closed_forms() and the gate record F245-l1-curl-coefficient.
    Module("interactions.derive_curl_subleading",
           "src/casim/engine/interactions/derive_curl_subleading.py",
           "interactions",
           findings=("F7", "F245"), exactness="machine", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml#F245-l1-curl-coefficient",)),
    # F246 (open-derivation L2). Same shape as F245: closed-form result,
    # inventory row, no failure mode until 2026-08-03.
    Module("interactions.derive_f26_dispersion",
           "src/casim/engine/interactions/derive_f26_dispersion.py",
           "interactions",
           findings=("F26", "F30", "F246"), exactness="machine",
           reach="standalone", role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml#F246-l2-curl-coefficient",)),
    # F247 (open-derivation Q3). A documented FREE INPUT — the deuteron cannot
    # separate g_omega from the F113 quark-Pauli core. The pass also repointed
    # its working-directory-relative artifact path at _results_path and routed
    # its bare numpy import through the D8 facade.
    Module("interactions.run_q3_omega_degeneracy",
           "src/casim/engine/interactions/run_q3_omega_degeneracy.py",
           "interactions",
           findings=("F113", "F240", "F247"), exactness="quantitative",
           reach="standalone", role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml#F247-q3-omega-degeneracy",),
           results=("test-results/Q3_omega_degeneracy.json",)),
    # Finding 15's velocity-addition extension. Backs an exactness-inventory
    # row. Not dead; still has no test record — the pass records that as its
    # first recommended follow-up rather than writing a fifth record on a
    # finding number it did not claim.
    Module("interactions.derive_velocity_addition",
           "src/casim/engine/interactions/derive_velocity_addition.py",
           "interactions",
           findings=("F15",), exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="partial"),
    # F142 Q1 — why the colour-dielectric tension does NOT map onto F86's exact
    # sigma = 2 pi v^2 n. A closed NEGATIVE with an inventory row; a negative
    # result with no test is still a claim that cannot regress visibly.
    Module("interactions.derive_dielectric_noconfine",
           "src/casim/engine/interactions/derive_dielectric_noconfine.py",
           "interactions",
           findings=("F139", "F142"), exactness="quantitative",
           reach="standalone", role="derivation", origin="spine",
           status="partial"),
    # The lattice-perturbation-theory Feynman-rule generator for the Wilson
    # SU(3) action. The most consequential misfiling of the ten: it serves d1,
    # and open-derivations.md unifies E3 = Q1 = Q2 = d1 as "the one model-action
    # one-loop background-field constant" — i.e. the single biggest genuinely
    # open target in the project. Marked `partial`: real, unfinished, and the
    # opposite of dead.
    Module("core.lpt_generator",
           "src/casim/engine/core/lpt_generator.py", "core",
           exactness=None, reach="standalone",
           role="kernel", origin="spine", status="partial"),
    # F207's materials companion — the finite-conductivity + thermal Lifshitz
    # reduction eta(a) needed to compare against Lamoreaux / Mohideen / Decca
    # sphere-plate data. The one honest open question of the ten: it is a
    # genuine orphan (nothing imports it, no __main__, no test, no finding, no
    # inventory row) but it is UNBUILT, not SUPERSEDED, so retiring it to
    # deprecated/code/ would require asserting a supersession that never
    # happened. Left in place, correctly labelled, with the decision handed to
    # Ben rather than taken quietly. Also still imports numpy directly (D8).
    Module("interactions.qed_casimir_materials",
           "src/casim/engine/interactions/qed_casimir_materials.py",
           "interactions",
           findings=("F207",), exactness=None, reach="unreferenced",
           role="kernel", origin="spine", status="dead_candidate"),
    # The E1 weight-as-phase attack, moved out of particles/ on 2026-08-03.
    # Both routes it tried are closed negatives (F253 topological, F256
    # dynamical), which under this repo's own definition makes it a FORK —
    # "a tested and rejected or live-exploratory branch; it preserves the
    # falsification record and is not dead code" (CLAUDE.md). It is the
    # evidence that founding decision 7 and open-derivations row E1 lean on
    # when they say every alternative is closed. Ledger S15.
    Module("forks.particles.derive_weight_as_phase",
           "src/casim/engine/forks/particles/derive_weight_as_phase.py",
           "forks",
           findings=("F175", "F230", "F253", "F255", "F256"), exactness=None,
           reach="unreferenced", role="fork", origin="spine",
           status="fork_live"),

    # ---------------------------------------------------------------------
    # Gap #5 of docs/status/completeness-2026-08-02.md — the dead_candidate
    # and unreferenced-module pass, executed 2026-08-03. Full reasoning per
    # module in docs/audits/module-disposition-2026-08-03.md.
    #
    # The finding of that pass, in one line: of the ten modules the frozen C0
    # manifest carries as `dead_candidate`, ONE was dead. The other nine were
    # UN-WIRED, and five of them were backing live exactness-inventory rows
    # while registered as dead code. `dead_candidate` was never a verdict —
    # dead-code-proposal.md says so in its own header — but it had been read
    # as one for three days, so the records below say what is true instead.
    #
    # Declared here rather than in the manifest because the manifest is a
    # frozen historical record (CLAUDE.md) and spine wins over manifest in
    # _register_from_manifest. Nothing in the manifest is edited.
    # ---------------------------------------------------------------------

    # F245 (open-derivation L1). Backs four exactness-inventory rows and a
    # finding cited as CLOSED; had no test of any kind because its verify()
    # only PRINTED. `check_closed_forms` and record F245-l1-curl-coefficient
    # added by the same pass.
    Module("interactions.derive_curl_subleading",
           "src/casim/engine/interactions/derive_curl_subleading.py",
           "interactions",
           findings=("F7", "F245"), exactness="machine", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml#F245-l1-curl-coefficient",)),
    # F246 (open-derivation L2). Same shape as F245: a live inventory row, a
    # CLOSED finding, and a module registered dead. The structural leg — all
    # even-power dispersion corrections vanish identically, so the F26 photon
    # carries no CPT-odd Lorentz violation — is what the GRB/AGN bounds are
    # compared against, which makes this one load-bearing downstream.
    Module("interactions.derive_f26_dispersion",
           "src/casim/engine/interactions/derive_f26_dispersion.py",
           "interactions",
           findings=("F26", "F30", "F246"), exactness="machine",
           reach="standalone", role="derivation", origin="spine",
           status="live",
           tests=("tests/registry/interactions.yaml#F246-l2-curl-coefficient",)),
    # F247 (open-derivation Q3). A documented FREE INPUT, which is exactly the
    # kind of result that rots unwatched: nothing fails when a negative stops
    # being true. `check_degeneracy` asserts the linear valley that IS the
    # degeneracy. The same pass also fixed two structural defects here — a
    # working-directory-relative artifact path (repointed at _results_path)
    # and a bare numpy import (routed through the D8 facade).
    Module("interactions.run_q3_omega_degeneracy",
           "src/casim/engine/interactions/run_q3_omega_degeneracy.py",
           "interactions",
           findings=("F113", "F240", "F247"), exactness="quantitative",
           reach="standalone", role="derivation", origin="spine",
           status="live",
           tests=("tests/registry/interactions.yaml#F247-q3-omega-degeneracy",),
           results=("test-results/Q3_omega_degeneracy.json",)),
    # F301 — finite-a boost covariance. Closes rubric row A2's standing
    # residual and the F24 remediation's DEFERRED item 10. The observable is
    # the Poincare-algebra defect D_i = (1/2c^2)d_i(Omega^2) - k_i = d_i Phi,
    # which is choice-free: it is a gradient, it is the COMPLETE obstruction
    # ([K,P] never fails and the [K,K] defect reduces to the same D_i), and it
    # is invariant under K -> K + f(k). Load-bearing downstream because it
    # turns F246's even-power vanishing into a boost-covariance ORDER, and
    # because it supplies the BCC rho(m) F22 recorded as missing.
    Module("interactions.derive_boost_covariance",
           "src/casim/engine/interactions/derive_boost_covariance.py",
           "interactions",
           findings=("F301", "F22", "F24", "F246", "F26"),
           exactness="exact", reach="standalone", role="derivation",
           origin="spine", status="live",
           tests=("tests/registry/interactions.yaml#F301-boost-covariance-defect",),
           results=("test-results/F301_boost_covariance.json",)),
    # Finding 15's velocity-addition extension. Live inventory row, no test
    # record yet — un-wired, not dead. Left `partial` deliberately: the status
    # says "this is real and unguarded", which is a truer statement than
    # either `live` or `dead_candidate`. Recommended next record in the
    # disposition report.
    Module("interactions.derive_velocity_addition",
           "src/casim/engine/interactions/derive_velocity_addition.py",
           "interactions",
           findings=("F15",), exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="partial"),
    # F142 Q1's negative result — why the colour-dielectric tension does NOT
    # map onto F86's exact sigma = 2 pi v^2 n. A no-go with a live inventory
    # row. Same disposition as above: un-wired, not dead.
    Module("interactions.derive_dielectric_noconfine",
           "src/casim/engine/interactions/derive_dielectric_noconfine.py",
           "interactions",
           findings=("F86", "F139", "F142"), exactness="quantitative",
           reach="standalone", role="derivation", origin="spine",
           status="partial"),
    # The lattice-perturbation-theory Feynman-rule generator for the Wilson
    # SU(3) action. The single most consequential mis-classification of the
    # ten: this serves d1, and open-derivations.md records d1 as E3 = Q1 = Q2,
    # i.e. ONE constant that closes three of the project's three genuinely
    # distinct open targets. It generates the vertices from the action rather
    # than transcribing them, which is the whole point (see
    # docs/theory/d1-kns-vertex-status.md on the fabrication risk). Not dead;
    # `partial` because the programme it serves is unfinished.
    Module("core.lpt_generator",
           "src/casim/engine/core/lpt_generator.py", "core",
           findings=("F162",), exactness="quantitative", reach="standalone",
           role="kernel", origin="spine", status="partial"),
    # The E1 attack on weight-as-phase, moved to engine/forks/particles/ by
    # the same pass. Both routes it tried are closed negatives (F253 excludes
    # the topological origin, F256 the dynamical one), and under this repo's
    # own definition a tested-and-rejected branch is a FORK, which "preserves
    # the falsification record and is not dead code". Ledger record
    # S15-E1-weight-as-phase-attack-is-a-fork.
    Module("forks.particles.derive_weight_as_phase",
           "src/casim/engine/forks/particles/derive_weight_as_phase.py",
           "forks",
           findings=("F230", "F253", "F255", "F256"), exactness=None,
           reach="standalone", role="fork", origin="spine",
           status="fork_live"),
    # The one module of the ten that the pass could NOT clear, re-declared
    # here so that its `dead_candidate` is a DECISION rather than an inherited
    # manifest string. It is a genuine orphan: nothing imports it, it has no
    # __main__, no test record, no finding names it, and it backs no
    # exactness-inventory row. But it is not SUPERSEDED — it is a real
    # capability that was never wired (the Lifshitz finite-conductivity +
    # thermal reduction factor eta(a) that turns F207's ideal Casimir law into
    # something comparable with Lamoreaux 1997 / Mohideen-Roy 1998 / Decca
    # 2007). Moving it to deprecated/code/ would require naming a supersession
    # in docs/theory/supersessions.yaml that did not happen, and the ledger is
    # not a place to park things. It also still imports numpy directly (D8).
    # Left in place, awaiting Ben's call: wire it to F207 with a record, or
    # retire it with a stated reason. See the disposition report.
    Module("interactions.qed_casimir_materials",
           "src/casim/engine/interactions/qed_casimir_materials.py",
           "interactions",
           findings=("F207",), exactness=None, reach="unreferenced",
           role="kernel", origin="spine", status="dead_candidate"),
    # F291 — why d = 3 (completeness-2026-08-02 rubric row A1, the first entry
    # of the ABSENT table). An analytical kernel, not a channel: it computes the
    # rank/kernel/cokernel of the walk's Bloch-vector Jacobian, counts the
    # isotropy-invariant intra-branch mass terms, and solves the bivector =
    # vector condition, showing that TWO independent routes each select d = 3
    # from structure the model had already adopted for other reasons.
    Module("lattice.dimensionality",
           "src/casim/engine/lattice/dimensionality.py",
           "lattice",
           findings=("F291", "F292"), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F291_dimension_selectors.py",
                  "tests/findings/test_F292_higher_multiples.py"),
           results=("test-results/F291_dimension_selectors.json",
                    "test-results/F292_higher_multiples.json")),

    # F316 — closes F313's LAST import. The Pell descent that F313 sec.6 cited
    # from Dubickas-Steuding Thm 2 is proved here over the Laurent ring, where
    # D-S's hypothesis "deg f = 0 => f constant" is FALSE (deg(1+w^-1) = 0 and
    # 1+w^-1 is not a unit; the units of R are the monomials). Replacement: a
    # two-sided width from the Newton polytope, which vanishes exactly on units,
    # plus the step D-S has no analogue of — UNITARITY makes every Newton
    # polytope centrally symmetric. The descent then drops D(b) by exactly D(u)
    # per step onto {+-1, +-A^+-1}. Audit kernel, not a channel.
    Module("lattice.laurent_pell",
           "src/casim/engine/lattice/laurent_pell.py",
           "lattice",
           findings=("F316",), exactness="machine", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F316_laurent_pell.py",),
           results=("test-results/F316_laurent_pell.json",)),

    # F313 — the "+1".  Where `dimensionality` selects the SPATIAL 3, this
    # module computes the Cayley-graph/update split that F291 sec.6 assumed:
    # the commutant of the BCC update inside the local homogeneous unitaries is
    # 2-dimensional and free, det splits it into exactly the shift lattice
    # (U(1) x Z^3) and exactly the powers of the update (the Pell group of
    # R[sqrt(1-u^2)], infinite cyclic), so d_time = rank su(2) = 1 from the
    # same s = 2 that bounds d_space by dim su(2) = 3.  Hand-rolled exact
    # Laurent arithmetic over Q(i) — sympy cannot expand A^8 here.  Audit
    # kernel, not a channel.
    Module("lattice.time_signature",
           "src/casim/engine/lattice/time_signature.py",
           "lattice",
           findings=("F313",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F313_time_signature.py",),
           results=("test-results/F313_time_signature.json",)),

    # F315 — F313 falsifier 5. The second dispersive commuting flow V = I (x) A
    # that F313 sec.9 measured on the FREE composite cell does not survive the
    # model's interactions: a homogeneous antisymmetrised two-particle sector of
    # the model's own walk shows V broken maximally (|dphi_V| ~ pi) by both the
    # contact (F217/F77) and photon-exchange (F68) kernels, and the O(G)
    # DEFORMATION obstructed on resonant elements, so no dressed V survives
    # either. Carries its own integrable positive control, without which a
    # verdict of "V dies" would be worthless. Audit kernel, not a channel.
    Module("lattice.time_signature_interacting",
           "src/casim/engine/lattice/time_signature_interacting.py",
           "lattice",
           findings=("F315",), exactness="machine", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F315_V_interaction.py",),
           results=("test-results/F315_V_interaction.json",)),

    # F302 — which spinor bilinear is a spatial 3-vector, and which sectors use
    # it. An audit kernel, not a channel: it proves eps = i*sigma_2 is the
    # object that converts dagger covariance into transpose covariance
    # (U^T eps U = det(U) eps, exact for any 2x2), measures the
    # 2 (n_hat . y_hat)^2 amplitude law of the retired transpose bilinear, and
    # checks every production W / Z / gluon construction for the same defect.
    # The audit closes negative: no live gauge sector carries it.
    Module("gauge.derive_bilinear_so3",
           "src/casim/engine/gauge/derive_bilinear_so3.py",
           "gauge",
           findings=("F302",), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F302_bilinear_so3.py",),
           results=("test-results/F302_bilinear_so3.json",)),

    # F306 — the curl-residual supersession (ledger S18). Not a new file: the
    # analytic-amplitude reading and its gate entry live in gauge/bilinear.py
    # alongside the original, deliberately, because maxwell_curl_residual is
    # left bit-for-bit unchanged (four call sites depend on its numbers) and the
    # two readings must be runnable side by side -- that comparison IS the
    # finding. Recorded here so the registry knows bilinear.py now carries F306.
    #
    # F20 remediation (review 2026-08-03, verdict OVERSTATED). The closed forms
    # the propagation demo was missing: the EXACT on-axis identity
    # omega(k x_hat) = k * c_lat (true at the u level bit-for-bit, both
    # branches), the group velocity dw/dk_x = c_lat * n_hat_x, its massive
    # counterpart, and the finite-width packet prediction c_lat * <n_hat_x^2>
    # for a fixed seed spinor vs c_lat * <n_hat_x> for a branch-pure one -- the
    # factor-of-two the finding's own mechanism was missing. Also owns the
    # wrap-free measured run, which is what turns a 0.37% demonstration into a
    # 1e-12 gate.
    Module("lattice.wavepacket",
           "src/casim/engine/lattice/wavepacket.py",
           "lattice",
           findings=("F20", "F26"), exactness="exact", reach="standalone",
           role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F20_wavepacket_group_velocity.py",),
           results=("test-results/F20_wavepacket_group_velocity.json",)),
    #
    # F314. The photon counterpart of lattice.wavepacket, and the closure of the
    # DEFERRED item the F20 remediation left behind: F20 item (3) claimed "the
    # photon exists and moves end-to-end" with the sigma-bilinear composite that
    # S1-F69-sigma-bilinear-photon retired, so the model had no real-space
    # demonstration that ITS OWN photon -- the paired-spinor photon of F67/F68/F69
    # -- propagates. Owns the closed-form pair group velocity on all three axes
    # (the c_lat*n_hat_i form is an x-axis-only identity), the exact on-axis
    # statement dOmega_pair/dk_x = c_lat at every k, and the wrap-free measured
    # run that turns F105's percent-level periodic-box beam demo into a 7.8e-16
    # gate. The propagator itself is gauge.photon, unmodified.
    Module("gauge.photon_packet",
           "src/casim/engine/gauge/photon_packet.py",
           "gauge",
           findings=("F314", "F20", "F69", "F105"), exactness="exact",
           reach="standalone", role="kernel", origin="spine", status="live",
           tests=("tests/findings/test_F314_photon_packet_propagation.py",),
           results=("test-results/F314_photon_packet_propagation.json",)),
    #
    # F280 — completeness-2026-08-04 gap #3. The bookkeeping layer that lets
    # d_1 be stated WITHOUT an absolute quadrature normalisation, which is the
    # restriction F287 sec.6 imposed when it measured the absolute b_0 recovery
    # at 0.955 and traced it to the cube not being a fundamental domain of the
    # sqrt(3)-fcc-periodic rule kernel. Carries no quadrature of its own: the
    # integrand is gauge.bgfield_loop's and the Wilson reference numbers are
    # F163's. What is new is the master identity (every term a difference), the
    # slope-normalised estimator that is exactly invariant under the F272-class
    # measure factor, and the three-leg budget that turns the open piece from
    # "the whole number" into one leg of three.
    # F305 — the lattice Feynman rules of the GENUINE BCC gauge action (the
    # 4-bond rhombus), derived by the same multilinear link expansion as
    # core.lpt_generator with only the loop word changed. Closes F265 sec.9
    # item 1 for the vertex half and supplies a genuine fundamental domain for
    # the gauge side (WS cell of the BCC reciprocal lattice; cube/BZ = 4).
    Module("gauge.lpt_bcc_vertex",
           "src/casim/engine/gauge/lpt_bcc_vertex.py",
           "gauge",
           findings=("F305", "F265", "F278", "F162", "F163"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F305_bcc_rhombic_vertices.py",)),

    # F324 -- the N_c bracket.  F298's C7 support {2,3} (imported) paired with
    # the Z_2 doublet parity of the DERIVED SU(2)_L (prior art: Baer & Wiese
    # 2001), closing the interval on N_c = 3 with no measured number, no
    # three-constituent baryon and no dependence on the X1 fork.  Six premises,
    # all named in the finding's section 0.
    Module("gauge.derive_ncolour_bracket",
           "src/casim/engine/gauge/derive_ncolour_bracket.py",
           "gauge",
           findings=("F324", "F317", "F318", "F298", "F293", "F279",
                     "F27", "F75", "F144"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F324_ncolour_bracket.py",),
           results=("test-results/F324_ncolour_bracket.json",)),
           
    # F307 — F280's subtracted slope-normalised estimator run action-consistently
    # on one code path (vertices AND propagator from the same action per side,
    # each on its own Brillouin zone). The machinery is closed; the NUMBER is not
    # quotable at n <= 20 (b0 recovery 0.41-0.49 on the BCC side) and the record's
    # S3 leg is red by design. Also demonstrates an F272/F277-class refold still
    # live in gauge.lpt_selfenergy.
    Module("gauge.lpt_d1_action_consistent",
           "src/casim/engine/gauge/lpt_d1_action_consistent.py",
           "gauge",
           findings=("F307", "F305", "F280", "F287", "F272", "F277"),
           exactness="bracketed", reach="standalone",
           role="derivation", origin="spine", status="partial",
           tests=("tests/findings/test_F307_action_consistent_d1.py",)),

    Module("gauge.lpt_d1_subtracted",
           "src/casim/engine/gauge/lpt_d1_subtracted.py",
           "gauge",
           findings=("F280", "F287", "F239", "F163", "F162", "F155"),
           exactness="bracketed", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F280_d1_subtracted.py",)),

    # F281 — completeness-2026-08-04 row A8 (measurement problem / classical
    # emergence), ABSENT with zero hits repo-wide, plus row A6 (Born rule,
    # "reproduced in tests, never derived"). Three legs, all built on structure
    # the model already owns: the pointer basis forced by the minimal-coupling
    # generator being diagonal in site occupation (F41/F42/F87); the Born rule
    # on a dynamical leg (only ell^2 survives a real BCC tick) and an envariance
    # leg with CA-native swaps (F212/F218); and classicality as the block-spin
    # attractor with the closed-form Dirichlet eigenvalue (F130/F133). Adds no
    # collapse term -- F227's "unitary, no objective collapse" is unchanged.
    Module("interactions.qi_measurement",
           "src/casim/engine/interactions/qi_measurement.py",
           "interactions",
           findings=("F281", "F227", "F226", "F212", "F218", "F130", "F133",
                     "F87", "F41"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F281_measurement.py",)),

    # F289 — completeness row A9 (spin-statistics), ABSENT: "implemented
    # (F217 Jordan-Wigner, F195 Gram-Schmidt), the connection is imported".
    # The contribution is deliberately framed as: the standard topological
    # derivation needs two inputs — the spatial dimension (pi_1 = S_n only for
    # d>=3) and the 2pi rotation phase — and in THIS model both are outputs
    # (F291/F292 derive d=3; the rotor supplies R(2pi) = -1 exactly). Also
    # derives that the paired-spinor photon of key decision 5 is a boson.
    Module("interactions.qi_spin_statistics",
           "src/casim/engine/interactions/qi_spin_statistics.py",
           "interactions",
           findings=("F289", "F291", "F292", "F217", "F195", "F68", "F26"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F289_spin_statistics.py",)),

    # F290 — completeness row A10 (cluster decomposition / no-signalling),
    # ABSENT. The CA-specific result is that the causal cone is STRICT where a
    # generic Lieb-Robinson system has only an exponential tail; the cone is
    # measured tight (1 site per brick-wall layer) rather than quoted
    # conservatively, and reconciled with F227's 4t convention numerically.
    Module("interactions.qi_cluster",
           "src/casim/engine/interactions/qi_cluster.py",
           "interactions",
           findings=("F290", "F227", "F226", "F212", "F281"),
           exactness="machine", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F290_cluster.py",)),

    # F293 — completeness row B10 ("why 3 colours", ABSENT, "a single
    # load-bearing integer"). Maps the route space: anomaly cancellation CANNOT
    # select N_c here (F279's no-go re-verified on the full six-constraint
    # system, symbolic in N_c over Q -- and the reason is model-specific, since
    # Y_Q comes out of the same nullspace proportional to N_c); colour is NOT
    # the spatial 3 (the O_h 3-cycle is an SU(3) element and fails to commute
    # with colour); the Z_3 centre route is CIRCULAR as the tree stands. What
    # works is a SELECTOR, not a derivation: the model's bare coupling
    # alpha_s(mu_0) = 1/(16 pi) carries no N_c (F110 C7's 4 is plaquette
    # geometry, no Casimir), so N_c is a 28-decade lever on the confinement
    # scale and only N_c=3 lands at the observed hadronic scale.
    # `bracketed` because the headline is a band, not a number.
    # F298 — the SU(N) Casimir ladder that F110 deferred, built for the
    # k-string (totally antisymmetric) sector, and the C7 matching re-run
    # against it. Two structural results: the C7 identity is well-defined ONLY
    # for N_c <= 3 (no measured input, independent of the F294 H1/H2 dispute),
    # and where it exists it carries 1/C_F so F294's H2 is structurally right.
    # Also withdraws F294's k-string discriminator as degenerate at N=3.
    Module("gauge.casimir_ladder",
           "src/casim/engine/gauge/casimir_ladder.py",
           "gauge",
           findings=("F298", "F294", "F293", "F110", "F144", "F86", "F97"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F298_casimir_ladder.py",)),

    # F299 — F294's physical discriminator, reinstated (F298 withdrew it as
    # "degenerate at N=3", but that degeneracy is exactly the antisymmetric-
    # tower restriction: there, at N=3, irrep and triality are in bijection).
    # The sextet shares the antitriplet's triality while carrying 5/2 its
    # Casimir, so the laws separate. Then generalises confinement.py's exactly
    # solvable 2D SU(3) Weyl-torus quadrature off the fundamental to arbitrary
    # irrep characters and runs it at the model's own beta = 2N/g_s^2 = 24:
    # sigma_6/sigma_3 = 2.4911511 vs 2.5 (Casimir) and 1 (centre), so the
    # model's own confinement sector answers H2. `quantitative` because the
    # headline number is the finite-beta lattice residual; the law it converges
    # to is exact.
    Module("gauge.casimir_scaling",
           "src/casim/engine/gauge/casimir_scaling.py",
           "gauge",
           findings=("F299", "F298", "F294", "F293", "F144", "F110", "F94",
                     "F86"),
           exactness="quantitative", reach="standalone",
           reachable_from=("gauge.confinement", "gauge.su3_ladder"),
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F299_casimir_scaling.py",),
           results=("test-results/F299_casimir_scaling.json",)),

    # F303 — is F144's bare coupling centre-normalised? No argument exists, and
    # three candidates are closed exactly: (1) not a scheme constant, the Casimir
    # shift 16 pi (C_F-1) = 16.755 is 26x F144's MEASURED A4 residual of 0.64 and
    # demands a Lambda ratio of 3.4e6 against 1.78; (2) not a three-link
    # plaquette, the only reading that would keep both g_s = 1/2 and the Casimir
    # (n C_F = 4 forces n = 3, which would even force N_c = 3 uniquely) -- the BCC
    # nearest-neighbour graph has NO closed 3-bond loop, by parity and by
    # exhaustive enumeration; (3) not the Cartan projection, |lambda|^2 = 1/3
    # gives a Landau pole above M_Z. F144 A1 steps 1-2 survive (the circularity
    # lemma's residual factorises as (r-1) x sine, so it fixes only a/b and is
    # group-blind); step 3 breaks. `exact` because N1-N3b/N5 are sympy/Q and
    # exhaustive; the quantitative rows are comparisons against F144's own
    # measured residual.
    # F325 -- X1 resolved. Branch A (Casimir) is closed two ways: structurally
    # its C_F is a mixed-operator artefact (F298 leg L6), quantitatively it sits
    # 5.63 decades outside CL252's band (F303 leg N8). This module carries the
    # third leg, the MAGNETIC side of C7, which no module held: the magnetic
    # term is a unit-entry adjacency in BOTH theories, so it adds no factor and
    # X1's named residual closes negatively. Also records two defects found on
    # the way -- F111b T7's 1-link-vs-4-link comparison, and that F144 A1 step 2
    # fixes only a RATIO so chi = 1 is a normalisation. `exact` because X4/X5
    # are exact/sympy and X2 is an extrapolated law with a measured scaling.
    Module("gauge.derive_x1_branch",
           "src/casim/engine/gauge/derive_x1_branch.py",
           "gauge",
           findings=("F325", "F324", "F303", "F299", "F298", "F294", "F144",
                     "F111b", "F110", "F101", "F280"),
           exactness="exact", reach="standalone",
           reachable_from=("gauge.su3_ladder", "gauge.casimir_ladder",
                           "gauge.derive_coupling_normalisation"),
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F325_x1_branch.py",),
           results=("test-results/F325_x1_branch.json",)),

    Module("gauge.derive_coupling_normalisation",
           "src/casim/engine/gauge/derive_coupling_normalisation.py",
           "gauge",
           findings=("F303", "F299", "F298", "F294", "F144", "F115", "F101",
                     "F110", "F91"),
           exactness="exact", reach="standalone",
           reachable_from=("gauge.casimir_scaling", "gauge.su3_ladder",
                           "gauge.derive_ncolour"),
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F303_coupling_normalisation.py",),
           results=("test-results/F303_coupling_normalisation.json",)),

    # F304 -- completeness row A6 (Born rule). F281 supplied two legs and named
    # the hypothesis under each; this module closes leg 1's by supplying
    # Gleason's two premises FROM THE RULE: dim >= 3 (a measurement needs a
    # record, so the smallest measurement Hilbert space is 4; the free step's
    # 2-dim momentum blocks are invariant but are NOT pointer contexts) and
    # non-contextuality (the record channel is H_int, a fixed operator of the
    # rule that carries no reference to the measured basis; remote contexts are
    # blocked by exact no-signalling). Gleason's theorem itself stays external,
    # the F289 posture. Also computes the dichotomy that makes the dimension
    # premise load-bearing: frame-function space dimension d^2 at d>=3, but
    # 1+sum_{odd l<=deg}(2l+1) at d=2, unbounded.
    Module("interactions.qi_born_gleason",
           "src/casim/engine/interactions/qi_born_gleason.py",
           "interactions",
           findings=("F304", "F281", "F290", "F227", "F87", "F41"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F304_born_gleason.py",),
           results=("test-results/F304_born_rule_gleason.json",)),

    # F317 -- completeness row B1's colour leg ("colour is still put in").
    # "Put in" bundles SIX impositions; this module attacks four and pins a
    # fifth.  DERIVED: the invariance group is U(N) -- the commutant of the
    # rule on the internal factor is COMPUTED to be M_N (dim 9), not assumed,
    # and the guard that makes the count mean anything is that the model's own
    # mass step + BCC walk generate the FULL M_4 on the Dirac factor (16).
    # It is the TRACELESS SU(N) because [SU(2)_L]^2 U(1)_trace = N_c b / 2 != 0
    # on the model's own F279/F293 nullspace while the same row makes it
    # identically zero for Y -- i.e. F27's chirality is what removes the U(1).
    # The symmetry is LOCAL because a CA rule has no global operations: the
    # on-site step commutes with a site-dependent V(x) (7e-16) and the HOP does
    # not (1.343), which forces the connection -- and explains why F27's U(x)
    # is pure gauge.  The coupling is VECTOR-LIKE because a chiral triplet
    # carries A^{888} = -1/sqrt(3) while a chiral doublet is anomaly-free,
    # which CLOSES F91's one unforced assignment (the BCC gluon's even law,
    # previously selected on elegance).  PINNED GIVEN ONE EMPIRICAL INPUT:
    # Lambda^3(C^N) carries a singlet at exactly N = 3, so three-constituent
    # baryons + DERIVED Fermi statistics (F289) give N_c = 3, agreeing with and
    # independent of F298's structural N_c <= 3.  STILL AN INPUT, and the
    # finding leads with it: THAT the quark carries an internal index at all.
    # F318 -- F317's residual, and the attack F317 itself named: can the CELL
    # carry the internal index?  Three questions were tangled in that residual
    # and they have three answers.  PERMIT: free.  The bound F291 flags as
    # "conditional on s = 2" is measured NOT to be -- what S1 needs is the
    # maximal ANTICOMMUTING subset of the HOP's traceless span, and the model's
    # branch-doubled cell widens that span 3 -> 6 while leaving the rank at 3
    # (tau_3 x sigma_i COMMUTES with 1 x sigma_i); an internal factor changes
    # neither.  On the time side the commutant grows by exactly N^2 -- 2 -> 18
    # at N = 3 -- but every added element is NON-DISPERSIVE (literal 0.0 vs the
    # update's 0.2846), and a commuting unitary is a clock only if it disperses.
    # That criterion is one F313 never had to state, and it is what stands
    # between d_time = 1 and d_time = 5 on a coloured cell.  SHAPE: forced -- a
    # walk that genuinely uses 5 anticommuting generators on C^4 has
    # ker J = coker J = 0 at d = 5, so the selector returns 5 rather than 3.
    # FORCE: NOT by the cell, which is measurably indifferent (identical
    # verdicts at N = 1 and N = 3 while the commutant differs 2 vs 18).  The
    # forcing is derived Fermi statistics (F289): spin alone caps a nodeless
    # level at TWO identical constituents, so the tree's three-constituent
    # bound state is impossible at N = 1.  RESIDUAL INPUT MOVED, NOT CLOSED:
    # from "an internal index exists" to "the matter sector contains a
    # three-constituent bound state" -- and F317 sec.6 consumes the SAME fact,
    # so the two findings do not independently confirm each other.
    Module("lattice.cell_internal_index",
           "src/casim/engine/lattice/cell_internal_index.py",
           "lattice",
           findings=("F318", "F317", "F291", "F313", "F315", "F289", "F122"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F318_cell_internal_index.py",),
           results=("test-results/F318_cell_internal_index.json",)),

    Module("gauge.derive_su3_structure",
           "src/casim/engine/gauge/derive_su3_structure.py",
           "gauge",
           findings=("F317", "F91", "F27", "F68", "F279", "F293", "F298",
                     "F289", "F43"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F317_su3_structure.py",),
           results=("test-results/F317_su3_structure.json",)),

    Module("gauge.derive_gauge_boson_masses",
           "src/casim/engine/gauge/derive_gauge_boson_masses.py",
           "gauge",
           findings=("F320", "F141", "F138", "F231", "F49", "F51", "F41",
                     "F27", "F119", "F127"),
           exactness="bracketed", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F320_gauge_boson_masses.py",),
           results=("test-results/F320_gauge_boson_masses.json",)),

    Module("gauge.colour_theta",
           "src/casim/engine/gauge/colour_theta.py",
           "gauge",
           findings=("F321", "F53", "F43", "F305", "F307", "F265", "F91",
                     "F27", "F162"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F321_strong_cp.py",),
           results=("test-results/F321_strong_cp.json",)),

    Module("gauge.derive_ncolour",
           "src/casim/engine/gauge/derive_ncolour.py",
           "gauge",
           findings=("F293", "F294", "F279", "F144", "F110", "F107", "F280",
                     "F291"),
           exactness="bracketed", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/findings/test_F293_why_three_colours.py",)),

    Module("interactions.qed_uv_completion",
           "src/casim/engine/interactions/qed_uv_completion.py",
           "interactions",
           findings=("F319", "F264", "F164", "F116", "F284", "F59", "F79",
                     "F107", "F251", "F301", "F69", "F26"),
           exactness="exact", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml",),
           results=("test-results/F319_uv_completion.json",)),

    Module("interactions.running_alpha_lattice_bound",
           "src/casim/engine/interactions/running_alpha_lattice_bound.py",
           "interactions",
           findings=("F322", "F251", "F277", "F261", "F115", "F138", "F231"),
           exactness="quantitative", reach="standalone",
           role="derivation", origin="spine", status="live",
           tests=("tests/registry/interactions.yaml",),
           results=("test-results/F322_b9_running_rederivation.json",)),
)


def _register_spine() -> None:
    for m in _SPINE:
        register(m)


_register_spine()
_register_from_manifest()
