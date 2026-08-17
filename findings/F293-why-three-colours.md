# F293 — Why three colours: anomalies **cannot** select $N_c$ and colour is **not** the spatial 3, but the model's $N_c$-free bare coupling turns $N_c$ into a **28-decade** lever on the confinement scale — and only $N_c=3$ lands at the observed hadronic scale

**Date:** 2026-08-05 - 20:40
**Numbering:** **F293**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `tender-gifted-pascal-3`, sector `gauge`.
**Status:** Confirmed — **15/15 PASS**, three declared controls each verified red. B1/B2 are exact (symbolic over ℚ, and literal `0.0` for the internal-index control); B5 is a **quantitative selector**, not a derivation.
**Verdict:** Row **B10** moves `ABSENT` → **PARTIAL**. $N_c=3$ is **still not derived**. What changes is that the space of routes is now mapped: two are closed as no-gos, one is shown circular, and one works as an **empirical selector** with its own circularity audited and its fragile direction named.
**Modules:** `src/casim/engine/gauge/derive_ncolour.py`
**Test / results:** record `F293-why-three-colours` (tier gate, entry `check_ncolour`), driver `tests/findings/test_F293_why_three_colours.py` → `test-results/F293_why_three_colours.json`
**Cross-references:** [[F279-hypercharge-constraint-attribution]] (the anomaly no-go, here re-verified on the full six-constraint system), [[F144-route-a-alpha-s-dimensional-transmutation]] ($g_s=\tfrac12$ derived; the running), [[F110-realtime-link-hamiltonian-confinement]] (the C7 $\chi$ map — **the absence of a Casimir there is the load-bearing fact of this finding**), [[F115-coupling-magnitudes-running-rotor]] (the rotor lock), [[F107-canonical-a-adoption-L4-grb-gate]] ($\mu_0$), [[F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1]] / [[F280-d1-subtracted-against-wilson]] (the open scheme constant whose band is propagated), [[F291-why-three-plus-one-dimensions]] / [[F292-no-higher-multiple-of-three]] ($d=3$; both state they do **not** touch B10 — this finding explains why they cannot), [[F97-baryon-no-go-centre-closure]] / [[F99-sigma-as-centre-lagrange-multiplier]] (the $\mathbb Z_3$ whose circularity is recorded).

---

## The question, and what would count as an answer

The completeness report calls B10 *"a single load-bearing integer"*: $N_c=3$ is an input, and F279 showed it is what turns derived charge *commensurability* into the observed *thirds*. Four routes are examined below. **Only one survives, and it is a selector rather than a derivation** — that distinction is the finding and is not softened anywhere.

---

## 1. R1 — anomaly cancellation cannot select $N_c$ (closed)

F279 §A3 already found that the hypercharge system closes for every $N_c$. This finding re-verifies it on the **full corrected six-constraint system** — both anomaly rows, the three mass-step rows, and the F47 Majorana row — symbolically in $N_c$ over ℚ:

$$y_Q:y_u:y_d:y_L:y_e:y_\nu \;=\; 1:(N_c{+}1):(1{-}N_c):-N_c:-2N_c:0,\qquad y_\phi=N_c$$

with **rank 6 and nullspace dimension 1 for every $N_c$** (verified at $N_c=1,2,3,4,5,7$ and symbolically), and both the gravitational and cubic $U(1)^3$ anomalies **identically zero as polynomials in $N_c$**. At $N_c=3$ this reproduces F279's $1:4:-2:-3:-6:0$ exactly.

> **Anomaly freedom fixes the hypercharge ratios and says nothing whatever about $N_c$.** The standard Standard-Model argument — that $N_c Y_Q+Y_L=0$ with $Y_Q=\tfrac16$, $Y_L=-\tfrac12$ forces $N_c=3$ — is unavailable *here*, because in this model $Y_Q$ is not independently given: it comes out of the same nullspace, proportional to $N_c$. The would-be derivation is exactly circular, and this section is what establishes that rather than assuming it.

---

## 2. R2 — colour is not the three spatial axes (closed)

This is the first thing anyone guesses in a lattice model that has just derived $d=3$ (F291/F292). It fails for a checkable reason.

The BCC point group $O_h$ contains the 3-cycle $C_3$ about $[111]$, which permutes the axes. As a matrix on three labels it is an **even** permutation, so $\det=+1$ and it *is* an element of $SU(3)$. But then:

$$\max_a\big\lVert[\,C_3,\ \lambda^a\,]\big\rVert = 2.449 \;\ne\; 0,$$

so an axis-identified colour would be **rotated by a lattice rotation** — colour would not be internal, and would be observable. The control is the genuine case: an internal $SU(3)$ acting on an index with no spatial meaning commutes with spatial rotations at residual **`0.0`**.

