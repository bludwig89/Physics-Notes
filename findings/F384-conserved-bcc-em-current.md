# F384 — The U(1) EM current the BCC Weyl walk actually conserves

*2026-09-14 - 13:10 · sector `gauge` · module `casim.engine.gauge.em_current` · test record `F384-conserved-em-current` (assertion, gate tier, 4/4 legs PASS) · results `test-results/F384_conserved_em_current.json`*

**Status:** Confirmed — 4/4 legs PASS, one declared control verified red and red only where declared.
**Checked:** 2026-09-14 - 11:43 — cold-subagent blind re-derivation + adversarial referee, 13-point attack pass: 10 PASS / 3 WEAKENS / 0 FAIL / 2 NOT RUN (N/A) — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F384-review-2026-09-14.md)). The blind re-derivation independently reproduced the construction (minimal longitudinal current, same Nyquist-corner obstruction) via a more general route than this finding's own presentation. The referee found the gate-tier `naive_current_much_worse` leg fragile to an undeclared packet-width choice (would fail at `width=1.0`) and a numeric error in the test registry's `notes:` field; both fixed in this pass (see §6 caveats) — the leg now compares against the derived current's masked residual instead of its full one, robust to `≳10^14×` across every configuration swept.

**Target.** Stage 1 of `docs/roadmaps/photon-fermion-coupling.md`, the photon↔fermion coupling gap. §1.1 of that roadmap found the model had a spatial isospin current for SU(2) (`gauge.weak_wmu.fermion_isospin_current`) and a colour charge density for SU(3) (`gauge.strong.noether_charge_density`), but **no U(1) analogue on the BCC Weyl field** — so a charged fermion had no handle with which to source a photon.

**The question.** The roadmap named the obvious first guess and flagged it as suspect: `ρ = q(|f|²+|g|²)`, `J^i = q ψ†σ^iψ` — the *continuum* Weyl current — and predicted it would only close the discrete continuity equation to `O(a)`, because `weyl_step_3d_bcc` is not a nearest-neighbour hop (`lattice.bcc.bcc_fractional_shift`: each BCC direction is a *fractional* lattice shift `d/√3`, not an integer `np.roll`). The task: derive the current the walk **actually** conserves, from its own unitary `bcc_unitary`, closing

$$\rho(t{+}1,x) - \rho(t,x) + i\,\mathbf C(\mathbf k)\cdot \mathbf J(\mathbf k) = 0$$

against the same curl symbol `charge_coupling.bcc_curl_symbol` already uses for the Gauss-law and Ampère checks.

**The answer.** ρ needs no derivation — it is the walk's own conserved probability density. J does: the continuity equation is one *linear* constraint per Fourier mode on whatever current field is called J, and `C(k)` is a fixed, known vector at every mode, so this constraint has a unique **minimal** (purely longitudinal-in-`Ĉ(k)`) solution:

$$\tilde J(\mathbf k) \;=\; i\,\hat{\mathbf C}(\mathbf k)\,\frac{\tilde\rho(t{+}1,\mathbf k)-\tilde\rho(t,\mathbf k)}{|\mathbf C(\mathbf k)|} \qquad (\mathbf k\neq 0,\ \tilde J(0)=0)$$

— the same construction continuum electrostatics already uses to solve a divergence constraint (`E=-∇φ`, the Coulomb-gauge minimal field). Because `ρ̃(t+1,·)-ρ̃(t,·)` is computed from one **real** `weyl_step_3d_bcc` tick (not an approximation of it), this closes the continuity equation to FFT round-off by construction, away from a small, disclosed, quantified structural gap (§3).

---

## 1. Derivation

For a Weyl 2-spinor `ψ=(f,g)`, `ρ(x) = q(|f(x)|²+|g(x)|²)` is exact and standard — it is precisely what `weyl_step_3d_bcc`'s unitarity conserves in total (`Σ_xρ(t+1)=Σ_xρ(t)` to machine precision, any `f,g`), so there is nothing to derive there.

The naive current `J^i=qψ†σ^iψ` (`em_current.bcc_naive_current`) is the same bilinear pattern already used for the SU(2) isospin current and the SU(3) colour current — a reasonable first guess, and the one the roadmap predicted would fail. It does: real space is the wrong place to look for an exact current here, because the walk's own real-space kernel is not compactly supported (a fractional-lattice-unit hop, Fourier-transformed onto the integer array, spreads over the whole lattice), so no local nearest-neighbour-looking bilinear can be exact by construction the way it can be for an ordinary tight-binding hop.

