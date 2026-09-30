# F395 — Stage 5 re-run against the fixed beam: the `m_index=4` anomaly persists, the off-axis breakdown changes, and claim 1 is restated as (A)/(B)/(C)

*2026-09-16 - 02:40 · sector `core` · module `casim.engine.core.photon_fermion_push` (new `beam_polarization=` threading, new `check_stage5_circular_beam_rerun`), `casim.engine.core.coupled` (`EmPhotonChannel`'s `beam_polarization=` config, backward compatible) · test record `F395-stage5-circular-beam-rerun` (assertion, gate tier, 6/6 legs PASS) · results `test-results/F395_stage5_circular_beam_rerun.json` · scenario `scenarios/photon_fermion_push.yaml` (updated to `beam_polarization: circular`)*

**Status:** Confirmed — 6/6 legs PASS, one declared control verified red on exactly 1 of 6 legs. `F390`'s own gate record re-verified bit-identical (8/8 PASS, same numbers) after this session's changes.
**Reviewed:** 2026-09-16 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F395-review-2026-09-16.md))

**Target.** Part D of `docs/roadmaps/photon-fermion-coupling-rerun-prompt.md` — the point of the whole exercise: re-run `scenarios/photon_fermion_push.yaml` and F390's own scenario harness against [[F392-beam-polarization-null-fix]]'s fixed (circular) beam, re-measure F390's `m_index=4` anomaly and off-axis breakdown *before theorising*, and restate the roadmap's Stage-5 claim 1 per `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` §6.2 (crystal momentum, not continuum momentum, is what a lattice conserves).

**Does not repeat Part C.** [[F394-bcc-dec-curl-part-c-decision]] deferred the BCC discrete-exterior-calculus curl complex; this finding's Stage 3 (below) is caveated accordingly, not re-measured against a new curl symbol that does not exist.

---

## 1. Stages 0–4 — confirmed unaffected, not rebuilt

Per the rerun-prompt's own instructions, each of these was **checked, not assumed**, by re-running the real gate test after this session's changes:

