# F393 — The missing `curl(grad φ)=0` gate leg for `bcc_curl_symbol`, gated honestly as a known defect

*2026-09-16 - 01:45 · sector `gauge` · module `casim.engine.gauge.charge_coupling` (new `check_curl_grad_identity_diagnostic`) · test record `F393-curl-grad-identity-diagnostic` (assertion, gate tier, 7/7 legs PASS) · results `test-results/F393_curl_grad_identity_diagnostic.json`*

**Status:** Confirmed — 7/7 legs PASS, one declared control verified red on exactly 5 of 7 legs.

**Reviewed:** 2026-09-16 — **CONFIRMED** ([independent review](../docs/reviews/F393-review-2026-09-16.md))

**Target.** Part B of `docs/roadmaps/photon-fermion-coupling-rerun-prompt.md`. `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` §3.2/§3.3 found that discrete exterior calculus gives *two* identities from `d∘d=0`, and only one of them was ever gated:

- `div(curl A) = 0`, i.e. `C·(C×x) ≡ 0` — **vacuous**: true for *any* vector field `C` whatsoever, a property of the cross product, not of `C`. This is exactly what the model's existing no-monopole gate (`i\hat C\cdot B\approx0$, F387/F388/F389) tests, and why it has stayed green throughout: it carries no information about whether `bcc_curl_symbol` is a genuine curl.
- `curl(grad φ) = 0`, i.e. `C×G = 0`, which requires `C ∥ G` — **the one that actually constrains `C`**, and it was never tested anywhere in the codebase before this finding.

**The answer.** `bcc_curl_symbol` fails the second identity maximally: `|C×G|/(|C||G|)` averages `0.7417` against the spectral gradient `G=k` and `0.7072` against the forward-difference gradient `G_j=e^{ik_j}-1$ — on average, "the curl of a gradient" is 74% of its maximum possible magnitude, not the `0` a genuine curl gives identically. This finding adds the missing gate leg. **It does not change `bcc_curl_symbol`** — per the rerun-prompt's own instruction, deciding whether/how to repair it (Part C, a discrete-exterior-calculus complex on the BCC lattice) is a separate, larger decision, made in a follow-up finding of this same session or deferred to a later one. This finding's whole job is to make the defect visible and permanently monitored rather than an untested assumption.

---

## 1. Verification against the real modules

`tools/verify_photon_momentum_diagnosis.py`'s `defect_2()` was run unmodified against the real `casim.engine.gauge.charge_coupling.bcc_curl_symbol` before any code was touched (see [[F392-beam-polarization-null-fix]] §1 for the full re-verification pass covering both Part A and Part B's numbers in one run). Every number reproduced exactly: `cos(C,k)` ranging the full `[-1,+1]` with `3864` of `4088` nonzero modes below `0.99`; the `R=\mathrm{diag}(1,-1,1)` reflection angles on the cubic axis/face diagonal/body diagonal; the `0.7417`/`0.7072` mean ratios; and the exact `±1`/`∓1` on-axis reflection facts. No discrepancy found.

## 2. Test results

| Leg | Claim (the **measured**, defective value — not a target) | Measured | Verdict |
|---|---|---|---|
| `matches_known_defect_spectral_max` | `\|C\times k\|/(\|C\|\|k\|)` max `=1.000000` | `1.000000` | PASS |
| `matches_known_defect_spectral_mean` | same, mean `=0.741692` | `0.741692` | PASS |
| `matches_known_defect_forward_diff_max` | `\|C\times G\|/(\|C\|\|G\|)`, `G_j=e^{ik_j}-1`, max `=1.000000` | `1.000000` | PASS |
| `matches_known_defect_forward_diff_mean` | same, mean `=0.707173` | `0.707173` | PASS |
| `onaxis_reflection_x_plus_one` | `\hat C(k)\cdot\hat k=+1$ on the x-axis, `m=1,2,3,4` | `+1.000000000` at every `m` | PASS |
| `onaxis_reflection_y_minus_one` | `\hat C(k)\cdot\hat k=-1$ on the y-axis, `m=1,2,3,4` | `-1.000000000` at every `m` | PASS |
| `onaxis_reflection_z_plus_one` | `\hat C(k)\cdot\hat k=+1$ on the z-axis, `m=1,2,3,4` | `+1.000000000` at every `m` | PASS |

