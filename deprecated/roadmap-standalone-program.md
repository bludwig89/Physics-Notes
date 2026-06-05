# Roadmap — Single-Run Scripts → Standalone Modeling Program

2026-06-04 - 19:08

## Goal

Convert the current collection of `ca_*.py` physics modules (~18k lines, 30+ files) and ~95 single-run `run_*`/`test_*` scripts into one installable program — `casim` — with:

1. A **CLI** driven by scenario config files (reproducible, scriptable, resumable runs).
2. An **interactive GUI** grown from `live_display.py` (load scenario, pause/step, inspect fields, adjust parameters live).

This is a refactor, not a rewrite. The physics kernels are already well-factored pure functions (e.g. `ca_wmu._f26_rotation_step`, `ca_bcc.weyl_step_3d_bcc`, `ca_gluon.gluon_rotation_step_spectral_bcc`, `ca_photon_pair.photon_step_spectral`). What is missing is the layer above them: a simulation engine, configuration, persistence, and a unified entry point.

## Current State (surveyed 2026-06-04)

- `ca-simulation/` — 30+ flat modules; physics steppers, diagnostics, and field constructors mixed in the same files; 19 modules carry `if __name__` demo blocks.
- `model-tests/` — 95 scripts, each hard-coding lattice size, tick count, seeds, and figure paths; each re-inserts `ca-simulation` onto `sys.path`.
- `live_display.py` — vispy point-cloud viewer with its own hard-coded initial condition and step loop (module-level state, keyboard controls).
- `test-results/` — JSON dumps + markdown summaries written ad hoc by each script.
- No package metadata; `requirements.txt` only (numpy, matplotlib).

## Architecture

### 1. Package layout (src layout, `pyproject.toml`)

```
casim/
├── lattice/        # ca_core, ca_core_exact, ca_bcc, ca_fft, ca_lazy, ca_lattice
├── fields/
│   ├── photon.py       # ca_photon_pair (F67/68/69 paired-spinor photon)
│   ├── electroweak.py  # ca_wmu, ca_weak, ca_z_field, ca_charged_current, ca_hypercharge
│   ├── strong.py       # ca_gluon, ca_strong, ca_colour_*, ca_confinement, spinor_color
│   ├── matter.py       # ca_dirac, ca_dirac_bcc, ca_baryon, ca_higgs
│   └── em.py           # ca_maxwell, ca_maxwell_2d (σ-bilinear; massive/non-Abelian sectors only, per F67)
├── gravity/        # ca_curved, ca_emqg, poisson_open (F64 dielectric K)
├── engine/         # NEW: Simulation class, channel registry, observers, checkpointing
├── analysis/       # dispersion fits, norm tracking, exactness checks (extracted from run_* scripts)
├── io/             # scenario loader, result writer (JSON schema for test-results/)
├── viz/            # viz.py, tick_heatmap.py (static figures)
├── gui/            # live_display.py refactored against engine API
└── cli.py          # entry point
```

Backward compatibility: keep thin shims (`ca_wmu.py` re-exporting from `casim.fields.electroweak`) for one phase so existing scripts keep running, then delete.

### 2. Engine (the new code)

The one genuinely new component. Sketch:

```python
class Simulation:
    lattice: LatticeSpec          # L, dims, topology (cubic | BCC), c_lat
    channels: dict[str, Channel]  # registered field channels
    observers: list[Observer]     # run every N ticks
    tick: int

    def step(self, n=1): ...      # advance all channels one CA tick
    def checkpoint(self, path): ...
    @classmethod
    def from_scenario(cls, path): ...
    @classmethod
    def resume(cls, checkpoint): ...

class Channel(Protocol):
    name: str
    propagator: str               # "even" | "chiral"  (F91 classification)
    def step(self, state, lattice) -> state: ...
    def energy(self, state) -> float: ...
```

Channel registry maps directly onto the F91 propagator classification, making the branch structure an explicit, inspectable program property:

| Channel | Propagator | Kernel |
|---|---|---|
| photon (γ) | even (forced) | `photon_step_spectral` / `_f26_rotation_step` |
| W± | chiral (forced) | `w_propagation_step_chiral` |
| Z | even + mass-suppressed axial split | `ca_z_field` steppers |
| gluon | even (forced, F91) | `gluon_rotation_step_spectral_bcc` |
| Weyl/Dirac matter | per-branch | `weyl_step_3d_bcc`, `covariant_weyl_step_3d_bcc_exact` |
| gravity | dielectric K renorm of rotation rule (F64) | `ca_curved` / `ca_emqg` |

Observers replace the inline diagnostics currently duplicated across run scripts: `NormConservation`, `DispersionFit`, `UnitarityResidual`, `EnergyTrace`, `FieldSnapshot`. Each writes into a structured result dict; exactness class (`exact` | `machine-precision`) is declared per observer so `exactness-inventory.md` can be generated rather than maintained by hand.

