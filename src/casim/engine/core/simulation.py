"""casim.engine.core.simulation — the Simulation engine and LatticeSpec.

The one genuinely new component (roadmap §2).  The engine advances a set of
field *channels* one CA tick at a time and runs *observers* on a cadence.  It
knows nothing about the physics inside a channel — channel state is opaque — so
spectral, BCC, and dielectric channels all coexist behind one loop.
"""
from __future__ import annotations

import json
import re
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import numpy as np

from .channel import Channel, build_channel
from .observers import Observer, build_observer
from .clock import Clock, ClockError, reconcile
from .graph import BusError, ChannelGraph, build_graph
from casim.constants import c_lat as C_LAT_REGISTRY

ROOT3 = float(np.sqrt(3.0))

#: Bumped to 2 by roadmap P3.2/P3.3: a checkpoint now round-trips the clock
#: (tick + dt + resolved mode) and the resolved bus order.  Version 1 files
#: still load — they are read as a synchronous unit-dt clock in declared order,
#: which is exactly what they were.
CHECKPOINT_VERSION = 2


def _parse_blockspin_schedule(spec: Any) -> Dict[int, int]:
    """Normalise a scenario ``blockspin:`` field into {tick: factor}.

    Accepts None, a single ``{at: T, factor: b}`` mapping, or a list of them.
    """
    if not spec:
        return {}
    if isinstance(spec, dict):
        spec = [spec]
    out: Dict[int, int] = {}
    for item in spec:
        at = int(item["at"])
        factor = int(item.get("factor", 2))
        if factor < 1:
            raise ValueError(f"blockspin factor must be ≥ 1, got {factor}")
        out[at] = factor
    return out


