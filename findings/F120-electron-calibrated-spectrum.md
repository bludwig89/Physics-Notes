# F120 — Calibrating the single mass scale on the electron: the locked-cell shape predicts the charged-lepton spectrum to 0.1 % from one mass and reads every fermion out in kg — with the sharp lesson that the electron is the *worst* anchor (it sits at the condensate node) and the τ is the ideal one (exactly δ-stable at the wall)

**Date:** 2026-06-09 - 16:30
**Status:** Confirmed — 7/7 checks PASS (`test_F120_electron_calibrated_spectrum.py`, <1 s). Pure math/numpy (no scipy, per CLAUDE.md). Executes the F119 follow-up: fix the one open scale $N$ with the electron and turn the model's dimensionless shape into absolute masses (MeV and kg).
**Script:** `tests/findings/test_F120_electron_calibrated_spectrum.py`
**Results:** `test-results/F120_electron_calibrated_spectrum.json`
**Cross-references:** [[F119-kg-scale-three-routes]] (the single open scale $N$ and the $\lambda_6=\tfrac14$ angle this uses), [[F118-self-consistent-Wvc-and-C]] / [[F101b-one-heavy-branch-fit-W]] (the condensate, equipartition $A=\sqrt2\bar y$, wall-pinning $y_\tau=1$), [[F96-second-shell-Eg-gap-saturation]] (the texture algebra $Q=\tfrac23\Leftrightarrow\delta=15°$), [[F78-koide-amplitude-from-cooper-pair]] ($m=y^2$, Koide), [[F46-pythagorean-lattice-mass]] / [[F83-fix-lattice-spacing-from-fermion-mass]] (the SI mass map), [[F112-si-predictions-from-canonical-a]] (the locked cell).

---

## 1. The calibration

The kilogram is already a unit (F119): with the cell locked (F107), $\hbar$ carries the kg and $m_\text{phys}=\hbar\arcsin(m_\text{lat})/(\tau c^2)$ returns kg with no free parameter (C1: the electron round-trips to $<10^{-12}$). The model supplies the dimensionless **shape** of the charged-lepton spectrum — the $E_g$ condensate at angle $\delta$ with equipartition $A=\sqrt2\bar y$ (F80/F92/F101), masses $m_a=y_a^2$ (F78), heaviest wall-pinned (F101-A0):

$$y_a=\bar y\,(1+\sqrt2\cos\theta_a),\quad \theta_a=\delta+\tfrac{2\pi a}{3},\quad \bar y=\frac{1}{1+\sqrt2\cos\delta}\ (\text{wall }y_\tau=1),\quad m_a=y_a^2.$$

So **$\delta$ alone fixes every mass ratio** and one measured mass fixes the scale $N$. We fix $N$ with the electron, as requested.

## 2. Electron-calibrated lepton spectrum (measured angle): 0.1 %

With the measured condensate angle $\delta=12.733°$, anchoring the scale on $m_e=0.510999$ MeV (C2):

| lepton | predicted (MeV) | predicted (kg) | PDG (MeV) | error |
|---|---|---|---|---|
| $e$ | 0.510999 *(anchor)* | $9.109384\times10^{-31}$ | 0.510999 | — |
| $\mu$ | **105.72** | $1.884666\times10^{-28}$ | 105.658 | **+0.06 %** |
| $\tau$ | **1777.95** | $3.169476\times10^{-27}$ | 1776.86 | **+0.06 %** |

From a *single* mass plus the equipartition shape, both heavier leptons land within 0.06 %. Koide $Q=2/3$ holds geometrically (C5: condensate $Q=0.666667$; data $0.666661$). This confirms the shape — with the caveat that $\delta$ here is taken from data (one extra input).

## 3. The sharp lesson: the electron is the worst anchor

When the angle is instead the model's own first-principles value ($\lambda_6=\tfrac14\Rightarrow\delta=13.36°$, F119-W2), the **electron-anchored** prediction is unstable — $m_\mu$ off by **+104 %** (C3). The reason is geometric: the electron sits near the **condensate node**, where $|\partial\ln m/\partial\delta|$ is $\approx10\times$ the muon's, while the **τ is exactly δ-stable** ($m_\tau^\text{cond}=1$ for all $\delta$, by wall-pinning). Anchoring on the lightest, most node-sensitive state amplifies the 2.7 % $\lambda_6$ uncertainty into an $O(1)$ scale error.

