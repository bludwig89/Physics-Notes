# F140 — The coarse-grained baryon element

`2026-06-11 - 06:50`

**Status.** Supplies the lattice baryon F132 deferred. Module
`ca-simulation/ca_baryon_blockspin.py`; tests
`tests/findings/test_F140_coarse_grained_baryon.py` (9/9 PASS).

---

## 1. What F132 left and F140 closes

F132 coarse-grained the pion and deuteron as real lattice bound states, but
handled the **baryon by ingredient covariance only** — its mass is the
F130-C1-covariant string scale ($E_\text{rel}\propto\sigma^{2/3}$) — because the
F122 three-quark solver is an explicitly-correlated-Gaussian (ECG) *basis*, not a
lattice that $R_b$ can act on. F140 builds a genuine **lattice baryon element**
that can be block-spun, and shows the proton's mass is reproduced on a coarse
lattice.

## 2. The hyperradial element

The rest-frame three-equal-mass-quark problem is 6-D (mass-normalised Jacobi
$\xi_1,\xi_2$; F122). Projecting onto the **hyperradius**
$\rho^2=\xi_1^2+\xi_2^2$ in the lowest ($K=0$) hyperspherical channel — the
symmetric S-state that dominates the confined ground state — reduces the 6-D
Laplacian to a 1-D radial equation for $u(\rho)=\rho^{5/2}R$:

$$-\frac1{2m}u'' + \frac1{2m}\frac{15/4}{\rho^2}u + V_\text{eff}(\rho)\,u = E\,u,
\qquad V_\text{eff}=C_\sigma\,\sigma\,\rho,$$

with the $d{=}6,\,K{=}0$ centrifugal $15/4=(d-1)(d-3)/4$ and the confinement
coefficient from the hyperangular average of the three pair lengths
$\sqrt2\,\rho\,|\hat n\!\cdot\!\hat e|$ over the unit 5-sphere:

$$C_\sigma = 3\sqrt2\,\langle|u|\rangle_{S^5} = 3\sqrt2\cdot\frac{16}{15\pi}
= \frac{16\sqrt2}{5\pi} = 1.4405.$$

(The one-gluon-exchange $1/r$ has a *divergent* $K{=}0$ hyperangular average — it
couples high-$K$ channels — so the confinement-dominated baryon, the F122 case, is
the clean one; the OGE is an optional regularised, subdominant correction.)

## 3. It reproduces the F122 baryon

The fixed-$K{=}0$ channel captures the confinement **scaling exactly**
($E_\text{rel}\propto\sigma^{2/3}$, measured slope $0.6666$) but only $\sim63\%$ of
the full ECG energy — the higher-$K$ channels are the rest (the adiabatic gap). A
single, $\sigma$-**independent** effective coefficient $C_\text{eff}=\kappa\,C_\sigma$
matched once to the ECG ($\kappa=2.0005$) makes the element reproduce the F122
baryon **across the whole $\sigma$ range to $<0.05\%$** — an EFT-style matching, not
a per-point fit (the match at $\sigma{=}1$ and at $\sigma{=}4$ give the same $\kappa$
to $<1\%$, because both energies scale as $\sigma^{2/3}$).

| $\sigma$ | element $E_\text{rel}$ | ECG $E_\text{rel}$ | rel. err |
|---|---|---|---|
| 0.5 | 3.8654 | 3.8667 | 0.03 % |
| 1.0 | 6.1359 | 6.1358 | 0.00 % |
| 2.0 | 9.7400 | 9.7453 | 0.05 % |
| 4.0 | 15.4610 | 15.4574 | 0.02 % |

## 4. It coarse-grains (the payoff)

The element is a 1-D lattice, so $R_b$ is hyperradial grid decimation
($h\to b\,h$). At fixed physical $C_\text{eff}$ the smooth linear potential
block-averages and the baryon mass + rms hyperradius are reproduced on $b\times$
fewer cells, with the irrelevant $O(h^2)$ error:

| $b$ | $h$ ratio | $E_\text{rel}$ rel. err | rms rel. err | amplitude overlap | cells |
|---|---|---|---|---|---|
| 2 | ×2 | 0.01 % | 0.01 % | 0.99994 | 1200 → 600 |
| 4 | ×4 | 0.03 % | 0.06 % | 0.99941 | 1200 → 300 |
| 8 | ×8 | 0.13 % | 0.27 % | 0.99668 | 1200 → 150 |

The coarse baryon stays confined (positive $E_\text{rel}$, sensible hyperradius)
and the error grows $\sim b^2$ — the same irrelevant-operator behaviour as the
F132 deuteron and the F130 T2 LIV operators.

In *lattice* units the confining coupling is instead the **relevant** operator
$\hat\sigma\to b\,\hat\sigma$ (eigenvalue $\lambda_\sigma=b>1$, identical to
F130-C1), so the physical baryon mass — a function of the physical string scale —
is the RG-invariant either way. The proton coarse-grains.

## 5. Honest limits

- **$K=0$ adiabatic channel.** The element uses the lowest hyperspherical
  harmonic; the $\sim37\%$ higher-$K$ energy is absorbed into the single matched
  $\kappa$. This is exact for the confinement *scaling* and quantitatively
  matched for the *magnitude*, but it is not a full multi-channel hyperspherical
  solve.
- **Confinement-dominated regime** (OGE off / regularised) — the F122 case; the
  attractive $1/r$ needs high-$K$ channels and is not reduced here.
- **Mass scaling, not absolute SI.** As throughout F122/F132-B, the absolute
  baryon mass in MeV is P6/scale-setting; F140 is about the *coarse-graining* of
  the confined three-body element.

## 6. Files

- `ca-simulation/ca_baryon_blockspin.py` — `hyperradial_baryon`,
  `calibrate_to_ecg`, `baryon_confinement_scaling`, `baryon_coarse_grain`,
  `confinement_relevant_flow`; closed-form hyperangular constants. Wraps
  `ca_baryon_dynamics` (ECG) read-only.
- `tests/findings/test_F140_coarse_grained_baryon.py` — 9 tests (K1–K5).
- Exactness inventory rows #85–86.
