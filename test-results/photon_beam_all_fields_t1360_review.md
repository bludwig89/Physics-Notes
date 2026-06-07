# Review: photon_beam_all_fields_t1360.npz (long run, L=48, 1360 ticks)

`2026-06-06 - 18:05`

Checkpoint: `src/casim/checkpoints/photon_beam_all_fields_t1360.npz` — L=48 cubic, seed 11, m_index 4 (k0 = 2π/12 = 0.5236, k0σ⊥ = π), ~16.1 box transits. Extends the documented L=32/60-tick smoke run (`smoke_photon_beam_all_fields.json`) by 22× in ticks.

## What holds (confirmations, now at much longer baseline)

1. **Norm conservation, all four channels coexisting, 1360 ticks:** photon 7.9e−15, W 3.5e−15, Z 5.0e−15, gravity 0.0 (static background). Machine precision; no secular drift.
2. **Per-mode unitarity / Tier-1 independence:** the photon's k-space mode populations |F_k|² at t=1360 match the analytic init packet mode-by-mode to **max rel. deviation 1.5e−9** (median 1.6e−11) over 4431 modes. No energy exchange between photon modes despite 1360 ticks through live W/Z/gravity fields — channel superposition confirmed dynamically, without needing the γ-only twin run. (Caveat: population match doesn't bound a uniform per-mode phase shift; the measured early-window speed matching the spectral prediction covers that to ~1%.)
3. **F105 (axial dispersionlessness) holds dynamically:** kx spectrum is exactly preserved (mean kx = k0 to 1e−15, σ_kx = 1/(4√2) to 1e−7) and Ω_pair(k,0,0) = k/√3 verified to 1e−12 out to k=3 — so there is zero axial chirp over 16 transits. All observed spreading is transverse-coupled.
4. Backward (−kx) power stays at 3.3e−4 of total — set by the one-sided init at k0σx ≈ 2.1, conserved, not growing.

## What's new from the longer run

1. **The beam fully delocalizes by t ≈ 900.** Circular rms spread: 2.83 (t=1) → 4.08 (t=60) → 8.55 (t=300) → 12.62 (t=900), then plateaus ~12.1–12.6 against the box-uniform limit L/√12 = 13.86. Transverse diffraction (Ω_⊥'' ≈ 1.09) fills the box; via the k⊥-dependence of v_x this also delocalizes the axial profile (axial min/max energy ratio 0.21 at t=1360).
2. **beam_track is only meaningful pre-saturation.** Windowed centroid fits: 0.5448 (t≤60), 0.561 (60–300), 0.569 (300–700), **0.592 (700–1000, nominally > c)**, 0.567 (1000–1360). The conserved spectral transport velocity computed from the t=1360 state is **⟨v_x⟩ = 0.5402** (exactly conserved under the linear evolution). All late-time drift, including the apparent superluminal window, is an artifact of the circular-centroid estimator on a near-uniform wrapped distribution — not physics. Practical rule: trust beam_track only while spread ≲ L/(2√12).
3. **Leading-order diffraction-deficit formula degrades at k0σ⊥ = π.** Measured deficit (spectral): (c − ⟨v_x⟩)/c = **6.44%** vs the yaml estimate 1/(2(k0σ⊥)²) = 5.07% — a 27% relative underestimate. At the smoke run's k0σ⊥ = 4.7 the same formula was good to ~10% (2.3% vs 2.5%). Keep k0σ⊥ ≳ 4–5 (or use the full Gaussian-weighted ⟨dΩ/dk_x⟩) when quoting expected beam speeds.

## Verdict

No new physics finding — F105 and Tier-1 superposition survive a 22× longer run at machine/spectral precision, which is the strongest multi-channel unitarity statement so far. The new information is methodological: the beam_track validity window, and the breakdown point of the paraxial deficit formula. Future long beam runs wanting a clean speed measurement need L ≥ 96 with σ⊥ ≥ 12 (as the yaml already suggests) or should report the spectral ⟨v_x⟩ instead of the centroid fit.
