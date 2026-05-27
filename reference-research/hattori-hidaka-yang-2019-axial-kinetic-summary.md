# Summary: "Axial Kinetic Theory and Spin Transport for Fermions with Arbitrary Mass"
### Koichi Hattori, Yoshimasa Hidaka, Di-Lun Yang — *Phys. Rev. D* **100**, 096011 (2019)

*Summarized: 2026-05-24 - 14:45*
*Source: `reference-research/axial-kinetic-theory-and-spin-transport-for-fermions.pdf`*

---

## 1. Core Thesis

The paper derives a **quantum kinetic theory for Dirac fermions of arbitrary mass** in a background electromagnetic field, using the Wigner-function formalism. The construction bridges two regimes that had been treated separately:

- **Massless fermions** (Weyl): Chiral Kinetic Theory (CKT). Spin is enslaved to momentum, so there is one scalar distribution function $f$ per chirality.
- **Massive fermions**: Spin is an independent dynamical d.o.f. — needs its own kinetic equation.

The result is one scalar kinetic equation (SKE) and one axial-vector kinetic equation (AKE), with magnetization currents pertinent to spin–orbit interaction. In the $m \to 0$ limit the AKE reduces to the established CKT.

---

## 2. Wigner Function and Clifford Decomposition (Section II)

For a massive Dirac field $\psi$, the lesser propagator $S^<_{\alpha\beta}(x,y) = \langle \bar\psi_\beta(y)\psi_\alpha(x)\rangle$ Wigner-transforms to $S^<(q,X)$ with $X = (x+y)/2$, $Y = x - y$. The Clifford decomposition is:

$$S^< = \mathcal{S} + i\mathcal{P}\gamma^5 + \mathcal{V}^\mu\gamma_\mu + \mathcal{A}^\mu\gamma^5\gamma_\mu + \tfrac{1}{2}\mathcal{S}^{\mu\nu}\Sigma_{\mu\nu} \tag{2}$$

with $\Sigma_{\mu\nu} = i[\gamma_\mu,\gamma_\nu]/2$. The five components carry physical content:

- $\mathcal{V}^\mu$: vector current → fermion number density and current
- $\mathcal{A}^\mu$: axial-vector current → chirality / spin polarization
- $\mathcal{S},\,\mathcal{P}$: scalar / pseudoscalar condensates
- $\mathcal{S}^{\mu\nu}$: spin (magnetization) tensor

---

## 3. Master Equations (Section II)

The collisionless equation $(\not\!\Pi - m)S^< + i\tfrac{\hbar}{2}\gamma^\mu \nabla_\mu S^< = 0$ with the gauge-covariant operators

$$\nabla_\mu = \partial_\mu + F_{\mu\nu}\partial_q^\nu - \tfrac{\hbar^2}{24}(\partial_\rho \partial_\lambda F_{\mu\nu})\partial_q^\rho \partial_q^\lambda \partial_q^\nu + O(\hbar^4), \quad
\Pi_\mu = q_\mu + \tfrac{\hbar^2}{12}(\partial_\rho F_{\mu\nu})\partial_q^\rho \partial_q^\nu + O(\hbar^4) \tag{A8}$$

yields ten equations. Three crucial ones link the components:

$$m\mathcal{S} = \Pi\cdot\mathcal{V}, \qquad m\mathcal{P} = -\tfrac{\hbar}{2}\nabla_\mu\mathcal{A}^\mu, \qquad m\mathcal{S}_{\mu\nu} = -\epsilon_{\mu\nu\rho\sigma}\Pi^\rho\mathcal{A}^\sigma + \tfrac{\hbar}{2}\nabla_{[\mu}\mathcal{V}_{\nu]} \tag{4}$$

This is the central structural finding: **mass acts as the coupling between the vector and axial sectors**. When $m = 0$, V and A decouple; when $m \neq 0$, they are algebraically tied through the scalar and tensor components.

---

## 4. Vector Wigner Functions / Scalar Kinetic Equation (Section III)

Perturbative expansion $(\mathcal{V}/\mathcal{A})^\mu = (\mathcal{V}/\mathcal{A})_0^\mu + \hbar(\mathcal{V}/\mathcal{A})_1^\mu$. The zeroth-order solutions sit on the mass shell:

$$(\mathcal{V}_0 / \mathcal{A}_0)^\mu = 2\pi(q/a)^\mu \delta(q^2 - m^2)\,f_{V/A}(q, X) \tag{11}$$

where $a^\mu$ is the (non-normalized) spin four-vector, $a\cdot q = 0$, $a^2 = -m^2$, and $f_{V/A}$ are the vector / axial distribution functions.

The first-order Wigner functions get a magnetization-current (MC) correction:

$$\mathcal{V}_1^\mu = 2\pi\widetilde{F}^{\mu\nu}a_\nu \delta'(q^2-m^2)f_A + 2\pi\delta(q^2-m^2)\,G^\mu \tag{12}$$

with $G^\mu = (\epsilon^{\mu\nu\rho\sigma}n_\nu / 2q\cdot n)[\Delta_\rho(a_\sigma f_A) + F_{\rho\sigma}f_A]$ where $n^\mu$ is the rest-frame timelike vector and $\widetilde F^{\mu\nu} = \epsilon^{\mu\nu\alpha\beta}F_{\alpha\beta}/2$ is the dual.

The SKE is obtained by plugging back. In the $m \to 0$ limit with $a^\mu = q^\mu$ it reduces exactly to the known CKT.

---

## 5. Axial Wigner Functions / AKE (Section IV)

