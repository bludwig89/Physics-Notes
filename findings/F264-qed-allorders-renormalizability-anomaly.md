# F264 — All-orders QED: renormalizability closure, Ward–Takahashi $Z_1=Z_2$ and charge universality, the Callan–Symanzik equation, and the ABJ anomaly with Nielsen–Ninomiya consistency

**Date:** 2026-07-26 - 14:10
**Status:** Confirmed — 17/17 checks PASS. Fourteen of the seventeen gates are **algebraically exact** (sympy, literal 0 / exact rational): the power-counting formula $D=4-\tfrac32E_f-E_\gamma$ with its order-independence, the counterterm closure to exactly $\{Z_1,Z_2,Z_3,\delta m\}$, the photon-insertion identity that makes Ward–Takahashi hold at every order, $Z_1=Z_2$ as the *unique* solution of the differential WT identity, charge universality, $\beta=e\gamma_3$ and $\beta=e^3/12\pi^2$ from F251's $b_0=\tfrac43$, the $\gamma_5$ trace identities over all 512 index combinations, **two independent exact routes to the ABJ coefficient $\tfrac{1}{16\pi^2}$** (Fujikawa heat kernel and the shift surface term $\tfrac{1}{32\pi^2}$), the vector-safe/axial-anomalous dichotomy, and the Weyl-point census. The remaining three are one numerical scan and two quantitative comparisons ($\pi^0\to\gamma\gamma$ at 0.65%, $0.4\sigma$; the Landau pole).
**Modules:** `ca-simulation/ca_qed_renormalization.py`, `ca-simulation/ca_chiral_anomaly.py`
**Verification script:** `tests/findings/test_F264_qed_allorders_anomaly.py`
**Result file:** `test-results/F264_qed_allorders_anomaly.json`
**Cross-references:** [[F251-qed-vacuum-polarization-running-alpha]] ($\Pi$, $Z_3$, $b_0=\tfrac43$ — the RG input, and the exact transversality that forbids a photon-mass counterterm), [[F252-qed-vertex-ae-lamb-shift]] ($\Lambda$, $Z_1$), [[F258-electron-self-energy]] ($\Sigma$, $Z_2$, $\delta m$; its differential WT identity is the one-loop instance of the all-orders statement proved here), [[F259-ir-bremsstrahlung]] (why the on-shell $Z_2$ finite part is IR-divergent), [[F260-qed-scattering-smatrix]] (the $C=i\gamma^2\gamma^0$ conjugation matrix behind Furry's theorem), [[F263-euler-heisenberg-schwinger-nonlinear-qed]] (the four-photon amplitude that power counting says is **finite** — and the $F\tilde F$-type operator that appears as an anomaly rather than a counterterm), [[F250-allk-gauge-pole-paired-photon]] (the massless transverse gauge pole; and the framing correction below), [[F68-minimal-coupling-forces-even-photon]] / [[F87-charge-coupling-paired-photon]] (the branch-blind identity-channel coupling — why the gauge anomaly is structurally zero), [[F69-paired-spinor-photon]] (the ±-branch pairing that does the mirror-gapping), [[F27-complex-mass-chiral-su2]] / [[F46-pythagorean-lattice-mass]] (the Dirac electron whose mass breaks the chiral charge), [[F26-speed-of-light-as-rotation-rate]] (the BCC walk), [[F75-generation-count-from-oh]] ($N_c=3$, which the $\pi^0$ width tests), [[F107-canonical-a-adopted]] (the lattice cutoff the Landau pole is compared against), [[F162-bgfield-b0-gate]] (the non-abelian $b_0=11$ template).

---

## The claim

F251/F252/F258 computed the three one-loop 1PI functions of the model's QED. Computing loops is not the same as having a theory: a theory needs the statements that hold at *every* order. This finding supplies them, and they hold.

1. **Renormalizability closure.** The superficial degree of divergence of a 1PI QED amplitude is $D=4-\tfrac32E_f-E_\gamma$, with **no dependence on the number of vertices or loops**. Only three amplitudes survive with $D\ge0$ once Furry's theorem and gauge invariance act, and their divergences are absorbed by exactly four counterterms $\{Z_1,Z_2,Z_3,\delta m\}$ — the same four at every order. No non-renormalizable counterterm is ever generated.
2. **Ward–Takahashi to all orders $\Rightarrow$ charge universality.** One exact propagator identity makes $q_\mu\Gamma^\mu(p',p)=S^{-1}(p')-S^{-1}(p)$ telescope diagram by diagram at any order. Its $q\to0$ limit forces $Z_1=Z_2$ as the *unique* solution, hence $e_R=Z_1^{-1}Z_2Z_3^{1/2}e_0=Z_3^{1/2}e_0$: the renormalized charge depends only on the photon field, so every fermion species carries the same charge regardless of its mass.
3. **Renormalization group.** The Callan–Symanzik equation with $\beta(e)=e^3/12\pi^2$ — exactly F251's $b_0=\tfrac43$ — and the all-orders structural relation $\beta(e)=e\,\gamma_3(e)$, itself a consequence of $Z_1=Z_2$.
4. **Chiral anomaly and lattice-doubling consistency.** The axial current carries the ABJ anomaly with coefficient $\tfrac{1}{16\pi^2}$, reached by two independent exact routes; the vector (gauge) current is anomaly-free *structurally*, because the F68/F87 coupling is branch-blind; and the Nielsen–Ninomiya no-go is threaded correctly, with the mechanism identified precisely (and one plausible-sounding mechanism ruled out).

---

## Part 1 — Renormalizability closure

### R1 — the degree of divergence, and why it does not grow (exact)

For a 1PI diagram with $L$ loops, $I_f$ internal fermion lines, $I_\gamma$ internal photon lines and $V$ vertices, $D=4L-I_f-2I_\gamma$. The QED topology fixes

$$L=I_f+I_\gamma-V+1,\qquad 2V=2I_f+E_f,\qquad V=2I_\gamma+E_\gamma,$$

and eliminating $I_f,I_\gamma,L$ gives

$$\boxed{\,D=4-\tfrac32E_f-E_\gamma\,}$$

with $\partial D/\partial V=\partial D/\partial L=0$ **identically** (sympy, literal 0). That cancellation *is* renormalizability: the divergence structure of a diagram depends only on its external legs, never on how complicated its interior is. A theory with a dimensionful coupling would leave a $+cV$ term here and would need an unbounded tower of counterterms.

### R2 — the census: exactly three divergent amplitudes (exact)

$E_f$ is even, so $D\ge0$ leaves a short finite list. Two reductions then act:

| $E_f$ | $E_\gamma$ | amplitude | $D$ naive | $D$ effective | verdict | counterterm |
|---|---|---|---|---|---|---|
| 0 | 0 | vacuum bubble | 4 | 4 | no external legs — normalisation | — |
| 0 | 1 | photon tadpole | 3 | — | **vanishes** by Furry / $C$-parity | — |
| 0 | 2 | $\Pi^{\mu\nu}$ | 2 | 0 | log-divergent after transversality | $Z_3$ |
| 0 | 3 | three-photon | 1 | — | **vanishes** by Furry / $C$-parity | — |
| 0 | 4 | four-photon box | 0 | $-4$ | **finite** (gauge invariance) | — |
| 2 | 0 | $\Sigma$ | 1 | 0 | log in both $A$ and $B$ | $\delta m$, $Z_2$ |
| 2 | 1 | $\Lambda^\mu$ | 0 | 0 | log-divergent | $Z_1$ |
| 4 | 0 | four-fermion | $-2$ | — | **not generated** | — |

Two entries deserve emphasis because the model's own results are what close them:

- **$\Pi^{\mu\nu}$**: the naive $D=2$ would permit a photon-mass divergence $g^{\mu\nu}\Lambda^2$. F251/Pi1 computes $q_\mu\Pi^{\mu\nu}=0$ exactly, forcing $\Pi^{\mu\nu}=(q^2g^{\mu\nu}-q^\mu q^\nu)\Pi(q^2)$, so only the log in $\Pi(q^2)$ diverges. No photon mass is generated at any order, and F250's gauge pole stays massless across the whole Brillouin zone.
- **the four-photon box**: naively log-divergent, but gauge invariance makes each external photon enter through $F_{\mu\nu}$, costing four momentum factors — $D_{\text{eff}}=-4$. So the model's light-by-light amplitude (F263, Euler–Heisenberg) needs **no counterterm** and is a genuine prediction rather than a fit.

### R3 — the operator-basis dual (exact)

The same statement in operator language. Enumerating every Lorentz-scalar, $U(1)$-gauge-invariant, hermitian, $P$- and $C$-even local operator of mass dimension $\le4$ built from $\{\psi,A_\mu,\partial_\mu\}$ leaves **exactly four**:

$$\bar\psi\,i\gamma^\mu\partial_\mu\psi\ (Z_2),\qquad e\,\bar\psi\gamma^\mu A_\mu\psi\ (Z_1),\qquad m\bar\psi\psi\ (\delta m),\qquad F_{\mu\nu}F^{\mu\nu}\ (Z_3).$$

The two instructive near-misses:

- $A_\mu A^\mu$ (dim 2, a photon mass) — excluded by gauge invariance, which here is not an assumption but F251/Pi1 and F250.
- $F_{\mu\nu}\tilde F^{\mu\nu}$ (dim 4, the $\theta$ term) — excluded by parity, and a total derivative. **This is exactly the operator the axial anomaly multiplies** (Part 4). There is no contradiction: it is forbidden as a term in the action while being generated as the divergence of a current.

Dimension-6 and above ($(\bar\psi\psi)^2$, $(F^2)^2$) are not generated, consistent with $D<0$.

---

## Part 2 — Ward–Takahashi to all orders, and charge universality

### R4 — the photon-insertion identity and the telescope (exact)

Everything rests on one identity. With $S(p)=(\slashed p-m)^{-1}$ and $q=p'-p$, since $\slashed q=S^{-1}(p')-S^{-1}(p)$,

