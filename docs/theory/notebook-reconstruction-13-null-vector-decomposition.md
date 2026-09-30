# Notebook Reconstruction — Batch 13: "Spinors as Null Vectors; Vector
# Decomposition" — Null-Vector Spinors, Tensor-Product Construction, and
# Decomposing an Arbitrary Vector Into Two Null Vectors (pp. 141–160)

Cold, independent reconstruction of `references/physics-notes-complete.md` pages 141–160
(NB-165 – NB-170). Continues directly from batch 12 (NB-154 – NB-164, pp.127–140). Per the
governing prompt's firewall, this batch does not consult `findings/`, `docs/claims/`, or any of
the other excluded files.

Date-time stamp: 2026-09-22 - (batch 13).

Scripts: `tests/runners/notebook-recon/run_NB-165_167_null_vector_spinor.py`,
`run_NB-168_170_vector_decomposition.py`.
Results: matching JSON files in `test-results/notebook-recon/`.

---

## NB-165 (p.141) — Restated Light-Cone Field Equation: **Inherits Batch 12's Verification**

Pure restatement of NB-158 ($V^\mu\partial_\nu V_\mu=0$) and NB-159 ($\vec V\cdot\partial_\mu\vec
V=0$), both independently verified exactly in batch 12 via direct differentiation of the
null-everywhere and unimodular-everywhere conditions. No new algebra to check. **Verdict: SOLID.**

## NB-166 (pp.141–142) — "Is a Spinor a Null Vector?": **Confirmed**

**Notebook:** if $V=\sigma^\mu V_\mu$ is null, its rows/columns are proportional:
$(V_0-V_z)/(-V_x-iV_y) = (-V_x+iV_y)/(V_0+V_z)$, reducing to $V_0^2-V_z^2=V_x^2+V_y^2$.

**Verified**: $\det(\sigma^\mu V_\mu)=V^\mu V_\mu$ exactly (direct symbolic computation of the
$2\times2$ determinant); cross-multiplying the stated proportionality is exactly the
$\det=0$ condition; that condition reduces exactly to the stated
$V_0^2-V_z^2=V_x^2+V_y^2$. **Verdict: SOLID.**

## NB-167 (pp.143–144) — Tensor-Product Null-Vector Construction: **Confirmed**

**Notebook:** $(k_1\ k_2)\otimes(\alpha,\beta)^T$ represents a valid $\sigma^\mu V_\mu$ (i.e. is
Hermitian) when $k_1=k_0\alpha^*,\ k_2=k_0'\beta^*$ with a single common real $k_0=k_0'$; the
spinor $(\alpha,\beta)$ itself gives a null vector via $(\alpha^*\ \beta^*)\otimes(\alpha,\beta)^T$.

**Verified**: setting $k_1=k_0\alpha^*,k_2=k_0\beta^*$ (real $k_0$, the **same** value for both)
makes both diagonal entries real and the off-diagonal entries exact complex conjugates of each
other — confirmed by direct symbolic Hermiticity check, and confirmed that a *different* $k_0$ for
each breaks the off-diagonal conjugate-symmetry. The special case $k_0=1$,
$(\alpha^*\ \beta^*)\otimes(\alpha,\beta)^T$, is confirmed to have **exactly zero determinant for
every** complex $\alpha,\beta$ — a clean, general, always-true null-vector construction, and
confirmed Hermitian. **Verdict: SOLID.**

---

## NB-168 (p.144) — Decomposition Into Two Null Vectors: **Confirmed**

**The general identity** $V^\mu V_\mu=2a^\mu b_\mu$ (given $V=a+b$, both $a,b$ null) is a trivial
consequence of bilinearity, confirmed by direct symbolic expansion.

**The explicit timelike example** — $V_\mu=\left(\tfrac12(t+|\vec V|),\tfrac12(\vec V+\hat
Vt)\right)+\left(\tfrac12(t-|\vec V|),\tfrac12(\vec V-\hat Vt)\right)$, restated as
$\tfrac12(1+V_0/|\vec V|)(|\vec V|,\vec V)+\tfrac12(1-V_0/|\vec V|)(-|\vec V|,\vec V)$ — is
confirmed on every count: the two pieces sum back to exactly $V_\mu=(t,\vec V)$; each piece is
independently confirmed null ($a_0^2=|\vec a|^2$ and $b_0^2=|\vec b|^2$, both exact); and the two
displayed algebraic forms are confirmed to be exactly the same decomposition, just rearranged.
**Verdict: SOLID.**

## NB-169 (p.144) — Classification Table by $1\pm V_0/|\vec V|$: **A Genuine Definitional Gap Found in the Spacelike Rows**

**Notebook:** a table classifying $V_\mu$ into "+timelike" ($V_0>|\vec V|$), "−timelike"
($V_0<-|\vec V|$), "+spacelike" ($V_0<|\vec V|$), and "−spacelike" ($V_0>-|\vec V|$), with claimed
consequent signs for $1\pm V_0/|\vec V|$ in each row.

**Verified, with a genuine problem found.** The two timelike rows check out exactly and
unambiguously against concrete test values. **The two spacelike rows do not**: the table's own
stated defining condition for "+spacelike," $V_0<|\vec V|$, is satisfied by **every** spacelike
vector — including ones with **negative** $V_0$. A direct counterexample ($V_0=-1,|\vec V|=2$,
genuinely spacelike and satisfying $V_0<|\vec V|$) gives $1+V_0/|\vec V|=0.5$, **not** "$>1$" as
the table's consequent column claims. The true condition for $1+V_0/|\vec V|>1$ is the *stricter*
$V_0>0$ (combined with $|V_0|<|\vec V|$), not merely $V_0<|\vec V|$. The table appears to intend
"+spacelike"/"−spacelike" as mirroring the future/past split of the timelike rows (positive vs.
negative $V_0$), but the printed defining conditions don't actually encode that distinction — both
conditions hold for *all* spacelike vectors regardless of the sign of $V_0$, so the two rows are
not well-defined as literally stated. **Verdict: NEEDS-WORK** (timelike rows confirmed exactly;
spacelike rows' defining conditions confirmed genuinely inadequate to distinguish the two claimed
cases, via direct counterexample).

