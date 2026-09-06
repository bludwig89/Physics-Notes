---
id: CL300
title: 'Under F130''s fixed-lambda bond-moving convention, no finite-order strong-coupling fluctuation correction to the block-spin confinement eigenvalue can supply a non-integer exponent: every order is exactly integer, and the composite quantity such an expansion could define is scheme-dependent, not universal'
slug: blockspin-fluctuation-corrections-stay-integer
tier: supporting
kind: no_go
status: live
domain: [QCD, cosmology]
exactness: exact
findings: [F362, F130, F310]
tests: [F362-blockspin-fluctuation-eigenvalue]
modules: [src/casim/engine/interactions/cosmology_blockspin_fluctuation.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-09-04
last_verified: 2026-09-04
provenance: authored
review_state: authored
confidence: high
---

# CL300 — Fluctuation corrections to the block-spin confinement eigenvalue stay integer, structurally, under F130's fixed-$\lambda$ bond-moving convention

## Statement

F130 C1 measured the model's confinement (string-tension) block-spin RG eigenvalue at $\lambda=0$
(the frozen flux tube, no plaquette fluctuations): $\lambda_\sigma=b$ exactly. This closes the
candidate route open-derivations row **G2** / rubric **K3**/**K12** named for supplying the
primordial tilt's anomalous dimension $\gamma$ (F310): adding the fluctuation correction the
$\lambda=0$ limit dropped, via the repo's own exact strong-coupling perturbation theory
(`link_hamiltonian.sigma_strong_pt2`, $c_2(g^2)=1/(6g^2)$ exact), does **not** move the eigenvalue
off $b^1$, and **cannot under that same convention** ($g^2\to bg^2$, $\lambda$ held fixed —
F130's own bond-moving rule, reused unmodified, not a full Migdal–Kadanoff decimation step
that would let $\lambda$ flow; see F362 §4a), for two independent, structural reasons:

1. **Every order is integer.** The strong-coupling series $\hat\sigma=\sum_n a_n\lambda^{2n}(g^2)^{1-2n}$
   carries an exact eigenvalue $b^{1-2n}$ at every order $n$ under bond-moving — $b^{-1},b^{-3},b^{-5},\dots$
   for $n\ge1$ — never a non-integer value, at any order, to all orders. This generalises F130
   C3/C4's "a linear block average is a Gaussian calculation" to the *entire* expansion around
   $\lambda=0$, not only its leading term.
2. **The one composite quantity this expansion can define at a finite blocking step is not
   scheme-independent.** Writing $\gamma_\text{eff}(b)=\log_b[\hat\sigma(bg^2,\lambda)/\hat\sigma(g^2,\lambda)]-1$,
   tuning it to a target value at one $b$ gives a *different* value at every other $b$ (30–82% spread
   across $b=2$–$5$ at every tuning tested) — failing the definition of a universal critical exponent
   regardless of which coupling is used.

The model's own calibrated confinement coupling ($g_s^2=\tfrac14$, F115/F325; $\lambda=\Omega^2$,
F101) additionally sits at $\varepsilon=\lambda^2/(3g^4)\sim5$–$15$, one to two decades past this
expansion's validity radius ($\varepsilon\ll1$) — the truncated string tension is negative
(unphysical) there — but this is a secondary point; reason 2 holds regardless of coupling.

## What it extends

Directly extends [[F130-blockspin-rg-gauge-gravity]] C1/C3/C4 (all-integer measured spectrum,
"round-off-floor identity" of a linear block average) to the *fluctuation-corrected* eigenvalue, and
answers [[F310-gamma-is-a-blockspin-eigenvalue]] falsifier 1 / `docs/claims/CL267-tilt-is-a-blockspin-eigenvalue.md`
falsifier 2 directly: the fluctuation-corrected computation those findings named as the single
highest-value next step was run, and returns exactly $\lambda_\sigma=b^1$ (structurally, not as a
numerical coincidence).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` C1 | $c_2(g^2)=1/(6g^2)$, matched to `sigma_strong_pt2` (real Kogut–Susskind diagonalisation) at 5 points to the float floor | exact |
| `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` C2 | term$_n$ eigenvalue $=b^{1-2n}$; $n=1$ relative eigenvalue $b^{-2}$ reproduces `blockspin.magnetic_deformation_ratio`'s independent measurement | exact (identity) + quantitative (cross-check, $<2\%$) |
| `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` C3 | $\gamma_\text{eff}(b)$ non-universal, 30–82% spread across $b=2$–$5$ at every tuning | quantitative |
| `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` C5 | model's own coupling gives $\varepsilon\sim5$–$15$, non-perturbative; truncated $\hat\sigma<0$ there | computed |
| `test-results/F362_blockspin_fluctuation.json` | 4/4 checks PASS, registry record `F362-blockspin-fluctuation-eigenvalue`, tier gate | — |

## Falsifier

**Any computation that returns a non-integer, $b$-independent eigenvalue for the confinement
sector** falsifies this claim's practical force (the universality test §C3 of F362 applies to any
candidate, not only the perturbative one tested here) — this includes, and is not limited to, a
non-perturbative (resummed, or genuinely distinct-fixed-point) treatment at fixed $\lambda$. A full
Migdal–Kadanoff decimation step that lets $\lambda$ itself flow and mix into new couplings (F362
§4a) is a live, untested route and would also count, even carried out only perturbatively in the
new couplings, since it falls outside the fixed-$\lambda$ convention this claim is scoped to.
Anything built as a further finite-order term of the *same* fixed-$\lambda$, $\lambda=0$ expansion is
excluded in advance by C2's power counting and would not constitute a falsifier.

## Status & history

`status: live`. This is a clean structural result, not contingent on the model's specific coupling
values (§ Statement, reason 2 holds regardless). It narrows — but does not resolve — the
contingency `docs/claims/CL267-tilt-is-a-blockspin-eigenvalue.md` carries: CL267's own falsifier 2
named exactly this computation, and it has now been run and found to confirm $\lambda_\sigma=b^1$
rather than move off it. CL267 is updated to record this (§ its own "Status & history"); CL267
itself is not withdrawn, since its overall identification ($\gamma\equiv y-1$, contingent on the
$t{=}0$ measure being critical) does not depend on which mechanism (if any) supplies the eigenvalue's
value.

## Sources

- `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md`
- `findings/F130-blockspin-rg-gauge-gravity.md`
- `findings/F310-gamma-is-a-blockspin-eigenvalue.md`
- `findings/F101-strong-coupling-sigma-compact-rotor.md` (the $\lambda=\chi\Omega^2$ mapping and $\Omega$ values used in C5)
- `docs/status/open-derivations.md` row **G2**
- `docs/claims/CL267-tilt-is-a-blockspin-eigenvalue.md`
- Migdal–Kadanoff recursion relations for lattice gauge theories (bond-moving + decimation generates flowing/mixed couplings; not performed here — F362 §4a): e.g. *Renormalization group equations in lattice gauge theories*, Nucl. Phys. B (1978), https://www.sciencedirect.com/science/article/abs/pii/0550321378902821 ; *Migdal–Kadanoff recursion relations in SU(2) and SU(3) gauge theories*, Nucl. Phys. B (1981), https://www.sciencedirect.com/science/article/abs/pii/0550321381904910
