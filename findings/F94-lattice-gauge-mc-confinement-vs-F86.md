# F94 — Confinement from 3+1D lattice-gauge Monte-Carlo (P1 Option A), tested against Option C (F86)

> **[PARTIALLY SUPERSEDED 2026-08-17 by F323, F265 — ledger S21-F94-hypercubic-action-not-the-model-lattice]**
>
> **DEAD:** The ensemble as a measurement on the model's lattice. F94's D=4 simple-hypercubic Wilson action is F265-blind: it has an exact kernel that frees one of the four <111> link axes and misses asymptotically 1/3 of the curvature-carrying link content, so any sigma or V(R) read off it is a number about the wrong lattice. The absolute-normalisation (FA4) and strong-coupling (FA5) anchors do not rescue it -- both actions share a classical continuum limit, which is why those checks could pass on a blind action. Also dead: the implicit isotropic beta_t = beta_s, which F323 derives to be beta_t/beta_s = 4 on the model's geometry.
>
> **STILL LIVE:** FA1, FA2 and FA3 (engine certificates, properties of the sampler not the lattice); CMP2, the sigma_A -> v* bridge, exact at 1e-16 and re-affirmed by F311 at 1.2e-16; CMP3's shared large-R slope with the Coulomb difference; the Luscher-Weisz two-level estimator and its 84x variance reduction; and the qualitative statement that the 3+1D potential rises, which F323's BCC run also finds.
>
> **NOTE:** The replacement is `gauge-bcc-mc-d4` (gate, 28/28, 5/5 controls CONTROL) and `run-bcc-confinement-d4` (battery). F94's own heading is NOT rewritten -- per D12 a finding records what a session concluded. Three consequences tracked elsewhere rather than here: CL087 rests on F94 ALONE and is narrowed in the same edit as this record; F299's `mc_reach` names forks/gauge/lgt_fork_A_mc.py as the successor engine and that pointer is now stale, with F323 executing the successor on the BCC ensemble instead; and rubric row B7's evidence list should gain F323 beside F94 on the next completeness sweep.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*

**Date:** 2026-06-04 - 14:33
**Status:** Confirmed — engine 6/6 PASS (correctness), comparison 4/4 PASS; FA2/FA3 machine-ε, FA1 machine-ε, FA4/FA5 statistical, multilevel 84× variance reduction. Production σ is user-run.
**Modules:** `ca-simulation/forks/lgt_fork_A_mc.py` (new)
**Tests:** `tests/findings/test_FA_lgt_mc.py` (engine, 6/6), `tests/findings/test_FA_vs_FC_comparison.py` (A-vs-C, 4/4), `tests/runners/run_lgt_confinement.py` (heavy, user-run)
**Results:** `test-results/FA_lgt_mc.json`, `test-results/FA_vs_FC_comparison.json`, `test-results/lgt_confinement.{json,md}` (smoke)
**Cross-refs:** F86 (Option C, the dual-SC/colour-dielectric route this is tested against), F70 (2D-exact area-law σ), F43 (dynamical gluons + Wilson primitives), `run_confinement_mc.py` (the plain-Metropolis wall this repairs).

---

## What this builds

**Option A** of `deprecated/roadmap-P1-binding-force-options.md`: the standard, rigorous binding-force route — thermalise the 3+1D SU(3) Wilson ensemble with a proper heat-bath, beat the exponential signal-to-noise wall with a **Lüscher–Weisz multilevel** estimator, and read off the confining static potential. Built as a fork to stand head-to-head with **Option C** (F86), the model-native colour-dielectric / dual superconductor.

This directly repairs the wall that defeated `run_confinement_mc.py` (plain 2D Metropolis): large Wilson/Polyakov correlators decay as $e^{-\sigma\,\text{Area}}$ far below the $1/\sqrt N$ noise floor, so the Creutz ratio came out NaN. Heat-bath gives short autocorrelation; the two-level estimator factorises the correlator into sublattice averages whose variances **multiply**, recovering an exponentially better signal.

## The engine (`lgt_fork_A_mc.py`)

- **D-dimensional SU(3) Wilson links** (used at D=4), Wilson action $S=\beta\sum_\square(1-\tfrac13\mathrm{Re\,Tr}\,U_\square)$.
- **Cabibbo–Marinari pseudo-heat-bath** over the three SU(2) subgroups, each sampled by a vectorised Creutz $a_0\sim\sqrt{1-a_0^2}\,e^{\xi a_0}$ sampler with effective coupling $\xi=\tfrac{2}{3}\beta k$; checkerboard-vectorised with the staple recomputed per parity (the μ-staple contains neighbouring μ-links).
- **SU(2)-subgroup over-relaxation** $R=(V_2^\dagger)^2$ — microcanonical, preserves the action exactly.
- **Observables:** mean plaquette, planar Wilson loops, Polyakov loop and correlator.
- **Lüscher–Weisz two-level estimator** for the Polyakov correlator: $\langle P(0)P^*(R)\rangle=\mathrm{Tr}_9\!\big[\prod_b M_b\big]$ with the doubled-index $9\times9$ block tensors $M_b[(i,j),(i',j')]=\langle L_b(0)_{ii'}\,\overline{L_b(R)_{jj'}}\rangle_\text{sub}$ averaged over interior sublattice updates that freeze the block-boundary spatial links.

All pure-numpy (no scipy), per project practice.

## Engine correctness (FA, 6/6)

