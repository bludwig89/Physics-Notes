# Project Review — Physics Summary

*2026-05-22. All equations in Markdown math. This document compiles every physics framework, equation, and derivation used or referenced in the "universe in a bottle" lattice-CA project.*

---

## 1. Cellular Automaton Interpretation ('t Hooft CAI)

The foundation is Gerard 't Hooft's **Cellular Automaton Interpretation** (2015). The core claim: quantum mechanics is an emergent statistical description of an underlying deterministic cellular automaton. Every quantum state is a superposition of "ontological" basis states that the CA cycles through deterministically.

**CA evolution operator.** For a deterministic CA the time-step operator is a permutation matrix, so its eigenvalues are unimodular:

$$U_\text{op}(\delta t) = e^{-iH_\text{op}\,\delta t}, \qquad 0 \le H_\text{op} < 2\pi/\delta t.$$

The Hamiltonian $H_\text{op}$ is defined only **modulo $2\pi/\delta t$** — the branch-cut ambiguity 't Hooft calls one of three obstructions to using $H_\text{op}$ directly. The QCA arccos dispersion (§2 below) is the concrete resolution of this ambiguity for the class of propagators consistent with the five informational principles.

**Bekenstein / area law.** In the strong-gravity limit 't Hooft's CAI §9.4 argues that the degrees of freedom inside a region scale as its surface area $R^2$, not its volume $R^3$ (Bekenstein bound, $S = \pi R^2$). The lattice vacuum-freezing result (80% of cells at $N = 0$ in the T5.A test) provides a concrete finite-lattice analog of this: only cells reached by the propagating wavepacket carry non-zero tick counts.

---

## 2. Quantum Cellular Automata (QCA) — Weyl and Dirac

The primary physics engine is the QCA framework of Bisio, D'Ariano, Perinotti, and Tosini (Papers 1–4).

### 2.1 Informational uniqueness principle

Five axioms on the single-step propagator $U$ — **linearity, unitarity, locality, homogeneity, isotropy** — force the 3D lattice geometry to be the **body-centred cubic (BCC)** lattice. No other regular 3D lattice satisfies all five simultaneously.

### 2.2 Weyl QCA — massless

On the BCC lattice the unique massless (Weyl) propagator has the unitary matrix:

$$U(\mathbf{k}) = u\,I + i\,\tilde{\mathbf{n}}\cdot\boldsymbol{\sigma},$$

where $u \in \mathbb R$, $\tilde{\mathbf{n}} \in \mathbb R^3$, and the **unitarity constraint** is

$$u^2 + |\tilde{\mathbf{n}}|^2 = 1.$$

The BCC kernel (Paper 1 Eq. 15, sign-corrected in Finding 1) is:

$$u = c_x c_y c_z - s_x s_y s_z,$$
$$\tilde{n}_x = s_x c_y c_z + c_x s_y s_z, \quad \tilde{n}_y = c_x s_y c_z + s_x c_y s_z, \quad \tilde{n}_z = c_x c_y s_z + s_x s_y c_z,$$

with $c_i = \cos(k_i a)$, $s_i = \sin(k_i a)$, $a = 1/\sqrt{3}$ (the BCC lattice constant for unit speed of light).

**BCC dispersion relation.** Eigenvalues of $U(\mathbf{k})$ are $e^{\pm i\omega(\mathbf{k})}$, giving the exact dispersion

$$\omega(\mathbf{k}) = \arccos(u(\mathbf{k})).$$

Along the $(1,0,0)$ axis this reduces to the exact linear relation $\omega = k/\sqrt{3}$, confirming the lattice speed of light:

$$c_\text{lat} = \frac{1}{\sqrt{d}} \quad (d = \text{spatial dimension}).$$

For $d=3$: $c_\text{lat} = 1/\sqrt{3}$; for $d=2$: $c_\text{lat} = 1/\sqrt{2}$.

**2D-square dispersion.** For the 2D-square Weyl QCA (Paper 1 Eq. 16):

