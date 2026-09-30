---
id: CL313
title: 'The photon channel''s finite-k Koster-Slater threshold coupling is repaired and genuinely decreases with momentum; the coordinate-axis floor is an exact double degeneracy'
slug: 'photon-finite-k-critical-coupling-repaired-and-decreasing'
tier: supporting
kind: derivation
status: live
domain: [SM, QFT]
exactness: quantitative
findings: [F401, F169, F397]
tests: [F401-photon-bound-state-finite-k]
modules: [casim.engine.gauge.photon_bound_state_finite_k, casim.engine.gauge.photon_bound_state]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL149
falsifier: stated
first_issued: '2026-09-23'
last_verified: '2026-09-23'
provenance: authored
review_state: authored
confidence: high
---

# CL313 — The photon channel's finite-k Koster-Slater threshold coupling is repaired and genuinely decreases with momentum; the coordinate-axis floor is an exact double degeneracy

## Statement

F169's `critical_coupling`/`threshold_wavefunction` (the photon's Koster–Slater two-body bound-state solver) took the continuum floor $T(k)$ as the minimum of the free two-body dispersion over a finite $L^3$ relative-momentum grid — exact at $k=0$ but a non-monotonic grid artifact at finite $k$, documented and left unrepaired by F169 itself. Substituting the already-exact closed form $T(k)=\min(\omega^+(k),\omega^-(k))$ (F397) **sharply reduces, but does not eliminate,** the underlying grid-commensurability artifact: over a dense 48-point $L$-scan at fixed $|k|=0.2$ along $(111)$, the closed form's worst-case single-step convergence backslide is roughly $4\times$ smaller than the grid form's, though occasional dips persist for both (found on independent review, 2026-09-23, narrowing an earlier draft's overclaim of convergence "at every step"). The re-derived critical coupling $g_c(k)$ — the strength at which a bound state sits exactly at the two-body floor — decreases monotonically with $|k|$ from the F169 $k=0$ value $2.2596$ along $(111)$ (confirmed to $|k|=1.0$: $2.2545,\,2.2183,\,2.1324,\,1.9738,\,1.8413,\,1.7353,\,1.6549$ at $|k|=0.05,\dots,1.0$) and along $(3,1,1)$, but **not** along $(2,1,0)$, which is a genuine counterexample (also found on review) — the decreasing trend is a real, checked property of specific directions, not a universal law of all finite-$k$ momenta. Separately, and exactly (proved symbolically, unaffected by the review): along any coordinate axis, both chiral dispersion branches collapse onto the identical isotropic cone $\omega^\pm(q,0,0)=|q|/\sqrt3$, so the symmetric-split energy $\Omega_\text{even}(k)$ and the collinear-endpoint floor $T(k)$ coincide **exactly, to all orders**, not merely to $O(k^3)$ as the general off-axis formula gives.

## What it extends

The Koster–Slater/Watson theory of a rank-one contact interaction binding two particles at a finite-dimensional continuum edge (the same finite-binding-threshold structure F74 already establishes for the model's scalar channel), applied here specifically to the photon's own finite-total-momentum sector. It sharpens F169/CL149's own leading-order offset statement ($\Omega_\text{even}(k)-T(k)=|k_xk_yk_z|/(3|k|)+O(k^3)$, "vanishing on the coordinate planes") to an exact statement along the narrower coordinate-**axis** case specifically, while confirming (via an explicit counterexample) that the general in-plane case genuinely retains a nonzero $O(k^3)$ residual, as F169's own wording already implied but did not check.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F401-photon-bound-state-finite-k-threshold-repair.md` | The full repair and characterization: axis identity (exact, sympy, cross-checked against the engine's own dispersion), in-plane contrast (genuine nonzero residual), L-convergence comparison at F169's own quoted $L$ values, the $g_c(k)$ sweep, and a declared control confirming $k=0$ is unaffected | exact (axis identity) / quantitative (convergence and sweep) |
| `findings/F169-photon-interacting-two-body-wavefunction.md` (C2/C4-note) | The artifact this repairs, and the k=0 value ($g_c=2.2596$) this repair leaves unchanged | quantitative |
| `findings/F397-notebook-factorization-route-pp176-182.md` (R6) | The closed-form $T(k)$ and offset $|\varepsilon(k)|$ this finding substitutes and builds on | exact |

## Falsifier

1. **Exhibit a coordinate-axis $q$ where the two chiral branches' dispersion differs.** This is a symbolic identity re-derived independently in F401's own test and should not be findable; stated for completeness.
2. **Exhibit a $k\in[0,1.0]$ along $(111)$ or $(3,1,1)$ where $g_c(k)$ exceeds its value at a smaller $|k|$ on the same ray.** Would narrow this card's specific numerical claim to the sub-range actually checked.
3. **Derive the physically gauge-consistent binding coupling at finite $k$ and show it does not track $g_c(k)$ as computed here, along whichever directions $g_c(k)$ is actually monotonic.** Would not falsify this card (which explicitly declines to identify the two) but would close the separate, harder question F169 already left open (the all-$k$ gauge-pole proof).
4. **Exhibit a principled classification of which directions show the decreasing trend and which (like $(2,1,0)$) do not.** Not established here; the three directions checked are a sample, not a classification, and this card does not claim otherwise.

## Status & history

First issued 2026-09-23, from `findings/F401-photon-bound-state-finite-k-threshold-repair.md`, a direct response to `docs/theory/notebook-followup-2026-09-22.md` Part VI.3 and `docs/theory/notebook-v2/index.md` §5 Prompt E. Rolls up to `CL149` (F169's own two-body-wavefunction card, currently `unreviewed-seed`) as the specific finite-$k$ threshold-repair half of that broader claim; this card is `authored` and independent of CL149's own review state. No prior status to narrate.

## Sources

- `findings/F401-photon-bound-state-finite-k-threshold-repair.md`
- `findings/F169-photon-interacting-two-body-wavefunction.md`
- `findings/F397-notebook-factorization-route-pp176-182.md`
- `findings/F168-paired-photon-binding-gauge-protected.md`, `findings/F250-allk-gauge-pole-paired-photon.md` (the reason this card's scope stops short of the physical photon's own finite-$k$ coupling)
- `docs/theory/notebook-followup-2026-09-22.md` Part VI.3; `docs/theory/notebook-v2/index.md` §5 Prompt E — the question this card answers
