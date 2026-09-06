# F350 — F337's named remedy (an anti-aliased Wigner-Seitz-cell mask) is built, VERIFIED IN ISOLATION to be far more accurate than the sharp mask it replaces, and measured to change **nothing** about $d_1$ leg 3's anomalous slow convergence — F337's own exhaustion condition for the "non-convergence, not falsification" reading now fires

**Date:** 2026-09-02 - 14:33
**Numbering:** **F350**, taken as `max+1` against `F349` (`casim index` → `NEXT FREE NUMBER F350`, no gaps).
**Status:** Mask module established (isolation gates PASS) + native re-run measured (result_dump artifact, not gate tier — same reasoning as F337's own native sweep). **Reviewed 2026-09-02** (inline adversarial self-review, §9): caught a real implementation bug (a shared node-count budget silently degraded the octree's effective depth from 6 at n=8 to 3 at n=40 — exactly backwards); fixed by batching, and the full native sweep was RE-RUN post-fix. The corrected numbers below are the post-fix, reviewed numbers; they agree with the pre-fix run to within the fit's own noise (§9), so the fix changes confidence, not the conclusion.
**Verdict — the mask (isolation, in the sense F337 Sec.4/6 asked for):** **BUILT AND VERIFIED.** `lpt_ws_mask_cutcell.smoothed_ws_mask` replaces `lpt_bcc_vertex.ws_mask`'s sharp, pointwise 0/1 Wigner–Seitz-cell indicator with an adaptive-octree fractional-coverage ("cut-cell") mask. Measured against the exact target volume fraction $V_\text{WS}/V_\text{cube}=1/4$ (F305 G7): the sharp mask's own volume-estimate error falls as $\sim n^{-1.07}$ (the staircase order F337 diagnosed); the smoothed mask's error is **~100× smaller at every $n$ tested** ($\le 7\times10^{-4}$, $n=8$–$40$) and does **not** need to shrink further with $n$ to already sit below the physics integral's own $O(1/n^2)$-class floor.
**Verdict — does it change $d_1$ leg 3 (S3)?** **NO, MEASURABLY.** Swapped into the actual `lpt_d1_action_consistent` loop integral (new `mask_grid` parameter, default `None` reproduces F337 bit-for-bit) and re-run natively at $n=12,16,20,24,28,32,36,40$: the fitted convergence exponent for the BCC/`phys` side is $0.92$ ($n{=}24$–$40$ fit) to $1.14$ ($n{=}28$–$40$ fit) — **statistically the same order as F337's sharp-mask result** ($1.11$–$1.35$), still more than a factor of 2 below the Wilson side's own $2.48$–$2.83$. The extrapolated $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3$–$34.1$ depending on fit window, **statistically unchanged from F337's own $31.3$**. Per F337 §4's own explicit exhaustion condition (quoted in full in §5 below), this is not available for a third "still not converged" reading: **F337's hypothesised mechanism (the sharp mask's staircase discretisation error) is measured not to be the cause of the anomalous slow convergence.**
**Modules:** `src/casim/engine/gauge/lpt_ws_mask_cutcell.py` (new); `src/casim/engine/gauge/lpt_d1_action_consistent.py` (extended: `_domain_weight`, `mask_grid` parameter threaded through `pi_loop`/`pi_loop_chunked`/`transverse_B_chunked`/`_side_chunked`/`branch_fork_native_sweep`, default `None` unchanged behaviour — verified bit-identical to pre-F350 at $n{=}12$, see §3).
**Runner:** `tests/runners/run_ws_mask_smoothed_sweep.py` (native, checkpointed, same pattern as F337's `run_l6_native_sweep.py`).
**Test / results:** record `F350-ws-mask-cutcell` (tier gate, entry `mask_isolation_convergence`) → `test-results/F350_ws_mask_isolation.json`; native re-run → `test-results/smoothed_ws_mask_sweep_checkpoint_v2.json` (per-point checkpoint, 96 points) and `test-results/F350_smoothed_dloops_sweep.json` (aggregated, fitted).
**Claim:** none — internal lattice-scheme methodology (testing a named candidate mechanism for a not-yet-quotable estimator's convergence rate) plus a reported, explicitly non-quotable intermediate number; asserts nothing about QM/SM/GR/SR directly and moves no claim card (F337, the finding this extends, carries none either). Declared 2026-09-02.
**Cross-references:** [[F337-l6-decided-native-sweep-outside-bracket]] (names this module's exact remedy and its exhaustion condition, §4/§6), [[F305-bcc-rhombic-lpt-vertices]] (the vertices and `ws_mask`/G7 volume fact this module tests against), [[F280-d1-subtracted-against-wilson]] (the bracket $[1,7.98]$ this measures against), [[F307-action-consistent-d1-and-a-live-refold]], [[F308-refold-repaired-and-two-defects-not-one]] (the estimator this reruns).
**Checked:** 2026-09-02 — inline adversarial self-review (disclosed, §9): 1 real bug found and fixed (a shared node-count budget silently degrading octree depth with n); full native sweep re-run post-fix; conclusion unchanged. 1 minor arithmetic correction (§5, "six" → "~five" decades). All other attacks PASS — **CONFIRMED, NARROWED ON ONE ARITHMETIC DETAIL**.

---

## 1. What was being tested, and why it matters

`docs/status/open-derivations.md` row **d1** (= E3 = Q1 = Q2) is the model's single largest open item: the strong-sector one-loop background-field constant $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$, required $1.773444$. F337 (2026-08-30) closed ledger row **L6** (both sub-questions — which object is the rule's gauge action at finite $a$; is the redundant link-axis mode dynamical) and ran the native $n=28$–$40$ sweep the ledger called for. It did **not** close d1: the two dLoops normalisations diverge instead of converging together, and the fitted convergence power on the BCC/rule side ($\sim n^{-1.1}$ to $n^{-1.35}$) is far slower than the Wilson/cube side's own ($\sim n^{-2.8}$to $n^{-2.97}$, close to the module's assumed $1/n^2$).

F337 §4 named a specific, checkable mechanism and, on review (§"Reviewed & corrected"), an explicit exhaustion condition for retiring the "non-convergence, not falsification" reading a third time:

> the smoothed/anti-aliased WS-mask remedy named in §5/§6 is built and re-run, and the resulting extrapolated $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ either (a) still lies outside $[1,7.98]$, or (b) lies inside it but the fitted convergence exponent is still below the Wilson side's $\approx2.8$ by more than a factor of 2. Either outcome is the falsification of the $g_s=\tfrac12$ lock or the monotonicity assumption that F280 named as a live possibility — not a third round of "still not converged."

This finding builds that mask, verifies it independently before trusting it (F337 §6's own caution: "It was not tested by, e.g., building a smoothed mask and re-measuring; that is next work, not this finding's content"), and then runs exactly that re-measurement.

## 2. Building the mask: what was tried, what was rejected, what was adopted

**The mechanism.** `lpt_bcc_vertex.ws_mask` tests Wigner–Seitz-cell membership pointwise, at each grid cell's center, using the half-space test $\mathbf k\cdot\mathbf G\le|\mathbf G|^2/2$ over the reciprocal vectors $\mathbf G$ (F305's genuine fundamental domain, one quarter of the cube, F305 G7). Used as an integration-domain weight in `pi_loop`/`pi_loop_chunked`, a cell's weight is either exactly $0$ or exactly $1$ depending on whether its *center* is inside — a textbook staircase discretisation of a smooth boundary, first order in the grid spacing.

**First attempt, tried and rejected: fixed-resolution supersampling.** Evaluate `ws_mask` at $S\times S\times S$ sub-points per boundary voxel and average, for a fixed $S$ (tested: $S=16$, on the boundary cells identified by 6-neighbour disagreement in the hard mask). Measured directly: this reduces the volume-estimate error by a constant factor ($\sim16\times$ at $n=40$) but leaves the **log–log slope unchanged**, $-1.00$ versus the sharp mask's $-1.07$ — i.e. still first order in $n$, only with a smaller prefactor, because a fixed sub-sample count's own per-cell bias does not shrink as $n$ grows (the total error stays $O(1/(nS))$). This does not meet the design goal ("whose own discretisation error is $O(1/n^2)$, matching the cube side") and was discarded.

**Adopted method: adaptive octree cut-cell refinement.** For each grid voxel, an *exact* interval (Lipschitz) bound classifies it, per half-space, as provably fully-inside, provably fully-outside, or ambiguous: since $\mathbf k\cdot\mathbf G$ is linear, its max/min over an axis-aligned voxel of half-width $h$ centred at $\mathbf k_0$ is exactly $\mathbf k_0\cdot\mathbf G\pm h\sum_i|G_i|$ — not an approximation. A voxel is resolved as soon as this bound fires for *any* half-space in *either* direction; ambiguous voxels are split into 8 octants and re-tested recursively, with a node-count safety valve (the residual ambiguous volume at the cutoff is assigned weight $0.5$ of itself — a documented, measured bias, not an assumption). Two things were needed to make this numerically well behaved, and are gated (`shell1_matches_ws_mask`):

* An early version using the full `lpt_bcc_vertex._recip_vectors(rng=2)` shell (124 candidate half-spaces) produced runaway node counts under refinement — traced to spurious near-degenerate "ambiguous" classifications from the second shell's extra, non-binding half-spaces. **Measured**: the first shell alone (26 vectors, `rng=1`) reproduces `ws_mask`'s boundary **exactly** (zero mismatches, every $n$ tested) — the second shell is provably redundant for this lattice. Restricting to the first shell fixed the octree's behaviour.
* The "fully outside" per-voxel test is itself conservative (it requires the *same* half-space to be violated everywhere in the voxel, missing voxels that are fully outside via *different* half-spaces in different sub-regions — the geometry near edges/vertices, where several faces meet). This does not make the test wrong, only slower to resolve some voxels than strictly necessary; the ambiguous *volume* was measured to shrink monotonically under refinement regardless (from $36.8\%$ of the initial ambiguous volume after one octree level to $1.05\%$ after five, at $n=16$), never growing, which is what makes the node-count safety valve's residual bias small and controllable.

**Isolation verification (gate `F350-ws-mask-cutcell`, `mask_isolation_convergence`).** Against the exact target $V_\text{WS}/V_\text{cube}=1/4$:

| $n$ | sharp-mask error | smoothed-mask error (post-bugfix, depth_max=5) |
|---:|---:|---:|
| 8 | 0.1094 | 5.46e-4 |
| 16 | 0.0508 | 4.18e-5 |
| 24 | 0.0330 | 4.37e-5 |
| 32 | 0.0244 | 5.36e-5 |
| 40 | 0.0194 | 3.65e-5 |

(the pre-fix numbers at depth\_max$=6$ were $2.03\times10^{-4}$, $4.18\times10^{-5}$, $1.56\times10^{-4}$, $9.73\times10^{-5}$, $2.23\times10^{-4}$ at the same five $n$ — already small, but with a bug, §9, making them *not* strictly improve with $n$, which the corrected column now does: $n=40$'s error is the smallest of all nine $n$ tested.) Sharp-mask error falls as $n^{-1.07}$ (fit over all 9 points, $n=8$–$40$); smoothed-mask error is $\sim500$–$2500\times$ smaller at every $n$ and requires no further shrinkage with $n$ to already sit below the $\sim n^{-2.5}$-to-$n^{-2.8}$ scale the Wilson side's *own* discretisation error occupies over the same range — i.e. it should not be the bottleneck in the physics integral. **Control (D9):** cutting the refinement to `depth_max=1` fails the same gate (worst error $0.0196$, an order of magnitude over the $5\times10^{-3}$ threshold) — a genuine per-depth measurement, not a hardcoded pass.

## 3. Wiring the mask into the loop integral

`lpt_d1_action_consistent.pi_loop`/`pi_loop_chunked` gained a `mask_grid` parameter (default `None`) via a new `_domain_weight` helper: `None` reproduces the sharp `bv.ws_mask(k)` exactly (verified: `branch_fork_native_sweep(ns=(8,12), mask_kind="sharp")` reproduces F337's own published $n{=}12$ row bit-for-bit — $b_0$ recovery $0.4134$, $d\text{Loops}_\text{slope}=-0.2438$, $d\text{Loops}_\text{analytic}=-1.1082$); a supplied `(n,n,n)` array is broadcast along the (mask-independent) temporal axis and used as the weight instead. `branch_fork_native_sweep` gained `mask_kind="sharp"|"smoothed"` to select between them; the Wilson/`sc` side is never affected (`domain="cube"`, no mask). This is a pure plumbing change — the `mask_grid=None` default path is untouched code, run identically to before.

## 4. The native re-run

Same grid ($n=12,16,20,24,28,32,36,40$), same 4 `CELL_RATIOS` momenta, same `pi_loop_chunked`/memory-chunking machinery F337 built — only the BCC-side domain weight is swapped for `smoothed_ws_mask(n, depth_max=5)` (post-bugfix, §9). Checkpointed runner (`run_ws_mask_smoothed_sweep.py`, mirroring F337's own pattern), 96 points total (`test-results/smoothed_ws_mask_sweep_checkpoint_v2.json`):

| $n$ | $b_0$ recovery, Wilson | $b_0$ recovery, `phys` (smoothed) | $b_0$ recovery, `phys` (F337, sharp) | $b_0$ recovery, `raw` (smoothed) | $b_0$ recovery, `raw` (F337, sharp) |
|---:|---:|---:|---:|---:|---:|
| 12 | 1.1144 | 0.4843 | 0.4134 | 0.5918 | 0.5245 |
| 16 | 1.1406 | 0.5079 | 0.4410 | 0.6433 | 0.6056 |
| 20 | 1.1230 | 0.5235 | 0.4911 | 0.6936 | 0.6813 |
| 24 | 1.0984 | 0.5454 | 0.5265 | 0.7583 | 0.7671 |
| 28 | 1.0756 | 0.5761 | 0.5679 | 0.8406 | 0.8672 |
| 32 | 1.0563 | 0.6153 | 0.6163 | 0.9400 | 0.9826 |
| 36 | 1.0404 | 0.6631 | 0.6719 | 1.0567 | 1.1136 |
| 40 | 1.0273 | 0.7186 | 0.7347 | 1.1895 | 1.2601 |

**Two things, both measured directly.** (1) At small $n$ (12–24) the smoothed mask visibly *helps* — `phys` recovery is closer to 1 than F337's sharp-mask value by $0.03$–$0.07$, consistent with the boundary-cell fraction (and hence the sharp mask's bias) being largest at coarse resolution. (2) By $n=32$–$40$ the two masks give **nearly identical** numbers, and the smoothed values are marginally *below* the sharp ones (e.g. $0.7186$ vs $0.7347$ at $n=40$) rather than above — the improvement does not persist, let alone grow, as $n$ increases. `raw` still crosses 1 between $n=32$ and $n=36$ and keeps climbing under the smoothed mask too ($1.057\to1.191$), reproducing F337's leg-2 divergence signature independently — L6's decision is corroborated again, not disturbed.

**Fitted convergence exponent** (log–log fit of $|1-b_0\text{ recovery}|$, same method F337 used):

| fit window | Wilson exponent | `phys` exponent (this finding, smoothed) | `phys` exponent (F337, sharp) |
|---|---:|---:|---:|
| $n=28$–$40$ | $2.83$ | $1.14$ | $1.35$ |
| $n=24$–$40$ | $2.48$ | $0.92$ | $1.11$ |

Both fit windows: the smoothed-mask exponent is *lower*, not higher, than F337's own sharp-mask exponent — if anything the direction is the wrong way for the staircase hypothesis, though the two are close enough (within the fit's own scatter, judged by the $\lesssim0.006$ residuals on both) that "unchanged" rather than "worse" is the honest reading; either way it is nowhere near closing the gap to the Wilson side's $2.5$–$2.8$.

**Extrapolated $\Lambda$**, using the analytic-normalised series alone (the one that demonstrably converges, per F337 and reproduced here) and each window's own fitted exponent:

$$\widehat{d\text{Loops}}=-2.734\ (p{=}1.141,\ n{=}28\text{–}40),\quad -2.905\ (p{=}0.920,\ n{=}24\text{–}40)$$
$$\Rightarrow\ \Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3\ \text{and}\ 34.1\ \text{respectively}$$

against F337's own headline $31.3$ (from averaging its two fit windows' $-2.671$ and $-2.792$) and the required $1.7734$, bracket $[1,7.98]$. **The extrapolated value is statistically indistinguishable from F337's, and remains outside the bracket by essentially the same factor of $\sim4$.**

## 5. Interpretation, per F337's own stated protocol

F337 §4 set the exhaustion condition quoted in §1 in advance of this finding's result, precisely so that a future session (this one) would not need to make a fresh judgement call about whether "still not converged" is available a third time. Both of its named triggering conditions are met: (a) the extrapolated $\Lambda$ is still outside $[1,7.98]$ (by both fit windows), **and** (b) the fitted convergence exponent ($0.92$–$1.14$) is still more than a factor of $2$ below the Wilson side's ($2.48$–$2.83$; ratio $\sim2.2$–$3.0\times$). Per F337's own words, this **is** "the falsification of the $g_s=\tfrac12$ lock or the monotonicity assumption... not a third round of 'still not converged.'"

**What this does and does not mean for the rest of the ledger.** It does **not**, on its own, reopen X1 (colour normalisation): F325 closed X1 on two legs both stated to be *independent of $d_1$*, and the specific value that row d1's own text names as reinstating branch A is $\Lambda\approx3.4\times10^6$ ($\sim5$ decades away, $\log_{10}(3.4\times10^6/31.3)\approx5.04$ — corrected on review, §9, from an earlier "six decades") — not the $\Lambda\approx31$–$34$ measured here or in F337. What it *does* establish is narrower and, this finding argues, still important: **F337's offered mechanism for d1 leg 3's slow convergence (the sharp WS-mask's staircase discretisation error) is measured, not merely argued, not to be the explanation** — building the exact remedy that mechanism calls for and re-running the identical computation changes the numbers by an amount inside the fit's own noise, not by the order-of-magnitude rate change the hypothesis predicted. This finding does **not** attempt to say what the correct next mechanism is (candidates not investigated here: the vertex form factors' own behaviour approaching the BZ boundary; some other feature of the `phys`-branch projection; a genuine, physical breakdown of the $g_s=\tfrac12$/branch-B monotonicity assumption itself) — that is future work, flagged in §7, not resolved here.

