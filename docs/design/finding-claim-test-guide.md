# Finding, Claim & Test Guide

*Split out of `CLAUDE.md` on 2026-08-19 to keep the always-loaded file small. CLAUDE.md
keeps a short, self-sufficient summary of each section below under the same heading
("Claims", "Concurrency", the test-registry subsection of "Building or changing a
module"); this file is where the full reasoning, edge cases, and enforcement detail
live. Load it before writing, reviewing, or auditing a finding, a claim card, or a
test record.*

---

## Claims

> **Any algebraic or physics-tested claim or element that extends, derives, or contradicts anything in quantum mechanics, the Standard Model, general relativity, or special relativity gets a card in `docs/claims/` and a row in the registries it touches.**

The bar is *extends established physics*, not *is interesting*. An engine-wiring result, a numerical technique, a refactor or a status record does **not** get a card — and where a finding is judged not to clear the bar, that judgement is itself recorded (`docs/audits/consolidation-plan-2026-08-04.md` §5), so "no card" is a decision rather than an omission.

**A claim is not a finding, and confusing them is the failure this layer exists to prevent.**

| Object | Question it answers | Tense |
|---|---|---|
| `findings/F{N}-*.md` | What did we do, and what came out? | past — written once, superseded rather than rewritten |
| `docs/claims/CL{N}-*.md` | What do we assert, right now, and what would kill it? | **present** — narrowed, made contingent, or withdrawn as the model moves |

A finding that says `**Status:** Confirmed — 5/5 PASS` is *correct to keep saying that* even after the ledger supersedes it: it records what a session concluded. The **claim** resting on it is what has to move. Sixteen findings in this repo are named in a `superseded:` list while their own headers still read "Confirmed" — that is not a defect in the findings, it is the gap the cards fill.

### Writing or changing a card

1. **Copy `docs/claims/TEMPLATE.md`.** Take the next id from `next_claim` in `docs/claims/registry.yaml`. `CL` is its own namespace and does not overlap `F<N>`, `D<N>`, `S<N>` or `C0`–`C9`.
2. **Fill the front matter from the closed vocabularies** — `docs/claims/README.md` has each one with its meaning. There is no `unknown`: a claim whose status cannot be determined is `open` **with the gap named**, which is a state someone can act on.
3. **State the claim so a reader who disagrees knows what they are disagreeing with.** Numbers verbatim from the source; no rounding, no "approximately" the source did not say.
4. **`falsifier: none` requires the structural reason to be named in the section.** "Structural" is a reason only when the structure is named. Otherwise it is `unset`, which is ratcheted debt.
5. **`make claims`** (= `casim index --only claims` + `check_claims.py`), then `make gate`.

### What a card may and may not change

Writing or editing a card **never** edits a finding, a physics module, a test record, the exactness inventory or the supersession ledger. If the position changed because the *physics* changed, that is a research session with its own claim on `docs/design/session-claims.yaml` and its own finding number; the card is updated to match afterwards.

The inverse is the point of the layer: **a finding may be superseded without any claim changing, and a claim may be narrowed without any finding changing.** Neither event is visible in the other object.

### What the gate enforces

`tools/check_claims.py` runs in `make gate`. Closed vocabularies, unique contiguous ids, filename == `{id}-{slug}.md`, every `findings:` entry resolving to a real file, every backticked repo path existing, `rolls_up_to` resolving, withdrawn cards keeping a non-stub retraction record, and the three debt ratchets (`unreviewed-seed`, `falsifier: unset`, `exactness: unset` — these may fall, never rise).

**The rule that does real work:** a card with `status: live` **fails** when *every* finding it rests on is named in a `superseded:` list in the ledger. That is the machine-checkable form of "overstated". It deliberately does **not** fire on a *partial* supersession — the standing lesson of this repo is that almost nothing here is superseded wholesale (of 14 test files one audit called superseded, exactly one was), and a check that flagged partials would train people to ignore it.

### Do not archive the falsification record

`kind: no_go` cards and `status: withdrawn` cards are the **last** things that should ever leave the tree. A withdrawn claim that is deleted is a claim that gets re-made — CL023–CL027 are the horizon-free black hole and its four dependent falsifiers, published live between 2026-06-08 and 2026-08-02, and each card's `## Status & history` **is** the retraction record. A gate test asserts they survive. The same applies to negative results in `findings/`: they describe themselves in the vocabulary of obsolescence ("a four-avenue no-go", "$d=6$ and $d=9$ excluded"), so any keyword sweep for dead material surfaces them first and most confidently. **Do not run one.**

---

## Test registry

### The test registry (D9) — `tests/registry/*.yaml`

One YAML per sector; `src/casim/tests/registry.py` loads them. `casim test` is the runner. `pytest` reaches the registry two ways — file-based `assertion` records by ordinary collection of their `path:`, and entry-driven records through `tests/casim/test_registry_entries.py`, which parametrises over `select(tier="gate")` records that name an `entry:` (`tests/conftest.py` hides those files so nothing runs twice under two contracts). **`kind: scenario` records have no `path:` and no `entry:`, so pytest cannot see them at all** — that is the 27-vs-24 gap in V-004. Use `casim test --tier gate` when you need the whole tier.

Field ownership matches the manifest convention: **`evidence:` is generated** and rewritten by `make registry-gen` on every run; **every other field is human-owned** and preserved across regeneration, keyed by `path:`.

```yaml
- id: F234-Wvc-triple-closed
  path: tests/findings/test_F234_Wvc_triple_closed.py
  kind: assertion            # assertion | result_dump | scenario | legacy_script
  tier: gate                 # gate | battery | archive
  sector: particles
  findings: [F234]
  module: casim.engine.particles.derive_lambda6_sextic
  entry: check_triple_closure
  params: {delta_star: 2/9}
  expect: {exactness: exact, tol: 0}
  results: [test-results/F234_Wvc_triple_closed.json]
```

- **`validate()` refuses a record with no failure mode.** A `legacy_script` is *labelled* debt; anything else must be able to fail. There is no third state, which is what closed P1's "RAN limbo".
- **A gate-tier `assertion` record declares a `control:` — a perturbation under which it MUST go red (D9/H2, 2026-08-07).** `validate()` refusing a record with *no declared failure mode* does not establish that the declared one can trip; F22's headline check was `x − (1 − 2(1−x)/2)`, identically zero for any expression, and it was green for months. A control names the perturbation and the legs it reddens:

```yaml
  control:
    - params: {linear_control: true}      # applied exactly as `casim test --param` would
      reds:   [G10-3, G10-4, G10-5, G10-6]   # these MUST go red; leg tags, resolved against the payload
      reason: dispersion replaced by exactly linear c|k|, so every lattice correction must vanish
      # only: false      # opt out of "and nothing else goes red", and say why in reason
```

- **Whether a record CAN fail is measured, not inferred — `make can-fail`.** Never decide it by reading the code or an AST: a dispatch table (`for name, fn in CHECKS: fn()`) presents one Call node on a loop variable, and that alone made three records read as "cannot fail" while they held 41, 39 and 30 reachable asserts (completeness Amendment 3). `casim.tests.runner.probe_can_fail` traces a real run and reports which `assert`/`raise` lines executed, plus whether the payload carries a verdict key — both are failure routes. Journalled to `test-results/can-fail.json` (**commit it**); `check_finding_records.py` prefers the measurement over its own static walk and says which answered. A timeout is **INCONCLUSIVE**, never cannot-fail. If you need to know whether a check can fail, **break it and watch**: import the module, corrupt one dependency it asserts on, confirm `AssertionError` propagates. Three lines, decisive.
  `make control` runs them and journals the verdicts to `test-results/control-soundness.json` (**commit it**); `make gate` then checks *statically* that every control is well-formed and carries a `CONTROL` verdict at the current code **fingerprint**, so touching a driver turns the gate red naming the record. Verdicts are `CONTROL` / `LEAK` (perturbation applied, still green) / `SPILL` (reddened legs it did not declare) / `INVALID` (leg absent, already red, or the driver crashed instead of failing) / `NOCTRL` (debt). **Write the MEASURED set into `reds:`, not the set you expected** — the seeding pass corrected two findings' own prose this way. A record with no control is counted debt (`gate_assertion_no_control`, ratcheted to zero); `make control-todo` lists them with the keyword arguments each entry point already accepts.
- **`sector` uses the module-sector vocabulary**, not a physics grouping. The physics grouping is `--finding`, which is exact rather than inferred.
- **A `result_dump` record fails by baseline diff against git HEAD.** Declaring the artifact is what arms it — but a promotion is only *proved* when a run actually rewrites that file; the runner's mtime guard reports the rest as `SKIP`, never a false `PASS`. `tools/arm_test_registry.py` does that pass and journals every verdict.
- **After any arming or sweep run: `--restore`, then `--apply`.** An arming run rewrites committed baselines in place, and forgetting `--restore` leaves modified baselines the strict drift checker will flag.
- **A sweep never writes a baseline.** `casim test --param k=v` runs in a temp dir and diffs in memory.
- **Baseline drift below 1×10⁻¹² is the `machine` floor, not a change.** The runner reports sub-floor deltas separately; `tools/check_result_drift.py` runs strict at 1e-15 and will disagree. Only `expect: {strict_floor: true}` overrides.
- **A baseline that is out of date *because the physics improved*** goes in `docs/theory/supersessions.yaml`'s `baselines:` block as `stale_by_design` (reports `STALE`, needs `clears_by:`) — not as `candidate`, which still reports `FAIL` on purpose so the category cannot become a parking lot. `tools/triage_baselines.py` splits the queue; `docs/status/baseline-provenance.md` is the standing decision list.

---

## Concurrency

### Concurrency — claim your TOPIC at session start, take a NUMBER at write time

Finding-number and test-ID collisions between parallel sessions have happened at F110, F129, F219, F229–F232, F262, and during C1/C2 and C5/C6. Every one had the same shape: two sessions each read the same "max finding number", each wrote the next one, and the loser found out afterwards. **Reading the max is not a reservation.**

**The two jobs are separate, and bundling them was the defect (revision 2, 2026-08-05).** Advertising your topic and sector has to happen at *session start* — its entire value is warning a parallel session off before either has done the work. Allocating a finding number cannot happen then, because nobody knows at session start how many findings a question will produce. The old protocol forced the second onto the first's clock, so every session guessed "3 to 5", most landed one, and the remainder stranded as gaps: seventeen interior gaps between F291 and F314 by 2026-08-04, each costing a hand-written declaration for a number nobody ever used.

**The claim board is `docs/design/session-claims.yaml`.** Its `about:` block holds the full schema. The protocol:

1. **Before any research, open a claim — with no numbers.** As soon as a question is posed or a model element is picked up, append a claim with your session handle, `status: open`, your sector, and a one-line topic. There is no `findings:` field and no block to size. This is one small append and it is the whole collision-avoidance mechanism.
2. **Claim your sector in the same entry**, and work in one sector. Rewire only files you own — a file importing another sector's module is still *your* file if it lives in your sector.
3. **Take a number only when you write the file, one at a time.** Run `casim index` and read the **`NEXT FREE NUMBER`** line. That is the lowest number declared `status: free` in `docs/design/finding-numbers.yaml` — a number nobody ever wrote at. In **one edit**: create `findings/F{N}-....md`, add `{N}: findings/F{N}-....md` to your claim's `used:` map, and **delete that number's `free` entry from `finding-numbers.yaml`**. Deleting the entry *is* the act of spending the number. Need a second finding? Repeat then, not now.
4. **Lowest free, not max+1.** The allocator hands back numbers below the maximum on purpose: the old scheme left a 22-number backlog (F280 upward), and ordinary work drains it. A finding landing at F280 on 2026-08-05 is expected, not a mistake. `casim index --check` **fails** if a `status: free` entry names a number whose file now exists — that is a spent number still advertising itself as available, which is how two sessions get handed the same one.
5. **Release at session end.** Set `released:` and a `release_note:` saying what landed. There is no "reserved but not used" to report — nothing was reserved. Released claims stay on the board; it is also the collision history.
6. **Retakability is declared, never inferred.** "No file exists" does not mean free. F219 and F229 have no file and are **not** retakable: the changelog records them as abandoned after a collision, so a reader chasing that citation must not land on unrelated physics. Only `status: free` is free; `resolved` and `retired` are not.

Writing a finding at `F<N>` claims the `F<N>-*` **test-ID namespace** with it, so a registry record `id: F280-something` needs no separate reservation. List a test ID explicitly on the board only when it does *not* derive from a number you hold — `run-*`, `fork-*`, `scenario-*`, or an `F<N>-*` on someone else's number.

**What the residual race is, honestly.** The window between reading `NEXT FREE NUMBER` and writing the file is no longer covered by a reservation. It is now seconds rather than the whole session, and a collision inside it produces a **duplicate**, which `casim index` already refuses loudly. The old window was hours and its failure mode was a silent gap, which nothing refused. That trade is the point of the change. The older `claims:` block in `docs/design/module-migration-manifest.yaml` is the migration-era sector board and is kept as history; new claims go in `session-claims.yaml`.

---

## Finding coverage rollout

The join between findings, tests, and claims (which `findings:` fields are a claim rather than a scrape, the `no-test`/`no-claim` declaration vocabularies, and the `5a`/`5b`/`5c` ratchets `make coverage` enforces) is documented in full in `docs/roadmaps/finding-coverage-rollout.md`. CLAUDE.md's own "Finding coverage — steady state" section (under "Building or changing a module") carries the day-to-day loop and the three load-bearing rules; read the rollout doc for the history, the measured buckets, and what's still open (§4 bucket 3, the F51–F250 middle, as of 2026-08-19).
