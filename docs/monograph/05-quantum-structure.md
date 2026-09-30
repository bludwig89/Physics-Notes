# Chapter 5 — Quantum Structure: the Pointer Basis, the Born Rule, and Classicality

*Chapter 5 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md`,
`findings/F304-born-rule-gleason-premises-forced.md`,
`findings/F312-born-rule-nonabelian-premises.md`, and
`findings/F329-gleason-regularity-closes-a6r.md` — the four findings `00-plan.md` §2 assigns to
this chapter, all read in full — plus `docs/monograph/01-postulates-and-ontology.md` (P4 and its
§1.3 "beable question", which this chapter continues rather than re-litigates),
`docs/monograph/03-the-update-rule.md` (the concrete unitary stepper these findings act on), and
`docs/monograph/04-structural-theorems.md` §4.2.8 (R4.12a–c, F290's exact no-signalling and strict
causal cone, reused here rather than re-derived). Checked directly against
`docs/theory/supersessions.yaml` (grepped for all four finding numbers: **zero hits** — none of
F281/F304/F312/F329 appears in any of the 23 supersession records) and against `claims-index.md`:
**CL253** (F281 only, `tier: headline`, `status: live`, `exactness: exact`) and **CL264** (F304,
F312, F329, F281, F290, F227; `tier: headline`, `status: live`, `exactness: exact`, `confidence:
high`) are this chapter's two headline cards; **CL268** (F312, F304, F281, F27, F41; `tier:
supporting`, `status: live`, `rolls_up_to: CL264`) is the non-Abelian extension read as its own
card per the finding-coverage rule. `docs/status/open-derivations.md` row **A6r** is recorded
**FULLY CLOSED** (2026-08-27, by F329) and row **A4r** (F378, Chapter 4's own gauged-CPT residual)
is a different, unrelated row despite the similar "narrowed again, same shape" phrasing — checked
directly and not conflated here. Notation, postulates and results are those of Chapters 1, 3 and 4
— $\psi$, $\hat n(x)$, $\mathcal U$, $H$, $c_\text{lat}$, the beable/changeable/superimposable
vocabulary — extended, never redefined.*

## 5.0 What this chapter establishes

Chapter 1 posed a question it explicitly declined to answer: P4 treats the per-cell amplitude as
physically real and takes no additional stance on whether a 't Hooft-style hidden classical layer
sits beneath it (§1.3, §1.7 item 1). That agnosticism is a considered position, not a placeholder —
but it leaves a debt unpaid. A genuinely unitary substrate, with no privileged ontological basis and
no collapse dynamics, *owes an account* of why measurements ever produce one definite outcome, why
that outcome is weighted by $\lvert\psi\rvert^2$, and why the macroscopic world looks classical at
all. Before the four findings this chapter reports, the model had essentially nothing to say on any
of these three questions beyond using their conclusions elsewhere in the tree without deriving them.
This chapter reports what the model's own mechanism turns out to be, built entirely from structure
the rule already has — minimal coupling, exact unitarity, the exact block-spin operator, the strict
causal cone — with **no collapse term added and no privileged basis postulated**. The result is not
uniform: one leg of the argument closes to a full theorem with no external citation surviving except
a single 69-year-old lemma; a second, independent leg is opened, shown to have a real unresolved
gap, and then rendered *unnecessary* rather than repaired; and the classicality argument is a
genuine derived result (an RG eigenvalue) with a precisely bounded scope. Keeping these three
outcomes distinct, rather than reporting a uniform "solved," is this chapter's central discipline —
the same discipline Chapter 4 applied to its own eleven findings.

## 5.1 Inputs

**Postulates used.** **P4** (linearity, exact unitarity, the amplitude treated as physically real,
with no additional hidden-classical-layer postulate) is the postulate this entire chapter tests
against the model's own results: every derivation below is a statement about what a *purely unitary*
substrate does, with no collapse dynamics inserted anywhere. **P2** (locality) is load-bearing in
three separate places: minimal coupling is *itself* a strictly local, per-site (or per-link) term —
the reason it can force a unique pointer observable at all is that it is the only kind of coupling
the rule contains, and that restriction is a locality-flavored consequence of the construction, not
an accident; the causal-cone cost of an envariant counter-swap (§5.2.3) is priced directly in Chapter
4's cone; and the remote-context leg of non-contextuality (§5.2.5) is exactly Chapter 4's exact
no-signalling result, reused rather than re-derived. **P6** (mass and hypercharge from a gauged
chiral $SU(2)$ connection, no Higgs) is the single most load-bearing postulate in this chapter after
P4: CLAUDE.md's Core Design Decision 3 — no Yukawa scalar, no derivative coupling, no non-minimal
term anywhere in the tree — is what makes the pointer basis and non-contextuality *forced* rather
than merely *observed*, in every one of the four findings, explicitly and by name. **P5** (the
primitive field is $\psi\in\mathbb C^2$) fixes the object the pointer observable $\hat
n(x)=\psi^\dagger\psi(x)$ is built from. **P1** and **P3** are not separately invoked; nothing below
turns on discreteness *per se* or on the point group.

**Prior results used, precisely.** **R3.2/R3.6** (Chapter 3: the concrete real-space stepper is
exactly local and exactly unitary, with zero residual) is what "the discrete-tick update is a
concrete unitary matrix, not an abstraction" cashes out to at every point this chapter builds an
operator on the model's Hilbert space. **R4.12a** (Chapter 4: no-signalling exact to
$7.77\times10^{-16}$, vs. $0.461$ under a non-local control) and **R4.12b** (the causal cone is
exactly zero outside $r=t$, vs. a generic Lieb–Robinson bound of $7.39$ at the same points) are used
*directly*, not merely cited by analogy: F304 §2.3's remote-context non-contextuality leg is R4.12a
read at a different pair of observables, and F281 §2.2's "cone cost" of an envariant counter-swap is
priced against the same causal-cone fact, in the tick convention $C(r,t)=0$ for $r>4t$ that Chapter
4 itself reconciles against R4.12b's $r=t$ convention (§4.2.8, "reconciles numerically... once the
two different tick conventions are accounted for"). This chapter does not re-derive either fact and
flags explicitly where each is used.

**Free inputs consumed, stated plainly.** Several, of different character, and the chapter does not
let any of them pass silently:

1. **Key decision 3 (Higgs-free, minimal coupling only) is a structural free input every result in
   this chapter leans on**, not a derived fact this chapter (or F281/F304/F312) establishes. It is a
   Chapter 1 postulate (P6) rather than a theorem: *given* that the model contains no non-minimal
   coupling anywhere, the pointer basis and non-contextuality are forced; if a future sector required
   a non-minimal term, every uniqueness claim below would need to be re-examined for that sector.
   This is exactly the shape of every falsifier in §5.8.
2. **The Schlosshauer–Fine assumption of F281's leg 2 (envariance) is not closed anywhere in this
   chapter.** It is opened (§5.2.3), its exact failure boundary is measured (§5.2.4), and it is then
   made *unnecessary* by the independent Gleason route (§5.2.6–5.2.9) rather than repaired. Leg 2
   remains on the record as an independent second argument carrying its own unresolved gap — this
   chapter reports that honestly rather than treating the Gleason closure as if it had also fixed
   leg 2.
3. **One premise is definitional, not physical, and stays that way throughout**: "an exhaustive set
   of records carries weights summing to one" is the definition of the object (a probability
   assignment) being derived, not an assumption a derivation could remove. F304's own closing section
   is explicit about this, and CL264 records it as the one item that "does not close, and is not
   claimed to."
4. **$N_c=3$ is used, not derived**, in F312's dimension bonus (§5.2.7): the claim that $SU(3)_c$
   alone clears Gleason's $d\ge3$ premise depends on $N=3$, which is an input from F293 (mapped, not
   closed) rather than a result this chapter's findings establish.
5. **F329's closure rests on a primary-source citation retrieved by automated PDF extraction**, not
   on a from-scratch re-derivation or a character-by-character read of the scanned original — F329
   §5 discloses this itself, including that the underlying Cooke–Keane–Moran (1985) PDF returned no
   machine-readable text at all this session. This chapter treats F329's closure as resting on a
   well-established, 69-year-old, continuously-cited peer-reviewed theorem, cited rather than
   independently re-verified against the typeset page images — a materially different confidence
   class from an unpublished argument, but a citation nonetheless, and named as such.

## 5.2 The derivation

### 5.2.1 The pointer basis is forced by minimal coupling, not chosen (F281 M1)

Every interaction in this tree enters as minimal coupling: a phase or rotation attached to the site
or link, multiplying the spinor there. Promoting the $U(1)$ gauge phase to the environment operator
it physically is gives the system–environment generator

$$H_\text{int}=\sum_x\hat\alpha(x)\otimes\hat n(x),\qquad\hat n(x)=\psi^\dagger\psi(x)=\tfrac12\big(\mathbb1-\hat Z_x\big),$$

and every term in it is, by construction, diagonal in the site-occupation basis, so

$$[H_\text{int},\hat n(y)]=0\qquad\text{exactly, literal }0.0\text{, for every }y.\tag{R5.1}$$

$$\boxed{\;\text{the model's pointer observable is local charge density — a theorem about the rule, not a posit (R5.1)}\;}$$

**Why "forced" rather than "observed" is the correct word, and why P6 is what makes it true.**
Standard decoherence theory (Zurek) identifies the pointer basis as whichever observable commutes
with $H_\text{int}$ — but $H_\text{int}$ is a *modelling input* there, chosen per problem. In this
model $H_\text{int}$ is not a choice: key decision 3 (P6) removes every alternative, because there is
no Yukawa scalar, no derivative coupling, and no non-minimal term of any kind anywhere in the tree
that could einselect a different observable. Measured directly against the alternatives that *would*
exist if the model contained them: a non-minimal $\sigma^x$ coupling gives commutator $6.2219$
(control), kinetic hopping gives $2.8284$ (pointer states exactly stable only in the
$\lVert H_\text{int}\rVert\gg\lVert H_\text{hop}\rVert$ limit), and the internal spin generator gives
$6.2219$ — **spin is not einselected**, which is the model correctly reproducing the fact that a spin
superposition survives until amplified into a position difference (a Stern–Gerlach magnet's whole
job), not a defect. Zurek's predictability sieve, scanned over the model's own $SU(2)$ rotor family,
agrees: the site basis minimizes produced entropy at $S=6.1\times10^{-16}$ under the model's own
coupling, and the control (non-minimal generator) moves the minimizer to $\theta=\pi/4$ and makes the
site basis the *worst* basis instead, confirming the check can fail and the control makes it fail.

**Uniqueness at every system size, not merely a one-cell scan (F281 §1.6).** At many cells the naive
sieve cannot claim to have found a global minimum over $U(2^n)/U(1)^{2^n}$. F281 replaces the scan
with an algebraic fact, computed rather than asserted: $\{\hat n(x)\}_{x=1}^n$ is a **maximal
abelian** subalgebra — its commutant dimension equals $\dim\mathcal H=2^n$ exactly, checked at
$n=1,2,3,4$ by matrix rank. A maximal abelian algebra has a unique joint eigenbasis up to phases and
label order, so the pointer basis is not *a* minimizer of the sieve at each size; it is *the* one, at
every size, with no scan required — and the gap between the pointer entropy (round-off, flat with
$n$) and the most-predictable generic state's entropy (growing from $0.041$ to $1.655$) **widens**
with system size: einselection gets sharper, not weaker, as the system grows. The one loophole —
degenerate environment coupling to two configurations identically — is tested and found to be exactly
what it should be: a decoherence-free subspace, the sole genuine exception, not a defect in the
uniqueness claim.

$$\boxed{\;\{\hat n(x)\}\text{ is maximal abelian at every system size — the unique pointer basis, sharpening (not weakening) as }n\text{ grows (R5.2)}\;}\tag{R5.2}$$

**The account of "collapse": decoherence, and a recurrence postponed past any observable horizon.**
With the environment in $\lvert+\rangle^{\otimes n_e}$, the coherence factor is exactly
$\lvert D(t)\rvert=\prod_j\lvert\cos(g_jt)\rvert$, verified to $6.7\times10^{-16}$; populations are
conserved to $4.4\times10^{-16}$ — decoherence, not collapse, since nothing is removed from the
state, and the branches merely stop interfering. Because the lattice is finite and the evolution
exactly unitary, $\lvert D(t)\rvert$ must recur; the fraction of time it exceeds $0.9$ falls
geometrically with environment size ($\log_{10}(\text{fraction})=-0.7611\,n_e+0.297$), extrapolating
to $\log_{10}(T_\text{rec}/\tau)\approx4.58\times10^{23}$ ticks for a mole of environment cells. This
is offered as exactly what it is and no more: the model's entire account of "why we never see a
superposition un-decohere" is that unitarity guarantees it eventually must, and the exponent
postpones it far past anything the age of the universe could probe. Consistent with F227's "unitary
theory with no objective collapse" (Chapter 4 does not touch F227 directly, but this chapter's whole
argument is compatible with, and adds no new mechanism beyond, that finding's own null result) by
construction, not as an independent check of anything.

$$\boxed{\;\text{decoherence factor exact in closed form; recurrence pushed to}\ \log_{10}(T_\text{rec}/\tau)\approx4.58\times10^{23}\ \text{ticks — the whole account of "collapse" (R5.3)}\;}\tag{R5.3}$$

### 5.2.2 The Born rule, leg 1: the dynamics itself singles out $\ell^2$ (F281 M2, first leg)

A branch weight must be additive, permutation-symmetric, and conserved by the evolution (branches do
not change identity under a deterministic unitary step, so a drifting measure would not be a
probability). Testing the $\ell^p$ family against one genuine BCC Weyl tick: $\ell^2$ is conserved to
literal $0.0$; every other tested $p\in\{1,1.5,2.5,3,4\}$ changes by $3$–$32\%$. The control that
makes this a statement about *mixing* rather than about $\ell^p$ in the abstract: at the register's
native exchange gate's permutation point (a monomial unitary, SWAP), *every* $p$ is conserved
exactly — so the $p=2$ singling-out is produced specifically by the lattice step's genuine mixing.

$$\boxed{\;\text{only }\ell^2\text{ survives a genuine lattice tick — literal }0.0\text{ change, vs. }3\text{–}32\%\text{ for every other }p\;}\tag{R5.4}$$

**What this leg assumes, named rather than hidden.** This leg says nothing about probability per se —
it says that *of* the additive, permutation-symmetric candidates, the dynamics permits exactly one.
It carries its own unstated hypothesis: that branch weights are a function of the amplitudes at all.
That hypothesis is the residual §5.2.6 closes.

### 5.2.3 The Born rule, leg 2: envariance, on CA-native gates, with its own real gap (F281 M2, second leg)

For $\lvert\psi\rangle=(\lvert s_0e_0\rangle+\lvert s_1e_1\rangle)/\sqrt2$, a swap on the system is
exactly undone by a counter-swap on the environment (ray infidelity $2.2\times10^{-16}$), so the two
outcomes cannot be distinguished by anything belonging to the system alone, forcing $p_0=p_1=1/2$.
This is checked as **CA-native**, not asserted abstractly: the model's own exchange interaction at
its permutation point *is* SWAP (residual literal $0.0$), the single-cell flip is the model's own
$SU(2)$ rotor at $\theta=\pi/2$, and the counter-swap must fit inside the causal cone — by R4.12b's
convention, $C(r,t)=0$ for $r>4t$, so a counter-swap at radius $R$ costs $\ge R/4$ ticks. **The Born
rule in this model has a light-cone price it does not have in abstract Hilbert space** — measured
directly, and found never binding (a BCC ball of radius $10^3$ reaches denominators
$M\sim10^{6.0\times10^8}$ within 250 ticks). Maximizing the restored overlap over $u_E\in U(2)$ gives
the closed form $2c_0c_1$, matching measurement to $1.1\times10^{-16}$: **envariance holds iff
$c_0=c_1$**, which is what turns this into an argument rather than a restatement. Fine-graining
$\lvert c_k\rvert^2=\mu_k/M$ via a CA-native controlled-copy (CNOT) produces $M$ exactly
equal-amplitude branches (deviation `0.0`), and every fine transposition is envariant (residual
`0.0`), giving $p_k=\lvert c_k\rvert^2$ exactly over $\mathbb Q$ when weights are obtained by counting
fine branches.

$$\boxed{\;\text{envariance forces }p_k=\lvert c_k\rvert^2\text{ on CA-native gates, reachable within the causal cone's cost, exact over }\mathbb Q\;}\tag{R5.5}$$

**The gap, named and not closed.** Leg 2 inherits the standard Schlosshauer–Fine objection in full: it
assumes outcome weights depend only on the reduced state of the system. Neither F281 nor any later
finding read for this chapter closes that assumption. This is the chapter's first explicit instance
of the discipline stated in §5.1: leg 2 is a real, independently useful argument, and it carries a
real, disclosed hole.

### 5.2.4 Why two independent legs, rather than one repaired leg

F281 deliberately carries both legs rather than one, because they rest on **independent, non-nested
hypotheses**: leg 1 assumes only that weights are *some* function of the amplitudes; leg 2 assumes
weights depend *only* on the reduced state (Schlosshauer–Fine). Neither implies the other, and
neither is derived in F281. This is the structural reason the chain below (§5.2.6 onward) matters: it
closes leg 1's hypothesis completely and, in the same stroke, removes any need for leg 2's — not by
repairing Schlosshauer–Fine, but by finding a route that never invokes it.

### 5.2.5 Classicality as an RG eigenvalue — set aside briefly, resumed in §5.2.10

The remaining piece of F281 (M3, the block-spin attractor) is deferred to §5.2.10, after the Born-rule
chain, so that the chapter's own logical order matches its assignment brief: pointer basis, then Born
rule (through its full Gleason closure), then classicality.

### 5.2.6 Closing leg 1's hypothesis: Gleason's theorem is forced, not cited (F304)

Gleason's theorem says a non-negative weight on rays, summing to one over *every* orthonormal basis,
in a Hilbert space of dimension $\ge3$, is necessarily $f(v)=\langle v\rvert\rho\lvert v\rangle$. It
is not usually treated as a derivation of the Born rule, because both of its premises — $\dim\ge3$
and non-contextuality — are free assumptions in ordinary quantum mechanics. F304's entire contribution
is that **neither premise is free in this model.**

**The dimension premise, structural rather than assumed.** F281's decoherence factor is an *empty
product* at zero environment cells — identically $1$ at every $t$ — so a measurement with no record
never writes one. The smallest Hilbert space carrying an actual measurement is therefore
$\dim=2^{1+1}=4>2$. The model *does* own genuine 2-dimensional invariant subspaces (momentum blocks
of the free walk, leakage $2.2\times10^{-16}$ under one tick), but they are **unreadable**: the
commutator of a momentum-block projector with the pointer observable is $0.17539$, matching the
closed form $\sqrt{2/N-2/N^2}$ to literal `0.0` — a momentum block is invariant but delocalized in
position, so it cannot serve as a measurement context. Combined with §5.2.1's maximal-abelian result
(exactly one pointer context, at every size), the dimension premise is met **before any choice of
apparatus is made**, not merely satisfied by the specific apparatus F304 happened to build.

$$\boxed{\;\dim\mathcal H_\text{min}=4>2\text{, structurally, and the model's own 2-dim subspaces are invariant but unreadable — the dimension premise is not free (R5.6)}\;}\tag{R5.6}$$

**The non-contextuality premise, a theorem about the generator.** $H_\text{int}=\sum_x\hat\alpha(x)
\otimes\hat n(x)$ contains no reference to which basis an experimenter completes a ray into. Measured
directly: five distinct contexts sharing the same ray give weight spread literal `0.0` under the
model's own generator, vs. $0.1549$ for a basis-referencing control built specifically to exist
nowhere in the tree. Remote contexts are excluded by R4.12a's exact no-signalling, reused directly:
$\max\lVert\rho_B(\text{ctx})-\rho_B(\text{ctx}_0)\rVert_\infty=9.7\times10^{-17}$ for the model's own
local coupling, vs. $0.1985$ for a non-local control — a contextual weight assignment across
spacelike separation would *signal*, and the rule forbids it exactly.

$$\boxed{\;\text{non-contextuality is a theorem about }H_\text{int}\text{, not an assumption about the experimenter (R5.7)}\;}\tag{R5.7}$$

**The theorem, applied.** With both premises forced, Gleason gives $w(v)=\langle
v\rvert\rho\lvert v\rangle$, and for a pure state $w(v)=\lvert\langle v\rvert\psi\rangle\rvert^2$ —
confirmed on the model's own channel to $2.2\times10^{-16}$. **F281's leg 1 hypothesis is now a
corollary**: Gleason gives $\operatorname{Tr}\rho=1$, unitarity preserves it, so $\ell^2$ is conserved
and nothing else is — re-derived through F281's own routine rather than a separate claim, so the two
findings cannot drift apart. **Leg 2 is not repaired; it is made unnecessary**, since this route never
invokes envariance and has nothing for the Schlosshauer–Fine objection to attach to.

### 5.2.7 The theorem itself, proved: one closed form gives both halves of Gleason's dichotomy (F304 §5)

F304's first issue cited Gleason's theorem as an external fact once its premises were forced. A later
revision (same finding, §5) goes further and *proves* the frame-function dichotomy for
$f\in L^2(\mathbb{CP}^{d-1})$, by representation theory rather than citation. Averaging the frame
condition over bases containing a fixed ray gives an operator identity $f+(d-1)Bf=W$; $B$ is
$U(d)$-equivariant, hence scalar on each isotypic component, with eigenvalue

$$b_k=\frac{P_k^{(d-2,0)}(-1)}{P_k^{(d-2,0)}(1)}=\frac{(-1)^k}{\binom{k+d-2}{k}},$$

and a component survives the frame condition iff $1+(d-1)b_k=0$. At $d=2$, $\binom{k}{k}=1$ for every
$k$, so **every odd $k$ survives** — the frame-function space is infinite-dimensional, reproducing
(and now *deriving*, rather than merely exhibiting by counterexample) the qubit's genuine hole,
matching the measured integer sequence $4,4,11,11,22,22,\dots$ exactly. At $d\ge3$,
$\binom{k+d-2}{k}$ is strictly increasing and exceeds $d-1$ for every $k\ge2$, so only $k=0,1$
survive — Born, on a space of dimension $d^2$, matching the measured $9,9,9$ ($d=3$) and $16,16,16$
($d=4$) exactly, as integers, with zero fit.

$$\boxed{\;b_k=\frac{(-1)^k}{\binom{k+d-2}{k}}\;\text{— one formula, both halves of Gleason's dichotomy, verified as an integer sequence at every tested }(d,k)\;}\tag{R5.8}$$

This closes the residual F304's first issue named — "Gleason's theorem is external" — down to a
single remaining external fact, stated precisely rather than smoothed over: the argument is complete
for $f\in L^2$, but Gleason's theorem needs only *boundedness*, and the bridge (a non-negative frame
function is automatically continuous) is not reproved here. That is exactly the residual §5.2.9
closes.

### 5.2.8 Extending non-contextuality to $SU(2)_L$ and $SU(3)_c$: one theorem, not two more cases (F312)

F304's non-contextuality result (§5.2.6) is proved for the $U(1)$ wrap generator only; the
$SU(2)_L$/$SU(3)_c$ commutators were "not written out," and the 2026-08-07 completeness sweep
downgraded rubric row A6 from `EXACT` to `PARTIAL` on exactly that seam. F312 answers a sharper
question than "run the same check twice more": *why* can a non-Abelian internal index not disturb
Gleason's frame condition, for any group the model might use?

**The current algebra, written out, with an exact $\delta_{xy}$.**

$$[\hat J^a(x),\hat J^b(y)]=i\,\delta_{xy}f^{abc}\hat J^c(x),$$

measured with the off-site piece ($x\ne y$) **literally `0.0`** for both $SU(2)_L$ and $SU(3)_c$ —
not zero to a tolerance. The entire non-Abelian structure is **intra-site**; a measurement context is
a choice of basis on the pointer factor, which is an **inter-site** object, so the structure constants
cannot reach it. The record observable is a gauge singlet **literally**
($[\hat J^a(x),\hat n(y)]=0$, both groups, every site pair) — occupation is what a cell holds, not
what colour or isospin it holds, by construction, so the record cannot resolve the internal index and
the internal index cannot move the record.

$$\boxed{\;\text{the non-Abelian current algebra is exactly intra-site; the record observable is a gauge singlet literally — for both }SU(2)_L\text{ and }SU(3)_c\;}\tag{R5.9}$$

**The theorem: Schur, not case-by-case verification.** A $G$-invariant frame function on
$\mathcal H_p\otimes V$ ($V$ an irreducible unitary representation) averages over $V$ to a multiple of
the identity, so $f(v\otimes\chi)=f_p(v)\cdot c$ with $c$ independent of the internal state, and the
frame condition on $\mathcal H_p\otimes V$ reduces to the frame condition on $\mathcal H_p$ alone —
§5.2.7's dichotomy applies unchanged, **for any compact group and any irreducible representation**,
verified on the Casimir ($C_2=(N^2-1)/2N$, a multiple of the identity to `0.0`/$2.22\times10^{-16}$).
This is why F312 is one theorem rather than two additional special cases: it covers whatever gauge
structure the model adds next (flagged in §5.2.11 for later chapters' non-Abelian sectors).

$$\boxed{\;\text{Schur's lemma makes the internal gauge index drop out of the frame condition, for any compact }G\text{ — not verified per-group but proved once (R5.10)}\;}\tag{R5.10}$$

**A bonus the $U(1)$ case could not have had.** Since $\dim(\mathcal H_p\otimes V)=d_p\cdot N$,
$SU(3)_c$ alone ($N=3$, no pointer needed) clears Gleason's $d\ge3$ premise, so **the $d=2$ hole is
unreachable in any gauge-charged sector** — it would require a total gauge singlet paired with a
two-dimensional pointer. This strengthens rather than merely repeats §5.2.6's dimension result, with
the explicit caveat that $N_c=3$ is F293's *input*, not something this chapter's chain derives (§5.1
item 4).

### 5.2.9 Closing the last external citation: the regularity bridge was already Gleason's own theorem (F329)

§5.2.7's proof is complete for $f\in L^2$. Gleason's theorem needs only *bounded* $f$, and the bridge
— non-negativity forces continuity — was named as external, attributed to Cooke, Keane & Moran
(1985). F329's finding is that this framing was one citation too narrow: Gleason's own 1957 paper
proves the *whole* dichotomy in two independent halves, and the half F304 §5 needed (**Theorem 2.8**:
every non-negative frame function on $S^2\subset\mathbb R^3$ is regular, proved from non-negativity
and compactness alone, via an oscillation-propagation argument on great circles) is already there,
in the same primary source whose *other* half (Theorem 2.3, continuity implies regularity) F304 §5
had already independently re-derived by representation theory without citing it. Combined with
Gleason's Lemma 3.3/Theorem 3.5 (any Hilbert space of dimension $\ge3$, real or complex, reduces to
the 3-dimensional case via completely-real subspaces), this closes for **every dimension this model
actually builds a measurement context on**: $d\in\{3,4,6,64,96\}$ — traced to the specific table cell
in F304/F312 that produces each one, machine-verified (`completely_real_subspace_exists`, literal
`0.0` Gram-matrix deviation for all five), with $d=2$ confirmed to correctly stay excluded as a
negative control.

$$\boxed{\;\text{the regularity bridge is Gleason's own Theorem 2.8 + Theorem 3.5/Lemma 3.3 (1957) — not Cooke–Keane–Moran's alone — verified to transfer to every }d\in\{3,4,6,64,96\}\text{ this model builds a context on (R5.11)}\;}\tag{R5.11}$$

**What this does and does not close.** It closes the last item F304 §5.5 named as external content.
It does **not** re-derive Gleason's Lemmas 2.5–2.7 (the covering/propagation combinatorics underlying
Theorem 2.8 itself) from scratch — those are cited, not reproduced symbol-by-symbol, and F329 is
explicit that this is the one piece of real analysis in the whole chain still resting on a citation
rather than an independent re-derivation (§5.1 item 5's honesty caveat). With this closure,
`docs/status/open-derivations.md` row **A6r** is recorded **fully closed** (2026-08-27) — the whole
chain from F281's two open hypotheses to F329's regularity bridge leaves, per CL264, exactly one
irreducible, definitional premise (§5.1 item 3) and nothing else.

### 5.2.10 Classicality as the block-spin attractor (F281 M3)

Returning to F281's third result, deferred from §5.2.5. Applying the model's own exact block average
$R_b$ (`block_average_field`) to a coherence carrying relative-phase wavevector $k$ gives the closed
form

$$\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2=\left[\frac{\sin(kb/2)}{b\sin(k/2)}\right]^2,$$

verified against the model's actual $R_b$ at nine $(k,b)$ points to $\le8.9\times10^{-16}$.
Populations are exactly marginal ($\lambda_\text{coh}(k{=}0,b)=1.0$ exactly; coarse total charge
matches fine total charge with residual `0.0`, consistent with F130's integer-exact Gauss law), while
coherence is *irrelevant* at $b^{-2}$ in one dimension and $b^{-6}$ in three, vanishing exactly at the
zone edge ($3.7\times10^{-33}$ at $k=\pi$, even $b$) but surviving at long wavelength ($0.9830$ at
$k=2\pi/L$, confirming $R_b$ is selective rather than merely destructive).

$$\boxed{\;\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2\text{, exactly; populations marginal, coherence an irrelevant operator with the }same\text{ leading power }(b^{-2})\text{ as F130's LIV operators (R5.12)}\;}\tag{R5.12}$$

**The physics is in the $k$-dependence, and this is the chapter's clearest genuinely derived (not
merely asserted) statement of classicality.** $k$ measures how distinguishable two superposed
branches are — a genuine cat state carries large $k$ and is crushed under coarse-graining, while a
long-wavelength difference survives. This is the correct qualitative physics ("more macroscopically
distinguishable superpositions decohere under coarse-graining faster"), obtained here as an RG
eigenvalue of an operator the model already owned (F130/F133), not asserted or fitted; coarse-graining
35 decades from the lattice cell to the laboratory scale suppresses a generic coherence by
$\log_{10}\lambda_\text{coh}^\text{total}\approx-143$. **This is the model's classical limit: the IR
fixed point of its own coarse-graining operator is a diagonal density matrix.** It is stated here
precisely rather than inflated: this is a statement about one specific coherence observable under one
specific, exact renormalization operator the model happens to own, not a general theorem that every
possible measure of "classicality" converges to a diagonal state under every possible coarse-graining
scheme.

### 5.2.11 What later chapters inherit from the F312/F329 extension

F312's Schur-reduction argument (§5.2.8) is stated for *any* compact gauge group and *any* irreducible
representation — it does not need to be re-derived when Chapter 12 (hypercharge/electroweak) and
Chapter 13 (colour/strong) build out the full $SU(2)_L\times SU(3)_c$ structure in detail; the
non-contextuality premise of the Born rule is already settled for those sectors by this chapter, and
those later chapters should cite R5.9/R5.10 rather than reopen the question. The one place a *future*
extension could reopen it is falsifier 4 of §5.8 (a reducible internal multiplet) — worth flagging
now, since Chapter 12/13's multiplets (the $SU(2)_L$ doublet, the $SU(3)_c$ triplet) are both
irreducible, but a later composite or reducible structure would not automatically inherit R5.10
without re-checking Schur's premise.

## 5.3 Results table

| # | Statement | Exactness | Source / test record |
|---|---|---|---|
| R5.1 | $[H_\text{int},\hat n(y)]=0$ exactly for the model's own minimal coupling — the pointer observable is forced to be local charge density | exact (literal `0.0`) | F281 §1.1–1.3; `F281-measurement-pointer-born-rg` (20/20, gate) |
| R5.2 | $\{\hat n(x)\}$ is maximal abelian at every tested system size — the unique pointer basis, sharpening with $n$ | exact (commutant-dimension computation) | F281 §1.6; same record |
| R5.3 | Decoherence factor exact in closed form; populations conserved to $4.4\times10^{-16}$; recurrence pushed to $\log_{10}(T_\text{rec}/\tau)\approx4.58\times10^{23}$ ticks | machine (measured) + exact (closed form) | F281 §1.4–1.5; same record |
| R5.4 | Only $\ell^2$ is conserved by a genuine BCC Weyl tick (literal `0.0`); every other tested $p$ changes 3–32% | exact / quantitative | F281 §2.1; same record |
| R5.5 | Envariance forces $p_k=\lvert c_k\rvert^2$ on CA-native gates, exact over $\mathbb Q$; costed against the causal cone, never binding | exact (fine-grained) / quantitative (cost) | F281 §2.2–2.5; same record |
| R5.6 | $\dim\mathcal H_\text{min}=4>2$, structurally; the model's 2-dim subspaces are invariant but unreadable | exact | F304 §1; `F304-born-rule-gleason` (21/21, gate) |
| R5.7 | Non-contextuality is a theorem about $H_\text{int}$: weight spread literal `0.0` across contexts sharing a ray; remote contexts excluded by exact no-signalling (reusing R4.12a) | exact | F304 §2; same record |
| R5.8 | $b_k=(-1)^k/\binom{k+d-2}{k}$ — one closed form for both halves of Gleason's dichotomy, verified as an integer sequence | exact | F304 §5; same record |
| R5.9 | The non-Abelian current algebra is exactly intra-site ($\delta_{xy}$ literal `0.0`); the record observable is a gauge singlet literally, for $SU(2)_L$ and $SU(3)_c$ | exact | F312 §2–3; `F312-born-nonabelian` (18/18, gate) |
| R5.10 | Schur's lemma factors the internal gauge index out of the frame condition, for any compact group and irrep; $SU(3)_c$ alone clears $d\ge3$ | exact | F312 §5–6; same record |
| R5.11 | The regularity bridge is Gleason's own 1957 Theorem 2.8 + Theorem 3.5/Lemma 3.3, transferring machine-exactly to every $d\in\{3,4,6,64,96\}$ this model builds a context on | exact-conditional (rests on citing Gleason 1957, not re-derived from scratch) | F329 §2–4; `F329-gleason-regularity` (8/8, gate) |
| R5.12 | $\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2$ exactly; populations marginal; coherence irrelevant at $b^{-2}$/$b^{-6}$ — the IR fixed point of $R_b$ is a diagonal density matrix | exact (closed form) + quantitative (RG exponents) | F281 §3; `F281-measurement-pointer-born-rg`, same record |

## 5.4 Comparison with measurement

This chapter is, by its own findings' explicit and repeated statement, **not falsifiable by
experiment** — and this is recorded as the correct outcome rather than an evasion. A model built to
reproduce quantum mechanics exactly is *supposed* to be experimentally indistinguishable from
standard QM once it has shown that its own unitary substrate forces the Born rule, the pointer basis,
and a classical limit; distinguishing it from ordinary QM would be a *failure* of the derivation, not
a success. Two operational points are worth stating precisely rather than left implicit:

- **No distinct prediction about measurement statistics is made anywhere in this chain.** Every
  numerical result above (the decoherence factor, the recurrence exponent, the $-143$-decade
  coherence suppression, the RG exponents) is a consequence of ordinary unitary quantum mechanics on
  a specific lattice Hamiltonian, checked against the model's own closed forms, not against any
  external dataset. CL253 and CL264 both state this explicitly in their own falsifier sections: the
  recurrence exponent and macroscopic coherence suppression are "unobservable by construction," and
  a Born-rule derivation that agreed with standard QM's numbers everywhere is exactly what a correct
  derivation should produce.
- **The one place this chapter's results connect to a genuine external comparison is the Bell/CHSH
  question Chapter 1 §1.3 already raised**, and this chapter changes nothing about it: 't Hooft's
  superdeterministic CAI and this project's direct-unitary-evolution route are both, by the sources'
  own account, "consistent with the data" (`t-hooft-2015-cai-summary.md` §5.2). F226's exact
  Tsirelson saturation (cited by F281/CL253/CL264 as cross-reference material, not re-derived in this
  chapter) is the concrete result underlying that statement; nothing in F281/F304/F312/F329 adds a
  new discriminating test between the two readings.

The falsifiers this chapter's claim cards do state (§5.8 below) are therefore all **internal**: a
declared perturbation of the model's own generator or coupling that must turn a specific check red.
None of them is a proposed laboratory measurement.

## 5.5 What was excluded, and why

Grounded in what the four findings and Chapter 1 actually argue, not in general interpretation-of-QM
lore:

- **A 't Hooft-style single privileged ontological basis.** Chapter 1 §1.3 already states this is not
  adopted, on the sources' own authority: "our model does not need this — we evolve the templates
  themselves unitarily on the lattice and reproduce QM directly." This chapter's contribution is to
  show *what the model does instead*: a pointer basis derived from minimal coupling (not postulated),
  and a Born rule derived from Gleason's theorem forced by the rule's own structure (not derived from
  a privileged classical state). Neither route is shown to be *superior*; both are shown, by the
  sources' own account, to reproduce the same observable predictions.
- **A many-worlds-style branching postulate.** No branching axiom is introduced anywhere in this
  chain. The "branches" of F281's envariance argument (§5.2.3) are ordinary superposition terms of a
  single unitary state, never separately reified as physically distinct worlds; the model's account
  of why an observer sees one outcome is decoherence into an einselected pointer basis (§5.2.1) plus
  the model's own unresolved agnosticism about what, if anything, is "really" picked out (Chapter 1
  §1.3), not a postulated multiplicity of realized branches.
- **Explicit collapse dynamics (GRW/CSL/Diósi–Penrose-style).** Not needed and not added. F227
  (cited, not re-derived here) shows the model's intrinsic decoherence floor is either exactly zero
  (effective theory) or Planck-suppressed to $\lesssim10^{-40}\,\text{s}^{-1}$ (substrate), sitting
  below every current collapse-model bound; this chapter's own recurrence argument (§5.2.1, R5.3)
  is the positive statement that a genuinely unitary theory's account of "no un-collapse is ever
  observed" is a large-exponent postponement, not an objective-collapse mechanism.
- **The Schlosshauer–Fine route to the Born rule, left open rather than repaired.** Leg 2 (§5.2.3)
  is not excluded as *wrong* — it is a genuine, independently interesting argument — but this chapter
  does not rely on it once §5.2.6–5.2.9 close leg 1's hypothesis by an independent route. Presenting
  leg 2 as closed by the Gleason chain would misstate what F304's own text says ("leg 2 is not
  repaired — it is unnecessary").
- **A non-minimal coupling anywhere in the model.** Not merely absent by oversight — actively
  excluded by CLAUDE.md's Core Design Decision 3 (P6), and every uniqueness argument in this chapter
  is conditional on that exclusion holding, named explicitly as a falsifier (§5.8).

## 5.6 What is still open

Revisiting Chapter 1 §1.7 item 1 directly, as the assignment brief requires, rather than assuming it
resolved: *"Whether a deeper deterministic substrate exists beneath the per-cell amplitude of P4/P5
is genuinely unsettled in the sources... this is the single most consequential open item in this
chapter [Chapter 1]."*

**This chapter's work does not close that question, and says so at every falsifier it states.**
What it does do is narrow a *different*, related question: not "does a hidden ontic layer exist,"
but "does the model's own unitary substrate, with no such layer, actually *suffice* to reproduce the
pointer basis, the Born rule, and classicality on its own terms." Before this chapter's four findings,
that second question was genuinely open — the model *used* the Born rule and a classical limit
throughout the tree (F212, F222, F226 and others) without ever deriving either. F281/F304/F312/F329
answer it in the affirmative, on the model's own construction, with no collapse term and no
privileged basis added. That is a real result, but it is a **sufficiency** result, not a
**necessity** or **uniqueness** result relative to 't Hooft's alternative: nothing in this chapter
shows that a hidden deterministic layer *cannot* also exist beneath the same amplitude, and every
relevant falsifier section (CL253, CL264) states plainly that the two readings remain experimentally
indistinguishable. **Chapter 1's open item 1 is therefore exactly as open as Chapter 1 left it, in
the specific sense of "which reading is true" — but the case for *not needing* the hidden layer is
now substantially stronger than a bare assertion**, because it rests on four completed derivations
rather than a stated intention. Readers should not mistake "the model doesn't need a hidden ontic
layer to reproduce QM" (shown here) for "no hidden ontic layer exists" (not addressed, and per the
sources, not addressable by any test proposed to date).

Three further open items, each named honestly by the findings themselves and reported rather than
smoothed over:

1. **The one irreducible premise** (§5.1 item 3): "an exhaustive set of records carries weights
   summing to one" is definitional, and every derivation of the Born rule — this chain's included —
   ends there. This is not a gap to be closed by more work; it is the honest floor of the regress.
2. **F329's closure rests on a citation, not a full re-derivation**, and is explicit about exactly
   which piece: Gleason's own Lemmas 2.5–2.7 (the covering/propagation combinatorics of Theorem 2.8)
   are cited, not reproduced symbol-by-symbol, retrieved via automated PDF extraction rather than a
   character-by-character read of the original scan (cross-checked across three independent
   fetches, per F329 §5, but not verified against the typeset page images). This is the one place in
   the whole F281→F304→F312→F329 chain where "exact" (as recorded in the results table) means "the
   arithmetic this session checked is exact" rather than "every step was independently re-derived
   from first principles."
3. **$N_c=3$ remains an input**, not a derivation, for F312's dimension bonus (§5.2.8); if a later
   chapter's own derivation of $N_c$ (Chapter 13, per `00-plan.md`'s CL281/CL287 material) were to
   revise it, F312's "colour alone clears $d\ge3$" consequence would need re-checking, though the
   Schur-reduction theorem itself (R5.10) is $N$-independent by construction.

> **Gap [G-4]:** `docs/claims/CL253-measurement-pointer-born-rg.md` (last verified 2026-08-05) states,
> under "Scope limit carried from F281 §'Remains'," that the pointer-basis diagonality argument (M1,
> R5.1 above) "is proved explicitly for the $U(1)$ wrap generator... the explicit non-Abelian
> commutator has not been written out. Widening it is named as the next step in F281." F312
> (2026-08-11) explicitly writes out exactly this commutator for the non-contextuality premise of
> the *Born rule* (G3: $[\hat J^a(x),\hat n(y)]=0$ literally, for both $SU(2)_L$ and $SU(3)_c$,
> every site pair) — and this is the identical operator identity the *pointer-basis* diagonality
> argument of §5.2.1 needs for the non-Abelian couplings, since $H_\text{int}=\sum_x\hat
> A^a(x)\otimes\hat J^a(x)$ diagonal in $\hat n(y)$ is exactly $[\hat J^a(x),\hat n(y)]=0$. F312's own
> header explicitly states it "closes" F281's open item 2. Yet `CL253` — the claim card that actually
> carries the pointer-basis statement (R5.1/R5.2) — has never been updated to record this, and still
> reads as if the non-Abelian gap for *its own* diagonality claim (as opposed to CL264's
> non-contextuality claim) is open. Whether this is a genuine remaining gap (perhaps the pointer-basis
> argument needs something beyond F312's G3, not examined here) or simply an un-propagated claim-card
> update is not resolved by this chapter, which is documentation-only and out of scope for editing
> claim cards; flagged here rather than silently treated as either closed or open. Logged in
> `docs/monograph/GAPS.md`.

## 5.7 Falsifiers

All internal — declared parameter perturbations of the model's own gate records, verified in this
session's tests to fire on exactly their own leg, per D9. None is a proposed experimental test (§5.4).

- **A non-minimal coupling required anywhere in the model** (a Yukawa scalar, a derivative coupling,
  any term not built from $\hat n(x)$ or its non-Abelian analogue $\hat J^a(x)$). Falsifies both the
  pointer-basis uniqueness argument (R5.1) and the non-contextuality premise (R5.7, R5.9) at a stroke,
  since both are exactly the *absence* of such a term. Tested: `--param coupling=nonminimal` reddens
  M1a/M1b/M1f; `--param coupling=contextual` reddens B2a/B2b.
- **A breach of exact locality or no-signalling** (R4.12a/R4.12b, Chapter 4). Would restore remote
  contextuality (F304 §2.3) and undercut the causal-cone cost argument of leg 2 (§5.2.3). Tested:
  `--param locality=nonlocal` reddens B3a.
- **A measurement context of total dimension 2 ever exhibited on this lattice.** Would make the
  $11$-, $22$-dimensional non-Born families of §5.2.7 physically realizable and break the derivation
  at its dimension premise. Tested: `--param gleason_dim=2` reddens B5a.
- **A measured $b_k$ (R5.8) or $\lambda_\text{coh}$ (R5.12) departing from its closed form beyond the
  stated machine floor.** Tested: `--param zonal=naive` reddens B7a; nine $(k,b)$ points checked
  directly for $\lambda_\text{coh}$.
- **A reducible internal gauge multiplet.** Schur's reduction (R5.10) gives a scalar only on an
  irreducible block; a reducible representation would make the frame function block-dependent, i.e.
  contextual in a new way. Both multiplets currently in the tree ($SU(2)_L$ doublet, $SU(3)_c$
  triplet) are irreducible, so this is a live falsifier for a *future* multiplet, not a present defect
  (§5.2.11).
- **A gauge-charged sector with a two-dimensional total Hilbert space.** Would restore the $d=2$ hole
  in a charged sector against F312's $\dim=d_pN$, $N\ge2$ arithmetic.
- **The regularity-bridge control failing to redden its own legs**, or the completely-real-subspace
  check failing for any of the five listed model dimensions, or the $d=2$ negative control passing.
  Any of these would mean F329's transfer of Gleason's Theorem 3.5 to this model's actual construction
  does not hold, reopening A6r. Verified: `--param control=True` reddens H2/H3 only.

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–4's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $H_\text{int}$ | The system–environment (or system–record) generator forced by minimal coupling, $\sum_x\hat\alpha(x)\otimes\hat n(x)$ ($U(1)$) or $\sum_x\hat A^a(x)\otimes\hat J^a(x)$ (non-Abelian); the object whose diagonality forces the pointer basis and whose context-blindness forces non-contextuality. | §5.2.1, §5.2.8 |
| $\hat J^a(x)$ | The site-local non-Abelian current, $\psi^\dagger(x)T^a\psi(x)$; the intra-site current algebra $[\hat J^a(x),\hat J^b(y)]=i\delta_{xy}f^{abc}\hat J^c(x)$ is exact. | §5.2.8 |
| $R_b$ | The model's exact block-average (renormalization) operator (F130/F133), whose coherence eigenvalue $\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2$ is this chapter's classicality result. | §5.2.10 |
| $D_b(k)$ | The Dirichlet kernel, $\tfrac1b\sum_{j=0}^{b-1}e^{ikj}$, whose squared modulus is $\lambda_\text{coh}$. | §5.2.10 |
| $b_k$ | The eigenvalue of the frame-condition averaging operator $B$ on the $k$-th isotypic component of $L^2(\mathbb{CP}^{d-1})$; $b_k=(-1)^k/\binom{k+d-2}{k}$, the closed form giving both halves of Gleason's dichotomy. | §5.2.7 |
| $V$ | The internal (gauge) Hilbert-space factor carrying a unitary irrep of $G$ ($V=\mathbb C^2$ for $SU(2)_L$, $\mathbb C^3$ for $SU(3)_c$), as distinct from the pointer factor $\mathcal H_p$. | §5.2.8 |

---

*New gap logged this chapter: **G-4** (§5.6), also recorded in `docs/monograph/GAPS.md`. No finding,
claim card, module, or test record was created or modified in the writing of this chapter.*
