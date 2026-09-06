---
id: CL301
title: 'The F228/F238 geon / one-cell Planck-mass black-hole remnant dark-matter candidate''s free abundance input carries two named 2025 gravitational-wave constraints of unequal strength: an order-of-magnitude formation-mass ceiling $M_\text{form}\lesssim1.6\times10^8$ g (from early-merger GW bounds, caveated), and a weaker, convention-sensitive non-Gaussianity plausibility argument on whatever sources the relic-forming perturbations (from the LIGO O3 exclusion of Gaussian-sourced Planck relics)'
slug: geon-relic-abundance-bounded-by-2025-gw-literature
tier: supporting
kind: prediction
status: open
domain: [cosmology]
exactness: bracketed
findings: [F365, F228, F238, F223]
tests: [F365-geon-relic-gw-bounds]
modules: [src/casim/engine/interactions/cosmology_geon_relic_gw_bounds.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-04'
last_verified: '2026-09-04'
provenance: authored
review_state: authored
confidence: medium
---

# CL301 — The F228/F238 geon relic abundance input carries two 2025 GW constraints of unequal strength

## Statement

The F228 geon / one-cell Planck-mass black-hole remnant dark-matter candidate's formation
fraction $\beta(M_\text{form})$ (F228 Sec. 4), previously left as "a genuinely free input"
(F238, CL209), now carries two named, previously-unchecked 2025 literature constraints of
**unequal strength**: (i) an order-of-magnitude formation-mass ceiling
$M_\text{form}\lesssim1.6\times10^8$ g, from combining F228's own $\beta(M_\text{form})$ formula
with the Domènech–Lin–Sasaki early-merger gravitational-wave bound of arXiv:2506.16154 — caveated
by that paper's own statement that the bound assumes a monochromatic PBH mass function it flags as
possibly unrealistic; and (ii) a **weaker, convention-sensitive** non-Gaussianity plausibility
argument — F238's own required amplitude $\sigma_\text{req}(M_\text{form})\approx0.058$–$0.079$
lands in the same broad regime, but not robustly inside, the $P_\mathcal{R}\sim10^{-2}$–$10^{-1}$
band that arXiv:2509.20533 associates with LIGO-O3 exclusion of Gaussian curvature statistics: using
that paper's own two internal $\sigma\leftrightarrow P_\mathcal{R}$ conventions (its Eq. 9 vs. its
Eq. 10, which the paper itself uses for its own headline number) moves the result across the band's
stated edge, so this half is a same-order-of-magnitude placement, not a quantitative hit.

## What it extends

Extends the model's own dark-matter candidate (F216/F223/F228, cosmology/GR-adjacent, not a
Standard-Model or QFT result) by placing it against two 2025 primordial-black-hole /
gravitational-wave results from the literature it had not previously been compared to. It derives
no new Standard Model or GR result itself; it is a quantitative-to-bracketed literature-comparison
narrowing (unevenly) the parameter space of an existing model-native claim.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F365-geon-relic-gw-bounds-sharpen-k7.md` | Full derivation, including its "Reviewed & corrected" section documenting the 2026-09-04 attack pass that downgraded the non-Gaussianity half from an initial overstated claim | mixed: quantitative (ceiling) / bracketed (non-Gaussianity) |
| `tests/registry/interactions.yaml` → `F365-geon-relic-gw-bounds` | 6/6 PASS under corrected, honestly-widened criteria (tier: battery) | quantitative / bracketed, mixed |
| `test-results/F365_geon_relic_gw_bounds.json` | Numeric results: ceiling masses, ratios, both $P_\mathcal{R}$ conventions | quantitative |
| `findings/F228-geon-production-and-stability.md` | The $\beta(M_\text{form})$ formula this card's ceiling is built on | order-of-magnitude |
| `findings/F238-geon-relic-abundance.md` | The $\sigma_\text{req}(M_\text{form})$ formula this card's non-Gaussianity argument is built on | quantitative (Press-Schechter arithmetic) |

## Falsifier

Two, matching the finding's Sec. 6, of unequal reach:

1. **Formation-mass side (the stronger falsifier).** If a future refinement of the early-merger GW
   bounds (DLS/PVL-type, or their successors) pushes the formation-mass ceiling below the minimum
   mass at which "formation then evaporation to a remnant" is a meaningful description at all
   ($M_\text{form}\gtrsim M_\text{Pl}$), the PBH-remnant production route closes entirely and
   F228's "only viable route" verdict would need a genuinely new mechanism.
2. **Statistics side (the weaker falsifier — named, not established here).** If the (currently
   unbuilt) inflaton/primordial-spectrum sector this model would need (F238 Sec. 6, K4/K5 EXCLUDED
   per F282) is ever constructed and is shown to produce **Gaussian** statistics at the
   PBH-formation scale, a genuine tension with the existing LIGO O3 bound becomes worth computing
   directly from that sector's own spectrum — this card names the check but, per the finding's
   Sec. 5 correction, does not itself establish the exclusion (the $P_\mathcal{R}$ placement used
   here is convention-sensitive and only same-order-of-magnitude).

Neither falsifier has fired; both are stated so a future session can check them without
re-deriving this card's arithmetic.

## Status & history

`open`: asserted with evidence of two different strengths, and both gaps are explicitly named —
(a) the formation-mass ceiling (falsifier 1) is the more robust half but is itself contingent on
the DLS bound's own stated monochromatic-mass-function assumption; (b) the $P_\mathcal{R}$
placement (falsifier 2's basis) was **originally overstated** ("all three land squarely inside the
band") and was corrected at the 2026-09-04 review-finding attack pass to a weaker, convention-
sensitive plausibility argument once it was checked against the source paper's own two internal
transfer-function conventions — see `findings/F365-geon-relic-gw-bounds-sharpen-k7.md`'s "Reviewed & corrected" section for the
full record. This card does not change K7's rubric grade (PARTIAL, unchanged) or reopen K8's
abundance verdict (F238/CL209, unchanged) — it narrows the free-input's parameter space along two
axes of unequal strength without deriving a non-tunable $\Omega_\text{DM}$.

**Date first issued:** 2026-09-04, alongside `findings/F365-geon-relic-gw-bounds-sharpen-k7.md`.
**Corrected:** 2026-09-04, same day, after the finding's own review-finding attack pass (see that
finding's "Reviewed & corrected" section) — the card's original `exactness: quantitative` and the
"squarely inside"/"independently falsifiable" framing of falsifier 2 are revised here to match the
finding's corrected content, rather than superseding a separately-issued version of this card.

## Sources

- `findings/F365-geon-relic-gw-bounds-sharpen-k7.md`
- `findings/F228-geon-production-and-stability.md`
- `findings/F238-geon-relic-abundance.md`
- Cheek, Ghoshal & Heurtier, "Comprehensively Constraining Ultra-Light Primordial Black Holes
  Through Relic Formation and Early Mergers," arXiv:2506.16154 (2025)
- "Gaussian Planck Relics are Ruled-Out as Dark Matter by LIGO," arXiv:2509.20533 (2025)
