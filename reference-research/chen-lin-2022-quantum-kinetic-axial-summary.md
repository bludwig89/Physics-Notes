# Summary: "Quantum Kinetic Theory with Vector and Axial Gauge Fields"
### Zhou Chen & Shu Lin — *Phys. Rev. D* **105**, 014015 (2022)

*Summarized: 2026-05-24 - 15:00*
*Source: `reference-research/quantum-kinetic-theory-with-vectory-and-axial-gauge-fields.pdf`*

---

## 1. Core Thesis

For massless chiral fermions, the paper extends quantum kinetic theory by treating **vector $A_\mu$ and axial $A_\mu^5$ gauge fields on equal footing**, working through first order in the gradient (ℏ) expansion. Putting both gauge fields at the same level — equivalent to treating left- and right-handed fermions symmetrically — yields the **covariant current** automatically. The **consistent current** (the one that obeys Wess–Zumino consistency) is then obtained from the covariant current by adding the Chern–Simons term. The Chen–Lin construction gives a unified derivation of all anomalous transports (CME, CVE, CSE, anomalous Hall) and Onsager-related correlation functions in a single framework.

---

## 2. Lagrangian and Kinetic Equation (Section II)

$$\mathcal{L} = i\bar\psi \not\!D \psi, \qquad D_\mu = \partial_\mu + iA_\mu + i\gamma^5 A_\mu^5 \tag{1}$$

Coupling constants are absorbed into the gauge potentials. The Wigner function with canonical momentum $p_\mu$ satisfies

$$\gamma_\mu\!\left(\mathcal{K}^\mu + \tfrac{i}{2}\mathcal{D}^\mu + \gamma^5 \Pi^\mu\right) S^<(p,X) = 0 \tag{4}$$

with

$$\mathcal{K}^\mu = p^\mu - A^\mu, \quad \mathcal{D}^\mu = \partial_X^\mu + (\partial_{X,\lambda}A^\mu)\partial_p^\lambda, \quad \Pi^\mu = A^{5\mu} + \tfrac{1}{2}(\partial_{X,\lambda}A^{5\mu})\partial_p^\lambda.$$

The clever step (avoiding axial-gauge subtleties) is to **directly solve Eq. (4) without defining any gauge link**: the gauge-linked Wigner function is obtained from the bare one by replacing the canonical momentum $p^\mu$ by the **kinetic momentum** $k_\mu^s = p_\mu - A_\mu \mp A_\mu^5$ for right- (+) and left- (−) handed components.

The resulting solution is automatically invariant under both vector and axial gauge symmetry.

---

## 3. Chiral Basis Decoupling (Eq. 11–14)

The Wigner function decouples in the chiral basis:

$$\mathcal{J}_s^\mu = \tfrac{1}{2}(\mathcal{V}^\mu + s\mathcal{A}^\mu), \quad s = \pm 1 \quad \text{(right- and left-handed)}$$

obeying

$$k_\mu^s \mathcal{J}_s^\mu = 0, \qquad \nabla_\mu^s \mathcal{J}_s^\mu = 0, \qquad k_\mu^s \mathcal{J}_s^\nu - k_\nu^s \mathcal{J}_s^\mu + \tfrac{s}{2}\epsilon^{\mu\nu\alpha\beta}\nabla_\alpha^s\mathcal{J}_{s,\beta} = 0 \tag{11{-}13}$$

with $k_\mu^s = p_\mu - A_\mu^s$ and $A_\mu^s = A_\mu + sA_\mu^5$, $\nabla_\mu^s = \partial_\mu + (\partial_\lambda A_\mu^s)\partial_p^\lambda$. Each chirality has its own effective gauge field $A_\mu^s$; the two chiral sectors are then **two independent chiral kinetic theories** stitched together.

---

## 4. Equilibrium and Killing Conditions (Section III)

The equilibrium Wigner function is the Fermi–Dirac distribution in kinetic momentum:

