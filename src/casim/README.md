# casim — the program

`casim` **is** the program (decision **D6**, roadmap C9, 2026-07-31). There is one
tree: every physics module lives under `casim.engine`, organised by sector on the
BCC base layer (**D1**); every constant comes from `casim.constants` (**D7**);
every numeric primitive comes from `casim.numerics` (**D8**); every test is a
declarative registry entry run through `casim test` (**D9**); every module is
registered (**D11**).

Until C9 this was a layer *above* a separate flat-kernel directory, which
remained the source of truth (the reversed decision **D2**). Those 124 kernels
and 47 forks now live here; the pre-clean original of each is in
`deprecated/code/`, and `docs/design/module-migration-manifest.yaml` maps all 171
old paths to their new ones.

## Install

```bash
pip install -e .            # needs setuptools>=64 (PEP 660)
pip install -e .[gui]       # + vispy/PyQt6 for the (Phase E) GUI
```

`PYTHONPATH=src` is all the path setup needed for an in-repo run; the Makefile
exports it and `tests/conftest.py` sets it for pytest. (`CASIM_LEGACY_DIR` still
exists, and `casim.LEGACY_DIR` is `None` unless a pre-C9 checkout is present —
nothing in the package reads through it.)

## CLI

```bash
casim list-channels                         # registry + F91 propagator class
casim run scenarios/photon_pair.yaml        # run a scenario, write JSON
casim run scenarios/bcc_weyl.yaml --ticks 500 --seed 1
casim resume checkpoints/gluon_bcc_t50.npz --ticks 150   # continue a long run
casim analyze test-results/casim_bcc_weyl.json --table
casim inventory                             # run checks, regenerate exactness table
casim test --scale 100x                     # unified grouped suite (see scenarios/SUITE-GUIDE.md)
casim test --list --scale 1000x             # dry-run plan: sizes, cost factor, memory
casim gui [scenario.yaml]                   # interactive viewer (needs casim[gui])
```

Without an editable install, run via `PYTHONPATH=src python -m casim.cli ...`.

## Layout

```
casim/
  lattice/    re-export: ca_lattice, ca_fft, ca_bcc, ca_core, ca_core_exact
  fields/     photon (γ even), electroweak (W chiral / Z even+axial),
              strong (gluon even, F91), matter (Weyl/Dirac), em (σ-bilinear)
  gravity/    poisson_open (numpy) + lazy ca_curved/ca_emqg (SciPy)
  lattice/    + backend.py: the FFT / chiral-transform seam (Phase G)  <- new
  engine/     Channel + registry, Simulation/LatticeSpec, observers   <- new
  particles/  typed particles stacked on the lattice (P1, see
              roadmap-particle-layer.md): exact quantum numbers,
              derived force matrix, particle/photon_sourced/
              gluon_sourced channels + particle_readout observer      <- new
  analysis/   summaries, exactness table, inventory generator          <- new
  io/         YAML scenario loader, JSON result writer                 <- new
  verify.py   canonical fidelity/exactness checks (one source)         <- new
  viz/        re-export: viz, tick_heatmap
  gui/        render.py (numpy) + app.py (vispy+Qt, engine-driven)     <- new
  cli.py      entry point: run/resume/analyze/inventory/list-channels/gui
```

## Testing & exactness inventory (Phase F)

