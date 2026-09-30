# Notebook Reconstruction — Batch 15 (Contaminated-Session Defer Pass)

**Date:** 2026-09-22 - 00:00
**Scope:** Two page ranges deferred by a prior session that had been
accidentally exposed to changelog-tail hints and so could not remain cold for
these specific items: p.77 (NB-099) and pp.176–182 (NB-180, NB-182, NB-184,
NB-185, NB-186 — the final pages of the notebook).
**Method:** Cold reconstruction per the standing firewall — no access to
`findings/`, `docs/claims/`, `docs/theory/key-decisions.md`,
`docs/theory/supersessions.yaml`, `src/casim/engine/**`, other batch
write-ups, or the reconstruction index. Worked only from the raw transcription
(`references/physics-notes-complete.md`, lines ~1895–1940 and ~3260–3362) plus
standard textbook physics and independent sympy computation.

---

## NB-099 (p.77) — Angular Momentum Conservation With a Mass Term

**Notebook:**

> "However, a mass term in the free Dirac equation apparently violates spin
> conservation too. Yet with free Dirac we understand that there's a bigger
> concept — angular momentum conservation — which holds the conservation
> principle. When the mass term flips spin it creates angular momentum in the
> field, so that $S_{-1/2}\to S_{1/2}$ is compensated with $J_N\to J_{N+1}$.
> Perhaps charge should be understood in a better way too, such that it is
> partly due to intrinsic properties of a particle, and partly not. These
> intrinsic qualities, then, would become $W_\pm$ bosons in a more advanced
> theory."
>
> "**Greiner Rel QM, p. 216, 217** — Shows $J$ commutes w/ $H$ w/ spherical
> potential: $J=L+S=L+\tfrac12\hbar\vec\Sigma$; $[L,\vec\alpha\cdot\vec
> p]=i\hbar\,\vec\alpha\times\vec p$ ($\vec L=\vec r\times\vec p$); $\vec\Sigma
> = \mathrm{diag}(\vec\sigma,\vec\sigma)$, $[S,\vec\alpha\cdot\vec
> p]=\tfrac12\hbar[\vec\Sigma,\vec\alpha\cdot\vec p]=-i\hbar\,\vec\alpha\times
> \vec p = -\tfrac{i}{\hbar}(\vec r\times\nabla)$."

**Verified:** Built explicit 4×4 Dirac matrices ($\alpha_i$, $\beta$,
$\Sigma_i$, Dirac representation) and confirmed $[\Sigma_i,\alpha_j]=2i\,
\epsilon_{ijk}\alpha_k$ and $[\Sigma_i,\beta]=0$ by direct matrix algebra.
Separately, built genuine differential operators ($p_j=-i\hbar\,\partial_j$,
$L_i=\epsilon_{iab}x_a p_b$, $S_i=\tfrac\hbar2\Sigma_i$) acting on a generic
symbolic 4-component spinor field $\psi(x,y,z)$ (four independent `sympy`
`Function`s, no special-casing), and confirmed as genuine operator identities
(all components, for $i=x,y,z$): $[L_i,\vec\alpha\cdot\vec p]=+i\hbar(\vec
\alpha\times\vec p)_i$, $[S_i,\vec\alpha\cdot\vec p]=-i\hbar(\vec\alpha\times
\vec p)_i$, and therefore $[J_i,H]=0$ for $H=\vec\alpha\cdot\vec p+\beta m$,
all $i$. Also checked the notebook's own extra written identity $-i\hbar(\vec
\alpha\times\vec p)\overset{?}{=}-\tfrac i\hbar(\vec r\times\nabla)$ directly
by applying both sides to a generic spinor: they are **not** the same
operator (the left side genuinely mixes the four spinor components through
$\alpha_j$; the right side, with no $\alpha$ factor, is a scalar orbital
operator proportional to the identity matrix and cannot do so).

