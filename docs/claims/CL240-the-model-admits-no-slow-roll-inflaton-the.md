---
id: CL240
title: 'The model admits **no** slow-roll inflaton: the F107 cell puts the lattice cutoff at $\Lambda=3^{-1/4}M_\text{Pl}=\sqrt{c_\text{lat}}\,M_\text{Pl}$ **exactly**,'
slug: 'the-model-admits-no-slow-roll-inflaton-the'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F282]
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

# CL240 — The model admits **no** slow-roll inflaton: the F107 cell puts the lattice cutoff at $\Lambda=3^{-1/4}M_\text{Pl}=\sqrt{c_\text{lat}}\,M_\text{Pl}$ **exactly**,

## Statement

The model admits **no** slow-roll inflaton: the F107 cell puts the lattice cutoff at $\Lambda=3^{-1/4}M_\text{Pl}=\sqrt{c_\text{lat}}\,M_\text{Pl}$ **exactly**, so every compact CA field direction carries $M_\text{Pl}^2/f^2\ge\sqrt3=1/c_\text{lat}$ and every slow-roll parameter is $O(10)$ — the primordial $P(k)$ is an automaton **initial condition**, not a dynamical output

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F282-no-slow-roll-inflaton-sub-planckian-cutoff.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F282-no-slow-roll-inflaton-sub-planckian-cutoff.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> **Structural no-go** (a documented negative, the same category as [[F204-alcubierre-warp-structural-exclusion]] and [[F216-massive-spin2-dark-mode]]) — 7/7 checks PASS. The obstruction constant $r_\text{min}=M_\text{Pl}^2/\Lambda^2=\sqrt3=1/c_\text{lat}$ is **exact-algebraic**; the per-candidate coefficients are **closed-form** ($K_\text{clock}=9$ exactly) or **machine-precision numerical** ($K_\text{radial}=5.9215$, on the model's own F118 couplings); the escape-route exclusions (Starobinsky, N-flation, periodic $n_s$) are **quantitative** with named margins.

**Date:** 2026-08-02 - 12:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F282-no-slow-roll-inflaton-sub-planckian-cutoff.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
