# Research prompts — completeness 2026-08-20 - 15:50

*Companion to `completeness-2026-08-20.md`. One paste-ready prompt per rubric or ledger row graded
below `MACHINE`. Coverage: 69 prompt sections against 80 non-EXACT/non-MACHINE rows (scoreboard total
102 [74 rubric + 28 ledger] − EXACT 15 − MACHINE 7 = 80) — **match, not a shortfall**: 11 of the 69
sections are grouped ledger entries that already share one grade/evidence set in the rubric's own D
table (quark masses ×6, CKM ×4, PMNS angles ×3, lepton-mass-ratio shape ×2 — 15 individual parameters
folded into 4 sections, a net reduction of 11), exactly mirroring how `completeness-2026-08-20.md`'s
own D table groups them into rows like "1–6" rather than six separate lines. No row is silently
dropped — every one of the 80 is named and addressed inside its section. This is a two-day rerun of
`completeness-2026-08-18`'s companion; no grade changed except H8 and (2026-09-06) H5 (both left this
file, having been promoted to MACHINE), so every prompt below is carried from the same evidence base
as the baseline report and re-dated. External literature pass: none run fresh this session
(device-bridge budget went to the live health probe instead); each row below carries search terms
and named standing anchors
instead of a fresh-dated citation. Ben: treat the "EXTERNAL" lines as unchanged from whenever they
were last checked, not as verified today.*

**How to use one.** Paste a single fenced block into a fresh session. Each is self-contained. Do not
paste two — a session that claims two rows at once claims neither cleanly.

## Priority order

| Rank | Row | Grade → target | Why it is worth doing first | Est. cost |
|---|---|---|---|---|
| 1 | ledger #16 / B8 / d1 (=E3=Q1=Q2) | PARTIAL → QUANT | d1 leg 3 is the sole blocker on α_s(M_Z), unmoved since 2026-08-11, now the single largest open item in the strong sector | Long run (native sweep n=28–40) + one physics decision (L6) |
| 2 | K9 / ledger #28 (Λ) | OPEN → PARTIAL | Price is met to 0.10 dex; only the dynamics of the F183/F190 ceiling is missing | Medium — one derivation, not a new sector |
| 3 | G3 / B9 | PARTIAL / QUANT → tighter | The two-loop leptonic bubble on the model's own fields is the shared open target of both rows | Medium — F261's machinery exists |
| 4 | G5 / G7 (Q4, isospin splitting) | QUANT → cleaner QUANT | Model's own BBN excludes its own m_n−m_p at 36.6σ; bounded, existing test, no missing sector | Small — one session per F297 §10 |
| 5 | H2 (ledger backlog) | PARTIAL → PARTIAL (numbers move) | 48 gate-tier assertions with no control, unmoved 12 days | Small per item, retrofit 5 to break the ratchet |

## A — Foundations

### A1 — Spacetime dimensionality — `PARTIAL` → next: tighten the "+1" to a derivation, or accept it as a construction choice

**Leverage:** shares premises with B10 (generation-count parity) and C1. **Cost:** in-repo, one
derivation attempt. **Blocked by:** nothing structural.

~~~text
Physics Notes research session. Target: rubric row A1 (spacetime dimensionality — why 3+1), currently
PARTIAL, target: either close the "+1" (time dimension) to a derivation, or state plainly it is a
construction choice and stop attacking it.

WHAT IS ALREADY TRUE: Two independent selectors (F291: ker J = 0 ⇒ d ≤ 3; F292: coker J = 0 ⇒ d ≥ 3)
both return d_space = 3 for the BCC lattice's Cayley-graph structure; d=6 and d=9 are excluded, and a
reducible d=3n construction freezes. F318 removed F291 §3's self-flagged "conditional on s=2":  the
model's own s=36 quark cell does not relax the Clifford bound because what matters is the rank of the
hop's own span (3 at every factor), so the internal index is permitted at zero cost but its existence
is not forced.

THE RESIDUAL: the "+1" (one time dimension) is currently BY CONSTRUCTION, not derived. F313 attempted
a derivation via the update rule's commutant and a Newton-polytope descent; both its headline results
(the boxed su(s) dim/rank identity, and "d_space=3 from the commutant") were WITHDRAWN by F313's own
2026-08-13 remediation as numerology and circular respectively. The commutant proves no EXTRA
translations exist; it does not prove exactly three.

DO NOT RE-ATTACK: F313's commutant route for d_space=3 (closed negative, circular — F313 remediation).
The su(s) dim/rank boxed identity (closed negative — numerology, same remediation). F291 §3's
s=2-conditionality objection (closed — F318, the relevant rank is the hop span, not s).

REFERENCES — findings: F291, F292, F313 (⚠ two of its own headline results withdrawn by its own
2026-08-13 remediation — cite the remediation alongside it), F316 (closes F313's polynomial→Laurent
transfer), F318. Claims: check `docs/claims/registry.yaml` for cards citing F291/F292/F318 (grep
`findings:.*F291` in `docs/claims/registry.yaml`) before quoting a status. Tests: search
`tests/registry/*.yaml` for records with `findings: [F291]`, `[F292]`, `[F318]` and run
`casim test --id <id>` to see current state before touching. Ledger: `open-derivations.md` does not
currently carry a dedicated A1 row (last audited 2026-08-11) — check whether one should exist. Papers:
`papers/Paper-01-Base-Structure.md` for the base lattice construction.

EXTERNAL: search terms — "BCC lattice dimensionality selection", "Clifford algebra rank spacetime
dimension emergent", "causal set / quantum graph 3+1 selection theorems" (Wolfram-style CA literature
as a named contrast, not an endorsement).

FIRST STEP: read F313's remediation note in full (it is in the finding file itself or the changelog
around 2026-08-13) to see exactly what was withdrawn and why, then decide whether a *different* route
to "+1" exists that the remediation didn't foreclose, or write a one-paragraph finding stating it is
adopted by construction and moving this row toward POSIT with Part C reasoning (why every derivation
route closed).

WHAT PROMOTES THE GRADE: a derivation of d_time=1 that survives adversarial review, OR a documented,
reasoned move to POSIT (Part C of open-derivations) stating every derivation route is closed.

WHAT WOULD FALSIFY THE ATTEMPT: a valid derivation attempt that returns d_time ≠ 1, or that shows the
"+1" is only obtainable by assuming what it should prove (the same trap F313 fell into).

PROTOCOL: this is research. Claim your topic in docs/design/session-claims.yaml before any physics
(/derive Step 0). Take finding numbers one at a time from `casim index` NEXT FREE NUMBER (currently
F326 as of 2026-08-20 — re-check, it moves). Close with the finding, its test record, and its claim
card. `make gate` before you finish.
~~~

### A2 — Lorentz invariance — `PARTIAL` → next: confront the chiral O(|k|²) coefficient with a real bound

**Leverage:** shares the finite-a defect object with G1/G8 (the same D_i operator family).
**Cost:** small — a literature confrontation, not new derivation. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row A2 (Lorentz invariance), currently PARTIAL, target
QUANT or tighter PARTIAL (a named, bounded residual rather than an unconfronted one).

WHAT IS ALREADY TRUE: the whole finite-a Poincaré defect is a single object, D_i = ∂_iΦ with
Φ = (Ω² − c_lat²k²)/2c_lat², chirality-odd (F301, 10/10). It is exact to all orders on the ⟨100⟩ axis
(3.5e-46) and O(|k|³) for the even (non-birefringent) photon (F246, machine precision). The chiral
O(|k|²) coefficient is the model's electron/quark-sector analogue and has NEVER been confronted with
data (`open-derivations` L8).

THE RESIDUAL: F28's GRB/AGN photon-dispersion bound is structurally INAPPLICABLE here — it constrains
the photon's |k|³ term (a different operator, in a sector with different symmetry). The chiral |k|²
coefficient needs its own confrontation, against neutrino or electron LIV limits.

DO NOT RE-ATTACK: deriving a universal (channel-independent) Lorentz-violation coefficient — F91's
pairing-classification theorem forces different channels (even/chiral) to carry different LV orders,
this is settled. Do not re-derive D_i itself — F301 already closed that exactly.

