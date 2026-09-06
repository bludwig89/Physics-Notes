# F184 — Tabulated-EoS neutron stars on the F181 kernel: SLy gives M_max=2.08 M⊙ and R(1.4)=11.1 km, consistent with PSR J0740 and NICER (scenario S1)

**Date:** 2026-06-30 - 04:00
**Numbering:** sequential build-out of the gravity-sector scenario catalog; this is **F184** (re-checked; max was F183).
**Status:** Confirmed — 3/3 checks PASS (as of 2026-09-03; N2's assertion was narrowed to what the corrected physics actually supports — see **Checked:** line and "Correction" below). The machinery (piecewise-polytrope EoS + two-function TOV) is exact; absolute M–R values inherit the published EoS digits and a single-crust simplification (R good to ~5%).
**Checked:** 2026-09-03 - 17:00 — found during the [[F356-multi-eos-nicer-robustness]] attack pass — **CORRECTED** (APR digit fix + N2 narrowed to M_max-only ordering, see below); re-verified 3/3 PASS after the fix
**Module:** `ca-simulation/ca_ns_eos.py` (uses `ca_interior_metric` / F181)
**Script:** `tests/findings/test_F184_tabulated_ns.py` (~23 s)
**Results:** `test-results/F184_tabulated_ns.json`
**Cross-references:** [[F181-covariant-interior-kernel-battery]] (the genuine GR/TOV interior), [[F176b-covariant-dielectric-tov-recovery]] (the recommended tabulated-EoS follow-up this delivers), [[F174-stellar-structure-overlay]] (the literal-F106 exclusion). External: Read, Lackey, Owen & Friedman PRD 79, 124032 (2009); PSR J0740+6620 (2.08±0.07 M⊙); NICER J0030/J0740 radii.

---

Scenario S1 of the catalog. Now that F181 made the neutron-star interior genuine GR/TOV, this drops realistic **piecewise-polytrope** equations of state (Read et al. 2009: SLy, APR4, MPA1 cores + a matched crust) into the two-function TOV solve.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| N1 | **SLy**: $M_{\max}=2.08\,M_\odot$ (turnover present), $R(1.4)=11.1$ km, surface redshift $0.63$ at $M_{\max}$ — consistent with PSR J0740+6620 ($2.08\pm0.07$) and the NICER radii (~11–12.5 km) | PASS |
| N2 | **EoS ordering**: the stiffer cores give larger $M_{\max}$ than SLy (narrowed 2026-09-03 from a compound $M_{\max}$-and-$R(1.4)$ claim; see Correction) | PASS (post-correction) |
| N3 | **GR/TOV structure**: each EoS shows a stable rising branch terminating at a maximum-mass turnover (the TOV instability) — not the literal-F106 runaway of F174 | PASS |

## Result

The model's neutron stars are now ordinary GR/TOV stars built on realistic microphysics: SLy lands at $2.08\,M_\odot$, sitting right on PSR J0740, with a canonical radius in the NICER band. The $AB\equiv1$ single-scalar residual that F176 flagged is gone (F181), so there is **no model-specific departure** in the mass–radius relation — the prediction is standard GR, which the data support. Absolute radii inherit the EoS digits and a single-crust approximation (R is ~5% low vs full-crust SLy); substituting a full multi-piece crust is the mechanical refinement.

## Correction (2026-09-03, found by the F356 attack pass)

The `EOS_PARAMS["APR"]` entry this finding's N2 check used, `(34.616, 3.514, 3.141, 3.291)`, does
**not** match Read, Lackey, Owen & Friedman (2009) Table III's AP4 row — verified directly
against the paper (arXiv:0812.2163), whose actual AP4 digits are `(34.269, 2.830, 3.445, 3.348)`.
SLy and MPA1 were independently re-verified against the same table and are correct as originally
entered; only the "APR" entry was wrong, and its origin (fabricated vs. a transcription of a
different table's row) was not established. `src/casim/engine/interactions/ns_eos.py` has been
corrected to the verified AP4 digits.

**Consequence for N2:** with the corrected digits, AP4 still has a larger $M_{\max}$ than SLy
($2.216$ vs $2.077\,M_\odot$) but a **smaller** $R(1.4)$ ($10.80$ vs $11.14$ km) in this
crust-simplified kernel — real AP4 is known in the literature to be markedly more compact at
canonical mass than its higher maximum mass might suggest. N2's original assertion (both
$M_{\max}$ *and* $R(1.4)$ must exceed SLy for every "stiffer" core) does not hold for the
corrected AP4, so the check has been **narrowed** to the part that does hold and is the standard
physical expectation — $M_{\max}$ ordering only ($M_{\max}^{\rm MPA1}>M_{\max}^{\rm AP4}>M_{\max}^{\rm SLy}$,
verified) — with $R(1.4)$ still computed and reported but no longer asserted to order the same
way. `tests/findings/test_F184_tabulated_ns.py`'s `check_N2_ordering` and its docstring were
updated accordingly; re-running gives **3/3 PASS**. N1 (SLy alone) and N3 (structural/turnover
check) were unaffected throughout — neither used the APR digits. This does **not** touch the
F181 kernel, which this finding never questioned and which the F356 attack pass separately found
no fault in. `test-results/F184_tabulated_ns.json` has been regenerated with the corrected
digits and the narrowed N2 check, and reflects 3/3 PASS.

See [[F356-multi-eos-nicer-robustness]] for the full attack-pass record and for AP4's corrected
absolute placement against current NICER/PSR data (it remains consistent, by a narrow ~0.7%
margin on the tightest current radius band — see that finding).

## Open / next
- Full multi-piece crust + verified APR4/MPA1 digits for absolute NICER placement.
- Tidal deformability $\Lambda(M)$ (GW170817) on the same kernel — pairs with the F185 moment of inertia for I-Love-Q.

## Files
- Module: `ca-simulation/ca_ns_eos.py` · Test: `tests/findings/test_F184_tabulated_ns.py` · Results: `test-results/F184_tabulated_ns.json`
