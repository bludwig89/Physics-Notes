---
id: CL267
title: The primordial tilt's anomalous dimension is the anomalous part of the model's own block-spin eigenvalue, and the same structure predicts n_t = 2 exactly and r ~ 1e-118
slug: tilt-is-a-blockspin-eigenvalue
tier: headline
kind: prediction
status: contingent
domain: [cosmology, QFT]
exactness: exact
findings: [F310, F285, F296, F130, F362]
tests: [F310-critical-measure, F362-blockspin-fluctuation-eigenvalue]
modules: [src/casim/engine/interactions/cosmology_critical_measure.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-11
last_verified: 2026-09-04
provenance: authored
review_state: authored
confidence: medium
---

# CL267 — The tilt is a block-spin eigenvalue, and the tensor spectrum is n_t = 2 exactly

## Statement

The $t=0$ state of the model's rigid 3D automaton is a probability measure on 3D field
configurations, i.e. a 3D Euclidean statistical field theory, so the primordial spectrum is that
measure's energy–energy correlator and **no holographic dual is required or claimed**. Under that
identification, with $\Delta_\varepsilon = d - 1/\nu$ and the model's own Poisson law
$\nabla^2\ln K = -(8\pi G/c^4)T^{00}$:

$$n_s = 3 - 2y,\qquad \gamma \equiv \tfrac12(1-n_s) = y-1\ \textbf{ identically},\qquad y \equiv 1/\nu,$$

so the primordial tilt's anomalous dimension **is** the anomalous part of the model's own block-spin
relevant eigenvalue, $\lambda = b^{1+\gamma}$. Two consequences are asserted:

1. **The model's measured RG predicts Harrison–Zel'dovich, and the data excludes it.** Every
   eigenvalue exponent F130 measured is an integer ($b^0$, $b^{+1}$, $b^{-n}$), and $y=1$ gives
   $n_s = 1$ exactly, excluded at $8.36\sigma$ (Planck 2018), $9.94\sigma$ (CMB-only 2025) and
   $9.38\sigma$ (+DESI DR2). The model therefore requires exactly **one** non-integer eigenvalue, of
   size $\gamma = 0.0136$–$0.0176$.
2. **The tensor spectrum is fixed with no free parameters.** In any CFT the stress tensor's dimension
   is protected by its own conservation, $\Delta_T = d$ exactly, while the energy operator's is not.
   Hence $n_t = 2$ **exactly** (strongly blue), and at the CMB pivot — $58.26$ decades below the
   Brillouin-zone edge — $\log_{10} r(k_*) \approx -118$.

## What it extends

**Established results this bears on.** (i) The Harrison–Zel'dovich spectrum $n_s = 1$ and its
observed $3.5\%$ violation — standard inflationary cosmology derives the tilt from slow-roll
parameters, $n_s - 1 = -6\epsilon + 2\eta$; this model has no inflaton (F282, exact no-go) and
derives the *form* $n_s = 3 - 2y$ from a 3D critical measure instead. (ii) The single-field
consistency relation $r = -8n_t$, which this **contradicts**: a protected stress-tensor dimension
gives $n_t = +2$ (blue) with $r$ unobservably small, where single-field inflation gives $n_t$ small
and negative with $r$ potentially detectable. (iii) The standard CFT theorem $\Delta_T = d$ for a
conserved stress tensor, which is cited rather than reproved and which supplies the whole of
consequence 2.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F310-gamma-is-a-blockspin-eigenvalue.md` C1 | $n_s = 3-2y$ and $\gamma \equiv y-1$; the Poisson bridge reproduces F285's own relation | exact (sympy, literal zero) |
| `findings/F310-gamma-is-a-blockspin-eigenvalue.md` C3/C4 | F130's five measured eigenvalue exponents are all integers; $y=1 \Rightarrow n_s=1$ exactly, excluded at $9.38$–$9.94\sigma$ on the two 2025 datasets | exact (prediction); computed ($\sigma$) |
| `findings/F310-gamma-is-a-blockspin-eigenvalue.md` C6 | $\Delta_T = d \Rightarrow n_t = 2$; $\log_{10} r(k_*) \approx -118$ | exact ($n_t$); computed (suppression) |
| `findings/F310-gamma-is-a-blockspin-eigenvalue.md` C2 | Corrects F285 D1 row 2: a critical Gaussian squared gives $\pi^3/k$, $n_s=-1$, not $k^0$ | exact (no quadrature) |
| `test-results/F310_critical_measure.json` | 16/16 PASS, record `F310-critical-measure`, tier gate, tol 0 | — |
| `test-results/control-soundness.json` | both declared controls verified **CONTROL** at the current fingerprint | — |

## Falsifier

**Three, each with a threshold.**

1. **$r > 10^{-10}$ detected.** The claim predicts $\sim10^{-118}$ and there is no parameter to move.
   BICEP Array targets $\sigma(r) \lesssim 0.003$; any detection at all kills consequence 2 and with
   it the identity reading. This is the sharpest falsifier the cosmology block carries.
2. **A block-spin computation, with fluctuation corrections included, that still returns exactly
   $\lambda_\sigma = b^1$.** Then $\gamma$ has nowhere in the model to live and consequence 1's
   requirement is unsatisfiable. This is in-repo, on F130's existing machinery, and is the highest-value
   next calculation.
3. **$dn_s/d\ln k$ measured significantly non-zero.** A critical point has exact power laws, so the
   claim requires $dn_s/d\ln k = 0$; the discriminator against F286's log class sits at
   $\sigma \sim 2.6\times10^{-4}$.

## Status & history

`status: contingent`, and the hypothesis it is contingent on is named: **that the $t=0$ measure is
critical.** F310 §11 states this as its largest residual — the argument is that the observed spectrum
is a power law over four decades and a 3D measure has power-law correlations only at a critical point,
which is an inference about the initial state rather than a derivation. The model does not require it.
Closing that hypothesis, or falsifier 2 returning a non-integer eigenvalue, would make this card
`live`.

**Falsifier 2 has been tested and did not fire (F362, 2026-09-04).** The fluctuation-corrected
block-spin computation this falsifier named was run on the repo's own exact strong-coupling PT
machinery and returns exactly $\lambda_\sigma=b^1$ -- structurally, not as a numerical near-miss:
every order of the expansion around $\lambda=0$ carries an integer eigenvalue (`docs/claims/CL300-blockspin-fluctuation-corrections-stay-integer.md`),
and the one composite quantity a finite-order expansion could define is scheme ($b$)-dependent, so it
could not supply a universal $\gamma$ even where it is formally evaluable. This closes the specific
mechanism falsifier 2 pointed at without resolving the card's contingency: the identification
$\gamma\equiv y-1$ is unaffected, and *whether* any mechanism (perturbative or not) supplies the
eigenvalue's value remains the open question. `status: contingent` stands; a non-perturbative
confinement-RG computation clearing CL300's own falsifier would still make this card `live`.

**What this card does not claim.** The primordial spectrum is still a **free initial condition** —
F282, F284 and F285 stand unchanged and CL-level statements about $A_s$ and $\Omega_\text{DM}$ are
untouched. What narrows is the *shape* of the freedom: a free function $P(k)$ becomes a choice of
universality class, one discrete label that then fixes $n_s$, $n_t$, $r$ and $dn_s/d\ln k$ with
nothing further. The $1/N$ reading of $\gamma$ (F310 C8) is a **target and not part of this claim**;
no field count the model owns lands in the required band $N \approx 63$–$81$, and F310's own test
goes red if one ever does.

**Relation to CL-level claims resting on F296.** F296 L5 excluded the naive holographic-dual reading
of this model on $r$ by $9.5$–$28.5\times$. That exclusion is **not contradicted**: it applies to the
dual reading, whose $r$ formula counts the dual's fields through the domain-wall/cosmology
dictionary. This card asserts there is no dictionary, so that formula does not apply and $r$ is
computed from the identity reading instead. F296's finding is unedited.

## Sources

- `findings/F310-gamma-is-a-blockspin-eigenvalue.md`
- `findings/F285-initial-condition-measure-cannot-tilt.md` (the Poisson bridge; D1 row 2, corrected)
- `findings/F296-holographic-cosmology-names-the-operator-and-validates-T1.md` (the operator, and the exclusion this re-homes)
- `findings/F130-blockspin-rg-gauge-gravity.md` (the measured Kadanoff spectrum)
- `findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` (falsifier 2, tested and did not fire) / `docs/claims/CL300-blockspin-fluctuation-corrections-stay-integer.md`
- `docs/status/open-derivations.md` row **G2**
- Balkenhol et al. 2025, *Inflation at the End of 2025* — $n_s = 0.9682\pm0.0032$ (CMB-only), $0.9728\pm0.0029$ (+DESI DR2), $r < 0.034$ (95 %)
- BICEP/Keck BK18; Planck 2018 X