What **is** exact is the Fourier-space statement itself. `ρ(t{+}1,x)-ρ(t,x)` and `J(x)`, whatever their internal bilinear structure, are just two real-space fields, and the *linear*, translation-invariant discrete-divergence relation between their transforms holds mode-by-mode regardless of how either field was produced — the same reasoning that already makes `charge_coupling.gauss_residual` a per-mode statement. So: compute `ρ(t)` and `ρ(t+1)=ρ(one weyl_step_3d_bcc tick)` exactly, FFT the difference, and solve the resulting one-equation-per-mode linear system for its minimal solution. `em_current.conserved_current` is exactly this — no field-specific assumption, no small-`k` expansion, applicable to any `f,g`.

## 2. Test

| Leg | Claim | Measured (default packet: `L=16`, `σ=2`, `k0=(0.6,0,0)`) | Verdict |
|---|---|---|---|
| `construction_closes` | derived current's *masked* (away from the §3 gap) continuity residual `< 1e-10` | `3.1e-17` | PASS |
| `naive_current_much_worse` | naive current's *full* residual `>` 100× derived current's own *masked* residual, same packet (see caveats — redesigned post-review) | naive `1.56e-01` vs derived-masked `3.1e-17` (`~5×10^15`×) | PASS |
| `naive_shrinks_with_lower_k0` | naive residual falls at lower carrier momentum (genuine `O(k·a)` discretisation, not a fixed disagreement) | `σ=4,k0=0.15` → `2.42e-02` `<` `1.56e-01` | PASS |
| `global_charge_conserved` | `Σ_xρ(t+1)=Σ_xρ(t)` to machine precision | `0.0` (exact) | PASS |

Broader sweep (not gated, recorded for context — `docs/status/changelog.md` Stage-1 entry):

| `L` | `σ` | `k0` | naive residual | derived residual (full, unmasked) |
|---|---|---|---|---|
| 16 | 2.0 | 0.60 | `1.56e-01` | `1.28e-04` |
| 16 | 4.0 | 0.30 | `4.29e-02` | `1.53e-03` |
| 32 | 4.0 | 0.30 | `4.18e-02` | `1.52e-08` |
| 32 | 6.0 | 0.15 | `1.43e-02` | `4.02e-05` |

Naive-current residual shrinks monotonically with `k0` (the `O(k·a)` signature); the derived current's residual — entirely the §3 gap, not a derivation error — shrinks far more sharply with `L` at fixed physical packet content (`1.53e-3→1.52e-8` doubling `L` at `σ=4,k0=0.3`), because a better-isolated packet has less spectral leakage into the periodic-box aliasing that feeds the gap (§3).

## 3. The Nyquist-corner gap — disclosed, not hidden

`bcc_curl_symbol`'s own construction (its docstring, `charge_coupling.py`) symmetrises `C(k)` to be exactly odd, `C(-k)=-C(k)`, as any real-field curl symbol must be. At the 8 lattice points where `k_i∈{0,π}` for every axis, this symmetrisation forces `C(k)=0` **exactly** — `k=0` is exempt (global charge conservation forces `ρ̃(0,t+1)-ρ̃(0,t)=0` there regardless, so the equation is vacuous, not violated), but the other **7** corner modes genuinely have no solution: if the charge density has any Fourier amplitude there, **no current, of any kind**, can source or drain that mode via the `C(k)·` divergence mechanism, because the operator's image excludes it — the discrete analogue of a continuum static charge distribution's own DC component not being recoverable from `E=-∇φ`.

Measured directly (`L=16`, default packet): exactly 8 modes have `|C(k)|<10^{-14}`; the worst non-origin offender sits at `k=(0,-π,0)` with `|Δρ̃|=1.28×10^{-4}` — three orders of magnitude below the packet's peak spectral weight (`0.21`), and (§2 table) shrinking sharply with better packet/lattice-size separation, consistent with this being fed mostly by the periodic-box aliasing of the (non-minimum-image) Gaussian packet builder used for testing rather than a fundamental property of the current construction. Not a defect: `conserved_current` returns this leftover explicitly (`nyquist_gap`) rather than silently masking it, and the gate-tier `construction_closes` leg is scoped to the modes where a solution exists at all.

## 4. What this does and does not close

