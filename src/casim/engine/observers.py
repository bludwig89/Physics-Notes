"""casim.engine.observers — diagnostics that run every N ticks.

Observers replace the inline diagnostics duplicated across the historical
``run_*`` scripts.  Each declares an ``exactness`` class (``"exact"`` |
``"machine-precision"`` | ``"quantitative"``) so a future pass can regenerate
``exactness-inventory.md`` rather than maintain it by hand (roadmap Phase F).

An observer is called with the live ``Simulation`` and appends structured
records into ``sim.results["observers"][<observer-name>]``.
"""
from __future__ import annotations

from typing import Any, Dict, List
import numpy as np  # noqa: F401  (available to observer subclasses)


class Observer:
    name: str = "observer"
    exactness: str = "quantitative"

    def __init__(self, every: int = 1, **config: Any):
        self.every = max(1, int(every))
        self.config = dict(config)
        self.records: List[Dict[str, Any]] = []

    def should_run(self, tick: int) -> bool:
        return tick % self.every == 0

    def observe(self, sim) -> None:
        raise NotImplementedError

    def summary(self) -> Dict[str, Any]:
        """One-shot end-of-run summary (overridable)."""
        return {}

    def result(self) -> Dict[str, Any]:
        return {
            "type": self.name,
            "exactness": self.exactness,
            "every": self.every,
            "records": self.records,
            "summary": self.summary(),
        }

    def spec(self) -> Dict[str, Any]:
        """Round-trippable build spec: ``build_observer(o.spec())`` rebuilds it."""
        return {"type": self.name, "every": self.every, **self.config}


# ----------------------------------------------------------------------
_OBS_REGISTRY: Dict[str, type] = {}


def register_observer(cls):
    _OBS_REGISTRY[cls.name] = cls
    return cls


def build_observer(spec: Dict[str, Any]) -> "Observer":
    spec = dict(spec)
    type_name = spec.pop("type")
    try:
        cls = _OBS_REGISTRY[type_name]
    except KeyError:
        raise KeyError(f"unknown observer {type_name!r}; "
                       f"registered: {sorted(_OBS_REGISTRY)}")
    return cls(**spec)


def registered_observers() -> Dict[str, type]:
    return dict(_OBS_REGISTRY)


# ======================================================================
# Concrete observers
# ======================================================================
@register_observer
class NormConservation(Observer):
    """Track relative drift of each channel's conserved scalar vs tick 0."""
    name = "norm_conservation"
    exactness = "machine-precision"

    def observe(self, sim) -> None:
        # Optional `channels` filter: restrict to genuinely norm-conserving
        # channels (e.g. exclude a sourced field whose energy physically grows).
        only = self.config.get("channels")
        rec = {"tick": sim.tick, "channels": {}}
        for cname, ch in sim.channels.items():
            if only and cname not in only:
                continue
            e = ch.energy(sim.states[cname])
            e0 = sim._energy0.get(cname)
            drift = abs(e - e0) / abs(e0) if e0 else 0.0
            rec["channels"][cname] = {"energy": e, "rel_drift": drift}
        self.records.append(rec)

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {}
        out = {}
        for cname in self.records[-1]["channels"]:
            out[cname] = max(r["channels"][cname]["rel_drift"]
                             for r in self.records)
        return {"max_rel_drift": out}


@register_observer
class EnergyTrace(Observer):
    """Record per-channel energy over time (no drift normalisation)."""
    name = "energy_trace"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        self.records.append({
            "tick": sim.tick,
            "energy": {c: ch.energy(sim.states[c])
                       for c, ch in sim.channels.items()},
        })


@register_observer
class UnitarityResidual(Observer):
    """Max ||U†U − I|| over modes for channels that expose it (exact → 0)."""
    name = "unitarity_residual"
    exactness = "exact"

    def observe(self, sim) -> None:
        rec = {"tick": sim.tick, "channels": {}}
        for cname, ch in sim.channels.items():
            fn = getattr(ch, "unitarity_residual", None)
            if fn is not None:
                rec["channels"][cname] = float(fn(sim.lattice, sim.rng))
        if rec["channels"]:
            self.records.append(rec)


@register_observer
class DispersionFit(Observer):
    """Residual of measured vs analytic dispersion for channels exposing it."""
    name = "dispersion_fit"
    exactness = "machine-precision"

    def observe(self, sim) -> None:
        rec = {"tick": sim.tick, "channels": {}}
        for cname, ch in sim.channels.items():
            fn = getattr(ch, "dispersion_residual", None)
            if fn is not None:
                rec["channels"][cname] = float(fn(sim.lattice, sim.rng))
        if rec["channels"]:
            self.records.append(rec)


@register_observer
class FieldSnapshot(Observer):
    """Store a compact summary of each channel's state (norm + small slice)."""
    name = "field_snapshot"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        rec = {"tick": sim.tick, "channels": {}}
        for cname, ch in sim.channels.items():
            st = sim.states[cname]
            obs_fn = getattr(ch, "observables", None)
            entry: Dict[str, Any] = {"energy": ch.energy(st)}
            if obs_fn is not None:
                entry.update(obs_fn(st, sim.lattice))
            rec["channels"][cname] = entry
        self.records.append(rec)
