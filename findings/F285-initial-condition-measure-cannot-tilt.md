# F285 — All three initial-condition routes close: via Poisson the primordial index is just the density slope, $P_\rho\propto k^{n_s}$, and the generic measures give $n_s=0$ (white noise) or $n_s=4$ (conserved-causal) while the one principled scale-free choice gives **exactly 1**, which Planck excludes at **8.4σ** — the hard observation is not the scale invariance but the **3.5% departure** from it, and a tilt needs a second, slowly-evolving scale, which is precisely what F282 excluded

**Date:** 2026-08-02 - 16:30
**Status:** **Negative result on all three handed-on directions**, with the residual sharpened from "a free function" to **one number the model cannot source**. 7/7 checks PASS. The spectral relation $P_\rho\propto k^{n_s}$ and the block-spin marginality (D3) are **exact-algebraic** (sympy); the measure predictions are **structural**; the decade counts are **computed**.
**Module:** `src/casim/engine/interactions/cosmology_initial_conditions.py`
**Registry record:** `F285-initial-condition-measure` (`tests/registry/interactions.yaml`, kind `assertion`, tier `gate`)
**Results:** `test-results/F285_initial_condition_measure.json`
**Executes:** `docs/theory/primordial-sector.md` §7, the three directions [[F284-rigid-lattice-expansion-and-primordial-state]] handed on. All three are now closed; §7 is rewritten with the outcomes.
**Cross-references:** [[F282-no-slow-roll-inflaton-sub-planckian-cutoff]] (no inflaton — and its C3 operator-marginality contrasted with D3's *state* marginality here), [[F283-elastic-lattice-excluded-and-f282-invariance]] (rigidity, and the exact scale-invariance of the obstruction), [[F284-rigid-lattice-expansion-and-primordial-state]] (the parent: fixed mode set, $P(k)$ as initial condition), [[F106-psi-K-sourcing-derivation]] (the model's **own** Poisson law $\nabla^2\ln K=-8\pi G T^{00}$ — this is what supplies the $k^{-4}$), [[F130-blockspin-rg-gauge-gravity]] (the Kadanoff transformation D3 dilates), [[F238-geon-relic-abundance]] (the *mirror* constraint: $\sim2\times10^{6}$ **more** small-scale power at the PBH scale, where this needs $10^{-56}$ **less** at CMB scales), [[F107-canonical-a-adoption-L4-grb-gate]] (the $a$ that fixes the BZ edge), [[F193-ontic-vacuum-gravitates-as-zero]] (the empty-lattice state the max-entropy measure perturbs around). External: Planck 2018 ($n_s=0.9649\pm0.0042$, $A_s=2.1\times10^{-9}$, pivot $k_*=0.05\,\text{Mpc}^{-1}$); Harrison 1970, Zel'dovich 1972; Traschen 1984 (integral constraints on causally-generated perturbations); Zel'dovich 1965 / Peebles 1980 ($k^4$ tail); Durrer, Kunz & Melchiorri 2002 (causal-seed models vs acoustic peaks).

Raised by Ben, 2026-08-02: *"build out the three untested directions for an initial-condition state."*

---

## 1. The relation everything runs through

The model supplies its own Poisson law — F106's $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$ — so $\Phi(k)\propto\rho(k)/k^2$ and $P_\Phi=P_\rho/k^4$. With the standard dimensionless power $\Delta^2(k)=k^3P(k)/2\pi^2$ and $\Delta^2_\Phi\propto k^{n_s-1}$:

$$k^3\cdot\frac{P_\rho}{k^4}\propto k^{n_s-1}\qquad\Longrightarrow\qquad \boxed{\ P_\rho(k)\propto k^{\,n_s}.\ }$$

So the whole question — *"what is the primordial spectral index?"* — reduces to *"what is the large-scale slope of the initial energy-density power spectrum on the lattice?"* Observation wants $P_\rho\propto k^{0.9649}$, i.e. very nearly $k^1$. Everything below is an answer to that one question.

## 2. D1 — a natural measure on the $t=0$ state

