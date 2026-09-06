---
id: CL294
title: 'The Dirac CP phase inherits F254''s $T_{2g}$ no-go: $D_{2h}$ transports a complex amplitude by sign alone, so no residual symmetry fixes any $T_{2g}$ phase either'
slug: 'delta-cp-inherits-the-t2g-no-go'
tier: supporting
kind: no_go
status: open
domain: [cosmology]
exactness: exact
findings: [F353]
tests: [F353-delta-cp-t2g-inheritance]
modules: [casim.engine.particles.derive_delta_cp_t2g, casim.engine.particles.majorana]
constants: []
supersessions: []
reviews: [docs/reviews/F353-review-2026-09-03.md]
rolls_up_to: CL223
falsifier: unset
first_issued: '2026-09-03'
last_verified: '2026-09-03'
provenance: authored
review_state: unreviewed-seed
confidence: medium
---

# CL294 — The Dirac CP phase inherits F254's $T_{2g}$ no-go

## Statement

The $D_{2h}$ stabiliser that F254 showed acts on the (real) $T_{2g}$ triplet as three inequivalent
1-d irreps acts on a **complex** $T_{2g}$ entry by the identical real sign $s_as_b$ — a real
orthogonal similarity transform can only flip a complex number's overall sign, never rotate its
phase. So F254's no-go (no residual symmetry relates the three amplitudes; the F92 equipartition
selector cannot apply, no degenerate multiplet) transfers verbatim from the magnitudes to the
phases of $(t_{xy},t_{yz},t_{zx})$, and hence to the Dirac CP phase $\delta_{CP}$ built from them
via the standard Jarlskog invariant. Confirmed numerically: F254's own real NuFIT-fit magnitudes
give $J=0$ exactly (a consequence of choosing real inputs, not a protected value), while
independent phases on top of those same magnitudes populate a continuous, generic, unprotected
range of $J$ (1000 draws, none returning to zero), and the phase-democratic point is equally
unprotected. Ledger parameter #26: $\mathrm{ABSENT}\to\mathrm{EXCLUDED}$.

## What it extends

Rolls up to **CL223** (F254's own card, "no lattice selector for the PMNS $T_{2g}$ channel"):
CL223 established the no-go for the mixing-angle content of $T_{2g}$; this card establishes that
the identical group-theoretic mechanism (not a new one) covers the phase content too, closing the
open question CL223 itself left standing in F254 §6's table ("Dirac CP phase: Free (needs complex
$T_{2g}$ — a 4th input; unchanged)"). Like CL223, this is a **negative/no-go** result relative to
the external rubric this project tracks (`docs/status/completeness-2026-08-20.md` parameter #26) —
it is not a derivation of the SM's $\delta_{CP}$ value, but a proof that no lattice selector for it
exists among residual-symmetry / equipartition mechanisms, sharpening "unaddressed" (`ABSENT`) into
a named theorem (`EXCLUDED`).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F353-delta-cp-t2g-inheritance.md` | The finding, in full | exact (T1) / numerical (T2–T4) |
| `tests/findings/test_F353_delta_cp_t2g_inheritance.py` | 6/6 PASS, `test-results/F353_delta_cp_t2g_inheritance.json` | machine-verified |
| `findings/F254-t2g-pmns-selector-nogo.md` | The magnitude-sector no-go this card extends | exact / numerical (as CL223) |

## Falsifier

**Not yet stated.** `falsifier: unset` is declared debt (as CL223's own card notes for itself).
Informally: a future finding that identifies a *dynamical* (not residual-symmetry) mechanism
fixing the $T_{2g}$ phases — e.g. from a UV completion of the condensate not yet built — would not
contradict this card (it only excludes *symmetry-selector* mechanisms), but would make the
"genuinely free" framing incomplete rather than wrong.

## Status & history

`open`, from the finding's own `**Status:**` line, quoted verbatim:

> Formal confirmation of a stated working hypothesis, plus two bonus repo-hygiene fixes — 6/6 PASS
> (`test_F353_delta_cp_t2g_inheritance.py`, ~30 s). **What is proven (exact / group-theoretic, T1):**
> the $D_{2h}$ stabiliser F254 built (F93 O3) acts on a $T_{2g}$ entry $t_{ab}$ by the real sign
> $s_a s_b$ **whether $t_{ab}$ is real or complex**... **Verdict:** $\delta_{CP}$ is genuinely free
> by the **same mechanism** F254 proved for the mixing angles... Ledger parameter **#26**:
> $\mathrm{ABSENT}\to\mathrm{EXCLUDED}$, matching rows #23–25's own grading exactly.

**Date:** 2026-09-03 - 00:40. Authored the same session as the finding (not a blind mechanical
extraction — see the finding §6 for the inline self-review this session ran on its own work, which
is why `review_state` is still `unreviewed-seed`: an inline review is not an independent
third-party pass in the sense `docs/claims/README.md` requires for `authored`).

## Sources

- `findings/F353-delta-cp-t2g-inheritance.md`
- `findings/F254-t2g-pmns-selector-nogo.md`
- `docs/claims/CL223-no-lattice-selector-for-the-pmns-channel-the.md`
- `docs/reviews/F353-review-2026-09-03.md`
