---
id: CL021
title: 'The cosmological constant is not derived — the 121-order problem is reduced to the Omega_Lambda coincidence'
slug: 'cosmological-constant-not-derived'
tier: headline
kind: non_claim
status: not_claimed
domain: [cosmology, GR]
exactness: quantitative
findings: [F164, F193, F196, F241, F319]
tests: []
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: none
first_issued: '2026-08-02'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL021 — The cosmological constant is not derived — the 121-order problem is reduced to the Omega_Lambda coincidence

## Statement

The cosmological constant is **not derived**. F193/F196 reduce the classic 121-order problem to the $\Omega_\Lambda\approx0.69$ coincidence, **which is not the same as explaining it**.

**Narrowed 2026-08-18 — the reduction rests on F193 §B/F196, not on F193 Part A.** F193's Part A route to a
zero bare CC (the beable vacuum) is a **uniform** deletion of the $\tfrac12$-per-mode $c$-number, and
CL275 excludes that class: F59 Part C builds $1/16\pi G$ out of the same $\tfrac12$, so the deletion
takes F79's $G$ with it. What survives, and what carries the $121$-order reduction, is the **capacity
ceiling** — F193 Part B's holographic dilution with F196's derived $p=2$, landing on
$\rho_\text{crit}=3c^4/8\pi GR_H^2$ — which is order-selective by construction because the bound *contains*
$G$. That ceiling is a **consistency requirement, not a suppression mechanism** (F241), so the card's
position is unchanged and if anything better supported: what is missing is now a mechanism *and* an $O(1)$,
not an $O(1)$ alone.

## What it extends

Recorded so that **absence is not read as a prediction**. This is a scope boundary, not a result: the project does not assert it, and `status: not_claimed` is the assertion that it does not assert it. The reduction is a real result — F164 quantified the 120.8-order overshoot, F193 recast the observed $\rho_\Lambda$ as an IR-diluted back-reaction, and F196 derived the dilution exponent $p=2$ from the model's own Schwarzschild law and area entropy — but the residual is a coincidence, not a derivation, and the card refuses the stronger reading. Since 2026-08-18 it refuses one more: **that the bare CC is zero in the ontology**. That was F193 Part A, and it is excluded by CL275.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md` | The bare overshoot quantified: $\log_{10}=120.8$, sign also wrong | quantitative |
| `findings/F193-ontic-vacuum-gravitates-as-zero.md` **§B** | The observed $\rho_\Lambda$ as an IR-diluted back-reaction: one factor of $(a/R_H)^2=5.958\times10^{-121}$ reproduces the overshoot to $0.54$ dex | computed |
| ~~`findings/F193-ontic-vacuum-gravitates-as-zero.md` **Part A** — beable $T^{00}$ on the empty lattice is exactly 0, so the bare CC vanishes in the ontology, killing both magnitude and sign~~ | **Withdrawn as evidence 2026-08-18.** The deletion is uniform in the heat-kernel order and takes $1/16\pi G$ with it — CL275. The finding is not superseded; this card no longer rests on that leg | ~~exact~~ |
| `findings/F241-omega-lambda-o1-residual-anthropic.md` | The surviving route fixes a **ceiling** $\rho\le\rho_\text{crit}$, not a value; the sub-unity factor is the coincidence problem | quantitative |
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §6 | Why Part A cannot be the route: $1/16\pi G$ and $\rho_\text{vac}$ are two moments of one zero-point sum | exact in form, computed in value |
| `findings/F196-dilution-exponent-derived.md` | $p=2$ derived two ways; residual $0.10$ dex from $\rho_\Lambda$, leftover $=\Omega_\Lambda\approx0.69$ | quantitative |

## Falsifier

None on the non-claim. The **component** results are live supporting claims carried by their backfill cards and are falsifiable individually — F196's $p=2$, and F241's ceiling (CL212). F193's "exact zero" is **no longer among them**: as of 2026-08-18 it is excluded rather than open, by CL275.

## Status & history

`not_claimed`. Recorded in the summary's Scope section from revision 2 (2026-08-02), unchanged by revision 3, and sharpened by revision 5 (2026-08-18 - 16:35), which added the CL275 no-go to the same entry.

**Amended 2026-08-18 - 17:15 — one Evidence row withdrawn; the card's position does not move.**
`completeness-2026-08-18` **Amendment 4** adjudicated the F311-vs-F319 disagreement in rubric row **K9**,
and the adjudication reaches this card: it was citing F193 **Part A** as `exact` evidence for a leg that
headline card CL275 excludes — the two headline cards were asserting opposite things about the same
leg since 2026-08-16, and nothing in the gate can see that, because `check_claims.py` tests supersession
and vocabulary, not agreement between cards. The row is withdrawn in place rather than deleted (the
retraction record is the point of this layer), F193 §B is stated separately from Part A, and F241/F319 are
added so the card names the route that actually carries the reduction. **`status: not_claimed`,
`falsifier: none` and `exactness: quantitative` are unchanged, and no finding was edited.**

## Sources

- `findings/F193-ontic-vacuum-gravitates-as-zero.md`
- `findings/F196-dilution-exponent-derived.md`
- `findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md`
- `findings/F241-omega-lambda-o1-residual-anthropic.md`
- `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §6
- `docs/status/completeness-2026-08-18.md` — Amendment 4
- `papers/Claims-and-Falsifiers-Summary.md` — Scope
