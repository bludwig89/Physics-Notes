# F28 — GRB / AGN dispersion test of F26 photon rotation prediction

**Date:** 2026-05-23 — 16:35
**Script:** `model-tests/test_F28_grb_dispersion.py`
**JSON:** `test-results/F28_grb_dispersion.json`

## Prediction tested

F26 — the $(\mathbf{E}, \mathbf{B})$ rotation truncated to its first nontrivial term — gives:

$$\omega(k) = c\,k - \tfrac{1}{6} c^3 k^3 + O(k^5)$$

Time-of-flight measures group velocity, so the relevant correction is:

$$\frac{v_g(E)}{c} = 1 - \tfrac{1}{2}\left(\frac{E}{E_\text{Planck}}\right)^2$$

assuming the lattice tick equals the Planck time. In the standard LIV
parameterisation $v/c = 1 - s_n(E/E_{\text{QG},n})^n$ with $n=2$, $s=+1$:

$$E_{\text{QG},2}^{\,F26} = \sqrt{2}\,E_\text{Planck} \approx 1.73 \times 10^{19}\,\text{GeV}$$

## Sources confronted

| Source | $z$ | $E_h$ | $\kappa_2(z)$ | $\Delta t(F26)$ | $\Delta t$ at exp. limit | Verdict |
|---|---|---|---|---|---|---|
| GRB 090510 (Fermi-LAT) | 0.903 | 31 GeV | 1.460 | $3.2 \times 10^{-18}$ s | $5.7 \times 10^{-2}$ s | below sens. (16.2 dec) |
| GRB 221009A (LHAASO) | 0.151 | 13 TeV | 0.168 | $6.5 \times 10^{-14}$ s | $4.0 \times 10^{1}$ s | below sens. (14.8 dec) |
| Mrk 501 flare (MAGIC) | 0.034 | 10 TeV | 0.035 | $8.0 \times 10^{-15}$ s | $7.4 \times 10^{2}$ s | below sens. (17.0 dec) |

Published 95% CL bounds used:
- Fermi-LAT GRB 090510: $E_{\text{QG},2} > 1.3 \times 10^{11}$ GeV (Vasileiou+ 2013)
- LHAASO GRB 221009A: $E_{\text{QG},2} > 7.0 \times 10^{11}$ GeV (Piran & Ouyang 2024)
- MAGIC Mrk 501: $E_{\text{QG},2} > 5.7 \times 10^{10}$ GeV (MAGIC Collab. 2008)

## What it would take to test F26

| Source | Photon energy required to reach today's sensitivity |
|---|---|
| GRB 090510 baseline | $\ge 4.1$ EeV |
| GRB 221009A baseline | $\ge 320$ EeV |
| Mrk 501 baseline | $\ge 3000$ EeV |

(One EeV = $10^9$ GeV. Current highest-energy detected photon is ~$10$ TeV = $10^{-5}$ EeV.)

## Verdict

**F26 is NOT excluded by any current experiment.** It sits roughly 15 decades
below the time-of-flight sensitivity of the best current experiment
(LHAASO GRB 221009A). Confirmation or exclusion at the Planck-scale tick
assumption is not within reach of any planned photon observatory.

The prediction is real, falsifiable in principle, and beyond present technology.

## Implications

1. **F26 survives every current LIV bound** — Fermi, MAGIC, HESS, LHAASO, IceCube
   are all consistent with $E_{\text{QG},2} = \sqrt{2}\,E_\text{Planck}$.
2. **It would only be testable** with cosmological-baseline photons at $\gtrsim 10^{20}$ eV,
   which is roughly the GZK cutoff for cosmic rays — photons that energetic from
   cosmological distances would already be absorbed on the CMB. So even
   astrophysically, the test is borderline impossible.
3. **The relevant near-term constraint** would relax the lattice-tick assumption.
   If the underlying CA tick rate is *not* the Planck time but instead some
   coarser scale (e.g., GUT-scale, $\tau \sim 10^4 t_P$), the equivalent
   $E_{\text{QG},2}$ drops to $\sim 10^{15}$ GeV and the prediction becomes
   testable with LHAASO-class experiments within a few orders of magnitude.

## Open follow-up

A separate scan over candidate lattice-tick rates would tell us *which*
tick-rate values are already ruled out by current photon time-of-flight
experiments. That is a cheap calculation and worth doing — it would convert
the current "untestable" verdict into a constraint on the lattice scale itself.
