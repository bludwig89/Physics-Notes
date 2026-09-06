---
id: CL162
title: 'Tabulated-EoS neutron stars on the F181 kernel: three published nuclear-matter cores (SLy, AP4, MPA1) each clear the PSR J0740+6620 mass floor and fall inside the PSR J0437-4715 68% NICER radius band, while a deliberately soft/stiff bracket (WFF1, MS1) is correctly excluded by the same check'
slug: 'tabulated-eos-neutron-stars-on-the-f181-kernel'
tier: supporting
kind: derivation
status: live
domain: [GR]
exactness: quantitative
findings: [F181, F184, F356]
tests: [F184-tabulated-ns, F356-eos-robustness]
modules: [casim.engine.interactions.ns_eos, casim.engine.interactions.interior_metric]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-04'
last_verified: '2026-09-03'
provenance: authored
review_state: authored
confidence: medium
---

# CL162 — Tabulated-EoS neutron stars on the F181 kernel, now checked against three published cores and the current NICER/PSR bands

## Statement

Dropping a published piecewise-polytrope equation of state (Read, Lackey, Owen & Friedman 2009)
into the F181 covariant two-function TOV kernel reproduces standard GR/TOV neutron-star structure
with no model-specific departure. For the three cores actually published as modern
nuclear-matter EoS (SLy, AP4, MPA1), $M_{\max}$ clears the PSR J0740+6620 mass floor
($\geq2.01\,M_\odot$) and $R(1.418\,M_\odot)$ falls inside the PSR J0437$-$4715 68% NICER radius
band $[10.73,12.31]$ km, for all three simultaneously (F356). AP4's margin on that band is narrow
(0.7%), and AP4 separately sits below the wider PSR J0740+6620 radius band's lower edge at
$M{=}2.08\,M_\odot$ — noted here because the claim above is scoped specifically to the J0437$-$4715
band, the tighter and more current of the two (see F356 "Reading the result" for why, and for why
the model's own low-biased crust systematic works to relieve rather than worsen that margin). The
check is not vacuous: a deliberately soft core (WFF1) and a deliberately very stiff core (MS1),
added specifically as a falsification bracket, are both turned away by the J0437$-$4715 band while
both still clear the mass floor (F356 E2).

## What it extends

General relativity's TOV interior-structure prediction for compact stars, confronted with the
current (2024) tightest NICER mass-radius measurements: PSR J0740+6620 (Fonseca et al. 2021 mass;
Dittmann et al. 2024 updated NICER+XMM radius) and PSR J0437$-$4715 (Choudhury et al. 2024, the
nearest/brightest MSP and the current tightest NICER radius band). This model asserts no
departure from GR here — the claim is that the model's induced-gravity interior kernel (F181)
reproduces the standard GR/TOV mass-radius relation, and that relation is what the data are
compared against.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F181-covariant-interior-kernel-battery.md` | The genuine two-function GR/TOV interior kernel this EoS machinery runs on | exact (metric algebra), numeric (TOV integration, to integrator floor) |
| `findings/F184-tabulated-eos-neutron-stars.md` | SLy alone: $M_{\max}=2.08\,M_\odot$, $R(1.4)=11.1$ km, consistent with the (looser, 2021-era) bands then available. Its N2 relative-ordering check was narrowed 2026-09-03 (to $M_{\max}$-only ordering) under the corrected AP4 digits and re-verified PASS — see its "Correction" section; does not affect the SLy result this card cites | quantitative |
| `findings/F356-multi-eos-nicer-robustness.md` | SLy+AP4+MPA1 all pass the J0437$-$4715 band, against the tighter current (2024) bands; WFF1/MS1 bracket correctly excluded. Includes this card's own AP4-digit correction and citation fix, found by F356's attack pass | quantitative |
| `test-results/F184_tabulated_ns.json`, `test-results/F356_eos_robustness.json` | The committed numeric results (result-dump baselines) | — |

## Falsifier

A standard, currently-favoured tabulated nuclear-matter EoS (i.e. not a deliberately extreme
outlier like WFF1/MS1) that, run through the unmodified F181 kernel, produces an $M_{\max}$ below
the PSR J0740+6620 mass floor, or an $R(1.418)$ outside the PSR J0437$-$4715 radius band, would
falsify this claim's "no model-specific departure" reading — it would mean the kernel's GR/TOV
structure disagrees with data using microphysics the nuclear-astrophysics community currently
treats as viable. Equivalently: if a future NICER/radio measurement tightens the J0437$-$4715 band
enough to exclude SLy, AP4, *and* MPA1 simultaneously, the claim as stated is falsified (a
tightened band excluding only one or two of the three would narrow, not falsify, it — see "Status
& history"; AP4 is the one closest to that edge already, at a 0.7% margin).

## Status & history

`live`. Broadened from the F184-only (SLy, one 2021-era band) form on 2026-09-03 once F356 ran
the same absolute check on AP4 and MPA1 against the current (2024) bands and both passed; the
card was also promoted from `unreviewed-seed` to `authored` at the same time (its statement,
falsifier and evidence table are now hand-written from the findings, not mechanically extracted).

**Corrected same day:** F356's own attack pass found the `APR` EoS digits used were not the
published AP4 row (a pre-existing defect inherited from F184) and that the PSR J0740+6620 radius
citation was misattributed ("Salmi et al." → corrected to Dittmann et al., arXiv:2406.14467). Both
are fixed; the corrected AP4 digits still pass the J0437$-$4715 band (now known to be a narrow
0.7% margin, stated above) so this card's `live` status and statement were not narrowed by the
correction, only its numbers and one attribution were.

**Not yet covered:** the moment of inertia (F185's $I/MR^2\approx0.31$) is still a toy
$K,\Gamma$-polytrope result, not computed on any of these tabulated cores directly (F356 "Open /
next"); this card's evidence table does not include an $I/MR^2$ row and none should be inferred.
Tidal deformability $\Lambda(1.4)$ against GW170817 is also not yet computed on this kernel.

## Sources

- `findings/F181-covariant-interior-kernel-battery.md`
- `findings/F184-tabulated-eos-neutron-stars.md`
- `findings/F356-multi-eos-nicer-robustness.md`
- Read, Lackey, Owen & Friedman, PRD 79, 124032 (2009) / arXiv:0812.2163
- Fonseca et al. 2021, ApJL 915, L12 / arXiv:2104.00880 (PSR J0740+6620 mass)
- Dittmann et al. 2024, ApJ / arXiv:2406.14467 (PSR J0740+6620 updated NICER radius)
- Choudhury et al. 2024, ApJL 971, L20 / arXiv:2407.06789 (PSR J0437$-$4715 NICER mass-radius)
