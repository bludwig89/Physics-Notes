# Finding coverage — the rollout: joining 317 findings to their tests and their claims

*Opened 2026-08-19. Owner: unassigned. Measured by `tools/audit_finding_coverage.py`
(landed 2026-08-19, additive, not yet in the gate). Report:
`.tmp/finding-coverage-audit-2026-08-19.md`.*

**Ratchets, armed at today's numbers, end state in brackets:**
`weak_only` **67** [0] · `dangling` **53** [0] · `claim_unset` **10** [0] ·
`unjoined` **0** [0, hold].

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
| Findings backed only by `legacy_script` debt | **1** (F204) |
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

### 2a. `findings:` becomes human-owned (decision: repair in place)

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

### 2b. A finding can say it has no test

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
distinction the current tree cannot express, and it is the one worth counting.

### 2c. A finding can say it makes no claim

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
| **3a** | **Stop `gen_test_registry.py` writing `findings:`; make it preserve.** | Until this lands, every hour of curation is one `make registry-gen` away from being erased. Nothing in §4 may start first. |
| **3b** | **Decide the F1–F16 id space.** The bundle `findings/F01-F15-findings.md` serves F1–F15; the registry names `F1 F2 F3 F4 F7 F10 F12 F16`; `findings-index.md` prints `F1`; the file stem is `F01`. | 8 of the 48 dangling ids are this one ambiguity. Any check written before the decision will encode the wrong answer. Recommended: the bundle declares `no-test (narrative-bundle)`, its members resolve to it by alias, and the alias table is the one written in `audit_finding_coverage.finding_aliases`. |
| **3c** | **Rule on `FA*/FB*/FC*/FG*` in `findings:`.** 40 of the 48 dangling ids are falsification briefs (`tests/falsification/FA01-*.md`) and first-generation tags — a different id space living in a field named for findings. | Recommended: they are legitimate references but belong in a sibling `verifies_brief:` (or `notes:`), not `findings:`. Otherwise the referential check in 5b can never reach zero and will be turned off. |
| **3d** | **F219 and the vacant numbers.** Two records cite `F219`, which `docs/design/finding-numbers.yaml` records as *deliberately unused* after a session collision. | The check in 5b must read `finding-numbers.yaml` and treat a vacant/retired number as an **error**, not a missing file — otherwise recovering the file later looks like the fix, and the number gets re-taken. |
| **3e** | **The tree is dirty: 107 uncommitted changes on `main`.** | A curation pass produces a large, mostly-mechanical diff across `tests/registry/*.yaml`. Landing it on top of 107 unrelated modifications makes review impossible and a revert unsafe. Commit or stash first, then branch. |

---

## 4. The drain — 67 findings, three buckets, ordered by what the answer costs

`python3 tools/audit_finding_coverage.py --report -` prints the live list;
section B is the work queue, already sorted by size.

### Bucket 1 — the F1–F50 era (25 findings, the bulk)

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

### Bucket 2 — the recent tail (F251–F300, 9 findings, plus F301+ stragglers)

The convention existed when these were written. Either the test is named
differently for a reason worth recording, or the record was never written.
Expect a genuine `awaiting-test` declaration or two here — that is a finding
about the tree, not a failure of the pass.

### Bucket 3 — the middle (F51–F250, 33 findings)

Mixed. Cheapest last because it is the least concentrated; by the time it is
reached, buckets 1 and 2 will have established the per-case pattern.

### Alongside: the two singletons

* **F204** — its only record is `legacy_script`, i.e. declared debt with possibly
  no failure mode at all. Either arm the record with `module:`/`entry:` or
  declare `awaiting-test`.
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
   were never meant to be — `**Claim:** none` is a normal, correct outcome, and
   it is the one that closes the check.

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
