# Script → scenario migration map

2026-06-04 - 21:50

Status of converting the 97 `model-tests/` scripts into `casim` scenarios
(roadmap Phase D, "migrate remaining run scripts as scenarios").

## Reality of the corpus

Of the 97 scripts, **34 contain a propagation step loop** (a `for`-loop over a
`*_step` kernel) — these are the genuinely run-loop-style simulations that map
onto the engine's `Simulation` + channels + observers model. The other **~63 are
analytic / algebraic derivations** (closed-form dispersion checks, group-theory
counting, Koide/NJL algebra, lattice-gauge Monte-Carlo). Those do not have a CA
tick loop, so they are **not** scenarios; they belong in the Phase F pytest
conversion as marked unit tests, run directly.

This is why "migrate remaining run scripts" is bounded: only the run-loop subset
becomes scenarios. The analytic scripts keep running unchanged (the legacy
modules are untouched).

## Channels now available (the propagating field content)

| channel | propagator | kernel | covers scripts like |
|---|---|---|---|
| `photon_pair` | even (forced) | `photon_step_spectral` | F67, F69, F72, F89, FG6, su2_photon_bridge |
| `weyl_bcc` | per-branch | `weyl_step_3d_bcc` | bcc dispersion/norm in run_qca_verifications, P0 fermions |
| `w_chiral` | chiral (forced) | `w_propagation_step_chiral` | F37, wmu_phase2/3, f26_rotation_law |
| `z_even` | even | `z_propagation_step_spectral` | FG4 dynamical-Z (free part) |
| `gluon_bcc` | even (forced, F91) | `gluon_rotation_step_spectral_bcc` | FG7 gluon dynamics (free part) |
| `gravity_dielectric` | dielectric K (F64) | `poisson_open` + K=exp(2GM/rc²) | F64 D-EM2 eikonal deflection |

All six are verified **bit-identical** to their raw kernels given the same seed.

## Migration tiers

**Tier 1 — done (free-propagation scenarios).** photon, Weyl, W, Z, gluon,
gravity-eikonal. Six scenarios in `scenarios/`, each bit-identical-verified.

**Tier 2 — DONE (sourced/coupled channels).** Implemented on an inter-channel
coupling hook (`Channel.step(state, lattice, context)`; the engine steps
channels in registration order and exposes siblings' live states). New
`casim.engine.coupled` channels, each bit-identical to its kernel:
`w_sourced`+`fermion_doublet` (the closed fermion↔W back-reaction loop, E2E B1),
`beta_decay` (F54 d→u+W⁻ vertex + Proca), `charge_photon` (F87 sourced
paired-photon Maxwell curl with a `C·J≡0` source). Scenarios:
`fermion_w_backreaction`, `beta_decay`, `charge_photon`.

**Tier 3 — DONE (non-unitary / heavy channels).** `casim.engine.tier3`:
`gauge_mc` — a 3+1D SU(3) lattice-gauge Monte-Carlo channel (`lgt_fork_A_mc`;
a tick = one heat-bath sweep, stochastic, drawing the engine RNG) covering
`run_lgt_confinement`/`run_confinement_mc`; pure numpy, bit-identical to the
fork and resumable (the Markov chain continues bit-for-bit). `refraction_2d` —
dynamical variable-c Weyl propagation (`ca_curved`) covering the F64 time-domain
deflection / `test_fork_D_doppler`-style refraction; exact-unitary but SciPy-
dependent, so lazy-imported and verified by `tools/verify_tier3_gravity.py`
where SciPy is installed.  To enable stochastic channels, `Channel.step` now
receives the engine's (checkpointed) `rng`.  Scenarios: `gauge_mc`,
`refraction_2d`.

**Stay as scripts (Phase F pytest).** All analytic derivations: F46, F47/F49,
F53–F61, F73–F80, F92, F93, etc. — no tick loop, so they become marked pytest
cases, not scenarios.

**All three migration tiers are now covered** by 12 registered channels; the
remaining scripts are the analytic-derivation set above.

## Acceptance

No legacy script has been deleted. Per the roadmap, a script is removed only
after its scenario reproduces the original JSON to machine precision; the
bit-identical kernel-fidelity tests are that gate for the six Tier-1 channels.
