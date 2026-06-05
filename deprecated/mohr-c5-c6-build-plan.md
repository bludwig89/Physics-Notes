# Mohr 2010 §C Gap Build — C1–C6 Status and C5/C6 Spec

*Drafted 2026-05-21 - 19:55. Source list: `reference-research/mohr-2010-maxwell-photon-wf-summary.md` §C.*

This doc captures the build status of the six items in [`mohr-2010-maxwell-photon-wf-summary.md`](reference-research/mohr-2010-maxwell-photon-wf-summary.md) §C ("Gaps — What Mohr Has That We Do Not"). C1–C4 are already implemented; this doc records that fact alongside the line refs and inventory IDs, then specifies C5 and C6 for build.

---

## Status table

| Item | Description | Status | Code | Inventory |
|---|---|---|---|---|
| **C1** | Explicit normalized polarization eigenstates $\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}})$ (Mohr Eqs. 210–216) | ✅ done | `ca_maxwell.py::polarization_basis`, `test_polarization_basis` (L276–352) | Tier 1 #22, #23, #24 |
| **C2** | Longitudinal (λ=0) photon mode $\psi^{(+)}_{\boldsymbol{k},0}$ (Mohr Eqs. 235, 237, 240, 249) | ✅ done | `ca_maxwell.py::longitudinal_mode`, `longitudinal_transverse_orthogonality` (L501–554) | Tier 1 #28, #29, #30 |
| **C3** | Lorentz boost behavior of $E_G, B_G$ via $\mathcal{V}(\boldsymbol{v})$ (Mohr Eqs. 171, 281–287) | ✅ done | `ca_maxwell.py::_lorentz_boost_6x6`, `lorentz_boost_covariance` (L402–494) | Tier 1 #25, #26, #27 |
| **C4** | Probability density / Poynting conservation (Mohr Eq. 55) | ✅ done | `ca_maxwell.py::composite_photon_energy_conservation` (L359–395) | Tier 2 #7 |
| **C5** | Angular-momentum eigenstates via matrix spherical harmonics (Mohr §8, Eqs. 391–393) | 🟡 building | this build | (new — pending) |
| **C6** | Source coupling and Maxwell Green function (Mohr Eqs. 57–58, source term $\Xi$) | 🟡 building | this build | (new — pending) |

Baseline regression confirmed 2026-05-21 - 19:42 — all C1–C4 tests pass at machine precision (transversality $1.6 \times 10^{-16}$, orthonormality $5.5 \times 10^{-16}$, completeness $4.4 \times 10^{-16}$, Poynting drift $4.5 \times 10^{-14}$ over 200 steps, boost-covariance components $\le 1.3 \times 10^{-15}$, longitudinal-mode residuals $\le 1.1 \times 10^{-16}$).

---

## C5 — Photon angular-momentum eigenstates: build spec

### Mathematical object

The vector spherical harmonic (VSH) couples scalar spherical harmonic $Y_{l m_l}(\hat{\boldsymbol{n}})$ with spin-1 unit vectors $\hat{\boldsymbol{e}}_{m_s}$ via Clebsch–Gordan coupling to total angular momentum $(j, m)$:

$$
\mathbf{Y}^m_{jl}(\hat{\boldsymbol{n}}) \;\equiv\; \sum_{m_l = -l}^{l}\sum_{m_s = -1}^{1} C^{j\,m}_{l\,m_l,\,1\,m_s}\, Y_{l\,m_l}(\hat{\boldsymbol{n}})\, \hat{\boldsymbol{e}}_{m_s}.
$$

Allowed orbital quantum numbers are $l \in \{j-1,\, j,\, j+1\}$. For $j \ge 1$, $l = j$ is the *magnetic-multipole* VSH; $l = j \pm 1$ combine to give *electric-multipole* and *longitudinal* photon states.

### Properties to verify

$$
\mathcal{J}^2\, \mathbf{Y}^m_{jl} = j(j+1)\, \mathbf{Y}^m_{jl}, \qquad
\mathcal{J}_z\, \mathbf{Y}^m_{jl} = m\, \mathbf{Y}^m_{jl},
$$
$$
\int \mathbf{Y}^{m\,\dagger}_{j\,l}(\hat{\boldsymbol{n}})\, \mathbf{Y}^{m'}_{j'\,l'}(\hat{\boldsymbol{n}})\, d\Omega \;=\; \delta_{jj'}\,\delta_{mm'}\,\delta_{ll'}.
$$

For physical transverse photons, the eigenstate combines $l = j \pm 1$ such that $\hat{\boldsymbol{k}}_s^\dagger \mathbf{Y}^m_{j,\text{E}} = 0$.

### Functions to add to `ca_maxwell.py`