$$f_s(k_s, X) = \tfrac{2}{(2\pi)^3}[\theta(u\cdot k_s)f_{FD}(\beta\cdot k_s - \bar\mu_s) + \theta(-u\cdot k_s)f_{FD}(-\beta\cdot k_s + \bar\mu_s)] \tag{22}$$

with $\beta^\mu = \beta u^\mu = u^\mu/T$ and $\bar\mu_s = \beta\mu_s$, $\mu_s = \mu + s\mu_5$.

Global equilibrium requires the **Killing conditions**:

$$\partial_\mu \beta_\nu + \partial_\nu \beta_\mu = 0, \qquad \partial_\mu \bar\mu_s = -F_{\mu\nu}^s \beta^\nu \tag{26{-}27}$$

Equation (27) decomposes as $\partial_\mu\bar\mu = -F_{\mu\nu}\beta^\nu$ and $\partial_\mu\bar\mu_5 = -F_{\mu\nu}^5 \beta^\nu$ — the gradient of vector chemical potential balances the electric field, and similarly for axial.

The first-order solution is

$$\mathcal{J}_\mu^s = k_\mu^s \delta(k_s^2)f_s - \tfrac{s}{2}\widetilde\Omega_{\mu\nu}k_s^\nu \delta(k_s^2)f_s' + s\widetilde F_{\mu\nu}^s k_s^\nu \delta'(k_s^2)f_s \tag{33}$$

with $\widetilde F_{\mu\nu}^s = \tfrac{1}{2}\epsilon^{\mu\nu\alpha\beta}F^s_{\alpha\beta}$, $\widetilde\Omega_{\mu\nu} = \tfrac{1}{2}\epsilon^{\mu\nu\alpha\beta}\Omega_{\alpha\beta}$.

---

## 5. Anomalous Transports (Section IV)

Integrating over $k_s$ gives the one-point currents. To first order:

$$j_{\pm}^{(1)\mu} = \xi_{\pm}\omega^\mu + \xi_{B\pm}B^\mu_{\pm} \tag{40}$$

with

$$\xi_s = \tfrac{s}{12\pi^2}\!\left(\tfrac{\pi^2}{\beta^2} + 3\mu_s^2\right), \qquad \xi_{Bs} = \tfrac{s}{4\pi^2}\mu_s. \tag{44{-}45}$$

The vector and axial currents (CME and CSE for vector $B$ field, plus axial counterparts) come out as

$$j^\mu_{B,\text{cons}} = \tfrac{1}{2\pi^2}\!\left(\mu_5 - \tfrac{A_0^5}{3}\right)B^\mu + \tfrac{1}{2\pi^2}\mu B_5^\mu, \quad
j^\mu_{5,B,\text{cons}} = \tfrac{1}{2\pi^2}\!\left(\mu_5 - \tfrac{A_0^5}{3}\right)B_5^\mu + \tfrac{1}{2\pi^2}\mu B^\mu \tag{68}$$

The covariant and consistent currents differ by Chern–Simons / Bardeen counterterms; consistent currents satisfy Wess–Zumino consistency conditions.

---

## 6. Covariant Anomaly (Section IV)

The conservation equations come out as expected:

$$\partial_\mu j^\mu_\text{cov} = \tfrac{1}{2\pi^2}(\vec E\cdot\vec B + \vec E_5\cdot\vec B_5), \qquad
\partial_\mu j_{5,\text{cov}}^\mu = \tfrac{1}{2\pi^2}(\vec E\cdot\vec B + \vec E_5\cdot\vec B_5). \tag{61{-}62}$$

Both vector and axial covariant currents have **the same** divergence — the standard covariant chiral anomaly. The fact that vector current is not conserved in the covariant scheme is the source of the consistent / covariant distinction.

Energy–momentum has the usual conservation $\partial_\mu T^{\{\mu\nu\}} = F^{\nu\mu}j_{\text{cov},\mu} + F^{\mu\nu}_5 j_{5,\text{cov},\mu}$, and the antisymmetric part vanishes (Belinfante–Rosenfeld). Onsager relations $\langle T^{\{0i\}}j^j\rangle = \langle T^{\{0j\}}j^i\rangle$ are reproduced.

