# casim suite guide — `casim test` (user-run, grouped, scaled)

`2026-06-16 - 19:14`

`casim test` is the **user-run** harness that runs the whole repo's runnable
tests in **groups**, with **periodic reporting**, at a chosen **scale tier** —
several orders of magnitude over the shipped sandbox sizes. It complements
`RUN-GUIDE.md`: that guide is for running one scenario; this one runs the whole
battery + every scenario + the real-space block-spin patches in one driver.

```bash
# dry-run: print the plan (sizes, cost factor, memory estimate) and exit
casim test --list --scale 1000x

# run everything at 10× (battery gate + scenarios + real-space patches)
casim test --scale 10x

# a long native production run, resumable, with a heartbeat every 30 s
casim test --scale 1000x --report-every 30 --checkpoint-every 100

# just the real-space proton/neutron/atom patches at 100×
casim test --scale 100x --groups realspace
```

Without an editable install: `PYTHONPATH=src python -m casim.cli test ...`.

Exit code is non-zero if any item is `FAIL` or `ERROR` (CI-friendly).

## Groups

| group | what it runs | scaled by the tier? |
|---|---|---|
| `battery` | the correctness battery — `tests/casim`, `tests/priority`, `tests/findings` | **no** — these assert algebraic/machine-precision exactness; they are the pass/fail *gate*, not a scale knob. `CASIM_SCALE` is exported so scale-aware tests/scripts can opt in. |
| `scenarios` | every committed CASIM YAML scenario, re-run at the tier's `L`/`ticks` | **yes** — `cost = L^dims × ticks` |
| `realspace` | the block-spin / real-space patches (proton, neutron, hydrogen, photon carrier) | **yes** — the tier grows the *represented physical patch* (the `block` factor), holding the tractable super-cell `L` fixed |

Default groups: `battery,scenarios,realspace`.

### The battery is hybrid (pytest **and** standalone scripts)

The repo's tests come in two shapes, so the battery auto-classifies every file
in each group dir and runs it the right way:

- **pytest-collectable** (defines a `test_` function or `Test` class — e.g. all
  of `tests/casim`, ~54 of `tests/findings`): run together in one `pytest`
  subprocess per group, results parsed from JUnit XML. If `pytest` is not
  installed these files report `SKIP` (the suite does not error), and the
  standalone scripts still run.
- **standalone scripts** (a `main()` + `__main__`, no `test_` functions — e.g.
  all 16 of `tests/priority`, ~100 of `tests/findings`): run as
  `python <file>`. Status comes from the **exit code** (non-zero → `ERROR`) and
  the **PASS/FAIL tokens the script prints** for its own gates: any `FAIL`/`❌`
  → `FAIL`; otherwise ≥1 `PASS`/`✅` → `PASS`; clean exit with neither → `RAN`.
  Each script is its own report row (`battery/priority::test_09_GR4_mercury`),
  so a failure is pinpointed. `--script-timeout` (default 900 s) caps each;
  `--no-scripts` runs only the pytest portion.

> A standalone script reporting `FAIL` means *that script's own scientific gate*
> did not pass at its committed parameters — it is the script talking, surfaced
> faithfully, not a harness error.

## Scale tiers

`cost = L^dims × ticks` (the RUN-GUIDE law). A tier is a pair of multipliers
chosen so a typical 3-D scenario lands near a target cost decade:

| tier | L× | ticks× | ~cost | real-space patch× | use |
|---|---|---|---|---|---|
| `smoke` | 1.0 | 1 | 1× | 1× | sandbox / dev-smoke gate (shipped YAML sizes) |
| `10x` | 1.6 | 2.5 | ~10× | 2× (→ ~8× cells) | quick scaled check |
| `100x` | 2.5 | 6.5 | ~100× | 4× (→ ~64× cells) | workstation |
| `1000x` | 4.0 | 16 | ~1000× | 8× (→ ~512× cells) | big native production run |

Per-scenario guards live in `src/casim/suite/tiers.py` (`OVERRIDES`):

- **`gauge_mc`** is 4-D (`cost = L^4`); `L` is capped per tier and the scale is
  carried by sweeps (ticks), per RUN-GUIDE (production ceiling ~`L=16`).
