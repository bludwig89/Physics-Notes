# F257 — The hydrogen Bethe logarithm derived from the model's own Coulomb spectrum (no literature input)

**Date:** 2026-07-20 - 14:30
**Status:** Confirmed — 4/4 checks PASS. The Bethe logarithms $\ln k_0(1s,2s,2p)$ are computed from the model Hamiltonian's Coulomb resolvent (Dalgarno–Lewis), reproducing the accepted values to ~2–3% with **no literature constant**; the resulting fully model-derived Lamb shift is $1059.9$ MHz vs measured $1057.845$ MHz.
**Module:** `ca-simulation/ca_bethe_log.py` (+ `ca_vertex_loop.lamb_shift_model_bethe`)
**Verification script:** `tests/findings/test_F257_bethe_log_from_spectrum.py`
**Result file:** `test-results/F257_bethe_log_from_spectrum.json`
**Cross-references:** [[F252-qed-vertex-ae-lamb-shift]] (removes its one literature input — the tabulated Bethe log — making the Lamb shift fully model-derived), [[F251-qed-vacuum-polarization-running-alpha]] (the Uehling piece), [[F125-p5-hydrogen-atom-em-bound-state]] (the Coulomb Hamiltonian whose resolvent is sampled).

---

## The claim

F252 computed the hydrogen Lamb shift but used the tabulated Bethe logarithm ($\ln k_0(2s)=2.8118$, Drake/Klarsfeld) as a literature constant. This finding **removes that input**: the Bethe logarithm — a log-weighted mean excitation energy over the full intermediate spectrum — is computed from the model's own Coulomb Hamiltonian, so the Lamb shift becomes a fully model-derived number.

$$\ln k_0(n,l)=\frac{\sum_m |\langle n|\mathbf p|m\rangle|^2 (E_m-E_n)\ln|E_m-E_n|}{\sum_m |\langle n|\mathbf p|m\rangle|^2 (E_m-E_n)}.$$

---

## Method — Dalgarno–Lewis resolvent (no slow state-sum)

A direct pseudostate sum converges very slowly (the $\ln|E_m-E_n|$ weight emphasises high-energy virtual states — every gauge, length/velocity/acceleration, was checked and all crawl). The state-sum is instead turned into a one-dimensional integral over the **Coulomb resolvent** using $\ln\varepsilon=\int_0^\infty[\tfrac1{1+t}-\tfrac1{\varepsilon+t}]dt$:

$$\ln k_0=\frac1D\int_0^\infty\!\Big[\frac{M_3}{1+t}-M_2+tM_1-t^2M_0+t^3F(t)\Big]dt+\ln 2,$$

with the length source $g_r=r\,u_n$, the energy moments $M_p=\langle g_r|(H_l-E_n)^p|g_r\rangle$, the denominator $D=M_3=\sum|\langle p\rangle|^2\Delta E$, and

$$F(t)=\langle g_r|(H_l-E_n+t)^{-1}|g_r\rangle$$

a **stable tridiagonal solve** of the inhomogeneous radial equation on the model's finite-difference Coulomb Hamiltonian — i.e. it samples the model's own spectrum through its resolvent. The $+\ln 2$ converts the Hartree-unit energies in the log to Rydberg (the tabulated convention).

**Below-threshold / degenerate intermediate states** (the 2p case: $1s$ lies below $2p$, $2s$ is degenerate) violate the $\varepsilon>0$ identity; they are projected out of the resolvent and added explicitly — the degenerate $\Delta E=0$ state contributes $0$; the below state contributes $|\langle p\rangle|^2\Delta E\ln|\Delta E|$ with $\Delta E<0$ (this is why $\ln k_0(2p)$ is small and negative).

---

## Results (grid $N=8000$, O($h$) Richardson)

| state | model $\ln k_0$ | accepted | deviation |
|-------|:---------------:|:--------:|:---------:|
| $1s$ | 2.9204 | 2.9841 | −2.1% |
| $2s$ | 2.7479 | 2.8118 | −2.3% |
| $2p$ | −0.0369 | −0.0300 | +0.007 (abs) |

**Fully model-derived Lamb shift** (no literature Bethe log): self-energy $+1087.1$ MHz (from the model $\ln k_0$) $+$ Uehling $-27.1$ MHz (from F251's $\Pi$) $=\mathbf{1059.9}$ MHz vs measured $1057.845$ MHz — **within 0.2%**. (With the literature Bethe log F252 gets $1052.2$ MHz; both bracket the measured value within ~0.6%. The slight over-shoot here is partly a fortuitous compensation: the ~2% low $\ln k_0(2s)$ raises the self-energy, offsetting the omitted higher-order QED. The honest statement is that the model-derived Bethe log yields a leading-order Lamb shift consistent with experiment to ~1%.)

---

## Verification summary (4/4)

| # | Check | Result |
|---|-------|:------:|
| B1 | $\ln k_0(1s)$ from model resolvent | 2.920 vs 2.984 (2.1%) |
| B2 | $\ln k_0(2s)$ from model resolvent | 2.748 vs 2.812 (2.3%) |
| B3 | $\ln k_0(2p)$ (below-threshold handled) | −0.037 vs −0.030 |
| B4 | Lamb shift, model Bethe log, vs measured | 1059.9 vs 1057.845 MHz |

---

## Scope and honesty

- **No literature Bethe log.** The values come entirely from the model's Coulomb Hamiltonian via its resolvent; the accepted numbers are used only for comparison.
- **Precision.** On a uniform radial grid the result converges as $O(h)$ and is limited to ~2–3% by the discretisation of the high-energy continuum (the short-distance region that dominates $M_3$; the O($h$) Richardson is self-consistent across grid pairs but the residual is a continuum-representation systematic, not a grid-spacing one). Reaching the tabulated 6-digit values needs a nucleus-clustered (logarithmic) grid or a Coulomb–Sturmian basis with the continuum tail handled analytically — the natural refinement, noted but not required for the physics point.
- **What is established.** The Bethe logarithm — the last literature input in the F252 Lamb shift — is derivable from the model's own spectrum, and doing so yields a Lamb shift consistent with measurement to ~1%. The Lamb shift is now a fully model-derived quantity.

---

## Files
- Module: `ca-simulation/ca_bethe_log.py`
- Lamb-shift wiring: `ca-simulation/ca_vertex_loop.py` (`lamb_shift_model_bethe`)
- Test: `tests/findings/test_F257_bethe_log_from_spectrum.py`
- Results: `test-results/F257_bethe_log_from_spectrum.json`
