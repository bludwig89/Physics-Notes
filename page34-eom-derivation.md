# Page 34 Equations of Motion — Derivation and Reconciliation with the Project

**Date:** 2026-05-30 - 21:06
**Scope:** Complete the four Euler–Lagrange equations that page 34 of `physics-notes-complete.md` sets up but leaves blank, then map each onto the project's emergent-gravity findings (F46, F50, F52, F55–F62), flagging where the Sachs first-order path diverges from what the lattice actually does.

> **Status of this document:** Analysis / reconciliation, not a new physics finding. The four EOM below are the *standard* result of a first-order (Palatini / Einstein–Cartan) variation; they are well-established in the continuum. The project-specific content is the reconciliation in each section. Term-by-term verification of the quaternion-trace algebra (especially $\delta R/\delta q^\mu$ in Sachs notation) must use the project's hand-rolled $\sigma$-matrix functions, **not** numpy/scipy (CLAUDE.md chiral-transform caveat) — it is presented here structurally.

---

## 0. The action and the independent fields

From pages 33–34, the total Lagrangian density is

$$\mathcal{L} = (-g)^{1/2}\Big\{\, R \;+\; \tfrac{i}{2}\big[\eta^{+} q^{\mu}\eta_{;\mu} - \eta^{+}_{;\mu} q^{\mu}\eta\big] \;+\; \tfrac{i}{2}\big[\chi^{+}\tilde q^{\mu}\chi_{;\mu} - \chi^{+}_{;\mu}\tilde q^{\mu}\chi\big]\Big\}$$

with the page-33/34 definitions

$$\eta_{;\mu} = \partial_\mu\eta + \Omega_\mu\eta,\qquad \chi_{;\mu}=\partial_\mu\chi + \Omega^{(\chi)}_\mu\chi,\qquad \Omega^{(\chi)}_\mu=-\Omega^{+}_\mu,$$

$$\sigma_0\,g^{\mu\nu}=\tfrac12\big(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu\big),\qquad g\equiv-\det g_{\mu\nu},$$

$$R=\tfrac14\,\mathrm{Tr}\big(K_{\mu\nu}q^\mu\tilde q^\nu - K_{\nu\mu}q^\mu q^\nu + q^\mu K^{+}_{\mu\nu}q^\nu - q^\nu K^{+}_{\mu\nu}\tilde q^\mu\big),$$

$$K_{\mu\nu}\equiv\partial_\mu\Omega_\nu-\partial_\nu\Omega_\mu+\Omega_\mu\Omega_\nu-\Omega_\nu\Omega_\mu.$$

Page 19 fixes the intent explicitly: **"to keep 1st order in derivatives, we must treat $\Omega_\mu$ and $q^\mu$ as separate independent variables."** So this is a *first-order (Palatini-type)* action with four independent fields:

$$\boxed{\;q^\mu,\quad \Omega_\mu,\quad \eta,\quad \chi\;}$$

(plus the conjugates $\eta^+,\chi^+$, varied independently). The Euler–Lagrange operator for each field $\psi$ is the page-34 equation

$$\Big(\tfrac{\partial\mathcal L}{\partial\psi_{;\mu}}\Big)_{;\mu}-\tfrac{\partial\mathcal L}{\partial\psi}=0.$$

**Prerequisite (review §4.7 / pages 27, 32):** $q^\mu=q^\mu_a\sigma^a$ carries a local Lorentz/tetrad redundancy that leaves $g^{\mu\nu}$ invariant. The variation $\delta/\delta q^\mu$ is only well-posed once that gauge is fixed; Sachs uses an *implicit* choice the notebook never names. Below, EOM 4 is stated up to this gauge freedom.

---

## 1. EOM for the matter fields — vary $\eta^{+}$ and $\chi^{+}$

Only the matter terms depend on $\eta^+$. The symmetrized kinetic term gives, after integrating the $\eta^+_{;\mu}$ piece by parts against the $(-g)^{1/2}$ measure,

