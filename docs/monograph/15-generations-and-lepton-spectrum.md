# Chapter 15 — Generations and the Lepton Spectrum: Three Families, the Mass Hierarchy, and the Weight-as-Phase Principle

*Chapter 15 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from the 37
findings `00-plan.md` §2 assigns to this chapter — F73, F74, F75, F76, F77, F78, F80, F81, F82, F84,
F92, F93, F95, F96, F101b, F108, F109, F118, F120, F121, F149, F150, F170, F175, F176, F177, F199,
F200, F234, F253, F255, F256, F342, F346, F347, F348, F352 — all read in full, plus
`docs/monograph/01-postulates-and-ontology.md` (P5, P6), `docs/monograph/11-mass-without-a-higgs.md`
(R11.1–R11.14, the chiral-$SU(2)$ mass mechanism this chapter's condensate sits on top of), and
`docs/monograph/12-hypercharge-and-electroweak.md` (R12.1–R12.32, especially its Group D/E material
on F141/F153, whose own text states — quoted verbatim in §15.1 below — that this chapter's condensate
is exactly the non-perturbative calculation those findings named as needed). Checked against
`docs/theory/key-decisions.md` decision 7 (the weight-as-phase founding principle, 2026-07-16),
`docs/theory/supersessions.yaml` records **S6** (F179 → F253/F255/F256) and **S15** (F230 →
F253/F255/F256), both read in full, and `claims-index.md` (CL028, CL005, CL004, CL293, CL291, and
the fourteen supporting cards resting on this chapter's individual findings, `status: open` at
`review_state: unreviewed-seed` throughout — see §15.7). `docs/monograph/GAPS.md` re-read
immediately before writing (last entry **G-8**, with **G-7** double-assigned across Chapters 12 and
18 per that ledger's own note); this chapter's own finding is logged as **G-9**.*

## 15.0 What this chapter establishes

Chapter 11 built the mechanism by which mass exists at all — a chiral $SU(2)$ connection $U(x)$,
gauging a representation ambiguity in the Dirac $\beta$ matrix, with the magnitude of each flavor's
mass left completely free by the bare rule (R11.14). This chapter is where that freedom is spent for
the charged leptons: not by fitting three numbers to three masses, but by deriving, from the BCC
lattice's own point-group representation theory, **why there are exactly three generations, why they
are not degenerate, and why their mass *ratios* take the specific values they do** — reproducing the
entire charged-lepton spectrum to $\le0.007\%$ from two derived numbers and one overall scale.

The chapter's spine is a single long chain of findings, built over three months (2026-06-01 through
2026-09-02), that starts from group theory and ends at a founding principle of the whole project
(CLAUDE.md Core Design Decision 7). Four questions structure it:

1. **Why exactly three generations, and why are they not degenerate?** Answered by the BCC lattice's
   cubic point group $O_h$: the unique odd-parity triplet irrep $T_{1u}$ forces the count to three and
   forbids a fourth (F75); breaking the residual cubic symmetry orthorhombically is what lifts the
   degeneracy (F76, F84) — with an honest, freshly-discovered gap in exactly how forced that
   identification is (F342).
2. **What physical object is the charged lepton, and why is its mass the square root of a lattice
   amplitude?** Answered by treating the lepton as a two-constituent Cooper pair (the same
   "Higgs-is-a-Cooper-pair" premise from Ludwig's notes that Chapter 11 already used to argue against
   a fundamental Higgs scalar) — a construction that, when pushed to its own limit (F73, F74, F77),
   turns out **not** to reproduce the 125 GeV Higgs boson, but does supply the exact kinematic and
   dynamical machinery (√m, the 45° equipartition, the constituent count $N=2$) that the *lepton*
   sector needs (F78, F80, F81, F82).
3. **What is the physical vacuum condensate that carries the generation-splitting field, and how much
   of its structure follows from the lattice alone?** Answered by identifying the splitting field as an
   $E_g$ condensate on the BCC second-neighbour shell (F93), deriving its cubic Landau invariant
   exactly from the Dirac sea (F95), excluding a whole class of quadratic-cost theories (F96), and
   closing the full self-consistent flavor functional on the physically required spontaneous-symmetry-
   breaking branch (F101b, F108, F109, F118, F149, F150).
4. **Why does the condensate's phase angle equal exactly $\tfrac29$ radians — the $E_g$ representation
   weight — rather than some fitted number?** This is the chapter's central derivation. $\delta^*=\tfrac29$
   is not merely measured to agree with the $E_g$ weight; it is **adopted as a founding principle**
   precisely *because* every dynamical alternative that could have produced $\tfrac29$ some other way
   is closed: a scale-free topological origin is excluded (F253), the phase's normalization is proved
   forced rather than posited (F255), and the one dynamical route that could in principle fit the angle
   is shown structurally incapable of doing so *exactly* (F256). §15.2.6 presents this three-way closure
   as the chapter's main derivation, per `docs/theory/key-decisions.md` decision 7's own framing — not
   relegated to an exclusions appendix.

## 15.1 Inputs

**Postulates used.** **P5** (`01-postulates-and-ontology.md` §1.2) — the massless Weyl-spinor
primitive — underlies the mass step's own dependence on chirality that F75's Step 3 selects the
$T_{1u}$ triplet by (§15.2.1). **P6** — the chiral $SU(2)$ connection $U(x)$ carrying mass without a
Higgs field — is the postulate whose *ratio* structure this chapter derives: Chapter 11 built the
mechanism, Chapter 12 built the electroweak sector on top of it, and this chapter is where the
specific numerical shape of the charged-lepton triplet is derived rather than left as three free
inputs. **P7** (the elegant-design heuristic, Ch.1 Gap G-1) is invoked once, explicitly, at the same
place Chapters 8 and 12 invoke it: the decision to *adopt* weight-as-phase as a founding principle
once every dynamical alternative is closed (§15.2.6) is a P7-style judgment — the simplest surviving
construction is preferred once the alternatives are eliminated, not derived from anything more
primitive. This chapter's own Gap G-9 (§15.6) flags one further place this preference's residual
honesty needs tracking.

**Prior results used.** **R11.11–R11.14** (`11-mass-without-a-higgs.md` §11.2.6) — the theorem that
rest mass is the unique zero-$\mathbf k$ rotation $\Omega_\text{rest}(m)=\arcsin m$, and R11.14's
explicit statement that the bare rule leaves **every** flavor's mass magnitude free, $m\in(0,1)$
equally admissible — is what this chapter's whole programme responds to: it fixes mass *ratios*
within one generation, and leaves the *overall scale* exactly where R11.14 left it, forward-cited to
Chapter 17. **R11.1–R11.7** (the mass step $M(\theta)$, the pure-gauge field $U(x)$) is the mechanism
whose representation-shell structure F75's Step 3 exploits. From Chapter 12, this chapter picks up an
explicit forward citation Chapter 12 itself made: discussing why the free fermion sea cannot supply
the electroweak channel-splitting stiffness its own $\sin^2\theta_W=\tfrac29$ counting needs, Chapter
12 states plainly that "the $8/7$ bookkeeping factor... must come from a non-perturbative computation
in the saturated $E_g$/EWSB condensate sector (F118, F150)" (`12-hypercharge-and-electroweak.md`
§12.2.23) — **this chapter is where that computation is done** (§15.2.5). Chapter 12's own F49 also
derives a second, independent $\tfrac29$ on the identical BCC second-neighbour shell (the
sublattice/bond-axis counting behind the Weinberg angle); this chapter's F175 derives a *third*,
representation-theoretic $\tfrac29$ on the same shell (§15.2.6) — three unrelated $\tfrac29$'s that
CLAUDE.md's constants registry (D7) is explicit must be kept as three separate registered constants,
never merged, because merging any of them "would turn a prediction into an input."

**Free inputs consumed — the chapter's most consequential accounting, read this carefully.** Per
CLAUDE.md's Core Design Decision 7, "the entire charged-lepton shape then follows from
$\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ to $\le0.007\%$ with zero shape parameters." Both quantities
in that pair must be individually audited, because they are *not* free inputs in the same sense:

1. **$\eta^2=\tfrac12$ (equivalently, the per-constituent saturation angle $t^*=45°$, or the
   circulant amplitude ratio $\eta=\sqrt2$ in F175/F346's parametrization) is *derived*, not fitted —
   but only given one adopted premise.** The premise is that the charged lepton is a bound pair of two
   spin-$\tfrac12$ constituents (F73) — the same "the Higgs is the Cooper pair, we presume" move from
   Ludwig's notes (`references/physics-notes-complete.md` pp.5–6) that Chapter 11 already used to
   argue mass generation needs no fundamental scalar. F73's own text is explicit that this premise
   is *adopted*, not derived from the QCA update rule. **Given** that premise, plus the bilinear
   condensate law $m=y^2$ it motivates (F78 Part A — itself "motivated, not proven" from the rule,
   F78 §6), the value $t^*=45°$ (hence $\eta^2=\sin^2t^*=\tfrac12$) is then derived four independent,
   mutually reinforcing ways: as the unique point where two independently-established mass laws
   ($m=\sin2t$ pair-sum kinematics and $m=y^2$ bilinear) are jointly consistent, given the standard
   two-quantum Fock normalization (F92, §15.2.4); as the phase-budget split of a two-constituent pair
   sharing a $\pi/2$ stability ceiling equally (F81, §15.2.3); as the coupling-independent location of
   the composite-mass energy minimum along a flat modulus (F82, §15.2.3); and, most strongly, as the
   unique attractor of the rule's own relaxational phase flow, with the pair-sum law itself derived
   directly from the update rule ($U\otimes U$ spectrum theorem, F109, §15.2.5) rather than assumed.
   F177 additionally identifies this 45° as the genuine Bogomolny/BPS self-dual point of the pair
   rotation (§15.2.6). **So $\eta^2=\tfrac12$'s status is: derived, given the Cooper-pair premise —
   and that premise is the chapter's first granted input**, inherited from Chapter 11's own stance on
   what mass is.
2. **$\delta^*=\tfrac29$ is different in kind.** The *number* $\tfrac29$ is derived exactly, with zero
   free parameters, as the $E_g$ representation weight $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})$ — pure
   $O_h$ group theory (F175). What is **not** derived from dynamics is the *identification* of that
   dimensionless weight with the condensate's physical phase angle, in radians. CLAUDE.md decision 7
   is explicit and this chapter follows it exactly: "This is taken as fundamental, not derived from
   the condensate dynamics." Weight-as-phase is **adopted as a founding principle**, and §15.2.6 is
   this chapter's central derivation of *why* that adoption is the right call: three independent
   findings (F253, F255, F256) close every route by which the value $\tfrac29$ could instead have
   been produced dynamically (fitted, computed, or read off a topological invariant), leaving
   weight-as-phase as the only route left standing. **So the chapter's second, and only truly
   irreducible, granted input is the weight-as-phase principle itself** — not the number $\tfrac29$,
   which is exact group theory, and not a residual fitted coupling, which F256 proves cannot exist.
