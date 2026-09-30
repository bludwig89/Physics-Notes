# Chapter 7 — Relativity on a Lattice

*Chapter 7 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F15-closed-form-lorentz-violation-coefficients.md`,
`findings/F22-velocity-addition-deformed-formula.md`,
`findings/F24-sl2c-boost-4current-covariance.md`, `findings/F28-grb-dispersion-test.md`,
`findings/F30-photon-dispersion-order-anisotropy-birefringence.md`,
`findings/F301-finite-a-boost-covariance-poincare-defect.md`,
`findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md`, and
`findings/F327-chiral-liv-coefficient-excluded-by-crab-electrons.md` (the eight findings
`00-plan.md` §2 assigns to this chapter, all read in full), checked directly against
`docs/theory/supersessions.yaml` (record **S19**, read in full — F15 is the *survivor*, replacing
two of F22's three claims; the direction is stated precisely in §7.2.4 below) and against
`claims-index.md`: **CL029** (F15, `withdrawn` — investigated in full in §7.2.3, and shown to be a
claims-layer bookkeeping error, not a physics retraction), **CL032** (F22, `withdrawn` — correctly,
per the S19 banner F22's own header carries), **CL034** (F24, `open`/`unreviewed-seed`), **CL262**
(F301+F327, `narrowed`), **CL263** (F301, `live`, rolls up to CL262), **CL284** (F327, `live`,
`no_go`), **CL011** (F28+F30+F107, `live`), **CL012** (F30+F66+F67+F105, `live`), **CL273/CL274**
(F319, `live`). `docs/reviews/F22-review-2026-08-04.md`, `F22-remediation-2026-08-04.md`,
`F24-review-2026-08-04.md`, `F24-remediation-2026-08-04.md`, and `F301-review-2026-08-12.md` are
read in full and cited directly rather than paraphrased from the findings' own summaries.
`references/special-relativity-derived-from-ca-summary.md` is read in full and cited in §7.1/§7.6.
Notation, postulates and results are those of Chapters 1, 2, 4 and 6
(`01-postulates-and-ontology.md`, `02-dimensions-and-lattice-selection.md`,
`04-structural-theorems.md`, `06-free-propagation-light-cone.md`) — $\mathbf k$, $\omega(\mathbf
k)$, $\Omega(\mathbf k)$, $c_\text{lat}$, $A(\mathbf k)$, $D_{\mathbf k}$, $\Theta$, $O_h$/$D_{2h}$/
$D_{4h}$ — extended, never redefined.*

## 7.0 What this chapter establishes

Chapter 1 named a rigid discrete lattice (P1–P3) as breaking exact Lorentz invariance "by
construction," conceded that only an "asymptotic/approximate" recovery is available, and stated
plainly that "whether it survives more rigorous scrutiny is an open question even by the QCA
literature's own account," explicitly deferring the full account to this chapter (Ch.1 §1.7 item
4). This chapter is that account. It shows: (i) the free single-Weyl-particle current algebra is
exactly covariant under the continuum SL(2,ℂ) boost — a textbook identity, correctly implemented,
that nonetheless says nothing about whether the lattice's own discrete *evolution* commutes with a
boost (F24); (ii) the entire failure of the Poincaré algebra at finite lattice spacing reduces to
the gradient of a single scalar — the off-shell invariant mass — whose order is fixed exactly by a
channel's branch structure: zero to all orders on the cubic axes, cubic ($O(|\mathbf k|^3)$) for the
even, paired-spinor photon, and one order worse ($O(|\mathbf k|^2)$) on a bare chiral branch (F301);
(iii) no single momentum reparametrisation can repair this for more than one channel at a time — the
DSR escape exists per-channel but is not a spacetime symmetry (F301, CL263); (iv) the closed-form
time-dilation Lorentz-violation coefficients are exact functions of the mass, all four strictly
negative, and supersede two of three claims from an earlier, independently-retracted finding on
velocity addition, whose one surviving claim they subsume (F15, replacing F22 per **S19**); (v) the
linear-in-$k$ piece of the photon dispersion is not a net time-of-flight effect at all — it is
chiral, cancels between the two paired helicities, and survives only as vacuum birefringence, which
is the sharper and different observational target (F30); (vi) reconciling the model's physical
Brillouin-zone cutoff with its own counterterm program shows the leading photon Lorentz-violating
operator is dimension-6, not dimension-5, with an exact rational coefficient — and that this closed
form is the same $O(|\mathbf k|^3)$ coefficient Chapter 6 already derived (R6.13), now confirmed to
$1.1\times10^{-20}$ by an independent route (F319); and (vii) the photon prediction is safely
consistent with every current bound by roughly fifteen decades (F28), while the *fermion* sector's
$O(|\mathbf k|^2)$ chiral defect, converted to physical units through the canonical lattice ruler, is
excluded by Crab-Nebula electron observations by just over seven decades — the sharpest, and only
currently-firing, falsifier this monograph has produced so far (F327). The honest answer to Chapter
1's open item, given in full in §7.6, is: clearer, but not closed, and closed in the *wrong*
direction for one physically-important channel.

## 7.1 Inputs

**Postulates used.** **P1** (discreteness) and **P2** (locality) throughout — every result below is
a statement about the same fixed, finite, iterated unitary Chapters 2–3 built, not about a continuum
limit taken in advance. **P3** (homogeneity/isotropy of *some* lattice, with the *specific* point
group left to Ch.2) is the postulate this chapter's entire subject matter tests the consequences of:
a genuine Lorentz boost is a continuous one-parameter family of transformations, and Ch.2's R2.12/
R2.13 already established that the lattice's own *exact* dynamical point group is the finite $D_{2h}$
(order 8) or $D_{4h}$ (order 16), never the full $O_h$ (order 48) at the lattice scale — full $O_h$
recovered only in the infrared, with a $C_3$-violating residual that is exactly $O(k^2)$ and shrinks
linearly in $|\mathbf k|$. This chapter is the continuous-boost analogue of that same fact: where
Ch.2 characterized the *rotation* subgroup's exact failure, this chapter characterizes the *boost*
sector's exact failure, and the two turn out to share a structural signature (§7.2.2). **P4**
(exact unitarity, $\mathcal U=e^{-iH}$) is what makes "the algebra of $H$, $P$, $K$" a well-posed
question at all — F301's entire construction is built on the exact spectral content of the update.
**P5** (the Weyl-spinor primitive) fixes the object every current and boost generator below acts on.
**P6** enters through the massive Dirac construction (F15, F22, F301 §3.1, F327) via the same
chiral-$SU(2)$ mass mechanism used throughout. **P7** is not invoked as a selection criterion in this
chapter — every result below is a computation, not a choice among equally-consistent alternatives.

**Prior results used, precisely.** **R2.12/R2.13** (Ch.2) — the exact finite point group and its
infrared-only completion to $O_h$ — is the discrete-rotation precedent this chapter's boost-sector
result (R7.3) mirrors structurally. **R4.7/R4.8** (Ch.4) — the exact discrete CPT theorem $\Theta
D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ for the free BCC Dirac walk, holding at *every* $\mathbf
k$ and mass with no small-$k$ expansion, together with the companion proof that ordinary parity
$\Pi$ alone cannot exist at any finite $\mathbf k$ — is the exact-symmetry baseline this chapter's
LIV results must be read against; §7.2.7 states precisely how F327's "CPT-odd" classification of its
excluded operator coexists with R4.7's exact $\Theta$-symmetry of the *same* dispersion, rather than
contradicting it. **R6.1** (Ch.6) — the algebraically exact on-axis linear dispersion, $\omega(k\hat
x)=k/\sqrt3$ for all $k$, both branches — is F301's own closed-form explanation for why the boost
defect vanishes to *all* orders specifically on the cubic axes. **R6.12/R6.13** (Ch.6, F246) — the
even-power vanishing of the paired photon's dispersion corrections, and the closed-form cubic
coefficient $c_3(\hat k)=-(\sqrt3/216)(p+3q)$ — is the exact object F319's dimension-6 result
reproduces from an independent route (§7.2.6 verifies the two agree algebraically, not merely
numerically). **R6.14** (Ch.6) is explicitly *not* re-invoked as a physical dispersion coefficient:
per the 2026-08-04 review (`supersessions.yaml` **S18**), F245's curl-residual construction is a
quadrature artifact of $c_\text{lat}$ itself, not an independent Lorentz-violation number, and
Chapter 6 already corrected this — this chapter follows that correction rather than re-opening it.

**Free inputs consumed, and precisely what work the lattice spacing does.** This is the sharpest
place this chapter must be exact, because the eight findings do not all consume $a$ the same way.

1. **F15's four coefficients, F22's surviving $\rho(m)$, F30's anisotropy/birefringence structure,
   and F301's entire algebra are dimensionless and structural.** None needs a numerical (SI) value
   of the lattice spacing $a$ — F15 §6 proves this explicitly ("$a$ is decorative... it cancels
   identically, before any expansion, at every order," checked to a spread of $1.3\times10^{-54}$
   across four values of $a$), and F301's $D_i,\Phi$ are functions of $\mathbf k$ and $m$ in
   lattice-native units throughout. These results hold regardless of what Chapter 17 eventually
   fixes $a$ to be in metres.
2. **F319's decoupling table and F327's physical-units confrontation both consume the *canonical*
   ruler, $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F79/F107) — a Chapter 17 result, spent here rather than
   derived here.** F319 uses it to compute $\Lambda_\text{UV}=\hbar c/a=1.8504\times10^{18}$ GeV
   and the resulting fractional-deviation table (§7.2.6); F327 uses the identical value to convert
   its dimensionless $b_2(\hat k)$ coefficient into $\eta=2\sqrt{8\pi}\,3^{1/4}/9=1.4661814811$ and
   $E_\text{LV}=8.327\times10^{18}$ GeV (§7.2.7). Both findings are explicit that this consumes,
   rather than derives, the canonical decision — the derivation itself is Chapter 17's, forward-cited
   here and in Ch.1/Ch.2/Ch.6 already.
3. **F28's own quoted number predates that canonical decision, and does not match it.** F28's table
   uses a *different*, provisional assumption — "assuming the lattice tick equals the Planck time"
   — giving $E_{\text{QG},2}^{F26}=\sqrt2\,E_\text{Planck}\approx1.73\times10^{19}$ GeV. The later
   claim card **CL011**, which folds in F107's actual canonical value, states the updated number as
   $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV — a genuinely different figure
   (a $\sim27\%$ shift), from a different, non-provisional value of $a$. Nothing in the findings read
   for this chapter reconciles F28's own displayed table with CL011's updated number; both numbers
   are so far below every current bound (§7.5) that the *qualitative* conclusion (currently
   untestable by $\sim15$ decades) is unaffected either way, but the discrepancy is a genuine,
   unreconciled loose end in the documentation, not a rounding artifact, and is logged as Gap
   [G-5] below rather than silently resolved in this chapter's favour.
4. **The exact algebraic results — F301's $D_i=\partial_i\Phi$ construction, the sign theorem of
   F15 §4, F319's dimension-counting and the $\langle100\rangle$ exactness — introduce no fitted or
   chosen parameter anywhere.** Every numerical coefficient in this chapter is either a pure rational
   or algebraic number forced by the BCC dispersion, or (for F327's confrontation) an external,
   registered, unfitted experimental bound.

> **Gap [G-5]:** F28's own results table (`findings/F28-grb-dispersion-test.md`) reports the photon
> LIV energy scale as $E_{\text{QG},2}^{F26}=\sqrt2\,E_\text{Planck}\approx1.73\times10^{19}$ GeV,
> under the explicit, provisional assumption that the lattice tick equals the Planck time. This
> predates the canonical lattice-spacing decision of F79/F107 (`docs/theory/key-decisions.md`), under
> which $a=\sqrt{8\pi}\,3^{1/4}\ell_P\ne\ell_P$. The claim card **CL011**
> (`docs/claims/CL011-quantum-gravity-dispersion-scale.md`), issued later and citing F107 directly,
> states the updated figure $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV — about
> $27\%$ lower. No finding or claim card read for this chapter reconciles the two numbers, updates
> F28's own table, or states which (if either) is the "current" value a reader should cite; both are
> so far below every existing bound (by $\sim15$ decades, §7.5) that the discrepancy has no
> observational consequence at present, but it is a genuine, unreconciled inconsistency between a
> finding's own displayed number and a later claim card's updated one — exactly the kind of loose end
> `docs/monograph/GAPS.md` exists to catch. Flagged for whoever finalizes Chapter 17's numerical
> closure (which should either re-derive F28's table with the canonical $a$ or explicitly retire the
> Planck-tick figure) and for Appendix A3 (constants ledger).

## 7.2 The derivation

### 7.2.1 What the continuum current algebra shows, and what it explicitly does not (F24)

Before asking whether the lattice's discrete *evolution* respects boosts, it is worth stating
precisely what the model's algebra *can* be shown to respect with no lattice input at all. The
SL(2,ℂ) pure-boost matrix $A=\exp(-\tfrac\zeta2\,\boldsymbol\sigma\cdot\hat v)$ induces the correct
covering-map action on the Weyl 4-current, $j'^\mu=(A\psi)^\dagger\bar\sigma^\mu(A\psi)=\Lambda^\mu{}_\nu
j^\nu$, verified to $3.71\times10^{-16}$ on a benign sample and to $1.11\times10^{-13}$ over a 2000-draw
worst case (the residual there is *conditioning* — a near-total cancellation for an anti-aligned
boost of a null current — not a machine-epsilon floor). This identity is textbook (Peskin &
Schroeder §3.2; Srednicki ch. 34–35; Weinberg vol. I §2.7), and F24's own 2026-08-04 review found it
to be, precisely, *"the covering map, restricted to the null cone, is the covering map"* — a
correctness check on the implementation, not a physics result: $H\mapsto AHA^\dagger$ on
$\mathrm{Herm}(2)\cong\mathbb R^{1,3}$ **is** the definition of the SL(2,ℂ)$\to SO^+(1,3)$ covering
map, so the identity could not have come out false.

$$\boxed{\;j'^\mu=\Lambda^\mu{}_\nu j^\nu\ \text{exactly, for the continuum SL(2,\mathbb C) boost acting on a single Weyl spinor}\;}\tag{R7.1}$$

(F24, `machine`, residual $3.71\times10^{-16}$ benign / $1.11\times10^{-13}$ worst-case over 2000
draws; test `F24-sl2c-covariance-full`, gate tier.) **What R7.1 is not.** No $a$, no $c_\text{lat}$,
no BCC geometry, no dispersion, no CA tick enters anywhere in this identity — it is pure $2\times2$
continuum spinor algebra, and F24's own corrected text states the load-bearing consequence
explicitly: *"the real question — whether the lattice **evolution** commutes with a boost at finite
$a$... is untouched by this identity and would generically not be exact."* F24's claim card,
**CL034**, remains `status: open`, `review_state: unreviewed-seed` — an administrative fact about
the claims layer's backlog (the card was mechanically seeded in the same 2026-08-04 sweep that
seeded dozens of others and has not yet been promoted), not a statement about the physics, which
F24's own finding text already narrows correctly. R7.1 is recorded here as the baseline this
chapter's real content (§7.2.2 onward) is measured against, and as the finding that first named the
question this chapter answers.

### 7.2.2 The finite-$a$ Poincaré defect is exactly one scalar (F301)

F24's deferred question — does the lattice's discrete update commute with a boost, at finite $a$ —
is not well-posed as literally stated, because the lattice has no boost operator; "boosting a
lattice state" requires *choosing* a map, and F22's own history (§7.2.4 below) is the cautionary
tale of what happens when that choice is made implicitly and not checked. F301 re-poses the question
as one about the **algebra**, which is choice-free: for a free channel with $H=\Omega(\mathbf k)$,
$P_i=k_i$, $x_i=i\partial_{k_i}$, and the minimal boost generator $K_i=\tfrac1{2c^2}\{x_i,\Omega\}$,

$$[K_i,P_j]=i\delta_{ij}\,\Omega/c^2\quad\text{(exact, for arbitrary }\Omega\text{)},\qquad
[K_i,H]=iP_i+iD_i,\qquad D_i(\mathbf k)=\partial_i\Phi,\quad
\Phi=\frac{\Omega^2-c^2|\mathbf k|^2}{2c^2}.\tag{R7.2}$$

Four facts, each verified symbolically for a *general* $\Omega$ (sympy zero), make $D_i$ the
complete obstruction rather than one candidate among several: $[K,P]$ never fails; the $[K,K]$
bracket's own defect reduces algebraically to the *same* $D_i$, so there is no second, independent
seam; $D_i$ is invariant under $K_i\to K_i+f(\mathbf k)$ for any real $f$, so it is not an artifact
of the particular minimal $K$ chosen; and $D_i$ is exactly the coefficient a real boost experiment
would measure, $\Omega'-\Omega(\mathbf k')=v(\mathbf D\cdot\hat v)+O(v^2)$, with the $O(v^2)$ scaling
confirmed to fall $100\times$ per $100\times$ smaller $v$.

$$\boxed{\;\text{finite-}a\text{ boost covariance}\iff\Phi=\text{const}\iff\Omega^2-c_\text{lat}^2|\mathbf k|^2=\text{const}\;}\tag{R7.3}$$

(F301 §2, `exact`, sympy zero on all four legs; test `F301-boost-covariance-defect`, gate tier,
6/6 controls verified red.) On this lattice $\Phi$ is *not* constant, and F301 computes $D_i$ exactly
for every channel the model runs:

- **Exactly zero, to all orders, on the three cubic axes.** Because $\omega(k\hat x)=k/\sqrt3$
  identically (R6.1), $\Phi$ is constant along $\langle100\rangle$ and $\mathbf D$ vanishes there not
  to leading order but *exactly* — verified at $3.5\times10^{-46}$ against a $\langle111\rangle$
  control of $1.8\times10^{-3}$.
- **$O(|\mathbf k|^3)$, rational coefficient, for the F26/F246 even (paired-photon) law:**
  $\mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)|\mathbf k|^3$, with $p,q$ the same cubic invariants R6.13
  already carries — the $\sqrt3$'s cancel exactly between $c_\text{lat}$ and $c_3$, leaving a
  rational number. Verified to $8.3\times10^{-13}$ over four directions after Richardson
  extrapolation.
- **$O(|\mathbf k|^2)$, one order worse, on a single chiral branch:** $\mathbf D^{(s)}=-s\,
  c_\text{lat}(k_yk_z,k_zk_x,k_xk_y)$, whose angular part $b_2(\hat k)=-\tfrac13\hat k_x\hat k_y\hat
  k_z$ is derived here in closed form for the first time (F246 had reported only two numbers on two
  directions; F301 reproduces both from the closed form to $5.5\times10^{-48}$).

$$\boxed{\;\mathbf D=0\ \text{(all orders, cubic axes)};\qquad \mathbf D\cdot\hat k=-\tfrac1{18}(p+3q)|\mathbf k|^3\ \text{(even law)};\qquad \mathbf D^{(s)}=-s\,c_\text{lat}(k_yk_z,k_zk_x,k_xk_y)\ \text{(chiral branch)}\;}\tag{R7.4}$$

(F301 §§3.2–3.4, `exact`/`machine`; residuals $3.5\times10^{-46}$, $8.3\times10^{-13}$,
$7.4\times10^{-18}$ respectively.) **Why the photon is better by exactly one order.**
$b_2(\hat k)\propto\hat k_x\hat k_y\hat k_z$ is an odd cubic harmonic, so $b_2(-\hat k)=-b_2(\hat k)$
and $\mathbf D^{(+)}=-\mathbf D^{(-)}$ at leading order — the paired/even channel of Chapter 8's
photon cancels it exactly, measured to shrink linearly with $|\mathbf k|$. **This is the same
helicity symmetrisation, counted twice, that makes the paired-spinor photon non-birefringent** (F67/
F68) *and* one order more Lorentz-covariant than a bare chiral fermion — the two properties are not
independent facts about the pairing construction but one property read two ways.

$$\boxed{\;\text{the photon's extra covariance order and its non-birefringence share one mechanism: the paired channel's even chirality symmetrisation}\;}\tag{R7.5}$$

(F301 §3.5.) **Exactly at the point Chapter 2's own point-group analysis leaves a structural
signature to compare against:** R2.13 found the walk's leading-order rotation covariance exact
($O_h$ recovered in the infrared) with a $C_3$-violating residual that is exactly $O(k^2)$; F301
finds the boost sector's leading-order covariance likewise exact on a measure-zero set (the cubic
axes) with the leading defect appearing at $O(k^2)$–$O(k^3)$ depending on channel. Both the discrete
rotation subgroup and the continuous boost sector fail at finite $a$ by an anisotropic, momentum-
dependent residual that vanishes at leading order and is closed-form beyond it — the same qualitative
shape recurring in two logically independent computations.

### 7.2.3 F15: the closed-form time-dilation coefficients, and the CL029 bookkeeping error

For the 2D-square lattice's exact Dirac dispersion $\cos\omega(k)=n\cos(ka)$, $n=\sqrt{1-m^2}$,
$a=c_\text{lat}=1/\sqrt2$, define $R(\beta)=\omega_\text{moving}/\omega_\text{static}$ (a specific,
explicitly-flagged choice of "moving clock rate," §7.5 below) and expand $R(\beta)-\sqrt{1-\beta^2}$
in even powers of $\beta$. With $\theta=\arcsin m$, $T=\tan\theta$, closed forms exist to arbitrary
order, e.g.

$$\beta_\text{LV}(m)=\frac12\Bigl(1-\frac T\theta\Bigr),\qquad
\gamma_\text{LV}(m)=\frac18-\frac1\theta\Bigl(\frac T8+\frac{T^3}{24}\Bigr),\tag{R7.6}$$

with $\delta_\text{LV}$ and $\varepsilon_\text{LV}$ (the $\beta^6,\beta^8$ coefficients) given
similarly in F15 §2. A non-perturbative closed form exists as well — $R(\beta)=[\arcsin(m\gamma)-
\beta\arcsin(\beta\gamma\tan\theta)]/\arcsin m$ — confirmed against the module's lattice evaluation
to $6.7\times10^{-15}$, and against an independent re-derivation via a different route to
$8.3\times10^{-17}$.

$$\boxed{\;\beta_\text{LV},\gamma_\text{LV},\delta_\text{LV},\varepsilon_\text{LV}(m)\ \text{closed form, exact algebraic, sign theorem: all four strictly negative for every }m\in(0,1)\;}\tag{R7.7}$$

(F15 §§2–4, `exact`; test `F15-closed-form-lv-coefficients`, gate tier, 6/6 PASS.) $\tan\theta>\theta$
on $(0,\tfrac\pi2)$ forces $T/\theta>1$ and hence every coefficient negative — the lattice clock
runs *slower* than SR at every order, never faster, and the entire tower vanishes as $m\to0$ (the
massless/Weyl sector is exactly Lorentz-invariant at this order; only the massive Dirac sector
carries the deformation, suppressed by $m^2$). §7.2.2's F301 result closes the loop this closed form
left open: §3.6 of F301 shows $D/k|_{k\to0}=1/\rho(m)-1=2\beta_\text{LV}/(1-2\beta_\text{LV})$ for
the 1D reduction, matched to twelve significant figures at every tested mass, and that on the full
BCC lattice the *massive* branch reduces to the identical function, $D_i\to(1/\rho(m)-1)k_i$,
verified to $4.7\times10^{-15}$. **So F15's coefficient is not a 2D-square artifact — it is the
isotropic, leading-order term of F301's general finite-$a$ boost defect, on the canonical lattice
too**, with the BCC-specific anisotropy entering only at the next order.

**The CL029 investigation.** `claims-index.md` lists **CL029** (F15's own claim card) as
`status: withdrawn` — an apparent direct contradiction of S19's statement that F15 is the
*surviving, replacing* finding, not the retracted one. Reading CL029 directly resolves this the same
way Chapter 3 resolved the analogous CL238/F276 discrepancy: the card's own `## Status & history`
section states plainly, *"A supersession/withdrawal banner appears in this finding's header, which
is why the card reads `withdrawn`... the specific ledger record has not been attached — do that
before relying on this status."* But F15's own header, read in full for this chapter (§0 above),
carries **no** supersession or withdrawal banner of any kind — it reads `**Status:** Confirmed — 6/6
PASS. Exact algebraic, zero fitted constants. Independently re-derived by a cold blind agent...`,
with no bracketed banner line at all. The only finding in this chapter's set that *does* carry such a
banner is **F22** (`[PARTIALLY SUPERSEDED 2026-08-04 by F15 — ledger S19-...]`), and CL029's own
`review_state: unreviewed-seed` label confirms it was generated by the same mechanical, prose-scraping
seeding pass that (correctly) produced F22's own withdrawn card, CL032. **The most likely reading is
that the seeding heuristic's banner-detection mis-attributed F22's banner to F15** (the two findings
are cross-referenced extensively in each other's files) rather than reading F15's own header, which
carries no such text. This chapter does not edit claim cards (out of scope, per its
documentation-only mandate), so the inconsistency is reported here precisely, exactly as it was
found, rather than silently smoothed over in either direction: **F15's own finding file is
`Confirmed`, does not appear as a superseded entry anywhere in `supersessions.yaml`'s 23 records, and
S19 names it explicitly as the survivor that replaces two of F22's three claims** — CL029's
`withdrawn` status is very likely a claims-layer bookkeeping defect, not a physics retraction, and
this chapter treats F15's own algebra (R7.6/R7.7 above) as fully live accordingly.

### 7.2.4 What F22 got right, what it got wrong, and exactly how S19 divides the two (F22, replaced by F15)

F22 originally claimed three things from the same 2D-square dispersion as F15: (1) that the SR
Lorentz boost acts *exactly* on the QCA 4-momentum $(\omega,k)$; (2) that the 4-momentum velocity
$u_p=kc_\text{lat}^2/\omega$ and the group velocity $u_g$ satisfy $u_p=\rho(m)u_g$ at $k\to0$ with
$\rho(m)=m/(\sqrt{1-m^2}\arcsin m)=1-2\beta_\text{LV}(m)$; and (3) a closed-form "deformed
velocity-addition formula" built from claim 1. The independent 2026-08-04 review
(`docs/reviews/F22-review-2026-08-04.md`, verdict **OVERSTATED**, 1 PASS / 2 WEAKENS / 10 FAIL)
found claims 1 and 3 false and retracted them; claim 2 survived and is confirmed independently.

**Claim 1 — dead.** The SR boost does *not* act exactly on $(\omega,k)$; it fails already at
$O(v)$, with the leading-order coefficient $1/\rho(m)-1=2\beta_\text{LV}(m)/(1-2\beta_\text{LV}(m))$
— measured $-0.0930513$ against a predicted $-0.0931003$ at $m=0.5$ (relative $5.3\times10^{-4}$),
rising to a $7.1\%$ error in $\omega$ at a finite boost ($m=0.7$, $k=1.0$, $v=0.3$). The finding's
own §"Step 4" had already reported this residual — $d_\text{qca}=v(1-1/\rho)$ — and called it "the
fundamental LV mismatch," a self-contradiction the review's own attack surfaced. Structurally it
cannot hold at all: on the shell $\omega$ is bounded in $[\theta,\pi-\theta]$ and periodic in $k$,
while boost orbits are unbounded hyperbolae. **Claim 3 — dead as stated, and a misnomer, not merely
imprecise.** In the variables where the boost *is* exact — $E=\sin\omega$, $c|\mathbf P|=n\sin(ka)/a$,
for which $E^2-c^2P^2=m^2$ identically and $u_g=c^2P/E$ exactly at every $k$ — velocity composition
is *ordinary, undeformed* Einstein addition, verified to $5.6\times10^{-17}$; the "deformed formula"
F22 headlined describes no lattice observable, and its own third-order estimate underestimates the
real, first-order boost response by a factor of $10^2$–$10^3$ (measured $103\times$ at $m=0.1$,
$3251\times$ at $m=0.5,k=0.01$).

$$\boxed{\;\text{F22 claim 1 (linear boost exact on }(\omega,k)\text{) — FALSE, fails at }O(v)\;}\qquad
\boxed{\;\text{F22 claim 3 (deformed velocity addition) — MISNOMER; the real repair is undeformed in }(E,P)\;}\tag{7.2.4a}$$

**Claim 2 — live, and this is the result S19 carries forward as F15's own companion.**
$\rho(m)=\tan\theta/\theta=1-2\beta_\text{LV}(m)$ was independently re-derived from F15's own
*definition* rather than its stated closed form, at sympy zero, and matched against the numerical
$u_p/u_g$ ratio to $3.4\times10^{-14}$ across $m\in[0.05,0.90]$.

$$\boxed{\;\rho(m)=\tan(\arcsin m)/\arcsin m=1-2\beta_\text{LV}(m)\;-\;\text{CONFIRMED, live, gate-record}\;}\tag{R7.8}$$

(F22 §"Corrections"; test `F22-rho-identity-and-offshell`, gate tier, promoted from `dead_candidate`
by the remediation.) **What is exact, and is the correct replacement for the dead claim 1.** With
$E\equiv\sin\omega$, $P\equiv n\sin(ka)/a$: $E^2-c_\text{lat}^2P^2=m^2$ identically, and the boost
acts exactly on $(E,P)$ — a genuine, nonlinear (doubly-special-relativity-type) realisation, whose
correct prior-art attribution (added by the same review) is Bibeau-Delisle, Bisio, D'Ariano,
Perinotti & Tosini, *EPL* **101** (2013) 60005 (arXiv:1310.6760) and Bisio, D'Ariano & Perinotti,
*Phil. Trans. R. Soc. A* **374** (2016) (arXiv:1503.01017). Two caveats travel with it and are
carried forward into F301's own general treatment (§7.2.2): the action is only *partial* ($\sin\omega
\le1$ forces $|\beta|<n$), and $\omega\mapsto\sin\omega$ is two-to-one across the Brillouin zone, so
the lift back to $\mathbf k$ is ambiguous.

