# Chapter 8 — The Photon

*Chapter 8 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F37-rs-bcc-chirality-helicity.md`, `findings/F39-two-helicity-photon-bilinear.md`,
`findings/F69-paired-spinor-photon.md`, `findings/F89-singlet-bilinear-is-paired-photon.md`,
`findings/F91-pairing-classification-theorem.md`, `findings/F105-axial-photon-exactly-dispersionless.md`,
`findings/F129-blockspin-free-photon.md`, `findings/F168-paired-photon-binding-gauge-protected.md`,
`findings/F169-photon-interacting-two-body-wavefunction.md`,
`findings/F207-casimir-effect-source-channel-and-gravitation.md`,
`findings/F209-modulated-casimir-beable-template-degeneracy.md`,
`findings/F250-allk-gauge-pole-paired-photon.md`,
`findings/F271-k-resolved-dielectric-photon-propagator.md`,
`findings/F306-curl-closes-at-k3-representation-artifact.md`,
`findings/F314-paired-photon-real-space-propagation.md` (the fifteen findings `00-plan.md` §2
assigns to this chapter, all read in full), checked directly against `docs/theory/supersessions.yaml`
records **S1** (read in full — the central supersession this chapter turns on),
**S18** (read in full — F306's resolution of the old curl-residual episode), and **S2**
(F91's own record, `superseded: []`, the gluon chiral→even migration), and against `claims-index.md`:
**CL002** (F69, `live`, `exact`, headline), **CL012** (F30/F66/F67/F105, `live`, `exact`,
non-birefringence), **CL084** (F89, `withdrawn` — investigated in full in §3.7/§6 below),
**CL148**/**CL149** (F168/F169, both `live`), **CL181**/**CL183** (F207/F209, both `live`),
**CL220** (F250, `live`), **CL235** (F271, `live`, exactness `unset`), **CL251** (F306,
`withdrawn` — investigated in §6.3), **CL283** (F314, `live`), **CL115** (F129, `live`).
Notation, postulates and results are those of Chapters 1, 6 and 7
(`01-postulates-and-ontology.md`, `06-free-propagation-light-cone.md`,
`07-relativity-on-a-lattice.md`) — $\mathbf k$, $\omega^\pm(\mathbf k)$, $\Omega(\mathbf k)$,
$\Omega_\text{even}$, $c_\text{lat}$, $\hat{\mathbf n}(\mathbf k)$ — extended, never redefined.
`references/mohr-2010-maxwell-photon-wf-summary.md` (the six-component photon-wavefunction
literature) is cited in §3 as external corroboration of the $(\mathbf E,i c\mathbf B)$
six-component object this chapter's pair bilinear reproduces, and in §7 for the gaps that
literature identifies against the model's own construction. `references/casimir-force-literature-and-model-integration.md`
is cited in §3.6 for F207/F209's external grounding (Jaffe 2005, Nikolić 2016, Calloni/Avino,
Wilson et al. 2011).

## 8.0 What this chapter establishes

The electromagnetic photon of this model is **not** a fundamental spin-1 field. It is a bound
pair of two spin-½ Weyl quanta — one on each of the lattice's two chiral branches, each carrying
half the total momentum — whose phase advances at the sum of the two constituent rates,
$\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$. This chapter derives
that construction from the ground up rather than citing it: it shows (i) why the two physical
circular polarisations are forced into a one-to-one correspondence with the lattice's two
chirality branches (F37); (ii) why the *identity/vector* channel specifically — not a free choice
among several equally consistent constructions — is the one the photon's coupling forces, while
the same argument forces the $W^\pm$ onto the opposite, purely chiral channel (F91); (iii) how the
paired construction realises that forced channel, and why "the pair only occurs as a pair" removes
the birefringence a single-branch photon would carry (F69); (iv) a chain of exactness results
confirming the construction's masslessness, gauge structure, and real-space propagation hold not
only at leading order but across the whole Brillouin zone and under coarse-graining (F105, F129,
F168, F169, F250, F314); (v) that the same construction reproduces the one measured room-
temperature observable usually attributed to "zero-point energy," the Casimir force, without
requiring the non-gravitating homogeneous zero-point sum to be physical (F207, F209); and (vi)
its generalisation to a position-dependent dielectric background, the beginning of the gravity
sector's photon sector (F271, scoped and forward-cited to Chapter 18). It then states, with equal
care, what construction this supersedes as *the photon* — the composite $\sigma$-bilinear that
assigns each helicity to its own branch and is therefore genuinely, linearly birefringent (F39) —
and what survives of that construction for later chapters (the massive and non-Abelian sectors,
Chapters 12–13).

## 8.1 Inputs

**Postulates used.** **P5** is the central postulate of this chapter: the primitive field is the
two-component complex Weyl spinor $\psi\in\mathbb C^2$, and the photon of this chapter is built as
a *bound pair of two such primitives* — nothing more fundamental is available to build it from,
and nothing less would do (a single Weyl quantum cannot be a spin-1, two-polarisation object; F250
§"Scope"). **P4** (exact unitarity, $\mathcal U=e^{-iH}$) underwrites every exactness claim below:
the pairing's masslessness (F168), its all-$k$ gauge pole (F250), and its real-space propagation
(F314) are all statements about the spectral and unitary structure of the same one-tick walk
Chapters 2–3 built, not about an approximation to it. **P1–P3** (discreteness, locality,
homogeneity/isotropy) enter only through the BCC dispersion $\omega^\pm(\mathbf k)$ this chapter
inherits from Chapter 6 (R6.1–R6.5) and does not re-derive. **P6** is not invoked directly, but is
the load-bearing contrast in F168's gauge-protection argument (§3.5 below): the same chiral-$SU(2)$
mass step that P6 introduces for matter is precisely the branch-*coupling* vertex the photon's
identity-channel coupling structurally lacks. **P7** (the elegant-design heuristic, Ch.1's Gap
[G-1]) is invoked once, explicitly, at a specific point where the forcing argument runs out — the
gluon sector's even-law assignment (§3.2 below) — and is flagged there rather than silently folded
into "forced."

**Prior results used, precisely.** **R6.3** (Ch.6) is the object this chapter's photon *is*: the
exact discrete rotation law $\mathbf E(t{+}1)=\cos\Omega\,\mathbf E(t)+\sin\Omega\,\mathbf B(t)$,
etc., with $\Omega(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ — Chapter 6 derived this
rotation law and its rate but explicitly deferred "why two Weyl quanta specifically pair, at
$\mathbf k/2$ each, to form this object" to this chapter (Ch.6 §6.2.3: "the pairing itself is that
chapter's content, not re-derived here"). **R6.4/R6.5** ($c_\text{lat}=1/\sqrt3$) fixes the
propagation speed inherited unchanged. **R6.8** (the BCC spin axis $\hat{\mathbf n}(\mathbf k)$,
closed form) is the object every helicity/chirality identification below is built from. **R6.12/
R6.13** (Ch.6, F246) — the even-law dispersion's exact evenness in $\mathbf k$ and its closed-form
cubic LIV coefficient — is cited in §3.4/§5 as the already-derived exactness structure this
chapter's photon inherits, not re-derived. **R7.5** (Ch.7, F301 §3.5) is used directly rather than
re-derived: "the photon's extra covariance order and its non-birefringence share one mechanism:
the paired channel's even chirality symmetrisation" — Chapter 7 showed the *same* helicity
symmetrisation that cancels the finite-$a$ boost defect at $O(\mathbf k^3)$ (rather than $O(\mathbf
k^2)$, as on a bare chiral branch) is the mechanism that removes the birefringence this chapter's
§6 discusses; this chapter cites that result rather than re-deriving the boost-covariance side of
it.

**Free inputs consumed, stated precisely.**

1. **The identification of the Riemann–Silberstein pair with the physical $(\mathbf E,\mathbf B)$
   field is a representation choice, not a derivation** — inherited unchanged from Ch.6's own
   citation of Mohr's six-component reformulation as external corroboration that packaging
   $(\mathbf E,\mathbf B)$ into one rotating/first-order object is legitimate. Nothing in this
   chapter's own findings supplies an independent argument that this reading, rather than some
   other six-component packaging, is *the* one nature uses; it is adopted because it is the
   reading under which the dispersion and pairing algebra below close exactly.
2. **The gluon sector's even-law assignment consumes P7 explicitly, not merely as narrative
   colour.** F91's own text states the point plainly: the BCC gluon's colour coupling is
   branch-blind (a scalar $\propto\mathbb I$ in branch space, exactly as F68's photon argument
   requires), so the *forcing* argument for even-vs-chiral applies to the gluon with the same
   strength as to the photon — but the code that actually ran at the time used the chiral W step
   instead, "unforced," and F91 §"G3" states the resolution explicitly: "confinement makes this
   unobservable, so nothing is falsified — but the assignment is unforced, and the F68-mirror
   argument + **the elegant-design philosophy** select the even law." The migration was then
   executed (F91 §"Migration executed", 2026-06-04; `docs/theory/supersessions.yaml` **S2**). This
   chapter records that the even-law choice for the gluon is *forced by the same argument as the
   photon's*, once the coupling's branch-blindness is granted, but that the actual code migration
   away from an equally-unfalsified alternative leaned on P7 for its timing/motivation, exactly the
   pattern Ch.1's Gap [G-1] already flagged as carrying no independent justification of its own.
3. **The binding coupling value that puts the photon exactly at the two-body threshold is external,
   not derived from first principles.** F169 is explicit: "the binding **coupling value** — why the
   EM channel sits exactly at criticality $g_c$ — is not derived from first principles here." What
   *is* derived (F168) is that the threshold value is the *gauge-protected, structurally forced*
   one, i.e. that *if* a bound state exists at all in this channel, it must sit at $E_b=0$; the
   existence of binding at that criticality is consumed as an input plausibility (the identity-
   channel coupling's actual strength is not independently fit here) rather than derived from the
   U(1) minimal-coupling Lagrangian.
4. **Nothing else is free.** Every dispersion, projector-rank, and RG eigenvalue in this chapter is
   a closed-form consequence of R6.1's $A(\mathbf k)=u(\mathbf k)\mathbb I-i\boldsymbol\sigma\cdot
   \tilde{\mathbf n}(\mathbf k)$ and the pairing $\mathbf k\to\mathbf k/2$, introducing no additional
   fitted constant.

## 8.2 The derivation

### 8.2.1 The two circular polarisations are forced onto the two chirality branches (F37)

Before any pairing construction is built, one algebraic fact fixes what object the pairing has to
be built from. The real $(\mathbf E,\mathbf B)$ rotation of R6.3, $R(\Omega)=\begin{psmallmatrix}
\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{psmallmatrix}$, has eigenvalues $e^{\mp i\Omega}$
with eigenvectors $(1,\mp i)^{\!\top}$ — an algebraic identity independent of what $\Omega(\mathbf
k)$ actually is. In field language these eigenvectors *are* the Riemann–Silberstein combinations
$\mathbf F_\pm(\mathbf k)\equiv\mathbf E(\mathbf k)\pm i\mathbf B(\mathbf k)$, with $R(\Omega)$
acting on $\mathbf F_+$ as $e^{-i\Omega}$ and on $\mathbf F_-$ as $e^{+i\Omega}$:

$$\boxed{\;R(\Omega)(1,\mp i)^{\!\top}=e^{\mp i\Omega}(1,\mp i)^{\!\top}\;\Longleftrightarrow\;\mathbf F_+(\mathbf k)\to e^{-i\Omega}\mathbf F_+(\mathbf k),\ \ \mathbf F_-(\mathbf k)\to e^{+i\Omega}\mathbf F_-(\mathbf k)\;}\tag{R8.1}$$

(F37, exact algebraic identity.) Reality of $(\mathbf E,\mathbf B)$ forces $\mathbf F_+(-\mathbf
k)=\mathbf F_-^*(\mathbf k)$ (Hermitian symmetry, "HS"); allowing each RS eigenstate to propagate at
its own rate $\phi^\pm(\mathbf k)$ and imposing HS at all times forces
$\phi^+(-\mathbf k)=\phi^-(\mathbf k)$ — the **chirality constraint** — which the BCC dispersion
satisfies exactly, $\omega^+(-\mathbf k)=\omega^-(\mathbf k)$ (the same cosine-even/sine-odd
structure R6.8's $\hat{\mathbf n}(\mathbf k)$ is built from). The *unique* Hermitian-symmetry-
preserving assignment is therefore $\mathbf F_+(\mathbf k)$ on the $+$ chirality branch and
$\mathbf F_-(\mathbf k)$ on the $-$ branch, with a plane wave along $\hat{\mathbf k}$ of positive
helicity (RCP, $\mathbf B=-i\mathbf E$) satisfying $\mathbf F_-=0$ identically and a negative-
helicity (LCP) wave satisfying $\mathbf F_+=0$:

$$\boxed{\;h=+1\ (\mathbf F_+\text{ only})\leftrightarrow\Omega^+(\mathbf k)=2\omega^+(\mathbf k/2);\qquad h=-1\ (\mathbf F_-\text{ only})\leftrightarrow\Omega^-(\mathbf k)=2\omega^-(\mathbf k/2)\;}\tag{R8.2}$$

(F37, exact algebraic identity, both legs.) **This correspondence is a fact about the lattice's
kinematics, not yet a choice of photon.** It fixes, exactly, what a *chirally-faithful* propagation
law would have to be — split, one helicity per branch — and hence what such a law would predict:
a birefringence $\Delta\Omega(\mathbf k)=\Omega^+(\mathbf k)-\Omega^-(\mathbf k)$, zero on the cube
axes (where $\omega^+=\omega^-$ by symmetry) and, along the body diagonal, linear in $k$ to leading
order, $\Delta v_\phi/c_\text{lat}\approx-k/18$ (F37, citing the F30 sympy expansion Chapter 7
already used at R7.9/R7.10). What R8.1/R8.2 do **not** yet fix is whether the photon *is* this
chirally-faithful, birefringent object. §8.2.2 supplies the argument that it is not, and §6 states
in full why not.

### 8.2.2 The pairing classification theorem: which channel is forced, per sector (F91)

The question R8.1/R8.2 leaves open — is the branch-split (chiral) propagation law, or some other
combination of the two branches, the one a given gauge boson's coupling actually realises? — is
answered by a single forcing principle, stated and verified across all four of the model's gauge
sectors at once. Let $(g_L,g_R)$ be a sector's coupling weights on the two BCC chiral branches (the
model's realisation of $\gamma^5$-projection). **The branch structure of the coupling operator
forces the propagation channel**:

| sector | $(g_L,g_R)$ | branch operator | forced channel |
|---|---|---|---|
| $\gamma$ | $(Q,Q)$ | scalar $\propto\mathbb I$ | **even** (identity) |
| $W^\pm$ | $(g,0)$ | projector $P_L$ | **chiral** (single-branch) |
| $Z$ | $(T_3{-}Qs^2,\,{-}Qs^2)$ | neither | neither pure channel — even exact for the vector part, axial part mass-suppressed |
| gluon | $(g_s,g_s)$ | scalar $\propto\mathbb I$ | **even** (identity, colour-blind) |

$$\boxed{\;\text{a scalar}\propto\mathbb I\text{ branch operator forces the even (paired) channel; a projector }P_L\text{ forces the chiral (single-branch) channel}\;}\tag{R8.3}$$

(F91, 13/13 checks, exact-ℚ/structural-zero for 5, machine $\le2\times10^{-13}$ for 6, quantitative/
contrast for 2.) The photon's row is the one this chapter needs: the electromagnetic charge $Q$ is
identical on both chiral branches ($Q_L-Q_R=0$ for every charged species, exact over $\mathbb Q$
from $Q=T_3+Y/2$), so the coupling operator is a scalar in branch space and commutes with *any*
branch-mixing unitary — exactly the F68 minimal-coupling argument Chapters 6/9 already lean on,
here promoted from a single-sector observation to one leg of a four-sector theorem. The $W^\pm$'s
row is the sharp contrast: $T_3=0$ over $\mathbb Q$ for every right-handed species, so the $SU(2)_L$
coupling in branch space is exactly the left-projector $P_L=\mathrm{diag}(1,0)$, which annihilates
the right branch identically ($\|P_L\psi_R\|=0.0$) — a single-branch source can never populate the
cross-branch pair the even law would require, so the even law is *excluded* for the $W$, not merely
unchosen. **The photon and the $W^\pm$ sit at the two ends of one and the same classification, by
the branch structure of their couplings alone** — this is the theorem this chapter's photon rests
on, and it is also the reason Chapters 12–13's $W$/$Z$/gluon sector can keep the chirally-faithful
propagation law without contradicting anything derived here (§6 states this explicitly). The
gluon's row is forced by the identical argument (colour acts on colour only, is branch-blind), with
the caveat recorded in §8.1 item 2 that the code migration realising the forced choice leaned on P7
for its timing.

### 8.2.3 The paired photon itself, and why it is non-birefringent by construction (F69)

R8.2 established what a *single-branch* photon's dispersion would be; R8.3 established that the
photon's coupling is not single-branch — it is the identity-channel scalar. The paired-spinor
construction realises that forced channel directly: the photon is a **bound $(+,-)$ pair**, total
momentum $\mathbf k$ shared equally between two Weyl constituents at $\mathbf k/2$ each, one on
each chirality branch. Because the pair is bound and symmetric, its phase per tick is the **sum**
of the constituent phases — not a choice of which branch to follow, but the only object a
bound, symmetric two-quantum state of this kind can carry:

$$\boxed{\;\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)\equiv\Omega_\text{even}(\mathbf k)\;}\tag{R8.4}$$

(F69, residual $0$ against R6.3's already-derived even-law rate, PP1; the construction adds no new
propagator, it identifies the existing even-law rotation as the rate *this specific two-quantum
pairing* produces.) **The non-birefringence mechanism, stated precisely.** In the excluded
chirally-faithful construction of §8.2.1, the two photon helicities $\mathbf F^\pm$ are assigned to
the two branches *independently*, so a generic linear polarisation — a superposition of both
helicities — splits by $\Delta\Omega$ as it propagates. In the paired photon there is **no
single-branch photon to split against**: "the pair only occurs as a pair" (Ludwig's own phrase,
`references/physics-notes-complete.md` pp.5–6, cited directly in F69), so both helicities of the
resulting field always ride the one rate $\Omega_\text{pair}$. Verified directly: a linearly
polarised body-diagonal mode run for 6 ticks accumulates splitting $S=-1.8\times10^{-15}$ under the
paired law versus $S=+0.07924=-\Delta\Omega\,N$ under the retired chiral law (F69, PP2). The pairing
is **massless and luminal** ($\Omega_\text{pair}(0)=0$ exactly, $\Omega_\text{pair}/k\to1/\sqrt3$ to
$7.7\times10^{-6}$, PP3) and **spin-1** in the operational sense that matters for a gauge boson: two
transverse polarisations, real, norm-conserving (PP5, residuals $\le1.8\times10^{-17}$).

$$\boxed{\;\text{no single-branch photon exists in the paired construction}\;\Longrightarrow\;\text{no birefringence to split against}\;}\tag{R8.5}$$

This is not a numerical coincidence among three independent arguments — F69's own text records that
observation (non-birefringence required by GRB/AGN polarimetry, F65/F66 as summarised at S1),
minimal coupling (the identity-channel forcing of R8.3), and Ludwig's own two-Weyl-quanta
construction all land on the identical dispersion $\Omega_\text{even}$.

### 8.2.4 Why the binding sits exactly at threshold, not merely kinematically (F168)

A pairing "constructed" from two constituent rates by fiat would leave open the question the
2026-06-29 audit raised against F69: is $E_b=0$ a *modelling choice*, or does the walk force it?
Two structural facts answer this. **First, the constituents are massless because the walk is a pure
hop.** The BCC one-tick unitary has no on-site term ($A_0=0$; F51 §2), so $u^\pm(0)=1$ exactly and
$\omega^\pm(0)=\arccos1=0$ — a massless constituent is the *absence* of a self-loop, not a tuned
limit; an on-site deficit $\varepsilon$ would open a gap $\omega(0)\approx\sqrt{2\varepsilon}$
(F168, B1, exact). **Second, the mass mechanism (P6's chiral-$SU(2)$ step) lives entirely in the
branch-*coupling* component of the vertex, and the photon's identity-channel coupling has none.**
The P6 mass step is $V(m)=\cos m\,\mathbb I+\sin m\,X$ with $X=\begin{psmallmatrix}0&i\\i&0
\end{psmallmatrix}$ coupling the two chiral branches ($\eta\leftrightarrow\chi$); its gap is
$\Omega(0)=m$ (F168, B4, to $4\times10^{-17}$). The photon's vertex, by R8.3, is the branch-diagonal
identity $e^{i\theta}\mathbb I$ — its $X$-component is identically zero — so it **cannot** generate
the mass step:

$$\boxed{\;E_b=0\text{ is gauge-protected: the mass term lives only in the branch-coupling vertex }X\text{, which the identity-channel photon coupling structurally lacks}\;}\tag{R8.6}$$

(F168, 4/4 checks, exact/machine $4\times10^{-17}$.) This is the lattice realisation of Weinberg's
massless-spin-1 theorem: the vector-current quantum stays massless because nothing in its coupling
can open a gap, not because a gap has been tuned to zero. It sharply distinguishes the photon from
its "spin-0 sibling" (F73/F74), whose binding gap is *not* protected and requires a fine-tuned,
super-critical contact coupling to bind at all — the photon needs no such tuning for its
masslessness, only (§8.1 item 3) an unexplained coupling strength for binding to occur in the first
place.

### 8.2.5 The interacting two-body wavefunction (F169)

F168 explains *why* the bound-state pole must sit at threshold; it leaves the actual two-body
dynamics unbuilt. In the relative-momentum coordinate $p$ of the two constituents (one at
$\mathbf k/2+p$ on the $+$ branch, one at $\mathbf k/2-p$ on the $-$ branch), the free two-body
continuum floor is $T(\mathbf k)=\min_p E_0(p;\mathbf k)$, $E_0(p;\mathbf k)=\omega^+(\mathbf
k/2+p)+\omega^-(\mathbf k/2-p)$, and R8.4's symmetric pairing is the $p=0$ member. A single
attractive contact in the relative coordinate makes the bound state the exact root of a rank-1
(Koster–Slater) secular equation, $1=g\langle1/(E_0(p;\mathbf k)-E_b)\rangle_\text{BZ}$; the photon
is the **marginally-bound threshold state**, $E_b\to T(\mathbf k)$ at the critical coupling
$g_c(\mathbf k)$. At $\mathbf k=0$ this threshold wavefunction is exact and normalizable
(residual $0$; finite 3-D Watson-type integral, $g_c=2.2596$ at the tested resolution), agrees with
an independent dense-Hermitian diagonalisation to $5.6\times10^{-14}$, and has a finite real-space
RMS relative radius $\approx1.91$ lattice units — an explicit, localised, finite-size bound pair,
not a point object:

$$\boxed{\;T(0)=\omega^+(0)+\omega^-(0)=0\ \text{exactly}\;\Longrightarrow\;\text{masslessness is inherited from the gapless constituents, independent of the coupling value}\;}\tag{R8.7}$$

(F169, 6/6 checks, exact residual $0$ for the secular identity, machine $5.6\times10^{-14}$ for the
two-method cross-check.) One refinement of R8.4 falls out: the symmetric $p=0$ split is not the
exact two-body floor at finite $\mathbf k$, $\Omega_\text{pair}(\mathbf k)-T(\mathbf k)=O(k^2)\ge0$
(fit exponent $2.10$) — F69's even law is the photon's *leading* small-$\mathbf k$ dispersion, exact
only as $\mathbf k\to0$; §8.2.7 (F250) clarifies this does not move the gauge propagator's actual
pole, which rides $\Omega_\text{pair}$ by the gauge/identity structure of R8.6, not by sitting at
$T(\mathbf k)$.

### 8.2.6 Exact dispersionlessness on-axis, at every $k$ (F105)

One closed-form corollary of R8.4 sharpens Chapter 6's R6.1 (the on-axis exact linearity of the
single-particle dispersion) into a statement about the *paired* rate. Along a lattice axis,
$k_y=k_z=0$, both branches of the BCC dispersion collapse identically —
$\omega^\pm(k\hat x/2)=\arccos\cos(k/2\sqrt3)=k/(2\sqrt3)$ exactly, the $\pm$ branch term vanishing
identically — so

$$\boxed{\;\Omega_\text{pair}(k\hat x)=\frac{\lvert k\rvert}{\sqrt3},\qquad0\le\frac{\lvert k\rvert}{\sqrt3}\le\pi,\ \text{exactly, at every }k,\text{ not only as }k\to0\;}\tag{R8.8}$$

(F105, algebraic identity, numerically confirmed to $3\times10^{-15}$ over $k\in[0.1,1.2]$.) A
photon travelling along a lattice axis therefore carries **zero vacuum dispersion at any energy up
to the zone edge** — the GRB time-of-flight signature of R7.13/R7.14 (Ch.7) is identically zero
on-axis; all of this chapter's model-specific vacuum-dispersion content (R6.13's cubic coefficient,
carried through Ch.7's R7.11/R7.12) lives entirely off-axis. Beam optics on-axis are correspondingly
purely diffractive: a collimated packet's speed deficit is set only by its transverse angular
spectrum, not by any on-axis energy dependence (F105, confirmed in `photon_beam_all_fields`, later
superseded in numerical precision — not in conclusion — by F314's exact closed form, §8.2.9).

### 8.2.7 The all-$k$ gauge pole: a single massless transverse pole across the whole Brillouin zone (F250)

R8.4's dispersion is the *rate*; F250 analyses the *propagator* it defines and proves the pole
structure is exactly the one a massless spin-1 gauge boson should have, at every $\mathbf k$ in the
zone, not merely in the $k\to0$ continuum limit. Writing the one-tick evolution of the 6-vector
$(\mathbf E,\mathbf B)$ as the block operator $M_6(\mathbf k)=M_2(\Omega_\text{pair})\otimes\mathbb
I_3$ with $M_2(\Omega)=e^{\Omega J}$, $J^2=-\mathbb I$, four facts hold as algebraic or
machine-precision identities:

- **Pole location, all $\mathbf k$ (exact).** $\det(e^{\pm i\Omega_\text{pair}(\mathbf k)}\mathbb
  I_2-M_2)=0$ for every $\mathbf k$ — not a small-$k$ expansion (residual $1.1\times10^{-16}$, 4000
  BZ points).
- **Massless anchor (exact).** $\Omega_\text{pair}(0)=0$ literally, the same pure-hop gaplessness
  R8.6 already established, inherited by the pair.
- **Ward identity / transverse invariance (exact).** $M_6$ acts as a scalar in Cartesian
  polarisation space, so $[M_6(\mathbf k),P_T(\mathbf k)\otimes\mathbb I_2]=0$ for every $\mathbf k$
  (residual literally $0$): a transverse field stays transverse under the exact discrete evolution,
  at every $\mathbf k$, the lattice statement of gauge invariance for this channel.
- **Transverse residue rank exactly 2 (machine).** The pole's residue, restricted to the transverse
  subspace, has rank exactly 2 — the two physical photon polarisations, not three — with
  $\hat{\mathbf k}\cdot R_T=0$ to $9.3\times10^{-17}$.

$$\boxed{\;\text{for every }\mathbf k\in\text{BZ, the resolvent }G(z,\mathbf k)=(z\mathbb I-M_6)^{-1}\text{ has a single simple massless pole at }\omega_\text{freq}=\pm\Omega_\text{pair}(\mathbf k)\text{, residue = the rank-2 transverse gauge projector}\;}\tag{R8.9}$$

(F250, 8/8 checks, exact/machine $\le7\times10^{-16}$.) A doubler scan on a $61^3$ grid over the
photon BZ finds the pole's zero attained at **exactly one** point, $\mathbf k=0$: the $\mathbf
k\to\mathbf k/2$ momentum-sharing of the pairing pushes the constituent walk's doubler copies (at
the *constituent* BZ boundary $|q_i|=\pi$) out to photon momentum $|k_i|=2\pi$, outside the photon
BZ — **the same pairing that removes birefringence also removes fermion doubling from the gauge
sector.** This is a statement about the tree-level propagator; F250 records explicitly that the
loop-corrected self-energy and any radiative shift of the residue are out of its scope.

### 8.2.8 Block-spin RG: $c_\text{lat}$ is an exact fixed point, LIV operators are irrelevant (F129)

The Kadanoff block-average map $\mathcal R_b$ on a periodic field, $(\mathcal R_bf)(X)=b^{-d}\sum_r
f(bX+r)$, has a real Fourier multiplier $D_b(k)=\sin(bk/2)/(b\sin(k/2))$ — real, hence phase-
preserving (it cannot touch $e^{-i\Omega t}$) — with exact zeros at the fold points $k=2\pi m/b$
($1.7\times10^{-16}$ over $b=2\ldots5$), so it is also anti-aliasing. For any analytic
$\Omega(\kappa)=\sum_na_n\kappa^n$, the coarse-grained rule is $\Omega_\text{coarse}(\kappa)=
b\,\Omega(\kappa/b)$ (sympy-exact, symbolic in $b$), giving $[\kappa^n]\Omega_\text{coarse}=
a_nb^{1-n}$:

$$\boxed{\;c_\text{lat}\ (n=1)\text{ is an exact RG fixed point, eigenvalue }b^0=1;\qquad\text{lattice-artifact (LIV) operators }(n\ge2)\text{ are irrelevant, eigenvalue }b^{1-n}\;}\tag{R8.10}$$

(F129, Part A sympy-exact, symbolic in $b$; $T1/T2/K/RS/V$ machine precision.) Instantiated on the
even-law body-diagonal series, the leading LIV coefficient measured is $a_3=-1/(162\sqrt3)$,
matching R6.13's Chapter-6 closed form exactly, with RG eigenvalue $b^{-2}$: the continuum law
$\Omega=c_\text{lat}|\mathbf k|$ is the attractive IR fixed point, confirmed for $b=1\ldots5$ to
$<10^{-9}$. At the level of a genuine field simulation, not merely the dispersion, the block-spin
map **commutes with the propagator**, $\mathcal R_b\circ(\text{evolve}_\text{fine})^{bN}=(\text{
evolve}_\text{coarse})^N\circ\mathcal R_b$, verified to $5.5\times10^{-15}$–$1.3\times10^{-14}$ for
$b=2,3$: a coarse photon simulation, on $b^3\times$ fewer cells and $b\times$ fewer ticks, **is**
the fine simulation restricted to resolved modes, to the FFT floor. This licenses treating a coarse
lattice as a faithful stand-in for the free even-law photon sector specifically (F129's own scope
note: the chiral $W$/Weyl propagators and confinement are separate, not-yet-block-renormalised
directions, out of this chapter's remit).

### 8.2.9 Real-space propagation at the closed-form pair group velocity (F314)

Every result above is spectral. F314 closes the loop by building an actual localised wave packet
and propagating it with the unmodified even-law step. The pair group velocity in general is
$\partial\Omega_\text{pair}/\partial k_i(\mathbf k)=\tfrac{c_\text{lat}}2[\hat g_i^+(\mathbf
k/2)+\hat g_i^-(\mathbf k/2)]$ (a closed form matched against a central difference of R8.4 to
$\le9.1\times10^{-11}$ on all three axes) and, on a coordinate axis, exactly $c_\text{lat}$ at every
$k$ (R8.8's identity in guarded form). A one-sided (branch-pure) wrap-free packet, seeded on the
photon-beam convention already used at F105, crosses a $128\times48\times48$ lattice with:

$$\boxed{\;\text{measured asymptotic drift }=0.5728449064271057\ \text{vs. closed-form }\langle\partial\Omega_\text{pair}/\partial k_x\rangle=0.5728449064271062,\ \text{relative residual }7.8\times10^{-16}\;}\tag{R8.11}$$

(F314, 10/10 checks; test `F314-photon-packet-propagation`, gate tier.) Energy is conserved on the
*moving* packet to $3.7\times10^{-15}$; there is no transient (the first tick already moves at the
asymptotic speed, unlike a fixed-spinor fermion packet); and the finite-aperture speed deficit,
which F105 had only approximated ($1/(2(k_0\sigma_\perp)^2)$, wrong by $5.8\%$ of the deficit
itself), is now exact. **Being wrap-free is a condition on the carrier, not only the box**: the
residual backward-propagating tail of a one-sided seed runs at $-c_\text{lat}$ and must itself
decay before reaching the boundary, requiring $k_0\sigma_\text{axis}\gtrsim5$ (six decades of
boundary-weight improvement between $k_0\sigma_x=3.14$ and $5.89$, now the gate's asserted
ceiling). One genuinely open diagnostic surfaces in passing (not resolved by this finding, recorded
honestly): seeded as the codebase's own one-sided convention, the packet propagates as above;
seeded instead as a textbook in-phase transverse Maxwell mode (real, $\mathbf E\perp\mathbf B$, in
phase, Hermitian), the same even law gives **zero net drift** — the packet splits into
counter-propagating halves, because such a seed has spectral support at both $\pm\mathbf k_0$ and
$\Omega_\text{pair}$ is even in $\mathbf k$. F314 explicitly does not adjudicate which
$(\mathbf E,\mathbf B)$ identification is the physically correct one (§8.7 below).

### 8.2.10 The Casimir force as a source-channel effect of this photon (F207, F209)

The one measured, room-temperature observable routinely attributed to "zero-point energy" is a
direct test of whether this chapter's photon reproduces known physics without smuggling in the
non-gravitating homogeneous zero-point sum a separate finding (F193, Ch.20/21's territory) excludes
from gravitating. The Casimir mode sum is IR-dominated: an Abel–Plana reduction of the perfect-
plate mode sum is peaked at $s\sim1/L\to0$, exactly where R8.8's dispersion is $\Omega_\text{pair}
\to c_\text{lat}|\mathbf k|$ — gapless, isotropic, exact — so the textbook result is recovered with
**no approximation**:

$$\boxed{\;\frac{F}{A}=-\frac{\pi^2\hbar c_\text{lat}}{240\,L^4},\qquad\frac{E}{A}=-\frac{\pi^2\hbar c_\text{lat}}{720\,L^3}\;}\tag{R8.12}$$

(F207, C2, exact-algebraic closed form; force coefficient matches a numeric integral to
$<10^{-12}$.) The EM result is exactly twice the scalar-Dirichlet value because R8.5's
non-birefringence means both transverse polarisations ride the single rate $\Omega_\text{pair}$
with no TE/TM splitting to track. The force lives entirely in $H_\text{int}$, the coupling of this
photon to matter currents — confirmed with Jaffe's $\delta$-mirror model (F207, C4): as the plate
coupling $\lambda\to0$ the energy $\to0$, exactly the source/van der Waals picture the external
literature (Jaffe 2005; Nikolić 2016, `references/casimir-force-literature-and-model-integration.md`
§1) has moved toward as the *fundamental* reading of the Casimir effect, as against the older
"sum the zero-point modes" heuristic. Feeding the Casimir shift $E_C$ as beable $T^{00}$ into the
weak-field gravity source (F106/F178, forward-cited to Chapter 18) gives $\Delta m=E_C/c^2$ by exact
Gauss-law closure (F207, G1) — the cavity weighs less, like nuclear binding energy — but this is
**numerically degenerate** with the strong-equivalence-principle vacuum-buoyancy prediction
(Calloni/Avino), so a static weighing cannot discriminate the model's beable-source picture from
ordinary SEP.

F209 asks whether *modulating* the cavity (Archimedes-style reflectivity switching, or the
dynamical Casimir effect) can break that degeneracy, and finds it cannot, at any order: an
independent Gauss-closure computation of the beable weight and a buoyancy-definition computation of
the SEP weight agree bit-identically in the time domain and at **every** Fourier harmonic of the
modulation (F209, M1, exact-algebraic, residual $0$), and a homogeneous offset $\rho_0$ added to
$T^{00}$ (including the model's own bare vacuum-energy value) cancels exactly in any differential
(tared) weighing, independent of its magnitude (F209, M2, exact). The mechanism is structural, not
a leading-order coincidence: in the weak field the model *is* GR (PPN $\beta=\gamma=1$), so the two
gravitation routes are literally the same field equation applied to the same source, and every
lab-weighable quantity is by construction an energy *change*, which both pictures agree on:

$$\boxed{\;\text{the beable-vs-template split is not lab-accessible via the Casimir effect at any order of modulation}\;}\tag{R8.13}$$

(F209, 4/4 checks, exact-algebraic/exact/quantified negative.) This is reported as an honest,
sharpened negative result, not a discrepancy — it is exactly the outcome F207 itself anticipated and
F209 was built to check rigorously rather than merely assume.

### 8.2.11 The dielectric generalisation, scoped (F271)

One further generalisation belongs to this chapter's photon rather than to Chapter 18's gravity
sector proper, because it is the *photon's* propagator that is being extended, even though the
background field $K(\mathbf x)$ it propagates through is a gravity-sector object (F64's
impedance-matched dielectric, $A=1/K$, $B=K$). The obstruction an earlier eikonal treatment left
open (F270) is that the position- **and** momentum-dependent rescaling $\Omega_K(\mathbf x,\mathbf
k)=\Omega_\text{pair}(\mathbf k)/K(\mathbf x)$ is diagonal in neither basis, so no single
homogeneous FFT applies it, and the earlier fix used a single, free, stated central rate $\omega_0$
with an $O(1)$, non-convergent error. F271 lifts the already-existing 2-D variable-speed Weyl-walk
solver (`lattice.curved.weyl_step_2d_varc_strang`) to the 3-D $(\mathbf E,\mathbf B)$ pair and
supplies two corrections the 2-D reference lacked: **Weyl (symmetric) operator ordering**, needed
because $\delta(\mathbf x)\Omega(\mathbf k)$ is a product of non-commuting position and momentum
operators and only the symmetrised product $M=\tfrac12(\delta\Omega+\Omega\delta)$ is self-adjoint
(the asymmetric choice leaves a norm drift that plateaus at $1.1\times10^{-5}$ and does not improve
with substepping; the symmetric choice converges as $1/n_\text{sub}^3$, reaching $2\times10^{-10}$);
and the **second-order $h^2M^2$ term** the first-order Taylor truncation drops, without which the
scheme is globally first order (measured exponent $1.0$) rather than the second order Strang
symmetrisation is supposed to deliver (measured exponent $2.00$ once restored):

$$\boxed{\;\text{a uniform dielectric }K\text{ reproduces the free even-law rotation exactly (}4\times10^{-15}\text{); an inhomogeneous }K(\mathbf x)\text{ converges at measured order 2.00, with no free parameter}\;}\tag{R8.14}$$

(F271, established for the operator's exactness, convergence and norm behaviour.) **What this
chapter's photon-side result does not claim, stated as precisely as the finding states it.** The
deflection *coefficient* against the GR prediction $4GM/c^2b$ is explicitly not asserted: a
gradient-index test's apparent 25% discrepancy was traced to a narrow-packet artifact (the ratio
runs $1.455\to1.092\to0.959$ as the packet widens, converging toward the geometric-optics limit of
1, not a real 25% error), and confronting the operator against GR's actual deflection needs open
boundaries and a large lattice — unstarted, and explicitly a Chapter 18/19-scale gravity-sector
task, not this chapter's. Whether the block-spin renormalisation of R8.10 commutes with this
dielectric generalisation is also unverified and is named, not guessed at. This finding's own
subject is the photon propagator's operator correctness on an inhomogeneous background; its
physical payoff (bending light, gravitational lensing) is Chapter 18/19's to draw out.

### 8.2.12 F89: the singlet-channel identity, verified constructively — and one correction the theorem forces

F68's channel argument (§8.2.2's identity-channel forcing) was originally a commutator-level claim.
F89 verifies it constructively against the model's actual evolution operators, closing the question
"does the model contain two unrelated kinds of gauge-boson entity — a pair photon and a bilinear
boson?" A cross-branch $(+,-)$ pair's **singlet** bilinear $G_s=\phi^{\!\top}(i\sigma_y)\psi$
advances at exactly $\Omega_\text{pair}(\mathbf k)$ (residual $4.9\times10^{-13}$ over 2000 $k$, 8
ticks), matching the rotation angle the model's canonical even propagator actually applies, mode by
mode; a **same-branch** pair through the same bilinear operators instead rides the chiral law
$\Omega^\pm=2\omega^\pm(\mathbf k/2)$, with the split matching R8.2's birefringence exactly
(F89, T1a/T2/T4, residuals $\le4.9\times10^{-13}$, one identity exact $0$):

$$\boxed{\;\text{one bilinear entity, two channels: cross-branch pairing}\to\Omega_\text{pair}\text{ (the photon); same-branch pairing}\to\Omega^\pm\text{ (the chiral sectors)}\;}\tag{R8.15}$$

(F89, 10/10 checks against the real model operators, worst machine residual $4.9\times10^{-13}$.)
This confirms there is no second photon entity — "paired photon" and "$\sigma$-bilinear machinery"
are one object read in two irreps, exactly as R8.3's forcing theorem requires — and grounds F68's
commutator argument dynamically: the Hermitian identity channel $\phi^\dagger\sigma^0\psi$ is
invariant under transport (the U(1) coupling channel is blind, residual $2.8\times10^{-15}$) while
the Hermitian $\sigma$-vector precesses about $\hat{\mathbf n}$ at exactly $2\omega$ per tick — the
dynamical content behind $[P,U^\pm]=0$ versus $[\sigma_i,\hat{\mathbf n}\cdot\boldsymbol\sigma]\neq
0$.

**One correction, forced by F91 and not made by F89 itself.** F89's own summary table (written
2026-06-04, the same day as F91, but built independently of it) reads the "same-branch pair"
row as the uniform law for "**W/Z/gluon**" — i.e. it presents the chiral channel as the law all
three non-Abelian/massive sectors ride. R8.3's pairing-classification theorem, derived later the
same day, shows this is not uniformly correct: the $W^\pm$ row is exactly right (its coupling is a
pure left-projector, chiral **forced**), the $Z$ row is only approximately right (even is exact for
the vector part; the axial remainder is a mass-suppressed, $O(k^3/m_Z)$ branch split, not a clean
chiral law), and — the substantive correction — **the gluon row is wrong**: F91 §"G3"/§"Migration
executed" shows the gluon's colour coupling is branch-blind exactly like the photon's, so the even
law is forced for the gluon too, and the codebase was migrated from the chiral BCC gluon step to
the even one on 2026-06-04 (`docs/theory/supersessions.yaml` **S2**, `superseded: []` — a partial,
not wholesale, correction, exactly the S19-style pattern Chapter 7 already met once for F22). F89's
constructive result (R8.15, "no second photon entity") is unaffected by this — it is a statement
about the *photon's own* channel, verified independently of the gluon question — but its summary
table's blanket "W/Z/gluon" label for the chiral row should be read as "$W$ (forced), $Z$
(approximately, mass-suppressed defect), **not** gluon (even, forced, as migrated)."

**The `withdrawn` status of CL084 (F89's claim card), investigated.** `claims-index.md` lists
**CL084** as `status: withdrawn`. Reading the card directly (`docs/claims/CL084-...md`) shows this
status was `inferred` — the card's own `## Status & history` section states plainly that it read
"a supersession/withdrawal banner" in F89's header. **F89's own finding-file header carries no such
banner**: it reads `**Status:** Confirmed — 10/10 checks against the real model operators...`, with
no bracketed `[SUPERSEDED...]` or `[WITHDRAWN...]` text anywhere in the file, and F89 does not
appear as a `superseded:` entry in any of `supersessions.yaml`'s 23 records (only F91 itself,
listed as F91's *own* `by:` field in S2, appears near F89's name, as the finding that closes F89's
open item — a citation, not a retraction). This is the identical claims-layer bookkeeping pattern
Chapter 7 found for CL029/F15 (§7.2.3 of `07-relativity-on-a-lattice.md`): a mechanical,
prose-scraping seeding pass most likely mis-attributed a nearby finding's banner (a heavily
cross-referenced sibling finding) to F89's own header. **Unlike the CL029 case, however, this
chapter's own reading above (R8.15's correction) shows there is a genuine, substantive issue with
F89's table** — not the constructive result itself, which stands, but its blanket labelling of the
chiral row as "W/Z/gluon" law, which R8.3/F91 shows is correct for $W$ only. So CL084's
`withdrawn` status is very likely a mechanical artifact (the same class of error as CL029), **and**
there is independently a real correction owed to F89's own summary table, unrelated to why the
card reads `withdrawn`. Both facts are recorded precisely rather than let either explain the other
away. This chapter treats F89's constructive result (R8.15) as live and cites it accordingly, while
presenting only the corrected (post-F91) reading of its channel table.