---

## 7. Correlation Functions (Section IV.B)

Using $\delta\Gamma/\delta A_\mu = j^\mu_\text{cons}$, the paper computes two- and three-point correlation functions:

$$\langle \widetilde j_\text{cons}^i(k)\widetilde j_\text{cons}^j(-k)\rangle = \tfrac{i\mu_5 \epsilon^{ijk}k^k}{2\pi^2}, \qquad
\langle \widetilde j_\text{cons}^i \widetilde j_{5,\text{cons}}^j \rangle = \tfrac{i\mu \epsilon^{ijk}k^k}{2\pi^2}, \ldots \tag{70}$$

and three-point analogs (Eq. 72) and current–stress-tensor correlators reproducing CVE.

---

## 8. Mass Limitation (explicit, Section V outlook)

The paper is strictly **massless**. The summary explicitly states:

> "Mass effect can be included. Since mass breaks axial symmetry explicitly, it requires a nontrivial modification to the solution presented in this work. It is known that mass introduces additional degrees of freedom. It would be interesting to see how the dynamics of these degrees of freedom are affected by the presence of an axial gauge field."

This is the explicit overlap point with Hattori–Hidaka–Yang 2019 (Axial Kinetic Theory) — that paper takes the massive-case bridge, but only with the vector EM field; Chen–Lin 2022 has both vector and axial gauge fields but only massless.

---

## 9. Direct Bearing on the Cellular-Automaton Project

### A. Vector + axial symmetric treatment as template
The most useful structural result is the **equal-footing treatment** of $A_\mu$ and $A_\mu^5$. In the CA model:
- The photon $A_\mu$ sits inside the F26 rotation law.
- F27's complex mass introduces a local SU(2) phase $U(x)$ acting on the chirality sector — this is the closest CA analog to the axial gauge field.
- Paper's $A_\mu^s = A_\mu + sA_\mu^5$ has direct interpretation: in the chiral basis (η, χ separately), each chirality sees an effective gauge field that differs by a sign-of-chirality term.

The CA correspondence: $U(x) = \exp(i\theta(x)\sigma_a)$ (F27's gauge field on the mass step) plays the role of the axial gauge field $A^5_\mu$ in the continuum, up to the BCC discretization.

### B. Covariant vs. consistent current distinction
The CA model has not yet drawn the distinction. F27 measures the axial Ward identity at machine precision. The continuum-side question is whether the lattice axial Ward identity, if it exists, is the **covariant** one (with anomaly) or the **consistent** one. This paper's Eq. (67) gives the explicit Chern–Simons-term transformation between them; could be used as a target test at finite lattice resolution.

### C. Killing condition $\partial_\mu \bar\mu_5 = -F^5_{\mu\nu}\beta^\nu$
For a CA model with thermal vorticity / chemical potential, the Killing condition is the kinematic constraint that has to hold for the F27 mass step to admit a steady-state distribution. Worth a test in extended CA runs.

### D. Limitations for the project
- **Massless only.** Cannot directly inform F27's complex-mass step.
- **External gauge fields only.** Both $A$ and $A^5$ are non-dynamical backgrounds; the paper does not generate them. This is exactly the opposite of what the project's F31/F32 roadmap is doing for $W_\mu$.
- **Does NOT eliminate $W_\mu$.** The "axial gauge field" $A^5_\mu$ is a probe field for the axial current, not a substitute for $W_\mu$ in giving fermions left-handed gauge dynamics.

---

## 10. Key Citations Carried Forward

- Stephanov & Yin 2012, Son & Yamamoto 2012, 2013 — Berry-phase derivation of CKT
- Hidaka, Pu & Yang 2017–2018 — collisional CKT, side-jump effects
- Mueller & Venugopalan 2018 — torsion-based derivation of energy–momentum correlation
- Bertlmann 2000 — Bardeen counterterms and covariant/consistent distinction (textbook)
- Hattori, Hidaka, Yang 2019 (AKT) — the massive companion paper; explicitly cited as the route for adding mass
