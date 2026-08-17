# Remediation — F21: curl residual geometry independence — superseded per Ben (was held at the Step-3 gate)

**Remediated:** 2026-08-04 - 15:50 — superseded by F306; see `## RESOLVED` at the foot of this file.
**Against:** [independent review 2026-08-04](F21-review-2026-08-04.md) — verdict **REFUTED**
**Outcome:** 0 APPLIED · 0 PARTIAL · 0 REJECTED · 0 DEFERRED · **14 ESCALATED**
**Gate:** unchanged (no edit made) · **Claim:** `gracious-jolly-meitner`, numbers 306–310, used none

## Why this file exists and why it changes nothing

`remediate-finding` Step 3 stops before *any* edit when the verdict is `REFUTED` or
`CIRCULAR`, or when the fix would touch `supersessions.yaml` or a canonical
decision. F21's remediation trips **all three**. So this file is the escalation
package: the ledger, the independent verification of the reviewer's central claim,
and the three options — with nothing applied.

**No file was edited under this remediation.** The only F21 write set so far is the
review report and one `**Reviewed:**` line, both from the review run.

## Independent verification of the reviewer's central claim

The reviewer's finding is severe enough that it was re-checked in this session
directly, not taken on report. Three measurements, on the BCC walk at
$\hat k \propto (1,0.4,0.7)$, using the shipped `bilinear.EM_bilinears` and
`bilinear.bilinear_G`:

**1. $E_G$ and $B_G$ are exactly real.**

| $k$ | $\max\lvert\mathrm{Im}\,E\rvert$ | $\max\lvert\mathrm{Im}\,B\rvert$ |
|---|---|---|
| $10^{-1}\ldots10^{-4}$ | **0.0** (exactly) | **0.0** (exactly) |

The residual's right-hand side, `1j*cross(two_n, B)`, is therefore pure imaginary
and orthogonal to the left-hand side in $\mathbb C^3$ by construction.

**2. The two sides have equal magnitude at every $k$.**

| $k$ | $\lVert\text{LHS}\rVert/\lVert\text{RHS}\rVert$ | $R_\text{F21}/\lvert k\rvert$ | $c_\text{lat}/\sqrt2$ |
|---|---|---|---|
| $10^{-1}$ | 1.0000000000 | 0.406617118358 | 0.408248290464 |
| $10^{-2}$ | 1.0000000000 | 0.408091850796 | 0.408248290464 |
| $10^{-3}$ | 1.0000000010 | 0.408232713999 | 0.408248290464 |
| $10^{-4}$ | 0.9999998583 | 0.408246704545 | 0.408248290464 |

So $\lVert\text{LHS}-\text{RHS}\rVert = \sqrt2\lVert\text{RHS}\rVert$ identically,
and $R \to c_\text{lat}/\sqrt2$ follows from nothing but $c_\text{lat}\equiv
d\Omega/d\lvert k\rvert$ and the $\sqrt2$ of quadrature addition.

**3. Merely dropping the `1j` does *not* fix it — the analytic-signal
identification does.** This is worth recording because it is the obvious first fix
and it fails:

| fix attempted | $R/\lvert k\rvert$ at $k=10^{-4}$ |
|---|---|
| drop the `1j`, RHS $= 2n\times B$ | 0.4082408 — **unchanged** |
| drop the `1j`, RHS $= -2n\times B$ | 0.4082526 — **unchanged** |
| analytic amplitudes $\hat E = g$, $\hat B = \hat n\times g$ | see below — **collapses** |

With $\hat E = g$, $\hat B = \hat n\times g$ (complex amplitudes rather than the
real $2\,\mathrm{Re}\,g$, $2\,\mathrm{Im}\,g$):

| $k$ | $R_\text{analytic}$, $\Delta t{=}1$ | $c^2k/4$ | $R_\text{analytic}$, exact $\partial_t$ | $c^3k^2/48$ |
|---|---|---|---|---|
| $10^{-1}$ | $8.267729\times10^{-3}$ | $8.333333\times10^{-3}$ | $3.962984\times10^{-5}$ | $4.009377\times10^{-5}$ |
| $10^{-2}$ | $8.326957\times10^{-4}$ | $8.333333\times10^{-4}$ | $4.004778\times10^{-7}$ | $4.009377\times10^{-7}$ |
| $10^{-3}$ | $8.332698\times10^{-5}$ | $8.333333\times10^{-5}$ | $4.295633\times10^{-9}$ | $4.009377\times10^{-9}$ |
| $10^{-4}$ | $8.333368\times10^{-6}$ | $8.333333\times10^{-6}$ | float64 cancellation floor | $4.009377\times10^{-11}$ |