A second, independent leg: $O_h$ is **finite** (order 48) and supplies at most $S_3$ (order 6) on the axes, while $SU(3)_c$ is a continuous 8-parameter group with 8 gluons. A finite group cannot contain a continuous one.

**What this does and does not exclude.** It excludes the *identification* of the colour 3 with the spatial 3. It does **not** address the bare numerical coincidence that both are 3, and this finding does not claim to. Saying otherwise would be the overclaim.

---

## 3. R3 — the $\mathbb Z_3$ centre route is circular (recorded, not counted)

F97, F99 and F110 make $\mathbb Z_3$ load-bearing for confinement, and a centre-based selector is the most natural-looking remaining idea: the centre of $SU(N)$ is $\mathbb Z_N$, so a lattice-supplied $\mathbb Z_3$ would fix $N_c=3$.

It does not work as the tree stands, because the tree introduces that $\mathbb Z_3$ **as the centre of $SU(3)$** — F110's own text reads *"$\mathbb Z_3$ — the SU(3) centre that carries the area law"*. A centre taken from the group cannot then select the group.

This is recorded as a structured result rather than a remark, so that $\mathbb Z_3$ is not quietly counted as evidence later. **Closing this route requires a $\mathbb Z_3$ derived from BCC/$O_h$ structure with no reference to the colour group** — which the tree does not have, and which is the single most promising remaining lead.

---

## 4. R5 — the selector that works

### 4.1 The one fact that makes it possible

**The model derives its bare colour coupling, and that derivation carries no $N_c$.** F144's chain is $\chi=1$ (rule circularity) together with the F110 C7 matrix identity $\chi=1/(4g_s^2)$, in which the **4 counts a plaquette's exclusive boundary links** — pure geometry. No Casimir, no adjoint dimension, no $N_c$ appears anywhere in it. Hence

$$\alpha_s(\mu_0)=\frac{g_s^2}{4\pi}=\frac1{16\pi}=0.0198944\qquad\text{at }\mu_0=1.850\times10^{18}\ \text{GeV},$$

**independent of $N_c$**, while the running to low scales depends on $N_c$ *only* through $\beta_0=(11N_c-2n_f)/3$. One equation, one unknown.

### 4.2 The primary, non-circular form: the confinement **scale**

Dimensional transmutation, $\Lambda=\mu_0\exp[-1/(2b_0\alpha_0)]$, makes the scale depend on $N_c$ **exponentially**:

| $N_c$ | $\Lambda$ (GeV) | $\log_{10}\Lambda$ |
|---:|---:|---:|
| 2 | $1.3\times10^{-23}$ | $-22.88$ |
| **3** | $\mathbf{4.7\times10^{-2}}$ | $\mathbf{-1.33}$ |
| 4 | $2.6\times10^{5}$ | $+5.41$ |
| 5 | $5.0\times10^{8}$ | $+8.70$ |

**A span of 28.3 orders of magnitude across $N_c=2..4$, of which only $N_c=3$ lands anywhere near the observed hadronic scale of a few hundred MeV.** At $N_c=2$ there is effectively no confinement scale at all; at $N_c\ge4$ the strong interaction would confine *above* the $Z$ mass ($\Lambda=256$ TeV at $N_c=4$).

This is the argument that carries the weight, for a reason given in §4.4.

### 4.3 The precise form: inverting the measured coupling

Solving the one-loop running for **real** $N_c$ at the measured $\alpha_s(M_Z)=0.1180$:

$$\boxed{\,N_c = 2.998\,}$$

and with the one physical flavour threshold above $M_Z$ ($n_f=6$ down to $m_t$, then $n_f=5$), $N_c=2.995$ — a shift of $0.09\%$. Among integers:

| $N_c$ | $\alpha_s(M_Z)$ | vs PDG |
|---:|---:|---|
| 2 | $0.0330$ | $0.28\times$ — far too small |
| **3** | $\mathbf{0.1186}$ | $\mathbf{+0.5\%}$ |
| 4 | — | Landau pole **above** $M_Z$ |
| 5 | — | Landau pole above $M_Z$ |

### 4.4 The circularity, audited rather than hidden

A selector that quietly consumed $N_c=3$ upstream would read back $N_c=3$ and mean nothing. Three inputs:

| Input | $N_c$-dependent? | Why |
|---|---|---|
| $\alpha_s(\mu_0)=1/(16\pi)$ | **no** | $\chi=1$ and the plaquette's 4 links; no Casimir |
| $\mu_0=\hbar c/a$ | **no** | F107 fixes $a$ from $\hbar,G,c$; the colour sector is absent |
| $\alpha_s(M_Z)_\text{PDG}$ | **YES** | every determination extracts it inside QCD with $N_c=3$ |

