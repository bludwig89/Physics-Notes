# Notebook Reconstruction — Batch 06: Complex Mass, Gauged Dirac Matrices, Weinberg–Salam
# Without Higgs (Opening) (pp. 57–67)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 57–67 (NB-075 – NB-085).

Date-time stamp: 2026-09-22 - (batch 06).

---

## NB-075 (p.57) — Sakurai Textbook Insert

A photocopied page from Sakurai's angular-momentum chapter, not the author's own derivation.
**Verdict: NOT-TESTABLE** (reference material, already the Phase-0 status; stands).

---

## NB-076/NB-077/NB-078 (pp.59–60) — Dirac Matrix Non-Uniqueness and Gauging

**Notebook:** standard Dirac $\alpha_i,\beta$ from $(\vec\alpha\cdot\vec pc+mc^2\beta)^2=(p^2c^2+
m^2c^4)I$ with $\alpha_i=\sigma_3\otimes\sigma_i$, $\beta=-\sigma_1\otimes\sigma_0$; non-uniqueness
$\beta=(a\sigma_1+b\sigma_2)\otimes\sigma_0$, $a^2+b^2=1$; gauged
$\beta_g=(U\sigma_1U^+)\otimes\sigma_0$, $U=\mathrm{diag}(1,e^{i\theta})$.

**Verified** (`run_NB-076_077_078_dirac_matrix_nonuniqueness.py`, sympy, explicit $4\times4$
tensor-product matrices): (1) the standard representation satisfies the full Dirac Clifford
algebra ($\{\alpha_i,\alpha_j\}=2\delta_{ij}I$, $\{\alpha_i,\beta\}=0$, $\beta^2=I$) exactly; (2)
the general $(a,b)$ family satisfies the same algebra for every $a,b$ with $a^2+b^2=1$; (3) the
gauged $\beta_g$ satisfies the same algebra **for every value of $\theta$**, symbolically.

