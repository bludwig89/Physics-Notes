# Notebook × SM Cross-Check — pp. 127–140: "Spinor Functions" — Weyl Component Equations,
# Light-Cone Constraint Field Equations, First "Maxwell from Weyl" Attempt

*2026-09-23 - 00:25 · checks `notebook-reconstruction-12-spinor-functions-maxwell-attempt.md` ·
protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-23, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.127-140 | 127–140 | REINFORCES | SETTLED | Standard Weyl-equation component algebra and light-cone/null-vector field constraints, correctly reconstructed via clean independent routes; this batch has the notebook's densest concentration of unresolved or internally inconsistent pages (one specific algebraic claim on a visibly disordered page could not be verified under any tried variant), but nothing that checks out conflicts with, or extends beyond, standard classical field theory. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from the classical-electrodynamics and Weyl-equation foundations already covered
in the pp.92-101 (Riemann-Silberstein/Maxwell) and pp.31-39 (Clifford algebra) cross-checks. This
batch is a further, more elaborate attempt at the same "Maxwell equations from a Weyl-type spinor
equation" program already graded there — the underlying physics anchor (null-vector field
constraints; the Maxwell-curl-equation pattern) is unchanged, standard, pre-2007 mathematics.

## Per-build verdicts

### NB-154 (p.127) — Weyl Equation in Component Form
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** $\sigma^\mu\partial_\mu\Psi=0$ rearranges into the standard coupled
  first-order component equations for a 2-spinor.
- **Anchor:** foundations — same Weyl-equation structure already covered at NB-039/040 (batch 03).
- **Verdict:** REINFORCES · SETTLED

