# F391 — F390's beam-polarization mismatch is ruled out as the direction/anti-alignment breakdown mechanism; the actual candidate is spin-dependence, not derived; Thomson cross-section stays out of reach

*2026-09-16 - 00:10 · sector `gauge` · module `casim.engine.gauge.em_photon_sourcing` (new `build_ck_transverse_beam_packet`, `check_ck_transverse_beam_mechanism`) · test record `F391-ck-transverse-beam-mechanism` (assertion, gate tier, 9/9 legs PASS) · results `test-results/F391_ck_transverse_beam_mechanism.json`*

**Status:** Confirmed (negative/redirected result) — 9/9 legs PASS, declared control verified red on exactly the two declared legs.
**Reviewed:** 2026-09-16 - 12:05 — cold-subagent blind re-derivation (retried once after a self-disclosed forbidden-file read) + adversarial referee, 13-point attack pass: 7 PASS / 1 WEAKENS / 2 FAIL(fixed) / 3 NOT RUN — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F391-review-2026-09-16.md)). The physics content (the beam fix changes nothing; the two new exact `Ĉ(k)` axis facts; the spin-state sensitivity) was independently reproduced bit-for-bit by both a blind subagent (a differently-coded construction, different defaults) and the referee (the real code, plus 3 extra perturbations and 1 extra spin state, all consistent). The review found and fixed one real defect, in tooling only, not physics: the registry's declared control (`tests/registry/gauge.yaml`) named a phantom leg belonging to F387's entry point rather than F391's own, making the control mechanically `INVALID` at review time; corrected to the two real legs and re-verified `CONTROL`. A separate, pre-existing, out-of-scope defect on F387's own control (`SPILL`) was found incidentally and spawned as a background-task suggestion rather than fixed here.

**Target.** The two structural gaps `findings/F390-photon-fermion-push-scenario.md` §3/§6 and `docs/reviews/F390-review-2026-09-15.md` left open: (1) F390's direction/anti-alignment claims hold only for an on-axis beam at `m_index≤3` (`L=16`); a "likely, not derived" mechanism was named (`photon.build_beam_packet` polarizes transverse to the Euclidean `k̂`, not `Ĉ(k)`, combined with F387's documented `Ĉ(k)` axis anisotropy) — build a genuinely `Ĉ(k)`-transverse beam and re-test whether the mismatch is the cause; (2) reconsider Stage 5's Thomson-cross-section stretch goal only if (1) makes the physics well-posed enough.

