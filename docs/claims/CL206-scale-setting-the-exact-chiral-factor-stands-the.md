---
id: CL206
title: '$\sqrt\sigma/f_\pi$ scale-setting: the exact chiral factor $7.04$ stands, the $+12\%$ confinement-factor residual is **not** removable by any principled BCC Bri'
slug: 'scale-setting-the-exact-chiral-factor-stands-the'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: quantitative
findings: [F235]
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

# CL206 — $\sqrt\sigma/f_\pi$ scale-setting: the exact chiral factor $7.04$ stands, the $+12\%$ confinement-factor residual is **not** removable by any principled BCC Bri

## Statement

$\sqrt\sigma/f_\pi$ scale-setting: the exact chiral factor $7.04$ stands, the $+12\%$ confinement-factor residual is **not** removable by any principled BCC Brillouin-zone cutoff, and it is the **same** strong-sector one-loop constant $d_1$ that E3 ($N$) and Q2 ($\alpha_s$ scheme) reduce to — so Q1, Q2 and E3 are one open number, not three

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F235-sqrt-sigma-fpi-scale-setting-unifies-with-d1.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F235-sqrt-sigma-fpi-scale-setting-unifies-with-d1.md` | The finding, in full | quantitative |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial + honest negative — 4/4 checks PASS (`test_F235_sqrt_sigma_fpi_scale_setting.py`, <1 s, stdlib). **This executes open-derivations prompt Q1 (#8).** The prompt asks to push $\sqrt\sigma/f_\pi$ (F124: $4.00$ axis vs empirical $4.56$, $+12\%$) below $5\%$ by deriving the scale-setting factor from strong-coupling running (F144 $\alpha_s$ + F86 $\sigma$), *or* to document the missing factor. Result: **the residual does not close to $<5\%$ from a cutoff-convention choice** — the value $\Lambda_\text{eff}=2.758/a$ needed to hit $4.56$ lies *below* even the per-axis BZ edge $\pi/a=3.14$ and far below every equal-volume BCC Debye radius, so no principled Brillouin-zone cutoff reaches it. The residual is a genuine **scale-setting** object, and F124 §5 / F144-A4 already identify it as *the same* one-loop matching constant $d_1$ (equiv. $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$) that E3 (F233) and Q2 (F154) reduce to. **Verdict: Q1 does not close independently; it merges with E3+Q2 into the single constant $d_1$ — the F162 background-field computation would close all three at once.**

**Date:** 2026-07-02 - 23:55

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F235-sqrt-sigma-fpi-scale-setting-unifies-with-d1.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
