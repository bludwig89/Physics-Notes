# F335 — Link reflection positivity for the BCC₃×ℤ lattice gauge action: the OS-Seiler/Menotti-Pelissetto hypotheses hold, unmodified by the BCC spatial geometry

**Date:** 2026-08-30 - 11:54
**Session:** `quiet-steady-osterwalder`
**Sector:** gauge
**Status:** Confirmed — 8/8 PASS (gate record), 1 declared control verified red on its own leg and only there
**Checked:** 2026-08-30 — 10 PASS / 3 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/gauge/reflection_positivity.py`
**Test record:** record `F335-reflection-positivity-bcc` (tier gate, `casim test --id F335-reflection-positivity-bcc`) — the control (`broken_dagger: true`) reddens leg `M1` only, and it is measured, not assumed, that leg `I1` cannot see the same bug (§2.3).
**Battery cross-check:** record `F335-reflection-positivity-gram` (result_dump, tier battery) carries the high-statistics Monte Carlo cross-check.
**Results:** `test-results/F335_reflection_positivity_bcc.json` (gate), `test-results/F335_reflection_positivity_gram_{anisotropic,isotropic,strong}.json` (battery)
**Cross-references:** F265 (the BCC action's geometry: 6 rhombi, 4 mixed rectangles), F323 (the anisotropy β_t/β_s = 4, derived), F313 (primitivity — no local half-tick, which is what makes Euclidean time a genuine ℤ factor rather than a fifth BCC generator), F94 (superseded hypercubic 4D leg — ledger S20), F299 (Casimir-scaling successor, unrelated content, same module family)

---

## 0. What completeness row B7 asked for, and what this delivers

Row B7 (confinement) has been PARTIAL since the tree first ran 3+1D sampling: exact in 2D (area law, established), constructed-but-unproven in 4D. F323 §4 stated plainly that a repo-wide grep for `reflection positiv`, `Osterwalder`, `Schrader`, `cluster expansion` returned **zero hits**, and that "no amount of sampling supplies" the missing transfer-matrix-with-positivity. The brief for this session was explicit about scope: determine whether the model's own BCC₃×ℤ action satisfies the Osterwalder–Seiler reflection-positivity axioms **at all** — a result either way — and do not re-attack Monte Carlo sampling of the confinement measure (string tension / Wilson-loop decay), which cannot close this residual regardless of statistics.

**The answer is yes, it does.** Link reflection positivity holds for the BCC₃×ℤ action, for the standard (non-heat-kernel) Wilson single-plaquette form, at any β_s, β_t ≥ 0, for any compact gauge group — established by verifying that the action satisfies the same three structural hypotheses the general theorem needs on a hypercubic lattice, and observing (the actual new content) that nothing in either the hypotheses or the proof references the *spatial* lattice's connectivity. This is a **necessary ingredient**, not a full confinement proof: reflection positivity is what licenses Osterwalder–Schrader reconstruction — a genuine Hilbert space and a bounded, self-adjoint transfer matrix — not a mass gap or an area law by itself. Row B7's residual **narrows**, from "no positivity machinery exists in the tree" to "the machinery exists, the model's own action satisfies it, and a strong-coupling / cluster-expansion argument on top of that transfer matrix is the next step for an actual proof." That next step is not attempted here.

---

## 1. The theorem being invoked, precisely

Link reflection positivity for lattice gauge theory with the Wilson plaquette action is due to Osterwalder & Seiler (*Ann. Phys.* **110**, 440, 1978), for reflections through planes of links; Menotti & Pelissetto (*Commun. Math. Phys.* **113**, 369, 1987) extended it to reflections through planes of *sites* and to correlators of *any* gauge-invariant observable, "relying on the particular structure of the Wilson action." The primary, load-bearing source for that "does not need aᵣ(β) ≥ 0" fact is Osterwalder & Seiler (1978) itself and Menotti & Pelissetto (1987) — the factorization argument below is theirs, not new in 2026. A 2026 exposition (Faizal, Ali & Alshal, arXiv:2606.19362, building a full SU(N) mass-gap construction on top of it) restates the same mechanism in a form this session found clearer to check against than the 1978/1987 originals, and is cited here purely as an expository convenience — **not as independent evidentiary support** and not for its own (unevaluated, unrelied-upon) mass-gap claim. Quoting it precisely, because it resolves a real subtlety this session had to check before trusting the argument: **the ordinary exponential Wilson action does *not* need character-expansion coefficients aᵣ(β) ≥ 0.** That positivity condition is a sufficient but unnecessary route (and the one the heat-kernel action needs, by construction); the general Wilson action gets link-reflection positivity directly from a Peter–Weyl "sum of squares" factorization across the reflection plane — the Gibbs weight splits into `U⁻ · U⁰ · U⁺` (links strictly behind, straddling, and ahead of the plane), the straddling plaquettes factor into products of half-plaquette representation functions under character expansion, and integrating the interface links `U⁰` against Haar measure collapses the whole thing into `Σ_α Φ_α(U⁻) Φ_α(U⁺)` for square-integrable `Φ_α` — manifestly of the form `⟨θF,F⟩ ≥ 0`.

Extracting what that factorization actually *needs*, independent of which compact group or which specific lattice carries it:

1. **(a) Nearest-neighbour time coupling.** The lattice's time direction must be a graph where each site has exactly one forward and one backward temporal neighbour, so that "the plane between slice t and slice t+1" is a well-defined single interface, not a family of interfaces at different depths.
2. **(b) Purely-spatial loops confined to one time-slice.** Any plaquette with zero net time component never straddles a reflection plane, so it does not enter the `U⁰` factorization step at all — it lives entirely in `U⁻` or entirely in `U⁺`.
3. **(c) Mixed loops cross exactly one time-step, with their temporal legs entering linearly.** A "mixed" plaquette must contain its temporal-link factors to the first power (once forward, once as a dagger) so that expanding it via Peter–Weyl actually produces the individual matrix elements `D^r_{ij}(U⁰)` needed for Haar orthogonality; a temporal link appearing squared, or a loop spanning two time-steps, breaks the single clean interface integral.

None of (a)–(c) says anything about the **spatial** lattice — not its dimension, not whether it is hypercubic, not how many link axes a site has, not whether it is bipartite. The theorem is topological in the time direction alone. That observation is the whole of this finding's new content: it licenses carrying a proof built for a 3+1D hypercubic lattice over to a lattice whose spatial part is BCC (F265) without inventing any new machinery.

---

## 2. The BCC₃×ℤ action satisfies (a)–(c) exactly — read off the code, not assumed

`bcc_action.py`'s `_build_loops()` builds exactly two loop classes on `BCC_3 spatial × ℤ time` (F265's 6 rhombi, F323's 4 mixed rectangles):

```python
for lab, (d1, d2) in zip(BCC_PLAQ_LABELS, BCC_PLAQUETTES):
    e1, e2 = _h4(d1), _h4(d2)                      # _h4(d, dt=0) — ALWAYS dt=0
    legs = [(e1,(0,0,0,0)), (e2,e1), (-e1,e1+e2), (-e2,e2)]
    loops.append((lab, 's', legs))                  # <- rhombi
