---
id: CL246
title: 'Why 3+1: two independent selectors already fix $d=3$; only the \"+1\" is by construction'
slug: 'why-3-1-two-independent-selectors-already-fix'
tier: supporting
kind: derivation
status: open
domain: [SM]
exactness: unset
findings: [F291, F318]
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

# CL246 — Why 3+1: two independent selectors already fix $d=3$; only the "+1" is by construction

## Statement

Why 3+1: two independent selectors already fix $d=3$; only the "+1" is by construction

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F291-why-three-plus-one-dimensions.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F291-why-three-plus-one-dimensions.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> *The finding states no `**Status:**` line.*

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F291-why-three-plus-one-dimensions.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract

## Amendment 2026-08-16 — the "conditional on s = 2" caveat is measured away (F318)

F291 §3 flags its own weakest point: *"Conditional on $s=2$. For $s=2^k$ the Clifford bound is
$2k+1$, so a larger cell would relax this to $d\le2k+1$."* On that reading the model's own
$s=36$ quark cell would permit $d\le11$ and S1 would be gone.

[[F318-cell-carries-the-internal-index]] measures it and it is not. The bound S1 needs is the
maximal mutually **anticommuting** subset inside the real span of the **hop's** traceless
Hermitian part, not the Clifford rank of the cell — and the model's branch-doubled Dirac cell
widens that span from 3 to **6** while leaving the anticommuting rank at **3**, because
$\tau_3\otimes\sigma_i$ *commutes* with $\mathbb 1\otimes\sigma_i$. An internal factor
$\otimes\mathbb 1_N$ changes neither number. So F291's stated boundary — *"losing S3 **and**
$s=2$ together would reopen the question"* — is not reached by anything the model actually does.

The converse is measured too, so this is a strengthening rather than a removal of content: a walk
that genuinely *uses* five anticommuting generators on $\mathbb C^4$ has
$\ker J=\operatorname{coker}J=0$ at $d=5$, and both selectors then return 5. F291 is left
**bit-unchanged** (D12); only the status of its caveat moves. See also **CL272**.
