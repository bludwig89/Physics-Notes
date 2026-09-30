# Chapter 13a — Colour Structure and Confinement

*Chapter 13a of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). This is the FIRST HALF
of a chapter split authorized by the plan's §8: the original "Chapter 13: Colour and the strong
sector" carried 49 findings, too many for one file. **13a** (this file, 26 findings) covers the
qualitative/structural half — why $SU(3)$, why three colours, and how confinement actually works.
**13b** ("Dynamical QCD and the X1 Casimir-normalisation saga," 23 findings) continues from here with
the quantitative $\alpha_s$/scheme-conversion/lattice-technical material and reads this chapter's
results before citing them (`docs/monograph/BUILD-STATE.yaml`). Sourced from
`findings/F43-fg7-dynamical-gluons.md`, `findings/F70-gradient-flow-confinement-string-tension.md`,
`findings/F86-colour-dielectric-dual-superconductor.md`, `findings/F88-colour-condensate-from-model.md`,
`findings/F90-e2e-nonabelian-bilinear-backreaction.md`,
`findings/F99-sigma-as-centre-lagrange-multiplier.md`, `findings/F100-gamma-from-transfer-operator.md`,
`findings/F101-strong-coupling-sigma-compact-rotor.md`, `findings/F102-coupled-rotors-crossover-survives.md`,
`findings/F110-realtime-link-hamiltonian-confinement.md`,
`findings/F117-gap-coupled-dielectric-gluon-propagator.md`, `findings/F135b-realspace-scalar-confinement.md`,
`findings/F137-live-colour-dielectric-flux-tube.md`, `findings/F139-self-consistent-dual-gl-backreaction.md`,
`findings/F142-dielectric-tension-no-go-and-nonabelian-scope.md`,
`findings/F166-triple-gluon-vertex-branch-blind.md`, `findings/F293-why-three-colours.md`,
`findings/F294-c7-chi-map-ncolour-audit.md`, `findings/F317-su3-structure-derived.md`,
`findings/F321-strong-cp-theta-zero-and-loop-stable.md`, `findings/F324-ncolour-bracket-closed.md`,
`findings/F325-x1-resolved-branch-b-adopted.md`,
`findings/F333-internal-index-existence-narrowed-to-confinement-and-baryon-statistics.md`,
`findings/F338-ncolour-ceiling.md`, `findings/F381-premise-a-irreducible-from-spin-statistics.md`, and
`findings/F382-vertex-not-G-periodic-cube-domain-excluded.md` — all 26 read in full. Checked directly
against `docs/theory/supersessions.yaml`: **S2-F91-gluon-chiral-to-even** (read in full; discussed at
length in §13a.2 below) is the one record touching this chapter's findings; none of the other 25 is
named in any of the 23 records. Checked against `claims-index.md`: **CL049** (F43), **CL067** (F70),
**CL081**/**CL083** (F86/F88), **CL091**/**CL092** (F99/F100), **CL094** (F102), **CL104** (F117),
**CL121** (F135b), **CL123** (F137), **CL124** (F139), **CL146** (F166), **CL006** (F97/F101/F110/F142,
`status: narrowed`, the confinement headline card), **CL271**/**CL272**/**CL281**/**CL287** (F317/F318
[not assigned here]/F324/F333, the colour-structure-forced-by-one-index chain), **CL257**/**CL282**
(the $N_c$ cards, `status: narrowed`/`live` respectively, both with specific bracketing caveats), and
**CL278** (F321). Notation and results are those of Chapters 1, 4, 11 and 12 — $\psi$, $D(\mathbf k)$,
$U(x)$, $\Omega(\mathbf k)$, $c_\text{lat}$, the $SU(2)_L$ construction — extended, never redefined.*

## 13a.0 What this chapter establishes, and its one-paragraph statement

The Standard Model simply posits $SU(3)_c$ with three colours, one gauge coupling, and confinement as
an empirically-observed but analytically-unproven property of the resulting Yang–Mills theory. This
chapter asks, of this project's lattice construction, how much of that structure is forced rather than
assumed, and — the harder question — *why* an $SU(3)$ Yang–Mills theory with matter of this content
actually confines, worked out as an explicit mechanism rather than cited as a lattice-QCD fact from the
literature. The answer, stated in full before the derivation: granted exactly **one** input — that the
quark carries an internal index the rule's own dynamics does not read — everything downstream of that
index (unitarity, specialness, locality forcing a connection, vector-like coupling, the even
propagation law, eight gluons) is **forced**, not chosen (§13a.2, F317). *Which* integer that index
carries is **not** forced to 3: three structurally-independent routes are closed as no-gos or shown
circular, and what survives is an empirical selector (a 28-decade confinement-scale lever) plus, later,
a genuine but incomplete anomaly-based narrowing that leaves the honest state of the art at "$N_c$ odd,
$N_c\ne1$, favoured at exactly 3 only by data" (§13a.3). And confinement itself — the model's most
important strong-sector result — is derived, not assumed: a chain running from an exact 2D area law,
through a forced colour-magnetic condensate, to a centre-algebra identity that makes the string tension
the Lagrange multiplier of $\mathbb Z_3$ centre-phase non-closure, to a real-time dynamical flux tube
that a baryon digs for itself and that survives a rigorous no-go about which of its two competing
real-space pictures is exact (§13a.4).

## 13a.1 Inputs

**Postulates used.** **P2/P3** (locality, homogeneity/isotropy of the BCC connectivity) are what make
§13a.2's central argument possible at all: a cellular automaton has no global operations, so an internal
rotation acting on an index the on-site rule does not read commutes with the on-site step for free,
while the *hopping* step (which compares two cells) forces a connection — this asymmetry, not an
imported gauge principle, is what F317 §3 calls "the price of the rule being local." **P4**
(unitarity) fixes the invariance group of the internal index to $U(N)$ by a computed commutant, not an
assumed representation theory. **P5/P6** (the Weyl-spinor primitive; the chiral $SU(2)_L$ mass
mechanism) are what make colour's coupling forced to be *vector-like* rather than chiral (§13a.2.2):
$SU(2)_L$ being chiral is the other half of the same fact that makes $SU(3)_c$'s coupling forced to be
vector-like — a chiral colour triplet is anomalous ($SU(N\ge3)$ has a symmetric cubic Casimir a chiral
doublet does not), so the model's derived electroweak chirality (Chapter 11) is what removes the
option. **P7** is not invoked as a selection criterion anywhere in this chapter — every forced result
below is forced by an explicit algebraic or group-theoretic argument, not chosen among equally-good
alternatives on elegance grounds; where elegance *was* the stated reason for a choice (F91's original
gluon-even classification, before F317 closed it — see §13a.2.2), this chapter records that it has
since been superseded by a forcing argument, not merely re-asserted.

**Prior results used, precisely.** **R4.4b/R4.4c** (`04-structural-theorems.md` §4.2.3, F289) — the
derived spin–statistics connection, specifically that $\pi_1=S_n$ (not the braid group $B_n$) only
because $d\ge3$, and that the exchange sign is forced rather than imported — is the machinery §13a.3.5
(F333, F381) builds on and is explicit about *not* re-deriving: a single spin-½ constituent's exchange
sign being forced does not, by itself, fix an $N$-constituent composite's statistics without knowing
$N$, which is exactly the residual F381 isolates. **R11.5/R11.6** (`11-mass-without-a-higgs.md`
§11.2.3, F27) — the exact $SU(2)_L$ Ward identity for the chiral mass step, and the proof that $U(x)$
carries zero physical information (pure gauge) — is the template F317 §3 explicitly generalises: *why*
$F27$'s connection needed no compensator on the on-site mass step (chirality-mixing, on-site) while a
colour connection is forced on the hopping step is one and the same locality argument, read on two
different steps of the same construction. **R12.3** (`12-hypercharge-and-electroweak.md` §12.2.3, F32)
— the $W$ field's own free-propagation law, adopted on physical (Hermitian-reality) grounds *before*
F91's forcing theorem existed — and its associated **Gap G-7** (the unreconciled duality between F32's
even choice and F91's later chiral-forcing theorem for the $W^\pm$'s coupling) are the direct point of
comparison for §13a.2.2's central finding: this chapter shows the identical question, asked of the
gluon, has a clean answer, and states explicitly why the gluon's case does not inherit G-7's
unresolved tension.

**Free inputs consumed.** This chapter's honest accounting, carried through to the results table,
is: **the internal colour index's bare existence** (F317 §0 item (i); narrowed further, not removed,
by F333/F381, §13a.3.5); **which integer that index carries** (only bracketed, not derived — the
tightest structural statement reached is "$N_c$ odd, $N_c\ne1$," §13a.3.4); **the colour-magnetic
condensate's dynamical magnitude** (its *existence* is forced, F88, but its 3+1D numerical VEV is not
computed in closed form — CL006's own scope statement, §13a.4.7); and **the quark mass texture at
three generations** (needed to complete the strong-CP statement of §13a.5 beyond one generation, where
it already closes exactly).

## 13a.2 The derivation — Group A: the gauge sector itself

### 13a.2.1 One index, six impositions, one residual (F317)

`docs/status/completeness-2026-08-07.md` row **B1** read, before this finding: "colour is still put
in." F317 shows that sentence bundles **six** separate impositions and that five of them are forced,
given only the sixth:

