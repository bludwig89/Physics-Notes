# Consolidation and deprecation plan — the claims layer, and what moves

**Date:** 2026-08-04 - 22:40
**Session:** `careful-tidy-noether` (claim board: `docs/design/session-claims.yaml`)
**Scope:** documentation architecture. **No physics was read, changed or judged.** No finding, test record, physics module, exactness row or ledger record was edited.
**Companion:** `docs/status/findings-supersession-triage-2026-08-04.md` — the header pass over all 282 active findings. This plan does not repeat its analysis; it acts on its §8 recommendation.

---

## 1. The question, and the answer this plan gives

> *The project, while having a large number of indexes and findings, feels bloated and scattered. How do we move anything dead, overstated, or false to `deprecated/` and tighten up, both now and going forward?*

The instinct behind the question is right and the proposed remedy is wrong, and the reason is already recorded twice in this repo.

- `deprecated/README.md` records it from P0.4: **of 14 test files an audit called superseded, exactly one was.** Eleven were a dead verdict wrapped around live, load-bearing algebra.
- `findings-supersession-triage-2026-08-04.md` records it again, at corpus scale, from the other direction: **zero of 282 findings qualify for retirement**, and a keyword sweep for obsolescence language flags 67 of them — *nearly all false positives of a specific kind*. The project's most valuable results are **negative results**, and a negative result describes itself in the exact vocabulary of obsolescence. "A four-avenue no-go", "$d=6$ and $d=9$ excluded", "the model admits **no** slow-roll inflaton". Any sweep looking for dead material surfaces the falsification record first and most confidently.

So the material is not the problem. **The missing object is.**

A **finding** is a research record: what a session did and what came out. It is written once and is thereafter historical — findings do not get rewritten when the model moves, and that is correct. But the project also makes **assertions**, in the present tense, and had nowhere to keep them. The symptom was `papers/Claims-and-Falsifiers-Summary.md`: a prose document whose revision 2 withdrew a core claim and four falsifiers in a blockquote, and whose revision 3 said *revision 2 was wrong about charge quantisation* in a second blockquote. Both corrections were right. **Neither was checkable, discoverable from the finding, or countable**, because a claim with no record of its own can only be corrected by editing the paragraph that states it.

That is what "bloated and scattered" actually describes: not too many findings, but **no way to ask what the project currently asserts** without reading 282 of them and a prose summary that may disagree with any of them.

**This plan therefore does not move findings. It adds the claims layer (D12), and moves only completed process documents.**

---

## 2. What was built

`docs/claims/` — one card per claim, `CL{NNN}-{slug}.md`. See `docs/claims/README.md` for the contract in full. In brief:

| Object | Question it answers |
|---|---|
| `findings/F{N}-*.md` | What did we do, and what came out? |
| `docs/claims/CL{N}-*.md` | **What do we assert, right now, and what would kill it?** |
| `docs/theory/supersessions.yaml` | What replaced what, and what survived? |
| `deprecated/` | What is out of the tree, and by what rule? |

**251 cards**, partitioning the corpus:

| Set | Count | Provenance |
|---|---|---|
| Authored from `Claims-and-Falsifiers-Summary.md` rev. 3 | 27 | `CL001`–`CL027`, `review_state: authored` |
| Authored, post-dating the summary | 1 | `CL028` (lepton shape angle, founding decision 7) |
| Seeded from a finding, **unreviewed** | 223 | `CL029`–`CL251`, `review_state: unreviewed-seed` |
| **NO CARD** — recorded decision, §5 | 8 | — |

The 27 authored cards carry all 10 core claims, all 5 live falsifiable predictions, all 6 scope non-claims, the $\alpha_s$ open tension, and **all 5 withdrawn claims** — the horizon-free black hole and its four dependent falsifiers, which revision 2 retracted in a blockquote and which now each have a card whose `## Status & history` *is* the retraction record.

### 2.1 The rule that does real work

`tools/check_claims.py` **fails a card that is `status: live` when every finding it rests on is named in a `superseded:` list in the ledger.** That is the machine-checkable form of "overstated", and it is the check revisions 2 and 3 would have tripped months before a human noticed.

