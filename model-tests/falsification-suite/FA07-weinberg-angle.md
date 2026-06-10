# FA07 — Weak mixing angle sin²θ_W = 1/4 (bare)

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★ (parameter-free bare value; +12% gap must be RG-shaped)
**Model element under test:** the bare Weinberg angle from BCC geometry (F45) and bond/sublattice counting (F49).
**Supersedes:** new

## Hypothesis (parameter-free prediction)
The σ↔τ swap geometry gives the bare (pre-RG) weak mixing angle

  `sin²θ_W = 1/4 = 0.2500`,

with a partial bond/sublattice-counting derivation giving `2/9 = 0.2222` (F49). Measured (PDG, on-shell) `0.2230`. The `+12%` of the `1/4` value is the bare→running gap, argued to be ~TeV matching not low-energy running (F115).

## Measured target + source
- PDG: `sin²θ_W(on-shell) = 0.22305`; `sin²θ̄(M_Z) = 0.23122` (running scheme-dependent).

## Falsification criterion
Falsified if:
1. The bare value cannot be reconciled with the measured running value by a legitimate matching/RG argument (the +12% must be shown to be RG/matching-shaped), **or**
2. The two model derivations (`1/4` swap-geometry vs `2/9` bond-counting) cannot be reconciled into one self-consistent bare value.

## CASIM build & run
Symbolic geometric derivation.
1. Symbolic (sympy): derive `sin²θ_W = 1/4` from the σ↔τ swap (F45) and `2/9` from BCC bond/sublattice counting (F49); document the relation between them.
2. Confirm the `+12%` gap vs PDG and tag it as bare-vs-running (cross-ref F115's "matching not running" finding).

## Pass/fail gate
- PASS: model bare `1/4` (and `2/9` partial), +12% vs PDG, residual RG/matching-shaped.
- FALSIFIED: residual is not RG-shaped, or the two derivations conflict irreconcilably.

## Provenance
F45 (σ↔τ swap), F49 (bond-counting 2/9), F35 (electroweak mixing), F115 (gap = matching not running), F112 §D.