So **§4.3 is partly circular and is labelled so.** §4.2 is not: *"hadrons exist and their mass scale is of order a GeV"* is not an $N_c$-dependent extraction. That is why the 28-decade scale argument is the headline and the $2.998$ is a refinement of it rather than the result.

### 4.5 Robust in the scale, fragile in the coupling

| Systematic | Size | Effect on $N_c$ |
|---|---|---|
| F280's $\Lambda$-ratio band (factor 8, both ways) | large | $N_c\in[2.90,3.11]$, width **0.21** |
| $\mu_0$ wrong by a factor **100** | absurd | $N_c=2.79$ |
| flavour thresholds | — | $0.09\%$ |
| $\alpha_s(\mu_0)$ wrong by $+25\%$ | — | $N_c=2.54$ |

Because the running is **logarithmic**, the scheme/cutoff uncertainty that *dominates* F144's own $\alpha_s$ prediction (the cutoff convention alone moves $\alpha_s(M_Z)$ by $\sim20\%$) barely moves $N_c$: the band width $0.21$ is five times smaller than the gap to the neighbouring integers. **The selector is robust exactly where F144's prediction is weak.**

It is fragile in the *coupling*: $\mathrm{d}N_c \approx 0.023$ per percent of $\alpha_s(\mu_0)$. **This is the falsifier.** If the abelian/geometric derivation of $g_s=\tfrac12$ (F110 C7 is a *dual $U(1)$* construction) is later found to carry an $N_c$-dependent factor in its translation to the $SU(N_c)$ coupling — a $C_A=N_c$ or $C_F=(N_c^2-1)/2N_c$ — the selector moves, and a 25% factor moves it to 2.54.

---

## 5. Controls

| Perturbation | Goes red at | Meaning |
|---|---|---|
| `--param alpha_s_MZ=0.05` | B5b ($N_c\to2.47$) | the selector **follows the data**; it does not return 3 for any input |
| `--param alpha0_factor=1.25` | B5b ($N_c\to2.54$) | the named fragility, made to fire |
| `--param mu0_factor=100.0` | B5b ($N_c\to2.79$) | even a 2-decade scale error leaves 3 the nearest integer |

The first is the important one: it is the check that §4.3 is a genuine inversion of measured data and not arithmetic that lands on 3 regardless.

---

## What this closes and what remains

**Closes.** B10 moves `ABSENT` → `PARTIAL`. The route space is mapped: anomalies **cannot** work here (and the reason is specific to this model — $Y_Q\propto N_c$ comes out of the same nullspace); the spatial identification is excluded; the $\mathbb Z_3$ route is circular as the tree stands; and the model's $N_c$-free bare coupling makes $N_c$ a 28-decade lever on the confinement scale, selecting 3.

**Remains, and is the honest headline.**

1. **$N_c=3$ is still not derived.** §4 consumes a measured number. A derivation would produce 3 from lattice structure with no empirical input, and nothing here does that.
2. **The single most promising lead is R3 made non-circular** — a $\mathbb Z_3$ from BCC/$O_h$ with no reference to the colour group. The lattice does have natural 3-fold structure (the four $C_3$ body-diagonal axes; the $2\pi/3$ holonomy F253 records), and whether any of it can carry triality independently is untested.
3. ~~**The abelian→non-abelian translation of $g_s=\tfrac12$ is unaudited.**~~ **AUDITED 2026-08-05 - 22:10 by [[F294-c7-chi-map-ncolour-audit]], and the answer cuts both ways.** The χ-map is *measured* $N$-free across $\mathbb Z_2..\mathbb Z_9$ and $U(1)$ (worst deviation literal `0.0`), which upgrades §4.1 from an observation to a measurement. **But the selector does not survive the alternative reading**: under a fundamental-Casimir matching it returns $N_c=1.28$ and under an adjoint matching it has no root at all. So §4.5's framing of the fragility as "a 25% factor takes it to 2.54" **understates it** — the wrong reading destroys the selector rather than shifting it. F294 §4 carries the corrected statement and CL257's falsifier is rewritten to match. The original text of this item is left struck through rather than deleted, because it is what F294 was written to answer. F110 C7 is a dual $U(1)$ construction. Confirming it carries no $N_c$ would harden §4; finding that it does would move the selector. This is a bounded, concrete next step and it is the one that most affects the result.
4. **§2 does not address the numerical coincidence** that the spatial 3 and the colour 3 are both 3 — only the identification of the groups.
