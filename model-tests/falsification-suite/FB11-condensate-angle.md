# FB11 — Condensate angle δ = 15° (chiral limit) vs measured 12.733°

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★ (the one open angle λ₆; its offset is carried by m_e/m_τ)
**Model element under test:** the E_g condensate angle δ that sets the lepton texture (F93/F101/F118/F119).
**Supersedes:** new

## Hypothesis
In the massless-electron limit the condensate angle is exactly

  `δ = 15°` (exact, m_e=0 limit),

with the first-principles dynamical value `λ₆=1/4 → δ=13.36°` (F119-W2). The measured angle (read from the lepton masses) is `12.733°`. The `2.27°` offset from 15° is carried by the finite `m_e/m_τ`.

## Measured target + source
- Lepton masses (PDG) → condensate angle `δ_meas = 12.733°`.

## Falsification criterion
Falsified if:
1. The exact `m_e=0` value is not `15°`, **or**
2. The first-principles `λ₆` cannot be reconciled with `δ_meas=12.733°` within the m_e/m_τ correction (i.e. the angle is over-determined and inconsistent), **or**
3. The same angle fails to simultaneously give the FB01 spectrum + FA05 Koide (internal consistency).

## CASIM build & run
Symbolic condensate geometry.
1. Symbolic: confirm `δ=15°` exactly in the m_e=0 limit; compute the m_e/m_τ correction → `12.733°`; confirm consistency with the FB01 spectrum and FA05 Koide from the same δ.
2. Document λ₆=1/4 → 13.36° as the open dynamical input (F118/F119).

## Pass/fail gate
- PASS: δ=15° exact (chiral limit); 2.27° offset accounted by m_e/m_τ; consistent with FB01/FA05.
- FALSIFIED: any of the three criteria above.

## Provenance
F93 (orthorhombic E_g vacuum), F101 (condensate angle fit), F118/F119 (λ₆ open input), F112 §D.
