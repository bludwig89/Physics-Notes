# F174 — The NICER overlay: solving both theories' hydrostatic structure shows the literal energy-only dielectric has no maximum neutron-star mass and is excluded by PSR J0740+6620 — unless the strong-field law is covariantized

> **⚠ Reclassified by [[F178-gravity-full-tensor-adoption]] (2026-06-29):** gravity sources from the full stress-energy tensor (induced Einstein equation canonical). the energy-only 'no maximum mass' result was the **diagnosis** that forced the F178 decision (adopt full-tensor gravity), not a standing model prediction.

**Date:** 2026-06-29 - 19:45
**Numbering:** max existing finding is F173 (this session's `F173-pressure-tolman-discriminator`); this is **F174** (re-checked per the CLAUDE.md concurrent-session caution — F170/171/172 were taken by other sessions earlier today).
**Status:** Confirmed — 5/5 checks PASS. Closes the open observable of [[F173-pressure-tolman-discriminator]] / FC09: each theory's hydrostatic structure is solved and overlaid on NICER. The Newtonian-limit convergence, the GR turnover, and the model's no-turnover/overprediction are all robust; the absolute radii use a toy Γ=2 polytrope (realistic EoS swappable).
**Module:** `ca-simulation/ca_stellar.py`
**Script:** `tests/findings/test_F174_stellar_overlay.py` (~6 s, numpy + local RK4, no scipy)
**Results:** `test-results/F174_stellar_overlay.json` (includes the full M–R and z–M overlay arrays)
**Cross-references:** [[F173-pressure-tolman-discriminator]] (the source-level discriminator this makes observable), [[F64-em-connection-gravity]] / [[F106-psi-K-sourcing-derivation]] (the dielectric law solved here), [[F114-dielectric-black-hole]] (the exterior strong-field counterpart). External: TOV (Tolman 1939, Oppenheimer–Volkoff 1939); PSR J0740+6620 M = 2.08 ± 0.07 M⊙ (Fonseca 2021), R = 12.35 ± 0.75 km (Miller 2021) / 12.92 km (Salmi 2024); PSR J0030+0451 (Riley/Miller 2019). Brief: `tests/falsification/FC09-neutron-star-pressure-redshift.md`.

---

## What was solved

F173 proved at the source level that the single-scalar dielectric sources gravity from energy density only (omitting GR's 3p Tolman term). This finding closes the chain to an observable by solving **each theory's own hydrostatic stellar structure** for the same equation of state and overlaying the results on neutron-star data.

**GR — Tolman–Oppenheimer–Volkoff:**
$$\frac{dm}{dr}=4\pi r^2\rho,\qquad \frac{dp}{dr}=-\frac{(\rho+p)(m+4\pi r^3p)}{r(r-2m)},\qquad z=(1-2M/R)^{-1/2}-1.$$

**Model — dielectric (literal F106: energy-only source, exponential metric):**
$$\frac{dm_E}{dr}=4\pi r^2\rho,\qquad \frac{dp}{dr}=-\frac{(\rho+p)\,m_E}{r^2},\qquad z=e^{M_E/R}-1.$$

The model's Euler equation uses the exact $g_{tt}=-e^{-2u}$ with the F106 potential $u'=-m_E/r^2$ — so it differs from TOV by exactly (i) no pressure in the mass source and (ii) no $(1-2m/r)$ spatial-curvature denominator. Both are direct consequences of one energy-sourced scalar. The EoS is a Γ=2 polytrope tuned so GR gives the observed $M_\text{max}\approx2.1\,M_\odot$.

## Checks (5/5)

| # | Check | Result | Tier |
|---|---|---|---|
| N1 | **Newtonian limit converges**: as compactness→0, $M_\text{model}/M_\text{GR}\to1$ (1.0015 at $M/R=5\times10^{-4}$, monotone toward unity) — validates the solver and F173's solar-system null | PASS | quantitative |
| N2 | **GR is realistic**: TOV gives a maximum-mass turnover at $M_\text{max}=2.14\,M_\odot$, $R=11.9$ km — matches PSR J0740+6620 | PASS | quantitative |
| N3 | **Model has no maximum mass**: no turnover in the NS range; mass still rising to $25\,M_\odot$ at the top of the density range, and it **overpredicts mass by 4.5×** at fixed central density $\rho_c=2\times10^{-3}$ | PASS | quantitative |
| N4 | **Fixed-mass radius**: at $1.4\,M_\odot$ the model star is $2.95$ km larger ($R=19.7$ vs $16.7$ km); at the J0740 mass $2.08\,M_\odot$, GR gives $R=13.3$ km (NICER $12.4\pm0.75$) while the model gives $R=19.6$ km — $\sim7$ km too large | PASS | quantitative |
| N5 | **Redshift offset grows with compactness**: $z_\text{model}-z_\text{GR}$ rises from $2\times10^{-4}$ to $0.52$ across $M/R=0.01\to0.27$ (same sign as F173) | PASS | quantitative |

## Verdict

Solving both structures makes the F173 discriminator concrete and **much larger than the uniform-sphere estimate suggested**: the absence of the relativistic $(1-2m/r)$ feedback and the missing pressure source compound, so the literal energy-only dielectric **has no neutron-star maximum mass** and overpredicts radii by many km. On the same EoS that makes GR reproduce PSR J0740+6620 ($2.08\,M_\odot$, $R\approx12.4$ km), the model predicts $R\approx19.6$ km at that mass and no Chandrasekhar-like upper limit at all. Measured neutron stars have a sharp $\sim2\,M_\odot$ maximum and $R\approx11$–$13$ km — so **the literal-F106 dielectric is observationally excluded in the strong-field interior.**

This is sharp, but it is a statement about the *literal* extension of the F106 weak-field law (flat Laplacian, energy-only) to strong field — the regime F64/F106 never fixed. The model therefore faces a clean fork:

1. **Keep one-field gravity** (∇²ln K = −8πT⁰⁰ literally) → excluded by neutron stars.
2. **Covariantize the strong-field law** — promote the source to the full induced $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$ inside matter (restoring the pressure source and the spatial-curvature feedback) → recovers TOV/GR, but sacrifices the single-scalar parsimony that motivated the dielectric.

Either the model accepts a falsified interior or it gives up one-field gravity where pressure is large. The exterior (β=γ=1, all solar-system tests, F114 black-hole shadow) is untouched by this — the failure is specifically the relativistic, pressurised interior.

## Open / next

- **Covariant variant.** Implement option 2 (covariant ∇² on the spatial metric **B**, with the pressure source) and re-run the overlay; quantify how much of GR-TOV it recovers and whether any residual NS signature survives. This is the decisive theoretical follow-up.
- **Realistic EoS.** Swap the Γ=2 polytrope for a tabulated nuclear EoS (APR, SLy) to put the GR curve precisely through the NICER credible regions and sharpen the model's exclusion margin.
- **Tidal deformability / GW170817.** A second, independent strong-field confrontation ($\Lambda$ vs mass) the same solver can produce.

## Files
- Module: `ca-simulation/ca_stellar.py`
- Test: `tests/findings/test_F174_stellar_overlay.py`
- Results + overlay arrays: `test-results/F174_stellar_overlay.json`
