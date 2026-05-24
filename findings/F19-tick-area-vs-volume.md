# Finding 19 (stub) — Does the active-tick region scale as area or volume in the strong-gravity limit?

*Drafted 2026-05-21 - 19:45. Status: **test spec only — no run, no data**. This file is a falsifiable target, not a result.*

---

## Background

Phase T5.A (`ca-emergent-time-plan.md` lines 215–223) and Exactness Inventory Tier 1 #2 establish that **true-vacuum cells satisfy $N(\mathbf{x}) = 0$ exactly** — bit-for-bit on 80% of an $L = 256$ lattice in the F1 vacuum regression. The lattice already has a structural distinction between "ticking" cells (active) and "frozen" cells (vacuum).

't Hooft CAI §9.4 ([`reference-research/t-hooft-2015-cai-summary.md`](../reference-research/t-hooft-2015-cai-summary.md); PDF p. 94–95) claims a *generic* version of the same observation:

> *"In any finite, simply connected region of space, the information contained in the bulk gradually disappears, but what sits at the surface will continue to be accessible, so that the information at the surface can be used to characterise the info-equivalence classes."*

with the Bekenstein bound (CAI Eq. 9.7, $S = \pi R^2$) forcing an **area law** — total ticking degrees of freedom inside a region grow as $R^2$, not $R^3$, in the strong-gravity / horizon limit.

The §9.4 claim is **horizon-specific**. Our T5.A claim is **flat-space**. The shared shape — "active region is a sub-manifold of the lattice, not the whole lattice" — is suggestive but proves nothing: T5.B explicitly predicts a *volume* scaling $(L/\sigma_x)^d$ for the lazy run, which is the **opposite** of an area law for a flat-space wave packet.

The decisive question is what happens in the *strong-gravity* regime where the §9.4 claim is meant to apply.

---

## Hypothesis

Define $N_\text{active}(R)$ as the number of lattice cells inside a sphere of radius $R$ (centred on a gravitating source) for which $N(\mathbf{x}) > 0$ after a long run, at fixed global tick count $n$.

| Hypothesis | Scaling | Interpretation |
|---|---|---|
| **H_vol** | $N_\text{active}(R) \propto R^3$ all the way into the would-be horizon | T5.A vacuum freezing is a *propagator artifact* of the QCA on a flat metric; the §9.4 surface-vs-bulk pattern is **coincidence**. |
| **H_area** | $N_\text{active}(R) \propto R^2$ inside the strong-field band | The variable-$c$ machinery produces area-law information storage from local lattice rules alone; the §9.4 pattern is a **hint** that needs a finding entry of its own. |
| **H_mixed** | Crossover from $R^3$ at large $R$ to $R^2$ near the horizon, at a finite $R_c$ | A weaker hint; record the crossover scale and the exponent $\alpha$ in $R^{\alpha(R)}$ as the empirical content. |

The hypothesis to be tested is **H_area** against the null **H_vol**.

---

## Test spec

### Setup

