---
id: CL274
title: The model has no dimension-5 Lorentz-violating photon operator, and the dimension-6 coefficient is the exact rational -[(1-sum n^4)/144 + (nx ny nz)^2/24]
slug: no-dimension-5-photon-operator
tier: headline
kind: prediction
status: live
domain: [QFT, SR]
exactness: exact
findings: [F319, F69, F67, F301, F26]
tests: [F319-uv-completion]
modules: [casim.engine.interactions.qed_uv_completion, casim.engine.gauge.photon]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: CL273
falsifier: stated
first_issued: 2026-08-16
last_verified: 2026-08-16
provenance: authored
review_state: authored
confidence: high
---

# CL274 — No dimension-5 photon operator; the dimension-6 coefficient is exact

## Statement

For the paired-spinor photon (F69), the deviation of the dispersion from linearity is

$$\frac{\Omega_\text{pair}(k)-c_\text{lat}\lvert k\rvert}{c_\text{lat}\lvert k\rvert}
= -\Big[\frac{1-\sum_i\hat n_i^4}{144}+\frac{\hat n_x^2\hat n_y^2\hat n_z^2}{24}\Big]\lvert k\rvert^{2}+O(\lvert k\rvert^{4}),$$

verified against the F26 BCC symbol to $1.1\times10^{-20}$ over nine directions in 60-digit
arithmetic. There is **no $O(\lvert k\rvert)$ term at all** — the leading Lorentz-violating
operator is dimension-6, not dimension-5 — established by measuring the scaling exponent
$p=2$ to better than $10^{-4}$ rather than by bounding a coefficient. The dimension-6
coefficient's range over directions is exactly $[-\tfrac1{162},\,0]$: $-1/162$ along
$\langle111\rangle$, and identically zero along $\langle100\rangle$, where the dispersion is
linear to all orders. At the F107 cell ($\Lambda_\text{UV}=1.8504\times10^{18}$ GeV) the
maximum fractional deviation is $3.0\times10^{-31}$ at 13 TeV and $3.5\times10^{-27}$ at
1.4 PeV.

## What it extends

Lorentz invariance is exact in special relativity and an input to the Standard Model. Every
discrete substrate deforms it, and the standard Lorentz-violation catalogue (Colladay–Kostelecký
style) orders the deformation by operator dimension, with the dimension-5 photon term the
observationally decisive one: GRB and AGN polarimetry bound it near $10^{-30}$, and that same
bound excluded this model's earlier $\sigma$-bilinear photon (F65–F67).

The claim is that the model does not merely *satisfy* that bound but has no such operator:
$\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$ is even in the branch label by construction,
which kills every odd power. The surviving deformation is dimension-6 with a coefficient the
lattice geometry hands over as a rational number — no tuning and no free parameter, which is
what distinguishes this from a Lorentz-violation model that fits its coefficients.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §4 (U5) | the closed form, nine directions, 60 dps | exact ($1.1\times10^{-20}$) |
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §5 (U6) | the decoupling table at $m_e$, $M_Z$, LHC, LHAASO | computed |
| record `F319-uv-completion`, legs `U5-closed-form-exact`, `U5-no-dim5`, `U5-bound-at-111`, `U5-zero-along-100`, `U5-engine-faithful` | 21/21 PASS; control `linear_control` reddens the first three | exact |
| `findings/F301-finite-a-boost-covariance-poincare-defect.md` | the $\langle100\rangle$ all-orders exactness ($3.5\times10^{-46}$), recovered here analytically | exact |
| `findings/F67-even-law-photon-vs-bilinear-mutually-exclusive.md`, `findings/F69-paired-spinor-photon.md` | why the pair rate is helicity-symmetric | exact |

The engine's shipped float64 `pair_dispersion` reproduces the closed form to $1.1\times10^{-7}$;
that residual is `arccos` conditioning at the probe, not physics, and both legs are reported
separately so the distinction stays visible.

## Falsifier

1. **Detection of dimension-5 photon Lorentz violation at any level.** The claim is that the
   operator is absent, not small, so there is no coefficient to shrink. This is the live
   observational falsifier: energy-dependent photon arrival times or birefringence with a linear
   (rather than quadratic) energy dependence.
2. A dispersion measurement contradicting the $O(\lvert k\rvert^2)$ coefficient. Not a
   terrestrial falsifier — it needs $E\sim\Lambda_\text{UV}$ — but recorded because the
   coefficient is a prediction rather than a fit.
3. Any direction with $\lvert\text{coefficient}\rvert>1/162$, which the cubic-invariant
   extremisation forbids.

## Status & history

Issued 2026-08-16 with F319. Supersedes nothing: the $\sigma$-bilinear photon's birefringence
exclusion (F65–F67) is a *different* statement about a *superseded* photon, and this card is
about the one that replaced it. Rolls up to CL273 as the measured instance of that ledger's
"dim $\ge6$ is irrelevant" row — the row is the only one whose coefficient is computed rather
than argued.

## Sources

- `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §4, §5
- `src/casim/engine/interactions/qed_uv_completion.py` (`dispersion_excess_closed_form`, `dispersion_excess_mp`)
- `src/casim/engine/gauge/photon.py` (`pair_dispersion`)