**Declared control** (`curl_symbol: 'true'`, i.e. substitute a genuine curl generator `C=k` for `bcc_curl_symbol`): `C×k≡0` trivially (any vector is parallel to itself), so the two spectral-gradient legs collapse to exactly `0.0`, far from the measured defect values, and the y-axis reflection vanishes (`\hat C\cdot\hat k=+1$ on every axis for a real curl, not `-1` on y). The forward-diff legs also redden (`0.509` mean, not `0.707173`) for a disclosed, different reason (§3). The x/z on-axis legs stay green because `\hat C=+\hat k$ there for *both* symbols (`bcc_curl_symbol`'s own reflection `R` is the identity on x and z). Measured, not assumed, to redden exactly 5 of 7 legs. `can-fail` verified.

## 3. A caveat on the control's forward-difference legs

The control's `forward_diff` legs redden not because a genuine curl symbol fails `curl(grad)=0` against the forward-difference gradient (it wouldn't, given its *own* consistent forward-difference gradient), but because the control substitutes a **spectral** `C=k` while the comparison gradient is the *mismatched* forward-difference `G_j=e^{ik_j}-1$ — two different discretizations of "gradient," which are only proportional in the `k\to0$ limit. A spectral curl compared against a forward-difference gradient is not expected to give exactly zero even when the curl itself is genuine; it is expected to differ from `bcc_curl_symbol`'s own specific defect number, which it does (`0.509` vs `0.707173`). This is disclosed so a future reader does not mistake the forward-diff legs' redness under control as evidence that the *identity itself* fails for a true curl — only that this particular numerical comparison is discretization-sensitive, a fact orthogonal to whether `C` is a genuine curl generator.

## 4. Why this was not caught in ~300 prior findings

Both `d∘d=0` identities are logically independent consequences of the same fact (the boundary of a boundary is empty) in a genuine discrete-exterior-calculus complex, where they hold identically by construction — but `bcc_curl_symbol` is not built from such a complex; it is built from `_bcc_uvec(k/2)`'s `n^+`, the fermion walk's own spin-quantisation axis (F387 §1), reused as a Maxwell curl generator. Reuse does not inherit either identity automatically. The vacuous one (`div∘curl=0`) happens to hold for *any* vector field, so it gave a false sense of verification for 300+ findings; the real one was simply never written down as a test until this finding.

## 5. What this does and does not close

This adds the missing diagnostic to the gate tier, permanently monitored from now on. It does **not** repair `bcc_curl_symbol` — every existing consumer (`solve_A_coulomb_3d`, `magnetostatic_B`, `maxwell_curl_step`, `em_current.conserved_current`, and F384/F386/F387/F388/F389/F390/F391's own gate records) is untouched, bit-for-bit. Whether and how to build a genuine discrete-exterior-calculus curl on the BCC lattice (Part C of the rerun prompt) is decided separately — see [[F394-bcc-dec-curl-part-c-decision]] (this session's Part C finding) for that decision and why it was, or was not, carried out this session.

## 6. Caveats

- **A CLI-reproducibility bug was found by the independent review and fixed, not merely disclosed.** `casim.tests.registry.parse_param` coerces a bare `--param curl_symbol=true` token to the Python bool `True` before it reaches `check_curl_grad_identity_diagnostic`, which originally accepted only the strings `"bcc"`/`"true"` — so the exact command this finding's own test driver documented for manually reproducing the control raised `ValueError` instead of running it. The registry's own YAML control was unaffected (it quotes the string, `curl_symbol: 'true'`, so the gate tier itself always ran correctly), but a human typing the documented command by hand could not reproduce it. Fixed by accepting the bool aliases (`True→"true"`, `False→"bcc"`) inside the function itself, rather than touching the shared `parse_param` (which many unrelated records also depend on). Re-verified: the control (`casim test --id F393-curl-grad-identity-diagnostic --control`) and the default record both still pass identically after the fix.
- **The asserted values are a regression baseline against a known defect, not a correctness target.** If `bcc_curl_symbol` is ever replaced (Part C) or repaired in place (explicitly not done by any finding in this chain — the rerun prompt forbids it), this leg's numbers should change, and that change would be the expected, desired outcome, not a red flag. A future session replacing the symbol should either retire this leg or repoint it at the new symbol's own (hopefully `0`) measured value.
- **The forward-difference comparison is a secondary, discretization-sensitive diagnostic**, not a strict test of the identity in its own right (§3) — the spectral comparison (`G=k`, the same convention `bcc_curl_symbol` itself is built in) is the primary, cleanest test of the two.
- **Only `L=16` is exercised.** The on-axis reflection facts are already established elsewhere (F387/F391) to be `L`-stable continuum-limit properties, not finite-lattice artifacts, and are not re-verified at multiple `L` here — this finding gates the fact at the one lattice size the rest of this chain's gate records use.
- Only the U(1)/EM sector's curl generator is examined; the non-Abelian curl generators (W/Z/gluon, still on the σ-bilinear construction) are out of scope, matching F387's own scope note.

**Test record:** `F393-curl-grad-identity-diagnostic` (`tests/registry/gauge.yaml`, kind `assertion`, tier `gate`, `expect.exactness: quantitative` — an honestly-scoped defect-monitoring check, not a round-off-floor identity). 7/7 legs PASS. One declared control, verified red on exactly 5 of 7 legs. `can-fail` verified.

**Claim:** none — this is a test-infrastructure addition (a previously-missing diagnostic gate leg for an existing engine construction), not itself a claim against established Standard Model/QM/GR/SR physics; no `docs/claims/` card is issued per D12's bar.

**Cross-references:** [[F392-beam-polarization-null-fix]] (Part A, verified together with this finding's numbers in one re-run of the audit's own diagnosis script), [[F387-curl-anisotropy-omega-pair-mismatch]] (the direction-anisotropy and reflection facts this finding gates for the first time), [[F384-conserved-bcc-em-current]], [[F386-a-field-convention]], [[F87-charge-coupling-paired-photon]] (whose `MX1` magnitude-only check this finding's own legs do not duplicate or contradict — squaring removes the sign, F387 §1).
