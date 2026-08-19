---
id: CL022
title: 'alpha_s(M_Z) = 0.11955 is the register''s largest open tension, at 2.1 sigma'
slug: 'alpha-s-at-mz-open-tension'
tier: headline
kind: deviation
status: open
domain: [QCD]
exactness: quantitative
findings: [F144, F115, F124, F299, F303, F325]
tests: [F303-coupling-normalisation, F325-x1-branch]
modules: [casim.engine.gauge.derive_coupling_normalisation]
constants: []
supersessions: [S20-F115-weinberg-gap-account-replaced-by-4piv-matching, S22-F298-mixed-matching-C_F-and-the-X1-branch]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-06-08'
last_verified: '2026-08-18'
provenance: authored
review_state: authored
confidence: high
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

**2026-08-18 — the contingency note is LIFTED (F325, S22-F298-mixed-matching-C_F-and-the-X1-branch).** F303 attached a history note that
this card's 2.1 sigma framing was contingent on hypothesis H1 — i.e. on branch B of the X1 fork — because the
alternative reading gave alpha_s(M_Z) = 0.0397 (-66.4 %) rather than a tension. **X1 is resolved and branch B is
adopted**, on two legs neither of which needs d_1: the Casimir branch's C_F is an artefact of evaluating the C7
identity with the abelian rotor's s(k)^2 against the SU(N) gauge theory's C_2(R_k) (F325 section 2; leg L6 of
F298-casimir-ladder, exact over Q), and independently the Casimir branch requires
Lambda_MSbar/Lambda_rule = 3.4e6, 5.63 decades outside F280/CL252's committed [1, 7.98] (F325 section 3; leg N8).
So the number and the 2.1 sigma stand unconditionally, and `confidence` moves medium -> high. What remains open
is unchanged: d_1 leg 3, which PINS the value inside the adopted branch rather than choosing a branch.

**F115 is cited here for CM3 only** — the rotor lock $g_s^2\chi=\tfrac14$ that makes $g_s$ non-independent. F115's CM2 reading of the Weinberg gap as a few-TeV matching offset is superseded by F138/F231 (ledger S20, 2026-08-17) and is not what this card rests on. Declared rather than left implicit because the same ambiguity let completeness row B9 grade its electroweak leg against the superseded reading for three consecutive reports.

`open`. **The measurement moved, not the model.** Revision 1 recorded $+1.3\%$ against a PDG average of $0.1180$; that average is now $0.1175\pm0.0010$, so the same unchanged model number is $+1.7\%$. Recording this as a card rather than a table row is deliberate: a residual that worsens because the world average shifted is the case a prose summary is worst at tracking.

## Sources

- `findings/F144-route-a-alpha-s-dimensional-transmutation.md`
- `findings/F124-sqrt-sigma-over-fpi-two-qcd-calibrations.md`
- `papers/Claims-and-Falsifiers-Summary.md` — headline numbers and the two-residuals note
