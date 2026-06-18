# FB02 — Nucleon mass from a single f_π anchor

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (one hadronic anchor → the nucleon to ~1%)
**Model element under test:** the F97/F123 claim that the nucleon mass IS the dynamical (χSB) constituent mass, m_p≈3m_c.
**Supersedes:** new

## Hypothesis (one calibrated anchor, rest predicted)
With the single chiral anchor `f_π=92.07 MeV` (the only hadronic input), the NJL constituent mass and nucleon mass are

  `m_c = 309.5 MeV`  (vs m_N/3 = 312.97, `+1.11%`),
  `m_p ≈ 3m_c = 928.5 MeV`  (vs PDG 938.27, `−1.05%`).

The nucleon mass is dynamical (χSB constituent), NOT the ~0.11% current-quark sum (F97). The residual confinement/OGE/hyperfine binding is the remaining ~1%.

## Measured target + source
- PDG: `m_p=938.272 MeV`, `m_n=939.565 MeV`; constituent `m_N/3≈312.97 MeV`.

## Falsification criterion
Falsified if:
1. Anchoring on f_π and using the constituent mass gives a nucleon mass off by more than a few % (currently −1.05%) that the residual binding cannot close, **or**
2. The dynamical-mass picture is contradicted (e.g. the constituent mass is shown not to dominate over the current-quark sum) — that would break F97.

## CASIM build & run
Dedicated scenario (f_π-anchored constituent route; pure numpy, sandbox-fast):
```bash
casim run scenarios/njl_nucleon.yaml --out test-results/FB02_nucleon.json
```
Reads off `m_c, m_p_3mc_MeV, m_p_rel_err, n_minus_p_MeV`. Verified output: m_c=309.5, m_p=928.47 (−1.05%), n−p=+1.51 (sign +).
1. Numerical (NJL, F77/F116): solve the gap equation with Λ=BZ edge, induced G; with f_π=92.07 anchor get `m_c=309.5`; form `3m_c=928.5`; confirm `−1.05%` vs PDG.
2. Dynamical cross-check (P2 three-body baryon):
```bash
casim run scenarios/proton_composite.yaml --L 64 --ticks 1000 \
    --out test-results/FB02_nucleon.json
```
Confirm the two routes (constituent NJL vs real-time three-body) agree and the current-quark sum is ~0.11% of M.

## Pass/fail gate
- PASS: m_p≈3m_c=928.5 within ~1% of 938.27 from the single f_π anchor.
- FALSIFIED: nucleon mass off beyond residual binding, or constituent-dominance broken.

## Provenance
F123 §H1/H2 (P6 SI nucleon), F97 (mass is dynamical not current-quark sum), F77/F116 (NJL gap + cutoff/G), F122 (P2 three-body baryon), F124 (√σ/f_π).