> **Gap [G-6]:** F89's own summary table (2026-06-04) labels the same-branch/chiral propagation
> channel as the law for "W/Z/gluon" collectively. F91, derived the same day, shows this is correct
> only for the $W^\pm$ (chiral forced by a pure left-projector coupling); the $Z$ carries only a
> mass-suppressed chiral remainder on top of an exact even vector part; and the gluon's channel is
> **even**, forced by the identical branch-blindness argument as the photon's — the codebase was
> migrated from the chiral to the even gluon step that same day (`supersessions.yaml` S2). F89's
> own file was never edited to reflect this, and no `supersessions.yaml` record names F89 as
> partially corrected by F91 (S2's `superseded:` field is empty, and no other record covers F89
> specifically). Separately, and not to be conflated with this substantive correction,
> `claims-index.md`'s CL084 (F89's claim card) reads `status: withdrawn`, but this is very likely a
> mechanical seeding-pass artifact unrelated to the table error — F89's own header carries no
> supersession banner and F89 appears in no `supersessions.yaml` `superseded:` list. Flagged for
> whoever next touches F89 or F91's cross-references (most directly Chapters 12/13, which inherit
> the corrected $W$/$Z$/gluon channel assignments) to either add a corrective note to F89's own file
> or record a proper partial-supersession entry; not fixed here, as this chapter is
> documentation-only.

