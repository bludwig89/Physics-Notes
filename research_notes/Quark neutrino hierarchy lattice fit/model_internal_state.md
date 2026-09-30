# Internal state of the Physics Notes CA model: fermion generations, mass hierarchy and mixing (as of 2026-09-24)

*Compiled 2026-09-24 - read-only survey of `/Users/ben.ludwig/AI/Physics Notes`. All sources are repo-relative paths. "Exact" = algebraic/group-theoretic; "machine" = floating point to ~1e-15; "input" = empirical or free; "no-go" = proven negative. Key equations are verbatim from the finding files.*

---

## Q1. How are three generations obtained (F75 / F342 / F292 / CL004), and what keeps the identification a hypothesis?

### Takeaway
Three generations = the unique odd-parity triplet irrep **T1u** of the BCC point group O_h, found in the 8-site BCC nearest-neighbour shell (Γ_shell = A1g ⊕ A2u ⊕ T1u ⊕ T2g). The group theory is exact, but the claim that a *physical generation* is that triplet is a **stated hypothesis** (CL004 status `contingent`). F342 shows the model's own gauge couplings cannot select T1u over T2g.

### Cited Findings
- **Operational definition (F75 §1):** a generation multiplet is a set of states that "(i) carry identical gauge quantum numbers ... (ii) are related by an exact symmetry of the vacuum ... (iii) are mutually independent". (ii)+(iii) ⇒ the multiplet is one irrep of O_h (order 48). — [findings/F75-three-generations-from-bcc-irrep-selection.md](findings/F75-three-generations-from-bcc-irrep-selection.md)
- **Four-step chain (F75 §3, 8/8 PASS, exact rationals):** (T1) the largest single-valued O_h irrep has dimension 3, since Σd² = 2(1+1+4+9+9) = 48, so there is no 4-dim irrep. (T2) The nearest-neighbour shell decomposes as `Γ_shell = A1g ⊕ A2u ⊕ T1u ⊕ T2g (1+1+3+3=8)`. (T3) The F27 mass is a *scalar*, so the partner χ must sit in an odd-parity (u) orbital. The odd content is A2u ⊕ T1u, and the only triplet among them is T1u, which rules out T2g. (T4) By Schur, O_h-invariant mass operators have degeneracies [1,1,3,3], and a 4-fold block fails to commute with O_h (commutator 1.0). — [F75](findings/F75-three-generations-from-bcc-irrep-selection.md)
- **F75's roles:** "the lattice supplies the triplet, the chiral mass step selects which one". F27 alone "has no discrete generation structure". — [F75 §4](findings/F75-three-generations-from-bcc-irrep-selection.md)
- **Structural commitment on mixing (F75 §6.1):** "Any inter-generation operator the model builds must be a T1u tensor; this constrains the allowed mixing (CKM/PMNS) textures the lattice can produce." — [F75](findings/F75-three-generations-from-bcc-irrep-selection.md)
- **F75's own §7 limitations:**
  1. "Generation index = orbital irrep of the nearest-neighbour shell" is "a model ... not derived from the QCA update rule".
  2. The hierarchy is not derived.
  3. Double-group caveat: the spinor double group O_h' has a 4-dim irrep (G_{3/2}). "No fourth" assumes the generation label factorises from spin, and F75 calls this "the load-bearing assumption behind 'no fourth'".
  4. If a pseudoscalar (γ5) mass channel were dynamically active it would couple the even T2g triplet, making the count "three per active mass-parity channel".
  — [F75 §7](findings/F75-three-generations-from-bcc-irrep-selection.md)
- **F342 (2026-08-31, 11/11 exact):** condition (i) is *vacuous*. The engine's charge coupling is "a scalar coupling constant, diagonal in the lattice-site basis" (`charge_coupling.py`, `minimal_coupling.py` carry a single scalar `q`; a grep for T1u in `src/casim/engine/` outside `forks/` returns zero hits). The 8 shell vertices form a single O_h orbit, so any diagonal O_h-invariant charge is ∝ identity. Condition (i) is therefore "satisfied identically by every 3-dimensional subspace of the shell, T1u and T2g alike". Condition (i) would only gain selecting power from a non-diagonal, irrep-block charge `Q_block = aΠ_A1g + bΠ_A2u + cΠ_T1u + dΠ_T2g` with c≠d. None exists outside three exploratory fork files. — [findings/F342-generation-identification-condition-i-vacuous.md](findings/F342-generation-identification-condition-i-vacuous.md)
- **F342 independent cross-check of the projectors:** Π_T1u = (1/8)MMᵀ from vertex coordinates and Π_T2g = (1/8)NNᵀ from pairwise products (s_y s_z, s_z s_x, s_x s_y). These satisfy MᵀM = NᵀN = 8·1, MᵀN = 0, exactly over ℚ. — [F342 §4](findings/F342-generation-identification-condition-i-vacuous.md)
- **F292 (8/8):**
  - d = 6 and d = 9 are excluded. The bivector overcount (d−1)/2 equals 1 only at d=3, and chirality requires D=d+1 to be even.
  - A reducible d=3n "freezes": rank J = 3, dim ker J = 3(n−1).
  - F292 §6 explicitly *declines* to read the frozen copies as generations ("the frozen directions have no dynamics to carry a generation label").
  - N_c=3 is "a different three".
  — [findings/F292-no-higher-multiple-of-three.md](findings/F292-no-higher-multiple-of-three.md)
- **CL004** "Exactly three fermion generations": kind derivation, **status contingent**, exactness exact, findings F75/F292/F342, falsifier stated (a fourth sequential generation). Non-discovery does not confirm it. — [docs/claims/CL004-exactly-three-fermion-generations.md](docs/claims/CL004-exactly-three-fermion-generations.md)
- **Completeness rubric row C1** "Exactly three generations" = **PARTIAL**, because the "physical identification is a stated hypothesis, now shown vacuous on one leg". — [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md) (line ~336)

### Inferences
- The generation count is a *symmetry-capacity* argument (max irrep dimension = 3), not a dynamical one. Any external mechanism that makes generations dynamical, such as a family symmetry acting as a genuine T1u ≅ vector of O_h ⊃ A4/S4/Δ(27)-like discrete groups, would need to supply the missing non-diagonal "irrep-block" coupling that F342 names.
- O_h contains S4 (rotation group O ≅ S4) and A4 subgroups. The model's T1u triplet is thus structurally close to discrete-flavour-symmetry model building (A4/S4 triplets). This is my inference; no finding says so.

### Gaps
- No finding derives the T1u ↔ generation identification from the QCA update rule.
- The double-group (spinor) caveat of F75 §7.3 is not attacked by any later finding I found.

---

