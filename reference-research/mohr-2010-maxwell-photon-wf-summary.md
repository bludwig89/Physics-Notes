# Summary: "Solutions of the Maxwell Equations and Photon Wave Functions"
### Peter J. Mohr — *Annals of Physics* **325**, 607–663 (2010)

*Summarized: 2026-05-20 - 14:00*

---

## 1. Core Thesis

Mohr constructs a complete quantum-mechanical formalism for photon wave functions by direct analogy with the Dirac equation. The key move is replacing the Dirac 2×2 Pauli spin matrices $\sigma^i$ with the 3×3 spin-1 tau matrices $\tau^i$, producing a six-component wave equation for the combined electric and magnetic field:

$$\Psi(x) = \begin{pmatrix} \boldsymbol{E}_s(x) \\ ic\boldsymbol{B}_s(x) \end{pmatrix}, \qquad \gamma^\mu \partial_\mu \Psi(x) = \Xi(x), \tag{52}$$

where $\Xi(x) = (-\mu_0 c \boldsymbol{J}_s(x),\ \boldsymbol{0})^T$ is the source term, and the 6×6 gamma matrices are:

$$\gamma^0 = \begin{pmatrix} \boldsymbol{I} & \boldsymbol{0} \\ \boldsymbol{0} & -\boldsymbol{I} \end{pmatrix}, \quad \gamma^i = \begin{pmatrix} \boldsymbol{0} & \tau^i \\ -\tau^i & \boldsymbol{0} \end{pmatrix}, \quad i = 1,2,3. \tag{46}$$

This simultaneously encodes both curl Maxwell equations ($\nabla \times \boldsymbol{B} = \ldots$ and $\nabla \times \boldsymbol{E} = \ldots$) as a single first-order matrix equation.

---

## 2. Three-Component Spin Matrices (Section 3)

The tau matrices are the $j=1$ (spin-1) analog of the Pauli matrices, satisfying the same commutation relations $[\tau^i, \tau^j] = i\epsilon_{ijk}\tau^k$. In spherical basis:

$$\tau^3 = \begin{pmatrix} 1&0&0\\0&0&0\\0&0&-1 \end{pmatrix}, \quad \tau^1 = \frac{1}{\sqrt{2}}\begin{pmatrix}0&1&0\\1&0&1\\0&1&0\end{pmatrix}, \quad \tau^2 = \frac{i}{\sqrt{2}}\begin{pmatrix}0&-1&0\\1&0&-1\\0&1&0\end{pmatrix}. \tag{15–17}$$

The Cartesian tau matrices $\tilde{\tau}^i = -iM^\dagger \tau^i M$ are antisymmetric ($\tilde{\tau}^\top = -\tilde{\tau}$) and satisfy:

$$\tilde{\tau}^i{}_{jk} = -\epsilon_{ijk}, \qquad (\tilde{\tau}\cdot\boldsymbol{a})^{ij} = -\epsilon_{ijk} a^k, \tag{37}$$

so $\tilde{\tau}\cdot\boldsymbol{a}$ is the cross-product matrix, i.e., $(\tilde{\tau}\cdot\boldsymbol{a})\boldsymbol{b}_c = (\boldsymbol{a}\times\boldsymbol{b})_c$.

Key identity used throughout:

$$(\boldsymbol{\tau}\cdot\boldsymbol{a})^\dagger \boldsymbol{\tau}\cdot\boldsymbol{b} = \boldsymbol{a}\cdot\boldsymbol{b} - \boldsymbol{b}_s \boldsymbol{a}_s^\dagger. \tag{30}$$

---

## 3. Matrix Maxwell Equation (Section 4)

In source-free form, the Maxwell equations factor into two uncoupled sectors:

$$\left(\boldsymbol{I}\frac{\partial}{\partial ct} + \boldsymbol{\tau}\cdot\nabla\right)(\boldsymbol{E}_s + ic\boldsymbol{B}_s) = 0, \tag{41}$$
$$\left(\boldsymbol{I}\frac{\partial}{\partial ct} - \boldsymbol{\tau}\cdot\nabla\right)(\boldsymbol{E}_s - ic\boldsymbol{B}_s) = 0. \tag{42}$$

These are the Maxwell analogs of the Weyl equations for right- and left-circularly polarized radiation. The full six-component equation (Eq. 52) is the spin-1 Dirac-form equation that applies for any polarization simultaneously. The energy-momentum density follows from:

