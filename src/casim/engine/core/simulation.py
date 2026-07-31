"""casim.engine.core.simulation — the Simulation engine and LatticeSpec.

The one genuinely new component (roadmap §2).  The engine advances a set of
field *channels* one CA tick at a time and runs *observers* on a cadence.  It
knows nothing about the physics inside a channel — channel state is opaque — so
spectral, BCC, and dielectric channels all coexist behind one loop.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import numpy as np

from .channel import Channel, build_channel
from .observers import Observer, build_observer
from casim.constants import c_lat as C_LAT_REGISTRY

ROOT3 = float(np.sqrt(3.0))

CHECKPOINT_VERSION = 1


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
        target_ticks: int = 0,
        title: str = "",
        description: str = "",
        blockspin_schedule: Any = None,
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
            blockspin_schedule=scenario.get("blockspin", None),
        )

    # ------------------------------------------------------------------
    def step(self, n: int = 1) -> None:
        """Advance all channels by ``n`` ticks, running observers on cadence."""
        for _ in range(n):
            # Channels step in registration order, reading siblings' live
            # states via the shared mapping (Tier-2 coupling); the mapping is
            # updated in place so later channels see earlier channels' new
            # states this tick.
            for cname, ch in self.channels.items():
                self.states[cname] = ch.step(
                    self.states[cname], self.lattice,
                    context=self.states, rng=self.rng)
            self.tick += 1
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
        """Write a resumable snapshot to ``path`` (NPZ).  Returns the path."""
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
        }
        arrays["__meta__"] = np.frombuffer(
            json.dumps(meta).encode("utf-8"), dtype=np.uint8)
        np.savez(path, **arrays)
        if not path.endswith(".npz"):
            path = path + ".npz"
        return os.path.abspath(path)

    @classmethod
    def resume(cls, path: str) -> "Simulation":
        """Rebuild a Simulation from a checkpoint, ready to continue stepping."""
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
            )
            # Restore exact state (overwriting the fresh init_state above).
            layout = meta["state_layout"]
            for cname in sim.channels:
                st: Dict[str, Any] = dict(layout[cname]["scalars"])
                for key in layout[cname]["arrays"]:
                    st[key] = np.array(data[f"state::{cname}::{key}"])
                sim.states[cname] = st
            sim.tick = int(meta["tick"])
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
