# F392 — The beam-polarization defect: `build_beam_packet` carried zero field momentum, fixed with a null Riemann–Silberstein construction

*2026-09-16 - 01:20 · sector `gauge` · module `casim.engine.gauge.photon` (new `polarization=` parameter on `build_beam_packet`, new `check_beam_polarization_fix`) · test record `F392-beam-polarization-null-fix` (assertion, gate tier, 6/6 legs PASS) · results `test-results/F392_beam_polarization_null_fix.json`*

**Status:** Confirmed — 6/6 legs PASS, one declared control verified red on exactly 4 of 6 legs.

**Reviewed:** 2026-09-16 — **CONFIRMED** ([independent review](../docs/reviews/F392-review-2026-09-16.md))

**Target.** Part A of `docs/roadmaps/photon-fermion-coupling-rerun-prompt.md`, implementing `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` §2/§8 step 1. That audit (re-verified against the real modules in this session, not the audit's own from-source reimplementation — see §5) found that `gauge.photon.build_beam_packet` (used by F390's whole momentum-conservation scenario) places `E` and `B` in the *same* Cartesian component: `E[pol_axis] = F.real`, `B[pol_axis] = F.imag`. So `E ∥ B` pointwise and the Poynting momentum `Σ E×B` vanishes **identically** — not approximately — at every axis and carrier mode tested. F390's entire momentum-conservation test ran against a field with no momentum to give.

**The answer.** The model's photon *is* the Riemann–Silberstein analytic field (decision 5, F67–F69: the paired-spinor photon rides `F = E + iB`). A genuine radiation field is **null**: `F·F = E² − B² + 2i E·B = 0`, i.e. `|E| = |B|` and `E ⊥ B` (`references/lattice-conservation-laws-research-review.md` §8). `build_beam_packet`'s original construction has `F = (\text{scalar envelope})·ê` with `ê` a single real basis vector, so `F·F = (\text{scalar})² ≠ 0` — not null, by construction. The fix is a complex circular polarization vector: with `a1=(axis+1)%3`, `a2=(axis+2)%3` and `ê = (ê_{a1} + i·ê_{a2})/√2`,

$$\mathbf F(x) = \hat{\mathbf e}\cdot f(x), \qquad f(x) = \text{envelope}(x)\cdot e^{ik_0 d_\text{axis}(x)}$$

so `F·F = f²·(ê·ê) = 0` exactly, since `ê` is a null complex unit vector (`ê_{a1}·ê_{a1} − ê_{a2}·ê_{a2} + 2i\,ê_{a1}·ê_{a2} = 1 − 1 + 0 = 0`). Concretely:

$$E_{a1}=\mathrm{Re}(f)/\sqrt2,\ B_{a1}=\mathrm{Im}(f)/\sqrt2,\qquad E_{a2}=-\mathrm{Im}(f)/\sqrt2,\ B_{a2}=\mathrm{Re}(f)/\sqrt2$$

New `polarization=` parameter on `build_beam_packet`: `"linear"` (default) is the original, unchanged construction — **bit-identical to git HEAD**, verified directly for every `axis∈{0,1,2}`, `m_index∈{1,2,3,4}` combination, so F386–F391's own gate records (all built on the original default) move by exactly zero bits. `"circular"` is the fix.

---

## 1. Verification against the real modules first

Per the rerun-prompt's own instruction ("the audit was written in a session that could not run `make gate`... your first job is to re-run every one of its checks against the real modules"), `tools/verify_photon_momentum_diagnosis.py` was run unmodified against this repo's actual `casim.engine.gauge.photon` and `casim.engine.gauge.charge_coupling` before any code was touched. Every number it reports (zero pointwise `E×B`, `75.126`/`+1.000000`/machine-zero `E·B` for the proposed fix, the `Ĉ(k)` reflection angles, the `74.2%` mean `|C×G|/(|C||G|)` for `bcc_curl_symbol`) reproduced exactly against the real modules — no discrepancy found, so the audit's diagnosis is confirmed, not merely assumed.

## 2. Test results

| Leg | Claim | Measured (`L=16`, `σ=3.0`, default axis/m sweep) | Verdict |
|---|---|---|---|
| `null_condition_holds` | `\|E·B\|/(‖E‖‖B‖) < 10^{-12}`, every `axis×m_index∈{2,4}` combo | `2.4×10^{-17}` (worst case) | PASS |
| `equal_magnitude_holds` | `\|‖E‖−‖B‖\|/‖E‖ < 10^{-12}`, same combos | `2.0×10^{-16}` (worst case) | PASS |
| `momentum_nonzero_and_aligned` | `\|Σ E×B\| > 0` and `\cos(P,\hat k) > 0.99`, same combos | `\cos = 1.000000` at every combo, no combo has zero momentum | PASS |
| `default_config_magnitude_matches_audit` | `\|Σ E×B\| = 75.126` at the audit's own `axis=0,m=2` configuration | `75.125961` | PASS |
| `momentum_conserved_under_free_propagator` | relative drift `< 5\times10^{-15}` over 40 ticks of `photon_step_spectral` | `3.6\times10^{-15}` | PASS |
| `linear_mode_bit_identical_to_default` | omitting `polarization=` gives exactly the same array as `polarization="linear"` | bit-identical | PASS |

