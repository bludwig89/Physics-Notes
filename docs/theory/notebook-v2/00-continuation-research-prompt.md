# Notebook v2 — Continuation Research Prompt

*2026-09-23 - 12:45 · paste-ready governing prompt for the fourth pass over M. Ludwig's 2007
notebook. Written for a session attached to this repo (Claude Code / Cowork with the Physics Notes
folder, plus web search). Paste everything below the line into a fresh session.*

---

# Notebook v2 — continue the lines of thinking

## 1. Mission

M. Ludwig's 2007 notebook (`references/physics-notes-complete.md`, pp.1–182) has now been through
three deliberately independent passes, and on 2026-09-22 it was declared **fully mined as a source**
(`docs/theory/notebook-followup-2026-09-22.md` Part V): every page is implemented, cited, or closed.

Your job is **not** to mine it again. Your job is to **continue it** — to take each line of thinking
the notebook opened, follow where the reconstruction, the correlation pass, the SM cross-check and
the model now leave it, and push it **one real step further**, the way the author would continue it
in 2026 with the CA model and the field's current physics in hand. The output is **Notebook v2**: a
living research notebook of continuation entries under `docs/theory/notebook-v2/`, plus whatever
findings, test records and claim cards the real steps produce.

A good v2 entry does one of three things: (a) turns a notebook intuition into a derived or measured
result in the model, (b) closes it as a clean negative with the reason, or (c) exposes a correlation
between threads — two questions that are one question in disguise — and says what that joint
question is. It must also leave behind the **new questions** it opened. That last part is what makes
this a notebook and not an audit.

## 2. The lenses, and your relationship to them

| Pass | Question | Files | Your access |
|---|---|---|---|
| Reconstruction (cold) | Is the 2007 math right, as written and corrected? | `docs/theory/notebook-reconstruction-*.md`, `-index.md` (NB-001…NB-186) | read-only |
| Correlation (operator) | How does each build relate to the model? | `notebook-reconstruction-correlation-queue.md`, `notebook-correlation-pass-*.md` | read; append addenda |
| SM cross-check | Does the corrected build reinforce / improve / conflict with 2026 physics? | `notebook-sm-crosscheck-*.md` (synthesis, handoff, ledger, 15 write-ups) | read; append-only on handoff |
| Follow-up | p.77 charge partition, pp.176–182 factorization | `notebook-followup-2026-09-22.md`, F396, F397 | read |
| **v2 (you)** | **Where does each line of thinking go next?** | `docs/theory/notebook-v2/` | **write** |

The firewall that governed the first three passes is **lifted for you** — you are the integrating
pass, so you read all of them *and* the model. The price of that access is attribution discipline:
in every v2 entry, tag each load-bearing statement with where it comes from —
`[NB p.N]` notebook, `[RECON NB-xxx]`, `[XCHECK pp.a–b]`, `[CORR]`, `[MODEL F#/CL#/decision n]`,
`[FIELD <citation>]`, `[V2]` your own new work. A reader must be able to tell a 2007 intuition from
a 2026 derivation from a literature fact at a glance.

**Never edit** reconstruction files, the reconstruction index, the SM cross-check write-ups/ledger,
or any existing finding. The handoff file and correlation queue are append-only: mark an item
`CLOSED → <path>` with a date-time, never delete or rewrite. A correlation-pass file you think is
wrong gets a dated `## Addendum` at the bottom, not an edit to its body.

## 3. Phase 0 — orient and claim (no physics yet)

1. Read, in this order: `CLAUDE.md`; `INDEX.md`; `findings-index.md`; `claims-index.md`;
   `tail -n 150 docs/status/changelog.md`; `docs/theory/key-decisions.md`;
   `notebook-sm-crosscheck-synthesis.md`; `notebook-sm-crosscheck-handoff.md`;
   `notebook-reconstruction-correlation-queue.md`; both `notebook-correlation-pass-2026-09-23*.md`;
   `notebook-followup-2026-09-22.md` (Parts V and VI in full, skim the rest);
   `docs/status/completeness-2026-09-08.md` and its `-prompts.md` companion (so you know which
   notebook threads already have a completeness row and a prompt). Read reconstruction batch
   write-ups and the notebook itself **targeted**, per thread, not wholesale.
