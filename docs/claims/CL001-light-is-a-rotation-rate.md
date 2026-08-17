---
id: CL001
title: 'The speed of light is a rotation rate, not a phase velocity'
slug: 'light-is-a-rotation-rate'
tier: headline
kind: reinterpretation
status: live
domain: [SR, QM]
exactness: exact
findings: [F25, F26]
tests: []
modules: [casim.engine.gauge.wmu]
constants: [c_lat]
supersessions: []
reviews: [docs/reviews/F25-review-2026-08-04.md]
rolls_up_to: null
falsifier: none
first_issued: '2026-06-08'
last_verified: '2026-08-04'
provenance: authored
review_state: authored
confidence: high
---

# CL001 — The speed of light is a rotation rate, not a phase velocity

## Statement

$c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf E,\mathbf B)$ vector pair per unit spatial wavenumber,
$$c_\text{lat}=\frac{d\Omega}{d\lvert\mathbf k\rvert}\bigg\rvert_{\lvert\mathbf k\rvert\to0}=\frac{1}{\sqrt3},$$
where $\Omega=2\omega(\lvert\mathbf k\rvert/2)$ is the angle the pair traverses per CA tick.

## What it extends

Special relativity's postulate that $c$ is a constant propagation speed, and Maxwell's curl law — which becomes the $O(\Omega)$ linearisation of the rotation rather than a fundamental equation. Energy conservation becomes geometric: a rotation preserves length.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F25-real-rotation-exact-discrete-time-maxwell.md` | The real-rotation formula holds to machine precision; the Maxwell curl law holds only to $O(k)$ | machine |
| `findings/F26-speed-of-light-as-rotation-rate.md` | The identification of $c_\text{lat}$ with $d\Omega/d\lvert\mathbf k\rvert$ | exact |

This is **founding decision 2** in `CLAUDE.md`; every downstream sector inherits it.

**Caution, recorded 2026-08-04.** F25's own title states the curl law closes only to $O(k)$. The F21/F23/F25 reviews (`docs/reviews/`) found that reported $O(k)$ failure to be a representation artifact of the σ-bilinear construction, and F306 carries the corrected result — the curl equation closes at $O(k^3)$ with coefficient $c_\text{lat}^3/48$. **This card is stated at the level of the rotation-rate identification, which none of those reviews touched.**

## Falsifier

None observational. The claim is a reinterpretation: it makes the same predictions as the identification $c=1/\sqrt3$ in lattice units, and is distinguishable only through the structures it forces downstream (CL012 birefringence, CL013 graviton speed), each of which carries its own falsifier. Recorded as `falsifier: none` with that named reason rather than left `unset`.

## Status & history

`live` since F26 (2026-05-21) and unchanged by any subsequent supersession. Not named in any record in `docs/theory/supersessions.yaml`.

## Sources

- `findings/F25-real-rotation-exact-discrete-time-maxwell.md`
- `findings/F26-speed-of-light-as-rotation-rate.md`
- `papers/Claims-and-Falsifiers-Summary.md` — core claim 1
- `CLAUDE.md` — Core Design Decision 2
- `docs/reviews/` — F21, F23, F25 reviews of 2026-08-04
