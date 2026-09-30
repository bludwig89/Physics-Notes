# Completeness overview — 2026-09-08 - 15:18

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: full sweep, 74 rows (blocks A, B, C, E, K, G, H) plus the 28-row parameter ledger (D).
Previous benchmark: `docs/status/completeness-2026-08-20.md` **as amended in place through
2026-09-06** (that file carries seven inline post-dated amendments; the amended state, not its
original text, is the baseline here). Health probe: run live against the repository on Ben's
machine via the device bridge, including — for the first time in this command's history — a
`make gate` run that completed. Research prompts for every row below `MACHINE`:
`completeness-2026-09-08-prompts.md` (79 rows / 67 sections). **Amended in place, 2026-09-10:**
row **A10** moved QUANT → PARTIAL (F380 names F331's mass-dependent kappa_100 residual as one
object, p_eff=1.489±0.039, matching the derived power 3/2 to <1%); scoreboard and row text updated
accordingly, one inline amendment so far.*

**This is a real sweep, not a rerun.** Nineteen days separate this report from its baseline and
**51 findings landed in them** (max **F325 → F376**, 368 finding files, `NEXT FREE NUMBER F377`).
The last three reports were all short-window reruns that carried blocks A–G verbatim; this one
re-graded every row against the ledgers, and eleven rows moved.

**The headline is not a physics result.** It is that `make gate` — the project's declared barrier —
**fails**, and has been failing while running in a silently reduced mode that the documented
workflow guarantees. Details in the health probe and rows H6/H8. Physics moved forward on nine
rows in the same window; the integrity block moved backward on two.

---

## Health probe (what actually ran)

Live via the device bridge from the repository root on Ben's machine. **Note the per-call budget
is ~180 s here, not the ~45 s the command file assumes** — which is why the gate ran at all.

| Target | Result |
|---|---|
| `make indexes-check` | **GREEN.** All 8 indexes current (`findings-index.md` 368, `project-status-index.md` 56, `tests-index.md` 485, `code-index.md` 270, `docs-index.md` 147, `test-results/manifest.json` 449, `exactness-inventory.md` 570, `claims-index.md` 305). Finding numbers: max **F376**, 357 distinct, 368 files, **0 duplicates**, 19 gaps (0 undeclared), **NEXT FREE NUMBER F377**. Exactness header F376 vs newest F376 → 0 behind. `[casim index] ok` |
| `make registry` | `485 record(s) cover 449 test file(s), all valid (D9)`. Kinds: assertion 202, result_dump 231, scenario 3, legacy_script 49. Tiers: **gate 114**. Baselines: 7 `stale_by_design`, 2 `candidate` (drift still FAILS, by design) |
| `make numerics` (D8) | **RATCHET FAILED.** 320 modules scanned. Direct `np.fft` calls **0** (must be 0 — is). Device-namespace fft 8, in 1 file, behind `require_float64`. Files importing numpy/scipy directly **169, was 168** — `files_with_direct_imports 168 -> 169`, one new unrouted import. Active backend `numpy.fft`; pyfftw vendored but not installed into the env |
| `make health` | 449 files: gate 25, battery 424, pytest-style 162, no-assert 240, **UNFALSIFIABLE 73**, import-time-physics 340. Check soundness: **111 gate-tier assertions** (was 82), **155 declared controls** (was 91; strong 73, weak 1), **NO CONTROL 37 — was 48, the first movement in this number since 2026-08-08** |
| `python3 tools/audit_tests.py --ratchet` | **RATCHET FAILED:** `import_time_work 336 -> 340 (+4)`, `no_assert 237 -> 240 (+3)`. Separately **improved**: `gate_assertion_no_control 48 -> 37`, not yet locked in (`--update-baseline` not run) |
| `python3 tools/gen_test_registry.py --check` | **STALE** — six sector files (`core`, `forks`, `gauge`, `interactions`, `lattice`, `particles`) are stale against their sources |
| `python3 tools/check_control_soundness.py` | **FAILED — 4 problems.** 155 controls declared, **151 verified RED**. One journalled **NOT SOUND**: `F350-ws-mask-cutcell#control0` — *"declared leg(s) ['pass'] do not exist in the payload; legs present: [] — a control naming a leg the driver no longer emits has silently stopped testing"*. Three **STALE** verdicts, all `F345-field-equation-uniqueness#control{0,1,2}` |
| `make coverage` | **FAIL — three ceilings breached:** `unjoined 2` (ceiling 0), `weak_only 2` (ceiling 0), `untested 2` (ceiling 0). Declared: `no-test 5`, `claim-none 20` |
| `make gate` | **RED — completed and FAILED, 10 of 33 checks, 59.5 s.** Four substantive failures, each independently reproduced above: *test health has not regressed*; *numerics imports have not regressed (D8)*; *test registry is current*; *declared negative controls are sound (D9/H2)*. Six further failures are `ModuleNotFoundError: No module named 'pytest'` and the run self-labels **`reduced mode: pytest was not available`** — see below, this is a real defect, not an environment excuse |
| module registry (D11) | 254 modules. Reach: **driven 52 (20.5 %)**, test-only 90, standalone 81, **unreferenced 24**, package-only 4, entry-script 3. Status: live 193, fork_live 25, fork_unclaimed 23, partial 12, dead_candidate 1 |
| exactness inventory | exact **168** (was 159), machine **198** (was 196), quantitative **204** (was 185). Coverage 570/570 (100 %) across 503 artifacts (was 448) |
| `git status` | **Clean** (one untracked `.claude/settings.local.json`). The 394-file backlog the 2026-09-05 audit declined to commit **was committed 2026-09-06** as `ed51277`. See Method notes on what that means for `result_dump` baselines |

### The gate's reduced mode is a repository defect, and it is load-bearing

`Makefile:10` reads `export PYTHONPATH := src`. Make's `export VAR := value` **overwrites** the
environment, so the workflow CLAUDE.md itself documents —

```bash
source "$PWD/.vendor/activate.sh"   # prepends .vendor/py310-linux-aarch64 to PYTHONPATH
make gate
```

— discards the vendor path at the moment `make` starts. `pytest` **is** present and importable
(9.1.1, verified: `python3 -c "import pytest"` succeeds with the vendor path set), but the gate's
own subprocesses cannot see it, so the run silently downgrades to `reduced mode: pytest was not
available` and six `tests/casim/` records fail on the import rather than on their content.

This is not cosmetic. The gate is the barrier the whole D9/D11/D12 apparatus rests on, and in the
documented invocation it has been skipping a substantial part of the package suite while still
reporting a pass/fail verdict on the rest. `make gate PYTHONPATH="src:$PWD/.vendor/py310-linux-aarch64"`
loads pytest correctly — and then exceeds the bridge's 180 s budget, so **the full-mode gate result
is still unknown**. What *is* known, and reproduced check-by-check above, is that the four
non-pytest failures are real and fail in either mode.

---

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A Foundations (12) | 5 | 1 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| B Gauge (12) | 4 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| C Matter (7) | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| E Gravity (13) | 4 | 1 | 4 | 2 | 0 | 1 | 0 | 1 | 0 | 0 |
| K Cosmology (12) | 0 | 0 | 1 | 7 | 0 | 0 | 1 | 3 | 0 | 0 |
| G Emergent (10) | 1 | 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| H Integrity (8) | 0 | 1 | 1 | 5 | 0 | 0 | 1 | 0 | 0 | 0 |
| **Total (74)** | **16** | **4** | **16** | **31** | **0** | **1** | **2** | **4** | **0** | **0** |

*Two baseline corrections are folded in rather than counted as movement: the 2026-08-20 scoreboard
was never updated for its own inline promotions of **A6** (`PARTIAL → EXACT`, 2026-08-27) and **E8**
(`QUANT → EXACT`, 2026-09-03) — that file says so about itself. Its printed totals
(14/5/17/32/0/1/1/4) are therefore not the state it actually recorded; the corrected baseline is
**16/5/17/30/0/1/1/4**, and this run's movement is measured against that.*

**Parameter ledger: 6 of 28 derived with zero free parameters, 2 partial, 2 fitted, 14 open or
absent, 4 excluded (permanently free — a result, not a gap).**

---

## The five things most worth building next

Ranked by (load-bearing × distance from closure). Two of the baseline's five are gone: **Q4 closed**
(F372, 2026-09-05) and **H2's control backlog finally moved** (48 → 37). Two are new.

### 1. `make gate` is red, and its reduced mode has been hiding how red

**What.** Four independent gate checks fail — the test-health ratchet (`import_time_work` +4,
`no_assert` +3), the D8 numerics ratchet (one new unrouted numpy import), a stale test registry
(six sector files), and control soundness (one control that has **silently stopped testing**, three
stale verdicts). On top of that the documented invocation runs in `reduced mode` because
`Makefile:10` clobbers the vendored `PYTHONPATH`, so the pytest half of the suite has not been
running at all under the workflow CLAUDE.md prescribes.

