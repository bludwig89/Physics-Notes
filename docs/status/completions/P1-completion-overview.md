# P2.1 + P1 Complete — Throughput and a Suite That Can Fail

*2026-07-30. Phases P2.1 and P1 of `docs/roadmaps/roadmap-unified-program.md`.
Follows `docs/status/P0-completion-overview.md`.*

`make gate` — 15 checks, 9.6 s.

---

## P2.1 — pyfftw

`ca_fft` has preferred pyfftw since it was written (`ca_fft.py:57-63`) and has
always exposed `set_workers` for it. pyfftw was never declared as a dependency,
so **every run in this project's history silently used single-threaded scipy**
while the module docstring advertised FFTW.

Three things changed:

1. **A real bug, found while wiring it.** The six pyfftw call sites never passed
   `threads=`, so even with pyfftw installed the FFTW path would have run
   single-threaded. `set_workers` was documented as applying to pyfftw and did
   nothing. Fixed, plus a 60 s plan-cache keepalive — without it every transform
   re-plans, which costs more than the threading gains.
2. **Declared as the `fast` extra**, not a hard dependency. pyfftw needs the
   FFTW C library and a platform wheel; making it required means a failed wheel
   build blocks `pip install -e .` entirely, turning a performance option into
   an availability risk. `make install` uses `.[fast,dev]`, and CI asserts the
   backend really is pyfftw so a missing wheel fails loudly.
3. **The fallback is no longer silent.** `casim backend [--bench]` reports and
   benchmarks the active library, and every `make gate` run prints it. A
   fallback you can see is a choice; one you cannot is a bug.

`tests/casim/test_fft_backend_equivalence.py` holds the contract every future
backend must meet, including the GPU backend in P2.4: all libraries agree to
1e-12 relative, round-trip is the identity, and **thread count cannot change the
result** — the specific regression risk introduced by wiring `threads=` through.

---

## P1 — the assertion deficit

### The core problem

232 of 344 test files contain no `assert`. They print `PASS`/`FAIL` tokens that
the runner scrapes from stdout; exit-0-with-no-token scores as `RAN`, which
reads like success. **70 files have no failure mode by any mechanism.**

### The fix, and why it did not require editing 173 files

The roadmap proposed a baseline harness with a new `tests/baselines/` directory.
On inspection that was unnecessary work: those tests already write their numbers
to `test-results/*.json`, and **those files are already committed to git**. So
HEAD *is* the baseline. No duplicate store to drift out of sync, and the
workflow for accepting a change is the one that already exists — read the diff,
`git add` it deliberately.

`src/casim/baselines.py` compares result payloads numerically:

- only numbers are compared; timestamps, paths, hostnames and durations are
  filtered by regex, not a literal list. The first run flagged `total_elapsed_s`
  as physics drift — exactly the false positive that trains people to ignore a
  checker;
- relative tolerance with an absolute floor, so a residual moving 1e-16 → 2e-16
  is noise and 1e-16 → 1e-6 is a finding;
- structural changes (a key appearing or vanishing) are reported separately from
  value changes, because they usually mean different things.

Wired into `runner.run_battery_script`, so any script that rewrites a result
artifact is now diffed against HEAD. **Drift outranks a printed PASS** — the
script's own gates can still be satisfied while a physical value has moved
underneath them.

Verified end to end: perturbing `B_F95` from `-5.69e-2` to `-5.72e-2` turned
`test_F234_Wvc_triple_closed.py` — which prints **6 PASS tokens and exits 0** —
into a `FAIL` naming the drifted quantity:

```
STATUS : FAIL
DETAIL : result drift vs HEAD — checks.C2_brake_from_derived_inputs
         .C_req_from_delta_and_B  0.03620112122936515 -> 0.03639198830087323
```

A third outcome was added alongside PASS/FAIL: a script with no assertion and no
token that **reproduced its committed numbers exactly** is now reported as a
genuine pass, with the reason stated. Only tests with nothing to diff at all
remain in `RAN`, and the detail text now says plainly that they have no failure
mode.

### The manifest (P1.4)

`test-results/manifest.json` replaces the prefix heuristic in
`regen_indexes.py`, which matched results to tests by filename prefix, capped at
two, left 104 of 339 index rows empty, and — looking in only one direction —
could not see an orphaned result at all.

Two bugs found building it:

- **The finding-ID regex never matched.** `\b(F[A-Z]?\d{2,3})\b` fails on
  `F107_canonical...` because `_` is a word character, so there is no boundary
  after `107`. That single character is why the old index resolved almost
  nothing by finding ID and fell back to guessing.
- **A naive finding-ID join produces 825 links**, because every test that merely
  mentions F107 in its docstring matches every F107 result. A mapping that says
  a result belongs to nine tests is not a mapping. Evidence is now ranked
  (declared-source → exact-stem → stem-prefix → declared-finding → finding-ID),
  the search stops at the first tier that matches, and a finding-ID match is
  only accepted when unique. Everything else is recorded as **ambiguous** — an
  honest state and a to-do, rather than nine wrong edges.

Also exploited: 117 result JSONs carry a `finding` key. An artifact naming its
own physics beats anything inferred from a filename.

| | before | after |
|---|---|---|
| links | 1,280 (fan-out) | 268 (237 by exact stem) |
| tests resolved to results | 234 | 241 |
| orphan results | 158 | 116 |
| ambiguous | not modelled | 30 |

### Tiers (P1.1)

