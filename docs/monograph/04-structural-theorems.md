# Chapter 4 — Structural Theorems: Reflection Positivity, CPT, Spin–Statistics, Cluster Decomposition

*Chapter 4 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F53-fg9-C-CP-per-species.md`, `findings/F289-spin-statistics-connection.md`,
`findings/F290-cluster-decomposition-strict-cone.md`,
`findings/F328-discrete-cpt-theorem-free-bcc-dirac-walk.md`,
`findings/F330-belt-trick-residual-named-not-closed.md`,
`findings/F331-cluster-decomposition-interacting-3d.md`,
`findings/F335-reflection-positivity-bcc-lattice.md`,
`findings/F377-p1-independent-of-bdpt-axioms-aperiodic-falsification.md`,
`findings/F378-discrete-cpt-gauged-kinetic-theorem-mass-sector-no-go.md`,
`findings/F379-emergent-so3-wrong-kind-for-postulate-1.md`, and
`findings/F380-cluster-asymptotic-series-residual-named.md` — the eleven findings `00-plan.md` §2
assigns to this chapter, all read in full. Checked directly against `docs/theory/supersessions.yaml`
(none of the eleven appears in any of the 23 records) and against `claims-index.md`: CL255 (F289,
F330), CL256 (F290), CL285 (F328, F53, rolled up further by CL306), CL286 (F331, F290, F380),
CL289 (F335), CL306 (F378, rolls up to CL285) all rest on this chapter's findings and are reported
below with their exact `status`/`exactness` fields rather than the findings' own (sometimes more
confident) headlines. F377 and F379 have **no claim card at all** — checked directly (`grep -n
"F377\]" claims-index.md` and the same for F379 both return nothing) — and this chapter says so
plainly at the point each is used, per the finding-coverage rule ("a finding with no claim says so
too"). Notation, postulates and results are those of `docs/monograph/01-postulates-and-ontology.md`
and `docs/monograph/02-dimensions-and-lattice-selection.md` and
`docs/monograph/03-the-update-rule.md` — $\mathbf x$, $t$, $a$, $\psi$, $\sigma^i$, $A(\mathbf k)$,
$D(\mathbf k)$, $c_\text{lat}$, $d$, $O_h$/$D_{2h}$/$D_{4h}$ — extended, never redefined.*

## 4.0 What this chapter establishes

Chapters 2 and 3 built the concrete object — a single local, homogeneous, unitary BCC walk, iterated
— and characterized exactly how much continuous structure it does and does not carry at the lattice
scale (R2.12/R2.13: exact $D_{2h}$/$D_{4h}$, $O_h$ only in the infrared). This chapter asks whether
that object satisfies the general mathematical-physics theorems any respectable local, unitary,
relativistic-*ish* quantum theory is expected to satisfy — reflection positivity, CPT, the
spin–statistics connection, cluster decomposition — and, where it does, on what grounds: a genuine
theorem forced by the lattice's own algebra, a numerically-verified property with a stated residual,
or an open/partial result honestly still short of a theorem. The eleven findings assigned here do
not all land in the same place, and the chapter's central discipline is to keep those places
distinct rather than let the word "theorem" flatten them: **two are full, exact theorems for the
sectors they cover** (link reflection positivity for the gauge action, discrete CPT for the free
Dirac walk); **one is an exact theorem plus a proved companion no-go** (the free-sector CPT result
also proves ordinary parity cannot exist at finite lattice spacing); **one extends the CPT theorem
partway and proves a general obstruction to extending it further** (the gauged mass sector); **one is
a genuine derivation of a theorem's premises, not the theorem itself** (spin–statistics); **two are
honest non-closures with the failure diagnosed rather than left unexamined** (the belt-trick residual
and its hardening against a "bigger continuum limit" escape); **one sharpens a nearby but distinct
posit's status without closing it** (single-generator dynamics); **and three build out cluster
decomposition from a 1-D free exact result to a named, theoretically-anchored residual in the
interacting 3-D theory.** The chapter's results table (§4.4) carries an explicit status column for
exactly this reason.

## 4.1 Inputs

**Postulates used.** **P1** (discreteness) and **P4** (linearity, exact unitarity, the amplitude
treated as physically real) throughout — every result in this chapter is a statement about a
concrete unitary matrix or its consequences, never about a probability distribution over hidden
classical states. **P2** (locality) is what gives cluster decomposition and the strict causal cone
their content (§4.3.4): a theorem about signaling and correlation decay is only interesting because
the update genuinely has bounded support (R3.6). **P3** (homogeneity/isotropy) underlies the
CPT/parity discussion throughout §4.3.3, since the question "does a fixed unitary $\Pi$ implement
parity at every $\mathbf k$" only has the shape it has because the update is the same operator at
every site. **P5** (the primitive field is $\psi\in\mathbb C^2$, a Weyl spinor) fixes the object
every operator in this chapter — $\Theta$, $C$, the SWAP, the exchange rotor — acts on. **P6** (mass
and hypercharge from a gauged chiral $SU(2)$ connection) is directly load-bearing for §4.3.3's second
half: F378's mass-sector no-go is specifically about *this* project's own Stueckelberg-type SU(2)L
mass-generation mechanism, not about SU(2)-gauged Dirac mass terms in general, and would not arise at
all under a Higgs mechanism (a fundamental scalar mass term does not require the two-link
construction F378's obstruction targets). **P7** is not invoked; no result in this chapter is chosen
among alternatives on aesthetic grounds — every choice below (which $\Theta$, which point group, which
exchange path) is forced or excluded by an explicit algebraic argument.

**Prior results used, precisely.** **R2.12/R2.13** (the exact $D_{2h}$/$D_{4h}$ covariance of the
free walk, $O_h$ recovered only in the infrared) is the standing warning this chapter must not
violate: §4.3.2's spin–statistics argument and §4.3.5's emergent-$SO(3)$ discussion both concern
*continuous* rotation groups, and the chapter is explicit, following F379, about exactly which
continuous-group claims are dynamical (leading-order/IR, hence conditioned on R2.13) versus
kinematic (a different kind of object R2.12/R2.13 says nothing about at all). **R2.6–R2.9** (the
commutant computation: $d_\text{time}=1$, no second candidate generator) is the result §4.2's opening
section (F377) sharpens from "no rival construction found" to "no rival construction *possible*,
tested against its only live alternative shape." **R3.2/R3.6** (the concrete real-space stepper; its
exact locality and unitarity, "for Chapter 4's use") is cited directly rather than re-derived: every
finding in this chapter that builds an operator on the model's Hilbert space (the CPT $\Theta$, the
exchange SWAP, the reflection map $\theta$) is building it *on* the walk R3.2 defines, and every
claim of exact locality in §4.3.4 is R3.6 read at the level of many-body causal propagation rather
than the single-particle stepper.

**Free inputs consumed, stated plainly.** Several, of different character, and the chapter is
explicit about which results are conditional on which:

1. **Every result in §4.3.2–§4.3.3 that touches "$d=3$" or "the exchange sign" inherits Chapter 2's
   own stated conditionality** on the $s=2$ minimality premise and on BDPT's imported uniqueness
   theorem (Ch.2 §2.7 items 1–2) — not re-flagged at every occurrence below, but genuinely present.
2. **F328's discrete CPT theorem and F335's reflection positivity theorem are each theorems about a
   *specific, named construction*** — the branch-$+$/dagger massive Dirac unitary `dirac_bcc.py`
   builds, and the Wilson single-plaquette BCC₃×ℤ action `bcc_action.py` builds, respectively — not
   about "the model" in some looser sense that would automatically cover every alternative
   discretization in the tree. F378 §3 makes this precisely concrete: a *second*, coexisting
   discretization of the massive Dirac walk (`covariant_dirac_doublet_step`'s branch-$+/-$ kinetic
   pairing) fails F328's identity already at zero gauge coupling, for a reason unrelated to gauge
   coupling at all (a cross-module architectural mismatch, named but not resolved by any finding read
   for this chapter).
3. **The general theorems this chapter's results extend — Osterwalder–Seiler/Menotti–Pelissetto for
   reflection positivity, Finkelstein–Rubinstein/Anastopoulos for spin–statistics, Lieb–Robinson for
   locality — are imported from the literature, not re-derived from scratch.** What is derived here,
   case by case, is that this model's *specific* lattice construction satisfies (or, for Postulate 1,
   fails to satisfy) the stated hypotheses of each imported theorem. This distinction is the spine of
   §4.5 below.

> **On whether reflection positivity is a prerequisite for the rest of this chapter.** It is not, and
> the chapter's ordering (RP first, per the assignment brief) is expository rather than logically
> load-bearing. F335's link reflection positivity is a statement about the **gauge (Yang–Mills link)
> sector** — the BCC₃×ℤ Wilson plaquette action built in `bcc_action.py` — built and verified in a
> module family entirely disjoint from the free/interacting Dirac-walk modules the spin–statistics,
> CPT, and cluster-decomposition findings use (`qi_spin_statistics.py`, `discrete_cpt.py`,
> `qi_cluster.py`, and their companions). None of F289/F330/F377/F379/F328/F378/F290/F331/F380 cites
> F335, and F335 cites none of them. Reflection positivity is placed first because, in Euclidean QFT
> generally, it is the standard technical foundation for constructing a genuine Hilbert space and
> transfer matrix (Osterwalder–Schrader reconstruction) — the same role it plays as a foundation for
> confinement proofs in Chapter 13 — not because the fermionic results below presuppose it.

## 4.2 The derivation

### 4.2.1 Before the theorems: is "the update" even a well-posed single object? (F377)

Every result in this chapter treats "the model's dynamics" as literally one fixed unitary matrix
$A(\mathbf k)$ (or its Dirac-doublet extension $D(\mathbf k)$), iterated. Chapter 2's R2.6–R2.9
established this algebraically as a fact about the commutant of the free walk — no other homogeneous
local unitary flow commutes with it — but named an unresolved companion question: is the requirement
that dynamics *be* single-generator iteration itself derivable from the model's other accepted
axioms, or is it an independent, irreducible posit? F377 answers this directly, and the chapter opens
with it because every $\Theta$-operator identity and every spin-rotor argument below silently assumes
the answer.

**The independence argument.** D'Ariano & Perinotti's own formal statement of the BDPT homogeneity
axiom — "for every $g,g'$ there exists $\pi$ such that $\pi(g)=g'$" — is a condition on the **Cayley
graph**, i.e. a spatial statement about indistinguishable lattice sites. The per-tick evolution
$\psi_{q,t+1}=A\psi_{q,t}$ (their own Eq. 2, $A$ carrying no $t$-index) is *asserted*, not derived
from the five stated principles (linearity, unitarity, locality, homogeneity, isotropy). Temporal
constancy of the update — what this project calls **P1** in its own open-derivations ledger (a
different, and easily confused, use of "P1" from this monograph's postulate P1 of discreteness) — is
never one of the five named axioms; it is part of what "quantum cellular automaton" already means,
definitionally, both in the BDPT program and in this project's own founding premise.

$$\boxed{\;\text{single-generator dynamics is logically independent of the five stated BDPT axioms — not merely "not yet derived" from them}\;}\tag{R4.1a}$$

**The regrouping lemma, and the one live counterexample shape.** Before testing anything, F377
establishes that almost every apparent multi-generator alternative is not a counterexample at all:
any **periodic** sequence of local homogeneous unitaries — Margolus partitioning, brick-wall updates,
alternating between this model's own two admissible per-tick maps $A^+(\mathbf k)$/$A^-(\mathbf k)$ —
reduces, after regrouping one tick as one full period, to iterating a single fixed operator
$B=A_p\cdots A_1$. Checked to $2.0\times10^{-15}$ against a direct $2n$-step product (with a declared
control — comparing against $B^{n+1}$ instead of $B^n$ — verified red at residual $0.69$). The only
logically live counterexample is therefore an **aperiodic** schedule, one that never reduces to a
finite regrouping.

**The falsification attempt.** F377 builds the least exotic such schedule available — a Sturmian
word (the canonical maximally-balanced non-eventually-periodic binary sequence) selecting between
$A^+$ and $A^-$ tick by tick, using literally the model's own two BDPT-admissible per-tick maps and
its own production stepper (`weyl_step_3d_bcc`) — and measures the ballistic transport exponent $p$
of $\mathrm{Var}[\mathbf x](t)\sim t^p$. Both single-generator baselines sit near the required
$p\approx2$; the aperiodic schedule's exponent sits measurably below the best-case (matched-eigenbasis)
periodic reference at two independently chosen parameter points (gaps $0.056$ and $0.093$, both above
a declared $0.03$ margin).

$$\boxed{\;\text{the only live alternative to single-generator dynamics was built from the model's own admissible maps and degrades required ballistic transport at every tested point}\;}\tag{R4.1b}$$

(F377 §§1–3; test `F377-time-generator-axiom-independence`, 2/2 PASS, battery tier, one control
verified RED.) **What this does and does not close, stated as precisely as F377 itself states it.**
This is a citation-based independence argument (§1) plus a two-point numerical experiment (§3), not a
derivation of single-generator dynamics from anything smaller, and not a proof that *no* aperiodic
schedule at *any* parameters could reach ballistic transport. **Claim:** none — no card exists in
`claims-index.md` for F377 (checked directly), consistent with the finding's own framing as ledger
maintenance on an open-derivations row rather than a new headline assertion. The honest status of the
single-generator posit moves, per F377 itself, from "adopted, not derived" to "adopted, shown
independent of the model's other axioms, and tested against its only concrete alternative
construction, which does not reproduce the model's required physics" — a materially stronger
characterization of the same free input, carried forward silently as the working premise for every
$D(\mathbf k)$-based theorem in the rest of this chapter.

### 4.2.2 Reflection positivity for the BCC gauge action (F335)

**What was open.** Confinement (a topic Chapter 13 develops in full) has stood on Monte Carlo
sampling alone; no positivity machinery — the technical foundation for Osterwalder–Schrader
reconstruction of a genuine Hilbert space and a bounded transfer matrix — existed anywhere in the
tree. F335 does not attempt a confinement proof; it determines whether the model's own BCC₃×ℤ gauge
action satisfies the relevant theorem's hypotheses at all.

**The theorem, and what it actually needs.** Link reflection positivity for the Wilson plaquette
action (Osterwalder & Seiler 1978; extended to site reflections and general gauge-invariant
observables by Menotti & Pelissetto 1987) reduces, via a Peter–Weyl "sum of squares" factorization
across the reflection plane, to three structural hypotheses that reference **only the time
direction**: (a) nearest-neighbor-only temporal coupling; (b) purely spatial loops confined to a
single time-slice; (c) mixed loops crossing exactly one time-step, with temporal legs entering
linearly. Crucially — and this is the finding's own new content, not a re-derivation of 1978/1987 —
**none of (a)–(c), or the factorization proof behind them, references the spatial lattice's
connectivity at all.**

**Verification against the actual code.** `bcc_action.py`'s loop-construction function is read
directly (not redescribed): it builds exactly ten loops per site (F265's six spatial rhombi, F323's
four mixed rectangles), and `loop_structure_reflection_hypotheses()` checks (a)–(c) as exact,
randomness-free combinatorial facts, all `True`. The reflection map $\theta$ (site map
$\tau\to L_t-1-\tau$, with the temporal link picking up a dagger and the spatial links none) is
confirmed an exact involution (`0.0`), and the mixed-rectangle trace identity — the one place a
naive raw-matrix comparison first gave a spurious $O(1)$ "residual" before the correct, weaker,
trace-level identity was identified — is verified to $4.5\times10^{-16}$.

$$\boxed{\;\text{the BCC₃×ℤ Wilson action satisfies hypotheses (a)–(c) exactly, unconditionally in }\beta_s,\beta_t\ge0\text{ and in the gauge group}\;}\tag{R4.2}$$

(F335 §§1–2, checks H1–H4, I1, M1; test `F335-reflection-positivity-bcc`, 8/8 PASS, gate tier, one
control — dropping the dagger — verified red on exactly the one leg that depends on it.) Because
(a)–(c) never reference spatial connectivity, the hypercubic-lattice theorem carries over to
BCC-space$\times\mathbb Z$-time **without inventing any new machinery** — the finding calls this "a
modest corollary, not a new theorem," and this chapter agrees with that self-assessment.

**Supplementary exact result.** For the SU(2) sector specifically, the Wilson character coefficients
$a_j(\beta)=\tfrac{2j+1}{\beta}I_{2j+1}(2\beta)$ (via the Bessel recursion identity, elementary) are
strictly positive for all $\beta>0$, $j\ge0$ — a second, independent route to reflection positivity
that the general factorization argument does not require but which is a clean closed form worth
recording. Verified by direct Weyl-measure quadrature, smallest sampled value $1.02\times10^{-6}$
(deep in the tail, correctly small, not zero).

$$\boxed{\;a_j(\beta)>0\text{ for all }\beta>0,\ j\ge0\text{ (SU(2), closed form via Bessel recursion)}\;}\tag{R4.3}$$

(F335 §3, check S1; same test record.) A supporting, non-proof numerical cross-check (the reflection
Gram matrix, sampled by heat-bath Monte Carlo at the model's own derived anisotropy $\beta_t/\beta_s=4$,
F323) finds the dominant eigenvalue positive by three to four orders of magnitude above noise in
every run, with nine sub-leading directions statistically consistent with zero (2.5–4.1$\sigma$) at
the one lattice volume tested — reported honestly as inconclusive-but-not-contradicting, not as
independent confirmation, and explicitly not swept in volume (F335 §4, §5).

**What this is not.** No mass gap, no area law, no confinement verdict — reflection positivity is a
necessary ingredient for reconstruction, not a statement about the transfer matrix's spectrum or
large-loop Wilson-loop behavior. Per **claim card CL289** (`status: open`, `exactness: machine`),
this is exactly how the claim is carried: "a necessary ingredient... not a confinement proof: no mass
gap, no area law, no string-tension verdict is claimed or implied." The next step — a strong-coupling
or cluster-expansion argument on top of the now-available transfer matrix — is named as the residual
and is Chapter 13's business, not attempted here.

### 4.2.3 Spin–statistics: the theorem's own premises, derived rather than imported (F289)

**What the standard argument needs, and what this model supplies for it.** The topological
derivation of the spin–statistics connection (Finkelstein–Rubinstein; the belt trick) needs two
premises that ordinary quantum mechanics simply imports: **(I1)** the spatial dimension, because
$\pi_1$ of the $n$-identical-particle configuration space is the symmetric group $S_n$ only for
$d\ge3$ (the braid group $B_n$ for $d=2$, where anyons exist), so only $d\ge3$ makes particle
exchange an involution restricted to $\pm1$; and **(I2)** the $2\pi$-rotation phase of the exchanged
object, which the belt-trick homotopy identifies with the exchange sign. **In this model both are
outputs rather than inputs**: $d=3$ is Chapter 2's own R2.1–R2.3 (two independent selectors), and the
$2\pi$-rotation phase is a property of the model's own SU(2) rotor, in the tree since the $c_\text{lat}$
rotation-rate construction (CLAUDE.md Core Design Decision 2).

$$\boxed{\;R(2\pi)=-\mathbb1\text{, to }1.73\times10^{-16}\text{, over 60 independent rotation axes}\;}\tag{R4.4a}$$

$$\boxed{\;\mathrm{SWAP}^2=\mathbb1\text{ exactly (spectrum }\{+1^{(3)},-1^{(1)}\}\text{); an anyonic exchange is a perfectly good unitary that fails ONLY the involution test, and only because }d\ge3\;}\tag{R4.4b}$$

(F289 §§2–3, checks S1–S6; test `F289-spin-statistics`, 11/11 PASS, gate tier, three controls
verified red and red only where declared.) The second boxed result is the finding's own emphasis, and
this chapter preserves it: checking only $\mathrm{SWAP}^2=\mathbb1$ would prove nothing about anyons,
since the algebra does not forbid an anyonic exchange operator — what excludes it is that $\sigma^2=1$
holds only because $\pi_1=S_n$ rather than $B_n$, i.e. specifically because $d\ge3$ (Chapter 2's
result, not an independent fact about this model).

**Realization, not assumption.** F217's Jordan–Wigner fermionic operators are shown to *realize* the
derived exchange sign rather than independently assume it: the anticommutators vanish exactly, and a
declared control — removing the Jordan–Wigner $Z$-string — makes the operators commute (residual
$4.0$), i.e. the string specifically is what carries the $-1$. Pauli exclusion follows as a
consequence (the $k$-particle sector dimensions are exactly $\binom nk$, not the bosonic
$\binom{n+k-1}{k}$), not as a separate postulate.

$$\boxed{\;\text{the Jordan–Wigner string realizes the derived exchange sign; removing it gives residual }4.0\text{, not }0\;}\tag{R4.4c}$$

**A derived consequence: the model's photon is a boson.** Key decision 5 (CLAUDE.md) makes the
electromagnetic photon a bound pair of two spin-½ Weyl quanta. Rotating the pair by $2\pi$ rotates
both constituents: $(-1)\times(-1)=+1$, residual $3.46\times10^{-16}$. This pairing was forced for an
unrelated reason — F65–F67's polarimetry exclusion of the birefringent composite $\sigma$-bilinear
photon (Chapter 8's own content) — and its independent delivery of the correct Bose statistics is a
consistency the model was not tuned for.

$$\boxed{\;\text{the paired-spinor photon is a boson: }(R(2\pi)\otimes R(2\pi))-\mathbb1\text{ at }3.46\times10^{-16}\;}\tag{R4.4d}$$

**Per claim card CL255** (`tier: supporting`, `status: live`, `exactness: exact`, `confidence: medium`
— all deliberate, not an oversight): this card explicitly does *not* claim the spin–statistics theorem
itself is proved, re-proved, or extended. Two steps remain genuinely external and are not claimed
otherwise anywhere in this chapter: the algebraic-topology fact $\pi_1=S_n$ for $d\ge3$ (standard,
imported), and the Finkelstein–Rubinstein homotopy between exchange and $2\pi$ rotation (the belt
trick itself) — which §4.2.4 below takes up directly.

### 4.2.4 The belt-trick residual, precisely named and tested against its only escape (F330, F379)

F289's own "what remains" flagged the belt trick's homotopy step as external and unattempted in a
lattice-native form. F330 and F379 do not close this gap — both are explicit, throughout, that they
do not — but they replace an unspecified import with a precisely stated postulate, a machine-verified
mechanism for that postulate's spin-½ consequence, and a general argument for why no future
"try a bigger symmetry group" attempt can close it either.

**The residual, named exactly.** Anastopoulos's geometric-quantisation treatment (quant-ph/0110169,
fetched and quoted directly in F379 rather than paraphrased) isolates the belt trick's one
non-topological ingredient as **Postulate 1**: exchanging two identical spin-$s$ systems must be
realizable as a smooth path along the orbit of the diagonal $SO(3)$ action on the classical phase
space $\Gamma$ (for spin-$s$, $\Gamma=S^2$), such that performing the exchange twice composes to
exactly one $2\pi$ rotation. The purely topological half of the belt trick — that any two
collision-avoiding exchange paths in $\mathbb R^3\setminus\{0\}\simeq S^2$ are homotopic, since
$\pi_1(S^2)=0$ — is elementary and transfers to this model, or any model in $\mathbb R^3$, at zero
cost. What Postulate 1 supplies *beyond* that elementary fact is the claim that spin transports along
the exchange path via the **same** rotation realizing the positional exchange, rather than via some
other, uncorrelated unitary — and this, Anastopoulos states plainly, is not derivable from geometry
alone; it is imposed by hand.

**The spin-½ mechanism, machine-verified for the first time.** F289 asserted that premise I2 "picks
the one for spin-½: $-1$" without exhibiting why. F330 exhibits it: at the belt trick's own exchange
angle $\theta=\pi$, the antisymmetric singlet is an exact scalar under $R(\theta,\hat n)\otimes
R(\theta,\hat n)$ for *every* rotation angle and axis (residual $1.8\times10^{-16}$), while the
symmetric triplet is an invariant subspace but is demonstrably **not** a scalar at $\theta=\pi$
(eigenvalues exactly $\{-1,+1,-1\}$, deviation $\sqrt{8/3}$ exactly) — a genuine, checkable asymmetry
between the two channels, confirmed non-vacuous by a declared control (substituting the $m=0$ triplet
member for the true singlet breaks the invariance).

$$\boxed{\;\text{the singlet is an exact scalar under the exchange rotor at every angle; the triplet is not, at }\theta=\pi\text{ specifically}\;}\tag{R4.5a}$$

(F330 §5, checks B1–B3; test `F330-belt-trick-reduction`, 4/4 PASS, gate tier, two controls verified
red and only there.)

**Attempted and abandoned, for a stated structural reason, not a search failure.** F330 asks directly
whether the BCC lattice's own structure — the finite point group $O_h$ (order 48), or the rotor's
dynamical rotation rate $\Omega(\mathbf k)$ — could supply Postulate 1 natively rather than leaving it
imported. It cannot, and the reason is a **category mismatch**: $O_h$ is a *finite* subgroup of
$SO(3)$ and carries no substitute for $\pi_1(SO(3))=\mathbb Z_2$'s *continuous* topological content —
"a finite group's classifying space has a different (and here, irrelevant) homotopy type from
$SO(3)$'s." The rotor's $\Omega(\mathbf k)$ is a **dynamical** (per-tick, momentum-dependent) rotation
rate; Postulate 1 needs a **kinematic** (parallel-transport, path-dependent) one — a categorically
different construction that happens to share the word "rotation."

$$\boxed{\;\text{Postulate 1 is not derived; the lattice-native attempt fails for a stated category-mismatch reason, not from insufficient searching}\;}\tag{R4.5b}$$

**Hardened against the natural escape: "try a bigger continuum limit."** F379 asks the next question
directly: does the model's own emergent *continuous* symmetry — F129/F130's block-spin RG isotropic
fixed point, or F344's exact leading-order $O_h$ covariance (R2.13) — recover a genuinely continuous
$SO(3)$ that the finite $O_h$ could not supply, and does *that* close the gap? F379 first confirms the
positive half: the model's own rotor (the identical function from F289/F330) exactly realizes
$SO(3)$-covariance of the idealized Weyl Hamiltonian for a **continuous** rotation, not restricted to
$O_h$'s 48 elements (worst residual over 280 swept combinations: $2.47\times10^{-16}$), and the
*actual shipped* BCC dispersion obeys the same law to the $O(k)$-relative accuracy F344's mechanism
predicts, on both chirality branches, confirmed for a generic continuous rotation.

$$\boxed{\;\text{F344's exact leading-order }O_h\text{ covariance genuinely extends to the full continuous }SO(3)\text{, using the model's own rotor and dispersion}\;}\tag{R4.6a}$$

**But this answers the wrong question, for a reason that forecloses the whole avenue, not just this
attempt.** Postulate 1's own architecture, per Anastopoulos's paper read directly, places its content
strictly at the level of **prequantisation** — the classical phase space $\Gamma$ and a transitive
symplectic $G$-action on it, *before any Hamiltonian is introduced*. F129/F130 and F344 are, without
exception, claims about the model's **time evolution** — a Hamiltonian-symmetry fact, true only in a
limit (IR fixed point, or leading order in $|\mathbf k|$). Since Postulate 1's content sits one
logical layer prior to any Hamiltonian, **no dynamical symmetry fact — of any size, however exactly
derived — can bear on it.** A second, independent layer sharpens this further: even Anastopoulos's
own worked example (an *exact*, non-approximate, transitive symplectic $SO(3)$ action on $\Gamma=S^2$
for a genuine free spin-$s$ system — strictly stronger than any dynamical-covariance fact this or any
model could hand over) *still* needs Postulate 1's lift condition as a separate, additional
assumption. So even a hypothetical future kinematic (rather than dynamical) $SO(3)$ construction built
from the lattice would not, by itself, close the gap.

$$\boxed{\;\text{no dynamical-symmetry fact, of any size, can supply Postulate 1 — the target is categorically prequantisation-level, not a bigger continuum limit}\;}\tag{R4.6b}$$

(F379 §§1–6, checks K1–K3; test `F379-so3-kinematic-gap`, 3/3 PASS, gate tier, one control verified
red on exactly the leg testing "same rotation, not an uncorrelated one." Independently reviewed by a
blind cold-subagent re-derivation that reached the same conclusion via its own reading of the primary
source and contributed the second layer above.)

**Claims, stated precisely.** CL255 (`status: live`, `exactness: exact`, `tier: supporting`,
`confidence: medium`) carries F330's narrowing as an amendment: "Postulate 1 is **not** derived... a
separate, explicitly non-numeric argument narrows its status further *in this model specifically*...
but this is stated as a POSIT-narrowing claim, not a derivation." **F379 itself carries no separate
claim card** — checked directly (`grep -n "F379\]" claims-index.md` returns nothing) — consistent
with its role as hardening an existing residual's diagnosis rather than asserting a new positive
result.

### 4.2.5 Discrete CPT for the free BCC Dirac walk (F328)

**What was open.** Prior to this finding, the model's discrete-symmetry content existed only at the
level of charge-*label* bookkeeping (§4.2.6 below, F53) and a scalar corollary
($\omega_0(+m)=\omega_0(-m)$) — nowhere in the tree was there an actual **operator** $\Theta$ built on
the walk's Hilbert space and checked against the dynamics the way a genuine CPT theorem requires. A
standing diagnostic in `docs/theory/ca-reference.md` ("Time-reversibility") tested something adjacent
and called it done — running the forward walk backward and confirming a $6\times10^{-14}$ round-trip
residual — which is a fact true of **any** unitary automaton on inspection and carries no antiunitary
content at all. Whether a genuine CPT theorem could even exist here was a live question, since
standard continuum proofs (Streater–Wightman) assume continuum Lorentz invariance, which this model
has only partially (a fact deferred to Chapter 7).

**The construction.** Writing the massive BCC Dirac one-tick unitary as
$D(\mathbf k)=\begin{pmatrix}nA^+(\mathbf k)&im\mathbb1\\im\mathbb1&nA^+(\mathbf k)^\dagger\end{pmatrix}$
(the branch-$+$/dagger construction `dirac_bcc.py` actually ships), two algebraic identities of the
free Weyl walk's own cos/sin closed form — (I) $A^s(\mathbf k)^{*}=\sigma_y A^s(\mathbf k)\sigma_y$ at
any fixed $\mathbf k$ (a **generic** fact about any real-$(u,\mathbf n)$ Pauli-basis unitary, not
BCC-specific), and (II) $A^{-s}(-\mathbf k)=\sigma_y A^s(\mathbf k)\sigma_y$ (branch swap plus momentum
flip — this one **is** specific to the BCC embedding) — chain through the block structure to give, for
**every** $\mathbf k$ and **every** admissible mass $|m|\le1$, with no small-$k$ expansion anywhere:

$$\boxed{\;\Theta\,D(\mathbf k)\,\Theta^{-1}=D(\mathbf k)^{-1},\qquad \Theta:=M\cdot K,\quad M:=\Sigma\cdot(\sigma_y\!\oplus\!\sigma_y),\quad \Sigma=\begin{pmatrix}0&\mathbb1\\\mathbb1&0\end{pmatrix}\;}\tag{R4.7}$$

with $K$ complex conjugation and $\Sigma$ the standard Dirac parity matrix $\gamma^0$ in the Weyl
basis. In position space, $(\Theta\psi)(x)=M\psi(-x)^{*}$: spatial reflection, an internal
spin-and-chirality twist, and complex conjugation combined into one antiunitary operator, satisfying
$\Theta^2=-1$ exactly — the Kramers signature of a genuine spin-½ antiunitary symmetry, not
bookkeeping. Verified to literal `0.0` over 500 random $(\mathbf k,m)$ samples plus the $\mathbf k=0$/
axis-aligned/$|m|\in\{0,1\}$ edge cases, and confirmed at $8.5\times10^{-16}$ in a full, nonlinear,
many-step ($N=12$) real-space FFT-mediated propagation test — the check that actually distinguishes a
genuine antiunitary symmetry from the "forward-then-dagger" invertibility every unitary automaton has
for free (contrast leg E2, the `ca-reference.md` negative control, which stays at the identical
floating floor for a completely different, symmetry-free reason).

**The companion no-go: parity alone cannot exist at finite $\mathbf k$, and this is a spectral proof, not merely unattempted.**
$D(\mathbf k)$'s eigenvalues are $e^{\pm i\omega(\mathbf k)}$ with
$\omega(\mathbf k)=\arccos(nu^+(\mathbf k))$; because the construction pairs only branch $+$ with its
own dagger, $\omega(-\mathbf k)$ is governed by a genuinely different function ($u^+(-\mathbf
k)=u^-(\mathbf k)\ne u^+(\mathbf k)$ generically). Conjugation by any fixed, momentum-independent
unitary preserves a matrix's spectrum, so since $D(\mathbf k)$ and $D(-\mathbf k)$ generically have
**different** spectra (measured minimum gap $1.58\times10^{-5}$ over 500 samples, vanishing only on
cubic axes, consistent with F301's independently-derived finite-$a$ Poincaré defect), **no fixed
unitary parity operator $\Pi$ can satisfy $\Pi D(\mathbf k)\Pi^{-1}=D(-\mathbf k)$ for every
$\mathbf k$** — an outright algebraic obstruction, not an unfound construction. Consistently, the
naive candidate $\Pi=\Sigma$ (plain block swap) misses $D(-\mathbf k)$ by $O(1)$ (measured $1.93$).

$$\boxed{\;\text{even the free, gauge-decoupled kinetic+mass term is not parity-symmetric at any finite }\mathbf k\text{ — only the full }\Theta\text{ survives, exactly}\;}\tag{R4.8}$$

(F328 §§2–4, legs A1–A2, B1–B3, C1–C2, D1–D3, E1–E2; test `F328-discrete-cpt-theorem`, 12/12 PASS,
gate tier, one control — dropping the $\sigma_y$ twist from $\Theta$ — verified red on exactly the
four legs that depend on it.) **Per claim card CL285** (`tier: headline`, `status: live`,
`exactness: exact`, `confidence: high`): this is the strongest single result in this chapter — a
proof route that "does not invoke continuum Lorentz invariance at any step," an operator identity
exact at finite lattice spacing, not a continuum-limit statement.

### 4.2.6 Per-species discrete-symmetry labels: the interaction's own C, P, CP (F53)

Independent of, and prior to, F328's operator-level construction, F53 established the model's
charge-label discrete-symmetry content, species by species, for the first generation. Charge
conjugation $C$ maps each species to its antiparticle, $(T_3,Q,Y,\chi)\to(-T_3,-Q,-Y,-\chi)$, with
Gell-Mann–Nishijima closure exact for both particle and antiparticle. Because the model's charged
current couples to the **left** sector alone, $C$'s image of a left-handed particle is a
right-handed antiparticle that does not couple — $C$ and $P$ are each **maximally** violated by the
interaction ($A_C=A_P=1$ exactly), while the combination $CP$ is exact for a single generation
(Jarlskog $J=0$ exactly, since a $1\times1$ CKM matrix carries no physical phase). The one candidate
CP-odd parameter — the complex-mass phase $\theta(x)$ — is shown pure gauge: the one-tick eigenphase
spectrum is $\theta$-independent to $3.3\times10^{-16}$, and the $\theta$-gauged step reduces to the
$\theta=0$ step bit-for-bit ($9.0\times10^{-16}$).

$$\boxed{\;C\text{ maximal, }P\text{ maximal, }CP\text{ exact (single generation) — a statement about the interaction's charge-label structure, not an operator on the Hilbert space}\;}\tag{R4.9}$$

(F53 §§1–3, parts P1–P6; 6/6 PASS.) **This is a genuinely different kind of claim from F328's**, and
CL285 states the distinction explicitly rather than treating F53 as a weaker draft of the same result:
F53 answers a representation-bookkeeping question (how do charge labels transform under the gauge
group) while F328 answers an operator question (does a fixed antiunitary map intertwine the dynamics
with its inverse). F328's own §5 makes the same point from the other direction: "F53 P6... is not
withdrawn — it is a true, cheaper corollary" of the fact $D(\mathbf k)$ and $D(\mathbf k)^{-1}$ share a
spectrum, which F328's $\Theta$ promotes to an operator statement. Neither supersedes the other.

### 4.2.7 Extending CPT to the gauge-coupled sector: an exact kinetic-sector theorem, and a proved mass-sector no-go (F378)

F328 named the SU(2)$_L$-gauged extension as its own stated residual. F378 attacks it directly and
finds a split result — one genuine extension, one genuine, general obstruction — rather than a clean
promotion in either direction.

**First finding: the actual gauge-coupled module in the tree fails F328's identity already at zero
gauge coupling**, for a reason unconnected to gauge coupling at all. `covariant_dirac_doublet_step`'s
kinetic term pairs branch $+$ with the true **opposite** branch $-$, not with branch $+$'s own dagger
the way `dirac_bcc.py` does — two different, coexisting discretizations of "the massive BCC Dirac
fermion" in the tree, each unitary by a different mechanism, and only one has a proven CPT theorem.
This cross-module architectural mismatch is named, not resolved, by F378 (§4.1 item 2 above records
the same point as a standing free input for this chapter).

**The kinetic sector, isolated: an exact extension via SU(2) pseudoreality.** Grafting a
spatially-uniform SU(2) link $U$ directly into `dirac_bcc.py`'s own branch-$+$/dagger architecture
($A^+(\mathbf k)\to A^+(\mathbf k)\otimes U$ in the kinetic block only, mass left an isospin scalar)
gives $D'(\mathbf k)=\begin{pmatrix}n(A^+(\mathbf k)\otimes U)&im\mathbb1_4\\im\mathbb1_4&n(A^+(\mathbf
k)\otimes U)^\dagger\end{pmatrix}$, and

$$\boxed{\;\Theta'D'(\mathbf k)\Theta'^{-1}=D'(\mathbf k)^{-1},\qquad \Theta':=M'\cdot K,\quad M':=\Sigma\cdot(\sigma_y\!\otimes\!\tau_2\ \oplus\ \sigma_y\!\otimes\!\tau_2)\;}\tag{R4.10}$$

holds exactly (residual $6.7\times10^{-16}$ over 300 random $(\mathbf k,m,U)$ samples, plus edge
cases at $3.1\times10^{-16}$), using the SU(2) pseudoreality identity $\tau_2U\tau_2^{-1}=U^{*}$ (true
for every $U\in SU(2)$, verified to literal `0.0` over 500 samples) in place of F328's identity (I)
for the isospin factor. **The Kramers signature flips**: $\sigma_y\otimes\tau_2$ is a Kronecker
product of two purely-imaginary matrices and is therefore real, giving $M'^2=\mathbb1$ and
$\Theta'^2=+\mathbb1$ (verified to literal `0.0` against $+\mathbb1$, and to residual $2.0$ against
$-\mathbb1$) — not F328's Kramers $\Theta^2=-1$. This is the generic behavior expected from composing
two independent pseudoreal (spin-½-like) twists, not a numerical curiosity.

**The mass sector: a genuine, provable obstruction, not merely a failed search.** The model's own
actual mass mechanism (`covariant_dirac_doublet_step`'s Stueckelberg-type construction) mixes
$\eta,\chi$ through a **second**, independent SU(2) link $V$, and the same $\Theta'$ fails at $O(1)$
against it (residual $2.85$, generic across tested $V$). Working through the block algebra shows the
mass block requires $\Lambda V^T\Lambda^{-1}=V$ for **every** $V\in SU(2)$ and some fixed operator
$\Lambda$ — but $V\mapsto V^T$ is a group **anti-automorphism**, conjugation by any fixed $\Lambda$ is
always an **automorphism**, and their composition can equal the identity map only if the group is
**abelian**. SU(2) is not, so **no fixed $\Lambda$ can exist** — a structural fact, not a search
failure, corroborated by a 500-sample Monte Carlo search over Haar-random $\Lambda$ finding none
closer than residual $0.28$.

$$\boxed{\;\text{no fixed isospin operator can repair }\Theta'\text{ for the gauged mass sector — an anti-automorphism can equal a fixed-point automorphism only on an abelian group, and SU(2) is not abelian}\;}\tag{R4.11}$$

(F378 §§2–5, legs X0, E1, A1, B1–B3, C1–C1b, D1–D3; test `F378-discrete-cpt-gauged-theorem`, 11/11
PASS, battery tier, one control verified red on exactly four legs.) **Per claim card CL306**
(`status: live`, `exactness: exact`, `tier: supporting`, `confidence: high`, `rolls_up_to: CL285`):
stated with a scope boundary the chapter preserves exactly rather than compresses — **this is not a
claim that the model's SU(2)$_L$ gauge theory violates CPT as a physical statement.** Every test above
holds the classical gauge/mass background **fixed** under the antiunitary map, mirroring exactly how
F328 tests $D(\mathbf k)$ against $D(\mathbf k)^{-1}$ at the same mass. The continuum Lüders–Pauli
argument for a genuine gauge theory instead lets $C,P,T$ also transform the connection itself; whether
a **background-transforming** $\Theta$ restores an identity for the mass sector is a different,
unattempted question — named as the row's new, narrower residual (ledger row A4r), not answered here
and not implied to be answerable by analogy with the continuum case.

### 4.2.8 Cluster decomposition: exact in the free 1-D theory, strict where Lieb–Robinson is only exponential (F290)

**The question.** A model built as one global rule on one lattice owes an account of why distant
experiments remain independent — a property completely unguaranteed by construction, and one the
tree had essentially no content on before this finding (a single QC aside, F227).

**No-signalling, exactly.** For product, Bell/GHZ, and generic entangled states, and twelve distinct
local unitaries on region $A$: $\max\lVert\rho_B'-\rho_B\rVert=7.77\times10^{-16}$ — nothing done on
$A$, including at maximal entanglement, is visible at $B$. A declared control (a genuinely non-local
unitary applied across the cut) moves $\rho_B$ by $0.461$, confirming the check is not vacuous.

$$\boxed{\;\text{no-signalling holds exactly: }7.77\times10^{-16}\text{, vs. }0.461\text{ under a non-local control}\;}\tag{R4.12a}$$

**The causal cone is strict — the genuinely CA-specific content.** A generic quantum spin system
obeys a Lieb–Robinson bound with an unavoidable **exponential tail**,
$\lVert[A(t),B]\rVert\le Ce^{-(r-vt)/\xi}$ — small outside the light cone, but never exactly zero. A
quantum cellular automaton instead has a genuinely **finite** light cone: outside it, the measured
difference is **exactly** zero ($6.87\times10^{-16}$, against a generic Lieb–Robinson bound evaluated
at the same points of $7.39$) — because the underlying circuit simply contains no path there, a fact
about connectivity rather than an estimate. The cone was measured, not conservatively bounded, at
exactly $r\le t$ (one site per brick-wall layer) — a first, conservative draft ($2t$) would have made
the check unfalsifiable, since shrinking it by one cell would still find every tested point genuinely
outside — and reconciles numerically with F227's separately-reported $r>4t$ once the two different
tick conventions (F227's is a *full* brick-wall with two Heisenberg-evolved operators) are accounted
for.

$$\boxed{\;\text{the causal cone is exactly zero outside }r=t\text{, where a generic Lieb–Robinson bound gives }7.39\text{ at the same points}\;}\tag{R4.12b}$$

**Clustering tied to the gap, in the 1-D free theory.** In the gapped ground state of a staggered-mass
lattice Dirac chain, connected correlations decay exponentially with $\xi\propto\Delta^{-0.93}$
($R^2=0.9994$ over an $8.3\times$ range in gap) — quoted **as measured**, not as the continuum value
($\xi=v/\Delta$, exponent $-1$); pushing to smaller mass makes the fit *worse*, not better, because
$\xi$ then exceeds what the finite chain resolves. At the gapless point the decay is power-law, not
exponential, confirming the check discriminates the two regimes rather than merely fitting whatever it
is given.

$$\boxed{\;\xi\propto\Delta^{-0.9268}\text{, }R^2=0.9994\text{ (measured, 1-D free theory); power-law, not exponential, at the gapless point}\;}\tag{R4.12c}$$

(F290 §§1–3, checks C1, C2, C3; test `F290-cluster-decomposition`, 10/10 PASS, gate tier, three
controls verified red and only where expected.) **Per claim card CL256** (`tier: headline`,
`status: live`, `exactness: machine` for the no-signalling/cone legs, `quantitative` for the
clustering exponent): the card is explicit that the clustering leg is scope-limited — "the clustering
leg is 1-D and free-fermion... cluster decomposition for the interacting 3-D BCC theory... is **not**
established" — precisely the residual §4.2.9 addresses next.

### 4.2.9 Cluster decomposition, extended to the interacting 3-D theory, and its own residual named (F331, F380)

**The free-fermion 3-D closed form, and a hazard hit and fixed.** F331 first derives a genuine 3-D
(not disguised 1-D) closed form for the (100)-axis correlation length,
$\kappa_{100}(m)=\sqrt3\operatorname{arccosh}(1/\sqrt{1-m^2})$, by extremizing the dispersion's
complex-momentum pole over the two real transverse momenta and proving (via a bilinear-corner
argument, not an assumption) that the (100) axis is the dominant singularity. Validating this
numerically against the model's own dispersion first **failed badly** — measured $\kappa\approx0.10$–
$0.15$ against the exact $0.9514$ at $m=0.5$ — for exactly the reason Chapter 2's R2.16 already named:
the naive cubic FFT grid is not the BCC crystal's true reciprocal lattice. The fix (`_oblique_kgrid`,
built directly on `WALK_RECIPROCAL_GENERATORS`) is not a re-fit but a correction to the sampling
domain itself, turned into a declared control (the naive grid gives ratio $\approx0.22$ instead of the
corrected $\approx1.07$–$1.17$).

**The interacting theory: a dynamically generated mass, in the lattice's own regulator.** A
lattice-native self-consistent NJL gap equation, regulated by the model's finite Brillouin zone rather
than an artificial cutoff (with a parameter-free exact anchor, $I_1^\text{lat}(1)=1/\pi$ exactly at
the QCA admissibility endpoint), generates a nonzero mass $m^*\approx0.605$ from a bare-massless
starting point for couplings $g\in(g_c,\pi)$, $g_c\approx2.637$ measured — chiral symmetry is
dynamically broken by the interaction alone, with a declared control (below $g_c$) confirming only
the trivial solution survives there.

$$\boxed{\;\kappa_{100}(m^*{=}0.605)=1.216\text{ (closed form); measured ratio }1.15\text{ at the dynamically-generated mass — cluster decomposition holds in the interacting, 3-D, mean-field theory}\;}\tag{R4.13}$$

(F331 §§1–4; test `F331-cluster-interacting-3d`, 5/5 PASS, gate tier, two controls verified red.)
Honestly graded `QUANT` at issue: the measured/exact ratio does not reach machine precision at any
tested mass or window (best $\approx5\%$ at $m=0.95$, worst $\approx53\%$ at $m=0.05$, monotonically
shrinking with mass).

**The residual, named as one object rather than an 18-entry tolerance table.** F380 asks the natural
next question — is F331's mass-dependent residual a red herring at the dynamically-selected mass
$m^*$, or does it follow the same curve as every other tested mass? The literal hypothesis (that
$m^*$ is numerically special) is **falsified directly**: the ratio at $m^*$ is $1.10960$, L-converged,
not unity to the numerical floor. But the *mechanism* generalizes: F331's `_fit_kappa` fits a pure
exponential to a correlator that actually carries an algebraic prefactor $r^{-p}$ from two independent
effects — $r^{-1}$ from ordinary transverse stationary-phase integration, **plus** an extra $r^{-1/2}$
because the axial dispersion $\omega(a)=\arccos(nu(a))$ vanishes as a **square-root branch point** at
the pole (not linearly, so not the ordinary continuum Yukawa case), giving a theoretically-derived
total power $p=3/2$. Converting F331's fixed-window fit bias into the implied effective power
$p_\text{eff}$ via the exact OLS regression-bias formula (no free parameter, no re-fit) gives:

$$\boxed{\;p_\text{eff}=1.489\pm0.039\text{ (2.65\% spread), matching the derived }p=3/2\text{ to }<1\%\text{, mass-independent across the full admissible range including at }m^*\;}\tag{R4.14}$$

(F380, checks C1–C3; test `F380-cluster-asymptotic-series-K`, 3/3 PASS, gate tier, one control —
using the wrong BCC axis's closed form as reference — verified red.) $m^*$ sits at $z=-0.62\sigma$
from the scan mean — unremarkable, which is the useful negative result: not "$m^*$ is special" but
"the entire table, $m^*$ included, is one object." **This is exactly the QUANT→PARTIAL promotion
shape** the state-of-model rubric names: a named seam (one theoretically-anchored power, not a
tolerance table), not a machine-precision closure — the sub-leading $\sim1\%$ offset from $3/2$ and
the sub-leading $\sim2.6\%$ scatter are not yet symbolically derived, and F380 is explicit that this
is the next, unattempted rung.

**Per claim card CL286** (`tier: headline`, `status: live`, `exactness: quantitative`,
`confidence: medium`): reports the same honest residual, and explicitly does not extend to F290's
separate 1-D exponent shortfall or to $S$-matrix-level cluster decomposition — both remain open, as
§4.6 records.

## 4.3 Results table

| # | Statement | Status | Exactness | Test record |
|---|---|---|---|---|
| R4.1a | Single-generator dynamics (Ch.2/3's R2.6–R2.9, R3.5) is independent of the five stated BDPT axioms, not merely undeprived | sharpened posit (no claim card) | citation-based argument | — |
| R4.1b | The only live counterexample shape (aperiodic Sturmian schedule, built from the model's own admissible maps) degrades required ballistic transport at every tested point | numerical experiment, not a theorem | quantitative | `F377-time-generator-axiom-independence` (2/2, battery) |
| R4.2 | The BCC₃×ℤ Wilson gauge action satisfies the three structural hypotheses of the OS/MP link-reflection-positivity theorem, exactly, for any compact group and $\beta_s,\beta_t\ge0$ | **full theorem** (hypotheses verified for this lattice; not a confinement proof) | exact / machine | `F335-reflection-positivity-bcc` (8/8, gate) |
| R4.3 | SU(2) Wilson character coefficients $a_j(\beta)>0$ for all $\beta>0,j\ge0$ (closed form) | full theorem (supplementary route) | exact | same record, leg S1 |
| R4.4a–d | Spin–statistics: $R(2\pi)=-\mathbb1$; SWAP is an involution only because $d\ge3$; the JW string realizes the exchange sign; the paired-spinor photon is a derived boson | **derivation of the theorem's premises**, not the theorem itself | exact | `F289-spin-statistics` (11/11, gate) |
| R4.5a–b | The belt-trick's spin-½ mechanism (singlet-scalar / triplet-non-scalar at $\theta=\pi$) is machine-verified; a lattice-native derivation of Postulate 1 is attempted and fails for a stated category-mismatch reason | **honest non-closure**, mechanism exhibited, residual precisely named | exact (mechanism) / not derived (postulate) | `F330-belt-trick-reduction` (4/4, gate) |
| R4.6a–b | F344's exact leading-order $O_h$ covariance extends to the full continuous $SO(3)$; but no dynamical-symmetry fact of any size can supply Postulate 1 (prequantisation-level mismatch) | **hardened no-go** (forecloses an entire avenue) | exact (K1–K3) / categorical argument | `F379-so3-kinematic-gap` (3/3, gate) |
| R4.7 | Discrete CPT for the free BCC Dirac walk: $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$, $\Theta^2=-1$ (Kramers), exact at every $\mathbf k,m$, no continuum Lorentz invariance invoked | **full theorem** | exact | `F328-discrete-cpt-theorem` (12/12, gate) |
| R4.8 | No fixed unitary parity $\Pi$ can satisfy $\Pi D(\mathbf k)\Pi^{-1}=D(-\mathbf k)$ for every $\mathbf k$ — a spectral obstruction | **proved no-go** (companion to R4.7) | exact / structural | same record, legs D1–D3 |
| R4.9 | Per-species $C$ maximal, $P$ maximal, $CP$ exact (single generation); the mass phase $\theta$ is pure gauge | charge-label theorem (distinct object from R4.7) | exact / machine | `FG9-C-CP-per-species` (declared debt; armed via `run-FC06-cpt-lorentz`) |
| R4.10 | The SU(2)$_L$-gauged **kinetic** term admits an exact CPT-type theorem via SU(2) pseudoreality, with a flipped ($\Theta'^2=+1$) involution | **extension, proved** (scope: fixed background only) | exact | `F378-discrete-cpt-gauged-theorem` (11/11, battery) |
| R4.11 | The SU(2)-gauged **mass** mechanism admits no fixed-isospin-operator analogue — an automorphism/anti-automorphism obstruction, general for non-abelian groups | **proved no-go** | exact / structural | same record, legs D1–D3 |
| R4.12a–c | No-signalling exact; the causal cone is strictly zero outside $r=t$ (vs. Lieb–Robinson's $7.39$ at the same points); $\xi\propto\Delta^{-0.93}$ in the 1-D gapped free theory | **full theorem** (no-signalling, cone) / measured (clustering) | exact–machine / quantitative | `F290-cluster-decomposition` (10/10, gate) |
| R4.13 | Cluster decomposition extended to the interacting, 3-D, mean-field (NJL) BCC theory, at a dynamically-generated mass $m^*$ | derivation, mean-field only | quantitative | `F331-cluster-interacting-3d` (5/5, gate) |
| R4.14 | R4.13's mass-dependent residual collapses to one theoretically-anchored power, $p_\text{eff}=1.489\pm0.039$, matching a derived $p=3/2$ to $<1\%$ | **named residual** (QUANT→PARTIAL promotion, not MACHINE) | quantitative | `F380-cluster-asymptotic-series-K` (3/3, gate) |

## 4.4 Comparison with measurement

Almost entirely not applicable, and stated so rather than papered over: every result in this chapter
is an internal-consistency or mathematical-physics theorem, checked against the model's own algebra
or against an imported theorem's stated hypotheses, not against an experimental number. One indirect
link is worth recording rather than leaving silent: **F328/CL285's discrete CPT theorem is the
structural fact underlying this project's discussion of CPT-violation bounds** — a model with an
*exact* CPT-type symmetry for its free sector has a principled reason to expect any observed
CPT-violating signal to be small and lattice-spacing-suppressed rather than generic, which is the
comparison Chapter 7 (relativity on a lattice, LIV coefficients, observational bounds) carries out in
full; nothing in this chapter itself is compared to a bound. Nothing else here — reflection
positivity, spin–statistics, cluster decomposition — has, or should be read as having, a direct
observational comparison at this level; these are checks that the model is a sound enough quantum
theory for later chapters' predictions to be trusted, not predictions themselves.

## 4.5 What was excluded, and why

- **A general, gauge-transforming CPT theorem for the SU(2)$_L$-coupled sector.** Not excluded as
  false — genuinely untested. F378 restricts every check to a **fixed** gauge/mass background, exactly
  mirroring F328's own fixed-mass test; the continuum Lüders–Pauli argument instead lets $C,P,T$ also
  transform the connection. This is named as the row's residual (§4.6), not assumed to fail by
  analogy with the mass-sector no-go, and not assumed to succeed by analogy with the kinetic-sector
  extension.
- **A fixed isospin operator repairing the gauged-mass CPT identity.** Excluded by a **general
  algebraic proof** (R4.11), not a failed search: an anti-automorphism ($V\mapsto V^T$) can equal a
  fixed-point automorphism (conjugation by any $\Lambda$) only on an abelian group, and SU(2) is not
  abelian. A 500-sample Monte Carlo search corroborates this without needing to rely on the algebra
  alone.
- **A lattice-native (finite point group, or dynamical rotor) derivation of the belt trick's
  Postulate 1.** Excluded twice, at two levels of generality: F330 shows the finite $O_h$ point group
  and the dynamical rotor $\Omega(\mathbf k)$ are each the wrong *kind* of object for this model
  specifically; F379 then shows the mismatch is general — *any* dynamical-symmetry fact, of any size
  or derived exactly, is categorically the wrong kind of object, because Postulate 1's content sits at
  the prequantisation level, prior to any Hamiltonian.
- **Any fixed unitary $\Pi$ implementing ordinary parity at finite lattice spacing, for the free
  Dirac walk.** Excluded by a spectral obstruction (R4.8): $D(\mathbf k)$ and $D(-\mathbf k)$
  generically have different eigenvalue spectra, and spectrum is a conjugation invariant.
- **Confinement, a mass gap, or an area law, as a consequence of reflection positivity alone.**
  Explicitly not claimed by F335/CL289: RP is a necessary ingredient for Osterwalder–Schrader
  reconstruction, not a statement about the resulting transfer matrix's spectrum. The next step (a
  strong-coupling or cluster expansion) is Chapter 13's business, not attempted here.
- **A discretization-independent CPT theorem.** F378 §3's discovery that a *second*, coexisting
  discretization of the massive Dirac walk fails F328's identity already at zero gauge coupling (for
  an unrelated branch-pairing reason) is a standing reminder that this chapter's theorems are about
  *specific named constructions*, not about "the model" as a discretization-independent object.

## 4.6 What is still open

Named because the source findings themselves name it, in every case:

1. **The belt trick's Postulate 1 is not derived, anywhere, by this project or in the cited
   literature.** F379 forecloses an entire class of future attempts (bigger dynamical symmetry
   groups) but does not attempt, and names as the only remaining logical avenue, a genuinely
   *kinematic* construction — a fact about the classical phase space and its group action, built from
   the lattice's own structure without reference to any Hamiltonian or dispersion at all. F379's own
   §8 adds a second-layer warning: even such a construction would still need to separately supply
   Postulate 1's lift/holonomy condition, which the mere existence of a group action does not fix.
2. **Whether a background-transforming $\Theta$ restores a CPT-type identity for the SU(2)-gauged
   mass sector** is a different, unattempted question from what F378 tests (§4.2.7) — named as ledger
   row A4r's residual, not answered here.
3. **The pre-existing cross-module discretization mismatch** (`covariant_dirac_doublet_step`'s
   branch-$+/-$ kinetic pairing vs. `dirac_bcc.py`'s branch-$+$/dagger pairing) is named by F378 §3 as
   an architectural inconsistency independent of the CPT question, and is not fixed by any finding
   read for this chapter.
4. **F335's reflection-positivity result stops short of a confinement proof.** The strong-coupling or
   cluster-expansion step needed to get from "a transfer matrix exists" to "the theory confines" is
   named as the residual and is not attempted; F335 §4's Gram-matrix numerical cross-check is
   explicitly reported as inconclusive-but-not-contradicting at the sub-leading scale, with volume
   dependence untested at even the one lattice size run.
5. **The 1-D exponent shortfall in F290's own clustering result** ($\xi\propto\Delta^{-0.93}$ vs. the
   continuum $-1$, a $7\%$ deviation that gets *worse*, not better, at smaller mass within the tested
   range) is untouched by F331/F380's separate 3-D extension — a different, unresolved residual on
   the free-theory side.
6. **F380's own promotion is QUANT→PARTIAL, not PARTIAL→MACHINE.** The theoretically-derived power
   $p=3/2$ explains the leading algebraic prefactor; the sub-leading $\sim1\%$ mean offset and
   $\sim2.6\%$ point-to-point scatter are not yet derived from a full symbolic expansion of the BCC
   dispersion's phase at the saddle, and F380 states this as the explicit next rung, not attempted.
7. **The interacting cluster-decomposition result (F331) is mean-field (NJL Hartree-type), not a
   full non-perturbative treatment with vertex corrections** — the identical scope limit F77 already
   carried, inherited rather than improved on here.
8. **$S$-matrix-level cluster decomposition** (connected amplitudes factorizing for distant clusters,
   the field-theoretic form of the property) is not addressed by F290 or F331/F380; what is shown
   throughout is the correlation-function and reduced-state form.
9. **The single-generator posit (F377)** is shown independent and tested against its only live
   alternative construction — not derived from anything smaller, and the numerical falsification
   attempt covers two parameter points, not an exhaustive sweep over wavepacket shapes, momenta, and
   irrationals.

No new gap (`G-4`) is logged for this chapter: every open item above is a residual the source findings
themselves state explicitly and precisely, not an assumption this chapter's authoring discovered
smuggled in without being named — the bar `docs/monograph/GAPS.md` sets for a logged gap. `GAPS.md` is
therefore not modified by this chapter.

## 4.7 Falsifiers

Collected from the relevant claim cards and the findings' own stated falsifiers, organized by result:

- **R4.1 (single-generator dynamics, F377):** a formal BDPT-program statement proving temporal
  homogeneity equivalent to graph homogeneity would kill the independence claim; a wider parameter
  sweep finding an aperiodic schedule whose ballistic exponent matches or exceeds the best periodic
  reference would reverse the falsification-attempt result (no claim card; falsifiers from the finding
  directly).
- **R4.2/R4.3 (reflection positivity, CL289):** a future engine change adding a longer-range temporal
  hop or a two-time-step mixed loop would break hypothesis (a)/(c); a demonstrated sign/indexing error
  surviving to machine precision would contradict the involution/trace identities; a stable,
  growing-with-statistics negative eigenvalue in the Gram construction (not a single few-$\sigma$ run)
  would directly contradict the theorem.
- **R4.4/R4.5/R4.6 (spin–statistics and the belt trick, CL255):** an anyonic exchange surviving as an
  involution, or $d\ne3$ under a re-derivation, would kill the premise-derivation claim; a demonstrated
  path from a genuinely kinematic (not dynamical) lattice construction to Postulate 1's lift condition
  would be the first real progress on the still-open residual, and per F379 would need to defeat its
  prequantisation-level argument first.
- **R4.7/R4.8 (discrete CPT, free sector, CL285):** any $(\mathbf k,m)$ at which
  $\Theta D(\mathbf k)\Theta^{-1}\ne D(\mathbf k)^{-1}$ to machine precision falsifies the theorem; any
  fixed $\Pi\ne\Sigma$ satisfying $\Pi D(\mathbf k)\Pi^{-1}=D(-\mathbf k)$ for all $\mathbf k$ falsifies
  the companion no-go.
- **R4.10/R4.11 (gauged CPT, CL306):** a $(\mathbf k,m,U)$ breaking the kinetic-sector identity would
  falsify the positive half; a fixed operator $\Lambda\ne\tau_2$ (or one acting on a larger space)
  satisfying $\Lambda V^T\Lambda^{-1}=V$ for every $V\in SU(2)$ would falsify the mass-sector no-go.
- **R4.12 (cluster decomposition, free theory, CL256):** any measured outside-cone difference above
  $10^{-12}$ at any $(r,t)$ falsifies the strict-cone claim directly; shrinking the declared cone
  radius below $r=t$ and still finding every tested point outside is the control that must, and does,
  fail.
- **R4.13/R4.14 (interacting cluster decomposition, CL286):** a genuinely dominant complex singularity
  elsewhere in the Brillouin zone (found by a more careful multi-dimensional saddle-point analysis)
  giving a smaller decay rate would falsify the closed form; a full symbolic sub-leading expansion
  disagreeing with the measured $p_\text{eff}=1.489\pm0.039$ band would falsify the named-residual
  mechanism.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–3's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\Theta$ | The antiunitary CPT-type operator for the free BCC Dirac walk, $\Theta=M\cdot K$, $M=\Sigma\cdot(\sigma_y\oplus\sigma_y)$; satisfies $\Theta^2=-1$ (Kramers). | §4.2.5 |
| $\Theta'$ | The SU(2)-gauged-kinetic-sector analogue of $\Theta$, using $\sigma_y\otimes\tau_2$ in place of $\sigma_y$; satisfies $\Theta'^2=+1$ (flipped, non-Kramers). | §4.2.7 |
| $\Sigma$ | The $\eta\leftrightarrow\chi$ chirality-block swap; the standard Dirac parity matrix $\gamma^0$ in the Weyl basis. | §4.2.5 |
| $\tau_2$ | The SU(2) pseudoreality matrix (numerically $\sigma_y$, kept as a distinct name for the isospin factor); $\tau_2U\tau_2^{-1}=U^{*}$ for every $U\in SU(2)$. | §4.2.7 |
| $\Gamma$ | The classical (pre-quantum) phase space of a spin-$s$ system, $\Gamma=S^2$ for spin-$s$; the level at which Anastopoulos's Postulate 1 is stated, prior to any Hamiltonian. | §4.2.4 |
| Postulate 1 (Anastopoulos) | The belt trick's isolated non-topological content: exchange must be realizable as a smooth diagonal-$SO(3)$-orbit path on $\Gamma$ composing, twice, to one $2\pi$ rotation, with spin transported via the *same* rotation as the positional exchange. | §4.2.4 |
| $\kappa_{100}(m)$, $\kappa_{110}(m)$ | The exact closed-form correlation-decay rates along the BCC (100)/(110) Cartesian axes for the free massive Dirac field, from the dispersion's complex-momentum pole. | §4.2.9 |
| $p_\text{eff}$ | The implied algebraic-prefactor power of the 3-D correlator's asymptotic decay, extracted via the exact OLS fit-bias formula; measured $1.489\pm0.039$, matching the derived $p=3/2$. | §4.2.9 |

---

*No new gap logged this chapter — every open item in §4.6 is a residual the source findings state
explicitly, not a smuggled-in assumption this chapter's authoring uncovered. No finding, claim card,
module, or test record was created or modified in the writing of this chapter.*
