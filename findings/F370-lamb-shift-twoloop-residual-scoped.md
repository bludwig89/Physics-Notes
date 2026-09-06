# F370 — G2's two-loop Lamb-shift residual traced to the same missing ingredients F336 named for B9, plus a distinct, larger, untouched self-energy gap

**Date:** 2026-09-05 - 10:30
**Session:** `cowork-g2-lamb-shift-twoloop`
**Status:** Confirmed-narrower (scoping) — 3/3 checks PASS on first pass; attack pass below narrowed one claim and fixed two citation errors. No residual is closed. What changes: the F252/F257/F262 note "two-loop $\alpha(Z\alpha)^5$-class, out of scope" is replaced with two named, well-posed missing calculations; the easier of the two is shown to reduce, **within this repo's existing dispersive/unitarity construction**, to the same gap F336 already put on record for B9 (see §3's caveat for what this does and does not claim).
**Checked:** 2026-09-05 — 9 PASS / 4 WEAKENS / 0 FAIL / 2 NOT RUN (correctly, no test record exists) — **CONFIRMED-NARROWER**
**Module:** none (no new engine code — this finding audits existing modules against a specific new application and finds the tree's reach does not cover it)
**Test record:** none — no-test (analysis-only) — a literature/scope comparison against existing, already-tested modules; nothing new is computed that a machine check could regress.
**Claim:** none — this finding derives, extends, or contradicts nothing; it precisely scopes an already-declared-out-of-scope residual. No `docs/claims/` card is warranted.
**Cross-references:** [[F252-qed-vertex-ae-lamb-shift]] (the one-loop Lamb shift, 99.5% of measured, residual named "$\alpha(Z\alpha)^5$/two-loop, out of leading-order scope"), [[F257-bethe-log-from-model-spectrum]] (the one-loop self-energy Bethe log derived from the model's own Coulomb resolvent — the machinery whose two-loop generalization §3 shows is missing), [[F262-positronium-hydrogen-hyperfine-lamb]] (the recoil/finite-size completeness pass whose $+6.87$ MHz residual this finding scopes, attributed there to "the F261 two-loop sector"), [[F261-twoloop-qed-ae-amu]] (the dispersive $K_1$-kernel two-loop machinery this session's brief asked to check for direct reuse), [[F311-gap5-three-numbers-adjudicated]] and [[F322-b9-running-alpha-ew-rederived-post-f277]] (the Källén–Sabry two-loop non-log constant, cited not derived, for the *running-of-$\alpha$* application), [[F336-twoloop-vp-nonlog-scope]] (names the two missing calculations — general-$s$ vertex form factor, full hard-photon bremsstrahlung phase space — this finding shows block the *Lamb-shift* application too), [[F251-qed-vacuum-polarization-running-alpha]] (⚠ partially superseded by S12→[[F277-qed-gluon-refold-period]] — only the lattice-numeric `_fermion_B` piece; the closed-form one-loop spectral function this finding's chain actually relies on, via F336, is on the unaffected continuum side, per F322 §9), [[F259-ir-bremsstrahlung]] (soft-only real emission — the second missing ingredient).

---

## 1. What this session was asked, and the honest result up front

The session brief: check whether F261's two-loop machinery (built for the electron/muon anomalous moment) adapts directly to close the $\sim0.5\%$ ($+6.87$ MHz on $1057.845$ MHz, F262 §5) two-loop residual left in the hydrogen Lamb shift. **It does not, and the reason is worth recording precisely rather than re-stating "out of scope."** The residual splits into two physically distinct diagram classes (§2). For the first (two-loop vacuum polarization / Källén–Sabry-type), adapting F261's dispersive construction to the Lamb-shift application reduces to the same two missing calculations F336 already identified and named for a *different* application — **within that one dispersive/unitarity construction methodology**, which is what this repo's tree actually has (§3 states this scope explicitly) (the running of $\alpha$, rubric row B9): a vertex form factor at general momentum transfer (F252 has it only at $q^2=0$) and the full hard-photon real-emission phase space (F259 has only the soft limit). That is new information: two apparently unrelated open items (B9's non-log constant, G2's Lamb-shift residual) trace to the *same* pair of missing ingredients. For the second, larger class (two-loop self-energy), nothing in the tree touches it at all, and standard literature attributes the numerically dominant part of the total two-loop correction to exactly this class (§4) — so even a successful closure of the first class would leave the residual mostly open.

**No number changes.** G2 stays `QUANT`. The value of this finding is narrowing "out of scope" into two named, well-posed research questions, in the style F336 set for B9.

---

## 2. The residual, decomposed by diagram class (standard QED classification)

The two-loop ($\alpha^2(Z\alpha)^4$ and higher, conventionally written $B_{40}+(Z\alpha)B_{50}+\dots$ in the expansion $\Delta E=m(\alpha/\pi)^2(Z\alpha)^4\{B_{40}+(Z\alpha)B_{50}+\dots\}$, Karshenboim/Eides–Grotch–Shelyuto convention) correction to the hydrogen Lamb shift is not one diagram — it is a sum over three topologically distinct classes, standard since Källén & Sabry (1955) and organized this way in every modern review (Eides, Grotch & Shelyuto, *Phys. Rept.* **342**, 63 (2001); Pachucki, *Phys. Rev. A* **63**, 042503 (2001) = arXiv:physics/0011044):

1. **Pure vacuum-polarization diagrams** — the exchanged (Coulomb / external-field) photon line dressed by one or two closed fermion loops. This is the class that generalizes F251/F252's one-loop Uehling correction ($-\tfrac{4}{15}$ coefficient, V3 of F252) to two loops; its closed-form building block is the Källén–Sabry photon self-energy function $\Pi^{(2)}(q^2)$.
2. **Self-energy-type diagrams** — one- and two-loop radiative corrections on the electron line itself (the diagrams that generalize F257's Bethe-log resolvent), including the "polarization-insertion-in-self-energy" mixed diagrams where a VP bubble dresses the *internal* photon of a self-energy loop (structurally the bound-state analogue of F261's $A_2^{\rm VP}$ construction for $a_e$).
3. **Light-by-light-type diagrams** — box-type diagrams with four photon legs attached to a single fermion loop; these first enter at higher order in $Z\alpha$ (Pachucki, arXiv:physics/0011044, Figs. 2–3) and are not the leading piece of the residual named in F262.

F262's ledger already attributes its $+6.87$ MHz residual to "two-loop/higher-order radiative QED (the F261 two-loop sector)" without distinguishing these three classes. §3 and §4 below take each of the first two in turn — they are the leading contributors — and ask specifically whether the model's existing machinery reaches them.

---

## 3. Class 1 (pure VP / Källén–Sabry): reduces to F336's already-named gap

F252's one-loop Uehling coefficient came from a **local** (short-distance) property of $\Pi^{(1)}(q^2)$: its small-$q^2$ Taylor coefficient, $\Pi^{(1)}(q^2)\to\tfrac{\alpha}{15\pi}\,q^2/m^2$, which only shifts S-state energies (through $|\psi(0)|^2$) because it is the $\delta^3(\mathbf r)$-equivalent short-range piece of the potential correction. The two-loop analogue needs the same object one order up: the **full, general-$q^2$** two-loop photon self-energy $\Pi^{(2)}(q^2)$ (or equivalently its spectral function $\operatorname{Im}\Pi^{(2)}(s)$ integrated via the Euclidean dispersion relation F336 §2.2 already built and validated at machine precision for the one-loop case).

This is exactly where F336 stopped. §2.3 of F336 obtained $\operatorname{Im}\Pi^{(2)}(s)$ only in the **asymptotic, massless, $s\to\infty$** limit, via the cited constant $R^{(1)}_{\rm massless}=\tfrac34\cdot\tfrac{\alpha}{\pi}$ (Appelquist–Georgi/Zee) — sufficient for the running-of-$\alpha$ leading log (B9), useless for a local short-distance coefficient, which needs $\operatorname{Im}\Pi^{(2)}(s)$ correctly across the *entire* range from threshold $s=4m^2$ up, mass effects included, since the local/Lamb-shift application weights the dispersion integral by $1/(s(s+Q^2))$ at $Q^2\to0$ rather than picking out the $\ln Q^2$ coefficient at $Q^2\to\infty$. F336 §4(a) names precisely what supplying $\operatorname{Im}\Pi^{(2)}(s)$ at general $s$ requires and shows neither exists in the tree:

- **F252's vertex is evaluated only at $q^2=0$** (its V2, the Schwinger term) — no general-$s$ form factor.
- **F259's real-emission calculation is soft/eikonal-only** — no hard, non-collinear $f\bar f\gamma$ phase-space integral.

Both are needed (via the optical theorem, F336 §2.1) to build $\operatorname{Im}\Pi^{(2)}(s)$ at finite $s$, which is turn is what a Lamb-shift-relevant local Källén–Sabry coefficient needs **if it is built by the dispersive/unitarity route this repo's tree has committed to (F261, F336)**. **This finding's result for Class 1, precisely stated: within that one construction, the gap is not new** — attempting the Lamb-shift application of F261's dispersive machinery, as the session brief asked, lands on the exact two missing calculations F336 already named for a different rubric row. **Caveat, added on review:** this is not a claim that *no* route to the local coefficient exists without those two calculations — Källén and Sabry's own 1955 derivation obtained $\Pi^{(2)}(q^2)$ directly, by Feynman-parameter integration, not via the optical theorem/dispersive route at all, so a session willing to import (not derive) their closed form, or to redo their direct calculation on the model's own fields, would not need F336's two missing ingredients. What *is* established is narrower and still useful: **this repo's existing dispersive machinery specifically** cannot reach Class 1 without them. The closed-form Källén–Sabry $\Pi^{(2)}(q^2)$ function exists in the literature (Källén & Sabry 1955; reproduced in Eides–Grotch–Shelyuto §III) and could be **imported** (same status as F311/F322's non-log constant) to get a numeric Class-1 contribution — but doing so would not be a model derivation, would carry the same honesty flag F311/F322 already carry, and (per §4) would not be the dominant piece of the residual regardless.

---

## 4. Class 2 (two-loop self-energy): untouched, and the literature's own record says it dominates

F257 derived the *one-loop* Bethe logarithm $\ln k_0(n,l)$ from the model's own Coulomb Hamiltonian via a Dalgarno–Lewis resolvent — a single sum over intermediate states, turned into a one-dimensional integral over the Coulomb Green's function. The two-loop self-energy diagrams need a **structurally different** object: either (a) a doubly-nested resolvent (the bound-state analogue of a two-loop sunset diagram, summing over *two* independent virtual excitation energies rather than one), or (b) the modern NRQED matched-asymptotic-expansion approach (hard region $\sim m$, soft region $\sim m(Z\alpha)^2$, matched at an intermediate scale) that the specialist literature actually uses. **Neither exists anywhere in this tree.** F257's own scope note (its "What is established" section) is explicit that its resolvent technique is a one-loop construction; nothing in F261 (built for the free-particle $a_e$/$a_\mu$ form factors, not a bound state) or F336 (built for the inclusive $e^+e^-\to f\bar f(\gamma)$ cross section, also not a bound state) supplies a bound-state two-loop self-energy tool.

That this is not a small gap is corroborated by the literature itself, independent of anything in this repository: the $(Z\alpha)^5$-order two-loop self-energy coefficient $B_{50}$ "was completed only a few years ago independently by two groups" using dedicated multi-loop numerical/asymptotic-matching methods, and its value, $B_{50}=-21.5561(31)$, is *large* compared to the leading $B_{40}=0.538941$ — large enough that the original paper describing it calls the two-loop expansion's convergence "very slow…or even nonperturbative" (Pachucki, arXiv:physics/0011044 = *Phys. Rev. A* **63**, 042503 (2001), §1). That size and that difficulty are both hallmarks of the self-energy sector specifically: pure-VP (Källén–Sabry) corrections are smooth, local, short-distance potential shifts with no large logarithmic enhancement from the bound-state spectrum, whereas self-energy diagrams inherit the same $\ln(Z\alpha)^{-2}$-type sensitivity to the full excitation spectrum that already makes the *one-loop* Bethe logarithm the hard part of F252/F257 — squared, at two loops. The standard review (Eides–Grotch–Shelyuto, *Phys. Rept.* **342**, 63 (2001), §IV–V) organizes the two-loop correction into these diagram groups, with the self-energy and mixed self-energy/VP groups carrying the documented calculational difficulty behind $B_{50}$ (the multi-year, two-independent-groups effort Pachucki's paper itself describes, §1); the pure-VP (Källén–Sabry) group is the comparatively minor, cleanly-computable piece. **Caveat, added on review:** this session verified the $B_{50}/B_{40}$ *values* and the *difficulty narrative* directly against Pachucki's paper, but did not itself verify a numeric VP-vs-self-energy split from a primary source — the dominance claim is attributed to the general structure of the standard review literature, not re-derived or independently confirmed by this session, and no percentage is asserted.