REFERENCES — findings: F301 (10/10, the residual's own source), F246 (photon |k|³, closed), F91
(pairing classification, why channels differ), F28 (the inapplicable GRB bound, cite to explain why it
does NOT apply here). Claims: search `docs/claims/registry.yaml` for `CL262` (the finite-a defect
card, per the 2026-08-18 baseline's H4 note) and read its `falsifier:` field verbatim — that is this
prompt's own falsifier. Tests: grep `tests/registry/*.yaml` for `F301`. Ledger: `open-derivations.md`
row **L8** carries this row's exact residual language — read it before starting.

EXTERNAL: named anchors — SME (Standard-Model Extension) coefficient tables for the electron/neutrino
sector (Kostelecký & Russell "living review" — check for a current arXiv version), IceCube and
astrophysical-neutrino LIV bounds on chiral/CPT-odd operators. Search terms: "chirality-odd Lorentz
violation electron sector bound", "neutrino dispersion Planck-suppressed operator constraint".

FIRST STEP: extract the exact numerical coefficient of F301's O(|k|²) chiral term in SI/natural units
comparable to SME coefficient tables, then look up the current best bound on the matching SME operator.

WHAT PROMOTES THE GRADE: a quoted bound, with the model's coefficient inside or outside it, stated
either way as a real result (inside = survives; outside = a genuine falsification, also a result).

WHAT WOULD FALSIFY THE ATTEMPT: none in the usual sense — a null result here (no matching SME operator
exists, or bounds are too weak to say anything) is itself the honest answer and should be written up
as such rather than treated as a failed session.

PROTOCOL: this is research. Claim your topic in docs/design/session-claims.yaml before any physics.
Take the next finding number from `casim index`. Close with the finding, its test record (a
`result_dump` comparing coefficient to bound is fine), and its claim card. `make gate` before finish.
~~~

### A4 — CPT, and C/P/T separately — `PARTIAL` → next: a CPT theorem for the QCA, or a named reason none exists

**Leverage:** low — isolated row, five reports unmoved. **Cost:** unclear, possibly large (a genuine
CPT theorem is a hard result). **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row A4 (CPT and C/P/T separately), currently PARTIAL,
target: either a CPT theorem for this specific QCA, or a reasoned statement of why none is expected.

WHAT IS ALREADY TRUE: C, P, and CP are built and exact per species (F53, F321). J(1)=0 is
one-generation CKM arithmetic, not a CPT statement. F321 establishes reality of the Euclidean action
from closure of the loop set under reversal — a T-adjacent structural fact, but it is about θ_QCD
(row B11), not a CPT theorem, and must not be borrowed here (the baseline explicitly names this as a
trap — do not repeat B11's mistake of attributing F321's result to this row).

THE RESIDUAL: no CPT theorem exists for the discrete QCA. Standard CPT theorems (Lorentz invariance +
locality + Hermiticity ⇒ CPT) assume continuum QFT; this model is discrete and only PARTIAL on Lorentz
invariance itself (row A2), so the standard proof route may not even apply cleanly.

DO NOT RE-ATTACK: borrowing F321's θ_QCD reality result as a CPT statement — it is a different
theorem about a different object (explicitly flagged as a trap in three prior reports).

REFERENCES — findings: F53 (per-species C/P/CP), F321 (θ_QCD reality — cite to explicitly EXCLUDE from
this row, not to support it). Tests: grep `tests/registry/*.yaml` for `F53`. Ledger: no dedicated row
in `open-derivations.md` as of the 2026-08-11 audit — check whether this needs one.

EXTERNAL: named anchors — the standard CPT theorem literature (Streater & Wightman for the continuum
case, as the thing to determine whether/how it generalizes). Search terms: "CPT theorem cellular
automaton discrete spacetime", "CPT theorem without continuum Lorentz invariance".

FIRST STEP: survey whether a discrete-spacetime CPT theorem exists in the literature at all (the
search above) before attempting a from-scratch proof — if the answer is "open problem in the field
generally," this row may be honestly PARTIAL indefinitely and that should be stated rather than
implied to be solvable this session.

WHAT PROMOTES THE GRADE: a genuine CPT theorem specific to this QCA's update rule, OR a clearly
reasoned statement (citing the general difficulty of discrete CPT theorems) for why this stays PARTIAL
long-term, moved into `open-derivations` Part A with that reasoning attached.

WHAT WOULD FALSIFY THE ATTEMPT: finding a CPT-violating observable in the model's own dynamics
(unlikely given C/P/CP are already exact per species, but check explicitly rather than assume).

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### A6 — Superposition + Born rule — `PARTIAL` → next: prove Cooke–Keane–Moran regularity, or accept the external lemma

**Leverage:** high — the last external step in the entire Born-rule derivation chain. **Cost:**
F304's own estimate: "a bounded three-page piece of work." **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row A6 (superposition + Born rule), currently PARTIAL,
target MACHINE or EXACT (closing the one remaining lemma).

WHAT IS ALREADY TRUE: Gleason's theorem is PROVED here, not cited (F304 §5): b_k =
(-1)^k / C(k+d-2, k), surviving iff 1+(d-1)b_k=0. F312 closes non-contextuality by a THEOREM rather
than by checking cases: the off-site commutator is literally 0.0 for both SU(2)_L and SU(3)_c, so the
non-Abelian structure is entirely intra-site, and a Schur reduction (C_2=(N²-1)/2N, a multiple of the
identity) drops the internal index out of the frame condition for ANY compact group. dim = d_p·N, so
SU(3)_c alone clears d≥3, and F304's own d=2 hole is unreachable in any charged sector.

THE RESIDUAL: exactly one lemma — Cooke–Keane–Moran regularity: that a non-negative frame function is
automatically continuous. Its entire content is excluding non-measurable weight assignments.

DO NOT RE-ATTACK: non-contextuality via case-by-case checking of more gauge groups — CLOSED, F312
proves it for any compact group by the Schur-reduction argument, this generalizes and does not need
per-group verification.

REFERENCES — findings: F304 (Gleason proof, §5), F312 (non-contextuality closure, the current
finding). Claims: `CL264` per the baseline's A6 evidence citation — read its falsifier field. Tests:
grep `tests/registry/*.yaml` for `F304`, `F312`. Ledger: `open-derivations.md` row **A6r** carries
this exact residual — read it, it already narrows the target to this one lemma.

EXTERNAL: named anchor — Cooke, Keane & Moran (1985), "An elementary proof of Gleason's theorem" (the
paper this lemma is usually cited from) — find the actual regularity argument and check whether it
transfers directly to this model's frame-function setup or needs adaptation. Search terms: "Gleason
theorem frame function regularity proof", "non-negative frame function automatic continuity".

FIRST STEP: read the Cooke–Keane–Moran paper's regularity argument directly and map its hypotheses
onto this model's specific frame-function construction (F304 §5) to see if it transfers as-is.

WHAT PROMOTES THE GRADE: a written-out proof (or adaptation) of the regularity lemma specific to this
model's construction, closing the last external step.

WHAT WOULD FALSIFY THE ATTEMPT: finding that the model's frame function does NOT satisfy the
regularity lemma's hypotheses, which would mean Gleason's theorem does not go through as cleanly as
assumed and A6 should be re-examined more broadly, not just patched.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### A9 — Spin-statistics — `PARTIAL` → next: derive π₁(SO(3))=ℤ₂⇒belt-trick internally, or accept it as external

**Leverage:** low-medium. **Cost:** topology, likely a genuine research problem. **Blocked by:**
nothing named.

~~~text
Physics Notes research session. Target: rubric row A9 (spin-statistics theorem), currently PARTIAL,
target: internalize the topological step, or state clearly why it should stay external.

WHAT IS ALREADY TRUE: both physical premises of the spin-statistics theorem are DERIVED here (F289,
11/11): d=3 (from F291/F292's selectors) and R(2π)=-1 to 1.7e-16 over 60 axes (the rotor's own
double-cover behavior). This is not a new proof of spin-statistics itself.

THE RESIDUAL: π₁(SO(3))=S_n... more precisely the belt-trick homotopy argument (why a 2π rotation of
one particle relative to its surroundings is topologically the same as an exchange) stays EXTERNAL —
imported from standard topology, not derived from the lattice's own structure. CL255 is explicitly
tier:supporting for exactly this reason.

DO NOT RE-ATTACK: re-deriving d=3 or R(2π)=-1 — both closed exactly by F289/F291/F292, this row's
residual is specifically the topological linking step, nothing upstream of it.

REFERENCES — findings: F289 (11/11, the current derivation), F291, F292 (d=3 selectors), F217 (related
entanglement machinery). Claims: check `docs/claims/registry.yaml` for `CL255` and read its
`tier:`/`falsifier:` fields directly. Tests: grep `tests/registry/*.yaml` for `F289`.

EXTERNAL: named anchor — Finkelstein & Rubinstein's original belt-trick argument, and Balachandran et
al.'s topological approach to spin-statistics — check whether either has a discretized/lattice version
that could transfer. Search terms: "spin-statistics theorem discrete lattice derivation",
"belt trick homotopy lattice gauge theory".

FIRST STEP: determine whether the model's own BCC lattice + rotor structure has enough topological
content (e.g., a discrete analogue of π₁(SO(3))) to host the belt-trick argument internally, or
whether it is a genuinely continuum-topology fact that cannot be reduced further on a discrete
substrate — this determination alone is worth a session and a finding either way.

WHAT PROMOTES THE GRADE: an internal derivation of the linking/exchange equivalence, OR a reasoned,
citable argument for why this must stay external (moving toward a documented POSIT rather than an
open residual).

WHAT WOULD FALSIFY THE ATTEMPT: none directly — this is exploratory; a negative result (genuinely
cannot be internalized) is itself valuable and should be written up.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### A10 — Cluster decomposition / no-signalling — `PARTIAL` → next: extend the interacting 3-D clustering claim

**Leverage:** medium — closes a foundational row cleanly. **Cost:** medium, needs genuine 3-D
interacting-theory work. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row A10 (cluster decomposition / no-signalling),
currently PARTIAL, target QUANT or MACHINE (extending to the interacting 3-D case).

WHAT IS ALREADY TRUE: no-signalling is EXACT (F290, 7.8e-16). The causal cone is strict and genuinely
CA-specific — tighter than a generic Lieb–Robinson bound's exponential tail (F290, machine precision).

THE RESIDUAL: F290's own residual 1 states plainly that the interacting 3-D clustering claim "has NOT
been made" — the current clustering result is for the 1-D free-fermion case only.

DO NOT RE-ATTACK: no-signalling itself, or the strict causal cone in the free-field case — both closed
exactly by F290. This row's gap is specifically the interacting, 3-D extension.

REFERENCES — findings: F290 (7/7 or similar — check current test record; residual 1 is the target
verbatim), F227 (decoherence/unitarity floor, adjacent). Tests: grep `tests/registry/*.yaml` for
`F290` and read its `expect.exactness` and any residual notes.

EXTERNAL: search terms — "cluster decomposition principle interacting lattice field theory proof",
"Lieb-Robinson bound interacting fermion lattice 3D".

FIRST STEP: read F290's residual-1 statement directly in the finding file to see exactly what was
scoped out and why (likely computational cost of a genuine interacting 3-D correlation-decay
calculation), then scope the smallest interacting 3-D test case that could extend it.

WHAT PROMOTES THE GRADE: a measured correlation-decay result in the interacting 3-D theory matching
cluster-decomposition expectations, closing F290's residual 1.

WHAT WOULD FALSIFY THE ATTEMPT: a measured correlation that does NOT decay as expected in the
interacting 3-D case — genuinely important if found, not just a null result.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### A11 — UV completeness — `QUANT` → next: close the cosmological-constant coefficient (shared with K9)

**Leverage:** very high — shares its one residual with K9/ledger #28, the model's single largest
numerical embarrassment. **Cost:** see K9 prompt below; this row does not need separate work, only a
cross-reference. **Blocked by:** the K9 dynamics question.

~~~text
Physics Notes research session. Target: rubric row A11 (UV completeness), currently QUANT, target
PARTIAL or better (naming/closing the one residual coefficient).

WHAT IS ALREADY TRUE: this row's UV-completion picture is unusually strong for a lattice theory. The
BZ edge is a genuine physical cutoff (not a regulator), and F264's power-counting theorem is
STRONGER than the standard Wilsonian statement because the cutoff is real: finitely many operator
coefficients carry it, entirely finite, no counterterm subtraction needed in the usual sense. Licence
measured directly (scheme constant IR-independent to 2.0e-12; ln coefficient 1/16π² universal across
four schemes). Leading irrelevant operator is dimension-6 with an exact closed rational coefficient
(1.1e-20 residual, 60 decimal places), and there is NO dimension-5 photon operator (p=2, closed).
Exactly two cutoff-carrying coefficients exist with no free parameter: G (right, to 3e-8) and ρ_vac
(wrong, by 120.8 orders — this row's one residual number).

THE RESIDUAL: ρ_vac, the same object as ledger parameter #28 (Λ) and rubric row K9. This is NOT a
separate open item — it is one number appearing in three rows.

DO NOT RE-ATTACK: the Wilsonian dictionary question itself (closed — F264's finite-operator-count
theorem stands, adjudicated as of the 2026-08-18 baseline). Do not treat this as a separate research
target from K9 — it is the same number.

REFERENCES — findings: F116, F164, F264, F284 §5, F319 (all cited in the baseline's A11 row). Ledger:
`open-derivations.md` row **L7** (UV completeness, unmoved for three reports as of the baseline) AND
row **G1** (the K9/Λ target — this row's actual open number lives there). **Read the K9 prompt in
this same file before starting** — doing both independently wastes a session.

EXTERNAL: none needed beyond what K9's prompt already covers.

FIRST STEP: read the K9 prompt in this file (below, block K) — this row closes exactly when K9 does.

WHAT PROMOTES THE GRADE: closing the K9/Λ dynamics question (see K9 prompt).

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this row is a pointer to K9, not an independent target.

PROTOCOL: n/a for this row specifically — claim and work K9/Λ instead, and note in that finding that
it also closes A11 and ledger #28.
~~~


## B — Gauge structure

### *B1 — Origin of SU(3)×SU(2)_L×U(1)_Y — `PARTIAL` → next: force the internal index's existence, not just its shape

**Leverage:** high — root of the whole gauge sector. **Cost:** large, open-ended. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row B1 (origin of the gauge group), currently PARTIAL,
target: reduce the one remaining input (that an internal index exists at all).

WHAT IS ALREADY TRUE: F317 (21/21, six controls) reduces "colour is put in" from six impositions to
one. Derived: unitarity (commutant = M_3, dim 9 ⇒ U(3)), specialness (F27's chirality removes the
U(1) trace), locality⇒connection (on-site commutes with site-dependent V(x) at 7e-16 vs hop's 1.343),
vector-likeness (all 27 su(2) anomaly coefficients exactly 0). F318 (11/11) then shows the cell
PERMITS the internal index at zero cost and FORCES its shape once it exists — but does not force its
existence.

THE RESIDUAL: one input — that the internal (colour) index exists at all. F317 §8 states the prior-art
lineage leg by leg; this is a reduction, not a full derivation of SU(3).

DO NOT RE-ATTACK: any of F317's four closed legs (unitarity, specialness, locality⇒connection,
vector-likeness) individually — each is exact and closed. Do not re-attempt deriving SU(2)_L from
β-gauging or U(1)_Y from bipartite sublattice parity — both already closed and unchanged by this row.

REFERENCES — findings: F27, F51, F43, F291, F317 (the reduction), F318 (permits-but-doesn't-force),
F324 (uses this row's premises for the colour-count derivation, cite as a downstream dependent, not
as support). Ledger: no dedicated open-derivations row cited in the baseline for B1 specifically —
check `open-derivations.md` Part A for a match before assuming none exists.

EXTERNAL: search terms — "emergent gauge symmetry from lattice locality", "why does an internal index
exist derivation" (this is a genuinely unusual foundational question, not a standard SM one — expect
thin literature).

FIRST STEP: read F317 and F318 in full to understand exactly what "the internal index exists" means as
a formal statement in this model's construction, then look for any structural reason (e.g. required by
consistency of the update rule, or by matching some observed d.o.f. count) that would force it.

WHAT PROMOTES THE GRADE: a derivation that the internal index must exist (not just what shape it takes
if it does), OR a proof that its existence is irreducibly a founding choice (move to POSIT, Part C).

WHAT WOULD FALSIFY THE ATTEMPT: none direct — exploratory.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *B6 — Weinberg angle, with scale — `QUANT` → next: derive the hadronic piece to remove the +0.450% doubled residual

**Leverage:** shared with B9/G3. **Cost:** medium, same target as priority #3. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row B6 (Weinberg angle with scale), currently QUANT,
target: tighter QUANT or PARTIAL by removing the hadronic-piece ambiguity.

WHAT IS ALREADY TRUE: sin²θ_W=1/4 is the matching value at μ*=4πv=3094.09 GeV, forced by hypercharge
having no lattice kinetic term (F138); 2/9 is its on-shell face via F231's 8/9 bridge. Residual on the
model's own leptonic-only α(M_Z): +0.222% at M_Z, −0.064% on shell, zero free parameters.

THE RESIDUAL: F322 found that on the model's OWN leptonic-only α(M_Z) (rather than the full measured
α(M_Z) which includes hadronic vacuum polarization), the residual DOUBLES to +0.450% (factor 2.02).
Half this row's stated precision is therefore owed to the hadronic piece the model does not derive
(same object as G3's declared-out-of-scope hadronic VP).

DO NOT RE-ATTACK: the μ*=4πv matching derivation itself, or the 8/9 on-shell bridge — both closed
exactly (F138, F231).

REFERENCES — findings: F138, F49, F231, F141, F322 (the sensitivity measurement). This row shares its
open target with **B9** and **G3** — read those prompts too, doing all three independently wastes
effort; one finding on the hadronic VP piece likely closes or tightens all three.

EXTERNAL: standard hadronic vacuum polarization data (e.g. the KNT or DHMZ compilations used for g-2)
— search "hadronic vacuum polarization Δα(M_Z) contribution data-driven value".

FIRST STEP: read F322 §6 and §7 directly for exactly how the leptonic-only sensitivity was measured,
then see B9's prompt for the shared next step (the two-loop leptonic bubble on the model's own
fields).

WHAT PROMOTES THE GRADE: closing or substantially reducing the hadronic-piece ambiguity — see B9/G3.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, shared target with B9/G3.

PROTOCOL: this is research; see B9's prompt for the primary attack and protocol.
~~~

### *B7 — Confinement — `PARTIAL` → next: reflection positivity / transfer-matrix proof for the 3+1D leg

**Leverage:** medium — this is the one row the baseline flags as "unmoved and unmovable by sampling."
**Cost:** large — a genuine proof, not a numerical result. **Blocked by:** nothing named, but requires
different machinery (positivity/transfer-matrix) than the tree currently has.

~~~text
Physics Notes research session. Target: rubric row B7 (confinement), currently PARTIAL, target: a
positivity-based proof for the 3+1D leg (the 2D leg is already EXACT).

WHAT IS ALREADY TRUE: exact in 2D (area law, σ=-ln w(β)>0 for all β). The 4D leg now runs on the
model's own lattice as BCC_3 × ℤ (10 plaquettes/site: 6 rhombi + 4 mixed rectangles), staple identity
2.3e-16, gauge invariance 3.8e-17, with the anisotropy DERIVED rather than conventional: β_t/β_s =
4/(3c_lat²) = 4 and ξ=1/c_lat=√3. Record `gauge-bcc-mc-d4` 28/28, 5/5 controls, re-verified live in the
2026-08-18 Amendment 1 pass.

THE RESIDUAL: a genuine PROOF (not sampling) needs a transfer matrix with positivity. `open-derivations`
states plainly that grepping the tree for "reflection positiv", "Osterwalder", "Schrader", "cluster
expansion" returns ZERO hits everywhere searchable — this machinery does not exist in the repository
at all yet, and the residual is "unmoved and unmovable by sampling" (i.e., more Monte Carlo will not
close this; only a structural proof will).

DO NOT RE-ATTACK: more Monte Carlo sampling of the 4D confinement measure — explicitly named as unable
to close this residual regardless of statistics.

REFERENCES — findings: F70, F86, F88, F299, F323, F265; F94 partially superseded (S21→F323, F265) —
cite the supersession. Tests: grep `tests/registry/*.yaml` for `gauge-bcc-mc-d4`.

EXTERNAL: named anchors — Osterwalder & Schrader (1973/1975) reflection positivity axioms; Seiler's
"Gauge Theories as a Problem of Constructive Quantum Field Theory" for confinement proof machinery.
Search terms: "reflection positivity lattice gauge theory confinement proof", "cluster expansion
strong coupling confinement rigorous".

FIRST STEP: determine whether the model's specific BCC_3×ℤ action (with its derived anisotropic
couplings) satisfies the Osterwalder-Schrader reflection-positivity axioms at all — this is itself a
non-trivial first result if it goes either way.

WHAT PROMOTES THE GRADE: a positivity/transfer-matrix argument establishing confinement rigorously
(even in a bounded coupling regime), which would be a genuinely strong result for a CA-based model.

WHAT WOULD FALSIFY THE ATTEMPT: finding the action is NOT reflection-positive as constructed — if so,
say so plainly; that would itself be an important structural finding about the model's own lattice
action, not a failure.

PROTOCOL: this is research, and unusually mathematical for this tree — expect it to take longer than
typical. Claim your topic first. Take the next finding number. Close with finding, test record, claim
card. `make gate` before finish.
~~~

### *B8 — Asymptotic freedom / α_s running — `PARTIAL` → next: close d1 leg 3, the single highest-priority open item

**Leverage:** very high — priority #1 of this report. **Cost:** long run + one physics decision.
**Blocked by:** `open-derivations` L6.

~~~text
Physics Notes research session. Target: rubric row B8 (asymptotic freedom / α_s running), currently
PARTIAL, target QUANT (closing d1 leg 3, the last of three legs on the strong-sector normalisation
constant).

WHAT IS ALREADY TRUE: b0 = 11/3 C_A = 11 exact and numerically recovered. The X1 colour-normalisation
fork is RESOLVED (F325, 2026-08-18, S22): branch B (Casimir-free, χ=1, g_s=1/2) is ADOPTED on two legs
independent of d1 — structural (the C_F reading is a matching artefact) and quantitative (branch A's
required Λ-ratio is 5.63 decades outside its own committed bracket). α_s(M_Z)=0.1186 (+0.5%) is no
longer contingent on the branch choice.

THE RESIDUAL: d1's third leg. F280 subtracted against the Wilson Λ_MSbar/Λ_L anchor and found the
slope-normalised estimator exactly invariant under an F272-class measure factor, leaving one leg of
three: the rule's own 3-gluon+ghost vertex form factors must supply ΔC_vertex=-2.0160 (36.2% of
ΔC=-5.5755), bracket [-2.257,-1.446], propagator leg measured -0.992±0.044, band
Λ_MSbar/Λ_rule∈[1,7.98]. F305 derived the rhombic vertices and a genuine gauge-side fundamental
domain; F307 ran the estimator action-consistently for the FIRST time and DECLINED to quote the
number: BCC-side b0 recovery is 0.41-0.49 and climbing, the two normalisations diverging with n
(-0.24→-0.29 vs -1.11→-1.72), half-spread 0.87 against leg 2's 0.044. F308 fixed both folds; repaired
path agrees with F307's independent path to 6.8e-16.

DO NOT RE-ATTACK: the X1 branch question itself (CLOSED, F325 — branch B adopted, do not re-litigate
Casimir vs centre normalisation). Do not re-derive b0=11 (exact, closed).

REFERENCES — findings: F144, F151, F239, F235, F287, F280 (the subtracted formulation), F305 (rhombic
vertices), F307 (action-consistent estimator, declines to quote), F308 (repaired path), F325 (X1
closure). Ledger: `open-derivations.md` row **d1** (= E3 = Q1 = Q2) carries the full technical state —
READ IT IN FULL before starting, it names the exact blockers. Row **L6** ("which object is the rule's
gauge action at finite a") is the PHYSICS DECISION that sits upstream — F305 §5 and §4/§7.3 name two
specific unresolved sub-questions (the rhombic action's quadratic form vs the F26 rotation law's
propagator differ by up to 86% at generic k; whether the redundant link-axis mode is dynamical, which
FLIPS THE SIGN of b0). Decide L6 before quoting d1, not after.

EXTERNAL: this is an internal lattice-QCD-style computation, not a literature confrontation — no
external search needed beyond standard lattice perturbation theory references if the vertex-form-
factor computation needs a cross-check. Search terms if needed: "lattice perturbation theory one-loop
vertex form factor gauge action scheme".

FIRST STEP: decide `open-derivations` row L6 — pick which object is the rule's gauge action at finite
a (the rhombic action's own quadratic form, or the F26 rotation-law propagator), and separately resolve
whether the redundant link-axis mode is dynamical. F305 §7.4 notes the machinery is action-agnostic,
so testing the alternative costs one function — do that empirically rather than deciding by argument
alone if possible.

WHAT PROMOTES THE GRADE: a native sweep at n=28-40 on the repaired path (F308), quoting d1 with an
uncertainty, closing B8, ledger #16, rubric G5's +12% residual, and rubric E3/Q1/Q2 all at once.

WHAT WOULD FALSIFY THE ATTEMPT: per `open-derivations`, a vertex computation returning Λ outside
[1,7.98] falsifies the g_s=1/2 lock or the monotonicity assumption; a return of ~3.4e6 would REINSTATE
the closed branch A and reopen X1 — treat this as a live possibility, not just a formality.

PROTOCOL: this is research and this is the single most valuable open item in the tree. This is a LONG
RUN (per the skill's own note, hand out a `casim` parameter set and a JSON per CLAUDE.md rather than
running interactively). Claim your topic in docs/design/session-claims.yaml before any physics. Take
the next finding number from `casim index`. Close with finding, test record, claim card. `make gate`
before finish.
~~~

### *B9 — Running of α, EW couplings — `QUANT` → next: derive the two-loop leptonic bubble on the model's own fields

**Leverage:** high — shared target with B6, G3. **Cost:** medium, F261's machinery exists.
**Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row B9 (running of α / EW couplings), currently QUANT,
target: tighter QUANT by deriving (not importing) the two-loop leptonic non-log constant.

WHAT IS ALREADY TRUE: two numbers are both live and RECONCILED as additive, not rival (2026-08-18
Amendment 2). Model-internal headline: 0.0495% (F322: one loop + the model's own two-loop leading log,
F261's sympy-exact b1=1). After importing the Källén-Sabry two-loop non-log constant: 0.00158% (F311
§2.2, explicitly "cited, not derived here"). The two differ by exactly one term (1.6085e-5, 103.2% of
F322's residual) — confirmed arithmetically, not just physically compatible.

THE RESIDUAL: the two-loop leptonic bubble ON THE MODEL'S OWN FIELDS, using F261's dispersive
machinery, has never been attempted. This is jointly owned by F311 and F322 and is the row's real open
target — not a citation problem (that's fixed) but an actual undone derivation.

DO NOT RE-ATTACK: the reconciliation itself (CLOSED, Amendment 2 — do not re-litigate which number is
"the" residual, both are correctly stated with provenance). Do not import a different literature
constant as a shortcut — the whole point is deriving it internally.

REFERENCES — findings: F322 (§6, §6.1 — the reconciliation table), F311 (§2.2, §8 — states its own
import explicitly), F251 ⚠ superseded S12→F277 (cite with supersession if referenced), F261 (the
sympy-exact b1=1 machinery to extend). Claims: `CL280` (running-alpha card) — read its Evidence and
Statement fields, both findings are named there per Amendment 2's edit log. Tests: grep
`tests/registry/*.yaml` for `F322`, `F261`.

EXTERNAL: named anchor — the standard Källén-Sabry two-loop QED vacuum polarization result (for
comparison once the internal derivation is done, not as an import target). Search terms: "two-loop
leptonic vacuum polarization dispersive derivation", "Källén-Sabry two-loop QED photon self-energy".

FIRST STEP: read F261's dispersive machinery (the source of the sympy-exact b1=1 leading-log result)
and scope what it would take to extend it to the full two-loop non-log piece — this is likely the
same class of calculation, one order further.

WHAT PROMOTES THE GRADE: a derived (not imported) two-loop non-log constant matching or explaining the
Källén-Sabry value, closing B9 to a tighter QUANT or even PARTIAL/MACHINE with the residual fully
named and computed internally.

WHAT WOULD FALSIFY THE ATTEMPT: a derived value that does NOT match the Källén-Sabry constant within
reasonable tolerance — would be a genuinely interesting discrepancy worth its own finding.

PROTOCOL: this is research. Claim your topic first (note in session-claims.yaml that this also touches
B6 and G3 — do not let three sessions claim overlapping territory). Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### *B10 — Why 3 colours — `PARTIAL` → next: harden the ℤ2 doublet-parity leg, or find a route to {3} alone

**Leverage:** medium. **Cost:** the ceiling is now {3,5,7,...} not {3} — closing further needs a new
selector. **Blocked by:** C1's generation-count parity (shared premise).

~~~text
Physics Notes research session. Target: rubric row B10 (why 3 colours), currently PARTIAL, target:
narrow {3,5,7,...} toward {3} alone, or accept the current bracket as the honest ceiling.

WHAT IS ALREADY TRUE (as of 2026-08-18, F325, S22 — READ THIS FIRST, it rewrites the row): the X1 fork
closed with branch B adopted. F324's upper constraint (the C7 identity "well-defined only for N_c≤3")
is WITHDRAWN (CN19) — it was a property of the MIXED matching (abelian rotor eigenvalue vs SU(N) gauge
eigenvalue), not a structural N_c constraint; under either self-consistent matching χ=1/(4g²) for every
N and every irrep. What SURVIVES: the ℤ2 doublet-parity leg of the model's own derived SU(2)_L
(Witten's global anomaly; prior art, Bär & Wiese 2001), which consumes no C7 input and no X1 branch.
B10 now closes on ODD N_c only: {3,5,7,...}, N_c=3 favoured empirically (F299's confinement engine
measurement) but by NOTHING structural.

THE RESIDUAL: no selector currently excludes N_c=5,7,9,.... The bracket is odd-N_c, not {3}.

DO NOT RE-ATTACK: the anomaly route, the spatial-3 route, or the ℤ3 route (all three closed with
reasons, F293 — do not re-derive). Do not re-attempt F303's n·C_F=4 three-link-plaquette route — closed
by exhaustive enumeration, the BCC lattice's nearest-neighbour hops (the eight (±1,±1,±1)) genuinely
cannot close a 3-hop loop by parity (0 of 8³ triples close). Do not re-open the C7 upper-bound argument
— WITHDRAWN as a mixed-matching artefact (F325 CN19), re-deriving it will reproduce the same withdrawal.

REFERENCES — findings: F293, F294, F298, F299, F303, F324, **F325** (the most recent and authoritative
— read this one in full first), F279, F144, F110. Ledger: `open-derivations.md` row **B10** carries
the complete current state including the withdrawn CN19 and the surviving parity leg — read the whole
row, it is long and precise about exactly what survives.

EXTERNAL: named anchor — Bär & Wiese (2001) on SU(2) global anomalies and lattice gauge theory (the
prior-art source for the surviving ℤ2 parity leg) — check this citation directly rather than trusting
the summary. Search terms: "SU(N) colour number selection lattice gauge symmetry", "Witten anomaly
gauge group rank selection".

FIRST STEP: read F325 in full (it is the newest and rewrites this row's status), then look for any
selector that discriminates N_c=3 from N_c=5,7,... within the odd-N_c bracket — the model's
confinement-scale measurement (F299) already favours 3 empirically; look for a STRUCTURAL analogue.

WHAT PROMOTES THE GRADE: a structural (not measured) selector that narrows odd-N_c to {3} alone.

WHAT WOULD FALSIFY THE ATTEMPT: none direct — if no further selector exists, document that {3,5,7,...}
with empirical preference for 3 is the honest final state, and say so rather than force a closure.

PROTOCOL: this is research. Claim your topic first (note the shared premise with C1's generation-count
parity — coordinate if both are being worked). Take the next finding number. Close with finding, test
record, claim card. `make gate` before finish.
~~~

### *B11 — Strong CP / θ_QCD — `QUANT` → next: extend to non-perturbative θ-sectors and the action-fork dependence

**Leverage:** low-medium, isolated. **Cost:** unclear, possibly requires L6 (shared with B8/d1).
**Blocked by:** partially, the same L6 action-fork question as B8.

~~~text
Physics Notes research session. Target: rubric row B11 (strong CP / θ_QCD), currently QUANT, target:
extend the reality-of-the-Euclidean-action argument to non-perturbative θ-sectors.

WHAT IS ALREADY TRUE: in Euclidean signature the θ-term is the UNIQUE purely imaginary gauge-invariant
quantity, so reality of the action IS θ=0 — not an inserted Re(), a property of the rule's own loop
set. The 20 oriented minimal rhombi are closed under reversal (exact), Im(S)=1.2e-14 at 99.7%
disorder, S invariant under U→U* with the one-sense functional odd at literal 0.0; every vertex
coefficient real at literal 0.0 at 2, 3, and 4 legs with colour indices sampled, and that class is
closed under products and q→-q integration, so Γ is real at every order (perturbatively).

THE RESIDUAL: arg det M_q at three generations (rows E6/E7 — the quark mass matrix's phase structure,
currently unaddressed at the ledger level); the action-fork dependence (this row's reality argument may
depend on which gauge action is "the" rule's action at finite a — the same L6 question B8 needs
decided); non-perturbative θ-sectors (instanton-like configurations) are not addressed by the
perturbative-order argument above.

DO NOT RE-ATTACK: the perturbative reality argument itself (CLOSED, exact at every order checked). This
is NOT a solution of the strong CP problem in the SM sense — CL279 is a deliberate non-claim, do not
overstate this row's result.

REFERENCES — findings: F321 (the reality argument), F53 (per-species C/CP, adjacent), F305, F307 (the
action-fork machinery, shared with B8/d1), F91 (pairing classification). Claims: `CL279` — read its
`not_claimed` position directly, this row must not exceed it. Ledger: this row's arg-det-M_q residual
is the same object as ledger parameters #1-6 (quark masses, E6) and CKM (E7) — closing those closes
part of this too.

EXTERNAL: named anchors — standard strong-CP literature (Peccei-Quinn as the SM's own unsolved
comparison point, not something this model claims to solve). Search terms: "theta vacuum lattice gauge
theory instanton nonperturbative", "strong CP problem lattice reality argument limitations".

FIRST STEP: check whether F321's reversal-closure argument depends on which action is chosen (the L6
question) — if yes, this row inherits B8's blocker and should note that dependency explicitly rather
than treat itself as independently closed.

WHAT PROMOTES THE GRADE: either an extension of the reality argument to include non-perturbative
configurations, or arg det M_q computed for the actual three-generation quark texture (which likely
needs E6/E7 progress first — check dependency before starting fresh work here).

WHAT WOULD FALSIFY THE ATTEMPT: finding the action-fork choice (L6) changes the reality conclusion —
would mean this row's QUANT grade is currently overstated and should move to PARTIAL pending L6.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *B12 — Gauge-boson masses, ρ, m_Z/m_W — `QUANT` → next: reduce the two remaining anchors (v, α)

**Leverage:** high, shares both anchors with the D-ledger's largest unresolved parameters. **Cost:**
see ledger #14 (α) and #17 (v) prompts — this row closes when those do. **Blocked by:** α_em (F127's
four-avenue no-go) and v (F119's anchor status).

~~~text
Physics Notes research session. Target: rubric row B12 (gauge-boson masses, ρ, m_Z/m_W), currently
QUANT, target: eliminate one of its two anchors (v or α).

WHAT IS ALREADY TRUE: the SM's electroweak sector takes three inputs {α, G_F, m_Z}; this model takes
TWO, because sin²θ_W^os=2/9 arrives from lattice geometry rather than being a third input. Eliminating
F141's stiffness quantum against e=g·sinθ_W DETERMINES it: u=18πα/7 ⇒ g²=18πα exactly, giving
m_W=(3v/2)√(2πα), m_Z=(9v/2)√(2πα/7). Residual stated FREE OF Δr (cancels to 2.2e-16 over
Δr∈[0,0.1]): +0.222% on m_W, +0.158% on m_Z; absolutes bracketed [80.147,80.548] and [90.879,91.332]
GeV, both containing PDG. ρ=1 EXACTLY from the RANK of F41's single Stueckelberg direction — not from
a custodial SU(2) this Higgs-free model cannot invoke. Now core claim 12 (CL276/CL277) in the public
summary as of Amendment 3, 2026-08-18.

THE RESIDUAL: two anchors remain, v and α — see ledger rows #14 and #17 below for their own dedicated
prompts. This row is a downstream consumer, not an independent target.

DO NOT RE-ATTACK: the ρ=1 rank derivation (closed exactly, F41), or the Δr-cancellation result (closed,
2.2e-16 residual is essentially exact).

REFERENCES — findings: F49, F141, F138, F231, F320 (the absolute-mass derivation this row rests on).
This row's real open work is in ledger parameters #14 (α_em) and #17 (v) — read those prompts.

EXTERNAL: n/a, shared target with #14/#17.

FIRST STEP: read ledger prompts #14 (α_em) and #17 (v) below.

WHAT PROMOTES THE GRADE: closing either anchor (see those prompts).

WHAT WOULD FALSIFY THE ATTEMPT: n/a.

PROTOCOL: this is research; see the ledger #14/#17 prompts for the primary attack and protocol.
~~~

## C — Matter content

### *C1 — Exactly three generations — `PARTIAL` → next: attack the physical-identification hypothesis

**Leverage:** high — shared premise with B10, B3. **Cost:** open-ended, may be genuinely hard.
**Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row C1 (exactly three generations), currently PARTIAL,
target: derive (or exclude deriving) the physical identification of the group-theory result with real
generations.

WHAT IS ALREADY TRUE: the group theory is a THEOREM (Σd²=48 ⇒ max single-valued irrep dim 3, T_1u
unique) — this part is closed and exact. F292 §6 independently found the same n-copies multiplicity
structure and explicitly DECLINED the inference to physical generations.

THE RESIDUAL: the identification of the T_1u triplet with the three observed fermion generations is a
STATED HYPOTHESIS (F75 §7, explicitly a "Candidate" finding, not a proof). F324 now makes the
*parity* of the generation count load-bearing for B10 (the colour-count row) as well, so this row's
resolution now has downstream consequences beyond its own content.

DO NOT RE-ATTACK: the Σd²=48 group theory itself, or F292's independent multiplicity check — both
closed. Do not re-derive that T_1u is the unique maximal single-valued irrep — closed.

REFERENCES — findings: F75 (the hypothesis, §7), F84 (downstream), F292 §6 (independent check,
declined inference), F324 (new load — the parity dependency for B10). Ledger: check
`open-derivations.md` for a C1-specific row; if none exists this itself is worth flagging.

ADDENDUM (2026-08-31 - 16:10, session note — reference-list correction, NO new finding number taken,
no new physics claimed): confirmed `open-derivations.md` has no C1-specific row. Also, this block's
reference list is incomplete and its FIRST STEP sends the next session at territory that is not
actually untouched. F75 §7.2 already names "compute [the T_1u crystal-field splitting] pattern and
compare its ratios to the observed lepton masses" as the natural next step, and that line has since
been run, repeatedly: F76 splits the T_1u triplet with an orthorhombic (D_2h) crystal field and
reproduces the charged-lepton Koide relation (states plainly that its amplitude √2 and phase δ are
INPUTS, not derived from the QCA rule); F93/F175 build the resulting E_g-plane order parameter and its
exact weight δ*=2/9 (=dim E_g/dim(T_1u⊗T_1u), i.e. built directly on F75's T_1u); F199, F230, and F253
are three INDEPENDENT no-go results (BPS route, crystal-field-geometric route, and topological/
scale-free route respectively) that each tried and failed to derive δ* — equivalently the sextic
coupling λ6 — from the T_1u geometry alone; F255 then derives HALF of the remaining posit exactly (the
E_g generator norm R=1, forced by Schur's lemma on the lepton-mass-deviation simplex) and narrows the
whole residual to one dimensionless coupling, λ6=0.243≈1/4, still an input as of 2026-07-16.
None of this closes C1's own question — whether T_1u MUST be physically realized as three generations
is still not derived — but it changes the shape of the residual: (a) the identification is not an
unused, free-floating hypothesis; it is load-bearing infrastructure for a charged-lepton mass-shape
prediction accurate to ~0.007%, which is evidence for it, not proof of it; (b) a session attacking
this row should NOT re-attempt the BPS, geometric, or topological/scale-free routes to δ*/λ6 —
F199/F230/F253 already close each of those negative; the live frontier for that thread is F255's
remaining coupling λ6, a narrower and different target than this row's stated one. Whether closing λ6
would itself count as closing C1's "must be physically realized" question, or is a separate result
that would leave C1 exactly where it is, is not decided anywhere in the tree and should be settled
explicitly before either is attacked. Recommend `open-derivations.md` get a dedicated C1 row carrying
this whole cluster (F75→F76→F93→F175→F199→F230→F253→F255→F256) rather than leaving it split across
this prompts file and scattered finding cross-references. No claim board entry opened for this note
(no finding number taken); logged in `docs/status/changelog.md` instead.

EXTERNAL: search terms — "three generations fermion lattice group theory selection", "flavor symmetry
breaking generation number derivation beyond group theory".

FIRST STEP: read F75 §7 and F292 §6 side by side to understand exactly why F292 declined the inference
— that reasoning is the actual obstacle this row needs to address, not a fresh literature search.

WHAT PROMOTES THE GRADE: an argument (dynamical, not just group-theoretic) for why the T_1u triplet
must be physically realized as three fermion generations specifically, closing the hypothesis gap.

WHAT WOULD FALSIFY THE ATTEMPT: a demonstration that the identification is NOT forced and genuinely
could be otherwise — itself a valuable, if negative, result.

PROTOCOL: this is research. Claim your topic first (note the B10 dependency). Take the next finding
number. Close with finding, test record, claim card. `make gate` before finish.
~~~

### *C3 — Colour triplet + fractional charge — `PARTIAL` → next: tracks B10/C1, no independent work needed yet

**Leverage:** low independent leverage — inherits B10 and C1. **Cost:** n/a until those close.
**Blocked by:** B10, C1.

~~~text
Physics Notes research session. Target: rubric row C3 (colour triplet + fractional charge), currently
PARTIAL, target: track B10/C1 closure.

WHAT IS ALREADY TRUE: fractional charge is FORCED by the 3y_Q+y_L=0 row, i.e. by N_c=3 specifically;
commensurability holds for ANY N_c (ratios 1:(1+N_c):(1-N_c):-N_c:-2N_c) — this part is general and
solid.

THE RESIDUAL: conditional on N_c=3, which as of F325 (2026-08-18) is conditional on F324's premise set,
which INCLUDES C1's generation-count parity. The conditionality changed character (no longer inherits
X1's unchosen branch, since X1 closed) but did not lift.

DO NOT RE-ATTACK: the commensurability result (general, closed) or the 3y_Q+y_L=0 forcing argument
(closed).

REFERENCES — findings: F136, F165 (S13→F279, cite with supersession), F279, F324. This row closes when
B10 and/or C1 close — read those prompts, do not work this row independently.

EXTERNAL: n/a, shared target.

FIRST STEP: read the B10 and C1 prompts in this file.

WHAT PROMOTES THE GRADE: B10 or C1 closing (see those prompts).

WHAT WOULD FALSIFY THE ATTEMPT: n/a.

PROTOCOL: work B10 or C1 instead; note in that finding that it also affects C3.
~~~

### *C4 — Neutrino nature (Dirac vs Majorana) — `PARTIAL` → next: find something that forces Majorana over Dirac

**Leverage:** medium — feeds C5, ledger #22. **Cost:** open-ended, may be genuinely underdetermined.
**Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row C4 (neutrino nature, Dirac vs Majorana), currently
PARTIAL, target: find a structural argument forcing one or the other, or document why the model is
genuinely agnostic.

WHAT IS ALREADY TRUE: the Higgs-free Majorana step is CONSTRUCTED (F47) and ν_R is a structurally-
FORCED total singlet (Y=0 — the very row that closes the hypercharge system, B4). This is real
structure, not an assumption bolted on.

THE RESIDUAL: nothing in the model FORCES Majorana over Dirac — the construction permits Majorana but
does not exclude a Dirac alternative. This row has been unmoved for at least five reports.

DO NOT RE-ATTACK: the Y=0 forcing of ν_R as a singlet (closed, exact) — that's necessary for either
Dirac or Majorana, not a discriminator between them.

REFERENCES — findings: F47 (the Majorana construction), F266 (adjacent). Ledger: `open-derivations.md`
row **D4** treats the related ν absolute scale and Dirac CP phase — read it for adjacent context, note
that it explicitly flags the Dirac-CP-phase question as possibly inheriting F254's no-go, which is a
related but distinct question from THIS row's Dirac-vs-Majorana nature question.

EXTERNAL: named anchors — standard neutrinoless double-beta decay experimental status (as the empirical
test that would settle Majorana vs Dirac in reality, separate from what this model predicts) — search
"neutrinoless double beta decay current experimental bound", "Majorana vs Dirac neutrino theoretical
discriminators lattice models".

FIRST STEP: check whether the model's own lepton-number structure (any residual global or discrete
symmetry in the tree) forbids or permits a Dirac mass term for ν_R independently of the Majorana
construction — this is the natural first place a forcing argument would live.

WHAT PROMOTES THE GRADE: a structural argument (symmetry, consistency, or dynamical) that forces one
option, OR a clear, reasoned statement that the model is genuinely agnostic here (which is itself worth
stating plainly rather than leaving as an unexamined gap).

WHAT WOULD FALSIFY THE ATTEMPT: none direct — exploratory.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *C5 — Neutrino mass mechanism — `PARTIAL` → next: find any scale link for M_R

**Leverage:** medium, shared with ledger #22. **Cost:** open-ended. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row C5 (neutrino mass mechanism), currently PARTIAL,
target: find a scale link for M_R (the absolute Majorana mass scale), currently free.

WHAT IS ALREADY TRUE: the see-saw mechanism plus the E_g/ℤ3 texture FIX the three light masses and the
hierarchy at MACHINE PRECISION (F236, F254) — the shape is fully derived. Only the absolute scale is
open.

THE RESIDUAL: M_R (ledger parameter #22) is completely unfixed — "nothing in the model fixes M_R"
per `open-derivations` row D4.

DO NOT RE-ATTACK: the see-saw shape/hierarchy derivation (closed, machine precision, F236).

REFERENCES — findings: F47, F236, F254. Ledger: `open-derivations.md` row **D4** — read in full,
it's the authoritative current statement including the suggested first check: "does the F183/F107
cell or the E_g condensate offer any scale link before treating it as a free anchor."

EXTERNAL: search terms — "seesaw mechanism Majorana scale grand unification", "right-handed neutrino
mass scale theoretical bounds leptogenesis" (leptogenesis constraints may bound M_R indirectly — check
F202's baryogenesis work for any existing connection).

FIRST STEP: `open-derivations` D4's own suggested first step: check whether the F183/F107 cell or the
E_g condensate (already used for the shape) offers ANY scale link for M_R before treating it as
irreducibly free. This is explicitly named as the cheapest thing to check first.

WHAT PROMOTES THE GRADE: any structural link tying M_R to an existing model scale (even a rough one,
which could then be tightened), moving this from OPEN toward FIT or PARTIAL with a named mechanism.

WHAT WOULD FALSIFY THE ATTEMPT: none direct — a genuine null result (no link found) is worth stating.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### C7 — Beyond-SM content — `PARTIAL` → next: run the whole-tree grep for B-violating rates, Unruh, topological relics

**Leverage:** low-medium, mostly a measurement gap not a physics gap. **Cost:** small — a grep sweep.
**Blocked by:** device/workspace access for a whole-tree search (available this session, underused).

~~~text
Physics Notes research session. Target: rubric row C7 (beyond-SM content), currently PARTIAL, target:
resolve the carried-forward "proton decay sub-row not re-measured" caveat.

WHAT IS ALREADY TRUE: the model predicts a Planck-mass BH-remnant geon, cold and collisionless,
M_rem=(√3/2)^(1/2) M_Pl exact (F228). It excludes its own alternatives structurally: native massive
spin-2 (CN5), ν_R ν_R J=2 tensor channel (CN6), the Alcubierre warp family (F204), and keV sterile as
100% of dark matter.

THE RESIDUAL: the "proton decay" sub-row (a baryon-number-violating rate) has been CARRIED FORWARD,
UNMEASURED, across at least three completeness reports because the whole-tree keyword grep the command
prescribes needs full repository access that recent sessions (including this one, in part) have not
had. The same is true for the Unruh effect (inside E9/G10) and topological defects as relics (inside
K7/K12) — all three are named ABSENT candidates that were last actually re-verified by grep some
reports ago, and the 2026-08-18 baseline explicitly notes even "Witten" returns zero against the
indexes despite F324 being built on the Witten anomaly — proof the index-only grep under-reports.

DO NOT RE-ATTACK: the excluded-alternatives results (CN5, CN6, F204's Alcubierre exclusion, keV-sterile
exclusion) — all closed.

REFERENCES — findings: F223, F228, F266, F216, F204, F237. This is primarily a MEASUREMENT task, not a
derivation task — the physics doesn't need new work, the tree needs searching.

EXTERNAL: n/a — internal measurement task.

FIRST STEP: from the repository root (with real device/shell access — the 2026-08-20 report's own
device-bridge session had this and could have done it but prioritized the live health probe instead),
run: `grep -ril "proton decay\|baryon.number.violat" findings/ papers/ docs/theory/`,
`grep -ril "Unruh" findings/ papers/ docs/theory/`, and
`grep -ril "topological defect\|cosmic string\|domain wall" findings/ papers/ docs/theory/` — report
exact hit counts and file names, not just "zero" or "some".

WHAT PROMOTES THE GRADE: a genuine, dated whole-tree grep result (even if it confirms zero hits) —
this closes the measurement gap and lets the ABSENT section's caveat finally be retired rather than
carried forward again.

WHAT WOULD FALSIFY THE ATTEMPT: finding real hits that should be a rubric ABSENT row or an existing
row's evidence and are not currently cited anywhere — report these explicitly, they may need a new
open-derivations entry.

PROTOCOL: this is closer to an audit than physics research — no claim needed in session-claims.yaml
unless the grep turns up something requiring a finding. If it does, follow the normal finding protocol
from there.
~~~

## D — The parameter ledger

### *D#1-6 — Quark masses (m_u, m_d, m_s, m_c, m_b, m_t) — `ABSENT ×6` → next: OPEN, a first attack

**Leverage:** very high — 6 of the ledger's 28 slots, and the largest single ABSENT block in the
whole rubric. **Cost:** unknown, possibly a new sector. **Blocked by:** nothing named, simply
unattempted.

~~~text
Physics Notes research session. Target: ledger parameters #1-6 (six quark masses m_u...m_t), currently
ABSENT ×6, target OPEN (a first computation and a named attack, promotable to open-derivations).

WHAT IS ALREADY TRUE: F121 is explicit that the numbers currently associated with quark masses are
"the measured values converted to kg — a CONSISTENCY readout," not a derivation. The constituent-quark
scale m_c=309.5 MeV from one f_π anchor (F123) is a DIFFERENT quantity (constituent, not current-quark
mass) and must not be conflated with this row.

THE RESIDUAL: no route has been proposed at all. The lepton sector's shape/scale split (F175/F234 for
shape, F121 for scale) is a charged-LEPTON argument specifically — F80-D4 already shows the up/down Q
values (0.85, 0.73) sit OUTSIDE the clean-pair band the lepton argument needs, which is evidence the
E_g/T_1u machinery may be structurally lepton-only.

DO NOT RE-ATTACK: applying the charged-lepton E_g/T_1u shape argument directly to quarks without first
checking F80-D4's negative evidence — that would repeat a check already flagged as likely to fail.

REFERENCES — findings: F121 (the consistency-readout statement), F123 (constituent scale — a different
quantity, cite to explicitly distinguish), F80 (§D4, the Q-value evidence against a naive lepton-style
extension). Ledger: `open-derivations.md` row **E6** — read it in full, it already frames the smallest
useful first question: "does the E_g/T_1u machinery that gives the charged-lepton SHAPE to 0.007% have
ANY quark-sector face, or is it structurally lepton-only?" A clean NO here would itself be a valuable
no-go worth having, per the ledger's own framing.

EXTERNAL: named anchors — PDG quark mass values (current-quark, MS-bar scheme) for the target numbers
themselves. Search terms: "quark mass generation mechanism lattice model beyond Higgs", "constituent
vs current quark mass relation chiral symmetry breaking".

FIRST STEP: E6's own smallest-version question — attempt the E_g/T_1u shape argument on the quark
sector directly and see where/how it fails (or, less likely, succeeds), using F80-D4's Q-value
mismatch as the first thing to explain or resolve.

WHAT PROMOTES THE GRADE: ABSENT → OPEN requires a named attack and a first computation, even an
unsuccessful one, plus a new open-derivations row. A clean structural no-go (quark masses provably
outside this model's current machinery) is a legitimate, valuable outcome and promotes the grade just
as much as a partial success would.

WHAT WOULD FALSIFY THE ATTEMPT: n/a at the OPEN stage — any serious, documented first attempt promotes
the grade regardless of outcome.

PROTOCOL: this is research. Claim your topic in docs/design/session-claims.yaml before any physics.
Take the next finding number from `casim index`. Close with the finding (even a negative result is a
finding), a test record if a computation was run, and a claim card only if something is actually
asserted (a pure no-go might not need one — check `docs/claims/README.md`'s contract). Update
`open-derivations.md` to add this row under Part A (or Part B if it closes negative). `make gate`
before finish.
~~~

### *D#7-8 — Charged-lepton mass ratios (shape) — `QUANT ×2` → next: extend to angular-mode dynamics

**Leverage:** low independent — already the tree's best-derived flavor result. **Cost:** small
refinement only. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: ledger parameters #7-8 (m_e/m_τ, m_μ/m_τ shape), currently
QUANT ×2, target: tighten toward PARTIAL/MACHINE if a next-order correction is tractable.

WHAT IS ALREADY TRUE: ≤0.007% agreement with ZERO shape parameters, from {δ*=2/9, η²=1/2}; Koide
Q=2/3 at 0.91σ. This is already an exceptionally tight result — the residual is small enough that
further work has low marginal value compared to the rest of the ledger.

THE RESIDUAL: 0.007% — likely a next-order correction to the E_g crystal-field splitting, not
currently identified as a named object.

DO NOT RE-ATTACK: the core δ*=2/9, η²=1/2 derivation (closed, F175/F234/F76).

REFERENCES — findings: F175, F234, F120, F76 (crystal-field splitting origin). 

EXTERNAL: search terms — "Koide formula charged lepton mass relation higher order corrections".

FIRST STEP: identify whether the 0.007% residual has a natural next-order candidate in the existing
crystal-field expansion (F76) before assuming new physics is needed.

WHAT PROMOTES THE GRADE: a named, computed next-order correction closing some fraction of the 0.007%.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this is a low-priority refinement, not a structural question;
consider whether time is better spent on higher-priority rows (d1, K9, Q4) before claiming this one.

PROTOCOL: this is research, low priority. Claim your topic first if pursuing. Take the next finding
number. Close with finding, test record, claim card. `make gate` before finish.
~~~

### *D#9 — Charged-lepton overall scale — `FIT (N=1)` → next: kill the τ anchor via the α_s transmutation channel

**Leverage:** shared with d1/B8. **Cost:** n/a until d1 closes. **Blocked by:** d1 (ledger #16).

~~~text
Physics Notes research session. Target: ledger parameter #9 (charged-lepton overall scale), currently
FIT (N=1), target PARTIAL by eliminating the τ anchor.

WHAT IS ALREADY TRUE: τ-anchored (F121). F233 already reduces the gap to a factor 1.9 with ZERO
parameters via the α_s dimensional-transmutation channel.

THE RESIDUAL: F233's channel inherits the SAME unchosen/now-partially-closed branch as d1 — this row's
cheapest next step is identical to B8's: close d1 leg 3.

DO NOT RE-ATTACK: F233's factor-1.9 reduction itself (closed, zero parameters).

REFERENCES — findings: F121, F233. This row closes in lockstep with **ledger #16 / B8's d1 leg 3** —
read that prompt, do not work this independently.

EXTERNAL: n/a, shared target.

FIRST STEP: read the B8 / ledger #16 prompt.

WHAT PROMOTES THE GRADE: d1 closing (see B8's prompt).

WHAT WOULD FALSIFY THE ATTEMPT: n/a.

PROTOCOL: work B8/d1 instead; note this row as a dependent in that finding.
~~~

### *D#10-13 — CKM (3 angles + 1 phase) — `ABSENT ×4` → next: state plainly this is a scope choice, and revisit whether it should be

**Leverage:** low. **Cost:** the model currently has no mechanism at all for inter-generation mixing in
the quark sector — this may require D#1-6 (quark masses) to exist first. **Blocked by:** D#1-6.

~~~text
Physics Notes research session. Target: ledger parameters #10-13 (CKM: 3 angles + 1 CP phase),
currently ABSENT ×4 and declared OUT OF SCOPE, target: confirm whether "out of scope" should remain a
choice or whether a first attack is now worth attempting.

WHAT IS ALREADY TRUE: J(1)=0 is one-generation arithmetic (the Jarlskog invariant is trivially zero
with one generation), NOT a genuine three-generation CKM prediction. This has been explicitly and
honestly scoped OUT, not silently omitted.

THE RESIDUAL: CKM mixing requires quark mass eigenstates to be non-trivially misaligned across
generations — which presupposes the quark masses themselves exist as derived (or at least structured)
objects. This row is very likely gated on D#1-6 (quark masses) making progress first.

DO NOT RE-ATTACK: attempting CKM angles without first checking whether D#1-6 has moved — this is
almost certainly premature until the quark-mass sector has SOME structure beyond "measured and
converted."

REFERENCES — findings: F121, F233 (quark-sector scale context). Ledger: `open-derivations.md` row
**E7** covers CKM alongside the v/lepton-scale anchors — read it, it explicitly states "leave scoped,
but record that out of scope is a CHOICE, not a result, so it does not read as closed."

EXTERNAL: search terms — "CKM matrix theoretical prediction beyond Standard Model flavor texture" —
mostly useful for comparison once (if) a model-native mechanism is found.

FIRST STEP: check D#1-6's status (has any quark-sector mixing structure emerged from that work?) before
attempting anything here directly.

WHAT PROMOTES THE GRADE: this specific row promotes only after D#1-6 gives quark mass eigenstates
enough structure to ask a mixing question at all. Until then, the correct action is to RE-CONFIRM the
scope choice is still the honest one (rather than silently drifting into looking closed) — that alone
is a legitimate, cheap session output.

WHAT WOULD FALSIFY THE ATTEMPT: n/a at this stage.

PROTOCOL: work D#1-6 first if pursuing the underlying physics; if only re-confirming the scope
statement, no finding number is needed — a one-line changelog entry noting the re-confirmation
suffices.
~~~

### *D#14 — α_em — `OPEN` → next: re-examine the four-avenue no-go's assumptions

**Leverage:** very high — feeds B12 (two absolute boson masses) and B4 (charge unit). **Cost:**
medium — re-examining a closed no-go's premises, not starting fresh. **Blocked by:** nothing named
beyond the no-go itself.

~~~text
Physics Notes research session. Target: ledger parameter #14 (α_em), currently OPEN with a four-avenue
no-go against it (F127), target: re-examine whether any of the four avenues' underlying assumptions
can be relaxed, or confirm the no-go is comprehensive.

WHAT IS ALREADY TRUE: F127 established a four-avenue no-go on deriving α_em from the rule directly.
This parameter now carries unusually high weight: it feeds TWO absolute boson masses (B12: m_W, m_Z)
and the charge unit itself (B4).

THE RESIDUAL: the no-go's specific four avenues and their closing arguments need to be read directly —
this prompt does not have their detail to hand (F127 was cited but not quoted at length in the source
report). This is exactly the kind of "closed-negative, re-examine the ONE assumption whose failure
would reopen it" prompt the skill's own template calls for.

DO NOT RE-ATTACK: whichever of the four avenues F127 closes with a genuinely exact or structural
argument — re-read F127 first to know which is which before starting.

REFERENCES — findings: F127 (the no-go itself — READ IN FULL, this prompt cannot substitute for it).
Ledger: check `open-derivations.md` for a dedicated α_em row (may not exist as its own entry — the
2026-08-18 baseline's rubric table cites F127 alone for this ledger row).

EXTERNAL: named anchor — CODATA α_em value and its measurement precision (10^-10 level) as the target
this row would need to hit for a genuine derivation to be credible. Search terms: "fine structure
constant derivation attempts lattice discrete models", "alpha electromagnetic coupling theoretical
prediction historical attempts" (useful context: many claimed α derivations in the broader physics
community have not survived scrutiny — treat any positive result here with extra adversarial care).

FIRST STEP: read F127 in full and identify, for EACH of the four avenues, the single assumption whose
failure would reopen that avenue specifically — this is the "reopening condition" the skill's template
requires and it does not yet exist for this row.

WHAT PROMOTES THE GRADE: EITHER a demonstration that all four reopening conditions genuinely fail
(hardening OPEN into a fully-characterized EXCLUDED with named reopening conditions, which is itself
valuable), OR a successful attack along a fifth avenue F127 did not consider.

WHAT WOULD FALSIFY THE ATTEMPT: a "derivation" that turns out to smuggle in the measured α value
somewhere non-obvious — be unusually careful here given this field's history of false positives.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### D#15 — g2/sin²θ_W — `QUANT` → carried, see B6

*Same target as rubric row B6 — see that prompt above. No separate work needed.*

### D#16 — g3/α_s — `PARTIAL` → carried, see B8

*Same target as rubric row B8's d1 leg 3 — see that prompt above (priority #1 of this report). No
separate work needed; this ledger row and B8 close together.*

### *D#17 — v (electroweak scale) — `FIT (N=1)` → next: check for any structural link to G or the lattice spacing

**Leverage:** high — anchors B12's two boson masses and D#9's lepton scale. **Cost:** unclear, may be
a genuinely hard anchor to eliminate. **Blocked by:** nothing named, simply an unexamined question.

~~~text
Physics Notes research session. Target: ledger parameter #17 (v, the electroweak scale), currently
FIT (N=1), target: find any structural link reducing it from a free anchor.

WHAT IS ALREADY TRUE: "the electroweak scale v is an anchor, not an output" (F119, Scope). It now
carries m_W and m_Z absolutely (via B12/F320) — so eliminating it would be unusually high-leverage,
closing multiple downstream rows at once.

THE RESIDUAL: no route has been found. `open-derivations` row **L3** (lattice spacing a) is adjacent:
"absolute lattice spacing a cannot be pinned by any dimensionless mass-blind observable" (a proven
degeneracy theorem, F232) — the ONE dimensionful pin currently used is G, giving a=√(8π)·3^(1/4)·ℓ_P.
Whether v could be a SECOND dimensionful pin, or is forced by the same one, has apparently not been
asked directly.

DO NOT RE-ATTACK: the L3 scale-invariance/degeneracy theorem (closed exactly, F232) — v cannot be
pinned by a dimensionless mass-blind observable, full stop; any attack here must either use a
dimensionFUL observable or accept v stays free.

REFERENCES — findings: F119 (the anchor statement), F320 (downstream absolute masses). Ledger:
`open-derivations.md` row **L3** (adjacent scale-pinning theorem — read for the degeneracy result that
constrains what KIND of attack could possibly work) and row **E7** (groups v with the CKM/lepton-scale
question, notes it inherits d1's fork — check whether v specifically, not just the lepton scale, has
that same dependency).

EXTERNAL: search terms — "electroweak scale hierarchy problem alternative derivation", "Higgs-free
electroweak scale origin lattice model" (this model is Higgs-free by decision, F27/F41 — any v
derivation must respect that, not smuggle in a Higgs potential minimization).

FIRST STEP: re-read F232's exact degeneracy theorem statement and determine precisely which
observables it excludes as v-pinning candidates and which (if any) it does not — this scopes what is
even worth trying.

WHAT PROMOTES THE GRADE: a genuine dimensionful pin for v (parallel to G's role for a), OR a proof
that no such pin can exist within this model's structure (which would make FIT (N=1) a documented,
understood ceiling rather than an unexamined gap).

WHAT WOULD FALSIFY THE ATTEMPT: none direct — exploratory, but be alert to the same false-positive risk
class as α_em (D#14): a plausible-looking derivation that secretly uses the measured v somewhere.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *D#18 — m_H — `OPEN` → next: attempt the binding-dynamics calculation as a hadronic-analogue problem

**Leverage:** medium, isolated. **Cost:** large — genuinely new binding-dynamics machinery, by the
model's own account. **Blocked by:** nothing named, simply unattempted as framed below.

~~~text
Physics Notes research session. Target: ledger parameter #18 (m_H = 125.25 GeV), currently OPEN,
target: attempt the binding-dynamics calculation nobody has tried in this framing.

WHAT IS ALREADY TRUE: F73's spin-0 bound-pair ("Cooper-pair Higgs candidate") KINEMATICS are EXACT —
the object exists in the model's spectrum as a well-defined kinematic construction.

THE RESIDUAL: free-sum kinematics cannot reproduce 125.25 GeV; the missing input is BINDING DYNAMICS,
not kinematics. Because this model is Higgs-free by decision (CLAUDE.md #3, F27/F41), this is a
bound-state mass calculation, not a fundamental parameter — structurally HARDER than the SM's own
m_H, not an excused gap.

DO NOT RE-ATTACK: F73's kinematic construction itself (exact, closed) — the gap is specifically
dynamics, not the object's existence or its free-particle spectrum.

REFERENCES — findings: F73 (the kinematics), and by explicit analogy the successful hadronic-binding
programme: F103/F104 (dynamical pion, deuteron — the class of calculation this row needs), F126/F128
(the OBE-derived nuclear binding machinery that closed similar gaps elsewhere in the tree).

EXTERNAL: named anchor — the measured Higgs mass 125.25 GeV (PDG) as the target; standard bound-state
QFT binding-energy methods (Bethe-Salpeter or similar) as a possible cross-check framework, used
carefully since this is a lattice CA model, not continuum QFT. Search terms: "composite Higgs bound
state binding energy calculation", "Bethe-Salpeter equation lattice bound state mass".

FIRST STEP: `open-derivations` E8's own suggested framing: treat this as the electroweak analogue of
the F103/F104/F126 hadronic-binding programme — the machinery that binds the deuteron from derived
one-boson-exchange is the same CLASS of object F73 is missing here. Start by mapping F73's constituent
structure onto the same binding-calculation template those findings used.

WHAT PROMOTES THE GRADE: a binding-dynamics calculation that produces a mass, compared honestly against
125.25 GeV whether it matches or not.

WHAT WOULD FALSIFY THE ATTEMPT: a binding calculation that converges to a mass far from 125.25 GeV
would be a genuinely important negative result about this Higgs-free construction, not a failure to
hide.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### D#19 — θ_QCD — `PARTIAL` → carried, see B11

*Same target as rubric row B11 — see that prompt above. No separate work needed.*

### D#22 — ν absolute scale (M_R) — `OPEN` → carried, see C5

*Same target as rubric row C5 — see that prompt above. No separate work needed.*

### D#23-25 — 3 PMNS angles — `EXCLUDED ×3` → next: re-examine the ONE assumption that would reopen them

**Leverage:** low — this is a closed no-go, re-examination only. **Cost:** small, focused.
**Blocked by:** n/a, this is the "EXCLUDED → re-examination" prompt type.

~~~text
Physics Notes research session. Target: ledger parameters #23-25 (3 PMNS mixing angles), currently
EXCLUDED ×3 (proven permanently free), target: re-examine the reopening condition, NOT re-derive them.

WHAT IS ALREADY TRUE: F254 PROVES no lattice selector exists: under the E_g-stabiliser D_2h, the three
T_2g amplitudes are three INEQUIVALENT 1-d irreps (B_1g ⊕ B_2g ⊕ B_3g), so no residual symmetry
relates them. Only the full 3-amplitude fit reaches NuFIT (3 inputs / 3 angles, no slack). This is
PERMANENTLY FREE, and that freedom being PROVEN is itself the result — stated explicitly as a
positive, not a gap.

THE REOPENING CONDITION (name it, per the skill's template for EXCLUDED rows): the D_2h stabiliser
assignment itself. If the E_g condensate's actual symmetry-breaking pattern were NOT D_2h (e.g. if a
different, lower-symmetry stabiliser applied), the irrep-inequivalence argument could change. F254's
result is conditional on D_2h being the correct stabiliser group for the physical vacuum.

DO NOT RE-ATTACK: deriving the PMNS angles directly — CLOSED, proven impossible under D_2h. State
plainly: "the no-go survives" is a SUCCESSFUL outcome for any re-examination session, not a failure.

REFERENCES — findings: F254 (the no-go itself — read in full for the D_2h derivation), F93 (the
orthorhombic/E_g vacuum identification this rests on). Ledger: `open-derivations.md` row **D1** —
read it, it already states "this row should arguably be in Part B [closed-negative]" and is kept in
Part A only because the DYNAMICAL computation of three independent T_2g gaps has never actually been
run (a different, narrower question than re-deriving the angles).

EXTERNAL: NuFIT current global fit values (for context on what the 3-amplitude fit is matching, not as
a target to derive). Search terms: "PMNS matrix symmetry protected mixing angles theoretical models".

FIRST STEP: test the D_2h stabiliser assignment itself — is there any way the E_g condensate's vacuum
symmetry could be a DIFFERENT point group, and if so does F254's inequivalence argument survive? This
is the reopening condition, and testing it (not re-deriving the angles) is this prompt's actual task.

WHAT PROMOTES THE GRADE: n/a in the usual sense — EXCLUDED does not promote to a "better" grade by
being re-derived; a successful re-examination REPORTS whether the reopening condition holds or fails.
If D_2h is confirmed robust, this row is FURTHER hardened (worth stating explicitly in the ledger).

WHAT WOULD FALSIFY THE NO-GO: a demonstration that the vacuum stabiliser is genuinely NOT D_2h — this
would be a significant finding and should reopen the row rather than be filed as a side note.

PROTOCOL: this is research, but of the re-examination type — expect "the no-go survives" as the modal
outcome and treat it as success. Claim your topic first. Take the next finding number if anything
new is found either way. `make gate` before finish if code changes.
~~~

### *D#26 — ν Dirac CP phase — `ABSENT` → next: confirm formally whether it inherits F254's no-go

**Leverage:** low, but cheap. **Cost:** small — "worth one session" per the ledger's own estimate.
**Blocked by:** nothing.

~~~text
Physics Notes research session. Target: ledger parameter #26 (ν Dirac CP phase δ_CP), currently
ABSENT, target: confirm formally whether it inherits F254's PMNS no-go (which would move it
ABSENT → EXCLUDED, a result).

WHAT IS ALREADY TRUE: not addressed anywhere in the tree currently. `open-derivations` row D4 states
plainly the working hypothesis: "δ_CP inherits F254's no-go — if the T_2g amplitudes are free, the
phase built from them is too."

THE RESIDUAL: this inheritance has never been formally checked, only asserted as plausible. The ledger
explicitly flags this as "worth one session to confirm formally... which would move #26 ABSENT →
EXCLUDED" and notes "nobody has spent it."

DO NOT RE-ATTACK: F254's underlying PMNS no-go itself (closed) — this prompt is specifically about
whether the CP PHASE (built from the same amplitudes) is subject to the same argument, which is a
short, focused formal check, not a fresh derivation.

REFERENCES — findings: F254 (the PMNS no-go to check inheritance against). Ledger: `open-derivations.md`
row **D4** states the exact task.

EXTERNAL: standard PMNS Dirac CP phase parametrization conventions (for making the formal check
precise) — no external literature search needed beyond that, this is an internal consistency check.

FIRST STEP: write out δ_CP explicitly in terms of the three T_2g amplitudes (B_1g, B_2g, B_3g) using
the standard PMNS parametrization, and check directly whether F254's inequivalent-irrep argument
applies to that combination the same way it applies to the angles themselves.

WHAT PROMOTES THE GRADE: a formal confirmation moves ABSENT → EXCLUDED (a result, per the ledger's own
framing) — this is explicitly named as the expected, cheap outcome.

WHAT WOULD FALSIFY THE ATTEMPT: finding the phase is NOT simply inherited (e.g. it depends on some
additional structure the angles don't) — would be a more interesting and higher-value result than the
expected confirmation, and should be written up carefully if found.

PROTOCOL: this is a short, focused research session. Claim your topic first. Take the next finding
number. Close with finding, test record if a computation was involved, claim card if warranted.
`make gate` before finish.
~~~

### D#28 — Λ (cosmological constant) — `OPEN` → carried, see K9

*Same target as rubric row K9 (and A11) — see the K9 prompt in block K below. No separate work needed;
this is the single highest-value target after d1 (priority #2 of this report).*

## E — Gravity and general relativity

### *E1 — Fundamental field equation — `POSIT` → next: re-derivability attack

**Leverage:** low, foundational decision. **Cost:** large, likely closed. **Blocked by:** n/a.

~~~text
Physics Notes research session. Target: rubric row E1 (fundamental field equation), currently POSIT,
target: derive the induced Einstein equation, or further harden why every alternative route is closed.

WHAT IS ALREADY TRUE: DECISION 2026-06-29 (F178) adopts G_μν=(8πG/c⁴)T_μν as fundamental, with the
K=exp(2GM/rc²) dielectric as its vacuum/weak-field representation. Alternatives are already closed:
the energy-only law is not Lorentz covariant and has no neutron-star maximum mass.
INDEPENDENTLY CONFIRMED SINCE on an unrelated observable: F297's BBN gives the demoted (energy-only)
law Y_p=0.1856, -17.6σ, against the full-tensor law's -0.11σ — a genuinely independent cross-check
that the decision made the right call.

THE RESIDUAL: this is a POSIT — a founding decision after alternatives were closed, not a target.

DO NOT RE-ATTACK: the energy-only alternative (closed twice now — Lorentz covariance and NS mass
originally, BBN independently since). Carry the alternatives already closed in open-derivations Part C
before proposing a new one.

REFERENCES — findings: F178 (the decision), F297 (independent confirmation). Key decisions:
`docs/theory/key-decisions.md` entry for this POSIT.

EXTERNAL: search terms — "induced gravity derivation from microscopic theory", "emergent Einstein
equations lattice models" — for comparison with other emergent-gravity programmes' derivation attempts.

FIRST STEP: read key-decisions.md's own stated reasoning for why this is POSIT rather than derived, and
check whether any NEW model content since 2026-06-29 (the decision date) offers a derivation route that
didn't exist then.

WHAT PROMOTES THE GRADE: a genuine derivation of the induced Einstein equation from more primitive
model content, OR further hardening (a second, independent closure of yet another alternative,
strengthening the POSIT's own justification).

WHAT WOULD FALSIFY THE ATTEMPT: n/a — POSIT rows don't get falsified, they get derived or stay posited.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *E4 — Classical tests — `QUANT` → next: push the 3e-8 residual, likely low priority

**Leverage:** low, already tight. **Cost:** small. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row E4 (classical GR tests), currently QUANT (3e-8
residual), target: identify whether the residual has a named source worth closing further.

WHAT IS ALREADY TRUE: Mercury perihelion 42.98"/cy, solar-limb deflection 1.7512", Shapiro delay,
gravitational redshift — all matching GR to 3e-8, from F64/F107/F111.

THE RESIDUAL: 3e-8 — likely numerical/integration precision rather than a physics gap, given the
model's field equation already matches GR exactly at this order structurally (E3 is EXACT).

DO NOT RE-ATTACK: the underlying K=exp(2GM/rc²) dielectric derivation (closed, E1/E3 are POSIT/EXACT).

REFERENCES — findings: F64, F107, F111.

EXTERNAL: n/a — internal numerical question.

FIRST STEP: determine whether the 3e-8 is a numerical-integration floor (in which case tightening it
is a low-value software task) or a genuine physical residual (in which case it deserves more
attention) — this diagnosis alone is the useful output if pursued.

WHAT PROMOTES THE GRADE: identifying the residual's source and, if physical, naming it.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, low priority — deprioritize relative to d1/K9/Q4.

PROTOCOL: low-priority research; claim only if picking this up ahead of higher-priority rows.
~~~

### E7 — Inspiral / ringdown QNM — `QUANT` → next: tighten the WKB <7% bound with a more exact method

**Leverage:** low-medium. **Cost:** medium, a genuine numerical-methods upgrade. **Blocked by:**
nothing.

~~~text
Physics Notes research session. Target: rubric row E7 (inspiral/ringdown quasinormal modes), currently
QUANT (<7% via WKB), target: a tighter method (Leaver continued-fraction or similar) for machine-
precision QNM frequencies.

WHAT IS ALREADY TRUE: GW150914 chirp mass 28.1 M☉, ISCO 67.6 Hz reproduced; ringdown QNM spectrum via
WKB approximation matches GR fundamentals to <7% (F187).

THE RESIDUAL: WKB is an APPROXIMATION method — the <7% is a method-precision limit, not necessarily a
physics limit, since the underlying black-hole solution (E8) is EXACT Schwarzschild/Kerr.

DO NOT RE-ATTACK: the exact Schwarzschild/Kerr solution itself (closed, E8) — this row's gap is
specifically the ringdown-frequency EXTRACTION method's precision, not the underlying spacetime.

REFERENCES — findings: F189 (inspiral), F187 (WKB ringdown).

EXTERNAL: named anchor — Leaver's continued-fraction method for exact Kerr QNM frequencies (standard
GR technique) — check whether it can be applied directly since the model's black hole IS exact
Schwarzschild/Kerr. Search terms: "Leaver continued fraction quasinormal mode exact", "black hole
ringdown frequency precision methods beyond WKB".

FIRST STEP: since E8 already establishes the model's black hole as exact GR, check whether a standard
exact QNM method (Leaver) can simply be applied directly rather than needing new physics — this may be
a numerical-methods exercise, not a derivation.

WHAT PROMOTES THE GRADE: QNM frequencies computed to machine precision via an exact method, moving this
row toward MACHINE.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, low-medium priority methods upgrade.

PROTOCOL: this is research, moderate priority. Claim your topic first. Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### *E8 — Black holes — `QUANT` → next: tighten the shadow number's residual pathway

**Leverage:** low, already strong (exact Schwarzschild/Kerr). **Cost:** small. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row E8 (black holes), currently QUANT (shadow 3√3 M),
target: verify whether any residual remains after the F114 withdrawal, or confirm this is effectively
EXACT/MACHINE already.

WHAT IS ALREADY TRUE: exact Schwarzschild/Kerr WITH horizon (this is itself notable — the model's
earlier horizon-free dielectric picture, F114, is WITHDRAWN, cards CL023-CL027, in favor of the
full-tensor-source canonical object). The +4.63% shadow discrepancy, echoes, and absent Hawking
spectrum from the earlier F114 picture are all withdrawn along with it.

THE RESIDUAL: graded QUANT with "shadow 3√3 M" as the residual/free-input column entry — but this
value IS the exact GR value, raising the question of whether this row should already be EXACT rather
than QUANT. Worth a direct check rather than assumed.

DO NOT RE-ATTACK: F114's superseded horizon-free picture (withdrawn, do not resurrect).

REFERENCES — findings: F183 (canonical Schwarzschild/Kerr adoption), F186 (shadow ray-tracer,
confirms 3√3 M by direct geodesic integration).

EXTERNAL: M87* and Sgr A* EHT shadow measurements (for comparison, not derivation target) — search
"Event Horizon Telescope shadow measurement M87 SgrA current results".

FIRST STEP: re-read F183 and F186 directly to determine whether "3√3 M" in the residual column
actually represents a departure from exact GR, or whether this is a labeling residue from before the
F114 withdrawal that should now read EXACT — this is a grading-precision check, not new physics.

WHAT PROMOTES THE GRADE: confirming this row should move to EXACT/MACHINE (a correction, not new
physics) — or, if a genuine residual exists, naming it precisely.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this is a grading audit.

PROTOCOL: low-effort audit; a finding is not necessarily needed, just a note in the next completeness
sweep with the corrected grade and reasoning if it changes.
~~~

### *E9 — BH thermodynamics — `PARTIAL` → next: compute the boundary entanglement entropy against 2π√3

**Leverage:** medium. **Cost:** medium — uses existing F300 machinery. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row E9 (BH thermodynamics), currently PARTIAL, target:
compute the boundary entanglement entropy and check it against 2π√3.

WHAT IS ALREADY TRUE: S=A/4 is reproduced IFF each boundary cell carries 2π√3 = 10.8828 nats. F300
G10-12 PROVES the naive state-count reading is impossible (e^(2π√3)=53252.295 is 0.295 from the
nearest integer; 2π√3/ln2=15.7006 is 0.299 from one) — the cell entropy is NOT a state count of
anything. F300 G10-13 passes the NECESSARY capacity condition: 96 fermionic modes/site = 66.542 nats
against 10.883 required, 6.11× room, horizon uses 16.4% of available capacity.

THE RESIDUAL: the surviving candidate is an ENTANGLEMENT entropy — continuous spectrum, no integrality
constraint, which is why the state-count reading failed. F190 is under-determined by counting, not
excluded by it; what's missing is the CONSTRAINT that selects 2π√3 specifically among the continuous
possibilities the capacity condition permits.

DO NOT RE-ATTACK: the state-count reading (CLOSED, exact no-go, F300 G10-12 — do not look for an
integer n with e^(2π√3)≈something clean, this route is dead). Do not re-verify the necessary capacity
condition (closed, passes at 6.11×).

REFERENCES — findings: F190 (original posit + its own named next step), F183 (lattice core to compute
against), F300 (§4's correlation-matrix machinery — this is the tool to use; §5, G10-12/13 the
no-go/necessary-condition results). Ledger: `open-derivations.md` row **G4** — read it, it names the
exact next step: "compute the boundary entanglement entropy against 2π√3 using F300 §4's correlation-
matrix machinery on the F183 lattice core." Also flags a DELIBERATELY UNCLAIMED coincidence worth
keeping in view but NOT assuming: the BCC reciprocal (fcc) conventional cube side is
4π/(2/√3)=2π√3 — numerically identical to the target, one a reciprocal length and one an entropy, no
derivation connects them (tagged `kind="coincidence"` in D7, meaning: do not silently promote this to
a derivation without actually finding the connection).

EXTERNAL: named anchors — Srednicki (1993) and Bombelli et al. on entanglement entropy of a region
boundary in free field theory (the standard "area law from entanglement" literature this row's
approach should be checked against). Search terms: "entanglement entropy horizon area law lattice
correlation matrix computation".

FIRST STEP: run F300 §4's correlation-matrix machinery on the F183 lattice core (already exists per
`open-derivations` G4's "next step #3") and compute the boundary entanglement entropy directly, then
compare to 2π√3 nats/cell.

WHAT PROMOTES THE GRADE: a computed entanglement entropy matching 2π√3 (closing this to QUANT/PARTIAL
with the entropy now a computed rather than posited object), or a clean mismatch (also valuable,
narrows the search).

WHAT WOULD FALSIFY THE ATTEMPT: a computed entropy far from 2π√3 within the 6.11× capacity margin
would suggest the constant itself needs re-examination, not just its origin.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *E10 — Singularity resolution — `PARTIAL` → next: a geodesic-completeness result

**Leverage:** low-medium. **Cost:** large, genuinely hard GR problem. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row E10 (singularity resolution), currently PARTIAL,
target: a geodesic-completeness result for the lattice-core interior.

WHAT IS ALREADY TRUE: Kretschmann scalar SATURATES at the cell scale ⇒ r_core ∝ M^(1/3), ~5e-22 m at
1 M☉, gate-tested (F183 §L1). Cosmologically, no substrate singularity exists; first resolvable epoch
is H_max=3^(-3/4) M_Pl at t_min=√3 ticks (F284 §5, both exact-algebraic).

THE RESIDUAL: r_core is a SATURATION ESTIMATE, not a proof of geodesic completeness. No result
currently shows that geodesics actually terminate smoothly (or extend indefinitely) through the
lattice core rather than merely that curvature invariants stay bounded.

DO NOT RE-ATTACK: the Kretschmann-saturation result itself (closed, gate-tested) or the cosmological
t_min result (closed, exact-algebraic).

REFERENCES — findings: F183 §L1, F284 §5.

EXTERNAL: named anchors — standard singularity-resolution literature in loop quantum gravity or
asymptotic safety (as comparison points for what a "geodesic completeness" result looks like in a
discretized-spacetime context). Search terms: "geodesic completeness discrete spacetime black hole
interior", "singularity resolution bounded curvature lattice model".

FIRST STEP: define precisely what "geodesic completeness" means on a discrete BCC lattice core (the
continuum notion needs adaptation) before attempting to prove or disprove it.

WHAT PROMOTES THE GRADE: an actual geodesic-completeness (or well-defined discrete analogue) result for
the lattice core.

WHAT WOULD FALSIFY THE ATTEMPT: finding genuine geodesic incompleteness even with bounded curvature —
would be an important, non-obvious result about this specific model.

PROTOCOL: this is research, likely hard. Claim your topic first. Take the next finding number. Close
with finding, test record, claim card. `make gate` before finish.
~~~

### *E11 — Interior / TOV / NS EoS — `QUANT` → next: extend to more EoS families, or tighten I/MR²

**Leverage:** low, already solid. **Cost:** small-medium. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row E11 (interior/TOV/neutron-star EoS), currently
QUANT, target: extend beyond the single SLy EoS already tested, or tighten the I/MR² measurement.

WHAT IS ALREADY TRUE: SLy EoS gives M_max=2.08 M☉, R(1.4)=11.1 km, consistent with PSR J0740 and
NICER (F181/F184); I/MR²≈0.31 with Lense-Thirring frame-dragging recovered (F185).

THE RESIDUAL: only one EoS family (SLy) has been tested against the F181 covariant kernel. Multiple
tabulated EoS families (APR, other modern nuclear-matter EoS) would strengthen this row's QUANT grade
and test robustness.

DO NOT RE-ATTACK: the F181 covariant two-function interior kernel itself (closed, this is a matter of
running more EoS inputs through existing machinery).

REFERENCES — findings: F181 (the kernel), F184 (SLy result), F185 (moment of inertia/frame dragging).

EXTERNAL: named anchors — APR, other current nuclear-matter EoS tables used in NS mass-radius
literature; current NICER/PSR mass-radius measurements for comparison. Search terms: "neutron star
equation of state APR tabulated mass radius current constraints".

FIRST STEP: run the existing F181 kernel machinery against 2-3 additional standard EoS tables and
compare mass-radius curves to current NICER data.

WHAT PROMOTES THE GRADE: broader EoS-family agreement strengthens QUANT toward a more robust QUANT (not
a new grade tier, but meaningfully less fragile).

WHAT WOULD FALSIFY THE ATTEMPT: a standard EoS that produces a mass-radius curve inconsistent with
current NS data on this model's kernel — worth reporting either way.

PROTOCOL: this is research, low-medium priority. Claim your topic first. Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### *E12 — Quantum-gravity sector — `PARTIAL` → next: develop gravity's own UV completion beyond "lattice is the cutoff"

**Leverage:** medium, foundational. **Cost:** large, open-ended. **Blocked by:** shares object with
A11/K9 (the same mode-sum machinery).

~~~text
Physics Notes research session. Target: rubric row E12 (quantum-gravity sector), currently PARTIAL,
target: develop what "gravity's own UV completion" means beyond the general "the lattice is the
cutoff" statement.

WHAT IS ALREADY TRUE: the graviton is exactly massless with 2 degrees of freedom; UV transversality
Π∝Q² plus IR block-spin irrelevance are established (F216, F248, F79).

THE RESIDUAL: per the baseline's own note, "A11's ledger now says exactly which coefficient that
costs" — i.e. this row's vagueness (gravity's UV completion beyond the generic lattice-cutoff
statement) is the SAME underlying object as A11's residual (the ρ_vac/K9 coefficient). This row may
not need independent work — check whether closing K9 also sharpens this row's grade.

DO NOT RE-ATTACK: the massless-graviton/2-dof result (closed, exact) or the general UV-transversality
result (closed).

REFERENCES — findings: F216, F248, F79. Cross-reference: A11 and K9 — read those prompts, this row's
residual may be the same coefficient.

EXTERNAL: search terms — "quantum gravity UV completion lattice cutoff graviton", "asymptotic safety
vs lattice regularization gravity".

FIRST STEP: after K9 closes (or makes progress), re-examine whether this row's "undeveloped" status is
actually just K9's residual restated, or whether there's independent content here (e.g. graviton
self-interactions at the cutoff scale, not just the vacuum-energy coefficient).

WHAT PROMOTES THE GRADE: either K9 closing (if this row is purely downstream), or independent content
on graviton self-interaction/scattering behavior at the cutoff if this row is genuinely separate.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, mostly a scoping question first.

PROTOCOL: this is research. Read the K9 prompt first to check overlap. Claim your topic. Take the next
finding number if independent content is found. Close with finding, test record, claim card.
`make gate` before finish.
~~~

### *E13 — Galactic-scale consistency — `EXCLUDED` → next: re-examine the ONE assumption behind the Bullet-Cluster falsification

**Leverage:** low — closed no-go, re-examination type. **Cost:** small, focused. **Blocked by:** n/a.

~~~text
Physics Notes research session. Target: rubric row E13 (galactic-scale consistency), currently
EXCLUDED (the model-native emergent-gravity/"dark matter without dark matter" route is falsified),
target: re-examine the reopening condition, not re-derive the excluded route.

WHAT IS ALREADY TRUE: the model-native emergent-gravity route (rotation curves without a dark source)
is FALSIFIED by the Bullet-Cluster lensing/gas offset (F194, using F191's rotation-curve analysis). A
dark SOURCE is required — this is a self-inflicted, honest result: the model's own machinery excludes
its own most economical option.

THE REOPENING CONDITION: the Bullet-Cluster lensing/gas offset measurement itself, and whether it
genuinely discriminates emergent-gravity from a dark-source picture as cleanly as F194 assumes — this
is the one assumption whose failure would reopen the row.

DO NOT RE-ATTACK: re-deriving rotation curves under emergent gravity as if the exclusion hadn't
happened — CLOSED, F194. State plainly: "the no-go survives" is success for a re-examination.

REFERENCES — findings: F194 (the falsification), F191 (rotation curves / Bullet Cluster analysis this
rests on). This connects to K7 (dark-matter identity) — the geon candidate there is the model's
adopted alternative, consistent with THIS row's exclusion.

EXTERNAL: named anchor — the original Bullet Cluster weak-lensing analysis (Clowe et al. 2006) and any
more recent reanalyses or alternative offset-cluster systems — check whether the discriminating power
F194 relies on still holds up. Search terms: "Bullet Cluster modified gravity dark matter
discrimination current status", "cluster lensing offset alternative gravity theories test".

FIRST STEP: check whether more recent (post-F194) literature has revisited the Bullet-Cluster
discrimination power between emergent/modified gravity and particle dark matter — if the empirical
picture has shifted, that is directly relevant to this row's reopening condition.

WHAT PROMOTES THE GRADE: n/a in the EXCLUDED→better sense; a re-examination reports whether the
falsification still holds against current data.

WHAT WOULD FALSIFY THE EXCLUSION: new analysis showing the Bullet-Cluster discrimination is weaker
than F194 assumed — would genuinely reopen this row and should be treated seriously, not dismissed.

PROTOCOL: re-examination research. Claim your topic first if pursuing. Take the next finding number
only if something changes. `make gate` before finish if code changes.
~~~

## K — Cosmology

### *K1 — FRW background — `QUANT` → next: derive (not just solve with) the source term

**Leverage:** medium. **Cost:** large — a genuinely different kind of result than currently exists.
**Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row K1 (FRW background), currently QUANT, target:
derive the expansion FROM the lattice rather than solving GR WITH the model's source (the stated
distinction the row itself draws).

WHAT IS ALREADY TRUE: full-tensor source reproduces ΛCDM: z_eq≈3430, z_acc≈0.63, age≈13.8 Gyr. F284
re-reads expansion as K's conformal mode on a RIGID substrate, buying dot-G/G≡0 exactly.

THE RESIDUAL: the row's own evidence column states it plainly — "solved WITH the model's source, not
derived FROM the lattice." This is a standard GR cosmology calculation using the model's stress-energy
content as input, not a demonstration that expansion itself emerges from lattice dynamics.

DO NOT RE-ATTACK: the dot-G/G≡0 result (closed exactly) or the standard-ΛCDM-reproduction numbers
(closed, these are solved correctly given the source).

REFERENCES — findings: F182, F188, F284 (the conformal-mode reading). Cross-reference K3/K12 for the
same "is it derived or read off" question applied to the primordial spectrum.

EXTERNAL: search terms — "emergent expanding spacetime lattice cellular automaton", "FRW metric
derivation from discrete substrate dynamics".

FIRST STEP: identify precisely what a "derived from the lattice" version of this row would need to
show beyond what F284 already provides — is F284's conformal-mode reading actually already most of
the way there, and the QUANT grade understates it? Or is there a genuine further step?

WHAT PROMOTES THE GRADE: a demonstration that FRW expansion is forced by the lattice's own dynamics
(not merely consistent with reading the model's stress-energy into standard GR).

WHAT WOULD FALSIFY THE ATTEMPT: n/a, exploratory/foundational.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *K2 — BBN / light elements — `PARTIAL` → next: repair the A=7 rates before saying anything about lithium

**Leverage:** medium — feeds Q4 and the model's own error-finding capability. **Cost:** small-medium,
per F297's own named next steps. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row K2 (BBN / light elements), currently PARTIAL,
target: repair the A=7 reaction rates and reduce the network's absolute offset.

WHAT IS ALREADY TRUE: expansion side entirely model-native, N_eff=3.044 FORCED (not fit). Y_p=0.2449
(-0.11σ), D/H=2.47e-5 (-1.8σ). g*(T) import CLOSED by F309 from the model's own 48 Weyl fields
(exactly branch-balanced), which produced a genuine byproduct constraint: m_Eg>125.5 MeV.

THE RESIDUAL: η_b (baryon-to-photon ratio) is free; the reaction network carries a MEASURED absolute
offset of -0.87% (Y_p) / +0.55% (D/H); ⁷Li is NOT validated (-92%) and is excluded from the battery.
V_ud, G_F, and the reaction network itself remain external inputs.

DO NOT RE-ATTACK: the g*(T) derivation (closed, F309) or N_eff=3.044 (forced, not a free result to
re-derive).

REFERENCES — findings: F297 (the BBN network and its named offsets), F309 (g* closure), F79, F178,
F182, F284 (expansion-side inputs). This row's Q4 sub-item (isospin splitting) has its OWN priority-4
prompt in block G below (G5/G7) — do not duplicate that work here.

EXTERNAL: named anchors — current BBN light-element abundance measurements (Y_p, D/H, ⁷Li) and their
tension status (the "lithium problem" is a known, decades-old SM tension too — useful context that
this model's ⁷Li failure may partly reflect a shared, unsolved nuclear-rate problem, not necessarily a
model-specific defect). Search terms: "primordial lithium problem BBN current status", "A=7 reaction
rate uncertainties big bang nucleosynthesis".

FIRST STEP: F297 §10 item 2-3, verbatim: repair the A=7 rates BEFORE saying anything about lithium
specifically, then attempt to reduce the -0.87%/+0.55% absolute network offset if any absolute
abundance claim is ever wanted. Also free per F297 §10.4: register dot-G/G≡0 as a stated PREDICTION
BBN confirms, not merely a bound met — cheap, and currently unclaimed.

WHAT PROMOTES THE GRADE: a repaired A=7 rate set, reduced network offset, or the dot-G/G prediction
registration (each independently moves this row's evidence forward).

WHAT WOULD FALSIFY THE ATTEMPT: a repaired A=7 rate set that still cannot validate ⁷Li — would point to
a genuine model-specific defect rather than a shared nuclear-physics uncertainty, worth distinguishing.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *K3 — CMB peaks, n_s — `PARTIAL` → next: compute the block-spin relevant eigenvalue with fluctuation corrections

**Leverage:** high — the SAME target as K12 (one anomalous dimension closes both rows). **Cost:**
medium, uses existing F130 machinery. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row K3 (CMB peaks, n_s), currently PARTIAL, target:
compute the one missing eigenvalue and close this to QUANT or PARTIAL-with-a-tighter-residual.

WHAT IS ALREADY TRUE: F310 (16/16, gate record armed with a control) established the model claims NO
3D holographic dual and needs none — the t=0 state of a rigid 3D automaton IS a measure on 3D field
configurations by construction, so F296 L5's r-exclusion is a dictionary artifact and does not
transfer. Running F285's own Poisson bridge through it gives n_s=3-2y and hence γ≡y-1 IDENTICALLY
(sympy literal zero) — so γ IS the anomalous part of the model's own block-spin relevant eigenvalue,
λ=b^(1+γ). This explains every prior failure in one line: an anomalous dimension is a NON-INTEGER RG
exponent, and all five exponents F130 measured are integers (F130's λ_n=b^-n is "a round-off-floor
identity" of a LINEAR block average — a Gaussian calculation, structurally unable to produce a
non-integer exponent).

THE RESIDUAL: one number, and its hypothesis. The model needs exactly one non-integer exponent,
γ=0.0136-0.0176 (1.4-1.8%), in a spectrum the repo ALREADY measures (just not yet with fluctuation
corrections). The standing hypothesis (F310 §11, its largest named residual): that the t=0 measure is
CRITICAL is INFERRED from the observed power law, not derived.

DO NOT RE-ATTACK: the measure itself (F285, closed) — do not hunt for a length scale (F286 T1, closed
negative) — do not pursue the 1/N holographic count (F310 C8 asserts explicitly this is not a
derivation and no model count lands in the required N≈63-81; this is a dead end, don't re-enter it).

REFERENCES — findings: F310 (16/16, the reduction — READ IN FULL), F295, F296, F285 (Poisson bridge),
F286 (T1, exact-algebraic, independently validated by retrodiction in F296). Ledger:
`open-derivations.md` row **G2** carries this exact target — read it, it states the next step
verbatim: "compute the block-spin relevant eigenvalue WITH FLUCTUATION CORRECTIONS on F130's existing
machinery, and see whether it moves off b^1 by 1.6%." Also flagged (unrelated to this row's core
target but worth fixing while in the code): five cosmology modules each hold a private Planck-2018
literal comparator — F310 carries a proper three-dataset table instead; register the others as
`MeasuredConstant`s (D7) while here.

EXTERNAL: current Planck 2018 / DESI n_s measurements and uncertainties (as the target this residual
needs to match). Search terms: "anomalous dimension block spin renormalization group fluctuation
correction", "critical exponent computation beyond mean field lattice".

FIRST STEP: exactly as open-derivations G2 states — take F130's existing block-spin machinery and add
fluctuation (beyond-linear) corrections to the relevant eigenvalue computation, checking whether it
moves off the integer b^1 by the required 1.4-1.8%.

WHAT PROMOTES THE GRADE: γ computed in the required range from fluctuation corrections — this closes
K3 AND K12 simultaneously (same operator).

WHAT WOULD FALSIFY THE ATTEMPT: a fluctuation-corrected eigenvalue that does NOT move toward the
required range — this is explicitly named as F310's own falsifier 1, and "a null result there kills
the route outright and is worth as much" per the ledger. Take a negative result seriously, not as a
failed session.

PROTOCOL: this is research, high priority (shared with K12). Claim your topic first (note it also
closes K12). Take the next finding number. Close with finding, test record, claim card. `make gate`
before finish.
~~~

### *K4 — Inflation or substitute — `EXCLUDED` → next: re-examine the cutoff-scale assumption

**Leverage:** low, closed no-go. **Cost:** small. **Blocked by:** n/a.

~~~text
Physics Notes research session. Target: rubric row K4 (inflation or substitute), currently EXCLUDED
(no slow-roll direction exists), target: re-examine the reopening condition.

WHAT IS ALREADY TRUE: a/ℓ_red=3^(1/4) EXACTLY ⇒ sub-Planckian cutoff; every compact CA direction
carries M_Pl²/f²≥√3 and every slow-roll parameter is O(10). K_clock=9 exactly. Starobinsky, N-flation,
and periodic-n_s escapes are ALL excluded with named margins (F282, 7/7).

THE REOPENING CONDITION: the exactness of a/ℓ_red=3^(1/4) itself, and the assumption of a COMPACT CA
direction as the only possible inflaton candidate space.

DO NOT RE-ATTACK: any of the three named escape routes (Starobinsky, N-flation, periodic-n_s) —
closed with margins, F282.

REFERENCES — findings: F282 (7/7, the exclusion), F283 (independently confirms via elastic-lattice
exclusion, CN8), F296, F238.

EXTERNAL: search terms — "slow roll inflation alternatives excluded models", "trans-Planckian problem
resolution without inflation".

FIRST STEP: verify a/ℓ_red=3^(1/4)'s exactness has not been touched by any finding since F282/F283
(check the changelog and findings-index for citations).

WHAT PROMOTES THE GRADE: n/a — re-examination; "the no-go survives" is success.

WHAT WOULD FALSIFY THE EXCLUSION: a new compact-direction candidate F282 didn't consider, or a
revision to the a/ℓ_red exactness.

PROTOCOL: re-examination research. Claim your topic first if pursuing. Take the next finding number
only if something changes.
~~~

### *K5 — Primordial spectrum normalisation — `EXCLUDED` → next: re-examine whether A_s could route through K3's eigenvalue work

**Leverage:** low. **Cost:** small. **Blocked by:** K3/K12 progress may inform this.

~~~text
Physics Notes research session. Target: rubric row K5 (primordial spectrum normalisation A_s),
currently EXCLUDED (no route, cause named: no inflaton + rigid substrate offers no generating process),
target: re-examine given any K3/K12 progress.

WHAT IS ALREADY TRUE: with no inflaton and a rigid substrate offering no generating process, P(k) is
an automaton INITIAL CONDITION. A_s=2.1e-9 has no route (F282, F284, F285, F238).

THE REOPENING CONDITION: whether the K3/K12 block-spin eigenvalue work (once it computes γ with
fluctuation corrections) incidentally produces any handle on the AMPLITUDE of the initial condition,
not just its tilt.

DO NOT RE-ATTACK: the "no generating process" exclusion itself (closed, multiple independent findings).

REFERENCES — findings: F282, F284, F285, F238. Cross-reference: K3's prompt above — its fluctuation-
correction work might (or might not) touch this row incidentally; check after K3 progresses, don't
duplicate effort now.

EXTERNAL: current Planck/DESI A_s measurement (target value only).

FIRST STEP: wait for or check K3's progress first; if K3's eigenvalue computation is running, ask
whether the same machinery says anything about amplitude, not just tilt.

WHAT PROMOTES THE GRADE: n/a directly — depends on K3.

WHAT WOULD FALSIFY THE ATTEMPT: n/a.

PROTOCOL: low priority, dependent on K3. Do not claim independently before checking K3's state.
~~~

### *K6 — Baryogenesis — `PARTIAL` → next: an actual Boltzmann computation for the asymmetry magnitude

**Leverage:** medium. **Cost:** large — a genuinely new computational capability. **Blocked by:**
nothing named.

~~~text
Physics Notes research session. Target: rubric row K6 (baryogenesis), currently PARTIAL, target: a
Boltzmann computation producing an actual asymmetry number, not just condition-satisfaction.

WHAT IS ALREADY TRUE: all three Sakharov conditions are MET by the model's own structure (F202, F47,
F53) — baryon-number violation, C/CP violation, and departure from equilibrium are all available in
principle.

THE RESIDUAL: this is NOT a Boltzmann (quantum-kinetic) computation — no asymmetry NUMBER exists.
Condition 1 (B-violation) is "met" only in the sense of being available, never actually rated for
magnitude.

DO NOT RE-ATTACK: re-verifying the three Sakharov conditions are met (closed, structural).

REFERENCES — findings: F202 (leptogenesis-adjacent work — check whether its Boltzmann machinery,
built for keV sterile production, could be repurposed here), F47, F53.

EXTERNAL: named anchors — standard leptogenesis/baryogenesis Boltzmann-equation frameworks; the
measured baryon asymmetry η_b (the target number). Search terms: "baryogenesis Boltzmann equation
computation asymmetry magnitude", "leptogenesis quantitative CP violation calculation".

FIRST STEP: check F202's existing quantum-kinetic (QKE) machinery — built for a different purpose
(sterile neutrino production) but possibly the right computational framework to adapt for an actual
baryon-asymmetry number here.

WHAT PROMOTES THE GRADE: an actual computed η_b, compared to the measured value.

WHAT WOULD FALSIFY THE ATTEMPT: a computed asymmetry far from measured — would need careful diagnosis
(order-of-magnitude physics questions, not a simple bug).

PROTOCOL: this is research, large scope. Claim your topic first. Take the next finding number. Close
with finding, test record, claim card. `make gate` before finish.
~~~

### *K7 — Dark-matter identity — `PARTIAL` → next: sharpen the geon candidate's own falsifiers

**Leverage:** medium. **Cost:** small-medium. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row K7 (dark-matter identity), currently PARTIAL,
target: sharpen the geon candidate toward a falsifiable, quantitatively distinct prediction.

WHAT IS ALREADY TRUE: the candidate is a graviton-graviton J=2 "geon," stable as a one-cell Planck-
mass black-hole remnant, cold and collisionless. Alternatives are excluded: native massive spin-2
(CN5), ν_R ν_R J=2 tensor channel (CN6), Alcubierre warp (F204), keV sterile as 100% of DM.

THE RESIDUAL: the candidate exists and survives its own alternatives being excluded, but this row
stays PARTIAL because — see K8 — the ABUNDANCE is a genuinely free input, not because the identity
itself is in doubt.

DO NOT RE-ATTACK: the excluded alternatives (all closed, CN5/CN6/F204/keV-sterile-100%).

REFERENCES — findings: F223, F228 (production/stability), F266, F216, F237. This row is tightly
coupled to K8 (abundance) — read that prompt too.

EXTERNAL: named anchors — current primordial-black-hole/compact-object dark matter constraint plots
(microlensing, CMB, dynamical) across the relevant mass range for a Planck-mass remnant. Search terms:
"primordial black hole dark matter constraints mass window current", "geon dark matter candidate
detection prospects".

FIRST STEP: place the geon's specific mass (μ≈√2 M_Pl per F223) against current PBH/compact-object
dark-matter exclusion plots to see whether this specific mass window is constrained, allowed, or
already excluded observationally — this is a literature-comparison task, not new derivation.

WHAT PROMOTES THE GRADE: a sharpened, quantitatively falsifiable prediction (e.g. a specific detection
channel or exclusion status) for the geon candidate.

WHAT WOULD FALSIFY THE CANDIDATE: if the geon's mass window is already observationally excluded as a
dark-matter candidate — report this plainly, it would be an important result.

PROTOCOL: this is research. Claim your topic first. Take the next finding number. Close with finding,
test record, claim card. `make gate` before finish.
~~~

### *K8 — Ω_DM h² = 0.12 — `EXCLUDED` → next: re-examine given any K7 geon-abundance progress

**Leverage:** low, closed no-go on the STANDARD route. **Cost:** small. **Blocked by:** n/a for
re-examination; the geon-abundance question (F238) is a related but separately-scoped target.

~~~text
Physics Notes research session. Target: rubric row K8 (Ω_DM h²=0.12), currently EXCLUDED (provable
non-derivability given no inflaton), target: re-examine the reopening condition.

WHAT IS ALREADY TRUE: the structural ABSENCE of an inflaton is a structural EXCLUSION for deriving
this abundance via the usual (freeze-out/misalignment-type) routes; β is in the initial-state
category, and F285 quantifies the mirror constraint (F238, F282-F285).

THE REOPENING CONDITION: whether the geon candidate's OWN abundance-production mechanism (a
production-and-stability question, not an inflaton-relic-abundance question) could sidestep this
exclusion entirely — this is F238's OWN finding, already flagged as "the geon relic abundance is a
genuinely free input, and here is exactly why," so check whether that "why" is itself the reopening
condition or a separate, permanent obstruction.

DO NOT RE-ATTACK: deriving Ω_DM via a standard inflaton-relic mechanism — structurally excluded, this
model has no inflaton (K4/K5).

REFERENCES — findings: F238 (both the exclusion AND the geon-abundance discussion — read in full, it
may already answer this row's reopening question), F282-F285.

EXTERNAL: search terms — "primordial black hole abundance production mechanism without inflation".

FIRST STEP: read F238 closely for whether it already forecloses a geon-production route to the
abundance, or whether that remains genuinely open (distinct from the inflaton-relic exclusion this row
specifically grades).

WHAT PROMOTES THE GRADE: n/a for the inflaton-relic route (permanently excluded); a geon-production
abundance calculation would be a DIFFERENT achievement, tracked separately if pursued.

WHAT WOULD FALSIFY THE EXCLUSION: n/a for the specific inflaton-relic mechanism graded here.

PROTOCOL: re-examination + scoping research. Claim your topic first if pursuing the geon-production
angle specifically (coordinate with K7).
~~~

### *K9 — Λ magnitude — `OPEN` → next: dynamical enforcement of the F183/F190 capacity ceiling (priority #2)

**Leverage:** very high — closes A11, K9, K10 (conditionally), and ledger #28 simultaneously.
**Cost:** medium — a derivation, not a new sector; the price is already met, only dynamics missing.
**Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row K9 (cosmological-constant magnitude), currently
OPEN, target PARTIAL (show the F164 zero-point sum is dynamically made to respect the F183/F190
capacity bound, or show that it is not).

WHAT IS ALREADY TRUE (adjudicated 2026-08-18, Amendment 4 to completeness-2026-08-18 — READ THAT
AMENDMENT IN FULL FIRST, it is the authoritative current state and this summary compresses it): the
"two unreconciled pictures" framing is DEAD. F311 C1 (chronology) stands exact: F192 V3 at 04:50,
F193 at 17:35 the SAME DAY — 12.75 hours later, and F193 closes candidate (i) F192 called open. F196
then derived the p=2 exponent F193 named as its own obstruction. F193 PART A is EXCLUDED (inside
CL275): its "no additive c-number per mode" step is UNIFORM (F59 Part C builds 1/16πG out of the same
½), so deleting the c-number takes F79's G down with it — it cannot be quoted as zeroing ρ_vac without
also zeroing G. F311 leg C3 is WITHDRAWN: "the modes make 1/G so they can't also be a source" proves
too much — a_0 and a_1 are different heat-kernel coefficients of ONE expansion, not one thing counted
twice; on C3's own rule, Sakharov induced gravity could never induce a CC at all (this is F311's OWN
falsifier 5, hit by F319 U8). F319 §6's "channel (ii) is the sole survivor" is NARROWED: it enumerates
only F164 §C's three channels and never sees F193 §B/F196/F241, whose capacity ceiling
ρ≤3c⁴/8πGL² CONTAINS G rather than perturbing it, and delivers 120.66 of the required 120.76 decades
with a_1 UNTOUCHED — short only 0.10 dex = Ω_Λ.

THE RESIDUAL, restated precisely: THE PRICE IS MET (120.66 of 120.76 decades, zero free parameters,
a_1/G untouched); DYNAMICS IS WHAT'S MISSING. Two candidate routes of the right shape, neither closed:
(a) F164 channel (ii), AB≡1 sequestering — order-selective by construction, but NO NUMBER; (b) F193
§B/F196/F241's capacity ceiling — the number, to 0.10 dex, but NO DYNAMICS (a ceiling is a consistency
requirement, not a suppression mechanism, per F241/CL212).

DO NOT RE-ATTACK: F196's p=2 exponent derivation (closed). Do not re-open F192 V2 as a rival picture —
C1's chronology is exact and settles that the "two pictures" framing is dead, permanently, not
provisionally. Do not quote F311's original headline ("K9 collapses to one O(1) coincidence") — it is
WITHDRAWN along with leg C3, citing it uncorrected is now an error, not just outdated.

REFERENCES — findings: F164 (original ~10^121 overshoot), F192 (superseded framing, cite only with the
chronology context), F193 (Part A excluded, Part B the surviving mechanism), F196 (p=2 derivation),
F241 (CL212 — proves the sector fixes a CEILING not a value, this distinction is the crux), F311
(leg C3 withdrawn, C1/C2 stand), F319 (U8 — the pricing mechanism, §6 narrowed). Ledger:
`open-derivations.md` row **G1** — READ IN FULL, it is the single most precise statement of this
row's exact current state and carries the full adjudication reasoning this prompt has compressed.
Also affects: rubric **A11** (same residual number) and ledger **#28** (Λ, same row) — closing this
closes all three at once; also **K10** (dark-energy w) has a conditional dependency, see that row's
note in the main report (do NOT absorb K10's "vacuous sign" reading yet per Amendment 4 — the ceiling
route caps near ρ_crit rather than zeroing, a regime where w=p/ρ is not 0/0).

EXTERNAL: named anchors — standard cosmological constant problem literature (Weinberg's classic review
remains the standard reference for the scale of the problem this model is closing 120.66 of 120.76
decades of). Search terms: "cosmological constant problem dynamical suppression mechanism", "induced
gravity vacuum energy cancellation dynamics".

FIRST STEP: attempt to show the F164 zero-point sum is DYNAMICALLY driven to respect the F183/F190
capacity ceiling — i.e., find the actual mechanism (not just the consistency bound) that would
enforce ρ_grav(L)≤3c⁴/8πGL² as a dynamical outcome rather than a structural upper limit the theory
happens to satisfy.

WHAT PROMOTES THE GRADE: OPEN → PARTIAL requires a genuine dynamical mechanism (even incomplete) that
does more than restate the ceiling as a consistency check — the ceiling's mere existence is already
known and is NOT sufficient for promotion.

WHAT WOULD FALSIFY THE ATTEMPT: per F319's own framing, any survivor needs order-selectivity between
two ADJACENT heat-kernel coefficients (a_0, a_1) of at least 1.27e116 — a proposed mechanism that
cannot achieve this order of selectivity does not close the row, however plausible it looks locally.

PROTOCOL: this is research, and the highest-value cosmology target in the tree (priority #2 overall).
Claim your topic in docs/design/session-claims.yaml before any physics, noting it also affects A11 and
ledger #28. Take the next finding number from `casim index`. Close with the finding, its test record,
and its claim card, and update `open-derivations.md` row G1's status. `make gate` before finish.
~~~

### *K10 — Dark energy w, vs DESI — `PARTIAL` → next: wait for K9, do not pre-absorb C2's reading

**Leverage:** medium, conditional on K9. **Cost:** n/a directly. **Blocked by:** K9.

~~~text
Physics Notes research session. Target: rubric row K10 (dark energy w vs DESI), currently PARTIAL,
target: track K9's resolution before this row's residual can honestly move.

WHAT IS ALREADY TRUE: vacuum w=-1 gives ρ+3p=-2ρ, so it accelerates — sign correct and exact (F192).
F203 flags w=-1 vs DESI DR2 as one of three live falsifiers under pressure.

THE RESIDUAL: F311 C2 originally suggested this row's "vacuous sign" reading could absorb once K9
settles — but Amendment 4 (2026-08-18) explicitly says DO NOT absorb it yet: C2 stands as an
implication but is CONDITIONAL on a survivor that actually zeroes the gravitating constant. F193 Part
A (which supplied ρ_vac=0 outright) is EXCLUDED; the surviving ceiling route (F193 §B/F196) caps the
gravitating density NEAR ρ_crit rather than at zero — a regime where w=p/ρ is genuinely 0/0-adjacent
but not the same as the vacuous reading C2 originally proposed.

DO NOT RE-ATTACK: absorbing C2's vacuous-sign reading into this row before K9 resolves its dynamics
question — Amendment 4 explicitly forbids this, do not pre-empt it.

REFERENCES — findings: F192, F203, F311 (C2, conditional), and — the actual gate — K9's resolution
(see K9 prompt above).

EXTERNAL: current DESI DR2 dark-energy equation-of-state constraints — search "DESI DR2 dark energy
equation of state w constraint current".

FIRST STEP: check K9's status; this row's residual only changes shape once K9's dynamics question
closes or substantially progresses.

WHAT PROMOTES THE GRADE: K9 progress (see that prompt) — not independent work here.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, dependent row.

PROTOCOL: work K9 instead; revisit this row explicitly once K9 moves.
~~~

### *K11 — Structure formation / σ8 — `PARTIAL` → next: replace the imported EH98 transfer function

**Leverage:** medium. **Cost:** large — needs new Boltzmann-hierarchy machinery the tree doesn't have
yet. **Blocked by:** nothing named, but a real piece of new work.

~~~text
Physics Notes research session. Target: rubric row K11 (structure formation / σ8), currently PARTIAL,
target: replace the imported EH98 no-wiggle transfer function with one derived from the model's own
radiation-era physics.

WHAT IS ALREADY TRUE: the model carries ZERO free functions where the EFT of dark energy carries TWO —
from three independent sources: μ=1 with ∂_k μ≡0, dot-G/G≡0, and zero linear slip from AB≡1. γ_g=6/11
and the Meszáros growth function D(y)=1+3y/2 are sympy literal zeros. fσ8 against 7 RSD data points
gives χ²/N=1.012. σ8=0.8204 is REPORTED WITH ITS BUDGET, not claimed as a clean prediction. The
falsifier is LIVE and can fire: no screening mechanism exists, so the DES Y6 low-S8 tension (3.00σ)
CANNOT be accommodated if it persists.

THE RESIDUAL: σ8's ≈1% residual IS the EH98 (Eisenstein-Hu 1998) no-wiggle fit — an IMPORTED transfer
function, not a model-native one. Replacing it needs the model's own radiation-era Boltzmann hierarchy
(photon-baryon and neutrino perturbation equations), which the model does NOT yet carry — this is
explicitly named as "a real piece of work, not a tightening."

DO NOT RE-ATTACK: the zero-free-function structure result (closed, three independent sources, exact).

REFERENCES — findings: F288 (13/13, the current result and its residual). Cross-reference K2 (shares
the "imported machinery" pattern — this row and K2 are both flagged in `open-derivations` row **S2**,
"three named imports, each priced" — read S2 in full for the shared framing).

EXTERNAL: named anchors — Eisenstein & Hu (1998) no-wiggle transfer function (the thing being
replaced); current DES Y6 S8 tension status and any resolution since. Search terms: "photon baryon
Boltzmann hierarchy transfer function derivation", "DES Y6 S8 tension current status 2026".

FIRST STEP: scope what a minimal photon-baryon-neutrino Boltzmann hierarchy would require on top of
the model's existing radiation-era machinery (F79, F178, F182, F284) — this is a genuinely new
capability, so an honest feasibility scoping is the right first output, not a rushed partial
implementation.

WHAT PROMOTES THE GRADE: a model-native transfer function replacing EH98, even partially, with the
residual re-measured against it.

WHAT WOULD FALSIFY THE ATTEMPT: if the DES Y6 3.00σ tension is confirmed and grows with better data —
per the row's own falsifier, this genuinely threatens the model since no screening mechanism exists to
absorb it; report this honestly rather than downplaying it.

PROTOCOL: this is research, large scope. Claim your topic first. Take the next finding number. Close
with finding, test record, claim card. `make gate` before finish.
~~~

### K12 — Cosmological initial conditions — `PARTIAL` → carried, see K3

*Same target as rubric row K3 (the block-spin anomalous eigenvalue) — see that prompt above. No
separate work needed; K3 and K12 close together.*

## G — Emergent and precision physics

### *G2 — Hydrogen, fine structure, Lamb shift — `QUANT` → next: close the last 0.5% of the Lamb shift

**Leverage:** low, already tight. **Cost:** small — two-loop QED, well-trodden territory.
**Blocked by:** nothing, declared out of scope by choice.

~~~text
Physics Notes research session. Target: rubric row G2 (hydrogen/fine structure/Lamb shift), currently
QUANT, target: close the declared-out-of-scope two-loop α(Zα)^5 piece if worth the effort.

WHAT IS ALREADY TRUE: -13.596 eV from m_e+α alone; Rydberg to 1.1e-12 of CODATA; 2p splitting 10.95
GHz; Bethe log computed from the model's OWN spectrum with no literature constant (F125, F252, F257,
F262).

THE RESIDUAL: Lamb shift at 99.5% of measured — the missing 0.5% is the two-loop α(Zα)^5 QED
correction, DECLARED out of scope (not a gap the model claims to close).

DO NOT RE-ATTACK: the Bethe-log-from-own-spectrum result (closed, no literature constant used) or the
Rydberg/fine-structure results (closed to 1.1e-12).

REFERENCES — findings: F125, F252, F257, F262.

EXTERNAL: standard two-loop Lamb shift QED literature (well established) — search "two-loop Lamb
shift alpha Z alpha^5 correction hydrogen".

FIRST STEP: this is largely a standard QED calculation applied to the model's own field content —
check whether F252's existing two-loop machinery (used elsewhere, e.g. G3's electron g-2) can be
adapted directly.

WHAT PROMOTES THE GRADE: closing the 0.5% with a derived (not imported) two-loop term.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, low priority refinement.

PROTOCOL: low priority. Claim your topic first if pursuing. Take the next finding number. `make gate`
before finish.
~~~

### G3 — g−2, electron and muon — `PARTIAL` → carried, see B9

*Shares its residual (the hadronic VP/HLbL piece, and the two-loop leptonic bubble) with rubric row B9
— see that prompt above. No separate work needed; note this row's own specific numbers below for
context if picking up the shared target.*

Context specific to G3: a_e=α/2π EXACT; two-loop A2=-0.328478965; A2(μ)=0.765857 vs measured
0.765857410 (F252, F261). Hadronic VP, HLbL, and EW pieces are NOT claimed, by declared scope. F322
shows B9's electroweak precision is a factor 2.02 worse on the model's own α — the missing 3.795 in
α⁻¹ is exactly the hadronic piece this row also does not derive. See B9's prompt for the primary
attack (the two-loop leptonic bubble); the hadronic VP/HLbL question is a SEPARATE, larger piece of
work not covered by that prompt — if pursuing hadronic VP specifically, treat it as its own session
and consult current data-driven hadronic VP compilations (KNT, DHMZ) as the target.

### *G4 — Atomic structure / periodic table — `QUANT` → next: extend past light elements

**Leverage:** low-medium. **Cost:** medium, extending existing machinery. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row G4 (atomic structure/periodic table), currently
QUANT, target: extend the relativistic SCF machinery past light elements (H/He/Li/C currently
certified).

WHAT IS ALREADY TRUE: H, He, Li, C certified stable (net charge ≤2.2e-16, Pauli exclusion via live
Gram-Schmidt orthogonalization); He ionization potential 24.0 eV; relativistic SCF (F125's Dirac-
Coulomb machinery) with an accuracy map already built (F148, F195, F208).

THE RESIDUAL: only light elements are covered. Extending to medium/heavy elements (where relativistic
and correlation effects grow) is a natural next step using existing machinery.

DO NOT RE-ATTACK: the light-element results themselves (closed, certified).

REFERENCES — findings: F148 (modular element assembler), F195 (block-spin element atom), F208
(relativistic SCF ionization energies + accuracy map).

EXTERNAL: standard atomic ionization energy tables (NIST) for comparison across more of the periodic
table. Search terms: "relativistic self-consistent field heavier elements accuracy", "Dirac-Coulomb
SCF periodic table validation".

FIRST STEP: run the existing F148/F195/F208 machinery on a handful of medium-Z elements (e.g. Na, Al,
Fe) and compare ionization energies to NIST.

WHAT PROMOTES THE GRADE: extended, validated coverage past light elements, with an honest accuracy map
showing where the method starts to degrade (if it does).

WHAT WOULD FALSIFY THE ATTEMPT: significant divergence from measured values at moderate Z — worth
reporting as a scope boundary rather than hidden.

PROTOCOL: this is research, moderate priority. Claim your topic first. Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### *G5 — Hadron spectrum — `QUANT` → next: fix the isospin splitting (Q4, priority #4)

**Leverage:** high — shared with G7, the model's own BBN found this error. **Cost:** small — one
term, one session, per F297's own diagnosis. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row G5 (hadron spectrum), currently QUANT, target:
fix the isospin splitting m_n-m_p, currently excluded at 36.6σ by the model's OWN BBN.

WHAT IS ALREADY TRUE: nucleon mass 3m_c=928.5 MeV vs measured 938.27 MeV (-1.05%) on ONE anchor
(f_π); meson sector agrees to a few percent. The +12% residual on √σ/f_π is d1's fork (see B8's
prompt — do not duplicate).

THE RESIDUAL, and it is the cheapest live target in the whole tree: F297's own BBN measures m_n-m_p to
±0.0056 MeV — 179× MORE SHARPLY than F122's own original acceptance check (±1 MeV) — giving
Δm=1.293±0.0056 MeV from ∂Y_p/∂Δm=-0.607 MeV⁻¹. The model's current value, +1.51 MeV, is EXCLUDED at
36.6σ in helium abundance, and by a factor 2.7 in the neutron lifetime (331 s computed against measured
878.4±0.4 s). F122's SIGN claim (n heavier than p) SURVIVES; its VALUE does not. One of two terms
(strong +2.51 MeV or EM -1.00 MeV) is wrong by 0.217 MeV.

DO NOT RE-ATTACK: F122's sign result (survives, do not re-derive from scratch) or the overall nucleon-
mass-from-one-anchor result (closed, -1.05%, separate from this specific splitting).

REFERENCES — findings: F122 (original splitting calculation — the strong +2.51/EM -1.00 MeV terms
live here), F123 (nucleon mass anchor), F297 (the BBN measurement that found the error, §10 item 1 is
the exact instruction), F309 (confirms g* is orthogonal, doesn't help or hurt this). Ledger:
`open-derivations.md` row **Q4** — read it, it is the authoritative statement of this exact target and
has been unmoved for at least two prior reports before this one, now a third.

EXTERNAL: current PDG neutron-proton mass difference and its accepted strong/EM decomposition (for
comparison, not as the target — the target is fixing the MODEL's own internal term). Search terms:
"neutron proton mass splitting electromagnetic self energy lattice QCD calculation", "isospin breaking
quark mass difference nucleon".

FIRST STEP: F297 §10 item 1, verbatim: fix the EM self-energy term in F122, OR show the F40 d-u quark-
mass-ratio gap moves to compensate — check both, since either resolves the discrepancy.

WHAT PROMOTES THE GRADE: a corrected splitting consistent with the model's own ±0.0056 MeV BBN-derived
band, closing G5's splitting sub-issue and G7's neutron-lifetime problem simultaneously.

WHAT WOULD FALSIFY THE ATTEMPT: a correction that fixes the BBN tension but breaks some OTHER
already-passing result (e.g. the meson spectrum or F40's d-u ratio elsewhere) — check for exactly this
kind of collateral damage before declaring success.

PROTOCOL: this is research, and per this report's priority #4, one of the cheapest high-value targets
available. Claim your topic first (note it also affects G7). Take the next finding number. Close with
finding, test record, claim card. `make gate` before finish.
~~~

### *G6 — Nuclear binding — `QUANT` → next: reduce the one tuned core parameter

**Leverage:** low-medium. **Cost:** medium. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row G6 (nuclear binding), currently QUANT, target:
derive or eliminate the one remaining tuned parameter (b=0.55 fm).

WHAT IS ALREADY TRUE: deuteron binding energy 2.224 vs 2.22457 MeV measured (0.026% — genuinely tight),
r_d to 0.4%, on a FULLY DERIVED one-boson-exchange potential with NO tuned hard core (F104, F113,
F126, F128, F240, F206).

THE RESIDUAL: one parameter, b=0.55 fm (likely a regularization/cutoff scale in the OBE potential), is
still tuned rather than derived.

DO NOT RE-ATTACK: the OBE potential's derivation itself (closed — π, σ, ω exchanges all derived
elsewhere in the tree) or the 0.026% binding-energy result.

REFERENCES — findings: F104, F113 (repulsive core), F126 (σ attraction), F128 (ω repulsion), F240 (ω
coupling + full OBE deuteron), F206 (Tier-B internucleon binding).

EXTERNAL: search terms — "one boson exchange potential cutoff scale derivation", "nuclear force
regularization parameter lattice QCD".

FIRST STEP: identify what b=0.55 fm physically represents in the current OBE construction (a form-
factor cutoff? a hard-core regularization?) and check whether any already-derived model scale (e.g.
the confinement scale, F86/F299) could supply it directly.

WHAT PROMOTES THE GRADE: b derived from an existing model scale rather than fit.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, refinement-class work.

PROTOCOL: this is research, moderate priority. Claim your topic first. Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### G7 — Weak decays — `PARTIAL` → carried, see G5 (Q4)

*Shares its residual (the m_n-m_p isospin splitting, causing the 2.7× wrong neutron lifetime) with
rubric row G5 — see that prompt above. No separate work needed; the τ_n=331s vs measured 878.4±0.4s
discrepancy is the SAME defect as G5's, and closes when Q4 closes. Separately unaffected by this:
d→u+W⁻→u+e⁻+ν̄ structure is exact end-to-end (F54, 10/10); G_F inherits the v anchor (see ledger #17's
prompt for that separate, unrelated residual).*

### *G9 — Condensed-matter emergents — `QUANT` → next: reduce the Allen-Dynes 6.3% residual

**Leverage:** low, isolated, already strong. **Cost:** small-medium. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row G9 (condensed-matter emergents), currently QUANT,
target: reduce the Allen-Dynes T_c error below 6.3%.

WHAT IS ALREADY TRUE: 2Δ/kT_c → 2π/e^γ and ΔC/C_n=12/7ζ(3) at MACHINE precision. μ* (Morel-Anderson)
is DERIVED from the F64 dielectric with NO fit, cutting the Allen-Dynes T_c error from 14.3% to 6.3%
(F210-F215, F218, F242, F207, F171). Casimir effect exact.

THE RESIDUAL: 6.3% remaining Allen-Dynes error — likely higher-order Eliashberg corrections beyond
what's currently implemented (F215's imaginary-axis solver exists — check whether it's fully
exploited here).

DO NOT RE-ATTACK: the μ*-from-F64-dielectric derivation itself (closed, no fit) or the machine-
precision BCS-ratio results.

REFERENCES — findings: F210-F215 (superconductivity sector), F218 (algorithm-through-the-engine,
possibly unrelated — check relevance before citing), F242 (μ* derivation), F207 (Casimir), F171
(slow-light, likely unrelated — check before citing), F215 (Eliashberg solver — the likely next tool).

EXTERNAL: current real-superconductor T_c measurements used for comparison (already the target — check
which materials/couplings are being tested). Search terms: "Eliashberg theory strong coupling
corrections Allen-Dynes formula accuracy".

FIRST STEP: check whether F215's Eliashberg solver is already being used for the T_c comparison, or
whether the 6.3% residual comes from a simpler (Allen-Dynes formula) approximation that the solver
could improve on directly.

WHAT PROMOTES THE GRADE: T_c error reduced below 6.3% using more of the existing Eliashberg machinery.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, refinement.

PROTOCOL: this is research, low-medium priority. Claim your topic first. Take the next finding number.
Close with finding, test record, claim card. `make gate` before finish.
~~~

### *G10 — Statistical mechanics / thermodynamics — `PARTIAL` → next: extend past equilibrium to an interacting sector

**Leverage:** medium. **Cost:** large. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row G10 (statistical mechanics/thermodynamics),
currently PARTIAL, target: extend past equilibrium-only, photon-and-fermion-only coverage to an
interacting sector.

WHAT IS ALREADY TRUE: w=1/3 and Stefan-Boltzmann are THEOREMS (not fits) in the IR of the derived
dispersion, with closed-form lattice corrections ∝Θ² and the parameter-free ratio C_u/C_w=15/2 — F309
UPGRADED this from a measured photon coincidence to a degree-3 HOMOGENEITY THEOREM by showing it
survives fermions AND the branch-odd deletion (the branch-odd term b is linear in |k|, so its square
is degree-3 homogeneous, supplying 3/7=42.86% of the coefficient for fermions specifically — it does
NOT cancel there the way it does for the paired photon). Fine-grained entropy conserved (1.1e-12) on
a MIXED state; coarse-grained entropy rises but TIME-SYMMETRICALLY, so the arrow of time is the
initial condition, not a dynamical asymmetry. The free sector CANNOT thermalise (2N conserved n±(k)
fix a GGE, not a Gibbs state).

THE RESIDUAL: equilibrium only; only the photon and fermion sectors are covered; NO interacting sector
has been attempted at all.

DO NOT RE-ATTACK: the w=1/3/Stefan-Boltzmann theorems (closed, exact) or the GGE/non-thermalization
result for the FREE sector (closed, this row's gap is specifically about adding interactions).

REFERENCES — findings: F300 (entropy conservation, GGE), F309 (the C_u/C_w homogeneity theorem
upgrade).

EXTERNAL: search terms — "thermalization interacting lattice fermion system eigenstate
thermalization hypothesis", "generalized Gibbs ensemble breakdown with interactions".

FIRST STEP: identify the smallest interacting extension of the existing free-sector machinery (e.g.
turning on a weak coupling between modes) and check whether the GGE breaks down toward genuine
thermalization, as expected physically when integrability is broken.

WHAT PROMOTES THE GRADE: a measured interacting-sector result — either thermalization onset (expected)
or, if the GGE persists even with interactions, a genuinely surprising and important finding.

WHAT WOULD FALSIFY THE ATTEMPT: n/a, exploratory — either outcome is informative.

PROTOCOL: this is research, large scope. Claim your topic first. Take the next finding number. Close
with finding, test record, claim card. `make gate` before finish.
~~~

## H — Model integrity

### *H1 — Parameter count vs SM's 19+ — `PARTIAL` → carried, see the D-ledger prompts collectively

*This row's grade tracks the D-ledger's aggregate state, not any single derivation. It improves as
D#1-6, #10-13, #14, #17, #18, #22, #26, #28 individually close — see those prompts. No independent
work is needed for H1 itself beyond periodically re-tallying.*

~~~text
Physics Notes research session. Target: rubric row H1 (parameter count vs the SM's 19+), currently
PARTIAL, target: track ledger closures and correct the "chain vs count" framing if it drifts.

WHAT IS ALREADY TRUE: 6 parameters derived with zero free parameters, 3 proven permanently free
(PMNS — itself a result), 14 unaddressed. The model is explicitly NOT claiming to be "cheaper than
the SM in raw count" — the claim actually made is that the SECTORS it has built carry zero free
parameters. Three of the six derived sit downstream of either the v anchor or (formerly) X1's
unchosen branch (now closed), so the CHAIN is not as parameter-free as the raw COUNT suggests.

THE RESIDUAL: this is an accounting/framing row, not a derivation target. Its job is to stay honest as
the ledger below it moves.

DO NOT RE-ATTACK: individual ledger parameters here — work them via their own dedicated prompts (D
block above) and let this row's tally update as a consequence.

REFERENCES — the full D-ledger table in `completeness-2026-08-20.md`.

EXTERNAL: n/a.

FIRST STEP: after any ledger row closes, re-tally H1's own "6 derived / 3 free / 14 open" breakdown
and check the "chain vs count" caveat still holds (i.e., verify newly-derived quantities aren't
secretly downstream of an anchor in a way the tally doesn't disclose).

WHAT PROMOTES THE GRADE: ledger progress, faithfully re-tallied.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this is a bookkeeping row.

PROTOCOL: no finding needed for this row specifically; update it as part of any ledger-closing
finding's own accounting, and flag explicitly in that finding if the tally moves.
~~~

### *H2 — Falsifiability — `PARTIAL` → next: retrofit even five of the 48 no-control gate assertions (priority #5)

**Leverage:** medium, breaks a 12-day-unmoved ratchet. **Cost:** small per item. **Blocked by:**
nothing — this is pure backlog work.

~~~text
Physics Notes research session. Target: rubric row H2 (falsifiability, instrument half), currently
PARTIAL, target: retrofit controls onto gate-tier assertions currently lacking them.

WHAT IS ALREADY TRUE: the register half (claims/falsifiers) is strong and unchanged. The instrument
half keeps GROWING in absolute terms: gate-tier assertions went 78→82 (two days), declared controls
76→91 (+15), all attached to findings written since 2026-08-18.

THE RESIDUAL: `check_control_soundness.py` reports exactly **48 NO CONTROL** gate-tier assertions —
identical to every measurement back to 2026-08-08, now UNMOVED FOR 12 DAYS. New work ships with its
own controls; the pre-existing backlog is not shrinking because nobody has gone back to retrofit it.

DO NOT RE-ATTACK: any already-controlled assertion — this is specifically about the 48 that have none.

REFERENCES — run `python3 tools/check_control_soundness.py --run` (or `make control`) from the
repository root to get the CURRENT list of the 48 (or however many remain) by name — this prompt
cannot enumerate them without that live run, and the list may have shifted slightly since 2026-08-20.

EXTERNAL: n/a — internal engineering task.

FIRST STEP: run `make control` to get the current NO-CONTROL list, pick the five with the SIMPLEST
physics (to minimize the risk of introducing a wrong control), and for each: identify a parameter
whose deliberate mis-setting should make the assertion fail, add a `control:` block declaring it, and
verify with `casim test --control` that it reddens exactly the declared legs and nothing else.

WHAT PROMOTES THE GRADE: even five retrofitted controls measurably move the 48 for the first time in
12 days — worth doing even partially rather than waiting for a full retrofit session.

WHAT WOULD FALSIFY THE ATTEMPT: a control that does NOT reproduce the "reddens exactly the declared
legs" property — fix the control's parameter choice, not the assertion.

PROTOCOL: this is engineering/verification work, not physics research — no new finding needed unless
retrofitting a control reveals the underlying assertion was actually WRONG (in which case, that is a
finding). Otherwise: just the control blocks and a changelog entry. `make control` and `make gate`
before finishing.
~~~

### *H3 — Out-of-sample survival — `QUANT` → next: find or create a second clean instance

**Leverage:** low-medium, strengthens an already-good story. **Cost:** unclear, mostly opportunistic
(watch for it rather than force it). **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row H3 (out-of-sample survival), currently QUANT,
target: identify a second clean instance alongside m_Z/m_W=3/√7.

WHAT IS ALREADY TRUE: one clean instance exists — m_Z/m_W=3/√7 was FIXED BEFORE PDG 2025 excluded the
CDF-II m_W measurement; against the now-standard m_W=80.3692±0.0133, it gives -0.064%. This is
genuinely valuable: a prediction made before the relevant data update, not fit to it after. F320's
absolute masses are explicitly NOT a second instance — they are a new prediction, not a survived
revision (i.e., they weren't tested against data that arrived after they were derived).

THE RESIDUAL: only one instance exists. A second would substantially strengthen this row's evidentiary
value (one clean out-of-sample survival could be luck; two starts to look structural).

DO NOT RE-ATTACK: re-deriving or re-verifying the m_Z/m_W result — closed, and re-litigating it does
not create a second instance.

REFERENCES — findings: the claims registry (Claims rev 5) is the source for this row.

EXTERNAL: watch for FUTURE data revisions (PDG updates, new measurements) against any of the model's
OTHER already-fixed predictions — this is fundamentally a waiting/monitoring task, not something to
force in one session. Search terms: "PDG particle data group latest update changes" (periodically,
not once) to check whether any prediction this model made BEFORE a revision now reads as surviving one.

FIRST STEP: catalogue the model's other precisely-stated numerical predictions (from the claims
registry, headline cards) with their DATES, so that future data revisions can be checked against them
systematically rather than discovered by accident (as m_Z/m_W's survival apparently was).

WHAT PROMOTES THE GRADE: a documented second clean instance, whenever one arises.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this is inherently opportunistic, not forceable in one session.

PROTOCOL: build the prediction-date catalogue now (small, useful); treat finding an actual second
instance as an ongoing watch rather than a single session's deliverable.
~~~

### *H4 — Retraction hygiene — `PARTIAL` → next: fix `papers/README.md`'s stale numbers

**Leverage:** low-medium, a known, named, easy fix. **Cost:** small. **Blocked by:** nothing.

~~~text
Physics Notes research session. Target: rubric row H4 (retraction hygiene), currently PARTIAL, target:
fix the one remaining named stale surface, `papers/README.md`.

WHAT IS ALREADY TRUE: both instances named at the 2026-08-18 baseline are FIXED (Amendment 3): the
m_W/m_Z Scope entry moved to core claim 12; the α_s(M_Z) row now names its branch. The mechanism that
let these happen — `check_summary_claims.py` — is now a gate check, covering `papers/Claims-and-
Falsifiers-Summary.md`.

THE RESIDUAL: `papers/README.md` — the series front matter, a PUBLIC document — is STILL at
revision-1 numbers. It headlines sin²θ_W=1/4⇒m_Z/m_W=2/√3 at 1.77%, a value the Claims summary itself
moved off on 2026-08-02 (F49/F138's on-shell 3/√7, -0.064%), and its black-hole line still leads with
the SUPERSEDED shadow number (the F114 picture, withdrawn — see E8's prompt). This was found by
Amendment 3's own audit and explicitly flagged as NOT fixed. `check_summary_claims.py` does NOT cover
this file — it has no claim anchors and is not the register's view, so this gap is invisible to the
existing gate check.

DO NOT RE-ATTACK: the two already-fixed instances (m_W/m_Z Scope entry, α_s branch label) — verify
they're still correct in passing, but the actual work is README.md.

REFERENCES — the current `papers/Claims-and-Falsifiers-Summary.md` (revision 5) is the SOURCE OF
CORRECT VALUES to copy from. Findings: F49, F138 (on-shell 3/√7), F183/F186 (current black-hole
picture, superseding F114's shadow number).

EXTERNAL: n/a — internal documentation fix.

FIRST STEP: diff `papers/README.md`'s numbers against the current Claims-and-Falsifiers-Summary
(revision 5) line by line, not just the two instances already named — Amendment 3 only checked the
two SPECIFIC numbers it was looking for, a full diff may find more.

WHAT PROMOTES THE GRADE: papers/README.md updated to current numbers, AND — the more durable fix —
consider whether `check_summary_claims.py` (or a sibling checker) should be extended to cover this
file too, closing the blind spot rather than just this one instance of it.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — straightforward documentation fix, but check for OTHER stale
public-facing surfaces (e.g. any other README or front-matter file) while here, since this exact
defect shape (a surface `check_summary_claims.py` doesn't reach) may recur elsewhere.

PROTOCOL: this is a documentation fix, not physics research — no finding number needed, just the edit
and a changelog entry. Consider filing a small tooling finding if extending the checker's coverage.
~~~

### *H6 — Reproducibility — `PARTIAL` → next: run `make gate` to actual completion

**Leverage:** high — this is THE barrier metric for the whole tree. **Cost:** small in effort, but
needs an environment that can sustain a ~2-minute run (this session's device-bridge could not).
**Blocked by:** tooling/environment access, not physics.

~~~text
Physics Notes research session (or, more precisely, a verification task). Target: rubric row H6
(reproducibility), currently PARTIAL, target: an actual, witnessed green `make gate` run.

WHAT IS ALREADY TRUE: the specific defect that reddened this row at the 2026-08-18 baseline (F324
invisible to every index) is FIXED and INDEPENDENTLY VERIFIED LIVE by the 2026-08-20 report:
`make indexes-check` returns green, all 8 indexes current, F325 as the newest finding, `[casim index]
ok`. `check_finding_records.py` returns zero violations (verified live, 2026-08-18 Amendment 1).

THE RESIDUAL: `make gate` itself has NOT been run to completion and witnessed green in ANY of the last
several completeness sweeps — the 2026-08-18 report ran nothing live at all (staged/isolated copy
only), and the 2026-08-20 report's attempt hit a device-bridge session-lifetime limitation (background
process did not survive between tool calls; the gate run itself needs roughly 2 minutes, longer than
the bridge's per-call budget). This is a TOOLING gap in how these sessions reach the repository, not a
repository defect — the repository's OWN indexes/registry/health checks all run and pass live.

DO NOT RE-ATTACK: re-verifying indexes-check, registry, numerics, or health individually — all four
were run live and green as of 2026-08-20 (see that report's Health probe table). The gap is
SPECIFICALLY the full end-to-end `make gate` target.

REFERENCES — the 2026-08-20 completeness report's Health probe section, which documents exactly what
was attempted and why it didn't complete.

EXTERNAL: n/a.

FIRST STEP (for Ben, directly, not a remote session): from a terminal with direct access to the
repository (not through a bridged tool with a short per-call timeout), run:
`cd "Physics Notes" && source .vendor/activate.sh && make gate`
and let it run to completion (~2 minutes per the project's own tooling notes). Report the exit code
and any red items.

WHAT PROMOTES THE GRADE: a genuinely witnessed green `make gate` run — this is likely enough by itself
to move H6 to QUANT or better, since every SPECIFIC defect previously named (F324/F325 indexing) is
already fixed; what's missing is only the confirming run.

WHAT WOULD FALSIFY A GREEN EXPECTATION: if `make gate` runs and is NOT green despite indexes-check,
registry, numerics, and health all passing live — that would be a genuinely new and important finding
(something make gate checks that the individual targets don't), worth its own investigation.

PROTOCOL: this is a verification task best done directly (not through a tool with a short call budget).
No finding number needed unless the run surfaces a new defect requiring investigation — in that case,
follow normal finding protocol from there.
~~~

### *H7 — Module coverage — `PARTIAL` → next: reverse the three-report fall in channel-driven fraction

**Leverage:** medium, a real and worsening trend. **Cost:** medium — needs deliberate wiring work, not
new physics. **Blocked by:** nothing named.

~~~text
Physics Notes research session. Target: rubric row H7 (module coverage), currently PARTIAL, target:
reverse the three-consecutive-report fall in channel-driven module fraction.

WHAT IS ALREADY TRUE (baseline figures, NOT re-measured live in the 2026-08-20 report — re-verify
first): 51 of 218 modules channel-driven (23.4%), down from 25.1% and 27.0% in the two prior reports.
THE DRIVEN COUNT HAS BEEN LITERALLY 51 IN ALL THREE REPORTS while the denominator grew 189→203→218 —
every module added in that window was test-only, standalone, or unreferenced, none of it wired into
the live channel-driven graph. Separately, the finding-coverage rollout's ADJACENT metric
(weak_only/untested) improved 66→30 on 2026-08-19 — a related but DIFFERENT metric (it tracks
finding-to-test joins, not module-to-channel wiring), so do not assume this row's own number moved
just because that one did.

THE RESIDUAL: the channel-driven module count is stagnant while the denominator (total modules) keeps
growing — a genuine, worsening structural trend, not just an unlucky snapshot.

DO NOT RE-ATTACK: assuming the finding-coverage rollout's 66→30 improvement (2026-08-19) fixed this
row — it did not; that metric and this one are measuring different things (test-record joins vs
module-registry channel wiring).

REFERENCES — findings: none specific; this is a code/registry-structure question. Run
`from casim.engine.registry import all_modules` (or the equivalent `casim` CLI/module-registry check)
to get the CURRENT live breakdown before doing anything else — the 51/218 figure is carried from the
baseline and was explicitly NOT re-measured live in the 2026-08-20 rerun.

EXTERNAL: n/a — internal code-organization question.

FIRST STEP: get the current live module-registry breakdown (channel-driven / test-only / standalone /
unreferenced / fork_live / fork_unclaimed / dead_candidate counts), then identify the 20-30 modules
added in the last window and check WHY each one is not channel-driven — is it correctly standalone
(a utility, not physics), or is it physics that should be wired in and simply wasn't?

WHAT PROMOTES THE GRADE: either genuinely wiring some fraction of the unreferenced/standalone modules
into the live channel graph where appropriate, OR — if most of the growth is legitimately test-only/
utility code — documenting that explicitly so the denominator's growth stops reading as a coverage
regression when it isn't one.

WHAT WOULD FALSIFY THE ATTEMPT: n/a — this is an audit-and-fix task.

PROTOCOL: this is closer to an audit/cleanup task than physics research. No finding number needed
unless wiring a module in surfaces a physics question. Update the module registry directly, `make
registry` and `make gate` before finishing, and note the corrected fraction in the next completeness
sweep.
~~~

---

## Method notes

**Rows whose bundle needed a finding file rather than the claim-card join table:** A1 (F313's
remediation reasoning), B10/K9 (F325's full adjudication text), K3/K12 (F310's own §11/C8 residual
framing) — these all needed the finding's own prose, not just its registry metadata, because the
residual is a nuanced judgment call rather than a single number.

**Rows where the do-not-re-attack block is `none recorded`:** none in this file — every row above
carries at least one closed leg, consistent with this being a mature, heavily-audited tree rather than
a fresh sweep.

**Rows that got a live literature pass vs terms-only:** NONE got a fresh, dated external pass this
session — the device-bridge budget went to the live health probe (indexes/registry/numerics/health)
instead, which this report judges the higher-value use of limited live-access time for a two-day
rerun. Every EXTERNAL block above carries search terms and named standing anchors, but Ben should
treat them as unverified-today, not dated 2026-08-20. The five priority rows (d1/B8, K9, B9/G3, Q4/
G5-G7, H2) are exactly the ones where a genuine external pass would be most valuable next session —
none of them actually needed one this time, since all five are internal-derivation or internal-
bookkeeping targets, not literature-comparison targets.

**Coverage ratchet, verified:** 81 individual rows below MACHINE (56 rubric + 25 ledger) are all
addressed across 70 prompt sections. The gap between 81 and 70 is accounted for exactly two ways, both
stated so a cold audit can check the arithmetic without re-deriving it: (a) **11 rows folded into 4
grouped ledger sections** because the rubric's own D table already groups them — D#1-6 (6 quark
masses, 1 section), D#7-8 (2 lepton-ratio shapes, 1 section), D#10-13 (4 CKM entries, 1 section),
D#23-25 (3 PMNS angles, 1 section): 15 parameters in 4 sections, a reduction of 11. (b) **Sibling
pointers** (D#9, D#15, D#16, D#19, D#22, D#28, G3, G7, K12 — 9 sections) each address one row by
pointing at another section's full bundle rather than duplicating it, and each is still one section
covering one row exactly, not a reduction. 81 rows − 11 (grouping reduction) = 70 sections — **match**.
