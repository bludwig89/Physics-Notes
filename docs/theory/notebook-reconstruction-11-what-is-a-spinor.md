# Notebook Reconstruction — Batch 11: "What is a Spinor?" — Direction Without
# Magnitude, Stereographic Projection, the Light Cone, and the General-Radius
# Rederivation (pp. 110–124)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 110–124
(NB-143 – NB-153), the "What is a Spinor?" numbered paper. Continues directly from batch 10
(NB-130 – NB-142, pp.103–109). Per the governing prompt's firewall, this batch does not consult
`findings/`, `docs/claims/`, or any of the other excluded files.

Date-time stamp: 2026-09-22 - (batch 11).

Scripts: `tests/runners/notebook-recon/run_NB-143_144_spinor_as_direction_topology.py`,
`run_NB-145_148_stereographic_projection_half.py`, `run_NB-149_152_lightcone_ST_reflections.py`,
`run_NB-153_general_radius_rederivation.py`.
Results: matching JSON files in `test-results/notebook-recon/`.

---

## NB-143 (pp.110–111) — $\eta=\alpha/\beta$ Invariance and "A Spinor Is a Direction Without a Magnitude"

**Verified**: $\eta=\alpha/\beta$ is trivially invariant under $\Psi\to a\Psi$ (direct symbolic
check). The thesis itself — a spinor is a direction without a magnitude — is a standard, apt
physical picture matching the Bloch-sphere correspondence between a spin-½ state and a point on
$S^2$ via $\boldsymbol\sigma\cdot\hat n$ eigenstates. One nuance worth flagging: the page's
footnote calling the discarded overall scale "only a trivial phase-invariance" is correct for
*this specific purpose* (extracting a direction), but a spinor's overall phase is not always
physically inert in general (e.g. Berry-phase and spin-rotation-by-$4\pi$ effects depend on
tracking it) — a simplification, not an error, for what this section is doing. **Verdict: SOLID.**

## NB-144 (pp.111–112) — Topological Argument: Sphere ≠ Plane

**Verified two ways.** (1) The general fact: a continuous bijection from a compact space ($S^2$)
onto a non-compact Hausdorff space ($\mathbb C$) cannot exist, since the continuous image of a
compact set is compact and $\mathbb C$ is not — standard point-set topology, exactly the reason a
single finite complex number cannot smoothly cover every direction. (2) The concrete instance:
symbolic limit analysis of the stereographic map $\zeta=(x+iy)/(1-z)$ along multiple different
meridian paths approaching the north pole $(0,0,1)$ confirms $|\zeta|\to\infty$ along every path
tried — a genuine, non-removable singularity at exactly one point, nowhere else. **Verdict:
SOLID.**

---

## NB-145 (pp.112–113) — Line/Sphere Intersection: **A Transcription Slip in (18a), Confirmed Not to Propagate**

**Notebook:** parametrizes the line from $(0,0,1)$ through $(\alpha,\beta,0)$ as $x=\tfrac12\alpha
t,\ y=\beta t,\ z=1-t$ (18a–c) — note the explicit $\tfrac12$ on $x$ only, not $y$ — then
substitutes into the radius-$\tfrac12$ sphere equation to get (19)/(20), solving to the boxed
$t=(\alpha^2+\beta^2+1)^{-1}$ (21).

**Verified**: solving the sphere/line intersection using the line **as described in words**
(from $(0,0,1)$ through $(\alpha,\beta,0)$, i.e. $x=\alpha t$, with **no** $\tfrac12$) reproduces
the boxed $t=(\alpha^2+\beta^2+1)^{-1}$ of (21) exactly. Keeping the literal $\tfrac12$ factor
from (18a) instead gives a different, non-matching $t$. **The explicit "$\tfrac12$" in (18a) is
itself the error** — an asymmetric factor on $x$ alone that doesn't belong on either coordinate;
(19)–(21) are internally consistent with each other and with the correctly-stated verbal
description of the line, not with (18a)'s own displayed formula. **Verdict: SOLID-WITH-CORRECTION.**

