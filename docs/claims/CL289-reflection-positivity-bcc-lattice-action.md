---
id: CL289
title: 'Link reflection positivity holds for the BCC3xZ lattice gauge action, for any compact group and any beta_s, beta_t >= 0'
slug: 'reflection-positivity-bcc-lattice-action'
tier: supporting
kind: derivation
status: open
domain: [QCD, QFT]
exactness: machine
findings: [F335, F265, F323, F313, F94]
tests: [F335-reflection-positivity-bcc, F335-reflection-positivity-gram]
modules: [casim.engine.gauge.reflection_positivity]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-30'
last_verified: '2026-08-30'
provenance: authored
review_state: authored
confidence: medium
---

# CL289 — Link reflection positivity holds for the BCC3xZ lattice gauge action

## Statement

The BCC3xZ lattice gauge action (F265's 6 spatial rhombi + F323's 4 mixed space-time
rectangles, on BCC-space x Z-time) satisfies the three structural hypotheses the
Osterwalder-Seiler (1978) / Menotti-Pelissetto (1987) link-reflection-positivity theorem
needs for the standard (non-heat-kernel) Wilson action: nearest-neighbour-only time
coupling, purely-spatial loops confined to one time-slice, and mixed loops crossing
exactly one time-step with their temporal legs entering linearly. None of these
hypotheses, or the Peter-Weyl factorization proof behind them, references the spatial
lattice's connectivity, so the theorem -- established for hypercubic lattices -- carries
over to BCC-space x Z-time unmodified. This holds for any compact gauge group and any
beta_s, beta_t >= 0; it does not depend on the specific anisotropy F323 derives.

## What it extends

Extends Osterwalder & Seiler's 1978 lattice-gauge-theory reflection-positivity result
(and Menotti & Pelissetto's 1987 site-reflection generalisation) to a non-hypercubic
spatial lattice for the first time in this tree -- and, as far as this session's
literature search found, states explicitly what those papers leave implicit: that the
argument is topological in the time direction alone and never uses the spatial
lattice's structure. It is a necessary ingredient for Osterwalder-Schrader reconstruction
(a genuine Hilbert space and a bounded self-adjoint transfer matrix) for THIS model's own
lattice gauge theory, not a re-derivation of the general theorem from first principles.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F335-reflection-positivity-bcc-lattice.md` Sec. 2 | the three hypotheses hold exactly, read off `BCC4_LOOPS`/`_stored` with no randomness | exact |
| same, Sec. 2.1-2.3 | the reflection map is an exact involution (0.0); the mixed-rectangle trace identity holds to 4.5e-16; the declared control (`broken_dagger`) reddens the one leg (`M1`) that depends on it | machine |
| same, Sec. 3 | SU(2) Wilson character coefficients a_j(beta) = I_2j(2 beta) - I_2j+2(2 beta) > 0 for all beta>0, j>=0 -- closed form via Bessel recursion, verified by direct Haar-measure quadrature | exact (supplementary; not required by the main argument) |
| same, Sec. 4 | the reflection Gram matrix's dominant eigenvalue is positive by 3-4 orders of magnitude over noise at three coupling points including the model's own derived anisotropy; nine near-zero sub-leading directions are statistically consistent with zero (2.5-4.1 sigma), not a stable violation | quantitative, honestly bounded -- NOT claimed as confirmation of those nine directions |

## Falsifier

A demonstrated violation of any of the three structural hypotheses in a future engine
change (a longer-range temporal hop, or a mixed loop spanning two time-steps) would
break the argument at the leg that checks it (`H1`-`H4`). A demonstrated sign or
indexing error in the reflection map beyond machine precision (`I1` or `M1` failing to
vanish) would directly contradict it. A stable, growing-with-statistics negative
eigenvalue in the Sec. 4 Gram construction -- not a single run at a few sigma, but a
trend across increasing statistics or volume -- would directly contradict it and require
revisiting the structural argument. `falsifier: stated`.

## Status & history

`status: open`. This card establishes a necessary ingredient (reflection positivity),
not a confinement proof: no mass gap, no area law, no string-tension verdict is claimed
or implied. Completeness row B7 (confinement) narrows from "no positivity machinery
exists in the tree" to "the machinery exists and the model's own action satisfies it; a
strong-coupling or cluster-expansion argument on top of the now-available transfer
matrix is the next step toward an actual proof." That next step is not attempted here
and is the open residual this card leaves. Companion to `CL087` (the 3+1D Monte-Carlo
engine on this same lattice, `status: narrowed`) and `CL006` (the headline confinement
card, 2D exact / 3+1D dual-superconductor picture) -- neither is superseded or narrowed
by this card, which adds a structural result orthogonal to both.

## Sources

- `findings/F335-reflection-positivity-bcc-lattice.md`
- `src/casim/engine/gauge/reflection_positivity.py`
- Osterwalder, K. & Seiler, E., "Gauge Field Theories on the Lattice," Ann. Phys. 110 (1978) 440.
- Menotti, P. & Pelissetto, A., "Osterwalder-Schrader Positivity for the Wilson Action," Commun. Math. Phys. 113 (1987) 369.
- Faizal, M., Ali, A. F. & Alshal, H., arXiv:2606.19362 (2026) -- cited for its Sec. 2.1 restatement of the factorization argument only.
- `findings/F265-bcc-gauge-action-blindness.md`, `findings/F323-anisotropy-derived-and-d4-casimir.md`, `findings/F313-one-time-dimension-from-the-update-commutant.md`
