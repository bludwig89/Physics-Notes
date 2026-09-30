# F62 — Dynamical Dirac CA on a curved background (D2) + linearized backreaction (D3a)

_Generated 2026-05-30 - 15:30 by `tests/findings/test_F62_dirac_gravity_fork.py`._

**5/6 PASS** (total 40.14 s). Module: `src/casim/engine/forks/gravity/dirac_gravity_fork.py`.

| Test | Pass | Key numbers |
|---|---|---|
| D1 flat Weyl regression | True | residual = 0.0e+00 |
| D2a Rindler free-fall | True | |g|/a·c_lat² = 0.9363, mass-universality spread = 0.04773, norm drift = 1.2e-14 |
| D2b dynamical redshift | True | ratio_meas = 0.9, pred = 0.9 |
| D2c Schwarzschild deflection | True | K_eik = -3.92, K_meas = -3.432, meas/eik = 0.8755 |
| D3a backreaction norm | True | norm drift = 2.4e-15 |
| D3a self-redshift | False | A_near = 0.7921, A_far = 1.024, ratio_meas = 1, pred = 0.8797 |