`casim.verify` holds the canonical checks; `tests/` asserts them under pytest
(markers `exact` / `machine_precision` / `slow`) or standalone
(`PYTHONPATH=src python tests/test_casim_exactness.py`). `casim inventory`
regenerates `test-results/casim-exactness-inventory.md` (scoped to the engine;
it does not touch the repo's hand-maintained `docs/status/exactness-inventory.md`).

### Unified scaled suite — `casim test` (Phase F+)

`casim test` (package `casim.suite`) runs the whole repo's runnable tests in
**groups** (`battery` = the correctness gate — hybrid pytest **+** standalone
`main()` scripts, classified per file; `scenarios`; `realspace`) with
**periodic reporting**, at a **scale tier** (`smoke`/`10x`/`100x`/`1000x`) — i.e.
orders of magnitude over the shipped sandbox sizes. The `realspace` group grows
the *represented physical patch* (the block-spin factor, F129–F133) so a
tractable super-cell lattice stands in for proton/neutron/atom-scale physical
cells. Long runs are chunked (heartbeat) and resumable (`--checkpoint-every` →
`casim resume`); the JSON+Markdown report is rewritten after every item so a
native run is inspectable mid-flight. Full reference: `scenarios/SUITE-GUIDE.md`.

## Backend seam (Phase G)

Spectral work routes through `casim.lattice.backend` (`fftn/ifftn/…` and a
`chiral_transform` hook). The default delegates to the audited `ca_fft`; swap in
numba/GPU or a hand-written chiral library with `backend.register_backend(...)`
+ `backend.use(name)` — no physics-code changes. **F134** validates the seam: a
second `numpy_fft` backend is identical to `ca_fft` to round-off (the regression a
GPU backend must pass), and `casim.lattice.chiral_core` is a verified hand-rolled
chiral core (explicit real/imag arithmetic, no `np.linalg`) registered through the
`chiral_transform` hook — matching the audited Weyl/W± kernels bit-for-bit.

## Channels (F91 propagator classification)

| type | propagator | kernel |
|---|---|---|
| `photon_pair` | even (forced) | `ca_photon_pair.photon_step_spectral` |
| `weyl_bcc` | per-branch | `ca_bcc.weyl_step_3d_bcc` |
| `w_chiral` | chiral (forced) | `ca_wmu.w_propagation_step_chiral` |
| `z_even` | even | `ca_z_field.z_propagation_step_spectral` |
| `gluon_bcc` | even (forced, F91) | `ca_gluon.gluon_rotation_step_spectral_bcc` |
| `gravity_dielectric` | dielectric K renorm (F64) | `poisson_open` + K=exp(2GM/rc²) |
| `w_sourced` + `fermion_doublet` | coupled (Tier-2) | `ca_wmu` sourced W + covariant Weyl (E2E) |
| `beta_decay` | chiral (Tier-2) | `ca_charged_current.emit_w_minus` + Proca |
| `charge_photon` | even (Tier-2) | `ca_charge_coupling.maxwell_curl_step` |
| `gauge_mc` | monte-carlo (Tier-3) | `lgt_fork_A_mc.heatbath_sweep` (SU(3) MC) |
| `particle` | per-branch (particle layer) | `weyl_step_3d_bcc` / `covariant_weyl_step_3d_bcc` + derived force matrix |
| `photon_sourced` | even (particle layer) | `ca_charge_coupling.maxwell_curl_step` ← particle `J_em` |
| `gluon_sourced` | even (particle layer) | `ca_gluon.gluon_sourced_step_bcc` ← quark `J_colour` |
| `refraction_2d` | variable-c (Tier-3) | `ca_curved.weyl_step_2d_varc_strang` (needs SciPy) |
| `njl_meson` | spectral (compute-once) | `ca_meson.solve_meson_spectrum` (pion/σ χSB sector, FB03) |
| `njl_nucleon` | spectral (compute-once) | `ca_si_scale.si_registry` (f_π-anchored 3m_c + n−p, FB02/FA06) |
| `string_tension` | spectral (compute-once) | `ca_qcd_scale_ratio.summary` (√σ/f_π, FB09) |

The three `spectral` channels (`casim.engine.spectral_matter`) wrap the
momentum-space matter solvers for the falsification suite: a "tick" runs the
solve once and the `field_snapshot` observer dumps the physics numbers + PDG
comparison to JSON. Scenarios: `njl_pion.yaml`, `njl_nucleon.yaml`,
`string_tension_fpi.yaml`.

## Coupled channels (Tier-2)

`Channel.step(state, lattice, context)` receives the engine's live
`{name: state}` map; channels step in registration order, so a field channel
can source from a partner matter current and act back within one tick. See
`casim.engine.coupled` and `scenarios/fermion_w_backreaction.yaml`. Independent
channels ignore `context` and stay bit-identical.

## Block-spin / physical patch (Phase 4, F133)

A run can declare a **physical patch size and a block factor** so a tractable
lattice of `L` super-cells represents `(L·block)^d` physical cells (the
coarse-graining substitution the scale roadmap rests on). The light speed
`c_lat` is the RG fixed point (F130), carried through unchanged.

```yaml
lattice: {physical_patch: 64, block: 4}    # → 16 super-cells, patch = 64 cells/axis
blockspin: [{at: 50, factor: 2}]           # coarse-grain the LIVE run at tick 50
```

`Simulation.block_spin(b)` applies the block-spin transform R_b in place
(grouping `b^dims` super-cells into one), shrinks `L → L/b`, accumulates the
block factor, and keeps the physical patch invariant — an adaptive-resolution CA
step. The even-law channel then propagates by the renormalised rule
Ω(κ/block) (`engine.blockspin.renormalized_even_step`), faithful in the IR
(`[R_b, evolution] = 0` on band-limited fields). Per-channel R_b is complex-safe
for spinors and uses the log rule for the gravity dielectric (A·B≡1). See
`scenarios/blockspin_photon.yaml`.

## Checkpoint / resume

A scenario may declare `checkpoint: {every: N, dir: checkpoints}`; the engine
drops an NPZ snapshot (all channel states + tick + RNG state + observer records)
every N ticks. `casim resume <snapshot.npz>` rebuilds the run and continues —
bit-identical to an uninterrupted run. This is how long jobs that exceed the
sandbox time limit are run: checkpoint, resume, repeat.

## Field dumps for visualisation (`field_dump`)

The engine never imports a renderer. The `field_dump` observer writes real 3-D
volumes to disk and any frontend reads them afterwards — ParaView, PyVista,
napari, or plain numpy. Full rationale in `docs/design/visualization.md`.

```yaml
observers:
  - {type: field_dump, every: 10, format: vti, stride: 2, max_mb: 256}
```

Writes `test-results/fields/<run>/<channel>_t000010.vti` per tick per channel,
plus a `<channel>.pvd` collection that opens the whole run as a ParaView time
series. Keys: `dir`, `channels` (filter), `format` (`vti` | `npz` | `both`),
`components` (also dump raw fields, default off), `stride` (spatial downsample),
`precision` (`float32` | `float64`), `max_mb` (write budget; dumping halts when
exceeded).

Always written: `density` — the channel's `density_field`, the same volume the
GUI point cloud renders, so file and live view cannot disagree. With
`components: true`, spinors additionally appear as `f_re`/`f_im`/`g_re`/`g_im`
and gauge fields as `E`/`B`. **Complex arrays are never written implicitly** —
`casim.io.vtk` refuses them, because a renderer that silently drops Im(ψ) yields
a plausible wrong picture (CLAUDE.md's caution on chiral transforms). Channels
with no spatial volume (compute-once spectral solves, the 2ⁿ many-body register)
are skipped and listed in the observer summary rather than failing the run.

Caveat: ImageData is a uniform grid, so a BCC lattice is written with cubic
indexing — exact for every array-indexed field, but geometric BCC sublattice
offsets are not applied. Topology travels in the sidecar metadata.

## Adding a scenario

```yaml
name: my_run
lattice: {L: 32, topology: bcc, c_lat: 0.5773502691896258}
seed: 7
ticks: 200
channels:
  - {type: weyl_bcc, sign: "+"}
observers:
  - {type: dispersion_fit, every: 200}
  - {type: norm_conservation, every: 10}
output: {json: test-results/my_run.json}
```

## Verifying engine fidelity

`tests/test_engine_reproduces_kernels.py` asserts the engine reproduces the raw
kernels **bit-for-bit** given the same seed — the roadmap's acceptance gate
before any legacy script is deleted.
