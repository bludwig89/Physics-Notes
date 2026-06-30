# Physics Audit Report — 2026-06-29

## Executive Summary

The cellular automaton model has a sound algebraic core: BCC unitarity forces the dispersion relation exactly, c_lat = 1/√3 is an exact RG fixed point, the paired-spinor photon resolution of birefringence is logically complete, and the E_g condensate selection as the unique generation-splitting channel is a genuine representation-theory theorem. However, five structural gaps weaken the model's strongest claims: (1) fermion masses are free parameters in the mass step, not derived from the QCA rule; (2) the paired-photon binding is kinematic, not dynamical; (3) the sextic brake C (λ₆ ≈ 1/4) controlling the lepton spectrum is fitted, making mass ratios post-dictions; (4) gravitational perturbations propagate via Poisson's equation (elliptic/instantaneous), conflicting with the GW170817 constraint |c_grav − c_photon|/c < 10⁻¹⁵; and (5) several quantities framed as "predictions" depend on phenomenological inputs (f_π, PDG quark masses, the condensate angle δ). The finding documentation quality is high, with unusually honest "scope" and "limitations" sections throughout.

---

## Critical Issues (blocks a physics claim)

### C1. Gravitational wave speed undefined
**Finding:** F64, F106  
**Severity:** High — potential falsification  
The gravity sector sources K via ∇²ln K = −(8πG/c⁴)T⁰⁰[ψ] (F106), which is Poisson's equation — elliptic, implying instantaneous propagation. No hyperbolic wave equation for K perturbations exists in the model. GW170817 constrains |c_grav − c_photon|/c < 10⁻¹⁵. The model must produce gravitational waves propagating at c = 1/√3 to survive this bound. F130 T3b only verifies the *static* Poisson source law survives blocking.  
**Recommended fix:** Derive the retarded (wave) equation for δK perturbations from the dielectric rotation rule; show c_grav = c_lat.

### C2. Lepton mass spectrum depends on fitted coefficient
**Finding:** F95, F96, F118  
**Severity:** High — downgrades "prediction" to "post-diction"  
The charged-lepton mass ratios depend on cos(3δ) = −B/(2C), where C is the sextic brake from the E_g condensate self-interaction. The value λ₆ ≈ 0.243 is extracted from data (the measured condensate angle δ = 12.73°), not derived from the QCA rule. At the model's own estimate (λ₆ = 1/4, from the sea-loop B), m_μ is off by +104%. The 0.1% lepton spectrum claim (F120) requires the measured angle as input, making it a one-parameter fit (N) to two data points (m_μ, m_τ). Until λ₆ is derived, the lepton mass ratios are post-dictions.  
**Recommended fix:** Derive C from the E_g condensate dynamics; alternatively, downgrade the lepton spectrum claim from "prediction" to "consistency with one fitted parameter."

### C3. F91 gluon "forced even" proven only at free-propagator level
**Finding:** F91  
**Severity:** Medium — weakens a classification theorem  
The gluon argument (G1) proves colour coupling is branch-blind: [diag(U⁺,U⁻) ⊗ I₃, I₄ ⊗ exp(iθ·T)] = 0 to 1.1×10⁻¹⁶. This covers the linear (free) propagator. However, the SU(3) self-coupling (triple and quartic gluon vertices) is not analyzed for its branch structure. If the nonlinear self-coupling has any chiral component, the even classification would need revision. The finding states "confinement makes this unobservable" — pragmatically true, but weakens "forced" to "forced at the free-field level."  
**Recommended fix:** Prove the triple-gluon vertex is branch-blind, or downgrade from "forced" to "forced at linear level, consistent at interacting level."

### C4. Nucleon mass is consistency check, not prediction
**Finding:** F123  
**Severity:** Medium — mislabeled epistemic status  
m_p ≈ 3m_c is the standard NJL/constituent-quark result. The constituent mass m_c = 309.5 MeV comes from the NJL gap equation whose couplings {GΛ², m₀/Λ} are calibrated to f_π = 92.07 MeV (user-selected anchor). The −1.05% agreement is real but is a consistency check of the NJL calibration, not an independent zero-parameter prediction. Finding H2 labels this "PREDICTION."  
**Recommended fix:** Relabel to "CONSISTENCY (1 anchor)" or "PREDICTION (1 input: f_π)."