**Why it matters.** Every other row in this report is graded from artifacts this barrier is supposed
to protect. H6 drops to `OPEN` on it and H8 drops off `MACHINE`. It is also the cheapest item on
this list by a wide margin.

**What blocks it.** Nothing structural. Each failure names its own file.

**Smallest next step.** `gen_test_registry.py` to unstale the registry; `make control` to re-verify
the three F345 verdicts; fix or retire `F350-ws-mask-cutcell#control0`; route the one new numpy
import through `casim.numerics` or declare it exempt; then decide whether `import_time_work`/
`no_assert` get repaired or the baseline re-locked with a reason. Separately, change `Makefile:10`
to append rather than overwrite (`export PYTHONPATH := src$(if $(PYTHONPATH),:$(PYTHONPATH))`) so
the gate stops running in reduced mode without saying so in its exit status.

### 2. d₁ — the strong-sector one-loop background-field constant (was #1, still open, but its blocker is gone)

**What.** Δ C_vertex = −2.0160 (36.2 % of ΔC), bracket [−2.257, −1.446]. Third leg of ledger row
**d₁**, the one open item between the tree and a quoted α_s(M_Z).

**What changed.** Its named upstream blocker **closed**: ledger row **L6** ("which object is the
rule's gauge action at finite a") was decided on both legs by **F337** (2026-08-30) — the rhombic
action's own quadratic form, not F26/Ω_even. F305's deliberate declination no longer stands in the
way. But **F350** then built F337's own named remedy (an anti-aliased Wigner–Seitz cut-cell mask),
verified it far more accurate than the sharp mask in isolation, and found it **does not explain the
slow convergence** — so the native sweep still does not land inside the bracket.

**Why it matters.** Blocks B8, D#16, G5, E3, and the charged-lepton scale D#9 via F233. One of the
six zero-free-parameter claims.

**Smallest next step.** With L6 decided and the mask excluded as the cause, the next candidate is
the finite-volume/discretisation systematic itself — run the native sweep at n=28–40 on the
F337-decided action and characterise the residual convergence rate directly rather than patching
the mask.

### 3. K6 — baryogenesis is now a computed number, and it misses by 10–11 decades

**What.** **F364** (new, 2026-09-04) replaces F202's Sakharov-conditions checklist with an actual
leading-order resonant-leptogenesis Boltzmann/QKE computation, using the model's **own** F201
heavy-neutrino masses (M₂≈0.40 GeV, M₃≈5.60 GeV) and Casas–Ibarra Yukawas fit to measured
oscillation data. Result: at the model's own untuned texture masses, scanning the free CP phase
caps at **Y_B/Y_B^obs ≈ 2×10⁻¹¹** — ten to eleven decades short — then collapses at larger Yukawa
into strong washout. A sharp Breit–Wigner resonance in ΔM₂₃/M *does* reach and exceed the observed
value, but only in a tuned window.

**Why it matters.** This is the model measuring its own shortfall, in the same shape Q4 had before
F372 dissolved it — and nothing has been recorded against it in the four days since. It also
supplies, as a by-product, the first **sphaleron B-violation rate** computed anywhere in the tree,
which is the thing C7 and K6 have both been carrying as absent.

**What blocks it.** Nothing structural — the machinery exists and runs.

**Smallest next step.** Decide whether the resonant window is reachable from the F201 texture
without tuning ΔM₂₃, or whether the 10–11 decade gap is a genuine falsifier of the F47/F201/F202
leptogenesis route. Either answer is a result; leaving it unadjudicated is not.

### 4. K9 / Λ — the question changed from "is there a mechanism?" to "do we adopt an imported one?"

**What.** **F367** (2026-09-04) supplies, for the first time, a mechanism that **exactly** achieves
the required order-selectivity: a Kaloper–Padilla-style global spacetime average annihilates any
spacetime-constant additive piece of the matter-trace source, independent of its magnitude —
sympy-verified as an identity, not imported from a citation. **F368** then ran CL303's own
falsifier 4 and found PPN / F178-vacuum / induced-G are *not* in tension, but surfaced two new
undischarged costs: sequestering's base action requires a spatially closed (k>0) cosmology, and its
solution is transient.

**Why it still sits at OPEN.** The mechanism is **not the model's own** and is explicitly **not
adopted** — grafting it would add global non-propagating Lagrange-multiplier fields to CLAUDE.md
decision 4's action. F332 already closed the two *local* channels structurally. So the model still
has no mechanism of its own; what it now has is a proof that an external one would suffice, plus a
named adoption decision with a priced bill.

**Smallest next step.** Take the adoption question directly: either work F367's own listed route 2
(show ρ_vac is not a spacetime constant under the model's adopted cosmology, which would break the
match without touching the identity), or work its route 6 (show the global sector is inconsistent
with decision 4's other adopted content), which would close adoption off and return K9 to a search.

### 5. Proton decay and the neutron EDM — the two genuine ABSENTs, both confirmed by tree-wide grep

**What.** This run finally ran the whole-tree keyword sweep the last three reports admitted they had
skipped. Two hard zeros:

- **Proton decay / B-violating rate.** `grep -rli "proton decay"` returns **zero** hits in
  `findings/`, `papers/`, `docs/claims/` and `docs/theory/`. Its only four hits in the entire
  repository are the completeness reports themselves — the row has been citing its own absence.
- **Neutron EDM / electric dipole moment.** **Zero** hits anywhere in the repository outside
  vendored third-party libraries.

**Why it matters.** Both are the standard *experimental* handle on a sector the model already makes
a claim in. B11 asserts θ_QCD = 0 exactly and is graded QUANT — but the observable that tests
strong CP is d_n, and the model has never computed it or confronted the bound. C7 and K6 both carry
"no B-violating rate anywhere", and F364 has now computed a sphaleron rate without anyone connecting
it to a proton lifetime.

**External anchors** (searched 2026-09-08, cited so the next session does not re-derive them):
d_n = (0.0 ± 1.1_stat ± 0.2_sys) × 10⁻²⁶ e·cm, PSI nEDM collaboration (Abel et al.), PRL **124**,
081803 (2020), arXiv:2001.11966; collaboration's quoted bound |d_n| < 1.8 × 10⁻²⁶ e·cm (90 % CL).
τ/B(p→e⁺π⁰) > 2.4 × 10³⁴ yr and τ/B(p→μ⁺π⁰) > 1.6 × 10³⁴ yr (90 % CL), 450 kton·yr, Super-Kamiokande
I–IV, arXiv:2010.16098, PRD (2020).

**Smallest next step.** For strong CP: compute d_n from θ̄ in the model's own hadronic sector and
confront the PSI bound — a bounded calculation on machinery F122/F123 already have. For B violation:
convert F364's computed sphaleron rate into a zero-temperature proton-decay statement, or show
structurally why the model forbids one.

---

## What is ABSENT

**No whole rubric row grades `ABSENT`** — but for the first time that statement is *measured*
rather than inherited. The 2026-08-20 report carried an empty ABSENT column for the third
consecutive run while explicitly admitting it had never run the tree-wide sweep and telling the
reader to discount the column. That sweep was run this time.

| Topic | findings/ | papers/ | docs/theory+status | docs/claims/ | Verdict |
|---|---:|---:|---:|---:|---|
| Neutron EDM / electric dipole moment | 0 | 0 | 0 | 0 | **ABSENT sub-item of B11** — the empirical handle on the model's own θ_QCD=0 claim |
| Proton decay | 0 | 0 | 4 (all completeness reports) | 0 | **ABSENT sub-item of C7 / K6** |
| Flavour-changing neutral currents / GIM | 0 | 0 | 1 (a design doc) | 0 | **ABSENT**, but honestly downstream of CKM (D#10–13), itself declared out of scope |
| Unruh effect | 1 | 0 | 4 | 0 | Present, passing — not a gap worth a row |
| Sphaleron | 2 | 0 | 2 | 1 | **Newly present** — F364 computes the rate |
| Cosmic strings / topological defects / monopoles | 11 | 1 | 6 | 2 | Covered |
| Domain wall | 5 | 0 | 3 | 1 | Covered (F366) |
| Neutrinoless double beta | 2 | 0 | 1 | 1 | Covered |
| Hawking radiation | 3 | 1 | 3 | 0 | Covered (E9) |
| Axion | 7 | 0 | 2 | 2 | Covered |
| Lepton universality | 2 | 1 | 3 | 0 | Covered |

**What the shape of this list means.** The gaps are not in the model's *structure* — every
foundational and gauge-sector topic the rubric names has a sector, a finding and usually a claim
card. They are in its **contact with experiment at the points where its own claims are testable**.
The model asserts θ_QCD = 0 and has never computed the one number that would test it. It asserts
all three Sakharov conditions and now a sphaleron rate, and has never converted either into a
proton lifetime. That is a different and more tractable failure than "no sector for this": in both
cases the machinery exists, the claim exists, and nobody has closed the loop to the measurement.
Both belong in `open-derivations.md` Part A and are in neither ledger today.

---

## Regressions and changes since 2026-08-20 (as amended through 2026-09-06)

### Regressions — grades that went backwards

| Row | Was | Now | Why |
|---|---|---|---|
| **H6** Reproducibility | PARTIAL (`make gate` NOT VERIFIED, three reports running) | **OPEN** | The gate was finally run to completion this session and it **fails**: 10 of 33 checks. Four failures are substantive and were each reproduced individually (test-health ratchet, D8 numerics ratchet, stale test registry, control soundness). Six more are `ModuleNotFoundError: pytest`, caused by `Makefile:10` overwriting the vendored `PYTHONPATH` — so the documented workflow has been running the barrier in `reduced mode` without that appearing in the verdict. Graded `OPEN` rather than `PARTIAL` because this is no longer "one named residual pending verification": it is a live target with a named attack and four specific red checks. This is the most important line in the report |
| **H8** Findings without a usable test record | **MACHINE** (`no test record` count 0, verified live 2026-08-20) | **PARTIAL** | The count is **5**, not 0: F358, F363, F364, F368, F370. `make coverage` also breaches three ceilings it was passing (`unjoined 2`, `weak_only 2`, `untested 2`, all ceiling 0). Separately, the CLAUDE.md rule that every finding carries a `**Checked:**` attack-pass header is **15 short** across the 51 new findings (F328, F329, F343, F346, F347, F348, F349, F351, F352, F353, F354, F358, F364, F374, F376). H8 was promoted to MACHINE on the strength of a checker enforcing an invariant; the invariant has since been broken by new work faster than the checker's ceiling was raised |

Both regressions are in the integrity block, both were invisible to every index and to the
changelog, and **surfacing exactly this is what the command exists for**. Neither is a physics
regression.

### Promotions and material narrowings

| Row | Was | Now | Why |
|---|---|---|---|
| **D#1–6** quark masses | ABSENT ×6 | **OPEN ×6** | Ledger row **E6** opened by **F346** (2026-09-02) and **F347**: the F175/F92 `weight-as-phase` shape mechanism is inverted on PDG 2024 up- and down-type triplets and shown **not** to transplant, and the literature's mixed-generation Koide tuples carry no more of it. Both are leaning no-goes, not derivations — but "no route proposed" is no longer true, which is precisely the ABSENT → OPEN promotion |
| **A6** Born rule | PARTIAL *(printed)* | EXACT | Baseline correction, not movement — promoted inline 2026-08-27 by F329; the 2026-08-20 scoreboard never absorbed it |
| **E8** Black holes | QUANT *(printed)* | EXACT | Baseline correction, not movement — promoted inline 2026-09-03; same cause |
| **H2** Falsifiability (evidence; grade held) | 82 assertions / 91 controls / **48 NO CONTROL, unmoved 12 days** | PARTIAL, 111 / 155 / **37** | **The backlog finally moved** — first fall since 2026-08-08, via two retrofit sessions (2026-09-06 - 03:10 and earlier). Grade held at PARTIAL and **not** raised, because the same probe found one control (`F350#control0`) journalled NOT SOUND — *"a control naming a leg the driver no longer emits has silently stopped testing"* — three stale verdicts (F345), and a pre-existing can-fail ratchet at 6 against ceiling 5, i.e. six gate entries that pass unconditionally regardless of content. A backlog that shrinks while the surviving controls rot is not a net improvement |

### Rows sharpened without moving grade

Nine rows gained real content in this window and stayed put, which is the honest outcome in each case:

- **B7** confinement — **F335** supplies the exact machinery B7's residual was named as blocked on. F323 had recorded that a repo-wide grep for `reflection positiv` / `Osterwalder` / `Schrader` returned zero hits; link reflection positivity for the BCC₃×ℤ Wilson action is now established at any β_s, β_t ≥ 0 for any compact gauge group. F335 states plainly: *"No mass gap, no area law, no confinement verdict."* The residual is now OS reconstruction → transfer-matrix spectrum, which is a target rather than a wall.
- **B8 / D#16** — **F337** closes L6; **F350** excludes the WS-cell mask as the cause of slow convergence. d₁ leg 3 alone remains.
- **B11** — **F340**: F321's action-fork dependency closed by L6, and reality upgraded from sampled to an exact theorem over the full non-perturbative configuration space.
- **C4** neutrino nature — **F341**: Majorana is now the *structurally required* completion (removing it reopens the F165/F279 hypercharge closure), conditional on one named premise. From "nothing forces either" to "one forced, conditional on a stated dependency".
- **E10** singularities — **F354**: the lattice-regulated core is **geodesically complete**, exact-algebraic, and the curvature bound alone forces it. E10's own named gap ("no geodesic-completeness result") is closed; the core *scale* stays contingent on three named inputs, so the grade holds.
- **E9** BH thermodynamics — **F355**: the horizon cell constant is **computed** rather than posited, and the two routes to the model's own induced 1/G **disagree** by a bracketed factor. Sharper and worse, which is the honest reading.
- **K2** BBN — **F361**: the A=7 rate fits carried transcription bugs against their own cited source (Kawano NUC123); fixing them takes ⁷Li/H from −92 % to **−6.3 %**. One of K2's three residuals discharged.
- **G9** — **F374** closes the Eliashberg-solver route as a no-go; **F375** crosses the target with a real DFT-sourced N(0) for Nb: Allen–Dynes headline **6.3 % → 4.9 %**.
- **G6** — **F373**: the OBE quark-size regulator b = 0.55 fm is not independently tuned; it matches the model's own gauge-derived confinement radius. G6's single free parameter is no longer independent, though the row stays QUANT since this is a consistency check, not a derivation.

### Also observed, not grade-worthy

- **Claims registry**: 283 → **305** cards. live 155 → 164, open 93, withdrawn 25, contingent 9, narrowed 9, not_claimed 5. `unreviewed-seed` 222 → 220. **Zero cards without a falsifier.** Headline tier 42 of 305.
- **Exactness**: exact 159 → **168**, machine 196 → **198**, quantitative 185 → **204**; artifacts 448 → 503; coverage stays 100 %.
- **Test registry**: 434 → **485** records; gate tier 85 → **114**.
- **Module registry**: 218 → **254** modules; driven 51 (23.4 %) → **52 (20.5 %)** — a fourth consecutive fall in the *fraction*. The 2026-09-05 audit (`docs/audits/module-disposition-2026-09-06.md`) read all 34 newly-registered modules and both non-driven pools and found every one correctly non-driven by design.
- **Git hygiene**: a stale `.git/index.lock` from 2026-08-19 blocked every git write for **18 days** (found 2026-09-05, renamed aside). The resulting 394-file backlog was committed 2026-09-06 as `ed51277`. See Method notes.

---

## Full rubric

*Rows carry their evidence forward from the amended baseline where nothing moved; every row was
re-read against `open-derivations.md`, `findings-index.md` and the claims registry this run.
⚠ marks a citation the supersession ledger names.*

### A — Foundations

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| A1 | Spacetime dimensionality | PARTIAL | F291, F292, F313, F316, F318, F326, F377 | the three Cayley generators; infinite volume; single-generator QCA dynamics is a named posit, now shown independent of the five BDPT axioms and tested against its only live alternative (not derived) | Two independent selectors each return {3}; d=6/d=9 excluded. F326 closes the "+1": no second candidate generator exists. F377 shows P1 is independent of BDPT's five axioms (their own homogeneity axiom is spatial-only) and runs the one falsification attempt a periodic scheme cannot make -- an aperiodic A+/A- alternation -- which does not reproduce ballistic F26/F27-regime transport. The residual posit is ledger Part C row **P1** — dynamics generated by iterating ONE local homogeneous unitary per tick |
| A2 | Lorentz invariance | PARTIAL | F26, F28, F30, F246, F129, F301, F327, F344 | deformed shell exact but not universal; the chiral coefficient is confronted and **EXCLUDED** | F327 converts F301's chiral $O(\lvert k\rvert^2)$ defect into a dimension-5 CPT-odd operator, $\lvert\eta\rvert_\text{max}=1.4662$, $E_\text{LV}=8.33\times10^{18}$ GeV, excluded by LHAASO/Crab by **7.05 decades**. Localised on one leg: an elementary fermion may not ride a single BCC chiral branch (CL284). Ledger **L9** is the repair. F344 adds the exact point symmetry ($D_{2h}$ unitary, $D_{4h}$ time-reversed). Tighter *and* worse — the honest reading |
| A3 | Causality / locality / finite speed | EXACT | F26, F204, F227, F290 | 0 | $c_\text{lat}=1/\sqrt3$; strict cone measured tight |
| A4 | CPT, and C/P/T separately | PARTIAL | F53, F321, F328 | the SU(2)$_L$ charged-current extension (ledger **A4r**) | F328 proves $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ **exactly** at every $\mathbf k$ and every $\lvert m\rvert\le1$ for the free massive BCC Dirac walk, $\Theta^2=-1$; and proves **no fixed unitary parity exists at any finite $\mathbf k$**. Named residual, not an unexamined one |
| A5 | Unitarity | EXACT | F276, F264, F300 | 0 | Length-preserving by construction |
| A6 | Superposition + Born rule | EXACT | F304, F312, F329, F281, F290, F227 | 0 | Gleason dichotomy for $f\in L^2$; non-contextuality closed for both gauge groups; F329 closes the regularity bridge by reduction to Gleason's own 1957 Thm 2.8 + 3.5. Ledger **A6r** fully closed. CL264 `contingent → live` |
| A7 | Entanglement, Bell/Tsirelson | EXACT | F212, F226, F214, F217 | 1.8e-15 | Tsirelson saturated exactly (CN1: Bell-indistinguishable from QM) |
| A8 | Measurement problem / classical limit | EXACT | F281, F130, F41 | 0 | Pointer basis forced; classicality a block-spin attractor |
| A9 | Spin-statistics | PARTIAL | F289, F291, F292, F217, F330, F379 | Anastopoulos Postulate 1 and $\pi_1=S_n$ stay external | F330 pins the belt trick's non-topological content to a **named** postulate; F379 tested the one route F330 left open (an emergent CONTINUOUS SO(3) from the continuum limit, vs. the finite $O_h$) — machine-confirms it is real (extends F344's 48-element covariance to the full continuous group, same rotor as F289/F330, exact) but shown, grounded in Anastopoulos's own primary text (fetched directly), to be categorically the wrong KIND of object: Postulate 1 is prequantisation-level (prior to any Hamiltonian), so no dynamical symmetry — of any size — can supply it. Generalises F330's "$O_h$ is finite" diagnosis and forecloses the "bigger continuum limit" avenue |
| A10 | Cluster decomposition / no-signalling | PARTIAL | F290, F227, F331, F380 | one named, theoretically-anchored seam: $p_\text{eff}=(\kappa_\text{measured}-\kappa_{100})/(S_{r,\ln r}/S_{rr})=1.489\pm0.039$ (2.65% relative spread, matching the derived power 3/2 to <1%, not yet closed-form to the numerical floor); F290's 1-D exponent shortfall and S-matrix-level clustering open | F331 extends clustering to the interacting 3-D BCC NJL mean-field with a closed-form $\kappa_{100}(m)=\sqrt3\,\text{arccosh}(1/\sqrt{1-m^2})$ from a genuine 3-D pole extremisation. **2026-09-10, F380** (mechanism corrected same day by its own review-finding pass): F331's mass-dependent ratio table (1.53 at m=0.05 → 0.95 at m=0.95) is named as ONE object — an $r^{-3/2}$ algebraic prefactor (2-transverse-dim stationary phase giving $r^{-1}$, PLUS an axial square-root branch point in $\omega=\arccos(nu)$ giving an extra $r^{-1/2}$ — NOT the continuum Yukawa's simple-pole $r^{-1}$) biasing F331's plain-exponential fit, re-expressed via the exact OLS regression-bias formula as $p_\text{eff}$ and measured mass-independent to 2.65% across the whole admissible range **including** the dynamically NJL-selected $m^*$ (z=-0.62σ) — the "first step" (is $m^*$ special?) is answered NO, which is what lets the table collapse |
| A11 | UV completeness | QUANT | F116, F164, F264, F284, F319, F332, F367, F368 | one number: $\rho_\text{vac}$, $10^{120.76}$ | Two cutoff-carrying coefficients, one right ($G$) one wrong by 120.8 orders. Ledger **L7**, unmoved for four reports. K9's mechanism question (F367/F368) is this row's residual's candidate; the number is unchanged |
| A12 | Continuum limit | MACHINE | F129–F135, D1 | ‖[R_b,evo]‖ ≤ 1.8e-15 | $c_\text{lat}$ an exact RG fixed point |

### B — Gauge structure

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| B1 | Origin of SU(3)×SU(2)_L×U(1)_Y | PARTIAL | F27, F51, F43, F291, F317, F318, F324, F333, F381 | two named observational facts (baryons are fermions; quarks are confined), not one bare fiat — and, per F381, not reducible to one with what the tree currently has | Reduced six-to-one by F317. F333 narrows the index's existence further: $N>1$ is **forced** given those two facts, via a generalised SU(N) constituent-count theorem plus a computed composite-exchange-parity rule. F381 tested whether premise (a) (baryons are fermions) is redundant with F289/F330's derived spin-statistics connection — computed no: that connection is a single-constituent theorem with no channel for a colour count, F333's own S1/S2 combination of it genuinely bifurcates on N, and substituting F324's separately-derived N-parity result is circular (F324's own premise (ii) presupposes colour's existence) and costs four more premises than it saves. $N_c=3$ itself untouched |
| B2 | Chirality | EXACT | F27, F91, F292 | Ward identity 1.1e-17 | W± chiral forced; independent Clifford-recursion route |
| B3 | Anomaly cancellation | EXACT | F38, F293, F324 | Witten check physics-verified, tree-unverified | All six traces exactly zero; F324 W2/W2b discharges the Witten SU(2) residual |
| B4 | Hypercharge / charge quantisation | EXACT | F165 ⚠(S13→F279), F279, F47, F51, F38 | one charge unit + $N_c=3$ for the thirds | Rank 6, dim 1 over ℚ. Moved from Scope to core claim 10 at summary rev 3 |
| B5 | EWSB mechanism | EXACT | F27, F34b, F44 | 0 | Higgs-free Stueckelberg; $m_A=0$ from rank-deficient mass matrix |
| B6 | Weinberg angle, with scale | QUANT | F138, F49, F231, F141, F334 | +0.222 % at $M_Z$; −0.064 % on shell; 0 free params | $\tfrac14$ is the $\mu_\star=4\pi v$ matching value, $\tfrac29$ its on-shell face. F334's ρ+ω VMD narrows the shared hadronic residual to 10.2 % of DHMZ2020's $\Delta\alpha_\text{had}^{(5)}(M_Z)$ |
| B7 | Confinement | PARTIAL | F70, F86, F88, F299, F323, F265, F335; F94 ⚠(S21→F323, F265) | mass gap / area law in 3+1D; OS reconstruction not carried out | 2D exact area law. **Residual redefined this run**: F335 establishes link reflection positivity for the BCC₃×ℤ Wilson action at any $\beta_s,\beta_t\ge0$ and any compact gauge group — the machinery F323 recorded as wholly absent. F335 is explicit that this yields *"no mass gap, no area law, no confinement verdict"*. The wall became a target |
| B8 | Asymptotic freedom / α_s running | PARTIAL | F144, F151, F239, F235, F287, F280, F299, F303, F325, F337, F350 | **d₁ leg 3 alone** | $b_0=11/3\,C_A=11$ exact. X1 resolved (F325, branch B). L6 **closed** by F337 — the upstream blocker is gone. F350 built and excluded F337's own named remedy (WS cut-cell mask) as the cause of slow convergence. $\alpha_s(M_Z)=0.1186$ (+0.5 %) contingent on d₁ alone |
| B9 | Running of α, EW couplings | QUANT | F322, F311, F251 ⚠(S12→F277), F261, F138, F231, F115 ⚠(S20→F138,F231), F334, F336 | 0.0495 % model-internal; 0.00158 % after importing Källén–Sabry; two-loop non-log constant open | Additive, not rival. F336 cross-checks the two-loop leading log via a second construction (unitarity + dispersion) and is explicit it is an **RG-forced consistency check, not a disjoint derivation**. F334 closes 10.2 % of the EW-leg hadronic gap with zero imported couplings |
| B10 | Why 3 colours | PARTIAL | F293, F294, F298, F299, F303, F324, F325, F338, F279, F144, F110 | odd $N_c$ only, {3,5,7,…}, not closed to {3} | F338 **explicitly does not narrow the bracket and says so first**: one previously-untested candidate route closed, one mod-16 lead flagged and not derived. CN19 stays withdrawn (F325/S22); the ℤ₂ doublet-parity leg (Bär & Wiese) survives |
| B11 | Strong CP / θ_QCD | QUANT | F321, F53, F305, F307, F91, F337, F340 | $\arg\det M_q$ at three generations (ledger E6/E7); lattice topological-charge quantization; **$d_n$ never computed** | F340 closes F321 §6's action-fork dependency via L6/F337 and upgrades reality from sampled to an **exact theorem** over the full non-perturbative configuration space; $Z$ as constructed is definitionally the $\theta=0$ sector-sum (cross-checked vs Vafa–Witten 1984). Deliberate non-claim (CL279): this is not a solution of strong CP. **New this run:** the neutron EDM — the observable that tests this row — appears nowhere in the repository (see ABSENT) |
| B12 | Gauge-boson masses, ρ, m_Z/m_W | QUANT | F49, F141, F138, F231, F320 | $v$ and $\alpha$ (two anchors); F141's equal-stiffness hypothesis | Two EW inputs vs the SM's three; $\rho=1$ exactly from F41's Stueckelberg rank, not a custodial SU(2). Core claim 12 (CL276/CL277) |

### C — Matter content

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| C1 | Exactly three generations | PARTIAL | F75, F84, F292, F342 | physical identification is a stated hypothesis, now shown **vacuous** on one leg | Group theory a theorem ($\sum d_\beta^2=48\Rightarrow T_{1u}$ unique); identification a hypothesis. F342: F75's own condition (i) supplies **zero** power to select $T_{1u}$ over $T_{2g}$ under the site-diagonal charge structure the engine implements, forced by the shell's 8 vertices forming a single $O_h$ orbit. Sharper and checkable (`casim test --id F342-generation-identification-gap`) |
| C2 | First-generation multiplet | EXACT | F38, F41, F42, F51, F165 ⚠(S13→F279), F279 | 0 | Complete and anomaly-free |
| C3 | Colour triplet + fractional charge | PARTIAL | F136, F165 ⚠(S13→F279), F279, F324, F333 | conditional on $N_c=3$ | Fractional charge forced by $3y_Q+y_L=0$; commensurability holds for any $N_c$ |
| C4 | Neutrino nature (Dirac vs Majorana) | PARTIAL | F47, F266, F341 | conditional on the model keeping its own hypercharge-closure dependency | **Materially narrowed.** F341: no protecting symmetry forbids the F47 Majorana term, and removing it **reopens the F165/F279 hypercharge closure** — so Majorana is the structurally required completion *within this model*, which the generic SM has no analogue of. From "nothing forces either" to "one forced, conditional on a named premise" |
| C5 | Neutrino mass mechanism | PARTIAL | F47, F236, F254, F343 | $M_R$ free — and now checked, not merely asserted | See-saw + $E_g$/ℤ₃ texture fix masses and hierarchy at machine precision; absolute scale unfixed. F343 is a **null result reasoned on three legs**: the F183/F107 cutoff requires an unexplained ~19-decade suppression with no mechanism, so $M_R$ is a genuine free anchor rather than an unattempted gap |
| C6 | Antimatter / charge conjugation | EXACT | F53, F260 | 0 | Per-species C; positron and crossing sector built |
| C7 | Beyond-SM content | PARTIAL | F223, F228, F266, F216, F204, F237, F364, F365, F366 | geon abundance free; **no proton-decay rate anywhere** | Planck-mass BH-remnant geon predicted; excludes its own alternatives (CN5, CN6, Alcubierre, keV sterile as 100 % DM). F365 checks the geon against two 2025 GW papers. **New this run:** F364 computes the first **sphaleron B-violation rate** in the tree — but proton decay itself is confirmed **ABSENT** by whole-tree grep (see ABSENT) |

### D — The parameter ledger

| # | Parameter | Grade | Evidence | Note |
|---|---|---|---|---|
| 1–6 | $m_u, m_d, m_s, m_c, m_b, m_t$ | **OPEN ×6** | F121, F346, F347 | **PROMOTED from ABSENT ×6 this run.** Ledger **E6** opened 2026-09-02: F346 inverts F175's exact 3-parameter circulant ansatz on PDG 2024 up-/down-type triplets and shows the `weight-as-phase` mechanism does **not** transplant; F347 closes the mixed-generation Koide route. Both leaning no-goes — but a route is now proposed and attacked, which ABSENT denied |
| 7–8 | $m_e/m_\tau$, $m_\mu/m_\tau$ (shape) | QUANT ×2 | F175, F234, F120, F348 | ≤0.007 % with zero shape parameters. F348 establishes the residual is a **measurement floor**, not a gap owed a next-order correction. Held at QUANT rather than promoted: nothing in the model is undetermined, but the row is still validated against a tolerance |
| 9 | Charged-lepton overall scale | FIT (N=1) | F121, F233, F351 | τ-anchored; F233 reduces the gap to factor 1.9 via the α_s transmutation channel — **inherits d₁** |
| 10–13 | CKM 3 angles + 1 phase | **ABSENT ×4** | — | Declared out of scope in the public summary; $J(1)=0$ is one-generation arithmetic, not a prediction. Ledger **E7**, re-checked 2026-09-02 |
| 14 | $\alpha_\text{em}$ | OPEN | F127, F339, F349 | Four-avenue no-go. **F339 gives each avenue a named reopening condition** plus two concrete unattempted attack surfaces; F349 corroborates from an independent, previously-uncited line (exact all-orders zero-stiffness theorems). Still not derived — but no longer a bare no-go |
| 15 | $g_2$ / $\sin^2\theta_W$ | QUANT | F138, F49, F231 | Derived with scale, +0.222 %, 0 parameters. Still downstream of the $v$ anchor via $\mu_\star=4\pi v$ |
| 16 | $g_3$ / $\alpha_s$ | PARTIAL | F144, F239, F287, F280, F303, F325, F337, F350 | X1 closed; **L6 closed (F337)**; d₁ leg 3 the sole remaining blocker. $\alpha_s(M_Z)=0.1186$ |
| 17 | $v$ | FIT (N=1) | F119, F351, Scope | Anchor, not output; carries $m_W$, $m_Z$ absolutely. **F351 answers L3/F232's standing question directly**: $v$ is *not* a second dimensionful pin for $G$ — the question collapses back onto d₁ |
| 18 | $m_H$ | OPEN | F73, F74, F77, F352 | Kinematics exact; binding dynamics missing. Ledger **E8**. F352 is a quantified negative: RG-improving the Cooper-pair compositeness condition from the model's own UV cutoff predicts $m_t=226.56$ GeV (+31.3 %) and $m_H=248.76$ GeV (+98.6 %) |
| 19 | $\theta_\text{QCD}$ | PARTIAL | F321, F53, F340 | No longer independent; $\bar\theta=\theta+\arg\det M_q$, first term now **exactly** zero non-perturbatively (F340). Reduces to rows #1–6, still OPEN |
| 20–21 | 2 light-ν mass ratios | MACHINE ×2 | F236 | $E_g$/ℤ₃ texture fixes masses and hierarchy at machine precision |
| 22 | ν absolute scale ($M_R$) | OPEN | F47, F343, Scope | Nothing fixes $M_R$ — and F343 now shows that as a reasoned three-leg null, not an unattempted gap |
| 23–25 | 3 PMNS angles | EXCLUDED ×3 | F254 | Proven no lattice selector — three inequivalent 1-d irreps under $D_{2h}$. Permanently free: a result |
| 26 | ν Dirac CP phase | EXCLUDED | F353 | F254's no-go transfers verbatim: the $D_{2h}$ stabiliser transports a complex $T_{2g}$ entry by the same real sign as a real one. $J=0$ is a consequence of real-only inputs, not a protected value |
| 27 | $G$ | EXACT | F79, F107 | Structural, 3e-8 vs CODATA, 0 free parameters |
| 28 | $\Lambda$ | OPEN | F164, F192, F193, F196, F241, F311, F319, F332, F367, F368 | Price met to 0.10 dex; the *dynamics* is the open item. F332 closed both local channels structurally; **F367 supplies the first mechanism that works** (exact sequestering selectivity, sympy-verified) but it is imported and **not adopted**; F368 prices two further undischarged costs (spatial closure, transience). See priority #4 |

**Ledger tally.** Derived with zero free parameters: **6** (#7–8, #15, #20–21, #27). Partial, one
named residual each: **2** (#16, #19). Fitted / free input: **2** (#9, #17). Open: **10** (#1–6,
#14, #18, #22, #28). Absent: **4** (#10–13). Excluded — permanently free, a result: **4** (#23–26).
Total 6+2+2+10+4+4 = **28**, checked.

*(The baseline printed "fitted or free input: 3 (#9, #14, #17)" while grading #14 `OPEN` in the same
table. Counted by grade here, α_em sits in OPEN and the fitted bucket is 2. No quantity moved; the
double-count is corrected.)*

**How to read that against the SM's 19.** Not "6 beats 19". The model derives 6 quantities the SM
takes free, proves 4 more **permanently free** (a result, not a gap), and does not yet close 14 — of
which 10 are quark masses and CKM. **Chain vs count, updated:** $\sin^2\theta_W$ (#15) still sits
downstream of the $v$ anchor, and **F351 has now checked and confirmed** that $v$ is not itself
pinned by a second dimensionful scale — the question collapses onto d₁. $\alpha_s$ (#16) is blocked
by d₁ alone now that L6 has closed. $\theta_\text{QCD}$ (#19) reduces to the quark-mass texture,
i.e. rows #1–6, now OPEN rather than ABSENT. The charged-lepton scale (#9) also inherits d₁. So
"zero free parameters in the sectors we built" remains true of the *count* and not of the *chain*,
and the chain has narrowed to two links: **$v$ and d₁**.

### E — Gravity and general relativity

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| E1 | Fundamental field equation | POSIT | F178, F297, F345, F383 | the posit itself (F345's one-sentence premise; the two named sub-items inside it are now both closed-negative rather than open — metric-only-LHS by F345 §6, at-most-second-order by F383/CN28) | DECISION 2026-06-29. **F345 narrows it substantially**: at two-derivative order the LHS is *forced* by Lanczos–Bach in the model's own derived $d=3+1$, and the full-tensor source is forced. **F383 (2026-09-10)** attacked whether lattice locality could forbid the four-derivative term outright (which would have promoted at-most-second-order to a derivation): extending F57's own BZ polarization one order further gives a robustly nonzero $\Pi_4$, so locality *generates* the higher-derivative tower rather than forbidding it — closed negative (ledger **CN28**), row stays POSIT for the reason F345 already gives. Ledger Part C row **E1g**; CL292 |
| E2 | Equivalence principle | MACHINE | F64, F62 ⚠(S3→F64) | — | — |
| E3 | PPN β, γ | EXACT | F64 | β=γ=1 exactly | GR-identical |
| E4 | Classical tests | QUANT | F64, F107, F111 | 3e-8 | Mercury, deflection, Shapiro, redshift |
| E5 | Newton's constant | EXACT | F79, F107 | 3e-8 vs CODATA | Structural, zero free parameters. F355 re-reads what the horizon constant grades as the model's own **induced** $1/G$ — $G$ itself untouched |
| E6 | GW speed, polarisations, dof | EXACT | F180, F248, F216 | ≤3e-83 | $c_\text{grav}=c_\gamma$ a genuine zero |
| E7 | Inspiral / ringdown QNM | QUANT | F189, F187 | <7 % (WKB) | GW150914 chirp mass, ISCO |
| E8 | Black holes | EXACT | F183, F186 | 0 — $b_c=3\sqrt3\,M$ exact, 0 % vs GR | Exact Schwarzschild/Kerr with horizon (Birkhoff ⇒ exact vacuum solution). The +4.63 % shadow belonged to the withdrawn F114 object, replaced by F178. Cross-checked by F183's photon-sphere solve (7.0e-11) and F186's independent ray-trace (1.45e-5); both floors are integrator truncation |
| E9 | BH thermodynamics | PARTIAL | F190, F183, F300 §5, F355 | the two routes to the induced $1/G$ **disagree** by a bracketed factor | $S=A/4$ iff each cell carries $2\pi\sqrt3$ nats; F300 proves the state-count reading impossible (CN20). **F355 computes the constant rather than positing it** — and the entanglement route and F79's heat-kernel route to the same quantity disagree (CL296 puts the model's own vacuum at ≈3.18× Bekenstein–Hawking). Ledger **G4**. Sharper and worse |
| E10 | Singularity resolution | PARTIAL | F183 §L1, F284 §5, F354 | core *scale* contingent on three named inputs | **The named gap is closed**: F354 proves the lattice-regulated core is **geodesically complete**, exact-algebraic, and that the curvature bound alone forces it (the Kretschmann scalar is a sum of squares). CL295 `contingent`. Grade holds because the scales, not the completeness, now carry the contingency |
| E11 | Interior / TOV / NS EoS | QUANT | F181, F184, F185, F356 | — | SLy $M_\text{max}=2.08\,M_\odot$, $R(1.4)=11.1$ km. F356 adds multi-EoS robustness against current NICER/PSR data: SLy, AP4 (corrected), MPA1 all pass |
| E12 | Quantum-gravity sector | QUANT | F216, F248, F79, F357, F359 | no scattering amplitude, cross-section or partial-wave bound computed; the hoop/geometric criterion not computed | Graviton massless, 2 dof (exact). F357: the paired photon/graviton band top is $\Omega_\text{max}=\pi$ **exactly**, $E_\text{max}=0.8247\,E_\text{Planck}$ (CL297). F359: two band-top quanta collide at exactly $\sqrt\pi\approx1.77\times$ the rest energy of the model's own one-cell Planck-mass remnant — clearing the *energetic* precondition of classicalization (Dvali–Gomez), explicitly not the geometric one (CL298) |
| E13 | Galactic-scale consistency | EXCLUDED | F194, F191, F358 | — | Emergent-gravity route falsified by Bullet Cluster; dark source required. **Re-examined 2026-09-03** (F358, ledger S23) against the live 2026 Hernandez/Famaey MOND-QUMOND dispute and the JWST-refined offset (Rihtaršič et al. 2026): exclusion survives; F194's "regardless of clump shape" over-claim withdrawn |

### K — Cosmology

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| K1 | FRW background | QUANT | F182, F188, F284, F360 | measured Ω's in; dynamics not derived | Solved *with* the model's source, not derived *from* the lattice. **F360 is explicit that it does not promote the grade**: F284 closes the *ontology* of expansion, not its *dynamics*; the Jacobson/Cai–Kim horizon-thermodynamics argument reproduces Friedmann independently but quasi-statically |
| K2 | BBN / light elements | PARTIAL | F297, F309, F361, F372, F79, F178, F182, F284 | $\eta_b$ free; network offset −0.87 % | $g_*(T)$ closed by F309 (CN25); $m_{E_g}>125.5$ MeV bound as a by-product (ledger **E5**). **F361 discharges the ⁷Li leg**: the A=7 rate fits carried transcription errors against their own cited source (Kawano NUC123), and repairing them takes ⁷Li/H from **−92 % to −6.3 %**. Two residuals left of three |
| K3 | CMB peaks, $n_s$ | PARTIAL | F310, F295, F296, F285, F286, F362 | the value of one non-integer block-spin eigenvalue | Model needs no 3D dual; $\gamma\equiv y-1$ identically. **F362** shows fluctuation corrections do **not** move F130's confinement eigenvalue off $b^1$ under F130's own bond-moving convention — the residual survives a real attack. Ledger **G2** |
| K4 | Inflation or substitute | EXCLUDED | F282, F283, F296, F238, F363 | cause named + 4 falsifiers | No slow-roll direction exists; $\Lambda=3^{-1/4}M_\text{Pl}$ exactly, so every compact CA direction carries $M_\text{Pl}^2/f^2\ge\sqrt3$ (CN7), and the elastic-lattice rescue is excluded four ways (CN8). **F363 re-examined it per this rubric's own reopening protocol** and the no-go survives: $a/\ell_\text{red}=3^{1/4}$ unmoved through F362, two further escape-route classes closed |
| K5 | Primordial spectrum normalisation | EXCLUDED | F282, F284, F285, F238 | $A_s$ free, cause named | $P(k)$ is an automaton initial condition |
| K6 | Baryogenesis | PARTIAL | F202, F47, F53, F364 | **magnitude now computed and 10–11 decades short** at the model's own inputs; rescued only by a tuned resonant $\Delta M_{23}$ | **Transformed this run.** F364 replaces F202's Sakharov checklist with a real LO resonant-leptogenesis Boltzmann/QKE computation on the model's **own** F201 masses ($M_2\approx0.40$, $M_3\approx5.60$ GeV) with Casas–Ibarra Yukawas fit to oscillation data: free CP phase caps at $Y_B/Y_B^\text{obs}\approx2\times10^{-11}$ then collapses into strong washout; a sharp Breit–Wigner in $\Delta M_{23}/M$ does exceed observation, but only tuned. **Also computes the tree's first sphaleron B-violation rate.** See priority #3 |
| K7 | Dark-matter identity | PARTIAL | F223, F228, F266, F216, F237, F365 | — | Candidate: graviton–graviton J=2 geon, Planck-mass remnant. F365 sharpens against two 2025 GW papers not previously cited; does not re-derive the identity |
| K8 | $\Omega_\text{DM}h^2=0.12$ | EXCLUDED | F238, F282–F285, F366 | free input, cause named | Provable non-derivability *given no inflaton*. **F366 re-examined it** on F238's own named reopening condition and returns "reopening, scoped and partial — not a closure and not an abundance derivation": the exclusion is scoped to the inflaton/Press–Schechter route, with a structurally distinct domain-wall route flagged. Grade held |
| K9 | $\Lambda$ magnitude | OPEN | F311, F319, F164, F192, F193, F196, F241, F332, F367, F368 | a mechanism **of the model's own**; adoption of an imported one is an open decision | F332 closed both *local* channels structurally (Fredholm-blind to a homogeneous source; block-spin wrong by 35+ decades). **F367 supplies the first positive result**: Kaloper–Padilla spacetime averaging annihilates a spacetime-constant source **exactly**, sympy-verified, unbounded selectivity — but it is imported machinery grafted onto decision 4's action and is explicitly **not adopted** (CL303 `contingent`). F368 checked CL303's falsifier 4 (PPN/F178/induced-$G$ not in tension) and added two undischarged costs: spatial closure ($k>0$) and transience. **Graded OPEN, arguably PARTIAL** — the seam is now named, but the model itself still has no mechanism, so promoting would credit the model with an import. See priority #4 |
| K10 | Dark energy $w$, vs DESI | PARTIAL | F192, F203 | sign exact; magnitude open | $w=-1$ sign correct; C2's "vacuous" reading stays conditional. **Live external pressure** (searched 2026-09-08): DESI DR2 prefers evolving dark energy over ΛCDM at **3.1σ** (BAO+CMB) and **2.8–4.2σ** with SNe depending on sample, favouring $w_0>-1$, $w_a<0$ — arXiv:2503.14738 (2025). The model's CN24 gives $\mu=1$, $\partial_k\mu\equiv0$, $\dot G/G\equiv0$ with **zero free functions**, so a confirmed evolving $w$ is a live falsifier, not a fitting opportunity |
| K11 | Structure formation / $\sigma_8$ | PARTIAL | F288, F369 | $A_s$ free; EH98 $T(k)$ still imported | Zero free functions vs EFT-of-DE's two (CN24); DES Y6 falsifier live (3.00σ). **F369** moves toward a model-native replacement for EH98: the sound horizon integrated on the model's own background lands **0.11 %** from the imported value, with S1/S2 exact-algebraic. Ledger **S2** item (i) partially narrowed |
| K12 | Cosmological initial conditions | PARTIAL | F284, F285, F286, F295, F296, F238, F310, F362 | one anomalous dimension, now internal | Same operator as K3; F362 applies here identically |

### G — Emergent and precision physics

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| G1 | Maxwell / classical EM | EXACT | F26, F87, F245, F246, F306, F314; F25 ⚠(S18→F306) | 0 | Composite-photon curl closes at $O(k^3)$ exactly, coefficient $c_\text{lat}^3/48=1/(144\sqrt3)$ (CN L5) |
| G2 | Hydrogen, fine structure, Lamb | QUANT | F125, F252, F257, F262, F370 | Lamb = 99.5 % of measured; **a distinct, larger, untouched self-energy gap now named** | −13.596 eV from $m_e+\alpha$ alone; Bethe logarithm from the model's own Coulomb spectrum. **F370 re-scopes the residual**: the "two-loop $\alpha(Z\alpha)^5$-class, out of scope" note is traced to the same missing ingredients F336 named for B9, **plus** a separate and larger self-energy gap nobody had named. No residual closed — the row's debt is bigger than it looked |
| G3 | $g-2$, electron and muon | PARTIAL | F252, F261, F334 | hadronic VP / HLbL / EW absent by **declared** scope | $a_e=\alpha/2\pi$ exact; muon QED through two loops ($A_2(\mu)=0.765857$ vs 0.765857410). F334's ρ+ω VMD captures ~10.2 % of $\Delta\alpha_\text{had}^{(5)}(M_Z)$ with zero imported couplings; φ, the multi-hadron continuum and charm/bottom entirely absent. Explicitly disclaimed in the summary's Scope |
| G4 | Atomic structure / periodic table | QUANT | F148, F195, F208, F371 | Hartree/no-exchange underbinding persists | H/He/Li/C certified stable. **F371 extends the relativistic SCF ionization-energy map from Z=1–20 to the full 3d series (Z=21–30, Sc–Zn)** — real coverage growth; the systematic underbinding is unchanged and now measured over a wider range |
| G5 | Hadron spectrum | QUANT | F123, F124, F235, F122, F297, F372 | 1 anchor ($f_\pi$); $\sqrt\sigma/f_\pi$ +12 % (inherits d₁) | **The 36.6σ defect is gone.** F372 (2026-09-05) shows the model's $m_n-m_p$ is not wrong — the *exclusion statistic* was: propagating the literature's own theory uncertainty (BMW 2015, ±0.280 MeV) takes it from **36.6σ to 0.77σ**, with three methods sharing no common fit clustering on 0.97–1.04 MeV for the EM term. Ledger **Q4 CLOSED** |
| G6 | Nuclear binding | QUANT | F104, F113, F126, F128, F240, F206, F373 | b = 0.55 fm — **no longer an independent parameter** | Deuteron $E_b$ 0.026 %, $r_d$ 0.4 % with no tuned core (CN Q3). **F373**: the OBE quark-size regulator b = 0.55 fm matches the model's own gauge-derived confinement radius, so it is not independently tuned. Held at QUANT — this is a consistency/insensitivity check, not a derivation |
| G7 | Weak decays | PARTIAL | F54, F48, F297, F372 | absolute rates tied to $v$; $\tau_n$ | Same sector as G5. F372's correction removes the $m_n-m_p$ input defect that fed this row's residual; the $\tau_n$ discrepancy has **not** been separately re-measured against the corrected statistic and is carried, not re-verified |
| G8 | Scattering / S-matrix | MACHINE | F260, F259, F263, F264, F258 ⚠(S12→F277) | — | Tree QED S-matrix, crossing, IR cancellation; $Z_1=Z_2$ a computed identity via the differential Ward–Takahashi identity |
| G9 | Condensed-matter emergents | QUANT | F210–F215, F218, F242, F207, F171, F374, F375 | Allen–Dynes **4.9 %** (was 6.3 %) | $\mu^*$ derived from the F64 dielectric, no fit (CN S1). **F374 closes the Eliashberg-solver/cutoff route as a NO-GO** (a real cutoff bug narrows it to 17 %, not below target) and names the actual next step; **F375 takes it**: a real DFT-sourced $N(0)$ for Nb crosses the target, 6.3 % → **4.9 %** |
| G10 | Statistical mechanics / thermodynamics | PARTIAL | F300, F309, F376 | ETH onset characterised, not a full thermalisation theorem | $w=1/3$, Stefan–Boltzmann theorems; the free sector **cannot** thermalise — $2N$ conserved $n_\pm(k)$ fix a GGE, and the arrow is the initial condition (CN21). **F376 delivers the row's first interacting-sector result**: the GGE breaks down toward genuine ETH thermalisation once an integrability-breaking interaction is on — the open next step F300 §4.1 and F309 §7.2 both named |

### H — Model integrity

| # | Requirement | Grade | Evidence | Note |
|---|---|---|---|---|
| H1 | Parameter count vs SM's 19+ | PARTIAL | ledger above | 6 derived, 4 proven-permanently-free, 2 partial, 2 fitted, 14 open or absent. Movement this run is **#1–6 ABSENT → OPEN** (F346/F347) and the fitted/open double-count corrected. Chain-vs-count caveat now names exactly two links: **$v$** (F351 confirms it is not itself pinned) and **d₁** |
| H2 | Falsifiability | PARTIAL | `docs/claims/` (305 cards, **0 without a falsifier**), `tests/registry/` (485 records, gate 114), live `make health` + `check_control_soundness.py` | **Register half strong and growing**: 305 cards, every one carrying a falsifier, 42 headline. **Instrument half is mixed**: 111 gate-tier assertions (was 82), 155 declared controls (was 91), **NO CONTROL 37 — down from 48, the first movement since 2026-08-08**. But of 155 controls, **151 verified RED, one is journalled NOT SOUND** (`F350#control0` — *"a control naming a leg the driver no longer emits has silently stopped testing"*) and **three verdicts are STALE** (F345 ×3). A separate pre-existing can-fail ratchet sits at 6 vs ceiling 5: six gate entries with no verdict key and no reachable assert, i.e. **they pass unconditionally regardless of content** (F283, F285, F286, F295, F296, F345). Grade held — a shrinking backlog alongside rotting controls is not a net gain |
| H3 | Out-of-sample survival | QUANT | Claims rev 7 | $m_Z/m_W=3/\sqrt7$ fixed before PDG 2025 excluded CDF-II $m_W$: −0.064 %. Still the only clean instance. F358's Bullet-Cluster re-examination against 2026 data is a second, weaker instance (an exclusion surviving new data, not a prediction confirmed) |
| H4 | Retraction hygiene | PARTIAL | `supersessions.yaml` S1–S23; `check_superseded_citations.py`; `check_summary_claims.py` (generalized to `GRADED_FILES`); summary rev 7 | The `papers/README.md` defect this row named is fixed — the file had been deleted whole in the unrelated commit `c142d1c`, was restored, and its headline numbers brought current to rev 7 with `<!-- claims: CLnnn=status -->` anchors now machine-checked. A sweep for the same defect shape elsewhere found none. **Held at PARTIAL, not raised**, per this row's own standing note: removing the one instance the audit named is not the full-surface audit it called for. 25 withdrawn cards remain in-tree, correctly |
| H5 | Internal consistency of decisions | MACHINE | key-decisions.md D1–D12; `open-derivations` Part D | All three historically-named live items closed; Part D tallies **Contradictions: 0** and says "Nothing further — it is closed". Re-verified this run against the live ledger. `MACHINE` not `EXACT`: the invariant is enforced by reading a maintained ledger, not a closed-form guarantee |
| H6 | Reproducibility | **OPEN** | live `make gate` (**RED, 10/33**), `make indexes-check` (GREEN), `gen_test_registry.py --check` (STALE ×6), `audit_numerics --ratchet` (FAILED), `audit_tests --ratchet` (FAILED), `check_control_soundness.py` (FAILED ×4) | **REGRESSION — see the Regressions table and priority #1.** Three reports carried this as PARTIAL "pending a genuine green gate run". The gate ran this session and is **red on four substantive checks**, plus six pytest-import failures caused by `Makefile:10` overwriting the vendored `PYTHONPATH`, which makes the *documented* invocation run in `reduced mode` while still emitting a verdict. Indexes are green and the tree is committed; the barrier is not. Full-mode gate result remains unknown (exceeds the bridge's 180 s budget once pytest loads) |
| H7 | Module coverage | PARTIAL | D11 registry, live: 254 modules, **52 driven (20.5 %)**, 24 unreferenced; `docs/audits/module-disposition-2026-09-06.md` | Fourth consecutive fall in the driven *fraction* (51/218 = 23.4 % → 52/254 = 20.5 %) — the denominator is growing faster than the channel wiring. **Mitigating and checked**: the 2026-09-05 audit read all 34 newly-registered modules and both full non-driven pools and found every one correctly non-driven by design (one-off derivation kernels closing a specific finding, or `fork_unclaimed` forks). Two pre-existing wiring gaps unchanged (`lpt_generator`, `qed_casimir_materials`) |
| H8 | Findings without a usable test record | **PARTIAL** | `findings-index.md` (`no test record`: **5**), `make coverage` (FAIL ×3 ceilings), `**Checked:**` header audit | **REGRESSION from MACHINE — see the Regressions table.** Five findings carry no test record (F358, F363, F364, F368, F370) against a ceiling of 0; `make coverage` breaches `unjoined 2`, `weak_only 2`, `untested 2`; and 15 of the 51 new findings lack the `**Checked:**` attack-pass header CLAUDE.md requires by any authoring route. F364 is the most consequential of the five — it is a new quantitative cosmology result (priority #3) with no record binding it |

*Every row above whose grade is not `EXACT` or `MACHINE` has a prompt in
`completeness-2026-09-08-prompts.md` under the anchor of the same row ID.*

---

## Method notes

**Live this run** (device bridge, real repository, one target per call): `make indexes-check`,
`make registry`, `make numerics`, `make health`, `make coverage`, **`make gate` (completed, RED)**,
`tools/audit_tests.py --ratchet`, `tools/audit_numerics.py --ratchet`,
`tools/gen_test_registry.py --check`, `tools/check_control_soundness.py`, the D11 module-registry
reach/status query, `git status` / `git log`, and the whole-tree ABSENT keyword sweep. The command
file assumes a ~45 s per-call budget; the actual budget on this bridge is ~180 s, which is the only
reason the gate ran — worth recording for the next session.

**What could not be verified.** The **full-mode** gate (with pytest on the path) exceeds 180 s and
was killed at 150 s with no usable log; only the reduced-mode run completed. So the pytest half of
`tests/casim/` has **not** been verified green or red this session — what is established is that
the four non-pytest checks fail in either mode. `make control --run` (re-verifying all 155 controls
against the current fingerprint) was also not run in full; `check_control_soundness.py` reports its
journalled verdicts, which is how the one NOT SOUND and three STALE entries were found.
Background/`nohup` processes do **not** survive between bridge calls — confirmed again this run, as
in the 2026-08-20 report.

**Rows that needed a finding file rather than the ledgers.** F335 (B7 — whether reflection
positivity closes confinement: it does not, and the finding says so), F364 (K6 — the actual $Y_B$
numbers, which appear in no index), F367/F368 (K9 — whether the sequestering mechanism is the
model's own: it is not), F341 (C4), F346 (D#1–6), F348 (D#7–8), F354 (E10), F355 (E9), F361 (K2),
F372 (G5), F373 (G6), F375 (G9). Everything else graded from `open-derivations.md`,
`findings-index.md`, the claims registry and the changelog.

**Spot-checks — the three grades I was least sure of, and what the check found:**

1. **K9 `OPEN`, against a case for `PARTIAL`.** F367's status line reads *"Positive on the
   mechanism's core selectivity claim (exact, sympy-verified); negative/honest on adoption."* Read
   §7 directly: *"Does not: adopt sequestering as part of this model's gravity sector. Doing so
   would graft new global, non-propagating Lagrange-multiplier fields onto the CLAUDE.md decision-4
   action — imported machinery, not derived from the CA."* Held at `OPEN`. Promoting on an
   explicitly unadopted import would credit the model with a mechanism it does not have — the exact
   H4 failure shape this rubric grades. The argument for `PARTIAL` is real and is stated in the row.
2. **B7 `PARTIAL`, against a case for promotion on F335.** F335 supplies precisely the machinery
   F323's repo-wide grep had found wholly absent, which looked like a promotion. The finding's own
   scope section settles it: *"No mass gap, no area law, no confinement verdict. Reflection
   positivity is a necessary ingredient for Osterwalder–Schrader reconstruction — it is not by
   itself a statement about the spectrum of that transfer matrix."* Grade held; residual rewritten.
3. **H8 `MACHINE → PARTIAL`.** Verified against the repository rather than the changelog:
   `grep -c "no test record" findings-index.md` returns **5** (was 0 at the baseline, verified the
   same way), naming F358, F363, F364, F368, F370; `make coverage` independently breaches three
   ceilings. Also audited the `**Checked:**` header across all 51 new findings — 36 have it, 15 do
   not. The regression is real and is new work outrunning its own integrity convention, not a
   measurement artefact.

**Baseline hygiene.** The 2026-08-20 report has been amended **in place** seven times, through
2026-09-06, with post-dated inline updates. Two of those amendments (A6 → EXACT, E8 → EXACT) never
reached its own scoreboard, which that file acknowledges about itself. The corrected baseline
(16/5/17/30/0/1/1/4) is what this run's movement is measured against; using the printed totals would
have manufactured two promotions that had already happened. **Recommendation, not an action taken
here:** amending a dated report in place makes the delta computation in this command unreliable. A
future amendment is better issued as a new dated report.

**A note on `result_dump` baselines.** 231 of 485 test records fail by baseline diff against
`git HEAD`. A stale `.git/index.lock` blocked every git write from 2026-08-19 to 2026-09-05 —
**18 days** — during which that failure mode could not have been exercised meaningfully, and the
394-file backlog was committed in one commit (`ed51277`, 2026-09-06). Nothing here says a baseline
is wrong; it does mean the drift protection was effectively dormant across most of the window this
report covers, and `make drift` after a genuine physics re-run is worth one session.

**Citations to superseded findings** are carried with their supersession inline (⚠): F165 (S13→F279),
F62 (S3→F64), F251 (S12→F277), F115 (S20→F138/F231), F94 (S21→F323/F265), F25 (S18→F306),
F258 (S12→F277). All F-numbers cited in this report were verified to exist in `findings/`.

**External literature this run** (searched 2026-09-08, all with provenance, none of it the model's
own): PSI nEDM collaboration (Abel et al.), PRL **124**, 081803 (2020), arXiv:2001.11966 —
$d_n=(0.0\pm1.1_\text{stat}\pm0.2_\text{sys})\times10^{-26}$ e·cm, quoted bound
$\lvert d_n\rvert<1.8\times10^{-26}$ e·cm (90 % CL). Super-Kamiokande I–IV, arXiv:2010.16098, PRD
(2020) — $\tau/B(p\to e^+\pi^0)>2.4\times10^{34}$ yr, $\tau/B(p\to\mu^+\pi^0)>1.6\times10^{34}$ yr
(90 % CL), 450 kton·yr. DESI DR2, arXiv:2503.14738 (2025) — dynamical dark energy preferred over
ΛCDM at 3.1σ (BAO+CMB), 2.8–4.2σ with SNe, favoured quadrant $w_0>-1$, $w_a<0$.

**Prompt coverage ratchet.** Rubric 74 + D-ledger 28 = **102** rows. At ceiling: rubric EXACT 16 +
MACHINE 4 = 20; ledger EXACT 1 (#27) + MACHINE 2 (#20–21) = 3; total **23**.
102 − 23 = **79** rows need a prompt. `completeness-2026-09-08-prompts.md` covers **79** rows in
**67** sections (grouped ledger entries: #1–6, #7–8, #10–13, #23–26) — **match**.

**Not edited by this run**, per the command's own standing rule: `open-derivations.md` and
`exactness-inventory.md`. Two items in the former are stale as of this sweep and a research session
should act on them — (i) the sector tally still reads "Contradictions: 0 / OPEN rows 17" without the
two ABSENT items this run surfaced (proton decay / B-violating rate; the neutron EDM), which belong
in Part A; (ii) row **E6** is now correctly OPEN but its "Suggested attack" column predates F346/F347
and still proposes the transplant those two findings closed.
