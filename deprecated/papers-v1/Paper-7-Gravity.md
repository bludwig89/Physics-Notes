# Paper VII — Gravity as a Lattice Dielectric: An Impedance-Matched Renormalisation of the Field Rotation Rate, GR-Identical PPN, and a Structural Newton Constant

**B. Ludwig**
*Independent researcher*

*Series: "A Universe in a Bottle" — Paper VII of X. Builds on Paper I (light as rotation rate), Paper II (the cell-size co-certification), and completes the four-interaction set (IV–VII).*

---

## Abstract

We present gravity in the BCC quantum-cellular-automaton model as a single, impedance-matched **lattice dielectric** $K(\mathbf x)$: a position-dependent renormalisation of the $(\mathbf E,\mathbf B)$ rotation rule that Paper I identified with the speed of light. With the canonical index $K=\exp(2GM/rc^2)$, metric legs $A=1/K$, $B=K$ obeying the exact reciprocal lock $AB\equiv1$, the model reproduces general relativity at the post-Newtonian level: $\beta=\gamma=1$, Mercury perihelion advance $42.98''$/century, and full Einstein factor-2 light bending ($4GM/bc^2$). A single scalar achieves what a single scalar generically cannot — simultaneous factor-1 redshift and factor-2 deflection — because the reciprocal lock keeps the lattice impedance $\sqrt{\mu/\varepsilon}=1$ exactly, so the rotation stays a *proper* rotation with no scalar contamination. We derive the dielectric placement $\varepsilon=\mu=K$ from the proper-rotation requirement plus the conformal invariance of source-free Maxwell, show that light dynamically bends light (the rest-mass route gives zero), promote the potential to a causal dynamical field, and — crucially — **free Newton's constant from the Sakharov premise**: the gravity field carries zero tree stiffness because the dominant lattice stress tensor is traceless, so the induced (loop) channel is forced as a theorem, giving the closed form $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ and the parameter-free prediction $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.598$. Sixteen field-level and dynamical tests pass.

---

## 1. Introduction

Gravity is the interaction least like the others: it couples universally, it is geometric in general relativity (GR), and its quantisation is unsolved. On a fixed lattice one cannot literally curve space, so a faithful model must encode the metric some other way. Paper I provides the handle: the speed of light is the rotation rate of the real field pair, $c_\text{lat}=d\Omega/d|\mathbf k|$. If that rate is made *position-dependent*, light slows in a well and bends — gravity becomes a renormalisation of the rotation rule itself.

This is the polarizable-vacuum / dielectric line of Puthoff and of Ostoma–Trushyk, and it is native to the present model because (Paper II) mass itself is confined $(\mathbf E,\mathbf B)$ rotation — there is no separate "mass substance" to source a metric from, only confined electromagnetic energy. The result is **one field, one source** (total field energy), in contrast to the two-leg, rest-mass-sourced metric that the earlier emergent-gravity forks of this project required for factor-2 bending.

---

## 2. The dielectric and its observables

We write the static isotropic metric as $ds^2=-A\,c_0^2dt^2+B\,\delta_{ij}dx^idx^j$, with photon coordinate speed $c_\text{eff}=c_0\sqrt{A/B}$ and eikonal index $n=c_0/c_\text{eff}=\sqrt{B/A}$. With $u\equiv GM/(rc^2)=-\phi/c^2$, the two solar-system observables are the leading $u$-slopes

$$
Z\equiv-\frac{d\sqrt A}{du}\bigg|_0\ (\text{GR: }1),\qquad
K_\text{bend}\equiv2\frac{dn}{du}\bigg|_0\ (\text{GR: }4,\ \text{Newton: }2).
\tag{2.1}
$$

### 2.1 One scalar gives both — the reciprocal lock

The decisive go/no-go: can one scalar give factor-1 redshift *and* factor-2 bend simultaneously? Three single-scalar placements (exact series):

| placement | $A,B$ | $Z$ | $K_\text{bend}$ | impedance const? | passes GR? |
|---|---|---|---|---|---|
| **dielectric** | $A=1/K,\ B=K$ | **1** | **4** | **yes** ($=1$) | **yes** |
| clock-only (rest leg) | $A=(1-u)^2,\ B=1$ | 1 | 2 | no | no |
| refractive-only (Gordon) | $A=1,\ B=(1+u)^2$ | 0 | 2 | no | no |

