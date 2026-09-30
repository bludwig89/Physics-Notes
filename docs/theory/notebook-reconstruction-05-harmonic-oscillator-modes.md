# Notebook Reconstruction — Batch 05: Harmonic-Oscillator Structure, 45° Rotation Trick,
# Even/Odd Mode Decomposition (pp. 51–56)

Cold, independent reconstruction and continuation of `references/physics-notes-complete.md`
pages 51–56 (NB-062 – NB-074).

Date-time stamp: 2026-09-22 - (batch 05).

---

## NB-062 (p.51) — Mode Inverse Relations

**Notebook:** $a_k^+=\tfrac12(\phi_{-k}-\tfrac i{\omega_k}\pi_k)$, $a_k=\tfrac12(\phi_k+\tfrac i
{\omega_k}\pi_{-k})$, with $a_k=(a_{-k}^+)^*$ — a *cross-indexed* form, differing in surface
appearance from p.45's same-index inverse ($a_k^+=\tfrac12(\phi_k-\tfrac i{\omega_k}\pi_k)$).

**Verified** (`run_NB-062_mode_inverse_relations.py`, sympy, symbolic linear-system solve):
checked p.51's formula on its own terms (not by forcing it to match p.45's differently-indexed
version): (1) the stated reality constraint $a_k=(a_{-k}^+)^*$ holds exactly; (2) the map
$\{\phi_k,\phi_{-k},\pi_k,\pi_{-k}\}\to\{a_k^+,a_k,a_{-k}^+,a_{-k}\}$ is a genuine, invertible
linear change of variables. Both are the minimum bar for a sensible mode definition, and both
hold. **Verdict: SOLID** (as a self-consistent, if differently-indexed, convention).

## NB-063/NB-064 (p.51) — Wavefunction Interpretation; "Overly Simplistic" Self-Critique

Standard interpretive statements ($|n\rangle=\Psi(\phi_{-p},\ldots,\phi_p)$, probability density
$P(\phi_j)$) plus the author's own correct observation that $a_k^+a_k$ isn't simply a
single-oscillator number operator in this cross-mode setting. **Verdict: NOT-TESTABLE**
(interpretive statement) / **SOLID** (the self-critique is accurate, matching the genuine
$k,-k$-mixing structure this batch confirms throughout).

---

## NB-065/NB-066 (p.52) — The 45° Rotation Trick: Confirmed, With a Sign-Labeling Note

**Notebook:** toy coupled-oscillator model $\mathcal H\psi=-\hbar^2\partial_x\partial_y\psi-
\omega_0^2xy\psi=E_0\psi$; claims a 45° rotation $x=(x'+y')/\sqrt2$, $y=(x'-y')/\sqrt2$
diagonalizes it into one positive and one negative harmonic oscillator.

**Verified** (`run_NB-065_066_45deg_rotation.py`, sympy, full symbolic pullback of an explicit
function $\psi(x',y')$ through the coordinate change, chain rule applied to actual derivatives —
**an implementation bug caught and fixed along the way**: an initial version applied the $x$-chain-rule
operator twice instead of once for $\partial_x$ and once (with the correct sign) for $\partial_y$,
producing a spurious leftover cross term $\partial_{x'}\partial_{y'}\psi$; fixed by applying the
correct $y$-operator $\tfrac1{\sqrt2}(\partial_{x'}-\partial_{y'})$ for the second factor):