A structural reason surfaces for free: $\beta_g$'s $\theta$-dependence lives entirely in the
second tensor factor (where $\beta$'s own $\sigma_0$ sits), while $\alpha_i=\sigma_3\otimes
\sigma_i$ acts on that same factor only through $\sigma_i$, which never touches an overall phase
on the $2\times2$ block $U\sigma_1U^+$ lives in — this is precisely *why* the gauge freedom acts
on "one half of the bispinor" only, exactly as the notebook observes, not merely an empirical
coincidence.

**Verdict: SOLID** (all three builds).

---

## NB-079 (p.61) — Weak Interaction Facts

Standard restated Standard Model facts ($W^\pm,Z$ couple only left-handed; $\gamma$ couples to
charge; $L\leftrightarrow R$ mixing $\Leftrightarrow$ mass). Correct as stated; not independently
derived on this page (a "known facts" summary). **Verdict: SOLID.**

---

## NB-080 (p.62) — Weinberg–Salam Lagrangian Without Higgs

Standard gauge-theory framework: $SU(2)$ field strength $\vec G^{\mu\nu}$, $U(1)$ field strength
$H^{\mu\nu}$, covariant derivatives $D_\mu^L,D_\mu^R$, explicit (non-dynamical) mass terms for
$\nu,e$. Correctly formed as a starting ansatz (the whole point of this section is to explore
what happens *without* a Higgs field generating those masses dynamically — the author states
this explicitly). **Verdict: SOLID** (structural framework, correctly assembled).

## NB-081 (p.62) — Critique of Dropping $\nu_R$

**Notebook:** conventional W–S drops $\nu_R$ and makes $e_R$ an isospin singlet, which the author
calls "stupid because it destroys the basic symmetry" between the doublets.

**Assessment.** This is a fair and historically-grounded critique — the standard-model choice to
omit $\nu_R$ is precisely because (at the time, and still in the minimal SM) neutrinos were taken
to be exactly massless, which is a *physical* input, not a symmetry requirement; the notebook's
observation that this breaks the manifest $L\leftrightarrow R$ symmetry between the lepton and
"neutrino" doublets is correct as a statement about the *structure* of the minimal SM (whether or
not one considers that structural asymmetry a flaw is a matter of taste/physics judgment, not
something with a right answer). **Verdict: SOLID** (as an accurate structural observation).

---

## NB-082/NB-083 (pp.63–64) — The $g'/g=\tan\theta$ Derivation, and a Precisely Located Sign Issue

**Notebook:** rotation $W^3_\mu=Z_\mu\cos\theta-A_\mu\sin\theta$, $W^0_\mu=Z_\mu\sin\theta+A_\mu
\cos\theta$ (with stated inverse); requiring $A_\mu$ not couple to $\nu_L$ gives boxed
$g'/g=\tan\theta$; then, requiring $A$'s coupling to $e_L$ be $e$, derives $e=2g\sin\theta$,
$\beta=\tfrac12e(\cot\theta-\tan\theta)$ — with the author's own margin note: *"the author flips
a sign somewhere; both forms are kept as written."*

**Verified, in two parts:**

**Part 1** (`run_NB-082_083_ws_rotation.py`, sympy, direct symbolic substitution): (a) the stated
forward/inverse rotation pair is a genuine matrix inverse of each other, confirmed exactly; (b)
substituting into $gW^3_\mu+g'W^0_\mu$ and demanding the $A_\mu$ coefficient vanish gives
$g'/g=\tan\theta$ **exactly**, confirmed by direct algebra; (c) as an independent cross-check
(not in the notebook), the resulting $Z$-coupling collapses to the clean closed form
$g/\cos\theta$ — exactly the standard electroweak result that the physical $Z$ coupling is
$g\sec\theta_W$, a good sign the rotation algebra is on the right track generally.

**Part 2 — locating the self-flagged sign issue precisely**
(`run_NB-083_e_beta_sign_issue.py`, sympy): the notebook's own p.63 coupling matrix shows
$\nu_L$ ($T_3=+\tfrac12$) couples via $+gW^3+g'W^0$ while $e_L$ ($T_3=-\tfrac12$) couples via
$-gW^3+g'W^0$ — a **relative sign flip** on the $g$ term that p.64's prose text doesn't restate
(it reuses "$gW^3+g'W^0$" without the flip). Testing both readings:

| reading | $e$ (should be $2g\sin\theta$) | $\beta$ |
|---|---|---|
| literal p.64 text (no sign flip) | $0$ — wrong | $g/\cos\theta$ — wrong |
| p.63-consistent ($T_3=-\tfrac12$ flip) | $2g\sin\theta$ — **exact match** | $g(\tfrac1{\cos\theta}-2\cos\theta)$ |

The $T_3$-flip reading is confirmed as the intended one (it's the only reading that reproduces
the notebook's own stated $e=2g\sin\theta$ exactly). But its resulting $\beta$ is the **exact
negative** of the notebook's own target $\beta=g(2\cos\theta-\tfrac1{\cos\theta})$ — i.e. $e$
checks out exactly and $\beta$ comes out sign-flipped. This **independently confirms and
precisely locates** the author's own self-flagged uncertainty: the sign slip is specifically in
$\beta$, not in $e$, and the fix is $\beta\to-\beta$.

**Verdict: SOLID** (NB-082, and NB-083's $g'/g=\tan\theta$ result); **SOLID-WITH-CORRECTION**
(NB-083's $\beta$ formula — corrected sign identified and confirmed, resolving the author's own
flagged uncertainty rather than leaving it open).

---

## NB-084 (pp.65–66) — Two Mass Formulas, Reconciled

**Notebook:** two different derivations of $m_Z^2$ in the same few pages, with the tension left
unresolved: (A, p.65) treating $W^3,W^0$ as independently massive gives
$m_Z^2=m_W^2\cos^2\theta+m_{W_0}^2\sin^2\theta$ plus an unwanted "anomalous" $Z$–$A$ cross term;
(B, p.66) assuming *only* a pure $Z$-mass term exists (photon massless from the start) and
matching coefficients gives the standard $m_Z^2=m_W^2/\cos^2\theta$.

**Verified and reconciled** (`run_NB-084_mass_matrix_comparison.py`, sympy, both expansions done
explicitly): both formulas are algebraically confirmed exactly as the notebook states them,
**and** the cross term in reading (A) is confirmed **genuinely nonzero** in general
($\propto(m_{W_0}^2-m_W^2)\sin2\theta$) — so the author's "anomalous term, what happens to it?"
concern is real, not a slip. The two readings aren't competing derivations of the same physics:
(A) posits two *independently* massive gauge bosons with no built-in reason for the photon to
stay exactly massless (hence the leftover mixing term); (B) assumes photon masslessness *a
priori* (as required by unbroken electromagnetism) and asks what $W^3$-coefficient a pure
$Z$-mass term implies — this is structurally the same constraint the Higgs mechanism enforces
automatically (the $(W^3,B)$ mass matrix from a single Higgs doublet vev has *exactly* one
massless and one massive eigenvalue *by construction*, not by separate postulate), which is
precisely why only (B) reproduces the standard relation.

**Verdict: SOLID** (upgraded from the Phase-0 provisional NEEDS-WORK — both formulas verified,
and the apparent tension between them fully explained rather than left open: they encode
different physical assumptions, not a contradiction).

---

## NB-085 (p.67) — Isospin/Spin Coupling Analogy: **Sign Error Found**

**Notebook:** claims $A_\mu$ couples to $\binom{\nu_L}{e_L}$ like $\begin{pmatrix}0&0\\0&1
\end{pmatrix}=\tfrac12(\tau_0+\tau_3)$ — i.e. projecting onto the lower ($e_L$) component.

**Verified** (sympy, direct matrix computation, standard convention $\tau_3=\mathrm{diag}(1,-1)$
with $\nu_L$ as $T_3=+\tfrac12$ upper component, $e_L$ as $T_3=-\tfrac12$ lower component — the
convention used throughout the surrounding pages, including NB-082/083's own $T_3$ assignments):
$$\tfrac12(\tau_0+\tau_3)=\mathrm{diag}(1,0)\ne\begin{pmatrix}0&0\\0&1\end{pmatrix}.$$
The projector onto the **lower** component is actually $\tfrac12(\tau_0-\tau_3)=\mathrm{diag}(0,1)$
— confirmed to match the target exactly. $\tfrac12(\tau_0+\tau_3)$ instead projects onto the
*upper* ($\nu_L$) component, the physically wrong statement (it would say $A_\mu$ couples to the
neutral, not the charged, lepton).

**Verdict: INCORRECT (as transcribed), SOLID-WITH-CORRECTION.** Corrected:
$\begin{pmatrix}0&0\\0&1\end{pmatrix}=\tfrac12(\tau_0-\tau_3)$, not $\tfrac12(\tau_0+\tau_3)$ —
a sign slip (or an implicit, unstated $\tau_3\to-\tau_3$ convention flip inconsistent with the
rest of the section). The companion claim (that $W$ couples to $\binom{e_R}{e_L}$ the same way
via $\tfrac12(\sigma_0+\sigma_3)$) has the identical structure and the identical sign issue.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-075 | NOT-TESTABLE |
| NB-076 | SOLID |
| NB-077 | SOLID |
| NB-078 | SOLID |
| NB-079 | SOLID |
| NB-080 | SOLID |
| NB-081 | SOLID |
| NB-082 | SOLID |
| NB-083 | SOLID / SOLID-WITH-CORRECTION ($\beta$ sign) |
| NB-084 | SOLID |
| NB-085 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |

**What closed:** the Dirac-matrix non-uniqueness and gauging claims (NB-076–078) all check out
exactly, with a structural explanation surfacing for free. The $g'/g=\tan\theta$ result
(NB-082/083) is confirmed exactly, and — going beyond what the notebook itself resolves — this
reconstruction **locates and fixes** the author's own self-flagged sign uncertainty precisely
(it's in $\beta$, not $e$; correction is $\beta\to-\beta$). NB-084's two-mass-formula tension,
left open by the notebook, is fully reconciled: both formulas are correct, they just encode
different physical assumptions (independently-massive $W^3,W^0$ vs. photon-massless-by-fiat),
and only the latter is the Higgs-mechanism-consistent one.

**What's still open:** nothing carried forward as NEEDS-WORK from this batch. NB-085's sign
error is new and independent of the NB-082/083 finding (different quantity, different page), not
a duplicate.

---

## Errata — errors in the notebook (2007)

- **p.64 (NB-083):** the $\beta=\tfrac12e(\cot\theta-\tan\theta)$ formula — equivalently
  $\beta=g(2\cos\theta-\tfrac1{\cos\theta})$ in closed form — has the wrong overall sign;
  corrected to $\beta=\tfrac1{\cos\theta}g-2g\cos\theta$ (the exact negative of the notebook's
  stated closed form). The companion $e=2g\sin\theta$ is exactly correct. Confirmed by direct
  symbolic substitution using the notebook's own p.63 $T_3$-sign convention.
- **p.67 (NB-085):** $\begin{pmatrix}0&0\\0&1\end{pmatrix}=\tfrac12(\tau_0+\tau_3)$ has the wrong
  sign; corrected to $\tfrac12(\tau_0-\tau_3)$ (confirmed by direct matrix computation using the
  standard $\tau_3=\mathrm{diag}(1,-1)$ convention used throughout the surrounding pages). The
  companion spin-projector claim has the identical error.

## Errata — errors in my framing of these prompts

- None found in this batch.

## Correlation queue additions

None from this batch meet the bar — these are internal notebook sign slips in a speculative,
non-Higgs W–S construction that the model (per CLAUDE.md decision 3) has moved well past via a
completely different hypercharge-on-$U(x)$ mechanism; there's no live structural question here
the model would plausibly have retained an opinion on.
