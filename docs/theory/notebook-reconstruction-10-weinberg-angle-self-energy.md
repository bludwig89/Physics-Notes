# Notebook Reconstruction — Batch 10: sin²θ_W Numerology, EM/Yukawa
# Self-Energy, Classical Electron Radius, Ellipse Foci, W-S Vector Bosons
# (pp. 103–109)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 103–109
(NB-130 – NB-142). Continues directly from batch 09 (NB-120 – NB-129, pp.92–101). Per the
governing prompt's firewall, this batch does not consult `findings/`, `docs/claims/`, or any of
the other excluded files. All physics-constant cross-checks use independently-sourced CODATA-like
values, never numbers copied from the notebook's own arithmetic.

Date-time stamp: 2026-09-22 - (batch 10).

Scripts: `tests/runners/notebook-recon/run_NB-130_134_sin2thetaw_numerology.py`,
`run_NB-135_137_em_yukawa_self_energy.py`, `run_NB-138_140_newton_electron_radius_ellipse.py`,
`run_NB-141_142_ws_vector_bosons.py`.
Results: matching JSON files in `test-results/notebook-recon/`.

---

## NB-130 (p.103) — Neutral-Charge Operator at the Experimental $\sin^2\theta_W$: **Confirmed**

**Notebook:** $Q'=t_3\cot\theta_W-t_0\tan\theta_W$ evaluated numerically at
$\sin^2\theta_W=0.232$, giving $Q'=\mathrm{diag}(2.37,-1.27)$.

**Verified** (`run_NB-130_134_sin2thetaw_numerology.py`): recomputing $\sin\theta_W,\cos\theta_W,
\cot\theta_W,\tan\theta_W$ from $\sin^2\theta_W=0.232$ alone reproduces every intermediate number
and the final diagonal matrix to the page's own stated precision. **Verdict: SOLID.**

## NB-131 (p.104) — Hypothetical $\sin\theta_W=\tfrac12$: **Confirmed**

**Verified**: $\cos\theta_W=\sqrt3/2$, $\cot\theta_W=\sqrt3$, $\tan\theta_W=1/\sqrt3$ all follow
exactly from $\sin\theta_W=\tfrac12$. **Verdict: SOLID.**

## NB-132 (p.104) — $\tau_\pm$, $V_\pm$, and the Coupling-Normalization Identity: **Confirmed**

**Notebook:** $\tau_\pm=\tfrac1{\sqrt2}(\tau_1\pm i\tau_2)$, $V_\pm=\tfrac1{\sqrt2}(W_1\pm iW_2)$,
and the identity $gW_1\tau_1+gW_2\tau_2=g(W_-\tau_++W_+\tau_-)$, leading to a coupling scaling
$\sim\sqrt2\,g\sim(\sqrt2/\sin\theta_W)e$.

**Verified**: $\tau_\pm$ matches exactly; the raising/lowering identity holds exactly (direct
matrix computation, no approximation); the modulus identity $|W_+|^2+|W_-|^2=|W_1|^2+|W_2|^2$
holds exactly for real $W_1,W_2$; the final coupling-scaling algebra follows immediately from
$g=e/\sin\theta_W$. **Verdict: SOLID.**

## NB-133 (p.104) — Hypothetical "Coupling to $W^\pm=3e$" $\Rightarrow\sin^2\theta_W=2/9$: **Confirmed**

**Verified**: solving $\sqrt2/\sin\theta_W=3$ gives $\sin\theta_W=\sqrt2/3$ exactly, and
$\sin^2\theta_W=2/9=0.2\overline2$ exactly. **Verdict: SOLID.** (This is presented in the notebook
as an idle "is there any significance to this?" numerology exercise, not a derived prediction —
scored purely on whether the stated algebra is correct, which it is.)

## NB-134 (p.104) — $Q_z$ at $\sin^2\theta_W=2/9$: **Two Errors Found; Author's Self-Flagged Failure Confirmed Genuine**

**Notebook:** states $\tan\theta_W=\sqrt{1/7}\approx0.535$, $\cot\theta_W=\sqrt{7/2}\approx1.871$,
$Q_z=\mathrm{diag}(2\sqrt7/3,\,1/\sqrt3)\approx\mathrm{diag}(2.37,1.33)$, then a separate "other
algebra" side-check (treating $\cot\theta+\tan\theta=7/3$, $\cot\theta-\tan\theta=4/3$ as exact,
solving $\cot\theta=11/6$) that ends in the author's own hand-marked **✗**.

