# F101 — Full strong-coupling σ from the rule's compact-rotor transfer operator: the non-perturbative log law and the Gaussian–confinement crossover

**Date:** 2026-06-05 - 15:35
**Status:** Confirmed — 5/5 checks PASS. S1 exact (charge-basis diagonalisation, truncation-converged $4\times10^{-16}$); S2/S3 asymptotically exact (weak→Gaussian, strong→log, relative errors $\to0$); S4 reconciliation with F70 (both slopes $\to-1$; leading character $\beta/18$); S5 the compact correction at the rule's coupling. **Extends F100 past the Gaussian/spin-wave regime to all couplings.**
**Script:** `model-tests/test_F101_strong_coupling_sigma.py` (<0.2 s)
**Results:** `test-results/F101_strong_coupling_sigma.json`
**Cross-references:** [[F100-gamma-from-transfer-operator]] (the Gaussian limit this extends; same transfer operator, now kept compact), [[F70-gradient-flow-confinement-string-tension]] (the all-coupling SU(3) $-\ln w(\beta)$ reconciled), [[F99-sigma-as-centre-lagrange-multiplier]] ($\sigma=-\ln s_1$), [[F95-B-derived-C-localized]] (BZ-average structure), [[F26-c-as-rotation-rate]] ($\Omega$).

---

## 1. What this closes

F100 derived $\sigma$ from the rule's transfer operator **in the Gaussian / spin-wave regime**, treating the plaquette flux $\phi$ as a *non-compact* Gaussian variable ($\sigma_1=\sigma_\phi^2/2$). That approximation misses the **compactness** of the flux — $\phi$ is an angle on a circle — which is exactly what dominates the strong-coupling, non-perturbative regime where confinement actually lives. This finding keeps the same transfer operator but **compact**, giving $\sigma$ at all couplings with no Gaussian assumption.

## 2. The compact rotor — the rule's single-plaquette transfer operator, kept exact

The rule's $(E,B)$ phase rotation, restricted to one plaquette mode and Wick-rotated, is the quantum rotor (Mathieu) Hamiltonian

$$H=\frac{1}{2\chi}\hat E^2-\lambda\cos\hat\phi,\qquad \hat E\,|m\rangle=m\,|m\rangle,\quad \cos\hat\phi:\;|m\rangle\leftrightarrow|m\pm1\rangle,$$

in the **integer-charge (Fourier) basis** — where $\hat E$ (the electric field) has the *compact* integer spectrum, the feature the Gaussian dropped. $\chi$ is the electric stiffness (moment of inertia), $\lambda$ the magnetic stiffness; the harmonic frequency is $\Omega=\sqrt{\lambda/\chi}$ (the F100 rotation rate). The ground state gives the centre order parameter at **all** couplings:

$$s_1=\langle e^{i\hat\phi}\rangle=\sum_m g_m\,g_{m+1},\qquad \sigma_1=-\ln s_1,$$

solved exactly by dense Hermitian diagonalisation (truncation-converged to $4\times10^{-16}$). $\sigma_1(\lambda)$ is monotone, spanning $\sim3.9$ (strong) down to $\sim0.03$ (weak).

## 3. The two limits — and the crossover between them

**Weak coupling $\lambda\to\infty$ (S2) → F100's Gaussian.** Large magnetic stiffness freezes the flux into a small arc; the rotor reduces to the oscillator and

$$\sigma_1\to\frac{1}{4\sqrt{\lambda\chi}}\quad(\chi{=}1:\ \tfrac1{4\Omega}),$$

reproducing F100 (relative error $\to0.3\%$ by $\lambda=2000$). The compact answer *contains* the Gaussian one.

**Strong coupling $\lambda\to0$ (S3) → non-perturbative log confinement.** First-order rotor perturbation theory: $|\psi_0\rangle\simeq|0\rangle+\lambda\chi(|1\rangle+|{-}1\rangle)$, so

$$s_1\to 2\lambda\chi\quad\Longrightarrow\quad\boxed{\ \sigma_1\to-\ln(2\lambda\chi)\ }\;\to\infty.$$

This is the genuine **strong-coupling area law $\sigma\sim-\ln(\text{coupling})$** — confinement as a logarithm of the magnetic stiffness, the regime the Gaussian could never reach (relative error $2\times10^{-5}$ at $\lambda=0.005$). Compactness is the whole story here: it is the integer charge spectrum that makes $s_1\to0$ and $\sigma\to\infty$ as the coupling softens.

