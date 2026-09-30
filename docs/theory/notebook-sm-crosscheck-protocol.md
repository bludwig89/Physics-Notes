# Notebook × Standard Model Cross-Check — Protocol

*Created 2026-09-22. The governing document for the third pass over M. Ludwig's 2007 notebook.
Companion files: `notebook-sm-crosscheck-ledger.md` (the tracker),
`notebook-sm-crosscheck-handoff.md` (questions this pass raises but does not answer),
`notebook-sm-crosscheck-ppAAA-BBB-*.md` (one write-up per run of consecutive sections). Runner:
the `/nb-sm-check` skill. Readiness tool: `tools/nb_sm_ledger.py`.*

---

## 1. What this pass is, and how it differs from the other two

The notebook now has three independent lenses. Keep them independent — that is the whole value.

| Pass | Question | Reference frame | Files |
|---|---|---|---|
| **Reconstruction** (cold) | Is the notebook's math right, as written and as corrected? | The notebook itself + standard textbooks | `notebook-reconstruction-*.md` |
| **Correlation** (operator-run) | How does each build relate to *our model*? | The repo: findings, claims, decisions | `notebook-reconstruction-correlation-queue.md` |
| **SM cross-check** (this one) | Given the corrected build, does it **reinforce**, **improve on**, or **conflict with** the Standard Model *as the field knows it today*? | Current external physics: PDG, experiment, 2020+ literature | `notebook-sm-crosscheck-*.md` |

The notebook was written in **2007** — before the Higgs discovery (2012), before θ₁₃ was measured
(2012), before the W-mass tension (CDF 2022) and its resolution by ATLAS/CMS (2024), before
KATRIN's sub-eV neutrino-mass bound, before GW170817 fixed c_grav = c. A large part of this pass's
value is the **hindsight column**: what the field learned after 2007 that bears on each idea.

**This pass does not grade the model, write findings, or open claims.** Anything it turns up that
the model should act on goes to the handoff file as a question or a paste-ready prompt. The D12
claims rule is not triggered by this pass, because nothing here is a claim *the project asserts* —
it is a record of how an external 2007 document sits against external 2026 physics.

---

## 2. Firewall rules

