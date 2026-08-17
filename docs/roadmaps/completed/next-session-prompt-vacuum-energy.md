# Next-session prompt — the BCC zero-point / vacuum-energy density and the cosmological-constant sector

*Drafted 2026-06-30 - 14:30. Hand this to a fresh session. It is self-contained but assumes the assistant will load the standard CLAUDE.md context indexes first.*

---

## Paste-in prompt

You are the research assistant on the "Physics Notes" / Universe-in-a-Bottle BCC cellular-automaton model. Your job this session is to push the **cosmological-constant / vacuum-energy sector** forward — to turn the standing 120-order problem from a *stated* problem into a *derived* (or honestly falsified) resolution, and to tie it to the dark-matter sector.

### Where the sector stands (read these first, do not re-derive them)

- **F164** (`findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md`) — computed the bare lattice vacuum-energy density at the F107 canonical cell: `ρ_vac ≈ 3.5×10¹¹¹ J/m³` vs observed `ρ_Λ ≈ 6×10⁻¹⁰ J/m³`, a definite, regulator-free overshoot of `log₁₀ ≈ 120.8`. Key exact facts: the BZ integral `I_CC = ∫_BZ ω/2 = 4.081`, and the **mean rotation angle ⟨ω⟩_BZ = π/2 exactly** (from the `q → q+π` sign-flip pairing `ω(q)+ω(q+π) = π`). The bare sign is **negative** (all-fermion vacuum, no fundamental bosons → no SUSY cancellation), i.e. wrong as well as too large.
- **F192** (`findings/F192-vacuum-energy-full-tensor.md`) — under the F178 full-tensor source, vacuum `w=−1` gives `ρ+3p=−2ρ`, so the **sign is now correct** (it accelerates) — but the ~10¹²¹ magnitude is unresolved and all four candidate cancellations remain underived.
- **F191** (`findings/F191-dark-matter-rotation-curves-bullet.md`) — dark matter under F178 needs a dark *source* (Bullet-Cluster lensing offset rules out a pure dielectric reweighting of baryons); the model-native candidate is a gravitating-yet-dark vacuum/condensate tied to the F164/F192 sector.
- Supporting: **F59** (isolated the `Λ⁴` CC sector vs the `Λ²` Newton sector), **F69** (paired-spinor photon, marginal binding), **F107** (canonical cell `a`), **F64/F178** (the dielectric / full-tensor gravity the vacuum energy gravitates through), `references/t-hooft-2015-cai-summary.md` (the CA-interpretation vacuum argument).

### The four candidate cancellation channels (from F164 §C) — your targets

1. **CA-native trivial vacuum ('t Hooft) — the leading, elegant-design-preferred lead.** The `½ħω`-per-mode is the *canonical-quantisation* prescription for a continuum field; the underlying object is a deterministic, unitary CA whose ontic ground state is the empty lattice, which costs exactly zero. On this reading the bare `Λ⁴` is a description artefact, the true bare CC is 0, and the observed small `ρ_Λ` is the back-reaction of the *actual non-vacuum field content*. **To close:** show that (a) the CA Hamiltonian's ontic ground state carries zero gravitating energy in the F64 dielectric, and (b) the leading non-vacuum back-reaction lands near `ρ_Λ` (or compute where it lands). This route uniquely fixes both the magnitude *and* the sign.
2. **Dielectric sequestering through F64.** A constant vacuum energy couples to gravity only through the global impedance-matched dielectric (`AB≡1`). **To close:** derive whether the reciprocal lock plus a global (cosmological volume) constraint actually removes the constant piece of `T⁰⁰_vac` from the rotation-rule renormalisation — i.e. does the constant `Λ⁴` fail to source curvature, leaving only fluctuations?
3. **Marginal-binding (F69).** A consistency statement only — explains why composite bosons add no new vacuum tower, but does **not** cancel the fermionic tower. Do not over-claim this; record it as a constraint, not a cancellation.
4. **(Reframing already done in F192)** — sign from `w=−1`. Don't redo; build on it.

### This session's objectives (pick the highest-value reachable one; don't attempt all)

1. **Primary:** turn candidate (i) from a *position* into a *calculation*. Concretely: define the CA ontic ground state precisely, show its gravitating energy in the F64/F178 sector is exactly zero (algebraic if possible, else machine-precision), and then estimate the leading non-vacuum back-reaction's magnitude and sign. Even a rigorous statement of *why* the back-reaction is parametrically `≪ Λ⁴` (with the small parameter named) is a real advance.
2. **Secondary:** attempt candidate (ii) — a clean derivation of whether the `AB≡1` global dielectric sequesters the constant vacuum term. This is self-contained and either yields a mechanism or a no-go.
3. **Tie-in:** assess whether *one* dark vacuum/condensate sector can serve as **both** dark energy (the residual `ρ_Λ`) and dark matter (the F191 clustering source) — what would have to be true (an equation of state that is `w≈−1` smooth on large scales but clusters on galactic scales), and whether the model's vacuum sector (F93 `E_g` condensate? F69 marginal channel?) can supply it. Flag this as speculative unless you can constrain it.

### Practices (project-mandated — follow exactly)

- **Algebraic exactness first**, then machine precision. Derive before introducing new physics. State clearly what is *derived* vs *computed* vs *posited* (use F164's status-table style).
- **Real arithmetic only** for any BCC dispersion / chiral work — numpy/scipy complex routines have burned this project before; mirror the self-contained real-arithmetic style of `gr_fork_F164_cosmological_constant.py`.
- Use **CASIM** where a run is needed; if a sandbox timeout looms, hand back a script + run parameters that emit a JSON result file to read.
- **Document outputs:** new physics → a new `findings/F{N}-name.md` (re-check the max F-number first per CLAUDE.md — concurrent sessions have been taking numbers; current max is **F192**, so you are likely **F193+**). Add a one-paragraph `docs/status/changelog.md` entry with a `yyyy-mm-dd - hh:mm` stamp. Update `docs/status/exactness-inventory.md` if you add exact/machine-precision results. Run `python3 tools/regen_indexes.py` at the end.
- Escape literal `|` as `\|` in any markdown table cells (including finding titles).
- Be honest about scope. A negative or "still open, but the obstruction is now named precisely" result is a valid, valuable outcome — this is the model's largest open problem and a fake resolution is worse than none.

### Deliverable

A new finding (F193+) that either (a) closes or materially advances one candidate cancellation with a derivation, or (b) sharpens the obstruction into a precise, falsifiable statement — plus the changelog/index updates. If you reach the DM/DE unification tie-in, record it as a separate short finding or an explicit "open / next" section, not as a claim.
