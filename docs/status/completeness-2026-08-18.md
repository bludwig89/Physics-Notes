# Completeness overview — 2026-08-18 - 10:21

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: full sweep, 74 rows (blocks A, B, C, E, K, G, H) plus the 28-row parameter ledger (D).
Previous benchmark: `docs/status/completeness-2026-08-07.md`, **as amended through its Amendment 11
(2026-08-17 - 21:50)** — that file was amended eleven times after issue and its own scoreboard was
never updated for any of them, so the honest comparison is against the amended tables, not the
scoreboard as first written. Both are given.*

**Health probe (what actually ran, and what could not).**

> **The device workspace was unavailable for this entire session**, as it was for the F324 session
> before it. `make gate`, `make indexes-check`, `make registry`, `make numerics`, `make health`,
> `make claims`, `make control` and `casim test` **were not run**. Everything below was measured by
> staging the repository's own files into an isolated container and running the repository's own
> checkers against them, or by parsing the committed artifacts directly. Where a number could not be
> obtained that way it is recorded as **NOT VERIFIED THIS RUN**, not as green.

**Measured from the committed tree this run.** Test registry: **429 records**, kinds
`result_dump` 225 / `assertion` 154 / `legacy_script` **47** / `scenario` 3; tiers `battery` 348 /
**gate 81** (was 58 at the previous report's issue, 63 after its Amendment 1). Gate-tier
`kind: assertion` records **78**, of which **30** carry a `control:` block declaring **76** controls
— against 61 / 13 / 29 at Amendment 3. Module registry: **218 modules**, **51 channel-driven
(23.4 %)**, 90 test-only, 46 standalone, 24 unreferenced, 4 package-only, 3 entry-script; statuses
live 157 / `fork_live` 25 / `fork_unclaimed` 23 / `partial` 12 / `dead_candidate` 1. Exactness tally
(generated block): **exact 159 / machine 196 / quantitative 185**, coverage **540 of 540 (100 %)**
across 446 artifacts, generated "through **F323**". Claims: **280 cards** — live 151, open 87,
withdrawn 27, narrowed 5, contingent 5, not_claimed 5; **223 `unreviewed-seed`**. `casim inventory`'s
own 14/14 engine checks are green as of the committed artifact (2026-08-17 - 21:54).

> **Gate: RED, and this run demonstrated it rather than inferring it.** The highest finding on disk
> is **F324** (`findings/F324-ncolour-bracket-closed.md`, 2026-08-17 - 19:50) and it appears in **no
> index**: not `findings-index.md` (which still reports *"max F323"*), not `claims-index.md`, not
> `docs/status/open-derivations.md`, not `docs/status/exactness-inventory.md`, not
> `docs/design/session-claims.yaml`, and not `docs/status/changelog.md`. Its declared record
> `F324-ncolour-bracket` **does not exist** in `tests/registry/*.yaml`, and its claim card
> `docs/claims/CL281-ncolour-bracketed-to-three.md` exists on disk but is absent from
> `claims-index.md` and `docs/claims/registry.yaml`.
>
> `tools/check_finding_records.py` — the guard the previous report's Amendment 1 built for exactly
> this defect, wired into `make gate` at `tools/run_gate.py:127` — was executed here against the
> repository's own registry and **fires**:
>
> ```
> F324-ncolour-bracket-closed.md: declares record `F324-ncolour-bracket`, which does not
> exist in tests/registry/. Either write the record or correct the finding's header.
> ```
>
> So `make gate` is red on a check that ran, not on one that timed out. `make indexes-check` and
> `make claims` are red by the same cause. **F324 says so itself** (§11: *"`make gate` was not run…
> the record, indexes and claim card are written but unarmed… `**Status:** Confirmed` is withheld
> deliberately"*), which makes this an honestly-declared debt rather than a false claim — but the
> barrier is red until the arming pass runs, and this report grades it that way.
>
> **NOT VERIFIED THIS RUN:** every one of the 81 gate records (none was executed); the
> `audit_tests --ratchet` triple (`unfalsifiable` / `no_assert` / `import_time_work`, last committed
> baseline 70 / 231 / 323); the `make numerics` and `make constants` ratchets; whether the 25→76
> declared controls still verify RED at the current code fingerprint.

---

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A Foundations (12) | 4 | 1 | 1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| B Gauge (12) | 4 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| C Matter (7) | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| E Gravity (13) | 3 | 1 | 4 | 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| K Cosmology (12) | 0 | 0 | 1 | 7 | 0 | 0 | 1 | 3 | 0 | 0 |
| G Emergent (10) | 1 | 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| H Integrity (8) | 0 | 0 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total (74)** | **14** | **3** | **16** | **35** | **0** | **1** | **1** | **4** | **0** | **0** |

*Every cell is counted from the grade column of the block's own table below; row sums equal the
block sizes (12, 12, 7, 13, 12, 10, 8 = 74). Against the previous report **as amended** (14 / 3 /
18 / 32 / 0 / 1 / 2 / 4): three rows move — K3 `OPEN → PARTIAL`, and **H4 and H6 both
`QUANT → PARTIAL`**. Against its scoreboard **as first written** (14 / 3 / 15 / 35 / 0 / 1 / 2 / 4)
the totals look almost unchanged, which is an artifact of that scoreboard never having been updated
for its own eleven amendments.*

**Parameter ledger: 6 of 28 derived, 2 partial, 6 fitted or free input, 14 open or absent** —
**unchanged for the fourth consecutive report.** No quark-mass, CKM, $\alpha$, $v$, $m_H$ or
$\Lambda$ work has landed in eleven days. F320's absolute $m_W$ and $m_Z$ do not move this ledger,
correctly: they are outputs of $\{g, g', v\}$, not members of the 28.

**The shape of this report.** The physics surface moved in one direction and the record-keeping
surface moved in the other, and the second is larger. Six findings — **F310, F312, F315, F316,
F317, F318** — landed between 2026-08-11 and 2026-08-16 and appear **nowhere** in the previous
report despite its eleven amendments; three of them narrow rubric residuals materially (B1, A1, A6).
The mechanism is visible once stated: **every one of the eleven amendments was written by the
session that produced the finding it records**, so a finding whose session did not amend the report
is invisible to the rubric no matter how load-bearing it is. Against that, the single sharpest item
this sweep found is that **all three legs of the previous report's gap #5 were closed by F311 on
2026-08-11**, and the report's own Amendment 9, written six days later, records two of them as still
open "on their fourth report" and re-does the third from scratch without citing F311 — while
`open-derivations.md` had already recorded the closure.

---

## The five things most worth building next

Ranked by (load-bearing × distance from closure).

### 1. Arm F324, and then stop letting a finding land unarmed — the defect is now on its fifth instance

**What.** F324 is a complete, adversarially-reviewed finding with 14/14 measured legs and eight
declared controls, and it is invisible to every index and every checker in the tree. Its record does
not exist, its claim card is on disk but not in the registry, and `make gate` is red because of it.

**Why it matters.** This is the same defect as F298/F299/F300/F301/F303 (previous report, item 2 and
Amendment 1), and it is the **first instance the guard built for it actually catches** — which is
the good news and also the whole point: the guard converts a silent hole into a red gate, and the
tree has been sitting on a red gate. More importantly, F324's own §11 names the cause precisely and
it is not carelessness: *the device workspace was unavailable*, so the session could not run
`casim index`, `make claims`, `make gate` or `make control` even though it wanted to. The tree has
no path for "physics verified, tree-unverified" other than shipping the finding and hoping the next
session arms it. Two sessions in a row have now hit it.

**What blocks it.** Nothing but a working environment: F324 §11 gives the exact order —
`make indexes` → `make claims` → `make gate` → `make control`.

**Smallest next step.** Run those four, in that order, and re-check `check_finding_records.py`.
Then, separately, decide what the tree does when the workspace is down: an explicit `unarmed:` field
on a finding that the index counts and the gate tolerates, versus the current situation where an
honest declaration inside §11 is invisible to every automated reader. The second half is the durable
fix and it is cheap.

### 2. The colour-normalisation fork X1, and $d_1$ — unmoved for eleven days, and now the *only* thing between the tree and its strong sector

**What.** Unchanged from the previous report's #1. F144's bare colour coupling is normalised on the
**centre** while the model's own confinement engine implements **Casimir** (F299), and F303 found no
argument for the centre reading and closed three candidate reconciliations exactly. The deciding
computation is $d_1$ — one leg of three still open ($\Delta C_\text{vertex} = -2.0160$, 36.2 % of
$\Delta C = -5.5755$, bracketed $[-2.257, -1.446]$).

**Why it matters, and what changed about it.** F324 **removes B10 from the fork's dependents** —
$N_c = 3$ no longer needs the centre reading, because it now follows from F298's structural
$N_c \le 3$ paired with the $\mathbb Z_2$ doublet parity, neither of which touches the branch. That
is a genuine reduction in the fork's blast radius. What survives is still large: B8, D16, G5, E3,
Q1, Q2 and one of the six quantities the model claims to derive with zero free parameters.

**What blocks it.** The apparatus is built (F280 formulation, F305 vertices, F307 one code path,
F308 refold repaired) and one physics choice sits upstream: `open-derivations` **L6** — which object
is "the rule's gauge action" at finite $a$, on which the *sign* of $b_0$ rides. F305 deliberately
declined to pick.

**Smallest next step.** Decide L6, then finish leg 3. **Nothing has been recorded against $d_1$
since F308 landed on 2026-08-11** — this is its second consecutive report at a standstill, and it
was the previous report's #1.

### 3. K9 has a live contradiction again, and it is not the one the row has been carrying — **ADJUDICATED by Amendment 4, 2026-08-18 - 17:15**

**What.** K9's residual has read *"two unreconciled pictures (F193/F196/F241 vs F192)"* for three
reports. **F311 (2026-08-11) dissolved that framing** — F192's open-list was superseded by F193
twelve and three-quarter hours after it was written, F192's $w=-1$ sign result is *vacuous* rather
than contradicted under $\rho_\text{vac} = 0$, and its $10^{121}$ **double-counts**, because in an
induced theory the zero-point mode sum *is* $1/G$ and cannot also be the source. `open-derivations`
row G1 records exactly that and calls K9 adjudicated.

**And then F319 (2026-08-16) priced the move and found it unaffordable.** F59's $1/16\pi G$ and
F164's $\rho_\text{vac}$ are the $a_0$ and $a_1$ moments of **one** zero-point sum — same modes,
same measure, same $\tfrac12$ — so demanding both observables is a 2×2 solve returning a cell of
8.29 Gpc. F164's channel (i), which is precisely the route F193 turned "from a position into a
derivation", is therefore **excluded**, and any survivor needs order-selectivity between two
*adjacent* heat-kernel coefficients of $\ge 1.27 \times 10^{116}$.

**Why it matters.** F311's C-leg is an *accounting* argument ("do not put the same sum on both
sides"); F319's U8 is a *mechanism* argument ("show me the thing that suppresses $a_0$ and spares
$a_1$, and here is its price"). They are not obviously inconsistent, but they cannot both be the
row's status: one says K9 collapsed to a single $O(1)$ coincidence, the other says the surviving
picture's mechanism is closed. **Neither finding cites the other**, five days apart, and
`open-derivations` G1 currently carries only F311's side. This is the *same shape* as X1 — two
adopted results that disagree — and Part D of that ledger has exactly one row.

**Smallest next step.** One session, no new physics: state whether F193's "the CA ground state costs
nothing to update" is an order-selective statement or a uniform one, and therefore whether F319 U8
excludes it. If it is uniform, K9's residual is F164 channel (ii) with a price tag; if it is
order-selective, F319 owes the row a re-reading. Either way **open-derivations gains a second Part D
entry**, which is worth as much as the answer.

> **Done, Amendment 4, 2026-08-18 - 17:15 — and the prediction in the last sentence was wrong, which is
> the part worth recording.** The answer is **uniform**: F193 A2 deletes the $\tfrac12$-per-mode
> $c$-number, and F59 Part C builds $1/16\pi G$ out of that same $\tfrac12$, so the deletion cannot
> tell the two moments apart. F193 **Part A** is therefore inside CL275 and excluded. But the branch
> this section did not consider is the live one: F193 **Part B** and F196 are a *different* mechanism,
> order-selective by construction, and they deliver $120.66$ of the required $120.76$ decades at zero
> cost to $a_1$. So F311 C3 is **withdrawn** (its own falsifier 5, hit by F319 U8) and F319 §6's "sole
> survivor" is **narrowed** — one side loses a leg and the other loses a sentence, which makes this an
> adjudication rather than a contradiction, and **no Part D row is opened**.

### 4. B9 now has two published numbers, and the tree does not notice — **CLOSED by Amendment 2, 2026-08-18 - 16:20**

**What.** F311 A2/A3 (2026-08-11) closes B9's leptonic $\Delta\alpha(M_Z)$ residual from $0.245\%$
to **$0.00158\%$** by identifying it as the two-loop leptonic term, using the standard Källén–Sabry
leading form — cited, not derived here (F311 §"Leg A's two-loop formula is cited, not derived"). F322
(2026-08-17) closes the *same* residual to **$0.0495\%$** using F261's sympy-exact $b_1 = 1$, i.e.
the model's own two-loop leading log, and explicitly leaves the two-loop non-log constant open at
$1.559\times10^{-5}$. **F322 does not cite F311 anywhere.**

**Why it matters.** The two are physically compatible — F322's residual is exactly what F311's
imported constant supplies — but they are not the same *claim*, and both are live: the $0.00158\%$
sits in `open-derivations` (which marks B9 closed), the $0.0495\%$ sits in the current completeness
report's Amendment 9 and in claim card CL280. The honest headline is F322's, because it is the one
the model derives; F311's requires a literature constant and should be quoted as such. Right now a
reader picks whichever document they open.

**Smallest next step.** One line in each document: state $0.0495\%$ as the model-internal number and
$0.00158\%$ as the number after importing the Källén–Sabry constant, and cross-reference F311 from
F322's row. Then decide whether deriving the two-loop leptonic bubble on the model's own fields
(F311 §"a different and larger piece of work", F261's machinery) is worth a session.

### 5. Q4 — the isospin splitting the model's own BBN excludes at $36.6\sigma$

**What.** Unchanged and still the cheapest live target in the tree. F297's BBN measures $m_n - m_p$
to $\pm 0.0056$ MeV where F122's own acceptance check used $\pm 1$ MeV; the model's $+1.51$ MeV is
excluded at $36.6\sigma$ in helium and by a factor 2.7 in $\tau_n$ (331 s against $878.4 \pm 0.4$).
One of two terms is wrong by 0.217 MeV.

**Why it matters.** It is a bounded numerical target with an acceptance band and a test that already
exists, it is the model finding its own error through an assembly grading its inputs, and **G5 and
G7 both carry it**. F309 confirmed $g_*$ is orthogonal to it and neither helps nor hurts.

**What blocks it.** Nothing. F297 §10 item 1, verbatim: fix the EM self-energy term in F122, or show
the F40 $d$–$u$ ratio moves.

**Smallest next step.** That, in one session. **It has now been open across two reports with nothing
recorded against it**, which is the second-longest standstill in this document after $d_1$.

---

## What is ABSENT

**The table is empty**, for the second consecutive report. No rubric row in blocks A, B, C, E, K, G
or H is graded `ABSENT`.

| # | Requirement | Status |
|---|---|---|
| — | — | No row in blocks A, B, C, E, K, G or H is `ABSENT` as of this sweep |

**Carried, and with a caveat this sweep must attach.** The previous report named three things with
zero repo-wide hits that sit *inside* rows rather than as rows of their own: proton decay / a
baryon-number-violating rate (inside C7 and K6), the Unruh effect (inside E9 and G10), and
topological defects as relics (inside K7 and K12). **This sweep could not re-run that measurement**:
the whole-tree grep the command prescribes needs the device workspace, and only the indexes and
ledgers were greppable here. Against those, all three still return zero — and so does `Witten`,
which is demonstrably wrong, because F324 §2 is built on the Witten $SU(2)$ global anomaly. That is
a clean illustration of why the command says to grep the tree rather than the index, and the three
sub-row gaps should be re-measured properly next sweep rather than inherited a third time.

**What the empty column means.** It still does not mean the model accounts for everything the rubric
asks. It means every rubric row has *a sector*, and the dominant grade is `PARTIAL` — 35 of 74, up
from 32 in the amended previous state, and the increase is entirely integrity rows moving *down*.
The remaining work continues to be depth and integrity work rather than coverage work, and this
report is the first in which the integrity half moved backwards.

---

## Regressions since 2026-08-07

Graded against that report **as amended to 2026-08-17 - 21:50**.

| Row | Was | Now | Why |
|---|---|---|---|
| H6 Reproducibility | QUANT ("recovered", 57/58 gate records seen green) | **PARTIAL** | The gate is **red**, demonstrated this run by executing `tools/check_finding_records.py` against the committed registry: F324 declares `F324-ncolour-bracket` at tier gate and no such record exists. `make indexes-check` and `make claims` fail by the same cause — F324 and CL281 are on disk and in no index. No gate record was executed this run, so the 81 are unverified as well as the barrier being red |
| H4 Retraction hygiene | QUANT ("recovered, and verified this run") | **PARTIAL** | The ledger machinery is sound and got better (S20, S21, `make citations`). The *outward* half now fails on H4's own second clause — *"is any derived result still published as an input?"* `papers/Claims-and-Falsifiers-Summary.md` (rev 4, 2026-08-04) still lists **"$m_W$ and $m_Z$ in absolute terms"** under **Scope — what is not claimed**, fourteen days after F320 derived them and CL016 was withdrawn with a full retraction record; it also still quotes $\alpha_s(M_Z) = 0.11955$, $+1.7\%$, $2.1\sigma$ without naming the X1 branch that number belongs to. The cards are right and the public summary is stale |
| H8 Findings without a usable test record | PARTIAL, 16 findings | **PARTIAL, and one worse in a way that matters** | The 16 are unchanged (all `b`-suffix or pre-convention, none cited in this rubric). **F324 is a seventeenth of a different kind**: not a missing record but a *declared* record that does not exist — the fifth instance of the F298–F303 defect, and the first the Amendment-1 guard catches  *(2026-08-18: F325 lands with its record `F325-x1-branch` armed and two verified controls, and F298/F299/F303 are partially superseded under **S22** — noted here so this row's citations carry their replacement.)* |
| H7 Module coverage | PARTIAL, 51/203 = 25.1 % | **PARTIAL, 51/218 = 23.4 %** | **Third consecutive fall, and the driven count has been literally 51 for three reports** while the denominator went 189 → 203 → 218. Every module added in eleven days is test-only, standalone or unreferenced |
| H2 Falsifiability (instrument half) | PARTIAL, 13 of 61 gate assertions with a control | **PARTIAL, 30 of 78** | Counted as a regression only in one narrow sense, and it is the interesting one: controls went 29 → 76 and every new finding declares them, but `gate_assertion_no_control` is **48 — exactly its committed ceiling**, unmoved since 2026-08-08. The growth was absorbed by new records; **the retrofit backlog of 48 has not fallen by one** |
| K9 $\Lambda$ magnitude | OPEN, "two unreconciled pictures, untouched since 2026-08-02" | **OPEN, with a different and better-posed contradiction** | Not a grade change, and not progress either. The F192-vs-F193 framing is **dead** (F311 C, 2026-08-11 — the two are consecutive, twelve and three-quarter hours apart). What replaces it is F311's accounting argument against F319 U8's mechanism argument, five days apart, neither citing the other, with `open-derivations` carrying only one side. **ADJUDICATED by Amendment 4, 2026-08-18 - 17:15:** F311 C3 withdrawn, F319 §6 narrowed, the residual restated as *enforcement of the F183/F190 ceiling*. Still **OPEN**, and the disagreement is gone |

**Content regression with no grade change, carried a third time: H2's register half.** `falsifier_unset`
was 226/226 cards at the previous report; the ledger records it falling to 225 when CL087 was
narrowed. `unreviewed-seed` stands at **223 of 280 cards**, the same 223 as the previous report while
the card count went 264 → 280 — sixteen new cards, none of them reviewed.

**Carried forward with nothing recorded: $d_1$** (second report), and **Q4**, the $36.6\sigma$
$m_n - m_p$ exclusion (second report).

### Resolved since 2026-08-07 — and this half is substantial

- **Gap #5 closed in full, on 2026-08-11, by F311** — and the previous report never recorded it.
  (a) B9's $\Delta\alpha(M_Z)$: proved untouched by S12-F277 by *reinstating* the removed refold
  (Pi4 bit-identical, Pi3 $\times 6880$), and the residual identified as the two-loop leptonic term.
  (b) The ten `candidate` baselines: all ten re-run and diffed — **zero regressions**, five exact,
  three wall-clock only (one character class in `_VOLATILE_RE` that a leading underscore defeated),
  one float-floor churn, one undeclared input. (c) K9: adjudicated to one picture. See the
  regression table for what F319 then did to (c).
- **Row B1's colour leg reduced six-to-one (F317, 21/21, six controls).** Of the six things "colour
  is put in" bundles, four are **derived** — unitarity (the commutant is $M_3$, dim 9), specialness
  (F27's chirality removes the $U(1)$ trace), locality⇒connection, and the vector-like coupling —
  and the group is pinned given **one** input. F91's last unforced assignment (the BCC gluon even
  law) closes with it. F317 is explicit that this is a reduction, not a derivation of $SU(3)$.
- **A1's self-flagged conditionality removed (F318, 11/11, four controls).** F291 §3's *"conditional
  on $s=2$"* does not bite: the model's actual $s=36$ quark cell does not relax the Clifford bound,
  because what S1 needs is the anticommuting rank of the **hop's own span**, which is 3 at every
  factor the model adds. The cell **permits** the internal index at zero cost and **forces its
  shape**; it does not force its existence.
- **A6's non-contextuality half closed by a theorem rather than by cases (F312).** The current
  algebra's off-site commutator is literally `0.0` for both $SU(2)_L$ and $SU(3)_c$, so the whole
  non-Abelian structure is intra-site; a Schur reduction makes the internal index drop out of the
  frame condition **for any compact group**. F304's residual 3 is discharged; one lemma remains.
- **K3 reduced and re-homed (F310, 16/16).** The model claims no 3D dual and needs none — the $t=0$
  state of a rigid automaton *is* a measure on 3D field configurations. Running F285's Poisson
  bridge through it gives $n_s = 3 - 2y$ and $\gamma \equiv y - 1$ identically, so $\gamma$ **is**
  the anomalous part of the model's own block-spin eigenvalue. The operator F295 §7 left external is
  now internal, and the row moves `OPEN → PARTIAL`.
- **F313's polynomial→Laurent transfer closed (F316)**, which was the honest residual the F313 review
  named after its packaging was retracted.
- **B10 leaves the X1 fork (F324, 14/14 in an isolated harness, eight controls).** The empirical
  $\Lambda$-scale selector is retired; $N_c = 3$ follows from F298's structural $\{2,3\}$ intersected
  with the $\mathbb Z_2$ doublet parity. Physics-verified, tree-unverified — see item 1.

---

## Full rubric

### A — Foundations

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| A1 | Spacetime dimensionality | PARTIAL | F291, F292, F313, F316, F318 | the three Cayley generators; infinite volume; $d_\text{time}$ verified at $s=2$ only | Two independent selectors each return $\{3\}$ ($\ker J = 0 \Rightarrow d \le 3$; $\operatorname{coker} J = 0 \Rightarrow d \ge 3$), $d=6$/$d=9$ excluded, reducible $d=3n$ freezes. **Two changes since the previous report, neither of them a grade move.** F318 removes F291 §3's self-flagged *"conditional on $s=2$"*: the model's own $s=36$ quark cell does not relax the Clifford bound, because the rank that matters is the hop's span. And the "+1" is now computed rather than adopted (F313, $d_\text{time}=1$ from the update's commutant, independently re-derived blind by a Newton-polytope descent that also proved $A$ **primitive**), with F316 closing its polynomial→Laurent transfer — **but F313's boxed $(\dim\mathfrak{su}(s), \operatorname{rank}\mathfrak{su}(s))$ identity and its "$d_\text{space}=3$ from the commutant" are both WITHDRAWN** by its own 2026-08-13 remediation, the first as numerology, the second as circular. The commutant proves *no extra* translations, not *three* |
| A2 | Lorentz invariance | PARTIAL | F26, F28, F30, F246, F129, F301 | deformed shell exact but **not universal**; the chiral coefficient has no bound against it | The whole finite-$a$ Poincaré defect is $D_i = \partial_i\Phi$ with $\Phi = (\Omega^2 - c_\text{lat}^2 k^2)/2c_\text{lat}^2$, chirality-odd, surviving $K \to K + f(k)$. Exact to all orders on $\langle100\rangle$ ($3.5\times10^{-46}$); $O(\lvert k\rvert^3)$ for the even photon. F301's record is armed (Amendment 1) and remains the tree's one gate record with **no parameter control**. `open-derivations` **L8**: F28's GRB bound is structurally inapplicable to this operator and no confrontation has been attempted |
| A3 | Causality / locality / finite speed | EXACT | F26, F204, F227, F290 | 0 | $c_\text{lat} = 1/\sqrt3$; strict cone $C(r,t) = 0$ for $r > 4t$, measured **tight** at 1 site/layer (bound 7.39 vs measured $6.9\times10^{-16}$) where a generic Lieb–Robinson system has an exponential tail |
| A4 | CPT, and C, P, T separately | PARTIAL | F53, F321 | no CPT theorem for the QCA; T is thin | C, P, CP built per species and exact; $J(1)=0$ is one-generation arithmetic. **Unmoved for four reports.** One adjacent gain worth recording without crediting it to this row: F321 establishes reality of the Euclidean action from closure of the loop set under reversal, which is a T-adjacent structural statement — but it is about $\theta_\text{QCD}$ (row B11), not about a CPT theorem, and this row should not repeat B11's mistake of borrowing a number from a different object |
| A5 | Unitarity | EXACT | F276, F264, F300 | 0 | Every step is a length-preserving rotation by construction; F300 adds fine-grained von Neumann entropy conserved to $1.1\times10^{-12}$ on a **mixed** state |
| A6 | Superposition + Born rule | PARTIAL | F304, **F312**, F281, F290, F227 | **one lemma**: Cooke–Keane–Moran regularity | Gleason is **proved here**, not cited (F304 §5): $b_k = (-1)^k/\binom{k+d-2}{k}$, surviving iff $1 + (d-1)b_k = 0$. **The residual this row carried has halved and the previous report did not have F312.** F304's residual 3 — non-contextuality shown for the $U(1)$ wrap generator only, with the $SU(2)_L$/$SU(3)_c$ commutators "not written out" — is closed by a theorem rather than by two more cases: the off-site commutator is literally `0.0` for both groups, so the non-Abelian structure is entirely intra-site, and a Schur reduction ($C_2 = (N^2-1)/2N$, a multiple of $\mathbb 1$) drops the internal index out of the frame condition **for any compact group**. $\dim = d_p N$, so $SU(3)_c$ clears $d \ge 3$ alone. Stays `PARTIAL` on the one remaining external lemma |
| A7 | Entanglement, Bell/Tsirelson | EXACT | F212, F226, F214, F217 | $1.8\times10^{-15}$ | Saturates Tsirelson $S = 2\sqrt2$ exactly ⇒ Bell-indistinguishable from QM (CN1, settled null) |
| A8 | Measurement problem / classical limit | EXACT | F281, F130, F41 | Born legs live at A6 | Pointer basis **forced** by minimal coupling ($[H_\text{int},\hat n]$ literal `0.0`; $\{\hat n(x)\}$ maximal abelian ⇒ unique); spin correctly **not** einselected; classicality a block-spin attractor, irrelevant at $b^{-2}$ per dimension. Arguable at EXACT — M3 is proved on the free flow, not the interacting theory |
| A9 | Spin-statistics | PARTIAL | F289, F291, F292, F217 | topological step external | Both premises derived here ($d=3$; $R(2\pi) = -\mathbb 1$ to $1.7\times10^{-16}$ over 60 axes). **Not** a new proof: $\pi_1 = S_n$ and the belt-trick homotopy stay external, and CL255 is `tier: supporting` for that reason. Unmoved |
| A10 | Cluster decomposition / no-signalling | PARTIAL | F290, F227 | clustering is 1-D free-fermion | No-signalling exact ($7.8\times10^{-16}$), strict cone genuinely CA-specific. F290's own residual 1 states the interacting 3-D claim "has *not* been made", which is the harder half of the row. Unmoved |
| A11 | UV completeness | QUANT | F116, F164, F264, F284, F319 | **one number**: $\rho_\text{vac}$, $10^{120.76}$ | The Wilsonian dictionary the tree never wrote: on a physical cutoff a counterterm is the *finite* bare→measured map, so F264's power-counting theorem reads "finitely many operator coefficients carry the cutoff" — stronger, entirely finite. Licence measured (scheme constant IR-independent to $2.0\times10^{-12}$; $\ln$ coefficient $1/16\pi^2$ universal across four schemes). Leading irrelevant operator dimension-6 with the exact rational $-[(1-\sum\hat n_i^4)/144 + (\hat n_x\hat n_y\hat n_z)^2/24]$ ($1.1\times10^{-20}$, 60 dps), and **no dimension-5 photon operator** ($p=2$). Exactly two cutoff-carrying coefficients with no free parameter, one right ($G$) and one wrong by 120.8 orders. **U8's cost was a live tension with F311; adjudicated by Amendment 4, 2026-08-18 - 17:15 — F311 C3 withdrawn, and §6's "channel (ii) is the sole survivor" narrowed, because it never enumerated F193 §B/F196. A11's residual is unchanged: one number, and the mechanism that would close it now has a candidate of the right shape and no dynamics — see K9** |
| A12 | Continuum limit | MACHINE | F129–F135, D1 | $\lVert[R_b,\text{evo}]\rVert \le 1.8\times10^{-15}$ | $c_\text{lat}$ an exact RG fixed point; simple-cubic code retained as the declared regression target |

### B — Gauge structure

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| B1 | Origin of $SU(3)\times SU(2)_L\times U(1)_Y$ | PARTIAL | F27, F51, F43, F291, **F317**, **F318**, F324 | **one input**: that the internal index exists | **Reduced six-to-one, and the previous report had none of this.** "Colour is put in" bundled six impositions; F317 derives four — unitarity (commutant computed $= M_3$, dim 9 ⇒ $U(3)$), specialness (F27's chirality removes the $U(1)$ trace, since $[SU(2)_L]^2 U(1)_\text{trace} = N_c b/2 \ne 0$ on the model's own nullspace while $Y$ gives $\equiv 0$), locality⇒connection (on-site commutes with site-dependent $V(x)$ at $7\times10^{-16}$ while the hop fails at 1.343), and vector-likeness (all 27 $\mathfrak{su}(2)$ anomaly coefficients exactly 0 against $A^{888} = -1/\sqrt3$) — and pins the group given one empirical input. F318 then shows the cell **permits** the index at zero cost and **forces its shape**, but does not force its existence. **This is a reduction, not a derivation**, and F317 §8 states the prior art leg by leg. $SU(2)_L$ from $\beta$-gauging and $U(1)_Y$ from bipartite sublattice parity are unchanged |
| B2 | Chirality | EXACT | F27, F91, F292 | Ward identity $1.1\times10^{-17}$ | $W^\pm$ chiral is *forced* — right-branch weight $\equiv 0$ over ℚ. F292's independent route: traceless $\Gamma = \gamma_1\cdots\gamma_D$ needs **odd** $d$, by explicit Clifford recursion $D = 2..8$. F317 §5 and F324 §2.3 both make F27's chirality load-bearing for the *colour* sector as well |
| B3 | Anomaly cancellation | EXACT | F38, F293, F324 | the Witten check is physics-verified, tree-unverified | All six traces (gauge + gravitational) exactly zero; F293 re-verifies the six-constraint system symbolically in $N_c$ over ℚ. **The residual "Witten $SU(2)$ still not checked", carried for four reports, is discharged as a by-product**: F324 W2 evaluates the mod-2 index on the model's own content, $D = n_\text{gen}(N_c{+}1) = 12$ at $N_c = 3$, hence $\mathbb Z_2$ invariant 0 — and W2b confirms the constraint excludes a non-empty set, so it is a statement rather than a property of every content. **Caveat, and it is why this note is longer than the grade motion**: F324 has no armed record, so the check is measured in an isolated harness and not in the tree |
| B4 | Hypercharge / charge quantisation | EXACT | F165 (S13 → F279), F279, F47, F51, F38 | one charge unit, $+ N_c = 3$ for the thirds | Rank 6, dim 1 over ℚ; closing constraint is the F47 Majorana step. Core claim 10. Lepton hypercharges are registry constants with provenance, `Y_E_R` resolving from `Y_LEPTON_L`, guarded by a gate check that re-solves the system; quark hypercharges deliberately unregistered because their fractions carry $N_c = 3$ — which F324 now supplies, conditionally on six premises |
| B5 | EWSB mechanism | EXACT | F27, F34b, F44 | 0 | Higgs-free Stueckelberg; $U(x)$ pure gauge; $m_A = 0$ from a rank-deficient mass matrix. Founding decision #3 |
| B6 | Weinberg angle, with scale | QUANT | F138, F49, F231, F141 | $+0.222\%$ at $M_Z$; $-0.064\%$ on shell; **0 free params** | $\tfrac14$ is the matching value at $\mu_\star = 4\pi v = 3094.09$ GeV, forced by $Y$ having no lattice kinetic term; $\tfrac29$ is its on-shell face via F231's $8/9$ bridge. F322 adds the sensitivity nobody had measured: on the model's *own* leptonic-only $\alpha(M_Z)$ the residual doubles to $+0.450\%$ (factor 2.02), so half this row's precision is owed to the hadronic piece it does not derive |
| B7 | Confinement | PARTIAL | F70, F86, F88, F299, **F323**, F265; F94 **partially superseded** (S21 → F323, F265) | 3+1D is constructed, not proven | Exact in 2D (area law, $\sigma = -\ln w(\beta) > 0$ for all $\beta$). The $d=4$ leg now runs on the model's own lattice as $\mathrm{BCC}_3 \times \mathbb Z$ (10 plaquettes per site: 6 rhombi + 4 mixed rectangles), staple identity $2.3\times10^{-16}$, gauge invariance $3.8\times10^{-17}$, with the anisotropy **derived** rather than conventional: $\beta_t/\beta_s = 4/(3c_\text{lat}^2) = 4$ and $\xi = 1/c_\text{lat} = \sqrt3$, i.e. $(4/3)\xi^2$ where the hypercubic relation is $\xi^2$. **The residual is unmoved and unmovable by sampling**: a proof needs a transfer matrix with positivity, and `reflection positiv` / `Osterwalder` / `Schrader` / `cluster expansion` return zero hits everywhere this sweep could look. Record `gauge-bcc-mc-d4` 28/28, 5/5 controls |
| B8 | Asymptotic freedom / $\alpha_s$ running | PARTIAL | F144, F151, F239, F235, F287, F280, F299, F303 | **the X1 normalisation fork**, then $d_1$ leg 3 | $b_0 = \tfrac{11}{3}C_A = 11$ exact and numerically recovered. $d_1$ has a subtracted formulation with 36.2 % of $\Delta C$ open, bracketed. The residual is still not only a value: $\alpha_s(M_Z) = 0.11858$ ($+0.5\%$) on the centre branch against $0.03970$ ($-66.4\%$) on Casimir, and the register's $0.11955$ / $+1.7\%$ / $2.1\sigma$ is a branch-B number stated without its branch. **Nothing recorded since 2026-08-11.** See gap #2  **AMENDED 2026-08-18 (F325, S22): the X1 fork is RESOLVED** — branch A tested and closed, branch B ($g_s=\tfrac12$) adopted, on two legs neither of which needs $d_1$. So the blocker is now $d_1$ leg 3 **alone**, and $\alpha_s(M_Z)=0.1186$ (+0.5 %) stops being contingent. F299/F303 are partially superseded by F325 here |
| B9 | Running of $\alpha$, EW couplings | QUANT | F322, F311, F251 ⚠ (S12 → F277), F261, F138, F231, F115 (S20 → F138, F231) | **two published numbers** (below) — **reconciled by Amendment 2, 2026-08-18 - 16:20: $0.0495\%$ model-internal, $0.00158\%$ after importing the Källén–Sabry constant; the row stays `QUANT`**; then row G3 | The model-internal number is F322's: F261's sympy-exact $b_1 = 1$, never previously fed into the running, contributes $\alpha^2 L_\ell/(4\pi^2)$ per lepton and closes $79.8\%$ of the shortfall with the correct sign — $0.2447\% \to \mathbf{0.0495\%}$, residual $1.559\times10^{-5}$ (two-loop non-log constant plus three loops). **F311 independently closed the same residual to $0.00158\%$ six days earlier** using the standard Källén–Sabry two-loop form, which F311 is explicit is *cited, not derived here*. F322 does not cite F311. Both numbers are live in different documents — see gap #4. The supersession worry is settled either way: `leptonic_running`'s call closure never touched the refolded path (bitwise identical under a kernel perturbation), and what F277 supplied was the *warrant* — the lattice bound on $\Delta\alpha$ was $183$–$190\times$ the claimed agreement with the refold present and is $0.088\times$ it and falling without |
| B10 | Why 3 colours | PARTIAL | F293, F294, F298, F299, F303, **F324**, F279, F144, F110 | **six premises**, none of them a measured number; premise (iii) has no control | **Row rewritten, and it is not a promotion — F324 §10 says so in its own words.** The empirical $\Lambda$-scale selector is retired and **B10 stops being a dependent of X1**: $N_c = 3$ is the intersection of F298's structural support $\{2,3\}$ (the C7 identity is well-defined only for $N_c \le 3$, over ℚ, consuming no measured number) with the $\mathbb Z_2$ doublet parity of the model's own derived $SU(2)_L$, $D = n_\text{gen}(N_c{+}1)$ odd. The parity is **prior art** (Bär & Wiese 2001, stated as such) and arrives locally as well under a $U(2)$ embedding. The incremental content over F298 is **one bit**, and its sign is a function of the assumed content (adjoint quarks return $\{2\}$). The debt is **transferred, not discharged**: from a hadron-spectroscopy fact to F75's generation parity (row C1) plus premises (iii)–(vi), and the premise count went *up*. Live exposure, named by F324 and not by F298: the sextet gives $\chi = 3/10$ against the tower's $3/4$, so the support $\{2,3\}$ is a property of the k-string **truncation**, not yet of the model  **AMENDED 2026-08-18 (F325, S22).** F324's **upper** constraint is F298's C7 support, and F325 shows that support is a property of the **mixed** matching — so it is withdrawn (CN19) and the bracket closes on **odd $N_c$** only, $\{3,5,7,\dots\}$. The $\mathbb Z_2$ doublet-parity leg is untouched. B10 does stop being an X1 dependent, but by X1 closing rather than by the selector retiring, and it does **not** close on $\{3\}$ |
| B11 | Strong CP / $\theta_\text{QCD}$ | QUANT | F321, F53, F305, F307, F91 | $\arg\det M_q$ at three generations (E6/E7); the action fork; non-perturbative $\theta$-sectors | In Euclidean signature the $\theta$-term is the **unique purely imaginary** gauge invariant, so reality of the action **is** $\theta = 0$ — and reality is a property of the rule's loop set, not of an inserted `Re()`. The 20 oriented minimal rhombi are closed under reversal (exact), giving $\operatorname{Im}S = 1.2\times10^{-14}$ at 99.7 % disorder, $S$ invariant under $U \to U^*$ with the one-sense functional odd at literal `0.0`; every vertex coefficient real at literal `0.0` at 2, 3 and 4 legs with colour indices sampled, and that class is closed under products and $q \to -q$ integration, so $\Gamma$ is real at every order. Sensitivity measured, not assumed. **Not a solution of the strong CP problem** — CL279 is a deliberate non-claim |
| B12 | Gauge-boson masses, $\rho$, $m_Z/m_W$ | QUANT | F49, F141, F138, F231, F320 | **$v$ and $\alpha$** (two anchors); F141's hypothesis (U) | The SM's electroweak sector takes three inputs $\{\alpha, G_F, m_Z\}$; this model takes **two**, because $\sin^2\theta_W^\text{os} = \tfrac29$ arrives from lattice geometry. Eliminating F141's stiffness quantum against $e = g\sin\theta_W$ **determines** it, $u = 18\pi\alpha/7$, giving $g^2 = 18\pi\alpha$ exactly and $m_W = \tfrac{3v}{2}\sqrt{2\pi\alpha}$, $m_Z = \tfrac{9v}{2}\sqrt{2\pi\alpha/7}$. Residual stated **free of $\Delta r$** (cancels to $2.2\times10^{-16}$ over $\Delta r \in [0,0.1]$): $+0.222\%$ on $m_W$, $+0.158\%$ on $m_Z$; absolutes bracketed $[80.147, 80.548]$ and $[90.879, 91.332]$ GeV, both containing PDG. $\rho = 1$ exactly from the **rank** of F41's single Stueckelberg direction, not from a custodial $SU(2)$ this Higgs-free model cannot invoke. **Note for H4**: the public summary still lists this row's result under "not claimed" |

### C — Matter content

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| C1 | Exactly three generations | PARTIAL | F75, F84 | the physical identification is a stated hypothesis | Group theory is a **theorem** ($\sum d^2 = 48$ ⇒ max single-valued irrep dim 3, $T_{1u}$ unique); the identification is a **hypothesis** (F75 §7, a Candidate finding). F292 §6 found the same $n$-copies multiplicity structure and **declined the inference**. **New load this report:** F324 premise (i) makes the *parity* of the generation count load-bearing for B10, so this row now carries colour as well as flavour. F324 records that the stronger per-generation form (Bär & Wiese) would remove the dependence at the cost of assuming each generation is independently consistent |
| C2 | First-generation multiplet | EXACT | F38, F41, F42, F51, F165 (S13 → F279), F279 | 0 | Complete and anomaly-free. F165's attribution is superseded by F279; its conclusion is retained in full |
| C3 | Colour triplet + fractional charge | PARTIAL | F136, F165 (S13 → F279), F279, F324 | conditional on $N_c = 3$, now via F324's six premises | Fractional charge is forced by the $3y_Q + y_L = 0$ row, i.e. by $N_c = 3$; commensurability holds for any $N_c$ (ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$). **The conditionality changes character rather than lifting**: it no longer inherits X1's unchosen branch, and instead inherits F324's premise set — which includes C1's generation parity |
| C4 | Neutrino nature (Dirac vs Majorana) | PARTIAL | F47, F266 | — | The Higgs-free Majorana step is constructed and $\nu_R$ is a structurally-forced total singlet ($Y = 0$, the row that closes the hypercharge system). Nothing **forces** Majorana over Dirac. Unmoved |
| C5 | Neutrino mass mechanism | PARTIAL | F47, F236, F254 | $M_R$ free | See-saw plus $E_g/\mathbb Z_3$ texture fix the three light masses and the hierarchy at machine precision; absolute scale unfixed. Unmoved |
| C6 | Antimatter / charge conjugation | EXACT | F53, F260 | 0 | Per-species $C$; positron and crossing sector built |
| C7 | Beyond-SM content | PARTIAL | F223, F228, F266, F216, F204, F237 | geon abundance free; **no $B$-violating rate anywhere** | Predicts a Planck-mass BH-remnant geon, cold and collisionless, $M_\text{rem} = (\sqrt3/2)^{1/2}M_\text{Pl}$ exact. Excludes its own alternatives: native massive spin-2 (CN5), $\nu_R\nu_R$ J=2 (CN6), Alcubierre warp, keV sterile as 100 % DM. The "proton decay" sub-row is **carried from the previous report and not re-measured** — the whole-tree grep needs the workspace |

### D — The parameter ledger

| # | Parameter | Grade | Evidence | Note |
|---|---|---|---|---|
| 1–6 | $m_u, m_d, m_s, m_c, m_b, m_t$ | ABSENT ×6 | F121 | Quark masses are "the measured values converted to kg — a **consistency** readout". The constituent scale $m_c = 309.5$ MeV from one $f_\pi$ anchor is a different quantity. `open-derivations` **E6**; no route proposed |
| 7–8 | $m_e/m_\tau$, $m_\mu/m_\tau$ (shape) | QUANT ×2 | F175, F234, F120 | $\le 0.007\%$ with **zero shape parameters**, from $\{\delta^* = \tfrac29,\ \eta^2 = \tfrac12\}$; Koide $Q = \tfrac23$ at $0.91\sigma$ |
| 9 | Charged-lepton overall scale | FIT (N=1) | F121, F233 | $\tau$-anchored. F233 reduces the gap to a factor 1.9 zero-parameter **through the $\alpha_s$ transmutation channel**, so it inherits gap #2's fork |
| 10–13 | CKM 3 angles + 1 phase | ABSENT ×4 | — | Declared out of scope. $J(1) = 0$ is one-generation arithmetic, not a prediction. "Out of scope" is a choice, not a result |
| 14 | $\alpha_\text{em}$ | OPEN | F127 | Four-avenue no-go on deriving it from the rule. Now carries two absolute boson masses downstream (B12) as well as the charge unit (B4) |
| 15 | $g_2$ / $\sin^2\theta_W$ | QUANT | F138, F49, F231 | Derived with its scale, $+0.222\%$, 0 parameters |
| 16 | $g_3$ / $\alpha_s$ | PARTIAL | F144, F239, F287, F280, F303 | **First the X1 fork, then $d_1$ leg 3** (36.2 % of $\Delta C$, bracketed). Route narrowed; value unmoved; branch unchosen; nothing recorded in eleven days  **AMENDED 2026-08-18 (F325, S22): the X1 fork is closed** — branch B adopted, branch chosen, value $\alpha_s(M_Z)=0.1186$; $d_1$ leg 3 is the only remaining blocker |
| 17 | $v$ | FIT (N=1) | F119, Scope | "The electroweak scale $v$ is an anchor, not an output." Now carries $m_W$ and $m_Z$ absolutely |
| 18 | $m_H$ | OPEN | F73 | Kinematics exact, but free-sum kinematics cannot reproduce 125.25 GeV; the missing input is binding dynamics. Higgs-free by decision makes this a bound-state mass — harder, not excused |
| 19 | $\theta_\text{QCD}$ | PARTIAL | F321, F53 | **Row corrected.** It read "tree-level pure gauge; loops open" citing F53 for three reports, and F53's number is the F27 complex-mass phase, not this. Under F321 the parameter stops being an *independent* input and becomes a function of the quark mass texture: $\bar\theta = \theta + \arg\det M_q$, first term zero at every order, second term rows 1–6 |
| 20–21 | 2 light-$\nu$ mass ratios | MACHINE ×2 | F236 | The $E_g/\mathbb Z_3$ texture fixes masses and hierarchy at machine precision |
| 22 | $\nu$ absolute scale ($M_R$) | OPEN | F47, Scope | Nothing in the model fixes $M_R$ |
| 23–25 | 3 PMNS angles | EXCLUDED ×3 | F254 | Proven **no lattice selector**: the three $T_{2g}$ amplitudes are three inequivalent 1-d irreps under the $E_g$-stabiliser $D_{2h}$. Permanently free — a result |
| 26 | $\nu$ Dirac CP phase | ABSENT | — | Not addressed. `open-derivations` **D4** notes it plausibly *inherits* F254's no-go, which would move it `ABSENT → EXCLUDED`; confirming that formally is one session and nobody has spent it |
| 27 | $G$ | EXACT | F79, F107 | $G = a^2c^3/(8\pi\sqrt3\,\hbar)$ structural; $3\times10^{-8}$ vs CODATA; 0 free parameters. Inherits F75's hypothesis status per claim 4 |
| 28 | $\Lambda$ | OPEN | F164, F192, F193, F196, F241, F311, F319 | See K9. The "two pictures" framing died on 2026-08-11; what replaced it is a priced mechanism requirement — and since Amendment 4 the price is **met to $0.10$ dex by the F183/F190 ceiling** (F193 §B/F196), with the *dynamics* of that ceiling, not its selectivity, the open item |

**Ledger tally — unchanged for the fourth report.** Derived with zero free parameters: **6** (2 lepton
ratios, $\sin^2\theta_W$, 2 $\nu$ mass ratios, $G$). Partial, one named residual each: **2**
($\alpha_s$, $\theta_\text{QCD}$). Fitted or free input: **6** (lepton scale, $v$, $\alpha$, 3 PMNS).
Open or absent: **14**.

**How to read that against the SM's 19.** Not "6 beats 19". The model **derives 6 quantities the SM
takes as free**, **proves 3 more permanently free** (PMNS — itself a result), and **does not yet
address 14**, of which 11 are quark masses and CKM. The qualifier the previous report added still
holds and has not improved: of the 6 derived, one ($\sin^2\theta_W$) and both partials sit
downstream of either the $v$ anchor or the unchosen X1 branch, so "zero free parameters in the
sectors we built" is true of the *count* and not of the *chain*. One thing this report adds: F320's
absolute $m_W$ and $m_Z$ are **not** new ledger entries, and describing them as reducing the
parameter count would be the drift this section exists to prevent.

### E — Gravity and general relativity

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| E1 | Fundamental field equation | POSIT | F178, F297 | — | DECISION 2026-06-29: induced Einstein equation $G_{\mu\nu} = (8\pi G/c^4)T_{\mu\nu}$. Alternatives genuinely closed; **independently confirmed since** on an unrelated observable (F297: the demoted energy-only law gives $Y_p = 0.1856$, $-17.6\sigma$) |
| E2 | Equivalence principle | MACHINE | F64, F62 (S3 → F64) | — | F62 is partially superseded; its lapse-mix sign convention is still production code |
| E3 | PPN $\beta,\gamma$ | EXACT | F64 | $\beta = \gamma = 1$ exactly | GR-identical. The naive linear dielectric ($\beta = \tfrac12$, 50.1″/cy) is excluded |
| E4 | Classical tests | QUANT | F64, F107, F111 | $3\times10^{-8}$ | Mercury 42.98″/cy, solar-limb 1.7512″, Shapiro, redshift |
| E5 | Newton's constant | EXACT | F79, F107 | $3\times10^{-8}$ vs CODATA | Structural, not Sakharov-premised. Fixes $a/\ell_P = \sqrt{8\pi}\,3^{1/4} = 6.5978$. **F319 U8 makes this row load-bearing for K9**: the same mode sum that gives $G$ is the one whose deletion would fix $\Lambda$. Amendment 4 sharpens the dependence in the model's favour: the surviving route (F196's capacity ceiling) *uses* this row's $G$ rather than perturbing it, so E5 is a **premise** of the K9 candidate, not a casualty of it |
| E6 | GW speed, polarisations, dof | EXACT | F180, F248, F216 | GW170817 residual $\le 3\times10^{-83}$ | $c_\text{grav} = c_\gamma$ is a **genuine zero**, inherited through F79 zero-tree-stiffness. Explicit TT graviton, 2 helicity-$\pm2$ modes, proven massless |
| E7 | Inspiral / ringdown QNM | QUANT | F189, F187 | $< 7\%$ (WKB) | GW150914 chirp mass 28.1 $M_\odot$, ISCO 67.6 Hz |
| E8 | Black holes | QUANT | F183, F186 | shadow $3\sqrt3 M$ | Exact Schwarzschild/Kerr with horizon. The $+4.63\%$ shadow, echoes and absent Hawking spectrum are withdrawn (cards CL023–CL027) |
| E9 | BH thermodynamics | PARTIAL | F190, F183, F300 §5 | one posited constant; the target is now an entanglement entropy | $S = A/4$ reproduced **iff** each cell carries $2\pi\sqrt3$ nats. F300 §5 proves F190's own next step impossible as written ($e^{2\pi\sqrt3} = 53252.295$ is $0.295$ from an integer; $2\pi\sqrt3/\ln2 = 15.7006$ is $0.299$ from one), so the cell entropy is not a state count of anything; the *necessary* capacity condition passes at $6.11\times$. The grade does not move, and the finding says so |
| E10 | Singularity resolution | PARTIAL | F183 §L1, F284 §5 | $r_\text{core}$ is a saturation estimate | Kretschmann saturates at the cell scale ⇒ $r_\text{core} \propto M^{1/3}$, $\sim5\times10^{-22}$ m at $1 M_\odot$, gate-tested. Cosmologically no substrate singularity, first resolvable epoch $H_\text{max} = 3^{-3/4}M_\text{Pl}$ at $t_\text{min} = \sqrt3$ ticks. No geodesic-completeness result |
| E11 | Interior / TOV / NS EoS | QUANT | F181, F184, F185 | — | SLy $M_\text{max} = 2.08 M_\odot$, $R(1.4) = 11.1$ km, consistent with PSR J0740 + NICER; $I/MR^2 \approx 0.31$ |
| E12 | Quantum-gravity sector | PARTIAL | F216, F248, F79 | — | Graviton exactly massless, 2 dof, UV transversality $\Pi \propto Q^2$ plus IR block-spin irrelevance. Gravity's own UV completion beyond "the lattice is the cutoff" is not developed; A11's ledger now says exactly which coefficient that costs |
| E13 | Galactic-scale consistency | EXCLUDED | F194, F191 | — | The model-native emergent-gravity route is **falsified** by the Bullet-Cluster lensing/gas offset. A dark *source* is required — a result, and a self-inflicted one |

### K — Cosmology

*Row IDs are `K`, not `F`.*

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| K1 | FRW background | QUANT | F182, F188, F284 | measured $\Omega$'s in | Full-tensor source reproduces ΛCDM: $z_\text{eq} \approx 3430$, $z_\text{acc} \approx 0.63$, age $\approx 13.8$ Gyr. F284 re-reads expansion as $K$'s conformal mode on a **rigid** substrate and buys $\dot G/G \equiv 0$ exactly. Solved *with* the model's source, not derived *from* the lattice |
| K2 | BBN / light elements | PARTIAL | F297, F309, F79, F178, F182, F284 | $\eta_b$ free; network offset $-0.87\%$; $^7$Li not validated; $V_{ud}$, $G_F$ external | Expansion side entirely model-native, $N_\text{eff} = 3.044$ *forced*. $Y_p = 0.2449$ ($-0.11\sigma$), D/H $= 2.47\times10^{-5}$ ($-1.8\sigma$). The $g_*(T)$ import is **closed** by F309 from the model's own 48 Weyl fields (exactly branch-balanced, 24 L / 24 R), which also produced a constraint the sector did not have: $m_{E_g} > 125.5$ MeV. Above the top threshold the model's $g_*$ is 105.75 or 107.75 and the SM's 106.75 is **unavailable** to it — recorded, deliberately not published as a falsifier |
| K3 | CMB peaks, $n_s$ | **PARTIAL** (was OPEN) | F310, F295, F296, F285, F286 | **the value of one non-integer block-spin eigenvalue** | **Moved by F310 (2026-08-11, 16/16, record armed with a control), which the previous report never recorded.** The in-repo question it named closed negative in the useful direction: the model claims no 3D dual and **needs none**, because the $t=0$ state of a rigid automaton *is* a measure on 3D field configurations, so F296 L5's $r$ exclusion is a dictionary artifact and does not transfer. Running F285's Poisson bridge through it gives $n_s = 3 - 2y$ and hence $\gamma \equiv y - 1$ **identically** (sympy literal zero) — so $\gamma$ **is** the anomalous part of the model's own block-spin relevant eigenvalue, $\lambda = b^{1+\gamma}$. That is the operator identification F295 §7 left open, now internal, and it explains every prior failure in one line: an anomalous dimension is a non-integer RG exponent and all five exponents F130 measured are integers. A full CMB fit remains out of scope. **Caveat**: F295 and F296 are two of the five cannot-fail cosmology gate records |
| K4 | Inflation or substitute | EXCLUDED | F282, F283, F296, F238 | cause named + 4 falsifiers | No slow-roll direction exists: $a/\ell_\text{red} = 3^{1/4}$ exactly ⇒ sub-Planckian cutoff; every compact CA direction carries $M_\text{Pl}^2/f^2 \ge \sqrt3$. F283 proved the obstruction exactly invariant under $a \to sa$ |
| K5 | Primordial spectrum normalisation | EXCLUDED | F282, F284, F285, F238 | $A_s$ free, cause named | With no inflaton and a rigid substrate offering no generating process, $P(k)$ is an automaton **initial condition**. $A_s = 2.1\times10^{-9}$ has no route |
| K6 | Baryogenesis | PARTIAL | F202, F47, F53 | magnitude not derived; **no $B$-violating rate** | All three Sakharov conditions met by the model's own structure. Not a Boltzmann computation; no asymmetry number. Condition 1 is *met* in the sense of being available, never rated |
| K7 | Dark-matter identity | PARTIAL | F223, F228, F266, F216, F237 | — | Candidate: graviton–graviton J=2 geon, stable as a one-cell Planck-mass BH remnant, cold and collisionless. Alternatives excluded |
| K8 | $\Omega_\text{DM}h^2 = 0.12$ | EXCLUDED | F238, F282–F285 | free input, cause named | Provable non-derivability: the structural *absence* of an inflaton is a structural *exclusion*, $\beta$ is in the initial-state category, and F285 quantifies the mirror constraint |
| K9 | $\Lambda$ magnitude | OPEN | F311, F319, F164, F192, F193, F196, F241 | **a *dynamical* enforcement of the F183/F190 capacity ceiling on the F164 sum, plus $\Omega_\Lambda$** (restated by Amendment 4; was *"an order-selective mechanism, priced at $\ge 1.27\times10^{116}$"* — the price is **met to $0.10$ dex**, the dynamics are not) | **The residual is restated, and it is a different object from the one this row carried for four reports.** The "two unreconciled pictures" framing is dead: F311 C showed F192 and F193 are *consecutive* (12.75 h apart), F192's $w=-1$ sign result **vacuous** rather than contradicted under $\rho_\text{vac} = 0$, and its $10^{121}$ a **double count** — in an induced theory the zero-point sum *is* $1/G$ and cannot also be a source. Five days later **F319 U8 priced that move and closed it**: $1/16\pi G$ and $\rho_\text{vac}$ are the two moments of one sum, so the 2×2 solve over both observables returns an 8.3 Gpc cell, and F164 channel (i) — the route F193 turned from a position into a derivation — is **excluded**. Channel (ii), sequestering through the $AB \equiv 1$ dielectric, is the sole survivor and is unevidenced. **Neither finding cites the other**, and `open-derivations` G1 carries only F311's side. Stays `OPEN`. **RESTATED by Amendment 4, 2026-08-18 - 17:15, and *not* into Part D.** F193's Part A is **uniform** — A2 deletes the $\tfrac12$-per-mode $c$-number and F59 Part C builds $1/16\pi G$ from that same $\tfrac12$ — so CL275 applies to it verbatim and it is excluded. **F311 C3 is withdrawn**: "the modes make $1/G$, so they cannot also be a source" proves too much, since $a_0$ and $a_1$ are different coefficients of one heat-kernel expansion and Sakharov induced gravity would then have no induced CC at all; this is F311's own falsifier 5, hit by F319 U8. **F319 §6 is narrowed**: it enumerates only F164's three channels and misses F193 **Part B** / F196 / F241, which is order-selective by construction — the ceiling $\rho\le3c^4/8\pi GL^2$ *contains* $G$ rather than perturbing it, and delivers $120.66$ of the required $120.76$ decades with $a_1$ untouched, short by $0.10$ dex $=\Omega_\Lambda$. **The residual is a *dynamical* enforcement of the F183/F190 capacity ceiling on the F164 sum** — two candidate routes of the right shape (channel (ii), no number; F193 §B/F196, the number to $0.10$ dex, no dynamics) — plus F241's $O(1)$ |
| K10 | Dark energy $w$, vs DESI | PARTIAL | F192, F203 | sign exact; magnitude open | Vacuum $w = -1$ gives $\rho + 3p = -2\rho$ so it accelerates — sign correct and exact. F203 flags $w = -1$ vs DESI DR2 as one of three falsifiers under pressure. **F311 C2 notes the sign statement is vacuous under $\rho_\text{vac} = 0$**, which this row should absorb once K9 settles. **Amendment 4, 2026-08-18 - 17:15: do not absorb it yet.** C2 stands as an implication but is *conditional* on a survivor that actually zeroes the gravitating constant — F193 Part A, the route that supplied $\rho_\text{vac}=0$ outright, is excluded, and the surviving ceiling route caps the gravitating density near $\rho_\text{crit}$ rather than at zero, which is a regime where $w=p/\rho$ is **not** $0/0$. K10's residual is unchanged and the row does not move |
| K11 | Structure formation / $\sigma_8$ | PARTIAL | F288 | $A_s$ free (K5); EH98 $T(k)$ imported | The EFT of dark energy carries two free functions; the model has **zero**, from three independent sources ($\mu = 1$ with $\partial_k\mu \equiv 0$; $\dot G/G \equiv 0$; zero linear slip). $\gamma_g = 6/11$ and Meszáros $D(y) = 1 + \tfrac32 y$ are sympy literal zeros; $f\sigma_8$ vs 7 RSD points gives $\chi^2/N = 1.012$. $\sigma_8 = 0.8204$ **reported with its budget, not claimed**. Falsifier can fire: no screening exists, so the DES Y6 low-$S_8$ direction ($3.00\sigma$) cannot be accommodated |
| K12 | Cosmological initial conditions | PARTIAL | F284, F285, F286, F295, F296, F238, F310 | one anomalous dimension, now internal | The state must be non-generic by $10^{-56}$ vs white noise at the pivot *and* $\sim2\times10^6$ enhanced at the PBH scale — opposite ends of the same function. F310 moves the residual's *character* the same way it moved K3's: the operator is the model's own block-spin eigenvalue, not an external candidate |

### G — Emergent and precision physics

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| G1 | Maxwell / classical EM | EXACT | F26, F87, F245, F246, F306, F314; F25 (S18 → F306, identity) | 0 | The composite-photon curl closes at $O(k^3)$ with exact coefficient $c_\text{lat}^3/48 = 1/(144\sqrt3)$; the reported $O(k)$ failure was a representation artifact. F314 gives the first real-space demonstration that the model's own photon propagates — closed-form pair group velocity matched at $7.8\times10^{-16}$ over 24 ticks on a wrap-free $128\times48\times48$ box, energy conserved to $3.7\times10^{-15}$ — and gated a new failure mode (wrap-freeness is a condition on the *carrier*) |
| G2 | Hydrogen, fine structure, Lamb | QUANT | F125, F252, F257, F262 | Lamb $= 99.5\%$ of measured | $-13.596$ eV from $m_e + \alpha$ alone; Ry to $1.1\times10^{-12}$ of CODATA; 2p split 10.95 GHz; Bethe log from the model's own spectrum with no literature constant. Residual is two-loop $\alpha(Z\alpha)^5$, declared out of scope |
| G3 | $g-2$, electron and muon | PARTIAL | F252, F261 | hadronic + EW absent by declared scope | $a_e = \alpha/2\pi$ exact; two-loop $A_2 = -0.328478965$; $A_2(\mu) = 0.765857$ vs $0.765857410$. Hadronic VP, HLbL and EW **not** claimed. **This row acquired a second dependent**: F322 shows B9's electroweak precision is a factor 2.02 worse on the model's own $\alpha$, and the missing $3.795$ in $\alpha^{-1}$ is exactly the hadronic piece that lives here |
| G4 | Atomic structure / periodic table | QUANT | F148, F195, F208 | light elements only | H/He/Li/C certified stable (net charge $\le2.2\times10^{-16}$, Pauli via live Gram–Schmidt); He IP 24.0 eV; relativistic SCF with an accuracy map |
| G5 | Hadron spectrum | QUANT | F123, F124, F235, F122, F297 | 1 anchor ($f_\pi$); $\sqrt\sigma/f_\pi$ $+12\%$; **$m_n - m_p$ excluded at $36.6\sigma$** | Nucleon $3m_c = 928.5$ vs 938.27 MeV ($-1.05\%$) on one anchor; mesons few-%. The $+12\%$ is $d_1$ and therefore gap #2's fork. The isospin splitting is `open-derivations` **Q4** and **nothing has been recorded against it in eleven days** — F122's *sign* claim survives, its value does not. The row keeps `QUANT` on the nucleon mass and the meson sector, not on the splitting |
| G6 | Nuclear binding | QUANT | F104, F113, F126, F128, F240, F206 | 1 parameter ($b = 0.55$ fm) | Deuteron $E_b$ 2.224 vs 2.22457 MeV (**0.026 %**), $r_d$ 0.4 %, on a fully derived OBE potential with no tuned hard core |
| G7 | Weak decays | PARTIAL | F54, F48, F297 | absolute rates tied to $v$; $\tau_n$ wrong by 2.7× | $d \to u + W^- \to u + e^- + \bar\nu$ end-to-end, 10/10. Structure exact; $G_F$ inherits the $v$ anchor. The free-neutron lifetime is a computed number (331 s against $878.4 \pm 0.4$) and it is wrong — the same defect as G5's, which is why Q4 closes two rows |
| G8 | Scattering / S-matrix | MACHINE | F260, F259, F263, F264, F258 (S12 → F277) | — | Tree QED S-matrix plus crossing; Bloch–Nordsieck IR cancellation; Euler–Heisenberg, light-by-light, Schwinger pair production; renormalizability with $D = 4 - \tfrac32 E_f - E_\gamma$ exact; $Z_1 = Z_2$ a computed identity, refold-corrected by F277 with $S_0$–$S_4$ unchanged |
| G9 | Condensed-matter emergents | QUANT | F210–F215, F218, F242, F207, F171 | Allen–Dynes $6.3\%$ | $2\Delta/kT_c \to 2\pi/e^\gamma$ and $\Delta C/C_n = 12/7\zeta(3)$ at machine precision; $\mu^*$ **derived** from the F64 dielectric with no fit, cutting $T_c$ error $14.3\% \to 6.3\%$. Casimir exact |
| G10 | Statistical mechanics / thermodynamics | PARTIAL | F300, F309 | equilibrium only; photon and fermion sectors, no interacting sector | $w = 1/3$ and Stefan–Boltzmann are **theorems** in the IR of the derived dispersion, with closed-form lattice corrections $\propto\Theta^2$ and the parameter-free ratio $C_u/C_w = 15/2$ — which F309 **upgraded** from a measured photon coincidence to a degree-3 homogeneity theorem by showing it survives fermions *and* the branch-odd deletion. The branch-odd term does **not** cancel for a fermion: $b$ is linear in $\lvert k\rvert$ so its square is degree-3 homogeneous, supplying $3/7 = 42.86\%$ of the coefficient. Fine-grained entropy conserved ($1.1\times10^{-12}$) on a mixed state; coarse-grained entropy rises **time-symmetrically**, so the arrow is the initial condition. The free sector **cannot** thermalise ($2N$ conserved $n_\pm(k)$ fix a GGE). **The previous report's clause "its claimed gate record does not exist" is stale** — armed 2026-08-07, with two controls |

### H — Model integrity

| # | Requirement | Grade | Evidence | Note |
|---|---|---|---|---|
| H1 | Parameter count vs the SM's 19+ | PARTIAL | ledger above | 6 derived, 3 proven-free, 14 unaddressed. **Not cheaper than the SM in raw count**; the sectors it has built carry zero free parameters, which is the claim actually made. Three of the six derived sit downstream of the $v$ anchor or of X1's unchosen branch, so the chain is not as parameter-free as the count. Unchanged |
| H2 | Falsifiability | PARTIAL | `docs/claims/`; `tests/registry/`; `audit_tests --ratchet` | **The register half is unchanged and strong**; the instrument half moved in one direction and stalled in another. Gate-tier `kind: assertion` records went 61 → **78** and declared controls 29 → **76**, all of them attached to findings written since 2026-08-08, which is real: every new finding now ships controls with measured red sets. But `gate_assertion_no_control` reads **48**, *exactly* its committed ceiling and unmoved since 2026-08-08 — the retrofit backlog has not fallen by one record, the growth was absorbed by new work. `unreviewed_seed` is **223 of 280 cards** — the same 223 as the previous report, against sixteen new cards. Whether the 76 controls still verify RED at the current fingerprint is **NOT VERIFIED THIS RUN** |
| H3 | Out-of-sample survival | QUANT | Claims rev 4 | One clean instance: $m_Z/m_W = 3/\sqrt7$ was fixed **before** PDG 2025 excluded CDF-II $m_W$; against $m_W = 80.3692 \pm 0.0133$ it gives $-0.064\%$. Still the only one. F320's absolute masses are not a second instance — they are a new prediction, not a survived revision |
| H4 | Retraction hygiene | **PARTIAL** (was QUANT) | supersessions.yaml S1–S21; `check_superseded_citations.py`; `papers/Claims-and-Falsifiers-Summary.md` rev 4 | **The inward machinery improved and the outward half regressed, and H4 asks about both.** New since the previous report: S20 (F115 entered the ledger 67 days late) and S21 (F94's hypercubic ensemble), banners stamped, and `make citations` — a genuinely new capability that propagates a supersession *outward* to the documents that cite it, at the granularity of one table row, with the B9 regression pinned as its own self-test. It caught five live violations on first run and then caught row B7 within ninety minutes of S21 being created. **What fails is H4's second clause**: `Claims-and-Falsifiers-Summary.md` is still at revision 4 (2026-08-04) and still lists *"$m_W$ and $m_Z$ in absolute terms"* under **Scope — what is not claimed**, fourteen days after F320 derived them and CL016 was withdrawn; it also still quotes $\alpha_s(M_Z)$'s $2.1\sigma$ without its branch. A derived result published as an input is exactly what this row is for. The register (cards) is correct; the public summary is not |
| H5 | Internal consistency of decisions | PARTIAL | key-decisions.md D1–D12; Part D of `open-derivations` | Decisions 1–7 mutually consistent as written. **X1 is unchanged and is still the largest item**: the confinement sector implements Casimir while the coupling normalisation its own $\alpha_s$ chain depends on requires the centre reading, with no argument for it and three candidate reconciliations closed. **Two new items this report, both of the same shape and neither with a ledger row:** (i) K9's F311-vs-F319 disagreement (see K9); (ii) B9 carries two different published residuals, $0.00158\%$ and $0.0495\%$, in two live documents, from two findings six days apart of which the later does not cite the earlier. Part D was built for exactly this shape and has one row. **DISPOSED by Amendment 2, 2026-08-18 - 16:20 — and *not* into Part D**: the two numbers are additive (one loop $+$ the model's own two-loop leading log, vs the same $+$ the imported Källén–Sabry constant, $103.2\%$ of F322's residual), so there is no disagreement to adjudicate; F322 now cites F311 in §6.1 and the quotation rule is model-internal-first. **Row stays `PARTIAL`** — X1 and item (i) are untouched. **Item (i) DISPOSED by Amendment 4, 2026-08-18 - 17:15, and also *not* into Part D**: K9's F311-vs-F319 disagreement is decidable and is decided — F311 C3 withdrawn (its own falsifier 5), F319 §6 narrowed, F193 Part A excluded — so it is an adjudication, not a fork the tree cannot choose. **Two of the row's three items are now closed; X1 is the whole of what remains, and the row stays `PARTIAL` because X1 has not moved** |
| H6 | Reproducibility | **PARTIAL** (was QUANT) | `tools/check_finding_records.py`, executed this run | **The gate is red, and this run demonstrated it.** F324's declared record `F324-ncolour-bracket` does not exist in `tests/registry/`, and the Amendment-1 guard wired into `make gate` fires on exactly that. `make indexes-check` and `make claims` fail by the same cause: F324 is in no index and CL281 is on disk but not in `claims-index.md` or `docs/claims/registry.yaml`. **None of the 81 gate records was executed this run** — the device workspace was unavailable for the whole session, as it was for the F324 session — so the barrier is both red and unmeasured. Mitigating and worth stating: F324 §11 declares all of this itself and withholds `Confirmed`; the failure is honestly-labelled debt, not a false claim. "From a clean checkout" remains untested |
| H7 | Module coverage | PARTIAL | D11 registry | **51 of 218 channel-driven (23.4 %)**, down from 25.1 % and 27.0 %. **Third consecutive fall, and the driven count has been literally 51 in all three** while the denominator went 189 → 203 → 218. 90 test-only, 46 standalone, 24 unreferenced, 25 `fork_live`, 23 `fork_unclaimed`, 1 `dead_candidate` |
| H8 | Claims without test records | PARTIAL | findings-index; `tests/registry/` | **16 findings carry `no test record`** — unchanged list, all `b`-suffix sub-findings or pre-convention files, none cited in this rubric. **The new instance is worse in kind than in count**: F324 *declares* a gate-tier record that does not exist, which is the fifth occurrence of the F298–F303 defect and the first that the Amendment-1 guard catches rather than a human. Separately, the five cannot-fail cosmology gate records (F283, F285, F286, F295, F296) still need pass criteria from the findings that own them — **K3's new grade rests partly on two of them**, which is stated here rather than buried  *(2026-08-18: F325 lands with its record `F325-x1-branch` armed and two verified controls, and F298/F299/F303 are partially superseded under **S22** — noted here so this row's citations carry their replacement.)* |

---

## Method notes

**Graded from the indexes and ledgers alone:** most of C, E, G and the D ledger, plus all of the
carried-forward A rows. `findings-index.md`, `open-derivations.md` (last audited 2026-08-11, so
eight findings behind), the generated exactness tally, `key-decisions.md` and
`Claims-and-Falsifiers-Summary.md` carry enough for those.

**Rows that required a finding file rather than a ledger,** because no index carries the content:
A1 and B1 (F317, F318, F313's remediation record in the changelog), A6 (F312), B3 and B10 (F324 —
which is in no index at all), B9 and K9 (F311 against F322 and F319 respectively; the disagreements
exist only in the finding texts), H4 (read directly from the papers directory), H6 and H8 (measured
by running `tools/check_finding_records.py` against `tests/registry/`).

**This is the same class of finding as the previous two reports made about the ledgers, and it has
moved up a level.** The 2026-08-04 sweep complained the ledgers were stale; the 2026-08-07 sweep
complained they were current but had no row shape for a contradiction. This sweep's complaint is
about the *report*: it was amended eleven times and **six findings still passed it by**, because
each amendment was written by the session that produced its own finding. An amendment mechanism that
only fires when the finding's author remembers is not a mechanism. The concrete cost is measurable —
gap #5 was closed in full on 2026-08-11 and re-opened on paper on 2026-08-17, and one of its three
legs was re-derived from scratch by a session that did not know the first existed.

**Grades verified by spot-check** (the three I was least sure of):

1. **H6 `QUANT → PARTIAL`** — not read, *run*. `tools/check_finding_records.py` was staged with
   `tests/registry/*.yaml` and the findings on hand, `_FINDINGS`/`_REGISTRY` repointed, and
   `check_declared_records()` executed: it returns one violation, on F324, with the message quoted in
   the health probe. The tool's own docstring confirms it reads both the `**Test record:**` and
   `**Test / results:**` spellings, and F324 uses the second. `tools/run_gate.py:127` wires it into
   the gate. This is the strongest statement this report could make without a working workspace, and
   it is a measurement rather than an inference.
2. **K9's residual, and whether K3 could move** — checked F311 §4 and F319 §6 directly. F311 C1's
   chronology is exact and checkable (F192 V3 at 04:50, F193 at 17:35 the same day) and its C3
   double-count argument is sound *as accounting*. F319 §6 is a different claim and its arithmetic is
   explicit: same modes, same measure, same $\tfrac12$, different powers of $a$, hence a 2×2 solve.
   Grepping both files: **F319 contains no reference to F311, F193, F196 or F241, and F311 predates
   F319 by five days.** The fix went to the row's residual, not to either citation. K3 was checked
   the same way and its move is cleaner: F310's record `F310-critical-measure` exists at tier gate
   with a declared control, and `open-derivations` G2 already carries the reduction — the previous
   report simply never saw it.
3. **B9's two numbers** — checked F311 §2.2 and F322 against each other. They are physically
   compatible (F322's stated residual $1.559\times10^{-5}$ is the non-log constant F311's imported
   Källén–Sabry form supplies), but they are different *claims*: F311 §"Prior art" says its two-loop
   formula is *"cited, not derived here"*, while F322's comes from F261's sympy-exact $b_1 = 1$
   inside the model. `grep -c F311 F322` returns **0**. The row is graded on F322's model-internal
   $0.0495\%$ with F311's number stated alongside, rather than picking the smaller residual silently.

**Every F-number cited was checked to exist** against the `findings/` listing, the F01–F15 bundle and
`deprecated/findings/`. F16–F19 resolve in `deprecated/`, correctly. **F324 exists as a file and in
no index**, which is why it is cited with that caveat attached everywhere it appears.

**Citations to superseded findings, carried with their supersession, in the same table row:** F251
(S12 → F277), F258 (S12 → F277), F165 (S13 → F279), F62 (S3 → F64), F25 (S18 → F306), F94 (S21 →
F323, F265), F115 (S20 → F138, F231). This report is the newest completeness file and therefore the
one `check_superseded_citations.py` grades at zero.

**What this run could not verify.** Every one of the 81 gate records (none executed). The
`audit_tests --ratchet` triple, the numerics ratchet and the constants ratchet. Whether the 76
declared controls still verify RED at the current code fingerprint. The whole-tree keyword sweep the
ABSENT section depends on — only the indexes and ledgers were greppable, and `Witten` returning zero
against them while F324 is built on the Witten anomaly shows how much that under-reports. Whether
the 62 manifest-linked-but-undeclared artifacts are still the C7 arming to-do. All of these need the
device workspace, which has now been unavailable across two consecutive sessions.

---

## Amendment 1 — 2026-08-18 - 12:04 — F324 is armed, and the arming found a second gate red

Ben asked for the arming pass the same day this report named it. The device workspace was still
unavailable, so the pass was executed by staging the repository into an isolated container and
running the repository's own code against it. What follows is what actually ran; H6 does **not**
move, and the reason is at the end.

**The record is written and it runs.** `F324-ncolour-bracket` now exists in
`tests/registry/gauge.yaml` — `kind: assertion`, `tier: gate`, `module:
casim.engine.gauge.derive_ncolour_bracket`, `entry: check_ncolour_bracket`, eleven declared
`params:`, `expect.exactness: exact`, twelve `findings:`, and eight `control:` blocks each carrying
its measured red set and its reason. `casim test --id F324-ncolour-bracket` returns **PASS**.

**The physics was re-measured in-tree, not taken from the finding.** F324's own §11 records that its
14/14 was measured in an isolated harness against a `casim.numerics` shim because the workspace was
down. Run here against the real `casimir_ladder.py`, `derive_ncolour.py` and
`derive_su3_structure.py`, `check_ncolour_bracket()` returns **15/15 PASS** — the fifteenth leg
being P2, the F317 cross-check that the harness could only reach by extracting one function.

**All eight controls verify, and each reddens exactly what F324 §7 declares.** Measured twice: once
directly, and once through `casim test --control`, which resolves the declared tags against the
payload's legs and enforces "and only where declared".

| control | measured reds | of 15 legs |
|---|---|---|
| `n_generations=2` | W2, W2b, W3b, B1 | premise (i) — the transfer of debt to row C1 |
| `include_lepton_doublet=false` | W1, W2, B1 | premise (v) — the parity inverts, bracket returns {2} |
| `vector_like_su2=true` | W1, W2, W2b, B1 | F27's chirality, load-bearing for the colour count |
| `quark_colour_rep=adjoint` | W1, W2, B1 | premise (iv) — the colour input the parity does consume |
| `c7_n_max=3` | U1 | an untested N ≥ 4 is not an excluded one |
| `scan_from=2` | U1, U1b, B1 | an untested lower edge is not an excluded one |
| `doubler_multiplicity=2` | W2, W2b, B1 | premise (vi) — CL020's caveat |
| `empty_tower_passes=true` | U1, B1 | premise (ii) — the N = 1 edge is a convention |

**`check_finding_records.py` no longer fires.** The check that was red on F324 when this report was
written now returns zero violations over the findings staged here. Note the scope honestly: it was
run over ten finding files, not all 316, because the whole-tree sweep needs the workspace. It is the
F324 clause that is verified closed, not the whole-tree property.

**And the arming found something this report did not know.** `check_control_soundness.py --gate` is
also part of `make gate`, and the committed journal (`test-results/control-soundness.json`,
generated 2026-08-17 - 16:31) predates F323 by five hours. So **all five `gauge-bcc-mc-d4` controls
were unarmed**: controls 3 and 4 (`hypercubic_anisotropy`, `unsymmetrised_reps` — the two F323 added,
and the first of them *is* the 4/3) were absent from the journal entirely, and controls 0–2 carried a
fingerprint measured against the pre-F323 `bcc_action.py`. That is a **second, independent gate red**,
older than F324's and not caused by it. All five were re-verified here and each returns `CONTROL` on
exactly the red set F323 declares. The journal now carries 133 items against 123; ten were added,
three had their fingerprint refreshed, **none was removed or otherwise changed** — verified by diff,
because a journal pass that silently drops another record's verdict is the failure this layer exists
to prevent.

**H6 stays `PARTIAL`, and the grade is not being held down for form's sake.** Three things are fixed
and three are not. Fixed: the F324 record exists at the tier it claims, its controls are journalled,
and F323's five are too. Not fixed: **F324 is still in no index** and **CL281 is still not in
`claims-index.md` or `docs/claims/registry.yaml`**, so `make indexes-check` and `make claims` remain
red; and **no gate record has been executed** — the 81 are still unverified this cycle. Regenerating
the indexes from a partial checkout would be worse than leaving them stale, because `casim index`
rewrites each index from what it can see and a missing file reads as a deleted row. That step needs
the real tree.

**Still owed on the device, in this order:** `make indexes` → `make claims` → `make gate` →
`make control`. The first two are the remaining reds; the third should now pass the two checks that
were failing; the fourth is a no-op for F324 and `gauge-bcc-mc-d4`, whose verdicts are banked, and
will re-verify the rest.

**One process note, recorded because it is the same shape as this report's method finding.** F323
landed at 21:55 on 2026-08-17 and its changelog entry lists what it verified — ledger, banners,
citations, claims, `casim index`, module registry, test registry, numerics and constants ratchets —
and `make control` is not among them. The two controls it had just written were therefore never
armed, and nothing said so until a checker was run today. A verification list that omits the one
target covering the thing the session just added is the same class of gap as an amendment mechanism
that only fires when the author remembers.
---

## Amendment 2 — 2026-08-18 - 16:20 — B9's two numbers reconciled; gap #4 closed and H5 (ii) disposed

Ben asked for the decision-consistency item the same day this report named it: *"B9 carries two
different published residuals, $0.00158\%$ and $0.0495\%$, in two live documents, from two findings six
days apart of which the later does not cite the earlier"* (row **H5** item (ii); gap #4). This amendment
records what was done and what it decided. **It is a citation-graph fix. No physics ran, no leg, control,
status, falsifier or value moved in any finding or card, and neither grade below changes.**

**The disposition: two rows of one sum, not a disagreement.** Both numbers are $\Delta\alpha_\ell(M_Z)$
against PDG $0.031498$, and they differ by exactly one term:

| | one loop | $+$ two-loop **leading log** ($b_1=1$, F261 — model-internal) | $+$ two-loop **non-log constant** (Källén–Sabry — imported) | $\Delta\alpha_\ell(M_Z)$ | residual |
|---|---:|---:|---:|---:|---:|
| **F322 §6** | $3.1420928\times10^{-2}$ | $+6.1483\times10^{-5}$ | — | $3.148241\times10^{-2}$ | $1.5589\times10^{-5}$ = $\mathbf{0.0495\%}$ |
| **F311 §2.2** | $3.1420928\times10^{-2}$ | $+6.1483\times10^{-5}$ | $+1.6085\times10^{-5}$ | $3.149850\times10^{-2}$ | $-4.96\times10^{-7}$ = $\mathbf{0.00158\%}$ (an **over**shoot) |

The imported constant is $103.2\%$ of F322's stated residual, overshooting it by $4.96\times10^{-7}$ —
the same excess F311 reports from the other side as $100.6\%$ of the *one-loop* residual, and the same
single comparison. The report's §4 read
*"physically compatible"*; that is now arithmetic rather than an assessment.

**The rule adopted, which is a quotation rule and not a physics one.** B9's headline is **$0.0495\%$, the
model-internal number**, because it is derived end to end with zero imported constants. **$0.00158\%$ is
quotable only with its provenance attached** — *"after importing the Källén–Sabry two-loop constant"* —
which is how F311 §8 states it itself. The open work is unchanged and is jointly owned by both findings:
the two-loop leptonic bubble **on the model's own fields**, from F261's dispersive machinery. Having a
term's literature value does not derive it.

**No Part D row was opened, deliberately.** H5 (ii) observed that *"Part D was built for exactly this shape
and has one row."* It was not the same shape. Part D is for **two adopted results that cannot both be
true**; these two are additive, and recording them as a contradiction would dilute the one row (X1) that
genuinely is one. What the ledger needed was a disposition, and it now has one.

**Edits made, all citation-side.**

| Document | What changed |
|---|---|
| `findings/F322-b9-running-alpha-ew-rederived-post-f277.md` | Dated citation banner; F311 added to the header cross-references and to §10; **new §6.1** — the term-by-term reconciliation table, the "not a Part D contradiction" statement, and a **priority note**: §2 and §5's *refold restored* rows independently reproduce **F311 leg A1**, so gap #5(a)'s first closure belongs to F311 (2026-08-11) and F322 is an independent reproduction of it; §9's non-log-constant bullet now names F311's value for the term |
| `docs/claims/CL280-running-alpha-leptonic-lattice-bounded-and-two-loop.md` | F311 added to `findings:` and to Evidence; Statement now names both numbers with provenance; dated amendment in *Status & history*. The card continues to assert the model-internal $0.0495\%$ |
| `docs/status/open-derivations.md` | Closed row **B9** carries both numbers and their provenance; the *Structural notes* sentence *"B9's $0.24\%$ has not been re-derived on the corrected code"* — false since 2026-08-11 — is corrected in place with the correction marked; sector tally updated; **addendum 2026-08-18 - 16:20** records the disposition |
| this report | this amendment |
| `docs/status/changelog.md` | one entry |

**Grades.** **B9 stays `QUANT`** — the row's problem was that it published two numbers, not that either was
wrong, and the model-internal one is the weaker of the two, so nothing moves upward on a citation fix.
**H5 stays `PARTIAL`**: item (ii) is disposed, X1 is untouched and is still the largest item, and item (i)
(K9's F311-vs-F319 disagreement) is untouched — **one of the row's three items closed**, which is not a
grade change. Gap **#4 is closed**; the report's §4 *"smallest next step"* asked for one line in each
document and a cross-reference from F322 to F311, and got that plus the arithmetic that makes the two
numbers one statement.

**What this does not do**, stated so the next sweep does not read it as more than it is: it does not derive
the two-loop non-log constant on the model's own fields (F322 §9, F311 §8 — the same open target), it does
not touch B9's real residual, which §7 of F322 identifies as the **hadronic** piece in row **G3**, and it
executed **no gate record** — the H6 reds named in Amendment 1 are unaffected either way.

## Amendment 3 — 2026-08-18 - 16:35 — H4's outward half: the public summary is at revision 5, and it is now checked

Ben asked for `make citations` to reach `papers/Claims-and-Falsifiers-Summary.md`, which is the row **H4**
defect this report named at 10:21 — *"the cards are right and the public summary is stale"*. This amendment
records what was built and what was corrected. **No physics ran**: no leg, control, status, falsifier,
exactness or value moved in any finding or card. Every number below was read off a card and copied.

**The defect had two named instances, and both are closed.** (a) The summary listed *"$m_W$ and $m_Z$ in
absolute terms"* under **Scope — what is not claimed**, fourteen days after **F320** derived them and
**CL016** was withdrawn. It is now **core claim 12** (CL276 + CL277), the Scope entry is struck through in
the revision-3 style with the withdrawal named, and the residual inputs are stated ($v$, $\alpha$, F141's
equal-stiffness hypothesis). (b) The $\alpha_s(M_Z)$ row quoted $0.11955$ / $+1.7\%$ / $2.1\sigma$ without
its branch; the row and the accompanying note now say H1/centre, give $0.03970$ on H2, name the
$\sigma_6/\sigma_3 = 2.4911511$ measurement that points the other way, and name the deciding
$\Lambda$-ratio ($\approx1.78$ vs $\approx3.4\times10^6$). **X1 is untouched by this** — the fork is
recorded, not closed.

**The mechanism, which is the part that outlives this fix.** `tools/check_summary_claims.py` grades the
summary against `docs/claims/` the way `check_superseded_citations.py` grades the rubric against the
ledger, and for the same reason: the register moved and nothing propagated the move outward, because that
checker never opens `papers/`. Every claim, falsifier and scope entry in the summary now carries an anchor
— an HTML comment, invisible in the PDF — naming its cards **and the status it is recording them at**:

    <!-- claims: CL276=live, CL277=live -->

Three failures held at **zero**: an id with no card; a recorded status the card disagrees with (this is the
CL016 catch, and it fires on *any* status move, not only withdrawal); and the inherited rule that a unit
naming a superseded finding must name its replacement. Coverage is a **ratchet**, not a flat fail — a
headline card the summary never mentions means the summary is *behind*, not wrong, and holding that at zero
would block a result from being recorded until it had been written up for a lay reader. The ceiling is
**0/38** as of this amendment. Supporting-tier cards are not counted: CL278–CL281 are correctly absent.
Unit = one markdown block, table rows individually, the same small unit and the same argument as the ledger
checker. Selftest: four cases, the CL016 miss among them, and the tool prints PASS/FAIL on every run.

**What the sweep found beyond the two named instances.** Ten headline cards issued since revision 4 were
absent from the summary altogether — the 0/38 ceiling is met by adding them as **claims 12–18** with their
falsifiers: CL276/CL277 (absolute masses, $\rho=1$), CL264/CL253 (Born rule via Gleason; einselection),
CL256 (exact no-signalling), CL262 (the finite-$a$ defect is $\partial_i\Phi$), CL273/CL275 (two Sakharov
sectors; the uniform-reweighting no-go, which also sharpens the Scope entry on $\Lambda$), CL254
(structure formation, with the DES Y6 $3.00\sigma$ stated as a live falsifier and the absence of screening
stated as why there is nothing to tune), CL267 (the tilt, with $n_s=1$'s $8.4$–$9.9\sigma$ exclusion
recorded as a bill the model has not paid). Contingent cards are marked contingent in the text, not
promoted.

**Newly found, not fixed, and not previously recorded anywhere:** `papers/README.md` — the series front
matter, a public document — is still at revision-1 numbers. It headlines $\sin^2\theta_W=\tfrac14
\Rightarrow m_Z/m_W = 2/\sqrt3$ at $1.77\%$, the value revision 2 of the summary moved off on 2026-08-02
(F49/F138 on-shell $3/\sqrt7$, $-0.064\%$), and its black-hole line still leads with the superseded shadow
number. `check_summary_claims.py` does **not** cover it: it has no claim anchors and is not the register's
view. That is the next instance of this same defect and it is now on the record.

| Document | What changed |
|---|---|
| `papers/Claims-and-Falsifiers-Summary.md` | **Revision 5.** Claims 12–18 added; the $m_W$/$m_Z$ Scope entry struck through and moved; the $\alpha_s$ row and note given their branch; the $\Lambda$ Scope entry sharpened by the CL275 no-go; four rows added to the headline table; four falsifiers added; the authored-card count corrected $28 \to 58$; 48 anchors added; revision-5 blockquote |
| `papers/pdf/Claims-and-Falsifiers-Summary.pdf` | Regenerated (pandoc/xelatex, DejaVu Serif). **It had been at the 2026-06-08 first issue** — three revisions behind, not one |
| `tools/check_summary_claims.py` | New. The checker described above, with its selftest |
| `Makefile` | `citations` runs both checkers; target comment updated |
| `tools/run_gate.py` | New gate line, in provenance, next to the ledger checker it complements |
| `docs/design/module-graph.json` | Regenerated (the new tool) |
| this report | this amendment |
| `docs/status/changelog.md` | one entry |

**Grades.** **H4 stays `PARTIAL` and its second clause is discharged.** Both named instances are fixed and
the mechanism that let them happen is now a gate check, but a grade rise should follow an audit rather than
a fix, and this amendment has just produced evidence that the audit is not finished — `papers/README.md`,
above, is the same defect on a surface no one had looked at. The next sweep should grade H4 against the
whole outward surface, not against the two rows this one names. **No other row moves**: B8 and H5 keep X1
exactly as they had it, and B12 was already `QUANT` on CL276/CL277 before this amendment touched anything.

## Amendment 4 — 2026-08-18 - 17:15 — K9's F311-vs-F319 disagreement adjudicated: one leg withdrawn, one narrowed, and the residual restated

Ben asked for §3's item on the day this report named it. §3's *"smallest next step"* was a single
question — *"state whether F193's 'the CA ground state costs nothing to update' is an order-selective
statement or a uniform one, and therefore whether F319 U8 excludes it"* — and it comes back **uniform**,
which decides the disagreement instead of filing it. **No physics ran and no module was executed.** Every
number below is read off F59, F164, F193, F196, F241 or F319 and re-checked arithmetically; no leg,
control, status, falsifier, exactness or value moves in any finding or card.

### 1. The answer is uniform, and F193 Part A is inside CL275

F193's load-bearing step is **A2**: the beable field-energy density is *"quadratic in the field with **no
additive $c$-number** per mode"*, the $+\tfrac12$-per-mode offset being a template (Fock) artefact that
does not source the F64 dielectric. That statement deletes a per-mode $c$-number. It has no way to know
which *moment* of the mode sum it is deleting — and F59 Part C builds the other Sakharov sector out of the
same object:

$$\frac{1}{16\pi G}\bigg|_\text{lat}=\eta\,g_*\!\!\int_\text{BZ}\!\frac{d^3k}{(2\pi)^3}\frac{1}{2\omega}
\qquad\text{against}\qquad
\rho_\text{vac}\ \text{from}\ \int_\text{BZ}\!\frac{d^3k}{(2\pi)^3}\frac{\omega}{2},$$

with $\eta$ the Seeley $a_1$ number of the *same* one-loop determinant. This is F319 §6's *"same modes,
same measure, same factor of $\tfrac12$"*, restated in F59's own notation — and it settles the question:
**deleting the $\tfrac12$ per mode deletes both sectors**. F193 Part A is $\lambda\to0$, precisely F319's
uniform class, so **CL275 applies to it verbatim and it is excluded**. It may not be quoted as a standing
derivation of "the bare CC is zero in the ontology" without also deleting F79's $G$.

### 2. F311 C3 is withdrawn — the double-count argument proves too much

C3 argues that F79 gives $1/G$ with zero tree-level stiffness, so in this model $1/G$ **is** the vacuum
mode sum, and F192 V2 therefore sums the same modes at the same cutoff a second time as a source. **The
premise is correct and is F79's. The inference does not follow.** The $a_0$ and $a_1$ coefficients are
*different terms of one heat-kernel expansion*, both generated by the same modes and neither equal to the
other; two moments of one measure are not one quantity counted twice. Applied as stated, C3's rule would
mean Sakharov induced gravity can never induce a cosmological constant at all — whereas the induced CC is
the standard, and hardest, part of that program. F319 computes both moments in one function over one grid
($I_\text{cc}=4.0810486$, $I_g=1.9807020$) for exactly this reason.

This is **F311's own falsifier 5** — *"an argument that the induced Einstein equation **does** carry an
independent zero-point source would restore F192 V2 ... this is the one place C could be wrong"* — hit by
F319 U8 five days later, with neither finding citing the other.

What survives of leg C: **C1 (the chronology) stands** and is exact — F192 V3 at 04:50, F193 at 17:35 the
same day — so the "two unreconciled pictures" framing stays dead, for the reason F311 gave. **C2 (F192's
$w=-1$ is vacuous rather than contradicted) stands as an implication**, but it is *conditional* on
$\rho_\text{vac}=0$ actually holding, which is now the open question rather than an established one (see
row **K10**, which should not absorb it yet). **C's headline — "K9 collapses to a single $O(1)$
coincidence" — falls with C3 and is withdrawn.** F311 itself is not edited: findings are written once and
superseded rather than rewritten (D12), which is what this report and the claims layer are for.

### 3. F319 §6 is narrowed — it never enumerated the tree's fourth channel

F319 §6 concludes *"channel (ii) is promoted to sole survivor"*, having read F164 §C's list of three. It
contains no reference to F193, F196, F241 or F311. But F193 **Part B** and F196 are a *different*
mechanism from F193 Part A, and they are order-selective by construction:

| route | what it does to $a_0$ ($\rho_\text{vac}$) | what it does to $a_1$ ($1/16\pi G$) |
|---|---|---|
| F193 **Part A** — beable vacuum | deletes the per-mode $c$-number | **deletes it too** — uniform, excluded (CL275) |
| F164 channel (ii) — $AB\equiv1$ sequestering | removes the constant piece from the source | untouched by construction — right shape, **no number** |
| F193 **Part B** / F196 — capacity ceiling | caps $\rho_\text{grav}(L)\le 3c^4/8\pi G L^2$ | **nothing: the bound *contains* $G$** |

F196 derives the exponent from the model's own structure by two independent routes — the F183 Schwarzschild
capacity ($p=3-1=2$, slope $-2.0$ machine-exact) and the F190 area entropy with Gibbons–Hawking
equipartition — converging on the same closed form $3c^4/8\pi GR_H^2=\rho_\text{crit}$. Measured against
F319's own price:

| quantity | value |
|---|---|
| required $a_0$ suppression (F319 U8) | $\ge120.76$ decades, with $\le2.2\times10^{-5}$ on $a_1$ |
| required relative selectivity | $\ge1.27\times10^{116}$ |
| delivered by the ceiling ($\rho_\text{vac}\to\rho_\text{crit}$) | $120.66$ decades |
| perturbation of $a_1$ | **zero** — the bound uses $G$, it does not move it |
| shortfall | $0.10$ dex, i.e. the sub-unity factor $\Omega_\Lambda$ |
| (F193 §B's own $(a/R_H)^2$ route, for comparison) | $120.22$ decades, $0.54$ dex short |

So the tree already carries a route of the shape F319 demands, short by the $O(1)$ factor **F241 already
classified as the coincidence problem** — not by 116 decades. What it does **not** carry is the dynamics.
F241 (CL212) is explicit that the F183/F190 sector fixes a **ceiling** $\rho\le\rho_\text{crit}$, not a
value; a ceiling is a consistency requirement, not a suppression mechanism, and nothing shows the F164 sum
is *made* to respect it. F319's *"an order-selective mechanism that actually delivers it — **OPEN**"*
therefore survives, better posed and with a candidate.

### 4. The residual, restated

> **K9's residual is a *dynamical* enforcement of the F183/F190 capacity ceiling on the F164 zero-point
> sum, plus $\Omega_\Lambda$.** Two candidate routes have the right shape and neither is closed: F164
> channel (ii), which has no number, and F193 §B/F196/F241, which has the number to $0.10$ dex and no
> dynamics. F193 Part A is excluded. This is a **weaker** claim than "one $O(1)$ coincidence" (F311's) and
> a **narrower** one than "channel (ii) with a $1.27\times10^{116}$ price tag" (F319's), and it is the one
> both findings' arithmetic supports.

**One inconsistency found in passing, recorded and not fixed.** F196's own table quotes observed
$\rho_\Lambda=6.0\times10^{-10}$ J/m³ (inherited from F164) in the same table as
$\Omega_\Lambda\rho_\text{crit}=5.23\times10^{-10}$ J/m³ — the two $\rho_\Lambda$ inputs in the tree differ
by $0.06$ dex, which is why "the shortfall is $0.10$ dex" and "the shortfall is $\Omega_\Lambda=0.685$"
are the same statement only to within that. It sits inside the $O(1)$ this row is open on and changes
nothing above, but it should be reconciled by whoever next touches F241's residual.

### 5. No Part D row was opened, deliberately

§3 predicted *"either way `open-derivations` gains a second Part D entry, which is worth as much as the
answer."* That prediction assumed both readings leave a standing disagreement. They do not. Part D is for
**two adopted results that cannot both be true and that the tree cannot currently choose between** — X1,
where the confinement engine and the coupling normalisation want different readings and three candidate
reconciliations are closed. Here the fork is decidable and is decided: one leg is withdrawn on an argument
its own author named as the place it could be wrong, and one sentence is narrowed on a channel its author
did not enumerate. Filing that as a contradiction would dilute the one row that genuinely is one. This is
the second time in one day the ledger's Part D was the wrong shelf (Amendment 2, H5 item (ii)), and the
distinction is the same both times: **Part D is for forks, not for errors.**

### Edits made, all citation-side

| Document | What changed |
|---|---|
| this report | §3 given a dated disposition blockquote; rows **K9**, **K10**, **A11**, **E5**, **H5** (item (i)), parameter **#28** and the K9 regression row amended in place; this amendment |
| `docs/status/open-derivations.md` | Row **G1** rewritten: the adjudication is now stated with C3 withdrawn and the residual restated; the "do not re-attack" column corrected, since F311 falsifier 5 has *fired*; addendum recording the disposition and why no Part D row was opened |
| `docs/claims/CL021-cosmological-constant-not-derived.md` | The Evidence row citing F193 Part A as **exact** is narrowed — it was the one place a headline card asserted the leg headline card CL275 excludes. The card's own position (`not_claimed`) is unchanged and, if anything, better supported |
| `docs/claims/CL275-uniform-zero-point-reweighting-excluded.md` | Statement's "the only one of the three with the right shape" qualified to *of F164's three*; F193 named as the finding that turned channel (i) into a derivation; F193/F196 added to `findings:` and to Evidence; dated amendment in *Status & history*. **The no-go itself is untouched** — no value, status, falsifier or exactness moves |
| `docs/status/changelog.md` | one entry |

`papers/Claims-and-Falsifiers-Summary.md` is **not** edited and does not need to be: its claim 16 and its
$\Lambda$ scope entry state the CL273/CL275 no-go, which is unchanged, and both cards keep
`status: live`, so the revision-5 anchors `<!-- claims: CL273=live, CL275=live -->` and
`<!-- claims: CL021=not_claimed, CL275=live -->` remain correct. Checked against
`tools/check_summary_claims.py`'s contract rather than assumed.

### Grades

**K9 stays `OPEN`.** The disagreement is gone and the residual is better posed, but nothing was derived —
this amendment moves a reading, not a number, and a row does not rise for that. **A11 stays `QUANT`**: its
residual is still one number and §6's requirement still stands; what changed is that the requirement now
has a candidate of the right shape. **H5 stays `PARTIAL`**, with item (i) disposed — two of its three items
are now closed in one day and **X1 is the whole of what remains**, which is the sharpest that row has been.
**K10, E5 and #28 do not move.**

**What this does not do.** It does not derive $\Lambda$, does not close F319's OPEN line, does not show the
F183/F190 ceiling is dynamically enforced (that is now the named next step), does not touch $\Omega_\Lambda$,
and executed **no gate record** — the H6 reds named in Amendment 1 are unaffected either way. The smallest
next step for K9 is no longer a reading question: **show that the F164 zero-point sum is made to respect
the F183 capacity bound, or show that it is not** — a physics session, in the sector F196 and F241 already
built.
