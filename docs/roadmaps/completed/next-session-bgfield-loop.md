# Next-session prompt — the background-field one-loop gluon self-energy → **pin q\***

`2026-06-16 - 23:55` — handoff. Paste the **Prompt** block below into a fresh session. This is the final, isolated computation of the strong-sector UV face: the matching scale **q\***. Everything around it is already done and validated; this sub-project computes the one finite number it reduces to. Exact paths/numbers in §Reference.

> **Target:** q\* a = exp(−d₁/2b₀^α) = **0.733** ⇔ Λ_MS̄/Λ_rule = **1.78** (NOT Wilson's 28.81). The whole problem = one finite number, the gluonic **d₁ ≈ 0.348** (1/α units).

---

## PROMPT (paste this)

> You are continuing the "universe in a bottle" QCA project — the final step of the strong-sector UV face: computing the matching scale q\* from the one-loop background-field gluon self-energy. Read `docs/design/qstar-gluon-d1-computation-plan.md` and `findings/F155-qstar-self-energy-and-freeze-bracket.md` first. Work to algebraic/machine exactness; **validate before trusting any number**; be scrupulously honest about scope. If a step doesn't close, say so — a wrong q\* is worse than an honest "not yet."
>
> **What is already DONE and VALIDATED (build on, do not rebuild):**
> - **q\* is bracketed** to [1/√3, ~0.97] with the implied 0.733 inside; Λ-ratio O(1), not Wilson (F155-A5, `ca_gluon_self_energy.py`).
> - **Tadpole sector is exactly empty** (F26 link exactly SO(2), u₀≡1; Wilson Z₀=0.1549 structurally absent) — F155-A0, machine precision. So the rule's d₁ is *purely* the gluon+ghost vertex finite part (no tadpole).
> - **Moment route is dead** (F155 §6.1 moment-insensitivity theorem): the LM scale is numerator-insensitive (~0.97 for scalar/k²/gluon/transverse), so the shift to 0.733 is *entirely* the finite vertex-dependent d₁. No moment/shortcut works.
> - **The 3-gluon vertex is validated**: numerically (`ca_lpt_vertex.py` — propagator, colour antisymmetry, full Bose symmetry, all machine precision) AND symbolically via the **Ward–Takahashi identity** p₁·Γ = Δ⁻¹(p₃)−Δ⁻¹(p₂) for all components (`ca_lpt_ward.py`, test 2/2). Continuum tensor Γ_{μνρ}=δ_{μν}(p₁−p₂)_ρ+cyc.
> - **The BZ-integration core + continuum subtraction are validated**: tadpole Z₀→0.154933 and the exact sum rule ∫k̂²/K̂=1/4 (`ca_lpt_wilson.py`, test 3/3); the subtracted-bubble d₁ machinery is n-convergent (`ca_gluon_self_energy.subtracted_bubble_constant`).
> - **A scaffold is waiting**: `ca-simulation/ca_bgfield_loop.py` wires in all the above and has explicit stubs (`bgfield_3gluon_vertex`, `bgfield_ghost_vertex`, `self_energy`, `b0_gate`, `d1_and_qstar`) — fill these in.
>
> **The one critical lesson (do not relearn the hard way):** b₀ = 11/3·C_A is recovered from the self-energy **only in the BACKGROUND-FIELD formalism** (Z_g = Z_A^{−1/2}, so b₀ comes from Π alone). Ordinary **Feynman-gauge Π is NOT transverse by itself and will NOT give b₀** without the vertex correction. So assemble the loop with the **background–quantum–quantum** vertices, not the plain ones.
>
> **Steps (each with a validation gate — pass it before moving on):**
>   1. **Background-field vertices.** Derive the bgfield 3-gluon vertex (and ghost-gluon vertex) by the split U = e^{iaA_bg}e^{iaq}, expanding the plaquette action to O(A_bg q²). Recommended: **sympy** symbolic expansion (extend `ca_lpt_ward.py`), cross-checked against the numerical extractor `ca_lpt_vertex.py`. **Gate:** the bgfield vertex must reduce to Γ_{μνρ} (the Ward-verified continuum tensor) in the a→0 limit, and carry the cos(k_μ/2) point-splitting form factors.
>   2. **Assemble Π_{μν}(p).** Gluon loop (½ × bgfield-vertex² × DD) + ghost loop (bgfield-ghost² × 1/K 1/K); tadpole/seagull = 0 (A0). Use the validated `ca_lpt_wilson.bz_integral` core. Transverse-project → Π(p²) = b₀ g² p²[ln(1/p²a²) + C].
>   3. **b₀ GATE (do this on the WILSON action first).** Assemble the Wilson-action background-field Π and confirm it gives **b₀ = 11/3·C_A = 11** (pure gauge) to a few %. This validates the whole pipeline against a known action. Only then swap in the rule propagator (K_rule = 3·Ω_even²) + the rule vertices and drop the tadpole.
>   4. **d₁ → q\*.** d₁ = b₀-normalised (C_lat^rule − C^MS̄) via the validated continuum subtraction; q\* a = exp(−d₁/2b₀^α); Λ-ratio = exp(d₁/2b₀^α). **Target q\* a = 0.733, Λ-ratio = 1.78.** If it lands near Wilson's ~29, the g_s=½ lock is falsified — A0 (exact tadpole-emptiness) makes that structurally impossible, but report honestly either way.
>
> **Sandbox note:** the 4D BZ quadrature at production resolution (n≥64) exceeds the 45 s cap — build a native runner `tests/runners/run_bgfield_loop.py` (JSON out, progress heartbeat, RAM/time notes) for Ben to run, mirroring `run_lpt_wilson_validation.py`. Prototype at small n in-sandbox.
>
> **Deliverables:** fill in `ca_bgfield_loop.py`; `tests/findings/test_F<n>_bgfield_loop.py` (the b₀ gate + d₁/q\* if it closes); results JSON; native runner; a finding `findings/F<n>-*.md` (check `findings-index.md` for the next free number — concurrent sessions take numbers); exactness rows; changelog; `python3 tools/regen_indexes.py`; memory pointer; update `docs/status/qcd-ir-coupling-problem-status.md` §5 Residual A and `docs/design/qstar-gluon-d1-computation-plan.md` to the outcome. **Be honest about scope** — if the b₀ gate doesn't pass, stop there and report; if d₁ only brackets q\*, say so.

---

## Reference (exact paths, status, numbers)

**Scaffold to fill:** `ca-simulation/ca_bgfield_loop.py` (stubs + wired-in validated ingredients; run `python3 ca_bgfield_loop.py` for the status map).

**Validated modules (build on):**
- `ca_lpt_ward.py` — continuum vertex Γ + Ward identity (symbolic, 2/2). Extend here for the bgfield vertices.
- `ca_lpt_vertex.py` — numerical vertex extractor (propagator, colour antisym, full Bose; 3/3). Cross-check tool.
- `ca_lpt_wilson.py` — BZ-integration core + Wilson tadpole Z₀ + sum rule (3/3); `bz_integral` is the quadrature engine.
- `ca_gluon_self_energy.py` — F155: tadpole-empty (A0), luminal gluon (A1), subtracted-bubble d₁ machinery (A3), q\* bracket (A5), moment-insensitivity (A6). `K_true_4d` = rule propagator kernel.
- `ca_scheme_constant.py` — F151: `a1()` (=11/3 exact), `implied_qstar()` (0.7327), the band.

**Findings:** F151 (V-scheme, a₁, q\* band), F155 (tadpole-empty, moment-insensitivity, bracket, Ward identity, vertex extractor), F154 (B solved, A cheap route out), F144 (lock, running), F129/F130 (near-perfect action — why the abelian piece sits at the band top).

**Targets (falsification-sharp):**
- b₀ gate: **11/3·C_A = 11** (pure gauge, n_f=0) from the assembled bgfield Π — on Wilson FIRST.
- q\* a = **0.7327** ⇔ Λ_MS̄/Λ_rule = **1.78** ⇔ α_s(M_Z)=0.1180, Λ³_MS̄=347 MeV (FLAG 343(12)).
- d₁ = **0.348** (1/α units); q\* a = exp(−d₁/2b₀^α), b₀^α = (11−2n_f/3)/4π.
- Wilson contrast: Λ_MS̄/Λ_L = **28.81** (Λ_L=0.03471 Λ_MS̄) — the rule must NOT come out near this (tadpole-free, A0).

**Key external references** (fetch as needed):
- Abbott, *The background field method* (Nucl. Phys. B185, 1981) — bgfield vertices, Z_g = Z_A^{−1/2}.
- Capitani, *Lattice perturbation theory* (Phys. Rept. 382, 2003) — lattice gluon vertices, form factors, the Wilson d₁.
- Lüscher–Weisz — bgfield LPT on the lattice.
- Kogut–Susskind 1975; Hamer et al hep-lat/9706017 — the Hamiltonian-scheme (the rule is Hamiltonian/real-time; the matching is the KS-scheme Λ, smaller/tadpole-free than Wilson).

**Pitfalls:**
- **Use background-field gauge** (the b₀ gate fails in Feynman gauge — verified 2026-06-16).
- The numerical extractor gives the *permutation-summed, cos-doubled* amplitude — good for symmetry checks, NOT for a clean single-vertex contraction (it failed a direct Ward contraction). Use the symbolic vertex for the loop; use the extractor only as a cross-check.
- q\* is the UV-finite *subtraction*, not a bare moment (F154/F155). Always subtract the continuum.
- Concurrent sessions take F-numbers — verify the next free number before writing files.
- Validate the pipeline on Wilson (known 28.81 / b₀=11) BEFORE trusting the rule's number.
