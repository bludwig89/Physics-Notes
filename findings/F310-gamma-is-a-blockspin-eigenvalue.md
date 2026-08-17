# F310 — The model needs **no 3D dual**: the $t=0$ state of a rigid 3D automaton **is** a 3D Euclidean measure, so F296's operator is present by construction — and running F285's own Poisson bridge through it gives $n_s=3-2y$ and therefore $\gamma\equiv y-1$ **identically**, so the tilt's anomalous dimension **is the anomalous part of the model's own block-spin eigenvalue**. Every exponent F130 measured is an **integer**, which is why no earlier route could produce one; and the identity reading predicts $n_t=2$ **exactly**, $r\sim10^{-118}$, repairing the exclusion that killed the naive dual

**Date:** 2026-08-11 - 18:40
**Numbering:** **F310**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `lucid-patient-zeldovich`, sector `interactions`.
**Status:** Confirmed — **16/16 PASS**, two declared controls each verified RED and journalled. C1, C2, C2b, C3, C4, C6 ($n_t$) and C7 are **exact** (sympy over ℚ, or literal integer/zero); C5, C6 (the suppression) and C8 are **computed**. C8 asserts that it is *not* a derivation.
**Module:** `casim.engine.interactions.cosmology_critical_measure` (`src/casim/engine/interactions/cosmology_critical_measure.py`)
**Script:** `tests/findings/test_F310_critical_measure.py` (registry entry `check_critical_measure`, tier **gate**)
**Results:** `test-results/F310_critical_measure.json`
**Executes:** `docs/status/open-derivations.md` row **G2**, whose *suggested attack* reads verbatim: *"the in-repo step is smaller and is the one to take first — decide whether the model claims a 3D dual at all, given that the naive field-content map already failed. A negative here is worth as much as a mechanism."*
**Answers:** [[F295-tilt-is-an-anomalous-dimension-not-a-second-scale]] §7's last row (*"which operator carries $\gamma$"*) **from inside the model**, where [[F296-holographic-cosmology-names-the-operator-and-validates-T1]] could only answer it from outside.
**Corrects:** [[F285-initial-condition-measure-cannot-tilt]] D1 row 2 — one sub-case, exactly, and **in F285's favour**.
**Cross-references:** [[F285-initial-condition-measure-cannot-tilt]] (S1's Poisson bridge $P_\rho\propto k^{n_s}$, reused unchanged; D1's measure table, one row corrected; D3's marginality, re-read), [[F284-rigid-lattice-expansion-and-primordial-state]] (the **rigid** 3D substrate that makes the $t=0$ state a 3D measure rather than a slice of something else), [[F130-blockspin-rg-gauge-gravity]] (the measured Kadanoff spectrum C3 audits, and C1's eigenvalue), [[F106-psi-K-sourcing-derivation]] (the model's own Poisson law), [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (no inflaton — untouched), [[F296-holographic-cosmology-names-the-operator-and-validates-T1]] (L4's operator, now internal; L5's $r$ exclusion, now shown not to transfer), [[F286-second-scale-must-be-a-log-not-a-length]] (T1 and T5's look-elsewhere discipline), [[F300-lattice-native-thermodynamics]] / [[F309-gstar-from-model-content]] (the 96-fermionic-modes-per-site count C8 quotes), [[F253-weight-as-phase-scale-nogo]] / [[F256-lambda6-sextic-derivative-nogo]] (the coincidence standard). External: Balkenhol et al. 2025 ($n_s=0.9682\pm0.0032$ CMB-only, $0.9728\pm0.0029$ +DESI DR2, $r<0.034$); Planck 2018 X; BICEP/Keck BK18.

Raised by Ben, 2026-08-11: *"attack open-derivations problem G2, the anomalous dimension."*

---

## 1. The question, and why the answer is "no, and it doesn't need one"

G2 asked whether the model claims a 3D dual, because F296 had found the model's structure a published home — **holographic cosmology**, which computes $n_s-1$ from a 3D QFT with no inflaton — and had then watched the obvious realisation of it fail: reading the model's own 48 Weyl fermions and 2 scalars as the dual's field content gives $r=0.32$–$0.97$ against BK18's $r<0.034$, over by $9.5$–$28.5\times$.

**The answer is no, and the reason dissolves the failure rather than working around it.**

Holographic cosmology reaches for a 3D QFT *by duality* — a bulk/boundary dictionary, with a radial direction traded for an energy scale. This model does not need one. Its $t=0$ state, on a **rigid** 3D lattice (F284), *is* a probability measure on 3D field configurations — which is to say, literally a **3D Euclidean statistical field theory**. And F285's own bridge makes the primordial spectrum literally that measure's energy–energy correlator:

