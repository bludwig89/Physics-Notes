# GR-3 Forks A & B — extended run

_Generated 2026-05-21 20:31 by `forks/gr3_forks_AB_extended.py`._

## Parameters

- Lattice $L=192$, $M=1.0$, $\sigma=3.0$, $G_N=0.0005$, $c_0=0.5$.
- GR-1/GR-2 impact parameter $b=8$.
- GR-3 (near, far) pairs: [(6, 16), (8, 22), (10, 28), (12, 30)].
- GR-4: 12 orbits, dt=5e-03, $GM=0.003$, $a=1$, $e=0.3$, $c=1$.

## Results

| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ (mean ± std) | GR-4 $\Delta\omega_\text{lat}/\Delta\omega_{\rm GR}$ | $\alpha_A$ | $\alpha_B$ | Perihelia |
|---|---|---|---|---|---|---|---|
| `fork_A_phase_tick` | -3.8666 | 1.0006 | 1.0001 ± 2.3e-05 | 2.0035 | 1.000 | 1.000 | 13 |
| `fork_B_anisotropic` | -3.8681 | 1.0007 | 1.0002 ± 6.3e-05 | 2.0035 | 1.000 | 1.000 | 13 |

## Interpretation

Forks A and B both use the full Schwarzschild metric ($\alpha_A=\alpha_B=1$), so:

- GR-1 and GR-2 should be identical to the baseline (photon sector unchanged).
- GR-3 should land near 1.0 (the factor-2 Pound-Rebka issue is fixed).
- GR-4 should land near **2.00** for these forks (the 3π normalisation in the harness means the Schwarzschild 6π advance yields ratio = 2; Fork C at α_A=α_B=0.5 would give ratio ≈ 1.00).

A larger spread in `orbit_std` across the 12 orbits than in the 6-orbit run would indicate unmodelled 2PN or numerical drift.
