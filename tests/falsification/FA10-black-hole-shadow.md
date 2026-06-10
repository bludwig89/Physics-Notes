# FA10 — Black-hole shadow is 4.63% larger (horizon-free)

**Tier:** A — sharp falsifier (genuine divergence from GR; the model's boldest strong-field claim)
**Falsification power:** ★★★★ (a measured shadow at the Schwarzschild value 3√3 to <4% precision falsifies the exponential metric)
**Model element under test:** the F114 dielectric black hole — exponential (Yilmaz-type) metric `K=e^(2u)`, horizon-free.
**Supersedes:** new

## Hypothesis (parameter-free prediction)
The canonical exponential metric departs from Schwarzschild in the strong field. The shadow impact parameter is

  `b_c = 2e ≈ 5.437 GM/c²`  vs Schwarzschild `3√3 ≈ 5.196` → **+4.63% larger** shadow,

with throat `R_min = e`, photon sphere `2√e`, throat redshift `1+z = e` (all sympy-exact). There is **no event horizon**: `g_tt = −e^(−2u)` has no finite root.

## Measured target + source
- EHT: M87* and Sgr A* shadow diameters (currently ~10% systematic/measurement uncertainty on the emission ring → shadow size).

## Falsification criterion
Falsified if:
1. A black-hole shadow is measured to be the **Schwarzschild value `3√3`** to better than ~4% precision (the model predicts +4.63%, so a confirmed Schwarzschild-sized shadow at <4% kills the exponential metric), **or**
2. A genuine event horizon / trapping surface is confirmed (e.g. a definitive null result on surface emission / hard-surface echoes that is inconsistent with a frozen horizon-free object would instead support GR over the model — track carefully).

## CASIM build & run
Strong-field eikonal; closed forms are sympy-exact.
```bash
casim run scenarios/dielectric_black_hole.yaml --L 64 \
    --out test-results/FA10_shadow.json
```
- Symbolic: confirm `b_c=2e`, photon sphere `2√e`, throat `e`, redshift `1+z=e`, and that `g_tt=−e^(−2u)` has no finite root (sympy).
- Quantitative: convert `b_c=2e` to μas for M87*/Sgr A* using measured M, D; compare to EHT ring diameters with their error bars.

## Pass/fail gate
- PASS: model `b_c=2e` (+4.63%), consistent with EHT within current uncertainty.
- FALSIFIED: shadow confirmed at Schwarzschild `3√3` to <4%, or a true horizon confirmed.

## Provenance
F114 (dielectric black hole), F64 (canonical K=e^(2u)), F107 (SI lock → μas), F112 §B.
