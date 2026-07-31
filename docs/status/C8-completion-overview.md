# C8 completion overview — CASIM owns the indexes

*2026-07-31 - 06:15. Phase C8 of `docs/roadmaps/roadmap-casim-consolidation.md`. Entry state: C0–C7 complete, both registries populated; five indexes scraped from the filesystem by a 249-line tool; the exactness inventory's hand-typed header 125 findings behind its own tree; 147 of 530 residual-bearing rows generated. Verified in FULL mode with the vendored scipy/pytest env.*

## Sector claim

```yaml
claims:
  indexes:
    session: vibrant-charming-cannon
    phase: C8
    claimed: 2026-07-31 - 05:21        # UTC
```

Claimed before any file was touched, and — like C7's `tests` claim — stated as **not a module sector**: it covers `tools/regen_indexes.py`, `tools/gen_exactness_inventory.py`, `tools/gen_manifest.py`, `src/casim/index/`, the five generated `*-index.md` files and `docs/status/exactness-inventory.md`. No `modules:` record and nothing inside `engine/`, so no conflict with C6's still-open `interactions`/`forks` claim.

## What landed

`src/casim/index/` — one module per target, each reading a registry — and `casim index [--check] [--only …]`.

| Target | Source | Before → after |
|---|---|---|
| `code-index.md` | module registry (D11) | docstring scrape → sector, status, reach, findings, exactness, test dependents |
| `tests-index.md` | test registry (D9) | filename-prefix heuristic → declared mapping, 350 rows |
| `findings-index.md` | `findings/` ⨝ ledger ⨝ D9 | summary only → + supersession annotation, test-record count, number-reuse flag |
| `docs-index.md` | prose scrape | 96 → 117 entries (`deprecated/` now listed) |
| `project-status-index.md` | prose scrape | unchanged in kind |
| `test-results/manifest.json` | the P1.4 builder, **imported** | unchanged output, one caller |
| `docs/status/exactness-inventory.md` | artifacts ⨝ D9 | 147 → **530** generated rows; header now generated |

**The manifest builder is imported, not re-implemented.** `tools/gen_manifest.py` is loaded by path and called, so `manifest.json` is byte-identical and there is no second copy of the linking logic to drift — the precedent C5 set by importing `migrate_module.py`'s templates rather than copying them.

### C8.1 — what the registries make possible

`tests-index.md`'s old Results column was produced by `result.startswith(test_stem)`, **capped at two matches**, and empty on 104 of 339 rows. The heuristic is deleted, not improved: every row is a registry record, so the mapping is declared, uncapped, and wrong only if a human wrote it wrong — in which case `casim test` fails on the same field. Two artifact columns now, deliberately:

- **Baselines** — the record's `results:`, i.e. what it *fails on*;
- **Other artifacts** — files the results manifest links to the same test that the record does *not* declare. That is C7's arming to-do list (52 records), in the open, rather than a fallback pretending to be a mapping.

`code-index.md` carries the four fields that make an index useful for deciding what to load, and the headline number falls out of it: **47 of 194 registered modules are channel-driven (24%)** — P6's "67 of 106 kernels are unreachable" as a generated cell.

### C8.2 — the finding-number audit, and what it found

`casim index` now fails on a duplicated finding number or a gap that is not declared in the new `docs/design/finding-numbers.yaml`.

It found **ten numbers used twice**, not the three the roadmap knew about:

| Number | The two files |
|---|---|
| F26 | speed-of-light-as-rotation-rate *(CLAUDE.md core decision 2)* / bcc-spin-axis-scalar-contamination |
| F101 | one-heavy-branch-fit-W / strong-coupling-sigma-compact-rotor |
| F102 | coupled-rotors-crossover-survives / particle-layer-em-su3-backaction |
| F134 | unified-real-space-integration / phase4-chiral-blockspin-completion |
| F136 | colour-triplet-dirac-quark-confinement / realspace-scalar-confinement |
| F174 | shape-angle-2-9-topological / stellar-structure-overlay |
| F176 | covariant-dielectric-tov-recovery / saturation-self-duality-principle |
| F199 | amplitude-mode-stability-nogo / angular-self-duality-derivation |
| F200 | eg-sextic-coupling-computed / sterile-neutrino-dark-matter |
| F218 | algorithm-through-the-engine / alpha2F-firstprinciples-and-pade-gap-ratio |

