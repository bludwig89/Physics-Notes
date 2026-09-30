# F404 — Fork: Koide pseudo-masses for quarks — excluded with lepton-like amplitudes, viable but non-predictive with a negative lightest down amplitude

**Date:** 2026-09-24 - 13:10
**Status:** Candidate finding (fork) — 8/8 checks PASS (P1, P6 exact in sympy; P2, P3, P5 quantitative, P3 with an exact criterion; P4a, P4b, P7 numerical searches). Three declared controls, each red exactly where declared. **Verdict on route 1: viable only by re-expressing the data; it predicts nothing the inputs don't already fix.**
**Module:** `casim.engine.forks.particles.koide_pseudomass_fork` (new, `forks/`, status `fork_live`)
**Test record:** `F404-koide-pseudomass-fork` (tier gate, entry `check_koide_pseudomass_fork`), driver `tests/findings/test_F404_koide_pseudomass_fork.py` → `test-results/F404_koide_pseudomass_fork.json`
**Checked:** 2026-09-24 - 15:30 — cold blind re-derivation + adversarial referee, **CONFIRMED-NARROWER**; P4a's penalty-weight artifact and P7's "every angle pair" overreach fixed in place (see `docs/reviews/F404-review-2026-09-24.md`).
**Reviewed:** 2026-09-24 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F404-review-2026-09-24.md))
**Claim:** CL316 (`docs/claims/CL316-koide-pseudomass-quark-route-nonpredictive.md`)
**Cross-references:** [[F76]] (quark $Q_\text{up}=0.849$, $Q_\text{down}=0.731$), [[F78]] (mass = amplitude squared), [[F93]] (E_g on the cube axes), [[F175]] (δ\* = 2/9), [[F346]] / [[F347]] (quark Koide probes), [[F403]] (the same off-diagonal channel for PMNS), research report `reports/Quark neutrino hierarchy lattice fit.md` route 1.

---

## Summary

Route 1 of the 2026-09-24 flavour report (Gérard–Goffinet–Herquet, PLB 633 (2006) 563; Żenczykowski, arXiv:1301.4143) keeps Koide exact ($k=1$, $Q=2/3$) on quark **pseudo-masses** and puts the departure from Koide into the quark mixing. This finding builds that route in the model's language and tests it. Each charged sector gets a Hermitian amplitude matrix $S_f=\mu_f(\mathbb 1+\sqrt2\,\hat E(\delta_f))+T_f$ on the $T_{1u}$ triplet: the A₁g + E_g part is exact Koide on the cube axes, as for the charged leptons, and $T_f$ holds the $T_{2g}$ (real symmetric) and $T_{1g}$ (imaginary antisymmetric) off-diagonals, which carry both the Q deviation and the CKM. Five results:

1. **The off-diagonal weight is fixed by data (exact identity).** $Q_\text{phys}-Q_\text{pseudo}=\lVert S_\text{off}\rVert_F^2/(\operatorname{tr}S)^2$ for every Hermitian $S$. Quarks need $\lVert S_\text{off}\rVert/\operatorname{tr}S=0.427$ (up) and $0.254$ (down, all positive); that is 74% and 44% of the E_g amplitude. Charged leptons need exactly zero.
2. **With lepton-like (all-positive) amplitudes the route is excluded.** Exact Koide pseudo-diagonals in both sectors *and* the measured CKM cannot hold together: among solutions that actually hold the CKM ($\chi^2\le1$), the smallest Koide violation is $2.1\times10^{-2}$ of $\operatorname{tr}S$ (mixed scheme; $2.3\times10^{-2}$ at $M_Z$), about 300 times the 0.007% shape precision the charged leptons meet. *(Corrected 2026-09-24 - 15:30: the first version reported $1.9\times10^{-3}$, a penalty-weight compromise at which $\lvert V_{cb}\rvert=0.124$; see the review.)*
3. **A universal E_g angle δ\* = 2/9 is excluded for all-positive down amplitudes** by the Schur–Horn theorem (exact criterion): the down sector admits only $\delta\le0.180$.
4. **With the lightest down amplitude negative ($-\sqrt{m_d}$) the route is viable** — exact Koide in both sectors, all four CKM moduli and $J$, at $\chi^2=0.119$ for five observables — **for every E_g angle pair tested inside a band $-0.05\lesssim\delta_D-\delta_U\lesssim0.1$**, including universal δ\*, Żenczykowski's $(2/27, 4/27)$ and the $(2/27, 1/9)$ coincidence candidate. Off the band the route fails even inside both Schur–Horn windows (e.g. $(0.24, 0.01)$: minimum violation $2\times10^{-2}$). $\chi^2=0.119$ is exactly the floor for the best unitary matrix on these five inputs; that floor is the tension inside a *mixed* CKM input set (global-fit $\lvert V_{us}\rvert$ and $J$, direct $\lvert V_{cb}\rvert,\lvert V_{ub}\rvert,\lvert V_{td}\rvert$), and it is about 0 for a pure global-fit set. So in this form the route reproduces the CKM as well as any unitary matrix can: it **predicts no CKM observable**, and its only output is a correlation between the two sector angles.
5. **CP violation needs the $T_{1g}$ component (exact).** If both amplitude matrices are real symmetric (E_g + $T_{2g}$ only), the CKM is real and $J=0$ identically.

