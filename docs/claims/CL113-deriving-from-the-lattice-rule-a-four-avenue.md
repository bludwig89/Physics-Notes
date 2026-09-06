---
id: CL113
title: 'Deriving $\alpha_\text{em}$ from the lattice rule: a four-avenue no-go, characterized'
slug: 'deriving-from-the-lattice-rule-a-four-avenue'
tier: supporting
kind: no_go
status: live
domain: [SM, QFT]
exactness: quantitative
findings: [F127, F339, F349]
tests: [F127-alpha-em-derivation, F339-alpha-em-reopening-conditions, F349-alpha-em-convergent-stiffness-evidence]
modules: []
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: none
first_issued: '2026-08-04'
last_verified: '2026-09-02'
provenance: extracted
review_state: authored
confidence: medium
---

# CL113 — Deriving $\alpha_\text{em}$ from the lattice rule: a four-avenue no-go, characterized

## Statement

$\alpha_\text{em}$ cannot currently be derived from the lattice rule. Four avenues were tried
(Sakharov-style induced coupling; an $O(1)$ lattice scale near the EW matching point; topological
charge quantization fixing the coupling; structural/impedance normalization) and all four produce
sharp or inconclusive negatives (F127). F339 names, for each avenue, the one assumption whose
failure would reopen it, using three findings that post-date F127 — and finds two of the four
reopening conditions are now *narrower* than F127 stated (avenues A and B), one is *confirmed and
precisely bounded* (avenue D), and one is a *genuinely unexplored* fifth-avenue candidate rather
than a closed door (avenue C, the Dirac-monopole/quantized-magnetic-charge route — never
constructed in this model). $\alpha_\text{em}$ remains the model's last irreducible dimensionless
input.

## What it extends

