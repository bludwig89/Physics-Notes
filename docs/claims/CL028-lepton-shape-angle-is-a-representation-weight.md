---
id: CL028
title: 'The charged-lepton condensate angle IS the E_g representation weight, delta* = 2/9 rad'
slug: 'lepton-shape-angle-is-a-representation-weight'
tier: headline
kind: derivation
status: live
domain: [SM]
exactness: exact
findings: [F175, F234, F253, F255, F256]
tests: [F234-Wvc-triple-closure]
modules: [casim.engine.particles.eg_sextic]
constants: [delta_star, lambda6]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-07-16'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL028 — The charged-lepton condensate angle IS the E_g representation weight, delta* = 2/9 rad

## Statement

The charged-lepton condensate angle equals the second-shell $E_g$ **representation weight**,
$$\delta^*=\frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\tfrac29\ \text{rad (exact }O_h).$$
The canonical $E_g$-plane angle **is** the weight it carries — weight-as-phase. $\delta^*=\tfrac29$ is **primary**; the sextic clock coupling $\lambda_6=0.243$ (equivalently $W=6\lambda_6=1.46$) is an **output** via $\lambda_6=\lvert B\rvert/(2e^6\cos\tfrac23)$, not a fit. The whole charged-lepton shape then follows from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ to $\le0.007\%$ with **zero shape parameters**.

## What it extends

The Standard Model's charged-lepton mass ratios, which are free inputs. Together with CL005 ($Q=\tfrac23$ fixes the *equipartition*) this fixes the *shape*; the overall *scale* remains an input (CL016's neighbour — see F119).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F175-lattice-2-9-eg-weight.md` | $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$, exact $O_h$ | exact |
| `findings/F255-generator-norm-fixed-by-F118-schur.md` | $R=1$ **forced** by Schur-isotropy of the $E_g$ irrep metric — the angle is a genuine radian, derived not posited | exact |
| `findings/F253-weight-as-phase-scale-nogo.md` | A scale-free topological origin is **excluded**; the only holonomy is $2\pi/3$ | exact (no-go) |
| `findings/F256-lambda6-sextic-derivative-nogo.md` | The dynamical Landau route **cannot** give exact $3\delta^*=Q$; independent sea-$B$/induced-$C$ origins ⇒ a $1.7\times10^{-5}$ near-coincidence | exact (no-go) |
| `findings/F234-Wvc-triple-closed-delta-2-9-pins-brake.md` | The $(W,v,c)$ triple closure; $\lambda_6$ as an output of $\delta^*$ | exact |

Gate record `F234-Wvc-triple-closure`; constants `delta_star`, `lambda6`.

## Falsifier

A charged-lepton mass measurement inconsistent with the $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ shape at better than $0.007\%$. Because $\delta^*$ is an exact rational fixed by $O_h$ representation theory, there is **no** parameter to re-fit — the two no-gos (F253, F256) closed the alternatives deliberately, which is what makes this falsifiable rather than adjustable.

## Status & history

`live` since 2026-07-16 as **founding decision 7** in `CLAUDE.md`. **Supersedes F179/CN3**, under which the lepton spectrum was a one-angle *fit* with $\delta^*$ granted rather than derived. Adopted because every alternative is closed, not because it fits best — F253 and F256 are the closures.

**Summary gap, opened and closed on the same day.** This card was authored 2026-08-04 because `papers/Claims-and-Falsifiers-Summary.md` did not carry the claim at all: weight-as-phase became a founding principle on 2026-07-16, and revision 3 — issued seventeen days later — did not include it. **Revision 4 (2026-08-04) adds it as core claim 11**, with the $0.007\%$ shape threshold as a stated falsifier. That the gap existed for nineteen days without being visible anywhere is the concrete case for the claims layer: nothing in `findings/` was wrong, and the project's public statement of what it asserts was simply missing a founding principle.

## Sources

- `findings/F175-lattice-2-9-eg-weight.md`
- `findings/F255-generator-norm-fixed-by-F118-schur.md`
- `findings/F253-weight-as-phase-scale-nogo.md`
- `findings/F256-lambda6-sextic-derivative-nogo.md`
- `findings/F234-Wvc-triple-closed-delta-2-9-pins-brake.md`
- `CLAUDE.md` — Core Design Decision 7
- `docs/theory/key-decisions.md`
