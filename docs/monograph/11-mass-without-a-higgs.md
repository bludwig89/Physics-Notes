# Chapter 11 — Mass Without a Higgs: Complex Mass, Chiral $SU(2)$ from $\beta$-Gauging

*Chapter 11 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F27-complex-mass-chiral-su2.md`, `findings/F40-quark-f27-mass-and-electroweak.md`,
`findings/F85-p0-dynamical-fermions.md`, and `findings/F167-restmass-from-rule-zero-k-rotation.md`
— the four findings `00-plan.md` §2 assigns to this chapter, all read in full — plus
`references/physics-notes-complete.md` pp. 59–69 (Ludwig's original 2007 notebook pages,
"Complex mass" through the weak-interaction/Weinberg–Salam-without-Higgs sketch, read directly
rather than only through Chapter 1's summary of them), `docs/monograph/01-postulates-and-ontology.md`
§1.2 (P5, P6 — this chapter derives P6's consequences; it does not re-argue P6's adoption),
`docs/monograph/04-structural-theorems.md` §4.2.7 (R4.10/R4.11, F378's discrete-CPT extension to
the $SU(2)_L$-gauged sector — a proved theorem for the kinetic term and a proved no-go for the
gauged mass mechanism, engaged in full in §11.5 below), and
`docs/monograph/06-free-propagation-light-cone.md` §6.2.6 (R6.10/R6.11, the spherical-Pythagorean
mass-shell identity, which already forward-cites this chapter's construction for
$\Omega_\text{rest}(m)=\arcsin m$ and is completed here). Checked directly against
`docs/theory/supersessions.yaml` (grepped for all four finding numbers: **zero hits** — none of
F27/F40/F85/F167 appears in any of the 23 supersession records) and against `claims-index.md`:
**CL003** (F27, F41; `tier: headline`, `status: live`, `exactness: machine`) is this chapter's
headline card, resting on F27 for its mass-mechanism half — F41 (hypercharge) is Chapter 12's
territory and is not re-derived here, consistent with CL003 itself resting on both findings while
this chapter covers only the mass half. **CL047** (F40), **CL080** (F85) and **CL147** (F167) are
supporting cards, all seeded 2026-08-04 at `review_state: unreviewed-seed` (extracted mechanically
from their findings, not yet independently confirmed) — this is reported as-is, not silently
upgraded. Notation, postulates and results are those of Chapters 1, 4 and 6 — $\psi$, $D(\mathbf
k)$, $\Theta$, $\Omega(\mathbf k)$, $c_\text{lat}$, $U(x)$ — extended, never redefined.*

## 11.0 What this chapter establishes

Chapter 1 posed P6 as a postulate and explicitly declined to derive it: "Complex mass is not
introduced by a fundamental scalar (Higgs) field... It is introduced by *gauging* an ambiguity
already present in how the spinor's own matrix representation is chosen from point to point... its
detailed construction and consequences are derived in full only in Chapters 11–12"
(`01-postulates-and-ontology.md` §1.2). This chapter is where that promise is kept for the mass
mechanism itself (Chapter 12 keeps it for hypercharge and the boson spectrum). Four questions are
answered, each closed by one of the four assigned findings:

1. **What, concretely, is the ambiguity Ludwig gauges, and what local structure does gauging it
   produce?** Answered by re-deriving `physics-notes-complete.md` pp. 59–60 directly (§11.2.1–11.2.2).
2. **Is the resulting chiral-$SU(2)$ complex-mass step a genuine, exactly unitary, exactly
   gauge-covariant construction, or only a formal sketch?** Answered by F27, which formalizes it as
   an explicit per-cell unitary and proves nine algebraic/numerical properties to machine precision
   or exactly (§11.2.3).
3. **Does the mechanism survive contact with the quark sector and with a dynamical (rather than
   merely algebraic) gauge field, and is it a genuine real-time propagating object rather than a
   formal identity?** Answered by F40 (quark-sector port + electroweak wiring, §11.2.4) and F85
   (P0 certification of $e,u,d$ as real, non-dispersing wavepackets, §11.2.5).
4. **In what sense is the resulting rest mass *forced* by the rule, rather than an arbitrary
   inserted parameter, and how does it relate to the rotation-rate reading of $c_\text{lat}$ that
   Chapter 6 already used?** Answered by F167, which proves the mass term is the unique admissible
   zero-$\mathbf k$ deformation of the rule and identifies rest mass as the $\mathbf k=0$ intercept
   of the same generator whose $\mathbf k\to0$ slope is $c_\text{lat}$ (§11.2.6).

The chapter also engages directly, rather than around, the one place a prior chapter found a
genuine obstruction touching this exact mechanism: R4.11's proof that no fixed isospin operator
extends the discrete CPT theorem to the $SU(2)$-gauged mass sector. §11.5 states precisely what
that no-go does and does not say about the construction built here.

## 11.1 Inputs

**Postulates used.** **P5** — the massless two-component Weyl spinor primitive
(`01-postulates-and-ontology.md` §1.2) — is the field this chapter's mechanism acts on: mass is not
carried by the primitive field itself, but "clothed" onto it, per Ludwig's own stated preference
that "mass is and ought to be generated by the interactions of... particles and their associated
fields" (`physics-notes-complete.md` p. 10, quoted already in Ch.1). **P6** — the postulated chiral
$SU(2)$ connection $U(x)$ replacing a fundamental Higgs field — is the postulate whose *mechanism*
this chapter derives; P6 itself is not re-argued or re-justified here (that adoption decision, and
its motivation, are Chapter 1's job, already done).

**Prior results used.** **R4.10/R4.11** (`04-structural-theorems.md` §4.2.7) — the SU(2) pseudoreal
extension of the discrete CPT theorem to the gauged *kinetic* term (proved, fixed background), and
the proved no-go that no fixed isospin operator extends it to the gauged *mass* mechanism this
chapter builds (an automorphism/anti-automorphism obstruction, general for non-abelian groups). This
chapter does not re-derive R4.10/R4.11; it uses them as the binding constraint checked against
§11.2.3's construction in §11.5. **R6.10/R6.11** (`06-free-propagation-light-cone.md` §6.2.6) — the
spherical Pythagorean identity $\cos\Omega_\text{Dirac}(\mathbf k,m)=\sqrt{1-m^2}\cos\omega_\text{
kin}(\mathbf k)$ and its continuum limit $E^2=m^2c^4+p^2c^2+O(\text{lattice}^4)$ — already used
$\Omega_\text{rest}(m)=\arcsin m$ "through its rotation angle... used here only through its rotation
angle" with an explicit forward-citation to this chapter's construction; §11.2.6 supplies the
derivation Chapter 6 borrowed in advance.

**Free inputs consumed — read this carefully, it is the load-bearing accounting for this chapter.**
The mechanism derived here fixes the **structural form** of mass completely and to closed form: that
a mass term exists at all, that it is the *unique* admissible $\mathbf k$-independent deformation of
the free rule (not one arbitrary choice among many), that it is necessarily a rotation angle
$\Omega_\text{rest}(m)=\arcsin m$, that the companion pseudoscalar direction is provably pure gauge,
and that the whole construction carries an exact local $SU(2)_L$ gauge symmetry with the correct
weak-isospin quantum numbers — all exact or machine-precision results, none of them free parameters.
It does **not** fix the **numerical value** of any mass. F167's own T6 check is explicit: "every
$m\in(0,1)$ gives an equally-unitary admissible rule" — the bare rule leaves each flavor's $m$ free.
Concretely: F27's tests run at a representative $m=0.3$; F40's quark-sector tests use representative
$m_u,m_d,m_s$ chosen so that $m_d/m_u\approx4$, $m_s/m_u\approx16$ **by construction**, to exercise
the mechanism, not because those ratios were derived; F85's P0 certification is explicit that its
"representative dimensionless lattice masses... are test values, not physical — that is a P6/scale
concern" (F85, "What was certified"). So this chapter's contribution to the monograph-wide
free-parameter ledger (Appendix A3) is: **zero new free parameters in the structural mechanism, and
one free continuous parameter per fermion flavor ($m_f$) in the mechanism's numerical content** —
exactly mirroring how Chapter 1 already logged P1 and P6 as the two *structural* free choices, with
the *numerical* mass values a separate, still-open ledger line. F167's own closing note flags that
this line is not permanently open: F144 (dimensional transmutation of the derived strong coupling,
not one of this chapter's assigned findings) is reported to fix the overall mass scale "to a factor
$\sim1.9$ with no tuning," and F233 supersedes F119's "no running channel" no-go on that basis — both
belong to Chapter 13 (colour) and Chapter 17 (SI closure) respectively, and are forward-cited, not
re-derived, here. Mass **ratios** within and across generations (the crystal-field hierarchy, Koide,
the $2/9$ shape angle) are Chapter 15's territory, built on top of this chapter's mechanism, not
supplied by it.

## 11.2 The derivation

### 11.2.1 Ludwig's starting observation: the Dirac $\alpha,\beta$ matrices are not unique

The ordinary Dirac equation is obtained by taking a matrix square root of the relativistic energy
relation: writing $i\hbar\,\partial_t\Psi=i\hbar c\,\vec\alpha\cdot\nabla\Psi+\beta m_0c^2\Psi$
requires
$$\left(\vec\alpha\cdot\vec p\,c+mc^2\beta\right)^2=(p^2c^2+m^2c^4)\,\mathbb I,\tag{11.1}$$
which fixes only the **algebra** the $\vec\alpha,\beta$ matrices must satisfy (mutual anticommutation,
each squaring to $\mathbb I$) — not a unique representation. Ludwig writes down the familiar
$\alpha_i=\sigma_3\otimes\sigma_i$, $\beta=-\sigma_1\otimes\sigma_0$, then makes the observation this
whole chapter is built on:

> "Interestingly, the choice of these matrices need not be unique... We might simply look at the
> fact that one could just as well write $\beta=(a\sigma_1+b\sigma_2)\otimes\sigma_0$ where
> $a^2+b^2=1$ and get the same solution of (3) above. Normally this choice of the $\alpha$ and $\beta$
> are considered arbitrary, and left at that." (`physics-notes-complete.md` p. 59)

That is: $\beta=\cos\theta\,\sigma_1\otimes\sigma_0+\sin\theta\,\sigma_2\otimes\sigma_0$ for *any*
fixed angle $\theta$ solves the same algebraic equation (11.1) and gives the same physics — a global,
one-parameter internal ambiguity in how the mass term is represented, present in the free theory and
normally discarded as a convention.

$$\boxed{\;\text{the Dirac }\beta\text{ matrix admits a one-parameter family }\beta(\theta)=(\cos\theta\,\sigma_1+\sin\theta\,\sigma_2)\otimes\sigma_0\text{, all solving (11.1) identically}\;}\tag{R11.1}$$

(`physics-notes-complete.md` p. 59; a constructive/algebraic observation, not a test-record result —
verified trivially by direct substitution, and re-derived independently and more completely by F167
T2 in §11.2.6 below.)

### 11.2.2 Gauging the ambiguity: the local connection $U(x)$

Page 60 makes the ambiguity local. Writing the representative $\beta$ of p. 59 as $\beta_g=(U\sigma_1
U^+)\otimes\sigma_0$ with $U=\mathrm{diag}(1,e^{i\theta})$ reproduces the same one-parameter family;
promoting $\theta\to\theta(x)$ turns a convention into a field:

> "Suppose, however, that these representations were gauged, so that they weren't the same from
> point to point. This seems to introduce an $SU(2)$ gauge symmetry of sorts into the system... It
> is fascinating to note that such a gauge symmetry acts on only one half of the bispinor. In this,
> the Weyl representation, that half of the bispinor corresponds to one particular helicity. This
> would seem to tie in with the weak interaction, which is also helicity-dependent and *thus related
> to mass*..." (`physics-notes-complete.md` p. 60)

This is the entire seed of the chapter: (i) the representation freedom in how mass is written down is
gauged into a genuine local field $U(x)$; (ii) because $\beta$ mixes chirality sectors (it is the
matrix that couples $\eta\leftrightarrow\chi$ in the Weyl basis), gauging it necessarily acts
chirally — on the left-handed sector only in the doublet extension — which Ludwig immediately flags
as the qualitative signature of the weak interaction, three pages before writing down a
Weinberg–Salam-shaped Lagrangian (p. 62) without ever introducing a Higgs field.

$$\boxed{\;\text{gauging }\theta\to\theta(x)\text{ in }\beta_g=(U\sigma_1U^\dagger)\otimes\sigma_0\text{ produces a local field that acts chirally, tying mass generation to helicity structure}\;}\tag{R11.2}$$

(`physics-notes-complete.md` p. 60.) Pages 61–69 carry this seed forward into a full sketch of
Weinberg–Salam without a Higgs field — $SU(2)\times U(1)$ gauge fields, the $W^\pm,Z,\gamma$
mixing, the Weinberg-angle relation $g'/g=\tan\theta_W$ (p. 64), mass terms for the gauge bosons
themselves, and the charged/neutral-current diagrams (p. 69). That material is **hypercharge and
electroweak-boson territory** — Chapter 12's assigned findings (F29, F31–F36, F41 et al.) formalize
it — and is not re-derived here; this chapter's scope is bounded to the fermion **mass** mechanism
alone, per the task brief and per CL003's own findings list (F27, not F41).

### 11.2.3 F27: the complex-mass step, formalized and verified

F27 (2026-05-23) turns pp. 59–60's sketch into an explicit, testable per-cell unitary. For a single
flavor, define $c_m=\cos(m\,dt)$, $s_m=\sin(m\,dt)$ and the mass step
$$\begin{pmatrix}\eta_\text{new}\\\chi_\text{new}\end{pmatrix}=\underbrace{\begin{pmatrix}c_m&is_me^{i\theta}\\is_me^{-i\theta}&c_m\end{pmatrix}}_{M(\theta)}\begin{pmatrix}\eta\\\chi\end{pmatrix}.\tag{11.2}$$

**Unitarity holds for every $\theta(x)$.** Writing $A=\begin{psmallmatrix}0&e^{i\theta}\\
e^{-i\theta}&0\end{psmallmatrix}$, $A$ is Hermitian with $A^2=\mathbb I$, so $M=c_m\mathbb I+is_mA$
satisfies $M^\dagger M=\mathbb I$ exactly — not an approximation valid for small $\theta$, an
algebraic identity for any $\theta(x)$ at all. Verified: norm drift over 50 steps with random
$\theta(x)$, $m=0.3$, $L=32$ gives residual $1.332\times10^{-15}$ (T1).

**The $SU(2)$ doublet extension.** For an isospin doublet $(\nu,e)$, replace the scalar $e^{i\theta}$
with $U(x)\in SU(2)$ acting on the isospin index alone:
$$\eta_\text{new}=c_m\,\eta+is_m\,(U\otimes\mathbb I_\text{spin})\,\chi,\qquad
\chi_\text{new}=is_m\,(U^\dagger\otimes\mathbb I_\text{spin})\,\eta+c_m\,\chi.\tag{11.3}$$
$A=\begin{psmallmatrix}0&U\otimes\mathbb I\\U^\dagger\otimes\mathbb I&0\end{psmallmatrix}$ is again
Hermitian with $A^2=\mathbb I$ (since $UU^\dagger=\mathbb I$), so unitarity holds by the identical
argument — residual $2.520\times10^{-14}$ over 40 steps with a random $SU(2)$ field, $m=0.3$, $L=24$
(T2).

$$\boxed{\;M(\theta)\text{ and its }SU(2)\text{ doublet extension are exactly unitary for every }\theta(x),U(x)\text{: }1.3\times10^{-15}\text{ (single flavor), }2.5\times10^{-14}\text{ (doublet)}\;}\tag{R11.3}$$

**The key result: chiral $SU(2)$ is an exact local gauge symmetry of the mass step alone.** The Ward
identity
$$V(x)\cdot\text{mass\_step}(\psi;\,U)=\text{mass\_step}\bigl(V(x)\cdot\psi;\,V(x)\cdot U\bigr)\tag{11.4}$$
holds — with $V(x)\in SU(2)$ acting **only** on the left-handed doublet $\eta$, right-handed $\chi$
untouched — to residual $1.055\times10^{-17}$ (T5, "the key test"). This is the mass mechanism's own
statement of P6: mass and the gauge symmetry are not two separately-imposed structures, they are the
*same* algebraic object read two ways.

$$\boxed{\;V(x)\cdot\text{mass\_step}(\psi;U)=\text{mass\_step}(V\!\cdot\!\psi;V\!\cdot\!U)\text{ to }1.055\times10^{-17}\text{ — chiral }SU(2)_L\text{ is exact, derived without a Higgs field}\;}\tag{R11.5}$$

**Chirality is exact, not approximate.** Under the $V(x)$ transform, $\lvert\chi_\text{new}-\chi_
\text{orig}\rvert=0.000\times10^0$ (literal zero) while $\lvert\eta_\text{new}-\eta_\text{orig}
\rvert=1.945$ — the right-handed sector is *identically* unmoved (T6), the defining property of a
chiral gauge theory rather than an approximately-chiral one.

**$U(x)$ plays the Higgs-VEV-direction role while remaining pure gauge.** Starting from a pure $\nu_L$
state and evolving 80 steps at $m=0.3$: with $U=\mathbb I$ the state ends up entirely in $\nu_R$
($0.564$); with $U=i\sigma_1$ it ends up entirely in $e_R$ ($0.564$, same magnitude); a $45°$ mix
splits it evenly (T9) — $U(x)$ steers *which* right-handed component the mass step excites, exactly
the job the Higgs VEV direction performs in the Standard Model. But the physical dispersion
$\omega(\mathbf k)$ is completely independent of $\theta$: maximum eigenvalue deviation across
$\theta\in\{0,\pi/3,\pi/2\}$ is $3.331\times10^{-16}$ (T3) — $U(x)$ carries **no** physical
information; it is pure gauge, never a propagating scalar degree of freedom.

$$\boxed{\;U(x)\text{ selects the mass-step coupling direction (T9, residual }0.564\text{, non-trivial) while the physical dispersion is }\theta\text{-independent to }3.3\times10^{-16}\text{ (T3) — U(x) is pure gauge, not a Higgs boson}\;}\tag{R11.6}$$

**A mass gap forms without a scalar condensate.** With $U=\mathbb I$ (no VEV of any kind) and $m=0$,
a state stays purely left-chiral ($N_R=0.000$ to $4.0\times10^{-15}$); with $m\ne0$, the
right-chirality fraction grows to $N_R=0.820$ after 80 steps (T7). The gap is a direct consequence of
the mass step's off-diagonal structure, with no dynamical scalar sector anywhere in the construction.
Finally, the left-handed $\nu_L$ state carries $T_3=+0.5000000000$ (residual $1.1\times10^{-16}$, T8)
— the correct Standard Model weak-isospin assignment, emerging from the $SU(2)$ structure of the
doublet directly.

$$\boxed{\;\text{a mass gap forms at }U=\mathbb I,\,m\ne0\text{ with zero scalar condensate ({N_R}: }0\to0.820\text{); }\nu_L\text{ carries }T_3=+\tfrac12\text{ exactly}\;}\tag{R11.7}$$

**What F27 itself discloses as not yet shown.** The finding is explicit about two known limitations
carried forward: (1) the free Weyl *kinetic* step alone is not $SU(2)$-invariant — exactly as in the
Standard Model, local gauge invariance of the kinetic term needs a gauge boson $W_\mu$, which the
mass-step-only construction here does not include; (2) quantization (loop corrections, anomaly
cancellation) is untested at the classical-CA level this finding operates at. Both are picked up
immediately by the next finding.

### 11.2.4 F40: the quark sector, and wiring the mass step to a dynamical gauge field

F40 (2026-05-26) closes two deficits a first-generation completeness review had named: quarks still
ran a Higgs–Yukawa-shaped mass path while leptons used F27's mechanism, and the quark doublet
$(u,d)_L$ had zero $SU(2)_L/W_\mu/Z/Y$ wiring at all.

**Phase 1 — porting F27 to quarks (FG-2).** The identical per-cell unitary (11.2) is applied per
flavor per colour; distinct $m_u,m_d,m_s$ give natural mass splitting, and the mass is colour-blind
(only the $SU(3)$ link rotates colour). Unitarity (Q1, $5.4\times10^{-15}$), the U(1) $\beta$-gauge
Ward identity per flavor (Q2, $1.2\times10^{-16}$), the mass gap without a Higgs (Q3), $\theta$-pure-
gauge invariance (Q5, $2.8\times10^{-14}$), colour neutrality (Q6, $1.1\times10^{-16}$), an exact
cold-link regression to nine independent F27 single-flavor steps (Q7, exact $0$), colour-charge
conservation (Q8, $1.7\times10^{-14}$), and the degenerate-doublet $SU(2)_L$ Ward identity (Q9,
$8.4\times10^{-17}$) all reproduce F27's leptonic results in the quark sector.

**The predicted failure modes fire exactly as F27 named them, and only as diagnostics, not
regressions.** With an explicit mass split $m_u\ne m_d$, the $SU(2)_L$ Ward identity breaks at
residual $2.4\times10^{-1}$ (Q10); with a spatially varying $V(x)$ and no $W_\mu$, the full (kinetic
+ mass) step breaks Ward invariance at $5.7\times10^{-1}$ (Q11). These are exactly F27's own "Known
Limitation 1" (the kinetic step is not $SU(2)$-invariant alone) made concrete, deliberately triggered
and correctly diagnosed rather than papered over.

$$\boxed{\;\text{split mass or a varying }V(x)\text{ without }W_\mu\text{ breaks Ward invariance at }O(1)\text{ (Q10/Q11) — exactly F27's own predicted failure mode, confirming the mechanism is understood, not merely fitted}\;}\tag{R11.8}$$

**Phase 4 — electroweak wiring restores it (FG-3).** Coupling the doublet to a dynamical $SU(2)$ link
field $W_\mu(x)$ (the 2D-square analog of the lepton-sector machinery Chapter 12 covers in full)
restores the $SU(2)_L$ Ward identity to machine precision for spatially uniform $V(x)$: residual
$2.8\times10^{-16}$ (QE2), matching the lepton-sector analog to within an order of magnitude. The
right-handed singlet $\chi$ stays exactly decoupled from $W$ at $m=0$ (QE3, exact $0$), and for
smoothly varying $V(x)$ the residual scales as $O(a\lvert\nabla V\rvert L)$ and vanishes in the
continuum limit (QE5) — the same lattice-spacing-suppressed behaviour the lepton sector shows.

$$\boxed{\;\text{coupling the doublet to a dynamical }W_\mu\text{ restores the }SU(2)_L\text{ Ward identity to }2.8\times10^{-16}\text{ (QE2); }\chi\text{ stays exactly decoupled at }m=0\text{ (QE3)}\;}\tag{R11.9}$$

**Scope note, carried forward exactly.** FG-3 delivers $SU(2)_L$ wiring only. Hypercharge, the
Weinberg mix, and the absolute $W$/$Z$ mass spectrum are explicitly left to Chapter 12 (F40's own
"Relation to prior findings" table names F35, electroweak mixing, as still pending). Nothing in this
section derives an absolute electroweak boson mass; the wiring is a proof that the mass mechanism and
a dynamical gauge connection are jointly consistent, not yet a spectrum calculation.

### 11.2.5 F85: certification as genuine dynamical wavepackets, not merely a formal identity

Everything so far is an algebraic/Ward-identity result about a one-tick unitary map. F85 (2026-06-03)
asks whether the mechanism, applied to the model's actual first-generation matter content, produces
genuine, real-time, measurably massive propagating objects — a different and stronger claim than
"the step is unitary."

Using representative lattice masses $m_e=0.05,\,m_u=0.10,\,m_d=0.40$ (the $d\!:\!u\approx4$ ratio
honouring F40's splitting, again test values, not physical), each of the electron, up- and down-quark
is certified as:

| Check | What it verifies | Result |
|---|---|---|
| Exact dispersion (A1) | Eigenphase of $D_{\mathbf k}$ matches the analytic $\arccos$ form | $2$–$3\times10^{-16}$, all three species |
| Group velocity (A2) | An on-axis real-time Weyl packet propagates at $c_\text{lat}=1/\sqrt3$ | relative $1.1\times10^{-4}$ |
| Norm conservation (B) | No leakage over 1000 ticks | $2.4$–$2.7\times10^{-13}$ |
| Zitterbewegung (C) | $k=0$ chirality oscillation at $\omega_Z=2\arcsin(m)$ | relative $5\times10^{-5}$–$1.2\times10^{-3}$ |
| Electric charge (D) | $Q=T_3+Y/2$ exactly over $\mathbb Q$ | $-1,\,+2/3,\,-1/3$ exact |
| Colour charge (E1–E3) | Conserved, pointwise-covariant, norm-conserved for $u,d$ | $10^{-13}$–$10^{-15}$ |

$$\boxed{\;e,u,d\text{ propagate as genuine real-time wavepackets: correct group velocity, machine-precision norm conservation over }10^3\text{ ticks, zitterbewegung at }\omega_Z=2\arcsin(m)\text{, exact charge, conserved colour}\;}\tag{R11.10}$$

The zitterbewegung result is the direct dynamical confirmation of $\Omega_\text{rest}(m)=\arcsin(m)$:
at $k=0$, the mass step's off-diagonal coupling mixes the chirality eigenstate between eigenphases
$\pm\arcsin m$, so the left–right population genuinely oscillates in real time at frequency
$2\arcsin m$, matching the formal identity §11.2.6 derives to $5\times10^{-5}$–$1.2\times10^{-3}$
relative precision by direct time-domain measurement, not by re-deriving the algebra.

**Scope, stated by F85 itself.** "P0 certifies single particles. It does **not** yet bind them...
The representative masses are not physical; absolute MeV awaits P6 (scale fixing, CO-1/F83)" — the
same free-input accounting §11.1 already gives: this chapter's mechanism, checked here against
genuinely dynamical propagation, still carries the mass *magnitude* as a free input per flavor.

### 11.2.6 F167: rest mass as the unique zero-$\mathbf k$ rotation rate — the bridge to Chapter 6

F167 (2026-06-29) answers a sharper question than §11.2.3–11.2.5's construction-and-verification: is
the mass term *forced* by the rule at all, or is it an arbitrary addable structure that merely
happens to be unitary? It separates this into a **structural** question (is mass forced, and forced
to be a rotation rate?) and a **magnitude** question (what is the value of $m$?), and closes the
first exactly.

**Step 1 — the mass term is the unique admissible deformation.** The one-tick Dirac update in Fourier
space is $D_{\mathbf k}=\begin{psmallmatrix}nW_{\mathbf k}&im\mathbb I_2\\im\mathbb I_2&nW_{\mathbf
k}^\dagger\end{psmallmatrix}$. Unitarity forces the kinetic rescale $n=\sqrt{1-m^2}$ — any other $n$
breaks $D_{\mathbf k}^\dagger D_{\mathbf k}=\mathbb I$ (correct $n$: residual $2\times10^{-16}$; a
$5\%$-wrong $n$: residual $\sim0.1$; T1). Among the sixteen Hermitian Dirac covariants, a
$\mathbf k$-independent (rest) term that can gap the spectrum must be simultaneously
**chirality-off-diagonal** (anticommute with $\gamma^5$, to couple $\eta\leftrightarrow\chi$) and a
**spin-rotation scalar** (commute with $\Sigma_i=\tfrac12\mathrm{diag}(\sigma_i,\sigma_i)$, to survive
at rest without breaking $SO(3)$). Exactly **two** of sixteen satisfy both: $\gamma^0$ (the physical
mass $m$) and $\gamma^0\gamma^5$ (the chiral phase $\theta$) — T2.

**This is the group-theoretic explanation of R11.1's ambiguity.** Ludwig's two-parameter family
$\beta(\theta)=(\cos\theta\,\sigma_1+\sin\theta\,\sigma_2)\otimes\sigma_0$ (p. 59) *is* exactly the
$\{\gamma^0,\gamma^0\gamma^5\}$ pair F167 derives as the complete, unique set of admissible rest
covariants — not a coincidence of representation choice, but the full content of "how many ways can a
$\mathbf k$-independent chirality-mixing, spin-scalar term be written," which turns out to be
one physical amplitude times one gauge phase, and nothing else.

$$\boxed{\;\text{unitarity forces }n=\sqrt{1-m^2}\text{; exactly 2 of 16 Dirac covariants are simultaneously chirality-off-diagonal and spin-scalar} - \gamma^0\text{ (mass) and }\gamma^0\gamma^5\text{ (pure-gauge phase) - matching R11.1's ambiguity exactly}\;}\tag{R11.11}$$

**Step 2 — rest mass is the zero-$\mathbf k$ eigen-rotation.** At $\mathbf k=0$, $W_0=\mathbb I$, so
$D_0=n\mathbb I_4+im\gamma^0=\exp(-i\Omega_\text{rest}A)$ with $A^2=\mathbb I$ and eigen-phases
$\pm\Omega_\text{rest}$, giving
$$\Omega_\text{rest}(m)=\arcsin m,\qquad\cos\Omega_\text{rest}=\sqrt{1-m^2}=n\tag{11.5}$$
exactly (T3) — this is the identity R6.10 already used, here supplied as a *conclusion* rather than
an identification: given Steps 1–2, rest mass **must** be a rotation angle, because it is the
$\mathbf k=0$ value of the rule's own eigen-phase, not a separately chosen functional form.

$$\boxed{\;\Omega_\text{rest}(m)=\arcsin m,\quad\cos\Omega_\text{rest}=\sqrt{1-m^2}\;}\tag{R11.12}$$

**Step 3 — the chiral phase is pure gauge, re-derived from the rest-phase spectrum.** The rest
eigen-phase is independent of $\theta$ to $2.2\times10^{-16}$ across $\theta\in\{0,0.7,\pi/3,1.9\}$
(T4) — the same conclusion as F27's T3 (§11.2.3), reached here directly from the operator spectrum
rather than from a numerical dispersion scan, and confirming R11.6 is not an artefact of F27's
particular test grid.

**Step 4 — $c_\text{lat}$ and rest mass are two readouts of one generator.** The full dispersion is
$\Omega_\text{Dirac}(\mathbf k,m)=\arccos\bigl(\sqrt{1-m^2}\,u(\mathbf k)\bigr)$, and
$$\Omega_\text{Dirac}(0,m)=\arcsin m\quad\text{(intercept = rest mass)},\qquad
\frac{d\Omega_\text{Dirac}}{d\lvert\mathbf k\rvert}\bigg\vert_{\mathbf k\to0,\,m=0}=\frac1{\sqrt3}=c_\text{lat}\quad\text{(slope)}\tag{11.6}$$
verified to $<10^{-12}$ (T5). "$c_\text{lat}$ is a rotation rate" (Chapter 6's opening claim,
CLAUDE.md Core Design Decisions 1–2) and "rest mass is the zero-$\mathbf k$ rotation rate" are the
same statement about the same generator — its slope and its intercept — closing algebraically the
"conceptual, not algebraic" gap the source audit that motivated F167 (audit G1) had named.

$$\boxed{\;\Omega_\text{Dirac}(0,m)=\arcsin m\text{ (rest-mass intercept)},\quad \tfrac{d\Omega_\text{Dirac}}{d\lvert\mathbf k\rvert}\big\vert_{\mathbf k\to0,m=0}=1/\sqrt3=c_\text{lat}\text{ (slope)} - \text{one generator, verified to}<10^{-12}\;}\tag{R11.13}$$

**Step 5 — dimensional rest energy, and the link to R6.11.** Restoring $\hbar$ and the lattice clock
$dt$: $E_0=(\hbar/dt)\arcsin m\to(\hbar/dt)\,m$ for $m\ll1$, with $m_\text{phys}=E_0/c^2$ — the
dimensionless rule parameter maps to physical mass through the lattice clock and $c$, and R6.11's
continuum $E^2=m^2c^4+p^2c^2+O(\text{lattice}^4)$ is the small-leg limit of the same spherical
identity (11.5)–(11.6) generalized to $\mathbf k\ne0$.

**The magnitude, explicitly not closed here.** T6 checks unitarity across $m\in\{0.05,\ldots,0.999\}$
and finds every value equally admissible (residual $2\times10^{-16}$ at each) — the bare rule genuinely
leaves $m$ free, matching §11.1's free-input accounting exactly. F167's own closing note (2026-06-29
update) records that this is not a permanently open magnitude problem: F144's dimensional
transmutation of the rule's derived strong coupling is reported to land the overall scale $N$ to a
factor $\sim1.9$ with no tuning, superseding F119's "no marginal channel" no-go via F233 — both
belong to Chapters 13 and 17 respectively and are forward-cited, not claimed, here.

$$\boxed{\;\text{every }m\in(0,1)\text{ is equally unitary/admissible in the bare rule (T6) - the magnitude of each flavor mass is not fixed by this chapter's mechanism, and is forward-cited to Ch.13/17}\;}\tag{R11.14}$$

## 11.3 Results table

| # | Statement | Status | Exactness | Test record |
|---|---|---|---|---|
| R11.1 | Ludwig's ambiguity: $\beta(\theta)=(\cos\theta\,\sigma_1+\sin\theta\,\sigma_2)\otimes\sigma_0$ solves (11.1) for any $\theta$ | constructive observation (primary source) | algebraic (trivial substitution) | `physics-notes-complete.md` p. 59; re-derived independently by F167 T2 |
| R11.2 | Gauging $\theta\to\theta(x)$ produces a local field acting chirally | constructive observation (primary source) | n/a — construction | `physics-notes-complete.md` p. 60 |
| R11.3 | The complex-mass step (11.2) and its $SU(2)$ doublet extension (11.3) are exactly unitary for any $\theta(x)$/$U(x)$ | **exact identity, verified** | machine | `complex-mass-chiral` (battery), T1/T2, $1.3\times10^{-15}$/$2.5\times10^{-14}$ |
| R11.4 (=R11.5 text) | $SU(2)_L$ Ward identity $V\cdot\text{mass}(\psi;U)=\text{mass}(V\psi;VU)$ holds exactly, $\eta$-only | **exact gauge symmetry, proved+verified** | exact | same record, T5, $1.055\times10^{-17}$ |
| R11.5 (chirality) | $\chi$ identically unchanged under $V(x)$; $\eta$ non-trivially transformed | **exact** | exact | same record, T6, literal $0$ |
| R11.6 | $U(x)$ steers coupling direction (T9, $0.564$) yet dispersion is $\theta$-independent (T3, $3.3\times10^{-16}$) — pure gauge, not a Higgs boson | derived + verified | exact / machine | same record, T3/T9 |
| R11.7 | Mass gap forms at $U=\mathbb I$, $m\ne0$ with zero scalar condensate; $\nu_L$ carries $T_3=+\tfrac12$ exactly | **exact** | exact / machine | same record, T7/T8 |
| R11.8 | Quark sector: mechanism ports exactly (Q1–Q9); split mass / unwired $V(x)$ breaks Ward invariance at $O(1)$, exactly as F27's own Known Limitation predicted | ported + diagnosed | machine (Q1–Q9) / diagnostic (Q10–Q11) | `FG2-quark-complex-mass` (battery), 11/11 |
| R11.9 | Coupling to dynamical $W_\mu$ restores $SU(2)_L$ Ward invariance to $2.8\times10^{-16}$ for uniform $V(x)$; $\chi$ stays exactly decoupled at $m=0$ | **exact, verified** | machine / exact | `FG3-quark-electroweak` (battery), QE2/QE3, 6/6 |
| R11.10 | $e,u,d$ propagate as genuine real-time wavepackets: correct group velocity, norm conservation ($10^3$ ticks), zitterbewegung $2\arcsin m$, exact charge, conserved colour | **certified** | machine ($10^{-13}$–$10^{-16}$) / quantitative ($10^{-3}$–$10^{-4}$) | `P0-dynamical-fermions` (battery), 16/16 |
| R11.11 | Unitarity forces $n=\sqrt{1-m^2}$; exactly 2 of 16 Dirac covariants qualify as rest mass terms — mass is unique, not arbitrary | **full theorem** | exact | `F167-restmass-from-rule` (battery, result_dump), T1/T2 |
| R11.12 | $\Omega_\text{rest}(m)=\arcsin m$, $\cos\Omega_\text{rest}=\sqrt{1-m^2}$ | **exact identity** | exact | same record, T3 |
| R11.13 | $c_\text{lat}$ (slope) and rest mass (intercept) are two readouts of one generator $\Omega_\text{Dirac}(\mathbf k,m)$ | **exact identity, the R6.10 bridge** | exact ($<10^{-12}$) | same record, T5 |
| R11.14 | Magnitude of $m$ not fixed by the bare mechanism — every $m\in(0,1)$ admissible; forward-cited to F144/F233 (Ch.13/17) | **open, scoped precisely** | scope / no-go | same record, T6 |

## 11.4 Comparison with measurement

**No absolute numerical mass prediction is produced at this chapter's level, and this is stated
precisely rather than implied away.** Every check in §11.2.3–11.2.5 that uses a numerical value of
$m$ uses a **representative, dimensionless, hand-chosen test value** — F27's $m=0.3$, F40's
$m_u=0.10/m_d=0.40/m_s\approx1.6$ (chosen to exercise a $4$:$16$ ratio, not to reproduce one), F85's
$m_e=0.05/m_u=0.10/m_d=0.40$ — and every source that states this explicitly says so ("test values,
not physical," F85). F40's Q4 check ("up/down/strange splitting: $r_d/r_u=3.96$ vs. expected $4$,
$r_s/r_u=15.22$ vs. expected $16$") is a **self-consistency check of the mechanism's dynamics**
against its own chosen input parameters — confirming the resulting mass-squared splitting tracks
$(m_f/m_u)^2$ as the mechanism's own algebra predicts, to $\sim1\%$ (a truncation effect of the
$\sin^2\to(\cdot)^2$ linearization) — not an independently derived prediction of the $4$:$16$ ratio
itself, which was chosen as an input.

What **is** compared to something external, at this chapter's level: R11.13's structural identity
that rest mass and $c_\text{lat}$ share one generator is checked to $<10^{-12}$ against the model's
own algebra (an internal-consistency comparison, not an experimental one, exactly like most of
Chapter 4's results); R11.10's zitterbewegung frequency $2\arcsin(m)$ is checked against the model's
*own* real-time dynamics, not against a laboratory measurement (zitterbewegung has never been
observed directly for a free electron — the closest analogues are trapped-ion and Bose–Einstein-
condensate quantum simulations, outside this chapter's scope).

**Where the numbers come from.** Mass **ratios** within a generation (the crystal-field hierarchy,
the $2/9$ shape angle, Koide's relation) are Chapter 15's derivation, built on the structural
mechanism established here. The **overall scale** (turning a dimensionless $m$ into an electron rest
mass in MeV) is Chapter 17's SI-closure derivation, using the dimensional-transmutation route F167
itself forward-cites (F144/F233, Chapters 13/17). This chapter's own comparison-with-measurement
content is therefore genuinely null at the numerical level, by design: it establishes *that* mass
exists, is unique, is a rotation rate, and is gauge-symmetric without a Higgs — not *how much* any
particular fermion weighs.

## 11.5 What was excluded, and why

**A fundamental Higgs scalar for mass generation.** Chapter 1 already excluded this at the postulate
level (P6, on Ludwig's stated preference that Weinberg–Salam "without the Higgs since it isn't
physical," `physics-notes-complete.md` p. 62). At the mechanism level, this chapter shows precisely
*what job* a fundamental Higgs would have needed to do, and how the construction here does it
differently: a Higgs mechanism needs (i) a dynamical scalar field with (ii) a symmetry-breaking
potential that (iii) acquires a nonzero vacuum expectation value, whose *direction* in isospin space
then selects which right-handed singlet each left-handed doublet component couples to. This
chapter's construction gets item (iii)'s job — direction selection — from $U(x)$ (R11.6, T9), but
$U(x)$ is proved to carry **zero** physical information (R11.6, T3: dispersion independent of
$\theta$ to $3.3\times10^{-16}$) — it is not dynamical, has no potential, and never propagates as a
degree of freedom. Items (i) and (ii) are simply absent from the construction, not hidden or
integrated out; the mass gap forms directly from the off-diagonal structure of (11.2)–(11.3) at
$U=\mathbb I$ (R11.7). This is precisely the "unnecessary, not falsified" distinction Chapter 1
already flagged and preserves here rather than overstating.

**The discrete CPT no-go (R4.11) — engaged directly, not avoided.** This is the chapter's one place
where a prior result names a genuine obstruction touching the exact construction built here, and it
is addressed precisely rather than either ignored or conflated with a stronger claim than the source
supports.

*What R4.11 actually tested.* F378 built the model's actual gauge-coupled fermion step
(`covariant_dirac_doublet_step`) explicitly and confirmed its mass term is "the Stueckelberg-type
mass-generation mechanism" — the same construction §11.2.3 derives, with the doublet mixed through an
independent $SU(2)$ link $V$ (F378 §5) — embedded alongside a *separately* varying kinetic-sector
link $U$. It then asked whether a **fixed** antiunitary operator $\Theta'$ intertwines the one-tick
evolution at a fixed background $(U,V)$ with the inverse evolution at that **same** fixed $(U,V)$ —
the literal discrete lattice analogue of the free-sector CPT theorem (R4.7/F328), and of the kinetic-
sector extension the same finding proves positively (R4.10). The mass sector fails: the block algebra
requires a fixed operator $\Lambda$ satisfying $\Lambda V^T\Lambda^{-1}=V$ for *every* $V\in SU(2)$,
but $V\mapsto V^T$ is a group anti-automorphism while conjugation by any fixed $\Lambda$ is always an
automorphism, and the two can coincide only on an abelian group — $SU(2)$ is not, so **no fixed
$\Lambda$ can exist** (R4.11, a general algebraic proof, corroborated by a 500-sample search finding
none closer than residual $0.28$).

*What this does, and does not, say about §11.2.3's construction.* R11.5 ($SU(2)_L$ gauge covariance
of the mass step, T5) and R4.11 (the fixed-background CPT intertwiner obstruction) are **different
mathematical statements about the same object**, and the difference is what resolves the apparent
tension. R11.5 is a Ward identity: transform $\psi$ **and** $U(x)$ **together** under a single
$V(x)\in SU(2)_L$, and the mass step commutes with that combined transformation exactly — this is
ordinary local gauge covariance, and it is what physical consistency of the construction actually
requires, proved to $1.055\times10^{-17}$. R4.11 asks a structurally different question: hold the
gauge background **fixed** and ask whether a single, background-independent antiunitary $\Theta'$
maps the dynamics at that fixed background to its own inverse — the discrete-CPT question, not the
gauge-covariance question. F378's own scope statement is explicit and is reproduced here rather than
paraphrased away: **"this is not a claim that the model's $SU(2)_L$ gauge theory violates CPT as a
physical statement"** — every test holds the background fixed, mirroring exactly how the free-sector
theorem (R4.7) holds $m$ fixed; the continuum Lüders–Pauli argument instead lets $C,P,T$ **also**
transform the connection itself, and R4.10's own positive kinetic-sector result already needed
exactly this kind of structure (the pseudoreality relation $\tau_2U\tau_2^{-1}=U^*$ describes *how*
$U$ transforms, not $U$ held fixed).

$$\boxed{\;\text{this chapter's construction does not avoid what F378 forbids - it is the same construction F378 tested - but what F378 forbids is a narrower claim (a fixed-background discrete-CPT intertwiner) than what this chapter's own gauge-covariance result (R11.5) establishes and needs}\;}\tag{\text{honest disclosure, per R4.11/CL306}}$$

Whether a **background-transforming** $\Theta$ (one that also maps $V\to V'$, rather than requiring
the identity at the same $V$) restores a theorem for the mass sector is an open question F378 states
it does not attempt (ledger row A4r's new, narrower residual) — carried forward to §11.6 rather than
resolved here, since resolving it is outside this chapter's four assigned findings.

## 11.6 What is still open

- **The numerical magnitude of every fermion mass** (R11.14): the bare mechanism admits any
  $m\in(0,1)$; closing this is the joint work of Chapter 13 (F144's dimensional transmutation of the
  strong coupling) and Chapter 17 (F233's supersession of F119's "no running channel" no-go, and SI
  closure).
- **The background-transforming CPT question for the gauged mass sector** (§11.5): whether letting
  $\Theta$ also transform the classical gauge/mass background restores a discrete-CPT-type identity
  for the $SU(2)$-gauged mass mechanism is explicitly named by F378 §6 as unattempted, not merely
  unresolved by omission.
- **A cross-module architectural inconsistency, disclosed by F378 itself, directly touching this
  chapter's mechanism.** Two different discretizations of "the massive BCC Dirac fermion" coexist in
  the tree: `dirac_bcc.py` (F328's module, branch-$+$/dagger pairing, has the proven free-sector CPT
  theorem R4.7) and `covariant_dirac_doublet_step` (this chapter's gauge-coupled module, branch-$+/-$
  pairing) — F378 found the latter fails F328's identity already at **zero** gauge coupling, for a
  reason unrelated to gauging at all (§4.2.7 of Chapter 4; F378 §3). This is named, not resolved,
  by any source read for this chapter.
- **Quantization.** F27 states explicitly that its result is at the classical CA level; loop
  corrections and anomaly cancellation are not tested by any of this chapter's four findings.
- **Right-handed singlets as dynamical, hypercharge-coupled fields; a dynamical $Z$; gluons brought
  to the dynamical-field standard; antiparticle/charge-conjugation closure per species** — F40's own
  "what still remains for first-generation closure" list, items 3–6, all Chapter 12/13 territory.

## 11.7 Falsifiers

**None of the four claim cards this chapter rests on states a falsifier.** CL003 (`falsifier: unset`)
is explicit: "The claims summary gives no observational threshold for this claim, and this card does
not invent one... Recorded as `falsifier: unset` (debt) rather than `none`, because a structural
reason has **not** been argued." CL047, CL080 and CL147 — all seeded 2026-08-04 at
`review_state: unreviewed-seed` — likewise carry `falsifier: unset`. This is reported as-is: it is a
genuine, disclosed gap in the claims layer for this chapter's headline result, not a silent omission
this chapter is introducing.

What Chapter 1 already stated at the postulate level bears directly here: **P6 is falsified
observationally if a fundamental scalar with the specific quantum numbers and self-interaction
structure of the Standard Model Higgs boson is required by data in a way this project's chiral-$SU(2)$
mass mechanism cannot reproduce** — and this chapter is where that comparison would actually be
carried out, not merely asserted; no source read for this chapter attempts that comparison against
LHC Higgs-sector data. Two narrower, internal falsifiers follow directly from this chapter's own
algebra, though none is currently promoted to a claim card: (i) R11.3/R11.5's unitarity and
Ward-identity results are exact algebraic identities — a single counterexample $(\theta,U,\psi)$
breaking either would falsify the construction outright, not merely weaken it; (ii) R11.11's
"exactly two of sixteen Dirac covariants" classification is a closed group-theoretic count — a third
admissible rest covariant, if found, would falsify the uniqueness claim that grounds R11.14's
"mass is forced, only its magnitude is free" framing.

## Notation established or extended in this chapter

| Symbol | Meaning | First used |
|---|---|---|
| $\alpha_i,\beta$ | The Dirac matrices in a Weyl-basis representation; $\beta_g=(U\sigma_1U^\dagger)\otimes\sigma_0$ is the gauged form | §11.2.1–11.2.2 (P5, forward-reserved in Ch.1) |
| $U(x)\in SU(2)$ | The chiral $SU(2)$ connection carrying complex mass (P6); here shown to be pure gauge in the mass step alone, with no propagating degree of freedom | §11.2.2–11.2.3 (P6, defined at last in Ch.1's forward reservation) |
| $M(\theta)$, $M_\text{SU2}$ | The per-cell mass-step unitary (11.2)–(11.3) | §11.2.3 |
| $\theta(x)$ | The pure-gauge chiral phase; the $\gamma^0\gamma^5$ covariant of R11.11 | §11.2.1, §11.2.6 |
| $V(x)$ | The gauge-coupled construction's independent mass-sector $SU(2)$ link (distinct from the kinetic-sector link $U$); the object R4.11's no-go concerns | §11.5 (reused from Ch.4) |
| $m_f$ | The dimensionless lattice mass parameter, one per fermion flavor; magnitude free at this chapter's level (R11.14) | §11.1, throughout |
| $\Omega_\text{rest}(m)=\arcsin m$ | The zero-$\mathbf k$ rest rotation angle; $\cos\Omega_\text{rest}=\sqrt{1-m^2}=n$ | §11.2.6 (R6.10 borrowed this in advance) |
| $\Omega_\text{Dirac}(\mathbf k,m)$ | The full one-generator Dirac dispersion; $c_\text{lat}$ (slope) and rest mass (intercept) are its two readouts | §11.2.6 |
| $\omega_Z=2\arcsin(m)$ | The zitterbewegung frequency, dynamically measured in F85 | §11.2.5 |