This is a **no-go** against deriving the Standard Model's fine-structure constant $\alpha_\text{em}$
from first principles within this lattice model — the electromagnetic analogue of the coupling
derivations that *do* succeed elsewhere in the project ($\sin^2\theta_W=1/4$ bare, F45; $g_s^2\chi=1/4$,
F115-CM3). The bar this card meets (`docs/claims/README.md`): it names the specific established
result (deriving a fundamental coupling constant from a more basic theory) the model does **not**
yet reach, and states precisely why not, avenue by avenue.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F127-alpha-em-derivation-four-avenue-nogo.md` | The four avenues and their original verdicts | quantitative |
| `findings/F339-alpha-em-nogo-reopening-conditions.md` | The reopening condition for each avenue; independent re-derivation of the hypercharge rank-6/7 result (avenue D, genuinely independent — rebuilds F279's six-row system from scratch); a re-check of the tensor-algebra tautology behind Ward transversality (avenue A — the harder model-specific result stays credited to F251/F277 alone, per the 2026-08-31 review); the $\mu_\star=4\pi v$ correction to avenue B; the zero-mentions check establishing avenue C's monopole route is unexplored, not excluded | quantitative (hypercharge rank is exact; the $\mu_\star=4\pi v$ agreement is quantitative) |
| `findings/F349-alpha-em-induced-stiffness-convergent-evidence.md` | An independent, previously-uncited evidence line (F41/F143/F147/F149/F153, all 2026-06, not cited by F339) corroborating avenues A and D by a disjoint mechanism: F143/F147 prove the induced gauge stiffness from any free-fermion loop is exactly zero, all orders, all channels (not a one-loop transversality check); F41 supplies the structural reason avenue D found "no constraint" (U(1)_Y has no bare kinetic term at all); F149/F153 show the condensate-sector route is attempted and exhausted at the perturbative-proxy level, narrowing avenue D's residual attack surface to the specific non-perturbative F118 self-energy | machine precision (F143/F147 residuals $\le10^{-11}$) + exact rational recomputation |

## Falsifier

**None — structural, and here is why.** A no-go against a derivation is not falsified by an
experiment; it is falsified by *finding the derivation*, i.e. by one of the two concrete attack
surfaces F339 names actually closing: (1) constructing a Dirac-monopole-type soliton on the BCC
lattice whose magnetic charge is independently fixed by lattice geometry, giving $\lvert e\rvert$
via Dirac quantization (avenue C); or (2) computing the vertex/overlap-integral F127's own avenue F
proposed, from the composite photon bilinear (F89) against an external fermion (avenue D/F). F349
narrows attack surface (2): the generic vertex/overlap-integral calculation has, in a closely
related form (the wrap/walk-loop stiffness, not literally the F89 construction), already been
attempted and exhausted at the perturbative level (F143/F147/F149/F153) — the honest remaining
form of (2) is specifically the non-perturbative $E_g$ condensate self-energy (F118) propagated
through the same wrap-stiffness channel, not a generic unattempted vertex calculation. Naming these
as the reopening conditions is what makes `falsifier: none` honest rather than a shrug — see
`docs/claims/README.md`'s definition (structural, no observational falsifier, reason stated).

## Status & history

`live`: the no-go holds as stated, and stronger than in 2026-08-04 for two of its four legs.

- **2026-06-10 (F127):** four avenues tried, all negative or inconclusive, from general QED
  reasoning and the model's charge-spectrum/impedance structure.
- **2026-08-04:** card seeded mechanically as `unreviewed-seed`; classification not confirmed.
- **2026-08-31 (F339):** re-examined per the D#14 ledger prompt. Avenue A's Ward-identity premise
  was already computed in-model by F251/F277 (not imported QED lore, as F127 had it) — F339 names
  this as the narrower reopening condition but only independently re-checks the trivial
  tensor-algebra corollary, not F251/F277's harder fermion-loop result (caught by the 2026-08-31
  adversarial review, `docs/reviews/F339-review-2026-08-31.md`, verdict CONFIRMED-NARROWER; the
  finding text was corrected accordingly). Avenue B's "no structural threshold" premise is *superseded* by F138
  ($\mu_\star=4\pi v$ exactly) but the correction does not help derive $\alpha$ — it folds avenue B
  into ledger row D#17 (deriving $v$), not D#14. Avenue D is confirmed still open and precisely
  bounded: F165/F279 close hypercharge *ratios* only (rank 6 of 7), independently re-derived here.
  Avenue C's topological route is flagged as genuinely unexplored (zero prior mentions of
  monopoles/Dirac quantization anywhere in the project), not attempted. Card promoted to
  `review_state: authored`, `falsifier` set from `unset` to `none` (with reason), domain corrected
  from `[SR]` to `[SM, QFT]`.
- **2026-09-02 (F349):** independent convergent-evidence check, found before F339 in this session's
  own search and folded in rather than duplicated. Corroborates avenues A and D via a disjoint,
  previously-uncited line (F41/F143/F147/F149/F153) — F143's transverse-channel no-go and F147's
  one-tick rigidity theorem are exact and non-perturbative (stronger in kind than F251/F277's
  one-loop transversality check, though they do not touch F339's residual compositeness/form-factor
  loophole); F41 explains avenue D's "no constraint found" structurally; F149/F153 show the
  condensate-sector route was tried and exhausted at the perturbative-proxy level (the physical
  condensate coupling is $O(1)$, outside that proxy's validity), narrowing falsifier attack surface
  (2) above accordingly. No new number for $\alpha_\text{em}$; grade unchanged.

## Sources

- `findings/F127-alpha-em-derivation-four-avenue-nogo.md`
- `findings/F339-alpha-em-nogo-reopening-conditions.md`
- `findings/F349-alpha-em-induced-stiffness-convergent-evidence.md`
- `docs/status/completeness-2026-08-20-prompts.md` (D#14 ledger prompt)
- `docs/claims/README.md` — the `no_go` / `falsifier: none` contract