Only the dielectric passes both. The structural reason is the **reciprocal lock $AB=1$**: a genuine dielectric scales $\varepsilon=\mu=K$ together, so the impedance $\sqrt{\mu/\varepsilon}=1$ is exactly $u$-independent — the $(\mathbf E,\mathbf B)$ amplitude ratio is preserved and the rotation stays a *proper* rotation with no scalar contamination. Fixing $K$ by factor-1 redshift ($\sqrt A=K^{-1/2}=1-u$) then forces $n=\sqrt{B/A}=K=1+2u+O(u^2)$, hence $K_\text{bend}=4$ — Einstein bending from one field.

### 2.2 Radiation gravitates as rest mass

The empirically sharp discriminator: two equal-energy sources — a rest-mass blob and a massless spherical shell of standing $(\mathbf E,\mathbf B)$ field energy — bend probe rays equally under the dielectric coupling (ratio $1.00002$), because both carry the same monopole. Under the rest-mass coupling the massless shell sources **nothing**. This zero-versus-Einstein split is the model's sharpest gravitational prediction, and it is realised dynamically: a 2D Maxwell pulse propagating through a dielectric well sourced by a *massless* field-energy lump bends with full factor-2, where the rest-mass route gives zero (light bends light).

---

## 3. Deriving the dielectric placement

The one posited input — *that* the renormalisation enters as a genuine dielectric rather than as a clock-only or refractive-only scalar — is derived in four exact steps from the proper $(\mathbf E,\mathbf B)$-rotation law (Paper I) plus a lattice confirmation:

1. **Plébański equivalent medium.** The equivalent medium of a static isotropic metric is $\varepsilon=\mu=\sqrt{B/A}=K$.
2. **Conformal invariance.** Source-free Maxwell is conformally invariant in $3+1$D, so the EM sector sees only the conformal class; it fixes $\varepsilon=\mu=K$ but is blind to the conformal factor.
3. **Impedance + index.** Demanding a proper rotation ($Z=\sqrt{\mu/\varepsilon}=1$, no scalar component) *and* index $n=\sqrt{\varepsilon\mu}=K$ has the unique solution $\varepsilon=\mu=K$.
4. **Reciprocal lock.** The conformal factor — the one thing EM is blind to — is supplied by the measured factor-1 redshift $\sqrt A=1-u$, giving $A=(1-u)^2$, $B=K$, $AB=1$.

