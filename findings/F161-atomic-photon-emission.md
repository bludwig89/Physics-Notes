# F161 — Dynamical-processes layer P1: photon emission from atoms

**Date:** 2026-06-17 - 20:40
**Status:** Confirmed — 4/4 checks PASS (`test_F161_atomic_emission.py`).
**Roadmap:** opens the dynamical-processes layer (emission → scattering → transport); P1 = atomic emission.
**Modules:** `ca-simulation/ca_emission.py` (new); uses `ca_atom` (F125 radial Coulomb solver + m_e, α, Rydberg).
**Cross-references:** [[F125-p5-hydrogen-atom-em-bound-state]] (the bound states / fine structure), [[F156-realspace-em-bound-electron]] (the real-time orbital), [[F120-electron-calibrated-spectrum]] (the m_e anchor).

## Result

The static atomic levels are turned into a **rate** and a **spectrum** — an
excited electron drops to a lower level and radiates a photon. From the model's
own constants (m_e, α — no new inputs) `ca_emission` predicts:

1. **Spectral lines** — ħω = E_i − E_f. The Lyman-α line comes out **121.50 nm**
   (data 121.567) and the Balmer visible series **656.1 / 486.0 / 433.9 /
   410.1 nm** (data 656.3 / 486.1 / 434.0 / 410.2) — the hydrogen spectrum.
2. **Spontaneous-emission rates** (Einstein A) from the dipole matrix element
   with the Δl = ±1 selection rule:
   - 2p→1s (Lyman-α): **A = 6.27×10⁸ s⁻¹, τ = 1.59 ns** (data 6.27×10⁸, 1.6 ns);
   - 3p→1s: 1.67×10⁸ s⁻¹; 3p→2s: 2.25×10⁷ s⁻¹ (both match the known rates);
   - 2s→1s (Δl=0) and 3d→1s (Δl=2): **A = 0** — dipole-forbidden (the 2s
     metastability that, in reality, forces the two-photon decay).

So the model reproduces atomic light — line positions, line intensities, and
selection rules — as a derived consequence of its bound states, not an
assumption. This is the first member of the dynamical-processes layer
("predict … photon emission from atoms, electrical flow, etc.").

## Method

Levels from the F125 radial Coulomb solver (E_n = −Ry/n²); the dipole is the
reduced-radial integral d = ∫u_f·x·u_i dx (u = xR) on a common grid;
A = (4/3)α³ω³·[l_max/(2l_i+1)]·d² in atomic units → s⁻¹. Numpy-only (scipy
optional via the ca_atom fallback).

## Exactness tier

Tier-3 quantitative: line wavelengths to <1 %, A-coefficients to a few %
(grid-limited radial integral). The frequencies are exact given the level
formula; the rates inherit the F125 radial-wavefunction accuracy.

## Next in the layer

P2 — scattering / cross sections (an in/out wavepacket S-matrix harness:
Compton, Rutherford, resonance widths). P3 — electrical transport (multi-
electron drift/conductivity under a field; builds on F157 multi-electron).
Stimulated emission / absorption and line intensities under a driving field are
the natural extension of P1.
