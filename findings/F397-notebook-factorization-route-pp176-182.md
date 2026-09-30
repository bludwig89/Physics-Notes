# F397 — The notebook's factorization route (pp.176–182): an exact, boost-covariant algebraic identity that is structurally true, redundant with F168/F169 for binding, and adds one derived number — the F169 offset coefficient

**Date:** 2026-09-21 - 13:30
**Status:** Confirmed as a bounded structural result — 19/19 gate legs PASS (algebraic legs machine, lattice legs quantitative; record class quantitative). **Outcome (b) with a partial (a):** the route is REDUNDANT with F168/F169 for the binding question and does NOT predict $g_c$; it does deliver one derived coefficient (the F169 $O(k^2)$ offset, leading order, exact form) and closes the free-phase-as-EM-$U(1)$ reading negatively and finds no correspondence for the $\hat a\leftrightarrow$ W/Z readings (these readings come from this session's framing of the route, not from the notebook text).
**Module:** `src/casim/engine/gauge/factorization.py`
**Test record:** `F397-factorization-route` (gate, quantitative)
**Claim:** CL309
**Checked:** 2026-09-21 — 13 attacks: 5 PASS / 7 WEAKENS / 1 FAIL (fixed) / 1 NOT RUN — **CONFIRMED-NARROWER**
**Cross-references:** [[F24-sl2c-boost-4current-covariance]], [[F25-real-rotation-exact-discrete-time-maxwell]], [[F68-minimal-coupling-forces-even-photon]], [[F69-paired-spinor-photon]], [[F91-pairing-classification-theorem]], [[F168-paired-photon-binding-gauge-protected]], [[F169-photon-interacting-two-body-wavefunction]], [[F250-allk-gauge-pole-paired-photon]], [[F30-photon-dispersion-order-anisotropy-birefringence]] (in-repo prior art for the $O(k^2)$ chiral term); `docs/audits/physics-notes-complete-review.md` §2 (page-map stopped at p.175) and §3.3; notebook pp.141–160, 176–182.

---

## Goal

Notebook pp.176–182 were the last unrepresented pages in the tree. They state two theorems: **T1** every null 4-vector *is* a spinor outer product; **T2** every non-null vector is two null vectors with a free direction $\hat a$. The structural claim is that a boson is a multi-spinor object *by algebraic identity, not by binding*. This finding builds T1/T2 against the model's own constituents and reports what they earn.

**Not the audit §3.3 object** (notebook pp.161–175; cf. F25, whose curl-residual reading is superseded by S18). The audit's longitudinal-only result concerns the *dynamics* of one spinor, $\sigma^\mu\partial_\mu$ acting on a single null $V$. T2 is the *algebraic* decomposition of a non-null $V$. Different objects; this finding never touches the former.

## Source resolution (before any physics)

**Uniqueness of the timelike decomposition — resolved from the scan (`physics_notes_0708.pdf`, pp.155–156).** The notebook's classification table says "only 1 for timelike", but the same pages state "$(t,0)$ can break down into $(t/2,\hat u\,t/2)+(t/2,-\hat u\,t/2)$ for any unit vector $\hat u$", and p.141–160 records the light-cone intersection as an ellipse (a 2-surface). The table's "1" is the *canonical* choice $\hat a=\hat V$. Free $\hat a\in S^2$ is right (Jacobian singular values $0.921,\,0.584$ at a fixed $V,\hat a$, rank 2).

**The notebook's boxed closed form is wrong.** $a_0=\tfrac1{2V_0}(V_0^2-|\vec V|^2+2\hat a\!\cdot\!\vec V)$ mixes $[V^2]$ with $[V]$ and does not give a null pair (measured null defect $3.83$ at the record's seed). The notebook's *own* preceding line, $a_0(V_0-\hat a\!\cdot\!\vec V)=\tfrac12(V_0^2-|\vec V|^2)$, gives the correct

$$a_0=\frac{V\!\cdot\!V}{2\,(V_0-\hat a\!\cdot\!\vec V)},\qquad a_\mu=a_0(1,\hat a),\quad b_\mu=V_\mu-a_\mu,$$