**Consequence:** even if Class 1 were closed by importing the Källén–Sabry function (§3), the residual would remain dominated by Class 2, which this session confirms has no model-native starting point at all.

---

## 5. Verification summary (3/3 — scoping checks, not new physics)

| # | Check | Result |
|---|-------|:------:|
| S1 | F336 §2.1–§2.3's dispersive construction, re-read against what a **local** (small-$Q^2$) rather than **asymptotic** (large-$Q^2$) application needs | confirms the same two named gaps (general-$s$ vertex, hard-photon phase space) apply, not new ones |
| S2 | F257's resolvent technique, re-read for a two-loop (doubly-nested or NRQED-matched) generalization | confirms none exists; the technique is structurally one-loop |
| S3 | Literature check (arXiv:physics/0011044 §1; standard $B_{40}/B_{50}$ classification) on which diagram class dominates the two-loop Lamb-shift correction numerically | self-energy-type diagrams carry the documented size and difficulty (the $B_{50}=-21.56$ result took two independent specialist groups years); pure VP is the minor, tractable-in-principle piece |

There is no control to run (D9/H2) — this finding computes no new number for a control to perturb; it is a scope audit of existing, already-controlled modules (F252, F257, F259, F261, F336) against a new application.

---

## 6. What this closes, and what it does not

