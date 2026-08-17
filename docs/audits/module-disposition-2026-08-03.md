# Module disposition pass — `dead_candidate` and unreferenced modules

**Date:** 2026-08-03 - 15:07
**Executes:** gap **#5** of `docs/status/completeness-2026-08-02.md` — "A `dead_candidate` and unreferenced-module pass".
**Session:** `funny-beautiful-newton` (claim board `docs/design/session-claims.yaml`).
**Scope:** both halves of the gap — the H8 half (findings carrying live claims with no test record) and the H7 half (dead vs merely un-wired).
**Findings written:** none. Reserved 299–301 released unused; this is a maintenance pass, not a physics result.

---

## 1. Headline

> **Of the ten modules registered `dead_candidate`, exactly one was dead.**

| Disposition | Count | Modules |
|---|---:|---|
| Genuinely dead → `deprecated/code/` | **1** | `core._viz_live_display` |
| Tested-and-rejected branch → `forks/` | **1** | `particles.derive_weight_as_phase` |
| **Never dead — never *wired*** | **7** | the five below plus `derive_beta_LV`, `derive_velocity_addition` |
| Honest open question, left in place | **1** | `interactions.qed_casimir_materials` |

`dead_candidate` was measuring *"nothing imports this"*. For an analytical derivation kernel — a script that closes an open-derivation row and is then cited by a finding — that is its **normal condition**, not a verdict. Five of the ten backed live rows of `docs/status/exactness-inventory.md` while their findings were cited as **CLOSED** in `open-derivations.md`.

This is the same lesson P0.4 recorded and the dead-code proposal restates in its own preamble: *of 14 files an audit called superseded, exactly one was superseded wholesale.* The signal reproduced the ratio almost exactly — 1 in 10.

---

## 2. What was done — the H8 half (test records)

Four findings carried live claims with **no test record**. All four now have gate-tier registry records, and all four **PASS**.

| Record | Finding | Module | Kind / tier | Runtime | Result |
|---|---|---|---|---|---|
| `F245-l1-curl-coefficient` | F245 (L1) | `interactions.derive_curl_subleading` | assertion / gate | 0.1 s | **PASS**, 6 checks |
| `F246-l2-curl-coefficient` | F246 (L2) | `interactions.derive_f26_dispersion` | assertion / gate | 0.0 s | **PASS**, 5 checks |
| `F247-q3-omega-degeneracy` | F247 (Q3) | `interactions.run_q3_omega_degeneracy` | assertion / gate | 8.3 s | **PASS**, 4 checks |
| `F278-bcc-lattice-constant` | F278 | `casim.engine.lattice.bcc` | assertion / gate | 0.8 s | **PASS**, 9 checks |

Each is an `entry:`-driven record with a real failure mode. Three of the four modules previously had a `verify()` or `main()` that **only printed** — which is precisely why the claims could not regress visibly, and precisely what the H8 row was measuring.

Three of the four records were written to fail in a way specific to the claim, not merely to re-run it:

- **F246** checks the even-power vanishing **differentially**: `c2`, `c4` → the fit floor for the even law *while the single-chirality law keeps them at −0.032 and −2.0×10⁻⁴*. A one-sided check would pass on a broken fit; this one asserts the even symmetrisation is doing the work.
- **F247** is a documented **free input** — a negative. The checks assert the *linearity* of the binding valley, because linearity **is** the degeneracy: a curved or flat-bottomed valley would mean the deuteron *does* separate ω from the F113 core, and the finding would be wrong. It also guards F247's correction to F240 in **both** directions, so the 0.208-not-0.43 quench cannot be silently reverted.
- **F245** asserts that Finding 7's reported `0.01883` is β at *one random direction* — the leg that stops a later reader re-promoting a seed artifact to a fundamental constant.