$$\omega(\mathbf{k}) = \arccos(\cos k_x \cos k_y).$$

### 2.3 Dirac QCA — massive

The massive Dirac 4-spinor is constructed by coupling two Weyl 2-spinors $\eta$ (left) and $\chi$ (right) through an off-diagonal mass term. The full propagator in momentum space is the $4\times4$ block matrix:

$$D(\mathbf{k}) = \begin{pmatrix} n\,U_k & im\,I \\ im\,I & n\,U_k^\dagger \end{pmatrix},$$

where $n = \sqrt{1-m^2}$ and $m \in [0,1]$ is the dimensionless mass. Unitarity of $D$ forces the off-diagonal block to be $im\,I$ exactly (not $im U_k^*$); in particular the lower-right block must be $U_k^\dagger$ (Hermitian conjugate, not element-wise conjugate).

**Dirac dispersion.** The exact-QCA Dirac dispersion on the 2D-square lattice:

$$\omega(\mathbf{k}) = \arccos\!\left(\sqrt{1-m^2}\,\cos k_x \cos k_y\right).$$

On the BCC in 3D:

$$\omega(\mathbf{k}) = \arccos\!\left(\sqrt{1-m^2}\,u_\text{BCC}(\mathbf{k})\right).$$

**Rest-frame energy / static mass.** At $\mathbf{k}=0$:

$$\omega_\text{static} = \arccos(\sqrt{1-m^2}) = \arcsin(m).$$

This is the lattice analog of $E_0 = mc^2$.

**Group velocity.** Along the $x$-axis at $k_y = 0$ (2D case):

$$v_g = \frac{\partial\omega}{\partial k} = \frac{\sqrt{1-m^2}\sin(ka)}{m + \text{(arccos denominator)}}.$$

At small $k$ this reduces to $v_g \approx (n/m)\,k + O(k^3)$, recovering the relativistic relation $v = p/E$.

### 2.4 Lattice speed of light — SI identification

Setting the lattice spacing $a = \ell_P$ (Planck length) and $\tau = t_P$ (Planck time) gives

$$c_\text{physical} = \frac{a}{\tau\sqrt{d}}.$$

This gives $c_\text{physical} = c/\sqrt{3}$ in 3D — off by $\sqrt{3}$ from the physical $c$. Three internally consistent resolutions have been identified (Finding 10) but the project has not committed to one.

### 2.5 Zitterbewegung

The mass term couples the $\eta$ and $\chi$ sectors with frequency $2\arcsin(m)$. The lattice correctly reproduces the zitterbewegung frequency at $\Delta\omega = 2\arcsin(m) = 2\omega_\text{static}$ (confirmed in D1 tests to 0.15%).

---

## 3. Special Relativity on the Lattice

### 3.1 Lorentz violation coefficients

The lattice SR-2 observable is the ratio $R(k) = \omega_\text{moving}/\omega_\text{static}$, compared to the continuum SR prediction $1/\gamma_\text{SR} = \sqrt{1-\beta^2}$, where $\beta = v_g/c_\text{lat}$. The departure is

$$R(\beta) - \frac{1}{\gamma_\text{SR}} = \beta_\text{LV}(m)\,\beta^2 + \gamma_\text{LV}(m)\,\beta^4 + \delta_\text{LV}(m)\,\beta^6 + \varepsilon_\text{LV}(m)\,\beta^8 + O(\beta^{10}).$$

The closed-form coefficients (Finding 15, all sympy-confirmed to bit-zero):

$$\boxed{\beta_\text{LV}(m) = \frac{1}{2}\!\left(1 - \frac{m}{\sqrt{1-m^2}\,\arcsin m}\right)}$$

$$\gamma_\text{LV}(m) = \frac{1}{8} - \frac{m(3-2m^2)}{24(1-m^2)^{3/2}\arcsin m}$$

