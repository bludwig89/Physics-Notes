# Completeness overview — 2026-08-07 - 14:11

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: full sweep, 74 rows (blocks A, B, C, E, K, G, H) plus the 28-row parameter ledger (D).
Previous benchmark: `docs/status/completeness-2026-08-04.md`, **as amended through its Amendment 5
(2026-08-06 - 12:40)** — that file was amended six times after issue and the honest comparison is
against the amended state, not the tables as first written. Both deltas are given.*

**Health probe (what actually ran).**

`make indexes-check` **green** — all eight generated indexes current; max **F314**, 287 distinct
numbers across 298 files, 0 duplicates, 27 declared gaps (0 undeclared), `NEXT FREE NUMBER F305`
(backlog 8), exactness header 0 findings behind. `make registry` **green** — **400 records over 390
test files**, all valid (D9); kinds `assertion` 125 / `result_dump` 221 / `scenario` 3 /
`legacy_script` **51**; **gate tier 58**; baselines 7 `stale_by_design`, **10 `candidate` (drift
still FAILS by design)**. `make numerics` **green** — 269 physics modules, 0 direct `np.fft`
transform calls, 164 files importing numpy/scipy, ratchet intact. `make constants` **green** — 46
registered, 12 PASS / 0 FAIL; C7 backlog 267 unregistered literals in `tests/`. `make claims` —
**264 cards** (live 139, open 87, withdrawn 26, narrowed 4, contingent 3, not_claimed 5); debt
`unreviewed_seed` **223/223**, `falsifier_unset` 226/226, `exactness_unset` 63/63. `make health` —
390 files, no-assert **233**, **UNFALSIFIABLE 72**, import-time physics **328**, 0 unregistered.
Exactness tally: **exact 159 / machine 195 / quantitative 184**, coverage **538 of 538 (100%)**
across 425 artifacts. Module registry: **203 modules, 51 channel-driven (25.1%)**, 90 test-only,
31 standalone, 24 unreferenced; statuses live 143 / `fork_live` 25 / `fork_unclaimed` 23 /
`partial` 11 / `dead_candidate` 1.

> **Gate: SEEN GREEN THIS RUN — 57 of the 58 gate records verified PASS, zero FAIL, zero ERROR.**
> Run in sector slices against the 45 s ceiling: core 4/4, lattice 7/7, gauge 10/10, interactions
> 17/17, suite 19/19 verified. **All three `kind: scenario` physics gates ran and passed**
> (`scenario-bcc-weyl`, `scenario-gluon-bcc`, `scenario-photon-pair`) — the first sweep in which
> they have been exercised. `supersession-ledger` is **green, 48 passed** (the S14 `P5.1` malformed
> decision id that was red across three sessions is fixed). The one record not verified is
> `registry-entries`: it ran past 43 s in two attempts without completing and without a failure
> appearing, so it is recorded as **NOT COMPLETED THIS RUN**, not as green.
>
> **The previous two reports' "environment artifact" was self-inflicted and is now closed.** Both
> recorded `ModuleNotFoundError: No module named 'pytest'` under the vendored activation and set it
> aside as a sandbox defect. It was not: `.vendor/activate.sh` exports `PYTHONPATH`, and invoking
> `PYTHONPATH=src python3 -m casim.cli …` **replaces** that export rather than prepending to it, so
> the vendored `pytest`/`scipy` were on disk and unreachable. With `PYTHONPATH="src:$PYTHONPATH"`
> every one of those records passes. Two reports of gate uncertainty came from one shell assignment.

---

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A Foundations (12) | 4 | 1 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| B Gauge (12) | 4 | 0 | 2 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| C Matter (7) | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| E Gravity (13) | 3 | 1 | 4 | 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| K Cosmology (12) | 0 | 0 | 1 | 6 | 0 | 0 | 2 | 3 | 0 | 0 |
| G Emergent (10) | 1 | 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| H Integrity (8) | 0 | 0 | 3 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total (74)** | **14** | **3** | **15** | **35** | **0** | **1** | **2** | **4** | **0** | **0** |

*Every cell is counted from the grade column of the block's own table below; row sums equal the
block sizes (12, 12, 7, 13, 12, 10, 8 = 74).*

**Parameter ledger: 6 of 28 derived, 2 partial, 6 fitted or free input, 14 open or absent** —
unchanged for the third consecutive report. No quark-mass, CKM, $\alpha$, $v$, $m_H$ or $\Lambda$
work landed in three days.

**The shape of this report.** Coverage work is finished: **the ABSENT column is empty for the first
time**, and it stayed empty when re-swept rather than being inherited. What replaced it is not
progress. Two rows regressed in content without moving grade — the strong sector's headline coupling
is now contingent on a fork nobody has chosen (B8/B10/D16), and G5's isospin splitting is excluded at
$36.6\sigma$ by the model's own BBN — and the tree acquired a new instance of the one defect it had
already diagnosed and named: **four findings written in the last three days claim gate-tier test
records, with declared controls, that do not exist.** Against that, two integrity rows genuinely
recover: H4 returns to `QUANT` on verified evidence. (H6 briefly read `QUANT` too; finishing the
one verification this report had left incomplete turned that record red and the grade back to
`PARTIAL` — see the amendment in the health probe.)

---

## The five things most worth building next

Ranked by (load-bearing × distance from closure).

### 1. The colour-normalisation fork — one computation decides six decades, and it is the same computation as $d_1$

**What.** F144's bare colour coupling is normalised on the **centre** ($\chi=1$, $g_s=\tfrac12$)
while its running uses the $SU(N_c)$ $\beta$-function. F299 measured the model's own confinement
engine and found it implements the **Casimir** law instead ($\sigma_6/\sigma_3=2.4911511$ against
$5/2$ Casimir and $1$ centre, seven rungs to $\le1.36\%$, converging to the exact law over
$\beta=24\to192$). F303 then went looking for the argument that would license the centre reading and
**did not find one**, closing three candidate reconciliations exactly: not a scheme constant (the
shift is $26\times$ F144's entire measured A4 residual), not a three-link plaquette (the BCC
nearest-neighbour graph has no closed 3-bond loop, by parity and by exhaustive enumeration), not the
Cartan projection (Landau pole above $M_Z$).

**Why it matters.** It is not a refinement, it is a branch. Branch B (centre) keeps
$\alpha_s(M_Z)=0.11858$, $+0.5\%$; Branch A (Casimir) gives $g_s=\sqrt3/4$ and
$\alpha_s(M_Z)=0.03970$, $-66.4\%$, and takes F144's headline, F119's 19-decade hierarchy channel and
CL022's *"largest open tension at $2.1\sigma$"* with it. The same fork is what makes B10's surviving
route conditional: F294 root-found $N_c=2.998$ under the centre reading, $N_c=1.28$ under the
fundamental Casimir reading, and **no root at all** under adjoint. So one unchosen rational number is
load-bearing for B8, B10, D16, G5, E3, Q1 and Q2 simultaneously.

**What blocks it.** Nothing but the computation. F303 §6 names it: a one-loop background-field
computation of the **model action's own** $\Lambda$-ratio — F144 A4's "model-action analogue of the
Hasenfratz constant". Branch A requires $\approx3.4\times10^6$, Branch B $\approx1.78$. Six decades
apart, so the answer cannot be ambiguous.

**Smallest next step.** That computation **is** $d_1$, and gap #3 of the previous report already
built its apparatus: F287 verified the background-field machinery and F280 executed the subtracted
formulation against the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$ anchor, leaving one
open leg — the rule vertex form factors, $-2.0160$ of the required $\Delta C=-5.5755$ (36.2%,
bracketed $[-2.257,-1.446]$). Close leg 3 and the fork closes with it. This was the previous
report's #3; it is now worth six decades more than it was on 2026-08-04, and **nothing has been done
on it since F280 landed on 2026-08-05 - 12:40.**

**One further thing this row should record.** F303 §5 found the caveat was flagged **at the source**:
F101 §7 wrote the "A-vs-C / Casimir caveat" on 2026-06-05, F144 was built on top of it a week later,
and the tree derived a headline number across it for two months before F294/F298/F299 rediscovered it
under a new name. That is not a surprise arriving from outside — it is a deferral coming due, and it
is the strongest argument in this report for reviewing **load-bearing** findings rather than old ones.

### 2. Four findings claim gate records that do not exist — the F299 defect, three times over, after F299 named it

**What.** F298, F299, F300 and F303 each state in their header that they own a **gate-tier** record
with declared controls. What the tree contains is four **auto-generated stubs** in
`tests/registry/core.yaml` — `kind: legacy_script`, `tier: battery`, no `entry:`, no `expect:`, no
controls, `n_test_funcs: 0`. `test_F300_thermodynamics.py`'s own docstring reads *"record
`F300-lattice-thermodynamics`, tier gate, so this file deliberately defines no test functions"* and
instructs `casim test --id F300-lattice-thermodynamics --param linear_control=True`. **No record of
that name exists**, so the file that deliberately defines no tests is registered as a legacy script
with no failure mode, and both declared controls are unrunnable. F301 has no record at all — and F301
is the finding this rubric cites for closing A2's finite-$a$ boost seam.

**Why it matters.** This is exactly the failure F299 diagnosed on 2026-08-06 - 12:35 — *"a missing
record is the one D9 failure the module side cannot see"* — recurring in the three findings written
after it, including F299's own. `check_test_registry` is green throughout, because a stub is a valid
record; `check_module_registry` is green, because the modules have rows. The two checks that would
catch it do not exist. Concretely: **G10, B10, B8 and the whole F298–F303 colour arc are graded in
this report on results whose stated verification cannot be run.** The `legacy_script` count moved
47 → 51 over the same period, which is the ratchet that is supposed to run to zero moving backwards.

**What blocks it.** Nothing. The information needed is already in the finding files, in a fixed field.

**Smallest next step.** One check: parse the `**Test record:**` line of every `findings/F*.md`, and
fail when the named id is absent from `tests/registry/*.yaml` or when its `tier`/`kind` disagree with
what the finding claims. Then re-arm the four records. A second, cheaper guard: fail any record whose
`path` file contains the string `tier gate` in its docstring while the record's own tier is not gate.

### 3. Falsifier and check soundness as a gate (H2) — the ratchet has not moved in three days

**What.** Unchanged from the previous report's #2, and now measurable as *unchanged*:
`audit_tests --ratchet` reads **unfalsifiable 72, no-assert 233, import-time 328** — bit-identical to
2026-08-04, across fourteen new findings. `falsifier_unset` stands at **226 of 226** claim cards.

**Why it matters.** Gap #2 was the previous report's second priority and the F300 session cited it
approvingly (CL260 declines to invent an observational threshold rather than faking one) — the norm
propagated, the mechanism did not. Item 2 above is what an unmechanised norm costs.

**What blocks it.** Nothing; F22's remediation already shows the pattern (`control_fails` requiring
the same code path to go red under a parameter override).

**Smallest next step.** Make a declared-and-verified perturbation a D9 requirement for
`kind: assertion` records, retro-fitted to the 58 gate-tier records rather than all 400.
`casim test --param k=v` is the machinery and is already in use by the newer findings.

### 4. $g_*(T)$ over the model's 48 Weyl fields — one small computation, two rubric rows

**What.** F300 built lattice-native thermodynamics for the **photon sector only** and named
$g_*(T)$ as its next step; F297's BBN thermal history imports an SM degree-of-freedom count. Both K2
and G10 carry the same import, and it is the only import either row has that the model could supply
from content it already owns (48 Weyl fields, 2 real $E_g$ scalars, $N_\text{eff}=3.044$ already
forced by F165/F279/F47).

**Why it matters.** It converts the one external input shared by the two most recently assembled
sectors into a derived one, and — on the pattern F297 and F300 both demonstrated — an assembly grades
its own inputs whether or not it finds a defect.

**What blocks it.** Nothing structural. F300's partition function is already general in the
dispersion; the work is enumerating the content and summing.

**Smallest next step.** Compute $g_*(T)$ and $g_{*s}(T)$ from the model's own field content across
the BBN window, then re-run `cosmology_bbn.py` against it and quote the shift in $Y_p$ and D/H.

### 5. The three numbers no report has re-derived

**What.** Three items are now on their third consecutive report with no work recorded against them.
**(a)** B9's leptonic $\Delta\alpha(M_Z)=0.24\%$ comes from F251, which S12-F277 supersedes, and F277
flipped a vacuum-polarization sign; grep still finds no post-F277 re-derivation. **(b)** The **10
`candidate` baselines** still report FAIL by design with no recorded decision on whether they are
regressions or accepted physics changes. **(c)** K9: the cosmological constant has **two
unreconciled pictures** (F193/F196/F241 vs F192 under the adopted F178 law), untouched since
2026-08-02.

**Why it matters.** (a) is the cheapest — one number, one re-run — and it is cited in the rubric as
`QUANT` evidence. (b) is ten silent reds. (c) is the only remaining `OPEN` row in cosmology besides
K3 and the one where the model contradicts itself rather than merely lacking an answer.

**Smallest next step.** (a) Re-derive $\Delta\alpha(M_Z)$ on post-F277 code and either re-bless or
move B9's grade. (b) One triage pass writing a decision per candidate baseline. (c) State which of
the two $\Lambda$ pictures the adopted F178 law actually entails.

---

## What is ABSENT

**The table is empty.** For the first time since this command was written, no rubric row is graded
`ABSENT`. The seven that the 2026-08-04 report opened with (A8, A9, A10, B10, K2, K11, G10) all
closed between 2026-08-05 and 2026-08-06, and this sweep re-checked each rather than inheriting the
amendment: all seven have findings, modules and index entries behind them.

| # | Requirement | Status |
|---|---|---|
| — | — | No row in blocks A, B, C, E, K, G or H is `ABSENT` as of this sweep |

**What the empty list means, and what it does not.** It does not mean the model accounts for
everything the rubric asks; it means every rubric row now has *a sector*, and the honest grades are
`PARTIAL` (35 of 74, up from 31 as first written) rather than `ABSENT`. The dominant grade in this
report is "attacked, with a named residual". That is a real change in the project's shape — the
2026-08-04 report's Amendment 5 predicted it in these words, *"the remaining work in this report is
now entirely integrity work, not coverage work"* — and this sweep confirms it: **all five items in
the ranking above are integrity or depth items, and only one is new physics.**

