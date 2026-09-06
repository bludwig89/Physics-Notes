# Completeness overview — 2026-08-20 - 15:50

*Graded against the external SM + GR + cosmology rubric in `.claude/commands/state-of-model.md`.
Scope: full sweep, 74 rows (blocks A, B, C, E, K, G, H) plus the 28-row parameter ledger (D).
Previous benchmark: `docs/status/completeness-2026-08-18.md`, as amended through its **Amendment 4**
(2026-08-18 - 17:15) — the requested baseline for this rerun. Health probe: run live against the
repository on Ben's machine via the device bridge (see below); `make gate` itself did not complete
in this session (see caveat) and is recorded as NOT VERIFIED THIS RUN, not as green.
Research prompts for every row below `MACHINE`: `completeness-2026-08-20-prompts.md` (81 prompts).*

**This is a two-day rerun, not a fresh sweep.** Two days separate this report from its baseline, one
of them (2026-08-19) carrying real work; the other (2026-08-18 evening → 2026-08-19 morning, and all
of 2026-08-20 up to this run) carries none, confirmed by `tail -n 200 changelog.md` ending at
2026-08-19 - 14:53 with nothing after it. **Physics did not move.** No finding, claim, or exactness
value changed between the baseline and this run. What moved is integrity bookkeeping — and one of
those bookkeeping fixes is large enough to move a rubric grade (H8).

## Health probe (what actually ran, and what could not)

Run live via the device bridge, one `make` target per call, from the repository root on Ben's
machine (`source .vendor/activate.sh` first):

