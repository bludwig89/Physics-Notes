# Remediation — F24: Weyl SL(2,ℂ) boost, Lorentz 4-current covariance

**Remediated:** 2026-08-04 - 14:50
**Against:** [independent review 2026-08-04](F24-review-2026-08-04.md) — verdict **CONFIRMED-NARROWER**
**Outcome:** 8 APPLIED · 0 PARTIAL · 0 REJECTED · 1 DEFERRED · 0 ESCALATED
**Gate:** test registry green (gate tier 45 → 46); `casim test --id F24-sl2c-covariance-full` PASS · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## What changed

The identity was never in doubt and reproduces bit-for-bit. What changed is the
*claim* around it and the *coverage* under it. The check ran **pure boosts only** —
and a pure boost is Hermitian, so $A^\dagger = A$ and the sandwich
$A^\dagger\bar\sigma^\mu A$ is structurally blind to the placement of the dagger,
which is the single most likely implementation error it exists to catch. Rotations
(unitary, $R^\dagger = R^{-1}$) and boost∘rotation compositions are now in, and the
quoted residual has been replaced by a worst case: $3.71\times10^{-16}$ was a benign
12-draw sample, and the honest number is $1.11\times10^{-13}$ at $\zeta\approx-6.9$,
limited by **conditioning on the null cone**, not by machine epsilon.

This is the only finding in the F20–F25 block whose remediation needed no escalation.

## Ledger

| # | Source | Item | Kind | Disposition | Evidence |
|---|---|---|---|---|---|
| 1 | A12, Rec 4 | Boost-only coverage cannot distinguish $A$ from $A^\dagger$ | module · test | **APPLIED** | New `sl2c_rotation()`; `sl2c_covariance_full()` covers boosts, rotations and compositions. Worst rel: boost $1.114\times10^{-13}$, rotation $5.850\times10^{-16}$, composition $4.187\times10^{-14}$ |
| 2 | A4, Rec 3 | $3.71\times10^{-16}$ presented as "the IEEE-754 floor" | claim | **APPLIED** | Replaced by a 2000-draw worst case. `legacy_sample_is_optimistic` **asserts** the worst case exceeds the legacy value by $>100\times$, so the claim cannot drift back |
| 3 | A10, Rec 2 | Sign convention omitted from `## Statement` | doc | **APPLIED** | $\Lambda^{0i} = -\sinh\zeta\,\hat v^i$ stated, with the measured consequence: **49.63** relative residual against the standard active $\Lambda(+\zeta)$ versus $2.090\times10^{-15}$ against $\Lambda(-\zeta)$. The module docstring was always right; the finding was not |
| 4 | A1/A10, Rec 1 | "This closes the Lorentz-covariance loop at the spinor level" | claim | **APPLIED** | `## Significance` rewritten: it is a convention/regression check of a definitional identity, with the covering-map argument spelled out and the nullity ($8.7\times10^{-16}$) recorded |
| 5 | A1, Rec 1 | No statement that the result has **no lattice content** | claim | **APPLIED** | Stated outright, together with what the load-bearing question actually is |
| 6 | A7/A8, Rec 5 | Rode on a six-finding battery `result_dump` with `has_assert: false` | test | **APPLIED** | Gate record `F24-sl2c-covariance-full`, `kind: assertion`, `expect: {exactness: machine, tol: 1e-10}`; `tests/findings/test_F24_sl2c_covariance.py` **6/6**; `casim test --id` PASS (0.3 s) |
| 7 | A11, Rec 6 | Prior art uncited | citation | **APPLIED** | `## Prior art`: Peskin & Schroeder §3.2, Srednicki ch. 34–35, Weinberg vol. I §2.7, Wess & Bagger app. A, plus two public write-ups |
| 8 | A9, Rec 8 | Pre-C9 `ca_maxwell.py` citation | doc | **APPLIED** | Repointed to `casim.engine.gauge.bilinear` |
| 9 | Rec 7 | The (1,0) contamination analysis is buried and F302 did not cite it | doc | **APPLIED** | New `## The part of this finding that was under-titled`, cross-linking F302 |
| 10 | A1 (the real gap) | Does the lattice **evolution** commute with a boost at finite $a$? | physics | **DEFERRED** | Landing site: `docs/roadmaps/next-steps.md`, with the measurement specified (boost-then-evolve vs evolve-then-boost, order in $ka$, comparison to the F15/F22 $\beta_\text{LV}$ coefficients) |

## Confirmed by the review — and now stated

- **The identity is exact and was independently re-derived at the operator level**,
  $A^\dagger\bar\sigma^\mu A = \Lambda^\mu{}_\nu\bar\sigma^\nu$ as $2\times2$
  matrices — stronger than the bilinear form F24 states, and it holds for every
  $\psi$ with no conditions. The finding now says so.
