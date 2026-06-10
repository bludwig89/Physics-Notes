# FB06 — Positronium levels are exactly half hydrogen

**Tier:** B — quantitative confrontation (de-risk / internal consistency of the two-body reduction)
**Falsification power:** ★★★ (certifies the two-body→relative-coordinate reduction underpinning FB04/FB05)
**Model element under test:** the F125 reduction of the e⁺e⁻ problem to the same 1/r solver with μ=m_e/2.
**Supersedes:** new

## Hypothesis (parameter-free given the reduction)
Because `Ry∝μ` and positronium has `μ=m_e/2`, every level is exactly half the infinite-mass hydrogen value:

  `Ry(Ps)/Ry(H_∞) = 0.5000000000` (to `10⁻⁹`),  ground state `−6.803 eV`,

with its own clean `−1/n²` series.

## Measured target + source
- Measured positronium ground state `−6.8 eV` (`1/4·Ry` ≈ 6.803 eV in the equal-mass reduction).

## Falsification criterion
Falsified if:
1. The ratio departs from exactly `1/2` beyond machine precision (would mean the two-body→relative-coordinate reduction is not faithful, undermining FB04/FB05), **or**
2. The Ps `−1/n²` series fails.

## CASIM build & run
Same 1/r solver, μ=m_e/2.
1. Numerical: solve the relative-coordinate 1/r problem with μ=m_e/2; confirm `Ry(Ps)/Ry(H_∞)=0.5` to 1e-9, ground `−6.803 eV`, `−1/n²` series.

## Pass/fail gate
- PASS: ratio = 1/2 to 1e-9, ground −6.803 eV, clean series.
- FALSIFIED: ratio ≠ 1/2 beyond machine precision.

## Provenance
F125 §A (positronium-first reduction certifies the two-body solve).