**S19, stated exactly once, for the record.** `docs/theory/supersessions.yaml` record
**S19-F22-velocity-addition-review-retraction**: `kind: retracted_by_review`, `by: [F15]`,
`superseded: []` (deliberately empty — a wholesale marking would be false, since claim 2 is correct
and load-bearing). F15 is the survivor; F22's claims 1 and 3 are dead; F22's claim 2 lives on as a
confirmed, gate-tested result and as F301's own leading-order limit. This chapter presents F15 as
primary (R7.6/R7.7) and cites F22 only for its one surviving claim (R7.8) — never as a "clean
derivation," per the assignment brief.

### 7.2.5 The chirality/anisotropy structure of the leading photon term (F30)

The BCC dispersion $\Omega^\pm(\mathbf k)=2\omega^\pm(\mathbf k/2)$ is exactly $c_\text{lat}k$ on the
cube axes (R6.1), picks up a quadratic correction on face diagonals, and — on a **single** chirality
branch — a genuinely **linear** correction along body diagonals, $\Omega^+\approx c_\text{lat}k-
\tfrac{\sqrt3}{54}k^2$ (sympy-exact, log-log slope $2.0020$ confirming the exponent). Decomposing
into the chirality-even part $\tfrac12(\Omega^++\Omega^-)$ (what unpolarised time-of-flight sees)
and the chirality-odd part $\tfrac12(\Omega^+-\Omega^-)$ (the birefringent splitting) along
$\langle111\rangle$:

