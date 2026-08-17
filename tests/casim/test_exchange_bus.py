"""Typed exchange bus — roadmap P3.3, blocker B3, finding F269.

*Created 2026-07-31 - 23:50.*

The two failures B3 named were both silent: a misspelled coupling target read
nothing and the run reported success, and reordering the YAML changed the
physics with no error and no record.  Both are asserted here as errors.
"""
from __future__ import annotations

import pytest
import yaml
from pathlib import Path

from casim.engine.core.channel import (
    Channel, build_channel, register, registered_channels)
from casim.engine.core.graph import BusError, build_graph
from casim.engine.core.simulation import LatticeSpec, Simulation


def _repo_root() -> Path:
    """Repo root, resolved on call rather than at import.

    A module-scope ``Path(__file__).resolve()`` is a call at top level, which is
    what P1.3's ``import_time_work`` ratchet counts — and the ratchet's own
    docstring notes that its blunt edge has already been paid for once. There is
    no reason to pay it again for a path lookup that only one test needs.
    """
    return Path(__file__).resolve().parents[2]


class _Node(Channel):
    """A channel that records the order it saw its partners' states in."""
    type_name = "_bus_node"
    topologies = ("cubic", "bcc")

    def init_state(self, lattice, rng):
        return {"v": 0, "seen": ()}

    def step(self, state, lattice, context=None, rng=None):
        seen = tuple(sorted(
            (n, context[n]["v"]) for n in self.consumes() if n in (context or {})))
        return {"v": state["v"] + 1, "seen": seen}

    def energy(self, state) -> float:
        return 1.0


@pytest.fixture(autouse=True, scope="module")
def _register_probe_channel():
    """Register ``_Node`` for this module only — see the note in
    ``test_engine_clock.py``: mutating a global registry at import is precisely
    what P1.3's ``import_time_work`` ratchet counts, and it fires on collection
    rather than on a run."""
    if "_bus_node" not in registered_channels():
        register(_Node)
    yield


def _sim(channels, bus=None):
    return Simulation(LatticeSpec(L=4, dims=3, topology="cubic"),
                      channels, bus=bus, seed=0)


# ----------------------------------------------------------------------
def test_T1_dangling_coupling_name_is_a_build_error():
    """``sources: [electrn]`` must fail at tick 0, not read nothing forever.

    This is B3's headline defect. The message has to carry both the bad name and
    the available ones, because the whole class of bug is a typo.
    """
    with pytest.raises(BusError) as ei:
        _sim([_Node("gauge", sources=["electrn"]), _Node("electron")])
    msg = str(ei.value)
    assert "electrn" in msg and "electron" in msg
    assert "silent None" in msg


def test_T2_topological_order_is_stable_on_registration_order():
    """An unconstrained pair keeps the order its author wrote.

    A sort that shuffled independent channels would move every committed
    baseline for no physical reason, so stability is a requirement, not a nicety.
    """
    g = build_graph([_Node("a"), _Node("b"), _Node("c")])
    assert g.order == ["a", "b", "c"]
    g2 = build_graph([_Node("c"), _Node("b"), _Node("a")])
    assert g2.order == ["c", "b", "a"]


def test_T3_a_real_dependency_reorders_and_is_reported():
    """A consumer declared before its producer is a recorded order violation."""
    sim = _sim([_Node("bag", sources=["quark"]), _Node("quark")])
    assert sim.graph.order == ["quark", "bag"]          # what it should be
    assert sim.graph.order_violations                   # ...and it is flagged
    # `auto` does not silently apply it — reordering is a physics change.
    assert sim.step_order == ["bag", "quark"]
    # ...but `topological` does, on request.
    s2 = _sim([_Node("bag", sources=["quark"]), _Node("quark")],
              bus={"order": "topological"})
    assert s2.step_order == ["quark", "bag"]


def test_T4_a_leapfrog_loop_is_a_cycle_not_a_misordering():
    """matter ↔ gauge is a cycle; its members keep declared order.

    Getting this wrong is worse than not sorting at all: a "topological sort"
    that broke a declared leapfrog would turn a same-tick coupling into a lagged
    one and call it a fix.
    """
    g = build_graph([_Node("gauge", sources=["q"]),
                     _Node("q", couplings={"strong": "gauge"})])
    assert g.cycles == [["gauge", "q"]]
    assert g.order == ["gauge", "q"]        # declared order preserved in-cycle
    assert not g.acyclic


def test_T5_jacobi_removes_order_dependence_inside_a_cycle():
    """Under ``jacobi`` every cycle member reads the same pre-tick snapshot.

    Checked by running the two orderings and comparing what each channel saw:
    under gauss_seidel they differ, under jacobi they must not.
    """
    def run(order, scheme):
        chs = [_Node("gauge", sources=["q"]),
               _Node("q", couplings={"strong": "gauge"})]
        if order == "reversed":
            chs = chs[::-1]
        s = _sim(chs, bus={"cycle_scheme": scheme, "order": "declared"})
        s.step(3)
        return {n: s.states[n]["seen"] for n in ("gauge", "q")}

    gs_a, gs_b = run("declared", "gauss_seidel"), run("reversed", "gauss_seidel")
    assert gs_a != gs_b, "gauss_seidel should be order-dependent — that is B3"

    j_a, j_b = run("declared", "jacobi"), run("reversed", "jacobi")
    assert j_a == j_b, "jacobi must not depend on order within the cycle"


