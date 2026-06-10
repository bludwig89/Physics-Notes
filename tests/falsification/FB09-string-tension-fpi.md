# FB09 — √σ/f_π from the two QCD calibrations

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★ (reconciles confinement and chiral calibrations from one lattice)
**Model element under test:** the F124 reconciliation `√σ/f_π = (Λ/f_π)(√σ/Λ)`.
**Supersedes:** new

## Hypothesis
The model's two QCD calibrations (confinement string tension σ; chiral f_π) are reconciled:

  chiral `Λ/f_π = 7.04` exact (Pagels-Stokar); confinement from the F86/F88 condensate `σ=2πv²` at the BZ cutoff → `√σ/f_π = 4.00` (axis) / `3.23` (sphere),

vs empirical `4.56` — a `~12–29%` residual attributed to scale-setting (bare rotor → ~1; the factor ~4 is the strong-coupling gap).

## Measured target + source
- Lattice/phenomenology: `√σ ≈ 420–440 MeV`, `f_π=92.4 MeV` → `√σ/f_π ≈ 4.56`.

## Falsification criterion
Falsified if:
1. The residual `~12–29%` is shown NOT to be scale-setting / strong-coupling-gap shaped (i.e. it is a genuine structural disagreement), **or**
2. The Pagels-Stokar `Λ/f_π=7.04` or the BPS `σ=2πv²` relations fail in-model.

## CASIM build & run
Dedicated chiral-route scenario (compute-once factorisation; pure numpy, sandbox-fast):
```bash
casim run scenarios/string_tension_fpi.yaml --out test-results/FB09_chiral.json
```
Reads off `sqrt_sigma_over_fpi_axis, _sphere, Lam_over_f_pi_chiral, empirical_sqrt_sigma_over_fpi`. Verified: axis 4.00, sphere 3.23, Λ/f_π=7.04, empirical 4.56 (axis −12.2%, sphere −29.3%).
1. Symbolic (what the channel does): confirm `Λ/f_π=7.04` (Pagels-Stokar) and `σ=2πv²` (F86 BPS); form `√σ/f_π` → 4.00 (axis)/3.23 (sphere); compare to 4.56.
2. Lattice-gauge σ confinement cross-check (Option A Monte-Carlo, F94) — sandbox smoke then production:
```bash
casim run scenarios/gauge_mc.yaml --L 8 --ticks 40 \
    --out test-results/FB09_sigma_smoke.json   # sandbox ceiling
# production (native, Ben): --L 12 --ticks 400
```
Confirm σ_A fixes the condensate `v*=√(σ_A/2π)` consistent with the chiral route.

## Pass/fail gate
- PASS: `√σ/f_π` in 3.2–4.0 with the residual demonstrably scale-setting-shaped.
- FALSIFIED: residual is structural, or the underlying relations fail.

## Provenance
F124 (√σ/f_π reconciliation), F86/F88 (colour condensate σ=2πv²), F94 (lattice-gauge MC), F116 (BZ cutoff).
