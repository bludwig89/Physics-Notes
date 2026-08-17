# Remediation — F23: smearing ruled out / phase-locked coefficient — superseded per Ben (was held at the Step-3 gate)

**Remediated:** 2026-08-04 - 15:50 — superseded by F306; see `## RESOLVED` at the foot of this file.
**Against:** [independent review 2026-08-04](F23-review-2026-08-04.md) — verdict **OVERSTATED**
**Outcome:** 0 APPLIED · 0 REJECTED · 0 DEFERRED · **9 ESCALATED**
**Gate:** unchanged (no edit made) · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## Why this is held rather than executed

The verdict is `OVERSTATED`, which is normally autonomous. It is held anyway,
because every substantive item trips Step 3 by a different route:

1. **It is the same decision as F21's.** F23 self-checks against F21's hard-coded
   constant, cites F21 as its baseline, and its whole question exists because of
   F21's framing. F21 is graded **REFUTED** and held at the gate. Remediating F23
   first would fix the downstream file against an upstream claim Ben has not yet
   ruled on — and if he chooses *supersede* for F21, F23's corrected text would
   have to be rewritten a second time.
2. **The fix corrects `docs/status/exactness-inventory.md:526` row 3**, which
   records the $\Delta t \to 0$ claim as settled and cites F23 **and F25** for it.
   That row is shared with a finding this session has not yet reviewed.
3. **It wants a `supersessions.yaml` entry**, alongside the F20 and F21 entries
   already escalated. That is explicitly Step-3 territory.
4. **F25 is not yet reviewed** and is the other citation on that inventory row.
   Its review is next in the queue; acting on F23 before it lands risks a third
   pass over the same paragraph.

## Ledger — every item PROPOSED, none applied

| # | Source | Item | Kind | Severity | Disposition |
|---|---|---|---|---|---|
| 1 | Verdict / Rec 1 | `## Root cause` and `## Next fork` are false: $\Delta t\to0$ does not resolve the lock | physics | verdict-changing | **ESCALATED** |
| 2 | Rec 2 | `exactness-inventory.md:526` row 3 records the $\Delta t\to0$ claim as settled | claim | verdict-changing | **ESCALATED** (shared with F25) |
| 3 | Rec 3 / A13 | Replace the leading-order argument with the blind agent's theorem ($R=0 \Rightarrow B\equiv0$, any weighting) | physics | class-changing | **ESCALATED** |
| 4 | A5 / Rec 4 | The $c_\text{lat}$ factor is attributed to a "3D average over random directions"; the limit is direction-independent | physics | class-changing | **ESCALATED** |
| 5 | A12 / Rec 5 | Fixed-$\sigma$ and fixed-$\delta$ rows have negative slopes — no $k\to0$ limit — but their coefficients are quoted as limits and compared as "150×"/"241×" | claim | class-changing | **ESCALATED** |
| 6 | A7 / Rec 6 | Shell $\beta=2$ gives 0.3637 (0.079–0.202 per direction), contradicting the literal headline; the normaliser explanation must travel with it | claim | verdict-changing | **ESCALATED** |
| 7 | A1 / Rec 7 | The self-check compares against F21's hard-coded `BASELINE_COEFF` from the same code path | test | class-changing | **ESCALATED** — the replacement target is F21's disposition |
| 8 | A8/A9 / Rec 8 | No test record; harness `fork_unclaimed`/`unreferenced` with empty findings; absent from `supersessions.yaml`; pre-C9 path | test · citation | cosmetic | **ESCALATED** — a record written now would assert numbers that may be withdrawn |
| 9 | A11 / Rec 9 | Paper 1's $f_k(q)$ is a bosonic-statistics device, so "smearing ruled out" is not a result about Paper 1 | doc | cosmetic | **ESCALATED** (would otherwise be autonomous; held only because Step 3 forbids editing the file) |

## What is salvageable

Substantial, and more than F21's:

- **F23 got the mechanism right first.** It identified the real-vs-imaginary phase
  structure on 2026-05-23; the F21 review reached the same conclusion independently
  on 2026-08-04. Whatever happens to the causal story, that diagnosis is F23's and
  it is correct.
- **The negative result survives in substance.** No smearing closes the residual at
  $O(k^3)$. The blind agent confirmed it across all three families and proved the
  stronger statement.
- **The finding named the right hypothesis.** H3 (discrete-time vs continuous-time
  / operator ordering) is the correct diagnosis; F23 promoted it to primary
  candidate. It attached the wrong mechanism to it, but the name was right.