### C5. n–p mass splitting: +17% residual unexplained
**Finding:** F122  
**Severity:** Medium — quantitative claim overstated  
The model gives m_n − m_p = +1.51 MeV vs measured 1.293 MeV (+17%). The dominant error is the crude EM self-energy estimate (δ^EM_p − δ^EM_n ≈ 1.00 MeV, while lattice QCD+QED gives ~0.32 MeV). The current-quark masses used (m_u = 2.16, m_d = 4.67 MeV) are PDG inputs, not model-derived, so this is not a zero-parameter prediction despite the framing.  
**Recommended fix:** State explicitly that current-quark masses are external inputs; compute or adopt a better EM self-energy estimate.

### C6. α_s(M_Z) honest residual is +8.4%, not +1.3%
**Finding:** F144  
**Severity:** Medium — framing vs substance  
The loop expansion converges at +8.4%. The 1-loop +1.3% is acknowledged as "fortuitous." The title leads with "zero free parameters" while the scheme constant (Λ ratio 1.78) remains uncomputed (requires the model-action analog of the Hasenfratz one-loop constant). The finding is internally honest but the framing is optimistic.  
**Recommended fix:** Lead with the converged +8.4% residual; flag the scheme constant as an open calculation.

---

## Algebraic/Mathematical Errors

No outright algebraic errors were found. All equations checked are dimensionally consistent. The BCC unitarity identity u² + |ñ|² = 1 is verified to 6.7×10⁻¹⁶. The sympy derivations in F64, F79, F93, and F106 are internally consistent.

One potential issue: the `_bcc_uvec` sign correction on n_y (ca_bcc.py line 108) is verified necessary (unitarity breaks at 4.7×10⁻¹ without it), but the original reference document (qca-papers-1-4-overview.md) has not been updated to mark the error.

---

## Logical Gaps (derivation chains with missing links)

### G1. Rest-mass is posited, not derived from the QCA rule
**Finding:** F26, F27, F46  
F26 establishes c_lat = dΩ/d|k| at k→0. The mass m enters through the F27 mass step cos(m·dt)·I + i·sin(m·dt)·A, where m is a free parameter. F46 provides the geometric Pythagorean identity E² = p²c² + m²c⁴, but this is an identification, not a derivation. The gap: "c_lat is a rotation rate" → "rest mass is the zero-k rotation rate" is conceptual, not algebraic.

### G2. Paired-photon binding is kinematic, not dynamical
**Finding:** F69  
The photon is defined as a (+,−) bound pair with Ω_pair = ω⁺(k/2) + ω⁻(k/2). The binding mechanism — why two Weyl quanta form a bound state at zero binding energy — is acknowledged as open ("Two-body binding dynamics" in F69 §5). The construction is kinematic (sum of constituent rates) rather than dynamic (interaction potential producing a bound state).

### G3. Weinberg angle matching scale is NDA, not derived
**Finding:** F138  
sin²θ_W → 1/4 as g_X → ∞ (the 331-type cap) is exact algebra (WM1). But μ* = 4πv is naive dimensional analysis, not a lattice calculation. The running uses SM 1-loop beta functions, not CA-derived RGE coefficients. F143 bounds the fermion contribution at per-mille; the remaining E_g condensate phase stiffness f_{E_g} (>99.6% of the wrap stiffness) is uncomputed.

### G4. Charge quantisation not derived
**Finding:** F41, F51  
F51 derives that the bipartite sublattice DOF *carries* hypercharge. But the specific charge assignments (Y_L = −1, Y_{eR} = −2, Y_Q = +1/3, etc.) are SM values put in by hand via constants in the code. The quark charges ±2/3, ±1/3 are input via Gell-Mann–Nishijima Q = T₃ + Y/2 with Y values assumed.