## Q2. Crystal-field splitting, orthorhombic break, E_g condensate, Koide Q=2/3 as 45° equipartition (F76/F78/F80/F84/F92/F93/F95/F96). Inputs vs derived; the mass formula

### Takeaway
The charged-lepton mass formula is
**√m_a = μ[1 + √2 cos(δ + 2πa/3)], a=0,1,2**
read as an A1g background plus an **E_g condensate on the BCC second-neighbour (cube-axis) shell** at angle δ. Derived: the √m variable (as a Cooper-pair bilinear), the √2 amplitude (Q=2/3 as a 45° consistency fixed point with the Fock √2 as its lone new input), E_g as the unique non-mixing splitter, the stabilizer D_2h, the spontaneity of the break, and the cubic Landau coefficient B. The angle δ = 2/9 is adopted as a principle (Q3). The overall scale is an anchor (Q3).

### Cited Findings
**F76 (6/6 PASS):**
- **C1 (exact):** three distinct masses require an orthorhombic D_2h break, T1u → B1u ⊕ B2u ⊕ B3u. Cubic gives [3], tetragonal [2,1], orthorhombic [1,1,1]. — [findings/F76-generation-mass-hierarchy-crystal-field.md](findings/F76-generation-mass-hierarchy-crystal-field.md)
- **C2 (exact, negative):** a crystal field linear in m fails. The fit gives mean 627.7 MeV and max|Δ|/m̄ = 1.83 > 1, i.e. non-perturbative. — [F76 §3](findings/F76-generation-mass-hierarchy-crystal-field.md)
- **C4 (exact identity):** cos²θ = (Σ√m)²/(3Σm) = 1/(3Q). So Q=2/3 ⇔ θ=45° ⇔ |A1g|²=|T1u|² (equipartition of √m between the democratic and splitting parts). — [F76 §4](findings/F76-generation-mass-hierarchy-crystal-field.md)
- **Data:** Q_lepton = 0.6666605 (|Q−2/3| = 6.2e-6, 0.91σ). The predicted m_τ = 1776.97 MeV vs PDG 1776.86±0.12. — [F76](findings/F76-generation-mass-hierarchy-crystal-field.md)
- **F76 §6 "Empirical input, not derived":** "The amplitude √2 — equivalently Q=2/3 exactly — is not derived ... The phase δ is a free fit parameter." Also: "the up-type (Q=0.849) and down-type (Q=0.731) quarks do not satisfy Q=2/3, and neutrinos are unconstrained here." — [F76 §6](findings/F76-generation-mass-hierarchy-crystal-field.md)

**F78 (6/6):**
- **Part A (derivation, given the Cooper-pair premise):** m_a ∝ ⟨y_a y_a⟩ = y_a², so "√m_a = y_a = the T1u vector component on axis a".
- **A2:** in u = m^s, the participation ratio 1/Q(s) = 3/2 only at s=1/2 (1.500014).
- **Part B:** 1/3 ≤ Q ≤ 1, and Q = 2/3 is the democratic–hierarchical midpoint. Symmetric cube dynamics give Q=1/3 (degenerate), so the √2 amplitude remained an input at F78.
— [findings/F78-koide-amplitude-from-cooper-pair.md](findings/F78-koide-amplitude-from-cooper-pair.md)

**F80 (4/4):**
- **Exact map:** Q(φ) = 1/(3cos²φ). At φ=45° this is the same SO(2) equal-split as the F73 bound-pair cap arcsin m_c = π/4.
- **Hypothesis (D4):** EM is the selector. Only the EM-coupled, colour-free sector (charged leptons) sits at 45°. Quarks are "dominated by the non-abelian QCD condensate". Neutrinos have Q "0.34–0.59", ordering-dependent.
- **Honest residual (D5):** perturbative EM supplies only α/π ≈ 0.13°, about 340× too weak to *drive* the 45° rotation.
— [findings/F80-one-45deg-em-saturation-koide.md](findings/F80-one-45deg-em-saturation-koide.md)

**F84 (4/4):**
- The democratic stiffness κ in E(φ) = ½κφ² − λ sin 2φ is the residual S3 generation-permutation symmetry. κ→∞ gives Q=1/3 (the F75 cubic, degenerate case); κ=0 gives Q=2/3.
- The same orthorhombic break removes κ.
- The data bound is κ/λ ≲ 2×10⁻⁵.
— [findings/F84-flatness-from-orthorhombic-break.md](findings/F84-flatness-from-orthorhombic-break.md)

**F92 (5/5):**
- The two mass laws L1 (pair-sum, m = sin 2t, F73) and L2 (bilinear, m = y², F78), with the two-quantum Fock amplitude y = √2 sin t, are jointly satisfiable only at 2 sin²t = sin 2t ⇔ **t = 45°** (sympy returns {π/4}), giving Q(45°) = 2/3 exactly.
- The F73 cap m_c ≤ 1/√2 becomes unitarity y ≤ 1.
- "only new input is the Bose pair factor √2".
- **Remaining:** why the generation-space angle participates in the pair phase budget "at all" (not derived from the QCA rule).
— [findings/F92-per-constituent-phase-consistency.md](findings/F92-per-constituent-phase-consistency.md)

**F93 (8/8; "major reframing"):**
- **O1 (exact):** sym(T1u⊗T1u) = A1g ⊕ E_g ⊕ T2g. A1g = trace (no split). E_g = diagonal-traceless doublet ("splits the three axes without mixing them"). **T2g = off-diagonal, only mixes axes.** "three distinct masses without axis mixing ⇔ a nonzero E_g field".
- **O2 (exact):** 1st shell (8 cube vertices) = A1g⊕A2u⊕T1u⊕T2g contains **no** E_g. The 2nd shell (6 cube-axis sites) = A1g ⊕ E_g ⊕ T1u. So the splitting field lives on the second shell, "the same second shell whose bond-axis counting produced F49's sin²θ_W=2/9".
- **O3 (exact):** a generic-angle E_g condensate has stabilizer D_2h (8 sign matrices, zero axis permutations). κ=0 becomes a stabilizer theorem. At δ ≡ 0 (mod 60°) the stabilizer is D_4h with a [2,1] degeneracy.
- **O4 (exact):** the F76 Z3 form *is* an A1g + E_g condensate. With E1 = diag(2,−1,−1)/√6 and E2 = diag(0,1,−1)/√2, d_a = e√(2/3) cos(δ − 2π(a−1)/3).
- **O5 (mechanism, coefficients not derived):** F(e,δ) = (r/2)e² + (b/3)e³cos3δ + (u/4)e⁴ + (w/6)e⁶cos²3δ. The orthorhombic phase wins iff C>0 and |B|<2C, with **cos3δ* = −B/(2C)**. A quartic theory can never orthorhombify; the sextic invariant is required.
- **O6 (machine):** the BCC dispersion is exactly O_h-symmetric (4.7e-16), so the break "must be spontaneous".
- **O7 (data):** δ_data = 12.7328° = 0.22224 rad; A/ȳ = 1.414201 vs √2; cos3δ = 0.785874 is "the one remaining free number".
— [findings/F93-orthorhombic-Eg-vacuum.md](findings/F93-orthorhombic-Eg-vacuum.md)

