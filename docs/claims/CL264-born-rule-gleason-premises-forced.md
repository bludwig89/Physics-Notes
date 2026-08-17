---
id: CL264
title: The rule supplies both premises of Gleason's theorem — a measurement here cannot live in dimension 2, and the record channel is a fixed operator that carries no reference to the measured basis — so the Born rule follows rather than being assumed
slug: born-rule-gleason-premises-forced
tier: headline
kind: derivation
status: contingent
domain: [QM]
exactness: exact
findings: [F304, F312, F281, F290, F227]
tests: [F304-born-rule-gleason, F312-born-nonabelian]
modules: [casim.engine.interactions.qi_born_gleason]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-06
last_verified: 2026-08-11
provenance: authored
review_state: authored
confidence: high
---

# CL264 — The Born rule is a theorem here because the rule forces Gleason's premises

## Statement

Gleason's theorem states that a non-negative, non-contextual weight $f$ on the rays of a Hilbert
space with $\dim\mathcal H\ge3$, satisfying $\sum_i f(e_i)=1$ for every orthonormal basis, is
necessarily $f(v)=\langle v\rvert\rho\lvert v\rangle$. It is not used as a derivation of the Born
rule in ordinary quantum mechanics because both of its premises are free assumptions there. **In
this model neither premise is free** — and, since the 2026-08-06 revision, **the theorem is proved
on this card's evidence rather than cited** (F304 §5).

**Dimension.** A measurement in this model is not defined without a *record*, and a record lives
on environment cells: with zero record cells the decoherence factor is the empty product,
identically $1$, so nothing is ever written. The smallest Hilbert space on which this model
realises a measurement is therefore $2^{1+1}=4>2$. The rule *does* own two-dimensional invariant
subspaces — the momentum blocks of `weyl_step_3d_bcc`, whose leakage under one genuine tick is
$2.2\times10^{-16}$ — but they are **not** measurement contexts: the pointer algebra is
position-diagonal and $\lVert[\Pi_k,\hat n(x)]\rVert_F=0.17539$, matching the closed form
$\sqrt{2/N-2/N^2}$ at $N=64$ with residual **literal `0.0`**. A momentum block is invariant but
unreadable.

**Non-contextuality.** The system–environment generator is
$H_\text{int}=\sum_x\hat\alpha(x)\otimes\hat n(x)$ — minimal coupling, a **fixed operator of the
rule**, containing no reference to a measured basis. Five distinct orthonormal bases containing
the same ray therefore write the same physical record for that ray: weight spread **literal
`0.0`**, record ray infidelity $2.2\times10^{-16}$, against $0.1549$ / $0.4916$ for a
basis-referencing control. Remote context changes cannot move a local weight either:
$9.7\times10^{-17}$, against $0.1985$ for a coupling outside the F227 cone.

**The theorem.** Averaging the frame condition over the bases containing a fixed ray gives the
operator identity $f+(d-1)Bf=W$, with $(Bf)(v)$ the mean of $f$ over the unit sphere of $v^\perp$.
$B$ is $U(d)$-equivariant, hence a scalar $b_k$ on each isotypic component of
$L^2(\mathbb{CP}^{d-1})$, and

$$b_k=\frac{P_k^{(d-2,0)}(-1)}{P_k^{(d-2,0)}(1)}=\frac{(-1)^k}{\binom{k+d-2}{k}},$$

so a component survives iff $1+(d-1)b_k=0$. **One formula gives both halves of the dichotomy.** At
$d=2$, $\binom{k}{k}=1$, so every odd $k$ survives and the weight space is infinite-dimensional. At
$d\ge3$, $\binom{k+d-2}{k}$ is strictly increasing and exceeds $d-1$ for every $k\ge2$, so only
$k=0,1$ survive and $f(v)=\langle v\rvert\rho\lvert v\rangle$ on a space of dimension
$1+(d^2-1)=d^2$. For a pure lattice state $f(v)=\lvert\langle v\rvert\psi\rangle\rvert^2$ —
confirmed on the model's own record channel at $2.2\times10^{-16}$.

