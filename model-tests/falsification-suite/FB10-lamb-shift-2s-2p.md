# FB10 — Lamb shift boundary: 2s₁/₂ == 2p₁/₂ at Dirac order

**Tier:** B — quantitative confrontation (marks the QED/QFT boundary)
**Falsification power:** ★★★ (a clean statement of what the model does NOT yet predict — the Lamb shift is QED-loop, beyond the current Dirac sector)
**Model element under test:** the F125 Dirac-level 2s–2p degeneracy and the explicit QED-4 boundary.
**Supersedes:** new

## Hypothesis (boundary statement)
At Dirac (one-particle relativistic) order the model gives the exact degeneracy

  `2s₁/₂ == 2p₁/₂` (machine precision),

so the measured `2s₁/₂−2p₁/₂` Lamb shift (1057 MHz) is **explicitly a QED radiative (vacuum-polarization + self-energy) effect the current sector does not contain**. This is an honesty/boundary test: it asserts where the matter sector stops, so a claim to predict the Lamb shift without a loop sector would be the falsifier.

## Measured target + source
- Measured Lamb shift `2s₁/₂−2p₁/₂ ≈ 1057.8 MHz` (QED).

## Falsification criterion
Falsified / flagged if:
1. The Dirac sector does NOT give exact `2s₁/₂==2p₁/₂` (would mean a spurious splitting — internal error), **or**
2. The model is claimed to reproduce the 1057 MHz Lamb shift without an explicit QED loop sector (over-claim) — this test exists to prevent that.

## CASIM build & run
Dirac degeneracy check (the boundary).
1. Numerical: from the FB05 radial-Dirac solve, confirm `2s₁/₂` and `2p₁/₂` are degenerate to machine precision.
2. Document explicitly: the residual measured 1057 MHz is QED-loop physics (vacuum polarization + self-energy), outside the current sector — a future roadmap item, not a present prediction.

## Pass/fail gate
- PASS: Dirac `2s₁/₂==2p₁/₂` exact AND the Lamb shift is correctly flagged QED-beyond-sector.
- FALSIFIED: spurious Dirac-level splitting, or an over-claim to predict the Lamb shift.

## Provenance
F125 §I (2s₁/₂==2p₁/₂ exact; Lamb = QED/QFT-4 boundary).