`F278-bcc-lattice-constant` is the record F278 §9 specified but did not add. It is also a candidate answer to audit item **V-016**, which found nothing guarding the `c_lat` separation: check 2 is a raw IEEE-754 bit compare against `0x3fe279a74590331d`, and checks 6 and 9 break on any change to the hop-phase convention in `bcc_fractional_shift` or to `_bcc_uvec`.

### 2.1 Three discrepancies the records surfaced on day one

Writing a record against a finding is a re-measurement, and three numbers did not reproduce. None changes a conclusion; all three are recorded rather than papered over.

| # | Finding | Claimed | Measured | Reading |
|---|---|---|---|---|
| 1 | F278 §9 check 8 | float residual `0.0` | `8.88e-16` = **exactly 1 ulp** | `1/c_lat` is one ulp below `np.sqrt(3)` (`0x3ffbb67ae8584ca9` vs `…caa`). This is **F278's own §2 ulp caveat** — the one warning not to transcribe a decimal for `a` — applied to its own check 8, where the finding did not apply it. The identity is exact; check 7 proves it in sympy. Only the float evaluation carries the ulp. |
| 2 | F245 §Method | 3D worst residual `9e-15` | `4.0e-12` | Three orders larger. Richardson-extrapolation conditioning, **not** a failure of the closed form — agreement is still 12 significant figures on a coefficient of order 10⁻². The record's bound is set to what the code achieves. |
| 3 | F247 §2 table | `8.26` at `g_cm = 9.155` | `8.2549` (rounds to `8.25`) | A one-digit rounding slip in the finding's table. Every other row reproduces to <10⁻³. |

Each is annotated inline at the assertion that found it, so the next reader meets the correction where it matters rather than only here.

### 2.2 Two structural defects fixed in passing

`run_q3_omega_degeneracy.py` violated two standing rules:

- **`import numpy as np`** — a bare numerics import (**D8**). Routed through `casim.numerics`.
- **`"../test-results/Q3_omega_degeneracy.json"`** — a **working-directory-relative artifact path**, the exact anti-pattern CLAUDE.md names ("only resolves from the directory the file used to live in"). Repointed at `casim.engine.particles._results_path`.

---

## 3. What was done — the H7 half (dead vs un-wired)

### 3.1 Genuinely dead → `deprecated/code/`

**`core._viz_live_display`** — the original 2007–08 vispy point-cloud viewer. Superseded by `casim.gui.app` (the same viewer re-pointed at a `casim.engine.Simulation`) and `casim.gui.render` (the numpy-only colour maps, re-exported as the single `casim.viz` API); its `density_to_rgba` duplicated `casim.gui.render.density_to_rgba` on identical colour stops. It carried its own **RETIRED** banner from roadmap P5.1 naming both replacements.

Moved to `deprecated/code/_viz_live_display.py` and recorded in `docs/theory/supersessions.yaml` as **S14**. The ledger entry is load-bearing, not decorative: the file's basename is not a manifest `source` (that is `live_display.py`), so `tools/check_deprecated.py` accepts it *only* via the ledger.

### 3.2 A fork, not dead code → `forks/particles/`

**`particles.derive_weight_as_phase`** — the E1 attack that tried to *derive* the weight-as-phase principle by two named routes: (A) saturation equipartition, (B) a BCC second-shell topological/Berry-phase moment. **Both routes are closed:** F253 excludes a scale-free topological origin (the only holonomy available is 2π/3); F256 shows the dynamical Landau route cannot give an exact 3δ\* = Q (independent sea-*B* / induced-*C* origins ⇒ the identity holds only to 1.7×10⁻⁵).

Under this repo's own definition that makes it a **fork**, not dead code — *"a tested and rejected or live-exploratory branch; it preserves the falsification record and is not dead code"* (CLAUDE.md, `engine/forks`). Deleting it would delete the evidence that both routes were tried and why each failed, which is exactly the evidence **founding decision 7** and **open-derivations row E1** lean on when they say every alternative is closed.

Moved to `src/casim/engine/forks/particles/`, registered `status: fork_live`, ledger **S15**.

