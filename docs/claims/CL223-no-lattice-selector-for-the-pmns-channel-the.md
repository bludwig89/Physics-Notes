---
id: CL223
title: 'No lattice selector for the PMNS $T_{2g}$ channel: the three neutrino-mixing amplitudes transform as **three inequivalent 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$'
slug: 'no-lattice-selector-for-the-pmns-channel-the'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F254]
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

# CL223 — No lattice selector for the PMNS $T_{2g}$ channel: the three neutrino-mixing amplitudes transform as **three inequivalent 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$

## Statement

No lattice selector for the PMNS $T_{2g}$ channel: the three neutrino-mixing amplitudes transform as **three inequivalent 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$) of the $E_g$-stabilizer $D_{2h}$, so no residual symmetry relates them and the F92 equipartition mechanism cannot apply — the PMNS angles are **genuinely free** (a stabilizer theorem, parallel to D3's free $\beta$)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F254-t2g-pmns-selector-nogo.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F254-t2g-pmns-selector-nogo.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Derivation + honest-negative closure — 4/4 PASS (`test_F254_t2g_pmns_selector.py`, ~9 s). **What is proven (exact / group-theoretic):** under the generic-$E_g$ stabilizer $D_{2h}$ (F93 O3), the three second-shell $T_{2g}$ axis-mixing amplitudes $(t_{xy}, t_{yz}, t_{zx})$ transform as **three inequivalent nontrivial 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$: distinct, zero-sum characters over the 8 group elements) — so **no residual lattice symmetry relates them** (T1). The democratic point $t_{xy}=t_{yz}=t_{zx}$ is invariant under only $\{+\mathbb 1, -\mathbb 1\}$ (order 2 of 8) → **not symmetry-protected**, and the F92 equipartition selector (which equalizes weights *within a single degenerate multiplet*) **cannot apply**, because the $E_g$ condensate splits the $T_{2g}$ triplet into three *inequivalent* irreps — there is no degenerate multiplet to equipartition over (T2). **Numerical no-go (T3):** democratic and single-channel one-parameter $T_{2g}$ ansätze miss NuFIT-5.2 (NO) by $>100^\circ{}^2$; only the **full three-amplitude** fit reaches the data ($\sim10^{-11}$ deg), with exactly **3 inputs for 3 angles** (no predictive slack). **Verdict:** the D1 selector **provably does not exist** among residual-symmetry / equipartition mechanisms — the PMNS angles are **genuinely free** (three independent order parameters in three inequivalent $D_{2h}$ channels), sharpening F236's fit-counting statement into a stabilizer theorem exactly parallel to D3's geon-abundance $\beta$.

**Date:** 2026-07-16 - 16:58

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F254-t2g-pmns-selector-nogo.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