**Declared control** (`null_check_polarization: linear`, i.e. swap the original defective mode into the null-condition checks): measured, not assumed, to redden exactly `equal_magnitude_holds`, `momentum_nonzero_and_aligned`, `default_config_magnitude_matches_audit`, `momentum_conserved_under_free_propagator` (4 of 6), leaving `null_condition_holds` and `linear_mode_bit_identical_to_default` green. `can-fail` verified (`tools/check_control_soundness.py --can-fail`: `CAN FAIL`).

## 3. A caveat on the `null_condition_holds` leg's discriminating power

`null_condition_holds` measures a **global**, space-summed `\Sigma_x E(x)\!\cdot\!B(x)` ratio, not the pointwise `F\!\cdot\!F(x)=0` condition a genuine null field satisfies at every point. For this specific symmetric Gaussian-envelope beam, the linear-mode control's global `E\!\cdot\!B` ratio also happens to measure small (`2.1\times10^{-17}`) — **not because the linear mode is null**, but because `E(x)B(x)=\mathrm{Re}(f(x))\mathrm{Im}(f(x))=\tfrac12|f(x)|^2\sin(2k_0d_\text{axis}(x))` is odd in the propagation-axis displacement about the packet centre while the envelope `|f(x)|^2` is even, so the space sum cancels by symmetry, independent of whether the field is genuinely null. The leg that actually discriminates the two modes is `equal_magnitude_holds` (`\|E\|\ne\|B\|` in linear mode, confirmed False under the control) together with `momentum_nonzero_and_aligned` (the real defect — `\Sigma E\times B` collapsing, not `E\!\cdot\!B`). `null_condition_holds` is retained because it is the literal quantity the rerun-prompt's own acceptance table names and because it is a correct, positive fact about the circular-mode fix (worst case `2.4\times10^{-17}$, well under the `10^{-16}` bar quoted there) — it is disclosed here as not being, by itself, the leg that would catch a regression back to linear-mode-shaped defects on an *asymmetric* beam construction, where the odd/even cancellation would not hold.

## 4. What this does and does not close

This removes the beam-construction defect from the momentum question — the beam a momentum test injects can now genuinely carry momentum. It does **not** touch `core.observers.Momentum` (verified sound already, per its own docstring and per this session's independent re-verification, §1) and does **not** change the `Ĉ(k)`-longitudinal leakage the paired-photon's own curl-symbol machinery measures for a beam built transverse to Euclidean `k̂` (unaffected by polarization convention, F386 §6/F391 §1's own domain — measured here too: `0.2755→0.2741` at `m=2`, matching the audit's own reported drop, itself explained by Part B/Part C's separate curl-symbol defect, not this one). Stage 5's actual re-run against this fixed beam is a separate finding (see cross-references).

## 5. Caveats

- **Only `build_beam_packet` is touched.** `build_pair_mode` was checked, not assumed, to already be correct (`E∥e1 ⊥ B∥e2=k̂×e1`, a standard transverse construction) — no change made there, matching the rerun-prompt's own instruction to confirm rather than assume.
- **The `momentum_conserved_under_free_propagator` leg uses the same k-space Parseval formula `core.observers.Momentum` uses** (`Σ_k E_k×\overline{B_k}`), not a real-space `np.cross(E,B).sum()`. The two are mathematically identical (Parseval) but differ at the `10^{-15}` floating-point-rounding level depending on evaluation order — measured directly in this session: `np.cross`-based summation gives `\sim1.8\times10^{-14}$ drift for the *identical* input and propagator, over 4× the acceptance bar, purely from a different floating-point evaluation order, while the observer's own manual-cross-product k-space formula gives `3.6\times10^{-15}`, under the bar. This is disclosed because a future session re-measuring this drift with a different (mathematically equivalent) implementation should not conclude the fix regressed if it sees a `~10^{-14}`-scale number from a `np.cross`-based check instead of this module's own formula.
- **The `polarization=` parameter is not wired into any scenario or channel yet.** `scenarios/photon_fermion_push.yaml` and the momentum-sensitive test in F390/F391's own harnesses still call the default (`"linear"`) construction internally via their own beam-seeding code paths; switching those to `"circular"` is Part D's job (a separate finding), not this one's.
- Only the `build_beam_packet` helper is in scope; `photon_step_spectral`, `pair_dispersion`, and every other function in `gauge/photon.py` is unmodified.

**Test record:** `F392-beam-polarization-null-fix` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`). 6/6 legs PASS. One declared control, verified red on exactly 4 of 6 legs (§2). `can-fail` verified.

**Claim:** none — this is an engine-capability/test-helper fix (a beam-construction defect and its repair), not itself a claim against established Standard Model/QM/GR/SR physics; no `docs/claims/` card is issued per D12's bar. It removes a confound from `docs/claims/CL307`'s own evidence base, addressed in that card's own update (see cross-references).

**Cross-references:** [[F390-photon-fermion-push-scenario]] (the finding whose entire momentum-conservation test ran against the zero-momentum beam this finding fixes), [[F391-ck-transverse-beam-mechanism]] (a different, already-fixed beam-construction defect — Euclidean-`k̂` vs `Ĉ(k)` polarization convention — orthogonal to this one; both defects were present simultaneously in F390's own beam), [[F387-curl-anisotropy-omega-pair-mismatch]] (the `Ĉ(k)`-longitudinal leakage this fix does not touch, §4), [[F69-paired-photon]] (decision 5, the Riemann–Silberstein construction this finding's null condition is native to, not imported).
