# Quark mass hierarchy and CKM mixing: current data and candidate mechanisms (as of 2026-09)

*Compiled 2026-09-24 - 00:00. Numbers marked "computed here" were calculated by this researcher from the cited inputs (Python, full precision). Nothing is fitted. Equations marked "standard" are textbook forms. The Xing review is the umbrella citation for them; their exact equations were not checked against the source in this session.*

---

## Q1. Current quark masses, CKM parameters, Jarlskog invariant, and how the mass ratios run with scale

### Takeaway
PDG 2025 gives light-quark masses in MS-bar at 2 GeV, charm and bottom as m(m), and the top from event kinematics (about 172.6 GeV). The CKM global fit (PDG review dated 1 Dec 2025) gives λ = 0.22501, A = 0.826, ρ̄ = 0.159, η̄ = 0.352, J = 3.12×10⁻⁵. Koide-type ratios for quarks depend strongly on scheme and scale. **The model's Q_up ≈ 0.849 and Q_down ≈ 0.731 match, to 3 digits, Q computed from the PDG *mixed-scale* summary-table masses (0.8488, 0.7313). At a common scale μ = M_Z they are 0.888 and 0.748.** This comparison therefore needs a stated scale convention.

### Cited Findings

**Quark masses (PDG 2024 + 2025 update summary table, created 30 May 2025)** — [PDG quark summary table](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf)
- Light quarks, MS-bar at μ = 2 GeV:
  - m_u = 2.16 ± 0.07 MeV
  - m_d = 4.70 ± 0.07 MeV
  - m_s = 93.5 ± 0.8 MeV
  - m_u/m_d = 0.462 ± 0.020
  - m̄ = (m_u+m_d)/2 = 3.49 ± 0.07 MeV
  - m_s/m̄ = 27.33 (+0.18/−0.14)
  - m_s/m_d = 17–22
- Heavy quarks, MS-bar mass at its own scale:
  - m_c(m_c) = 1.2730 ± 0.0046 GeV
  - m_b(m_b) = 4.183 ± 0.007 GeV
  - m_b − m_c = 3.45 ± 0.05 GeV
- Top quark:
  - direct (kinematic) mass 172.56 ± 0.31 GeV
  - MS-bar mass from cross-section 162.5 (+2.1/−1.5) GeV
  - pole mass from cross-section 172.4 ± 0.7 GeV
  - width 1.42 (+0.19/−0.15) GeV
