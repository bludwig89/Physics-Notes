# Completeness overview — 2026-08-04 - 21:12

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: full sweep, 74 rows (blocks A, B, C, E, K, G, H) plus the 28-row parameter ledger (D).
Previous benchmark: `docs/status/completeness-2026-08-02.md` (as amended through 18:20 that day).*

**Health probe (what actually ran).**

`make indexes-check` **green** — all seven generated indexes current; max **F306**, 272 distinct
labels across 283 files, 0 duplicate finding numbers, 34 declared gaps (0 undeclared), exactness
header 0 findings behind. One non-defect noted by the checker itself: 57 records have
manifest-linked artifacts they do not declare (C7 arming to-do). `make registry` **green** — 385
records over 376 test files, all valid (D9); kinds `assertion` 114 / `result_dump` 221 /
`scenario` 3 / `legacy_script` 47; **gate tier 47**; baselines 7 `stale_by_design`, **10
`candidate` (drift still FAILS by design)**. `make numerics` **green** — 254 physics modules
scanned, 0 direct `np.fft` transform calls, 163 files importing numpy/scipy (was 165), ratchet
intact. `make health` — 376 files, no-assert 233, **UNFALSIFIABLE 72** (no assert *and* no result
artifact: cannot fail), import-time physics 328, 0 unregistered files. Exactness tally: **exact
156 / machine 195 / quantitative 184**, coverage **535 of 535 (100%)** across 411 artifacts.
Module registry: **189 modules, 51 channel-driven (27.0%)**, 24 unreferenced, 17 standalone;
statuses live 129 / `fork_live` 25 / `fork_unclaimed` 23 / `partial` 11 / **`dead_candidate` 1**.

> **Gate: NOT VERIFIED GREEN THIS RUN, and one record is confirmed red.** `make gate` needs
> ~2 min against a ~45 s sandbox ceiling and a backgrounded run dies with its bash call. Two
> records were run individually: **`supersession-ledger` FAILS** — `S14-P5.1-live-display-retired`
> carries a malformed decision id `P5.1`; this was flagged on 2026-08-03 by the F302 session, again
> on 2026-08-04 by the triage pass and again by the F306 session, and it is **still red two days
> later**. `registry-integrity` also returned non-zero, but only with
> `ModuleNotFoundError: No module named 'pytest'` under the vendored activation — an environment
> artifact of this sandbox, not a physics failure. **Ben should run `make gate` once end to end**;
> the three `kind: scenario` physics gates were not exercised this run.

---

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A Foundations (12) | 3 | 1 | 0 | 5 | 0 | 0 | 0 | 0 | 3 | 0 |
| B Gauge (12) | 4 | 0 | 2 | 5 | 0 | 0 | 0 | 0 | 1 | 0 |
| C Matter (7) | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| E Gravity (13) | 3 | 1 | 4 | 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| K Cosmology (12) | 0 | 0 | 1 | 4 | 0 | 0 | 2 | 3 | 2 | 0 |
| G Emergent (10) | 1 | 1 | 5 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| H Integrity (8) | 0 | 0 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total (74)** | **13** | **3** | **13** | **31** | **0** | **1** | **2** | **4** | **7** | **0** |

*Every cell is counted from the grade column of the block's own table below; row sums equal the
block sizes (12, 12, 7, 13, 12, 10, 8 = 74). This is the generation method the previous run's
correction note asked for.*

**Parameter ledger: 6 of 28 derived, 2 partial, 6 fitted or free input, 14 open or absent** —
unchanged from 2026-08-02. No quark-mass, CKM, $\alpha$, $v$, $m_H$ or $\Lambda$ work landed in
the two days.

**Two ABSENT rows closed; three integrity rows fell.** The physics moved forward — A1 (why 3+1)
and E10 (singularity resolution) both leave `ABSENT` — while H2, H4 and H6 each drop
`QUANT → PARTIAL` on evidence produced by this project's own new review instrument. That is the
report: the model got slightly more complete and measurably less well-evidenced in the same
48 hours, and the second fact is the larger one.

---

## The five things most worth building next

Ranked by (load-bearing × distance from closure).

### 1. The review-debt base rate: 10 findings reviewed, 0 clean confirmations

**What.** `/review-finding` ran 11 times between 2026-08-03 and 2026-08-04 (`docs/reviews/`).
Verdicts: F01–F15 bundle *physics CONFIRMED / artifact UNDER-EVIDENCED*; **F16 OVERSTATED, F17
OVERSTATED, F18 OVERSTATED, F19 CIRCULAR** (all four retired to `deprecated/findings/`);
**F20 OVERSTATED, F21 REFUTED, F22 OVERSTATED, F23 OVERSTATED, F24 CONFIRMED-NARROWER, F25
OVERSTATED.** Not one individually-reviewed finding survived unchanged. **262 findings have never
been through this instrument**, and the rubric above cites roughly 130 of them.

**Why it matters.** It is not the corrections themselves — every one improved the tree, and F306
turned the worst of them into a *better* result than the original claim (the composite-photon curl
closes at $O(k^3)$, not $O(k)$). It is the **shape** of the defect, which was the same in almost
every case: **a check that could not fail.** F22 set `beta_LV_sym = (1-rho)/2` and then simplified
`rho - (1 - 2*beta_LV_sym)` — identically zero for any expression, including $\rho=42$. F21's
self-check compared the harness to a constant produced by the same code path; F23's did the same;
F16's "all three forks resolve it" was a tautology because each fork was *defined* by setting the
quantity; F25's six test records covered a claim that cannot fail. The suite's own metric agrees:
**72 test files are UNFALSIFIABLE** — no assert *and* no result artifact.

**What blocks it.** Nothing structural. The instrument exists, works, and is cheap enough to have
cleared ten findings in two days.

**Smallest next step.** Stop reviewing in numerical order. F16–F25 are the oldest files in the
tree, written before the conventions existed, so the 10-for-10 rate is biased upward and should be
said so — but the fix is to spend the next reviews on **load-bearing** findings instead: the ones
this rubric cites most (F26, F27, F64, F79, F138, F175, F178), plus **F32**, the one file the
2026-08-04 triage found with zero citations and zero code references. A review of F64 or F175
tells us something about twenty rubric rows; a review of F26 tells us something about all of them.

### 2. Falsifier and check soundness as a gate, not a review by-product (H2)

**What.** There is no mechanism that asks whether a finding's own verification can fail. The
review series found six instances by hand; `make health` counts 72 candidates mechanically and
nothing acts on the number.

**Why it matters.** The previous report's closing line was *"the next sweep should check falsifier
soundness, not just grades"* — and the two days since supplied the evidence that it must. This is
also the row where the model's public standing is most exposed: `Claims-and-Falsifiers-Summary.md`
carries five thresholds, and F282's falsifier 5 had to be struck as *unable to fire*. A published
falsifier that cannot fire is worse than a wrong number, because it invites wasted work.

**What blocks it.** Nothing. F22's remediation already shows the pattern: it added a
`control_fails` leg that requires the same code path to go red under `rho_override="42"`.

**Smallest next step.** Make that leg a **D9 requirement** for `kind: assertion` records — a
record must declare a perturbation under which it fails, and `casim test` must verify it does.
`casim test --param k=v` already exists and is exactly the machinery needed. Start by retro-fitting
the 47 gate-tier records rather than all 385.

### 3. The strong-sector constant $d_1$ — prerequisite discharged, route now named

**What.** The one one-loop background-field lattice→V matching constant,
$\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$. **E3 = Q1 = Q2 all reduce to it**
(open-derivations sector tally). It owns the register's largest live tension:
$\alpha_s(M_Z)=0.11955$ vs PDG 2025 $0.1175\pm0.0010$, **+1.7%, $\approx2.1\sigma$**.

**Why it matters.** Unchanged from 2026-08-02, and it is the only item on that list that would
move a *number* rather than a status. It also carries the $\sqrt\sigma/f_\pi$ +12% residual (G5)
and the overall mass scale $N$ (D9).

**What blocks it.** No longer the apparatus — **F287 discharged that prerequisite** (F162 is 3/3
post-F277, no refold survives, subtracted shift grid-convergent to $1.8\times10^{-4}$, and
$b_0=11$ recovered numerically as well as symbolically). What blocks it now is narrower and was
named by F287: absolute $b_0$ recovery is **0.952, not 1**, because the midpoint cube is not a
fundamental domain of a $\sqrt3$-fcc-periodic function, and $d_1$ is an *absolute* constant.

**Smallest next step.** Formulate $d_1$ **subtracted against the Wilson
$\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ reference** — the gate F162's G3 already named —
rather than settling the F267 fundamental domain first. Nothing has been done on this since
2026-08-02 - 12:38.

### 4. Which operator carries $\gamma$ (K3, K12) — the cosmology question is live again