**F95 (7/7):**
- The Dirac-sea loop derives the cubic term B = −(3/2)I₂ ȳA³ = −3√2 I₂ ȳ⁴, with I₂ = ⟨cot ω_kin⟩_BCC = 0.2202. The sign is B<0, the hierarchical side.
- The sextic brake C cannot come from any per-axis loop: it scales ∝ ȳ^~7 and is tetragonally locked by 31 decades.
- C is localized to the E_g condensate's own self-interaction, with C = 0.636|B| required.
— [findings/F95-B-derived-C-localized.md](findings/F95-B-derived-C-localized.md)

**F96 (8/8):**
- **Two-value theorem:** quadratic-cost mean-field gap theory on the BCC Dirac sea supports "at most two distinct generation masses", so a non-quadratic E_g self-term is needed for three distinct masses.
- **Exact texture algebra:** for (m_h, m_mid, 0), Q = (1+u²)/(1+u)² and tan δ = √3u/(2−u). Q=2/3 ⇔ u = 2−√3 ⇔ δ = 15°.
- The sextic W(Σp_a³)² unlocks a three-distinct-mass phase.
— [findings/F96-second-shell-Eg-gap-saturation.md](findings/F96-second-shell-Eg-gap-saturation.md)

**F101b (6/6):**
- The BCC sea has a "cliff" at saturation, f′(m) → −∞, so the heaviest flavor is wall-pinned at y_τ = 1: "The τ mass is the saturation scale."
- Negatives: the lepton point is metastable along the minimal 3-coupling family, and the static RPA gives a wrong-sign sextic.
— [findings/F101b-one-heavy-branch-fit-W.md](findings/F101b-one-heavy-branch-fit-W.md)

**F118 (8/8):**
- A self-consistent (W,v,c) solution exists only on the κ_E<0 (spontaneous E_g, Mexican-hat) branch. There the PDG lepton spectrum is the global ground state (gap −2e-6 on a 121³ grid).
- Couplings are O(1): κ_E ≈ −2.2, c ≈ 1.1, v ≈ 0.16.
- λ6 = 0.243 ≈ 1/4 (W = 6λ6 = 1.46). The sea loop is excluded for C by sign (C_loop = −0.018).
— [findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md](findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md)

**Claim cards:**
- CL005 (Koide Q=2/3 as 45° equipartition): derivation, **live**, exact, findings F92/F93.
- CL072 (F76 crystal field): **open**.
- CL075 (F80): **open**.
- CL079 (F84): **open**.
— [claims-index.md](claims-index.md), [docs/claims/](docs/claims/)

### Inferences
- **Inputs vs outputs for the charged leptons:**

  | Status | Items |
  |---|---|
  | Derived | E_g channel selection (exact); second-shell home (exact); D_2h stabilizer / κ=0 (exact); spontaneity (machine); √m bilinear (derived from the Cooper-pair premise); √2 ⇔ 45° consistency (exact, with the Fock √2 as the lone new input); B (derived, closed form) |
  | Adopted principle | δ* = 2/9 (Q3) |
  | Output | λ6 / C |
  | Anchor | overall scale μ (Q3) |

- The mechanism is "a Landau theory of a spontaneously condensed E_g (d-wave-like, second-shell) order parameter, which selects a Koide circulant". For external literature, the natural matches are: Koide/Brannen circulant (Z3 Fourier) mass matrices, Froggatt–Nielsen-free "democratic-to-hierarchical" textures, and discrete-flavour vacuum alignment. My inference.

### Gaps
- The Landau coefficients r, u, and the sextic w are not derived from the QCA rule. F95 derives only B.
- The √2 still rests on the Cooper-pair (bilinear) premise, which F92 §6 says is not derived from the update rule.

---

## Q3. δ* = 2/9 as E_g representation weight, η² = 1/2, λ6 (F175/F176/F230/F234/F253/F255/F256, key decision 7). Is the overall mass scale derived?

### Takeaway
δ* = dim(E_g)/dim(T1u⊗T1u) = 2/9 rad is **adopted as a founding principle** ("weight-as-phase", key decision 7, 2026-07-16). The dynamical route cannot derive it exactly (F256). λ6 = 0.243 is an **output**. Together with the √2 amplitude, the charged-lepton *ratios* follow to ≤0.007% with zero shape parameters. The **overall scale is not derived**: it is τ-anchored (FIT N=1). F233 shows it transmutes from α_s to within a factor ≈1.9, with a residual equal to the shared strong-sector constant d₁.

### Cited Findings
**F175 (5/5), exact representation weight:**
- T1u⊗T1u = A1g ⊕ E_g ⊕ T1g ⊕ T2g (1+2+3+3 = 9), so the E_g weight = 2/9. This parallels F49's sin²θ_W = 2/9 on the same second shell.
- **Prediction** with δ* = 2/9 and √2: m_μ/m_e = 206.770 vs 206.7683 (+0.001%); m_τ/m_e = 3477.47 vs 3477.228 (+0.007%).
- Open at the time: "weight-as-phase" (why a phase in radians equals a representation weight).
— [findings/F175-lattice-2-9-eg-weight.md](findings/F175-lattice-2-9-eg-weight.md)

**F174b:** δ* = 2/9 rad is corroborated by Brannen's fit δ = 0.2222220(19). Geometric/algebraic-cosine alternatives (cos3δ = 11/14, π/4) are excluded at 10σ/31σ, which marks δ* as a "rational radian". — [findings/F174b-shape-angle-2-9-topological.md](findings/F174b-shape-angle-2-9-topological.md)

**F230 (SUPERSEDED):** a crystal-field/equipartition geometric derivation of 2/9 closes negative. — [findings-index.md](findings-index.md) row F230

**F253 (5/5, negative/sharpened):**
- Weight→phase reduces to one posit, POSIT-N (the E_g generator is unit-normalized).
- The topological escape is excluded: "the only E_g holonomy on the BCC 2nd shell is 2π/3"; 2/9 is a multiplicity, not a holonomy.
— [findings/F253-weight-as-phase-scale-nogo.md](findings/F253-weight-as-phase-scale-nogo.md)

