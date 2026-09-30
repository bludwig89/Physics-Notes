# /monograph — Build the complete derivation monograph

Read the whole model and write it out as one continuous body of physics, from first
postulates to the present edge of what we have built, with every derivation shown in
full. The target is **reconstruction**: a competent physicist with this document and no
access to the repository must be able to rebuild the theory from scratch — every
postulate stated, every step shown, every constant derived or declared as an input.

**Scope:** physics derivations. The code is *cited* (module name, finding, test record)
but not specified — a rebuilder re-derives the physics and writes their own numerics.
Do not turn chapters into API documentation.

**This command writes documentation only.** It creates no finding, no claim card, no
module, no test record, and changes no physics. If the read turns up a genuine error or
contradiction in the model, it goes in the gap ledger (§8) — you do not fix it here.

Arguments (`$ARGUMENTS`):

| Form | Effect |
|---|---|
| *(empty)* | Full build: Phase 0, approval, then every chapter |
| `outline` | Phase 0 only — write the plan and stop |
| `resume` | Read `BUILD-STATE.yaml`, continue from the first chapter not `done` |
| `ch:N` *(or `ch:N,M`)* | Rebuild only those chapters, overwriting them |
| `--auto` | Skip the approval gate in Phase 0 (for unattended runs) |

---

## 0. Output layout

Everything lands in `docs/monograph/`:

```
docs/monograph/
  README.md            # what this is, how it was built, how to read it, the tag legend
  00-plan.md           # the chapter spine + source map (Phase 0 product)
  BUILD-STATE.yaml     # resumability ledger — one record per chapter
  NN-<slug>.md         # one file per chapter, numbered in derivation order
  A1-no-go-ledger.md   # appendix: every excluded route
  A2-supersessions.md  # appendix: what replaced what, and when
  A3-constants.md      # appendix: every constant, closed form, provenance, exactness
  A4-open-residuals.md # appendix: what is not closed, with its size
  A5-symbols.md        # appendix: notation and symbol glossary
  GAPS.md              # things the repo could not source — the honesty file
```

One chapter per file. Do not build one giant markdown file; it cannot be reviewed,
resumed, or regenerated chapter-wise.

---

## 1. Read order — before anything else

Load, in this order, and do **not** skip any of them:

1. `CLAUDE.md` — the six core design decisions are the spine of Part I–IV
2. `INDEX.md` — the map
3. `docs/theory/key-decisions.md` — D1–D12 plus the physics decisions and *why* each was taken
4. **`docs/theory/supersessions.yaml`** — load-bearing, see §3
5. `claims-index.md` — what the project asserts **right now**
6. `findings-index.md` — the whole finding list, one line each
7. `docs/status/exactness-inventory.md` — the exact / machine-precision / quantitative split
8. `docs-index.md` — theory docs, papers, reference summaries
9. `papers/README.md` and the Paper-01…12 series — these are prior attempts at exactly this
   document, at lower resolution. Use them for the *spine*, never as a source of fact:
   they predate later findings and some of what they say has been superseded.
10. `docs/status/project-status.md` and `tail -n 200 docs/status/changelog.md`

Do **not** read `findings/` wholesale. It is ~400 files and several million tokens.
Chapters pull the findings they need, by number, from the index.

`references/physics-notes-complete.md` (~44k tokens) is Mark Ludwig's original notes —
the historical seed of the model. Read it only in the Foundations and Higgs-free-mass
chapters, where provenance matters, and attribute it as *source material*, not as a
result of this project.

---

## 2. Phase 0 — the spine

Produce `docs/monograph/00-plan.md` before writing a word of physics.

**Order chapters by derivational dependency, not by finding number.** F-numbers record
the order in which things were *discovered*; the monograph presents the order in which
things are *derived*. A chapter may only use results established in an earlier chapter,
in a stated postulate, or in cited external measurement.

Proposed spine — **verify and adjust it against the indexes; add, split, merge or
reorder as the actual dependency graph demands, and record every change you make in
`00-plan.md` with its reason:**

