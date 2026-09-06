# F344 — The adopted BCC free-Weyl walk's exact point symmetry is $D_{2h}$ under unitary covariance and $D_{4h}$ once time-reversed ($A\to A^\dagger$) covariance is admitted — never $O_h$: unitarity and $C_3$ covariance of the $T_{2g}$ sector are exactly incompatible, so $O_h$ is an exact *infrared* symmetry of the walk (broken at $O(k^2)$ by a closed-form defect) — which closes the free walk as a candidate for F342's condition-(i) escape hatch

**Date:** 2026-08-31 - 21:09
**Numbering:** **F344** (`casim index` NEXT FREE NUMBER, max F343, no gaps — max+1, no declaration needed).
**Status:** **Confirmed — 11/11 legs PASS, exact.** Independently re-derived from a claim card alone by a cold agent using a different parameterisation (see `docs/reviews/F344-review-2026-09-01.md`), which reproduced every number and forced one narrowing, now applied: **the covariance group depends on which criterion is used, and both are reported.** Under $A(gk)=UA(k)U^\dagger$ with $U$ unitary and $R\in SO(3)$ the group is $D_{2h}$, order **8**; admitting the eight elements that realise $A(gk)=UA(k)^\dagger U^\dagger$ instead (det $R=-1$, i.e. rotation accompanied by step reversal / chirality exchange) gives $D_{4h}$, order **16**. Neither is $O_h$, and the $C_3$ exclusion is the same under both. Every leg but one is pure integer arithmetic on the eight-dimensional monomial basis $\{c,s\}^{\otimes3}$ (no floats, no fitting); the remaining leg cross-checks all 16 covariant elements against the shipped `_bcc_uvec` at residual **exactly 0.0** over 240 $k$-samples. Two declared negative controls verified (`casim test --id F344-bcc-walk-point-symmetry --control`).
**Module:** `src/casim/engine/lattice/bcc_point_symmetry.py` (new).
**Checked:** 2026-09-01 - 15:20 — hybrid review (genuine cold-subagent blind re-derivation from a claim card alone, which reproduced every number by a different parameterisation; the adversarial-referee subagent was terminated by an account spend limit, so attacks 1–13 were completed inline by the authoring session and are correspondingly weaker), 9 PASS / 3 WEAKENS / 0 FAIL / 1 PARTIAL — **CONFIRMED-NARROWER**. Both narrowings applied: the 16-vs-8 criterion split is now in the title, and falsifier 2 was rewritten after the review found it pointed at the retired `gauge.bilinear`. See `docs/reviews/F344-review-2026-09-01.md`.

