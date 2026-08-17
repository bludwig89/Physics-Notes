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
| photon_beam_all_fields | 32 / 60 | 3.0 s | γ beam + W + Z + gravity (added 2026-06-06) |
| bcc_fields_companion | 16 / 60 | 0.7 s | weyl + gluon + gravity (added 2026-06-06) |
| gravity_dynamic_selfsourced | 24 / 60 | 2.5 s | two-way ψ↔K loop: massive packet sources its own dynamical dielectric (F106) and free-falls in it (F62 mix); F64 mainlined (added 2026-06-06) |

## gauge_mc after P2.5 (2026-07-31)

`gauge_mc` was the worst scenario in the suite and is not FFT-bound, so P2.1–P2.4
did nothing for it. P2.5 profiled it and changed the two things the profile named.
**Controlled A/B in one process, D=4, β=5.7, heat-bath only:**

| L | before | after | speedup | + reunit cadence 10 | speedup |
|---|---|---|---|---|---|
| 4 | 22.3 ms/sweep | 14.7 | **1.52×** | 13.8 | **1.62×** |
| 6 | 83.9 ms/sweep | 40.8 | **2.06×** | 37.8 | **2.22×** |
| 8 | 237.7 ms/sweep | 99.8 | **2.38×** | 91.6 | **2.59×** |

What changed, in profile order: `np.einsum('...ij,...jk->...ik')` → BLAS `zgemm`
via `casim.numerics.linalg.batched_matmul` (was **54%** of a sweep), and the
per-site SVD reunitarisation → Gram–Schmidt (`su3_reunitarise`, 13.4 ms → 2.4 ms,
**5.5×** on its own). `reunit_every` is now a **cadence** — `thermalise(...,
reunit_every=10)` reunitarises every tenth sweep, and unitarity still holds at
~3e-15 because the SU(2)-subgroup update is exactly unitary and only round-off
accumulates.

**The production ceiling moves L=12 → ~15, not to 16–20 as the roadmap hoped.**
Cost is $L^4$, so 2.4× buys $2.4^{1/4} = 1.24×$ in $L$. Reaching L=16 needs 3.2×
and L=20 needs 7.7×, and the remaining profile is 44% BLAS matmul (already
optimal in numpy), ~18% heat-bath RNG sampling, and a staple recompute that is
*physically required*. So the rest of that gap is a compiled or GPU path — P2.4's
problem, not P2.5's.

**Two roadmap items were measured and declined**, both recorded in the code:

- *"Reuse `staple_field` across parities"* — **wrong**. After the even half-sweep
  the odd-parity staples change by order 5.8 (the even ones by exactly 0), because
  a staple contains $U_\mu(x\pm\nu)$ at the opposite parity. Caching would use a
  stale staple for half of every sweep and break detailed balance.
- *"Eliminate the ~18 full-array `np.roll` copies via halo buffers"* — **not worth
  it**. `np.roll` measures at **7%** of a sweep; removing it entirely would give
  1.07× for a substantial refactor.

One test changed with this: **FA4** averaged a single Monte-Carlo chain, and any
bit-level perturbation re-rolls a chaotic trajectory. At HEAD's own code, 1 seed
in 8 already failed its 2.5% tolerance. It now averages 6 independent chains and
asserts statistical adequacy; the tolerance is unchanged. The physics is
untouched — ensemble mean 0.559021 ± 0.001411 vs 0.558816 ± 0.001271 at HEAD, a
**0.15σ** difference.

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

## Long runs — sizing, resuming, checkpoints (roadmap P2.6)

**Size it before you start it.** `--list` now prints a wall-clock estimate next
to the memory projection:

```bash
casim test --list --scale 1000x        # L, ticks, cost factor, ~GB, ~wall
```

The estimate is a **measured per-scenario anchor** (the table above) times the
computed cost ratio, with an `N log N` correction for the FFT-bound scenarios.
It is not a benchmark: the anchors are this sandbox, cache behaviour past L3 is
not modelled, and `gauge_mc` is not FFT-bound so its log correction is off. Treat
it as a lower bound with the right order of magnitude — enough to decide, not
enough to quote. A scenario with no anchor prints `?` rather than a guess.

**Resume instead of restarting.** A suite run that dies part-way used to restart
from item 1, and its timestamped `out_dir` meant it could not even find its own
checkpoints:

```bash
casim test --scale 1000x                    # dies at item 9 of 14
casim test --scale 1000x --resume           # picks up at item 10
casim test --scale 1000x --resume --redo=failures   # also re-runs non-PASS items
casim test --scale 1000x --resume --redo scenarios/gluon_bcc   # one item
```

`--resume` reuses the newest `test-results/suite/<scale>_*` directory (or the
`--out` you name) and treats the `suite_report.json` it already rewrites after
every item as the journal, so nothing extra is persisted and a resumed run keeps
the verdicts already earned.

**Checkpoints are now safe to kill.** Writes are atomic (temp file plus
`os.replace`), so a kill mid-write leaves the *previous* good snapshot intact
rather than a truncated file at the name the resume path looks for. They are
compressed by default and rotated — the newest three auto-checkpoints per run are
kept, ordered by tick rather than mtime, and an explicitly-named
`checkpoint(path)` is never rotated away. Tune with `Simulation(...,
checkpoint_compress=..., checkpoint_keep=...)`; `checkpoint_keep=0` disables
rotation.

> One bug worth knowing about if you have results from before 2026-07-31:
> `Simulation.resume()` did not restore the block-spin schedule, so **a resumed
> run silently skipped every remaining scheduled $R_b$ event** and still reported
> success. Any resumed real-space/block-spin result from before that date should
> be re-run.

## Handing results back to Claude

Always pass `--out test-results/<name>.json`. After a production run, Claude reads
that JSON directly and interprets it with:

```bash
casim analyze test-results/prod_gauge_mc.json --table
```

So the loop is: Claude validates small in-sandbox → Ben runs full native → Claude
reads the committed JSON and reports the physics. No timeout ever gates the science.