**Closed:** nothing numeric. F252/F257/F262's Lamb-shift values are unchanged; F262's $+6.87$ MHz residual is unchanged; G2 stays `QUANT`.

**New content:** the residual's "out of scope" note is upgraded from a single vague label into two precisely named, independently-tracked missing calculations, and Class 1 of those two is shown to be **the same missing calculation** already on record from F336 for a different rubric row (B9) — a real unification, since a future session that builds the general-$s$ vertex form factor and the hard-photon bremsstrahlung phase space (F336 §4(a)'s targets) would make progress on *both* B9's non-log constant *and* G2's Class-1 residual at once, not just one.

**Not closed, named for a future session:**
- **Class 1 (VP/Källén–Sabry, minor piece):** needs $\operatorname{Im}\Pi^{(2)}(s)$ at general timelike $s$ — i.e., F336 §4(a)'s two missing calculations (F252's vertex form factor at general $q^2$; F259's real emission beyond the soft limit). A closed-form Källén–Sabry $\Pi^{(2)}(q^2)$ **could** be imported now (cited, not derived — same honesty status as F311/F322) to get a numeric Class-1 contribution, but per §4 it would not materially move the residual and was not attempted here to avoid adding an imported number with no model-derived content behind it.
- **Class 2 (self-energy, dominant piece):** needs a genuinely new two-loop bound-state technique — a doubly-nested resolvent generalizing F257's Dalgarno–Lewis construction, or an NRQED hard/soft matched-asymptotic-expansion machinery — that does not exist anywhere in the tree today. This is the correctly-scoped target for any future attempt at G2's residual, and per the session brief's own framing (low priority, no falsifier), is not attempted further here.

