"""casim.engine.channel — the Channel abstraction and registry.

A *channel* is one field sector evolving on the lattice.  Each channel owns its
own state representation (real-space arrays, k-space arrays, or anything else —
the engine never inspects it) and exposes a uniform interface so the
``Simulation`` can advance and measure it without knowing the physics.

The registry maps a channel ``type`` string (used in scenario YAML) onto a
concrete class, and records the F91 propagator classification
(``"even" | "chiral" | ...``) so the branch structure is an explicit,
inspectable program property (``casim list-channels``).
"""
from __future__ import annotations

from typing import Any, Dict, Type
import numpy as np


class Channel:
    """Base class for a field channel.

    Subclasses set ``type_name`` and ``propagator`` and implement
    ``init_state`` / ``step`` / ``energy``.  Optional hooks
    (``unitarity_residual``, ``dispersion_residual``, ``observables``) are used
    by the corresponding observers when present.
    """

    #: scenario key, e.g. "photon_pair"
    type_name: str = "channel"
    #: F91 propagator class: "even" | "chiral" | "even+axial" | "per-branch" | "dielectric"
    propagator: str = "even"
    #: lattice topologies this channel supports
    topologies: tuple = ("cubic", "bcc")

    def __init__(self, name: str | None = None, **config: Any):
        self.name = name or self.type_name
        self.config = dict(config)

    # --- required interface -------------------------------------------------
    def init_state(self, lattice, rng: np.random.Generator):
        """Return the initial channel state for ``lattice``."""
        raise NotImplementedError

    def step(self, state, lattice, context=None, rng=None):
        """Advance ``state`` by one CA tick; return the new state.

        ``context`` (Tier-2 coupling) is the engine's live mapping of
        ``{channel_name: state}``.  Within a tick the engine steps channels in
        registration order and updates the mapping in place, so a channel sees
        the *already-updated* states of channels registered before it and the
        *pre-tick* states of those after it.  A coupled channel (e.g. a gauge
        field sourced by a matter current) reads its partner's state from here.

        ``rng`` is the engine's ``numpy.random.Generator`` (its state is
        checkpointed), passed so stochastic / non-unitary channels (e.g. a
        Monte-Carlo gauge sweep) draw reproducibly.  Deterministic channels
        ignore both ``context`` and ``rng`` and stay bit-identical.
        """
        raise NotImplementedError

    def energy(self, state) -> float:
        """Return a conserved positive scalar (norm / field energy)."""
        raise NotImplementedError

    # --- optional hooks (used by observers when defined) --------------------
    # def unitarity_residual(self, lattice) -> float: ...
    # def dispersion_residual(self, lattice, rng) -> float: ...
    # def observables(self, state, lattice) -> dict: ...

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type_name,
            "propagator": self.propagator,
            "topologies": list(self.topologies),
        }

    def spec(self) -> Dict[str, Any]:
        """Round-trippable build spec: ``build_channel(ch.spec())`` rebuilds it."""
        return {"type": self.type_name, "name": self.name, **self.config}

    def density_field(self, state) -> "np.ndarray":
        """Return a 3-D real scalar volume for visualisation (GUI point cloud).

        Default handles the common state layouts: spinor (``f``/``g``),
        gauge (``E``/``B`` as (L,L,L) or (C,L,L,L)), and dielectric (``K``).
        Channels with exotic state should override.
        """
        if "f" in state and "g" in state:
            d = np.abs(state["f"]) ** 2 + np.abs(state["g"]) ** 2
            return np.asarray(d.real if np.iscomplexobj(d) else d)
        if "E" in state and "B" in state:
            E, B = np.asarray(state["E"]), np.asarray(state["B"])
            d = E ** 2 + B ** 2
            if d.ndim == 4:        # (components, L, L, L) → sum over components
                d = d.sum(axis=0)
            return np.asarray(d.real if np.iscomplexobj(d) else d)
        if "K" in state:
            return np.asarray(state["K"]) - 1.0
        for v in state.values():   # fallback: first ndarray
            if isinstance(v, np.ndarray):
                a = np.abs(v) ** 2
                return a.sum(axis=0) if a.ndim == 4 else a
        raise ValueError("no renderable array in channel state")


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------
_REGISTRY: Dict[str, Type[Channel]] = {}


def register(cls: Type[Channel]) -> Type[Channel]:
    """Class decorator: register a channel under its ``type_name``."""
    key = cls.type_name
    if key in _REGISTRY and _REGISTRY[key] is not cls:
        raise ValueError(f"channel type {key!r} already registered")
    _REGISTRY[key] = cls
    return cls


def get_channel_class(type_name: str) -> Type[Channel]:
    try:
        return _REGISTRY[type_name]
    except KeyError:
        raise KeyError(
            f"unknown channel type {type_name!r}; "
            f"registered: {sorted(_REGISTRY)}"
        )


def build_channel(spec: Dict[str, Any]) -> Channel:
    """Build a channel instance from a scenario dict ``{type:, name?:, ...}``."""
    spec = dict(spec)
    type_name = spec.pop("type")
    name = spec.pop("name", None)
    cls = get_channel_class(type_name)
    return cls(name=name, **spec)


def registered_channels() -> Dict[str, Type[Channel]]:
    return dict(_REGISTRY)