**F255 (4/4):**
- R = 1 (a genuine radian) is *derived* via Schur-isotropy of the E_g irrep metric (DᵀD = 1 to 4.4e-16).
- The lepton deviations p_a = √m_a − mean lie in the E_g plane to 2.3e-16, and the direct geometric angle = 0.22223 rad.
- Half (b), angle = weight, does not close: using λ6 to derive 2/9 is circular.
— [findings/F255-generator-norm-fixed-by-F118-schur.md](findings/F255-generator-norm-fixed-by-F118-schur.md)

**F256 (4/4):**
- "derive λ6 = 0.243" is misposed. B (Dirac sea, ∝ ȳ⁴) and C (induced condensate) are independent, so −B/2C = cos(2/3) is a "1.7×10⁻⁵ near-coincidence".
- λ6 = 0.243 lies strictly between the only available rationals, 2/9 (Fierz, F145) and 1/4 (rotor, F144), and matches neither.
- Exact closure is possible only via weight-as-phase.
— [findings/F256-lambda6-sextic-derivative-nogo.md](findings/F256-lambda6-sextic-derivative-nogo.md)

**F234 (5/5):** feeding δ* = 2/9 into cos3δ* = |B|/2C with the derived B = −0.0569 gives C_req = 0.0362 and λ6 = 0.243 exactly. The arrow is angle → brake. This supersedes F179's "λ6 not reducible" relabel. — [findings/F234-Wvc-triple-closed-delta-2-9-pins-brake.md](findings/F234-Wvc-triple-closed-delta-2-9-pins-brake.md)

**Key decision 7 (CLAUDE.md; docs/theory/key-decisions.md line 13):** "We adopt as a principle that the charged-lepton condensate shape-angle equals the second-shell E_g representation weight ... This is taken as fundamental, not derived from the condensate dynamics." λ6 = |B|/(2e⁶cos(2/3)) is an output. — [docs/theory/key-decisions.md](docs/theory/key-decisions.md)

**Ledger:** open-derivations Part C row E1 = "DECISION 2026-07-16". Row E4 is closed into E1. — [docs/status/open-derivations.md](docs/status/open-derivations.md)

**CL028** (lepton shape angle is a representation weight): derivation, **live**, exact, findings F175/F234/F253/F255/F256. — [claims-index.md](claims-index.md)

**F348:** the 0.007% m_τ/m_e residual is a 1.04σ effect against the PDG m_τ uncertainty, i.e. a measurement floor. — [findings/F348-*](findings/)

**Overall scale:**
- **F121:** the τ is adopted as the canonical scale anchor; it is wall-pinned, hence δ-stable. — [findings/F121-tau-anchored-canonical-spectrum.md](findings/F121-tau-anchored-canonical-spectrum.md)
- **F233:** N = m_lat(τ) ≈ 5.5×10⁻¹⁹ is generated by asymptotic freedom from α_s(μ₀) = 1/(16π) at μ₀ = ħc/a = 1.85×10¹⁸ GeV. N_pred = 2.86×10⁻¹⁹, "a factor 1.9 ... with no free parameter". The residual is the one-loop matching constant d₁. — [findings/F233-mass-scale-N-transmutation-supersedes-F119.md](findings/F233-mass-scale-N-transmutation-supersedes-F119.md)
- **F170:** the lepton/E_g condensate scale = O(1)×Λ_QCD. The E_g condensate "has no independent contact coupling — its self-interactions are induced by the strong sector (F145/F150)". The gap-kernel ratio is G_c^{Eg}/G_c^{s-wave} → 1.08. The measured m_τ/Λ ≈ 3.4–5.7 is bracketed, not pinned. — [findings/F170-lepton-colour-scale-link.md](findings/F170-lepton-colour-scale-link.md)
- **Completeness 2026-09-08:** row 7–8 lepton shape = QUANT×2 (≤0.007%); row 9 charged-lepton overall scale = **FIT (N=1)**, "inherits d₁". — [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md)
- **Ledger d₁:** the required value is 1.773444, and the number is "STILL NOT QUOTABLE". F337's native sweep gave Λ_MS/Λ_rule = 31.3, outside F280's bracket [1, 7.98]. — [docs/status/open-derivations.md](docs/status/open-derivations.md)
- **E5 (m_{E_g} scalar mass):** undetermined, with a BBN lower bound of >125.5 MeV (F309). — [docs/status/open-derivations.md](docs/status/open-derivations.md)

**Notation caveat.** The √2 amplitude is written two ways in the repo, and both mean Koide Q = 2/3 via Q = 1/3 + η²/6 in the η=√2 convention:
- η² = 1/2 in CLAUDE.md, F175 and F346's header.
- η = √2 (η² = 2) in F346/F347's tables ("lepton's derived η²=2 (F92)").
— [F175 §5](findings/F175-lattice-2-9-eg-weight.md); [F347 §2](findings/F347-quark-mixed-koide-tuples-leaning-nogo.md)

### Inferences
- The lepton sector has exactly one dimensionful input (the τ anchor, i.e. d₁) and zero dimensionless shape inputs. Both shape numbers carry principle-level caveats: the √2 rests on the Cooper-pair premise, and 2/9 is an adopted principle.
- Any external mechanism for quarks must either reproduce a different weight/amplitude pair per sector, or supply a different mechanism entirely. The model has no second "weight" principle.

### Gaps
- F176 (saturation self-duality principle) was not read in detail. The index says it proposes "angular invariant equals its…" as the dynamical principle behind 2/9, and it predates the key-decision adoption.

---

## Q4. Quarks: Q_up = 0.849, Q_down = 0.731; F346/F347; any CKM/Cabibbo findings; how quark masses enter the engine

### Takeaway
There is **no derivation of any quark mass or CKM element**:
- Quark current masses are **per-species inputs**: the "consistency readout" of F121, graded OPEN×6.
- CKM is **declared out of scope** (CL017; J=0 is one-generation arithmetic).
- The lepton E_g/weight-as-phase mechanism **does not transplant** to (u,c,t), (d,s,b), (u,d,s) or (c,b,t) (F346/F347, leaning no-gos).
- F346 records one flagged-not-adopted coincidence: the down-type δ is 1.45σ from the A1g weight 1/9.
- No finding (none found under quark/CKM/Cabibbo/Wolfenstein/flavour/Yukawa greps) derives a Cabibbo angle or Wolfenstein parameters.