## What it extends

Gleason (1957) and its standard reception. The theorem is normally regarded as a *characterisation*
of quantum probability rather than a derivation of it, for two reasons that are both about the
premises rather than the mathematics: Bell's 1966 objection that non-contextuality is unmotivated,
and the $d=2$ gap that makes the qubit — the most-used system in the subject — a counterexample.
This claim asserts that a lattice model whose interactions are all fixed by the rule removes both
objections *for that model*, converting a characterisation into a derivation.

It also narrows what the project has to take on trust. As first issued (2026-08-06 morning) this
card carried Gleason as an external theorem, the posture F289 takes toward the belt-trick homotopy.
It no longer does: §5 of F304 proves the frame-function theorem for $f\in L^2$, and the proof
*derives* the $d=2$ hole that §3 had exhibited by example. The rank computations that were written
as evidence for a citation are now **predictions**, checked as integers.

It also extends the model's own position. F281 derived the Born rule on two legs and named the
undischarged hypothesis under each; `CL253` therefore declined to carry the Born leg at all and
recorded that a card should be written "when one of those two hypotheses is closed". **Leg 1's
hypothesis — that branch weights are a function of the amplitudes at all — is now a conclusion**,
since Gleason derives both that $f$ is a function of the state and that the function is quadratic.
Leg 2's Schlosshauer–Fine premise is not repaired but made *unnecessary*: this route never uses
envariance.

It does **not** extend or contradict unitarity. No collapse term is added and F227's "unitary
theory with no objective collapse" is unchanged.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F304-born-rule-gleason-premises-forced.md` §1 | no record without cells ⇒ $\dim\ge4$; momentum-block leakage $2.2\times10^{-16}$; $\lVert[\Pi_k,\hat n]\rVert=0.17539$ matching $\sqrt{2/N-2/N^2}$ at residual `0.0`; commutant dimension $2^n$ for $n=1,2,3$ | exact |
| `findings/F304-born-rule-gleason-premises-forced.md` §2 | weight spread across five contexts sharing a ray, literal `0.0`; record ray infidelity $2.2\times10^{-16}$; label-permutation spread $2.2\times10^{-16}$; remote-context deviation $9.7\times10^{-17}$ | exact |
| `findings/F304-born-rule-gleason-premises-forced.md` §3 | frame-function space dimension $=d^2$ at $d=3,4$ for every degree, *and is* the Hermitian forms ($5.7\times10^{-15}$); at $d=2$, $1+\sum_{\ell\ \text{odd}\le\deg}(2\ell+1)=4,4,11,11,22,22$ matching its closed form as an integer | exact |
| `findings/F304-born-rule-gleason-premises-forced.md` §5 | the frame-function theorem **proved**: $B$'s spectrum vs the closed form $b_k$ with $\dim V_k$ multiplicities, $\le1.6\times10^{-15}$; $1+(d-1)b_1=0$ **exactly** in `Fraction` arithmetic for $d=2..12$; $d\ge3,k\le40$ strictly positive with min gap $0.5$; $d=2$ survivors exactly the odd $k$; the proof predicts §3.3's measured integers with no fitting | exact |
| `findings/F304-born-rule-gleason-premises-forced.md` §4 | $\max\lvert w-\lvert\langle v\rvert\psi\rangle\rvert^2\rvert=2.2\times10^{-16}$; $\ell^2$ change literal `0.0`, min over other $p$ $=0.0335$ | exact |
| Record `F304-born-rule-gleason` (tier gate, entry `check_born_gleason`) | **21/21**, with four declared controls verified red on their own legs | exact |
| `findings/F312-born-rule-nonabelian-premises.md` | Non-contextuality on $SU(2)_L$ and $SU(3)_c$, and the Schur reduction making the internal index irrelevant for any compact group; 18/18, three controls red | exact |
| `test-results/F304_born_rule_gleason.json` | the result artifact | machine |
| `test-results/F312_born_nonabelian.json` | the non-Abelian premises artifact | exact |

