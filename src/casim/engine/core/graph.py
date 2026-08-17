"""casim.engine.core.graph — the typed exchange bus (roadmap P3.3, blocker B3).

*Created 2026-07-31 - 22:25.*

Before this module, channel ordering was **load-bearing and unchecked**.
``Simulation.step`` iterated ``self.channels`` in registration order — i.e. the
order the ``channels:`` list happened to appear in the YAML — updating the
shared context mapping in place, so a channel saw the *already-updated* state of
everything listed above it and the *pre-tick* state of everything below it.
That is a Gauss–Seidel sweep whose sweep order is a text-file line number.

Two failure modes followed, and both are silent:

1. **Reordering the YAML changes the physics.**  Moving ``w_sourced`` below the
   fermion doublet it sources turns a same-tick coupling into a one-tick-lagged
   one, with no error and no record.  The docstrings of the coupled channels say
   things like "register this BEFORE the fermion channel" — a comment doing a
   type system's job.
2. **A misspelled coupling target is a silent ``None``.**  ``sources: {electrn:
   1.0}`` looks up a key that is not in the context, the channel reads nothing,
   and the run completes with that coupling simply absent.

This module replaces the line number with a declared dependency graph.  Each
channel declares :meth:`~casim.engine.core.channel.Channel.provides` and
:meth:`~casim.engine.core.channel.Channel.consumes`; the engine resolves
consumers to producers, **errors at build time** on a dangling name, and
topologically sorts the result.

Cycles are expected, not exceptional — a fermion sourcing a gauge field that
back-reacts on the fermion *is* a cycle, and it is the physics.  A cycle is
therefore resolved by an **explicitly declared scheme** rather than by line
order:

``gauss_seidel`` (default)
    Break the cycle at its declared entry point and sweep, reading updated
    upstream states.  This reproduces today's behaviour exactly when the
    declared order matches the YAML order, which is how the migration stays
    bit-identical.
``jacobi``
    Every channel in the cycle reads the *pre-tick* state of the whole cycle,
    so the result no longer depends on order within the cycle at all.  Costs one
    extra copy of the cycle's states per tick.

Determinism note: the sort is stable on the original registration order, so a
scenario whose graph does not constrain two channels relative to each other
keeps the order its author wrote.  A topological sort that shuffled independent
channels would make every existing baseline move for no physical reason.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence, Set, Tuple

__all__ = [
    "BusError",
    "ChannelGraph",
    "build_graph",
]


class BusError(ValueError):
    """A scenario's channel couplings do not form a resolvable graph.

    Raised at **build time**.  The whole point of P3.3 is that an unsatisfied
    ``consumes`` stops being a silent ``None`` at tick 400 and becomes an error
    at tick 0, with the offending name and the available names printed.
    """


@dataclass
class ChannelGraph:
    """The resolved dependency graph over a scenario's channels."""

    #: execution order (channel names), topologically sorted, stable
    order: List[str] = field(default_factory=list)
    #: name -> quantities it publishes
    provides: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    #: name -> quantities it reads
    consumes: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    #: name -> upstream channel names it depends on
    edges: Dict[str, Tuple[str, ...]] = field(default_factory=dict)
    #: strongly-connected components with more than one member, in order
    cycles: List[List[str]] = field(default_factory=list)
    #: how cycles are resolved: "gauss_seidel" | "jacobi"
    cycle_scheme: str = "gauss_seidel"
    #: True when the sort had to preserve registration order inside a cycle
    order_is_declared: bool = True

    @property
    def acyclic(self) -> bool:
        return not self.cycles

    def cycle_members(self) -> Set[str]:
        return {n for c in self.cycles for n in c}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order": list(self.order),
            "provides": {k: list(v) for k, v in self.provides.items()},
            "consumes": {k: list(v) for k, v in self.consumes.items()},
            "edges": {k: list(v) for k, v in self.edges.items()},
            "cycles": [list(c) for c in self.cycles],
            "cycle_scheme": self.cycle_scheme,
            "acyclic": self.acyclic,
        }

    def report(self) -> str:
        lines = [f"exchange bus  {len(self.order)} channels  "
                 f"{'acyclic' if self.acyclic else f'{len(self.cycles)} cycle(s), scheme={self.cycle_scheme}'}"]
        for n in self.order:
            dep = ", ".join(self.edges.get(n, ())) or "-"
            lines.append(f"  {n:<24} consumes<- {dep}")
        for c in self.cycles:
            lines.append(f"  cycle: {' -> '.join(c)} -> {c[0]}")
        return "\n".join(lines)