So one exactly-solved operator interpolates from F100's weak-coupling $\tfrac1{4\sqrt\lambda}$ to the non-perturbative $-\ln(2\lambda)$ — the Gaussian–confinement crossover.

## 4. Reconciliation with F70 (S4) — the same logarithmic law

The strong-coupling slope $d\sigma/d\ln(\text{coupling})\to-1$ for **both** the rotor ($-0.999$) and F70's $-\ln w(\beta)$ ($-1.004$): a universal logarithm. And F70's plaquette weight has the exact SU(3) leading character coefficient

$$w(\beta)\to\frac{\beta}{2N^2}=\frac{\beta}{18}\quad(\text{measured }0.05560\text{ vs }1/18=0.05556),$$

so $\sigma_{F70}\to-\ln(\beta/18)$ — the same $-\ln(\text{coupling})$ form as the rotor's $-\ln(2\lambda)$. The rotor's $\lambda$ and F70's $\beta/18$ are the same magnetic coupling seen from the Hamiltonian and Euclidean sides; they confine by the identical logarithm.

## 5. The compact correction at the actual rule (S5)

Mapping $\lambda=\chi\Omega^2$, the rotor extends F100's $\gamma(\Omega)$/$\sigma(\Omega)$ to all couplings. At the actual 2D rule's *moderate* coupling ($\Omega\approx1.3$) the compact rotor corrects F100's Gaussian $\sigma$ **upward by $\sim12\%$** ($0.2150$ vs $0.1923$) — compactness adds disorder the Gaussian under-counts. Softening the rule ($\Omega\to0.1$) drives $\sigma>3.9$, into strong-coupling confinement. The real rule sits near the weak end, where the $\sim12\%$ compact correction is the leading non-Gaussian effect.

## 6. Check summary (5/5)

| Check | Statement | Tier | Residual |
|---|---|---|---|
| S1 | compact rotor $\sigma(\lambda)=-\ln\langle e^{i\phi}\rangle$ exact at all couplings; monotone, truncation-converged | 1/2 | trunc $4\times10^{-16}$ |
| S2 | weak limit $\to$ F100 Gaussian $1/(4\sqrt{\lambda\chi})$ | asymptotic | rel $\to0.3\%$ |
| S3 | strong limit $s_1\to2\lambda\chi$, $\sigma\to-\ln(2\lambda\chi)$ (log confinement) | asymptotic | rel $2\times10^{-5}$ |
| S4 | F70 reconciliation: both slopes $\to-1$; $w\to\beta/18=\beta/(2N^2)$ | 1 + numeric | slopes $-0.999/-1.004$ |
| S5 | rule map $\lambda=\chi\Omega^2$; compact correction $+12\%$ at $\Omega{=}1.3$; soft $\Omega$ confines | numeric | $+11.8\%$ |

## 7. Honest scope

- **Reduced single-plaquette / single-mode rotor.** The exact crossover is for the effective single-plaquette degree of freedom; the full multi-mode interacting compact theory (true 3+1D $\sigma$) is still F94's gauge-MC. The rotor is the exactly-solvable bridge that shows *the mechanism* (compactness → log law) and matches F70 in 2D.
- **U(1) rotor vs $\mathbb{Z}_3$ centre.** The rotor here is the compact U(1) parent; the centre is $\mathbb{Z}_3$. The strong-coupling log law and the limits are robust to this, but the precise centre projection at intermediate coupling carries the same A-vs-C / Casimir caveat as F98–F100 ($\sigma_2=2\sigma_1$ Abelian vs $\sigma_1$ Casimir).
- **$\chi$ normalisation.** $\chi=1$ (the symmetric $(E,B)$ rotation); a physical electric/magnetic stiffness ratio rescales $\lambda$ (not the limits or the log law).

## 8. Provenance

- New content: the compact-rotor transfer operator at all couplings (§2), the strong-coupling log law $\sigma\to-\ln(2\lambda\chi)$ from rotor PT (§3), the F70 reconciliation via the $\beta/18$ leading character and the $-1$ log slope (§4), the compact correction at the rule's coupling (§5).
- Reused: F100 Gaussian limit; F70 `ca_confinement` ($-\ln w$, $w$, leading coefficient); F99 $\sigma=-\ln s_1$.
- Verification: `model-tests/test_F101_strong_coupling_sigma.py` (2026-06-05, 5/5 PASS), results `test-results/F101_strong_coupling_sigma.json`.
