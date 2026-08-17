---
id: CL145
title: 'The lattice 3-gluon + ghost vertices are **transcribed with their cos(k/2) form factors and validated** (continuum limit exact to O(a²)), the full Wilson backgr'
slug: 'the-lattice-3-gluon-ghost-vertices-are-transcribed'
tier: supporting
kind: no_go
status: open
domain: [QCD]
exactness: exact
findings: [F163]
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

# CL145 — The lattice 3-gluon + ghost vertices are **transcribed with their cos(k/2) form factors and validated** (continuum limit exact to O(a²)), the full Wilson backgr

## Statement

The lattice 3-gluon + ghost vertices are **transcribed with their cos(k/2) form factors and validated** (continuum limit exact to O(a²)), the full Wilson background-field self-energy is **assembled with the tadpole**, and the b₀/tadpole sub-pieces reproduce Wilson — but the **finite constant that pins Λ_MSbar/Λ_L = 28.81 does NOT converge at sandbox BZ resolution** (no Q→0 plateau), so the digit is deferred to the native high-res run

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial — the **vertex transcription is DONE and validated** (the F162-G3 open item), the **full self-energy with tadpole is assembled**, and the **tadpole/measure transversality restoration is now COMPLETE and EXACT** (machine precision). The validatable sub-pieces match Wilson (vertex continuum limit O(a²) exact; tadpole $Z_0=0.1549334$ machine; b₀ log vertex-independent). The **literal 28.81 reproduction is still NOT closed**, but for a now-sharper reason: with transversality restored, the scheme-clean lattice constant $dC$ is extractable, but converting to $\Lambda_{\overline{\rm MS}}/\Lambda_L$ needs (a) the Q→0 high-res extrapolation and (b) the **MS-bar continuum reference constant** (the large factor in 28.81 is the sharp-cutoff↔MS-bar scheme difference). 5/5 structural checks PASS. W1 exact (O(a²) vertex limit); W2 machine (Z₀); W3 mass isotropic; **W4 transversality EXACT (Ward residual $\sim10^{-18}$)**; W5 scope-sharp (scheme-clean dC extractable, literal 28.81 needs MS-bar reference).

**Date:** 2026-06-18 - 21:20 (rev — tadpole/measure transversality restoration completed)

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