Stage 0 (this session, no finding of its own — an observer/infrastructure addition) gave the engine a momentum observable but no charge/current handle. This finding supplies the fermion→field half: a charge and a current the walk itself conserves. It does **not** yet give the field a way to act back on the fermion with a directional (momentum-transferring) force — that is Stage 2 (the per-link covariant U(1) step) and Stage 3 (the potential the fermion reads).

## 5. Test record, controls

**Test record:** `F384-conserved-em-current` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`). 4/4 legs PASS. `path: tests/findings/test_F384_conserved_em_current.py` (a driver with no `test_*` functions of its own — the gate contract is the entry point, collected by `tests/casim/test_registry_entries.py`, matching the F381 precedent). One declared control: `use_naive_for_construction: true` swaps the naive current into `construction_closes`'s own check, which — measured, not assumed — turns **exactly** that leg red (`casim test --id F384-conserved-em-current --control`: `reddens exactly ['construction_closes'] of 4 leg(s)`), while the other three, which never read that current, stay green. `can-fail` verified (`tools/check_control_soundness.py --can-fail`: `CAN FAIL`, journalled to `test-results/can-fail.json`).

## 6. Caveats

- **The gate-tier `naive_current_much_worse` leg was found fragile by the independent review and fixed, not merely disclosed.** The original version compared the naive current's full residual against the *derived* current's own **full** residual — which is dominated almost entirely by the Nyquist-corner gap (§3), not by genuine construction error (they agree to ~15 digits in every configuration checked). Because the gap's magnitude varies over 4+ orders of magnitude with packet width, a plausible width choice (`width=1.0` at this record's `L=16,k0=0.6`) dropped the true ratio to `~1.7×`, below the 100× bar, for a reason that had nothing to do with the naive current's own accuracy. Fixed 2026-09-14: the leg now compares against the derived current's **masked** residual (its genuine algebraic performance, §1), which is both the physically correct comparator and far more robust — measured `≳10^14`× across every `width∈{1,2,4,6}` and `k0∈{0.02,…,1.6}` combination swept in review. See `docs/reviews/F384-review-2026-09-14.md`.
- **The derived current is not unique.** §1's construction is explicitly the *minimal* (purely longitudinal-in-`Ĉ(k)`) solution — continuity fixes only the projection of `J̃(k)` along `Ĉ(k)`; the transverse (⊥`Ĉ(k)`) part is free, unconstrained gauge freedom, so `conserved_current` returns one member of an infinite gauge-equivalent family, not *the* current in any stronger sense. Any Stage 2–5 use of this current should not assume its transverse structure carries physical content.
- The Nyquist-corner gap magnitude reported here is not cleanly separated from the specific (non-periodic-aware) Gaussian packet builder (`core.coupled.gaussian_packet`) used for testing, which does not use minimum-image distance and so has some genuine edge/wraparound spectral leakage at small `L` (confirmed by direct source read in review). The gap's existence and its `C(k)=0`-forced mechanism are exact and packet-independent; its *measured magnitude* for a specific packet conflates that mechanism with this builder's own boundary artifact. Not resolved here — a future session wanting a tighter bound should use a periodic (minimum-image) packet builder.
- Only the Weyl 2-spinor case is covered (matching `weyl_step_3d_bcc`); the massive Dirac case (`dirac_bcc`) is not addressed and was not asked for by Stage 1.
- The naive current is not shown to be *wrong* in any regime this project already relies on — F29/F65-F69/F87 and the SU(2)/SU(3) analogues never checked their bilinear currents against exact discrete continuity, so this finding does not retroactively call any of them into question; it establishes the standard against which Stage 2 onward should be measured, for the U(1) sector specifically.
- The `exactness="machine"` tag in the module registry covers `conserved_current`'s masked residual specifically, not the module as a whole (`bcc_naive_current` is explicitly not machine-exact — that is the point of the comparison).

**Test record:** see §5. **Claim:** none — this is an engine-capability addition (a current construction) rather than a claim about what the model predicts or shows against established physics; no `docs/claims/` card is issued per D12's bar ("extends established physics," not "is interesting"). It is infrastructure Stage 2–5 will build claims on top of.

**Cross-references:** [[F87-charge-coupling-paired-photon]] (the `bcc_curl_symbol`/Gauss-law machinery this current is built against), [[F68-minimal-coupling-forces-even-photon]] (the U(1) coupling channel this current will feed, Stage 2), [[F29-w-triplet-bilinear-su2-bridge]] (the SU(2) isospin-current precedent this supersedes no part of — see caveats).
