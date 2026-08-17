# F299 — F298's withdrawal of the discriminator was **too broad**: the degeneracy is the k-string restriction, not $N=3$, and once you leave that tower the model's own exactly solvable 2D SU(3) engine **answers** — $\sigma_6/\sigma_3=2.4911511$ against $5/2$ (Casimir) and $1$ (centre), so the model's confinement sector says **H2**

**Date:** 2026-08-06 - 12:35
**Numbering:** **F299**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `bright-keen-wilson`, sector `gauge`.
**Status:** Confirmed — **10/10 PASS**, both declared controls verified red at exactly the checks declared. The group theory is exact over ℚ; the quadrature is anchored on `confinement.string_tension` at $1.1\times10^{-16}$ and grid-converged at $5.8\times10^{-15}$; the headline $1.4\%$ is a finite-$\beta$ lattice artefact that S5 drives to $1.7\times10^{-4}$.
**Verdict:** Three results. **(1)** F298's "the discriminator is degenerate at $N=3$" is **correct about the antisymmetric tower and wrong as a general statement** — inside that tower irrep and triality are in bijection at $N=3$, so *no* centre law can disagree with *any* Casimir law there; the sextet $(2,0)$ carries the antitriplet's triality with $5/2$ its Casimir, and the laws separate. **F298's withdrawal is reversed.** **(2)** The **analytic engine settles it**: generalising `confinement.py`'s exact 2D SU(3) Weyl-torus quadrature off the fundamental and running it at the model's own $\beta=2N/g_s^2=24$ gives Casimir scaling on all seven rungs to $\le1.4\%$, converging to exact as $\beta\to\infty$, and excludes centre dominance on the sextet at $2.491$ against $1$. **(3)** The **Monte-Carlo engine is not needed** for this question and answers a different one — but it is now known to be **free to ask**, because higher-rep Wilson loops are polynomials in the fundamental loop matrix F94 already measures.
**Modules:** `src/casim/engine/gauge/casimir_scaling.py` (new)
**Test / results:** record `F299-casimir-scaling` (tier gate, entry `check_casimir_scaling`) → `test-results/F299_casimir_scaling.json`. **Also landed here:** record `F298-casimir-ladder`, which F298 cited on 2026-08-05 but never wrote — see §6.
**Cross-references:** [[F298-casimir-ladder-c7-rerun]] (the withdrawal reversed, and the $N_c\le3$ leg left standing), [[F294-c7-chi-map-ncolour-audit]] (whose recommendation this executes as written), [[F293-why-three-colours]] / CL257 (the selector this undermines), [[F111-su3-ladder-casimir-scaling]] / [[F110-realtime-link-hamiltonian-confinement]] (the SU(3) ladder and the C7 identity), [[F144-route-a-alpha-s-dimensional-transmutation]] ($g_s=\tfrac12$, hence $\beta=24$), [[F70-2d-exact-area-law]] / [[F43-dynamical-gluons-wilson]] (the 2D-exact engine generalised here), [[F94-lattice-gauge-mc-confinement-vs-F86]] (the 3+1D Monte-Carlo, and what asking it would cost), [[F86-colour-dielectric-dual-superconductor]] (a winding law, not a Casimir law).

---

## 1. What F298 withdrew, and the one word that was substituted

F294 §"Remains" item 2 said:

> **Discriminate physically:** measure $\sigma_R$ for **higher representations** in the model's own confinement sector (F86 analytic, F94 Monte-Carlo). Casimir scaling favours H2; dependence only on the $\mathbb Z_N$ class favours H1.

F298 §4 answered it for **k-strings** and withdrew the recommendation:

> At $N=3$ that test is degenerate. Casimir, centre and sine **all** predict $\sigma_2/\sigma_1=1$… **The test is sound and inapplicable.**

The arithmetic is right and is reproduced here (check S2b). The scope is not. F294 said *higher representations*; F298 built the **totally antisymmetric tower** and generalised a property of that tower to the whole question.

