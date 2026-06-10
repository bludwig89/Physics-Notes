# F106 — The ψ→K sourcing law: the dielectric is sourced by the fermion's own energy density, with no free coupling

**Date:** 2026-06-06 - 17:55
**Status:** Candidate finding — 5/5 checks PASS. E1 (coefficient identity) and E4/E5 (nonrel reduction, source identity) are **exact** (sympy zero residual / machine precision); E2/E3 (Poisson recovery of the canonical $K$) are lattice to $\le 2\%$ (finite periodic box). Closes the one remaining "posited input" in the F64 backreaction loop — the coupling and the source are both now derived.
**Module / test:** `tests/findings/test_F106_psi_K_sourcing.py` (~3 s; numpy + sympy, all real arithmetic).
**Results:** `test-results/F106_psi_K_sourcing.json`.
**Cross-references:** [[F64-em-connection-gravity]] (the dielectric this sources; D-EM5 conformal leg, D-EM8 dynamical Φ), [[F79-structural-newton-constant]] (the structural $G$ that fixes the coefficient), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$; mass = confined $(\mathbf E,\mathbf B)$ rotation), [[F62-dirac-gravity-dynamical-fork]] (the curved-Dirac stepper and the backreaction loop that fed in $|\Psi|^2$), [[F52-gravity-from-rest-leg-backreaction]] (the rest-leg source this generalises), [[F60-induced-G-channel-reconciliation]] (loop channel).

---

## 1. The gap this closes

F64 established **what** gravity is on the lattice — a single impedance-locked
dielectric $K(x)$ renormalising the $(\mathbf E,\mathbf B)$ rotation rule, with
$A=1/K$, $B=K$, canonical $K=e^{2GM/rc^2}$ ($AB\equiv1$, $\beta=\gamma=1$). What it
did **not** derive is **how the matter field ψ sources $K$**. The backreaction
runs (F62-D3a, F64-D-EM4/D-EM11) closed the loop *numerically* by the stand-in

$$\nabla^2\Phi = 4\pi G\,\rho,\qquad \rho = |\Psi|^2,\qquad K=e^{-2\Phi/c^2},$$

with two posited pieces: (i) the source is the **probability** density $|\Psi|^2$,
not an energy density; (ii) $G$ is a free knob in the solver. The 2026-06-06 audit
listed exactly this — "gravity dynamical in the F64 fork (Poisson background), $4\pi G$
by hand." This finding derives the sourcing law from the model's own structure,
removing both posits.

## 2. The derivation (three legs already in the model)

**Leg 1 — the source is ψ's energy density, and that energy *is* confined rotation (F26).**
A fermion at rest is not a separate "mass substance" sitting on the lattice: by F26,
mass **is** confined $(\mathbf E,\mathbf B)$ rotation. The thing ψ carries that can
load the lattice is therefore its **energy density** $T^{00}[\psi]$ — the expectation
of the F62 curved-Dirac Hamiltonian density,

$$T^{00}[\psi] = \Psi^\dagger\big[c_\text{eff}(\mathbf x)\,\boldsymbol\alpha\!\cdot\!\hat{\mathbf p} + \sqrt{A(\mathbf x)}\,m\,\beta\big]\Psi .$$

For a rest eigenstate ($\mathbf p=0$) this is $\sqrt A\,m\,|\Psi|^2$ → $m|\Psi|^2$ in
the flat limit (E5): **energy, not bare probability, is what the field hands to the
source.** Radiation and rest mass with equal $T^{00}$ source equally — the empirical
content of F64-D-EM3 (ratio $1.000$), and the reason the source is $T^{00}$ rather
than $\rho_\text{rest}$.

**Leg 2 — the lattice's response is the induced stiffness, and $G$ is structural (F79).**
$K$ is a reparametrization of the rotation rule, not a fundamental field, so it has
**zero tree stiffness** (F79-S3: the EM stress tensor is traceless, hands $K$ no bare
kinetic term). Its entire stiffness is the induced/loop response — the Sakharov term
whose coefficient F79 fixes with no free parameter:

$$\frac1G = 2\pi\,\eta\,g_*\sqrt d\;\frac{\hbar}{a^2c^3} = 8\pi\sqrt3\,\frac{\hbar}{a^2c^3},\qquad
\big(\eta=\tfrac1{12},\ g_*=48,\ d=3\big).$$

The static weak-field reduction of the induced Einstein equation
$G_{\mu\nu}=\tfrac{8\pi G}{c^4}T_{\mu\nu}$ is Poisson with source $T^{00}$, the $4\pi$
being the lattice-exact 3-D Green's function (F58/D-EM10).

**Leg 3 — the impedance lock converts Φ to $\ln K$ (F64-D-EM5).**
The dielectric carries **both** metric legs as one scalar: $\sqrt A = e^{-u}$,
$K=B=e^{2u}$ with $u=-\Phi/c^2$, so $\ln K = -2\Phi/c^2$. The factor **2** is the
$AB\equiv1$ two-leg lock — the same lock that gives factor-2 light bending from one
field.

**Assembling.** $\nabla^2\ln K = -\tfrac{2}{c^2}\nabla^2\Phi = -\tfrac{2}{c^2}\cdot\tfrac{4\pi G}{c^2}T^{00}$:

$$\boxed{\;\nabla^2\ln K(\mathbf x) = -\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x)\;}
\qquad\text{(D-PK)}$$

Substituting F79's $G$ and $c_\text{lat}=1/\sqrt3$ (F26) collapses the coefficient to
**pure lattice quantities — no $G$, no $4\pi$, no free coupling**:

$$\boxed{\;\nabla^2\ln K = -\frac{a^2\,c_\text{lat}}{\hbar\,c}\,T^{00}[\psi]\;}
\qquad\Big(\tfrac{8\pi G}{c^4}=\tfrac{a^2 c_\text{lat}}{\hbar c},\ \text{exact}\Big).$$

The matter field sources the *log* of its own dielectric through its energy density,
with a stiffness that is just the cell area $a^2$ over $\hbar c$ times the rotation
rate $c_\text{lat}$. This is the elegant-design endpoint: the lattice bends its
rotation rule in proportion to the rotation energy already confined in it.

## 3. Verification (5/5)

| check | statement | result | status |
|---|---|---|---|
| **E1** | coefficient identity $8\pi G/c^4 = a^2 c_\text{lat}/(\hbar c)$, $c_\text{lat}=1/\sqrt3$ | residual $=0$ (sympy) | **PASS (exact)** |
| **E2** | Gaussian $T^{00}$ through D-PK → far-field $\ln K = 2GM/rc^2$ | rel residual $0.023$ | PASS (grid) |
| **E3** | slope $\langle\ln K\cdot r\rangle = 2GM/c^2$, $M=\int T^{00}/c^2$ | $0.04003$ vs $0.04$ ($6\times10^{-4}$) | PASS |
| **E4** | nonrel $T^{00}=mc^2|\Psi|^2$ ⇒ D-PK $=$ code's $4\pi G_\text{eff}|\Psi|^2$, $G_\text{eff}=2Gm$ | identity holds | **PASS (exact)** |
| **E5** | rest eigenstate $T^{00}=m|\Psi|^2$ (energy is the source) | ratio $1.0$ | **PASS** |

E3 is the sharp one: sourcing an arbitrary Gaussian energy lump through D-PK
reproduces the canonical $K=e^{2GM/rc^2}$ with $M$ read off as $\int T^{00}/c^2$ to
$6\times10^{-4}$ — the $2\%$ in E2 is periodic-box discretisation of the field away
from the fitted slope, not a coefficient error.

## 4. What is derived vs posited

- **Derived (new):** the sourcing law D-PK itself — *that* the source is $T^{00}[\psi]$
  (Leg 1, F26), *that* the coupling is $8\pi G/c^4$ with $G$ structural (Leg 2, F79),
  and *that* the Φ→$K$ conversion carries the factor 2 (Leg 3, F64-D-EM5). The
  assembled coefficient $a^2c_\text{lat}/(\hbar c)$ is **free of any fitted constant**.
  The previous loop's two posits ($\rho=|\Psi|^2$, free $G$) are now the nonrelativistic
  limit (E4) of a derived law.
- **Still posited (inherited, bounded):** the one SI ruler $a$ (audit C.1, unavoidable —
  one length cannot come from pure numbers); the spin-1 gauge contribution to $g_*$
  (F79's flagged $\sqrt{\cdot}$ correction). Neither is a *new* input; both predate F106.
- **Honest scope:** D-PK is the static / slow-matter (Poisson) reduction. Because the
  impedance lock $AB\equiv1$ makes the single scalar $K$ carry both metric legs, the
  spatial-leg ("pressure") weight that GR needs for factor-2 bending is supplied
  automatically — so sourcing from $T^{00}$ alone is correct for the dielectric, and
  D-EM3/D-EM7 already confirmed the resulting $K_\text{bend}\to4$. A fully covariant
  $T_{\mu\nu}$-sourced, finite-$c_g$ (D-EM8) version is the natural next build.

## 5. Consequence for the engine

This is the analytic warrant for replacing `ρ = |Ψ|²` with `ρ_E = T⁰⁰[ψ]/c²` in the
F64 backreaction loop (`run_backreaction_dielectric`) and dropping `G` as a call
argument in favour of the F79 closed form. That is the "merge F64 dynamical Φ into the
production engine" item (audit B.2 #1) with its physics now closed rather than posited.
The relativistic energy density also fixes a real defect of the $|\Psi|^2$ proxy: a fast
packet then gravitates by its *total* energy (kinetic included), as F64-D-EM3 demands,
where bare probability density would have under-counted it.

## 6. Provenance

- New content: the three-leg assembly of D-PK, the lattice-only coefficient
  $a^2c_\text{lat}/(\hbar c)$, and the identification of $T^{00}$ (not $|\Psi|^2$) as the
  source via F26.
- Reuses: F26 ($c_\text{lat}=1/\sqrt3$, mass = confined rotation), F79 (structural $G$,
  zero-tree-stiffness ⇒ loop channel), F64-D-EM5 ($\ln K=-2\Phi/c^2$ impedance leg),
  F62 (curved-Dirac energy density and the backreaction loop), F58/D-EM10 (the $4\pi$
  lattice Green's function).
- Verification: `tests/findings/test_F106_psi_K_sourcing.py` (2026-06-06 - 17:55, 5/5 PASS),
  results `test-results/F106_psi_K_sourcing.json`.
