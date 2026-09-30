# Neutrino masses, mass ordering and PMNS mixing — data and mechanisms (status 2026-09)

*Research notes, 2026-09-24 - 10:49. Written for the question: can a Higgs-free lattice model whose three generations are the T1u triplet of O_h, with an E_g (Z3-like) second-shell texture, reproduce the lepton mixing data? Numbers marked "(computed here)" are my own arithmetic on the cited inputs, not quoted from a source.*

## Q1. Current oscillation parameters, mass ordering, absolute-mass bounds

### Takeaway
The PMNS matrix is now measured to few-percent precision except for θ23's octant and δ_CP. After JUNO's first data (Nov 2025), sin²θ12 = 0.3096 (+0.0057/−0.0073) and Δm²21 = 7.53×10⁻⁵ eV² (±1.3%). Normal ordering is preferred at only ~2.2–2.5σ. Cosmology (DESI DR2 + CMB, Σm_ν < 0.064 eV at 95%) now sits right on the NO oscillation floor (Σ ≳ 0.059 eV) and disfavours IO. Laboratory bounds (KATRIN m_β < 0.45 eV; KamLAND-Zen m_ββ < 28–122 meV) are still far weaker.

### Cited Findings

**NuFIT 6.0 (data to Sept 2024; arXiv:2410.05380, JHEP 12 (2024) 216).** Two variants: "IC19 w/o SK-atm" and "IC24 with SK-atm" — [arXiv PDF, Table 1](https://arxiv.org/pdf/2410.05380)

| Parameter | NO, IC24+SK-atm (global best fit) | IO, same (Δχ² = 6.1) | NO, IC19 w/o SK-atm (Δχ² = 0.6; IO is best there) |
|---|---|---|---|
| sin²θ12 | 0.308 +0.012/−0.011 (3σ: 0.275–0.345) | 0.308 | 0.307 |
| θ12 | 33.68° +0.73/−0.70 | 33.68° | 33.68° |
| sin²θ23 | 0.470 +0.017/−0.013 (3σ: 0.435–0.585) | 0.550 | 0.561 (θ23 = 48.5°) |
| θ23 | 43.3° +1.0/−0.8 | 47.9° | 48.5° +0.7/−0.9 |
| sin²θ13 | 0.02215 +0.00056/−0.00058 | 0.02231 | 0.02195 |
| θ13 | 8.56° ± 0.11 (3σ: 8.19–8.89) | 8.59° | 8.52° |
| δ_CP | 212° +26/−41 (3σ: 124–364) | 274° +22/−25 | 177° +19/−20 |
| Δm²21 | 7.49 ± 0.19 ×10⁻⁵ eV² | same | same |
| Δm²3ℓ | +2.513 +0.021/−0.019 ×10⁻³ eV² | −2.484 ± 0.020 | +2.534 +0.025/−0.023 |

- Relative 3σ precision: θ12 ~13%, θ13 ~8%, Δm²21 ~15%, |Δm²3ℓ| ~6%. θ23's octant is still ambiguous: the other-octant minimum always has Δχ² < 4 — [arXiv:2410.05380](https://arxiv.org/abs/2410.05380)
- Leptonic Jarlskog: J_CP^max = 0.0333 ± 0.0007. In NO, CP conservation is disfavoured by only Δχ² = 0.02 (0.55 with IC24+SK). In IO, CP conservation is disfavoured at 3.6σ (4σ), with J_best ≈ −0.032. For comparison, the quark J = 3.12×10⁻⁵ — [NuFIT 6.0 PDF §2](https://arxiv.org/pdf/2410.05380)
- T2K and NOvA appearance data each favour NO on their own, but in the combination they pull in different directions, which weakens the ordering discrimination — [arXiv:2410.05380 abstract](https://arxiv.org/abs/2410.05380)

**JUNO first results (59.1 days, Aug 26 – Nov 2, 2025; arXiv:2511.14593; Nature 2026)**
- sin²θ12 = 0.3092 ± 0.0087 and Δm²21 = (7.50 ± 0.12)×10⁻⁵ eV² (NO assumed). This is 1.6× more precise than all previous measurements combined — [arXiv:2511.14593](https://arxiv.org/abs/2511.14593); [Nature](https://www.nature.com/articles/s41586-026-10538-z)
- Press coverage says JUNO "confirmed" the ~1.5σ solar-vs-reactor Δm²21 difference — [phys.org](https://phys.org/news/2025-11-juno-physics-results-months.html). The NuFIT follow-up below does not explicitly discuss this tension, so treat the claim as unconfirmed.

**NuFIT 6.1 / "Lessons from the first JUNO results" (Esteban, Gonzalez-Garcia, Maltoni, Martinez-Soler, Pinheiro, Schwetz; arXiv:2601.09791)**
- sin²θ12 = 0.3096 +0.0057/−0.0073 and Δm²21 = (7.530 +0.096/−0.097)×10⁻⁵ eV². JUNO already dominates the (1,2) sector — [arXiv:2601.09791](https://arxiv.org/html/2601.09791v2)
- Mass ordering: Δχ²(IO−NO) = 4.6 without atmospheric data and 9.4 with SK + IceCube. The p-value for IO is ≈ 2.0–2.6%, i.e. ~2.2–2.3σ, and the authors call this preliminary — [arXiv:2601.09791](https://arxiv.org/html/2601.09791v2)
- A separate (1,2)-sector update after JUNO also exists — [arXiv:2511.21650](https://arxiv.org/pdf/2511.21650)

**Bari group (Capozzi, Giarè, Lisi, Marrone, Melchiorri, Palazzo; arXiv:2503.07752, PRD 111, 093006 (2025))**
- Data to early 2025. |Δm²| is the first parameter below 1% precision (0.8% at 1σ). NO is preferred over IO at 2.2σ. The paper also combines oscillation data with DESI/cosmology — [arXiv:2503.07752](https://arxiv.org/abs/2503.07752)
- I did not retrieve the 2025–26 de Salas–Valle (Valencia) update.

**Absolute mass**
- KATRIN: m_β < 0.45 eV (90% CL) from 259 days (2019–21, ~36 M electrons), a factor-2 improvement. Science 388, 180 (2025), arXiv:2406.13516 — [arXiv](https://arxiv.org/html/2406.13516); [Science](https://www.science.org/doi/10.1126/science.adq9592)
- DESI DR2 BAO + CMB (ΛCDM, three degenerate ν): Σm_ν < 0.0642 eV (95%), σ(Σm_ν) = 0.020 eV. This approaches the oscillation lower bound and is in tension with IO. An "effective" Σm_ν allowed to go negative prefers negative values, ~3σ from the oscillation floor (σ = 0.053 eV) — [OSTI: Constraints on neutrino physics from DESI DR2 BAO and DR1 full shape](https://www.osti.gov/biblio/3006914) (DESI collaboration paper; I believe it is arXiv:2503.14744, but that ID was not fetched). A discussion of how robust the cosmological bound is: [arXiv:2407.13831](https://arxiv.org/pdf/2407.13831). Loosening mechanisms, e.g. interacting dark energy: [arXiv:2606.05005](https://arxiv.org/abs/2606.05005), [arXiv:2504.20338](https://arxiv.org/abs/2504.20338)

**0νββ**
- KamLAND-Zen 800, full dataset (2.1 ton·yr ¹³⁶Xe), combined with the earlier phase: T½ > 3.8×10²⁶ yr (90% CL), giving m_ββ < 28–122 meV. arXiv:2406.11438, PRL — [arXiv](https://arxiv.org/abs/2406.11438)
- LEGEND-200 (⁷⁶Ge): T½ > 1.6×10²⁶ yr alone, giving m_ββ < 70–161 meV. Combined GERDA + MJD + LEGEND-200 sensitivity is > 2.8×10²⁶ yr, with no signal — [EPJ Web Conf.](https://doi.org/10.1051/epjconf/202533801002); [LBNL news 2026-03](https://nuclearscience.lbl.gov/2026/03/30/legend-200-publishes-its-first-results/)

### Inferences
- Orderings (standard facts, not fetched): for NO, m2 ≥ √Δm²21 ≈ 8.7 meV and m3 ≥ √Δm²31 ≈ 50 meV, so Σ ≥ ~0.059 eV. For IO, Σ ≥ ~0.10 eV. DESI's 0.064 eV therefore leaves almost no room above the NO minimum. A lattice model predicting NO with m1 ≈ 0 (Σ ≈ 0.059–0.060 eV) is cosmologically the safest option. Any prediction with Σ ≳ 0.07 eV is in mild tension; ≳ 0.1 eV (IO or quasi-degenerate) is disfavoured.
- The scale-free observable to target is the ratio r ≡ Δm²21/Δm²31 = 0.0300 ± ~0.0004 (computed here, NuFIT 6.1 × NuFIT 6.0 Δm²31). It is now known to ~1.4%, dominated by JUNO.
- The IO m_ββ band (~15–50 meV) is already partly probed by KamLAND-Zen. The NO band with m1 → 0 is ~1–4 meV, far below reach.

### Gaps
- Official JUNO mass-ordering result (needs ~6 yr of exposure); no 2026 JUNO ordering release was found.
- Latest de Salas–Valle fit numbers were not retrieved.
- Whether a NuFIT 6.1 full table (θ23, δ) differs materially from 6.0: I only obtained the (1,2)-sector numbers and the ordering Δχ².

---

## Q2. Discrete-symmetry mixing patterns (TBM, BM, GR, S4 ≅ O, TM1/TM2, μ–τ, CSD(n), direct vs semi-direct)

### Takeaway
Exact tribimaximal (TBM), bimaximal and golden-ratio mixing are excluded at leading order. θ13 ≈ 8.6° killed them in 2012, and JUNO's sin²θ12 = 0.3096 now also excludes TBM's solar angle 1/3 at ~4σ (computed here). The surviving descendants are TM1 (first TBM column preserved: sin²θ12 = 0.318, ~1–1.5σ high) and μ–τ-reflection-type predictions for (θ23, δ). TM2 (sin²θ12 = 0.341) is excluded at ~5σ (computed here). The canonical group for TBM/TM1 is S4, which is isomorphic to O, the rotation group of the cube. Its residual-symmetry recipe needs a Z3 (C3 about a body diagonal) in the charged-lepton sector and a Z2×Z2 (or one Z2 for TM1) in the neutrino sector. A Z3-only texture on its own gives no predictive mixing.

### Cited Findings
- Surviving descendant — TM1 sum rules:
  - Solar: sin²θ12 = 1 − 2/[3(1 − sin²θ13)], which gives sin²θ12 = 0.3182 ± 0.0004.
  - Atmospheric (parameter-free correlation): cos δ = [1/6 − sin²θ12 cos²θ23 − cos²θ12 sin²θ23 sin²θ13] / (2 s12 c12 s23 c23 s13), which gives δ ≈ −71° at sin²θ23 = 0.573.
  - m_ee ~ 2–5 meV.
  - The prediction is 1.0σ above JUNO's value and 1.2σ above NuFIT 6.0's — [Ardakanian, arXiv:2603.21264](https://arxiv.org/html/2603.21264). *Source caveat:* a single-author paper from an "independent researcher". The sum rules themselves are standard (King–Luhn review below).
- Littlest Seesaw: two right-handed neutrinos with CSD(3) Dirac alignments (0,1,1) and (1,3,1). It is the minimal predictive type-I seesaw and gives TM1 mixing, with near-maximal θ23 correlated with near-maximal CP violation — [King, arXiv:1512.07531](https://arxiv.org/pdf/1512.07531). An S4 realisation of TM1 with spontaneous CP violation — [Luhn, arXiv:1306.2358](https://arxiv.org/html/1306.2358).
- Minimality of A4 for the Z3 failure: an abelian Z3 Froggatt–Nielsen charge texture in a type-I seesaw fails for neutrinos.
  - The Majorana bilinear (q_i + q_j) mod 3 leaves an unsuppressed off-diagonal M_R entry (charges 1+2 ≡ 0). This over-suppresses m1 and m2 to O(ε³), giving Δm²21/Δm²31 ~ 4×10⁻¹¹ (median) against the observed 0.030.
  - The PMNS angles come out Haar-random (median sin²θ12 ≈ 0.5), with "no mixing structure".
  - The claimed fix is a non-abelian triplet group (A4 ⊂ S4), with a singlet flavon plus a triplet flavon aligned along (1,1,1). This gives m1 = a, m2 = a + b, m3 = −a at LO (TBM), and TM1 at NLO.
  - The paper names S4/T′ as the natural group that breaks to Z3 for quarks and A4 for leptons.
  - It also notes that the cusp (Im τ → ∞) of modular A4 reproduces the Z3 pathology — [arXiv:2603.21264](https://arxiv.org/html/2603.21264). *Directly analogous to this project's E_g/Z3 failure. Same single-author caveat.*
- Canonical references (primary papers; IDs from my knowledge, not fetched this session):
  - TBM ansatz: Harrison–Perkins–Scott — [hep-ph/0202074](https://arxiv.org/abs/hep-ph/0202074)
  - A4 model: Altarelli–Feruglio — [hep-ph/0504165](https://arxiv.org/abs/hep-ph/0504165); review [arXiv:1002.0211](https://arxiv.org/abs/1002.0211)
  - Lam's residual-symmetry argument that S4 is the minimal group for TBM — [arXiv:0804.2622](https://arxiv.org/abs/0804.2622)
  - King–Luhn, "Neutrino mass and mixing with discrete symmetry", Rept. Prog. Phys. 76 (2013) 056201 — [arXiv:1301.1340](https://arxiv.org/abs/1301.1340)
  - Xing, Phys. Rept. 854 (2020) — [arXiv:1909.09610](https://arxiv.org/abs/1909.09610)
  - Feruglio–Romanino, RMP 93 (2021) — [arXiv:1912.06028](https://arxiv.org/abs/1912.06028)

Pattern values for sin²θ12, and pulls against NuFIT 6.1's sin²θ12 = 0.3096 +0.0057/−0.0073 (computed here, using sin²θ13 = 0.02215):

| Pattern | Group / origin | LO prediction | sin²θ12 | Pull vs 0.3096 | Status |
|---|---|---|---|---|---|
| TBM | A4, S4 (Z3 × [Z2×Z2]) | s²12 = 1/3, s²23 = 1/2, θ13 = 0 | 0.3333 | +4.2σ | dead at LO (θ13 = 0, and now θ12 too) |
| TM1 | S4 with residual Z2 = SU; CSD(3) | TBM column 1 kept | 0.3182 | +1.5σ | alive; JUNO precision ~0.003 is the test |
| TM2 | A4/S4 with residual Z2 = S | TBM column 2 kept | 0.3409 | +5.5σ | excluded |
| Golden ratio GR1 | A5 | tan θ12 = 1/φ | 0.2764 | −4.5σ | bare pattern excluded |
| Golden ratio GR2 | D10 | cos θ12 = φ/2 | 0.3455 | +6.3σ | excluded |
| Bimaximal | S4 (other residuals) | θ12 = θ23 = 45° | 0.5 | ≫ 10σ | only with large charged-lepton corrections |

- μ–τ reflection symmetry (Harrison–Scott, CP-generalised) predicts θ23 = 45° and δ = ±90°. NuFIT 6.0 NO best fits (θ23 = 43.3° with δ = 212°, or 48.5° with δ = 177°) sit ~1–2σ away, and it is allowed within 3σ — [NuFIT 6.0 table](https://arxiv.org/pdf/2410.05380) (inference from the ranges).

### Inferences
- **The structural point for the lattice model.** In the direct approach, the group generated by the charged-lepton residual symmetry T (order 3) and the neutrino residual Klein group {S, U} is exactly S4 ≅ O, and its 3-dim irrep is the cube's vector representation. Since O_h = O × {E, inversion}, the model's T1u triplet restricts to O as the vector triplet (the 3 of S4 in a Cartesian basis). In that basis:
  - T is the C3 rotation that cyclically permutes x → y → z (body diagonal (111)). Its eigenbasis is the Z3 Fourier ("trimaximal", Cabibbo–Wolfenstein) matrix.
  - The neutrino Z2s are C2 rotations of the cube. U is the μ–τ exchange, a C2 about a face diagonal (0,1,−1).
  - TBM follows when the charged-lepton mass matrix is Z3 (C3) invariant and the neutrino mass matrix is invariant under the two C2's that commute into a Klein group.

  A texture built only from E_g/Z3 structure fixes the Z3 residual, but it does *not* impose the neutrino-side C2 invariance. So the mixing it produces is either the bare trimaximal matrix (all |U_αi|² = 1/3 ⇒ θ12 = θ23 = 45°, sin²θ13 = 1/3 i.e. θ13 = 35.3° — badly excluded) or unconstrained. The expected cure within O_h is to make the neutrino (Majorana) mass matrix invariant under a C2 (TM1) or a Klein subgroup (TBM + corrections) of O. In an O_h lattice that is a *different* residual subgroup from the one governing the charged leptons (E_g/Z3).
- Also in the lattice language (inference): E_g is the doublet 2 of S4 (S4 → S3 quotient), which is why it carries only Z3/S3 information and cannot by itself produce 3×3 mixing with a preserved column.
- A semi-direct/TM1 route predicts sin²θ12 = 0.318 and a (θ23, δ) correlation. If JUNO pushes sin²θ12 below ~0.31 with ±0.003 errors, TM1 dies at > 3σ. This is a near-term falsifier any O-based construction inherits.

### Gaps
- No review-level fetch of how many S4 / Δ(6n²) semi-direct (CP + flavour) models survive NuFIT 6.x. The table above is my own pattern arithmetic.
- The Ardakanian claim (Z3 failure ⇒ A4 minimal) is from a non-refereed single-author preprint. Its logic matches standard lore, but its numbers are unverified.

---

## Q3. Koide-type relations for neutrinos (Brannen etc.)

### Takeaway
Brannen's 2006 neutrino Koide sets Q = 2/3 with phase δ_ν = 2/9 + π/12 (the charged-lepton phase plus 15°) and a negative √m1. It predicts NO with m ≈ (0.38, 8.9, 50.7) meV and Σ = 0.060 eV. The scale-free ratio Δm²21/Δm²31 = 0.0308 is now 1.9σ above data (computed here), and the absolute masses fitted in 2006 are 2.9–3.6σ off current splittings. The relation is not dead, but it is under growing pressure from JUNO.

### Cited Findings
- Brannen: √m_νg = 0.1000(26) √eV × [1 + √2 cos(2gπ/3 + π/12 + 2/9)]. The charged-lepton phase is 2/9, and the neutrino phase is 2/9 + π/12. The smallest √m is taken negative. Predicted (2006): m1 = 0.00038 eV, m2 = 0.0089 eV, m3 = 0.0507 eV — [Brannen, APS/JPS 2006 talk](https://indico.phys.hawaii.edu/event/3/contributions/1662/attachments/943/1138/jpp06_DensMat.pdf); [ADS abstract](https://ui.adsabs.harvard.edu/abs/2006APS..NWS.B3014B/abstract); [summary blog](https://washparkprophet.blogspot.com/2011/03/standard-model-still-probably-broken.html)
- Koide's Z3-symmetric (√m = μ[1 + √2 cos(δ + 2πn/3)]) parametrisation applied to quarks and mixings — [arXiv:1301.4143](https://arxiv.org/pdf/1301.4143)
- TBM linked to a relation between neutrino and charged-lepton mass spectra — [hep-ph/0605074](https://arxiv.org/pdf/hep-ph/0605074)
- Koide/circle geometry — [arXiv:1201.2067](https://arxiv.org/pdf/1201.2067)
- Spin path integrals and generations (Brannen) — [arXiv:1006.3114](https://arxiv.org/pdf/1006.3114)
- Another 2026 proposed relation among the mass-squared differences — [arXiv:2601.18781](https://arxiv.org/html/2601.18781v1) (not read in detail)

Brannen's formula evaluated against current data (computed here; formula as cited):

| Quantity | Brannen | Data | Pull |
|---|---|---|---|
| √m_g (√eV) | −0.01958, 0.09440, 0.22518 | — | — |
| Q | 2/3 exactly | — | — |
| Δm²21 | 7.93×10⁻⁵ eV² | JUNO 7.50 ± 0.12 | +3.6σ |
| Δm²31 | 2.571×10⁻³ eV² | NuFIT 6.0 NO 2.513 ± 0.020 | +2.9σ |
| Ratio r = Δm²21/Δm²31 (independent of μ) | 0.0308 | 0.0300 ± 0.0004 | ~+1.9σ |
| Σm_ν | 0.0600 eV | DESI < 0.064 eV | compatible |

### Inferences
- **Direct relevance.** This project already has δ* = 2/9 as the charged-lepton E_g phase (key decision 7). Brannen's neutrino phase is 2/9 + π/12. π/12 = 15° is a natural O_h/Z24-type angle (half of a C12 step, related to the 2π/3 holonomy by a factor 1/8). So if the lattice produces a neutrino phase offset of π/12 relative to the lepton E_g angle, it reproduces Brannen, and must then live with its current ~2σ pressure on r.
- The fixed-phase prediction of r is sharp: a one-parameter scan (δ_ν = 2/9 + x) would find the x that gives r = 0.0300. That is a quick lattice-side check (not done here).
- Brannen predicts only masses, not PMNS. A Koide-type Z3 circulant is diagonalised by the trimaximal matrix, so on its own it gives the wrong mixing (see Q2). This is the same failure mode the project met.

### Gaps
- I did not retrieve the Gerard–Goffinet–Herquet or Rivero(–Gsponer) neutrino-Koide papers. Their exact formulas and current status are unverified here.
- No peer-reviewed 2024–26 assessment of neutrino Koide against NuFIT 6/JUNO was found. The pulls above are my own.

---

## Q4. Mass-generation mechanisms: seesaw I/II/III, inverse/linear, radiative, Dirac vs Majorana, Weinberg operator — and which need no Higgs vev

### Takeaway
Every Majorana mechanism for the *active* neutrinos reduces, at low energy, to the Weinberg operator (LH)(LH)/Λ. That operator needs an SU(2)_L × U(1)_Y-breaking doublet order parameter, but not necessarily an elementary Higgs: a condensate or dynamical EWSB carrying the same quantum numbers suffices. The right-handed Majorana mass M_R is a gauge singlet and needs no EW breaking at all. The Dirac mass m_D = y v and the type-II triplet vev do need EW breaking.

### Cited Findings (primary-literature IDs from my knowledge; not fetched this session — verify before quoting)
- Type-I seesaw: m_ν ≈ −m_D M_R⁻¹ m_Dᵀ (Minkowski 1977; Gell-Mann–Ramond–Slansky; Yanagida; Mohapatra–Senjanović 1980). Type II: m_ν = y_Δ v_Δ with v_Δ ≈ μ v²/M_Δ² (scalar triplet). Type III: fermion triplets Σ. Inverse seesaw: m_ν ≈ m_D M⁻¹ μ Mᵀ⁻¹ m_Dᵀ, with small lepton-number-breaking μ. Linear seesaw: m_ν ∝ m_D M⁻¹ m_Lᵀ + transpose. Radiative: Zee (1980, one loop, charged singlet + second doublet), Zee–Babu (two loop), scotogenic (Ma 2006, [hep-ph/0601225](https://arxiv.org/abs/hep-ph/0601225); inert doublet + Z2, dark-matter link). Reviews: [Xing arXiv:1909.09610](https://arxiv.org/abs/1909.09610); [King–Luhn arXiv:1301.1340](https://arxiv.org/abs/1301.1340)
- Minimal Zee–Wolfenstein model predicts near-bimaximal θ12 and is excluded by solar data (e.g. He, [hep-ph/0307172](https://arxiv.org/abs/hep-ph/0307172)); the general Zee model survives.
- Dirac vs Majorana: the only direct probe is 0νββ, which is not observed (KamLAND-Zen m_ββ < 28–122 meV, [arXiv:2406.11438](https://arxiv.org/abs/2406.11438)). For NO with small m1, m_ββ can even vanish through Majorana-phase cancellation (standard result).
- Littlest seesaw (type-I, two RH ν, CSD(3)) is the most predictive minimal type-I realisation of TM1 — [arXiv:1512.07531](https://arxiv.org/pdf/1512.07531)

### Inferences
- **Higgs-free compatibility map for the lattice model:**
  - *M_R (singlet Majorana).* Needs no EW breaking and fits the existing per-generation Higgs-free Majorana. It can come from a lepton-number-breaking condensate (ν_R ν_R ⟨…⟩, majoron-type) or directly from lattice structure.
  - *m_D.* Needs a doublet order parameter. In this model that role is played by hypercharge-on-U(x) plus whatever condensate gives the charged leptons their mass. Type-I is then fully "Higgs-free" provided the same condensate sources m_D.
  - *Type II.* Needs a Y = 1 triplet vev. It must be a composite/induced triplet order parameter, and is constrained by ρ ≈ 1 (v_Δ ≲ few GeV).
  - *Inverse/linear.* Attractive when a small μ comes from a symmetry being almost unbroken, e.g. a weakly broken lattice Z_n. They allow TeV-scale M.
  - *Radiative (Zee/scotogenic).* Need extra scalars, which are awkward in a Higgs-free framework unless those scalars are composites.
- The mixing lives in whichever matrix carries the flavour symmetry. In the type-I direct approach, TBM/TM1 come from m_D alignments (CSD) with M_R diagonal, or from M_R structure with m_D ∝ 1. The project's failed 3×3 seesaw used the E_g texture. The literature's successful minimal pattern (littlest seesaw) instead puts the flavour structure into m_D *column alignments*: (0,1,1) and (1,n,n−2) with n = 3. That is a concrete alternative target.

### Gaps
- No 2024–26 source was fetched specifically on dynamical/condensate generation of the Weinberg operator (e.g. top-condensate or technicolor neutrino-mass models). This remains a literature gap in these notes.

---

## Q5. Modular flavour symmetry and quark–lepton complementarity

### Takeaway
Modular flavour models (Γ3 ≅ A4, Γ4 ≅ S4, Γ5 ≅ A5; Feruglio 2017) are the most active 2024–26 flavour-model programme. Fits to NuFIT 6.0/6.1 are routine, and near fixed points (τ = i, ω, i∞) they reproduce TM1-like patterns. There is a direct JUNO-precision confrontation paper. Quark–lepton complementarity (θ12 + θC = 45°) is excluded as an exact relation: θ12 + θC ≈ 46.8° ± 0.35° is ~5σ from 45° (computed here).

### Cited Findings
- Recent papers:
  - Modular mixing confronted with JUNO precision — [PRD, "Modular mixing in light of precision measurement in JUNO"](https://journals.aps.org/prd/abstract/10.1103/xv4x-gly8) (details not fetched)
  - Fixed-point predictions for masses, mixing and leptogenesis, fitted to NuFIT 6.1 — [arXiv:2604.04585](https://arxiv.org/html/2604.04585)
  - Level-4 (S4) modular symmetry selected from quark/lepton mass patterns — [arXiv:2609.09262](https://arxiv.org/pdf/2609.09262)
  - Modular S4/A4 fixed points — [arXiv:1910.03460](https://arxiv.org/html/1910.03460)
  - TM1 with two modular S4 groups — [arXiv:1908.02770](https://pith.science/paper/1908.02770)
  - Oscillation-experiment tests of modular models — [arXiv:2305.08576](https://arxiv.org/pdf/2305.08576)
  - Review: Kobayashi–Tanimoto, IJMPA 39, 2441012 (2024) (cited in search listing)
- Origin: Feruglio, "Are neutrino masses modular forms?", [arXiv:1706.08749](https://arxiv.org/abs/1706.08749) (ID from knowledge)
- In the cusp limit (Im τ → ∞), modular A4 degenerates into residual-Z3 behaviour with the Z3 pathology — [arXiv:2603.21264](https://arxiv.org/html/2603.21264)

### Inferences
- QLC arithmetic: θ12 = 33.81° from sin²θ12 = 0.3096 (NuFIT 6.1), plus θC ≈ 13.04°, gives 46.85°. With σ(θ12) ≈ 0.35°, that is ~5σ from 45° (computed here). QLC survives only as an approximate relation with O(1°) corrections.
- For the lattice: modular Γ4 ≅ S4 ≅ O is the modular group whose finite quotient is exactly the cube's rotation group. A lattice analogue of "τ near a fixed point" would be the E_g-plane angle choosing a stabiliser inside O. A residual-Z3 stabiliser (τ = ω) is the charged-lepton-like case. A residual-Z2 stabiliser (τ = i) is the neutrino/TM1-like case.

### Gaps
- No full numeric table of best-fit modular S4 models vs NuFIT 6.x was obtained. The JUNO-modular PRD was not read.

---

## Q6. Sterile neutrinos (light and keV)

### Takeaway
The light (eV-scale) sterile-neutrino explanation of the short-baseline anomalies has been largely excluded, so any lattice extra singlet should be heavy or very weakly mixed:
- MicroBooNE (Nature, Dec 2025) excludes the single 3+1 sterile interpretation of LSND/MiniBooNE at 95% CL.
- KATRIN (Nature, Dec 2025) excludes most of the reactor/gallium-anomaly parameter space at Δm² ~ few–hundreds eV².

### Cited Findings
- MicroBooNE used BNB + NuMI beams in one LArTPC, which breaks the νe appearance/disappearance degeneracy. It excludes the single light sterile ν interpretation of LSND and MiniBooNE at 95% CL and a notable part of the gallium-anomaly region. Nature 648, 64 (2025); [arXiv:2512.07159](https://arxiv.org/abs/2512.07159); [Fermilab news](https://news.fnal.gov/2025/12/microboone-finds-no-evidence-for-a-sterile-neutrino/)
- KATRIN, 259 days: sterile search sensitive to Δm²41 from a few to several hundred eV². Together with reactor experiments it now consistently rules out light steriles with noticeable active mixing, including much of the reactor/gallium-anomaly space. Nature 2025; [arXiv:2503.18667](https://arxiv.org/pdf/2503.18667); [MPIK news](https://www.mpi-hd.mpg.de/mpi/en/public-relations/news/news-item/katrin-tightens-the-net-around-the-elusive-sterile-neutrino)
- Residual MicroBooNE–MiniBooNE tension in 3+1 fits is still being studied — [arXiv:2603.15322](https://arxiv.org/pdf/2603.15322); [arXiv:2503.13594](https://arxiv.org/pdf/2503.13594)

### Inferences
- The MiniBooNE low-energy excess itself remains unexplained, but it is no longer a 3+1-oscillation argument. A lattice model does not need, and should not predict, an eV-scale sterile state with |U_e4|² ~ 10⁻².

### Gaps
- keV sterile-neutrino dark matter (X-ray 3.5 keV line status, Lyman-α and phase-space bounds, 2024–26) was **not researched in this pass**. No sourced statement is available here.
- The gallium anomaly (BEST) is not fully resolved by these results; its current interpretation was not fetched.
