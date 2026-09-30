# F387 — the Ĉ(k) direction anisotropy and the Ω_pair(k)/|C_odd(k)| sourcing mismatch: a Stage-4 design fix

*2026-09-15 - 09:08 · sector `gauge` · module `casim.engine.gauge.em_photon_sourcing` (new) · test record `F387-curl-anisotropy-omega-pair-mismatch` (assertion, gate tier, 12/12 legs PASS) · results `test-results/F387_curl_anisotropy_omega_pair_mismatch.json`*

**Status:** Confirmed — 12/12 legs PASS, control verified red on exactly the two declared legs.
**Reviewed:** 2026-09-15 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F387-review-2026-09-15.md)). Data, fix, and module unchanged; the review found §2's original prose overstated the causal role of the `Ω_pair(k)`/`|C_odd(k)|` value-mismatch in the `iĈ·B≠0` defect (an elimination experiment shows the defect persists, undiminished, even with the mismatch removed by construction) — corrected in-pass to attribute the defect to its actual, structural, value-independent cause (no `Ĉ(k)`-projection in any scalar rotation law).

**Target.** Two structural facts the [F386 review](../docs/reviews/F386-review-2026-09-14.md) surfaced and explicitly left open (`findings/F386-a-field-convention.md` §5–6): (1) whether `charge_coupling.bcc_curl_symbol`'s direction anisotropy is already accounted for by F87 or needs its own finding; (2) what Stage 4 of `docs/roadmaps/photon-fermion-coupling.md` should do about `photon.pair_dispersion` (`Ω_pair(k)`) and `bcc_curl_symbol`'s magnitude `|C_odd(k)|` being different functions of `k`. This finding answers both and ships a concrete, machine-precision-verified fix for the second.

---

## 1. The direction anisotropy — new, not covered by F87

`bcc_curl_symbol`'s direction does not converge to `k̂` as `k→0` off the cubic axes. Measured (reproducing the review's numbers independently, on the actual grid-based `bcc_curl_symbol`, not just the analytic small-`k` formula):

| Direction | angle(`Ĉ(k)`, `k̂`) | Predicted |
|---|---|---|
| cubic axis `(1,0,0)` | `0.000000°` | `0` |
| face diagonal `(1,1,0)` | `90.000000°` | `90°` |
| body diagonal `(1,1,1)` | `70.528779°` | `arccos(1/3) = 70.528779°` |

**Stable from `L=16` to `L=128`** — measured *exactly* `70.52877936550931°` at the smallest nonzero body-diagonal grid mode for every `L` in `{16, 32, 64, 128, 256}`. This confirms the review's claim: the angle is a genuine continuum-limit property of `bcc_curl_symbol`'s construction, not a finite-lattice artifact that would shrink as `L→∞`. The exact limiting direction is `Ĉ(k) → (k_x, −k_y, k_z)/|k|`. **Scoping note:** the registered, re-runnable gate leg `curl_direction_anisotropy_stable_with_L` only compares two of these (`L=16` vs `L_stability=64`), not the full five-point sweep — the broader `L`-independence above was checked directly for this finding (and independently reproduced by the F387 review) but is not itself something `casim test` re-verifies on every run.