It also means the rubric has run out of resolution. Three things with **zero hits repo-wide** sit
*inside* rows rather than as rows of their own, and a future sweep should either grade them or say
why not:

| Sub-row gap | Where it lives | Hits |
|---|---|---|
| Proton decay / baryon-number-violating rate | C7 (beyond-SM content), K6 (Sakharov #1) | `findings/` 0, `papers/` 0, `docs/` 0 |
| Unruh effect / accelerated-observer thermality | E9 (BH thermodynamics), G10 | 0 everywhere |
| Topological defects (strings, walls, monopoles as relics) | K7 (DM identity), K12 | 1 `docs/` hit, 0 findings |

The first is the sharpest: K6 grades all three Sakharov conditions as met, and the model has no
baryon-number-violating process with a rate. "Met" and "computed" are different claims, and the row
says so, but the absence of any $B$-violation calculation anywhere in the tree is not visible from the
row as graded.

---

## Regressions since 2026-08-04

Graded against that report **as amended to 2026-08-06 - 12:40**. Two rows regress in content without
moving grade, one integrity row is worse, and two grades are corrected downward on argument rather
than on new evidence.

| Row | Was | Now | Why |
|---|---|---|---|
| B8 Asymptotic freedom / $\alpha_s$ | PARTIAL, residual "$d_1$" | **PARTIAL, residual is a fork** | F299 measures the model's own confinement engine implementing **Casimir** scaling; F303 finds **no argument** for the centre normalisation the coupling uses, and closes three candidate reconciliations exactly. $\alpha_s(M_Z)$ is branch-contingent: $0.11858$ ($+0.5\%$) vs $0.03970$ ($-66.4\%$). CL022's $2.1\sigma$ framing is contingent on an unchosen branch and gains a history note saying so |
| B10 Why 3 colours | PARTIAL, "one surviving route, contingent on an unvalidated modelling choice" | **PARTIAL, the choice is now contradicted by the model's own engine** | F294 already showed the selector returns $N_c=1.28$ under fundamental Casimir and has no root under adjoint. F299 then showed the tree's confinement sector **implements Casimir**. The one route that returns 3 requires the reading the model's own machinery does not use |
| G5 Hadron spectrum | QUANT, "$m_n-m_p=+1.51$ (sign correct)" | **QUANT, with an excluded sub-result** | F297's BBN measures $m_n-m_p$ to $\pm0.0056$ MeV, where F122's own acceptance check used $\pm1$ MeV. The model's $+1.51$ MeV is excluded at $36.6\sigma$ in helium and by a factor 2.7 in $\tau_n$ (331 s vs $878.4\pm0.4$). The K2 amendment recorded this on 2026-08-05; **the G5 row was never updated** and still reads as a passing number |
| H8 Findings without a usable test record | PARTIAL, 18 findings | **PARTIAL, and materially worse** | 17 findings carry `no test record`, but the list now includes **F301** — the finding this rubric cites for closing A2's boost seam. Separately, F298/F299/F300/F303 claim gate-tier records with declared controls; the tree has auto-generated `legacy_script`/`battery` stubs. `legacy_script` 47 → 51 |
| H7 Module coverage | PARTIAL, 51/189 = 27.0% | **PARTIAL, 51/203 = 25.1%** | Denominator grew by 14, driven count did not move. Same mechanism as last report, second consecutive fall |
| A6 Superposition + Born rule | EXACT (Amendment, 2026-08-06) | **PARTIAL** | **Correction on argument, not new evidence.** F304 §5 does prove the frame-function theorem here, and that is a real result. But F304's own residual 3 is live: context-blindness is proved for the **$U(1)$ wrap generator only**; the $SU(2)_L$ and $SU(3)_c$ commutators are "not written out". Non-contextuality is a *premise of the derivation*, so a premise verified on one of three gauge factors is a named seam, which is `PARTIAL` by this rubric's own vocabulary |
| A10 Cluster decomposition / no-signalling | MACHINE (Amendment, 2026-08-05) | **PARTIAL** | **Correction on argument.** No-signalling is machine-exact ($7.8\times10^{-16}$) and the strictly-zero cone is a genuine CA-specific result. But the row's other half — clustering — is established only in **1-D free-fermion**, and F290's own residual 1 says the interacting 3-D statement "has *not* been made". A row graded on its easier half is over-graded |

**Content regression with no grade change, carried a second time: H2.** The ratchet
(`unfalsifiable 72`, `no_assert 233`, `import_time 328`) is bit-identical to the previous report
across three days and fourteen findings. The previous report asked for this to be mechanised; item 2
of this report's ranking is what the delay cost.

**Carried forward, third consecutive report — all still unverified.** B9's $\Delta\alpha(M_Z)=0.24\%$
un-re-derived post-F277 (F251 is superseded by S12). 10 `candidate` baselines still FAIL by design
with no recorded decision. K9's two unreconciled $\Lambda$ pictures, untouched since 2026-08-02.

### Resolved since 2026-08-04 — and this half is substantial

- **H4 `PARTIAL → QUANT`.** Banner enforcement landed (`careful-tidy-noether-2`, 2026-08-05 - 00:10):
  `apply_supersession_banners.py` gained a markdown path keyed off `record["findings"]`,
  `test_no_orphan_banners` was widened to walk `findings/` and `deprecated/findings/`, `findings:`
  blocks were populated on S3/S4/S6/S10/S11/S12/S13/S15/S18, and the S14 `P5.1` malformed decision id
  was fixed. **Verified this run**: `supersession-ledger` gate record green, 48 passed.
- **H6 `PARTIAL → QUANT`.** The barrier was seen green — 57 of 58 gate records PASS, 0 FAIL, all three
  scenario physics gates exercised for the first time. The one incomplete record is named above.
- **Gap #5b closed.** `open-derivations.md` was re-audited on 2026-08-05 to frontier **F314** (it had
  been at F256). Genuinely-distinct open targets **3 → 5** (both additions honest: G2 was previously
  mis-graded excluded, B10 was never counted), closed-negative rows **12 → 20**, and rubric row IDs
  are now named in the ledger's status cells, which is what gap #5 existed to make possible.
- **Gap #3 executed verbatim.** F280 formulated $d_1$ subtracted against the Wilson anchor, with a
  three-leg budget of the required $\Delta C=-5.5755$: Wilson seagull structurally absent $-2.5676$
  (46.1%), propagator face measured $-0.9919\pm0.0439$ (17.8%, the first absolute number for that
  leg), rule vertex form factors $-2.0160$ **OPEN** (36.2%).
- **H5's one live code-vs-finding contradiction closed.** The lepton hypercharges are `casim.constants`
  entries with `(F165, F279)` provenance, `Y_E_R` *resolves from* `Y_LEPTON_L` rather than being typed,
  and the F279 gate record re-solves the six-row system and reads the normalisation back out of the
  registry. The quark hypercharges are deliberately **not** registered, because their fractions carry
  the underived $N_c=3$ — which is B10's problem, not H5's.
- **The claims layer (D12) is standing.** 264 cards with a gate check that fails a `live` card whose
  every finding is superseded; `Claims-and-Falsifiers-Summary.md` at revision 4 with the charged-lepton
  shape angle as core claim 11.
- **The "environment artifact" was a shell assignment.** See the health-probe note.

---

## Amendment 6 — 2026-08-16 - 18:45 — row A11 moves, and it costs F164 a channel

Row A11 was the report's longest-standing `PARTIAL`: three consecutive reports, no work against
it, and a diagnosis ("both individually sound, nowhere reconciled") that named a *missing
document* rather than missing physics. F319 supplies it and the row moves to `QUANT`.

The reconciliation itself is standard Wilsonian EFT, and the interesting fact is that this tree
had never written it: `wilson` returns the Wilson gauge action and the Wilson $\Lambda_L$
constant, never Wilson's renormalisation group, and `irrelevant operator` / `decoupling` /
`dimension-6` return nothing. Three hundred findings of Wilsonian physics without the Wilsonian
vocabulary, and A11 is where the gap surfaced as an apparent contradiction.

**Why `QUANT` and not `EXACT`.** The model *is* UV-finite — no divergences, no Landau pole in
domain (258.9 decades outside it), a fixed mode set, a finite cell budget. Its residual is one
number, $\rho_\text{vac}$, and one number that is wrong by $10^{120.76}$ is not an EXACT row.
What changed is that the residual is now **counted and named** rather than described: the ledger
proves exactly two coefficients carry the cutoff with no parameter to absorb them, and the model
predicts one of them correctly.

**The new cost, which should not be read as progress.** F319 U8 is a no-go, and it lands on the
model's own preferred escape. F59 builds $1/16\pi G$ from $\int d^3k/2\omega$ and F164 builds
$\rho_\text{vac}$ from $\int d^3k\,\omega/2$ over the same modes with the same $\tfrac12$; they
are two moments of one sum carrying different powers of $a$. So the $2\times2$ solve for
$(\lambda,a)$ against both observables returns $a^\star=8.29$ Gpc and $\lambda^\star=5.8\times10^{120}$
— an *enhancement*. F164's channel (i), which that finding called "the leading candidate
(elegant-design preferred)" while labelling it "a position, not a calculation", is closed by
doing the calculation. **The model cannot delete its zero-point sum without deleting F79's $G$.**

That is a genuine loss of an option, and it is the honest shape of this amendment: A11 improves
because the accounting improved, while the physics problem underneath got *harder to escape* and
acquired a price tag — a surviving mechanism needs $\ge1.27\times10^{116}$ of selectivity between
two adjacent heat-kernel coefficients. Gap #1b below records it.

**Gap #1b — an order-selective vacuum-energy mechanism.** F164 channel (ii) (sequestering through
the $AB\equiv1$ dielectric) is the only one of the three with the right shape, and it is
unevidenced. This is now the single named residual of block A.

F164 is **not** superseded: its computation stands and F319 reproduces $I_\text{cc}=4.081$
independently. What moved is the disposition of one candidate resolution — a claim changing
without a finding changing, which is what D12 exists for (CL275).

---

## Amendment 7 — 2026-08-16 - 19:20 — row B12 moves, and it was an accounting error

