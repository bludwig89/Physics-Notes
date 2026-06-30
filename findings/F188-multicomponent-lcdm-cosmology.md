# F188 — Multi-component cosmology under the full-tensor source: z_eq≈3430, z_acc≈0.63, age≈13.8 Gyr — standard ΛCDM, with pressure setting every transition (scenario S5)

**Date:** 2026-06-30 - 04:30
**Numbering:** **F188** (re-checked).
**Status:** Confirmed — 3/3 checks PASS. Standard FLRW integration with the full-tensor ($\rho+3p$) source; quantitative.
**Module:** `ca-simulation/ca_cosmology.py` (multi-component extension)
**Script:** `tests/findings/test_F188_lcdm.py`
**Results:** `test-results/F188_lcdm.json`
**Cross-references:** [[F182-friedmann-pressure-cosmology]] (the single-component Friedmann pair this builds on), [[F178-gravity-full-tensor-adoption]] (the source), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] / [[F192-vacuum-energy-full-tensor]] (the $\Lambda$ magnitude). External: Planck 2018 ($\Omega_m=0.315$, $\Omega_\Lambda=0.685$, $H_0=67.4$, age $13.80$ Gyr).

---

Scenario S5. Extends the F182 Friedmann pair to a flat three-component background ($\Omega_r+\Omega_m+\Omega_\Lambda=1$), where the acceleration equation $\ddot a/a=-\tfrac{H_0^2}{2}[2\Omega_r a^{-4}+\Omega_m a^{-3}-2\Omega_\Lambda]$ weights each component by $\rho+3p$.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| L1 | Cosmic timeline: $1+z_{\rm eq}=\Omega_m/\Omega_r\Rightarrow z_{\rm eq}=3433$; acceleration onset $z_{\rm acc}=0.63$; age $=13.79$ Gyr — all matching Planck-2018 ΛCDM | PASS |
| L2 | Acceleration sign from $\rho+3p$: decelerating in the radiation/matter era ($\ddot a<0$), accelerating today and in the future ($\ddot a>0$) — driven by $\Lambda$'s $w=-1$ | PASS |
| L3 | Flat normalization: $E(a{=}1)=1$ exactly | PASS |

## Result

The full-tensor source reproduces the standard ΛCDM expansion history with no tuning beyond the measured density fractions: matter–radiation equality at $z\approx3430$, the onset of acceleration at $z\approx0.63$, and a present age of $13.8$ Gyr. Every transition is set by the **pressure-weighted** source — radiation ($w=\tfrac13$) and matter ($w=0$) decelerate, $\Lambda$ ($w=-1$, $\rho+3p=-2\rho$) accelerates. This is the cosmological pay-off of F182: the energy-only law would have mis-weighted radiation by a factor 2 and mis-dated equality and nucleosynthesis.

## Open / next
- Perturbation growth $D(a)$ and the CMB acoustic scale (the pressure term enters the growth equation).
- Couple to the $\Lambda$ magnitude problem (F192/F164).

## Files
- Module: `ca-simulation/ca_cosmology.py` · Test: `tests/findings/test_F188_lcdm.py` · Results: `test-results/F188_lcdm.json`