## 8.3 Results table

| # | Statement | Exactness | Residual / tolerance | Source |
|---|---|---|---|---|
| R8.1/R8.2 | RS eigenstates $\mathbf F_\pm=\mathbf E\pm i\mathbf B$ are the rotation's exact eigenvectors; Hermitian symmetry forces the unique branch assignment $h=\pm1\leftrightarrow\Omega^\pm(\mathbf k)=2\omega^\pm(\mathbf k/2)$ | exact (algebraic identity) | — | F37 |
| R8.3 | Pairing classification theorem: scalar $\propto\mathbb I$ coupling forces even channel (γ, gluon); projector $P_L$ forces chiral channel (W); Z mixed | exact-ℚ / structural-zero (5) / machine $\le2\times10^{-13}$ (6) | 13/13 | F91; test `test_F91_pairing_classification.py` |
| R8.4/R8.5 | Paired photon $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)=\Omega_\text{even}$; non-birefringent, massless, luminal, 2-polarisation spin-1 | exact (residual $0$ vs even law) / machine ($\le7.7\times10^{-6}$) | 5/5 | F69; CL002 (`live`, exact) |
| R8.6 | Binding gauge-protected: $E_b=0$ forced because the mass vertex's branch-coupling component $X\equiv0$ for the identity-channel photon | exact / machine $4\times10^{-17}$ | 4/4 | F168; CL148 (`live`, exact) |
| R8.7 | Interacting two-body wavefunction: normalizable threshold bound state; $T(0)=0$ exactly, masslessness inherited from gapless constituents | exact (residual $0$) / machine $5.6\times10^{-14}$ | 6/6 | F169; CL149 (`live`, exact) |
| R8.8 | On-axis dispersionlessness at every $k$, not only $k\to0$: $\Omega_\text{pair}(k\hat x)=\lvert k\rvert/\sqrt3$ | exact (algebraic identity) | $3\times10^{-15}$ | F105 |
| R8.9 | All-$k$ gauge pole: single massless transverse pole across the whole BZ; Ward identity; rank-2 residue; no doubler | exact (pole location, Ward, massless anchor) / machine $\le7\times10^{-16}$ (residue, unitarity) | 8/8 | F250; CL220 (`live`, exact) |
| R8.10 | Block-spin RG: $c_\text{lat}$ exact fixed point ($n{=}1$, eigenvalue $b^0$); LIV operators irrelevant ($n\ge2$, eigenvalue $b^{1-n}$); coarse run = fine run to FFT floor | exact (sympy, symbolic $b$) / machine $<10^{-9}$–$10^{-14}$ | 5/5 | F129; CL115 (`live`, exact) |
| R8.11 | Real-space packet propagates at closed-form pair group velocity; energy conserved on the moving packet; no transient | machine | $7.8\times10^{-16}$ | F314; CL283 (`live`, machine) |
| R8.12 | Casimir force reproduced exactly from the photon as a source/$H_\text{int}$ effect: $F/A=-\pi^2\hbar c_\text{lat}/240L^4$ | exact-algebraic | $<10^{-12}$ | F207; CL181 (`live`, exact) |
| R8.13 | Modulated Casimir: beable-vs-template degeneracy survives to all orders/harmonics — not lab-accessible via Casimir | exact-algebraic (M1) / exact (M2, M3) | residual $0$ | F209; CL183 (`live`, exact) |
| R8.14 | Dielectric-background generalisation: uniform $K$ exact, inhomogeneous $K(\mathbf x)$ converges at order 2.00 with Weyl ordering; deflection coefficient **not** claimed | exact (uniform) / machine, convergent (inhomogeneous) | $4\times10^{-15}$ (uniform); $2\times10^{-10}$ at $n_\text{sub}{=}64$ | F271; CL235 (`live`, exactness unset) |
| R8.15 | Singlet-bilinear channel identity verified constructively against real model operators; corrected reading: chiral row is $W$ (forced), $Z$ (mass-suppressed), **not** gluon (even, forced, migrated) | machine (identity) / — (table correction) | $4.9\times10^{-13}$ | F89 (corrected per F91/S2); CL084 investigated, §8.2.12 |

