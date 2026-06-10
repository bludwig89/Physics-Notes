# FA08 — Exactly three fermion generations

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★ (a discovered 4th generation kills the selection rule)
**Model element under test:** BCC point-group selection of the F27 chiral mass step giving exactly three stable orbital-shell irreps (F75).
**Supersedes:** new

## Hypothesis (structural prediction)
The BCC point group admits **exactly three** independent, stable irreps that can carry the F27 chiral mass step → exactly three fermion generations with identical gauge quantum numbers. The group theory is exact; the physical identification (generation index = orbital-shell irrep) is a stated hypothesis (F75 §7).

## Measured target + source
- PDG / LEP: invisible Z width gives `N_ν = 2.984 ± 0.008` light active neutrinos → 3 generations. No 4th-generation fermion observed.

## Falsification criterion
Falsified if:
1. A 4th-generation chiral fermion (quark or charged lepton) is discovered, **or**
2. A 4th light active neutrino is confirmed (sterile-neutrino anomalies do not count unless confirmed as a 4th active generation), **or**
3. The group-theory multiplicity is shown to permit a number other than three stable mass-carrying irreps.

## CASIM build & run
Group-theory selection; verify symbolically.
1. Symbolic: rebuild the BCC point-group character table from generators (integer-orthonormal cross-check), count the stable irreps compatible with the F27 chiral mass step and the F38 anomaly-cancellation quantum numbers; confirm the multiplicity is exactly 3.
2. Confirm consistency with LEP `N_ν ≈ 3`.

## Pass/fail gate
- PASS: exactly three stable mass-carrying irreps AND no 4th generation observed.
- FALSIFIED: any of the three criteria above.

## Provenance
F75 (three generations from BCC irrep selection), F76 (generation hierarchy crystal-field), F84 (flatness/orthorhombic break), F38 (anomaly cancellation), F27 (chiral mass step).
