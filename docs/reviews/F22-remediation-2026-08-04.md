# Remediation — F22: QCA velocity addition from the arccos dispersion

**Remediated:** 2026-08-04 - 09:15
**Against:** [independent review 2026-08-04](F22-review-2026-08-04.md) — verdict **OVERSTATED**
**Outcome:** 9 APPLIED · 1 APPLIED-PARTIAL · 0 REJECTED · 1 DEFERRED · 2 ESCALATED
**Gate:** module/test registries and indexes green; full `make gate` not seen end-to-end (sandbox ceiling) · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## What changed

The single fix that mattered was to a *check*, not to the physics: F22's headline
"sympy bit-zero" verification of $\rho = 1-2\beta_\text{LV}$ could not fail. It
wrote `beta_LV_sym = (1 − rho)/2` and then simplified `rho − (1 − 2·beta_LV_sym)`,
which is $x-(1-2(1-x)/2)\equiv0$ for any expression — the referee obtained residual
0 from a deliberately wrong $\rho$, and then from $\rho = 42$. It is now checked
against the Finding-15 module's own closed form, with $\rho$ taken from a sympy
limit of the dispersion, and with a **negative control asserted to go red**. The
same record measures the $O(vk)$ coefficient by which F22's claim 1 fails, so the
false claim now has a number attached instead of being asserted away.

## Ledger

| # | Source | Item | Kind | Disposition | Evidence / landing site |
|---|---|---|---|---|---|
| 1 | A1/A4, Rec 3 | The $\rho = 1-2\beta_\text{LV}$ check is a definitional tautology | test | **APPLIED** | `check_rho_identity()` — left side a sympy limit of $\omega=\arccos(n\cos(ka))$, right side `derive_beta_LV.beta_LV` (itself gated by `F15-closed-form-lv-coefficients`). Negative control asserted: `rho_override="42"` ⇒ `symbolic_identity: False`, `numeric_identity: False` |
| 2 | A1 | The `acos(√(1−m²)) = asin(m)` step sympy will not close | test | **APPLIED** | Asserted separately at 50 dps over 199 points; residual $6.7\times10^{-50}$. Both halves can fail |
| 3 | A7/A8, Rec 4 | No test record; the one F22-tagged record is mass-insensitive | test | **APPLIED** | New gate record `F22-rho-identity-and-offshell`, `expect: {exactness: exact, tol: 0}`; `tests/findings/test_F22_rho_identity.py` **10/10**; `casim test --id` PASS (1.1 s). Gate tier 44 → 45 |
| 4 | A8 | Module registered `dead_candidate`, `findings: []`; `code-index.md` attributed it to F15 | module | **APPLIED** | `Module("interactions.derive_velocity_addition", …, findings=("F15","F22"), exactness="exact", status="live")` in `_SPINE`, mirroring how F15's own module was promoted. `check_module_registry` green, 189 modules |
| 5 | Rec 1 | Claim 1 is false; publish the $O(vk)$ coefficient as the real result | physics | **APPLIED-PARTIAL** | `offshell_boost_coefficient()` measures it — $-0.0930513$ vs predicted $1/\rho-1 = -0.0931003$ at $m{=}0.5$, rel $5.3\times10^{-4}$ — and the test asserts it is **nonzero**, i.e. asserts the failure. **Retracting claim 1 from the headline is ESCALATED** |
| 6 | Rec 2 | "Deformed velocity addition" is a misnomer | claim | **ESCALATED** | Flagged in the finding with the corrected statement ($E^2-c^2P^2=m^2$, undeformed Einstein composition, non-closed domain); the headline retraction is Ben's |
| 7 | Rec 3 | Inventory rows 45/46/47 are identities, not exactness | claim | **ESCALATED** | Row 46's checked expression has `free_symbols = {u,v,ρ}` — the dispersion never enters. Tied to items 5 and 6 |
| 8 | A11, Rec 5 | Prior art uncited | citation | **APPLIED** | New `## Prior art`: arXiv:1310.6760 (EPL 101, 60005, 2013) and arXiv:1503.01017 (Phil. Trans. R. Soc. A 374, 2016). "Derived here" retained, "novel" withdrawn |
| 9 | A12, Rec 6 | 2D-square / $k_y{=}0$ qualifier dropped downstream | claim | **APPLIED** | `**Scope:**` line in the header; `project-status.md` entry rewritten |
| 10 | A10, Rec 6 | Scope creep into `project-status.md` | claim | **APPLIED** | That entry now leads with the correction and states what survives and what does not |
| 11 | A12 | $\rho$ runs at finite $k$; $u_p$ superluminal for $ka>\pi/2$; $\rho\to\infty$ as $m\to1$ | doc | **APPLIED** | All three stated in the Summary and in `## Corrections` |
| 12 | A9, Rec 7 | Pre-C9 path `ca-simulation/derive_velocity_addition.py` | doc | **APPLIED** | Repointed to `casim.engine.interactions.derive_velocity_addition` |
| 13 | A6/A13, Rec 7 | No falsifier, and no statement that the sector is untestable | claim | **APPLIED** | New `## Falsifiability` with three thresholds **and** the honest limitation: the effect vanishes for photons so GRB bounds are structurally inapplicable, and the massive-sector coefficient sits $\sim5\times10^{-41}$ of muon-time-dilation sensitivity |
| 14 | A2 | F22 absent from `papers/Claims-and-Falsifiers-Summary.md` | claim | **DEFERRED** | Adding it should follow the escalated retraction, not precede it — otherwise the register gains a claim that is about to change. Landing site: this ledger row and the escalation below |
| 15 | A12 | Does any of this survive on BCC? | physics | **DEFERRED** | Stated as open in `## Status`. The BCC form has no obvious analogue of $\sin^2\omega - n^2\sin^2u = m^2$ and no code path exists |

