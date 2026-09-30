# Residual symmetry decides what the lattice can fit

*2026-09-24 - 00:00 — synthesis of four research notes (`research_notes/Quark neutrino hierarchy lattice fit/`). Internal status labels follow `model_internal_state.md`. **Exact** means algebraic or group-theoretic. **Hypothesis** means stated but not derived. **Input** means fitted or free. **No-go** means a proven negative. **Coincidence candidate** means a numerical match with no mechanism behind it. "Computed here" marks arithmetic done for this report or its notes, not quoted from a source.*

Of the mechanisms in the literature, the one that fits the CA model best is the **residual-symmetry, or "vacuum misalignment", family** of S4 ≅ O flavour models. The model's O_h structure already is that family in lattice form:

- T1u is the S4 triplet.
- The E_g second-shell condensate is the S4 "doublet flavon".
- T2g and T1g are the triplet flavons.

T1u⊗T1u = A1g⊕E_g⊕T1g⊕T2g matches S4's 3⊗3 = 1⊕2⊕3⊕3′ term by term ([Ishimori et al., arXiv:1003.3552](https://arxiv.org/abs/1003.3552); [King–Luhn, arXiv:1301.1340](https://arxiv.org/abs/1301.1340)). That match has consequences. For neutrinos, residual-symmetry analysis gives a hard fork. If the charged leptons are diagonal on the cube axes, as the model currently assumes, **no O_h residual symmetry on the neutrino side can give a viable PMNS**. Every such residual either leaves a degenerate pair or fixes a mixing column that contains a zero. So PMNS has two possible sources. One is the D_2h-breaking T2g amplitudes, which F254 proved are free. The other is reinterpreting the charged-lepton condensate as a trigonal [111] circulant. That reinterpretation opens the one surviving S4 descendant, TM1, which predicts sin²θ12 = 0.318, 1.0–1.5σ above JUNO. For quarks, the best-fitting route is the **Gérard–Goffinet–Herquet/Żenczykowski "pseudo-mass" scheme**: Koide k = 1 holds before mixing, and the off-Koide quark spectra and CKM come from the same small off-diagonal (T2g) distortion. This keeps the model's exact outputs (Q = 2/3, a weight-valued angle) and puts the new physics in the channel F93 and F236 already name as the only one that can mix. Two more routes also fit naturally: sector-dependent E_g angles, and a colour- or charge-dressed E_g amplitude. Their supporting numbers are coincidence candidates, not evidence. Froggatt–Nielsen, warped/clockwork geometry, type-II/radiative neutrino masses, and minimal top condensation fit badly or are already excluded. They either need an elementary Higgs doublet, which decision 3 forbids, or they were excluded by the model's own findings.

## The model offers exact slots but no quark or mixing outputs

The model's flavour sector is lopsided. For charged leptons, three pieces are derived:

- **E_g as the unique non-mixing splitter** (F93 O1, exact);
- **the D_2h stabilizer** (F93 O3, exact);
- **Koide Q = 2/3 as 45° equipartition** (F92, exact, with the Fock √2 as its one new input).

The shape angle **δ* = 2/9 rad is an adopted principle** (key decision 7; F253, F255 and F256 close every derivation route). λ₆ = 0.243 is an **output** (F234), and the overall scale is an **input**: τ-anchored, FIT N=1, reducing to d₁ (F121, F233). With these, the ratios m_μ/m_e and m_τ/m_e come out to ≤0.007% with zero shape parameters (F175) ([model_internal_state.md](../research_notes/Quark%20neutrino%20hierarchy%20lattice%20fit/model_internal_state.md)).

Quarks have none of this. The six current masses are **per-species inputs** (OPEN×6). The CKM matrix is **declared out of scope** (CL017, ABSENT×4). F346 and F347 are leaning no-gos: the lepton circulant does not transplant to (u,c,t), (d,s,b), (u,d,s) or (c,b,t). Neutrinos sit in between:

- **F47** supplies a Higgs-free anti-linear Majorana step. F341 argues hypercharge closure forces it (contingent).
- **F236** shows the three-generation see-saw with E_g texture on both M_D and M_R is diagonal on the cube axes, so **PMNS = 1 exactly (no-go)**.
- **F254** proves the three T2g amplitudes that could fix this are **permanently free**. They carry three inequivalent 1-d irreps of D_2h.
- **F353** extends the same freedom to δ_CP.
- **F343** shows **M_R is free**.