## 8.4 Comparison with measurement

The direct observational comparison for this chapter's headline claim — non-birefringence — is
carried out in Chapter 7, not re-derived here: R7.9/R7.10 (F30) show the linear-in-$k$ dispersion
term is chiral and cancels between the two paired helicities by exactly the mechanism R8.5 states
here, so unpolarised (net) time-of-flight dispersion is quadratic in every direction, and R7.5
(F301 §3.5) identifies this as the *same* helicity symmetrisation that gives the photon one order
of extra boost covariance over a bare chiral branch. **CL012** (`live`, `exact`) states the resulting
claim precisely: the physical photon is exactly non-birefringent, "structurally, not within a
tolerance" — falsified by any measured energy-dependent rotation of the polarisation plane from a
cosmological source with a *linear* energy dependence, the exact signature R8.5's mechanism forces
to cancel identically. This chapter adds two further, independently-verified consistency checks
beyond Chapter 7's dispersion-order argument: the Casimir force (R8.12) reproduces a real, measured,
room-temperature effect exactly, with no free parameter, from this same photon's IR dispersion; and
R8.13 shows that even the most direct conceivable lab discriminator between "the photon's vacuum
zero-point sum gravitates" and "only its configuration-dependent shift gravitates" — modulating a
Casimir cavity — cannot in principle separate the two pictures, at any order. Neither result is a
new falsification opportunity for the photon construction itself (both are honest negatives or
exact reproductions of known physics); both are evidence the construction does not silently
introduce new, unconstrained physics where none is observed.

