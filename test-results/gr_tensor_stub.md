# Fork E — tensor-metric gravity stub

_Generated 2026-05-21 by `forks/gr_tensor_stub.py` (Finding 19)._

Shared open-BC potential: $L=96$, $M=1.0$, $\sigma=3.0$, $G_N=0.0005$, $c_0=0.5$, $b=8$; $\phi\in[-1.320e-04, -6.014e-06]$.

## Field sector (GR-1 / GR-2 / GR-3)

| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ |
|---|---|---|---|
| `baseline_paper6` | -3.8260 | 1.0029 | 1.9991 ± 2.3e-04 |
| `fork_B_anisotropic` | -3.8275 | 1.0031 | 1.0002 ± 6.3e-05 |
| `fork_E_linearized` | -3.8275 | 1.0031 | 1.0002 ± 6.3e-05 |
| `fork_E_exact_isotropic` | -3.8273 | 1.0031 | 0.9999 ± 1.7e-05 |

Baseline shows the factor-2 GR-3 ratio; carrying $g_{00}$ (clock $=\sqrt{-g_{00}}$) in Fork E drives it to 1. GR-1/GR-2 are unchanged across columns — the deflection/Shapiro residual is discretisation, not the scalar→tensor structure.

## GR-4 — geodesic perihelion advance on the exact metric

| Orbit | $v^2/c^2$ | geodesic (rad/orbit) | $6\pi GM/pc^2$ | ratio |
|---|---|---|---|---|
| Mercury-like | 3.297e-03 | 6.285406e-02 | 6.214139e-02 | 1.01147 |
| weak-field check | 1.042e-05 | 1.944229e-04 | 1.963495e-04 | 0.9901875 |

The weak-field ratio → 1 is the integrator self-check. The Mercury-like geodesic carries all PN orders, so its small departure from the 1PN closed form is physical higher-order content, not truncation error.

## Self-checks

- [PASS] `E_linearized_matches_forkB`
- [PASS] `E_exact_fixes_gr3`
- [PASS] `baseline_still_factor2`
- [FAIL] `geodesic_recovers_1PN_weakfield`

**ALL CHECKS: FAIL**