## NB-146 (p.113) — $x,y,z$ in Terms of $\zeta,\zeta^*$ (24a–c): **A Precise, Three-Way Mixed-Convention Error Found**

**Notebook:** $x=(\zeta+\bar\zeta)/(1+|\zeta|^2)$ (24a), $y=(\zeta-\bar\zeta)/(1+|\zeta|^2)$
(24b), $z=|\zeta|^2/(1+|\zeta|^2)$ (24c).

**Verified, precisely quantified.** Two ground truths were derived independently and compared
against all three formulas: **(A)** the actually-described radius-$\tfrac12$ sphere centered at
$(0,0,\tfrac12)$ (using the corrected line from NB-145), and **(B)** the standard textbook
stereographic-projection formula for a **unit sphere centered at the origin** (independently
re-derived from scratch: $x=2\alpha/(1{+}\alpha^2{+}\beta^2)$, etc. — confirmed to be the genuine
correct formula for that different sphere).

- **(24b)** as literally transcribed is not even real: $\zeta-\bar\zeta=2i\beta$ is purely
  imaginary, so dividing by the real denominator $1+|\zeta|^2$ cannot equal the real coordinate
  $y$ — a defect detectable from the formula alone, with no external reference needed. Restoring
  the obviously-missing factor of $i$ in the denominator makes it real.
- **Once corrected, (24a) and (24b) are each *exactly twice* the true radius-$\tfrac12$-sphere
  $x,y$ — and exactly equal to the standard unit-sphere formula (B) instead.**
- **(24c), in sharp contrast, exactly matches the true radius-$\tfrac12$ sphere $z$** — not the
  unit-sphere $z$, which differs from it.

**Conclusion: (24a–c) is an internally *mixed* set, not a single typo** — $(24a,b)$ use the
standard unit-sphere convention (very plausibly copied from a memorized textbook formula) while
$(24c)$ uses the different, correct-for-this-page radius-$\tfrac12$ convention set up two
paragraphs earlier. **Verdict: INCORRECT (as transcribed) / SOLID-WITH-CORRECTION.**

## NB-147 (p.113) — Inverse Map $\zeta=(x+iy)/(1-z)$: **Confirmed**

**Verified**: substituting the true radius-$\tfrac12$-sphere $x,y,z$ (from NB-145's corrected line)
into $(x+iy)/(1-z)$ reduces exactly to $\zeta=\alpha+i\beta$. This inverse formula is correct for
the sphere actually described on the page, independent of NB-146's mixed-convention issue in the
*forward* formulas — the inverse only needs a ratio, and the specific overall-scale mismatch in
$(24a,b)$ happens not to affect this particular check. **Verdict: SOLID.**

## NB-148 (pp.113–114) — Homogeneous/Projective Form (27a–c): **Internally Consistent — With a Different Sphere Than (24a–c)**

**Notebook:** $\zeta=\xi/\eta$ (26), with $x,y,z$ given as ratios of $\xi,\eta$ and their
conjugates (27a–c), claimed to reduce to (24a–c) at $\eta=1$.

**Verified**: unlike $(24a{-}c)$, the projective triple $(27a{-}c)$ is **internally consistent
with itself** — at $\eta=1$, all three of $x$, $y$ (once the identical missing-$i$ fix from
NB-146 is applied) and $z$ exactly match the **standard unit-sphere** convention (independently
re-derived), none matching the actual radius-$\tfrac12$ sphere. So $(27a{-}c)$ is a
self-consistent, correctly-executed formula — just for a different sphere than the one
geometrically set up on pp.112–113, and it does *not* actually reduce to $(24a{-}c)$ as claimed,
since $(24c)$ uses yet a third, different convention from both. The scale-invariance under
$(\xi,\eta)\to(\lambda\xi,\lambda\eta)$ — the property the whole construction is *for* — is
confirmed exactly regardless, correctly reproducing the spinor ambiguity of (14). **Verdict:
SOLID-WITH-CORRECTION.**

---

## NB-149 (pp.114–115) — The Light Cone and the Photon "Single Point" Argument

**Verified**: the length-contraction/time-dilation formulas are standard and self-consistent. The
underlying **mathematical** conclusion — that null-separated points correspond to "a direction
with zero length" — is sound and matches the genuine structure of Minkowski space (a null vector
satisfies $V\cdot V=0$, and a null ray really is characterized only by direction). One honest
caveat: the specific **physical** argument used to motivate it — invoking "the photon's own frame
of reference" — is not rigorous special relativity, since no valid inertial rest frame exists for
a massless particle (the Lorentz transformation to $v=c$ is singular, not a mere boundary case).
This is a well-known, common pedagogical shortcut, not a novel error, and it doesn't affect the
correctness of the mathematical conclusion it's used to motivate. **Verdict: SOLID** (mathematical
conclusion correct and standard; the physical framing is a common informal heuristic worth
flagging but not scoring as wrong).

