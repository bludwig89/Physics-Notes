# FC01 — Mercury perihelion precession (GR-4)

**Tier:** C — consistency regression (the model is GR-identical at PPN order; this is a check, not a prediction)
**Falsification power:** ★★★ (a departure from 42.98″/century would break the dielectric's β=γ=1)
**Model element under test:** timelike geodesics of the F64 dielectric metric.
**Supersedes:** `tests-priority/test_09_GR4_mercury.py`

## Hypothesis (GR-identical)
The canonical dielectric reproduces the GR perihelion advance

  `Δω = 6πGM/[a(1−e²)c²] = 42.98″/century` for Mercury (PPN β=γ=1).

## Measured target + source
- Observed anomalous precession `43.0″/century`.

## Falsification criterion
Falsified if the dielectric geodesic gives a perihelion advance differing from the GR value beyond ~1% (a confirmed `β≠1` or `γ≠1` would do it — links to FA03).

## CASIM build & run
Leapfrog geodesic of the effective metric (test the metric ansatz, not the FFT-Poisson kernel; PBC handled in FC02/FC04).
1. Integrate timelike geodesics on `ds²=−(1+2φ/c²)c²dt²+(1−2φ/c²)δ_ij dx^i dx^j` (the canonical K=e^(2u) at O(φ/c²)); extract Δω per orbit; confirm `6πGM/[a(1−e²)c²]` to ≤5%.
2. Cross-check the exact exponential metric gives the same O(u) precession (strong-field departure is a separate item, FA10).

## Pass/fail gate
- PASS: Δω within 5% of `6πGM/[a(1−e²)c²]`.
- FALSIFIED: departure from GR precession beyond precision.

## Provenance
F64 (dielectric PPN β=γ=1), F16 (GR-3/GR-4 fork — Mercury the discriminator), F112 §B (CONSISTENCY).
