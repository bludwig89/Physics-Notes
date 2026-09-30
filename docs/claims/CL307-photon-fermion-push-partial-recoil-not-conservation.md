---
id: CL307
title: 'For a photon beam propagating along a lattice-cubic axis at small carrier wavenumber, a photon-fermion push in the model recoils the fermion along the beam''s own direction and the field''s and matter''s momentum changes are nearly anti-parallel, but total momentum is not conserved exactly at any coupling tested, and both the direction and anti-alignment results invert or vanish off-axis'
slug: photon-fermion-push-partial-recoil-not-conservation
tier: supporting
kind: deviation
status: narrowed
domain: [SR, QFT]
exactness: quantitative
findings: [F390, F389, F388, F385, F387, F391, F392, F395]
tests: [F390-photon-fermion-push, F391-ck-transverse-beam-mechanism, F392-beam-polarization-null-fix, F395-stage5-circular-beam-rerun]
modules: [casim.engine.core.photon_fermion_push, casim.engine.core.coupled, casim.engine.gauge.em_photon_sourcing, casim.engine.gauge.photon]
constants: []
supersessions: []
reviews: [docs/reviews/F390-review-2026-09-15.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-15'
last_verified: '2026-09-16'
provenance: authored
review_state: authored
confidence: low
---

# CL307 — A photon-fermion push recoils correctly in direction, not in conserved momentum — and only for beams along a lattice-cubic axis

## Statement

When a genuine, `Ĉ(k)`-transverse photon beam propagating **along a lattice-cubic axis, at small carrier wavenumber** (`m_index≤3` at `L=16`) pushes a localized Weyl fermion at rest via this model's per-link U(1) covariant step (F385), the fermion's momentum shift aligns with the beam's own wavevector (`cos≈0.98–0.995` in that regime), and the field's and matter's momentum changes are measured nearly anti-parallel (`cos≈-0.989`). **Neither result generalizes.** Total momentum is not conserved exactly at any coupling strength tested regardless of axis. Outside the narrow on-axis/small-`m_index` domain — a beam along a different Cartesian axis, or the same axis at only twice the carrier wavenumber (`m_index=4`) — the direction correlation collapses to `cos≈0` or reverses sign entirely, and the anti-parallel result **inverts to near-exactly parallel** (`cos≈+0.99995`). This card was narrowed to this domain-restricted form at first issue, after an independent review found the broader, axis-unrestricted form asserted in a draft of the underlying finding to be factually false.

## What it extends

The classical-electrodynamics/special-relativistic expectation that a closed, gauge-invariant matter+field system conserves total momentum exactly (a Noether consequence of translation invariance acting on one covariant action), and the more basic expectation that a photon's push on a charge is along the photon's own direction of travel, robust to the photon's propagation direction. This model's coupled fermion↔photon construction gets the second right only in a narrow geometric regime and never achieves the first; this card documents both facts precisely, including where they hold and where they demonstrably do not.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F390-photon-fermion-push-scenario.md` §2-3 | On-axis: direction `cos=0.995`, anti-alignment `cos=-0.989`, conservation residual `17%` at best-measured coupling. Off-axis (`axis=1`): direction `cos=-0.0019` (no correlation), anti-alignment **inverted** to `cos=+0.99995`. On-axis at `m_index=4`: direction **inverted** to `cos=-0.988` | quantitative |
| `docs/reviews/F390-review-2026-09-15.md` | Independently reproduced every number above via a blind re-derivation and an adversarial referee pass, both against the real code, not a reimplementation | quantitative |
| `findings/F389-radiative-transverse-em-current.md` §4 | The structural mechanism: matter recoil `O(g_lat)`, field momentum `O(g_lat²)` in the self-sourced-only case — the root cause F390 confirms extends (with a linear, not quadratic, scaling once a beam dominates) to a beam-driven case | quantitative |
| `findings/F387-curl-anisotropy-omega-pair-mismatch.md` §1 | The axis-asymmetric sign in the lattice's own curl generator, `Ĉ(k)→(k_x,-k_y,k_z)/|k|` — real and exact, but **ruled out as the breakdown's mechanism** by F391 (next row): a beam built to be genuinely `Ĉ(k)`-transverse reproduces the identical breakdown | exact (cited structural fact; causal role ruled out) |
| `findings/F391-ck-transverse-beam-mechanism.md` | **Tested the F387 mechanism directly and found it not responsible**: a beam-construction helper polarized exactly against `Ĉ(k)` (zero longitudinal leak, vs. F390's own 27.5%) reproduces the on-axis correlation, the `m_index=4` sign flip, and the off-axis decorrelation to 3-4 significant figures. Also found the recoil direction is sensitive to the fermion's own fixed internal spin state (`cos=0.517` between two spin choices at fixed beam config) — a candidate mechanism, not derived — and sharpened F387's own table: `Ĉ(k)` is exactly *anti-parallel* to `k̂` along the lattice's y-axis (`180°`), not merely anisotropic | quantitative (breakdown persistence); machine (new `Ĉ(k)` axis facts) |
| `tests/registry/core.yaml` `F390-photon-fermion-push`; `tests/registry/gauge.yaml` `F391-ck-transverse-beam-mechanism` | 8/8 and 9/9 gate legs PASS respectively (F390's two legs added specifically to gate the axis breakdown; F391's legs confirm the breakdown persists under the ruled-out-mechanism's fix), each with independently-verified controls | machine (registration) / quantitative (physics) |

## Claim 1 (momentum conservation), restated as of F395

`docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` §6.2 found that F390's original beam (`E∥B` pointwise, `Σ E×B≡0` identically — a construction defect, `findings/F392-beam-polarization-null-fix.md`) means F390's own claim-1 residual (`17%`) was never comparing a genuine momentum exchange in the first place, and, independent of that defect, that the roadmap's claim 1 (`ΔP_matter+ΔP_field≈0` for a continuum-style `P`) **cannot be made exact by any scheme on a lattice** — discrete translation symmetry conserves only crystal momentum, modulo reciprocal-lattice vectors. `findings/F395-stage5-circular-beam-rerun.md` re-ran Stage 5 against the fixed beam and confirms this: claim 1 as originally written is **withdrawn as unachievable**, replaced by three measured targets —

- **(A) exact charge conservation** — **not delivered** by casim's actual bridged architecture (the fermion's own norm drifts `0.54%` over the scenario's 20 ticks under F385's per-link step, bounded but genuinely nonzero); the audit's "delivered outright" language described its own single-action *prototype*, not anything running in this repo today.
- **(B) exact crystal-momentum translation covariance**, `Φ∘T=T∘Φ` — **delivered**, measured to `1.5×10⁻¹⁵`.
- **(C) matched-order approach to the continuum** — **still mismatched** (doubling `g_lat`: matter `×0.994`, field `×2.036`), for a more specific reason than F389's original diagnosis: the matter push in a beam-driven scenario is dominated by a coupling-*independent* term (F388 §2's unconditional per-link push), so its flat doubling ratio is not evidence of anything matching.

## Falsifier

**Already triggered once, in the direction the card now reflects.** This card's first version (issued the same day) claimed the direction and anti-alignment results held broadly, with a stated falsifier of "a wider parameter sweep finding the anti-alignment breaks down badly." The independent review ran exactly that sweep during the same review cycle and found not just a breakdown but a sign inversion — the card was narrowed in response, in the same pass, rather than left standing on a falsified premise. **One proposed route back toward `live` has since been tried and closed**: this card originally named "a derivation identifying and correcting the specific mechanism (the beam-polarization/`Ĉ(k)`-anisotropy mismatch...) that recovers the broad, axis-independent form" as the way to strengthen the card. F391 built and tested exactly that fix and found it changes nothing — the mismatch was real but not causal. Going forward, this narrowed card's own falsifier: finding that the direction/anti-alignment results *also* fail within the stated domain (on-axis, `m_index≤3`, at other lattice sizes `L`) would remove even the narrow positive claim; conversely, a derivation of F391 §3's spin-dependence candidate that both explains the on-axis success and recovers a broader domain would strengthen this card back toward `live` — no such derivation exists yet.

## Status & history

**Narrowed at issue, in two stages within the same day.** The card was first drafted with the broader, axis-unrestricted statement (direction confirmed generally, anti-alignment "robust across every perturbation swept"). Before this card or its underlying finding were considered complete, the mandatory independent review (`docs/reviews/F390-review-2026-09-15.md`) tested the one dimension the draft's own disclosed sweep had never varied — beam propagation axis — and found the broad claim false: the anti-alignment result inverts sign entirely for an off-axis beam, and the direction correlation itself reverses at `m_index=4`. This card was rewritten to the domain-restricted form above in the same pass, per this project's standing rule that a finding's own review-driven fixes are applied before, not after, the record is treated as settled. `confidence` is set to `low` (down from an initial `medium`) reflecting that the mechanism behind even the narrowed, on-axis claim is measured, not derived (see Falsifier), and that the domain restriction itself was found empirically rather than predicted.

**2026-09-16 update (`findings/F391-ck-transverse-beam-mechanism.md`):** the specific mechanism this card's Evidence table had named as "likely" — the beam-construction helper's Euclidean-`k̂` polarization mismatched against `Ĉ(k)` — was built, fixed, and re-tested directly. The fix changes nothing: the on-axis correlation, the `m_index=4` sign flip, and the off-axis decorrelation all persist unchanged under a beam that is genuinely `Ĉ(k)`-transverse by construction (zero longitudinal leak, vs. the original's 27.5%). The named mechanism is real (F387's `Ĉ(k)` axis anisotropy is confirmed and even sharpened — `Ĉ(k)` is exactly *anti-parallel* to `k̂` on the lattice's y-axis) but not causal for this breakdown. This does not change the card's `status` or narrowed domain (the on-axis result is re-confirmed, not contradicted) but it does close the specific falsifier route this card had pointed to, and redirects the open question toward a new, untested candidate (F391 §3: the fermion's own fixed internal spin state) — `confidence` remains `low`.

**2026-09-16 update (`findings/F392-beam-polarization-null-fix.md`, `findings/F395-stage5-circular-beam-rerun.md`):** a *second*, independent beam-construction defect was found and fixed — F390's original beam had `E∥B` pointwise (zero Poynting momentum by construction, orthogonal to F391's `Ĉ(k)`-transversality fix, which kept a linear-type polarization). Re-running Stage 5 against the genuinely null (circular-polarization) fix: the on-axis direction result is re-confirmed (`cos=0.994`, matching F390/F391 to 3 significant figures) and the `m_index=4` anomaly persists (`cos=-0.949`, still sign-reversed) — a *third* independent beam-construction fix that does not touch it, further reinforcing F391 §3's matter-side (spin-state) candidate. **But the off-axis result genuinely changes in kind**, unlike under F391's fix: at a 20-tick snapshot, `axis=1` moves from `cos≈-0.002` (F390 and F391, both linear-type beams, at every tick count they checked) to a nonzero, positive value under circular polarization; `axis=2` moves to a nonzero, negative value. Polarization convention (linear vs. circular), not only transversality convention (`k̂` vs. `Ĉ(k)`), is therefore part of the off-axis picture — a genuinely new, unpredicted qualitative result, not yet explained. **Correction (independent review, `docs/reviews/F395-review-2026-09-16.md`):** F395's first version quoted specific point values (`cos=+0.328`/`-0.101`) as if settled; a tick-count sweep (`10,20,30,40`) shows neither has converged — `axis=1`'s value drifts non-monotonically down to `0.160` by tick 40 (below the gate leg's own reproducibility threshold), and `axis=2`'s value changes sign between tick 30 and 40. The qualitative claim (circular polarization changes the off-axis result relative to either linear-type fix, robust across coupling strengths) stands; the specific numbers do not, and this card no longer cites them as fixed values. The card's narrowed domain and `low` confidence are unchanged; claim 1 is separately restated above, per the audit's own crystal-momentum argument, independent of either beam fix.

## Sources

- `findings/F395-stage5-circular-beam-rerun.md`
- `findings/F392-beam-polarization-null-fix.md`
- `findings/F391-ck-transverse-beam-mechanism.md`
- `findings/F390-photon-fermion-push-scenario.md`
- `docs/reviews/F390-review-2026-09-15.md`
- `findings/F389-radiative-transverse-em-current.md`
- `findings/F388-fermion-photon-coupled-channels.md`
- `findings/F387-curl-anisotropy-omega-pair-mismatch.md`
- `findings/F385-u1-link-covariant-step.md`
- `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md`
- `docs/roadmaps/photon-fermion-coupling.md` (Stage 5 claims 1 and 2)
- `docs/roadmaps/photon-fermion-coupling-rerun-prompt.md`
