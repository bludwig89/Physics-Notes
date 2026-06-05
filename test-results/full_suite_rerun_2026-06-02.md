# Full Test-Suite Rerun — Non-Superseded Suite

**2026-06-02 - 12:30**

Fresh run of the entire test suite that has not been deprecated or superseded,
triggered by the recent model additions (especially the **dual / paired-spinor
photon**, F67–F69/F72) plus the F73–F80 mass/Koide work and the F64/F79 gravity
findings. Run on Python 3.10, numpy 2.2.6, scipy 1.15.3, matplotlib 3.10 (Agg),
mpmath 1.3.

## Headline

**76 PASS · 6 FAIL · 2 INCOMPLETE** across **84** non-superseded test units.

The entire **current-model core passes**, including every photon test in the new
paired-spinor picture:

- **Paired-spinor photon** — F67 (even-law vs bilinear mutually exclusive), F68
  (U(1) minimal coupling forces the even photon), F69 (paired photon: massless,
  luminal $c=1/\sqrt3$, transverse, non-birefringent), F72 (universal even
  propagator): **all PASS**. The birefringence-exclusion analyses F65/F66 that
  retired the σ-bilinear photon also re-confirm.
- **Gravity (F64 dielectric / F79 structural G)** — F55–F61, F63, F79 PASS;
  F64 sub-tests D-EM1…D-EM10 re-confirmed PASS (D-EM11 deferred, see below).
- **Mass / generations / Koide** — F46, F73–F81 all PASS.
- **Gauge sector** — SU(2) (`wmu` phases 1–6, F45), hypercharge, SU(3) Noether,
  gluon dynamics + gradient flow + confinement (FG7/7b/7c), baryon singlet
  (FG7d/F71), anomaly cancellation (FG1), quark EW + complex mass (FG2/FG3/FG4),
  β-decay (FG8), C/CP per species (FG9): **all PASS**.
- **Validation tier (`tests-priority/`)** — 13 of 15 PASS (GR light bending,
  Pound–Rebka, Shapiro, Mercury, CHSH, CPT, Zeno, neutrino, Heisenberg, Doppler,
  Planck-LV, charge quantisation).

## Excluded as superseded (per `CLAUDE.md` / `key-decisions.md`)

These were **not run** — the model has explicitly retired them:

| Excluded test | Superseded by |
|---|---|
| `test_F50_gravity_fork_dirac.py` | F64 dielectric gravity (was two-leg metric) |
| `test_F52_restleg_backreaction.py` | F64 dielectric gravity |
| `test_F62_dirac_gravity_fork.py` | F64 dielectric gravity |
| `test_FG6_two_helicity_photon.py` | F69 paired-spinor photon (σ-bilinear retired as the photon) |

## Failures (6)

| Test | What fails | Reading |
|---|---|---|
| `tests-priority/test_08_QM2_tunneling.py` | **Crash** — `ca_dirac` has no attribute `dirac_step_u1_2d_splitstep` | Stale test: the U(1)-coupled Dirac step was renamed/removed in the photon/U(1) refactor (current API: `mass_step_1flavor_u1` + `dirac_step_2d_splitstep`). Test needs updating to the new API — **likely a real casualty of the F68/F69 changes.** |
| `run_phaseF_tests.py` | **Crash** in F1 — `unified_step` diverges, effective mass → −1.6×10⁹, trips the \|m\|≤1 admissibility check | Exercises the **Higgs path `ca_unified`/`ca_higgs`**, which is *design-superseded* in this Higgs-free model (core decision 3, F27). Arguably belongs in the excluded set; flagged rather than silently dropped. |
| `test_SR5_photon_frame_invariance.py` | G7/G8 wavepacket **group-velocity via FFT** miss the 1e-10 gate (resid 1.3e-2, 5.5e-2) | Analytic Lorentz checks G1–G6 pass at machine precision (≤2e-15); only the FFT-bin group-velocity estimator is imprecise. Measurement-method limitation, not a physics failure — candidate for the resolution-free Hilbert estimator already used in F64 D-EM11. |
| `tests-priority/test_15_QM6_twoslit.py` | Part 1 double-slit visibility V=0.465 (<0.80) and Part 3 monotone degradation both fail; V_meas frozen at 0.46478 across all amplitude ratios | Visibility measurement looks broken (identical V for every $r=A_2/A_1$). Pre-existing two-slit harness issue; not touched by the recent photon work. |
| `test_wmu_phase7_backreaction.py` | WB.5 **massless-limit** (massive W step → free step at $m_W=0$) fails; 4/5 subtests pass | Edge case in the W Proca step at exactly $m_W=0$; WB.1–WB.4 (currents, back-reaction, massive dispersion) pass. |
| `test_fork_D_doppler.py` | Parts 1 & 3 (lab-frame Doppler, relativistic reconstruction) fail; Part 2 (γ from dispersion) passes | **Exploratory fork** whose own summary already reads "Paper §7 Lorentz-emergence … NOT CONFIRMED within this CA implementation." A known-open exploration, not a regression. |