**What.** The primordial tilt is a **scale-free anomalous dimension** $\gamma=0.017550$, not a
second scale (F295). F296 names a candidate operator — the trace of the 3D stress tensor
$T^i{}_i$ in holographic cosmology — inside a branch the published literature explicitly leaves
unanalysed (McFadden–Skenderis $f_1=0$; the PRL's footnote 2 says so verbatim).

**Why it matters.** This row was graded `EXCLUDED` two days ago on a reading F295 corrected three
hours after the report was written. Read correctly, F285's "scale-free ⇒ $n_s=1$, excluded at
8.4σ" is the **positive** statement $\gamma\ne0$. The cosmology block's only live target other
than $\Lambda$.

**What blocks it.** The naive field map is dead: feeding the model's own content (48 Weyl fermions,
2 real scalars of the $E_g$ doublet — fermion-dominated *because* the model is Higgs-free) into
HC's closed form gives $r=0.323$–$0.970$ against BK18's $r_{0.05}<0.036$, over by 9.0× and 26.9×.
Reaching the bound needs $N_\Phi>792$ scalars; the model has 2.

**Smallest next step.** F296 says it, and it is honest that this is **external** work: a worked
$f_1=0$ conformal-dual calculation of $\gamma$. The in-repo step is smaller — decide whether the
model claims a dual at all, given that the field map already failed.

### 5. Connect the ledgers to the files they grade (H4, H5)

**What.** Two stale-authority problems, one mechanical fix each.
**(a)** `findings/` has **no banner enforcement at all**: `tools/apply_supersession_banners.py`
and `test_no_orphan_banners` both iterate `record["tests"]` and walk only `tests/` and `src/`, so
the `findings:` blocks added at the F16–F19 retirement are read by nothing, all 8 active finding
banners are hand-written and unverified, and 4 of them (F20, F22, F64, F176b) have no ledger record
at all. All 16 findings the ledger names as superseded still read `Status: Confirmed — N/N PASS`.
**(b)** `docs/status/open-derivations.md` was last audited **2026-07-19 at frontier F256**. The
tree is at **F306**. The ledger this command is supposed to grade against knows nothing about
F282–F296 — the entire primordial-sector arc — and its G1 row is written as if F295/F296 had not
happened.

**Why it matters.** Both are why this sweep had to grade several rows from `changelog.md` rather
than from a ledger. A ledger that a reader must cross-check against the changelog is not an
authority.

**What blocks it.** (a) Concurrency, at the time: the triage deliberately did not execute its own
§5 fix because the `gracious-jolly-meitner` claim was open on F20–F25 and touching the same file.
That claim has since closed. (b) Nothing.

**Smallest next step.** (a) The triage wrote the three steps out: add a markdown path to
`apply_supersession_banners.py` keyed off `record["findings"]`, widen `test_no_orphan_banners` to
walk `findings/`, then populate `findings:` blocks on S3, S4, S6, S10, S11, S12, S13, S15 from the
`retained:` clauses that already exist. (b) Re-run the open-derivations audit prompt; the frontier
is 50 findings away.

---

## What is ABSENT

The seven rows where the model has **no sector at all**. None appears in `open-derivations.md`,
because that ledger tracks attacked targets and these have not been attacked.

| # | Requirement | Note |
|---|---|---|
| A8 | Measurement problem / classical emergence | Zero hits repo-wide (the single `docs/` hit is the previous completeness report). A unitary QCA with no account of measurement or the classical limit |
| A9 | Spin-statistics connection | Zero hits. Fermionic antisymmetry is *implemented* (F217 Jordan–Wigner, F195 live Gram–Schmidt Pauli); the connection is imported |
| A10 | Cluster decomposition | Zero hits. No-signalling appears once (F227) and only as a QC aside |
| B10 | Why 3 colours | $N_c=3$ is an input and load-bearing: F279 makes it the source of the *thirds* (commensurability holds for any $N_c$). **F291 and F292 both state explicitly that they do not touch it** |
| ~~K2~~ | ~~BBN / light-element abundances~~ | **LEFT THIS TABLE 2026-08-05 (F297).** 9 findings mentioned BBN and every one used it as a *bound* (F283/F284 on $\dot G/G$, F237 on relics), never computing an abundance. Row now `PARTIAL`; see the K block |
| ~~K11~~ | ~~Structure formation / $\sigma_8$~~ | **LEFT THIS TABLE 2026-08-05 (F288).** It was absent in the *ordinary* sense — the machinery existed and nobody had connected it — and that is exactly how it closed: three findings the tree already owned (F106, F64, F284), no new physics. Row now `PARTIAL`; see the K block |
| ~~G10~~ | ~~Statistical mechanics / thermodynamics on the lattice~~ | **LEFT THIS TABLE 2026-08-06 (F300).** Temperature entered cosmology and superconductivity as an external parameter and all 18 entropy mentions were black-hole or information entropy. Row now `PARTIAL`; see the G block and Amendment 5 |

**Reading this list.** It shrank from 13 to 7 in two days, and only two of those six closures were
new physics (A1 via F291/F292, and K12 on 2026-08-02). Three were reclassifications to `EXCLUDED`
on the same day the baseline was written, and **one — E10 — was never absent at all**: F183 §L1
has carried a gate-tested lattice-regulated core since 2026-06-30. The remaining seven split
cleanly: four are the quantum-foundations layer a cellular-automaton model would be *expected* to
speak to and does not (A8, A9, A10, plus G10), two are cosmology sectors with no entry point
(K2, K11), and one is a single load-bearing integer (B10). The foundations half is still the more
surprising, and it has not moved.

> **Amendment, 2026-08-05.** Two of the seven have since closed, and the pattern is worth
> recording. **K11** went `ABSENT → PARTIAL` (F288) and **A8** was taken up by a concurrent
> session (F281). Neither needed new physics: K11 closed by connecting F106, F64 and F284 —
> all already in the tree — which is what "absent in the ordinary sense" turned out to mean.
> Five remain: A9, A10, G10, K2, B10. The foundations half is now three of five rather than
> four of seven, so the imbalance this section flagged has narrowed but not reversed.