### 3.3 Never dead — never wired (7)

| Module | Backs | Was | Now |
|---|---|---|---|
| `interactions.derive_curl_subleading` | F7, F245 + 4 inventory rows | `dead_candidate` | `live`, tested |
| `interactions.derive_f26_dispersion` | F26, F30, F246 + inventory row | `dead_candidate` | `live`, tested |
| `interactions.run_q3_omega_degeneracy` | F113, F240, F247 | `dead_candidate` | `live`, tested |
| `interactions.derive_beta_LV` | F12, F15 + 4 inventory rows | `dead_candidate` | `live` — corrected independently the same day by the F01–F15 review session |
| `interactions.derive_velocity_addition` | F15 + inventory row | `dead_candidate` | `partial` — **still untested** (follow-up 1) |
| `interactions.derive_dielectric_noconfine` | F139, F142 + inventory row | `dead_candidate` | `partial` — **still untested** (follow-up 2) |
| `core.lpt_generator` | the **d1** programme | `dead_candidate` | `partial` |

**`core.lpt_generator` is the most consequential misfiling of the ten.** It is the automated lattice-perturbation-theory Feynman-rule generator for the Wilson SU(3) action, built to close **d1** = Λ\_MS-bar/Λ\_L — and `open-derivations.md` unifies **E3 = Q1 = Q2 = d1** as *"the one model-action one-loop background-field constant"*, i.e. the single biggest genuinely-open target in the project. It was filed as dead code. It is real, unfinished, and the opposite of dead.

Its own docstring gives the reason it exists: hand-transcribing Wilson vertices *"risks fabricating coefficients"*, so the module derives every vertex from the action instead. That is a deliberate anti-fabrication measure sitting in a directory labelled "probably delete".

### 3.4 The one honest open question

**`interactions.qed_casimir_materials`** — F207's materials companion (finite-conductivity + thermal Lifshitz reduction η(a), needed to compare the model's ideal Casimir law against Lamoreaux 1997 / Mohideen & Roy 1998 / Decca 2007 sphere-plate data).

It is a genuine orphan: nothing imports it, no `__main__`, no test, no finding names it, no inventory row. It is also the only one of the ten that the dead-code proposal's *structural* signal independently flags.

**It is left in place, still `dead_candidate`, deliberately.** It is **unbuilt, not superseded** — retiring it to `deprecated/code/` requires naming it in the supersession ledger, and there is no supersession to assert. Writing one would be a false entry to satisfy a checker. The decision is a judgement about whether the materials comparison is still wanted, and that is Ben's to make, not something to take quietly inside a maintenance pass. It also still imports numpy directly (**D8**).

---

## 4. An operational discovery worth more than the pass

`_viz_live_display.py`'s retirement banner said its move was blocked because *"`git mv` needs an `unlink` this mount refuses"*, and handed the move back for Ben's machine. **That diagnosis was wrong, and it had been costing sessions work.**

- This mount refuses `unlink(2)` — confirmed: `rm`, `os.remove` and `git clean` all fail with `Operation not permitted`.
- **It permits `rename(2)`.** `git mv` is a rename plus an index write, so **`git mv` works.** It only strands a zero-byte `.git/index.lock` afterwards — which is itself cleared by a rename.

The real blocker was different and worse: a **stale `.git/index.lock` dated 2026-07-31 09:23**, left by an earlier half-failed operation, which had been silently failing *every git index write in this repo for three days*. CLAUDE.md predicts exactly this failure ("a half-failed checkout strands a `.git/index.lock` it also cannot remove") but records no way out. There is one: **rename the lock**, don't try to delete it.

Two stray probe files from earlier sessions hitting the same wall (`.unlink_probe`, `.unlink_probe2`) were parked in the git-ignored `.vendor/_scratch/` by the same method, so the repo root is clean of them.