**Verified, two independent errors found:**

1. **The printed radical for $\tan\theta_W$ doesn't match its own decimal.** $\sqrt{1/7}=0.378$,
not $0.535$ — the correct closed form is $\sqrt{2/7}=0.5345$, which matches the accompanying
decimal exactly. The "$1/7$" should read "$2/7$"; $\cot\theta_W=\sqrt{7/2}$ is correct as written.

2. **The boxed $Q_z$ decimal $2.37$ is not the value at $\sin^2\theta_W=2/9$ — it is NB-130's
experimental value, apparently carried over.** The true value of $\cot\theta_W+\tan\theta_W$ at
$\sin^2\theta_W=2/9$ is $\sqrt{7/2}+\sqrt{2/7}=\tfrac{9\sqrt{14}}{14}=2.4054$, not $2.37$ — and
$2.37$ is *exactly* NB-130's experimental $Q'_{11}$ value from the previous page. The stated
symbolic form $2\sqrt7/3=1.764$ doesn't match either number. The other entry, $\cot\theta_W-
\tan\theta_W$, has the correct decimal ($1.3363\approx1.33$) but its stated symbolic form
$1/\sqrt3=0.577$ doesn't match that decimal at all.

3. **The author's own "other algebra" self-consistency check is a real, confirmed catch, not
overcaution.** Treating the (already slightly-off) rounded decimals as exact fractions
$\cot\theta+\tan\theta=7/3$ and $\cot\theta-\tan\theta=4/3$ gives $\cot\theta=11/6$ by averaging —
but then $11/6+6/11=157/66=2.379\ne7/3=2.333$, confirmed exactly by direct fraction arithmetic.
The root cause is now precisely identified: $7/3$ and $4/3$ are only rough two-decimal roundings
of the true $2.405$ and $1.336$ (the first already corrupted by the copied-over $2.37$), so no
single exact $\cot\theta_W$ can satisfy both simultaneously — exactly the inconsistency the
author's own arithmetic surfaced.

**Verdict: NEEDS-WORK** — self-flagged error confirmed genuine, with both root causes (a
symbolic-radical transcription slip, and an apparently-copied numeric entry) precisely located.

---

## NB-135 (p.105) — Classical EM Self-Energy: **Confirmed**

**Verified**: $\int_{r_0}^\infty E^2\,dV=4\pi e^2/r_0$ for $E=e/r^2$ (direct symbolic
integration), and dividing by the standard $8\pi$ field-energy prefactor gives exactly
$\mathcal E=e^2/(2r_0)$. **Verdict: SOLID.**

## NB-136 (p.105) — Yukawa Self-Energy Integral: **The Log+Series Identity Confirmed Genuine**

**Notebook:** integrates $\int_{r_0}^\infty e^{-2\alpha r}/r^2\,dr$ by parts, then expresses the
remaining $\int e^{-2\alpha r}/r\,dr$ via the identity
$\int\frac{e^{-x}}{x}dx=\ln x+\sum_{n=1}^\infty\frac{(-x)^n}{n\cdot n!}$, calling the whole result
"quite ugly... should probably be done numerically."

**Verified**: the integration-by-parts step matches sympy's own closed-form (Ei-based)
antiderivative structure exactly; the log+series identity for $\int e^{-x}/x\,dx$ is confirmed
both order-by-order (symbolic series expansion) and by direct numerical differentiation of a
60-term truncation against $e^{-x}/x$ at a representative point ($x=1.7$, agreement to
$10^{-4}$). This is a genuine, standard identity (the series definition of the exponential
integral $\mathrm{Ei}$), correctly invoked. **Verdict: SOLID** — and the author's own assessment
that this doesn't reduce to anything cleaner is fair; no simpler closed form exists.

## NB-137 (p.105) — Ratio Table and Physical-Constant Bookkeeping: **Partially Confirmed, Partially Underspecified**

