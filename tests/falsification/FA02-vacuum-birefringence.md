# FA02 — Vacuum birefringence is exactly zero

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★★ (any detection excludes the even-law paired photon, the model's chosen photon)
**Model element under test:** the F69 paired/even-law photon as THE electromagnetic photon (supersedes the σ-bilinear photon).
**Supersedes:** new (no tests-priority equivalent)

## Hypothesis (parameter-free prediction)
Because the physical photon is the chirality-**even** paired-spinor object (F67/F68/F69), the two polarisations share one dispersion branch: vacuum birefringence parameter

  `η = 0` exactly, at any lattice spacing `a`.

This is a hard structural prediction, not a small number — the excluded σ-bilinear counterfactual (F65/F66) would instead give linear, Planck-suppressed birefringence that polarimetry already rules out.

## Measured target + source
- Optical/X-ray/γ-ray polarimetry of distant AGN and GRBs: linear vacuum birefringence `η < ~10⁻¹⁵` (and tightening). No detection to date.

## Falsification criterion
**Any** confirmed detection of vacuum birefringence (energy-dependent rotation of the polarization plane / helicity-dependent dispersion) at any level excludes the even-law photon and forces the model back onto the already-excluded σ-bilinear branch — i.e. it falsifies the photon sector as currently constructed.

## CASIM build & run
Structural; verify the two polarisations are degenerate on the live propagator.
```bash
casim run scenarios/photon_pair.yaml --L 128 --ticks 2000 \
    --out test-results/FA02_birefringence.json
```
Initialise both helicity states, propagate, and confirm their dispersion relations `Ω₊(k)` and `Ω₋(k)` coincide to machine precision (`max|Ω₊−Ω₋| < 1e-13`). Cross-check symbolically that the even-law rotation step `ca_wmu._f26_rotation_step` is helicity-blind. Contrast with the σ-bilinear channel (`ca_maxwell.py`) which must show the split (regression that the right object was retired).

## Pass/fail gate
- PASS: `|Ω₊−Ω₋| < 1e-13` for all k AND no measured birefringence detection exists.
- FALSIFIED: a confirmed birefringence detection at any frontier.

## Provenance
F65 (helicity↔branch map), F66 (all-sky anisotropy no rescue), F67 (even vs bilinear mutually exclusive), F68 (minimal coupling forces even), F69 (paired photon), F112 §C.