$$\delta_\text{LV}(m) = \frac{1}{16} - \frac{m(8m^4-20m^2+15)}{240(1-m^2)^{5/2}\arcsin m}$$

$$\varepsilon_\text{LV}(m) = \frac{5}{128} - \frac{m(35-70m^2+56m^4-16m^6)}{896(1-m^2)^{7/2}\arcsin m}$$

**Key properties:**

- $\beta_\text{LV}(m) < 0$ for all $m \in (0,1)$ — the lattice **over-dilates** time relative to continuum SR.
- $\beta_\text{LV}(m) \to 0$ as $m \to 0$ — the Weyl (massless) sector is **exactly Lorentz-invariant** to this order.
- Small-mass expansion: $\beta_\text{LV}(m) = -m^2/6 - 11m^4/90 + O(m^6)$.
- The general LV tower coefficient follows the pattern: rational constant from SR expansion at $\beta^{2n}$, minus $m \cdot P_n(m) / [(2n)!! \cdot (1-m^2)^{(2n-1)/2} \cdot \arcsin m]$.

### 3.2 Deformed velocity addition (Finding 22)

The 4-momentum velocity $u_p = kc_\text{lat}^2/\omega$ and group velocity $u_g$ are related by

$$u_p = \rho(m)\,u_g, \qquad \rho(m) = \frac{m}{\sqrt{1-m^2}\,\arcsin m} = 1 - 2\beta_\text{LV}(m).$$

Since 4-momentum adds via standard SR, this gives the **closed-form deformed velocity-addition formula**:

$$u'_\text{QCA} = \frac{u_g + v_g}{1 + 2\rho^2(m)\,u_g v_g}$$

with deviation from SR:

$$\delta u' = \frac{2(1-\rho^2)\,u\,v\,(u+v)}{(1+2\rho^2 uv)(1+2uv)} \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v).$$

In the massless limit $\rho \to 1$, $\delta u' = 0$: standard SR velocity addition is recovered exactly.

### 3.3 Deformed special relativity (DSR)

From Paper 4 (Bisio et al.), the deformed Lorentz transformation is

$$L^\mathcal{D}_\beta = \mathcal{D}^{-1} \circ L_\beta \circ \mathcal{D},$$

where $\mathcal{D}$ is a deformation map. This reproduces the QCA's $O(k^2)$ dispersion correction at the representation level.

---

## 4. General Relativity on the Lattice

### 4.1 Variable-$c$ propagator

Gravity is introduced by promoting $c$ to a position-dependent field:

$$c(\mathbf{x}) = \frac{c_0}{1 - 2\phi(\mathbf{x})/c_0^2},$$

where $\phi$ is the Newtonian gravitational potential. This is the Paper 6 isotropic effective-medium ansatz. The propagation kernel becomes $c(\mathbf{x})$-dependent at each cell.

The variable-$c$ stepper uses the **Cayley transform** to maintain exact unitarity:

$$U_\text{Cayley} = \frac{I - iH\,dt/2}{I + iH\,dt/2},$$

with the Strang symmetric composition for second-order accuracy.

### 4.2 Open-BC Poisson solver

The gravitational potential is sourced by $\nabla^2\phi = 4\pi G\rho$ with **free-space boundary conditions**, implemented via the James/Hockney zero-padded FFT method:

1. Zero-pad the source $\rho$ from $(L,L,L)$ to $(2L,2L,2L)$.
2. Build the discrete free-space Green's function $G(r) = -1/(4\pi r)$ on the doubled grid.
3. Convolve: $\phi_k = 4\pi G_N \cdot \rho_k \cdot G_k$.
4. Extract the central $(L,L,L)$ block.

This recovers $\phi(r) = -G_N M/r$ to machine precision for $r \ge 20$ cells.

### 4.3 Light deflection (GR-1)

The eikonal deflection integral:

$$\Delta\theta = \frac{4GM}{bc^2},$$

