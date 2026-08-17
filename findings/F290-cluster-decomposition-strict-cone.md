# F290 — Cluster decomposition on the lattice: no-signalling is **exact**, the causal cone is **strict** where a generic Lieb–Robinson system has only an exponential tail, and the correlation length **is** the gap ($\xi\propto\Delta^{-0.93}$ measured)

**Date:** 2026-08-05 - 18:25
**Numbering:** **F290**, taken as `NEXT FREE NUMBER` (a backlog number — spending it **closes** a gap). Session `tender-gifted-pascal-2`, sector `interactions`.
**Status:** Confirmed — **10/10 PASS**, three declared controls each verified red **and red only where expected**. C1 and C2 are machine-precision ($\le7.8\times10^{-16}$); C3 is quantitative and the exponent is quoted **as measured**, not as the continuum value.
**Verdict:** Completeness row **A10** leaves `ABSENT`. The genuinely CA-specific result is C2c: an automaton's light cone is *strictly* zero outside, where a generic quantum spin system has an exponentially small but non-zero tail.
**Modules:** `src/casim/engine/interactions/qi_cluster.py`
**Test / results:** record `F290-cluster-decomposition` (tier gate, entry `check_cluster`), driver `tests/findings/test_F290_cluster.py` → `test-results/F290_cluster_decomposition.json`
**Cross-references:** [[F227-decoherence-unitarity-floor]] (the correlator cone $C(r,t)=0$ for $r>4t$ — reconciled with this finding's tighter cone numerically in §2.3), [[F226-bell-tsirelson-indistinguishable]] (the entangled states used in §1), [[F212-dynamical-entanglement-generation]] / [[F217-field-native-fermion-entanglement]] (the register and the fermion machinery), [[F281-measurement-pointer-basis-born-rule-rg-classicality]] / [[F289-spin-statistics-connection]] (the neighbouring A8/A9 work). External: Lieb & Robinson, *Commun. Math. Phys.* **28** (1972) 251.

---

## The question

Cluster decomposition — that distant experiments are independent — is the property most obviously at risk in a model where everything is **one global rule on one lattice**. A deterministic substrate that reproduces quantum mechanics owes an account of it, and the completeness report records that the tree had none: *"Zero hits. No-signalling appears once (F227) and only as a QC aside."*

---

## 1. C1 — no-signalling, exactly

For every state in $\{$product, Bell/GHZ, generic entangled$\}$ and every one of twelve local unitaries on $A$ (a different rotor on each $A$ cell, so $U_A$ is not a product of identical factors):

$$\max\big\lVert\rho_B'-\rho_B\big\rVert\ =\ 7.77\times10^{-16}.$$

Nothing done on $A$ is visible at $B$ — including when $A$ and $B$ are maximally entangled, which is the case that matters. This is not an assumption bolted on to protect relativity; it follows from the state living on a tensor product and the operation being local.

**Control.** A **non**-local unitary — the model's own entangler applied *across* the cut — moves $\rho_B$ by $0.461$. Without this row, C1 would also pass for a broken partial trace or for a state with no $B$-dependence at all.

---

## 2. C2 — the causal cone is strict, and this is the CA-specific part

### 2.1 The statement

Perturb site 0 with a local unitary, evolve both the perturbed and unperturbed states under brick-wall layers of the model's native exchange gate, and read the reduced state at every site $r$:

| Region | $\max\lVert\rho_r'-\rho_r\rVert$ |
|---|---:|
| **outside** the cone | $6.87\times10^{-16}$ |
| inside the cone (control) | $1.068$ |

### 2.2 Why this is stronger than Lieb–Robinson

A generic quantum spin system obeys a Lieb–Robinson bound with an **exponential tail**:

$$\big\lVert[A(t),B]\big\rVert\ \le\ C\,e^{-(r-vt)/\xi}$$

— small outside the cone, but never zero. A **quantum cellular automaton** has a *finite* light cone: outside it the difference is **exactly** zero, because the circuit simply does not contain a path. Evaluated at the same outside-cone points, the generic bound is

$$\max C\,e^{-(r-vt)/\xi}\ =\ 7.39,$$

against a measured $6.9\times10^{-16}$. **The difference between "exponentially small" and "zero" is what the automaton structure buys**, and it is the one result in this finding that a non-automaton model could not reproduce.

### 2.3 The cone is measured *tight*, and reconciled with F227

The first draft of this module claimed a cone radius of $2t$. That claim was **conservative**, and a conservative cone makes the check unfalsifiable — shrinking it by one cell still left every tested point genuinely outside, so the `cone_slack` control could not fire. Measuring instead:

| $t$ (brick-wall layers) | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| largest $r$ with non-zero $\Delta$ | 1 | 2 | 3 | 4 | 5 |

so the tight cone is $r\le t$: **exactly one site per brick-wall layer.** With that value the control fires, which is the whole reason to measure rather than bound.

**This does not contradict F227's $r>4t$.** F227's tick is a *full* brick-wall (both gate offsets, so 2 sites per tick) and its observable $C(r,t)=\langle Z_0Z_r\rangle-\langle Z_0\rangle\langle Z_r\rangle$ carries **two** Heisenberg-evolved operators, each with its own cone: $2\times2\times t=4t$. The two findings are the same physics in different tick conventions, and `cone_convention_check` verifies the factor numerically rather than asserting it in prose — because two findings quoting different light cones is exactly the kind of thing that should be resolved in code.

---

## 3. C3 — cluster decomposition, with $\xi$ tied to the model's own gap

In the gapped ground state of the staggered-mass (lattice Dirac) chain, connected correlations decay exponentially, and the decay length tracks the gap:

| $m$ | gap $\Delta$ | $\xi$ | exp. fit $R^2$ |
|---:|---:|---:|---:|
| 0.12 | 0.24 | 13.78 | 0.9966 |
| 0.20 | 0.40 | 8.48 | 0.9977 |
| 0.35 | 0.70 | 4.92 | 0.9986 |
| 0.60 | 1.20 | 2.95 | 0.9993 |
| 1.00 | 2.00 | 1.84 | 0.9997 |

$$\xi\ \propto\ \Delta^{-0.9268},\qquad R^2=0.9994\ \text{over an }8.3\times\text{ range in gap.}$$

**The exponent is quoted as measured, not as the continuum value, and that is deliberate.** The relativistic relation is $\xi=v/\Delta$, i.e. exponent $-1$; the measured $-0.93$ is $7\%$ short, and the residual is a lattice correction. Pushing to smaller mass does **not** drive it to $-1$ — it makes it *worse* ($-0.85$), because $\xi$ then exceeds what a finite chain resolves. Quoting $-1$ here, or claiming convergence that the data does not show, would be an overclaim of exactly the kind the 2026-08-04 review series kept finding. The defensible statement is: **the correlation length is set by the gap and scales inverse-linearly to within 7%; it is not a free parameter.**

Two further honesty rows. The staggered mass makes $\lvert C(r)\rvert$ alternate between two sublattice branches sharing a decay rate but not a prefactor, so the fit is restricted to one parity; the two branches are checked to give the same $\xi$ to $7.5\%$, which is what makes the restriction bookkeeping rather than curve-picking. And the fit window is scaled to the expected $\xi$ at each mass, so every point is fitted over the same number of correlation lengths — a fixed window would measure the window.

**Control: the gapless point.** At $m=0$ the decay is power-law, not exponential:

| fit | $R^2$ |
|---|---:|
| power law ($p=0.87$) | $0.9988$ |
| exponential | $0.8712$ |

so cluster decomposition holds only *algebraically* when the gap closes. A check that could not tell the gapped and gapless cases apart would prove nothing about either.

---

## 4. Controls

| Perturbation | Goes red at | Meaning |
|---|---|---|
| `--param locality=nonlocal` | C1 | no-signalling is about *locality*, not about partial traces |
| `--param cone_slack=-1` | C2 | pins the cone radius to $t$ rather than merely asserting some cone exists |
| `--param mass=0.0` | C3, C3b, C3d | no gap ⇒ no finite correlation length |

Each is asserted in the driver to go red **and only where expected**.

---

## What this closes and what remains

**Closes.** Row A10 leaves `ABSENT`. The model has exact no-signalling with a non-local control, a strict causal cone measured tight and reconciled with F227, and exponential clustering whose length is the gap rather than a fitted parameter.

**Remains, and is not hidden.**

1. **The clustering leg is 1-D and free-fermion.** The staggered chain is exactly solvable, which is why it gives a clean $\xi$; the statement has *not* been made for the interacting 3-D BCC theory, where cluster decomposition is the harder and more interesting claim.
2. **The $7\%$ exponent shortfall is unresolved**, and the finite-size study above shows this measurement cannot resolve it further. Either a larger chain or the exact lattice pole condition would settle whether the deviation is purely a lattice correction.
3. **Cluster decomposition for the $S$-matrix** — the field-theoretic form, that connected amplitudes factorise for distant clusters — is not addressed. What is shown here is the correlation-function and reduced-state form.
4. **No new empirical prediction.** C1 and C2 are structural; C3 reproduces standard gapped-phase behaviour. The CA-specific content is the *strictness* of the cone, which is a sharpening of a bound rather than a measurable departure.