1. **Input is the reconstruction's corrected verdict, not the raw transcription.** Cross-check the
   build *as the reconstruction left it*: for `SOLID-WITH-CORRECTION` use the corrected form; for
   `INCORRECT` note the error and cross-check the intent only if the batch write-up states one.
   Read the notebook page (`references/physics-notes-complete.md`, the build's line range) for
   context only.
2. **Only disposed builds.** A build is ready when its ledger Status is anything except `PENDING`,
   `IN-PROGRESS` or `CONTAMINATED-DEFER-TO-SUBAGENT`. `NOT-TESTABLE` and `DEAD-END-*` builds **are**
   in scope — a speculation the notebook could not test (Higgs as a Cooper pair, the neutrino as the
   "missing monopole") is exactly where the modern field may have an answer. A section is ready
   when every build in it is ready. `tools/nb_sm_ledger.py` computes this.
3. **External lens only.** Verdicts rest on external sources. Do not read `findings/`,
   `docs/claims/`, `claims-index.md`, `findings-index.md`, `src/`, `docs/status/changelog.md` or
   the model-specific halves of `references/*-summary.md` to *form* a verdict. (Several reference
   summaries contain model content — the reconstruction's contamination log names
   `mohr-2010-maxwell-photon-wf-summary.md`. Go to the primary source instead.) If model context
   leaks in anyway, log it in the write-up's contamination section and say which verdicts it could
   have touched.
4. **Read-only on the reconstruction.** Never edit `notebook-reconstruction-*.md`, the index, or
   the correlation queue — they are being edited concurrently. If the cross-check finds a
   reconstruction verdict that looks wrong, record it under *Reconstruction queries* in the
   write-up and the handoff file; do not fix it.
5. **Re-check on change.** Each ledger row stores a hash of the reconstruction statuses it was
   checked against. If the reconstruction later revises a build (it has happened — see 02b), the tool
   flags the row `STALE` and it must be re-run.

---

## 3. Unit of work

- **Row** = one page-group section of `notebook-reconstruction-index.md` (the `## Pages …`
  headings). 50-odd rows. This is what the ledger tracks.
- **Run** = one or more *consecutive* sections, usually everything that shares a value in the
  ledger's `Batch` column (the reconstruction write-up(s) the builds were disposed in). A section
  whose builds span two batches (e.g. pp.62–72 = batches 06 + 07) is checked whole, in one run,
  reading both batch files. One run produces one write-up named by its page span:
  `notebook-sm-crosscheck-ppAAA-BBB-<slug>.md` (zero-padded, e.g. `pp057-072`). Batch 02b's
  corrections are always read together with batch 02.
- **Verdict granularity** = per build (NB-ID), rolled up per section.

---

## 4. Verdict vocabulary

Every build gets **two** tags plus a hindsight note.

### 4a. Relation to the Standard Model (the user's three words, plus one)

| Tag | Meaning | Minimum evidence |
|---|---|---|
| **REINFORCES** | The corrected build reproduces, re-derives, or is consistent with SM physics as currently measured. Includes a non-standard *route* to a standard *result*. | One A/B source stating the SM result |
| **IMPROVES** | Goes beyond the minimal SM in a direction that addresses a recognized SM gap (neutrino mass, hierarchy, parameter origin, gravity–spin coupling, …) **and** is not excluded by data. Must name the live research line it belongs to. | Two sources: one establishing the gap, one showing the line is live (2020+) and unexcluded |
| **CONFLICTS** | Contradicts an SM prediction that has been experimentally confirmed, contradicts a measured value, or violates a structural requirement the field treats as settled (gauge invariance, unitarity, anomaly cancellation, Lorentz invariance at tested precision). Sub-tag **-DATA** or **-THEORY**. | One A-grade source for -DATA; one A/B for -THEORY; state the number or theorem |
| **NEUTRAL** | Textbook background, reference inserts, math/chemistry asides, or content with no SM bearing. | None beyond saying why |

`IMPROVES` is the tag most prone to wishful grading. When in doubt between IMPROVES and NEUTRAL,
choose NEUTRAL and put the idea in the handoff file. An idea can be **both** IMPROVES in intent and
CONFLICTS in its specific 2007 form (e.g. adding ν_R is now required by data; the specific mass
term proposed may not be) — then tag the specific form, and state the intent separately.

### 4b. Status in the live field

| Tag | Meaning |
|---|---|
| **SETTLED** | Textbook-standard, not under active dispute. |
| **ACTIVE** | Live research line with 2020+ papers; not decided. |
| **CONTESTED** | Live, and current data or analyses disagree with each other (e.g. a tension ≥ 3σ). |
| **EXCLUDED** | Ruled out by data or by a theorem the field accepts. State by what, and when. |
| **DORMANT** | Was a research line; little or no work since ~2015, not excluded. |

### 4c. Hindsight note (one or two lines, required)

What did the field learn **after 2007** that bears on this build? "Nothing relevant" is a valid
answer and should be stated, not left blank.

### 4d. What would decide it (for ACTIVE / CONTESTED only)

Name the experiment or calculation and, if public, its timeline (HL-LHC, FCC-ee, DUNE, Hyper-K,
JUNO, LEGEND-1000, nEXO, KATRIN/Project 8, MOLLER, P2, CMB-S4, LISA, lattice QCD …).

---

## 5. Source rules

| Grade | Examples | Use |
|---|---|---|
| **A** | PDG Review of Particle Physics (cite the edition year), collaboration measurement papers (ATLAS, CMS, LHCb, CDF, KATRIN, Planck, LIGO/Virgo …), CODATA | Required for any CONFLICTS-DATA and for every quoted number |
| **B** | Peer-reviewed theory papers and reviews (PRL, PRD, JHEP, RMP, Phys. Rept., Living Reviews …) | Theory positions; IMPROVES/CONFLICTS-THEORY |
| **C** | arXiv preprints not yet published | Allowed for "the line is live"; never alone for a verdict |
| **D** | Textbooks, lecture notes, encyclopedias, press | Background only |

- **Look everything current up.** Every number and every "the field currently thinks" statement
  comes from a source fetched in the session, not recall. Quote the value with its uncertainty and
  the source year.
- **Cite as** `[Short title (Collab./Author, year)](URL)` with grade in brackets after: `[A]`.
- **Live** means 2020 or later. For ACTIVE/CONTESTED, at least one source must be 2023 or later.
- If a site is unreachable, say so; do not substitute a mirror or cached copy.
- Record the search queries used, in the write-up's appendix, so a later re-run can see what was
  and was not looked for.

---

## 6. Procedure for one run

**Step 0 — Readiness.** `python3 tools/nb_sm_ledger.py --status` → take the suggested next run
(or the section keys / page span passed to `/nb-sm-check`). Every section in the run must be
`READY` or `STALE`. If the ledger is
missing or out of date, `python3 tools/nb_sm_ledger.py --refresh` first. Stamp the time
(`date "+%Y-%m-%d - %H:%M"`).

**Step 1 — Extract.** Read the batch write-up(s) for the run. For every NB-ID in the run's sections, write the
**claim as the field would state it**: one sentence, in standard notation, corrected form, no
notebook-specific symbols. Note the reconstruction status you are checking against.

**Step 2 — Anchor.** For each claim, name the SM (or GR/QFT-foundations) anchor it touches: a
sector (EW, QCD, QED, Higgs, flavour, neutrino, gravity, cosmology, foundations), and the specific
prediction, parameter or structural requirement. Builds with no anchor go straight to NEUTRAL.

**Step 3 — Research.** Group the anchors (a batch usually has 2–6 distinct ones) and research each
once:
  (a) the current established status or value (PDG first);
  (b) live work since 2020 — theory lines, experimental tests, open tensions;
  (c) anything that directly addresses the notebook's specific idea (a named model, a no-go
      theorem, an exclusion).
