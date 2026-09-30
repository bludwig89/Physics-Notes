"""casim.engine.core.observers — diagnostics that run every N ticks.

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
class TotalEnergy(Observer):
    """Global energy of the whole run — roadmap **P3.5**, blocker **B4**.

    *Added 2026-07-31 - 22:55.*

    The roadmap calls this "the single most important deliverable" and the
    reason is one sentence: **without it a unified run produces pictures nobody
    can falsify.**  Every other observer measures one channel; a coupled run's
    only global claim is that energy moves *between* channels without being
    created, and nothing in the engine could state that, let alone check it.

    What is summed, and what deliberately is not
    --------------------------------------------
    Each channel is asked for
    :meth:`~casim.engine.core.channel.Channel.energy_density` — a genuine energy
    per cell in one convention (:math:`\\tfrac12(E^2+B^2)` for gauge, the
    F106-E5 rest leg :math:`m|\\Psi|^2` for matter).  That is **not** the same
    question as :meth:`~casim.engine.core.channel.Channel.energy`, which is a
    conserved *drift probe* and for spinor channels returns a dimensionless
    probability norm.  Summing norms and energies was the deeper half of B4 and
    unifying the ½ alone would not have fixed it.

    A channel that cannot express an energy density — a massless matter packet
    with no declared mass, a Monte-Carlo sweep — returns ``None`` and is listed
    under ``missing``.  It is **not** counted as zero.  An absent leg and a
    vanishing leg are different claims and only one of them is checkable; a
    total silently missing a term is worse than no total, because it looks
    conserved.  ``covered`` therefore reports the fraction of channels actually
    in the sum, and ``strict: true`` turns any missing leg into a hard failure
    for scenarios that claim full coverage.

    Summary fields
    --------------
    ``max_rel_drift``
        max |E(t) − E(0)| / |E(0)| over the run — the number the P3 acceptance
        gate reads ("conserving total energy to the machine-precision class over
        ≥ 10³ ticks").
    ``exactness_class``
        ``machine`` (< 1e-12), ``tight`` (< 1e-9), ``quantitative`` otherwise.
        Named rather than left to the reader, so a regression is visible as a
        class change and not only as a digit.
    ``covered`` / ``missing``
        How much of the run the total actually accounts for.
    """
    name = "total_energy"
    label = "Total Energy"
    exactness = "machine-precision"

    def observe(self, sim) -> None:
        only = self.config.get("channels")
        total = 0.0
        per: Dict[str, float] = {}
        missing: List[str] = []
        for cname, ch in sim.channels.items():
            if only and cname not in only:
                continue
            try:
                u = ch.energy_density(sim.states[cname])
            except Exception:
                u = None
            if u is None:
                missing.append(cname)
                continue
            e = float(np.sum(np.asarray(u).real))
            per[cname] = e
            total += e
        rec = {
            "tick": sim.tick,
            "time": float(getattr(sim, "clock", None).time)
                    if getattr(sim, "clock", None) is not None else float(sim.tick),
            "total": total,
            "channels": per,
            "missing": missing,
        }
        self.records.append(rec)

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {}
        e0 = self.records[0]["total"]
        drift = max(abs(r["total"] - e0) / abs(e0) for r in self.records) \
            if e0 else 0.0
        cls = ("machine" if drift < 1e-12
               else "tight" if drift < 1e-9
               else "quantitative")
        last = self.records[-1]
        n_cov = len(last["channels"])
        n_all = n_cov + len(last["missing"])
        out = {
            "E0": e0,
            "E_final": last["total"],
            "max_rel_drift": drift,
            "exactness_class": cls,
            "covered": f"{n_cov}/{n_all}",
            "missing": last["missing"],
        }
        if self.config.get("strict") and last["missing"]:
            out["strict_violation"] = (
                f"strict total energy asked for, but {len(last['missing'])} "
                f"channel(s) contribute no energy density: {last['missing']}")
        return out


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
class Momentum(Observer):
    """Matter and field momentum — Stage 0 of the photon-fermion coupling
    roadmap (``docs/roadmaps/photon-fermion-coupling.md``).

    Built because §1.5 of that roadmap found *no* momentum observable existed
    anywhere in the engine, so a recoil could not be seen even where the
    physics to produce one existed.  Two independent constructions, one per
    kind of channel a state dict can hold:

    ``P_matter`` — spectral, exact.  For every complex spinor-like array the
    channel's state exposes (``f``/``g``, or an isospin doublet's
    ``f_nu``/``f_e``/``g_nu``/``g_e``, or a Dirac quartet's
    ``eta_u``/``eta_d``/``chi_u``/``chi_d``), ``Σ_k k · |ψ̃(k)|² / N``.  This
    is ``⟨ψ|-i∇|ψ⟩`` — the Noether charge of the lattice's own translation
    symmetry.  It needs no reference to *which* kinetic operator is applied to
    the field: any complex field on a periodic lattice has this momentum,
    exactly, and it is invariant under *any* purely-diagonal-in-k propagator
    (the free BCC Weyl step among them) because such a step only ever
    multiplies each mode by a phase-preserving unitary, leaving |ψ̃(k)|²
    untouched mode-by-mode. A propagator that mixes k-modes (e.g. a
    position-space gauge rotation applied before the spectral step) has no
    such guarantee, which is exactly the question Stage 0 puts to the
    existing fermion↔W loop.

    ``P_field`` — for a channel carrying a real ``(E, B)`` pair:

        P_field = Σ_k [E_k × conj(B_k)] / N

    **First attempt, and why it was wrong.**  The natural first guess —
    weight the model's own curl-symbol *direction* ``Ĉ(k) =
    C(k)/|C(k)|`` (``gauge.charge_coupling.bcc_curl_symbol``) by the mode
    energy density ``(|E_k|²+|B_k|²)/2`` — is *identically zero for every
    real (E,B) field*, not merely a poor approximation.  A real field has
    exact Hermitian symmetry, ``E_k(-k) = conj(E_k(k))``, so the energy
    density is *even*: ``u(-k) = u(k)``.  ``bcc_curl_symbol`` is
    deliberately constructed to be exactly *odd*, ``Ĉ(-k) = -Ĉ(k)`` (its own
    docstring: "symmetrise over the grid involution ... the symbol is then
    exactly odd, as the FFT of a real field requires").  Pairing each mode
    with its negation, ``Ĉ(k)u(k) + Ĉ(-k)u(-k) = Ĉ(k)u(k) - Ĉ(k)u(k) ≡ 0``
    term by term — confirmed numerically (an axis-aligned beam packet from
    ``fields.photon.build_beam_packet`` gave P_field ~1e-16 at every tick,
    not because the field carries no momentum but because the construction
    is mathematically incapable of returning a nonzero answer).  An
    *amplitude-only* quantity like energy density has thrown away exactly
    the phase relationship between E and B that a cross product needs.

    **What actually works.**  ``E_k × conj(B_k)`` is *not* amplitude-only —
    it keeps the E/B phase relationship a genuine cross product needs, and by
    the discrete correlation theorem (Parseval for a product of two real
    fields) it is exactly ``Σ_x [E(x) × B(x)]`` — this is derived from the
    lattice's own Fourier representation of the *same* (E, B) pair the
    curl-symbol formalism already operates on, not pasted in from continuum
    Maxwell.  It is conserved **exactly** (bit-identical, not merely small)
    under one tick of the free rotation ``gauge.photon.photon_step_spectral``
    — verified numerically for a genuine transverse plane-wave mode
    (``fields.photon.build_pair_mode``, ``E∥e1 ⊥ B∥e2 ⊥ k̂``) held over 40
    ticks — because that step rotates ``(E_k[a], B_k[a])`` by the *same*
    angle ``Ω_pair(k)`` independently for each Cartesian component ``a``,
    the discrete analogue of the continuum Poynting-theorem identity that
    keeps ``∫E×B`` invariant under source-free Maxwell evolution.  The
    single-component ``build_beam_packet`` construction (E and B sharing one
    Cartesian axis, the RS-analytic-signal ``F=E+iB`` embedding) has ``E∥B``
    pointwise and so carries **zero** field momentum by construction — a
    real limitation of that helper for this purpose, not of this formula;
    use ``build_pair_mode`` (or any genuinely transverse two-axis
    construction) when a nonzero ``P_field`` baseline is wanted.

    ``P_total`` in the summary is ``P_matter + P_field`` for whichever of the
    two legs a channel provides, one row per channel plus a run-wide sum
    across every channel present — the quantity Stage 5's momentum-
    conservation claim (``ΔP_matter + ΔP_field ≈ 0``) will be read off.

    Normalisation: both sums divide by ``N`` (Parseval, matching numpy's
    unnormalised-forward/``1/N``-inverse FFT convention), so for a
    unit-normalised matter packet ``P_matter`` is literally the expectation
    value ``⟨k⟩``.  ``P_field`` carries the same convention for direct
    comparability, not because field norm is probability-normalised.

    A channel exposing neither shape (i.e. not a spinor and not an (E,B)
    pair — the many-body register, a scalar dielectric) is silently skipped.

    **Why ``P_field`` is restricted to ``photon_pair``/``charge_photon``/
    ``em_photon``.** (Stage 4, ``docs/roadmaps/photon-fermion-coupling.md``:
    ``em_photon``'s ``(E,B)`` is the same audited genuine spatial 3-vector
    pair as ``photon_pair``'s, sourced but not reshaped, so it belongs on
    this whitelist for the identical reason.)
    ``w_sourced``, ``z_even`` and ``gluon_bcc`` *also* carry state dicts keyed
    ``"E"``/``"B"``, but their leading axis is not a spatial polarisation —
    it is the isospin triplet (``w_sourced``, shape ``(3,L,L,L)``, the *same*
    shape as the photon's genuine spatial vector, by coincidence), a bare
    scalar (``z_even``, ``(L,L,L)``), or the colour octet (``gluon_bcc``,
    ``(8,L,L,L)``).  A cross product across an isospin or colour index is not
    a momentum — it has no more meaning than crossing two rows of an
    unrelated table — so this observer whitelists the channel types whose
    ``(E,B)`` are audited to be genuine 3-component spatial vectors rather
    than keying on array shape, which cannot tell an isospin triplet from a
    polarisation triplet.  W/Z/gluon field momentum is not implemented here;
    doing so honestly needs those channels to carry a spatial-vector-valued
    field (shape ``(3,3,L,L,L)``: generator × spatial axis), which they do
    not.
    """
    name = "momentum"
    label = "Momentum"
    exactness = "exact"

    #: state keys treated as complex spinor components of one matter field.
    _MATTER_KEYS = ("f", "g", "f_nu", "f_e", "g_nu", "g_e",
                    "eta_u", "eta_d", "chi_u", "chi_d", "f_u", "f_d")

    #: channel types whose (E, B) are audited genuine spatial 3-vectors
    #: (F69 paired-photon law) rather than an isospin/colour-indexed pair
    #: that merely happens to share the "E"/"B" key names — see class
    #: docstring.
    _EM_VECTOR_CHANNELS = ("photon_pair", "charge_photon", "em_photon")

    def observe(self, sim) -> None:
        from casim.numerics import fft as _fft
        from casim.engine.lattice.geometry import make_kgrid_3d

        rec: Dict[str, Any] = {"tick": sim.tick, "channels": {}}
        for cname, ch in sim.channels.items():
            st = sim.states[cname]
            entry: Dict[str, Any] = {}

            mkeys = [k for k in self._MATTER_KEYS
                     if k in st and np.iscomplexobj(np.asarray(st[k]))]
            if mkeys:
                shape = np.asarray(st[mkeys[0]]).shape
                # Spatial axes are the trailing three; any leading axis is an
                # internal index (e.g. a colour-stacked quark, (3, L, L, L)),
                # summed over after a transform on the spatial axes only.
                spatial = shape[-3:]
                KX, KY, KZ = make_kgrid_3d(*spatial)
                n = KX.size
                Pm = np.zeros(3)
                for key in mkeys:
                    a = np.asarray(st[key])
                    if a.shape != shape:
                        continue
                    dens = np.abs(_fft.fftn(a, axes=(-3, -2, -1))) ** 2
                    if dens.ndim > 3:
                        dens = dens.reshape((-1,) + spatial).sum(axis=0)
                    Pm[0] += float(np.sum(KX * dens))
                    Pm[1] += float(np.sum(KY * dens))
                    Pm[2] += float(np.sum(KZ * dens))
                entry["P_matter"] = (Pm / n).tolist()

            if (ch.type_name in self._EM_VECTOR_CHANNELS
                    and "E" in st and "B" in st):
                E, B = np.asarray(st["E"]), np.asarray(st["B"])
                if E.shape[:1] == (3,) and B.shape == E.shape:
                    n = E[0].size
                    Ek = [_fft.fftn(E[a]) for a in range(3)]
                    Bk = [_fft.fftn(B[a]) for a in range(3)]
                    # E_k x conj(B_k), summed over k: Parseval's correlation
                    # theorem makes this exactly Sum_x [E(x) x B(x)] (see
                    # class docstring) — the field momentum this model's own
                    # (E,B) Fourier representation carries, not an amplitude-
                    # only construction that a real field's Hermitian
                    # symmetry would force to vanish identically.
                    px = Ek[1] * np.conj(Bk[2]) - Ek[2] * np.conj(Bk[1])
                    py = Ek[2] * np.conj(Bk[0]) - Ek[0] * np.conj(Bk[2])
                    pz = Ek[0] * np.conj(Bk[1]) - Ek[1] * np.conj(Bk[0])
                    Pf = np.array([px.sum(), py.sum(), pz.sum()]).real
                    entry["P_field"] = (Pf / n).tolist()

            if entry:
                # `rel_drift` vs this run's own first record — the scalar the
                # generic exactness table (casim.analysis._scalarize) reads,
                # matching the convention every other machine/exact observer
                # here uses (NormConservation, TotalEnergy).
                if not hasattr(self, "_P0"):
                    self._P0: Dict[str, Dict[str, np.ndarray]] = {}
                p0 = self._P0.get(cname)
                if p0 is None:
                    self._P0[cname] = {k: np.array(v) for k, v in entry.items()}
                    entry["rel_drift"] = 0.0
                else:
                    worst = 0.0
                    for key, val in entry.items():
                        p0v = p0.get(key)
                        if p0v is None:
                            continue
                        base = float(np.linalg.norm(p0v))
                        d = float(np.linalg.norm(np.array(val) - p0v))
                        worst = max(worst, d / base if base > 1e-300 else d)
                    entry["rel_drift"] = worst
                rec["channels"][cname] = entry
        self.records.append(rec)

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {}
        r0, rf = self.records[0], self.records[-1]
        out: Dict[str, Any] = {}
        total0 = np.zeros(3)
        totalf = np.zeros(3)
        for cname in rf["channels"]:
            c0 = r0["channels"].get(cname, {})
            cf = rf["channels"][cname]
            row: Dict[str, Any] = {}
            for key in ("P_matter", "P_field"):
                if key in c0 and key in cf:
                    p0 = np.array(c0[key])
                    pf = np.array(cf[key])
                    total0 += p0
                    totalf += pf
                    row[key] = {
                        "P0": p0.tolist(), "Pf": pf.tolist(),
                        "delta": (pf - p0).tolist(),
                        "delta_mag": float(np.linalg.norm(pf - p0)),
                    }
            if row:
                out[cname] = row
        out["P_total"] = {
            "P0": total0.tolist(), "Pf": totalf.tolist(),
            "delta": (totalf - total0).tolist(),
            "delta_mag": float(np.linalg.norm(totalf - total0)),
        }
        return out


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


@register_observer
class FieldDump(Observer):
    """Dump real 3-D field volumes to disk for offline rendering.

    The visualisation seam (``docs/design/visualization.md``): the engine never
    imports a renderer.  It writes VTK ImageData (``.vti``, via the
    dependency-free :mod:`casim.io.vtk` writer) and/or ``.npz``, and ParaView,
    PyVista, napari, or plain numpy read the result afterwards.  This keeps
    long native runs inspectable after the fact — the same motivation as
    checkpoint/resume — and means no GUI toolkit is on the physics path.

    What gets written
    -----------------
    Always ``density`` — the channel's :meth:`Channel.density_field`, the same
    real scalar volume the GUI point cloud renders, so the file and the live
    view cannot disagree.  With ``components: true``, additionally the channel's
    own arrays reduced to real parts: spinors as ``f_re/f_im/g_re/g_im``, gauge
    fields as ``E``/``B`` (3-vectors when component-shaped), the dielectric as
    ``K``.

    Complex data is **never** written implicitly.  Every complex array is split
    into explicitly named real and imaginary volumes, because a renderer that
    silently drops the imaginary part produces a picture that looks fine and is
    wrong (CLAUDE.md's standing caution on chiral transforms).

    Scenario keys
    -------------
    ``dir``         output directory (default ``test-results/fields/<run>``)
    ``channels``    optional list of channel names to restrict to
    ``format``      ``"vti"`` (default) | ``"npz"`` | ``"both"``
    ``components``  also dump the raw real components (default ``False``)
    ``stride``      spatial downsample factor (default 1 = full resolution)
    ``precision``   ``"float32"`` (default) | ``"float64"``
    ``max_mb``      write budget; dumping stops when exceeded (default 512)

    Example::

        observers:
          - {type: field_dump, every: 10, format: vti, stride: 2, max_mb: 256}
    """
    name = "field_dump"
    label = "Field Dump"
    exactness = "quantitative"

    def __init__(self, every: int = 1, **config: Any):
        super().__init__(every=every, **config)
        self._files: List[Dict[str, Any]] = []
        self._bytes = 0
        self._stopped = False
        self._skipped: Dict[str, str] = {}

    # -- reduction: channel state → {name: real ndarray} -------------------
    @staticmethod
    def _real_arrays(ch, state, components: bool) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        try:
            d = np.asarray(ch.density_field(state))
        except Exception as exc:  # channel has no renderable volume
            raise ValueError(f"no density field: {exc}") from exc
        if d.ndim not in (2, 3):
            raise ValueError(f"density has shape {d.shape}, not a 2-/3-D volume")
        out["density"] = np.real(d) if np.iscomplexobj(d) else d

        if not components:
            return out
        for key in ("f", "g"):
            if key in state:
                a = np.asarray(state[key])
                if a.ndim not in (2, 3):
                    continue
                if np.iscomplexobj(a):
                    out[f"{key}_re"] = a.real
                    out[f"{key}_im"] = a.imag
                else:
                    out[key] = a
        for key in ("E", "B"):
            if key in state:
                a = np.asarray(state[key])
                if np.iscomplexobj(a):
                    out[f"{key}_re"], out[f"{key}_im"] = a.real, a.imag
                elif a.ndim in (2, 3, 4):
                    out[key] = a
        if "K" in state:
            a = np.asarray(state["K"])
            if a.ndim in (2, 3):
                out["K"] = np.real(a) if np.iscomplexobj(a) else a
        return out

    @staticmethod
    def _stride(a: np.ndarray, s: int) -> np.ndarray:
        if s <= 1:
            return a
        if a.ndim == 4:
            return a[:, ::s, ::s, ::s]
        if a.ndim == 3:
            return a[::s, ::s, ::s]
        return a[::s, ::s]

    # -- the per-tick dump --------------------------------------------------
    def observe(self, sim) -> None:
        if self._stopped:
            return
        import os

        from ...io.vtk import write_image_data

        run = getattr(sim, "name", None) or "run"
        outdir = self.config.get("dir") or os.path.join(
            "test-results", "fields", str(run))
        only = self.config.get("channels")
        fmt = str(self.config.get("format", "vti")).lower()
        components = bool(self.config.get("components", False))
        stride = max(1, int(self.config.get("stride", 1)))
        dtype = (np.float64 if str(self.config.get("precision", "float32"))
                 == "float64" else np.float32)
        max_bytes = float(self.config.get("max_mb", 512)) * 1024 * 1024

        rec: Dict[str, Any] = {"tick": sim.tick, "files": []}
        for cname, ch in sim.channels.items():
            if only and cname not in only:
                continue
            try:
                arrays = self._real_arrays(ch, sim.states[cname], components)
            except Exception as exc:
                # Compute-once spectral channels and the 2^n many-body register
                # hold no spatial volume; record why and move on rather than
                # failing a run over a diagnostic.
                self._skipped.setdefault(cname, str(exc))
                continue
            arrays = {k: self._stride(np.asarray(v), stride)
                      for k, v in arrays.items()}

            stem = os.path.join(outdir, f"{cname}_t{sim.tick:06d}")
            written: List[str] = []
            if fmt in ("vti", "both"):
                written.append(write_image_data(
                    stem + ".vti", arrays,
                    spacing=(stride, stride, stride),
                    dtype=dtype,
                    field_data={"tick": sim.tick,
                                "energy": ch.energy(sim.states[cname]),
                                "c_lat": float(getattr(sim.lattice,
                                                       "c_lat", 0.0)),
                                "block": float(getattr(sim.lattice,
                                                       "block", 1))},
                ))
            if fmt in ("npz", "both"):
                os.makedirs(outdir, exist_ok=True)
                np.savez_compressed(
                    stem + ".npz",
                    **{k: v.astype(dtype) for k, v in arrays.items()})
                written.append(os.path.abspath(stem + ".npz"))

            for path in written:
                size = os.path.getsize(path)
                self._bytes += size
                entry = {"tick": sim.tick, "channel": cname,
                         "path": path, "bytes": size,
                         "fields": sorted(arrays)}
                self._files.append(entry)
                rec["files"].append(entry)

        rec["cumulative_bytes"] = self._bytes
        self.records.append(rec)

        if self._bytes > max_bytes:
            self._stopped = True
            rec["stopped"] = (
                f"write budget max_mb={self.config.get('max_mb', 512)} "
                f"exceeded at tick {sim.tick}; dumping halted"
            )

    # -- end of run: index the series --------------------------------------
    def summary(self) -> Dict[str, Any]:
        if not self._files:
            return {"files_written": 0, "skipped_channels": self._skipped}
        import os

        from ...io.vtk import write_pvd

        collections: Dict[str, str] = {}
        by_channel: Dict[str, List] = {}
        for e in self._files:
            if e["path"].endswith(".vti"):
                by_channel.setdefault(e["channel"], []).append(
                    (float(e["tick"]), os.path.basename(e["path"])))
        for cname, entries in by_channel.items():
            outdir = os.path.dirname(
                next(e["path"] for e in self._files
                     if e["channel"] == cname and e["path"].endswith(".vti")))
            collections[cname] = write_pvd(
                os.path.join(outdir, f"{cname}.pvd"), sorted(entries))

        return {
            "files_written": len(self._files),
            "total_mb": round(self._bytes / (1024 * 1024), 3),
            "collections": collections,
            "skipped_channels": self._skipped,
            "stopped_early": self._stopped,
            "note": ("ImageData is a uniform grid: a BCC lattice is written "
                     "with cubic indexing (array layout is exact; geometric "
                     "BCC offsets are not applied). Open the .pvd in ParaView "
                     "to load the run as a time series."),
        }