A caution on labels: the "MACHINE×2" grade for light-ν mass ratios in the completeness table covers the see-saw algebra, not a parameter-free Δm² prediction. F236 uses input Dirac masses and free δ_D and δ_ν.

The constraint that matters most for importing literature mechanisms is decision 3, **hypercharge on U(x) with no Higgs**. The model has "no Yukawa mechanism anywhere". Each species' mass is a bare parameter in the F27 chiral step (F41; notebook cross-check). A literature mechanism therefore enters only if it can be rewritten as a **lattice-geometric condensate** (E_g, T2g, T1g on the second shell) or a **pair condensate** (the F78 bilinear m = y²). Mechanisms that need a doublet VEV to carry flavour have no such rewrite unless the doublet is made composite. That rules out Froggatt–Nielsen flavons coupled to H, type-II triplets, and Zee or scotogenic scalars ([Xing, arXiv:1909.09610](https://arxiv.org/abs/1909.09610)). One structural fact helps for neutrinos: **a right-handed Majorana mass is a gauge singlet and needs no electroweak breaking**, so type-I see-saw is the one standard neutrino mechanism that is natively Higgs-free ([King–Luhn, arXiv:1301.1340](https://arxiv.org/abs/1301.1340)).

## Current data sharpen targets and expose scheme dependence

The quark numbers come from **PDG 2025**: m_u = 2.16 ± 0.07, m_d = 4.70 ± 0.07 and m_s = 93.5 ± 0.8 MeV (MS-bar, 2 GeV); m_c(m_c) = 1.2730 GeV; m_b(m_b) = 4.183 GeV; and a direct (kinematic) top mass of 172.56 ± 0.31 GeV ([PDG quark summary](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf)). The CKM fit gives λ = 0.22501 ± 0.00068, A = 0.826, ρ̄ = 0.159, η̄ = 0.352 and **J = 3.12×10⁻⁵** ([PDG CKM review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf)).