**Why the tower cannot discriminate, stated structurally.** At $N=3$ the antisymmetric tower is $\{(1,0),(0,1)\}$ and the triality map $k\mapsto k \bmod 3$ is **injective on it**. So irrep and triality are in bijection there, and any law that is a function of one is automatically a function of the other. A tower on which two laws are *forced* to agree cannot be evidence about which of them is right. The degeneracy is a property of the **restriction**, and $N=3$ only enters by making the tower two rungs long.

---

## 2. Result 1 — outside the tower the laws separate, at $N=3$, by a factor of $5/2$

| rep | $(p,q)$ | dim | $C_2$ | triality | Casimir law $C_2/C_F$ | centre law |
|---|---|---:|---|---:|---:|---:|
| $3$ | (1,0) | 3 | 4/3 | 1 | 1 | 1 |
| $\bar3$ | (0,1) | 3 | 4/3 | 2 | 1 | 1 |
| **6** | **(2,0)** | **6** | **10/3** | **2** | **5/2** | **1** |
| 8 | (1,1) | 8 | 3 | 0 | 9/4 | 0 |
| 10 | (3,0) | 10 | 6 | 0 | 9/2 | 0 |
| 15 | (2,1) | 15 | 16/3 | 1 | 4 | 1 |
| 15′ | (4,0) | 15 | 28/3 | 1 | 7 | 1 |
| 27 | (2,2) | 27 | 8 | 0 | 6 | 0 |

The load-bearing row is the sextet: **triality 2, the same as the antitriplet, and $C_2=10/3$, two and a half times the antitriplet's $4/3$.** A law that reads only the centre charge is obliged to give $\sigma_6=\sigma_{\bar3}$; a law that reads the Casimir is obliged to give $\sigma_6=\tfrac52\sigma_{\bar3}$. Six of the eight rungs separate the laws. **A factor of $5/2$ is not a tolerance question.**

The adjoint separates them even harder ($9/4$ against $0$), but it is the *weaker* witness, because triality-0 sources are screened in $d=4$ and their asymptotic tension vanishes under Casimir scaling too. The sextet carries non-zero triality, so it confines under **both** laws and they still disagree — which is why it is quoted first.

---

## 3. Result 2 — the analytic engine answers, and it says Casimir

`confinement.py` is an **exactly solvable** 2D SU(3) engine: in 2D axial gauge the plaquettes are independent, so for *any* irrep the Wilson loop factorises and

$$\sigma_R=-\ln w_R(\beta),\qquad w_R(\beta)=\Big\langle \frac{\chi_R(U)}{d_R}\Big\rangle_{\beta},\qquad d\mu_\beta\propto e^{(\beta/N)\,\mathrm{Re}\,\chi_F}\,dU_{\text{Haar}}.$$

It had only ever been run in the fundamental. `casimir_scaling.py` generalises it to arbitrary irrep characters — division-free Jacobi–Trudi, as `su3_ladder.singlet_multiplicity_torus` already does, so there is no $0/0$ at degenerate torus points and the periodic rectangle rule stays spectral — and runs it at **the model's own coupling**: F144's $g_s=\tfrac12$ gives $\beta=2N/g_s^2=24$.

| rep | measured $\sigma_R/\sigma_3$ | Casimir law | centre law | dev. from Casimir |
|---|---:|---:|---:|---:|
| $\bar3$ | 1.0000000 | 1 | 1 | 0 (exact, conjugation) |
| **6** | **2.4911511** | **2.5** | **1** | **0.35%** |
| 8 | 2.2433555 | 2.25 | 0 | 0.30% |
| 10 | 4.4634964 | 4.5 | 0 | 0.81% |
| 15 | 3.9720941 | 4 | 1 | 0.70% |
| 15′ | 6.9047286 | 7 | 1 | 1.36% |
| 27 | 5.9314777 | 6 | 0 | 1.14% |