| # | Chapter | Core question |
|---|---|---|
| 1 | Postulates and ontology | What is assumed, and what is the beable? |
| 2 | Why 3+1 dimensions, why this lattice | Dimension count, BCC selection, lattice constant, point symmetry |
| 3 | The update rule | The walk, one time dimension, the update commutant, locality |
| 4 | Structural theorems | Reflection positivity, CPT, spin–statistics, cluster decomposition |
| 5 | Quantum structure | Born rule, pointer basis, measurement, classicality |
| 6 | Free propagation and the light cone | Dispersion, c_lat = 1/√3, rotation-rate reading of c |
| 7 | Relativity on a lattice | Boost covariance, velocity addition, LIV coefficients, the observational bounds |
| 8 | The photon | Pairing classification, the paired-spinor photon, why the σ-bilinear photon is excluded |
| 9 | Electromagnetism | Charge coupling, the conserved current, the link-covariant step, the A-field convention |
| 10 | Photon ↔ fermion | The coupled channels and the push — the live edge |
| 11 | Mass without a Higgs | Complex mass, chiral SU(2) from β-gauging, Ludwig's construction |
| 12 | Hypercharge and the electroweak sector | U(1)_Y on U(x), anomaly cancellation, W/Z, the Weinberg angle, absolute boson masses |
| 13 | Colour and the strong sector | SU(3) structure, why three colours, dielectric confinement, α_s, the string tension |
| 14 | Hadrons | Pion, nucleon, deuteron, the NN potential |
| 15 | Generations and the lepton spectrum | Three generations, the crystal-field hierarchy, Koide, the 2/9 shape angle |
| 16 | Neutrinos | Seesaw, Majorana closure, PMNS, δ_CP |
| 17 | Scale setting and SI closure | The lattice spacing, mass-scale transmutation, √σ/f_π, the SI anchor |
| 18 | Gravity | Rest-leg back-reaction, structural G, the induced Einstein equation, the dielectric representation |
| 19 | Strong-field and wave gravity | GW speed, the TT graviton, black holes, neutron stars, ringdown |
| 20 | Cosmology | Friedmann sector, BBN, structure formation, the inflation no-go |
| 21 | The cosmological constant | The problem, the dilution exponent, sequestering, what remains |
| 22 | The dark sector | Sterile neutrinos, the spin-2 mode, geons, relic abundances, falsifiers |
| 23 | QED precision | Vacuum polarization, running α, a_e/a_μ, Lamb shift, the comparison battery |
| 24 | Atoms and matter | Bound electrons, many-body atoms, ionization energies, block-spin elements |
| 25 | Emergent condensed matter and information | Superconductivity, entanglement, the quantum-computing cross-tests, thermodynamics |

For each chapter, `00-plan.md` records: the chapter title, the question it answers, the
**ordered** list of source findings (`F###`), the claim cards (`CL###`) that rest on it,
the theory docs and papers that cover it, its upstream chapter dependencies, and a
one-line statement of what a reader can derive after reading it.

Then check the spine for **coverage**: walk `findings-index.md` top to bottom and confirm
every finding is either assigned to a chapter, assigned to an appendix (no-go,
supersession), or explicitly listed in `00-plan.md` under "deliberately out of scope"
with a reason (engineering-only findings, tooling, scenario-language work, GUI). No
finding may be silently dropped.

**Stop here and show the user the spine** — chapter list, coverage count
(assigned / no-go / superseded / out of scope / total), and any reordering you did
against the proposal above. Wait for approval before Phase 1. Skip this gate only on
`--auto`.

---

## 3. The supersession rule — read this twice

> A finding is **past tense**: what a session concluded, and it is never rewritten.
> The monograph is **present tense**: what the model asserts now.

Writing a chapter from a finding file alone will document physics the project has since
abandoned. Before any chapter is written, its findings are checked against
`docs/theory/supersessions.yaml` and `claims-index.md`.

The rule for each result:

- **Live** — derive it in full, in the main line of the chapter.
- **Partially superseded** — derive the part that stands; say precisely which part moved,
  to what, and in which finding. Do not present the whole as live.
- **Fully superseded** — it does **not** appear in the main line. It appears in the
  chapter's "What was excluded" section (§5) and in `A2-supersessions.md`, with the
  successor named.
- **Contradiction between two live findings** — do not adjudicate it yourself. Document
  both positions, mark it in `GAPS.md`, and carry on.

Known traps to check explicitly, and you will find more:

- The σ-bilinear composite photon is superseded for the photon by the paired-spinor
  photon (F65–F69) but **retained** for W/Z/gluon. A chapter that says "the photon is a
  σ-bilinear" is wrong; one that says "the σ-bilinear construction is dead" is also wrong.
- Gravity's canonical law is the induced Einstein equation with a full stress-energy
  source (F178). The exponential dielectric K is the **vacuum/weak-field representation**,
  not the interior field equation, and the F114 horizon-free black hole is superseded.
