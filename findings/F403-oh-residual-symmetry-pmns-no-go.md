# F403 — No $O_h$ residual symmetry fixes PMNS in the cube-axis charged-lepton frame; the [111]-trimaximal frame admits TM1

**Date:** 2026-09-24 - 11:20
**Status:** Candidate finding — 15/15 checks PASS (group/eigenspace/moduli/gCP/subgroup-lattice legs exact in sympy; data legs quantitative against NuFIT 6.0 3σ, so the record's class is `quantitative`). Two declared controls, each red exactly where declared. **A no-go, conditional on an exactly cube-diagonal charged-lepton frame, plus one conditional opening.**
**Checked:** 2026-09-24 - 12:40 — cold blind re-derivation + adversarial referee, **CONFIRMED-NARROWER**; all ten referee defects fixed in place (see `docs/reviews/F403-review-2026-09-24.md`).
**Reviewed:** 2026-09-24 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F403-review-2026-09-24.md))
**Module:** `casim.engine.particles.derive_oh_residual_pmns` (new)
**Test record:** `F403-oh-residual-pmns` (tier gate, entry `check_oh_residual_pmns`), driver `tests/findings/test_F403_oh_residual_pmns.py` → `test-results/F403_oh_residual_pmns.json`
**Claim:** CL315 (`docs/claims/CL315-no-oh-residual-fixes-pmns-in-cube-frame.md`), rolls up to CL223
**Cross-references:** [[F254]] (the $T_{2g}$ amplitudes are free — this finding says no $O_h$ selection can fix them), [[F236]] (E_g-only see-saw gives PMNS = 1), [[F353]] (δ_CP inherits the no-go), [[F93]] / [[F76]] (the cube-axis E_g frame), [[F75]] (generations = $T_{1u}$), research report `reports/Quark neutrino hierarchy lattice fit.md` (2026-09-24), which proposed this check.

---

## Summary

In the "direct" flavour-symmetry approach, lepton mixing comes from a mismatch between the residual symmetry kept by the charged-lepton mass matrix and the one kept by the neutrino mass matrix. For the model, the candidate residuals are subgroups of the lattice point group $O_h$ acting on the $T_{1u}$ generation triplet. The model's adopted charged-lepton frame is the cube axes, because the E_g condensate is diagonal there (F76/F93). This finding enumerates all 23 non-identity rotations of $O$ exactly and shows that, **if the charged-lepton frame is exactly the cube axes, no residual unitary symmetry in the neutrino sector is compatible with the measured PMNS matrix**. Each one pins a PMNS column to a cube axis or a face diagonal (both contain a zero, but no PMNS element anywhere in the 3σ box is below $0.0203$), or to the trimaximal matrix (which needs $\sin^2\theta_{13}=1/3$, far above the 3σ upper edge $0.0239$). The same Koide spectrum written as a [111]-circulant — the *trimaximal* frame — behaves differently: the three face-diagonal $C_2'$ rotations then fix the TM1 column $(2/3,1/6,1/6)$, giving $\sin^2\theta_{12}=1-2/(3\cos^2\theta_{13})\in[0.3170,0.3195]$ and $\delta\in[252.4°,293.4°]$, inside current data. Among generalised-CP residuals in the cube frame, the $y\leftrightarrow z$ mirror gives μ–τ reflection ($\theta_{23}=45°$, $\delta=\pm90°$), which is still viable; the diagonal ones force $J=0$.

## Physics

**Setting.** In $T_{1u}$ the 48 elements of $O_h$ are the signed $3\times3$ permutation matrices. A mass term is a bilinear, so $g$ and $-g$ act identically ($(-g)^TM(-g)=g^TMg$, leg G2). The effective group is therefore the rotation group $O\cong S_4$: 24 elements in classes $E + 3C_2 + 6C_2' + 8C_3 + 6C_4$ (leg G1).

