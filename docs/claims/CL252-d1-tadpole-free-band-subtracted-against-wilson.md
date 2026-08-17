---
id: CL252
title: 'The lattice-to-MSbar constant for the rule action is bracketed: Lambda_MSbar/Lambda_rule in [1, 7.980], containing the required 1.7734 and excluding Wilson''s 28.8086'
slug: 'd1-tadpole-free-band-subtracted-against-wilson'
tier: supporting
kind: derivation
status: open
domain: [QCD]
exactness: bracketed
findings: [F280, F287, F163, F162, F155, F239]
tests: [F280-d1-subtracted]
modules: [src/casim/engine/gauge/lpt_d1_subtracted.py]
constants: [q_star_a_implied]
supersessions: []
reviews: []
rolls_up_to: CL022
falsifier: stated
first_issued: '2026-08-05'
last_verified: '2026-08-05'
provenance: authored
review_state: authored
confidence: medium
---

# CL252 — The lattice-to-MSbar constant for the rule action is bracketed

## Statement

Formulated **subtracted against the Wilson anchor** $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$, the rule action's one-loop matching constant satisfies

$$\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}=28.8086\,\exp\!\Big[-\tfrac12\big(T_W+\delta_\text{loops}\big)\Big]\ \in\ [1,\ 7.980],$$

which contains the value $1.773444$ the $g_s=\tfrac12$ lock requires and excludes Wilson's $28.8086$ by $3.61\times$. The required shift decomposes into three legs in $\Delta C$ units: the Wilson seagull $+$ Haar measure being **structurally absent** ($-2.5676$, 46.1%), the **measured** propagator face ($-0.9919\pm0.0439$, 17.8%), and the still-open rule vertex form factors ($-2.0160$, 36.2%, within $[-2.257,-1.446]$). The upper edge of the band rests on a **named monotonicity assumption**, not a theorem.

## What it extends

QCD's lattice-to-$\overline{\rm MS}$ scheme matching. In lattice gauge theory $\Lambda_{\overline{\rm MS}}/\Lambda_L$ is an action-specific one-loop constant computed per action (Kawai–Nakayama–Seo for Wilson). The claim is that the model's action has one too, that it is $O(1)$ rather than Wilson's $\sim29$ because its tadpole sector is exactly empty, and that the value the model's own $g_s=\tfrac12$ lock needs lies inside the resulting bracket. It bears directly on $\alpha_s(M_Z)$, which is why it rolls up to CL022.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F280-d1-subtracted-against-wilson.md` | the master identity (differences only), the measure-invariant estimator, the three-leg budget, the band | bracketed |
| test record `F280-d1-subtracted` (tier gate, entry `check_d1_subtracted`) | 6/6 PASS; S1 residual $6.7\times10^{-16}$, S2 invariance $3.1\times10^{-15}$, S3 propagator leg $1/n^2$-convergent | exact / quantitative |
| `findings/F155-qstar-self-energy-and-freeze-bracket.md` | A0 — the rule's tadpole sector is *exactly* empty ($u_0\equiv1$), which makes leg 1 structural | exact |
| `findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md` | the Wilson loops-only constant $C_\text{lat}=6.138643$ and the analytic $C_{\overline{\rm MS}}=131/66$ the band's upper edge is built from | quantitative |
| `findings/F287-bgfield-apparatus-sound-post-F277.md` | §6 — the restriction that forbids an absolute normalisation, and §4's measured 5.3–5.7$\times$ rule-beats-Wilson ordering the monotonicity assumption leans on | quantitative |

## Falsifier

A completed computation of the rule's $\cos(k/2)$-dressed 3-gluon $+$ ghost vertex form factors that returns $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ **outside $[1,\ 7.980]$** — equivalently a vertex leg outside $[-2.257,\ -1.446]$ in $\Delta C$ units. Which edge is crossed says which premise died: below $1$ means $\Delta C_\text{rule}^\text{loops}<0$ and the monotonicity assumption is wrong; above $7.980$ means the rule's loops-only constant exceeds Wilson's and the $g_s=\tfrac12$ lock is wrong.

## Status & history

`open` — the band is a bracket, and the number inside it is not yet computed. The gap this card fills is that the *route* to that number changed on 2026-08-05: F287 had forbidden taking $d_1$ from the quadrature's absolute normalisation, leaving the item apparently blocked behind F267's fundamental-domain question, and F280 shows it is not — the subtracted formulation reaches the same object without one. What the card asserts is therefore weaker than a value and stronger than "open": a two-sided bracket with a stated falsifier, plus the statement that the open piece is now 36.2% of the required shift rather than all of it.

The cheapest way to narrow this is **not** new physics: F163's own item (a), the $Q\to0$ high-resolution extrapolation of Wilson's loops-only $C_\text{lat}$, halves the width on the vertex-leg target without moving the total.

## Sources

- `findings/F280-d1-subtracted-against-wilson.md`
- `findings/F287-bgfield-apparatus-sound-post-F277.md` §6
- `findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md`
- `docs/status/completeness-2026-08-04.md` — gap #3, the step this executes
- Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40 — the Wilson anchor