## NB-150 (p.115) — Four Light-Cone Connections and Their Negation Relations: **Confirmed**

**Verified**: $p_{21}=-f_{12}$ and $p_{12}=-f_{21}$ both follow immediately and exactly from the
four stated null-vector definitions. **Verdict: SOLID.**

## NB-151 (pp.115–116) — $\mathcal S(\zeta)=\mathcal T(\zeta)=-1/\zeta^*$: **Confirmed**

**Verified**: building $\mathcal S(\zeta)$ from full spatial reflection and $\mathcal T(\zeta)$
from time reversal independently, then using the null-cone condition $x^2+y^2=t^2-z^2$ to
eliminate $y$, both reduce **exactly** to $-1/\zeta^*$ — confirmed by direct symbolic
substitution, not approximation. **Verdict: SOLID.**

## NB-152 (p.116) — Ambiguity in $\mathcal S(\xi),\mathcal S(\eta)$: **Confirmed**

**Verified**: the notebook's own assignment $\mathcal S(\xi)=-\eta^*,\ \mathcal S(\eta)=\xi^*$
exactly reproduces $\mathcal S(\zeta)=-\eta^*/\xi^*$ as claimed, and any common complex rescaling
$(\lambda\mathcal S(\xi),\lambda\mathcal S(\eta))$ leaves that ratio unchanged for any $\lambda$ —
confirming the notebook's own point that only the *ratio* is fixed and the individual component
assignment is genuinely, provably ambiguous. **Verdict: SOLID.**

---

## NB-153 (pp.121–124) — General-Radius Rederivation: **One Genuine Error Found, One Apparent Error Resolved as Intentional, Everything Else Confirmed**

**Notebook:** sphere $x^2+y^2+z^2=r^2$, line from $(0,0,r)$ through $(\alpha,\beta,0)$
parametrized $x=\alpha t,\ y=\beta t,\ z=r(1-t)$; boxed intersection result "$2r/t=r^2+\alpha^2+
\beta^2$" $\Rightarrow t=2r/(r^2+\alpha^2+\beta^2)$; $x,y,z$ in terms of $\eta=\alpha+i\beta$;
inverse $\eta=(x+iy)/(r-z)$, claimed "independent of $r$"; then a separate inverse-projection
subsection (30a–c, 32, 33, 37) and a concluding claim about reading a null quaternion as two
antipodal spinor projections.

**Four findings, precisely separated:**