def _blockspin_merge(scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Combine a scenario's legacy ``blockspin:`` field with any ``do: blockspin``
    entries in its P4 ``events:`` timeline, as a list ``_parse_blockspin_schedule``
    accepts."""
    legacy = scenario.get("blockspin")
    combined: List[Dict[str, Any]] = []
    if isinstance(legacy, dict):
        combined.append(legacy)
    elif isinstance(legacy, list):
        combined.extend(legacy)
    combined.extend(_blockspin_from_events(scenario.get("events")))
    return combined


def _blockspin_from_events(events: Any) -> List[Dict[str, Any]]:
    """Extract ``do: blockspin`` entries from a P4 ``events:`` timeline.

    The generic events timeline (P4) is validated by ``casim.io.schema``; here
    the engine consumes the one action it already has native machinery for —
    a timed block-spin — by translating it into the ``{at, factor}`` form
    ``_parse_blockspin_schedule`` accepts.  Other actions are left for the
    engine's event dispatch to grow into and are ignored here rather than
    silently dropped elsewhere.
    """
    if not events:
        return []
    out: List[Dict[str, Any]] = []
    for ev in events:
        if isinstance(ev, dict) and ev.get("do") == "blockspin" and "at" in ev:
            out.append({"at": ev["at"], "factor": ev.get("factor", 2)})
    return out


@dataclass
class LatticeSpec:
    """Lattice substrate: size, dimensionality, topology, signal speed.

    Block-spin (Phase 4, F133): ``block`` is the number of physical cells per
    axis that each simulated super-cell stands for.  A run therefore simulates
    ``L`` super-cells but *declares* a physical patch of ``physical_L = L·block``
    cells per axis (``cell_factor = block^dims`` physical cells each).  c_lat is
    an RG fixed point (F130 T1), carried through unchanged.
    """
    L: int = 32
    dims: int = 3
    topology: str = "cubic"        # "cubic" | "bcc"
    c_lat: float = C_LAT_REGISTRY  # F26 rotation-rate speed of light
    block: int = 1                 # physical cells per super-cell per axis (R_b)

    @property
    def physical_L(self) -> int:
        """Physical cells per axis represented: L · block."""
        return int(self.L) * int(self.block)

    @property
    def cell_factor(self) -> int:
        """Physical cells per super-cell: block^dims."""
        return int(self.block) ** int(self.dims)

    def validate_channel(self, ch: Channel) -> None:
        if self.topology not in ch.topologies:
            raise ValueError(
                f"channel {ch.name!r} ({ch.type_name}) supports "
                f"{ch.topologies}, but lattice topology is {self.topology!r}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {"L": self.L, "dims": self.dims,
                "topology": self.topology, "c_lat": self.c_lat,
                "block": self.block,
                "physical_L": self.physical_L,
                "cell_factor": self.cell_factor}


class Simulation:
    """Advance channels on a shared lattice and collect observer records."""

    def __init__(
        self,
        lattice: LatticeSpec,
        channels: List[Channel],
        observers: Optional[List[Observer]] = None,
        seed: int = 0,
        name: str = "run",
        checkpoint_every: int = 0,
        checkpoint_dir: str = "checkpoints",
        checkpoint_compress: bool = True,
        checkpoint_keep: int = 3,
        target_ticks: int = 0,
        title: str = "",
        description: str = "",
        blockspin_schedule: Any = None,
        clock: Optional[Dict[str, Any]] = None,
        bus: Optional[Dict[str, Any]] = None,
    ):
        self.lattice = lattice
        self.name = name
        #: presentation-only scenario metadata (YAML title:/description:);
        #: ``name`` remains the stable run identifier.
        self.title = str(title or "")
        self.description = str(description or "")
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)
        self.tick = 0
        self.checkpoint_every = int(checkpoint_every)
        self.checkpoint_dir = checkpoint_dir
        #: P2.6 — compress snapshots (field states compress well) and keep only
        #: the newest N auto-checkpoints so a multi-day run cannot fill a disk.
        self.checkpoint_compress = bool(checkpoint_compress)
        self.checkpoint_keep = int(checkpoint_keep)
        self.target_ticks = int(target_ticks)
        #: scheduled block-spin events {tick: factor} (Phase 4); applied in step()
        self._blockspin_schedule = _parse_blockspin_schedule(blockspin_schedule)
        #: log of applied R_b operations, surfaced in collect_results()
        self.blockspin_events: List[Dict[str, Any]] = []

        self.channels: Dict[str, Channel] = {}
        self.states: Dict[str, Any] = {}
        self._energy0: Dict[str, float] = {}
        for ch in channels:
            lattice.validate_channel(ch)
            if ch.name in self.channels:
                raise ValueError(f"duplicate channel name {ch.name!r}")
            self.channels[ch.name] = ch
            self.states[ch.name] = ch.init_state(lattice, self.rng)
            self._energy0[ch.name] = ch.energy(self.states[ch.name])

        self.observers: List[Observer] = list(observers or [])
        self.results: Dict[str, Any] = {}

        # --- P3.2: the engine owns physical time -------------------------
        # Built AFTER the channels so it can read their configs, and before any
        # step so an unreconcilable clock is a build-time error.
        self._clock_spec = dict(clock or {})
        self.clock: Clock = reconcile(list(self.channels.values()),
                                      self._clock_spec)
        self.clock.tick = self.tick

        # --- P3.3: the typed exchange bus --------------------------------
        self._bus_spec = dict(bus or {})
        self.graph: ChannelGraph = self._build_bus()

    # ------------------------------------------------------------------
    def _build_bus(self) -> ChannelGraph:
        """Resolve the exchange bus and decide the execution order.

        ``bus.order``:

        ``auto`` (default)
            Apply the topological order **only when it already equals the
            declared order**.  Otherwise keep the declared order and record the
            violation.  This is what makes P3.3 land without moving a single
            committed baseline: reordering a scenario's channels is a *physics*
            change (it turns a same-tick coupling into a lagged one), so it is
            opt-in per scenario rather than a side effect of an engine upgrade.
        ``topological``
            Apply the sorted order.  The correct target state.
        ``declared``
            Never reorder; still validate names and report violations.

        ``bus.strict`` (default ``True``) makes a ``consumes`` name that nothing
        provides a build-time :class:`BusError` instead of a silent ``None``.
        """
        spec = dict(self._bus_spec)
        mode = str(spec.pop("order", "auto")).lower()
        if mode not in ("auto", "topological", "declared"):
            raise BusError(
                f"bus.order must be 'auto', 'topological' or 'declared', "
                f"got {mode!r}")
        g = build_graph(list(self.channels.values()), spec,
                        strict=bool(spec.get("strict", True)))
        declared = list(self.channels.keys())
        g.order_violations = [n for n, d in zip(declared, g.order) if n != d]
        g.order_mode = mode
        if mode == "declared" or (mode == "auto" and g.order_violations):
            g.applied_order = declared
        else:
            g.applied_order = list(g.order)
        return g

    @property
    def step_order(self) -> List[str]:
        """Channel names in the order ``step()`` walks them this tick."""
        return list(getattr(self.graph, "applied_order", list(self.channels)))

    # ------------------------------------------------------------------
    @classmethod
    def from_scenario(cls, scenario: Dict[str, Any]) -> "Simulation":
        """Build a Simulation from a parsed scenario dict (see casim.io)."""
        lat = scenario.get("lattice", {})
        block = int(lat.get("block", 1))
        if "physical_patch" in lat:
            # declare the physical patch + block factor; derive the super-cell L
            phys = int(lat["physical_patch"])
            if phys % block != 0:
                raise ValueError(
                    f"physical_patch={phys} not divisible by block={block}")
            L = phys // block
        else:
            L = int(lat.get("L", 32))
        lattice = LatticeSpec(
            L=L,
            dims=int(lat.get("dims", 3)),
            topology=str(lat.get("topology", "cubic")),
            c_lat=float(lat.get("c_lat", C_LAT_REGISTRY)),
            block=block,
        )
        channels = [build_channel(c) for c in scenario.get("channels", [])]
        observers = [build_observer(o) for o in scenario.get("observers", [])]
        ckpt = scenario.get("checkpoint", {}) or {}
        return cls(
            lattice=lattice,
            channels=channels,
            observers=observers,
            seed=int(scenario.get("seed", 0)),
            name=str(scenario.get("name", "run")),
            checkpoint_every=int(ckpt.get("every", 0)),
            checkpoint_dir=str(ckpt.get("dir", "checkpoints")),
            target_ticks=int(scenario.get("ticks", 0)),
            title=str(scenario.get("title", "")),
            description=str(scenario.get("description", "")),
            blockspin_schedule=_blockspin_merge(scenario),
            clock=scenario.get("clock", None),
            bus=scenario.get("bus", None),
        )

    # ------------------------------------------------------------------
    def step(self, n: int = 1) -> None:
        """Advance all channels by ``n`` engine ticks, observers on cadence.

        One engine tick is ``self.clock.dt`` of physical time (P3.2).  Channels
        walk :attr:`step_order` — the bus-resolved order (P3.3), which defaults
        to registration order — and each is stepped ``clock.n_sub(name)`` times,
        so a channel whose native step is finer than the global ``dt`` catches
        up instead of silently running slow.

        Cycle scheme (P3.3).  Under ``gauss_seidel`` the context mapping is
        updated in place, so a channel sees the *already-updated* states of
        those before it and the *pre-tick* states of those after it — the
        historical behaviour.  Under ``jacobi`` every channel in a declared
        cycle reads a frozen pre-tick snapshot, so the result does not depend on
        order within the cycle at all.
        """
        jacobi = (self.graph.cycle_scheme == "jacobi"
                  and bool(self.graph.cycles))
        cycle_members = self.graph.cycle_members() if jacobi else set()
        order = self.step_order
        for _ in range(n):
            frozen = ({c: self.states[c] for c in cycle_members}
                      if jacobi else None)
            for cname in order:
                ch = self.channels[cname]
                ctx = self.states
                if jacobi and cname in cycle_members:
                    # Pre-tick view of the cycle, live view of everything else.
                    ctx = dict(self.states)
                    ctx.update(frozen)
                st = self.states[cname]
                for _s in range(self.clock.n_sub(cname)):
                    st = ch.step(st, self.lattice, context=ctx, rng=self.rng)
                    if not jacobi:
                        self.states[cname] = st
                self.states[cname] = st
            self.tick += 1
            self.clock.tick = self.tick
            self._run_observers()
            if self.tick in self._blockspin_schedule:
                self.block_spin(self._blockspin_schedule[self.tick])
            if self.checkpoint_every and self.tick % self.checkpoint_every == 0:
                self.checkpoint(self._auto_checkpoint_path())

    # ------------------------------------------------------------------
    def block_spin(self, b: int) -> Dict[str, Any]:
        """Apply the block-spin transform R_b as a first-class engine operation
        (Phase 4, F133).

        Coarse-grains every channel state in place (grouping b^dims fine
        super-cells into one), shrinks the lattice L → L/b and accumulates the
        block factor so the lattice keeps representing the SAME physical patch
        (``physical_L`` invariant; c_lat is the F130-T1 fixed point, unchanged).
        Subsequent ``step`` calls then advance the coarse field — the channels
        that support a renormalised rule (even-law, F130 T1/T2) stay physically
        faithful.  Returns the recorded event.
        """
        if b == 1:
            return {"tick": self.tick, "factor": 1, "noop": True}
        if self.lattice.L % b != 0:
            raise ValueError(
                f"cannot block-spin L={self.lattice.L} by b={b} (not divisible)")
        phys_before = self.lattice.physical_L
        for cname, ch in self.channels.items():
            self.states[cname] = ch.block_spin(self.states[cname],
                                               self.lattice, b)
        self.lattice.L //= b
        self.lattice.block *= b
        assert self.lattice.physical_L == phys_before, "physical patch not conserved"
        for ch in self.channels.values():
            self.lattice.validate_channel(ch)
        # energy baseline is representation-dependent across R_b; refresh it
        self._energy0 = {c: ch.energy(self.states[c])
                         for c, ch in self.channels.items()}
        event = {
            "tick": self.tick, "factor": b,
            "L_after": self.lattice.L, "block_after": self.lattice.block,
            "physical_L": self.lattice.physical_L,
            "cells_per_supercell": self.lattice.cell_factor,
        }
        self.blockspin_events.append(event)
        return event

    def run(self, ticks: int) -> Dict[str, Any]:
        """Run for ``ticks`` ticks (observers also fire once at tick 0)."""
        self._run_observers()  # baseline
        self.step(ticks)
        return self.collect_results()

    def _run_observers(self) -> None:
        for obs in self.observers:
            if obs.should_run(self.tick):
                obs.observe(self)

    # ------------------------------------------------------------------
    def collect_results(self) -> Dict[str, Any]:
        self.results = {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "seed": self.seed,
            "ticks": self.tick,
            "lattice": self.lattice.to_dict(),
            "channels": {c: ch.describe() for c, ch in self.channels.items()},
            "observers": {obs.name: obs.result() for obs in self.observers},
        }
        # P3.2/P3.3 — the clock and the bus are reported on every run, including
        # when they changed nothing.  A desynchronised scenario that produces a
        # normal-looking results file is exactly the failure this phase exists
        # to end, so `synchronous: false` has to be visible in the artifact.
        self.results["clock"] = self.clock.to_dict()
        self.results["bus"] = {
            **self.graph.to_dict(),
            "order_mode": getattr(self.graph, "order_mode", "auto"),
            "applied_order": self.step_order,
            "order_violations": getattr(self.graph, "order_violations", []),
            "unresolved": getattr(self.graph, "unresolved", []),
        }
        if self.lattice.block > 1 or self.blockspin_events:
            from .blockspin import patch_summary
            self.results["physical_patch"] = patch_summary(self.lattice)
            self.results["blockspin_events"] = self.blockspin_events
        return self.results

    def state_norms(self) -> Dict[str, float]:
        return {c: ch.energy(self.states[c]) for c, ch in self.channels.items()}

    # ==================================================================
    # Checkpointing & resume (roadmap §4) — NPZ snapshot of all channel
    # states + tick + RNG state, enough to continue a long run that
    # exceeds the sandbox time limit.
    # ==================================================================
    def _auto_checkpoint_path(self) -> str:
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        return os.path.join(self.checkpoint_dir, f"{self.name}_t{self.tick}.npz")

    def checkpoint(self, path: str) -> str:
        """Write a resumable snapshot to ``path`` (NPZ).  Returns the path.

        Roadmap **P2.6**: atomic, optionally compressed, and rotating.

        The pre-P2.6 version was a bare ``np.savez`` called from inside the tick
        loop with no rotation — the likeliest single way a multi-day run loses
        everything, because a kill during the write leaves a truncated file
        *at the name the resume path looks for*, so the crash destroys the
        previous good checkpoint as well as the current one. Three changes:

        * **atomic** — write to ``<path>.tmp-<pid>`` then ``os.replace``, which
          is atomic on POSIX and Windows. A kill mid-write now leaves the last
          good checkpoint intact and a stray ``.tmp`` file.
        * **compressed** — ``savez_compressed`` when :attr:`checkpoint_compress`
          is set (the default). Field states are smooth arrays and compress
          well; the cost is CPU on a path that is already I/O-bound.
        * **rotating** — keep the last :attr:`checkpoint_keep` auto-checkpoints
          and unlink the rest, so a long run cannot fill the disk. Only files
          matching this run's own auto-checkpoint pattern are ever removed, and
          an explicit ``checkpoint(path)`` call is never rotated away.

        Note the sandbox caveat recorded in CLAUDE.md: this mount refuses
        ``unlink``, so rotation is best-effort and a failure to remove an old
        checkpoint is logged into the return value's directory, never raised —
        losing a rotation is not worth losing a run over.
        """
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
        arrays: Dict[str, np.ndarray] = {}
        state_layout: Dict[str, Dict[str, Any]] = {}
        for cname, st in self.states.items():
            layout = {"arrays": [], "scalars": {}}
            for key, val in st.items():
                if isinstance(val, np.ndarray):
                    akey = f"state::{cname}::{key}"
                    arrays[akey] = val
                    layout["arrays"].append(key)
                else:
                    layout["scalars"][key] = val
            state_layout[cname] = layout

        meta = {
            "version": CHECKPOINT_VERSION,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "seed": self.seed,
            "tick": self.tick,
            "target_ticks": self.target_ticks,
            "lattice": self.lattice.to_dict(),
            "rng_state": self.rng.bit_generator.state,
            "energy0": self._energy0,
            "channels": [ch.spec() for ch in self.channels.values()],
            "observers": [obs.spec() for obs in self.observers],
            "observer_records": [obs.records for obs in self.observers],
            "state_layout": state_layout,
            "checkpoint_every": self.checkpoint_every,
            "checkpoint_dir": self.checkpoint_dir,
            # P2.6: carried so `resume()` can restore it. Its absence was a
            # silent-wrong bug, not a missing feature — see `resume()`.
            "blockspin_schedule": {str(k): int(v)
                                   for k, v in self._blockspin_schedule.items()},
            "blockspin_events": self.blockspin_events,
            # P3.2/P3.3. Carried for the same reason `blockspin_schedule` is:
            # a resumed run that silently reverts to a different clock or a
            # different channel order completes and reports success while doing
            # different physics. Round-trip the *spec*, not the resolved Clock —
            # the resolution is deterministic from the spec plus the channels,
            # so re-deriving it on resume also proves the two agree.
            "clock_spec": self._clock_spec,
            "bus_spec": self._bus_spec,
        }
        arrays["__meta__"] = np.frombuffer(
            json.dumps(meta).encode("utf-8"), dtype=np.uint8)

        final = path if path.endswith(".npz") else path + ".npz"
        # Atomic. Note np.savez *appends* `.npz` to a path that lacks it, so
        # passing a temp *name* would silently produce `<tmp>.npz` and the
        # rename would then fail on a file that does not exist. Handing it an
        # open file object writes exactly where told, with no name rewriting.
        tmp = f"{final}.tmp-{os.getpid()}"
        saver = np.savez_compressed if self.checkpoint_compress else np.savez
        try:
            with open(tmp, "wb") as fh:
                saver(fh, **arrays)
            os.replace(tmp, final)
        except BaseException:
            try:
                os.remove(tmp)
            except OSError:
                pass
            raise
        self._rotate_checkpoints()
        return os.path.abspath(final)

    def _rotate_checkpoints(self) -> None:
        """Keep the newest ``checkpoint_keep`` auto-checkpoints of THIS run.

        Deliberately narrow: it only ever considers files matching this run's
        own ``{name}_t{tick}.npz`` pattern in ``checkpoint_dir``, and sorts by
        the tick parsed out of the filename rather than by mtime — a resumed run
        rewrites old ticks with new mtimes, so mtime order would delete the
        wrong ones. ``checkpoint_keep <= 0`` disables rotation.
        """
        keep = int(self.checkpoint_keep)
        if keep <= 0:
            return
        pat = re.compile(rf"^{re.escape(self.name)}_t(\d+)\.npz$")
        try:
            entries = os.listdir(self.checkpoint_dir)
        except OSError:
            return
        found: List[tuple] = []
        for fn in entries:
            m = pat.match(fn)
            if m:
                found.append((int(m.group(1)), fn))
        for _, fn in sorted(found, reverse=True)[keep:]:
            try:
                os.remove(os.path.join(self.checkpoint_dir, fn))
            except OSError:
                # This mount refuses unlink (CLAUDE.md). A failed rotation is
                # disk pressure; raising here would lose the run instead.
                pass

    @classmethod
    def resume(cls, path: str) -> "Simulation":
        """Rebuild a Simulation from a checkpoint, ready to continue stepping.

        Roadmap **P2.6** fixed a silent-wrong bug here: this method did not pass
        ``blockspin_schedule`` to the constructor, so a resumed run had an empty
        schedule and **skipped every remaining scheduled $R_b$ event** while
        reporting success. That is worse than a crash — the run completes, the
        results file looks normal, and the block-spin physics the scenario asked
        for simply did not happen. The schedule and the applied-event log are
        now both round-tripped, and `tests/casim/test_checkpoint_ops.py` asserts
        it rather than trusting it.
        """
        with np.load(path, allow_pickle=False) as data:
            meta = json.loads(bytes(data["__meta__"]).decode("utf-8"))
            lat = meta["lattice"]
            lattice = LatticeSpec(
                L=int(lat["L"]), dims=int(lat["dims"]),
                topology=str(lat["topology"]), c_lat=float(lat["c_lat"]),
                block=int(lat.get("block", 1)),
            )
            channels = [build_channel(c) for c in meta["channels"]]
            observers = [build_observer(o) for o in meta["observers"]]
            sim = cls(
                lattice=lattice, channels=channels, observers=observers,
                seed=int(meta["seed"]), name=str(meta["name"]),
                checkpoint_every=int(meta.get("checkpoint_every", 0)),
                checkpoint_dir=str(meta.get("checkpoint_dir", "checkpoints")),
                target_ticks=int(meta.get("target_ticks", 0)),
                title=str(meta.get("title", "")),
                description=str(meta.get("description", "")),
                # P2.6. `_parse_blockspin_schedule` wants the scenario shape
                # (`[{at, factor}]`), so convert back from the stored map. A
                # pre-P2.6 checkpoint has no such key and resumes with an empty
                # schedule, exactly as it did before — old files stay loadable.
                blockspin_schedule=[
                    {"at": int(k), "factor": int(v)}
                    for k, v in (meta.get("blockspin_schedule") or {}).items()
                ],
                # A version-1 checkpoint has neither key and resumes as a
                # synchronous unit-dt clock in declared order — which is
                # precisely what it was, so old files stay loadable.
                clock=meta.get("clock_spec") or None,
                bus=meta.get("bus_spec") or None,
            )
            sim.blockspin_events = list(meta.get("blockspin_events") or [])
            # Restore exact state (overwriting the fresh init_state above).
            layout = meta["state_layout"]
            for cname in sim.channels:
                st: Dict[str, Any] = dict(layout[cname]["scalars"])
                for key in layout[cname]["arrays"]:
                    st[key] = np.array(data[f"state::{cname}::{key}"])
                sim.states[cname] = st
            sim.tick = int(meta["tick"])
            sim.clock.tick = sim.tick
            sim.rng.bit_generator.state = meta["rng_state"]
            sim._energy0 = {k: float(v) for k, v in meta["energy0"].items()}
            for obs, recs in zip(sim.observers, meta["observer_records"]):
                obs.records = recs
        return sim

    def run_to_target(self) -> Dict[str, Any]:
        """Continue stepping until ``target_ticks`` is reached."""
        remaining = max(0, self.target_ticks - self.tick)
        if remaining:
            self.step(remaining)
        return self.collect_results()