for i, a in enumerate(BCC_LINK_AXES):
    ha = _h4(a)
    legs = [(ha,(0,0,0,0)), (T_HOP,ha), (-ha,ha+T_HOP), (-T_HOP,T_HOP)]
    loops.append((f'st{i}', 't', legs))             # <- mixed rectangles
```

with `_T_HOP = (0,0,0,1)` the *only* temporal hop anywhere in the module (`_stored` raises `ValueError` on anything else). `reflection_positivity.loop_structure_reflection_hypotheses()` turns this into an exact, randomness-free check over the ten loops rather than an eyeballed reading of the source:

| hypothesis | check | result |
|---|---|---|
| (a) nearest-neighbour time hop only | every temporal leg has `h[:3]==(0,0,0)` and `\|h[3]\|==1` | **True** |
| (b) rhombi confined to one time-slice | zero temporal legs on all 6 rhombi | **True** |
| (c), part 1 | exactly 2 temporal legs per mixed rectangle (linear, not squared) | **True** |
| (c), part 2 | those 2 legs are one `+t̂`, one `−t̂` (single time-step crossing) | **True** |
| loop count | 6 rhombi + 4 mixed rectangles = 10, not the hypercubic 6 | **True** |

All five hold exactly (gate legs `H1`–`H4`, `test-results/F335_reflection_positivity_bcc.json`). §2.1 of `bcc_action.py`'s own header already states the geometry in prose ("ten plaquettes per site, not the hypercubic six"); this is that prose promoted to a machine-checked assertion, plus the observation that it is *precisely* the checklist condition (a)–(c) needs.

### 2.1 The reflection map

Time-reflection θ through the plane between slice `Lt−1` and slice `0` (site map `τ → Lt−1−τ`), applied to a link configuration:

- **Spatial fields:** `θU_a(x,τ) = U_a(x, Lt−1−τ)`, **no dagger**. A purely spatial link never crosses a time-slice, so reflection only relabels which slice it lives on.
- **Temporal field:** `θU_t(x,τ) = U_t(x, (Lt−2−τ) mod Lt)^†`. The directed bond `τ → τ+1` becomes, after `t → −1−t`, a bond running backwards in time — the dagger of the forward-stored bond based at the new site.

`reflection_involution_residual` confirms `θ∘θ = identity` **exactly** (`0.0`, both configurations bit-identical) — the map is a genuine involution, not merely a convention.

### 2.2 The mixed-rectangle trace identity — a cyclic-rotation subtlety, caught by getting it wrong first

The mixed rectangle at `(x,τ)` along axis `a` is `P = U_a(x,τ)·U_t(x+a,τ)·U_a(x,τ+1)^†·U_t(x,τ)^†` (read directly off `_build_loops`'s leg list). Applying θ termwise and simplifying with `μ := Lt−2−τ`:

```
θP(x,τ) = U_a(x,μ+1) · U_t(x+a,μ)^† · U_a(x,μ)^† · U_t(x,μ)
P(x,μ)^† = U_t(x,μ) · U_a(x,μ+1) · U_t(x+a,μ)^† · U_a(x,μ)^†
```

These are the **same four factors in cyclic order**, not the same matrix — `θP(x,τ)` is `P(x,μ)^†` rotated by moving its last factor to the front. Trace is cyclic-invariant; the raw matrix generally is not. The first version of this module's diagnostic compared raw matrices and got a large, real, O(1) "residual" (`1.985`) that looked like a bug in θ. It was not: it was checking a stronger identity than the theorem needs. The provable, and only provable, identity is on the trace:

$$\mathrm{Tr}\big(\theta P_{\text{mixed}}(\tau)\big) = \overline{\mathrm{Tr}\big(P_{\text{mixed}}(\tau_{\text{mirror}})\big)}, \qquad \tau_{\text{mirror}} = (L_t-2-\tau) \bmod L_t,$$

which is exactly what is needed (RP concerns gauge-invariant, trace-class observables, and `Re Tr` of a complex conjugate equals `Re Tr` of the original). Measured: **4.5×10⁻¹⁶** (gate leg `M1`), machine precision. This is the correct fix, not a loosened check — §2.3's control is what confirms `M1`, not the abandoned raw-matrix comparison, is the leg that actually certifies the dagger convention.

### 2.3 The control

`broken_dagger=True` drops the dagger on the reflected temporal field. Measured, not assumed: the bare time-index permutation `τ → (Lt−2−τ) mod Lt` is *already self-inverse* regardless of any dagger, so `I1` (the involution check) stays at exactly `0.0` under the control — it cannot see this bug by construction, a fact about the index map rather than a weakness in the leg. `M1` reddens to `3.30` (O(1), as a wrong-dagger error should). `H1`–`H4` (pure combinatorics on `BCC4_LOOPS`, no θ involved) and `S1` (§3, no θ involved) stay green, single-legged — 7/8 PASS under the control, `M1` the sole casualty, exactly as declared.

---

## 3. Supplementary exact result: SU(2) Wilson character positivity (not needed by §1–2, but a clean closed form)

Faizal et al. 2026 note character-coefficient positivity is *not required* for the general argument above. It is nonetheless a fully closed-form, independently checkable fact for the SU(2) sector, and worth deriving because it is the *other* classical route to reflection positivity (the one Osterwalder & Seiler's original 1978 paper actually used before the more general factorization argument was recognised as sufficient on its own).

For `U ∈ SU(2)` with rotation angle `θ` (`Tr_F U = 2cos(θ/2)`), the spin-`j` character is `χ_j(θ) = sin((2j+1)θ/2)/sin(θ/2)`, and the Wilson Boltzmann factor `exp(β Re Tr U) = exp(2β cos(θ/2))` expands using the classical Bessel generating function `Σ_n I_n(x) e^{inφ} = e^{x\cosφ}` with `x=2β, φ=θ/2`, matched against the character basis:

$$a_j(\beta) = I_{2j}(2\beta) - I_{2j+2}(2\beta),$$

with `I_n` the modified Bessel function of the first kind. This is not a fit: the Bessel recursion identity `I_{n-1}(x) - I_{n+1}(x) = (2n/x) I_n(x)` (elementary, from the defining ODE) gives, at `n = 2j+1`,

$$a_j(\beta) = \frac{2j+1}{\beta} I_{2j+1}(2\beta) > 0 \quad \text{for all } \beta>0,\ j\ge0,$$

since every modified Bessel function of the first kind is strictly positive for positive argument. `su2_character_coeff_numeric` verifies this by direct Weyl-measure quadrature (`dμ(θ) = (1/π)\sin^2(θ/2)\,dθ`, plain numpy Riemann sum — no scipy, D8-compliant) rather than by importing the closed form: at `β ∈ {0.3, 1.0, 3.0}`, `j ∈ {0, 0.5, 1, 1.5, 2, 3}`, every sampled coefficient is positive, smallest **1.02×10⁻⁶** (`β=0.3, j=3` — deep in the tail, correctly small, still measurably positive, not a numerical zero). Gate leg `S1`.

---

## 4. Numerical cross-check: the reflection Gram matrix (support evidence, not a proof, not the forbidden re-attack)

This is explicitly **not** a re-attack of the confinement-measure (string-tension / Wilson-loop-decay) Monte Carlo the session brief named as unable to close this residual regardless of statistics. It checks a structurally different quantity: whether the empirical Gram matrix

$$G_{ij} = \big\langle F_i(\tau_{\text{neg}})\, F_j(\tau_{\text{pos}}) \big\rangle_S$$

built from the ten local, real, gauge-invariant plaquette traces (`F_i` = `Re Tr P_i / N` for the 6 rhombi + 4 mixed rectangles), sampled by heat-bath Monte Carlo on the actual BCC₃×ℤ action and reflected through a genuine time-slice boundary, comes out Hermitian positive-semi-definite — the direct numerical signature RP predicts. A stable, growing-with-statistics negative eigenvalue here would falsify §1–2; it is a legitimate, distinct diagnostic that a wrong sign or off-by-one in the reflection map (exactly the kind of bug §2.2/§2.3 already caught once) would show up in, that the analytic argument alone cannot rule out by inspection.

SU(2), `L=4` (16 genuine BCC sites/slice), `Lt=6`, 150 thermalisation + 1600 measurement sweeps (over-relaxation 2), sampled every 4 sweeps (400 samples), at the model's own derived anisotropy `β_t/β_s = 4` (F323) plus two comparison points:

| run | β_s | β_t | dominant eigenvalue | smallest eigenvalue | bootstrap σ | smallest/σ |
|---|---:|---:|---:|---:|---:|---:|
| anisotropic (model's own ratio) | 2.0 | 8.0 | **6.801** | −3.18×10⁻⁴ | 8.42×10⁻⁵ | −3.8σ |
| isotropic (control point) | 2.0 | 2.0 | **4.320** | −6.68×10⁻⁴ | 1.78×10⁻⁴ | −3.7σ |
| strong coupling | 0.5 | 2.0 | **0.875** | −1.72×10⁻³ | 4.67×10⁻⁴ | −3.7σ |

Full 10-eigenvalue spectrum, anisotropic run: `{−3.18, −2.62, −0.81, −0.25, 0.01, 0.06, 0.54, 1.76, 3.36} × 10⁻⁴`, then `6.801`. *(Re-run 2026-08-30 with the per-loop-type mirror-index fix — attack 12 of the F335 review pass caught the Gram check using one shared `tau_neg` for both rhombus and mixed-rectangle observables where §2.2's own derivation requires two different mirror indices; `tau_neg_rhombus = (Lt−1−τ)%Lt`, `tau_neg_mixed = (Lt−2−τ)%Lt`. The corrected numbers are close to the stale pre-fix ones and the qualitative conclusion is unchanged.)*

**Read this honestly, not optimistically.** In all three runs, one eigenvalue — the O_h-symmetric common mode, essentially the mean action density — is unambiguously and overwhelmingly positive, three to four orders of magnitude above the noise floor. The other nine sit in a tight cluster around zero (10⁻⁴–10⁻³), roughly half above and half below, each within 3.7–3.8 bootstrap standard deviations of zero. That is consistent with the true values of those nine directions being at or very near zero (an O_h near-degeneracy among differently-oriented plaquette fluctuations at this small volume), with the sign of each noisy estimate essentially a coin flip — **not** a stable, significant violation, but also **not** independently resolved at that sub-leading scale by the statistics run here. None of the three runs shows a *growing* magnitude or a *stable* sign as β is varied, which is what a genuine violation would be expected to do; a single run at ~3.7σ negative is unremarkable among nine near-degenerate directions across three configurations (27 numbers), and the consistency of that ~3.7σ figure across all three β-values (rather than growing with β_t as a real effect coupled to the anisotropy would) is itself evidence for noise over signal. Resolving this cleanly would need substantially more statistics than is proportionate for a supporting cross-check — the actual proof is §1–2, which does not depend on this measurement at all. This check was also run at only `L=4` (16 genuine BCC sites/time-slice); volume dependence was not swept, so a residual finite-size effect on these near-zero directions cannot be excluded from this data alone — see §5 and the falsifiers in §6.

---

## 5. What is claimed, and what is not

**Claimed:** the BCC₃×ℤ Wilson action satisfies the structural hypotheses of the Osterwalder–Seiler / Menotti–Pelissetto link-reflection-positivity theorem, exactly and unconditionally in β_s, β_t ≥ 0 and in the gauge group. The theorem itself is established literature, not re-derived from scratch here; what is new is verifying, directly from the code that defines the action (not from a redescription of it), that its three load-bearing hypotheses hold, and the observation that those hypotheses — and the Peter–Weyl factorization proof behind them — never reference the spatial lattice's connectivity, so the hypercubic-lattice theorem carries over to BCC-space×ℤ-time without new machinery. The SU(2) character-coefficient positivity (§3) is an independent, exact, closed-form supplementary result. The Gram-matrix measurement (§4) is supporting numerical evidence, reported with its actual statistical uncertainty, not additional proof.

**Not claimed:**
- **No mass gap, no area law, no confinement verdict.** Reflection positivity is a necessary ingredient for Osterwalder–Schrader reconstruction (a genuine Hilbert space, a bounded self-adjoint transfer matrix) — it is not by itself a statement about the spectrum of that transfer matrix or about the large-loop behaviour of Wilson loops. The next step toward an actual confinement proof — a strong-coupling expansion or cluster expansion establishing linear confinement (or a mass gap) from the now-available transfer matrix — is not attempted here and remains the residual (§0, §6).
- **The general theorem (§1) is cited, not re-derived from first principles.** A full line-by-line re-verification of the Peter–Weyl factorization argument, checking every Gram-matrix/Cauchy–Schwarz step against the primary sources, is beyond this session's scope; what is re-derived from scratch is the model-specific content of §2 (the loop structure, the reflection map, its exact identities) and §3 (the SU(2) closed form).
- **§4's Gram check is not a proof and does not, by itself, distinguish "RP holds" from "RP holds and these nine directions are merely small."** It is reported as inconclusive-but-not-contradicting at the sub-leading scale, explicitly.
- **Volume dependence of the §4 Gram check was not swept.** All three runs use `L=4` (16 genuine BCC sites per time-slice); whether the nine near-zero eigenvalues' scatter narrows, stays flat, or grows relative to the dominant mode at larger `L` is not tested by this finding, so §4's "consistent with zero, not a violation" reading is stated only for the volume actually run, not asserted to hold at all sizes.
- **The site/link-reflection distinction is not tracked.** Osterwalder–Seiler's original 1978 result concerns link reflections (used here — reflecting through the plane between two time-slices, at the same place a temporal link sits); Menotti–Pelissetto's 1987 extension to site reflections and general observables is cited as the source of the "any gauge-invariant F" strength claimed in §1, but this finding's own reflection map (§2.1) is a link reflection, which is what the theorem needs at minimum.

## Prior art

This finding does not claim a new theorem. Link reflection positivity for the Wilson action is Osterwalder & Seiler (1978); the extension to site reflections and general gauge-invariant observables is Menotti & Pelissetto (1987) — both cited in full in §1 and §7. What is checked here, and is not something this session found already done in the literature for a BCC spatial lattice specifically, is that the *hypotheses* of that 45-year-old theorem hold for this model's particular BCC₃×ℤ action, read off the action's own loop-construction code rather than assumed by analogy with the hypercubic case. The observation that the theorem's proof never references spatial connectivity (§1, final paragraph) is, as far as this session's literature search found, not written down elsewhere in this specific form — but it is a direct, close corollary of reading the 1978/1987 proofs on their own terms, not a deep new result. Call this a modest corollary, not a new theorem: the mathematics is 1978/1987; the content added here is verifying that one particular non-hypercubic lattice actually falls inside its hypotheses, plus the mechanical work (§2–§4) of checking that on the code.

## 6. Falsifiers

1. A demonstration that hypothesis (a), (b), or (c) in §2 fails for some loop not enumerated here (e.g. a future engine change adding a longer-range temporal hop, or a mixed loop spanning two time-steps) would break the argument at exactly the leg (`H1`–`H4`) that checks it.
2. A demonstrated sign or indexing error in `theta_reflect_config` beyond what §2.2/§2.3 already found and fixed — i.e. a residual on `I1` or `M1` that does not vanish to machine precision — would directly contradict §2.
3. A stable, growing-with-statistics negative eigenvalue in the §4 Gram construction (not a single run at a few σ, but a trend across increasing statistics or increasing volume) would directly contradict §1–2 and require revisiting the structural argument, not just re-running with better statistics.
4. If a future attempt at the strong-coupling/cluster-expansion step (§0's stated next residual) finds that the *specific* anisotropic couplings derived in F323 (β_t/β_s = 4) put the model outside the convergence radius of the standard strong-coupling expansion, that would not falsify reflection positivity itself but would narrow what can be built on top of it.

## Reviewed & corrected

**2026-08-30 - 12:40** — attack pass: **CONFIRMED-NARROWER**. Found: a genuine internal inconsistency in §4's Gram-matrix code — it used one shared mirror time-slice for both rhombus and mixed-rectangle observables where §2.2's own derived reflection identity requires two different mirror indices (`tau_neg_rhombus = (Lt−1−τ)%Lt` vs. `tau_neg_mixed = (Lt−2−τ)%Lt`); plus three WEAKENS (the Faizal et al. 2026 citation read as more evidentiary than it should, prior-art/novelty framing needed an explicit corollary-not-theorem statement, and the `L=4` Gram check's volume dependence was untested and undisclosed). Fixed: added `_mixed_reflection_observable_batch` and reran the three battery configurations with the corrected per-loop-type mirroring (§4's table and spectra updated; conclusion unchanged — smallest eigenvalue in each run is ~3.7–3.8 bootstrap σ from zero, not a stable violation); hedged the Faizal citation to expository-only (§1); added a `## Prior art` section stating the corollary-not-theorem scope; added an explicit "volume dependence not swept" line to §5 and §4. Rejected: none — the eight structural/identity/character legs (H1–H4, I1, S1, G1) and the M1 control all attacked cleanly and needed no change. Deferred: the strong-coupling/cluster-expansion proof step itself (§0, §5, §6) — the actual next residual after RP, not a defect in this finding; a larger-`L` Gram sweep to resolve the volume question, landing site noted as future work rather than run here given the session's time budget.

