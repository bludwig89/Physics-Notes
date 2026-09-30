# Notebook × SM Cross-Check — pp. 51–56: Harmonic-Oscillator Structure, 45° Rotation Trick,
# Even/Odd Mode Decomposition

*2026-09-22 - 22:15 · checks `notebook-reconstruction-05-harmonic-oscillator-modes.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.51 | 51 | NEUTRAL | SETTLED | Mode-inverse relations and their wavefunction interpretation — internal operator-algebra bookkeeping, no independent SM/GR claim. |
| pp.52 | 52 | NEUTRAL | SETTLED | The 45° coordinate-rotation trick diagonalizing a toy coupled oscillator — a mathematical technique, not a physical prediction. |
| pp.53 | 53 | REINFORCES | SETTLED | Bose symmetrization mechanics (commuting ladder operators enforce exchange symmetry) is genuine, standard, SM-relevant QFT content. |
| pp.54 | 54 | NEUTRAL | SETTLED | A real algebra error (wrong reality condition) was found and corrected by the reconstruction; purely internal notebook arithmetic, no external anchor. |
| pp.55 | 55 | NEUTRAL | SETTLED | Open question about dropping the antisymmetric sector, plus an ink-damaged partial computation — internal bookkeeping, no independent SM/GR claim. |
| pp.56 | 56 | NEUTRAL | SETTLED | $\alpha,\beta$ mode-mixing algebra and its parity-based cross-term cancellation — internal operator algebra. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from what the pp.1-2 and pp.41-49 cross-checks already cover for the same
underlying free-scalar-field/Fock-space foundations. This batch is almost entirely internal
operator-algebra manipulation of a specific mode-mixing convention the notebook is working out for
itself (analogous to batch 02's trace-derivative lemmas, or batch 01's Fourier-convention scratch
work) rather than claims that touch a distinct external SM/GR anchor. The one build with a genuine
standalone physical anchor (NB-067, Bose symmetrization) rests on the spin-statistics connection
for bosons, itself unchanged textbook physics with no post-2007 revision.

## Per-build verdicts

### NB-062 (p.51) — Cross-Indexed Mode Inverse Relations
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** none in SM/GR terms — a self-consistency check of a particular
  (cross-indexed) convention for inverting field/momentum modes into ladder operators.
- **Anchor:** none (bookkeeping/convention, not a physical claim; protocol §4a: no anchor → NEUTRAL).
- **Verdict:** NEUTRAL · SETTLED

### NB-063, NB-064 (p.51) — Wavefunction Interpretation; Self-Critique
- **Checked against:** reconstruction status `NOT-TESTABLE` / `SOLID`
- **Claim (field terms):** interpretive statements about the multi-mode wavefunction; a correct
  observation that $a_k^+a_k$ is not a simple single-oscillator number operator in this
  cross-mode setting.
- **Anchor:** none distinct from NB-062.
- **Verdict:** NEUTRAL · SETTLED

### NB-065, NB-066 (p.52) — 45° Rotation Diagonalizing a Toy Coupled Oscillator
- **Checked against:** reconstruction status `SOLID` (central qualitative claim exactly confirmed;
  a coordinate-labeling discrepancy noted, not a physics error)
- **Claim (field terms):** none in SM/GR terms — a coordinate-rotation technique diagonalizing a
  specific bilinear ($xy$-coupled) toy Hamiltonian into one positive and one negative harmonic
  oscillator.
- **Anchor:** none — this is a mathematical diagonalization trick applied to a toy model, not
  itself a claim about a physical system.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a. (Note: an inverted/negative harmonic oscillator is loosely reminiscent of
  "ghost" degrees of freedom that appear in gauge-fixed quantization, but the notebook's toy model
  here is a generic coupled-oscillator exercise, not a gauge-fixing construction — not claimed as a
  connection.)

### NB-067 (p.53) — Bose Symmetrization Mechanics
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the symmetrization operator $S=\tfrac1{N!}\sum_PP$ and the fact that
  commuting creation operators automatically enforce Bose exchange symmetry on multi-particle
  states.
- **Anchor:** foundations — the operator-algebra mechanism underlying Bose–Einstein statistics for
  identical integer-spin particles, standard and load-bearing throughout the SM (photons, gluons,
  W/Z, Higgs are all bosons obeying exactly this exchange symmetry).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — unchanged, standard since the 1920s (Bose, Einstein, Dirac, Jordan).

### NB-068, NB-069 (p.54) — Reality Condition (Corrected)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
- **Claim (field terms):** none in SM/GR terms — an internal notebook arithmetic error (the
  claimed reality condition $\phi_k=\phi_{-k}$ is wrong; the correct standard condition
  $\phi_{-k}=\phi_k^*$ is what the notebook's own formulas actually give) confirmed numerically by
  the reconstruction on an explicit asymmetric test function.
- **Anchor:** none — this is a self-consistency/arithmetic question about a specific field's
  Fourier coefficients, not an independent SM/GR-testable claim (the *correct* condition,
  $\phi_{-k}=\phi_k^*$, is of course standard, but the error itself has no external physics content
  to grade against).
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-070 (p.55) — $H$ in $\alpha,\beta$ Operators
- **Checked against:** reconstruction status `SOLID` (by structural analogy to NB-073)
- **Claim (field terms):** none in SM/GR terms — algebraic substitution mechanics.
- **Anchor:** none.
- **Verdict:** NEUTRAL · SETTLED

### NB-071 (p.55) — Open Question: Can the Antisymmetric ($\beta$) Sector Be Dropped?
- **Checked against:** reconstruction status `NOT-TESTABLE` (genuinely still open; one candidate
  route to an easy "yes," resting on NB-068/069's incorrect claim, is closed off)
- **Claim (field terms):** an open question posed by the author, not a claim.
- **Anchor:** none identifiable from the page — no specific physical distinction between the
  sectors is proposed that could be checked against external physics.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a — still an open notebook question, not something external physics resolves as
  posed (too underspecified to anchor to a named SM structure).

### NB-072 (p.55) — Ink-Blot-Damaged Commutator Computation
- **Checked against:** reconstruction status `NEEDS-WORK` (unrecoverable due to physical page
  damage, not a physics or reconstruction gap)
- **Claim (field terms):** none recoverable.
- **Anchor:** none.
- **Verdict:** NEUTRAL · SETTLED

### NB-073, NB-074 (p.56) — $\alpha,\beta$ Mixing Ansatz; Parity Cancellation of the Cross Term
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** none in SM/GR terms — operator-algebra expansion, and the standard
  elementary fact that an odd-under-$k\to-k$ integrand vanishes when integrated over a symmetric
  domain.
- **Anchor:** none — the parity-vanishing argument used is elementary calculus (the same principle
  as $\int_{-L}^L k\,dk=0$), not a distinct SM/GR structural fact.
- **Verdict:** NEUTRAL · SETTLED

## Reconstruction queries
None.

## Handoff items raised (mirrored into the handoff file)
None this run.

## Contamination log
None. This run drew only on the reconstruction file; nearly all builds in this batch are internal
operator algebra with no external SM/GR anchor, so no new searches were needed beyond confirming
that assessment (recorded below).

## Appendix — search queries used
None. Every build in this batch either has no SM/GR anchor (protocol §4a routes these straight to
NEUTRAL without requiring a search) or (NB-067) rests on unchanged, pre-2007 textbook physics
already covered in the pp.1-2 write-up's treatment of the same foundations.

## Sources
None beyond the reconstruction file itself; no external claims were made in this run requiring citation.