$$\boxed{\,S(p')\,\slashed q\,S(p)=S(p)-S(p')\,}\tag{$*$}$$

verified to literal zero with explicit $4\times4$ gammas, four symbolic momentum components and symbolic mass (the closed-form propagator's exactness as the inverse of $\slashed p-m$ is checked in the same tier).

**Why it holds at every order.** Take any diagram at any order and any continuous fermion line through it carrying momenta $k_0,\dots,k_n$. Inserting the external photon vertex *adds* a propagator: $S(k_i)\to S(k_i+q)\,\slashed q\,S(k_i)$ — the same momentum $k_i$ on both sides of $\slashed q$, which is precisely $(*)$'s form. Propagators downstream of the insertion pick up $q$; upstream ones do not. Defining

$$T_i:=\Big[\prod_{j\ge i}S(k_j+q)\Big]\Big[\prod_{j<i}S(k_j)\Big],$$

insertion at position $i$ contributes exactly $T_{i+1}-T_i$, so summing over the $n+1$ insertion points **telescopes**:

$$\sum_{i=0}^{n}\big(T_{i+1}-T_i\big)=T_{n+1}-T_0=(\text{all unshifted})-(\text{all shifted}).$$

Every interior term cancels against its neighbour and only the two ends survive; amputating the external legs gives $q_\mu\Gamma^\mu(p',p)=S^{-1}(p')-S^{-1}(p)$. Nothing in the argument mentions the order in $e$: internal photons and loop momenta are spectators.

On this lattice the two prerequisites are supplied rather than assumed. The coupling is the F68/F87 identity-channel vertex $P=e^{iqA\cdot d\ell}\,\mathbb I_2$, whose branch-blindness puts the **same** $\gamma^\mu$ at every attachment point (a branch-dependent vertex would spoil the telescope), and the internal photon is the F69/F250 paired photon, diagonal in polarisation.

The assembled chain telescope was also verified directly for $n=1,2,3,4$ — inserting $\slashed q$ at each of the $n+1$ positions and summing, against an independently built right-hand side containing no $\slashed q$ anywhere — in exact rational arithmetic over several generic momentum draws. *(Tiering, stated honestly: $(*)$ is the fully symbolic exact gate and is the whole content; the chain checks are exact-arithmetic confirmations of the one-line induction, not a second proof. Fully symbolic 4-momentum chains of length 4 are not tractable in sympy and would add nothing.)*

### R5 — $Z_1=Z_2$ as the unique solution (exact)

Letting $q\to0$ in the WT identity gives the **differential** WT identity

$$\Gamma^\mu(p,p)=\frac{\partial S^{-1}(p)}{\partial p_\mu},$$

whose one-loop instance F258/S3 already computed ($\partial\Sigma/\partial p_\mu=-\Lambda^\mu(p,p)$). Inserting the renormalized definitions $S^{-1}(p)=Z_2^{-1}(\slashed p-m)$ (residue $Z_2$ at the physical pole) and $\Gamma^\mu(p,p)=Z_1^{-1}\gamma^\mu$:

$$Z_1^{-1}\gamma^\mu=\frac{\partial}{\partial p_\mu}\Big[Z_2^{-1}(\slashed p-m)\Big]=Z_2^{-1}\gamma^\mu\quad\Longrightarrow\quad \boxed{Z_1=Z_2}$$

Solved entry by entry from the matrix equation for every $\mu$: the unique solution is $Z_1=Z_2$. Because the WT identity holds at every order (R4), so does this. The one-loop instance checks out against F252 and F258, whose log coefficients are both $-\alpha/4\pi$.

### R6 — charge universality (exact)

$$e_R=Z_1^{-1}Z_2Z_3^{1/2}e_0\ \xrightarrow{\ Z_1=Z_2\ }\ e_R=Z_3^{1/2}e_0.$$

$Z_1$ and $Z_2$ *are* species-dependent — at one loop each carries $\ln(\Lambda^2/m_f^2)$, verified here to be genuinely different for two species of different mass — but that dependence cancels identically, and the difference $e_R^{(1)}-e_R^{(2)}$ is literal 0. The renormalized charge depends only on the photon field's renormalization.

This is why $|q_e|=|q_\mu|=|q_\tau|=|q_p|$ **exactly** rather than approximately, despite masses differing by orders of magnitude — a fact measured to $\sim10^{-21}$. ($Z_3$ of course receives a contribution from every species in the loop; that is the $b_0=\tfrac43$ flavour sum. The point is that every species then sees the *same* $Z_3$.)

---

## Part 3 — The renormalization group

### R7 — the Callan–Symanzik equation (exact)

$$\left[\mu\frac{\partial}{\partial\mu}+\beta(e)\frac{\partial}{\partial e}+n\,\gamma_2(e)+m\,\gamma_3(e)\right]\Gamma^{(n,m)}\big(\{p\};e,\mu\big)=0$$

with $\beta=\mu\,de/d\mu$ and $\gamma_i=\tfrac12\mu\,d\ln Z_i/d\mu$. F251/Pi2 gives $\mu\,d\alpha/d\mu=2\alpha^2/3\pi$ ($b_0^{\text{QED}}=\tfrac43$); with $\alpha=e^2/4\pi$ this is $\mu\,d\alpha/d\mu=(e/2\pi)\beta$, so

$$\beta(e)=\frac{e^3}{12\pi^2},\qquad \gamma_3=\frac{\alpha}{3\pi}=\frac{e^2}{12\pi^2},\qquad \gamma_2=\frac{\alpha}{4\pi}\ \ (\text{Feynman gauge}).$$

Both directions of the $b_0$ conversion are exact rationals (reading $b_0$ back out of $\beta$ returns exactly $\tfrac43$); nothing is fitted.

**The structural relation.** Because $Z_1=Z_2$, $e_R=Z_3^{1/2}e_0$ with $e_0$ independent of $\mu$, so differentiating gives

$$\boxed{\,\beta(e)=e\,\gamma_3(e)\,}\qquad\text{exactly, to all orders.}$$

The entire QED beta function is carried by the photon field's anomalous dimension; the fermion sector cannot contribute to it. Verified as a literal identity at one loop. This is the RG-level restatement of charge universality: the running of the coupling is a property of the photon, not of whichever fermion is probing it.

$\gamma_2$ is gauge-**dependent**, as is $Z_2$. That is not a defect — $\gamma_2$ is not an observable. The gauge-independent content is $\beta$ (equivalently $\gamma_3$) and the physical combinations F252/F258/F259 assemble into cross sections.

### R8 — the Landau pole, stated honestly (quantitative)

$$\alpha(\mu)=\frac{\alpha_0}{1-\frac{\alpha_0}{3\pi}\ln(\mu^2/\mu_0^2)},\qquad \mu_L=m_e\exp\!\Big(\frac{3\pi}{2\alpha_0}\Big)\approx10^{277}\ \text{GeV}.$$

QED is not asymptotically free and the one-loop coupling has a spurious pole. Two caveats, in order of importance:

1. The pole is an artefact of extrapolating a one-loop formula ~640 e-foldings beyond where it was fitted; the electroweak and QCD embeddings change the running long before then. Nothing here claims the formula is valid at $\mu_L$.
2. **Specific to this model**: the lattice supplies a *physical* UV cutoff. With the F107 canonical ruler $a=6.5978\,\ell_P$, $\Lambda_a=\hbar c/a\approx1.9\times10^{18}$ GeV — and $\mu_L$ sits **259 decades above it**. In this model the Landau pole is not merely unreached in practice; it lies outside the theory's domain of definition, because there are no momenta beyond the Brillouin zone. Continuum QED owes an apology for the Landau pole; a lattice QED does not.

That is a structural remark, not a resolution of the continuum problem, and is recorded as such.

---

## Part 4 — The chiral anomaly and lattice-doubling consistency

A lattice Weyl construction claiming to *be* QED has to thread a narrow gap. The **vector** (gauge) current must be exactly conserved, or the gauge symmetry is anomalous and the Ward identities of Parts 1–3 are false. The **axial** current must *not* be conserved — it must carry precisely the ABJ anomaly, because that anomaly is measured. And Nielsen–Ninomiya says a lattice cannot simply wish for this.

### A1 — $\gamma_5$ and the trace identities (exact)

$\gamma_5=i\gamma^0\gamma^1\gamma^2\gamma^3$ in the F252/F258 basis: $\gamma_5^2=1$, $\{\gamma_5,\gamma^\mu\}=0$, hermitian, with $P_{L,R}=(1\mp\gamma_5)/2$ idempotent, orthogonal and complete. The traces the anomaly needs, verified over **all** index combinations:

$$\mathrm{Tr}[\gamma_5\gamma^\mu\gamma^\nu]=0\ (16),\qquad \mathrm{Tr}[\gamma_5\gamma^\mu\gamma^\nu\gamma^\rho\gamma^\sigma]=-4i\,\epsilon^{\mu\nu\rho\sigma}\ (256),$$
$$\mathrm{Tr}[\gamma_5\sigma^{\mu\nu}\sigma^{\rho\sigma}]=+4i\,\epsilon^{\mu\nu\rho\sigma}\ (256).$$

The relative sign of the last two is forced by $\sigma^{\mu\nu}=\tfrac i2[\gamma^\mu,\gamma^\nu]$, not chosen: $\sigma\sigma=-\tfrac14[\gamma,\gamma][\gamma,\gamma]$, and under $\mathrm{Tr}[\gamma_5\,\cdot\,]$ only the four-gamma piece survives, giving $-\tfrac14\cdot4\cdot(-4i\epsilon)=+4i\epsilon$. This four-gamma trace is the **only** source of $\epsilon^{\mu\nu\rho\sigma}$ in the anomaly, which is why the anomaly multiplies $\epsilon FF$ (i.e. $\mathbf E\cdot\mathbf B$) and nothing else.

### A2 — the classical baseline (exact)

$$\partial_\mu\big(\bar\psi\gamma^\mu\psi\big)=0\ \ (\text{any }m),\qquad \partial_\mu\big(\bar\psi\gamma^\mu\gamma_5\psi\big)=2im\,\bar\psi\gamma_5\psi.$$

One commutator separates them: $\gamma_5$ **anti**commutes with the kinetic term $\slashed p$ but **commutes** with the mass term $m\mathbb 1$ (both verified to literal zero). In the axial case the sign flip makes the two kinetic contributions cancel while the two mass contributions add.

So the model has **no exactly conserved chiral charge to begin with**: its electron is the massive Dirac fermion of F27/F46, whose complex mass couples the two chiral branches. That will matter in A6/A8. The *anomaly* is the statement that the right-hand side does not vanish as $m\to0$ — the quantum theory adds an $m$-independent piece.

### A3 — the coefficient, route 1: Fujikawa (exact)

Under a local chiral rotation the fermion **measure** is not invariant; its Jacobian is a regulated $\gamma_5$ trace. Three exact ingredients:

1. $\slashed D^2=D^2+\tfrac e2\sigma^{\mu\nu}F_{\mu\nu}$ exactly (from $[D_\mu,D_\nu]=-ieF_{\mu\nu}$; the Clifford split $\gamma^\mu\gamma^\nu=\eta^{\mu\nu}+\sigma^{\mu\nu}/i$ verified to literal zero). The only non-scalar piece of the heat-kernel exponent is a single power of $\sigma\!\cdot\!F$.
2. $\mathrm{Tr}[\gamma_5\times(\text{fewer than two }\sigma)]=0$, and $\mathrm{Tr}[\gamma_5\sigma\sigma]=+4i\epsilon$ (A1). So **only the second-order term** of the exponential survives — which is what makes the anomaly a two-photon object.
3. $\displaystyle\int\!\frac{d^4k_E}{(2\pi)^4}e^{-k^2/\Lambda^2}=\frac{\Lambda^4}{16\pi^2}$ exactly.

**The regulator cancels.** Ingredient 2 supplies $1/\Lambda^4$ and ingredient 3 supplies $\Lambda^4$; their product is a pure rational over $\pi^2$ with no $\Lambda$ left ($\partial/\partial\Lambda=0$ verified). That manifest cancellation is why the coefficient is regulator-independent even though the anomaly is "the" scheme-dependent piece of the naive calculation. Assembling,

$$\boxed{\,\partial_\mu j_5^\mu=2im\,\bar\psi\gamma_5\psi-\frac{e^2}{16\pi^2}\,\epsilon^{\mu\nu\rho\sigma}F_{\mu\nu}F_{\rho\sigma}\,}$$

and the equivalent normalisations check against each other: $\epsilon^{\mu\nu\rho\sigma}F_{\mu\nu}F_{\rho\sigma}=-8\,\mathbf E\cdot\mathbf B$ and $e^2=4\pi\alpha$ give $\partial_\mu j_5^\mu\big|_{\text{anom}}=\tfrac{2\alpha}{\pi}\mathbf E\cdot\mathbf B$, and $e^2/16\pi^2=\alpha/4\pi$.

*On signs, honestly:* the gate tests the **magnitude** $\tfrac{1}{16\pi^2}$, which is what is physical and regulator-independent and what $\pi^0\to\gamma\gamma$ measures. The overall sign is fixed by a convention chain ($\epsilon^{0123}=+1$, the ordering inside $\gamma_5$, the sign of $e$, the Euclidean continuation route); it is recorded, not tuned. In the stated conventions the assembly returns $-e^2/16\pi^2$ on its own.

### A4 — the coefficient, route 2: the shift surface term (exact, independent)

The AVV triangle is only **linearly** divergent, so shifting its loop momentum is illegitimate and leaves a finite surface term. That freedom is exactly what the anomaly removes: once the two vector Ward identities are imposed — as they must be — the leftover is forced into the axial channel. For the canonical linearly divergent integrand $f^\mu(k)=k^\mu/(k^2+D)^2$,

$$\int\!\frac{d^4k}{(2\pi)^4}\big[f^\mu(k+a)-f^\mu(k)\big] =a^\mu\frac{1}{16\pi^2}\int_0^\infty\!\frac{D\,t\,dt}{(t+D)^3} =a^\mu\frac{1}{16\pi^2}\cdot D\cdot\frac{1}{2D} =\boxed{\frac{a^\mu}{32\pi^2}}$$

Three features, all verified symbolically: the two individually **log-divergent** pieces cancel, so the surface term is finite; the result is exactly **$D$-independent** (the $D$ cancels the $1/D$), which is required since the measured ABJ coefficient does not depend on the fermion mass; and $\tfrac{1}{16\pi^2}/\tfrac{1}{32\pi^2}=2$ exactly — the two chiralities (A5).

So a heat-kernel trace over the measure and a boundary term at infinity, two arguments with nothing in common, reach the same rational. Neither is fitted to the other.

### A5 — why the same triangle is safe for gauge and fatal for axial (exact)

The anomaly of a single chiral branch is $\pm\mathcal A_0$, signed by chirality. A current inherits whatever weighting it assigns the branches, and since $\gamma^\mu=\gamma^\mu(P_L+P_R)$ while $\gamma^\mu\gamma_5=\gamma^\mu(P_R-P_L)$ (both verified to literal zero):

| current | branch weights | anomaly |
|---|---|---|
| vector $\bar\psi\gamma^\mu\psi$ | $(+1,+1)$ | $(+1)(+\mathcal A_0)+(+1)(-\mathcal A_0)=0$ |
| axial $\bar\psi\gamma^\mu\gamma_5\psi$ | $(-1,+1)$ | $(-1)(+\mathcal A_0)+(+1)(-\mathcal A_0)=-2\mathcal A_0$ |

The gauge current is anomaly-free; the axial current carries twice the per-branch anomaly — and that factor 2 is precisely the one relating A4's $\tfrac{1}{32\pi^2}$ to $\tfrac{1}{16\pi^2}$.

**The model-specific point.** In a generic chiral gauge theory the $(+1,+1)$ vector weighting is a *choice* of charge assignment, and gauge-anomaly freedom is a constraint one imposes on the spectrum ($\sum_f q_f^3=0$). Here it is not a choice. The $U(1)$ coupling is the F68/F87 identity-channel vertex

$$P=e^{iqA\cdot d\ell}\,\mathbb I_2,$$

proportional to the **identity** in branch space — branch-blind, with no $X$ (branch-mixing) component (F168; verified here as $\mathrm{tr}(\sigma_xP)=0$ and $[P,\sigma_z]=0$). It therefore assigns the two chiral branches the same charge by construction: **the model's $U(1)$ is vector-like structurally, and the gauge anomaly is zero structurally rather than by arithmetic cancellation.** This is the same branch-blindness that F68 showed forces the photon onto the even law and that F251/Pi1 needs for exact transversality.

### A6 — the Weyl-point census in the *true* Brillouin zone (exact)

**The true BZ is not the cube.** The walk hops along $d\in\{\pm1\}^3$ with phases $e^{iq\cdot d}$ ($q=k/\sqrt3$). Two momenta are identical iff $G\cdot d\in2\pi\mathbb Z$ for all eight $d$ — satisfied by $\pi(1,1,0),\pi(1,0,1),\pi(0,1,1)$. The reciprocal lattice is **fcc**, the true BZ has volume $2\pi^3=(2\pi)^3/4$, and the cube $[-\pi,\pi]^3$ holds exactly **4 copies** of it. A census run on the cube therefore counts every Weyl point four times — which is why a naive scan appears to show 8 zeros per branch when there are really 2.

Per chiral branch, in the true BZ (chirality = $\mathrm{sign}\det(\partial n_i/\partial q_j)$, the Berry monopole charge of the walk's Bloch vector, computed symbolically — no eigen-decomposition of a chiral matrix, per CLAUDE.md):

| branch | point | $u$ | $\omega$ | $\chi$ | partner branch $u$ | partner $\omega$ |
|---|---|---|---|---|---|---|
| $+$ | $\Gamma=(0,0,0)$ | $+1$ | $0$ | $-1$ | $+1$ | $0$ (gapless) |
| $+$ | $R=\tfrac\pi2(1,1,1)$ | $+1$ | $0$ | $+1$ | $-1$ | $\pi$ (**band top**) |
| $-$ | $\Gamma=(0,0,0)$ | $+1$ | $0$ | $+1$ | $+1$ | $0$ (gapless) |
| $-$ | $R=\tfrac\pi2(1,1,-1)$ | $+1$ | $0$ | $-1$ | $-1$ | $\pi$ (**band top**) |

$\sum\chi=0$ per branch, as Nielsen–Ninomiya requires, and the determinants come out exactly $\pm1$. **Two Weyl points is the minimum a lattice permits** — the BCC walk is a *minimal* lattice Weyl fermion, not a coarse one with $2^d$ doublers.

**The decisive extra fact.** At $q=\tfrac\pi2(a,b,c)$ every cosine vanishes and $s_xs_ys_z=abc$, so $u^\pm=0\pm abc$ — hence exactly one branch is gapless and its **partner sits at $u=-1$, i.e. $\omega=\pi$, the very top of the band.** All of this is exact algebra, not numerics. Since a light *Dirac* mode requires both branches gapless at the same momentum (the F27/F46 mass is what couples them), that happens at $\Gamma$ and nowhere else.

An independent numerical BZ scan ($61^3$) confirms the census: 8 zeros per branch modulo $2\pi$ on the cube, folding under the fcc reciprocal lattice to exactly 2 — $\Gamma$ plus one half-integer corner. Nothing was missed by looking only at the closed-form points.

### A7/A8 — Nielsen–Ninomiya, threaded correctly

**The no-go, precisely.** A lattice fermion that is (a) local, (b) translation invariant, (c) hermitian, and (d) has an exactly conserved, local, quantized chiral charge has Weyl points in opposite-chirality pairs summing to zero — so any anomaly cancels between a mode and its mirror, and the continuum ABJ result *cannot* be reproduced.

Which hypothesis fails here:

| hypothesis | holds? | why |
|---|---|---|
| locality | **yes** | 8 nearest-neighbour BCC hops, finite range |
| translation invariance | **yes** | the walk is a convolution, diagonal in Fourier space |
| hermiticity / unitarity | **yes** | $U(q)=u\mathbb I-i\boldsymbol\sigma\!\cdot\!\mathbf n$ with $u^2+\lvert\mathbf n\rvert^2=1$ |
| exactly conserved local chiral charge | **NO** | the physical fermion is the F27/F46 **Dirac** electron; its mass couples the two branches and anticommutes with $\gamma_5$ (A2) |

Exactly one hypothesis fails, and not by a contrivance. This is the same escape route Wilson fermions use, with one difference worth stating: for Wilson fermions the chirality-breaking term is an artefact added by hand and tuned away in the continuum limit, whereas here it is the **physical electron mass**.

So the no-go's *conclusion* does not apply, and the census shows how the light spectrum ends up anomalous **without violating the topological sum rule**: $\sum\chi=0$ over the whole BZ (NN respected, not evaded), but the two members of the pair are not equivalent —

- **$\Gamma$**: both branches gapless ($u^+=u^-=1$ exactly) → the mass pairs them into one light Dirac mode, which carries the full continuum anomaly $\tfrac{1}{16\pi^2}$;
- **$R$**: partner branch at $\omega=\pi$ → no light Dirac partner, so the NN-mandated mirror is gapped at the lattice scale and removed from the low-energy theory.

Structurally this is the **momentum-space analogue of domain-wall / overlap fermions**, where the mirror chirality is exiled to a far wall in an extra dimension; here the ±-branch structure does the exiling inside the existing Brillouin zone.

Separately, the gauge side is safe on two counts: the current is anomaly-free structurally (A5), and F250 shows the gauge *boson* has a single massless transverse pole with no doubler copy, so there is no spurious second gauge current either.

### Honest correction to the motivating framing

It is tempting to say the F250 doubler-folding — the paired photon's $k/2$ sharing pushing its would-be doubler pole to $\lvert k_i\rvert=2\pi$, outside the photon BZ — is what leaves the axial anomaly uncancelled. **That is not the mechanism**, and it is recorded here as a correction rather than quietly assumed:

- The anomaly arises from a fermion **loop** whose momentum is integrated over the whole **fermion** Brillouin zone. It therefore samples every Weyl point no matter how small the external photon momenta are. Restricting the photon's momentum range cannot remove a doubler's contribution to a loop.
- What actually does the work is the mirror-point gapping of A6 — a property of the **fermion** spectrum, not the photon's.

The two statements do share a root cause: both follow from the ±-branch pairing of F69, which is presumably why they are easy to conflate. But they are two statements, and the anomaly depends on the fermion one. F250's result stands exactly as F250 stated it — a claim about the gauge-boson spectrum.

### A9 — the anomaly is measured: $\pi^0\to\gamma\gamma$ (quantitative)

$$\Gamma(\pi^0\to\gamma\gamma)=\frac{\alpha^2m_{\pi^0}^3}{64\pi^3f_\pi^2},$$

where the $1/64\pi^3$ descends directly from the $\tfrac{1}{16\pi^2}$ of A3/A4. With $m_{\pi^0}=134.977$ MeV, $f_\pi=92.28$ MeV, $\alpha^{-1}=137.036$:

| | value |
|---|---|
| model | **7.749 eV** |
| PDG | $7.80\pm0.12$ eV |
| relative error | **0.65%** ($0.42\sigma$) |

**Where $N_c$ enters.** The quark-level coefficient for this channel is $\sum_qN_c(q_u^2-q_d^2)=N_c(\tfrac49-\tfrac19)=N_c/3$, which equals exactly 1 for $N_c=3$ — and the formula assumes that 1. So this single number tests the anomaly coefficient **and** the model's colour count simultaneously (F75 derives $N_c=3$ from $O_h$ rather than assuming it):

| | $N_c=2$ | $N_c=3$ | $N_c=4$ |
|---|---|---|---|
| predicted width (eV) | 3.44 | **7.75** | 13.78 |
| error vs PDG | $-56\%$ | $+0.65\%$ | $+77\%$ |

Nothing is fitted: $m_\pi$, $f_\pi$ and $\alpha$ are inputs and the rational prefactor is the anomaly. This is one of the few places where a colour *count* is directly visible in an electromagnetic decay rate.

---

## Verification summary (17/17)

| gate | quantity | tier | result |
|---|---|---|---|
| R1 | $D=4-\tfrac32E_f-E_\gamma$; $\partial D/\partial V=\partial D/\partial L=0$ | exact | PASS |
| R2 | only $\Sigma,\Pi,\Lambda$ diverge; 4-photon finite; 4-fermion $D=-2$ | exact | PASS |
| R3 | dim $\le4$ operator basis $=\{Z_1,Z_2,Z_3,\delta m\}$ | exact | PASS |
| R4 | $S(p')\slashed qS(p)=S(p)-S(p')$; chain telescope $n=1..4$ | exact / exact-rational | PASS |
| R5 | differential WT $\Rightarrow Z_1=Z_2$ unique, every $\mu$ | exact | PASS |
| R6 | $e_R=Z_3^{1/2}e_0$ species-independent (two masses) | exact | PASS |
| R7 | CS equation; $\beta=e^3/12\pi^2$; $b_0=\tfrac43$; $\beta=e\gamma_3$ | exact | PASS |
| R8 | $\mu_L\approx10^{277}$ GeV, 259 decades above $\Lambda_a$ | quantitative | PASS |
| A1 | $\gamma_5$ algebra; 512 trace combinations | exact | PASS |
| A2 | vector conserved; axial $=2im\bar\psi\gamma_5\psi$ | exact | PASS |
| A3 | Fujikawa $\lvert$coeff$\rvert=\tfrac{1}{16\pi^2}$; regulator cancels | exact | PASS |
| A4 | surface term $\tfrac{1}{32\pi^2}$, $D$-independent; ratio 2 | exact | PASS |
| A5 | $\mathcal A_V=0$, $\mathcal A_A=-2\mathcal A_0$; branch-blind $U(1)$ | exact | PASS |
| A6 | 2 Weyl points/branch, $\sum\chi=0$; mirror partner at $\omega=\pi$ | exact | PASS |
| A7 | $61^3$ scan: 8 mod $2\pi$ → 2 under fcc folding | numerical | PASS |
| A8 | exactly one NN hypothesis fails | structural | PASS |
| A9 | $\Gamma(\pi^0\to\gamma\gamma)=7.749$ eV vs $7.80\pm0.12$ | quantitative | PASS |

---

## Why this matters

One-loop QED closed with F258. This is the statement that the model's QED is a **theory**: renormalizable with a closed four-element counterterm set at every order, gauge-anomaly-free with charge universality following from an all-orders Ward identity, equipped with an RG whose beta function is carried entirely by the photon, and reproducing the ABJ anomaly with the correct coefficient by two independent routes while satisfying Nielsen–Ninomiya rather than quietly violating it.

Three results are specific to *this* model rather than restatements of textbook QED:

1. **The gauge anomaly vanishes structurally, not by charge bookkeeping.** The F68/F87 identity-channel coupling is branch-blind, so the $U(1)$ is vector-like by construction. There is no anomaly-cancellation condition to impose on the spectrum.
2. **The BCC walk is a *minimal* lattice Weyl fermion** — 2 Weyl points per branch in the true fcc BZ, not $2^d$ — and the NN-mandated mirror is gapped at the band top by the ±-branch structure. The model realizes the domain-wall/overlap mechanism in momentum space, using the same pairing that makes the photon (F69).
3. **The Landau pole lies outside the theory's domain of definition**, 259 decades above the F107 Brillouin-zone cutoff. A lattice theory does not inherit the continuum's UV embarrassment.

---

## Scope and honesty ledger

- **Exact (sympy, literal 0 / exact rational):** R1 (with the $V$- and $L$-independence); R2/R3 closure; R4's core identity $(*)$ (fully symbolic, four symbolic momenta + symbolic mass); R5 $Z_1=Z_2$ solved uniquely per $\mu$; R6 universality; R7 $\beta$, $b_0$, $\gamma_3$, $\beta=e\gamma_3$; A1 (512 combinations); A2; A3 (including the manifest $\Lambda$ cancellation); A4 (including $D$-independence and the factor 2); A5; A6 (chiralities exactly $\pm1$; $u^\pm=0\pm abc$ at the corners).
- **Exact rational arithmetic, generic momenta (not a second symbolic proof):** R4's assembled chain telescope for $n=1..4$. The symbolic content is $(*)$; the telescope follows from it by a one-line induction given in the module docstring.
- **Numerical:** A7's $61^3$ BZ scan (a completeness check on the closed-form census, not the census itself).
- **Quantitative:** A9 $\pi^0\to\gamma\gamma$ (0.65%, $0.42\sigma$); R8's Landau-scale comparison.
- **Structural / argued rather than computed:** A8's identification of *which* NN hypothesis fails. The failure itself is exact (A2's $\{\gamma_5,m\}\ne0$), but "this is the same escape route as Wilson fermions" is a classification, not a theorem.
- **Sign conventions:** the anomaly gate tests the magnitude $\tfrac{1}{16\pi^2}$. The overall sign depends on a convention chain ($\epsilon^{0123}$, the ordering in $\gamma_5$, the sign of $e$, the Euclidean route) and is documented, not tuned. In the stated conventions the assembly independently returns $-e^2/16\pi^2$.
- **Corrected framing (recorded, not buried):** the F250 paired-photon doubler-folding is **not** the mechanism that keeps the axial anomaly uncancelled; the mirror-point gapping of A6 is. See the correction subsection above.
- **Out of scope:** the full AVV triangle computed diagram-by-diagram with its vector-Ward redistribution (the two routes here reach the coefficient without it); non-abelian anomalies and the electroweak $\sum Y^3$ conditions (the $SU(2)\times U(1)$ sector, not this one); the anomaly's two-loop non-renormalization (Adler–Bardeen) — stated in the literature, not verified here; $f_\pi$ is an input, not derived from the model's QCD sector (F151/F152).

---

## External references

- F. J. Dyson, *Phys. Rev.* **75**, 1736 (1949) — the S-matrix, renormalization, and the counterterm program.
- J. C. Ward, *Phys. Rev.* **78**, 182 (1950); Y. Takahashi, *Nuovo Cim.* **6**, 371 (1957) — the Ward–Takahashi identity and $Z_1=Z_2$.
- C. G. Callan, *Phys. Rev. D* **2**, 1541 (1970); K. Symanzik, *Commun. Math. Phys.* **18**, 227 (1970) — the renormalization-group equation.
- S. L. Adler, *Phys. Rev.* **177**, 2426 (1969); J. S. Bell & R. Jackiw, *Nuovo Cim. A* **60**, 47 (1969) — the ABJ axial anomaly.
- K. Fujikawa, *Phys. Rev. Lett.* **42**, 1195 (1979) — the anomaly as the fermion-measure Jacobian (route A3).
- S. L. Adler & W. A. Bardeen, *Phys. Rev.* **182**, 1517 (1969) — non-renormalization of the anomaly.
- H. B. Nielsen & M. Ninomiya, *Nucl. Phys. B* **185**, 20 (1981); **193**, 173 (1981) — the fermion-doubling no-go.
- D. B. Kaplan, *Phys. Lett. B* **288**, 342 (1992); R. Narayanan & H. Neuberger, *Nucl. Phys. B* **443**, 305 (1995) — domain-wall / overlap fermions (the mechanism A6/A8 parallels).
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §10 (power counting), §12 (Callan–Symanzik), §19 (the axial anomaly).
- Particle Data Group, *Review of Particle Physics* (2024) — $\Gamma(\pi^0\to\gamma\gamma)$, $f_\pi$.
