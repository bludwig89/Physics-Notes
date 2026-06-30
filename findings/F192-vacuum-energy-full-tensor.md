# F192 — The cosmological constant under the full-tensor source: vacuum w=−1 gives ρ+3p=−2ρ so it accelerates (sign correct), but the ~10¹²¹ magnitude overshoot (F164) remains open (scenario S9, open)

**Date:** 2026-06-30 - 04:50
**Numbering:** **F192** (re-checked).
**Status:** Partial / open — 3/3 checks PASS (the sign result is exact; the magnitude is explicitly unresolved). This is an honest reframing of F164, not a solution.
**Module:** `ca-simulation/ca_vacuum_energy.py` (reuses the F164 fork)
**Script:** `tests/findings/test_F192_vacuum_energy.py`
**Results:** `test-results/F192_vacuum_energy.json`
**Cross-references:** [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the magnitude problem), [[F178-gravity-full-tensor-adoption]] (the full-tensor source), [[F182-friedmann-pressure-cosmology]] / [[F188-multicomponent-lcdm-cosmology]] (where $\Lambda$ enters the expansion). External: Planck $\rho_\Lambda\approx6\times10^{-10}$ J/m³.

---

Scenario S9. Reframes the F164 cosmological-constant problem under the full-tensor source.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| V1 | Vacuum $w=-1\Rightarrow\rho+3p=-2\rho<0$: the full-tensor acceleration equation makes the vacuum **accelerate** the expansion — the correct dark-energy sign (the demoted energy-only law, using $\rho$ only, would decelerate) | PASS |
| V2 | Bare overshoot: the BCC zero-point density overshoots observed $\Lambda$ by $\log_{10}\approx120.8$ — reproducing F164 | PASS |
| V3 | Open status: all four candidate cancellations (boson–fermion sign, CA-native 't Hooft vacuum, F64 sequestering, F69 marginal binding) remain *underived* | PASS |

## Result

The full-tensor source buys the model one real thing in the dark-energy sector: the **sign**. Because vacuum energy has $w=-1$, the combination that gravitates is $\rho+3p=-2\rho$, which accelerates the expansion — exactly the role $\Lambda$ plays, and a sign the energy-only law would have gotten wrong. What it does **not** buy is the magnitude: the bare lattice zero-point density still overshoots the observed value by ~120 orders (F164), and none of the candidate cancellations is derived from first principles. So F178 makes the cosmological constant a *consistent* part of the full-tensor cosmology (right sign, enters Friedmann correctly, F188) while leaving the magnitude as the model's largest open problem.

## Honest scope
This finding quantifies and reframes; it does not solve. The sign result (V1) is exact; the overshoot (V2) is the F164 number; the ledger (V3) is the open list.

## Open / next
- Derive one candidate cancellation (the CA-native 't Hooft vacuum is the F164-preferred lead) to a definite, sub-leading residual.
- Tie the surviving vacuum component to the F191 dark-matter candidate (one dark vacuum sector for both DM and DE).

## Files
- Module: `ca-simulation/ca_vacuum_energy.py` · Test: `tests/findings/test_F192_vacuum_energy.py` · Results: `test-results/F192_vacuum_energy.json`