**Builds on:** [[F26-speed-of-light-as-rotation-rate]] (the walk's leading-order Weyl limit $H_W=\sigma\!\cdot\!k/\sqrt3$, whose covariance this finding *confirms*), [[F30-photon-dispersion-order-anisotropy-birefringence]] (the independent, closed, exact anisotropy of $\omega=\arccos u$ — untouched here, and logically disjoint: $u$ carries no spin structure), [[F342-generation-identification-condition-i-vacuous]] (§5/§7, the condition-(i) escape hatch this finding closes), [[F291-why-three-plus-one-dimensions]] (the named weak link: "the lattice's isotropy group … is a premise, not something proved here"), [[F302-sigma-bilinear-so3-covariance]] (the $\varepsilon=i\sigma_2$ mechanism — invoked here and shown *not* to be the explanation), [[F75-three-generations-from-bcc-irrep-selection]] (the $T_{1u}$/$T_{2g}$ shell irreps whose labels this finding shows cannot be carried over to the walk).
**Test record:** `F344-bcc-walk-point-symmetry` (tier **gate**, sector lattice, `kind: assertion`, `expect.exactness: exact`, `tol: 0`).
**Claim:** none — pending. The result is a statement about the model's own internal lattice symmetry, not yet about a measured quantity; a card is owed only if the $D_{4h}$ residual symmetry is ever propagated to an observable (see §7, falsifier 2). Session `careful-noether-wigner`, `docs/design/session-claims.yaml`.

---

## 1. The question, and the hand-off that produced it

A prior session, attacking F342's constructive escape hatch (rubric C1 — exhibit an $O_h$-invariant coupling in the adopted engine that is *not* diagonal in the site basis), proposed the free Weyl walk itself as the candidate: it is BDPT-forced, already adopted, manifestly non-diagonal, and its momentum-space vector $\tilde{\mathbf n}(k)$ mixes $T_{1u}$ content at $O(k)$ with $T_{2g}$ content at $O(k^2)$. If that mixing were an honest $O_h$ statement, an RG-relevance argument would follow: $T_{1u}$ relevant, $T_{2g}$ irrelevant, generation triplet selected.

That session stalled on a covariance test that failed at **leading** order — which should have been impossible, since $H\to\sigma\!\cdot\!k/\sqrt3$ is cited from F26 onward. Three leads were named: (a) the branch label moves under proper rotations; (b) an F302-style Pauli-basis artifact; (c) plain active/passive bookkeeping.

This finding answers all three, and then answers the question they were in service of.

## 2. Setup: the walk in a basis that makes the question finite

Write the shipped object (`bcc._bcc_uvec`, Paper 1 Eq. 15) in the eight monomials of $\{c_i,s_i\}$, $c_i:=\cos(k_i/\sqrt3)$, $s_i:=\sin(k_i/\sqrt3)$:

$$A^s(k)=u^s(k)\,\mathbb I-i\,\boldsymbol\sigma\cdot\mathbf n^s(k),\qquad
u^s=\alpha\,c_xc_yc_z+\beta\,s_xs_ys_z,\qquad
n^s_a=p_a M^{(1)}_a+q_a M^{(2)}_a,$$

with $M^{(1)}_a$ the monomial carrying $s$ in slot $a$ and $c$ elsewhere (the $O(k)$, $T_{1u}$-labelled monomial) and $M^{(2)}_a$ the monomial carrying $c$ in slot $a$ and $s$ elsewhere (the $O(k^2)$, $T_{2g}$-labelled one). The shipped convention is $\alpha=1$, $\beta=s$, and

$$p=(+1,\,-s,\,+1),\qquad q=(-s,\,+1,\,+s).$$

Each coefficient is a sign that may depend on the branch label $s=\pm1$, i.e. one of $\{+1,-1,+s,-s\}$ — four possibilities each, $4^6=4096$ assignments in all.

**Unitarity pins the coefficients to $\pm1$ (leg C1, exact).** The eight squared monomials, rewritten in $x_i:=c_i^2$ (so $s_i^2=1-x_i$), are the eight products $\prod_i(x_i\text{ or }1-x_i)$ — the indicator basis of the multilinear polynomials in three variables, of exact rank $\mathbf 8$ over $\mathbb Q$ (computed by fraction-free elimination in the module). Hence $\sum_m\lambda_m(\text{monomial}_m)^2=1$ forces every $\lambda_m=1$: no coefficient of $u$ or $\mathbf n$ may have modulus other than 1. What remains is the single cross-term condition

$$\alpha\beta+\sum_a p_aq_a=0\qquad\Longleftrightarrow\qquad \sum_a p_aq_a=-s .$$

So the sweep over $\{+1,-1,+s,-s\}^6$ is **exhaustive over all real-coefficient walks of this form**, not a guessed family: 576 of the 4096 assignments are unitary. (Rank 8 and the unique solution $\lambda_m\equiv1$ were re-verified independently in `sympy`.) *Scope, stated at its true width:* complex coefficients add nothing **when** $\mathbf n$ is a phase times a real vector — then $\bar{\mathbf n}\times\mathbf n=0$, unitarity forces the phases equal mod $\pi$, and $A$ is a global phase times the real form — but a genuinely complex $\mathbf n$ ($\bar{\mathbf n}\times\mathbf n\neq0$) is **not excluded here** and rests on BDPT's own uniqueness statement, not on this finding. (This is also the precise reason the `_bcc_uvec` comment's transcription check — "$u^2+|\mathbf n|^2=1$ only with the corrected sign" — fixed the source typo but could not have detected an overall sign flip on any single component: only the *products* $p_aq_a$ enter.)

## 3. Lead (a) is real, and it is the whole cause of the apparent leading-order failure

For $g\in O_h$ a signed permutation with signs $\varepsilon_i$ and permutation $\pi$,

$$u^s(gk)=u^{\,\tau_g(s)}(k),\qquad \tau_g(s)=s\cdot\textstyle\prod_i\varepsilon_i ,\qquad \prod_i\varepsilon_i=\det(g)\,\mathrm{sgn}(\pi).$$

Verified as an exact monomial identity for all 48 elements and both branches (leg C2). **Exactly 24 of the 48 elements swap the chirality branch**, and the 24 that preserve it form $T_d$ — not $O_h$. The 90° rotation about $z$ used by the stalled session, $R_z$, has $\prod\varepsilon=-1$: it is a *proper* rotation that nevertheless swaps branches (leg C2b). Testing $H(R_zk)$ against $U H(k)U^\dagger$ at **fixed** branch is therefore not a weakened test — it is the wrong test, and it fails at the first order at which anything is nonzero. Lead (a) is confirmed, and it dissolves the reported leading-order failure exactly as the hand-off guessed.