**Why: the same sign correction `_bcc_uvec` carries for the fermion walk.** `bcc_curl_symbol` (`charge_coupling.py`) builds its vector from `_bcc_uvec(k/2, sign='+')`'s `n^+` — the *same* object `lattice.bcc.bcc_spin_axis` uses for the Weyl walk's spin-quantisation axis, whose own docstring already states the small-`k` limit `n̂ → (k_x, −k_y, k_z)/|k|` and calls the `y`-sign flip "an intrinsic chirality convention of the Bisio BCC walk" — correct and load-bearing for spin–momentum locking (`_bcc_uvec`'s own inline comment: without the corrected sign, `u²+|n|²=1` fails by `4.7e-01` instead of holding to `4.4e-16`; changelog 2026-05-15). `bcc_curl_symbol` inherits that sign unchanged when it reuses `n^+(k/2)` as a Maxwell curl generator for a *different* physical object (the photon's `(E,B)` curl, not a fermion's spin axis) — nothing about the reuse is wrong, but nothing previously stated that a fermion-sector chirality convention was now also defining "transverse" for the photon sector.

**Isotropic magnitude, unaffected.** `|C|/|k| → 1/√3` independent of direction to `O(k²)` (measured axis-vs-body-diagonal difference: `7.4e-3` at `L=16` → `4.6e-4` at `L=64` → `1.2e-4` at `L=128`, shrinking `4×` each doubling — the expected leading-order convergence). Squaring removes the sign that produces the direction anisotropy, so every existing speed/`c_lat`/magnitude check (F87's MX1, F26's `c_lat`) is untouched.

**Is this already covered by F87?** No. `findings/F87-charge-coupling-paired-photon.md`'s only magnitude/direction-adjacent check is `MX1: |C|/|k| → 1/√3` — a magnitude-only statement. F87 never measures `Ĉ(k)`'s *direction* against `k̂` anywhere in its 20 checks (AB1–AB5, MX1–MX5, E2E). The underlying sign-convention fact was documented once, in `bcc_spin_axis`'s docstring, for the fermion spin axis — a different physical quantity in a different module, with no cross-reference to `charge_coupling.bcc_curl_symbol`. So: **the mathematical fact was known (in `bcc.py`); its consequence for the photon/charge-coupling curl generator was not, anywhere** — this is what the review found and what this finding now makes explicit and citable. It gets this finding number per the review's own request (F386 §6: "flagged for a future session to reconcile against F87 and to decide whether it needs its own finding number").

**Does it require a code fix?** No. Every existing consumer of `bcc_curl_symbol` (`solve_A_coulomb_3d`, `magnetostatic_B`, `maxwell_curl_step`, `em_current.conserved_current`) already measures transversality/longitudinality against `Ĉ(k)` itself, not the naive Euclidean `k̂` — so the anisotropy was never silently assumed away by those functions; it was simply undocumented as a *fact about the yardstick*. The one place it does bite is exactly what F386 §6 already disclosed: the beam/mode *test helpers* (`photon.build_beam_packet`, `build_pair_mode`) build polarizations transverse to `k̂`, not `Ĉ(k)`, so they leak `Ĉ(k)`-longitudinal content that grows with `L` at fixed physical packet parameters — already caveated there, not reopened here.

## 2. The Ω_pair(k)/|C_odd(k)| mismatch — a related but non-causal fact; the actual mechanism

Two distinct "curl symbols" exist in this codebase and are used by different parts of the sourcing pipeline:

* **`photon.pair_dispersion`, `Ω_pair(k)`** — a real *scalar*. `photon_step_spectral` rotates `(E,B)` by this angle *identically across every Cartesian component*, performing no `Ĉ(k)`-projection whatsoever. This is decision 5's canonical, non-birefringent photon propagator (F67–F69) and is unchanged by this finding.
* **`charge_coupling.bcc_curl_symbol`, `C_odd(k)`** — a real *3-vector*. `maxwell_curl_step`, `em_current.conserved_current` (F384), and `solve_A_coulomb_3d` (F386) all build on it via cross products, which structurally cannot generate a `Ĉ(k)`-longitudinal `B` from a `Ĉ(k)`-transverse source.

They agree only at small `k`: measured `Ω_pair(k)/|C_odd(k)| = 1.000134` at the smallest nonzero grid mode (`L=64`), diverging to `1.954` at the Brillouin-zone-edge body-diagonal mode (`L=16`, `m=7` of `m_max=8`) — a factor-of-2 disagreement, not a rounding effect. (Table, body diagonal, `L=24`: `m=1 → 1.005`, `m=4 → 1.091`, `m=8 → 1.444`, `m=11 → 2.108`.)

**The mismatch above is *not* what causes the violation described next — verified by elimination (F387 review, 2026-09-15).** Substituting `Om = |C_odd(k)|` exactly for `Ω_pair(k)` inside an otherwise-identical scalar per-mode rotation step (i.e. removing the value-mismatch by construction, so the substituted law and `|C_odd(k)|` agree at *every* `k`, not just small `k`) still produces `‖iĈ·B‖ = 2.485` by tick 6 on the same scenario §4 measures — marginally *larger* than the `2.415` measured with the real `Ω_pair`, not smaller. So the mismatch's size is not even the dominant driver of the defect's magnitude, let alone its existence: the dominant, in fact sufficient, cause is structural, independent of which particular scalar `Ω(k)` the rotation uses (§3 below states this precisely). The value-mismatch quantified above remains a real, separate structural fact worth recording — it matters for other purposes, e.g. it rules out "just substitute `|C_odd(k)|` for `Ω_pair(k)`" as a fix, since that substitution changes nothing about the defect while also giving genuine transverse photon content the wrong (non-canonical) dispersion — but it is not the reason sourcing breaks the no-monopole invariant.

**Consequence (already disclosed as a bug symptom in F386 §5; the mechanism, traced here, is structural, not the value-mismatch):** the roadmap's own Stage-4 sketch — `E += g·J` applied to the whole `Ω_pair`-rotated field — sources a purely-`Ĉ(k)`-longitudinal current (F384's conserved current is *defined* that way) directly into the rotation. Since `photon_step_spectral` applies the same rotation to every Cartesian component with **no `Ĉ(k)`-projection whatsoever** — a property of *any* scalar per-mode rotation law, matched to `|C_odd(k)|` in value or not, per the elimination test above — a purely-longitudinal `E` rotates into an equally longitudinal, *nonzero* `B`: `i Ĉ·B ≠ 0`, growing every tick. Reproduced here: `naive_sourced_scenario` (the literal roadmap recipe) reaches `‖iĈ·B‖ = 2.41` by tick 6 (`L=16`, `g=0.5`) from a static Weyl packet's own F384 current — a genuine violation of this model's own no-monopole invariant, not a numerical artifact.