**Verdict: SOLID.** The cited Greiner mathematics — $[L,\vec\alpha\cdot\vec
p]=i\hbar\,\vec\alpha\times\vec p$, $[S,\vec\alpha\cdot\vec
p]=-i\hbar\,\vec\alpha\times\vec p$, and their consequence that $J=L+S$
(not $L$ alone) commutes with the free/central Dirac Hamiltonian — is
reproduced exactly by two independent methods (explicit matrices; genuine
differential-operator action on a generic spinor). The notebook's own extra
identity equating $-i\hbar(\vec\alpha\times\vec p)$ to $-\tfrac i\hbar(\vec
r\times\nabla)$ is flagged as a likely transcription artifact (see errata
below) but does not affect the verdict, since it plays no role in the actual
$J=L+S$ argument (which correctly uses $[S,\vec\alpha\cdot\vec
p]=-i\hbar\,\vec\alpha\times\vec p$). The surrounding narrative — recasting
the mass term's spin flip as an angular-momentum-conserving exchange with
"the field," and speculating that charge conservation might similarly split
into an intrinsic piece plus a $W_\pm$-boson piece — is explicitly hedged
("Perhaps…") and is a research motivation, not a derivation; it is not
scored as a separate testable sub-claim.

---

## NB-180 (p.176) — Two Coordinate Systems / Rotation Phase

**Notebook:**

> "Consider two separate coordinate systems and their respective
> stereographic representations $(x_s,y_s,z_s)$ versus $(x_s',y_s',z_s')$ and
> $(x_0,y_0)$ vs $(x_0',y_0')$. Rotation about $z$: changes overall phase of
> $(x_0,y_0)$, sending $x_0+iy_0\to e^{i\theta}(x_0+iy_0)$. — $Z$ determined
> by direction of motion of photon; $R$ of sphere determines relative
> magnitude; What is overall phase?"

**Verified:** The page gives the claim but not the underlying stereographic
projection formula it is a fact about (that formula appears earlier in the
notebook, outside this session's assigned range), so it was reconstructed
independently: the standard unit-sphere stereographic map $x=(\eta+\eta^*)/
(1+\eta\eta^*)$, $y=-i(\eta-\eta^*)/(1+\eta\eta^*)$, $z=(\eta\eta^*-1)/
(\eta\eta^*+1)$ for $\eta=x_0+iy_0$. Substituted $\eta\to e^{i\theta}\eta$
symbolically and confirmed, for symbolic real $\theta,x_0,y_0$, that $(x,y,z)$
transforms by an exact rotation by $\theta$ about $z$ (and $z$ is invariant).

**Verdict: SOLID.** This is the standard fact that a rotation about the
sphere's polar axis acts as a pure phase (Möbius) transformation on the
stereographic-plane coordinate; the substitution exactly reproduces a $z$-axis
rotation of $(x,y,z)$, directly answering the page's own question. The "3-item
outline for spinor paper" on the same page (null vectors as tensor products /
non-null decomposition / spinor field equations of motion) is a bare
table-of-contents entry with no math — **NOT-TESTABLE** (and is executed by
the very builds below).

---

## NB-182 (pp.176–177) — Construction of Null Vectors as Tensor Products

**Notebook:**

> "$(\alpha^*\ \beta^*)\otimes\binom{\alpha}{\beta}=\begin{pmatrix}\alpha
> \alpha^*&\beta^*\alpha\\\alpha^*\beta&\beta^*\beta\end{pmatrix}=
> \begin{pmatrix}V_0-V_z&-V_x+iV_y\\-V_x-iV_y&V_0+V_z\end{pmatrix}$. So $\det
> Q=\alpha\alpha^*\beta\beta^*-\alpha^*\beta\alpha\beta^*=0$ ✓. $\alpha\alpha^*
> =V_0-V_z$, $\beta\beta^*=V_0+V_z$, $\alpha^*\beta=-V_x-iV_y$. Write:
> $\alpha=\sqrt{V_0-V_z}e^{i\theta}$, $\beta=\sqrt{V_0+V_z}e^{i\phi}$;
> $\alpha^*\beta=\sqrt{(V_0-V_z)(V_0+V_z)}e^{i(\phi-\theta)}=\sqrt{V_0^2-V_z^2}
> e^{i(\phi-\theta)}=\sqrt{V_x^2+V_y^2}e^{i(\phi-\theta)}$; **Ambiguity of
> $e^{i\theta}$ key.** $\frac{V_x+iV_y}{\sqrt{V_x^2+V_y^2}}=-e^{i(\phi-\theta)}$."

**Verified:** Confirmed $Q=vv^\dagger$, $v=(\alpha,\beta)^T$, reproduces
exactly the four written entries; confirmed $\det Q=0$ identically for
generic complex $\alpha,\beta$ (any rank-1 outer product is singular).
Substituted the polar forms with $P\equiv V_0-V_z$, $Q'\equiv V_0+V_z$ treated
as positive symbols (required for the real square roots used, i.e. $V$
future-pointing/timelike-or-null) and confirmed $\alpha\alpha^*=P$,
$\beta\beta^*=Q'$, $\alpha^*\beta=\sqrt{PQ'}e^{i(\phi-\theta)}$ exactly.
Confirmed $V_0^2-V_z^2=V_x^2+V_y^2$ follows algebraically from $V$ being null
($V_0^2=V_x^2+V_y^2+V_z^2$, given/implicit in this "null vector" section).
Confirmed the final boxed phase relation is an exact, direct algebraic
rearrangement of $\alpha^*\beta=-V_x-iV_y$ together with the above.