- **The harness is clean where F21's text is not** — it uses the opposite-helicity
  pairing and 8 random directions, so it never samples the $\hat n_y = 0$ surface
  where the residual is $0/0$. No reported digit is round-off.

## The decision Ben faces

This is **not** a separate decision from F21's. Recommended handling:

**Bundle F20, F21, F23 and F25 into one disposition.** All four rest on the σ-bilinear
composite photon; all four are absent from `S1-F69-sigma-bilinear-photon`; F17 and
F18 were already added to that entry and deprecated on 2026-08-03. The natural shape
is one ledger entry covering the family, with per-finding LIVE/DEAD text:

- **F20** — items 1–2 (Weyl/Dirac propagation) LIVE and now at machine precision;
  item 3 (composite photon) DEAD.
- **F21** — the closed form and the three lemmas LIVE; the $O(k)$ interpretation and
  "geometry is ruled out" DEAD.
- **F23** — the phase-lock diagnosis and the smearing negative LIVE; the
  finite-$\Delta t$ root cause DEAD.
- **F25** — pending review.

and one successor finding carrying the corrected physics: *the σ-bilinear satisfies
the lattice curl law at $O(k^3)$ with coefficient $c_\text{lat}^3/48$ once $E_G,B_G$
are read as analytic amplitudes; the reported $O(k)$ failure was a representation
mismatch; smearing was never the variable.* Finding numbers 306–310 are held by this
session and unspent.

## Method notes

- The decisive measurement — $\Delta t$-independence of the residual at $1$,
  $10^{-3}$, $10^{-6}$ and for the exact derivative — was run in this session
  against the shipped `bilinear` module, not inherited from an agent.
- The review itself is **hybrid mode**: the blind re-derivation was cold and
  complete, the adversarial referee pass was inline after a session limit killed the
  cold run. The inline half had already seen the F21 review, so it was not cold on
  the central question. That weakens the referee rows, not the blind half, and the
  central falsification is a measurement rather than a judgement.


---

## RESOLVED 2026-08-04 - 15:50 — Ben authorised "supersede + successor"

The Step-3 gate is cleared. Ben chose **option B (supersede + successor)** for the
F21/F23/F25 family and **"survey first"** for `bilinear.py`. Both were executed:

**The survey** (which decided the code question). `maxwell_curl_residual` has four
consumers — `tests/runners/run_L_tests.py:231`,
`bilinear_2d.maxwell_curl_residual_2d`, and the F21 and F23 fork harnesses.
`EM_bilinears` has far more, including `test_su2_photon_bridge.py` and
`test_FG6_two_helicity_photon.py` and about a dozen internal uses. So **nothing was
changed**: `maxwell_curl_residual` is bit-for-bit as it was, and the corrected
reading is a **sibling** function, `maxwell_curl_residual_analytic`. Migrating the
four consumers is deliberately left open.

**What landed.**

| Item | Where |
|---|---|
| Successor finding | `findings/F306-curl-closes-at-k3-representation-artifact.md` |
| Ledger entry | `S18-curl-residual-representation-artifact` in `docs/theory/supersessions.yaml`, with per-finding LIVE/DEAD text for F20, F21, F23, F25 |
| Gate record | `F306-curl-closes-at-k3` — runs **both** readings on the same fields at the same $k$; that comparison is the test |
| Code | `maxwell_curl_residual_analytic`, `check_curl_closes_at_k3` (sibling functions; the original untouched) |
| Banner | on this finding's header |
| Exactness inventory | row 3 corrected; Tier-1 #7 and #49 **withdrawn**; #51 reclassified as an identity; Tier-2 #15 annotated |

**The measurement that settles it**, both readings, same fields, same $k$:

| $k$ | original (real pair) | analytic amplitudes | closed form $c_\text{lat}^3k^2/48$ |
|---|---|---|---|
| $10^{-1}$ | 0.4100532 | $4.0643\times10^{-5}$ | $4.0094\times10^{-5}$ |
| $10^{-2}$ | 0.4084358 | $4.0149\times10^{-7}$ | $4.0094\times10^{-7}$ |
| $10^{-3}$ | 0.4082671 | $4.3648\times10^{-9}$ | $4.0094\times10^{-9}$ |

Flat versus falling by a factor of 9312. Everything above in this file that reads
as pending is now disposed.
