# Notebook × SM Cross-Check — pp. 141–160: "Spinors as Null Vectors; Vector Decomposition"

*2026-09-23 - 00:35 · checks `notebook-reconstruction-13-null-vector-decomposition.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-23, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.141-160 | 141–160 | REINFORCES | SETTLED | Standard special-relativistic null-vector/spinor correspondence and its tensor-product construction, exactly confirmed; a genuine classification-table gap and a genuine algebra error in a general decomposition formula were both found and corrected, but nothing here extends beyond, or conflicts with, standard SR. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from the light-cone/null-vector foundations already covered in the pp.127-140
cross-check (this section is a direct continuation of that same material — NB-165 is a bare
restatement of NB-158/159). The spinor$\leftrightarrow$null-vector correspondence
($\det(\sigma^\mu V_\mu)=V^\mu V_\mu=0$ for a null vector) is standard, unchanged mathematics
predating this notebook by decades (Penrose-Rindler spinor calculus, itself building on van der
Waerden's 1929 formalism).

## Per-build verdicts

### NB-165 (p.141) — Restated Light-Cone Field Equation
- **Checked against:** reconstruction status `SOLID` (a pure restatement of NB-158/159, already
  verified in batch 12)
- **Claim / anchor:** foundations — same as NB-158/159 (pp.127-140 cross-check).
- **Verdict:** REINFORCES · SETTLED

### NB-166 (pp.141–142) — "Is a Spinor a Null Vector?"
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** $\det(\sigma^\mu V_\mu)=V^\mu V_\mu$ exactly, so a null 4-vector
  corresponds to a Hermitian $2\times2$ matrix with vanishing determinant — the standard
  spinor/null-vector correspondence.
- **Anchor:** foundations — standard 2-spinor formalism (van der Waerden 1929; Penrose-Rindler),
  the mathematical basis for representing a null direction by a spinor, unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-167 (pp.143–144) — Tensor-Product Null-Vector Construction
- **Checked against:** reconstruction status `SOLID` (confirmed to always produce a null vector for
  *any* spinor, a general and always-true construction)
- **Claim (field terms):** the outer product $\bar\Psi\otimes\Psi$ of a spinor with its own
  conjugate is always Hermitian with exactly zero determinant — i.e. always represents a null
  vector.
- **Anchor:** foundations — the standard spinor-to-null-vector map (this construction, generalized
  to a Dirac spinor, is exactly how a fermion's null momentum/current is built from its spinor in
  the massless limit throughout the SM).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-168 (p.144) — Decomposition of a Timelike Vector Into Two Null Vectors
- **Checked against:** reconstruction status `SOLID` (the general bilinear identity and the
  explicit timelike example both confirmed exactly)
- **Claim (field terms):** any vector $V=a+b$ with $a,b$ both null satisfies $V^\mu V_\mu=2a^\mu
  b_\mu$; an explicit timelike vector is decomposed into two null pieces this way.
- **Anchor:** foundations — elementary bilinear algebra applied to the Minkowski inner product,
  standard.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-169 (p.144) — Timelike/Spacelike Classification Table (Genuine Definitional Gap Found)
- **Checked against:** reconstruction status `NEEDS-WORK` (the two timelike rows confirmed exactly;
  the two spacelike rows' stated defining conditions confirmed genuinely inadequate to distinguish
  the two cases they claim to, via an explicit counterexample)
- **Claim / anchor:** none in external SM/GR terms beyond standard timelike/spacelike
  classification — this is an internal notebook bookkeeping table with a genuine gap, not a
  physical claim with external content to check further.
- **Verdict:** NEUTRAL · SETTLED

### NB-170 (pp.144–145) — General Timelike Decomposition Formula (Algebra Error Found and Corrected)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
  (the defining equation is exact; the boxed closed-form solution for it, and a closing remark
  about $\det(\sigma^\mu V_\mu)$, are both found wrong and corrected)
- **Claim / anchor:** none beyond NB-166/168's already-covered null-vector/determinant
  correspondence — this build's errors are internal algebra-solving slips, not disputes with
  external physics.
- **Verdict:** NEUTRAL · SETTLED

## Reconstruction queries
None. Both corrections in this batch (NB-169's classification gap, NB-170's algebra error) are
internal notebook-fidelity findings, independently consistent with standard SR once corrected.

## Handoff items raised (mirrored into the handoff file)
None this run.

## Contamination log
None. This run drew only on the reconstruction file; the anchor (SR null-vector/spinor
correspondence) reuses ground already covered in the pp.31-39, pp.92-101, and pp.127-140
write-ups, so no new external search was needed.

## Appendix — search queries used
None — see the contamination log.

## Sources
None beyond the reconstruction file; no claims in this run required new citation beyond what
earlier write-ups already established for the same null-vector/spinor foundations.
