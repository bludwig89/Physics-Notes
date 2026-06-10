# FB01 — Charged-lepton spectrum from one anchor + the condensate shape

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (the entire shape is predicted; only the overall scale is calibrated)
**Model element under test:** the E_g condensate equipartition shape (F120/F121), τ-anchored.
**Supersedes:** new

## Hypothesis (mostly predicted, one calibrated scale)
With the scale anchored on the wall-pinned τ (exactly δ-stable, zero anchor error) and the condensate angle δ, the shape predicts the two lighter leptons:

  `m_μ` to `−0.00%`, `m_e` to `−0.06%` (measured angle δ=12.733°).

Only the overall scale N (=m_τ) and the angle λ₆ are inputs; all ratios + Koide (FA05) are predicted.

## Measured target + source
- PDG: `m_e=0.51099895`, `m_μ=105.6583755`, `m_τ=1776.86 MeV`.

## Falsification criterion
Falsified if:
1. With the τ anchor + measured angle, predicted `m_μ`, `m_e` are off by more than the stated ≤0.06%, **or**
2. The first-principles angle (`λ₆=1/4 → δ=13.36°`) gives predictions that diverge by O(1) in a way that cannot be attributed to the known node-sensitivity (electron sits at the condensate node, F120), **or**
3. The same shape fails to also yield Koide `Q=2/3` (FA05) — internal-consistency falsifier.

## CASIM build & run
Closed-form spectrum; verify numerically.
1. Numerical: build the E_g condensate at angle δ, equipartition `A=√2·ȳ`, `m_a=y_a²`, heaviest wall-pinned `m_τ^cond=1`; anchor N on m_τ; read out m_μ, m_e; confirm ≤0.06%.
2. Sensitivity: confirm `|∂ln m_τ/∂δ| < 1e-6` (τ δ-stable) and the electron's ~10× larger node sensitivity (documents why τ not e is the anchor).

## Pass/fail gate
- PASS: τ-anchored m_μ, m_e within ≤0.06% (measured angle) AND Koide Q=2/3 holds.
- FALSIFIED: residuals exceed the stated shape error not attributable to node-sensitivity.

## Provenance
F120 (electron-calibrated spectrum + node lesson), F121 (τ-anchored canonical spectrum — adopted standard output), F93/F101 (condensate angle), F118/F119 (open inputs N and λ₆).
