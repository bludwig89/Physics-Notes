---
id: CL089
title: 'The second-shell $E_g$ gap computation at saturation amplitude: a two-value theorem excludes the strictly quadratic theory, the exact massless-electron texture '
slug: 'the-second-shell-gap-computation-at-saturation-amplitude'
tier: supporting
kind: derivation
status: open
domain: [condensed-matter]
exactness: exact
findings: [F96]
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

# CL089 — The second-shell $E_g$ gap computation at saturation amplitude: a two-value theorem excludes the strictly quadratic theory, the exact massless-electron texture 

## Statement

The second-shell $E_g$ gap computation at saturation amplitude: a two-value theorem excludes the strictly quadratic theory, the exact massless-electron texture algebra ($Q=\tfrac23\iff\delta=15°$), and the constructive unlock by the sextic invariant

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F96-second-shell-Eg-gap-saturation.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F96-second-shell-Eg-gap-saturation.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (strong structural result + exact algebra + constructive sufficiency) — 8/8 checks PASS. **The headline is a no-go with teeth:** the quadratic-cost mean-field gap theory on the BCC Dirac sea — any per-flavor + democratic four-fermion contact, either amplitude→mass map in the chain — supports **at most two distinct generation masses** (the two-value theorem, T3, realized over the full phase map, T4). The observed three distinct lepton masses therefore *exclude* it, making the non-quadratic $E_g$ self-term (F95's $C$) necessary for a **third independent reason** — beyond the angle brake (F95) and $m_e>0$, it is required for the very existence of three distinct masses. **The exact algebra:** any $(m_h, m_\text{mid}, 0)$ texture obeys $Q(u)=\frac{1+u^2}{(1+u)^2}$, $\tan\delta=\frac{\sqrt3\,u}{2-u}$ with $u=\sqrt{m_\text{mid}/m_h}$, and $Q=\tfrac23\iff u=2-\sqrt3=\tan15°\iff\delta=15°$ exactly, $\cos3\delta=1/\sqrt2$ — a new exact $45°$ ($=3\delta$) in the chain, and the $\varepsilon\to0$ limit the unlocked theory must approach. **Constructive sufficiency:** adding the single invariant $W(\sum_a p_a^3)^2$ — the $e^6\cos^23\delta$ sextic in flavor variables, whose square root is exactly F95's derived cubic — unlocks a three-distinct-mass phase (30 minimizers found). See §7.

**Date:** 2026-06-05 - 04:55

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F96-second-shell-Eg-gap-saturation.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