- The PDG quark-mass review notes that the "2 GeV" masses from N_f = 2+1 and 2+1+1 lattice simulations are in slightly different schemes (N_L = 3 vs 4) — [PDG Quark Masses review](https://pdg.lbl.gov/2025/reviews/rpp2024-rev-quark-masses.pdf)
- FLAG Review 2024 (arXiv:2411.04268, published in PRD Jan 2026) is the lattice-average source. It gives light masses in MS-bar at 2 GeV, and m_c, m_b, by N_f. Its specific FLAG numbers were not extracted in this session — [FLAG 2024](https://arxiv.org/abs/2411.04268)

**Running masses at M_Z** — [Antusch, Hinze, Saad, arXiv:2510.01312](https://arxiv.org/html/2510.01312v1) (Oct 2025, PDG 2024 inputs)
- MS-bar Yukawas at M_Z:
  - y_u = (7.04±0.15)×10⁻⁶
  - y_d = (1.54±0.02)×10⁻⁵
  - y_s = (3.06±0.04)×10⁻⁴
  - y_c = (3.56±0.06)×10⁻³
  - y_b = (1.630±0.009)×10⁻²
  - y_t = 0.967±0.004
- The paper tabulates the same parameters up to 10¹⁶ GeV. At 10¹⁶ GeV, y_t = 0.4454±0.0048.
- CKM at M_Z (UTfit 2023):
  - θ₁₂ = 0.2251±0.0008
  - θ₂₃ = (4.193±0.041)×10⁻²
  - θ₁₃ = (3.70±0.08)×10⁻³
  - δ = 1.139±0.023 rad
  - J = (3.09±0.07)×10⁻⁵
- Double ratio (y_μ/y_s)(y_d/y_e) = 10.58±0.11 (Georgi–Jarlskog-type test)
- Masses at M_Z, computed here as m = y·v/√2 with v = 246.22 GeV:
  - m_u = 1.23 MeV, m_d = 2.68 MeV, m_s = 53.3 MeV
  - m_c = 0.620 GeV, m_b = 2.838 GeV, m_t = 168.4 GeV

**CKM (PDG review "CKM Quark-Mixing Matrix", dated 1 Dec 2025)** — [PDG CKM review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf)
- Global fit, CKMfitter method:
  - λ = 0.22501 ± 0.00068
  - A = 0.826 (+0.016/−0.015)
  - ρ̄ = 0.1591 ± 0.0094
  - η̄ = 0.3523 (+0.0073/−0.0071)
- UTfit method: λ = 0.22497(70), A = 0.839(11), ρ̄ = 0.1581(92), η̄ = 0.3548(72)
- Jarlskog invariant J = 3.12 (+0.13/−0.12) ×10⁻⁵
- Standard parametrization:
  - s₁₂ = 0.22501(68)
  - s₂₃ = 0.04183 (+0.00079/−0.00069)
  - s₁₃ = 0.003732 (+0.000090/−0.000085)
  - δ = 1.147 ± 0.026 rad
- Fitted magnitudes:
  - |V_ud| = 0.97435(16), |V_cs| = 0.97349(16)
  - |V_cd| = 0.22487(68)
  - |V_td| = 0.00858 (+19/−17)
  - |V_ts| = 0.04111 (+77/−68)
  - |V_tb| = 0.999118
- Direct determinations:
  - |V_ud| = 0.97367 ± 0.00032 (superallowed β decays)
  - |V_us| = 0.22431 ± 0.00085
  - |V_cb| = (41.1±1.2)×10⁻³ (inclusive 42.2±0.5, exclusive 39.8±0.6 — a persistent tension)
  - |V_ub|: inclusive 4.13 ± 0.12 (+0.13) ×10⁻³, exclusive 3.67 ± 0.09 ± 0.12 ×10⁻³
  - γ = 65.7 ± 3.0°
- First-row unitarity: |V_ud|²+|V_us|²+|V_ub|² = 0.9984 ± 0.0007. This is a **2.3σ deficit**, caused by the reduced |V_ud|. The PDG says it degrades the SM fit consistency.
- Earlier CKMfitter numbers, for reference (older):
  - 2021: λ=0.22500, A=0.8132, ρ̄=0.1566, η̄=0.3475, J=3.044×10⁻⁵
  - 2023: A=0.8215, λ=0.22498 — [search summary of CKMfitter updates](https://www.researchgate.net/publication/367121994_Recent_CKMfitter_updates_on_global_fits_of_the_CKM_matrix)

**Scale dependence of Koide-type ratios**
- Charged-lepton running masses violate Q = 2/3 by about 0.2% at M_Z, whereas pole masses satisfy it. For quarks, Q_U(M_Z) ≈ 0.89 and Q_D(M_Z) ≈ 0.74, and these are nearly stable from M_Z to about 10¹⁴ GeV. Grouping by mass rather than isospin, the heavy triple (c,b,t) sits much closer to 2/3 than the light triple (u,d,s) — [Xing & Zhang, PLB 635 (2006) 107, via Pith citation page](https://pith.science/citations/2c67d384-28dd-4b38-833b-d0db5444b964); [Rousselle arXiv:2608.19277](https://arxiv.org/html/2608.19277)
- Żenczykowski writes Koide's formula as Q = (1+k²)/3. Lepton pole masses give k_L = 1. For quarks, k_D ≈ 1.08 and k_U ≈ 1.25 at μ = 2 GeV, rising to k_D = 1.12 and k_U = 1.29 at M_Z. Running to lower scales lowers k, but "the top quark mass is so large that one certainly cannot bring k_U into the vicinity of 1" — [Żenczykowski arXiv:1301.4143](https://arxiv.org/abs/1301.4143)

**Koide Q and Brannen/Koide phase δ for quark triples, computed here**

Parametrization: √m_j = √M·(1 + √2·k·cos(2πj/3 + δ)), so Q = (1+k²)/3. The phase is tan δ = √3(√m₂−√m₁)/(2√m₃−√m₂−√m₁) (Żenczykowski eq. 5). As a check, lepton pole masses give Q = 0.666664 and δ = 0.222225 (2/9 = 0.222222).

| Triple | Q (PDG mixed scale) | δ (mixed) | Q (all at M_Z) | δ (M_Z) |
|---|---|---|---|---|
| u,c,t | **0.8488** | 0.0745 | 0.8876 | 0.0518 |
| d,s,b | **0.7313** | 0.1101 | 0.7478 | 0.1001 |
| c,b,t | 0.6692 | 0.069 | 0.7201 | 0.066 |
| −s,c,b (Rivero sign) | 0.6748 | — | 0.6991 | — |
| u,d,s | 0.5667 | 0.077 | 0.5669 | 0.077 |
| d,s,c | 0.6073 | — | 0.5904 | — |

(k from the same data: PDG mixed k_D = 1.093, k_U = 1.244; M_Z k_D = 1.115, k_U = 1.290. These agree with Żenczykowski's quoted values.)

### Inferences
- The model's Q_up = 0.849 and Q_down = 0.731 agree to about 0.1% with the PDG mixed-scale convention: u,d,s at 2 GeV MS-bar, c,b at m(m), t kinematic. They do not agree with a common-scale MS-bar evaluation (0.888 / 0.748 at M_Z). Either the model's outputs correspond to "physical-ish" masses at each quark's own scale, or the agreement depends on the convention. Any claim should state which convention it uses. The Q values are stable to about 0.3–0.5% within the mixed convention (m_u/m_d and m_s uncertainties are about 3% and 1%). Between conventions they move by about 5% (up) and 2% (down).
- Up-type ratios run noticeably between 2 GeV and M_Z. Q_up rises from 0.849 to 0.888 mainly because m_t(M_Z)/m_c(M_Z) is larger than 172.6/1.273.
- Wolfenstein λ ≈ √(m_d/m_s) holds to about 0.4%: 0.2242 at 2 GeV, 0.2243 at M_Z, vs λ = 0.2250. Both masses run together, so the ratio is scale-stable. See Q3.

### Gaps
- FLAG 2024 numerical averages (m_s, m_ud, m_c, m_b by N_f) were not extracted. The PDG averages are dominated by the same lattice inputs.
- No PDG 2026 edition numbers were found separately. The CKM review fetched is dated 1 Dec 2025 and may be the 2026-cycle update.
- Full Antusch et al. tables at 1 TeV to 10¹⁶ GeV for light Yukawas were not transcribed. Only y_t(10¹⁶) was obtained.

---

## Q2. Koide-type extensions to quarks: Rivero/waterfall, Kartavtsev, Sumino, Żenczykowski phases, QCD shifts

### Takeaway
No quark triple satisfies Q = 2/3 at a common scale with conventional signs. The near-misses are (c,b,t) at 0.669 (mixed scale) and Rivero's (−√m_s, √m_c, √m_b) at 0.675. The most relevant result for this model: **Żenczykowski (2013) conjectured δ_U = 2/27 = δ_L/3 and δ_D = 4/27 = 2δ_L/3, with δ_L = 2/9, for low-energy quark masses.** Against current PDG 2025 masses, δ_U(mixed) = 0.0745 matches 2/27 = 0.0741 to 0.6%. δ_D(mixed) = 0.110 misses 4/27 = 0.148 by 26%; his fit required m_s ≈ 160 MeV. Sumino's family-gauge mechanism explains why Koide holds at *pole* masses for leptons. No calculable QCD analogue that shifts Q from 2/3 for quarks was found.

### Cited Findings
- **Żenczykowski, "Koide's Z₃-symmetric parametrization, quark masses and mixings", arXiv:1301.4143** (PRD 2013). Main points:
  - Uses √m_fj = √M_f(1+√2 k_f cos(2πj/3+δ_f)).
  - For charged leptons k_L = 1 and δ_L = 0.2222324. With δ_L = 2/9 this predicts m_τ = 1776.9664 MeV.
  - Cites his PRD 86 (2012) 117303 for the observation δ_U ≈ 2/27 and δ_D ≈ 4/27 at low energy.
  - Adopts the Gérard–Goffinet–Herquet proposal (PLB 633 (2006) 563) that k_f = 1 holds for weak-basis "pseudo-masses", not mass eigenvalues.
  - Uses representative low-energy masses m_d = 7.843, m_s = 160.0, m_b = 4209, m_u = 4.392, m_c = 1296, m_t = 172000 MeV, which by construction reproduce δ_D = 4/27 and δ_U = 2/27 (verified here: 0.14814 and 0.07407).
  - Imposing k_D = k_U = 1.015 on pseudo-masses with the Fritzsch–Xing CKM decomposition gives a mixing angle θ ≈ 2.44°, "in good agreement with experiment".
  - Notes that Gérard et al. needed m_s(M_Z) about 2.5× the standard value to get k ≈ 1.
  - Source: [arXiv:1301.4143](https://arxiv.org/abs/1301.4143) (full text read)
- **Kartavtsev, "A remark on the Koide relation for quarks", arXiv:1111.0480** (2 pages, Nov 2011). It proposes a generalization of Koide's relation that combines up and down quarks and "approximates the Koide limit reasonably well". The exact formula was not extracted — [arXiv:1111.0480](https://arxiv.org/abs/1111.0480)
- **Rivero, "A new Koide tuple: strange-charm-bottom", arXiv:1111.7232.**
  - Claims (s,c,b) forms a Koide tuple when the sign of √m_s is negative, extending the earlier (c,b,t) tuple. It calls this tuple "quasi-orthogonal" to the lepton tuple.
  - In the "waterfall" picture, alternating up/down triples t-b-c-s-u-d chain together.
  - The original waterfall needed m_u → 0, which "has since fallen out of favor" empirically.
  - Sources: [ar5iv 1111.7232](https://ar5iv.arxiv.org/html/1111.7232); [Rivero, "Koide formula: beyond charged leptons" (ResearchGate)](https://www.researchgate.net/publication/275410011_Koide_formula_beyond_charged_leptons)
  - Computed here: Q(−s,c,b) = 0.6748 (mixed) and 0.6991 (M_Z). Q(c,b,t) = 0.6692 (mixed) and 0.7201 (M_Z). **Both are near 2/3 only in the mixed-scale convention.**
- **Sumino** (arXiv:0812.2090, PLB 671 (2009) 477; arXiv:0812.2103 / JHEP 05 (2009) 075; arXiv:0903.3640):
  - An effective theory with U(3)×SU(2) family gauge symmetry. Lepton masses come from the VEV of a 9-component scalar Φ, with m ∝ ⟨Φ⟩².
  - The radiative correction from family gauge bosons **cancels the QED correction** to Koide's formula when α = α_F/4, assuming U(3)_family unifies with SU(2)_L.
  - This is why Koide holds for pole masses rather than running masses. Without the cancellation, QED running alone shifts Q at order α.
  - Sources: [arXiv:0812.2103](https://arxiv.org/abs/0812.2103), [arXiv:0812.2090](https://arxiv.org/abs/0812.2090)
  - Follow-ups: family gauge bosons with inverted hierarchy [arXiv:1203.2028](https://arxiv.org/pdf/1203.2028); an anomaly-free version of the cancellation [arXiv:1608.04514](https://arxiv.org/pdf/1608.04514)
- **Rousselle, arXiv:2608.19277 (v2, 10 Sep 2026).**
  - U(3)_F → U(1)³_F with a flavon coupled to the Higgs via a dimension-6 operator.
  - "Dynamical vacuum alignment" imposes equipartition I₀ = I₈ between the flavour-singlet and flavour-octet invariants, giving Q = 2/3. It formalizes and extends Sumino.
  - It explicitly does **not** extend to quarks. It attributes the failure to the SU(3)_c vacuum and confinement, and gives no Q_U or Q_D calculation and no QCD correction to Q.
  - Source: [arXiv:2608.19277](https://arxiv.org/html/2608.19277)
- **Xing & Zhang, PLB 635 (2006) 107**: Koide-like ratios for running quark masses (Q_U ≈ 0.89, Q_D ≈ 0.74 at M_Z), nearly stable up to about 10¹⁴ GeV — [Pith citation page](https://pith.science/citations/2c67d384-28dd-4b38-833b-d0db5444b964). Rodejohann & Zhang, PLB 698 (2011) 152, also give k values for quarks and neutrinos; cited via Żenczykowski.
- A modified Koide formula from flavour nonets in a scalar-potential/Yukawaon model — [Nucl. Phys. B (2021), ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0550321321002431). Empirical explorations of Koide-type formulas — [EPJC 2016](https://link.springer.com/article/10.1140/epjc/s10052-016-3990-3).

### Inferences
- **The (2/9)/3 and (2/9)·(2/3) phase pattern connects directly to δ* = 2/9 in the model.** Today δ_U at mixed scale (0.0745) is within 0.6% of 2/27. δ_D is not near 4/27 with PDG 2025 masses (0.110; m_s = 93.5 MeV is much smaller than the 160 MeV he used). δ_D(mixed) = 0.110 is close to δ_L/2 = 1/9 = 0.1111 (1% off). This is a numerical observation made here, not a published claim, and it may be a coincidence.
- A lattice model predicting quark Q values at fixed δ* must also set k_U and k_D, i.e. the "amplitude" rather than the phase. Pure O_h representation theory would naturally fix k = 1 (Q = 2/3). The observed k_U ≈ 1.24 and k_D ≈ 1.09 therefore need a crystal-field or colour-sector source.
- The Gérard–Goffinet–Herquet and Żenczykowski route keeps Q = 2/3 for *weak-basis* quark pseudo-masses and moves the deviation into the CKM rotation. It is a concrete falsifiable alternative for a model whose exact output is Q = 2/3 before mixing.
- Sumino's mechanism depends on gauge-coupling bookkeeping, α_F = 4α. Any QCD analogue would need α_s-sized cancellations, which are not calculable in the same perturbative way. No literature was found that computes a QCD shift of Q from 2/3.

### Gaps
- Kartavtsev's exact formula and scale were not extracted (abstract only).
- Żenczykowski PRD 86 (2012) 117303 was not read directly. The quark masses and scheme behind δ_U ≈ 2/27 and δ_D ≈ 4/27 are known only through the 2013 paper.
- The exact scale at which Rivero evaluated (−s,c,b) was not confirmed.
- Brannen's original sqrt-mass papers (brannenworks.com, 2006) were not accessed. They are cited via Żenczykowski and Rivero–Gsponer hep-ph/0505220.

---

## Q3. Froggatt–Nielsen, GST relation, Fritzsch and texture zeros, democratic matrix plus perturbation

### Takeaway
These are the older, low-parameter-count approaches. The Gatto–Sartori–Tonin relation |V_us| ≈ √(m_d/m_s) still works to about 0.4% and is scale-stable. Froggatt–Nielsen explains hierarchies as powers of ε ≈ λ ≈ 0.22 but has O(1) coefficients and no sharp predictions. The original six-zero Fritzsch texture is excluded because it needs a much lighter top. Four-zero Hermitian textures remain viable. Current mechanism literature (modular flavour) often reproduces FN as a limit.

### Cited Findings
- Computed here from PDG and Antusch inputs:
  - GST: √(m_d/m_s) = 0.2242 (2 GeV) and 0.2243 (M_Z), vs |V_us| = 0.22501(68) (PDG fit) or 0.22431(85) (direct).
  - Companion hierarchies at M_Z:
    - √(m_u/m_c) = 0.0445
    - √(m_s/m_b) = 0.137
    - √(m_c/m_t) = 0.0607
    - m_s/m_b = 0.0188
    - m_c/m_t = 0.00368
  - Compare |V_cb| = 0.0418 and |V_ub|/|V_cb| = 0.089.
  - Inputs: [PDG summary](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf), [arXiv:2510.01312](https://arxiv.org/html/2510.01312v1), [PDG CKM](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-ckm-matrix.pdf)
- Xing's Physics Reports review (vol. 854 (2020) 1–147, arXiv:1909.09610) is the comprehensive source for texture zeros, Fritzsch and nearest-neighbour textures, democratic (S3_L×S3_R) textures with breaking, and "simple discrete and continuous flavor symmetries" in model-independent Yukawa-texture determination — [arXiv:1909.09610](https://arxiv.org/abs/1909.09610)
- Fritzsch & Xing (PLB 413 (1997) 396; PRD 57 (1998) 594) argued that the quark mass hierarchy picks out a "most physical" CKM parametrization, V = U_u† U_d with tan θ_u ≈ √(m_u/m_c) and tan θ_d ≈ √(m_d/m_s). Żenczykowski builds on this — [arXiv:1301.4143](https://arxiv.org/abs/1301.4143)
- Standard equations (textbook forms; cited to the Xing review, not re-verified in this session):
  - FN: Y_ij ~ c_ij ε^(q_i + u_j) with ε = ⟨θ⟩/Λ ≈ 0.2. Typically m_u:m_c:m_t ~ ε⁸:ε⁴:1 and m_d:m_s:m_b ~ ε⁴:ε²:1. Then V_us ~ ε, V_cb ~ ε², V_ub ~ ε³.
  - Fritzsch six-zero: M = [[0,A,0],[A*,0,B],[0,B*,C]], which gives |V_cb| ≈ |√(m_s/m_b) − e^{iφ}√(m_c/m_t)|. It fails for m_t ≳ 100 GeV.
  - Democratic: M = (c/3)·J, where J is the all-ones matrix. This gives one heavy eigenvalue (t or b) and two zero eigenvalues, lifted by small diagonal S3-breaking terms (Harari–Haut–Weyers 1978; Fritzsch–Xing).
  - Source: [arXiv:1909.09610](https://arxiv.org/abs/1909.09610)

### Inferences
- A crystal-field split T1u triplet is in effect an S3- or S4-symmetric matrix plus perturbations, so the democratic and "S3 plus breaking" literature is the closest traditional analogue. An orthorhombic break takes O_h to D2h and lifts the triplet into three singlets. This is structurally a diagonal breaking of a degenerate triplet, i.e. the opposite limit from democratic rank-1.
- GST succeeds only if the down-sector 1–2 rotation dominates V_us and the (1,1) element of M_d is zero. A lattice model reproduces λ "for free" if its down-type matrix has a texture zero at (1,1) in the weak basis.

### Gaps
- Primary sources for FN (1979), GST (1968), Fritzsch (1977–78) and Harari–Haut–Weyers (1978) were not fetched. The equations above are standard forms and should be verified against Xing's review before quoting.
- No 2024–26 status paper on four-zero textures was retrieved.

---

## Q4. Discrete and modular flavour symmetries for quarks; Cabibbo angle from group theory

### Takeaway
Residual-symmetry ("direct") approaches can produce the Cabibbo angle from group theory:
- Δ(6N²) with a Z₂×Z₂ residual gives |V_us| = 0.222521 for 7 | N.
- Holthausen–Lim find only Δ(6·10²), (Z₁₈×Z₆)⋊S₃ and Δ(6·16²) reproduce all mixing angles (with Dirac neutrinos) among groups up to order 200.

These give only θ_C at leading order; θ₂₃, θ₁₃ and the masses need breaking. Modular flavour symmetry (Γ_N ≅ S3, A4, S4, A5 and double covers) has become the dominant 2019–26 programme. Hierarchies come from the modulus τ sitting near a fixed point (i, ω, i∞), where residual symmetry makes masses scale as powers of the distance ε. This is effectively a geometric FN mechanism.

### Cited Findings
- Ishimori & King, "A model of quarks with Δ(6N²) family symmetry", arXiv:1403.4395: "the Cabibbo angle is correctly determined by a residual Z₂×Z₂ subgroup", while the smaller angles are only qualitative — [arXiv:1403.4395](https://arxiv.org/pdf/1403.4395)
- Ishimori, King, Okada, Tanimoto, "Quark mixing from Δ(6N²) family symmetry", arXiv:1411.5845: |V_us| = 0.222521 when N is a multiple of 7, i.e. sin(π/14) = 0.2225. For N = 14, about 3% breaking of Z₂×Z₂ allows full agreement — [arXiv:1411.5845](https://arxiv.org/pdf/1411.5845)
- Holthausen & Lim, PRD 88 (2013) 033018, arXiv:1306.4356: quark mixing from mismatched remnant symmetries. Several groups give "only the Cabibbo angle at leading order". Assuming Dirac neutrinos, Δ(6·10²), (Z₁₈×Z₆)⋊S₃ and Δ(6·16²) are the only groups (order ≤ 200 scan) reproducing favoured mixing — [arXiv:1306.4356](https://arxiv.org/abs/1306.4356)
- Related: "The Cabibbo angle as a universal seed for quark and lepton mixings" [arXiv:1410.3658](https://arxiv.org/abs/1410.3658); dihedral groups for quark and lepton mixing [JHEP03(2019)056](https://link.springer.com/article/10.1007/JHEP03(2019)056); residual-symmetry vacuum alignment [JHEP07(2026)022](https://link.springer.com/article/10.1007/JHEP07(2026)022)
- Modular flavour and fixed points:
  - Chen, Li, Liu, Ratz, "Modular Flavor Symmetries and Fermion Mass Hierarchies", arXiv:2506.23343 (June 2025): hierarchical masses *require* ⟨τ⟩ near a critical point (i, i∞, ω). The paper classifies how masses scale with distance from i and ω and compares with FN — [arXiv:2506.23343](https://arxiv.org/abs/2506.23343)
  - "Quark masses and CKM hierarchies from S4′ modular flavor symmetry", arXiv:2301.07439 (EPJC 2023): τ at large Im τ, residual Z4^T approximately unbroken, "the Froggatt–Nielsen mechanism works" — [arXiv:2301.07439](https://arxiv.org/abs/2301.07439)
  - "Quark masses and mixing from modular S4′ with canonical Kähler effects", arXiv:2604.01422 (JHEP08(2026)162): S4′ plus CP. Canonical normalization from the Kähler metric is essential to reproduce hierarchies with O(1) couplings — [arXiv:2604.01422](https://arxiv.org/html/2604.01422)
  - Petcov & Tanimoto: A4 modular quark models near τ = ω and near τ = i∞ (2023) — [search summary](https://arxiv.org/pdf/2412.18435)
  - "Large and small hierarchies from finite modular symmetries" [arXiv:2412.18435](https://arxiv.org/pdf/2412.18435); "Modular Symmetry with Weighton" [arXiv:2505.12916](https://arxiv.org/pdf/2505.12916); non-holomorphic modular A5 [arXiv:2410.24103](https://arxiv.org/pdf/2410.24103)
  - "Modular binary octahedral symmetry for flavor structure of Standard Model" (2O ≅ modular S4′-type): generations as a triplet or as 2 ⊕ 1 of 2O — [arXiv:2307.14926](https://arxiv.org/pdf/2307.14926)
  - Ding (TDLI talk, Nov 2024), modular symmetry overview — [slides](https://indico-tdli.sjtu.edu.cn/event/2779/attachments/5216/8631/modular%20symmetry%20and%20applications%20in%20particle%20physics%20and%20cosmology_dinggj(1).pdf)

### Inferences
- Parameter counts vary. Residual-symmetry models predict θ_C with zero continuous parameters (a group choice plus a residual subgroup) but leave masses free. Modular quark models typically use 6–12 real parameters (Re τ, Im τ plus coupling ratios) for 10 observables (6 masses, 3 angles, 1 phase). The better fits (S4′ plus CP) reach χ² ≲ few with O(1) couplings, but hierarchy still requires tuning τ to within ε ~ 0.01–0.1 of a fixed point.
- sin(π/14) = 0.2225 is 1.1% below λ = 0.2250 (PDG fit) and about 0.8% below direct |V_us|. It is now in mild tension without the allowed 3% breaking.
- For an O_h model, the dihedral residual-symmetry results are relevant. The Cabibbo angle arises as a mismatch between residual Z₂×Z₂ subgroups in the up and down sectors. An orthorhombic (D2h ⊃ Z₂×Z₂) crystal-field break is exactly a Z₂×Z₂ residual. If up and down quarks feel differently-oriented orthorhombic breaks, the mismatch angle would be group-theoretic. O_h itself only gives angles from its 4-fold and 3-fold axes (π/4, arctan√2 and so on), which are not near 0.225.

### Gaps
- No single 2025–26 review with a table of modular quark-fit χ² and parameter counts was retrieved. The Kobayashi–Tanimoto modular review was not fetched.
- A4, S4, T′ and Δ(27) quark-sector models specifically (as distinct from modular ones) were not surveyed individually. The general finding that the tri-bimaximal groups give no Cabibbo angle at leading order is standard but was not sourced here.
- Lam's work on the Cabibbo angle from finite groups was not located in this session.

---

## Q5. Geometric, extra-dimensional, clockwork, radiative and condensate mechanisms

### Takeaway
Geometric mechanisms replace free Yukawa hierarchies with exponentials of O(1) geometric parameters. The best examples are Randall–Sundrum bulk-mass wavefunction overlaps, split fermions and clockwork chains. They explain hierarchy and CKM scaling (V_ij ~ F_qi/F_qj) with "anarchic" O(1) 5D Yukawas, but predict no individual numbers. Their falsifiable content is in FCNC and ε_K constraints on the KK/clockwork scale.

### Cited Findings
- "Flavor Physics in the Randall-Sundrum Model I", arXiv:0807.4937. Fermion hierarchies and CKM come "naturally in terms of anarchic five-dimensional Yukawa matrices and wave-function overlap integrals" — [arXiv:0807.4937](https://arxiv.org/abs/0807.4937)
- The anarchic RS model is "a low energy solution to both the electroweak hierarchy and flavor problems", probed by LFV — [hep-ph/0606021](https://arxiv.org/html/hep-ph/0606021v1). Loop-induced dipoles are in "Warped Penguins", arXiv:1004.2037 — [arXiv:1004.2037](https://arxiv.org/pdf/1004.2037). RS with T′ family symmetry — [arXiv:0907.3963](https://arxiv.org/pdf/0907.3963)
- "A clockwork solution to the flavor puzzle", arXiv:1807.09792 (JHEP10(2018)099). Clockwork chains naturally explain SM quark mass and mixing hierarchies; the paper discusses the similarities and differences with RS — [arXiv:1807.09792](https://arxiv.org/pdf/1807.09792)
- Standard forms (not re-verified here):
  - RS zero-mode profile F(c) ≈ √((1−2c)/(1−ε^(1−2c))), giving m_q ~ v·F(c_Q)·Y₅·F(c_q).
  - Clockwork: Yukawa ~ q^(−N) for N sites and charge ratio q.
- A 2026 "low-rank ternary structure of fermion masses and hidden flavor coordinates" paper appeared in results — [arXiv:2606.08459](https://arxiv.org/pdf/2606.08459). It was not read.

### Inferences
- The model's crystal-field and condensate picture is closest to split-fermion and localization ideas, where the hierarchy is exponential in a geometric separation. The difference is that O_h gives an exact representation-theory origin for a triplet, whereas RS and clockwork put in three copies by hand.

### Gaps
- Radiative (loop-induced, "one mass per loop order") hierarchies and top-condensation/NJL quark-mass mechanisms were **not researched in this session** (tool budget). Known references such as Weinberg 1972, Balakrishna 1988, Dobrescu–Fox 2008 and Bardeen–Hill–Lindner 1990 are unsourced here and should be treated as leads only.
- Split fermions (Arkani-Hamed–Schmaltz 2000) were not fetched.

---

## Q6. Cubic, octahedral (O, O_h, S4) and crystal-field or lattice-inspired quark masses

### Takeaway
S4 ≅ O is a mainstream flavour group, in both traditional and modular (Γ4 ≅ S4, 2O ≅ S4′) forms, and S4 models give acceptable CKM plus hierarchies with breaking. No paper was found that uses the full O_h point group (including inversion/parity) with a *crystal-field* (O_h → D4h/D2h) splitting of a T1u triplet to generate quark masses. The model's construction appears to be unexplored in the literature, as far as this search could establish.

### Cited Findings
- "S4 Flavor Symmetry and Fermion Masses: Towards a Grand Unified theory of Flavor", hep-ph/0602244: S4 ≅ O used for all fermions — [hep-ph/0602244](https://arxiv.org/pdf/hep-ph/0602244)
- An S4 model with acceptable CKM and "realistic mass hierarchies between all the fermions" — [Nucl. Phys. B (2009), ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0550321309001357)
- The modular binary octahedral group 2O has generations as a triplet or 2 ⊕ 1 — [arXiv:2307.14926](https://arxiv.org/pdf/2307.14926)
- "Octahedral Symmetry in Elementary Particle Physics" (ResearchGate, 2021; provenance and peer review unclear) — [ResearchGate](https://www.researchgate.net/publication/349694645_Octahedral_Symmetry_in_Elementary_Particle_Physics)
- "The fermion mass matrices near a fixed point", Z. Phys. C (older, not read) — [Springer](https://link.springer.com/article/10.1007/BF01421758)

### Inferences
- In S4 language the model's T1u triplet is the 3 (or 3′ depending on convention). Parity-odd T1u is absent in S4 ≅ O models, because inversion is not part of the flavour group there. That gives O_h an extra handle: the g/u distinction. The E_g second shell corresponds to the S4 doublet 2. Standard S4 flavour models do use a doublet flavon (2) to break S4 → Z₂×Z₂ or similar. **An E_g condensate breaking a T1u (3) triplet is therefore group-theoretically the same move as the S4 "doublet flavon" models**, and those papers are the natural comparison literature.
- Checkable prediction: if one angle δ* = 2/9 sets lepton masses, then Żenczykowski-type δ_U = δ*/3 and δ_D = 2δ*/3 would be natural targets for any colour-induced rescaling of the phase. With current masses only δ_U(mixed) ≈ 2/27 holds (0.6%); δ_D(mixed) ≈ 1/9 = δ*/2 (1%). Both are numerical observations from this session.

### Gaps
- No literature search hit on "crystal field" plus "quark mass" or on a BCC lattice with generation triplets. There may be isolated or unrefereed papers not found in one search.
- The S4-model details (parameter counts and fit quality for the quark sector) in hep-ph/0602244 and the 2009 NPB paper were not extracted.