3. **What remains genuinely free, and forward-cited.** The overall mass *scale* (turning the
   dimensionless shape into an electron rest mass in MeV) is not fixed by anything in this chapter —
   exactly the R11.14 residual, closed only by Chapter 13's dimensional transmutation of the strong
   coupling and Chapter 17's SI-scale anchor (forward-cited, not re-derived, in §15.2.7). The quark
   sector's mass texture is **not** derived by any mechanism in this chapter — F346/F347 show the
   direct transplant of this chapter's own mechanism fails for quarks (§15.5). The neutrino sector is
   Chapter 16's territory.

So the chapter's honest free-parameter ledger is: **zero numerical shape parameters, given two
granted structural premises** — the Cooper-pair mass-generation premise (inherited from Chapter 11)
and the weight-as-phase principle (adopted here, §15.2.6, on the strength of a three-way closure) —
plus the one still-open overall scale (forward-cited to Chapter 17).

## 15.2 The derivation

### 15.2.1 Three generations, and why they are not degenerate

**F75 — exactly three generations from $O_h$ representation theory.** Define a generation multiplet
operationally: states that (i) carry identical gauge quantum numbers, (ii) are related by an exact
symmetry of the vacuum, and (iii) are mutually independent. Conditions (ii)+(iii) together are exactly
the statement "fills one irreducible representation" of the BCC vacuum's cubic point group $O_h$
(order 48). Building the group from its generators and projecting the character table exactly over the
integers: the largest single-valued (tensor) irrep of $O_h$ has dimension **3** — $\sum_i d_i^2=48$ is
saturated only by $1,1,2,3,3$ in each parity sector, with no 4-dimensional single-valued irrep
anywhere. The BCC nearest-neighbour shell (the 8 body-diagonal vertices the F27 mass step couples to)
decomposes as $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ ($1+1+3+3=8$), so the shell *physically
furnishes* a triplet, not merely permits one abstractly. The Dirac mass bilinear must be a true scalar
(required for the F46/R11.12 spherical-Pythagorean dispersion $\Omega_\text{rest}=\arcsin m$ to hold),
which forces the anchored $A_{1g}$ chirality's mass partner into an **odd-parity** shell orbital; of
the shell's two odd-parity pieces, $A_{2u}$ (a lone singlet) and $T_{1u}$ (the unique odd triplet),
only $T_{1u}$ is a multiplet at all:

$$\boxed{\;\text{generations}=\dim\big(\text{unique odd triplet }T_{1u}\text{ of }O_h\big)=3,\quad
O_h\text{ has no 4-dim single-valued irrep — a fourth is forbidden, not merely disfavoured}\;}\tag{R15.1}$$

A group-averaged random $O_h$-invariant Hermitian mass operator has eigenvalue degeneracies exactly
$[1,1,3,3]$ (commutator residual $4.4\times10^{-16}$); forcing a fourth state into the triplet's
degeneracy breaks the commutator to $1.0$ — a 4-dimensional degenerate block simply does not commute
with $O_h$. The fourth generation is excluded **or** unstable (split away under any symmetry-
respecting dynamics), matching the LHC/$Z$-invisible-width exclusion of a sequential fourth
generation, here as a representation-theoretic theorem rather than a fit (8/8 checks, F75).

**F75's own stated limitation, sharpened by F342.** F75 §7 was explicit from the start that "generation
index = orbital irrep of the nearest-neighbour shell" is "a model... not derived from the QCA update
rule" — the group theory (R15.1) is exact, the physical *identification* is a hypothesis. F342 (2026-
08-31) attacks this hypothesis directly and finds it **cannot be resolved by F75's own criterion**:
condition (i) — "identical gauge quantum numbers" — turns out to have zero selecting power under this
project's own adopted engine. Every gauge module the tree actually uses (`charge_coupling.py`,
`minimal_coupling.py`) implements a single scalar coupling constant, diagonal in the site basis, with
no shell or irrep index anywhere (a direct `grep` for `T_1u`/`T1u` outside `forks/` returns zero
hits). Because the model's founding homogeneity posit makes the BCC shell's 8 vertices a single $O_h$
orbit, any $O_h$-invariant charge operator diagonal in that basis is **forced to a multiple of the
identity** — it cannot distinguish $T_{1u}$ from $T_{2g}$, or from any other 3-dimensional subspace of
the shell, and so cannot do the selecting job F75's condition (i) was written to do. This is proved,
not merely observed: a declared control (replacing $O_h$ with the non-transitive subgroup generated
by a single $C_{4z}$ rotation) makes the diagonal-forced-constant claim go red exactly where it
should, confirming the argument is checkable rather than assumed (11/11 checks, F342). F342 also
re-derives F75's own $T_2$ decomposition by an independently-typed method (two equivariant embeddings
of the shell into $\mathbb R^3$, giving exact projectors $\Pi_{T_{1u}},\Pi_{T_{2g}}$ over $\mathbb Q$)
as a cross-check, unrelated to the identification question itself.