## 8.5 What was excluded, and why

**The composite $\sigma$-bilinear photon (F39, and the underlying construction R8.1/R8.2 make
available), excluded as *the* photon.** The alternative construction R8.2 makes available — assign
each helicity to its own branch, $\mathbf F^+\to\Omega^+$, $\mathbf F^-\to\Omega^-$ — is not merely
a hypothetical: F39 builds it explicitly as a two-branch composite bilinear
(`EM_bilinears_two_helicity`, `w_propagation_step_chiral`) and confirms, at the bilinear level
rather than the field level F37 worked at, that it reproduces exactly the predicted chiral
dispersion per helicity (residual $1.5\times10^{-15}$ over 12 cases) and F30's closed-form
birefringence coefficient $\Delta\Omega=-(\sqrt3/27)k^2+O(k^4)$ to $4.5\times10^{-5}$ relative
(F39, FG6.5/FG6.6, 10/10 checks). **This construction is genuinely, linearly birefringent** — the
two circular polarisations acquire different phase velocities, $\Delta v_\phi/c_\text{lat}
\approx-k/18$ on the body diagonal, growing linearly with photon energy — and per
`docs/theory/supersessions.yaml` record **S1** (`superseded: [F65, F66, F67, F17, F18]`), this
linear vacuum birefringence is excluded by GRB/AGN polarimetry at the model's own gravity-fixed
cell size (F65/F66, not themselves assigned to this chapter and not re-derived here; their
conclusion is cited from S1's own summary, per `00-plan.md`'s routing of F65–F67 to Appendix A2).
S1's `reason:` field states the exclusion is not the only argument against this construction as the
photon: the same pairing is also the physical realisation of the U(1) identity channel R8.3's
minimal-coupling forcing requires — so the paired construction "was not merely permitted, it was
required."