> **Amendment 2, 2026-08-05 - 18:40** (session `tender-gifted-pascal-2`, the thread that took A8).
> **A9 and A10 have now closed too** — F289 and F290 — so of the seven ABSENT rows this report
> opened with, **four are gone and three remain: G10, K2, B10**. The foundations block is now
> **clear**: A8, A9 and A10 all closed within two days of being named, and none of the three needed
> new physics. A9 reuses F291/F292's derived $d=3$ plus the rotor the tree has had since F26; A10
> reuses F227's cone and F212's register; A8 reused minimal coupling and the F130 $R_b$. That is
> the same pattern K11 showed, and it is now the dominant one: **"absent" in this tree has mostly
> meant "never assembled", not "not there"** — which is a statement about the report's own method
> as much as about the model, and argues for re-reading the remaining three (G10 lattice
> thermodynamics especially) as assembly problems before treating them as research problems.
>
> Two cautions against reading the closures as stronger than they are. F289 is explicitly **not** a
> proof of the spin-statistics theorem — it shows the model derives the theorem's two *premises*,
> and its card (CL255) is `tier: supporting`, `confidence: medium` for that reason. F290's
> clustering leg is **1-D and free-fermion**; the interacting 3-D statement is not established.
> Both limits are named in the findings and on the cards.
>
> **Amendment 3, 2026-08-05 - 20:55** (same thread). **B10 moves `ABSENT` → `PARTIAL`** (F293), so
> **five of the seven are gone and two remain: G10 and K2.** B10 is the one closure that did NOT
> follow the "never assembled" pattern the previous amendment identified, and the difference is
> instructive. $N_c=3$ is **still not derived**; what F293 supplies is a *map of the route space* —
> anomaly cancellation is proved unable to select $N_c$ (and for a model-specific reason: $Y_Q$
> falls out of the same nullspace $\propto N_c$, so the usual SM argument is circular here), colour
> is proved not to be the spatial 3, the $\mathbb Z_3$ centre route is proved circular as the tree
> stands, and what works is an **empirical selector** rather than a derivation. This report should
> not record B10 as answered: the grade moves because the question is now bounded, not because the
> integer is explained.
>
> **Amendment 3b, 2026-08-05 - 22:25.** F294 executed F293's own named next step (auditing the F110
> C7 $\chi$-map for $N_c$) and the result makes B10's `PARTIAL` **more** conditional, not less. The
> $\chi$-map is now *measured* $N$-free across $\mathbb Z_2..\mathbb Z_9$ and $U(1)$ (deviation
> literal `0.0`) — but that covers only the groups the model implements, and under a
> fundamental-Casimir reading the selector returns $N_c=1.28$ while an adjoint reading has **no root
> at all**. F293's falsifier described this as a 25% shift; it is structural. CL257 is corrected.
> A future sweep should read B10 as: *the route space is mapped, and the one surviving route is
> contingent on a modelling choice that has never been validated.*
>
> **Amendment 4, 2026-08-05 - 23:20** (session `quiet-eager-gamow`). **K2 moves `ABSENT` →
> `PARTIAL`** (F297), so **six of the seven are gone and one remains: G10.** K2 followed the
> "never assembled" pattern in its *method* — the expansion side was already owned outright
> (structural $G$ from F79/F107, the F178 source law, $\dot G/G\equiv0$ from F284, and an
> $N_\text{eff}=3.044$ with no free parameter, because $\nu_R$ is a total singlet and the model is
> Higgs-free) and nothing new had to be invented to run a BBN code on it. It did **not** follow the
> pattern in its *outcome*, and that is the part worth recording.
>
> Assembling the sector produced a **falsifier, not a confirmation**. The light elements come out
> right ($Y_p$ at $-0.11\sigma$, D/H at $-1.8\sigma$), and BBN then does two things this report did
> not anticipate. It **independently confirms the F178 adoption** — the demoted energy-only law
> gives $Y_p=0.1856$, $-17.6\sigma$ — on an observable three decades of redshift away from the
> neutron-star argument that actually decided it. And it **measures** $m_n-m_p$ to $\pm0.0056$ MeV,
> where F122's own acceptance check used $\pm1$ MeV: a factor 179, against which the model's derived
> $+1.51$ MeV is excluded at $36.6\sigma$ in helium and by a factor 2.7 in the free-neutron lifetime.
> F122's sign claim survives; its value does not.
>
> **This is a data point for gap #1 of this report, not only for the K block.** The review series
> found ten of ten individually-reviewed findings needed correction and argued the fix was to review
> *load-bearing* findings rather than old ones. K2 says something adjacent and cheaper:
> **assembling an absent sector is itself a review instrument**, because it forces every input
> through an observation that had never been applied to it. F122's S8 sat at "within 1 MeV, sign
> correct" from 2026-06-09 with nobody disputing it, and no amount of re-reading F122 would have
> tightened that tolerance — one afternoon of BBN did. The remaining row, **G10** (lattice
> thermodynamics), is worth reading the same way: as an assembly that will grade its own inputs.
>
> **Amendment 5, 2026-08-06 - 12:40** (session `bright-candid-gibbs`). **G10 moves `ABSENT` →
> `PARTIAL`** (F300), so **all seven of the ABSENT rows this report opened with are now closed**,
> in two days plus one morning. The table above is empty.
>
> G10 followed the "never assembled" pattern completely: the partition function is a Brillouin-zone
> integral over the paired-spinor dispersion the tree has owned since F69, the ruler is F107, the
> walk is F26, and nothing new had to be invented. It also did what Amendment 4 predicted it
> would — **the assembly graded its own inputs, and this time the input passed.** F297 assumed the
> continuum $p=\rho/3$; F300 derives it, in closed form, with the correction at the BBN bottleneck
> at $1.2\times10^{-44}$. That is a different kind of result from K2's and worth naming as such:
> **assembling an absent sector is a review instrument whether or not it finds a defect**, because
> before this morning nobody in this tree could have said whether the number was $10^{-44}$ or
> $10^{-2}$, and "we checked and it is fine" is only available to someone who checked.
>
> Three cautions against reading this closure as stronger than it is, all named in the finding
> rather than left for a reader to find. (a) The equation of state is the **equilibrium** measure on
> the derived dispersion; the same finding proves the free sector does not dynamically reach it
> ($2N$ conserved branch occupations ⇒ a GGE, not Gibbs), so §3 must never be cited as evidence
> that the lattice thermalises. (b) It is the **photon sector only** — a $g_*(T)$ over the model's
> 48 Weyl fields is the named next step, and until it exists the cosmology block still imports an
> SM degree-of-freedom count. (c) The second-law leg is **time-symmetric** and says so: the arrow
> is the initial condition plus the coarse-graining, not the dynamics.
>
> One row this closure deliberately does **not** move is **E9**. F300 §5 proves F190's own named
> next step impossible as written — $e^{2\pi\sqrt3}=53252.295$ is not an integer, so the per-cell
> entropy is not a state count of anything — and passes the necessary capacity condition at
> $6.11\times$. That sharpens the target without deriving the number, and the finding, the card
> (CL261) and the changelog all say the grade stays put. Compare B10's Amendment 3, where the same
> distinction had to be drawn: **a question becoming well-posed is not the question being answered.**
>
> With the ABSENT table empty, the report's own ranking should be re-read. Nothing here touched
> gaps #1 (review debt: 262 findings never through `/review-finding`), #2 (falsifier soundness as a
> gate) or #5 (the ledgers, and `open-derivations.md` now 50 findings stale) — and F300 is a live
> example of why #2 matters, since its CL260 had to reason explicitly about *not* inventing an
> observational threshold for a distortion that is 29 orders of magnitude out of reach. **The
> remaining work in this report is now entirely integrity work, not coverage work.** That is a
> larger change in the shape of the project than any single row.

---

## Regressions since 2026-08-02

**Three integrity rows fell, all on the same evidence.** These are not new defects introduced in
two days; they are pre-existing conditions that the new review instrument made visible, which is
the correct thing for a completeness report to record as a regression in *grade*.

| Row | Was | Now | Why |
|---|---|---|---|
| H2 Falsifiability | QUANT | **PARTIAL** | Register-level thresholds unchanged (5, all numerical), but finding-level check soundness is unaudited and measurably weak: 6 of 6 reviewed findings had a check that could not fail; 72 test files are UNFALSIFIABLE by the suite's own metric; F282's falsifier 5 had to be struck as unable to fire |
| H4 Retraction hygiene | QUANT | **PARTIAL** | The *mechanism* is still exemplary (the supersession unit is a check, not a file). The *enforcement* is absent where a reader looks: all 16 ledger-named superseded findings still read `Confirmed — N/N PASS`; `findings/` is walked by no banner test; 4 hand-written banners have no ledger record |
| H6 Reproducibility | QUANT | **PARTIAL** | `make gate` not seen green end-to-end; **`supersession-ledger` confirmed FAIL this run** (S14 `P5.1` malformed decision id), red since 2026-08-03 across three sessions that each flagged it; gate records 28 → 47, none of the three `scenario` physics gates exercised |

**One EXCLUDED grade was wrong and is corrected upward in prospects, downward in closure.**

- **K3 `EXCLUDED → OPEN`.** The 2026-08-02 - 16:45 amendment graded K3 `EXCLUDED` on F285's
  "every natural measure gives $n_s=0$ or 4; scale-free gives exactly 1, excluded at 8.4σ".
  **F295, three hours later, corrected F286's reading of its own theorem** and with it F285's row:
  $p=0$ is not the trivial case, it is a scale-free anomalous dimension, so the 8.4σ exclusion is
  the *positive* statement $\gamma=0.017550\ne0$. F296 then named a candidate operator and a named
  obstruction. A row with an identified attack is `OPEN`, not `EXCLUDED`. **The report was never
  amended for F295 or F296**, which landed at 19:35 and 21:00 the same evening.
- **K5 kept at `EXCLUDED`, and the previous note is narrowed.** That note said F285 reduced K5
  "from a free function to one number — the 3.5% tilt". The tilt is the *index* (K3/K12); K5 is the
  *amplitude* $A_s$, for which nothing has changed and no route exists. The two were conflated.

**One grade was wrong from the baseline run in the other direction.**

- **E10 `ABSENT → PARTIAL`.** The baseline note read *"F183 gives exact Schwarzschild, so the
  singularity is inherited from GR. The lattice cutoff is the obvious resolution and is not worked
  out anywhere."* It is worked out, in F183 itself: §L1 is a gate-tested check that Kretschmann
  curvature saturates at the cell scale, giving $r_\text{core}=(48(GM/c^2)^2a^4)^{1/6}\propto
  M^{1/3}$ — $\sim5\times10^{-22}$ m for $1\,M_\odot$, $\sim10^{12}$ cells across, and F183 calls
  it "the model's substrate-level singularity resolution". F284 §5 then added the cosmological half
  (no substrate singularity; first resolvable epoch $H_\text{max}=3^{-3/4}M_\text{Pl}$ at
  $t_\text{min}=\sqrt3$ ticks). This row should have been `PARTIAL` on 2026-08-02.

**Content regression with no grade change: A2 (Lorentz invariance).** The row stays `PARTIAL`, but
its seam is now named and worse than it read. **F22's claim 1 is false** — the linear SR boost does
not preserve the arccos mass shell, and the remediation now *asserts* the failure at first order in
$v$ with coefficient $1/\rho-1$ (measured $-0.0930513$ vs predicted $-0.0931003$ at $m=0.5$).
**F24 no longer claims to "close the Lorentz-covariance loop"** — the review found it ran pure
boosts only, which are Hermitian and therefore structurally blind to the dagger placement the test
existed to catch, and narrowed the finding to a convention/regression check with **no lattice
content at all**. The actual question — does the lattice *evolution* commute with a boost at finite
$a$ — is now explicitly DEFERRED into `next-steps.md`. Two findings that read like Lorentz
covariance results do not supply one.