✓ **Exact** (null residual $2.7\times10^{-15}$, $a_0,b_0>0$ for every $\hat a$). At $\hat a=+\hat V$ it reproduces the p.145 canonical split $\tfrac12(V_0+|\vec V|)(1,\hat V)+\tfrac12(V_0-|\vec V|)(1,-\hat V)$ exactly.

## Results

**R1 — T1 exact.** $\sigma\!\cdot\!V=\psi\psi^\dagger$ with $\psi=(\alpha,\beta)$; the only freedom is $\psi\to e^{i\theta}\psi$ (residual $5.8\times10^{-15}$). ✓ Exact.

**R2 — Leg space is $U(2)/U(1)^2=S^2$.** For $M=\sigma\!\cdot\!V=\Psi\Psi^\dagger$ with $\Psi=(\xi,\eta)$, $U=M^{-1/2}\Psi$ is unitary (residual $1.5\times10^{-14}$; closed-form $\sqrt M=(M+\sqrt{\det M})/\sqrt{\operatorname{tr}M+2\sqrt{\det M}}$, no eigensolver). So the free direction $\hat a$ *is* the coset $U(2)/U(1)_\xi\times U(1)_\eta$, and the spinor-pair's 8 real parameters $=4$ (the vector $V$) $+\,4$ ($U(2)$ = $\hat a$: 2 $+$ leg phases: 2). ✓ Exact.

**R3 — Covariance gate (1e) passes.** Under $S\in SL(2,\mathbb C)$, $M\to SMS^\dagger$, the decomposition of $\Lambda V$ along $\Lambda a$'s direction returns $\Lambda a,\Lambda b$ exactly (residual $5.2\times10^{-14}$, gated at $10^{-12}$). The $U(2)$ leg freedom acts on the *right* of $\Psi$, Lorentz on the *left*; they commute, so $\hat a$ is a genuine covariant label, not frame-dependent structure. Consistent with F24.

**R4 — Null limit (question 1a).** The photon $V=(\Omega_\text{even},c\vec k)$ is null: T1 applies, T2 does not. As $V\!\cdot\!V\to0$ the $S^2$ of decompositions collapses: leg-energy range $[(V_0-|\vec V|)/2,(V_0+|\vec V|)/2]$ tends to $[0,|\vec V|]$, leaving only $a=0$, $b=0$ and the collinear family $a=xV$, $b=(1-x)V$ — a one-parameter momentum-fraction, **no $\hat a$**. This is the sense in which the massless boson has one leg and no free direction. ✓ Exact.

**R5 — Question 1b: T1 against the lattice constituents.** With $V=(\Omega_\text{even}(k),c\vec k)$ the two constituents at $k/2$ have Minkowski defects $m_\pm^2=\omega_\pm^2-c^2q^2$ that scale as $|k|^{3.03}$ with **opposite signs** (ratio $\to-1$), and cancel in the pair: $V\!\cdot\!V=\Omega_\text{even}^2-c^2k^2\to-\kappa|k|^{4.00}$ ($\kappa(111)=0.00412$; direction-dependent — $\kappa(110)\approx0.0023$, $\approx0$ on a coordinate axis — and gated only along $(111)$). So the lattice pair is *not* exactly null; it is spacelike at $O(k^4)$, the cubic terms having cancelled between the branches. Consequently T1 is **exact for the continuum photon and violated at $O(k^4)$ on the lattice** — a lattice artefact of the same $O_h$ family as F69's dispersion, not a defect of the identity. ~ Numerical (exponents $3.03,\,4.00$).

**R6 — Question 1c: the F169 $O(k^2)$ offset, derived.** Expanding the audited BCC dispersion,

$$\omega^\pm(\vec q)=c|\vec q|\pm\varepsilon(\vec q)+O(q^3),\qquad \varepsilon(\vec q)=-\frac{q_xq_yq_z}{3|\vec q|},\quad \omega^-(\vec q)=\omega^+(-\vec q).$$