$$\bar{\Psi}cp^0\Psi = \frac{1}{2}\!\left(\epsilon_0|\boldsymbol{E}|^2 + \frac{1}{\mu_0}|\boldsymbol{B}|^2\right) = u, \tag{55}$$
$$\bar{\Psi}\boldsymbol{p}\Psi = \frac{1}{c^2\mu_0}\operatorname{Re}\boldsymbol{E}\times\boldsymbol{B}^* = \boldsymbol{g}, \tag{56}$$

reproducing the Poynting theorem and electromagnetic energy density exactly.

---

## 4. Transverse and Longitudinal Decomposition (Section 5)

Hermitian projection operators are defined on the spherical-basis fields:

$$\boldsymbol{\Pi}^T_s(\boldsymbol{a}) = \frac{(\boldsymbol{\tau}\cdot\boldsymbol{a})^\dagger(\boldsymbol{\tau}\cdot\boldsymbol{a})}{\boldsymbol{a}\cdot\boldsymbol{a}}, \qquad \boldsymbol{\Pi}^L_s(\boldsymbol{a}) = \frac{\boldsymbol{a}_s \boldsymbol{a}_s^\dagger}{\boldsymbol{a}\cdot\boldsymbol{a}}. \tag{60–61}$$

In differential form with $\boldsymbol{a} \to \nabla$:

$$\boldsymbol{\Pi}^T_s(\nabla) = \frac{(\boldsymbol{\tau}\cdot\nabla)^2}{\nabla^2}, \qquad \boldsymbol{\Pi}^L_s(\nabla) = \frac{\nabla_s\nabla_s^\dagger}{\nabla^2}. \tag{70–71}$$

Key properties: $[\boldsymbol{\Pi}^T]^2 = \boldsymbol{\Pi}^T$, $\boldsymbol{\Pi}^T + \boldsymbol{\Pi}^L = I$, $\boldsymbol{\Pi}^T \boldsymbol{\Pi}^L = 0$, and $\boldsymbol{\Pi}^T_s \boldsymbol{a}_s = 0$ (Eq. 66 — the longitudinal direction is killed by the transverse projector). The Maxwell equations separate cleanly into decoupled transverse and longitudinal sectors, with $\boldsymbol{B}^L_s = 0$ eliminating the longitudinal magnetic sector.

---

## 5. Lorentz Invariance (Section 6)

The six-component equation is Lorentz invariant. The field transformation under a velocity boost $\boldsymbol{v} = c\tanh\zeta\,\hat{\boldsymbol{v}}$ is:

$$\mathcal{V}(\boldsymbol{v}) = e^{\zeta\mathcal{K}\cdot\hat{v}}, \qquad \mathcal{K} = \begin{pmatrix}\boldsymbol{0} & \boldsymbol{\tau} \\ \boldsymbol{\tau} & \boldsymbol{0}\end{pmatrix}, \tag{169–170}$$

which expands to:

$$\mathcal{V}(\boldsymbol{v})\Psi = \begin{pmatrix}\boldsymbol{E}_s + (\boldsymbol{\tau}\cdot\hat{\boldsymbol{v}})^2\boldsymbol{E}_s(\cosh\zeta-1) + i\boldsymbol{\tau}\cdot\hat{\boldsymbol{v}}\,c\boldsymbol{B}_s\sinh\zeta \\ i[c\boldsymbol{B}_s + (\boldsymbol{\tau}\cdot\hat{\boldsymbol{v}})^2 c\boldsymbol{B}_s(\cosh\zeta-1) - i\boldsymbol{\tau}\cdot\hat{\boldsymbol{v}}\,\boldsymbol{E}_s\sinh\zeta]\end{pmatrix}. \tag{172}$$

Under rotations, the six-component rotation operator is $\mathcal{R}(\boldsymbol{u}) = e^{-i\boldsymbol{\mathcal{S}}\cdot\boldsymbol{u}}$ with $\mathcal{S} = \operatorname{diag}(\boldsymbol{\tau}, \boldsymbol{\tau})$. Parity and time-reversal matrices are:

$$\mathcal{P} = \pm\begin{pmatrix}\boldsymbol{I} & \boldsymbol{0} \\ \boldsymbol{0} & -\boldsymbol{I}\end{pmatrix}, \qquad \mathcal{T} = \begin{pmatrix}\boldsymbol{I} & \boldsymbol{0} \\ \boldsymbol{0} & -\boldsymbol{I}\end{pmatrix}. \tag{191, 200}$$