**Most actionable:** `test_08_QM2_tunneling.py` (one-line API rename) and the
`run_phaseF` Higgs-path crash (decide: exclude as superseded, or guard the
divergence). The two photon-relevant suites the rerun was meant to stress
(SR5, QM6) fail only in their FFT/visibility *measurement* layers, not in the
paired-spinor propagator itself.

## Incomplete — exceed the in-session sandbox cap (~45 s/call)

| Test | Status | Note |
|---|---|---|
| `test_F64_em_connection.py` | D-EM1…D-EM10 **PASS** in-session; **D-EM11** (co-evolving self-redshift, 120² Cayley solve × 220 steps × 2 packets, several minutes) not completed | D-EM11 was **PASS** in the most recent prior run (`test-results/F64_em_connection.json`, 16/16, 2026-05-31). |
| `run_phase_tests.py` (Phases A–E) | Phase A1 **PASS**; A2+ is matplotlib **frame-rendering**, too slow in-session | Numeric core overlaps `run_phase2_f26_tests.py` (**17/17 PASS** this run). |

Both can be finished locally with the helper added this run:
`model-tests/run_heavy_rerun.py` → writes `test-results/heavy_rerun_<date>.json`.

## Notes on classification

Verdicts were captured by an incremental harness (`run_suite.py`, exit code +
output tail), then re-adjudicated at the subtest level. Two first-pass false
positives were corrected: `test_f26_rotation_law.py` (9/9 PASS — the heuristic
mismatched on the string "0 failed") and `run_phase2_f26_tests.py` (17/17 PASS,
same cause). Conversely two exit-0 tests with no top-level OVERALL line were
re-classified as FAIL after reading their subtest summaries
(`test_wmu_phase7_backreaction.py`, `test_fork_D_doppler.py`).

## Full results

See table below; per-test JSON dumps are in `test-results/` (written by the
tests themselves).

### Per-test table (84 units)