$\varepsilon$ is homogeneous of degree 2, odd, and vanishes on the coordinate planes. In the continuum ($\varepsilon=0$) the two-body threshold at fixed $\vec k$ is *exactly* the T1 null condition: $T(\vec k)=c|\vec k|$, reached only on the collinear valley $q_1=x\vec k,\;q_2=(1-x)\vec k$, **flat in $x$**. The lattice term lifts it linearly:

$$E_0(x)=c|\vec k|+\varepsilon(\vec k)\,(2x-1)+O(k^3),$$

so $\Omega_\text{even}$ ($x=\tfrac12$) is the zero of the lift and the true minimum sits at the endpoint $x\in\{0,1\}$:

$$\boxed{\Omega_\text{even}(\vec k)-T(\vec k)=|\varepsilon(\vec k)|+O(k^3)=\frac{|k_xk_yk_z|}{3|\vec k|}+O(k^3)}$$

Measured ratio to $|\varepsilon|$: $1.054,\,1.026,\,1.013$ at $|k|\to|k|/2,/4,/8$ (→ 1, error linear in $|k|$); on coordinate planes ($\varepsilon=0$) the offset drops to exponent $3.00$; $\Omega_\text{even}-T$ matches $\Omega_\text{even}-\min_b\omega^b(\vec k)$ to $\sim10^{-8}$ (that residual is `arccos` rounding near 1, $\sqrt{2\cdot10^{-16}}$, not physics). Convergence to ratio 1 is slow near coordinate planes (e.g. $(0.707,0.707,0.007)$: $2.02\to1.15$ over the same halvings). F169's own stochastic `true_threshold` is under-converged at small $k$ and gives ratios $1.043,\,0.986,\,0.876$ at these three $k$, so its quoted exponent $2.10$ is contaminated by search noise; the pattern search used here was cross-checked against 2M random BZ points and Nelder–Mead from the zero-energy BZ nodes (nothing below $T$). So F169's fit exponent $2.10$ is the $O(k^2)$ law with $O(k^3)$ corrections and direction dependence, and the **coefficient is an exact closed form** $\tfrac13|\hat k_x\hat k_y\hat k_z|\,|k|^2$. ✓ Exact form / ~ numerical confirmation.