**Notebook:** a numeric table $I(n)$ vs. $n$ (four rows, spanning $0.1493$ down to
$1.48\times10^{-5}$, annotated with $m_e=511\,\mathrm{keV}$ at $n=1$ and $m_\nu=5\,\mathrm{eV}$
at $n=2$), plus $M_W=80\,\mathrm{GeV}=1.43\times10^{-25}\,\mathrm{kg}$,
$h=6.626\times10^{-34}\,\mathrm{J\cdot s}$, and $k=\hbar c/(m_ec^2)=1.39$.

**Verified, honestly split:**
- $M_W=80\,\mathrm{GeV}\to1.4261\times10^{-25}\,\mathrm{kg}$ (independent CODATA conversion)
matches the stated $1.43\times10^{-25}\,\mathrm{kg}$ to within rounding.
- $h=6.62607\times10^{-34}\,\mathrm{J\cdot s}$ (CODATA) matches the stated value exactly to the
precision given.
- **The $I(n)$ table's precise defining formula could not be reconstructed from the page's own
notation.** A natural dimensionless reading (treating $n$ as the lower integration limit of the
already-derived Yukawa integral in units where $u=\alpha r$) reproduces only the $n=1$ row to
order of magnitude and diverges badly by $n=3,7$; more tellingly, the annotation pairs $n=1$ with
$m_e=511\,\mathrm{keV}$ and $n=2$ with $m_\nu=5\,\mathrm{eV}$ — five orders of magnitude apart in
a single index step — which is not the behavior of one smoothly-varying integration-limit formula
at all. This table most likely indexes distinct physical mass scales through $r_0$ or $\alpha$ in
a way the surviving transcription doesn't preserve enough context to pin down. Rather than force
a fit, this is reported honestly as **underspecified**.
- **The specific value $k=\hbar c/(m_ec^2)=1.39$ could not be matched to the reduced Compton
wavelength of the electron** ($\hbar/(m_ec)=386\,\mathrm{fm}=3.86\times10^{-13}\,\mathrm{m}$)
under any unit choice tried (m, fm, pm). Likely a context-dependent ratio against another length
scale introduced earlier that the transcription doesn't carry forward.

**Verdict: NEEDS-WORK** — the two constants that could be pinned down (M_W conversion, $h$) check
out; the table and the $k=1.39$ figure are flagged as insufficiently specified by the page as
transcribed, not as wrong.

---

## NB-138 (p.106) — Linear Interpolation / Newton's Method: **Confirmed (Background Math)**

Standard algebraic rearrangements of the secant/Newton update formula, all confirmed
self-consistent by direct symbolic solve. **Verdict: SOLID** — a generic math aside, not a
physics claim.

## NB-139 (p.106) — Classical Electron Radius: **Confirmed, With the Factor-of-2 Convention Identified**

**Notebook:** $r_0=e^2/(2m_ec^2)\approx1.43\times10^{-15}\,\mathrm m$.