- **`charge_photon`** is forced to odd `L` (curl stencil).
- **`refraction_2d`** is 2-D (`cost = L^2`) so it takes a larger `L` per tier.
- the **spectral compute-once** falsification scenarios (`njl_pion`,
  `njl_nucleon`, `string_tension_fpi`) are size-invariant → `SKIP` above smoke.
- **static eikonal** (`gravity_deflection`) scales the Poisson grid only.

`--list` prints the resolved `L`/`ticks`/`block`, the represented vs compute
cell counts, the cost factor, and a (conservative) memory estimate per item, so
you can pick a tier that fits your machine before committing to a run. Use
`--mem-gb G` to auto-skip any scenario whose projected footprint exceeds `G`.

## Real-space block-spin tiers (proton / neutron / atom)

A literal real-space fill is permanently off the table — at the canonical ruler
(F107, `a = 6.5978 ℓ_P`) a proton is ~1.6×10¹⁹ cells across, a hydrogen atom
~5×10²³ (roadmap-scale-to-real-space §0). The real-space scenarios instead
declare a **physical patch** via the block-spin factor (F129–F133): `L`
super-cells *represent* `(L·block)^dims` physical cells, and the suite's
real-space tiers **grow `block`** so the represented physical volume climbs by
orders of magnitude while the compute lattice stays fixed.

| scenario | object | binding mechanism | base |
|---|---|---|---|
| `realspace_photon_patch` | free photon | even-law carrier, the F133-proven-faithful R_b case (with a live coarse-graining event) | patch 32³, block 2 |
| `realspace_proton_1fm` | proton (uud) | live colour-dielectric bag (F137); FA06/F40 isospin split (d heavier by the 2.51 MeV current-mass gap; fractional charges + photon Coulomb, net +1) | patch 32³, block 2 |
| `realspace_neutron_1fm` | neutron (udd) | live colour-dielectric bag (F137); FA06/F40 isospin split (two heavy d → m_n>m_p; net 0, EM self-energy cancels) | patch 32³, block 2 |
| `realspace_hydrogen_bohr` | hydrogen (p,e) | uud↔gluon confinement loop + (p,e) Coulomb α + F64 gravity | patch 32³, block 2 |

These name the object and report the represented-cell count honestly; **no SI
fm/cell is asserted** — absolute fm/eV remain P6/scale-gated (F123), exactly as
in `unified_hydrogen.yaml`. Structure and loop-consistency are the deliverable.

## Output & periodic reporting

Each run writes to `test-results/suite/<scale>_<timestamp>/` (gitignored):

- `suite_report.json` / `suite_report.md` — rewritten **after every item** and
  every group, so a multi-hour native run is inspectable mid-flight; the header
  reads `IN PROGRESS` until the final flush marks it `COMPLETE`.
- `scenarios/<name>.json` — each scenario's full results JSON (the existing
  schema; never clobbers the committed `test-results/*.json`).
- `junit/battery_<group>.xml` — raw pytest JUnit output per battery group.
- `checkpoints/` — NPZ snapshots when `--checkpoint-every` is set.

During long scenarios a heartbeat line (`… name: tick k/N (p%)`) prints every
`--report-every` seconds (long runs are driven in tick-chunks for this).

## Resuming a job that exceeds a wall-clock cap

Set `--checkpoint-every N`; each scenario drops a resumable NPZ every `N` ticks.
A single interrupted scenario can be continued with
`casim resume <snapshot.npz> --ticks <target>` (bit-identical to an
uninterrupted run). This is the same checkpoint/resume path documented in
`src/casim/README.md`.

## Flags

| flag | default | meaning |
|---|---|---|
| `--scale` | `smoke` | `smoke` \| `10x` \| `100x` \| `1000x` |
| `--groups` | `battery,scenarios,realspace` | comma list |
| `--only` | (all) | comma list of scenario names to restrict to |
| `--out` | `test-results/suite/<scale>_<stamp>` | report dir |
| `--report-every` | `15` | seconds between progress heartbeats |
| `--checkpoint-every` | `0` (off) | NPZ checkpoint cadence (ticks) |
| `--mem-gb` | (off) | skip scenarios whose projected footprint exceeds this |
| `--script-timeout` | `900` | per standalone battery-script timeout (s) |
| `--no-scripts` | — | battery: run only pytest-style files, skip standalone scripts |
| `--list` | — | dry-run: print the plan and exit |
