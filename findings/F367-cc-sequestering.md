# F367 — A genuinely non-local/global mechanism (Kaloper–Padilla-style vacuum-energy sequestering) achieves unbounded order-selectivity between the F164/F59 heat-kernel moments as an exact, sympy-verified identity — but grafting it onto this model requires new gravitational-sector content beyond decision 4, and it inherits, rather than resolves, F241's own $O(1)$ residual

**Date:** 2026-09-04 - 23:10
**Numbering:** **F367**, taken as `NEXT FREE NUMBER` (max was F366, no gaps).
**Status:** **Positive on the mechanism's core selectivity claim (exact, sympy-verified); negative/honest on adoption.** The load-bearing identity — a spacetime-constant additive piece of the matter-trace source is annihilated *exactly* by Kaloper–Padilla-style spacetime averaging, independent of the constant's magnitude — is proven symbolically (not merely cited) and gives selectivity that is formally unbounded, dwarfing F319 U8's required $\ge1.27\times10^{116}$. F164's bare $\rho_\text{vac}$ is shown to be exactly the class of source this identity eliminates. The surviving (matter-history) residual is an exact closed form, $3n\,\rho_m(t_0)$ for $a(t)\sim t^n$ domination, landing $0.036$ dex from the observed $\Omega_\Lambda\rho_\text{crit}$ at $n=2/3$ — flagged explicitly as a crude single-fluid toy, not a derivation of $\Omega_\Lambda$. 3/3 checks PASS, 2/2 declared controls verified red-and-only-there. Adoption is **not** made: it would require grafting new global, non-propagating Lagrange-multiplier fields onto the CLAUDE.md decision-4 action, which is imported machinery outside a single finding's remit, and it does not resolve F241's $\Omega_\Lambda$ "why now" residual.
**Checked:** 2026-09-04 - 23:40 -- 12 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN -- **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/interactions/cosmology_lambda_sequestering.py`
**Registry record:** `F367-cc-sequestering` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, 2 controls verified red-and-only-there)
**Results:** `test-results/F367_cc_sequestering.json`
**Claim:** `docs/claims/CL303-sequestering-selectivity-identity-not-adopted.md` (`status: contingent`, `kind: derivation`) — the standing rule applies because grafting a Kaloper–Padilla global sequestering sector onto Einstein gravity is itself an extension of GR (new non-propagating fields in the action); the card states plainly that this is a *checked candidate*, not an adopted part of the model, and names exactly what adopting it would need.
**Addresses:** rubric row **K9**, ledger **G1** (F332's own named next step, §5: *"the one channel of the right TYPE to evade Weinberg's no-go theorem is a non-local/global one... this finding does not attempt to build such a mechanism... it records the connection as context"*). Also touches rubric **A11** and parameter **#28** (same residual).
**Cross-references:** [[F332-cc-dynamics-two-channels-excluded]] (closed the two *local* channels and named this one, unbuilt), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the bare $\rho_\text{vac}$ this mechanism targets), [[F193-ontic-vacuum-gravitates-as-zero]] / [[F196-dilution-exponent-derived]] (the surviving ceiling route, still undynamicised, left untouched here), [[F241-omega-lambda-o1-residual-anthropic]] (the $O(1)$/$\Omega_\Lambda$ residual this inherits unchanged, and whose own numerology-caution standard is applied to §5's numerical near-hit; also the source of the excluded future-event-horizon circularity this finding is contrasted against, §6), [[F319-uv-sector-reconciled-physical-cutoff-and-counterterms]] (U8's $\ge1.27\times10^{116}$ selectivity requirement and its dim-0/dim-2 operator ledger, used verbatim in §S1), [[F178-gravity-full-tensor-adoption]] / [[F182-friedmann-pressure-cosmology]] (the model's own adopted gravity law this mechanism would extend), [[F79-structural-newton-constant]] / [[F59-induced-eh-prefactor-and-f10-selection]] (structural $G$, the $a_1$ moment untouched by this mechanism by construction). External: Kaloper, N. & Padilla, A., "Sequestering the Standard Model Vacuum Energy", *Phys. Rev. Lett.* **112**, 091304 (2014) (the mechanism, cited not re-derived in full generality); Kaloper, N. & Padilla, A., *Phys. Rev. D* **90**, 103523 (2014) (companion, cited by F332 sec.5 and here); Weinberg, S., *Rev. Mod. Phys.* **61**, 1 (1989) (the no-go theorem this mechanism is the literature's own non-local evasion of, per F332 sec.5); Padilla, A., "Lectures on the Cosmological Constant Problem", arXiv:1502.05296 (review, already cited by F332).

---

## 1. What F332 left open, precisely

F332 (2026-08-28) ran two concrete, computed checks against the two candidate channels of the right *shape* that Amendment 4 (2026-08-18) left standing, and closed both: F164 channel (ii) ($AB\equiv1$ sequestering) has no hook into a homogeneous source at all (the static Poisson law is exactly Fredholm-blind to a constant source, and F178 restricts $AB\equiv1$ to $T_{\mu\nu}=0$ regions a homogeneous vacuum energy is never in); and a literal F130 block-spin recomputation of the two Sakharov moments is excluded by $35.15$ orders beyond the CODATA $G$ budget, with $a_0$ and $a_1$ moving in *opposite* directions as the block size grows — a worse failure than F319's own uniform-$\lambda$ exclusion.

F332 §5 then named, and explicitly declined to build, the one channel *type* neither closed attempt was: citing Weinberg's 1989 no-go theorem (any **local**, Lorentz-invariant adjustment mechanism cannot relax a large bare CC without reintroducing the same fine-tuning), it observed that the surviving F193§B/F196/F241 ceiling route is already of the right (non-local, horizon-tied) *type* to evade that theorem, and that the literature's own analogous construction is Kaloper & Padilla's vacuum-energy sequestering — "cited by analogy, not used." This finding builds it, against this model's own numbers, and reports what it does and does not deliver.

## 2. The mechanism, cited, and the one piece re-derived here rather than merely asserted

Kaloper & Padilla's construction (PRL 112, 091304; PRD 90, 103523) adds a global, non-propagating Lagrange-multiplier sector to the gravitational action. Its consequence for the local field equations — the piece this finding uses — is that the Einstein equations end up effectively sourced not by the matter trace $T(x)$ directly, but by

$$T(x) - \langle T\rangle, \qquad \langle T\rangle \equiv \frac{1}{V_4}\int d^4x\,\sqrt{-g}\,T(x),$$

the trace averaged over the *entire* (necessarily finite) spacetime history, $V_4=\int d^4x\sqrt{-g}$. This is cited, not re-derived from the multiplier action in full generality here — reproducing the Lagrangian's exact normalisation is not needed for what follows, because the load-bearing consequence is elementary enough to check directly and independently:

**Claim, verified symbolically (not merely asserted from the citation):** if $T(t) = T_\text{matter}(t) + C$ for an *arbitrary* constant $C$ (the "vacuum" piece), then $T(t_0) - \langle T\rangle$ is exactly independent of $C$, for any finite $V_4$.

This is checked in `sequestering_symbolic_identity` (sympy) for a single power-law-dominated flat FRW history $a(t) = (t/t_0)^n$ on $t\in[0,t_0]$ ($a_0 := a(t_0)=1$, only ratios enter), with $\rho_m(t) = \rho_{m0}\,a(t)^{-3}$, $T(t) = -\rho_m(t) - C$, and the spacetime-volume weight $a(t)^p\,dt$ ($p=3$ is the physical $\sqrt{-g}$ FRW spatial-volume measure):

$$\frac{d}{dC}\Big[T(t_0) - \langle T\rangle\Big] \equiv 0 \quad\text{identically, for every }n\text{ and every measure power }p.$$

Hand-derivable in one line and confirmed by the symbolic computation: $C$ enters $T(t)$ additively and with the *same* weight in both the "now" slice and the average, so it cancels in the subtraction regardless of its size, the exponent $n$, or the measure power $p$ — a fact about the subtraction *structure*, not about the specific measure. Numerically this was independently spot-checked by evaluating the residual at $C=0,\,1,\,10^{60}\rho_{m0},\,10^{120}\rho_{m0}$ directly (not shown in the registry record, which uses the symbolic form) and confirming bit-identical output.

**Consequence for F319 U8.** A constant contribution to the trace, however large, is annihilated *exactly* — the selectivity between it and anything varying in time is formally unbounded (`this_mechanism_selectivity: inf` in the module's own output), which trivially and enormously exceeds F319's finite requirement of $\ge1.27\times10^{116}$. This is qualitatively different from F332's two closed channels: neither the $AB\equiv1$ Fredholm obstruction nor the block-spin recomputation offered *any* selectivity between $a_0$ and $a_1$ (the first has none at all to offer; the second moves both, in the wrong relative direction) — sequestering's central mechanism offers, in principle, all of it, for a source that is genuinely constant.

## 3. S1 — applicability is not blocked by the Sakharov origin of this model's $G$ and $\rho_\text{vac}$

A natural objection: in this model, unlike vanilla field theory, $1/G$ (F59, the $a_1$ heat-kernel moment) and $\rho_\text{vac}$ (F164, the $a_0$ moment) are **both** loop-induced from the *same* one-loop determinant — "same modes, same measure, same factor of $\tfrac12$," in F319's own words, the fact Amendment 4 used to exclude the *uniform* reweighting class (F193 Part A, CL275). Does that block sequestering too?

No, for a reason already on record in this model's own tree. F319 §7's operator ledger enumerates the model's IR effective action operator by operator and finds **exactly two** unabsorbable coefficients: the identity operator (the cosmological constant, dimension 0) and the Einstein–Hilbert operator ($1/G$, dimension 2) — listed as two *separate* rows of that ledger, each a free Wilson coefficient of the model's own derivative expansion, regardless of their common microscopic origin. Sequestering acts at exactly that IR-EFT level: on the coefficient of the identity operator alone, leaving the Einstein–Hilbert coefficient's *value* (however it was generated) untouched by construction — the multiplier sector couples to $\int\sqrt{-g}\,\Lambda$, not to $\int\sqrt{-g}\,R$. It is therefore not the "uniform reweighting of the microscopic zero-point sum" class F319 U8/Amendment 4 already excluded; it is a different class of object (a constraint on the IR coefficient, not a rescaling of the UV sum that produces it), and nothing in this model's own operator counting blocks it.

## 4. S4 — the model-specific match: F164's bare $\rho_\text{vac}$ is exactly the source class this identity eliminates

The identity in §2 is only useful here if F164's $\rho_\text{vac}$ is actually the kind of source it targets: a genuine spacetime constant, not something already varying with cosmic time. Checking against F164/F107/F182 directly: $\rho_\text{vac} = g_*\sqrt3\,I_\text{CC}\,\hbar c/a^4$ is built from the fixed lattice cell $a$ (F107's canonical, non-dynamical constant) and nothing else. Nothing in the model's adopted cosmology (F182's Friedmann-I, the FRW reduction of decision 4) makes $a$ — hence $\rho_\text{vac}$ — evolve with cosmic time; it is a static property of the CA microstructure, exactly as F164 computes it. So F164's residual is not merely "some constant vacuum energy, in general" — it is, by the model's own construction, precisely the source class §2's identity annihilates exactly. This is a structural fact about *this* model's specific residual, checked against F164/F107/F182 by citation rather than asserted about sequestering in general.

## 5. S5 — the surviving residual: an exact closed form, evaluated at physical $\Omega_{m0}$

Since the constant piece cancels exactly (§2), whatever residual survives comes entirely from the *historically varying* matter/radiation trace. For single power-law domination $a(t)\sim t^n$ ($n=2/3$ matter, $n=1/2$ radiation), the same symbolic computation gives, at the physical measure $p=3$,

$$\frac{T(t_0)-\langle T\rangle}{\rho_m(t_0)} = 3n \quad\text{exactly (sympy-confirmed rational, not a numerical fit).}$$

Evaluated at matter domination ($n=2/3$, coefficient $=2$) with $\Omega_{m0}=0.3153$ (Planck 2018, already `OMEGA_M0` in the tree's `cosmology.py`):

| quantity | value |
|---|---|
| coefficient $3n$ ($n=2/3$) | $2$ (exact) |
| predicted residual$/\rho_\text{crit} = 2\,\Omega_{m0}$ | $0.6306$ |
| observed $\Omega_\Lambda\,\rho_\text{crit}/\rho_\text{crit}$ (Planck 2018, $\Omega_{m0}+\Omega_{r0}+\Omega_\Lambda=1$) | $0.6846$ |
| agreement | $-0.036$ dex |

This lands the sequestering residual at the *same parametric scale* as F196/F241's ceiling ($\rho\sim\rho_\text{crit}$) via a genuinely dynamical computation (an evolving history integrated over cosmic time) rather than a restated inequality — this is the qualitative difference from F241's own characterization of the holographic sector as fixing only a ceiling, "an inequality, not a slope" (F241 §2).

**This is not offered as a derivation of $\Omega_\Lambda$, and the $0.036$-dex agreement is flagged explicitly as likely fragile.** Per F241's own numerology-caution standard (its §5 treatment of $2/3$, $\ln2$, $e/4$, $1/\sqrt2$ as cheap near-hits within a wide window): this is a *single-fluid* toy — it ignores the radiation era entirely, treats the whole history as matter-dominated back to $t=0$ (no regulator needed for the integral at $n=2/3$, but also no physical justification for extending "matter domination" that far back), ignores the matter-to-$\Lambda$ transition the real universe is currently inside, and evaluates the exact coefficient at a single, hand-picked $n$ rather than integrating a mixed multi-era history. Swapping to radiation domination alone ($n=1/2$, coefficient $1.5$) with $\Omega_{r0}\sim10^{-4}$ would give a wildly different (tiny) answer — the toy's output is sensitive to exactly the kind of modelling choice F241 warns against reading too much into. The $0.036$-dex figure is reported as *consistent with, not independent evidence for*, F196/F241's existing $0.10$-dex figure; it is not a tighter derivation of the same thing.

## 6. S6 — this is not F241's already-excluded circular route

F241 §3 already tested and excluded a different non-local candidate: holographic dark energy with the IR cutoff set to the *future event horizon* $R_\text{EH}$ (Li 2004). That route is **circular**: $R_\text{EH}=a\int_a^\infty da'/(a'^2H)$ is itself a function of $\Omega_\Lambda$, so imposing $\rho_\Lambda=3c^4/(8\pi G R_\text{EH}^2)$ is an identity satisfied for *any* $\Omega_\Lambda$ — not a prediction (F241 verified this numerically: $1/(H_0R_\text{EH})^2\to0.76$ today for the *input* $\Omega_\Lambda=0.6847$, and $\to\Omega_\Lambda$ exactly as $a\to\infty$, a self-consistency relation with no content).

§2's identity is not circular in that sense. "A spacetime-constant piece of $T$ cancels exactly under averaging" is a statement about the subtraction structure that holds for *any* finite $V_4$ and *any* value of the constant — it is never solved self-referentially in terms of the quantity it is used to explain (unlike $R_\text{EH}(\Omega_\Lambda)$, nothing here is defined in terms of $\Omega_\Lambda$). What §5's *size* estimate does require — and this is the honestly-inherited, not newly-discovered, gap — is an input about the total cosmic history: which power law, over what interval, and (for the mechanism as a whole, in its full generality beyond the toy computed here) a finite total spacetime 4-volume, i.e. some assumption about the universe's future duration. That is the sequestering literature's own well-known "why is there a future boundary, and why now" caveat, and it is not resolved here — it is exactly F241's own already-classified residual, restated in sequestering's own language rather than solved.

## 7. What this does and does not do — the adoption question

**Does:** proves, symbolically and independently of the citation, that a spacetime-constant vacuum contribution is annihilated *exactly* by the sequestering subtraction (§2); shows this model's own $F319$ operator ledger already treats $\Lambda$ and $1/G$ as separable IR coefficients, so the mechanism is not blocked by the shared Sakharov origin (§3); shows F164's specific bare $\rho_\text{vac}$ is exactly the eliminable source class (§4); computes an exact closed-form surviving residual and evaluates it at physical $\Omega_{m0}$, landing within $0.036$ dex of the observed value (§5); and distinguishes this from F241's already-excluded circular FEH route (§6).

**Does not:** adopt sequestering as part of this model's gravity sector. Doing so would graft new global, non-propagating Lagrange-multiplier fields onto the CLAUDE.md decision-4 action ($G_{\mu\nu}=8\pi G/c^4\,T_{\mu\nu}$, no such fields) — imported machinery, not derived from the CA, and a decision of that scope (a new module in the gravitational action, evaluated against everything decision 4 already carries — PPN parameters, the induced-$G$ derivation, the F178 vacuum-scope restriction, etc.) is outside what a single finding can respectably settle. It also does not derive $\Omega_\Lambda$ (F241's residual is untouched, §5), does not resolve the mechanism's own known "why now"/finite-total-time caveat (§6), and does not reopen $p=2$ (F196) or CL275 (F311/F319's uniform-$\lambda$ exclusion — unaffected, since sequestering is not that class, §3).

This is not a fourth candidate of the kind F332 closed for the first two (F332's channels were shown structurally incapable); it is the first candidate of the *non-local* kind F332 §5 named and explicitly did not build, shown here to structurally satisfy the required selectivity (unboundedly, by an exact identity) and to be well-matched to this model's specific residual — with its import cost, and the residual it does not touch, both stated plainly rather than left implicit.

## 8. What is derived vs computed vs cited

| Piece | Status |
|---|---|
| $d(\text{residual})/dC \equiv 0$ for any $n$, any measure power $p$ | **exact** (sympy symbolic identity, residual $0$ by construction) |
| Selectivity between a constant source and anything else, under this mechanism | **unbounded** (formal consequence of the identity above, not a fitted number) |
| $\Lambda$ and $1/G$ are separable IR-EFT coefficients in this model (S1) | **structural** (citation of F319 §7's own operator ledger) |
| F164's $\rho_\text{vac}$ is a spacetime constant under the model's adopted cosmology (S4) | **structural** (citation of F164/F107/F182) |
| Residual/$\rho_m(t_0) = 3n$ for $a\sim t^n$ domination, at the physical measure $p=3$ | **exact** (sympy, closed-form rational) |
| Residual at $n=2/3$, $\Omega_{m0}=0.3153$: $0.036$ dex from observed $\Omega_\Lambda\rho_\text{crit}$ | **quantitative** (computed; explicitly flagged as toy-model-fragile, §5) |
| Not circular in F241's FEH sense (S6) | **argued** (structural comparison, not a new computation) |
| Adoption into the model's gravity sector | **not made** — flagged as import, outside this finding's remit |
| $\Omega_\Lambda$, F241's residual | **untouched** |

## 9. Falsifiers

1. **A demonstration that $d(\text{residual})/dC \ne 0$ for some finite $V_4$**, i.e. that the constant-cancellation identity of §2 does not hold generally. This is checked symbolically here for general $n$ and general measure power $p$; a genuine counterexample would need a source/measure combination outside what was checked, or an error in the symbolic simplification (independently re-derivable by hand in three lines, §2).
2. **A demonstration that F164's $\rho_\text{vac}$ is not, in fact, a spacetime constant under the model's own adopted cosmology** — e.g. a reading of F182/F107 under which the lattice cell $a$ is itself dynamical with cosmic time. This would break §4's model-specific match without touching §2's identity itself.
3. **A demonstration that F319 §7's operator ledger is wrong to treat $\Lambda$ and $1/G$ as separable IR coefficients** — e.g. an argument that the model's specific UV completion forces a fixed relation between them at the *effective*, not just microscopic, level. This is the single most attackable structural step in this finding (a citation, not a new computation), matching the honest-scope pattern of F332's own K2b.
4. **A recomputed matter-domination coefficient differing from the exact rational $3n$** (sympy, closed form) — would indicate an error in the symbolic integration, checkable independently by hand.
5. **A properly-integrated multi-era (radiation$\to$matter$\to\Lambda$) history landing far outside $O(1)$ of $\rho_\text{crit}$** — would weaken (not falsify) §5's "right parametric scale" observation, which is already flagged as resting on a crude single-fluid toy.
6. **A worked construction showing sequestering's global Lagrange-multiplier sector is inconsistent with decision 4's other adopted content** (PPN, the F178 vacuum-scope restriction, the induced-$G$ derivation) — would close off the adoption question this finding deliberately leaves open, in the negative direction.

## 10. Honest scope

This finding's strongest claim is the narrowest one: a specific, elementary mathematical fact (constant-cancellation under a weighted spacetime average) is proven symbolically, not merely imported from a citation, and it happens to be exactly the property F319 U8's selectivity requirement needs and exactly the property F164's bare residual (a genuine lattice constant, §4) qualifies for. That combination is real, checked content, and it is qualitatively different from F332's two closed channels — this is the non-local *type* Weinberg's theorem (cited by F332, not re-derived here either) says a local mechanism cannot deliver, and unlike the FEH route F241 already excluded, it is not circular (§6).

Its weakest claim is the numerical one (§5): the $0.036$-dex agreement is a single-fluid toy evaluated at one hand-picked exponent, explicitly not offered as a tightening of F196/F241's $0.10$-dex figure, and flagged using F241's own stated standard for treating such near-hits with suspicion. Between those two lies the adoption question, which this finding poses honestly rather than resolves: sequestering's core mechanism is structurally well-suited to this model's specific problem, but adopting it as *the* mechanism would be a decision-level change to the model's gravitational action, not a conclusion a single finding is positioned to reach — CLAUDE.md's own project-structure decisions (1–7) were each established over multiple findings and a decision-level review, and this finding does not attempt to substitute for that process for what would be an eighth. K9 is therefore reported here as advanced from "no genuinely dynamical mechanism has been checked against this model's numbers" (F332's endpoint) to "one has, it structurally works for the reason required, and here is exactly what adopting it would cost" — an incomplete but real step, not a closure.

## 11. Files

- Module: `src/casim/engine/interactions/cosmology_lambda_sequestering.py`
- Registry record: `F367-cc-sequestering` in `tests/registry/interactions.yaml` (tier gate, 2 controls verified red-and-only-there)
- Results: `test-results/F367_cc_sequestering.json`
- Registered: `src/casim/engine/registry.py` (`interactions.cosmology_lambda_sequestering`)
- Claim card: `docs/claims/CL303-sequestering-selectivity-identity-not-adopted.md`

## Reviewed & corrected

**2026-09-04 - 23:40 -- attack pass (inline, 13-point checklist, `.claude/commands/review-finding.md`
protocol -- no cold subagent available against this device-mounted repo in this session, per
review-finding's own inline fallback):**

1. **Numerical claims re-run independently.** `run()` re-executed with fresh values; `0.6306`,
   `-0.0357` dex, and the exact rationals `3n`, `dresidual_dC=0` all reproduce bit-for-bit from the
   registry's own `test-results/F367_cc_sequestering.json`. PASS.
2. **Circularity check against F241's own excluded route (S6).** Verified F241 §3's own text
   (`findings/F241-*.md`) states the FEH route is circular because $R_\text{EH}$ is *defined* in terms
   of $\Omega_\Lambda$; confirmed §2's identity contains no such self-reference (checked the sympy
   expression tree directly -- `C` and `V4` are the only free symbols besides `n`, `p`, `rho_m0`, none
   of which is $\Omega_\Lambda$ or a proxy for it). PASS.
3. **"Unbounded selectivity" claim stress-tested.** Confirmed numerically (not just symbolically) at
   $C/\rho_{m0}\in\{0,1,10^{60},10^{120}\}$: residual unchanged to float64 precision at every value.
   Added as an explicit numerical spot-check note in §2 (was previously asserted from the symbolic
   result alone). **WEAKENS -> fixed**: the finding's first draft did not mention this numerical
   cross-check; added.
4. **S1's "not blocked by shared origin" argument attacked directly.** Tried to construct a
   counterexample where sequestering's IR-level action on $\Lambda$ implicitly also constrains $G$
   through the multiplier sector's own consistency (e.g. if $\sigma$'s equation of motion involved $R$
   as well as $\Lambda$ in the general KP construction) -- the *specific*, minimal linear-coupling
   version cited here (coupling to $\int\sqrt{-g}\Lambda$ alone) does not have this feature, but the
   general KP papers admit non-linear coupling functions $f(\Lambda/\mu^4)$ that could in principle
   entangle sectors further. **WEAKENS -> not fixed, flagged**: added falsifier 3 explicitly naming
   this as the single most attackable step, rather than silently assuming the minimal linear case is
   representative of "the mechanism" in general.
5. **Checked the module's controls actually fire as claimed.** Re-ran `casim test --control --id
   F367-cc-sequestering` after the fixes above: both controls verified red-and-only-there, unchanged.
   PASS.
6. **Checked for overclaim in the header/status line against §7's honest-scope section.** First draft
   of the Status line read "closes K9's dynamics gap"; corrected to "positive on the core selectivity
   claim... negative/honest on adoption," matching §7's actual conclusion. Fixed before this was ever
   externally visible (caught in the same authoring pass, not a separate review finding).
7. **Checked exactness classification per constant.** `exactness: quantitative` on the registry record
   is right for the overall record (mixes the exact §2/§5-coefficient results with the quantitative
   §5-comparison number and the structural §3/§4/§6 citations) -- matches F332's own precedent of
   registering a mixed-exactness finding under its dominant/weakest-link class. PASS.
8. **Checked `casim index`, module registry, and test registry all green** after every edit (§ this
   session's own tool output): `casim index` reports max F366 pre-write (clean, no collision), module
   registry 251/250 covered, `casim test --id`/`--control` both pass. PASS.
9. Re-read F332 in full to confirm no restatement of an already-closed channel; confirmed this finding
   builds the *third*, previously-unbuilt channel type, not a rehash of K1-K4. PASS.
10. Re-read F241 in full to confirm the "why now" framing and the numerology-caution standard were
    applied consistently (not just gestured at) in §5 and §6. PASS.
11. Checked the claim card's `status: contingent` is the correct closed-vocabulary value (not `open`,
    which would imply the evidence for the *stated* claim is incomplete, when actually the claim IS the
    contingency) -- confirmed against `docs/claims/README.md`'s vocabulary table. PASS.
12. Checked no existing finding or claim already covers this exact ground (searched
    `findings-index.md` for "sequestering", "Kaloper", "Padilla" -- only F332's citation, no prior
    build). PASS.
13. Checked the session-claims.yaml topic claim matches what was actually done (not broader or
    narrower). PASS.

**Verdict: CONFIRMED-NARROWER.** Two WEAKENS, both addressed: one by adding an explicit numerical
cross-check (item 3), one by adding falsifier 3 to name the general-coupling-function caveat explicitly
rather than silently assuming the minimal linear case generalizes (item 4). No FAIL. Both declared
controls re-verified unchanged after the fixes.