- The lepton shape angle: δ* = 2/9 is **primary**, λ₆ is an **output** (F234 arrow), and
  F179's relabelling is superseded by F253/F255/F256. Getting the arrow backwards turns a
  derivation into a fit.
- The cosmological constant: F193 Part A is *excluded*; Part B / the F196 dilution
  exponent is the live route. Check the later CC findings before writing that chapter.

---

## 4. Chapter build — one subagent per chapter, cold

Dispatch each chapter to its own subagent. The parent keeps the spine, the ledger, and
the cross-chapter consistency pass; it does not hold chapter text in context.

Each subagent gets: the chapter's row from `00-plan.md`, the postulate list and symbol
table from Chapter 1 (once it exists), the "results available from earlier chapters"
list, this file's §3, §5 and §6, and instructions to write **the file** and return only
a short report — what it wrote, what it could not source, what it found superseded, and
any new symbol it introduced.

Chapters whose dependencies are satisfied may run in parallel; a chapter never starts
before the chapters it depends on are `done`, because it must cite their numbered
results. Chapter 1 runs alone and first: it fixes the postulate numbering and the symbol
table that every later chapter cites.

After each chapter returns, the parent updates `BUILD-STATE.yaml`:

```yaml
chapters:
  - n: 6
    slug: free-propagation
    status: done            # pending | in_progress | done | blocked
    findings: [F20, F25, F26, F30, F245, F306]
    results: [R6.1, R6.2, R6.3]      # numbered results this chapter established
    new_symbols: [Omega, c_lat]
    gaps: 1
    built: 2026-09-16 - 14:20
```

Write the ledger after **every** chapter, not at the end. A session that dies mid-build
must be resumable with `/monograph resume` and nothing else.

---

## 5. What a chapter must contain

Every chapter, in this order:

1. **Title and one-paragraph statement** of what the chapter establishes.
2. **Inputs.** Three explicit lists, and they are not optional:
   - *Postulates used* — by number, from Chapter 1.
   - *Prior results used* — by result number (`R12.3`), from earlier chapters.
   - *Free inputs consumed* — every number that enters this chapter without being
     derived: measured values used as anchors, fitted parameters, bracketed constants,
     conventions. State for each whether it is an anchor (calibration against
     measurement), a fit, or a convention. **A derivation that quietly consumes a free
     parameter is the single most damaging failure this document can contain.**
3. **The derivation.** Full algebra, step by step. Every non-obvious step gets its
   justification inline. Each substantive result is numbered `R<chapter>.<n>` and stated
   as a display equation. A reader must be able to reproduce every step with pen and
   paper; where the step is a numerical evaluation rather than algebra, say so, give the
   inputs and the value, and cite the test record that produces it.
4. **Results table** — result number, statement, exactness class (exact algebraic /
   machine precision / quantitative, per `docs/status/exactness-inventory.md`), residual
   where one exists, and the finding and test record it comes from.
5. **Comparison with measurement**, where the chapter predicts something measurable:
   model value, measured value with its source, deviation, and whether the comparison is
   a prediction or a calibration. Never present a calibration as a prediction.
6. **What was excluded, and why.** Inline, here, not deferred to the appendix: the routes
   this chapter's live result had to beat. For each — what was tried, what killed it
   (the argument, not just the verdict), and the finding number. This section is what
   stops a rebuilder from walking back down a road we already closed. If a no-go is what
   *forces* the live result, it belongs in the derivation itself, not in this section.
7. **What is still open.** Named residuals with sizes, and what would close them.
8. **Falsifiers.** What measurement would kill the chapter's claims, from the claim cards.

Rules for the writing:

- **Derive, don't assert.** "It can be shown that" is a defect. If the derivation is
  long, it is long; if a step is in a finding, reproduce the step, do not link to it.
- Every equation and every number carries its provenance: `[F317]`, `[CL042]`,
  `[test-results/F234_....json]`. A number with no provenance is a bug.
- Constants come from the registry with their **closed form**, never a truncated decimal
  (`2/9`, `1/√3`, `√(8π)·3^(1/4)`), with the float in parentheses if a float helps.
- Values that coincide are not the same constant. 2/9 is three unrelated constants
  (`delta_star`, `sin2_thetaW_onshell`, `c_fierz_colour`); f_π is three; 1/√3 is two.
  Merging any of them silently converts a prediction into an input — keep them distinct
  and say why they coincide where it matters.
- Markdown math (`$…$`, `$$…$$`) throughout. Escape literal `|` in tables as `\|` or use
  `\lvert k\rvert`.