**The lemma.** A sharper form (found by the blind re-derivation): writing $M=U^*DU^\dagger$ and $h=U^\dagger RU$, invariance gives $h^TDh=D$ with $h$ unitary, and for distinct masses this forces $h=\mathrm{diag}(\pm1)$. So a residual element must act as $\pm1$ on every mass eigenstate, hence be an **involution**, and any residual group is at most $Z_2\times Z_2$; $C_3$ and $C_4$ are excluded outright. The module uses the weaker, equivalent-for-columns form: if $R^TMR=M$ for a real orthogonal $R$, then $H=M^\dagger M$ satisfies $R^THR=H$, so $H$ commutes with $R$. The light neutrino masses are non-degenerate ($\Delta m^2_{21},\Delta m^2_{31}\ne0$), so each eigenline of $H$ is an eigenline of $R$. **Every 1-dimensional eigenspace of $R$ is therefore a column of $U_\nu$**, up to a phase. For Dirac neutrinos the same argument runs with $H=MM^\dagger$. A residual *subgroup* imposes the constraint of each of its elements, so the element-by-element verdict covers every subgroup.

**Cube-axis frame ($U_\ell=\mathbb 1$, so $U_\text{PMNS}=U_\nu$).** The fixed columns, as exact squared moduli (leg E1):

| Class | Fixed eigenlines | PMNS column(s), $\lvert U\rvert^2$ | Verdict |
|---|---|---|---|
| $C_2$ (3) | axis $e_x$, $e_y$, $e_z$ | $(1,0,0)$ and permutations | two zeros — excluded |
| $C_2'$ (6) | face diagonal $(0,1,\pm1)/\sqrt2$ etc. | $(0,\tfrac12,\tfrac12)$ and permutations | one zero — excluded |
| $C_3$ (8) | $(1,1,1)/\sqrt3$, $(1,\omega,\omega^2)/\sqrt3$, … | every $\lvert U\rvert^2=\tfrac13$ | needs $\sin^2\theta_{13}=\tfrac13$ — excluded |
| $C_4$ (6) | axis + $(1,\pm i,0)/\sqrt2$ | $(1,0,0)$, $(\tfrac12,\tfrac12,0)$ | zeros — excluded |

The data comparison (leg N1) takes every row assignment (which cube axis is $e,\mu,\tau$) and every column label (which mass eigenstate). The smallest PMNS element anywhere in the NuFIT 6.0 NO 3σ box is $\lvert U_{e3}\rvert^2=\sin^2(8.19°)=0.0203>0$ (leg N2, a grid scan over the whole box; the next-smallest element is about $0.056$). That kills every column with a zero; the all-$\tfrac13$ matrix is killed by the upper edge $\sin^2\theta_{13}\le0.0239$. So none of the four classes survives. As a second, independent reason for Majorana neutrinos, a symmetric $M$ invariant under $C_3$ or $C_4$ has a degenerate pair of eigenvalues (leg E2, exact linear solve).

**Trimaximal frame ($U_\ell=F$, $F_{ak}=\omega^{ak}/\sqrt3$).** This is the other way to write the same Koide spectrum: a Hermitian circulant with $\lvert b\rvert/a=1/\sqrt2$ and $\arg b=2/9$, i.e. a [111] trigonal ($T_{2g}$) plus axial ($T_{1g}$) distortion. Here $U_\text{PMNS}=F^\dagger U_\nu$, and the table changes (leg B1, exact):

| Class | PMNS column $\lvert U\rvert^2$ | NuFIT 6.0 3σ | JUNO-inclusive 6.1 (approx. 3σ) |
|---|---|---|---|
| $C_2'$ with like-sign diagonal (3) | $(\tfrac23,\tfrac16,\tfrac16)$ — **TM1** | viable | viable |
| $C_2'$ with unlike-sign diagonal (3) | $(0,\tfrac12,\tfrac12)$ | excluded | excluded |
| $C_2$ (3) | $(\tfrac13,\tfrac13,\tfrac13)$ — TM2 | viable ($0.341<0.345$) | excluded |
| $C_3$, $C_4$ | full matrices with zeros or degeneracies | excluded | excluded |