### G5. g* = 48 depends on F75's physical hypothesis
**Finding:** F75, F79  
F75 derives dim(T₁u) = 3 from O_h representation theory (exact group theory). But F75's own status line states: "the physical identification (generation index = orbital shell irrep) is a stated hypothesis, not a theorem." The chain F75 → F79 inherits this. If the generation count differed, g* and hence a/ℓ_P would shift.

### G6. BPS coupling assumed in confinement derivation
**Finding:** F86  
The exact σ = 2πv²n holds only at the critical (type-I/II boundary) coupling λ = e². For general κ, σ = 2πv²n·ε(κ). No argument is given for why the QCD vacuum should sit at the BPS point. The confinement statement σ > 0 holds for all κ (good), but the numerical tension value used in the A↔C bridge is BPS-specific.

### G7. Block-spin commutativity proven only for free propagators
**Finding:** F130  
[R_b, R(Ω)] = 0 to 2.9×10⁻¹⁴ is verified for the free propagator only. For matter-coupled propagators where Ω depends on local fields (dielectric K, gauge links), the block-averaging and rotation do not obviously commute. The multi-scale program (F159/F160) rests on this unproven extension.

### G8. U(x) "pure gauge" terminology confusion
**Finding:** F41, F34b  
F41/F42 state U(x) is "pure gauge" (no kinetic term). But F34b's Stueckelberg mechanism provides (f²/2)tr|D_μU|² — which IS a kinetic term making three of U's four DOFs physical (eaten by W±, Z). U(x) is not truly "pure gauge" in the usual sense. This is terminological confusion, not algebraic error.

---

## Omissions (physics that should be in the model but is absent or unaddressed)

### Acknowledged in docs/roadmaps

| Omission | Status | Where acknowledged |
|----------|--------|--------------------|
| CKM mixing matrix | Not derived; F54 flags as future work | F54 §6, F75 §6 |
| PMNS matrix | Not derived | F47 |
| Current quark masses | Not derived; PDG inputs used | F116 §9 |
| Overall mass scale N = 5.5×10⁻¹⁹ | Open hierarchy problem | F119 (explicit no-go) |
| Quark-sector E_g extension | Identified but not built | F116 §9 |
| √σ/f_π from first principles | 12–29% residual | F124 §5 |

### Not acknowledged or insufficiently flagged

| Omission | Severity | Notes |
|----------|----------|-------|
| **Gravitational wave equation** | High | No dynamic (hyperbolic) equation for K perturbations; GW170817 is a hard constraint |
| **Electron g−2** | High | No mention anywhere in findings; the most precisely tested QED prediction (10⁻¹²) is unaddressed |
| **Cosmological constant** | High | F59 identifies the Λ⁴ integral but no finding computes the CC or explains why it's small; the model inherits the standard 120-order-of-magnitude problem |
| **Strong CP at loop level** | Medium | F53: θ = pure gauge at tree level (P5, 3.3×10⁻¹⁶); whether θ_QCD = 0 survives loops is unaddressed |
| **W/Z masses in GeV** | Medium | Ratio m_Z/m_W predicted to 1.8%; absolute masses require v (external) |
| **Double-group caveat for 3 generations** | Low | F75 §7: O_h' has a 4D spinor irrep G_{3/2}; exclusion relies on generation ≠ spin assumption |

---

## Inconsistencies Between Findings

### I1. F49 sin²θ_W = 2/9 vs F138 sin²θ_W = 1/4
F49 gives 2/9 from sublattice/bond counting; F138 gives 1/4 from the embedding cap. F138 §5 attempts reconciliation: 2/9 is the "on-shell endpoint" and 1/4 is the "UV cap." The bridge (ratio 8/9) is not yet derived. F141 reframes 2/9 as an on-shell mass statement m_W²:m_Z² = 7:9, which is PDG-compatible to −0.063%, but the connection between the two values remains unbuilt.