Algebraically, with $2\lvert n\rvert = 2\sin(\Omega/2)$ and $\hat n\times(\hat n\times\hat E) = -\hat E$:

$$\bigl(e^{-i\Omega}-1\bigr) + 2i\sin\tfrac\Omega2
 = 2i\sin\tfrac\Omega2\bigl(1-e^{-i\Omega/2}\bigr),
\qquad \bigl\lvert\cdot\bigr\rvert = 4\sin\tfrac\Omega2\sin\tfrac\Omega4 \simeq \tfrac{\Omega^2}{2},$$

giving $R \simeq \Omega^2/(4\lvert k\rvert) = c_\text{lat}^2\lvert k\rvert/4$; and
replacing the one-tick difference by the exact derivative $-i\Omega$ leaves
$\lvert\Omega - 2\sin(\Omega/2)\rvert \simeq \Omega^3/24$, giving
$R \simeq c_\text{lat}^3 k^2/48$. **Both closed forms confirmed to 3–4 digits.**

**Conclusion of the verification: the reviewer is right.** The un-smeared pointwise
bilinear satisfies the lattice curl equation to $O(k^3)$ — the criterion recorded
at `references/qca-papers-1-4-overview.md:407` — once $E_G,B_G$ are read as
analytic amplitudes rather than as real vectors. F21's central claim, that the
$O(k)$ failure is "intrinsic to the un-smeared pointwise bilinear", does not hold.

## Ledger — every item PROPOSED, none applied

| # | Source | Item | Kind | Severity | Disposition |
|---|---|---|---|---|---|
| 1 | Verdict | REFUTED — the finding's conclusion is false, its arithmetic is not | physics | verdict-changing | **ESCALATED** |
| 2 | Rec 1 | Fix the residual definition in `bilinear.py::maxwell_curl_residual` and the fork harness; re-measure | module | verdict-changing | **ESCALATED** |
| 3 | Rec 2 | Withdraw exactness-inventory **#49**; revert **#7** to its pre-F21 wording | claim | verdict-changing | **ESCALATED** |
| 4 | Rec 3 | Withdraw Interpretation §2, §4 and the "Geometry is ruled out" verdict; propagate to `project-status.md:812` and `ca-reference.md:709` | claim | verdict-changing | **ESCALATED** |
| 5 | Rec 4 | Re-open Finding 2's hypothesis #3 (operator-algebra vs c-number bilinear) | physics | verdict-changing | **ESCALATED** |
| 6 | Rec 5 | Re-examine F23 — its baseline self-check is F21's constant | physics | verdict-changing | **ESCALATED** (and F23 is next in this session's queue) |
| 7 | Rec 6 / A9 | Add F21 and F23 to `supersessions.yaml` under `S1-F69-sigma-bilinear-photon` | citation | class-changing | **ESCALATED** — supersessions edit |
| 8 | Rec 7 / A12 | Three of five geometry rows have no module and no artifact | test | class-changing | **ESCALATED** — the table may not survive item 2 |
| 9 | Rec 8 / A8 | No registry record; the three fork modules unlinked to F21 in `registry.py` | test | class-changing | **ESCALATED** — a record written now would assert the refuted number |
| 10 | Rec 9 / A2 | Stale pre-C9 paths; F21:76 "both $+$helicity" contradicts `harness.py:58`; `bilinear.py:521-527` comment contradicts line 515 | doc | cosmetic | **ESCALATED** (would otherwise be autonomous — held only because Step 3 forbids editing the file at all) |
| 11 | Rec 10 / A12 | Doubler claim is a Brillouin-zone convention; BCC symbol has period $2\pi\sqrt3$ | claim | class-changing | **ESCALATED** |
| 12 | Rec 11 / A10 | Configuration qualifier sits in a caveat, not in the boxed equation | claim | cosmetic | **ESCALATED** |
| 13 | A4 | "rel err $4.6\times10^{-7}$ — harness faithful" is the F245 anisotropy $\beta k$, not a fidelity number | claim | class-changing | **ESCALATED** |
| 14 | A11 | F245 independently derived the same object 8 weeks later without citing F21 | citation | cosmetic | **ESCALATED** |

## What is salvageable

This matters for choosing between the options, and the review is explicit about it:

- **Every number in F21 is correct.** Both agents reproduced the harness
  bit-for-bit; the BCC value is $0.40824847879427933$ against the recorded
  $0.40824848$. The finding was never wrong about what it measured.