$$\mathcal H\psi=\Big[-\tfrac12\partial_{x'}^2\psi-\tfrac{\omega^2}2x'^2\psi\Big]+\Big[\tfrac12
\partial_{y'}^2\psi+\tfrac{\omega^2}2y'^2\psi\Big]$$

— confirmed **exactly** (symbolic residual identically zero). This is precisely one *negative*
harmonic-oscillator Hamiltonian (in $x'$) plus one *positive* one (in $y'$), matching the
notebook's qualitative claim exactly. The notebook's own literal transcription (line 1339) has
the opposite sign assignment ($+\omega^2x'^2$, $-\omega^2y'^2$) — since the physical claim ("one
positive, one negative") holds either way, this is most likely a $x'\leftrightarrow y'$ labeling
difference rather than a physics error.

**Verdict: SOLID** (central qualitative claim exactly confirmed; a labeling-level discrepancy
noted, not a physics error).

---

## NB-067 (p.53) — Bose Symmetrization Mechanics

Standard: the symmetrization operator $S=\tfrac1{N!}\sum_PP$ and the fact that commuting
creation operators automatically enforce Bose exchange symmetry. Elementary, standard QFT.
**Verdict: SOLID.**

---

## NB-068/NB-069 (p.54) — Reality Condition: **Genuine Error Found**

**Notebook:** derives $\phi_k=2\omega_k\int\phi(x)\cos(kx)d^3x+i2\omega_k\int\phi(x)\sin(kx)d^3x$
and $\phi_{-k}=2\omega_k\int\phi(x)\cos(kx)d^3x-i2\omega_k\int\phi(x)\sin(kx)d^3x$ for real
$\phi(x)$, then concludes **"$\phi_k-\phi_{-k}=0\Rightarrow\tilde\phi_q=0$."**

**Reconstruction.** From the notebook's own two displayed formulas, $\phi_{-k}$ is literally
$\phi_k$ with $i\to-i$ — i.e. $\phi_{-k}=\phi_k^*$, the standard reality condition for a real
scalar field's Fourier coefficients. That is *not* the same statement as $\phi_k=\phi_{-k}$,
which would require $\phi(x)$ to be an *even* function, not merely real.

**Verified numerically** (`run_NB-068_069_reality_condition.py`, scipy quadrature, an explicit
real but deliberately **asymmetric** test function $\phi(x)=e^{-(x-0.3)^2}+0.5e^{-(x+1.1)^2/0.7}$,
at $k=0.9$):

| quantity | value |
|---|---|
| $\|\phi_k-\phi_{-k}\|$ (notebook's literal claim) | $1.033$ — **not zero** |
| $\|\phi_k^*-\phi_{-k}\|$ (standard reality condition) | $0.0$ — exact |

Confirms precisely what the algebra predicts: the literal claim fails for a generic real
(asymmetric) field, while the standard reality condition $\phi_{-k}=\phi_k^*$ holds exactly, and
is directly readable off the notebook's own two formulas without any extra assumption.

**Verdict: INCORRECT (as transcribed), SOLID-WITH-CORRECTION.** Corrected statement:
$\phi_k^*=\phi_{-k}$ (equivalently $\phi_k-\phi_{-k}^*=0$), the standard reality condition — not
$\phi_k=\phi_{-k}$. This has a direct consequence for NB-071 below.

---

## NB-070 (p.55) — $H$ in $\alpha,\beta$ Operators

Direct algebraic consequence of the even/odd $\bar\phi_p,\tilde\phi_q$ decomposition and mode
definitions from NB-068/069, structurally the same substitution mechanics independently verified
for NB-073 below (same mixing-operator algebra, one page later). **Verdict: SOLID** (by
structural analogy to the verified NB-073 mechanics; not separately re-scripted).

## NB-071 (p.55) — Open Question: Can the Antisymmetric ($\beta$) Sector Be Dropped?

**Notebook:** poses this as an open question — "Two sets of particles described here. Can
antisymmetric be done away with due to non-Bose statistics?"

**Reconstruction, connecting to NB-068/069's finding.** The notebook's route toward an easy "yes"
seems to have been the (incorrect, per NB-069) belief that reality of $\phi(x)$ forces
$\tilde\phi_q=0$ (the antisymmetric/odd combination) identically. Since that's not generically
true — reality gives $\phi_{-k}=\phi_k^*$, not $\phi_k=\phi_{-k}$ — the antisymmetric $\beta$
sector is **not** eliminated by reality alone for a generic field configuration; whatever
justification (if any) exists for treating it specially would need to come from elsewhere (e.g.
a genuine physical distinction between the sectors, not a kinematic identity). This is exactly
the kind of thing a cold reconstruction is supposed to surface: the question the notebook poses
is still open, and one candidate route to answering it (the one implicit in the page 54 algebra)
is now known to be a dead end. **Verdict: NOT-TESTABLE** (open question, correctly still open;
NB-068/069's finding closes off one candidate resolution without answering the question itself).

## NB-072 (p.55) — Ink-Blot-Damaged Commutator Computation

**Notebook:** partial computation of $[\alpha_k,\alpha_p^+]$, physically obscured by an ink blot
in the original notebook page, transcription marked "(further algebra, partly obscured by ink
blot)."

**Assessment.** The general structure ($[\alpha_k,\alpha_p^+]$ should reduce to a Kronecker/Dirac
delta times a normalization, by the standard construction $\alpha_k=\tfrac12(\bar\phi_k-\tfrac i
{\omega_k}\bar\pi_k)$ from even-combination fields obeying canonical $[\bar\phi,\bar\pi]$
commutators) is unremarkable and expected to work out the same way NB-062's and NB-073's
mode-mixing algebra does. But the specific missing steps are physically illegible in the source
material, not just elided by the author. **Verdict: NEEDS-WORK** (unrecoverable due to page
damage, not a physics or reconstruction gap — nothing to close here without the original page).

---

## NB-073 (p.56) — Mixing Ansatz; $a_k^+a_k+a_ka_k^+$ Expansion

**Notebook:** $a_k^\pm=\tfrac1{\sqrt2}(\alpha_k^\pm\pm i\beta_k^\pm)$; expands
$a_k^+a_k+a_ka_k^+$ into $\alpha,\beta$ operators.

**Verified** (`run_NB-073_074_T_cross_term.py`, exact truncated 2-mode Fock matrices, $N=8$
levels — **two sign-slip bugs in this reconstruction's own script caught and fixed along the
way**, confirmed against an independent sympy noncommutative-symbol expansion before the final
matrix check): the full expansion
$$a_k^+a_k+a_ka_k^+=\tfrac12(\alpha_k^+\alpha_k+\alpha_k\alpha_k^++\beta_k^+\beta_k+\beta_k\beta_k^+)
+\tfrac i2(\beta_k^+\alpha_k-\alpha_k^+\beta_k+\alpha_k\beta_k^+-\beta_k\alpha_k^+)$$
matches the notebook's own displayed expansion (lines 1450–1456) **exactly**, confirmed to
machine precision ($3.6\times10^{-15}$). **Verdict: SOLID.**

## NB-074 (p.56) — The $T$ Cross Term Vanishes by Parity

**Notebook:** defines $T=\tfrac i2(\beta_k^+\alpha_k-\alpha_k^+\beta_k+\beta_k\alpha_k^+-
\alpha_k\beta_k^+)$ (the imaginary cross-term piece of NB-073's expansion); using
$\alpha_k=\alpha_{-k}$ (even) and $\beta_k=-\beta_{-k}$ (odd), concludes $T_k=-T_{-k}$, hence
$\int T_k\,d^3k=0$.

**Verified** (same script, sympy symbolic substitution on noncommuting operator symbols): the
stated parity substitution ($\alpha\to\alpha$, $\beta\to-\beta$ under $k\to-k$) applied to $T$
gives exactly $T(-k)=-T(k)$, confirmed symbolically. The consequence — that an operator-valued
function odd under $k\to-k$ integrates to the zero operator over the (symmetric) integration
domain — is the standard elementary fact that any odd integrand vanishes on a symmetric domain
(the same principle as $\int_{-L}^L k\,dk=0$), applying identically to an operator-valued
integrand added term by term. **Verdict: SOLID.**

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-062 | SOLID |
| NB-063 | NOT-TESTABLE |
| NB-064 | SOLID |
| NB-065 | SOLID |
| NB-066 | SOLID |
| NB-067 | SOLID |
| NB-068 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-069 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |
| NB-070 | SOLID |
| NB-071 | NOT-TESTABLE |
| NB-072 | NEEDS-WORK |
| NB-073 | SOLID |
| NB-074 | SOLID |

**What closed:** the 45° rotation trick (NB-065/066) is confirmed exactly, catching and fixing a
genuine bug in this reconstruction's own first-pass script along the way (a repeated-operator
chain-rule slip). The full $\alpha,\beta$ mixing algebra (NB-073) and the parity-based vanishing
of the cross term (NB-074) are both confirmed exactly, after two of this reconstruction's own
sign-convention slips were caught and fixed pre-verdict. A genuine notebook error was found at
NB-068/069: the claimed reality condition $\phi_k=\phi_{-k}$ is wrong (only true for an even
field); the correct standard condition $\phi_{-k}=\phi_k^*$ is directly confirmed instead,
numerically, on an explicit asymmetric test function.

**What's still open:** NB-071's question (can the antisymmetric $\beta$ sector be dropped?) is
still genuinely open — this batch shows one candidate route to an easy "yes" (via the NB-068/069
claim) doesn't work, without resolving the question itself. NB-072 stays open due to physical
page damage in the source material, not a reconstruction gap.

---

## Errata — errors in the notebook (2007)

- **p.54 (NB-068/NB-069):** the stated reality-condition claim "$\phi_k-\phi_{-k}=0\Rightarrow
  \tilde\phi_q=0$" is wrong for a generic real field — confirmed numerically on an explicit
  asymmetric real test function ($|\phi_k-\phi_{-k}|=1.03$, not zero). The correct condition,
  directly readable off the notebook's own two displayed formulas, is $\phi_{-k}=\phi_k^*$ (not
  $\phi_k=\phi_{-k}$). This has a live consequence for the open question at NB-071 (see above).

## Errata — errors in my framing of these prompts

- The first version of the NB-065/066 script (45° rotation) applied the coordinate-change
  first-derivative operator for $\partial_x$ twice instead of once for $\partial_x$ and once
  (with the correct, different sign) for $\partial_y$, producing a spurious cross term. Caught
  by inspecting the residual before writing a verdict; fixed.
- The first version of the NB-073/074 script ($\alpha,\beta$ mixing algebra) had two sign errors
  in the target expression (a missing overall $\tfrac12$ factor, then two terms with flipped
  signs) found via cross-checking against an independent sympy noncommutative-symbol expansion.
  Both caught and fixed before being written into a verdict.

## Correlation queue additions

None from this batch meet the bar for a model-comparison question — the genuine finding
(NB-068/069's reality-condition error) is purely internal notebook arithmetic with no obvious
connection to a specific model claim, and NB-071 stays an open question rather than a testable
claim to queue.