$$\Omega^+-\Omega^-=-\frac{\sqrt3}{27}k^2\ \Rightarrow\ \frac{\Delta v_\phi}c\Big|_\text{biref.}=-\frac k9\ \ (\text{linear, }n=1),\qquad
\frac{\Omega^++\Omega^-}2=c_\text{lat}k+O(k^3)\ \ (\text{net, }n=2).\tag{R7.9}$$

$$\boxed{\;\text{the linear (}n{=}1\text{) piece is chiral and cancels between the two helicities; unpolarised time-of-flight is genuinely quadratic (}n{=}2\text{) in every direction}\;}\tag{R7.10}$$

(F30, `exact` for the sympy series/decomposition, `high-precision numeric` for the log-log slopes;
test `test_F30_dispersion_order.py`.) This resolves what F30's own header calls a direct
contradiction the project once carried between two earlier documents disagreeing on whether the
leading correction is linear or quadratic: **both were right, about different observables.** The
linear $-k/18$ (single-chirality, body-diagonal) is real but manifests only as **vacuum
birefringence** — an energy-dependent rotation of the polarisation plane, maximal on body diagonals
and exactly zero on cube axes — not as a net arrival-time shift. F30 itself flags, as its own
critical open item, whether the two physical circular polarisations correspond to the two BCC
chirality branches at all; per CLAUDE.md's Core Design Decision 5 and Chapter 8's own construction,
the physical paired-spinor photon *is* the even combination by construction (F69), which is exactly
why **CL012** can state the physical photon is "exactly non-birefringent — structurally, not within
a tolerance": the chirality-odd piece that would carry F30's linear birefringence signal is precisely
the piece the pairing construction cancels (R7.5 above, same mechanism).

