# FA03 — Newton's constant predicted from the cell

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★★ (a wrong G, fifth force, or PPN deviation breaks the dielectric-gravity sector)
**Model element under test:** `G = a²c³/(8π√3·ħ)` (F79 structural Newton constant) with the canonical cell, and the F64 dielectric being PPN-identical to GR.
**Supersedes:** new — the absolute-G claim is not in tests-priority

## Hypothesis (parameter-free prediction)
With the canonical cell `a` fixed by F79/F107 (no gravitational input), the lattice stiffness gives

  `G = a²c³/(8π√3·ħ) = 6.674300×10⁻¹¹ m³kg⁻¹s⁻²`,

matching CODATA to `3.0×10⁻⁸`. The `8π√3` is the F79 Sakharov-induced stiffness (`2πη g*√d`, fermionic `g*=48` exact). The dielectric is GR-identical at post-Newtonian order: PPN `β=γ=1` exactly (F64 D-EM9).

## Measured target + source
- CODATA G = 6.67430(15)×10⁻¹¹ (relative uncertainty ~2.2×10⁻⁵).
- PPN: `|γ−1| < 2.3×10⁻⁵` (Cassini), `|β−1| < ~10⁻⁴` (LLR).
- Fifth-force / Yukawa-deviation bounds across sub-mm to planetary scales.

## Falsification criterion
The dielectric sector dies if:
1. A confirmed laboratory G shift moves the accepted value **outside** the model's `3.0×10⁻⁸` residual band in a way the canonical `a/ℓ_P` cannot absorb, **or**
2. Any confirmed PPN deviation `β≠1` or `γ≠1` beyond measurement error (the model is exactly `β=γ=1`), **or**
3. A confirmed fifth force / composition-dependent or Yukawa deviation from `1/r²` Newtonian + GR.

## CASIM build & run
Closed form + GR-consistency.
1. Symbolic (sympy, no chiral transforms): evaluate `G = a²c³/(8π√3·ħ)` at `a = √(8π)·3^(1/4)·ℓ_P`; confirm `6.674300×10⁻¹¹` and the `3.0×10⁻⁸` residual vs CODATA. Re-derive `8π√3` from `2πη g*√d` with `η=1/12`, `g*=48`, `d=3` as an independent check.
2. PPN consistency on the dielectric:
```bash
casim run scenarios/gravity_deflection.yaml --L 128 \
    --out test-results/FA03_ppn.json
```
Confirm the eikonal deflection coefficient is exactly `−4` at all field strengths (FA09) and the weak-field metric returns `β=γ=1`.

## Pass/fail gate
- PASS: `G` matches CODATA to `3.0×10⁻⁸` AND `β=γ=1` to current PPN precision.
- FALSIFIED: any of the three criteria above.

## Provenance
F79 (structural Newton constant closed form), F64 (EM-connection gravity, D-EM9 PPN), F107 (canonical a), F112 §B (registry headline).
