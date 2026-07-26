# F254 — No lattice selector for the PMNS $T_{2g}$ channel: the three neutrino-mixing amplitudes transform as **three inequivalent 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$) of the $E_g$-stabilizer $D_{2h}$, so no residual symmetry relates them and the F92 equipartition mechanism cannot apply — the PMNS angles are **genuinely free** (a stabilizer theorem, parallel to D3's free $\beta$)

**Date:** 2026-07-16 - 16:58
**Numbering:** **F254** (open-derivation prompt **D1** follow-up; F253 was taken by a concurrent session — `F253-weight-as-phase-scale-nogo`, re-checked before assigning).
**Status:** Derivation + honest-negative closure — 4/4 PASS (`test_F254_t2g_pmns_selector.py`, ~9 s). **What is proven (exact / group-theoretic):** under the generic-$E_g$ stabilizer $D_{2h}$ (F93 O3), the three second-shell $T_{2g}$ axis-mixing amplitudes $(t_{xy}, t_{yz}, t_{zx})$ transform as **three inequivalent nontrivial 1-d irreps** ($B_{1g}, B_{2g}, B_{3g}$: distinct, zero-sum characters over the 8 group elements) — so **no residual lattice symmetry relates them** (T1). The democratic point $t_{xy}=t_{yz}=t_{zx}$ is invariant under only $\{+\mathbb 1, -\mathbb 1\}$ (order 2 of 8) → **not symmetry-protected**, and the F92 equipartition selector (which equalizes weights *within a single degenerate multiplet*) **cannot apply**, because the $E_g$ condensate splits the $T_{2g}$ triplet into three *inequivalent* irreps — there is no degenerate multiplet to equipartition over (T2). **Numerical no-go (T3):** democratic and single-channel one-parameter $T_{2g}$ ansätze miss NuFIT-5.2 (NO) by $>100^\circ{}^2$; only the **full three-amplitude** fit reaches the data ($\sim10^{-11}$ deg), with exactly **3 inputs for 3 angles** (no predictive slack). **Verdict:** the D1 selector **provably does not exist** among residual-symmetry / equipartition mechanisms — the PMNS angles are **genuinely free** (three independent order parameters in three inequivalent $D_{2h}$ channels), sharpening F236's fit-counting statement into a stabilizer theorem exactly parallel to D3's geon-abundance $\beta$.
**Module:** `ca-simulation/derive_t2g_pmns_selector.py` (new — the $D_{2h}$ irrep analysis + the one-parameter no-go scan); reuses `ca_majorana.py` (F236).
**Tests / results:** `tests/findings/test_F254_t2g_pmns_selector.py` → `test-results/F254_t2g_pmns_selector.json` (4/4 PASS).
**Cross-references:** [[F236-three-generation-seesaw-pmns]] (D1 anchor: $E_g$ texture ⇒ PMNS $=\mathbb 1$; mixing localised to $T_{2g}$; this finding proves the $T_{2g}$ amplitudes cannot be fixed by symmetry), [[F93-orthorhombic-Eg-vacuum]] (O1: $\mathrm{sym}(T_{1u}^{\otimes2})=A_{1g}\oplus E_g\oplus T_{2g}$, $T_{2g}$ = unique off-diagonal channel, **commitment #1**; O3: generic-$\delta$ stabilizer $=D_{2h}$ with **zero** axis permutations — the theorem this finding builds on), [[F92-per-constituent-phase-consistency]] (the equipartition mechanism whose applicability is here decided — negatively), [[F76-generation-mass-hierarchy-crystal-field]] / [[F201-kev-sterile-from-eg-texture]] ($Z_3$ / $E_g$ texture that fixes the masses), [[F47-majorana-seesaw-higgs-free]] (single-flavour see-saw). External: NuFIT-5.2 normal-ordering global fit (the mixing targets).

---

## 1. The prompt (D1) and the acceptance test

F236 built the full $3\times3$ Higgs-free see-saw and proved a structural no-go: with the $E_g$ ($Z_3$) generation texture on both $M_D$ and $M_R$, the light matrix $m_\nu=-M_D M_R^{-1}M_D^\top$ is diagonal in the cube-axis basis, so **PMNS $=\mathbb 1$ exactly**. Large lepton mixing must therefore be carried by the orthogonal second-shell $T_{2g}$ (axis-mixing) channel (F93 commitment #1), whose three amplitudes $(t_{xy}, t_{yz}, t_{zx})$ F236 left as **free inputs** (6 inputs reproduce 5 observables). The D1 prompt asks:

> **Acceptance.** Find a symmetry / dynamical selector on the lattice that fixes the $T_{2g}$ amplitudes (and hence the PMNS angles) from geometry — reproducing the angles with **no free mixing inputs** — *or* a clean statement that the $T_{2g}$ amplitudes are **genuinely free** (parallel to D3's $\beta$).

The outcome below is the **second branch, sharpened into a theorem**: not only does F236's fit use "one input per angle," but the residual symmetry of the $E_g$-broken vacuum *provably* cannot relate or fix those inputs, and the one candidate mechanism the prompt names (F92 equipartition) is structurally inapplicable.

## 2. The residual symmetry: $D_{2h}$ acts on $T_{2g}$ as three inequivalent 1-d irreps (T1)

F93 O3 proved that a generic-angle $E_g$ condensate leaves the stabilizer
$$D_{2h}=\{\,\mathrm{diag}(s_x, s_y, s_z)\ :\ s_a\in\{+1,-1\}\,\}\quad(\text{order }8),$$
with **no** nontrivial axis permutation (the generation $S_3$ is completely broken). A $T_{2g}$ perturbation is the symmetric off-diagonal matrix
$$T=\begin{pmatrix}0 & t_{xy} & t_{zx}\\ t_{xy} & 0 & t_{yz}\\ t_{zx} & t_{yz} & 0\end{pmatrix},\qquad T\mapsto S\,T\,S^\top,\ \ (S T S^\top)_{ij}=s_i s_j\,T_{ij}.$$
So under $D_{2h}$ each amplitude picks up a **sign**:
$$t_{xy}\mapsto s_x s_y\,t_{xy},\qquad t_{yz}\mapsto s_y s_z\,t_{yz},\qquad t_{zx}\mapsto s_z s_x\,t_{zx}.$$

Computing the character (the sign) of each amplitude over the 8 group elements gives three **distinct** vectors, each summing to zero (orthogonal to the trivial rep):

| amplitude | $D_{2h}$ character (over the 8 signs) | irrep |
|---|---|---|
| $t_{xy}$ | $[+,+,-,-,-,-,+,+]$ | $B_{1g}$ (character $\chi=s_x s_y$) |
| $t_{yz}$ | $[+,-,-,+,+,-,-,+]$ | $B_{2g}$ (character $\chi=s_y s_z$) |
| $t_{zx}$ | $[+,-,+,-,-,+,-,+]$ | $B_{3g}$ (character $\chi=s_z s_x$) |

$$\boxed{\ (t_{xy}, t_{yz}, t_{zx})\ \text{transform as three INEQUIVALENT 1-d irreps }B_{1g}\oplus B_{2g}\oplus B_{3g}\text{ of }D_{2h}\ }$$

Because the three irreps are inequivalent, **no element of the residual symmetry group maps one amplitude to another**. They are three genuinely independent order parameters, each condensing in its own symmetry channel. This is the group-theoretic root of F236's "free inputs": the $E_g$ condensate that *defines* the vacuum has already removed every symmetry that could have tied the mixing amplitudes together.

## 3. Why F92 equipartition cannot rescue a selector (T2)

The prompt's suggested attack is the F92 saturation-equipartition mechanism — the same principle that fixed the $\sqrt2$ amplitude of the $E_g$ texture (the $45^\circ$ equipartition of a two-component doublet). Equipartition is a statement **within one degenerate multiplet**: it distributes weight equally among the components of a *single* irreducible representation that the dynamics leaves degenerate. But §2 shows the $E_g$ condensate **splits** the $T_{2g}$ triplet into three *inequivalent* 1-d irreps — there is no surviving degenerate multiplet across which weight could be equipartitioned. Concretely, the democratic (would-be equipartitioned) point $t_{xy}=t_{yz}=t_{zx}$ is invariant under only $\{+\mathbb 1, -\mathbb 1\}$ of $D_{2h}$ (stabilizer order **2 of 8**, verified), so democracy is *not* symmetry-protected: any dynamics respecting only the residual $D_{2h}$ is free to give the three channels different gaps. **The mechanism that fixed the $E_g$ $\sqrt2$ has no $T_{2g}$ analog.**

A nonzero $T_{2g}$ condensate further breaks $D_{2h}$ (a single $B_{ig}$ amplitude survives only its own $\mathbb Z_2\times\mathbb Z_2$ subgroup), so lepton mixing is a genuinely **independent, second symmetry-breaking event** stacked on the $E_g$ vacuum — not a descendant of it. This is the precise structural sense in which the PMNS angles parallel D3's geon abundance: a free order parameter of an orthogonal breaking, not an omission.

## 4. Numerical no-go: every one-parameter symmetric ansatz fails (T3)

Using the F236 machinery (`ca_majorana.py`) with the reference hierarchical Dirac masses $M_D=(5\times10^{-4}, 0.10, 1.0)$ GeV and $M_{R0}=10^{12}$, scanning the neutrino condensate angle $\delta_\nu$ and the $T_{2g}$ scale:

| ansatz | free params | best fit to NuFIT-5.2 (NO) | cost | disposition |
|---|---|---|---|---|
| democratic $t_{xy}=t_{yz}=t_{zx}$ | 1 (scale) | $(\theta_{12},\theta_{13},\theta_{23})\approx(22.5^\circ, 19.6^\circ, 63.9^\circ)$ | $462\ \mathrm{deg}^2$ | **fails** |
| single $t_{xy}$ only | 1 | $(33.4^\circ, 0, 0)$ | $2475\ \mathrm{deg}^2$ | **fails** (drives $\theta_{12}$ only) |
| single $t_{yz}$ only | 1 | $(0, 0, 49.0^\circ)$ | $1190\ \mathrm{deg}^2$ | **fails** (drives $\theta_{23}$ only) |
| single $t_{zx}$ only | 1 | $(33.4^\circ, 0, 90^\circ)$ | $1755\ \mathrm{deg}^2$ | **fails** |
| **full** $(t_{xy}, t_{yz}, t_{zx})$ | 3 | all three matched | $\max\lvert\text{resid}\rvert\approx1.3\times10^{-11}$ deg | **reaches data** |

Targets: $\theta_{12}=33.4^\circ,\ \theta_{13}=8.6^\circ,\ \theta_{23}=49.0^\circ$. The single-channel rows are the numerical face of the T1 theorem: each $T_{2g}$ amplitude, living in its own $D_{2h}$ irrep, drives essentially **one** independent rotation, so no single amplitude (and no symmetric combination of them) can populate all three angles. Only when all three inequivalent channels are switched on independently is the data reachable — and then it is reached with **exactly three inputs for three angles**, i.e. with **zero predictive slack** (a fit, not a prediction). This confirms F236's input count is not an artifact of a poor ansatz: it is forced.

## 5. Consistency check: the mass sector is untouched (T4)

Turning the selector search on does not disturb F236's derived mass sector: with $T_{2g}=0$ the $E_g$-only texture still gives PMNS $=\mathbb 1$ to $<10^{-6}$ deg (F236 S2 no-go reproduced), so the three light masses / hierarchy remain the derived outputs they were, and only the mixing is at issue.

## 6. What is derived vs computed vs free (updated after F254)

| Piece | Status |
|---|---|
| light-$\nu$ masses + hierarchy (from $E_g/Z_3$ texture + F201 node) | **Derived** (F236/F201, carried over) |
| $E_g$-only $\Rightarrow$ PMNS $=\mathbb 1$ | **Exact no-go** (F236 S2; T4 here) |
| $(t_{xy}, t_{yz}, t_{zx})$ transform as $B_{1g}\oplus B_{2g}\oplus B_{3g}$ of $D_{2h}$ | **Exact / group-theoretic** (T1) — three inequivalent irreps |
| no residual symmetry relates the three amplitudes | **Proven** (T1) |
| F92 equipartition selects the $T_{2g}$ amplitudes | **Excluded** (T2) — no degenerate multiplet to equipartition |
| PMNS angles reproducible only with the full 3 amplitudes | **Numerical** (T3) — 3 inputs / 3 angles, no slack |
| the three $T_{2g}$ amplitudes (→ 3 mixing angles) | **Genuinely free** (this finding) — three independent $D_{2h}$ order parameters |
| Dirac CP phase | **Free** (needs complex $T_{2g}$ — a 4th input; unchanged) |

## 7. Verdict and implications

The D1 target **closes as a sharpened honest-negative**: the PMNS mixing angles are genuinely free inputs, and this is now a **theorem about the residual symmetry** of the $E_g$-broken vacuum, not merely an observation about input-counting. The $E_g$ condensate — the very object that derives the charged-lepton and neutrino *mass* spectra — breaks the generation $S_3$ so completely ($D_{2h}$, zero axis permutations) that the three $T_{2g}$ mixing channels land in three *inequivalent* 1-d irreps, with no symmetry relating them and no degenerate multiplet for equipartition to act on. A lattice derivation of neutrino mixing therefore cannot come from a symmetry selector at all; it must come from an **explicit dynamical computation of three independent $T_{2g}$ gaps** ($B_{1g}, B_{2g}, B_{3g}$), one per channel — the direct analog of how the charged-lepton masses reduce to the $E_g$ Landau ratio (F93 §8, F234), but now three-fold and *un-tied by symmetry*. Until such a three-channel gap computation exists, the PMNS angles stand as free order parameters exactly parallel to D3's geon-abundance $\beta$.

This also **tightens F93's falsifiable commitment #1**: it is not merely that mixing "must come from $T_{2g}$" — the $T_{2g}$ channel is *irreducibly three-dimensional and un-symmetric* in the broken vacuum, so any future claim to derive PMNS from a *single* $T_{2g}$ parameter (democratic, equipartitioned, or otherwise symmetric) is falsified here (T3).

## 8. Falsifiable structural commitments

1. Any lattice derivation of the PMNS angles must supply **three independent** $T_{2g}$ amplitudes ($B_{1g}, B_{2g}, B_{3g}$ channels); a construction that fixes them by a *single* symmetry parameter (democracy / equipartition / $\mathbb Z_3$) is provably incapable of reaching NuFIT (T2, T3) and is falsified.
2. Because the three channels are inequivalent irreps, a correct derivation will generically predict **three different** $T_{2g}$ gaps; a computation that returns them equal (democratic) contradicts the data and is falsified.
3. The $T_{2g}$ condensate further breaks $D_{2h}\to$ a $\mathbb Z_2$; if a future lattice dynamics forbids this secondary breaking (e.g. protects the full $D_{2h}$), the model would predict **zero** lepton mixing — falsified by data. Nonzero PMNS is thus a nontrivial demand that the $T_{2g}$ channels *do* condense.

## 9. Test summary (`test_F254_t2g_pmns_selector.py`, 2026-07-16 - 16:58)

| Check | Statement | Result | Tier | Status |
|---|---|---|---|---|
| T1 | $(t_{xy}, t_{yz}, t_{zx})$ = three inequivalent 1-d irreps of $D_{2h}$ | distinct zero-sum characters | exact (group theory) | PASS |
| T2 | democracy unprotected (stab. order 2/8); equipartition inapplicable | order $=2$ | exact | PASS |
| T3 | one-parameter symmetric ansätze fail; full 3-amp reaches data | democratic $462\ \mathrm{deg}^2$; full $1.3\times10^{-11}$ deg | numerical | PASS |
| T4 | $E_g$-only $\Rightarrow$ PMNS $=\mathbb 1$ (F236 no-go preserved) | $<10^{-6}$ deg | exact | PASS |

**Overall 4/4 PASS** (~9 s). JSON: [`test-results/F254_t2g_pmns_selector.json`](../test-results/F254_t2g_pmns_selector.json).

## 10. Provenance

- New content: the $D_{2h}$-irrep decomposition of the $T_{2g}$ triplet ($B_{1g}\oplus B_{2g}\oplus B_{3g}$, three inequivalent 1-d irreps, T1); the equipartition-inapplicability argument (T2); the one-parameter numerical no-go and the "3 inputs / 3 angles, no slack" statement (T3); the resulting sharpened honest-negative closure of D1.
- Reuses: F236 `ca_majorana.py` see-saw + PMNS pipeline; F93 O1/O3 representation theory and the $D_{2h}$ stabilizer theorem; F92 equipartition (whose scope is here delimited); NuFIT-5.2 normal-ordering targets.
- Verification: `tests/findings/test_F254_t2g_pmns_selector.py` (2026-07-16 - 16:58, 4/4 PASS), results `test-results/F254_t2g_pmns_selector.json`; driver `ca-simulation/derive_t2g_pmns_selector.py`.
