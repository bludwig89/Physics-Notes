# Notebook × SM Cross-Check — p. 77 and pp. 176–182: Angular Momentum Conservation With a Mass
# Term; Construction of Null Vectors; Final Pages

*2026-09-23 - 00:55 · checks `notebook-reconstruction-15-contaminated-defer-pass.md` (a
contaminated-session defer pass, cold-reconstructed independently per its own firewall — see that
file's header) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-23, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.77 | 77 | REINFORCES | SETTLED | The standard relativistic-QM fact that total angular momentum $J=L+S$, not orbital $L$ alone, commutes with the Dirac Hamiltonian is confirmed exactly by two independent methods; a hedged, unspecific speculation about charge and $W^\pm$ bosons is too vague to anchor to a checkable claim. |
| pp.176-182 | 176–182 | REINFORCES | SETTLED | The notebook's final pages continue the same null-vector/stereographic-projection construction already graded standard and correct throughout batches 11, 13, and 14; several genuine, precisely-located dimensional slips in the notebook's very last, most hastily-written lines were found and corrected, none changing the underlying (standard) mathematics. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from what earlier write-ups already cover for the same anchors: the Dirac
equation's $J=L+S$ conservation structure (unchanged since Dirac 1928) and the null-vector/spinor/
stereographic-projection foundations (unchanged since van der Waerden 1929, already researched for
the pp.110-124, pp.141-160, and pp.161-175 cross-checks).

## Per-build verdicts

### NB-099 (p.77) — Angular Momentum Conservation With a Mass Term
- **Checked against:** reconstruction status `SOLID` (a cold, independently reconstructed pass —
  this build was previously contaminated for a prior session and re-derived here from the raw
  transcription and standard textbook physics only)
- **Claim (field terms):** the free Dirac Hamiltonian's mass term mixes spin components (violating
  what would naively look like separate spin conservation), but total angular momentum
  $J=L+S=L+\tfrac12\hbar\vec\Sigma$ commutes with $H=\vec\alpha\cdot\vec p+\beta m$ exactly,
  confirmed here by two independent methods (explicit $4\times4$ matrix algebra, and genuine
  differential-operator action on a generic symbolic spinor field).
- **Anchor:** foundations — standard relativistic quantum mechanics (Greiner, cited accurately by
  the notebook), unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — this has been settled physics since the earliest days of the Dirac
  equation.
- A separate, explicitly hedged aside — that charge conservation might similarly split into an
  "intrinsic" piece plus a $W^\pm$-boson piece, in "a more advanced theory" — is too unspecific to
  anchor to any checkable external claim (unlike, e.g., the more concrete $\nu_R$ critique at
  NB-081, pp.57-76 cross-check, which had a sharp, checkable structural question behind it). Graded
  NEUTRAL/NOT-TESTABLE, consistent with the reconstruction's own characterization as "a research
  motivation, not a derivation."

### NB-180 (p.176) — Rotation About $z$ as an Overall Phase on the Stereographic Coordinate
- **Checked against:** reconstruction status `SOLID` (independently reconstructed since the
  underlying stereographic formula this page assumes lies outside this batch's page range;
  confirmed to reproduce an exact $z$-axis rotation)
- **Claim (field terms):** a rotation about the polar axis of the projection sphere acts as a pure
  phase (Möbius) transformation, $x_0+iy_0\to e^{i\theta}(x_0+iy_0)$, on the stereographic-plane
  coordinate.
- **Anchor:** foundations — the same standard stereographic-projection/spinor correspondence
  already established at NB-143-153 (pp.110-124 cross-check).
- **Verdict:** REINFORCES · SETTLED

### NB-182 (pp.176–177) — Null Vectors as Outer Products; Phase Ambiguity
- **Checked against:** reconstruction status `SOLID` (every step confirmed exactly, once the
  section's implicit nullness/future-pointing assumption is made explicit)
- **Claim (field terms):** the outer product $vv^\dagger$ of a spinor with its own conjugate
  reproduces the standard null-vector Hermitian-matrix correspondence, with a genuine phase
  ambiguity in how the individual spinor components are assigned (the same kind of ambiguity
  already confirmed at NB-152, pp.110-124 cross-check).
- **Anchor:** foundations — same as NB-167 (pp.141-160 cross-check), the standard tensor/outer-
  product null-vector construction.
- **Verdict:** REINFORCES · SETTLED

### NB-184 (p.178) — Null $2\times2$ Matrix Factorization (Intermediate Slip Found)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (the final boxed
  factorization — every rank-≤1 matrix is an outer product of two vectors — confirmed exact; one
  intermediate line found to contain a genuine algebra slip, confirmed by direct counterexample,
  not propagating into the correct final result)
- **Claim / anchor:** none beyond the standard rank-1-matrix-is-an-outer-product fact, unchanged
  linear algebra.
- **Verdict:** NEUTRAL · SETTLED

### NB-185 (pp.178–179) — Timelike Decomposition Into Two Null Vectors (Notational Overload Resolved)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (the geometry and master
  relation $V\cdot V=2V\cdot a$ confirmed standard and exact; the boxed "solved for $a_0$" formula
  resolved as correct only under a specific reading of the notationally-overloaded "$\hat a\cdot V$"
  — the raw vector's dot product, not a true unit-vector dot product — which is how the notebook
  itself uses the symbol one section later)
- **Claim / anchor:** none beyond the same standard null-vector decomposition already established
  at NB-168/170 (pp.141-160 cross-check).
- **Verdict:** NEUTRAL · SETTLED (the underlying geometry is REINFORCES-standard, already graded at
  NB-168; this build's own specific content is the notation-resolution itself, an internal
  bookkeeping matter)

### NB-186 (pp.179–182) — Final Null Component Geometry (Three Independent Dimensional Slips Found)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (the core geometric machinery
  confirmed exact; three further, independent slips found in the notebook's very last lines — a
  squared-instead-of-linear denominator, a claimed "sphere" that is actually an ellipsoid and is
  dimensionally short a factor of $V_0^2$, and a closing cylindrical formula dimensionally short
  one factor of $r$ — all precisely located and corrected, consistent with these being the
  notebook's most hastily-written closing lines)
- **Claim / anchor:** none beyond the same stereographic-projection/null-vector foundations already
  established throughout batches 11, 13, and 14.
- **Verdict:** NEUTRAL · SETTLED

## Reconstruction queries
None. All corrections in this batch (NB-184's intermediate slip, NB-185's notational overload,
NB-186's three dimensional slips) are internal notebook-fidelity findings, independently consistent
with standard geometry/algebra once corrected — and the reconstruction's own note that these
are the notebook's literal final, most hastily-written lines ("End of notebook" immediately
follows) is a plausible, unforced explanation for their concentration here.

## Handoff items raised (mirrored into the handoff file)
None this run.

## Contamination log
None in this cross-check session. (The reconstruction file itself documents, in its own header,
that it is a defer-pass re-reconstruction of material a *prior reconstruction session* had
accidentally been exposed to changelog-tail hints about — that contamination event belongs to the
reconstruction pass, is already disclosed and handled there per its own firewall, and does not
carry into this SM cross-check, which read only the clean, independently-reconstructed result.)

## Appendix — search queries used
None — see the contamination log and the "what the field learned" section; every anchor in this
batch reuses ground already researched and cited in the pp.110-124, pp.141-160, and pp.161-175
write-ups.

## Sources
None beyond the reconstruction file; no claims in this run required new citation beyond what
earlier write-ups already established for the same Dirac-equation and null-vector/spinor
foundations.