$$\nabla^2\ln K=-\frac{8\pi G}{c^4}T^{00}\ \Longrightarrow\ P_\Phi=\frac{P_\rho}{k^4}\ \Longrightarrow\ \boxed{P_\rho(k)\propto k^{\,n_s}}$$

So the object HC obtains by a dictionary is present here **by construction**. There is nothing to map, and therefore nothing to map wrongly.

**This is what repairs F296 L5.** HC's $r$ formula counts the *dual's* fields, and it is an artifact of the dictionary — it is how a 4D tensor mode is read off a 3D correlator through the domain-wall/cosmology correspondence. With no dictionary there is no such formula, so the $9.5$–$28.5\times$ exclusion does not transfer. §6 computes $r$ from the identity reading instead, and gets a very different answer.

---

## 2. C1 — the load-bearing identity: $\gamma$ **is** an RG eigenvalue

$\rho=T^{00}$ is the energy density. In a 3D statistical field theory that is the **energy operator** $\varepsilon$ — the singlet bilinear — and at a critical point it carries the scaling dimension

$$\Delta_\varepsilon=d-\frac1\nu,\qquad P_\varepsilon(k)\propto k^{\,2\Delta_\varepsilon-d}.$$

In $d=3$, with $y\equiv1/\nu$ the thermal RG eigenvalue:

$$n_s=2\Delta_\varepsilon-3=3-\frac2\nu=3-2y\qquad\Longrightarrow\qquad \boxed{\gamma\equiv\frac{1-n_s}{2}=y-1\ \ \textbf{identically}.}$$

No approximation, no limit, no fit — sympy returns $\gamma(y)-(y-1)=0$. **The anomalous dimension the tilt needs is the anomalous part of the model's own block-spin relevant eigenvalue**, $\lambda=b^{1+\gamma}$ instead of $b^1$. That is the operator identification G2 asked for, and it is *in-model* where F296's was external.

Two limits fall out, both exact, and both already on the register under other names:

| $\nu$ | fixed point | $n_s$ | where the register already has it |
|---|---|---:|---|
| $1$ | spherical / large-$N$ | $\mathbf{1}$ exactly | F285 D1 row 4, "the one principled scale-free choice" |
| $\tfrac12$ | Gaussian / mean field | $\mathbf{-1}$ exactly | §3, and **not** where F285 put it |

The Poisson bridge is re-derived rather than assumed: $\Delta^2_\Phi\propto k^{3+(2\Delta_\varepsilon-3)-4}=k^{n_s-1}$, symbolically identical to F285's own relation.

---

## 3. C2 — a correction to F285 D1 row 2, exact, and it makes F285 *stronger*

F285's measure table row 2 reads:

> *"Any local functional of short-range-correlated fields — thermal, gapped, **or even a critical Gaussian field squared** — gives $k^0$."*

The parenthetical is wrong, and F285's own text says why without noticing: its derivation carries the hypothesis *"for a Gaussian field with any **integrable** $P_\phi$"*, and the critical case $P_\phi=1/q^2$ is **not** integrable in $d=3$ ($\int d^3q/q^2$ diverges linearly). Done properly, with the angular integral in closed form and the radial one rescaled by $q=kx$:

$$P_\rho(k)=\int d^3q\,P_\phi(q)P_\phi(|\mathbf k-\mathbf q|)=\frac{2\pi}{k}\int_0^\infty\frac{dx}{x}\ln\left\lvert\frac{1+x}{1-x}\right\rvert=\frac{2\pi}{k}\cdot\frac{\pi^2}{2}=\boxed{\frac{\pi^3}{k}}$$

so $n_s=-1$ **exactly**, not $0$. The bracket is exact in two halves: $\int_0^1=2\sum_{j\ge0}(2j+1)^{-2}=\pi^2/4$, and $x\to1/x$ maps $[1,\infty)$ onto $(0,1]$ with the integrand invariant. No quadrature is used anywhere in this leg, so it carries no tolerance.

**Three things follow, and the third is the reason this is in the finding at all.**

1. **F285's conclusion is strengthened, not weakened.** $-1$ is *further* from the observed $0.965$ than $0$ is. The correction costs F285 nothing.
2. **The gapped sub-case is untouched** (C2b): an exponentially-decaying correlator has an analytic transform at $k=0$, so it does give $k^0$. This corrects one parenthetical, not the row.
3. **It is the first sign that criticality is where the exponent lives.** F285's row 2 was the argument that closed the critical route — *"the critical route collapses into the generic one"* — and it does not. A critical measure does **not** collapse to white noise; it produces a different, computable exponent. That is exactly the door C1 walks through.