## Falsifier

Three, each a declared parameter perturbation of the gate record, and each verified to fire:

1. `casim test --id F304-born-rule-gleason --param coupling=contextual` — replace the record
   channel with any generator that references the measured basis. B2a/B2b go red. **If a
   context-referencing coupling is ever found to be required anywhere in the model — a Yukawa
   scalar, a derivative coupling, any term not built from $\hat n(x)$ — this claim fails**,
   because the non-contextuality argument is exactly the absence of such a term. This is the same
   dependency on key decision 3 that `CL253` carries.
2. `--param locality=nonlocal` — B3a goes red. A coupling outside the F227 cone restores remote
   contextuality, so any breach of the strict cone or of F290's exact no-signalling breaks the
   remote half of the premise.
3. `--param gleason_dim=2` — B5a goes red. Included because it is the way the dimension premise
   could be vacuous, and the ratchet should say so: if a measurement context of total dimension 2
   were ever exhibited on this lattice, the $11$-, $22$-dimensional non-Born families of §3 would
   become physically realisable and the derivation would fail.
4. `--param zonal=naive` — B7a goes red. Replaces $b_k$ with $(-1)^k/(d-1)^k$, which is *correct*
   at $k=0$ and $k=1$ and wrong only from $k=2$. Without this control B7a could be passing on the
   two trivial modes; with it, the closed form is tested where it does work. A measured
   $b_k$ departing from $(-1)^k/\binom{k+d-2}{k}$ by more than $10^{-12}$ at any $(d,k)$ would
   falsify §5 directly.

The claim is **not** falsifiable by experiment, and that is the correct outcome rather than an
evasion: a model that agrees with quantum mechanics about probabilities is supposed to be
experimentally indistinguishable here (cf. `CL`-level CN1, the settled Bell null, and F226's exact
Tsirelson saturation). `tier: headline` therefore rests on the structural result, not on a
prediction.

## Status & history