- **Source.** A gravitating Gaussian mass profile $\rho(\mathbf{x}) = M\,\mathcal{G}_\sigma(\mathbf{x})$ centred at the lattice midpoint, sourcing $\phi(\mathbf{x})$ via the existing open-BC James–Hockney Poisson solver (`ca-simulation/poisson_open.py`).
- **Strength.** Tune $GM$ so that $|\phi|/c_0^2 \in [10^{-2}, 0.5]$ at the strongest core voxels. The upper end is **strong-field** by the Cayley variable-$c$ stepper's lights ($c(\mathbf{x}) = c_0/(1 - 2\phi/c_0^2)$ is finite for $\phi > -c_0^2/2$, divergent at $\phi = -c_0^2/2$). Run at least three field strengths; do **not** push past the formal horizon — the test is about the run-up to it, not the singularity itself.
- **Propagator.** `ca_curved.py` (Cayley variable-$c$ Strang composition), the only stepper in the project that supports a position-dependent $c$ with verified exact unitarity (Exactness Inventory Tier 2 #2, $5.5 \times 10^{-15}$ norm drift).
- **Excitation.** A Gaussian wavepacket of width $\sigma_\psi$ launched from radius $R_0 \gg \sigma$ inbound toward the source. The packet provides the "tick fuel" — cells only acquire $N > 0$ if a non-vacuum amplitude reaches them.
- **Lattice.** $L \in \{96, 128, 192\}$ at minimum. Open BC.
- **Runtime.** $n_\text{steps}$ chosen so the packet has had time to fall past the strong-field band and re-emerge (rough order: $2R_0/c_0$ in lattice units).
- **Tick counter.** Use the binary $N_\text{binary}(\mathbf{x})$ already implemented for T1.B (the same counter that yielded the Tier 1 #2 result). The phase-accumulation variant (Finding 11) is a secondary read.

### Observable

$$
N_\text{active}(R) \;\equiv\; \#\,\{\mathbf{x} : \|\mathbf{x} - \mathbf{x}_0\| \le R \;\text{and}\; N_\text{binary}(\mathbf{x}) > 0\}
$$

Reported on a radius grid $R \in [\sigma, R_0]$ in steps of $\Delta R = 2$ cells. Fit $\log N_\text{active} = \alpha \log R + \beta$ in two bands:

- **Outer band** $R \in [r_\text{flat}, R_0]$ where $|\phi|/c_0^2 < 10^{-3}$ — sanity-check that $\alpha \to 3$ (volume) in the flat-space limit.
- **Inner band** $R \in [\sigma, r_\text{strong}]$ where $|\phi|/c_0^2 > 0.1$ — the diagnostic band. $\alpha$ here is the test statistic.

Report $\alpha_\text{outer}$ and $\alpha_\text{inner}$, with bootstrap 95% CI from the radius bins.

### Sanity checks

1. **Flat-space null.** Set $GM = 0$ (no gravity). Verify $\alpha_\text{inner} \approx 3$ at all $R$ — this confirms the test instrument reads volume scaling when volume scaling is the truth.
2. **Recover T5.A on the run.** Verify $N(\mathbf{x}) = 0$ exactly outside the packet's causal cone, as in the F1 regression. Anything else is an instrumentation error.
3. **No spurious area-law from radial binning.** A spherical shell of constant thickness has surface $\propto R^2$ regardless of what's inside it. Use *cumulative* $N_\text{active}(R)$ (volume-aggregated), not *shell* $\Delta N_\text{active}/\Delta R$, as the primary statistic, and report both.
4. **Norm drift.** Confirm Cayley stepper norm drift stays at $\le 10^{-14}$ over the run; abort otherwise.

---

## Decision rules

After running across the field-strength grid:

| Outcome | $\alpha_\text{inner}$ (95% CI) | Verdict | Action |
|---|---|---|---|
| **VOL** | $\alpha_\text{inner} \in [2.8, 3.2]$ at all field strengths | Volume scaling persists into the strong-field band. §9.4 ↔ T5.A is **coincidence**. | Close this finding as a null result. No further work. |
| **AREA** | $\alpha_\text{inner} \in [1.8, 2.2]$ at the strongest field, and monotonically dropping from $\sim 3$ at the weakest | Area scaling emerges in the strong-field limit. **Hint confirmed.** | Promote to a full Finding 18; open a follow-up to derive $\alpha$ analytically from the Cayley stepper structure; document under Exactness Inventory Tier 1 or 3 depending on residual size. |
| **MIXED** | $\alpha_\text{inner}$ between the two bands, or non-monotone in field strength | Partial hint. Log crossover $R_c$ where $\alpha$ first drops below 2.5. | Record the crossover and the field strength at which it appears. Do not promote; flag as inconclusive pending deeper-field runs. |
| **NULL_FAIL** | Sanity check 1 ($GM=0$) does **not** yield $\alpha \approx 3$ | Test instrument is broken. | Debug the radius binning and the binary counter before any other conclusion. |

The **VOL** branch is the prior — area scaling would be a genuinely new lattice phenomenon not predicted by anything in the v2 stack.

---

## What this test cannot decide

- It does not test the **information content** of surface cells, only the **count** of ticking cells. The §9.4 claim is sharper — it says the *labels* of info-equivalence classes live on the surface. The count-of-active-cells test is a necessary, not sufficient, condition for the §9.4 picture.
- It does not probe **horizon dynamics** — the Cayley stepper is regular and unitary throughout, with no information-loss mechanism. If §9.4 requires information loss at the horizon (CAI §9.3), this test cannot see it.
- It does not extend to **rotating** or **charged** sources — only the static, spherically symmetric Newtonian potential.

---

## Open questions to resolve before running

1. **What is "$N > 0$" in floating-point?** The F1 vacuum regression got bit-for-bit zero because of an exact propagator-fixed-point structure. In a *gravitating* run with the Cayley stepper, vacuum cells may pick up $O(\varepsilon)$ amplitude from the variable-$c$ rotation. The threshold for "active" needs a pilot: $\|\psi(\mathbf{x})\|^2 > \varepsilon_\text{cut}$ for what $\varepsilon_\text{cut}$? Suggested pilot at $\varepsilon_\text{cut} \in \{10^{-15}, 10^{-12}, 10^{-9}\}$ to verify $\alpha$ is independent of the cut.
2. **Field-strength ceiling.** How close to $\phi = -c_0^2/2$ can the Cayley stepper run before norm drift exceeds $10^{-14}$? Sets the deepest accessible point in the inner band.
3. **Packet width vs. lattice spacing.** $\sigma_\psi$ must be $\ge 4$ cells for the dispersion to behave; $\sigma_\psi \ll r_\text{strong}$ for the radial bins to resolve the inner band. Pick before run.

---

## Cross-references

- Source claim 1: [`ca-emergent-time-plan.md`](../ca-emergent-time-plan.md) Phase T5.A (lines 215–223), T5.B (225–233), T5.C (235–245).
- Source claim 2: [`reference-research/Cellular-Automaton-Interpretation-of-Quantum-Mechanics.pdf`](../reference-research/Cellular-Automaton-Interpretation-of-Quantum-Mechanics.pdf) §9.4, p. 94–95, Eq. 9.7.
- Antecedent: [`reference-research/t-hooft-2015-cai-summary.md`](../reference-research/t-hooft-2015-cai-summary.md) §6 item 5 (the "is this a coincidence or a hint" prompt).
- Empirical anchor: [`exactness-inventory.md`](../exactness-inventory.md) Tier 1 #2 (vacuum freezing $N = 0$ on 80% of $L=256$).
- Instrument: `ca-simulation/ca_curved.py` (Cayley variable-$c$); `ca-simulation/poisson_open.py` (James–Hockney Poisson); tick-counter from T1.B.
- Tracking: [`lattice-vs-spacetime-tests.md`](../lattice-vs-spacetime-tests.md) — add a row labelled "F18 area-vs-volume" once a run is scheduled.

---

*End of stub. Promote to a full finding only after a passing-or-failing run with the decision-rule branches above resolved.*
