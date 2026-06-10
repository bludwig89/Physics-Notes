# FA09 — Light-bending coefficient = −4 and absolute solar deflection

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★ (exact at all field strengths; absolute deflection inherits the G residual)
**Model element under test:** the F64 dielectric eikonal bending of the canonical `K=e^(2u)` metric.
**Supersedes:** `tests-priority/test_01_GR1_light_deflection.py`, `test_01b_GR1_openBC.py`

## Hypothesis (parameter-free prediction)
The canonical dielectric gives the light-bending coefficient

  `K_bend = −4` exactly, for **all** field strengths (sympy zero residual, F112),

so the absolute solar light deflection is

  `Δφ = 4GM_⊙/(R_⊙c²) = 1.751190″`,

inheriting the F79 G-residual of `3.0×10⁻⁸` (M_⊙ from the G-independent product GM_⊙).

## Measured target + source
- VLBI / GR: solar limb deflection `1.7510″` (and `γ` from Cassini `|γ−1|<2.3×10⁻⁵`).

## Falsification criterion
Falsified if:
1. The measured deflection coefficient departs from `−4` (i.e. `γ≠1`) beyond current precision, **or**
2. The model's eikonal integral fails to give exactly `−4` at higher field strength (it shouldn't — `ln K=2u` is exactly Coulombic), exposing a strong-field departure where GR is confirmed.

## CASIM build & run
Eikonal on the dielectric.
```bash
casim run scenarios/gravity_deflection.yaml --L 64 \
    --out test-results/FA09_deflection.json
casim analyze test-results/FA09_deflection.json --table
```
- Symbolic: confirm the eikonal bending integral on `K=e^(2u)` gives `K_bend=−4` exactly at all `u` (sympy).
- Numerical: confirm absolute solar deflection `1.751190″` at the canonical cell.
- Open-BC Poisson cross-check (supersedes test_01b): confirm no PBC artefact.

## Pass/fail gate
- PASS: `K_bend=−4` exact AND absolute `1.751190″` within the G-residual of VLBI.
- FALSIFIED: measured coefficient ≠ −4 beyond precision, or strong-field departure where GR holds.

## Provenance
F64 (D-EM5 bending, D-EM9 PPN), F107 (L4 absolute lensing / canonical a), F112 §B, F114 (strong-field departure begins only at the photon sphere → FA10).