**Worst deviation from Casimir scaling: 1.36%. Nearest miss of a centre prediction on a separating rung: 1.49 absolute.** The two are not close to comparable, and the check that they are not (S4b) is separate from the check that Casimir fits (S4).

Three things make this a measurement rather than a fit:

1. **It is anchored on the engine it generalises.** The generalised quadrature's fundamental $\sigma_3$ reproduces `confinement.string_tension(24)` to $1.1\times10^{-16}$ (S3). The higher-rep numbers come out of the same integral.
2. **It is the approach to an *exact* law, not agreement at one coupling.** In the continuum limit $\sigma_R=(g_0^2/2)C_2(R)$ with $g_0^2=2N/\beta$, so the residual must vanish — and it does, monotonically: $1.36\%\to0.30\%\to0.070\%\to0.017\%$ at $\beta=24,48,96,192$ (S5). The $1.4\%$ is the lattice artefact at the model's finite $\beta$; the law it converges to is exact.
3. **It is not a numerical accident.** The quadrature is spectral: $n=160$ and $n=480$ agree on $\sigma_6/\sigma_3$ to $5.8\times10^{-15}$ (S6).

**Control (declared).** `--param beta=2.0` puts the engine at strong coupling, where $\sigma_6/\sigma_3=2.14$ — neither $5/2$ nor $1$. S4 goes red. So this is a statement about the model's **own weak coupling**, not a universal claim about 2D gauge theory. (At very strong coupling the ratios drift toward a box-counting law, which is the character expansion's leading order and not either hypothesis.)

### The $d=2$ caveat, and why it does not weaken the verdict

$d=2$ has no transverse gluons, hence no string breaking, hence **centre dominance cannot appear there even in principle.** That must be said, and this finding says it in the module docstring, in the test file and here.

The reason it does not rescue H1: **C7 is a single-plaquette, bare-normalisation identity.** It fixes what one link in irrep $R$ costs — $\tfrac{g^2}{2}\cdot4\cdot C_2(R)$ against $s(k)^2/(2\chi)$ — not what an infinitely long string costs. Screening is an infrared phenomenon; it changes which state a long string decays into, and it cannot renormalise the ultraviolet cost of a link. The regime C7 lives in is exactly the regime where $d=2$ and $d=4$ agree and where the 2D computation is exact. **An engine that could show centre dominance would be answering a different question.**

---

## 4. Result 3 — the Monte-Carlo engine, and what asking it would cost

F294 named F94 (3+1D SU(3) heat-bath with a Lüscher–Weisz two-level estimator) as a candidate discriminator. Two findings about it:

**It is free to ask.** Higher-rep Wilson loops are *polynomials in the fundamental loop matrix F94 already measures*:

$$\chi_6(W)=\tfrac12\big[(\mathrm{Tr}\,W)^2+\mathrm{Tr}\,W^2\big],\qquad \chi_8(W)=\lvert\mathrm{Tr}\,W\rvert^2-1,\qquad \chi_{10}(W)=\tfrac16\big[(\mathrm{Tr}\,W)^3+3\,\mathrm{Tr}\,W\,\mathrm{Tr}\,W^2+2\,\mathrm{Tr}\,W^3\big].$$

Verified on the maximal torus to $8.9\times10^{-15}$ (S7), which is a complete proof for class functions since every SU(3) element is conjugate to a torus element. **No new sampling** — the same configurations, a different trace.

**But it answers a different question.** What F94 would measure is the $d=4$ *regime structure*: Casimir scaling at intermediate $R$ with the adjoint and decuplet strings breaking asymptotically. That is worth having, and it is the question $d=2$ cannot be asked. It is **not** the C7 normalisation question, which §3 settles. So: the analytic engine settles H1/H2; the Monte-Carlo engine is the tool for the infrared companion question, and its run parameters are recorded in `mc_reach()` rather than left as a suggestion.

**F86 is neither.** Its BPS law $\sigma_n=2\pi v^2n$ is linear in the *winding*, so it gives 2 for both the antitriplet and the sextet and disagrees with Casimir, centre and sine alike. F298 read that correctly: it locates F86 at the non-interacting-vortex point rather than settling anything.

