---
id: CL280
title: The model's leptonic running of alpha reproduces PDG Delta alpha(M_Z) to 0.0495%, and its lattice contribution is bounded below that residual
slug: running-alpha-leptonic-lattice-bounded-and-two-loop
tier: supporting
kind: derivation
status: contingent
domain: [QFT, SM]
exactness: quantitative
findings: [F322, F251, F277, F261, F138]
tests: [F322-b9-running-rederived]
modules: [casim.engine.interactions.running_alpha_lattice_bound, casim.engine.interactions.qed_vacuum_polarization, casim.engine.interactions.qed_twoloop_ae]
constants: [sin2_thetaW_uv]
supersessions: [S12-F277-refold-removed-qed-and-gluon]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-17
last_verified: 2026-08-17
provenance: authored
review_state: authored
confidence: medium
---

# CL280 — The leptonic running of $\alpha$ to $M_Z$, with its lattice contribution bounded

## Statement

The model's one-loop leptonic vacuum polarization, driven by its own exact $b_0^\text{QED}=4/3$,
gives $\Delta\alpha_\ell(M_Z)=0.03142093$; adding the two-loop leading log fixed by its own
sympy-exact $b_1=1$ (F261) gives $\Delta\alpha_\ell(M_Z)=0.03148241$, against PDG leptonic
$0.031498$ — a residual of $0.0495\%$, or $1.559\times10^{-5}$ in $\Delta\alpha$. The
**lattice** contribution to this quantity is bounded at $6.77\times10^{-6}$ at $n=28$
($0.088$ of the residual) and falls with grid refinement, because the subtracted transverse
coefficient $\Delta=B_\text{rule}-B_\text{cont}$ is $q$-flat and a $q$-independent constant in
$\Pi$ cancels identically in $\Pi(0)-\Pi(s)$. The conversion between the two is exact and
model-internal: $\delta(\Delta\alpha)=4\pi\alpha\,\delta B$.

Separately, on the electroweak side, one-loop Higgs-free running from the F138 matching
condition $\sin^2\theta_W(\mu_\star)=\tfrac14$ at $\mu_\star=4\pi v=3094.09$ GeV gives
$\sin^2\bar\theta_W(M_Z)=0.2317341$, $+0.222\%$ against PDG $\overline{\text{MS}}$ $0.23122$ —
but only when PDG $\alpha_\text{em}(M_Z)^{-1}=127.951$ is supplied as an input. On the model's
own leptonic-only $\alpha(M_Z)$ the residual is $+0.450\%$, a factor $2.02$.

## What it extends

Standard-Model QED: the universal one- and two-loop running of the electromagnetic coupling
($b_0=4/3$, $b_1=1$ per unit-charge Dirac fermion) and the leptonic contribution to
$\Delta\alpha(M_Z)$; and the electroweak mixing angle's one-loop RG evolution. The extension is
that both come out of a cellular-automaton lattice rather than a continuum field theory, and
that the lattice's *own* modification of the running is here bounded rather than assumed absent.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F322-b9-running-alpha-ew-rederived-post-f277.md` | all six legs; the bound, the two-loop closure, the EW $\alpha$-sensitivity | quantitative |
| `findings/F251-qed-vacuum-polarization-running-alpha.md` | $b_0^\text{QED}=4/3$ and Ward transversality, sympy-exact | exact |
| `findings/F261-twoloop-qed-ae-amu.md` | $b_1=1$, sympy-exact | exact |
| `findings/F277-qed-gluon-refold-period.md` | the refold removal that makes $\Delta$ $q$-flat to $1.7\times10^{-5}$ | quantitative |
| `findings/F138-weinberg-gap-closure-4piv-matching.md` | the $\mu_\star=4\pi v$ matching and $+0.222\%$ | quantitative |
| `test-results/F322_b9_running_rederivation.json` | the artifact | — |

Record `F322-b9-running-rederived` (gate tier) carries two declared controls, both verified
`CONTROL` over disjoint red sets: restoring the F277 refold reddens the bound legs (B9-3, B9-4);
zeroing $b_1$ reddens the two-loop leg (B9-5).

## Falsifier

Three, with thresholds:

1. **The bound.** If the spread of $\Delta=B_\text{rule}-B_\text{cont}$ over
   $Q\in[0.1,0.3]$ stops falling with $n$ — ratio bound$(n_\text{max})/$bound$(n_\text{min})\ge0.7$
   at $n\in\{20,24,28\}$ — the non-flatness is a residual log rather than grid noise and the
   lattice contribution is no longer bounded below the residual. This is exactly what the
   `refold_control` perturbation demonstrates (ratio $0.965$).
2. **The two-loop closure.** If an improved PDG leptonic $\Delta\alpha(M_Z)$ moved by more than
   $\sim1.5\times10^{-5}$ *away* from $0.03148241$, the two-loop leading log would stop being an
   improvement over one loop and B9-5 would go red.
3. **The EW leg.** A measured $\sin^2\bar\theta_W(M_Z)$ differing from $0.2317341$ by more than
   $0.5\%$ falsifies the F138 matching at one loop, independently of the running of $\alpha$.

## Status & history

`contingent`, not `live`, and the contingency is named: the electroweak half's $+0.222\%$
depends on PDG $\alpha_\text{em}(M_Z)$ as an input, and on the model's own leptonic-only
$\alpha$ the residual doubles to $+0.450\%$. The missing $3.795$ in $\alpha^{-1}(\overline{\text{MS}})$
is the hadronic vacuum polarization, which this model defers to rubric row G3 (F151/F152) and
does not derive. So the claim is contingent on an external input whose size is now quantified,
which is a different and more honest state than `live`.

Two further limits are stated rather than absorbed: the two-loop **non-log** constant and three
loops are not derived (they are the residual $1.559\times10^{-5}$), and $\alpha$ itself is not
derived at all (F127's four-avenue no-go). This card does not assert either.

Issued 2026-08-17, on the re-derivation that closed `completeness-2026-08-07` gap #5(a) — the
$0.24\%$ carried un-re-derived for three consecutive reports. F322 establishes that the number
never depended on the refolded path (disjoint call closure, measured bitwise), so F277 did not
change it; what F277 supplied was its **warrant**, since with the refold present the lattice
uncertainty on $\Delta\alpha$ was $183$–$190\times$ the agreement being claimed.

## Sources

- `findings/F322-b9-running-alpha-ew-rederived-post-f277.md`
- `findings/F251-qed-vacuum-polarization-running-alpha.md`
- `findings/F261-twoloop-qed-ae-amu.md`
- `findings/F277-qed-gluon-refold-period.md`
- `findings/F138-weinberg-gap-closure-4piv-matching.md`
- `docs/status/completeness-2026-08-07.md` row B9 and gap #5(a)
- `docs/theory/supersessions.yaml` S12