- **The closed form is a genuine, and stronger, result.**
  $R = \sqrt2\sin(\Omega/2)/\lvert k\rvert$ is exact at all $k$ for the whole walk
  class, and the ratio to $c_\text{lat}$ is exact to 42 digits at 60 dps, against
  the six figures claimed. Whatever happens to the interpretation, that algebra
  survives.
- **The three lemmas survive and are reusable.** $G_T$ is a complex null vector
  ($G_T\cdot G_T = 0$) whenever $\psi$ is a helicity eigenstate — hence
  $E\perp B$, $\lVert E\rVert = \lVert B\rVert$ exactly, and
  $\hat n\times B = \mp E$. That is a clean structural result about the bilinear
  and it is not in the finding.
- **Attack 7 passed.** The perturbation behaves exactly as the closed form
  predicts across six geometry variants and two spec readings.
- **The doubler observation is real, just mis-scoped.** Cubic *does* have 8
  doublers on $[-\pi,\pi)^3$; the defect is that BCC's 1 is measured on 19% of its
  own fundamental cell.

## The three options

**Option A — repair.** Keep F21, rewrite it around the corrected residual. The
title becomes the positive result: *the un-smeared pointwise bilinear satisfies the
lattice curl law to $O(k^3)$ with coefficient $c_\text{lat}^3/48$; the previously
reported $O(k)$ failure was a real-vs-imaginary representation mismatch.* Keep the
closed form and the three lemmas as the finding's core.
*Costs:* `bilinear.py` changes (a live module, with unknown downstream consumers);
inventory #49 withdrawn and #7 reverted; `project-status.md` and `ca-reference.md`
rewritten. *Destroys:* nothing that is true.

**Option B — supersede.** Banner F21, write a `supersessions.yaml` entry, and put
the corrected physics in a successor finding (F306 is held and unspent). F21 stays
readable as the record of what was believed, with its numbers intact.
*Costs:* one finding number; the ledger entry; the same inventory and status edits.
*Destroys:* nothing. *Advantage:* the append-only history is cleanest, and F23's
re-examination can cite the successor rather than a corrected-in-place F21.

**Option C — retire.** Move F21 to `deprecated/findings/` as F16–F19 were.
*Costs:* finding number 21 becomes a declared gap; F23's and F25's citations all
need repointing. *Destroys:* the closed form and the three lemmas, unless they are
rescued into a successor first — so this is really Option B with the original
deleted, and there is no reason to prefer it.

**Recommendation: Option B.** The defect is at the root (the residual's definition,
not its measurement), which is the review's own criterion for supersession rather
than repair. And the salvage is substantial and clean — a closed form, three
lemmas, and a corrected $O(k^3)$ result — which is exactly what a successor finding
is for. Option A would leave a finding whose title, boxed equation and verdict all
had to be inverted in place, which is the outcome the append-only rule exists to
prevent.

**One thing to decide with it:** whether `bilinear.py::maxwell_curl_residual` is
changed or left alone with a banner. Changing it alters a live module whose other
consumers were not surveyed in this run; leaving it means the repo keeps a function
that measures a convention. The review recommends changing it; this session did not
check what else calls it.

## Still open

Everything. Nothing was applied.

**Immediate knock-on:** F23 ("smearing is ruled out; the $c_\text{lat}/\sqrt2$
coefficient is algebraically phase-locked") is next in this session's review queue
and is built on F21's constant as its baseline self-check. Its review will be run
independently, but the outcome here strongly conditions it — a rule-out of a fix to
a non-problem is not a rule-out of anything. F25 ("real-rotation formula holds to
machine precision; Maxwell curl holds only to $O(k)$") is in the same family and
carries the same $O(k)$ premise in its title.

## Method notes

- The verification above was run in this session against the shipped modules; it is
  not a re-report of the referee's numbers. The one place it *disagrees* with the
  referee's framing: the referee offered "drop the `1j` and use the real-field curl"
  as an equivalent fix to the analytic-signal identification. **It is not** — both
  sign choices leave $R/\lvert k\rvert = 0.408$ unchanged. Only the analytic-signal
  identification collapses the residual. Anyone acting on recommendation 1 should
  know that, or they will conclude the diagnosis is wrong.
- Not checked: what else in the tree calls `maxwell_curl_residual` or depends on the
  real-valued $E_G,B_G$ convention. That survey is a prerequisite for Option A.
- Not checked: Bisio et al. Eq. 35 in the original. arXiv was unreachable from the
  sandbox for both agents. The attribution of *why* the mismatch exists (operator
  adjoint vs `np.conj` on a c-number) rests on the repo's own transcription. The
  numerical result does not depend on it.


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