**Leads (b) and (c) are *not* the explanation, and the code needs no change.** With the branch map applied, the leading term is $\mathbf n=\mathrm{diag}(p)\,\mathbf k/\sqrt3+O(k^2)$ with $p_a=\pm1$, so $\mathbf n(gk)=(SgS^{-1})\mathbf n(k)$ with $S=\mathrm{diag}(p)$: an honest $SO(3)$ map for every proper $g$, for **every** admissible convention (leg C7 — the $O(k)$ truncation is covariant under all 48). The shipped $n_y$ sign is not a bug: $\det\mathrm{diag}(p)$ is $-1$ on the $+$ branch and $+1$ on the $-$ branch, i.e. the two branches carry **opposite leading-order chirality**, which is what the module's own docstring asserts and what two Weyl branches must do. The "tidier-looking" conventions with $p=(+1,+1,+1)$ give both branches the *same* chirality and are physically wrong. `_bcc_uvec` is correct as written.

> **The hand-off's high-priority falsification branch does not obtain.** The walk *is* $O_h$-covariant at leading order. The model's claimed leading-order isotropy, cited from F26 onward, stands untouched.

## 4. The result: the exact covariance group is $D_{2h}$ (unitary) / $D_{4h}$ (step reversal admitted), and no convention does better

**Two premises, stated before the answer.** (i) $R$ and $U$ are **$k$-independent**. Without this the question is vacuous: $\omega=\arccos u$ *is* fully $O_h$-covariant (leg C2 — the branch map is the whole of its transformation), so a $k$-dependent $U$ diagonalising $A$ pointwise exists for all 48 elements and says nothing. The entire content of $L$ is $k$-independence. (ii) $u$ must transform too, not only $\mathbf n$ — $UAU^\dagger$ cannot move the identity component — which is what forces the branch map of §3 rather than leaving it a free knob.

Define, frame-independently (the $SO(3)$ image of a spin lift is fixed only up to $\mathbf n\to S\mathbf n$, which conjugates $R$, and $\det R$ is invariant under that; so *existence* of $R$, not $R=g$, is the frame-invariant question, while $\det R$ is a frame-invariant grading of the answer):

$$L:=\{g\in O_h:\ \exists R\in O(3),\ \ \mathbf n^s(gk)=R\,\mathbf n^{\tau_g(s)}(k)\ \}.$$

Because $\mathbf n_a(gk)$ is supported on exactly the two monomials of $\mathbf n_{j(a)}$, $R$ is forced to be the signed permutation carrying $g$'s permutation, and each of its three entries is over-determined (two monomials, one unknown). The test is finite, exact and has no free choices.

| | shipped walk | best over all 576 unitary conventions |
|---|---|---|
| $\lvert L\rvert$, $R\in O(3)$ (rotation, step reversal allowed) | **16** ($D_{4h}$; 4-fold axis $z$) | **16** — never more |
| proper elements of $L$ | 8 | 8 |
| $\lvert L\rvert$, $R\in SO(3)$ (**unitary** covariance, $\ker(g\mapsto\det R)$) | **8** ($D_{2h}$) | 8 — never more |
| body-diagonal $C_3$ rotations in $L$ | 0 of 8 | **0 of 8, in 0 of 576 conventions** |
| $\lvert L\rvert$ for the $O(k)$ truncation | 48 | 48 |

$L$ is closed, $g\mapsto R_g$ is a homomorphism, and $L$ leaves exactly one coordinate axis invariant: **$L\cong D_{4h}$, order 16 of 48** (legs C3, C5).

**But $L$ splits, and the split is frame-invariant.** Only 8 of the 16 have $\det R=+1$; those, and only those, are implementable as $A(gk)=U A(k)U^\dagger$ with $U$ unitary, and they form $\ker(g\mapsto\det R)$ — the eight diagonal sign matrices, i.e. **$D_{2h}$, order 8**, with all three axes invariant and no tetragonal character (leg C4). The other 8 (the $(xy)$-transposition coset, $C_{4z}$ among them) have $\det R=-1$ on both branches with no branch choice repairing it, and $\det R$ is invariant under the spin-frame change $\mathbf n\to S\mathbf n$, so no reframing converts them. They realise instead

$$A(gk)=U\,A(k)^\dagger\,U^\dagger\qquad(\text{verified independently at residual }5.7\times10^{-16};\ \text{the }UAU^\dagger\text{ form fails at residual }1.97),$$