### 7.2.6 The UV/EFT organization: a physical cutoff and a counterterm program are one statement (F319)

Row A11 of the completeness rubric recorded, for three reports running, that the model's physical
Brillouin-zone cutoff and its full continuum-style renormalisation program (F264) were nowhere
reconciled. F319 supplies the dictionary: on a physical cutoff there are no divergences, so a
"counterterm" is not a subtraction of an infinity but the finite map from bare lattice parameters to
measured ones; the $\ln$ coefficient of a one-loop amplitude is universal across any compact-BZ
regulator (verified to $8.4\times10^{-12}$ between an unimproved and a Symanzik-improved lattice
action against the continuum value $1/16\pi^2$), while the additive constant is scheme-dependent and
IR-independent (drift over a six-decade mass ladder: $2.0\times10^{-12}$) — which is exactly what
licenses F264's counterterm program to run *on top of* a genuinely finite cutoff.

For this chapter's purposes the load-bearing result is the leading irrelevant operator itself.
Expanding the paired-photon dispersion to next order,

$$\frac{\Omega_\text{pair}(k)-c_\text{lat}k}{c_\text{lat}k}=-\Bigl[\frac{1-\sum_i\hat n_i^4}{144}+\frac{\hat n_x^2\hat n_y^2\hat n_z^2}{24}\Bigr]k^2+O(k^4),\tag{R7.11}$$