**One is not a physics collision but a filename defect, and it hides a second one:** `F136-realspace-scalar-confinement.md` opens with `# F135 — Real-space confinement (U1)`. Its content is F135, while `F135-blockspin-wavepacket-realtime.md` is a *different* F135. So F135 is also used twice, invisibly, because one of the pair wears an F136 filename. That is the cheapest of the ten to fix and the clearest argument for the check existing.

Gaps: F2–F15 are **accepted** — findings 1–15 predate the one-file-per-finding layout and live in `findings/F01-F15-findings.md`, which is also why the inventory cites "Finding 1" rather than "F1". F219 and F229 are **resolved** — abandoned after collisions the changelog records. F111 and F127 are **unreviewed and are real holes**: both have live tests (`test_F111_second_order_deflection.py`, `test_F111_tree_gauge_su3_ladder.py` — itself an F111 collision in the test tree — and `test_F127_alpha_em_derivation.py`) and no finding file at all.

**All ten duplicates are recorded as `status: unreviewed`, and `casim index` prints that count on every run.** Detecting a collision is not resolving one. Deciding which file keeps a number is a physics-ownership call — F26 in particular is a founding citation — so C8 converted an invisible problem into a listed one and stopped there. A stale declaration (an exception for a duplicate that no longer exists) also fails, because leaving one behind silently re-arms the next collision.

### C8.4 — the inventory, and the honest way to 100%

P1.5 generated 147 of 530 rows and said why: the class vocabulary in the artifacts is not standardised — `exact` (61), `machine-precision` (34), `machine` (31), `quantitative` (132), plus `Tier-B`, `PREDICTION`, `structural`, and channel labels like `coupled` that are not exactness classes at all.

C8 uses **three rules in order, and records which one fired per row**:

1. `declared` — the entry's own label, canonicalised. P1's rule. **147 rows.**
2. `record` — the owning test-registry record's `expect.exactness` (D9, closed vocabulary by construction). **0 rows today** — see the correction below.
3. `signature` — the numerical criterion *this document already defines* in its own "Reading the table" section: residual `== 0` → exact, `< 1e-12` → machine, larger → quantitative. **383 rows.**

Coverage: **530 of 530 (100%)**, reported per rule rather than as one figure, because "classified" means something different in each case. Result: 154 exact, 195 machine, 181 quantitative.

**A correction to the C7 overview, made here.** That document claimed 84 registry records declared an `expect.exactness`. The true figure was **4** — the F234 record and the three scenario records, the only ones C7 hand-authored. The number was written from memory and not measured; C8 measured it at 4 on the first query, which is why rule 2 contributes nothing yet and rule 3 had to exist. The C7 overview now carries that correction inline. What `expect.exactness` actually buys is that a declared class **cannot be outside the closed vocabulary** — not that many records had one.

**The hand-written Tier 1–3 tables were not deleted**, against the roadmap's "generate the tables outright". They carry a *Predicted form* column — the physics claim, e.g. "$u^2+\lVert\tilde{\mathbf n}\rVert^2 = 1$ (Paper 1 Eq. 15, sign-corrected)" — which no artifact records. Replacing them with machine labels like `C1_derived_cos3delta` would have raised coverage and destroyed information. They are retitled **(curated)** and stay authoritative for the claim; the generated tables are additive and complete. Recorded as a deviation, with that reason.

**Staleness reads 0 because the number is now generated, not because the metric was weakened.** The freshness header (`covers findings through **F265**`) and the whole tally are inside generated markers, so the hand-typed `F140` that sat 125 findings behind cannot recur. A non-zero value now means `casim index` has not been run, which `--check` catches anyway.

### C8.3 — retirement