$$\boxed{\;i\,q^\mu\eta_{;\mu} + \tfrac{i}{2}\,\frac{1}{(-g)^{1/2}}\partial_\mu\!\big[(-g)^{1/2}q^\mu\big]\,\eta = 0\;}$$

and identically for $\chi$ with $q^\mu\to\tilde q^\mu$. When $\Omega_\mu$ is the metric-compatible connection (the on-shell result of §3), the divergence term is exactly the spin-connection contribution that promotes $\partial_\mu\to{}_{;\mu}$, and the equation collapses to the clean **curved-tetrad massless Weyl equations**

$$\boxed{\;q^\mu\eta_{;\mu}=0,\qquad \tilde q^\mu\chi_{;\mu}=0.\;}$$

Page 17's option $\chi=\varepsilon\,\eta^*$ (or the space-reflected mass-coupled pair $\sigma^\mu\partial_\mu\varphi+im\zeta=0$) reintroduces a mass that links the two chiralities; that is the only place a rest mass enters.

### Reconciliation — ✅ already realized and tested (F50, F62)

This EOM is **not merely completable — the project already implements and tests it**, in Hamiltonian/lattice form. F62's curved-tetrad chiral Dirac Hamiltonian

$$i\,\partial_t\Psi=\big[c_\text{eff}(\mathbf x)\,\boldsymbol\alpha\cdot\hat{\mathbf p}+\sqrt{A(\mathbf x)}\,m\,\beta\big]\Psi,\qquad c_\text{eff}=c_0\sqrt{A/B}$$

is exactly the static-diagonal-metric reduction of $q^\mu\eta_{;\mu}=0$ (mass-coupled to its partner). The map is direct:

| Sachs page-34 object | Project realization |
|---|---|
| $q^\mu\eta_{;\mu}=0$, $\tilde q^\mu\chi_{;\mu}=0$ (two chiralities) | F62 D1: with $m=0$, two decoupled exact-QCA Weyl walks (**residual 0.0, bit-for-bit**) |
| rest mass linking $\eta\leftrightarrow\chi$ (page 17) | F46/F50 **rest leg** $\sqrt A\,m\,\beta$ — the proper-time clock |
| site-dependent $q^\mu$ (curved tetrad) | F50: kinetic leg $\to c_\text{eff}=c_0\sqrt{A/B}$, rest leg $\to\sqrt A$ |

So EOM 1–2 are the *one part of page 34 the project did carry forward* — just expressed as an exactly-unitary lattice stepper rather than a covariant PDE. **No divergence here.** F62 even tests the equivalence principle (mass-universal free-fall) and factor-2 deflection emerging from this equation.

---

## 2. EOM for the connection — vary $\Omega_\mu$

$\Omega_\mu$ appears (i) in $R$ through $K_{\mu\nu}$, and (ii) linearly in the matter terms through $\eta_{;\mu},\chi_{;\mu}$. The variation is

$$\frac{\delta\big[(-g)^{1/2}R\big]}{\delta\Omega_\mu} \;+\; \frac{\delta\mathcal{L}_M}{\delta\Omega_\mu}=0.$$

The gravitational piece is the spinor-form covariant-constancy (tetrad-postulate) condition; the matter piece is the **spin current**

$$J^{\mu}\sim \tfrac{i}{2}\big(\eta^+ q^\mu\,\delta\Omega\,\eta + \dots\big)\;\Rightarrow\; S^{\mu}{}_{ab}\propto \eta^+ q^\mu\sigma_{[ab]}\eta + (\eta\to\chi).$$

Setting the variation to zero yields the **Einstein–Cartan connection equation**: the antisymmetric part of $\Omega_\mu$ (torsion) is fixed *algebraically* by the spinor spin density,

$$\boxed{\;T^{\lambda}{}_{\mu\nu}\;\propto\;S^{\lambda}{}_{\mu\nu}(\eta,\chi).\;}$$

