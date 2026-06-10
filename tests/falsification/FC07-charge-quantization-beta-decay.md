# FC07 — Charge quantization, anomaly cancellation, and β-decay (QG-4, FG sector)

**Tier:** C — consistency regression
**Falsification power:** ★★★★ (anomaly cancellation is a sharp structural requirement; charge quantization is exact)
**Model element under test:** the F38 first-generation anomaly cancellation, exact electric-charge assignments, and the F54 β-decay charged current.
**Supersedes:** `tests-priority/test_10_QG4_charge.py`, and folds in `test_07_QFT5_neutrino.py`

## Hypothesis
- **Charge quantization:** electric charges are exact rationals (`Q_e=−1`, `Q_u=+2/3`, `Q_d=−1/3`, `Q_ν=0`) from the hypercharge/Gell-Mann–Nishijima structure (F41/F35); proton and electron charges are exactly opposite.
- **Anomaly cancellation (FG-1):** all six gauge-anomaly traces are exactly zero per generation (F38) — required for consistency.
- **β-decay (FG-8):** `d→u+W⁻→u+e⁻+ν̄` proceeds with the correct chiral (left-handed) structure (F54).
- **Neutrino (QFT-5):** Higgs-free Majorana ν_R see-saw gives a naturally small ν mass (F47).

## Measured target + source
- Charge neutrality of atoms: `|Q_p+Q_e|/e < 10⁻²¹`. Beta-decay kinematics/chirality. Neutrino masses `Σm_ν < ~0.12 eV` (cosmology) and oscillation Δm².

## Falsification criterion
Falsified if:
1. Any anomaly trace is nonzero (gauge inconsistency — structural), **or**
2. Charges are not exact rationals / proton-electron charges not exactly opposite, **or**
3. β-decay shows the wrong chirality (the W couples left-handed; a right-branch weight must be ≡0), **or**
4. The see-saw cannot accommodate the measured ν mass scale.

## CASIM build & run
1. Anomaly: compute all six FG-1 traces from the F38 quantum numbers; confirm exactly zero.
2. Charges: confirm `Q` assignments are exact rationals and Σ over a generation is anomaly-free; proton charge `= −`electron.
3. β-decay (Tier-2 chiral channel):
```bash
casim run scenarios/beta_decay.yaml --L 16 --ticks 24 \
    --out test-results/FC07_beta.json
```
Confirm `d→u+W⁻→u+e⁻+ν̄` with left-handed coupling (right-branch weight ≡ 0).
4. Neutrino: confirm the F47 see-saw scaling gives a small ν mass.

## Pass/fail gate
- PASS: anomalies zero, charges exact rationals, β-decay left-chiral, see-saw natural.
- FALSIFIED: any of the four criteria above.

## Provenance
F38 (anomaly cancellation), F41/F35 (hypercharge / Gell-Mann-Nishijima), F54 (β-decay), F47 (Majorana see-saw), F53 (C/CP). Folds in QG-4 + QFT-5.
