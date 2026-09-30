# Notebook × SM Cross-Check — pp. 161–175: "Maxwell Equations from Spinor" (Full Derivation)

*2026-09-23 - 00:45 · checks `notebook-reconstruction-14-maxwell-from-spinor.md` (the
reconstruction's own standing contamination-log flag on this page range — extra scrutiny warranted
as the notebook's most complete Maxwell-from-Weyl attempt — is noted; this cross-check found no
model-internal content in the reconstruction file itself for this batch, so no contamination
occurred here) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-23, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.161-175 | 161–175 | REINFORCES | SETTLED | The notebook's most complete attempt at deriving Maxwell-like equations from a Weyl-quaternion equation is confirmed algebraically exhaustive and correct; the resulting system is a genuine, self-consistent single-real-vector-field subsystem, explicitly narrower than (not equivalent to, and not in conflict with) the real two-field vacuum Maxwell system — including a "striking" result (only longitudinal, not transverse, waves are allowed) that is exactly correct for this specific simpler construction and does not contradict real transverse light once the two constructions are properly distinguished. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from the classical-electrodynamics foundations already covered in the pp.92-101
(Riemann-Silberstein) and pp.127-140 write-ups. This batch's central external-physics question —
does this construction reproduce real vacuum Maxwell theory — has a fixed, unchanging answer
(partially: it reproduces a genuine but simpler curl-free subsystem, not the full two-field
theory), settled by the mathematics itself rather than by anything the field learned post-2007.

## Per-build verdicts

### NB-171, NB-172 (p.161–162) — Weyl-Quaternion Matrix Product; Real/Imaginary Split
- **Checked against:** reconstruction status `SOLID` (both; an uncleaned scratch-line artifact in
  an intermediate, non-load-bearing line noted for NB-172)
- **Claim / anchor:** none independently — intermediate matrix-algebra steps feeding into NB-173's
  central claim, below.
- **Verdict:** NEUTRAL · SETTLED

