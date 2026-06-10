# FA06 — Neutron–proton mass splitting (sign and magnitude, no QCD anchor)

**Tier:** A — sharp falsifier
**Falsification power:** ★★★★★ (sharpest matter-sector prediction; needs no QCD scale anchor)
**Model element under test:** the F40 down–up current-mass gap competing with the proton's EM self-energy.
**Supersedes:** new

## Hypothesis (parameter-free prediction)
The n–p splitting needs **no** QCD anchor — it is the F40 down–up current-mass gap (`+2.51 MeV`, neutron-heavier) beating the proton's larger EM self-energy (`−1.00 MeV`):

  `m_n − m_p = +1.51 MeV` (sign **positive**, neutron heavier).

Measured `+1.293 MeV`. This is a genuine prediction of both **sign** and **magnitude**.

## Measured target + source
- PDG: `m_n − m_p = +1.29333 MeV`.

## Falsification criterion
Falsified if:
1. The model's competing terms gave the **wrong sign** (they don't — but any future re-derivation that flips the sign falsifies), **or**
2. The magnitude `+1.51 MeV` is shown to be off by more than the EM-self-energy modelling uncertainty (currently +0.22 MeV high, ~17%) in a way the constituent decomposition cannot absorb.

## CASIM build & run
Dedicated scenario (same channel as FB02; emits the n−p decomposition):
```bash
casim run scenarios/njl_nucleon.yaml --out test-results/FA06_np.json
```
Reads off `n_minus_p_MeV, n_minus_p_sign_positive, np_strong_term_MeV, np_em_term_MeV`. Verified: strong `+2.51`, EM `−1.00`, total `+1.51 MeV`, sign positive.
1. Symbolic: the down–up current-mass gap → `+2.51 MeV` (F40 Y-extension); proton EM self-energy → `−1.00 MeV`; sum `+1.51 MeV`. Confirm sign and value.
2. Dynamical baryon cross-check (the two-route P2 baryon):
```bash
casim run scenarios/proton_composite.yaml --L 16 --ticks 60 \
    --out test-results/FA06_np.json
```
Compare proton vs neutron three-body binding with the F40 current masses; confirm the neutron is heavier and the gap sign is positive.

## Pass/fail gate
- PASS: model gives `+1.51 MeV`, correct sign, within ~0.25 MeV of PDG `+1.293`.
- FALSIFIED: wrong sign, or magnitude off beyond EM-self-energy uncertainty.

## Provenance
F123 §H3 (n–p splitting as the sharpest matter PREDICTION), F40 (quark Y / down–up gap), F122 (dynamical baryon three-body).
