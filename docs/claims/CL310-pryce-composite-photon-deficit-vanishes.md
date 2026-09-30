---
id: CL310
title: 'Pauli blocking between two F69/F169 composite photons vanishes as the BZ grid is refined toward the continuum threshold equation'
slug: 'pryce-composite-photon-deficit-vanishes'
tier: supporting
kind: derivation
status: live
domain: [QM, QFT]
exactness: quantitative
findings: [F398, F69, F169]
tests: [F398-pryce-composite-commutator]
modules: [casim.engine.gauge.photon_pryce_commutator]
constants: []
supersessions: [S24-F169-C3-threshold-search-replaced-by-closed-form]
reviews: []
rolls_up_to: CL002
falsifier: stated
first_issued: '2026-09-23'
last_verified: '2026-09-23'
provenance: authored
review_state: authored
confidence: medium
---

# CL310 — Pauli blocking between two F69/F169 composite photons vanishes as the BZ grid is refined toward the continuum threshold equation

## Statement

For the composite creation operator $a_{\mathbf k}^\dagger=\sum_p\psi_{\mathbf k}(p)\,b^\dagger_{+,\mathbf k/2+p}b^\dagger_{-,\mathbf k/2-p}$ built from the F69 paired-photon's constituents and the F169 marginally-bound relative-momentum wavefunction, the two-composite-photon norm deficit from the ideal-boson value has the exact closed form $\big\|(a^\dagger_{\mathbf k})^2|0\rangle\big\|^2=2\left(1-\sum_p\psi_{\mathbf k}(p)^4\right)$, and the deficit term $\sum_p\psi(p)^4$ falls as $\sim L^{-2}$ as the Brillouin-zone relative-momentum grid $L$ is refined toward the continuum threshold equation (measured ratio $107.5$ between $L{=}10$ and $L{=}100$ against a derived $(100/10)^2=100$ prediction). Pryce's (1938) exact-Bose-commutation obstruction for a two-fermion composite is present and nonzero at every finite resolution, but it is a computable, vanishing correction for this specific marginally-bound construction, not a structural failure of approximate boson statistics.

## What it extends

Pryce (1938): a composite built from two fermionic constituents cannot satisfy exact canonical Bose commutation — the general result behind why Cooper pairs, deuterons, pions and (in the de Broglie/Jordan/Perkins "neutrino theory of light" line) a hypothetical fermion-pair photon are only ever *approximately* bosonic. **Correction (2026-09-23, from this card's own attack-and-fix review, `docs/reviews/F398-review-2026-09-23.md`, attack 11):** the exact inverse-participation-ratio deviation formula itself ($1-\sum_p\psi(p)^4$ for two composites) is *not* new — it is standard machinery in the composite-boson/"coboson" literature (Combescot et al.; the bosonic-character normalization $\chi_M=\langle0|C^MC^{\dagger M}|0\rangle/M!$), which this card did not originally cite. What this card actually contributes is narrower and still genuine: applying that known formula to *this model's own* specific, already-derived (F169) marginally-bound photon wavefunction, and deriving+measuring how the resulting deviation scales as the model's own momentum-grid resolution is refined ($\sim L^{-2}$ for this gapless/threshold wavefunction shape) — a direction (grid-resolution scaling of a threshold wavefunction, as opposed to the standard dilute-density-limit scaling) the review found no prior-art match for.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F398-pryce-composite-photon-commutator.md` | Closed-form identity verified against an independent brute-force Fock-space construction (residual $8.9\times10^{-16}$, two grid sizes); $L^{-2}$ scaling measured against two independently-verified-clean grid points; two sound, isolated negative controls (`pairing="shared"` breaks only the identity leg; `wavefunction="uniform"` breaks only the scaling leg, landing on the different, correctly-predicted $L^{-3}$ law) | quantitative (identity itself machine-exact; the scaling law is a measured trend with disclosed grid-commensurability noise) |
| `findings/F69-paired-spinor-photon.md` | The pairing $a^\dagger_{\mathbf k}$ is built from (one constituent per BCC chiral branch, momentum $\mathbf k/2$ each at $p=0$) | exact |
| `findings/F169-photon-interacting-two-body-wavefunction.md` | The relative-momentum wavefunction $\psi_{\mathbf k}(p)$ this card's operator uses, including its own documented finite-$k$ grid-threshold caveat (not inherited here — this card is a $\mathbf k=0$ calculation, where F169 states its wavefunction is exact, not a grid artifact) | machine (at $\mathbf k=0$) |

## Falsifier

Two, at different depths:

1. **The scaling law, directly.** A future session computing $\sum_p\psi(p)^4$ over a wider, denser $L$ range (or with a method that controls the grid-commensurability noise this card's own finding discloses) and finding the deficit does **not** trend toward zero — e.g. saturates at an $O(1)$ value, or the raw `bulk_norm_is_L3` diagnostic fails to hold near-constant — would falsify the $L^{-2}$/vanishing-deficit reading. Threshold: the same $[30,400]$ ratio band this card's own gate check uses.
2. **The scope of the claim, structurally.** This card's operator is built from a single, frozen wavefunction shape ($N$ identical copies of $a^\dagger_{\mathbf k}$), which is the same, well-defined observable Pryce's own calculation addresses — it is *not* a claim about the genuine many-composite variational ground state (which could reorganize as occupation grows). A future session building that ground state and finding a *different*, non-vanishing residual would not falsify this card (a different, harder question), but would show this card's result does not extend to real multi-photon states (a laser, a coherent state) without further work — named explicitly as out of scope in `findings/F398-pryce-composite-photon-commutator.md`'s own "what this does not address" section.

## Status & history

First issued 2026-09-23, from `findings/F398-pryce-composite-photon-commutator.md`. No prior status to narrate — this is the card's first version. `confidence: medium` rather than `high`, deliberately: the identity (Result 1) is machine-exact and independently cross-checked, but the scaling law (Result 2) carries real, disclosed grid-commensurability noise and was checked at two pre-verified-clean endpoints rather than a dense, noise-controlled sweep.

## Sources

- `findings/F398-pryce-composite-photon-commutator.md`
- `findings/F69-paired-spinor-photon.md`
- `findings/F169-photon-interacting-two-body-wavefunction.md`
- Pryce, M. H. L. (1938) — the composite-boson exact-commutation result this card computes an instance of (external, not re-derived from primary source in this session; carried from the notebook-reconstruction correlation queue's own citation of the historical result, not independently verified against Pryce's original paper)
- `docs/theory/notebook-reconstruction-correlation-queue.md` (NB-007 row, the question this card answers)