## Physics

**The fork's hypothesis.** In F78 the mass is the square of an amplitude. Promote that amplitude to a Hermitian matrix on the generation triplet, $M_f=S_f^2$, with eigenvalues $\lambda_{f,i}=\pm\sqrt{m_{f,i}}$ and $S_f=U_f\,\mathrm{diag}(\lambda_f)\,U_f^\dagger$. The CKM is $V=U_U^\dagger U_D$. $T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g}$ covers all nine entries: A₁g + E_g is the diagonal, $T_{2g}$ the real symmetric off-diagonals, $T_{1g}$ the antisymmetric ones (imaginary in a Hermitian $S$). Route 1 then says: the **diagonal** (the pseudo-mass amplitudes) is exact Koide at some E_g angle, $S_{aa}=\mu_f[1+\sqrt2\cos(\delta_f+2\pi a/3)]$, with $3\mu_f=\operatorname{tr}S_f=\sum_i\lambda_{f,i}$ fixed.

**P1 — the trace identity (exact).** For Hermitian $S$, $\operatorname{tr}S^2=\sum_a S_{aa}^2+2\sum_{a<b}\lvert S_{ab}\rvert^2$ and $\operatorname{tr}S^2=\sum m$. Dividing by $(\operatorname{tr}S)^2$:

$$Q_\text{phys}=Q_\text{pseudo}+\frac{\lVert S_\text{off}\rVert_F^2}{(\operatorname{tr}S)^2}.$$

Mixing can only *raise* Q above the pseudo value, which is the right direction for quarks. With $Q_\text{pseudo}=2/3$ the needed off-diagonal weight is $\sqrt{Q_\text{phys}-2/3}$ — no freedom.

**P2 — how big it is.**

| Sector | Scheme | $Q_\text{phys}$ | $\lVert S_\text{off}\rVert/\operatorname{tr}S$ | relative to E_g amplitude |
|---|---|---|---|---|
| up | mixed (PDG 2025) | 0.849 | 0.427 | 0.739 |
| down, all positive | mixed | 0.731 | 0.254 | 0.440 |
| down, $-\sqrt{m_d}$ | mixed | 0.822 | 0.394 | 0.682 |
| up | $M_Z$ | 0.888 | 0.470 | 0.814 |
| down, $-\sqrt{m_d}$ | $M_Z$ | 0.833 | 0.408 | 0.707 |

(The E_g part of $S$ has Frobenius norm $\sqrt3\,\mu$, so "relative to E_g" is the second-to-last column times $\sqrt3$.) The quark sectors need a $T_{2g}$/$T_{1g}$ condensate 70–80% as large as their E_g condensate, while the charged leptons need none: $Q_\text{lep}=0.6666645$ at pole masses is at or below 2/3, so $\lVert S_\text{off}\rVert=0$. With $-\sqrt{m_d}$ the up and down requirements come within 8% of each other, which a colour-universal source could in principle supply. That is an observation, not a derivation.

**P3 — which E_g angles are allowed (Schur–Horn).** A Hermitian matrix with eigenvalues $\lambda$ and diagonal $d$ exists if and only if $d$ is majorised by $\lambda$ (Schur–Horn theorem). Scanning δ over one fundamental cell $[0,\pi/3]$ of the Koide shape's relabelling symmetry (mixed scheme):