## 7. Sources

- `src/casim/engine/gauge/reflection_positivity.py` — `loop_structure_reflection_hypotheses`, `theta_reflect_config`, `reflection_involution_residual`, `mixed_plaquette_reflection_trace_residual`, `su2_character_coeff_numeric`, `su2_character_positivity_residual`, `reflection_positivity_gram_check`, `check_reflection_positivity_bcc`
- `tests/runners/run_reflection_positivity_gram.py` — the battery statistics runner
- Osterwalder, K. & Seiler, E., "Gauge Field Theories on the Lattice," *Ann. Phys.* **110** (1978) 440.
- Menotti, P. & Pelissetto, A., "Osterwalder-Schrader Positivity for the Wilson Action," *Commun. Math. Phys.* **113** (1987) 369.
- Faizal, M., Ali, A. F. & Alshal, H., "Reflection-Positive Construction of a Four-Dimensional SU(N) Yang-Mills Theory With Mass Gap and Confinement," arXiv:2606.19362 (2026); *Fortschr. Phys.* (2026), doi:10.1002/prop.70097. Cited for its Sec. 2.1 restatement of the character-coefficient-free factorization argument, not for its own mass-gap claim, which this finding neither relies on nor evaluates.
- `findings/F265-bcc-gauge-action-blindness.md` (the 6-rhombus geometry), `findings/F323-anisotropy-derived-and-d4-casimir.md` §4 (the "zero hits" residual this finding answers), `findings/F313-one-time-dimension-from-the-update-commutant.md` (primitivity, §2.1's justification for treating Euclidean time as a genuine ℤ factor)
- `docs/status/completeness-2026-08-20-prompts.md` B7, `docs/status/completeness-2026-08-18.md` B7 row (the research brief this finding answers)
