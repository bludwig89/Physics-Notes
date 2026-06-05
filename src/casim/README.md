# casim — standalone modeling program (roadmap Phases A–C)

`casim` is the program layer over the audited `ca-simulation/` physics kernels.
It is a **refactor, not a rewrite**: the flat `ca_*.py` modules remain the single
source of truth and keep working unchanged; `casim` adds the engine,
configuration, persistence, and entry point described in
`roadmap-standalone-program.md`.

## Install

```bash
pip install -e .            # needs setuptools>=64 (PEP 660)
pip install -e .[gui]       # + vispy/PyQt6 for the (Phase E) GUI
```

`casim` finds the repo's `ca-simulation/` directory automatically; override with
the `CASIM_LEGACY_DIR` environment variable if needed.

## CLI

```bash
casim list-channels                         # registry + F91 propagator class
casim run scenarios/photon_pair.yaml        # run a scenario, write JSON
casim run scenarios/bcc_weyl.yaml --ticks 500 --seed 1
casim resume checkpoints/gluon_bcc_t50.npz --ticks 150   # continue a long run
casim analyze test-results/casim_bcc_weyl.json --table
casim inventory                             # run checks, regenerate exactness table
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
it does not touch the repo's hand-maintained `exactness-inventory.md`).

## Backend seam (Phase G)

Spectral work routes through `casim.lattice.backend` (`fftn/ifftn/…` and a
`chiral_transform` hook). The default delegates to the audited `ca_fft`; swap in
numba/GPU or a hand-written chiral library with `backend.register_backend(...)`
+ `backend.use(name)` — no physics-code changes.

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

## Coupled channels (Tier-2)

`Channel.step(state, lattice, context)` receives the engine's live
`{name: state}` map; channels step in registration order, so a field channel
can source from a partner matter current and act back within one tick. See
`casim.engine.coupled` and `scenarios/fermion_w_backreaction.yaml`. Independent
channels ignore `context` and stay bit-identical.

## Checkpoint / resume

A scenario may declare `checkpoint: {every: N, dir: checkpoints}`; the engine
drops an NPZ snapshot (all channel states + tick + RNG state + observer records)
every N ticks. `casim resume <snapshot.npz>` rebuilds the run and continues —
bit-identical to an uninterrupted run. This is how long jobs that exceed the
sandbox time limit are run: checkpoint, resume, repeat.

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
