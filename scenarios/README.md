# Scenarios

Each YAML here is a reproducible run: `casim run scenarios/<name>.yaml`.
One driver + a committed config + seed reproduces a historical run; every
scenario is verified bit-identical to its raw `ca-simulation` kernel in
`tests/test_engine_reproduces_kernels.py`.

| scenario | channel | propagator (F91) | topology | what it checks |
|---|---|---|---|---|
| `photon_pair.yaml` | `photon_pair` | even (forced) | cubic | real, norm-conserving even-law (E,B); pair dispersion = even rate (F69) |
| `bcc_weyl.yaml` | `weyl_bcc` | per-branch | bcc | exact-unitary Weyl walk; norm floor, ‖U†U−I‖, dispersion (F49 substrate) |
| `w_chiral.yaml` | `w_chiral` | chiral (forced) | cubic | chirally-faithful F37 W propagation; norm conservation |
| `z_even.yaml` | `z_even` | even | cubic | massless Z = even γ-law on a single (E_Z,B_Z) pair |
| `gluon_bcc.yaml` | `gluon_bcc` | even (forced, F91) | bcc | octet BCC even-law gluon; **+ checkpoint every 50 ticks** |
| `gravity_deflection.yaml` | `gravity_dielectric` | dielectric K (F64) | cubic | eikonal light bend = GR 4GM/(c²b) (finite-aperture) |
| `fermion_w_backreaction.yaml` | `w_sourced` + `fermion_doublet` | coupled (Tier-2) | bcc | closed fermion↔W loop: current sources W, W acts back via SU(2) links (E2E B1) |
| `beta_decay.yaml` | `beta_decay` | chiral (Tier-2) | bcc | F54 d→u+W⁻ vertex emission + massive-Proca propagation |
| `charge_photon.yaml` | `charge_photon` | even (Tier-2) | cubic | F87 sourced paired-photon Maxwell curl, divergence-free charge current (odd L) |
| `gauge_mc.yaml` | `gauge_mc` | monte-carlo (Tier-3) | cubic (4D) | F94 SU(3) lattice-gauge heat-bath MC; tick=sweep; thermalises, checkpoints |
| `refraction_2d.yaml` | `refraction_2d` | variable-c (Tier-3) | cubic (2D) | F64 time-domain variable-c packet refraction (Snell); **needs SciPy** |
| `photon_beam_all_fields.yaml` | `photon_pair` (init: beam) + `w_chiral` + `z_even` + `gravity_dielectric` | even (forced) | cubic | travelling γ beam along +x through all live cubic fields: beam speed = dΩ_pair/dk\|k0 (− diffraction ≈ 1/(2(k0σ⊥)²)), per-channel norm conservation, Tier-1 non-interaction (bit-identical to γ-only run) |
| `bcc_fields_companion.yaml` | `weyl_bcc` + `gluon_bcc` + `gravity_dielectric` | per-branch / even | bcc | companion: the BCC-only fields (can't share the photon's cubic lattice) coexisting — norms, exact Weyl unitarity, dispersion |

**Tier-3 channels** are non-unitary or heavy. `gauge_mc` is stochastic — a tick
is one Monte-Carlo sweep drawing from the engine's (checkpointed) RNG, so a long
thermalisation can be stopped and resumed and the Markov chain continues
bit-for-bit. `refraction_2d` needs SciPy (`ca_curved`); run it where SciPy is
installed, or verify with `tools/verify_tier3_gravity.py`.

**Tier-2 coupling.** Channels listed in a scenario step in order; each sees its
siblings' live states via the engine's coupling context. Order matters for
coupled pairs — in `fermion_w_backreaction`, `w_sourced` is listed first so it
consumes the pre-tick fermion current and publishes the updated potential for
the fermion's covariant step that same tick.

## Checkpoint / resume

`gluon_bcc.yaml` declares `checkpoint: {every: 50, dir: checkpoints}`; a run
drops `checkpoints/gluon_bcc_t{50,100,150}.npz`. Resume any of them:

```bash
casim resume checkpoints/gluon_bcc_t50.npz --ticks 150 --out test-results/resumed.json
```

A resumed run is bit-identical to an uninterrupted one (state, RNG, and observer
records all restored) — this is the mechanism for long runs that exceed the
sandbox time limit.

## Scenario schema

```yaml
name: <str>
lattice: {L: int, dims: 3, topology: cubic|bcc, c_lat: float}
seed: int
ticks: int
channels:  [ {type: <registered channel>, ...channel kwargs} ]
observers: [ {type: <registered observer>, every: int, ...} ]
checkpoint: {every: int, dir: path}        # optional
output: {json: path}                        # optional
```

Run `casim list-channels` for the live channel/observer registry.