Issued 2026-08-06 from F304, written to close completeness row **A6** ("Born rule is *reproduced*
in tests, never derived"). This is the card `CL253` §"Status & history" asked a later session to
write: *"A Born-rule card should be written when one of those two hypotheses is closed, or written
now as `status: contingent` with the hypothesis named — that is a judgement for the next session."*
The judgement made here is that leg 1's hypothesis **is** closed, and the card is issued
`contingent` anyway, on a premise the earlier session did not name because F281's route did not
isolate it.

**`status: contingent`, and the hypothesis is named.** Two things were granted at first issue.
The first has since been discharged; the second has not, and cannot be.

1. ~~**Gleason's theorem itself is external and is not reproved here.**~~ **Discharged
   2026-08-06 - 18:20.** F304 §5 proves the frame-function theorem for $f\in L^2$ by harmonic
   analysis on ray space, and the proof is better than the citation in one specific respect: the
   $d=2$ hole and the $d\ge3$ rigidity come out of the *same line* of the *same formula*
   ($\binom{k}{k}=1$ versus $\binom{k+d-2}{k}>d-1$), so "why is $d\ge3$ the hinge" is answered by
   arithmetic rather than deferred to someone else's proof.
   **What replaces it is one lemma, not a theorem.** §5 is complete for $f\in L^2$; Gleason's
   theorem holds for merely *bounded* $f$, and the bridge — a non-negative frame function is
   automatically continuous — is the Cooke–Keane–Moran regularity lemma, cited not reproved. Its
   entire content is the exclusion of **non-measurable** weight assignments: every bounded
   measurable weight on a compact ray space lies in $L^2$ and is covered. `status` stays
   `contingent` on that lemma. **Closing it is a real, bounded piece of work** (CKM is three pages
   of sphere geometry) and is the obvious next step for anyone who wants this card `live`.
1b. ~~**Non-contextuality is proved for the $U(1)$ wrap generator only; the $SU(2)_L$ and
   $SU(3)_c$ commutators are not written out.**~~ **Discharged 2026-08-11 by F312**, and by a
   *theorem* rather than by running the $U(1)$ check twice more. The current algebra is written
   out with its $\delta_{xy}$ **exact** — the off-site commutator $[\hat J^a(x),\hat J^b(y)]$,
   $x\ne y$, is literally `0.0` for both groups — so the entire non-Abelian structure is
   **intra-site**, while a measurement context is a choice of basis on the pointer factor, an
   **inter-site** object. The record observable is a gauge singlet literally
   ($[\hat J^a,\hat n]=0.0$), and a **Schur reduction** ($\sum_aT^aT^a$ a multiple of $\mathbb 1$,
   value $(N^2-1)/2N$) makes the internal index factor out of the frame condition **for any
   compact group and any irrep** — which is why this closes the seam for whatever the model adds
   next, not just for these two. One consequence strengthens the card: since
   $\dim(\mathcal H_p\otimes V)=d_pN$, **$SU(3)_c$ clears the $d\ge3$ premise on its own** and
   §5's $d=2$ hole is **unreachable in any gauge-charged sector**. *This was the second of
   rubric A6's two stated reasons for `PARTIAL`; only the CKM lemma of item 1 now remains.*
   The non-Abelian result carries its own card, **CL268**, which rolls up to this one.

2. **One premise is irreducible: that an exhaustive set of records carries weights summing to
   one.** That is the definition of the object being derived rather than a physical input, and no
   derivation of the Born rule escapes it. It is strictly weaker than either hypothesis F281 had
   to carry, which is the whole content of the advance.

**Scope limit carried from F304 §"Remains", inherited from F281 open item 2.** The
context-blindness argument is written out for the $U(1)$ wrap generator. The $SU(2)_L$ and
$SU(3)_c$ couplings are site-local rotations and are diagonal in position by construction, but the
explicit non-Abelian commutator has not been written. This card's statement is correct as written
— the record channel carries no reference to the measured basis — but the *uniqueness* half is
$U(1)$-explicit and non-Abelian-by-inspection, exactly as `CL253` records for its own diagonality
argument.

**What this card does not do.** It does not edit F281, whose two legs remain a correct record of
what that session concluded, and it does not withdraw them: leg 1 survives as a corollary (B6b
re-measures it through F281's own routine), and leg 2 survives as an independent second argument
with its own known gap. `CL253` is unchanged in substance and gains only a history note that its
stated condition has been met.

## Sources

- `findings/F304-born-rule-gleason-premises-forced.md`
- `findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md` §2.6 — the two hypotheses this card discharges and declines
- `docs/claims/CL253-measurement-pointer-born-rg.md` §"Status & history" — the request this card answers
- `findings/F290-cluster-decomposition-strict-cone.md` — exact no-signalling
- `findings/F227-decoherence-unitarity-floor.md` — the strict causal cone; unitary, no objective collapse
- `findings/F289-spin-statistics-connection.md` — the precedent for deriving a theorem's premises while citing the theorem
- `src/casim/engine/gauge/minimal_coupling.py` — the generator whose context-blindness is the argument
- `src/casim/engine/lattice/bcc.py` — `weyl_step_3d_bcc`, whose momentum blocks are the objection §1.2 answers
- `docs/status/completeness-2026-08-04.md` — row A6, the gap this closes
- A. M. Gleason, *J. Math. Mech.* **6** (1957) 885 — the theorem, reproved for $L^2$ in F304 §5
- R. Cooke, M. Keane & W. Moran, *Math. Proc. Camb. Phil. Soc.* **98** (1985) 117 — the regularity lemma, the one step still cited
- J. S. Bell, *Rev. Mod. Phys.* **38** (1966) 447 — the non-contextuality objection this model removes