Two honest statements about what produced it. (i) The coefficient is nearly a corollary of $\omega^\pm=c|q|\pm\varepsilon$ (in-repo: [F30](F30-photon-dispersion-order-anisotropy-birefringence.md) already has the $-\sqrt3k^2/54$ chiral term along $(111)$, zero on axes, consistent with this $\varepsilon$); what is new is the general-direction closed form and its identification with the two-body floor. The coefficient comes from the lattice dispersion; factorization contributes only the *interpretation* (the flat collinear valley is the $V$-null degeneracy of T2, and the lifted minimum is its degenerate endpoint). (ii) A caution for F169 (not a contradiction, flagged for that finding's owner): the threshold $T(\vec k)$ is the endpoint where one constituent carries all of $\vec k$ and the other has zero momentum ($\omega(0)=0$), i.e. $T\simeq\min_b\omega^b(\vec k)$. The F169 threshold state is then a spin-½-like configuration at its lower end, and the spin-1 identification lives at $x=\tfrac12$, *above* $T$ by $|\varepsilon|$.

**R7 — Question 1d: $g_c$ is NOT reached.** T1 is an identity between a *field* $V_\mu$ and a spinor bilinear; it is silent about the *spectrum*. It carries no coupling, so it neither predicts nor removes $g_c$: whether a normalizable pole sits at $T(\vec k)$ is dynamics (F169). The photon's zero binding is "forced by identity" only if the photon is *defined* as the bilinear operator — a definition, not a statement about the Fock-space state. Under that reading the route is **redundant with F168**, which already gives the structural reason. $g_c=2.2596$ stays the one external input.

**R8 — Question 2: $\hat a$ and the W/Z sector.**

- **2a.** Asymmetry stands: photon (null) one leg, no $\hat a$; massive vector (timelike) two legs plus $\hat a\in S^2$ ✓.
- **2b — F91 W±: closes negative.** Chirality carries **no** data in T2: the right-handed leg is fixed by the left one, $\tilde\psi=\sigma_y\psi^*$, $\tilde\psi\tilde\psi^\dagger=\bar\sigma\!\cdot\!a$ (residual $<10^{-13}$). "Right-branch weight $\equiv0$" is a leg *label* the algebra does not see. And a degenerate two-null decomposition ($b=0$) requires $V$ null; for any timelike $V$ both legs have $a_0,b_0\ge(V_0-|\vec V|)/2>0$. A massive W therefore cannot correspond to an absent leg. **No correspondence** between F91's chiral assignment and a degenerate decomposition.
- **2c — Z axial split: no correspondence.** The $\hat a$-dependence of the leg energy is the full spread $\Delta a_0=|\vec V|$ (measured $1.000000000$ at $m=0.01,0.1,0.3,1$): mass-independent and $O(k)$. F91's $\sim k^3$ axial split is a *propagation* splitting of the pair's energy, whereas $a_0(\hat a)$ is an internal, unobservable label of a decomposition of a *fixed* $V$. The two are not comparable quantities, so this is **not an exclusion** (a review attack correctly flagged that reading as a category error) — only the absence of any matching mass suppression, and no mechanism by which $\hat a$ would enter a propagator.
- **Untested structural analogy, not a result:** $S^2=SU(2)/U(1)$ has the same shape as the weak-isospin orientation coset. Nothing here derives the identification; it is recorded so it is not re-discovered as new.

**R9 — Degree-of-freedom arithmetic (2d), explicit.**

| | $V$ | real params of $V$ | spinor params | internal (free) |
|---|---|---|---|---|
| null | $4-1$ | 3 | $\psi$: 4 | 4 − 3 = **1** (phase) |
| timelike | 4 | 4 | $(\xi,\eta)$: 8 | 8 − 4 = **4** = $U(2)$ = $\hat a$ (2) + leg phases (2) |

Null: $3=3$ ✓ (spinor 4 − phase 1). Polarizations: the rest-frame content of $(\tfrac12,\tfrac12)$ is $1\oplus0$ under rotations; the triplet gives the 3 massive states, and for a null $V$ the $m=0$ (longitudinal) triplet member is removed, leaving 2 — the standard count, and the Srednicki/Varlamov "bispinor" remark that the composite-photon literature cites as its motivation (the conflation is upstream: that remark is this identity, not a dynamical binding).

**What the four $U(2)$ parameters are.** This is the standard massive spinor-helicity structure (Arkani-Hamed–Huang–Huang): a massive $p=\lambda^I\tilde\lambda_I$ carries an $SU(2)$ **little-group index $I$**, and $\hat a$ is the spin-quantization axis of the legs in the rest frame ($V_\mu=(m,0)\to$ two null legs $(m/2)(1,\pm\hat a)$, spin up/down along $\hat a$). The three $SU(2)$ generators are the massive particle's little-group rotations, *not* unmatched internal redundancy — an earlier draft called them "unrewarded structure" and was wrong to. The remaining $U(1)$ is the overall phase (R10). The route does not *derive* 2 vs 3; it re-expresses the standard count.

**R10 — The $U(1)$ claim: closes negative.** ✓ The free phase $e^{i\theta}$ of T1 *is* local: $\psi\to e^{i\theta(x)}\psi$ leaves $V$ invariant exactly ($0$) and shifts the induced connection $a_\mu=\operatorname{Im}\psi^\dagger\partial_\mu\psi$ by $\partial_\mu\theta$ (residual $2.3\times10^{-11}$). But: (i) it is the **Hopf/Berry redundancy** of parametrizing $V$; it acts trivially on $V$; (ii) the connection is a *composite* whose field strength is the pull-back area form $f_{\mu\nu}=\tfrac12\hat n\!\cdot\!(\partial_\mu\hat n\times\partial_\nu\hat n)$ (measured $-0.161451056$ vs $-0.161451057$), **degree 0 in the amplitude of $V$** (Maxwell $F$ is degree 1) and quadratic in gradients — not Maxwell; (iii) *(dropped as evidence after review: a random 4-vector added to a null one trivially breaks nullness, and the null momentum-like $V$ is not the potential $A_\mu$, whose shift need not preserve nullness)*. The phase does not reproduce F68's minimal coupling or F250's gauge pole. The $U(1)$ leg is **closed negative**; the rest of the route survives independently.

**R11 — the $O(k^4)$ pair defect $\kappa$, DERIVED (2026-09-22; closes this finding's own deferred item).** R5 measured the paired photon's Minkowski defect as $V\!\cdot\!V=-\kappa(\hat k)\,|k|^4$ with $\kappa(111)=0.00412$ and $\kappa\approx0$ on a coordinate axis, and left $\kappa$ underived. It is exact, and it is **not new physics**:

$$\boxed{\ \kappa(\hat k)=\frac{1-\sum_i\hat k_i^4}{216}+\frac{(\hat k_x\hat k_y\hat k_z)^2}{36}\;=\;2c_\text{lat}^2\,\bigl|C(\hat k)\bigr|,\qquad c_\text{lat}^2=\tfrac13\ }$$

where $C(\hat k)=-\bigl[(1-\sum_i\hat n_i^4)/144+(\hat n_x\hat n_y\hat n_z)^2/24\bigr]$ is the **already-established exact rational coefficient of the model's dimension-6 photon Lorentz-violation operator** ([CL274](../docs/claims/CL274-no-dimension-5-photon-operator.md), F246/F30). The relation is the trivial one: if $\Omega_\text{even}=c_\text{lat}|k|\bigl(1+C(\hat k)|k|^2\bigr)+O(k^5)$ then $V\!\cdot\!V=\Omega_\text{even}^2-c_\text{lat}^2|k|^2=2c_\text{lat}^2C|k|^4+O(k^6)$.

Verified at 60-digit precision with Richardson extrapolation in $t^2$ over **16 directions** (10 named + 6 random integer triples): worst absolute difference $2.2\times10^{-16}$ against $\kappa$-values of order $10^{-3}$. Range $\kappa\in[0,\,1/243]$, maximal along $\langle111\rangle$ ($\kappa=1/243$), exactly zero along $\langle100\rangle$ — matching CL274's stated $C$-range $[-1/162,0]$ under the factor $2c_\text{lat}^2=2/3$. The direct dispersion check $\Omega_\text{even}/(c_\text{lat}|k|)-1=C(\hat k)|k|^2$ reproduces $C$ to $10^{-6}$ relative at $|k|=0.02$.

**Interpretation — the sentence that matters.** "The paired photon's lattice 4-momentum is not exactly null" and "the model's leading photon Lorentz violation is a dimension-6 operator with coefficient $C$" are the **same statement in two variables**. The $O(k^4)$ defect is not a newly discovered flaw in the photon construction; it is the quantity the GRB/LHAASO gate (F107, CL274) was already built around, re-expressed as $V\!\cdot\!V$. Nothing downstream moves.

## Verdict

| Question | Result |
|---|---|
| Source: is $\hat a$ free? | **Yes**, $S^2$ (table's "1" is canonical); boxed closed form defective |
| 1a/1b T1 vs lattice constituents | exact continuum; $O(k^4)$ lattice violation, exponents 3.03/4.00 |
| 1c F169 offset | **derived**: $\tfrac13|\hat k_x\hat k_y\hat k_z|k^2$, flat collinear valley lifted linearly |
| 1d $g_c$ | **not reached** — redundant with F168 |
| 1e covariance | passes ($5.2\times10^{-14}$) |
| 2b W± ↔ degenerate leg | **negative** |
| 2c Z axial ~ $k^3$ | **no correspondence** (incomparable quantities; not an exclusion) |
| 2d DOF | closes for null; timelike: 4 parameters = little-group $SU(2)$ + phase (standard massive spinor-helicity) |
| $U(1)$ from the phase | **negative** (local, but composite/Hopf; connection quadratic in gradients, not Maxwell) |

**Outcome reached: (b) redundant with F168/F169 for binding, with a partial (a) — the F169 offset coefficient.** The page-map gap is closed: pp.176–182 now have a finding, a claim card, and a corrected T2 formula.

## Verification summary

Module `casim.engine.gauge.factorization`; record `F397-factorization-route` (gate, quantitative — algebraic legs at $10^{-12}$, lattice legs looser); declared control `formula=notebook` reddens exactly `t2_pair_null_and_sums`. No scipy, no eigensolver on any chiral matrix.

| Leg | Type | Measured |
|---|---|---|
| T2 null pair / sum | exact | $2.7\times10^{-15}$ |
| notebook boxed formula defective | documented | $3.83$ |
| canonical split = $\hat a=\hat V$ | exact | $<10^{-13}$ |
| T1 outer product | exact | $5.8\times10^{-15}$ |
| $U(2)$ unitarity of leg space | exact | $1.5\times10^{-14}$ |
| $\hat a$ Jacobian rank 2 | exact | $0.921,\,0.584$ |
| $SL(2,\mathbb C)$ covariance | machine | $5.2\times10^{-14}$ |
| chirality is not extra data | exact | $<10^{-13}$ |
| timelike legs non-degenerate / spread $=|\vec V|$ | exact | $1.000000000$ |
| leg / pair defect exponents | quantitative | $3.03$ / $4.00$ |
| $\varepsilon$ closed form; offset $=|\varepsilon|$; valley linear; plane exponent | quantitative | $1.054\to1.013$; $3.00$ |
| local $U(1)$ legs (2) | machine | $2.3\times10^{-11}$ |

## What is not shown

$g_c$ is not derived. The leg-space $SU(2)$ is *not* identified with weak isospin. The F169 threshold's spin content at the endpoint $x=0$ is flagged, not analysed. ~~The coefficient $\kappa$ of the $O(k^4)$ pair defect is measured, not derived.~~ **Derived 2026-09-22 — see R11.** Lattice branch conventions ($\hat n^+\to C\hat q$ with $C=\operatorname{diag}(1,-1,1)$, $\hat n^-\to\hat q$) were not needed for the results above and were left untouched.

## Prior art

The two theorems are standard: null vector $=$ spinor bilinear and timelike vector $=$ sum of two null vectors are the Penrose–Rindler spin-frame relations; massive spinor-helicity (Arkani-Hamed–Huang–Huang 2017, arXiv:1709.04891) is exactly T2 with the $SU(2)$ little-group index; the composite $U(1)$ connection of a spinor phase is the $\mathbb{CP}^1$ Berry/Hopf connection. The novelty here is confined to the correction of the notebook's boxed formula, the test against the model's lattice constituents, and the general-direction closed form for the F169 offset (partly in F30).

## Reviewed & corrected

**2026-09-21 - 15:00** — attack pass: **CONFIRMED-NARROWER**. Found: no error in T1, T2 or $\varepsilon$ (re-derived in sympy); overstated: 2c read as an exclusion (category error), R9's "unrewarded structure" (it is the massive little group), several vacuous or loose legs, quoted numbers not reproducing at the record's seed, F25 cited without its S18 note, F30 prior art uncited. Fixed: legs tightened (covariance $10^{-12}$; offset ratio $\le1.5\%$; valley leg now resolves $\varepsilon$), tautological legs removed from the gate (DOF arithmetic, degree-0, gradient-shift), numbers re-quoted from the record, record class lowered to quantitative and its `findings:` reduced to F397 (the record does not run F169 code), prose narrowed as above, prior art added. Rejected: none. Deferred: ~~derive $\kappa$ of the $O(k^4)$ pair defect and its direction dependence~~ (**done 2026-09-22, R11 — it is $2c_\text{lat}^2|C|$, the CL274 dimension-6 coefficient**); ~~a converged re-run of F169's `true_threshold`~~ (**done 2026-09-22 — F169 C3 corrected; the threshold has a closed form and no search is needed**).
