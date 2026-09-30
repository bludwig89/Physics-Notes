# Chapter 6 — Free Propagation and the Light Cone

*Chapter 6 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F26-speed-of-light-as-rotation-rate.md`, `findings/F26b-bcc-spin-axis-scalar-contamination.md`,
`findings/F46-pythagorean-lattice-mass.md`, `findings/F171-slowlight-rotation-vs-phase.md`,
`findings/F245-curl-subleading-closed-forms.md`, `findings/F246-f26-even-dispersion-subleading.md`,
`findings/F300-lattice-native-thermodynamics.md`, and `findings/F20-photon-fermion-propagation-demo.md`
(the eight findings `00-plan.md` §2 assigns to this chapter), read against
`docs/theory/supersessions.yaml` (none of the eight appears as a `superseded:` entry in any of the
23 records; F20 alone appears, as a `partial` item of S18, discussed in full in §6.6 below rather
than smoothed over), `claims-index.md` (CL001, CL030, CL151, CL260, CL261, CL265 — statuses reported
verbatim below), and `docs/status/exactness-inventory.md` (rows #3, #49, #181, #298, cross-checked
against $c_\text{lat}=1/\sqrt3$ and against the F306/S18 reclassification of the composite-photon
curl residual). Notation, postulates and results are those of Chapters 1–3
(`01-postulates-and-ontology.md`, `02-dimensions-and-lattice-selection.md`,
`03-the-update-rule.md`) — $\mathbf k$, $\omega(\mathbf k)$, $c_\text{lat}$, $A(\mathbf k)=u\mathbb
I-i\boldsymbol\sigma\cdot\tilde{\mathbf n}$, $\theta(\mathbf k)=\arccos u$ — extended, never
redefined. `references/mohr-2010-maxwell-photon-wf-summary.md` (the Riemann–Silberstein-style
six-component Maxwell/Dirac analogy) is cited in §6.2 as external corroboration that combining
$(\mathbf E,\mathbf B)$ into one rotating object is a legitimate, independently-known construction,
not an idiosyncrasy of this model.

## 6.0 What this chapter establishes

Chapter 1 reserved two symbols without content — $\mathbf k$/$\omega(\mathbf k)$ ("left undefined
in detail until Chapter 6") and $c_\text{lat}$ ("defined and derived in Chapter 6 as a rotation
rate, not a phase velocity") — and Chapter 3 wrote down the concrete free-walk stepper
$A(\mathbf k)=e^{-iH(\mathbf k)}$, $H(\mathbf k)=\theta(\mathbf k)\hat{\mathbf n}(\mathbf
k)\cdot\boldsymbol\sigma$, whose rotation angle $\theta(\mathbf k)$ it explicitly deferred reading
as $c_\text{lat}$ to this chapter (R3.4). This chapter is where that deferral is discharged. It
shows: (i) the free walk's on-axis dispersion is *exactly* linear in $\mathbf k$, at every $|\mathbf
k|$, on both helicity branches — an algebraic identity, not a small-$k$ limit; (ii) the physically
adopted speed of light is not this dispersion's phase velocity but the rate at which a real,
physically-rotating $(\mathbf E,\mathbf B)$-type bilinear pair turns per unit wavenumber, and that
rate evaluates, from the stepper of Chapter 3 alone, to the closed number $c_\text{lat}=1/\sqrt3$;
(iii) the two readings — phase velocity and rotation rate — are numerically identical at leading
order and conceptually distinct, with the distinction only visible in the subleading dispersion
structure and in what each reading says "physically moves"; (iv) the massive (Dirac) dispersion
composes with the massless one by an exact spherical-trigonometric law whose continuum limit is
Einstein's $E^2=p^2c^2+m^2c^4$; (v) the subleading corrections to both the rotation law and (in a
now-reclassified sense) an older composite-field construction are closed form, and structurally
forbid a CPT-odd ($k^2$) Lorentz-violating term while permitting a CPT-even cubic one; (vi) a slow-
light/EIT test that could in principle have discriminated the rotation-rate reading from the
textbook phase-velocity reading instead shows the two are isomorphic in the linear regime; and
(vii) the resulting dispersion relation, taken as a theorem rather than an input, forces the
continuum radiation equation of state $w=1/3$ with closed-form lattice corrections — the first
genuinely thermodynamic consequence this monograph draws, flagged here as a partial reach beyond
this chapter's own remit. Chapter 6 also closes the loop on Chapter 2's own Gap [G-2]: two premises
Chapter 2 used before this chapter existed are shown here to have been used only in the form
Chapter 2 needed them in, not in the quantitative form this chapter now supplies — see §6.1.

## 6.1 Inputs

**Postulates used.** **P1** (discreteness — the rotation angle advances once per indivisible tick;
without a discrete tick there is no "per-tick rotation" to define). **P2/P3** (locality, homogeneity,
isotropy — carried in through R3.1–R3.6, not re-invoked directly). **P4** (linearity, exact unitarity,
$\mathcal U=e^{-iH}$ — this chapter's entire construction is the spectral content of that generator,
already exhibited in Ch.3 R3.4). **P5** (the per-cell field is $\psi\in\mathbb C^2$ — the object whose
bilinears rotate). **P6** enters through F46's mass term (the same chiral-$SU(2)_L$ complex-phase
mechanism Ch.2 §2.3.2 used to force $d\ge3$) but is not otherwise invoked. **P7** is not invoked.

**Prior results used, precisely.** **R3.1** (the explicit Bloch form $A(\mathbf k)=u(\mathbf
k)\mathbb I-i\boldsymbol\sigma\cdot\tilde{\mathbf n}(\mathbf k)$, the eight-monomial BCC basis,
$u^2+\lVert\tilde{\mathbf n}\rVert^2\equiv1$) is the object every dispersion computation below
expands. **R3.4** ($A(\mathbf k)=e^{-iH(\mathbf k)}$, $\theta(\mathbf k)=\arccos u(\mathbf k)$,
explicitly deferring the rotation-rate reading of $\theta$ to this chapter) is the deferral this
chapter discharges. **R2.3/R2.10** (the derived dimension $d=3$ and the BCC lattice constant
$a=2/\sqrt3=2c_\text{lat}$ in lattice-native units, with hop length $\lvert\boldsymbol\delta\rvert=1$
exactly) fix the units in which the number $1/\sqrt3$ below is meaningful. **R2.13** (the exact
infrared recovery of full $O_h$ isotropy) is used implicitly: the leading-order dispersion below is
isotropic precisely because $O_h$ is exact at that order.

**Free inputs consumed, stated precisely.** Two, of different character, plus a closed accounting
of what is *not* free:

1. **A units convention, not a physical input.** The numeral $c_\text{lat}=1/\sqrt3$ is meaningful
   only in lattice-native units (hop length set to $1$, tick duration set to $1$, per Ch.1's
   notation table and R2.10). Changing that convention rescales the number without changing any
   physics; the *dimensionless* content — $c_\text{lat}=1/\sqrt d$ at $d=3$ — is convention-free
   (cited already at Ch.2 §2.5 as BDPT Eq. 21, re-derived directly from R3.1 in §6.2 below rather
   than re-imported).
2. **Which physical quantity the symbol "$c$" fundamentally names is an interpretive choice, not a
   computation.** The stepper's dispersion $\omega(\mathbf k)$ is the same closed-form object
   (R3.1's $\theta(\mathbf k)=\arccos u(\mathbf k)$) under either reading; §6.2 shows explicitly that
   the phase-velocity reading ($\omega/|\mathbf k|$) and the rotation-rate reading ($d\Omega/d|\mathbf
   k|$) coincide at leading order — both equal $1/\sqrt3$ — so *no numeral* is at stake in adopting
   one reading over the other. What is at stake is which object is treated as physically real: a
   complex phase advancing through space, or a real bilinear pair rotating in an internal plane
   while sitting in place. CLAUDE.md's Core Design Decision 2 adopts the second reading; this
   chapter derives its numerical content but does not — because no source does — supply an
   independent argument that the rotation reading is *true* rather than merely an equally valid
   relabelling. §6.6 and §6.7 state exactly how far this indeterminacy currently reaches (F171).
3. **Nothing else is free.** Given $d=3$ (Ch.2), the concrete stepper $A(\mathbf k)$ (Ch.3, itself
   unique up to the inert global phase and the chirality-sign labelling already flagged as free at
   Ch.3 §3.1), and the units convention above, the value $c_\text{lat}=1/\sqrt3$ follows from a
   single closed-form limit with no further numerical freedom — this chapter introduces no new
   fitted or chosen parameter.

> **Gap [G-2], resolution.** Chapter 2 §2.1 flagged that its own R2.1/R2.3 dimension-count
> derivation used CLAUDE.md's Core Design Decision 2 ($c_\text{lat}$ as an $(\mathbf E,\mathbf
> B)$-rotation rate) and Decision 5 (the paired-spinor photon) before either was promoted to a
> numbered postulate or derived in detail — precisely the two items this chapter now supplies in
> full. Re-reading Chapter 2's actual use of each premise against what this chapter derives shows
> the dependency is **not circular, and for a specific, checkable reason in each case**:
> - Ch.2's route (b) (§2.3.1) needed only that $c_\text{lat}$ be *definable* as a single number
>   $d\Omega/d|\mathbf k|$ at $|\mathbf k|\to0$ — i.e., that the limit not be direction-dependent.
>   That is a statement about the existence of a limit, decided by whether $\ker J=0$ (a fact about
>   the Jacobian of $\tilde{\mathbf n}$, already in hand before this chapter). It does not require
>   knowing the limit's *value*. This chapter computes the value ($1/\sqrt3$, §6.2) and confirms in
>   passing that the limit is indeed direction-independent at leading order (isotropic, matching
>   Ch.2's R2.13) — a strictly stronger, later-arriving fact than what route (b) consumed.
> - Ch.2's route S3 (§2.3.3) needed only that CDD2's $(\mathbf E,\mathbf B)$ pair be a
>   vector-plus-bivector (or, in CDD5's native language, that the paired construction's field
>   strength be an $\mathfrak{su}(2)$ triplet) — a representation-theoretic fact about *what kind of
>   object* the rotating pair is, true in any $d$ and settled by counting dimensions
>   ($\dim\Lambda^2\mathbb R^d$ vs. $\dim\mathbb R^d$, or $\dim\mathfrak{su}(2)=3$), independent of
>   the pair's dynamics or of the numeral $c_\text{lat}$ evaluates to. This chapter's own
>   construction (§6.2) is built on exactly the bilinear object S3's counting argument presupposes
>   the *shape* of, without needing this chapter's derivation to exist first.
>
> In both cases Chapter 2 used the **structural form** of a decision that CLAUDE.md had already
> fixed independently of $d$ — a defining equation's shape and existence conditions — while this
> chapter supplies the **quantitative derivation and value**. This is the ordinary, non-circular
> pattern of a later chapter proving in full what an earlier chapter cited by name (the monograph
> does this routinely, e.g. Ch.3 citing Ch.2's R2.6–R2.9 operationally before either existed in the
> same document); it is not the pathological pattern of a chapter's *conclusion* depending on a
> *number* only a later chapter supplies. **Verdict: G-2 is a genuine gap in the postulate ledger's
> bookkeeping (Chapter 1's P1–P7 table should have flagged CDD2/CDD5 as forward-used, which it did
> only for $c_\text{lat}$'s symbol reservation and not for its role in Ch.2's own derivation), but it
> is not a logical circularity in the physics.** This resolution is appended to
> `docs/monograph/GAPS.md` rather than treated as closing the ledger gap itself, since Chapter 1's
> own table is not this chapter's file to edit.

## 6.2 The derivation

### 6.2.1 The on-axis light cone is exactly straight

Along a coordinate axis, $\mathbf k=k\hat x$, two of R3.1's transverse cosines are $\cos0=1$ and two
of its transverse sines are $\sin0=0$ — both exactly representable in floating point — so
$u(k\hat x)=\cos(k/\sqrt3)$ on **both** helicity branches ($s=\pm1$ drops out because the branch term
carries a factor $s_ys_z=0$). Hence

$$\boxed{\;\omega(k\hat x)=\arccos u(k\hat x)=\frac{k}{\sqrt3}\;}\qquad\text{for every }k\in[0,\pi\sqrt3],\text{ both branches,}\tag{R6.1}$$

an algebraic identity, not a small-$k$ limit: $\partial^2\omega/\partial k_x^2\equiv0$ along the axis,
so the on-axis dispersion carries **no** $k^2$ or higher correction of any kind. This is verified at
tolerance $0$ (bit-for-bit) at 500 sample points on both branches, with the body-diagonal residual
($1.954$, order-unity) serving as the control that keeps the exact check from being a tautology
(F20 §"The closed forms", test `F20-bcc-onaxis-dispersion-exact`, gate tier). No other direction on
the BCC lattice shares this property; §6.2.4 below gives the general (off-axis, dispersive) case.

### 6.2.2 The general small-$\lvert\mathbf k\rvert$ limit, and the value $1/\sqrt3$

Away from the axes, expand R3.1's $u(\mathbf k)=c_xc_yc_z+s\,s_xs_ys_z$ with $c_i=\cos(k_i/\sqrt3)$,
$s_i=\sin(k_i/\sqrt3)$ to leading order:

$$c_xc_yc_z=1-\frac{k_x^2+k_y^2+k_z^2}{6}+O(k^4),\qquad s\,s_xs_ys_z=O(k^3)$$

(the branch term is odd, hence subleading and direction-anisotropic — this is exactly the term
F245/F246 characterise in closed form, §6.4 below). So $u(\mathbf k)=1-\lvert\mathbf k\rvert^2/6+
O(k^3)$ **isotropically** to this order — matching Ch.2's R2.13 (full $O_h$ recovered exactly at
leading order) — and

$$\omega(\mathbf k)=\arccos u(\mathbf k)=\sqrt{2(1-u)}+O\big((1-u)^{3/2}\big)=\frac{\lvert\mathbf
k\rvert}{\sqrt3}+O(k^2)\quad\text{as }\lvert\mathbf k\rvert\to0.\tag{R6.2}$$

The single-branch **phase velocity** $\omega(\mathbf k)/\lvert\mathbf k\rvert\to1/\sqrt3$ as
$\lvert\mathbf k\rvert\to0$: this is the textbook reading, computed directly from Chapter 3's
stepper with no further input.

### 6.2.3 The rotation-rate reading, and its value

The alternative reading (CLAUDE.md Core Design Decision 2, F26) is built not on $\omega(\mathbf k)$
itself but on the angle a **real bilinear pair** traverses per tick. For a spinor mode at momentum
$\mathbf k/2$, form the bilinear $G$ built from $\psi$ (the composite object standing in for
$(\mathbf E,\mathbf B)$); under one application of the walk this bilinear's own phase advances at
**twice** the single-particle rate, evaluated at half the momentum — a bilinear in $\psi$ inherits
the phase of $\psi\otimes\psi^{*}$, and both factors are displaced by $\mathbf k/2$ in the paired
construction Chapter 8 derives in full (F67/F68/F69; the pairing itself is that chapter's content,
not re-derived here). This gives the exact discrete rotation law (F26, from F25's real-rotation
identity, reproduced from the source finding rather than re-derived):

$$\mathbf E(t+1)=\cos\Omega\,\mathbf E(t)+\sin\Omega\,\mathbf B(t),\qquad \mathbf
B(t+1)=-\sin\Omega\,\mathbf E(t)+\cos\Omega\,\mathbf B(t),\qquad \Omega(\mathbf
k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2),\tag{R6.3}$$

exact to machine precision (F26 §Background, citing F25's $2.0\times10^{-16}$ residual), with
$\omega^\pm$ R3.1's two helicity branches. Because $u^\pm(-\mathbf q)=u^\mp(\mathbf q)$ (the BCC
chiral constraint, §6.4 below), $\Omega(\mathbf k)$ is manifestly the **even** ("paired," non-
birefringent) combination — the propagator CLAUDE.md's Core Design Decision 5 identifies as the
physical photon's, carried forward unchanged into the current tree as
`casim.engine.gauge.wmu._f26_rotation_step`. Evaluating the **rotation rate**,

$$c_\text{lat}:=\frac{d\Omega}{d\lvert\mathbf k\rvert}\bigg\rvert_{\lvert\mathbf
k\rvert\to0}=2\cdot\frac{d}{d\lvert\mathbf k\rvert}\,\omega\!\left(\frac{\lvert\mathbf
k\rvert}{2}\right)\bigg\rvert_{0}=2\cdot\frac12\cdot\frac{1}{\sqrt3}=\frac1{\sqrt3},\tag{R6.4}$$

using R6.2's leading-order slope for $\omega$. **The two readings give the identical number at
leading order** — this is the sense in which §6.1 item 2's interpretive choice carries no numerical
content at this order — and the value matches the general BDPT closed form $c_\text{lat}=1/\sqrt
d\rvert_{d=3}$ already cited (without derivation) at Ch.2 §2.5 and in F26's own "more primitive
definition" remark.

$$\boxed{\;c_\text{lat}=\frac1{\sqrt3}=0.5773502692\ldots\;}\tag{R6.5}$$

(F26, `exact`; CL001, `live`, `exact`, `provenance: authored`.)

### 6.2.4 What actually distinguishes the two readings

Off leading order the two readings separate, and this is where the rotation-rate picture earns its
keep as more than a relabelling. Taylor-expanding R6.3's rotation to first order in $\Omega$ gives
$d\mathbf E/dt=\Omega\cdot\mathbf B=c_\text{lat}\lvert\mathbf k\rvert\,\mathbf B$, i.e. in position
space $\partial_t\mathbf E=c_\text{lat}\nabla\times\mathbf B$ — **Maxwell's curl equation is the
first-order Taylor expansion of the exact rotation, not a separately fundamental law** (F26). The
exact rotation matrix's continuous-time generator,

$$R(\Omega)=\begin{pmatrix}\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{pmatrix}\ \to\
\mathbb I+\Omega J+O(\Omega^2),\qquad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\ J^2=-\mathbb I,
\tag{R6.6}$$

identifies the imaginary unit of the continuum Maxwell equations with the real $2\times2$
antisymmetric generator of this rotation — "the imaginary unit is not fundamental; it is the
algebraic artifact of linearizing a real rotation" (F26). Energy conservation, correspondingly,
becomes **geometric** rather than dynamical: $\lVert\mathbf E\rVert^2+\lVert\mathbf B\rVert^2$ is
conserved because a rotation preserves length (Pythagoras), not because of a separately-imposed
Poynting theorem. Mohr's independent six-component reformulation of the free Maxwell equations
(`references/mohr-2010-maxwell-photon-wf-summary.md` §3, Eqs. 41–42) is external corroboration that
packaging $(\mathbf E,\mathbf B)$ into one first-order rotating object is a legitimate, previously
known move in the literature, not an artifact of this model — though Mohr's construction stays in
the continuum and does not itself make the "rotation, not propagation" ontological claim CDD2 makes.

$$\boxed{\;\text{Maxwell's curl law}=O(\Omega)\text{ linearisation of the exact rotation (R6.3)};\quad i\leftrightarrow J,\ J^2=-\mathbb I;\quad\text{energy conservation}=\text{rotation-length invariance}\;}\tag{R6.7}$$

### 6.2.5 The BCC spin axis: the object every formula above is built on

R3.1's $\tilde{\mathbf n}(\mathbf k)$ and its unit form $\hat{\mathbf n}(\mathbf k)$ — the **BCC spin
axis**, the Bloch vector of the positive-helicity eigenmode, $(\hat{\mathbf n}\cdot\boldsymbol
\sigma)\psi_+=+\psi_+$ — has the closed form (F26b, sign convention '+'):

$$u=c_xc_yc_z+s_xs_ys_z,\quad n_x=s_xc_yc_z-c_xs_ys_z,\quad n_y=-c_xs_yc_z+s_xc_ys_z,\quad
n_z=c_xc_ys_z+s_xs_yc_z,\qquad\hat{\mathbf n}=\mathbf n/\lvert\mathbf n\rvert,\tag{R6.8}$$

with continuum limit $\hat{\mathbf n}\to(\hat k_x,-\hat k_y,\hat k_z)$ — an intrinsic $y$-sign flip
that is the same chirality-convention artefact Ch.3 §3.1 already flagged as a free labelling choice,
not new content. This closed form is the object every group-velocity and helicity-projection
formula in this chapter and in F20/F46 is built from (F26b §"The BCC Spin Axis", checks A/B,
residuals $2.8\times10^{-14}$/$6.2\times10^{-14}$, gate tier `F26b-spin-axis-scalar-contamination`).
F26b's own headline result — the scalar contamination of the *retired* $(1,0)$ $\sigma$-bilinear
representation under a Lorentz boost, $\lvert\psi^T\psi\rvert^2=1-\hat n_y^2$ — is a property of a
construction CLAUDE.md's Core Design Decision 5 no longer identifies as the physical photon (S1,
F65–F67$\to$F69; the $\sigma$-bilinear is retained only for the W/Z/gluon sector, Ch.12–13); it is
recorded here as a correct, unsuperseded closed-form result, but its principal forward relevance is
to Chapter 7's boost analysis and to Chapter 12–13's retained bilinear construction, not to this
chapter's photon. Only R6.8's $\hat{\mathbf n}(\mathbf k)$ itself is load-bearing for §6.2's
dispersion story.

$$\boxed{\;\hat{\mathbf n}(\mathbf k)\text{ (R6.8) is the shared geometric object behind every dispersion/group-velocity formula in this chapter; F26b's own scalar-contamination result belongs to Ch.7/Ch.12–13, not Ch.6}\;}\tag{R6.9}$$

### 6.2.6 The massive dispersion: a spherical Pythagorean law, and Einstein's mass shell

Combining R3.1's massless kinetic step with the chiral-$SU(2)$ mass step (P6; Ch.11's construction,
used here only through its rotation angle $\Omega_\text{rest}(m)=\arcsin m$ at $\mathbf k=0$) gives
the 4-component Dirac propagator $D_{\mathbf k}=\begin{psmallmatrix}nW_{\mathbf k}&im\mathbb I\\
im\mathbb I&nW_{\mathbf k}^\dagger\end{psmallmatrix}$, $n=\sqrt{1-m^2}$. Its eigen-frequency
$\Omega_\text{Dirac}(\mathbf k,m)$ satisfies, exactly (F46 §3, from the characteristic equation of
the $2\times2$ blocks, using the QCA admissibility constraint $n^2+m^2=1$):

$$\boxed{\;\cos\Omega_\text{Dirac}(\mathbf k,m)=\cos\Omega_\text{rest}(m)\cdot\cos\omega_\text{kin}(\mathbf
k)=\sqrt{1-m^2}\,\cos\omega_\text{kin}(\mathbf k)\;}\tag{R6.10}$$

— the spherical law of cosines for a right spherical triangle with legs $\Omega_\text{rest}(m)$ and
$\omega_\text{kin}(\mathbf k)$ (R6.2's massless dispersion) and hypotenuse $\Omega_\text{Dirac}$.
Expanding both sides in $\cos x=1-x^2/2+x^4/24-\ldots$ and matching at $O(s^2)$ gives $\Omega^2=m^2+
\omega_\text{kin}^2+O(s^4)$; substituting R6.2's $\omega_\text{kin}\to c_\text{lat}\lvert\mathbf
k\rvert$ and identifying $\Omega\leftrightarrow E$, $m\leftrightarrow mc^2$, $\lvert\mathbf
k\rvert\leftrightarrow p$:

$$\boxed{\;E^2=m^2c^4+p^2c^2+O(\text{lattice}^4)\;}\tag{R6.11}$$

**Einstein's relativistic mass-shell relation is the continuum limit of an exact discrete spherical-
trigonometric identity**, not a separately postulated axiom (F46 §3.4, P7 fit: measured $O(s^4)$
log-log slope $4.0055$ against a predicted $4.0$). The identity holds on both the 2D-square and 3D-
BCC lattices, both helicity branches, verified to $3.3\times10^{-16}$–$9.4\times10^{-16}$ across
eight independent checks (F46, test `test_F46_pythagorean_mass.py`, 8/8 PASS). This is also this
model's realisation of a construction Ludwig's own 2007 notes proposed and then rejected for the
wrong reason — a helical trajectory, $c^2=v_\text{eff}^2+(2\pi\nu r)^2$
(`references/physics-notes-complete.md` pp. 73–74) — dismissed there because $v\to c$ as $E\to\infty$
appeared wrong; relativistically that limit is correct, and F46 §7 identifies the notebook's
Euclidean-Pythagorean approximation as the small-angle limit of the exact spherical law above.

### 6.2.7 Subleading structure: two constructions, one superseded reading

Two closed-form completions of the leading-order dispersion exist, and they are **not** the same
object, a distinction the tree's own 2026-08-04 review (ledger `S18-curl-residual-representation-
artifact`) forces onto this chapter's presentation.

**F245 (closed form, but for a since-reclassified construction).** Finding 7 (pre-dating this
chapter's tree) measured a curl residual for the retired $\sigma$-bilinear ("composite-photon")
construction, $\text{curl residual}/\lVert k\rVert=1/\sqrt{2d}+(\text{subleading})$. F245 derives the
subleading terms exactly: $\alpha(p)=(\cos4p-9)/768$ on the 2D square lattice (on-axis value
$-1/96$, derived algebraically as $r/k=1/2-k^2/96+O(k^4)$ from the exact bilinear evolution) and
$\beta(\hat k)=-(\sqrt2/12)\hat k_x\hat k_y\hat k_z$ on 3D BCC (verified to $9\times10^{-15}$,
vanishing on every coordinate plane, extremal on the body diagonals). **These closed forms are
correct as derivations of a well-defined mathematical quantity, but that quantity is not a physical
Lorentz-violation coefficient.** The 2026-08-04 review (S18, superseding F21/F23/F25's
*interpretation*, not their measurements) found the residual's two sides are orthogonal, equal-
length real 3-vectors by construction ($\lVert\text{LHS}\rVert/\lVert\text{RHS}\rVert=1.0000000000$
at every $\mathbf k$), so $c_\text{lat}/\sqrt2$ "is $c_\text{lat}$ — by its own definition $c_\text{
lat}=d\Omega/d|\mathbf k|$ (F26) — times a quadrature factor," carrying zero evidential weight as a
physical dispersion correction (`docs/theory/supersessions.yaml` S18; exactness-inventory row #3).
F245's own derivation is retained as correct mathematics about that (now understood to be
artifactual) quantity; it is not cited below as a physical prediction.

**F246 (the physical result).** The *actual* even-rotation propagator's dispersion,
$\Omega_\text{even}(\mathbf k)/\lvert\mathbf k\rvert=c_\text{lat}+c_3(\hat k)\lvert\mathbf
k\rvert^2+\ldots$ (this is R6.3's $\Omega$, the module the paired photon actually runs on), has two
closed-form results:

$$\boxed{\;\text{all even-power }(k^2,k^4,\ldots)\text{ dispersion corrections vanish identically}\;}\tag{R6.12}$$

— forced algebraically by $\Omega_\text{even}(\mathbf k)=\Omega_\text{even}(-\mathbf k)$ (the BCC
chiral constraint $u_+(-\mathbf q)=u_-(\mathbf q)$, §6.2.3), which permits only odd powers of
$\lvert\mathbf k\rvert$ in an expansion whose leading term is already odd ($c_\text{lat}\lvert
\mathbf k\rvert$) — and

$$\boxed{\;c_3(\hat k)=-\frac{\sqrt3}{216}\big(p+3q\big),\qquad p=\textstyle\sum_{i<j}\hat
k_i^2\hat k_j^2,\ \ q=\hat k_x^2\hat k_y^2\hat k_z^2\;}\tag{R6.13}$$

verified to $4.5\times10^{-19}$ across ten rational directions, vanishing exactly on $\langle
100\rangle$ (matching R6.1's exact on-axis linearity) and extremal on $\langle111\rangle$,
$c_3=-\sqrt3/486=-0.00356389$. **Physical content:** the model's photon carries no CPT-odd ($k^2$)
Lorentz violation of any kind; its leading vacuum-dispersion signature is the CPT-even cubic
$\lvert\mathbf k\rvert^3$ term (F246), exactly the functional form the standard GRB/AGN vacuum-
dispersion literature constrains — the quantitative bound is Chapter 7's job, not this chapter's.

## 6.3 Results table

| # | Statement | Exactness | Residual / tolerance | Source |
|---|---|---|---|---|
| R6.1 | On-axis dispersion $\omega(k\hat x)=k/\sqrt3$, exact for **all** $k\in[0,\pi\sqrt3]$, both branches; no $k^2$ term at any order | exact | tolerance $0$, 500 points, body-diagonal control $1.954$ | F20; test `F20-bcc-onaxis-dispersion-exact` (gate) |
| R6.2 | General small-$\lvert\mathbf k\rvert$ limit $\omega(\mathbf k)\to\lvert\mathbf k\rvert/\sqrt3$, isotropic to this order | exact (closed-form expansion) | — | this chapter §6.2.2, from R3.1 |
| R6.3 | Exact discrete rotation law for the real $(\mathbf E,\mathbf B)$ pair, $\Omega(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ | machine | $2.0\times10^{-16}$ (F25, cited by F26) | F26 §Background |
| R6.4/R6.5 | $c_\text{lat}:=d\Omega/d\lvert\mathbf k\rvert\rvert_0=1/\sqrt3=0.5773502692\ldots$ | exact | closed form | F26; CL001 (`live`, `exact`) |
| R6.6/R6.7 | Maxwell's curl law is the $O(\Omega)$ linearisation of R6.3; $i\leftrightarrow$ the real generator $J$, $J^2=-\mathbb I$; energy conservation is geometric | exact | closed-form Taylor identity | F26 §"Consequences" |
| R6.8 | BCC spin axis $\hat{\mathbf n}(\mathbf k)$, closed form; continuum limit $(\hat k_x,-\hat k_y,\hat k_z)$ | exact | $2.8\times10^{-14}$/$6.2\times10^{-14}$ | F26b; test `F26b-spin-axis-scalar-contamination` (gate) |
| R6.9 | F26b's own scalar-contamination headline belongs to the retired $\sigma$-bilinear construction (Ch.7/12–13), not this chapter's photon | — (scoping statement) | — | this chapter §6.2.5 |
| R6.10 | Spherical Pythagorean identity $\cos\Omega_\text{Dirac}=\sqrt{1-m^2}\cos\omega_\text{kin}$ | exact | $\le3.3\times10^{-16}$ (2D), $\le9.4\times10^{-16}$ (BCC) | F46; `test_F46_pythagorean_mass.py` (8/8) |
| R6.11 | Continuum limit $E^2=m^2c^4+p^2c^2+O(\text{lattice}^4)$; $O(s^4)$ slope measured $4.0055$ vs. predicted $4.0$ | exact (identity) / quantitative (slope fit) | slope $4.0\pm0.05$ | F46 §3.4, P7 |
| R6.12 | All even-power ($k^2,k^4,\ldots$) corrections to the even-rotation law vanish identically | exact | forced by $\Omega_\text{even}(k)=\Omega_\text{even}(-k)$ | F246 |
| R6.13 | $c_3(\hat k)=-(\sqrt3/216)(p+3q)$, the leading (cubic, $\lvert k\rvert^3$) LIV-relevant coefficient | machine | $4.5\times10^{-19}$, 10 directions | F246; `casim.engine.interactions.derive_f26_dispersion` |
| R6.14 | F245's $\alpha(p)$/$\beta(\hat k)$ closed forms are correct math for a construction (the $\sigma$-bilinear curl residual) since reclassified as a representation artifact, not a physical LIV coefficient | exact (as math) / **not physical** (per S18) | $2.8\times10^{-19}$/$9\times10^{-15}$ | F245; `docs/theory/supersessions.yaml` S18 |
| R6.15 | Slow light/EIT: the rotation-rate and phase-velocity propagators agree to machine precision; the Sommerfeld front stays exactly luminal regardless of $v_g$'s sign | machine | $\le4.1\times10^{-16}$ | F171; CL151 (`live`, `unreviewed-seed`) |
| R6.16 | Radiation equation of state: $w=1/3$ exactly at leading order (Euler's theorem on the degree-1-homogeneous dispersion), with closed-form $\Theta^2$ lattice corrections | exact (leading order) / exact-vs-quadrature (corrections, $\sim4$–$5\times10^{-4}$) | see F300 table | F300; CL260 (`live`, `exact`) — **flagged as a partial reach beyond this chapter's remit, §6.5** |

## 6.4 Comparison with measurement

This chapter fixes the **dimensionless, structural** value $c_\text{lat}=1/\sqrt3$ in lattice-native
units — a statement about the ratio of two lattice-defined quantities (a rotation rate and a
wavenumber), not yet a number with physical units. Converting this to an actual speed in metres per
second requires the lattice spacing $a$'s SI value, which is **not** fixed by anything in this
chapter: that is the canonical-ruler decision of Chapter 17 (F79/F107), forward-cited already at
Ch.1 §1.5 and Ch.2 §2.5. Nothing here should be read as a claim about the measured speed of light in
SI units; what this chapter delivers is the input Chapter 17 needs (the dimensionless dispersion
relation and its exact/closed-form structure) together with the two comparisons that *are*
available at this level:

- **The rotation-rate reading is empirically indistinguishable from the phase-velocity reading in
  every linear-optics regime tested.** F171's slow-light/EIT construction reproduces the Hau (1999,
  17 m/s) and Wang (2000, $-c/310$) anchors to machine precision under *either* reading (R6.15), and
  the Sommerfeld front stays luminal in both. CL001's own falsifier field records this precisely:
  `falsifier: none`, with the stated reason that the claim "makes the same predictions as the
  identification $c=1/\sqrt3$ in lattice units, and is distinguishable only through the structures
  it forces downstream" (birefringence, graviton speed — Chapters 8, 19).
- **The genuinely model-specific signature (R6.13's CPT-even cubic term) is unreachable by slow
  light.** F171's own check (S4) shows the lattice cubic term is set by the *vacuum* wavenumber
  $a\lvert\mathbf k\rvert$, not by the group index $n_g$ a dispersive medium controls — a
  slow-light medium steepens $dn/d\omega$ but leaves $a\lvert\mathbf k\rvert$ untouched, so no
  laboratory dispersion-engineering route enhances it. At optical wavelengths the fractional
  deviation is $\sim10^{-54}$; the only channel where R6.13's coefficient becomes observable is
  cosmological time-of-flight over GRB/AGN baselines, which Chapter 7 carries out in full.

## 6.5 What was excluded, and why

- **Treating $\omega/\lvert\mathbf k\rvert$ (phase velocity) as the fundamental definition of $c$.**
  Not shown wrong — R6.2 computes it and gets the same leading value as the rotation-rate reading —
  but not adopted, per CLAUDE.md's Core Design Decision 2, on the stated grounds that a complex
  phase is "not the propagation rate of a complex phase through space" and that Maxwell's curl
  equation and the appearance of $i$ are better explained as artifacts of linearising a real
  rotation (R6.6/R6.7) than as fundamental. §6.1 records honestly that no source supplies an
  independent argument that this reading is *true* rather than merely equally valid; F171 (§6.4)
  shows the two are laboratory-indistinguishable in every regime tested so far.
- **F245's curl-residual construction as a physical Lorentz-violation coefficient.** Excluded, as of
  the 2026-08-04 review (S18), on the exact grounds given in §6.2.7/R6.14: the residual's two sides
  are orthogonal equal-length real vectors by the bilinear construction's own definition, so the
  measured coefficient $c_\text{lat}/\sqrt2$ is a quadrature artifact of $c_\text{lat}$ itself, not
  an independent physical number. F245's algebra is retained as correct; its physical billing is
  not.
- **The $\sigma$-bilinear ("composite-photon") construction generally, as the model's electromagnetic
  field.** Touched here only through F26b's scalar-contamination result (R6.9) and F245's residual
  (R6.14), both flagged as belonging to a construction Core Design Decision 5 no longer identifies
  with the photon (retired for that role at S1, F65–F67$\to$F69, retained only for W/Z/gluon). Full
  treatment of why is Chapter 8's, not this chapter's.
- **Slow light/EIT as a discriminating test.** Considered explicitly (F171, Track 1.b of the "real-
  world device" programme) and found not to discriminate: S1–S3 show the rotation-rate and phase-
  velocity propagators give the identical real field to machine precision in both a slow (EIT) and a
  fast (gain-doublet) medium, and the front stays luminal regardless. This is reported as a genuine,
  informative negative result (§6.4), not papered over as if some other test had already settled the
  ontological question.

## 6.6 What is still open

1. **No source offers an independent argument that the rotation-rate reading of $c$ is physically
   preferred over the phase-velocity reading, beyond internal elegance (P7) and the conceptual
   payoff of R6.6/R6.7.** This is not a new gap — it is the same open item already disclosed at
   Ch.1's Gap [G-1] (the elegant-design heuristic) and confirmed empirically indistinguishable at
   leading order by F171 — but it is worth restating precisely here, in the chapter that makes the
   claim its headline result: **the two readings currently make identical predictions everywhere
   they have been compared**, and the reinterpretation's evidential weight rests entirely on what it
   forces downstream (Chapters 8, 18, 19 — the paired-spinor photon, the dielectric gravity picture,
   graviton speed), not on any measurement made in this chapter.
2. **F20's item (3) — a composite-photon real-space propagation demonstration — is withdrawn**, not
   merely superseded in interpretation: it used the retired $\sigma$-bilinear construction as "the
   photon," which CLAUDE.md's Core Design Decision 5 no longer endorses in that role. F20's items
   (1) and (2) (Weyl and Dirac real-space group-velocity agreement, promoted by their own 2026-08-03
   remediation to $1.7\times10^{-15}$/$1.6\times10^{-15}$) are unaffected and are cited above (R6.1)
   only for the exact on-axis identity, not for the withdrawn photon leg. F314 (outside this
   chapter's assigned finding set, forward-cited in F20's own record) redoes the demonstration with
   the paired-spinor photon and gets the correct target and exact energy conservation — the fix this
   chapter's photon needed, delivered in the tree, just not among this chapter's eight assigned
   findings.
3. **F245's overall constants ($1/768$ in 2D, $\sqrt2/12$ in 3D) and F246's ($\sqrt3/216$) are pinned
   to machine precision but not given a standalone algebraic derivation of their full angular form**
   — only the 2D on-axis case (F245) is closed algebraically. This is disclosed in both source
   findings and simply carried forward.
4. **F246's next coefficient, $c_5(\hat k)$ (the $\lvert k\rvert^5$ term), is not extracted.**
   Named as the natural next step in F246 itself; not attempted here.
5. **F300's radiation-EoS material (§6.7 below) rests on the paired photon's Brillouin zone shape**,
   which F300 itself states is "not settled" and sidesteps by direct measurement in the regime
   ($\Theta\ll1$) where the zone's edge is exponentially suppressed. This is an open geometric
   question this chapter inherits without resolving.

## 6.7 A downstream consequence, flagged as a partial reach: the radiation equation of state (F300)

`00-plan.md` assigns F300 to this chapter, and its headline result *is* a direct corollary of the
dispersion derived above — but the bulk of F300's content (temperature as an emergent scale, the
second law, the generalised-Gibbs-ensemble no-go, the F190 microstate-counting no-go) is genuinely
thermodynamic material whose natural home is Chapter 25's emergent-thermodynamics treatment, not a
chapter about free propagation and the light cone. This chapter states only the corollary that
belongs here and forward-points the rest, rather than force the full apparatus into a chapter it
does not fit.

**The corollary.** At leading order the paired-photon dispersion $\Omega_\text{pair}(\mathbf
k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ (R6.3) is exactly homogeneous of degree 1 along
$\langle100\rangle$ (R6.1's exact on-axis linearity, holding at *every* $\lvert\mathbf k\rvert$, not
just $\lvert\mathbf k\rvert\to0$) and homogeneous of degree 1 to leading order in every direction
(R6.2). Euler's theorem then gives $\mathbf k\cdot\nabla_{\mathbf k}\Omega=\Omega$ for the
momentum-flux pressure $p=\tfrac1{3V}\sum_{\mathbf k}n_B(\mathbf k\cdot\nabla_{\mathbf k}\Omega)$, so

$$\boxed{\;w=p/u=\tfrac13\ \text{exactly at leading order — a theorem of the derived dispersion, not an assumed equation of state}\;}\tag{R6.17}$$

(F300 §3; CL260, `live`, `exact`, `provenance: authored`). The leading finite-lattice correction is a
closed-form pure number times $\Theta^2$ ($\Theta=k_BT\tau/\hbar$, the dimensionless temperature
built from the same lattice tick $\tau$ Chapter 17 will fix in SI units): $u/u_\text{SB}-1=
(40\pi^2/441)\Theta^2$, $\tfrac13-w=(16\pi^2/1323)\Theta^2$, both confirmed against direct
Brillouin-zone quadrature to $\sim4$–$5\times10^{-4}$ relative (F300 §3, Table). At every temperature
this monograph's cosmology chapters actually use (BBN, the QCD crossover, the electroweak scale) the
correction is $10^{-33}$ or smaller — F300's own statement that the continuum assumption these
chapters make is "safe by 44 orders of magnitude at the BBN bottleneck."

**What is explicitly not claimed here.** The temperature scale $T_\text{lat}$, the second-law
analysis (fine-grained entropy conserved exactly; coarse-grained entropy rises to a generalised-Gibbs
plateau, not a Gibbs state, because the free walk carries $2N$ exactly conserved branch-occupation
charges), and the F190 microstate-counting no-go are F300's own content and belong to Chapter 25; they
are not restated here. Readers wanting F300 in full should go to Chapter 25, not treat this section
as a substitute.

## 6.8 Falsifiers

From the relevant claim cards (`docs/claims/`), reported at their actual status rather than smoothed
into a uniform "falsifiable" narrative:

1. **CL001 (the rotation-rate identification itself) carries `falsifier: none`, by design**, on the
   stated grounds that it is a reinterpretation making identical predictions to $c=1/\sqrt3$ at this
   level — it is falsifiable only through the structures it forces downstream, each with its own
   card: CL012 (birefringence) and CL013 (graviton speed), both outside this chapter's scope.
   Chapter 7 is where the model's actual Lorentz-invariance-violation falsifiers (built on R6.13's
   cubic coefficient) are worked out in full against GRB/AGN time-of-flight and LHAASO-class bounds;
   this chapter states only the structural result those bounds test.
2. **R6.1/R6.10's exact identities are falsified in construction**, not by experiment, if a
   recomputation of the BCC stepper's on-axis dispersion or the Dirac spherical-trigonometric
   identity from R3.1 and the chiral mass step yields any nonzero residual beyond floating-point
   round-off — these are closed-form algebraic claims, checkable directly.
3. **R6.12's even-power vanishing is falsified** if any nonzero $k^2$ (or other even-power) term is
   found in the even-rotation law's dispersion; this would also falsify the chiral constraint
   $u_+(-\mathbf q)=u_-(\mathbf q)$ it is derived from, which is itself checkable independently
   against R3.1.
4. **CL151 (F171's no-go) carries `falsifier: unset`** — declared debt in the claims layer (D12),
   not a claim that no falsifier exists. The honest current state is that no laboratory test is known
   that would discriminate the rotation-rate reading from phase velocity in the linear-optics regime;
   Chapter 7's strong-field/polarimetry channels (vacuum birefringence, time-of-flight) are the
   candidates F171 itself names as the places a genuine discriminator might live.
5. **CL260 (the radiation EoS, §6.7) carries `falsifier: stated`**: F300's own falsifier is any
   observed Planck-spectrum distortion of the *lattice-discreteness* type,
   $\delta I_\nu/I_\nu\propto(\nu\tau)^2$ with the derived coefficient, at frequencies far below
   $1/\tau$ — and F300 is explicit that the predicted distortion is unobservably small at any
   currently reachable sensitivity (FIRAS-class $10^{-5}$ corresponds to $T\approx1.2\times10^{29}$
   K), a falsifier that cannot currently fire, disclosed as such rather than left implicit.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–3's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $c_\text{lat}$ | The lattice speed of light, $c_\text{lat}=d\Omega/d\lvert\mathbf k\rvert\rvert_0=1/\sqrt3$ in lattice-native units — a rotation rate of the real $(\mathbf E,\mathbf B)$ pair, not a phase velocity. Discharges Ch.1's forward reservation. | §6.2.3 |
| $\Omega(\mathbf k)$, $\Omega_\text{even}(\mathbf k)$ | The rotation angle of the real bilinear pair per tick, $\Omega=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$; even under $\mathbf k\to-\mathbf k$ by the BCC chiral constraint (R6.12). | §6.2.3 |
| $\hat{\mathbf n}(\mathbf k)$ | The BCC spin axis: the Bloch vector of the positive-helicity eigenmode of R3.1's $A(\mathbf k)$, closed form R6.8. | §6.2.5 |
| $\Omega_\text{rest}(m)$, $\Omega_\text{Dirac}(\mathbf k,m)$ | The mass-step rotation angle $\arcsin m$ and the full Dirac dispersion, related by the spherical Pythagorean identity R6.10. | §6.2.6 |
| $\Theta$ | The dimensionless lattice temperature, $\Theta=k_BT\tau/\hbar$, used only in §6.7's equation-of-state corollary; the SI value of $\tau$ is a Chapter 17 result. | §6.7 |

---

*This chapter resolves Chapter 2's Gap [G-2] (§6.1) rather than logging a new numbered gap; the
resolution is appended to `docs/monograph/GAPS.md` under a new "Chapter 6" heading. No finding,
claim card, module, or test record was created or modified in the writing of this chapter.*