---

## 4. C3/C4 — why every earlier route failed, in one sentence

An anomalous dimension is, by definition, a **non-integer** RG exponent. F130 measured this lattice's Kadanoff spectrum, and every exponent in it is an **integer**:

| operator | eigenvalue | class | exactness |
|---|---:|---|---|
| $c_\text{lat}$ (continuum light speed) | $b^{0}$ | marginal | exact |
| $\sigma$ (confinement — the **one** relevant direction) | $b^{+1}$ | relevant | exact |
| LIV operators, $n\ge2$ | $b^{-n}$ | irrelevant | exact |
| gravity discretisation error | $b^{-2}$ | irrelevant | machine |
| deconfining $\lambda$ | $b^{-2}$ | irrelevant | quantitative |

**Five entries, five integers, and F130 says why without meaning to.** Its own text records that $\lambda_n=b^{-n}$ is *"a round-off-floor identity, independent of fit"* — an algebraic identity of the **linear block average**. A linear block average on free fields is a Gaussian calculation, and Gaussian calculations cannot generate anomalous dimensions. So the model's *measured* RG spectrum contains none, and the measurement was taken at an order that could not have produced one.

Run F130's own relevant eigenvalue $y=1$ through C1 (**C4**):

$$n_s=3-2(1)=1\qquad\text{exactly.}$$

**The model's own measured RG predicts Harrison–Zel'dovich** — and the data excludes it at $8.36\sigma$ (Planck 2018), $\mathbf{9.94\sigma}$ (CMB-only 2025) and $\mathbf{9.38\sigma}$ (+DESI DR2). That re-derives F285's headline from the *RG* side rather than the *measure* side, which is worth having because the two sides were previously unconnected — and it localises the whole of G2 to a single number.

> **G2 is now: the model needs exactly one non-integer eigenvalue, of size $\sim1.6\%$, and F130's machinery is where it would be found.**

$\nu=1$ is the **spherical-model / $N\to\infty$** fixed point, the unique standard universality class with $\nu=1$. So the statement "the model's block-spin, run at Gaussian order, gives Harrison–Zel'dovich" and the statement "the model's block-spin sits at the large-$N$ fixed point" are the same statement.

---

## 5. C5 — what the data asks for

