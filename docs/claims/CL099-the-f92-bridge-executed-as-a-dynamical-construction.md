---
id: CL099
title: 'The F92 bridge executed as a dynamical construction: the pair-sum law is derived from the update rule ($U\otimes U$ rotates the symmetric two-quantum channel by'
slug: 'the-f92-bridge-executed-as-a-dynamical-construction'
tier: supporting
kind: derivation
status: open
domain: [GR]
exactness: exact
findings: [F109]
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

# CL099 — The F92 bridge executed as a dynamical construction: the pair-sum law is derived from the update rule ($U\otimes U$ rotates the symmetric two-quantum channel by

## Statement

The F92 bridge executed as a dynamical construction: the pair-sum law is derived from the update rule ($U\otimes U$ rotates the symmetric two-quantum channel by exactly $2t$), the 45°/unitarity-cap point is the unique attractor of the rule-driven phase flow (repulsion rate at the origin exactly $4I_2$), and the flavor-resolved condensation experiment lands on the constrained point with the $(A_{1g},E_g)$ decomposition measured, not posited

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F109-f92-bridge-construction.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F109-f92-bridge-construction.md` | The finding, in full | exact |

**This card's only evidence is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support. Promoting it to `authored` means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt, ratcheted down by `tools/check_claims.py`. It is not a claim that no falsifier exists — that would be `falsifier: none`, which requires the structural reason to be named.

## Status & history

`open`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Partial (closing C.4's simulation build; the honest residuals are explicit) — 5/5 checks PASS. **What is constructed (audit item C.4, the F92 §6 build):** (B1) the per-tick chirality allocation is **flavor-resolved in the model's own code** — three flavor axes each execute the unit 2-vector $(\cos t_a,\sin t_a)$, $t_a=m_a\,dt$, bit-level (`ca_dirac.mass_step_1flavor_u1`, extends F92-P1); (B2, **exact**) the two-constituent one-tick step $U(t)\otimes U(t)$, $U=e^{it\sigma_1}$, has spectrum $\{e^{2it},1,1,e^{-2it}\}$ with all four eigenpairs verified symbolically — the maximally-rotating channel is the **symmetric two-quantum combination** (exactly the state the Fock $\sqrt2$ of F92-P2 normalizes) and traverses $2t$ per tick, so $m_\text{comp}=\sin2t$ by F46: **L1, previously kinematic (F73), is derived from the update rule**; (B3) the relaxational flow of the constituent phase under the sea energy with L1 kinematics, $E(t)=f(\sin2t)$, has exactly two fixed points — $t=0$ **repulsive** with exact rate $4I_2$ (measured $0.8772$ vs $4\times0.21913=0.8765$ at $L=24$) and $t=45°$ the **attractor** whose stiffness diverges toward the wall (the F46 arccos cliff; measured $3.0\to10.5\to30.4$ as $\varepsilon\to0$): every seed in $(0°,90°)$ flows to $45°$ exactly, where $y=\sqrt2\sin t_*=1$ (budget filled), $m_\text{pair}=1$ (mass peak) and $c^2=2\cot t_*=2$ (Fock) — **F92's triple saturation and F101-A0's wall-pinning emerge as the dynamical endpoint of the flow**; (B4) the flavor-resolved pairing simulation: from 1000 random seeds the projected flow of the F108-completed gap functional condenses into the constrained channel with basin fractions **lepton 49.1%**, $(0,0,0)$ 41.1%, $(1,1,1)$ 0.1%, and the **measured** (common, differential) decomposition at the lepton basin: $Q=0.666661$, $\delta=12.733°$, $\cos3\delta=0.785874$, equipartition $e/(\sqrt3\bar y)=0.999991$ ($A=\sqrt2\,\bar y$), Fock readout $c^2=2.000018$ — the F92-P5 data pin reproduced by the dynamics. Honest comparisons: minimal couplings → $(0,0,0)$ 87.9% with the lepton basin metastable at 11.7% (F101-A2/F108 realized dynamically); wall-constrained flow ($y_\tau\equiv1$, the audit's "constrained to one point") → the light flavors condense at the data point in **91.8%** of seeds. See §5.

**Date:** 2026-06-06 - 23:30

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

## Sources

- `findings/F109-f92-bridge-construction.md`
- `docs/claims/README.md` — the `unreviewed-seed` contract
