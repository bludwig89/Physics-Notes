---
id: CL293
title: 'Minimal single-channel top condensation for the F73 Cooper-pair Higgs, RG-improved from the model''s own F79/F107 lattice cutoff, is excluded: it predicts m_t=226.6 GeV (+31%) and m_H=248.8 GeV (+99%, essentially double) against the measured 172.57/125.25 GeV'
slug: 'minimal-top-condensation-excluded-at-model-cutoff'
tier: supporting
kind: no_go
status: live
domain: [SM]
exactness: quantitative
findings: [F352, F73, F74, F77, F107]
tests: [F352-higgs-bhl-compositeness]
modules: [casim.engine.particles.derive_higgs_bhl_compositeness]
constants: [a_over_ellP]
supersessions: []
reviews: [docs/reviews/F352-review-2026-09-02.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-02'
last_verified: '2026-09-02'
provenance: authored
review_state: authored
confidence: high
---

# CL293 — Minimal top-condensation compositeness is excluded as the origin of both m_t and m_H at this model's own derived cutoff

## Statement

Renormalisation-group-improving the F73/F77 Cooper-pair compositeness condition
($m_H(\Lambda)=2m_t(\Lambda)$, $y_t(\Lambda)\to\infty$) down from the model's own derived UV
cutoff $\Lambda_\text{model}=E_\text{Planck}/(a/\ell_P)=1.850\times10^{18}$ GeV (F79/F107, exact,
not chosen for convenience) via the standard 1-loop SM RGEs predicts $m_t=226.56$ GeV ($+31.3\%$
vs. measured $172.57$ GeV) and $m_H=248.76$ GeV ($+98.6\%$, essentially double the measured
$125.25$ GeV). **Minimal single-channel top condensation, anchored at this model's own cutoff,
is therefore excluded as the simultaneous dynamical origin of the top and Higgs masses.**

## What it extends

This directly engages Standard Model electroweak symmetry breaking: it tests, inside this
Higgs-free model's own machinery, the same Bardeen–Hill–Lindner (1990) minimal top-condensation
scenario that was historically proposed as a dynamical (non-fundamental-scalar) origin for the SM
Higgs, and finds the identical qualitative failure mode the SM literature already established
for that scenario at a GUT/Planck-scale cutoff (a Higgs mass roughly double the observed value) —
here reproduced with a cutoff the model derives rather than one chosen after the fact. It **does
not** contradict the SM's own Higgs sector; it excludes one specific composite-Higgs realisation
of *this* model's Cooper-pair candidate (F73).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F352-higgs-bhl-compositeness-rg-negative.md` | The RG-improved calculation, headline numbers, $Y_0$/solver/$\Lambda$ robustness checks | quantitative |
| `tests/registry/particles.yaml` record `F352-higgs-bhl-compositeness` (7/7 PASS) | Y0-convergence, ratio moving off F77's flat ceiling, quantified overshoot in both masses | quantitative |
| `test-results/F352_higgs_bhl_compositeness.json` | Full numeric record (gauge couplings, headline, convergence table, $\Lambda$-sweep) | quantitative |
| `docs/reviews/F352-review-2026-09-02.md` | Inline self-review, 13-point attack list, verdict CONFIRMED-NARROWER | — |
| `findings/F74-two-constituent-bound-state-binding.md`, `findings/F77-njl-gap-rpa-selfconsistent.md` | The static (non-RG) no-go this extends: no sub-threshold binding at any coupling, at mean-field/RPA order | quantitative / machine |

## Falsifier

A future revision of the model's own UV cutoff (a supersession of F79/F107's $a/\ell_P$) that
moved $\Lambda_\text{model}$ down by many orders of magnitude toward the TeV scale would weaken
this specific exclusion (the BHL quasi-fixed-point prediction only saturates near the current
value for $\Lambda\gtrsim10^{6}$ GeV; F352 Part D shows the trend). Independently, a full lattice
Bethe–Salpeter treatment (F77's own named next step, not attempted here) or an additional
model-native strong-binding channel (a "topcolor" analogue) landing within a few percent of
$m_t=172.57$ GeV and $m_H=125.25$ GeV simultaneously would show that *some* dynamics in this
model reaches the measured values, though it would not by itself undo this card's narrower
claim about the minimal single-channel scenario specifically, which would need an error in the
RG calculation or cutoff identification to be overturned directly.

## Status & history

`live` since first issue (2026-09-02) — the claim is stated at the scope it was tested (minimal
single-channel compositeness only) and no broader form was ever asserted, so there is no
narrowing history yet. See F352 "Scope / next" for the specific untested channels (lattice
Bethe–Salpeter, multi-channel/topcolor analogues, the F73-constituent identification question)
that this card deliberately does not claim to address.

## Sources

- `findings/F352-higgs-bhl-compositeness-rg-negative.md`
- `findings/F73-spin0-bound-pair-scalar.md`, `findings/F74-two-constituent-bound-state-binding.md`, `findings/F77-njl-gap-rpa-selfconsistent.md`
- `findings/F107-canonical-a-adoption-L4-grb-gate.md`
- Bardeen, Hill & Lindner, *Phys. Rev.* D41 (1990) 1647 (external; minimal top-condensation RG method)
- [Top quark condensate — Wikipedia](https://en.wikipedia.org/wiki/Top_quark_condensate) (historical-verdict cross-check, fetched 2026-09-02)
- `docs/status/open-derivations.md` row E8 / parameter #18
