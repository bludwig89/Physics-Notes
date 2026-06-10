# FB07 — Deuteron: the first nucleus binds via the pion tensor force

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (structural: binds ONLY through the tensor force; a priori the model has no nuclear force)
**Model element under test:** the F104/F126 ³S₁–³D₁ deuteron bound by one-pion-exchange tensor + σ attraction − ω repulsion + quark-Pauli core.
**Supersedes:** new

## Hypothesis (mostly predicted, one tuned core)
The deuteron binds as a single shallow `J^P=1⁺`, I=0 state **only** through the pion tensor force (central-only OPEP is unbound at the same core — structural):

  `E_b = 2.224 MeV`, `κ = √(M_N E_b)/ħc = 0.2316 fm⁻¹`, `r_d ≈ 1.94 fm`, D-state `P_D≈6.6–7%`.

The F126 σ attraction (g²/4π=8.18, m_σ=2m_c) binds at physical b=0.55 fm; F113 gives the +341.8 MeV quark-Pauli+chromomagnetic repulsive core. Inputs: m_π, f_π (model), g_A=1.272 (one external number via Goldberger-Treiman), M_N (external/P6).

## Measured target + source
- Measured: `E_b=2.22457 MeV`, `J^P=1⁺`, I=0, `r_d≈1.97 fm`, D-state `P_D≈4–6%`, `κ=0.2316 fm⁻¹`.

## Falsification criterion
Falsified if:
1. The full tensor treatment fails to bind while central-only also fails (the tensor-essential structure is the key claim), **or**
2. The bound state is not a single `J^P=1⁺` I=0 with a few-% D-state, **or**
3. The ³S₁ tail slope departs from `κ=√(M_N E_b)/ħc` beyond ~1% with the physical E_b.

## CASIM build & run
Coupled ³S₁–³D₁ channel solve with OPEP tensor + σ + core.
1. Numerical: build the tensor spin-angular matrix from Clebsch-Gordan; confirm it equals Rarita-Schwinger `[[0,2√2],[2√2,−2]]` to ~1e-14. Solve the coupled-channel bound state; confirm single `1⁺` state, tensor-essential (central-only unbound), D-state ~7%.
2. Confirm ³S₁ tail slope vs κ (0.34%), and that tuning one short-range core radius lands E_b=2.224 MeV at physical κ=0.2316 fm⁻¹.

## Pass/fail gate
- PASS: binds only with tensor; single 1⁺ I=0; E_b tunable to 2.224 MeV at physical κ; D-state few-%.
- FALSIFIED: any of the three criteria above.

## Provenance
F104 (P4 deuteron tensor nucleus), F126 (σ attraction), F113 (NN repulsive core), F103 (pion).
