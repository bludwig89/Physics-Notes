"""casim.engine.core.channel — the Channel abstraction and registry.

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


def field_energy(E, B) -> float:
    """The engine's one gauge-field energy: :math:`U = \\tfrac12\\sum(E^2+B^2)`.

    **Roadmap P3.5 / blocker B4, decided 2026-07-31.**  The engine carried two
    conventions: ``coupled.field_energy`` had the ½ and the four ``channels.py``
    gauge channels did not, so ``PhotonPairChannel.energy`` was exactly twice
    ``WSourcedChannel.energy`` for the same field.  Nothing could sum them, and
    that — not the factor itself — is why B4 said *"nothing a coupled run could
    fail."*

    The ½ wins.  It is the physical field energy density, it is what
    ``gravity.T00_field_energy`` already sourced gravity from, and keeping the
    other convention would have made every engine-wide energy twice the value
    any GR or QED comparison expects.  The six channels that summed without the
    ½ now route through here and their reported energies **halve** — recorded as
    a supersession, not as drift, because the factor is exact and known.  No
    *registry-declared baseline* moves; 55 tracked result dumps do, by exactly
    2×, and only when re-run.

    Leading component/colour axes are summed, so a (3,L,L,L) photon and an
    (8,L,L,L) gluon both return a scalar in the same units.
    """
    E = np.asarray(E)
    B = np.asarray(B)
    return 0.5 * float(np.sum(E * E) + np.sum(B * B))


class Channel:
    """Base class for a field channel.

    Subclasses set ``type_name`` and ``propagator`` and implement
    ``init_state`` / ``step`` / ``energy``.  Optional hooks
    (``unitarity_residual``, ``dispersion_residual``, ``observables``) are used
    by the corresponding observers when present.
    """

    #: scenario key, e.g. "photon_pair"
    type_name: str = "channel"
    #: clean display name for GUI/CLI surfaces, e.g. "Photon Pair".  The
    #: ``type_name`` key stays the stable scenario/JSON identifier; ``label``
    #: is presentation only and never participates in registry lookups.
    label: str = ""
    #: F91 propagator class: "even" | "chiral" | "even+axial" | "per-branch" | "dielectric"
    propagator: str = "even"
    #: lattice topologies this channel supports
    topologies: tuple = ("cubic", "bcc")

    # --- clock (roadmap P3.2, blocker B2) -----------------------------------
    #: Physical time one ``step()`` call advances.  The default 1.0 says "one
    #: step is one CA tick", which is right for every spectral rotation law
    #: (F26/F67/F91) — their Δt is baked into the exponent.  A channel whose
    #: stepper takes a Δt argument overrides this, or reads it from a ``dt``
    #: config key, which :func:`casim.engine.core.clock.reconcile` picks up
    #: automatically.  ``None`` means **time-agnostic**: a compute-once solve, a
    #: projector, or a Monte-Carlo sweep — stepped once per tick, exempt from
    #: reconciliation.
    dt_native: float | None = 1.0
    #: CFL / stability ceiling on ``dt_native``.  ``None`` ⇒ unconstrained.  A
    #: scenario may lower this but never raise it.
    dt_max: float | None = None
    #: May the engine call ``step()`` more than once per tick?  ``False`` where
    #: repeated stepping changes the *meaning* rather than the resolution.
    subcyclable: bool = True

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

    @property
    def display_label(self) -> str:
        """Clean display name; falls back to ``type_name`` if unset."""
        return self.label or self.type_name

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type_name,
            "label": self.display_label,
            "propagator": self.propagator,
            "topologies": list(self.topologies),
        }

    # --- typed exchange bus (roadmap P3.3, blocker B3) ----------------------
    def provides(self) -> tuple:
        """Quantity names this channel publishes into the tick context.

        Default: the channel's own name, because every channel publishes its
        state under that key.  A channel that computes a named exchange
        quantity (``J_em``, ``J_colour``, ``T00``, ``A_mu``, ``sqrt_A``, …)
        should add it.
        """
        return (self.name,)

    def consumes(self) -> tuple:
        """Quantity names this channel reads out of the tick context.

        Derived by default from the ``sources``/``source``/``partner`` config
        keys the coupled channels already use, so most channels get a correct
        dependency edge with no change.  Override when a channel reads a
        partner by some other route.
        """
        cfg = self.config or {}
        out: list = []
        src = cfg.get("sources")
        if isinstance(src, dict):
            out.extend(str(k) for k in src)
        elif isinstance(src, (list, tuple)):
            out.extend(str(k) for k in src)
        elif isinstance(src, str):
            out.append(src)
        # ``couplings: {strong: gluon_field, em: photon_field, gravity: gmass}``
        # is how every particle channel names its partners.  Missing this key
        # was not a cosmetic gap: without it the particle→gauge edges vanish,
        # the genuine particle↔gauge *cycle* looks like a DAG, and the engine
        # would happily "topologically sort" a leapfrog into a lag.
        coup = cfg.get("couplings")
        if isinstance(coup, dict):
            out.extend(str(v) for v in coup.values() if isinstance(v, str))
        for key in ("source", "partner", "channel", "matter", "gauge"):
            v = cfg.get(key)
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, (list, tuple)):
                out.extend(str(x) for x in v)
        seen, uniq = set(), []
        for q in out:
            if q not in seen:
                seen.add(q)
                uniq.append(q)
        return tuple(uniq)

    # --- unified stress-energy (roadmap P3.4, blocker B5) -------------------
    def energy_density(self, state) -> "np.ndarray | None":
        """Additive energy density on the lattice, or ``None`` if undefined.

        This is **not** :meth:`energy`.  ``energy`` is the channel's conserved
        *drift probe* and is allowed to be a probability norm (spinor channels
        return Σ|ψ|², which is dimensionless).  ``energy_density`` is a genuine
        energy per cell in lattice units, in one convention across every
        channel, so the P3.5 ``TotalEnergy`` observer can sum it and the P3.4
        stress-energy protocol can source gravity from it.

        Default handles the two common layouts:

        * gauge ``(E, B)`` → :math:`u = \\tfrac12(E^2+B^2)`, summed over any
          leading component/colour axis.  This is the convention
          ``T00_field_energy`` already used;
        * spinor ``(f, g)`` / ``psi`` → ``mass`` × |ψ|², the F106-E5 rest leg.
          Returns ``None`` when the channel declares no mass, because a
          probability density is not an energy and guessing a conversion would
          be worse than reporting that the leg is missing.
        """
        from casim.engine.interactions.gravity import (
            T00_field_energy, T00_dirac_rest)
        if "E" in state and "B" in state:
            return T00_field_energy(state["E"], state["B"])
        mass = self.config.get("mass", self.config.get("m"))
        if mass is None:
            return None
        if "f" in state and "g" in state:
            return T00_dirac_rest(state["f"], state["g"], 0.0, 0.0, float(mass))
        if "psi" in state:
            return float(mass) * np.abs(np.asarray(state["psi"])) ** 2
        return None

    # --- gravity readback (roadmap P3.6, blocker B5 part 2) ----------------
    def gravity_partner(self):
        """Name of the ``gravity_dielectric`` channel this channel reads, or None.

        Accepts either ``gravity: <name>`` or the particle-style
        ``couplings: {gravity: <name>}``, so a gauge channel and a matter
        channel name their gravity partner the same way.
        """
        cfg = self.config or {}
        g = cfg.get("gravity")
        if isinstance(g, str):
            return g
        coup = cfg.get("couplings")
        if isinstance(coup, dict) and isinstance(coup.get("gravity"), str):
            return coup["gravity"]
        return None

    def read_K(self, context):
        """Local dielectric ``K(x)`` from the gravity partner, or ``None``.

        **Roadmap P3.6.**  Blocker B5 recorded that *no gauge channel reads
        K* — gravity was sourced by matter and read back by matter, but the
        gauge sector sat outside the loop entirely, so light did not bend in the
        production engine at all; deflection existed only in
        ``forks/gravity/gr_fork_F64_em_connection.py``.  This is the read side of
        that loop, available to every channel rather than to matter alone.

        Returns ``None`` — never an array of ones — when no partner is wired,
        the partner has not built ``K`` yet, or the field is exactly flat.  That
        keeps every no-gravity path bit-identical: a caller that gets ``None``
        takes the branch it always took.
        """
        name = self.gravity_partner()
        if not name or not context:
            return None
        gs = context.get(name)
        if not gs or "K" not in gs:
            return None
        K = np.asarray(gs["K"])
        if np.all(K == 1.0):
            return None
        return K

    def T_munu(self, state, lattice=None) -> Dict[str, "np.ndarray"]:
        """Stress-energy legs this channel contributes, keyed ``"00"``, ``"0i"``.

        The engine treats a missing key as "this channel does not source that
        leg", never as zero — an absent momentum density and a vanishing one are
        different claims and only one of them is checkable.  Default supplies
        ``"00"`` from :meth:`energy_density` and no ``"0i"``.
        """
        u = self.energy_density(state)
        return {} if u is None else {"00": u}

    def spec(self) -> Dict[str, Any]:
        """Round-trippable build spec: ``build_channel(ch.spec())`` rebuilds it."""
        return {"type": self.type_name, "name": self.name, **self.config}

    # --- block-spin RG hook (Phase 4, F133) ---------------------------------
    def block_spin(self, state, lattice, b: int):
        """Coarse-grain this channel's state under R_b (block factor ``b``).

        Default dispatches on the state layout via
        ``casim.engine.core.blockspin.block_state`` (even/chiral/dielectric (E,B)
        fields → component-wise block-average; (f,g) spinors → complex-safe
        block-average; gravity (φ,K) → block-average the linear φ, rebuild K).
        Channels with exotic state should override.
        """
        from .blockspin import block_state
        return block_state(state, b, self.propagator)

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

    def spinor_field(self, state):
        """Return ``(f, g)`` complex volumes for Bloch-sphere colouring, or None.

        The GUI's "spinor" colour mode uses this to colour points by orientation
        (helicity) and relative phase instead of density.  Default returns the
        ``f``/``g`` pair for spinor channels (e.g. ``weyl_bcc``) and ``None`` for
        channels with no 2-spinor state (gauge, dielectric, …), which the GUI
        falls back to density for.
        """
        if "f" in state and "g" in state:
            return np.asarray(state["f"]), np.asarray(state["g"])
        return None


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
