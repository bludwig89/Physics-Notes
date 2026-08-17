---
id: CL137
title: 'Building and solving the two strong-sector residuals: **Residual B is solved** (the self-consistent gap fixes the IR coupling $\alpha_\text{eff}^\ast=0.376/0.41'
slug: 'building-and-solving-the-two-strong-sector-residuals'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: exact
findings: [F154]
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

# CL137 — Building and solving the two strong-sector residuals: **Residual B is solved** (the self-consistent gap fixes the IR coupling $\alpha_\text{eff}^\ast=0.376/0.41

## Statement

Building and solving the two strong-sector residuals: **Residual B is solved** (the self-consistent gap fixes the IR coupling $\alpha_\text{eff}^\ast=0.376/0.411\approx0.39$, converged and $L$-stable, reproducing F151-S5 from first principles); **Residual A's cheap route fails** ($q_\ast$ is a UV-finite lattice−continuum subtraction, not a propagator log-moment — the full one-loop integral remains)

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F154-residuals-A-B-built-and-solved.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F154-residuals-A-B-built-and-solved.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (one residual solved, one residual's shortcut ruled out) — 5/5 checks PASS. **B (solved):** the full **nonlinear** self-consistent gap equation $M(k)=m_0+24\langle G_S(k{-}q)M(q)/\sqrt{K{+}M^2}\rangle$ — built here, not in F145 (which only had the *linearised* $M\!\to\!0$ eigenvalue) — converges, with the coupling fixed by the physical constituent mass $M(0)=1.50$ (=311 MeV, F77/F124), to $\alpha_\text{eff}^\ast=0.376$ ($m_D{=}0.532$) / $0.411$ ($m_V{=}0.727$): **identical to F151-S5/F152 to 3 digits**, now as a converged ($\sim130$-iteration) fixed point that is $L$-stable ($0.3764$ at $L{=}16/24/32$). The naive perturbative running ($\Lambda^{(3)}=347$ MeV) **overshoots** to $M(0)\approx1400$–$1570$ MeV, confirming the deep-IR running is unreliable (the IR coupling is genuinely a distinct nonperturbative object, not the frozen running). **A (cheap route fails, honest negative):** with the V-scheme + exact $a_1=\tfrac{11}3$ already fixed (F151), the only residual is the matching scale $q_\ast$. Its natural shortcut — the gluon-propagator **log-moment** over the BZ — does **not** pin it: the converged moments are *UV* scales ($\langle\ln K\rangle_\text{4D}=2$ exactly $\Rightarrow q_\ast^\text{bare}=e/a=2.72/a$; the $1/K$-weighted $=2.30/a$), all **above** F151's band $[1/\sqrt3,1]/a$, while the only weight that reaches the band ($1/K^2$) is IR-divergent and grid-dependent ($1.01\!\to\!0.65$ as $n{:}24\!\to\!64$). The lesson is physical: $q_\ast$ is the **UV-finite lattice−continuum subtraction** (the true $d_1$ integral), not a bare moment — so **A still requires the full one-loop background-field computation**, exactly as F151 §8 said. **Coupling of the two:** B fixes the *dimensionless* gap physics ($\alpha_\text{eff}^\ast\leftrightarrow M(0)$); removing B's mass anchor entirely needs the *absolute scale*, which **is** A — so the last freedom is one scale, and it sits in the one integral A names. See §6.

**Date:** 2026-06-12 - 19:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F154-residuals-A-B-built-and-solved.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