$$\boxed{\;\text{the composite }\sigma\text{-bilinear photon (F39, S1) — excluded }\textit{as the photon}\text{: genuinely, linearly birefringent, ruled out by GRB/AGN polarimetry}\;}\tag{R8.16}$$

**What survives, precisely — and where it is going.** S1's `retained:` field is explicit and this
chapter states both halves, per `00-plan.md`'s own flagged trap: "the sigma-bilinear FIELD
CONSTRUCTION survives for the massive and non-Abelian sectors (W/Z/gluon), which are not under the
polarimetry bound. Only the photon attribution died." R8.3's pairing-classification theorem makes
this precise rather than a blanket exemption: the chiral, single-branch propagation law F39 built
is *forced*, not merely permitted, for the $W^\pm$ (whose coupling is a pure left-projector — the
even law is structurally excluded there, since a single-branch source can never populate the
cross-branch pair, F91 W2), *approximately* forced for the $Z$ (even exact for the vector part, a
mass-suppressed $O(k^3/m_Z)$ chiral remainder for the axial part, F91 Z3), and **not** forced for
the gluon, whose colour coupling is branch-blind exactly like the photon's own — the even law is
forced there too, and the codebase's BCC gluon step was migrated from chiral to even accordingly
(§8.2.12, S2). A chapter that said "the σ-bilinear construction is dead" would therefore be wrong in
two independent ways: it remains the canonical field construction for $W$/$Z$ (Chapter 12's
territory) and for the massive/confined sectors generally, and even the label "W/Z/gluon" for
"where the chiral law survives" needs the R8.3/R8.15 correction to be accurate. Chapters 12–13
inherit this corrected assignment directly.

