# Review — `particles_first_gen` to t13162 (L=32 BCC)

`2026-06-05 - 22:50`

Source: `checkpoints/particles_first_gen_t13162.npz` → exported with
`casim export ... --stride 10` to `test-results/export_particles_t13162.json`
(468 KB; 1316 observer records each, every 10 ticks).

## Verdict

Matter sector is **healthy and exact**; one field channel (`photon_field`) is
**numerically diverging** — a propagator-choice bug, not a physics result.

## What is correct

| channel | reading | status |
|---|---|---|
| `electron` (lepton doublet) | norm = 2.000000000004 — drift **2.2e-12** over 13,162 ticks | ✅ machine-precision unitary |
| `u_quark` | norm = 1.0000000000002 — drift **2.0e-13** | ✅ machine-precision unitary |
| `gmass` (F64 gravity) | static background, drift 0; K_max = 23.8; eikonal deflection 3.32 vs GR-finite-aperture 4.58 (rel 0.27) | ✅ static; deflection gap expected at L=32 / b=5 (coarse, small impact parameter) |
| `w_field` | energy rises 0.01 → ~69 then **plateaus** (69.25 → 69.28 → 69.25 at t≥12k) | ✅ saturating, bounded — rotation-law propagator |
| `gluon_field` | energy rises ~linearly to 441 | ⚠️ expected for P1 source-only coupling (no back-reaction sink → steady energy injection); polynomial, not unstable |

The unitary cores do exactly what they should: the electron and u-quark
wavepackets stay norm-exact to 1e-12/1e-13 across 13k ticks while moving around
the periodic L=32 box, and the gravity dielectric stays a fixed background.

## The bug: `photon_field` exponential blow-up

```
tick     810   photon energy = 6.2e0
tick    1610                 = 1.6e8
tick    4010                 = 1.7e31
tick    8010                 = 6.7e69
tick   13110                 = 1.3e119
```

Constant exponential growth: energy ∝ 10^(0.0096·t), i.e. amplitude grows
**~1.1 % per tick** (eigenvalue magnitude > 1). This is a classic explicit
finite-difference instability, not physics.

**Root cause.** `PhotonSourcedChannel.step` propagates with
`ca_charge_coupling.maxwell_curl_step` — the *explicit linearized-Maxwell curl*
update (E += dt·curl B − J; B −= dt·curl E). Per F25/F26 and CLAUDE.md design
decision #5, the curl equations are only the **first-order Taylor linearization
of the exact unitary (E,B) rotation law**; the explicit curl scheme is only
conditionally stable, and under continuous current sourcing over thousands of
ticks it diverges. The other two sourced fields avoid this because they use the
**even rotation-law propagator** (`w_sourced` and `gluon_sourced` both do
`rotation_step (unitary) + source kick`), which is why `w_field` plateaus and
`gluon_field` only grows linearly while `photon_field` explodes.

## Recommended fix (one change, its own task + test)

Re-point `PhotonSourcedChannel` from `maxwell_curl_step` to the audited
even-law paired-photon propagator (`ca_photon_pair.photon_step_spectral` /
`ca_wmu._f26_rotation_step`) followed by the same real-space source kick the
gluon/W channels use:

```
E_rot, B_rot = photon_step_spectral(E, B)     # exact unitary rotation
E = E_rot + g_em * J * dt                       # source injection
```

This matches the canonical photon (F67/F68/F69 even law), is unconditionally
stable (the free part is a rigid rotation, norm-exact), and brings the photon
channel in line with the W and gluon. The matter sector and all 22 particle-
layer tests are unaffected.

> Note: this is the long-run confirmation of the F26 thesis from the program
> side — the curl equation and the rotation law agree at small k / few ticks
> (which is why the smoke run at t=60 looked fine) but diverge under sustained
> evolution; only the rotation law is stable.

## Resolution (2026-06-05 - 23:10)

Fixed. `PhotonSourcedChannel` re-pointed from `maxwell_curl_step` to
`ca_photon_pair.photon_step_spectral` (even rotation law) + source kick. Photon
energy is now bounded — 43.7 at t=2000 vs ~10^19 for the retired curl step at
the same point — with electron norm exact. New regression test
`test_P5_1_sourced_photon_long_run_bounded` (2000-tick sustained drive) locks
it; particle-layer suite 23/23, engine-fidelity 13/13. See changelog
2026-06-05 23:10.