It fired immediately, on seven seeds — **F50, F52, F55, F62** (replaced by F64's EM-connection route), **F230** (by F253/F255), **F251, F258** (by the F272/F277 refold repair). Every one of those findings' own status lines still reads `Confirmed — N/N tests PASS`, which the triage pass measured and is exactly what it predicted: *"not one header says superseded."* Both objects are correct simultaneously — the finding records what it concluded, the claim resting on it has to move — and the split between them is the whole point of the layer. The seeder now reads the ledger, and those seven are `open` with the reason quoted on the card.

It deliberately does **not** fire on a *partial* supersession, for the P0.4 reason: a check that flagged partials would train people to ignore it.

### 2.2 Declared debt, ratcheted

| Ratchet | Count | Meaning |
|---|---|---|
| `review_state: unreviewed-seed` | 223 | The finding is the evidence; **no reviewer has confirmed the classification.** |
| `falsifier: unset` | 226 | No falsifier stated. Not a claim that none exists — that is `falsifier: none`, which requires the structural reason to be **named**. |
| `exactness: unset` | 63 | The finding's own status line did not state an exactness class in words the extractor could read. |

These may fall, never rise; `check_claims.py --ratchet-update` only ever lowers a ceiling. **223 unreviewed seeds is not a claim of 223 results.** It is a countable, gate-enforced queue where there was previously an uncounted one, and `/review-finding` → `/remediate-finding` → the card's status is the intended way to drain it.

---

## 3. Executed in this session

Only moves with **no** physics content and **no** inbound reference outside a generated index. Everything else is queued in §4 for a session that owns the relevant file.

| Move | Count | Rule |
|---|---|---|
| `docs/status/*-completion-overview.md`, `C9-readiness.md` → `docs/status/completions/` | 12 | A completed engineering phase is history, not status. `docs/status/` held 22 files of which 12 were finished-phase records; it now holds the 10 that are actually current. **Not `deprecated/`** — these are complete, not superseded, and the distinction is the one `deprecated/README.md` insists on. |
| Landed one-off prompts → `docs/roadmaps/completed/` | 12 | A next-session prompt whose finding exists is a finished work order. Each is listed in §3.1 with the finding that closed it. `docs/roadmaps/` held 24 files, of which half were spent. |
| `outreach-posts-draft.md` (repo root) → `papers/` | 1 | Root clutter; it belongs beside `papers/Outreach-Emails.md`. |

`src/casim/index/docs.py` gained the two new groups so both directories stay in `docs-index.md` — a moved document that leaves the index is a document someone rewrites.

### 3.1 The prompts moved, and what closed each

| Prompt | Closed by |
|---|---|
| `next-session-bgfield-loop.md` | F162, F287 |
| `next-session-prompt-vacuum-energy.md` | F164, F193, F196 |
| `next-session-residual-A-solve.md` | F154, F155 |
| `next-session-stable-atomic-structure.md` | F195, F206 |
| `p5-gui-workbench-handback.md` | F275 |
| `qc-routes-3-4-prompt.md` | F226, F227 |
| `F216-followon-spin2-mass-abundance-prompt.md` | F223, F228, F238 |
| `F223-followup-geon-production-brief.md` | F228 |
| `prompt-superconductivity-construction-2026-06-30.md` | F210–F215, F218b |
| `angular-self-duality-solve-2026-06-30.md` | F199, F200 |
| `mass-magnitude-derivation-2026-06-29.md` | F119, F233 |
| `gravity-sector-scenarios-2026-06-30.md` | F181–F190 |

**Deliberately not moved:** `prompt-weinberg-8over7-closure.md` — CL007 names the 8/7 closure as a live open item, so the prompt is live. `open-derivations-prompts{,-v2}.md`, `loop-sector-buildout-prompt.md`, `next-steps{,-pt2}.md`, and every `roadmap-*.md` are current.

---

## 4. Queued, NOT executed — each needs a session that owns the file

Listed with what blocks it. Nothing here is a judgement that the item is dead.

> **Q1 and Q3 were executed later the same day**, on Ben's authorisation — see
> §7. They are left in the table below in their original wording rather than
> deleted, because a queue that erases its own entries cannot be audited: the
> reason an item was *deferred* is evidence about how the project works, and it
> is not recoverable from the fact that it eventually got done.

| # | Item | Why it is queued rather than done |
|---|---|---|
| Q1 | **Finding-level supersession banners.** `apply_supersession_banners.py` builds its worklist from `record["tests"]` and stamps Python docstrings; it never reads `record["findings"]` and returns `no-docstring` for markdown. `test_no_orphan_banners` walks `tests/` and `src/` only. So all 8 banners on active findings are hand-written and unverified, and 4 of them (F20, F22, F64, F176b) have **no ledger record at all** — the exact orphan the test exists to catch, in the one directory it does not walk. | Touches `docs/theory/supersessions.yaml`, on which claim `gracious-jolly-meitner` has an **escalated, unexecuted** edit. Triage §5 is the full fix in three steps. |
| Q2 | **A fourth ledger status term.** S13 (F165) and S15 (F230) both say `RETAINED: EVERYTHING`. Neither `fully_superseded` nor `partially_superseded` is honest; what died is a sub-claim. Triage §5.2 proposes `sub_claim_superseded`. | Same file, same escalation. |
| Q3 | **`Claims-and-Falsifiers-Summary.md` revision 4.** It predates founding decision 7 and carries no lepton-shape-angle claim; **CL028** is authored here to fill that gap and is the only card with no counterpart in the summary. The summary should also gain a pointer to `docs/claims/`. | A public document. Ben's call on wording. |
| Q4 | **Three authored cards carry `falsifier: unset`** — CL003 (mass without a Higgs field), CL006 (confinement, 3+1D half), CL010 (charge quantisation). In each case the summary states no threshold and this session **declined to invent one**. CL010's is arguably `none` with a structural reason (an algebraic uniqueness statement over ℚ is falsified by exhibiting a second solution, not by a measurement) — but the structure has not been argued in the finding, so it stays `unset`. | Physics judgement. Not a documentation decision. |
| Q5 | **F32** — the only finding in the corpus with zero citations from other findings *and* zero references from `src/`, `tests/`, `scenarios/`. An **orphan** signal, not an obsolescence signal. | Triage §7: the single file where `/review-finding` would tell us something a header cannot. |
| Q6 | **Draining the 223 unreviewed seeds.** Each promotion is one `/review-finding` pass plus naming the test records and artifacts. | Research work, by sector, over many sessions. The ratchet makes it countable. |
| Q7 | **`docs/design/` prose vs. registry.** 20 files mixing live registries (`session-claims.yaml`, `module-graph.json`, `finding-numbers.yaml`) with spent build briefs (`casimir-effect-build-brief.md` → F207/F209; `alcubierre-warp-structural-test.md` → F204; `qstar-gluon-d1-computation-plan.md`; `warp-shift-vector-construction.md`). | Several are cited by findings as provenance. Needs a per-file reference check, not a sweep. |
| Q8 | **`deprecated/` top level.** 20 loose superseded plans with no dated entry in `deprecated/README.md` — the level's own acceptance rule ("a dated entry below saying why") is the one rule in that directory `make gate` does **not** enforce, because `check_deprecated.py` covers `code/` and `tests/` only. | Extend `check_deprecated.py`, then backfill entries. Cheap, and it closes the last unenforced corner of the destination. |

---

## 5. NO CARD — findings that do not clear the bar, with reasons

`docs/claims/README.md`: *the bar is **extends established physics**, not **is interesting** — an engine-wiring result, a numerical technique, a refactor, or a status record does not get a card.* Recorded here so that "no card" is a decision rather than an omission.

| Finding | Reason |
|---|---|
| F01 | A scratch list of possible findings. There is no assertion to card. |
| F133 | Engine wiring — makes the block-spin RG a first-class CASIM operation. The physics claim is F130's (CL107); this is its implementation. |
| F134b | Numerics — a hand-rolled chiral core and the measured FFT floor. Backend correctness; no physics extended. |
| F160 | Engine wiring — runs the F159 two-grid atom as one engine run. The physics claim is F159's. |
| F268 | Engine defect and repair: the scheduler had no clock, and 18 of 46 scenarios were desynchronised. |
| F269 | Engine defect and repair: channel ordering was a line number. |
| F274 | Tooling — scenario language v2, fail-at-load validation. |
| F275 | Tooling — the GUI workbench and headless run diffing. |

**Judgement calls that went the other way**, recorded because they are the near misses: F270 (one energy convention + a global conservation gate) **got a card** — energy conservation is physics even when the occasion was an engineering cleanup. F272 and F277 (the refold defect) **got cards** — the defect flipped a sign in vacuum polarisation, so the correction is a physics result. F276 (the variable-$c$ Weyl stepper had global order zero) **got a card** — it is a numerical-order claim about a curved-space integrator that carries a gate record. F221 (Kraus channels + stabilizer codes) **got a card** — it asserts the substrate hosts fault-tolerant QEC, which is a claim about the substrate.

---

## 6. Going forward — the standing rule

Added to `CLAUDE.md` as **decision D12**:

> **Any algebraic or physics-tested claim or element that extends, derives, or contradicts anything in quantum mechanics, the Standard Model, general relativity, or special relativity gets a card in `docs/claims/` and a row in the registries it touches.**

Three properties make this hold rather than decay:

1. **The card is the record; `registry.yaml` is a projection.** Generation runs *backwards* from every other registry in this repo, and deliberately: a module cannot carry its own metadata, but a claim's prose and its metadata are the same object. Splitting them would produce exactly one thing — a card whose status line disagrees with its registry row.
2. **`make gate` fails on a stale index, an unknown vocabulary value, a broken reference, a raised debt ceiling, or a live claim standing on wholly superseded ground.** None of those is a convention.
3. **A card never edits a finding.** Writing or narrowing a claim touches no finding, module, test record, exactness row or ledger entry. The inverse also holds and is the point: *a finding may be superseded without any claim changing, and a claim may be narrowed without any finding changing.* Neither event is visible in the other object, and until now the project had no place to notice the difference.

The consolidation this asks for going forward is therefore **not** a periodic sweep of `findings/`. Sweeps of this corpus have now been attempted twice and were wrong 13 times out of 14 and 0 times out of 282. It is: *when the position changes, change the card* — and let the gate say so when someone doesn't.

---

## 7. Executed after authorisation — Q1 and Q3 (2026-08-04 - 23:55)

Ben authorised Q1 and Q3 the same day. Both are done; the queue rows above stand as written.

### Q1 — the finding-level banner mechanism

The diagnosis held. `apply_supersession_banners.py` built its worklist from `record["tests"]` and stamped a *Python module docstring*, so it returned `no-docstring` for every markdown file and never read `record["findings"]`. `findings/` is where a **reader** meets a superseded result, and it was the one directory with no enforcement at all.

| Fix | What landed |
|---|---|
| **Markdown path** | `build_md_banner()` + `apply_to_markdown()` — a blockquote carrying the same DEAD / STILL LIVE / REPLACED BY / NOTE fields, stamped **immediately after the H1** (never before: `casim index` scrapes the H1 for `findings-index.md`, and a banner above it would rewrite every index row). Idempotent, `--check`-honouring. |
| **Enforcement widened** | `test_no_orphan_banners` now walks `findings/` and `deprecated/findings/`; a new parametrised `test_classified_finding_carries_its_banner` is the markdown twin of the docstring check. |
| **Ledger populated** | `findings:` blocks on **S3, S4, S6, S10, S11, S12, S13, S15, S18** — 25 per-file entries, every `dead:`/`live:` string taken from that record's own `retained:`/`scope:` clause or from the review it cites. **No new physics judgement was made.** |
| **New status: `sub_claim_superseded`** | Exactly what triage §5.2 asked for. S13 (F165) and S15 (F230) both say `RETAINED: EVERYTHING`; marking either `partially_superseded` would tell a reader the result is in doubt when the ledger says the opposite. |
| **New kind: `retracted_by_review`** | The ledger had no way to say *a claim was withdrawn by an independent review rather than replaced by a successor finding*. F22 is the case that proves it: attack 1 is simply false and attack 3 shows the headline was a misnomer — nothing took their place, so `superseded:` is legitimately empty and the per-file entry carries the split. |
| **Orphans reconciled** | All four. **F64** and **F176b** → S4. **F20** → S18, which executes the escalation `gracious-jolly-meitner` left open; F20 is **not** added to any top-level `superseded:` list, because items 1 and 2 are live and were *promoted* to machine precision by their own remediation, so a wholesale marking would be false. **F22** → new record **S19**. Seven hand-written tombstones were removed and replaced by generated ones; adoption and renumbering notes were left alone. |
| **S14 fixed** | `by: [P5.1]` names a roadmap phase, and the schema test required `D\d+` for `methodology` records — red since 2026-08-03, captured as an already-red baseline by the triage. The test now accepts a phase id rather than the record inventing a decision that was never taken. |

**Result: 40 files stamped and idempotent; `test_supersession_ledger` 48/48 — green for the first time since 2026-08-03.** Sixteen findings whose headers still read `Confirmed — N/N PASS` while the ledger called them superseded now carry a banner that says which part is dead and which part is load-bearing.

### Q3 — Claims-and-Falsifiers-Summary revision 4

Two changes. **(i)** The charged-lepton shape angle is added as **core claim 11**, with the $0.007\%$ threshold as a stated falsifier. $\delta^*=\tfrac29$ had been a *founding principle* since 2026-07-16 and revision 3 — issued seventeen days later — did not carry it. **(ii)** A §"Where the claims live" section records that the document is now a summary and `docs/claims/` is the register.

That nineteen-day gap is the cleanest argument for the layer in this repo: **nothing in `findings/` was wrong.** F175, F253, F255 and F256 all said the right thing the whole time. What was missing was any object whose job it is to state what the project currently asserts — so a founding principle could be adopted, recorded in `CLAUDE.md`, and still be absent from the public claim set, with no check anywhere able to notice.

### Still open from §4

**Q2** (folded into Q1 — `sub_claim_superseded` exists now), **Q4** (CL003/CL006/CL010 falsifiers — physics judgement), **Q5** (F32, the orphan finding), **Q6** (draining 223 seeds), **Q7** (`docs/design/` prose vs. registry), **Q8** (`deprecated/` top level has no enforced acceptance rule).
