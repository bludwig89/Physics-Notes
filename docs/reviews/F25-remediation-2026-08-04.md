# Remediation — F25: real-rotation exact / discrete-time Maxwell — superseded per Ben (was held at the Step-3 gate)

**Remediated:** 2026-08-04 - 15:50 — superseded by F306; see `## RESOLVED` at the foot of this file.
**Against:** [independent review 2026-08-04](F25-review-2026-08-04.md) — verdict **OVERSTATED**
**Outcome:** 0 APPLIED · 0 REJECTED · 0 DEFERRED · **9 ESCALATED**
**Gate:** unchanged (no edit made) · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## Why this is held

Same reason as F23, one link further down the chain. F25 inherits the
$c_\text{lat}/\sqrt2$ coefficient from F21 (**REFUTED**) and F23 (**OVERSTATED**),
shares `exactness-inventory.md:526` row 3 with F23, and would need a
`supersessions.yaml` entry alongside F20, F21 and F23. Every one of those is Step-3
territory, and remediating F25 before Ben rules on the family would mean rewriting it
twice.

## Ledger — every item PROPOSED, none applied

| # | Source | Item | Kind | Severity | Disposition |
|---|---|---|---|---|---|
| 1 | Rec 1 | `## Physical interpretation` item 3 — "Maxwell is the $\Delta t\to0$ limit" — is false | physics | verdict-changing | **ESCALATED** |
| 2 | Rec 1 | item 4 — "the $O(k)$ residual is a prediction, not a failure… the leading Planck-scale signature" — is false | physics | verdict-changing | **ESCALATED** |
| 3 | Rec 2 | `exactness-inventory.md:526` row 3 records both as settled | claim | verdict-changing | **ESCALATED** (shared with F23 — fix once) |
| 4 | Rec 3 | Publish the positive result: analytic amplitudes close the curl law at $O(k^3)$, coefficient $c_\text{lat}^3/48$, reducing to $\omega = \sin\omega$ | physics | verdict-changing | **ESCALATED** — this is the successor finding, and a finding number is Ben's call |
| 5 | Rec 4 / A1,A3 | P1 is an identity, presented in `## Results` as a prediction beating Maxwell "by 5 orders of magnitude" | claim | class-changing | **ESCALATED** |
| 6 | Rec 5 | Unresolved working note left in the published text ("Wait — … Let me expand carefully:") | doc | cosmetic | **ESCALATED** (would otherwise be autonomous; held only because Step 3 forbids editing the file) |
| 7 | Rec 6 | `## What is not changed by this assumption` is three-quarters stale | citation | class-changing | **ESCALATED** |
| 8 | Rec 7 / A9 | Absent from `supersessions.yaml`; cites F17 (deprecated), F21 (REFUTED), F23 (OVERSTATED); pre-C9 paths | citation | class-changing | **ESCALATED** |
| 9 | Rec 8,9 / A12,A13 | Pairing and branch undeclared and untested; item 5's falsifier names no experiment | test · claim | class-changing | **ESCALATED** |

## What is salvageable

More than in any other finding in this block:

- **Every number in F25 is correct**, and its own derivation section is *honest*
  about P1 being an identity ("no small-$k$ approximation required"). The defect is
  the framing around it, not the algebra.
- **F25 has 6 test records** — by far the best coverage of F20–F25, which have 0, 0,
  1 (mass-insensitive), 0 and 1 respectively. The infrastructure is there; it is
  pointed at a claim that cannot fail.
- **F25 is one substitution from the right answer.** Reading $E,B$ as analytic
  amplitudes rather than as the $2\mathrm{Re}/2\mathrm{Im}$ quadrature pair collapses
  the curl equation to $\omega(k/2) = \sin\omega(k/2)$ and closes it at $O(k^3)$ with
  coefficient $c_\text{lat}^3/48 = 1/(144\sqrt3)$. **That coefficient was reached
  three separate times in this review series** — by the F21 referee, by this
  session's own verification, and by F25's blind agent via
  $\Omega - 2\lvert n\rvert = k^3/(72\sqrt3)$ — and all three agree.
- **The real-rotation law itself is exactly right**, including its handedness (the
  transpose arrangement is wrong by $2\sin\Omega$, checked).

## The successor finding this block wants

If Ben authorises it, one finding replaces the broken interpretation across F21, F23
and F25 at once:

> The σ-bilinear composite field satisfies the lattice Maxwell curl equation to
> $O(k^3)$ with coefficient $c_\text{lat}^3/48$. The previously reported $O(k)$
> failure was a representation mismatch: $E_G = 2\lvert n\rvert\mathrm{Re}\,G_T$ and
> $B_G = 2\lvert n\rvert\mathrm{Im}\,G_T$ are the time-quadrature pair of one
> circularly polarised amplitude, with $B = \hat n\times E$ exactly, so
> $\partial_t E \parallel B$ while $\nabla\times B \parallel -E$ — orthogonal at every
> $\Delta t$ and for any smearing. Read as analytic amplitudes the whole discrepancy
> reduces to $\omega = \sin\omega$. Geometry (F21), smearing (F23) and discrete time
> (F23/F25) were never the variable.

Numbers 306–310 are held by this session and unspent.

## Method notes

- The decisive checks were run in this session against the shipped modules:
  $\cos(B,\hat n\times E) = 1.0000000000$;
  $\lVert\Omega B\rVert/\lVert2n\times B\rVert = 1.0000000137$ at $k=10^{-3}$;
  residual 0.4082469 / 0.4082468 / 0.4082469 at $\Delta t = 10^{-3}$, $10^{-6}$ and
  exact; analytic-amplitude residual matching $k^2/(144\sqrt3)$ across three decades.
- The review is **hybrid mode** — cold blind agent, inline referee — and the inline
  half had already seen the F21 and F23 reviews. That is why the $\Delta t$ claim was
  settled by measurement rather than by argument.
- Not chased: whether the $72$ in $k^2/72$ is the same $72$ as the constants
  registry's $1/(72\pi)$. The repo's own rule is that values which coincide stay
  separate constants, so this needs a deliberate check rather than an assumption.


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