### 3. Scenario files (YAML)

Each `run_*` script collapses to a config:

```yaml
# scenarios/F49_bcc_weinberg.yaml
name: F49-bcc-weinberg-2over9
lattice: {L: 32, topology: bcc, c_lat: 0.57735026918962576}   # 1/√3
seed: 7
ticks: 200
channels:
  - {type: weyl_bcc, sign: "+", init: gaussian, sigma: 3.0}
observers:
  - {type: dispersion_fit, every: 1}
  - {type: norm_conservation, every: 10}
checkpoint: {every: 1000, dir: checkpoints/}
output: {json: test-results/F49.json, figures: test-results/figures/}
```

One driver replaces ~95 scripts. Every historical result becomes reproducible from a committed config + seed.

### 4. Checkpointing & long runs

HDF5 (or NPZ) snapshots of all channel states + tick counter + RNG state, every N ticks, with `casim resume`. This directly addresses the standing problem of runs exceeding the 90 s sandbox limit: long jobs run on Ben's machine, are resumable, and Claude reads checkpoints/JSON results between runs instead of needing the run to finish in one shot.

### 5. CLI

```
casim run scenarios/F49_bcc_weinberg.yaml [--ticks N] [--seed S]
casim resume checkpoints/F49_t1000.h5
casim analyze test-results/F49.json [--figures]
casim gui [scenarios/photon_pair.yaml]
casim list-channels        # registry + propagator class (even/chiral) per F91
```

### 6. GUI (grow live_display.py)

Phase 1 — re-point: `live_display` consumes a `Simulation` instead of its own module-level loop. Existing controls (pause, reset, ±c, helicity cycle, density threshold) become engine calls. Vispy + Qt stays.

Phase 2 — control panel (Qt dock around the vispy canvas):
- Scenario load/save; channel enable/disable; parameter sliders bound to scenario values.
- Tick controls: run / pause / single-step / run-to-tick.
- Live observer readouts: norm drift, energy per channel, dispersion residual.
- Field selector: which channel and which quantity (|ψ|², E/B rotation phase, K dielectric) the point cloud renders.
- Checkpoint save/load from the GUI.

Phase 3 (optional) — slice/heatmap 2-D views (reuse `tick_heatmap.py`) alongside the 3-D cloud.

### 7. Tests → pytest

`test_F*.py` scripts become a pytest suite with markers: `@pytest.mark.exact`, `@pytest.mark.machine_precision`, `@pytest.mark.slow`. `tests-priority/` becomes the default CI selection. A small plugin collects marker + tolerance metadata and regenerates `exactness-inventory.md`.

### 8. Backend abstraction (deferred)

Route FFTs and chiral transforms through one thin module (`casim.lattice.backend`) so numpy can be swapped for the hand-written chiral library (per the standing numpy/scipy chiral-transform concern in CLAUDE.md) or numba/GPU later, without touching physics code. Not needed for the initial conversion; the seam should exist from day one.

## Phasing

| Phase | Work | Outcome |
|---|---|---|
| A | `pyproject.toml`, src layout, move modules, compat shims | `pip install -e .`; old scripts still run |
| B | Engine: `Simulation`, channel registry, 4–5 observers | core abstraction in place |
| C | Scenario loader + CLI `run`/`analyze`; migrate 3 pilot scripts (suggest: photon pair F69, BCC Weyl dispersion, F64 light deflection) | proof the pattern covers spectral, BCC, and gravity cases |
| D | Checkpointing + `resume`; migrate remaining run scripts as scenarios | long-run problem solved |
| E | GUI phase 1–2 | interactive program |
| F | pytest conversion + exactness-inventory generation | tests self-documenting |
| G | Backend abstraction, optional GPU | performance path |

Phases A–C are the structural change and should land together before anything else migrates. Each phase gets a changelog entry; no physics behavior changes anywhere — every migrated scenario must reproduce its original script's JSON output (machine-precision identical given the same seed) before the script is deleted.

## Risks / decisions to make

- **Spectral vs. real-space stepping**: several kernels are k-space (FFT-resident); the engine must let a channel keep state in k-space between ticks rather than forcing round-trips. Channel protocol above allows this — state shape is channel-owned.
- **BCC vs. cubic coexistence**: lattice topology is a `LatticeSpec` property; channels declare which topologies they support, and the engine refuses mismatched scenarios.
- **Qt dependency**: GUI pulls in PyQt6; keep it an optional extra (`pip install casim[gui]`) so headless runs stay numpy+matplotlib only.
- **Naming**: `casim` is a placeholder; pick before Phase A.