1. `_clebsch_gordan(j1, m1, j2, m2, j, m)` — sympy-backed CG coefficient, `lru_cache`'d.
2. `_scalar_sph_harm(l, m, theta, phi)` — standard $Y_{l m}(\theta, \phi)$ in numpy.
3. `vector_spherical_harmonic(j, m, l, theta, phi)` — returns 3-vector in spherical basis (Mohr's $\hat{\boldsymbol{e}}_{m_s}$ basis is exactly the spherical-basis unit vectors $\hat{\boldsymbol{e}}^s_{m_s}$).
4. `photon_ang_mom_eigenstate(j, m, kappa, theta, phi)` — wraps the VSH into the 6-component photon spinor $(\mathbf{Y}, \tau\cdot\hat{\boldsymbol{k}}\,\mathbf{Y})^T$ for $\kappa = +$ (positive energy).
5. `test_vsh_orthonormality(j_max=2, n_theta=20, n_phi=20)` — Gauss-Legendre × uniform quadrature of the $L^2$ orthonormality identity.
6. `test_vsh_eigenvalues(j_max=2, n_dirs=8)` — apply $\mathcal{J}_z = L_z + S_z$ as the differential operator $-i\partial_\phi I + S_z$ via finite difference on $\phi$, check eigenvalue is $m$ to FFT precision. ($\mathcal{J}^2$ check via numerical second-derivative.)

### Acceptance tier

- **Tier 1 algebraic identity** for orthonormality: residual / (4π × ε) < 1 on quadrature exact for polynomials up to $2l_\text{max}+1$ in $\cos\theta$.
- **Machine precision** for the eigenvalue checks (finite-difference floor).

---

## C6 — Source coupling and Maxwell Green function: build spec

### Mathematical objects

Mohr's source term (paraphrased from §C6, Eqs. 57–58):
$$
\Xi(x) \;=\; (-\mu_0 c\, \mathbf{J}_s(x),\ \mathbf{0})^T,
$$
where $\mathbf{J}_s$ is the current 3-vector in the spherical basis. The Maxwell equation is then $i\partial_t \Psi = H\Psi + \Xi$.

Free-space retarded Green function in momentum space:
$$
G(\omega, \boldsymbol{k}) \;=\; (H(\boldsymbol{k}) - \omega - i\epsilon)^{-1}, \qquad H(\boldsymbol{k}) = c\, \alpha\cdot\boldsymbol{k},
$$
with $\alpha = \begin{pmatrix} 0 & \tau\cdot\hat{\boldsymbol{k}} \\ \tau\cdot\hat{\boldsymbol{k}} & 0 \end{pmatrix}$ (Mohr §4).

Dirac current (sourcing the photon field):
$$
J^\mu(x) \;=\; \bar\psi(x)\, \gamma^\mu\, \psi(x), \qquad \partial_\mu J^\mu = 0.
$$

### Functions to add to `ca_maxwell.py`

1. `maxwell_hamiltonian_k(k_c)` — 6×6 matrix $H(\boldsymbol{k}) = c\,\alpha\cdot\boldsymbol{k}$.
2. `maxwell_green_function_k(omega, k_c, eps=1e-9)` — $(H(\boldsymbol{k}) - \omega - i\epsilon)^{-1}$, complex 6×6.
3. `dirac_current_4momentum(psi)` — given a 4-component Dirac spinor at fixed $k$, return $J^\mu \in \mathbb{R}^4$ (Cartesian).
4. `maxwell_source_term(J_c)` — convert Cartesian $\mathbf{J}$ to Mohr's 6-component $\Xi$.
5. `test_green_function_inverse(n_dirs=8, omega_factor=0.5)` — at $\omega = (\text{omega\_factor}) \cdot c\,|k|$, verify $(H - \omega) \cdot G(\omega, k) = I$ to machine precision (avoiding the on-shell pole at $\omega = \pm c|k|$).
6. `test_current_conservation(k_mag=0.3, n_dirs=8)` — for Dirac plane-wave eigenstates, verify $k_\mu J^\mu = 0$ to FFT precision.

### Acceptance tier

- **Tier 1 algebraic identity** for Green-function inverse at off-shell $\omega$ (residual is the linear-algebra round-off floor on a 6×6 inversion).
- **Machine precision** for current conservation $k_\mu J^\mu$ on Dirac eigenstates (FFT round-off after the bilinear product).

---

## Out of scope for this build (deferred)

- The Mohr §C6 *practical* application: computing the radiation field from a localized Dirac current via the Green function. This requires a coupled-sector run and is parked under "future Phase G" in the Mohr summary. The C6 build below establishes the *primitives* (Green function + source term + current) without yet exercising the coupled radiation calculation.
- The §C5 *radial* wave-function coefficients of Mohr Eqs. 391–393 — i.e. the energy eigenstates that combine VSHs with spherical Bessel functions. The angular part is built here; the radial part is deferred until needed for an atomic transition matrix element.

---

## Run order

1. Edit `ca_maxwell.py` — add C5 then C6 functions and their main-block test invocations.
2. Run `python3 ca_maxwell.py` end-to-end; capture stdout to `test-results/mohr_c5_c6_results.md`.
3. Inspect residuals; promote any that hit the acceptance tier into `exactness-inventory.md`.
4. If all pass, write a Findings entry summarizing the additions. If anything fails, do not promote — record the failure mode in this doc.

---

## Cross-references

- Source: [`reference-research/mohr-2010-maxwell-photon-wf-summary.md`](reference-research/mohr-2010-maxwell-photon-wf-summary.md) §C
- Code: [`ca-simulation/ca_maxwell.py`](ca-simulation/ca_maxwell.py)
- Inventory: [`exactness-inventory.md`](exactness-inventory.md) Tier 1 #22–30 and Tier 2 #7
- Companion build: composite-photon framework (Paper 1 Eq. 35)