i.e. rotation accompanied by **step reversal**, equivalently the F302 $\varepsilon=i\sigma_2$ route $\varepsilon A^\dagger\varepsilon^{-1}$ — chirality exchange, the expected behaviour of such operations on a chiral field, but *not* a symmetry of the forward dynamics. **So: unitary covariance group $D_{2h}$ (8/48); $D_{4h}$ (16/48) only if time-reversed covariance is admitted.** The $C_3$ exclusion below is unaffected — the body diagonals admit no $R$ at all, proper or improper.

**The obstruction, in one line.** $C_3$ covariance requires $p_aq_b=p_bq_a$ for all $a,b$; with the $p_a$ equal (leading-order isotropy) that forces $q_x=q_y=q_z=q$, whence $\sum_ap_aq_a=3q=\pm3$, while unitarity demands $\mp1$. **Unitarity and $C_3$ covariance of the $T_{2g}$ sector are mutually exclusive** — the three $T_{2g}$ coefficients cannot all agree, so one axis is always singled out. Sweeping all 576 unitary conventions finds a $C_3$ in $L$ for **zero** of them (leg C5).

**The defect is closed-form (leg C6).** For the 120° rotation about $(1,1,1)$,

$$\mathbf n_x(C_3k;s)-\mathbf n_z(k;s)=(q_x-q_z)\,M^{(2)}_z=-2s\,s_xs_yc_z ,$$

exactly, on both branches — pure $T_{2g}$ monomial, no $T_{1u}$ or $A_{1g}$ admixture. It is $O(k^2)$ absolute and therefore $O(k)$ *relative* to $\lvert\mathbf n\rvert\simeq\lvert k\rvert/\sqrt3$.

**Cross-check against the shipped code (leg C8).** Using `_bcc_uvec` itself on 240 fixed $k$: every one of the 16 elements of $L$ satisfies $\mathbf n(gk)=R\,\mathbf n(k)$ at maximum residual **0.0** — the two sides are the same floats up to sign, so exact zero is structural and the *meaningful* content of the leg is that it is not $O(1)$: flipping a single entry of the derived $R$ gives residual $1.16$, and testing against the wrong branch target gives $0.95$. Robust to the $k$-sample: identical verdict and slope at 40, 240 and 900 samples. Minimising the residual over all 48 candidate $R$ and both target branches, the $C_3$ floor runs $1.016\times10^{-1}$, $1.028\times10^{-2}$, $1.026\times10^{-3}$, $1.026\times10^{-4}$ over $\lvert k\rvert\sim10^{-1}\ldots10^{-4}$ — decade ratios $9.886$, $10.020$, $10.002$, converging to exactly 10, i.e. **linear in $\lvert k\rvert$** across four decades, exactly as the closed form requires. The 4-fold rotation about $x$ fails identically while the one about $z$ is exact, confirming the distinguished axis is a real feature of the walk and not an artifact of the fit.

## 5. What this means for F342 / rubric C1 — the escape hatch is closed, with a reason

F342's hatch asks for an **$O_h$-invariant**, site-non-diagonal coupling in the adopted engine. The free walk is non-diagonal, but it is not $O_h$-invariant: it is $D_{4h}$-invariant, and the very term that would have carried the "$T_{2g}$" label is *the term that breaks $O_h$*. Consequently:

1. The walk's $O(k^2)$ piece is **not a $T_{2g}$ tensor of $O_h$**. Its monomials transform in the $T_{2g}$ *orbital* basis — that classification (the hand-off's item 2) is correct arithmetic and is not disputed — but the full spin-plus-orbital object of which they are the coefficients does not carry an $O_h$ representation at all. Labelling it "$T_{2g}$" is bookkeeping, not representation theory.
2. Therefore **no $O_h$ RG-relevance argument can be built on it.** "$T_{1u}$ is relevant, $T_{2g}$ is an irrelevant lattice correction to the same field" presupposes both are $O_h$ irreps of one covariant object. They are not. F75/F342's $T_{1u}$-vs-$T_{2g}$ question is an *exact* $O_h$ statement at the lattice scale, and at the lattice scale the walk's symmetry is $D_{4h}$ — it has strictly less structure than the question needs, not more.
3. So this angle is **closed, not merely unfinished**, and it is closed for a reason that also forecloses re-tries: the free walk cannot supply exact $O_h$ selecting power at *any* order in $k$, under *any* sign convention, because the only place it could come from is the $T_{2g}$ term whose coefficients unitarity forbids from being equal. F342's escape hatch remains open, but this candidate is spent. Record it so nobody re-attempts it.