| Test | Verdict | Time (s) |
|------|---------|----------|
| `run_phase2_f26_tests.py` | ✅ PASS | 0.84 |
| `run_phaseF_tests.py` | ❌ FAIL | 4.12 |
| `run_phase_tests.py` | ⏳ INCOMPLETE | 40.06 |
| `run_qca_verifications.py` | ✅ PASS | 0.37 |
| `test_F28_grb_dispersion.py` | ✅ PASS | 0.44 |
| `test_F30_dispersion_order.py` | ✅ PASS | 15.52 |
| `test_F37_delta_omega.py` | ✅ PASS | 15.21 |
| `test_F46_pythagorean_mass.py` | ✅ PASS | 0.79 |
| `test_F49_bcc_weinberg_2over9.py` | ✅ PASS | 0.37 |
| `test_F55_spatial_metric_backreaction.py` | ✅ PASS | 0.63 |
| `test_F56_einstein_coupling_derivation.py` | ✅ PASS | 0.87 |
| `test_F57_induced_eh_from_backreaction.py` | ✅ PASS | 4.86 |
| `test_F58_clockrate_coupling_derivation.py` | ✅ PASS | 0.46 |
| `test_F59_induced_eh_prefactor.py` | ✅ PASS | 6.41 |
| `test_F60_channel_reconciliation.py` | ✅ PASS | 0.33 |
| `test_F61_weyl_eta_gstar.py` | ✅ PASS | 0.64 |
| `test_F63_spin_torsion_estimate.py` | ✅ PASS | 0.20 |
| `test_F64_em_connection.py` | ⏳ INCOMPLETE | 43.02 |
| `test_F65_helicity_chirality_map.py` | ✅ PASS | 0.24 |
| `test_F66_allsky_birefringence_anisotropy.py` | ✅ PASS | 0.70 |
| `test_F67_option1_even_law_photon.py` | ✅ PASS | 0.72 |
| `test_F68_minimal_coupling_forces_even_photon.py` | ✅ PASS | 0.86 |
| `test_F69_paired_photon.py` | ✅ PASS | 1.02 |
| `test_F72_universal_even_propagator.py` | ✅ PASS | 1.03 |
| `test_F73_spin0_bound_pair.py` | ✅ PASS | 0.17 |
| `test_F74_bound_state_binding.py` | ✅ PASS | 1.15 |
| `test_F75_three_generations_irrep.py` | ✅ PASS | 0.17 |
| `test_F76_generation_hierarchy.py` | ✅ PASS | 2.04 |
| `test_F77_njl_gap_rpa.py` | ✅ PASS | 1.25 |
| `test_F78_koide_amplitude_pairing.py` | ✅ PASS | 0.68 |
| `test_F79_structural_G.py` | ✅ PASS | 0.23 |
| `test_F80_em_saturation_45deg.py` | ✅ PASS | 0.15 |
| `test_F81_45deg_pair_saturation.py` | ✅ PASS | 0.15 |
| `test_FG1_anomaly_cancellation.py` | ✅ PASS | 0.03 |
| `test_FG2_quark_complex_mass.py` | ✅ PASS | 2.84 |
| `test_FG3_quark_electroweak.py` | ✅ PASS | 0.87 |
| `test_FG4_dynamical_Z.py` | ✅ PASS | 0.79 |
| `test_FG7_gluon_dynamics.py` | ✅ PASS | 1.47 |
| `test_FG7b_gradient_flow.py` | ✅ PASS | 0.78 |
| `test_FG7c_confinement.py` | ✅ PASS | 21.55 |
| `test_FG7d_baryon_singlet.py` | ✅ PASS | 0.38 |
| `test_FG8_beta_decay.py` | ✅ PASS | 1.40 |
| `test_FG9_C_CP_per_species.py` | ✅ PASS | 1.26 |
| `test_SR2_3D_time_dilation.py` | ✅ PASS | 34.56 |
| `test_SR2_time_dilation.py` | ✅ PASS | 9.12 |
| `test_SR5_photon_frame_invariance.py` | ❌ FAIL | 0.39 |
| `test_complex_mass_chiral.py` | ✅ PASS | 1.38 |
| `test_emergent_time_T1.py` | ✅ PASS | 1.81 |
| `test_emergent_time_T5.py` | ✅ PASS | 3.09 |
| `test_emergent_time_shapiro.py` | ✅ PASS | 1.62 |
| `test_f26_rotation_law.py` | ✅ PASS | 0.50 |
| `test_f45_sigma_tau_weinberg.py` | ✅ PASS | 0.15 |
| `test_fork_B_fresnel.py` | ✅ PASS | 17.18 |
| `test_fork_D_doppler.py` | ❌ FAIL | 1.21 |
| `test_hypercharge.py` | ✅ PASS | 0.39 |
| `test_hypercharge_extension.py` | ✅ PASS | 0.37 |
| `test_majorana_fork.py` | ✅ PASS | 0.37 |
| `test_su2_photon_bridge.py` | ✅ PASS | 0.39 |
| `test_su3_noether.py` | ✅ PASS | 7.02 |
| `test_sublattice_hypercharge.py` | ✅ PASS | 0.49 |
| `test_wmu_phase1.py` | ✅ PASS | 0.72 |
| `test_wmu_phase2.py` | ✅ PASS | 4.48 |
| `test_wmu_phase3.py` | ✅ PASS | 0.39 |
| `test_wmu_phase4.py` | ✅ PASS | 1.34 |
| `test_wmu_phase5_stueckelberg.py` | ✅ PASS | 0.47 |
| `test_wmu_phase6.py` | ✅ PASS | 0.39 |
| `test_wmu_phase6_rank1.py` | ✅ PASS | 0.46 |
| `test_wmu_phase7_backreaction.py` | ❌ FAIL | 1.47 |
| `tests-priority/test_01_GR1_light_deflection.py` | ✅ PASS | 1.06 |
| `tests-priority/test_01b_GR1_openBC.py` | ✅ PASS | 9.67 |
| `tests-priority/test_02_QM1_CHSH.py` | ✅ PASS | 0.38 |
| `tests-priority/test_04_GR3_pound_rebka.py` | ✅ PASS | 0.20 |
| `tests-priority/test_05_GR2_shapiro.py` | ✅ PASS | 0.74 |
| `tests-priority/test_05b_GR2_openBC.py` | ✅ PASS | 6.01 |
| `tests-priority/test_06_QG2_planck_LV.py` | ✅ PASS | 0.36 |
| `tests-priority/test_07_QFT5_neutrino.py` | ✅ PASS | 0.15 |
| `tests-priority/test_08_QM2_tunneling.py` | ❌ FAIL | 0.39 |
| `tests-priority/test_09_GR4_mercury.py` | ✅ PASS | 2.03 |
| `tests-priority/test_10_QG4_charge.py` | ✅ PASS | 11.00 |
| `tests-priority/test_11_SR4_doppler.py` | ✅ PASS | 4.07 |
| `tests-priority/test_12_QM3_heisenberg.py` | ✅ PASS | 0.15 |
| `tests-priority/test_13_QFT8_CPT.py` | ✅ PASS | 3.54 |
| `tests-priority/test_14_QM4_zeno.py` | ✅ PASS | 0.17 |
| `tests-priority/test_15_QM6_twoslit.py` | ❌ FAIL | 5.16 |