1. **A genuine dimensional error in the boxed $t$.** Solving the sphere/line intersection
directly gives $t=2r^2/(r^2+\alpha^2+\beta^2)$ — the notebook's own $2r/(\dots)$ is missing a
factor of $r$. This is not just a symbolic mismatch: $t$ must be a dimensionless line parameter,
and $2r/(r^2+\alpha^2+\beta^2)$ has units of inverse length if $\alpha,\beta,r$ carry units of
length, while $2r^2/(\dots)$ is correctly dimensionless. **Verdict component: INCORRECT (as
transcribed) / SOLID-WITH-CORRECTION.**

2. **The $x,y,z$ formulas that follow are exactly correct — using the *corrected* $t$, not the
notebook's own literally-stated one.** Substituting the corrected $t=2r^2/(\dots)$ reproduces all
three of the boxed $x=r^2(\eta+\eta^*)/(r^2+\eta\eta^*)$, $y=-ir^2(\eta-\eta^*)/(r^2+\eta\eta^*)$,
$z=r(\eta\eta^*-r^2)/(r^2+\eta\eta^*)$ exactly — meaning whoever derived these used the right $t$
even though the boxed intersection formula two lines above has the typo. **Verdict component:
SOLID.**

3. **The inverse formula and "independent of $r$" claim resolve to a single, coherent,
non-error picture.** $(x+iy)/(r-z)$ evaluates *exactly* to $\eta/r$, not $\eta$ itself — read as a
literal claim to recover the plane coordinate $\eta=\alpha+i\beta$, this is off by a factor of
$r$. But the very next sentence on the page is precisely the claim that this formula "is
independent of $r$" — and $\eta/r$ (not $\eta$) is exactly the quantity with that property,
confirmed directly: $\eta$ itself scales linearly under an overall rescaling of the whole
configuration $(\alpha,\beta,r)\to\lambda(\alpha,\beta,r)$, while $\eta/r$ does not (both scale
together and cancel). This is exactly the scale-free "direction without magnitude" the entire
section is building toward — read this way, calling $(x+iy)/(r-z)$ "$\eta$" at this specific step
is a labeling looseness for the normalized $\eta/r$, not a dropped factor. **Verdict component:
SOLID**, once read this way.

4. **The inverse-projection subsection (30a–c, 32, 33, 37) is confirmed exactly.** $(30a{-}c)$ are
exactly the same forward projection formula as $x,y,z$ above, relabeled $(\alpha,\beta)\to
(x_0,y_0)$ — confirmed by direct substitution. The quadratic $x_c x_0^2-2r^2x_0+x_cr^2=0$ (32)
follows immediately from $(30a)$ at $y_0=0$. Its two roots
$x_0^\pm=(r/x_c)(r\pm\sqrt{r^2-x_c^2})$ (33) match the direct quadratic solution exactly. The
product identity $x_0^+x_0^-=r^2$ (37) is confirmed by direct multiplication. **Verdict component:
SOLID.**

**Overall verdict: SOLID-WITH-CORRECTION** — one genuine, precisely located dimensional slip in
the boxed intersection result (component 1), with everything built on top of it (components 2–4)
shown to use the *correct* value throughout, plus one apparent discrepancy (component 3) resolved
as the section's own stated point rather than an error.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-143 | SOLID |
| NB-144 | SOLID |
| NB-145 | SOLID-WITH-CORRECTION |
| NB-146 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-147 | SOLID |
| NB-148 | SOLID-WITH-CORRECTION |
| NB-149 | SOLID |
| NB-150 | SOLID |
| NB-151 | SOLID |
| NB-152 | SOLID |
| NB-153 | SOLID-WITH-CORRECTION |