**Two exactness Tier-1 rows withdrawn (G1's evidence, not its grade).** Under F306 / ledger S18:
Tier-1 **#7 and #49 are withdrawn**, #51 reclassified, Tier-2 #15 annotated, and inventory row 3's
2026-05-23 "reframed as resolved" is corrected. Worth recording because **#7 had been
retroactively rewritten to point at #49 — the entry that superseded it.** G1 stays `EXACT`: the
curl closes at $O(k^3)$ with the exact coefficient $c_\text{lat}^3/48=1/(144\sqrt3)$, which is
better than what was claimed, and F25's rotation law is live as an identity.

**Carried forward, second consecutive report — both still unverified.**

- **Whether F277's refold fix left B9's cited numbers re-blessed.** Leptonic
  $\Delta\alpha(M_Z)=0.24\%$ comes from F251, which S12 supersedes, and F277 *flipped a sign* in
  vacuum polarization. F287 verified the background-field apparatus (that is B8); grep finds no
  post-F277 re-derivation of the 0.24%. **B9 cites a superseded finding for a number nobody has
  re-checked.**
- **10 `candidate` baselines still report FAIL by design**, with no recorded decision.

**Resolved since the last report.** The `dimensionality.py` unregistered-module item is closed
(F291/F292 registered it, `_SPINE`, 189 modules). The `dead_candidate` count fell 10 → 1. Findings
with no test record fell 28 → 18. Gate records 28 → 47.

**Still open from the last report's gap #4.** `hypercharge.py` writes `Y_LEPTON_L = -1`,
`Y_E_R = -2`, `Y_NU_R = 0` as literals under a comment reading *"SM hypercharge assignment"*.
They are **derived** (F165, re-derived by F279) and belong in `casim.constants` with provenance.
F279 follow-up 1, unactioned. This is the one live code-vs-finding contradiction in H5.

> **Update 2026-08-06 — closed.** The three are `casim.constants` entries (`electroweak` sector,
> F165+F279 provenance) and `hypercharge.py` imports them; the F279 gate record gained
> `check_registry_values_are_on_the_derived_line`, which re-solves the six-row system and reads the
> normalisation back out of the registry. The grade above is left as the 2026-08-04 snapshot read it.
> What is *not* closed: the quark hypercharges are still literals, because their fractions carry the
> underived $N_c = 3$ (F279 A3) — that is B10's problem, not H5's.

---

## Full rubric

### A — Foundations

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| A1 | Spacetime dimensionality | **PARTIAL** (was ABSENT) | **F291**, **F292** | the "+1"; $s=2$ minimal cell | Two logically independent selectors each return $\{3\}$: $\ker J=0\Rightarrow d\le3$ and $\operatorname{coker}J=0\Rightarrow d\ge3$ (a phase to gauge exists iff $\operatorname{coker}J=0$, so founding decision 1 needs $d\ge3$); and $\dim\Lambda^2\mathbb R^d/d=(d-1)/2=1$ only at $d=3$, which never mentions the cell. F292 kills $d=6$ (no chirality at all, $D=7$ odd product $\propto\mathbb I$) and $d=9$ (overcounts by 4), and shows reducible $d=3n$ **freezes** ($\ker J=3(n-1)$ exact zero modes). Not `EXACT`: the "+1" is by construction and this derives $d$ from *adopted* structure. F291 §7 asks for exactly this grade |
| A2 | Lorentz invariance | PARTIAL | F26, F28, F30, F246, F129, **F301** | leading CPT-even $\lvert k\rvert^3$, $c_3(\hat k)=-(\sqrt3/216)(p+3q)$; **finite-$a$ boost covariance now ADDRESSED and negative — broken at $O(\lvert k\rvert^2)$ on chiral branches, $O(\lvert k\rvert^3)$ on the even law, exact on the cubic axes (F301)** | All even-power ($k^2,k^4$) LV terms vanish **identically** (F246, exact); LIV bound ~15 decades below GRB sensitivity (F28); LIV operators irrelevant under block-spin, $\lambda_n=b^{-n}$ (F129/F130). **Seam CLOSED 2026-08-06 by F301.** The whole Poincaré defect is the gradient of one scalar, $\Phi=(\Omega^2-c_\text{lat}^2k^2)/2c_\text{lat}^2$ — $[K,P]$ never fails and the $[K,K]$ defect reduces to the same $D_i=\partial_i\Phi$, which also survives $K\to K+f(k)$, so the answer is not a property of a chosen boost. **Exact to all orders on $\langle100\rangle$**; $\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)\lvert k\rvert^3$ (rational) for the even photon; $\mathbf D^{(s)}=-s\,c_\text{lat}(k_yk_z,k_zk_x,k_xk_y)$, one order worse, on a chiral branch — the difference being the chirality-oddness of $b_2=-\tfrac13\hat k_x\hat k_y\hat k_z$, i.e. the same symmetrisation that kills birefringence. Both $⚠$ marks are answered rather than carried: F22's $\rho(m)$ **is** the leading BCC term ($D_i\to(1/\rho-1)k_i$) and F24's deferred question has a result. A deformed $(E,P)$ shell is exact at finite $a$ for every mass but **not universal** ($\Omega_\text{even}-\omega_+=\tfrac13\hat k_x\hat k_y\hat k_z\lvert k\rvert^2$), which is why this stays `PARTIAL` rather than becoming `EXACT` |
| A3 | Causality / locality / finite speed | EXACT | F26, F204, F227 | 0 | $c_\text{lat}=1/\sqrt3$; strict causal cone $C(r,t)=0$ for $r>4t$ (F227); superluminal warp family structurally excluded (F204) |
| A4 | CPT, and C, P, T separately | PARTIAL | F53 | — | C, P, CP built per species and exact; $C$/$P$ maximal; CP conserved at one generation ($J(1)=0$ arithmetic, not a prediction). **No CPT theorem for the QCA**; T is thin |
| A5 | Unitarity | EXACT | F276, F264 | 0 | Every step is a length-preserving rotation by construction |
| A6 | Superposition + Born rule | **EXACT** (was PARTIAL "never derived"; F304 + §5, 2026-08-06) | F304, F281, F290, F227 | Cooke–Keane–Moran regularity lemma; the $\sum w=1$ premise | Superposition is structural. The Born rule is **derived**, and since F304 §5 the theorem it rests on is **proved here rather than cited** — the grade moves off the A9 precedent for that reason. Premises forced by the rule: $\dim\ge3$ (a measurement needs a record and a record needs cells ⇒ min dim 4; the free step's 2-dim momentum blocks are invariant but **unreadable**, $\lVert[\Pi_k,\hat n]\rVert=\sqrt{2/N-2/N^2}$ at residual `0.0`) and non-contextuality (the record channel is $H_\text{int}$, a fixed operator of the rule carrying no reference to the measured basis — weight spread across contexts literal `0.0`; remote contexts blocked by F290's exact no-signalling). Theorem: $b_k=(-1)^k/\binom{k+d-2}{k}$, survives iff $1+(d-1)b_k=0$ — **one formula gives both halves**, every odd $k$ at $d=2$ (the hole) and only $k\le1$ at $d\ge3$ (dimension $d^2$). F281 leg 1's hypothesis becomes a **conclusion**, leg 2 becomes unnecessary. Residual is now one **lemma** (non-negative frame function ⇒ continuous; excludes non-measurable weights) plus the irreducible "a probability exists" premise |
| A7 | Entanglement, Bell/Tsirelson | EXACT | F212, F226, F214, F217 | $1.8\times10^{-15}$ | Saturates Tsirelson $S=2\sqrt2$ **exactly** ⇒ Bell-indistinguishable from QM (CN1, settled null); entanglement *generated* from product input |
| A8 | Measurement problem / classical limit | **EXACT** (was ABSENT; F281, 2026-08-05) | F281, F130, F41 | Born-rule hypotheses | Pointer basis **forced** by minimal coupling ($[H_\text{int},\hat n]$ = literal `0.0`; $\{\hat n(x)\}$ maximal abelian ⇒ unique); classicality = block-spin attractor, $\lambda_\text{coh}=\lvert D_b(k)\rvert^2$, irrelevant at $b^{-6}$. Born on two legs, both with named gaps |
| A9 | Spin-statistics | **PARTIAL** (was ABSENT; F289, 2026-08-05) | F289, F291, F292, F217 | topological step external | The theorem's two premises are **derived** here ($d=3$ from F291/F292; $R(2\pi)=-\mathbb 1$ from the rotor, $1.7\times10^{-16}$ over 60 axes), so Fermi for spin-½ and Bose for the paired-spinor photon follow. **Not** a new proof of the theorem: $\pi_1=S_n$ and the belt-trick homotopy stay external |
| A10 | Cluster decomposition / no-signalling | **MACHINE** (was ABSENT; F290, 2026-08-05) | F290, F227 | 1-D free-fermion clustering | No-signalling exact ($7.8\times10^{-16}$); the cone is **strictly** finite where a generic Lieb–Robinson system has an exponential tail (bound 7.39 at the same points vs $6.9\times10^{-16}$ measured), measured tight at 1 site/layer and reconciled with F227's $4t$. Clustering $\xi\propto\Delta^{-0.9268}$ quoted as measured |
| A11 | UV completeness | PARTIAL | F116, F164, F264, F284 | — | The BZ edge is a **physical** cutoff, yet F264 runs the full renormalisation program with counterterms on top. F284 §5 sharpens the first picture ("the cutoff does the work usually handed to quantum gravity") without reconciling it with the second. **Arguable:** both are individually sound and nowhere reconciled |
| A12 | Continuum limit | MACHINE | F129–F135, D1 | $\lVert[R_b,\text{evo}]\rVert\le1.8\times10^{-15}$ | $c_\text{lat}$ an exact RG fixed point; simple-cubic code retained as the declared regression target |

