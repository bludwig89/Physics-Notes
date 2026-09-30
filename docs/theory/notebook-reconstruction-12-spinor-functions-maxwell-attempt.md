# Notebook Reconstruction — Batch 12: "Spinor Functions" — Weyl Component
# Equations, the Light-Cone Constraint Field Equation, and the First
# "Maxwell from Weyl" Attempt (pp. 127–140)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 127–140
(NB-154 – NB-164), the "Spinor Functions" section of a new spiral-bound notebook. Continues
directly from batch 11 (NB-143 – NB-153, pp.110–124). Per the governing prompt's firewall, this
batch does not consult `findings/`, `docs/claims/`, or any of the other excluded files. This is
the densest, messiest stretch reconstructed so far — the notebook's own text visibly disintegrates
partway through (an inserted devotional line appears mid-derivation), and several claims could not
be verified as stated despite exhaustive search; both are reported honestly below rather than
forced to a fit.

Date-time stamp: 2026-09-22 - (batch 12).

Scripts: `tests/runners/notebook-recon/run_NB-154_157_weyl_component_form.py`,
`run_NB-158_160_lightcone_constraint_field_eq.py`, `run_NB-161_164_maxwell_from_weyl.py`.
Results: matching JSON files in `test-results/notebook-recon/`.

---

## NB-154 (p.127) — $\sigma^\mu\partial_\mu\Psi=0$ in Component Form: **Confirmed**

**Verified**: building $\sigma^i\partial_i$ from the standard Pauli matrices, splitting it into
off-diagonal ($\sigma_x,\sigma_y$) plus diagonal ($\sigma_z$) pieces, and reading off components
reproduces the notebook's own displayed $\partial_0\eta,\partial_0\xi$ equations exactly, and the
rearranged forms (1a) $(\partial_0-\partial_z)\eta=(\partial_x-i\partial_y)\xi$ and (1b)
$(\partial_0+\partial_z)\xi=(\partial_x+i\partial_y)\eta$ follow by direct algebraic rearrangement.
**Verdict: SOLID.**

## NB-155 (pp.127–128) — Attempted Equation for $\varphi=\eta/\xi$: **A Genuine Product-Rule Slip, Confirming the Author's Own "Intractable Mess" Verdict**

**Notebook:** substitutes $\eta=\varphi\xi$ into (1a), displaying
$(\partial_0-\partial_z)(\varphi\xi) = \varphi(\partial_0-\partial_z)\xi+(\partial_0+\partial_z)
\varphi\cdot\xi$.

**Verified**: the correct product-rule expansion of $(\partial_0-\partial_z)(\varphi\xi)$ is
$\varphi(\partial_0-\partial_z)\xi+\xi(\partial_0-\partial_z)\varphi$ — the **same** operator
$(\partial_0-\partial_z)$ must apply to $\varphi$ as to the whole product, not the
opposite-sign $(\partial_0+\partial_z)$ the notebook displays. Confirmed by direct symbolic
product-rule expansion. **Verdict: INCORRECT (as transcribed) / DEAD-END-AUTHOR-CALLED-IT** — the
author's own immediate assessment ("this seems an intractable mess!") is correct, and this
reconstruction independently confirms a genuine algebra slip underlies that mess, not just its
inherent difficulty.

## NB-156 (pp.128–129) — Wave Equations $(\partial_0^2-\nabla^2)\xi=0$, $(\partial_0^2-\nabla^2)\eta=0$: **Confirmed**

**Verified**, step by step: applying $(\partial_0-\partial_z)$ to (1b) gives
$(\partial_0^2-\partial_z^2)\xi$ on the left; the right side rearranges (partial derivatives
commute) to $(\partial_x+i\partial_y)(\partial_0-\partial_z)\eta$, and substituting (1a) gives
$(\partial_x+i\partial_y)(\partial_x-i\partial_y)\xi=(\partial_x^2+\partial_y^2)\xi$ — all three
steps confirmed exactly by direct symbolic computation. **Verdict: SOLID** (the companion equation
for $\eta$ follows by the identical argument with $\eta\leftrightarrow\xi$, (1a)$\leftrightarrow$
(1b) swapped, not independently re-run but confirmed by symmetry).

## NB-157 (p.129) — Attempted Factorization Into (3a)+(3b): **Algebra Confirmed; the "Split" Correctly Flagged by the Author as a Nontrivial Ansatz**