Crucially: two Lorentz invariants are identified,

$$\bar{\Psi}\Psi = |\boldsymbol{E}|^2 - c^2|\boldsymbol{B}|^2, \qquad \bar{\Psi}\eta\Psi = 2ic\operatorname{Re}\boldsymbol{E}\cdot\boldsymbol{B}. \tag{181–182}$$

---

## 6. Plane-Wave Eigenfunctions (Section 7)

The Hamiltonian is $\mathcal{H} = c\boldsymbol{\alpha}\cdot\boldsymbol{p} = -i\hbar c\boldsymbol{\alpha}\cdot\nabla$ with $\alpha^i = \gamma^0\gamma^i$.

**Transverse wave functions** ($\lambda = 1, 2$, polarization vectors $\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}})$ perpendicular to $\hat{\boldsymbol{k}}$):

$$\psi^{(\pm)}_{\boldsymbol{k},\lambda}(\boldsymbol{x}) = \frac{1}{\sqrt{2(2\pi)^3}} \begin{pmatrix} \hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}}) \\ \boldsymbol{\tau}\cdot\hat{\boldsymbol{k}}\,\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}}) \end{pmatrix} e^{\pm i\boldsymbol{k}\cdot\boldsymbol{x}}, \qquad \mathcal{H}\psi^{(\pm)}_{\boldsymbol{k},\lambda} = \pm\hbar c|\boldsymbol{k}|\,\psi^{(\pm)}_{\boldsymbol{k},\lambda}. \tag{217, 222}$$

**Longitudinal wave functions** ($\lambda = 0$, $\hat{\boldsymbol{\epsilon}}_0(\hat{\boldsymbol{k}}) = \hat{\boldsymbol{k}}_s$):

$$\psi^{(+)}_{\boldsymbol{k},0}(\boldsymbol{x}) = \frac{1}{\sqrt{(2\pi)^3}}\begin{pmatrix}\hat{\boldsymbol{\epsilon}}_0(\hat{\boldsymbol{k}})\\\boldsymbol{0}\end{pmatrix}e^{i\boldsymbol{k}\cdot\boldsymbol{x}}, \qquad \mathcal{H}\psi^{(\pm)}_{\boldsymbol{k},0} = 0. \tag{237, 241}$$

Longitudinal photons carry zero energy — they represent Coulomb-gauge fields ($\boldsymbol{E}$ of a static charge). Dispersion for transverse photons:

$$\omega = c|\boldsymbol{k}| \quad (\text{transverse}), \qquad \omega = 0 \quad (\text{longitudinal}). \tag{253–254}$$

**Completeness** (transverse + longitudinal):

$$\sum_{\kappa=\pm}\sum_{\lambda=0}^2 \int d\boldsymbol{k}\;\psi^{(\kappa)}_{\boldsymbol{k},\lambda}(\boldsymbol{x}_2)\psi^{(\kappa)\dagger}_{\boldsymbol{k},\lambda}(\boldsymbol{x}_1) = \mathcal{I}\,\delta(\boldsymbol{x}_2-\boldsymbol{x}_1). \tag{250}$$

Orthogonality of transverse polarization vectors:

$$\sum_{\lambda=1}^2 \hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}})\hat{\boldsymbol{\epsilon}}_\lambda^\dagger(\hat{\boldsymbol{k}}) = \boldsymbol{I} - \hat{\boldsymbol{k}}_s\hat{\boldsymbol{k}}_s^\dagger = (\boldsymbol{\tau}\cdot\hat{\boldsymbol{k}})^2 = \boldsymbol{\Pi}^T_s(\hat{\boldsymbol{k}}). \tag{213}$$

**Velocity transformation of transverse wave functions** (boost by $\boldsymbol{v}$):