$$\boxed{\;\text{condition (i) of F75's own operational definition is forced vacuous by the model's site-diagonal gauge coupling — the physical identification "generation}=T_{1u}\text{" remains a hypothesis, and is now shown not to be closeable by F75's own criterion}\;}\tag{R15.2}$$

F342 is explicit that this is a narrowing, not a promotion or a demotion, of the generation-count
claim's status (`docs/claims/CL004` stays `contingent`) — it identifies precisely *why* the
identification is still open, rather than leaving the reason vague, and names the one constructive
route that would close it: exhibit an $O_h$-invariant coupling in the adopted (non-fork) engine that
is **not** diagonal in the site basis. No such coupling currently exists.

**F76 — the crystal-field hierarchy, and Koide as a cubic-geometry identity.** F75 fixes the count at
three but leaves the triplet degenerate. Three *distinct* masses require breaking the residual cubic
symmetry: counting eigenvalue patterns as the vacuum symmetry lowers ($O_h\to D_{4h}\to D_{2h}$) shows
a tetragonal (one-axis) distortion gives only two distinct masses, and **three inequivalent masses
require breaking all the way to the orthorhombic point group $D_{2h}$** — three inequivalent axes,
$T_{1u}\to B_{1u}\oplus B_{2u}\oplus B_{3u}$. A perturbation *linear* in the mass is excluded
quantitatively (the fitted splitting exceeds the mean by 83%, not a small correction). The variable
that works is $\sqrt m$: writing $\mathbf s=(\sqrt{m_e},\sqrt{m_\mu},\sqrt{m_\tau})$ and splitting it
into its cubic-invariant ($A_{1g}$, along $\hat n=(1,1,1)/\sqrt3$) and traceless ($T_{1u}$) parts gives
an exact identity relating the angle $\theta$ between $\mathbf s$ and $\hat n$ to the Koide ratio:

$$\boxed{\;\cos^2\theta=\frac{1}{3Q},\qquad Q\equiv\frac{\sum_a m_a}{(\sum_a\sqrt{m_a})^2}\;}\tag{R15.3}$$

so **Koide's $Q=\tfrac23$ is exactly the equipartition condition $\theta=45°$**, i.e. equal weight
between the cubic-scalar and the symmetry-breaking parts of $\sqrt m$ — reframing a sixty-year-old
empirical relation as a cubic-geometry statement, before any dynamics is invoked. The measured
charged leptons sit on this point to $6.2\times10^{-6}$ ($0.91\sigma$ of the $m_\tau$ uncertainty),
and enforcing $Q=\tfrac23$ predicts $m_\tau=1776.97$ MeV against PDG $1776.86\pm0.12$ MeV
($6.1\times10^{-5}$ relative). At this stage the equipartition amplitude ($\sqrt2$) and phase are
still **fit** parameters (F76's own honest disclosure) — deriving them is the work of §15.2.3–15.2.4.

**F84 — flatness is a stabilizer theorem, tied to the same break.** Modelling the residual "democratic"
restoring force with a stiffness $\kappa$ ($E(\phi)=\tfrac12\kappa\phi^2-\lambda\sin2\phi$), the
observed exact $45°$ requires $\kappa\to0$ — a genuine structural claim, not an approximation.
F93 (§15.2.4) later identifies $\kappa$ precisely as the residual $S_3$ generation-permutation
symmetry and shows its vanishing is a *theorem about the condensate's stabilizer subgroup at a
generic angle*, not an assumption:

$$\boxed{\;\kappa\to\infty\ (\text{cubic}, S_3\text{ intact})\Rightarrow Q\to\tfrac13\text{ (F75 degenerate triplet)};\qquad\kappa=0\ (\text{orthorhombic}, S_3\text{ broken})\Rightarrow Q=\tfrac23\;}\tag{R15.4}$$

One order parameter — the orthorhombicity — supplies the count (F75), the distinctness (F76), and the
flatness that lets $Q$ saturate at $\tfrac23$ (F82/F84), with the data bounding the residual
democratic stiffness at $\kappa/\lambda\lesssim2\times10^{-5}$.

### 15.2.2 The Cooper-pair channel, and why it is not the Higgs boson

Before deriving the lepton amplitude, three findings establish — and, crucially, *test to destruction*
— the pairing premise on the object it was first proposed for: the 125 GeV scalar.

**F73 — exact pair-sum kinematics.** Two constituents of lattice mass $m_1,m_2$, forming the spin-0
singlet partner of the F69 paired-spinor photon's spin-1 channel, compose their rest-rotation angles
additively ($\Omega_\text{pair}=\arcsin m_1+\arcsin m_2$, F69's phase-sum rule), giving the exact,
sub-additive composite mass

$$\boxed{\;m_H=\sin(\arcsin m_1+\arcsin m_2)\le m_1+m_2\;}\tag{R15.5}$$

with a built-in geometric binding deficit and a hard stability ceiling: the composite saturates
($m_H=1$) at equal constituent mass $m_c=1/\sqrt2$ ($\Omega_\text{pair}=\pi/2$). At the electroweak
scale this deficit is astronomically small ($\sim10^{-33}$), so the kinematics alone predict
$m_H\simeq m_1+m_2$ — which a near-threshold $t\bar t$ "molecule" overshoots (345 GeV vs 125 GeV) and
an equal-constituent threshold identification undershoots to no known fermion (62.6 GeV). The
kinematics fix a channel and a ceiling, not a value; the missing ingredient is genuine binding
dynamics.

**F74 — the binding dynamics exist, and are quantifiably too weak (or too fine-tuned).** A rigorous
3-D lattice contact-well solver gives an exact critical coupling $g_c=2t/W_3$ (the Watson integral)
and an exact binding-depth function $E_b(g)$, verified against direct diagonalization to
$1.3\times10^{-15}$. Reaching 125 GeV from a $t\bar t$ pair needs binding fraction $\beta=0.637$; the
model's own gauge sector supplies only $\beta\sim\alpha^2/8\approx7\times10^{-6}$ (five orders short),
and a contact interaction strong enough to reach $\beta\in(0,1)$ at all requires tuning the coupling to
within $\sim m_\text{lat}^2\sim10^{-33}$ of criticality — the Higgs hierarchy problem appearing
intrinsically in the model's own language, not evaded.

**F77 — the self-consistent theory removes the last degree of freedom, and the no-go sharpens to an
identity.** A single NJL coupling $G$ both dynamically generates the constituent mass (the gap
equation) and, in the same ladder, fixes the scalar pole — reproducing the pion as an exact Goldstone
boson and the measured light-meson sector to $\le4\%$. The result:

$$\boxed{\;m_\sigma\ge2m_c\text{ at every coupling}\;(\text{chiral limit: exactly }m_\sigma=2m_c)\;}\tag{R15.6}$$

so a "125 GeV from $t\bar t$" scalar is **structurally excluded** at mean-field/RPA order, not merely
numerically disfavoured — raising the coupling scales $m_c$ and $m_\sigma$ together at fixed ratio,
never producing sub-threshold binding. This is the honest terminus of the direct Higgs-as-Cooper-pair
programme (F352, §15.2.7, later confirms this quantitatively via renormalisation-group improvement at
the model's own derived UV cutoff — still off by a factor of ~2). **The pairing machinery this section
built is not wasted, however**: it is exactly the construction §15.2.3 needs for the charged-lepton
sector, where the physics is different (a democratic vs. hierarchical vacuum, not a single scalar
mass) and, unlike the Higgs case, does succeed.

### 15.2.3 Why $\sqrt m$, why 45°, and why $N=2$

**F78 — mass is the square of the pairing amplitude.** Applying the same Cooper-pair premise to
fermion *mass* (not just the would-be Higgs): if generation $a$'s mass is a pair-condensate bilinear
in a constituent amplitude $y_a$, then $m_a\propto y_a^2$, and $y_a$ — not $m_a$ — is the object that
carries the $T_{1u}$ vector quantum numbers. This is the answer to F76's open "why $\sqrt m$": Koide is
a statement about $y=\sqrt m$ precisely because mass is quadratic in the fundamental pairing
amplitude. Independent corroboration: generalizing to $m^s$ and asking which power gives a clean
rational participation ratio, the data select $s=\tfrac12$ uniquely (residual $1.4\times10^{-5}$
against neighbouring powers).

**F80 — one 45°, and the EM/colour selection rule.** Writing $\mathbf y=\sqrt m$ as a unit vector
rotated by angle $\phi$ off the democratic axis gives the exact map

$$\boxed{\;Q(\phi)=\frac{1}{3\cos^2\phi}\;}\tag{R15.7}$$

with $\phi=0°\!\to\!Q=\tfrac13$ (democratic), $\phi=45°\!\to\!Q=\tfrac23$ (equipartition),
$\phi=54.7°\!\to\!Q=1$ (single-axis). This is *the same* SO(2) equipartition as the F73 constituent
stability cap ($\arcsin m_c=45°$, rest = kinetic weight): both are the equal-split point of a
two-channel unitary rotation, and the measured leptons sit at $\phi_\text{lepton}=44.99974°$. Only
charged leptons — electromagnetically coupled and colour-free — sit at this critical point; up- and
down-type quarks ($Q=0.849,\,0.731$, QCD-dominated) and neutrinos (uncharged, unpinned) do not. The
honest residual, disclosed rather than smoothed over: *perturbative* EM is $\sim340\times$ too weak
to drive a full $45°$ rotation — EM explains **which sector** reaches the critical point, not the
**magnitude** of the rotation.

**F81 — why 45°: the pair halves the phase budget, and $Q$ reads off $N$.** Combining the F69
pair-phase-sum rule with a stability-saturation condition ($N\phi=\pi/2$ for $N$ constituents) gives

$$\boxed{\;Q_N=\frac{1}{3\cos^2(\pi/2N)}\;}\tag{R15.8}$$

For the pair, $N=2$: $\phi=\pi/4=45°$ exactly, $Q=\tfrac23$ exactly — no residual fit. $Q_N$ is a
strictly decreasing function of $N$ (democratic limit $\tfrac13$ at $N\to\infty$); the measured
$Q_\text{lepton}=0.666661$ uniquely selects $N=2$ (residual $6\times10^{-6}$; $N=3$ misses by $0.22$).
The Cooper-pair premise is now *read off the data*, not merely assumed.

**F82 — why the pair sits at saturation (not somewhere below it), independent of coupling strength.**
The composite mass $m_H=\sin2\phi$ *peaks* at exactly the saturation edge $\phi=45°$; a bound state
lowering its energy by increasing its own gap therefore has its energy minimum at $\phi=45°$ for
**any** binding strength $\lambda>0$ (verified over ten decades of $\lambda$) — dissolving the F80
"EM too weak" worry, since the weakness of EM sets the well's *depth*, not the minimum's *location*.
The one remaining assumption is that $\phi$ is a **flat direction** (no stiffness $\kappa>0$ restoring
toward democracy); exact $45°$ data are direct evidence $\kappa=0$, and F93 (§15.2.4) later proves
this is a stabilizer theorem, not an assumption (R15.4 above).

### 15.2.4 The saturated $E_g$ condensate

**F92 — the consistency theorem: two independently-derived mass laws force 45°, and the data pin the
Fock normalization.** Two laws describe the same composite: the pair-sum law $m=\sin2t$ (F73/F69) and
the bilinear law $m=y^2$ (F78), related by the standard two-quantum Fock normalization $y=\sqrt2\sin t$.
Demanding both hold simultaneously:

$$\boxed{\;2\sin^2t=\sin2t\iff\tan t=1\iff t=45°\ \text{(unique on }(0°,90°)\text{, sympy-exact)}\;}\tag{R15.9}$$

— a *third*, independent route to $45°$, one that does not assume the identification "generation
angle = constituent phase" but *solves for the one point where it can hold*. This also sharpens the
F73 stability cap: $y=\sqrt2\sin t\le1$ is exactly **unitarity of the pair amplitude**, with three
saturations coinciding at $t=45°$ (amplitude fills the budget, composite mass peaks, pair phase fills
$\pi/2$). Running the logic in reverse, the measured leptons *measure* the normalization constant:
$c^2_\text{data}=2\cot\phi_\text{lepton}=2.000018$ — the two-quantum Bose factor read off the mass
spectrum to $1.9\times10^{-5}$.

**F93 — the orthorhombic order parameter identified: an $E_g$ condensate on the second-neighbour
shell.** "Orthorhombic vacuum" had been a name, not a mechanism. F93 supplies four exact structural
facts. **(i)** The only crystal-field channel that splits the $T_{1u}$ triplet's three axes without
mixing them is uniquely $E_g$ — $\mathrm{sym}(T_{1u}\otimes T_{1u})=A_{1g}\oplus E_g\oplus T_{2g}$,
Schur degeneracies $[1,2,3]$, and $E_g$ is exactly the diagonal-traceless doublet. **(ii)** $E_g$ has
no home on the BCC first (nearest-neighbour) shell at all — its minimal home is the **second**
(cube-axis) shell, $A_{1g}\oplus E_g\oplus T_{1u}$, $[1,2,3]$ — the identical shell whose bond/axis
counting produces Chapter 12's F49 Weinberg-angle $\tfrac29$ (§15.1). **(iii)** At a generic condensate
angle the residual stabilizer is $D_{2h}$ (order 8) with **zero** axis-permuting elements — F84's
$\kappa=0$ flatness is a theorem about this stabilizer, not an inference. **(iv)** The vacuum
dispersion, including the BCC anisotropy, is exactly $O_h$-symmetric (residual $4.7\times10^{-16}$
under all 48 elements) — it carries zero $E_g$ component, so the break **cannot** be inherited from
the lattice geometry; it must be spontaneous. A Landau analysis through sixth order in the $E_g$
doublet shows the orthorhombic (three-distinct-mass) phase requires a **sextic** invariant — a quartic
theory can *never* orthorhombify the vacuum (0/169 mismatches on a numerical global-minimization
grid) — giving the exact criterion

$$\boxed{\;\text{orthorhombic phase}\iff C>0,\ |B|<2C,\qquad\cos3\delta^*=-\frac{B}{2C}\;}\tag{R15.10}$$

with the data fixing the one remaining free number to $\cos3\delta^*=0.785874$ (F93 O7).

**F95 — the cubic invariant $B$ derived exactly, and $C$ localized by a 31-decade no-go.** The
harmonic content of the Landau potential is itself derived (a roots-of-unity theorem: only
$\cos3n\delta$ can appear); the cubic coefficient is shown to be $A_{1g}\times E_g$ interference,
vanishing identically for a pure splitting field, with a closed form and the correct sign from the
Dirac-sea loop:

$$\boxed{\;B=-3\sqrt2\,I_2\,\bar y^4,\quad I_2=\langle\cot\omega_\text{kin}\rangle_\text{BCC}=0.2202,\quad B<0\;}\tag{R15.11}$$

verified against the full nonperturbative BZ computation to $1.4\times10^{-4}$. The **same** loop's
sextic coefficient scales as $\bar y^{\sim7}$ against $B\sim\bar y^4$: at the physical lattice
amplitudes the angle is locked by **31 decades** — no per-axis energy of any kind (another fermion
loop, a bond energy) can supply $C$. This localizes $C$ to a direct, $O(1)$-strength self-interaction
of the second-shell condensate itself, with the data demanding $C_\text{req}=0.636|B|$.

**F96 — a two-value theorem excludes the quadratic theory, and the massless-electron limit is exact.**
A strictly quadratic-cost mean-field gap theory on the exact BCC Dirac sea (the mean-field image of
any four-fermion contact) supports **at most two** distinct stable generation masses, for any
amplitude-to-mass map tried (a census proof, not a numerical accident). Three observed masses
therefore exclude it outright — making the non-quadratic $E_g$ self-term (F95's $C$) necessary for a
*third* independent reason, beyond the angle brake and $m_e>0$. Along the way, the exact
massless-electron texture algebra gives a second, sharp $45°$: for any $(m_h,m_\text{mid},0)$
spectrum, $Q=\tfrac23\iff3\delta=\tfrac\pi4$ (sympy-exact). Adding the single symmetry-allowed sextic
invariant $W(\sum_ap_a^3)^2$ — precisely $e^6\cos^23\delta$ in flavor variables — is **sufficient** to
unlock a three-distinct-mass phase (30 minimizers found on a modest scan), demonstrating the missing
term is not only necessary but capable of doing the job.

### 15.2.5 The flavor-functional architecture: closing the self-consistent condensate

**F101b — the sea has a cliff, and the τ mass is the saturation scale itself.** The Dirac-sea energy
per generation has divergent slope at the saturation edge ($g'(m)\to-\infty$ as $m\to1$, the
$\arccos$-dispersion cliff), so any *interior* heavy flavor is a saddle — the heaviest generation is
forced exactly onto the wall:

$$\boxed{\;y_\tau=1\ \text{exactly: the }\tau\text{ mass IS the saturation scale of the condensate}\;}\tag{R15.12}$$

With $\tau$ wall-pinned, the two light-flavor stationarity equations become linear, giving a
closed-form coupling family $(\kappa_E,\mu)(W)$ that reproduces the exact measured spectrum as a
genuine KKT local vacuum over $W\in[0.10,21.6]$. Two independent routes — F95's Landau angle
requirement and this spectrum fit — converge on $W^*\approx1.46$.

**F108 — an exact no-go excludes the entire democratic-invariant class, and localizes global
stability.** F101b's fit is metastable (squeezed between the all-saturated and empty vacua). F108
proves the obvious fix — "add a democratic-sector invariant $w(\bar y)$" — **cannot work at any
strength or functional form**: the refit leaves the wall-KKT margin invariant and the lepton point's
gap to its own democratic shadow is bounded below by an exact, $w$-independent floor
$\Delta_\infty=+0.0386>0$. Every single quartic invariant fails likewise; only the **pair**
$\{v\sum_ay_a^4\ (v<0),\ c\,e^4\ (c>0)\}$ succeeds — a quartic-for-quadratic swap in the $E_g$ sector —
making the exact lepton point the **global** ground state at fixed $W^*$. The honest tension: this
same $\sum y_a^4$ feeds the F95 cubic, shifting the angle requirement to where the completion's own
stability is lost — an open self-consistency problem F108 states but does not close. A
momentum-resolved sea-polarization bubble is built and verified against exact diagonalization
($1.8\times10^{-6}$) but stays wrong-sign at one loop — confirming, more sharply than F95, that no
free-fermion loop of any kind can supply the brake.

**F109 — the pair-sum law derived from the rule itself, and 45° as a genuine dynamical attractor.**
Where F73 *assumed* the pair-sum kinematics, F109 derives it: the two-constituent update
$U(t)\otimes U(t)$ has exact spectrum $\{e^{\pm2it},1,1\}$, with the maximally-rotating channel being
precisely the symmetric two-quantum state the Fock $\sqrt2$ normalizes — the composite genuinely
rotates at $2t$ per tick because the update rule says so, not by kinematic construction. A relaxational
flow of the phase under the sea energy has exactly two fixed points: $t=0$ (repulsive, exact rate
$4I_2$, matching F95's $I_2$ measured independently) and $t=45°$ (the unique attractor, stiffness
diverging toward the wall). A 1000-seed flavor-resolved condensation experiment lands on the
constrained point in the majority basin once F108's completion is included, with the
$(A_{1g},E_g)$ decomposition **measured**, not imposed, reproducing $Q$, $\delta$, equipartition, and
the Fock factor all to the same precision the data give.

**F118 — the self-consistent triple closes, on the branch spontaneous $E_g$ condensation requires.**
The open self-consistency tension of F108 is resolved: allowing the **attractive** ($\kappa_E<0$)
$E_g$ sign — the Mexican-hat condition that spontaneous condensation (F93) physically *requires* — a
self-consistent solution exists with the exact lepton spectrum as the global ground state (dense
$121^3$ search, gap $-2\times10^{-6}$), wall-KKT and constrained-Hessian conditions both satisfied,
and **all completion couplings $O(1)$ over a 2D region** — robust, not a knife-edge. The
$\kappa_E>0$ (repulsive) branch is excluded everywhere. The unique symmetry-allowed brake is now
identified precisely:

$$\boxed{\;C=\lambda_6\,e^6,\quad\lambda_6=0.636\,|B|/e^6=0.243\approx\tfrac14,\quad W=6\lambda_6=1.46\;}\tag{R15.13}$$

with the sea loop now excluded from sourcing $C$ by **sign** (wrong-sign sextic at saturation) as well
as by scaling — a doubled version of F95's no-go.

**F149 — mass is the unique electroweak channel-splitting agent, and this is Chapter 12's own missing
piece.** Applying the model's exact Dirac construction as a proxy for the electroweak condensate
coupling, the massless BCC sea's exact vector/hypercharge channel-equality (Chapter 12's F147) is
shown to survive at the *kinematic* level for any mass but split, with an exactly $m^2$ onset, at the
*dynamical* (response) level — mass is the **only** thing in the model's fermion sector that can split
these channels at all. Crucially, exhaustive charge-content counting (both the bare walk and the full
F38 generation spectrum) is shown to give the wrong ratio by exact rational factors ($\times\tfrac87$
and $\times\tfrac{10}{21}$ respectively) — **eliminating free-sea charge counting entirely** as the
source of the F49 electroweak-mixing ratio. This is exactly the calculation Chapter 12 forward-cited:
its own text states the $\tfrac87$ bookkeeping factor "must come from a non-perturbative computation
in the saturated $E_g$/EWSB condensate sector (F118, F150)" — this chapter's condensate *is* that
sector, and this section's architecture is what a future session would use to complete Chapter 12's
open item, though the explicit numerical closure is not performed here.

**F150 — the brake's source and kind are closed; its magnitude joins one shared residual.** Combining
F95's per-axis scaling no-go with Chapter 12's own F147 (the free sea has **exactly zero** static
response to any gauge field, in every channel) gives a categorical two-route no-go: $C$ cannot arise
from the free fermion sea by any mechanism whatsoever. Its *kind* is then fixed by Chapter 12's own
F145 induced-coupling machinery (the colour-blind Fierz $c=\tfrac29$): the $E_g$ self-couplings, like
the strong sector's NJL contact, are **induced** by integrating out the binding exchange — resolving
what an earlier finding (F115) had flagged as an unjustified "notation collision" between the lepton
condensate coupling and the gluon coupling. This reclassifies $\lambda_6$ from an isolated fitted
number into a member of the single nonperturbative IR-coupling residual that already governs
$\sqrt\sigma/f_\pi$, the strong-coupling transmutation scale, and the $\chi$SB critical coupling
(Chapter 13's territory). The target sharpens to a striking, convention-independent identity:

$$\boxed{\;\cos3\delta^*=\cos Q,\qquad Q=\tfrac23\ (\text{Koide}),\qquad\text{agreement }1.7\times10^{-5}\;}\tag{R15.14}$$

i.e. $3\delta^*=Q$ to $4\times10^{-5}$ — the angular and radial invariants of the *same* saturated
condensate coincide. §15.2.6 picks up this identity as the seed of the weight-as-phase programme.

### 15.2.6 Weight-as-phase: the central derivation

This is the chapter's headline result, and per `docs/theory/key-decisions.md` decision 7 it is
presented here as a derivation, not relegated to an exclusions appendix — the whole point of the
argument is that a *no-go* forcing the adopted principle belongs in the reasoning itself.

**The primary derivation: $\delta^*=\tfrac29$ rad as the exact $E_g$ representation weight (F175).**
$T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g}$, dimensions $1+2+3+3=9$; the unique
non-mixing splitting channel is $E_g$ (F93 O1). Its weight in the full 9-dimensional bilinear is

$$\boxed{\;\delta^*=\frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\frac29\ \text{rad}\;}\tag{R15.15}$$

verified by explicit $O_h$ character projection over all 24 rotations (multiplicity of $E$ exactly 1).
This is the same "$2$ special out of $9$ total" structure as Chapter 12's independent gauge-sector
$\tfrac29$ (F49, sublattices over bond axes) — two unrelated countings on the identical second shell,
landing on the same fraction. Feeding the derived, un-fitted $\delta^*=\tfrac29$ into
$\sqrt{m_a}=\mu(1+\sqrt2\cos(\delta^*+\tfrac{2\pi a}{3}))$ — using the also-derived $\eta^2=\tfrac12$
(§15.2.3–15.2.4) — reproduces the charged-lepton mass **ratios** with zero shape parameters:

$$\boxed{\;m_\mu/m_e=206.770\ (+0.001\%),\qquad m_\tau/m_e=3477.47\ (+0.007\%)\;}\tag{R15.16}$$

**F234 — the $(W,v,c)$ triple closes, and $\lambda_6$ becomes an output.** F118 established existence
and stability of the self-consistent flavor functional (§15.2.5) but left the *value* of the brake
$\lambda_6$ as its one open item. Feeding the derived $\delta^*=\tfrac29$ into the F118/F150
brake-matching relation $\cos3\delta^*=|B|/2C$, using the **derived** cubic $B$ (F95, R15.11), fixes
the brake with no fit at all:

$$\boxed{\;C=\frac{|B|}{2\cos\tfrac23}=0.0362\ (=F118\text{'s }C_\text{req}\text{ to the digit}),\qquad\lambda_6=0.243,\ W=1.46\ (\text{derived, not fit})\;}\tag{R15.17}$$

The arrow now runs **angle $\to$ brake**, not the reverse: existence and stability were closed by
F118, and F175's derived angle closes the value. This is stated by the finding itself, and repeated
here because it is load-bearing for §15.5: **F234 explicitly supersedes F179's earlier relabelling**
(CN3), under which $\lambda_6$ had been judged "not reducible to a first-principles number" and the
spectrum downgraded to "a one-angle fit." $\lambda_6$ *is* reducible — via the derived $\delta^*$.

**Why adopt weight-as-phase, rather than continue to treat $\delta^*=\tfrac29$ as merely a
striking numerical target? The precursor search, and why it closed negative.** Two weeks before the
principle's formal adoption, a first attempt tried to *derive* the identification dynamically, via
"saturation self-duality": F176 posits that the condensate's angular invariant $3\delta$ equals its
radial invariant $Q$; F177 tests this against the model's own BPS/Bogomolny structure and finds it
**half-derivable**: the *radial* half ($Q=\tfrac23$) genuinely follows from Bogomolny self-duality —
the pair rotation's $45°$ peak (F82, R15.11) is exactly the self-dual point $\sin\phi=\cos\phi$ — but
the *angular* half ($3\delta=Q$) is **not** a standard Bogomolny consequence: Bogomolny fixes domain-
wall tensions, not the vacuum angle, which remains the ordinary Landau minimiser $\cos3\delta^*=-B/2C$.
F199 then attacks the angular half directly and closes it **negative on three independent structural
grounds**: (S1) there is no F92-style second kinematic relation — the Koide ratio $Q$ is *exactly*
$\delta$-independent ($\partial Q/\partial\delta\equiv0$, sympy-exact), so nothing forces the angular
minimiser to equal it; (S2) the IR coupling does not cancel in $C/|B|$ — the cubic $B$ is a
parameter-free, $O(\alpha^0)$ Dirac-sea loop while the sextic $C$ is an $O(\alpha^{\ge1})$ **induced**
coupling (F150), so their ratio carries the coupling undiluted and is a *computed* nonperturbative
number, never an algebraic identity; (S3) the BPS wall/bulk degeneracy is quantitatively at the
vacuum-existence threshold $C/|B|=\tfrac12$, not at the self-dual $0.636$. F200 then builds the actual
end-to-end saturated-condensate computation this whole line calls for — assembling $C/|B|$ from the
full nonperturbative sea cubic, the saturation amplitude, a freshly recomputed IR coupling, and the
induced sextic $\lambda_6=\tfrac29c$ (the sextic/quartic ratio of the $E_g$ composite *is* the F145
Fierz rational, matching F118's independent fit to $0.6\%$) — landing at $C/|B|=0.69$ central with a
residual band $[0.47,0.75]$ that brackets **both** the self-dual value ($0.63622$) and the competing
$2/\pi$ ($0.63662$, a $4\times10^{-4}$ split): the computation is real, converges to the right
neighbourhood, and genuinely **cannot discriminate** the two candidates — confirming F199's structural
verdict with an actual number rather than an argument.

**The forcing argument: three findings close every alternative route (F253, F255, F256).** With the
dynamical route shown computed-not-algebraic (F199/F200), a second, sharper pass — the one CLAUDE.md
decision 7 and `supersessions.yaml` records S6/S15 actually cite — attacks the two remaining logically
possible routes by which $\tfrac29$ *radians* could arise without being adopted as a principle.

*Route 1: saturation equipartition (F253).* Modelling the generation order parameter as a unit vector
in the full 9-dimensional bilinear, "saturation" (maximal democracy over the 9-dimensional space) does
give the $E_g$ channel weight $\tfrac29$ — but turning a *weight* into an *azimuth* (a radian) needs
one further statement, isolated as **POSIT-N**: the $E_g$ rotation generator is normalized so the
full-bilinear democratic phase budget equals exactly one radian. Given POSIT-N, $\delta^*=\tfrac29\,
\text{rad}$ exactly; without it, $\delta=\tfrac29\,R$ for a free generator-norm ratio $R$ — scale-
degenerate. **No $O(1)$ combination of the saturation data supplies $R=1$.**

*Route 2: a scale-free topological origin (F253).* If $\tfrac29$ radians arose as a genuine holonomy
(winding number), it would beat the normalization problem entirely — a holonomy *is* intrinsically an
arc/radius ratio. It does not: the only $E_g$ holonomy the BCC second shell's actual $C_3$ action
produces is exactly $2\pi/3$ (a rational multiple of $\pi$); $\tfrac29$ enters *only* as a scale-free
representation **multiplicity**, and is not any low-order quantized phase $2\pi p/q$ ($q\le24$).

$$\boxed{\;\text{the only }E_g\text{ holonomy on the BCC second shell is }2\pi/3;\quad\tfrac29\text{ is a multiplicity, not a winding — topological escape excluded}\;}\tag{R15.18}$$

*Half the normalization problem is then solved, not merely posited (F255).* Checking POSIT-N against
the F118 functional directly: the lepton amplitude deviations $p_a=\sqrt{m_a}-\overline{\sqrt m}$ lie
**exactly** in the $E_g$ plane ($\perp(1,1,1)$ to $2.3\times10^{-16}$), and because $E_g$ is a
genuine 2-dimensional *irreducible* representation of $O_h$, Schur's lemma forces its invariant metric
to be isotropic — the $O_h$ generators act **orthogonally** on the doublet ($D^\mathsf{T}D=\mathbb1$ to
$4.4\times10^{-16}$). An isotropic metric is angle-preserving under any overall rescaling, so:

$$\boxed{\;R=1\text{ is forced by Schur-isotropy of the }E_g\text{ irrep metric — a theorem, not a posit; the condensate phase is a genuine, canonical radian}\;}\tag{R15.19}$$

F253's POSIT-N is thereby split cleanly into a *derived* half (the normalization) and one remaining
open half (does the canonical angle equal the weight): the residual has shrunk from "a normalization
and an identity" to a single dimensionless coupling, $\lambda_6=0.243$.

*The dynamical route to that one remaining coupling is then closed too (F256).* Directly attempting to
derive $\lambda_6=0.243$ shows the request is structurally misposed. In the **dynamical** picture
($\delta$ set by the Landau minimiser), $B$ (sea, $O(\alpha^0)$) and $C$ (induced, $O(\alpha^{\ge1})$)
have independent physical origins with no locking mechanism, so $3\delta^*=Q$ can be, at best, the
observed $1.7\times10^{-5}$ near-coincidence (R15.14) — never an exact identity; and the $\lambda_6$
*required* for the exact match sits strictly between the model's only two available $O(1)$ rationals
(the Fierz $\tfrac29=0.222$ and the rotor $\tfrac14=0.250$), matching neither. In the **weight-as-
phase** picture, $\lambda_6$ is instead an *output* of the derived angle (F234, R15.17) — derivative
by construction. **$\lambda_6$ is derivative in both pictures**; there is no fundamental target left
to compute:

$$\boxed{\;\text{Route (I) [dynamical] cannot be exact}\ \Rightarrow\ \text{exact closure of }\delta^*=\tfrac29\text{ can come ONLY from the weight-as-phase principle}\;}\tag{R15.20}$$

**The three-way closure, assembled.** F253 excludes the topological route and localizes the
equipartition route to a single normalization constant; F255 proves that constant is not free — it is
forced by Schur-isotropy of the irrep metric, upgrading half the residual from posit to theorem; F256
proves the *other* half — the weight-identity itself — cannot be obtained from the dynamical Landau
route, because its two ingredients live at different orders in the IR coupling and therefore cannot
lock exactly. **Every alternative to weight-as-phase is closed.** This is precisely CLAUDE.md's own
stated rationale for adopting it as a founding principle rather than continuing to search for a
derivation: "we adopt as a principle... because every alternative route is closed."

$$\boxed{\;\textbf{Weight-as-phase is adopted}: \delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29\text{ rad — the canonical }E_g\text{-plane angle IS the representation weight it carries}\;}\tag{R15.21}$$

### 15.2.7 The calibrated spectrum, and precision

**F120/F121 — calibration, and the sharp lesson that the electron is the wrong anchor.** With the
shape fixed ($\delta$, $\eta^2$), one measured mass sets the overall scale $N$. F120 shows this
concretely and finds a sharp, general lesson: the electron sits near the condensate's *node*
(where $|\partial\ln m/\partial\delta|$ is $\sim10\times$ larger than the muon's), so anchoring on it
amplifies any residual angle uncertainty enormously (a $2.7\%$ error in the model's own first-
principles angle inflates to a $+104\%$ error in $m_\mu$). The $\tau$, by contrast, is **exactly**
$\delta$-stable — it sits at the wall-pinned saturation point ($y_\tau=1$ for *all* $\delta$, R15.12),
so anchoring on it contributes **zero** angle sensitivity:

$$\boxed{\;\tau\text{-anchored (}\delta=12.733°\text{ measured): }m_\mu=105.6575\text{ MeV }(-0.00\%),\ m_e=0.51069\text{ MeV }(-0.06\%)\;}\tag{R15.22}$$

F121 formally adopts the $\tau$-anchored readout as the project's standard mass-sector output, with a
full fermion table in kg (electron/muon/tau predicted from the shape; quark masses a converted
consistency readout, not a prediction — the shape mechanism does not extend to quarks, §15.5). Free
inputs at this stage: exactly two — the overall scale $N$ (fixed by the $\tau$ anchor) and the
condensate angle $\lambda_6$ — the identical accounting §15.1 already gives, now with $\lambda_6$
derived rather than fitted (R15.17).

**F348 — the residual is quantified, and shown to be a measurement floor, not a missing term.** The
$0.007\%$ residual on $m_\tau/m_e$ (R15.16) is, in MeV, $+0.125$ MeV against the current PDG
uncertainty $\pm0.12$ MeV:

$$\boxed{\;m_\tau/m_e\text{ residual}=1.04\sigma\text{ of current PDG }m_\tau\text{ precision}\;}\tag{R15.23}$$

statistically indistinguishable from measurement noise today. A numeric Jacobian check confirms both
mass-ratio residuals (the $0.001\%$ *and* the $0.007\%$) trace to a **single** small offset between
the exact $\{\delta^*,\eta^2\}$ and the free 2-parameter fit values (already flagged, unquantified, in
F175), reconstructing both to $<0.01\%$ relative error — one joint tension, not two independent gaps.
F256's route-(I) no-go (R15.20) independently rules out any computable in-model correction to
$\delta^*$, so the honest verdict is a quantified precision floor with a named, falsifiable re-attack
condition: distinguishing this residual from zero needs the $m_\tau$ world-average uncertainty to
tighten by $\sim1.9\times$ (for $2\sigma$), $\sim2.9\times$ ($3\sigma$), or $\sim4.8\times$ ($5\sigma$).

### 15.2.8 Cross-sector link: the lepton scale tracks $\Lambda_\text{QCD}$

**F170 — the lepton/colour scale coincidence is a mechanism, not a numerology.** An earlier finding
(F144, not itself assigned to this chapter) had *identified* the colourless lepton mass scale $N$ with
the colour transmutation scale $\Lambda_\text{QCD}$, without explaining why a sector carrying no
colour should track one that does. F170 supplies the mechanism: **(i)** the $E_g$ condensate has no
independent contact coupling of its own — its self-couplings are induced by the strong sector (F145,
F150, §15.2.5), so there is no separate lepton-sector scale to begin with; **(ii)** comparing gap-
kernel criticality integrals for the $E_g$ (lepton) and s-wave (colour $\chi$SB) channels on the exact
BCC lattice gives a ratio converging to $1.08$ as the lattice size grows — the two channels reach
criticality at essentially the same running coupling, within a factor $\sim1.3$:

$$\boxed{\;v_{E_g}=O(1)\times\Lambda_\text{QCD}\;}\tag{R15.24}$$

The colourless lepton condensate inherits the colour scale because it possesses **neither** an
independent coupling **nor** a kinematics that could produce a different one — the model's own version
of extended-technicolor "feeding." The exact residual $O(1)$ factor (measured $m_\tau/\Lambda\sim3.4$–
$5.7$) is not a new free number: it is the **same** shared saturated-condensate IR residual as
$\lambda_6$ (§15.2.5–15.2.6), not an independent input.

## 15.3 Results table

| # | Statement | Status | Exactness | Source |
|---|---|---|---|---|
| R15.1 | Exactly 3 generations $=\dim(T_{1u})$; $O_h$ has no 4-dim single-valued irrep, a 4th is forbidden | theorem | exact | F75 (8/8) |
| R15.2 | F75's condition (i) is forced vacuous under the model's site-diagonal charge coupling; the physical identification remains a hypothesis, now shown not closeable by F75's own criterion | theorem (narrowing) | exact | F342 (11/11) |
| R15.3 | $\cos^2\theta=1/(3Q)$: Koide $Q=2/3$ is exactly the 45° equipartition of $\sqrt m$; 3 distinct masses require the orthorhombic $D_{2h}$ break | identity + structural | exact | F76 (6/6) |
| R15.4 | Flatness $\kappa\to0$ interpolates the cubic ($Q=1/3$) and orthorhombic ($Q=2/3$) endpoints; the order parameter is one and the same as R15.3's break | structural | exact | F84 (4/4) |
| R15.5 | Pair-sum kinematics $m_H=\sin(\arcsin m_1+\arcsin m_2)$; stability ceiling at $m_c=1/\sqrt2$ | exact identity | exact ($\le4\times10^{-51}$) | F73 (6/6) |
| R15.6 | 3-D binding threshold $g_c$, exact $E_b(g)$; gauge sector $\sim10^5\times$ too weak, deep binding needs $\sim10^{-33}$ fine-tuning | quantified no-go | machine ($1.3\times10^{-15}$) | F74 (6/6) |
| R15.7 | Self-consistent NJL+RPA: $m_\sigma\ge2m_c$ at every coupling (chiral limit exact) — Higgs-from-$t\bar t$ structurally excluded, not merely disfavoured | theorem | exact/machine ($2.3\times10^{-14}$) | F77 (14/14) |
| R15.8 | $m=y^2$ bilinear condensate law; data select power $s=1/2$ uniquely | derivation + data | exact/quant. | F78 (6/6) |
| R15.9 | $Q(\phi)=1/(3\cos^2\phi)$; SO(2) unification of the F73 cap and Koide; EM/colour selection pattern | identity + pattern | exact | F80 (4/4) |
| R15.10 | $Q_N=1/(3\cos^2(\pi/2N))$; data select $N=2$ uniquely (residual $6\times10^{-6}$) | derivation + data | exact | F81 (4/4) |
| R15.11 | Composite mass peaks at 45° for any coupling $\lambda>0$; exact 45° $\iff$ flat direction | derived + data | exact | F82 (4/4) |
| R15.12 | Consistency theorem: L1+L2+Fock $\Rightarrow$ $t=45°$ unique; F73 cap = pair-amplitude unitarity; data pin $c^2=2.000018$ | theorem | exact/data | F92 (5/5) |
| R15.13 | Splitting field uniquely $E_g$; lives on 2nd shell; generic stabilizer $D_{2h}$ has no axis-permuting elements ($\kappa=0$ theorem); sextic required (quartic never works); break must be spontaneous | theorem (4-part) | exact | F93 (8/8) |
| R15.14 | $B=-3\sqrt2I_2\bar y^4$, sign derived; $C$ excluded from any per-axis energy (31-decade lock) | derivation + no-go | exact/$1.4\times10^{-4}$ | F95 (7/7) |
| R15.15 | Two-value theorem: quadratic gap theory admits $\le2$ distinct masses — excluded by data; massless texture $Q=2/3\iff\delta=15°$ exact; sextic invariant sufficient | theorem + exact + sufficiency | exact | F96 (8/8) |
| R15.16 | Sea cliff forces $y_\tau=1$ exactly — $\tau$ mass IS the saturation scale; closed-form coupling family, $W^*\approx1.46$–1.5 (two routes converge) | theorem + fit | exact | F101b (6/6) |
| R15.17 | No democratic invariant closes stability at any strength (exact floor $\Delta_\infty=0.0386$); $\{v,c\}$ quartic pair globally stable at fixed $W^*$; momentum bubble wrong-sign at one loop | no-go + sufficiency + no-go | exact | F108 (11/11) |
| R15.18 | Pair-sum law derived from $U\otimes U$ spectrum theorem (not assumed); 45° is the unique flow attractor; condensation reproduces the measured decomposition | theorem + dynamics | exact/data | F109 (5/5) |
| R15.19 | Self-consistent $(W,v,c)$ triple closes on $\kappa_E<0$ branch — physically required sign; $\kappa_E>0$ excluded everywhere; couplings $O(1)$ over 2D region; $\lambda_6=0.243$ | closure | exact ($-2\times10^{-6}$) | F118 (8/8) |
| R15.20 | Mass is the unique EW channel-splitting agent; free-sea charge counting eliminated by exact rational factors ($\times8/7$, $\times10/21$) | theorem + no-go | exact/machine | F149 (8/8) |
| R15.21 | Two-route no-go: $C$ cannot come from the free sea at all (F95+Ch.12's F147); $\lambda_6$ is an induced coupling (resolves the F115 "notation collision"); target $3\delta^*=Q$ to $1.7\times10^{-5}$ | no-go + reclassification | exact ($1.7\times10^{-5}$) | F150 (5/5) |
| R15.22 | $\delta^*=2/9$ rad derived exactly as the $E_g$ representation weight; zero-shape-parameter spectrum to $\le0.007\%$ | **derivation** | exact ($O_h$ group theory) | F175 (5/5) |
| R15.23 | $(W,v,c)$ triple closed: $\lambda_6=0.243$ from $\delta^*=2/9$ via the derived $B$ — output, not fit; supersedes F179/CN3 | closure | exact (to the digit) | F234 (5/5) |
| R15.24 | Precursor: self-duality principle $3\delta^*=Q$ posited; BPS closes the radial half exactly, not the angular half | posit + partial derivation | exact (radial) | F176/F177 (8/8 combined) |
| R15.25 | Three-ground structural no-go on the dynamical angular derivation: no second relation exists; IR coupling doesn't cancel; BPS wall sits at $1/2$ not $0.636$; data at self-dual to $10^{-5}$ ($0.89\sigma$) | no-go | exact | F199 (5/5) |
| R15.26 | End-to-end saturated-condensate computation: $\lambda_6=\tfrac29c$ (sextic/quartic = Fierz rational, 0.6% match); assembled $C/\lvert B\rvert=0.69$, band brackets both candidate values — confirms cannot discriminate | computation | exact (structure)/quant. (value) | F200 (5/5) |
| R15.27 | Equipartition route reduces to POSIT-N (a normalization), not supplied by saturation data; topological route excluded (only holonomy $2\pi/3$; $2/9$ is a multiplicity) | no-go (2 routes) | exact | F253 (5/5) |
| R15.28 | $R=1$ forced by Schur-isotropy of the $E_g$ irrep metric — the condensate phase is a genuine, canonical radian | **theorem** | exact ($4.4\times10^{-16}$) | F255 (4/4) |
| R15.29 | "Derive $\lambda_6$" is misposed: dynamical route cannot lock exactly (different coupling orders); weight-as-phase route makes it an output — only the principle can close E1 | **theorem/dichotomy** | exact | F256 (4/4) |
| R15.30 | Electron is the worst mass anchor (condensate node, $\sim10\times$ sensitivity); $\tau$ is exactly $\delta$-stable (wall-pinned) — adopted as canonical anchor | derivation + adoption | exact/quant. | F120/F121 (12/12 combined) |
| R15.31 | $m_\tau/m_e$ residual is a $1.04\sigma$ measurement-floor effect, not a missing term; F256's no-go rules out any computable correction; named re-attack thresholds | quantification | data | F348 (5/5) |
| R15.32 | Lepton scale tracks $\Lambda_\text{QCD}$ to $O(1)$: no independent coupling (induced) + near-degenerate gap-kernel criticality ($\to1.08$) | mechanism | exact/quant. | F170 (4/4) |

## 15.4 Comparison with measurement

**The headline number.** Using only the derived pair $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ — zero
fitted shape parameters — the charged-lepton mass ratios reproduce PDG 2024 values to

$$m_\mu/m_e:\ +0.001\%,\qquad m_\tau/m_e:\ +0.007\%$$

(R15.16, F175 D4, reproduced independently in F234 §3). This is not a post-hoc fit: $\delta^*$ is pure
$O_h$ group theory and $\eta^2$ is independently pinned by the pair-consistency theorem (R15.9) to
$1.9\times10^{-5}$. Koide's ratio, an independent function of $\eta^2$ alone, comes out
$Q=0.666667$ exactly against the measured $Q=0.666661$ ($0.91\sigma$).

**The $\tau$-anchored canonical readout** (F121, adopted as the project's standard) reproduces
$m_\mu$ to $-0.00\%$ and $m_e$ to $-0.06\%$ from the single $\tau$ anchor, with zero angle sensitivity
in the anchor itself — the sharpest available cross-check that the shape, not the anchor choice, is
carrying the prediction.

**The residual is quantified, not hand-waved.** F348 places the $0.007\%$ $m_\tau/m_e$ discrepancy
precisely at $1.04\sigma$ of the current PDG $m_\tau$ world-average uncertainty ($\pm0.12$ MeV) — not
currently distinguishable from measurement noise, and shown (by a numeric Jacobian) to be the single
joint consequence of a $\sim10^{-5}$-radian offset already visible in the free two-parameter fit
(F174 S4), not two independent unexplained corrections. F256 independently rules out any computable
in-model correction (§15.2.6, R15.20), so this is reported as an honest precision floor with a stated
re-attack condition, rather than either claimed as exact agreement or left as an unexplained residual.

**What is a prediction, and what is a consistency readout.** Per F120/F121, only the charged-lepton
*shape* is predicted this way; the overall mass *scale* is set by one measured anchor (forward-cited
to Chapter 17 for the first-principles closure), and the quark masses tabulated alongside the leptons
in F120/F121's tables are the **measured** values converted to kg — a consistency readout, since
§15.5 below shows the shape mechanism itself does not transplant to quarks.

## 15.5 What was excluded, and why

**F108's democratic no-go excludes an entire class of stabilizing completions.** Before F118's closure
on the spontaneous-$E_g$ branch, the most natural fix for the F101b fit's metastability — add *some*
invariant built from the democratic amplitude $\bar y$ alone — was tested exhaustively and excluded
exactly, for any strength and any functional form (R15.17). This is not a narrow negative result: the
proof shows the splitting cost the lepton point pays cannot be offset by anything that leaves the
$(1,1,1)$ and $(0,0,0)$ competing vacua untouched, which every democratic-sector invariant does by
construction. The class of "just add a symmetric correction" theories is closed as a matter of
algebra, redirecting the search toward the condensate's own non-quadratic self-interaction — which is
exactly where F118 finds the closure.

**F342's internal gap in the generation-count identification.** F75's group theory is a theorem;
its physical reading ("generation index = $T_{1u}$ orbital") is, and per F342 remains, a stated
hypothesis. What F342 adds is not a weaker version of the same doubt but a *sharper* one: the
specific criterion F75 itself proposed to justify the identification (condition (i), shared gauge
quantum numbers) is shown to carry **zero** selecting power under the model's own adopted, site-
diagonal gauge coupling — a checked, falsifiable statement (with a declared control that correctly
reddens), not an impression. `docs/claims/CL004`'s status stays `contingent` because of this, not in
spite of it (§15.7). F342 is explicit this is a known-hard problem across the wider literature
attempting similar derivations (e.g. Furey's sedenion construction, which gets the same "$S_3$ factor
with unclear physical correspondence"), not an idiosyncrasy of this model.

**F346/F347's quark-sector non-transplant no-gos.** The weight-as-phase mechanism (§15.2.6) is
specifically a charged-lepton result, and two findings test directly whether it extends to quarks.
F346 inverts F175's exact circulant ansatz on both same-generation-type quark triplets
($u,c,t$ and $d,s,b$): the up-type fitted angle misses every candidate $O_h$ weight by
$>200\sigma$ — decisive — while the down-type angle sits a nominal $1.4\sigma$ from $A_{1g}=\tfrac19$,
a proximity current data cannot exclude but which a properly-scaled look-elsewhere calculation shows
is only a modest ($p\approx0.57\%$), not overwhelming, coincidence, with no independent theoretical
reason (unlike F80's EM-selection story for leptons) to expect that specific weight for down-type
quarks. Neither sector's fitted amplitude reaches the lepton's derived $\eta^2=2$, and the two quark
sectors disagree with each other. F347 extends this to the literature's *mixed*-generation-type
tuples: the historical Harari–Haut–Weyers $(u,d,s)$ Koide match relied on an assumption (massless up
quark) current data no longer support, and Rodejohann–Zhang's $(c,b,t)$ $Q\approx\tfrac23$ claim,
while numerically real, is shown to be blind to the phase information the lepton mechanism actually
needs — decomposed into $(\eta,\delta)$, it misses decisively on both axes. Together these are
**leaning no-gos, not full closures**: no alternative quark-sector mechanism (anchored to a different
mass definition, or incorporating the QCD condensate directly) has been tried, and the generation-
**count** question (whether quarks share the same $T_{1u}$ triplet structure, independent of the
shape mechanism) remains untouched and open.

**F352's Higgs-compositeness negative result.** §15.2.2 already showed the direct Cooper-pair
construction cannot reach 125 GeV at mean-field/RPA order (F77, R15.7). F352 closes the most obvious
escape — that renormalisation-group running, integrated over the model's own derived Planck-scale
lattice cutoff (F79/F107, no free scale choice), might rescue the identification — and finds it does
not: minimal single-channel top condensation predicts $m_t=226.56$ GeV ($+31.3\%$) and
$m_H=248.76$ GeV ($+98.6\%$, essentially double), reproducing the historically known failure mode of
minimal Bardeen–Hill–Lindner top condensation, independently, at a cutoff the model does not get to
choose. This is not a re-litigation of the negative; it is the "maybe RG running rescues it" escape
hatch closed with an actual computed number rather than an assumption. A literal lattice Bethe–
Salpeter ladder (vertex corrections beyond RPA) remains untried and is the one channel this chapter's
own findings name as still capable, in principle, of behaving differently.

**Supersession: F179 and F230, per `supersessions.yaml` S6 and S15.** Two earlier findings are routed
out of this chapter's main line, per `docs/theory/supersessions.yaml`. **F179** (the "$\lambda_6$ not
reducible / spectrum is a one-angle fit" relabel) is superseded by the F253/F255/F256 trio
(record **S6**): what F179 correctly diagnosed — that no clean rational for $\lambda_6$ was then
available — is now understood not as a permanent limitation but as the *reason* weight-as-phase must
be adopted rather than fitted (§15.2.6); nothing of F179's content is separately retained (S6's
`retained:` field is empty). **F230** (an earlier crystal-field attack on the same angular problem) is
likewise superseded by the same trio (record **S15**): F230's contribution — sharpening the
obstruction to "a radian cannot equal a pure ratio without a scale" — survives as the precise
statement F253's POSIT-N names and F255 then proves forced (R15.19), but F230 itself is not part of
this chapter's main line. Both supersessions are consistent with this chapter's own framing: the
adoption of weight-as-phase is presented throughout §15.2.6 as the resolution these two earlier,
now-superseded attempts were reaching for.

## 15.6 What is still open

1. **The generation-identification hypothesis itself.** F75's group theory fixes the *count*; F342
   shows the model's own criterion for fixing the physical *identification* (which shell states are
   generations) is currently vacuous. The constructive path F342 names — an $O_h$-invariant,
   non-diagonal (orbital-shape-dependent) gauge coupling in the adopted engine — does not currently
   exist anywhere in the tree. `docs/claims/CL004` stays `contingent` on this basis.
2. **The overall mass scale.** Nothing in this chapter fixes $N$ (the map from dimensionless lattice
   mass to MeV); this is the direct continuation of Chapter 11's R11.14, forward-cited in full to
   Chapter 13 (dimensional transmutation of the strong coupling) and Chapter 17 (SI-scale closure).
3. **The quark-sector shape mechanism.** F346/F347 close off the two most literature-prominent
   quark-triplet Koide groupings as direct transplants of this chapter's mechanism, but do not
   exhaustively search the combinatorial space, do not test Rivero's signed-ansatz variant, and do not
   attempt a quark-native mechanism built on a different mass definition (e.g. the constituent rather
   than current mass) or incorporating the QCD condensate.
4. **Precise closure of Chapter 12's F49 electroweak channel-splitting ratio.** F149 (R15.20)
   establishes that mass is the unique agent capable of splitting the relevant channels and eliminates
   free-sea charge counting exactly, but does not itself complete the numerical calculation of the
   $8/7$ bookkeeping factor from the saturated condensate — the architecture this chapter builds
   (§15.2.5) is what such a calculation would use, but it has not yet been run.
5. **The direct value of the completion couplings $(v,c)$ within F118's stable 2D region.** F118
   shows a robust region of couplings closes the flavor functional, and F200 shows $\lambda_6=\tfrac29c$
   reduces the sextic to the quartic $c$ — but $c$ itself is not derived from first principles; it is
   the same shared nonperturbative residual named throughout §15.2.5–15.2.6.

## 15.7 Falsifiers

**CL028** (the headline card this chapter's central derivation rests on, `tier: headline`, `status:
live`, `exactness: exact`) states its falsifier explicitly and without qualification: a charged-lepton
mass measurement inconsistent with the $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ shape at better than
$0.007\%$ would falsify it — and because $\delta^*$ is an exact rational fixed by $O_h$ representation
theory (not a re-fittable parameter), there is no adjustable slack to absorb such a discrepancy. Per
`docs/theory/key-decisions.md` decision 7, the model's own stated falsification handle is precise: an
improved $m_\tau$ measurement that moves the effective $\delta^*$ off $\tfrac29$ would falsify the
principle — currently sitting at $-0.89\sigma$ ($0.003\%$), a number this chapter's own F348 sharpens
(the closely related $m_\tau/m_e$ mass-ratio residual sits at a numerically distinct but consistent
$1.04\sigma$; §15.6 Gap G-9 below flags that these related-but-not-identical $\sigma$ figures, drawn
from three different invariants — $\delta^*$ itself, the Koide ratio $Q$, and the mass ratio $m_\tau/m_e$
— have never been reconciled into one canonical number in the source material). F348's named
re-attack condition (a $\sim2$–$5\times$ tightening of the $m_\tau$ world average) is this chapter's
concrete, dated falsification programme.

**CL005** (F92, F93; `live`, `exact`) — the Koide-as-45°-equipartition claim — carries the same
$0.007\%$-class falsifier implicitly, since $Q=2/3$ is a direct consequence of $\eta^2=\tfrac12$.

**CL004** (F75, F292, F342; `contingent`, `exact`) — exactly three fermion generations — is falsified
group-theoretically (not observationally) if a rigorous re-derivation under the model's actual axioms
yields a fourth admissible symmetry-protected multiplet; falsified in its *identification* (not its
count) if F342's constructive route (§15.6 item 1) is closed the wrong way, or, per F75's own §7,
if a future experiment finds a genuine sequential fourth generation, which the model's group theory
would then have to accommodate or fail.

**CL293** (F352; `no_go`, `live`, `quantitative`) is not this chapter's headline falsifier but is
directly relevant: it is a *closed* negative result (minimal top condensation excluded at the model's
own cutoff), not an open falsifiable claim of this chapter's own construction.

> **Gap [G-10]:** The falsification handle for weight-as-phase is quoted with at least three
> numerically distinct — though closely related — $\sigma$ figures across the source material:
> $-0.89\sigma$ (`docs/theory/key-decisions.md` decision 7, for $\delta^*$ directly, $0.003\%$),
> $0.91\sigma$ (F76 §4/F174, for the Koide ratio $Q$, $6.2\times10^{-6}$ absolute), and $1.04\sigma$
> (F348, for the $m_\tau/m_e$ mass-ratio residual, $+0.125$ MeV). These are three different
> observables (an angle, a dimensionless ratio, and a mass ratio) sensitive to the same underlying
> $\sim10^{-5}$-radian offset between the exact $\{\delta^*,\eta^2\}$ point and the free-fit values
> (F174 S4), and F348's own Jacobian check (R15.31) shows they are the *same* single tension expressed
> three ways — but no source read for this chapter states this explicitly or collects the three
> figures into one canonical statement of "how many sigma is the model currently at." A reader citing
> "the" falsification-handle figure for weight-as-phase should be aware which of the three observables
> it refers to. Not fixed here (documentation-only); flagged for whoever next updates
> `docs/theory/key-decisions.md` decision 7 or CL028 to state precisely, in one place, which invariant
> each quoted $\sigma$ tracks, and ideally to note that they are consistent restatements of one offset
> rather than three independent tensions.

---

## Notation established or extended in this chapter

| Symbol | Meaning | First used |
|---|---|---|
| $T_{1u}$ | The unique odd-parity 3-dimensional irrep of $O_h$; the generation multiplet | §15.2.1 (F75) |
| $E_g$ | The 2-dimensional $O_h$ irrep carrying the generation-splitting order parameter, on the BCC second-neighbour shell | §15.2.1/§15.2.4 (F93) |
| $Q$ | The Koide ratio $\sum m_a/(\sum\sqrt{m_a})^2$; $Q=2/3$ is the 45° equipartition point | §15.2.1 (F76) |
| $y_a=\sqrt{m_a}$ | The pairing/condensate amplitude carrying the $T_{1u}$/$E_g$ vector quantum numbers | §15.2.3 (F78) |
| $\phi,\ t$ | The generation-space rotation angle / per-constituent pair phase; $45°$ is the universal equipartition point | §15.2.3 (F80, F81) |
| $\bar y,\ e,\ \delta$ | The $E_g$ condensate's democratic ($A_{1g}$) amplitude, splitting ($E_g$) magnitude, and phase angle | §15.2.4 (F93) |
| $B,\ C,\ \lambda_6$ | The cubic and sextic Landau invariants of the $E_g$ condensate; $\lambda_6\equiv C/e^6$, the sextic clock coupling | §15.2.4–15.2.5 (F95, F118) |
| $\delta^*$ | The physical (saturated-condensate) value of $\delta$; adopted as $=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad | §15.2.6 (F175) |
| POSIT-N | The (now-derived, R15.19) statement that the $E_g$ generator norm $R=1$ | §15.2.6 (F253, F255) |
| $\eta^2$ | The equipartition amplitude, $\sin^2t^*=\tfrac12$ at the pair-saturation angle $t^*=45°$ | §15.2.3–15.2.4 (F92) |
| $N$ | The overall fermion mass scale (dimensionless lattice mass $\to$ MeV); left free by this chapter, forward-cited to Ch.13/17 | §15.1, §15.6 |
