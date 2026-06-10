# FC06 — CPT invariance and Lorentz covariance (QFT-8, SR sector)

**Tier:** C — consistency regression
**Falsification power:** ★★★★ (CPT is a deep structural requirement; the SR sector also carries the FA01/FA02 LIV story)
**Model element under test:** the discrete C, P, CP/CPT structure (F53/F54) and SL(2,ℂ) Lorentz covariance (F24).
**Supersedes:** `tests-priority/test_13_QFT8_CPT.py`, `test_11_SR4_doppler.py`

## Hypothesis
- **CPT:** the lattice C, P, CP operations are well-defined per species; CP conserved (Jarlskog `N(1)=0`), θ pure gauge → CPT preserved (F53).
- **Lorentz:** the Weyl SL(2,ℂ) boost gives exact 4-current covariance (F24); relativistic Doppler `ν'=ν√[(1−β)/(1+β)]` (SR-4) holds in the continuum limit, with the quantifiable LV residue of FA01 at finite k.

## Measured target + source
- CPT: no confirmed violation (e.g. `|m_K⁰−m_K̄⁰|/m_K < 10⁻¹⁸`); neutral-kaon, antihydrogen tests.
- Relativistic Doppler: confirmed (Ives-Stilwell and modern ion-storage-ring tests to ~10⁻⁹).

## Falsification criterion
Falsified if:
1. The lattice C/P/CP bookkeeping produces a CPT-violating asymmetry (e.g. particle/antiparticle mass or lifetime split) beyond numerical floor, **or**
2. The boosted 4-current is not covariant (SL(2,ℂ) fails), **or**
3. Relativistic Doppler departs from the SR form beyond the FA01 LV residue.

## CASIM build & run
1. CPT: build per-species C, P, CP (F53); confirm CP conserved (Jarlskog N(1)=0), particle/antiparticle symmetric to numerical floor.
2. Boost: apply the Weyl SL(2,ℂ) boost; confirm 4-current covariance (F24) to machine precision.
3. Doppler: emit a periodic wavepacket stream to a drifting receiver; confirm `ν'=ν√[(1−β)/(1+β)]` in the small-k limit; quantify the finite-k LV residue (consistent with FA01).

## Pass/fail gate
- PASS: CPT preserved, SL(2,ℂ) covariant, Doppler matches SR to the FA01 residue.
- FALSIFIED: any of the three criteria above.

## Provenance
F53 (C/CP per-species, CPT), F54 (β-decay charged current), F24 (SL(2,ℂ) boost covariance), F22 (velocity addition), FA01 (LV residue).