| Target | Result |
|---|---|
| `make indexes-check` | **GREEN.** All 8 indexes current (`findings-index.md` 317 entries, `project-status-index.md` 56, `tests-index.md` 434, `code-index.md` 236, `docs-index.md` 143, `test-results/manifest.json` 412, `exactness-inventory.md` 540, `claims-index.md` 283). Finding numbers: max **F325**, 306 distinct, 317 files, 0 duplicates, 19 gaps (none undeclared), **NEXT FREE NUMBER F326** (no gaps at the top — this is max+1). Exactness header F325 vs newest F325 → 0 findings behind. `[casim index] ok` |
| `make registry` | `434 record(s) cover 412 test file(s), all valid (D9)`. Kinds: assertion 159, result_dump 225, scenario 3, legacy_script 47. Tiers: gate 85, battery — (declared debt 47) |
| `make numerics` (D8) | 286 modules scanned. Direct `np.fft` calls: **0** (must be 0 — is). Device-namespace fft calls: 8, in 1 file, behind `require_float64`. 165 files import numpy/scipy/ca_fft. Active backend: `numpy.fft` (pyfftw not installed — a performance note, not a correctness defect) |
| `make health` | 412 files: gate tier 25, battery 387, pytest-style 147, no-assert 231, UNFALSIFIABLE 70, import-time-physics 326. Test registry: 434 records (159 assertion / 225 result_dump / 47 legacy_script declared debt). Check-soundness: 82 gate-tier assertions, 91 declared controls (33 strong, 1 weak), **NO CONTROL 48 — unmoved since 2026-08-08**, exactly the baseline's committed ceiling |
| `make gate` | **NOT VERIFIED THIS RUN.** Started in the background (`nohup make gate > .tmp/gate_run_2026-08-20.log 2>&1 &`); the device bridge's per-call budget (≈45 s) is shorter than the gate's own run time (~2 min per the skill's own note), and the background process did not survive between tool calls in this session's bridge (log came back empty, no process found on the next poll) — a session/process-lifetime limitation of the bridge tooling, not a repository defect. **Command for Ben to run directly:** `cd "Physics Notes" && source .vendor/activate.sh && make gate` |

**Everything else in this probe is a genuine live measurement**, not a re-read of the baseline —
first time this project's completeness command has run with real device access rather than a staged,
isolated copy (contrast the 2026-08-18 report's header, which ran nothing live and graded from
committed artifacts alone).

---

## Scoreboard

| Block | EXACT | MACHINE | QUANT | PARTIAL | FIT | POSIT | OPEN | EXCLUDED | ABSENT | N/A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A Foundations (12) | 4 | 1 | 2 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| B Gauge (12) | 4 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| C Matter (7) | 2 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| E Gravity (13) | 3 | 1 | 4 | 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| K Cosmology (12) | 0 | 0 | 1 | 7 | 0 | 0 | 1 | 3 | 0 | 0 |
| G Emergent (10) | 1 | 1 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| H Integrity (8) | 0 | **2** | 1 | **5** | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total (74)** | **14** | **5** | **17** | **32** | **0** | **1** | **1** | **4** | **0** | **0** |

*Every cell counted from the grade column of the block's own table below. Against the baseline
(14 / 3 / 16 / 35 / 0 / 1 / 1 / 4): **three rows have moved since**: H8 `PARTIAL → MACHINE`,
(2026-08-27) A10 `PARTIAL → QUANT` (F331 closes F290's residual 1 — the interacting 3-D
cluster-decomposition claim), and (2026-09-06) H5 `PARTIAL → MACHINE` (X1, the row's last live
item, closed 2026-08-18 by F325; grading-integrity re-read, no new physics — see the row). Nothing
else in the 74-row rubric has changed grade.*

**Parameter ledger: 6 of 28 derived, 2 partial, 3 fitted or free input, 13 open or absent, 4
excluded (permanently free, a result, not a gap) — moved once since the fifth report: F353
(2026-09-03) confirmed the ν Dirac CP phase (#26) inherits F254's PMNS no-go verbatim, joining the
3 PMNS angles as proven-permanently-free rather than open.** No quark-mass, CKM, α, v, m_H or Λ work
has landed. **UPDATED 2026-09-05 (H1 re-tally):** F353's own edit updated the D-section tally below
but never reached this caption or the H1 row itself, and left an arithmetic double-count (PMNS
counted in both `fitted-or-free` and the new `EXCLUDED` bucket, summing to 31 of 28 items) — both
fixed here, no ledger movement beyond F353's own. F320's absolute m_W and m_Z still do not move this
ledger.

---

## The five things most worth building next

Ranked by (load-bearing × distance from closure). **Unchanged from the baseline** — nothing in this
window touched d₁, X1's residual (Q1/Q2/Q3), K9, B9, or Q4, and the baseline's own #1 (arm F324) is
now *done* (see below), promoting its list by one slot.

### 1. d₁ — the strong-sector one-loop background-field constant (was #2, now #1 by elimination)

**What.** The X1 colour-normalisation fork closed on 2026-08-18 (F325, branch B adopted), which
removed B10 from the fork's dependents but left the fork's largest cost untouched: the third leg of
`open-derivations` **d₁**, Δ C_vertex = −2.0160 (36.2 % of ΔC), bracket [−2.257, −1.446]. This is the
one open item standing directly between the tree and a quoted α_s(M_Z). **Nothing has been recorded
against it since F308 landed on 2026-08-11 — its third consecutive report at a standstill.**

**Why it matters.** Blocks B8, D16, G5, E3, Q1, Q2 — one of six zero-free-parameter claims.

**What blocks it.** `open-derivations` **L6** — which object is "the rule's gauge action" at finite
a — sits upstream and F305 deliberately declined to pick it.

**Smallest next step.** Decide L6, then run the native sweep at n=28–40 on the repaired path (F308).

### 2. K9 / G1 — the cosmological-constant residual is now a dynamics question, not a selectivity one — **PARTIALLY ATTACKED 2026-08-28 (F332)**

**What.** Adjudicated by the baseline's own Amendment 4 (2026-08-18 - 17:15): F193 Part A excluded
(uniform, inside CL275), F311 leg C3 withdrawn, F319 §6 narrowed. The surviving route — F193 §B/F196's
capacity ceiling — delivers 120.66 of the required 120.76 decades with a₁ untouched, short 0.10 dex =
Ω_Λ. **The price is met; the dynamics that would enforce the ceiling are what's missing**, and nothing
has moved on that specific question since the adjudication.

**Smallest next step.** Show the F164 zero-point sum is dynamically made to respect the F183 capacity
bound, or show that it is not — per `open-derivations` G1's restated target.

**UPDATED 2026-08-28 (F332, `findings/F332-cc-dynamics-two-channels-excluded.md`, verdict
CONFIRMED-NARROWER, full attack-and-fix pass complete).** Took the smallest-next-step question at
face value and tested three concrete dynamical channels rather than re-reading the ceiling: (1) is
the ceiling formula literally the model's own Friedmann-I constraint (F182) at L=R_H? — **yes**,
exactly, and the bare F164 sum's own self-consistent Friedmann horizon works out sub-lattice-cell,
which is itself informative about how far from the ceiling the bare sum sits; (2) can F164 channel
(ii) (AB≡1 dielectric sequestering) mechanistically act on a homogeneous vacuum-energy source at
all? — **no**, and not merely unevidenced: the static Poisson-type equation is exactly Fredholm-blind
to any spatially uniform source (the k=0 mode has zero response on a periodic domain), and F178
independently restricts the AB≡1 representation to T_μν=0 (vacuum) regions, never the matter/energy-
filled cosmological interior — this channel is **closed**, not merely unattempted; (3) does a literal
F130 block-spin coarse-graining of the F59/F164 Sakharov moments (a₀, a₁) reach F319 U8's required
order-selectivity (≥1.27×10¹¹⁶, with a₁ perturbed ≤2.2×10⁻⁵)? — **no**, by 35+ decades: a₀ falls as
~b⁻⁴ while a₁ *rises* as ~b under this transform, the wrong relative direction, worse than F319's own
uniform-λ "enhancement." **Net effect on the grade: none — still OPEN.** Two named candidate
mechanisms are now eliminated with computed content rather than left as unattempted possibilities,
narrowing what remains to try, but eliminating rivals is not itself the missing positive mechanism the
promotion bar (OPEN → PARTIAL) requires. The sole surviving candidate is unchanged: F193§B/F196/F241's
capacity ceiling, still undynamicised. See `open-derivations.md` row G1 for the updated ledger entry.

### 3. B9's real residual — the hadronic piece in row G3

**What.** B9's two published numbers were reconciled (Amendment 2): 0.0495 % model-internal headline,
0.00158 % after importing the Källén–Sabry constant. Both readings agree the true open target is the
two-loop leptonic bubble on the model's own fields (F261's dispersive machinery) — not yet attempted —
and that B9's *practical* precision ceiling is the hadronic vacuum-polarisation piece row G3 does not
derive (declared out of scope there).

**Smallest next step.** One session on F261's machinery for the leptonic bubble; separately, decide
whether hadronic VP is ever brought in-scope for G3.

### 4. Q4 — the isospin splitting the model's own BBN excludes at 36.6σ

**What.** Unmoved, now on its **third** report with nothing recorded against it. F297's BBN measures
m_n − m_p to ±0.0056 MeV; the model's +1.51 MeV is excluded at 36.6σ. F297 §10 item 1: fix the EM
self-energy term in F122, or show the F40 d–u ratio moves.

**Why it still leads the "cheapest live target" list.** Bounded numerical target, existing test,
no missing sector — this is the model finding its own error, not a coverage gap.

### 5. H2's retrofit backlog — 48 gate-tier assertions with no control, unmoved since 2026-08-08

**What.** Confirmed again live this run: `check_control_soundness.py` reports **48 NO CONTROL**,
identical to the number reported at every prior sweep back to 2026-08-08, while declared controls
continue to grow with new work (76 → 91 in two days, +15, all attached to findings written since
2026-08-18). The backlog is not shrinking; it is being outrun by new work that ships with its own
controls.

**Smallest next step.** Retrofit even five of the 48 in a session and the ratchet finally moves — it
has not moved in twelve days.

---

## What is ABSENT

**Still empty**, for the third consecutive report. No rubric row in blocks A, B, C, E, K, G or H is
graded `ABSENT`. This run inherits the baseline's own caveat rather than re-measuring it: a whole-tree
keyword grep (proton decay / B-violating rate; Unruh effect; topological defects as relics) needs a
tree-wide search this session's device-bridge budget did not extend to beyond the targeted greps
already run (see Method notes). Take the empty column at the same discount the baseline did.

---

## Regressions and changes since 2026-08-18

*Graded against the baseline as amended through Amendment 4 (2026-08-18 - 17:15).*

| Row | Was | Now | Why |
|---|---|---|---|
| **H8** Findings without a usable test record | PARTIAL, 16 findings + F324's declared-but-missing record | **MACHINE** | **2026-08-19 - 13:55, "H8 closed."** Of the 16 `no test record` findings, 14 had a test, a passing test, and a registry record all along — the join was broken by a wrong or absent `findings:` field on the record (ten `b`-suffix number collisions inherited from the C8.2 rename, four records with `findings:` unset entirely, two crediting only a co-author). Fixed by correcting the field, not by writing new tests. The genuine two gaps (F26b, F142) got real new gate records with measured controls. **Verified live this run**: `grep -c "no test record" findings-index.md` → **0**. `tests-index.md` now resolves 432→434 records against 316 findings with number collisions correct. Graded `MACHINE` rather than `EXACT` because the invariant is enforced by a checker script (`check_finding_records.py`) rather than a closed-form guarantee, and because the adjacent `audit_tests --ratchet` triple the same session flagged as going red-on-arrival from concurrent F324 work was **not reproduced** by this run's live measurement (see Method notes) — worth a direct re-check before calling the whole test-integrity picture settled |
| H6 Reproducibility (evidence only — grade unchanged) | PARTIAL; `make indexes-check` demonstrated RED (F324 in no index) | **PARTIAL still** | The specific defect that reddened indexes-check at the baseline (F324 invisible to every index) is now fixed and **independently verified live** this run: `make indexes-check` returns green with F325 as the newest finding and all 8 indexes current. That is real progress on H6's first named defect. The grade does not move because H6's second half — whether `make gate` itself runs clean end-to-end — remains **NOT VERIFIED THIS RUN** (see Health probe); a green `indexes-check` is necessary but not sufficient for a green gate |
| H2 Falsifiability (evidence only — grade unchanged) | PARTIAL, 78 gate-tier assertions / 76 controls / 48 no-control | **PARTIAL still**, 82 / 91 / **48** | Growth continues exactly on the baseline's own pattern: assertions +4, controls +15, all attached to new work; the no-control backlog is **still exactly 48**, unmoved since 2026-08-08 (now 12 days). Recorded as a number update, not a grade motion — the row already named this pattern and it continues unbroken |
| H4, H5, K9, K10, A11, B8, B10 — parameter #16, #28 | Amendment 3 / Amendment 4 states | **Unchanged** | These were already carried at their amended state in the baseline (this rerun's stated benchmark); nothing in the 2026-08-19–20 window touched claims, findings, or the public summary. Re-verified by reading the changelog tail directly rather than re-deriving: no entry after 2026-08-18 - 17:15 mentions a claim, finding, exactness value, or the papers directory until 2026-08-19's index/coverage/CLAUDE.md entries, none of which are physics |

### Also observed, not grade-worthy on its own

- **Test registry growth**: 429 → 434 records, gate tier 81 → 85 (roughly +4, consistent with the
  two new H8 gate records plus F325's own arming). Kinds now assertion 159 / result_dump 225 /
  legacy_script 47 / scenario 3.
- **Claims registry growth**: 280 → 283 cards; live 151 → 155; narrowed 5 → 6; withdrawn 27 → 25;
  `unreviewed-seed` 223 → 222. Net movement is small and does not touch any headline card cited by
  this rubric.
- **Exactness inventory**: class counts **unchanged** (exact 159 / machine 196 / quantitative 185,
  coverage 540/540), but the artifact count ticked 446 → 448 and the generated-through marker moved
  F323 → **F325**. F324/F325 evidently did not add new residual-bearing entries to this specific
  ledger even though they landed two new gate records elsewhere — worth a one-line note in the next
  sweep if it recurs, since it is a slightly surprising null.
- **`findings-index.md` now sorts in finding-number order** (2026-08-19 - 15:20) — cosmetic, no
  content, summary, status or count changed.
- **Finding-coverage rollout §4 bucket 1** (2026-08-19 - 13:35): 24 pre-convention findings (F21–F48
  era) had their `findings:` joins repaired; the coverage audit's `weak_only`/`untested` metric moved
  66 → 30. This metric is not itself a rubric row (it is upstream evidence for H7/H8) and H7's own
  module-registry fraction was not re-measured live this run (`casim` module-registry check was not
  among the targets this session's device-bridge budget reached) — **H7 stays PARTIAL, carried, not
  re-verified**.
- **`docs-index.md`** was one row stale (missing the new `finding-claim-test-guide.md`) as of
  2026-08-19 - 14:53; this run's live `make indexes-check` shows it **current**, so that gap has
  since closed (presumably by a `make indexes` run not separately logged, or folded into the
  2026-08-19 - 15:20 entry).

**Nothing else moved.** No new finding landed (max is still F325, confirmed live), no claim changed
status, no exactness value changed, and the baseline's own five priorities (d₁, X1 residual, K9, B9,
Q4) are untouched except where already closed by the baseline's own amendments.

---

## Full rubric

*Unchanged rows are carried verbatim from `completeness-2026-08-18.md` as amended through Amendment
4 — re-verified against the changelog and, where practical this session, against a live measurement
(see Method notes for which). Only **H8** differs from the baseline text.*

### A — Foundations

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| A1 | Spacetime dimensionality | PARTIAL | F291, F292, F313, F316, F318, F326 | the three Cayley generators; infinite volume; single-generator QCA dynamics is a named posit, not derived | Two independent selectors each return {3}; d=6/d=9 excluded; F318 removes F291 §3's self-flagged conditionality; F313's commutant identity and "d_space=3 from the commutant" are WITHDRAWN by its own remediation as numerology/circular. F326 (2026-08-20) closes the last open question about the "+1" — no second candidate generator exists, from BDPT uniqueness and F313's own closed commutant — and names single-map-iterated dynamics as the residual posit (`open-derivations.md` Part C row P1); grade unchanged, this is a residual restatement, not a promotion |
| A2 | Lorentz invariance | PARTIAL | F26, F28, F30, F246, F129, F301, **F327** | **UPDATED 2026-08-26 — the residual is now a FALSIFICATION, not an unconfronted number.** deformed shell exact but not universal; the chiral coefficient has been confronted and is EXCLUDED | F327 converts F301's chiral O(\|k\|²) defect through the F79/F107 ruler into a local dimension-5 CPT-odd operator, \|η\|max = 2√(8π)3^(1/4)/9 = 1.4662, E_LV = (9/2)E_a = 8.33e18 GeV, and LHAASO/Crab electrons exclude it by **7.05 decades** (5.08 subluminal). Localised on ONE leg: an elementary fermion may not ride a single BCC chiral branch (CL284); F301's algebra is untouched and CL262 is narrowed, not withdrawn. `open-derivations` **L8 closes → L9** (a branch-paired unitary massive propagator; no local mass mixing supplies one). Stays PARTIAL — the row is now *tighter* (named, bounded, actionable) and *worse* (the bound is violated), which is the honest reading |
| A3 | Causality / locality / finite speed | EXACT | F26, F204, F227, F290 | 0 | c_lat=1/√3; strict cone measured tight |
| A4 | CPT, and C/P/T separately | PARTIAL | F53, F321, **F328** | **UPDATED 2026-08-26 — an exact free-sector CPT theorem now exists; the gauge-coupled extension is the named residual.** No prior module built C, P or T as an operator on the one-tick unitary (F53 is charge-label bookkeeping, not an operator theorem) | F328 builds $\Theta=\Sigma\cdot(\sigma_y\!\oplus\!\sigma_y)\cdot K$ (reflection + an internal spin/chirality twist + complex conjugation) and proves $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ **exactly** at every $\mathbf k$ and every $\lvert m\rvert\le1$, no small-$k$ expansion, for the free (gauge-decoupled) massive BCC Dirac walk; $\Theta^2=-1$ (Kramers). Separately proves **no fixed unitary parity can exist at any finite $\mathbf k$** ($D(\mathbf k)$ and $D(-\mathbf k)$ have different spectra — a spectral re-derivation of F301's chirality-odd defect, independent of F327's experimental exclusion of a single physical branch). Stays PARTIAL: the SU(2)$_L$ charged-current extension (F53's own "C, P maximally violated by the coupling") is a **named** open item (ledger row **A4r**), not an unexamined one. Explicitly does NOT reuse F321's $\theta_\text{QCD}$ reality result (a different object, row B11) |
| A5 | Unitarity | EXACT | F276, F264, F300 | 0 | Length-preserving by construction |
| A6 | Superposition + Born rule | **EXACT** | F304, F312, **F329**, F281, F290, F227 | 0 | **UPDATED 2026-08-27 — the last residual (Cooke–Keane–Moran regularity) is closed.** Gleason's dichotomy proved for $f\in L^2$ (F304 §5); non-contextuality closed by theorem for both gauge groups (F312); the regularity bridge from bounded to $L^2$ closed by F329, which shows the identical proposition is Gleason's own 1957 Theorem 2.8 + Theorem 3.5 reduction, requiring nothing beyond non-negativity, compactness, and dim$\ge3$ — verified machine on every dimension this model builds a measurement context on. CL264: `contingent → live` |
| A7 | Entanglement, Bell/Tsirelson | EXACT | F212, F226, F214, F217 | 1.8e-15 | Tsirelson saturated exactly |
| A8 | Measurement problem / classical limit | EXACT | F281, F130, F41 | 0 (A6's Born legs closed 2026-08-27, F329) | Pointer basis forced; classicality a block-spin attractor |
| A9 | Spin-statistics | PARTIAL | F289, F291, F292, F217, **F330** | topological step external, now precisely named | **UPDATED 2026-08-27 — the residual is now a NAMED postulate, not a vague import.** F330 pins the belt trick's non-topological content to Anastopoulos's Postulate 1 (quant-ph/0110169: exchange must be a smooth SO(3)-orbit path composing, twice, to one 2π rotation) and machine-verifies its spin-½ consequence on the model's own rotor (the antisymmetric singlet is an exact scalar under R(θ,n)⊗R(θ,n) for every θ,n; the symmetric triplet is not, at θ=π) — closing the mechanism F289 itself left unexhibited (*why* spin-½ picks −1, not merely that ±1 are the only options). A lattice-native derivation was attempted and abandoned with a stated structural reason (O_h is finite and carries no π₁(SO(3)) content; the rotor's Ω(k) is dynamical, not kinematic/parallel-transport). π₁=S_n and Postulate 1 itself both stay external |
| A10 | Cluster decomposition / no-signalling | QUANT | F290, F227, **F331** | **UPDATED 2026-08-27 — F290's residual 1 closed.** kappa_100 ratio 1.17 at default m=0.5 (residual shrinks monotonically with mass: 1.53 at m=0.05 to 0.95 at m=0.95) | F331 extends F290's 1-D free-fermion clustering to the interacting (lattice-native NJL mean-field), 3-D BCC theory: an exact closed-form kappa_100(m)=sqrt3*arccosh(1/sqrt(1-m^2)), from a genuine 3-D pole extremisation (proved dominant, not assumed), validated against the model's own dispersion once the CORRECT Brillouin zone is used (the naive cubic FFT grid is F267's own hazard, hit and fixed here, not just avoided); a self-consistent NJL gap equation dynamically generates a mass from a bare-massless start; cluster decomposition confirmed AT that mass. Mean-field only (F77's own scope); F290's separate 1-D exponent-shortfall residual (item 2) and S-matrix-level clustering remain open |
| A11 | UV completeness | QUANT | F116, F164, F264, F284, F319, **F332** | one number: ρ_vac, 10^120.76 | Two cutoff-carrying coefficients, one right (G) one wrong by 120.8 orders. K9's Amendment-4 restatement is this row's residual's candidate mechanism — still no dynamics. **UPDATED 2026-08-28:** F332 closes two of the candidate mechanisms (see K9); this row's residual is unchanged, still one number |
| A12 | Continuum limit | MACHINE | F129–F135, D1 | ‖[R_b,evo]‖≤1.8e-15 | c_lat an exact RG fixed point |

### B — Gauge structure

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| B1 | Origin of SU(3)×SU(2)_L×U(1)_Y | PARTIAL | F27, F51, F43, F291, F317, F318, F324, **F333** | two named observational facts (baryons are fermions; quarks are confined), not one bare fiat | Reduced six-to-one by F317 (unitarity, specialness, locality⇒connection, vector-likeness); F318 shows the cell permits but does not force the index's existence. **UPDATED 2026-08-28:** F333 narrows F318/F324's "index exists by fiat" further — N>1 is forced given (a) real baryons are fermions and (b) quarks are confined (dim su(1)=0, no gauge boson), combining a generalised SU(N) constituent-count theorem with a computed composite-exchange-parity rule; independently reproduces F324's post-S22 {3,5,7,…} bracket as a cross-check. N_c=3 itself untouched (still F317 §6 / F318 §D / F324's) |
| B2 | Chirality | EXACT | F27, F91, F292 | Ward identity 1.1e-17 | W± chiral forced; F292 independent Clifford-recursion route |
| B3 | Anomaly cancellation | EXACT | F38, F293, F324 | Witten check physics-verified, tree-unverified | All six traces exactly zero; F324 W2/W2b discharges the four-report-old Witten SU(2) residual |
| B4 | Hypercharge / charge quantisation | EXACT | F165 (S13→F279), F279, F47, F51, F38 | one charge unit + N_c=3 for the thirds | Rank 6, dim 1 over ℚ |
| B5 | EWSB mechanism | EXACT | F27, F34b, F44 | 0 | Higgs-free Stueckelberg; m_A=0 from rank-deficient mass matrix |
| B6 | Weinberg angle, with scale | QUANT | F138, F49, F231, F141, **F334** | +0.222% at M_Z; −0.064% on shell; 0 free params | ¼ is the μ*=4πv matching value; 2/9 its on-shell face. **UPDATED 2026-08-30:** F334 gives the shared hadronic-VP residual (below, B9/G3) a first model-internal ρ+ω VMD estimate, 10.2% of DHMZ2020's Δα_had⁽⁵⁾(M_Z); grade unchanged, residual narrowed not closed |
| B7 | Confinement | PARTIAL | F70, F86, F88, F299, F323, F265; F94 partially superseded (S21→F323, F265) | 3+1D constructed, not proven | 2D exact area law; 4D residual unmovable by sampling absent reflection-positivity machinery |
| B8 | Asymptotic freedom / α_s running | PARTIAL | F144, F151, F239, F235, F287, F280, F299, F303, F325 | **d1 leg 3 alone** (X1 fork closed 2026-08-18) | b0=11/3 C_A=11 exact. X1 RESOLVED (F325, S22): branch B (g_s=½) adopted on two legs independent of d1. α_s(M_Z)=0.1186 (+0.5%) no longer contingent on the branch, still contingent on d1 leg 3 (unmoved since 2026-08-11 — see priority #1) |
| B9 | Running of α, EW couplings | QUANT | F322, F311, F251⚠(S12→F277), F261, F138, F231, F115(S20→F138,F231), **F334** | 0.0495% model-internal headline; 0.00158% after importing Källén–Sabry | Reconciled by Amendment 2 (2026-08-18): additive, not rival. Real open residual is the hadronic piece in G3 (priority #3). **UPDATED 2026-08-30:** F334's ρ+ω VMD piece (zero imported couplings, from the model's own g_ρππ) closes 10.2% of the EW-leg gap, sin²θ_W residual +0.450%→+0.427% on the model's own leptonic alpha; the two-loop non-log constant (this row's OTHER open target) is untouched |
| B10 | Why 3 colours | PARTIAL | F293, F294, F298, F299, F303, F324, F325, F279, F144, F110 | odd N_c only, {3,5,7,...}, not closed to {3} | AMENDED by F325 (S22): F324's upper constraint (CN19) withdrawn as a mixed-matching artefact; ℤ2 doublet-parity leg (prior art, Bär & Wiese) survives untouched. B10 exits the X1 fork by X1 closing, not by the selector retiring |
| B11 | Strong CP / θ_QCD | QUANT | F321, F53, F305, F307, F91, F337, F340 | arg det M_q at three generations (E6/E7); lattice topological-charge quantization (distinct from θ=0, standard lattice-QCD subtlety) | Reality of Euclidean action IS θ=0, from closure of the minimal loop set under reversal. Not a solution of strong CP (CL279 deliberate non-claim). **UPDATED 2026-08-31 (F340):** the action-fork dependency F321 §6 named is CLOSED — F337/L6 decided F321's construction was already on the correct branch (rhombic action's own quadratic form, not F26/Ω_even) — and reality is now proved exactly (not sampled) for the full non-perturbative configuration space; the model's Z, as constructed, is definitionally the θ=0 sector-sum (cross-checked against Vafa–Witten 1984). |
| B12 | Gauge-boson masses, ρ, m_Z/m_W | QUANT | F49, F141, F138, F231, F320 | v and α (two anchors); F141's hypothesis (U) | Model takes two EW inputs vs SM's three. ρ=1 exactly from F41's Stueckelberg rank. Now core claim 12 (CL276/CL277) in the public summary as of Amendment 3 |

### C — Matter content

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| C1 | Exactly three generations | PARTIAL | F75, F84, F292, F342 | physical identification is a stated hypothesis | Group theory a theorem (ΣdΒ²=48 ⇒ T_1u unique); identification a hypothesis. F324 makes the generation-count *parity* load-bearing for B10 too. **UPDATED 2026-08-31 (F342):** not merely unproven — F75's own condition (i) ("identical gauge quantum numbers") is shown to supply zero power to select T_1u over T_2g under the site-diagonal charge structure the adopted engine actually implements, forced by the shell's 8 vertices forming a single O_h orbit. Grade unchanged; the reason it stays PARTIAL is now sharper and checkable (`casim test --id F342-generation-identification-gap`) |
| C2 | First-generation multiplet | EXACT | F38, F41, F42, F51, F165(S13→F279), F279 | 0 | Complete and anomaly-free |
| C3 | Colour triplet + fractional charge | PARTIAL | F136, F165(S13→F279), F279, F324 | conditional on N_c=3 via F324's premises | Fractional charge forced by 3y_Q+y_L=0; commensurability holds for any N_c |
| C4 | Neutrino nature (Dirac vs Majorana) | PARTIAL | F47, F266 | — | ν_R structurally forced total singlet; nothing forces Majorana over Dirac |
| C5 | Neutrino mass mechanism | PARTIAL | F47, F236, F254 | M_R free | See-saw + E_g/ℤ3 texture fix masses/hierarchy at machine precision; absolute scale unfixed |
| C6 | Antimatter / charge conjugation | EXACT | F53, F260 | 0 | Per-species C; positron and crossing sector built |
| C7 | Beyond-SM content | PARTIAL | F223, F228, F266, F216, F204, F237 | geon abundance free; no B-violating rate anywhere | Planck-mass BH-remnant geon predicted; excludes its own alternatives (CN5, CN6, Alcubierre, keV sterile as 100% DM). Proton-decay sub-row carried, not re-measured this sweep (needs whole-tree grep) |

### D — The parameter ledger

| # | Parameter | Grade | Evidence | Note |
|---|---|---|---|---|
| 1–6 | m_u, m_d, m_s, m_c, m_b, m_t | ABSENT ×6 | F121 | Quark masses are a consistency readout, not a derivation. `open-derivations` E6; no route proposed |
| 7–8 | m_e/m_τ, m_μ/m_τ (shape) | QUANT ×2 | F175, F234, F120 | ≤0.007% with zero shape parameters |
| 9 | Charged-lepton overall scale | FIT (N=1) | F121, F233 | τ-anchored; F233 reduces the gap to factor 1.9 via the α_s transmutation channel — inherits d1 |
| 10–13 | CKM 3 angles + 1 phase | ABSENT ×4 | — | Declared out of scope; J(1)=0 is one-generation arithmetic |
| 14 | α_em | OPEN | F127 | Four-avenue no-go on deriving it from the rule |
| 15 | g2 / sin²θ_W | QUANT | F138, F49, F231 | Derived with scale, +0.222%, 0 parameters |
| 16 | g3 / α_s | PARTIAL | F144, F239, F287, F280, F303, F325 | X1 fork closed (F325); d1 leg 3 the sole remaining blocker; α_s(M_Z)=0.1186 |
| 17 | v | FIT (N=1) | F119, Scope | Anchor, not output; now carries m_W, m_Z absolutely |
| 18 | m_H | OPEN | F73 | Kinematics exact; binding dynamics missing |
| 19 | θ_QCD | PARTIAL | F321, F53 | No longer independent; θ̄=θ+arg det M_q, first term zero at every order |
| 20–21 | 2 light-ν mass ratios | MACHINE ×2 | F236 | E_g/ℤ3 texture fixes masses and hierarchy at machine precision |
| 22 | ν absolute scale (M_R) | OPEN | F47, Scope | Nothing in the model fixes M_R |
| 23–25 | 3 PMNS angles | EXCLUDED ×3 | F254 | Proven no lattice selector — three inequivalent 1-d irreps under D_2h. Permanently free, a result |
| 26 | ν Dirac CP phase | EXCLUDED | F353 | **UPDATED 2026-09-03:** confirmed formally (F353) -- the D_2h stabiliser transports a complex T_2g entry by the same real sign as a real one (never rotates its phase), so F254's no-go transfers verbatim; F254's real fit gives J=0 exactly (a consequence of real-only inputs, not a protected value), and independent phases populate a generic, unprotected J. `open-derivations` D4 |
| 27 | G | EXACT | F79, F107 | Structural, 3e-8 vs CODATA, 0 free parameters |
| 28 | Λ | OPEN | F164, F192, F193, F196, F241, F311, F319, **F332** | See K9/priority #2. Price met to 0.10 dex; dynamics of the ceiling is the open item. **UPDATED 2026-08-28:** F332 closes two candidate mechanisms (dielectric sequestering; naive block-spin) without supplying a positive one — grade unchanged |

**Ledger tally — UPDATED 2026-09-03 (F353); arithmetic corrected 2026-09-05.** Derived with zero
free parameters: 6 (#7-8, #15, #20-21, #27). Partial, one named residual each: 2 (#16, #19). Fitted
or free input: 3 (#9, #14, #17 — lepton scale, α_em, v; the 3 PMNS angles moved out of this bucket
into EXCLUDED below, since F353 gave them their own bucket without removing them from this one,
which had left the tally summing to 31 of 28 items). Open or absent: 13 (was 14 -- #26 moves to
EXCLUDED). EXCLUDED (permanently free, a result, not a gap): 4 (#23-25 + #26, all four now
F254/F353). Total 6+2+3+13+4=28, checked.

**How to read that against the SM's 19.** Not "6 beats 19". The model derives 6 quantities the SM
takes as free, proves 4 more permanently free (3 PMNS angles + the ν Dirac CP phase — itself a
result, not a gap), and does not yet address 13, of which 10 are quark masses and CKM. **The chain
vs count caveat, updated:** of the 6 derived, sin²θ_W (#15) still sits downstream of the v anchor
(its MS-bar/on-shell reconciliation runs through the scale μ*=4πv, F138/F231) — that link is
unchanged. The X1 fork named in earlier reports is no longer a live dependency: X1 closed 2026-08-18
(F325, branch B adopted), so nothing here is downstream of an *unchosen* branch anymore. What
replaced it: the two PARTIAL rows each carry their own separate residual now — α_s (#16) is blocked
solely by d1 (the strong-sector one-loop background-field constant, still open, this file's own
priority #1), and θ_QCD (#19) reduces to a function of the quark-mass texture (θ̄=θ+arg det M_q,
first term zero at every order) — i.e. downstream of rows #1–6, still ABSENT. The charged-lepton
scale (#9, FIT) also inherits d1 via F233's transmutation channel. So "zero free parameters in the
sectors we built" is still true of the *count* and not of the *chain* — the specific links have
just moved from (v, X1) to (v, d1, quark masses).

### E — Gravity and general relativity

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| E1 | Fundamental field equation | POSIT | F178, F297 | — | DECISION 2026-06-29; independently confirmed by F297's BBN |
| E2 | Equivalence principle | MACHINE | F64, F62(S3→F64) | — | — |
| E3 | PPN β, γ | EXACT | F64 | β=γ=1 exactly | GR-identical |
| E4 | Classical tests | QUANT | F64, F107, F111 | 3e-8 | Mercury, deflection, Shapiro, redshift |
| E5 | Newton's constant | EXACT | F79, F107 | 3e-8 vs CODATA | Structural. Load-bearing premise of the K9 candidate route (uses G, doesn't perturb it). F332 (2026-08-28) reuses the CODATA relative uncertainty 2.2e-5 as the exclusion budget for a block-spin K9 channel — G itself untouched |
| E6 | GW speed, polarisations, dof | EXACT | F180, F248, F216 | ≤3e-83 | c_grav=c_γ a genuine zero |
| E7 | Inspiral / ringdown QNM | QUANT | F189, F187 | <7% (WKB) | GW150914 chirp mass, ISCO |
| E8 | Black holes | **EXACT** | F183, F186 | 0 — b_c=3√3 M exact, 0% vs GR (was +4.63% under the withdrawn F114 object, replaced by F178) | **UPDATED 2026-09-03 — grading-precision correction, not new physics.** Exact Schwarzschild/Kerr with horizon. F183's own ledger check X1 states the comparison directly (`F114_shadow_pct_vs_GR`=4.627%, `F178_shadow_pct_vs_GR`=0.0, `test-results/F183_blackhole.json`): b_c=3√3 M is the closed-form Schwarzschild photon-sphere result (Birkhoff ⇒ exact vacuum solution), not a fitted or approximate quantity, so "shadow 3√3 M" in this row's old residual column was a labeling holdover from before F114's withdrawal (when the model's actual prediction, 2eM=5.437M, really was a +4.63% QUANT-tier deviation). Two independent numeric cross-checks confirm without moving the value — F183's own photon-sphere solve agrees to 7.0e-11 and F186's independent backward null-geodesic ray-trace agrees to 1.45e-5 relative (`test-results/F186_shadow_raytrace.json`) — both floors are integrator truncation, not physics. Meets this project's own `EXACT` definition (closed form, zero free parameters), matching the E3/E5/E6 convention where an EXACT row's residual column states the achieved closed-form value rather than a tolerance. Scoreboard tally, prompt-coverage ratchet, and `completeness-2026-08-20-prompts.md`'s E8 prompt left for the next full sweep to reconcile (this file's scoreboard is already stale against other inline updates, e.g. A6's 2026-08-27 promotion). No finding/test/claim change — see changelog 2026-09-03. |
| E9 | BH thermodynamics | PARTIAL | F190, F183, F300 §5 | one posited constant; target now an entanglement entropy | S=A/4 iff each cell carries 2π√3 nats; F300 proves the state-count reading impossible |
| E10 | Singularity resolution | PARTIAL | F183 §L1, F284 §5 | r_core a saturation estimate | Kretschmann saturates at cell scale; no geodesic-completeness result |
| E11 | Interior / TOV / NS EoS | QUANT | F181, F184, F185 | — | SLy M_max=2.08 M☉, R(1.4)=11.1 km |
| E12 | Quantum-gravity sector | QUANT | F216, F248, F79, F357, **F359** | graviton-graviton scattering amplitude / dynamical partial-wave unitarity bound still not computed | Graviton massless, 2 dof (F216/F248, exact). F357 (2026-09-03): the qualitative "lattice is the cutoff" note is a computed, closed-form number -- the paired photon/graviton dispersion law is bounded above by $\pi$ radians/tick EXACTLY, giving $E_\text{max}=\sqrt{\pi\sqrt3/8}\,E_\text{Planck}=0.8247\,E_\text{Planck}$ via F79/F107's registered ruler (zero new free parameters) -- a **kinematic** ceiling, explicitly scoped away from A11/K9's $\rho_\text{vac}$ residual (CL297, session `quiet-precise-regge`). **UPDATED 2026-09-03 (F359):** the *dynamical* half F357 left open is sharpened, at a kinematic-threshold tier: a head-on collision of two of the model's own band-top quanta carries CM energy exactly $\sqrt\pi\approx1.77$ times the rest-mass energy of the model's own exact one-cell Planck-mass black-hole remnant (F228's $M_\text{rem}$, re-derived here from the SAME registered ruler as F357's $E_\text{max}$, so the ratio is $A$-independent and exact-algebraic, zero new free parameters) -- a single quantum alone falls short ($\sqrt\pi/2\approx0.89$). This exactly clears the necessary *energetic* precondition of the standard "self-completeness via classicalization" resolution of the naive graviton-graviton unitarity puzzle (Dvali--Gomez 1005.3497; 't Hooft 1987) -- that literature's own criterion is geometric (a hoop/impact-parameter condition), which is **not** computed here, and **no scattering amplitude, cross-section, or partial-wave bound is computed** either (CL298); the geometric criterion and any dynamical calculation are the residual now named precisely and are the natural next attack if this row is to close further. |
| E13 | Galactic-scale consistency | EXCLUDED | F194, F191, F358 | — | Emergent-gravity route falsified by Bullet Cluster; dark source required. **RE-EXAMINED 2026-09-03 (F358, ledger S23):** exclusion survives against the live 2026 Hernandez/Famaey MOND-QUMOND dispute and JWST-refined offset (Rihtaršič et al. 2026); F194's "regardless of clump shape" over-claim withdrawn, bottom-line verdict retained and independently reinforced |

### K — Cosmology

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| K1 | FRW background | QUANT | F182, F188, F284 | measured Ω's in | Solved with the model's source, not derived from the lattice |
| K2 | BBN / light elements | PARTIAL | F297, F309, F79, F178, F182, F284 | η_b free; network offset −0.87%; ⁷Li not validated | g*(T) closed by F309; m_Eg>125.5 MeV bound produced as a byproduct |
| K3 | CMB peaks, n_s | PARTIAL | F310, F295, F296, F285, F286 | value of one non-integer block-spin eigenvalue | Model needs no 3D dual; γ≡y−1 identically. Unmoved since baseline |
| K4 | Inflation or substitute | EXCLUDED | F282, F283, F296, F238 | cause named + 4 falsifiers | No slow-roll direction exists |
| K5 | Primordial spectrum normalisation | EXCLUDED | F282, F284, F285, F238 | A_s free, cause named | P(k) is an automaton initial condition |
| K6 | Baryogenesis | PARTIAL | F202, F47, F53 | magnitude not derived; no B-violating rate | All three Sakharov conditions met structurally |
| K7 | Dark-matter identity | PARTIAL | F223, F228, F266, F216, F237 | — | Candidate: graviton–graviton J=2 geon, Planck-mass remnant |
| K8 | Ω_DM h²=0.12 | EXCLUDED | F238, F282–F285 | free input, cause named | Provable non-derivability given no inflaton |
| K9 | Λ magnitude | OPEN | F311, F319, F164, F192, F193, F196, F241, **F332** | dynamical enforcement of the F183/F190 capacity ceiling on the F164 sum, plus Ω_Λ | Adjudicated Amendment 4: F193 Part A excluded, F311 C3 withdrawn, F319 §6 narrowed. Price met to 0.10 dex; no dynamics. **UPDATED 2026-08-28 (F332):** two candidate dynamical mechanisms tested and closed — F164 channel (ii) (AB≡1 dielectric sequestering) is Fredholm-blind to any homogeneous source (structurally, not merely unevidenced — a uniform source has zero response at k=0 on the periodic static equation), and F178 restricts AB≡1 to T_μν=0 regions, never the matter-filled cosmological interior; a literal F130 block-spin coarse-graining of the F59/F164 Sakharov moments is excluded by 35+ decades beyond the CODATA G budget (a_0 ~ b⁻⁴ falls while a_1 ~ b simultaneously rises — the wrong direction, worse than F319 U8's uniform-λ route). Also shows the ceiling formula IS the model's own Friedmann-I law (F182) evaluated at L=R_H, not an independent import, and that the bare F164 sum's own self-consistent Friedmann horizon is sub-lattice-cell. Negative result: two candidates eliminated with computed content, but no positive mechanism supplied — sole surviving route (F193§B/F196/F241's ceiling) untouched and still undynamicised. **Grade holds at OPEN** (does not meet the promotion bar: elimination of rivals is not itself a mechanism). Priority #2, still open as of 2026-08-28 |
| K10 | Dark energy w, vs DESI | PARTIAL | F192, F203 | sign exact; magnitude open | w=−1 sign correct; C2's "vacuous" reading stays conditional (Amendment 4: do not absorb yet, since the ceiling route caps near ρ_crit rather than zeroing) |
| K11 | Structure formation / σ8 | PARTIAL | F288 | A_s free; EH98 T(k) imported | Zero free functions vs EFT-of-DE's two; DES Y6 falsifier live (3.00σ) |
| K12 | Cosmological initial conditions | PARTIAL | F284, F285, F286, F295, F296, F238, F310 | one anomalous dimension, now internal | Same operator as K3 |

### G — Emergent and precision physics

| # | Requirement | Grade | Evidence | Residual / free inputs | Note |
|---|---|---|---|---|---|
| G1 | Maxwell / classical EM | EXACT | F26, F87, F245, F246, F306, F314; F25(S18→F306) | 0 | Composite-photon curl closes at O(k³) exactly |
| G2 | Hydrogen, fine structure, Lamb | QUANT | F125, F252, F257, F262 | Lamb=99.5% of measured | −13.596 eV from m_e+α alone |
| G3 | g−2, electron and muon | PARTIAL | F252, F261, **F334** | hadronic + EW absent by declared scope | a_e=α/2π exact; hadronic VP/HLbL/EW not claimed — B9's real ceiling (priority #3). **UPDATED 2026-08-30:** F334's ρ+ω narrow-resonance VMD estimate (B9/B6's shared target) captures ~10.2% of DHMZ2020's Δα_had⁽⁵⁾(M_Z) with zero imported couplings; φ, the multi-hadron continuum, and charm/bottom are still entirely absent — grade unchanged at PARTIAL |
| G4 | Atomic structure / periodic table | QUANT | F148, F195, F208 | light elements only | H/He/Li/C certified stable |
| G5 | Hadron spectrum | QUANT | F123, F124, F235, F122, F297 | 1 anchor (f_π); √σ/f_π +12% (d1); m_n−m_p excluded at 36.6σ | Priority #4 (Q4) lives here and in G7 |
| G6 | Nuclear binding | QUANT | F104, F113, F126, F128, F240, F206 | 1 parameter (b=0.55 fm) | Deuteron E_b 0.026% |
| G7 | Weak decays | PARTIAL | F54, F48, F297 | absolute rates tied to v; τ_n wrong by 2.7× | Same Q4 defect as G5 |
| G8 | Scattering / S-matrix | MACHINE | F260, F259, F263, F264, F258(S12→F277) | — | Tree QED S-matrix, crossing, IR cancellation |
| G9 | Condensed-matter emergents | QUANT | F210–F215, F218, F242, F207, F171 | Allen–Dynes 6.3% | μ* derived from F64 dielectric, no fit |
| G10 | Statistical mechanics / thermodynamics | PARTIAL | F300, F309 | equilibrium only | w=1/3, Stefan–Boltzmann theorems; free sector cannot thermalise |

### H — Model integrity

| # | Requirement | Grade | Evidence | Note |
|---|---|---|---|---|
| H1 | Parameter count vs SM's 19+ | PARTIAL | ledger above | 6 derived, 4 proven-permanently-free (was 3 — F353 adds the ν Dirac CP phase, 2026-09-03), 2 partial, 3 fitted/free input, 13 unaddressed. **UPDATED 2026-09-05:** re-tallied against F353, which had updated the D-section tally but never reached this row or the Scoreboard caption; also fixed an arithmetic double-count in the D-section tally (see there). Chain-vs-count caveat restated there too — X1 closed 2026-08-18 so no longer a live dependency; sin²θ_W still downstream of v, α_s now downstream of d1 alone, θ_QCD downstream of the still-ABSENT quark-mass rows |
| H2 | Falsifiability | PARTIAL | `docs/claims/`, `tests/registry/`, live `make health` this run | Register half unchanged and strong. Instrument half: 82 gate-tier assertions (was 78), 91 declared controls (was 76), **48 NO CONTROL — unmoved since 2026-08-08, now 12 days**. `unreviewed_seed` 222/283 (was 223/280) |
| H3 | Out-of-sample survival | QUANT | Claims rev 5 | m_Z/m_W=3/√7 fixed before PDG 2025 excluded CDF-II m_W: −0.064%. Still the only clean instance |
| H4 | Retraction hygiene | PARTIAL | supersessions.yaml S1–S21; `check_superseded_citations.py`; `check_summary_claims.py`; Claims-and-Falsifiers-Summary rev 7 | **UPDATED 2026-09-06:** the `papers/README.md` residual this row named is fixed — the file had in fact been deleted whole (accidentally, in the unrelated 2026-08-19 commit `c142d1c`), was restored from git history, and its headline numbers were brought current to summary rev 7 ($m_Z/m_W=3/\sqrt7$ on-shell, $-0.064\%$, replacing the withdrawn $2/\sqrt3$/$1.77\%$; the absolute $m_W$/$m_Z$ prediction, F320/claim 12, added alongside it). Its headline bullets now carry `<!-- claims: CLnnn=status -->` anchors and `tools/check_summary_claims.py` was generalized (`GRADED_FILES`) to check them, so this specific surface no longer depends on a by-hand audit noticing it drift. A sweep of the other tracked `README.md`/front-matter files for the same defect shape found none. **Grade held at PARTIAL, not raised**, per this row's own 2026-08-18 note: a fix is not the full-surface audit that note called for, only removal of the one instance the audit had already named |
| H5 | Internal consistency of decisions | **MACHINE** | key-decisions.md D1–D12; Part D of `open-derivations` | **UPDATED 2026-09-06 — moved from PARTIAL.** Re-read this row's own history: it named exactly three live items over its lifetime, and all three are now closed — (i) K9's F311-vs-F319 disagreement (Amendment 4); (ii) B9's two published residuals, reconciled as additive (Amendment 2); (iii) X1, the coupling-normalisation/Casimir contradiction, **resolved 2026-08-18 (F325, 7/7)**: branch A tested and closed on two independent legs (structural — the $C_F$ reading is a matching artefact; quantitative — branch A sits 5.63 decades outside CL252's committed bound), branch B adopted. `open-derivations.md` Part D — this row's own source ledger — states this directly: "**Nothing further — it is closed**" and tallies **Contradictions: 0**. Independently reaffirmed by an unrelated session five days later (2026-09-05 H1 ledger re-tally: "X1 ... closed 2026-08-18 (F325) and is no longer a live dependency"). **Checked for a fourth, never-named consistency question and found none**: F325 §6 does flag a residual (which $\Omega$ the single-plaquette rotor carries on the BCC dispersion, plausibly F155's $q_*$), but that is a *different, already-tracked* open quantitative item — it lives under rubric row **B10** ($N_c$ selector, still PARTIAL) and ledger item **#16** ($\alpha_s$/$d_1$, still PARTIAL) — not a case of two adopted decisions disagreeing, so it does not reopen this row. D2's reversal remains a documented, machine-tracked supersession (`S8`), not a live contradiction; the stale 2026-08-04 `S14-P5.1` schema item was fixed the same week and never resurfaced here. **Graded `MACHINE` rather than `EXACT`**, matching this block's own H8 precedent: the "no contradiction" invariant is enforced by reading the maintained `open-derivations.md` Part D ledger (corroborated by an independent session), not by a closed-form guarantee that no future decision can ever conflict |
| H6 | Reproducibility | PARTIAL | `check_finding_records.py` (0 violations, live 2026-08-18 Amendment 1); `make indexes-check` (**GREEN, verified live this run**) | Indexes are current and F324/F325 fully indexed. `make gate` itself remains **NOT VERIFIED THIS RUN** — could not be run to completion in this session (see Health probe). Grade held at PARTIAL pending a genuine green gate run |
| H7 | Module coverage | PARTIAL | D11 registry (baseline figures, not re-measured live this run) | 51 of 218 channel-driven (23.4%), carried from baseline. Finding-coverage rollout's adjacent `weak_only`/`untested` metric improved 66→30 (2026-08-19) but that is not this row's own metric |
| **H8** | **Claims without test records** | **MACHINE** | findings-index.md (`no test record` count: **0**, verified live this run); `tests-index.md` 434 records / 316 findings; 2026-08-19 - 13:55 changelog entry | **Moved from PARTIAL.** 14 of 16 prior gaps were a broken `findings:` join, not a missing test, fixed by correcting the field; the genuine two (F26b, F142) got real gate records with measured controls. `audit_tests --ratchet` was reported red-on-arrival (70→75, 231→236) from *concurrent, uncommitted* F324-adjacent work the same day — this run's own live `make health` measured **70 / 231**, i.e. the pre-redness baseline, so that specific redness was not present in the tree as measured today; flagged in Method notes as worth a direct, dedicated re-check rather than treated as settled |

---

## Method notes

**Live this run** (via the device bridge, against the real repository, not a staged/isolated copy —
a first for this command; contrast the baseline, which ran nothing live): `make indexes-check`,
`make registry`, `make numerics`, `make health`, plus targeted `grep`/`wc` reads of
`findings-index.md`, `claims-index.md`, `docs/claims/registry.yaml`, and
`docs/status/exactness-inventory.md`'s generated header. `make gate` was attempted and did not
complete (see Health probe) — recorded as NOT VERIFIED, not inferred green.

**Read in full or in relevant part:** `INDEX.md`, `findings-index.md` (full listing), the previous
report `completeness-2026-08-18.md` including all four of its amendments (full text — this rerun's
whole basis), `open-derivations.md` (Parts A–D), `project-status-index.md`, `tail -n 200
changelog.md` (covers 2026-08-18 - 12:04 through 2026-08-19 - 14:53, which is confirmed to be the
most recent entry — nothing has landed since).

**Not re-derived from scratch.** The full text of blocks A, B, C, D, E, K, G and the unchanged rows
of H is carried verbatim from the baseline as amended, rather than re-graded from primary sources,
because the changelog shows no finding, claim, or exactness value changed in the window — re-deriving
each row's evidence would reproduce the same citations the baseline already assembled. This is a
deliberate scope choice for a two-day rerun with a confirmed-empty physics delta; a sweep after a
longer gap, or one where the changelog shows finding activity, should not take this shortcut.

**Spot-checks (the three grades I was least sure of):**

1. **H8 `PARTIAL → MACHINE`** — verified live: `grep -c "no test record" findings-index.md` returns
   `0` against the actual repository file, not the changelog's prose claim. Graded `MACHINE` rather
   than `EXACT` because the guarantee is enforced by a checker script, not a closed-form identity, and
   because the ratchet-redness question (below) is not fully resolved.
2. **The `audit_tests --ratchet` discrepancy** — the 2026-08-19 changelog entry states the ratchet was
   red-on-arrival at 70→75 / 231→236 / 323→325 "from the F324 work already uncommitted in the tree,"
   and that removing the two new H8 records leaves the counts unchanged (i.e., the redness predates
   H8's own fix). This run's live `make health` measured **70 / 231** — the *pre*-redness numbers —
   directly from the current tree. Two readings are possible: the uncommitted F324-adjacent work was
   since committed cleanly (redness resolved), or it was never merged into this checkout. I could not
   distinguish these in the device-bridge budget available and did **not** grade H6/H8 up or down on
   this ambiguity; it is flagged rather than resolved. **Ben: worth a direct `python3
   tools/audit_tests.py --ratchet` run to settle this.**
3. **H6's indexes-check claim** — re-ran `make indexes-check` live rather than trusting the baseline's
   Amendment-1 description of it (which was itself run against a staged copy, not the live tree). It
   returned green with F325 as the newest finding, confirming the baseline's Amendment 1 fix held.

**What this run could not verify:** `make gate` end-to-end (see Health probe); `make claims`;
`make control`; whether the 91 declared controls still verify RED at the current code fingerprint;
the whole-tree keyword sweep the ABSENT section's caveat depends on; H7's live module-registry
fraction (carried from the baseline's own figures, not re-measured).

**Prompt coverage ratchet.** Scoreboard total 74 + D-ledger 28 = 102 rows. EXACT (14) + MACHINE (5,
rubric — H5 moved 2026-09-06) + EXACT (1, ledger) + MACHINE (2, ledger) = 22 rows at ceiling.
102 − 22 = **80** rows need a prompt. `completeness-2026-08-20-prompts.md` covers 80 via 69 sections
(grouped ledger entries) — **match**; H5's prompt section removed the same session it closed.