## 3. The key structural fact that makes the fix exact, not heuristic

`photon_step_spectral` applies the *same* `2×2` `(E,B)` rotation independently to each Cartesian component (the rotation matrix depends only on `k`, broadcasting identically over the `x,y,z` axis). The `Ĉ(k)`-transverse/longitudinal projector (`split_transverse_longitudinal`, built from the same `bcc_curl_symbol` machinery `solve_A_coulomb_3d` uses) acts only on the Cartesian/direction index, identically for `E` and `B`. These two operators act on different tensor factors of the per-mode 6-dimensional `(E_x,E_y,E_z,B_x,B_y,B_z)` space, so **they commute exactly**:

$$R(\Omega_\text{pair}(k)) \otimes I_3 \;,\qquad I_2 \otimes P_{\hat C}(k) \;\;\Rightarrow\;\; [R\otimes I_3,\; I_2\otimes P_{\hat C}] = 0 .$$

Measured on random `(E,B)` fields of norm `≈72` (`L=12`): rotate-then-project vs. project-then-rotate agree to `‖Δ‖ ≈ 2.9×10⁻¹⁴` — relative `≈4×10⁻¹⁶`, machine round-off (`rotation_commutes_with_TL_projection`). Direct corollary, also verified: a purely-`Ĉ(k)`-longitudinal `(E,B)` stays purely longitudinal under free rotation forever, and a purely-transverse one stays purely transverse forever (`‖B_r − (B_r)_T‖/‖B_r‖ ≈ 4×10⁻¹⁶` either way). **The two sectors never mix under the free propagator; all of F386 §5's mixing came from the sourcing step, not the rotation.**

## 4. The fix — a sector split, not a wholesale propagator swap