where $b$ is the impact parameter and the integral picks up contributions from the gradient $\partial_y \phi$ along the photon path. The lattice coefficient $|K| = \Delta\theta\, b\, c_0^2 / (GM)$ converges to $3.881$ with the open-BC kernel (3.0% off Einstein's factor-4; PASS at 5% gate).

### 4.4 Shapiro delay (GR-2)

The excess travel time along a ray of impact parameter $b$:

$$\Delta t_\text{excess} = \int \!\left(\frac{1}{c(\mathbf{x})} - \frac{1}{c_0}\right)d\ell,$$

compared to the GR closed form:

$$\Delta t_\text{GR} = \frac{2GM}{c_0^3}\log\!\frac{r_1 + r_2 + r_{12}}{r_1 + r_2 - r_{12}}.$$

With the open-BC kernel the lattice ratio $\Delta t_\text{lat}/\Delta t_\text{GR} = 1.00058$ at $L=192$ (0.06% off; PASS at 0.1% gate). This **pins the PPN parameter $\gamma = 1$**.

### 4.5 Pound–Rebka redshift (GR-3) — factor-2 discrepancy and resolution

The Paper-6 single-scalar $c(\mathbf{x})$ ansatz gives:

$$\frac{\Delta\nu}{\nu} = \frac{2\Delta\phi}{c^2},$$

but measured GR requires $\Delta\nu/\nu = \Delta\phi/c^2$. The factor-2 discrepancy is an intrinsic feature of coupling both the metric time component $g_{00}$ and spatial component $g_{ii}$ to the same scalar $\phi$. Three forks resolve it (Finding 16):

- **Fork A:** Separate phase-tick field $\tau(\mathbf{x}) = 1 + \phi/c_0^2$ for the clock, independent of the spatial propagator.
- **Fork B:** Anisotropic metric $g_{00} = -(1+2\phi/c_0^2)$, $g_{ii} = (1-2\phi/c_0^2)$, with $c_\gamma = c_0\sqrt{|g_{00}|/g_{ii}}$.
- **Fork C:** Two exponents — photons see $2\phi$, matter sees $\phi$. *Falsified* by GR-4 (predicts half the Mercury perihelion advance).

### 4.6 Mercury perihelion precession (GR-4)

The 1PN Will/Soffel equation of motion:

$$\ddot{\mathbf{r}} = -\frac{GM\hat{r}}{r^2} + \frac{GM}{c^2 r^2}\!\left[\!\left(\frac{4GM}{r} - v^2\right)\hat{r} + 4(\hat{r}\cdot\mathbf{v})\mathbf{v}\right].$$

The predicted per-orbit advance:

$$\Delta\omega_\text{GR} = \frac{6\pi GM}{a(1-e^2)c^2}.$$

The lattice gives 1.5% error at $v^2/c^2 = 5.6\times10^{-3}$, consistent with the expected 2PN truncation.

---

## 5. Composite Photon

### 5.1 De Broglie bilinear construction

The composite photon is a bilinear of two BCC Weyl QCA spinors $\phi$ and $\psi$ (each at half the photon momentum):

$$G^i(\mathbf{k},t) = \phi^T(\mathbf{k}/2)\,\sigma^i\,\psi(\mathbf{k}/2),$$

where $\sigma^i$ are the Pauli matrices. The transverse components $G_T = \mathbf{A} + i\mathbf{C}$ (real 3-vector decomposition) give the electric and magnetic fields:

$$E_G = 2|\tilde{n}|\,\mathbf{A}, \qquad B_G = 2|\tilde{n}|\,\mathbf{C}.$$

**Poynting energy conservation (Finding 17).** For helicity eigenmodes:

$$\mathbf{A}\cdot\mathbf{C} = 0, \quad \|\mathbf{A}\|^2 = \|\mathbf{C}\|^2 \quad\text{(circularity identities)},$$

which imply:

$$\|E_G\|^2 + c^2\|B_G\|^2 = 4|\tilde{n}|^2\|G_T\|^2 = \text{const}.$$

This is exactly conserved (machine precision, Finding 17 / Tier 1 #44).

### 5.2 Composite-photon dispersion

The photon frequency is $\Omega = 2\omega_\text{half}$, giving (on BCC):

$$\Omega_\gamma = \frac{|\mathbf{k}|}{\sqrt{3}} = c_\text{lat}\,|\mathbf{k}|.$$

### 5.3 Curl residual — $O(k)$ gap

The pointwise bilinear satisfies the Maxwell curl equation only to $O(k)$:

$$\frac{\|\partial_t \mathbf{E}_G - i\,2\tilde{\mathbf{n}}\times\mathbf{B}_G\|}{(\|\mathbf{E}_G\|+\|\mathbf{B}_G\|)\,|k|} = \frac{c_\text{lat}}{\sqrt{2}} \quad \text{(geometry-independent, Finding 21)}.$$

This is an exact law: the coefficient $c_\text{lat}/\sqrt{2}$ holds across BCC, simple-cubic, and scaled-cubic geometries (5 geometries verified to 6 figures). Fixing the geometry does **not** fix the curl equation; Paper 1's smearing function $f_\mathbf{k}(\mathbf{q})$ is required to push the residual from $O(k)$ to $O(k^3)$.

---

## 6. Mohr (2010) Photon Wave Function

### 6.1 Six-component Ψ

Mohr constructs a Lorentz-covariant photon wave function as a 6-component spinor:

$$\Psi = \begin{pmatrix}\mathbf{E}_s \\ ic\mathbf{B}_s\end{pmatrix},$$

satisfying $i\partial_t\Psi = c|\mathbf{p}|\Psi$ (massless wave equation) with the Hamiltonian expressed via **spin-1 tau matrices** $\tau^i$ (the $3\times3$ generalisation of Pauli matrices):

$$H = c\,\boldsymbol{\tau}\cdot\mathbf{p}.$$

### 6.2 Polarization basis (C1)

Two transverse polarization vectors $\hat{\epsilon}_\lambda$ ($\lambda = \pm 1$) and one longitudinal $\hat{k}_s$:

- Transversality: $\hat{k}_s^\dagger \hat{\epsilon}_\lambda = 0$.
- Orthonormality: $\hat{\epsilon}_\lambda^\dagger \hat{\epsilon}_\mu = \delta_{\lambda\mu}$.
- Completeness: $\sum_\lambda \hat{\epsilon}_\lambda \hat{\epsilon}_\lambda^\dagger = (\boldsymbol{\tau}\cdot\hat{k})^2$.

### 6.3 Lorentz boost covariance (C3)

Under a Lorentz boost with velocity $v$ the wave function transforms as:

$$\hat{\epsilon}'_\lambda = \hat{\epsilon}_\lambda\,\xi, \qquad \xi = \cosh\zeta + \hat{v}\cdot\hat{k}\sinh\zeta,$$

with the boosted transversality $\hat{k}'{}^\dagger_s \hat{\epsilon}' = 0$ preserved exactly.

### 6.4 Vector spherical harmonics (C5)

Angular-momentum eigenstates are built from the CG-coupled vector spherical harmonics $Y^m_{jl}(\theta,\phi)$ satisfying:

- Orthonormality: $\int Y^{m\dagger}_{jl}\cdot Y^{m'}_{j'l'}\,d\Omega = \delta_{jj'}\delta_{mm'}\delta_{ll'}$.
- Transversality for magnetic multipoles: $\hat{n}_s^\dagger\cdot Y^m_{j,M} = 0$.
- $J_z$ eigenvalue: $(L_z + S_z)Y^m_{jl} = m\,Y^m_{jl}$.

### 6.5 Maxwell Green function (C6)

The inverse Hamiltonian (off-shell Green function):

$$(H(\mathbf{k}) - (\omega + i\varepsilon)I)\cdot G(\omega,\mathbf{k}) = I.$$

The Weyl current for a BCC eigenmode:

$$J^0 = \psi^\dagger\psi = 1, \quad \|\vec{J}\| = \|\psi^\dagger\vec{\sigma}\psi\| = 1, \quad \vec{J} = \hat{n}.$$

---

## 7. EMQG — Electro-Magnetic Quantum Gravity (Ostoma-Trushyk 1999)

### 7.1 Field equation

EMQG modifies the Poisson equation to include retardation:

$$\nabla^2\phi - \frac{1}{c^2}\frac{\partial^2\phi}{\partial t^2} = 4\pi G\rho.$$

This is the scalar wave equation with gravitational source, recovering Newtonian gravity in the static limit.

### 7.2 Three mass definitions

EMQG distinguishes: (i) **gravitational mass** $m_g$ sourcing $\phi$; (ii) **inertial mass** $m_i$ resisting acceleration; (iii) **quantum mass** $m_q$ from internal oscillation energy. EMQG derives their equality as an emergent consequence of the lattice dynamics — not a postulate.

### 7.3 Fizeau analog

The index-of-refraction formulation: gravitational time dilation is equivalent to a locally varying speed of light, exactly as Fizeau's experiment measures the group velocity of light in a moving medium. The EMQG $c(\mathbf{x})$ field is the lattice realisation of this.

---

## 8. SU(2) Weak Gauge — Parity Violation

The weak gauge couples **only to the left-chirality (η) sector** of the Dirac spinor:

$$U_\text{weak} = e^{i\,\boldsymbol{\alpha}\cdot\boldsymbol{\sigma}/2} \quad \text{(acting on }\eta\text{ only)}.$$

**Parity violation.** A right-chirality ($\chi$) initial state evolves with **zero SU(2) phase pickup** — confirmed to machine zero (Tier 1 #10). A left-chirality state picks up the full gauge phase.

---

## 9. SU(3) Strong Gauge

### 9.1 Gell-Mann generators

The eight $3\times3$ Hermitian traceless generators $T^a = \lambda^a/2$ satisfy:

$$\mathrm{Tr}(T^a T^b) = \tfrac{1}{2}\delta^{ab}, \qquad [T^a, T^b] = if^{abc}T^c.$$

Normalisation confirmed to Tier 1 residual $1.1\times10^{-16}$ (#31).

### 9.2 Link-variable lattice formulation

The gauge field lives on lattice links as SU(3)-valued matrices $U_\mu(\mathbf{x})$. Quarks carry a 3-component colour index $q = (q_r, q_g, q_b)^T$. The covariant propagation step:

$$q(\mathbf{x}+\hat\mu) \to U_\mu(\mathbf{x})\,q(\mathbf{x}+\hat\mu).$$

### 9.3 Wilson plaquette action

The gauge-invariant action density is:

$$S_\text{Wilson} = \sum_{\square} \mathrm{Re}\,\mathrm{Tr}\,U_\square, \qquad U_\square = U_\mu U_\nu U_\mu^\dagger U_\nu^\dagger.$$

Gauge invariance under $U_\mu(\mathbf{x}) \to V(\mathbf{x})U_\mu(\mathbf{x})V^\dagger(\mathbf{x}+\hat\mu)$ is exact (Tier 1 #34, residual $4.4\times10^{-16}$).

### 9.4 Colour charge conservation

The global colour charge:

$$Q^a = \sum_\mathbf{x} q^\dagger(\mathbf{x})\,T^a\,q(\mathbf{x})$$

is conserved under the cold-link SU(3) Strang stepper to machine precision (Tier 2 #8).

---

## 10. Higgs Mechanism

### 10.1 Complex scalar field — Mexican-hat potential

The Higgs field $\Phi(\mathbf{x}) \in \mathbb{C}$ evolves under the potential:

$$V(\Phi) = -\mu^2|\Phi|^2 + \lambda|\Phi|^4, \qquad |\Phi|^2_\text{vac} = v^2 = \frac{\mu^2}{2\lambda}.$$

The vacuum expectation value $v = \mu/\sqrt{2\lambda}$ breaks the $U(1)$ symmetry spontaneously.

### 10.2 Goldstone boson

The angular (phase) mode has the dispersion:

$$\omega_G = |\mathbf{k}|,$$

confirmed to lattice precision (Tier 1 #6, residual $\le 0.88\,\varepsilon$ at $L=640$).

### 10.3 Higgs radial mode

The radial (amplitude) mode has the dispersion:

$$\omega_H = \sqrt{|\mathbf{k}|^2 + 2\mu^2},$$

confirmed with $O(dt^2)$ Verlet accuracy (Tier 3 #6).

### 10.4 Yukawa coupling

The fermion acquires a position-dependent mass from the Higgs vev:

$$m_\text{eff}(\mathbf{x}) = y\,\mathrm{Re}(\Phi(\mathbf{x})),$$

where $y$ is the Yukawa coupling constant. In the uniform-$\Phi$ limit this reduces exactly to a constant mass: $m_\text{eff} = y\cdot v$ (Tier 1 #49, Yukawa uniform-Φ regression exact to bit-zero).

---

## 11. Split-Step FFT Propagator

The exact-unitary propagator uses **Strang symmetric composition** (split-step):

$$U_\text{Strang}(\Delta t) = e^{-iH_x\Delta t/2}\,e^{-iH_y\Delta t/2}\,e^{-iH_z\Delta t}\,e^{-iH_y\Delta t/2}\,e^{-iH_x\Delta t/2}.$$

Each factor is computed via FFT: transform to $k$-space, multiply by the eigenvalue, inverse transform. This is **exact-unitary** (norm conserved to machine precision) and is the core numerical method for all Weyl, Dirac, Maxwell, and gauge propagation steps.

The FFT round-off floor is $\sim 1$ ulp of complex128 per step, scaling as $\sqrt{N_\text{cells}} \times n_\text{steps}$.

---

## 12. Emergent Time

Each lattice cell accumulates a **tick counter** $N(\mathbf{x})$ counting the number of times the local amplitude was large enough to constitute a "tick". Two implementations:

- **Binary tick** $N_\text{binary}$: increments by 1 when $|\psi(\mathbf{x})|^2 > \text{threshold}$.
- **Phase accumulation**: counts full $2\pi$ phase cycles.

**Key result (Finding 11).** In the variable-$c$ (curved spacetime) regime, the ratio of tick counts inside vs outside a gravitational well satisfies:

$$\frac{N_\text{phase,in}}{N_\text{phase,out}} = \frac{c_\text{in}}{c_\text{out}},$$

to residual $2.7\times10^{-16}$ — the Shapiro-delay relation for tick rates.

**Vacuum freezing (Finding / Tier 1 #2).** True-vacuum cells satisfy $N_\text{binary}(\mathbf{x}) = 0$ exactly — 80% of an $L=256$ lattice remains frozen in the F1 vacuum regression.

---

## 13. Scalar QFT — Handwritten Notes (Mark Ludwig)

The physics notes pages include canonical quantisation of the scalar field:

$$\mathcal{L} = \tfrac{1}{2}(\partial_\mu\phi)^2 - \tfrac{1}{2}m^2\phi^2.$$

**Mode expansion:**

$$\phi(\mathbf{x},t) = \int \frac{d^3k}{(2\pi)^3 2\omega_k}\left[a_{\mathbf k}e^{i(\mathbf{k}\cdot\mathbf{x}-\omega_k t)} + a_{\mathbf k}^\dagger e^{-i(\mathbf{k}\cdot\mathbf{x}-\omega_k t)}\right],$$

$$[\phi(\mathbf{x},t), \pi(\mathbf{y},t)] = i\delta^3(\mathbf{x}-\mathbf{y}).$$

**Weyl representation.** The Dirac equation $i\gamma^\mu\partial_\mu\psi = m\psi$ in the Weyl (chiral) basis with $\gamma^5\psi_{L/R} = \mp\psi_{L/R}$.

---

## 14. Sachs Electrogravity (from physics notes)

The notes include Sachs's spinor extension of GR, constructing the electromagnetic and gravitational fields as components of a single spinor-valued curvature tensor. The Sachs formalism treats the photon and graviton as two helicity states of the same underlying entity — this connects to the composite-photon construction (§5) and provides a potential route to unification beyond the Standard Model.

---

## 15. Neutrino Oscillations (QFT-5)

The PMNS mixing matrix $U$ relates flavour states $(ν_e, ν_\mu, ν_\tau)$ to mass eigenstates:

$$|\nu_\alpha(t)\rangle = \sum_i U_{\alpha i}\,e^{-i\omega_i t}\,|\nu_i\rangle.$$

**Unitarity:** $U U^\dagger = I$ confirmed to $7.7\times10^{-17}$ (Tier 1 #16).

**2-flavour oscillation probability:**

$$P(\nu_\alpha \to \nu_\beta) = \sin^2(2\theta)\sin^2\!\left(\frac{\Delta m^2 L}{4E}\right).$$

The lattice propagator reproduces this exactly to $4.4\times10^{-16}$ (Tier 1 #17).

---

## 16. Bell / CHSH Inequality (QM-1)

The CHSH operator $S = A(B+B') + A'(B-B')$ obeys:

$$|S| \le 2 \quad \text{(classical)}, \qquad |S| \le 2\sqrt{2} \quad \text{(Tsirelson, quantum)}.$$

The lattice Dirac singlet saturates the Tsirelson bound $|S| = 2\sqrt{2}$ to $4.4\times10^{-16}$ with the pure state, confirming the lattice is genuinely quantum (not a local hidden-variable model) to machine precision.

---

## 17. Aharonov–Bohm Effect (E1)

A charged particle traversing a loop enclosing magnetic flux $\Phi_B$ acquires a phase:

$$\Delta\phi_{AB} = \exp\!\left(i\oint \mathbf{A}\cdot d\boldsymbol{\ell}\right).$$

The lattice U(1) gauge coupling gives this phase pickup exactly, confirmed to $4.4\times10^{-16}$ (Tier 1 #14).

---

## 18. Planck-Scale Lorentz Violation Bound (QG-2)

The QG-2 test translates the dimensionless lattice LV coefficient $\beta_\text{LV}$ to a physical energy scale using the SI identification $a = \ell_P$:

$$E_\text{LV} = \frac{m_P c^2}{\sqrt{|\beta_\text{LV}(m)|}} \approx 1.87\times10^{20}\,\text{GeV}.$$

The Fermi GRB 090510 bound requires $E_\text{LV} \gtrsim 1.2\times10^{19}$ GeV. The lattice passes by $\sim10\times$ at $a = \ell_P$, and would remain consistent for $a$ up to $\sim1.5\times10^{-34}$ m (about $10\times\ell_P$).

---

## 19. Noether Charge Conservation (QG-4)

**U(1) charge:** $Q = \sum_\mathbf{x}\psi^\dagger(\mathbf{x})\psi(\mathbf{x})$ is conserved to $1.8\times10^{-16}$ per step (the FFT floor).

**Chiral charge:** $Q_\chi = Q_L - Q_R$ is conserved exactly at $m=0$ (Tier 1 #18, residual $2.2\times10^{-16}$) and explicitly broken at $m\ne0$ by the mass coupling — as expected.

**Discrete continuity equation:**

$$\partial_t\rho + \nabla\cdot\mathbf{j} = 0,$$

confirmed globally to $2.2\times10^{-16}$ over a single step (Tier 1, Finding 14.13 Stage 4).

---

*End of Physics Summary. Cross-reference: `findings.md`, `exactness-inventory.md`, `reference-research/`, and the simulation modules in `ca-simulation/`.*
