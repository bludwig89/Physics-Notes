---
id: CL022
title: 'alpha_s(M_Z) = 0.11955 is the register''s largest open tension, at 2.1 sigma'
slug: 'alpha-s-at-mz-open-tension'
tier: headline
kind: deviation
status: open
domain: [QCD]
exactness: quantitative
findings: [F144, F115, F124, F299, F303]
tests: [F303-coupling-normalisation]
modules: [casim.engine.gauge.derive_coupling_normalisation]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-06'
provenance: authored
review_state: authored
confidence: medium
---

# CL022 — alpha_s(M_Z) = 0.11955 is the register's largest open tension, at 2.1 sigma

## Statement

The model gives $\alpha_s(M_Z)=0.11955$ (1-loop) against the PDG 2025 average $0.1175\pm0.0010$: **$+1.7\%$, i.e. $\approx2.1\sigma$ of experiment**. One scheme-matching input. This is **the register's largest open tension and is stated as such**.

## What it extends

QCD, in which $\alpha_s$ is a measured input. The model derives it from $g_s=1/2$ at the Brillouin-zone edge with one scheme-matching input, so the residual is a real disagreement rather than a fit quality.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F144-route-a-alpha-s-dimensional-transmutation.md` | $g_s=1/2$ derived; $\alpha_s(M_Z)$ converged, zero-parameter up to the scheme input | quantitative |
| `findings/F115-coupling-magnitudes-running-rotor.md` | The rotor lock $g_s^2\chi=1/4$ | exact |
| `findings/F124-sqrt-sigma-over-fpi-two-qcd-calibrations.md` | The $\sqrt\sigma/f_\pi$ scale-setting residual, which is the same open coefficient | quantitative |

## Falsifier

A tightened world-average $\alpha_s(M_Z)$ that moved the residual past $3\sigma$ without a corresponding scheme-matching resolution would falsify the derivation route. **The residual has already moved once for this reason and in the unfavourable direction** — see history.


**The $2.1\sigma$ framing is contingent on H1, added 2026-08-06 (F299/F303).** This card's number
assumes the model's bare coupling is $1/(16\pi)$ — F294's hypothesis **H1**, in which the F110 C7
matching carries no Casimir. F299 measured which law the model's own confinement sector obeys: at the
model's own coupling $\beta=2N/g_s^2=24$ the exactly solvable 2D SU(3) engine gives
$\sigma_6/\sigma_3=2.4911511$ against $5/2$ (Casimir) and $1$ (centre) — **Casimir scaling, i.e.
H2**. Under H2 the bare coupling is $1/(16\pi C_F)$, $g_s=\sqrt3/4$, and $\alpha_s(M_Z)=0.03970$:
**not a $2.1\sigma$ tension but a $-66\%$ miss.** F303 then looked for an argument that the coupling
is centre-normalised and found none, closing three candidates exactly — the Casimir shift is $26\times$
F144's *measured* A4 residual so it is not a scheme constant; the three-link plaquette that would
reconcile both readings does not exist on the BCC graph (no closed 3-bond loop, by parity and by
exhaustive enumeration); the Cartan reading gives a Landau pole above $M_Z$. **So this card is
currently the H1 branch of a fork the tree cannot close**, and the deciding computation is named in
F303 §"Remains" item 3: a one-loop background-field $\Lambda$-ratio for the model action, which must
come out $\approx1.78$ under H1 and $\approx3.4\times10^6$ under H2. Six decades apart, so it cannot
come out ambiguous.

## Status & history

`open`. **The measurement moved, not the model.** Revision 1 recorded $+1.3\%$ against a PDG average of $0.1180$; that average is now $0.1175\pm0.0010$, so the same unchanged model number is $+1.7\%$. Recording this as a card rather than a table row is deliberate: a residual that worsens because the world average shifted is the case a prose summary is worst at tracking.

## Sources

- `findings/F144-route-a-alpha-s-dimensional-transmutation.md`
- `findings/F124-sqrt-sigma-over-fpi-two-qcd-calibrations.md`
- `papers/Claims-and-Falsifiers-Summary.md` — headline numbers and the two-residuals note