### NB-155 (pp.127–128) — Attempted $\varphi=\eta/\xi$ Equation (Genuine Product-Rule Slip)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) /
  DEAD-END-AUTHOR-CALLED-IT` (a genuine product-rule error confirmed, vindicating the author's own
  immediate "intractable mess" self-assessment)
- **Claim / anchor:** none surviving — an abandoned, self-corrected attempt.
- **Verdict:** NEUTRAL · SETTLED

### NB-156 (pp.128–129) — Wave Equations for $\xi,\eta$
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** each Weyl component independently satisfies the standard massless wave
  equation $(\partial_0^2-\nabla^2)\psi=0$, as required for consistency with the first-order Weyl
  equation.
- **Anchor:** foundations — standard, unchanged.
- **Verdict:** REINFORCES · SETTLED

### NB-157 (p.129) — Attempted Factorization (Algebra Confirmed; Split Correctly Flagged as an Ansatz)
- **Checked against:** reconstruction status `SOLID` (the algebra up to the combined relation is
  exact; the reconstruction independently confirms the author's own tentative framing of a
  proposed further split is an accurate, non-overclaiming self-assessment — the split is
  sufficient but not forced by the preceding algebra)
- **Claim / anchor:** none distinct — pure algebraic manipulation, correctly self-assessed by the
  author as tentative.
- **Verdict:** NEUTRAL · SETTLED

### NB-158, NB-159 (pp.129–131) — Light-Cone and Unimodular Constraint Field Equations
- **Checked against:** reconstruction status `SOLID` (both; confirmed via a cleaner independent
  route than the page's own hard-to-follow finite-difference argument, matching the precedent set
  for NB-109/110 in batch 08 — verify the physically meaningful final claim directly)
- **Claim (field terms):** if a vector field satisfies $V^\mu V_\mu=0$ (null) or $|\vec V|=1$
  (unimodular) identically at every spacetime point, differentiating forces
  $V^\mu\partial_\nu V_\mu=0$ and, combined with nullity, $V_0=\text{const}$.
- **Anchor:** foundations — standard differential-geometric consequence of an identically-satisfied
  algebraic constraint on a field, unchanged mathematics.
- **Verdict:** REINFORCES · SETTLED

### NB-160 (p.131) — $\zeta=(V_1+iV_2)/(V_0-V_3)$ Relabeling
- **Checked against:** reconstruction status `SOLID` (direct relabeling of the already-established
  light-cone spinor ratio from the pp.110-124 material)
- **Claim / anchor:** none new — a substitution, not an independent claim.
- **Verdict:** NEUTRAL · SETTLED

### NB-161 (pp.131–132) — "Maxwell Equations from the Weyl Equation" (Two Inconsistencies Found)
- **Checked against:** reconstruction status `NEEDS-WORK` (a sign mismatch between a matrix and its
  own componentwise expansion, confirmed by direct multiplication; a self-contradictory field
  identification with no fully consistent reading found under either natural interpretation tried)
- **Claim / anchor:** none survives as a checkable external claim — this specific page's execution
  does not check out as transcribed. The broader program's *goal* (Maxwell from a Weyl-type
  equation) is not in question, since it succeeds cleanly elsewhere in the notebook (NB-129, batch
  09; NB-158/159/162 above/below) — only this specific page's algebra is unresolved.
- **Verdict:** NEUTRAL · SETTLED

### NB-162 (pp.132–133) — Fresh Maxwell-Curl Ansatz $\partial_0\vec V=-\nabla V_0$,
### $\partial_0V_0=\vec\nabla\cdot\vec V$
- **Checked against:** reconstruction status `NEEDS-WORK` (not derived from the immediately
  preceding NB-158/159 constraints — a fresh ansatz the page doesn't flag as a transition; but its
  *form* is independently confirmed to be the standard Maxwell-curl-equation pattern, the same one
  verified exactly at NB-129 in batch 09)
- **Claim (field terms):** the boxed equations have exactly the structural form of one half of the
  vacuum Maxwell curl equations, with $\vec V,V_0$ playing roles analogous to the field-strength
  components already verified in the Riemann-Silberstein construction.
- **Anchor:** classical electrodynamics — the same anchor already fully researched and cited at
  NB-129 (pp.92-101 cross-check); not re-researched here to avoid duplication.
- **Verdict:** REINFORCES · SETTLED (the mathematical *form*, which is what can be checked
  independently of the notebook's own unflagged transition into this ansatz)
- **Hindsight:** see NB-129's write-up (pp.92-101 cross-check) for the Riemann-Silberstein/
  photon-wavefunction context this pattern connects to.

### NB-163 (p.133) — Paired Field $\xi'=-\eta^*,\eta'=\xi^*$ (Specific Claim Unverifiable)
- **Checked against:** reconstruction status `NEEDS-WORK` (an exhaustive computer search over all
  eight natural sign/pairing variants found no match to the notebook's own displayed target
  equations; the surrounding transcription is visibly disordered at exactly this point, consistent
  with a genuinely confused or corrupted notebook passage rather than a reconstruction failure)
- **Claim / anchor:** the specific algebraic claim as stated cannot be checked (no verified content
  to grade). The reconstruction separately notes the *broader conceptual point* — that a
  charge-conjugation-type construction from a Weyl spinor's conjugated components generically
  produces an independent second solution, adding degrees of freedom beyond a single real null
  4-vector's minimal encoding — is standard, correct physics in general, but this is a general
  background fact offered by the reconstruction, not something this specific page's own
  (unverifiable) algebra establishes.
- **Verdict:** NEUTRAL · SETTLED (nothing checkable survives at the level of this specific build)

### NB-164 (p.133) — Quaternion $q=\sigma^\mu V_\mu$ Column Decomposition
- **Checked against:** reconstruction status `SOLID`
- **Claim / anchor:** none in external SM/GR terms — a direct, confirmed matrix-column identity.
- **Verdict:** NEUTRAL · SETTLED

## Reconstruction queries
None. NB-161's and NB-163's unresolved status is the reconstruction's own honest finding (genuine
notebook inconsistencies/possible page corruption), not a dispute with external physics this
cross-check would query.

## Handoff items raised (mirrored into the handoff file)
None this run.

## Contamination log
None. This run drew only on the reconstruction file; the anchors involved (Weyl equation, Maxwell
curl structure, null-vector constraints) were already researched and cited in the pp.31-39 and
pp.92-101 write-ups, so no new external search was needed.

## Appendix — search queries used
None — see the contamination log; every anchor in this batch reuses ground already covered and
cited in earlier write-ups (pp.31-39, pp.92-101).

## Sources
Carried over from `notebook-sm-crosscheck-pp092-101-lepton-table-rotation-spin1.md` (NB-129's
Riemann-Silberstein/Maxwell citations, the same anchor as NB-162 here): [The role of the Riemann-Silberstein vector in classical and quantum theories of electromagnetism (*J. Phys. A* 46, 053001, 2013)](https://iopscience.iop.org/article/10.1088/1751-8113/46/5/053001) [B]
