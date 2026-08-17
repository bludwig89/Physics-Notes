---
id: CL205
title: 'The overall mass scale $N$ is **not** the deepest free number: F119''s \"no running channel\" no-go is superseded by F144''s dimensional transmutation — colour-sect'
slug: 'the-overall-mass-scale-is-not-the-deepest'
tier: supporting
kind: no_go
status: withdrawn
domain: [QCD]
exactness: machine
findings: [F233]
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

# CL205 — The overall mass scale $N$ is **not** the deepest free number: F119's "no running channel" no-go is superseded by F144's dimensional transmutation — colour-sect

## Statement

The overall mass scale $N$ is **not** the deepest free number: F119's "no running channel" no-go is superseded by F144's dimensional transmutation — colour-sector asymptotic freedom generates $N$ to a factor $\approx1.9$ with zero parameters, and the whole residual is the one shared strong-sector scheme constant $d_1$

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F233-mass-scale-N-transmutation-supersedes-F119.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F233-mass-scale-N-transmutation-supersedes-F119.md` | The finding, in full | machine |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`withdrawn`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Reconciliation / reclassification — 5/5 checks PASS (`test_F233_mass_scale_N_transmutation.py`, <1 s, reproduces `ca_alpha_s_running`). **This executes open-derivations prompt E3 (#6).** The prompt (and the 2026-07-02 ledger) still label $N=m_\text{lat}(\tau)\approx5.5\times10^{-19}$ "the deepest single open number — genuinely may be the hierarchy," citing F119's sharp no-go ("the gap mechanism can't make $N$ from $O(1)$ couplings — $\sim10^{-36}$ tuning, **no running channel**"). But F119 is dated 2026-06-09; **F144 (2026-06-12) already built the running channel** and the ledger's E3 row never integrated it. The channel is **asymptotic freedom itself**: the rule-locked bare coupling $\alpha_s(\mu_0)=1/(16\pi)$ at $\mu_0=\hbar c/a=1.85\times10^{18}$ GeV runs down (standard $\overline{\rm MS}$, zero knobs) to $\Lambda_{\overline{\rm MS}}$, giving $N_\text{pred}=\Lambda^{(3)}/\mu_0=2.86\times10^{-19}$ (loop-converged) — **a factor $1.9$ from F119's $5.5\times10^{-19}$, across 19 decades, with no free parameter.** The entire residual is the single one-loop matching constant $d_1$ (equivalent $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$, vs Wilson's $28.81$) — **the same number** that Q1 ($\sqrt\sigma/f_\pi$ scale-setting, F124) and Q2 ($\alpha_s$ scheme, F144-A4/F154) reduce to. **Verdict: E3 is demoted from "genuinely free" to "transmutation-generated to a factor $1.9$; residual = the shared scheme constant."**

**Date:** 2026-07-02 - 23:40

**A supersession/withdrawal banner appears in this finding's header**, which is why the card reads `withdrawn`. The specific ledger record has not been attached — do that before relying on this status.

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F233-mass-scale-N-transmutation-supersedes-F119.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