| dataset | $n_s$ | $\gamma=(1-n_s)/2$ | $y=1+\gamma$ | $\nu=1/y$ |
|---|---|---:|---:|---:|
| Planck 2018 (F295's own literal) | $0.9649\pm0.0042$ | $0.017550\pm0.0021$ | $1.017550$ | $0.982753$ |
| CMB-only 2025 | $0.9682\pm0.0032$ | $0.015900\pm0.0016$ | $1.015900$ | $0.984349$ |
| +DESI DR2 | $0.9728\pm0.0029$ | $0.013600\pm0.00145$ | $1.013600$ | $0.986582$ |

Three comparator datasets are carried as a **table**, not one literal — the 2026-08-08 changelog entry recorded exactly what a single stale `NS_OBS = 0.9649` costs, and this module is not going to repeat it.

---

## 6. C6 — the prediction, and it is the one zero-parameter number here

In **any** conformal field theory the stress tensor's dimension is **protected by its own conservation**: $\partial_\mu T^{\mu\nu}=0\Rightarrow\Delta_T=d$ exactly. The energy operator's dimension is not protected. **That asymmetry is the whole content of this section.**

$$\text{scalars: }\Delta_\varepsilon=3-\tfrac1\nu\ \text{(anomalous)}\ \Rightarrow\ n_s\approx0.97,\qquad \text{tensors: }\Delta_T=3\ \text{(protected)}\ \Rightarrow\ \boxed{n_t=2\ \text{exactly}}$$

A strongly **blue** tensor spectrum. At the CMB pivot, $58.26$ decades below the BZ edge (F285 D2's number, reused):

$$\log_{10}r(k_*)\simeq-118.6\ /\ -118.4\ /\ -118.1\quad\text{across the three datasets.}$$

**Zero parameters, from a theorem.** Compare F296 L5, where the naive dual gave $r=0.323$ (conformal) / $0.970$ (minimal) against BK18's $r<0.034$ — excluded by $9.5$–$28.5\times$. The identity reading does not merely survive the test that killed the dual reading; it predicts the model can **never** produce an observable primordial tensor mode, which is what BK18, BICEP Array and everything after them will keep seeing.

**C7** is a consistency check rather than a new result: a critical point has exact power laws, so $dn_s/d\ln k\equiv0$ — F295 A1, re-derived from the critical-measure structure instead of from the constancy of $\gamma$. The two routes agreeing is the point.

---

## 7. C8 — the $1/N$ target, which is **not** a derivation and is asserted not to be

$\nu=1$ is the $N\to\infty$ fixed point, so a **finite** field content tilts it downward: $\nu<1$, hence $n_s<1$.

> **The sign of the observed tilt is forced by finiteness alone.** That is the one thing in this section the model gets for free, and it is not nothing — F285's whole difficulty was that the model had no reason to prefer red over blue.

The magnitude is a different matter. With the leading large-$N$ result $\nu=1-32/(3\pi^2N)$ for $O(N)$ in $d=3$:

| dataset | $N$ required |
|---|---:|
| Planck 2018 | $62.7$ |
| CMB-only 2025 | $69.1$ |
| +DESI DR2 | $80.6$ |

against the counts the model actually owns:

| candidate | $N$ | $n_s$ | vs Planck 2018 | vs CMB-only | vs +DESI |
|---|---:|---:|---:|---:|---:|
| 48 Weyl fields | 48 | $0.95393$ | $-2.61\sigma$ | $-4.46\sigma$ | $-6.51\sigma$ |
| 96 fermionic modes/site (F300 G10-13) | 96 | $0.97723$ | $+2.94\sigma$ | $+2.82\sigma$ | $+1.53\sigma$ |
| $96+12$ gauge $+2\ E_g$ | 110 | $0.98016$ | $+3.63\sigma$ | $+3.74\sigma$ | $+2.54\sigma$ |
| 192 real Grassmann components | 192 | $0.98868$ | $+5.66\sigma$ | $+6.40\sigma$ | $+5.48\sigma$ |

**No candidate lands in the band.** The check asserts this: `C8-no-hit` goes **red** if any model count ever falls inside $1\sigma$, so that a coincidence has to be read by a human before it can be claimed. F286 T5's look-elsewhere count applies to the value unchanged, and a shape argument does not improve a value's statistics — the standing lesson of F253/F256 and of F295 §4, which said the same thing about $\tfrac29$ and was right to.

**One free discriminator, worth recording because it costs nothing.** As the data improved, F295's $\tfrac29$ moved **away** ($-0.06\to-2.82\sigma$) while $N=96$ moved **toward** ($+2.94\to+1.53\sigma$). Two candidate mechanisms with opposite drifts under the same data. The next dataset separates them, and neither party has to do anything.

---

## 8. Verdict

> **Does the model claim a 3D dual? No — and it needs none.** The $t=0$ state of a rigid 3D automaton *is* a 3D Euclidean measure, so the object holographic cosmology reaches for by duality is present here by construction, and F296 L5's $r$ exclusion — an artifact of the dictionary — does not transfer. Running F285's own Poisson bridge through that measure gives $n_s=3-2y$ and hence $\gamma\equiv y-1$ **identically**, so the tilt's anomalous dimension **is** the anomalous part of the model's own block-spin relevant eigenvalue. That is why every earlier route failed: an anomalous dimension is a non-integer RG exponent, F130's measured spectrum is entirely integers, and F130 records the reason itself — its eigenvalues are algebraic identities of a *linear* block average, which is a Gaussian calculation. Feeding F130's $y=1$ back through gives $n_s=1$ exactly, so **the model's own RG predicts Harrison–Zel'dovich and the data excludes it at $9.4$–$9.9\sigma$**. Along the way F285's D1 row 2 is corrected exactly and in its own favour ($\pi^3/k$, $n_s=-1$, not $k^0$). The identity reading then makes the one zero-parameter prediction available here: the stress tensor's dimension is protected by conservation while the energy operator's is not, so $n_t=2$ **exactly** and $r\sim10^{-118}$ — the model can never produce an observable tensor mode.

**What this does to G2.** It was *"a number attached to a kind of object the model cannot name, with an external candidate and a quantified obstruction."* It is now *"one non-integer eigenvalue, of size $1.6\%$, in a spectrum the repo already measures with machinery the repo already owns."* That is the same question asked of a different file.

---

## 9. Falsifiers

1. **A block-spin computation with fluctuation corrections that still returns exactly $\lambda_\sigma=b^1$.** Kills the whole route: $\gamma$ would have nowhere in the model to live, and F295 falsifier 5 (a pure initial condition with no scaling dimension) would be the surviving reading. **This is the single highest-value next calculation and it is in-repo.**
2. **A detection of $r>10^{-10}$.** Kills the identity reading outright — it predicts $10^{-118}$, and there is no parameter to move.
3. **A measured $dn_s/d\ln k$ significantly nonzero.** A critical point has exact power laws, so this kills the critical-measure reading and favours F286's log class. The two separate at $\sigma\sim2.6\times10^{-4}$.
4. **A demonstration that the $t=0$ measure cannot be critical.** Returns the problem to F285 D1 and $n_s=0$. This is the finding's largest residual and it is not proved here.
5. **A model field count landing inside $1\sigma$ of the required $N$.** Would *not* confirm C8 — it would trip `C8-no-hit` and force a human read, which is the point of asserting it.
6. **A non-integer eigenvalue found elsewhere in the model's RG of the wrong size.** Would give $\gamma$ a home and the wrong value at once.

---

## 10. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $n_s=3-2y$ from $\Delta_\varepsilon=d-1/\nu$ and the F285 Poisson bridge | **exact-algebraic** (sympy) |
| $\gamma\equiv y-1$ — the operator identification | **exact-algebraic** (literal zero residual) |
| $\nu=1\Rightarrow n_s=1$; $\nu=\tfrac12\Rightarrow n_s=-1$ | **exact** (integers) |
| Critical Gaussian squared $=\pi^3/k$, $n_s=-1$ (corrects F285 D1 row 2) | **exact** (no quadrature; bracket $=\pi^2/2$ in two closed halves) |
| Gapped sub-case gives $k^0$ (F285 correct there) | **exact** |
| Every F130 eigenvalue exponent is an integer | **exact** (4 of 5 exact in F130 itself; the fifth quantitative and consistent) |
| $y=1\Rightarrow n_s=1$, excluded at $8.36/9.94/9.38\sigma$ | **exact** (prediction) $+$ **computed** (the $\sigma$'s) |
| $\Delta_T=d$ protected $\Rightarrow n_t=2$ | **exact** (CFT theorem, not derived here) |
| $\log_{10}r(k_*)\approx-118$ | **computed** (on F285 D2's decade count) |
| $dn_s/d\ln k\equiv0$ | **exact**; reproduces F295 A1 |
| Required $y=1.0136$–$1.0176$ | **computed** |
| $N$ required $\approx63$–$81$; no model count lands there | **computed**; **explicitly not a derivation** |
| **Whether the $t=0$ measure is critical** | **open — the finding's largest residual** |
| **The value of the one non-integer eigenvalue** | **open — but now an in-repo computation on F130's machinery** |

---

## 11. Honest scope

**The initial condition is still free.** F282, F284 and F285 are untouched — there is no inflaton, the substrate is rigid, and $P(k)$ is an automaton initial condition. Nothing here changes that, and it would be easy and wrong to read §2 as a derivation of the spectrum. What changes is the **shape** of the freedom: a free *function* $P(k)$ becomes a choice of **universality class** — a discrete label which then fixes $n_s$, $n_t$, $r$ and $dn_s/d\ln k$ with no further parameters. That is a large reduction and it is the honest claim.

**Criticality is inferred, not derived.** The argument is: the observed spectrum is a power law over four decades; a 3D measure has power-law correlations only at a critical point; therefore the $t=0$ measure is critical. The first step is an observation and the second is a theorem, but the conclusion is an inference about the initial state, and the model does not *require* it. §9 falsifier 4 is the honest form of this.

**$\Delta_T=d$ is a CFT theorem, cited not proved.** It follows from stress-tensor conservation and is standard; this finding does not reprove it, in the same posture F304 took toward Cooke–Keane–Moran before it closed that gap. Its consequence — $n_t=2$ — is the load-bearing half and is checked symbolically.

**C3's spectrum is F130's, transcribed.** This finding does not re-measure the Kadanoff eigenvalues; it audits the list F130 reported and asserts a property of it (integrality). If F130's list is incomplete, C3's conclusion is about the reported spectrum and not about the model — which is exactly why falsifier 1 is a *computation* and not a re-reading.

**C8 is a target and says so in its own assertions.** The temptation to present $N=96$ at $+1.53\sigma$ against +DESI as a hit is real, the drift is in the flattering direction, and the finding declines. F295 §4 made the same call about $\tfrac29$ at $0.064\sigma$ and the data subsequently moved it to $-2.82\sigma$; that is the standing argument for the discipline, and it is two weeks old.

---

## 12. Files
- Module: `src/casim/engine/interactions/cosmology_critical_measure.py`
- Test: `tests/findings/test_F310_critical_measure.py` (record `F310-critical-measure`, tier gate, 16/16, 1.1 s)
- Results: `test-results/F310_critical_measure.json`
- Controls: both verified **CONTROL** 2026-08-11 and journalled to `test-results/control-soundness.json`