**What closed:** the core conceptual argument of the whole "What is a Spinor?" paper (NB-143,
NB-144) is confirmed sound both as physics (the direction-without-magnitude picture) and as
mathematics (the compactness argument for why one complex number can't cover a sphere). The
$r=\tfrac12$ stereographic-projection derivation (NB-145–148) is found to mix two genuinely
different sphere conventions across its own equations — a precisely quantified, three-way split
between the actually-described radius-$\tfrac12$ sphere and a standard unit-sphere formula
apparently copied in from memory — with the two inverse-direction checks (NB-147, and the general
radius-$r$ case's own inverse in NB-153) both confirmed to correctly recover the *actually*
intended geometric quantity once the right convention is identified. The light-cone/$\mathcal
S,\mathcal T$-reflection material (NB-149–152) checks out completely, with one honest note about
an informal (not rigorous) physical framing that doesn't affect the math. NB-153's general-radius
rederivation has one genuine dimensional slip in its intersection formula, shown not to propagate
into anything built on top of it, plus a superficially-odd-looking inverse formula resolved as
being exactly the point the page itself is making about scale-independence.

**What's still open:** nothing left materially open — every build in this batch reached either a
clean SOLID or a fully closed, precisely quantified correction.

---

## Errata — errors in the notebook (2007)

- **p.112 (NB-145):** the line parametrization (18a) states $x=\tfrac12\alpha t$ (an unexplained,
  asymmetric factor of $\tfrac12$ appearing on $x$ but not $y$); the boxed intersection result
  (19)–(21) is self-consistent only *without* this factor (i.e. with the line as described in
  words, $x=\alpha t$). The $\tfrac12$ does not propagate past this one line.
- **p.113 (NB-146):** the projection formulas (24a–c) mix two different spheres: $(24a)$ and
  $(24b)$ (the latter also independently missing a factor of $i$ needed to be real at all) exactly
  match the standard textbook unit-sphere convention (radius 1, centered at the origin), while
  $(24c)$ matches the different, correct-for-this-page radius-$\tfrac12$ sphere convention set up
  moments earlier. $(27a{-}c)$ is internally self-consistent with the unit-sphere convention
  throughout (once its own copy of the same missing-$i$ issue in the $y$-component is corrected),
  so it does not actually reduce to $(24a{-}c)$ as claimed, since $(24c)$ alone uses a third,
  different convention.
- **p.121 (NB-153):** the boxed intersection result "$2r/t=r^2+\alpha^2+\beta^2$" is missing a
  factor of $r$ — dimensionally, $t$ (a dimensionless line parameter) cannot equal
  $2r/(r^2+\alpha^2+\beta^2)$ (units of inverse length); the correct result is
  $t=2r^2/(r^2+\alpha^2+\beta^2)$. All subsequent formulas on the page (the $x,y,z$ expressions,
  the inverse map, the inverse-projection subsection) are shown to use the *correct* $t$
  throughout, so this slip is isolated to the one boxed line and does not propagate.

## Errata — errors in my framing of these prompts

- An initial check of NB-153's equation (33) compared the two solutions of the quadratic (32) to
  the notebook's stated $x_0^\pm$ using Python's `set()` equality on unevaluated sympy
  expressions, which reported a false mismatch (sympy expressions with the same value but
  different unsimplified forms don't reliably compare equal via set/hash operations). Caught by
  re-checking with pairwise symbolic-difference comparisons instead, which confirmed an exact
  match.
- An initial reading of NB-153's inverse formula ("$\eta=(x+iy)/(r-z)$... independent of $r$")
  treated the factor-of-$r$ discrepancy found by direct substitution as a probable notebook error
  before checking the page's own very next sentence, which is precisely the "independent of $r$"
  claim — recognizing that $\eta/r$ (not $\eta$) is exactly the quantity with that scale-invariance
  property resolved this as the section's own intended point rather than a dropped factor,
  avoiding a false-positive error report.

## Correlation queue additions

None from this batch meet the bar. This section is pure mathematical/geometric construction
(stereographic projection, the light cone, projective coordinates) with no contact point to any
named physics decision beyond the general fact — already covered by the correlation queue's
standing NB-007 entry — that spinor/Weyl-equation machinery of this general kind underlies the
model's own fermion sector. Nothing new and specific enough to add a fresh row.