| | imposition | status |
|---|---|---|
| (i) | the quark carries an internal index **at all** | still an input — nothing derives it |
| (ii) | the index has dimension **3** | Group B's business, not this section's — §13a.3 |
| (iii) | its invariance group is **unitary** | **derived** — the commutant of the model's own steps (mass step + BCC walk) is computed, not assumed, to be $M_9=M_{3^2}$, i.e. the full matrix algebra on a 3-dimensional internal factor, whose norm-preserving subgroup is exactly $U(3)$ (F317 §4, checks S4a–S4c). A first draft used a spin-blind walk and got a spuriously large commutant (36, not 9) — recorded in the finding as a hazard a later re-derivation might repeat. |
| (iv) | the group is **special** unitary, not $U(3)$ | **derived** — the $U(1)$ trace subgroup of $U(3)$ is anomalous against the model's own derived $[SU(2)_L]^2 U(1)$ constraint, because the same row that fixes hypercharge ($N_c y_Q + y_L = 0$) cannot simultaneously be satisfied by a colour-blind trace charge (F317 §5, S5a/S5b) |
| (v) | the symmetry is **local**, hence carries a connection | **derived** — a cellular automaton has no global operations, so an on-site step is automatically covariant under a *site-dependent* internal rotation with no compensator, while a hopping step (comparing two cells) is not; the gluon connection is "the price of the rule being local," not an added ingredient (F317 §3) |
| (vi) | the coupling is **vector-like**, not chiral like $SU(2)_L$'s | **derived** — a chiral colour triplet is anomalous ($su(3)$ carries a non-zero symmetric cubic invariant $A^{888}=-\tfrac1{\sqrt3}\ne0$, unlike $su(2)$'s exactly-zero 27 triples), so anomaly cancellation forces the vector-like assignment given the model's derived $SU(2)_L$ chirality (F317 §2, S1a–S1c) |

