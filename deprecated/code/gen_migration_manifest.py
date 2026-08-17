#!/usr/bin/env python3
"""Build `docs/design/module-migration-manifest.yaml` — roadmap C0.3.

**The manifest is this roadmap's real product.** Phases C1-C9 execute it; a file
with no record does not move. Everything else in C0 exists to fill in its
fields honestly.

Two halves, and the split is deliberate:

  * **CLASSIFICATION is hand-authored**, in the `SECTOR` table below. Which
    subpackage a module belongs to is a judgement about the physics, not
    something a script can infer from an import graph, and the roadmap requires
    it be "resolved once, on paper, not 40 files into a migration". Editing
    that table is how you change a target path.

  * **EVIDENCE is generated** — reachability, tests, baselines, np/scipy call
    sites, constants, dead-code proposals, ledger records. All of it comes from
    `module-graph.json`, `dead-code-proposal.json`, `manifest.json`,
    `supersessions.yaml` and `casim.constants`, so it cannot drift from the
    tree without `--check` noticing.

The one field that is neither: `dead_symbols`. It starts **empty** and stays
empty until a human accepts a line out of `dead_symbols_proposed`.
`migrate_module.py` strips `dead_symbols` and ignores the proposals entirely.
That is the P0.4 lesson wired into the data model rather than written in a
comment.

Usage:
    python3 tools/gen_migration_manifest.py           # write it
    python3 tools/gen_migration_manifest.py --check   # exit 1 if stale/incomplete
    python3 tools/gen_migration_manifest.py --report  # summary, no write
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import yaml

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO, "src"))

GRAPH = os.path.join(_REPO, "docs", "design", "module-graph.json")
DEAD = os.path.join(_REPO, "docs", "design", "dead-code-proposal.json")
RESULTS_MANIFEST = os.path.join(_REPO, "test-results", "manifest.json")
LEDGER = os.path.join(_REPO, "docs", "theory", "supersessions.yaml")
OUT = os.path.join(_REPO, "docs", "design", "module-migration-manifest.yaml")

# The seven engine sectors of roadmap §4, plus `numerics` and `constants` for
# the two modules that are absorbed rather than moved.
SECTORS = ("numerics", "constants", "core", "lattice", "gauge", "particles",
           "interactions", "forks")

# Which phase migrates which sector.
PHASE_OF_SECTOR = {
    "numerics": "C1", "constants": "C2", "core": "C3", "lattice": "C3",
    "gauge": "C4", "particles": "C5", "interactions": "C6", "forks": "C6",
}

# ---------------------------------------------------------------------------
# HAND-AUTHORED CLASSIFICATION.
#
# module stem -> (sector, subpath)  where the target is
#     src/casim/engine/<sector>/<subpath>.py
# except sector `numerics` / `constants`, which land outside engine/.
#
# Sourced from the roadmap's C4/C5/C6 scope lists, `code-index.md`, and the
# 2026-07-29 kernel-coverage addendum. Disagreements about placement are
# settled HERE, before any file moves.
# ---------------------------------------------------------------------------
SECTOR: dict[str, tuple[str, str]] = {
    # -- absorbed, not moved (C1/C2) -------------------------------------
    "ca_fft":                       ("numerics", "fft"),
    "ca_lazy":                      ("numerics", "lazy"),

    # -- lattice: the BCC base layer (C3) ---------------------------------
    "ca_lattice":                   ("lattice", "geometry"),
    "ca_bcc":                       ("lattice", "bcc"),
    "ca_core":                      ("lattice", "core"),
    "ca_core_exact":                ("lattice", "core_exact"),
    "ca_blockspin":                 ("lattice", "blockspin"),
    "ca_blockspin_dynamical":       ("lattice", "blockspin_dynamical"),
    "ca_blockspin_binding":         ("lattice", "blockspin_binding"),
    "ca_baryon_blockspin":          ("lattice", "blockspin_baryon"),
    "ca_multigrid":                 ("lattice", "multigrid"),
    "poisson_open":                 ("lattice", "poisson_open"),
    "ca_si_scale":                  ("lattice", "si_scale"),
    "ca_curved":                    ("lattice", "curved"),

    # -- core: engine services (C3) ---------------------------------------
    "ca_manybody":                  ("core", "manybody"),
    "ca_lpt_generator":             ("core", "lpt_generator"),

    # -- gauge (C4) --------------------------------------------------------
    "ca_maxwell":                   ("gauge", "bilinear"),
    "ca_maxwell_2d":                ("gauge", "bilinear_2d"),
    "ca_photon_pair":               ("gauge", "photon"),
    "ca_photon_bs":                 ("gauge", "photon_bound_state"),
    "ca_charge_coupling":           ("gauge", "charge_coupling"),
    "ca_minimal_coupling":          ("gauge", "minimal_coupling"),
    "ca_emission":                  ("gauge", "emission"),
    "ca_propagator":                ("gauge", "propagator"),
    "ca_rotation":                  ("gauge", "rotation"),
    "ca_wmu":                       ("gauge", "weak_wmu"),
    "ca_z_field":                   ("gauge", "weak_z"),
    "ca_weak":                      ("gauge", "weak"),
    "ca_charged_current":           ("gauge", "charged_current"),
    "ca_hypercharge":               ("gauge", "hypercharge"),
    "ca_chiral_anomaly":            ("gauge", "chiral_anomaly"),
    "ca_bcc_gauge":                 ("gauge", "bcc_action"),
    "ca_gluon":                     ("gauge", "gluon"),
    "ca_gluon_self_energy":         ("gauge", "gluon_self_energy"),
    "ca_bgfield_loop":              ("gauge", "bgfield_loop"),
    "ca_strong":                    ("gauge", "strong"),
    "ca_su3_ladder":                ("gauge", "su3_ladder"),
    "ca_cooling":                   ("gauge", "cooling"),
    "ca_link_hamiltonian":          ("gauge", "link_hamiltonian"),
    "ca_confinement":               ("gauge", "confinement"),
    "ca_colour_dielectric":         ("gauge", "colour_dielectric"),
    "ca_colour_condensate":         ("gauge", "colour_condensate"),
    "ca_lpt_selfenergy":            ("gauge", "lpt_selfenergy"),
    "ca_lpt_vertex":                ("gauge", "lpt_vertex"),
    "ca_lpt_ward":                  ("gauge", "lpt_ward"),
    "ca_lpt_wilson":                ("gauge", "lpt_wilson"),
    "ca_lpt_wilson_selfenergy":     ("gauge", "lpt_wilson_selfenergy"),

    # -- particles (C5) ----------------------------------------------------
    "ca_dirac":                     ("particles", "dirac"),
    "ca_dirac_bcc":                 ("particles", "dirac_bcc"),
    "ca_second_quant":              ("particles", "second_quant"),
    "ca_baryon":                    ("particles", "baryon"),
    "ca_baryon_dynamics":           ("particles", "baryon_dynamics"),
    "ca_meson":                     ("particles", "meson"),
    "ca_nuclear":                   ("particles", "nuclear"),
    "ca_nuclear_core":              ("particles", "nuclear_core"),
    "ca_atom":                      ("particles", "atom"),
    "ca_element":                   ("particles", "element"),
    "ca_positronium":               ("particles", "positronium"),
    "ca_hyperfine":                 ("particles", "hyperfine"),
    "ca_majorana":                  ("particles", "majorana"),
    "ca_higgs":                     ("particles", "higgs"),
    "ca_eg_sextic_coupling":        ("particles", "eg_sextic"),
    "ca_induced_stiffness":         ("particles", "induced_stiffness"),
    "derive_generator_norm_from_F118": ("particles", "derive_generator_norm"),
    "derive_lambda6_sextic":        ("particles", "derive_lambda6_sextic"),
    "derive_weight_as_phase":       ("particles", "derive_weight_as_phase"),
    "derive_t2g_pmns_selector":     ("particles", "derive_t2g_pmns"),
    "derive_colour_condensate":     ("particles", "derive_colour_condensate"),

    # -- interactions: gravity + astrophysics (C6) -------------------------
    "ca_gravity":                   ("interactions", "gravity"),
    "ca_emqg":                      ("interactions", "gravity_emqg"),
    "ca_emergent_gravity":          ("interactions", "gravity_emergent"),
    "ca_dual_gl_backreaction":      ("interactions", "gravity_backreaction"),
    "ca_blackhole":                 ("interactions", "blackhole"),
    "ca_qnm":                       ("interactions", "qnm"),
    "ca_inspiral":                  ("interactions", "inspiral"),
    "ca_horizon_entropy":           ("interactions", "horizon_entropy"),
    "ca_interior_metric":           ("interactions", "interior_metric"),
    "ca_tolman":                    ("interactions", "tolman"),
    "ca_ns_eos":                    ("interactions", "ns_eos"),
    "ca_stellar":                   ("interactions", "stellar"),
    "ca_cosmology":                 ("interactions", "cosmology"),
    "ca_darkmatter":                ("interactions", "darkmatter"),
    "ca_raytrace":                  ("interactions", "raytrace"),
    "ca_vacuum_energy":             ("interactions", "vacuum_energy"),
    # QED precision
    "ca_amu":                       ("interactions", "qed_amu"),
    "ca_twoloop_ae":                ("interactions", "qed_twoloop_ae"),
    "ca_bethe_log":                 ("interactions", "qed_bethe_log"),
    "ca_electron_self_energy":      ("interactions", "qed_electron_self_energy"),
    "ca_vacuum_polarization":       ("interactions", "qed_vacuum_polarization"),
    "ca_qed_renormalization":       ("interactions", "qed_renormalization"),
    "ca_qed_scattering":            ("interactions", "qed_scattering"),
    "ca_vertex_loop":               ("interactions", "qed_vertex_loop"),
    "ca_euler_heisenberg":          ("interactions", "qed_euler_heisenberg"),
    "ca_schwinger_pair":            ("interactions", "qed_schwinger_pair"),
    "ca_casimir":                   ("interactions", "qed_casimir"),
    "ca_casimir_materials":         ("interactions", "qed_casimir_materials"),
    "ca_ir_bremsstrahlung":         ("interactions", "qed_ir_bremsstrahlung"),
    # running / scale setting
    "ca_alpha_s_running":           ("interactions", "running_alpha_s"),
    "ca_gap_solve":                 ("interactions", "running_gap_solve"),
    "ca_njl_induced_coupling":      ("interactions", "running_njl"),
    "ca_scheme_constant":           ("interactions", "running_scheme_constant"),
    "ca_qcd_scale_ratio":           ("interactions", "running_scale_ratio"),
    "ca_qstar_logmoment":           ("interactions", "running_qstar_logmoment"),
    "ca_ir_coupling":               ("interactions", "running_ir_coupling"),
    # quantum info / condensed / applied
    "ca_quantum_algorithms":        ("interactions", "qi_algorithms"),
    "ca_bell_tsirelson":            ("interactions", "qi_bell_tsirelson"),
    "ca_decoherence_floor":         ("interactions", "qi_decoherence_floor"),
    "ca_qc_si":                     ("interactions", "qi_qc_si"),
    "ca_quantum_noise":             ("interactions", "qi_noise"),
    "ca_entanglement":              ("interactions", "qi_entanglement"),
    "ca_superconductivity":         ("interactions", "superconductivity"),
    "ca_slowlight":                 ("interactions", "slowlight"),
    "ca_unified":                   ("interactions", "unified"),
    # derivations that belong to the interaction sectors
    "derive_beta_LV":               ("interactions", "derive_beta_LV"),
    "derive_curl_subleading":       ("interactions", "derive_curl_subleading"),
    "derive_dielectric_noconfine":  ("interactions", "derive_dielectric_noconfine"),
    "derive_f26_dispersion":        ("interactions", "derive_f26_dispersion"),
    "derive_velocity_addition":     ("interactions", "derive_velocity_addition"),
    "run_Q3_omega_degeneracy":      ("interactions", "run_q3_omega_degeneracy"),
    "benchmark_jax":                ("numerics", "benchmark"),

    # -- viz / support: NOT engine physics --------------------------------
    # These land under casim.viz, not casim.engine. P5.1 already rules that
    # live_display.py and spinor_color.py are retired outright (no importers;
    # live_display pip-installs at import time), so they are the roadmap's
    # only pre-approved delete-on-migrate entries — and even they get a
    # deprecated/code/ backup first.
    "viz":                          ("core", "_viz_legacy"),
    "tick_heatmap":                 ("core", "_viz_tick_heatmap"),
    "live_display":                 ("core", "_viz_live_display"),
    "spinor_color":                 ("core", "_viz_spinor_color"),
}

# Forks keep their own tree, one subdirectory per sector, so the fork/mainline
# distinction survives the move (roadmap C6: "a rejected fork is a recorded
# negative result, not dead code").
FORK_SECTOR = [
    (re.compile(r"^gr3?_fork|^gr_tensor|^dirac_gravity_fork"), "gravity"),
    (re.compile(r"^dm_fork"), "darkmatter"),
    (re.compile(r"^lgt_fork|^curl_fork"), "gauge"),
    (re.compile(r"^hypercharge_fork"), "electroweak"),
    (re.compile(r"^complex_mass_fork"), "particles"),
    (re.compile(r"^smearing_fork"), "lattice"),
]

# Roadmap C3.3 records these as absorbed into casim.numerics at C1 rather than
# moved to an engine sector.
ABSORBED = {"ca_fft": "casim.numerics.fft", "ca_lazy": "casim.numerics.lazy"}

FINDING_RE = re.compile(r"(?<![A-Za-z0-9])(F[A-Z]{0,2}\d{1,3})(?![0-9])")


# ---------------------------------------------------------------------------
def _load(path: str, what: str) -> dict:
    if not os.path.exists(path):
        sys.exit(f"{what} is missing ({os.path.relpath(path, _REPO)}) — "
                 f"run the earlier C0 step first")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh) if path.endswith(".json") else yaml.safe_load(fh)


def _target_for(rel: str, role: str) -> tuple[str, str, str]:
    """(sector, target path, phase) for one migratable file."""
    stem = os.path.basename(rel)[:-3]
    if role == "fork":
        if stem == "__init__":
            return "forks", "src/casim/engine/forks/__init__.py", "C6"
        sub = next((s for pat, s in FORK_SECTOR if pat.match(stem)), "misc")
        return "forks", f"src/casim/engine/forks/{sub}/{stem}.py", "C6"
    if stem not in SECTOR:
        return "", "", ""
    sector, sub = SECTOR[stem]
    if sector == "numerics":
        return sector, f"src/casim/numerics/{sub}.py", PHASE_OF_SECTOR[sector]
    if sector == "constants":
        return sector, f"src/casim/constants/{sub}.py", PHASE_OF_SECTOR[sector]
    return sector, f"src/casim/engine/{sector}/{sub}.py", PHASE_OF_SECTOR[sector]


def _constants_for(rel: str) -> list[str]:
    try:
        import casim.constants as C
    except Exception:
        return []
    out = {c.symbol for c in C.all_constants()
           for s in c.sites if s.path == rel}
    return sorted(out)


def _reach_union(src_node: dict, tgt_node: dict | None, role: str) -> str:
    """`reach` for a module that may exist under two names (shim + engine target).

    Same precedence as `gen_module_graph.py` — driven > package-only > test-only >
    entry-script > unreferenced — applied to the OR of the two nodes' three
    reachability booleans. Added at C6: without it, migrating a module makes it
    look less reachable than it was, which is precisely backwards.
    """
    def _or(key: str) -> bool:
        return bool(src_node.get(key) or (tgt_node or {}).get(key))
    if _or("driven"):
        return "driven"
    if _or("package_reachable"):
        return "package-only"
    if _or("test_referenced"):
        return "test-only"
    if role == "derivation" and src_node.get("has_main"):
        return "entry-script"
    return "unreferenced"


def build() -> dict:
    graph = _load(GRAPH, "module-graph.json")
    dead = _load(DEAD, "dead-code-proposal.json")
    ledger = _load(LEDGER, "supersessions.yaml")
    results = (_load(RESULTS_MANIFEST, "test-results/manifest.json")
               if os.path.exists(RESULTS_MANIFEST) else {"tests": {}})

    nodes = graph["nodes"]
    migratable = {r: n for r, n in nodes.items()
                  if n["role"] in ("kernel", "fork", "derivation", "support")}

    # proposals, indexed by path
    prop_files = {f["path"] for f in dead["signal_1_structural"]["files"]}
    prop_syms: dict[str, list[str]] = {}
    for s in dead["signal_1_structural"]["symbols"]:
        prop_syms.setdefault(s["path"], []).append(s["symbol"])
    ledger_syms: dict[str, list[dict]] = {}
    for c in dead["signal_2_ledger"]["candidates"]:
        for w in c["defined_in"]:
            ledger_syms.setdefault(w, []).append(c)
    protected: dict[str, list[str]] = {}
    for c in dead["signal_2_ledger"]["protected"]:
        for w in c["defined_in"]:
            protected.setdefault(w, []).append(c["symbol"])

    # Ledger `code:` paths, indexed so a record survives migration. Once a module
    # moves, the honest ledger cites its NEW path (the ledger's own test says "a
    # ledger that cites a moved file is a ledger nobody can trust"), but every
    # manifest record is keyed by its ca-simulation SOURCE. Indexing the target
    # under the source as well is what stops a repointed ledger entry from
    # silently downgrading a `partial` record to `live` and dropping its
    # protected symbols. Added at C6, when the first `code:` paths were repointed.
    target_to_source: dict[str, str] = {}
    for rel in migratable:
        _s, _t, _p = _target_for(rel, migratable[rel]["role"])
        if _t:
            target_to_source.setdefault(_t, rel)

    # Same aliasing for the dead-code signals: after a migration the symbols are
    # DEFINED at the target path, so a proposal or a ledger-protected symbol would
    # otherwise stop being attached to the record that owns it.
    for _d in (prop_syms, protected):
        for _t, _s in target_to_source.items():
            if _t in _d:
                _d.setdefault(_s, [])
                for _v in _d[_t]:
                    if _v not in _d[_s]:
                        _d[_s].append(_v)

    ledger_by_path: dict[str, list[dict]] = {}
    for rec in ledger.get("supersessions", []):
        for c in rec.get("code", []) or []:
            p = c.get("path")
            if not p:
                continue
            entry = {"record": rec["id"], "kind": rec.get("kind"),
                     "note": (c.get("note") or "").strip()}
            for key in {p, target_to_source.get(p, p)}:
                ledger_by_path.setdefault(key, []).append(dict(entry))

    records = []
    collisions: dict[str, list[str]] = {}
    unclassified: list[str] = []

    for rel in sorted(migratable):
        n = migratable[rel]
        sector, target, phase = _target_for(rel, n["role"])
        if not sector:
            unclassified.append(rel)
            continue
        collisions.setdefault(target, []).append(rel)

        tests = n.get("tests", [])
        baselines = n.get("results", [])
        led = ledger_by_path.get(rel, [])

        # status. `partial` means the ledger touches it but did not kill it —
        # which in this project is the usual case and the one that needs a
        # human, so it is never inferred as `superseded`.
        #
        # Forks are classified FIRST and can never be `dead_candidate`. A fork
        # that nothing imports is the normal end state of a fork: it was an
        # alternative that got tested and rejected, and that rejection is the
        # falsification record. Letting the structural signal label it dead
        # would propose deleting the project's own negative results.
        if n["role"] == "fork":
            status = ("fork_live" if n["reach"] != "unreferenced"
                      else "fork_unclaimed")
        elif rel in prop_files and not led:
            status = "dead_candidate"
        elif led:
            status = "partial"
        else:
            status = "live"

        rec = {
            "id": os.path.basename(rel),
            "source": rel,
            "target": target,
            "sector": sector,
            "phase": phase,
            "role": n["role"],
            "status": status,
            # Union of the module's TWO graph nodes, for the same reason as
            # `reachable_from` below: the shim keeps the ca-simulation name and
            # the old test references, the target carries every rewired import,
            # and the graph gives `reach` only to ca-simulation roles — so a
            # migrated module read from its source node alone looks LESS
            # connected after migration than before. `lgt_fork_A_mc` is the clean
            # example: shim says `test-only`, target is `driven` from
            # engine/core/tier3.py, and `driven` is the true answer.
            "reach": _reach_union(n, graph["nodes"].get(target), n["role"]),
            # C6/D11: WHICH channels reach it, not just whether any does. This
            # is the field casim.engine.registry exposes as `reachable_from`, and
            # the one that gives P6's kernel-coverage question a queryable value.
            #
            # Union of the SOURCE node and the TARGET node, because after a
            # migration the module has two names in the graph: the shim at the
            # ca-simulation path (reached by unmigrated tests using the old name)
            # and the real module at the engine path (reached by everything
            # rewired). Reading either alone understates reach for the same
            # physics; the union answers "which channels drive this code".
            "reachable_from": sorted(
                set(n.get("reachable_from", []))
                | set((graph["nodes"].get(target) or {}).get(
                    "reachable_from", []))),
            "lines": n["lines"],
            # From the graph, which reads the WHOLE module docstring. Deriving
            # them here from `doc` (the first line only) recorded ca_gluon.py
            # and ca_gravity.py as citing no findings at all.
            "findings": n.get("findings", []),
            "summary": (n["doc"] or "")[:150],
            # ACCEPTED dead symbols. Empty by construction — a human moves a
            # line here out of dead_symbols_proposed. migrate_module.py strips
            # THIS list and never reads the proposals.
            "dead_symbols": [],
            "dead_symbols_proposed": sorted(prop_syms.get(rel, [])),
            "protected_symbols": sorted(protected.get(rel, [])),
            "ledger": led,
            "tests": tests,
            "baselines": baselines,
            "numerics_sites": {"np": n["np_sites"], "scipy": n["scipy_sites"],
                               "fft": n["fft_sites"]},
            "constants_sites": _constants_for(rel),
            "migrated": None,
        }
        if rel in ABSORBED:
            rec["absorbed_into"] = ABSORBED[rel]
            rec["note"] = ("absorbed into the numerics facade at C1 rather "
                           "than moved as a module")
        if ledger_syms.get(rel):
            rec["ledger_symbol_candidates"] = [
                {"symbol": c["symbol"], "record": c["record"],
                 "from": c["source_field"],
                 "sibling_of_protected": c["sibling_of_protected"]}
                for c in ledger_syms[rel]]
        records.append(rec)

    dupes = {t: v for t, v in collisions.items() if len(v) > 1}

    by_phase: dict[str, int] = {}
    by_sector: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for r in records:
        by_phase[r["phase"]] = by_phase.get(r["phase"], 0) + 1
        by_sector[r["sector"]] = by_sector.get(r["sector"], 0) + 1
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    return {
        "version": 1,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d - %H:%M UTC"),
        "about": (
            "Roadmap C0.3. One record per file under ca-simulation/. Phases "
            "C1-C9 execute this file; a file with no record does not move. "
            "CLASSIFICATION (sector/target) is hand-authored in "
            "tools/gen_migration_manifest.py; EVIDENCE is generated from the "
            "module graph, dead-code proposal, results manifest and "
            "supersession ledger. `dead_symbols` is ACCEPTED-ONLY and starts "
            "empty: migrate_module.py strips it and never reads "
            "`dead_symbols_proposed`."),
        "field_notes": {
            "status": {
                "live": "no ledger record, referenced — migrate as-is",
                "partial": "the ledger names it but did not kill it. THE "
                           "COMMON CASE. Needs a human to decide what, if "
                           "anything, is dead inside it.",
                "dead_candidate": "nothing imports it and it has no __main__",
                "fork_live": "a fork something still references",
                "fork_unclaimed": "a fork nothing references — a RECORDED "
                                  "NEGATIVE RESULT, not dead code. Migrates.",
            },
            "reach": graph["criterion"],
            "dead_symbols": "accepted; stripped by migrate_module.py",
            "dead_symbols_proposed": "advisory; never acted on",
        },
        "summary": {
            "records": len(records),
            "migratable_in_graph": len(migratable),
            "unclassified": unclassified,
            "target_collisions": dupes,
            "by_phase": by_phase,
            "by_sector": by_sector,
            "by_status": by_status,
            "accepted_dead_symbols": sum(len(r["dead_symbols"]) for r in records),
            "proposed_dead_symbols": sum(
                len(r["dead_symbols_proposed"]) for r in records),
        },
        # Sector claims (roadmap concurrency rule: C4/C5/C6 may run in parallel
        # sessions, so a session records its sector here BEFORE moving a file).
        # Preserved across regeneration by `_preserve_accepted`.
        "claims": {},
        "modules": records,
    }


# ---------------------------------------------------------------------------
def validate(m: dict) -> list[str]:
    """The C0 acceptance gate, as assertions."""
    s = m["summary"]
    errs = []
    if s["unclassified"]:
        errs.append(
            f"{len(s['unclassified'])} file(s) have no SECTOR entry — add them "
            f"to tools/gen_migration_manifest.py: "
            + ", ".join(s["unclassified"][:8]))
    if s["records"] != s["migratable_in_graph"]:
        errs.append(f"coverage {s['records']}/{s['migratable_in_graph']} — "
                    f"every migratable file needs a record")
    if s["target_collisions"]:
        for t, v in s["target_collisions"].items():
            errs.append(f"two sources target {t}: {', '.join(v)}")
    for r in m["modules"]:
        if r["sector"] not in SECTORS:
            errs.append(f"{r['id']}: unknown sector {r['sector']!r}")
        if r["phase"] not in ("C1", "C2", "C3", "C4", "C5", "C6"):
            errs.append(f"{r['id']}: unknown phase {r['phase']!r}")
        for sym in r["dead_symbols"]:
            if sym in r["protected_symbols"]:
                errs.append(f"{r['id']}: {sym} is ACCEPTED dead but is named "
                            f"in a ledger `retained:` field")
    return errs


def report(m: dict) -> None:
    s = m["summary"]
    print(f"\nmigration manifest")
    print(f"  records              {s['records']} / {s['migratable_in_graph']} "
          f"migratable files")
    print(f"  accepted dead syms   {s['accepted_dead_symbols']}  "
          f"({s['proposed_dead_symbols']} proposed, awaiting a human)")
    print("\n  by phase")
    for k in sorted(s["by_phase"]):
        print(f"    {k}  {s['by_phase'][k]:>4d}")
    print("\n  by sector")
    for k in sorted(s["by_sector"], key=lambda x: -s["by_sector"][x]):
        print(f"    {k:<14s} {s['by_sector'][k]:>4d}")
    print("\n  by status")
    for k in sorted(s["by_status"], key=lambda x: -s["by_status"][x]):
        print(f"    {k:<16s} {s['by_status'][k]:>4d}")
    errs = validate(m)
    if errs:
        print(f"\n  INVALID ({len(errs)}):")
        for e in errs[:20]:
            print(f"    - {e}")
    else:
        print("\n  valid: full coverage, unique targets, known sectors/phases")


def _dump(m: dict) -> str:
    head = (
        "# ---------------------------------------------------------------------------\n"
        "# Module migration manifest — roadmap C0.3.\n"
        "#\n"
        "# AUTO-GENERATED by tools/gen_migration_manifest.py. To change where a\n"
        "# module lands, edit the SECTOR table in that script, not this file.\n"
        "#\n"
        "# EXCEPTION: `dead_symbols` is the one human-owned field. Move a line\n"
        "# into it from `dead_symbols_proposed` only after reading the module.\n"
        "# tools/migrate_module.py strips `dead_symbols` and NEVER reads the\n"
        "# proposals. Accepted entries are preserved across regeneration.\n"
        "# ---------------------------------------------------------------------------\n")
    return head + yaml.safe_dump(m, sort_keys=False, width=100,
                                 default_flow_style=False, allow_unicode=True)


# Fields that are STATE, not evidence: a regeneration must never reset them.
#
# `dead_symbols` is human-accepted. `migrated` and `drift` are written by
# tools/migrate_module.py and record that a migration actually happened.
#
# `migrated` was added to this list on 2026-07-30 after a concurrent session
# regenerated the manifest and silently reset ca_fft.py's stamp to null while
# the migration itself was complete (shim in place, target present, backup in
# deprecated/code/). `tools/check_deprecated.py` then reported the tree as
# INVALID — "a backup exists but the manifest record has migrated: null" —
# which is exactly the false alarm a lost stamp produces. C4/C5/C6 explicitly
# invite parallel sessions, so a regenerator that clobbers migration state is
# a collision waiting to happen on a much larger scale.
_STATE_FIELDS = ("dead_symbols", "migrated", "drift")


def _preserve_accepted(m: dict) -> None:
    """Carry human-accepted and migration-state fields across a regeneration."""
    if not os.path.exists(OUT):
        return
    with open(OUT, encoding="utf-8") as fh:
        old = yaml.safe_load(fh) or {}
    keep = {r["source"]: r for r in old.get("modules", [])}
    for r in m["modules"]:
        prev = keep.get(r["source"])
        if not prev:
            continue
        for field in _STATE_FIELDS:
            if prev.get(field):
                r[field] = prev[field]
    # Sector claims are session state, not derivable from the tree — carry them.
    if old.get("claims"):
        m["claims"] = old["claims"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    m = build()
    _preserve_accepted(m)

    if args.report:
        report(m)
        return 1 if validate(m) else 0

    if args.check:
        errs = validate(m)
        if errs:
            print("migration manifest INVALID:")
            for e in errs:
                print(f"  - {e}")
            return 1
        if not os.path.exists(OUT):
            print("module-migration-manifest.yaml is missing — run "
                  "`python3 tools/gen_migration_manifest.py`")
            return 1
        with open(OUT, encoding="utf-8") as fh:
            old = yaml.safe_load(fh)
        a = {k: v for k, v in (old or {}).items() if k != "updated"}
        b = {k: v for k, v in m.items() if k != "updated"}
        if a != b:
            print("module-migration-manifest.yaml is stale — run "
                  "`python3 tools/gen_migration_manifest.py`")
            return 1
        print(f"migration manifest is current — {m['summary']['records']} "
              f"records, full coverage")
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(_dump(m))
    report(m)
    print(f"\nwrote {os.path.relpath(OUT, _REPO)}")
    return 1 if validate(m) else 0


if __name__ == "__main__":
    sys.exit(main())