### B — Gauge structure

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| B1 | Origin of $SU(3)\times SU(2)_L\times U(1)_Y$ | PARTIAL | F27, F51, F43, F291 | $SU(3)_c$ imposed | $SU(2)_L$ derived by $\beta$-gauging the complex-mass step; $U(1)_Y$ from bipartite sublattice parity. **F291 adds a structural precondition:** the phase $SU(2)_L$ gauges exists only for $\operatorname{coker}J=0$, i.e. only at $d\ge3$. Colour is still put in |
| B2 | Chirality | EXACT | F27, F91, F292 | Ward identity $1.1\times10^{-17}$ | $W^\pm$ chiral is *forced* — right-branch weight $\equiv0$ over ℚ. F292's S4 adds an independent route: a traceless $\Gamma=\gamma_1\cdots\gamma_D$ needs **odd** $d$, verified by explicit Clifford recursion $D=2..8$, written twice and separately typed |
| B3 | Anomaly cancellation | EXACT | F38 | literal 0 over ℚ | All six traces (gauge + gravitational) exactly zero. **Witten $SU(2)$ global anomaly still not checked** |
| B4 | Hypercharge / charge quantisation | EXACT | F165, F279, F47, F51, F38 | one charge unit, + $N_c=3$ for the thirds | Rank 6, dim 1 over ℚ; closing constraint is the F47 Majorana step, not the grav anomaly. Register at rev 3, core claim 10. **Code literals remain** — see Regressions |
| B5 | EWSB mechanism | EXACT | F27, F34b, F44 | 0 | Higgs-free Stueckelberg; $U(x)$ pure gauge; $m_A=0$ from a rank-deficient mass matrix. Founding decision #3 |
| B6 | Weinberg angle, with scale | QUANT | F138, F49, F231, F141 | $+0.22\%$ at $M_Z$; $-0.064\%$ on shell; **0 free params** | $\tfrac14$ = matching at $\mu_\star=4\pi v=3.09$ TeV, forced by $Y$ having no lattice kinetic term; $\tfrac29$ is its on-shell face (F231) |
| B7 | Confinement | PARTIAL | F70, F86, F94, F88 | 3+1D is constructed, not proven | **Exact in 2D** (area law, $\sigma=-\ln w(\beta)>0$ for all $\beta$). 3+1D = colour-dielectric dual superconductor, cross-checked against independent gauge Monte-Carlo |
| B8 | Asymptotic freedom / $\alpha_s$ running | PARTIAL | F144, F151, F239, F235, **F287** | **$d_1$**; $\alpha_s(M_Z)$ $+1.7\%$ ($2.1\sigma$) | $g_s=\tfrac12$ derived, $b_0=\tfrac{11}3C_A=11$ exact **and now recovered numerically** (F287: 10.47 at $n=32$, log-slope ratio $1.00213\to1$). Prerequisite discharged; residual unchanged. See gap #3 |
| B9 | Running of $\alpha$, EW couplings | QUANT | F251 ⚠, F261, F115 | leptonic $\Delta\alpha(M_Z)$ $0.24\%$ | $e=g/2$ reduces EW to one magnitude (F115). **F251 superseded by S12-F277, which flipped a vacuum-polarization sign; the 0.24% has not been re-derived post-F277.** Second report carrying this |
| B10 | Why 3 colours | **PARTIAL** (was ABSENT; F293, 2026-08-05) | F293, F279, F144, F110 | $N_c$ still not derived; selector consumes measured data | Anomalies **cannot** select $N_c$ here (nullspace dim 1 for every $N_c$, symbolic over ℚ); colour is **not** the spatial 3 ($[C_3,\lambda^a]=2.449$); the $\mathbb Z_3$ route is **circular**. What works: the $N_c$-free bare coupling makes $\Lambda$ span **28.3 decades** over $N_c=2..4$ and only 3 lands at the hadronic scale ($N_c=2.998$ from $\alpha_s$, partly circular and labelled so) |
| B11 | Strong CP / $\theta_\text{QCD}$ | PARTIAL | F53 | tree $3.3\times10^{-16}$; loops open | $\theta$ pure gauge at tree level. The 2026-06-29 audit flagged loop survival and it is still unaddressed |
| B12 | Gauge-boson masses, $\rho$, $m_Z/m_W$ | PARTIAL | F49, F141, F138 | ratio $-0.064\%$; **absolute scale is an input** | $m_Z/m_W=3/\sqrt7$ exact-form. $v$ is an anchor, so $m_W$, $m_Z$ absolute are not predicted (Scope says so) |

### C — Matter content

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| C1 | Exactly three generations | PARTIAL | F75, F84 | physical identification is a hypothesis | Group theory is a **theorem** ($\sum d^2=\lvert O_h\rvert=48$ ⇒ max single-valued irrep dim 3, $T_{1u}$ unique); the identification is a **stated hypothesis** (F75 §7, a Candidate finding). **Hygiene note:** F292 §6 found that its $n$-copies-into-one-triplet map has multiplicity $n$ — the same structure F75 uses — and **declined the inference**, recording the resemblance so a later session does not mistake it for a result |
| C2 | First-generation multiplet | EXACT | F38, F41, F42, F51, F165 | 0 | Complete and anomaly-free |
| C3 | Colour triplet + fractional charge | PARTIAL | F136, F165, F279 | conditional on $N_c=3$ | Fractional charge is *forced* — but by the $3y_Q+y_L=0$ row, i.e. by the input $N_c=3$; F279 makes this explicit (commensurability holds for any $N_c$) |
| C4 | Neutrino nature (Dirac vs Majorana) | PARTIAL | F47, F266 | — | The Higgs-free Majorana step is constructed and $\nu_R$ is a structurally-forced total singlet ($Y=0$). Nothing **forces** Majorana over Dirac |
| C5 | Neutrino mass mechanism | PARTIAL | F47, F236, F254 | $M_R$ free | See-saw + $E_g/Z_3$ texture fix the three light masses and hierarchy at machine precision; absolute scale unfixed |
| C6 | Antimatter / charge conjugation | EXACT | F53, F260 | 0 | Per-species $C$; positron and crossing sector built |
| C7 | Beyond-SM content | PARTIAL | F223, F228, F266, F216, F204 | geon abundance free | Predicts a Planck-mass BH-remnant geon. **Excludes** its own alternatives: native massive spin-2 (F216 CN5), $\nu_R\nu_R$ J=2 (CN6), Alcubierre warp (F204), keV sterile as 100% DM (F237) |

### D — The parameter ledger