**Verified**: the product-rule expansion of $(\partial_0^2-\nabla^2)(\varphi\xi)=0$ matches the
notebook's displayed six-term expansion exactly; applying (2b) (the just-confirmed wave equation
for $\xi$) to drop the $\varphi(\partial_0^2-\nabla^2)\xi$ term leaves exactly the notebook's
combined relation $\xi(\partial_0^2\varphi-\nabla^2\varphi) = 2(\nabla\varphi)\cdot(\nabla\xi) -
2(\partial_0\varphi)(\partial_0\xi)$ — confirmed by direct symbolic substitution.

**On the proposed split into (3a) $\partial_0^2\varphi-\nabla^2\varphi=0$ and (3b)
$(\nabla\varphi)\cdot(\nabla\xi)-(\partial_0\varphi)(\partial_0\xi)=0$:** this single combined
relation has the form $\xi A = 2B$; setting both $A=0$ and $B=0$ separately is **sufficient** to
satisfy it but is **not forced** by the algebra above — any $\xi,A,B$ with $\xi A=2B$ (e.g. both
nonzero but in the right proportion) would also satisfy the original relation. The author's own
phrasing — "Could we split these...?" — correctly flags this as a proposed additional ansatz
rather than a derived consequence. **Verdict: SOLID** (the algebra up to the combined relation is
exact; the author's own tentative framing of the subsequent split is an accurate self-assessment,
not an overclaim).

---

## NB-158 (pp.129–130) — Light-Cone Constraint Field Equation $V^\mu\partial_\nu V_\mu=0$: **Confirmed via a Cleaner Independent Route**

**Notebook:** derives the boxed "essential equation" $V^\mu\partial_\nu V_\mu=0$ via a
finite-difference argument using $\Delta x^\mu$, with notation that reuses the index $\mu$ for two
different roles ("$\Delta x^\mu\partial_\mu V_\mu$") and is difficult to follow literally.

**Reconstruction.** Rather than re-trace the page's own informal argument, this was verified via
the clean, standard, and rigorous route: if $V^\mu(x)V_\mu(x)=0$ holds **identically at every
spacetime point** (not just one), differentiating with respect to any $x^\nu$ gives
$\partial_\nu(V^\mu V_\mu)=2V^\mu\partial_\nu V_\mu=0$ by the product rule and symmetry of the
contraction — forcing exactly the boxed result, confirmed by direct symbolic differentiation for
all four $\nu$. **Verdict: SOLID** (final boxed result confirmed via a clean, independent
derivation; the page's own finite-difference path has confusing, index-clashing notation not
independently verified line-by-line — matching the precedent set in batch 08 for NB-109/110,
verifying the physically meaningful final claim directly rather than an unclear derivation path).

## NB-159 (pp.130–131) — Unimodular Constraint and $V_0=\text{const}$: **Confirmed**

**Verified** by the identical clean argument: differentiating $|\vec V|^2=1$ everywhere gives
$\vec V\cdot\partial_\nu\vec V=0$ for all $\nu$ (confirmed directly). Substituting this into
NB-158's $V^\mu\partial_\nu V_\mu=0$ leaves exactly $V_0\,\partial_\nu V_0=0$ for every $\nu$
(confirmed by direct substitution) — forcing $V_0=\text{const}$ for $V_0\ne0$, exactly the
notebook's own conclusion. **Verdict: SOLID.**

## NB-160 (p.131) — $\zeta=(V_1+iV_2)/(V_0-V_3)$: **Confirmed**

A direct, exact relabeling of the previously-established light-cone spinor ratio
$\zeta=(x+iy)/(t-z)$ with $(t,x,y,z)\to(V_0,V_1,V_2,V_3)$ — confirmed by direct substitution.
**Verdict: SOLID.**

---

## NB-161 (pp.131–132) — "Maxwell Equations from the Weyl Equation": **Two Genuine Inconsistencies Found**