$$\mathcal{V}(\boldsymbol{v})\psi^{(\kappa)}_{\boldsymbol{k},\lambda}(V^{-1}(\boldsymbol{v})x) = \xi\,\psi^{(\kappa)}_{\boldsymbol{k}',\lambda}(x), \qquad \xi = \cosh\zeta + \hat{\boldsymbol{v}}\cdot\hat{\boldsymbol{k}}\sinh\zeta. \tag{281, 287}$$

The boosted transverse wave function is still transverse (polarization is preserved), unlike the vector potential which requires a gauge transformation after a boost.

**Wave packet** (normalized Gaussian, $\boldsymbol{k}_0$ along $\hat{\boldsymbol{k}}_0$, widths $a$ and $b$):

$$\Psi_f(\boldsymbol{x}) = \frac{1}{a^{\frac{1}{2}}b}\left(\frac{2}{\pi^3}\right)^{\frac{1}{4}}\begin{pmatrix}\hat{\boldsymbol{\epsilon}}_1(\hat{\boldsymbol{k}}_0) \\ \boldsymbol{\tau}\cdot\hat{\boldsymbol{k}}_0\,\hat{\boldsymbol{\epsilon}}_1(\hat{\boldsymbol{k}}_0)\end{pmatrix} e^{-i(\omega_0 t - \boldsymbol{k}_0\cdot\boldsymbol{x})} e^{-(ct - \hat{\boldsymbol{k}}_0\cdot\boldsymbol{x})^2/a^2 - x_\perp^2/b^2}. \tag{366}$$

Probability density $Q(\boldsymbol{x}) = \Psi_f^\dagger \Psi_f$, flux $\boldsymbol{q}(\boldsymbol{x}) = \hat{\boldsymbol{k}}_0 Q^0(\boldsymbol{x})$ — the packet moves with velocity $c$ in the $\hat{\boldsymbol{k}}_0$ direction.

---

## 7. Angular Momentum Eigenfunctions (Section 8)

Total angular momentum: $\mathcal{J} = \boldsymbol{x}\times\mathcal{P} + \hbar\mathcal{S}$ with $[\mathcal{H}, \mathcal{J}] = 0$.

Matrix spherical harmonics constructed by Clebsch-Gordan coupling of orbital $L$ and spin-1 $\boldsymbol{\tau}$:

$$\boldsymbol{Y}^m_{jl}(\hat{\boldsymbol{x}}) = \sum_\nu (l\,1\,m{-}\nu\,1\,\nu | l\,1\,j\,m) Y^{m-\nu}_l(\hat{\boldsymbol{x}})\,\hat{\boldsymbol{\epsilon}}^{(\nu)}, \tag{386}$$

with three families: $l = j$ (electric-type), $l = j+1$ (magnetic-type), $l = j-1$. Alternative set:

$$\boldsymbol{X}_1^{jm} = \boldsymbol{Y}^m_{jj}, \quad \boldsymbol{X}_2^{jm} = \frac{1}{\hbar\sqrt{j(j+1)}}\boldsymbol{\tau}\cdot\boldsymbol{x}\,\boldsymbol{L}_s Y^m_j, \quad \boldsymbol{X}_3^{jm} = \hat{\boldsymbol{x}}_s Y^m_j. \tag{402–404}$$

---

## 8. Maxwell Green Function (Section 9, inferred)

The Green function is constructed from the complete set of plane-wave solutions:

$$G(x_2 - x_1) = \sum_{\kappa,\lambda} \int d\boldsymbol{k}\;\psi^{(\kappa)}_{\boldsymbol{k},\lambda}(\boldsymbol{x}_2)\psi^{(\kappa)\dagger}_{\boldsymbol{k},\lambda}(\boldsymbol{x}_1)\,e^{-i\kappa\omega(t_2-t_1)},$$

and takes the same covariant form as the Dirac Green function. Applications include dipole radiation from an oscillating source and radiation from an atomic transition current.

---

## 9. Key Requirements Satisfied

Mohr establishes that the six-component photon wave function satisfies all required quantum-mechanical properties:

| Property | Result |
|---|---|
| Solutions of first-order Maxwell equations | ✓ by construction |
| Linear superposition | ✓ (linear equation) |
| Lorentz invariant | ✓ proved in §6 |
| Hamiltonian with complete eigenfunctions | ✓ §7–8 |
| Normalizable wave packets | ✓ Eq. (352) |
| Conservation of probability | ✓ Poynting theorem (§7.9) |
| Transversality preserved under boosts | ✓ §7.6 (unlike vector potential) |
| Angular momentum eigenstates | ✓ §8 |
| Green function | ✓ §9 |

---

---

# Comparison with Current Wave Function Implementation

*2026-05-20 - 14:00*

---

## A. Structural Correspondence

Our project implements photons as composite bilinears of two Weyl QCA spinors (Bisio et al. 2015 Paper 1, Eq. 35):

$$G^i(\boldsymbol{k}) = \phi^T(\boldsymbol{k}/2)\,\sigma^i\,\psi(\boldsymbol{k}/2), \quad E_G = |n_{k/2}|(G_T + G_T^\dagger), \quad B_G = i|n_{k/2}|(G_T^\dagger - G_T).$$

Mohr's wave function is:

$$\Psi = \begin{pmatrix}\boldsymbol{E}_s \\ ic\boldsymbol{B}_s\end{pmatrix}.$$

These are the **same six-component object** — upper 3 = $\boldsymbol{E}$ field, lower 3 = $ic\boldsymbol{B}$ field — but derived from fundamentally different starting points. Mohr takes the EM fields as primitive and writes the wave function directly. We derive them as bilinears from more fundamental Weyl spinors. The outputs $E_G, B_G$ from `ca_maxwell.py` are exactly the upper and lower three components of Mohr's $\Psi$.

The key structural difference: Mohr uses 3×3 tau matrices (spin-1); our Weyl building blocks use 2×2 Pauli matrices (spin-1/2). The spin-1 character of the photon emerges in our model from the **bilinear product** $\phi^T\sigma^i\psi$ (two spin-1/2 objects combining into spin-1), while in Mohr it is fundamental.

---

## B. What Our Code Already Implements Correctly

| Mohr concept | Our implementation | Status |
|---|---|---|
| Transverse projector $\Pi^T_s(\nabla)$ | `_transverse_part` in `ca_maxwell.py` | ✓ correct (residual 4.58e-17) |
| Dispersion $\omega_\gamma = c\|k\|$ | `maxwell_dispersion_residual` | ✓ exact algebraic $\|k\|/\sqrt{d}$ |
| $\boldsymbol{k}\cdot\boldsymbol{E}_G = 0$, $\boldsymbol{k}\cdot\boldsymbol{B}_G = 0$ | `maxwell_transversality` | ✓ passes |
| Free Maxwell curl equations $\partial_t E = i\boldsymbol{n}\times B$ | `maxwell_curl_residual` | ✓ passes at small $k$ |
| Helicity decomposition $\psi = (\boldsymbol{E}\pm ic\boldsymbol{B})$ | Eigenmodes via `weyl_eigenmodes_3d_bcc` | ✓ implicit |
| Probability conservation (norm) | Weyl QCA unitarity | ✓ machine-ε |

---

## C. Gaps — What Mohr Has That We Do Not

### C1. Explicit Normalized Polarization Eigenstates

Mohr provides normalized plane-wave eigenfunctions (Eq. 217) with factor $1/\sqrt{2(2\pi)^3}$ and two explicit polarization vectors $\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}})$ for arbitrary $\hat{\boldsymbol{k}}$.

