"""casim.suite.tiers — scale tiers and per-scenario sizing.

The user-run suite runs the *same* scenario files at several orders of
magnitude more compute than the shipped (sandbox) sizes.  Cost scales as

    cost  =  L**dims  ×  ticks          (the RUN-GUIDE law)

so a tier is a pair of multipliers ``(L_mult, ticks_mult)`` chosen so that the
typical 3-D scenario lands near a target cost decade:

    smoke   1×      shipped YAML sizes (sandbox / dev-smoke tier)
    10x     ~10×    L×1.6, ticks×2.5      (1.6**3 × 2.5 ≈ 10)
    100x    ~100×   L×2.5, ticks×6.5      (2.5**3 × 6.5 ≈ 102)
    1000x   ~1000×  L×4.0, ticks×16       (4.0**3 × 16  ≈ 1024)

Per-scenario overrides protect the pathological cases (the 4-D ``gauge_mc``
whose cost is ``L**4``; the odd-``L`` ``charge_photon``) and let a scenario opt
into explicit production sizes or be skipped at a tier.

Real-space / block-spin scenarios are handled differently: the tier grows the
**physical patch** (the ``block`` factor), so the *represented* physical volume
climbs by orders of magnitude while the tractable super-cell lattice ``L`` is
held fixed.  This is the F129–F133 coarse-graining substitution — "a coarse
cell stands in for many physical cells" (roadmap-scale-to-real-space §0).

Nothing here invents an SI fm/cell mapping: the canonical ruler is Planck-scale
(F107, a = 6.5978 ℓ_P), so a literal real-space fill is ~45 decades out of
reach.  The real-space tiers report the represented physical cell count
(``physical_L**dims``) honestly; absolute fm/eV stay scale-gated (F123).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

# Bytes for one complex128 lattice scalar; scenarios carry several state arrays
# plus FFT working memory, so the footprint estimate multiplies by a fudge.
_BYTES_PER_CELL = 16
_STATE_ARRAYS_GUESS = 6      # spinor (f,g) + gauge (E,B) + scratch, typical
_FFT_OVERHEAD = 3.0          # out-of-place transforms keep a few copies live

# ---------------------------------------------------------------------------
# Wall-time model — roadmap P2.6
#
# `--list` predicted memory but not duration, so nobody could size a multi-day
# run before launching it: the only way to find out that a 1000x tier would take
# a week was to start it. This is the missing half.
#
# **What it is: a measured per-scenario anchor times a computed cost ratio.**
# The anchors below are the sandbox wall-clock times recorded in
# `scenarios/RUN-GUIDE.md` at each scenario's shipped size. The estimate is
#
#     seconds ~= anchor * cost_factor * log_correction
#
# where `cost_factor` is (L^dims * ticks) / (base_L^dims * base_ticks) — already
# computed for the memory model — and `log_correction` accounts for the FFT's
# N log N rather than N, which a pure cell-count ratio misses.
#
# **What it is not: a benchmark.** Three honest caveats, all of which make it a
# lower bound on a big tier:
#   * the anchors are one machine (the sandbox), and the roadmap's P2.1/P2.4
#     throughput claim has never been measured on Ben's hardware, so a real run
#     may be faster;
#   * cache behaviour degrades once the working set leaves L3, which this does
#     not model at all;
#   * `gauge_mc` is not FFT-bound (it is an L^4 link update with a per-site
#     reunitarisation), so its log correction is deliberately disabled.
# An estimate that says "about a day" when the truth is "about three days" is
# still the difference between a decision and a surprise, which is why this
# ships labelled rather than waiting for a benchmark rig.
# ---------------------------------------------------------------------------

#: Measured sandbox wall-clock at each scenario's *shipped* size, from
#: `scenarios/RUN-GUIDE.md`. A scenario with no anchor reports `None` rather
#: than a guess.
_SMOKE_SECONDS: Dict[str, float] = {
    "photon_pair": 0.8,
    "bcc_weyl": 0.7,
    "w_chiral": 0.7,
    "z_even": 0.5,
    "gluon_bcc": 1.1,
    "gravity_deflection": 0.3,
    "fermion_w_backreaction": 0.5,
    "beta_decay": 0.5,
    "charge_photon": 0.5,
    "refraction_2d": 1.3,
    "gauge_mc": 6.0,
    "photon_beam_all_fields": 3.0,
    "bcc_fields_companion": 0.7,
    "gravity_dynamic_selfsourced": 2.5,
}

#: Scenarios whose cost is not FFT-dominated, so no N log N correction applies.
_NOT_FFT_BOUND = frozenset({"gauge_mc"})


def _log_correction(compute_cells: int, base_cells: int) -> float:
    """The `log N` in `N log N`, as a ratio. 1.0 when the sizes match."""
    import math
    if compute_cells <= 1 or base_cells <= 1:
        return 1.0
    return math.log2(compute_cells) / math.log2(base_cells)


@dataclass(frozen=True)
class Tier:
    name: str
    L_mult: float
    ticks_mult: float
    # block-spin patch multiplier (grows the represented physical patch)
    patch_mult: float
    target_cost: float
    blurb: str


TIERS: Dict[str, Tier] = {
    "smoke": Tier("smoke", 1.0, 1.0, 1.0, 1.0,
                  "shipped YAML sizes — sandbox / dev-smoke gate"),
    "10x":   Tier("10x", 1.6, 2.5, 2.0, 10.0,
                  "~10× compute; ~8× more represented physical cells"),
    "100x":  Tier("100x", 2.5, 6.5, 4.0, 100.0,
                  "~100× compute; ~64× more represented physical cells"),
    "1000x": Tier("1000x", 4.0, 16.0, 8.0, 1000.0,
                  "~1000× compute; ~512× more represented physical cells"),
}

DEFAULT_TIER = "smoke"


@dataclass
class ScenarioOverride:
    """Per-scenario sizing controls.

    ``explicit`` maps a tier name to an exact ``(L, ticks)`` pair, bypassing the
    generic multipliers (use for the RUN-GUIDE production sizes or to cap a
    pathological scenario).  ``L_parity`` forces even/odd ``L``.  ``L_cap`` is a
    hard ceiling on the scaled ``L``.  ``skip_tiers`` drops the scenario at
    those tiers (e.g. a 4-D MC that is production-only).  ``realspace=True``
    routes scaling through the block-spin patch instead of ``L``.
    """
    explicit: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    L_parity: str = "any"            # "any" | "even" | "odd"
    L_cap: Optional[int] = None
    ticks_cap: Optional[int] = None
    skip_tiers: Tuple[str, ...] = ()
    realspace: bool = False
    note: str = ""


# Hand-tuned guards for the scenarios whose cost does not follow the generic
# L**3 rule, drawn from scenarios/RUN-GUIDE.md production guidance.
OVERRIDES: Dict[str, ScenarioOverride] = {
    # 4-D gauge Monte-Carlo: cost is L**4, so a generic L×4 would be 256× per
    # extra ticks.  Cap L tightly and let ticks (sweeps) carry the scale.
    "gauge_mc": ScenarioOverride(
        explicit={"smoke": (6, 40), "10x": (8, 120),
                  "100x": (10, 400), "1000x": (12, 1200)},
        note="L**4 cost; production ceiling ~L=16 (RUN-GUIDE). Native only at 1000x."),
    # charge_photon requires an odd L (curl staggering).
    "charge_photon": ScenarioOverride(L_parity="odd",
                                      note="odd L required by the curl stencil"),
    # 2-D refraction: cost is L**2, so it can take a larger L per tier.
    "refraction_2d": ScenarioOverride(
        explicit={"smoke": (128, 80), "10x": (256, 200),
                  "100x": (512, 520), "1000x": (1024, 1280)},
        note="2-D (L**2 cost); needs SciPy"),
    # The compute-once spectral falsification scenarios have no L/ticks knob.
    "njl_pion": ScenarioOverride(skip_tiers=("10x", "100x", "1000x"),
                                 note="spectral compute-once; size-invariant"),
    "njl_nucleon": ScenarioOverride(skip_tiers=("10x", "100x", "1000x"),
                                    note="spectral compute-once; size-invariant"),
    "string_tension_fpi": ScenarioOverride(skip_tiers=("10x", "100x", "1000x"),
                                           note="spectral compute-once; size-invariant"),
    # Static eikonal — one Poisson solve; scale the grid only.
    "gravity_deflection": ScenarioOverride(
        explicit={"smoke": (64, 0), "10x": (128, 0),
                  "100x": (256, 0), "1000x": (512, 0)},
        note="static eikonal; ticks=0, scale the Poisson grid"),
    # Real-space block-spin scenarios: scale the physical patch, not L.
    "realspace_proton_1fm": ScenarioOverride(realspace=True,
                                             note="nucleon-scale block-spin patch"),
    "realspace_neutron_1fm": ScenarioOverride(realspace=True,
                                              note="nucleon-scale block-spin patch"),
    "realspace_hydrogen_bohr": ScenarioOverride(realspace=True,
                                                note="atom-scale block-spin patch"),
    "realspace_photon_patch": ScenarioOverride(realspace=True,
                                               note="F133 even-law carrier on a real-space patch"),
    "blockspin_photon": ScenarioOverride(realspace=True,
                                         note="Phase-4 adaptive-resolution photon"),
}


def _coerce_parity(L: int, parity: str) -> int:
    L = max(2, int(round(L)))
    if parity == "odd" and L % 2 == 0:
        L += 1
    elif parity == "even" and L % 2 == 1:
        L += 1
    return L


@dataclass
class SizePlan:
    """Effective sizing for one scenario at one tier."""
    scenario: str
    tier: str
    dims: int
    base_L: int
    base_ticks: int
    L: int
    ticks: int
    block: int                    # block-spin factor (real-space scenarios)
    physical_L: int               # cells per axis represented (L*block)
    represented_cells: int        # physical_L ** dims
    compute_cells: int            # L ** dims  (what the machine actually holds)
    cost_factor: float            # vs the scenario's own smoke baseline
    mem_bytes: int
    realspace: bool
    skipped: bool
    #: P2.6 wall-time ESTIMATE in seconds, or None when the scenario has no
    #: measured anchor. See the module header for the model and its caveats.
    wall_seconds: Optional[float] = None
    note: str = ""

    @property
    def mem_gb(self) -> float:
        return self.mem_bytes / 1024 ** 3

    @property
    def wall_human(self) -> str:
        """The estimate as something a human can decide on, or `?`."""
        s = self.wall_seconds
        if s is None:
            return "?"
        if s < 90:
            return f"{s:.0f}s"
        if s < 5400:
            return f"{s / 60:.0f}m"
        if s < 172800:
            return f"{s / 3600:.1f}h"
        return f"{s / 86400:.1f}d"

    def as_overrides(self) -> Dict[str, int]:
        """The ``--L`` / ``--ticks`` overrides to feed the engine."""
        out: Dict[str, int] = {}
        if not self.realspace:
            out["L"] = self.L
        out["ticks"] = self.ticks
        return out


def lattice_dims(scenario: Dict) -> int:
    lat = scenario.get("lattice", {}) or {}
    return int(lat.get("dims", 3))


def base_L_of(scenario: Dict) -> int:
    lat = scenario.get("lattice", {}) or {}
    if "physical_patch" in lat:
        block = int(lat.get("block", 1))
        return int(lat["physical_patch"]) // max(1, block)
    return int(lat.get("L", 16))


def plan_size(name: str, scenario: Dict, tier_name: str) -> SizePlan:
    """Compute the effective (L, ticks, block) for ``scenario`` at ``tier``."""
    if tier_name not in TIERS:
        raise ValueError(f"unknown tier {tier_name!r}; choose {list(TIERS)}")
    tier = TIERS[tier_name]
    ov = OVERRIDES.get(name, ScenarioOverride())
    dims = lattice_dims(scenario)
    lat = scenario.get("lattice", {}) or {}

    base_L = base_L_of(scenario)
    base_ticks = int(scenario.get("ticks", 0))
    base_block = int(lat.get("block", 1))

    skipped = tier_name in ov.skip_tiers

    if ov.realspace:
        # Grow the represented physical patch via the block factor; hold the
        # tractable super-cell lattice L fixed.
        block = max(1, int(round(base_block * tier.patch_mult)))
        L = base_L
        ticks = max(base_ticks, int(round(base_ticks * (tier.ticks_mult ** 0.5))))
    elif tier_name in ov.explicit:
        L, ticks = ov.explicit[tier_name]
        block = base_block
    else:
        L = _coerce_parity(base_L * tier.L_mult, ov.L_parity)
        if ov.L_cap:
            L = min(L, ov.L_cap)
        ticks = int(round(base_ticks * tier.ticks_mult))
        if ov.ticks_cap:
            ticks = min(ticks, ov.ticks_cap)
        block = base_block

    physical_L = L * block
    represented_cells = physical_L ** dims
    compute_cells = L ** dims
    smoke_compute = base_L ** dims * max(1, base_ticks)
    this_compute = compute_cells * max(1, ticks)
    cost_factor = this_compute / max(1, smoke_compute)
    mem_bytes = int(compute_cells * _BYTES_PER_CELL
                    * _STATE_ARRAYS_GUESS * _FFT_OVERHEAD)

    # P2.6 wall-time estimate. `None` when there is no measured anchor — an
    # absent estimate is honest, a fabricated one is not.
    anchor = _SMOKE_SECONDS.get(name)
    if anchor is None:
        wall_seconds = None
    else:
        corr = (1.0 if name in _NOT_FFT_BOUND
                else _log_correction(compute_cells, base_L ** dims))
        wall_seconds = float(anchor) * float(cost_factor) * corr

    return SizePlan(
        scenario=name, tier=tier_name, dims=dims,
        base_L=base_L, base_ticks=base_ticks,
        L=L, ticks=ticks, block=block,
        physical_L=physical_L, represented_cells=represented_cells,
        compute_cells=compute_cells, cost_factor=cost_factor,
        mem_bytes=mem_bytes, realspace=ov.realspace, skipped=skipped,
        wall_seconds=wall_seconds, note=ov.note,
    )


def tier_names() -> Tuple[str, ...]:
    return tuple(TIERS)
