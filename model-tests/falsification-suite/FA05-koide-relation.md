# FA05 — Koide relation Q = 2/3

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★★ (one part in 10⁵ agreement, parameter-free)
**Model element under test:** the E_g condensate equipartition geometry that fixes the charged-lepton mass texture (F46/F80/F81).
**Supersedes:** new

## Hypothesis (parameter-free prediction)
The charged-lepton Cooper-pair bilinear sits at the 45° equipartition node, giving the Koide ratio

  `Q = (m_e+m_μ+m_τ) / [ (√m_e+√m_μ+√m_τ)² ] = 2/3 = 0.6666667`,

as a geometric (cubic-vector) consequence of the condensate, not a fit.

## Measured target + source
- PDG lepton masses: `m_e=0.51099895 MeV`, `m_μ=105.6583755 MeV`, `m_τ=1776.86 MeV` → measured `Q = 0.666661`.

## Falsification criterion
Falsified if:
1. Improved τ-mass measurement moves measured `Q` away from `2/3` beyond the model's stated structure (currently 1×10⁻⁵ from 2/3), **or**
2. The `√m` (Cooper-pair amplitude) basis is shown to be physically untenable, breaking the derivation.

## CASIM build & run
Closed-form geometric prediction; verify symbolically + numerically.
1. Symbolic (sympy): show the E_g condensate at equipartition (`A=√2·ȳ`, `m_a=y_a²`) yields `Q=2/3` exactly; show the angle dependence cancels (Koide is angle-independent).
2. Numerical: plug PDG masses into the Koide formula, confirm `0.666661`; confirm model `0.6666667` agrees to `1×10⁻⁵`.

## Pass/fail gate
- PASS: model `Q=2/3` and PDG masses give `0.666661` (within 1×10⁻⁵).
- FALSIFIED: measured Q drifts off 2/3 beyond the model's geometry.

## Provenance
F46 (Pythagorean lattice mass), F76 (Koide as cubic-vector signature), F78 (why √m), F80/F81/F82 (45° equipartition / saturation), F112 §D.
