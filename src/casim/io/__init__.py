"""casim.io — scenario loading and result writing.

A scenario is a YAML file; one driver + a committed config + seed reproduces a
historical run.  Results are written as JSON into ``test-results/`` (the schema
the repository already uses).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict

import yaml


def load_scenario(path: str) -> Dict[str, Any]:
    """Load and lightly validate a scenario YAML file."""
    with open(path, "r") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"scenario {path!r} did not parse to a mapping")
    data.setdefault("name", os.path.splitext(os.path.basename(path))[0])
    data.setdefault("channels", [])
    data.setdefault("observers", [])
    data.setdefault("seed", 0)
    data.setdefault("ticks", 0)
    if not data["channels"]:
        raise ValueError(f"scenario {path!r} declares no channels")
    return data


def dump_scenario(scenario: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as fh:
        yaml.safe_dump(scenario, fh, sort_keys=False)


def write_results(results: Dict[str, Any], path: str) -> str:
    """Write a results dict to JSON, creating parent directories."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    return os.path.abspath(path)


def read_results(path: str) -> Dict[str, Any]:
    with open(path, "r") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------
# Checkpoint export (NPZ → compact JSON Claude can read)
# ----------------------------------------------------------------------
def _array_stats(a) -> Dict[str, Any]:
    """Compact summary of one state array — never the raw values."""
    import numpy as np
    a = np.asarray(a)
    out: Dict[str, Any] = {"shape": list(a.shape), "dtype": str(a.dtype)}
    if a.size == 0:
        return out
    if np.iscomplexobj(a):
        mag = np.abs(a)
        out.update(abs_max=float(mag.max()), abs_mean=float(mag.mean()),
                   l2=float(np.sqrt(np.sum(mag ** 2))))
    else:
        out.update(min=float(a.min()), max=float(a.max()),
                   mean=float(a.mean()), l2=float(np.sqrt(np.sum(a ** 2))))
    return out


def export_checkpoint(checkpoint: str, out: str | None = None,
                      stride: int = 1) -> str:
    """Resume a checkpoint and write a compact, human/Claude-readable JSON.

    Includes: run meta (name, tick, lattice, seed), the restored observer
    time series (every ``stride``-th record), and per-channel summaries —
    ``describe()``, conserved energy + drift-from-tick-0, the channel's
    ``observables()`` if it exposes them, and compact stats of each state
    array (shape/min/max/mean/L2).  Raw arrays are *not* dumped.
    """
    from casim.engine import Simulation   # local import: avoids io→engine cycle
    sim = Simulation.resume(checkpoint)
    channels: Dict[str, Any] = {}
    for cname, ch in sim.channels.items():
        st = sim.states[cname]
        e = ch.energy(st)
        e0 = sim._energy0.get(cname)
        entry: Dict[str, Any] = {
            **ch.describe(),
            "energy": e,
            "energy0": e0,
            "rel_drift": (abs(e - e0) / abs(e0)) if e0 else None,
        }
        obs_fn = getattr(ch, "observables", None)
        if obs_fn is not None:
            try:
                entry["observables"] = obs_fn(st, sim.lattice)
            except Exception as exc:           # pragma: no cover
                entry["observables_error"] = repr(exc)
        entry["state_arrays"] = {
            k: _array_stats(v) for k, v in st.items()
            if hasattr(v, "shape")
        }
        channels[cname] = entry

    observers: Dict[str, Any] = {}
    for obs in sim.observers:
        recs = obs.records[::stride] if stride > 1 else obs.records
        observers[obs.name] = {
            "exactness": obs.exactness,
            "every": obs.every,
            "n_records": len(obs.records),
            "stride": stride,
            "records": recs,
            "summary": obs.summary(),
        }

    payload = {
        "source_checkpoint": os.path.abspath(checkpoint),
        "name": sim.name,
        "tick": sim.tick,
        "target_ticks": sim.target_ticks,
        "seed": sim.seed,
        "lattice": sim.lattice.to_dict(),
        "channels": channels,
        "observers": observers,
    }
    if out is None:
        base = os.path.splitext(os.path.basename(checkpoint))[0]
        out = os.path.join("test-results", f"export_{base}.json")
    return write_results(payload, out)


__all__ = [
    "load_scenario", "dump_scenario",
    "write_results", "read_results", "export_checkpoint",
]