**F65/F66/F67 themselves are not re-derived here.** Per `00-plan.md` §5, they are routed to
Appendix A2 as superseded findings, not assigned to this chapter; this chapter cites only S1's own
summary of what they showed (linear birefringence, excluded by polarimetry at the model's adopted
cell size) rather than reconstructing their argument.

**F306's supersession of the old curl-residual episode — not this chapter's photon, and not a
retraction of F306 itself.** A tempting but incorrect reading of F306's title ("the composite-photon
curl equation closes at $O(k^3)$") is that it somehow rehabilitates the retired $\sigma$-bilinear as
a candidate photon. F306's own text states the opposite explicitly: "this is not a new photon. The
$\sigma$-bilinear construction remains retired for the photon by S1-F69-sigma-bilinear-photon...
F306 says only that the curl equation was never the reason to retire it. The model's photon is
still the paired-spinor photon." What F306 corrects (superseding the *interpretation* of F21/F23/F25
per S18, with every underlying measurement reproduced bit-for-bit) is a three-month-old
representation artifact: the old curl-residual reading conflated a real 3-vector quadrature pair
with a complex Maxwell $(\mathbf E,\mathbf B)$ pair, producing a spurious, flat "$O(k)$ failure"
that was actually $c_\text{lat}$ times a quadrature factor; read with the amplitudes correctly as
analytic (not real-quadrature) quantities, the curl equation closes at $O(k^3)$ with coefficient
$c_\text{lat}^3/48=1/(144\sqrt3)$ — exactly the pass criterion the source QCA literature itself
states (`references/qca-papers-1-4-overview.md:407`).

