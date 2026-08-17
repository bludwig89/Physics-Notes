"""casim.engine.core.clock — the engine's physical clock (roadmap P3.2, blocker B2).

*Created 2026-07-31 - 22:10.*

Before this module the engine had a **tick counter, not a clock**.
``Simulation.step(n)`` took no ``dt``; each channel privately decided what "a
tick" meant by reading its own ``dt`` config key.  Nine such sites across seven
channel classes carried four different values (0.1, 0.2, 0.5, 1.0) and the
engine reconciled none of them, so in a scenario mixing them the channels
advanced *different amounts of physical time per engine tick* while being
coupled to each other through the shared context mapping.

Measured at construction time (2026-07-31): **18 of 46 shipped scenarios are
desynchronised**, and they include every flagship unified scenario —
``unified_hydrogen``, ``particles_first_gen``, ``proton_confined`` — in which a
``photon_sourced`` channel at ``dt=0.1`` is coupled to matter running at
``dt=1.0``.  The EM field in those runs advances **one tenth** of the physical
time its own source does, per tick.  See ``findings/F268-engine-clock-channel-desync.md``.

The model
---------
The engine owns one physical time step :math:`\\Delta t`.  Each channel declares
what *one call to* ``step()`` advances:

``dt_native``
    The physical time one ``step()`` call advances.  ``None`` means the channel
    is **time-agnostic** (a compute-once solve, a Monte-Carlo sweep, a
    projector) — it is stepped exactly once per engine tick and takes no part in
    reconciliation.

``dt_max``
    A CFL / stability ceiling on ``dt_native``.  Declaring ``dt_native >
    dt_max`` is a build-time error, not a run-time blow-up.

``subcyclable``
    Whether the engine may call ``step()`` more than once per tick.  ``False``
    for channels where repeated stepping changes the *meaning* rather than the
    resolution — a Monte-Carlo sweep resampling an ensemble, for instance.

Reconciliation.  :math:`\\Delta t` defaults to the **coarsest** declared
``dt_native`` (so it is a whole multiple of the finer ones) and each channel
sub-cycles :math:`n = \\Delta t / dt_\\text{native}` times per tick.  The ratio
is checked **exactly**, with :class:`fractions.Fraction` on the decimal
representation rather than a float tolerance, because 0.1 and 0.2 are not
binary-exact and a float division would leave 9.999999999999998.

Modes, and why the default is not ``strict``
--------------------------------------------
``strict``
    Sub-cycle.  This is the physically correct behaviour and the target state.

``legacy``
    Force :math:`n = 1` for every channel — the exact pre-P3.2 behaviour,
    bit-identical, so no committed baseline moves.  The reconciliation is still
    *computed and recorded*, so the desynchronisation is visible in results even
    when it is not corrected.

``auto`` (the default)
    ``strict`` when the scenario is already synchronous (every :math:`n = 1`,
    which is 28 of the 46 shipped scenarios), ``legacy`` otherwise.

The escape hatch is deliberate.  Switching the 18 desynchronised scenarios to
``strict`` is a *physics* change that moves their results by construction; it
wants its own session, a finding, and a supersession record — not a silent
rewrite smuggled in with an engine refactor.  What this module changes today is
that the desync is **declared, computed, and reported** instead of being an
emergent property of nine scattered config lookups.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence

__all__ = [
    "ClockError",
    "ChannelTiming",
    "Clock",
    "reconcile",
]


class ClockError(ValueError):
    """A scenario's channel timings cannot be reconciled onto one clock.

    Always raised at **build time** (``Simulation.__init__``), never mid-run:
    an unreconcilable clock is a scenario defect, and the roadmap's B3 lesson is
    that a defect which surfaces at tick 400 has already wasted the run.
    """


def _exact(x: float) -> Fraction:
    """Exact rational for a config float, via its decimal repr.

    ``Fraction(0.1)`` is 3602879701896397/36028797018963968 — the binary double
    — so ``Fraction(1.0) / Fraction(0.1)`` is *not* 10.  ``Fraction(str(0.1))``
    is 1/10 and the ratio is exactly 10.  Config ``dt`` values are written by
    humans in decimal, so the decimal reading is the intended one.
    """
    return Fraction(str(float(x)))


@dataclass(frozen=True)
class ChannelTiming:
    """One channel's resolved place on the engine clock."""

    name: str
    type_name: str
    #: physical time one ``step()`` call advances; None ⇒ time-agnostic
    dt_native: Optional[float]
    #: stability ceiling on ``dt_native``; None ⇒ unconstrained
    dt_max: Optional[float]
    #: may the engine call ``step()`` more than once per tick?
    subcyclable: bool
    #: resolved sub-cycles per engine tick
    n_sub: int
    #: physical time this channel actually advances per engine tick
    dt_effective: float
    #: True when ``n_sub`` was forced to 1 by ``legacy`` mode despite the
    #: reconciliation asking for more — i.e. this channel is running slow
    desynchronised: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type_name,
            "dt_native": self.dt_native,
            "dt_max": self.dt_max,
            "subcyclable": self.subcyclable,
            "n_sub": self.n_sub,
            "dt_effective": self.dt_effective,
            "desynchronised": self.desynchronised,
        }


