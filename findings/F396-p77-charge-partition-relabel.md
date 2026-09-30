# F396 — The p.77 charge partition: Leg A's premise is false in the model, and the partition is F27's Stueckelberg Ward structure, with the W± sink refuted in unitary gauge

*2026-09-21 - 12:30 · sector `gauge` · module `casim.engine.gauge.derive_charge_partition` (new) · record `F396-charge-partition-p77` (tier gate)*

**Status:** Confirmed as a **disposition** — 14/14 legs PASS, three declared controls verified red. Disposition **(b) closed as a relabel with no predictive content**; the strong form ("W± is the physical charge sink of the mass step") is **not supported by the model** (see §4–5). Class: the Leg B charge results are machine-precision but largely guaranteed by the species-diagonal structure of the F27 coupling (§4); Leg A's J_z ratios are numerical thresholds, not machine results.
**Reviewed:** 2026-09-21 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F396-review-2026-09-21.md))
**Test record:** record `F396-charge-partition-p77` (tier gate) — `tests/registry/gauge.yaml`, D9. Declared 2026-09-21 - 12:30.
**Claim:** [CL308](../docs/claims/CL308-p77-charge-partition-is-f27-stueckelberg-relabel.md)
**Source:** `references/physics-notes-complete.md` pp.76–77 (primary), 90–91, 103–104; audit `docs/audits/physics-notes-complete-review.md` §4.2.

## 1. What was tested

p.77: the weak mass term "violates charge conservation" exactly as the free-Dirac mass term "violates spin conservation"; J = L + S rescues the latter, so charge is "partly intrinsic, partly not", the non-intrinsic part becoming W±, and mass then arises "from another field". A candidate alternative to F27's β-gauging. Two legs, both checked in the model's own kernels.

## 2. Leg A — the analogy's premise, in `particles.dirac_bcc`

| Quantity | Result | Class |
|---|---|---|
| Mass-step-alone change of ⟨Σ_z⟩ | **2.8×10⁻¹⁷** — the mass step is the pointwise η↔χ rotation and [Σ, β] = 0 | machine |
| Full step: ⟨S_z⟩ swing over 12 ticks (m=0.2) | 0.107 (k₀≈0.18), 0.215 (k₀≈0.58): spin *is* exchanged, but by the **kinetic** step | numerical |
| ⟨J_z⟩ swing / ⟨S_z⟩ swing (mean over 4 seeds; single-seed range 0.04–0.11 small k, 0.06–0.30 large k) | **0.068** at small k, **0.218** at large k — conserved only in the continuum limit; drift scales ≈ linearly in k | numerical |
| Lattice point group of the BCC Weyl block | **D₂** (C₂ₓ, C₂ᵧ, C₂z: 1.1×10⁻¹⁶); C₄z and C₃ fail (1.47) | machine |
| Spin generator | the block is A ≈ 1 − i k·σ*/√3 (conjugate rep): S_z = −σ_z/2; the naive +σ_z/2 gives a J_z swing ≈ 2× the S_z swing | machine (low-k residual 5×10⁻⁵ ∝ k) |

**Outcome (ii) with a twist.** The premise "the mass term flips S_z" is **false in this representation**: the mass step conserves Σ exactly. What it flips is *chirality* (η↔χ, the γ₅ eigenvalue). The notebook says as much itself on p.91 ("the mass term … does not mix handedness — i.e. it conserves helicity/spin"). And J_z is conserved only to O(k), because the exact lattice group is D₂, not SO(2): there is no exact ⟨L_z⟩. The analogy's correct transcription is therefore **chirality-linked charges (T₃, Y) ↔ the thing the mass violates; Q ↔ what survives** — which is Leg B.

## 3. Leg B — per-tick charge bookkeeping of the F27/F41 mass step

Hypercharge kernel `gauge.hypercharge.mass_step_doublet_su2xu1y`, random states, random pointwise U(x) ∈ SU(2) and α(x), 40 samples.

1. **Q = T₃ + Y/2 is an exact operator identity** on (ν_L, e_L, ν_R, e_R) (Fractions) — no correction term. The neutral-charge form of pp.103–104, Q′ = (t₃ − sin²θ Q)/(sinθ cosθ) = t₃ cotθ − t₀ tanθ with t₀ = Q − t₃, holds to 4.4×10⁻¹⁶; at sin²θ = ¼ (F138) the coefficients are √3 and 1/√3 = c_lat.
2. **Exact ΔQ of the mass step.** In the unitary-gauge frame η̃ = U†η the step is diagonal in isospin and **ΔQ = 0 to 2.2×10⁻¹⁶**, for any U, α. Simultaneously **ΔT₃ = −ΔY/2 ≠ 0** (max 2.6×10⁻² per sample): the mass step violates the *weak* charges and conserves the electric one. Measured on the raw η, ΔQ ≠ 0 (max 3.2×10⁻²); for a pure-η_e state it is **exactly ΔQ = +sin²(m·dt)·|b|²·‖η_e‖²** (residual 1.5×10⁻¹⁶), zero at b = 0 — a frame artifact.
3. **Equality with F54's W charge — FAILS.** F54's charged current is the left-handed bilinear J⁺ = η_ν*η_e. On the pure-η_e state J⁺ ≡ 0 to machine zero while the raw-frame ΔQ is finite. They are different objects: the raw-frame ΔQ is a mixed-chirality (η–χ) gauge artifact; F54's is a species-level Q-conserving vertex. There is no tick-for-tick identity, and the hoped-for equality is **not** available.
4. **The discriminator (U = I, α = 0).** The mass step is fully allowed, ΔQ = 5.6×10⁻¹⁷, ΔT₃ = 6.9×10⁻³, ΔY = 1.38×10⁻². p.77's strong reading ("no field leg → mass step forbidden on the charge-changing component") is not what the model does: at U = I there is **no charge-changing component** (the step is isospin-diagonal), and the T₃/Y-violating chirality flip is **allowed and is the mass**. The β-gauging reading is right about the mass gap.
5. **The Ward identity (F27, restated, not re-attacked)**: V·step(ψ;U) = step(Vψ;VU) at 2.8×10⁻¹⁷.