| Tier | Contents | Invocation |
|---|---|---|
| `gate` | `tests/casim` — asserting, fast | `pytest`, `make gate` |
| `battery` | findings + priority + runners + scenarios | `casim test` |
| `archive` | fully-superseded files, from the ledger | excluded |

**`tests/runners` (45 files) is now in the battery.** It was in an opt-in
`numerical` group absent from `DEFAULT_GROUPS`, so nothing ever ran it. The
archive tier reads `docs/theory/supersessions.yaml` and excludes only
`fully_superseded` — the partially-superseded files keep running, because their
live checks are load-bearing.

Battery composition: 343 files (122 pytest-style, 221 scripts), 1 archived.

### Import-time side effects and the ratchet (P1.3)

**320 of 344 test files execute physics at module import**, so
`pytest --collect-only` runs the suite. Restructuring all of them is a long,
risky job that should not be done in one pass and should not be done without
baselines — which P1.2 has only just provided.

So P1.3 delivers the instrument and the ratchet rather than a rushed refactor.
`tools/audit_tests.py --ratchet` fails if any of three counts regresses past the
recorded high-water mark:

```
unfalsifiable        70   (no assert AND no result artifact)
import_time_work    320   (executes on --collect-only)
no_assert           232
```

Verified: adding one throwaway unfalsifiable test trips all three. The numbers
can now only move down, and `--list` prints exactly which files to fix.

### Exactness inventory (P1.5)

The roadmap wanted Tier 1/2/3 generated outright. **That is not yet honest.** A
survey of all 391 result JSONs finds the class vocabulary is not standardised:
`exact` (61), `machine-precision` (34), `machine` (31), `quantitative` (132),
plus `Tier-B`, `PREDICTION`, `structural`, and channel classes like `coupled`
and `background` that are not exactness classes at all. Only ~69 files record a
residual. Generating a table from that would produce a confident-looking
document with silent holes.

So `tools/gen_exactness_inventory.py` emits the **147 rows that are derivable
without guessing** into a marked generated section of the single inventory file,
states its coverage explicitly (147 classifiable of 530 residual entries; **383
unclassified and therefore invisible**), and leaves the hand tables
authoritative. Unifying the class vocabulary is the prerequisite for full
generation and is the tracked follow-on.

The staleness check produced the sharpest single number in this phase:

```
hand header      2026-06-11 / F140
newest finding   F265
FINDINGS BEHIND  125
```

---

## Acceptance gate

| Roadmap criterion | Result |
|---|---|
| Gate green in < 2 min | **PASS** — 15 checks, 9.6 s |
| Manifest resolves results to owning tests | **PASS** — bidirectional; orphans and ambiguity named rather than guessed |
| Perturbing a constant fails a named set of tests | **PASS** — `B_F95` perturbation flips a 6-PASS-token script to FAIL and names the quantity |
| No test in `RAN` limbo | **PARTIAL** — see below |

**The one criterion not fully met, stated plainly.** The roadmap asked that
every findings test either assert, diff a baseline, or be tombstoned, with zero
in `RAN`. The mechanism for all three now exists and is enforced, and the 241
tests with result artifacts have left limbo. But ~70 tests emit nothing at all,
so there is nothing to diff, and they can only be fixed by adding assertions —
file by file, with judgement about what each one actually claims. The ratchet
guarantees that number cannot grow. Reporting this as done would be the kind of
tidy-looking claim P0 was built to prevent.

---

## Files

**New**

```
src/casim/baselines.py                    numeric drift engine
tools/gen_manifest.py                     result <-> test <-> finding
tools/check_result_drift.py               drift report vs git
tools/audit_tests.py                      suite health + ratchet
tools/gen_exactness_inventory.py          derived rows + staleness
tools/test_health_baseline.json           the high-water mark
tests/casim/test_fft_backend_equivalence.py
test-results/manifest.json
```

**Modified**

```
pyproject.toml                 fast/dev extras
ca-simulation/ca_fft.py        threads= bug, plan keepalive, describe()
src/casim/cli.py               `casim backend [--bench]`
src/casim/suite/runner.py      runners group, archive tier, drift check
tools/run_gate.py              backend line + 3 health checks
Makefile                       install/backend/manifest/health/drift
.github/workflows/gate.yml     .[fast], pyfftw assertion
docs/status/exactness-inventory.md   generated section
```

---

## Note on your working tree

The drift checker's first real run flagged numeric movement in **your own
uncommitted changes** from before this session:

```
test-results/wmu_phase3.json
  ~ results[1].residual   0.08233760649393078 -> 0.08689495866462986   (5.2%)
  ~ results[1].slope      1.0105989763250631  -> 1.0022771475615901    (0.8%)
  ~ results[4].ym_action  11.703422910401915  -> 9.35434478408237      (20%)
test-results/wmu_phase4.json
  ~ results[4].residual   1.428e-13 -> 1.854e-13
test-results/FG7_gluon_dynamics.json
  ~ results[11].residual  7.105e-15 -> 8.216e-15
```

The two residual moves are at the FFT floor and are almost certainly noise. The
`wmu_phase3` slope and `ym_action` moves are not — a 20% shift in a Yang–Mills
action is a physics change. That is uncommitted work from your `ca_wmu.py` /
`ca_gluon.py` edits, so I have left all of it untouched. Worth a look before you
commit.

---

## Next

**P3.1** is the critical path: the BCC unification spike, which must be a
derivation before it is a port. Two smaller items that would pay for themselves
first: unifying the exactness class vocabulary (unblocks full P1.5 generation),
and working down the 70 unfalsifiable tests, now that the ratchet makes progress
visible and irreversible.