**The answer.** (1) **The named mechanism is ruled out.** A beam built to be exactly `Ĉ(k)`-transverse mode-by-mode (zero longitudinal leak to machine precision, vs. F390's own ~27.5%) reproduces the identical breakdown pattern — same on-axis correlation, same `m_index=4` sign flip, same off-axis decorrelation, to 3-4 significant figures. The mismatch F390/F387 flagged as "likely" is real (it exists, it is exactly what F387 §caveats measured) but it is not what causes the breakdown; removing it changes nothing. A sharper, previously-untested structural fact about `Ĉ(k)` is confirmed along the way (`Ĉ(k)` is exactly *anti-parallel* to `k̂` along the lattice's own y-axis — `180°`, not merely "some other angle" — while the z-axis stays exactly aligned, `0°`, like x), and a different candidate mechanism is identified (the per-link step's sensitivity to the fermion's own fixed internal spin state) but **not derived**. (2) **The Thomson cross-section stays out of reach**, for a sharper reason than F390 gave: the breakdown is no longer just an unresolved modeling artifact in the *input* (a fixable beam-construction convention) — it is now known to depend on an arbitrary internal degree of freedom (the fermion's own spin state) that F390's construction sets once, by an unexamined default, and never varies. A cross-section computed against that default would be a statement about one arbitrary spin choice, not about the coupling.

---

## 1. The negative result — a genuinely `Ĉ(k)`-transverse beam changes nothing

`build_ck_transverse_beam_packet` (new, `em_photon_sourcing.py`) builds the same envelope/carrier construction as `photon.build_beam_packet` (a one-sided analytic signal `F(x) = envelope(x)·exp(ik0(x_axis−x0))`), but instead of assigning `F(x)` to one fixed Cartesian polarization component, it projects the reference polarization direction `v0` onto the plane orthogonal to `Ĉ(k)` **at every Fourier mode independently** and renormalizes:

$$\mathbf e(\mathbf k) = \widehat{\mathbf v_0 - \hat{\mathbf C}(\mathbf k)\,(\hat{\mathbf C}(\mathbf k)\cdot \mathbf v_0)}$$

so `e(k)·Ĉ(k) ≡ 0` exactly (for `Ĉ(k)≠0`), by construction — not by projecting-and-discarding the finished field after the fact, the way `photon_fermion_push.build_push_run` uses `split_transverse_longitudinal` on F390's original beam. No norm is thrown away: the polarization direction simply follows `Ĉ(k)`'s own local transverse plane instead of a single fixed lab-frame direction.

**Verified genuinely transverse, to machine precision** (`L=16`, `m_index=2`, `axis=0`, `σ=3.0`): `‖iĈ·B‖ = 7.6×10⁻¹⁴` and the residual `Ĉ`-longitudinal fraction of `E` is `0.031` — the small residual traced entirely to the disclosed Nyquist-corner modes where `Ĉ(k)≡0` and no transverse plane exists to project onto (F384 §3; the fallback there is `v0` itself, not transverse to anything). Contrast: F390's original beam recipe (`build_beam_packet` + post-hoc `split_transverse_longitudinal`) leaks **`27.5%`** of its own norm as `Ĉ(k)`-longitudinal content before it is even discarded — reproducing F387/F390's own disclosed number exactly.

**Re-running F390's own axis/m_index grid with the new construction, side by side with the original:**

| Config | `cos(ΔP_matter,k̂_beam)` — new (`Ĉ(k)`-transverse) | — old (F390's original) |
|---|---|---|
| `m_index=2, axis=0` (on-axis default) | `0.9926` | `0.9948` |
| `m_index=4, axis=0` (the sign flip) | `-0.9874` | `-0.9884` |
| `m_index=2, axis=1` (off-axis) | `-0.0020` | `-0.0019` |

Every number agrees to 3 significant figures. **The fix changes essentially nothing.** This directly falsifies the "likely mechanism" F390 §3 and the F390 review both named as plausible: the beam's own `Ĉ(k)`-transversality was never what was breaking the direction correlation off-axis or at `m_index=4`. `docs/claims/CL307`'s stated route back toward `live` — "a derivation identifying and correcting the specific mechanism... that recovers the broad, axis-independent form" — is now known not to run through this route; see §4.

## 2. A sharper `Ĉ(k)` structural fact — extending, not correcting, F387

F387 §1 tabulated `angle(Ĉ(k),k̂)` on four directions: the cubic axis `(1,0,0)` (`0°`), the face diagonal (`90°`), the body diagonal (`arccos(1/3)=70.53°`), and (in its own review) a generic `(2,1,0)` direction (`53.13°`). It never tested the y-axis or z-axis *in isolation* — a real gap, since the underlying sign convention `_bcc_uvec` carries (`n_y^± = ∓c_xs_yc_z + s_xc_yc_z` — "an intrinsic chirality convention," per that module's own docstring, and per F387 §1 the source of the anisotropy) singles out the y-coordinate specifically, not merely "some direction relative to the cubic lattice." Measured directly (`L=64`, smallest nonzero grid mode):

| Direction | `angle(Ĉ(k),k̂)` |
|---|---|
| x-axis `(1,0,0)` (F387's own table) | `0°` |
| **y-axis `(0,1,0)` (new)** | **`180°`** |
| **z-axis `(0,0,1)` (new)** | **`0°`** |

`Ĉ(k)` is exactly *anti-parallel* to `k̂` for a beam propagating along the lattice's own y-axis — not merely rotated away from it by some anisotropic angle, but pointing the opposite way. z behaves like x (aligned); only y is singled out. **Stable from `L=64` to `L=128`** (`180.000000°` exactly at both), confirming — by the same method F387 used for its own four directions — that this is a continuum-limit property of the construction, not a finite-lattice artifact.

**Why this is consistent with, and sharpens, F387's own small-`k` formula.** F387 §1 gives the limiting direction `Ĉ(k) → (k_x,−k_y,k_z)/|k|` as `k→0`. This is exactly the map `R = \mathrm{diag}(1,-1,1)` applied to `k̂` — an orthogonal **reflection** (`R^2=I`, `\det R = -1`), not a rotation. Evaluated on `k̂ = ŷ = (0,1,0)`: `Rŷ = (0,-1,0) = -ŷ`, i.e. exactly `180°` — the y-axis result above is this formula's own prediction, simply never evaluated there before. A broader numerical check (informational, not gated — reported for context, not re-verified by `casim test`) confirms `Ĉ(k)̂ ≈ R k̂` to `O(k)` for generic (non-symmetric) directions too, with the residual `‖Ĉ̂(k) - Rk̂‖` growing from `~7×10⁻⁴` near `k=0` to `~1` near the Brillouin-zone edge on an `L=64` grid — consistent with F387's own leading-order framing, extended here from four special directions to a general small-`k` closed form. This closed form is not itself gated (F387 already scoped its own direction legs to symmetric directions only, §caveats; this finding does not attempt a general-direction gate leg either) — only the two new axis facts (§2's table, both exact and `L`-stable) are promoted to permanent gate legs.

## 3. What actually varies the push direction, then — a candidate, not a derivation

Having ruled out the beam's own transversality convention, a direct diagnostic sweep (informational — reported here, not separately gated beyond the one leg below) varied the beam's propagation axis and polarization axis independently (`axis, pol_axis ∈ {0,1,2}`, `axis≠pol_axis`, six valid combinations, `m_index=2`, otherwise F390's default configuration) and inspected the *full* matter-recoil vector, not just its cosine with `k̂`:

| `(axis, pol_axis)` | Dominant component of `ΔP_matter` | Matches beam's `k̂`? |
|---|---|---|
| `(x, y)` — F390's own default | **x** | Yes |
| `(x, z)` | y | No |
| `(y, x)` | y | No |
| `(y, z)` — F390's off-axis default | **x** | No |
| `(z, x)` | y | No |
| `(z, y)` | x | No |

Two things stand out. First, **the recoil is confined to the x–y plane in every one of the six combinations tested — never dominantly along z** — a much more specific, and more surprising, fact than "off-axis beams decorrelate." Second, **`(axis=x, pol=y)` — F390's own hand-picked default — is the *only* one of the six where the recoil actually tracks the beam's own propagation direction**; every other combination, including the off-axis default F390's own review used, pushes the fermion along a direction unrelated to either the beam's `k̂` or its polarization axis. F390's positive on-axis result was not a representative sample of a generally-working mechanism weakening at the edges; it was the one configuration, of six tested, where the (still not understood) underlying bias happens to coincide with the beam's own direction.

**A candidate mechanism, tested but not derived: the fermion's own fixed internal spin state.** `core.coupled.FermionEmChannel.init_state` seeds `g = np.zeros_like(f)` unconditionally — a definite, fixed chirality eigenstate, not a generic superposition — and the per-link step's hop-direction-dependent spinor rotations (`minimal_coupling.u1_link_weyl_step_3d_bcc`'s `M_mats`) couple to that internal state, not merely to the field's spatial direction. Measured (`axis=1, pol_axis=2`, otherwise default, both with the genuinely `Ĉ(k)`-transverse beam so §1's ruled-out mechanism cannot be responsible for any difference seen): replacing the default `f`-only eigenstate with an equal superposition (`f,g ← f/√2, f/√2`) changes the recoil vector from `[-0.0330, -0.0001, -0.0000]` to `[-0.0313, -0.0519, -0.0037]` — `cos` between the two is `0.517`, a large, unambiguous change in direction, not a small perturbation. **This shows the push genuinely depends on an internal degree of freedom the beam-construction fix cannot touch — supporting a spin-dependent (spin–orbit-type) coupling as the real candidate — but this finding does not derive the closed-form relationship between the fermion's spin state, the beam's axis/polarization, and the resulting push direction.** That derivation, or a systematic scan over spin states crossed with beam configurations, is left for a future session.

## 4. Consequence for `docs/claims/CL307`

CL307's own falsifier section names one specific route back toward `live`: "a derivation identifying and correcting the specific mechanism (the beam-polarization/`Ĉ(k)`-anisotropy mismatch...) that recovers the broad, axis-independent form." This finding tests exactly that route and finds it closed — the named mechanism, corrected by construction, recovers nothing. This is not itself a new falsifying observation against CL307's *current* (already-narrowed, on-axis-only) statement — the on-axis result is re-confirmed, not contradicted, by the new construction (§1's table) — but it does mean the specific "how to fix this" story CL307 pointed to is now known to be wrong, and the card is updated (§ its own file) to say so and to point at §3's spin-dependence candidate instead, without claiming that candidate as established.

## 5. Claim 4 (Thomson cross-section) — still out of reach, and now for a sharper reason

F390 §6 deferred the Thomson-limit cross-section citing three obstacles: no genuine far-field on a periodic/spectral lattice, ~27% norm loss on the projected beam, and no closing energy/momentum budget. This finding removes the second obstacle as stated (§1's construction loses none of the beam's norm to the `Ĉ(k)` projection) but does not thereby make the cross-section attainable, because **a fourth, more fundamental obstacle is now disclosed**: §3 shows the recoil this cross-section would need to normalize against depends on the fermion's own internal spin state, which F390's (and this finding's) harness sets once, by an unexamined default (`g≡0`), and which the roadmap never named as a physical input. A cross-section is a property of the *coupling*, not of one arbitrary initial condition; computing one now would silently be reporting a number that depends on a choice this finding has just shown is load-bearing and was never controlled for. The first and third obstacles (no far-field on this lattice; no closing energy/momentum budget, F390 §5) are unchanged and independently still block the calculation. **What would need to change:** a derivation (or, short of that, a systematic scan) establishing which spin state, if any, is the physically appropriate one for an "isotropic" or "unpolarized" incident-fermion cross-section, *and* a resolution of F390's own far-field and energy-budget gaps. Until then this stretch goal remains explicitly deferred, not attempted.

## 6. Test results

| Leg | Claim | Measured | Verdict |
|---|---|---|---|
| `beam_exactly_ck_transverse` | new beam: `‖iĈ·B‖<10⁻⁸` | `7.6×10⁻¹⁴` | PASS |
| `beam_near_zero_longitudinal_leak` | new beam: `Ĉ`-longitudinal fraction of `E` `<0.05` | `0.031` | PASS |
| `curl_y_axis_antiparallel_180deg` | `angle(Ĉ,k̂)=180°` on the y-axis | `180.000000°` | PASS |
| `curl_z_axis_parallel_0deg` | `angle(Ĉ,k̂)=0°` on the z-axis | `0.000000°` | PASS |
| `curl_y_axis_antiparallel_stable_with_L` | angle unchanged `L=64→128` | `180.0°` both | PASS |
| `onaxis_correlation_holds_with_both_beams` | F390's on-axis result survives the fix: `cos>0.9` for both constructions | `0.993` / `0.995` | PASS |
| `m4_sign_flip_persists_with_both_beams` | the `m_index=4` flip survives: `cos<-0.5` for both | `-0.987` / `-0.988` | PASS |
| `offaxis_decorrelation_persists_with_both_beams` | off-axis decorrelation survives: `\|cos\|<0.3` for both | `-0.002` / `-0.002` | PASS |
| `push_direction_sensitive_to_fermion_spin_state` | recoil vector changes direction with the fermion's own spin state: `cos<0.98` between two spin choices | `0.517` | PASS |

**Declared control:** `use_ck_beam=false` swaps the *original* F390 beam recipe in for every leg — measured, not assumed, to turn exactly `beam_exactly_ck_transverse` (`‖iĈ·B‖=72.9`) and `beam_near_zero_longitudinal_leak` (`0.275`, matching F390/F387's own disclosed number) red, while the other seven legs — which either measure `Ĉ(k)`'s own beam-independent structure or explicitly test *both* constructions side by side already — stay green (`7/9`).

## 7. Caveats

- **The `(axis,pol_axis)` grid in §3 is six points, not a systematic scan.** It is enough to falsify "recoil tracks the beam" as a general rule and to show confinement to the x–y plane across every combination tested, but a future session wanting the *general* rule (which combinations track what, and why z is never dominant) should scan more widely, including `m_index` and varying the fermion's `k0`/width, not just the six `(axis,pol)` pairs here.
- **The spin-sensitivity leg (§3, §6) tests exactly two spin states** (`f`-only, the equal-amplitude superposition) at one fixed beam configuration. It establishes that spin state matters, not how it matters — no closed-form or even a broader empirical map of push-direction vs. spin-state is attempted here.
- **The broader small-`k` closed form `Ĉ̂(k)≈Rk̂`, `R=\mathrm{diag}(1,-1,1)`, is reported for context (§2) and is not itself gated** beyond the two new axis-specific legs; a future session wanting a general-direction, gated version of this relation would need to define and verify a tolerance that scales with `|k|`, which this finding does not attempt (mirroring F387's own choice to gate only symmetric directions, §caveats there).
- **This finding does not identify why `(axis=x, pol=y)` specifically is the one combination (of six) that works** — no mechanism is offered for why this particular pairing avoids whatever bias produces the other five results; it is reported as an observed fact, not explained.
- Only the Weyl 2-spinor / U(1) sector and the specific `EmPhotonChannel`/`FermionEmChannel` construction (F388/F389) are covered, matching F384–F390's own scope.
- The `exactness` tag is not machine-precision throughout: the transversality legs (`beam_exactly_ck_transverse`, the two `curl_*` structural legs) are machine-precision (`≤8×10⁻¹⁴`, `L`-stable to `10⁻⁹`); the three `*_persists_with_both_beams` legs and the spin-sensitivity leg are threshold/comparison checks on a 20-tick dynamical run, the same `quantitative` class F390's own record used, and for the same reason — this is a genuinely dynamical, coupled-channel measurement, not a closed-form identity.

**Test record:** `F391-ck-transverse-beam-mechanism` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`, `expect.exactness: quantitative`). 9/9 legs PASS. One declared control (§6), verified can-fail.

**Claim:** none — this is an engine-capability/mechanism investigation (does a specific named beam-construction fix resolve F390's axis-dependence, and is the Thomson-cross-section stretch goal now well-posed), not itself a new claim against established Standard Model/QM/GR/SR physics; it updates the evidence and falsifier reasoning behind the existing `docs/claims/CL307` (§4) rather than issuing a new card, per D12's bar (a negative/redirecting result about *why* an existing claim's domain restriction holds, not a new assertion against established physics).

**Cross-references:** [[F390-photon-fermion-push-scenario]] (§3, §6 — the two gaps this finding investigates), [[F387-curl-anisotropy-omega-pair-mismatch]] (§1 — the direction-anisotropy table this finding extends to the y/z axes and whose named mismatch is ruled out as the breakdown's cause), [[F386-a-field-convention]] (§6 — where the beam-helper's Euclidean-`k̂` polarization convention was first flagged as an open item), [[F389-radiative-transverse-em-current]], [[F388-fermion-photon-coupled-channels]], [[F385-u1-link-covariant-step]] (the per-link step whose spin-dependent `M_mats` §3's candidate mechanism implicates).