In the **absence** of spinor sources this forces torsion $=0$ and recovers eq. 3.88, $\Omega_\mu=-\tfrac14 q_\rho(\partial_\mu\tilde q^\rho+\Gamma^\rho_{\tau\mu}\tilde q^\tau)$ — i.e. the first-order and second-order formulations agree, and the independent $\Omega$ is *not* an extra dynamical degree of freedom.

### Reconciliation — ⚠️ collapses to torsion-free; the project never promotes $\Omega$ to a dynamical field

This is the first genuine fork. The project's emergent gravity (F52, F57) has **no fundamental connection sector at all**: the metric is the rest-leg lapse $A$ (sourced by mass density, F52) plus the kinetic-leg factor $B$ (F55), and the connection is whatever those imply — Levi-Civita, **torsion-free by construction**. F50/F62's tetrad-Dirac runs on exactly that torsion-free connection.

So the project's position on EOM 3 is: *it is consistent, but trivially so* — the project assumes the torsion-free branch from the outset, which is the source-free solution of Sachs' EOM 3. The Einstein–Cartan **spin-torsion** that the first-order variation would generate (torsion $\propto$ fermion spin density) is **absent from the project**. Logical verdict:

- If spin-torsion is negligible (the usual case — it is a four-fermion contact term suppressed by $G$), the two routes agree and nothing is lost.
- If it is ever made to matter, it would be a *new, untested prediction* outside the current lattice model — flagged, not adopted.

This matches the review's standing note that Sachs' first-order machinery is "sound but a specific choice not adopted."

---

## 3. EOM for the tetrad — vary $q^\mu$ (the Einstein equation)

$q^\mu$ appears in $R$, in the measure $(-g)^{1/2}$ via $g^{\mu\nu}=\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)/\sigma_0$, and in the matter kinetic terms. Up to the tetrad gauge-fixing of §0, the variation gives the **Einstein field equation in tetrad/quaternion form**

$$\boxed{\;G_{\mu\nu}[q,\Omega]\;=\;8\pi\,T_{\mu\nu}^{(\eta,\chi)},\qquad
T_{\mu\nu}=\tfrac{i}{2}\big(\eta^+q_{(\mu}\eta_{;\nu)}-\eta^+_{;(\mu}q_{\nu)}\eta\big)+(\eta\!\to\!\chi,\,q\!\to\!\tilde q).\;}$$

This is precisely page 18's $G_{\mu\nu}=8\pi T_{\mu\nu}$ (and the page-19 Hamiltonian $\mathcal H_E=\tfrac1{8\pi}(R_{00}-\tfrac12 g_{00}R)$) promoted to a full dynamical equation by the $q^\mu$-variation. In Sachs' first-order action the $R$ term is **fundamental**, so EOM 4 is Einstein's equation *by postulate*.

### Reconciliation — ⚠️ correct as an *effective* law, but the project derives $R$ instead of postulating it, and splits the single tensor equation in two

This is where the project's most developed findings live, and where it most sharply departs from page 34:

**(a) The Einstein–Hilbert term is induced, not fundamental.** F55–F57 show the lattice has *no* bare $R$ term; integrating out the F26 matter modes (coupled to the rest-leg potential $\Phi$ via the F52 density coupling $\int\Phi\rho$) generates a finite, correctly-signed $(\nabla\Phi)^2$ stiffness — the Sakharov mechanism, *exhibited* not assumed (F57: $\Pi_2=+0.061>0$). So Sachs' EOM 4 is the project's *effective* field equation, with

$$\frac{1}{16\pi G}=\Pi_2\;(\text{a BZ loop integral, F57}),\qquad G\propto\text{lattice spacing}^2\;(\text{F56/F59}),\qquad P_\text{pre}=\sqrt{2\pi\eta g_*},\;\eta_\text{Weyl}=\tfrac1{12}\;(\text{F61}).$$

Newton's constant is emergent — *not* a fundamental coupling multiplying a postulated $R$.