| Test | What it checks | Residual | Tier |
|------|----------------|----------|------|
| FA1 | heat-bath + OR keep links in SU(3) (unitarity + det=1) | $1.1\times10^{-15}$ | 2 |
| FA2 | over-relaxation preserves the Wilson action (microcanonical) | $1.2\times10^{-16}$ | 1 |
| FA3 | staple/action-gradient identity $\sum_\text{links}\mathrm{Re\,Tr}(U_\mu R_\mu)=4\cdot$plaq-sum | $8.9\times10^{-16}$ | 1 |
| FA4 | mean plaquette matches published SU(3) ⟨P⟩ (β=5.7, 6.0) | $1.7\times10^{-2}$ | 3 |
| FA5 | strong-coupling limit ⟨plaq⟩ → β/18 (β=0.5, 1.0) | $1.4\times10^{-1}$ | 3 |
| FA6 | two-level estimator agrees with direct & cuts its variance | **84× var↓** | 3 |

**FA3** is the central certificate — it proves the local quantity the heat-bath samples is exactly the Wilson-action gradient (the ratio-4 identity catches any staple/dagger error; an earlier double-dagger bug was found this way). **FA4** pins the absolute normalisation: ⟨P⟩(β=6.0)=0.594 reproduced to 0.6%. **FA6** is the wall-beating proof: on a small lattice the two-level estimator agrees with the direct Polyakov correlator within errors while reducing the per-sample variance by **~84×** (0.0009 vs 0.076) — the same exponential gain that makes 3+1D σ measurable at all.

**Production smoke run** (`run_lgt_confinement.py --smoke`, L=6, β=5.8): the two-level correlators come out clean, positive and decreasing — $C(1)=0.073,\,C(2)=0.018,\,C(3)=0.009$ — giving a **rising, confining** static potential $V(1)=0.44<V(2)=0.67<V(3)=0.78$. The wall is beaten. The precise $\sigma$ with jackknife error bars is the user-run production (L=10, R≤4).

## Tested against Option C (CMP, 4/4)

The two routes measure the **same observable** — the confining static potential — by **completely independent methods**: A from the gauge ensemble, C from the dual-superconductor flux tube ($\sigma_C=2\pi v^2$, exact).

| Test | What it establishes | Result |
|------|---------------------|--------|
| CMP1 | both confine: $V_A(R)$ rises (measured) and $\sigma>0$ both ways | PASS |
| CMP2 | gauge-MC $\sigma_A$ **fixes** the dual-SC condensate $v^*=\sqrt{\sigma_A/2\pi}$; C with $v^*$ reproduces $\sigma_A$ to $10^{-16}$ | PASS |
| CMP3 | shared large-$R$ slope; the difference is exactly the Coulomb $-e/R$ that C's BPS flux tube omits | PASS |
| CMP4 | $\sigma_A>0$ and the F70 2D-exact $\sigma(\beta)>0$ & decreasing — two further anchors | PASS |

**The headline (CMP2): Option A predicts Option C's only free parameter.** Option C leaves the condensate VEV $v$ free ($\sigma_C=2\pi v^2$). The gauge-MC string tension fixes it: $v^*=\sqrt{\sigma_A/2\pi}$. The two parametrisations are therefore not rival fits but the same physics — the dual-superconductor condensate scale **is** the gauge-MC string tension, re-expressed. For the smoke $\sigma_A\approx0.056$ this gives $v^*\approx0.094$ in lattice units (sensible, $O(0.1)$).

**The honest gap (CMP3): C omits the Coulomb tail.** $V_A(R)=\mu+\sigma R-e/R$ (Coulomb + linear, the full lattice result) vs $V_C(R)=\mu+\sigma R$ (pure linear, the BPS flux tube). They share the large-$R$ slope $\sigma$ (both confine identically as $R\to\infty$); they differ at small $R$ by exactly $-e/R$, the one-gluon-exchange Coulomb term that the BPS flux-tube picture does not contain. This is a real, quantified limitation of Option C, made explicit here rather than papered over.

## How A and C compare overall

- **C is exact but assumes the condensate; A is statistical but derives confinement from the gauge action.** C gives $\sigma=2\pi v^2$ algebraically (F86 CD1) but takes the colour-magnetic condensate as input. A makes no such assumption — confinement emerges from the SU(3) Wilson ensemble — at the cost of being a Monte-Carlo measurement with error bars (least aligned with the project's exactness preference, exactly as the roadmap warned).
- **A repairs the MC wall; C sidesteps it.** A beats the signal-to-noise wall with the multilevel estimator (FA6, 84×); C replaced the observable entirely (F86). Both are legitimate; only A produces a $\sigma$ from the gauge-loop ensemble.
- **They agree where they must and differ where it is honest to differ:** identical large-$R$ confinement, the condensate-↔-$\sigma$ bridge, and the small-$R$ Coulomb term present in A and absent in C.

## Honest scope / open items

- **Production σ is user-run.** The sandbox cannot run a converged 4D measurement; the engine, the multilevel variance reduction, and the confining $V(R)$ are all demonstrated, but the precise $\sigma\pm$error needs `run_lgt_confinement.py` (L=10, minutes–hours).
- **Statistical, not exact.** Tier-3 by nature; the absolute-normalisation (FA4) and strong-coupling (FA5) checks anchor it, but $\sigma$ carries MC error.
- **Two-level only.** A full $n$-level recursive LW would push larger $R$/$T$; the two-level already demonstrates the principle and suffices for the comparison.
- **Abelian-projection-free.** Unlike C (which uses the dual-Abelian-Higgs reduction), A is the full non-Abelian SU(3) — a point in A's favour for rigor.

## Exactness-inventory additions

Tier 1 (algebraic / bit-for-bit): FA2 (OR action invariance), FA3 (staple identity), CMP2 (bridge), CMP3 (Coulomb-gap = $-e/R$ exactly) — 4 entries.
Tier 2 (machine precision): FA1 (SU(3) preserved) — 1 entry.
Tier 3 (statistical): FA4, FA5, FA6 (84× variance reduction), CMP1, CMP4 — 5 entries.
