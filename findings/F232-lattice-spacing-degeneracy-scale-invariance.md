# F232 — L3: pinning the lattice spacing $a$ independently of mass — the light-deflection route is **degenerate** (a scale-invariance theorem), and the mass-independent pin is the F79 $G$-match, not lensing

> **Numbering note:** highest committed finding at write time was F228; concurrent sessions may collide — re-checked, this is **F232**.

**Date:** 2026-07-02 - 16:20
**Status:** Confirmed (negative / degeneracy result) — 5/5 checks PASS. Executes the F83 open follow-up #1 (open line 141 of `docs/roadmaps/next-steps.md`): combine the F46 rest-leg relation with the absolute light-deflection coefficient to pin $a$ without a mass. The attempt **closes negative**: the deflection coefficient is exactly $-4$, dimensionless and $a$-independent (F107 L4a), so it supplies **zero** constraint on $a$ — the F83 $(a,m_\text{lat})$ ray is unbroken. The general reason is a **scale-invariance theorem**: no dimensionless, mass-independent lattice observable can fix a length. The third input that *does* break the degeneracy is the **dimensionful** gravitational coupling $G$ (equivalently $\ell_P$), which pins $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ via F79 — a mass-independent pin, but the $G$-match, not the lensing route the follow-up proposed.
**Module:** none new — analytic identity on F83 ($\triangle$) + F79 (structural $a/\ell_P$) + F107 (L4a exact $-4$); real-arithmetic quadrature guard.
**Script:** `tests/findings/test_F232_lattice_spacing_degeneracy.py` (<1 s; stdlib + numpy real quadrature only — no chiral transforms)
**Results:** `test-results/F232_lattice_spacing_degeneracy.json`
**Cross-references:** [[F83-fix-lattice-spacing-from-fermion-mass]] (the $(\triangle)$ relation + $(a,m_\text{lat})$ degeneracy this closes; its open follow-up #1 is the literal target), [[F107-canonical-a-adoption-L4-grb-gate]] (L4a: $K_\text{bend}=-4$ **exact at all field strengths**, and the demotion of F83 to a consistency check; the $\sqrt d$ lives in the SI map, *not* in the dimensionless coefficient), [[F79-structural-newton-constant]] (the mass-independent pin: $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$, coefficient $8\pi\sqrt3$, and the "one ruler no lattice can supply" limit), [[F64-em-connection-gravity]] (canonical $K=e^{2u}$, $\ln K=2u$ Coulombic), [[F46-pythagorean-lattice-mass]] ($\Omega_\text{rest}=\arcsin m_\text{lat}$), F10 (the $\sqrt d$ lightcone $a/\tau=c\sqrt d$).

---

## 1. The target and the two constraints

F83 established the exact **rest-leg (triangle) relation**, one equation in two unknowns:

$$a \;=\; \sqrt d\,\arcsin(m_\text{lat})\,\bar\lambda_C ,\qquad \bar\lambda_C=\frac{\hbar}{m_\text{phys}c}\tag{$\triangle$}$$

A single measured fermion mass therefore fixes only the **ray** $a(m_\text{lat})$, not a point (F83 §2). The proposed second constraint (F83 follow-up #1) was the **absolute light-deflection coefficient**

$$\Delta\theta=\frac{4GM}{b\,c^2},$$

flagged in Finding 10 as possibly carrying "an explicit $\sqrt d$" that could break the degeneracy. This finding tests exactly that combination.

## 2. The lensing coefficient is exactly $-4$ and $a$-independent (the negative)

For the canonical dielectric $K=e^{2u}$, $u=GM/(rc^2)$ (F64 D-EM5), the log-index is exactly Coulombic, $\ln K=2GM/(rc^2)$, so the straight-ray eikonal deflection is

$$\alpha=\int_{-\infty}^{\infty}\partial_b[\ln K]\,dx=-\frac{4GM}{b\,c^2}\qquad\textbf{exactly, at every field strength}$$

(F107 L4a, sympy). The coefficient $-4$ is a **pure number**: it contains no lattice spacing. The verification quadrature returns $-4.0000$ for the cell size $a$ swept across **47 decades** ($a/\ell_P\in\{1,\,6.598,\,10^{17},\,10^{-30}\}$) — the deflection observable is manifestly scale-free (**T3**). The Finding-10 $\sqrt d$ warning was resolved by F107: the $\sqrt d$ lives entirely in the **SI map** (it is already inside F79's $8\pi\sqrt3$), *not* in the dimensionless bending coefficient. 

**Consequence.** Adding $\Delta\theta$ to $(\triangle)$ adds no equation in $a$: the pair is invariant under the rescaling

$$a\to s\,a,\qquad \arcsin(m_\text{lat})\to \arcsin(m_\text{lat})/s\quad(\text{measured }m_\text{phys}\text{ fixed}),$$

and the deflection coefficient is untouched. The census (**T4**) confirms a one-parameter family of lattices ($m_\text{lat}=10^{-30}\dots0.5$, i.e. $a/\ell_P\sim10^{-8}\dots10^{22}$) all reproduce the electron mass *and* the same $-4$ bending. **The light-deflection route is degenerate.**

## 3. The scale-invariance theorem

The negative is not specific to lensing. State it generally:

> **Theorem (no dimensionless observable pins $a$).** Any lattice observable that is (i) dimensionless and (ii) independent of the measured masses is invariant under the cell rescaling $a\to s\,a$ (with the tick $\tau=a/(c\sqrt d)$ scaling with it, so $c_\text{lat}=1/\sqrt d$ is held). It therefore carries **no information about the absolute cell size** $a$.

The factor-$4$ deflection, PPN $\beta=\gamma=1$ (F64/F107), the Shapiro ratio, the birefringence coefficient — all are dimensionless and mass-blind, hence all are blind to $a$. Pinning $a$ requires an input that carries a **length or mass dimension**. Two such inputs exist:

1. a measured **fermion mass** — but F83 proved one mass gives only the ray $(\triangle)$ (one dimensionful datum, one equation short);
2. the **gravitational coupling** $G$ — a second dimensionful datum.

## 4. The mass-independent pin that works: the F79 $G$-match

The $G$-match is the productive route. F79 derives the *dimensionless* ratio structurally,

$$\frac{a}{\ell_P}=\sqrt{2\pi\eta g_*}\;d^{1/4}=\sqrt{8\pi}\,3^{1/4}=6.59782\quad(\eta=\tfrac1{12},\;g_*=48,\;d=3),$$

so with $\ell_P=\sqrt{\hbar G/c^3}$ the cell is pinned **without any fermion mass**:

$$\boxed{\,a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=1.06638\times10^{-34}\ \text{m}\,}\qquad(\textbf{T5}).$$

The self-consistency is exact: $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ with $a=k\ell_P$, $k=\sqrt{8\pi}3^{1/4}$, is the **identity** $k^2/(8\pi\sqrt3)\equiv1$ (**T2**, residual $10^{-16}$) — i.e. the $G$-match fixes the pure number $a/\ell_P$ and inherits the metre from $\ell_P$ (from $\{\hbar,G,c\}$). This is the honest "one ruler no lattice can supply" limit of F79/F107, made precise as the answer to L3.

**So the mass-independent pin the prompt asked for exists — it is the $G$-match, delivering $a=6.598\,\ell_P$ — but it is a *dimensionful gravitational* input, not the *dimensionless* lensing coefficient.** Confronting the two candidate cells: F79's $6.598\,\ell_P$ supersedes the older minimal-content $3.81\,\ell_P$ (F61), and F107's GRB gate independently excludes anything near the F83 top-quark ceiling ($1.9\times10^{17}\ell_P$) by $\sim9$ decades, leaving $6.598\,\ell_P$ as the sole standing value.

## 5. What is derived vs. what remains

**Established (this finding):** the light-deflection route to $a$ is **degenerate** — coefficient $-4$ exact and $a$-independent over 47 decades (T3), so $(\triangle)$+lensing leaves $a$ free (T4); the general **scale-invariance theorem** (no dimensionless mass-blind observable pins $a$, §3); the working pin is the F79 $G$-match, an *identity* given $\{\hbar,G,c\}$ (T2/T5), yielding $a=6.598\,\ell_P$.

**The third input, named:** a **dimensionful gravitational measurement** — $G$ (equivalently $\ell_P$). It is not "another coefficient with a stray $\sqrt d$"; it is the metre-carrying constant, and it is exactly what F79/F107 already use.

**Unchanged:** the one honest limit is dimensional and shared by any theory — $a/\ell_P$ is derived; the metre enters once, through $\ell_P$. The F83 follow-up #1 is hereby closed (negative/degenerate); "not-yet-met #7" (SI identification of $a$) is answered: adopted via the $G$-match (F107), with L3 supplying the degeneracy proof that no massless observable could have done it.

## 6. Check summary (`test_F232_lattice_spacing_degeneracy.py`, 2026-07-02 - 16:20)

| # | Statement | Result | Status |
|---|---|---|---|
| T1 | $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79 structural) | $6.59782$ | PASS |
| T2 | $G$-match $k^2/(8\pi\sqrt3)\equiv1$ (a scales with $\ell_P$) | $1.0$ ($10^{-16}$) | PASS |
| T3 | eikonal coeff $=-4$, $a$-independent over 47 decades | $-4.0000$ | PASS |
| T4 | $(\triangle)$ + $a$-free lensing $\Rightarrow$ $a$ undetermined (ray) | family | PASS |
| T5 | third input $=G$: $a=6.598\,\ell_P=1.066\times10^{-34}$ m | resid $10^{-4}$ | PASS |

**Overall 5/5 PASS** (<1 s).

## 7. Provenance

- **New content:** the explicit degenerate close of the $(\triangle)$+lensing combination (F83 follow-up #1); the scale-invariance theorem (§3); the observation that the $G$-match is an *identity* (T2) and therefore pins $a/\ell_P$, not the metre.
- **Reused:** F83 ($\triangle$, degeneracy, ceiling), F107 (L4a exact $-4$, GRB gate, F83 demotion), F79 ($a/\ell_P=\sqrt{8\pi}3^{1/4}$, $8\pi\sqrt3$), F64 ($K=e^{2u}$), F46 ($\arcsin m_\text{lat}$). Constants: CODATA 2018 ($\ell_P$, $\hbar c=197.327$ MeV·fm), PDG electron mass.
- **Verification:** `tests/findings/test_F232_lattice_spacing_degeneracy.py` (2026-07-02 - 16:20, 5/5 PASS), results `test-results/F232_lattice_spacing_degeneracy.json`. Real arithmetic only — numpy-safe.