| # | Parameter | Grade | Evidence | Note |
|---|---|---|---|---|
| 1–6 | $m_u,m_d,m_s,m_c,m_b,m_t$ | ABSENT ×6 | F121 | Quark masses are "the measured values converted to kg — a **consistency** readout" (F121). The *constituent* scale $m_c=309.5$ MeV from one $f_\pi$ anchor (F123) is a different quantity |
| 7–8 | $m_e/m_\tau$, $m_\mu/m_\tau$ (shape) | QUANT ×2 | F175, F234, F120 | $\le0.007\%$ with **zero shape parameters**, from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$. Koide $Q=\tfrac23$ at $0.91\sigma$ |
| 9 | Charged-lepton overall scale | FIT (N=1) | F121, F233 | $\tau$-anchored; F233 reduces the derivation gap to a factor 1.9 zero-param, but the anchor is still an anchor |
| 10–13 | CKM 3 angles + 1 phase | ABSENT ×4 | — | Scope: out of scope. $J(1)=0$ is one-generation arithmetic, not a prediction |
| 14 | $\alpha_\text{em}$ | OPEN | F127 | **Four-avenue no-go** on deriving it from the rule. Still the one EM input |
| 15 | $g_2$ / $\sin^2\theta_W$ | QUANT | F138, F49 | Derived with its scale, $+0.22\%$, 0 params |
| 16 | $g_3$ / $\alpha_s$ | PARTIAL | F144, F239, F287 | One residual: $d_1$. Route narrowed by F287, value unmoved |
| 17 | $v$ | FIT (N=1) | Scope | "The electroweak scale $v$ is an anchor, not an output" |
| 18 | $m_H$ | OPEN | F73 | Kinematics exact, but free-sum kinematics **cannot** reproduce 125.25 GeV; missing input is binding dynamics |
| 19 | $\theta_\text{QCD}$ | PARTIAL | F53 | Tree-level pure gauge; loops open |
| 20–21 | 2 light-$\nu$ mass ratios | MACHINE ×2 | F236 | The $E_g/Z_3$ texture fixes masses + hierarchy at machine precision |
| 22 | $\nu$ absolute scale ($M_R$) | OPEN | F47, Scope | "nothing in the model fixes $M_R$" |
| 23–25 | 3 PMNS angles | EXCLUDED ×3 | F254 | Proven **no lattice selector**: the three $T_{2g}$ amplitudes are three inequivalent 1-d irreps under the $E_g$-stabiliser $D_{2h}$. Genuinely and permanently free — a result |
| 26 | $\nu$ Dirac CP phase | ABSENT | — | Not addressed |
| 27 | $G$ | EXACT | F79, F107 | $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ structural; $3\times10^{-8}$ vs CODATA; 0 free params. Inherits F75's hypothesis status per Claims claim 4 |
| 28 | $\Lambda$ | OPEN | F164, F192, F193, F196, F241 | Two unreconciled pictures; untouched since 2026-08-02 |

**Ledger tally — unchanged.** Derived with zero free parameters: **6** (2 lepton ratios,
$\sin^2\theta_W$, 2 $\nu$ mass ratios, $G$). Partial, one named residual each: **2** ($\alpha_s$,
$\theta_\text{QCD}$). Fitted or free input: **6** (lepton scale, $v$, $\alpha$, 3 PMNS). Open or
absent: **14**.

**How to read that against the SM's 19.** Not "6 beats 19". The model **derives 6 quantities the
SM takes as free**, **proves 3 more permanently free** (PMNS, F254 — itself a result), and **does
not yet address 14**, of which 11 are quark masses and CKM. The SM's parameter count is not
reduced until the quark sector is addressed; the sectors the model *has* built carry genuinely
zero free parameters, and that is the claim actually being made.

### E — Gravity and general relativity

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| E1 | Fundamental field equation | POSIT | F178 | — | DECISION 2026-06-29: induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$. Alternatives genuinely closed: energy-only is not Lorentz covariant and has **no** NS maximum mass (excluded by PSR J0740, F174/F176) |
| E2 | Equivalence principle | MACHINE | F64, F62 ⚠ | — | F62 is named in S3 (superseded in part); its lapse-mix sign convention is still production code |
| E3 | PPN $\beta,\gamma$ | EXACT | F64 | $\beta=\gamma=1$ exactly | GR-identical. The naive linear dielectric ($\beta=\tfrac12$, 50.1″/cy) is excluded |
| E4 | Classical tests | QUANT | F64, F107, F111 | $3\times10^{-8}$ | Mercury 42.98″/cy, solar-limb 1.7512″, Shapiro, redshift |
| E5 | Newton's constant | EXACT | F79, F107 | $3\times10^{-8}$ vs CODATA | Structural, not Sakharov-premised. Fixes $a/\ell_P=\sqrt{8\pi}3^{1/4}=6.5978$ |
| E6 | GW speed, polarisations, dof | EXACT | F180, F248, F216 | GW170817 residual $\le3\times10^{-83}$ | $c_\text{grav}=c_\gamma$ is a **genuine zero**, inherited through F79 zero-tree-stiffness. Explicit TT graviton, 2 helicity-$\pm2$ modes, proven massless |
| E7 | Inspiral / ringdown QNM | QUANT | F189, F187 | $<7\%$ (WKB) | GW150914 chirp mass 28.1 $M_\odot$, ISCO 67.6 Hz |
| E8 | Black holes | QUANT | F183, F186 | shadow $3\sqrt3M$ | Exact Schwarzschild/Kerr with horizon. The $+4.63\%$ shadow, echoes and absent Hawking spectrum are WITHDRAWN (F114 → F178) |
| E9 | BH thermodynamics | PARTIAL | F190, F183 | one posited constant | $S=A/4$ reproduced **iff** each F107 cell carries exactly $2\pi\sqrt3$ nats — F190 labels itself speculative. Hawking radiation inherited from GR, not derived |
| E10 | Singularity resolution | **PARTIAL** (was ABSENT) | **F183 §L1**, **F284 §5** | $r_\text{core}$ is a quantitative prediction, not a completeness theorem | **Mis-graded in the baseline run.** BH: Kretschmann $K=48M^2/r^6$ saturates at the cell scale $1/a^4$ ⇒ $r_\text{core}=(48(GM/c^2)^2a^4)^{1/6}\propto M^{1/3}$, $\sim5\times10^{-22}$ m at $1M_\odot$, $\sim10^{12}$ cells across — gate-tested, called "the model's substrate-level singularity resolution". Cosmological: no substrate singularity, first resolvable epoch $H_\text{max}=3^{-3/4}M_\text{Pl}$ at $t_\text{min}=\sqrt3$ ticks. Not `QUANT`: there is no geodesic-completeness result and no interior solution on the core |
| E11 | Interior / TOV / NS EoS | QUANT | F181, F184, F185 | — | SLy $M_\text{max}=2.08M_\odot$, $R(1.4)=11.1$ km, consistent with PSR J0740 + NICER; $I/MR^2\approx0.31$, Lense-Thirring recovered |
| E12 | Quantum-gravity sector | PARTIAL | F216, F248, F79 | — | Graviton exactly massless, 2 dof, UV transversality $\Pi\propto Q^2$ + IR block-spin irrelevance. Gravity's own UV completion beyond "the lattice is the cutoff" is not developed |
| E13 | Galactic-scale consistency | EXCLUDED | F194, F191 | — | The model-native emergent-gravity route is **falsified** by the Bullet-Cluster lensing/gas offset. A dark *source* is required — a result, and a self-inflicted one |

### K — Cosmology

