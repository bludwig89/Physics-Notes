"""casim.gui.sidebar — per-particle / per-field readout panels (roadmap P3).

Pure and **headless-testable**: the sidebar data feed is built entirely from
each channel's audited ``observables()`` (plus its declared ``type_name`` /
``propagator`` class), so the live GUI readouts are guaranteed to *be* the
engine's own readouts — the P3 gate ("live readouts match ``observables()``").
``app.py`` renders ``sidebar_text`` into the Qt dock on the existing tick
callback; there is no physics or numerics in this module.

The split is by channel role, not by hard-coded names:

* **particles** — channels with ``type_name == "particle"`` (the typed
  ``ParticleChannel`` wavepackets).  Panel: norm, centroid position, velocity,
  exact charges, and each active force with its coupling-fidelity tier.
* **fields** — every other channel.  Panel: field energy, F91 propagator
  class, and any extra scalar readouts the channel publishes (e.g. the gravity
  dielectric's ``K_max`` / deflection, the sourced photon's ``alpha_max``).
"""
from __future__ import annotations

from typing import Any, Dict, List


def _is_particle(ch) -> bool:
    return getattr(ch, "type_name", None) == "particle"


def _channel_observables(sim, name, ch) -> Dict[str, Any]:
    """``ch.observables`` for the live state, or ``{}`` if it cannot render."""
    try:
        return dict(ch.observables(sim.states[name], sim.lattice))
    except Exception:                       # a channel may lack a readout
        return {}


def sidebar_model(sim) -> Dict[str, Any]:
    """Structured sidebar data ``{tick, particles:[...], fields:[...]}``.

    Every per-channel ``observables`` payload is taken verbatim from
    ``ch.observables(state, lattice)`` so the panel cannot drift from the
    engine's own readout.  Each entry also carries the channel's static
    ``type`` and F91 ``propagator`` class for the field panel header.
    """
    particles: List[Dict[str, Any]] = []
    fields: List[Dict[str, Any]] = []
    for name, ch in sim.channels.items():
        entry = {
            "name": name,
            "type": getattr(ch, "type_name", "?"),
            "propagator": getattr(ch, "propagator", "?"),
            "observables": _channel_observables(sim, name, ch),
        }
        (particles if _is_particle(ch) else fields).append(entry)
    return {"tick": int(sim.tick), "particles": particles, "fields": fields}


# ----------------------------------------------------------------------
# Text rendering (what the Qt dock label shows)
# ----------------------------------------------------------------------
def _fmt_vec(v, p=2) -> str:
    try:
        return "[" + ", ".join(f"{float(x):.{p}f}" for x in v) + "]"
    except Exception:
        return str(v)


def _fmt_charges(charges) -> str:
    """One ``Q/T3/Y`` line per Weyl member of a particle (doublets list two)."""
    out = []
    for c in charges:
        q = c.get("Q"); t3 = c.get("T3"); y = c.get("Y")
        tag = c.get("name", "")
        bits = f"Q={q} T3={t3} Y={y}"
        if c.get("colour"):
            bits += " colour"
        out.append(f"{tag}: {bits}" if tag else bits)
    return "; ".join(out)


def _particle_lines(p) -> List[str]:
    o = p["observables"]
    lines = [f"● {p['name']}  ({o.get('species', p['type'])})"]
    if "norm" in o:
        lines.append(f"    norm     {o['norm']:.5g}")
    if "centroid" in o:
        lines.append(f"    pos      {_fmt_vec(o['centroid'])}")
    if "velocity_per_tick" in o:
        lines.append(f"    vel/tick {_fmt_vec(o['velocity_per_tick'], 3)}")
    if "charges" in o:
        lines.append(f"    charges  {_fmt_charges(o['charges'])}")
    if o.get("couplings"):
        forces = ", ".join(f"{f}:{d['tier']}→{d['partner']}"
                           for f, d in o["couplings"].items())
        lines.append(f"    forces   {forces}")
    if "grav_K_centroid" in o:
        lines.append(f"    gravity  K={o['grav_K_centroid']:.4g} "
                     f"φ={o.get('grav_potential', 0.0):.3g}")
    return lines


def _field_lines(fld) -> List[str]:
    o = fld["observables"]
    lines = [f"▢ {fld['name']}  [{fld['type']} · {fld['propagator']}]"]
    if "field_energy" in o:
        lines.append(f"    energy   {o['field_energy']:.5g}")
    if "alpha_max" in o:
        lines.append(f"    α_max    {o['alpha_max']:.3g}")
    if "K_max" in o:
        lines.append(f"    K_max    {o['K_max']:.5g}")
    if "deflection_measured" in o:
        lines.append(f"    bend     {o['deflection_measured']:.4g} "
                     f"(GR {o.get('deflection_GR_finite_aperture', float('nan')):.4g})")
    return lines


def sidebar_text(sim) -> str:
    """Human-readable sidebar block for the Qt dock (and for tests)."""
    m = sidebar_model(sim)
    out: List[str] = [f"tick {m['tick']}"]
    if m["particles"]:
        out.append("— particles —")
        for p in m["particles"]:
            out.extend(_particle_lines(p))
    if m["fields"]:
        out.append("— fields —")
        for fld in m["fields"]:
            out.extend(_field_lines(fld))
    return "\n".join(out)
