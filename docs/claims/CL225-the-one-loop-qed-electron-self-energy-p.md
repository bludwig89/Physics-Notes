---
id: CL225
title: 'The one-loop QED electron self-energy Σ(p): mass renormalization δm, wavefunction renormalization Z₂, and Z₁=Z₂ proven from the loop integrals'
slug: 'the-one-loop-qed-electron-self-energy-p'
tier: supporting
kind: derivation
status: open
domain: [cosmology]
exactness: exact
findings: [F258]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-04'
last_verified: '2026-08-04'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL225 — The one-loop QED electron self-energy Σ(p): mass renormalization δm, wavefunction renormalization Z₂, and Z₁=Z₂ proven from the loop integrals

## Statement

The one-loop QED electron self-energy Σ(p): mass renormalization δm, wavefunction renormalization Z₂, and Z₁=Z₂ proven from the loop integrals

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F258-electron-self-energy.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F258-electron-self-energy.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 6/6 checks PASS. The mass shift $\delta m=\tfrac{3\alpha}{4\pi}m\ln(\Lambda^2/m^2)$ and the wavefunction renormalization $Z_2=1-\tfrac{\alpha}{4\pi}\ln(\Lambda^2/m^2)$ are **algebraically exact** (sympy; the on-shell parametric integrals evaluate to exactly $3$ and $-1$); the differential Ward–Takahashi identity $\partial\Sigma/\partial p_\mu=-\Lambda^\mu(p,p)$ is **derived from the loop integrand**, turning $Z_1=Z_2$ from an assumption (F252) into a **computed** identity; lattice = continuum after subtraction. This completes the one-loop 1PI set $\{Z_3\ (\Pi,\text{F251}),\ Z_2\ (\Sigma,\text{F258}),\ Z_1\ (\Lambda,\text{F252})\}$ with all Ward identities verified.

**Date:** 2026-07-22 - 09:30

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F258-electron-self-energy.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