## Confirmed by the review — and now stated

- **$\rho(m) = \tan\theta/\theta = 1-2\beta_\text{LV}$ was re-derived independently**,
  from F15's *definition* rather than its stated closed form, at sympy zero — with
  $\gamma_\text{LV} = \tfrac18 - \tfrac1\theta(\tfrac T8+\tfrac{T^3}{24})$ as a free
  cross-check that also matched. The finding did not say the identity had ever been
  checked against anything independent; now it has been, and the check that exists
  in code reflects that.
- **Attack 5 passed.** $\rho$ is forced by the arccos dispersion, not fitted; no
  look-elsewhere freedom. This is the finding's genuine content.
- **The free-input count is correct** — one ($m$), zero fitted, with
  $a = c_\text{lat}$ cancelling identically because $\omega$ depends on $k$ only
  through $u=ka$. That is the one axis F22 was already right about, and it is worth
  saying so given how much else moved.

## Rejected recommendations

None. Every recommendation was either applied, escalated, or deferred with a
landing site.

## Physics and code changed

| File | Change | Why | Verified by |
|---|---|---|---|
| `src/casim/engine/interactions/derive_velocity_addition.py` | Tautological check removed with an explanatory note; new `check_rho_identity`, `offshell_boost_coefficient`, `check_offshell_and_control`; `__main__` writes the artifact | The check could not fail; claim 1's failure had no number | 10/10 pytest; negative control red |
| `src/casim/engine/registry.py` | Module promoted to `_SPINE`, `dead_candidate → live`, `findings=(F15,F22)` | It was attributed to F15 only, which is how F22 had no coverage | `check_module_registry` green |
| `tests/registry/interactions.yaml` | New gate record | D9 | `check_test_registry` green, gate 45 |
| `tests/findings/test_F22_rho_identity.py` | New, 10 tests incl. the negative control and the off-shell assertions | pytest face | 10 passed |
| `findings/F22-…md` | Scope line, banner, claims 1 and 3 struck through with the measured refutation, `## Prior art`, `## Corrections`, `## Falsifiability`, `## Status` | Step 6 | — |
| `docs/status/project-status.md` | Entry rewritten to lead with the correction | Scope creep | documentary |

## Exactness movement

| Result | Was | Now | Cause |
|---|---|---|---|
| $\rho = 1-2\beta_\text{LV}$ | Tier-1 exact on a tautological check | **exact**, on a check with a negative control | The class is unchanged; the *evidence* is what moved |
| Boost exact on $(\omega,k)$ | Tier-1 exact | **false**, $O(vk)$ with coefficient $1/\rho-1$ | Escalated for formal retraction |
| $\delta u'$ closed form | Tier-1 exact | **misnamed**; misses the lattice by $10^2$–$10^3\times$ | Escalated |
| $O(vk)$ off-shell coefficient | did not exist | **machine**, rel $5.3\times10^{-4}$ vs closed form | New |

## Still open

**ESCALATED (2).**

1. **Retract claims 1 and 3 from F22's headline** and re-title the finding. Claim 1
   goes from EXACT to *false*; claim 3 from "deformed formula" to "the composition
   law is undeformed Einstein addition in the nonlinear variables". This moves a
   headline claim by more than two exactness classes, which is Step-3 territory.
   The corrected physics is already written into the finding's `## Corrections` and
   measured in the gate record — only the headline and the title are held.
2. **Dispose of exactness-inventory rows 45, 46 and 47.** Rows 46 and 47 are
   identities whose checked expressions never touch the dispersion. They should be
   deleted or moved out of Tier 1, which is tied to decision 1.

**DEFERRED (2).** Adding F22 to `papers/Claims-and-Falsifiers-Summary.md` (should
follow the retraction, not precede it); and whether any of this survives on the
canonical BCC lattice.

## Method notes

- **The repaired check was itself checked.** It is not enough to rewrite a
  tautology into something that returns 0; the test asserts that the *same* code
  path returns non-zero under `rho_override="42"`. Without that assertion there
  would be no evidence the repair worked.
- **Where sympy would not cooperate.** The limit returns
  $m/(\sqrt{1-m^2}\arccos\sqrt{1-m^2})$ while F15 writes
  $m/(\sqrt{1-m^2}\arcsin m)$. `simplify` leaves $\arcsin(\sin t)$ and
  $\arccos\lvert\cos t\rvert$ standing without a domain assumption, and substituting
  $m=\sin t$ does not help for the same reason. Rather than force it, the
  $\arccos\sqrt{1-m^2}=\arcsin m$ lemma is asserted numerically at 50 dps over the
  open interval and then applied — so the weak step is visible and gated rather
  than hidden inside a `simplify`.
- **Not verified:** whether the deformed map $(E,P)$ is unique; anything off the
  $k_y=0$ axis; the Bailey and Vasileiou sensitivity numbers, which came from the
  review and were not re-sourced.
- **Least sure:** whether item 5 should have been fully APPLIED rather than
  APPLIED-PARTIAL. The physics is measured, tested and written down; only the
  headline sentence is held. A reader who stops at the title still sees the old
  claim, struck through — which is the append-only rule working, but it is also a
  half-corrected finding until Ben rules.