@dataclass
class Clock:
    """The engine's physical time.

    ``tick`` counts engine ticks; ``time`` is the physical time elapsed,
    ``tick · dt``.  Both are checkpointed.  A channel never reads this object —
    it is handed its own ``n_sub`` by the engine — so the clock stays a property
    of the *engine*, which is the whole point of B2.
    """

    dt: float = 1.0
    mode: str = "auto"
    #: resolved mode after ``auto`` is decided
    resolved_mode: str = "strict"
    timings: Dict[str, ChannelTiming] = field(default_factory=dict)
    tick: int = 0

    @property
    def time(self) -> float:
        """Physical time elapsed: ``tick · dt``."""
        return self.tick * self.dt

    @property
    def synchronous(self) -> bool:
        """True when every channel advances the full ``dt`` each tick."""
        return not any(t.desynchronised for t in self.timings.values())

    def n_sub(self, channel_name: str) -> int:
        t = self.timings.get(channel_name)
        return t.n_sub if t is not None else 1

    def advance(self) -> None:
        self.tick += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dt": self.dt,
            "mode": self.mode,
            "resolved_mode": self.resolved_mode,
            "tick": self.tick,
            "time": self.time,
            "synchronous": self.synchronous,
            "channels": {n: t.to_dict() for n, t in self.timings.items()},
            "desynchronised": sorted(
                n for n, t in self.timings.items() if t.desynchronised),
        }

    # -- reporting -------------------------------------------------------
    def report(self) -> str:
        """One-line-per-channel human summary (CLI / GUI sidebar)."""
        lines = [f"clock  dt={self.dt:g}  mode={self.resolved_mode}"
                 f"  t={self.time:g}  ({'synchronous' if self.synchronous else 'DESYNCHRONISED'})"]
        for n, t in self.timings.items():
            tag = "  << running slow" if t.desynchronised else ""
            native = "agnostic" if t.dt_native is None else f"{t.dt_native:g}"
            lines.append(
                f"  {n:<24} dt_native={native:<9} n_sub={t.n_sub:<4}"
                f" dt_eff={t.dt_effective:g}{tag}")
        return "\n".join(lines)


# ----------------------------------------------------------------------
# Reconciliation
# ----------------------------------------------------------------------
def _channel_timing_spec(ch) -> tuple:
    """Read ``(dt_native, dt_max, subcyclable)`` off a channel.

    Config wins over the class attribute, so a scenario can retune a stepper
    without subclassing — but ``dt_max`` is a *stability* property of the rule
    and a config value may only ever lower it, never raise it.  Raising a CFL
    ceiling from YAML is exactly the kind of silent instability the roadmap's
    "typo → silent None" complaint is about.
    """
    cfg = getattr(ch, "config", {}) or {}

    dt_native = getattr(ch, "dt_native", None)
    if "dt" in cfg:
        dt_native = float(cfg["dt"])
    elif dt_native is not None:
        dt_native = float(dt_native)

    dt_max = getattr(ch, "dt_max", None)
    dt_max = None if dt_max is None else float(dt_max)
    if "dt_max" in cfg:
        want = float(cfg["dt_max"])
        if dt_max is not None and want > dt_max:
            raise ClockError(
                f"channel {ch.name!r} ({ch.type_name}): scenario dt_max={want:g} "
                f"exceeds the rule's stability ceiling {dt_max:g}. A config may "
                f"lower a CFL limit, never raise it.")
        dt_max = want

    subcyclable = bool(cfg.get("subcyclable", getattr(ch, "subcyclable", True)))
    return dt_native, dt_max, subcyclable