A 1D Yee finite-difference simulation confirms it: the impedance-matched dielectric is reflectionless at an index step (to the grid floor), while refractive-only and clock-only placements reflect at the Fresnel value. The reflected backward wave *is* the scalar contamination a proper rotation forbids — so "position-dependent rotation that stays a proper rotation" forces the dielectric. Conceptually, the conformally-invariant EM sector carries both metric legs as one scalar (answering the earlier two-leg route's open problem of sourcing the spatial leg), and is blind only to the conformal factor, which is the gravitational redshift / clock rate.

---

## 4. Strong field: PPN and the canonical exponential

Exact post-Newtonian analysis of $g_{tt}=-A$, $g_{ij}=B\delta_{ij}$:

| metric | $\beta$ | $\gamma$ | light bend/GR | Mercury ″/cy |
|---|---|---|---|---|
| redshift-fixed $K=(1-u)^{-2}$ | $\tfrac12$ | $1$ | $1$ | **50.1** (excluded) |
| **exponential $K=e^{2u}$** | $1$ | $1$ | $1$ | **42.98** |
| Schwarzschild (ref) | $1$ | $1$ | $1$ | $42.98$ |

Light deflection depends only on $\gamma=1$, so the dielectric passes the bending test exactly. But perihelion advance depends on $\beta$: the naive linear dielectric $K=(1-u)^{-2}$ has $\beta=\tfrac12$, predicting Mercury $50.1''$/cy — a $16.7\%$ excess excluded by the MESSENGER bound. The EM-sector derivation fixes $K$ only to linear order; the second-PPN (Mercury) test selects the nonlinear completion

$$
\boxed{\;K=e^{2GM/rc^2},\qquad A=1/K,\ B=K,\ AB\equiv1,\;}
\tag{4.1}
$$

which restores $\beta=\gamma=1$ (GR-identical) and converges on exactly the Puthoff polarizable-vacuum form — now *derived* by impedance matching rather than assumed. The two forms agree at $O(u)$ ($(1-u)^{-2}=1+2u+3u^2+\cdots$ vs $e^{2u}=1+2u+2u^2+\cdots$), so all weak-field results are unchanged.

A causal dynamical completion is provided: promoting the potential to a field with a kinetic term, $\Box\Phi=-4\pi G\rho$, gives a static Poisson limit, retarded propagation at the graviton speed $c_g$, and energy conservation — i.e. dielectric gravitational waves. The dynamical Dirac wave-packet battery (equivalence principle, redshift, factor-2 deflection, backreaction) reproduces every result of the earlier two-leg emergent-gravity module using one field equation instead of two.

---

## 5. Newton's constant from lattice structure

The last posited input, the $4\pi G$ coupling, is fixed by recognising what the gravity field *is*.

### 5.1 The pivot: $K$ is a conformal factor, not a fundamental field

By the derivation of §3, $K$ is the conformal factor the EM action is blind to. A conformal (Weyl) rescaling couples to matter through the *trace* of the stress tensor, $\delta S=\int\sqrt g\,T^\mu{}_\mu\,\delta\sigma$. The source-free electromagnetic stress tensor is **traceless in $3+1$D**, $T^\mu{}_\mu^\text{(EM)}=0$ (verified to $3.6\times10^{-15}$ on random fields). Therefore the conformal factor has **no source and no tree action** — the gravity field has *zero tree stiffness*. There is no fundamental graviton on this lattice whose bare kinetic term could set $G$; $K$ is a derived reparametrisation, and its entire stiffness is the induced (loop) response of the fundamental $(\mathbf E,\mathbf B)$/spinor modes.

### 5.2 The loop channel is forced

The two candidate stiffnesses scale differently in $c_\text{lat}$: the tree (fundamental-graviton) channel as $c_\text{lat}^{+2}$, the induced (loop) channel as $c_\text{lat}^{-1}$, a gap of $c_\text{lat}^3$. Since §5.1 shows there is no tree term to measure, the physical coupling is the loop channel,

$$
\frac{1}{16\pi G}\propto\frac{1}{c_\text{lat}}=\sqrt d.
\tag{5.1}
$$

### 5.3 Every input is structural; the closed form

| input | value | fixed by |
|---|---|---|
| $c_\text{lat}$ | $1/\sqrt d$ | BCC rotation rule (Paper I) |
| $\eta_\text{Weyl}$ | $\tfrac1{12}$ | Seeley–DeWitt heat-kernel coefficient |
| $g_*$ | $48=16\times3$ | $O_h$ generation theorem (Paper VIII) $\times$ anomaly-free content |

The mode count $g_*$ is the decisive upgrade: the generation count $3$ is a theorem about the BCC point group ($\dim T_{1u}$, no 4-dim single-valued irrep), so with the anomaly-free 16-Weyl content per generation ($L{=}2,e_R{=}1,Q{=}6,u_R{=}3,d_R{=}3,\nu_R{=}1$), $g_*=48$ is a count of the lattice's own protected normal modes, not a matter-content input. Assembling the Sakharov integral gives the closed form

$$
\boxed{\;\frac{1}{G}=2\pi\,\eta\,g_*\sqrt d\,\frac{\hbar}{a^2c^3},\qquad
G=\frac{a^2c^3}{8\pi\sqrt3\,\hbar},\;}
\tag{5.2}
$$

with the parameter-free coefficient $2\pi\eta g_*\sqrt d=2\pi\cdot\tfrac1{12}\cdot48\cdot\sqrt3=8\pi\sqrt3=43.531$. The dimensionless content the lattice predicts is

$$
\frac{a}{\ell_P}=\sqrt{2\pi\eta g_*}\,d^{1/4}=\sqrt{8\pi}\,3^{1/4}=6.5978,
\tag{5.3}
$$

with tick $\tau/t_P=\sqrt{8\pi}\,3^{-1/4}=3.809$ and the $d$-independent invariant $\sqrt{ac\tau}/\ell_P=\sqrt{8\pi}=5.013$. Anchoring $a$ at $\ell_P$ returns $G=6.6743\times10^{-11}$ SI to $3\times10^{-8}$ (CODATA round-off), confirming the algebra.

### 5.4 The one honest limit

No theory yields a dimensionful $G$ from pure numbers — that needs one ruler. The lattice predicts the *dimensionless* $a/\ell_P$ (equivalently $8\pi\sqrt3$). To state $G$ in SI one must anchor the single length $a$. The genuinely independent anchor is a **measured fermion mass** via the lattice-mass map (Paper III), which references no Planck length; under it $G$ becomes an output of particle data, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ with $a$ read from, e.g., the electron mass. That is the sharpest "derive $G$" the framework supports, and it is falsifiable through (5.3). The spin-1 gauge contribution to $g_*$ is a bounded, mild $\sqrt{\cdot}$ correction.

---

## 6. Cell-size co-certification with the photon

The cell size that (5.3) forces, $a\approx6.2\times10^{-35}$ m $\approx3.8\,\ell_P$ (one generation), is the same cell size at which the *chiral* photon was excluded by polarimetry by $\sim14$ decades. The **paired photon** (Paper II) removes that birefringence prediction entirely, so the gravity-fixed cell size now simultaneously (i) reproduces $G$ and (ii) survives all astrophysical vacuum-birefringence bounds, with the Lorentz-violation cutoff at $E_\text{LV}\sim2.9\times10^{19}$ GeV. Papers II and VII thus co-certify a single cell size — a consistency gain that does not touch any dimensionless prediction.

---

## 7. Verification summary

| Result | Section | Residual / status |
|---|---|---|
| Single-scalar viability ($Z=1$, $K_\text{bend}=4$) | §2.1 | exact; ratio to rest-leg $=2.000$ |
| Radiation gravitates as rest mass | §2.2 | $1.00002$ (rest-leg: $0$) |
| Dielectric placement derived (reflectionless) | §3 | $R=0.009$ (Fresnel $0.111$ otherwise) |
| Absolute 3D bend $K_\text{bend}\to4$ | §4 | $4.0015$ at $u=10^{-4}$ |
| PPN $\beta=\gamma=1$ (Mercury $42.98''$) | §4 | exact (vs $50.1''$ for linear) |
| EM stress tensor traceless | §5.1 | $3.6\times10^{-15}$ |
| Channel exponents $(2,-1,-3)$ | §5.2 | exact |
| $g_*=48$; $a/\ell_P=\sqrt{8\pi}3^{1/4}$ | §5.3 | exact; $G$ consistent to $3\times10^{-8}$ |

Sixteen field-level and dynamical tests pass. Underlying findings: F64 (EM-connection / dielectric gravity, D-EM1–D-EM11), F79 (structural Newton constant), F55–F62 (the superseded two-leg route and its lessons), F69 (cell-size co-certification).

---

## 8. Discussion

Gravity in this model is not a new field but a modulation of the field already present: the rotation rate that *is* the speed of light. One impedance-matched scalar reproduces GR's weak- and strong-field phenomenology, with the reciprocal lock $AB=1$ doing the work that two independently-sourced metric legs did in the earlier route. The deepest result is that Newton's constant is not free: because the gravity field is a conformal reparametrisation with no tree stiffness, $G$ is the lattice's induced dielectric stiffness against bending its own rotation rule, fixed (up to one ruler) by $c_\text{lat}=1/\sqrt3$, $\eta=\tfrac1{12}$, and the generation theorem $g_*=48$.

Open items, all bounded: the spin-1 gauge contribution to $g_*$; a full strong-field battery on the exponential $K$ against exact Schwarzschild geodesics; a two-body / gravitational-wave sector; and 3D dynamical light-bends-light. The lineage is Sachs' electrogravity (the notebook's starting point), Puthoff's polarizable vacuum, and Ostoma–Trushyk.

---

## References

1. H. E. Puthoff, "Polarizable-vacuum (PV) approach to general relativity," *Found. Phys.* **32**, 927 (2002).
2. T. Ostoma, M. Trushyk, "Electromagnetic Quantum Gravity" (1999).
3. A. D. Sakharov, "Vacuum quantum fluctuations in curved space and the theory of gravitation," *Dokl. Akad. Nauk SSSR* **177**, 70 (1967) — induced gravity.
4. M. Sachs, *General Relativity and Matter* (Reidel, 1982) — electrogravity unification (notebook source, "Sachs Made Easy").
5. C. M. Will, *Theory and Experiment in Gravitational Physics* (Cambridge, 2018) — PPN formalism.
6. Project findings: F64 (dielectric gravity), F79 (structural $G$), F55–F62 (two-leg route), F69 (cell-size co-certification).

*Companion papers: I (light as rotation), II (photon / cell size), VIII (generation count / $g_*$).*
