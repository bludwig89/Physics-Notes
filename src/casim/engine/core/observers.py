"""casim.engine.observers — diagnostics that run every N ticks.

Observers replace the inline diagnostics duplicated across the historical
``run_*`` scripts.  Each declares an ``exactness`` class (``"exact"`` |
``"machine-precision"`` | ``"quantitative"``) so a future pass can regenerate
``docs/status/exactness-inventory.md`` rather than maintain it by hand (roadmap Phase F).

An observer is called with the live ``Simulation`` and appends structured
records into ``sim.results["observers"][<observer-name>]``.
"""
from __future__ import annotations

from typing import Any, Dict, List
import numpy as np  # noqa: F401  (available to observer subclasses)


class Observer:
    name: str = "observer"
    #: clean display name for GUI/CLI surfaces, e.g. "Norm Conservation".
    #: ``name`` stays the stable scenario/JSON key; ``label`` is presentation only.
    label: str = ""
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

    @property
    def display_label(self) -> str:
        """Clean display name; falls back to ``name`` if unset."""
        return self.label or self.name

    def result(self) -> Dict[str, Any]:
        return {
            "type": self.name,
            "label": self.display_label,
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
    label = "Norm Conservation"
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
    label = "Energy Trace"
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
    label = "Unitarity Residual"
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
    label = "Dispersion Fit"
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
class BeamTrack(Observer):
    """Track a localized packet's energy centroid along its propagation axis.

    (2026-06-06) Built for ``photon_pair`` ``init: beam`` but works on any
    channel whose state holds real (E, B) arrays.  Per record: the circular
    (periodic-safe) energy centroid along ``axis`` and the rms axial spread.
    Summary: unwrapped centroid vs tick → measured beam speed, compared to the
    analytic finite-k group velocity dΩ_pair/dk|k0 and to c_lat = 1/√3.
    """
    name = "beam_track"
    label = "Beam Track"
    exactness = "quantitative"

    def observe(self, sim) -> None:
        cname = self.config.get("channel", "photon_pair")
        if cname not in sim.states:
            # allow referencing by type when a custom name was not set
            for n, ch in sim.channels.items():
                if ch.type_name == cname:
                    cname = n
                    break
        ch = sim.channels[cname]
        st = sim.states[cname]
        axis = ch.config.get("axis", self.config.get("axis", "x"))
        if axis in ("x", "y", "z"):
            axis = {"x": 0, "y": 1, "z": 2}[axis]
        axis = int(axis)
        E, B = np.asarray(st["E"]), np.asarray(st["B"])
        u = E ** 2 + B ** 2
        if u.ndim == 4:
            u = u.sum(axis=0)
        L = u.shape[axis]
        # axial energy profile, then circular centroid (periodic-safe)
        sum_axes = tuple(a for a in range(u.ndim) if a != axis)
        p = u.sum(axis=sum_axes)
        ptot = float(p.sum())
        theta = 2.0 * np.pi * np.arange(L) / L
        z = np.sum(p * np.exp(1j * theta)) / ptot
        centroid = (L / (2.0 * np.pi)) * float(np.angle(z)) % L
        # circular rms spread about the centroid
        d = np.remainder(np.arange(L) - centroid + L / 2.0, L) - L / 2.0
        spread = float(np.sqrt(np.sum(p * d ** 2) / ptot))
        self._meta = {"cname": cname, "axis": axis, "L": L,
                      "m_index": ch.config.get("m_index"),
                      "c_lat": float(getattr(sim.lattice, "c_lat", 0.0))}
        self.records.append({"tick": sim.tick,
                             "centroid": centroid,
                             "spread": spread,
                             "energy": ptot})

    def summary(self) -> Dict[str, Any]:
        if len(self.records) < 2 or not hasattr(self, "_meta"):
            return {}
        L = self._meta["L"]
        ticks = np.array([r["tick"] for r in self.records], float)
        cen = np.array([r["centroid"] for r in self.records], float)
        # unwrap across the periodic boundary
        d = np.diff(cen)
        d = np.remainder(d + L / 2.0, L) - L / 2.0
        unwrapped = np.concatenate([[cen[0]], cen[0] + np.cumsum(d)])
        v_meas = float(np.polyfit(ticks, unwrapped, 1)[0])
        out: Dict[str, Any] = {
            "channel": self._meta["cname"],
            "axis": self._meta["axis"],
            "speed_measured": v_meas,
            "c_lat": self._meta["c_lat"],
            "distance_travelled": float(unwrapped[-1] - unwrapped[0]),
            "spread_initial": self.records[0]["spread"],
            "spread_final": self.records[-1]["spread"],
        }
        m = self._meta.get("m_index")
        if m is not None:
            try:
                from casim.fields.photon import group_velocity_at
                k0vec = np.zeros(3)
                k0vec[self._meta["axis"]] = 2.0 * np.pi * float(m) / L
                nhat = np.zeros(3)
                nhat[self._meta["axis"]] = 1.0
                v_g = group_velocity_at(k0vec, nhat)
                out["speed_group_analytic"] = float(v_g)
                out["rel_error_vs_group"] = abs(v_meas - v_g) / abs(v_g)
            except Exception:  # pragma: no cover — analytic compare optional
                pass
        return out


@register_observer
class FieldSnapshot(Observer):
    """Store a compact summary of each channel's state (norm + small slice)."""
    name = "field_snapshot"
    label = "Field Snapshot"
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
