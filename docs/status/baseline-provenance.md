# Baseline provenance — telling supersession apart from regression

*2026-07-31 - 10:40. Built after the C7.5 arming pass left 26 records failing on numeric drift and the obvious question had no mechanism behind it: **which of these numbers are wrong because something broke, and which are wrong because the model improved?***

## The gap

A committed `test-results/*.json` **is** the accepted value; C7's baseline diff fails when a run stops reproducing it. But a baseline that predates a model change looks exactly like one that just broke, and accepting a drift was a bare `git add` — no recorded reason, indistinguishable from accepting a regression.

The supersession ledger already carried provenance for **code** (`code:`) and **tests** (`tests:`). Artifacts were the missing third. So `baselines:` entries now hang off the supersession record whose physics moved, which puts the reason a number is out of date on the same object that records what replaced it.

## Three statuses, and only one changes a verdict

| Status | Meaning | `casim test` reports |
|---|---|---|
| `stale_by_design` | **Decided.** The numbers predate this supersession, so a re-run is *expected* to differ. | **`STALE`** |
| `candidate` | **Not decided.** Triage flagged it; the physics link is plausible but unread. | **`FAIL`**, unchanged |
| `live` | Re-blessed. `accepted_by` names the finding the numbers now encode; drift is a real regression. | `PASS` / `FAIL` |

**That asymmetry is the design, not an oversight.** If `candidate` suppressed failures the category would become a place to park inconvenient reds — precisely the failure mode P0.4 documented for file-level supersession claims, where an audit called 14 test files superseded and exactly one was. `tests/casim/test_supersession_ledger.py` asserts the asymmetry directly, because it is the one property of this mechanism that could quietly rot.

Two more rules with teeth, enforced by `casim.tests.ledger.validate()` and run in `make gate`:

- **All, not any.** A record whose drift spans one `stale_by_design` artifact and one undeclared artifact stays **red**. Reporting the whole record STALE would hide the live failure.
- **Every entry must be clearable.** A `stale_by_design` or `candidate` entry without `clears_by:` is rejected — an entry that cannot be cleared is a permanent excuse. A `live` entry without `accepted_by:` is rejected — a re-blessing needs an author.

## What the triage found

`tools/triage_baselines.py` joins the arming journal to the ledger: for each drifting record, does any ledger record name the findings its test claims?

| | count |
|---|---:|
| Drifting records | 29 |
| **Supersession candidates** (a ledger record names their findings) | **11** |
| **Regression candidates** (no ledger link — suspect the code) | **18** |

Eleven have `baselines:` entries now — one decided, ten as candidates:

| Artifact | Ledger | Status |
|---|---|---|
| `F62_dirac_gravity_fork.json` | S3 | **`stale_by_design`** |
| `F64_em_connection.json` | S4 | candidate |
| `F87_charge_coupling_paired_photon.json` | S1 | candidate |
| `F128_omega_repulsion.json` | S3 | candidate |
| `F181_covariant_interior_battery.json` | S4 | candidate |
| `F182_friedmann_pressure.json` | S4 | candidate |
| `F184_tabulated_ns.json` | S4 | candidate |
| `F200_alcubierre_structural.json` | S4 | candidate |
| `F240_omega_coupling_derivation.json` | S3 | candidate |
| `F241_omega_lambda_residual.json` | S4 | candidate |
| `FA_vs_FC_comparison.json` | S1 | candidate |

**Only F62 is decided, and it is the clearest case in the repo.** Its committed numbers *are* the two-leg rest-mass-sourced fork that S3 replaced — the artifact encodes D3a's self-redshift from ρ = |Ψ|², which F64 and then F178 superseded. A re-run drifts *because the mechanism changed*, so `FAIL` was the wrong verdict. And the fork is retained deliberately as the falsification record (roadmap §8), which is exactly why its baseline must not be re-blessed to look current. Verified end to end: `casim test --id F62-dirac-gravity-fork` now reports `STALE` naming S3, while `F241-omega-lambda-residual` — a candidate — still reports `FAIL`.

**Two candidates I flagged as weak on purpose.** `F128_omega_repulsion` and `F240_omega_coupling_derivation` came from the finding join, not from reading the physics; their `clears_by:` says to **delete the entry** if the link turns out spurious, because a wrong candidate is noise in a queue whose whole value is that it is short.