**Verdict: SOLID.** Every step checks out exactly once $V$'s implicit
nullness and future-pointing character are made explicit (used but not
restated on this page). The written "$\otimes$" ordering is a loose,
non-standard use of "tensor product" for an outer product (common in hand
notes) but reproduces the correct entries regardless.

---

## NB-184 (p.178) — Null Matrix Factorization

**Notebook:**

> "A matrix $M=\begin{pmatrix}a&b\\c&d\end{pmatrix}$ with $\det(M)=ad-bc=0$:
> $ad=bc\Rightarrow \frac ab=\frac cd$ and $\frac ac=\frac bd$. So if $b=\alpha
> a$ then $c=\alpha d$; if $c=\beta a$ then $d=\beta b$; so:
> $M=\begin{pmatrix}a&\alpha a\\\beta a&\alpha\beta a\end{pmatrix}=a(1\ \alpha)
> \otimes\binom1\beta$, $\alpha=b/a$."

**Verified:** Symbolically confirmed the final boxed factorization
$M=a\cdot(1,\beta)^T\otimes(1,\alpha)$ with $\alpha=b/a,\beta=c/a$ holds
exactly for generic $a,b,c,d$ subject only to $ad=bc$ (a standard fact: every
rank-≤1 2×2 matrix is an outer product of two vectors). Separately tested the
notebook's own *intermediate* claim "if $b=\alpha a$ then $c=\alpha d$" by
eliminating $d$ via the constraint: the difference $c-\alpha d$ reduces to
$-c+b^2c/a^2$, which is **not** identically zero. Confirmed with a concrete
counterexample $a{=}1,b{=}2,c{=}3\Rightarrow d{=}6$ (satisfies $ad=bc$):
$\alpha=2$, $\alpha d=12\ne c=3$.

**Verdict: SOLID-WITH-CORRECTION.** The final boxed result is exactly
correct. The intermediate line "if $b=\alpha a$ then $c=\alpha d$" is a
genuine algebra slip — the correct intermediate relation is $d=\alpha c$ (not
$c=\alpha d$), consistent with the final $d=\alpha\beta a$ once $\beta=c/a$ is
also used. The slip does not propagate into the correct final result.

---

## NB-185 (pp.178–179) — Timelike Decomposition Into Two Null Vectors

**Notebook:**

> "$\tfrac12(V_0^2-|\vec V|^2)^{1/2}=a_0(V_0-\hat a\cdot\vec V)$ … Timelike:
> $a_\mu=(a_0,a_0\hat a)$ is a null vector. $V_\mu=a_\mu+b_\mu=a_\mu+(V_\mu-
> a_\mu)$. For both on the light cone: $a^\mu a_\mu=0$,
> $(V_\mu-a_\mu)(V^\mu-a^\mu)=0$ … $v^2\equiv V_\mu V^\mu=2V_\mu a^\mu=2a_0V_0-
> 2a_0(\hat a\cdot\vec V)$, which can be solved for $a_0$: **$a_\mu=
> \frac1{2V_0}(V_0^2-|\vec V|^2+2\hat a\cdot\vec V)(1,\hat a)$**."