## 6. What this means for F291's named weak link — a sharpening, in both directions

F291 flags "the lattice's isotropy group … is a premise, not something proved here — the weakest link in S1." This finding converts the premise into a measured statement for the one object that actually propagates:

- **Good news.** $O_h$ is an *exact infrared symmetry* of the adopted walk: the $O(k)$ truncation is covariant under all 48 elements (leg C7), and the covariance defect vanishes linearly in $\lvert k\rvert$ (leg C8). Continuum isotropy is not assumed — it is the exactly-characterised limit of a lattice law whose breaking term is known in closed form.
- **Bad news, stated plainly.** At the lattice scale the walk's exact point symmetry is $D_{2h}$ (8/48) under unitary covariance, $D_{4h}$ (16/48) if step-reversed covariance is admitted, and no reformulation of Eq. 15 removes it. Any argument that needs full $O_h$ *at the lattice scale* — F75's shell-irrep identification, F175's exact $O_h$ weights, F342's projector machinery — is resting on the **geometry of the 8-vertex shell and the on-site step**, not on the adopted dynamics. That is a legitimate footing (the shell really is a single $O_h$ orbit, F342 verifies it), but it is a *different* footing, and the two must not be quietly interchanged.

## 7. Falsifiers

1. **Exhibit a unitary BCC $s=2$ Weyl automaton, of any form, that is exactly $C_3$-covariant.** This finding proves impossibility only within the Eq. 15 monomial form (which BDPT state is the complete solution set modulo unitary conjugation — that uniqueness is the paper's, not this finding's, and is the one imported premise). A counterexample outside that form kills §4.
2. **Show the $D_{2h}/D_{4h}$ residual has an observable consequence.** The breaking sits in the spin texture at $O(k^2)$ with $\lvert\mathbf n\rvert$ and $\omega$ untouched, so it is invisible to every dispersion test (all of F30 included) and to the paired-photon rate $\Omega_\text{pair}$, which depends on $u$ alone. It is *not* obviously invisible to anything that consumes the full 2×2 walk rather than $\lvert\mathbf n\rvert$. The live consumers, checked against the current tree, are: `casim.lattice.chiral_core` (calls `_bcc_uvec` directly), `casim.engine.particles.dirac_bcc`, `casim.engine.core.blockspin`, `casim.engine.interactions.thermodynamics` and `casim.engine.particles.induced_stiffness` (all via `bcc_unitary`). **Note the target that is *not* on that list:** the $\sigma$-bilinear photon of `casim.engine.gauge.bilinear` was retired on 2026-06-01 (S1-F69) precisely for being *helicity$\leftrightarrow$branch birefringent*, and F302 showed its transpose form is not even an $SO(3)$ 3-vector — which reads, in hindsight, like the same entanglement of the branch label with spatial operations that §3 makes exact. The adopted photon (`gauge.photon`, F67/F68/F69) never touches `_bcc_uvec` and is unaffected. **Checking the five live consumers is the single most valuable follow-up and it is not done here.**
3. **Show the branch map is not $\tau_g(s)=s\prod\varepsilon_i$** — e.g. that the two branches should be related by an extra operation that restores a larger $L$. Leg C2 is an exact identity, so this would have to attack the definition of the branches, not the algebra.

## 8. What is *not* claimed

- Nothing about $\omega=\arccos u$. F30's anisotropy results are independent, closed, and untouched: $u$ is the same function in every convention swept here, and the branch map leaves it invariant by construction.
- No code change. `_bcc_uvec` is correct as shipped (§3); the "improvement" a naive covariance fit suggests is physically wrong.
- **No claim that BDPT were wrong.** Paper 1's isotropy condition (Eq. 5) requires only that *some* finite group $L$ of graph automorphisms admit a faithful unitary representation — not that $L=O_h$ — and the paper's own abstract recovers Weyl dynamics "in the relativistic limit". A group of order 8 or 16 satisfies Eq. 5, and §6's "exact infrared symmetry" is that phrase made quantitative. What is new here is the exact residual group and the exclusion proof, not a correction to the paper. (Caveat recorded honestly: the primary paper's own choice of $L$ could not be retrieved this session — the fetch needed an approval that did not arrive — so this attribution rests on `references/qca-papers-1-4-overview.md` and the published abstract, not on Paper 1 §III.)
- No claim that $D_{2h}/D_{4h}$ is a *defect* of the model. A finite lattice law with a broken point group at the lattice scale and an exact continuum symmetry is the normal situation; what is new is that this one's breaking is now exactly characterised rather than assumed absent.