2. `grep -n notebook docs/design/session-claims.yaml` — if another session has an open claim on a
   notebook topic, do not duplicate it. Then open your own claim (no numbers): sector `notebook-v2`
   or the sector of your first thread, topic "Notebook v2 continuation pass".
3. Run `make gate` and record the result. If it is red, confirm it is red *the same way* the latest
   completeness report says before assuming you broke anything.
4. Take finding numbers only at write time, one at a time, from `casim index` **NEXT FREE NUMBER**.

## 4. Phase 1 — the thread map (no new physics)

Write `docs/theory/notebook-v2/01-thread-map.md`.

A **thread** is a line of reasoning, spanning one or more NB-IDs, that the notebook left open,
extendable, or self-doubted. Harvest threads from all of these, not just the first:

- every open row of the correlation queue and every open item in handoff §A/§B;
- synthesis §2 (vindicated), §4 (open), §5 (ranked handoff);
- follow-up Part V "Recorded as structure, not yet used" and "Still open", and Part VI.3;
- ledger rows with status `NEEDS-WORK`, `DEAD-END-AUTHOR-CALLED-IT`, or `NOT-TESTABLE` — a
  speculation that could not be tested in 2007 may be testable in CASIM now;
- the author's own self-doubt markers ("not good!", "is there any significance to this?", ✗) —
  F396/NB-037 show that the author's doubt was sometimes premature.

For each thread, one row: ID (`T01`…), NB-IDs, one-line statement of the line of thinking, verdict
in each lens, **what the model already has** (findings/claims/modules — search `findings-index.md`,
`claims-index.md`, `code-index.md` and `grep -ril` over `findings/` and `docs/claims/` before
writing "absent", and record the search terms you used), what the field has, the natural next step,
and cost class (`in-repo minutes` / `in-repo hours` / `long run → script for Ben` / `decision`).

Then write the **correlation section**: clusters where several threads are the same question.
Name the joint question for each cluster in one sentence. Seed clusters to verify, split, or
reject — do not assume they are right:

- **Pairing, 0 ⊕ 1.** NB-007/008/009 ↔ F69 (spin-1 photon pair), F73 (spin-0 singlet of the same
  pairing = "Cooper-pair Higgs"), F74, F77, F80, F352, F199b, F210–F213 (superconductivity).
- **Mass as internal structure.** NB-012/013 (field-energy mass), NB-093–095 (helical motion at c)
  ↔ decision 2 (c as a rotation rate, F25/F26), F46 (Ω_rest = arcsin m), F122/F123/F140 (baryon).
- **Null / spinor geometry.** NB-143–186 ↔ F397 (T1 map), F37/CL044 (Riemann–Silberstein ↔ BCC
  chirality), celestial holography (B.3 pass).
- **Electroweak numerology → structure.** NB-130–134 ↔ F49/F141/F138/F320 and the three registered
  2/9 constants.
- **Discrete geometry and dimension.** NB-005/006/043/044 ↔ decision D1 (BCC), F354, completeness
  row A1, causal sets / Wolfram / 't Hooft–Elze (handoff B.2).
- **Gravity with spin.** NB-015–038 (Sachs, ECSK torsion) ↔ decision 4, F63, F178, F345.

## 5. Seed leads — verified 2026-09-23 while writing this prompt

These were checked against the tree when this prompt was written. Re-verify each before building on
it; the tree moves.

