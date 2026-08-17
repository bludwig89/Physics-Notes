---
id: CL073
title: 'Self-consistent NJL gap + RPA: one coupling fixes both $m_c$ and $E_b$, and it confirms the F74 ceiling'
slug: 'self-consistent-njl-gap-rpa-one-coupling-fixes'
tier: supporting
kind: derivation
status: live
domain: [QCD]
exactness: exact
findings: [F77]
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

# CL073 — Self-consistent NJL gap + RPA: one coupling fixes both $m_c$ and $E_b$, and it confirms the F74 ceiling

## Statement

Self-consistent NJL gap + RPA: one coupling fixes both $m_c$ and $E_b$, and it confirms the F74 ceiling

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F77-njl-gap-rpa-selfconsistent.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F77-njl-gap-rpa-selfconsistent.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 14/14 checks PASS. The two chiral-limit theorems (Goldstone $m_\pi=0$ and the NJL relation $m_\sigma=2m_c$) reproduce to machine precision ($2.3\times10^{-14}$), the polarization split identity is exact ($1.8\times10^{-16}$), and the canonical SU(2) fit reproduces the **measured** $m_c$, $f_\pi$, $m_\pi$ and $\langle\bar qq\rangle$ to within $0.2$–$4\%$. The F74 follow-up is answered.

**Date:** 2026-06-01 - 20:05

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F77-njl-gap-rpa-selfconsistent.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