**Verified:** Built $a_\mu=(a_0,a_0\hat a_x,a_0\hat a_y,a_0\hat a_z)$ and
$b_\mu=V_\mu-a_\mu$ from scratch with the mostly-plus dot product and
confirmed the identity $b\cdot b=V\cdot V-2V\cdot a+a\cdot a$ and $V\cdot
a=a_0(V_0-\hat a\cdot\vec V)$, hence the master relation $V\cdot V=2V\cdot a$
given both null. Then tested two readings of "solved for $a_0$": **(A)**
$\hat a$ a genuinely independent, normalized unit vector — `sympy.solve()`
gives the *ratio* $a_0=(V_0^2-|\vec V|^2)/(2(V_0-\hat a\cdot\vec V))$, which
does **not** match the notebook's additive boxed form (numeric
counterexample $V_0{=}5,|\vec V|^2{=}9,\hat a\cdot\vec V{=}1$: ratio gives
$2$, boxed gives $9/5$); **(B)** $(a_x,a_y,a_z)$ as the raw (non-unit) spatial
components of the null vector itself (exactly how the very next section uses
them, "$\hat a=(a_x,a_y,a_z)/\sqrt{a_x^2+a_y^2+a_z^2}$") — here the same
master relation gives the boxed additive form **exactly**.

**Verdict: SOLID-WITH-CORRECTION.** The geometry (splitting a timelike vector
into two null vectors) and the master relation $V\cdot V=2V\cdot a$ are
standard and confirmed exactly. The boxed "solved for $a_0$" formula is
mathematically wrong if $\hat a\cdot V$ means a true unit-vector dot product,
but exactly correct if the same symbol is read as the raw vector's dot
product with $V$ — which is how the notebook itself uses it one section
later. This is a **notational** overloading of the hat symbol, not a physics
error; correct statement: $a_0=(V_0^2-|\vec V|^2+2\,\vec a\cdot\vec V)/(2V_0)$
using the raw vector, with the true unit-direction closed form instead being
the ratio above.

---

## NB-186 (pp.179–182) — Final Null Component Geometry

**Notebook:**

> "$a_0=b+\hat a\cdot\vec u$ … If $\vec V\parallel\hat z$: $a_0(V_0-a_zV_z)=
> \tfrac12(V_0^2-V_z^2)$; $\sqrt{a_x^2+a_y^2+a_z^2}=a_0=\tfrac14\frac{V_0^2-
> V_z^2}{(V_0-a_zV_z)^2}$; $a_x^2+a_y^2+(a_z-\tfrac12V_z)^2=\tfrac14\alpha$,
> $\alpha=1-V_z^2/V_0^2$ … cylindrical: $\rho_s=\dfrac{2r\rho_0}{r^2-\rho^2}$,
> $\theta_s=\theta_0$."

