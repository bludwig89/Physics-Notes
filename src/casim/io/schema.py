"""casim.io.schema — the strict scenario schema (v2). Roadmap P4.

Before this module, ``load_scenario`` validated exactly two things: that the
file parsed to a mapping and that ``channels`` was non-empty.  A misspelled key
(``withd: 1.5`` for ``width``) was silently ignored, and a coupling target that
named no channel became a silent ``None`` at tick 400.  This module is the
"error at load, not at tick 400" half of P4.

Two design rules, both inherited from the engine's own graph (F269):

  * **Unknown keys are errors, not comments.** The whole point of a schema is
    that a typo cannot be a no-op.  Every block below declares its allowed keys,
    and an unlisted key is reported with the block it appeared in.
  * **Channel/observer *parameters* are NOT whitelisted.** A channel type owns
    its own parameter names (``sigma``, ``eps_strong``, ``coulomb`` …) and the
    schema layer must not maintain a copy of that list — that is exactly the
    curated-key-list mistake ``casim.engine.core.graph._config_channel_refs``
    documents.  So a channel entry is checked for a *registered* ``type`` and
    for the typed fields the engine reads structurally (``name``, ``seed``),
    and its remaining keys are passed through untouched.

Versioning.  A scenario with ``version: 2`` is validated strictly and a failure
raises :class:`ScenarioError`.  A scenario with no ``version`` is treated as v1:
it still loads (one deprecation cycle, per P4) and only the always-true
structural checks apply.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

SCHEMA_VERSION = 2

# ----------------------------------------------------------------------
# Allowed keys, by block.  A value of ``None`` means "any scalar/structure";
# a type or tuple of types means "must be an instance of".
# ----------------------------------------------------------------------
_TOP_KEYS: Dict[str, Any] = {
    "version": int,
    "name": str,
    "title": str,
    "description": str,
    "lattice": dict,
    "seed": int,
    "ticks": int,
    "channels": list,
    "observers": list,
    "output": dict,
    "checkpoint": dict,
    "clock": dict,          # P3.2 engine clock spec
    "bus": dict,            # P3.3 exchange-bus spec (cycle_scheme, strict)
    "blockspin": None,      # legacy tick->factor schedule (kept; see events)
    # --- P4 additions ---
    "units": dict,
    "events": list,
    "expect": dict,
    "boundaries": dict,
    "view": dict,
    "extends": (str, list),
    "sweep": dict,
    "compute": dict,
}

_LATTICE_KEYS: Dict[str, Any] = {
    "L": int,
    "dims": int,
    "topology": str,
    "c_lat": (int, float),
    "physical_patch": int,
    "block": int,
}

_OUTPUT_KEYS = {"json": str, "dir": str, "figures": str}
_CHECKPOINT_KEYS = {"every": int, "dir": str}
_CLOCK_KEYS = {"dt": (int, float), "scheme": str, "strict": bool}
_BUS_KEYS = {"cycle_scheme": str, "strict": bool}
_UNITS_KEYS = {"cell_m": (int, float), "tick_s": (int, float),
               "mass_kg": (int, float), "energy_eV": (int, float),
               "anchor": str}
_EXPECT_KEYS = {"exactness": str, "tol": (int, float), "gates": list}
_BOUND_KEYS = {"type": str, "x": str, "y": str, "z": str, "region": dict}
_VIEW_KEYS = {"camera": dict, "channels": list, "colour_mode": str,
              "color_mode": str, "slice": dict, "steps_per_frame": int,
              "threshold": (int, float)}
_COMPUTE_KEYS = {"dtype": str, "device": str, "threads": int,
                 "backend": str, "mem_gb": (int, float),
                 "allow_float32": bool}
_SWEEP_KEYS = {"params": dict, "seeds": list}
_EVENT_KEYS = {"at": int, "every": int, "do": str, "channel": str,
               "factor": int, "value": None, "params": dict}

_EXACTNESS_VOCAB = {"exact", "machine", "quantitative", "bracketed",
                    "external"}
_TOPOLOGY_VOCAB = {"cubic", "square", "bcc"}
_EVENT_ACTIONS = {"blockspin", "inject", "pulse", "measure", "ramp",
                  "checkpoint", "set"}
_CYCLE_SCHEMES = {"gauss_seidel", "jacobi"}


class ScenarioError(ValueError):
    """A scenario failed strict (v2) schema validation."""


# ----------------------------------------------------------------------
def _check_keys(block: Any, allowed: Dict[str, Any], where: str,
                errs: List[str]) -> None:
    if not isinstance(block, dict):
        errs.append(f"{where}: expected a mapping, got {type(block).__name__}")
        return
    for k, v in block.items():
        if k not in allowed:
            near = _suggest(k, allowed)
            hint = f" (did you mean {near!r}?)" if near else ""
            errs.append(f"{where}: unknown key {k!r}{hint}. "
                        f"allowed: {sorted(allowed)}")
            continue
        exp = allowed[k]
        if exp is not None and not isinstance(v, exp):
            names = (exp.__name__ if isinstance(exp, type)
                     else "/".join(t.__name__ for t in exp))
            errs.append(f"{where}.{k}: expected {names}, "
                        f"got {type(v).__name__}")


def _suggest(key: str, allowed: Dict[str, Any]) -> Optional[str]:
    """Cheap edit-distance-1 typo suggestion, no dependency."""
    key = key.lower()
    best = None
    for cand in allowed:
        c = cand.lower()
        if abs(len(c) - len(key)) > 2:
            continue
        # shared-prefix + length proximity is enough for 'withd'->'width'
        common = sum(1 for a, b in zip(sorted(c), sorted(key)) if a == b)
        if common >= max(len(c), len(key)) - 2:
            best = cand
    return best


def _channel_names(data: Dict[str, Any]) -> List[str]:
    names: List[str] = []
    for i, c in enumerate(data.get("channels") or []):
        if isinstance(c, dict):
            names.append(str(c.get("name", c.get("type", f"ch{i}"))))
    return names


def _registered_types():
    """Return (channel_types, observer_types) or (None, None) if the engine
    cannot be imported (e.g. schema used stand-alone in a tool)."""
    try:
        from casim.engine import registered_channels, registered_observers
        return set(registered_channels()), set(registered_observers())
    except Exception:       # pragma: no cover - engine optional at validate time
        return None, None


# ----------------------------------------------------------------------
def validate(data: Any, path: Optional[str] = None) -> List[str]:
    """Validate a parsed scenario mapping against the v2 schema.

    Returns a list of human-readable error strings (empty == valid).  Does not
    raise; :func:`validate_strict` is the raising wrapper.  Channel/observer
    *parameters* are intentionally not whitelisted (see module docstring); their
    cross-references, however, are checked.
    """
    where = f"scenario {path!r}" if path else "scenario"
    errs: List[str] = []
    if not isinstance(data, dict):
        return [f"{where}: did not parse to a mapping"]

    _check_keys(data, _TOP_KEYS, where, errs)

    lat = data.get("lattice")
    if lat is not None:
        _check_keys(lat, _LATTICE_KEYS, f"{where}.lattice", errs)
        topo = lat.get("topology")
        if isinstance(topo, str) and topo not in _TOPOLOGY_VOCAB:
            errs.append(f"{where}.lattice.topology: {topo!r} is not one of "
                        f"{sorted(_TOPOLOGY_VOCAB)}")
        if "physical_patch" in lat and "block" in lat:
            pp, bl = lat.get("physical_patch"), lat.get("block")
            if isinstance(pp, int) and isinstance(bl, int) and bl and pp % bl:
                errs.append(f"{where}.lattice: physical_patch={pp} is not "
                            f"divisible by block={bl}")

    for name, keys in (("output", _OUTPUT_KEYS), ("checkpoint", _CHECKPOINT_KEYS),
                       ("clock", _CLOCK_KEYS), ("bus", _BUS_KEYS),
                       ("units", _UNITS_KEYS), ("compute", _COMPUTE_KEYS),
                       ("sweep", _SWEEP_KEYS), ("view", _VIEW_KEYS),
                       ("boundaries", _BOUND_KEYS)):
        blk = data.get(name)
        if blk is not None:
            _check_keys(blk, keys, f"{where}.{name}", errs)

    _validate_expect(data.get("expect"), f"{where}.expect", errs)
    _validate_compute(data.get("compute"), f"{where}.compute", errs)
    _validate_bus(data.get("bus"), f"{where}.bus", errs)

    ch_types, ob_types = _registered_types()
    names = _channel_names(data)
    nameset = set(names)

    # channels
    channels = data.get("channels")
    if not channels:
        errs.append(f"{where}: declares no channels")
    elif not isinstance(channels, list):
        errs.append(f"{where}.channels: expected a list")
    else:
        for i, c in enumerate(channels):
            tag = f"{where}.channels[{i}]"
            if not isinstance(c, dict):
                errs.append(f"{tag}: expected a mapping")
                continue
            t = c.get("type")
            if not t:
                errs.append(f"{tag}: missing required 'type'")
            elif ch_types is not None and t not in ch_types:
                errs.append(f"{tag}: unknown channel type {t!r}. "
                            f"`casim list-channels` shows the registry")
            if "seed" in c and not isinstance(c["seed"], int):
                errs.append(f"{tag}.seed: expected int (per-channel RNG seed)")
            _validate_sources(c.get("sources"), nameset, tag, errs)

    # observers reference channels by name; a dangling ref is a typo.
    observers = data.get("observers")
    if observers is not None and not isinstance(observers, list):
        errs.append(f"{where}.observers: expected a list")
    elif observers:
        for i, o in enumerate(observers):
            tag = f"{where}.observers[{i}]"
            if not isinstance(o, dict):
                errs.append(f"{tag}: expected a mapping")
                continue
            t = o.get("type")
            if not t:
                errs.append(f"{tag}: missing required 'type'")
            elif ob_types is not None and t not in ob_types:
                errs.append(f"{tag}: unknown observer type {t!r}")
            if "every" in o and not (isinstance(o["every"], int)
                                     and o["every"] >= 1):
                errs.append(f"{tag}.every: expected a positive int")
            _validate_obs_refs(o, nameset, tag, errs)

    _validate_events(data.get("events"), nameset, f"{where}.events", errs)
    return errs


def _validate_sources(sources, nameset, tag, errs) -> None:
    # ``sources`` is either a list of channel names, or a weighted mapping
    # {channel_name: weight} (e.g. gravity_dielectric's self-sourcing).
    if sources is None:
        return
    if isinstance(sources, dict):
        refs = list(sources.keys())
    elif isinstance(sources, list):
        refs = sources
    else:
        errs.append(f"{tag}.sources: expected a list of channel names or a "
                    f"{{channel: weight}} mapping")
        return
    for s in refs:
        if isinstance(s, str) and s not in nameset:
            errs.append(f"{tag}.sources: {s!r} names no channel in this "
                        f"scenario. channels: {sorted(nameset)}")


def _validate_obs_refs(o, nameset, tag, errs) -> None:
    # Observers point at channels via several keys; each value that is a string
    # or list-of-strings must name a channel.
    for key in ("channels", "channel", "cluster", "electron", "gluon",
                "photon"):
        if key not in o:
            continue
        val = o[key]
        refs = val if isinstance(val, list) else [val]
        for r in refs:
            if isinstance(r, str) and r not in nameset:
                errs.append(f"{tag}.{key}: {r!r} names no channel. "
                            f"channels: {sorted(nameset)}")


def _validate_events(events, nameset, where, errs) -> None:
    if events is None:
        return
    if not isinstance(events, list):
        errs.append(f"{where}: expected a list of event mappings")
        return
    for i, ev in enumerate(events):
        tag = f"{where}[{i}]"
        if not isinstance(ev, dict):
            errs.append(f"{tag}: expected a mapping")
            continue
        _check_keys(ev, _EVENT_KEYS, tag, errs)
        if "at" not in ev and "every" not in ev:
            errs.append(f"{tag}: an event needs 'at' (a tick) or 'every'")
        do = ev.get("do")
        if not do:
            errs.append(f"{tag}: missing required 'do' (the action)")
        elif do not in _EVENT_ACTIONS:
            errs.append(f"{tag}.do: {do!r} is not one of "
                        f"{sorted(_EVENT_ACTIONS)}")
        ch = ev.get("channel")
        if isinstance(ch, str) and ch not in nameset:
            errs.append(f"{tag}.channel: {ch!r} names no channel")


def _validate_expect(expect, where, errs) -> None:
    if expect is None:
        return
    _check_keys(expect, _EXPECT_KEYS, where, errs)
    ex = expect.get("exactness")
    if isinstance(ex, str) and ex not in _EXACTNESS_VOCAB:
        errs.append(f"{where}.exactness: {ex!r} is not one of "
                    f"{sorted(_EXACTNESS_VOCAB)}")
    gates = expect.get("gates")
    if gates is not None and not isinstance(gates, list):
        errs.append(f"{where}.gates: expected a list")


def _validate_compute(compute, where, errs) -> None:
    if compute is None:
        return
    dtype = compute.get("dtype")
    if isinstance(dtype, str) and dtype not in ("complex128", "float64"):
        if dtype in ("complex64", "float32"):
            if not compute.get("allow_float32"):
                errs.append(
                    f"{where}.dtype: {dtype!r} is below the 1e-12 gate. "
                    f"Set compute.allow_float32: true to opt in explicitly "
                    f"(this mirrors CASIM_ALLOW_FLOAT32).")
        else:
            errs.append(f"{where}.dtype: {dtype!r} unrecognised "
                        f"(complex128 | float64 | complex64 | float32)")


def _validate_bus(bus, where, errs) -> None:
    if bus is None:
        return
    scheme = bus.get("cycle_scheme")
    if isinstance(scheme, str) and scheme not in _CYCLE_SCHEMES:
        errs.append(f"{where}.cycle_scheme: {scheme!r} is not one of "
                    f"{sorted(_CYCLE_SCHEMES)}")


def validate_strict(data: Any, path: Optional[str] = None) -> None:
    """Validate and raise :class:`ScenarioError` on the first block of errors."""
    errs = validate(data, path)
    if errs:
        head = f"scenario {path!r} failed v2 validation" if path \
            else "scenario failed v2 validation"
        raise ScenarioError(head + ":\n  - " + "\n  - ".join(errs))


__all__ = ["SCHEMA_VERSION", "ScenarioError", "validate", "validate_strict"]