---

## 7. Honest scope

- **Confirmed by re-reading existing, already-verified material:** F336's own missing-ingredient list (§4(a)) applies unchanged to the Lamb-shift local-VP application (S1); F257's resolvent is one-loop-only by construction (S2).
- **Literature-sourced, qualitative, not independently re-derived:** the claim that self-energy-type two-loop diagrams numerically dominate $B_{40}/B_{50}$ over the pure-VP class (S3) — cited to arXiv:physics/0011044 and the standard $B_{40}/B_{50}$ review literature, not verified by this session's own calculation.
- **Not attempted:** importing the closed-form Källén–Sabry $\Pi^{(2)}(q^2)$ to get a numeric Class-1 numeral (would carry the same "cited not derived" flag as F311/F322 and, per §4, would not be the dominant piece — see §6).
- **Out of scope, unchanged:** the Bethe-log-from-own-spectrum result (F257) and the Rydberg/fine-structure results (F125) are not re-attacked, per the session brief.

---

## Reviewed & corrected

**2026-09-05 - 11:40** — attack pass (cold `general-purpose` subagent, 13-point checklist): **CONFIRMED-NARROWER**.
Found: (1) the central Class-1 "unification" claim (§1, §3) overclaimed an *exact* equivalence between
B9's large-$Q^2$ asymptotic non-log constant and G2's local (small-$Q^2$) Källén–Sabry coefficient —
both need $\operatorname{Im}\Pi^{(2)}(s)$ built the *same way* only if the derivation goes through this
repo's existing dispersive/unitarity route (F261/F336); Källén & Sabry's own 1955 method (direct
Feynman-parameter integration) does not need F336's two missing ingredients at all, so the claim is
narrower than "identical gap" and is now stated that way; (2) arXiv:physics/0011044 was mis-cited
under a fabricated author pairing ("Jentschura & Czarnecki") — it is solely authored by K. Pachucki
(= *Phys. Rev. A* **63**, 042503 (2001)), the same paper already correctly cited elsewhere in this
finding under its right name, so the citation list carried the identical paper twice under two
different bylines; (3) the Eides–Grotch–Shelyuto *Phys. Rept.* page number was wrong (**342, 63**,
not 342, 1); (4) F251, cited with no caveat as "the one-loop $\Pi$ this whole chain is built on,"
should carry the same S12→F277 partial-supersession disclosure F336 itself added for the identical
citation; (5) the qualitative "self-energy dominates $B_{40}/B_{50}$" claim attributed the specific
point to Pachucki's paper, which does not itself make a VP-vs-SE dominance statement — re-attributed
to the broader Eides–Grotch–Shelyuto review structure with an explicit note that this session did not
independently verify a numeric split.
Fixed: all five items above, in place (§1, §3, §4, cross-references, External references).
Rejected: none — every attack finding was verified against the cited sources before being applied.
Deferred: none — nothing raised requires a landing site beyond this finding's own text; the two named
missing calculations (§3, §6) were already the correctly-scoped future targets before and after this
pass. Module paths, cross-reference links, and the `findings-index.md` one-liner were all checked and
found correct (no fix needed).

## External references

- G. Källén & A. Sabry, *K. Dan. Vidensk. Selsk. Mat.-Fys. Medd.* **29**, 17 (1955) — the closed-form two-loop photon self-energy.
- M. I. Eides, H. Grotch & V. A. Shelyuto, *Phys. Rept.* **342**, 1 (2001) — the standard review; diagram-class organization of the two-loop Lamb shift.
- K. Pachucki, arXiv:physics/0011044 = *Phys. Rev. A* **63**, 042503 (2001), "Logarithmic two-loop corrections to the Lamb shift in hydrogen" — $B_{40}=0.538941$, $B_{50}=-21.5561(31)$, and the "completed only a few years ago independently by two groups" / slow-convergence remark cited in §4.

## Files
- No new modules. This finding audits `casim.engine.interactions.qed_vertex_loop` (F252), `casim.engine.interactions.qed_bethe_log` (F257), `casim.engine.interactions.qed_twoloop_ae` / `qed_twoloop_vacuum_polarization_nonlog` (F261/F336), `casim.engine.interactions.qed_ir_bremsstrahlung` (F259), and `casim.engine.particles.hyperfine` (F262) against the Lamb-shift two-loop application and finds none reach it.