**Verified:** (i) $a_0=b+\hat a\cdot\vec u$ is a trivial, confirmed
algebraic regrouping of NB-185's boxed formula. (ii) Re-derived the $V\parallel
z$ master relation from scratch (from $a\cdot a=0$, $b\cdot b=0$, without
reference to NB-185's boxed line): got exactly $V_0a_0-V_za_z=\tfrac12(V_0^2-
V_z^2)$, matching the notebook's line "$a_0(V_0-\hat a_zV_z)=\tfrac12(V_0^2-
V_z^2)$" exactly once $\hat a_z=a_z/a_0$. (iii) Dividing that relation through
by $(V_0-\hat a_zV_z)$ gives $a_0=\tfrac12(V_0^2-V_z^2)/(V_0-\hat a_zV_z)$ — a
**first**-power denominator, coefficient $\tfrac12$ — which does **not** match
the notebook's next line ($\tfrac14(\cdot)/(\cdot)^2$); confirmed by direct
symbolic division and a numeric example ($V_0{=}5,V_z{=}3,a_z{=}0.5$: notebook
value $361/1600$, correct value $19/10$, matching the true $a_0$). (iv)
Eliminated $a_0$ between the (correct) master relation and the definitional
$a_0^2=a_x^2+a_y^2+a_z^2$ directly (no dependence on the flawed line iii) to
get the true $(a_x,a_y,a_z)$ locus, and compared it to the notebook's claimed
sphere: they do **not** match (numeric check at $V_0{=}5,V_z{=}3,a_z{=}1$:
claimed sphere requires $a_x^2+a_y^2+(a_z-\tfrac32)^2=0.16$, but the true
locus gives $4.09$). The claimed equation is also dimensionally inconsistent
by itself (LHS carries units of length², RHS $\alpha/4$ is dimensionless).
Derived and confirmed the correct locus is an **ellipsoid of revolution**
about $z$: $a_x^2+a_y^2+\alpha(a_z-\tfrac12V_z)^2=\tfrac14V_0^2\alpha$
(equatorial radius $\tfrac12V_0\sqrt\alpha$, polar semi-axis $\tfrac12V_0$;
reduces to the notebook's claimed sphere exactly when $V_z=0$). (v) Checked
the closing cylindrical formula against the standard stereographic
tangent-half-angle double-angle identity ($\rho_0=r\tan(\phi/2)\iff\rho_s=
r\tan\phi$): the notebook's literal $\rho_s=2r\rho_0/(r^2-\rho_0^2)$ reduces
exactly to $\tan\phi$ (dimensionless — and indeed dimensionally impossible
for a radius, since $2r\rho_0$ and $r^2-\rho_0^2$ both carry units of
length²), one factor of $r$ short of the correct identity; the corrected
$\rho_s=2r^2\rho_0/(r^2-\rho_0^2)$ reproduces $r\tan\phi$ exactly.

**Verdict: SOLID-WITH-CORRECTION.** The core geometric machinery (parts i,
ii) is exactly right. Three further lines each contain a genuine, independent
slip — a squared-instead-of-linear denominator (iii), a claimed sphere that
is actually an ellipsoid and is dimensionally short a $V_0^2$ (iv), and a
cylindrical closing formula dimensionally short one factor of $r$ (v) — all
of the same "dropped/duplicated length-dimension factor" character, which is
unsurprising given these are the notebook's very last, most hastily-written
lines (the transcription ends "(End of notebook)" immediately after).

---

## Batch Summary

| Build | Page(s) | Verdict |
|---|---|---|
| NB-099 | 77 | SOLID |
| NB-180 | 176 | SOLID |
| NB-182 | 176–177 | SOLID |
| NB-184 | 178 | SOLID-WITH-CORRECTION |
| NB-185 | 178–179 | SOLID-WITH-CORRECTION |
| NB-186 | 179–182 | SOLID-WITH-CORRECTION |

(The "outline for spinor paper" 3-item to-do list on p.176 and the bare
bullet questions accompanying NB-180 were folded into NB-180's write-up as
NOT-TESTABLE context rather than scored as separate builds, since they carry
no independent math and the to-do items are executed by NB-182/184/185/186
themselves.)

---

## Errata — errors in the notebook (2007)

1. **p.77, Greiner citation line:** "$-i\hbar(\vec\alpha\times\vec p)=
   -\tfrac i\hbar(\vec r\times\nabla)$" equates a spin-matrix-valued operator
   (mixes spinor components via $\alpha_j$) to a scalar orbital operator
   (proportional to the identity in spinor space) — these cannot be the same
   operator, confirmed by applying both to a generic spinor. Likely a
   transcription artifact conflating the correct $[S,\vec\alpha\cdot\vec
   p]=-i\hbar\,\vec\alpha\times\vec p$ with the unrelated fact that
   $L_i=-i\hbar(\vec r\times\nabla)_i$. Does not affect the surrounding
   $J=L+S$ argument, which uses the correct identity.
2. **p.178, NB-184 intermediate step:** "if $b=\alpha a$ then $c=\alpha d$"
   should read $d=\alpha c$ (or equivalently be derived from $\beta=c/a$
   directly); confirmed false in general, with counterexample. The final
   boxed factorization is unaffected and correct.
3. **p.178–179, NB-185 boxed $a_0$ formula:** notationally overloads
   "$\hat a\cdot V$" — correct as written only if read as the raw vector
   $\vec a\cdot\vec V$ (as the very next section does), not literally
   $(\text{unit }\hat a)\cdot\vec V$; the true unit-vector closed form is the
   ratio $a_0=(V_0^2-|\vec V|^2)/(2(V_0-\hat a\cdot\vec V))$.
4. **p.179–182, NB-186 line 3351:** "$a_0=\tfrac14(V_0^2-V_z^2)/(V_0-\hat
   a_zV_z)^2$" should be the first-power form $a_0=\tfrac12(V_0^2-V_z^2)/
   (V_0-\hat a_zV_z)$; confirmed by direct division and numeric check.