Our code samples random directions for testing, but never constructs an explicit, labeled polarization basis $(\hat{\boldsymbol{\epsilon}}_1, \hat{\boldsymbol{\epsilon}}_2)$ perpendicular to $\hat{\boldsymbol{k}}$. We use the Weyl eigenvectors as a proxy. This matters for:
- Correctly identifying helicity $\lambda = \pm 1$ (circular polarization) states
- Projecting wave packets onto definite polarization

**Improvement:** Add a function `polarization_basis(khat)` returning $\hat{\boldsymbol{\epsilon}}_1, \hat{\boldsymbol{\epsilon}}_2$ in the spherical basis, following Mohr Eqs. (210)–(216). For $\boldsymbol{k}$ in the $\hat{e}^3$ direction these are explicitly (Eq. 215–216):

$$\hat{\boldsymbol{\epsilon}}_1(\hat{e}^3) = \frac{1}{\sqrt{2}}\begin{pmatrix}-1\\0\\1\end{pmatrix}_s, \quad \hat{\boldsymbol{\epsilon}}_2(\hat{e}^3) = \frac{i}{\sqrt{2}}\begin{pmatrix}1\\0\\1\end{pmatrix}_s \quad \text{(linear)};$$
$$\hat{\boldsymbol{\epsilon}}_1(\hat{e}^3) = \begin{pmatrix}1\\0\\0\end{pmatrix}, \quad \hat{\boldsymbol{\epsilon}}_2(\hat{e}^3) = \begin{pmatrix}0\\0\\1\end{pmatrix} \quad \text{(circular, Eq. 216).}$$