| Stage | Instruction | Verified this session |
|---|---|---|
| **0** | Re-run the momentum baseline; `core.observers.Momentum` is verified sound, do not "fix" it. | Confirmed unmodified. `Momentum.P_field = Σ_k E_k×\overline{B_k}` (the class docstring's own derivation) is exactly what [[F392-beam-polarization-null-fix]]'s own drift check reuses (`3.6×10^{-15}` over 40 ticks) — the observer needed no change; only the beam it was fed did. |
| **1** | F384's current is unchanged as algebra; record audit §6.1's point as a named successor route, don't rebuild. | `test_F384_conserved_em_current.py` re-run: 4/4 PASS, identical numbers (`construction_residual=3.10\times10^{-17}$, etc.) to F384's own reported values. The audit's point stands as recorded there — not re-derived here. |
| **2** | F385 unaffected; confirm, don't redo. | `test_F385_u1_link_covariant_step.py` re-run: 10/10 PASS, identical numbers (`norm_drift_slope_fork_a=0.996`, `momentum_transfer_mag={'a':6.26,'b':3.22,'d':9.79}`). |
| **3** | `solve_A_coulomb_3d` inherits the curl defect; caveat since Part C did not land. | Unaffected by this session (`F386`/`F387` re-run: 7/7 and 12/12 PASS, identical numbers). Caveat stands: every `A` this scenario's fermion reads is still built on `bcc_curl_symbol`, whose `curl(\mathrm{grad})=0` failure [[F393-curl-grad-identity-diagnostic]] now gates but does not fix. |
| **4** | Re-run F388 with the fixed beam. | **F388 never used `build_beam_packet` in the first place** — its own `seeded_photon_gives_sustained_push` leg uses `photon.build_pair_mode` (already `E⊥B` correct, F390's own audit confirms this at §2.1), matching F388 §caveats' own disclosure. So there is nothing to "re-run with the fixed beam" for F388 specifically — checked directly (`test_F388_fermion_photon_coupled_channels.py`: 7/7 PASS, `matter_push_end=3.118\times10^{-5}$, matching F388's own reported `\sim3.12\times10^{-5}$ at tick 20) and confirmed unaffected, not merely assumed. |

`F389`'s own two test records were also re-run and confirmed unaffected (3/3 and 4/4 PASS, identical numbers) — its own harness is self-sourced-only (no seeded beam at all).

## 2. Stage 5 — the re-measurement

`photon_fermion_push.build_push_run`/`run_push_scenario`/`check_photon_fermion_push` gained a `beam_polarization=` parameter (default `"linear"`, bit-identical — F390's own gate record re-verified 8/8 PASS with identical numbers after this change). `core.coupled.EmPhotonChannel.init_state` gained the matching `beam_polarization=` config key (same default), and `scenarios/photon_fermion_push.yaml` was updated to `beam_polarization: circular`.

### 2.1 The `m_index=4` anomaly — re-measured, persists

| Config | F390 (linear beam) | F395 (circular beam) |
|---|---|---|
| `cos(ΔP_matter, k̂_beam)`, `axis=0, m=4` | `-0.988` | `-0.949` |

**The sign reversal persists with the fixed beam.** This confirms the audit's own prediction (§8, item 2): `Ĉ=+\hat k` exactly at `m=4` on the x-axis (F387/F391), and [[F392-beam-polarization-null-fix]]'s own acceptance table gives `\cos(P,\hat k)=+1.000000$ at `m=4` on every axis for the beam's *own* momentum — so neither of Part A's defect nor Part B/C's curl-symbol defect can be the mechanism. This is consistent with, and now independently re-confirms from a third angle, [[F391-ck-transverse-beam-mechanism]] §3's own conclusion: the mechanism is on the **matter side** (the fermion's fixed internal spin state, per that finding's `cos=0.517` sensitivity measurement), not the photon sector, and it survives yet another beam-construction fix — this time circular-vs-linear polarization, which is orthogonal to F391's own Ĉ(k)-transversality fix. **Not derived here either.**

### 2.2 The off-axis breakdown — re-measured, and it *changes*, genuinely

This is the one place Part D's "measure, do not predict" instruction produced a real surprise. F390 (linear beam, Euclidean-`k̂`-transverse) and F391 (linear beam, `Ĉ(k)`-transverse) both measured near-total decorrelation for an off-axis (`axis=1`) beam: `\cos(\Delta P_\text{matter},\hat k_\text{beam})\approx-0.002$ in both cases — the two prior beam-construction fixes left this number essentially unchanged. **The genuinely circular beam does not reproduce that:**

| Config | F390 (linear, `k̂`-transverse) | F391 (linear, `Ĉ(k)`-transverse) | F395 (circular) |
|---|---|---|---|
| `axis=1, m=2`: `\cos(\Delta P_\text{matter},\hat k)` | `-0.0019` | `-0.0020` | `+0.328` |
| `axis=1, m=2`: `\cos(\Delta P_\text{matter},\Delta P_\text{field})` | (not reported) | (not reported) | `+0.248` |
| `axis=2, m=2`: `\cos(\Delta P_\text{matter},\hat k)` | `-0.0093` | (not reported) | `-0.101` |
| `axis=2, m=2`: `\cos(\Delta P_\text{matter},\Delta P_\text{field})` | (not reported) | (not reported) | `-0.819` |

Two things are true at once, and both matter: (1) **circular polarization measurably changes the off-axis result**, unlike either prior beam-construction fix — so polarization convention (linear vs. circular), not merely the transversality convention (`k̂` vs. `Ĉ(k)`), is part of the picture; (2) **the change is itself axis-dependent and does not restore a clean, general "direction tracks the beam" rule** — `axis=1` gives a modest positive correlation, `axis=2` a small negative one, neither close to the on-axis `+0.99`. This is disclosed as a genuinely new, measured fact, not theorised further here — a future session wanting the mechanism should treat *both* the polarization convention and F391's own spin-state candidate as live variables, not just the latter.

**Correction, found by the independent review (`docs/reviews/F395-review-2026-09-16.md`) and independently re-confirmed here: the specific point values in the table above are a 20-tick snapshot, not a converged or stable measurement — presenting them as settled comparison numbers overclaimed their precision.** Re-run at `ticks∈{10,20,30,40}` (otherwise the default configuration), re-measured directly:

| `ticks` | `\cos(\Delta P_\text{matter},\hat k)`, `axis=1` | `\cos(\Delta P_\text{matter},\hat k)`, `axis=2` |
|---|---|---|
| 10 | `+0.260` | `-0.184` |
| 20 (this finding's own default) | `+0.324` | `-0.096` |
| 30 | `+0.225` | `-0.085` |
| 40 | `+0.160` | `+0.102` |

`axis=1`'s correlation drifts non-monotonically and falls to `0.160` by tick 40 — **below** the gate leg's own `>0.2` threshold, meaning the leg's PASS is a property of the specific `ticks=20` default, not a stable fact that would survive a longer run at face value. `axis=2`'s correlation **changes sign** between tick 30 and tick 40. Neither series shows a sign of settling to a steady state within the window tested. **The qualitative claim survives**: at every tick count tested, both axes measure a nonzero, non-`\approx0$ correlation — genuinely different from F390/F391's own near-machine-zero numbers at every tick count they reported — so "circular polarization changes the off-axis result relative to either linear-type fix" remains true. **The specific numbers `+0.328`/`-0.101` do not** — they should be read as one snapshot of a still-evolving quantity, not a settled measurement, and any future citation of this finding (including the claim-card update below) should say so rather than quote them as fixed values.

### 2.3 Claim 1, restated per the audit's §6.2

The roadmap's claim 1 (`ΔP_matter+ΔP_field\approx0$ for a continuum-style `P`) is **withdrawn as unachievable**, not left open, per the rerun-prompt's own instruction. Replaced with three targets, each measured directly against casim's actual construction (not the audit's own single-action prototype):

**(A) Exact charge conservation.** **Not delivered by the existing bridged architecture.** Measured: the fermion's own norm (`\Sigma|\psi|^2$, the model's own conserved probability/charge density) drifts by `0.54\%$ over the scenario's 20 ticks under the actual per-link covariant step (F385 fork a, the gate-level choice) — bounded (matching F385's and F388's own already-established `O(|qA|\cdot a)$ drift, and F388's own `norm_drift_bounded` leg), but genuinely nonzero, not the audit §6.2's "delivered outright" language. **That language described the audit's own §7 single-action *prototype* (a genuine lattice Ward identity from `\partial H/\partial A`), which casim's actual construction does not implement** — F385's fork (a) is a norm-violating, Peierls-phase per-link step chosen explicitly over the unitary alternatives because it is the one the roadmap asked for at the gate level (F385 §4). Target (A) is real and achievable, but only via the single-action route audit §6.1 describes — not by anything running today.

**(B) Exact crystal-momentum conservation**, checked directly as `\Phi\circ T=T\circ\Phi$: translate the *entire* initial state (fields and fermion together) by one lattice site, run the simulation, and compare against running first and translating the result. **Holds to machine precision**, measured `1.5\times10^{-15}$ (relative) — because none of the per-tick update rules (`photon_step_spectral`'s FFT-diagonal rotation, `u1_link_weyl_step_3d_bcc`'s shift-based hop, `solve_A_coulomb_3d`'s algebraic Gauss solve) reference an absolute lattice coordinate; each is built from convolutions/shifts that commute with translation by construction. This is genuinely delivered, and gated for the first time here.

**(C) Matched-order approach to the continuum.** **Still mismatched**, but the mismatch itself takes a different shape than F389 §4's self-sourced case, and the difference is itself informative. Doubling `g_lat`: `\|\Delta P_\text{matter}\|$ scales by `\times0.994$ (essentially flat) while `\|\Delta P_\text{field}\|$ scales by `\times2.036$ (roughly linear, *not* F389's own `\times\!\sim\!4$ quadratic). **The flat matter-push ratio is not evidence of a matched order** — it is F390 §3's own already-disclosed fact that `\|\Delta P_\text{matter}\|$ in this beam-driven scenario is set almost entirely by the *coupling-independent* unconditional per-link push (F388 §2's mechanism), not by anything that scales with `g_lat` at all. So the "order" being measured for the matter channel here is dominated by a term with no coupling dependence, while the field channel's order is genuinely `g_lat`-driven — the two remain structurally unmatched, for a reason one level more specific than F389's original diagnosis, not because the fix changed the underlying architecture (it did not).

## 3. What moved and what did not

**Moved:** the off-axis correlation's qualitative behaviour (§2.2) — a real, new, robust-to-coupling-strength result, though its specific point values are a non-converged snapshot, not a settled measurement (§2.2's correction). **Did not move:** claim 2's on-axis confirmation (`\cos=0.994$, matching F390/F391 to 3 significant figures), the `m_index=4` anomaly (still present, still unexplained by any photon-sector fix), and claim 1's fundamental unachievability (now given a precise, three-part replacement rather than an open residual).

## 4. Caveats

- **The off-axis result (§2.2) is not converged in run length, and this finding's first version overclaimed it as a settled pair of numbers — found by the independent review, corrected in §2.2.** The gate leg (`ticks=20`) is honestly reproducible at that specific configuration, but a reader should not treat `+0.328`/`-0.101` as the off-axis correlation's asymptotic value; §2.2's own tick-sweep table shows it has not settled by tick 40. The gate leg itself is not wrong (it measures exactly its own declared configuration, reproducibly), but the prose around it needed the correction now in place.
- **The off-axis result (§2.2) is not derived, only measured**, and only at two off-axis configurations (`axis=1` and `axis=2`, both `m_index=2`) — matching the scope F390/F391 themselves used, not a systematic grid. A future session should treat both circular-vs-linear polarization *and* F391's spin-state candidate as simultaneous, not yet disentangled, variables.
- **Target (A)'s `0.54\%$ drift is this specific configuration's number**, not a general bound — F385 already established the drift scales with `|qA|\cdot a$; a stronger-coupling or longer run would show more, per that finding's own derivation, not a new one here. **The gate leg testing it (`0<charge_drift<0.5`) is weak, found by the independent review**: sweeping coupling to `16×` default and run length to `5×` default, the measured drift never exceeded `~0.10`, nowhere near the `0.5` ceiling — the leg would not catch a materially larger drift than what is already reported. The prose claim (§2.3(A)) is honestly measured; the registry threshold is a loose sanity bound, not a tight one, matching the same scoping gap F388's own `norm_drift_bounded` leg already disclosed for the identical mechanism. Not tightened here — a future session could derive a tighter bound from F385's own `O(|qA|\cdot a)` scaling rather than the current arbitrary ceiling.
- **Target (C)'s doubling-ratio measurement uses only one doubling step** (`g_lat\to2g_lat$), matching F390/F389's own precedent; a fuller `O(g^n)` characterization (multiple doublings, log-log slope) is not attempted here.
- **Part C (the BCC DEC curl) did not land** ([[F394-bcc-dec-curl-part-c-decision]]) — every number in this finding still runs through `bcc_curl_symbol`'s own, now-gated ([[F393-curl-grad-identity-diagnostic]]) defect. Stage 3's caveat (§1 table) is not resolved by anything in this finding.
- Only the Weyl 2-spinor / U(1) sector is covered, matching F384–F391's own scope.

**Test record:** `F395-stage5-circular-beam-rerun` (`tests/registry/core.yaml`, kind `assertion`, tier `gate`, `expect.exactness: quantitative`). 6/6 legs PASS. One declared control, verified red on exactly 1 of 6 legs. `can-fail` verified.

**Claim:** see [[CL307-photon-fermion-push-partial-recoil-not-conservation]] — this finding's re-measurement and claim-1 restatement update that card directly (§ its own file); no new card is issued.

**Cross-references:** [[F392-beam-polarization-null-fix]] (the fix this finding re-runs against), [[F393-curl-grad-identity-diagnostic]], [[F394-bcc-dec-curl-part-c-decision]] (the still-open curl defect this finding's Stage 3 caveats), [[F390-photon-fermion-push-scenario]], [[F391-ck-transverse-beam-mechanism]] (the two prior beam-construction fixes this finding's off-axis result diverges from), [[F389-radiative-transverse-em-current]] (the `O(g)`-vs-`O(g²)` mismatch this finding's target (C) re-measures in the beam-driven case), [[F388-fermion-photon-coupled-channels]] (the unconditional-push mechanism behind target (C)'s flat matter ratio).