**The `withdrawn` status of CL251 (F306's claim card), investigated.** As with CL084 above,
`claims-index.md` lists **CL251** as `status: withdrawn`, and the card's own text again states this
was `inferred` from "a supersession/withdrawal banner" the card's seeding pass detected in F306's
header. **F306's own header carries no such banner** — it reads `**Status:** Confirmed —
quantitative closed form, gate-tested`, and F306 appears in `supersessions.yaml`'s **S18** record
only as the *successor* (`by: [F306]`), never as a `superseded:` entry; the finding's own `##
Status` section states plainly, "**Live.** Gate record `F306-curl-closes-at-k3`, 5/5." Unlike F89's
case (§8.2.12), there is no substantive issue underlying CL251's `withdrawn` label either — F306's
content is exactly what its live status says. This is the identical mechanical seeding-pass
artifact Chapter 7 found for CL029/F15: most likely, the banner-detection heuristic picked up the
word "supersedes" (or the explicit `Supersedes the interpretation of:` line in F306's own header,
naming the *superseded* findings F21/F23/F25) and mis-attributed it to F306 itself. This chapter
treats F306's result (cited above, and already used identically in Chapter 6's R6.12/R6.13 and
Chapter 7's R7.11/R7.12) as fully live, consistent with those chapters' own treatment.

## 8.6 What is still open

1. **The identification of the Riemann–Silberstein pair with $(\mathbf E,\mathbf B)$ — this
   chapter's own foundational input (§8.1 item 1) — is a representation choice this chapter does
   not independently justify.** Mohr's six-component reformulation (`references/mohr-2010-maxwell-
   photon-wf-summary.md`) is offered as external corroboration that the packaging is legitimate,
   but Mohr's own paper is agnostic about whether the photon is composite or fundamental and does
   not itself adjudicate which real-vs-analytic-amplitude reading is physical — the same open
   question F314 surfaces concretely in real space (§8.2.9's in-phase-vs-one-sided seed comparison)
   and which F306 addresses only for the curl equation specifically, not for the seed convention
   generally. This is a genuine, disclosed open item across three findings (F306, F314, and Mohr's
   own comparison notes), not smoothed into a single answer here.
2. **The binding coupling strength that puts the photon exactly at two-body criticality is not
   derived from the U(1) minimal-coupling Lagrangian** (§8.1 item 3; F169's own "still external"
   item). F168 explains why the *threshold value*, if binding occurs at all, must be the
   gauge-protected one; it does not explain why binding occurs with exactly that critical strength
   rather than sub-critically (no bound state) or over-critically (a massive bound state, which
   R8.6 already excludes on structural grounds — so over-criticality is ruled out, but the
   under-critical alternative is not independently excluded by anything read for this chapter).
3. **A fully gauge-invariant, all-$k$ polarisation-tensor proof of the protected massless pole is
   not built.** F169 names this explicitly: "the naive single-cone f-sum does not cleanly cancel at
   the gapless Weyl point, so this needs the proper regularised treatment — not done here." F250's
   own all-$k$ pole proof (R8.9) is a tree-level/free-propagator statement; the loop-corrected
   self-energy is explicitly out of its scope.
4. **The deflection coefficient against GR is not claimed** by F271 (R8.14), and confronting it
   properly (open boundaries, weak field, large lattice) is unstarted — this is squarely Chapter
   18/19's task, not attempted here even in preliminary form.
5. **Whether the block-spin renormalisation (R8.10) commutes with the dielectric generalisation
   (R8.14) is unverified**, named explicitly by F271 rather than guessed at: "guessing would put an
   unverified factor inside a gravity result."
6. **Gap [G-6] (§8.2.12) is unresolved as documentation**: F89's own summary table has not been
   corrected in place, and no `supersessions.yaml` record formally captures the partial correction
   R8.3/S2 forces on it.

## 8.7 Falsifiers

From the relevant claim cards, at their actual status:

1. **CL002 (F69, the headline claim) carries `falsifier: stated`.** Any observation establishing
   the electromagnetic photon is *not* a composite two-Weyl-quantum bound state at the scale this
   model probes — most directly, any confirmed detection of linear vacuum birefringence with the
   energy dependence R8.2's excluded chiral construction predicts — would falsify the paired
   construction in favour of the excluded alternative (or some third option not considered here).
2. **CL012 (non-birefringence) carries `falsifier: stated`**: any measured energy-dependent rotation
   of the polarisation plane from a cosmological source with a *linear*, rather than absent, energy
   dependence — precisely the signal R8.5's pairing mechanism forces to cancel identically. This is
   the sharpest and most direct falsifier this chapter's construction carries; Chapter 7's R7.13
   already established it is roughly fifteen decades from any current bound.
3. **CL220 (F250, the all-$k$ gauge pole) is falsified in construction**, not by experiment, if any
   nonzero longitudinal/scalar residue component or any second pole is found anywhere in the BZ for
   the even-law propagator — a closed algebraic claim, checkable directly against R8.9's exact pole
   location and Ward-identity results.
4. **CL115 (F129, the RG fixed point) is falsified in construction** if the measured LIV-operator
   RG eigenvalue departs from $b^{1-n}$ at any order, or if a coarse-grained run of the free photon
   sector fails to reproduce the fine-grained run on resolved modes beyond the stated FFT floor.
5. **CL148/CL149 (F168/F169, binding) carry `falsifier: unset`** — declared debt in the claims
   layer, not a claim that no falsifier exists. The honest current state, per §8.6 item 2, is that
   no independent derivation of the critical coupling itself has been attempted; a demonstration
   that the U(1) minimal-coupling Lagrangian forces some *other* coupling strength — sub- or
   super-critical — would falsify the current picture that the photon sits exactly at threshold.
6. **CL181/CL183 (F207/F209, Casimir) carry `falsifier: unset`.** The clean, in-principle falsifier
   both findings name explicitly is the $O((a/L)^2)$ lattice-dispersion correction to the Casimir
   force — unobservably small ($\sim10^{-56}$ relative at laboratory $L$) but a genuine,
   model-specific prediction distinct from the textbook result, not currently reachable by any
   proposed measurement.
7. **CL235 (F271) carries no exactness class and no stated falsifier** — appropriately, since the
   finding itself is explicit that the deflection coefficient against GR (the observable that would
   let this construction be confronted with data) is not yet computed.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–7's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\mathbf F_\pm(\mathbf k)$ | The Riemann–Silberstein combinations $\mathbf E(\mathbf k)\pm i\mathbf B(\mathbf k)$; the exact eigenvectors of the $(\mathbf E,\mathbf B)$ rotation, eigenvalues $e^{\mp i\Omega}$. | §8.2.1 |
| $\Omega^\pm(\mathbf k)$ | The (excluded, chirally-faithful) single-branch photon dispersion, $\Omega^\pm(\mathbf k)=2\omega^\pm(\mathbf k/2)$; carries genuine linear birefringence. | §8.2.1 |
| $\Omega_\text{pair}(\mathbf k)$ | The physical paired-photon dispersion, $\equiv\Omega_\text{even}(\mathbf k)$ of Ch.6's R6.3, re-derived here as the rate a bound cross-branch two-Weyl-quantum pair necessarily carries. | §8.2.3 |
| $(g_L,g_R)$ | A sector's coupling weights on the two BCC chiral branches; the pairing-classification theorem's input (scalar $\propto\mathbb I$ forces even, projector $P_L$ forces chiral). | §8.2.2 |
| $T(\mathbf k)$ | The free two-body continuum floor, $\min_p[\omega^+(\mathbf k/2+p)+\omega^-(\mathbf k/2-p)]$; $\Omega_\text{pair}$ is its leading small-$\mathbf k$ form, exact only as $\mathbf k\to0$. | §8.2.5 |
| $M_6(\mathbf k)$, $P_T(\mathbf k)$ | The 6-vector $(\mathbf E,\mathbf B)$ evolution block operator and the transverse projector; $[M_6,P_T\otimes\mathbb I_2]=0$ exactly, the lattice Ward identity. | §8.2.7 |
| $K(\mathbf x)$ | The position-dependent dielectric (F64, Ch.18) this chapter's photon propagator is generalised to propagate through; forward-reserved here, owned by Ch.18. | §8.2.11 |

---

*New gap logged this chapter: **G-6** (§8.2.12), also recorded in `docs/monograph/GAPS.md`. No
finding, claim card, module, or test record was created or modified in the writing of this
chapter.*