### I2. F45 mass ratio vs F138 running angle
F45 predicts m_Z/m_W = 2/√3 = 1.1547 from the bare angle 1/4. F138's running gives sin²θ_W(M_Z) = 0.23173, which implies m_Z/m_W = 1/√(1−0.23173) = 1.1408. These are not mutually consistent (+1.2% discrepancy). The model needs to specify which on-shell relation holds.

### I3. Composite-to-gauge photon transition cost
F67/F68/F69 retire the σ-bilinear as the photon but keep it for W/Z/gluon. The SU(2) W-triplet bridge (F29) was built on the bilinear — with the photon separated, the bridge's photon leg is severed. F89 attempts reconciliation ("singlet bilinear IS the paired photon"), but the EM photon and W boson no longer share the same composite structure. Whether this matters physically is unaddressed.

---

## Minor Issues (notation, precision claims, documentation)

| # | Issue | Location |
|---|-------|----------|
| M1 | F87 Gauss residual (2×10⁻¹²) scaling with L and t not reported; 10⁻¹² is 3 orders above other machine-precision claims | F87 |
| M2 | F116 lattice-BZ NJL uses simple-cubic dispersion; should use BCC for quantitative claims | F116 |
| M3 | F94 Monte-Carlo string tension from smoke run (L=6); production values (L=10) needed for precision | F94 |
| M4 | F26 states c_lat "is not a propagation speed" while defining it as dΩ/d\|k\| (which IS the group velocity); philosophically provocative but mathematically identical | F26 |
| M5 | F105 "all k" claim should emphasize the natural BZ cutoff \|k\| ≤ π√3 ≈ 5.44 | F105 |
| M6 | ca_bcc.py sign correction on n_y not cross-referenced back to qca-papers-1-4-overview.md | ca_bcc.py:108 |
| M7 | F41 cites `test_hypercharge_fork.py` but file is named `test_hypercharge.py` | F41 |
| M8 | F26 (speed-of-light finding) doesn't cite its test file in the header, though `test_f26_rotation_law.py` exists | F26 |
| M9 | F161 (atomic emission) is noticeably thinner than other findings; lacks structured test table and results-JSON path | F161 |
| M10 | F118 λ₆ inherits ~1% uncertainty from the BZ lattice-size-dependent sea integral B (L=24 convergence) | F118 |
| M11 | F125 hydrogen ground state uses Schrödinger/Dirac solver with external m_e and α, not a CA-specific calculation; validates "model contains QM" but does not test lattice corrections | F125 |

---

## Verified Correct (things explicitly checked and found sound)