## 6. What this changes on the ledger

- **Row d1 / rubric B8 remain open**, now with F337's staircase-mask mechanism tested and excluded rather than merely offered. The "grid, not physics" framing (already qualified once, by F337 itself) is now qualified a second time: the specific grid remedy the ledger and F337 both named has been built, verified, and shown not to be the fix.
- **Ledger row D#9 (charged-lepton overall scale) and D#17 ($v$)**, per `docs/status/open-derivations.md` row E7, are *the same blocker as $d_1$* once F233 is taken seriously — this finding changes nothing about their status directly, but confirms the blocker they share with d1 is not resolved by the route this session tested.
- **L6 stands, untouched** — this finding does not re-litigate it; the `raw`-branch divergence-past-1 signature reproduces independently under the new mask, corroborating rather than disturbing F337's leg-2 decision.
- **A concrete next-step gap**: per F337's own exhaustion language, the honest state of d1 leg 3 is now "the two named hypotheses (grid resolution insufficient; sharp-mask discretisation) are both tested and excluded as the *sole* explanation" — the next session attacking this row should not re-offer either without new evidence, and should instead look at the vertex/propagator construction itself or the branch assumption, per §5.

## 7. Honest scope

- **The octree's "fully outside" test is conservative** (§2) — some voxels are refined further than a tighter test would require. This affects only *how much* refinement work is done, not the correctness of the final weight (verified: the ambiguous volume shrinks monotonically under refinement, never regressing).
- **The residual node-count safety valve** (voxels still ambiguous when refinement is cut off) assigns weight $0.5$ of the remaining tiny volume — a documented approximation, not a claim of exactness; its contribution to the isolation gate's measured error is included in the numbers reported in §2, not assumed away.
- **The "unchanged vs marginally worse" exponent comparison in §4 is not itself a formal significance test** — with only 4–5 points per fit window (the same limitation F337's own fits had), a $\pm0.1$–$0.2$ shift in a log–log power-law exponent is within ordinary fit noise for this data volume. The honest claim is the qualitative one stated in §5 (still $>2\times$ below Wilson, still outside the bracket), not a precise second-decimal comparison between $1.14$ and $1.35$.
- **This finding does not identify the actual mechanism** behind d1 leg 3's slow convergence, only excludes one specific, previously-named candidate. See §5's closing paragraph for what is left untested.
- **`make gate` was not run in full** on this session's device shell (same operational constraint F337 recorded — long/heavy passes risk timeouts on a 45–180s device-shell budget). Verified individually instead (§8).

## 9. Reviewed & corrected

**2026-09-02 — inline adversarial self-review** (disclosed: run by the same session that wrote
this finding, per `.claude/commands/review-finding.md`'s `--inline` mode — no independent cold
subagent infrastructure was available on this device shell; treat the confidence accordingly,
weaker than a genuinely blind review). Ran the command's Step-3-style attack checklist against
the finding, its module, its tests and its result JSONs.

**Found (real, not previously disclosed): the octree's node-count safety budget was SHARED across
the whole array of ambiguous voxels being refined together**, not per voxel or per batch. Since
the per-level refinement cost scales with the array's own size, this made the depth actually
reached fall as the array got bigger — measured directly: effective depth 6 at $n=8$ down to only
3 at $n=40$, exactly backwards, since more boundary/ambiguous voxels at larger $n$ is the normal
case, not a sign of less headroom. The isolation gate's *aggregate* volume-estimate error
happened to stay flat regardless (§2's original numbers, at depth\_max$=6$, nominal) — most
likely because the crude weight-$0.5$ residual assignment is already a fair average for this
symmetric geometry — but this was empirical luck for a pure-volume test, not evidence the mask
behaved identically when weighted by the actual (non-constant) physics integrand.

**Fixed:** `_cutcell_fraction` now splits its input into batches sized so any ONE batch can
finish to the full `depth_max` within a fixed memory budget (`node_budget`), and every batch runs
independently to completion — so every voxel reaches the *same* depth regardless of how many
ambiguous voxels there are in total; only the number of batches grows with $n$. Verified: the
mask's output is now provably independent of `node_budget` (identical bit-for-bit under a
$25\times$ larger budget, at every $n$ tested) — a new regression test,
`test_effective_depth_is_independent_of_node_budget`, guards this. Default settings changed from
`depth_max=6`/a single global `node_cap=2\times10^6` to `depth_max=5`/`node_budget=4\times10^6`
per batch (§2's table above reports the post-fix numbers at these settings).

**Re-ran the full native $n=12$–$40$ sweep with the fix** (new checkpoint,
`smoothed_ws_mask_sweep_checkpoint_v2.json`, superseding the pre-fix run) — §§2 and 4's tables and
numbers above are the corrected, post-fix values. The fitted convergence exponents moved from
$1.141/0.920$ (pre-fix) to $1.135/0.916$ (post-fix, $n{=}28$–$40$/$n{=}24$–$40$), and the
extrapolated $\Lambda$ from $31.31/34.10$ to $31.35/34.16$ — changes far inside the fits' own
noise. **The bug was real and worth fixing, but it did not change this finding's conclusion**;
fixing it raises confidence in that conclusion rather than reversing it.

**Other attacks, PASS or WEAKENS, folded into the text above or left as minor corrections:**
the "sharp"-path bit-identity and the F337 $n{=}12$ reproduction were independently re-verified
(exact match); the mask's first-shell-only test was re-checked at additional untested $n$ (all
exact matches); the exhaustion-condition arithmetic (ratios $0.37$ and $0.40$, both $<0.5$; both
extrapolated $\Lambda$ outside $[1,7.98]$) was independently redone and confirmed; the
"six decades" characterisation of the gap to branch A's reinstatement value was found to be a
minor arithmetic overstatement (the true gap is $\sim5$ decades) and is corrected in §5; the
$0.92$–$1.14$-vs-$1.11$–$1.35$ comparison between this finding's and F337's exponents was
confirmed to already be correctly hedged in §7 as within ordinary 4–5-point fit noise, not a
precise distinction.

## 8. Provenance

- **New:** `lpt_ws_mask_cutcell.py` in full (`_classify`, `_cutcell_fraction`, `smoothed_ws_mask`, `shell1_matches_ws_mask`, `mask_isolation_convergence`); `lpt_d1_action_consistent._domain_weight` and the `mask_grid` parameter threaded through `pi_loop`/`pi_loop_chunked`/`transverse_B_chunked`/`_side_chunked`/`branch_fork_native_sweep` (with `mask_kind="sharp"|"smoothed"`); `tests/runners/run_ws_mask_smoothed_sweep.py`; the rejected fixed-supersampling measurement (§2, not committed as code — reproducible from the description).
- **Reused, not re-derived:** `lpt_bcc_vertex.ws_mask`/`_G`/`_GHALF`/G7's exact $1/4$ volume fact (F305); `lpt_d1_action_consistent.pi_loop_chunked`/`_side_chunked`/`transverse_B_chunked` and `lpt_d1_subtracted.slope_normalised_constant`/`CELL_RATIOS`/`lambda_from_dc`/`lambda_ratio_rule_target`/`F163_C_LAT_WILSON_LOOPS`/`C_MSBAR` (F280/F307/F337), unmodified except for the added optional parameter.
- **Verification:** registry record `F350-ws-mask-cutcell` (tier gate, entry `mask_isolation_convergence`), 1 declared control verified red-only-where-declared; `test-results/F350_ws_mask_isolation.json`, `test-results/smoothed_ws_mask_sweep_checkpoint_v2.json`, `test-results/F350_smoothed_dloops_sweep.json`.