**Notebook:** restates $\sigma^\mu\partial_\mu$ as an explicit matrix, applies it to
$(\eta,\xi)^T$, then sets "$\xi=V_x+iV_y=V_0-V_z$" and "$\eta=t-z$" (identifications that, taken
literally, are self-contradictory and inconsistent with the section's own established conventions)
before displaying four real-part equations claimed to reduce, "by symmetry," to the light-cone-like
system of NB-162.

**Two things checked, both confirmed genuine:**

1. **The boxed $\sigma^\mu\partial_\mu$ matrix and its own very next componentwise expansion
disagree in sign.** Direct matrix multiplication of the matrix exactly as given (with
"$-\partial_x+i\partial_y$" in the (1,2) entry) against $(\eta,\xi)^T$ gives row 1 $=
(\partial_0-\partial_z)\eta+(-\partial_x+i\partial_y)\xi$ — but the page's own displayed
componentwise equation (1) shows row 1 with the **opposite sign** on the $\xi$ term,
$(\partial_x-i\partial_y)\xi$. Confirmed by direct symbolic matrix multiplication.

2. **Neither natural reading of the $\eta,\xi\leftrightarrow V$ identification reproduces all
four displayed equations.** Two candidate labelings were tried — (A) $\eta=V_x+iV_y,\ \xi=V_0-V_z$
(matching the literal word order) and (B) $\eta=V_0-V_z,\ \xi=V_x+iV_y$ (matching NB-160's own
$\zeta$ convention) — against the first two displayed real-part equations and the curl-free
condition $\partial_yV_x-\partial_xV_y=0$. **Candidate A reproduces only the first ($\partial_x$)
equation; candidate B reproduces only the curl-free condition; neither reproduces all three.**

**Verdict: NEEDS-WORK.** Two independently-confirmed inconsistencies — a sign mismatch between the
matrix and its own componentwise expansion, and an ambiguous, self-contradictory $\eta,\xi$
identification that no single natural reading fully resolves. The section's overall *goal*
(getting from a Weyl-type equation to a Maxwell-like system) is not in question — it succeeds
cleanly in NB-129 (batch 09) and, via a different route, in NB-158/159 above — but this specific
page's own execution does not check out as transcribed.

## NB-162 (pp.132–133) — Boxed $\partial_0\vec V=-\nabla V_0$, $\partial_0V_0=\vec\nabla\cdot\vec V$: **A Fresh Ansatz, Not a Derived Consequence of NB-158/159**

**Assessment.** These two boxed equations are **not** a re-derivation of NB-158/159's null +
unimodular constraints — those forced the much stronger $V_0=\text{const}$, whereas this system
permits $V_0$ to vary, constrained only by $\vec\nabla\cdot\vec V$. Structurally, this is exactly
the same Maxwell-curl-equation *form* independently confirmed correct in batch 09's NB-129
($\psi_+=E+iB$ reducing to $\partial_tE=c\nabla\times B$, $\partial_tB=-c\nabla\times E$), here
with a single vector $\vec V$ playing a role analogous to one of $E,B$ and the scalar $V_0$
playing a different, partner role — not the full two-independent-3-vector field-strength
structure. The notebook does not flag the transition from the NB-158/159 regime to this one.
**Verdict: NEEDS-WORK** — a fresh physical ansatz introduced without being shown to follow from
the immediately preceding, already-verified material; the form itself is the standard,
independently-confirmed Maxwell-curl pattern.

## NB-163 (p.133) — Paired Field $\xi'=-\eta^*,\ \eta'=\xi^*$: **The Specific Claim Could Not Be Verified, Despite an Exhaustive Search**

**Notebook:** claims this substitution transforms $\sigma^\mu\partial_\mu(\xi,\eta)^T=0$ into two
displayed equations (3a),(3b), asserted to be "the same as (1a) and (1b)."

**Verified, exhaustively.** Direct symbolic substitution of the literal $\xi'=-\eta^*,\eta'=\xi^*$
does **not** reproduce the notebook's own displayed (3a) or (3b). An exhaustive sweep over all
eight sign/source combinations of $(\xi',\eta')$ built from $(\pm\eta^*,\pm\xi^*)$ was checked
against (3a), (3b), the original (1a)/(1b), and their conjugates and negations — **no match was
found under any variant**. This specific algebraic claim could not be reconstructed. Notably, the
surrounding text is visibly disordered at exactly this point — an out-of-place devotional line
("Let me find grace in thy sight, oh Yahweh...") appears immediately after, consistent with this
being a genuinely confused or corrupted passage in the original notebook rather than a clean
derivation this reconstruction simply failed to follow. **The broader conceptual point is
unaffected and stands on its own**: a charge-conjugation-type construction from a Weyl spinor's
complex-conjugated components generically producing an independent second solution — thereby
adding degrees of freedom beyond a single real null 4-vector's minimal encoding — is standard and
correct physics, regardless of this specific page's algebra. **Verdict: NEEDS-WORK.**

## NB-164 (p.133) — Quaternion $q=\sigma^\mu V_\mu$ and Its Column Decomposition: **Confirmed**

**Verified**: $q=V_0\sigma_0-V_x\sigma_x-V_y\sigma_y-V_z\sigma_z$ matches the notebook's explicit
matrix $\begin{pmatrix}V_0-V_z&-V_x+iV_y\\-V_x-iV_y&V_0+V_z\end{pmatrix}$ exactly, and the two
displayed 2-spinors $\varphi_1,\varphi_2$ are confirmed to be exactly $q$'s first and second
columns respectively. **Verdict: SOLID.**

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-154 | SOLID |
| NB-155 | INCORRECT (as transcribed) / DEAD-END-AUTHOR-CALLED-IT |
| NB-156 | SOLID |
| NB-157 | SOLID |
| NB-158 | SOLID |
| NB-159 | SOLID |
| NB-160 | SOLID |
| NB-161 | NEEDS-WORK |
| NB-162 | NEEDS-WORK |
| NB-163 | NEEDS-WORK |
| NB-164 | SOLID |

**What closed:** the clean first-order Weyl component system (NB-154), its wave-equation
consequences (NB-156), and the light-cone/unimodular constraint field equations (NB-158, NB-159,
confirmed via a cleaner independent route than the page's own messy finite-difference argument)
are all exactly correct. NB-155's abandoned spinor-ratio attempt is confirmed to contain a genuine
product-rule slip, vindicating the author's own immediate "intractable mess" verdict. NB-157's
algebra is exact, and the author's own tentative framing of a subsequent equation-splitting move
is confirmed to be an accurate (not overclaiming) self-assessment. NB-164's quaternion
decomposition is exact.

**What's still open:** this batch has the highest concentration of unresolved material in the
reconstruction so far. NB-161 contains two independently-confirmed inconsistencies (a sign
mismatch between a matrix and its own componentwise expansion; a self-contradictory field
identification with no fully-consistent reading found). NB-162 is a fresh physical ansatz not
shown to follow from the immediately preceding, already-verified constraints. NB-163's specific
algebraic claim could not be verified despite an exhaustive computer search over every natural
sign/pairing variant — flagged honestly as unresolved, with the note that the surrounding text
itself shows signs of disorder at exactly this point, rather than forced into a false match.

---

## Errata — errors in the notebook (2007)

- **p.127 (NB-155):** the displayed product-rule expansion of $(\partial_0-\partial_z)(\varphi\xi)$
  uses $(\partial_0+\partial_z)\varphi$ where the correct product rule requires the same
  $(\partial_0-\partial_z)$ operator on $\varphi$ as on the whole product — confirmed by direct
  symbolic expansion. Consistent with, and likely the specific cause of, the author's own
  immediate "intractable mess" assessment.
- **p.131 (NB-161):** the boxed $\sigma^\mu\partial_\mu$ matrix and its own next-line componentwise
  expansion disagree in the sign of the $\xi$ term in row 1 — confirmed by direct matrix
  multiplication. The paragraph's field identification ("$\xi=V_x+iV_y=V_0-V_z$") is
  self-contradictory as written (equates two generically-different quantities), and neither of
  the two most natural readings fully reproduces the page's own four displayed real-part
  equations.
- **p.133 (NB-163):** the claimed transformation of $\sigma^\mu\partial_\mu(\xi,\eta)^T=0$ under
  $\xi'=-\eta^*,\eta'=\xi^*$ into the displayed (3a),(3b) could not be verified under any of eight
  systematically-checked sign/pairing variants — likely a genuinely confused or corrupted passage,
  signaled also by the out-of-place devotional line immediately following it in the transcription.

## Errata — errors in my framing of these prompts

- An initial NB-164 verification compared sympy `Matrix` objects to the Python integer `0` (e.g.
  `sp.simplify(A - B) == 0`) instead of `sp.zeros(n, m)`, which always evaluates `False` for a
  non-empty matrix regardless of whether the matrix is actually the zero matrix — this produced
  three false "mismatch" results (`q_matches`, `phi1_is_col1`, `phi2_is_col2`) despite the
  underlying algebra being exactly correct (confirmed by printing the matrices, which were
  visibly identical). Caught by inspecting `srepr` of the difference directly, which showed exact
  zero entries; fixed by comparing to `sp.zeros(...)` throughout.
- An initial NB-163 check used the wrong assignment (`eta_p=-conj(eta)`, `xi_p=conj(xi)`) —
  swapping which of $\eta,\xi$ each primed field is built from, the opposite of the notebook's own
  stated $\xi'=-\eta^*,\eta'=\xi^*$. This was caught before drawing a conclusion by re-reading the
  page's exact wording and the fact that the target equations (3a),(3b) explicitly use the
  $(\xi,\eta)$ vector ordering (reversed from page 127's $(\eta,\xi)$), not the ordering first
  assumed; the corrected, exhaustive version is what's reported above.

## Correlation queue additions

None from this batch meet the bar as a fresh entry. NB-162's Maxwell-curl-equation-shaped ansatz
is the same structural pattern as batch 09's NB-129 (already queued), not a new independent
occurrence worth a second row — noted here in the write-up for cross-reference rather than
duplicated in the queue.
