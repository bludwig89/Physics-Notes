---
id: CL270
title: The second dispersive clock that a free composite cell carries is an artifact of freeness — the model's interactions break it maximally and obstruct every O(G) deformation of it, so the rank-one time count is the count of the interacting theory at any cell, not only at the minimal one
slug: second-clock-is-an-artifact-of-freeness
tier: supporting
kind: no_go
status: live
domain: [QM, SR, QFT]
exactness: machine
findings: [F315, F313]
tests: [F315-V-interaction]
modules: [casim.engine.lattice.time_signature_interacting]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL269
falsifier: stated
first_issued: 2026-08-12
last_verified: 2026-08-12
provenance: authored
review_state: authored
confidence: medium
---

# CL270 — The second clock is an artifact of freeness

## Statement

The second dispersive commuting flow $V=\mathbb I_\text{branch}\otimes A$ that the **free** $s=4$
Dirac walk carries (F313 §9, $\lVert[V,D]\rVert\le2.2\times10^{-16}$ at every mass) does **not**
survive the model's interactions:

- $V$ is broken **maximally** — $\max\lvert\Delta\phi_V\rvert = 3.113$, i.e. $\simeq\pi$, the
  largest a phase difference can be — by the contact kernel (Hubbard/NJL, F217/F77) **and** by
  photon exchange (F68, $1/q^2$). The verdict does not depend on the kernel's form, only on its
  being a genuine scatterer.
- **No $O(G)$ deformation of $V$ can be conserved.** A deformed charge $Q_1+GQ_2$ requires
  $Q_2=\Delta q_V\,W/\Delta\Omega$, which is solvable except where $\Delta\Omega\equiv0\pmod{2\pi}$;
  on those **resonant** elements $\Delta q_V$ must vanish by itself and does not — 1 340 of them
  carry $\Delta q_V$ up to $2.876$.

Therefore the rank-one time count of CL269 is **not** confined to the minimal cell $s=2$. It is the
count of the **interacting** theory at any cell.

## What it extends

It is a standard and correct observation in many-body physics that a free theory is integrable and
carries a large commutant of extra conserved charges, and that generic interactions destroy them.
This claim applies that to the model's spacetime signature, where the consequence is unusual: the
extra commuting flow of the free composite is a candidate **second time dimension**, so its removal
is what makes "one time" a statement about the physical theory rather than about a free
approximation to it. Established physics assumes one time and never has to ask; this claim is the
model paying that cost explicitly.

It also closes, in the negative, the standing question of whether the CA model is **integrable** at
the relevant order. It is not.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F315-V-does-not-survive-interaction.md` | the full argument: C1 free limit, C2 integrable control, C3/C4 both kernels, C5 the obstruction, C6 its control, C7/C8 robustness, C10 the honest negative | machine |
| `tests/registry/lattice.yaml` → `F315-V-interaction` | 11/11 PASS, gate tier, **three controls verified RED** (`L=2`, `kind=mode_diagonal`, `res_tol=0.0`) | machine, tol $10^{-12}$ |
| `test-results/F315_V_interaction.json` | result artifact; five runner claims armed | machine |
| `findings/F313-one-time-dimension-from-the-update-commutant.md` | §9, the residual this discharges | exact |

**The reduction is an identity.** Because $\Gamma(V)$ commutes with $\Gamma(D)$ exactly,
$[\Gamma(V),U]=\Gamma(D)[\Gamma(V),e^{-iH_\text{int}}]$, so "V survives iff $H_\text{int}$ connects
only states of equal $q_V$ mod $2\pi$" involves no approximation.

**The test is controlled in both directions**, which is what makes a negative result meaningful
here: an integrable mode-diagonal interaction yields **zero** obstructed elements, so the test can
report survival; and on the same resonant set the *evolution's own* charge is conserved to
$1.8\times10^{-15}$, so the test is not flagging every charge indiscriminately.

## Falsifier

1. **Exhibit a nonzero $Q_2$ solving $[Q_1,H_\text{int}]+[Q_2,H_0]=0$ with $Q_1=q_V$** — i.e. show
   the 1 340 resonant obstructions are an artifact of the resonance tolerance rather than exact
   degeneracies.
2. **Show the resonant set is empty at a defensible tolerance.** (The `res_tol=0.0` control.)
3. **Exhibit a model interaction — a genuine scatterer, not mode-diagonal — under which $V$
   survives.**
4. **Show the F86 colour dielectric conserves $q_V$.** The confining non-Abelian sector was named in
   F313's falsifier 5 and is **not** tested here; if it restored the second flow, this claim would
   have to be narrowed to the Abelian sectors.
5. **Show the obstruction vanishes as $L\to\infty$** — that it is a finite-grid umklapp artifact
   with no continuum counterpart. Given the §5 mechanism below, this is the most interesting attack
   on the claim and it is not answered.

## Status & history

**`live`, and issued as a `no_go`** — it closes an option (a physical second time) rather than
predicting a number, so it belongs to the falsification record and should be among the last things
archived.

**`confidence: medium`, for two stated reasons.** The obstruction is **leading order in $G$**. That
is the standard and decisive form of the no-extra-conserved-charge argument, but it is not an
all-orders proof and this card does not claim one. And the **F86 colour dielectric** — one of the
two interactions F313's falsifier 5 actually named — was not tested; the two kernels here are the
contact vertex and photon exchange.

**A prediction of the session that was wrong, kept rather than dropped.** The $\langle100\rangle$
restriction was expected to go blind, because the model's on-axis dispersion is exactly linear
(F20/F301; residual $9.3\times10^{-15}$, re-measured in F315's C10) and a linear phase is additive
under momentum conservation. It does **not** go blind — 2 592 obstructed elements — because the
eigenphase is $\arccos$-folded into $(-\pi,\pi]$, so **umklapp destroys additivity even on an
exactly linear branch**. This changes the stated mechanism: the breaking is driven by the mod-$2\pi$
structure of a QCA eigenphase, not by lattice curvature alone. It is a stronger reason, and it is
why falsifier 5 above is the live attack.

**The $L=2$ trap, recorded because it was hit.** The first many-body run of this work was on an
$L=2$ grid, where every $\theta_j\in\{0,\pi\}$, every $\sin\theta_j=0$, the Bloch vector vanishes
identically and the walk is trivial — a clean false negative reporting $10^{-16}$ for every
commutator. It is now a declared control that must go RED.

## Sources

- `findings/F315-V-does-not-survive-interaction.md`
- `findings/F313-one-time-dimension-from-the-update-commutant.md` — §9 and falsifier 5, the target
- `src/casim/engine/lattice/time_signature_interacting.py`
- `tests/findings/test_F315_V_interaction.py` — record `F315-V-interaction`, 11/11, three controls RED
- `test-results/F315_V_interaction.json`
- `docs/claims/CL269-one-time-from-update-commutant.md` — the card this rolls up to, whose composite-cell contingency this discharges
- `references/qca-papers-1-4-overview.md` — Paper 1 Eqs. 15 and 23, the walk and its Dirac composite