The main surprise concerns the model's quoted Q values. **Q_up = 0.849 and Q_down = 0.731 reproduce Q computed from PDG's mixed-scale summary table** (0.8488 and 0.7313). At a common scale μ = M_Z they become **0.888 and 0.748** (computed here from [Antusch–Hinze–Saad, arXiv:2510.01312](https://arxiv.org/html/2510.01312v1)). Every quark-sector claim about Q or δ therefore has to name its mass scheme. QCD running moves quarks further from Koide as μ rises. Charged-lepton Koide itself holds for pole masses and degrades by about 0.2% at M_Z ([Żenczykowski, arXiv:1301.4143](https://arxiv.org/abs/1301.4143)).

For neutrinos the data have moved since F236 was fitted. **JUNO plus NuFIT 6.1** give sin²θ12 = 0.3096 (+0.0057/−0.0073) and Δm²21 = 7.530×10⁻⁵ eV². Normal ordering is preferred at only about 2.2–2.3σ ([arXiv:2601.09791](https://arxiv.org/html/2601.09791v2)). **NuFIT 6.0's global NO best fit has θ23 = 43.3°, sin²θ13 = 0.02215 and Δm²3ℓ = 2.513×10⁻³ eV²** ([arXiv:2410.05380](https://arxiv.org/pdf/2410.05380)). F236's T2g fit targeted NuFIT 5.2 (θ23 = 49.0°, Δm²21 = 7.42×10⁻⁵), so the preferred θ23 octant it reproduced has since flipped in the headline fit. Cosmology now bounds **Σm_ν < 0.0642 eV** (DESI DR2 + CMB). That sits just above the NO floor of about 0.059 eV, which makes "NO with m₁ ≈ 0" the safest spectrum ([DESI via OSTI](https://www.osti.gov/biblio/3006914)). The cleanest scale-free target is **r = Δm²21/Δm²31 ≈ 0.0300 ± 0.0004** (computed here).

**Where the notes disagree.** The cubic-group note computed its quark fits from quark masses "from memory". Those values match the fetched PDG 2025 numbers, and its δ values (0.0745 and 0.1101) agree with the quark note's. One difference: it labels 172.57 GeV a pole mass, but PDG classes 172.56 GeV as the direct/kinematic mass. The pole mass from cross-sections is 172.4 ± 0.7 GeV. The cubic note also recalled |V_us| = 0.2243, which is the direct value (0.22431). The global-fit λ is 0.22501. Its neutrino inputs (Δm²21 ≈ 7.42×10⁻⁵, Δm²31 ≈ 2.515×10⁻³) are pre-JUNO. I use the fetched NuFIT 6.0/6.1 and JUNO values throughout. Finally, the Koide amplitude is written two ways in the repo, η² = 1/2 (CLAUDE.md, F175) and η = √2 (F346, F347). Both denote Q = 2/3.

## Residual-symmetry mismatch is the best structural fit, and it forces a fork for neutrinos

In the S4 "direct" approach, lepton mixing is the mismatch between two residual subgroups: one left by the charged-lepton flavon, one left by the neutrino flavon. Lam showed S4 is the minimal group for tribimaximal mixing ([arXiv:0809.1185](https://arxiv.org/abs/0809.1185)). Since O ≅ S4 is the cube's rotation group, the cube and its crystal-field language are the natural setting for this approach.

The obstacle is the model's current basis. In the cubic-axis basis the **Z3 = C3[111] Fourier matrix combined with the rhombic Klein group {C2x, C2′[011]} reproduces TBM exactly**. The generic E_g condensate instead leaves the *cubic-axis* D_2h as the charged-lepton residual ([cubic-group note](../research_notes/Quark%20neutrino%20hierarchy%20lattice%20fit/cubic_group_crystal_field.md)). I enumerated all 48 O_h matrices on T1u (computed here). **Every O_h involution fixes a mass eigenvector along a cube axis (1,0,0) or a face diagonal (0,1,±1)/√2.** Each of those makes a PMNS column with a zero entry, but the smallest measured element is |U_e3|² ≈ 0.022, so no column contains a zero. C3 and C4 residuals force a degenerate pair. The consequence goes beyond the notes' statement that TBM is unreachable: **with cube-axis charged leptons, no nontrivial O_h residual symmetry in the neutral sector gives viable mixing.** F254's conclusion, that PMNS lives in free, symmetry-unrelated T2g amplitudes, is then a theorem about O_h itself, not a gap in the model. This enumeration covers ordinary residual symmetries only. Generalised-CP residuals were not examined.

The cubic note offers a way out through a **basis equivalence** (exact, verified numerically there). Rotate the E_g-diagonal Koide matrix at δ = 2/9 by the trimaximal matrix F. The result is a Hermitian circulant a·1 + bP + b*P² with **|b|/a = 1/√2 and arg b = 2/9**. Its real symmetric part is a T2g distortion along [111]; its imaginary antisymmetric part is a T1g axial distortion along [111]; and **tan δ = T1g/T2g**. The Koide spectrum therefore has two lattice realisations with different physics:

- **(a)** an E_g condensate with cubic-axis eigenstates and residual D_2h (the current model);
- **(b)** a trigonal [111] condensate with trimaximal eigenstates and residual C3.

Only (b) lets an O_h Klein subgroup or single C2 on the neutrino side produce TBM or its descendants. TBM itself is now dead: θ13 ≠ 0, and sin²θ12 = 1/3 sits +4.2σ from JUNO. **TM1 survives with sin²θ12 = 0.318, about 1.0–1.5σ high.** TM1 also gives a parameter-free (θ23, δ_CP) correlation. JUNO's projected ±0.003 precision on sin²θ12 can kill it ([Ardakanian, arXiv:2603.21264](https://arxiv.org/html/2603.21264), a single-author preprint whose sum rules are standard; [King, arXiv:1512.07531](https://arxiv.org/pdf/1512.07531)).

Picture (b) is costly. It gives up F93's "E_g is the unique non-mixing splitter", and it gives up the second-shell E_g home that ties δ* to F49's 2/9. Decision 7's "the E_g-plane angle *is* the weight" would survive only as a numerical equality, arg b = 2/9, with no reason for that value. T1g is also T-odd, and a symmetric Majorana matrix cannot carry it. So (b) would reopen a key decision. It is a live fork, not a drop-in fix.

The alternative that keeps decision 7 intact exploits F343's observation that **ν_R is a total gauge singlet**. If the E_g condensate is induced by the strong sector (F170), ν_R may not feel it. In that case M_R could keep a larger residual subgroup than the charged sector. The enumeration above shows that is not enough by itself: the neutral-sector residual has to be *non-O_h* or come from dynamics. This is the precise content of ledger row D1's still-unrun "dynamical T2g gap computation". The littlest-see-saw (CSD(3)) Dirac alignments (0,1,1) and (1,3,1) point in the same direction ([King, arXiv:1512.07531](https://arxiv.org/pdf/1512.07531)). Their first column is a cube face diagonal. Their second is not a cube symmetry axis, so an O_h lattice would need an extra dynamical input to produce it.

## Quark routes rank by how much of the lepton machinery they reuse

The table ranks every candidate. "Fit" measures how much existing, derived structure a route reuses against how much it must add.

| Rank | Route (literature anchor) | Fit to model | What the model must add | Status of supporting numbers |
|---|---|---|---|---|
| 1 | Koide pseudo-masses: k = 1 in the weak basis, CKM = U_U†U_D ([Żenczykowski, arXiv:1301.4143](https://arxiv.org/abs/1301.4143)) | High: keeps exact Q = 2/3 and puts deviations in T2g, which F93/F236 already identify as the only mixing channel; F236 §4 notes E_g-only gives CKM = 1, near data | Sector-specific T2g amplitudes (free by the F254 argument unless fixed dynamically); a T1g or complex T2g phase for J ≠ 0 | Żenczykowski's fit needed k = 1.015 and gave θ ≈ 2.44° vs 2.37° measured. The Gérard et al. variant needed m_s(M_Z) about 2.5× standard: real pressure |
| 2 | Sector-dependent E_g angle at a weight fraction (δ_U = δ*/3, δ_D = 2δ*/3 per Żenczykowski) | High in form: same Landau functional, O_h sees δ only through cos 3δ (F93 O5) | A principle assigning quark angles; says nothing about CKM, which stays 1 if both are E_g-diagonal | **Coincidence candidates.** δ_U(mixed) = 0.0745 vs 2/27 = 0.0741 (about 2.7σ using F346's implied error; computed here), and δ_U(M_Z) = 0.052 fails. δ_D(mixed) = 0.110 misses 4/27 by 26% and sits 1.45σ from 1/9 = δ*/2 (F346 "flagged, not adopted"; look-elsewhere p ≈ 0.3–0.6%) |
| 3 | Colour/charge-dressed E_g amplitude, a Sumino-style radiative shift of equipartition ([Sumino, arXiv:0812.2103](https://arxiv.org/abs/0812.2103)) | Medium: F170 says E_g self-couplings are *induced by the strong sector*, so the dressing has a home | A computation of F95's B (and C) with colour and charge factors; must produce k_U² = 1.55 and k_D² = 1.19 at mixed scale | Colour is common to u and d, so it **cannot alone** explain k_U ≠ k_D. (k²−1) differs by 2.8× between sectors (computed here). Needs charge dependence, echoing F80's EM-selector hypothesis |
| 4 | Gatto–Sartori–Tonin / four-zero textures, \|V_us\| ≈ √(m_d/m_s) ([Xing, arXiv:1909.09610](https://arxiv.org/abs/1909.09610)) | Medium: a T2g_xy (B1g) element plus a vanishing light-axis diagonal | A reason for the texture zero, **in the mass bilinear M = YY†, not in the amplitude Y** | Works to 0.36% vs λ = 0.22501 and is scale-stable. A Hermitian Y with a (1,1) zero gives sin θ_C ≈ (m_d/m_s)^¼ → 0.43, excluded (computed here) |
| 5 | Near-fixed-point hierarchy: modular Γ4 ≅ S4, T′ 2+1 structure ([Chen et al., arXiv:2506.23343](https://arxiv.org/abs/2506.23343); [Ding et al., arXiv:2307.14926](https://arxiv.org/abs/2307.14926)) | Medium-low: all three charged sectors sit near the tetragonal point δ ≈ 0, where T1u → E_u ⊕ A2u is 2+1 | A lattice analogue of "distance from a fixed point" that scales masses as powers of ε | Analogy only; modular fits use 6–14 real parameters |
| 6 | Group-theoretic Cabibbo from D7/Δ(6N²) residual mismatch ([arXiv:1411.5845](https://arxiv.org/pdf/1411.5845); [Holthausen–Lim, arXiv:1306.4356](https://arxiv.org/abs/1306.4356)) | Low: O_h contains no D7. Its angles (π/4, arctan√2) are nowhere near 0.225 | A group not inside O_h | sin(π/14) = 0.2225 is 1.1% below λ |
| 7 | Froggatt–Nielsen, RS/clockwork, split fermions ([arXiv:0807.4937](https://arxiv.org/abs/0807.4937); [arXiv:1807.09792](https://arxiv.org/pdf/1807.09792)) | Low: need a Higgs-coupled flavon or an extra dimension, and they predict no individual numbers | Composite flavon or lattice-overlap recast | Explain scaling, not values |
| 8 | Minimal top condensation (F352 → CL293) | Excluded internally | — | m_t = 226.6 GeV predicted, +31% |

Two further numbers need labels. **sin(2/9) = 0.2204 lies 1.7% below the direct |V_us| and 2.0% below the fit λ**, so it is a coincidence candidate with no mechanism. The Gatto-type relation beats it by a factor of five in accuracy. The pattern that 3δ_U ≈ 0.224 ≈ δ* and 3δ_D ≈ 0.330 ≈ 1/3 (the T-irrep weight) at mixed scale is **also a coincidence candidate**. It would additionally contradict decision 7, which puts the weight on δ, not on 3δ.

## Neutrino routes: type-I is native, the phase offset has a lattice reading

Among mass mechanisms, **type-I see-saw is the only natively Higgs-free option**, and the model already has it: F47 plus F236. Inverse and linear see-saws fit reasonably well if a small lepton-number-breaking μ comes from an almost-unbroken lattice Z_n. Type-II, type-III and radiative (Zee, scotogenic) models need elementary scalars and fit poorly. Every Majorana route reduces to the Weinberg operator, which needs a doublet-like order parameter, not necessarily an elementary one ([King–Luhn, arXiv:1301.1340](https://arxiv.org/abs/1301.1340)). The light-sterile escape is closed. MicroBooNE excludes the single 3+1 interpretation of LSND/MiniBooNE at 95% CL ([arXiv:2512.07159](https://arxiv.org/abs/2512.07159)), and KATRIN excludes most of the reactor/gallium region ([arXiv:2503.18667](https://arxiv.org/pdf/2503.18667)). Any extra F201-type singlet must be heavy or very weakly mixed. F237 separately excludes the 5.6 keV sterile as resonantly produced dark matter.

For the mass *spectrum*, Brannen's neutrino Koide is the literature route closest to the model. It keeps Q = 2/3, takes the lightest √m negative, and sets **δ_ν = 2/9 + π/12** ([Brannen 2006](https://brannenworks.com/MASSES2.pdf)). Against current data it predicts **r = 0.0308 against 0.0300 ± 0.0004, about 1.9σ high**, with Σ = 0.060 eV. Its 2006 absolute masses are 2.9–3.6σ off today's splittings ([neutrino note](../research_notes/Quark%20neutrino%20hierarchy%20lattice%20fit/neutrino_hierarchy_pmns.md)). The two notes fix the scale differently: one keeps Brannen's 2006 μ, the other refits to Δm²21. As a result they disagree on the sign of the Δm²31 miss (+2.9σ versus −4%). They agree on the scale-free r ≈ 0.0308. The best-fit offset is δ_ν ≈ 0.4778, i.e. δ* + 0.256 rather than δ* + 0.2618. That fit used pre-JUNO inputs.

The cubic note calls π/12 "not a natural O_h angle". There is an exact alternative reading (computed here): **π/12 is the node of the Koide circulant**. The smallest √m eigenvalue 1 + √2 cos(δ + 2π/3) vanishes exactly at δ = π/12, because 3π/4 − 2π/3 = π/12. At δ* it is still +0.040, which is why √m_e is small but positive. F201 already puts the M_R texture 0.14° from this node to produce its keV/GeV split. Brannen's phase can therefore be read as "δ* plus a shift to the node". That is a coincidence candidate that the model can test, not evidence. Brannen's form fixes masses only. A circulant is diagonalised by the trimaximal matrix, so it does not solve PMNS, which the previous section showed is a separate problem.

## Next derivations that can succeed or fail cleanly

Seven derivations follow, ordered by payoff per unit of effort.

**First**, formalise the O_h residual-symmetry theorem in sympy over all subgroups, not just involutions, and add generalised-CP residuals. The two claims to test are:

- in the cube-axis charged-lepton frame, no O_h residual gives viable PMNS;
- picture (b), with C3[111] charged leptons, admits TM1 through a named C2 of O.

This is exact and finite. It would extend F254 and CL223 from "the T2g amplitudes are free" to "no O_h selection can fix them". If picture (b) passes, it yields a falsifier already scheduled by JUNO: sin²θ12 = 0.318.

> **Result (2026-09-24 - 14:47) — done: [F403](../findings/F403-oh-residual-symmetry-pmns-no-go.md), claim CL315, gate record `F403-oh-residual-pmns` (15/15 PASS; both controls go red where declared).** Both claims hold.
> - **All subgroups, exact.** All 98 subgroups of O_h (30 of them in O) were built by closure in sympy. A subgroup allows a non-degenerate neutrino mass matrix only if it is an elementary abelian 2-group: 49 subgroups, of order at most 8. That rules out C3 and C4 residuals outright.
> - **Cube-axis frame: no-go.** None of the 47 non-trivial admissible subgroups is viable against NuFIT 6.0 at 3σ. Every fixed column either contains a zero (while θ13 ≠ 0) or is trimaximal (which would need sin²θ13 = 1/3).
> - **Generalised CP.** In the cube frame the only viable O_h constraint left is the y↔z mirror, i.e. μ–τ reflection (θ23 = 45°, δ = ±90°). Diagonal CP residuals force J = 0.
> - **Picture (b): TM1 opens.** In the C3[111] (trimaximal) frame the like-sign face-diagonal C2′ fix the TM1 column (2/3, 1/6, 1/6). That gives sin²θ12 = 1 − 2/(3cos²θ13) ∈ [0.3170, 0.3195], about 1.3–1.7σ above JUNO, and δ ∈ [252°, 293°]. All 18 surviving subgroups fix a single column (TM1 or TM2). No residual that fixes all three columns survives in any frame.
> - **BCC frame.** It changes nothing. The point group is still O_h, and the four [111] nearest-neighbour directions are not orthogonal, so no real "BCC frame" exists. The face-diagonal (C2′) frame is also a no-go. The C3[111] eigenbasis is the only O_h frame that opens.
> - **Caveat.** The no-go assumes the charged leptons are exactly diagonal on the cube axes. A charged-lepton rotation of order θ13 ≈ 0.15 rad would evade it. Picture (b) is recorded as an opening, not adopted, because it would reopen key decision 7. Derivation two decides between the frames.

**Second**, decide the picture (a)/(b) fork energetically. Extend the F118 Landau functional with T2g[111] and T1g[111] order parameters, then ask whether the E_g-diagonal or the trigonal-circulant condensate is the ground state at the F118 couplings. A (b) win would be a key-decision-level event.

**Third**, run the pseudo-mass quark fit. Per sector: A1g + E_g √M at k = 1, with δ at the candidate values, plus three T2g amplitudes and one phase. Fit PDG 2025 masses and CKM in *both* the mixed and the M_Z schemes. Count parameters against 10 observables, and test whether GST emerges without being imposed. The route fails if it needs m_s far from 93.5 MeV.

> **Result (2026-09-24 - 17:10) — done: [F407](../findings/F407-koide-pseudomass-minimal-quark-fit.md), claim CL316 extended, gate record `F407-koide-pseudomass-minimal` (7/7 in both schemes; both controls red exactly on the M2 legs).** The route passes the failure test and predicts nothing.
> - **Count.** 9 parameters (μ_U, μ_D, six T2g, one T1g) against 10 observables; the Jacobian has rank 9, so there is one genuine degree of freedom. The CKM also needs |V_td|: J alone leaves the cos δ_CP branch open.
> - **Candidate angles.** (δ*, δ*), (δ*/3, 2δ*/3) and (δ*/3, δ*/2) all fit at Δχ² ≤ 1 in the mixed and M_Z schemes, inside F404's band. The one degree of freedom does not discriminate between them.
> - **m_s.** It is not pulled (93.5–94.5 MeV mixed, 53.2–53.4 MeV at M_Z). The fit chooses a signed down sector itself: lightest amplitude negative, or middle negative in both sectors. Forced all-positive amplitudes close only at m_s ≈ 27 MeV (mixed) or 12.6 MeV (M_Z), about a quarter of PDG, the opposite direction from Gérard et al.
> - **GST.** It does not emerge. With |V_us| held out the fits span 0.2–0.98 above a soft floor near 0.19–0.20, and that floor does not scale as √(m_d/m_s).

**Fourth**, compute F95's cubic coefficient B with quark colour and charge factors. The test is whether the equipartition point shifts to c²/2 ≈ 1.55 (up) and 1.19 (down). The derivation fails if the shift is sector-blind.

> **Result (2026-09-24 - 15:35) — done, clean fail: [F405](../findings/F405-quark-B-colour-charge-koide-shift-no-go.md), gate record `F405-quark-B-colour-charge` (11/11 PASS; both controls go red where declared; attack pass CONFIRMED-NARROWER).**
> - **B with colour:** $B_q=N_c k_f^3 B_\ell$, giving −0.328 (up) and −0.223 (down) at the lepton ȳ. But B only multiplies cos 3δ, and Q = (1+k²)/3 is δ-blind, so no factor on B (or C) can move k.
> - **Stronger than sector-blind.** Colour and charge are the same on all three generations, so any dressing proportional to the identity leaves k exactly unchanged: a uniform mass rescale, an overall loop factor, or mass-independent running. The shift is zero, not merely sector-blind.
> - **The loop's own k-preference is k² ≈ 1.9,** which is wrong even for leptons. With a finite-stiffness selector, lepton Koide precision (PDG 2024 m_τ) would require a quark loop weight at least 4.6×10³ times the lepton one, where colour supplies 3.
> - **Loophole, a coincidence candidate.** The power-law undressing m → m^(1+ε) gives ε_U/ε_D = 3.88. That is 1.8–2.4σ from Q_u²/Q_d² = 4 depending on the error model, and it needs an O(1) coefficient, about 10⁴× any perturbative colour×charge loop. It goes to derivation seven's ledger.
> - **Still open.** These are the next derivations if route 3 is pursued:
>   - an A₁g/E_g-differential (inter-generation) stiffness, which is F95 §7's uncomputed loophole and the literal "dressed E_g amplitude";
>   - generation-dependent (family) charges, as in Sumino;
>   - a sector-dependent internal amplitude in the unitarity-cap regime (F405 L3), which is g-blind but can reach any quark k².

**Fifth**, feed the F236 see-saw with M_D locked at δ* and M_R scanned through the circulant node. Test whether r = 0.0300 comes out with NO, m₁ ≈ 0 and Σ ≤ 0.064 eV, and record m_ββ.

**Sixth**, re-target F236's T2g fit at NuFIT 6.0/6.1, including the θ23 octant, before any PMNS number is quoted again.

**Seventh**, enter every numerical match named here in one look-elsewhere-corrected ledger so none is promoted by accident: δ_U ≈ 2/27, δ_D ≈ 1/9, 3δ ≈ weights, sin(2/9) ≈ |V_us|, and π/12 as the node offset.

## Conclusion

The literature and the lattice agree on one point: masses come from diagonal condensates, and mixing comes from the *relative orientation of residual symmetries* between sectors. The model has built the diagonal half with unusual economy. Its no-gos (F236, F254, F353) are the lattice form of the standard S4 lesson that a Z3 or doublet texture alone cannot mix. The enumeration here extends those no-gos. In the cube-axis frame, O_h has no residual symmetry that could supply the neutrino mixing. PMNS therefore needs one of two things: new dynamics, or a reinterpretation of δ* as a trigonal axial-to-polar ratio. That choice is the most consequential open decision in the flavour sector, because it sets whether the model faces the JUNO TM1 test at all.

For quarks, the most promising path accepts Q = 2/3 as a pre-mixing statement and makes T2g carry both the Koide violation and the CKM. Colour dressing alone cannot distinguish up from down, so a charge-sensitive ingredient is unavoidable. The quark "phase" coincidences are fragile: they depend on the mass scheme and on m_s. They should not steer the programme until a derivation predicts them in a stated scheme.