Parallel research subagents are fine for (b)/(c) when there are more than three anchors; give each
the firewall rules in §2 verbatim.

**Step 4 — Verdict.** Assign §4 tags per build, with the hindsight note and, where applicable,
"what would decide it". Roll up per section: the section tag is the most consequential build tag
(CONFLICTS > IMPROVES > REINFORCES > NEUTRAL), plus a one-line section summary.

**Step 5 — Handoff.** Anything that should reach the model — a CONFLICTS the model might inherit,
an IMPROVES line the model might already be on, a number the model should compare against — goes
into `notebook-sm-crosscheck-handoff.md` as a question (never answered here) or a paste-ready
research prompt. Reconstruction verdicts that look wrong go there too, under *Reconstruction
queries*.

**Step 6 — Cold check.** Hand every CONFLICTS and IMPROVES verdict, with its cited sources, to a
fresh subagent that has not seen the write-up's reasoning. Its only job: for each citation, does
the source actually say what the verdict says it says, and is the number quoted correctly? Fix or
downgrade anything it fails. Record the check in the write-up header
(`**Cold-checked:** yyyy-mm-dd, n verdicts, k changed`).

**Step 7 — Record.** Write the run's write-up (template §7), then record each section with
`python3 tools/nb_sm_ledger.py --set <key> --relation <tag> --field <tag> --writeup <file>`,
which also stamps the status hash that later `STALE` detection compares against. Never
hand-edit `Readiness` or `Checked-against`. Run `make indexes` so the new doc is
listed. Do not write changelog entries while the reconstruction is still running (§2.3).

---

## 7. Write-up template

```markdown
# Notebook × SM Cross-Check — pp. a–b: <title>

*yyyy-mm-dd - HH:MM · checks `notebook-reconstruction-NN-<slug>.md` (+ any other batch files) · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** yyyy-mm-dd, n verdicts, k changed

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|

## What the field learned since 2007 that matters for this batch
(3–6 bullets, each with a source)

## Per-build verdicts
### NB-xxx (p.N) — <short title>
- **Checked against:** reconstruction status `…`
- **Claim (field terms):** …
- **Anchor:** sector — specific prediction/parameter
- **Current status:** … [source][A]
- **Live work:** … [source][B/C]
- **Verdict:** REINFORCES | IMPROVES | CONFLICTS-DATA | CONFLICTS-THEORY | NEUTRAL · SETTLED | ACTIVE | CONTESTED | EXCLUDED | DORMANT
- **Hindsight:** …
- **What would decide it:** … (ACTIVE/CONTESTED only)

## Reconstruction queries
## Handoff items raised (mirrored into the handoff file)
## Contamination log
## Appendix — search queries used
## Sources
```

---

## 8. Finishing the whole notebook

When every ledger row is checked, write `notebook-sm-crosscheck-synthesis.md`: the tally by tag,
the notebook's ideas that the field has since vindicated, the ones it has excluded, the ones still
live, and a ranked list of the handoff items. That document — not the per-batch write-ups — is
the one to hand a physicist.