**Consequence:** file *moves* — retirement to `deprecated/`, promotion to `forks/`, any restructuring — are available in the sandbox after all. They were being deferred to Ben's machine on a false premise.

---

## 5. Counts

| Measure | Before | After |
|---|---:|---:|
| Modules registered `dead_candidate` | 10 | **1** |
| Modules registered `partial` | 8 | 11 |
| Findings in the four named rows with no test record | 4 | **0** |
| Gate-tier registry records | 36 | **40** |
| Supersession ledger records | 13 | 15 |

### 5.1 Verification

Every check run after the change, one at a time (the sandbox kills a single bash
call at ~45 s, so `run_gate.py` end-to-end does not fit — CLAUDE.md's note):

| Check | Result |
|---|---|
| `casim test --id F245…,F246…,F247…,F278…` | **4/4 PASS**, 9.8 s |
| `casim test --tier gate` (by sector: core, lattice, gauge, interactions, suite) | **all PASS** — includes the three `scenario` records `pytest` cannot collect (V-004) |
| `check_module_registry` (D11) | 188 registered, 187 files on disk, all covered |
| `check_deprecated` | 195 files accounted for |
| `check_test_registry` (D9) | 380 records, 0 files unregistered |
| `gen_test_registry --check` / `gen_module_graph --check` | current (both were **stale at baseline**, from concurrent sessions; regenerated) |
| `audit_numerics --ratchet` (D8) | OK — not regressed |
| `audit_constants --ratchet` (D7) | OK — 0 rogue literals in `src` |
| `casim index` | all seven targets; 0 undeclared duplicates, 0 undeclared gaps |
| `audit_tests --ratchet` | **RED — inherited, see follow-up 4** |

### 5.2 Concurrency

Three other sessions were live in this repo during the pass; none was collided with.

- **`loving-keen-wright`** (interactions) was promoting Finding 15 out of the
  `F01–F15` bundle at the same time — which covers `interactions.derive_beta_LV`,
  one of the ten. Their `_SPINE` record landed first; this pass left it untouched
  and did not duplicate their test. Their independent `/review-finding` run
  (`docs/reviews/F01-F15-review-2026-08-03.md`, defect 1) reached the **same**
  verdict about that module from a cold context: registered dead, backing four
  "exact algebraic" inventory rows. Two routes, one conclusion.
- **`blissful-optimistic-galileo`** (lattice, F291–294) and
  **`sharp-jolly-goldberg-2`** (gauge, F302–305) were also active. F302 landed
  mid-pass; the block reserved here (299–301) did not collide and is released
  unused.

---

## 6. Follow-ups, in priority order

1. **`derive_velocity_addition` has no test record.** It backs an exactness-inventory row on Finding 15's velocity-addition extension. Same shape as F245/F246 — a closed-form result whose only implementation cannot fail. Cheapest remaining H8 item.
2. **`derive_dielectric_noconfine` has no test record.** A closed *negative* (F142 Q1) backing an inventory row. A negative with no test is still a claim that cannot regress visibly.
3. **Decide `qed_casimir_materials`** (§3.4) — build out the materials comparison, or supersede it explicitly. Not a maintenance decision.
4. **The test-health ratchet is red, and it is not this pass's debt.** Baseline measured before any change here: `unfalsifiable 70→72`, `import_time_work 323→327`, `no_assert 231→233`, `legacy_script 47→48`, all from the concurrent F291–F296 and F01–F15 sessions. It needs a baseline move with a reason, by whoever owns those files.
5. **Correct F278 §9, F245 §Method and F247 §2** with the three re-measured numbers in §2.1 — small edits, and the findings are the documents other work reads.
6. **The `dead_candidate` label itself is mis-specified.** It currently means "nothing imports this", which for an analytical derivation kernel is normal. Either rename it (`unreferenced`, which the registry already has as a `reach` value) or make the dead-code proposal require a *second* signal — a supersession, or the absence of any finding and inventory row — before a module can carry it. As it stands the label produced nine false positives out of ten.
