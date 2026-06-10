# FC02 — Shapiro time delay (GR-2)

**Tier:** C — consistency regression
**Falsification power:** ★★★ (probes γ=1 in the time sector)
**Model element under test:** null propagation through the F64 dielectric (variable local light speed).
**Supersedes:** `tests-priority/test_05_GR2_shapiro.py`, `test_05b_GR2_openBC.py`

## Hypothesis (GR-identical)
Signals crossing the dielectric well accrue the GR Shapiro delay

  `Δt = (2GM/c³)·ln[(r₁+r₂+R)/(r₁+r₂−R)]` (PPN γ=1).

## Measured target + source
- Cassini: `(1+γ)/2 = 1.000021 ± 0.000023` → γ=1 to 2.3×10⁻⁵.

## Falsification criterion
Falsified if the model delay departs from the GR form (i.e. effective `γ≠1`) beyond Cassini precision.

## CASIM build & run
Null geodesic / eikonal time-of-flight on the open-BC dielectric.
```bash
casim run scenarios/gravity_deflection.yaml --L 64 \
    --out test-results/FC02_shapiro.json
```
1. Use the **open-boundary** Poisson kernel (supersedes test_05b) to avoid PBC artefacts; integrate null time-of-flight past the mass; confirm the logarithmic Shapiro form with γ=1 to grid floor.

## Pass/fail gate
- PASS: delay matches GR Shapiro form, effective γ=1 within grid floor.
- FALSIFIED: effective γ≠1 beyond Cassini.

## Provenance
F64 (D-EM9 PPN γ=1), F112 §B (CONSISTENCY), open-BC Poisson solver (next-steps GR-2 rerun).
