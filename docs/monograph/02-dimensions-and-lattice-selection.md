# Chapter 2 — Why 3+1 Dimensions, and Why This Lattice

*Chapter 2 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F267-walk-bz-measure-not-the-fft-cube.md`, `findings/F273-mode-sum-vs-bz-integral-audit.md`,
`findings/F278-bcc-lattice-constant-two-over-root-three.md`,
`findings/F291-why-three-plus-one-dimensions.md`, `findings/F292-no-higher-multiple-of-three.md`,
`findings/F313-one-time-dimension-from-the-update-commutant.md`,
`findings/F315-V-does-not-survive-interaction.md`, `findings/F316-laurent-pell-descent-proved.md`,
`findings/F318-cell-carries-the-internal-index.md`,
`findings/F326-the-plus-one-closes-no-second-generator.md`,
`findings/F344-bcc-walk-point-symmetry-d4h.md` — the eleven findings `00-plan.md` §2 assigns to
this chapter, checked directly against `docs/theory/supersessions.yaml` (none of the eleven
appears in any of the 23 records) and against `claims-index.md` (claim cards CL246, CL247, CL269,
CL270, CL272, CL020 rest on this chapter's findings; their `review_state`/`status` are reported
verbatim below rather than smoothed over). Notation, postulates and results are those of
`docs/monograph/01-postulates-and-ontology.md` — $\mathbf x$, $t$, $a$, $\tau$, $\psi$,
$\sigma^i$, $G$, $L$, $\mathcal U$, $H$, $c_\text{lat}$ — extended, never redefined.

## 2.0 What this chapter establishes

Postulate **P3** fixed that *some* homogeneous, isotropic lattice geometry exists, with *some*
finite point-symmetry group, but explicitly left the dimension count, the specific lattice, the
lattice constant and the point group all open — "that further selection is a derived result, not
a postulate" (Ch.1 §1.2, P3). This chapter is that derivation. It shows: (i) the model's own
already-adopted structure — not an appeal to the founding QCA uniqueness theorem alone — pins the
spatial dimension at exactly $d=3$, twice over, and excludes every higher multiple of three; (ii)
the "+1" (exactly one time dimension) is not asserted by construction but computed, as the
commutant of the update itself, and the computation survives being asked in its strong,
interacting form; (iii) the resulting lattice is body-centred cubic with lattice constant
$a=2/\sqrt3$ in lattice-native units, a number that turns out to already be sitting unnamed in
the code as $2c_\text{lat}$; (iv) the lattice's geometric neighbour shell is an exact $O_h$ orbit,
but the specific unitary dynamics BDPT forces onto it realizes only $D_{2h}$ (or $D_{4h}$, on a
weaker criterion) exactly, with full $O_h$ recovered only as the leading-order (infrared) limit —
a distinction later chapters must not blur; (v) the same minimal cell has room, at zero
dimensional cost, for an internal (colour) index of a specific shape, though nothing in the
lattice's geometry forces that index to exist; and (vi) the array most of the tree's own code
actually runs on (the cubic FFT grid) is *not* the BCC crystal's true Brillouin zone, a correction
that matters for how later chapters read their own mode sums.

## 2.1 Inputs

**Postulates used.** **P1** (discreteness) and **P2** (locality) throughout — F313's central move
is the identification "local $\equiv$ Laurent polynomial," which is P2 made algebraic. **P3**
(homogeneity/isotropy of *some* lattice, dimension/lattice/point-group left open) is the postulate
this whole chapter discharges. **P5** (the primitive field is a massless two-component complex
spinor) supplies the minimal cell dimension $s=2$ that every derivation below leans on. **P6**
(mass and hypercharge from a gauged chiral $SU(2)$ connection, not a Higgs field) is used as a
premise inside F291's lower-bound argument (§2.3.2 below) — the requirement that a complex mass
phase exist to gauge is exactly what forces $d\ge3$.

**Prior results used.** None in the monograph's own numbering — Chapter 1 fixes postulates only,
no numbered `R` results. This chapter's own results (`R2.1`–`R2.12`) are the first in the series.

**Free inputs consumed, stated precisely.** Four, and they are not all of the same kind:

1. **$s=2$, the minimal spinor cell**, is not derived anywhere in this chapter or its source
   findings — it is BDPT's own minimality axiom (cited, not re-proved; Ch.1 P5's forward pointer:
   "Chapter 2/Chapter 4 carry the QCA-literature uniqueness proof in full rigor — the $s=2$ result
   is not re-derived here"). Every dimension-count result below is conditional on it, and F291's
   own stated boundary is exact about the price of losing it: "losing S3 *and* $s=2$ together
   would reopen the question" (`findings/F291-why-three-plus-one-dimensions.md` §7).
2. **The specific BCC solution at $(s,d)=(2,3)$ is BDPT's uniqueness theorem, imported.** BDPT
   obtain one walk in each of $d=1,2,3$ at $s=2$ — "the trivial shift, the square-lattice walk, and
   the BCC walk … uniqueness holds within a dimension" (F291 §1, citing
   `references/qca-papers-1-4-overview.md`). That BCC, not some other isotropic 3-D lattice, is the
   $d=3$ solution is this imported theorem's content, not something re-derived in the findings
   assigned to this chapter.
3. **Infinite volume**, load-bearing specifically for the time-dimension count (F313 §2, flagged
   by its own 2026-08-13 review as previously undeclared): on a finite periodic lattice the Laurent
   ring collapses to a non-domain, units stop being monomials, and the whole commutant argument for
   $d_\text{time}=1$ fails. §2.4 below states this every time the result is used.
4. **The lattice constant's dimensionless value, $a=2/\sqrt3$, is fully forced** — not an
   independent input — once the hop-phase convention already used by the code's Weyl-walk
   Bloch matrix is read as a real-space translation (F278 §2). What is *not* fixed by anything in
   this chapter is the constant's **absolute SI value** (metres, seconds): that is the canonical
   lattice-spacing decision of `docs/theory/key-decisions.md` (F79/F107), reserved for Chapter 17.
   F278 itself is explicit that its result is "a dimensionless lattice-unit statement about the
   walk's geometry. It is **not** the canonical physical cell size of F107/F112 and carries no
   metres" (F278 §8).

> **Gap [G-2]:** Two of the premises load-bearing in this chapter's own source findings —
> CLAUDE.md's Core Design Decision 2 (the lattice speed of light $c_\text{lat}$ is *defined* as
> the rotation rate of the real $(\mathbf E,\mathbf B)$ vector pair) and Core Design Decision 5
> (the electromagnetic photon is specifically the paired-spinor construction) — are used directly
> in F291 §3 route (b) and §5 (S3) to help exclude $d\ge4$ and to supply the second, independent
> selector of $d=3$. Neither decision was promoted to a numbered postulate in Chapter 1: only
> CDD1/3 (→ **P6**) and CDD6 (→ **P7**) were. Chapter 1's own notation table lists $c_\text{lat}$
> and the paired-spinor photon only as *forward reservations* for Chapters 6 and 8 — and `00-plan.md`
> lists Chapters 6 and 8 as *depending on* Chapter 2 for exactly the dimension count this chapter
> derives using them. This is not a logical circularity — CDD2 and CDD5 are adopted conventions
> fixed by CLAUDE.md independently of $d$, not theorems Chapters 6/8 must first prove — but a
> reader checking "what this chapter assumes" against Chapter 1's P1–P7 table alone would miss two
> inputs this chapter actually uses. Flagged here and in `docs/monograph/GAPS.md` rather than
> silently patched by minting new P-numbers Chapter 1's build did not sanction.

## 2.2 The object every selector acts on

Postulate P5 fixes the per-cell field as $\psi\in\mathbb C^2$ ($s=2$). Write the one-tick update's
momentum-space (Bloch) representation in the Pauli decomposition BDPT use:

$$A(\mathbf k) = u(\mathbf k)\,\mathbb I - i\,\boldsymbol\sigma\cdot\tilde{\mathbf n}(\mathbf k),
\qquad u^2 + \lVert\tilde{\mathbf n}\rVert^2 = 1,$$

with $\mathbf k\in\mathbb R^d$ for now-unspecified $d$. $A(\mathbf k)$ is the Bloch-space
realisation of the abstract per-tick evolution $\mathcal U$ of Ch.1 P4, restricted to the free
single-particle sector; the two are the same object viewed at two levels, and $A$ is the notation
this chapter (following its source findings) uses throughout. Every dimension-count argument below
is a statement about the **Jacobian of the Bloch vector at the origin**,

$$J = \frac{\partial\tilde{\mathbf n}}{\partial\mathbf k}\bigg|_{\mathbf k=0} : \mathbb R^d \to \mathbb R^3.$$

$J$ has **three rows in every dimension**, because the traceless Hermitian part of a $2\times2$
matrix is a 3-dimensional real vector space (every such matrix is $\mathbf a\cdot\boldsymbol\sigma$
for a unique real $\mathbf a$), and the largest mutually anticommuting subset of that space has
exactly 3 elements (F291 §2). Both selectors below are statements about when this $3\times d$ map
is, respectively, injective and surjective.

## 2.3 The derivation

### 2.3.1 Why not $d\ge4$: the upper bound

For $d\ge4$, $J$ cannot be injective — three rows cannot have trivial kernel on
$\mathbb R^{d>3}$ — so $\ker J\ne0$ for some momentum direction $\mathbf k_0$, i.e. a
zero-energy propagating direction at leading order. Two independent routes close this off (F291
§3):

- **Route (a)** assumes the isotropy point group acts irreducibly on $\mathbb R^d$ (standard for a
  Bravais lattice, but a genuine premise, not proved in this chapter): then $\ker J$, being
  group-invariant, is either $0$ or all of $\mathbb R^d$, and the latter is the trivial (frozen)
  automaton.
- **Route (b)** needs no representation-theoretic premise, but does need $c_\text{lat}$ to be
  *definable* as a single number, $d\Omega/d\lVert\mathbf k\rVert$ at $\lVert\mathbf k\rVert\to0$
  (CDD2, flagged in Gap G-2 above): with $\ker J\ne0$ that limit is direction-dependent and does
  not exist, so the definition itself excludes $d\ge4$.

$$\boxed{\;d\le3\;}\tag{R2.1}$$

verified exactly for $d\in\{1,2,3\}$ against the BDPT Bloch vectors, re-typed independently of the
engine implementation (F291 check B1, test record `F291-dimension-selectors`, 9/9 PASS, gate
tier, `exact`).

### 2.3.2 Why not $d<3$: the lower bound

$\operatorname{coker}J=\mathbb R^3/\operatorname{im}J$ is the set of internal spin axes no
momentum direction ever rotates. Any $\hat{\mathbf m}$ in it is point-group-fixed, so
$H(\mathbf k)=\boldsymbol\sigma\cdot\tilde{\mathbf n}(\mathbf k)+m\,\boldsymbol\sigma\cdot\hat{\mathbf m}$
is an admissible isotropic mass term for a *single* Weyl branch whenever $\operatorname{coker}J\ne0$
— which is exactly $d<3$ (F291 §4). Hermiticity forces such a diagonal mass to be real, carrying
no phase. But **P6** requires a complex phase to gauge (Ludwig's chiral $SU(2)_L$, $m\to me^{i\beta}$),
and a phase survives Hermiticity only in an *off-diagonal*, inter-branch mass block — the two-branch
BDPT Dirac construction. So:

$$\text{a phase to gauge exists (P6)} \iff \text{mass is inter-branch} \iff \operatorname{coker}J=0 \iff d\ge3.$$

$$\boxed{\;d\ge3\;}\tag{R2.2}$$

checked forward and backward at $d=2,3$ (F291 checks B2/B3, same test record). A corollary worth
recording for later chapters: $J$ is square only at $d=3$, where
$\det J=\mp c_\text{lat}^3$, so the two-valued chirality/helicity label F291 traces to F91 *is* the
orientation of this map — there is no determinant, hence no handedness invariant, at any other $d$.

### 2.3.3 $d=3$, confirmed by a second, independent route

R2.1 $\wedge$ R2.2 already give $d=3$ (F291 checks B1–B3, test `F291-dimension-selectors`). A
logically separate route, mentioning neither $s$ nor the mass step, gives the same answer. CDD2's
$(\mathbf E,\mathbf B)$ vector pair (flagged in Gap G-2) requires the magnetic bivector and the
electric vector to have equal dimension:

$$\dim\Lambda^2\mathbb R^d = \dim\mathbb R^d \iff \tfrac{d(d-1)}2=d \iff d\in\{0,3\}\tag{exact, over the integers}$$

with $d=0$ trivial. This is not merely consistent with $d=3$; it independently forces it, and it
survives even if the $s=2$ minimality premise that R2.1/R2.2 lean on were ever dropped. (There is
no $d=7$ loophole: a cross product also exists in 7 dimensions, but it is the octonionic product,
not the Hodge dual the model's $\mathbf B$ actually is — $\dim\Lambda^2\mathbb R^7=21\ne7$.) The
paired-spinor photon of CDD5 (also Gap G-2) restates the same fact natively: its field strength is
a $\boldsymbol\sigma$-triplet, $\dim\mathfrak{su}(2)=3$ in any $d$, identifiable with a spatial
vector only at $d=3$.

$$\boxed{\;d=3,\ \text{two independent routes}\;}\tag{R2.3}$$

(F291 check C1, `exact`.) Losing either route (S1$\wedge$S2, or S3) leaves the other standing; only
losing S3 *and* $s=2$ together would reopen the question (F291 §7).

### 2.3.4 No higher multiple of three

Because the model already contains more than one "3" (three spatial dimensions, and — as later
chapters will show — three colours and three generations), the natural next question is whether
$d=6$ or $d=9$ survive as "three copies of three." They do not, and for two independent reasons
(F292):

- **The bivector overcount is a strictly increasing function of $d$** that passes through 1 exactly
  once: $\dim\Lambda^2\mathbb R^d/d=(d-1)/2=1 \iff d=3$. At $d=6$ it is $5/2$; at $d=9$ it is $4$.
  Neither can carry the vector $(\mathbf E,\mathbf B)$ pair, independent of the cell dimension $s$.
- **A chirality projector needs $D=d+1$ (spacetime dimension) even.** In odd $D$ the product of all
  gamma matrices is proportional to the identity and the Dirac representation does not split, so
  there is nothing for the chiral $SU(2)_L$ phase (P6) to act on. $d=6$ has $D=7$ (odd): no
  chirality at all, excluded outright, not a near miss. $d=9$ has $D=10$ (even): it clears this test
  and then dies on the bivector overcount above.

$$\boxed{\;d=6,\,9\ \text{excluded, by two independent mechanisms}\;}\tag{R2.4}$$

(F292 checks A1, B1–B3; test `F292-higher-multiples`, 8/8 PASS, gate tier, `exact`.) A useful
cross-check this produces for free: $d=2$ is excluded *twice*, once by the cokernel/mass argument
of §2.3.2 and once by the chirality-parity argument here — two unrelated mechanisms neither built
to test $d=2$ specifically, both rejecting it.

**The reducible case, $d=3n$ as $n$ separate copies of $\mathbb R^3$**, is the version of the
question that actually survives the longest, because reading $\mathbb R^{3n}$ as
$\bigoplus_b\mathbb R^3$ makes the point group act block-diagonally, which is exactly what §2.3.1's
route (a) premise (irreducibility) assumed away. It still fails, and the reason is informative
rather than a repeat: a 2-dimensional cell has exactly *one* $\boldsymbol\sigma$-triplet
($\dim\mathfrak{su}(2)=3$), so every block must map into the *same* internal $\mathbb R^3$, giving
$\operatorname{rank}J=3$ and $\dim\ker J=3(n-1)$ regardless of $n$ (F292 §4, check C1). **This is
not compactification** — there is no radius and no Kaluza–Klein tower — it is degeneracy: the
extra $3(n-1)$ directions carry no leading-order dispersion, and any coupling they could carry
enters only at $O(k^2)$ or beyond, which the model's own measured Kadanoff RG spectrum
($\lambda_n=b^{-n}$, imported from F130, not re-derived in this chapter) classifies as irrelevant.

$$\boxed{\;d=3n,\ n\ge2:\ \text{the extra }3(n-1)\text{ directions freeze at leading order, RG-irrelevant beyond it}\;}\tag{R2.5}$$

F292 §6 is explicit that this does *not* license reading the frozen copies as generations — that
resemblance is named and explicitly declined, not promoted, since nothing here gives the frozen
directions any dynamics to carry a label with, and $N_c=3$ is untouched by anything in this
section (deferred to Ch.13).

### 2.3.5 Why exactly one time dimension: the "+1", computed rather than asserted

Chapter 1 records (P4/P5 forward pointers) that the update generates a $\mathbb Z$-action, and an
earlier reading (F291 §6) argued informally that any second commuting flow "would, under
homogeneity, be a further generator of the Cayley graph — that is, another space direction" — a
claim later found to presuppose the very space/time split at issue (F313 §1). F313 replaces the
argument with a computation: take the update's own commutant inside the local, homogeneous
unitaries, and see what it contains.

**The setting is P2 made algebraic.** Local homogeneous $2\times2$ operators on the BCC lattice are
matrices over the Laurent ring $R=\mathbb C[w_1^{\pm1},w_2^{\pm1},w_3^{\pm1}]$,
$w_j=e^{ik_j/\sqrt3}$ — "local" *is* "finite Laurent support," which is exactly P2's finite
neighbourhood, made into algebra. This identification is itself an input, not a consequence
(F313's own 2026-08-13 self-correction): three things are fed in, not one — $s=2$; **infinite
volume** (on a finite periodic lattice $R$ collapses to a non-domain and the whole argument fails);
and the three Cayley generators of the automaton's own BCC group $\Lambda$.

Solving $[B,A]=0$ for general $2\times2$ $B$ over $R$ gives a commutant that is exactly
2-dimensional, $\operatorname{span}\{\mathbb I,\boldsymbol\sigma\cdot\tilde{\mathbf n}\}$, and free
of rank 2 (F313 §§3–4, checks C1–C2). The determinant then splits it cleanly:

$$\boxed{\;\{B\in\mathcal C:\det B\text{ alone matters}\}=U(1)\times\mathbb Z^3\ \text{(exactly the shifts, nothing more)}\;}\tag{R2.6a}$$

$$\boxed{\;\ker(\det)=\{\zeta A^n : n\in\mathbb Z\}\ \text{(exactly the powers of the update)}\;}\tag{R2.6b}$$

$$\boxed{\;d_\text{time}=1,\ \text{at }s=2\text{ on an infinite lattice}\;}\tag{R2.6}$$

(F313 §§5–6, checks C3–C4; test `F313-time-signature`, 13/13 PASS after remediation, gate tier,
three declared controls verified RED.) The non-scalar half is a Pell equation
$a^2-b^2N=1$, $N=1-u^2$, over $R[\sqrt N]$; $N$ is squarefree (a genuine field extension, not a
split into "two universes"), and the update $A=(u,-i)$ is its **fundamental solution** with
$\deg b=0$ — the shortest possible nonzero time step. The one theorem this needed from outside the
tree (a polynomial-ring Pell-descent theorem, originally mis-cited to Abel 1826 and then corrected
to Pastor 2001/Dubickas–Steuding 2004) does not transfer to a Laurent ring for free — a degree-zero
Laurent polynomial need not be a unit — so F313's chain carried one open import. **F316 closes it
in-repo**: a two-sided width function $D(f)=h_f(\lambda)+h_f(-\lambda)$ against a
$\mathbb Q$-independent direction $\lambda$ correctly detects units where the ordinary degree fails
($D(f)=0\iff f$ a monomial), and unitarity ($a^*=a,\ b^*=-b$) makes the relevant Newton polytopes
centrally symmetric, which is the extra ingredient the polynomial proof neither needs nor has. The
descent then goes through exactly, landing on $\{\pm A^{\pm1}\}$ (F316 §3; test `F316-laurent-pell`,
10/10 PASS, gate tier, `machine`, since the separation step is evaluated at an irrational $\lambda$
in float).

$$\boxed{\;\text{the polynomial}\to\text{Laurent transfer holds; F313's chain now imports nothing}\;}\tag{R2.7}$$

**Does this survive interaction?** F313 §9 measured a residual: the model's own $s=4$ massive
Dirac composite carries a *second* dispersive commuting flow, $V=\mathbb I_\text{branch}\otimes A$,
at every mass tested. F313 called this a reading — "$V$ is the $s=2$ update lifted branch-blind" —
not yet a result, and named the strong form of the test as the one that decides: does a *deformed*
charge $Q=Q_1+GQ_2+\ldots$ survive, since an interacting integrable theory could carry one even if
the free-theory symmetry itself breaks. F315 runs exactly that test, in a homogeneous,
antisymmetrised two-particle sector at fixed total momentum, against both a contact (Hubbard/NJL)
kernel and photon exchange: $V$ is broken **maximally** ($\max\lvert\Delta\phi_V\rvert\simeq\pi$),
and the $O(G)$ deformation is **obstructed** — 1,340 resonant matrix elements, where the standard
deformation formula's denominator vanishes, carry a nonzero numerator that no choice of $Q_2$ can
cancel. Controls confirm the test can report survival (a deliberately integrable interaction
leaves $V$ exactly conserved) and is not simply flagging every charge (the evolution's own charge
stays conserved on the same resonant set to $1.8\times10^{-15}$).

$$\boxed{\;V\text{ is an artifact of freeness; }d_\text{time}=1\text{ is the count of the interacting theory at any cell tested}\;}\tag{R2.8}$$

(F315 §§4–5, checks I1–I7; test `F315-V-interaction`, 11/11 PASS, gate tier, `machine`, three
controls verified RED.) This is a leading-order, not all-orders, statement, and the F86 colour
dielectric specifically is not among the interactions tested (§2.7 below).

**Was $A$ ever really the only candidate to begin with?** F313–F316 all compute what commutes with
a *given* $A$; none asks where $A$, as the sole object to take a commutant of, comes from. F326
closes this from two directions that were already in the tree, neither previously read together:
BDPT's own uniqueness theorem denies a second, independently constructible walk at $(s,d)=(2,3)$
(there is exactly one, up to conjugation and the chirality sign); and F313's own closed commutant
(§§3–4, undisturbed by its remediation) denies a second commuting generator any room — the
2-dimensional commutant is already exhausted by the shift lattice and the powers of $A$. Two
grounding checks tie this to the running engine rather than leaving it purely algebraic: the
engine's `Clock`/`Channel` machinery persists exactly one time-state field, with any channel's
finer sub-stepping a deterministic, engine-fixed multiple of it; and the model's own coupled
$s=4$ Dirac composite evolves, to machine precision, as powers of a single matrix, with no
per-branch time parameter in the production stepper's signature.

$$\boxed{\;\text{no second candidate generator exists, from either direction}\;}\tag{R2.9}$$

(F326 §§2–4, checks G1–G2; test `F326-time-single-generator`, 2/2 PASS, gate tier, `machine`, two
controls verified RED.) What this does **not** do is derive that the dynamics must be "one map,
iterated" from anything more primitive — that is the QCA-defining posit itself, on the same
footing as P2/P3's other un-derived axioms (§2.6 below), and F326 says so explicitly rather than
implying a deeper derivation exists.

### 2.3.6 The resulting lattice: BCC, and its constant is $a=2/\sqrt3$

The Weyl walk's hop phase, already shipped in the engine as
$e^{i\mathbf k\cdot\mathbf d/\sqrt3}$, $\mathbf d\in\{\pm1\}^3$, is a translation by the real-space
vector $\boldsymbol\delta=\mathbf d/\sqrt3$. Matching this to the BCC nearest-neighbour vector
$\tfrac a2(\pm1,\pm1,\pm1)$ of a lattice with conventional cube edge $a$:

$$\boxed{\;a=\frac2{\sqrt3}=2c_\text{lat}\;}\tag{R2.10}$$

with $\lvert\boldsymbol\delta\rvert=\tfrac{\sqrt3}2a=1$ exactly. This is not a new number: $a/2$
and the registered constant `c_lat` are the *same IEEE-754 double* (bit pattern
`0x3fe279a74590331d`), so $a$ requires no separate registration and must never be written as an
independent decimal literal (F278 §2, `exact`, checks 1–4). Two previously *measured* quantities
promote to closed form as a direct consequence: F267's cube/true-zone volume ratio,
$4/(3\sqrt3)=a^3/2$ (the BCC primitive cell volume, as a pure number, because the sampling lattice
has unit cell volume), and F273's measured "$\sqrt3\cdot$fcc" period lattice, which is exactly the
reciprocal of this same BCC crystal, $4\pi/a=2\pi\sqrt3$ (F278 §§4–5, checks 5–7, `exact`).

$$\boxed{\;V_\text{cube}/V_\text{BZ}=a^3/2=4\sqrt3/9\approx0.7698,\qquad 4\pi/a=2\pi\sqrt3\;}\tag{R2.11}$$

One further, sharper fact locates a mode exactly rather than approximately: the zone corner H sits
at $\lvert\mathbf k\rvert=2\pi/a=\pi\sqrt3$, and both dispersion branches evaluate to exactly $\pi$
there (F278 §6, checks 8–9, `exact`, floating-point literal $0.0$). This qualifies, without
overturning, the "no fermion doublers" claim (CL020, `narrowed`): true on the cubic FFT cube every
computation in the tree actually runs on (one zero, no $\pi$-point, $L$ up to 128), but the true
BCC crystal carries a $\pi$-mode exactly at H, and whether that constitutes a doubler is not
decided by this chapter (§2.7 below).

### 2.3.7 The point group: geometry says $O_h$, the dynamics says $D_{2h}$/$D_{4h}$

Postulate P3 requires only that the neighbour set admit the action of *some* finite point group.
The BCC neighbour shell (the 8 body-diagonal hops) genuinely is a single $O_h$ orbit — 48 elements
— and that geometric fact is what later shell-irrep arguments (Ch.15's $E_g$-weight construction,
among others) are entitled to use. But the specific unitary walk BDPT force onto that shell is a
*different* object, and its exact covariance group is strictly smaller.

Unitarity alone pins every one of the walk's eight Bloch-monomial coefficients to modulus 1 (the
squared monomials form an exact rank-8 basis over $\mathbb Q$, so $\sum\lambda_m(\cdot)^2=1$ forces
every $\lambda_m=1$), leaving a single cross-term condition. Sweeping all $4^6=4096$ sign
assignments exhaustively, 576 are unitary — this is the complete search, not a guessed family.
Testing covariance $A(g\mathbf k)=U A(\mathbf k)U^\dagger$ ($U$ unitary, $k$-independent) against
every $g\in O_h$, correctly accounting for the fact that 24 of the 48 elements swap the walk's
chirality branch (an effect the naive test missed and mistook for a leading-order failure):

$$\boxed{\;L_\text{unitary}\cong D_{2h},\ \text{order }8;\qquad L_\text{incl.\ step-reversal}\cong D_{4h},\ \text{order }16\;}\tag{R2.12}$$

*of 48, and neither is $O_h$, in any of the 576 unitary conventions* (F344 §4, checks C3–C5). The
obstruction is exact and structural: $C_3$ covariance of the walk's $O(k^2)$ ("$T_{2g}$") sector
would require its three coefficients to agree, while unitarity's cross-term condition forces them
to differ in sign — mutually exclusive, in every convention (F344 §4, "the obstruction, in one
line"). **The defect is closed-form and vanishes at leading order**: the $O(k)$ (leading, "$T_{1u}$")
truncation *is* exactly $O_h$-covariant for all 48 elements, and the $C_3$-violating residual is
$O(k^2)$ absolute, measured to shrink linearly in $\lvert k\rvert$ across four decades (F344 §4,
check C8).

$$\boxed{\;O_h\text{ is an exact }\textit{infrared}\text{ symmetry of the walk, not a lattice-scale one}\;}\tag{R2.13}$$

(F344 §§3–4, checks C1–C8; test `F344-bcc-walk-point-symmetry`, 11/11 PASS, gate tier, `exact`.)
This is the sharpened form of the premise F291 itself flagged as its own weakest link ("the
lattice's isotropy group … is a premise, not something proved here"): it is not simply true or
false, but scale-dependent, and now exactly characterised rather than assumed. Later chapters that
need full $O_h$ *at the lattice scale* (Ch.15's shell-irrep machinery, in particular) rest on the
geometric shell, not on this dynamical covariance group, and the two footings must not be
interchanged (F344 §6).

### 2.3.8 The cell has room for an internal index, at zero cost, in one shape, but nothing forces it

A separate question — whether the minimal cell can carry the internal (colour) index later
chapters need — turns out to have three different answers depending on exactly what is asked
(F318). **Permission:** enlarging the cell by an internal tensor factor $\otimes\mathbb 1_N$ costs
nothing on either the space or the time side. On the space side, what R2.1's selector actually
needs is not the cell's total Clifford rank but the maximal *anticommuting* rank of the **hop's**
own traceless-Hermitian span — and that stays exactly 3 whether the cell is the bare $s=2$ Weyl
branch, the branch-doubled $s=4$ Dirac cell (span widens $3\to6$ but the extra generators
*commute* rather than anticommute with the original three), or the model's actual $s=12$ or
$s=36$ coloured quark cell (an internal tensor factor changes neither the span's dimension nor any
commutator). On the time side, an internal factor multiplies the commutant's dimension by exactly
$N^2$ ($2\to18$ at $N=3$), but every added element is **non-dispersive** — its eigenphase is
exactly constant in $\mathbf k$ (measured at literal $0.0$, against the update's own $0.2846$) — so
it is a global internal symmetry, not a second clock; this supplies F313's count the one criterion
it never had to state before an internal factor existed.

$$\boxed{\;\text{an internal }\otimes\mathbb 1_N\text{ factor costs zero spatial and zero temporal directions}\;}\tag{R2.14}$$

**Shape:** this is not vacuous, because a genuinely *different* enlargement — one that adds a new
generator anticommuting with the hop, e.g. moving to a five-generator Clifford construction on
$\mathbb C^4$ — does cost something: the selector's answer moves from 3 to 5, exactly as R2.1's
counting predicts (F318 §B4, the converse check). So R2.1's conditionality on $s=2$, which F291
itself flagged as its weakest link, sharpens rather than vanishes: it is conditional on the *hop's*
anticommuting rank being 3, which the model's actual coloured cell satisfies, but a differently
*shaped* enlargement would not.

**Existence is not forced by any of this.** Space and time verdicts are identical at $N=1$ and
$N=3$; the cell is measurably indifferent to whether the internal index exists at all. What forces
it to exist is Fermi statistics (derived in-tree, F289, not imported) applied to a nodeless
(hence totally symmetric) spatial ground state: explicit antisymmetrisation shows a three-particle
bound state cannot exist at all at $N=1$, but can at $N\ge2$ — and the tree does contain
three-constituent bound states (built dynamically, as an operator, and in real space — forward
reference to Ch.13/14's baryon constructions). So the index's *existence* is forced by a smaller,
concrete, still-external input — "the matter sector contains a three-constituent bound state" —
not by lattice geometry.

$$\boxed{\;\text{the index's shape is forced; its existence is forced by derived statistics + an external three-constituent fact, not by the cell}\;}\tag{R2.15}$$

(F318 §§A–D, checks A1–A2, B1–B4, C1–C2, D1–D3; test `F318-cell-internal-index`, 11/11 PASS, gate
tier, `exact`, four declared controls verified red only where declared.) What that index *becomes*
— why specifically $N=3$, confinement, $\alpha_s$ — is Chapter 13's content, not this chapter's;
this section establishes only that the lattice has the room, at the price stated, and no more.

### 2.3.9 The array is not the crystal's true Brillouin zone

A correction that later chapters must inherit rather than rediscover. The cubic FFT grid every
engine module actually computes on is periodic under $2\pi$ per axis; the walk's own dispersion
(and, F273 shows, essentially *every* dispersion in the tree, gauge sector included) is periodic
under the coarser lattice $\sqrt3\times$fcc — F278 identifies this exactly as the reciprocal
lattice of the BCC crystal of §2.3.6 (R2.11 above). Consequently the cubic FFT cube is not a
fundamental domain of the walk at all, and where it *is* used as a stand-in for a continuum
Brillouin-zone integral, the cube's grid-mean differs from the true zone average by
$10.7\%$–$16.9\%$ on the observables measured (F267 §S4, `quantitative`, Monte Carlo with
declared seeds).

$$\boxed{\;\text{the cube covers only }a^3/2=4\sqrt3/9\approx77\%\text{ of the true BCC zone, and is not its fundamental domain}\;}\tag{R2.16}$$

**The distinction that matters, and it is not a blanket correction.** For an observable that is
genuinely a trace over the finite lattice's *own* modes — a vacuum-fluctuation sum, a density of
states on the array as actually implemented — the cube is exactly correct, because it *is* the
complete, non-redundant mode set of the $L^3$ system; nothing is over- or under-counted. The error
appears only when a cube grid-mean stands in for a continuum BZ integral of the underlying
dispersion, or is compared against a differently-discretised calculation. F273 traces this exactly
through the model's own $I_2=\langle\cot\omega\rangle$ moment (feeding $B$, hence
$\lambda_6=0.243$, in the lepton sextic chain, CDD7): the cube is the *correct* mode set for that
sum (a leading-order Taylor coefficient of the finite-lattice sea energy), so the **number** stands,
but the **label** — "Brillouin-zone average" — is wrong, since the true zone average of the same
quantity is exactly zero by symmetry.

$$\boxed{\;\text{no factor should be inserted anywhere; each }k\text{-space average must be classified, per observable, as a mode sum (cube correct) or a BZ-integral stand-in (cube biased)}\;}\tag{R2.17}$$

(F267 §§S1–S5, F273 §§1–3, `exact`/`machine`/`quantitative` as tabulated below; test records
`F267-walk-bz-measure`, `F272-F273-bz-period-lattices`.) F273 explicitly declines to resolve, and
this chapter does not resolve either, a genuine open tension named in §2.7 below: whether the
array *is* the physical lattice (and the word "Brillouin zone" is a misnomer to retire) or the BCC
crystal is physical and the array an unfaithful discretisation of it (in which case the classified
mode sums, $I_2$ included, are sampling a biased sub-region). This is deliberately not decided
here — see §2.7.

## 2.4 Results table

| # | Statement | Exactness | Residual / tolerance | Source |
|---|---|---|---|---|
| R2.1 | $d\le3$ (Bloch-Jacobian kernel argument) | exact | closed form, $d\in\{1,2,3\}$ verified | F291 §3, check B1; test `F291-dimension-selectors` (9/9, gate) |
| R2.2 | $d\ge3$ (cokernel + chiral-mass-phase argument, P6) | exact | closed form; checked at $d=2,3$ | F291 §4, checks B2–B3; same test record |
| R2.3 | $d=3$, from two logically independent routes (S1$\wedge$S2, and S3) | exact | $\det J=\mp c_\text{lat}^3$ exact; $\dim\Lambda^2\mathbb R^d=d\iff d\in\{0,3\}$ exact over $\mathbb Z$ | F291 §§2,5, checks C1, D1–D2 |
| R2.4 | $d=6,9$ excluded (bivector overcount $\ne1$; $d=6$ additionally has no chirality projector) | exact | closed-form identity; Clifford recursion built and checked twice | F292 §§2–3, checks A1, B1–B3; test `F292-higher-multiples` (8/8, gate) |
| R2.5 | Reducible $d=3n$: extra $3(n-1)$ directions freeze at leading order, RG-irrelevant beyond it | exact (freezing) / quantitative (irrelevance, imports F130) | $\dim\ker J=3(n-1)$ exact; irrelevance is F130's measured Kadanoff spectrum, not re-derived here | F292 §4, check C1 |
| R2.6 | $d_\text{time}=1$: commutant splits exactly into shifts $U(1)\times\mathbb Z^3$ and powers of $A$ | quantitative (per CL269's post-review grade; the algebra is closed-form but rests on the three declared inputs) | rank-2 commutant; degree-0 fundamental Pell solution | F313 §§3–6, checks C1–C4; test `F313-time-signature` (13/13, gate, 3 controls RED) |
| R2.7 | The polynomial$\to$Laurent transfer F313 needed is proved in-repo; no import remains | machine | separation measured against an irrational $\lambda$, exact algebraic identities elsewhere | F316 §§2–3; test `F316-laurent-pell` (10/10, gate, 3 controls RED) |
| R2.8 | The $s=4$ composite's second dispersive flow $V$ does not survive interaction (leading order); $d_\text{time}=1$ holds interacting | machine | $\max\lvert\Delta\phi_V\rvert\simeq\pi$; obstruction measured on 1,340/1,930 resonant elements | F315 §4, checks I1–I7; test `F315-V-interaction` (11/11, gate, 3 controls RED) |
| R2.9 | No second candidate time generator exists (BDPT uniqueness + closed commutant, both directions) | machine (citation-based synthesis + two grounding checks; the uniqueness citation itself is not independently re-verified in-repo) | G1/G2 exact-integer and $\sim10^{-16}$ checks; scope of what they prove narrowed in F326's own review | F326 §§2–4; test `F326-time-single-generator` (2/2, gate, 2 controls RED) |
| R2.10 | BCC lattice constant $a=2/\sqrt3=2c_\text{lat}$ (dimensionless, lattice-native units) | exact | $a/2$ and `c_lat` are the identical IEEE-754 double | F278 §2, checks 1–3 |
| R2.11 | $V_\text{cube}/V_\text{BZ}=a^3/2=4\sqrt3/9$; period lattice $4\pi/a=2\pi\sqrt3$; $\omega=\pi$ exactly at zone corner H | exact | sympy residual $\equiv0$; floating-point literal $0.0$ at H | F278 §§4–6, checks 4–9 |
| R2.12 | Exact walk covariance group: $D_{2h}$ (order 8, unitary) / $D_{4h}$ (order 16, with step reversal); never $O_h$ | exact | exhaustive search over 576 unitary sign conventions | F344 §4, checks C3–C5; test `F344-bcc-walk-point-symmetry` (11/11, gate) |
| R2.13 | $O_h$ is an exact infrared (leading-order) symmetry of the walk; the $C_3$-breaking residual is $O(k^2)$, vanishing linearly in $\lvert k\rvert$ | exact (leading order) / machine (residual scaling, 4 decades) | check C7 (all 48, $O(k)$ exact); check C8 (decade ratios $\to10$) | F344 §4, checks C6–C8 |
| R2.14 | An internal $\otimes\mathbb 1_N$ factor costs zero spatial and zero temporal directions | exact | anticommuting rank 3 at $N=1,3$; internal commutant elements non-dispersive at literal 0.0 | F318 §§B–C; test `F318-cell-internal-index` (11/11, gate, 4 controls) |
| R2.15 | The index's shape is forced (an anticommutation-adding enlargement moves the selector to 5); its existence is forced by derived Fermi statistics + a three-constituent bound state, not by the cell | exact | explicit antisymmetriser rank at $N=1,2,3$ | F318 §§B4, D; same test record |
| R2.16 | The cubic FFT cube covers $\approx77\%$ of the true BCC zone and is not the walk's fundamental domain | exact (ratio) / quantitative (10.7–16.9% BZ-integral error, Monte Carlo) | $a^3/2=4/(3\sqrt3)$ exact; MC error with declared seeds | F267 §§S1–S4; F278 §4; tests `F267-walk-bz-measure`, `F272-F273-bz-period-lattices` |
| R2.17 | Mode sums on the cube are correct as computed; "Brillouin-zone average" is a mislabelling where the cube substitutes for a continuum integral | exact (the classification argument) | $I_2$ traced as a leading Taylor coefficient of the finite-lattice sea energy | F273 §§1–3 |

## 2.5 Comparison with measurement

This chapter is almost entirely structural/internal-consistency work — none of R2.1–R2.17 is
itself checked against an experimental number, and none should be read as if it were. Two links to
eventual observation are worth stating rather than leaving silent:

- **$d$ is, in principle, measurable through $c_\text{lat}$.** $c_\text{lat}=1/\sqrt d$ (BDPT Eq.
  21), and $\lvert\det J\rvert=c_\text{lat}^3$ ties the same number to the handedness structure of
  §2.3.2's corollary. A measured $c_\text{lat}\ne1/\sqrt3$ at the lattice scale would falsify
  $d=3$ directly — but this is the same observable Chapter 6/7's light-cone and LIV-bound machinery
  already carries; nothing new is measured in this chapter.
- **The lattice constant's absolute (SI) value is not compared against anything here.** R2.10 fixes
  only the dimensionless ratio $a=2/\sqrt3$ in lattice-native units. Whether that cell is small
  enough to have escaped every existing bound (GRB time-of-flight, LHAASO, etc.) is the canonical
  SI-ruler decision of Chapter 17 (F79/F107), not this chapter's claim.

Everything else in this chapter — the point-group covariance class, the internal-index cost
structure, the FFT-cube/true-zone distinction — is a statement about the model's own internal
geometry, checked against itself (independent re-derivations, exhaustive sign-convention sweeps,
declared negative controls), not against data.

## 2.6 What was excluded, and why

- **$d=1,2$.** $d=1$ fails the bivector/vector match (R2.3) and has no transverse direction for a
  photon at all (CDD5). $d=2$ fails **twice**, by two mechanisms neither built to test it: the
  cokernel/mass argument (§2.3.2 — a real, ungauged parity-odd mass survives, so P6 has nothing to
  gauge) and the chirality-parity argument (§2.3.4 — $D=3$ is odd, no projector).
- **$d\ge4$, and specifically $d=6,9$, and reducible $d=3n$.** Excluded by R2.1/R2.4/R2.5
  respectively, by mechanisms that disagree about exactly *which* dimensions they kill — evidence,
  per F292 §3, that the selectors are independent constraints and not one argument dressed three
  ways.
- **Simple cubic, as the canonical lattice.** Not excluded by any argument in this chapter's
  findings; excluded by the model's own D1 engineering decision, which is explicit about the
  distinction this chapter must preserve: simple-cubic code is **retained**, banner-labelled a
  "reference implementation, continuum-limit regression target, not canonical" — it is not claimed
  wrong, and it is not the object §2.3.6–§2.3.9 derive facts about. BDPT's own uniqueness theorem
  (imported, §2.1 item 2) is what actually selects BCC over other isotropic $d=3$ lattices at
  $s=2$; this chapter derives the *constant* of that already-selected lattice, not the selection
  itself.
- **A second, independently posited time generator** (e.g. a Bars-style two-time construction).
  Closed by R2.9 from both directions — no second BDPT solution exists to start from, and no room
  exists in the closed commutant for one built to commute with $A$. Cited only as informed
  contrast (I. Bars, *Class. Quantum Grav.* **18** (2001) 3113, external, not tested on this
  lattice): where a genuine two-time theory has been built and made consistent, the extra direction
  survives only as gauge redundancy, collapsing back to ordinary one-time dynamics — evidence that
  single-generator dynamics is the economical, non-pathological choice, not a proof that no
  alternative construction could ever work here.
- **Full $O_h$ covariance of the propagating dynamics, at the lattice scale.** Not excluded as
  wrong — recovered exactly as the infrared limit (R2.13) — but excluded as an *exact lattice-scale*
  statement (R2.12): unitarity and $C_3$ covariance of the walk's $O(k^2)$ sector are provably
  incompatible, in every one of 576 admissible sign conventions.
- **A naive factor-4 (gauge-sector) or "$\sqrt3$" correction transplanted onto fermion-sector mode
  sums.** F278 §7 shows both sectors' measure factors are the *same* relation, $a^3/2$, evaluated
  at each sector's own lattice constant ($a=2$ for the integer-hop gauge links, $a=2/\sqrt3$ for
  the fermion walk); transplanting the gauge side's factor of 4 onto the fermion side would
  over-correct by $(\sqrt3)^3\approx5.196$.

## 2.7 What is still open

Named because the source findings themselves name it, not papered over:

1. **The $s=2$ minimality premise is adopted, not derived, anywhere in this chapter or the wider
   tree checked here.** Every dimension-count result (R2.1–R2.9) is conditional on it; F291's own
   stated boundary is that losing S3 *and* $s=2$ together would reopen the whole question.
2. **BDPT's uniqueness theorem for the specific BCC solution at $(s,d)=(2,3)$ is imported, not
   re-derived**, in the findings assigned to this chapter (§2.1 item 2).
3. **The Reading 1 / Reading 2 tension of F273/F278 is genuinely unresolved and load-bearing.**
   Either the cubic array is the physical lattice (in which case "Brillouin zone" language for the
   $\sqrt3\cdot$fcc period should be retired), or the BCC crystal is physical and the array an
   unfaithful discretisation of it (in which case every mode sum classified as "correct as
   computed" in R2.17, $I_2$/$\lambda_6=0.243$ included, is sampling a biased sub-region whose
   unbiased value is exactly zero). F273 explicitly declines to choose, calling it "more
   fundamental than the four remaining cubic layers" still to be audited; this chapter inherits
   that non-resolution rather than picking a side.
4. **Whether the $\omega=\pi$ mode at the true zone corner H (R2.11) constitutes a fermion doubler**
   is located exactly but not decided (F278 §6); CL020 records the qualified, not the retracted,
   form of the no-doublers claim.
5. **R2.8/F315's obstruction is leading order.** It is the standard, decisive form of a
   no-extra-conserved-charge argument, not an all-orders proof, and the F86 colour dielectric —
   the confining, non-Abelian sector — is explicitly named by F313's own falsifier 5 and is
   explicitly *not* among the interactions F315 tested.
6. **F344's residual $D_{2h}/D_{4h}$ covariance defect has no checked observable consequence.**
   It is invisible to every dispersion test and to the paired-photon pair rate (both depend only
   on $u$, not the full spin texture), but F344 names five live consumers of the full walk
   (`chiral_core`, `dirac_bcc`, `blockspin`, `thermodynamics`, `induced_stiffness`) that have not
   been checked against it.
7. **F318's forcing argument consumes, rather than derives, "the matter sector contains a
   three-constituent bound state."** That fact is in-tree (built dynamically, as an operator, and
   in real space — Ch.13/14), not a tabulated hadron mass, but it remains an external input to
   this chapter's own argument, and F318 is explicit that this does not independently corroborate
   F317's separate empirical route to the same conclusion — the two consume the same underlying
   fact.
8. **Why the model's cell is a tensor product at all** (rather than colour being entangled with the
   walk's own index in some other way) is untouched by anything in this chapter (F318 falsifier 4).

## 2.8 Falsifiers

From the findings' own stated falsifiers and the claim cards resting on them (CL246, CL247, CL269,
CL270, CL272, CL020 — all reported here with their actual `status`/`review_state`, since CL246 and
CL247 are `provenance: extracted`, `review_state: unreviewed-seed`, i.e. seeded mechanically from
their findings' prose and not yet independently promoted, even though the underlying findings'
own gate-tier tests pass; the physics content below is the findings', not weakened by the claim
layer's administrative lag):

1. Exhibit an $s=2$ isotropic unitary walk in $d\ge4$ with $\ker J=0$, or an isotropy-invariant
   intra-branch mass term at $d=3$ — either kills R2.1 or R2.2 (F291 falsifiers 1–2).
2. Formulate the model's Maxwell sector with $\mathbf B$ as a bivector and recover the existing
   exact rotation law and $c_\text{lat}=d\Omega/d\lvert\mathbf k\rvert$ — kills R2.3's S3 route
   (F291 falsifier 3).
3. Exhibit a chirality projector in odd spacetime dimension $D\le8$, or an isotropic $s=2$ walk on
   $\mathbb R^{3n}$, $n\ge2$, with anticommuting rank $>3$ — reopens $d=6$ or the reducible case
   respectively (F292 falsifiers 1–2).
4. Exhibit a local homogeneous unitary commuting with $A$ that is not a shift or a power of $A$, a
   Pell solution not of the form $\zeta A^n$, or $N=1-u^2$ shown to be a square in $R$ — any one
   kills R2.6/R2.9 (F313 falsifiers 1–3; F326 falsifier 2).
5. Show the model's interactions (specifically the F86 colour dielectric, or an all-orders
   treatment of any tested interaction) conserve $V=\mathbb I\otimes A$ — reopens R2.8 (F313
   falsifier 5, F315 falsifier 4).
6. Break the infinite-volume premise: exhibit the finite $L$, if any, at which a rank-$>1$
   commutant appears (F313 falsifier 8) — a direct test of the free input flagged in §2.1 item 3.
7. Exhibit a unitary BCC $s=2$ Weyl automaton, of any form, that is exactly $C_3$-covariant —
   kills R2.12/R2.13 (F344 falsifier 1); or show the residual $D_{2h}/D_{4h}$ defect has an
   observable consequence in one of the five named live consumers — would promote §2.7 item 6 from
   open to closed, in either direction (F344 falsifier 2).
8. Exhibit a model enlargement that adds an anticommuting generator to the hop (reopens R2.14 at a
   different selector value) or a stable bound state with a constituent count other than three, or
   with a non-nodeless ground state (undermines R2.15's forcing argument) (F318 falsifiers 2–3).
9. CL020's stated falsifier: build the discriminating observable that distinguishes the cubic FFT
   grid from the true BCC zone, to decide whether the corner-H $\pi$-mode is a genuine doubler —
   not yet built.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Ch.1's table; all quantities in
lattice-native units unless noted.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $s$ | The per-cell internal (spinor) dimension; $s=2$ is BDPT's minimal Weyl cell (P5), imported not derived. | §2.1, §2.2 |
| $d$ | The number of spatial dimensions; this chapter's central result is $d=3$ (R2.3). | §2.2 |
| $D$ | The spacetime dimension, $D=d+1$; used in the chirality-parity argument (R2.4). | §2.3.4 |
| $A(\mathbf k)$ | The Bloch-space (momentum-representation) form of the per-tick update $\mathcal U$ (Ch.1 P4), restricted to the free single-particle sector: $A=u\mathbb I-i\boldsymbol\sigma\cdot\tilde{\mathbf n}$. | §2.2 |
| $u(\mathbf k)$, $\tilde{\mathbf n}(\mathbf k)$ | The scalar and Bloch-vector parts of $A(\mathbf k)$'s Pauli decomposition. | §2.2 |
| $J$ | The Jacobian of $\tilde{\mathbf n}$ at $\mathbf k=0$, $J:\mathbb R^d\to\mathbb R^3$; the object every dimension selector in this chapter is a statement about. | §2.2 |
| $\Lambda$ | The automaton's own BCC Cayley group (index 4 in $\mathbb Z^3$); realizes Ch.1's abstract $G$. | §2.3.5 |
| $R$ | The Laurent ring $\mathbb C[w_1^{\pm1},w_2^{\pm1},w_3^{\pm1}]$ over which local homogeneous operators are represented; "local" $\equiv$ "finite Laurent support" (P2, made algebraic). | §2.3.5 |
| $\mathcal C$ | The commutant of $A$ inside the local homogeneous unitaries; $\dim_R\mathcal C=2$. | §2.3.5 |
| $a$ | The BCC lattice's conventional cube edge, now fixed at $a=2/\sqrt3=2c_\text{lat}$ (dimensionless, lattice-native; SI value deferred to Ch.17). Extends Ch.1's reserved symbol with a concrete value. | §2.3.6 |
| $O_h$, $D_{2h}$, $D_{4h}$ | The full octahedral point group (order 48; the exact symmetry of the BCC neighbour shell) and its two subgroups (orders 8, 16) that the propagating dynamics actually realizes exactly. Realizes Ch.1's reserved symbol $L$. | §2.3.7 |
| $N$ | The internal (colour) tensor-factor multiplicity; the cell's cost in space/time directions is independent of $N$ (R2.14), but its forced existence and value are Ch.13's content. | §2.3.8 |

---

*New Gap logged this chapter: **G-2** (§2.1), also recorded in `docs/monograph/GAPS.md`. No
finding, claim card, module, or test record was created or modified in the writing of this
chapter.*
