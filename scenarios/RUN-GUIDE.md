# casim run guide — sandbox vs production

`2026-06-05 - 14:02`

Workflow split: **Claude runs reduced settings in the sandbox** (≤45 s per call) to
validate that a scenario passes and to time it; **Ben runs the full production
settings natively** with no wall-clock cap. Same scenario file, same seed, same
code path — only `L`/`--ticks` change, so a sandbox smoke and a production run are
the *same* experiment at two resolutions.

## The one knob that matters: `--L`

`casim run` now accepts a lattice-size override so size no longer requires editing
YAML:

```bash
casim run scenarios/<name>.yaml --L <edge> --ticks <n> --seed <s> --out <path.json>
```

`--L` overrides `lattice.L`; `--ticks`/`--seed`/`--out` override their scenario
fields. Omit a flag to use the value committed in the YAML.

Cost scales as **(volume) × (ticks)** = `L^dims × ticks`. For the 4D gauge MC that's
`L⁴`, so L is by far the dominant term — doubling L is 16× the work.

## Sandbox baseline (measured 2026-06-05, shipped sizes)

Every committed scenario already passes inside the sandbox at its default size; the
shipped YAMLs are effectively the dev/smoke tier.

| scenario | shipped L / ticks | sandbox wall | notes |
|---|---|---|---|
| photon_pair | 16 / 40 | 0.8 s | |
| bcc_weyl | 16 / 200 | 0.7 s | |
| w_chiral | 16 / 60 | 0.7 s | |
| z_even | 16 / 60 | 0.5 s | |
| gluon_bcc | 12 / 150 | 1.1 s | checkpoints every 50 |
| gravity_deflection | 64 / 0 | 0.3 s | static eikonal |
| fermion_w_backreaction | 8 / 20 | 0.5 s | coupled Tier-2 |
| beta_decay | 16 / 24 | 0.5 s | |
| charge_photon | 13 / 30 | 0.5 s | odd L required |
| refraction_2d | 128 / 80 | 1.3 s | needs SciPy |
| gauge_mc | 6 / 40 | 6.0 s | Tier-3 stochastic; L⁴ |

## gauge_mc scaling (the only one that hits the cap)

Measured / extrapolated on the `L⁴` curve at 40 sweeps:

| L | wall (40 sweeps) | where it runs |
|---|---|---|
| 6 | 6 s (measured) | sandbox ✓ |
| 8 | 17.7 s (measured) | sandbox ✓ (practical ceiling) |
| 10 | ~46 s | **production only** |
| 12 | ~95 s | production |
| 16 | ~300 s | production |

Sweeps scale linearly on top of this, so a production thermalisation (L=12,
400 sweeps) is on the order of ~15 min — fine natively, impossible in-sandbox.

## Recommended commands

**Sandbox smoke (Claude) — confirm pass + time:**

```bash
# representative: cheap everywhere
casim run scenarios/photon_pair.yaml --out test-results/smoke_photon_pair.json

# gauge MC at the sandbox ceiling
casim run scenarios/gauge_mc.yaml --L 8 --ticks 40 --out test-results/smoke_gauge_mc.json
```

**Production (Ben, native) — full size:**

```bash
# long SU(3) thermalisation, checkpointed & resumable
casim run scenarios/gauge_mc.yaml --L 12 --ticks 400 \
    --out test-results/prod_gauge_mc.json
# resume from a checkpoint if interrupted:
casim resume checkpoints/gauge_mc_t380.npz --ticks 400 \
    --out test-results/prod_gauge_mc.json

# high-res refraction (needs SciPy)
casim run scenarios/refraction_2d.yaml --L 512 --ticks 400 \
    --out test-results/prod_refraction.json
```

Adjust L/ticks to taste — the curves above let you predict wall time before
committing a long run.

## Handing results back to Claude

Always pass `--out test-results/<name>.json`. After a production run, Claude reads
that JSON directly and interprets it with:

```bash
casim analyze test-results/prod_gauge_mc.json --table
```

So the loop is: Claude validates small in-sandbox → Ben runs full native → Claude
reads the committed JSON and reports the physics. No timeout ever gates the science.