---

## 5. What this costs the B10 selector — and the one thing it does not touch

Under H2, F294's root-finding returns $N_c=1.28$: **the F293/CL257 selector does not survive.** And it cannot be rescued by moving the lattice scale. Solving the one-loop running for the $\mu_0$ each hypothesis needs in order to reproduce the measured $\alpha_s(M_Z)=0.1180$:

| reading | $1/\alpha_0$ | $\mu_0$ required | vs the model's $1.850\times10^{18}$ GeV | vs $M_\text{Planck}$ |
|---|---:|---:|---:|---:|
| **H1** $1/(16\pi)$ | 50.265 | $1.782\times10^{18}$ GeV | $-1.6\%$ | 0.84 decades below |
| **H2** $1/(16\pi C_F)$ | 67.021 | $6.060\times10^{24}$ GeV | **+6.5 decades** | **+5.7 decades above** |

H1 lands on the model's own lattice scale to under two percent. H2 wants a scale nearly six decades **above** the Planck mass, which is not a scale the lattice can have. **So the conflict is structural, not a tolerance**, and it is now sharper than F298 left it: F298 said the model "cannot consistently have both", and this finding says which one its own confinement engine implements. Either the $0.08\%$ agreement of $1/(16\pi)$ with the required bare coupling is a one-part-in-a-thousand coincidence, or somebody must supply the missing argument that the model's coupling is normalised on the **centre** while its running uses the **$SU(N_c)$** $\beta$-function — and that argument does not exist in the tree.

**CL257 is affected and F298's structural leg is not.** The $N_c\le3$ result — the C7 identity is well-defined only for $N_c\le3$ — holds under *both* readings and consumes no measured number. It is untouched here and remains the only part of B10 that is structural. What F299 damages is the *empirical* selector of CL257(c), which needs H1.

---

## 6. Housekeeping that was not optional

F298 declared `record F298-casimir-ladder (tier gate, entry check_casimir_ladder)`. **That record did not exist.** The module, its `_SPINE` row, `tests/findings/test_F298_casimir_ladder.py` and `test-results/F298_casimir_ladder.json` had all landed; the one object that *arms* them had not, so an 8/8 result was sitting in the tree with nothing in `casim test` able to run it. The record is written here (§"Test / results"), with its two controls declared, and `check_test_registry` is green at 397 records.

This is the failure mode D9 exists to prevent, and it is worth naming: **a finding that cites a record is not evidence that the record exists.** Nothing in the gate catches a *missing* record whose module is otherwise fully registered — `check_module_registry` was green throughout, because the module had a row and a `tests=` pointer to a file that really is on disk.

---

## What this closes and what remains

**Closes.** F294's recommendation, executed as written rather than withdrawn. The discriminator is live at $N=3$, the model's analytic engine answers it, and the answer is Casimir scaling. F298's degeneracy is relocated from a property of $N=3$ to a property of the antisymmetric tower, with the control that proves the relocation. The missing F298 gate record is landed.

**Remains.**

1. **The H1/H2 tension is now decided against H1 on model-internal evidence, which makes the $0.08\%$ agreement the thing needing explanation.** Either an argument that the coupling is centre-normalised — which would have to explain why the running then uses the $SU(N_c)$ $\beta$-function — or acceptance that F144's agreement is a coincidence. This is the sharpest open item in the B10 line and it is now a question about F144, not about F110.
2. **The $d=4$ regime question is cheap and unasked.** Run F94 at $\beta\in[5.8,6.2]$ with the three character polynomials above and measure where Casimir scaling gives way to screening. No new sampling; parameters in `mc_reach()`. It does not bear on C7, and it would tell the confinement sector something it does not know.
3. **B10's grade does not move.** `PARTIAL` stands, but its content has shifted: the structural $N_c\le3$ leg (F298) is now carrying more of it, and the empirical $\Lambda$-scale selector is carrying less.
