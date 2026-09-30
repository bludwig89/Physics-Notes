---
id: CL149
title: 'The photon''s interacting two-body wavefunction: a normalizable threshold bound state whose masslessness is inherited from gapless constituents'
slug: 'the-photon-s-interacting-two-body-wavefunction-a'
tier: supporting
kind: prediction
status: live
domain: [SM]
exactness: exact
findings: [F169, F397]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: unset
first_issued: '2026-08-04'
last_verified: '2026-09-22'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL149 — The photon's interacting two-body wavefunction: a normalizable threshold bound state whose masslessness is inherited from gapless constituents

## Statement

The photon's interacting two-body wavefunction: a normalizable threshold bound state whose masslessness is inherited from gapless constituents

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F169-photon-interacting-two-body-wavefunction.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Amendment — 2026-09-22 (C3 only)

The finding's C3 originally quoted a **fit exponent 2.10** for $\Omega_\text{even}(k)-T(k)$, obtained from a
local stochastic descent (`true_threshold`) that under-converged at small $|k|$. That number is **withdrawn**.
Both quantities now have closed forms:

- the two-body floor $T(\mathbf k)=\min\bigl(\omega^+(\mathbf k),\omega^-(\mathbf k)\bigr)$, attained at the
  collinear endpoint $p=\pm\mathbf k/2$ (exact: $\omega^\pm(0)=0$ identically);
- the offset $\Omega_\text{even}(\mathbf k)-T(\mathbf k)=|k_xk_yk_z|/(3|\mathbf k|)+O(k^3)$, direction-dependent,
  vanishing on the coordinate planes.

Converged exponent **2.007**. The claim's substance — a normalizable threshold bound state whose masslessness is
inherited from gapless constituents — is **unchanged**: it rests on C1/C2/C4/C5/C6, all of which are statements at
$k=0$ or at fixed finite $k$, none of which used the search. Derived in [F397](../../findings/F397-notebook-factorization-route-pp176-182.md) R6.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F169-photon-interacting-two-body-wavefunction.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed (the interacting wavefunction is built) — 6/6 checks PASS (secular residual exactly 0; two-method agreement $5.6\times10^{-14}$; $T(0)=0$ exact). Builds the explicit two-constituent bound-state wavefunction that [F69](F69-paired-spinor-photon.md)/[F74](F74-two-constituent-bound-state-binding.md)/[F168](F168-paired-photon-binding-gauge-protected.md) deferred. The binding *coupling value* (criticality) remains the one external input, as in F74.

**Date:** 2026-06-29 - 17:55

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F169-photon-interacting-two-body-wavefunction.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