*Row IDs are `K`, not `F`.*

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| K1 | FRW background | QUANT | F182, F188, F284 | measured $\Omega$'s in | Full-tensor source reproduces ΛCDM: $z_\text{eq}\approx3430$, $z_\text{acc}\approx0.63$, age $\approx13.8$ Gyr. F284 re-reads expansion as $K$'s conformal mode on a **rigid** substrate — F182/F188's numbers do not move — and buys $\dot G/G\equiv0$ exactly. Solved *with* the model's source, not derived *from* the lattice |
| K2 | BBN / light elements | **PARTIAL** (was ABSENT) | **F297**, F79, F178, F182, F284 | $\eta_b$ free (K6/F202); network offset $-0.87\%$; $^7$Li not validated | **Closed 2026-08-05 by F297.** The expansion side is entirely model-native — structural $G$ (F79/F107), the F178 source law, $\dot G/G\equiv0$ (F284), and $N_\text{eff}=3.044$ *forced* by the model's own content ($\nu_R$ a total singlet by F165/F279 with a heavy Majorana mass; Higgs-free, so no light scalar) — and the light elements come out: $Y_p=0.2449$ ($-0.11\sigma$ vs Aver 2021), D/H $=2.47\times10^{-5}$ ($-1.8\sigma$ vs Cooke 2018). **Two results beyond the closure.** (i) BBN independently confirms the F178 adoption on an observable unrelated to the NS argument that decided it: the demoted energy-only law expands at a *derived* $S=\sqrt{\kappa/2}=1/\sqrt2$ and gives $Y_p=0.1856$, $-17.6\sigma$ — conditional on the dynamical reading, since F182 A1 makes that law inconsistent for $p\ne0$. (ii) BBN + $\tau_n$ **measure** $m_n-m_p$ to $\pm0.0056$ MeV where F122's own check S8b used $\pm1$ MeV, and the model's $+1.51$ MeV is excluded at $36.6\sigma$ ($\tau_n$: 331 s vs $878.4\pm0.4$). Cannot reach `QUANT`: $\eta_b$ is external by construction, the $A=7$ chain is 92% low and excluded from the battery, and the network's $-0.87\%$ offset rides every absolute number |
| K3 | CMB peaks, $n_s$ | **OPEN** (was EXCLUDED) | **F295**, **F296**, F285, F286 | $\gamma=0.017550$; operator unidentified in-model | Full CMB fit still out of scope (F223). The *index* is not excluded: F295 showed F286 mis-read its own T1 — $p=0$ is a **scale-free anomalous dimension**, not the trivial case — so F285's 8.4σ exclusion of $n_s=1$ is the positive statement $\gamma\ne0$. Constant $\gamma$ needs no second scale and predicts $dn_s/d\ln k=0$ exactly (sympy literal zero); F286's log class predicts $-2.62\times10^{-4}$; they separate at $\sigma\sim2.6\times10^{-4}$. F296 names the operator ($T^i{}_i$ in holographic cosmology) and the obstruction. **Attack identified ⇒ OPEN.** See Regressions |
| K4 | Inflation or substitute | EXCLUDED | F282, F283, F296, F238 | cause named + 4 falsifiers | No slow-roll direction exists: $a/\ell_\text{red}=3^{1/4}$ exactly ⇒ sub-Planckian cutoff, every compact CA direction carries $M_\text{Pl}^2/f^2\ge\sqrt3$. F283 proved the obstruction exactly invariant under $a\to sa$ ($\partial r/\partial s\equiv0$), striking F282's own falsifier 5. **F296 strengthens the row**: holographic cosmology is an established framework that computes $n_s-1$ with no inflaton at all |
| K5 | Primordial spectrum normalisation | EXCLUDED | F282, F284, F285, F238 | $A_s$ free, cause named | With no inflaton and a rigid substrate offering no generating process, $P(k)$ is an automaton **initial condition**. **Narrowed from the previous report:** its note credited F285 with reducing this to "one number, the 3.5% tilt" — the tilt is the *index* and belongs to K3/K12. The **amplitude** $A_s=2.1\times10^{-9}$ has no route and has not moved |
| K6 | Baryogenesis | PARTIAL | F202, F47, F53 | magnitude not derived | All three Sakharov conditions met by the model's own structure (L-violation from F47's anti-linear Majorana step, CP available from F53). Not a Boltzmann computation; no asymmetry number |
| K7 | Dark-matter identity | PARTIAL | F223, F228, F266, F216, F237 | — | Candidate: graviton–graviton J=2 geon, stable as a one-cell Planck-mass BH remnant, $M_\text{rem}=(\sqrt3/2)^{1/2}M_\text{Pl}$ exact, cold and collisionless. Alternatives excluded |
| K8 | $\Omega_\text{DM}h^2=0.12$ | EXCLUDED | F238 | free input, cause named | Provable non-derivability: $\beta$ is a cosmological initial condition pinned by the small-scale primordial amplitude. A scale-invariant spectrum under-produces by $\sim2.1\times10^7$ orders. Read as "permanently free, cause named" |
| K9 | $\Lambda$ magnitude | OPEN | F192, F193, F196, F241 | two unreconciled pictures | Route (a) F193/F196/F241: bare CC exactly zero, $p=2$ dilution derived, 121 orders reduced to the $\Omega_\Lambda\approx0.685$ coincidence. Route (b) F192, under the **adopted** F178 law: the zero-point sum still overshoots by $\sim10^{121}$, all four cancellations underived. **Not one open question but two answers that disagree.** Untouched since 2026-08-02. See gap in the previous report; still live |
| K10 | Dark energy $w$, vs DESI | PARTIAL | F192, F203 | sign exact; magnitude open | Vacuum $w=-1$ gives $\rho+3p=-2\rho$ so it accelerates — sign correct and exact. F203 flags $w=-1$ vs DESI DR2 as one of three falsifiers under pressure |
| K11 | Structure formation / $\sigma_8$ | **PARTIAL** (was ABSENT) | **F288** | $A_s$ free (K5); EH98 $T(k)$ imported | **Closed 2026-08-05 by F288.** The EFT of dark energy carries two free functions $\mu(a,k),\Sigma(a,k)$; the model has **zero**, from three independent sources — $\mu=1$ with $\partial_k\mu\equiv0$ (F106/F178), $\dot G/G\equiv0$ (F79/F284), zero linear slip from $AB\equiv1$ (F64 D-EM9). $\gamma_g=6/11$ and Meszáros $D(y)=1+\tfrac32y$ are sympy literal zeros; $\mu$ is *pinned* to $[0.986,1.008]$ at 1σ; $f\sigma_8$ vs 7 RSD points gives diagonal $\chi^2/N=1.012$. $\sigma_8=0.8204$ is **reported with its budget, not claimed** — cannot reach `QUANT` while K5 stands. Discreteness $\le1.3\times10^{-112}$ at Lyman-α. Falsifier: no screening exists, so the DES Y6 low-$S_8$ direction ($3.00\sigma$) cannot be accommodated |
| K12 | Cosmological initial conditions | PARTIAL | F284, F285, F286, F295, F296, F238 | one anomalous dimension, operator unnamed in-model | Content deepened, grade unchanged. The state must be non-generic by $10^{-56}$ vs white noise at the pivot *and* $\sim2\times10^6$ enhanced at the PBH scale (F238) — opposite ends of the same function. The residual is now a specific number ($\gamma=0.017550$) attached to a specific kind of object (a scaling dimension), with an external candidate and a quantified obstruction ($r$ over BK18 by 9.0–26.9×) |

### G — Emergent and precision physics

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| G1 | Maxwell / classical EM | EXACT | F26, F87, F245, F246, **F306**; F25 (identity) | 0 | **Evidence rewritten, grade unchanged and better supported.** The composite-photon curl closes at $O(k^3)$ with exact coefficient $c_\text{lat}^3/48=1/(144\sqrt3)$ — the pass criterion recorded at `references/qca-papers-1-4-overview.md:407` — and the reported $O(k)$ failure was a representation artifact ($E_G,B_G$ real vs an imaginary RHS; $B=\hat n\times E$ exactly, so the two sides are orthogonal 3-vectors of equal length). F25's rotation law is live but is an **identity**, not a prediction competing with Maxwell. Tier-1 rows #7, #49 withdrawn; #51 reclassified (S18) |
| G2 | Hydrogen, fine structure, Lamb | QUANT | F125, F252, F257, F262 | Lamb $=99.5\%$ of measured | $-13.596$ eV from $m_e+\alpha$ alone; Ry to $1.1\times10^{-12}$ of CODATA; 2p split 10.95 GHz; Bethe log from the model's own spectrum. Residual = two-loop $\alpha(Z\alpha)^5$, declared out of scope |
| G3 | $g-2$, electron and muon | PARTIAL | F252, F261 | hadronic + EW absent by declared scope | $a_e=\alpha/2\pi$ exact; two-loop $A_2=-0.328478965$; $A_2(\mu)=0.765857$ vs known $0.765857410$. Hadronic VP, HLbL and EW **not** claimed — which is the entire interesting part of the muon anomaly |
| G4 | Atomic structure / periodic table | QUANT | F148, F195, F208 | light elements only | H/He/Li/C certified stable (net charge $\le2.2\times10^{-16}$, Pauli via live Gram–Schmidt); He IP 24.0 eV; relativistic SCF with an accuracy map |
| G5 | Hadron spectrum | QUANT | F123, F124, F235, F122 | 1 anchor ($f_\pi$); $\sqrt\sigma/f_\pi$ $+12\%$ | Nucleon $3m_c=928.5$ vs 938.27 MeV ($-1.05\%$) on one anchor; $m_n-m_p=+1.51$ (sign correct); mesons few-%. The $+12\%$ is $d_1$ again |
| G6 | Nuclear binding | QUANT | F104, F113, F126, F128, F240, F206 | 1 param ($b=0.55$ fm) | Deuteron $E_b$ 2.224 vs 2.22457 MeV (**0.026%**), $r_d$ 0.4%, on a **fully derived** OBE potential with no tuned hard core |
| G7 | Weak decays | PARTIAL | F54, F48 | absolute rates tied to $v$ | $d\to u+W^-\to u+e^-+\bar\nu$ end-to-end, 10/10. Structure exact; $G_F$ inherits the $v$ anchor |
| G8 | Scattering / S-matrix | MACHINE | F260, F259, F263, F264 | — | Tree QED S-matrix + crossing; Bloch–Nordsieck IR cancellation; Euler–Heisenberg, light-by-light, Schwinger pair production; renormalizability with $D=4-\tfrac32E_f-E_\gamma$ exact |
| G9 | Condensed-matter emergents | QUANT | F210–F215, F218, F242, F207, F171 | Allen–Dynes $6.3\%$ | $2\Delta/kT_c\to2\pi/e^\gamma$ and $\Delta C/C_n=12/7\zeta(3)$ at machine precision; $\mu^*$ **derived** from the F64 dielectric (no fit), cutting $T_c$ error $14.3\%\to6.3\%$. Casimir exact |
| G10 | Statistical mechanics / thermodynamics | **PARTIAL** (was ABSENT) | **F300** | equilibrium only; photon sector only; $g_*(T)$ not built | **Closed 2026-08-06 by F300.** The partition function is built on the model's own derived dispersion, not a continuum ansatz. $w=1/3$ and Stefan–Boltzmann are **theorems** in the IR (Euler's theorem on a degree-1 homogeneous $\Omega$), with closed-form lattice corrections $u/u_\text{SB}-1=(40\pi^2/441)\Theta^2$, $\tfrac13-w=(16\pi^2/1323)\Theta^2$, $s/s_\text{SB}-1=(4\pi^2/49)\Theta^2$ and the parameter-free ratio $C_u/C_w=15/2$, each against BZ quadrature to $\le5.0\times10^{-4}$. $T_\text{lattice}=3.719\times10^{31}$ K; **F297's continuum $p=\rho/3$ is safe by 44 orders at the BBN bottleneck** — an assumption graded, not a null. Fine-grained entropy conserved on a mixed state ($1.1\times10^{-12}$); coarse-grained entropy rises but **time-symmetrically** ($1.8\times10^{-4}$), so the arrow is the initial condition, not the dynamics. The free sector **cannot** thermalise: $2N$ conserved $n_\pm(k)$ fix a GGE (plateau/GGE $0.554\to0.998$ as the subsystem shrinks); Gibbs needs F110's interacting sector. Cannot reach `QUANT` while the EoS is equilibrium-only and $g_*(T)$ is unbuilt |

