# F127 — Deriving $\alpha_\text{em}$ from the lattice rule: a four-avenue no-go

*2026-06-10. **Recovered 2026-07-31** at the roadmap C8.2 close-out: the audit found F127 was a numbering gap with a live test and no finding file. The write-up already existed in the test's docstring and its artifact; this file records it where the index can see it. **`tests/findings/test_F127_alpha_em_derivation.py` remains the primary record** — nothing here is new physics, and every verdict is quoted from that test and `test-results/F127_alpha_em_derivation.json`.*

## Summary

$\alpha \approx 1/137.036$ is the model's **last irreducible dimensionless input**. Everything adjacent to it is already derived:

| Coupling | Source |
|---|---|
| $g'/g$ | $\sigma\leftrightarrow\tau$ swap geometry (F45: $\sin^2\theta_W = 1/4$) |
| $g_s$ | rotor stiffness (F115-CM3: $g_s^2\chi = 1/4$) |
| EW family | one-parameter (F115-CM1: $e = g/2$, etc.) |

This finding tries four routes to $\alpha$ and reports each as a sharp result. **All four are negatives**, which is the finding: it locates *why* the derivation fails rather than leaving it as an open wish.

| Avenue | Verdict | Reason |
|---|---|---|
| **A** — Sakharov-style induced coupling | **sharp negative** | The U(1) **Ward identity $\Pi(0) = 0$** blocks the mechanism. The conformal anomaly is what enables the same route for $G$ ($T^\mu_{\ \mu} = 0 \Rightarrow$ zero tree stiffness); electromagnetism has no analogue. $I_1^{BZ} = 0.446$ would give $\alpha_\text{hyp} = 0.84$, a factor 115 from measurement |
| **B** — an $O(1)$ lattice scale near the EW matching point | **sharp negative** | $\mu_\star/E_\text{lat} = 2\times10^{-15}$ with $E_\text{lat} = 1.85\times10^{18}$ GeV; there is no $O(1)$ lattice scale near 3.7 TeV |
| **C** — topology fixes the coupling | **sharp negative** | Topology fixes the charge **spectrum** $\{0,\tfrac13,\tfrac23,1\}$, not the **magnitude** $\lvert e\rvert$ |
| **D** — structural normalisation | **inconclusive** | $Z=1$, $c = 1/\sqrt3$ and the curl normalisation are all structural, but the Peierls coupling $q$ is independent of them. No constraint found |
| **E** — numerical observation | **observation, not derivation** | $1/\alpha(\Lambda) = 64 = z_{NN}^2$ under one-loop running gives $1/\alpha(0) \approx 138.6$, **1.14%** from 137.036. Suggestive; not derived from the rule |
| **F** — diagnosis | — | identifies the missing structural element |

**Conclusion, as the artifact states it:** all four derivation avenues produce sharp negatives, and the structural obstruction is the U(1) Ward identity — $\Pi(0) = 0$ prevents the Sakharov mechanism that works for $G$. The $1/\alpha(\Lambda) = 64$ coincidence is recorded as an observation precisely so it is not mistaken for a result.

## Why this file exists

C8.2's finding-number audit reported F127 as a **gap** — no finding file — while `tests/findings/test_F127_alpha_em_derivation.py` was live and producing a committed artifact. A no-go of this weight (it names the project's last free dimensionless input and explains the obstruction) being invisible to `findings-index.md` is exactly the kind of hole the audit was built to surface.

**Status:** live, and a standing negative result. Artifact `test-results/F127_alpha_em_derivation.json`; registry record `F127-alpha-em-derivation`. Related: [[F115-coupling-magnitudes]] (the derived couplings), [[F45-sigma-tau-weinberg]] ($\sin^2\theta_W$), and the F151/F152 IR-coupling line for the strong-sector analogue of the same question.
