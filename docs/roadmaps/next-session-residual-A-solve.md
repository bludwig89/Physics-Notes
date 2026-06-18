# Next-session prompt — build out Residuals A & B, then **solve/derive Residual A**

`2026-06-12 - 20:10` — handoff. Paste the **Prompt** block below into a fresh session. Everything it needs is in this repo; exact paths are in §Reference. The goal is the single remaining strong-sector number: the UV matching scale **q\*** (≡ the rule→MS̄ scheme constant), target **q\* = 0.733/a** ⇔ Λ_MS̄/Λ_rule = 1.78. Residual B is already solved (F154); this session finishes B's loose end and solves A.

---

## PROMPT (paste this)

> You are continuing the "universe in a bottle" QCA project. Read `docs/status/qcd-ir-coupling-problem-status.md`, then findings **F151** (UV scheme constant, V-scheme + a₁), **F152** (IR face), and **F154** (the A/B build: B solved, A's cheap route ruled out). Your job: **build the full one-loop machinery for Residual A and derive q\*** (the matching scale), and tighten Residual B's freeze-value. Work to algebraic exactness first, then machine precision; document everything as a new finding (check `findings-index.md` for the next free F-number — concurrent sessions have been taking numbers, so verify before writing).
>
> **What is already nailed (do not re-derive, build on):**
> - The bare lock is exact: g_s² = 1/4 ⇒ α_s(μ₀)=1/16π at μ₀=ħc/a=1.85×10¹⁸ GeV (F144).
> - The rule's coupling **is the V-scheme (static-potential) coupling**, tree-exact, because the lock normalises F110's static energy V(R)=½g²q²R (F151 S1). So the one-loop conversion V→MS̄ is the **known** constant a₁=(31C_A−20T_F n_f)/9 = 11/3 (n_f=6); Δ(1/α)=a₁/4π=0.2918 exact.
> - The full needed shift is Δ(1/α)|_μ₀ = 0.640 = **0.292 (a₁, exact)** + **0.348 (the q\* piece)**, with q\*=0.733/a implied by α_s(M_Z)=0.1180 and lying in the geometric band [1/√3, 1]/a (F151).
> - The conversion is O(1)≈1.8, NOT Wilson's 28.81, because the rule is a near-perfect action (F129 irrelevant LIV) with **exactly unitary links ⇒ no tadpole** (F151 S2; the Wilson Z₀=0.1549 term is structurally absent).
> - **F154 ruled out the cheap route**: the gluon-propagator log-moment gives UV scales (⟨lnK⟩_4D=2 ⇒ e/a; 1/K-weighted 2.30/a), above the band. q\* is the **UV-finite lattice−continuum subtraction**, not a bare moment.
>
> **Residual A — TWO routes; do Route A-NP first (cleaner), then A-PT to cross-check:**
>
> **Route A-NP (nonperturbative, model-native — recommended first).** The model has its own RG: F130-C1 established the block-spin flow g²_coarse = b·g²_fine with confinement the one relevant direction. Use **step-scaling** (à la the ALPHA/twisted-gradient-flow programme, arXiv:1702.06289) to measure the running coupling vs scale directly, with no lattice PT and no gauge-fixing:
>   1. Define a renormalised coupling from a model observable at scale 1/L — the **static-potential (V-scheme) coupling** α_V(1/L) from F110/F146's measured V(R) (Coulomb coefficient of the short-distance potential), or the F130 block-spin step function.
>   2. Run from the BZ-edge bare value (α=1/16π) down through block-spin steps; read off the scale at which α_V equals the bare lock — that scale **is q\***.
>   3. Cross-check against the F146 SU(3) static potential (the high-res CASIM run below measures α_V(q) and σ independently).
>   - Success: q\* = 0.733/a (±band), equivalently the run reproduces α_s(M_Z)=0.118 and Λ³_MS=347 MeV (FLAG 1.1%, F151 S4).
>
> **Route A-PT (analytic one-loop background-field LPT — the rigorous closer).** Build `ca-simulation/ca_gluon_self_energy.py`:
>   1. **Action.** The gauge sector is the Kogut–Susskind Hamiltonian H=(g²/2)Σ Ê² − λ Σ cos φ̂_p (F110, `ca_link_hamiltonian.py`) / the F26 real rotation (`ca_wmu._f26_rotation_step`). Use the **Hamiltonian-scheme** LPT (Kogut–Susskind 1975; Hamer et al hep-lat/9706017) — the model is real-time/Hamiltonian, NOT Euclidean Wilson, so the matching is the Hamiltonian Λ-parameter, which has its own (smaller, tadpole-free) structure. Do not blindly copy the Wilson d₁=5.88.
>   2. **Background field split** U = e^{iaA_bg} e^{iaq}, expand to quadratic in the quantum field q; extract the gluon propagator and the 3-/4-gluon (+ghost, if covariant gauge) vertices on the BCC BZ.
>   3. **One-loop self-energy Π(p)** and the coupling renormalisation Z_g; the matching constant is the **UV-finite part after subtracting the continuum log** (this is the piece F154's moment missed). Confirm the tadpole sector is empty (u₀≡1) as F151 S2 argued.
>   4. **q\*** = the BLM scale of that finite part. Success criterion identical to Route A-NP: q\* = 0.733/a / Λ-ratio 1.78. If it lands near Wilson's ~29, the g_s=½ lock is falsified — report honestly either way.
>
> **Residual B — finish the loose end (B's machinery is solved, F154/`ca_gap_solve.py`):** the inverse solve gives α_eff*=0.376/0.411 by **imposing** M(0)=311 MeV. Two open sub-items: (i) derive the **freeze value** 0.39 from the saturation/decoupling mechanism *without* anchoring M(0) (the naive running overshoots 5×, so the freeze is genuine nonperturbative physics — connect it to the F117 gap-massive propagator and the F101 Gaussian→confinement crossover); (ii) M(0)'s absolute MeV scale comes from A — so once A closes, re-run B to output m_c, f_π (proper Pagels–Stokar, F124) and λ₆ (F150) with no anchor.
>
> **Verification:** run `tests/runners/run_residual_AB_highres.py` (high-L B + high-n log-moment) and the CASIM static-potential command in §Verification of this doc; read the JSON back to confirm convergence at production resolution. Add a `qstar_highres()` entry point to `ca_gluon_self_energy.py` so the runner's A-hook fires.
>
> **Deliverables:** new module(s), a `tests/findings/test_F<n>_*.py` (5/5), results JSON, a finding `findings/F<n>-*.md`, exactness rows, changelog entry, `python3 tools/regen_indexes.py`, and a memory pointer. Update `docs/status/qcd-ir-coupling-problem-status.md` §5 Residual A to "solved" (or sharpened) per the outcome. **Be honest about scope** — if A only brackets q\* rather than pinning it, say so.

---

## Reference (exact paths & numbers)

**Findings:** `F144` (lock, running), `F145` (Fierz 2/9, linearised gap), `F151-scheme-constant-determined` (V-scheme, a₁, q\* band), `F152-ir-coupling-the-irface` (IR face, branch), `F154-residuals-A-B-built-and-solved` (B solved, A cheap route out), `F129/F130` (block-spin RG), `F110` (KS link Hamiltonian), `F146` (SU(3) static potential / σ).

**Modules:** `ca_gap_solve.py` (B, built), `ca_qstar_logmoment.py` (A cheap route, built), `ca_scheme_constant.py` (F151: `a1()`, `corrected_chain()`, `implied_qstar()`), `ca_alpha_s_running.py` (F144 running), `ca_njl_induced_coupling.py` (F145 kernel), `ca_link_hamiltonian.py` (F110), `ca_wmu.py` (`_f26_rotation_step`), `ca_strong.py` (SU(3)). **To build:** `ca_gluon_self_energy.py`.

**Targets (falsification-sharp):**
- q\* a = 0.7327 (≡ Δ(1/α) scale piece 0.348; ≡ α_s(M_Z)=0.1180; ≡ Λ³_MS=347 MeV, FLAG 343(12)).
- Λ_MS̄/Λ_rule = 1.78 (Wilson 28.81 — must NOT come out near Wilson).
- a₁(6)=11/3 exact (already in `ca_scheme_constant.a1`).
- band [1/√3, 1]/a = [0.577, 1.0]/a; geometric mean 3^{−1/4}=0.7598 (suggestive, F107 cell carries 3^{1/4}; not a derivation).
- B cross-check: α_eff* = 0.376 (m_D=0.532) / 0.411 (m_V=0.727); M(0)=1.50 lattice = 311 MeV.

**Key external references** (the next session should fetch as needed):
- Kogut & Susskind 1975 — the Hamiltonian (KS) formulation.
- Hamer et al, *Recent Advances in Hamiltonian Lattice Gauge Theory* (arXiv:hep-lat/9706017) — Hamiltonian-scheme coupling/series.
- ALPHA / twisted gradient flow Λ determination (arXiv:1702.06289) — nonperturbative step-scaling (Route A-NP).
- Hasenfratz–Hasenfratz / Lepage–Mackenzie — Wilson d₁=5.88, tadpole improvement (the contrast, F151 S2).

**Pitfalls:**
- The model is **Hamiltonian/real-time**, not Euclidean Wilson — use the KS-scheme matching, not Wilson's number.
- Gauge fixing is required for the off-shell self-energy (Route A-PT); Route A-NP (physical static potential / step-scaling) avoids it — prefer it for the headline.
- q\* is a **UV-finite subtraction**; do not report a bare BZ moment as q\* (F154's lesson).
- Concurrent sessions take F-numbers — verify the next free number before writing files.

---

## Verification — high-resolution, user-run (outside the sandbox)

Two complementary checks. Run natively (no 45 s cap); each writes a JSON for a later session to read.

### 1. Numerical solve (B + A log-moment + A self-energy hook)
```bash
cd "<repo root>"
python3 tests/runners/run_residual_AB_highres.py \
    --L 32 48 64 96 \
    --nlog 64 96 128 \
    --out test-results/residual_AB_highres.json
```
- Confirms B's α_eff* is converged at production L (expect 0.376/0.411, spread < 1e-3 between L=64 and 96).
- Tabulates the q\* log-moment to high BZ resolution (confirms the cheap route's UV verdict is not a small-grid artifact).
- The A self-energy **hook auto-fires** once `ca_gluon_self_energy.py` with `qstar_highres()` exists — re-run after building A to capture the production q\*.
- Cost: L=96 ≈ 30–60 min/mass; 4D n=96 log-moment ≈ 5 GB RAM (drop to `--nlog 64 96` or 3D if memory-limited).

### 2. CASIM gauge-dynamics cross-check (the V-scheme coupling, independent of LPT)
The V-scheme coupling A is built on is *defined* by the static potential. Measure it directly from the model's own SU(3) dynamics at high resolution (extends F146).

**Current state of `run_su3_3d_string_tension.py`:** its CLI only accepts `--beta --L --smoke` and it prints (no `--out`, no production thermalisation flags, no JSON, and it fits **only the linear σ**, not the short-distance Coulomb). So the production cross-check is a small **build step**, not a ready command:
  1. Extend `run(...)` (it already takes `n_therm, n_meas, meas_every, rmax, tmax, seed`) and add CLI flags `--ntherm --nmeas --rmax --tmax --seed --out`, dumping the `run()` dict to JSON.
  2. Add a **short-distance Coulomb fit** V(R) = V₀ − (4/3)·α_V/R + σR to the measured Wilson-loop potential; the Coulomb coefficient gives **α_V(q)** at the lattice scale.
  3. Then the production cross-check is:
```bash
python3 tests/runners/run_su3_3d_string_tension.py \
    --beta 9.0 --L 24 --ntherm 4000 --nmeas 2000 --rmax 10 --tmax 10 \
    --seed 1 --out test-results/su3_static_potential_b9.json
# repeat at a second beta (e.g. 12.0) to bracket the running
```
- α_V(q) vs the bare lock 1/16π cross-checks q\* nonperturbatively (Route A-NP leg, no gauge fixing).
- σa² at high statistics → √σ/Λ (F124 leg) and the F146 confinement radius come out of the same run.

Read both JSONs back in the next session: B converged + (A-NP static-potential α_V and/or A-PT self-energy q\*) agreeing on q\*=0.733/a closes the strong sector.