Anchor robustness at the model angle (C4):

| anchor | predicts | error | predicts | error |
|---|---|---|---|---|
| **τ** (wall, δ-stable) | $m_\mu$ | **+5.5 %** | $m_e$ | −48 % (node) |
| $\mu$ | $m_\tau$ | −5.2 % | $m_e$ | −51 % (node) |
| $e$ (node) | $m_\mu$ | +104 % | $m_\tau$ | +93 % |

The heavy ratios are predicted to $\sim5\%$ from the τ anchor (tracking the $\lambda_6$ error); the electron is intrinsically uncertain wherever the angle is. **Recommendation: anchor the scale on the τ (the wall), not the electron** — even though the electron was the requested anchor, the τ is the physically robust one.

## 4. Every fermion in kg

Once $N$ is set (C6), the whole fermion sector reads out in kg. Leptons are *predicted* by the shape (≤0.1 %); quark entries are the *measured* masses converted to kg — the model fits, not predicts, the quark texture, so these are a **consistency** readout, not a prediction:

| fermion | mass (kg) | tier |
|---|---|---|
| up | $3.85\times10^{-30}$ | consistency |
| down | $8.33\times10^{-30}$ | consistency |
| strange | $1.67\times10^{-28}$ | consistency |
| charm | $2.26\times10^{-27}$ | consistency |
| bottom | $7.45\times10^{-27}$ | consistency |
| top | $3.08\times10^{-25}$ | consistency |

## 5. What is genuinely predicted vs calibrated

**Predicted (parameter-free):** Koide $Q=2/3$; the *entire* lepton shape from one mass plus the angle. **Calibrated:** the overall scale $N$ (one mass — the F119 open number) and the angle $\delta$ (whose exact value is the open $\lambda_6$, F118/F119). **Consistency only:** the quark masses in kg. The honest reading: with one mass and the measured angle the lepton sector is reproduced to 0.1 %; the irreducible open inputs remain exactly two — the overall scale $N$ and the angle $\lambda_6$ — both flagged in F119.

> **Relabel (F179, 2026-06-29 — audit C2).** The angle, not $\lambda_6$, is the honest one-parameter handle: $\lambda_6$ is convention-laden and is **not** a clean rational (the "$\approx\tfrac14$" framing above misses the data angle by $0.67°$; $\tfrac29$ misses by $2.48°$). The convention-independent statement is the condensate angle $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$), Koide-locked to data at $<1\sigma$ but **not derived**. Granting that one relation, one anchor reproduces the spectrum to $0.01\%$ — so this section's "predicted (parameter-free)" should read **one-angle consistency fit** (one Koide-locked angle + one scale $N$), not a zero-parameter prediction. See [[F179-lambda6-derivation-attempt-and-relabel]].

## 6. Test summary (`test_F120_electron_calibrated_spectrum.py`, 2026-06-09 - 16:30)

| Check | Statement | Result | Status |
|---|---|---|---|
| C1 | $m_e$ fixes $N$; locked-cell map round-trips | $<10^{-12}$ | PASS |
| C2 | e-anchored, measured angle: $m_\mu,m_\tau$ | +0.06 %, +0.06 % | PASS |
| C3 | e-anchored, model angle: unstable (node) | $m_\mu$ +104 %; e/μ sens. ×10 | PASS |
| C4 | τ is the robust anchor (wall, δ-stable) | $m_\mu$ +5.5 % | PASS |
| C5 | Koide $Q=2/3$ | $0.666667$ | PASS |
| C6 | full fermion kg table | leptons ≤0.1 % | PASS |
| V | verdict | — | PASS |

**Overall 7/7 PASS** (<1 s).

## 7. Provenance

- New content: the electron-calibrated lepton spectrum in MeV and kg (C2); the node-sensitivity analysis showing the electron is the worst anchor and the wall-pinned τ exactly δ-stable (C3/C4); the full fermion kg readout (C6).
- Machinery: the F101/F118 condensate shape (equipartition, wall-pinning); PDG 2024 masses; CODATA 2018 constants and the F79/F107 locked cell.
- Verification: `tests/findings/test_F120_electron_calibrated_spectrum.py` (2026-06-09 - 16:30, 7/7 PASS), results `test-results/F120_electron_calibrated_spectrum.json`.