## 4. The sharp point — who absorbs the missing T₃

*Caveat (review): ΔT₃ = −ΔY/2 follows algebraically from ΔQ = 0 plus Q = T₃ + Y/2, and ΔQ = 0 in unitary gauge is guaranteed because the F27 coupling is species-diagonal (ν↔ν, e↔e). The legs verify the kernel implements this, not that it could have come out otherwise; the control `mass_mixing=charged` shows the Q leg is a property of the F27 coupling. The result is the Standard-Model statement (mass breaks T₃ and Y, preserves Q; the Goldstones are eaten) — no prior art is exceeded.*

Because ΔT₃ = −ΔY/2 identically, the T₃ the mass step removes is **absorbed by hypercharge** (the neutral α/B direction, F41), not by a charged carrier. In unitary gauge the W± have **no role in the bookkeeping** of the mass step. The off-diagonal U entries b (the would-be "W± leg") appear only in a frame where U is not diagonal — i.e. they are the Goldstone/Stueckelberg directions that gauge-transform away, exactly as the Ward identity says. So:

- p.77's **weak form** — the conserved charge is (fermion part) + (U-part) under the joint transformation U → VU, ψ → Vψ — is *exactly* F27's Ward identity, already in the tree. A relabel: *"intrinsic + field leg" = "ψ + Stueckelberg U"*.
- p.77's **strong form** — W± as a physical charged field that carries the missing charge — finds no role in the model: for the diagonal part the missing T₃ is balanced by the neutral (hypercharge) direction, and the off-diagonal part is gauge. This is a consequence of the F27 coupling being Q-neutral, as in the SM, not an independent refutation.

## 5. Constraints and disposition

- **F143.** The field leg would need its own kinetic term to be a dynamical charge sink. The transverse induced wrap stiffness of U is **exactly zero** (F42's wrap is conjugation) and the longitudinal is 0.16–0.36 % of v². So the F42/F143 fermion loop cannot supply the stiffness p.77 needs; U stays a pure-gauge compensator and the kinetic sector remains F41's open problem. Not a new no-go — it is F143 applying to this reading.
- **F320.** m_W, m_Z are already absolute predictions from ρ = 1 and rank. Nothing in p.77's partition adds or changes a parameter (b carries none), so it neither reproduces nor competes with them.
- **Mass half.** Does the partition predict anything about mass? **No — it relabels.** The mass step's ΔT₃ is fixed by m·dt as an input (closed form in §3.2); the notebook's pp.10–11 self-field-energy hierarchy is independent of the partition.
- **Audit §4.2** ("A ↔ S, W ↔ Q", pp.62–67, 90): the Leg A/B mirror above is its content in this model — the mass conserves Σ and Q and violates chirality, T₃, Y. It does **not** derive sin²θ_W; that stays with F138/F49/F45. §4.2 is closed as "recorded, relabel", not as a Weinberg-angle derivation.

**Disposition: (b)** relabel, no predictive content; strong form not supported (neutral direction balances ΔT₃ in unitary gauge; F143 gives the leg no fermion-loop stiffness, which does not exclude other routes). Not (a): the step-2 equality does not hold.

## 6. Limits

- Leg A's J_z numbers are from one seeded random-spinor packet (L = 32, 12 ticks); the *ratio* and its growth with k are stable, the exact values are packet-specific. The D₂/C₄ statement is exact on the block, not a claim about the full many-site dynamics.
- Charges are the Fraction quantum numbers of the F41/F42 convention (Y(e_R) = −2, Y(ν_R) = 0). The ν_R assignment is a convention of the existing kernel.
- Leg B's raw-frame ΔQ is a foil, not a serious rival; the F54 comparison (§3.3) is a "not the same object" statement, not a discriminating test. Only the pointwise mass step was analysed; the kinetic step's charge conservation is F27/F41/F54's.

## 7. Sources
`findings/F27-complex-mass-chiral-su2.md`, F41, F42, F54, F138, F143, F320; notebook pp.76–77, 90–91, 103–104.
