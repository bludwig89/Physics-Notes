# F236 — The full 3×3 Higgs-free see-saw: the F93/F76/F201 $E_g$ generation texture fixes the three light active masses (reducing exactly to F47 per generation), but forces PMNS $=\mathbb 1$ — a structural no-go that pins lepton mixing to the second-shell $T_{2g}$ channel, whose three amplitudes remain free inputs

**Date:** 2026-07-03 - 15:20
**Numbering:** **F236** (reserved for open-derivation prompt D1; prior session max in the F229–F235 band, re-checked).
**Status:** Derivation + honest negative result — 5/5 checks PASS (`test_F236_three_generation_seesaw.py`, ~15 s, numpy real/complex arithmetic with hand-rolled residual checks). **What is derived (exact/machine-precision):** the 3×3 see-saw $[[0,M_D],[M_D^\top,M_R]]$ generalises F47 and reduces to three copies of the F47 $M_D^2/M_R$ block at machine precision; with $M_D$ and $M_R$ both carrying the $E_g$ texture (the F93 O1 diagonal-traceless channel) the light matrix $m_\nu=-M_D M_R^{-1}M_D^\top$ is **diagonal**, so **PMNS $=\mathbb 1$** exactly. **What is a free input (the honest core):** large lepton mixing cannot come from $E_g$ alone — it is forced onto the second-shell $T_{2g}$ (axis-mixing) channel (F93 falsifiable commitment #1), whose three amplitudes are **not pinned** by the texture. All five oscillation observables ($\theta_{12},\theta_{13},\theta_{23},\Delta m^2_{21},\Delta m^2_{31}$) are reproducible, but with **6 inputs for 5 observables** — the *masses/hierarchy* are derived (F201 node), the *mixing angles* are free.
**Module:** `ca-simulation/ca_majorana.py` (new — promotes the F47 Majorana/see-saw primitives to 3×3, F47 open follow-up #1).
**Tests / results:** `tests/findings/test_F236_three_generation_seesaw.py` → `test-results/F236_three_generation_seesaw.json` (5/5 PASS).
**Cross-references:** [[F47-majorana-seesaw-higgs-free]] (the single-flavour block and the $M_D^2/M_R$ scaling this generalises; open follow-ups #1/#2), [[F201-kev-sterile-from-eg-texture]] ($M_R$ carries the $E_g$ texture; the $Z_3$ node that makes one eigenvalue light), [[F93-orthorhombic-Eg-vacuum]] (O1: $E_g$ = unique **non-mixing** diagonal splitter; **commitment #1**: $T_{2g}$ = unique off-diagonal/PMNS-like channel; O4: the $Z_3$ cosine form), [[F76-generation-mass-hierarchy-crystal-field]] (the $\sqrt m$ $Z_3$ texture, $\delta_e=12.73°$), [[F75-three-generations-from-bcc-irrep-selection]] (three generations = the $T_{1u}$ triplet), [[F92-per-constituent-phase-consistency]] (the $\sqrt2$ equipartition amplitude). External: NuFIT-5.2 normal-ordering global fit (the oscillation targets).

---

## 1. The prompt (D1) and the acceptance test

F47 built the Higgs-free single-flavour $\nu_R$ Majorana step and the see-saw scaling $m_\nu\approx M_D^2/M_R$. D1 asks to generalise to the full 3×3 case: assemble the 6×6

$$M_6=\begin{pmatrix}0 & M_D\\ M_D^\top & M_R\end{pmatrix},$$

with $M_R$ textured by the F93/F76 $Z_3$ ($E_g$) generation structure (F201), diagonalise for the three light active masses and the PMNS matrix, and state the acceptance:

> **Acceptance.** The light mass-squared splittings and PMNS angles reproduced within tolerance **from the lattice texture (no free mixing angles)**, *or* a clear account of which texture inputs remain free.

The outcome below is the **second branch, sharply**: the texture derives the light *masses* (and their hierarchy, via the F201 node) but is provably unable to generate the PMNS angles — those are a distinct ($T_{2g}$) input.

## 2. The texture is diagonal — the central structural fact

F93 O1 proved that the crystal field splitting the $T_{1u}$ generation triplet decomposes as

$$\mathrm{sym}(T_{1u}\otimes T_{1u})=A_{1g}\oplus E_g\oplus T_{2g},$$

with $E_g$ the **diagonal-traceless** channel (splits the three cube axes *without mixing them*) and $T_{2g}$ the **off-diagonal** channel (the *only* channel that mixes axes). The F93/F76/F201 generation texture is an $A_{1g}$ background plus an $E_g$ condensate (F93 O4), so in the cube-axis ("generation-axis") basis it is **exactly diagonal**:

$$\sqrt{M_a}=M_{R0}\big[\,1+\sqrt2\cos(\delta_\nu+\tfrac{2\pi a}{3})\,\big],\qquad M_R=\mathrm{diag}(M_a),\quad a=0,1,2.$$

The Dirac matrix $M_D$, being the same kind of $A_{1g}+E_g$ object on the same second-neighbour shell of the same BCC lattice, is diagonal in the **same** cube-axis basis (it may sit at its own angle $\delta_D$). Since the charged-lepton mass matrix is *also* $E_g$-diagonal in that basis, the charged-lepton rotation is $U_e=\mathbb 1$ in the cube-axis basis and $\mathrm{PMNS}=U_e^\dagger U_\nu=U_\nu$.

## 3. The 3×3 see-saw reduces to F47, exactly (S1)

Because $M_D$ and $M_R$ are simultaneously diagonal, the type-I light block

$$m_\nu=-M_D M_R^{-1}M_D^\top=-\mathrm{diag}\!\big(M_{D,a}^2/M_{R,a}\big)$$

is diagonal and the three light masses are **three independent copies of the F47 result** $|\lambda_-|=M_{D,a}^2/M_{R,a}$. Test **S1** verifies the module light masses equal the F47 per-generation Vieta form $M_D^2/M_R$ (the numerically stable branch F47 uses to dodge the $M_R\gg M_D$ cancellation) to machine precision:

| generation | $M_{D,a}$ (GeV) | $M_{R,a}$ (GeV) | module $m_a$ | F47 $M_D^2/M_R$ |
|---:|---:|---:|---:|---:|
| 1 | $5.0\times10^{-4}$ | $E_g$-textured | $\approx8.6\times10^{-20}$ | matches |
| 2 | $0.10$ | $E_g$-textured | $\approx5.8\times10^{-14}$ | matches |
| 3 | $1.0$ | $E_g$-textured | $\approx3.4\times10^{-13}$ | matches |

Max relative residual $<10^{-9}$; $\lVert m_\nu\rVert$ residual $=0$. The 3×3 construction is a faithful generalisation of F47, and the F201 $Z_3$ node (one $\sqrt{M_a}\to0$ at $\delta_\nu\to135°$) still makes one *heavy* $M_R$ eigenvalue light (the keV-sterile mechanism) — carried over unchanged.

## 4. PMNS $=\mathbb 1$: the $E_g$-only no-go (S2)

With $m_\nu$ diagonal, its eigenvectors are the coordinate axes, so

$$\boxed{\ \text{$E_g$ texture on both $M_D$ and $M_R$}\ \Longrightarrow\ \text{PMNS}=\mathbb 1,\ \theta_{12}=\theta_{13}=\theta_{23}=0\ }$$

Test **S2** returns all three angles $=0$ to $<10^{-9}$ degrees. This is a genuine structural obstruction: changing the condensate angles $\delta_D,\delta_\nu$ or the scale $M_{R0}$ only rescales the *eigenvalues* — the *eigenvectors* stay pinned to the cube axes, so **no choice of $E_g$ inputs produces any mixing at all.** The observed large angles ($\theta_{12}\approx33°$, $\theta_{23}\approx49°$) are therefore impossible from the $E_g$ texture. (Contrast the near-diagonal CKM: for quarks small mixing would be a near-success of the $E_g$-diagonal picture; for leptons the mixing is $O(1)$ and the no-go is stark.)

## 5. Mixing lives in $T_{2g}$ — the F93 commitment, made quantitative (S3, S4)

F93's falsifiable commitment #1 states that any inter-generation mixing operator **must** come from the second-shell $T_{2g}$ (axis-mixing) channel. Adding a symmetric off-diagonal $T_{2g}$ perturbation to $M_R$,

$$M_R\to M_R+\begin{pmatrix}0 & t_{xy} & t_{zx}\\ t_{xy} & 0 & t_{yz}\\ t_{zx} & t_{yz} & 0\end{pmatrix},$$

switches the PMNS angles on (test **S3**: $\max\theta>1°$ for generic $t$). Fitting $(\delta_D,\delta_\nu,M_{R0},t_{xy},t_{yz},t_{zx})$ to the NuFIT-5.2 normal-ordering targets reproduces **all five** observables (test **S4**, final cost $\approx0$):

| observable | fit | NuFIT-5.2 (NO) | status |
|---|---:|---:|---|
| $\theta_{12}$ | $33.4°$ | $33.4°$ | reproduced |
| $\theta_{13}$ | $8.6°$ | $8.6°$ | reproduced |
| $\theta_{23}$ | $49.0°$ | $49.0°$ | reproduced |
| $\Delta m^2_{21}$ | $7.42\times10^{-5}$ eV² | $7.42\times10^{-5}$ | reproduced |
| $\Delta m^2_{31}$ | $2.51\times10^{-3}$ eV² | $2.51\times10^{-3}$ | reproduced |

**But this is a fit, not a prediction:** six inputs for five observables. The three $T_{2g}$ amplitudes are the mixing degrees of freedom, and the texture does not pin them. (Note $\theta_{13}$ in particular is unreachable if $M_D$ is *locked* to the charged-lepton texture — freeing $M_D$'s own angle $\delta_D$ is one of the extra inputs.) This is the honest content of the acceptance test's second branch.

## 6. 6×6 ↔ type-I consistency, hand-rolled (S5)

Per the numerics House Rule, the block-diagonalisation is cross-checked two ways. (i) The three smallest $|$eigenvalues$|$ of the full complex $6\times6$ $M_6$ match the exact type-I block $m_\nu=-M_DM_R^{-1}M_D^\top$ in the hierarchical regime $M_{R0}=10^{12}$ to $<10^{-9}M_{R0}$ (test **S5**, residual $\sim10^{-20}$ for the $E_g$-only case; $\sim10^{-5}$-relative subleading corrections when $T_{2g}$ is switched on, as expected for finite $M_D/M_R$). (ii) Every spectrum is validated by a hand-rolled residual $\max_j\lVert Mv_j-\lambda_j v_j\rVert$ rather than trusting the library eigensolver — the light-sector residual on $m_\nu$ is $0.0$/machine-zero throughout.

## 7. What is derived vs computed vs free

| Piece | Status |
|---|---|
| 6×6 see-saw $[[0,M_D],[M_D^\top,M_R]]$; type-I $m_\nu=-M_DM_R^{-1}M_D^\top$ | **Derived** (standard construction; F47 §Open #2) |
| 3×3 diagonal see-saw = three F47 $M_D^2/M_R$ blocks | **Exact / machine-precision** (S1) |
| $M_R$, $M_D$ diagonal in cube-axis basis (both $E_g$, F93 O1/O4) | **Argued** (structural, same shell/lattice; not a new posit) |
| $E_g$ texture $\Rightarrow$ PMNS $=\mathbb 1$ (no-go) | **Exact** (S2) — a proof, not a fit |
| one light eigenvalue from the $Z_3$ node ($\delta_\nu\to135°$) | **Derived** (F201, carried over) |
| light-mass *ordering/hierarchy* from the texture | **Computed** (F76/F201 machinery) |
| PMNS *angles* | **Free** — a $T_{2g}$ input the $E_g$ texture does not pin (S3, S4) |
| the three $T_{2g}$ amplitudes ($t_{xy},t_{yz},t_{zx}$) | **Free inputs** (3 numbers for 3 angles + 1 phase) |
| overall Majorana scale $M_{R0}$, Dirac angle $\delta_D$ | **Free** (as in F201/F76) |

## 8. Verdict and implications

The lattice **does** derive the light-neutrino *mass sector*: the 3×3 see-saw is a clean generalisation of F47 (three $M_D^2/M_R$ blocks, machine-precise), and the $E_g/Z_3$ texture supplies the hierarchy and — via the F201 node — one naturally light state. It **does not** derive PMNS mixing: the $E_g$ texture is diagonal by representation theory (F93 O1), so it forces PMNS $=\mathbb 1$, and the observed $O(1)$ angles must be carried by the orthogonal second-shell $T_{2g}$ channel whose amplitudes are free. This *confirms* F93's falsifiable commitment #1 ($T_{2g}$ = the unique off-diagonal channel) and *sharpens* the open problem: deriving the neutrino mixing angles is now precisely the problem of deriving the second-shell $T_{2g}$ condensate (a gap computation in the $T_{2g}$ channel), exactly parallel to how deriving the charged-lepton masses reduced to the $E_g$ Landau ratio (F93 §8, F234). The number of genuinely free lepton-sector inputs after F236 is: $\{M_{R0},\ \delta_D,\ \delta_\nu\}$ (masses/scale, already known free) $+\ \{t_{xy},t_{yz},t_{zx}\}$ (mixing, newly localised to $T_{2g}$).

## 9. Falsifiable structural commitments

1. Any future lattice derivation of neutrino mixing **must** produce it from the second-shell $T_{2g}$ channel — an $E_g$-only or $A_{1g}$-only construction is provably incapable (S2). A model that claims PMNS from the diagonal texture alone is falsified here.
2. Because the same second shell carries both the $E_g$ (mass) and $T_{2g}$ (mixing) channels, the neutrino mixing texture and the charged-lepton mass texture are **not independent objects** — a $T_{2g}$ derivation that ignores the coexisting $E_g$ condensate is incomplete.
3. If the eventual $T_{2g}$ amplitudes are forced small by the lattice (as they plausibly are for quarks → near-diagonal CKM), the model would predict *small* lepton mixing — falsified by data; large lepton mixing is a nontrivial demand on the $T_{2g}$ gap.

## 10. Test summary (`test_F236_three_generation_seesaw.py`, 2026-07-03 - 15:20)

| Check | Statement | Result | Tier | Status |
|---|---|---|---|---|
| S1 | 3×3 diagonal see-saw = three F47 $M_D^2/M_R$ blocks | rel. resid $<10^{-9}$, $\lVert m_\nu\rVert$ resid $0$ | machine precision | PASS |
| S2 | $E_g$-only $\Rightarrow$ PMNS $=\mathbb 1$ | all angles $<10^{-9}°$ | exact (no-go) | PASS |
| S3 | $T_{2g}$ switches mixing on | $\max\theta>1°$ | qualitative | PASS |
| S4 | data reproducible with free $T_{2g}$ | all 5 obs matched; 6 inputs / 5 obs | fit (not predictive) | PASS |
| S5 | 6×6 ↔ type-I block, hand-rolled residual | $\lesssim10^{-20}$ ($E_g$-only) | machine precision | PASS |

**Overall 5/5 PASS** (~15 s). JSON: [`test-results/F236_three_generation_seesaw.json`](../test-results/F236_three_generation_seesaw.json).

## 11. Provenance

- New content: the 3×3 promotion module `ca_majorana.py` (F47 open follow-up #1); the exact reduction of the diagonal 3×3 see-saw to F47; the $E_g$-only PMNS-$=\mathbb 1$ no-go (S2) and its localisation of lepton mixing to the $T_{2g}$ channel; the honest input count.
- Reuses: F47 see-saw algebra and the Vieta stable branch; F93 O1/O4 representation theory and commitment #1; F76/F93/F201 $Z_3$ texture; F92 $\sqrt2$ amplitude.
- Verification: `tests/findings/test_F236_three_generation_seesaw.py` (2026-07-03 - 15:20, 5/5 PASS), results `test-results/F236_three_generation_seesaw.json`. Oscillation targets: NuFIT-5.2 normal-ordering central values.