`tools/regen_indexes.py` and `tools/gen_exactness_inventory.py` are deprecation shims that forward to `casim index` and re-implement nothing; both go to `deprecated/code/` at C9. `make indexes` is `casim index`, `make indexes-check` is `casim index --check`, `make manifest` is `casim index --only results,exactness`. CLAUDE.md's §"Index maintenance" is rewritten, including the new rule about declaring a finding-number collision. `INDEX.md` stays hand-maintained — it maps the directory layout, which no registry knows.

**The gate loses two checks and gains one.** `gen_manifest.py --check` and `gen_exactness_inventory.py --check` are replaced by `casim index --check`, which covers all seven targets plus the numbering audit. Three separately-checked artifacts could each be stale while the others were clean; now one command answers for all of them.

## A defect found by building the check

`casim index --check` went red on a **one-minute mtime difference**. The manifest records each artifact's `mtime`, so any run that merely *touched* a result file — a pytest session regenerating `casim-exactness-inventory.md`, say — made the manifest "stale" even though no number moved. `gen_manifest.py --check` compared mtimes too, which is exactly why it kept reporting stale during C7 for no reason anyone could act on. mtime is a filesystem fact, not content; the manifest already carries a numeric `fingerprint`, and that is what should decide staleness. `generated`, `git_sha` and `mtime` are now the three excluded keys, and idempotence is verified by an assertion rather than by eye.

## Acceptance gate C8 — item by item

| Criterion | Verdict |
|---|---|
| `casim index` on a clean tree produces a zero diff (idempotent) | **MET** — asserted in `tests/casim/test_index_integrity.py`; two consecutive runs report `current` for all seven targets. The first version was *not* idempotent (it accumulated a blank line per run) and `--check` caught it |
| `tests-index.md` has no empty Results cell the registry could fill | **MET** — asserted per record: every declared baseline appears in the file |
| `exactness-inventory.md` generated at ≥95% coverage with the residual gap stated numerically | **MET** — 100% (530/530), stated per rule: 147 declared, 0 by record, 383 by signature |
| Staleness metric reads 0 | **MET** — header F265 vs newest F265 |
| Finding-number audit fails on a duplicate or unexplained gap (C8.2) | **MET** — and it fails on a *stale* declaration too |
| `make gate` green | **NOT MET, and not C8's** — 16 of 17; the one red is the 52 C3.4 shim imports in `engine/interactions/` (23) and `engine/forks/` (29), unchanged at 52 from entry to exit, in sectors claimed by the still-open C6 session |
| `make drift` clean | **MET for C8** — the same 7 pre-existing drifted artifacts as at C7 exit (latest mtime 07-30 17:18, before this work); C8 rewrote none of them |

Gate checks were verified individually rather than in one `tools/run_gate.py` run, because this sandbox kills any single command at 45 s; that includes `pytest tests/casim` (**128 passed, 1 skipped**) and the exact `casim index --check` invocation the gate now issues.

## Handoff

**C9 (retirement) is unblocked and inherits from C8:**

- delete the two shims (`tools/regen_indexes.py`, `tools/gen_exactness_inventory.py`) into `deprecated/code/`;
- CLAUDE.md's §"Index maintenance" is already C8-correct, so C9's doc pass is smaller than the roadmap assumes; §"Project Structure" and §"Context" still need the `ca-simulation/` rewrite;
- `code-index.md`'s shim section becomes empty by construction when `ca-simulation/` goes, which is a free post-C9 check.

**Needs a physics owner, not an engineer:**

- **the ten `unreviewed` duplicate finding numbers**, F26 and F136/F135 first — F136 is a filename fix that resolves two collisions at once;
- **F111 and F127**: live tests, no finding file.

**Still open elsewhere:** C7's 226 unarmed `result_dump` promotions and 38 debt records; and the 52 shim imports, which block the gate for everyone until C6 releases its claim.

*Cross-references: `docs/roadmaps/roadmap-casim-consolidation.md` §C8, `docs/status/C7-completion-overview.md`, `docs/status/P1-completion-overview.md` §P1.4–P1.5, `docs/design/finding-numbers.yaml`, `src/casim/index/`.*