def _tarjan_sccs(nodes: Sequence[str],
                 succ: Dict[str, Tuple[str, ...]]) -> List[List[str]]:
    """Strongly-connected components, iterative (no recursion depth limit).

    Iterative on purpose: a long linear chain of channels would blow the Python
    recursion limit in the textbook recursive form, and a crash whose message is
    ``RecursionError`` tells a physicist nothing about their scenario.
    """
    index: Dict[str, int] = {}
    low: Dict[str, int] = {}
    on_stack: Dict[str, bool] = {}
    stack: List[str] = []
    out: List[List[str]] = []
    counter = 0

    for root in nodes:
        if root in index:
            continue
        work: List[Tuple[str, int]] = [(root, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index[v] = low[v] = counter
                counter += 1
                stack.append(v)
                on_stack[v] = True
            recursed = False
            succs = succ.get(v, ())
            for i in range(pi, len(succs)):
                w = succs[i]
                work[-1] = (v, i + 1)
                if w not in index:
                    work.append((w, 0))
                    recursed = True
                    break
                if on_stack.get(w):
                    low[v] = min(low[v], index[w])
            if recursed:
                continue
            if low[v] == index[v]:
                comp: List[str] = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
            work.pop()
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[v])
    return out


def _config_channel_refs(ch, names: Set[str]) -> Tuple[str, ...]:
    """Every string *anywhere* in ``ch.config`` that names another channel.

    This is the structural answer to a bug that has now occurred twice.
    ``Channel.consumes`` originally read a hand-maintained list of config keys
    (``sources``, ``partner``, …).  It missed ``couplings:`` — which made all 13
    matter↔gauge cycles look like DAGs (F269) — and, once that was patched, an
    exhaustive audit found it still missed **45 more edges** across four key
    paths: ``confine.field`` (12), ``confine.partners[]`` (30), ``fermion`` (2)
    and ``w_field`` (1).

    A curated key list cannot be right, because the key is chosen by whoever
    writes a channel and the graph is maintained by whoever writes the engine.
    So the graph stops guessing which keys are couplings and instead uses the
    one fact it holds and a channel does not: **the set of channel names in this
    scenario.**  Any config string that *is* another channel's name is a
    reference to that channel — there is no other reason for it to be there.

    This over-reads only if a scenario uses a channel's name as an unrelated
    string value (a label, a mode); the resulting edge is spurious but harmless,
    because a spurious dependency can at worst constrain an order that was
    already free, whereas a *missing* dependency silently turns a coupling into
    a lag. The asymmetry is the whole argument.
    """
    out: List[str] = []
    seen: Set[str] = set()

    def walk(o) -> None:
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                walk(v)
        elif isinstance(o, str) and o in names and o != ch.name and o not in seen:
            seen.add(o)
            out.append(o)

    walk(ch.config or {})
    return tuple(out)


def build_graph(channels: Sequence, spec: Dict[str, Any] | None = None,
                strict: bool = True) -> ChannelGraph:
    """Resolve ``channels`` into a :class:`ChannelGraph`.

    ``spec`` keys: ``cycle_scheme`` (``gauss_seidel`` | ``jacobi``) and
    ``strict`` (override the argument).

    With ``strict`` (the default), a ``consumes`` name that no channel provides
    is a :class:`BusError`.  ``strict=False`` downgrades it to a recorded
    ``unresolved`` edge — needed only for the pre-P3.3 scenarios whose configs
    carry non-channel keys, and the engine reports the count so the exemption
    cannot quietly become permanent.
    """
    spec = dict(spec or {})
    strict = bool(spec.get("strict", strict))
    scheme = str(spec.get("cycle_scheme", "gauss_seidel")).lower()
    if scheme not in ("gauss_seidel", "jacobi"):
        raise BusError(
            f"cycle_scheme must be 'gauss_seidel' or 'jacobi', got {scheme!r}")

    names = [ch.name for ch in channels]
    provides: Dict[str, Tuple[str, ...]] = {}
    consumes: Dict[str, Tuple[str, ...]] = {}
    producer: Dict[str, str] = {}

    for ch in channels:
        p = tuple(ch.provides())
        provides[ch.name] = p
        for q in p:
            # First declarer wins; a second is a genuine ambiguity because the
            # consumer could not say which one it meant.
            if q in producer and producer[q] != ch.name:
                raise BusError(
                    f"quantity {q!r} is provided by both {producer[q]!r} and "
                    f"{ch.name!r}; a consumer cannot disambiguate. Rename one, "
                    f"or have the consumer name the channel directly.")
            producer[q] = ch.name

    unresolved: List[Tuple[str, str]] = []
    edges: Dict[str, Tuple[str, ...]] = {}
    all_names = set(names)
    for ch in channels:
        # Declared consumes (named quantities a channel computes) UNION every
        # config string that names a sibling. See `_config_channel_refs` for why
        # the second half exists and why it is not a curated key list.
        declared = tuple(ch.consumes())
        c = declared + tuple(q for q in _config_channel_refs(ch, all_names)
                             if q not in declared)
        consumes[ch.name] = c
        dep: List[str] = []
        for q in c:
            src = producer.get(q)
            if src is None:
                if strict:
                    raise BusError(
                        f"channel {ch.name!r} ({ch.type_name}) consumes {q!r}, "
                        f"which no channel provides.\n"
                        f"  available: {sorted(producer)}\n"
                        f"  This was previously a silent None — the coupling "
                        f"simply did not happen and the run reported success.")
                unresolved.append((ch.name, q))
                continue
            if src != ch.name and src not in dep:
                dep.append(src)
        edges[ch.name] = tuple(dep)

    # Topological sort, stable on registration order.  `edges[v]` lists v's
    # dependencies, so an edge runs dep -> v.
    succ: Dict[str, Tuple[str, ...]] = {n: () for n in names}
    for v, deps in edges.items():
        for d in deps:
            succ[d] = succ[d] + (v,)

    sccs = _tarjan_sccs(names, succ)
    rank = {n: i for i, n in enumerate(names)}
    comp_of: Dict[str, int] = {}
    comps: List[List[str]] = []
    for comp in sccs:
        comp_sorted = sorted(comp, key=lambda n: rank[n])
        idx = len(comps)
        comps.append(comp_sorted)
        for n in comp_sorted:
            comp_of[n] = idx

    # Condensation is a DAG; Kahn over it, breaking ties by earliest member.
    cdeps: Dict[int, Set[int]] = {i: set() for i in range(len(comps))}
    for v, deps in edges.items():
        for d in deps:
            if comp_of[d] != comp_of[v]:
                cdeps[comp_of[v]].add(comp_of[d])

    ready = sorted((i for i, d in cdeps.items() if not d),
                   key=lambda i: rank[comps[i][0]])
    order: List[str] = []
    done: Set[int] = set()
    remaining = dict(cdeps)
    while ready:
        i = ready.pop(0)
        done.add(i)
        order.extend(comps[i])
        newly = []
        for j, d in remaining.items():
            if j in done or j in ready:
                continue
            if d <= done:
                newly.append(j)
        ready = sorted(ready + newly, key=lambda k: rank[comps[k][0]])
    if len(order) != len(names):        # defensive; condensation is acyclic
        missing = [n for n in names if n not in order]
        raise BusError(f"could not order channels {missing!r}")

    cycles = [c for c in comps if len(c) > 1]
    # A self-loop (a channel consuming its own output) is a cycle of one and is
    # legitimate — it is just a stateful stepper — so it is not reported.

    g = ChannelGraph(order=order, provides=provides, consumes=consumes,
                     edges=edges, cycles=cycles, cycle_scheme=scheme)
    if unresolved:
        g.to_dict  # keep the dataclass shape; record on the instance
        setattr(g, "unresolved", unresolved)
    return g
