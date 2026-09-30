# Chapter 12 — Hypercharge and the Electroweak Sector

*Chapter 12 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F29-w-triplet-bilinear-su2-bridge.md`, `findings/F31-wmu-covariant-hopping.md`,
`findings/F32-wmu-free-propagation.md`, `findings/F33-wmu-yang-mills.md`,
`findings/F34-wmu-fermion-vertex.md`, `findings/F34b-wmu-mass-stueckelberg.md`,
`findings/F35-electroweak-mixing.md`, `findings/F36-wmu-backreaction.md`,
`findings/F38-fg1-anomaly-cancellation.md`, `findings/F41-hypercharge-higgs-free-su2.md`,
`findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md`,
`findings/F44-higgs-free-mA-zero-from-rank1-stueckelberg.md`,
`findings/F45-sigma-tau-swap-weinberg-angle.md`, `findings/F48-dynamical-Z-neutral-current.md`,
`findings/F49-bcc-finite-k-weinberg-angle.md`, `findings/F51-bipartite-sublattice-hypercharge.md`,
`findings/F54-fg8-beta-decay-charged-current.md`,
`findings/F138-weinberg-gap-closure-4piv-matching.md`,
`findings/F141-ws-cell-7axes-onshell-mass-counting.md`,
`findings/F143-wrap-loop-stiffness-nogo.md`,
`findings/F147-walk-loop-rigidity-channel-equality.md`,
`findings/F153-diamagnetic-chargeblind-splitting-paramagnetic.md`,
`findings/F231-weinberg-2over9-onshell-face-of-1over4.md`,
`findings/F279-hypercharge-constraint-attribution.md`,
`findings/F320-absolute-gauge-boson-masses-and-rho.md` (the twenty-five findings `00-plan.md` §2
assigns to this chapter, all read in full). Checked directly against `docs/theory/supersessions.yaml`
**S13** (F165→F279, read in full — the hypercharge-attribution correction this chapter adopts in
place of the superseded gravitational-anomaly account) and against a full grep of all twenty-five
finding numbers across the other 22 supersession records (zero hits — none of this chapter's
findings is itself superseded; the `F29`/`F31`/`F32` substring hits in a mechanical grep resolve to
unrelated findings `F298`/`F299`, confirmed by direct inspection). Checked against `claims-index.md`:
**CL007** (F41/F49/F138, `live`, `exact`, "the Weinberg angle is derived, with its scale" — this
chapter's Group D headline), **CL014** (F49/F138/F231, `live`, `exact`, the $\sin^2\theta_W=1/4$-at-
$4\pi v$-and-$2/9$-on-shell threshold claim), **CL276**/**CL277** (F320/F141/F138/F231/F49/F51,
`live`, `bracketed`/`exact`, the absolute-mass and $\rho=1$ cards — this chapter's capstone),
**CL010** (F165/F279/F47/F27/F41, `live`, `exact`, `falsifier: unset`, charge quantisation),
**CL016** (F138/F320, `withdrawn` by F320 itself — the old "$m_W$, $m_Z$ absolute are not claimed"
non-claim card, superseded within this chapter's own source material). Notation, postulates and
results are those of Chapters 1, 8, 9 and 11 (`01-postulates-and-ontology.md`,
`08-the-photon.md`, `09-electromagnetism.md`, `11-mass-without-a-higgs.md`) — $\psi$, $U(x)$,
$\Omega_\text{pair}(\mathbf k)=\Omega_\text{even}(\mathbf k)$, $\Omega^\pm(\mathbf k)$,
$c_\text{lat}$, $\omega^\pm(\mathbf k)$, $M(\theta)$ — extended, never redefined. Per Chapter 8's
Gap **G-6** (`docs/monograph/GAPS.md`), the corrected $W$/$Z$/gluon propagation-channel table is
used throughout: $W^\pm$ chiral (forced, pure left-projector coupling), $Z$ mostly-even with a
mass-suppressed chiral remainder, gluon even (Chapter 13's territory) — re-verified directly against
F91 itself (Chapter 8 §8.2.2, R8.3) rather than trusted from any single earlier summary. A genuine,
previously undisclosed architectural tension between that classification and this chapter's own
primary sources (the $W_\mu$ roadmap, F31–F36) is found and flagged as Gap **G-7** below.*

## 12.0 What this chapter establishes

Chapter 11 built the mass mechanism — a chiral $SU(2)$ connection $U(x)$ gauging the representation
freedom already present in the Dirac $\beta$ matrix — and explicitly stopped at the boundary of its
four assigned findings: "Hypercharge, the Weinberg mix, and the absolute $W$/$Z$ mass spectrum are
explicitly left to Chapter 12" (`11-mass-without-a-higgs.md` §11.2.4). This chapter keeps that
promise in full. It has three jobs, pursued largely in parallel across two decades of the project's
history (2026-05-24 through 2026-08-16) and reconciled here for the first time in one place:

1. **Promote $U(x)$'s $SU(2)_L$ part to a genuine dynamical gauge field $W_\mu$** — link variables,
   free propagation, Yang–Mills self-coupling, the fermion vertex, Stueckelberg mass generation,
   electroweak mixing into $A$/$Z$, and fermion back-reaction — the six-phase "$W_\mu$ roadmap"
   (F31–F36), bridged to Chapter 8's rotation-law machinery by F29 and completed by F48's dynamical
   $Z$ neutral current.
2. **Add hypercharge on the same connection $U(x)$**, per CLAUDE.md's Core Design Decision 3 ("no
   Higgs need be introduced"): compatibility with the Higgs-free chiral $SU(2)$ mass step (F41),
   extension to quarks and promotion of the right-handed singlets to dynamical $Y$-coupled fields
   (F42), a representation-theoretic derivation of *where* on the lattice hypercharge lives (F51),
   and a corrected account of what *closes* the hypercharge quantisation system (F279, replacing a
   superseded gravitational-anomaly claim with the model's own Majorana step).
3. **Derive the Weinberg angle, by three convergent routes, and the absolute $W$/$Z$ masses with
   $\rho=1$** — first-generation anomaly cancellation (F38) and the rank-deficient photon mass
   matrix (F44) as prerequisites; the internal $\sigma\leftrightarrow\tau$ swap counting giving
   $\sin^2\theta_W=\tfrac14$ (F45); the external BCC bond/sublattice counting giving $\tfrac29$
   (F49), given a representation-theoretic footing by F51 and a geometric one by F141's Wigner–Seitz
   lemma; the reconciliation showing these are *one angle, two faces* — a UV MS-bar cap at
   $\mu_\star=4\pi v$ and its IR on-shell endpoint at $M_Z$ (F138, F231) — rather than competing
   values; two independent no-go results (F143, F147) proving the free fermion sea cannot itself
   supply the stiffness that would turn either counting into an exact number, redirecting that work
   to the Higgs-free condensate sector; and the chapter's capstone, F320's elimination of F141's
   free normalisation quantum against $e=g\sin\theta_W$, giving **closed-form absolute** $m_W$ and
   $m_Z$ from only $\{\alpha,G_F\}$ — one fewer electroweak input than the Standard Model needs —
   together with $\rho=1$ derived from the *rank* of the Higgs-free breaking rather than from
   custodial $SU(2)$, which this model does not have. F54 closes the chapter's physics content by
   running the whole first-generation charged-current chain, $d\to u+e^-+\bar\nu_e$, end to end.

## 12.1 Inputs

**Postulates used.** **P6** is the central postulate of this chapter, in the fullest sense it has
been used anywhere in the monograph so far: Chapter 11 derived the *mass* mechanism P6 promises;
this chapter derives everything else P6's own text reserves for it — "Hypercharge is carried on
this same connection $U(x)$, not on a separate scalar sector" (`01-postulates-and-ontology.md`
§1.2). **P5** (the massless Weyl-spinor primitive) is the field every current, vertex and doublet
bilinear in this chapter is built from; no Dirac mass step is assumed anywhere except where §12.2.1
onward explicitly invokes Chapter 11's mechanism. **P4** (exact unitarity) underwrites every
machine-precision and exact-algebraic result below — the $SU(2)_L$ link unitarity of F31, the
Ward identities of F34/F41/F42, the mass-matrix rank-deficiency of F44 — in the same sense it
underwrote Chapters 8, 9 and 11. **P1–P3** (discreteness, locality, the BCC lattice and its point
group $O_h$) enter through the specific integer counts this chapter's Weinberg-angle derivations
consume directly and without approximation: the $2$ BCC sublattices (F51), the $7$ Wigner–Seitz
facet axes (F141), and the exact $O_h$ symmetry that forces the counting's cross-set equalities
where they hold. **P7** (the elegant-design heuristic, Ch.1's Gap G-1) is invoked once, explicitly,
in the same place Chapter 8 flagged it: F91's even-vs-chiral forcing argument, which this chapter's
own Gap **G-7** below shows was never actually applied to the $W_\mu$ roadmap's own construction.

**Prior results used, precisely.** **R11.1–R11.6** (Ch.11, F27) are the mass step $M(\theta)$ and
the pure-gauge field $U(x)$ this chapter's hypercharge extension (F41, F42) and $SU(2)_L$-gauged
Stueckelberg construction (F34b, F44) directly extend — nothing about the mass mechanism itself is
re-derived. **R8.3** (Ch.8, F91) is the pairing-classification theorem this chapter inherits *as
corrected* by Gap G-6: $\gamma$ and gluon even (forced, scalar coupling), $W^\pm$ chiral (forced,
pure $P_L$ coupling, $\|P_L\psi_R\|=0$ exactly), $Z$ mostly even with a mass-suppressed chiral
remainder. **R9.1/R9.2** (Ch.9, F68) is the single-sector seed R8.3 generalizes; this chapter does
not re-derive either, but §12.2.1 shows directly that the $W_\mu$ roadmap's own primary source
(F32) reaches an apparently different conclusion about which dispersion law the $W$ field actually
carries — engaged in full as Gap G-7, not smoothed over. **R6.3** (Ch.6, the even rotation law
$\Omega_\text{even}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$) is the exact object
F29 and F32 both verify the $W$-triplet bilinear and the free $W_\mu$ field reproduce component by
component.

**Free inputs consumed — the chapter's most consequential accounting.** This chapter's headline
result (F320) is that $m_W$ and $m_Z$ are predicted from **exactly two** electroweak inputs, where
the Standard Model needs three ($\{\alpha, G_F, m_Z\}$ against $\{\alpha, G_F\}$). What those two
inputs actually *are* must be stated with the same precision Chapter 9 used for its own no-go:

1. **$\alpha_\text{em}$ is external, exactly as Chapter 9 disclosed, and this chapter's dependence
   on it is new and load-bearing, not incidental.** Chapter 9 (§9.3, R9.10–R9.12) established that
   $\alpha_\text{em}\approx1/137.036$ is "the model's last irreducible dimensionless input" — four
   independent avenues to derive its magnitude from the lattice rule all report a sharp or
   inconclusive negative (F127), with two concrete but unattempted reopening routes named (F339)
   and independent non-perturbative evidence corroborating two of the four closures (F349). This
   chapter does not revisit that no-go and does not attempt to close it. What changes here is only
   the *weight* $\alpha_\text{em}$ carries: before this chapter it fixed the electron's coupling to
   the photon; after F320 it is *also* the sole magnitude input (via $e^2=4\pi\alpha$) that,
   combined with the model's own derived coupling-ratio structure, fixes $g$, $g'$, and hence
   $m_W$ and $m_Z$ in absolute GeV. F320 states this plainly: "It was the one EM input; it is now
   also an input to the boson masses, so its weight increased." This is exactly the kind of
   dependency Chapter 9 asked later chapters to disclose explicitly rather than let look like a
   hidden inconsistency — stated here in full: **the absolute electroweak boson masses derived in
   this chapter rest on an external input Chapter 9 already flagged as undlerived, not on a hidden
   new assumption.**
2. **$G_F$ (equivalently $v=(\sqrt2\,G_F)^{-1/2}=246.22$ GeV) is likewise external — not a lattice
   prediction, but the SI/EW-scale ruler this chapter takes as given.** F119 (cited by F138, F320,
   not itself a Chapter 12 finding) finds the overall mass scale $N=m_\text{lat}(\tau)$ has no
   $O(1)$ lattice mechanism and remains `FIT (N=1)`. F320 is explicit and undiluted about this:
   "$v$. F119's $N$ has no $O(1)$ mechanism... Everything [in F320] is *relative to* $v$." So the
   absolute-mass prediction is a prediction of $m_W$ and $m_Z$ *given* $v$ and $\alpha$, not a
   prediction of $v$ itself — which remains, as it was before this chapter, an external SI anchor
   forward-cited to Chapter 17.
3. **The compositeness matching scale $\mu_\star=4\pi v$ (F138) is Naive-Dimensional-Analysis
   (NDA), not a computed number.** It is the scale at which $\sin^2\theta_W=\tfrac14$ is taken to
   hold exactly (§12.2.4 below); the measured trajectory actually crosses $\tfrac14$ at
   $\mu_\times=3.42$ TeV, an $e^{0.099}$ (10%) offset from $4\pi v=3.094$ TeV, which F138 explicitly
   attributes to NDA's own $O(1)$ ambiguity, not to a derivation error, and which F143 (§12.2.6
   below) subsequently bounds: the one computable correction to $\mu_\star$ (a fermion loop) moves
   it by at most $0.2\%$, an order of magnitude below the NDA offset itself.
4. **The equal-stiffness hypothesis (U) that underlies F141's $2:7$ mass counting and F320's
   elimination of the stiffness quantum $u$ is a structural assumption, not (yet) a derivation from
   the model's own condensate dynamics.** F320 states this without qualification: "F141's hypothesis
   (U)... all still open... This finding makes (U) carry strictly more than it did." §12.2.9–12.2.11
   below carry the full honest status of (U) rather than treat F320's use of it as settled.
5. **Nothing else in this chapter's structural results (the anomaly traces, the Ward identities,
   the mass-matrix rank, the $\Delta r$-cancellation theorem) is free** — each is a closed-form or
   exact-rational consequence of the charge assignments, the gauge structure, or the algebra of the
   mass matrix, introducing no additional fitted constant beyond items 1–4 above.

## 12.2 The derivation

### Group A — building $W_\mu$ as a dynamical gauge field

#### 12.2.1 The bridge from the photon's rotation law to the chiral $SU(2)$ doublet (F29)

Before any dynamical gauge field exists, one bilinear-level question needs an answer: does
extending Chapter 8's photon bilinear machinery to isospin doublets, using $\tau^a$ on the isospin
index to build a "W-triplet" analogue, obey the same rotation law and behave cleanly under $SU(2)$?
F29 (2026-05-23, predating the $W_\mu$ roadmap by one day) answers yes on both counts, using the
**Hermitian** doublet bilinear $W_H^{a,i}(\mathbf k)=\sum_{\alpha\beta}(\tau^a)_{\alpha\beta}
(\phi^\alpha)^\dagger\sigma^i\psi^\beta$ rather than the earlier transpose form (which is *not*
$SU(2)$-clean — $V^TV\ne\mathbb I$ for $V\in SU(2)$, confirmed by a structural $O(1)$ deviation):

$$\boxed{\;\text{each }W^a\text{ component rotates under }R(\Omega)\text{ with }\Omega(\mathbf k)=2\omega_\text{BCC}(\mathbf k/2)\text{, exactly conserved norm, transverse residual matching the photon's }c_\text{lat}\mathbf k\text{ scaling}\;}\tag{R12.1}$$

(F29, 8/8 checks PASS, exact/machine $\le6.7\times10^{-16}$.) The triplet transforms as the
$SU(2)$ **adjoint** under a doublet rotation $V(x)$ ($R^{ab}(V)=\tfrac12\mathrm{tr}(\tau^aV\tau^bV^\dagger)$,
residual $3.08\times10^{-16}$), and the total triplet magnitude $\sum_a\|W^a\|^2$ is exactly
$SU(2)$-invariant. This is the bridge between Chapter 6's rotation-law machinery (inherited by
Chapter 8's photon) and Chapter 11's chiral $SU(2)$: it establishes, at the kinematic/bilinear
level, that a triplet built on the F27 doublet inherits Chapter 6's even-rotation propagation
component by component — before the $W_\mu$ roadmap makes this a genuine dynamical field. F29's own
"Known Limitations" are explicit that this is a **kinematic** bridge only: "these are kinematic
tests at the bilinear level... the kinetic step is still $SU(2)$-gauge-broken in absence of
$W_\mu$," setting up exactly the six-phase programme §12.2.2–12.2.7 completes.

#### 12.2.2 Phase 1 — $SU(2)$ link variables and exact covariant BCC hopping (F31)

F31 (2026-05-24) introduces $SU(2)$ link variables $U_\ell\in SU(2)$ on all 8 BCC nearest-neighbour
hop directions and builds a gauge-covariant Weyl step. Because the BCC hop is a *fractional* shift
($e^{i\mathbf k\cdot\mathbf d/\sqrt3}$, not an integer `np.roll`), two constructions are needed and
kept distinct rather than conflated: a **site-average** step (`covariant_weyl_step_3d_bcc`), which
conserves the doublet norm exactly for *any* unitary link field but satisfies the Ward identity only
to $O(a)$ for spatially varying $V$ — the lattice-QCD-style $O(a)$-improved-action situation, not a
defect — and a **per-link exact** step
(`covariant_weyl_step_3d_bcc_exact`), which satisfies the local $SU(2)_L$ Ward identity
$V(x)\cdot\text{step}(\psi;U)=\text{step}(V\psi;VUV^\dagger)$ at machine precision for constant $V$
but is not norm-conserving off that special case:

$$\boxed{\;U_\text{BCC}(\mathbf k)=\sum_{\mathbf d\in\text{BCC}}M_{\mathbf d}\,e^{i\mathbf k\cdot\mathbf d/\sqrt3}\text{, both link-covariant steps reduce exactly to the free BCC step at }U_\ell=\mathbb I\text{, Ward identity }1.2\times10^{-17}\;}\tag{R12.2}$$

(F31, 6/6 checks PASS, machine $\le1.9\times10^{-14}$/exact.) This is Phase 1 of the $W_\mu$
roadmap, and it partially closes Chapter 11's own F27 "Known Limitation 1" (the kinetic step is not
$SU(2)$-invariant without a gauge field) — full closure is deferred, correctly, to Phase 4 (§12.2.5).

#### 12.2.3 Phase 2 — free $W$ propagation and the even-dispersion requirement (F32)

F32 (2026-05-24) establishes that the free $W_\mu$ field propagates as a triplet of decoupled
photon-like objects. The critical technical content is a **reality constraint**, not a coupling-
structure argument: the BCC dispersion is chirally asymmetric, $\omega^+(-\mathbf k)=\omega^-(\mathbf
k)\ne\omega^+(\mathbf k)$ in general, and the gauge potential $W$ is a real field, so its Fourier
transform must carry Hermitian symmetry, $\hat W(-\mathbf k)=\hat W(\mathbf k)^*$. Applying the
chirally asymmetric rotation $\Omega=2\omega^+(\mathbf k)$ **breaks** that symmetry outright,
measured directly as IFFT imaginary parts up to $\sim0.8$ (not round-off) and $\sim56\%$ energy
drift over 200 steps. The fix, adopted throughout the rest of the roadmap, is the **symmetrized
(even)** dispersion already familiar from Chapter 8's photon:

$$\boxed{\;\Omega_W(\mathbf k)=\Omega_\text{even}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)\text{, exact Hermitian symmetry, energy drift }3.1\times10^{-14}\text{ over 200 steps, vs. }56\%\text{ under the chiral law}\;}\tag{R12.3}$$

(F32, 4/4 checks PASS, machine $\le3.1\times10^{-14}$.) The three isospin components propagate as
exactly decoupled abelian channels at this order (superposition and zero-seepage both hold to
residual $0.0$), and both dispersion choices agree in the continuum limit $\Omega\to2c_\text{lat}
|\mathbf k|$ — no physical distinction survives $\mathbf k\to0$. **This result is the seed of Gap
G-7 below**: F32 rejects the chiral single-branch law for the $W$ field on physical grounds (a real
classical field cannot propagate stably under it), a full eleven days before F91 derives that the
$W^\pm$'s own fermion coupling structurally *forces* precisely that chiral law. The tension between
these two results, never reconciled anywhere in the sources read for this chapter, is stated in
full at §12.2.12.

#### 12.2.4 Phase 3 — Yang–Mills self-coupling on the BCC lattice (F33)

F33 (2026-05-24) promotes $W_\mu$ from a background field (Phases 1–2) to a genuinely dynamical one
via the non-Abelian Wilson plaquette action. The field strength $F^a_{\mu\nu}(x)=-\tfrac i2
\mathrm{tr}[\tau^a(U_\square(x)-U_\square^\dagger(x))]$, built from the BCC composite-link plaquette
$U_\square=U_\mu(x)U_\nu(x{+}\hat\mu)U_\mu^\dagger(x{+}\hat\nu)U_\nu^\dagger(x)$, is exactly zero at
the identity-link vacuum (bit-for-bit), non-trivial for random links (confirming the commutator
term $g[A_\mu,A_\nu]$ genuinely enters, not merely the Abelian case by accident), and gauge-
invariant under constant $SU(2)$ rotation acting on $F$ as the adjoint ($\|F\|^2$ invariant,
residual $5.93\times10^{-16}$):

$$\boxed{\;F^a_{\mu\nu}(x)=-\tfrac i2\mathrm{tr}[\tau^a(U_\square-U_\square^\dagger)]\text{, gauge-invariant }\|F\|^2\text{, link unitarity preserved to }10^{-13}\text{ after self-coupling steps, Yang-Mills action decreases under gradient flow}\;}\tag{R12.4}$$

(F33, 5/5 checks PASS, exact/machine $\le5.93\times10^{-16}$.) This is the non-Abelian self-coupling
Phase 2's abelian-decoupled triplet lacks — the commutator structure that will, at Phase 7 (§12.2.8),
carry the fermion source back into the gauge sector.

#### 12.2.5 Phase 4 — the fermion vertex, full closure of the doublet's gauge covariance (F34)

F34 (2026-05-24) wires the Phase 3 dynamical $W_\mu$ field into the Dirac doublet stepper via a
Strang-split kinetic-mass-kinetic step, $\psi(t{+}dt)=K(dt/2)M(dt)K(dt/2)\psi(t)$, with the
left-handed $\eta=(\nu_L,e_L)$ doublet coupling to $W_\mu$ links and the right-handed $\chi$ using
identity links — matching Chapter 11's own construction (R11.5's $V(x)$-only-on-$\eta$ Ward
identity) exactly. This is the full closure of F27's Known Limitations 1 and 2:

$$\boxed{\;V(x)\cdot\text{step}(\psi;U)=\text{step}(V\psi;VUV^\dagger)\text{ to }1.687\times10^{-17}\text{; }\chi\text{ exactly decoupled from }W\text{ at }m=0\text{ (residual }0.0\text{, bit-for-bit)}\;}\tag{R12.5}$$

(F34, 5/5 checks PASS, exact/machine $\le1.854\times10^{-13}$.) The Ward identity's proof is by
induction on the Strang split: the kinetic step satisfies it by F31's covariant construction, the
mass step by F27's own mass Ward identity (Ch.11, R11.5), and their composition inherits both
exactly — this is the concrete mechanism by which Chapter 11's mass sector and this chapter's kinetic
sector fit together into one covariant object. The right-handed decoupling at $m=0$ is the same
exact-chirality statement Chapter 11 already established for the mass step alone (R11.5), now shown
to survive the addition of a dynamical gauge field: at $m=0$, $\chi$ is a **complete spectator** to
$W_\mu$, bit-for-bit, the defining property of a chiral gauge theory realised in the construction
rather than imposed on it.

#### 12.2.6 Phase 5B — Stueckelberg $W$-boson mass generation (F34b)

F34b (2026-05-24) generates a $W$ mass without a Higgs VEV, via the Stueckelberg/non-linear-sigma
mechanism: a scalar $SU(2)$ field $U_\text{st}(x)$ acquires a kinetic energy
$\mathrm{tr}[(\partial_\mu U_\text{st})^\dagger(\partial_\mu U_\text{st})]$ that plays the role of
the mass term, $m_W=gf$, $f=\sqrt{\langle|\partial_\mu U_\text{st}|^2\rangle}$:

$$\boxed{\;U_\text{st}=\mathbb I\Rightarrow m_W=0\text{ exactly; random }U_\text{st}\Rightarrow m_W>0\text{; }m_W\text{ exactly gauge-invariant under constant }SU(2)\text{ (residual }0.0\text{); all three longitudinal components non-zero for a generic }U_\text{st}\;}\tag{R12.6}$$

(F34b, 5/5 checks PASS, machine $\le1.776\times10^{-15}$/exact.) The promotion of Chapter 11's mass
link $U_m(x)$ to a dynamical field is precisely the Stueckelberg interpretation: $U_m(x)$ *is* the
longitudinal Goldstone of $SU(2)_L$ symmetry breaking, and the gradient-flow evolution of
$U_\text{st}$ (a heat-kernel step, $\hat U_\text{st,new}(k)=e^{-dt\,k^2}\hat U_\text{st}(k)$)
monotonically damps its kinetic energy — a $79.5\%$ reduction measured over five steps.

#### 12.2.7 Phase 6 — electroweak mixing: the Weinberg angle as an input, the Weinberg rotation as an exact algebraic structure (F35)

F35 (2026-05-24) implements the Weinberg mixing itself, treating $\theta_W$ as an **input**
parameter at this stage (its first-principles value is Group D's separate business, §12.2.13
onward). The $O(2)$ rotation $(A,Z)^\top=R(\theta_W)(B,W^3)^\top$ is verified to be an exact
inverse of its own unmixing (residual $8.9\times10^{-16}$), to **commute** with the free
$\Omega_\text{even}$ propagation law at every $\theta_W$ (residual $\le2.2\times10^{-15}$ — the
Weinberg rotation and the photon's own causal structure are structurally independent operations),
and to reproduce two exact algebraic identities with no further input:

$$\boxed{\;\frac{m_Z}{m_W}=\frac{1}{\cos\theta_W}\text{ (residual }0.0\text{, bit-for-bit); }Q=T_3+\frac Y2\text{ exact for all 7 first-generation states (residual }5.6\times10^{-17}\text{)}\;}\tag{R12.7}$$

(F35, 5/5 checks PASS, exact/machine $\le2.22\times10^{-15}$.) This is the Gell-Mann–Nishijima
relation, verified here for the first time on the model's actual per-species hypercharge and
isospin registry (the values Group C's F38 later shows are anomaly-consistent), and the mass-ratio
identity F44 (§12.2.16) will show is not merely algebra but a structural consequence of the
model's own rank-deficient photon mass matrix.

#### 12.2.8 Phase 7 — Yang–Mills back-reaction and massive $W$ (Proca) dispersion (F36)

F36 (2026-05-24) closes the loop between the fermionic and bosonic sectors: the left-handed isospin
current $J^a(x)=\psi_L^\dagger(\tau^a/2)\psi_L$ sources the gauge field via the linearized Yang-Mills
equation $\partial_t\hat E^a(\mathbf k)=\Omega(\mathbf k)\hat B^a(\mathbf k)+g\hat J^a(\mathbf k)$,
with the diagonal-in-$a$ coupling structure verified exactly (a pure-$J^3$ source drives only $W^3$;
after 10 steps $W^1=W^2=0$ exactly, no cross-isospin leakage). The massless BCC dispersion is
replaced by the full Proca form:

$$\boxed{\;\omega^2(\mathbf k)=m_W^2+\Omega_\text{even}^2(\mathbf k)\text{, verified to }\le1.4\times10^{-13}\text{ across three masses; massless limit exact (residual }0.0\text{, bit-for-bit)}\;}\tag{R12.8}$$

(F36, 5/5 checks PASS, exact/machine $\le1.4\times10^{-13}$.) The factor of 4 relative to the naive
continuum $c_\text{lat}^2|\mathbf k|^2$ limit arises from the double-BCC-hop structure of the
paired-style rotation, not from any modification of $c_\text{lat}$ itself; the model treats lattice
UV structure and mass as separate, orthogonal ingredients — mass sets the $\mathbf k=0$ gap, lattice
geometry sets the high-$\mathbf k$ structure, and the massless limit reducing exactly (not just
approximately) to the free step is the direct check that this separation is clean.

#### 12.2.9 A dynamical $Z$, and the F45 electron-coupling prediction (F48)

F48 (2026-05-28) is not among the strict $W_\mu$-roadmap phases the assigned-findings list labels
F31–F36, but belongs logically at the end of that programme: it promotes F35's algebraic Weinberg
mixing to a **propagating** $Z$ field with a genuine, dynamical, per-species fermion neutral-current
source — the last piece needed before Group F's end-to-end integration (F54). The neutral current
$J^Z_0(x)=J^3_0(x)-\sin^2\theta_W\,J^\text{em}_0(x)$ is built explicitly from per-species densities
and cross-checked against the SM per-species sum $\sum_f(g_L^f\rho_L^f+g_R^f\rho_R^f)$, agreeing to
FFT floor; the $Z$ propagates under the same $\Omega_\text{even}$ rotation as the photon
(massless case) and under the identical Proca form of R12.8 (massive case). The chapter's first
genuinely non-trivial numerical *prediction* using a first-principles Weinberg angle appears here:

$$\boxed{\;g_V^{e_L}=T_3^{e_L}-2Q^{e_L}\sin^2\theta_W=-\tfrac12-2(-1)(\tfrac14)=0\text{ exactly, at the F45 bare lattice angle }\sin^2\theta_W=\tfrac14\;}\tag{R12.9}$$

(F48, 12/12 checks PASS, 6 bit-for-bit zero, remainder $\le1.5\times10^{-13}$.) The counter-check at
the PDG on-shell angle ($\sin^2\theta_W\approx0.231$) gives $g_V^{e_L}\approx-0.038$, visibly
non-zero — confirming the vanishing at $\sin^2\theta_W=\tfrac14$ is a genuine structural feature of
the F45 swap geometry, not a generic property of the vector-coupling formula. This is, in effect,
the same $-12\%$ gap between F45's bare $\tfrac14$ and the measured angle expressed in a different
observable, and it is closed by exactly the same physics (Group D) that closes the mass ratio gap.

### Group B — hypercharge

#### 12.2.10 Hypercharge compatible with the Higgs-free chiral $SU(2)$ mass model (F41)

Chapter 11's F27 mass step couples $\eta_L$ (hypercharge $Y_L=-1$) directly to $\chi_R$
($Y_{e_R}=-2$ or $Y_{\nu_R}=0$); under a naive $U(1)_Y$ rotation the bilinear $\eta^\dagger\chi$
picks up a non-trivial phase $\alpha(Y_R-Y_L)/2\ne0$, so the bare F27 mass step is **not**
$U(1)_Y$-invariant. F41 (2026-05-26) resolves this by extending $U(x)$ to carry the Higgs-equivalent
hypercharge as a diagonal factor,
$U(x)\to U(x)\cdot\mathrm{diag}(e^{i\alpha\Delta Y_\nu/2},e^{i\alpha\Delta Y_e/2})$ with
$\Delta Y_e=Y_L-Y_{e_R}=+1$ and $\Delta Y_\nu=Y_L-Y_{\nu_R}=-1$ — exactly the SM Higgs hypercharge
and its conjugate, respectively:

$$\boxed{\;U(1)_Y\text{ Ward identity exact for both branches ({\le}9.2\times10^{-16}); SU(2)_L Ward identity preserved unchanged; mass step unitarity preserved; no isospin leakage at }U=\mathbb I\;}\tag{R12.10}$$

(F41, 7/7 checks PASS, machine $\le9.16\times10^{-16}$/exact.) This is a clean re-interpretation of
the Standard Model's Higgs hypercharge $Y_\Phi=+1$: it is not a property of any physical scalar, but
the hypercharge $U(x)$'s pure-gauge phase must carry for the chiral mass step to commute with
$U(1)_Y$ at all. The extra phase degree of freedom costs one additional Goldstone mode, exactly the
one Stueckelberg (F34b, §12.2.6) eats to give the $Z$ its longitudinal mode — nothing about F34b's
construction changes; F41 simply identifies which physical role its extra Goldstone plays.

#### 12.2.11 Hypercharge extended to quarks; right-handed singlets promoted to dynamical $Y$-coupled kinetic fields (F42)

F42 (2026-05-27) closes two follow-ups F41 itself named. First, the quark mass step ports verbatim:
$\Delta Y_u=Y_{Q_L}-Y_{u_R}=-1$ and $\Delta Y_d=Y_{Q_L}-Y_{d_R}=+1$ are **numerically identical** to
the lepton $(\Delta Y_\nu,\Delta Y_e)$ pair — this is not a coincidence but a direct consequence of
$\Delta Y$ depending only on $Y_L-Y_R$, which the Standard Model's single Higgs field enforces to be
the same $(-1,+1)$ pair across generations and species (up-type vs. down-type); in the Higgs-free
construction it is the fact that one extended $U(x)$ field with two diagonal phase eigenvalues
services both sectors. Second, and more consequentially, the right-handed singlets ($e_R,u_R,d_R$),
previously passive spectators, are promoted to genuinely **dynamical** $Y$-coupled fields via a
site-centred Stueckelberg wrap of the spectral kinetic step:

$$\boxed{\;\chi(x)\xrightarrow{e^{-i\alpha(x)Y/2}}\tilde\chi(x)\xrightarrow{U_W(\mathbf k,\Delta t/2)}\tilde\chi'(x)\xrightarrow{e^{+i\alpha(x)Y/2}}\chi'(x)\text{, exact gauge covariance for any }\alpha(x),\beta(x)\;}\tag{R12.11}$$

(F42, 8/8 checks PASS, machine $\le9.93\times10^{-16}$/exact.) The gauge-covariance identity
$S[\alpha+\beta](e^{i\beta Y/2}\chi)=e^{i\beta Y/2}S[\alpha](\chi)$ is checked for each of the three
singlets with random $\alpha,\beta$; at $\alpha\equiv0$ the step reduces bit-for-bit to the bare
spectral Weyl half-step, so every prior F27/F41 test not switching on $\alpha$ is unaffected. This
closes the first-generation completeness review's item 3 (dynamical $e_R,u_R,d_R$ via kinetic-step
$U(1)_Y$) and is the direct prerequisite for F48's dynamical $Z$ (§12.2.9), since the $Z$ couples
to $\chi$ through its $Y$-component.

#### 12.2.12 The bipartite sublattice as the unique carrier of hypercharge (F51)

F49 (Group D, §12.2.15) left an explicit gap: its BCC-geometric $2:7$ counting invoked a
"sublattice-staggered $U(1)$" for hypercharge without deriving *why* the sublattice degree of
freedom, rather than some other internal structure, should carry it. F51 (2026-05-29) closes this
by representation theory. The BCC Weyl walk is bipartite: every body-diagonal hop changes the
coordinate sum by an odd integer, so the sublattice parity $P=(-1)^{x_1+x_2+x_3}$ **anticommutes**
with the one-tick unitary, $\{P,W\}=0$ exactly ($1.05\times10^{-15}$). Because $W^2$ is even under
this shift, $P$ is conserved by the *physical* (stroboscopic, two-tick) dynamics — $[W^2,P]=0$
($1.8\times10^{-15}$) — generating a genuine abelian $U(1)_P=e^{i\theta P}$:

$$\boxed{\;U_Y(\theta)=e^{i\theta P}\text{ is (1) abelian, (2) stroboscopically conserved, (3) a Schur scalar on the spin/isospin }SU(2)\text{ (}[P,\sigma_a]=0\text{ exactly), (4) orthogonal to chirality}\;}\tag{R12.12}$$

(F51, 5/5 checks PASS, exact/machine $\le1.8\times10^{-15}$.) These four properties are exactly the
defining relations of the hypercharge factor $U(1)_Y$ inside $SU(2)\times U(1)_Y$: property (3) by
Schur's lemma means $U_Y(\theta)$ can only assign each spin/isospin multiplet a phase, never rotate
states into one another, precisely as a factor commuting with — never mixing into — $SU(2)_L$ must.
The sharper claim is uniqueness: because the minimal BCC cell has internal dimension $s=2$, entirely
consumed by the spin $SU(2)$ (its generators span every traceless Hermitian operator on
$\mathbb C^2$), **the only non-trivial abelian charge available without enlarging the cell is a
property of the walk's graph — the bipartite sublattice parity.** F51 does not re-derive the
hypercharge *values* (F38's job, §12.2.14) or the coupling *ratio* (F49/F138/F141/F320's job,
§12.2.15 onward); it derives *where* the abelian factor structurally has to live, closing exactly
the gap F49 itself named as its central unresolved point.

#### 12.2.13 The hypercharge-attribution correction: F279 supersedes F165 (S13)

An earlier finding, **F165** (2026-06-29, not itself a Chapter 12 assigned finding and now
partially superseded), concluded that the five generation hypercharges are forced up to one overall
normalisation by three anomaly rows plus two chiral-mass-step rows — with the gravitational anomaly
$[\text{grav}]^2\cdot U(1)_Y$ counted as one of the five independent constraints. **F279**
(2026-08-02) re-derives the same system from scratch, independently of F165's own script, and finds
F165's *conclusion* correct but *two of its steps* wrong. `docs/theory/supersessions.yaml`
record **S13-F279-hypercharge-attribution** records this precisely: `by: [F279]`,
`superseded: [F165]`, and — the load-bearing detail — `retained: EVERYTHING F165 CONCLUDES`. This
is *not* a case where the physics moved; it is a corrected attribution of *why* the physics holds,
recorded with S13's own `sub_claim_superseded`-style framing (two specific claims replaced, the
conclusion untouched), and this chapter presents only the corrected account per the assignment's
explicit instruction.

**What was wrong.** F165's system omitted the right-handed neutrino $\nu_R$ from the gravitational
trace. Once $\nu_R$ is carried as a field with its own hypercharge $y_\nu$ and its own mass-step row
(the conjugate phase $y_\nu=y_L+y_\phi$, exactly as the model's own `hypercharge.py` module encodes
it), the gravitational row $\sum_i n_iY_i=0$ is **identically satisfied by the other five
constraints already** — the rank is 5 with or without it, and the remaining system on the anomaly
rows plus the three mass-step rows alone is **two-dimensional**, not one: $y_Q,\,y_\phi$ both free.
F165 reached its one-dimensional result only by leaving $\nu_R$ out of the gravitational trace —
numerically identical to imposing $y_\nu=0$ without stating that step. Separately, F165 §3's claim
that removing colour ($N_c=1$) breaks the closure is also false: the system closes to a one-dimensional
line for **every** $N_c$, with ratios $1:(1+N_c):(1-N_c):-N_c:-2N_c$, verified at $N_c=1,\ldots,5$
and symbolically.

**What actually closes the system.** F47's Higgs-free see-saw (Chapter 16's territory, forward-cited
here) requires the right-handed neutrino to carry a **Majorana** mass term $\nu_R^\mathsf{T}C\nu_R$.
That bilinear carries hypercharge $2y_\nu$, so gauge invariance of the term forces
$2y_\nu=0\Leftrightarrow y_\nu=0$ exactly, with no normalisation freedom — a Majorana mass is only
available to a field of exactly zero hypercharge:

$$\boxed{\;\text{the closing constraint for hypercharge quantisation is }2y_\nu=0\text{ (F47's Majorana step), not the gravitational anomaly}\;}\tag{R12.13}$$

(F279, 5/5 checks PASS, exact over $\mathbb Q$ — literal integer zero, not float.) Adding this row
restores F165's result exactly: six constraints in seven unknowns, rank 6, nullspace dimension 1,
the identical ratios $y_Q:y_u:y_d:y_L:y_e:y_\nu=1:4:-2:-3:-6:0$, with $y_\phi=3y_Q$ and — as a
consequence, not an independent constraint — **both** the gravitational and cubic $U(1)_Y^3$
anomalies vanish identically on that line. F279's own text frames why the corrected route is
stronger, not merely different: F165's original version was a lattice realisation of a known
Standard-Model theorem (anomaly freedom plus one Yukawa per charged sector quantises hypercharge);
the corrected version instead leans on something the Standard Model does *not* have — a Higgs-free
Majorana step this model's own construction (F27/F41/F47) already required for the neutrino
see-saw — so the quantisation now follows from the model's *own distinguishing structure*, not an
imported theorem. F279 also corrects F165's colour claim precisely: charge **quantisation** (that
lepton charges are integers and quark charges are rationals of the same unit) is derived for every
$N_c$; the specific fractions $\tfrac23,-\tfrac13$ additionally require $N_c=3$, which remains an
external input (Chapter 13's "why three colours" question, graded `ABSENT` in the project's own
completeness audit).

> **Forward citation, not a derivation here.** F279's closing constraint is the Majorana mass step,
> which belongs structurally to Chapter 16 (Neutrinos, F47 assigned there). This chapter states the
> correction precisely and uses its *result* — hypercharge quantisation to one overall normalisation,
> now correctly attributed — without re-deriving the Majorana construction itself; Chapter 16 is
> where F47 is built in full.

### Group C — anomaly cancellation and mass generation

#### 12.2.14 First-generation anomaly cancellation: all six traces exactly zero (F38)

F27 (Chapter 11) explicitly flagged "anomaly cancellation... not tested." F38 (2026-05-26) discharges
that flag directly, over $\mathbb Q$ rather than to floating-point tolerance — every trace below is
computed with Python's `fractions.Fraction` end to end, so the residuals reported are literal
integers, not floats indistinguishable from zero:

| Trace | Statement | Result |
|---|---|---|
| $[\text{grav}]^2\cdot U(1)_Y$ | $\sum_in_iY_i$ | $-2+2+2-4+2=0$ |
| $U(1)_Y^3$ | $\sum_in_iY_i^3$ | $-2+8+\tfrac{6-192+24}{27}=0$ |
| $[SU(2)_L]^2\cdot U(1)_Y$ | doublets only | $-\tfrac12+\tfrac12=0$ |
| $[SU(3)_c]^2\cdot U(1)_Y$ | triplets only | $\tfrac13-\tfrac23+\tfrac13=0$ |
| $[SU(3)_c]^3$ | pure colour cubic | $2-1-1=0$ |
| $[SU(2)_L]^3$ | pseudo-real, $A(R)\equiv0$ | $0$ identically |

$$\boxed{\;\text{all six anomaly traces vanish exactly over }\mathbb Q\text{, promoting the completeness-review "anomaly cancellation" row from ❌ to ✅}\;}\tag{R12.14}$$

(F38, exact-rational, six independent checks, all $0$.) This is a property of the charge assignments
alone — a statement that both the SM continuum theory and this lattice model inherit the moment they
adopt the same generation content — and it is what proves the charge bookkeeping Group B and Group D
depend on has not silently been broken anywhere in this model. F38's own §6 states clearly what is
*not* closed here: antiparticle/$C$/$CP$ structure per species (later closed as F53, not a Chapter 12
finding) and the quark sector's electroweak wiring (closed by F40, Chapter 11, and completed here by
F42/§12.2.11).

#### 12.2.15 $m_A=0$ from the rank-deficient Stueckelberg mass matrix (F44)

F44 (2026-05-27) resolves an open item from Ludwig's own notebook: the notebook's diagonal-mass
parameterisation $\tfrac12m_W^2W_3^2+\tfrac12m_{W_0}^2W_0^2$ produces, after Weinberg rotation, a
residual "anomalous" cross term $\propto(m_W^2-m_{W_0}^2)\sin\theta_W\cos\theta_W\,A_\mu Z^\mu$ that
the notebook flags but never resolves, imposing $m_A=0$ by hand to recover the SM relation. F44
shows that in the **actual** F34b+F41 construction — a single Stueckelberg field
$U(x)\in SU(2)_L\times U(1)_Y$ inside one covariant derivative — this never arises: the $(W^3,B)$
mass block factorises as an exact outer product,

$$M^2_{(W^3,B)}=f^2\begin{pmatrix}g\\-g'\end{pmatrix}\begin{pmatrix}g&-g'\end{pmatrix},$$

$$\boxed{\;\det M^2_{(W^3,B)}=f^2(g^2g'^2-(gg')^2)=0\text{ identically — rank 1, zero eigenvalue = photon, non-zero eigenvalue }m_Z^2=f^2(g^2+g'^2)\;}\tag{R12.15}$$

(F44, 5/5 checks PASS, machine $\le2.19\times10^{-16}$; lattice-level rank-1 verification $1.13\times
10^{-11}$.) The photon eigenvector is $(g',g)/\sqrt{g^2+g'^2}=(\sin\theta_W,\cos\theta_W)$ — exactly
F35's own Weinberg rotation (§12.2.7). $m_A=0$ is therefore **automatic**, not a separately imposed
condition, and the notebook's "anomalous" cross term is simply the off-diagonal of $M^2$ before
diagonalisation, absorbed exactly by the rotation that already makes F35's $m_Z/m_W=1/\cos\theta_W$
algebraic. This single-field construction is the *only* real-mass realisation available — the
notebook's implicit two-field theory would need $m_{W_0}^2/m_W^2=-\tan^2\theta_W$, impossible for
real masses — and F44's rank-1 result is what F320's absolute-mass capstone (§12.2.24) later shows
extends, unmodified, to $\rho=1$: the same determinant vanishes identically in the stiffness quantum
$u$, not at a tuned point.

#### 12.2.16 The diamagnetic contact is charge-blind: the electroweak channel splitting is purely paramagnetic (F153)

F153 (2026-06-12) is the last of the three "structural obstruction" findings this chapter groups
with the mass-generation cluster because its result is about the *mechanism* of channel splitting,
not primarily about the Weinberg-angle value itself (its direct target is F149's route-adjudication
puzzle, engaged in full at §12.2.22–12.2.23). The result relevant to this section: for a gauge field
coupled by Peierls substitution to the fermion sea, the $O(\varepsilon^2)$ diamagnetic (seagull)
contact term is **identical** in the vector ($SU(2)_L$) and staggered (hypercharge) channels:

$$\boxed{\;\chi_\text{stag}-\chi_\text{vec}=(\chi_\text{stag}-\chi_\text{vec})_\text{paramagnetic}\text{ exactly (residual }1.1\times10^{-10}\text{) — the seagull term drops out of the channel difference}\;}\tag{R12.16}$$

(F153, 5/5 checks PASS, exact $1.1\times10^{-10}$ for the charge-blindness itself.) The mechanism is
that the per-tick contact carries the parity charge squared ($P^2=1$, hence charge-blind) and the
cross term's two sign sources ($-P$ on the second tick and $V_4(\cdot+Q)=-V_4$, since $e^{i\mathbf
d\cdot\mathbf Q}=-1$ for every odd body-diagonal hop) cancel exactly. This is a genuine structural
gain — it resolves an apparent sign contradiction between two earlier numerical measurements (F149's
N6 and N7, which had disagreed in sign because the contact term dominates each channel's *absolute*
value while the *difference*, which is all either measurement was actually sensitive to, is a clean
paramagnetic object) — and it means any future attempt to compute the free-fermion contribution to
the electroweak channel splitting can restrict attention entirely to the paramagnetic (current-current)
piece. F153's further, decisive negative results about what this does and does not deliver for the
Weinberg-angle counting are carried in full at §12.2.22–12.2.23, alongside F143 and F147.

### Group D — the Weinberg angle, derived by three convergent routes

#### 12.2.17 The internal derivation: $\sigma\leftrightarrow\tau$ swap geometry gives $\sin^2\theta_W=\tfrac14$ (F45)

F45 (2026-05-27) is the first attempt in this chapter's history to derive $\theta_W$ rather than
consume it as an input. Every BCC site carries a Weyl spinor with both a spin index (σ-space,
$\mathbb C^2_\sigma$) and a weak-isospin index (τ-space, $\mathbb C^2_\tau$); the notebook's own
observation ("$A_\mu$ works on the isospin vector just like $W$ works on the spin vector," p.67/71)
is formalized as the involution $\Pi:A\otimes B\mapsto B\otimes A$, which decomposes the 4D doublet
space into a 3D swap-**triplet** ($\Pi=+1$, identified with the three $SU(2)_L$ generators) and a
1D swap-**singlet** ($\Pi=-1$, the $U(1)_Y$ Cartan direction). Assigning **equal bare lattice
strength per generator direction** — the natural swap-symmetric normalisation, with no empirical
input — gives:

$$\boxed{\;\frac{g'^2}{g^2}=\frac{1}{3}\quad\Longleftrightarrow\quad\sin^2\theta_W=\frac14,\ \cos^2\theta_W=\frac34,\ \frac{m_Z}{m_W}=\frac2{\sqrt3}\;}\tag{R12.17}$$

(F45, algebraic prediction, `fractions`-exact.) An independent cross-check using Casimirs — $C_2(SU(2)_L)
=T(T+1)=\tfrac34$ on the L-doublet against $C_2(U(1)_Y)=(Y_L/2)^2=\tfrac14$ — reproduces the identical
ratio $\tfrac13$, confirming the 1:3 split is geometric, not normalisation-dependent. Against PDG,
$\sin^2\theta_W=\tfrac14$ is $+12.0\%$ high; $m_Z/m_W=2/\sqrt3=1.1547$ is $+1.77\%$ high with **zero
fit parameters** — closer, at the tree level, than the canonical $SU(5)$ GUT prediction $\tfrac38$
($+68\%$), and it is precisely this tree value that Groups D's later findings (F138, F231) show is
not the final story but rather the UV endpoint of a chain that does close to $<0.3\%$.

#### 12.2.18 The external derivation: BCC bond/sublattice counting gives $\sin^2\theta_W=\tfrac29$ (F49)

F49 (2026-05-28), the same day as F44, poses a structurally different counting. The BCC lattice has
$8$ nearest-neighbour bonds ($4$ unique body-diagonal axes) and $6$ next-nearest bonds ($3$ unique
face axes), for $14$ total bonds / $7$ unique axes to second shell, plus $2$ interpenetrating cubic
sublattices (the bipartite structure F51 later derives is the unique hypercharge carrier).
**Assigning** $SU(2)_L$ one generator per bond axis (weight 7) and $U(1)_Y$ one generator per
sublattice (weight 2) gives:

$$\boxed{\;\frac{g'^2}{g^2}=\frac{n_\text{sublattice}}{n_\text{bond axis}}=\frac27\quad\Longleftrightarrow\quad\sin^2\theta_W=\frac29=0.2222\overline2\;}\tag{R12.18}$$

(F49, exact rational, matched by direct numerical verification against `casim.engine.lattice.bcc`
that the leading-order group velocity $c_\text{lat}$ is identical across all 7 axes when both
chirality branches are summed.) This matches the notebook's own p.104 numerology ("$W^\pm=3e$
exactly" $\Rightarrow\sin^2\theta_W=2/9$) exactly, and lands $-0.44\%$ from the PDG on-shell value —
an order of magnitude closer than F45's tree value. F49's own text is unambiguous that this is a
**partial** derivation: "the assignment itself is not yet derived" — specifically, why $U(1)_Y$ is
the sublattice-staggered $U(1)$ (closed by F51, §12.2.12) and why $SU(2)_L$ is spread uniformly
across all 7 axes rather than, say, only the 4 body-diagonal ones (which would give $\sin^2\theta_W
=\tfrac13$, far off). F49 itself frames F45 and its own counting as complementary rather than
contradictory — "F45 counts internal ($\sigma\otimes\tau$) representation dimensions; F49 counts
external (BCC lattice) structural multiplicities" — a framing Groups D's remaining findings sharpen
into an exact reconciliation.

#### 12.2.19 Closing the gap: $\sin^2\theta_W=\tfrac14$ is the compositeness-scale matching condition, forced by hypercharge having no lattice kinetic term (F138)

F138 (2026-06-11) supplies the mechanism that turns F45's $+12\%$ "bare lattice value" framing into
a precisely-scaled prediction. The premise is F41 itself (§12.2.10): $U(1)_Y$ is not an independent
lattice gauge field — it rides on $U(x)$ as a Stueckelberg phase, with **no independent kinetic
term** at the lattice level, i.e. a formally infinite bare abelian coupling. In any embedding where
the physical hypercharge mixes a non-abelian Cartan direction (F45's swap-singlet, embedding ratio
$g_X^2/g_L^2=1/3$) with an external abelian factor $g_X$, the exact 331-type relation
$\sin^2\theta_W=t^2/(1+4t^2)$, $t^2=g_X^2/g_L^2$, forces $\sin^2\theta_W<\tfrac14$ for any finite
$g_X$ and $\sin^2\theta_W\to\tfrac14$ **exactly as $g_X\to\infty$** — precisely F41's structural
starting point, not a pathology to evade:

$$\boxed{\;\sin^2\theta_W=\tfrac14\text{ holds exactly at the scale }\mu_\star\text{ where the induced }Y\text{ kinetic term turns on; running below it applies as usual}\;}\tag{R12.19}$$

(F138, WM1, exact algebra.) The scale is identified by NDA at $\mu_\star=4\pi v=3.094$ TeV, the
generic scale at which a strongly-coupled Higgs-free EWSB sector (F27/F41/F118) resolves. Anchoring
$\sin^2\theta_W(\mu_\star)=\tfrac14$ exactly and running with the model's own (Higgs-free) one-loop
$\beta$-coefficients ($b_1=4$, $b_2=-\tfrac{10}3$, vs. the SM's $b_1=\tfrac{41}{10}$,
$b_2=-\tfrac{19}6$) gives:

$$\boxed{\;\sin^2\bar\theta_W(M_Z)=0.23173\text{ (Higgs-free)},\ 0.23210\text{ (SM }b_i\text{) vs. PDG MS-bar }0.23122\text{: residual }+0.22\%,\ +0.38\%\;}\tag{R12.20}$$

(F138, WM2, numeric, decisive.) This reduces the bare $+8.12\%$ MS-bar gap (equivalently F45's
$+12.0\%$ on-shell framing) by roughly $40\times$, using only $\alpha_\text{em}(M_Z)$ and $v$
(already an external ruler, per §12.1) — no new knob. The measured trajectory crosses $\tfrac14$ at
$\mu_\times=3.42$ TeV; $\ln(\mu_\times/4\pi v)=0.099$, a $\sim10\%$ scale agreement comfortably
within one-loop truncation and NDA's $O(1)$ ambiguity, and this residual is exactly what F143 later
bounds (§12.2.22). F138 also reframes F49's $\tfrac29$: since $\tfrac29\cdot(4/1)=8/9$ is an exact
bridge from $\tfrac14$, F49's value is reinterpreted (and eventually confirmed, F231) as an
**on-shell endpoint**, not a competing tree value.

#### 12.2.20 The reconciliation: $\sin^2\theta_W=\tfrac29$ is the on-shell face of $\tfrac14$, not a rival value (F231)

F231 (2026-07-02) closes the question F138 §5 posed but left open — is the $8/9=(2/9)/(1/4)$ bridge
an accident, or does it decompose into physics? $\tfrac29$ is, algebraically, a mass-ratio
statement: $\sin^2\theta_W^\text{os}\equiv1-m_W^2/m_Z^2=\tfrac29\Leftrightarrow m_Z/m_W=3/\sqrt7$
(against PDG: $-0.44\%$/$-0.064\%$ respectively) — a statement about physical masses in the
**on-shell scheme at $M_Z$**, whereas F138's $\tfrac14$ is the **MS-bar** angle at the **UV scale**
$4\pi v$. The $8/9$ bridge factorises cleanly into exactly the two steps that separate these:

$$\boxed{\;\frac{2/9}{1/4}=\underbrace{\frac{0.23173}{0.25}}_{\text{one-loop running }=\,0.9269}\times\underbrace{\frac{0.223209}{0.23122}}_{\text{MS-bar}\to\text{on-shell }=\,0.9654}=0.8948\ \text{vs. }\tfrac89=0.8889:\ \text{residual }0.67\%\;}\tag{R12.21}$$

(F231, W1–W4, 5/5 checks PASS, quantitative/reconciliation.) Propagating the chain end to end —
$\tfrac14\xrightarrow{4\pi v\to M_Z\text{ run}}0.23173\xrightarrow{\text{scheme}}0.22370$ vs.
$\tfrac29=0.22222$ — lands at the identical $0.66\%$ residual. The reconciled statement: **$\tfrac14$
and $\tfrac29$ are one angle, two faces**, joined by one-loop running $\times$ scheme conversion, not
two independent geometric coincidences and not a genuine rival pair. F231's own honest scoping is
precise on what this does and does not settle: F49's BCC counting reproduces the on-shell endpoint
*structurally* (its assignment, per §12.2.18, still underived), so $\tfrac29$'s status moves from
"competing value" to "on-shell face, matched to $0.67\%$" — a structural match sharpened to a
falsifiable target (F49 must reproduce the on-shell scheme, $3/\sqrt7$, not the MS-bar one), not yet
a second independent rigorous derivation.

#### 12.2.21 The Wigner–Seitz lemma: 7 is exact, and $2:7$ is mass counting, $m_W^2:m_Z^2=7:9$ (F141)

F141 (2026-06-11, same day as F138) closes the geometric half of what remained open after F51 and
F138: why does F49's counting stop at "second shell," and how does a coupling-ratio counting become
consistent with F231's later requirement that $\tfrac29$ be an on-shell (mass), not MS-bar
(coupling), statement? First, an exact geometric lemma, proved by an integer relevance criterion and
a covering-radius bound (verified to $\mathbb Z$/$\mathbb Q$ exactness, not a truncation choice):

$$\boxed{\;\text{the BCC Wigner–Seitz cell (truncated octahedron) has exactly }14\text{ facets}=8\text{ hexagonal (⊥ body diagonals)}+6\text{ square (⊥ face axes)}\Rightarrow7\text{ facet axes mod inversion, and nothing beyond the second shell can ever be relevant (covering-radius }4\mu^2=5<8\text{, the next shell)}\;}\tag{R12.22}$$

(F141, V1–V2, 11/11 checks PASS, exact over $\mathbb Z$/$\mathbb Q$.) F49's "7" is therefore the
*complete* facet-axis count of BCC's own Voronoi cell, not an arbitrary shell truncation. Second, an
**equal-stiffness channel hypothesis (U)**: the EWSB condensate contributes one universal stiffness
quantum $u$ per structural channel — one per WS facet axis (7, charged/bond sector) and one per
sublattice (2, F51's abelian sector) — giving $g^2=7u$, $g'^2=2u$ and, exactly over $\mathbb Q$:

$$\boxed{\;\frac{m_W^2}{m_Z^2}=\frac{g^2}{g^2+g'^2}=\frac79,\qquad\frac{m_Z}{m_W}=\frac3{\sqrt7},\qquad\sin^2\theta_W^\text{os}=\frac29\;}\tag{R12.23}$$

(F141, V3–V4, exact/numeric; residual vs. PDG $m_Z/m_W$: $-0.063\%$.) This is scheme-correct under
F231 by construction — masses, not running couplings, define the on-shell angle — and sharper than
F49's original coupling-ratio framing, because equal stiffness *at the condensate scale* is the only
requirement (RG running above/below is irrelevant to a mass ratio). F141's own text is unambiguous
that hypothesis (U) is a **programme, not a result**: it decomposes into (U1) equality across the 7
axis channels *at the condensate level* (only the free-dispersion precondition is established), (U2)
equality between the axis-channel quantum and the sublattice-channel quantum (the cross-normalisation
between non-abelian and abelian sectors — historically where such counting arguments fail), and (U3)
explicit quadratic-form assembly. F141 names the concrete next step (an induced-stiffness lattice
loop) that — if it closes — would simultaneously fix F138's NDA-based $\mu_\star$ and F141's (U2).
Two independent findings (§12.2.22–12.2.23) go looking for exactly that number.

#### 12.2.22 Two no-go results: the free fermion sea cannot supply the required stiffness (F143, F147)

F143 (2026-06-12) computes F141's named lattice loop on the **wrap route** — gauging $Y$ through the
F42 Stueckelberg sandwich on $U(x)$ — and finds a decisive structural obstruction. The model's own
gauging convention makes the kinetic-sector coupling a **unitary conjugation**
$W_\alpha=e^{i\alpha(x)Y/2}W(\mathbf k)e^{-i\alpha(x)Y/2}$ for any static $\alpha(x)$: the sea
spectrum is exactly invariant, so the kinetic-sector fermion loop induces **zero** abelian
field-strength stiffness identically, at all orders, all scales:

$$\boxed{\;\text{transverse (field-strength) channel: exactly zero induced stiffness, all orders (}1.3\times10^{-15}\text{); longitudinal (Goldstone) channel: }\hat f\in[0.17,0.38]\text{, no large-log enhancement}\;}\tag{R12.24}$$

(F143, 5/5 checks PASS, exact/machine.) The only non-conjugate wrap entry is the mass step itself, so
any induced wrap stiffness is structurally tied to chiral-mass generation — deriving, not assuming,
F138's premise that the matching sits at the EWSB scale. The longitudinal loop is computed both by
exact supercell diagonalisation and by second-order eigenvalue perturbation theory (agreeing to
$5.8\times10^{-4}$), giving a small **lattice contact term** with no continuum-style
Pagels–Stokar log enhancement — the fermion sea's share of $v^2$ is bounded at $0.16$–$0.36\%$,
shifting $\mu_\star$ by at most $0.08$–$0.18\%$, an order of magnitude below F138's own NDA offset.

F147 (2026-06-12, concurrent with F143) takes the complementary **walk route** — gauging the fermion
walk itself by Peierls substitution — and reaches the same conclusion by an independent mechanism, an
exact **gauge-rigidity theorem**: the half-filled one-tick sea has exactly zero static response to
any plane-wave gauge field in *either* channel (vector or staggered), to $10^{-12}$ at field
strengths up to $\varepsilon=0.3$, via a spectral closure under $\theta\to\theta+\pi$ and
$\theta\to\pi-\theta$ that holds for **any** gauge field because Peierls phases cannot break
bipartiteness:

$$\boxed{\;\text{one-tick gauge rigidity: zero induced stiffness, every channel, exact — the gauge stiffness cannot come from the free fermion sector, two-route convergent (F143 wrap + F147 walk)}\;}\tag{R12.25}$$

(F147, 10/10 checks PASS, exact/machine $\le10^{-12}$.) In the physical **stroboscopic** (two-tick)
sea, F147 proves a second, more targeted result directly relevant to F141's hypothesis (U2): the
staggered (hypercharge) and vector bubbles are **pointwise identical** ($|M_\text{stag}|=|M_\text{vec}|$
at every $\mathbf q$, residual $10^{-14}$; full brute-force response channel-equal to $10^{-12}$–$7
\times10^{-8}$) — the stroboscopic staggering momentum $\mathbf Q$ is an exact symmetry of the
response. This settles the **dynamical half** of F141's (U2) at the free-fermion level: per-unit-
charge quanta are exactly equal, ratio 1. But applying the equal per-charge quanta to the bare walk
charges gives $\sin^2\theta_W^\text{free}=\tfrac15$, not $\tfrac29$ — the exact factor $8/7$ that
separates F49's target ratio $2/7$ from the free-sea value $1/4$ is localized, not explained, by this
result: it must come from **charge content and channel multiplicity** (F38's hypercharge spectrum
layered on F51's carrier, and/or F141's WS-cell counting), not from loop dynamics, which F147 shows
is fixed at ratio 1.

$$\boxed{\;\text{free-sea bookkeeping: }t^2=\tfrac14,\ \sin^2\theta_W^\text{free}=\tfrac15\text{ — the F49 gap reduced to the exact factor }8/7\;}\tag{R12.26}$$

#### 12.2.23 The bookkeeping factor stays unresolved at the perturbative level; the physical condensate is $O(1)$ (F153, continued)

F153 (already introduced structurally at §12.2.16) directly tests F141's two live routes to the
residual $8/7$ factor — (b) a condensate splitting function $R(m)$ with $t^2=\tfrac14R$, and
(a) the geometric $8$-hop-to-$7$-axis multiplicity — using the charge-blind diamagnetic term of
R12.16 to isolate the genuinely channel-distinguishing (paramagnetic) piece. Both routes come back
negative at the free-Dirac-proxy level, and the reason why is itself a structural result:

- **Route (b) fails.** A clean isotropic small-$\tilde q$ ratio $R(m)$ is not extractable in the
  two-tick sea at any reachable lattice size — the gapless cones and the second Fermi boundary at
  $\Omega=\pm\pi$ contaminate every extraction route tried, and the one sign-stable signal that does
  survive ($\chi_\text{vec}/\chi_\text{stag}<1$, monotone decreasing in $m$) points **away** from the
  needed $R=8/7$, not toward it.
- **Route (a) is partially answered but does not deliver a clean count.** The vector-stiffness
  channel matrix is not diagonal in the hop basis nor the antipodal-axis basis; the WS face-axis
  channels (F141) *do* appear in the bilinear, but organize into 4 anisotropic pairs set by the
  gauge-momentum direction, not a flat $7$- or $8$-fold degeneracy.
- **The deeper reason, Result D.** Matching the proxy Dirac mass to the actual F118 lepton
  condensate ($e=\|y-\bar y\|=0.728$, all completion couplings $O(1)$) shows the physical condensate
  sits at **$O(1)$ coupling** — the F150 saturated regime — not the small-$m$ region where any
  perturbative $R(m)$ expansion is valid at all:

$$\boxed{\;\text{the physical EWSB condensate coupling is }O(1)\text{: a small-}m\text{ perturbative proxy was never the right tool, and the on-shell }\sin^2\theta_W=\tfrac29\text{ stands as exact algebra (F141) independent of any }R(m)\;}\tag{R12.27}$$

(F153, 5/5 checks PASS, exact/numeric/structural.) The net effect of F143, F147 and F153 together is
to **redirect**, not weaken, the remaining programme: all three independently point to the same
conclusion — the $8/7$ bookkeeping factor, and with it the full closure of F141's hypothesis (U),
must come from a non-perturbative computation in the saturated $E_g$/EWSB condensate sector (F118,
F150), not from any free-fermion loop, perturbative or otherwise. The on-shell $\tfrac29$ prediction
itself is untouched by any of this — it never depended on the loop calculations that were attempted
and found wanting.

### Group F — end-to-end integration and the absolute masses

#### 12.2.24 The capstone: absolute $m_W$, $m_Z$ predicted from two inputs, and $\rho=1$ from rank (F320)

F320 (2026-08-16) is this chapter's headline result. It starts from an accounting correction: the
project's own completeness ledger (row B12) and a withdrawn claim card (`CL016`) had read "$v$ is an
input" as implying "$m_W$ is not predicted" — true premise, non-sequitur conclusion. The relevant
comparison is the **input count**:

| | electroweak inputs | outputs |
|---|---|---|
| Standard Model | $\{\alpha,\ G_F,\ m_Z\}$ — three | $m_W$, $\sin^2\theta_W$ |
| this model | $\{\alpha,\ G_F\}$ — **two** | $m_W$, $m_Z$, $\sin^2\theta_W$ |

The Standard Model must be *handed* a boson mass before it can produce the other one; this model is
not, because $\sin^2\theta_W^\text{os}=\tfrac29$ already comes from lattice geometry (F49, made
complete by F51 and F141). Three genuinely new results fall out of drawing the accounting boundary
correctly.

**First, F141's free stiffness quantum $u$ is determined, not merely constrained.** Electric charge
is not independent in this scheme; it is the unbroken combination $e=g\sin\theta_W$, equivalently
$e^2=g^2g'^2/(g^2+g'^2)$. With $g^2=7u$, $g'^2=2u$ from F141 (R12.23), this closes $u$ exactly:

$$\boxed{\;u=\frac{9e^2}{14}=\frac{18\pi\alpha}7\quad\Longrightarrow\quad g^2=18\pi\alpha,\quad g'^2=\frac{36\pi\alpha}7\;}\tag{R12.28}$$

(F320, V2a–c, exact, $<10^{-12}$/$1.4\times10^{-14}$.) With $m_W=gv/2$, $m_Z=\sqrt{g^2+g'^2}\,v/2$:

$$\boxed{\;m_W=\frac{3v}2\sqrt{2\pi\alpha},\qquad m_Z=\frac{9v}2\sqrt{\frac{2\pi\alpha}7}\;}\tag{R12.29}$$

Both closed forms are new to the tree at F320's writing, and both are exact rational multiples of
$\pi\alpha$ under the coefficients $\tfrac32$, $\tfrac92$ and the radical $\sqrt7$ — all three of
which are BCC facet and sublattice counts and nothing else. F320's own text is explicit that this
step **inherits, and does not resolve**, the open status of F141's hypothesis (U) — see §12.1 item
4 and §12.2.26 below.

**Second, $\rho=1$ follows exactly from the *rank* of the Higgs-free breaking, not from custodial
$SU(2)$.** This model has no Higgs field (Chapter 11), so it cannot use the standard tree-level
argument (the custodial $SU(2)$ of a Higgs doublet). F41 absorbs exactly **one** Stueckelberg
direction on $U(x)$ — the single combination $\Delta Y=Y_L-Y_R$ — so the condensate's quadratic
form is the outer product of one covector with itself, $M^2=\tfrac{v^2}4ww^\top$, $w=(g,-g')$,
exactly the F44 rank-1 structure of §12.2.15 generalized to arbitrary $u$:

$$\boxed{\;\det M^2=\Big(\frac{v^2}4\Big)^2(g^2g'^2-(gg')^2)=\Big(\frac{v^2}4\Big)^2(14u^2-14u^2)=0\text{ identically, for every }u\quad\Longrightarrow\quad\rho\equiv\frac{m_W^2}{m_Z^2\cos^2\theta_W}=\frac{7u}{9u\cdot(7/9)}=1\text{ exactly}\;}\tag{R12.30}$$

(F320, V1a–d, exact over $\mathbb Q$ at five independent rational $u$.) The control
`rank_two_breaking=true` (an independent second condensate direction) is what confirms this is a
genuine measurement, not a restatement: it turns V1a–c red and *nothing else*, cleanly separating
"rank owns $\rho$" from "counting owns the ratio."

**Third, and the load-bearing leg: the absolute-mass residual equals the on-shell-angle residual,
independent of any radiative correction.** The on-shell relation $m_W^2\sin^2\theta_W=\pi\alpha/
(\sqrt2\,G_F(1-\Delta r))$ carries a radiative correction $\Delta r$ this model does not compute —
the obvious objection to any absolute-mass claim. It does not survive taking a ratio: the model and
the Standard Model sit on the *same* relation with the *same* $\Delta r$, so

$$\boxed{\;\frac{m_W^\text{model}}{m_W^\text{obs}}=\sqrt{\frac{\sin^2\theta_W^\text{obs}}{2/9}}\text{ exactly, for every }\Delta r\text{ (verified constant to }2.2\times10^{-16}\text{ over }\Delta r\in[0,0.10]\text{, 41 points)}\;}\tag{R12.31}$$

(F320, V4a, machine $2.2\times10^{-16}$.) The absolute-mass prediction therefore inherits the
accuracy of the on-shell angle (F231's $-0.44\%$) and adds no freedom of its own — nothing about the
absolute masses is a fit, because the only thing that could have been fitted cancels identically.

#### 12.2.25 β-decay: the charged current runs end-to-end (F54)

F54 (2026-05-29) is this chapter's structural integration test, wiring together every piece built
above — the left-handed $SU(2)_L$ doublet bilinears (F29), the covariant Dirac doublet's maximal
parity violation (F34), the $W$-coupled quark doublet (Chapter 11's F40, extended here), dynamical
and Proca-mass $W$ propagation (F36), and the per-species electroweak charge registry (F35/F48) —
into the signature first-generation weak process $d\to u+W^-\to u+e^-+\bar\nu_e$. The new charged-
current raising/lowering structure ($T^\pm$, $W^\pm$, $J^\pm$) is the one missing primitive:

$$\boxed{\;\Delta E(W^-)=\frac g{\sqrt2}\big(J^1+iJ^2\big)\Delta t=\frac g{\sqrt2}J^+_\text{quark}\Delta t,\quad J^+_\text{quark}(x)=u_L^*(x)d_L(x)\text{, residual }9.2\times10^{-16}\;}\tag{R12.32}$$

(F54, 10/10 checks PASS, 7 exact/exact-$\mathbb Q$, 3 machine $\le3.1\times10^{-13}$.) The $d\to u$
vertex emerges directly from the existing $W$-sourcing machinery (F36's back-reaction, §12.2.8) once
the charged combination $W^-=(W^1+iW^2)/\sqrt2$ is formed — no new dynamics. Maximal parity
violation is exact (the $V-A$ projector $P_L$ annihilates a right-handed spinor bit-for-bit, matching
F34's $\chi$-decoupling, R12.5); charge, baryon and lepton number are conserved exactly over
$\mathbb Q$ at both vertices and for the full process, including $B-L$; and the heavy-$W$ Fermi
limit is reproduced exactly at $q^2=0$, $G_F/\sqrt2=g^2/8m_W^2$, with the leading correction
$-q^2/m_W^2$ — the textbook propagator expansion, with no fit parameters. An end-to-end pipeline
run (CC10) confirms the whole chain is one dynamical, causal object: a localized quark current
sources a $W^-$ field that propagates (Proca, R12.8) to a distant site and drives the leptonic
charged current there, with global charge conservation holding exactly throughout. F54's own
"Bottom line" states plainly that this closes the last of the first-generation Tier-A structural
tests — what remains is Tier-B calibration (SI units, Chapter 17's territory), not structure.

### 12.2.26 A genuine architectural tension, flagged rather than resolved

> **Gap [G-7]:** Chapter 8's own text (§8.2.2, R8.3) states that "Chapters 12–13's $W$/$Z$/gluon
> sector can keep the chirally-faithful propagation law without contradicting anything derived
> here" — i.e. the expectation, written before this chapter's own source material was read in full,
> is that the $W^\pm$ boson in Chapters 12/13 rides the **chiral** channel $\Omega^\pm(\mathbf k)=
> 2\omega^\pm(\mathbf k/2)$, forced by its coupling's pure left-projector structure ($\|P_L\psi_R\|=0$
> exactly, F91). Reading this chapter's actual primary source for the $W$ field's free propagation
> law — F32 (2026-05-24, Phase 2 of the $W_\mu$ roadmap, eleven days before F91 is derived) — finds
> the opposite: F32 explicitly **rejects** the chiral dispersion for the classical $W$ field, on
> direct physical grounds (a real-valued field cannot remain Hermitian-symmetric under it — measured
> as IFFT imaginary parts up to $\sim0.8$ and $\sim56\%$ energy drift over 200 ticks), and adopts
> instead the **even** law $\Omega_\text{even}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$
> — the identical dispersion Chapter 8 uses for the photon. Every subsequent finding in this
> chapter's Group A (F33, F34, F34b, F36, F48) builds on F32's even-dispersion choice without
> revisiting it; none of them, nor any finding in Chapter 8 or Chapter 9, cites F32's specific
> physical argument or engages with the apparent conflict against R8.3's later forcing theorem. The
> two results may ultimately concern different objects — R8.3's classification is (per Chapter 8's
> own framing, R8.15/F89) fundamentally about the propagation law a *composite bilinear of two
> Weyl constituents* inherits from its branch-coupling structure (mirroring how the photon of
> Chapter 8 *is* literally a bound Weyl pair), whereas the $W_\mu$ roadmap (F31–F36, F48) builds
> $W$ as an independently postulated classical $SU(2)$ Yang–Mills link field in the standard
> lattice-gauge-theory sense, never constructed as a fermion bilinear at all — but no source read
> for this chapter states this distinction explicitly, reconciles the two constructions, or explains
> why a boson built the second way should (or should not) still be subject to R8.3's coupling-
> structure forcing argument. This is not merely F89's already-flagged table-labelling issue (Ch.8
> Gap G-6, about which *row* of a summary table says "W/Z/gluon"); it is an unreconciled duality in
> what the $W$ boson **is**, constructively, between two halves of the source material this
> monograph draws on. Not resolved here, as this chapter is documentation-only; flagged for whoever
> next works on either the $W_\mu$ roadmap or the composite-bilinear/pairing-classification
> framework (most directly Chapter 13, which inherits the same duality for the gluon, and any future
> session revisiting F32's own module `ca_wmu.py` or F91's classification table).

## 12.3 Results table

| # | Statement | Exactness | Residual / tolerance | Source |
|---|---|---|---|---|
| R12.1 | $W$-triplet bilinear inherits the photon rotation law component-by-component; adjoint $SU(2)$ transformation | exact/machine | $\le6.7\times10^{-16}$ | F29 (8/8) |
| R12.2 | $SU(2)$ link variables, exact covariant BCC hopping, reduces to free step at $U_\ell=\mathbb I$ | exact/machine | Ward $1.2\times10^{-17}$ | F31 (6/6) |
| R12.3 | Even dispersion $\Omega_\text{even}$ required for a real $W$ field; chiral law violates Hermitian symmetry | machine | drift $3.1\times10^{-14}$ vs. $56\%$ | F32 (4/4) |
| R12.4 | Wilson-plaquette $SU(2)$ field strength; gauge-invariant $\|F\|^2$; identity vacuum $F\equiv0$ exact | exact/machine | $\le5.93\times10^{-16}$ | F33 (5/5) |
| R12.5 | Full Ward identity for the covariant doublet step; $\chi$ exactly decoupled at $m=0$ | exact/machine | $\le1.854\times10^{-13}$ | F34 (5/5); closes F27 Limitations 1/2 |
| R12.6 | Stueckelberg $W$ mass; $m_W=0$ at $U_\text{st}=\mathbb I$; exact gauge invariance of $m_W$ | exact/machine | $\le1.776\times10^{-15}$ | F34b (5/5) |
| R12.7 | Weinberg mixing exact self-inverse, commutes with propagation; $m_Z/m_W=1/\cos\theta_W$; $Q=T_3+Y/2$ | exact | $\le2.22\times10^{-15}$ | F35 (5/5) |
| R12.8 | Fermion back-reaction sources $W$ diagonally in isospin; Proca dispersion $\omega^2=m_W^2+\Omega_\text{even}^2$ | exact/machine | $\le1.4\times10^{-13}$ | F36 (5/5) |
| R12.9 | Dynamical $Z$; $g_V^{e_L}=0$ exactly at $\sin^2\theta_W=1/4$; source-basis identity | exact/machine | $\le1.5\times10^{-13}$ | F48 (12/12) |
| R12.10 | Hypercharge Ward identity on the F27 mass step, both branches; no isospin leakage | machine/exact | $\le9.16\times10^{-16}$ | F41 (7/7) |
| R12.11 | Quark hypercharge ports verbatim; $\chi$ singlets promoted to dynamical $Y$-covariant kinetic fields | machine/exact | $\le9.93\times10^{-16}$ | F42 (8/8) |
| R12.12 | Bipartite sublattice parity is abelian, stroboscopically conserved, Schur scalar, chirality-orthogonal, unique carrier | exact/machine | $\le1.8\times10^{-15}$ | F51 (5/5) |
| R12.13 | Hypercharge quantisation closes via F47's Majorana step ($2y_\nu=0$), not the gravitational anomaly | exact over $\mathbb Q$ | $0$ (literal) | F279 (5/5); supersedes F165 §2/§3 (S13) |
| R12.14 | All six anomaly traces vanish exactly over $\mathbb Q$ | exact over $\mathbb Q$ | $0$ (literal) | F38 (6/6) |
| R12.15 | $(W^3,B)$ mass block is rank-1 identically; $m_A=0$ automatic; photon eigenvector = Weinberg rotation | exact | $\le2.19\times10^{-16}$ | F44 (5/5) |
| R12.16 | Diamagnetic contact charge-blind; channel splitting purely paramagnetic | exact | $1.1\times10^{-10}$ | F153 (part) |
| R12.17 | $\sigma\leftrightarrow\tau$ swap counting: $\sin^2\theta_W=1/4$ bare, $m_Z/m_W=2/\sqrt3$ | exact rational | $+12.0\%$/$+1.77\%$ vs. PDG | F45 |
| R12.18 | BCC $2$:$7$ sublattice/bond-axis counting: $\sin^2\theta_W=2/9$ | exact rational, partial derivation | $-0.44\%$ vs. PDG | F49 |
| R12.19–20 | $\sin^2\theta_W=1/4$ is the UV MS-bar cap at $\mu_\star=4\pi v$, forced by $U(1)_Y$'s absent kinetic term; runs to $0.23173$ | exact mechanism / numeric | $+0.22\%$ (Higgs-free) | F138 (WM1–3) |
| R12.21 | $2/9$ is the on-shell face of $1/4$: $8/9=$ running $\times$ scheme conversion, residual $0.67\%$ | reconciliation | $0.67\%$ | F231 (W1–4) |
| R12.22–23 | 7 = exact WS-cell facet-axis count; equal-stiffness hypothesis (U) $\Rightarrow m_W^2{:}m_Z^2=7{:}9$ | exact lemma / conditional exact | $-0.063\%$ ($m_Z/m_W$) | F141 (11/11); (U) unproven, §12.2.21 |
| R12.24 | Wrap route: transverse induced stiffness exactly zero (all orders); longitudinal per-mille, no large-log | exact/numeric no-go | $1.3\times10^{-15}$; $0.16$–$0.36\%$ of $v^2$ | F143 (5/5) |
| R12.25–26 | Walk route: one-tick gauge rigidity exact, every channel; stroboscopic channel-quanta ratio $=1$; free-sea gap $=8/7$ | exact no-go / exact rational | $\le10^{-12}$ | F147 (10/10) |
| R12.27 | Free-Dirac proxy for the $8/7$ factor fails (both routes); physical condensate is $O(1)$, outside perturbative regime | structural negative | — | F153 (5/5) |
| R12.28–30 | Stiffness quantum $u=18\pi\alpha/7$ determined; $m_W=\tfrac{3v}2\sqrt{2\pi\alpha}$, $m_Z=\tfrac{9v}2\sqrt{2\pi\alpha/7}$; $\rho=1$ from rank | exact (conditional on (U)) | $<10^{-12}$–$1.4\times10^{-14}$ | F320 (22/22) |
| R12.31 | $\Delta r$-cancellation theorem: absolute-mass residual = on-shell-angle residual, for every $\Delta r$ | machine, $\Delta r$-free | $2.2\times10^{-16}$ | F320 (V4a) |
| R12.32 | $d\to u+e^-+\bar\nu_e$ integrated end-to-end; V−A, charge/baryon/lepton number exact; Fermi limit exact at $q^2=0$ | exact/exact-$\mathbb Q$/machine | $\le3.1\times10^{-13}$ | F54 (10/10) |

## 12.4 Comparison with measurement

This chapter carries the strongest, most precisely quotable numerical content of any chapter so far
in the monograph, and every number below is drawn from the committed finding files and their
`test-results/*.json` artifacts, cited to the specific residual reported there.

**The Weinberg angle, both faces.** F45's bare tree value $\sin^2\theta_W=\tfrac14$ is $+12.0\%$
from the PDG on-shell $0.22321$ (mass-ratio comparison: $m_Z/m_W=2/\sqrt3=1.1547$ vs. PDG
$1.1346$, $+1.77\%$). F49's BCC counting $\sin^2\theta_W=\tfrac29=0.2222\overline2$ is $-0.44\%$
from the same PDG on-shell value ($m_Z/m_W=3/\sqrt7=1.133893$ vs. PDG $1.134614$, $-0.064\%$,
F231/F141). F138's mechanism closes F45's MS-bar gap to $\sin^2\bar\theta_W(M_Z)=0.23173$
(Higgs-free $\beta$-coefficients) against PDG MS-bar $0.23122$: residual $+0.22\%$ — roughly forty
times smaller than the uncorrected $+8.12\%$ MS-bar gap, and closer than the Standard Model's own
$b_i$ ($0.23210$, $+0.38\%$). F231 shows these are not competing numbers: the exact bridge
$8/9$ between them decomposes into one-loop running ($0.9269$) times MS-bar-to-on-shell scheme
conversion ($0.9654$), reproducing $8/9=0.8889$ to $0.67\%$.

**The absolute boson masses, F320's capstone bracket.** At tree level ($\Delta r=0$), $m_W=79.0836$
GeV ($-1.60\%$ vs. PDG $80.3692$), $m_Z=89.6724$ GeV ($-1.66\%$ vs. PDG $91.1880$) — the expected
deficit, which is exactly the radiative correction $\Delta r$ the Standard Model's own tree relation
also carries. With $\Delta r$ bracketed between the model-supplied piece ($\Delta\alpha-\tfrac72
\Delta\rho$, using the model's own $c^2/s^2=\tfrac72$ exactly) and the value the PDG masses
themselves imply:

$$m_W\in[80.147,\,80.548]\ \text{GeV},\qquad m_Z\in[90.879,\,91.332]\ \text{GeV}$$

both containing the PDG central values, with the bracket's width ($0.00965$) matching the Standard
Model's own residual radiative term $\Delta r_\text{rem}\approx0.0096$ from the literature — the
check that the bracket is the right object, not merely a convenient one. Most decisively, **the
$\Delta r$-free result**: because the model and the SM sit on the same on-shell relation with the
same $\Delta r$, the mass-ratio ${m_W^\text{model}}/{m_W^\text{obs}}=\sqrt{\sin^2\theta_W^\text{obs}
/(2/9)}$ is constant to $2.2\times10^{-16}$ across the entire tested range $\Delta r\in[0,0.10]$,
giving

$$\boxed{\;m_W:\ +0.222\%,\qquad m_Z:\ +0.158\%\;}$$

as a residual free of any radiative-correction assumption whatsoever. This is the number to cite
when asked "how good is the prediction" — it inherits F231's on-shell-angle accuracy exactly and
adds no freedom of its own.

**$\rho=1$.** Verified exactly (as a `Fraction`, not to tolerance) for every value of the stiffness
quantum $u$ — a genuine derivation from the rank of the Higgs-free Stueckelberg breaking, where the
Standard Model instead needs the custodial $SU(2)$ of a Higgs doublet this model does not have.

**Anomaly cancellation and charge assignments.** All six FG-1 anomaly traces vanish as literal
integer zeros over $\mathbb Q$ (F38); the Gell-Mann–Nishijima relation $Q=T_3+Y/2$ holds exactly for
all seven first-generation states (F35, F38); the hypercharge assignment is quantised to one overall
normalisation, now correctly attributed to F47's Majorana step rather than the gravitational anomaly
(F279).

## 12.5 What was excluded, and why

**A dynamical Higgs boson anywhere in this chapter's construction.** Excluded at the postulate level
by Chapter 1 (P6) and at the mechanism level by Chapter 11 (F27); this chapter shows in full detail
what the Higgs's *electroweak-sector* roles specifically are replaced by — the VEV-direction role by
$U(x)$ (Chapter 11, R11.6), the mass-generation role by the Stueckelberg construction (F34b), the
custodial-$SU(2)$ role for $\rho=1$ by the *rank* of the single-Stueckelberg-direction breaking
(F44, F320) rather than by an imposed symmetry, and the third-input role for the absolute boson
masses by nothing at all — $\sin^2\theta_W$ is supplied by lattice geometry instead (F49/F141),
which is precisely why the Standard Model's third input is not needed here.

**The notebook's two-field Stueckelberg parameterisation.** F44 shows explicitly that Ludwig's own
notebook implicitly assumes two *independent* Stueckelberg fields (one for $SU(2)_L$, one for
$U(1)_Y$), which would require $m_{W_0}^2/m_W^2=-\tan^2\theta_W$ — impossible for real masses — to
force $m_A=0$. The model's actual F34b+F41 construction uses **one** field, for which $m_A=0$ is
automatic rather than fine-tuned; the two-field theory is not adopted, and its impossibility for
real masses is recorded as a positive argument for the single-field construction being the only
consistent realisation.

**Perturbative free-fermion proxies for the $8/7$ bookkeeping factor.** F143's wrap-route loop and
F147's walk-route loop both prove, by independent exact mechanisms, that the free fermion sea cannot
supply gauge-channel stiffness at all (one-tick rigidity, transverse conjugation no-go); F153 then
tests the two remaining free-Dirac-proxy routes to the $8/7$ factor directly (a small-$m$ splitting
function $R(m)$, and a geometric multiplicity count) and finds both fail to deliver a clean number —
the small-$m$ expansion is shown to be the wrong regime entirely, since the physical condensate
coupling is $O(1)$ (F150's saturated regime). None of these three findings is a failure of the
$\sin^2\theta_W=\tfrac29$ on-shell prediction itself, which is exact algebra (F141) independent of
any of them; they are a systematic elimination of the *wrong tools* for closing F141's hypothesis
(U), redirecting the remaining work to the non-perturbative condensate sector.

**The chiral (single-branch) propagation law for the classical $W$ field.** F32 rejects it directly
and decisively on physical grounds — Hermitian-symmetry violation for a real-valued field — in favor
of the even law used throughout the rest of Group A. This exclusion is stated in F32's own text with
a measured, quantitative reason (not a preference), and it is the one exclusion in this chapter that
Gap G-7 (§12.2.26) shows sits in unreconciled tension with a later theorem (R8.3) about which channel
the $W$'s *coupling* should force.

## 12.6 What is still open

1. **The equal-stiffness hypothesis (U) that underlies F141's counting and F320's absolute masses
   remains an unproven structural assumption**, decomposed into three sub-claims (U1 condensate-level
   equality across the 7 axis channels, U2 axis↔sublattice cross-normalisation, U3 explicit
   quadratic-form assembly), none fully closed. F143/F147/F153 collectively prove the free fermion
   sea cannot supply it and redirect the calculation to the non-perturbative $E_g$/EWSB condensate
   sector (F118, F150) — named as the concrete next step by three independent findings, but not
   attempted by any of them.
2. **$\alpha_\text{em}$'s magnitude remains undlerived** (Chapter 9's own no-go, F127/F339/F349),
   and this chapter's absolute-mass prediction now depends on it directly, not only through the
   electron's coupling — increasing, in F320's own words, the weight that no-go carries.
3. **$v$ (equivalently $G_F$) remains an external SI/EW-scale anchor**, per F119, unchanged by
   anything in this chapter; every absolute number quoted here is relative to it.
4. **The NDA identification $\mu_\star=4\pi v$ is not a computed scale.** F143 bounds the one
   computable correction (the fermion-loop share of $v^2$) at $0.08$–$0.18\%$, an order of magnitude
   below the $10\%$ NDA offset itself, but does not replace NDA with a derived number.
5. **$N_c=3$ remains an external input** (graded `ABSENT` in the project's own completeness sweep,
   per F279's own text) — hypercharge *quantisation* is derived for any $N_c$; the specific fractions
   $\tfrac23,-\tfrac13$ additionally require $N_c=3$, forward-cited to Chapter 13.
6. **Gap G-7 (§12.2.26)** — the unreconciled duality between the $W_\mu$ roadmap's independently
   postulated Yang–Mills link field and the composite-bilinear/pairing-classification framework's
   apparent requirement that a $P_L$-coupled boson ride the chiral channel — is genuinely open, not
   merely under-explained; it is not resolved by anything read for this chapter and is flagged
   forward, most directly to Chapter 13's gluon sector, which inherits the identical question.
7. **The Weinberg-angle counting's own internal-vs-external reconciliation (F45 vs. F49) is a
   structural match, not a rigorous joint derivation.** F49's own text names the specific open
   question (how a $1{:}3$ internal count and a $2{:}7$ external count could both govern the same
   generator structure without conflict) and F231/F141 sharpen its target (the on-shell scheme) but
   do not resolve it.

## 12.7 Falsifiers

From the relevant claim cards, at their actual status:

1. **CL007 (F41/F49/F138, `live`, `exact`, `falsifier: stated`)** — "The Weinberg angle is derived,
   with its scale." Falsifier: a precision $m_W$ that moves $m_Z/m_W$ off $3/\sqrt7$ by more than the
   running uncertainty; **CL014 carries the numerical threshold**.
2. **CL014 (F49/F138/F231, `live`, `exact`, `falsifier: stated`)** — the $\sin^2\theta_W=\tfrac14$-
   at-$4\pi v$-and-$\tfrac29$-on-shell threshold claim. Falsifier: identical to CL007's — a precision
   $m_W$ moving $m_Z/m_W$ off $3/\sqrt7$ beyond the running uncertainty.
3. **CL276 (F320/F141/F138/F231/F49/F51, `live`, `bracketed`, `falsifier: stated`)** — the absolute
   two-input mass prediction. Falsifier, stated with no free parameter to absorb it: the claim dies
   if $\sqrt{\sin^2\theta_W^\text{obs}/(2/9)}$ leaves $[0.995,1.005]$ — i.e. the on-shell angle
   residual leaving $\pm1\%$. The entire residual **is** the angle residual, by R12.31's own
   $\Delta r$-cancellation theorem.
4. **CL277 (F320/F41/F27/F51/F141, `live`, `exact`, `falsifier: none`)** — $\rho=1$ from rank, not
   custodial $SU(2)$. No stated falsifier: a genuine second condensate direction (the
   `rank_two_breaking` control) would break it, but this is a construction-level statement about the
   model's own breaking mechanism, not an independent experimental prediction distinct from $\rho=1$
   itself, which is already extremely tightly measured and matched by every viable electroweak model.
5. **CL010 (F165/F279/F47/F27/F41, `live`, `exact`, `falsifier: unset`)** — charge quantisation is
   derived, not assumed. No falsifier is currently stated for this card; recorded as debt rather than
   filled in here, consistent with how this chapter reports every other unresolved status rather than
   inventing one.
6. **CL016 (F138/F320, `withdrawn`)** — the old "absolute $m_W$/$m_Z$ not claimed" non-claim card is
   withdrawn by F320 itself, within this chapter's own source material; recorded here as the
   claims-layer trace of this chapter's capstone result superseding a prior, narrower non-claim, not
   as a new correction this chapter is making.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–11's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $W_\mu^a(x)$, $U_\ell\in SU(2)$ | The dynamical $SU(2)_L$ gauge field and its BCC link variables | §12.2.2 (F31) |
| $\Omega_W(\mathbf k)=\Omega_\text{even}(\mathbf k)$ | The free $W$-field dispersion, identical in form to the photon's (R6.3); adopted for Hermitian-symmetry reasons, not coupling-structure ones — see Gap G-7 | §12.2.3 (F32) |
| $F^a_{\mu\nu}(x)$ | The $SU(2)$ Wilson-plaquette field strength | §12.2.4 (F33) |
| $U_\text{st}(x)\in SU(2)$ | The Stueckelberg scalar generating $m_W$ without a Higgs VEV | §12.2.6 (F34b) |
| $\theta_W$ | The Weinberg angle; an input at F35, derived by three routes at Group D | §12.2.7 (F35), derived §12.2.17–12.2.24 |
| $\Delta Y_e,\Delta Y_\nu,\Delta Y_u,\Delta Y_d$ | The Higgs-equivalent hypercharge differences $Y_L-Y_R$ absorbed into $U(x)$; numerically $(\mp1,\pm1)$ across sectors | §12.2.10–12.2.11 (F41, F42) |
| $P=(-1)^{x_1+x_2+x_3}$ | The BCC bipartite sublattice parity; the unique carrier of hypercharge | §12.2.12 (F51) |
| $y_Q,y_u,y_d,y_L,y_e,y_\nu,y_\phi$ | The normalised hypercharge unknowns of the F165/F279 quantisation system | §12.2.13 (F279) |
| $u$ | F141's universal per-channel stiffness quantum; free in F141, determined ($=18\pi\alpha/7$) in F320 | §12.2.21 (F141), closed §12.2.24 (F320) |
| $\mu_\star=4\pi v$ | The NDA compositeness matching scale at which $\sin^2\theta_W=\tfrac14$ holds exactly | §12.2.19 (F138) |
| $\Delta r$ | The electroweak radiative correction to the on-shell mass relation; external, bracketed but shown to cancel in F320's mass-ratio theorem | §12.2.24 (F320) |
| $T^\pm=T^1\pm iT^2$, $J^\pm(x)$ | The charged-current raising/lowering generators and currents | §12.2.25 (F54) |

---

*Gap **G-7** logged in `docs/monograph/GAPS.md` under a new "Chapter 12" section, appended after
Chapter 8's G-6 entry (the last existing entry at the time of writing). No other new gap found: the
remaining open items of §12.6 are, without exception, disclosed honestly and in detail by the
findings' own text (F138 §7, F141 §5, F143 §7, F147 §5, F153 §7, F320 §6) rather than papered over,
and are therefore carried in this chapter's own §12.6 rather than logged as documentation gaps. No
finding, claim card, module, or test record was created or modified in the writing of this chapter.*
