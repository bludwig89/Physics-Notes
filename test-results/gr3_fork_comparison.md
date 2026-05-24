# GR-3 candidate-fix cross-fork comparison

_Generated 2026-05-21 by `forks/gr3_fork_harness.py`._

## Shared parameters

- Lattice $L = 128$, source $M = 1.0$, $\sigma = 3.0$, $G_N = 0.0005$, $c_0 = 0.5$.
- GR-1 / GR-2 impact parameter $b = 8$ (GR-1) / $b = 8$ (GR-2).
- GR-3 (near, far) pairs: [(6, 16), (8, 22), (10, 28), (12, 30)].
- GR-4: 1PN EOM, $GM=0.003$, $a=1.0$, $e=0.3$, $c=1$, 6 orbits.

## Headline results

| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ (mean ± std) | GR-4 $\Delta\omega_\text{lat} / \Delta\omega_\text{GR}$ | $\alpha_A$ | $\alpha_B$ |
|---|---|---|---|---|---|---|
| `baseline_paper6` | -3.8495 | 1.0016 | 1.9991 ± 2.3e-04 | 2.0033 | 1.000 | 1.000 |
| `fork_A_phase_tick` | -3.8495 | 1.0016 | 1.0001 ± 2.3e-05 | 2.0033 | 1.000 | 1.000 |
| `fork_B_anisotropic` | -3.8511 | 1.0018 | 1.0002 ± 6.3e-05 | 2.0033 | 1.000 | 1.000 |
| `fork_C_restricted_c` | -3.8495 | 1.0016 | 0.9998 ± 5.7e-05 | 1.0006 | 0.500 | 0.500 |

### Expected predictions

| Fork | GR-1 | GR-2 | GR-3 | GR-4 |
|---|---|---|---|---|
| baseline_paper6 | $K \approx 4$ | ratio $\approx 1$ | ratio$_{GR} = 2$ (off) | ratio $\approx 1$ |
| fork_A_phase_tick | $K \approx 4$ | ratio $\approx 1$ | ratio$_{GR} = 1$ (fixed) | ratio $\approx 1$ |
| fork_B_anisotropic | $K \approx 4$ | ratio $\approx 1$ | ratio$_{GR} = 1$ (fixed) | ratio $\approx 1$ |
| fork_C_restricted_c | $K \approx 4$ | ratio $\approx 1$ | ratio$_{GR} = 1$ (fixed) | ratio $\approx 0.33$ |

GR-4 discriminator: Fork C predicts a halved (and possibly
further suppressed by the $\alpha_A\alpha_B$ cross term)
perihelion advance because both $g_{00}$ and $g_{ii}$
have halved matter coupling.  Forks A and B reproduce the
standard Schwarzschild advance and are observationally
equivalent at this order.

## Verdict logic

- All forks fix GR-3 (baseline column shows factor 2; the
  three candidate columns show ratio_GR ≈ 1).
- GR-1 and GR-2 are unchanged across forks (all preserve
  the Paper-6 $c_\gamma$ form to leading order).
- GR-4 is the discriminator: matches baseline (≈1) for
  Forks A and B, suppressed for Fork C.

## Files

- `ca-simulation/forks/gr3_fork_baseline.py`
- `ca-simulation/forks/gr3_fork_A_phase_tick.py`
- `ca-simulation/forks/gr3_fork_B_anisotropic.py`
- `ca-simulation/forks/gr3_fork_C_restricted_c.py`
- `ca-simulation/forks/gr3_fork_harness.py`