## NB-170 (pp.144–145) — General Timelike Decomposition Formula: **A Genuine Algebra Error Found and Corrected; a Second Error in the Closing Remark**

**Notebook:** derives the defining condition $v^2=2a_0V_0-2(\hat a\cdot\vec V)a_0$ (equivalently
$a_0(V_0-\hat a\cdot\vec V)=v^2/2$), then boxes
$a_\mu=\frac{1}{2V_0}\left(V_0^2-|\vec V|^2+2\hat a\cdot\vec V\right)(1,\hat a)$.

**Verified, precisely quantified.** The defining condition itself is exactly right — confirmed
independently from first principles (requiring $b=V-a$ null given $a$ null, i.e.
$a^\mu V_\mu=v^2/2$), matching the notebook's own displayed line exactly. **But solving that
equation for $a_0$ gives**
$a_0=\dfrac{V_0^2-|\vec V|^2}{2(V_0-\hat a\cdot\vec V)}$ — **not** the boxed formula. Direct
symbolic substitution confirms: the *independently re-derived* $a_0$ makes $b=V-a$ exactly null
(residual $=0$), while the *notebook's own boxed* $a_0$ does **not** (a manifestly nonzero
residual). This is a genuine, precisely located algebra error isolated to the final
solving-for-$a_0$ step — the equation immediately above the box is exactly right.

**The closing remark, "$\sqrt{V_\mu V^\mu}=\det(\sigma^\mu V_\mu)$," is also incorrect** — NB-166
already established $\det(\sigma^\mu V_\mu)=V^\mu V_\mu$ **exactly**, with no square root on
either side; taking a square root of only the left side contradicts that already-verified
identity for any $V^\mu V_\mu$ not equal to 0 or 1. The correct statement, consistent with NB-166,
simply drops the square root: $V_\mu V^\mu=\det(\sigma^\mu V_\mu)$.

**Verdict: INCORRECT (as transcribed) / SOLID-WITH-CORRECTION** — the setup and defining equation
are exact; the boxed final solution for $a_0$ is wrong and is corrected here; the closing remark
is also wrong and corrected.

---

## Batch Summary

| Build | Verdict |
|---|---|
| NB-165 | SOLID |
| NB-166 | SOLID |
| NB-167 | SOLID |
| NB-168 | SOLID |
| NB-169 | NEEDS-WORK |
| NB-170 | INCORRECT (as transcribed) / SOLID-WITH-CORRECTION |

**What closed:** the null-vector/spinor correspondence (NB-166), the general tensor-product
null-vector construction (NB-167, confirmed to always work for *any* spinor), and the explicit
timelike two-null-vector decomposition (NB-168) are all exactly confirmed. NB-170's algebra error
is fully closed: the defining equation is exact, the boxed solution for it is wrong, and this
reconstruction supplies the correct closed-form replacement, confirmed to make both pieces null.
The closing remark's dropped/misplaced square root is also identified and corrected.

**What's still open:** NB-169's classification table has a genuine definitional gap in its
spacelike rows (the stated threshold conditions don't distinguish the two cases the table claims
to distinguish) — flagged with a precise counterexample rather than a full rewrite of the
author's evident intent (a positive/negative-$V_0$ split mirroring the timelike rows), since the
notebook doesn't spell out enough to be certain that's exactly what was meant.

---

## Errata — errors in the notebook (2007)

- **p.144 (NB-169):** the classification table's stated defining conditions for "+spacelike"
  ($V_0<|\vec V|$) and "−spacelike" ($V_0>-|\vec V|$) are both satisfied by *every* spacelike
  vector regardless of the sign of $V_0$ — they do not distinguish two different cases the way the
  table's consequent columns require. Confirmed by direct counterexample ($V_0=-1,|\vec V|=2$).
- **p.145 (NB-170):** the boxed formula
  $a_\mu=\frac{1}{2V_0}(V_0^2-|\vec V|^2+2\hat a\cdot\vec V)(1,\hat a)$ does not solve the page's
  own immediately-preceding, correctly-derived defining equation
  $a_0(V_0-\hat a\cdot\vec V)=\tfrac12(V_0^2-|\vec V|^2)$ — confirmed by direct substitution (the
  boxed formula leaves $b=V-a$ non-null). The correct solution is
  $a_0=\dfrac{V_0^2-|\vec V|^2}{2(V_0-\hat a\cdot\vec V)}$, confirmed exactly.
- **p.145 (NB-170):** the closing remark "$\sqrt{V_\mu V^\mu}=\det(\sigma^\mu V_\mu)$" contradicts
  the exact identity $\det(\sigma^\mu V_\mu)=V^\mu V_\mu$ established on p.141 (NB-166); the
  correct statement omits the square root entirely.

## Errata — errors in my framing of these prompts

- None found in this batch — every check reached a definite result on the first well-posed
  attempt, aside from routine iteration to phrase the NB-169 counterexample search clearly.

## Correlation queue additions

None from this batch meet the bar. This section is self-contained null-vector/spinor geometry
with no contact point to any named model decision beyond the general spinor/Weyl-equation
machinery already covered by the standing NB-007 correlation-queue entry.
