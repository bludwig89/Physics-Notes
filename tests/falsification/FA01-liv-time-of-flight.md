# FA01 — Lorentz-violation time-of-flight scale (the cell's sharpest falsifier)

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★★ (directly kills the adopted lattice spacing `a`)
**Model element under test:** the canonical cell `a = √(8π)·3^(1/4)·ℓ_P = 1.06638×10⁻³⁴ m` (F79/F107) via the F30 even-law photon dispersion.
**Supersedes:** `tests-priority/test_06_QG2_planck_LV.py`

## Hypothesis (parameter-free prediction)
The even-law paired photon (F69) has the exact group-velocity dispersion
`δv_g/c = −k²/54` (F30), giving a quadratic (n=2) time-of-flight energy scale

  `E_QG,2 = √54 · ħc/a = 1.360×10¹⁹ GeV = 1.11 E_P`.

The dispersion is **subluminal** and **quadratic** — there is no linear (n=1) net time-of-flight term (the linear term is chiral/birefringent only, F30), so a linear-order LIV detection would also falsify the model (see FA02).

## Measured target + source
- LHAASO GRB 221009A: `E_QG,2 > 7.0×10¹¹ GeV` (current best one-sided bound on quadratic subluminal LIV).
- Track Fermi-LAT / CTA / LHAASO updates for any **positive** n=2 time-of-flight detection.

## Falsification criterion
The cell dies if **either**:
1. A confirmed subluminal n=2 time-of-flight bound is pushed **above** `1.4×10¹⁹ GeV` (the model sits at 1.36×10¹⁹, so a bound above ~1.4×10¹⁹ excludes it), **or**
2. A confirmed **superluminal** n=2 signal is detected at any scale (model is strictly subluminal), **or**
3. A net **linear** (n=1) time-of-flight effect is detected (model has none — see FA02).

## CASIM build & run
The prediction is an exact closed form; verify it two ways.
1. Symbolic: evaluate `E_QG,2 = √54·ħc/a` at the canonical cell and confirm `1.360×10¹⁹ GeV`; confirm `δv_g/c = −k²/54` from the even law symbolically (sympy, no chiral transforms).
2. Numerical dispersion fit on the live propagator:
```bash
casim run scenarios/photon_pair.yaml --L 64 --ticks 200 \
    --out test-results/FA01_liv_tof.json
casim analyze test-results/FA01_liv_tof.json --table
```
Fit `Ω_pair(k)` at small k; extract the k² coefficient and confirm it equals `−1/54` (the axis-aligned channel is exactly dispersionless per F105 — fit an off-axis ray to see the −k²/54 term). Sandbox L=64 is cheap (<1 s); no production run needed.

## Pass/fail gate
- PASS: `E_QG,2 = 1.360×10¹⁹ GeV` to fit floor AND current best measured bound (7×10¹¹ GeV) is below it.
- FALSIFIED: any of the three criteria above.

## Provenance
F30 (even-law dispersion order), F28 (LHAASO/GRB bound), F105 (axis dispersionless), F112 §C (registry row + falsification threshold), F69 (paired photon).