### Cited Findings
- **F76/F80:** Q_up = 0.849, Q_down = 0.731, "not 2/3". F80 attributes this to QCD contamination (EM-selector hypothesis) and notes "two different Q's ... no universal value". — [F76](findings/F76-generation-mass-hierarchy-crystal-field.md); [F80 §5](findings/F80-one-45deg-em-saturation-koide.md)
- **F346 (6/6, battery; independent review CONFIRMED-NARROWER):**
  - Method: invert the exact circulant √m_a = μ(1+η cos(δ+2πa/3)) on PDG 2024 masses: u 2.16±0.07, c 1273.0±4.6, t 172570±290; d 4.70±0.07, s 93.5±0.8, b 4183±7 MeV. The t mass is a kinematic mass, a flagged scheme inconsistency.
  - Results table:

    | Sector | Q | η² | δ mod 2π/3 | Distance to nearest weight |
    |---|---|---|---|---|
    | Up | 0.8488 | 3.093 | 0.07452 rad | **219σ** from A1g = 1/9 (882σ from E_g, 1546σ from T = 1/3) |
    | Down | 0.7313 | 2.388 | 0.11012 rad | **1.45σ** from A1g = 1/9 |

  - Range-based look-elsewhere: p ≈ 0.28% (down alone), p ≈ 0.57% (either sector). This was corrected from a wrongly scaled p ≈ 0.6 by review.
  - The down-type proximity is "flagged, not adopted": there is no theoretical reason for A1g, and it does not recur in up-type.
  - "Any 3 positive numbers admit an exact (μ,η,δ) fit": the ansatz is a coordinate change, so only where δ lands is informative.
  — [findings/F346-quark-shape-eg-t1u-leaning-nogo.md](findings/F346-quark-shape-eg-t1u-leaning-nogo.md)
- **F347 (8/8, battery; review CONFIRMED):**
  - **(u,d,s)** (Harari–Haut–Weyers 1978): Q = 0.5667, 15% off 2/3. The 1978 match relied on m_u = 0. δ = 0.0769 rad, 10.8σ from A1g; η² = 1.400.
  - **(c,b,t)** (Rodejohann–Zhang 2011): Q = 0.66922, within 0.38% of 2/3. But Q = 1/3 + η²/6 exactly is δ-independent. η² = 2.01533 is **9.6σ** from 2. δ = 0.06865 rad is **204σ** from A1g (look-elsewhere p = 12.2%).
  - Rivero's signed (s,c,b) tuple (arXiv:1111.7232) was not tested, because it needs a sign-flip generalisation of the ansatz.
  — [findings/F347-quark-mixed-koide-tuples-leaning-nogo.md](findings/F347-quark-mixed-koide-tuples-leaning-nogo.md)