**Verified**: the standard CODATA classical electron radius is $r_e=2.8179\times10^{-15}\,
\mathrm m$, defined via $\mathcal E=e^2/r_e$ (no factor of 2). This page's convention instead sets
$\mathcal E=e^2/(2r_0)=m_ec^2$ (the same field-energy convention used consistently since NB-135),
which by definition gives exactly $r_0=r_e/2=1.409\times10^{-15}\,\mathrm m$ — matching the
notebook's stated $1.43\times10^{-15}\,\mathrm m$ to within rounding. **This is not an error**:
both conventions for "the electron's classical radius" appear in the literature (the ambiguity is
explicitly discussed in, e.g., Jackson's *Classical Electrodynamics*), and the arithmetic is
exactly consistent once the convention actually in use (matching NB-135's own field-energy
prefactor) is identified. **Verdict: SOLID.**

## NB-140 (p.107) — Ellipse Foci: **A Transcription Slip Found; the Derivation Itself Is Exactly Correct**

**Notebook:** states the ellipse as $\frac{x^2}{b^2}+\frac{y^2}{b^2}=1$, derives $a^2+1=b^2$ from
$d_++d_-=\text{const}$, and gives the numeric example $b=1.2\Rightarrow a\approx0.67$.

**Reconstruction.** The equation *exactly as transcribed* — both denominators equal $b^2$ —
literally describes a **circle** of radius $b$, not an ellipse with distinct foci; this is
inconsistent with everything that follows. The stated intercepts ($x=\pm b$, $y=\pm1$) are only
consistent with the corrected equation $\frac{x^2}{b^2}+y^2=1$ (y-denominator $1$, not $b^2$) —
confirmed directly (both intercept sets recovered exactly by solving the corrected equation).
Given that correction, the standard analytic-geometry foci formula $a=\sqrt{b^2-1}$ satisfies
$a^2+1=b^2$ exactly, and re-deriving it independently via the page's own method
($d_++d_-=\text{const}$, matched at the two named intercepts) reproduces the identical formula.
The $b=1.2$ example: true value $a=\sqrt{11}/5=0.6633$; correctly rounded to two decimals this is
$0.66$, not the notebook's stated $0.67$ — a trivial $0.01$ rounding slip.

**Verdict: SOLID-WITH-CORRECTION.** The top-line equation as transcribed is wrong (describes a
circle), almost certainly a duplicated-"$b^2$" transcription slip rather than the 2007 author's
own conceptual error, since the entire rest of the page is self-consistent with, and only with,
the corrected equation. The actual derivation, method, and final formula are all exactly right;
the numeric example carries a negligible rounding slip.

---

## NB-141 (pp.108–109) — Promoting the Scalar $W^\pm$ Contact Term to a Vector Boson: **A Silently-Abandoned Reasoning Step Found, but the Final Construction Is Standard**

**Notebook:** proposes "presumably... $W_\pm=\partial_\mu W_\pm^\mu$" to promote the earlier
scalar contact interaction to a vector-mediated one, then immediately writes down
$\mathcal L_{WS}=g_0(\sigma_\mu\otimes\tau_0)W_\mu^{\,+}\bar\nu_Le_L+g_0(\sigma_\mu\otimes\tau)
W_\mu^{\,-}\bar e_L\nu_L$.

**Analysis.** These two ideas are **not the same construction**. Literally substituting
$W_\pm=\partial_\mu W_\pm^\mu$ (a Lorentz scalar built from a four-divergence) into the old scalar
contact term would produce a term with an extra derivative and no free vector index to contract
against a fermion current. What the page actually writes next is instead the standard
**minimal-coupling / Yang–Mills pattern**: a vector current $\bar\nu_L\sigma_\mu e_L$ (built from
the fermion bilinear itself, using $\sigma_\mu$ as the Weyl "gamma matrices") dotted directly into
the gauge field $W_\mu$, with no derivative on $W$ anywhere — this is, in fact, structurally
identical to how the real Standard Model's charged-current Lagrangian is built. The author's own
parenthetical guess is a genuine dead end, silently abandoned one line later in favor of the
construction that actually works, without the page remarking on the inconsistency.

**Verdict: NEEDS-WORK.** The stated intermediate reasoning doesn't connect to what follows; the
final Lagrangian the author lands on is nonetheless structurally sound and standard.

## NB-142 (p.109) — Weinberg Angle "Kludge" and the $W,B$-Mass Question: **Two Fair, Standard Observations**

Both of the page's conceptual points check out as textbook-accurate: (1) the Weinberg angle is
indeed precisely the free rotation parameter that accommodates $g'\ne g$ between an otherwise
independent $U(1)$ and $SU(2)$ coupling — "kludge" is an editorial framing of a genuine, still-open
question about the Standard Model, not a technical inaccuracy; (2) an unbroken gauge boson of a
self-coupled theory is required by the gauge symmetry to be massless, so asking why $W,B$ should be
massive when they "specifically couple only to themselves" is exactly the structural tension that
motivates the Higgs mechanism in the real Standard Model — which this notebook has deliberately
been trying to avoid throughout (per pp.92–97's stated goal). **Verdict: NOT-TESTABLE** — accurate,
standard conceptual observations, not closed derivations.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-130 | SOLID |
| NB-131 | SOLID |
| NB-132 | SOLID |
| NB-133 | SOLID |
| NB-134 | NEEDS-WORK (self-flagged error confirmed genuine, root cause found) |
| NB-135 | SOLID |
| NB-136 | SOLID |
| NB-137 | NEEDS-WORK (M_W, h confirmed; I(n) table and k=1.39 underspecified) |
| NB-138 | SOLID |
| NB-139 | SOLID |
| NB-140 | SOLID-WITH-CORRECTION |
| NB-141 | NEEDS-WORK (dead-end reasoning step, but sound final construction) |
| NB-142 | NOT-TESTABLE |

**What closed:** the entire sin²θ_W numerology chain (NB-130–133) checks out exactly, including
the notebook's own "coupling to $3e$" numerology giving exactly $2/9$. NB-134's self-flagged
inconsistency is confirmed genuine and its root causes precisely located (a $\sqrt{1/7}$ vs.
$\sqrt{2/7}$ radical slip, and a $Q_z$ entry that appears to be copied from the wrong page's
result rather than recomputed). NB-135/136/138/139 are all exactly confirmed, including
identifying NB-139's apparent "factor of 2" as a known, deliberate literature convention rather
than an error. NB-140's top-line equation is found to describe a circle rather than an ellipse
(evidently a transcription slip), with the actual derivation underneath shown to be exactly
correct once corrected. NB-141's stated reasoning step is shown not to connect to its own
conclusion, though the conclusion itself is standard and sound.

**What's still open:** NB-137's $I(n)$ table and the $k=1.39$ figure could not be reconstructed
from the page's surviving transcription — flagged honestly as underspecified rather than forced
to an incorrect match.

---

## Errata — errors in the notebook (2007)

- **p.104 (NB-134):** $\tan\theta_W$ printed as $\sqrt{1/7}\approx0.378$ where the accompanying
  decimal $\approx0.535$ requires $\sqrt{2/7}=0.5345$; the $Q_z$ entry $2.37$ (claimed $=2\sqrt7/3$)
  does not match the true value at $\sin^2\theta_W=2/9$ ($9\sqrt{14}/14=2.405$) and instead exactly
  equals NB-130's *experimental* result from the previous page — apparently copied rather than
  recomputed. The author's own follow-up consistency check correctly catches a resulting
  inconsistency (marked with a hand-drawn ✗), confirmed here to be a genuine failure
  ($11/6+6/11=157/66\ne7/3$), not an overreaction.
- **p.107 (NB-140):** the ellipse equation as transcribed, $x^2/b^2+y^2/b^2=1$, describes a circle
  (both denominators equal); the stated intercepts and the entire subsequent derivation are only
  consistent with $x^2/b^2+y^2=1$. The $b=1.2$ numeric example rounds to $0.67$ where the correctly
  rounded value is $0.66$ (true value $0.6633$) — a trivial slip.

## Errata — errors in my framing of these prompts

- An initial attempt to reconstruct NB-137's $I(n)$ table assumed $n$ was a simple integration
  lower-limit parameter of a single dimensionless integral and computed candidate values that
  matched only the first row to order of magnitude. Rather than force this into a false "match"
  or declare the notebook wrong, the annotation's own mass labels ($m_e=511\,\mathrm{keV}$ at
  $n=1$, $m_\nu=5\,\mathrm{eV}$ at $n=2$ — five orders of magnitude apart) were checked directly
  and shown to be inconsistent with any single smooth formula in $n$, leading to the honest
  "underspecified" verdict rather than a forced numerical claim.
- An initial NB-140 intercept check declared the $x,y$ symbols `positive=True`, which caused
  `sympy.solve` to silently return only the positive root of each intercept equation and made the
  ellipse-vs-circle check appear to fail even after the correct equation was substituted. Caught by
  inspecting the raw solve output before writing a verdict; fixed by re-declaring the symbols as
  plain-real (not positive-restricted) for that specific check.

## Correlation queue additions

One entry added — see the correlation queue file for the full row. NB-133's notebook-native
derivation lands on $\sin^2\theta_W=2/9$ exactly, from an idle "what if the charged-current
coupling is exactly $3e$?" hypothesis the author immediately questions ("is there any significance
to this?") and never develops further — NB-134's own follow-up arithmetic on the very same page
then fails its own self-consistency check (see above), so the notebook itself does not treat this
as a solid result. This reconstruction flags the bare numerical coincidence with the governing
prompt's own decision 7 ($\delta^*=2/9$ rad, described there as load-bearing and "primary") as
worth a correlation-queue question, with the caveats stated plainly: the two $2/9$'s arise from
completely unrelated hypotheses (a weak-coupling-ratio guess here vs. a representation-weight
angle there), share no derivation route this reconstruction can identify, and the notebook's own
instance is explicitly tentative and self-undermined by its own arithmetic. Flagged as a question
precisely because the resemblance could be entirely coincidental — not softened, per the queue's
own standing rule, but not overstated either.