For the axial sector the master equations alone are ambiguous in the MC term, so the paper builds the Wigner function directly from second quantization. The result (after a tractable amount of algebra) is the **Axial Kinetic Equation**:

$$0 = \delta(q^2 - m^2)\!\left[q\cdot\Delta(a^\mu f_A) + F^{\nu\mu}a_\nu f_A\right] + (\hbar\text{ corrections involving spin tensor, MC, frame vector}) \tag{28}$$

The spin part of $\Delta_\mu \bar a^\nu = q\cdot \Delta a^\nu + F^\nu{}_\mu a^\mu$ is the **Bargmann–Michel–Telegdi equation** — the textbook semiclassical spin precession law for a relativistic particle in EM field. The AKE is the spin-polarization generalization.

In the $m \to 0$ limit the AKE reduces to the CKT (multiplied by $q^\mu$).

---

## 6. Anomalous Transport in Thermal Equilibrium (Section V)

The paper constructs equilibrium Wigner functions in constant magnetic field and thermal vorticity:

$$\mathcal{V}^\mu_\mathrm{eq} = 2\pi\delta(q^2 - m^2)\,q^\mu f_0, \qquad
\mathcal{A}^\mu_\mathrm{eq} = 2\pi\hbar\!\left[\tfrac{\delta'(q^2-m^2)}{4}q_\nu\epsilon^{\mu\nu\alpha\beta}\Omega_{\alpha\beta}\partial_{q,\beta} + \widetilde F^{\mu\nu}q_\nu\delta'(q^2-m^2)\right]\!f_0 \tag{31{-}32}$$

where $\Omega_{\mu\nu}$ is the thermal vorticity. Two main mass-corrected results:

- **Chiral Magnetic Effect (CME)** and **vector CVE**: vanish at equilibrium when $m \neq 0$.
- **Chiral Separation Effect (CSE)** and **axial CVE**: receive explicit mass corrections, with coefficients $\sigma_{B/\omega} = \tfrac{\hbar}{2\pi^2}\int_0^\infty d|q|\,g_{B/\omega}f_0^{(\pm)}(E_q)$ that interpolate between massless and massive limits.

---

## 7. Spin Hall Current (Eq. 30)

A particularly clean nonrelativistic result with constant frame vector and constant electric field:

$$J_5^\mu \approx -2\pi\hbar \epsilon^{\mu\nu\alpha\beta} E_\alpha n_\beta \int_q \delta(q^2 - m^2)\,\partial_{q\nu}f_V \tag{30}$$

This is the **spin Hall current** induced by an electric field acting on the rest-frame spin axis — a direct kinetic-theory derivation, mass-dependent, with no chiral anomaly required.

---

## 8. Direct Bearing on the Cellular-Automaton Project

The paper is **massless–to–massive bridge** technology for a quantum kinetic description of spinning fermions. It is not a mass-generation paper; it takes $m$ as a fixed parameter and asks how transport equations should look. Three points of contact with the CA model:

### A. Mass as V↔A coupling
The relations $m\mathcal{S} = \Pi\cdot\mathcal{V}$, $m\mathcal{P} = -\tfrac{\hbar}{2}\nabla\cdot\mathcal{A}$ are the continuum face of F27's mass-step: $\eta_\text{new}$ depends on $\chi$ with coefficient $im\,e^{i\theta}$ — left and right chirality are coupled through the mass parameter, with the coupling phase carrying chiral charge transfer between V and A sectors. The continuum check is whether F27's mass step, in the long-wavelength limit, reproduces $m\mathcal{S} = \Pi\cdot\mathcal{V}$ to algebraic exactness.

### B. Bargmann–Michel–Telegdi as a benchmark
The AKE contains the BMT equation as its $\hbar^0$ truncation. A CA-level test would be: prepare a polarized fermion wavepacket on the BCC lattice, evolve with F27's complex-mass step in a uniform background EM field, and verify the spin four-vector precesses according to BMT. This is a clean, mass-dependent, machine-precision target.

### C. Magnetization-current corrections
The MC term, $G^\mu$ in (13), is a structural prediction: at $O(\hbar)$ the vector current of a massive fermion in a non-uniform background acquires a contribution from spatial gradients of the axial distribution. This is **new physics** for the CA model in the sense that it predicts a measurable cross-coupling of axial and vector currents at finite mass. F27 already exhibits the analogous algebraic coupling at the step level — but the kinetic-theory consequence (a magnetization current) has not yet been tested.

### D. What the paper does NOT do for the project
- It does **not** generate mass. Mass is an input.
- It does **not** introduce $W_\mu$. The only gauge field is the U(1) EM field $A_\mu$.
- It does **not** treat chiral SU(2). The chirality is U(1) axial only.

So this paper is useful for **verifying** F27 against established continuum kinetic theory; it does not offer a way to eliminate either $W_\mu$ or the mass parameter from the model.

---

## 9. Key Citations Carried Forward

- Vasak, Gyulassy & Elze 1987 — Wigner-function approach to QFT plasma
- Stephanov & Yin 2012, Son & Yamamoto 2013 — Chiral Kinetic Theory foundational papers
- Hidaka, Pu & Yang 2017–2018 — collisional CKT, side-jump effects
- Becattini et al. 2013, Liu & Lin 2018 — global polarization, Λ hyperons in heavy-ion collisions
- Mueller & Venugopalan 2018, Yi & Yang 2020 — earlier mass-corrected AKT attempts
- Bargmann–Michel–Telegdi 1959 — classical relativistic spin precession
