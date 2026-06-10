# FB05 — Hydrogen fine structure (Dirac) 2p₃/₂−2p₁/₂ = 10.95 GHz

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (the α⁴ fine-structure law from a hand-rolled Dirac integrator)
**Model element under test:** the F125 radial-Dirac fine structure (Sommerfeld == series == numerical Dirac).
**Supersedes:** new

## Hypothesis (one EM input α)
The relativistic radial-Dirac solve gives:

  `2p₃/₂ − 2p₁/₂ = 45.28 μeV = 10.95 GHz` (measured ≈10.969 GHz, `0.18%`),

absolute scaling `∝α⁴` (fitted slope 4.0001), relative-to-binding `∝α²` (slope 2.0000). `1s₁/₂` at `−13.605874 eV` (CODATA Ry 13.605693 + the O(α⁴) Dirac shift). Sommerfeld formula matches its own `O((Zα)⁴)` series to `5×10⁻¹⁰` and a hand-rolled RK4 numerical Dirac integrator to `≤1.3×10⁻⁶`.

## Measured target + source
- Measured H 2p fine-structure splitting `≈10.969 GHz`; CODATA Rydberg.

## Falsification criterion
Falsified if:
1. The fine-structure splitting departs from `~10.95 GHz` beyond the stated 0.18% (i.e. the α⁴ law fails), **or**
2. The numerical Dirac integrator disagrees with the Sommerfeld closed form beyond ~1e-6 (internal-consistency falsifier), **or**
3. The α-scaling slopes depart from 4 (absolute) / 2 (relative).

## CASIM build & run
Hand-rolled numerical radial Dirac (RK4, inward+outward Wronskian matching of G,F components — do NOT rely on scipy for the chiral/Dirac pieces, per CLAUDE.md).
1. Numerical: integrate the radial Dirac equation for `1s₁/₂`, `2p₁/₂`, `2p₃/₂`; compute the splitting; confirm `10.95 GHz` and ≤1.3e-6 agreement with Sommerfeld.
2. Scaling: vary α, fit absolute slope (→4.0001) and relative slope (→2.0000).
3. Confirm `1s₁/₂ = −13.605874 eV`.

## Pass/fail gate
- PASS: splitting `10.95 GHz` (0.18% of measured), α⁴/α² slopes, Dirac==Sommerfeld to 1e-6.
- FALSIFIED: any of the three criteria above.

## Provenance
F125 §F/G/H (Sommerfeld == series == numerical Dirac; fine-structure law).
