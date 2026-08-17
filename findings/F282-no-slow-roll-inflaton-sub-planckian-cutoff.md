# F282 — The model admits **no** slow-roll inflaton: the F107 cell puts the lattice cutoff at $\Lambda=3^{-1/4}M_\text{Pl}=\sqrt{c_\text{lat}}\,M_\text{Pl}$ **exactly**, so every compact CA field direction carries $M_\text{Pl}^2/f^2\ge\sqrt3=1/c_\text{lat}$ and every slow-roll parameter is $O(10)$ — the primordial $P(k)$ is an automaton **initial condition**, not a dynamical output

**Date:** 2026-08-02 - 12:20
**Status:** **Structural no-go** (a documented negative, the same category as [[F204-alcubierre-warp-structural-exclusion]] and [[F216-massive-spin2-dark-mode]]) — 7/7 checks PASS. The obstruction constant $r_\text{min}=M_\text{Pl}^2/\Lambda^2=\sqrt3=1/c_\text{lat}$ is **exact-algebraic**; the per-candidate coefficients are **closed-form** ($K_\text{clock}=9$ exactly) or **machine-precision numerical** ($K_\text{radial}=5.9215$, on the model's own F118 couplings); the escape-route exclusions (Starobinsky, N-flation, periodic $n_s$) are **quantitative** with named margins.
**Module:** `src/casim/engine/interactions/cosmology_primordial.py`
**Registry record:** `F282-inflaton-candidate-slowroll` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F282_primordial_sector_nogo.json`
**Cross-references:** [[F238-geon-relic-abundance]] (the parent: proved $\beta$ non-derivable *because* "there is no inflaton sector" — this finding proves there **cannot be one**, upgrading F238's structural absence to a structural exclusion), [[F107-canonical-a-adoption-L4-grb-gate]] / [[F79-structural-newton-constant]] ($a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ — the exact input that does all the work), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$ — the obstruction constant is its inverse), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $E_g$ Mexican hat and its $O(1)$ couplings), [[F234-Wvc-triple-closed-delta-2-9-pins-brake]] / [[F175-lattice-2-9-eg-weight]] ($\lambda_6=0.243$ and $\delta^*=\tfrac29$ derived — which is *why* there is no tuning freedom left), [[F193-ontic-vacuum-gravitates-as-zero]] (fixes the additive constant in the hat: the true vacuum gravitates as zero, so $V_0$ is **not** free), [[F216-massive-spin2-dark-mode]] / [[F180-gravitational-wave-speed]] (graviton = 2 dof; $\ln K$ has no potential in vacuum ⇒ not an inflaton), [[F130-blockspin-rg-gauge-gravity]] (the measured Kadanoff spectrum: no nearly-marginal scalar), [[F27-complex-mass-chiral-su2]] (Higgs-free by construction — the SM scalar inflation usually reaches for does not exist here). External: Planck 2018 ($n_s=0.9649\pm0.0042$, $A_s=2.1\times10^{-9}$); BICEP/Keck 2021 ($r<0.036$); Starobinsky 1980; Freese–Frieman–Olinto 1990 (natural inflation); Lyth 1997; Banks–Dine–Fox–Gorbatov 2003 (no super-Planckian axion decay constants); Dimopoulos et al. 2008 (N-flation); Albrecht et al. / Pen–Seljak–Turok (causal-seed models excluded by acoustic-peak coherence).

Raised by the 2026-08-02 completeness sweep (`docs/status/completeness-2026-08-02.md`, **gap #1**, rubric row **K4**), whose prescribed smallest next step was exactly this question: *"does the model admit an inflationary sector, and if not, why not — a no-go here is worth as much as a mechanism."*

> **CORRECTION 2026-08-02 - 14:00 ([[F283-elastic-lattice-excluded-and-f282-invariance]]).** §9 **falsifier 5 is struck** — it was unsound. It claimed the no-go could be falsified by a different lattice spacing; it cannot, because F79 ties $G\propto a^2$, so $M_\text{Pl}$ and $\Lambda_\text{UV}$ scale together and $r=\sqrt3$ is **exactly invariant** under any stretch $a\to sa$ ($\partial r/\partial s\equiv0$). The obstruction does not depend on the F107 value of $a$ at all; it is a **scale-free geometric invariant** of the BCC lattice, equal to $1/c_\text{lat}$. **Everything else in this finding stands, and the verdict is strengthened**: the no-go cannot be dialled away, only broken by falsifiers 1–4. F283 also shows an elastic lattice is independently excluded by $\dot G/G$ (LLR + BBN), the 2-dof graviton count and GW170817; [[F284-rigid-lattice-expansion-and-primordial-state]] then says what expansion and the primordial state *are* on the rigid substrate that leaves.

---

## 1. The acceptance test, stated up front

K4 asks for inflation **or a declared substitute**. The sweep's framing was explicit: *"nothing structural has been shown to block it — that is the point. No no-go exists here because no attempt exists. This is untouched ground, not defended ground."*

**Acceptance:** either (i) a model-native field direction that sustains $\gtrsim55$ e-folds of slow roll with $n_s$ in the Planck band, or (ii) a proof that no such direction exists, with the obstruction named and quantified.

**Outcome: branch (ii).** The ground is now defended. Every scalar direction the model owns fails slow roll, they all fail by $O(10)$ rather than marginally, and they all fail for **one exact reason**.

## 2. The obstruction, in one line

$$\boxed{\ \frac{a}{\ell_\text{red}}=3^{1/4}\ \text{exactly}\quad\Longrightarrow\quad \Lambda_\text{UV}=\frac1a=\sqrt{c_\text{lat}}\,M_\text{Pl},\qquad r_\text{min}\equiv\frac{M_\text{Pl}^2}{\Lambda_\text{UV}^2}=\sqrt3=\frac1{c_\text{lat}}.\ }$$

**Derivation (exact).** F79's structural Newton constant $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, adopted as canonical by F107, fixes the ruler at $a/\ell_P=\sqrt{8\pi}\,3^{1/4}$ where $\ell_P=\sqrt{\hbar G/c^3}$ is the **non-reduced** Planck length. Slow roll is written in **reduced** Planck units, $M_\text{Pl}=1/\sqrt{8\pi G}$, i.e. $\ell_\text{red}=\sqrt{8\pi}\,\ell_P$. The $\sqrt{8\pi}$ cancels identically:

$$\frac{a}{\ell_\text{red}}=\frac{\sqrt{8\pi}\,3^{1/4}}{\sqrt{8\pi}}=3^{1/4}=1.3160740\ldots$$

So the lattice spacing is $3^{1/4}$ *reduced* Planck lengths and the UV cutoff is **sub-Planckian**: $\Lambda_\text{UV}=0.75984\,M_\text{Pl}$. Because $c_\text{lat}=1/\sqrt3$ (F26), this is the striking identity

$$\Lambda_\text{UV}=\sqrt{c_\text{lat}}\;M_\text{Pl},\qquad \frac{M_\text{Pl}^2}{\Lambda_\text{UV}^2}=\frac1{c_\text{lat}}=\sqrt3.$$

**The number that forbids inflation is the inverse lattice light speed.** The same $\sqrt3$ that makes light slower than the lattice's own causal maximum makes gravity strong enough, at the cutoff, to spoil every flat direction. Both come from $d=3$.

## 3. Why that single number is fatal (the compactness leg)

A cellular automaton has a **bounded per-cell state space** — unit spinors, $SU(2)$ links, compact angles. There is no non-compact scalar to run up. Every candidate's canonically normalised field is therefore $\phi=f\chi$ with $\chi$ a bounded dimensionless lattice variable and

$$f=\frac{\sqrt J}{a},\qquad J=\text{the dimensionless lattice stiffness},$$

so every slow-roll parameter carries the **universal prefactor**

$$r\equiv\frac{M_\text{Pl}^2}{f^2}=\frac{\sqrt3}{J}=\frac{1}{c_\text{lat}J},$$

and for any candidate

$$\min_{\text{field range}}\ \max\big(\epsilon,|\eta|\big)=K\,r=\frac{K\sqrt3}{J},$$

with $K$ a pure number fixed by the shape of the potential. Slow roll needs this $\lesssim0.02$ ($|\eta|\lesssim1/2N_e$ at $N_e\simeq55$). **$J$ is the only escape**, and the model has already computed it to be $O(1)$: every coupling in the F118 functional lies in $[0.16,\,2.4]$.

## 4. Candidate 1 — the $E_g$ clock angle $\delta$ ($K=9$, closed form)

The model's one genuine angular direction is the $E_g$ condensate clock, whose potential is *fully determined* — $\lambda_6=0.243$ is derived (F234 from $\delta^*=\tfrac29$, F175), not fitted:

$$V(\delta)=\lambda_6e^6\cos^2 3\delta=\tfrac{A}{2}\left(1+\cos6\delta\right),\qquad A=\lambda_6e_\text{sat}^6=0.037690.$$

With $u=\cos6\delta$,

$$\frac{\epsilon}{r}=18\,\frac{1-u}{1+u}=18\tan^2 3\delta,\qquad \frac{|\eta|}{r}=36\,\frac{|u|}{1+u}.$$

$\epsilon$ falls and $|\eta|$ rises with $u$; they cross at $u^*=\tfrac13$, where both equal **9**. So

$$K_\text{clock}=9\quad\text{exactly}$$

— independent of $\lambda_6$ and of $e$ (the amplitude cancels between $V''$ and $V$; the potential's *scale* is irrelevant, only its *shape*). The harmonic number 6 of the clock invariant is what makes this large: a generic $p$-fold periodic direction gives $K=p^2/4$.

At $J=1$: $\min\max(\epsilon,|\eta|)=9\sqrt3=15.59$. **Required to inflate:**

$$r\le\frac{0.02}{9}\ \Longrightarrow\ f\ \ge\ 15\sqrt2\,M_\text{Pl}=21.21\,M_\text{Pl}=27.9\,\Lambda_\text{UV},\qquad J\ \ge\ 779.$$

## 5. Candidate 2 — the $E_g$ radial magnitude $e$ ($K=5.92$)

The F118 spontaneous-$E_g$ Mexican hat at its self-consistent point ($\kappa_E=-2.156$, $c=1.10$, $\lambda_6=0.243$):

$$V(e)=\tfrac{\kappa_E}{2}e^2+c\,e^4+\lambda_6e^6+V_0.$$

**$V_0$ is not free.** F193 proves the ontic lattice vacuum gravitates as exactly zero, so $V(e_\text{min})=0$ and the hilltop energy is forced: $e_\text{min}=0.65499$, $V_0=+0.240831$. Every number below is then determined by the model, with nothing left to tune.

At the hilltop, $\eta/r=\kappa_E/V_0=-8.952$. Scanning the whole hat,

$$K_\text{radial}=\min_e\max(\epsilon,|\eta|)/r=5.9215\quad\text{at }e=0.3006,$$

giving at $J=1$ a value $10.26$, and **required to inflate**: $f\ge17.21\,M_\text{Pl}$, $J\ge513$.

**The two independent $E_g$ directions agree to within a factor 1.5.** That is the robustness check: the no-go is not an artefact of one potential's shape.

## 6. Closing the escape routes

| Escape | Status | Margin |
|---|---|---|
| **Any periodic direction, via $n_s$** | excluded | $n_s-1=-p^2r\frac{3+u}{1-u}$; $\frac{3+u}{1-u}\ge1$ over the whole range (min at the hilltop $u=-1$), so $n_s\le1-p^2\sqrt3/J$ **everywhere**. The most generous case $p=1$, $J=1$ gives $n_s\le-0.732$ vs Planck $0.9649\pm0.0042$: **404σ**. The model's own clock ($p=6$) gives $n_s\le-61.4$ |
| **Starobinsky $R^2$ plateau** | excluded | Needs $c_2\simeq4.93\times10^{8}$ ($M_s=1.3\times10^{-5}M_\text{Pl}$ from $A_s$). F79 gives gravity **zero tree stiffness** — the graviton kinetic term *is* the induced matter loop — so $c_2$ is a one-loop induced coefficient $\sim N_\text{dof}/96\pi^2\simeq0.106$ at $N_\text{dof}=100$. **Short by 9.67 decades.** Independently: that $c_2$ puts the scalaron at $M_s=0.889\,M_\text{Pl}>\Lambda_\text{UV}=0.760\,M_\text{Pl}$ — above the cutoff, so not in the EFT at all |
| **N-flation / multi-field** | excluded | $\Delta\phi_\text{eff}=\sqrt N f$ would need $N\simeq780$ independent scalar directions. The model has **2** (the $E_g$ doublet's $e$ and $\delta$); it is Higgs-free by construction (F27), so there is no other scalar with a potential. Shortfall $\approx390\times$. The species-scale argument ($\Lambda_\text{QG}\to M_\text{Pl}/\sqrt N$) removes the gain even if there were more |
| **The conformal mode $\ln K$** | excluded | F216: the metric graviton has exactly **2 dof**, massless and transverse, protected by an emergent-diff Ward identity — there is no propagating scalar graviton. F180: $\ln K$ obeys $(\nabla^2-c_\text{lat}^{-2}\partial_t^2)\ln K=-(8\pi G/c^4)T^{00}$, i.e. a **sourced** equation with $V\equiv0$ in vacuum. A field with no potential has no vacuum energy to inflate on |
| **Gauge / Stueckelberg phases** | excluded | F41/F42: $U(x)$ absorbing $\Delta Y$ is a compact **pure-gauge** phase. Gauge invariance forbids a potential for it |
| **Criticality substitute (causal seeds)** | excluded (empirically) | A lattice-native, *causal*, sub-horizon mechanism generating $P(k)$ produces incoherent, active-source perturbations, excluded by the observed acoustic-peak phase coherence. F130's measured Kadanoff spectrum says the same thing structurally — see §7 |

## 7. The same no-go, read off the RG flow (F130)

A slow-roll direction *is* a nearly-**marginal** operator: Kadanoff eigenvalue $\lambda=b^0=1$. F130 measured this lattice's full block-spin spectrum:

| Direction | Exponent | Eigenvalue | F130 exactness |
|---|---:|---|---|
| Confinement $\sigma$ | $+1$ | $b$ (relevant) | exact (C1) |
| Deconfining $\lambda$ | $-2$ | $b^{-2}$ | quantitative (C1) |
| LIV operators, $n\ge2$ | $-n$ | $b^{-n}$ | exact, round-off-floor identity (T2) |

**The spectrum has a gap around marginality**: the nearest scaling exponents to $0$ are $+1$ and $-2$. The only marginal object ($b^0$) is the continuum light speed — the fixed point itself, not a scalar field with a potential. So there is no nearly-marginal scalar operator for a slow-roll field to *be*. This is the identical $O(1)$ obstruction of §3–§5, obtained from the model's own measured RG data instead of from any Lagrangian, and it is the reason the "criticality substitute" cannot be rescued: the fixed point is not merely un-inflationary, its scalar spectrum has an $O(1)$ gap where inflation would have to live.

## 8. Verdict

> **The model does not admit a slow-roll inflaton, and cannot be made to admit one without breaking something already derived.** The lattice cutoff is sub-Planckian by the exact factor $3^{1/4}=1/\sqrt{c_\text{lat}}$; every CA field direction is compact with an $O(1)$ lattice stiffness; therefore every slow-roll parameter is bounded below by $O(1)\times\sqrt3$. Inflating would require a decay constant $f\simeq20\,M_\text{Pl}$ — **28× the lattice cutoff** — i.e. a stiffness $J\sim5\times10^2$–$8\times10^2$ in a sector where every coupling the model has derived is $O(1)$. Every standard escape (plateau $R^2$, multi-field, conformal mode, gauge phase, causal seeds) is closed by an already-established finding or by data.

**Consequence for the rubric.** K4 moves **ABSENT → EXCLUDED**, with the cause named and a falsifier attached. K5 and K12 become **provably non-derivable**, joining K8: the primordial power spectrum $P(k)$ — amplitude, tilt and all — is an **initial condition of the automaton**, specified at $t=0$ across the whole lattice, not a dynamical output. This is not evasion: in a CA the initial state *is* a legitimate primitive, and it is the only object in the model that can carry super-horizon correlations without a causal mechanism. It is also honest about the cost: the model buys its $\Omega_\text{DM}$, its $n_s$ and its $A_s$ from the same shop, and F238's single free number becomes a free *function*.

**This generalises F238.** F238 proved $\beta$ non-derivable *because the inflaton sector had not been built*, leaving open that someone might build it. F282 closes that: it cannot be built. The chain $\Omega_\text{DM}\leftarrow\beta\leftarrow\sigma(k_\text{PBH})\leftarrow P(k)\leftarrow$ inflaton now terminates on a **proven** absence rather than an observed one.

## 9. Falsifiers

1. **Exhibit a scalar direction with $J\ge780$.** Any CA field whose lattice stiffness exceeds the model's entire computed coupling range by three orders would break §3. This is the sharpest single number to attack.
2. **Exhibit a non-compact field direction.** The compactness leg (§3) is structural, not computed; a genuinely unbounded per-cell degree of freedom would void it.
3. **A derived $R^2$ coefficient $c_2\gtrsim10^{8}$.** F79's zero-tree-stiffness is what caps $c_2$ at the one-loop induced value; a large tree-level $R^2$ would reopen Starobinsky.
4. **A super-horizon-coherent, causal generation mechanism.** Would defeat the acoustic-peak exclusion in §6.
5. ~~**A change to $a/\ell_P$.** The whole no-go rides on $\sqrt{8\pi}\,3^{1/4}$ (F79/F107). If $a$ were $\gtrsim20\times$ smaller in Planck units — cutoff far *above* $M_\text{Pl}$ — the obstruction would evaporate.~~ **STRUCK 2026-08-02 - 14:00 by [[F283-elastic-lattice-excluded-and-f282-invariance]]. This falsifier was unsound.** $a$ cancels: F79 ties $G\propto a^2$, so under $a\to sa$ *both* $M_\text{Pl}=3^{1/4}\hbar/(sac)$ and $\Lambda_\text{UV}=\hbar/(sac)$ scale as $1/s$ and $r=\sqrt3$ is invariant, $\partial r/\partial s\equiv0$ (exact, sympy). $M_\text{Pl}$ is not an external yardstick in this model — it *is* a lattice quantity. **The obstruction is a scale-free geometric invariant of the BCC lattice ($r=1/c_\text{lat}$, from the $d=3$ eight-neighbour walk) and cannot be dialled away by any choice of spacing, constant or dynamical.** Falsifiers 1–4 are unaffected; the verdict is strengthened.

## 10. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $a/\ell_\text{red}=3^{1/4}$; $\Lambda=\sqrt{c_\text{lat}}M_\text{Pl}$; $r_\text{min}=\sqrt3=1/c_\text{lat}$ | **exact-algebraic** (sympy, from F79/F107) |
| $K_\text{clock}=9$, crossing at $u^*=\tfrac13$; $\epsilon/r=18\tan^23\delta$ | **exact-algebraic** (closed form, amplitude-independent) |
| $n_s\le1-p^2r$ for any periodic direction ($\min$ of $(3+u)/(1-u)$ is 1) | **exact-algebraic** |
| $K_\text{radial}=5.9215$, $e_\text{min}=0.65499$, $V_0=0.240831$ | **machine** (on F118 couplings + F193-forced $V_0$) |
| Compactness ⇒ $f=\sqrt J/a$; $J=O(1)$ from the F118 coupling range | **structural** + **quantitative** |
| Starobinsky shortfall 9.67 decades; scalaron above cutoff | **quantitative** (order-of-magnitude $N_\text{dof}$) |
| N-flation shortfall $\approx390\times$; conformal / gauge-phase exclusions | **structural** (F216/F180/F41) |
| RG marginality gap $=1$ | **exact** (F130 T2/C1 eigenvalues) |
| A **substitute** that predicts $n_s=0.965$ and $A_s=2.1\times10^{-9}$ | **open** — and, per §8, must now come from initial-condition physics, not field dynamics |

## 11. Honest scope

The strong content is the exact obstruction constant and its identification with $1/c_\text{lat}$: this is not "we looked and found nothing flat," it is "flatness costs $M_\text{Pl}^2/f^2\ge\sqrt3$ and the model has already spent every parameter that could pay." The weaker legs are the ones that carry an order-of-magnitude: $J=O(1)$ is inferred from the F118 coupling range rather than computed from a second-shell kinetic term (falsifier 1 is exactly this), and $N_\text{dof}\simeq100$ in the Starobinsky leg is an SM count. Neither touches the conclusion: $J$ would have to be wrong by $\sim3$ orders and $N_\text{dof}$ by $\sim10$ for the verdict to move, and the two E_g candidates and the RG spectrum agree independently. What this finding does **not** do is supply the substitute — it proves the substitute cannot be a field, which is what makes the remaining option (initial conditions) forced rather than chosen.

## 12. Files
- Module: `src/casim/engine/interactions/cosmology_primordial.py`
- Test: `tests/findings/test_F282_primordial_sector_nogo.py`
- Results: `test-results/F282_primordial_sector_nogo.json`
