---
id: CL208
title: 'The keV-sterile resolution attempt (open-derivation D2): can resonant Shi-Fuller production plus late **entropy dilution** thread the current X-ray + Lyman-α wi'
slug: 'the-kev-sterile-resolution-attempt-open-derivation-d2'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: unset
findings: [F237]
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

# CL208 — The keV-sterile resolution attempt (open-derivation D2): can resonant Shi-Fuller production plus late **entropy dilution** thread the current X-ray + Lyman-α wi

## Statement

The keV-sterile resolution attempt (open-derivation D2): can resonant Shi-Fuller production plus late **entropy dilution** thread the current X-ray + Lyman-α windows for the F47/F200 keV sterile? **No — clean exclusion.** The two levers are anti-correlated through the mixing: passing Lyman-α requires dilution $S$, which needs $S\times$ more production, which raises $\sin^2 2\theta$ (X-ray line rate) by exactly $\log_{10}S$ dex — the X-ray margin worsens as $S$ while the Lyman-α floor improves only as $S^{-4/9}$, so **no $S$ co-satisfies both**. The keV sterile is excluded as 100% DM; hand off to the **F223/F228 Planck-mass spin-2 geon** (the viable 100%-DM candidate). The keV sterile survives only as a bounded sub-dominant component

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F237-kev-sterile-resolution.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F237-kev-sterile-resolution.md` | The finding, in full | unset |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> **Clean exclusion (a valid, publishable negative result per House Rules).** Reuses the validated F205 QKE production solver and adds one new physical lever — post-production entropy dilution — then scans the full $(m_s, L, S)$ space. No point clears both the current X-ray line bound and even the *conservative* (3.5 keV) Lyman-α floor, at either the 5.6 keV texture mass or the 7.1 keV benchmark. The exclusion is mechanism-level (opposite-sign scaling exponents), not a grid artifact. 7/7 acceptance checks PASS.

**Date:** 2026-07-03 - 14:20

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F237-kev-sterile-resolution.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
