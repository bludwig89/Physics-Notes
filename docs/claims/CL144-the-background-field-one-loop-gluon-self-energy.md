---
id: CL144
title: 'The background-field one-loop gluon self-energy is **assembled and the $b_0=\tfrac{11}{3}C_A=11$ recovery gate PASSES exactly** (transverse, gluon : ghost $=10:'
slug: 'the-background-field-one-loop-gluon-self-energy'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F162]
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

# CL144 — The background-field one-loop gluon self-energy is **assembled and the $b_0=\tfrac{11}{3}C_A=11$ recovery gate PASSES exactly** (transverse, gluon : ghost $=10:

## Statement

The background-field one-loop gluon self-energy is **assembled and the $b_0=\tfrac{11}{3}C_A=11$ recovery gate PASSES exactly** (transverse, gluon : ghost $=10:1$), and the lattice running is confirmed propagator-independent — but the finite $d_1$ that pins $q_\ast$ to the digit stays **open** (the vertex form-factor part, with its Wilson-28.81 gate), so the F155 bracket $q_\ast a\in[1/\sqrt3,\sim0.97]$ stands

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F162-bgfield-self-energy-b0-gate.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F162-bgfield-self-energy-b0-gate.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial — the **b₀ gate is PASSED** (exact, continuum + lattice-propagator-independent), which is the loop-assembly validation F155 lacked; the **finite $d_1$ to the digit is NOT closed** (it needs the bespoke lattice 3-gluon + ghost form factors, validated against Wilson's $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ — not executed). 3/3 checks PASS. G1 exact (b₀=11, transverse, gluon:ghost 10:1 — symbolic/machine); G2 well-conditioned (lattice b₀ = continuum b₀, subtracted shift q-flat to $<10^{-3}$); G3 scope-sharp.

**Date:** 2026-06-18 - 14:30

**`docs/theory/supersessions.yaml` names this finding in a `superseded:` list**, while the finding's own status line above still reads as concluded. Both are correct: a finding records what a session concluded and does not get rewritten; the *claim* resting on it is what moves. This card is therefore `open`, not `live` — whether the assertion survives its supersession has **not** been reviewed.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F162-bgfield-self-energy-b0-gate.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
