# FB03 — Pion sector: m_π, f_π, ⟨q̄q⟩, GMOR, Goldstone

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★★ (the pion as the χSB Goldstone, with the GMOR slope)
**Model element under test:** the F77/F103 NJL gap+RPA pseudoscalar pole as a certified dynamical Goldstone boson.
**Supersedes:** new

## Hypothesis (one coupling G, multiple outputs)
From one coupling (Λ=651.5 MeV, GΛ²=2.10, m₀=5.5 MeV):

  `m_c=311.2 MeV` (~4.2%), `m_π=140.5 MeV` (~4.1%), `f_π=92.6 MeV` (0.2%), `⟨q̄q⟩` (a few %).

Structural predictions: exact Goldstone theorem in the chiral limit (`1−2G·Π_PS(0)=0` ≡ gap equation, residual 2.3×10⁻¹⁴); GMOR `m_π²∝m₀` to 0.39%; Goldstone scaling flat to 0.86%.

## Measured target + source
- PDG: `m_π=135–138 MeV`, `f_π=92.4 MeV`; lattice `⟨q̄q⟩^(1/3)≈−272 MeV`; constituent `m_c≈325 MeV`.

## Falsification criterion
Falsified if:
1. The pseudoscalar pole fails to go massless in the chiral limit (Goldstone theorem broken — structural), **or**
2. GMOR linearity `m_π²∝m₀` fails beyond the stated 0.39%, **or**
3. The single-coupling fit cannot reproduce m_π, f_π, ⟨q̄q⟩ simultaneously to the few-% level.

## CASIM build & run
Dedicated scenario (compute-once NJL gap + RPA ladder; pure numpy, sandbox-fast):
```bash
casim run scenarios/njl_pion.yaml --out test-results/FB03_pion.json
```
Reads off `m_c, m_pi, m_sigma, m_rho, f_pi, condensate, gmor_rel` + the chiral-limit `m_pi_chiral_limit_MeV` (Goldstone). Verified output: m_c=311.2, m_π=140.5, f_π=92.6, m_σ/2m_c=1.0, GMOR=0.39%, chiral m_π=1.6×10⁻⁴ MeV.
1. Numerical (what the channel does): solve gap eq for m_c; sum q̄q ladder for the pseudoscalar pole (m_π) and its f_π; compute ⟨q̄q⟩. Confirm the quoted residuals. (No chiral transforms; check numpy/scipy per CLAUDE.md.)
2. Goldstone: in m₀→0 limit confirm `1−2G·Π_PS(0)=0` ≡ gap equation (residual ~1e-14) and the pole at m_π=0.
3. GMOR: vary m₀, confirm `m_π²∝m₀` linear to 0.39%.
4. Real-space cross-check: relative-coordinate bound state vs dense diagonalisation (agreement ~1e-15).

## Pass/fail gate
- PASS: m_π, f_π, ⟨q̄q⟩, m_c within a few %; Goldstone exact; GMOR ≤0.4%.
- FALSIFIED: any of the three criteria above.

## Provenance
F103 (P3 dynamical pion Goldstone), F77 (NJL gap+RPA self-consistent), F116 (cutoff/G), F124 (√σ/f_π).
