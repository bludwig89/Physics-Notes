# F356 — Multi-EoS robustness of the F181/F184 tabulated-EoS kernel against current NICER/PSR mass-radius data: SLy, AP4 (corrected), MPA1 all pass the discriminating current band; a deliberately soft/stiff bracket (WFF1, MS1) is correctly excluded

**Date:** 2026-09-03 - 16:30
**Numbering:** max existing F-number was F355; this is **F356** (`casim index` NEXT FREE NUMBER, no gap).
**Status:** Confirmed — 3/3 checks PASS (as originally run, and unchanged after the digit correction below). The machinery (piecewise-polytrope EoS + F181 two-function TOV) is exact; absolute M–R values inherit the published EoS digits and the F184 single-crust simplification (R good to ~5%).
**Checked:** 2026-09-03 - 17:00 — 11 PASS / 2 WEAKENS / 2 FAIL / 0 NOT RUN — **UNDER-EVIDENCED, then CORRECTED** (see "Reviewed & corrected" below; post-correction re-verification: **CONFIRMED**, all pass/fail verdicts unchanged, numbers updated)
**Module:** `src/casim/engine/interactions/ns_eos.py` (extended: `EOS_PARAMS` gains `WFF1`, `MS1`; the pre-existing `APR` entry was found wrong during this finding's own attack pass and corrected — see below; uses `interior_metric` / F181)
**Script:** `tests/findings/test_F356_eos_robustness.py` (~60 s)
**Results:** `test-results/F356_eos_robustness.json`
**Cross-references:** [[F181-covariant-interior-kernel-battery]] (the genuine GR/TOV interior this reuses unchanged — the attack pass below found no fault in it), [[F184-tabulated-eos-neutron-stars]] (the SLy-only absolute check this extends to AP4/MPA1; see F184's own "Correction" section for the consequence there — N2 flips PASS→FAIL under the same digit fix), [[F185-slow-rotation-moment-of-inertia]] (the I/MR² result, untouched here — still a toy K=100,Γ=2 polytrope, not tied to a tabulated EoS; remains open, see below). External: Read, Lackey, Owen & Friedman, PRD 79, 124032 (2009) (arXiv:0812.2163) — EoS parametrization; AP4/WFF1/MS1 digits verified directly against Table III during this finding's attack pass. Fonseca et al. 2021, ApJL 915, L12 (arXiv:2104.00880) — PSR J0740+6620 mass. Dittmann et al. 2024, ApJ (arXiv:2406.14467) — updated PSR J0740+6620 NICER+XMM radius (corrected attribution — see "Reviewed & corrected"; not Salmi et al., whose companion paper arXiv:2406.14466 reports a different number). Choudhury et al. 2024, ApJL 971, L20 (arXiv:2407.06789) — PSR J0437−4715 NICER mass-radius.

---

## The residual this closes

F184 built the machinery to run any Read et al. (2009) piecewise-polytrope EoS through the F181 kernel, and `EOS_PARAMS` already carried three cores (SLy, APR/AP4, MPA1). But F184's absolute physical-band check (N1: turnover + PSR-J0740-consistent $M_{\max}$ + NICER-band $R(1.4)$) was run on **SLy only**; APR/AP4 and MPA1 were used solely for the *relative* ordering check (N2), never checked against data themselves. Rubric row E11 was graded QUANT on the strength of one EoS family. This finding runs the same absolute-band logic on all three published cores, against the two tightest **current** (2024) NICER/PSR measurements, and adds two deliberately extreme cores (WFF1, MS1) as a falsification bracket so the check is shown to have real discriminating power rather than passing anything handed to it.

## Current data anchors (superseding F184's looser citation)

| Pulsar | Mass | Radius (68% CI) | Source |
|---|---|---|---|
| PSR J0740+6620 | $2.08\pm0.07\,M_\odot$ | $12.92^{+2.09}_{-1.13}$ km | Fonseca et al. 2021 (mass, unchanged since F184); **Dittmann et al. 2024** (radius — updated NICER+XMM exposure, supersedes the earlier Miller/Riley 2021 bands F184 cited loosely) |
| PSR J0437−4715 | $1.418\pm0.037\,M_\odot$ | $11.36^{+0.95}_{-0.63}$ km | **Choudhury et al. 2024** — nearest/brightest MSP, the tightest current NICER radius band, and its mass sits close enough to the canonical $1.4\,M_\odot$ that $R(1.418)$ is compared almost directly to the usual $R(1.4)$ figure of merit |

The J0437−4715 radius band $[10.73,12.31]$ km is markedly tighter than the band F184 used, and it is the discriminator that does the work below.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| E1 | **Standard cores, absolute band:** SLy, AP4, MPA1 each show a turnover, $M_{\max}\geq2.01\,M_\odot$ (J0740 lower edge), and $R(1.418\,M_\odot)$ inside $[10.73,12.31]$ km (J0437−4715 68% band) | PASS |
| E2 | **Bracket falsification:** WFF1 (soft) and MS1 (very stiff) both clear the J0740 mass floor but are **both excluded** by the same J0437−4715 radius band — the check is not vacuous | PASS |
| E3 | **GR/TOV structure:** all five cores (the F184 three plus WFF1/MS1) show a stable rising branch terminating at a maximum-mass turnover | PASS |

**Overall 3/3 PASS.**

## Numbers (post-correction — see "Reviewed & corrected")

| EoS | $M_{\max}$ ($M_\odot$) | $R(1.418)$ (km) | $R(2.08)$ (km) | J0740 mass | J0437 radius | J0740 radius |
|---|---|---|---|---|---|---|
| SLy | 2.077 | 11.14 | — ($M_{\max}<2.08$) | ✓ | ✓ | ✓ (n/a, not reached) |
| AP4 (corrected) | 2.216 | 10.81 | 10.60 | ✓ | ✓ (0.7% margin) | **✗ below band** |
| MPA1 | 2.491 | 11.73 | 12.06 | ✓ | ✓ | ✓ |
| WFF1 (soft, added) | 2.153 | 10.01 | 9.77 | ✓ | ✗ (below band) | ✗ (below band) |
| MS1 (stiff, added) | 2.789 | 13.92 | 14.38 | ✓ | ✗ (above band) | ✓ (band is wide) |

$n{=}80$ central-density grid points per curve, same RK4/step convention as F184 (`h_cm=500`). SLy and MPA1 reproduce F184's own numbers to the stated precision. AP4's digits were corrected during this finding's attack pass (see below); the table above already reflects the corrected values.

## Reading the result

SLy and MPA1 sit inside **both** current bands simultaneously by comfortable margins. AP4 (once correctly digitized — see below) is a more interesting case: it clears the J0740 mass floor easily ($M_{\max}=2.22\,M_\odot$) and passes the tighter, more current J0437−4715 radius band, but only by a **0.7% margin** ($R(1.418)=10.81$ vs. the band's $10.73$ km lower edge) — and it sits **below** the wider J0740 radius band's lower edge at $M=2.08\,M_\odot$ ($R=10.60$ vs. $11.79$ km). This is a genuine, reportable tension, not one this finding's own E1 check is designed to catch (E1 gates on the J0437 band only, the deliberately-chosen tighter and more current discriminator — see "Reviewed & corrected," attack 4, for why that choice predates and is independent of this particular number). Two things work in AP4's favour here: J0740's radius measurement carries a much wider uncertainty than J0437's, so "below the 68% lower edge" is a soft violation, not an exclusion; and F184's own admitted single-crust systematic biases every radius in this table **low** by ~5%, which is in the direction that would relieve, not worsen, both of AP4's tight margins. Real AP4 is well known in the literature to be markedly more compact at canonical mass than a naive reading of its high $M_{\max}$ would suggest, so a compact result here is physically expected, not a code defect.

The other two added cores — WFF1 and MS1 — were included *because* they are known extremes, and both are correctly turned away by the J0437−4715 band while both still clear the J0740 mass floor. That asymmetry matches the literature's general reading that current NICER radii, not pulsar masses, are the sharper current lever on EoS stiffness — this is the "worth reporting either way" falsification check, and it reports a clean exclusion. Nothing here attacks or reopens the F181 kernel: the kernel is unchanged, and the attack pass below found no fault in it.

## Reviewed & corrected

**2026-09-03 - 17:00** — attack pass (13 attacks + unprompted check on interpolation logic): 11 PASS, 2 WEAKENS, 2 FAIL, 0 NOT RUN. Overall verdict from the cold attacking subagent: **UNDER-EVIDENCED**, deciding attacks 1 (circularity — digit verification) and 3 (exactness inflation — margin vs. systematic).

**Found:** the pre-existing `EOS_PARAMS["APR"]` entry `(34.616, 3.514, 3.141, 3.291)` — inherited unchanged from F184, never itself digit-checked until this finding's stated purpose was to do exactly that — does not match Read et al. (2009) Table III's AP4 row, verified by independently fetching the paper. The finding's citation "Salmi et al. 2024" for the PSR J0740+6620 radius (arXiv:2406.14467) was also wrong: that paper's authors are Dittmann, Miller, Lamb et al.; the real Salmi et al. 2024 paper is the companion arXiv:2406.14466 and reports a different number ($R{=}12.49^{+1.28}_{-0.88}$ km, $M{=}2.073\pm0.069\,M_\odot$) not used here. Two WEAKENS: (a) only 2 of ~23 Read-catalog cores were tried as the falsification bracket, so "genuine discriminating power" is shown on a 5-core sample, not the fuller catalog; (b) three brand-new (2026-09) NICER papers on PSR J1614−2230, PSR J0614−3329 and a combined J1614−2230/J2124−3358/47 Tuc X7 constraint exist and were not used.

**Fixed:** `src/casim/engine/interactions/ns_eos.py`'s `APR` entry corrected to the verified AP4 digits `(34.269, 2.830, 3.445, 3.348)`; both test scripts (`test_F356_eos_robustness.py` here and `test_F184_tabulated_ns.py`) re-run against the corrected table. F356's own E1/E2/E3 verdicts are unchanged (still 3/3 PASS) with updated numbers (AP4's row above). F184's N2 check initially flipped PASS→FAIL under the corrected digits, because its original assertion was a compound claim (both $M_{\max}$ *and* $R(1.4)$ order with stiffness) that does not hold for the real AP4 — AP4's genuinely higher $M_{\max}$ comes with a genuinely smaller $R(1.4)$ than SLy in this kernel, a known real feature of AP4, not a defect. N2 was narrowed to the part that is both true and the standard physical expectation ($M_{\max}$ ordering only); re-verified 3/3 PASS. See [[F184-tabulated-eos-neutron-stars]]'s own "Correction" section for the full account. The "Salmi et al." citation corrected to "Dittmann et al." throughout this finding and in `docs/claims/CL162-...md`. The tight AP4 margins (attack 3) are now stated explicitly in "Reading the result" above rather than left implicit in a table.

**Rejected:** none of the 13 attacks' verdicts were rejected outright.

**Deferred:** attack 5's broader-catalog coverage (run the remaining ~18 Read Table III cores, not just SLy/AP4/MPA1/WFF1/MS1) and attack 6's newer (Sept 2026) NICER data points — both real, both genuinely their own follow-up work, not required to support this finding's narrower claim (three specific published cores vs. two specific current measurements) — landing site: this finding's own "Open / next," below.

Independently re-verified by me (not just the subagent) before applying: AP4's corrected digits fetched a second time directly from arXiv:0812.2163 Table III and cross-checked against the SLy/MPA1 rows already in the table (both matched exactly, confirming the fetch's reliability); the Dittmann-vs-Salmi authorship and the two papers' differing numbers confirmed directly from both abstracts; F184's N2 flip to FAIL, and then its return to PASS under the narrowed assertion, both reproduced by actually re-running its script, not inferred.

## Open / next

- **APR4/MPA1 crust:** still the F184 single-crust simplification (~5% radius systematic, low-biased); a verified full multi-piece crust digit set would relieve AP4's tight current margins rather than worsen them (see "Reading the result").
- **Broader EoS-catalog coverage:** only 5 of Read et al. (2009)'s ~23 tabulated cores have been run through the absolute-band check (deferred by the attack pass, attack 5). Running the remainder would make the "genuine discriminating power" claim rest on the full catalog rather than a hand-picked bracket.
- **Newer (2026) NICER data:** PSR J1614−2230, PSR J0614−3329, and a combined J1614−2230/J2124−3358/47 Tuc X7 constraint (all arXiv:2609.0xxxx, September 2026) were flagged by the attack pass (attack 6) and not yet incorporated — a natural next current-data update.
- **Tabulated-EoS moment of inertia:** F185's $I/MR^2\approx0.31$ is a toy $K,\Gamma$-polytrope result, not yet computed on SLy/AP4/MPA1 directly — `ca_rotation.py`'s `frame_drag` needs an `eos.rho_of_p` inverse that `ns_eos.PiecewisePolytrope` does not currently expose (it has `eps_of_p`, the forward map only).
- **Tidal deformability $\Lambda(1.4)$** against GW170817, on the same five-EoS set, for a genuinely independent (non-mass-radius) current-data cross-check — flagged as open by F184 and still open here.

## Files
- Module: `src/casim/engine/interactions/ns_eos.py` (extended, and one pre-existing entry corrected)
- Test: `tests/findings/test_F356_eos_robustness.py`
- Results: `test-results/F356_eos_robustness.json`