- **Ledger E6** (six quark masses): OPEN. "Do not re-run the F175/F92 direct-transplant check". Three named untried avenues:
  1. whether F75's charge-blind generation-count mechanism says anything about quark generations;
  2. a shape mechanism anchored to the **constituent** mass (F123's m_c = 309.5 MeV) instead of the current mass;
  3. Rivero's signed (s,c,b).
  — [docs/status/open-derivations.md](docs/status/open-derivations.md)
- **Ledger E7 / CL017 (CKM):**
  - "CKM: ABSENT ×4, declared out of scope ($J(1)=0$ is one-generation arithmetic, not a prediction)". This was re-confirmed 2026-09-02 after F346/F347, because they "do not supply any quark mass-eigenstate structure a mixing angle could be built from".
  - CL017: non_claim, `not_claimed`, finding F53.
  — [docs/status/open-derivations.md](docs/status/open-derivations.md); [docs/claims/CL017-ckm-and-cp-violation-out-of-scope.md](docs/claims/CL017-ckm-and-cp-violation-out-of-scope.md)
- **Completeness 2026-09-08:**
  - #1–6 quark masses: OPEN×6.
  - #10–13 CKM: ABSENT×4.
  - FCNC/GIM: ABSENT, "downstream of CKM".
  - B11 strong CP: arg det M_q at three generations is E6/E7.
  — [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md)
- **Engine treatment (F40, 11/11 + 6/6):**
  - The quark F27 mass step is applied "per flavour per colour"; "Distinct m_u, m_d, m_s give natural up/down/strange mass splitting at the flavour level, and the mass is colour-blind (only the SU(3) link rotates colour)".
  - Diagnostic Q10: an explicit split m_u ≠ m_d breaks SU(2)_L at the mass-term level (Ward residual 2.4e-1), one of "the Known Limitations F27 itself flagged".
  — [findings/F40-quark-f27-mass-and-electroweak.md](findings/F40-quark-f27-mass-and-electroweak.md)
- **Related quark-scale results (not current masses):**
  - F123: constituent m_c = 309.5 MeV and 3m_c ≈ m_p to ~1% from one f_π anchor. — [findings/F123-p6-si-scale-matter-sector.md](findings/F123-p6-si-scale-matter-sector.md)
  - F402: Ji decomposition, σ_N = 46 MeV supported. — [findings-index.md](findings-index.md)
  - F352: top condensation at the lattice cutoff Λ = 1.85×10¹⁸ GeV predicts m_t = 226.6 GeV (+31%) and m_H = 248.8 GeV. Minimal single-channel top condensation is EXCLUDED (CL293). — [docs/status/open-derivations.md](docs/status/open-derivations.md) row E8
- **Structural hint on CKM (F236 §4):** "for quarks small mixing would be a near-success of the E_g-diagonal picture". An E_g-only texture gives identity mixing, and CKM is near-identity. — [findings/F236-three-generation-seesaw-pmns.md](findings/F236-three-generation-seesaw-pmns.md)

### Inferences
- **Available quark-sector hooks:** the T1u triplet (generation count, charge-blind), the second-shell A1g ⊕ E_g ⊕ T2g crystal-field decomposition, the circulant Z3 form, and the finding that mixing can only come from T2g (F93 commitment #1, F236). Nothing in the model yet makes the E_g angle or amplitude sector-dependent (colour or charge dependent). F80's "EM selector" is a qualitative hypothesis without a quark-sector mechanism.
- If up- and down-type E_g condensates sit at different angles in the *same* cube-axis basis, CKM = 1 exactly. Non-trivial CKM would need T2g amplitudes that differ between up- and down-type sectors. By F254's stabilizer argument those amplitudes would be free (see Q5). External mechanisms supplying small quark mixing (e.g. Fritzsch/Gatto–Sartori–Tonin √(m_d/m_s) relations, or Froggatt–Nielsen) would need to act through T2g. My inference.

### Gaps
- No finding computes quark masses from any lattice mechanism.
- No finding tests colour-dependent modification of the E_g Landau theory.
- No Cabibbo/Wolfenstein/Gatto relation has been tested.
- The constituent-mass anchored shape route and Rivero's signed tuple are both untried.

---

## Q5. Neutrinos: F47, F201, F236, F254, F353, F341, F343, sterile DM; what failed in F236 and why

### Takeaway
The neutrino sector has four parts:
1. A **Higgs-free anti-linear Majorana step** (F47), structurally forced by hypercharge closure (F341, conditional).
2. A **3×3 type-I see-saw** whose E_g/Z3 texture gives masses and hierarchy (F236).
3. **PMNS = 1 exactly** from E_g alone (the F236 no-go). Mixing must come from the second-shell T2g channel, whose three amplitudes are **provably free** (F254: three inequivalent 1-d irreps of D_2h). δ_CP inherits the same freedom (F353).
4. The **absolute scale M_R is free** (F343 three-leg null).

### Cited Findings
- **F47 (6/6):**
  - The Majorana step is χ_u′ = c_M χ_u − i s_M χ_d*, χ_d′ = c_M χ_d + i s_M χ_u*. It is anti-linear, which makes it the source of L-violation, and it is R-unitary.
  - U(1)_Y-invariant iff Y_νR = 0.
  - The see-saw m_ν ≈ M_D²/M_R holds at machine precision for M_R/M_D ∈ [3, 10⁵].
  — [findings/F47-majorana-seesaw-higgs-free.md](findings/F47-majorana-seesaw-higgs-free.md)
- **F341:** no protecting symmetry forbids the Majorana term, and removing it reopens the F165/F279 hypercharge closure. CL290: `contingent`. Rubric C4 is PARTIAL. — [findings/F341-majorana-forced-by-hypercharge-closure.md](findings/F341-majorana-forced-by-hypercharge-closure.md); [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md)
- **F279:** hypercharge quantisation is closed by the F47 Majorana step, not by the gravitational anomaly. — [findings-index.md](findings-index.md)
- **F201 (5/5):**
  - Setup: M_R is taken to carry the same Z3 texture, √M_a = M_R0[1+√2 cos(δ_ν+2πa/3)].
  - Node: at φ = 135°, 1+√2cos φ = 0 exactly, so one eigenvalue → 0.
  - Numbers: δ_ν = 134.86° (0.14° from the node) gives M₁/M₃ ~ 10⁻⁶. With M_R0 ~ 1 GeV this yields M₁ ≈ 5.6 keV and M₃ ≈ 5.6 GeV (the νMSM split).
  - Status: M_R0 and δ_ν are "accommodated" (two inputs); "M_R inherits the same angle-texture" is "a structural argument ... not a derivation".
  — [findings/F201-kev-sterile-from-eg-texture.md](findings/F201-kev-sterile-from-eg-texture.md)
- **F205/F237/F266 (keV sterile as DM):**
  - F205: QKE production solver validated.
  - F237: "Clean exclusion". Resonant Shi–Fuller production plus entropy dilution cannot clear both the X-ray and the conservative 3.5 keV Lyman-α bounds, at either 5.6 keV or 7.1 keV.
  - F266: still lists the F47 sterile as a "viable, model-native" candidate with mass and production "accommodated".
  — [findings/F237-*](findings/); [findings/F205-*](findings/); [findings/F266-sterile-neutrino-dark-matter.md](findings/F266-sterile-neutrino-dark-matter.md)
- **F364:** resonant leptogenesis at the native F201 masses (M₂ ≈ 0.40, M₃ ≈ 5.60 GeV) with Casas–Ibarra Yukawas fit to oscillation data. The CP phase alone falls ~10–11 decades short of Y_B. Degeneracy matching needs ΔM/M ≈ 10⁻¹⁷, "sixteen orders of magnitude finer than the O(1) split the texture actually predicts". — [findings/F364-baryogenesis-boltzmann.md](findings/F364-baryogenesis-boltzmann.md)
- **F236 (5/5), what failed and why:**
  - M_D and M_R both carry A1g + E_g texture on the same second shell, so both are diagonal in the cube-axis basis. The charged-lepton matrix is too, so U_e = 1 and PMNS = U_ν.
  - Then m_ν = −M_D M_R⁻¹ M_Dᵀ = −diag(M_{D,a}²/M_{R,a}), i.e. three copies of F47 (residual <1e-9).
  - **"E_g texture on both M_D and M_R ⟹ PMNS = 1, θ12 = θ13 = θ23 = 0"**. Changing δ_D, δ_ν or M_R0 "only rescales the eigenvalues — the eigenvectors stay pinned to the cube axes".
  - Adding a symmetric off-diagonal T2g perturbation (t_xy, t_yz, t_zx) to M_R reproduces NuFIT-5.2 NO exactly: θ12 = 33.4°, θ13 = 8.6°, θ23 = 49.0°, Δm²21 = 7.42e-5, Δm²31 = 2.51e-3 eV². But this uses "six inputs for five observables" (δ_D, δ_ν, M_R0, t_xy, t_yz, t_zx). θ13 is "unreachable if M_D is locked to the charged-lepton texture".
  - The illustrative M_D inputs (5×10⁻⁴, 0.10, 1.0 GeV) are inputs.
  - Its §7 table classes light-mass ordering/hierarchy as "Computed", PMNS angles as "Free", and M_R0 and δ_D as "Free".
  — [findings/F236-three-generation-seesaw-pmns.md](findings/F236-three-generation-seesaw-pmns.md)
- **F254 (4/4), stabilizer theorem:**
  - Under D_2h = {diag(s_x,s_y,s_z)}, t_ab ↦ s_a s_b t_ab, so (t_xy, t_yz, t_zx) = B1g ⊕ B2g ⊕ B3g, three **inequivalent** 1-d irreps.
  - The democratic point is invariant only under {±1}. F92 equipartition "cannot apply" because there is no degenerate multiplet.
  - One-parameter ansätze (democratic, single-channel) miss NuFIT by >100 deg². Only the full 3-amplitude fit works (3 inputs for 3 angles).
  - Parameters #23–25 are graded "EXCLUDED ×3 — permanently free, which is a result".
  — [findings/F254-t2g-pmns-selector-nogo.md](findings/F254-t2g-pmns-selector-nogo.md); [docs/status/open-derivations.md](docs/status/open-derivations.md) row D1
- **F353 (6/6):**
  - The D_2h sign action on a complex t_ab only flips by 0 or π, so the F254 no-go transfers to phases. δ_CP (#26) becomes EXCLUDED.
  - F254's real fit gives J = 0 exactly, "a consequence of using only real inputs, not a value protected by any symmetry".
  — [findings/F353-delta-cp-t2g-inheritance.md](findings/F353-delta-cp-t2g-inheritance.md)
- **F343 (8/8), null on M_R:**
  1. The lattice cutoff needs an unexplained ~19-decade suppression (Λ/M_R0 ~ 10¹⁹). The closest coincidence, (1/(72π))⁸, is flagged, not adopted.
  2. The E_g/Z3 texture "provably factors M_R0 out identically" (sympy).
  3. ν_R's total gauge-singlet status removes every RG/confinement handle.
  - M_R is a "5th member of the E5–E7 scale-anchoring cluster".
  — [findings/F343-majorana-scale-no-link-found.md](findings/F343-majorana-scale-no-link-found.md)
- **CL018:** "No absolute neutrino mass is predicted — the see-saw supplies a mechanism, not a scale" (not_claimed). **CL291** no_go live. **CL207 (F236)** and **CL223 (F254)** no_go, open. — [claims-index.md](claims-index.md)
- **Completeness:** #20–21 light-ν mass ratios MACHINE×2 (F236); #22 ν absolute scale OPEN; #23–25 PMNS EXCLUDED×3; #26 δ_CP EXCLUDED; C5 neutrino mass mechanism PARTIAL. — [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md)
- **Ordering and tribimaximal:** F236 fits normal ordering only (NuFIT-5.2 NO). F80 notes the neutrino Koide Q "swings 0.34–0.59" with unknown lightest mass and ordering, and calls near-tribimaximal PMNS "the independent democratic signature of the neutral sector". I found no finding testing inverted ordering, tribimaximal/TM1/TM2, μ–τ symmetry, or θ13 specifically. — [F80 §5](findings/F80-one-45deg-em-saturation-koide.md)

### Inferences
- **Tension:** the completeness grading marks light-ν mass ratios "MACHINE ×2 … derived", but F236 itself uses input Dirac masses M_D and free δ_D, δ_ν. The "derived" label refers to the see-saw algebra and texture form, not to predicted Δm² values. A writer should not quote the light-ν ratios as parameter-free predictions.
- **What an external mechanism must supply:** the three T2g amplitudes, i.e. something that breaks D_2h further or relates B1g/B2g/B3g. In the model's language, a tribimaximal or A4/S4 flavour vacuum would be a *non-generic* T2g condensate requiring an additional symmetry that the E_g-broken vacuum lacks by construction (F254). My inference.

### Gaps
- No dynamical T2g gap computation has been run. Ledger D1 says this is why the row is still in Part A.
- Inverted ordering, the lightest-mass value, and 0νββ predictions beyond "Covered" were not examined in the findings read.

---

## Q6. How colour enters; hypercharge on U(x) (no Higgs) and where Yukawa-like couplings can come from; which mass mechanisms exist (F27, F78, NJL)

### Takeaway
Fermion masses enter only through the **F27 chiral mass step**, a local unitary η↔χ rotation with a gauged phase (SU(2)_L × U(1)_Y pure gauge in U(x), F41). Each species has a **bare mass parameter**; the model has "no Yukawa mechanism anywhere". Dynamical mass generation exists only as an **NJL/Cooper-pair gap** (F77/F145) for the constituent/χSB scale, and as the E_g condensate Landau/gap theory for the lepton shape. Colour enters the lepton sector only indirectly: E_g self-couplings are *induced by the strong sector*, and the lepton scale ≈ O(1)×Λ_QCD (F170). For quarks, the mass step is colour-blind (F40), and no colour-modified crystal field exists.

### Cited Findings
- **F27 (9/9):** M(θ) = [[c_m, i s_m e^{iθ}], [i s_m e^{−iθ}, c_m]]. The SU(2) doublet extension replaces e^{iθ} with U(x). Ward identity V(x)·mass_step(ψ;U) = mass_step(V(x)ψ; V(x)U), residual 1.06e-17, so chiral SU(2)_L is a local gauge symmetry of the mass step. — [findings/F27-complex-mass-chiral-su2.md](findings/F27-complex-mass-chiral-su2.md)
- **F41:** "After F27 (chiral SU(2) mass from β-gauging — no Higgs Yukawa)". The bare F27 step is not U(1)_Y invariant. Fix: U(x) → U(x)·diag(e^{+iαΔY_ν/2}, e^{+iαΔY_e/2}) with ΔY_e = +1, ΔY_ν = −1, which promotes U(x) to pure gauge in SU(2)_L × U(1)_Y. "No physical scalar boson is introduced". — [findings/F41-hypercharge-higgs-free-su2.md](findings/F41-hypercharge-higgs-free-su2.md)
- **Notebook SM-crosscheck handoff (row 2, closed 2026-09-23):** "The model has no Yukawa mechanism anywhere (F41: 'F27... no Higgs Yukawa' — the fermion mass m is a bare per-species parameter, structurally decoupled from the Stueckelberg gauge-mass scale f=v/2)". The F73 Cooper-pair scalar "has exact kinematics but no coupling-to-fermions construction of any kind". — [docs/theory/notebook-sm-crosscheck-handoff.md](docs/theory/notebook-sm-crosscheck-handoff.md); [docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md](docs/theory/notebook-v2/)
- **F40 (quarks):** the F27 doublet step applies per flavour per colour, and the mass is colour-blind. A split m_u ≠ m_d breaks SU(2)_L at the mass-term level (Q10 residual 0.24). — [findings/F40-quark-f27-mass-and-electroweak.md](findings/F40-quark-f27-mass-and-electroweak.md)
- **F42:** hypercharge is extended to the quark sector, and right-handed singlets are made dynamical Y-coupled fields (8/8). — [findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md](findings/F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md)
- **F77 (14/14):** a self-consistent NJL gap + RPA with one coupling fixes m_c and E_b. Goldstone m_π = 0 and m_σ = 2m_c hold to 2.3e-14. m_c, f_π, m_π and ⟨q̄q⟩ are reproduced to 0.2–4%. — [findings/F77-njl-gap-rpa-selfconsistent.md](findings/F77-njl-gap-rpa-selfconsistent.md)
- **F145:** the NJL coupling is induced, with exact Fierz c = 2/9. The bare coupling is subcritical; the running coupling is supercritical, so χSB is forced. — [findings/F145-route-c-induced-njl-coupling.md](findings/F145-route-c-induced-njl-coupling.md)
- **F78:** "Apply the same premise to the source of fermion mass: generation a's mass is set by a pair condensate ... m_a ∝ y_a²". This is the Cooper-pair bilinear, the model's candidate "Yukawa substitute" at the level of the generation amplitude. — [findings/F78-koide-amplitude-from-cooper-pair.md](findings/F78-koide-amplitude-from-cooper-pair.md)
- **F170:** the E_g condensate "has no independent contact coupling — its self-interactions are induced by the strong sector (F145/F150)". Its gap-kernel geometry is near-degenerate with the colour χSB channel (1.08), forcing v_Eg = O(1)×Λ_QCD. — [findings/F170-lepton-colour-scale-link.md](findings/F170-lepton-colour-scale-link.md)
- **F80 D4:** quarks are "dominated by the non-abelian QCD condensate, which pushes them off the clean EM point". This is a hypothesis, with no computed mechanism. — [F80](findings/F80-one-45deg-em-saturation-koide.md)
- **L9 (ledger, opened by F327):** "a massive Dirac fermion on this lattice rides one chiral branch", which carries a dimension-5 CPT-odd LV operator excluded by 7.05 decades vs LHAASO/Crab. The fermion propagator needs a repair: "a single eigenvalue that is a SUM over both branches". "No local mass mixing supplies one". This is an open foundational issue for *any* massive-fermion mechanism. — [docs/status/open-derivations.md](docs/status/open-derivations.md) row L9
- **E8 (Higgs mass):** F73 bound-pair kinematics are exact, but "no sub-threshold binding exists in the gauge/mean-field sector at ANY coupling". F352's BHL top-condensation is excluded. Untried: a lattice Bethe–Salpeter ladder, and a topcolor-analogue multi-channel sector. — [docs/status/open-derivations.md](docs/status/open-derivations.md)
- **N_c = 3 (B10):** PARTIAL. F298 gives the structural leg N_c ≤ 3; the selector conflicts with F299's Casimir confinement (Part D). F292/F293: colour's 3 is not the spatial/generation 3. — [docs/status/open-derivations.md](docs/status/open-derivations.md)

### Inferences
- **Where Yukawa-like couplings can live, given hypercharge-on-U(x):** the Y mismatch that a Higgs would carry is absorbed into the pure-gauge U(x). Any generation-dependent mass matrix therefore has to be built from the per-species mass parameter m in the F27 step. That parameter could be promoted to a 3×3 generation matrix acting on the T1u index, i.e. the E_g/T2g crystal-field fields. There is no scalar doublet whose VEV could carry flavour structure; flavour structure must be a lattice-geometric condensate (E_g, T2g) or a pair condensate (F78). External mechanisms that assume a Higgs doublet (Froggatt–Nielsen flavons coupled to H, radiative Yukawas via Higgs loops) would need translating into "condensate-on-shell" language. My inference.
- **The model's two quark-relevant condensates both live in the strong sector:** the colour χSB/NJL condensate (constituent mass) and the E_g induced coupling. A colour-dependent E_g angle or amplitude is conceivable but unbuilt.

### Gaps
- No finding builds a generation-matrix-valued F27 mass step for quarks.
- No finding computes how an SU(3)-colour condensate would shift the E_g Landau coefficients (B, C) for quarks relative to leptons.
- The F40 Q10 SU(2)_L breaking by m_u ≠ m_d: I found no finding resolving it via the F41 hypercharge-in-U(x) construction for quarks. F41 addresses the Y mismatch but I did not verify how isospin splitting is handled.

---

## Q7. Open items in the ledger, roadmaps, completeness reports and notebook cross-check

### Takeaway
All flavour-sector open items are tracked in `docs/status/open-derivations.md`:

| Row | Content | Status |
|---|---|---|
| E6 | Quark masses | OPEN; three untried avenues |
| E7 | CKM | out of scope |
| E7 / d₁ | v and the charged-lepton scale | FIT(N=1), reduces to d₁ |
| E5 | m_{E_g} | undetermined; BBN bound |
| D1 | PMNS | proven free |
| D4 | M_R | OPEN; δ_CP EXCLUDED |
| E8 | m_H | OPEN |
| L9 | Massive-fermion propagator repair | open |

`docs/roadmaps/next-steps-pt2.md` contains no quark/neutrino/flavour items (grep returned nothing). The notebook cross-check adds only the "no Yukawa" point and a falsified notebook mechanism.

### Cited Findings
- **E6 row:** see Q4. **Suggested attacks:** (i) the F75 count for quarks, (ii) a constituent-mass anchored shape, (iii) the Rivero signed tuple. — [docs/status/open-derivations.md](docs/status/open-derivations.md)
- **D1 row:** "should arguably be in Part B ... kept in A only because the dynamical computation of three independent T2g gaps has never been run." — [docs/status/open-derivations.md](docs/status/open-derivations.md)
- **E7 row:** the F351 check found no second dimensionful pin for v, so v collapses to d₁. — [docs/status/open-derivations.md](docs/status/open-derivations.md); [findings/F351-electroweak-scale-v-not-second-pin-collapses-to-d1.md](findings/F351-electroweak-scale-v-not-second-pin-collapses-to-d1.md)
- **Completeness 2026-09-08 parameter table:**
  - Quark masses OPEN ×6.
  - Lepton shape QUANT ×2.
  - Lepton scale FIT.
  - CKM ABSENT ×4.
  - Light-ν ratios MACHINE ×2.
  - ν scale OPEN.
  - PMNS EXCLUDED ×3.
  - δ_CP EXCLUDED.
  - C1 PARTIAL; C4, C5 PARTIAL.
  — [docs/status/completeness-2026-09-08.md](docs/status/completeness-2026-09-08.md)
- **Notebook SM cross-check synthesis §3:** the notebook's "mass-hierarchy-from-interaction-count" mechanism (pp.9–11, NB-013) is "cleanly falsified by the charged-lepton sector alone: electron, muon, and tau share identical SM gauge interactions yet span a factor of ~3477". The notebook's Higgsless Weinberg–Salam premise is flagged as excluded by the 2012/2022 Higgs data. — [docs/theory/notebook-sm-crosscheck-synthesis.md](docs/theory/notebook-sm-crosscheck-synthesis.md)
- **Notebook SM cross-check synthesis §4:** the composite "Cooper pair" Higgs (NB-009) is listed as "genuinely open" (pNGB composite-Higgs literature). — [docs/theory/notebook-sm-crosscheck-synthesis.md](docs/theory/notebook-sm-crosscheck-synthesis.md)

### Inferences
**Plug-in points for external literature,** ranked by how cleanly they attach to existing structure:
1. **Quark T2g/E_g textures in up vs down sectors, producing CKM.** The model already proves E_g-only gives CKM = 1. A small, sector-differing T2g would be the natural slot, but by F254 its amplitudes are free unless an extra mechanism fixes them.
2. **Sign-generalised / constituent-mass Koide variants for quarks** (E6 avenues ii, iii).
3. **A dynamical T2g gap computation or flavour-symmetry vacuum alignment for PMNS**, which must evade the D_2h inequivalence theorem.
4. **A mechanism tying M_R to d₁/Λ_QCD.** F343 shows ν_R singlet status blocks the model's only running handle.
5. **Anything requiring an elementary Higgs doublet** is structurally incompatible with decision 3 unless recast as a condensate.

### Gaps
- `docs/status/completeness-2026-09-08-prompts.md` was not read in detail. It may contain paste-ready research prompts for rows E6/D1/D4.
- The 2026-08-20 completeness report and its prompts were not compared.