Row B12 read `PARTIAL` with the residual **"absolute scale is an input"**, and the register
carried that as an explicit `non_claim` (CL016: "$m_W$ and $m_Z$ in absolute terms are not
predicted — only their ratio"). F320 finds the premise true, the conclusion false, and the row
moves to `QUANT`.

**The error was one inference, and it is worth naming precisely.** The card reasoned: $v$ is an
anchor, therefore $m_W$ and $m_Z$ are not predicted. $v$ *is* an anchor — F119's overall scale
$N=m_\text{lat}(\tau)$ has no $O(1)$ mechanism, ledger 17 stays `FIT (N=1)`, and F320 does not
touch it. But the two statements differ by the **input count**. The Standard Model's electroweak
sector takes three measured inputs — $\alpha$, $G_F$ and one boson mass — and predicts the other.
This model takes **two**, because $\sin^2\theta_W^\text{os}=\tfrac29$ arrives from lattice
geometry instead of from a third measurement. Two inputs is not zero inputs, and F320 leads with
that. But an object produced from inputs that do not include it is an output.

**Why nobody had noticed.** The missing step is three lines. F141 posits one stiffness quantum $u$
per structural channel ($g^2=7u$, $g'^2=2u$), takes the ratio, and stops — correctly, because the
ratio does not need $u$. Eliminating $u$ against $e=g\sin\theta_W$ determines it:
$u=18\pi\alpha/7$, hence $g^2=18\pi\alpha$ exactly and

$$m_W=\frac{3v}{2}\sqrt{2\pi\alpha},\qquad m_Z=\frac{9v}{2}\sqrt{\frac{2\pi\alpha}{7}} .$$

Neither closed form was anywhere in the tree. The rationals are the BCC Wigner–Seitz facet count
and the F51 sublattice count; no free parameter survives.

**Why `QUANT` and not `EXACT`.** The tree value is $-1.60\%$ and the radiative correction
$\Delta r$ is external, so the absolute numbers are a **bracket**: $m_W\in[80.147,80.548]$ GeV and
$m_Z\in[90.879,91.332]$ GeV, both containing PDG. What makes the row `QUANT` rather than merely
bracketed is that the residual is stated **free of $\Delta r$**: model and SM sit on the same
on-shell relation with the same $\Delta r$, which cancels in the ratio (verified to
$2.2\times10^{-16}$ over $\Delta r\in[0,0.10]$), leaving $+0.222\%$ on $m_W$ and $+0.158\%$ on
$m_Z$. The absolute-mass prediction inherits the on-shell angle's accuracy and **adds no new
freedom** — which is why it can be quoted at all.

**The $\rho$ leg, which the row also asked for and nothing had ever supplied.** The SM gets
$\rho=1$ at tree level from the Higgs doublet's custodial $SU(2)$. This model has no Higgs field
and therefore no access to that argument, and until now had no substitute. F41 absorbs exactly
**one** Stueckelberg direction on $U(x)$, so the breaking is **rank one**, so $\det M^2$ vanishes
*identically in $u$* — checked over $\mathbb Q$ at five independent rationals — so the photon is
exactly massless and $\rho=1$ exactly for every $u$. That is a determinant, not a symmetry
assumption, and the `rank_two_breaking=true` control turns it into a measurement: exactly the
three $\rho$ legs go red and nothing else does.

**What got more expensive, which should not be read as progress.** F141's equal-stiffness
hypothesis (U) — (U1) equality across the two facet types, (U2) the axis↔sublattice
cross-normalisation, (U3) the quadratic-form assembly — is still open, and it now carries **two
absolute masses where it previously carried one ratio**. The `equal_stiffness=false` control
prices that: break (U1) and fourteen legs go red. The induced-stiffness lattice loop that F138 §4
and F141 §4 already both name as their next step is now the next step for a third row as well.
That three-way convergence on one calculation is the standing recommendation out of this
amendment.

**Gap: the electroweak scale is unchanged and is now the whole residual of block B12.** $v$ and
$\alpha$ are the two anchors; F119 and F127 own them; neither moved.

CL016 is **withdrawn** with a full retraction record — the second card in the register retired for
stating a scope boundary one step too far in. CL276 and CL277 are its live successors.

---

## Full rubric

### A — Foundations

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| A1 | Spacetime dimensionality | PARTIAL | F291, F292 | the "+1"; $s=2$ minimal cell | Two independent selectors each return $\{3\}$: $\ker J=0\Rightarrow d\le3$, $\operatorname{coker}J=0\Rightarrow d\ge3$; and $\dim\Lambda^2\mathbb R^d/d=1$ only at $d=3$. $d=6$ and $d=9$ excluded; reducible $d=3n$ freezes. Not `EXACT` — the "+1" is by construction and $d$ is derived from *adopted* structure. F291 §7 asks for this grade |
| A2 | Lorentz invariance | PARTIAL | F26, F28, F30, F246, F129, F301 | deformed shell exact but **not universal** | Seam closed 2026-08-06: the whole Poincaré defect is $D_i=\partial_i\Phi$, $\Phi=(\Omega^2-c_\text{lat}^2k^2)/2c_\text{lat}^2$ — $[K,P]$ never fails, $[K,K]$ reduces to the same $D_i$, and $D_i$ survives $K\to K+f(k)$, so it is not an artifact of a chosen boost. Exact to all orders on $\langle100\rangle$ ($3.5\times10^{-46}$); $O(\lvert k\rvert^3)$ rational for the even photon; one order worse on a chiral branch. **F301 itself has no test record** — see H8 |
| A3 | Causality / locality / finite speed | EXACT | F26, F204, F227, F290 | 0 | $c_\text{lat}=1/\sqrt3$; strict cone $C(r,t)=0$ for $r>4t$; F290 measures the cone **tight** at 1 site/layer where a generic Lieb–Robinson system has an exponential tail (bound 7.39 vs measured $6.9\times10^{-16}$) |
| A4 | CPT, and C, P, T separately | PARTIAL | F53 | — | C, P, CP built per species and exact; CP conserved at one generation ($J(1)=0$ arithmetic, not a prediction). **No CPT theorem for the QCA**; T is thin. Unmoved for three reports |
| A5 | Unitarity | EXACT | F276, F264, F300 | 0 | Every step is a length-preserving rotation by construction; F300 adds fine-grained von Neumann entropy conserved to $1.1\times10^{-12}$ on a **mixed** state |
| A6 | Superposition + Born rule | **PARTIAL** (was EXACT) | F304, F281, F290, F227 | non-contextuality proved for $U(1)$ only; CKM regularity lemma | Superposition structural; the Born rule is derived and **Gleason is proved here** (F304 §5): $b_k=(-1)^k/\binom{k+d-2}{k}$, survives iff $1+(d-1)b_k=0$ — one formula gives every odd $k$ at $d=2$ and only $k\le1$ at $d\ge3$. Both premises are forced by the rule: $\dim\ge3$ (a record needs cells; the 2-dim momentum blocks are invariant but **unreadable**, $\lVert[\Pi_k,\hat n]\rVert$ matching $\sqrt{2/N-2/N^2}$ at literal `0.0`) and non-contextuality (weight spread literal `0.0`). **Downgraded from the 2026-08-06 amendment**: F304's own residual 3 says context-blindness is shown for the $U(1)$ wrap generator only and the $SU(2)_L$/$SU(3)_c$ commutators are not written out. A premise verified on one of three gauge factors is a named seam. Record `F304-born-rule-gleason` verified **PASS** this run |
| A7 | Entanglement, Bell/Tsirelson | EXACT | F212, F226, F214, F217 | $1.8\times10^{-15}$ | Saturates Tsirelson $S=2\sqrt2$ exactly ⇒ Bell-indistinguishable from QM (CN1, settled null) |
| A8 | Measurement problem / classical limit | EXACT | F281, F130, F41 | Born legs now live at A6 | Pointer basis **forced** by minimal coupling ($[H_\text{int},\hat n]$ literal `0.0`; $\{\hat n(x)\}$ maximal abelian ⇒ unique); predictability sieve minimises at the site basis, spin correctly **not** einselected; classicality is a block-spin attractor, $\lambda_\text{coh}$ the Dirichlet kernel, irrelevant at $b^{-2}$ per dimension. **Arguable at EXACT**: M3 is proved on the free block-spin flow, not on the interacting theory. Held because the pointer result is a literal zero and a uniqueness statement, not a tolerance |
| A9 | Spin-statistics | PARTIAL | F289, F291, F292, F217 | topological step external | The theorem's two premises are derived here ($d=3$; $R(2\pi)=-\mathbb 1$ to $1.7\times10^{-16}$ over 60 axes). **Not** a new proof: $\pi_1=S_n$ and the belt-trick homotopy stay external, and CL255 is `tier: supporting` for that reason |
| A10 | Cluster decomposition / no-signalling | **PARTIAL** (was MACHINE) | F290, F227 | clustering is 1-D free-fermion | No-signalling exact ($7.8\times10^{-16}$) and the strictly-zero cone is genuinely CA-specific. **Downgraded**: the clustering half is a staggered 1-D free-fermion chain, $\xi\propto\Delta^{-0.9268}$ quoted as measured, and F290's own residual 1 states the interacting 3-D claim "has *not* been made" — which is the harder and more interesting half of the row |
| A11 | UV completeness | **QUANT** (was PARTIAL) | F116, F164, F264, F284, **F319** | **one number**: $\rho_\text{vac}$, $10^{120.76}$ | **Amended 2026-08-16 — the reconciliation landed (F319, 21/21, 4/4 controls CONTROL).** The dictionary was Wilsonian and simply absent from the tree: on a physical cutoff a counterterm is the *finite* bare→measured map, and F264's power-counting theorem reads "finitely many operator coefficients carry the cutoff" rather than "finitely many counterterms absorb the infinities" — strictly stronger, entirely finite. The licence is measured, not asserted: the lattice-vs-continuum scheme constant is IR-independent ($2.0\times10^{-12}$ drift over six decades of $m$) and the $\ln$ coefficient $1/16\pi^2$ is universal across four schemes while the constant is not. Decoupling is quantified — the leading irrelevant operator is dimension-6 with the **exact rational** coefficient $-[(1-\sum\hat n_i^4)/144+(\hat n_x\hat n_y\hat n_z)^2/24]$ ($1.1\times10^{-20}$, 60 dps), **no dimension-5 term exists** (exponent $p=2$), and the residue is $3.0\times10^{-31}$ at LHC. The ledger then counts **exactly two** cutoff-carrying coefficients with no free parameter — the two Sakharov sectors — one right ($G$) and one wrong by 120.8 orders. Not EXACT because that second number is still open. **New cost, not a free win**: F319 U8 shows the $\Lambda^4$ and $\Lambda^2$ sectors are two moments of one measure, so F164's *own leading* cancellation channel (i) is **excluded** — the 2×2 solve returns an 8.3 Gpc cell. See gap #1b |
| A12 | Continuum limit | MACHINE | F129–F135, D1 | $\lVert[R_b,\text{evo}]\rVert\le1.8\times10^{-15}$ | $c_\text{lat}$ an exact RG fixed point; simple-cubic code retained as the declared regression target |

### B — Gauge structure

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| B1 | Origin of $SU(3)\times SU(2)_L\times U(1)_Y$ | PARTIAL | F27, F51, F43, F291 | $SU(3)_c$ imposed | $SU(2)_L$ derived by $\beta$-gauging the complex-mass step; $U(1)_Y$ from bipartite sublattice parity; F291 adds the precondition that the phase $SU(2)_L$ gauges exists only for $\operatorname{coker}J=0$, i.e. $d\ge3$. Colour is still put in |
| B2 | Chirality | EXACT | F27, F91, F292 | Ward identity $1.1\times10^{-17}$ | $W^\pm$ chiral is *forced* — right-branch weight $\equiv0$ over ℚ. F292 adds an independent route: traceless $\Gamma=\gamma_1\cdots\gamma_D$ needs **odd** $d$, by explicit Clifford recursion $D=2..8$ |
| B3 | Anomaly cancellation | EXACT | F38, F293 | Witten global anomaly unchecked | All six traces (gauge + gravitational) exactly zero. F293 re-verifies the full six-constraint system symbolically in $N_c$ over ℚ: grav and cubic identically zero as polynomials. **Witten $SU(2)$ still not checked** — unmoved for three reports |
| B4 | Hypercharge / charge quantisation | EXACT | F165, F279, F47, F51, F38 | one charge unit, + $N_c=3$ for the thirds | Rank 6, dim 1 over ℚ; closing constraint is the F47 Majorana step. Core claim 10. **Code literals closed for the leptons** (2026-08-06): registry constants with provenance, `Y_E_R` resolving from `Y_LEPTON_L`, guarded by a gate check that re-solves the system. Quark hypercharges deliberately unregistered — their fractions carry the underived $N_c=3$ |
| B5 | EWSB mechanism | EXACT | F27, F34b, F44 | 0 | Higgs-free Stueckelberg; $U(x)$ pure gauge; $m_A=0$ from a rank-deficient mass matrix. Founding decision #3 |
| B6 | Weinberg angle, with scale | QUANT | F138, F49, F231, F141 | $+0.22\%$ at $M_Z$; $-0.064\%$ on shell; **0 free params** | $\tfrac14$ = matching at $\mu_\star=4\pi v=3.09$ TeV, forced by $Y$ having no lattice kinetic term; $\tfrac29$ is its on-shell face |
| B7 | Confinement | PARTIAL | F70, F86, F88, **F299**, **F323**; F94 **partially superseded** by F265, F323 (ledger `S21`) | 3+1D is constructed, not proven; $d=2$ for the F299 leg | Exact in 2D (area law, $\sigma=-\ln w(\beta)>0$ for all $\beta$). **Amended 2026-08-17 — the d=4 leg was never on the model's lattice.** F94 sampled a simple-hypercubic Wilson action, which F265 proved has an exact kernel freeing one of the four $\langle111\rangle$ link axes and missing asymptotically 1/3 of the curvature-carrying link content; both actions share a classical continuum limit, so F94's normalisation anchors could pass on a blind action. F323 supplies the replacement on the genuine BCC action as $\mathrm{BCC}_3\times\mathbb Z$ (10 plaquettes per site: 6 rhombi + 4 mixed rectangles), staple identity $2.3\times10^{-16}$, gauge invariance $3.8\times10^{-17}$, and **derives the anisotropy** $\beta_t/\beta_s=4/(3c_\text{lat}^2)=4$, $\xi=1/c_\text{lat}=\sqrt3$ — which is $(4/3)\xi^2$, not the hypercubic $\xi^2$. It also executes F299's d=4 Casimir successor, unrun since 2026-08-06. **The residual is unmoved and unmovable by sampling**: a proof needs a transfer matrix with positivity, absent repo-wide. **H8's clause "F299's claimed gate record does not exist" is STALE** — armed 2026-08-07, passes. See Amendment 11 |
| B8 | Asymptotic freedom / $\alpha_s$ running | PARTIAL | F144, F151, F239, F235, F287, **F280**, **F299**, **F303** | **the H1/H2 normalisation fork**, then $d_1$ leg 3 | $b_0=\tfrac{11}3C_A=11$ exact and numerically recovered (F287). $d_1$ now has a subtracted formulation (F280) with 36.2% of $\Delta C$ open. **But the residual is no longer only a value.** F303: no argument exists for the centre normalisation the chain uses; the Casimir reading gives $\alpha_s(M_Z)=0.03970$ ($-66.4\%$) against the centre reading's $0.11858$ ($+0.5\%$), and the tree cannot currently choose. The register's $0.11955$/$+1.7\%$/$2.1\sigma$ is a Branch-B number stated without its branch. See gap #1 |
| B9 | Running of $\alpha$, EW couplings | QUANT | F322, F251 ⚠, F261, F138, F231, F115 | leptonic $\Delta\alpha(M_Z)$ $\mathbf{0.0495\%}$; EW $+0.222\%$ | **Re-derived post-F277 by F322 (Amendment 9, 2026-08-17) — the flag was mis-stated.** The $0.24\%$ never touched the refolded path (disjoint call closure, bitwise). What F277 supplied was the *warrant*: the lattice bound on $\Delta\alpha$ was $183$–$190\times$ the quoted agreement with the refold present, and is $0.088\times$ it and falling without. F261's exact $b_1=1$, never previously fed into the running, closes $79.8\%$ of the shortfall. Residual is now row **G3** (hadronic), which the EW leg's $\alpha$-sensitivity quantifies at a factor $2.02$ |
| B10 | Why 3 colours | PARTIAL | F293, F294, **F298**, **F299**, **F303**, F279, F144, F110 | $N_c$ still not derived; the surviving route is contradicted by the model's own engine | Anomalies **cannot** select $N_c$ here (nullspace dim 1 for every $N_c$); colour is **not** the spatial 3; the $\mathbb Z_3$ route is **circular**. The one route that returns 3 is the $\Lambda$-scale selector (28.3 decades over $N_c=2..4$; $N_c=2.998$ from $\alpha_s$, partly circular and labelled so) — and it needs the centre reading H1. F299 then measured the model's confinement sector implementing **Casimir** (H2), under which F294 root-finds $N_c=1.28$; the adjoint reading has **no root at all**. Read this row as: *the route space is mapped, the one surviving route requires a normalisation the model's own machinery does not use, and no argument for it exists* |
| B11 | Strong CP / $\theta_\text{QCD}$ | **QUANT** (was PARTIAL) | **F321**, F53, F305, F307, F91 | **$\arg\det M_q$ at three generations** (E6/E7); the action fork; non-perturbative $\theta$-sectors | **Amended 2026-08-17 — the row's own evidence was misattributed, and the loop question is closed (F321, 20/20, 3/3 controls CONTROL over disjoint red sets).** The residual this row carried for three reports — *"tree $3.3\times10^{-16}$; loops open"* — quoted F53, but F53 P5 measures the **F27 complex-mass phase** and F53's own Remaining section says strong CP *"is a separate phase in the gluon sector (F43), untouched here"*. The number is correct and was attached to the wrong object, so the row did not have tree-level evidence either. Same shape as B12's Amendment 7. The physics then closes on an identity nobody had used here: in Euclidean signature the $\theta$-term is the **unique purely imaginary** gauge invariant, so *"the rule's action is real"* and *"the rule has no $\theta$-term"* are the same statement — and reality is a property of the rule's **loop set**, not of a `Re()` anyone inserted. The 20 oriented minimal rhombi are **closed under reversal** (exact, 0 missing), giving $\operatorname{Im}S=1.2\times10^{-14}$ on Haar-random SU(3) at 99.7 % disorder, $S$ invariant under $U\to U^*$ while the one-sense functional is **odd at literal `0.0`**. Every vertex coefficient is real at **literal `0.0`** at 2, 3 and 4 legs with colour indices sampled — and since that function class is closed under products and $q\to-q$ symmetric loop integration, $\Gamma$ is real at **every order**, which is exactly the item the 2026-06-29 audit flagged. Sensitivity is measured, not assumed: injecting $\theta$ gives $\operatorname{Im}S=-\theta\sum Q$ exactly with $\sum Q=2.078\ne0$. Not EXACT, and the reason is the honest one: $\bar\theta=\theta+\arg\det M_q$, this closes the **first** term only, and the second is the quark mass texture (E6/E7). **This is not a solution of the strong CP problem** — see CL279, a deliberate non-claim. See Amendment 8 |
| B12 | Gauge-boson masses, $\rho$, $m_Z/m_W$ | **QUANT** (was PARTIAL) | F49, F141, F138, F231, **F320** | **$v$ and $\alpha$** (two anchors, unchanged); F141's hypothesis (U) | **Amended 2026-08-16 — the row was an accounting error (F320, 22/22, 3/3 controls CONTROL).** "$v$ is an anchor" is true and "$m_W$, $m_Z$ are not predicted" does not follow from it: the SM's electroweak sector takes three inputs $\{\alpha,G_F,m_Z\}$, this model takes **two**, and an object produced from inputs that do not include it is an output. Eliminating F141's stiffness quantum against $e=g\sin\theta_W$ **determines** it, $u=18\pi\alpha/7$, giving $g^2=18\pi\alpha$ exactly and the closed forms $m_W=\tfrac{3v}{2}\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}{2}\sqrt{2\pi\alpha/7}$ — neither of which was anywhere in the tree. Residual stated **free of $\Delta r$** ($2.2\times10^{-16}$ over $\Delta r\in[0,0.1]$, because the correction is common to model and SM and cancels in the ratio): $+0.222\%$ on $m_W$, $+0.158\%$ on $m_Z$; absolute values bracketed at $[80.147,80.548]$ and $[90.879,91.332]$ GeV, both containing PDG. **The $\rho$ leg is new**: no $\rho$ derivation existed, and $\rho=1$ follows from the **rank** of F41's single Stueckelberg direction ($\det M^2\equiv0$ over $\mathbb Q$ at five rationals), not from a custodial $SU(2)$ this Higgs-free model cannot invoke. Not EXACT: $v$ stays ledger-17 `FIT (N=1)` (F119), $\alpha$ stays F127's no-go, $\Delta r$ is external, and F141's (U) now carries two absolute masses where it carried one ratio. See Amendment 7 |

### C — Matter content

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| C1 | Exactly three generations | PARTIAL | F75, F84 | physical identification is a hypothesis | Group theory is a **theorem** ($\sum d^2=48$ ⇒ max single-valued irrep dim 3, $T_{1u}$ unique); the identification is a **stated hypothesis** (F75 §7, a Candidate finding). F292 §6 found the same $n$-copies multiplicity structure and **declined the inference** rather than counting it as support |
| C2 | First-generation multiplet | EXACT | F38, F41, F42, F51, F165 → F279 | 0 | Complete and anomaly-free. F165's attribution is superseded by F279 (S13); its conclusion is retained in full |
| C3 | Colour triplet + fractional charge | PARTIAL | F136, F165, F279 | conditional on $N_c=3$ | Fractional charge is forced by the $3y_Q+y_L=0$ row, i.e. by the input $N_c=3$; commensurability holds for any $N_c$. Inherits B10's new conditionality |
| C4 | Neutrino nature (Dirac vs Majorana) | PARTIAL | F47, F266 | — | The Higgs-free Majorana step is constructed and $\nu_R$ is a structurally-forced total singlet ($Y=0$, and F279 A2 makes that row the one that closes the hypercharge system). Nothing **forces** Majorana over Dirac |
| C5 | Neutrino mass mechanism | PARTIAL | F47, F236, F254 | $M_R$ free | See-saw + $E_g/Z_3$ texture fix the three light masses and hierarchy at machine precision; absolute scale unfixed |
| C6 | Antimatter / charge conjugation | EXACT | F53, F260 | 0 | Per-species $C$; positron and crossing sector built |
| C7 | Beyond-SM content | PARTIAL | F223, F228, F266, F216, F204, F237 | geon abundance free; **no $B$-violating rate anywhere** | Predicts a Planck-mass BH-remnant geon, cold and collisionless. Excludes its own alternatives: native massive spin-2 (CN5), $\nu_R\nu_R$ J=2 (CN6), Alcubierre warp (F204), keV sterile as 100% DM (F237). New note: "proton decay" has **zero hits repo-wide** — the model's $B$-violation content is stated (F47's anti-linear Majorana step) and never rated |

### D — The parameter ledger

| # | Parameter | Grade | Evidence | Note |
|---|---|---|---|---|
| 1–6 | $m_u,m_d,m_s,m_c,m_b,m_t$ | ABSENT ×6 | F121 | Quark masses are "the measured values converted to kg — a **consistency** readout". The constituent scale $m_c=309.5$ MeV from one $f_\pi$ anchor (F123) is a different quantity |
| 7–8 | $m_e/m_\tau$, $m_\mu/m_\tau$ (shape) | QUANT ×2 | F175, F234, F120 | $\le0.007\%$ with **zero shape parameters**, from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$; Koide $Q=\tfrac23$ at $0.91\sigma$. Now core claim 11 of the register (rev 4) |
| 9 | Charged-lepton overall scale | FIT (N=1) | F121, F233 | $\tau$-anchored. F233 reduces the derivation gap to a factor 1.9 zero-param — **through the $\alpha_s$ transmutation channel, so it inherits gap #1's fork** |
| 10–13 | CKM 3 angles + 1 phase | ABSENT ×4 | — | Scope: out of scope. $J(1)=0$ is one-generation arithmetic, not a prediction |
| 14 | $\alpha_\text{em}$ | OPEN | F127 | Four-avenue no-go on deriving it from the rule. Still the one EM input |
| 15 | $g_2$ / $\sin^2\theta_W$ | QUANT | F138, F49 | Derived with its scale, $+0.22\%$, 0 params |
| 16 | $g_3$ / $\alpha_s$ | PARTIAL | F144, F239, F287, F280, F303 | Residual restated: **first the H1/H2 fork, then $d_1$ leg 3** (36.2% of $\Delta C$, bracketed). Route narrowed by F280; value unmoved; branch unchosen |
| 17 | $v$ | FIT (N=1) | Scope | "The electroweak scale $v$ is an anchor, not an output" |
| 18 | $m_H$ | OPEN | F73 | Kinematics exact, but free-sum kinematics cannot reproduce 125.25 GeV; missing input is binding dynamics |
| 19 | $\theta_\text{QCD}$ | PARTIAL | F53 | Tree-level pure gauge; loops open |
| 20–21 | 2 light-$\nu$ mass ratios | MACHINE ×2 | F236 | The $E_g/Z_3$ texture fixes masses + hierarchy at machine precision |
| 22 | $\nu$ absolute scale ($M_R$) | OPEN | F47, Scope | Nothing in the model fixes $M_R$ |
| 23–25 | 3 PMNS angles | EXCLUDED ×3 | F254 | Proven **no lattice selector**: the three $T_{2g}$ amplitudes are three inequivalent 1-d irreps under the $E_g$-stabiliser $D_{2h}$. Permanently free — a result |
| 26 | $\nu$ Dirac CP phase | ABSENT | — | Not addressed |
| 27 | $G$ | EXACT | F79, F107 | $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ structural; $3\times10^{-8}$ vs CODATA; 0 free params. Inherits F75's hypothesis status per claim 4 |
| 28 | $\Lambda$ | OPEN | F164, F192, F193, F196, F241 | Two unreconciled pictures; untouched since 2026-08-02, third report |

**Ledger tally — unchanged for the third report.** Derived with zero free parameters: **6** (2 lepton
ratios, $\sin^2\theta_W$, 2 $\nu$ mass ratios, $G$). Partial, one named residual each: **2**
($\alpha_s$, $\theta_\text{QCD}$). Fitted or free input: **6** (lepton scale, $v$, $\alpha$, 3 PMNS).
Open or absent: **14**.

**How to read that against the SM's 19.** Not "6 beats 19". The model **derives 6 quantities the SM
takes as free**, **proves 3 more permanently free** (PMNS, F254 — itself a result), and **does not yet
address 14**, of which 11 are quark masses and CKM. One thing this report must add: of the 6 derived,
**one ($\sin^2\theta_W$) and both partials now sit downstream of the unchosen colour-normalisation
branch or of $v$**, so "zero free parameters in the sectors we built" is true of the *count* and not
yet of the *chain*.

### E — Gravity and general relativity

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| E1 | Fundamental field equation | POSIT | F178 | — | DECISION 2026-06-29: induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$. Alternatives genuinely closed: energy-only is not Lorentz covariant and has no NS maximum mass. **Independently confirmed since** by BBN on an unrelated observable (F297: the demoted law gives $Y_p=0.1856$, $-17.6\sigma$) |
| E2 | Equivalence principle | MACHINE | F64, F62 ⚠ | — | F62 is named in S3 (superseded in part); its lapse-mix sign convention is still production code |
| E3 | PPN $\beta,\gamma$ | EXACT | F64 | $\beta=\gamma=1$ exactly | GR-identical. The naive linear dielectric ($\beta=\tfrac12$, 50.1″/cy) is excluded |
| E4 | Classical tests | QUANT | F64, F107, F111 | $3\times10^{-8}$ | Mercury 42.98″/cy, solar-limb 1.7512″, Shapiro, redshift |
| E5 | Newton's constant | EXACT | F79, F107 | $3\times10^{-8}$ vs CODATA | Structural, not Sakharov-premised. Fixes $a/\ell_P=\sqrt{8\pi}3^{1/4}=6.5978$ |
| E6 | GW speed, polarisations, dof | EXACT | F180, F248, F216 | GW170817 residual $\le3\times10^{-83}$ | $c_\text{grav}=c_\gamma$ is a **genuine zero**, inherited through F79 zero-tree-stiffness. Explicit TT graviton, 2 helicity-$\pm2$ modes, proven massless |
| E7 | Inspiral / ringdown QNM | QUANT | F189, F187 | $<7\%$ (WKB) | GW150914 chirp mass 28.1 $M_\odot$, ISCO 67.6 Hz |
| E8 | Black holes | QUANT | F183, F186 | shadow $3\sqrt3M$ | Exact Schwarzschild/Kerr with horizon. The $+4.63\%$ shadow, echoes and absent Hawking spectrum are WITHDRAWN (cards CL023–CL027) |
| E9 | BH thermodynamics | PARTIAL | F190, F183, **F300 §5** | one posited constant; the target is now an entanglement entropy | $S=A/4$ reproduced **iff** each F107 cell carries $2\pi\sqrt3$ nats — F190 labels itself speculative. **F300 §5 proves F190's own named next step impossible as written**: $e^{2\pi\sqrt3}=53252.295$ is $0.295$ from an integer and $2\pi\sqrt3/\ln2=15.7006$ is $0.299$ from one, so the cell entropy is not a state count of anything. The *necessary* capacity condition passes at $6.11\times$ (96 fermionic modes/site, $66.542$ nats against $10.883$ required). **The grade does not move, and the finding says so** — a question becoming well-posed is not the question being answered |
| E10 | Singularity resolution | PARTIAL | F183 §L1, F284 §5 | $r_\text{core}$ is a saturation estimate | BH: Kretschmann saturates at the cell scale ⇒ $r_\text{core}\propto M^{1/3}$, $\sim5\times10^{-22}$ m at $1M_\odot$, gate-tested. Cosmological: no substrate singularity, first resolvable epoch $H_\text{max}=3^{-3/4}M_\text{Pl}$ at $t_\text{min}=\sqrt3$ ticks. No geodesic-completeness result, no interior solution on the core |
| E11 | Interior / TOV / NS EoS | QUANT | F181, F184, F185 | — | SLy $M_\text{max}=2.08M_\odot$, $R(1.4)=11.1$ km, consistent with PSR J0740 + NICER; $I/MR^2\approx0.31$ |
| E12 | Quantum-gravity sector | PARTIAL | F216, F248, F79 | — | Graviton exactly massless, 2 dof, UV transversality $\Pi\propto Q^2$ + IR block-spin irrelevance. Gravity's own UV completion beyond "the lattice is the cutoff" is not developed |
| E13 | Galactic-scale consistency | EXCLUDED | F194, F191 | — | The model-native emergent-gravity route is **falsified** by the Bullet-Cluster lensing/gas offset. A dark *source* is required — a result, and a self-inflicted one |

### K — Cosmology

*Row IDs are `K`, not `F`.*

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| K1 | FRW background | QUANT | F182, F188, F284 | measured $\Omega$'s in | Full-tensor source reproduces ΛCDM: $z_\text{eq}\approx3430$, $z_\text{acc}\approx0.63$, age $\approx13.8$ Gyr. F284 re-reads expansion as $K$'s conformal mode on a **rigid** substrate and buys $\dot G/G\equiv0$ exactly. Solved *with* the model's source, not derived *from* the lattice |
| K2 | BBN / light elements | PARTIAL | F297, F79, F178, F182, F284 | $\eta_b$ free; network offset $-0.87\%$; $^7$Li not validated; **$g_*(T)$ imported** | Expansion side entirely model-native, $N_\text{eff}=3.044$ *forced* by the model's own content. $Y_p=0.2449$ ($-0.11\sigma$), D/H $=2.47\times10^{-5}$ ($-1.8\sigma$). Two results beyond the closure: it independently confirms F178, and it **measures** $m_n-m_p$ 179× more sharply than F122's own check — see G5. F300 has since discharged one of its assumptions (continuum $p=\rho/3$ safe by 44 orders) and named the one that remains ($g_*(T)$ over the 48 Weyl fields) — gap #4 |
| K3 | CMB peaks, $n_s$ | OPEN | F295, F296, F285, F286 | $\gamma=0.017550$; operator unidentified in-model | Full CMB fit out of scope. The *index* is not excluded: $p=0$ is a **scale-free anomalous dimension**, so F285's 8.4σ exclusion of $n_s=1$ is the positive statement $\gamma\ne0$. Constant $\gamma$ predicts $dn_s/d\ln k=0$ exactly; F286's log class predicts $-2.62\times10^{-4}$; they separate at $\sigma\sim2.6\times10^{-4}$. F296 names the operator ($T^i{}_i$ in holographic cosmology) and the obstruction. Now ledger row **G2**, the audit's "headline new problem" |
| K4 | Inflation or substitute | EXCLUDED | F282, F283, F296, F238 | cause named + 4 falsifiers | No slow-roll direction exists: $a/\ell_\text{red}=3^{1/4}$ exactly ⇒ sub-Planckian cutoff; every compact CA direction carries $M_\text{Pl}^2/f^2\ge\sqrt3$. F283 proved the obstruction exactly invariant under $a\to sa$ ($\partial r/\partial s\equiv0$). Ledger CN7/CN8 |
| K5 | Primordial spectrum normalisation | EXCLUDED | F282, F284, F285, F238 | $A_s$ free, cause named | With no inflaton and a rigid substrate offering no generating process, $P(k)$ is an automaton **initial condition**. The amplitude $A_s=2.1\times10^{-9}$ has no route and has not moved |
| K6 | Baryogenesis | PARTIAL | F202, F47, F53 | magnitude not derived; **no $B$-violating rate** | All three Sakharov conditions met by the model's own structure. Not a Boltzmann computation; no asymmetry number — and "proton decay" and "sphaleron" between them have one finding hit in the whole tree. Condition 1 is *met* in the sense of being available, never rated |
| K7 | Dark-matter identity | PARTIAL | F223, F228, F266, F216, F237 | — | Candidate: graviton–graviton J=2 geon, stable as a one-cell Planck-mass BH remnant, $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$ exact, cold and collisionless. Alternatives excluded |
| K8 | $\Omega_\text{DM}h^2=0.12$ | EXCLUDED | F238, F282–F285 | free input, cause named | Provable non-derivability, and **upgraded this audit from "observed free" to "proven free"**: F282 turns the structural *absence* of an inflaton into a structural *exclusion*, F284 puts $\beta$ in the right category (initial state), F285 quantifies the mirror constraint. Ledger D3 |
| K9 | $\Lambda$ magnitude | OPEN | F192, F193, F196, F241 | two unreconciled pictures | Route (a): bare CC exactly zero, $p=2$ dilution derived, 121 orders reduced to the $\Omega_\Lambda\approx0.685$ coincidence. Route (b) under the adopted F178 law: the zero-point sum still overshoots by $\sim10^{121}$, all four cancellations underived. **Not one open question but two answers that disagree.** Untouched since 2026-08-02 — third consecutive report |
| K10 | Dark energy $w$, vs DESI | PARTIAL | F192, F203 | sign exact; magnitude open | Vacuum $w=-1$ gives $\rho+3p=-2\rho$ so it accelerates — sign correct and exact. F203 flags $w=-1$ vs DESI DR2 as one of three falsifiers under pressure |
| K11 | Structure formation / $\sigma_8$ | PARTIAL | F288 | $A_s$ free (K5); EH98 $T(k)$ imported | The EFT of dark energy carries two free functions; the model has **zero**, from three independent sources ($\mu=1$ with $\partial_k\mu\equiv0$; $\dot G/G\equiv0$; zero linear slip from $AB\equiv1$). $\gamma_g=6/11$ and Meszáros $D(y)=1+\tfrac32y$ are sympy literal zeros; $f\sigma_8$ vs 7 RSD points gives diagonal $\chi^2/N=1.012$. $\sigma_8=0.8204$ **reported with its budget, not claimed**. Falsifier: no screening exists, so the DES Y6 low-$S_8$ direction ($3.00\sigma$) cannot be accommodated |
| K12 | Cosmological initial conditions | PARTIAL | F284, F285, F286, F295, F296, F238 | one anomalous dimension, operator unnamed in-model | The state must be non-generic by $10^{-56}$ vs white noise at the pivot *and* $\sim2\times10^6$ enhanced at the PBH scale — opposite ends of the same function. Residual is a specific number attached to a specific kind of object, with an external candidate and a quantified obstruction ($r$ over BK18 by 9.0–26.9×) |

### G — Emergent and precision physics

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| G1 | Maxwell / classical EM | EXACT | F26, F87, F245, F246, F306, **F314**; F25 (identity) | 0 | The composite-photon curl closes at $O(k^3)$ with exact coefficient $c_\text{lat}^3/48=1/(144\sqrt3)$; the reported $O(k)$ failure was a representation artifact. **New this cycle:** F314 gives the model's first real-space demonstration that its own photon propagates — closed-form pair group velocity $\partial\Omega_\text{pair}/\partial k_i$ matched at $7.8\times10^{-16}$ over 24 ticks on a wrap-free $128\times48\times48$ box, energy conserved to $3.7\times10^{-15}$ on the moving packet, no transient. It also found and gated a new failure mode (wrap-freeness is a condition on the *carrier*: at $k_0\sigma_x=3.14$ the residual degrades six decades) and escalated two items rather than burying them |
| G2 | Hydrogen, fine structure, Lamb | QUANT | F125, F252, F257, F262 | Lamb $=99.5\%$ of measured | $-13.596$ eV from $m_e+\alpha$ alone; Ry to $1.1\times10^{-12}$ of CODATA; 2p split 10.95 GHz; Bethe log from the model's own spectrum with no literature constant. Residual = two-loop $\alpha(Z\alpha)^5$, declared out of scope |
| G3 | $g-2$, electron and muon | PARTIAL | F252, F261 | hadronic + EW absent by declared scope | $a_e=\alpha/2\pi$ exact; two-loop $A_2=-0.328478965$; $A_2(\mu)=0.765857$ vs $0.765857410$. Hadronic VP, HLbL and EW **not** claimed — the entire interesting part of the muon anomaly |
| G4 | Atomic structure / periodic table | QUANT | F148, F195, F208 | light elements only | H/He/Li/C certified stable (net charge $\le2.2\times10^{-16}$, Pauli via live Gram–Schmidt); He IP 24.0 eV; relativistic SCF with an accuracy map |
| G5 | Hadron spectrum | QUANT | F123, F124, F235, F122, **F297** | 1 anchor ($f_\pi$); $\sqrt\sigma/f_\pi$ $+12\%$; **$m_n-m_p$ excluded at $36.6\sigma$** | Nucleon $3m_c=928.5$ vs 938.27 MeV ($-1.05\%$) on one anchor; mesons few-%. The $+12\%$ is $d_1$, and therefore now also gap #1's fork. **Regression recorded here for the first time:** F297's BBN measures $m_n-m_p$ to $\pm0.0056$ MeV against F122's own $\pm1$ MeV acceptance, and the model's $+1.51$ MeV is excluded at $36.6\sigma$ in helium and by 2.7× in $\tau_n$ (331 s vs $878.4\pm0.4$). F122's **sign** claim survives; its value does not. The row keeps `QUANT` on the nucleon mass and the meson sector, not on the splitting |
| G6 | Nuclear binding | QUANT | F104, F113, F126, F128, F240, F206 | 1 param ($b=0.55$ fm) | Deuteron $E_b$ 2.224 vs 2.22457 MeV (**0.026%**), $r_d$ 0.4%, on a fully derived OBE potential with no tuned hard core |
| G7 | Weak decays | PARTIAL | F54, F48 | absolute rates tied to $v$ | $d\to u+W^-\to u+e^-+\bar\nu$ end-to-end, 10/10. Structure exact; $G_F$ inherits the $v$ anchor. **F297 adds an independent handle**: the free-neutron lifetime is now a computed number (331 s) and it is wrong by 2.7× |
| G8 | Scattering / S-matrix | MACHINE | F260, F259, F263, F264 | — | Tree QED S-matrix + crossing; Bloch–Nordsieck IR cancellation; Euler–Heisenberg, light-by-light, Schwinger pair production; renormalizability with $D=4-\tfrac32E_f-E_\gamma$ exact; $Z_1=Z_2$ a computed identity (F258, refold-corrected by F277 — S12; its $S_0$–$S_4$ are unchanged) |
| G9 | Condensed-matter emergents | QUANT | F210–F215, F218, F242, F207, F171 | Allen–Dynes $6.3\%$ | $2\Delta/kT_c\to2\pi/e^\gamma$ and $\Delta C/C_n=12/7\zeta(3)$ at machine precision; $\mu^*$ **derived** from the F64 dielectric (no fit), cutting $T_c$ error $14.3\%\to6.3\%$. Casimir exact |
| G10 | Statistical mechanics / thermodynamics | PARTIAL | F300 | equilibrium only; photon sector only; $g_*(T)$ not built | The partition function is built on the model's **own** derived dispersion. $w=1/3$ and Stefan–Boltzmann are **theorems** in the IR, with closed-form lattice corrections $\propto\Theta^2$ and the parameter-free ratio $C_u/C_w=15/2$, each against BZ quadrature to $\le5.0\times10^{-4}$. $T_\text{lattice}=3.719\times10^{31}$ K; F297's continuum $p=\rho/3$ safe by 44 orders. Fine-grained entropy conserved ($1.1\times10^{-12}$) on a **mixed** state; coarse-grained entropy rises but **time-symmetrically** ($1.8\times10^{-4}$), so the arrow is the initial condition, not the dynamics. The free sector **cannot** thermalise: $2N$ conserved $n_\pm(k)$ fix a GGE. **Its claimed gate record does not exist** — see H8 |

### H — Model integrity

| # | Requirement | Grade | Evidence | Note |
|---|---|---|---|---|
| H1 | Parameter count vs the SM's 19+ | PARTIAL | ledger above | 6 derived, 3 proven-free, 14 unaddressed. **Not cheaper than the SM in raw count**; the sectors it has built carry zero free parameters, which is the claim actually made. New qualifier this report: three of the six derived quantities sit downstream of either the $v$ anchor or gap #1's unchosen branch, so the chain is not as parameter-free as the count |
| H2 | Falsifiability | PARTIAL | Claims rev 4 + `docs/claims/`; `make health`; `audit_tests --ratchet` | Register level unchanged and strong: five numerical thresholds, plus the shape falsifier at $0.007\%$. **Instrument level has not moved at all**: `unfalsifiable 72`, `no_assert 233`, `import_time 328` are bit-identical to 2026-08-04 across fourteen findings, and `falsifier_unset` is 226/226 cards. The claims layer added the first machine check for overstatement (a `live` card whose every finding is superseded now fails the gate), which is why this is not a further downgrade |
| H3 | Out-of-sample survival | QUANT | Claims rev 4 | One clean instance: $m_Z/m_W=3/\sqrt7$ fixed **before** PDG 2025 excluded CDF-II $m_W$; against $m_W=80.3692\pm0.0133$ it gives $-0.064\%$. Unchanged, and still the only one |
| H4 | Retraction hygiene | **QUANT** (was PARTIAL) | supersessions.yaml S1–S18; `supersession-ledger` gate | **Recovered, and verified this run.** The enforcement gap the previous report named is closed: `apply_supersession_banners.py` has a markdown path keyed off `record["findings"]`, `test_no_orphan_banners` walks `findings/` and `deprecated/findings/`, `findings:` blocks are populated on nine ledger rows, and the S14 `P5.1` malformed id is fixed. `supersession-ledger` **48 passed** in this sweep. Withdrawn claims are cards (CL023–CL027) with a gate test asserting they are never deleted. Not `EXACT`/`MACHINE` — this is a process row |
| H5 | Internal consistency of decisions | PARTIAL | key-decisions.md D1–D12 | Decisions 1–7 mutually consistent as written; D2 reversed on the record (S8). The hypercharge code-vs-finding contradiction is **closed**. **One new and larger item replaces it**, and it is physics rather than bookkeeping: the confinement sector implements Casimir scaling (F299) while the coupling normalisation the same sector's $\alpha_s$ chain depends on requires the centre reading, with no argument for it (F303) and three candidate reconciliations closed. Two remaining watch items: B9's un-re-derived $0.24\%$; four findings whose stated test records do not exist |
| H6 | Reproducibility | **QUANT** (was PARTIAL) | 58 gate records; this run | **Recovered.** 57 of 58 gate records verified PASS in sector slices, 0 FAIL, 0 ERROR; **all three `kind: scenario` physics gates exercised and green** for the first time in this command's history. `registry-entries` did not complete inside the 45 s ceiling and is recorded as unverified, not green. Gate records 47 → 58. Two caveats keep this off `MACHINE`: "from a clean checkout" is untested (the working tree carries a large uncommitted diff), and the barrier's *coverage* is the H8 problem below |
| H7 | Module coverage | PARTIAL | D11 registry | **51 of 203 channel-driven (25.1%)**, down from 27.0%: the denominator grew by 14 and the driven count did not move. 90 test-only, 31 standalone, 24 unreferenced, 25 `fork_live`, 23 `fork_unclaimed`, `dead_candidate` 1 |
| H8 | Claims without test records | PARTIAL | findings-index; `tests/registry/` | **REMEDIATED 2026-08-07 - 17:05, same day, and the grade stays `PARTIAL`.** As graded at 14:11: 17 findings carried `no test record` including **F301** (this rubric's evidence for A2), and F298/F299/F300/F303 each claimed a gate-tier record with declared controls where the tree held an auto-scaffolded `legacy_script`/`battery` stub. All five are now armed and verified — see Amendment 1. Post-fix: **16 findings with no test record** (F26b, F32, F34b, F40, F85, F90, F101b, F102b, F111b, F134b, F135b, F142, F174b, F176b, F199b, F218b — all `b`-suffix sub-findings or pre-convention files, none cited in this rubric), `legacy_script` **51 → 47**, gate records **58 → 63**. The grade does not move to `QUANT`, because the arming pass surfaced a second and larger instance of the same disease: **8 gate records whose entry cannot go red at all** (Amendment 1), two of which this rubric cites |

---

## Amendment 1 — 2026-08-07 - 17:05: gap #2 executed, and it found a bigger hole

Ben asked for the phantom gate records to be found and fixed. Both happened the same day this
report named them, so the H8 row above is a snapshot of a state that no longer exists and is
annotated rather than rewritten.

**The sweep.** Every `findings/F*.md` header field naming a test record was parsed and matched
against `tests/registry/*.yaml`. Exactly five findings were wrong, the five this report named:
`F298-casimir-ladder`, `F299-casimir-scaling` and `F303-coupling-normalisation` held
`kind: legacy_script`, `tier: battery` stubs; `F300-lattice-thermodynamics` did not exist under
that id at all (a stub named `F300-thermodynamics` stood in its place); `F301-boost-covariance-defect`
had no record of any kind. Nothing else in 298 findings was mis-declared.

**The fix.** All five are armed as `kind: assertion`, `tier: gate`, with `module:`, `entry:`,
`params:` and `expect:`, written through `gen_test_registry`'s own `build()`/`write()` so the next
regeneration preserves them (human fields win; only `evidence:` is refreshed — verified idempotent).
Each was then run through `casim test` and passes. **Every declared control was re-measured, and each
reddens exactly the checks its finding names and nothing else:**

| Record | Control | Reddens |
|---|---|---|
| F298-casimir-ladder | `tower=symmetric` | L2, L3 |
| F298-casimir-ladder | `n_max=3` | L2 |
| F299-casimir-scaling | `tower=kstring` | S2, S4b |
| F299-casimir-scaling | `beta=2.0` | S4 |
| F300-lattice-thermodynamics | `linear_control=True` | G10-3, G10-4, G10-5, G10-6 |
| F300-lattice-thermodynamics | `nonunitary_control=True` | G10-7, G10-9, G10-10 |
| F303-coupling-normalisation | `assume_three_bond_loop=True` | N3 |
| F303-coupling-normalisation | `scheme_residual=20.0` | N4 |
| F301-boost-covariance-defect | *(no parameter control exists)* | 30 asserts inside the entry; verified by perturbing `omega_branch` by $10^{-6}$ in-memory, which fires one |

Two by-products worth recording. `thermodynamics.check_g10`'s docstring listed G10-3/4/5 and G10-7 —
three checks short of what the controls actually redden; the finding had it right and the docstring
was corrected. And F301's record is honest that it has **no parameter control**: its six declared
controls are internal legs of the same run, which is weaker than the other four and is written into
the record rather than papered over.

**The bigger hole, found while arming F301.** `casim.tests.runner._interpret_return` maps an entry's
return value onto a verdict, and **a dict carrying no `passed`/`pass`/`ok`/`gate`/`all_pass` key
reads as PASS**. So a gate entry that returns measurements and contains no reachable `assert` or
`raise` always passes. Eight gate records are in that state:

| Record | Rubric row it supports |
|---|---|
| F291-dimension-selectors | **A1** (why 3+1) |
| F292-higher-multiples | A1, B2 |
| F282-inflaton-candidate-slowroll | K4, K8 |
| F283-elastic-lattice-excluded | K4 |
| F285-initial-condition-measure | K5, K12 |
| F286-second-scale-classification | K3, K12 |
| F295-tilt-is-an-anomalous-dimension | **K3** |
| F296-holographic-anomalous-dimension | **K3** |

That is the whole primordial arc plus the dimensionality pair — and it means A1's and K3's evidence
is currently unfalsifiable *in the mechanical sense*, not merely under-controlled. Fixing them is not
a registry edit: each needs pass criteria taken from the finding that owns it, which is physics work
and is left for Ben rather than guessed at here.

**The guard.** `tools/check_finding_records.py`, wired into `make gate` and `make records`, asserts
both classes: (1) every record a finding declares exists, at the tier it claims; (2) the number of
cannot-fail gate entries is a **ratchet** at ceiling 8 — it may fall, never rise. It is a ratchet
rather than a hard failure because turning the gate red on eight pre-existing findings would only
train people to skip the check. Verified with two negative controls: demoting the F300 record back to
a `legacy_script`/`battery` stub — literally this morning's state — turns it red on exactly that
record, and pointing F300's finding at a nonexistent id turns it red on exactly that; restoring
either returns it green. The ratchet was also seen to fire, at ceiling 7 against a measured 8, before
the ceiling was set.

**Why nothing caught this.** `check_test_registry` validates records against their schema and a stub
is a valid record; `check_module_registry` checks modules have rows and they did; `gen_test_registry`
keys existing records by **path**, so a record that was never written is silently scaffolded as a
`legacy_script` and the session reads a green checker as confirmation. The one artifact that knew the
truth was the finding's own header field, and nothing read it. It does now.

## Amendment 2 — 2026-08-07 - 17:45: gap #3 executed, check soundness is a gate

Written by a session running concurrently with Amendment 1 and reconciled against it; the collision
it caused is recorded at the end.

**What changed.** Ranking item **#3** is built at the scope it asked for — *"a declared-and-verified
perturbation [as] a D9 requirement for `kind: assertion` records, retro-fitted to the 58 gate-tier
records rather than all 400."*

**The diagnosis was right, and narrower than it looked.** The norm was not missing: ten gate records
already declared their controls, in prose, in `notes:`. F300 — *"`--param linear_control=True` reds
G10-3/4/5/6"*. F304 — *"FOUR declared controls, each verified red on its own leg."* What was missing is
that no machine read those sentences, so the claim was re-made by hand every session and the instrument
counts came back bit-identical. A `control:` block is now that sentence as data (`params:` / `reds:` /
`reason:` / `only:`), `casim test --control` applies the perturbation and judges it **on legs** against
an unperturbed baseline, and `make gate` checks statically that every control carries a verified verdict
at the current code **fingerprint**.

| | |
|---|---:|
| gate-tier `kind: assertion` records | 61 |
| declaring a control | **11** (10 strong, 1 weak) |
| `gate_assertion_no_control` — fifth ratchet key, → 0 | **50** |
| controls declared | **25** |
| verified RED at the current fingerprint | **25 of 25** |

**H2 stated as this report would state it.** Register level unchanged; `falsifier_unset` is still
226/226, which is the register half and a different object. Instrument level: `unfalsifiable 72 /
no_assert 233 / import_time 328` are **still bit-identical** — those three are not what gap #3 asked to
move, and re-baselining them to look like progress is the laundering this report spent two pages
objecting to. What is new is a fifth key, and it is the first of the five that measures whether a check
*can* fail rather than whether a mechanism is present. **H2 stays `PARTIAL`**: the mechanism exists and
11 of 61 records are behind it. That is a named residual, not a closure.

**Two of the ten prose declarations were wrong, and the measurement is what said so.** F290's
`mass=0.0` reddens **C3, C3b and C3d** — its module docstring said C3. F281's `coupling=nonminimal`
reddens **M1a, M1b and M1f** — its notes said M1a/M1b. Both surfaced as `SPILL` and both were widened
to the measured set. This is the correction Amendment 1 also made by hand against `check_g10`'s
docstring; the difference is that it is now the tool's job.

**Independent confirmation of Amendment 1.** The eight control rows in Amendment 1's table were
re-derived here from the registry by a different mechanism, and every one agrees — L2/L3, L2, S2/S4b,
S4, G10-3/4/5/6, G10-7/9/10, N3, N4. Two hand measurements agreeing is worth more than either alone,
and neither pass knew the other was running.

**The two guards are complementary, not duplicates.** Amendment 1's `check_finding_records.py` counts
gate entries that **cannot fail at all** (ceiling 8, from `_interpret_return` scoring a verdict-free
dict as PASS). This one asks, of the entries that *can*, whether they actually do **where they say they
do**. Neither subsumes the other: an entry can have a reachable failure path and still have no
demonstrated perturbation that reaches it, which is what F22 was for months.

**The teeth were tested, not asserted.** A one-line edit to `casimir_ladder.py` turns the gate red
naming `F298-casimir-ladder#control0` and `#control1` (exit 1); restoring returns exit 0.
`record_fingerprint` covers `runner.py` itself, because the first re-run replayed four stale `INVALID`
verdicts **because the checker had been fixed and the fingerprint had not noticed** — item #2's disease
one level up again, caught inside the hour. And the layer carries its own negative control:
`test_a_noop_perturbation_is_reported_as_leak` feeds the checker a switch that changes nothing, because
shipping a soundness gate with no demonstrated failure mode would have reproduced this report's item #2
a third time, in the file whose subject is that defect.

**The collision, recorded rather than tidied.** This session staged `tools/run_gate.py` before 17:05
and committed its edited copy at ~17:20, which **dropped Amendment 1's
`check_finding_records.py` gate line** — written 15 minutes earlier, in the file that enforces
everything else. It was noticed only because this session went back to read Amendment 1, and is
restored (with `records` added to `.PHONY`, which was also missing). Both sessions held a `session-claims`
entry; neither collided on a finding number, a test id or a physics module. The mechanism that failed
is the one CLAUDE.md does *not* cover: **shared infrastructure files edited from a stale read.**
`run_gate.py`, `Makefile`, `audit_tests.py` and `tests/registry/*.yaml` are the four both passes
touched. The concurrency protocol reserves numbers and sectors; it says nothing about the gate wiring,
and this is the second time in two days that the tree's own enforcement layer has been the casualty.

**What this does not close.** The 50 records still without a control — the ratchet's job, and a retrofit
pass. `make control-todo` prints the worklist with each entry point's existing keyword arguments;
several already have a `*_control` switch written and never exercised from the registry, which is the
same shape as the prose-only declarations this pass converted.

## Amendment 3 — 2026-08-08 - 10:20: three of the eight cannot-fail records could always fail

Correction to **Amendment 1**, found while starting the bucket-C work it scoped, and verified three
ways before anything was changed.

**The claim.** Amendment 1 reported *"8 gate records whose entry cannot go red at all"*, and concluded
that **A1's and K3's evidence is unfalsifiable in the mechanical sense**. The list was
F282, F283, F285, F286, F291, F292, F295, F296.

**Three of them hold 41, 39 and 30 reachable asserts.** F282 (41), F291 (39) and F292 (30). They can
fail, and always could. The detector was right about the rule and wrong about the reach:
`_reachable_raises` walks the call graph from the entry through `ast.Call` nodes, and these three
entries do not *name* their checks —

```python
for name, fn in CHECKS:      # CHECKS = (("A1_...", check_A1_...), ...)
    out[name] = fn()         # the only Call node is on a loop variable
```

— so the walk sees one call to something called `fn`, finds it in no function table, and returns zero.
A **dispatch table** defeats a call-graph walk. Nothing about the physics was involved.

**Verified empirically, not by reading the AST.** Each was run untouched (PASS), then with one
dependency corrupted: F291 with a wrong `S1_and_S2`, F292 with a deliberately non-Clifford gamma,
F282 through its own `CHECKS` table. All three raised `AssertionError`, i.e. the record goes **RED**.

**The fix** is six lines in `_reachable_raises`: a module-level binding whose value mentions functions
defined in the same module is a dispatch table, and referencing it by name makes its members
reachable. Measured count **8 → 5**, ceiling lowered to 5 with `--ratchet-update`.

**So bucket C is five records, and all five are cosmology:** F283, F285, F286, F295, F296. Those are
genuine — zero asserts and zero raises in the whole module, 35 floats and 14 prose strings in F283's
case, with fields named `verdict` and `answer_to_ben` holding paragraphs. They still need pass criteria
taken from the findings that own them, which is still physics work and still Ben's.

**What this changes in the grades.** **A1's evidence is not mechanically unfalsifiable** — F291 and
F292 are its support and both assert throughout. Amendment 1's sentence should be read as applying to
**K3, K5, K12 and K4's F283 leg only**. The primordial arc keeps the finding; the dimensionality pair
does not.

**F291 and F292 are now armed** (Ben's call, this session), with two declared controls each, all four
verified RED:

| Record | Control | What it establishes |
|---|---|---|
| F291 | `cell_dim=4` | the internal 3 comes from the s = 2 cell, not from arithmetic |
| F291 | `d_scan_max=3` | an upper bound at 3 is unevidenced unless the scan reaches d ≥ 4 |
| F292 | `clifford_D_max=2` | a parity claim needs both parities in the scan |
| F292 | `n_blocks_max=1` | at n = 1 there is no reducible case to collapse |

All four are the **F298 idiom** — *a scan that cannot see the failure cannot claim it* — and all four
use the no-`reds:` verdict-flip form, because these two drivers assert rather than emitting a `checks`
list. Per-leg attribution would need the checks-list conversion and is optional for records that
already fail.

**One by-product worth recording, because it is the checker earning its keep.** The first draft of
F291's `cell_dim` control raised `ValueError` — `max_anticommuting_traceless_hermitian` refuses any
cell but s = 2 — and `casim test --control` scored it **INVALID**, *"the perturbed run CRASHED rather
than failing its checks."* That is the correct verdict and it caught a control that would otherwise
have been banked as sound on the strength of an exception. It is now caught and asserted on.

**Counts after this amendment:** 61 gate-tier assertions, **13** with a declared control (12 strong,
1 weak), **29 controls all verified RED**, `gate_assertion_no_control` **48**, cannot-fail **5**.

## Amendment 4 — 2026-08-11 - 17:35: gap #4 executed, and the term everyone expected to cancel does not

**F309** (`src/casim/engine/interactions/thermodynamics_gstar.py`, gate record
`F309-gstar-model-content`, 14/14, two controls verified red) closes gap #4 and F300's next step
#1. Both **K2** and **G10** lose the degree-of-freedom import.

**The technical result is not the one the gap was written expecting.** F300 §7.2 named the blocker
as "the fermionic BZ sums **with the branch-odd term handled**", and the natural reading — the term
the paired photon cancels, whose angular mean is zero by parity — is that handling it means
watching it drop out. It does not. A single BCC Weyl branch carries
$\omega^\pm=c|\mathbf k|[1\mp b|\mathbf k|-a|\mathbf k|^2]$ with $b=\hat n_x\hat n_y\hat n_z/\sqrt3$;
$b$ is **linear** in $|\mathbf k|$, so its **square** is degree-3 homogeneous, exactly like the
anisotropic term, and a square neither cancels between branches nor averages to zero. It supplies
$3/7=42.86\,\%$ of the coefficient. $C_u^F=310\pi^2/441$, $C_w^F=124\pi^2/1323$, $C_s^F=31\pi^2/49$,
each exactly $31/4=7\times\tfrac{31}{28}$ times F300's photon value — 7 geometric, $31/28$ pure
statistics.

**Two things the photon alone could not show.** $C_u/C_w=15/2$ holds for fermions *and survives the
branch-odd deletion*, so F300's "parameter-free ratio" upgrades from a measured photon coincidence
to a degree-3 homogeneity theorem, independent of statistics and of the anisotropy. And the control
that proves it is the same one that reddens GS-3/4/5 — an invariance and a value distinguished by a
single perturbation, which is the shape gap #3's amendment argued for.

**On the content side the answer is a null, and the null is the result.** The model's 48 Weyl fields
are exactly branch-balanced (24 L / 24 R, imbalance 0), and the BBN-window content it *derives* is
the three-species bath F297 *assumed*: $g_*(10\ \text{MeV})=10.749339$, $g_{*s}\to3.909435$ on the
$T_\nu/T_\gamma$ that entropy conservation produces rather than imposes. What was implicit is now
priced: $\nu_R$ would add $+5.25$ (48.8 %), the muon residual is $9.2\times10^{-4}$, and the
**undetermined $E_g$ scalar mass acquires a new BBN-derived lower bound, $m_{E_g}>125.5$ MeV** —
assembling the sector produced a constraint the sector did not have, which is the third time this
pattern has held (F297, F300, now F309).

**The one non-null substitution, and the honest size of it.** Re-running K2 on the model's own
electron mass (F121, $0.51069$ MeV) moves $Y_p$ by $+1.080\times10^{-4}$ ($+0.032\sigma$) and D/H by
$+1.057\times10^{-4}$ relative ($+0.009\sigma$), both **toward** the data. Neither is evidence at
present precision; seeing it needs $\sigma(Y_p)\lesssim1.08\times10^{-4}$, a **31×** improvement on
Aver et al. 2021, and that number is quoted rather than left for a reader to work out.

**One new content-level disagreement with the Standard Model, labelled rather than published.**
Above the top threshold the model's $g_*$ is $105.75$ (heavy $E_g$) or $107.75$ (light) — the SM's
$106.75$ is **unavailable** to it, the difference being exactly the single physical Higgs scalar
traded for the two-component $E_g$ doublet. The carrying observable,
$\Omega_\text{GW}\propto g_*g_{*s}^{-4/3}$, moves $0.31\,\%$: below anything current or planned, so
it is recorded and **not** written as a claim-card falsifier (F300's discipline).

**A name collision recorded on the way past.** F59/F61 write $g_*$ for the *gravitating* Weyl-mode
count in the induced-Newton-constant prefactor and get 15 per first generation; this is the
*cosmological* relativistic degree-of-freedom count. Different quantities, different counting rules,
neither a correction to the other — flagged in F309 §7.8 and in the module docstring, because grep
finds both.

Claim cards **CL265** (the fermionic EoS, rolling up to CL260) and **CL266** (the derived content
and the one-dof high-T difference). Gap #4 is closed; gaps #1, #5(a)(b)(c) are untouched by this
work.

**Two pre-existing reds this run did not cause and did not fix**, both inherited from the F308
session and both named in its release note: `registry-entries` fails on
`['F305-bcc-rhombic-vertices', 'F307-action-consistent-d1']` (each declares an `entry:` *and*
carries pytest functions — "pick one contract"), and `audit_tests --ratchet` is $+1$ on
`unfalsifiable`/`no_assert` because `tests/findings/test_F308_refold_repaired.py` carries zero
asserts. F309's own test file carries five and declares its artifact; it is in neither delta.

## Method notes

**Graded from the indexes and ledgers alone:** most of C, E, G and the D ledger.
`findings-index.md`, the re-audited `open-derivations.md`, the exactness tally, `key-decisions.md`
and `Claims-and-Falsifiers-Summary.md` (rev 4) carry enough.

**Rows that required a finding file or the changelog rather than a ledger:** B7, B8, B10, D16, H5
(F299 and F303 both post-date the 2026-08-05 ledger re-audit, and the H1/H2 fork appears in no
ledger — `open-derivations.md`'s B10 row predates F299 and reads as if the empirical selector were
intact); G5 (the $m_n-m_p$ exclusion lives in F297 and in the previous report's K2 amendment, and
nothing propagated it to the hadron row); G1 (F314); A6 and A10 (the residual lists in F304 and F290,
which no index carries); H8 (read directly from `tests/registry/core.yaml` against the findings'
`**Test record:**` headers).

**This is itself a finding about the ledgers, and it is the mirror image of last report's.** The
previous sweep's complaint was staleness — `open-derivations.md` 50 findings behind. That is fixed.
The complaint this sweep has is different: the ledgers are current and **still cannot see the H1/H2
fork**, because it is not a target, a no-go or a posit — it is two adopted results that disagree.
There is no ledger row shape for "the tree contains a contradiction", and B8's, B10's and D16's
grades all now depend on one.

**Grades verified by spot-check** (the three I was least sure of):

1. **A6 `EXACT → PARTIAL`** — checked F304 directly, including §5. The proof is real and better than
   the amendment credited: the frame-function theorem is reproved here and one closed form
   $b_k=(-1)^k/\binom{k+d-2}{k}$ gives both halves of the dichotomy. But the finding's own
   "Remains" §3 is unambiguous: context-blindness is proved for the $U(1)$ wrap generator, and the
   $SU(2)_L$/$SU(3)_c$ commutators "are still not written out". Non-contextuality is one of the two
   Gleason premises, so this is a seam in the derivation, not in an application of it. The record
   `F304-born-rule-gleason` was run and **passes**. The fix went to the grade, not the citation.
2. **A10 `MACHINE → PARTIAL`** — checked F290. Its own residual 1 reads *"The clustering leg is 1-D
   and free-fermion… the statement has not been made for the interacting 3-D BCC theory, where
   cluster decomposition is the harder and more interesting claim."* The no-signalling half is
   machine-exact and the strict cone is a genuine CA-specific result, but the row is named for
   clustering and clustering is not established. Verified `F290-cluster-decomposition` passes.
3. **H8, and the four missing gate records** — checked by hand rather than trusted. `casim test
   --list --tier gate` returns 58 records and none is named `F300-lattice-thermodynamics`,
   `F298-casimir-ladder` (gate), `F299-casimir-scaling` (gate) or `F303-coupling-normalisation`
   (gate). `grep` finds records with three of those ids in `tests/registry/core.yaml`, all
   `kind: legacy_script`, `tier: battery`, `n_test_funcs: 0`, no `entry:`. `casim test --id
   F300-lattice-thermodynamics` returns *"no registry record matches that selection"* — the exact
   command `test_F300_thermodynamics.py`'s docstring instructs a reader to run. This is the defect
   F299 itself diagnosed in F298 on 2026-08-06 and then reproduced.

**Every F-number cited was checked to exist** (`findings/` plus `deprecated/findings/` plus the
F01–F15 bundle). F16–F19 resolve in `deprecated/findings/`, correctly — they were retired 2026-08-03.

**Citations to superseded findings, carried with their supersession:** F251, F258 (→ F277, S12 — B9's
number un-re-derived, flagged for the third time); F162 (→ F272, S11 — apparatus re-verified by F287,
route executed by F280); F165 (→ F279, S13 — conclusion retained, two steps retracted, code now
aligned); F62 (→ F64, S3 — sign convention still production code); F114 (→ F178, S4); F179 (→ F253,
S6); F65/F66/F67 (→ F69, S1 — and F302 corrects S1's `retained:` clause: what survives for W/Z/gluon
is the *Hermitian* bilinear, not the σ-transpose construction, which survives nowhere);
F155 (→ F277, S12); F270 (→ F271, S10); F21/F23/F25 (→ F306, S18); F20 (partial, S18);
F16–F19 (retired, S1/S16/S17).

**A numbering observation, not a defect.** The previous report recorded `max F306`; the index now
reports `max F314` with F314's changelog entry stamped **2026-08-04 - 17:20**, i.e. before that report
was written at 21:12. F314 is therefore a finding the previous sweep did not count or cite, and its
result (G1) is folded in here. The one-at-a-time allocator adopted 2026-08-05 - 09:30 makes this class
of confusion structurally impossible going forward; the 8-number backlog (305, 307–313) drains as
ordinary work lands.

**What this run could not verify.** The `registry-entries` gate record (ran past 43 s twice without
completing and without a failure appearing). Whether F277's refold fix left B9's $\Delta\alpha(M_Z)$
re-blessed — third consecutive report. Whether the 10 `candidate` baselines are regressions or
accepted physics changes — third consecutive report. Whether the 62 manifest-linked-but-undeclared
artifacts are the C7 arming to-do the checker calls them (57 last report). Whether the four missing
gate records were written and later clobbered by `gen_test_registry.py` or never written at all — the
working tree carries one large uncommitted diff, so git cannot answer it; only the current state is
reported above.

## Amendment 8 — 2026-08-17 - 11:30 — row B11 moves, and its evidence was the wrong theta

**F321** (`colour_theta.py`, record `F321-strong-cp`, 20/20, 3/3 controls CONTROL over **disjoint** red sets).

**The accounting first, because it is the larger error.** B11 read *"tree $3.3\times10^{-16}$; loops open"* for three consecutive reports, citing F53. F53's P5 measures the **F27 complex-mass phase**, and F53's Remaining section says, in its own words, that strong CP *"is a separate phase in the gluon sector (F43), untouched here"*. So the row was not "tree closed, loops open" — it had no tree-level evidence for $\theta_\text{QCD}$ at all, and the loop question was stacked on a number about a different quantity. This is the third row in three amendments whose residual turned out to be an accounting statement rather than a physics one (A11, B12, now B11), and the pattern is worth naming: **a residual that has not moved in three reports is more likely mis-stated than hard.**

**The physics.** The identity that does the work was available all along and unused here: in Euclidean signature the $\theta$-term is the *unique purely imaginary* gauge invariant, so reality of the action **is** $\theta=0$. And reality is not a convention — the rule's 20 oriented minimal rhombi are closed under reversal, so $\sum\operatorname{Tr}U=2\operatorname{Re}\sum\operatorname{Tr}U$ configuration by configuration. Measured: $\operatorname{Im}S=1.2\times10^{-14}$ at 99.7 % disorder; $S$ invariant under $U\to U^*$ while the one-sense loop functional is odd under it at literal `0.0`; every position-space vertex coefficient real at literal `0.0` at 2, 3 and 4 legs with colour indices sampled. The loop claim is then a **closure property**, not a diagram census: functions obeying $V(-k)=\overline{V(k)}$ are closed under products and under $q\to-q$ symmetric loop integration, so $\Gamma$ obeys it at every order.

**What it cost, and what it did not buy.** It does not solve the strong CP problem and does not predict $\bar\theta$ — CL279 is a deliberate `non_claim` card saying so, because "the model has no $\theta$-term" reads at a glance like "the model solves strong CP". $\bar\theta=\theta+\arg\det M_q$; the second term is E6/E7 and open. Ledger **E9** closes in exactly one sense: parameter #19 stops being an *independent* input and becomes a function of the quark mass texture.

**Two named gaps, neither papered over.** (1) `lpt_bcc_vertex`'s action fork is still open, so the argument was run on the other branch too — the F26 even law is P-even at literal `0.0`, the retained chiral law is not (1.98) — and "survives both branches" is weaker than "derived on the settled branch". (2) Non-perturbative $\theta$-sectors are not addressed by either the all-orders or the configuration-wise statement.

**And one leg that was measured and thrown away.** The first draft had P-oddness of the clover $Q$ as load-bearing. It is **false at finite $a$**: relative defect 0.42–0.83, and it does **not** fall as the field weakens, with no orientation-permutation-with-sign-and-translation match either. So "$\mathbf E\cdot\mathbf B$ is P-odd" is used as a continuum statement only and every load-bearing leg rests on reality / $U\to U^*$. F321 §7 records it rather than quietly dropping it.

**Control 2 found a real defect in this finding's own first draft** — the strongest evidence yet that the D9/H2 layer pays for itself. The original vertex probe sampled momenta at `lpt_bcc_vertex.terms`'s hardcoded colour assignment $[T^0,T^1,T^2]$ and stayed **green** under the one-sense control, while the one-sense action's imaginary part was a plainly visible $O(A^3)$. The imaginary part lives in the antisymmetric $f^{abc}$ structure, which a fixed-index probe cannot see. Caught by the mechanism, not by review.

## Amendment 9 — 2026-08-17 - 21:55 — row B9 re-derived, and gap #5(a) closes on an accounting error

**F322** (`running_alpha_lattice_bound.py`, record `F322-b9-running-rederived`, 6/6, 2/2 controls `CONTROL` over **disjoint** red sets). Claim card **CL280**, `contingent`.

**The accounting first, because it is again the larger error.** Gap #5(a) called this *"the cheapest — one number, one re-run"* and carried it three times. The re-run was cheap; the premise was wrong. `leptonic_running`'s call closure is $\{$`_dalpha_lepton`$\}$ — `_fermion_B` and `_K_lat`, the refolded path, are not in it. Measured rather than argued: replacing the kernel with $7.3\,K_\text{lat}+0.5$ leaves $\Delta\alpha_\ell(M_Z)=0.03142092800460496$ **bitwise** identical. F277 §6 had already said "F251 5/5 unchanged"; what was missing was the reason, and the reason is that Pi4 is a closed form in $\ln(s/m_\ell^2)$ that never enters the loop integrand. **That is four consecutive amendments** — A11, B12, B11, B9 — in which a residual immobile for three reports turned out to be mis-stated rather than hard. The pattern named in Amendment 8 now has enough instances to be a standing prior on this document, not an observation about one row.

**The physics the flag should have asked, and the answer is better than "unchanged".** Because $B=-\Pi$ and the running is the *subtracted* $\Delta\alpha(s)=\Pi(0)-\Pi(s)$, a $q$-independent constant in $\Pi$ cancels identically. So F251's Pi3 $q$-flatness is not merely "the log coefficient is propagator-independent" — it **is** invariance of $\Delta\alpha$ itself, and Pi3's measured non-flatness is an error bar on the model's $\Delta\alpha$ prediction. The conversion is exact and model-internal, $\delta(\Delta\alpha)=4\pi\alpha\,\delta B$, read off the module's own $b_0^\text{QED}=4/3$. (A fitted normalisation was tried and **rejected**: at finite $n$ the midpoint cube cannot resolve $\ln(1/Q^2)$ below $Q\sim\pi/n$, so the fit is still $62\%$ low at $n{=}28$. The subtracted $\Delta$ is where the grid artifacts cancel; the normalisation has to come from the algebra.)

Measured, with the $n$-dependence as the discriminator — grid noise shrinks, a residual log does not:

| | bound on $\delta(\Delta\alpha)$ at $n{=}28$ | $\times$ the $7.71\times10^{-5}$ PDG shortfall | fraction of $\Delta\alpha$ | ratio $n{=}28/n{=}20$ |
|---|---:|---:|---:|---:|
| post-F277 | $6.77\times10^{-6}$ | $\mathbf{0.088}$ | $2.2\times10^{-4}$ | $\mathbf{0.398}$ (falling) |
| refold restored | $1.41\times10^{-2}$ | $\mathbf{183}$ | $0.448$ | $\mathbf{0.965}$ ($n$-flat) |

**So F277 did not change B9's number; it created its warrant.** Before it, "matches PDG to $0.24\%$" carried a lattice uncertainty roughly $190\times$ larger than the agreement claimed — the number was right and unwarranted at once. That is why the flag was worth carrying even though its literal form was false, and it is the more useful reading of the third-consecutive-report entry than the one this document kept making.

**And the shortfall is now attributed rather than tolerated.** It is two-loop, and the coefficient has been in the tree since 2026-07-23: F261's $b_1=1$ is sympy-exact and was never fed into the running. The two-loop leading log $\alpha^2L_\ell/(4\pi^2)$ per lepton closes $79.8\%$ of it with the correct sign — $\Delta\alpha_\ell(M_Z)=0.03148241$ vs PDG $0.031498$, i.e. $0.2447\%\to\mathbf{0.0495\%}$, and $1/\alpha(M_Z)|_\text{lep}$ $132.7302\to132.7218$. The two-loop non-log constant and three loops are **not** derived; they are the residual $1.559\times10^{-5}$.

**B9's EW leg was graded on the wrong finding too.** The row cited F115, whose CM2 anchored the bare angle at the Planck scale and overshot by $-74\%$; F138/F231 superseded that reading in June and July. F138's matching at $\mu_\star=4\pi v=3094.09$ GeV is reproduced exactly here: $\sin^2\bar\theta_W(M_Z)=0.2317341$, $+0.222\%$ vs PDG $\overline{\text{MS}}$. Then the measurement nobody had made — that running takes $\alpha_\text{em}(M_Z)$ as an **input**, and on the model's own leptonic-only $\alpha$ the residual doubles to $+0.450\%$ (factor $2.02$; the missing $3.795$ in $\alpha^{-1}$ is the hadronic piece). **B9's two halves are not independent — they share one input, and half of the EW leg's precision is owed to a number the model does not derive.** B9's real residual is therefore row **G3**, which is where it should have been pointing for three reports.

**Gap #5 status after this amendment:** (a) **closed**. (b) the 10 `candidate` baselines and (c) K9's two $\Lambda$ pictures are untouched by this session and remain on their fourth report.

## Amendment 10 — 2026-08-17 - 23:30 — F115 enters the ledger 67 days late, and the mechanism that let that happen is closed

**Ledger record S20-F115-weinberg-gap-account-replaced-by-4piv-matching** (`partially_superseded`, by F138 and F231). Banner stamped. New gate check `tools/check_superseded_citations.py`, wired into `make gate` and `make citations`, with two tests in `tests/casim/test_supersession_ledger.py` (record `supersession-ledger`, now 51 passed).

**What was wrong.** Amendment 9 recorded that row B9's electroweak leg had been graded on F115 while F138 and F231 superseded that reading in June and July. It did not ask why nothing caught it. The answer is that **F115 was never in the supersession ledger at all** — so `apply_supersession_banners.py` stamped nothing, `test_no_orphan_banners` had nothing to find, and `check_claims.py` rule 4 could not fire either, because that rule deliberately covers only a `live` card resting on *wholly* superseded ground and F115's CM1/CM3/CM4 are alive. A **partial supersession cited without its replacement had no owner anywhere in the tree.**

**What is dead and what is not.** Only CM2's *conclusion* — that the +12% gap is "a low-scale (~few-TeV) matching offset" identified by where the measured SM trajectory happens to cross $\tfrac14$. F138 derives the scale instead ($\mu_\star=4\pi v=3094$ GeV, forced by hypercharge having no lattice kinetic term) and closes the gap to $+0.22\%$; F231 makes F49's $\tfrac29$ the on-shell face via the $8/9$ bridge. **CM1 is untouched and is still B9's correct citation** ($e=g/2$, $g'=g/\sqrt3$, $g_Z=2g/\sqrt3$ as exact rationals — one EW magnitude, not three), as are CM3's rotor lock $g_s^2\chi=\tfrac14$ and CM4's $e^6$ notation no-go. CM2's *negative* — that Planck-anchored running overshoots by $-74\%$ — is retained and load-bearing, because it is why a matching interpretation is needed at all; F138 says so itself. CM2b's measured $3.4$–$3.7$ TeV crossing is **demoted** to a consistency check on F138's derived $3.094$ TeV. No number moves and no test changes verdict.

**The mechanism.** A supersession now has two directions, and the ledger's `about:` block says so. Inward: `make stamp`, unchanged. Outward: `make citations` requires every markdown table row in the **current** completeness report and in `open-derivations.md`, and every claim card's front matter, to name a replacement from the record's `by:` list alongside the superseded finding — or to say `superseded` / name the ledger id in the same row. **The unit is one table row**, because an acknowledgement 400 lines from the row that gets it wrong is exactly how B9 read. Older completeness reports are excluded by design: they are frozen records of what a past sweep concluded, and rewriting one to satisfy a check invented afterwards would falsify the audit trail.

**What it found immediately** — five live violations in the current documents, all now cleared: C2 cited F165 without F279 (S13); G8 cited F258 without F277 (S12); `open-derivations` cited F155 without F277, F67 without F69 (S1), and **F115 without F138/F231** — the same error as B9, still live in a second document. Claim cards carry a counted, falling ceiling of **19** (down from 20 — CL022 now declares S20 and states that it cites F115 for CM3 only); most are `open` or `withdrawn` cards where the citation is a historical record rather than a live grade.

**Verified fires, not just passes.** The check's negative control is the B9 row itself: with the replacement removed from `open-derivations.md` it goes red on that exact line, and green again when restored. Three matcher cases are pinned in `test_the_citation_matcher_actually_fires` — bare citation fires, replacement named clears, explicit marker clears.

## Amendment 11 — 2026-08-17 - 21:50 — row B7's d=4 leg was never on the model's lattice, and the anisotropy is derived

*Ordering note: Amendment 10 carries a later wall-clock stamp (23:30) than this one despite landing
first. The device clock read 21:50 when this was written; the stamps are hand-entered and 10 preceded
11 in the file. Nothing depends on the difference.*

**Ledger record `S21-F94-hypercubic-action-not-the-model-lattice`** (`partially_superseded`, by F323
and F265). Banner stamped. `CL087` **narrowed** — it rested on F94 alone, so `check_claims.py` rule 4
fired, correctly. **And Amendment 10's brand-new `make citations` check caught this row within the
hour**: B7 cited F94 without naming a replacement, which is exactly the failure mode Amendment 10 was
built for, on a supersession created ninety minutes after it landed. That is the outward direction
working on its first real case rather than on its self-test.

**What was wrong, and it is not a number.** Every 3+1D confinement statement in the tree ran on
`forks/gauge/lgt_fork_A_mc.py` — a **simple-hypercubic** Wilson action, `D=4` cubic, "by convention
the LAST lattice axis is Euclidean time". F265 proved in July that this construction is *blind*: it
has an exact kernel that leaves one of the four $\langle111\rangle$ link axes completely free, so
$S_\text{SC}\equiv0$ to round-off on configurations where the genuine BCC Wilson density is $\approx1$,
and asymptotically it misses **1/3 of the curvature-carrying link content**. F265 named the remedy in
its own text — *"the Monte-Carlo actions (F94 4D cubic, F146 3D cubic) … to be rebuilt on the BCC
lattice"* — and nothing was built for seven weeks, so F94 remained B7's only $d=4$ leg. **The reason
this was invisible is the reason it matters:** both actions have the *same classical continuum limit*,
so F94's absolute-normalisation and strong-coupling anchors (FA4, FA5) could pass on a blind action,
and their passing was never evidence the ensemble was right.

**What survives, because `fully_superseded` would be false.** F94's engine certificates FA1–FA3 are
properties of the Cabibbo–Marinari sampler, not of its lattice; CMP2's bridge
$v_*=\sqrt{\sigma_A/2\pi}$ is exact at $10^{-16}$ and F311 leg B re-verified it at $1.2\times10^{-16}$
over five seeds; the Lüscher–Weisz estimator and its 84× variance reduction stand. So does the
qualitative statement that the potential rises — F323's BCC run also finds a positive Creutz ratio.
F311's separate adjudication is **not** re-homed: `FA_vs_FC_comparison.json`'s drift is an *undeclared
input* (`_measure_sigma_A` reads `lgt_confinement.json`), explicitly not a supersession, and its
`clears_by` action is still open.

**The anisotropy is now derived, and the previous session's guess about it was wrong.** `xi = a_s/a_t`
was carried as a flagged convention ($\beta_t=\beta_s$). Two separate statements close it, and the
distinction is the content: **F313's primitivity** (no local half-tick, so the tick has no root in the
local homogeneous algebra) is what licenses a *fixed* $a_t$ rather than a refinable one — it supplies
no value, and the earlier speculation that it *fixes* $a_t$ is withdrawn. **Isotropy of the weak-field
limit** supplies the value, via two independent exact closure identities of the BCC geometry
($\sum_p m_pm_p^{\mathsf T}=4I$ over the 6 $\langle110\rangle$ rhombus half-normals, and
$\sum_a aa^{\mathsf T}=4I$ over the 4 $\langle111\rangle$ axes):
$\beta_t/\beta_s=4\lambda^2/a_t^2$, then $a_t=c_\text{lat}\lambda\sqrt3$ from the emergent light cone,
giving $\beta_t/\beta_s=4/(3c_\text{lat}^2)=\mathbf4$ and $\xi=1/c_\text{lat}=\sqrt3$ exactly. **The
new number is the $4/3$:** the hypercubic relation is $\beta_t/\beta_s=\xi^2$ and the BCC answer is
$(4/3)\xi^2$, so the textbook substitution would have been wrong by a third. Measured as well as
derived — a constant-$F$ abelian configuration gives $4-g^2/16+O(g^4)$, the truncation coefficient
holding at exactly $1/16$ over a factor two in $g$, and one Richardson step lands on
$3.99999999908$. Consistency, not a new number: $\xi=1/c_\text{lat}$ reproduces **F284's $r$** by a
route that never mentions cosmology, and $a_t=\lambda$ exactly in integer units, so the whole
anisotropy is the $\langle111\rangle$ hop length.

**F299's $d=4$ successor ran, and two engine gaps were what had blocked it** — not physics. Its three
character polynomials had **never been applied to a loop matrix** anywhere in the tree (they lived in
`mc_reach`'s docstring as torus-eigenvalue expressions, verified against the same Jacobi–Trudi
determinant that produced them), and **no function returned the traces to evaluate them**
(`wilson_loop_planar` ends on `np.real(np.trace(acc))/3` averaged over sites; `polyakov_loop_field`
returns $\operatorname{Tr}W$ only). Both are now supplied, and the polynomials are cross-checked
against **explicit representation matrices** — $\mathrm{Sym}^2$/$\mathrm{Sym}^3$ by symmetric-subspace
isometry and $\mathrm{Ad}(U)_{ab}=2\operatorname{tr}(T_aUT_bU^\dagger)$ — at $\le4.6\times10^{-16}$,
which is a check the tree had never run and which self-consistency against the determinant could not
have caught. First measurement at $\beta_s=5.9$ on $6^4$ with **3 configurations**:
$\sigma_6/\sigma_3=2.466$, $\sigma_8/\sigma_3=2.224$, $\sigma_{10}/\sigma_3=4.378$ at $R\times T=2\times2$
against the exact $5/2$, $9/4$, $9/2$ — within a few percent — with all three falling **below** the
Casimir line at $3\times3$, most steeply for the decuplet. **That is labelled preliminary and is not a
claim**: the $2\times3$ versus $3\times2$ asymmetry alone exceeds the effect being read at $3\times3$.

**B7's grade does not move, and should not.** The row's residual is *"3+1D is constructed, not
proven"*, and it is unmoved: a proof needs a lattice-wide Euclidean transfer matrix with positivity,
and `reflection positiv`, `Osterwalder`, `Schrader` and `cluster expansion` return **zero hits
repo-wide**. What changed is that the construction is now on the right lattice with a derived
anisotropy, which is a precondition for a proof rather than a substitute for one. Record
`gauge-bcc-mc-d4` 28/28 with **5/5 controls `CONTROL`**; battery `run-bcc-confinement-d4`.

**One correction to this document, found in passing.** Row B7 and row H8 both carry *"F299's claimed
gate record does not exist"*. It was **armed 2026-08-07**, the day after F299 landed, and passes with
both controls declared. H8's clause is stale and B7's copy of it is removed here; H8 itself is left to
the next sweep, which owns that row.
