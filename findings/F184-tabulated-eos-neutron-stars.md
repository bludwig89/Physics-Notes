# F184 — Tabulated-EoS neutron stars on the F181 kernel: SLy gives M_max=2.08 M⊙ and R(1.4)=11.1 km, consistent with PSR J0740 and NICER (scenario S1)

**Date:** 2026-06-30 - 04:00
**Numbering:** sequential build-out of the gravity-sector scenario catalog; this is **F184** (re-checked; max was F183).
**Status:** Confirmed — 3/3 checks PASS. The machinery (piecewise-polytrope EoS + two-function TOV) is exact; absolute M–R values inherit the published EoS digits and a single-crust simplification (R good to ~5%).
**Module:** `ca-simulation/ca_ns_eos.py` (uses `ca_interior_metric` / F181)
**Script:** `tests/findings/test_F184_tabulated_ns.py` (~23 s)
**Results:** `test-results/F184_tabulated_ns.json`
**Cross-references:** [[F181-covariant-interior-kernel-battery]] (the genuine GR/TOV interior), [[F176-covariant-dielectric-tov-recovery]] (the recommended tabulated-EoS follow-up this delivers), [[F174-stellar-structure-overlay]] (the literal-F106 exclusion). External: Read, Lackey, Owen & Friedman PRD 79, 124032 (2009); PSR J0740+6620 (2.08±0.07 M⊙); NICER J0030/J0740 radii.

---

Scenario S1 of the catalog. Now that F181 made the neutron-star interior genuine GR/TOV, this drops realistic **piecewise-polytrope** equations of state (Read et al. 2009: SLy, APR4, MPA1 cores + a matched crust) into the two-function TOV solve.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| N1 | **SLy**: $M_{\max}=2.08\,M_\odot$ (turnover present), $R(1.4)=11.1$ km, surface redshift $0.63$ at $M_{\max}$ — consistent with PSR J0740+6620 ($2.08\pm0.07$) and the NICER radii (~11–12.5 km) | PASS |
| N2 | **EoS ordering**: the stiffer cores give larger $M_{\max}$ and $R(1.4)$ than SLy (monotone stiffness trend) | PASS |
| N3 | **GR/TOV structure**: each EoS shows a stable rising branch terminating at a maximum-mass turnover (the TOV instability) — not the literal-F106 runaway of F174 | PASS |

## Result

The model's neutron stars are now ordinary GR/TOV stars built on realistic microphysics: SLy lands at $2.08\,M_\odot$, sitting right on PSR J0740, with a canonical radius in the NICER band. The $AB\equiv1$ single-scalar residual that F176 flagged is gone (F181), so there is **no model-specific departure** in the mass–radius relation — the prediction is standard GR, which the data support. Absolute radii inherit the EoS digits and a single-crust approximation (R is ~5% low vs full-crust SLy); substituting a full multi-piece crust is the mechanical refinement.

## Open / next
- Full multi-piece crust + verified APR4/MPA1 digits for absolute NICER placement.
- Tidal deformability $\Lambda(M)$ (GW170817) on the same kernel — pairs with the F185 moment of inertia for I-Love-Q.

## Files
- Module: `ca-simulation/ca_ns_eos.py` · Test: `tests/findings/test_F184_tabulated_ns.py` · Results: `test-results/F184_tabulated_ns.json`