$$\boxed{\;\text{R13a.1 — granted one internal index the rule does not read, }U(N)\text{ (commutant, S4b), }SU(N)\text{ (anomaly, S5a/S5b), locality} \Rightarrow\text{connection (S3a–d), and vector-like coupling (S1c) are all forced; the index's bare existence is not}\;}\tag{R13a.1}$$

(F317 §§1–7, checks S0–S5e, 21/21 PASS, six declared controls each red only where declared.)
**Claim:** `docs/claims/CL271-colour-structure-forced-by-one-index.md` — `status: live`, `exactness:
exact`, `tier: headline` — states the same six-way split and is careful, as this chapter is, that it
does **not** touch the $N_c$-value question (row B10, §13a.3) or the X1 colour-normalisation fork
(deferred to Chapter 13b in full).

An incidental but important side effect: F317 §6 also computes, as a corollary, that given three
quark-only ($\varepsilon$-tensor) constituents, an $SU(N)$-invariant singlet in $\Lambda^3(\mathbb
C^N)$ exists at exactly one value, $N=3$ (verified $N=2\ldots6$). This is *not* offered here as a
derivation of $N_c=3$ — as F317 itself states, and as F324 later shows explicitly (§13a.3.4), the
"three constituent" premise is not independent information once $N_c$ is otherwise fixed — but it is
the seed of the Group B discussion that follows.

### 13a.2.2 The even propagation law: forced, not chosen — and unlike the $W$, the gluon inherits no unresolved duality

Chapter 12's Gap **G-7** (`docs/monograph/GAPS.md`) flags an unreconciled tension for the $W^\pm$
boson: F32 (2026-05-24) rejects the *chiral* dispersion law for the classical $W$ field on direct
physical grounds — a real-valued field cannot remain Hermitian-symmetric under it, measured as IFFT
imaginary parts up to $\sim0.8$ and $56\%$ energy drift — and adopts the *even* law instead, eleven
days **before** F91 (2026-06-04) proves that the $W^\pm$'s own fermion coupling structurally *forces*
the opposite: the chiral channel, because $\|P_L\psi_R\|=0$ exactly for a pure left-projector coupling.
Chapter 12 states plainly that this tension between "what a real classical Yang–Mills field needs" and
"what the coupling forces" was never reconciled anywhere in the sources it read, and explicitly flags
that "Chapter 13 inherits the identical question for the gluon" (§12.2.26).

**This chapter's answer, worked through the actual chronology of the gluon sector's own findings, is
that no such duality exists for the gluon — the two requirements agree, and three independent findings
close every route by which they could have disagreed.**

**F91's own free-field argument (2026-06-04).** The commutator that classifies a coupling's propagation
law is $\big[\mathrm{diag}(U^+,U^-)\otimes\mathbf I_3,\ \mathbf I_4\otimes e^{i\theta\cdot T}\big]=0$
to $1.1\times10^{-16}$: the colour generator $T^a$ acts identically on both BCC chiral branches,
i.e. the fermion–gluon coupling is branch-blind. By the same F68 argument that forces the photon's
even law, a branch-blind coupling can source only the helicity-symmetric (even) dispersion. F91's own
text records this classification as resting on the vector-like assignment being "by construction," and
the even law's specific adoption as resting partly on "the elegant-design philosophy" — i.e., at this
point in the record, the classification was correct but its premise was still a choice, not yet a
theorem.

**S2-F91-gluon-chiral-to-even (2026-06-04, same day).** The production code is migrated from the
chiral to the even gluon step on the strength of F91's commutator alone
(`docs/theory/supersessions.yaml`, record `S2-F91-gluon-chiral-to-even`): "the colour coupling is
branch-blind, so the gluon is even (the F68 commutator argument verbatim in colour)... a correctness
migration, not a phenomenological one." The chiral step is retained as
`gluon_rotation_step_spectral_bcc_chiral` for historical comparison; the even step
(`gluon_rotation_step_spectral_bcc`) is canonical from this point forward.

**F166 (2026-06-29) closes the interacting-level loophole.** F91's forcing argument was, as recorded,
proven only at the *free-propagator* level; the 2026-06-29 physics audit's item C3 named the
hypothetical risk directly: "if the nonlinear self-coupling has any chiral component, the even
classification would need revision... weakens 'forced' to 'forced at the free-field level.'" F166
answers it by inspecting the model's own triple-gluon vertex ($\Gamma^F_{\alpha\mu\lambda}$, the F162/
F163 background-field object): it is a rank-3 tensor built entirely from Lorentz and colour indices,
with **no spinor/branch axis at all** — the pure-gauge plaquette action $S(A)$ that generates the
self-coupling is a functional of the gauge field alone. Its chiral (pseudoscalar) projection is
therefore identically zero, $P_{\gamma^5}(\mathbf I_2)=\tfrac12\mathrm{Tr}(\gamma^5\mathbf I_2)=0$,
confirmed as an exact structural zero (T1–T4, 4/4 PASS) and contrasted directly against the $W$'s
nonzero $P_{\gamma^5}=1/2$ in the same table. The quartic vertex follows by the identical argument
(same index content, not separately computed). **The even law is forced at the interacting level too,
with no chiral component anywhere in the gluon sector — not a hypothetical closed, but the actual
vertex measured and found branch-trivial.**

**F317 (2026-08-16) closes the last unforced premise.** F91's classification chain had one remaining
non-forced link: the vector-like assignment itself, recorded as "by construction." F317 §2.1 states
this explicitly and closes it: "S1c replaces *by construction* with *forced*. F91's chain then runs
with no free step: anomaly freedom $\Rightarrow (g_L,g_R)=(g_s,g_s)\Rightarrow$ branch-space coupling
$\propto\mathbf 1\Rightarrow$ (F68 verbatim) even law." What was chosen on elegance grounds in F91 is,
after F317, derived from the same anomaly-cancellation argument that forces colour to be vector-like at
all (§13a.2.1, item (vi)).

$$\boxed{\;\text{R13a.2 — the gluon's even propagation law is forced at every level checked: free coupling (F91 G1, S2-migrated), self-coupling / interacting vertex (F166, exact structural zero), and its remaining premise (vector-like coupling itself, F317). No competing requirement — reality of a classical field, coupling forcing, self-coupling structure — pulls the other way, unlike the still-open W duality (Chapter 12, Gap G-7)}\;}\tag{R13a.2}$$

**Why the gluon's case differs structurally from the $W$'s, stated precisely.** The $W$'s duality is
genuine because two different *constructions* of the same object disagree: an independently postulated
classical $SU(2)$ Yang–Mills link field (F31–F36, built and required to be real and Hermitian-symmetric
— hence even, F32) versus a composite-bilinear coupling whose branch structure is chirally-projecting
by the fermion content itself (hence forced chiral, F91). For the gluon, **the two constructions were
never in tension**: F43's gluon octet bilinear $G^{a,i}$ (the composite-bilinear route, paralleling
F91's classification machinery) and F43's Wilson-plaquette Yang–Mills self-coupling (the independently
postulated classical-link route, paralleling F31–F36) are both forced onto the identical even law — the
composite-bilinear route because the colour coupling is branch-blind (F91/F317), and the classical-link
route because a colour-blind self-coupling carries no branch/spinor content to disagree with that
(F166). A real, Hermitian-symmetric classical gluon field and a branch-blind fermion coupling *want the
same dispersion law* for the gluon, where they wanted opposite ones for the $W$. This is a
consequence, not a coincidence: the $W^\pm$'s coupling is chiral (pure left-projector) precisely
because $SU(2)_L$ is chiral (Chapter 11), while colour's coupling is vector-like precisely because
$SU(3)_c$ cannot be chiral without an anomaly (§13a.2.1, item (vi)) — the same electroweak-chirality
fact that makes the $W$ genuinely torn between two requirements is what leaves the gluon with no such
tension at all. **No new gap is logged in `docs/monograph/GAPS.md` for this question**, because none
was found: this is a resolution, carried through the gluon sector's actual chronology, not a silent
side-stepping of Chapter 12's open item.

### 13a.2.3 The dynamical gluon field, built and certified (F43, F90)

With the group, connection and propagation law all forced or fixed, F43 (2026-05-27) builds the actual
dynamical gluon sector — the $SU(2)_L$-sector construction of Chapter 12 (F29 bilinear, F33 self-
coupling, F36 back-reaction), ported to $SU(3)_c$ with $\tau^a\to T^a$, $\epsilon^{abc}\to f^{abc}$:

- **Structure constants.** The nine independent non-zero $f^{abc}$ built from $[T^a,T^b]=if^{abc}T^c$;
  the Jacobi identity holds across all $8^4$ index combinations to $1.1\times10^{-16}$.
- **The colour-octet bilinear** $G^{a,i}(\mathbf x)=\sum_f\sum_{cc'}(T^a)_{cc'}\sum_{\alpha\beta}
  q^{f,c,\alpha\dagger}\sigma^i_{\alpha\beta}q^{f,c',\beta}$, propagating by the (now-forced) even
  rotation law on both the 2D-square and BCC lattices — the eight octet components are the gluons.
- **The Wilson plaquette field strength and Yang–Mills self-coupling**, gauge-invariant ($\|F\|^2$
  residual $5.93\times10^{-16}$) and unitarity-preserving to $10^{-15}$ after self-coupling steps.
- **A Wilson-loop area-law diagnostic**: the cold-link baseline reproduces $\langle\mathrm{Re}\,
  \mathrm{Tr}\,W\rangle=N_c=3$ exactly, local $SU(3)$ gauge invariance holds to $4.6\times10^{-16}$, and
  Haar-random (strong-coupling) links decorrelate the loop by $\sim75\times$ — the deconfined baseline
  and the seed of §13a.4's confinement chain.
- **Quark-current sourcing**, colour-diagonal by construction (each octet component $a$ sourced only
  by its own current $J^a$), reducing bit-for-bit to the free step at $m_g=0$.

(F43 §§Phase A–D, 20/20 PASS, 8 bit-for-bit exact.) F90 (2026-06-04) then **certifies the full
end-to-end loop** for the non-Abelian sectors together (W, Z, gluon): a real fermion current sources
the field exactly (kick residual $4.4\times10^{-16}$), the work–energy ledger closes to
$4.0\times10^{-17}$ over 30 ticks, a causal colour-current front propagates and arrives after the
correct light-time, global $SU(3)$ covariance holds for the sourced step ($3.1\times10^{-15}$), the
$f^{abc}$ Jacobi identity re-verifies, and — the new result — the fermion↔gluon back-reaction loop
closes in **both directions simultaneously** for the first time (norm $6.4\times10^{-15}$, ledger
$6.9\times10^{-18}$, exact $g=0$ reduction, nonzero back-action $3.3\times10^{-3}$), with field-energy
radiation confirmed against a zero-current control that stays exactly zero.

$$\boxed{\;\text{R13a.3 — the dynamical SU(3) gluon sector (octet bilinear, Yang–Mills self-coupling, Wilson-loop diagnostics, quark-current sourcing) is built structurally parallel to Chapter 12's }W\text{ construction, and certified end-to-end with a closed fermion}\leftrightarrow\text{gluon back-reaction loop}\;}\tag{R13a.3}$$

(F43: `CL049`, `status: live`, `falsifier: unset`. F90 introduces no new claim card of its own; it is
an integration/certification finding in the F85 style.)

## 13a.3 The derivation — Group B: why three colours

Having established *that* the colour sector's structure follows from one internal index, the harder
question — *why that index carries the value 3* — is attacked directly and honestly left open. Row
**B10** of the completeness rubric is the project's own name for this question.

### 13a.3.1 Three closed no-gos (F293 R1–R3)

**R1 — anomaly cancellation cannot select $N_c$.** The Standard Model's textbook argument (that $N_cY_Q
+Y_L=0$ with independently-fixed $Y_Q=\tfrac16$, $Y_L=-\tfrac12$ forces $N_c=3$) is unavailable in this
model, because $Y_Q$ is not independently given here — it comes out of the *same* hypercharge nullspace
that is proportional to $N_c$ ($y_Q:y_u:y_d:y_L:y_e:y_\nu = 1:(N_c{+}1):(1{-}N_c):{-}N_c:{-}2N_c:0$).
The nullspace has dimension exactly 1 for **every** $N_c$ tested ($N_c=1,2,3,4,5,7$), and both the
gravitational and cubic $U(1)^3$ anomalies vanish identically as polynomials in $N_c$. The would-be
derivation is exactly circular.

**R2 — colour is not the spatial 3.** The BCC point group $O_h$'s $C_3$ rotation about $[111]$ is,
formally, an element of $SU(3)$ acting on three spatial-axis labels — but $\max_a\|[C_3,\lambda^a]\|=
2.449\ne0$: an axis-identified colour would be *rotated by an ordinary lattice rotation* and hence
observable, whereas a genuine internal $SU(3)$ commutes with spatial rotations exactly ($0.0$).
Independently, $O_h$ is finite (order 48, supplying at most $S_3$ on three axes) and cannot contain the
continuous 8-parameter group $SU(3)_c$ needs.

**R3 — the $\mathbb Z_3$-centre route is circular as the tree stands.** F97/F99/F110 make the $\mathbb
Z_3$ centre load-bearing *for confinement* (§13a.4), and a centre-based $N_c$ selector is the most
natural-looking remaining idea — but the tree introduces that $\mathbb Z_3$ **as the centre of
$SU(3)$** (F110: "$\mathbb Z_3$ — the $SU(3)$ centre that carries the area law"). A centre taken *from*
the group cannot then select the group. Closing this route would need a $\mathbb Z_3$ derived from
BCC/$O_h$ structure with no reference to the colour group at all — the tree does not have one, and
F293 names this as the single most promising remaining lead.

### 13a.3.2 The selector that works, and its audited fragility (F293, F294)

**The one fact that makes a selector possible at all.** The model derives its bare colour coupling
($g_s=\tfrac12$, from F144's chain via the F110 C7 matrix identity $\chi=1/(4g_s^2)$) with **no
$N_c$-dependence anywhere in the derivation** — no Casimir, no adjoint dimension. Dimensional
transmutation then makes the confinement *scale* $\Lambda$ depend on $N_c$ **exponentially** through
the one-loop $\beta$-function coefficient $\beta_0=(11N_c-2n_f)/3$:

| $N_c$ | $\Lambda$ (GeV) |
|---:|---:|
| 2 | $1.3\times10^{-23}$ |
| **3** | $\mathbf{4.7\times10^{-2}}$ |
| 4 | $2.6\times10^{5}$ |
| 5 | $5.0\times10^{8}$ |

A span of **28.3 orders of magnitude** across $N_c=2\ldots4$, of which only $N_c=3$ lands anywhere near
the observed hadronic scale of a few hundred MeV. Inverting the one-loop running against the measured
$\alpha_s(M_Z)=0.1180$ gives $N_c=2.998$ ($2.995$ with the top threshold), the nearest integer by a wide
margin ($N_c=2$ gives $\alpha_s(M_Z)=0.033$, roughly $0.28\times$ the measured value; $N_c\ge4$ puts the
Landau pole above $M_Z$ entirely).

**The circularity, audited rather than hidden.** Of the selector's three inputs, only the extraction
of $\alpha_s(M_Z)_\text{PDG}$ is $N_c$-dependent (every determination is made *inside* QCD with
$N_c=3$ already assumed); the bare coupling $\alpha_s(\mu_0)=1/(16\pi)$ and the scale $\mu_0=\hbar c/a$
carry no $N_c$. This is why the 28-decade scale argument, not the precise $N_c=2.998$, is treated as
the headline: it needs only "hadrons exist at a scale of order a GeV," not a circular extraction.

**F294's audit cuts both ways.** F293's premise — that the F110 C7 identity $\chi=1/(4g_s^2)$ carries
no $N_c$ — is confirmed **exactly** by direct measurement across seven groups ($\mathbb Z_2$ through
$\mathbb Z_9$ and $U(1)$; worst deviation literally $0.0$), upgrading it from a reading of the
derivation's text to a computed fact. But the selector's fragility is worse than F293's own falsifier
stated: under the *alternative*, physically-motivated reading (matching the rotor's electric term
against a genuine $SU(N)$ link's **Casimir**, rather than the implemented $\mathbb Z_N$/$U(1)$ centre),
the selector returns $N_c=1.28$ (fundamental Casimir matching) or has **no solution at all** (adjoint
matching) — not a $25\%$ shift, a collapse. F294 names the deciding computation ("build the $SU(N)$
Casimir ladder that F110 deferred, and re-run C7 against it") as the sharpest open item in the sector.

$$\boxed{\;\text{R13a.4 — anomalies cannot select }N_c\text{ (circular here); colour}\ne\text{the spatial 3 (excluded); the }\mathbb Z_3\text{ centre route is circular as built; a 28.3-decade confinement-scale lever selects }N_c=3\text{ empirically, exactly (}N\text{-free) on one reading and destroyed on another, unvalidated reading}\;}\tag{R13a.4}$$

(F293: 15/15 PASS, `CL257`, `status: narrowed`, `exactness: bracketed`, `falsifier: stated`. F294:
folded into the F293 gate record as checks B6/B6b.)

### 13a.3.3 The bracket closes to $\{3\}$, then reopens to odd $N_c\ne1$ (F324, F325)

**F324 (2026-08-17) closes the interval to a single value**, using no measured number and no
three-constituent baryon. Two independent constraints:

- **Lower — the Witten $SU(2)_L$ global anomaly.** $\pi_4(SU(2))=\mathbb Z_2$: an $SU(2)$ gauge theory
  with an odd number of Weyl isospin-$\tfrac12$ doublets has no well-defined path integral (Witten
  1982; the specific conclusion "$N_c$ must be odd in the standard model" is prior art, Bär & Wiese
  2001). Evaluated on the model's own derived $SU(2)_L$ content ($D_\text{gen}=N_c+1$ doublets per
  generation), the constraint bites: $D$ is odd (hence the constraint satisfied) exactly for $N_c$
  even, is **even** (hence violated) for $N_c$ odd $\Rightarrow$ excludes even $N_c$. It rests on six
  named premises (odd generation count parity, the colour sector's existence, the $\mathbb Z_{N_c}$
  rotor-modulus identification, quarks in the defining representation, one lepton doublet per
  generation, no fermion doubling) — booked explicitly, not hidden, and it bites specifically because
  $SU(2)_L$ is chiral (F27): pairing every doublet with a mirror makes it vacuous.
- **Upper — F298's C7 support.** F298's criterion (a level-independent $\chi_k$ existing across the
  $k$-string tower) has non-trivial support only at $N=\{2,3\}$ over the scanned range.

$$\{2,3\}\cap\{\text{odd},\ne1\}=\{3\}.$$

**F325 (the next day) withdraws the upper leg.** The apparent "X1" inconsistency — two adopted
$g_s$ values six decades apart, one from F144's rule-circularity chain and one from a Casimir-scaling
reading of the same C7 identity — is resolved: the $C_F$ that the "mixed" evaluation needs exists only
by matching two different operators' spectra (the model's own integer $\hat E^2$ ladder against an
$SU(N)$ link's Casimir ladder), and **both self-consistent evaluations give $\chi=1/(4g^2)$ for every
$N$ and every irrep**. F110's C1 already verifies, to machine precision, that the F101 rotor **is**
the F110 link Hamiltonian restricted to one plaquette's Gauss sector — one operator in two notations,
whose brackets cancel identically. F325 corroborates this on two independent legs (a quantitative
exclusion of the Casimir branch against the model's own $d_1$-derived bracket, $5.63$ decades outside
it; and a full audit of the C7 identity's magnetic side against a genuine $SU(N)$ Hamiltonian,
`su3_ladder.py`/F111b, closing the identity's one previously-unchecked half). **CN19 — "the C7 identity
is well-defined only for $N_c\le3$" — falls**, and F324's upper constraint falls with it.

$$\{N_c\text{ odd},\ N_c\ne1\}=\{3,5,7,9,11,\ldots\}$$

is the bracket that survives, with $N_c=3$ favoured empirically (§13a.3.2's 28-decade lever) and by
nothing structural.

$$\boxed{\;\text{R13a.5 — the Witten }SU(2)_L\text{ global anomaly paired with an (initially believed, later withdrawn) C7 upper bound closes the interval to }\{3\}\text{; resolving the X1 colour-normalisation fork in favour of the centre reading withdraws the upper bound, reopening the bracket to odd }N_c\ne1\;}\tag{R13a.5}$$

(F324: 14/14 PASS in an isolated harness — explicitly **not** run through `make gate` at write time,
flagged honestly in the finding's own §11 as "physics verified, tree-unverified." F325: 7/7 PASS, both
controls verified red only where declared. `CL281`, `status: narrowed`; `CL257` re-narrowed to match;
`CL282` records the Casimir branch's exclusion specifically, `status: live`, `kind: no_go`.)

### 13a.3.4 The bracket does not narrow further (F338)

F338 (2026-08-31) checks whether anything closes the reopened bracket back down. Three previously-open
avenues are examined:

- **A colour-native $\pi_4$ anomaly.** Closed by citation: $\pi_4(SU(N))=0$ identically for every
  $N\ge3$ (Bott 1959); only $SU(2)$ carries the non-trivial class. The colour group cannot supply a
  second, independent global-anomaly constraint at any $N_c\ge3$.
- **An exact elementary count.** The model's per-generation Weyl-fermion content is exactly
  $4(N_c+1)$, which equals **16 precisely at $N_c=3$** — matching the Standard Model's well-known
  16-Weyl-fermions-per-generation figure. This is elementary arithmetic with no topological content by
  itself.
- **A flagged, explicitly unverified mod-16 lead.** *If* the Dai-Freed/Pin$^+$ bordism condition behind
  the Standard Model's "total count $\equiv0\pmod{16}$" (García-Etxebarria & Montero; Wang) generalises
  as a bare fermion-count condition to this model's arbitrary-$N_c$ content, the bracket would narrow
  to $N_c\equiv3\pmod4$, i.e. $\{3,7,11,15,\ldots\}$. **This is not verified**: the invariant's actual
  generator ($X=5(B-L)-4Y$) has fixed coefficients derived *for* $N_c=3$, and nothing in the source
  literature is shown to generalise it. Recorded as a flagged coincidence, explicitly excluded from the
  finding's own pass tally.

An external literature cross-check (Bär & Wiese 2001; Tanizaki 2018; a review of the $\pi^0\to2\gamma$
"number of colours" argument) confirms that **no further theoretical $N_c$ selector exists in the
general, non-lattice chiral-gauge-theory literature either** — the residual this model carries is
generic to any theory of this shape, not a lattice-specific shortfall.

$$\boxed{\;\text{R13a.6 — the odd-}N_c\ne1\text{ bracket does not narrow further with currently-verified methods; a well-defined but unverified mod-16 lead could narrow it to }\{3,7,11,15,\ldots\}\text{ if its physical premise generalises; the residual is confirmed generic to the class of theory, not a defect of this construction}\;}\tag{R13a.6}$$

(F338: 4/4 PASS — explicitly disclosed as certifying code correctness only, not G3's physics, per the
finding's own self-correction on review. No claim card issued.)

### 13a.3.5 Why an internal index must exist at all — narrowed to two named facts, and shown irreducible (F333, F381)

A separate and logically prior question to "which $N$": does an internal colour index need to exist at
all, i.e. is $N=1$ (no colour) actually excluded? F333 (2026-08-28) answers this without presupposing
$N_c=3$ anywhere in the argument.

**The generalised theorem (not F317 §6's fixed slice).** For $SU(N)$'s fundamental representation,
$\Lambda^k(\mathbb C^N)^{SU(N)}$ — the invariant subspace of the $k$-th antisymmetric power — is
1-dimensional exactly at $k=N$ and zero otherwise, computed (not quoted) as a genuine $(N,k)$ scan,
$N=1\ldots6$, $k=1\ldots4$, 24 pairs, 0 mismatches.

**Composite exchange statistics, computed.** A composite of $k$ identical spin-½ fermions is itself a
fermion under exchange iff $k$ is **odd** — verified by explicit permutation-signature computation
(`sympy.combinatorics`), not invoked as folklore.

**Combined: a quark-only colour singlet is fermionic iff $N$ is odd.** A colour-singlet baryon built
from valence quarks alone has, by the first result, exactly $k=N$ constituents; by the second, is a
fermion iff $N$ is odd. Checked against the observational fact that real baryons (the proton, the
neutron) **are** fermions: consistent only for odd $N$.

**$N=1$ is separately excluded by confinement.** $\dim\mathfrak{su}(N)=N^2-1$ is **exactly zero** at
$N=1$ — literally no possible gauge boson, hence no possible confining force — checked against the
observational fact that free fractional electric charge has never been detected (the historical
Greenberg/$\Delta^{++}$ motivation for colour, used here in the opposite logical direction: to
constrain $N$'s parity, not to fix $N=3$ given a known multiplicity).

$$\{N:\ N\text{ odd},\ N\ge2\}=\{3,5,7,9,11,\ldots\}$$

— matching F324/F325's post-X1 bracket **exactly**, reached from entirely independent premises
(representation theory and Fermi statistics, versus Witten's global anomaly), recorded honestly as "a
real but modest cross-check" rather than a striking coincidence, since "odd and $\ge2$" is a fairly
generic shape for a mod-2 constraint to take.

$$\boxed{\;\text{R13a.7 — an internal colour index must exist (}N\ne1\text{), given two named observational facts (real baryons are fermions; quarks are confined) combined with a genuinely generalised }SU(N)\text{ representation-theory theorem and a computed composite-statistics rule; the resulting odd-}N\text{ bracket matches F324/F325's independently, reached from disjoint premises}\;}\tag{R13a.7}$$

**F381 (2026-09-10) checks whether this reduces the premise count further, and finds it does not.**
The question: is "real baryons are fermions" — one of F333's two named premises — already latent in the
model's own *derived* spin–statistics connection (F289/F330, R4.4a–R4.4c), so that citing the proton's
observed statistics would be redundant with physics the tree already has? Answered by direct
computation, not assertion: a text/parameter-signature scan of both derivation modules finds **zero**
colour/composite-count tokens and **no parameter channel** through which a colour rank could even be
supplied (an in-memory-injection control confirms the scanner would catch a hit if one existed). The
reason is structural, not an oversight: F289/F330 force that a single spin-½ *constituent's* exchange
sign is $-1$; that fact alone is blind to $N$, while F333's own composite-parity rule genuinely
bifurcates on $N$ (verified fermionic/bosonic alternating for $N=2\ldots7$) — premise (a) is precisely
the missing evaluation that resolves which branch matches reality. The one apparent escape — importing
F324's separately-derived odd-$N_c$ result to discharge premise (a) as a corollary — is closed on two
independent legs: it is **circular** (F324's own second premise, read directly from its code, is "the
colour sector exists," presupposing what would be derived), and even setting circularity aside it
**costs more than it saves** (F324's own premise count is 6, against F333's 2 — a net increase of 4).

$$\boxed{\;\text{R13a.8 — "real baryons are fermions" is not derivable from the model's own spin-statistics theorem (F289/F330), which is blind to composite count; the one apparent substitute (F324's odd-}N_c\text{ chain) is both circular and more expensive; row B1 stays at two irreducible, named empirical premises}\;}\tag{R13a.8}$$

(F333: 6/6 PASS, `CL287`, `status: contingent`, rolls up to `CL272`. F381: 5/5 PASS, five controls each
red only where declared, `claim: none` — a negative closure result, not a new physics assertion, so it
issues no card per D12's bar.)

## 13a.4 The derivation — Group C: the confinement mechanism

This is the chapter's centrepiece: an explicit, multi-route derivation of *why* the resulting $SU(3)$
Yang–Mills theory with quarks confines — not a citation of lattice-QCD folklore, and not an assumption.

### 13a.4.1 The exact 2D anchor: confinement as a genuine model prediction (F70)

Before any dynamics, F70 supplies a rigorous, exactly-solvable testbed. In two Euclidean dimensions,
after gauge-fixing to axial gauge, the plaquette variables of an $SU(N)$ lattice gauge theory are
**independent** (Schur's lemma), so a Wilson loop enclosing area $A=R\cdot T$ has
$\langle\tfrac1N\mathrm{Re}\,\mathrm{Tr}\,W\rangle=w(\beta)^A$ **exactly**, giving

$$\sigma(\beta)=-\ln w(\beta)>0\quad\text{for every finite }\beta,\qquad V(R)=\sigma R,$$

computed by Weyl-torus quadrature to $3\times10^{-17}$. The Creutz ratio $\chi(R,T)=\sigma$ is
independent of $(R,T)$ to $2.2\times10^{-16}$ — the cleanest possible confinement signature, since the
area-difference of the four loops defining it is always exactly one plaquette. Representative
values: $\sigma(\beta{=}0.25,\ldots,20)=4.256,\ldots,0.219$, strictly positive at every coupling. A
companion Wilson gradient-flow/cooling driver is built and certified (gauge-covariant to $7.8\times
10^{-15}$, action-monotone, diffusive with decay rate $\propto\hat k^2$ to $4.9\times10^{-10}$); running
it on a thermalised configuration shows confinement lives in the **disordered** ensemble and cooling
*dissolves* it ($\langle\text{plaq}\rangle:0.070\to0.962$, $\sigma_\text{eff}:2.66\to0.039$) — a smoother,
not a confiner, and the reason the static-potential measurement itself uses the unflowed ensemble.

$$\boxed{\;\text{R13a.9 — in 2D, }SU(3)\text{ lattice gauge theory confines at every finite coupling, exactly (Schur factorisation, machine-precision Creutz ratio); this is the first point at which the model }\textit{predicts}\text{ confinement rather than merely being compatible with it}\;}\tag{R13a.9}$$

(F70: 14/14 PASS (6+8), `CL067`, `falsifier: unset`.)

### 13a.4.2 Confinement as a colour-dielectric dual superconductor (F86)

The 3+1D mechanism, in the model's own rotation-rate language, is the **dual Meissner effect**: the
QCD vacuum is a colour-magnetic condensate that, by dual superconductivity, expels colour-*electric*
flux, squeezing a $q\bar q$ pair's field into a fixed-energy-per-length tube. Read as a colour-
dielectric $\varepsilon_c(x)$ renormalising the gluon $(\mathbf E,\mathbf B)$ rotation rule — the exact
structural parallel of Chapter 18's gravitational dielectric $K(x)$, but in the **opposite impedance
regime**:

| | gravity dielectric ($K$) | confining dielectric ($\varepsilon_c$) |
|---|---|---|
| impedance | matched, $AB\equiv1$ | broken, $\varepsilon_c$ alone |
| effect | transparent — bends light | opaque — expels colour-electric flux |
| consequence | lensing, redshift | flux tube, linear $V(R)$ |

At the critical (BPS) coupling the Abrikosov–Nielsen–Olesen vortex energy completes exactly to a sum of
squares plus a topological boundary term (verified in exact `sympy` symbolic arithmetic, not machine
precision), giving the profile-independent

$$\sigma_\text{BPS}=2\pi v^2n\qquad\text{(exact)},$$

with $v$ the condensate VEV. A trivial dielectric reduces the gluon step to the free even-law
propagator bit-for-bit; a non-trivial $\varepsilon_c$ rescales $\Omega\to\Omega/\sqrt{\varepsilon_c}$
— as $\varepsilon_c\to0$ the rotation freezes and the colour field cannot propagate into the condensed
vacuum, which **is** confinement in this chapter's rotation-rate reading of $c$ (CLAUDE.md Core Design
Decision 2). The colour-magnetic condensate itself is, at this point, an **input**, flagged explicitly
as the construction's one research risk.

$$\boxed{\;\text{R13a.10 — given a colour-magnetic condensate, the model's own rotation-rate dielectric mechanism (the F64 gravity template, opposite impedance regime) reproduces the exact BPS flux-tube tension }\sigma=2\pi v^2n\text{ and expresses confinement as the freezing of the gluon rotation rate}\;}\tag{R13a.10}$$

(F86: 6/6 PASS, `CL081`, `falsifier: unset`.)

### 13a.4.3 The condensate is derived, not assumed (F88)

F86's one flagged research risk is closed the same day it was flagged. F88 derives the condensate from
two independent directions, using only ingredients the model already has:

**Route 1 — the trivial vacuum is unstable, forced.** Linearising the full Yang–Mills equation of
motion around a constant chromomagnetic background, the charged gluon with spin aligned along the
field is an exact growing mode, $\gamma^2=+gB$ (verified symbolically, all 12 EOM components closing
exactly; a charged-scalar control on the identical background is stable, $\omega^2=+gB>0$ — isolating
the anomalous chromomagnetic moment generated by $\epsilon^{abc}$, the same structure constants F43
implements, as the specific source of the instability). Hurwitz-zeta regularisation of the resulting
Landau tower gives a one-loop effective potential with the exact asymptotic-freedom log coefficient and
a closed-form minimum $B_\text{min}>0$ **for every coupling $g>0$** — the trivial vacuum is never the
ground state. In the model's rotation-rate language: this mode's $\Omega^2<0$ means it does not
rotate, it grows, and "a vacuum whose rotation rule cannot rotate is not the vacuum."

**Route 2 — what condenses is identified.** The model's link variables are compact group elements *by
construction*, so magnetic monopoles exist automatically, with no added ingredient — verified as exact
integer, gauge-invariant charges via the DeGrand–Toussaint construction on the model's own compact
links. Two exact duality identities (Villain/Poisson; the Coulomb-gas-to-sine-Gordon Gaussian identity,
both to machine precision) turn the resulting monopole gas into a dual sine-Gordon theory whose Debye
mass is the dual Meissner mass, with $z>0\Rightarrow m_D>0\Rightarrow\sigma>0$ — no adjustable input.
The model's own SU(3) links (Cartan-projected) carry these monopoles at measured non-zero density; a
compact-U(1) Monte Carlo hands back the condensate VEV as a **measured**, not assumed, quantity
($v=m_D/e=0.713$ at a representative coupling).

$$\boxed{\;\text{R13a.11 — the colour-magnetic condensate is forced (the trivial vacuum decays for every gauge coupling, via the same structure constants that generate the gluon self-coupling) and identified (compact links automatically carry monopoles, whose dual-Meissner screening supplies F86's VEV as a measured, not assumed, quantity)}\;}\tag{R13a.11}$$

(F88: 8/8 PASS, `CL083`, `falsifier: unset`. The finding is explicit that the Savvidy state itself is
not the final vacuum — the true ground state is a disordered condensate of domains, which is exactly
what F86 parametrises phenomenologically as $\varepsilon_c(x)$, not a detailed structure this finding
resolves.)

### 13a.4.4 The string tension as a centre-algebra identity, exactly (F99, F100, F101, F102)

The dielectric picture (§§13a.4.2–13a.4.3) is a mechanism; this sub-chain derives $\sigma$ **from the
rule's own centre algebra**, closing the loop F97/F98 had left open (*"the Lagrange statement is
structural... not yet a derivation of $\sigma$ as the multiplier inside the QCA update rule"*).

**F99 — $\sigma$ *is* the centre-twist Lagrange multiplier, exactly.** The rule is centre-covariant: a
$\mathbb Z_N$ centre transform on one time-slice's temporal links sends every Polyakov loop
$P\to zP$ while leaving contractible Wilson loops invariant (verified on real SU(3) links to
$5\times10^{-16}$). Projecting the plaquette holonomy onto its centre sector gives, in the F70 2D
testbed, $\langle W_k\rangle=s_k^A$ exactly, $\sigma_k=-\ln s_k$ — the $\mathbb Z_N$ analogue of F70's
own law, with $\sigma_0=0$ (closure costs nothing) and $\sigma_k>0$ off closure, proven symbolically. A
source of N-ality $k$ is equivalent to a centre twist $\theta_k=2\pi k/N$; stationarity of the twisted
free energy shows $\theta$ *is* the multiplier conjugate to the centre charge, and its value at
$c=k$ is exactly $\sigma_k$ — not merely analogous to a Lagrange multiplier, an identity. F99 also
re-derives F70's own SU(3) table from this centre-projection law and recovers F86's $\sigma=2\pi v^2n$
as the small-$\sigma$/Abelian-BPS linearisation of the same centre free energy.

**F100 — the centre disorder $\gamma$ is a closed-form functional of the rule's dispersion.** The
rule's rotation tick is exactly a harmonic-oscillator phase rotation; Wick-rotating gives a transfer
operator whose ground state has the standard per-mode flux moment $\langle\phi^2\rangle=1/(2\Omega)$
(verified to $3\times10^{-16}$). Summing over the Brillouin zone (convergent, Richardson-extrapolated)
gives the vacuum flux variance as a BZ average of the inverse rotation rate,
$\sigma_1=\tfrac14\langle1/\Omega(\mathbf k)\rangle_\text{BZ}$, and inverting F99's clock-weight relation
against this gives the closed-form map $\gamma(\Omega)$. **The headline:** confinement's scale and the
propagation speed are two faces of one dispersion — $c_\text{lat}$ is $\Omega$'s *slope* at $k\to0$
(Chapter 6); $\sigma_1$ is $\Omega$'s *inverse average* over the zone. A rule that propagates fast
confines weakly; a slow rule confines strongly.

**F101 — extended to all couplings via the compact rotor, non-perturbatively.** F100's construction
treats the plaquette flux as a non-compact Gaussian variable, missing exactly the compactness that
dominates the strong-coupling regime where confinement actually lives. Keeping the same transfer
operator but **compact** — the quantum (Mathieu) rotor $H=\tfrac1{2\chi}\hat E^2-\lambda\cos\hat\phi$ —
solves $\sigma(\lambda)=-\ln\langle e^{i\phi}\rangle$ exactly at all couplings (dense diagonalisation,
truncation-converged to $4\times10^{-16}$). The weak-coupling limit reproduces F100's Gaussian result;
the strong-coupling limit gives the genuine **non-perturbative logarithmic area law**,
$\sigma_1\to-\ln(2\lambda\chi)\to\infty$ — compactness is the whole mechanism here. The strong-coupling
slope matches F70's SU(3) law exactly (both $\to-1$ in $\ln(\text{coupling})$), and F70's own leading
plaquette-weight coefficient reproduces the exact SU(3) group-theory value $\beta/(2N^2)=\beta/18$ to
five figures.

**F102 — the crossover survives genuine multi-plaquette coupling.** Exact diagonalisation of coupled
$\mathbb Z_3$ rotors (open strips, $P=1,2,3$ plaquettes, Lanczos validated against dense ED to
$2.7\times10^{-14}$) confirms: at strong coupling, plaquettes **decouple** (curves for different $P$
coincide to $2\times10^{-6}$), so F101's single-rotor result and F70's independent-plaquette area law
are exact there; the universal logarithmic slope ($-1.0$ to $-1.03$) survives coupling unchanged; and
the only genuinely new effect of coupling is a finite $O(1)$ Wilson-loop prefactor plus a
weak-coupling ordering that *grows with $P$* — the finite-size precursor of the true deconfinement
transition. Coupling sharpens the crossover rather than washing it out.

$$\boxed{\;\text{R13a.12 — the string tension is exactly the Lagrange multiplier conjugate to }\mathbb Z_N\text{ centre-phase non-closure (F99), its disorder parameter is a closed-form Brillouin-zone average of the rule's own rotation rate (F100), the resulting Gaussian-to-logarithmic-confinement crossover is exact at all couplings for a single plaquette (F101, compact rotor) and survives genuine multi-plaquette coupling exactly (F102)}\;}\tag{R13a.12}$$

(F99: `CL091`. F100: `CL092`. F101: no separate card found in the checked slice above F102's
`CL094`, `status: live`, `falsifier: unset` for all four.)

### 13a.4.5 Real-time dynamics: the flux tube in motion, and the condensate wired into propagation (F110, F117)

Every result so far is either Euclidean (F70, F99–F102) or static energetics (F86). F110 builds the
first genuinely **real-time** confinement dynamics: the Kogut–Susskind Hamiltonian
$H=\tfrac{g^2}2\sum_\ell\hat E_\ell^2-\lambda\sum_p\cos\hat\phi_p$ is the exact multi-plaquette
generalisation of F101's single rotor (verified as a literal matrix identity, residual $0.0$ — the
rotor *is* the link Hamiltonian restricted to one plaquette's Gauss sector, the fact §13a.3.3 later
leans on to resolve X1). Gauss's law is **solved, not imposed**, via an exact dual height
representation (direct-vs-dual spectral identity confirmed to $1.9\times10^{-14}$ in vacuum and charged
sectors). The static potential is confirmed linear and positive at every tested coupling; and, the new
capability, real-time Krylov evolution (norm/energy drift $\sim10^{-14}$) shows a bare flux string
**persists** as a positive electric-energy excess under confining coupling (time-averaged, roughly
double the uniform share) while it **melts below the vacuum fluctuation level** at weak coupling —
confinement versus dissolution watched directly in time evolution, not inferred from a static energy.

F117 then wires F88's derived condensate into this dynamical propagator: one measured number — the
condensate VEV $v$ — simultaneously fixes the colour-dielectric $\varepsilon_c(x)$, the dual-Meissner
gluon mass $m_V=ev=m_D$, the screening length $\lambda=1/m_V$, and (through $\sigma=2\pi v^2$) the
tension — not three separate inputs but three faces of the one gap, all reductions bit-for-bit exact
at $\varepsilon_c=1$/$m_V=0$ and confirmed entirely on the now-canonical **even** gluon law (no
contradiction with §13a.2.2's forcing result).

$$\boxed{\;\text{R13a.13 — Gauss's law is exact by construction in a real-time link Hamiltonian that is literally the F101 rotor's multi-plaquette generalisation; the resulting flux tube persists under confining coupling and melts under weak coupling in genuine time evolution; a single measured condensate VEV simultaneously fixes the dielectric, the gluon mass gap, the screening length, and the string tension}\;}\tag{R13a.13}$$

(F110: `CL006`'s primary evidence for the 3+1D half, `status: narrowed`. F117: `CL104`, `falsifier:
unset`.)

### 13a.4.6 The real-space baryon: scalar confinement, not vector — and why (F135b, F137, F139)

A separate, complementary chain asks the question in real space: does a confining potential actually
bind a real-time Dirac constituent into a stationary baryon, and what *kind* of potential (in the
Dirac-equation sense) does the job?

**F135b — the decisive mechanism is a Lorentz-scalar mass, not a vector potential, and the reason is
the Klein paradox.** A **vector** (time-component) linear potential — the naive phase-kick reading of
"potential energy" — does **not** bind a light relativistic fermion: a steep vector step is
transparent by the Klein paradox (pair production/transmission), confirmed directly (a vector phase
kick of any $\sigma$ leaves the dispersion identical to free). A **Lorentz-scalar** linear potential —
added to the *mass*, $m_\text{eff}(x)=m+\sigma|x-R_\text{cm}|$ — does bind, because a position-dependent
mass has no Klein transmission channel (the gap grows with $r$, excluding the wavefunction). This is
precisely the MIT-bag mechanism, and it is precisely **F86 read in the quark's own frame**: the
colour dielectric $\varepsilon_c\to0$ in the condensed vacuum means an effectively infinite mass
outside the flux tube — the bag wall *is* the scalar confining mass. Three massive Dirac constituents
confined this way plateau at a stationary cluster RMS ($\approx3.7$, 300 ticks) while an identical free
control disperses to box saturation; the vector-mode control reproduces free dispersal within $15\%$,
confirming the Klein-tunnelling prediction directly.

**F137 — the confining field made live.** The scalar bag of F135b is promoted from a posited geometric
profile to a field **sourced dynamically by the quarks' own colour charge** — the F86 mechanism
realised in real time: $\rho(x)=\sum\|J_\text{colour}(x)\|$, $\phi=G_\lambda*\rho$,
$f^2=e^{-\phi/\phi_0}$, $S(x)=M_\text{bag}f^2(x)$, $\varepsilon_c=1-f^2$. The condensate melts where
colour charge sits and stays full in the vacuum; the resulting cluster binds *more* tightly than the
geometric string ($\text{RMS}\approx2.95$ vs $3.7$). For two static charges the condensate melts into a
connected channel with an approximately linear energy-versus-separation law over $R\lesssim4\lambda$ —
the F86 flux-tube signature realised dynamically. **A disclosed caveat, not swept aside**: the same
self-sourced mechanism also self-traps a **single, isolated** colour charge, which should not exist as
a stable object under genuine $\mathbb Z_3$ singlet confinement. This is honestly named as generic
scalar self-trapping (MIT-bag physics), not a derivation of centre-closure selection — that remains
F97/F99's job (§13a.4.4), and the confinement *scale* here is still imported ($M_\text{bag}$, $\phi_0$,
$\lambda$), not generated from the gauge sector's own dynamics.

**F139 — the mean-field limitation is cured by a genuine self-consistent back-reaction.** F137's fixed
smear $\lambda$ makes the flux tube pinch off beyond $\sim2\lambda$ — an artefact, not physics. F139
implements the full dual-Ginzburg–Landau coupled system: the condensate $f(x)$ and the colour-electric
displacement $\mathbf D^a$ (fixed by a **dielectric** Gauss law, $\nabla\cdot(\varepsilon_c\nabla\psi^a)
=-\rho^a$) are solved to **mutual** consistency — the flux the condensate confines is what melts the
condensate, closing the loop. The coupled iteration converges to a genuine fixed point (residual
$9.5\times10^{-7}$, 313 iterations); the pinch-off is cured (self-consistent tube stays connected,
$\varepsilon_c^\text{mid}>0.97$, at separations where the mean-field version had collapsed to $0.12$);
and the resulting bag energy is linear in $R$ with an $R$-independent tension to within a factor $1.23$
— the dynamical realisation of a genuine flux tube, cured of its earlier finite-range artefact.

$$\boxed{\;\text{R13a.14 — the confining potential a real-time Dirac baryon actually needs is Lorentz-scalar, not vector (the Klein paradox excludes the vector reading); this scalar bag can be made live (self-sourced by the quarks' own colour charge, F137) and self-consistent (mutual condensate}\leftrightarrow\text{flux back-reaction, F139, curing the mean-field pinch-off) — but the self-sourced mean-field version alone also self-traps an isolated colour charge, a disclosed limitation distinct from genuine singlet-selection physics}\;}\tag{R13a.14}$$

(F135b: `CL121`, `falsifier: unset`. F137: `CL123`, `exactness: machine`. F139: `CL124`, `exactness:
exact`.)

### 13a.4.7 A proved no-go: the dielectric tube cannot reach the exact topological tension (F142)

F139 left two threads explicitly open. F142 attacks both and answers with a sharp no-go on the first
and a scope theorem on the second — the honest boundary of what the real-space dielectric picture can
and cannot deliver exactly.

**Q1 — can the F139 dielectric tube be mapped onto $\sigma=2\pi v^2n$ with algebraic exactness? No.**
The dual-superconductor dictionary reproduces the correct **scaling** but with the wrong prefactor
($\sigma_\text{FL}=\tfrac1{\sqrt2}(2\pi v^2n)$, not $2\pi v^2n$ — exact algebra, not an approximation).
Worse: a direct "spread-thin" analysis of the continuum $\varepsilon_c=1-f^2$ functional shows the
tension **is not bounded below at all** — $\sigma_\text{spread}\propto A^{-1/3}\to0$ as the flux spreads
over a growing transverse area, confirmed both analytically (decade ratio $10^{1/3}$ to machine
precision) and by direct gradient-flow minimisation in a growing box ($\sigma(L)$ falls as $L^{-2/3}$,
matching to $<2\%$). **F139's apparent "constant tension to a factor 1.23" is therefore a regulator
artefact of its finite box and dielectric floor, not a genuine confining functional** — stated plainly,
not softened. The structural reason: $\sigma=2\pi v^2n$ is the *topological* charge of a magnetic
vortex whose phase winds $n$ times, pinning the field at infinity; F139's electric tube carries its
flux as a source charge with **no winding**, so nothing pins it and the spreading mode is open. **The
exact map to $2\pi v^2n$ already exists, and it does not run through the dielectric tube at all**: it
is F99's centre-Lagrange-multiplier identity (§13a.4.4), whose small-$\sigma$/Abelian-BPS limit
reproduces $\sigma_k=2\pi v^2k$ *by construction*, as the linearisation of an exact centre free energy
— not as the saturated tension of any electric functional.

**Q2 — can the full non-Abelian condensate be solved in closed form? Only its centre content.** The
condensate's **existence** is forced (F88, N1 here); its **N-ality classification** is exact and
representation-/dimension-independent group theory ($\sigma_0=0$, $\sigma_k>0$ off closure,
$\sigma_k=\sigma_{N-k}$ — the $\mathbb Z_N$ centre algebra of the rule, N2); its **Casimir/$k$-string
ratios** are exact SU(3) group theory (N3–N4); and Abelian dominance (the fundamental flux is carried
by the Cartan subalgebra, off-diagonal gluons affecting the VEV magnitude but not the N-ality, N5)
legitimises the Cartan-projected approximation F86/F137/F139 actually use. What is **not** derivable in
closed form is the condensate's **dynamical magnitude** — the VEV $v$, the absolute 3+1D $\sigma$, and
which of the two candidate universal $k$-string laws (Casimir vs. sine) holds for $N\ge4$ (they
coincide, degenerately, at $SU(3)$) — this remains the genuine non-perturbative mass-gap problem, open
in this model exactly as it is in continuum QCD, and is the item `CL006` names as the reason its own
3+1D half is scoped as "mechanism plus cross-check," not "derivation."

$$\boxed{\;\text{R13a.15 — the real-space colour-dielectric flux tube (F86/F137/F139) cannot be mapped onto the exact topological tension }\sigma=2\pi v^2n\text{ (a proved obstruction: the continuum functional is unbounded below, and F139's apparent constant tension is a finite-box/floor regulator artefact); the exact map is F99's centre-algebra identity instead; the non-Abelian condensate is algebraically solvable only in its centre-projected content — existence, N-ality classification, and SU(3) Casimir ratios — with its dynamical magnitude remaining the open non-perturbative mass-gap problem}\;}\tag{R13a.15}$$

(F142: no dedicated claim card of its own found in the checked slice; its content is folded into
`CL006`'s own scoped statement, which names F142 explicitly among its four evidence findings.)

## 13a.5 The derivation — Group D: strong CP

**Placement note.** This finding sits at the boundary between the structural gauge-sector story of
this chapter and the loop-level machinery Chapter 13b develops in depth (the same rhombic BCC vertex
apparatus, `lpt_bcc_vertex`, that Chapter 13b's $d_1$/scheme-conversion saga uses extensively). It is
kept here, per the plan's assignment, because its central content — a structural, non-perturbative
theorem about the rule's own loop set, not a numerical extraction — is qualitative in exactly this
chapter's sense; findings that *use* the same vertex apparatus for quantitative running-coupling work
belong to Chapter 13b.

F321 answers completeness row **B11**, first correcting its own prior mis-attribution: the row's
tree-level "$3.3\times10^{-16}$" residual was F53's measurement of the *unrelated* F27 complex-mass
phase, not any statement about the gluon sector's $\theta$ — F53 itself says explicitly that strong CP
"is a separate phase in the gluon sector, untouched here." The actual content:

**In Euclidean signature, the $\theta$-term is the unique purely imaginary gauge invariant** — the path
weight is $e^{-S_\text{YM}+i\theta Q}$ — so "the rule's action is real" and "the rule contains no
$\theta$-term" are the same statement. The model's minimal gauge loop is the 4-bond BCC rhombus, and
its 20 oriented minimal loops (6 spatial $\times2$, 4 temporal $\times2$) are **closed under reversal**
by explicit combinatorial enumeration — the load-bearing structural fact. Consequently, on genuinely
disordered Haar-random SU(3) configurations (99.7% disorder), the action's imaginary part is $1.2\times
10^{-14}$ — not merely small, but demonstrably sensitive (injecting a hand-set $\theta$ gives
$\mathrm{Im}\,S=-\theta\sum Q$ *exactly*, confirming the zero measured is a genuine null result, not an
insensitive probe). Independently, every vertex coefficient of the rule's own action (2-, 3-, and
4-point, colour indices sampled) is real at **literal `0.0`** — including the 3-point (triple-gluon)
vertex the 2026-06-29 audit specifically flagged as unanalysed for exactly this question. Because the
class of momentum-space functions obeying $V(-k)=\overline{V(k)}$ is closed under products and under
symmetric-measure loop integration, **no loop at any order can generate an imaginary part** — the
audit's open item is closed by a closure property of the rule's loop set, not diagram by diagram.

**The fermion side.** The physical invariant is $\bar\theta=\theta_\text{QCD}+\arg\det M_q$. At one
generation, $\arg\det M_q$ (correcting how F53's number is usually quoted: the *determinant* of the
off-diagonal $2\times2$ mass matrix is $+m^2$, not $-m^2$) is exactly $0$, independent of the F27 phase
— so $\bar\theta=0$ closes exactly at one generation, from two logically separate sources: $\theta_
\text{QCD}$ from the loop-set argument above, $\arg\det M_q$ from the mass-matrix structure. At three
generations $\arg\det M_q$ depends on the full quark-mass texture (open-derivations E6/E7) and is
**not** closed by this finding.

**What honestly remains open**, named rather than hidden: (i) the model's own action carries a
documented fork between the F26 rotation law and the rhombic plaquette action, which agree in the
continuum and disagree at finite momentum without a stated resolution — the theorem is checked to
survive *both* branches (the retained chiral branch is P-odd but excluded on other grounds; the
canonical even branch is P-even, consistent with F91/F317's forced classification, §13a.2.2), but
"survives both branches" is weaker than "derived on the settled branch"; (ii) the argument is
configuration-by-configuration (non-perturbative, §"reality non-perturbatively") and all-orders
perturbative (§"reality perturbatively") separately, but does not address whether the rule's Hilbert
space carries distinct $\theta$-vacua a real action could still select between; (iii) the naive
continuum expectation that the field-strength dot product $\mathbf E\cdot\mathbf B$ is P-odd is
**measured false** at finite lattice spacing for the reconstructed rhombic clover (a genuine, disclosed
defect the finding records rather than quietly avoids by using it), so every load-bearing leg instead
rests on the $U\to U^*$/reality argument, not naive parity.

$$\boxed{\;\text{R13a.16 — }\theta_\text{QCD}=0\text{ is a theorem of the rule's minimal-loop set being closed under reversal, non-perturbatively measured and all-orders perturbatively proved by a closure property; }\bar\theta=0\text{ closes exactly at one generation via an independent mass-matrix argument; the strong-CP question is a genuinely reduced parameter count (one input removed) not a value prediction, and remains open at three generations pending the quark mass texture}\;}\tag{R13a.16}$$

(F321: 20/20 PASS, 5 at literal `0.0`, 3 controls each reddening disjoint leg sets. `CL278`, `status:
live`, `falsifier: stated` — three named computational kills, no observational falsifier since a
neutron-EDM bound constrains $\bar\theta$, not $\theta$, a distinct claim card's subject.)

## 13a.6 Results table

| # | Statement | Status | Exactness | Source |
|---|---|---|---|---|
| R13a.1 | Colour's unitarity, specialness, locality⇒connection, and vector-like coupling are all forced given one internal index; the index's bare existence is not | forced (5 of 6 legs) + 1 input | exact | F317, 21/21 |
| R13a.2 | The gluon's even propagation law is forced at every level (free, self-coupling, and its remaining premise); no W-style unresolved duality exists | forced, closed chain | exact | F91/S2, F166, F317 |
| R13a.3 | The dynamical SU(3) gluon sector is built and E2E-certified with a closed bidirectional fermion↔gluon back-reaction loop | built + certified | machine (best legs exact) | F43, F90 |
| R13a.4 | Three routes to selecting $N_c$ closed/circular; a 28.3-decade confinement-scale lever selects $N_c=3$ empirically, exactly N-free but fragile to an unvalidated translation hypothesis | empirical selector, audited fragile | bracketed | F293, F294 |
| R13a.5 | Witten anomaly + (withdrawn) C7 upper bound closes the bracket to $\{3\}$; resolving X1 in favour of the centre reading reopens it to odd $N_c\ne1$ | narrowed then reopened | exact (given premises) | F324, F325 |
| R13a.6 | The odd-$N_c\ne1$ bracket does not narrow further with verified methods; residual confirmed generic to the theory class | closed (negative result) | exact (citation) | F338 |
| R13a.7 | $N\ne1$ (an internal index must exist) given two named observational facts, reached independently of F324/F325's route and matching its bracket | derived, contingent on 2 premises | exact | F333 |
| R13a.8 | The "baryons are fermions" premise is not reducible to the model's own spin-statistics theorem; the one substitute is circular and costlier | closed (negative result) | exact | F381 |
| R13a.9 | 2D SU(3) lattice gauge theory confines at every finite coupling, exactly | exact theorem | exact/machine | F70 |
| R13a.10 | Given a condensate, the model's dielectric mechanism reproduces the exact BPS tension $\sigma=2\pi v^2n$ | derived given input | exact (BPS algebra) | F86 |
| R13a.11 | The colour-magnetic condensate is forced (every $g>0$) and its VEV is measured, not assumed | forced + measured | exact (forcing) / quantitative (VEV) | F88 |
| R13a.12 | $\sigma$ is exactly the centre-twist Lagrange multiplier; its disorder is a closed-form BZ average of $\Omega$; the Gaussian↔log crossover is exact at all couplings and survives multi-plaquette coupling | exact identity chain | exact / machine | F99, F100, F101, F102 |
| R13a.13 | Gauss's law is exact in a real-time link Hamiltonian; the flux tube persists/melts in genuine time evolution; one measured VEV fixes dielectric, mass gap, screening length, and tension together | built + dynamical | machine | F110, F117 |
| R13a.14 | Confinement of a real baryon needs a Lorentz-scalar potential (Klein paradox excludes vector); made live and self-consistent; the live version also self-traps a lone charge (disclosed limitation) | mechanism derived + built | quantitative | F135b, F137, F139 |
| R13a.15 | The dielectric flux tube cannot reach the exact topological tension (proved no-go); the exact map is the centre route instead; the non-Abelian condensate is exactly solvable only in centre content | no-go + scope theorem | exact (no-go) | F142 |
| R13a.16 | $\theta_\text{QCD}=0$ is a theorem of loop-set reversal-closure, non-perturbative and all-orders; $\bar\theta=0$ at one generation | theorem (one generation) | exact | F321 |

## 13a.7 Comparison with measurement

This chapter's comparisons are largely structural (does the mechanism reproduce the right qualitative
and scaling behaviour) rather than the precision numerical comparisons Chapter 13b's $\alpha_s$/scheme-
conversion material carries out. Two genuine quantitative comparisons belong here:

- **The confinement scale, order-of-magnitude.** §13a.3.2's $N_c$-selector, run at $N_c=3$, gives
  $\Lambda\approx4.7\times10^{-2}$ GeV — the right order of magnitude for the observed hadronic scale
  (a few hundred MeV), though not compared to a precision target here (that comparison, and the
  absolute scale-setting via $\sqrt\sigma/f_\pi$, is Chapter 17's job). What is checked at *this*
  chapter's level is the discriminating power: $N_c=2$ gives essentially no confinement scale at all
  ($10^{-23}$ GeV) and $N_c\ge4$ puts confinement above the electroweak scale — the comparison that
  makes $N_c=3$ a 28-decade-wide empirical selector, not a precision fit.
- **Real QCD's approximate Casimir scaling at intermediate distance.** F294 §5 names this honestly as
  the counterweight to the model's own adopted centre-dominant reading: real lattice QCD shows Casimir
  scaling of higher-representation string tensions at intermediate distance, with centre dominance only
  asymptotic, while the model's X1 resolution (§13a.3.3) adopts the pure centre reading throughout. This
  is recorded as an open tension between the model's normalisation choice and one qualitative feature of
  real lattice data, not resolved here.

No fermion mass, coupling-constant, or hadron-spectrum number is produced or compared at this chapter's
level — those are Chapter 13b (dynamical $\alpha_s$), Chapter 14 (hadrons), and Chapter 17 (SI
closure)'s territory, consuming this chapter's structural results as inputs.

## 13a.8 What was excluded, and why

- **The dielectric flux tube as the exact carrier of $\sigma=2\pi v^2n$** (F142, §13a.4.7). A proved
  no-go, not merely an unattempted route: the continuum electric-dielectric functional has no finite
  lower bound (flux spreads thin, $\sigma\propto A^{-1/3}\to0$), and F139's apparent success is a
  finite-box/dielectric-floor regulator artefact. The topological winding that makes $2\pi v^2n$ exact
  belongs to the *magnetic* vortex construction (F86), not the electric tube; the genuinely exact map
  to the same number runs through F99's centre algebra instead.
- **Anomaly cancellation as an $N_c$ selector** (F293 R1, §13a.3.1). Circular in this model specifically
  — unlike the Standard Model, $Y_Q$ is not independently fixed here, so the textbook argument has no
  foothold.
- **Colour identified with the three spatial axes** (F293 R2, §13a.3.1). Excluded by an explicit
  non-commutation measurement: an axis-identified colour would be visibly rotated by an ordinary
  lattice rotation.
- **The $\mathbb Z_3$-centre route to $N_c$, as the tree currently stands** (F293 R3, §13a.3.1).
  Circular — the $\mathbb Z_3$ is introduced *as* $SU(3)$'s own centre, so it cannot independently
  select the group. Named as the single most promising unclosed lead.
- **The Casimir-normalisation branch of the bare colour coupling** (F325, `CL282`, `kind: no_go`). Excluded
  on two independent legs — a structural argument (the $C_F$ the Casimir reading needs is a
  matching artefact between two different operators whose spectra genuinely differ) and a quantitative
  one ($5.63$ decades outside the model's own $d_1$-derived bracket) — in favour of the centre
  (branch B) reading. Full quantitative detail of this exclusion belongs to Chapter 13b.
- **A fundamental Higgs-style scalar for the colour-magnetic condensate.** Not separately argued against
  as an alternative in the sources read for this chapter — the condensate is instead *derived* (F88) as
  the forced ground state of the model's own Yang–Mills dynamics, making the question of an alternative
  input scalar moot rather than excluded by comparison.

## 13a.9 What is still open

- **Which integer $N_c$ carries, beyond "odd and $\ne1$."** The tightest structural statement this
  chapter reaches is $N_c\in\{3,5,7,9,11,\ldots\}$ (§13a.3.4, F338); $N_c=3$ is selected only
  empirically (§13a.3.2). The one well-defined, not-yet-executed computation that could narrow this
  further is verifying whether the Dai-Freed/Pin$^+$ mod-16 bordism condition's generator generalises
  to arbitrary $N_c$ in this model's own content (F338 §7 item 1).
- **The colour-magnetic condensate's dynamical magnitude in 3+1D** — the genuine non-perturbative
  mass-gap problem, open here exactly as in continuum QCD (F142 Q2, `CL006`'s own scope statement).
- **Whether the model's action-fork (F26 rotation law vs. rhombic plaquette action, disagreeing at
  finite momentum) is resolved**, which the strong-CP theorem currently sidesteps by checking both
  branches rather than presupposing one (§13a.5).
- **The finite-lattice-spacing parity eigenvalue of the reconstructed field-strength clover**, measured
  false where the continuum expectation ($\mathbf E\cdot\mathbf B$ P-odd) would naively apply (F321
  §7) — disclosed and worked around, not yet repaired.
- **F382's boundary call, stated explicitly.** F382 (2026-09-10) measures that the vertex-derived
  numerator in Chapter 13b's own $d_1$ loop-integral estimator does **not** share the propagator's exact
  invariance under the BCC reciprocal lattice (a genuine, previously-unmeasured $\sim220\%$ effect at
  tested points), and directly tests the natural remedy — integrating over the full reciprocal cube
  instead of the Wigner–Seitz quarter-cell — finding it makes the estimator's already-slow convergence
  **worse**, not better, corroborating (without extending) the domain choice Chapter 13b's own $d_1$
  machinery already uses. This finding's actual subject — a loop-integral convergence diagnostic for
  the dynamical strong-coupling estimator — belongs squarely to **Chapter 13b's** subject matter (the
  X1/$d_1$ saga), not to this chapter's structural/qualitative content; it is recorded here only because
  it is one of this chapter's 26 assigned findings, and the boundary call is made explicitly rather than
  forcing a technical loop-integral result into a chapter about colour structure and confinement
  mechanism. Chapter 13b should treat F382 as primary source material for its own $d_1$/vertex-
  machinery discussion.
- **The self-sourced flux tube's inability to distinguish generic self-trapping from genuine
  $\mathbb Z_3$-singlet selection** (F137's disclosed caveat, §13a.4.6) — the live/self-consistent bag
  mechanisms bind *any* colour-charge configuration, including an isolated single quark that should not
  exist as a stable object under true confinement; the actual singlet-selection physics remains
  F97/F99's centre-closure argument, not the real-space bag construction.

## 13a.10 Falsifiers

Most of this chapter's claim cards (`CL049`, `CL067`, `CL081`, `CL083`, `CL091`, `CL092`, `CL094`,
`CL104`, `CL121`, `CL123`, `CL124`) carry `falsifier: unset` — declared debt per D12's own vocabulary,
not a claim that no falsifier exists. The findings' own algebraic identities are, in every such case,
their own de facto falsifiers: a single measured counterexample to any of the boxed exact identities
above (R13a.9–R13a.13) would falsify the corresponding construction outright.

Where a falsifier **is** stated:

- **R13a.1/R13a.2 (`CL271`).** Any step of the rule found to read the colour index directly (the
  commutant control `rule_reads_colour=true` collapses $9\to3$); a colour representation other than a
  single fundamental per chirality; a right-handed $SU(2)_L$ doublet entering the model's content
  (removing the anomaly that forces vector-like colour); a stable colour-singlet with a constituent
  count other than three.
- **R13a.4/R13a.5 (`CL257`, `CL281`, `CL282`).** An improved measurement of $\alpha_s(M_Z)$ moving the
  selector's central value; a completed $SU(N)$ Casimir-ladder computation returning a value inside the
  Casimir branch's excluded region (this would reinstate branch A and CN19 with it); any $N\ge4$ at
  which the C7 identity is found to hold non-trivially.
- **R13a.7/R13a.8 (`CL287`).** A stable, quark-only bound state observed with an even number of
  valence constituents; the proton/neutron shown not to be fermions (neither remotely plausible, but
  the correct falsification target for the physical, as opposed to mathematical, content).
- **R13a.16 (`CL278`).** Exhibiting one SU(3) configuration with $\mathrm{Im}\,S\ne0$ at gate
  tolerance; exhibiting one vertex coefficient with nonzero imaginary part at any leg count or colour
  assignment; showing the rule's minimal-loop set is *not* reversal-closed (the load-bearing input, and
  the one the card itself names as least certain). No observational falsifier exists for
  $\theta_\text{QCD}$ itself, since a neutron-EDM bound constrains $\bar\theta$, a distinct claim.

No genuine gap was logged in `docs/monograph/GAPS.md` by this chapter. Chapter 12's Gap **G-7**
(the $W$-propagator-law duality) was checked directly against the gluon sector's actual chronology
(§13a.2.2) and found **not** to recur: F91, F166 and F317 together force the gluon's even law at every
level with no competing requirement, which is a resolution of the question G-7 raised for this
sector, not a new instance of it.