verified against the F26 symbol to $1.1\times10^{-20}$ in 60-digit arithmetic over nine directions.
**This is algebraically the same object as Chapter 6's R6.13** — using $p=\sum_{i<j}\hat
n_i^2\hat n_j^2=(1-\sum_i\hat n_i^4)/2$ and $q=\hat n_x^2\hat n_y^2\hat n_z^2$, R7.11's bracket
reduces identically to $(p+3q)/72$, exactly $1/(72\sqrt3/216)=c_3(\hat k)/c_\text{lat}$ from R6.13 —
so F319's independently-derived dimension-6 coefficient and F246's dispersion coefficient are the
*same* closed form reached by two different routes, not merely numerically consistent. **There is no
$O(k)$ (dimension-5) term at all** — established as a scaling *exponent* ($p=2$ to better than
$10^{-4}$), which is the phenomenologically decisive statement: dimension-5 photon Lorentz
violation is the operator that killed the earlier, retired $\sigma$-bilinear photon (F65–F67) against
GRB/AGN polarimetry near $10^{-30}$, and the paired photon does not merely satisfy that bound — the
operator is structurally absent, forced by $\Omega_\text{pair}$ being even in the branch label.

$$\boxed{\;\text{leading photon LV operator is dimension-6; coefficient exact-rational, range }[-\tfrac1{162},0]\text{; exactly zero on }\langle100\rangle\text{; no dimension-5 operator at all}\;}\tag{R7.12}$$

(F319 §4, `exact-algebraic`, $1.1\times10^{-20}$; test `F319-uv-completion`, 21/21 PASS, gate tier,
4/4 controls red.) At the F107 cell, the maximum fractional deviation from continuum dispersion is
$3.0\times10^{-31}$ at LHC energies and $3.5\times10^{-27}$ at LHAASO energies (§7.2.7 below spends
this same value differently, for the *fermion* channel).

### 7.2.7 Comparison with observation: the photon survives by fifteen decades, the fermion does not, by seven

**The photon (F28).** F26's quadratic dispersion prediction, confronted with the three strongest
current photon time-of-flight bounds:

| Experiment | Best 95% CL $E_{\text{QG},2}$ | Predicted $\Delta t$ | Sensitivity reached | Margin |
|---|---|---|---|---|
| Fermi-LAT GRB 090510 | $1.3\times10^{11}$ GeV | $3.2\times10^{-18}$ s | $5.7\times10^{-2}$ s | 16.2 decades |
| LHAASO GRB 221009A | $7.0\times10^{11}$ GeV | $6.5\times10^{-14}$ s | $4.0\times10^{1}$ s | 14.8 decades |
| MAGIC Mrk 501 | $5.7\times10^{10}$ GeV | $8.0\times10^{-15}$ s | $7.4\times10^{2}$ s | 17.0 decades |