For general $\hat{\boldsymbol{k}}$, rotate these using $\boldsymbol{R}_s(\boldsymbol{u})$ per Mohr Eq. (264): $\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}}') = \boldsymbol{R}_s(\boldsymbol{u})\hat{\boldsymbol{\epsilon}}_\lambda(\hat{\boldsymbol{k}})$.

### C2. Longitudinal (λ=0) Photon Mode

Mohr explicitly includes longitudinal photon states with $\omega = 0$ and polarization $\hat{\boldsymbol{\epsilon}}_0 = \hat{\boldsymbol{k}}_s$ (Eq. 235). These represent the static Coulomb field of a charge and are needed for the full completeness relation (Eq. 250).

Our `ca_maxwell.py` only tests transverse modes. There is no longitudinal mode in the BCC bilinear construction. This is physically correct for free photons but means our completeness relation is only the transverse part (Eq. 231), not the full electromagnetic Hilbert space.

**Improvement:** Add a `longitudinal_mode(khat)` function returning $\psi^{(+)}_{\boldsymbol{k},0} = (\hat{\boldsymbol{k}}_s, \boldsymbol{0})^T / \sqrt{(2\pi)^3}$ and verify it is orthogonal to the bilinear transverse states. This is needed if we ever want to represent static field configurations or source-coupled photons.

### C3. Lorentz Boost Behavior of $E_G, B_G$

