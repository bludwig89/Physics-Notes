# casim exactness inventory (auto-generated)

_Generated 2026-06-05 - 04:01 by `casim inventory` (casim.analysis.inventory). 13/13 checks pass._

Auto-generated from `casim.verify.run_all()`; do not edit by hand. This is scoped to the `casim` engine and does **not** replace the repository's hand-maintained `exactness-inventory.md`.

| check | channel | class | residual | tolerance | pass |
|---|---|---|---|---|---|
| kernel_fidelity | photon_pair | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | weyl_bcc | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | w_chiral | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | z_even | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | gluon_bcc | exact | 0.000e+00 | 1e-12 | ✅ |
| norm_drift | weyl_bcc | machine-precision | 3.726e-14 | 1e-10 | ✅ |
| unitarity_residual | weyl_bcc | exact | 6.345e-16 | 1e-12 | ✅ |
| eikonal_vs_GR | gravity_dielectric | quantitative | 1.892e-03 | 1e-02 | ✅ |
| resume_bit_identical | weyl_bcc | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | fermion↔W | exact | 0.000e+00 | 1e-12 | ✅ |
| kernel_fidelity | beta_decay | exact | 0.000e+00 | 1e-12 | ✅ |
| charge_continuity | charge_photon | machine-precision | 8.058e-16 | 1e-10 | ✅ |
| kernel_fidelity | gauge_mc | exact | 0.000e+00 | 1e-12 | ✅ |

## Classes

- **exact** — algebraically zero; evaluated in float64 it sits at the round-off floor (gate 1e-12).
- **machine-precision** — converges to the FFT/float floor (gate 1e-10).
- **quantitative** — a measured physical agreement with its own gate (e.g. eikonal-vs-GR < 1%).
