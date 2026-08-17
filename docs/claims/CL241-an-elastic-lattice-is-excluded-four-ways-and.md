---
id: CL241
title: 'An elastic lattice is excluded four ways, and it **cannot** rescue F282: because F79 ties $G$ to $a^2$, the ratio $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$ is **i'
slug: 'an-elastic-lattice-is-excluded-four-ways-and'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F283]
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

# CL241 — An elastic lattice is excluded four ways, and it **cannot** rescue F282: because F79 ties $G$ to $a^2$, the ratio $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$ is **i

## Statement

An elastic lattice is excluded four ways, and it **cannot** rescue F282: because F79 ties $G$ to $a^2$, the ratio $M_\text{Pl}/\Lambda_\text{UV}=3^{1/4}$ is **invariant** under any stretch $a\to sa$ ($\partial r/\partial s\equiv0$), so the inflation obstruction $r=\sqrt3=1/c_\text{lat}$ is a scale-free geometric property of the BCC lattice — this **corrects F282 falsifier #5**

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F283-elastic-lattice-excluded-and-f282-invariance.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F283-elastic-lattice-excluded-and-f282-invariance.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> **Structural no-go + a correction to F282.** 8/8 checks PASS. The invariance (E1) is **exact-algebraic** (sympy, symbols kept free so the cancellation is exhibited rather than asserted); the varying-$G$ and light-cone bounds (E2, E4) are **quantitative** against LLR/BBN/GW170817; the volume-mode dichotomy (E3) is **structural**, resting on F79/F180/F216.

**Date:** 2026-08-02 - 14:00

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F283-elastic-lattice-excluded-and-f282-invariance.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