- **The implementation is correct.** `weyl_sl2c_4current_covariance()` returns
  3.707420040408194e-16, reproduced bit-for-bit.
- **Free inputs: none, as claimed.** Attacks 2, 5 and 6 all passed. F24 is the only
  finding in this block with a clean input count *and* a pre-existing test record.
- **F24 anticipated F302 by two months.** Its representation-theory section derives
  the $(0,0)$ scalar contamination of the transpose bilinear $\psi^T\sigma\psi$ and
  places it in the $(1,0)$ irrep — the same conclusion F302 reached independently on
  2026-08-03 by the $U^T\epsilon U = \det(U)\epsilon$ route, without citing F24.
  That is the finding's real contribution and its title does not mention it.

## Rejected recommendations

None.

## Physics and code changed

| File | Change | Why | Verified by |
|---|---|---|---|
| `src/casim/engine/gauge/bilinear.py` | New `sl2c_rotation`, `_four_current`, `_lorentz_boost_matrix`, `_so3_rotation_matrix`, `sl2c_covariance_full`; artifact write guarded behind `__main__` **and** `CASIM_F24=1` | Rotation branch was the untested one; worst case replaces a benign sample | 6/6 pytest; record PASS |
| `tests/registry/gauge.yaml` | Gate record `F24-sl2c-covariance-full` | D9 | `check_test_registry` green, gate 46 |
| `tests/findings/test_F24_sl2c_covariance.py` | New, 6 tests | pytest face | 6 passed |
| `findings/F24-…md` | Sign convention, `## Significance` rewritten, `## Prior art`, `## Corrections`, the under-titled section, `## Status` | Step 6 | — |
| `docs/roadmaps/next-steps.md` | The deferred lattice-boost-commutator item | A deferral without a landing site is a silent drop | — |

## Exactness movement

| Result | Was | Now | Cause |
|---|---|---|---|
| SL(2,ℂ) → SO(1,3) on the 4-current | machine, $3.71\times10^{-16}$, boosts only | **machine**, $1.11\times10^{-13}$ worst case over boosts + rotations + compositions | Correct estimator and full subgroup coverage |
| "closes the Lorentz-covariance loop" | asserted | **withdrawn** — a convention/regression check | The map is the definition of the covering map |

No class changed. The number got *larger* and the claim got *smaller*, which is what
a correct worst-case estimator and an honest label look like.

## Still open

**DEFERRED (1).** Whether the lattice **evolution** commutes with a Lorentz boost at
finite $a$. Nothing in F24 bears on it: the identity is continuum $2\times2$ spinor
algebra with no $a$, no $c_\text{lat}$, no BCC geometry, no dispersion and no CA
tick. It would generically **not** be exact — the Brillouin zone and finite $a$ break
boosts — so the interesting quantity is the order in $ka$ at which the commutator
fails, and whether that matches the F15/F22 $\beta_\text{LV}$ coefficients. Landed in
`docs/roadmaps/next-steps.md`.

**Not escalated, deliberately.** The reviewer's explicit view, adopted here: F24 does
**not** belong in `S1-F69-sigma-bilinear-photon` alongside F20, F21 and F23. It lives
in the same module, but the object it studies —the Hermitian 4-current
$\psi^\dagger\bar\sigma^\mu\psi$ — is not the retired transpose bilinear, and F24 is
the file that first explained why the transpose one fails.

## Method notes

- The rotation branch is not decoration. `test_F24_rotation_matrix_is_unitary_not_hermitian`
  asserts $R^\dagger R = I$ *and* $R^\dagger \neq R$, which is the structural reason
  the boost-only test was blind. Without that assertion the new coverage would look
  like more of the same.
- The tolerance $10^{-10}$ is derived from the $e^{2\zeta}\epsilon$ growth on the
  null cone at $\zeta_\text{scale} = 2$, not read off the residual. The measured
  worst case sits three orders under it, which is the margin that growth law implies.
- **Not verified:** whether `run_FC06_cpt_lorentz.py`'s F24 block is the same code
  path as `weyl_sl2c_4current_covariance()`. The function was called directly to
  avoid the runner writing `test-results/FC06_cpt_lorentz.json` into the repo. The
  old battery record is left in place and untouched.
- **Least sure:** whether item 4 should also have narrowed the finding's *title*.
  "Weyl SL(2,ℂ) Boost: Lorentz 4-Current Covariance" is accurate as far as it goes,
  and the review did not ask for a re-title — but the finding's most valuable content
  is the $(1,0)$ contamination analysis, which the title does not mention.