### NB-173 (pp.162–163) — Central Claim: Weyl-Quaternion Equation Reduces to a Maxwell-Curl-Shaped
### System
- **Checked against:** reconstruction status `SOLID` (confirmed exhaustively — all 8 real scalar
  equations the full matrix product actually produces were checked, not just the ones the page
  happens to display, with the redundant 8th equation correctly explained by the Hermitian
  matrix's 4 real independent components)
- **Claim (field terms):** the Weyl-quaternion equation $(\sigma^\mu\partial_\mu)(\sigma^\mu
  V_\mu)=0$, for a single real vector field $V_\mu=(V_0,\vec V)$, reduces exactly to
  $\partial_0\vec V=-\nabla V_0$, $\nabla\times\vec V=0$, $\vec\nabla\cdot\vec V=-\partial_0V_0$.
- **Anchor:** classical electrodynamics — is this a genuine derivation of (some or all of) vacuum
  Maxwell's equations from a spinor/Weyl construction? The reconstruction's own honest physical
  caveat, independently confirmed here: this uses a *single* real 3-vector with a scalar partner,
  not the genuine two-independent-3-vector $(E,B)$ field-strength structure of real
  electromagnetism, so it is a related but strictly narrower mathematical object than full vacuum
  Maxwell theory (the notebook's own "Maxwell-like... to be sure" hedge is accurate, not an
  overclaim).
- **Verdict:** REINFORCES · SETTLED (a non-standard route to a genuine, self-consistent
  mathematical subsystem, correctly and honestly characterized by both the notebook and the
  reconstruction as narrower than full Maxwell theory — not a claim that conflicts with real EM,
  since it does not claim to reproduce all of it)
- **Hindsight:** none — the distinction between this single-field construction and the true
  two-field Maxwell system is a matter of counting degrees of freedom, unaffected by anything
  learned since 2007.

### NB-174, NB-176 (pp.163–164) — Wave-Equation Consequences
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the boxed system implies the standard wave equation
  $\partial_0^2\vec V=\nabla^2\vec V$ (and the analogous scalar equation for $V_0$), via the
  standard vector identity $\nabla(\nabla\cdot\vec V)=\nabla^2\vec V+\nabla\times(\nabla\times\vec
  V)$.
- **Anchor:** foundations — standard vector calculus and wave-equation derivation, unchanged.
- **Verdict:** REINFORCES · SETTLED

### NB-175 (p.164) — Plane-Wave Ansatz Forces $k=\omega$, Not $k=-\omega$
- **Checked against:** reconstruction status `SOLID` (the actual distinguishing mechanism — the
  wave's amplitude, not its dispersion relation, which is sign-symmetric and cannot by itself
  distinguish the two — correctly identified by the reconstruction)
- **Claim (field terms):** for a specific plane-wave ansatz, self-consistency of the boxed system
  selects $k=+\omega$, not $k=-\omega$, via the amplitude relation, not the (sign-symmetric)
  dispersion relation alone.
- **Anchor:** foundations — a correct, if subtle, point about how a linear system's amplitude
  relations can carry more information than its dispersion relation alone.
- **Verdict:** REINFORCES · SETTLED

### NB-177 (pp.166–167) — Null-Vector Special Case (Root Cause of a Tangled Passage Found)
- **Checked against:** reconstruction status `NEEDS-WORK` (a previously-flagged "tangled" passage
  traced to a precise root cause: an invalid over-generalized chain-rule shortcut,
  $\nabla V_0=\vec V/V_0$, that only holds when each vector component depends solely on its own
  matching coordinate — not a general identity)
- **Claim / anchor:** none survives as a checkable external claim beyond the general vector-calculus
  fact that the shortcut used is not generically valid — a math error, not a physics dispute.
- **Verdict:** NEUTRAL · SETTLED

### NB-178 (pp.167–168) — Transverse Waves Excluded; Only Longitudinal Allowed
### (Confirmed, and Resolved as Not Actually in Tension With Real EM)
- **Checked against:** reconstruction status `SOLID` (upgraded from a Phase-0 provisional
  NEEDS-WORK that had flagged this as "striking, contradicts a transverse EM photon, needs careful
  checking" — the reconstruction confirms the result exactly and resolves the apparent tension)
- **Claim (field terms):** the boxed system's curl-free condition $\nabla\times\vec V=0$ genuinely
  excludes a pure transverse plane wave and forces a longitudinal one instead.
- **Anchor:** classical electrodynamics — real vacuum light is strictly transverse (a direct,
  extremely well-tested consequence of Maxwell's equations, confirmed in every optics/radio
  experiment ever done). Does this build's "longitudinal, not transverse" result contradict that?
- **Current status:** no. As NB-173 already establishes, this construction is a single-real-vector
  subsystem, not the genuine two-field $(E,B)$ Maxwell theory — real transverse light requires the
  coupled two-field structure ($\nabla\times E=-\partial_tB$, not $\nabla\times\vec V=0$), which
  this simpler model does not have. The longitudinal-only result is an accurate, self-contained
  consequence of the specific (simpler, single-field) system actually built, not a claim about real
  light, and the notebook's own text does not claim otherwise.
- **Verdict:** REINFORCES · SETTLED (correct math, correctly scoped; explicitly does **not**
  conflict with the well-established transversality of real EM waves, because it is not a claim
  about the same physical system)
- **Hindsight:** transverse electromagnetic waves remain as thoroughly confirmed today as in 2007
  (radio, optics, every photon-polarization experiment); nothing here bears on that fact one way or
  the other, once the two constructions (this notebook's single-field model vs. real two-field EM)
  are correctly distinguished — which both the notebook's own hedged language and the
  reconstruction's analysis already do correctly.

### NB-179 (pp.168–175) — General-Radius Stereographic Summary (Cleanest Confirmed Stretch)
- **Checked against:** reconstruction status `SOLID` in full (every equation checked; notably, this
  restatement's own formulas do not repeat the dimensional error found in the batch-11 version of
  the same material, and explicitly state the scale-invariance point batch 11 had to infer)
- **Claim / anchor:** none beyond the null-vector/spinor and stereographic-projection foundations
  already established at NB-143-153 (pp.110-124 cross-check) and NB-165-170 (pp.141-160
  cross-check).
- **Verdict:** REINFORCES · SETTLED (consistent with, and the cleanest confirmation of, material
  already graded REINFORCES/IMPROVES in those earlier write-ups)

## Reconstruction queries
None. The reconstruction's own resolution of NB-177 (root-cause diagnosis) and NB-178 (apparent
tension with real EM resolved) are both independently confirmed correct by this cross-check's read
of the underlying vector calculus and electrodynamics.

## Handoff items raised (mirrored into the handoff file)
None new this run — the reconstruction's own correlation-queue note (that this batch's single-field
construction and NB-129's two-field Riemann-Silberstein construction are two distinct 2007
constructions, not to be conflated) is already recorded there and does not need duplication here.

## Contamination log
None. Despite this page range carrying the reconstruction's own standing contamination-log flag
(extra scrutiny warranted as the most complete Maxwell-from-Weyl attempt in the notebook), no
model-internal content was found in this batch's reconstruction file — unlike the pp.103-109 batch,
this file's own correlation-queue section discusses only the notebook's internal constructions
(this batch's single-field system vs. NB-129's two-field one) without naming any specific
model decision, finding, or file. Nothing was excluded from consideration on that basis.

## Appendix — search queries used
None — see the contamination log; every anchor in this batch (Maxwell/vector-calculus foundations,
null-vector/spinor correspondence) reuses ground already researched and cited in the pp.92-101,
pp.110-124, and pp.141-160 write-ups.

## Sources
Carried over from `notebook-sm-crosscheck-pp092-101-lepton-table-rotation-spin1.md`: [The role of the Riemann-Silberstein vector in classical and quantum theories of electromagnetism (*J. Phys. A* 46, 053001, 2013)](https://iopscience.iop.org/article/10.1088/1751-8113/46/5/053001) [B]