**(b) The single tensor equation resolves into the two-leg structure.** Sachs writes one $G_{\mu\nu}=8\pi T_{\mu\nu}$. The project (F50/F52/F55) finds that the lattice carries gravity on two distinct legs of the F46 Pythagorean mass triangle:

- **rest leg** (lapse $A$, the $G_{00}$/clock-rate sector) — sourced by mass density gives the **Newtonian** potential and the factor-1 redshift (F52);
- **kinetic leg** (spatial $B$) — must *also* be mass-sourced to supply the second half of light bending, recovering the **Einstein factor-2** (F55, F62-D2c eikonal $K\approx4$).

So "completing EOM 4" in the project means: the $G_{00}$ component is the F52 mass-sourced rest leg; the full $G_{\mu\nu}$ requires the F55 trace-reversal/kinetic-leg sourcing; and the coefficient is the F57/F59/F61 induced $1/G$. The project **derives** what Sachs **assumes**.

---

## 4. Verdict — is page 34 "completable," and what does it mean here?

**Mathematically: yes, fully and in closed form.** The four EOM are:

1. $q^\mu\eta_{;\mu}=0$ — curved-tetrad Weyl equation for $\eta$;
2. $\tilde q^\mu\chi_{;\mu}=0$ — same for $\chi$ (rest mass links the pair);
3. $T^\lambda{}_{\mu\nu}\propto S^\lambda{}_{\mu\nu}$ — Einstein–Cartan connection/torsion equation (torsion-free in the source-free branch);
4. $G_{\mu\nu}[q,\Omega]=8\pi T_{\mu\nu}^{(\eta,\chi)}$ — Einstein field equation.

**In the project's framework, "completing" it is mostly already done — and partly superseded:**

| EOM | Continuum result | Project status |
|---|---|---|
| 1, 2 (matter) | Weyl/Dirac in curved tetrad | ✅ **Realized & tested** as the F50/F62 exact-unitary lattice stepper. Direct match, no fork. |
| 3 (connection) | Einstein–Cartan torsion = spin density | ⚠️ **Trivialized**: project is torsion-free by construction; Sachs' spin-torsion is absent (consistent if negligible, a new prediction if not). |
| 4 (Einstein eq) | $G_{\mu\nu}=8\pi T_{\mu\nu}$, $R$ postulated | ⚠️ **Superseded/refined**: $R$ is *induced* (F55–F57), $G$ is emergent (F56/F59/F61), and the one tensor equation splits into the rest-leg/kinetic-leg structure (F52/F55). |

**Bottom line.** The page-34 variation is internally completable and reproduces standard first-order Sachs electrogravity. But the logical reconciliation shows the project has effectively *already answered three of the four EOM by other means* — implementing the matter equations exactly (F62), assuming away the connection sector (torsion-free), and **deriving rather than postulating** the gravitational field equation (Sakharov-induced EH, F55–F61). Carrying out Sachs' full $\delta R/\delta q^\mu$ algebra term-by-term would be a faithful textbook reproduction; it would not add new lattice physics, and it rests on the EM-as-connection identification the project rejects.

**If anything here is worth a new test:** the only genuinely *new* content the first-order route exposes is EOM 3's spin-torsion four-fermion term. A bounded check — does the project's torsion-free assumption cost anything at the lattice's fermion densities? — could be scoped as a small fork against F62, with the chiral-algebra caveat (hand-rolled $\sigma$-matrix functions, not numpy/scipy).

---

### Cross-references
- Source: `reference-research/physics-notes-complete.md` pp. 15–20, 33–34
- `physics-notes-complete-review.md` §4.7 (tetrad gauge-fixing), §5 (Sachs path not adopted)
- Findings: F46 (lattice mass triangle), F50 (gravity on the rest leg), F52 (mass-sourced lapse), F55 (kinetic-leg / factor-2), F56–F57 (induced EH), F59–F61 (induced $G$, $\eta=1/12$), F62 (time-domain Dirac-gravity)
- Plan: `ca-dirac-gravity-plan.md` (D3b nonlinear Sachs-Hamiltonian route remains open)