$$\boxed{\;\text{F26/F319's photon prediction is consistent with every current LIV bound, by roughly 15 decades, and is effectively unfalsifiable by time-of-flight with foreseeable technology}\;}\tag{R7.13}$$

(F28, `quantitative`; test `test_F28_grb_dispersion.py`.) Photon energies $\sim10^7$–$10^8\times$
above any currently observed source would be needed to bring F26's prediction within reach — above
the GZK cutoff, where cosmological-baseline photons are absorbed on the CMB before arrival. Any
observed *linear* ($n=1$) photon dispersion would falsify F26 outright, since the structural
prediction is exactly quadratic with a fixed sign; no such observation exists (§7.1 item 3 records
the one open numerical discrepancy in how this bound is quoted).

**The fermion (F327) — a sharp exclusion.** The chiral $O(|\mathbf k|^2)$ defect of R7.4 is not
merely a lattice-algebra curiosity: a massive BCC Dirac fermion, built from the model's own one-tick
unitary `dirac_bcc.py`, has eigenphases $\pm\arccos(n\,u_+(\mathbf k))$, each two-fold degenerate
(residual $2.3\times10^{-33}$) — i.e. it rides **one** chiral branch, spin-independently, with the
sign flipping between particle and antiparticle. No $k$-independent unitary mass mixing can put the
two Weyl blocks on different branch invariants at all (proved exactly, residual $0.0$, via a trace-
cyclicity argument that is genuine algebra, not merely unsearched); a $k$-dependent, strictly local
one *can* — but its "mass" enters linearly rather than as $m^2/2E$ (it is an axial CPT-odd term, not
a Lorentz-scalar mass), and its spectrum **splits** $b_2$ to $\mp|b_2|$ rather than cancelling it, so
a superluminal eigenstate survives regardless. The photon's escape — a single eigenvalue that is a
**sum** over both branches, $\Omega_\text{even}=\omega_+(\mathbf k/2)+\omega_-(\mathbf k/2)$ — is a
two-quantum construction an elementary one-particle excitation cannot perform.

Converting through the canonical ruler ($a=\sqrt{8\pi}\,3^{1/4}\ell_P$, F79/F107) gives a local,
analytic, dimension-5 CPT-odd operator,

$$E^2=m^2c^4+c^2p^2-\frac2{\sqrt3}\frac{(cp_x)(cp_y)(cp_z)}{E_a},\qquad
|\eta|_\text{max}=\frac{2\sqrt{8\pi}\,3^{1/4}}9=1.4661814811,\qquad
E_\text{LV}=\frac92E_a=8.327\times10^{18}\ \text{GeV}.\tag{R7.14}$$

Confronted with Li & Ma (*Phys. Lett. B* **829** (2022) 137034), whose $1.12$ PeV LHAASO photon from
the Crab Nebula requires electrons of at least that energy (inverse-Compton kinematics):

| | model | bound | verdict |
|---|---|---|---|
| $E_\text{LV}$, superluminal | $8.327\times10^{18}$ GeV | $\ge9.4\times10^{25}$ GeV | short by **7.05 decades** |
| $E_\text{LV}$, subluminal | $8.327\times10^{18}$ GeV | $\ge1\times10^{24}$ GeV | short by **5.08 decades** |

$$\boxed{\;\text{an elementary matter field of this model cannot ride a single BCC chiral branch — excluded by 7.05 (superluminal) / 5.08 (subluminal) decades}\;}\tag{R7.15}$$

(F327, `quantitative`; test `F327-chiral-liv-bound`, 20/20 PASS, gate tier, 2/2 controls red on
exactly the four legs each.) Four candidate escapes are each measured and each closed in the finding
itself (choosing the harmless sign — closed by the operator's oddness, since the Crab is a pair
plasma and both signs are realised; hiding the geometry — the sky fraction evading the bound is
$6.2\times10^{-7}$ and does not survive a gyrating electron sweeping its momentum through a full
circle; shrinking the ruler — costs $G$ a factor $1.3\times10^{14}$, per $G\propto a^2$; blaming the
lattice as such — the *same* ruler leaves the photon's dimension-6 operator $2\times10^{13}$ times
softer at the same energy, so the exclusion is channel-specific, not lattice-wide).

**F301's algebra is not falsified by this.** What R7.15 excludes is the *physical assignment* — that
an elementary fermion of this model may ride a bare, unpaired chiral branch — not the algebra of
$D_i=\partial_i\Phi$ itself, which remains exact and untouched. **CL262 is accordingly `narrowed`,
not `withdrawn`**: its structural content (given a channel and its branch structure, the defect is
$\partial_i\Phi$ with the stated order) is unchanged; what is no longer part of the card is *which*
channels the model may physically use, which is now CL284's content. **CL263** (no universal
momentum map) is untouched by the exclusion and is, per its own sources, *strengthened*: its central
gap — the photon-vs-fermion group-velocity difference — is exactly the observable R7.15 confronts.

**CPT, connected precisely to Chapter 4.** F327 classifies its excluded operator as "CPT-odd" in the
Standard-Model-Extension cataloguing sense — the coefficient flips sign between particle and
antiparticle, and between antipodal directions. This is not in tension with Chapter 4's exact
discrete CPT theorem (R4.7): $\Theta D(\mathbf k)\Theta^{-1}=D(\mathbf k)^{-1}$ was proved for
*exactly* the same `dirac_bcc.py` massive-walk dispersion $\omega=\arccos(nu_+(\mathbf k))$ that
carries the $b_2$ defect, at every $\mathbf k$ and mass, with no small-$k$ expansion — so the model's
own exact antiunitary $\Theta$-symmetry survives *regardless* of the chiral LV term's presence, since
$\Theta$ was never conditioned on that term being absent. "CPT-odd" in F327's sense is a statement
about how the coefficient would transform under the *separate*, individually-broken continuum $C$,
$P$, $T$ factors of an assumed-exact low-energy effective field theory — and Chapter 4's own R4.8
already proved that ordinary parity $\Pi$ alone cannot exist at any finite $\mathbf k$ on this
lattice, so decomposing $\Theta$ into separate continuum $C$, $P$, $T$ pieces is not an operation the
lattice theory supports exactly in the first place. The two facts — exact discrete $\Theta$ (R4.7),
and a "CPT-odd"-classified Lorentz-violating operator excluded by observation (R7.15) — describe
different objects (an exact operator identity of the lattice dynamics; an EFT-matching label for how
a residual transforms) and are both true simultaneously without contradiction.

## 7.3 Results table

| # | Statement | Exactness | Residual / status | Source |
|---|---|---|---|---|
| R7.1 | Continuum SL(2,ℂ) boost acts exactly on the Weyl 4-current | machine | $3.71\times10^{-16}$ benign / $1.11\times10^{-13}$ worst-case | F24; test `F24-sl2c-covariance-full` (gate) |
| R7.2 | The finite-$a$ Poincaré defect is exactly $D_i=\partial_i\Phi$, $\Phi=(\Omega^2-c^2k^2)/2c^2$ — the complete obstruction | exact (sympy zero) | four independent algebraic checks | F301 §2; test `F301-boost-covariance-defect` (gate, 6 controls red) |
| R7.3 | $\mathbf D=0$ (all orders, cubic axes); $O(k^3)$, rational, for the even/paired photon; $O(k^2)$ on a bare chiral branch | exact / machine | $3.5\times10^{-46}$ / $8.3\times10^{-13}$ / $7.4\times10^{-18}$ | F301 §§3.2–3.4 |
| R7.4 | No universal momentum map exists for more than one channel — the DSR repair is per-channel, not a spacetime symmetry | machine | gap $7.9\times10^{-14}$, vanishes on control (coordinate plane, $4.8\times10^{-8}$) | F301 §3.7; **CL263** (`live`, no_go) |
| R7.5 | Closed-form $\beta_\text{LV},\gamma_\text{LV},\delta_\text{LV},\varepsilon_\text{LV}(m)$, all strictly negative | exact algebraic | independent re-derivation $8.3\times10^{-17}$ | F15; test `F15-closed-form-lv-coefficients` (gate). **CL029 marked `withdrawn` — a claims-layer bookkeeping error, per §7.2.3; the finding itself is `Confirmed`, unsuperseded** |
| R7.6 | F22 claim 1 (linear boost exact on $(\omega,k)$) — **DEAD**, fails at $O(v)$ | — | measured $-0.0930513$ vs predicted $-0.0931003$ | F22; retracted by S19, `docs/reviews/F22-review-2026-08-04.md` |
| R7.7 | F22 claim 3 (deformed velocity-addition formula) — **DEAD**, misnomer; real repair is undeformed Einstein addition in $(E,P)$ | — | misses true response by $10^2$–$10^3\times$ | F22; retracted by S19 |
| R7.8 | F22 claim 2 (survives): $\rho(m)=\tan\theta/\theta=1-2\beta_\text{LV}(m)$ | exact / machine | sympy 0; $3.4\times10^{-14}$ | F22 (survives per S19); test `F22-rho-identity-and-offshell` (gate) |
| R7.9/R7.10 | The linear ($n{=}1$) dispersion term is chiral/birefringent, not net time-of-flight; net (unpolarised) dispersion is quadratic ($n{=}2$) everywhere | exact (series) / high-precision numeric (slopes) | log-log slopes $2.0020$, $3.0000$ | F30; test `test_F30_dispersion_order.py`. **CL012** (`live`, exact — physical photon non-birefringent) |
| R7.11/R7.12 | Leading photon LV operator is dimension-6, exact-rational coefficient (algebraically identical to Ch.6's R6.13); no dimension-5 operator at all | exact-algebraic | $1.1\times10^{-20}$ (60 dps) | F319 §4; test `F319-uv-completion` (gate, 21/21, 4 controls red). **CL274** (`live`, exact) |
| R7.13 | F26/F319 photon prediction consistent with all current LIV bounds, ~15 decades below sensitivity | quantitative | see table §7.2.7 | F28; test `test_F28_grb_dispersion.py`. **CL011** (`live`) — see Gap [G-5] re: numerical value used |
| R7.14/R7.15 | Chiral $O(k^2)$ fermion defect $\to$ dimension-5 CPT-odd operator, $|\eta|_\text{max}=1.4662$; **excluded** by Crab electrons by 7.05/5.08 decades | quantitative | see table §7.2.7 | F327; test `F327-chiral-liv-bound` (gate, 20/20, 2 controls red). **CL284** (`live`, no_go); **CL262 narrowed** |

## 7.4 Comparison with measurement

This chapter has more direct observational content than any prior chapter in the monograph. Two
comparisons are live and resolved in opposite directions:

- **The photon survives, by roughly fifteen decades (R7.13).** F26/F319's structural prediction —
  quadratic, not linear, in energy, with a fixed sign and an exact-rational coefficient — is
  consistent with every current bound (Fermi-LAT, LHAASO, MAGIC) and, under present technology and
  the GZK cutoff, is not reachable at all. This is a genuinely different epistemic status from "not
  yet tested": F28 states plainly that no foreseeable photon time-of-flight experiment can test it.
- **The fermion sector fails, by just over seven decades (R7.15).** This is the sharpest, and the
  only currently-*firing*, falsifier this monograph has produced through Chapter 7: F327's
  confrontation with Li & Ma's Crab-Nebula electron analysis excludes the physical assignment "an
  elementary fermion rides a single BCC chiral branch" outright. The exclusion is channel-specific —
  it says nothing against the photon sector or against F301's algebra — but it is a live,
  already-fired result, not a future test.
- **The lattice spacing's numerical value is doing real, but unevenly-sourced, work here** (§7.1
  item 2–3 above): F319 and F327 both spend the canonical ruler of F79/F107 (a Chapter 17 result);
  F28's own displayed number does not (Gap G-5). Chapter 17's eventual numerical closure should
  either re-derive F28's comparison table with the canonical $a$ or explicitly retire the older
  Planck-tick figure in favour of CL011's updated one.
- **F15/F22/F30/F301's coefficients are, by contrast, purely structural** and carry no SI content at
  this stage — they hold in lattice-native units for any eventual value of $a$, and nothing in
  Chapter 17 could falsify them without falsifying the underlying dispersion itself.

## 7.5 What was excluded, and why

- **F22 claims 1 and 3, in full.** Claim 1 ("the SR boost acts exactly on the QCA 4-momentum") is
  false, not merely imprecise: it fails at leading order, $O(v)$, and the finding's own text had
  already measured the failure and called it "the fundamental LV mismatch" one section before
  asserting the boost was exact — a direct self-contradiction the 2026-08-04 review's attack pass
  surfaced (`docs/reviews/F22-review-2026-08-04.md`, verdict OVERSTATED, 1 PASS/2 WEAKENS/10 FAIL).
  Claim 3 ("deformed velocity-addition formula") is a misnomer: in the variables where the boost
  genuinely is exact ($E=\sin\omega$, $P=n\sin(ka)/a$), velocity composition is *undeformed* Einstein
  addition, verified to $5.6\times10^{-17}$, and the formula F22 actually derived underestimates the
  lattice's real boost response by two to three orders of magnitude. Both retractions are recorded in
  `supersessions.yaml` **S19**, with `by: [F15]` and a deliberately empty `superseded:` field, since a
  wholesale supersession marking would falsely retire F22's still-live claim 2.
- **A universal (channel-independent) momentum reparametrisation, as a repair for finite-$a$ Lorentz
  covariance.** Excluded by F301 §3.7/**CL263**: a per-channel DSR realisation exists and is exact
  (R7.4 above, the surviving half of F22's programme), but the F26 even law and a bare chiral branch
  cannot be brought onto the same map — $\Omega_\text{even}(\mathbf k)-\omega_+(\mathbf k)=+\tfrac13
  \hat k_x\hat k_y\hat k_z|\mathbf k|^2+O(k^3)$, non-zero off the coordinate planes and confirmed to
  vanish exactly *on* them (the control that rules out a fit artifact). What is *not* excluded: a
  non-radial map (rotating $\hat{\mathbf P}$ away from $\hat{\mathbf k}$), and any statement about
  multi-particle additivity of the deformed momentum — both are named as the honest residual, not
  claimed closed.
- **An elementary matter field riding a single, unpaired BCC chiral branch.** Excluded observationally
  by F327/**CL284**, by 7.05 (superluminal) and 5.08 (subluminal) decades against Crab-Nebula
  electrons. Every obvious repair is closed in the finding itself: an ultralocal unitary mass mixing
  cannot even separate the two branches (proved exactly, not merely unsearched); a local,
  $k$-dependent one can, but delivers a linear (non-Lorentz-scalar) mass and a *split*, not cancelled,
  spectrum — a superluminal eigenstate survives regardless. What survives as an open repair direction
  — a genuinely paired, two-quantum matter excitation, echoing the photon's own construction — is
  named but not built (§7.6).
- **F245's curl-residual construction, as a physical LIV coefficient (carried over from Chapter 6,
  not re-litigated here).** This chapter's treatment of the photon LIV order (F30, F319) is built
  entirely on the reclassified, physical F26/F246 even-law dispersion, never on F245's retired
  quadrature artifact (S18) — consistent with Chapter 6's own correction.

## 7.6 What is still open

Chapter 1 §1.7 item 4 asked, plainly: is Lorentz invariance's ultimate status any clearer after this
chapter than it was at the postulate level? **Yes, substantially — but the answer sharpens in a
direction the model did not want it to.**

1. **The general shape of the failure is now closed-form and exact, not merely "approximate
   recovery."** Chapter 1 could say only that recovery is "asymptotic" and that "whether it survives
   more rigorous scrutiny is an open question." This chapter answers precisely how much survives:
   exact discrete point-group covariance on the finite $D_{2h}/D_{4h}$ subgroup at every order (Ch.2),
   exact discrete CPT for the free massive walk at every order (Ch.4, R4.7), exact continuum boost
   covariance of the single-particle current algebra (R7.1), and a *single scalar*, $\Phi$, carrying
   the entire remaining defect in the boost sector, with its order fixed exactly by a channel's
   branch structure (R7.2–R7.4). This is a materially stronger characterization than "asymptotic."
2. **But the model's own physical fermion sector has been shown, observationally, to sit on the wrong
   side of that characterization.** This is new relative to Chapter 1: it was not previously known
   whether the finite-$a$ defect was large enough to matter at any reachable energy. F327 shows that,
   for the specific channel ("an elementary fermion rides a bare chiral branch") the model currently
   uses, it does — by seven decades. **The open item has moved from "is there a defect" to "does the
   model's matter sector need a different construction than the one it currently has."**
3. **The repair is a founding-level, unattempted question, not a parameter fit.** F327's own
   recommended next step — asking whether a matter excitation can be a *pair* on this lattice the way
   the photon is, so that its energy is a genuine sum over branches rather than a spectrum containing
   both — is named as ledger row **L9** and is explicitly not attempted by any finding read for this
   chapter. Whether such a construction exists, and whether it is compatible with everything Chapter
   4's spin-statistics and CPT theorems already established for the *current* single-branch Dirac
   walk, is untouched.
4. **The DSR/per-channel escape is real but structurally incomplete**, and this chapter does not
   overstate it: it repairs a single channel exactly (R7.8, R7.4's positive half) but provably cannot
   repair two channels with a single map (CL263), and its own two internal caveats — the partial
   domain ($|\beta|<n$) and the two-to-one lift ambiguity — are carried forward unresolved.
5. **F28's own quoted photon LIV scale has not been reconciled with the canonical lattice-spacing
   decision it predates** (Gap G-5) — a documentation loose end with no current physical consequence,
   but one Chapter 17 inherits.
6. **Elegant-design (P7) offered no argument, and still offers none, for *why* the rotation-rate
   reading of $c$ (Ch.6) should be physically preferred over the phase-velocity reading** — this
   chapter's results are computed identically under either reading (the boost algebra of R7.2 is a
   statement about $\Omega(\mathbf k)$ alone, indifferent to which physical picture "$c$" is read
   from), so nothing here closes Ch.1's Gap [G-1] or Ch.6's item 1 either.

**Honest summary.** Lorentz invariance's status is clearer than Chapter 1 left it — the defect is now
an exact, closed-form, channel-dependent scalar rather than an unquantified "asymptotic" claim — but
it is not resolved, and for the one sector (elementary matter) where the model's current construction
has been checked against a hard observational bound, the checked construction is excluded. The
open question that remains is squarely architectural, not numerical.

## 7.7 Falsifiers

From the relevant claim cards, at their actual status:

1. **CL284 (F327) is a `no_go` that has already fired against the model's current construction.**
   What would *reverse* it: a unitary, massive, one-quantum matter propagator whose single eigenvalue
   is a genuine sum over both chiral branches (the L9 repair, §7.6 item 3); a revision of the
   canonical ruler that does not cost $G$ a factor of $1.3\times10^{14}$; a retraction of the Crab
   Nebula's electron-energy inference; or a sign-structure error that would weaken (not remove) the
   exclusion from 7.05 to 5.08 decades. None of these is currently in hand.
2. **CL262 (F301, narrowed) carries `falsifier: stated`, with three independent kills**: (a) the
   observational one — already fired by F327, as recorded above; (b) internal/structural — any live
   channel whose defect appears at an order other than its branch structure predicts; (c) algebraic —
   any boost generator outside $\tfrac1{2c^2}\{x_i,\Omega\}+f(\mathbf k)$ that still satisfies
   $[K_i,P_j]=i\delta_{ij}\Omega/c^2$ and closes the algebra on $P=k$, without the defect reducing to
   $\partial_i\Phi$.
3. **CL263 (no universal momentum map) is falsified by exhibiting a single-valued map under which
   both the even photon law and a chiral Weyl branch are simultaneously exactly Minkowski**, or by
   showing the physical fermion channel is *not* on a single chiral branch (which would remove the
   card's premise rather than its algebra — and is exactly what §7.6's repair direction would need to
   supply).
4. **CL011/CL274 (the photon sector) carry `falsifier: stated`**: any measured linear ($n=1$) photon
   dispersion at any scale kills F26/F319 outright, as would any $n=2$ bound tightening past the
   model's own predicted scale ($1.36\times10^{19}$ GeV per CL011, or $1.73\times10^{19}$ GeV per
   F28's own un-reconciled table, Gap G-5) — currently roughly fifteen decades from reach.
5. **CL012 (photon non-birefringence) is falsified by any measured energy-dependent rotation of the
   polarisation plane from a cosmological source with a linear, rather than absent, energy
   dependence** — the exact signature F30 shows must cancel identically if the physical photon is the
   even/paired channel Chapter 8 constructs.
6. **R7.5's sign theorem (F15) is falsified in construction**, not by experiment, if any $m\in(0,1)$
   is found where $\tan(\arcsin m)/\arcsin m\le1$ — an elementary calculus fact ($\tan\theta>\theta$
   on $(0,\pi/2)$) that cannot fail, recorded as a falsifier only for completeness of the ledger.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–6's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $K_i$ | The (minimal) boost generator, $K_i=\tfrac1{2c^2}\{x_i,\Omega\}$, with $x_i=i\partial_{k_i}$ the position operator on the Brillouin-zone torus. | §7.2.2 |
| $\Phi(\mathbf k)$ | The off-shell invariant mass, $\Phi=(\Omega^2-c_\text{lat}^2\lvert\mathbf k\rvert^2)/2c_\text{lat}^2$; the single scalar potential whose gradient is the entire finite-$a$ Poincaré defect. | §7.2.2 |
| $D_i(\mathbf k)$ | The Poincaré defect itself, $D_i=\partial_i\Phi$; zero to all orders on the cubic axes, $O(\lvert k\rvert^3)$ for the even/paired photon, $O(\lvert k\rvert^2)$ on a bare chiral branch. | §7.2.2 |
| $\beta_\text{LV},\gamma_\text{LV},\delta_\text{LV},\varepsilon_\text{LV}(m)$ | The closed-form SR-2 time-dilation Lorentz-violation coefficients, all strictly negative on $(0,1)$; $\beta_\text{LV}=\tfrac12(1-\tan\theta/\theta)$, $\theta=\arcsin m$. | §7.2.3 |
| $\rho(m)$ | $\rho(m)=\tan(\arcsin m)/\arcsin m=1-2\beta_\text{LV}(m)$; the leading isotropic term of $D_i$ on both the 2D-square and BCC lattices. | §7.2.4 |
| $\eta(\hat k)$, $E_\text{LV}$ | The Myers–Pospelov dimension-5 coefficient and energy scale for the excluded single-branch chiral fermion operator; $\eta=-\tfrac2{\sqrt3}\tfrac a{\ell_P}\hat k_x\hat k_y\hat k_z$, $\lvert\eta\rvert_\text{max}=2\sqrt{8\pi}\,3^{1/4}/9$. | §7.2.7 |

---

*New gap logged this chapter: **G-5** (§7.1), also recorded in `docs/monograph/GAPS.md`. No finding,
claim card, module, or test record was created or modified in the writing of this chapter.*