| Candidate measure | $P_\rho$ slope | $n_s$ | vs Planck |
|---|---:|---:|---|
| **Uniform / maximum entropy** (each cell's state independent) | $k^0$ | **0** | 230σ |
| **Any local functional of short-range-correlated fields** — thermal, gapped, or even a critical Gaussian field squared | $k^0$ | **0** | 230σ |
| **Locally conserved** initial data (Traschen integral constraints kill the $k^0$ and $k^2$ terms) | $k^4$ | **4** | 723σ |
| **Scale-free in the metric** ($\Delta^2_\Phi=$ const — the simplest non-trivial condition on $\ln K$) | $k^1$ | **1** | **8.4σ** |

**The second row is the robust one.** It is tempting to reach for a *critical* measure, since criticality is the one equilibrium state with power-law correlations — and F130 has already mapped this lattice's Kadanoff flow. But the observable is the **energy density**, which is a *local quadratic* functional of the fields. For a Gaussian field with any integrable $P_\phi$, $\rho\sim\phi^2$ has $P_\rho(k)=2\!\int\!P_\phi(q)P_\phi(k-q)\,d^3q\to$ const as $k\to0$. **White noise, regardless of the field's own criticality.** So the critical route collapses into the generic one, and $n_s=0$ is not an artifact of choosing a dull measure — it is what *any* short-range-correlated initial state gives.

**The two generic measures bracket the observation without touching it** ($0<0.9649<4$), and the one principled scale-free choice overshoots. It is worth being fair to that last row: "the initial condition on the metric is scale-free" is a genuinely elegant, one-parameter, assumption-light choice, and it is exactly Harrison–Zel'dovich. It is also **excluded at 8.4σ**. Planck does not merely prefer a tilt; it rules out exact scale invariance.

### How non-generic the initial state has to be

Taking the CMB pivot $k_*=0.05\,\text{Mpc}^{-1}$ against the lattice BZ edge $k_\text{BZ}=\pi/a$ with $a=1.0664\times10^{-34}$ m:

$$\frac{k_*}{k_\text{BZ}}=5.50\times10^{-59}\qquad(\textbf{58.26 decades}).$$

So relative to white noise, the initial state must carry

$$\left(\frac{k_*}{k_\text{BZ}}\right)^{n_s}=10^{-56.2}$$

— **56 decades less** large-scale power than the generic measure — and simultaneously $10^{+176.8}$, **177 decades more** than the conserved-causal one. The required state is astronomically non-generic in both directions.

**This mirrors F238.** F238 found that $\Omega_\text{DM}$ needs $\sim2\times10^{6}$ **more** small-scale power at the PBH scale than the CMB amplitude implies. Here the CMB scale needs $10^{-56}$ **less** than white noise. The two constraints pull on opposite ends of the same free function, which is a much tighter statement about $P(k)$ than either alone.

## 3. D2 — the Brillouin-zone edge is closed, and permanently

The lattice's one intrinsic $k$-space feature sits 58.26 decades above the pivot. The leading lattice correction is $O((ka)^2)$, and at the pivot $ka=1.73\times10^{-58}$, so

$$(ka)^2=2.99\times10^{-116}\qquad(\textbf{115.5 decades below unity}).$$

Dead — as expected. What is *not* merely expected is the strengthening F284 supplies: because the lattice is **rigid**, $k/k_\text{BZ}$ for a comoving mode is **time-independent**, so the BZ edge was never nearer to observable scales at any epoch. On an expanding-lattice picture one could at least ask whether observable modes were once near the cutoff. Here one cannot. **Direction 2 is closed permanently, not just today.**

## 4. D3 — block-spin fixes the shape and cannot touch the tilt (exact)

Under a Kadanoff dilation $k\to k/b$ with the $d=3$ variance normalisation, a power law maps as

$$P(k)=A\,k^n\ \longmapsto\ b^{-(3+n)}A\,k^n,$$

verified symbolically for $n\in\{-2,-1,0,1,2,4\}$ and for general $n$ (the log-slope out equals the log-slope in, identically). **The same exponent for every $n$**, with the entire effect of the transformation absorbed into the amplitude.

So the fixed-point set of block-spin is a **one-parameter line** of power laws, and $n$ is an **exactly marginal label** along it. Direction 3 therefore delivers something real but small: it explains why $P(k)$ should be a *power law* at all — that shape is RG-stable and needs no tuning — and it is structurally incapable of selecting the exponent.

> **A contrast worth stating, because it is easy to conflate.** F282 C3 found that the *dynamical operator* spectrum has an $O(1)$ **gap** around marginality: there is nothing for a slow-roll field to *be*. D3 finds that the *initial-state spectral index* is **exactly marginal**: there is nothing to *fix the tilt*. Two different objects, two opposite marginality statements — and both cut the same way.

*(Method note: a Monte-Carlo version of D3 — generate Gaussian fields, block-average, refit the slope — was tried first and discarded. Block averaging is a top-hat **plus decimation**, so it carries a window bias and an aliasing sum that are artifacts of the estimator rather than of the RG, and at the few-percent level they swamped the effect; the residual drift did not converge monotonically in the fit band. Verifying a three-line identity with a noisy estimator that introduces two artifacts of its own is the wrong instrument, so D3 is symbolic.)*

## 5. The synthesis — the tilt is the hard part, not the scale invariance

Assemble the three:

1. The only **scale-free** initial condition is $n_s=1$ exactly. Planck excludes it at **8.4σ**.
2. Therefore the initial state must be **tilted** — by the small amount $|1-n_s|=0.0351$.
3. A tilt is a *departure from scale invariance*, so it requires a **second scale** — something that distinguishes one $k$ from another.
4. The rigid lattice has exactly **one** scale, $a$, whose imprint at the pivot is $3\times10^{-116}$.
5. Inflation supplies the second scale for free: $n_s-1=-6\epsilon+2\eta$ is small *because* it is a slow-roll ratio — the slow evolution of $H$ during inflation is itself the second scale.

> **So the observation that is hardest for this model is not $n_s\approx1$. It is $n_s\ne1$.** Near-scale-invariance is cheap — any scale-free initial condition gives it. The 3.5% tilt is what needs a slowly-evolving scale, and that is exactly the object F282 excluded. The model can be handed the primordial spectrum as an initial condition, but it cannot be handed a *principle* that picks 0.9649 rather than 1.

## 6. Verdict

> **All three handed-on directions close, and the residual is sharper than before.** Via the model's own Poisson law, $n_s$ *is* the initial density slope. Every short-range-correlated measure — uniform, thermal, gapped, or critical-squared — gives $n_s=0$; imposing local conservation gives $n_s=4$; the one principled scale-free choice gives exactly 1, excluded at 8.4σ. The Brillouin-zone edge is 58 decades away and, on a rigid lattice, permanently so. Block-spin makes the power-law *form* free but leaves the exponent exactly marginal. **What was "a free function" in F284 is now one number the model has no principle to source: the 3.5% tilt.**

This is a **negative result that improves the ledger.** F284 left $P(k)$ as an unconstrained free function, which is unfalsifiable and therefore cheap. F285 replaces it with a specific, quantified, falsifiable deficit — and identifies the exact feature (a slowly-evolving second scale) whose absence causes it.

## 7. Falsifiers

1. **A measure on lattice initial states that yields $P_\rho\propto k^{0.96}$.** The sharpest possible refutation. §2 argues every short-range-correlated measure gives $k^0$; a counterexample with genuine long-range correlations of that strength would overturn the finding.
2. **A second intrinsic lattice scale.** §5 step 4 asserts there is only one ($a$). A second — a condensate correlation length surviving to cosmological scales, say — would supply a tilt mechanism.
3. **A revision of $n_s$ toward 1.** Exact HZ is excluded at 8.4σ *by Planck*; if that moved to $\lesssim2σ$ the "scale-free in the metric" row becomes viable and the finding's headline dissolves.
4. **A non-Poisson relation between the initial density and $\Phi$.** §1 uses the model's own F106 law; a $k$-dependent transfer beyond $k^{-2}$ would shift every exponent in the table.
5. **A demonstration that $\rho$ is not a local quadratic functional of the lattice fields.** Would break §2's collapse of the critical route into the generic one.

## 8. What is exact vs computed vs open

| Piece | Status |
|---|---|
| $P_\rho\propto k^{n_s}$ from Poisson $+$ $\Delta^2=k^3P$ | **exact-algebraic** (F106's own law) |
| Block-spin: $A k^n\mapsto b^{-(3+n)}Ak^n$, exponent preserved for all $n$ | **exact** (sympy, general $n$) |
| Exponent is an exactly marginal label; fixed-point set is a line | **exact** |
| Uniform / short-range / critical-squared measures $\Rightarrow n_s=0$ | **structural** (convolution theorem, $k\to0$ limit) |
| Locally conserved $\Rightarrow n_s=4$ | **structural** (Traschen constraints, external) |
| Scale-free-in-metric $\Rightarrow n_s=1$; excluded at 8.36σ | **exact** $+$ **external** (Planck) |
| $k_*/k_\text{BZ}=5.50\times10^{-59}$, 58.26 decades | **computed** (F107 anchor) |
| $10^{-56.2}$ suppression vs white noise; $10^{+176.8}$ vs conserved-causal | **computed** |
| $(ka)^2=3.0\times10^{-116}$; permanent because rigid | **computed** $+$ **structural** (F284) |
| A principle that selects $n_s=0.9649$ | **open — and now known to require a second, slowly-evolving scale** |

## 9. Honest scope

D3 and §1 are exact and cheap; their value is in what they *remove* from the candidate list, not in difficulty. D1's central claim — that the energy density of any short-range-correlated state is white noise on large scales — rests on the convolution limit and is solid for Gaussian fields and local functionals; a strongly non-Gaussian initial state with engineered long-range correlations is not covered, and that is falsifier 1. The $k^4$ row is imported (Traschen) rather than re-derived on this lattice. The decade counts assume the pivot and the F107 $a$, both of which are firm. And the headline is a *reframing* as much as a computation: the arithmetic in §5 is trivial, but the observation that near-scale-invariance is the cheap part and the tilt is the expensive part is the thing that changes what should be worked on next — and it says the next attempt should look for a second scale, not a better measure.

## 10. Files
- Module: `src/casim/engine/interactions/cosmology_initial_conditions.py`
- Test: `tests/findings/test_F285_initial_condition_measure.py`
- Results: `test-results/F285_initial_condition_measure.json`
- Theory doc updated: `docs/theory/primordial-sector.md` §7