| Sector | Admissible δ | δ\* = 2/9 = 0.2222 |
|---|---|---|
| up, all positive | $[0,\,0.252]$ | allowed |
| down, all positive | $[0,\,0.180]$ | **excluded** |
| down, $-\sqrt{m_d}$ | $[0,\,0.356]$ | allowed |

At $M_Z$ the windows are $[0,0.254]$, $[0,0.185]$ and $[0,0.349]$. So **the lepton angle cannot also be the down-quark pseudo-mass angle unless the lightest down amplitude is negative.**

**P4 — the joint problem (numerical).** The two sectors share a basis, so $U_U$ and $U_D$ are not independent: the CKM ties them. Unknowns: $U_U$, $U_D$ (three angles and a phase each, since the diagonal depends only on $\lvert U\rvert^2$), two relative phases, and the two E_g angles (12 real). Constraints: exact Koide diagonals (2 + 2) and the CKM (four moduli + $J$). The fork solves this with a hand-written Levenberg–Marquardt, 24 random starts. A scipy `least_squares` prototype in scratch agreed to three digits.

- **P4a, all positive:** the smallest Koide violation among starts that hold the CKM at $\chi^2\le1$ is $2.08\times10^{-2}$ of $\operatorname{tr}S$ (mixed) and $2.29\times10^{-2}$ ($M_Z$), at Koide penalty weight $10^2$. Stiffening the penalty to $10^4$ (the first version) drives the reported residual to $1.9\times10^{-3}$, but only by giving up the CKM ($\lvert V_{cb}\rvert=0.124$, $\chi^2\approx7600$); the third control now checks that P4a refuses that compromise. Drop the CKM from the problem (control `ckm_weight=0`) and exact solutions appear at once — but with $\lvert V_{us}\rvert\approx0.54$, $\lvert V_{cb}\rvert\approx0.40$. The obstruction is geometric: the Koide shape caps the largest diagonal at about $0.80\operatorname{tr}S$ for small δ, so the up sector must leak about 13% of the top amplitude off its axis (top carries 0.918 of $\sum\lambda$) and the down sector only about 5% of the bottom's (0.845). A shared basis with $\lvert V_{cb}\rvert=0.041$ cannot absorb that difference.
- **P4b / P7, $-\sqrt{m_d}$:** exact Koide in both sectors at $\chi^2=0.119$ for every pair tested: $(0.05,0.05)$, universal $(2/9,2/9)$, $(2/27,4/27)$, $(2/27,1/9)$ and $(0.2,0.3)$. A direct fit of a unitary matrix to the same five inputs (`unitary_floor`, computed in the leg) also gives 0.1186, so the route adds nothing to the CKM. It is **not** true that every admissible pair fits: the review's grid found solutions only in a diagonal band $-0.05\lesssim\delta_D-\delta_U\lesssim0.1$. Pairs such as $(0.24,0.01)$, $(0.25,0.25)$ and $(0.10,0.40)$ fail, although they sit inside both Schur–Horn windows. P7 now asserts the off-band failure at $(0.24,0.01)$. δ\* = 2/9 on the diagonal is viable, near the band's upper edge.
- **Fine tuning (scratch, not asserted by a leg):** in the fitted solutions each sector rotates a lot (roughly 13–15% of the heaviest state's weight off-axis, and up to about 35° between the two light states), and the small CKM comes from the near-cancellation of the two sector rotations. Nothing in the fork explains that alignment.

**P6 — CP violation needs $T_{1g}$ (exact).** Real symmetric $S_U$, $S_D$ have real orthogonal $U_U$, $U_D$, so $V$ is real and $J=\operatorname{Im}(V_{11}V_{22}V_{12}^*V_{21}^*)=0$ identically. The measured $J=3.12\times10^{-5}$ therefore requires the $T_{1g}$ (antisymmetric, imaginary) channel, which is T-odd.

## What breaks, and what it means for the model

| What route 1 needs | Status in the model | Verdict |
|---|---|---|
| Exact Koide pseudo-diagonal (A₁g + E_g) for quarks | Same structure as the leptons | fine |
| $T_{2g}$/$T_{1g}$ off-diagonals at 70–80% of the E_g amplitude, in quark sectors only | No source; the leptons must have exactly none | **unexplained** — needs a quark-only (colour-sourced?) off-diagonal condensate |
| All-positive amplitudes (lepton-like) | Natural | **excluded** (P4a) |
| A negative lightest down amplitude | Not derived; Rivero-type sign choice | **input** |
| A principle fixing $\delta_U$, $\delta_D$ | None; any pair in the band $-0.05\lesssim\delta_D-\delta_U\lesssim0.1$ fits | **non-predictive for CKM; angles correlated** (P7) |
| A T-odd $T_{1g}$ condensate for CP violation | None | **new structure required** (P6) |
| Near-alignment of two large sector rotations | None | **fine-tuned** |

Route 1 is therefore **not a derivation of the quark hierarchy or the CKM**. In the only form that survives, it reparametrises six masses and four CKM parameters into sector angles and off-diagonal textures with at least as many free numbers. What it *does* contribute is two exact, model-independent constraints that any future quark-sector mechanism in this model must meet: the off-diagonal weight is fixed by $Q_\text{phys}$ (P1), and CP violation requires a $T_{1g}$ component (P6). It also closes one door: the leptons' δ\* cannot be the down-quark pseudo-angle with lepton-like signs (P3).

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| $Q_\text{phys}-Q_\text{pseudo}=\lVert S_\text{off}\rVert_F^2/(\operatorname{tr}S)^2$ | exact (sympy) | 0 |
| Real symmetric $S_U$, $S_D$ ⇒ $J=0$ | exact (sympy) | 0 |
| Required off-diagonal weights (table) | quantitative (PDG 2025 / Antusch et al. masses) | mass errors ≈ 1–3% on light quarks |
| Schur–Horn δ windows | exact criterion, quantitative input | δ grid step $10^{-3}$ |
| All-positive joint failure, min Koide violation $2.1\times10^{-2}$ at CKM $\chi^2\le1$ | numerical search (24 starts; blind re-derivation agrees, $\approx2\times10^{-2}$) | not a proof |
| Signed route fits at the unitary floor $\chi^2=0.119$ | numerical | — |

## Tests

`casim test --id F404-koide-pseudomass-fork` — 8/8 legs PASS (P1, P2, P3, P4a, P4b, P5, P6, P7 — P5 is the lepton check), about 18 s.
Controls (`casim test --control --id F404-koide-pseudomass-fork`), both CONTROL:
- `down_signs=+++` → P3, P4b, P7 red (the negative $\sqrt{m_d}$ is the whole of the route's viability).
- `ckm_weight=0.0` → P4a red (the all-positive failure is a CKM incompatibility, not a per-sector one).
- `koide_weight=10000` → P4a red (an over-stiff penalty abandons the CKM; P4a refuses to report the compromise).

The scheme was also run at `scheme=MZ` by hand: all legs pass with the $M_Z$ numbers quoted above.

## Scope and limits

- **"Pseudo-mass" here means the diagonal of the amplitude matrix $S$**, the object F78 makes natural. Gérard–Goffinet–Herquet and Żenczykowski define pseudo-masses in a specific weak basis of the mass matrix; the fork tests the model's version, not a literal reproduction of theirs.
- **P4a is a numerical search**, not a proof. The geometric argument in P4 explains it but was not turned into a bound.
- **Non-Hermitian $S$ was not tested.** A general complex amplitude matrix frees the overall scale (Sing–Thompson replaces Schur–Horn), which makes the route even less predictive.
- **Sign patterns tested:** all positive, $-\sqrt{m_d}$, and $(-\sqrt{m_u},-\sqrt{m_d})$ (one scratch run looked viable; not asserted by any leg, treat as untested). Flipping a middle or heavy amplitude was scanned only for Schur–Horn admissibility.

## Status

Fork, `fork_live`: viable in the signed form, rejected as an explanation. **Claim:** CL316 records the non-predictivity verdict and the two exact constraints. Next steps a quark-sector mechanism would need: (i) a dynamical source for a quark-only $T_{2g}$/$T_{1g}$ condensate at the size P2 fixes; (ii) a principle that fixes δ_U and δ_D; (iii) a reason for the negative $\sqrt{m_d}$.
