---
id: CL276
title: 'm_W and m_Z are predicted absolutely from two electroweak inputs, where the Standard Model needs three'
slug: 'absolute-gauge-boson-masses-two-inputs'
tier: headline
kind: prediction
status: live
domain: [SM]
exactness: bracketed
findings: [F320, F141, F138, F231, F49, F51]
tests: [F320-gauge-boson-masses]
modules: [src/casim/engine/gauge/derive_gauge_boson_masses.py]
constants: [sin2_thetaW_onshell]
supersessions: []
reviews: []
rolls_up_to: CL007
falsifier: stated
first_issued: '2026-08-16'
last_verified: '2026-08-16'
provenance: authored
review_state: authored
confidence: high
---

# CL276 — m_W and m_Z are predicted absolutely from two electroweak inputs, where the Standard Model needs three

## Statement

Given $\{\alpha,\ G_F\}$ and nothing else, the model predicts

$$m_W=\frac{3v}{2}\sqrt{2\pi\alpha},\qquad m_Z=\frac{9v}{2}\sqrt{\frac{2\pi\alpha}{7}},\qquad v=(\sqrt2\,G_F)^{-1/2},$$

exactly, where the rationals are the BCC Wigner–Seitz facet count (7) and sublattice count (2)
of F141/F51 and the stiffness quantum $u=18\pi\alpha/7$ is **determined**, not free.

At tree level this gives $m_W=79.0836$ GeV and $m_Z=89.6724$ GeV ($-1.5996\%$, $-1.6621\%$).
Including the external radiative correction $\Delta r$ the prediction is the bracket
$m_W\in[80.1473,\ 80.5475]$ GeV and $m_Z\in[90.8785,\ 91.3323]$ GeV, both of which contain the
PDG 2024 values $80.3692$ and $91.1880$ GeV.

The residual is stated $\Delta r$-**free**: because the model and the Standard Model sit on the
same on-shell relation with the same $\Delta r$, the ratio
$m_W^\text{model}/m_W^\text{obs}=\sqrt{\sin^2\theta_W^\text{obs}/(2/9)}$ holds for every
$\Delta r$ (verified to $2.2\times10^{-16}$ over $\Delta r\in[0,0.10]$), giving
$+0.222\%$ on $m_W$ and $+0.158\%$ on $m_Z$.

## What it extends

The Standard Model's electroweak sector takes three measured inputs — $\alpha$, $G_F$ and one
boson mass (conventionally $m_Z$) — and predicts the other boson mass and $\sin^2\theta_W$. This
model takes **two**, because $\sin^2\theta_W^\text{os}=2/9$ comes from lattice geometry rather
than from a third measurement. The claim is a reduction of the electroweak input count by one,
and the deliverable is that both boson masses become outputs.

It does **not** extend anything about the electroweak *scale*: $v$ remains an anchor (ledger 17,
`FIT (N=1)`), F119's finding that the overall scale $N$ has no $O(1)$ mechanism is untouched, and
$\alpha$ remains the EM input (F127's four-avenue no-go). Two inputs is not zero inputs.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F320-absolute-gauge-boson-masses-and-rho.md` §2 | $u=18\pi\alpha/7$ from $e=g\sin\theta_W$; $g^2=18\pi\alpha$, $g'^2=36\pi\alpha/7$; the two closed forms | exact |
| `findings/F320-absolute-gauge-boson-masses-and-rho.md` §4 | $\Delta r$ cancels in the ratio; $+0.222\%$ / $+0.158\%$ | machine |
| `findings/F320-absolute-gauge-boson-masses-and-rho.md` §5 | the bracket, and that its width is the SM's own $\Delta r_\text{rem}=0.00965$ | bracketed |
| `findings/F141-ws-cell-7axes-onshell-mass-counting.md` | the 7 facet axes (exact lemma) and the $2:7$ equal-stiffness hypothesis this rests on | exact |
| record `F320-gauge-boson-masses` | 22/22, three controls each `CONTROL` over disjoint leg sets | bracketed |
| `test-results/F320_gauge_boson_masses.json` | full payload | — |

## Falsifier

The entire residual is the on-shell Weinberg angle, and there is no parameter left to absorb a
change in it. The claim dies if $\sqrt{\sin^2\theta_W^\text{obs}/(2/9)}$ leaves $[0.995,1.005]$
— equivalently if the measured $m_Z/m_W$ moves off $3/\sqrt7=1.133893$ by more than $0.1\%$. A
measurement of $m_W$ at fixed $\{\alpha,G_F\}$ outside $[80.147,80.548]$ GeV that is not
attributable to $\Delta r$ kills it directly.

The claim is **conditional on F141's equal-stiffness hypothesis (U)**, whose (U1)/(U2)/(U3) legs
are open. The control `equal_stiffness=false` in the record shows what fails if (U) fails: the
whole counting block and every absolute number, though *not* CL277.

## Status & history

`live`, first issued 2026-08-16 with F320. This card **supersedes the scope boundary** recorded
in CL016, which said the absolute masses were not predicted; CL016 moves to `withdrawn` on the
same date, and its retraction record explains why the boundary was drawn in the wrong place — the
premise ("$v$ is an anchor") was true and the conclusion did not follow from it.

Completeness row B12 moves PARTIAL → QUANT on this card plus CL277.

## Sources

- `findings/F320-absolute-gauge-boson-masses-and-rho.md`
- `findings/F141-ws-cell-7axes-onshell-mass-counting.md`
- `findings/F231-weinberg-2over9-onshell-face-of-1over4.md`
- `docs/claims/CL016-mw-and-mz-absolute-not-claimed.md` — withdrawn by this card
- `docs/status/completeness-2026-08-07.md` — row B12