def test_T6_two_providers_of_one_quantity_is_an_error():
    """Ambiguity a consumer could not resolve is refused at build time.

    Two differently-named channels both publishing ``J_em`` is not a naming
    nuisance — a consumer asking for ``J_em`` has no way to say which it meant,
    so picking one (say, the first) would be the engine making a physics choice
    on the scenario author's behalf.
    """
    class _Dual(_Node):
        type_name = "_bus_dual"

        def provides(self):
            return (self.name, "J_em")

    with pytest.raises(BusError, match="provided by both"):
        build_graph([_Dual("a"), _Dual("b")])
    # One provider is fine, and the consumer resolves to it.
    g = build_graph([_Dual("a"), _Node("c", source="J_em")])
    assert g.edges["c"] == ("a",)


def test_T8_config_refs_are_found_structurally_not_by_a_key_list():
    """A coupling is found because it *names a channel*, not because the engine
    knows its key.

    The curated-key-list approach failed twice: it missed ``couplings:`` (all 13
    matter↔gauge cycles looked like DAGs) and then, once patched, an exhaustive
    audit found **45 more edges** hiding under ``confine.field`` (12),
    ``confine.partners[]`` (30), ``fermion`` (2) and ``w_field`` (1). Each check
    below uses a key the engine has never heard of.
    """
    for key, cfg in (
        ("confine.field", {"confine": {"mode": "scalar", "field": "bag"}}),
        ("confine.partners", {"confine": {"partners": ["bag"]}}),
        ("a_novel_key", {"a_novel_key": "bag"}),
        ("deeply.nested", {"a": {"b": [{"c": "bag"}]}}),
    ):
        g = build_graph([_Node("bag"), _Node("q", **cfg)])
        assert g.edges["q"] == ("bag",), f"{key} not detected"
    # ...and a self-reference is not an edge
    g = build_graph([_Node("bag", note="bag")])
    assert g.edges["bag"] == ()


def test_T9_the_bag_quark_loop_is_a_cycle_in_every_bag_scenario():
    """`confine: {field: bag}` makes bag↔quark a genuine leapfrog cycle.

    This is the finding that resolved four of the five reported "ordering
    violations": they were **false positives**. The bag is declared before the
    quarks on purpose — it reads their pre-tick colour density and publishes the
    confining mass they read this tick. Reordering it would have converted a
    declared leapfrog into a lag while reporting a fix.
    """
    for name in ("proton_bag", "proton_bag_sc",
                 "realspace_proton_1fm", "realspace_neutron_1fm"):
        p = _repo_root() / "scenarios" / f"{name}.yaml"
        d = yaml.safe_load(p.read_text())
        chs = [build_channel(c) for c in d["channels"]]
        g = build_graph(chs)
        members = g.cycle_members()
        assert "bag" in members, f"{name}: bag is not in a cycle"
        assert any(c.name.startswith(("u_", "d_")) for c in chs
                   if c.name in members), f"{name}: no quark in the bag's cycle"
        # the declared order is preserved inside the cycle, so nothing moves
        assert g.order == [c.name for c in chs], name


def test_T10_the_free_variants_dangling_looking_edge_carries_no_data():
    """`unified_hydrogen_free`'s remaining violation is **vacuous**.

    Its matter channels have ``couplings: {}``, and `_publish_currents` only
    writes ``J_em``/``J_colour`` when the corresponding coupling is configured.
    So the gauge channels' ``sources:`` name channels that publish nothing: the
    edge resolves (the name is real) but carries no payload. Both orderings are
    therefore bit-identical and the gauge fields stay identically zero.

    Recorded as a test because it is a *new* silent-failure class, distinct from
    B3's typo: a **live name with no payload**. The strict check cannot catch it,
    because there is nothing wrong with the name.
    """
    import numpy as np
    from casim.engine.core.simulation import Simulation

    d = yaml.safe_load((_repo_root() / "scenarios"
                        / "unified_hydrogen_free.yaml").read_text())
    d.pop("output", None)
    d["ticks"] = 20

    def run(order):
        s = Simulation.from_scenario({**d, "bus": {"order": order}})
        s.step(20)
        return s

    a, b = run("declared"), run("topological")
    assert a.step_order != b.step_order, "the two orders should differ"

    compared = 0
    for n in a.channels:
        for k, va in a.states[n].items():
            vb = b.states[n].get(k)
            if isinstance(va, np.ndarray) and isinstance(vb, np.ndarray):
                assert np.array_equal(va, vb), f"{n}.{k} moved with the order"
                compared += 1
    assert compared >= 20, compared

    # the reason: nothing is published, so the sourced fields never turn on
    assert not [k for k in a.states["u_r"] if k.startswith("J_")]
    assert float(np.max(np.abs(a.states["photon_field"]["E"]))) == 0.0


def test_T7_every_shipped_scenario_resolves_strictly():
    """All 46 scenario YAMLs must have fully-resolvable couplings.

    This is the regression that keeps the strict check honest: if someone adds a
    scenario with a typo'd coupling target, it fails here rather than producing
    a plausible-looking run.
    """
    paths = sorted((_repo_root() / "scenarios").glob("*.yaml"))
    assert len(paths) >= 40, "scenario set unexpectedly small"
    checked = 0
    for p in paths:
        d = yaml.safe_load(p.read_text()) or {}
        specs = d.get("channels") or []
        if not specs:
            continue
        chs = [build_channel(c) for c in specs]
        g = build_graph(chs, d.get("bus"), strict=True)   # raises on a dangling name
        assert len(g.order) == len(chs)
        checked += 1
    assert checked >= 40
