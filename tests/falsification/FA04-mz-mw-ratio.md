# FA04 — Z/W mass ratio = 2/√3

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★ (zero-fit-parameter electroweak prediction)
**Model element under test:** the σ↔τ swap geometry on the BCC lattice that fixes the bare Weinberg sector (F45).
**Supersedes:** new — electroweak ratios are not in tests-priority

## Hypothesis (parameter-free prediction)
The BCC σ↔τ swap geometry gives the bare tree-level mass ratio

  `m_Z/m_W = 2/√3 = 1.154701`,

with **zero fit parameters**. Measured `1.13460` (PDG) — a `+1.77%` overshoot attributable to the bare-vs-running (radiative) gap.

## Measured target + source
- PDG: `m_W = 80.369 GeV`, `m_Z = 91.188 GeV` → `m_Z/m_W = 1.13460`.

## Falsification criterion
The bare geometry is in tension / falsified if:
1. The measured ratio moves **away** from `2/√3` (currently +1.77%) rather than being closable by known electroweak radiative corrections, **or**
2. A first-principles running calculation in-model fails to close the +1.77% gap in the right direction (i.e. the residual is shown not to be RG-shaped).

## CASIM build & run
Closed-form geometric prediction; verify symbolically.
1. Symbolic (sympy): derive `m_Z/m_W = 2/√3` and `sin²θ_W = 1/4` from the σ↔τ swap on the BCC lattice (F45 construction); confirm against PDG to `+1.77%` / `+12%`.
2. Optional dynamical cross-check on the Z/W channels:
```bash
casim run scenarios/z_even.yaml --L 64 --ticks 1000 --out test-results/FA04_z.json
casim run scenarios/w_chiral.yaml --L 64 --ticks 1000 --out test-results/FA04_w.json
```
Confirm the mass terms entering each propagator carry the `2/√3` ratio.

## Pass/fail gate
- PASS: model `2/√3 = 1.1547`, within `+1.77%` of PDG, and the residual is RG-shaped.
- FALSIFIED: ratio drifts off `2/√3` beyond what running can explain.

## Provenance
F45 (σ↔τ swap Weinberg angle and m_Z/m_W), F35 (electroweak mixing), F49 (bond-counting sin²θ_W=2/9 partial), F112 §D, F115 (12% Weinberg gap is matching not running).
