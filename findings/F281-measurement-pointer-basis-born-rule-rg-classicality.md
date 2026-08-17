# F281 — The measurement problem on the lattice: the pointer basis is **forced** by minimal coupling, the Born rule follows on two independent legs, and classicality is the **block-spin attractor** with closed-form eigenvalue $\lambda_\text{coh}=\lvert D_b(k)\rvert^2$

**Date:** 2026-08-05 - 15:10
**Numbering:** **F281**, taken as `NEXT FREE NUMBER` from `docs/design/finding-numbers.yaml` (a backlog number — spending it **closes** a gap rather than opening one). Session `tender-gifted-pascal`, sector `interactions`.
**Status:** Confirmed — **20/20 PASS** (17 at first issue; +3 on 2026-08-05 - 16:40 when open item #3 closed, §1.6), with **three declared controls that each go red on their own leg** (verified in the driver, not only asserted in prose). Two results are exact in the literal sense — `0.0`, not $10^{-16}$: the pointer commutator and the $\ell^2$ change under a real BCC Weyl tick. The rest are machine precision ($\le 9\times10^{-16}$).
**Verdict:** Completeness row **A8** (measurement problem / classical emergence) was `ABSENT` with *zero hits repo-wide*. It is no longer absent. Row **A6** (Born rule, "reproduced in tests, never derived") gains a derivation with two independent legs and a named residual gap on one of them.
**Modules:** `src/casim/engine/interactions/qi_measurement.py`
**Test / results:** record `F281-measurement-pointer-born-rg` (tier gate, entry `check_measurement`), driver `tests/findings/test_F281_measurement.py` → `test-results/F281_measurement_pointer_born_rg.json`
**Cross-references:** [[F41-hypercharge-higgs-free]] / [[F87-charge-coupling-paired-photon]] (minimal coupling — the generator whose diagonality is the whole of M1), [[F212-dynamical-entanglement-generation]] / [[F218-algorithm-through-engine]] (the native register and its gate set), [[F226-bell-tsirelson-indistinguishable]] (Tsirelson saturation), [[F227-decoherence-unitarity-floor]] (causal cone $C(r,t)=0$ for $r>4t$; unitary with no objective collapse — **unchanged** by this finding), [[F130-blockspin-rg-gauge-gravity]] / [[F133-blockspin-casim-engine]] (the exact $R_b$). Key decision 3 (Higgs-free) is load-bearing in §1. External: Zurek (einselection, predictability sieve, envariance); Schlosshauer–Fine (the standing objection to envariance, carried openly in §2.3).

---

## The question

The model is a deterministic, reversible, strictly local QCA. Such a model owes an account of three things it has never given:

1. **Why is the classical world made of localised objects?** Decoherence theory answers "because the pointer basis commutes with $H_\text{int}$" — but in ordinary quantum mechanics $H_\text{int}$ is an *input*. What does this model, whose interactions are all fixed by the rule, actually select?
2. **Why $\lvert\psi\rvert^2$?** F212/F222/F226 *use* the Born rule throughout. Nothing derives it.
3. **Where does classical physics come from?** The model owns an exact renormalisation operator $R_b$ (F130–F134) and has never asked what it does to coherence.

Each is answered below using structure the model already has. **No new physics is introduced, and no collapse term is added** — F227's "unitary theory with no objective collapse" survives this finding intact.

---

## 1. M1 — the pointer basis is forced, not chosen

### 1.1 The structural statement

Every interaction in this tree enters as **minimal coupling**: a phase attached to the site or link, multiplying the spinor there. For $U(1)$ this is the Stueckelberg wrap of `casim.engine.gauge.minimal_coupling.u1_wrap_weyl_step_3d_bcc` (the F41/F42 architecture, exact gauge covariance):

$$\psi(x)\ \longrightarrow\ e^{-i q\,\alpha(x)}\,\psi(x)$$

Promoting the gauge phase $\alpha$ to the environment operator it physically is, the system–environment generator is

$$H_\text{int}\ =\ \sum_x \hat\alpha(x)\otimes\hat n(x),\qquad \hat n(x)=\psi^\dagger\psi(x)=\tfrac12\big(\mathbb 1-\hat Z_x\big)$$

**Every term is diagonal in the site-occupation basis.** Therefore

$$\big[\,H_\text{int},\ \hat n(y)\,\big]\ =\ 0\qquad\text{exactly, for every }y.$$

Einselection has no freedom left. The pointer observable of this model is the **local charge density**, and classicality is **position definiteness** — a theorem about the rule rather than a posit.

**Key decision 3 is load-bearing here.** The reason no *other* observable can be einselected is that the model has no non-minimal coupling anywhere: no Yukawa scalar, no Higgs field, no derivative coupling. A model with a Higgs would have to check this separately; this one cannot fail to have position as its pointer observable.

### 1.2 What the model does *not* einselect, and why that is correct

| Generator | $\max_y\lVert[H,\hat n(y)]\rVert_F$ | Reading |
|---|---:|---|
| **Minimal coupling** (the model's own) | **`0.0`** (literal) | position **is** the pointer observable |
| Non-minimal $\sigma^x$ coupling (control) | $6.2219$ | the model contains no such term; if it did, position would not be selected |
| Kinetic hopping $\tfrac12(XX+YY)$ | $2.8284$ | pointer states are exactly stable only in the measurement limit $\lVert H_\text{int}\rVert\gg\lVert H_\text{hop}\rVert$ |
| Internal spin generator $\sigma^x$ | $6.2219$ | **spin is *not* einselected** |

The last row is the one worth pausing on, because it is a *correct physical prediction* rather than a convenient one. The minimal coupling is blind to the internal spin direction, so **a spin superposition does not decohere on its own**; it survives until it is amplified into a *position* difference. That is precisely what a Stern–Gerlach magnet is for. A model that einselected spin directly would be wrong about the most-taught experiment in quantum mechanics.

### 1.3 The predictability sieve agrees, and its control flips the answer

Zurek's sieve scans candidate bases and keeps the one that produces least entropy. Scanning the candidate basis $\{U(\theta)\lvert0\rangle,\ U(\theta)\lvert1\rangle\}$ (the model's own SU(2) rotor; $\theta=0$ is site occupation), with a 3-cell environment:

| Generator | $\theta_\text{min}$ | $S$ at the site basis | $S_\text{max}$ |
|---|---:|---:|---:|
| minimal (the model) | **$0$** | $6.1\times10^{-16}$ | $0.6872$ at $\theta=\pi/4$ |
| non-minimal (control) | $\pi/4$ | $0.6929$ | $0.6929$ |

Under the model's own coupling the site basis produces **exactly zero** entropy — pointer states are perfectly stable, not approximately so. Under the control the minimiser moves to $\theta=\pi/4$ and the site basis becomes the *worst* basis, at $\ln 2 = 0.6931$ within the discretisation of the scan. The check can fail, and the control makes it fail.

### 1.4 The decoherence factor in closed form

With the environment in $\lvert+\rangle^{\otimes n_e}$, the $\hat n=0$ branch leaves it alone and the $\hat n=1$ branch rotates it by $\exp(-it\sum_j g_j Z_j)$, so the coherence is exactly

$$\big\lvert D(t)\big\rvert=\prod_{j=1}^{n_e}\big\lvert\cos(g_j t)\big\rvert$$

verified against full system+environment evolution to $6.7\times10^{-16}$ over $n_e\in\{1,2,3,4\}$ and five times. **Populations are conserved to $4.4\times10^{-16}$** — decoherence, not collapse: nothing is removed from the state, the branches merely stop interfering.

### 1.5 Finite environment ⇒ recurrence, not collapse

Because the lattice is finite and the evolution unitary, $\lvert D(t)\rvert$ must return. Measuring the fraction of time $\lvert D\rvert>0.9$ by Weyl equidistribution over the incommensurate $g_j$:

| $n_e$ | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| fraction | $0.2871$ | $0.0654$ | $0.0125$ | $1.88\times10^{-3}$ | $2.65\times10^{-4}$ |

a clean geometric law, $\log_{10}(\text{fraction}) = -0.7611\,n_e + 0.297$. Extrapolated to a mole of environment cells the recurrence time is

$$\log_{10}\!\big(T_\text{rec}/\tau\big)\ \approx\ 4.58\times10^{23}$$

lattice ticks. The age of the universe is $10^{17.6}$ s and $\tau\approx2\times10^{-43}$ s, so the prefactors are not worth writing down. **This is the model's whole account of "collapse": it does not happen, and the return is postponed by an exponent of order Avogadro's number.** That is consistent with F227 by construction and is not an independent test of anything — it is the honest statement of what a unitary theory can say.

---

## 2. M2 — the Born rule, on two independent legs

### 2.1 Leg 1 (dynamical): only $\ell^2$ survives the rule

A weight over branches must be (i) additive over branches, (ii) permutation-symmetric, and (iii) **conserved by the evolution** — branches do not change identity under a deterministic unitary step, so a measure that drifted would not be a probability. Take the $\ell^p$ family $\sum_i\lvert\psi_i\rvert^p$ and apply **one genuine BCC Weyl QCA tick** (`weyl_step_3d_bcc`, $L=8$ — the model's own fundamental step, not a toy):

| $p$ | 1 | 1.5 | **2** | 2.5 | 3 | 4 |
|---|---:|---:|---:|---:|---:|---:|
| relative change | $4.75\%$ | $3.35\%$ | **`0.0`** | $5.17\%$ | $12.2\%$ | $32.1\%$ |

$\ell^2$ is conserved to a literal zero; nothing else is conserved at all. The reason is structural: $\ell^2$ is invariant under *every* unitary, whereas $\ell^p$ for $p\ne2$ is invariant only under **monomial** (permutation × phase) unitaries, and a mixing lattice step is not one.

**The control that makes this a statement about mixing rather than about $\ell^p$:** repeat with the register's native exchange gate at its *permutation point*, $\mathrm{SWAP}=(\mathbb1+\vec\sigma_A\!\cdot\!\vec\sigma_B)/2$ — a monomial unitary. Then **every** $p$ is conserved exactly (max change `0.0`). So the $p=2$ singling-out is produced by the lattice step's mixing, which is what the argument needs.

**This leg assumes nothing about probability.** It says: of the additive permutation-symmetric candidates, the dynamics permits exactly one.

### 2.2 Leg 2 (envariance): equal amplitudes, with CA-native swaps

For $\lvert\psi\rangle=(\lvert s_0e_0\rangle+\lvert s_1e_1\rangle)/\sqrt2$, a swap on $S$ is undone exactly by the counter-swap on $E$: $(u_S\otimes u_E)\lvert\psi\rangle=\lvert\psi\rangle$ up to a global phase, ray infidelity $2.2\times10^{-16}$. The two outcomes therefore cannot be distinguished by anything belonging to $S$, so $p_0=p_1=\tfrac12$.

**What is CA-native, and it is not decoration.** In abstract QM one simply asserts that the counter-swap unitary exists. Here it must be *reachable by the model's own rule*, and this is checked rather than assumed:

- The model's exchange interaction at its permutation point **is** SWAP — residual `0.0` against the explicit permutation matrix.
- The single-cell flip is the model's SU(2) rotor at $\theta=\pi/2$, residual $6.1\times10^{-17}$ from a genuine flip.
- The swap must fit **inside the causal cone**: by F227, $C(r,t)=0$ for $r>4t$, so a counter-swap on environment cells at radius $R$ costs $\ge R/4$ ticks. The Born rule in this model has a light-cone price that it does not have in Hilbert space.

**A defect worth recording, because it is the exact failure mode the 2026-08-04 completeness report names.** The first draft of this module used the rotor at $\theta=\pi$. The rotor convention is $R(\theta,\hat n)=\cos\theta\,\mathbb1-i\sin\theta\,(\hat n\cdot\vec\sigma)$ — a Bloch rotation by $2\theta$ — so $\theta=\pi$ gives $-\mathbb1$, a **global phase**, which satisfies every envariance identity *vacuously*. Two checks passed for no reason. It was caught by the unequal-amplitude control below returning $1.0$ where it should have returned $0.96$. The genuine-flip condition is now check **M2c**, and `--param flip_angle_over_pi=1.0` is a declared control that must go red.

### 2.3 The crux: unequal amplitudes are **not** envariant

Maximising the restored overlap over *every* $u_E\in U(2)$ (the nuclear norm of $G=B^\dagger A$) gives the closed form $2c_0c_1$:

| $c_0$ | 0.8 | 0.6 | $1/\sqrt2$ | 0.99 |
|---|---:|---:|---:|---:|
| $\max_{u_E}\lvert\langle\psi\rvert(u_S\otimes u_E)\lvert\psi\rangle\rvert$ | $0.96$ | $0.96$ | **$1.0$** | $0.2793$ |

matching $2c_0c_1$ to $1.1\times10^{-16}$. Envariance holds **iff** $c_0=c_1$. That is what makes leg 2 an argument rather than a restatement.

### 2.4 Fine-graining gives $p_k=\lvert c_k\rvert^2$

For $\lvert c_k\rvert^2=\mu_k/M$ with integer $\mu_k$, a controlled-copy onto counters attached to both sides (a CNOT, native per F218) produces

$$\sum_k c_k\lvert s_k\rangle\lvert e_k\rangle\ \longrightarrow\ \frac1{\sqrt M}\sum_{m=1}^{M}\lvert S_m\rangle\lvert E_m\rangle$$

— $M$ branches of **exactly** equal amplitude (deviation from $1/\sqrt M$: `0.0`). Every transposition of fine branches is envariant (residual `0.0`), so each carries weight $1/M$, and summing over the $\mu_k$ branches of outcome $k$:

| $\mu$ | $(1,1)$ | $(1,2)$ | $(1,3)$ | $(2,3)$ | $(3,5)$ | $(1,2,4)$ |
|---|---|---|---|---|---|---|
| $p_k$ vs $\lvert c_k\rvert^2$ | agree | agree | agree | agree | agree | agree |

to $1.1\times10^{-16}$, and **exactly over $\mathbb Q$** when the branch weights are obtained by *counting* the fine branches rather than by re-quoting $\mu$. Two controls keep this honest: transpositions applied to the *un*-fine-grained unequal state are **not** envariant (min residual $0.201$), and a *uniform* fine-graining — every outcome given the same number of branches, ignoring its amplitude — gives a residual up to $0.238$, i.e. it fails, as it must.

### 2.5 The cone cost, quantified

Splitting into $M$ branches needs $\log_2 M$ environment cells inside the cone. A BCC ball of radius $10^3$ cells holds $2\times10^9$ cells, hence denominators up to $M\sim10^{6.0\times10^{8}}$, reachable in $250$ ticks. **The restriction is real and never binding**, which is worth knowing precisely because it *could* have been binding.

### 2.6 The residual gap, stated plainly

Leg 2 inherits the standard **Schlosshauer–Fine** objection: it assumes outcome weights depend only on the reduced state of $S$. This finding does not close that objection and does not claim to. **Leg 1 does not make that assumption** — which is exactly why both legs are carried rather than one. What is established is: *if* branch weights are a function of the amplitudes at all, the dynamics permits only $\lvert\psi\rvert^2$ (leg 1); and *if* weights depend only on the reduced state, envariance forces $\lvert\psi\rvert^2$ (leg 2). The two hypotheses are independent and neither is derived here.

---

## 3. M3 — classicality is the block-spin attractor

### 3.1 The closed-form RG eigenvalue

Apply the model's own exact block average $R_b$ (`block_average_field`, F130/F133) to a coherence whose relative phase carries wavevector $k$. A plane wave transforms as $\psi(x)=e^{ikx}\to\psi_c(X)=e^{ikbX}D_b(k)$ with the Dirichlet kernel $D_b(k)=\frac1b\sum_{j=0}^{b-1}e^{ikj}$, so the coherence $\rho(x,y)=\psi(x)\psi^*(y)$ carries the RG eigenvalue

$$\boxed{\ \lambda_\text{coh}(k,b)\ =\ \big\lvert D_b(k)\big\rvert^2\ =\ \left[\frac{\sin(kb/2)}{b\,\sin(k/2)}\right]^{2}\ }$$

verified against the model's actual $R_b$ at nine $(k,b)$ points to $\le 8.9\times10^{-16}$.

### 3.2 Populations marginal, coherence irrelevant

| Quantity | Value | Class |
|---|---:|---|
| $\lambda_\text{coh}(k=0,b)$ | **`1.0`** exactly | **marginal** |
| coarse total charge vs fine | residual **`0.0`** | conserved (cf. F130 Gauss law integer-exact) |
| $\lambda_\text{coh}$ envelope, generic $k$, 1-D | $b^{-2}$, exponent **`-2.0`** | **irrelevant** |
| $\lambda_\text{coh}$ envelope, 3-D | $b^{-6}$, exponent **`-6.0`** | **irrelevant** |
| $\lambda_\text{coh}(k=\pi, b\text{ even})$ | $3.7\times10^{-33}$ | **exactly zero** at the zone edge |
| $\lambda_\text{coh}$ at $k=2\pi/L$ (control) | $0.9830$ | long-wavelength coherence **survives** |

The exponent is algebraic, not fitted: $\lvert\sin(kb/2)\rvert\le1$ bounds the envelope at exactly $1/(b\sin(k/2))^2$, and the numerical fit returns $-2.0$ and $-6.0$ with residual $0$.

**The statement.** Under the model's own coarse-graining, populations are marginal and coherences are irrelevant. The IR fixed point of a quantum lattice is therefore a **diagonal density matrix** — classical probability theory is the block-spin attractor, and *that* is the classical limit. Further:

> **Coherence is irrelevant at exactly the same leading order as the F130 Lorentz-violating operators** ($\lambda_n=b^{-n}$, leading $n=2$). The same $b^{-2}$ that makes the lattice look Lorentz-invariant in the IR makes it look classical.

### 3.3 The physics is in the $k$-dependence

$k$ is the wavevector of the *relative phase between the superposed branches*, so it measures how distinguishable they are. Two branches differing by a large momentum — a genuine cat state — carry large $k$ and are crushed; two branches that differ only at long wavelength survive. **The more macroscopically distinguishable a superposition is, the faster its coherence becomes irrelevant.** That is the correct physics, obtained here as an RG eigenvalue rather than asserted, and the $k\to0$ control is what shows $R_b$ is selective rather than merely destructive.

Coarse-graining 35 decades from the lattice cell to the laboratory ($b=10$ per step) suppresses a generic coherence by

$$\log_{10}\lambda_\text{coh}^\text{total}\ \approx\ -143 .$$

---

## What this closes and what remains

**Closes.** Completeness row **A8** leaves `ABSENT`: the model now has a pointer basis it *derives* rather than chooses, a classical limit that is a property of its own RG operator, and an account of "collapse" as decoherence plus an Avogadro-exponent recurrence. Row **A6** gains a two-legged Born derivation, exact over $\mathbb Q$ on the fine-graining leg.

**Remains, and is not hidden.**

1. **The Schlosshauer–Fine gap on leg 2** (§2.6) is open. Leg 1 is independent of it but rests on its own unproven hypothesis (that weights are a function of amplitudes at all). Neither leg is a proof; together they narrow the space considerably.
2. **§1.1's diagonality is proved for the $U(1)$ wrap generator.** The $SU(2)_L$ and $SU(3)_c$ couplings are site-local rotations (`su3_rotate_weyl_step_3d_bcc`, `covariant_weyl_step_3d_bcc`) and are diagonal in *position* while acting on internal indices — which is what §1.2 requires — but the explicit non-Abelian commutator has not been written out here. That is a half-session of work and should be done before the claim card is widened beyond $U(1)$.
3. ~~**The sieve is run on one system cell with a 3-cell environment.**~~ **CLOSED 2026-08-05 - 16:40 — see §1.6 below.**
4. ~~**Row A9 (spin–statistics) and A10 (cluster decomposition) are untouched.**~~ **CLOSED 2026-08-05** by [[F289-spin-statistics-connection]] (A9) and [[F290-cluster-decomposition-strict-cone]] (A10).

---

## 1.6 The sieve at many cells — open item #3, closed 2026-08-05 - 16:40

The one-cell sieve of §1.3 scans a **one-parameter** family. At many cells the candidate space is the whole of $U(2^n)/U(1)^{2^n}$, and no scan can claim to have found a *global* minimum there. The scale-up therefore replaces the scan with the algebraic statement that makes it unnecessary:

> $\{\hat n(x)\}_{x=1..n}$ is a **maximal abelian** subalgebra of the system's operator algebra — its commutant is exactly the diagonal algebra.

A maximal abelian algebra has a **unique** joint eigenbasis up to phases and label ordering. So the pointer basis is not merely *a* minimiser of the sieve; it is **the** one, at every system size, with no scan required. The commutant dimension is *computed* — the kernel of $X\mapsto([X,\hat n(x)])_x$, via matrix rank — not asserted:

| $n_\text{sys}$ | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| commutant dimension | 2 | 4 | 8 | 16 |
| $\dim\mathcal H = 2^{n}$ | 2 | 4 | 8 | 16 |
| maximal abelian? | ✓ | ✓ | ✓ | ✓ |
| $S$ at the pointer basis | $6.7\times10^{-16}$ | $6.7\times10^{-16}$ | $6.7\times10^{-16}$ | $6.7\times10^{-16}$ |
| min $S$ over generic states | $0.041$ | $0.729$ | $1.440$ | $1.655$ |

Two things are worth reading off this table. The pointer entropy **does not grow with $n$** — it stays at round-off. And the entropy of the *most predictable* generic state grows from $0.041$ to $1.655$, so the gap between the pointer basis and everything else **widens** with system size: **einselection gets sharper, not weaker, as the system grows.** That is the opposite of what a one-cell result could have been hiding, and it is why the scale-up was worth doing rather than assuming.

### The one loophole, and it is real physics

Uniqueness has exactly one way to fail, and this finding would be dishonest not to test it: if the environment couples to two configurations **identically** it cannot resolve them, and their superposition stays predictable. Probing with $(\lvert01\rangle-\lvert10\rangle)/\sqrt2$ — a superposition of two *different* occupation patterns, so it must decohere under any resolving environment:

| Same state, same probe | entropy produced |
|---|---:|
| **resolving** environment (generic couplings) | $0.4807$ |
| **degenerate** environment (cells 0 and 1 coupled identically) | $6.7\times10^{-16}$ |

This is a **decoherence-free subspace** — a real, experimentally exploited phenomenon, appearing here as the exact and only exception to the uniqueness of the pointer basis. It is carried as check M1h.

**Gate impact:** F281's record grows from 17 to **20 checks** (M1f, M1g, M1h), all PASS, and the three declared controls still fire on their own legs — `coupling=nonminimal` now reds M1a, M1b **and M1f**.

**Not claimed.** No objective-collapse term is added; nothing here contradicts or weakens F227. Nothing here is a new empirical prediction — the recurrence exponent and the $10^{-143}$ suppression are consequences of unitarity plus coarse-graining, and both are unobservable by construction.