- Define every symbol on first use and add it to `A5-symbols.md`. If a symbol is already
  in the glossary with a different meaning, rename yours and say so.
- Present tense, third person, no session narration ("we then tried…" belongs in a
  finding, not here). Exception: §6, where the history *is* the content.
- Length follows the physics. A chapter that needs forty pages of algebra gets them.
  Do not compress a derivation to hit a size; do not pad one that is genuinely short.

---

## 6. Sourcing discipline

Chapters are written **from the repository**, not from the model's general physics
knowledge. Standard textbook physics may be used for context, comparison, and to state
what the model must reproduce — clearly marked as external — but every step of *our*
derivation comes from a finding, a theory doc, a claim card, a constants entry or a test
result, and is cited.

When a derivation in the repo has a hole — a step asserted without proof, a number with
no closed form, a chain that does not actually connect — **do not fill it in**. Write
what is there, mark the hole inline as

```markdown
> **Gap [G-12]:** F146 asserts the bag constant follows from the string tension but the
> intermediate step is not shown in the finding or its test. Not reconstructible from
> the repository as of 2026-09-16.
```

and add the same entry to `GAPS.md` with the chapter, the finding, and what is missing.
A monograph that silently papers over a gap is worse than one that names it: the whole
point is that someone could rebuild this, and a fabricated bridge sends them into a
derivation that does not exist.

Cross-check as you go, without re-running physics: every number you print must match the
constants registry, the exactness inventory or a committed result JSON. Where a finding's
prose and a committed result disagree, print the committed result, and log the
disagreement in `GAPS.md`. Do not run `make gate` or long physics runs for this build; if
you believe a documented number is stale, say so in `GAPS.md` rather than re-deriving it.

---

## 7. Appendices

- **A1 — No-go ledger.** Every excluded route in the model, one row each: what was
  proposed, what excluded it, the argument in one or two sentences, the finding, and
  whether the exclusion is structural (cannot be reopened) or conditional (and if
  conditional, exactly what would reopen it — F339 is the pattern to follow).
- **A2 — Supersessions.** From `docs/theory/supersessions.yaml` plus what you found:
  what replaced what, when, why, and which chapter now carries the live version.
- **A3 — Constants.** Every registered constant: symbol, closed form, float, exactness
  class, provenance finding, derivation string, and whether it is derived, anchored,
  fitted or conventional. Total the free inputs at the bottom — **the count of genuinely
  free parameters in the model is one of the most important numbers in this document.**
- **A4 — Open residuals.** Everything not closed, with its size, where it bites, and
  what would close it. Sort by size of the residual.
- **A5 — Symbols.** Notation, units, index conventions, lattice conventions.

---

## 8. Final pass — the parent does this itself

After the last chapter:

1. **Dependency audit.** Every `R<n>.<m>` cited in a chapter is established in an earlier
   chapter, never a later one. Forward references are a defect; fix by reordering or by
   promoting the needed result earlier, and note the move in `00-plan.md`.
2. **Postulate audit.** Every postulate in Chapter 1 is used somewhere. Anything used but
   not stated becomes a new postulate — and a postulate discovered this late is itself a
   finding worth telling the user about (not writing: see the header).
3. **Free-parameter audit.** Reconcile every chapter's "free inputs consumed" list against
   `A3`. A parameter that appears in a chapter but not in A3, or vice versa, is a defect.
4. **Coverage audit.** Every finding from `findings-index.md` is accounted for. Print the
   final tally.
5. **Reconstruction test.** For three chapters chosen at random, hand a cold subagent the
   chapter plus its dependencies and ask a single question: *could you rebuild this result
   from this text alone, with no repository access?* Its answer, verbatim, goes in
   `README.md` under "Reconstruction check". If any answer is no, fix the chapter and
   re-run that check.
6. **README.md** — what this is, the build date, the tag legend, how to read it, the
   coverage tally, the free-parameter count, and the reconstruction check.
7. `make indexes`, then a one-paragraph entry in `docs/status/changelog.md` stamped
   `yyyy-mm-dd - hh:mm`.

Report to the user: chapters written, total size, findings covered, free parameters
counted, gaps logged, and the three biggest gaps by name.

---

## 9. Standing constraints

- Do not read whole large files into context: `changelog.md` is ~100k tokens, the
  findings directory is far larger. Index first, targeted reads second.
- Do not edit any finding, claim card, module, test record or registry. If the read
  turns up something that *should* change one, tell the user at the end; that is a
  separate research session with its own finding number.