def reconcile(channels: Sequence, spec: Optional[Dict[str, Any]] = None) -> Clock:
    """Build a :class:`Clock` for ``channels`` from a scenario ``clock:`` block.

    ``spec`` keys: ``dt`` (force the global step) and ``mode``
    (``auto`` | ``strict`` | ``legacy``).

    Raises :class:`ClockError` — at build time — when a channel's ``dt_native``
    does not divide the global ``dt`` exactly, when a channel that forbids
    sub-cycling would need it, or when a declared step exceeds its own stability
    ceiling.
    """
    spec = dict(spec or {})
    mode = str(spec.get("mode", "auto")).lower()
    if mode not in ("auto", "strict", "legacy"):
        raise ClockError(
            f"clock mode must be 'auto', 'strict' or 'legacy', got {mode!r}")

    specs: List[tuple] = []
    for ch in channels:
        dt_native, dt_max, subcyclable = _channel_timing_spec(ch)
        if (dt_native is not None and dt_max is not None
                and dt_native > dt_max * (1.0 + 1e-12)):
            raise ClockError(
                f"channel {ch.name!r} ({ch.type_name}): dt_native={dt_native:g} "
                f"exceeds its stability ceiling dt_max={dt_max:g}")
        if dt_native is not None and dt_native <= 0.0:
            raise ClockError(
                f"channel {ch.name!r} ({ch.type_name}): dt_native must be > 0, "
                f"got {dt_native:g}")
        specs.append((ch, dt_native, dt_max, subcyclable))

    declared = [d for _, d, _, _ in specs if d is not None]

    # Global Δt: the scenario's choice, else the COARSEST declared native step.
    # Coarsest (not finest) because the finer channels must sub-cycle *up* to
    # the engine tick — n = Δt/dt_native — and that is only an integer if Δt is
    # the multiple. Taking the finest would make every coarse channel need a
    # fractional step, which no stepper can do.
    if "dt" in spec:
        dt = float(spec["dt"])
        if dt <= 0.0:
            raise ClockError(f"clock dt must be > 0, got {dt:g}")
    else:
        dt = max(declared) if declared else 1.0

    # Stability: Δt may not exceed any channel's ceiling.
    for ch, _dtn, dt_max, _sc in specs:
        if dt_max is not None and dt > dt_max * (1.0 + 1e-12):
            raise ClockError(
                f"global dt={dt:g} exceeds the stability ceiling dt_max="
                f"{dt_max:g} of channel {ch.name!r} ({ch.type_name}). Lower the "
                f"scenario's clock.dt, or let it default to the coarsest "
                f"dt_native.")

    dt_q = _exact(dt)
    timings: Dict[str, ChannelTiming] = {}
    wants_subcycling = False
    for ch, dt_native, dt_max, subcyclable in specs:
        if dt_native is None:                       # time-agnostic
            timings[ch.name] = ChannelTiming(
                ch.name, ch.type_name, None, dt_max, subcyclable, 1, dt)
            continue
        ratio = dt_q / _exact(dt_native)
        if ratio.denominator != 1:
            raise ClockError(
                f"channel {ch.name!r} ({ch.type_name}): dt_native="
                f"{dt_native:g} does not divide the global dt={dt:g} "
                f"(ratio {float(ratio):.12g}). A channel can only sub-cycle a "
                f"whole number of times per tick — pick a dt_native that "
                f"divides {dt:g}, or set clock.dt explicitly.")
        n = int(ratio)
        if n < 1:
            raise ClockError(
                f"channel {ch.name!r} ({ch.type_name}): dt_native="
                f"{dt_native:g} is coarser than the global dt={dt:g}; a channel "
                f"cannot advance more than one tick per tick.")
        if n > 1:
            wants_subcycling = True
            if not subcyclable:
                raise ClockError(
                    f"channel {ch.name!r} ({ch.type_name}) declares "
                    f"subcyclable=False but needs n_sub={n} to stay on the "
                    f"global dt={dt:g}. Either give it dt_native={dt:g}, or set "
                    f"clock.dt={dt_native:g} so the whole engine runs at its "
                    f"step.")
        timings[ch.name] = ChannelTiming(
            ch.name, ch.type_name, dt_native, dt_max, subcyclable, n, dt)

    resolved = mode
    if mode == "auto":
        resolved = "legacy" if wants_subcycling else "strict"

    if resolved == "legacy":
        # Force n_sub = 1 — bit-identical to pre-P3.2 — but *record* which
        # channels are therefore running slow, so the desync is an observable
        # rather than an emergent surprise.
        for name, t in list(timings.items()):
            if t.n_sub > 1:
                timings[name] = ChannelTiming(
                    t.name, t.type_name, t.dt_native, t.dt_max, t.subcyclable,
                    1, float(t.dt_native), desynchronised=True)

    return Clock(dt=dt, mode=mode, resolved_mode=resolved, timings=timings)