Mohr proves (§7.6) that under a velocity boost, the transverse photon wave function transforms as $\mathcal{V}(\boldsymbol{v})\psi^{(\kappa)}_{\boldsymbol{k},\lambda} = \xi\,\psi^{(\kappa)}_{\boldsymbol{k}',\lambda}$ with $\xi = \cosh\zeta + \hat{\boldsymbol{v}}\cdot\hat{\boldsymbol{k}}\sinh\zeta$, and crucially the boosted wave function remains **transverse** (Eq. 284).

We have never tested whether our bilinear construction $E_G, B_G$ at boosted momenta equals the Lorentz-transformed field from the rest-frame bilinear. This would be a test of Lorentz covariance at the composite-photon level.

**Improvement:** Implement a test: compute $E_G, B_G$ at momentum $\boldsymbol{k}$; boost the wave function using Mohr's $\mathcal{V}(\boldsymbol{v})$ matrix (Eq. 171); compute $E_G, B_G$ at momentum $\boldsymbol{k}' = V(\boldsymbol{v})\boldsymbol{k}$; verify they agree to machine precision.

### C4. Probability Density and Poynting Vector Identification ✓ **CLOSED 2026-05-21**

Mohr identifies $Q(\boldsymbol{x}) = \Psi^\dagger\Psi = \epsilon_0|\boldsymbol{E}|^2 + \frac{1}{\mu_0 c^2}|\boldsymbol{B}|^2$ (up to factors) and $\boldsymbol{q}(\boldsymbol{x}) = \boldsymbol{S}/c^2$ (Poynting vector) as the probability four-current. The conserved probability density is $q^0 = \bar{\Psi}\gamma^0\Psi$.

**Result (Finding 17):** $\|E_G(t)\|^2 + c^2\|B_G(t)\|^2$ is conserved at machine precision under composite-photon propagation. Measured max relative deviation $4.77\times 10^{-14}$ over 200 steps; per-step rate $1.4\times 10^{-16}\approx\varepsilon_\text{machine}$. The conservation is algebraically exact and **c-independent**: the BCC bilinear $G_T = \psi_+^T\sigma\psi_+$ produces a circularly polarized field ($\boldsymbol A\cdot\boldsymbol C=0$, $\|\boldsymbol A\|^2=\|\boldsymbol C\|^2$) which is the condition for the $c^2$-weighted energy to be invariant under the phase rotation $G_T\to e^{-i\Omega}G_T$ for any $c$.

**Test function:** `ca_maxwell.composite_photon_energy_conservation_c2()`. Added as Exactness Inventory Tier 1 #44 and Tier 2 #10.

### C5. Angular Momentum Eigenstates

Mohr constructs angular-momentum eigenstates via matrix spherical harmonics $\boldsymbol{Y}^m_{jl}$ (Section 8), which are eigenstates of $\mathcal{J}^2$ and $\mathcal{J}^3$ with $j = 1/2, 3/2, \ldots$ for the spin-1 photon.

**We have no angular momentum eigenstates whatsoever for the photon.** The plane-wave basis used in `ca_maxwell.py` is an eigenstate of momentum, not angular momentum. This is a complete gap — and it's the basis for all radiation multipole expansions (E1, M1, E2, etc.).

**Improvement (longer term):** Add `photon_ang_mom_eigenstate(j, m, l, r, energy='+')` that returns the radial wave function coefficients for the angular-momentum eigenstates following Mohr Eqs. (391)–(393). Priority: needed if we ever want to compute atomic transition matrix elements or radiation patterns.

### C6. Source Coupling and Green Function

Mohr derives the Poynting theorem with sources (Eq. 57–58), the source-term $\Xi(x) = (-\mu_0 c\boldsymbol{J}_s, \boldsymbol{0})^T$, and the Maxwell Green function. This enables computing radiation from a current source without having to solve the coupled Maxwell equations from scratch.

Our composite-photon construction is entirely source-free. There is no mechanism in `ca_maxwell.py` to couple the photon bilinear to a current $\boldsymbol{J}$.

**Improvement (longer term):** The Green function approach would let us compute the radiation field from, e.g., the Dirac current $J^\mu = \bar{\psi}\gamma^\mu\psi$ in `ca_dirac.py`, connecting the Maxwell and Dirac sectors. This is a natural target for a future Phase G test.

---

## D. Possible Immediate Improvements to Current Code

Priority-ordered improvements that are concretely implementable:

| Priority | Improvement | Effort | Impact |
|---|---|---|---|
| **High** | Add `polarization_basis(khat)` returning $\hat{\boldsymbol{\epsilon}}_{1,2}(\hat{\boldsymbol{k}})$ in spherical basis | Low | Fixes implicit polarization; enables helicity tests |
| ~~**High**~~ **DONE** | ~~Test Poynting energy conservation of the $E_G, B_G$ bilinear~~ | ~~Low~~ | Closed: Finding 17, Exactness Inventory Tier 1 #44 + Tier 2 #10 (2026-05-21) |
| **Medium** | Add Lorentz boost covariance test using Mohr's $\mathcal{V}(\boldsymbol{v})$ | Medium | Validates the composite photon is truly Lorentz-covariant |
| **Medium** | Add longitudinal ($\lambda=0$) mode and verify orthogonality | Medium | Completes the photon Hilbert space |
| **Low** | Angular momentum eigenstates via matrix spherical harmonics | High | Opens multipole radiation calculations |
| **Low** | Green function construction for source-coupled radiation | High | Enables Dirac↔Maxwell coupling |

---

## E. What Mohr Does NOT Have That We Do

Our bilinear construction has several features Mohr's framework lacks:

- **Lattice-exact dispersion**: our photon dispersion $\omega = |k|/\sqrt{d}$ is an exact algebraic result of the BCC QCA structure, not a continuum approximation.
- **Composite structure**: our $G^i = \phi^T\sigma^i\psi$ derives photons from Weyl spinors, implementing the De Broglie neutrino-theory-of-light at the QCA level. Mohr treats $\boldsymbol{E}, \boldsymbol{B}$ as primitive.
- **Unitarity by construction**: the BCC Weyl propagator is exactly unitary for all $k$, guaranteeing exact norm conservation and time-reversibility without any CFL constraint.
- **Connection to the Weyl/Dirac sector**: our composite photon shares the same lattice and propagator as the Dirac field, making Yukawa-type coupling (F3) and eventual QED simulation natural.

Mohr's continuum formulation is agnostic about the microscopic origin of the photon and does not address whether the wave function is fundamental or composite.

---

## F. Summary Verdict

Mohr's paper is most directly useful to this project as a **reference for the structure our composite-photon wave function should reproduce in the continuum limit**. The six-component $\Psi = (E_G, icB_G)^T$ we construct is exactly the object Mohr analyzes, and our transversality, dispersion, and curl tests are verifying exactly the properties Mohr proves. The main actionable gaps are:

1. **Explicit polarization basis** — straightforward to add to `ca_maxwell.py`
2. **Poynting energy conservation test** — should be added to the exactness inventory
3. **Lorentz covariance test** — medium effort, high physics payoff
4. **Angular momentum eigenstates** — longer-term, needed for multipole radiation

The composite-photon approach (our model) and Mohr's direct approach are complementary, not competing. Mohr provides the continuum target; we provide the lattice-microscopic derivation.

---

*Added to `project-status.md` and `ca-reference.md`: 2026-05-20*
