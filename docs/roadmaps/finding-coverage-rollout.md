# Finding coverage — the rollout: joining 317 findings to their tests and their claims

*Opened 2026-08-19. Owner: unassigned. Measured by `tools/audit_finding_coverage.py`
(landed 2026-08-19, additive, not yet in the gate). Report:
`.tmp/finding-coverage-audit-2026-08-19.md`.*

**Ratchets, end state in brackets.** Armed at the morning's numbers; re-armed the
same afternoon where a step closed:
`untested` **20** [0] · `unclaimed` **0** [0, hold] · `weak_only` **20** [0] ·
`claim_unset` **0** [0, hold] · `dangling` **0** [0, hold] · `blank` **0** [0, hold] ·
`retired` **0** [0, hold] · `briefs_in_findings` **0** [0, hold] ·
`bad_declaration` **0** [0, hold] · `unjoined` **0** [0, hold].

`make coverage` runs them. `REPORT=path` writes the triage queue.

---

## LANDED 2026-08-19

| Step | What | Result |
|---|---|---|
| **3a** | `gen_test_registry.py` no longer writes or back-fills `findings:`; the `FINDING_RE` scrape goes to `evidence.mentions`. `findings:` is human-owned and means *if that finding is false, this record goes red*. | Verified by two consecutive regenerations: zero drift across 434 records, `--check` idempotent. |
| **3c** | Falsification briefs and first-generation tags are not findings. New `briefs:` field on `TestRecord`; 64 ids across 44 records moved out of `findings:`. | `briefs_in_findings` **40 → 0** |
| **3d** | `F219` cleared from `F220-field-native-execution` and `F221-noise-error-correction`, each annotated. Its `finding-numbers.yaml` entry now says the work became F222 and no file is coming. The checker reads that file and fails a record naming a blank. | `blank` **2 → 0** |
| **3b** | `findings/F01-F15-findings.md` declares `**Covers:** F1–F15` and `**Test record:** none — no-test (narrative-bundle)`. Members resolve to it; a dedicated file outranks the range, so promoted **F15** keeps its own record and CL029. `F16` — *retired* to `deprecated/findings/`, not missing — came out of `FC01-mercury-perihelion` with a pointer in `notes:`. | `dangling` **53 → 0**, new `retired` bucket at 0 |
| **2b** | A finding can say it has no test: `**Test record:** none — no-test (<reason>)`, closed vocabulary of four. An unknown reason, or a bare `none`, is a violation at ceiling 0. `check_finding_records.py` hardened to recognise the declaration rather than skipping it by accident. | `bad_declaration` ratchet, at 0 |
| **2c** | A finding can say it makes no claim: `**Claim:** none — <reason>`, plus `pending` for a card that is owed. A reason is required after the dash. | `claim_none_declared` / `claims_pending` counters |
| **2 — the teeth** | `awaiting-test` and `pending` are DEBT, not exits. They clear `weak_only`/`claim_unset` because the finding has stopped being silent, but the new `untested` and `unclaimed` totals hold the sum — so relabelling moves a finding between counters and leaves the real number where it was. | The 66-drain cannot be closed by find-and-replace |
| **4 — bucket 1** | *2026-08-19 - 13:35.* The **F1–F50 era, all 24 findings** (F21 F23 F25 F26 F26b F27 F29 F31–F36 F38–F45 F47 F48). Eleven records gained the finding on their side of the join (`wmu-phase1`+F31, `wmu-phase3`+F33, `wmu-phase4`+F34, `wmu-phase6`+F35, `wmu-phase7-backreaction` already had F36, `su2-photon-bridge`+F29, `hypercharge`+F41, `FG1-anomaly-cancellation`+F38, `FG6-two-helicity-photon`+F39, `FG7-gluon-dynamics`+F43, `FG4-dynamical-Z`+F48, `majorana-fork`+F47). Twenty findings gained a `**Test record:** record `X`` header. **Zero `awaiting-test` declarations were needed** — every one of the 24 had a real record already in the tree. | `weak_only` / `untested` **66 → 30**; bucket 1 is empty in section B |
| **4 — the measurement** | *Same pass.* Bucket 1's own recipe (steps 1–4 below) rewrites `findings:` and never renames a file, so under the original name-only `strong` test it could not move `weak_only` **at all**. Two fixes, both in `audit_finding_coverage.py`: `_NAME_ID` makes the NAME test case- and suffix-aware (`f26-rotation-law` **is** F26's record; `F26b-…` **is** F26b's), and a **two-sided DECLARED join** — the finding's header names record X *and* X's `findings:` names the finding back — counts as strong. `_FINDING_RE` is untouched, because it must keep reproducing what the generator inferred. | −4 from the name fix, −32 from the declared join, measured separately |
| **4 — bucket 2** | *2026-08-19 - 19:00.* The **recent tail: 9 findings** (F266 F268 F269 F270 F271 F274 F275 F277 F323), plus **F204**, which fell out of the same defect. Again **zero `awaiting-test` declarations** — all ten had a real record in the tree. Seven needed only the finding's side of the join (`P3.2-engine-clock`, `P3.3-exchange-bus`, `P3.4-P3.6-total-energy-and-gravity-loop`, `scenario-schema-v2`, `viz-api`+`results-compare`, `F272-F273-bz-period-lattices`, `gauge-bcc-mc-d4` all already named their finding). Three were worse than a missing header: **two records named a pre-renumber `F200`** — `F200-sterile-neutrino-dm` is F266's (renumbered 2026-07-31) and `F200-alcubierre-structural` is F204's (its own header says so) — so both declared they could go red on the *E_g sextic-coupling* finding, which neither touches; and **F323 carried its record in a field called `**Record:**`**, which neither `check_finding_records.py` nor this tool reads. `P3.4-P3.6` gained F271 (T8b–T8d, T9, T10 are F271's own evidence legs E2–E8). | `weak_only` / `untested` **30 → 20**; `legacy-debt-only` **1 → 0** (F204's real record is a `result_dump`, not the `legacy_script`); bucket 2 is empty in section B |
| **6 — the claim side** | *Same pass, verification not curation.* The eight `**Claim:** none` declarations and the cards behind the other two were read against the ledger. **Two seeded cards were statused backwards**: `CL232` (F266) read `withdrawn` off a **renumbering** banner, and `CL235` (F271) read `withdrawn` off the word *Supersedes* in a finding that is the **superseder** (`S10`). Neither finding is in any `superseded:` list. Both corrected to `live` with the reason quoted in `## Status & history`; both stay `unreviewed-seed`. | `withdrawn` **27 → 25**; `claim_unset` / `unclaimed` re-armed **10 → 0** |
| **5** | `make coverage` wired into the Makefile beside `records`/`registry`. | Failure mode demonstrated by injection: a bogus, blank, retired, or brief id in any record's `findings:` turns it red; every declaration case verified against a live finding and reverted. |

**Not yet in `run_gate.py`.** A ratchet outside the gate is a tool, not a barrier
— the same point `control-soundness-rollout.md` §0 makes. One line adds it; it
was left out because `run_gate.py` is shared infra with a live collision history
(see the `repo-gotcha-shared-infra-stale-read` note).

**Still open:** the drain's remaining **20** — all of it §4 bucket 3, the F51–F250
middle — and the no-test vocabulary rollout beyond the bundle. §6's claim gap is
measured closed (0), so its ratchets are re-armed at 0.

**Not caused here, seen from here.** Two things this pass found and did not own:
`check_summary_claims.py` is **red at HEAD** (`CL282`, a live headline card, does
not reach `papers/Claims-and-Falsifiers-Summary.md`), and
`docs/design/module-graph.json` is stale in the tree by one module
(`gauge/derive_x1_branch.py`, F325) — regenerating it is a 285-line diff that
belongs to F325's session, so it was left alone. Both are in the HEAD commit.

---

## 0. The thing to understand before anything else

`make records` is green. It has been green the whole time. It reports
*"317 findings: every declared test record exists at the tier it claims."*

It is green because **34 findings declare a record**. The other 283 declare
nothing, and a finding that declares nothing cannot fail a check that only reads
declarations. The number 317 in that message counts the files it opened, not the
findings it verified.

Underneath, the join that *does* exist runs the other way — `findings:` on each
test record — and it is **inferred, not asserted**. `gen_test_registry.py` fills
it by running `FINDING_RE` over the test's filename and its docstring:

```python
findings = sorted(set(FINDING_RE.findall(os.path.basename(rel) + " " + doc)), ...)
```

So "F26 is covered by 32 test records" means *32 files contain the string F26*.
No test file in the tree is named for F26, and no record id contains it. F26 is
the finding behind CL001 — the speed of light as a rotation rate, the load-bearing
claim of the whole model — and **nothing in `tests/` goes red if it is wrong**,
or at least nothing that says so.

That is the defect. Everything below is draining it.

---

## 1. Measured state, 2026-08-19

317 findings · 434 test records · 282 claim cards.

| Gap | Count |
|---|---|
| Findings joined to no record at all | **0** |
| Findings whose only records are prose mentions | **67** |
| Findings backed only by `legacy_script` debt | **1** (F204) — **0 since bucket 2**: F204's real record was there, filed under a pre-renumber `F200` id |
| Records naming a finding id that has no file | **53** (48 distinct ids) |
| Records with an empty `findings:` | **50** |
| Findings named by no claim card, declaring no `claim: none` | **10** |
| Findings with a no-test declaration | **0** — the state does not exist yet |

The 67 are not spread evenly. They are an **era**:

| Band | Findings | Mention-only | Share |
|---|---|---|---|
| F1–F50 | 35 | 25 | **71%** |
| F51–F100 | 50 | 10 | 20% |
| F101–F150 | 55 | 14 | 25% |
| F151–F200 | 53 | 6 | 11% |
| F201–F250 | 49 | 2 | 4% |
| F251–F300 | 50 | 9 | 18% |
| F301–F350 | 25 | 1 | 4% |

The `tests/findings/test_F###_*.py` naming convention arrived somewhere around
F150. Everything written before it inherits its association from a regex. The
recent tail (F251–F300, 9) is a different problem and worth a separate look — the
convention existed and was not followed.

---

## 2. What changes in the schema — three states that do not currently exist

### 2a. `findings:` becomes human-owned (decision: repair in place) — **LANDED**

Today `findings:` is generated and `evidence:` is generated. Nothing on a record
is a human assertion about *what this test verifies*. The fix keeps one field and
moves the regex output out of the way:

```yaml
- id: F234-Wvc-triple-closure
  path: tests/findings/test_F234_Wvc_triple_closed.py
  findings: [F234]              # HUMAN-OWNED: this test goes red if F234 is wrong
  evidence:
    mentions: [F92, F118, F234] # GENERATED: FINDING_RE hits, an index, not a claim
```

Two edits to `tools/gen_test_registry.py`:

* write the regex hits to `evidence["mentions"]`, never to `rec["findings"]`;
* **preserve** an existing `findings:` across regeneration, exactly as
  `dead_symbols` is preserved in the migration manifest.

The order matters and is forced: **the generator must stop writing `findings:`
before the curation pass starts**, or the first `make registry-gen` after the
pass silently reverts it. This is step 3a and it blocks everything in §4.

The meaning of `findings:` after this change is one sentence, and it is the test
a reviewer applies: *if this finding is false, can this record go red?* Not "is
it about" — "can it fail."

### 2b. A finding can say it has no test — **LANDED**

Lives in the finding header, parsed by the same `_HEADER` regex
`check_finding_records.py` already uses:

```markdown
**Test record:** none — no-test (analysis-only)
```

Closed reason vocabulary, four values:

| Reason | Meaning |
|---|---|
| `analysis-only` | closed-form arithmetic contained in the finding; nothing to run |
| `narrative-bundle` | a bundle or index file, not one testable finding (F01–F15) |
| `superseded` | fully superseded per `docs/theory/supersessions.yaml` |
| `awaiting-test` | **DEBT.** A test is owed. Counted by its own ratchet, drains to 0. |

`awaiting-test` is what makes this honest rather than an escape hatch: the
difference between "no test is needed" and "no test yet" is exactly the
distinction the tree could not express, and it is the one worth counting. It is
counted by `untested`, which holds `weak_only + awaiting_test`, so declaring debt
is *neutral* — it never reduces the work, it only names it.

### 2c. A finding can say it makes no claim — **LANDED**

A finding does **not** need a claim card, and the join is not 1:1 — one card
routinely rests on six findings, and infrastructure findings assert nothing a
card should hold. But absence and un-triaged absence must be distinguishable:

```markdown
**Claim:** none — infrastructure; asserts no physics a card would carry
```

---

## 3. Blockers — do these before the drain

| # | What | Why it blocks |
|---|---|---|
| **3a** | ~~**Stop `gen_test_registry.py` writing `findings:`; make it preserve.**~~ **DONE.** | Until this lands, every hour of curation is one `make registry-gen` away from being erased. Nothing in §4 may start first. |
| **3b** | ~~**Decide the F1–F16 id space.**~~ **DONE — `Covers:` + no-test.** The bundle `findings/F01-F15-findings.md` serves F1–F15; the registry names `F1 F2 F3 F4 F7 F10 F12 F16`; `findings-index.md` prints `F1`; the file stem is `F01`. | 8 of the 48 dangling ids are this one ambiguity. Any check written before the decision will encode the wrong answer. Recommended: the bundle declares `no-test (narrative-bundle)`, its members resolve to it by alias, and the alias table is the one written in `audit_finding_coverage.finding_aliases`. |
| **3c** | ~~**Rule on `FA*/FB*/FC*/FG*` in `findings:`.**~~ **DONE — `briefs:`.** 40 of the 48 dangling ids are falsification briefs (`tests/falsification/FA01-*.md`) and first-generation tags — a different id space living in a field named for findings. | Recommended: they are legitimate references but belong in a sibling `verifies_brief:` (or `notes:`), not `findings:`. Otherwise the referential check in 5b can never reach zero and will be turned off. |
| **3d** | ~~**F219 and the vacant numbers.**~~ **DONE.** Two records cite `F219`, which `docs/design/finding-numbers.yaml` records as *deliberately unused* after a session collision. | The check in 5b must read `finding-numbers.yaml` and treat a vacant/retired number as an **error**, not a missing file — otherwise recovering the file later looks like the fix, and the number gets re-taken. |
| **3e** | **The tree is dirty: 107 uncommitted changes on `main`.** | A curation pass produces a large, mostly-mechanical diff across `tests/registry/*.yaml`. Landing it on top of 107 unrelated modifications makes review impossible and a revert unsafe. Commit or stash first, then branch. |

---

## 4. The drain — 67 findings, three buckets, ordered by what the answer costs

`python3 tools/audit_finding_coverage.py --report -` prints the live list;
section B is the work queue, already sorted by size.

### Bucket 1 — the F1–F50 era (24 findings, the bulk) — **DRAINED 2026-08-19 - 13:35**

> **All 24 closed.** Not one needed an `awaiting-test` declaration: in every case
> the test was already in the tree, named for the physics, and the join was
> missing from one side or both. Four records had `findings: null` outright
> (`wmu-phase3`, `wmu-phase4`, `FG1-anomaly-cancellation`, and `hypercharge`
> which named F27/F34 but not the finding it *is*). F21/F23/F25 needed nothing on
> the registry side at all — `F306-curl-closes-at-k3` already named them and its
> own `note:` calls itself "the successor record for the F21/F23/F25 curl family";
> only the metric could not see it.
>
> **Two things this pass deliberately did NOT do.**
>
> 1. **No wholesale pruning.** Section 9 names over-pruning as the risk whose
>    error direction is *silent*, and `weak_only` does not move with it either
>    way, so section C is left as a reviewed queue rather than a diff. The one
>    attribution known to be false is flagged, not cut: `majorana-fork` carries
>    `F43`, which in that file's docstring is a **pre-renumbering** F43 ("F43 bare
>    ν_R Majorana mass step"), while today's F43 is FG-7 dynamical gluons. F47's
>    own header repeats the stale number, so the two must be ruled on together.
> 2. **No promotion off `legacy_script`.** Five of the twenty-four now declare a
>    home record that is itself declared debt — `complex-mass-chiral` (F27),
>    `su2-photon-bridge` (F29), `FG1-anomaly-cancellation` (F38),
>    `FG6-two-helicity-photon` (F39), `f45-sigma-tau-weinberg` (F45). Each also
>    has a non-debt record, so `debt_only` holds at 1 (F204) — but "declared" is
>    not "armed", and arming these is C7.4/C7.5 work, not curation.


Pre-convention findings. For each, the question is short and the answer is
usually already in the tree — the test exists, it is just named for the physics
rather than the finding (`test_hypercharge.py`, `test_su2_photon_bridge.py`,
`test_complex_mass_chiral.py`, `test_SR2_time_dilation.py`).

Per finding, ~10 minutes:

1. read the finding's `**Script:**` / `**Results:**` header — most name a real file;
2. find the record for that file in `tests/registry/*.yaml`;
3. add the finding to that record's `findings:` — **only** if the test can go red on it;
4. prune the finding out of the records that merely mention it.

Do these **in number order**, and do F25/F26/F27/F41/F45 first regardless of
order: they are the foundation findings, they carry the largest false counts
(32, 27, 11, 10), and every later finding's prose mentions them, which is
precisely why the regex inflated them.

### Bucket 2 — the recent tail (F251–F300 + the F301+ straggler) — **DRAINED 2026-08-19 - 19:00**

> **All 9 closed, and F204 with them.** The prediction above was that the
> convention existed when these were written, so either the test is named
> differently for a reason worth recording or the record was never written.
> **The second case did not occur once.** Every one of the ten had a real record;
> what was missing was a declaration, and in three cases the record's own
> `findings:` pointed at the wrong finding.
>
> | Finding | Record it declares now | What was actually wrong |
> |---|---|---|
> | F266 | `F200-sterile-neutrino-dm` (battery) | record named **F200**, a pre-renumber id — F266 since 2026-07-31 |
> | F268 | `P3.2-engine-clock` (gate) | finding-side declaration only |
> | F269 | `P3.3-exchange-bus` (gate) | finding-side declaration only |
> | F270 | `P3.4-P3.6-total-energy-and-gravity-loop` (gate) | finding-side declaration only |
> | F271 | `P3.4-P3.6-…` (gate) + `F276-curved-weyl-ordering-second-order` (gate) | the record carrying T8b–T10, its own evidence legs, did not name it |
> | F274 | `scenario-schema-v2` (gate) | finding-side declaration only |
> | F275 | `viz-api` + `results-compare` (gate) | finding-side declaration only |
> | F277 | `F272-F273-bz-period-lattices` (gate) | finding-side declaration only (T6–T9 are F277's) |
> | F323 | `gauge-bcc-mc-d4` (gate) | declared in a field called `**Record:**`, which no tool reads |
> | F204 | `F200-alcubierre-structural` (battery) | record named **F200**; F204's own header already said the filename kept the working tag |
>
> **The lesson is the mirror of bucket 1's.** Bucket 1 was a *convention* gap —
> pre-F150 tests are named for the physics. Bucket 2 is a *declaration* gap: the
> curation is right on both sides in most cases and the metric cannot see it
> until the finding says so. The three real defects were all **id drift**, not
> missing coverage: a renumber (F266), a filename that kept a working tag (F204),
> and a field name a human chose that no parser reads (F323). A renumbered
> finding is the dangerous one — the stale id resolves to a **live, unrelated
> finding**, so the record reads as covered and asserts something false, which is
> exactly the shape §5b was built for and cannot catch.
>
> **Not done here.** `run-bcc-confinement-d4` (battery) is F323's declared
> battery and still names only F265/F94. Adding F323 was judged an *addition*
> rather than a correction — the runner dumps numbers and F323's anisotropy
> derivation is not what would move them — so §9's safe direction was taken and
> the association was left alone. Also left: 20 findings' worth of bucket 3.

### Bucket 3 — the middle (F51–F250, 33 findings)

Mixed. Cheapest last because it is the least concentrated; by the time it is
reached, buckets 1 and 2 will have established the per-case pattern.

### Alongside: the two singletons

* **F204** — ~~its only record is `legacy_script`~~ **CLOSED with bucket 2.** It was
  never debt-only: `F200-alcubierre-structural` is F204's `result_dump` record,
  filed under the working `F200` id the finding's own header flags. The
  `legacy_script` (`run-warp-openitems-explore`) stays declared debt; it is no
  longer the only record. `debt_only` is 0.
* **50 records with an empty `findings:`** — not in the 67 (no finding is missing
  because of them), but each is a test that verifies nothing nameable. Sweep once
  after bucket 3; expect most to be infrastructure and legitimately empty.

---

## 5. The checks — what makes it stay fixed

All three land as **ratchets** first, armed at today's counts, wired into
`run_gate.py` alongside `check_finding_records` and `check_control_soundness`.
A hard failure on day one only trains people to skip the check; that lesson is
already written down in `check_finding_records._CEILING`'s comment.

| # | Check | Rule | Armed at |
|---|---|---|---|
| **5a** | finding → test | every `findings/F*.md` is named by ≥1 record's `findings:`, **or** declares `no-test (<reason>)` from the closed vocabulary | `weak_only` 67 → 0 |
| **5b** | registry → finding | every id in a record's `findings:` resolves to a real `findings/F*.md` and is not vacant/retired per `finding-numbers.yaml` | `dangling` 53 → 0 |
| **5c** | finding → claim | every finding is named by ≥1 card **or** declares `**Claim:** none — <reason>` | `claim_unset` 10 → 0 |

5b is the direct mirror of `check_claims.py` rule 3, which has enforced exactly
this for claim cards since D12. The test registry never got the same rule, which
is the whole reason 53 records drifted.

Add `awaiting-test` as a fourth ratchet once 5a is at zero — it is the honest
successor number, and it should not be allowed to grow.

`make coverage` is the entry point; `make coverage LIST=1` prints the queue.

---

## 6. The ten claim-gap findings

`F01 · F133 · F134b · F160 · F268 · F269 · F274 · F275 · F308 · F314`

Not a backlog of ten cards to author. Each needs **reading once** to answer one
question — *does this finding assert something a card should carry?* — and then
a declaration either way. Expect most to close as `**Claim:** none`: F01 is the
narrative bundle, F133 and F134b are block-spin engine/integration work, F308 and
F314 are recent and may simply be un-carded yet.

Two of the ten (F268, F269) are also in the mention-only 67, so batch them with
bucket 3 and answer both questions in one read.

---

## 7. Steady state — what a session does from now on

```bash
casim index                              # next free number, as always
# ... write the module, the finding, the test ...
# write the record and set findings: BY HAND — the generator will not do it
make registry-gen                        # refreshes evidence:, preserves findings:
make coverage                            # 5a/5b/5c, within ceilings
make gate
```

Three rules:

1. **`findings:` is a claim you are making.** *If this finding is false, this
   record goes red.* If you cannot say that sentence about the pair, do not write
   it — `evidence.mentions` already holds the weaker fact.
2. **A finding with no test says so, with a reason.** Silence is the state this
   rollout exists to remove; do not put it back.
3. **A finding with no claim says so too.** Findings and claims are not 1:1 and
   were never meant to be — `**Claim:** none — <reason>` is a normal, correct
   outcome, and it is the one that closes the check. `pending` when the card is
   genuinely owed.

`/finding` writes both fields into the template, so a new finding starts with the
questions in front of it rather than answered by silence.

---

## 8. Sequencing

| Step | Depends on | Rough size |
|---|---|---|
| 3e commit/stash, branch | — | minutes |
| 3a generator change | 3e | ~1 h, small diff, high leverage |
| 3b/3c/3d id-space rulings | — (can run in parallel with 3a) | one sitting, decisions not code |
| 5b referential check + dangling sweep | 3a, 3c, 3d | mostly mechanical once ruled |
| Bucket 1 (25) | 3a, 3b | the bulk; batch by sector, review per batch |
| Bucket 2 (9), Bucket 3 (33) | bucket 1 pattern | steady |
| §6 claim triage (10) | — | one sitting |
| 5a/5c checks + `make coverage` wiring | buckets drained enough to arm | small |
| Ratchet ceilings to 0, indexes regenerated | all | small |

**Batch by the registry's own sector vocabulary** — `core`, `forks`, `gauge`,
`interactions`, `lattice`, `particles`, `suite` — one YAML file per batch. That
keeps each diff inside one file, which is the only thing that makes a
300-line registry diff reviewable.

---

## 9. Risks

* **Concurrent sessions.** Finding numbers have collided in this repo before
  (F219 and F229 are vacant because of it, and the F129 note in project memory
  records another). A curation pass touching all seven registry YAMLs is maximally
  exposed. Land it as one branch, one review, one merge — not incrementally on
  `main`.
* **Regeneration reverting curation.** Mitigated by 3a, which is why 3a is first
  and not negotiable.
* **Over-pruning.** Removing a finding from a record's `findings:` when the test
  genuinely does cover it silently *reduces* real coverage. The safe direction of
  error is to keep the association and note the doubt; `evidence.mentions`
  preserves the regex answer permanently, so nothing is lost by pruning, but the
  reviewable record of what was intended lives in the commit message. Write it.
* **`make gate` runtime.** `audit_finding_coverage.py` reads 317 markdown files
  and 8 YAMLs — sub-second, no imports of `casim` physics. It will not move the
  45 s sandbox ceiling `control-soundness-rollout.md` §0b is still waiting to see
  measured.