TM1 also fixes a $(\theta_{23},\delta)$ correlation: $\lvert U_{\mu1}\rvert=\lvert U_{\tau1}\rvert$ gives $\cos\delta=-\dfrac{(s_{12}^2-c_{12}^2s_{13}^2)\cos2\theta_{23}}{2s_{12}c_{12}s_{13}\sin2\theta_{23}}$ (derived symbolically in leg B4), and over the 3σ box this confines $\delta$ to $[252.4°,\,293.4°]$. This is the sharper falsifier. The TM1 sum rule is $\sin^2\theta_{12}=1-\dfrac{2}{3\cos^2\theta_{13}}$. Across the θ13 3σ band this gives $[0.31702,\,0.31952]$ (leg B3). NuFIT 6.1 + JUNO has $0.3096^{+0.0057}_{-0.0073}$, so TM1 sits about $1.3$–$1.7\sigma$ high. TM2 gives $0.3409$ at the θ13 best fit: inside NuFIT 6.0's published 3σ range, but about 5.5σ from the JUNO value. The JUNO 3σ band used here is a Gaussian extrapolation of the published 1σ errors, not a published range, and is labelled that way in the module.

**Generalised CP (cube frame, leg C1).** A CP residual $X\in O_h$ requires $XX^*=1$; since $X$ is real, $X^2=1$, so $X$ is an involution. It imposes $U^*=XUK$ with $K$ a diagonal phase matrix.
- **Diagonal $X$** (identity, axis $C_2$): the rephasing invariant $Q=U_{e1}U_{\mu2}U_{e2}^*U_{\mu1}^*$ satisfies $Q^*=Q$ exactly, so $J=0$ and $\delta\in\{0,\pi\}$. This is viable, since 180° is inside the NO range, but it predicts nothing about the angles.
- **$y\leftrightarrow z$ mirror** (face-diagonal $C_2'$, with $e$ on the fixed axis): $\lvert U_{\mu i}\rvert=\lvert U_{\tau i}\rvert$. Column 3 forces $\theta_{23}=\pi/4$. At $\theta_{23}=\pi/4$, $\lvert U_{\mu1}\rvert^2-\lvert U_{\tau1}\rvert^2=\sin2\theta_{12}\sin\theta_{13}\cos\delta$ (exact), so $\delta=\pm\pi/2$. This is Harrison–Scott μ–τ reflection, and it is inside the 3σ box ($\sin^2\theta_{23}=\tfrac12$, $\delta=270°$).
- **Mirrors that swap $e$ with $\mu$ or $\tau$:** these need $\lvert U_{e3}\rvert=\lvert U_{\mu3}\rvert$ or $\lvert U_{\tau3}\rvert$, but $\max\lvert U_{e3}\rvert^2=0.0239<0.405\le\min\lvert U_{\mu3,\tau3}\rvert^2$. Excluded.

## What this means for the model

1. **F254 becomes a theorem about $O_h$, given an exactly cube-diagonal charged-lepton frame.** In that frame no unitary residual of the lattice point group is viable, and no $O_h$ residual of any kind (unitary or generalised CP) fixes θ12 or θ13. Whatever sets them is dynamics (the "dynamical $T_{2g}$ gap" of ledger row D1), a structure outside $O_h$, or a charged-lepton correction to the cube frame. The last is a real escape route: a charged-lepton rotation of order $\theta_{13}\approx0.15$ rad is exactly the size that fills the zeros, which is the standard "TBM plus charged-lepton correction" rescue. So the no-go is conditional on $U_\ell=\mathbb 1$ exactly.
2. **The only $O_h$ prediction left in the E_g frame is μ–τ reflection**, from a CP-type residual: $\theta_{23}=45°$ and $\delta=\pm90°$. It fixes neither θ12 nor θ13. The model would have to give ν_R's Majorana texture a $y\leftrightarrow z$ CP symmetry. That is compatible with F343's observation that ν_R is a total gauge singlet, but nothing in the model derives it yet.
3. **The trimaximal reading opens TM1.** That reading is a fork of key decision 7 (it drops F93's "E_g is the unique non-mixing splitter"), so this finding does not adopt it. It does settle the group-theory side: if the charged leptons are [111]-trimaximal, an $O$ face-diagonal $C_2'$ in the neutrino sector gives TM1, whose $\sin^2\theta_{12}\approx0.318$ JUNO can test within a few years. The energetic side — whether the condensate prefers the E_g-diagonal or the trigonal-circulant form in the F118 Landau functional — is not addressed here.

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| $O_h$ order 48, $O$ classes $1+3+6+8+6$, sign-blindness on bilinears | exact (sympy) | 0 |
| Fixed PMNS columns per class, cube and trimaximal frames (tables above) | exact (sympy rationals) | 0 |
| $C_3$/$C_4$-invariant symmetric $M$ has a degenerate pair | exact (linear solve) | 0 |
| gCP: diagonal $X\Rightarrow J=0$; $y\leftrightarrow z$ mirror $\Rightarrow\theta_{23}=\pi/4$, $\lvert U_{\mu1}\rvert^2-\lvert U_{\tau1}\rvert^2=\sin2\theta_{12}\sin\theta_{13}\cos\delta$ | exact (sympy) | 0 |
| TM1 sum rule $\sin^2\theta_{12}=1-2/(3\cos^2\theta_{13})$ | exact | 0 |
| No-go / viability against NuFIT 6.0 3σ | quantitative (data box, grid over θ13, θ23; the $\cos\delta$ interval is read from the δ window) | grid step 1/120 of the $s_{23}^2$ range; tolerance $10^{-4}$ on $\lvert U_{\mu i}\rvert^2$, about 200× below the smallest cube-frame gap |
| TM1 correlation $\cos\delta$ closed form | exact (sympy solve) | 0 |
| TM1 $\delta\in[252.4°,293.4°]$ over the box | quantitative | grid |

## Tests

`casim test --id F403-oh-residual-pmns` — 15/15 legs PASS (G1, G2, E1, E2, N1, N2, B1, B2, B3, B4, S1, S2, S3, S4, C1), about 11 s.
Controls (`casim test --control --id F403-oh-residual-pmns`), both CONTROL:
- `frame=trimaximal` → exactly N1 and S2 red (TM1 and TM2 become viable).
- `frame=face_diagonal` → green (the face-diagonal frame is also a no-go, leg S4).
- `theta13_lo_deg=0` → N1, N2, B2, B4, S2, S3, S4 red (single-zero columns become viable, and so do TBM-type three-column residuals; the TM1 δ correlation is undefined; the no-go rests on θ13 ≠ 0).
- Referee sweeps also ran `theta13_lo_deg=1` and `=5` (green, correctly: any θ13 > 0 still excludes zeros) and `s12sq_band=nufit61_juno_approx` (green; TM2 survivors drop 3 → 0).

## Addendum (2026-09-24 - 14:16) — the full subgroup lattice, and the BCC frame

**Subgroups, enumerated rather than argued (legs S1–S3).** The module now builds every subgroup of $O_h$ by closure in sympy: **98** subgroups, **30** of them inside $O$. For each subgroup $H$ it solves $g^TMg=M$ for all $g\in H$ exactly, and asks whether the invariant family has a characteristic-polynomial discriminant that is not identically zero, i.e. whether a non-degenerate mass spectrum is possible. The answer is exact: **$H$ is admissible iff it is an elementary abelian 2-group** (every element an involution). That gives **49** admissible subgroups, of order 1, 2, 4 and 8. Order 8 is $Z_2\times Z_2\times\{\pm\mathbb 1\}$, which acts on a bilinear as $Z_2\times Z_2$. This checks the lemma in §Physics subgroup by subgroup. Every column an admissible subgroup forces is its joint 1-dim eigenspace, and each one is already a 1-dim eigenline of one of its elements, so the element-wise verdict really does cover the lattice.
- **Cube frame (S2):** 47 non-trivial admissible subgroups; **none viable.**
- **Trimaximal frame (S3):** 18 survivors, all of order 2 or 4 ($\langle C_2'\rangle$ or $\langle C_2\rangle$, possibly times $\pm\mathbb 1$), each fixing exactly **one** column, TM1 $(\tfrac23,\tfrac16,\tfrac16)$ or TM2 $(\tfrac13,\tfrac13,\tfrac13)$.
- **In neither frame does a three-column ($Z_2\times Z_2$) residual survive.** Full residual determination of PMNS by $O_h$ is dead in every frame tested. In the trimaximal frame the $Z_2\times Z_2$ residual gives TBM, which becomes viable only if $\theta_{13}=0$; that is part of what the θ13 control turns red.

**The BCC frame (S4).** BCC has the same point group $O_h$, and the generations are the same $T_{1u}$. So S1 carries over unchanged, and the only freedom a BCC reading adds is the choice of charged-lepton frame. The nearest-neighbour directions of BCC are the four body diagonals $[111]$, but these are not mutually orthogonal (Gram off-diagonal $-\tfrac13$, exact). So there is **no orthonormal "BCC nearest-neighbour frame"**. The orthonormal frames $O_h$ singles out are three:

| Frame | Distinguished by | Verdict |
|---|---|---|
| cube axes $e_x,e_y,e_z$ (BCC next-nearest neighbours) | $C_4$/$C_2$ eigenbasis; the E_g reading | no-go |
| face diagonals $(1,\pm1,0)/\sqrt2,\ (0,0,1)$ | $C_2'$ eigenbasis | **no-go** — forced columns are $(1,0,0)$, $(0,\tfrac12,\tfrac12)$ (zeros) or $(\tfrac12,\tfrac14,\tfrac14)$, which would need $\sin^2\theta_{12}\approx\tfrac14$ (below the 0.275 edge) or $\tfrac34$ |
| $C_3[111]$ eigenbasis $(1,\omega^k,\omega^{2k})/\sqrt3$ | the [111] body diagonal's $Z_3$ | trimaximal: TM1/TM2 open |

So the BCC question resolves as follows. Its [111] axes affect flavour only through the complex $C_3$ eigenbasis, which is exactly the trimaximal frame already in this finding. No real BCC frame escapes the no-go.

## Scope and limits

- **Residuals inside $O_h$ only.** A neutrino residual from a larger group (for example $\Delta(6n^2)$, or $S_4$ acting on a *different* 3-dimensional embedding) is not covered.
- **The trimaximal frame's gCP residuals were not enumerated.**
- **The cube-frame statement assumes the charged-lepton eigenvectors are exactly the cube axes**, as in the E_g reading (F93: E_g splits the axes without mixing them). A charged-lepton rotation of size $\epsilon$ moves the zeros to $O(\epsilon)$, and $\epsilon\approx\theta_{13}\approx0.15$ rad evades the no-go entirely. Nothing in the model currently produces such a rotation for the charged leptons (their exact Koide shape leaves no room for off-diagonal amplitude; see F404), but the no-go is stated as conditional on it.
- **Prior art.** The classification is the standard $S_4$ residual-symmetry analysis (Lam, arXiv:0809.1185; Hernandez–Smirnov, arXiv:1204.0445 and arXiv:1212.2149; King–Luhn, arXiv:1301.1340) and $S_4$ with generalised CP giving μ–τ reflection (Feruglio–Hagedorn–Ziegler, arXiv:1211.5560), applied to the model's specific charged-lepton frame. The novelty is the application — that the model's E_g frame (and the face-diagonal frame, S4) are frames in which $O_h$ can fix nothing — not the group theory.
- **Test legs that cannot fail.** G2 and the $J=0$ identity in C1 are algebraic identities kept as sanity checks. Their failure modes are not controlled; the controls sit on N1, N2, B2 and B4.
- **Data:** NuFIT 6.0 NO with SK atmospheric data, 3σ (arXiv:2410.05380). For inverted ordering the smallest element is still $\lvert U_{e3}\rvert$ with a similar θ13, so the zero-entry exclusion carries over; only NO was run.

## Status

Candidate. Open next steps: (i) decide between the E_g and trimaximal readings energetically (F118 Landau functional extended by $T_{2g}[111]$ and $T_{1g}[111]$); (ii) if the E_g frame stands, test whether a $y\leftrightarrow z$ CP symmetry of $M_R$ follows from anything (F343/F341); (iii) re-fit F236 against NuFIT 6.x (its target was NuFIT 5.2, θ23 = 49°).
