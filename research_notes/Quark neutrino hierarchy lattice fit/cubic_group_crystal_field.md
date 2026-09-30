# Cubic/octahedral flavour groups, crystal-field splitting, and extending the Koide mechanism to quarks and neutrinos

*Research notes, 2026-09-24 - 00:00. Scope: O ≅ S4, O_h = O × Ci, subgroups (T ≅ A4, D4, D3 ≅ S3, D2h, C3v, Z3), double covers (2O, 2T = T'), crystal-field analogies, circulant/Koide parametrisation of quarks and neutrinos.*

**Labels used below:** **[GT]** = established group theory (textbook, or checked numerically in scratch this session). **[LIT]** = a model proposal or empirical observation from the literature. **[CALC]** = my own numerical calculation this session (scripts are in the session scratchpad, not in the repo). **[INF]** = inference for the BCC/T1u/E_g model.

**Convention.** I write √m_k = μ[1 + c·cos(δ + 2πk/3)]. This gives Q = Σm/(Σ√m)² = (1 + c²/2)/3, so Q = 2/3 ⇔ c = √2. Brannen and Żenczykowski write c = √2·k (or 2η), so k = 1 (η² = ½) is the Koide point. For each triplet I fit (c, δ) exactly by a discrete Z3 Fourier transform of (√m_heavy, √m_light, √m_middle). This ordering puts δ in the small positive branch, as for leptons.

---

## Q1. S4/O flavour models: generation irreps, flavon alignments, and how S4's 3⊗3 maps onto O_h's T1u⊗T1u

### Takeaway
S4 is the rotation group O of the cube. Its 3 and 3′ are the T1 and T2 irreps (which label is "3" depends on the author's basis). In the literature, generations usually sit in a triplet, with the doublet E and the triplets carried by flavons. S4's 3⊗3 = 1+2+3+3′ is exactly O_h's T1u⊗T1u = A1g+Eg+T1g+T2g. The symmetric part is A1g+Eg+T2g (6 dimensions); the antisymmetric part is T1g (3 dimensions). So a Hermitian 3×3 mass matrix on a T1u triplet contains exactly one E_g doublet, and dim(Eg)/dim(T1u⊗T1u) = 2/9 is a statement about this decomposition.

### Cited findings
- **[LIT]** Lam showed that tri-bimaximal (TBM) lepton mixing uniquely picks S4 (the permutation group of four objects, i.e. the symmetry group of the cube/octahedron) as the minimal horizontal symmetry. If mixing is exactly TBM, the minimal unbroken horizontal group is S4, not A4. — [Lam, arXiv:0809.1185, PRD 78, 073015 (2008)](https://arxiv.org/abs/0809.1185)
- **[LIT]** Related papers: "S4 as a natural flavor symmetry for lepton mixing" ([arXiv:0811.0345](https://arxiv.org/abs/0811.0345)); "Is S4 the horizontal symmetry of tri-bimaximal lepton mixing?" ([arXiv:0906.2689](https://arxiv.org/pdf/0906.2689)); a minimal-seesaw realisation of TBM with S4 ([arXiv:1106.2715](https://arxiv.org/pdf/1106.2715)); Lam's "bottom-up analysis of horizontal symmetry" ([arXiv:0907.2206](https://arxiv.org/html/0907.2206)).
- **[LIT]** Hagedorn–Lindner–Mohapatra built an extension of the Standard Model in which a spontaneously broken S4 fixes the flavour structure of both quarks and leptons, embedded in a SUSY SO(10) "GUT of flavour". — [arXiv:hep-ph/0602244](https://arxiv.org/html/hep-ph/0602244)
- **[LIT]** The standard reference for character tables, tensor products and breaking patterns of S_N, A_N, T′, D_N, Q_N, Σ(2N²), Δ(3N²), T7, Σ(3N³) and Δ(6N²), with A4/S4/Δ(54) flavour models, is Ishimori, Kobayashi, Ohki, Okada, Shimizu, Tanimoto, Prog. Theor. Phys. Suppl. 183 (2010). — [arXiv:1003.3552](https://arxiv.org/abs/1003.3552)
- **[LIT]** King–Luhn's review (Rept. Prog. Phys. 76, 056201, 2013) covers flavon vacuum alignment and model-building strategies, including SU(5)×A4, SU(5)×S4 and SU(5)×Δ(96) examples that cover quarks. — [arXiv:1301.1340](https://arxiv.org/abs/1301.1340)
- **[GT]** O ≅ S4 has irreps A1, A2, E, T1, T2 (dimensions 1, 1, 2, 3, 3), corresponding to S4's 1, 1′, 2, 3, 3′. O_h = O × {E, i} doubles each into g/u. T1u is the polar vector (x, y, z), i.e. the nearest-neighbour shell direction set. T1u⊗T1u = A1g ⊕ Eg ⊕ T1g ⊕ T2g. Sym² = A1g (x²+y²+z²) ⊕ Eg (2z²−x²−y², √3(x²−y²)) ⊕ T2g (yz, zx, xy). Λ² = T1g (axial vector). — standard. For the orbital version (d orbitals = Eg ⊕ T2g; p = T1u) see [UCSD Physics 220 group-theory notes, ch. 6](https://courses.physics.ucsd.edu/2018/Spring/physics220/LECTURES/CH06.pdf) and [LibreTexts correlation diagrams](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Inorganic_Chemistry_(LibreTexts)/11:_Coordination_Chemistry_III_-_Electronic_Spectra/11.03:_Electronic_Spectra_of_Coordination_Compounds/11.3.02:_Correlation_Diagrams)
- **[GT]** Restricting S4 → A4 (O → T) gives 3 → 3, 3′ → 3, 2 → 1′ ⊕ 1″, 1′ → 1. The E doublet of S4 becomes the pair of complex A4 singlets 1′, 1″. These carry charge ω, ω² under the Z3 = C3[111], so an E_g vev at angle θ is a pair of Z3-charged singlet vevs with relative phase e^{±iθ}. — follows from the restriction; tensor-product tables in [arXiv:1003.3552](https://arxiv.org/abs/1003.3552)

### Inferences
- **[INF]** This is the dictionary for the BCC model. "Generations = T1u" corresponds to "generations in S4's 3 (or 3′)". "E_g condensate" corresponds to "S4 doublet flavon φ_2". "T2g condensate" corresponds to "3′ flavon" and "T1g" to the antisymmetric 3. In the S4 literature, the doublet flavon is the object that splits the charged-lepton masses diagonally, and the triplet flavons are what align the neutrino sector. The model's E_g-on-second-shell is therefore the lattice analogue of the standard S4 doublet flavon.
- **[INF] Exact statement, verified in [CALC].** The mass matrix A1g + Eg, diagonal in the cubic (x, y, z) basis, has entries a + b·cos(θ + 2πk/3) (k = x, y, z), where θ is the E_g-plane angle. The Koide/Brannen form is therefore literally "A1g + Eg on a T1u triplet", with δ equal to the E_g angle. The Koide condition Q = 2/3 is equipartition: in √M, ‖A1g component‖² = ‖Eg component‖². At δ = 2/9 I checked both norms equal 3.000 to machine precision. This is the Hilbert-space form of Foot's "45° between (√m_i) and (1,1,1)". — [Foot, hep-ph/9402242](https://arxiv.org/pdf/hep-ph/9402242v1); [Wikipedia: Koide formula](https://en.wikipedia.org/wiki/Koide_formula)
- **[INF]** The E⊗E⊗E → A1 cubic invariant is ∝ cos 3θ. So the only O_h-invariant function of the E_g angle at cubic order is cos 3δ. That explains why 3δ-relations, and the model's cos(2/3) = cos 3δ*, are the natural invariants. It also means lattice potentials see δ only modulo 2π/3 and up to reflection.

### Gaps
- I did not fetch the S4 papers' explicit Clebsch tables or their 3-vs-3′ basis conventions. Which physical generation (L, e^c, ν^c) sits in 3 vs 3′ differs between Ma, Hagedorn–Lindner–Mohapatra, Bazzocchi–Merlo–Morisi and King–Luhn. Check the individual papers before claiming a specific assignment.
- The authorship of 0811.0345 and 0906.2689 was not verified in this session. From memory they are Bazzocchi–Morisi and Grimus–Lavoura–Ludl respectively; verify before citing.

---

## Q2. Residual symmetries as "different crystal-field distortions per sector"; what trigonal, tetragonal and orthorhombic distortions of an O_h triplet produce

### Takeaway
Crystal-field group theory settles the degeneracy patterns. A tetragonal [001] (D4h) or trigonal [111] (D3d) distortion splits T1u only as 1+2. A full 1+1+1 split needs orthorhombic D2h or lower. In E_g language, a generic E_g vev breaks O_h → D2h, and the tetragonal points are θ = 0, ±2π/3. So δ* = 2/9 measures the orthorhombic departure from a tetragonal distortion. TBM arises from S4 when the charged-lepton sector keeps Z3 = C3[111] (trigonal) and the neutrino sector keeps a Klein group {C2x, C2′[011]}. I checked this explicitly in the cubic basis. A charged-lepton sector with cubic-axis D2h residual symmetry (the plain E_g-diagonal picture) cannot get TBM from any O_h residual subgroup on the neutrino side.

### Cited findings
- **[GT] Crystal-field correlation (Bethe 1929 / Koster et al. 1963 tables):**

  | O_h irrep | D4h ([001]) | D3d ([111]) | D2h (cubic axes) |
  |---|---|---|---|
  | T1u (x,y,z) | A2u + Eu | A2u + Eu | B1u + B2u + B3u |
  | Eg | A1g + B1g | Eg | 2 Ag |
  | T2g | B2g + Eg | A1g + Eg | B1g + B2g + B3g |
  | T1g | A2g + Eg | A2g + Eg | B1g + B2g + B3g |

  Sources: [LibreTexts correlation diagrams](https://chem.libretexts.org/Bookshelves/Inorganic_Chemistry/Inorganic_Chemistry_(LibreTexts)/11:_Coordination_Chemistry_III_-_Electronic_Spectra/11.03:_Electronic_Spectra_of_Coordination_Compounds/11.3.02:_Correlation_Diagrams); [UMass Jahn–Teller notes](https://alpha.chem.umb.edu/chemistry/ch612/documents/JahnTeller_000.pdf); [UCSD Physics 220 ch. 6](https://courses.physics.ucsd.edu/2018/Spring/physics220/LECTURES/CH06.pdf).

  **Caution:** the web-search summary I got misstated two entries (it gave T1u→B2u+Eu in D2h and T2g→B2g+Eg in D3d). The table above is the correct textbook result, which I re-derived: in D2h every cubic axis is its own 1-D irrep; in D3d the [111]-symmetric xy+yz+zx is invariant, so it is A1g.
- **[GT] Which O_h components realise each distortion on a triplet mass matrix:**
  - Tetragonal/orthorhombic distortions are **E_g**. They are diagonal in the cubic basis.
  - The trigonal [111] distortion is the **T2g** component along (1,1,1), i.e. all off-diagonals equal. That is the democratic matrix: eigenvalues a+2t, a−t, a−t, with eigenvector (1,1,1)/√3.
  - A Hermitian but complex matrix can also carry **T1g** (i × a real antisymmetric matrix). T1g along [111] is time-reversal odd and axial.
- **[CALC]** Rotate the E_g-diagonal Koide matrix (a=1, c=√2, δ=2/9) by the Z3 Fourier (trimaximal) matrix F. The result is the Hermitian circulant M = a·1 + bP + b*P², where P is cyclic permutation (C3 about [111]). Its parameters are |b|/a = 0.70711 = 1/√2 and arg b = 0.22222 = 2/9. Its real symmetric off-diagonal part is 0.68972 (the T2g[111] trigonal component); its imaginary antisymmetric part is 0.15584 (the T1g[111] axial component). **tan δ = T1g/T2g = 0.15584/0.68972 = tan(2/9).**

  So the same Koide spectrum has two pictures:
  - (a) E_g angle δ in the cubic-diagonal picture, with residual D2h and the cubic axes as mass eigenstates;
  - (b) the ratio of axial to polar trigonal distortion along [111], with residual Z3 = C3[111] and trimaximal mass eigenstates.
- **[LIT]** Lam showed TBM follows from residual symmetries, with S4 the minimal group. Standard construction: G_ℓ = Z3 (generator T), G_ν = Z2×Z2 (generators S, U). — [arXiv:0809.1185](https://arxiv.org/abs/0809.1185); review in [King–Luhn 1301.1340](https://arxiv.org/abs/1301.1340)
- **[CALC] TBM in cubic language.** Take the cubic (x, y, z) basis, with T = cyclic permutation = C3[111], S = diag(1,−1,−1) = C2x, and U = −(y↔z) = C2′ about [0,1,−1] (as a T1 matrix). The common eigenbasis of {S, U} is {x, (y+z)/√2, (y−z)/√2}. Its overlap with F gives |U|² columns (1/3,1/3,1/3), (2/3,1/6,1/6) and (0,1/2,1/2): exactly TBM up to column order.

  So the neutrino residual group is the rhombic D2 with principal axes x, [011], [01̄1], a subgroup of the tetragonal D4 around x. It is **not** the cubic-axis D2 = {C2x, C2y, C2z}. With that choice (G_ℓ = Z3[111], G_ν = cubic D2) the mixing is F itself, all |U|² = 1/3, which is excluded.
- **[LIT] Earliest crystal-field-style mechanism.** Harari–Haut–Weyers (1978) gave all same-charge quarks identical Yukawas ("democratic", S3_L×S3_R symmetric) in an SU(2)_L×SU(2)_R×U(1) model. They got tan²θ_C = m_d/m_s and θ_C ≈ 15°. — [Phys. Lett. B78 (1978) 459, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0370269378904859); [OSTI record](https://www.osti.gov/etdeweb/biblio/6222628). Later democracy-breaking work: [arXiv:1705.01391](https://arxiv.org/html/1705.01391), [arXiv:1608.08988](https://arxiv.org/html/1608.08988).
- **[LIT]** Papers exist that explicitly draw the analogy between finite flavour groups and crystallographic/molecular point groups: e.g. [hep-ph/9409330 "Simple non-Abelian finite flavor groups and fermion masses"](https://arxiv.org/pdf/hep-ph/9409330), [hep-ph/0005249 "Discrete flavor symmetries and mass matrix textures"](https://arxiv.org/pdf/hep-ph/0005249), [1110.6376 "Finite flavour groups of fermions"](https://arxiv.org/pdf/1110.6376). I found no paper that frames flavour breaking as a Jahn–Teller / crystal-field distortion of an O_h triplet on a lattice.

### Inferences
- **[INF] Key structural point for the model.** Taken literally, "E_g condensate, diagonal in cubic axes" makes the charged-lepton mass basis the cubic axes, with residual D2h. Then no O_h residual group on the neutrino side gives TBM-like mixing:
  - neutrino Z3[111] → trimaximal, excluded;
  - neutrino rhombic D2 → only 2–3 maximal, excluded;
  - neutrino cubic D2 → no mixing.

  To reproduce lepton mixing the model needs one of two things. Either (b): the charged-lepton E_g realised as a [111] T2g+T1g circulant, so the charged-lepton residual group is C3[111]. Or: accept that the lepton mixing comes from something other than residual O_h subgroups (the mass-matrix mismatch between the charged-lepton and neutrino condensates). Picture (b) makes δ* = arctan(T1g/T2g) along [111] rather than an E_g-plane angle. This is a genuine fork in the model's interpretation of δ*.
- **[INF]** Per-sector distortion menu:
  - trigonal [111] (T2g real) alone → democratic 1+2 spectrum, with the heavy state along (1,1,1): the Harari–Haut–Weyers top/bottom-dominance picture;
  - tetragonal (E_g at θ = 0 mod 2π/3) → 1+2 with cubic-axis eigenstates;
  - orthorhombic (generic E_g) → 1+1+1 with cubic-axis eigenstates;
  - trigonal with an axial admixture (T2g+T1g along [111]) → 1+1+1 Koide-circulant with trimaximal eigenstates.

  Quark hierarchies (m_t ≫ m_c ≫ m_u) are closest to "nearly democratic": c close to 2, see Q3.

### Gaps
- I found no paper that uses O_h's E_g/T2g/T1g crystal-field decomposition explicitly as the flavon basis for leptons and quarks together. The closest are the S4 doublet/triplet flavon models. "Crystal-field flavour" as a named programme does not appear to exist in the literature I found.
- I did not verify the Wilczek–Zee early family-symmetry papers or Ma's A4 "tetrahedral" paper (from memory: Ma–Rajasekaran, hep-ph/0106291). Verify before citing.

---

## Q3. Circulant/Koide parametrisation of quarks: what (c, δ) the up and down quarks need, and any pattern relating the lepton phase 2/9 to quark phases

### Takeaway
Charged leptons sit at c = √2 and δ = 2/9 to about 10⁻⁶. Quarks need c ≈ 1.76 (up) and c ≈ 1.55 (down), i.e. k = c/√2 ≈ 1.24 and 1.09, which is further from the Koide point at higher scales. Żenczykowski (2012–13) observed that at low energy the phases take δ_U ≈ 2/27 = δ_L/3 and δ_D ≈ 4/27 = 2δ_L/3. My fit reproduces δ_U = 0.0745 (vs 2/27 = 0.0741) with top pole + m_c(m_c) + m_u(2 GeV). But δ_D is strongly scheme-dependent: 0.110 with PDG m_s(2 GeV), and it reaches 4/27 only with a large low-energy m_s ≈ 160 MeV. Rivero and Rodejohann–Zhang found Koide Q ≈ 2/3 for the heavy triplet (c,b,t) and for (−√s, c, b).

### Cited findings
- **[LIT]** Brannen's parametrisation: the square root of the charged-lepton mass matrix is the circulant Γ(μ, η, δ) with eigenvalues μ(1 + 2η cos(δ + 2nπ/3)). Fitting gives η² ≈ ½ and δ₁ = 0.22222204717(48) (from AMU data), versus 2/9 = 0.2222222. The 2nπ/3 comes from the circulant eigenvectors; the rational δ comes from the operator. — [Brannen, "The Lepton Masses" (2006), brannenworks.com/MASSES2.pdf](https://brannenworks.com/MASSES2.pdf)
- **[LIT]** Żenczykowski: the Koide phases δ_L = 3δ_D/2 = 3δ_U = 2/9 are "possibly exact" at the low-energy scale.
  - k_L = 1. At µ = 2 GeV, k_D ≈ 1.08 and k_U ≈ 1.25; at M_Z, k_D = 1.12 and k_U = 1.29.
  - At M_Z the charged-lepton k_L and δ_L deviate from 1 and 2/9 by about 0.2% and 0.5%. He concludes that the explanation should not be sought at a high (GUT) scale.
  - The representative low-energy masses consistent with δ_D = 4/27 and δ_U = 2/27 (in MeV) are m_d = 7.843, m_s = 160.0, m_b = 4209, m_u = 4.392, m_c = 1296, m_t = 172000.
  - Following Gérard–Goffinet–Herquet, he conjectures that k_D = k_U = 1 holds in the *weak* basis for "pseudo-masses", with CKM = U_U†U_D in Fritzsch–Xing form. This works with k_D = k_U = 1.015, giving θ ≈ 2.44° vs 2.37° measured. His Fritzsch–Xing angles are θ_u = 4.87° ± 0.23°, θ_d = 12.11° ± 0.47°, θ = 2.37° ± 0.05°.

  — [Żenczykowski, arXiv:1301.4143](https://arxiv.org/abs/1301.4143) (full text read). Earlier phase observation: P. Żenczykowski, PRD 86, 117303 (2012), [arXiv:1210.4125](https://arxiv.org/abs/1210.4125) (cited via [Wikipedia](https://en.wikipedia.org/wiki/Koide_formula)). Gérard, Goffinet, Herquet, PLB 633 (2006) 563 (cited in 1301.4143; arXiv ID not verified).
- **[LIT]** Rodejohann–Zhang: Koide does not hold for (u,c,t) or (d,s,b), but may hold for the light triplet (u,d,s) and the heavy triplet (c,b,t) separately. Light neutrinos cannot obey it directly without modification. — [arXiv:1101.5525, PLB 698 (2011) 152](https://arxiv.org/abs/1101.5525)
- **[LIT]** Rivero: with a negative sign on √m_s, (s, c, b) forms a Koide tuple (Q ≈ 0.675). This continues the (c, b, t) tuple and is "quasi-orthogonal" to the lepton triplet. — [arXiv:1111.7232](https://arxiv.org/abs/1111.7232); Q value from [Wikipedia](https://en.wikipedia.org/wiki/Koide_formula). A chained-triplet top-mass prediction (≈173.26 GeV) is attributed on Wikipedia to follow-up work ([Cao, arXiv:1205.4068](https://en.wikipedia.org/wiki/Koide_formula)).
- **[CALC] Fits.** Inputs are my recollection of PDG-2024 central values, not re-fetched: m_u = 2.16, m_d = 4.70, m_s = 93.5 MeV (MS-bar, 2 GeV); m_c(m_c) = 1.273 GeV; m_b(m_b) = 4.183 GeV; m_t = 172.57 GeV (pole) or 162.5 GeV (MS-bar); M_Z-scale values ≈ Huang–Zhou 2021. See the [PDG quark summary](https://pdg.lbl.gov) for current values.

  | Triplet / scheme | Q | c (Koide = √2 = 1.41421) | k = c/√2 | δ (rad) | 3δ |
  |---|---|---|---|---|---|
  | e, μ, τ (pole) | 0.666660 | 1.41420 | 1.00000 | **0.222230** | 0.66669 |
  | up: t pole, c(m_c), u(2 GeV) | 0.8488 | 1.7586 | 1.2435 | **0.07452** (2/27 = 0.07407) | 0.2236 |
  | up: t MS-bar(m_t), same c, u | 0.8449 | 1.7520 | 1.2389 | 0.07689 | 0.2307 |
  | up @ M_Z (u 1.23, c 620, t 168260 MeV) | 0.8876 | 1.8236 | 1.2895 | 0.05183 | 0.1555 |
  | down: b(m_b), s, d (2 GeV) | 0.7313 | 1.5452 | 1.0926 | **0.1101** (1/9 = 0.1111; 4/27 = 0.1481) | 0.3304 |
  | down @ M_Z (d 2.67, s 53.16, b 2839 MeV) | 0.7481 | 1.5775 | 1.1154 | 0.1000 | 0.3001 |
  | (c, b, t): c(m_c), b(m_b), t pole | 0.6692 | — | — | — | — |
  | (−√s, c, b) (PDG values above) | 0.6748 | — | — | — | — |

  My k values reproduce Żenczykowski's k_U ≈ 1.25, k_D ≈ 1.08–1.09 (2 GeV) and 1.29 / 1.12 (M_Z), which cross-checks the fit.

### Inferences
- **[INF]** δ_U ≈ δ*/3 = 2/27 holds to 0.6% in the mixed "natural scale" scheme (top pole) and fails in the uniform M_Z scheme (0.052). Any lattice claim of δ_U = δ*/3 has to name its mass scheme. The same holds for δ_D: 1/9 = δ*/2 (0.9% off) with PDG 2 GeV light masses, and 4/27 = 2δ*/3 only with m_s ≈ 160 MeV. The data cannot currently distinguish δ_D = δ*/2 from 2δ*/3; the discriminator is the low-scale m_s.
- **[INF]** Model reading: in E_g language, all three charged sectors sit near the tetragonal point θ = 0 (δ small), and the quarks have *larger* E_g amplitude than the A1g amplitude (c > √2 ⇒ ‖Eg‖² > ‖A1g‖²). A natural lattice hypothesis: quarks carry an extra E_g contribution, e.g. from colour or a different shell weight, that breaks the singlet–doublet equipartition that gives Q = 2/3. The amplitude ratios needed are ‖Eg‖²/‖A1g‖² = c²/2 ≈ 1.55 (up) and ≈ 1.19 (down) at the mixed scale.

### Gaps
- PDG 2024/2025 quark masses and NuFIT values were used from memory, not re-fetched. Re-run the scratch fit with pinned inputs before promoting any number.
- No paper I found derives δ_U = δ_L/3 or δ_D = 2δ_L/3. They remain empirical observations by a single author.

---

## Q4. Mixing from misalignment: CKM as the relative rotation of two differently distorted bases; Cabibbo-angle predictions

### Takeaway
There are three families of mechanism:
1. **Democratic/texture:** Harari–Haut–Weyers give tan²θ_C = m_d/m_s, which I compute as θ_C = 12.96° (sin = 0.2242 vs |V_us| ≈ 0.2243).
2. **Group-theoretic:** a dihedral D7/D14 broken to different subgroups in the up and down sectors gives θ_C from group data alone; Holthausen–Lim scanned groups up to order 1536.
3. **Koide "pseudo-mass":** Żenczykowski / Gérard et al., where k = 1 holds in the weak basis and CKM = U_U†U_D.

As a numerical coincidence, sin(δ*) = sin(2/9) = 0.2204 (12.73°), 1.8% below |V_us| and within 1.3σ of Żenczykowski's Fritzsch–Xing θ_d = 12.11° ± 0.47°.

### Cited findings
- **[LIT]** Harari–Haut–Weyers 1978: tan²θ_C = m_d/m_s and θ_C ≈ 15° from S3-symmetric ("democratic") Higgs couplings. — [PLB 78 (1978) 459](https://www.sciencedirect.com/science/article/abs/pii/0370269378904859); [OSTI](https://www.osti.gov/etdeweb/biblio/6222628)
- **[LIT]** Blum–Hagedorn–Hohenegger: with SM gauge group and D7 × Z2(aux) flavour symmetry, θ_C is predicted "in terms of group theoretical quantities only". These are the index n of D_n, the representation index j, and the preserved subgroups m_u, m_d in the up and down sectors. D7 is broken to *different* subgroups in each sector. — [arXiv:0710.5061, JHEP 03 (2008) 070](https://arxiv.org/pdf/0710.5061). Follow-up: D14 as a common origin of θ_C and θ₁₃^ℓ — [arXiv:1204.0715](https://arxiv.org/pdf/1204.0715).
- **[LIT]** Holthausen–Lim scanned finite groups of order < 1536 for residual-symmetry mixing. Some groups give only the Cabibbo angle at leading order. With Dirac neutrinos, 4 groups of order ≤ 200 give acceptable quark and lepton angles; (Z18×Z6)⋊S3 is the most predictive by their measure. — [arXiv:1306.4356](https://arxiv.org/abs/1306.4356). Related: "The Cabibbo angle as a universal seed for quark and lepton mixings" [arXiv:1410.3658](https://arxiv.org/abs/1410.3658); unified quark–lepton mixing from flavour + CP symmetries [JHEP02(2018)038](https://link.springer.com/article/10.1007/JHEP02(2018)038) and [PRD 98, 055011](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.055011).
- **[LIT]** Żenczykowski's pseudo-mass scheme (details and numbers in Q3). — [arXiv:1301.4143](https://arxiv.org/abs/1301.4143)
- **[CALC]** Numerical comparison:

  | Quantity | Value | Angle |
  |---|---|---|
  | √(m_d/m_s) (PDG 2 GeV) | 0.22420 | 12.956° |
  | \|V_us\| ≈ 0.2243 (recalled) | 0.2243 | 12.962° |
  | sin(π/14) (Δ(6n²) / D14 value, n = 7) | 0.22252 | — |
  | sin(2/9) | 0.22040 | 12.732° |
  | π/12 | — | 15° |

### Inferences
- **[INF]** The lattice analogue of Blum–Hagedorn–Hohenegger and Holthausen–Lim: up and down quarks see E_g condensates with different angles (δ_U ≠ δ_D), or distortion axes related by an O_h element. Two cases:
  - Both distortions are E_g, diagonal in cubic axes. Then the mass eigenbases coincide and CKM = 1, whatever the angles. Misalignment needs the sectors to differ in which O_h component (E_g vs T2g/T1g) or which axis carries the distortion, not just in the E_g angle.
  - Both are [111] circulants, i.e. picture (b). Then both are diagonalised by the same F and CKM = 1 again.

  So a CKM needs mixed-type distortions, e.g. up ≈ circulant[111] and down ≈ E_g-diagonal. The resulting misalignment is F-like: large, trimaximal. This is the classic reason quark-sector residual-symmetry models need small groups (D_n) or corrections. The small Cabibbo angle suggests both quark sectors share nearly the same residual symmetry and only a small E_g-type angle differs.
- **[INF]** The coincidences sin δ* ≈ |V_us| (1.8% off) and θ_d(FX) ≈ δ* (1.3σ) are suggestive but unforced. Treat them as hypotheses needing a mechanism, not as evidence. The closer (though also scheme-laden) relation is the Gatto-type √(m_d/m_s) ≈ |V_us|.

### Gaps
- I did not get the exact D7 prediction formula from the Blum–Hagedorn–Hohenegger abstract. From memory it is |V_us| = sin(π/14) ≈ 0.2225 from D14 / D7 with 1-D preserved subgroups; unverified. The Δ(6n²) quark-mixing paper (Ishimori–King–Okada–Tanimoto) was seen only as a search listing.
- I did not verify a primary source for Gatto–Sartori–Tonin (1968) sin θ_C ≈ √(m_d/m_s).

---

## Q5. Neutrinos in the circulant language

### Takeaway
Neutrinos do not fit Q = 2/3 with all √m positive. Brannen fits Q = 2/3 by taking the lightest neutrino's √m **negative**, with δ₀ = 0.486(21) (2006 data). This is close to 2/9 + π/12 = 0.4840. With current oscillation data (Δm²₂₁ ≈ 7.42×10⁻⁵ eV², Δm²₃₁ ≈ 2.515×10⁻³ eV², normal ordering, recalled), I find the required δ_ν = 0.4778, 0.006 below 2/9 + π/12. The latter predicts Δm²₃₁ = 2.41×10⁻³ eV², about 4% low, which is a tension at current precision.

### Cited findings
- **[LIT]** Brannen: m₁ + m₂ + m₃ = (2/3)(−√m₁ + √m₂ + √m₃)². Fit: m₁ = 0.000388(46) eV, m₂ = 0.00895(17) eV, m₃ = 0.0507(30) eV, μ₀ = 0.1000(26) eV^½, δ₀ = 0.486(21). Earlier attempts failed because they assumed all √m positive. — [Brannen MASSES2.pdf (2006)](https://brannenworks.com/MASSES2.pdf); [APS NW 2006 abstract](https://ui.adsabs.harvard.edu/abs/2006APS..NWS.B3014B/abstract)
- **[LIT]** Żenczykowski quotes k_ν ≤ 0.81 (with all √m positive) from Rodejohann–Zhang. — [arXiv:1301.4143](https://arxiv.org/abs/1301.4143); [arXiv:1101.5525](https://arxiv.org/abs/1101.5525)
- **[LIT]** Koide's own neutrino work: TBM plus a relation between neutrino and charged-lepton spectra ([hep-ph/0605074](https://arxiv.org/pdf/hep-ph/0605074)); Koide-relation neutrino mass estimate ([hep-ph/0505028](https://arxiv.org/pdf/hep-ph/0505028)); review of charged-lepton mass formula ([0706.2534](https://arxiv.org/pdf/0706.2534)).
- **[CALC]**
  - With all √m positive and m₁ = 0, 0.001, 0.005, 0.01 eV: Q_ν = 0.586, 0.492, 0.419, 0.382. Q_ν ≤ 0.586, so c < √2 and Koide fails, consistent with k_ν ≤ 0.81.
  - Negative-root Brannen form, Q = 2/3 enforced, fit to the oscillation ratio: δ_ν = 0.47784, giving m = (0.00036, 0.00862, 0.05015) eV, Σ = 0.0591 eV.
  - δ = 2/9 + π/12 = 0.48402 gives m = (0.00037, 0.00862, 0.04905) eV and Δm²₃₁ = 2.406×10⁻³ eV².

### Inferences
- **[INF]** A sign flip of one √m eigenvalue is, in the E_g picture, the statement that the lightest √m eigenvalue 1 + √2 cos(δ + 2π/3) is negative, i.e. the lattice √M is not positive-definite. For the charged leptons the smallest eigenvalue √m_e is only just positive at δ = 2/9. Pushing δ past about 0.26 rad flips it. The neutrino phase lies on the other side of that line.
- **[INF]** π/12 is not a natural O_h angle: O_h angles are multiples of π/4 and π/3, so their differences give π/12 = π/3 − π/4. If a neutrino offset were real, a lattice account would have to explain why it is the difference of a 3-fold and a 4-fold rotation angle, e.g. a C4 vs C3 residual-axis mismatch between the charged and neutral sectors. That is speculative, and the 4% Δm² tension counts against the exact π/12.

### Gaps
- Oscillation parameters were recalled, not fetched from NuFIT 6.x. Re-check before quantitative use.
- Neutrinos may be Majorana. A Majorana mass matrix is symmetric, not Hermitian, so it cannot carry the T1g (antisymmetric) component that gives the phase in picture (b). If neutrinos are Majorana, the circulant phase has to come from elsewhere (Rodejohann–Zhang's Majorana-phase route).

---

## Q6. Double groups: 2O / O′ / T′ spinor irreps, and whether generations should carry them

### Takeaway
The O_h double group adds the spinor irreps E½(g,u) (Γ6±, 2-dim), E5/2(g,u) (Γ7±, 2-dim) and G3/2(g,u) (Γ8±, 4-dim). A spin-½ particle in a T1u orbital splits as T1u ⊗ E½ = E½u ⊕ G3/2u (a 2+4 spin–orbit-like split), not into 3 generations. Flavour models do use 2O (as a modular group) and T′ = 2T (its doublets hold the first two quark generations), but as internal flavour groups, not spacetime-locked ones.

### Cited findings
- **[GT]** Binary octahedral group 2O, order 48. It has the 8 irreps of O (via the quotient) plus 3 spinorial irreps of dimension 2, 2 and 4, with Σd² = 24 + 24. In O_h double-group (Bethe/Koster) notation these are E½, E5/2, G3/2, each doubled into g/u. The spin–orbit decomposition T1 ⊗ E½ = E½ ⊕ G3/2 is the crystal-field version of l=1 ⊗ s=½ = j=½ ⊕ j=3/2. — standard (Koster, Dimmock, Wheeler, Statz 1963); I found no web source this session, so it is listed here as textbook GT.
- **[LIT]** Ding, Liu, Lu, Weng: modular binary octahedral 2O as a flavour symmetry. They built modular forms in all 2O irreps, classified the fermion mass models, and found a minimal model fitting quark and lepton masses and mixing with 14 real parameters (including τ). They also studied hierarchies near modular fixed points. — [arXiv:2307.14926, JHEP 11 (2023) 083](https://arxiv.org/abs/2307.14926)
- **[LIT]** Feruglio–Hagedorn–Lin–Merlo: a T′ (double-tetrahedral) SUSY model with near-TBM lepton mixing. The realistic quark masses and mixing come from T′ *doublet* representations, i.e. a 2+1 generation structure. — [NPB 775 (2007) 120](https://www.sciencedirect.com/science/article/abs/pii/S0550321307002635); non-SUSY T′ flavour: [arXiv:1611.00784](https://arxiv.org/pdf/1611.00784), [PRD 100, 035006](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.035006); radiative T′ quark masses: [arXiv:1608.06999](https://arxiv.org/html/1608.06999)
- **[LIT]** Recent modular-flavour hierarchy work: [JHEP10(2025)033](https://link.springer.com/article/10.1007/JHEP10(2025)033), [JHEP06(2025)096](https://link.springer.com/article/10.1007/JHEP06(2025)096)

### Inferences
- **[INF]** If lattice spin and generation index are tied to the same O_h, spinor generations would transform under 2O. A spinor triplet does not exist there: spinor irreps have dimension 2 or 4. The three generations must therefore be a *bosonic* (integer) irrep of O_h, T1u, tensored with an independent spin-½. This matches the model's choice.
- **[INF]** The T′ lesson is that quark models prefer 2+1 (a doublet for generations 1–2 plus a singlet for the 3rd). Under O_h → D4h, T1u → Eu ⊕ A2u is exactly 2+1. So a quark sector dominated by a tetragonal distortion, with the heavy 3rd generation along the tetragonal axis, is the lattice analogue of T′ quark models.

### Gaps
- I found no paper that puts fermion generations in O_h double-group spinor irreps on a lattice.

---

## Q7. Colour as a second triplet; why quark Koide fails (running, pole masses)

### Takeaway
I found no literature on interference between an SU(3) colour triplet and a cubic generation triplet. The literature explanations for quark-Koide failure are: scheme and running (the quark phases and amplitudes move with µ); the absence of pole masses for light quarks under confinement; and the fact that even lepton Koide holds for *pole* masses and degrades at M_Z. Sumino's family-gauge mechanism is the one concrete account of why the relation is exact at low energy, via a QED–family-gauge cancellation.

### Cited findings
- **[LIT]** Lepton Koide holds for pole (low-energy) masses. At M_Z, k_L and δ_L deviate by about 0.2% and 0.5%. Light-quark pole masses cannot be checked "due to the problem of quark confinement". — [Żenczykowski 1301.4143](https://arxiv.org/abs/1301.4143); [Wikipedia](https://en.wikipedia.org/wiki/Koide_formula)
- **[LIT]** Sumino: a U(3)×SU(2) family gauge symmetry. If α = ¼α_F, the 1-loop family-gauge correction cancels the 1-loop QED correction to Koide's formula. Unification with SU(2)_L at 10²–10³ TeV. — [arXiv:0812.2103, JHEP 05 (2009) 075](https://arxiv.org/abs/0812.2103); [arXiv:0812.2090, PLB 671 (2009) 477](https://arxiv.org/abs/0812.2090)
- **[CALC]** From the Q3 table: at M_Z, Q_up rises from 0.849 to 0.888 and Q_down from 0.731 to 0.748, moving further from 2/3. QCD running pushes quarks *away* from Koide as the scale rises, the same direction as QED does for leptons but much larger.

### Inferences
- **[INF]** Sumino's cancellation relates a gauge coupling to the family coupling. The lattice analogue would be colour-dressed E_g stiffness: a quark's E_g amplitude renormalised by the colour sector. That would explain k_q > 1 as a colour correction to the singlet–doublet equipartition. The SU(3) 3 and the O_h T1u live in different spaces (internal vs lattice), so there is no group-theoretic obstruction. Any interference would be dynamical, through the E_g stiffness.

### Gaps
- No source found on colour–cubic-triplet interplay. No source found that computes quark Koide with QCD-corrected "pole-like" or threshold masses systematically. The Xing–Zhang 2006 running-mass tables (PLB 635, 107) were cited in 1301.4143 but not fetched.
