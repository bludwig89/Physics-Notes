# FC04 — Light deflection, dynamical open-BC (GR-1)

**Tier:** C — consistency regression
**Falsification power:** ★★★ (the propagating-wave companion to FA09's eikonal)
**Model element under test:** dynamical photon propagation through the F64 dielectric (vs the FA09 static eikonal).
**Supersedes:** `tests-priority/test_01_GR1_light_deflection.py`, `test_01b_GR1_openBC.py`

## Hypothesis (GR-identical)
A propagating photon wavepacket bends by the GR value

  `Δφ = 4GM/(bc²)` (γ=1), absolute solar `1.7510″`,

with the **open-boundary** Poisson kernel removing PBC artefacts (the test_01b fix).

## Measured target + source
- VLBI solar deflection `1.7510″`.

## Falsification criterion
Falsified if the dynamical deflection departs from `4GM/(bc²)` beyond grid floor, OR if it disagrees with the FA09 static eikonal (internal consistency: static and dynamical must match).

## CASIM build & run
Propagate a photon-pair wavepacket past the open-BC dielectric well.
```bash
casim run scenarios/gravity_deflection.yaml --L 128 \
    --out test-results/FC04_deflection_dyn.json
```
1. Use open-BC Poisson (supersedes test_01b); measure the wavepacket's angular deflection; confirm `4GM/(bc²)` and agreement with FA09's eikonal `K_bend=−4`.

## Pass/fail gate
- PASS: dynamical deflection = `4GM/(bc²)` (1.7510″), matches FA09 eikonal.
- FALSIFIED: departure beyond grid floor, or static/dynamical mismatch.

## Provenance
F64 (D-EM5 bending), F107 (L4 absolute lensing), F112 §B, open-BC Poisson solver. Companion to FA09.
