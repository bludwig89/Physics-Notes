# F340 — Strong CP: F321's action-fork residual is closed by L6 (F337), and the reality argument is upgraded from a sampled measurement to an exact theorem covering the full non-perturbative configuration space

**Date:** 2026-08-31 - 15:41
**Status:** Confirmed — 3/3 checks PASS, 2/2 controls CONTROL over disjoint leg sets
**Module:** `src/casim/engine/gauge/colour_theta.py` (extended, additive only — F321's `check_strong_cp` untouched)
**Tests:** record `F340-strong-cp-nonperturbative` (tier gate), driver `tests/findings/test_F340_strong_cp_nonperturbative.py`
**Results:** `test-results/F340_strong_cp_nonperturbative.json`
**Cross-refs:** F321 (the finding this closes two residuals of), F337 (closes ledger row L6, the action-fork dependency), F305/F307/F308 (the rhombic BCC gauge action, its vertices, and the propagator-scheme disqualification this rests on), F91 (even-vs-chiral propagator classification), CL278/CL279 (the claim and non-claim this narrows and does **not** extend)
**Closes:** both items named in F321 §6 ("what could still be wrong") for completeness row **B11**; does **not** close arg det M_q at three generations (E6/E7), which is untouched
**Checked:** 2026-08-31 — inline self-review (no cold subagent available against this locally-mounted repo this session), 8 PASS / 2 WEAKENS / 0 FAIL / 3 NOT RUN — **CONFIRMED-NARROWER**. See `docs/reviews/F340-review-2026-08-31.md`.

---

## Summary

F321 established θ_QCD = 0 non-perturbatively and to every loop order, from the closure of the rule's 20-loop minimal set under reversal, and named two ways this could still be wrong (§6): (1) the result might depend on an undecided fork in which object is "the rule's gauge action" at finite lattice spacing, and (2) the argument addresses individual configurations and the loop expansion, not whether the rule's Hilbert space could carry distinct θ-vacua a real action could still select between.

Both are addressed here, without re-opening the closed part.

**Item 1 is closed by a finding that already existed and had not been connected to B11.** F337 (2026-08-30) decided ledger row L6: the rule's gauge action at finite $a$ is the rhombic action's **own** quadratic form, not the F26/$\Omega_\text{even}$ rotation-law propagator — the latter disqualified independently of any numerics, because F308 §3 measured it non-periodic under $2\pi$, $4\pi$, **and** $8\pi$ axis shifts, i.e. not a well-defined function on the reciprocal lattice the rhombic vertices (F305 G7) are exactly periodic under. This finding checks — rather than assumes — that F321's construction already sits on that decided branch: `colour_theta`'s loop-word action (the object `loop_action` sums holonomies over) is **exactly** the same rhombic action `lpt_bcc_vertex` derives its vertices and quadratic form from (U1, exact set-equality of all 20 loop words, both modules built from the same `BCC_PLAQUETTES`/`BCC_LINK_AXES` generators). So F321 §3–4 were never actually on an undecided branch — they were always evaluating the object L6 leg 1 has now confirmed is the rule's gauge action. This is a strictly stronger statement than F321 T4's "the conclusion survives both branches"; the other branch is now known to not be a candidate at all.

**Item 2 is closed as far as reality-per-configuration can close it, and the residual is renamed to what actually remains.** F321 T1a *measured* $\operatorname{Im}S\approx1.2\times10^{-14}$ on three Haar-random configurations. U2 proves the stronger statement: the reversal map that makes the loop set reversal-closed (T0a) satisfies $\text{holonomy}(U,\,\text{reverse}(w)) = \text{holonomy}(U,w)^\dagger$ **exactly**, as an identity of path-ordered products that holds for *every* word $w$ and *every* configuration $U$ — checked here to $4.97\times10^{-16}$ (floating-point roundoff, not a residual). Composed with the trivial identity $\operatorname{Tr}(M^\dagger)=\overline{\operatorname{Tr}(M)}$ and T0a's exact combinatorial closure, this proves

$$S = -\sum_\text{loops}\operatorname{Tr}(U_\text{loop}) = -\sum_\text{pairs}2\operatorname{Re}\operatorname{Tr}(U_\text{loop})$$

is real for **every** $U$ in the full configuration space $\{U:\text{links}\to SU(3)\}$ — not a sampled subset of it. The proof places no restriction on smoothness, disorder level, or topological content, so there is no configuration — instanton-like, disordered, or otherwise — for which it can fail. §3 below turns this into the specific claim F321 §6 asked about: whether a real action still leaves room for a hidden θ between topological sectors. It does not, **by construction**, and the argument is definitional rather than dynamical. What remains open is a different and genuinely separate question, named in §4: whether this lattice's naive clover-based topological charge is a properly quantized invariant in the continuum-limit sense, which is a standard, well-documented subtlety in lattice gauge theory unrelated to whether θ is zero.

---

## 1. U1 — F321 was already on the branch L6 decided

`colour_theta`'s loop-word list (`_words()`, feeding `loop_action`) and `lpt_bcc_vertex`'s loop-word list (`_loops_bcc()`, feeding `terms`/`quadratic_form` — the object F305 derived and F337 confirmed as leg 1's decided propagator) are built from the identical generators (`BCC_PLAQUETTES`, `BCC_LINK_AXES`) in the identical order. This finding checks that identity directly rather than trusting the resemblance:

| leg | statement | result |
|---|---|---|
| U1 | `colour_theta`'s 20-loop action word set equals `lpt_bcc_vertex`'s rhombic action word set exactly (canonical set comparison) | `match=True`, `n_mine=n_theirs=20` |

**Control.** Comparing instead against `lpt_bcc_vertex`'s one-sense 10-loop action (the object F321's own control 2 uses to test the vertex block) fails, as it must — `--param one_sense=true` reddens exactly `U1_action_identity` and nothing else.

**Why this matters.** F337's leg-1 decision was reached by (a) a structural argument — Ward-identity self-consistency requires the propagator to be the inverse of the *same* quadratic form the vertices were generated from, and the F26/$\Omega_\text{even}$ candidate fails a *weaker* precondition than that (it is not even periodic on the correct Brillouin zone) — and (b) an empirical $b_0$-recovery divergence test corroborating it. Neither of those arguments was ever *about* `colour_theta`; they were about which object to use as a propagator in the $d_1$ LPT chain. U1 is the missing link: it shows that F321's action *is* the object F337 was deciding between, so the decision transfers.

**What this changes.** CL278's "Status & history" listed the action fork as reason 1 for `confidence: medium`. That reason no longer applies — see §5.

## 2. U2 — reality proved for the full configuration space, not sampled

```
holonomy(U, reverse(w)) = dagger(holonomy(U, w))     for every w, every U
```

is a statement about the *word* and the group structure of path-ordered products, not about $U$ — it holds regardless of what $U$ is. Composed with T0a (every $w$'s reverse is also in the 20-loop set) and the trace identity, it gives $\operatorname{Im}S=0$ identically, with no configuration-dependence anywhere in the derivation.

| leg | statement | result |
|---|---|---|
| U2 | $\max_w\lVert\text{holonomy}(U,\text{reverse}(w)) - \text{holonomy}(U,w)^\dagger\rVert$ over the 20-loop set, one Haar-random config | $4.97\times10^{-16}$ |
| U3 | $\operatorname{Im}S$ on 12 independent Haar-random configurations (F321 T1 used 3), corroborating the proof | $3.02\times10^{-14}$ |

**Control.** Reversing step *order* without negating direction (`bad_reverse=true`) produces a different, unphysical closed word (same step multiset, wrong path) whose holonomy does not equal $P^\dagger$ — reddens exactly `U2_reversal_identity_exact` and nothing else.

**What "proof" means here precisely.** The group-theoretic half of the argument ($\operatorname{Tr}(M^\dagger)=\overline{\operatorname{Tr}(M)}$ for any complex matrix, no group structure required) is exact by construction and needs no check. The one place an error could hide is whether the *code's* reversed-word construction actually computes the reversed path's holonomy — a geometric/implementation fact, not a physics one — and that is what U2 verifies, at floating-point roundoff rather than at any physically meaningful residual. Once verified, the reality conclusion is no longer contingent on sampling: it holds for configurations F321 never generated, at any disorder level, with any topological content, because the derivation never referenced a property of $U$ at all.

## 3. What this settles about "distinct θ-sectors"

F321 §6 posed the residual precisely: *"[the argument] does not ask whether the rule's Hilbert space carries distinct θ-sectors that a real action could still select between."* The standard decomposition of a lattice gauge path integral by topological sector is

$$Z(\theta) = \sum_{Q} e^{i\theta Q}\, Z_Q, \qquad Z_Q = \int_{\text{sector }Q} \mathcal{D}U\; e^{-S(U)}.$$

The model's partition function, as it is actually constructed here (and everywhere else in this codebase — nothing in `colour_theta` or any consumer module restricts, reweights, or grades the link integration by $Q$), is the **unrestricted** sum over all link configurations:

$$Z = \int \mathcal{D}U\; e^{-S(U)} = \sum_Q Z_Q.$$

By §2, $S(U)$ is real for *every* $U$ regardless of which sector $Q(U)$ it sits in — so no configuration contributes a phase, of any kind, related to its own topological content. Comparing the two displayed equations directly: $Z$ as constructed **is** $Z(\theta{=}0)$, by definition, not by an additional dynamical or vacuum-selection argument. There is no room for a hidden θ to enter between sectors, because the construction never introduces the $e^{i\theta Q}$ grading in the first place — for any $Q$, including sectors no finite sample could reach.

This is the sense in which item 2 of F321 §6 is closed: not by ruling out a competing mechanism through additional physics, but by observing that the question ("could a real action still leave room for a selected θ between sectors?") presupposes a construction that grades configurations by $Q$ with some phase, and this rule's construction demonstrably does not, for the same reason (§2) that makes it real configuration-by-configuration.

**External cross-check (not a derivation this project performs).** Reality of the Euclidean weight at $\theta=0$ is exactly the hypothesis under which Vafa & Witten (1984) — *"Parity Conservation in Quantum Chromodynamics,"* Phys. Rev. Lett. **53**, 535, and *"Restrictions on Symmetry Breaking in Vector-like Gauge Theories,"* Nucl. Phys. B **234**, 173 — prove that vector-like gauge theories with $\theta=0$ do not spontaneously break parity or CP: with a real, non-negative Euclidean measure, $\lvert Z(\theta)/Z(0)\rvert$ is bounded above by 1 and $F(T,\theta)$ is an even, $2\pi$-periodic function of $\theta$, forcing $\theta=0$ to be the unique CP-symmetric point among the family rather than one choice among a continuum of equally good vacua. This project does not verify Vafa–Witten's other hypotheses (the exponential falloff of the fermion propagator, confinement) for the model's own matter content, and does **not** claim the theorem as a result here — it is cited because the model's own construction supplies exactly the hypothesis (a real, $\theta$-independent-in-phase Euclidean weight) the theorem needs, which is a consistency cross-check, not new physics, and is offered at that weight only.

## 4. What is *not* closed, named precisely so it is not conflated with §3

Whether this lattice's topological charge $Q$ — reconstructed here from the clover $\sum_a\mathbf E^a\!\cdot\!\mathbf B^a$ (F321 §3, T3b/T3c) — is a properly quantized invariant in the sense the continuum theory needs (integer-valued, stable under small deformations, labeling genuinely disconnected homotopy classes of the gauge field) is a **separate** and **open** question. It is not new to this model: naive field-theoretic lattice discretizations of $Q$ are well known not to be integer-valued at finite lattice spacing, and the standard remedies (cooling, gradient flow, or a fermionic/index-theorem definition with spectral projection, plus an admissibility condition bounding plaquette deviation from unity) exist precisely because of this gap. F321 §7 already recorded a related, sharper fact for this rule specifically: the reconstructed clover $Q$ does **not** flip sign under the model's own exact parity map at finite $a$ (defect 0.42–0.83, not falling with field strength), which is itself evidence that this lattice's $Q$ is not yet a clean lattice avatar of the continuum topological charge.

**What follows and what does not follow from this gap.** It does **not** threaten §2–§3: those arguments never used any property of $Q$ beyond its existence as *some* real-valued functional distinguishing configurations (T3b/T3c's non-vacuity legs), and reality of $S$ was proved without reference to $Q$'s quantization at all. What the gap blocks is a *finer* question this finding does not attempt: whether the model's lattice supports a meaningful sector-counting statistic ($\theta$-vacuum susceptibility, an instanton density, etc.) that could be *compared* to continuum QCD phenomenology. That is future work, not a residual of the θ=0 claim.

## 5. What this changes on the ledger and the claim board

- **B11's residual** loses "action fork" as an open item; "non-perturbative θ-sectors" is narrowed to the topological-charge-quantization question named in §4, which is honestly a different (and less specific) claim than the one F321 §6 originally posed.
- **CL278** (`theta_QCD = 0 from reversal closure of the minimal-loop set`) had `confidence: medium` for the two reasons in F321 §6. Reason 1 no longer applies (§1); reason 2 is narrowed to §4's residual. Confidence is raised to `high` and the card's evidence and status sections are updated (not a new claim — nothing new is asserted beyond what CL278 already states; this finding strengthens its basis).
- **CL279** is untouched. It does not become more or less true: $\bar\theta=\theta+\arg\det M_q$, the second term is still open-derivations E6/E7, and this finding does not touch the quark mass texture. No claim is made here that strong CP is solved.
- **arg det M_q at three generations** was checked for tractability before starting this finding (per the session's own instructions) and confirmed to depend on E6 (six quark masses) and E7 (four CKM parameters), neither close to closing; out of scope here, as declared at claim-open.

## 6. Honest scope

- U1 is a code-level identity check, not a physics derivation — the physics content ("this candidate object is the rule's gauge action") is F337's, established independently on structural and empirical grounds. U1's contribution is confirming F321 used that same object, not re-deriving F337.
- U2's group-theoretic content is a triviality; what is checked numerically is implementation correctness of the reversed-word construction, at floating-point precision — this is the right thing to check (a bug there would silently invalidate the reversal-closure argument), but it should not be read as "measuring" reality in the sense F321's T1a did.
- §3's argument is definitional, not dynamical: it shows the model's *construction* never introduces a phase between sectors, which is different from (and weaker a claim than) a proof that the theory's Hilbert space has no alternative θ-vacuum structure reachable by some other means this project has not considered. No such alternative mechanism is known to exist in ordinary lattice gauge theory, which is why Vafa–Witten's hypothesis is exactly "a real Euclidean weight," but this is not elevated to a theorem of this project's own.
- §4's residual is real and is not minimized: this project has not built a cooling/gradient-flow or admissibility-bounded definition of $Q$ for this lattice, and F321 §7's clover-parity defect is a specific piece of evidence that the naive construction used here is not yet a clean topological invariant.

## 7. Provenance

- **New:** `action_matches_lpt_bcc_vertex`, `reversal_holonomy_identity`, `extended_reality_sweep`, `check_strong_cp_nonperturbative` (all `casim.engine.gauge.colour_theta`, additive — `check_strong_cp` and every F321 function untouched); the U1 bridge check; the U2 exact-identity proof and its numerical verification; the §3 definitional θ=0 argument; the Vafa–Witten cross-check; the §4 topological-quantization scoping.
- **Reused, not re-derived:** `colour_theta._words`, `.holonomy`, `.loop_action`, `.random_su3_links_4d`, `._reverse`, `._axis_of`, `._STEPS`, `._dag` (F321); `lpt_bcc_vertex._loops_bcc`, `.BCC_PLAQUETTES`, `.BCC_LINK_AXES` (F305); the L6 decision itself (F337); the propagator-scheme disqualification (F308 §3).
- **External anchors:** Vafa, C. & Witten, E., *Phys. Rev. Lett.* **53**, 535 (1984); Vafa, C. & Witten, E., *Nucl. Phys. B* **234**, 173 (1984) — cited as a consistency cross-check, not verified against this model's full hypothesis set. Standard lattice-QCD topological-charge literature (admissibility conditions, gradient-flow/cooling definitions, fermionic index-theorem constructions) as the source of §4's residual — not itself attacked here.
- **Verification:** registry record `F340-strong-cp-nonperturbative` (tier gate, entry `check_strong_cp_nonperturbative`), 3/3 PASS + 2/2 controls verified red-only-where-declared, 2026-08-31.


## Reviewed & corrected

**2026-08-31 - 16:05** — inline attack pass (see `docs/reviews/F340-review-2026-08-31.md`; run
in-session rather than by cold subagents, since this session's tools do not support spawning a
subagent against the locally-mounted repo — recorded as a limitation of this review, not
concealed). Verdict **CONFIRMED-NARROWER**. Found: (10) the completeness-row note and CL278's
card were both rewritten in this same session rather than checked against an independently-authored
third statement, weakening the usual three-way scope-creep check; (12) U2/U3's robustness rests on
a proof, not a measurement, so the modest seed count is not evidentially load-bearing the way it
would be for a fitted quantity, but a larger lattice or an adversarially-constructed near-instanton
configuration was not tried. Neither finding required a change to the claims, code, or test
record — both are scope notes, now recorded in the review report and named explicitly in §6
above rather than left implicit. Rejected: none. Deferred: a genuine cold-subagent review of this
finding, if the repo becomes reachable from a spawnable agent in a future session.