### H — Model integrity

| # | Requirement | Grade | Evidence | Note |
|---|---|---|---|---|
| H1 | Parameter count vs the SM's 19+ | PARTIAL | ledger above | 6 derived, 3 proven-free, 14 unaddressed. **Not cheaper than the SM in raw count**; the sectors it has built carry zero free parameters, which is the claim actually made. Do not let the headline drift from the second statement to the first |
| H2 | Falsifiability | **PARTIAL** (was QUANT) | Claims rev 3; `docs/reviews/`; `make health` | Register level is unchanged and strong: five falsifiers with numerical thresholds. **Instrument level is not.** All six individually-reviewed findings in the F20–F25 block had a verification that could not fail; 72 test files are UNFALSIFIABLE by the suite's own metric; F282's falsifier 5 had to be struck as unable to fire. The previous report asked the next sweep to check exactly this. See gap #2 |
| H3 | Out-of-sample survival | QUANT | Claims rev 3 | One clean instance: $m_Z/m_W=3/\sqrt7$ was fixed **before** PDG 2025 excluded CDF-II $m_W$; against the resulting $m_W=80.3692\pm0.0133$ it gives $-0.064\%$. Unchanged |
| H4 | Retraction hygiene | **PARTIAL** (was QUANT) | `docs/status/findings-supersession-triage-2026-08-04.md`; supersessions.yaml S1–S18 | Mechanism still exemplary — the supersession unit is a **check**, and S18 carries per-finding LIVE/DEAD text of a quality nothing else in the tree matches. Enforcement is the problem: all 16 ledger-named superseded findings still read `Confirmed — N/N PASS`; `apply_supersession_banners.py` and `test_no_orphan_banners` walk only `tests/` and `src/`, so `findings/` banners are hand-written and unverified; 4 of them (F20, F22, F64, F176b) have no ledger record. See gap #5 |
| H5 | Internal consistency of decisions | PARTIAL | key-decisions.md D1–D11 | Decisions 1–7 mutually consistent as written; D2 reversed on the record (S8). **Three live watch items:** `hypercharge.py` still writes derived hypercharges as literals under an "SM values" comment (F279 follow-up 1, unactioned); F251/F258 superseded by F277 with a sign flip and B9's number un-re-derived; `S14-P5.1` malformed decision id keeps a gate record red |
| H6 | Reproducibility | **PARTIAL** (was QUANT) | 47 gate records | **`make gate` was not seen green, and one record is confirmed red this run** — `supersession-ledger` FAILs on the S14 `P5.1` decision id, flagged three times since 2026-08-03 and still unfixed. Records grew 28 → 47, which is real progress in coverage. The three `scenario` physics gates were not exercised; a 45 s sandbox ceiling against a ~2 min barrier is now a standing measurement problem, not an incident |
| H7 | Module coverage | PARTIAL | D11 registry | **51 of 189 channel-driven (27.0%)**; 90 test-only, 24 unreferenced, 17 standalone, 25 `fork_live`, 23 `fork_unclaimed`, **`dead_candidate` 10 → 1**. The percentage fell because the denominator grew, not because wiring regressed |
| H8 | Claims without test records | PARTIAL | findings-index | **18 findings have no test record (was 28).** The four load-bearing ones the previous report named — F245, F246, F247, F278 — now carry gate-tier records. Remaining cheapest items: `derive_velocity_addition` and `derive_dielectric_noconfine`, both `partial` and untested |

---

## Method notes

**Graded from the indexes alone:** most of B, C, E, G. `findings-index.md`, the exactness tally,
`key-decisions.md` and `Claims-and-Falsifiers-Summary.md` (rev 3) carry enough.

**Rows that required a finding file or the changelog rather than a ledger:** A1 and B1/B2 (F291
§7, F292 §6 — the rubric-consequence and declined-inference sections exist nowhere else); E10
(F183 §L1 and F284 §5 — the index line for F183 says "exact Schwarzschild/Kerr" and does not
mention the core); K3, K5, K12 (F295 and F296 both **post-date every ledger**, and
`open-derivations.md` has not been audited since F256); A2 and G1 (the F20–F25 review verdicts and
ledger S18 — `findings-index.md` carries no review column, so this is only visible in
`docs/status/changelog.md` and `docs/reviews/`); H2, H4, H6 (the triage report and a live
`casim test --id` run).

**This is itself a finding about the ledgers.** `open-derivations.md` was last audited
**2026-07-19 at frontier F256**; the tree is at **F306**. Its G1 row is the authority for K9 and is
written as if the F282–F296 arc did not exist. Per this command's own rules I have **not** edited
it — flagged for a research session. `findings-index.md` has no review-verdict column, which is
why a REFUTED finding and a Confirmed one look identical there.

**Grades verified by spot-check** (the three I was least sure of):

1. **A1 PARTIAL** — checked F291 directly. §7 asks for this grade in these words: *"A1 should move
   `ABSENT → PARTIAL` on the next completeness run: the grade is not `EXACT` because the '+1' is
   structural and because S1/S2 lean on $s=2$."* It also states the honest boundary (losing S3
   *and* $s=2$ together reopens the question) and that B10 is untouched. Grade stands as written by
   the finding, not softened by me.
2. **E10 PARTIAL** — checked F183. The baseline note ("not worked out anywhere") is **wrong**.
   F183 §L1 is a gate-tested check ("L1 · PASS · quantitative") and §"the lattice-regulated core"
   calls it *"the model's substrate-level singularity resolution"*. Held to `PARTIAL` rather than
   `QUANT` because $r_\text{core}$ is a saturation estimate, there is no geodesic-completeness
   theorem, and F183's own Open/next lists the Kerr interior as unbuilt. The fix went to the grade,
   not to the citation.
3. **K3 OPEN** — checked F295 and F296. F295's §on F286: *"$p=0$ is not trivial — it is a
   scale-free anomalous dimension"*, with $dn_s/d\ln k\equiv0$ at sympy literal zero, and it
   explicitly repairs F285's row to read $\gamma\ne0$, $\gamma=0.017550$. F296 supplies a named
   operator and a named obstruction. `OPEN` is right; `EXCLUDED` was right only under a reading
   that its own author corrected three hours later. Note F295 §4 is careful that **the statistics
   did not improve** — F286 T5's count (6 hits in 396, $p=0.32$) applies unchanged to the $\tfrac29$
   coincidence, and no operator has been identified *in this model*. K3 is `OPEN`, not `PARTIAL`.

**Every F-number cited was checked to exist** (`findings/` plus `deprecated/findings/` plus the
F01–F15 bundle): 168 distinct numbers, zero missing. F16–F19 resolve in `deprecated/findings/`,
which is correct — they were retired 2026-08-03.

**Citations to superseded findings, carried with their supersession:** F251, F258 (→ F277, S12 —
and B9's number is un-re-derived, flagged); F162 (→ F272, S11 — apparatus re-verified by F287);
F165 (→ F279, S13 — conclusion retained, two steps retracted); F62 (→ F64, S3 — sign convention
still production code); F114 (→ F178, S4); F179 (→ F253, S6); F65/F66/F67 (→ F69, S1);
F155 (→ F277, S12); F270 (→ F271, S10); F21/F23/F25 (→ F306, S18, per-finding LIVE/DEAD);
F20 (partial, S18); F16–F19 (retired, S1/S16/S17).

**What this run could not verify.** `make gate` end to end, and therefore the three `kind:
scenario` physics gates — a 45 s call ceiling against a ~2 min barrier. Whether F277's refold fix
left B9's $\Delta\alpha(M_Z)=0.24\%$ re-blessed (second consecutive report). Whether the 10
`candidate` baselines represent regressions or accepted physics changes (second consecutive
report). Whether the 57 manifest-linked-but-undeclared artifacts are the C7 arming to-do the
checker calls them.