| # | Claim | Finding | Verification |
|---|-------|---------|--------------|
| V1 | BCC unitarity u² + \|ñ\|² = 1 forces dispersion Ω(k) | F01, ca_bcc.py | Algebraic identity; verified to 6.7×10⁻¹⁶ over 10⁴ random k-vectors |
| V2 | c_lat = 1/√3 exact and is an RG fixed point | F25/F26, F129 | Follows from H_W = (1/√d)σ·k; eigenvalue b⁰ = 1 under blocking for b ∈ {1–5} |
| V3 | On-axis Ω_pair(k x̂) = \|k\|/√3 at all k (not just small k) | F105 | Algebraic: s_y = s_z = 0 on axis; max residual 2×10⁻¹⁴ |
| V4 | F27 SU(2)_L Ward identity and mass-step unitarity | F27 | cos+i·sin of Hermitian structure; T5 residual 1.1×10⁻¹⁷ |
| V5 | Hypercharge absorption into U(x); Gell-Mann–Nishijima exact | F41/F42 | All 15 Ward identities pass at machine precision |
| V6 | Paired photon non-birefringence | F68/F69 | U(1) as identity in branch space → even channel forced; PP2 Stokes = 1.8×10⁻¹⁵ |
| V7 | F91: γ even (forced), W± chiral (forced) | F91 | Q_L − Q_R ≡ 0 (ℚ-exact); T₃ᴿ = 0 (ℚ-exact); ‖P_L ψ_R‖ = 0.0 |
| V8 | F54 β-decay: V−A structure, conservation laws | F54 | Charge/B/L/B−L conserved exactly (ℚ); G_F/√2 = g²/(8m_W²) at q²=0 to 4.2×10⁻¹⁷ |
| V9 | F64 dielectric gravity: AB ≡ 1 derived (not imposed) | F64 | Chain: proper rotation → Z=1 → ε=μ=K → A=1/K, B=K → AB=1 |
| V10 | F64 PPN: β = γ = 1 (GR-identical) for K = e^{2u} | F64 D-EM9 | Specific to exponential form; linearised K = (1−u)⁻² gives β=1/2 (excluded by Mercury) |
| V11 | F79 structural G: closed form, tracelessness kills tree stiffness | F79 | T^μ_μ(EM) = 0 in 3+1D; forces loop/induced channel |
| V12 | F106 sourcing coefficient purely structural | F106 | Reduces to a²c_lat/(ħc); no free coupling (E1, sympy) |
| V13 | F93 E_g uniqueness theorem | F93 | sym(T₁u ⊗ T₁u) = A₁g + E_g + T₂g; exact integer arithmetic over all 48 O_h ops |
| V14 | F73 mass cap m_c ≤ 1/√2 from pair-sum kinematics | F73 | Over-wrap bound; top quark m_lat ~ 5×10⁻¹⁷, far below cap |
| V15 | F92 triple saturation condition exact | F92 | sympy solveset returns {π/4}; data c² = 2.000018 vs Fock value 2 |
| V16 | F75 three generations from O_h irrep selection | F75 | No 4D single-valued irrep; parity selects unique odd triplet T₁u |
| V17 | F47 seesaw scaling | F47 | Machine precision across M_R/M_D from 3 to 10⁵ |
| V18 | F86/F94 confinement: BPS tension exact; A↔C bridge algebraic identity | F86, F94 | σ = 2πv²n verified by sympy; CMP2 residual 10⁻¹⁶ |
| V19 | F130 Gauss's law under blocking | F130 T3a | Z-flux divergence telescopes exactly; residual ≡ 0 |
| V20 | Finding file quality: derived-vs-assumed clarity consistently good | Sample of 10 | All have dates, equations are dimensionally consistent, tests exist |

---

## Recommended Priority Fixes

1. P**Derive a gravitational wave equation** from the dielectric rotation rule and prove c_grav = c_lat = 1/√3. Without this, GW170817 potentially falsifies the gravity sector. *(Critical — C1)*

2. P**Derive the sextic brake C (λ₆)** from the E_g condensate dynamics, or honestly relabel the lepton spectrum as a one-parameter fit. This is the single most impactful open coefficient. *(Critical — C2)*

3. W,D**Analyze the triple-gluon vertex branch structure** to either upgrade the gluon "even" classification to fully proven, or document it as a free-field result. *(Critical — C3)*

4. **Relabel prediction tiers** throughout F122, F123, F144 to distinguish zero-parameter predictions from consistency checks and NDA-dependent results. *(Critical — C4, C5, C6)*

5. W,D**Derive charge quantisation** from the lattice structure (close the F51 → Y-value gap), or document the SM hypercharge assignments as model input. *(Logical gap — G4)*

6. **Close the F49/F138 Weinberg angle bridge**: derive the relationship between the on-shell 2/9 and the UV cap 1/4. F141's WS-cell reframing is promising but incomplete. *(Inconsistency — I1)*

7. **Compute the E_g condensate phase stiffness f_{E_g}** to close the Weinberg matching scale from NDA to exact. *(Logical gap — G3)*

8. **Attempt a g−2 calculation** for the electron. If the paired-photon propagator is correct, the 1-loop QED vertex correction should be computable and is the most powerful precision test available. *(Omission)*

9. **Migrate F116 NJL from simple-cubic to BCC dispersion** for quantitative consistency with the model's own lattice. *(Minor — M2)*

10. P**Address the cosmological constant** at least at the level of identifying the cancellation mechanism or acknowledging the 120-order problem explicitly in a finding. *(Omission)*