1. **Correlation pass A.1 appears to contradict F73.** A.1 (2026-09-23) concludes the model
   "bypassed NB-009 altogether" and never attempted "the same pair, two applications." But
   `findings/F73-spin0-bound-pair-scalar.md` (2026-06-01) cites notebook pp.5–6 ("the Higgs is the
   Cooper pair, we presume") and builds the **spin-0 singlet of the same pairing whose spin-1
   combination is the F69 photon** — which is NB-009's unification. F73's own status: kinematics
   exact, mass **not** predicted, m_H ≈ v/2 **flagged, not derived**; F352 (BHL compositeness)
   is a quantified negative. Adjudicate this and append an addendum to the A.1 file. It feeds
   directly into the open **handoff A.2** (the 125 GeV scalar with mass-proportional couplings,
   *Nature* 607, 52–59, 2022): F73 states that as built the model has no Higgs-matching particle and
   calls that a standing obligation. A continuation that does not need the mass: does the F73
   channel's coupling to each fermion scale with that fermion's mass (the κ-framework signature)?
2. **The notebook's sin²θ_W = 2/9 is a registered model constant.** NB-133's hypothesis (W±
   coupling = 3e, which the reconstruction reduces to √2/sin θ_W = 3) gives sin²θ_W = 2/9 exactly.
   `casim.constants.sin2_thetaW_onshell` is `Fraction(2, 9)`, exact, derived from the on-shell
   m_W²:m_Z² = 7:9 BCC facet-axis count (F49/F141/F138/F320; PDG on-shell 0.22305). The correlation
   queue asked about δ* = 2/9 instead — a *different* registered 2/9 that the registry forbids
   merging. So the queue row is answered more strongly than it asked. Continue: is the notebook's
   "coupling = 3e" route an independent derivation of the same number or a restatement of it, and
   does NB-134's self-flagged failed check (11/6 + 6/11 = 157/66 ≠ 7/3) have a corrected form that
   closes once the model's 7:9 is in hand? **Do not** count 2/9 as a new prediction — the model
   already has it; v2's contribution is lineage and the corrected check.
3. **Pryce 1938 has never been engaged.** `grep -ril pryce findings docs/claims` returns nothing.
   The queue's NB-007 row asks whether the paired-spinor photon (F67–F69, decision 5) addresses the
   impossibility of exact Bose commutation for a two-fermion composite. Concrete step: build the
   composite photon operator on F69's construction with the second-quantized machinery
   (F212/F217/`second_quant`) and measure the deviation of [a, a†] from 1 as a function of
   occupation and lattice volume. A scaling law here is a finding.
4. **Torsion has a magnitude estimate but no claim-level stance.** NB-037's resolution is ECSK
   torsion sourced by spin; decision 4 is torsion-free; F63 estimates spin-torsion at ≲0.3% at F62
   densities, O(1) only above ~3 quanta per cell. The XCHECK pp.15–29 write-up names a 2023/24
   tabletop-test proposal. Compute the model's number for that experiment's observable, and decide
   whether "torsion-free" is an assertion that needs a D12 claim card with a falsifier.
5. **"Mass from field energy" has a quantitative test available.** XCHECK pp.9–11 vindicates the
   intuition for hadrons via the lattice-QCD nucleon mass decomposition (~9% from quark masses).
   The model has a dynamical baryon (F122) and an SI-scale nucleon ≈ 928 MeV (F123). Decompose the
   model's own nucleon mass into constituent-mass vs. field/binding terms and compare with the
   published lattice decomposition (quark condensate, gluon energy, trace anomaly).
6. **Follow-up Part V leftovers**, each a candidate thread: BCC Weyl block point group is exactly
   D₂; conjugate-rep spin sign S_z = −σ_z/2; threshold spin content sits |ε| above the floor;
   S² = SU(2)/U(1) leg coset ↔ weak-isospin coset (recorded as an **untested analogy** — do not
   rediscover it as new); g_c = 2.2596 is still the one external input in the photon channel; F41's
   kinetic-sector problem, bounded by F143; and Part VI.3's finite-k grid threshold artifact, which
   the follow-up says needs **its own finding** because fixing it changes g_c at finite k.
7. **Quick closes, probably.** NB-128/129 Riemann–Silberstein ↔ F37/F39/F65/CL044; handoff B.1
   (triviality) ↔ F319/F340/F352, where the sextic E_g coupling is non-renormalizable in 4D and the
   cutoff is physical per F319, so the Aizenman–Duminil-Copin theorem is likely out of scope — say
   so precisely, with the scope conditions, or show it is not.

## 6. Phase 2 — triage

Rank the threads and clusters in the thread map, using these criteria in order:

1. does it bear on a stated key decision (1–7, D1–D12) or on a live claim card?
2. can it be driven to algebraic exactness, machine precision, or a falsifiable number, in-repo?
3. does it resolve an inconsistency between passes (seed lead 1 is one)?
4. cost.

Post the ranked top ten to the user with `SendUserMessage` (one line each: thread, next step, cost).
If the user is present, let them reorder; if not, proceed in your order and say so at the top of the
thread map.

## 7. Phase 3 — continue threads, one at a time

For each thread, in ranked order, write `docs/theory/notebook-v2/NB2-{NNN}-{slug}.md`. Finish one
cleanly before starting the next. Template:

```markdown
# NB2-NNN — <the line of thinking, as a question>

**Date:** yyyy-mm-dd - hh:mm · **Thread:** Txx · **Cluster:** <name>
**Lineage:** NB-xxx [RECON verdict] · XCHECK <relation/status> · CORR <row/pass> · MODEL <F#/CL#>
**Disposition:** FINDING F{N} | CLOSED-NEGATIVE | CLOSED-LINEAGE | OPEN-HANDOFF | LONG-RUN-SCRIPT

## Where the notebook left it          (quote the page; the author's own words)
## Where the three passes left it      (one paragraph per lens, tagged)
## What the model already has          (with the search terms used)
## What the field has now              (primary sources, dated)
## The next step, taken                (derivation first; then CASIM; numbers with exactness class)
## Result                              (what moved; residuals; what did not move and why)
## Correlations exposed                (other threads this touches; the joint question if any)
## New questions opened                (the notebook continues here)
## Files touched
```

Working rules:

- **Algebra before physics, then CASIM.** Attempt a closed-form derivation before adding anything
  to the engine. Exactness preference: algebraic, then machine precision, then quantitative.
- **A real physics result becomes a finding.** New quantitative result → `/finding` (which chains
  the attack-and-fix review), a test **registry record** with `findings:` set by hand, and a claim
  card if it extends, derives or contradicts QM/SM/GR/SR (D12). Lineage-only or descriptive work
  stays a v2 entry with no finding number, as the A.1 and B.3 passes did.
- **Long runs go to Ben.** If a step exceeds the sandbox limit, write the script or `casim`
  parameters that emit a JSON, mark the entry `LONG-RUN-SCRIPT`, and move on.
- **Close the loop.** When a thread answers a handoff or queue item, append `CLOSED → <path>` there.
- Follow the repo's module, constants, numerics and test-registry rules in CLAUDE.md, and check
  `casim.numerics.chiral` before trusting numpy on chiral transforms.

## 8. Honesty rules

- **Negative results are the normal result.** F396 and F397 both came back mostly negative, and
  that was their value. Record a negative in full: what was tried, where it failed, what it rules
  out.
- **A resemblance is not a derivation.** A matching number counts as a prediction only if it was
  derived before being compared. Never merge coincident constants (the registry has three 2/9s,
  three f_π, two 1/√3 on purpose). Never upgrade "flagged, not derived" to "derived".
- **Two spot checks are not a scan** (follow-up VI.3). Sweep before asserting a trend.
- **Read before claiming absence.** Every "the model has nothing on X" states the search that
  found nothing.
- **Correct the record where it is wrong**, including earlier passes and this prompt — by addendum,
  with the evidence.

## 9. Phase 4 — synthesis

Write `docs/theory/notebook-v2/index.md`:

1. a ledger of every NB2 entry with its disposition and any F/CL numbers;
2. **"What the 2007 lines of thinking have become"**: a short narrative per cluster;
3. the updated correlation map, including clusters you found that were not seeded;
4. **open questions v2 has raised**, the new notebook frontier;
5. paste-ready prompts for the next session, one per open thread, in the house style of
   `docs/status/completeness-2026-09-08-prompts.md` (self-contained; names the target, what exists,
   what is closed, what to run first).

## 10. Close the session

`make indexes` → confirm every finding you touched has a `**Checked:**` line → `make coverage` →
`make gate` → one-paragraph `docs/status/changelog.md` entry → release your session claim with a
`release_note:`. Every new file entry carries a `yyyy-mm-dd - hh:mm` stamp.

## 11. Scope and budget

Complete Phases 0–2 in full; they are cheap and they are what the next session inherits. Then take
as many Phase 3 threads as you can finish **cleanly**. Three finished entries are worth more than
ten half-started ones. Always write Phase 4, even if only a few threads were continued, so the map
and the prompts survive the session.
