# F288 — Structure formation on the lattice: the model's gravity law fixes linear growth with **zero free functions** where the EFT of dark energy has two, giving $\gamma_g=6/11$ exactly, a Meszáros solution with a literal-zero residual, and an S8 falsifier that cannot be tuned away

**Date:** 2026-08-05 - 10:35
**Status:** Confirmed — **13/13 checks PASS**. Four legs are **exact-algebraic** (S1 zero linear slip, S2 $\mu\equiv1$ with $\partial_k\mu\equiv0$, D1 $\gamma_g=6/11$, D2 the Meszáros solution — all sympy literal zeros); D3/D4/D5/B1/B2 are **quantitative**; S3 is a **constraint count**; C1 is a **built-in control** that proves the numeric legs can go red.
**Module:** `src/casim/engine/interactions/cosmology_growth.py`
**Registry record:** `F288-structure-formation-growth` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`, `entry: run`)
**Results:** `test-results/F288_structure_formation.json`
**Prompt:** `docs/roadmaps/k11-structure-formation-prompt.md`
**Attacks:** `docs/status/completeness-2026-08-04.md` row **K11** (*structure formation / $\sigma_8$*), graded **ABSENT** — *"zero hits, on four separate keyword sweeps"* — one of only two cosmology rows with no entry point at all.
**Cross-references:** [[F182-friedmann-pressure-cosmology]] / [[F188-multicomponent-lcdm-cosmology]] (the background this grows perturbations on), [[F178-gravity-full-tensor-adoption]] (the adopted law), [[F106-psi-K-sourcing-derivation]] (the static weak-field reduction that supplies $\mu$), [[F64-em-connection-gravity]] ($AB\equiv1$, D-EM9, the impedance match that supplies zero slip), [[F79-structural-newton-constant]] / [[F284-rigid-lattice-conformal-expansion]] ($G$ structural on a rigid substrate $\Rightarrow$ no time dependence), [[F130-blockspin-rg-gauge-gravity]] (the $\lambda_n=b^{-n}$ irrelevance that bounds discreteness), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] / [[F285-primordial-spectrum-tilt]] (K5: $A_s$ is provably free — the reason $\sigma_8$ is reported and not claimed), [[F295-tilt-is-an-anomalous-dimension]] ($n_s$ imported live, so the two cannot drift), [[F266-sterile-neutrino-dark-matter]] / [[F223-geon-dark-matter]] / [[F216-massive-spin2-dark-mode]] (K7's two candidates), [[F203-dark-sector-falsifiers]] (the Lyman-α floor this hands the sterile back to), [[F173-single-scalar-anisotropic-stress]] (why the zero-slip result is scoped to the gravity sector). External: Planck 2018 VI; eBOSS DR16 (Alam et al. 2021); DESI DR1 peculiar-velocity survey 2025; DES Y6 3×2pt and the combined-CMB baseline (Abbott et al. 2026); KiDS-Legacy 2025; *Status of the $S_8$ Tension: A 2026 Review*; Eisenstein & Hu 1998; Viel et al. 2005; Carroll, Press & Turner 1992.

---

## 1. What K11 actually asks, and what it cannot ask

Linear structure formation has three inputs, and two of them are already decided elsewhere:

| Ingredient | Standing | Row |
|---|---|---|
| Background $H(a)$ | **Have it** — ΛCDM reproduced, $z_\text{eq}\approx3430$ | K1 `QUANT` |
| Growth of $\delta_m$ under the model's own gravity | **Nothing** | **K11, the gap** |
| Primordial $P(k)$ | **Provably free** — $A_s$ has no route | K5 `EXCLUDED` |

$\sigma_8$ is linear in $\sqrt{A_s}$, so K5 forecloses predicting it. A finding that claimed
otherwise would be exactly the defect the 2026-08-03/04 review series caught ten times out of ten.
So $\sigma_8$ is **reported with its import budget in the same table**, never claimed.

The claim is the middle row — and it is the one place a gravity theory can differ from GR **without
differing in the background**, which is why it is worth more than the number.

## 2. The result: two free functions in the EFT, zero in the model

Every modified-gravity model in the S8 literature lives in two free functions of $(a,k)$:

$$k^2\Psi=-4\pi Ga^2\,\mu(a,k)\,\bar\rho\,\Delta,\qquad
k^2(\Phi+\Psi)=-8\pi Ga^2\,\Sigma(a,k)\,\bar\rho\,\Delta .$$

The lattice fixes both to 1, by **three structurally independent facts it already owns**. None is
introduced here. The contribution is noticing that together they leave nothing to tune.

| Closure | Mechanism | Source | Check |
|---|---|---|---|
| $\mu=1$, no $k$ | $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ with $\ln K=2\Phi/c^2$ collapses to Poisson with coefficient exactly $4\pi G$; $\partial\mu/\partial k\equiv0$ | F106 / F178 | **S2**, sympy zero |
| $\partial\mu/\partial a=0$ | $G$ structural on a rigid substrate $\Rightarrow\dot G/G\equiv0$ exactly | F79 / F284 | **S3** |
| $\Sigma=1$ (zero slip) | $AB\equiv1$, the impedance match — the same condition as PPN $\gamma=1$ | F64 D-EM9 | **S1**, sympy zero |

**Three distinct sources, so this is a genuine count and not one fact wearing three hats.**

### S1 — $AB\equiv1$ kills linear-order slip, exactly

Writing $K=e^{2\Phi}$ and reading off Newtonian-gauge potentials from $-(1+2\Psi)=-1/K$ and
$a^2(1-2\Phi_N)=Ka^2$:

$$\Phi_N-\Psi=1-\cosh 2\Phi=-2\sinh^2\Phi=\underbrace{0}_{\text{coefficient of }\Phi^1}-2\Phi^2+O(\Phi^4).$$

The **linear coefficient is a literal zero**. Slip enters at 2PN, first order in the potential
*amplitude*: $\eta-1=2\Phi\approx2\times10^{-5}$ for cosmological potentials — four orders below any
current constraint. There is no dial in the model that could produce or absorb a linear-order slip.

> **Scope, stated because it matters.** This is a statement about the **gravity** sector.
> Free-streaming neutrinos carry genuine anisotropic stress and source the usual GR slip in the
> radiation era; the lattice removes the gravitational dial, not the matter source (cf. F173).

### S2 — and the regime it is valid in

F178 demoted F106's energy-only law to the **static weak-field reduction**. That is *exactly* the
quasi-static sub-horizon regime linear CDM growth needs ($p=0$, no anisotropic stress). It is **not**
valid super-horizon or for relativistic radiation-era modes — those are carried by the transfer
function, not by this ODE. Saying so is part of the result.

## 3. What follows, derived

### D1 — the growth index is $6/11$, exactly

Substituting $f=c\,\Omega_m^{\gamma_g}$ into the model's own growth equation and expanding about
$\Omega_m=1$ splits into two orders, and **both are informative**:

$$\underbrace{c^2+\tfrac{c}{2}-\tfrac32\mu=0}_{\text{order }\epsilon^0}\ \Rightarrow\
c=\frac{\sqrt{1+24\mu}-1}{4}\ \overset{\mu=1}{=}\ 1,\qquad
\underbrace{3-\tfrac{11}{2}\gamma_g=0}_{\text{order }\epsilon^1}\ \Rightarrow\
\boxed{\gamma_g=\tfrac{6}{11}}$$

The order-0 leg is the sharper one: $f\to1$ as $\Omega_m\to1$ holds **iff** $\mu=1$, so any
$\mu\ne1$ is visible in the *amplitude* of $f$ as well as in the index. $\gamma_g=6/11$ is a
**prediction** here rather than a fit precisely because $\mu=1$ is forced — a general
modified-gravity theory carries $\gamma_g$ as a free parameter.

### D2 — the Meszáros solution, literal-zero residual

$$\frac{d^2\delta}{dy^2}+\frac{2+3y}{2y(1+y)}\frac{d\delta}{dy}-\frac{3\delta}{2y(1+y)}=0,
\qquad y=a/a_\text{eq},\qquad D(y)=1+\tfrac32 y .$$

Residual: **literal `0`** (the decaying partner too). This is the one place the transfer function's
*shape* is derived by the model rather than imported — sub-horizon CDM grows by only $5/2$ across
the whole radiation era, which is the origin of the $T(k)\sim\ln k/k^2$ large-$k$ falloff.

### D3 — growth on the real background, and the integrator falsified

| Quantity | Model | Reference | Δ |
|---|---|---|---|
| $D(a{=}1)/a$ | $0.78799$ | $0.78719$ (Carroll–Press–Turner) | $+0.10\%$ |
| $f(z{=}0)$ | $0.52739$ | $\Omega_m^{0.55}=0.53003$ | $-0.50\%$ |
| $\gamma_g$ at $\Omega_m=0.3153$ | $0.55433$ | $6/11=0.54545$ ($\Omega_m\to1$ limit) | — |
| radiation-convention sensitivity of $f$ | $3.8\times10^{-5}$ | — | measured, not assumed |

The CPT leg is the integrator's own falsification test: a wrong initial condition or a wrong source
coefficient moves $D(1)$ by percent, and the tolerance is $0.3\%$.

$f\sigma_8(z)$ against seven RSD points (DESI DR1 PV, BOSS DR12 ×3, eBOSS DR16 LRG/ELG/QSO):
$\chi^2/N=1.012$, max pull $1.8\sigma$. **Diagonal $\chi^2$ only** — the three BOSS DR12 points are
correlated and their covariance is not applied, so this is a consistency statement, not a likelihood.

### D4 — $\sigma_8$, with the budget in the same table

$$\sigma_8=0.8204,\qquad S_8=0.8410\qquad(+1.15\%\ \text{vs Planck's }0.8111)$$

| Line | Value | Status |
|---|---|---|
| $A_s$ | $2.100\times10^{-9}$ | **FREE INPUT** — K5 `EXCLUDED`, no route |
| $n_s$ | $0.9649$, imported **live** from `cosmology_anomalous_dimension.NS_OBS` | fitted; F295 routes it to $\gamma=0.017550$, a relabelling |
| $T(k)$ coefficients | Eisenstein–Hu 1998 no-wiggle | **imported** |
| $\sum m_\nu$ | $0.06$ eV, applied as $-4f_\nu$ on $\sigma_8$ | Planck baseline |
| $\Omega_m,\Omega_b,h$ | Planck 2018 | measured; the same inputs K1/F188 takes |
| **Derived here** | $D(a)$, the Meszáros stagnation $T(k)$ encodes, $\gamma_g=6/11$ | — |

The residual $\approx1\%$ after the neutrino correction is the **no-wiggle fit itself**, documented
at the 1–2% level in $\sigma_8$. It is an imported-fit residual, not a model residual.

### D5 — $\mu=1$ is not just derived, it is **pinned**

In matter domination $\delta\sim a^{p}$ with $p(\mu)=\tfrac14\!\left(\sqrt{1+24\mu}-1\right)$ and
$dp/d\mu|_1=\tfrac35$, so $\sim7$ e-folds of integration amplify a constant fractional error in
$\mu$ by $d\ln\sigma_8/d\mu\approx4$.

| Bound | 1σ interval on $\mu$ | Leans on |
|---|---|---|
| amplitude-anchored ($A_s$ fixed at the CMB) | $[0.986,\ 1.008]$ | EH98 $T(k)$ + $A_s$ |
| shape-only ($f\sigma_8$ amplitude marginalised) | upper edge $1.156$; **lower side runs off the scan floor** | nothing but the $f\sigma_8$ redshift shape |

The shape-only lower side is reported as *absent*, not as $0.5$: with the amplitude marginalised, a
suppressed growth rate is degenerate with a larger $A_s$. Quoting the scan floor as a limit would be
quoting the scan range as physics.

So the structural claim is tested at the **1.1% level**, not merely asserted.

## 4. The two bounds nobody had computed

### B1 — the lattice is invisible, by 113 orders

| Scale | Cells across | Relative $O((ka)^2)$ correction |
|---|---|---|
| Hubble radius $c/H_0$ | $4.1\times10^{60}$ | $6.0\times10^{-121}$ |
| $\sigma_8$ sphere, $8\,h^{-1}$ Mpc | $3.44\times10^{57}$ | $8.5\times10^{-116}$ |
| Lyman-α, $\sim0.3$ Mpc | $8.7\times10^{55}$ | $1.3\times10^{-112}$ |

with $a=1.0664\times10^{-34}$ m from $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ (F79/F107) and the $O((ka)^2)$
scaling from F130's block-spin irrelevance $\lambda_n=b^{-n}$. **This is the licence to use the
continuum growth equation at all** — a load-bearing bound, not a curiosity.

### B2 — $\sigma_8$ is blind to K7's dark-matter identity; Lyman-α is not

| Candidate | Mass | Half-mode $k$ | $\sigma_8$ suppression |
|---|---|---|---|
| Geon remnant, $M=(\sqrt3/2)^{1/2}M_\text{Pl}$ | $1.14\times10^{22}$ keV | $4.4\times10^{28}\,h\,$Mpc$^{-1}$ | none — pure CDM |
| F266 sterile $\nu_R$ | $5.6$ keV | $45.9\,h\,$Mpc$^{-1}$ | $2.7\times10^{-6}$ |

The $\sigma_8$ scale is $k\approx0.125\,h\,$Mpc$^{-1}$ — about **2.6 decades** below the sterile's
half-mode. So a 5.6 keV sterile and a Planck-mass geon are indistinguishable in $\sigma_8$ at the
$10^{-6}$ level, far below any measurement error.

**K11 does not settle K7 — it says which probe does.** The observable that is not blind is the
Lyman-α forest ($k\sim1$–$20\,h\,$Mpc$^{-1}$), which is exactly where F203's 9–15 keV floor already
puts the F266 sterile under pressure. That is a redirection of an open question, not a closure of it.

## 5. The falsifier, and why it can fire

$\mu\equiv1$ is **$k$-independent by derivation**, so the model has **no screening mechanism** — the
standard route by which modified gravity relieves S8 on nonlinear scales while evading linear-scale
bounds (a hatch the 2026 review names explicitly). The model therefore predicts the combined-CMB
$S_8$ propagated forward by GR growth, with nothing to tune.

| Probe | $S_8$ | Model at $0.8410$ |
|---|---|---|
| Combined CMB (Planck18+ACT DR6+SPT-3G) | $0.836^{+0.012}_{-0.013}$ | $0.29\sigma$ |
| KiDS-Legacy 2025 | $0.815^{+0.016}_{-0.021}$ | $1.17\sigma$ |
| **DES Y6 $3\times2$pt** | $0.789\pm0.012$ | **$3.00\sigma$** |
| eROSITA eRASS1 clusters | $0.86\pm0.01$ | high side |

> **If the DES Y6 direction consolidates as physical rather than as photo-$z$ / baryonic-feedback
> systematics, the model's gravity sector is falsified outright.** It cannot be accommodated,
> because there is nothing to accommodate it with. The model sides with *"the spread is
> systematics"* — a position the field itself is split on (KiDS-Legacy moved **up** by $0.056$ into
> consistency; eROSITA sits $1.5\sigma$ **high**). Euclid decides.

The corresponding registry control is built into the module rather than left to a sweep: **C1**
drives the same code path at $\mu=0.90$ and requires three legs to go red. They do —
$\sigma_8$ moves $-32.0\%$ and $\Delta\chi^2=+86.0$. This is the H2 pattern the
completeness report's gap #2 asks for, discharged at the point of writing rather than retro-fitted.

## 6. Checks (13/13)

| # | Check | Class | Result |
|---|---|---|---|
| S1 | $AB\equiv1\Rightarrow$ linear slip coefficient is literal `0`; $\eta-1=2\Phi\approx2\times10^{-5}$ | exact | PASS |
| S2 | F106 $\Rightarrow\mu=1$ and $\partial_k\mu=0$, both sympy `0` | exact | PASS |
| S3 | Constraint count: EFT 2 free functions, model 0, from 3 distinct sources | structural | PASS |
| D1 | $\gamma_g=6/11$ exact; $c=1$ iff $\mu=1$ | exact | PASS |
| D2 | Meszáros $D(y)=1+\tfrac32y$, residual literal `0` (both modes) | exact | PASS |
| D3a | $D(1)$ vs Carroll–Press–Turner $+0.10\%$; radiation sensitivity $3.8\times10^{-5}$ | quantitative | PASS |
| D3b | $f\sigma_8$ vs 7 RSD points, $\chi^2/N=1.012$ (diagonal) | quantitative | PASS |
| D4 | $\sigma_8=0.8204$, $+1.15\%$ vs Planck, budget declared | quantitative | PASS |
| D5 | $\mu\in[0.986,1.008]$ at 1σ; shape-only floor reported as absent | quantitative | PASS |
| B1 | Discreteness $\le1.3\times10^{-112}$ at Lyman-α | bound | PASS |
| B2 | $\sigma_8$ suppression $2.7\times10^{-6}$ for the 5.6 keV sterile — blind | quantitative | PASS |
| C1 | Control: $\mu=0.90$ turns 3 legs red, $\Delta\chi^2=+86.0$ | control | PASS |
| F | S8 falsifier stated with its firing condition and current split status | discipline | PASS |

## 7. What this moves, and what it does not

**Moves:** K11 `ABSENT → PARTIAL`. Growth derived with zero free functions and tested at 1.1%;
$\sigma_8$ computed with $A_s$ declared free. **It cannot reach `QUANT` while K5 stands** — that is
not a gap in this finding, it is K5's cause propagating downstream, and it is stated rather than
worked around.

**Does not move:** K5 (still `EXCLUDED`), K7 (redirected to Lyman-α, not settled), K3 (the tilt is
imported live from F295, not re-derived), K9 (untouched). No finding, module, constant, baseline or
supersession record belonging to another session was changed.

**Open, and specified:** the $\approx1\%$ $\sigma_8$ residual is the EH98 no-wiggle fit. Replacing
it with a transfer function computed from the model's own radiation-era Boltzmann hierarchy would
turn an imported residual into a model residual — and that is a real piece of work (it needs the
photon–baryon and neutrino hierarchies the model does not yet carry), not a tightening.