This directly answers the question F386 §5 posed ("should sourcing use `maxwell_curl_step`'s law instead of `photon_step_spectral`?") with a more precise recipe than either wholesale option: **neither is replaced.** `Ω_pair` stays the propagator for the genuine radiative (transverse) sector, exactly as decision 5 established; the `Ĉ(k)`-based Gauss/current machinery stays the sourcing law for the non-propagating (longitudinal, Coulomb) sector — the lattice analogue of the continuum split between a transverse radiation field (wave equation) and an instantaneous Coulomb field (Gauss's law, never touches `B`). This fix does not, and does not need to, reconcile `Ω_pair(k)` and `|C_odd(k)|`'s disagreement (§2) — it renders that disagreement irrelevant to the no-monopole invariant by construction, since the longitudinal sector is never touched by `Ω_pair`'s rotation at all under the split.

`em_photon_sourcing.split_sourced_scenario` implements it: split the current `J` into `Ĉ(k)`-transverse/longitudinal parts (§3's `split_transverse_longitudinal`, the same projector `solve_A_coulomb_3d`/`magnetostatic_B` already use — no new curl operator); rotate only `(E_T,B_T)` by `photon_step_spectral`, sourced by `J_T`; carry the charge density `ρ` forward via the model's own continuity law `∂_tρ=−iĈ·J` (F384) and solve `E_L` *algebraically* each tick from the instantaneous Gauss law `iĈ·E_L=ρ`; `B_L` is never populated at all.

**Measured, same scenario as §2 (`L=16`, `n_ticks=6`, `g=0.5`, static F384 current):**

| Recipe | `‖iĈ·B‖` at tick 6 | `‖E_L‖` at tick 6 |
|---|---|---|
| naive (roadmap sketch, unprojected) | `2.41` | — (never computed) |
| split (this finding's fix) | `2.76×10⁻¹⁶` | `0.298` |

`iĈ·B=0` holds **by construction** in the fix (nothing to cancel — `B_L` is structurally never assigned a value), not by a numerical coincidence, while the charge's own Coulomb field (`E_L`) still correctly grows to carry the sourced charge — the fix does not simply discard the current's effect, it routes it to the sector that can represent it without breaking the no-monopole invariant. Sanity check: with `J=0` the split recipe's transverse output is bit-identical to plain `photon_step_spectral` iterated on its own (`uncharged_residual_vs_free_rotation = 0.0`) — the fix changes nothing about ordinary free photon propagation.

## 5. Test results

| Leg | Claim | Measured | Verdict |
|---|---|---|---|
| `curl_direction_matches_cubic_axis` | angle(`Ĉ`,`k̂`)=0° on-axis | `0.0°` | PASS |
| `curl_direction_face_diagonal_90deg` | angle=90° on a face diagonal | `90.0°` | PASS |
| `curl_direction_body_diagonal_arccos_1_3` | angle=`arccos(1/3)` on the body diagonal | `70.528779°` | PASS |
| `curl_direction_anisotropy_stable_with_L` | angle unchanged `L=16→64` | `70.52877936550931°` both | PASS |
| `curl_magnitude_isotropic` | `|C|/|k|` axis≈body to `O(k²)`, `L=64` | `Δ=4.6×10⁻⁴` | PASS |
| `omega_pair_matches_curl_at_small_k` | `Ω_pair/|C_odd|→1` at small `k`, `L=64` | `1.000134` | PASS |
| `omega_pair_diverges_from_curl_away_from_small_k` | ratio `>1.3` near BZ edge, `L=16` | `1.954` | PASS |
| `rotation_commutes_with_TL_projection` | rotate∘project = project∘rotate | `2.0×10⁻¹⁶` (relative) | PASS |
| `naive_sourcing_violates_no_monopole` | roadmap-sketch recipe: `‖iĈ·B‖` grows | `2.41` (tick 6) | PASS |
| `split_sourcing_preserves_no_monopole` | fix: `‖iĈ·B‖` stays ≈0 | `2.76×10⁻¹⁶` | PASS |
| `split_sourcing_couples_charge_into_EL` | fix still carries the charge's Coulomb field | `‖E_L‖=0.298` | PASS |
| `split_sourcing_reduces_to_free_rotation_when_uncharged` | `J=0` ⇒ identical to plain `photon_step_spectral` | `0.0` | PASS |

**Test record:** `F387-curl-anisotropy-omega-pair-mismatch` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`). 12/12 legs PASS. One declared control: `use_split_for_no_monopole_check: false` swaps the naive (unprojected) recipe in for the fix legs, which — measured, not assumed — turns exactly `split_sourcing_preserves_no_monopole` (`2.41` monopole residual, matching the naive leg exactly, as expected: it *is* the naive recipe under the flag) and `split_sourcing_couples_charge_into_EL` (the fallback path never computes `E_L` at all, so its norm reads `0.0`, honestly below the leg's threshold) red, while every other leg — none of which reads the flagged scenario — stays green.

## 6. What this does and does not close

This gives Stage 4 a concrete, verified sourcing recipe for `em_photon`: replace the roadmap's literal `E += g·J` sketch with `split_sourced_scenario`'s pattern (transverse sector: `Ω_pair` rotation + `J_T` source; longitudinal sector: algebraic Gauss solve from `ρ`, continuity-updated). It does **not** build the coupled `Channel` pair itself (`em_photon`/`fermion_em`, still Stage 4's job — this finding supplies the sourcing law one of its two channels should use, not the `Channel` subclass, topology-tag fix, or registration), and it does not run with a *dynamical* current (this finding's `J` is static, matching F386's own harness — a real `em_photon`/`fermion_em` loop's current changes every tick as the fermion channel evolves, which is Stage 4/5's scope). The charge-continuity update (`∂_tρ=−iĈ·J`) is exact for a static `J`; a dynamical current would need `ρ` integrated tick-by-tick from the fermion channel's own evolving current rather than a single precomputed `drho`, which this finding's harness does not exercise.

## 7. Caveats

- **The `Ĉ(k)`-transverse/longitudinal split inherits the same disclosed Nyquist-corner gap every other `bcc_curl_symbol` consumer has** (F384 §3): the 7 non-origin Brillouin-zone-corner modes where `C(k)≡0` exactly have no projection defined; `split_transverse_longitudinal` puts all of a mode's content in `V_T` there by convention (nothing to remove), matching `solve_A_coulomb_3d`'s treatment of the same modes.
- **`curl_magnitude_isotropic` and `omega_pair_matches_curl_at_small_k` are leading-order (`O(k²)`) statements**, checked on a finer grid (`L_stability=64`) than the rest of the record (`L=16`) precisely because the residual is `k`-dependent and shrinks with `L`; this is disclosed in-line in the module rather than left implicit, matching the F384/F385/F386 reviews' own scoping-transparency fix.
- **This finding's sourcing scenario uses a static current**, matching F386's harness precedent — see §6. A future Stage-4 session building the actual dynamical coupled channels should re-verify the no-monopole leg under a current that changes tick-to-tick, not assume this finding's static-current result generalizes without re-measurement.
- **The direction-anisotropy legs are exact by construction on symmetric directions** (cubic axis, face diagonal, body diagonal, and the tested generic `(2,1,0)` direction from the review) but this finding does not attempt a general closed-form `angle(Ĉ(k),k̂)` for arbitrary direction — the review's four sampled directions (now reproduced here) are the full extent of what is checked.
- Only the U(1)/EM sector is covered; the anisotropy's consequence (if any) for the non-Abelian curl generators (W/Z/gluon, still on the σ-bilinear construction, F68 part 3) is out of scope here.
- The `exactness="machine"` tag covers every leg here (all residuals `≤2.8×10⁻¹⁴` except the two explicitly-scoped `O(k²)` legs, which are their own honestly-disclosed asymptotic-tolerance class, and the two threshold-style "does it exceed a bound" legs `omega_pair_diverges_from_curl_away_from_small_k` / `naive_sourcing_violates_no_monopole`, which are qualitative by their own nature — they assert a defect exists, not a value to round-off).

**Claim:** none — this is an engine-capability/interface investigation and design fix (how Stage 4's `em_photon` channel should source `E` consistent with the model's own no-monopole invariant), not a claim against established Standard Model/QM/GR/SR physics; no `docs/claims/` card is issued per D12's bar.

**Cross-references:** [[F386-a-field-convention]] (§5–6, where both structural facts were first surfaced and left open), [[F385-u1-link-covariant-step]], [[F384-conserved-bcc-em-current]] (the purely-longitudinal current whose sourcing this finding resolves), [[F87-charge-coupling-paired-photon]] (confirmed above to disclose the curl symbol's magnitude only, never its direction — the gap this finding closes).