## Your decision queue

For each of the ten candidates: read the drifted values, then either

- promote to `stale_by_design` with the reason (the drift is the model improving), or
- leave the entry and fix the code (it is a regression), or
- delete the entry (the ledger link was spurious).

Highest value first, in my reading:

1. **`F182_friedmann_pressure` + `F184_tabulated_ns`** — the same physics question (pressure sourcing after F178's full T_μν) at two radii. One decision covers both.
2. **`F64_em_connection`** — F64 is the *superseding* side of S3, yet its own baseline predates S4's reclassification of F106. If the vacuum entries reproduce and only the interior moved, that is a clean `stale_by_design`, and it would confirm F178 keeps Schwarzschild in vacuum.
3. **`F87` + `FA_vs_FC_comparison`** — the photon-channel pair. 12 drifting values in a comparison table is a lot; suspect the harness as much as the physics.
4. **`F128` + `F240`** — decide whether the link is real at all.

The 18 regression candidates are a different job and want a code answer. `FG2`/`FG3` already have C5's analysis pointing at stale committed baselines rather than regressions, and `F192_vacuum_energy`'s baseline is from **today**, so suspect the code there first.

## P2.5 — three baselines changed deliberately (2026-07-31 - 21:10)

**These are not part of the queue above.** They are working-tree changes this
session made on purpose, and they are recorded here so that `git add`-ing them is
a decision with a reason attached rather than silent drift. Ben: accept all three
together, or none.

| Artifact | What moved | Why it is correct |
|---|---|---|
| `FA_lgt_mc.json` | 18 changed, **22 added** keys | FA4's protocol changed from **one** Monte-Carlo chain to an ensemble of **6**, adding `sem`, `sem_rel`, `per_chain` and a `statistics` block. Deliberate and strictly stronger — see below |
| `FG7_gluon_dynamics.json` | 3 residuals | BLAS reassociation. All three are **below the 1e-12 machine floor** in absolute value (7.1e-15→8.2e-15, 1.75e-13→1.14e-13, 2.6e-15→3.4e-16); the large *relative* numbers are noise-on-noise |
| `FG7b_gradient_flow.json` | 4 values | Same cause. Three are sub-floor (2.5e-14→2.1e-14 etc.). The fourth is the only one above the floor: `results[5].residual` 4.9418e-10 → 4.9421e-10, **relative 4.5e-5**, a 1–2 ULP matmul difference amplified through the gradient flow |

**Cause, in one line:** P2.5 routed `cooling._mm` from `np.einsum` onto
`casim.numerics.linalg.batched_matmul` (BLAS `zgemm`), which C1 already measured
and recorded as a **1–2 ULP, not bit-identical** change. Everything built on
`Re Tr` therefore moves in its last bits.

**Why FA4's change is not a loosened test.** As a single chain it was passing by
luck: measured at HEAD's own code over 8 seeds at β=5.7, |rel| ran 0.35%–**2.69%**
against a 2.5% tolerance, so **1 seed in 8 already failed**. A Monte-Carlo
trajectory is chaotic, so any bit-level perturbation re-rolls it. The tolerance is
**unchanged**; what changed is that the test now averages 6 independent chains and
*additionally* asserts that the standard error is 3× under the tolerance, so a
noisy ensemble fails as inconclusive instead of passing by luck.

**Proof the physics did not move:** ensemble mean over 10 seeds is
0.559021 ± 0.001411 with P2.5 against 0.558816 ± 0.001271 at HEAD — a **0.15 σ**
difference. The trajectory moved; the distribution did not.

Two further artifacts (`FG7c_confinement.json`, `FG7e_colour_condensate.json`)
were re-run and **restored to HEAD**: their only diffs were `elapsed_s` timings.

## Commands

```bash
python3 tools/triage_baselines.py              # the report above
python3 tools/triage_baselines.py --yaml       # paste-ready ledger entries
python3 tools/triage_baselines.py --undeclared # only the not-yet-recorded
casim test --id <record>                       # see STALE vs FAIL for one record
make registry                                  # counts, incl. stale vs candidate
```

*Cross-references: `docs/theory/supersessions.yaml` (`baseline_status_vocabulary` and the `baselines:` blocks), `src/casim/tests/ledger.py`, `tools/triage_baselines.py`, `docs/status/C7-completion-overview.md` §"C7 close-out".*