5. **p.179–182, NB-186 "sphere" claim:** "$a_x^2+a_y^2+(a_z-\tfrac12V_z)^2=
   \tfrac14\alpha$" is both dimensionally inconsistent (missing an overall
   $V_0^2$ on the right) and geometrically wrong in general (the true locus
   is an ellipsoid, $a_x^2+a_y^2+\alpha(a_z-\tfrac12V_z)^2=\tfrac14V_0^2
   \alpha$, degenerating to the stated sphere only when $V_z=0$).
6. **p.182, NB-186 closing cylindrical formula:** "$\rho_s=2r\rho_0/
   (r^2-\rho_0^2)$" is dimensionally inconsistent (dimensionless, but $\rho_s$
   must carry units of length) and is missing one factor of $r$; corrected:
   $\rho_s=2r^2\rho_0/(r^2-\rho_0^2)$, which is then exactly the standard
   tangent-double-angle stereographic radius identity.
7. **p.179 line 3319 (minor, cosmetic):** "$\tfrac12(V_0^2-|\vec V|^2)^{1/2}$"
   carries a literal square-root exponent that is inconsistent with the
   (correct, no-square-root) restatement three lines later; almost certainly
   an OCR/transcription artifact reading a coefficient $\tfrac12$ as an
   exponent $1/2$.

## Errata — errors in my framing of these prompts

1. My first attempt at NB-180's rotation check reported a false mismatch
   (`x_matches_rotation`/`y_matches_rotation` = False) purely because `sympy`
   does not automatically rewrite `exp(I*theta)` into `cos`/`sin` before
   `simplify()`/`expand_trig()` are applied — the underlying algebra was
   correct throughout. Fixed by explicitly calling `.rewrite(sp.cos)` before
   simplifying; re-ran and confirmed an exact match. Logged here since the
   first, uncorrected run would have produced a false NEEDS-WORK verdict on a
   build that is actually SOLID.
2. Similarly for NB-182: declaring `V0, Vz` as plain `real=True` symbols left
   `sqrt(V0-Vz)*conjugate(sqrt(V0-Vz))` unsimplified (sympy cannot assume the
   sign of a generic real symbol), producing spurious `False` results for
   steps that are true given the section's own implicit positivity
   requirement ($V$ future-pointing/null, so $V_0\pm V_z>0$). Fixed by
   reparametrizing with genuinely `positive=True` symbols $P=V_0-V_z$,
   $Q'=V_0+V_z$ for that specific check; the underlying claim was correct all
   along.
3. My first pass at NB-186's sphere/ellipsoid check made a bookkeeping error
   feeding an already-derived (and itself possibly-erroneous) intermediate
   formula back into the locus derivation rather than re-deriving the locus
   from the two original null conditions directly. Caught by a from-scratch
   symbolic re-derivation (eliminating $a_0$ between $a\cdot a=0$ and
   $b\cdot b=0$ with no reference to any of the notebook's own intermediate
   lines) plus an explicit numeric spot-check, which is what produced the
   ellipsoid-not-sphere finding reported above with confidence.
4. I initially assumed (without checking) that the cylindrical formula's
   "corrected" form would be $\rho_s=r\tan\phi$ matching the literal formula
   as transcribed; a first symbolic check showed a clean, non-trivial
   residual ($(1-r)\tan\phi$) rather than a messy non-identity, which was the
   tell that a clean one-factor-of-$r$ correction (not a deeper error) was
   the right fix — confirmed by testing $\rho_s=2r^2\rho_0/(r^2-\rho_0^2)$
   directly, and cross-checked independently via dimensional analysis alone
   (the literal formula is provably dimensionless, so it cannot equal a
   radius on dimensional grounds regardless of the trig algebra).
5. I did not have access to this notebook's own earlier pages (outside the
   assigned line range) for the general-radius stereographic projection
   formula referenced implicitly by NB-180's "two coordinate systems"
   framing, or for the $\rho_0=r\tan(\phi/2)$-type parametrization assumed in
   verifying NB-186's cylindrical formula. Both were reconstructed
   independently from standard stereographic-projection facts rather than
   read from the notebook; flagged explicitly in each build's write-up.
