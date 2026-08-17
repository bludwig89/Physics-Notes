# F304 — The Born rule is a **theorem** on this lattice: the rule *forces* both Gleason premises, closing the hypothesis F281 left open

*2026-08-06 - 15:20 · sector `interactions` · session `keen-lucid-gleason` ·
module `casim.engine.interactions.qi_born_gleason` ·
test record `F304-born-rule-gleason` (**21/21** PASS, gate tier; 16/16 at first issue, +5 on 2026-08-06 - 18:20 when §5 closed residual #1) ·
results `test-results/F304_born_rule_gleason.json`*

**Target.** Completeness row **A6**: *"Superposition is structural. Born rule is **reproduced** in tests, never derived."* [[F281-measurement-pointer-basis-born-rule-rg-classicality]] moved that row with two legs and then said, in its own §2.6, exactly what it had not done:

> leg 1 assumes *branch weights are a function of the amplitudes at all*;
> leg 2 assumes *outcome weights depend only on the reduced state of $S$* (Schlosshauer–Fine).

`docs/claims/CL253-measurement-pointer-born-rg.md` consequently refuses to carry the Born leg at all, and records that a card should be written **"when one of those two hypotheses is closed."** This finding closes the first and makes the second unnecessary.

**Cross-references:** [[F281-measurement-pointer-basis-born-rule-rg-classicality]] (the pointer basis, the maximal-abelian result §1.6, and the two legs superseded in their role as *hypotheses*), [[F41-hypercharge-higgs-free]] / [[F87-charge-coupling-paired-photon]] (minimal coupling — the generator that does the work), [[F227-decoherence-unitarity-floor]] (the strict causal cone; unitary, no objective collapse — **unchanged**), [[F290-cluster-decomposition-strict-cone]] (exact no-signalling), [[F289-spin-statistics-connection]] (the precedent for carrying an external theorem while deriving its premises — the posture this finding held at first issue and no longer needs, §5). Key decision 3 (Higgs-free) is load-bearing in §2.

---

## The question, stated so that it can be answered

Gleason's theorem already says everything one could want:

> Let $\dim\mathcal H\ge3$ and let $f$ assign a non-negative weight to each ray such that $\sum_i f(e_i)=1$ for **every** orthonormal basis. Then $f(v)=\langle v\rvert\rho\lvert v\rangle$ for a unique density operator $\rho$.

It is not used as a *derivation* of the Born rule in ordinary quantum mechanics because both of its premises are, there, free assumptions:

1. **$\dim\ge3$.** Dimension 2 is a genuine hole, not a technicality: every orthonormal basis of $\mathbb C^2$ is an antipodal pair on the Bloch sphere, so $f(\hat n)+f(-\hat n)=1$ is the *whole* frame condition and any odd function satisfies it. Born occupies four dimensions of an infinite-dimensional space of admissible weights.
2. **Non-contextuality.** Bell's 1966 objection: nothing forces the weight of an outcome to be independent of which commuting observables are read alongside it. In ordinary QM $H_\text{int}$ is a modelling input, so contextual assignments cannot be excluded.

**Neither premise is free in this model.** That is the whole finding — and since 2026-08-06 - 18:20 the theorem those premises feed is **proved here too**, not cited (§5).

---

## 1. B1 — the model owns no two-dimensional measurement context

### 1.1 A measurement needs a record, and a record needs cells

The decoherence factor of F281 §1.4 is $\lvert D(t)\rvert=\prod_{j=1}^{n_e}\lvert\cos(g_jt)\rvert$. At $n_e=0$ that is the **empty product**: identically $1$ at every $t$ (measured deviation `0.0`), so nothing is ever written and no outcome exists. A measurement in this model therefore requires at least one system cell *and* one record cell, and the Hilbert space carrying it has dimension

$$\dim\mathcal H_\text{min}=2^{1+1}=4\ >\ 2 .$$

Gleason's dimension premise is met **structurally**, before any choice of apparatus. It is not that $d\ge3$ is likely or usual here; it is that $d=2$ names an object — a measurement with no record — which the model does not contain.

### 1.2 The rule *does* own 2-dim invariant subspaces, and they are unreadable

This is the objection worth taking seriously, because `weyl_step_3d_bcc` is block-diagonal $2\times2$ in momentum: the model has 2-dimensional invariant subspaces in abundance. If one of them were a measurement context, the $d=2$ hole of §3 would be physically realisable.

It is not, and both halves are measured on the model's own step ($L=4$, $N=64$ sites):

| | measured | reading |
|---|---:|---|
| leakage of a plane wave out of its block under one genuine tick | $2.2\times10^{-16}$ | the block **is** invariant |
| $\lVert[\Pi_k,\hat n(x)]\rVert_F$ | $0.17539$ | the block is **not** a pointer context |
| closed form $\sqrt{2/N-2/N^2}$ | $0.17539$ | residual **`0.0`** |

The pointer algebra is position-diagonal; a momentum-block projector is maximally delocalised in position. A momentum block is therefore **invariant but unreadable**, and every readable context is a position record on $N\ge2$ cells. The commutator is not merely non-zero — it matches its closed form exactly, so the check is a statement about the lattice rather than about round-off.

### 1.3 And there is exactly one pointer context

$\{\hat n(x)\}$ is **maximal abelian** — recomputed here rather than cited, because §2 stands on it. Commutant dimension by matrix rank:

| $n_\text{sys}$ | 1 | 2 | 3 |
|---|---:|---:|---:|
| commutant dimension | 2 | 4 | 8 |
| $\dim\mathcal H=2^{n}$ | 2 | 4 | 8 |

A maximal abelian algebra has a unique joint eigenbasis up to phases and label order. There is one pointer context, and every measurement is *a rotor into it*.

---

## 2. B2/B3 — non-contextuality is a property of the rule, not an assumption about the experimenter

### 2.1 The lemma

Every interaction in this tree enters as minimal coupling, so the system–environment generator is

$$H_\text{int}=\sum_x\hat\alpha(x)\otimes\hat n(x),$$

a **fixed operator of the rule**. Read what it does not contain: any reference to a measured basis. An experimenter who completes a ray $v$ into an orthonormal basis is choosing a rotor $U$; the record channel is generated by $H_\text{int}$, which does not know $U$. Therefore

> **Two contexts that share a ray write the same physical record for that ray.**

That is Gleason's non-contextuality premise, and here it is a theorem about the generator. **Key decision 3 is what closes the alternatives:** the model has no Yukawa scalar, no derivative coupling, no non-minimal term anywhere — so there is no term available that *could* reference a context.

### 2.2 Measured, with a control that flips it

Five distinct contexts containing the same ray, $n_\text{sys}=2$, $n_\text{env}=3$:

| generator | weight spread over 5 contexts | record ray infidelity |
|---|---:|---:|
| **minimal coupling** (the model's own) | **`0.0`** (literal) | $2.2\times10^{-16}$ |
| basis-referencing coupling (control) | $0.1549$ | $0.4916$ |

The control generator $H^\text{ctx}=\sum_k w_k\,\Pi_k^{(U)}\otimes\hat\alpha$ is built from the projectors of the *specific* context. It exists nowhere in this model; it is constructed only so that the check has a way to fail, and it does fail, on exactly its own leg.

**Outcome labels are not contexts.** Routing the same ray to a different pointer slot writes a *different* record — a different $\hat n$ pattern — but must not move its weight. Spread over all four slots: $2.2\times10^{-16}$. Permutation symmetry is a separate structural premise from context-blindness and is measured separately rather than folded in.

### 2.3 Remote contexts: non-contextuality is no-signalling

Gleason also needs the weight to be blind to context choices made *elsewhere*. In this model that is not an assumption either — it is the strict causal cone. Six cells (two system, two record cells each side), $A$ and $B$ maximally entangled; $A$ varies **which basis she measures**:

| coupling | $\max\lVert\rho_B(\text{ctx})-\rho_B(\text{ctx}_0)\rVert_\infty$ |
|---|---:|
| **local** (the model's own) | $9.7\times10^{-17}$ |
| non-local (control: $A$'s system coupled to $B$'s record cells) | $0.1985$ |

Consistent with F290's exact no-signalling ($7.8\times10^{-16}$) and F227's $C(r,t)=0$ for $r>4t$. A contextual weight assignment across spacelike separation would **signal**; the rule forbids it.

---

## 3. B4/B5 — the dichotomy, computed, so the dimension premise is load-bearing

A premise that is merely *satisfied* proves nothing about whether it matters. This section computes what would go wrong without it.

### 3.1 The $d=2$ hole, exhibited

Take $f(v)=\tfrac12+\varepsilon P_3(n_z)$ with $\varepsilon=0.15$ and $P_3$ the lowest odd Legendre polynomial above the Born one:

| | measured |
|---|---:|
| $\max_\text{2000 bases}\lvert\sum_i f(e_i)-1\rvert$ | $1.1\times10^{-15}$ |
| best-fit $\langle v\rvert\rho\lvert v\rangle$ over 4000 rays, max residual | $0.14713$ |
| … rms residual | $0.05823$ |

It **is** a frame function, to machine precision, and **no** density operator reproduces it. The $d=2$ hole is real and quantified.

### 3.2 The same family dies at $d=3$

Lifting the identical construction to $\mathbb C^3$ and summing over 4000 random orthonormal triads: mean $0.9985$, **spread $0.35724$**. The orthonormal triads of $\mathbb C^3$ are not antipodal pairs, so the odd-harmonic freedom has nothing to sit in.

### 3.3 Gleason rigidity as an integer

Parametrise the phase-invariant weights of polynomial degree $\deg$ in $\rho$ — i.e. $f(v)=\langle v^{\otimes\deg}\rvert M\lvert v^{\otimes\deg}\rangle$, $M$ Hermitian on $\mathrm{Sym}^{\deg}$, real dimension $K^2$ — and impose the frame condition over more random orthonormal bases than there are parameters. Count the null space.

| $d$ | $\deg$ | params | frame-function dimension | $d^2$ | verdict |
|---:|---:|---:|---:|---:|---|
| 3 | 1 | 9 | **9** | 9 | rigid |
| 3 | 2 | 36 | **9** | 9 | rigid |
| 3 | 3 | 100 | **9** | 9 | rigid |
| 4 | 1 | 16 | **16** | 16 | rigid |
| 4 | 2 | 100 | **16** | 16 | rigid |
| 4 | 3 | 400 | **16** | 16 | rigid |

and the surviving space **is** the Hermitian forms — every Hermitian form is recovered from the computed null space with max residual $5.7\times10^{-15}$. The dimension does not grow with the degree. That is Gleason's conclusion, obtained as a rank computation rather than quoted.

At $d=2$ the same computation gives, **exactly**,

$$\dim\ \big\{\text{frame functions of degree}\le\deg\big\}\ =\ 1+\!\!\sum_{\substack{\ell\ \text{odd}\\ \ell\le\deg}}\!\!(2\ell+1)$$

| $\deg$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| computed | 4 | 4 | **11** | **11** | **22** | **22** |
| closed form | 4 | 4 | 11 | 11 | 22 | 22 |

Every entry matches its closed form as an **integer**, and the sequence grows without bound: Born is four dimensions of an infinite-dimensional space. `--param gleason_dim=2` forces the analysis onto $d=2$ and reds B5a, which is the check that the dimension premise is doing work.

---

## 4. B6 — the closure

**Theorem (Born on the lattice).** Let a measurement in this model be (i) a rotor from the model's own gate set, (ii) the fixed minimal-coupling record channel, (iii) an exhaustive set of pointer records carrying weights that sum to one. Then

- by **B1**, the Hilbert space carrying the records has $\dim\ge4>2$;
- by **B2**, the weight depends on the outcome ray alone — the channel contains no reference to the context;
- by **B3**, no remote context choice can move it, on pain of signalling;

so the weight is a frame function on a space of dimension $\ge3$, and by Gleason

$$w(v)=\langle v\rvert\rho\lvert v\rangle,\qquad\text{and for a pure lattice state}\qquad w(v)=\lvert\langle v\rvert\psi\rangle\rvert^2 . \qquad\blacksquare$$

Confirmed on the model's own channel: over four rays, $\max\lvert w-\lvert\langle v\rvert\psi\rangle\rvert^2\rvert=2.2\times10^{-16}$.

**F281 leg 1 is now a corollary, not a hypothesis.** Gleason gives $\operatorname{Tr}\rho=1$; unitarity preserves it; so $\ell^2$ is conserved and nothing else is. Re-measured through F281's own `lp_conservation_bcc` on a genuine BCC Weyl tick: $p=2$ change **`0.0`**, minimum change over every other $p$ $=0.0335$. The two findings cannot drift apart, because this finding calls that function rather than reimplementing it.

**F281 leg 2 is not repaired — it is unnecessary.** This route never uses envariance, so the Schlosshauer–Fine objection has nothing to attach to. Leg 2 remains on the record as an independent second argument with its own known gap.

---

## 5. The theorem itself, **proved** — F304 no longer cites Gleason

This section was added on 2026-08-06 - 18:20, after the finding was first issued. Everything above is unchanged; what changes is residual #1, which said *"Gleason's theorem is external and is not reproved here."* It is now reproved, on the class the model needs, and the proof turns out to give **both halves of the dichotomy from a single formula** — including the $d=2$ hole, which §3.1 had merely exhibited by example.

### 5.1 The frame condition is an operator identity

Let $f$ be a frame function on the rays of $\mathbb C^d$: $\sum_i f(e_i)=W$ for every orthonormal basis. Fix a ray $v$. Every orthonormal basis containing $v$ is $v$ together with an orthonormal basis of $v^\perp$, and for a Haar-random such basis each of the remaining $d-1$ vectors is **marginally uniform** on the unit sphere of $v^\perp$. Averaging the frame condition over those bases,

$$\boxed{\ f(v)\ +\ (d-1)\,(Bf)(v)\ =\ W\ },\qquad (Bf)(v):=\underset{w\in S(v^\perp)}{\mathbb E}\,f(w).$$

$B$ commutes with the $U(d)$ action on ray space, so by Schur's lemma it is a **scalar** $b_k$ on each isotypic component $V_k$ of $L^2(\mathbb{CP}^{d-1})$ — $V_0$ the constants, $V_1$ the traceless Hermitian forms, and in general the $(k,0,\dots,0,-k)$ representation with

$$\dim V_k=\binom{k+d-1}{k}^{\!2}-\binom{k+d-2}{k-1}^{\!2}.$$

Component by component the identity reads, for $k\ge1$ (where $W$ contributes nothing),

$$f_k\,\big[\,1+(d-1)\,b_k\,\big]=0 .$$

### 5.2 The eigenvalue, in closed form

For $f$ of pure degree $k$ write $f(v)=\operatorname{Tr}\!\big[M\,(vv^\dagger)^{\otimes k}\big]$ on $\mathrm{Sym}^k$. Averaging $w$ over $S(v^\perp)$ gives, by Schur on the irreducible $\mathrm{Sym}^k(v^\perp)$,

$$\underset{w\in S(v^\perp)}{\mathbb E}\big[(ww^\dagger)^{\otimes k}\big]=\frac{P_k(v^\perp)}{\dim\mathrm{Sym}^k(v^\perp)},\qquad \dim\mathrm{Sym}^k(v^\perp)=\binom{k+d-2}{k},$$

so $B$ is the *zonal* operator whose kernel depends only on $\lvert\langle v,w\rangle\rvert^2$, evaluated at the orthogonality point. Its zonal spherical function on $\mathbb{CP}^{d-1}$ is the Jacobi polynomial $P_k^{(d-2,0)}$, and with $P_k^{(\alpha,\beta)}(-1)=(-1)^k\binom{k+\beta}{k}$, $P_k^{(\alpha,\beta)}(1)=\binom{k+\alpha}{k}$,

$$\boxed{\ b_k\ =\ \frac{P_k^{(d-2,0)}(-1)}{P_k^{(d-2,0)}(1)}\ =\ \frac{(-1)^k}{\binom{k+d-2}{k}}\ }$$

Sanity: $b_0=1$, and $b_1=-1/(d-1)$ — which is just $\mathbb E_{w\in S(v^\perp)}\langle w\rvert H\lvert w\rangle=(\operatorname{Tr}H-\langle v\rvert H\lvert v\rangle)/(d-1)$ for traceless $H$, computable in one line without any of the above.

### 5.3 One formula, both halves of the dichotomy

A component survives iff $1+(d-1)b_k=0$, i.e. iff $k$ is **odd** and $\binom{k+d-2}{k}=d-1$.

**$d=2$.** $\binom{k}{k}=1$ for every $k$, so $b_k=(-1)^k$ and the condition is $1+(-1)^k=0$: **every odd $k$ survives.** The frame-function space is infinite-dimensional, and restricted to harmonic degree $\le K$ its dimension is (using $\dim V_k=2k+1$ at $d=2$)

$$1+\!\!\sum_{\substack{k\ \text{odd}\\ k\le K}}\!\!(2k+1)\ =\ 4,\ 4,\ 11,\ 11,\ 22,\ 22,\ \dots$$

— **the exact sequence §3.3 measured**, before this proof existed. The Born forms are $k\le1$, four dimensions of it. §3.1's explicit $P_3(n_z)$ counterexample is now seen for what it is: the $k=3$ component, the first survivor above Born.

**$d\ge3$.** $\binom{k+d-2}{k}$ is strictly increasing in $k$; it equals $d-1$ at $k=1$, and at $k=2$ it is $\binom{d}{2}=d(d-1)/2>d-1$ strictly, because $d>2$. So for every $k\ge2$,

$$1+(d-1)b_k\ \ge\ 1-\frac{d-1}{\binom{k+d-2}{k}}\ >\ 0 .$$

Only $k=0$ and $k=1$ survive: $f=W/d+\text{(traceless Hermitian form)}$, i.e. $f(v)=\langle v\rvert\rho\lvert v\rangle$, on a space of dimension $1+(d^2-1)=d^2$ — **the integer §3.3 measured at $d=3,4$**. $\blacksquare$

The two cases are not analogous-but-separate arguments. They are $\binom{k}{k}=1$ versus $\binom{k+d-2}{k}>d-1$, in the same line of the same formula. *That* is why $d\ge3$ is the hinge, and it is now an arithmetic fact about binomial coefficients rather than a feature of Gleason's proof one has to take on trust.

### 5.4 Verified, with a control that only bites above the resonance

| Check | What is tested | Result |
|---|---|---|
| **B7a** | $B$'s spectrum on the degree-$\le k$ functions, at $(d,k)=(2,1),(2,3),(3,1),(3,2),(4,1),(4,2)$: eigenvalues vs the closed form, **with $\dim V_k$ multiplicities**, and the function-space dimension vs $\sum_j\dim V_j$ as an integer | $\le1.6\times10^{-15}$; dimensions $4,16,9,36,16,100$ all exact |
| **B7b** | $1+(d-1)b_1=0$ for $d=2..12$, in `Fraction` arithmetic | **exactly $0$** — no floating point anywhere |
| **B7c** | $d\ge3$, $2\le k\le40$: strictly positive, and $\binom{k+d-2}{k}$ strictly increasing | min gap $\mathbf{0.5}$ |
| **B7d** | $d=2$: survivors are exactly $k=1,3,5,7,9,11,\dots$ | exact |
| **B7e** | the proof **predicts** §3.3's measured integers with no fitting | $4,4,11,11,22,22$ and $d^2$, all agreeing |

**The control.** `--param zonal=naive` replaces $b_k$ with $(-1)^k/(d-1)^k$ — a formula that is *correct at $k=0$ and $k=1$* and wrong only from $k=2$. It reds B7a and nothing else. Without it, B7a could be passing on the two trivial modes; with it, the check is shown to test the closed form where the closed form actually does work.

### 5.5 What is still cited — one lemma, not a theorem

The argument of §5.1–5.3 is complete for $f\in L^2$. Gleason's theorem holds for merely **bounded** $f$, and the bridge — that a non-negative frame function is automatically continuous — is the **Cooke–Keane–Moran regularity lemma** (Cooke, Keane & Moran 1985), which is not reproved here.

Stated precisely, so the residual is not larger than it is: every bounded **measurable** weight on a compact ray space lies in $L^2$ and is covered by §5.3. What the lemma excludes is a **non-measurable** weight assignment. That is the whole of the remaining external content, and it is one lemma rather than the theorem.

---

## What this closes, and the premise that remains

**Closes.** Row **A6** moves from *"reproduced in tests, never derived"* to a derivation whose premises are consequences of the rule. The specific hypothesis F281 §2.6 named — *that branch weights are a function of the amplitudes at all* — is now a **conclusion**: Gleason derives both that $w$ is a function of the state and that the function is quadratic.

**Remains, and is not hidden.**

1. ~~**Gleason's theorem is external and is not reproved here.**~~ **CLOSED 2026-08-06 - 18:20 — see §5.** The frame-function theorem is now proved, and the proof gives both halves of the dichotomy from the single closed form $b_k=(-1)^k/\binom{k+d-2}{k}$. What remains external is **one lemma, not a theorem**: Cooke–Keane–Moran regularity, i.e. that a non-negative frame function is automatically continuous. Its content is the exclusion of *non-measurable* weight assignments; every bounded measurable weight on a compact ray space is in $L^2$ and is covered by §5.3. §3.3's rank computations, which were written as evidence for a cited theorem, are now **predictions of the proof** and are checked as integers (B7e).
2. **One premise is irreducible: that an exhaustive set of records carries weights summing to one.** That is the definition of the object being derived, not a physical input. It is strictly weaker than either hypothesis F281 had to carry, and it is the honest end of the regress — no derivation of the Born rule escapes it.
3. **§2.1's context-blindness is proved for the $U(1)$ wrap generator**, inheriting F281's open item 2: the $SU(2)_L$ and $SU(3)_c$ couplings are site-local rotations and are diagonal in position by construction, but the explicit non-Abelian commutator is still not written out. Widening B2 beyond $U(1)$ is the named next step, and it is the same half-session F281 named.
4. **Not an empirical prediction.** Nothing here is falsifiable by experiment; it is falsifiable by the three declared parameter controls, each verified red on its own leg. A model that agrees with quantum mechanics about probabilities is *supposed* to be experimentally indistinguishable at this point (cf. CN1, the settled Bell null).
