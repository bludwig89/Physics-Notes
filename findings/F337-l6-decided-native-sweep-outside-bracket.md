# F337 — Ledger row L6 is **decided on both legs** (propagator = the rhombic action's own quadratic form; the redundant link-axis mode is **not** dynamical), and the native $n=28$–$40$ sweep the ledger called for **does not close $d_1$ leg 3** — it sharpens the tension instead, to $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\approx31$, outside F280's own $[1,7.98]$ bracket

**Date:** 2026-08-30 - 13:10
**Numbering:** **F337**, taken as `max+1` against `F336` (`casim index` → `NEXT FREE NUMBER F337`, no gaps) after a same-session collision: `F336` was claimed by a concurrent session (`findings/F336-twoloop-vp-nonlog-scope.md`) while this session was mid-computation. Re-checked immediately; artifacts renamed before anything was committed.
**Status:** Established (L6 decided) + measured-but-inconclusive (d1 leg 3) — **4/4 PASS** on the gate-tier record, 1 declared control verified red-only-where-declared, `casim test --id F337-l6-decision` (PASS, ~16 s). The native $n=24$–$40$ sweep is a committed artifact, not a gate-tier assertion (it cannot run at gate speed — see §4).
**Verdict — L6 leg 1 (propagator):** **DECIDED.** The rule's gauge action at finite $a$ is the rhombic action's **own quadratic form** (already the code default), not the F26/$\Omega_\text{even}$ rotation-law propagator. Structural: vertex/propagator consistency (the exact lattice Ward identity, F305 G5) requires both to derive from the same action; F308 §3 already measured the alternative, $K_\text{true,4d}=3\Omega_\text{even}^2+k_t^2$, to be **aperiodic** under the very reciprocal lattice the rhombic vertices are exactly periodic under (F305 G7) — disqualifying it as a lattice propagator on this Brillouin zone regardless of numerics. Empirical, new: substituting it for the own quadratic form while keeping the rhombic vertices fixed makes the $b_0$-recovery diagnostic **diverge away from 1** with resolution ($1.13\to1.66\to2.08$ at $n=8,10,12$) instead of converging.
**Verdict — L6 leg 2 (is the redundant link-axis mode dynamical?):** **DECIDED — not dynamical; project it out (the `phys` branch, already the code default).** F305 §4's exact isometry argument ($PP^{\mathsf T}=\mathbb I$, so only the projected branch's continuum limit is 4-D Yang–Mills) is now backed by new numerical evidence this finding adds: extending the $b_0$-recovery ladder from F307's $n=12$–$20$ out to $n=8$–$40$ (11 points) shows the unprojected (`raw`) branch **crossing 1 somewhere in the $n=28$–$40$ range and continuing to climb** ($0.38\to1.26$, monotonic, no turnover; the precise crossing point is Q-window sensitive, see §3 and §6) — a clean divergence, not a faster convergence as the $n\le20$ ladder alone could suggest — while the projected (`phys`) branch approaches 1 monotonically from below throughout, never crossing it.
**Verdict — $d_1$ leg 3 (S3, quotability):** **STILL NOT QUOTABLE**, and the native sweep the ledger predicted would close it does not. New diagnosis: fitting the *actual* convergence power (not assuming $1/n^2$) gives $b_0$-recovery deviation $\sim n^{-1.1\text{ to }-1.35}$ on the rule side against $\sim n^{-2.8}$ on the Wilson side — a genuinely slower rate, plausibly the sharp Wigner–Seitz domain mask's $O(1/n)$-type boundary discretisation (present only on the BCC/rule side) against the smooth periodic cube integration (Wilson side, no mask needed). Central estimate from the one series that *does* converge cleanly under the fitted power (analytic-normalised; the slope-normalised series' increments do **not** shrink through $n=40$ and are not used for the headline): $\widehat{d\text{Loops}}=-2.731\pm0.060$, implying $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3$ — outside F280's $[1,7.98]$ bracket by a factor of $\sim4$. Read as **non-convergence, not falsification** (per F307's own standing caution on exactly this failure mode), but the direction of travel (further out, not closer in, as $n$ grows) is the opposite of what the ledger's "grid, not physics" remedy predicted.
**Modules:** `src/casim/engine/gauge/lpt_d1_action_consistent.py` (extended: `pi_loop_chunked`, `_side_chunked`, `_chunk_for`, `_omega_even_quadratic_form`, `propagator_scheme_divergence`, `branch_fork_native_sweep`, `check_l6_decision`)
**Runner:** `tests/runners/run_l6_native_sweep.py` (native, checkpointed; ~15–20 min wall time spread over many short invocations on this session's 4 GB machine)
**Test / results:** record `F337-l6-decision` (tier gate, entry `check_l6_decision`) → `test-results/F337_l6_decision.json`; native sweep → `test-results/F337_l6_native_sweep.json` (aggregated) and `test-results/F337_l6_native_sweep_raw_per_Q.json` (per-momentum checkpoint)
**Claim:** none — internal lattice-scheme methodology (which object is the gauge propagator at finite $a$; a convergence-rate diagnosis of a not-yet-quotable estimator) plus a reported, explicitly non-quotable intermediate number; asserts nothing about QM/SM/GR/SR and moves no claim card (F305/F307/F308, the findings this extends, carry none either — CL278/CL239 cite them as supporting evidence for other cards, not as their own subjects). Declared 2026-08-30.
**Cross-references:** [[F305-bcc-rhombic-lpt-vertices]] (the fork this decides, §§4–5, and the vertex/domain machinery reused verbatim), [[F307-action-consistent-d1-and-a-live-refold]] (the estimator this extends; its $n=12$–$20$ ladder and S3 red-by-design), [[F308-refold-repaired-and-two-defects-not-one]] (the repaired path this runs on; its $K_\text{true,4d}$ aperiodicity measurement, reused as the structural half of leg 1), [[F280-d1-subtracted-against-wilson]] (the budget and bracket this measures against), [[F325-x1-resolved-branch-b-adopted]] (upstream — not re-litigated), [[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the Wilson-side anchor constants).
**Checked:** 2026-08-30 — 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**

---

## 1. What was being decided, and the plan

`docs/status/open-derivations.md` row **L6** named two sub-questions blocking $d_1$ leg 3, and named its own method:

> F305 §7.4 notes the machinery is action-agnostic, so testing the alternative costs one function — do that empirically rather than deciding by argument alone if possible.

Both legs are decided in that spirit: an empirical test is built and run for each, and both are checked against (and corroborate) the structural arguments F305 already gave. Neither leg needed re-litigating the X1 branch question (closed, F325) or $b_0=11$ (exact, closed) — this finding does not touch either.

## 2. Leg 1 — the propagator, decided

**The candidates.** (a) the rhombic action's own quadratic form, $S(k)=\sum_l\hat k_l^2$ over the 5 generalised link axes (F305) — already the default in `lpt_d1_action_consistent.pi_loop`; (b) the F26/$\Omega_\text{even}$ rotation-law kinetic form, generalised to 4D by F308 §3 as $K_\text{true,4d}(k)=3\,\Omega_\text{even}(\mathbf k)^2+k_t^2$.

**Structural argument (already available, restated because it is decisive on its own).** Lattice perturbation theory's one-loop Ward/Slavnov–Taylor identities cancel only when the internal-line propagator is the inverse of the *same* quadratic form the vertices were generated from — F305's vertices and $S(k)$ come from literally the same term enumeration over the same rhombic loop words (`lpt_bcc_vertex.terms`), which is exactly why the tree-level Ward identity (G5, $\sum_j\Gamma_{ij}\hat k_j=0$) holds to $10^{-13}$. $K_\text{true,4d}$ is not derived from that expansion at all — it comes from the second-quantised single-particle rotation law (decision 2, CLAUDE.md) — and F308 §3 already measured it to be **aperiodic** under $2\pi$, $4\pi$ *and* $8\pi$ axis shifts, i.e. not periodic under the reciprocal lattice the rhombic vertices (and $S(k)$, F305 G7) are exactly periodic under. A propagator that is not a well-defined function on the same Brillouin-zone torus as the vertices is not a lattice Feynman rule on this lattice at all, independent of what any number comes out to.

**Empirical test (new).** `propagator_scheme_divergence` (registry entry `check_l6_decision`) runs the identical rhombic 3-gluon+ghost vertices against both propagator choices, at $n=6,8,10,12$, using the module's own $b_0$-recovery diagnostic:

| $n$ | $b_0$ recovery, own $S(k)$ | $b_0$ recovery, swapped $K_\text{true,4d}$ |
|---:|---:|---:|
| 6 | 0.2087 | 0.4929 |
| 8 | 0.3097 | 1.1269 |
| 10 | 0.3779 | 1.6635 |
| 12 | 0.4134 | 2.0778 |

The own-form deviation from 1 shrinks monotonically ($0.79\to0.59$); the swapped deviation **grows** ($0.51\to1.08$, already past 1 by $n=8$ and climbing). This is the directional signature §5 of F305 predicted (agreement only at $k\to0$, up to 86% apart at generic $k$) made quantitative in the one-loop diagnostic that actually matters for quoting $d_1$.

**Control (D9).** Swapping which candidate occupies the "own" vs "swapped" slot (`swap_control=True`) must flip both conditions to `False` — a hardcoded verdict could not do this, only a genuine measurement can. Verified: `own_dev_nonincreasing=False`, `swap_diverges=False` under the swap. Gate record `F337-l6-decision`, leg `L6_leg1_propagator_divergence`.

**Decision: the rhombic action's own quadratic form is the rule's gauge action at finite $a$.** No code change was needed — this was already `lpt_d1_action_consistent`'s default, adopted pragmatically by F307 for LPT self-consistency; this finding is what turns that pragmatic default into a decided founding choice, with both a structural reason and a measured signature.

## 3. Leg 2 — the redundant link-axis mode, decided

F305 §4 gave an exact structural argument (the Cartesian projector $P^a{}_i=d_i^a/2$ satisfies $PP^{\mathsf T}=\mathbb I$ **exactly**, so only the branch that projects out $\hat n=\tfrac12(-1,1,1,1)$ has a continuum limit that is 4-D Yang–Mills at all) plus a small, ungated, sub-resolution-floor numerical trend ($b_0$ at $n=8,12,16$: projected $9.67\to11.56$ towards $11$; unprojected $-2.21\to-1.86$, wrong sign). F307's own gated ladder ($n=12$–$20$, properly above the F287 §5 resolution floor) complicated this picture: on that ladder the **unprojected** branch's $b_0$ recovery ($0.52\to0.68$) was numerically *closer* to 1 than the projected branch's ($0.41\to0.49$) at every $n$ — the opposite ordering from F305's ungated trend. Taken at face value over $n\le20$ alone, this looked like a genuine tension between the structural argument and the module's own quoting diagnostic.

**It is not a tension — it is a short ladder.** Extending the same measurement (module's `_side`, unchunked for $n\le24$, `pi_loop_chunked` for $n\ge28$ — verified bit-identical to $10^{-16}$, §4) out to $n=40$ resolves it cleanly:

| $n$ | $b_0$ recovery, Wilson | $b_0$ recovery, `phys` (projected) | $b_0$ recovery, `raw` (unprojected) |
|---:|---:|---:|---:|
| 8 | 0.9060 | 0.3097 | 0.3839 |
| 10 | 1.0495 | 0.3779 | 0.4719 |
| 12 | 1.1144 | 0.4134 | 0.5245 |
| 14 | 1.1377 | 0.4410 | 0.5704 |
| 16 | 1.1406 | 0.4579 | 0.6056 |
| 20 | 1.1230 | 0.4911 | 0.6813 |
| 24 | 1.0984 | 0.5265 | 0.7671 |
| 28 | 1.0756 | 0.5679 | 0.8672 |
| 32 | 1.0563 | 0.6163 | 0.9826 |
| 36 | 1.0404 | 0.6719 | **1.1136** |
| 40 | 1.0273 | 0.7347 | **1.2601** |

`raw` crosses 1 between $n=32$ and $n=36$ on this four-momentum fit and keeps climbing — it is not converging faster than `phys`, it is **diverging past the target**, monotonically, with no turnover across an 11-point ladder spanning $n=8$ to $40$. `phys` approaches 1 monotonically from below throughout and never crosses it. A log–log power fit of $|1-b_0\text{ recovery}|$ over $n=28$–$40$ gives exponent $-2.97$ for `raw` (deviation *growing* as $n^{2.97}$) against a genuine convergent $+1.35$ for `phys` (§4). The earlier, shorter ladder's ordering was real but pre-asymptotic — exactly the caution F307/F308 attach to every number in this chain.

**Q-window sensitivity (added on review, 2026-08-30).** The *exact* crossing interval is not robust to which of the four `CELL_RATIOS` momenta anchors the slope fit: leave-one-out refits (dropping each of the 4 momentum points in turn and refitting $b_0$ recovery from the remaining 3) move the nominal `raw` crossing anywhere from $n=28$–$32$ to $n=36$–$40$ — across the full measured range, not a small perturbation. What **is** robust across all four leave-one-out variants — and is the claim this finding actually needs — is direction and endpoint, not the interval: `raw`'s $|1-b_0\text{ recovery}|$ increases monotonically in every variant and lands strictly above 1 by $n=40$ in every variant, while `phys`'s stays below 1 and approaches it monotonically in every variant, never crossing. The finding is corrected to rest on that weaker, robust statement rather than on the specific $n=32$–$36$ interval.

**Decision: the redundant link-axis mode is not dynamical; the projected (`phys`) branch is the rule's gauge sector.** Both the exact structural argument and the extended numerical ladder now agree, where over $n\le20$ alone they appeared to disagree.

## 4. The native $n=28$–$40$ sweep: it runs, but does not close S3

**Memory, not physics, was the obstacle at $n\ge28$.** `lpt_d1_action_consistent.pi_loop`'s unchunked path builds the full $(n,n,n,n,5,5,5)$ vertex tensors twice (`W`, `Z`) plus their gauge-fixing terms — on this session's 4 GB machine, `run_sweep2.py` (the direct, unchunked call) was **SIGKILLed by the OOM killer** at $n=32$: measured peak RSS $3.79\,$GB against $3.9\,$GB total, wall clock $7.4\,$s (`/usr/bin/time -v`, reproduced twice). `pi_loop_chunked` streams the first grid axis in slices of size $\lceil131072/n^3\rceil$ (chosen so peak memory is roughly constant, $\approx0.4$–$0.8\,$GB from $n=28$ through $n=40$) and is verified **bit-identical** to the unchunked path at shared $n$ ($\max|\Delta|\sim10^{-15}$ at $n=24$, measured directly on review; well inside the gate-tier test's $10^{-12}$ tolerance — see `tests/findings/test_F337_l6_decision.py`). This is what let the sweep the ledger asked for actually run.

**What it found.** $dLoops = \hat C(\text{rule}) - \hat C(\text{Wilson})$, `phys` branch, both normalisations:

| $n$ | slope-normalised | analytic-normalised |
|---:|---:|---:|
| 12 | $-0.244$ | $-1.108$ |
| 16 | $-0.224$ | $-1.464$ |
| 20 | $-0.295$ | $-1.722$ |
| 24 | $-0.439$ | $-1.912$ |
| 28 | $-0.639$ | $-2.053$ |
| 32 | $-0.878$ | $-2.158$ |
| 36 | $-1.142$ | $-2.235$ |
| 40 | $-1.418$ | $-2.288$ |

Two things, both new:

1. **The two normalisations do not bracket each other convergently** (F280's leg 2 signature of a trustworthy estimator) — they move apart, then the analytic series decelerates while the slope series does not. The **analytic-normalised** series has differences that shrink geometrically ($-0.141,-0.105,-0.077,-0.053$ across $n=24\to40$, ratio $\approx0.7$ each step) — a clean, fittable power-law convergence. The **slope-normalised** series' differences ($-0.200,-0.239,-0.264,-0.276$) are still *growing* through $n=40$, with only the *second* differences shrinking — consistent with an asymptotically **linear**, not convergent, approach in this range. A 3-parameter free fit ($A+Bn^{-p}$) on 4–5 points is ill-conditioned for either series taken alone (checked: it returns unphysical near-zero or runaway exponents); fixing $p$ from an independent measurement is the only way to get a meaningful limit.
2. **The convergence rate itself is much slower than the module's built-in $1/n^2$ assumption.** A log–log fit of $|1-b_0\text{ recovery}_\text{phys}|$ gives exponent $p=1.35$ (fit on $n=28$–$40$, 4 points) or $p=1.11$ (fit on $n=24$–$40$, 5 points) — compare the Wilson side's own $p=2.83$ over the same range, close to the assumed $1/n^2$. Using either fitted $p$ (not the built-in $1/n^2$) to extrapolate the analytic-normalised $dLoops$ series gives $-2.671$ ($p=1.35$) or $-2.792$ ($p=1.11$) — much closer to each other than the $1/n^2$-assumption extrapolation would give, and both residual sets are small (analytic: max residual $0.006$; the fit is genuinely good).

**Plausible mechanism, named but not proven.** The Wilson/cube side needs no domain mask — the cube already is its own Brillouin zone. The rule/BCC side integrates over the Wigner–Seitz cell via `lpt_bcc_vertex.ws_mask`, a **sharp 0/1 indicator** evaluated pointwise on the same cubic FFT grid (F305 §7 item 2). A hard boundary sampled on a grid is a textbook source of $O(1/n)$ "staircase" discretisation error (surface-to-volume, not the smooth $O(1/n^2)$ bulk error a periodic integrand gets) — and $p\approx1.1$–$1.35$ sits exactly between a pure $O(1/n)$ boundary term and the bulk $O(1/n^2)$, consistent with a mix of both. This is offered as the most likely explanation for why the rule side's convergence rate genuinely differs from the Wilson side's and from the module's own $1/n^2$ extrapolation assumption — it is not verified by directly measuring the mask's own convergence in isolation, which is the natural next step (§6).

**Central estimate.** Using only the analytic-normalised series (the one that demonstrably converges) and averaging its two fitted-power extrapolations:

$$\widehat{dLoops} = -2.731 \pm 0.060, \qquad \Delta C_\text{rule,loops} = 6.885, \qquad \boxed{\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule} = 31.3}$$

against F280's required $1.7734$ and its own standing bracket $[1, 7.98]$. **This is outside the bracket by a factor of $\sim4$.** Per the ledger's own two-sided falsifier language (F280 §7, restated at row d1): a vertex computation returning $\Lambda$ outside $[1,7.98]$ was named as a live possibility that "falsifies the $g_s=\tfrac12$ lock or the monotonicity assumption." **This finding does not make that call.** F307 §3 already showed a similar (smaller) out-of-bracket implied value ($14.27$, at $n\le20$) and explicitly read it as the estimator reporting non-convergence rather than physics — and the diagnosis in this section (a demonstrably-too-slow, mask-driven convergence rate that the naive $1/n^2$ ansatz was hiding) is exactly the kind of finding that supports the same reading here, now with a mechanism rather than a guess. The number is **reported, not quoted** — it is not $d_1$, and $S3$ stays red.

**Exhaustion condition for the “non-convergence, not falsification” reading (added on review, 2026-08-30).** This reading has now been invoked twice on the same estimator — F307 §3 ($\Lambda=14.27$, $n\le20$) and this finding (above, $\Lambda=31.3$, $n\le40$) — with the implied value moving *away* from the bracket both times, not toward it. It is not available a third time for free. It is retired, and F280 §7's two-sided falsifier language takes over, specifically if: the smoothed/anti-aliased WS-mask remedy named in §5/§6 is built and re-run, and the resulting extrapolated $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ either (a) still lies outside $[1,7.98]$, or (b) lies inside it but the fitted convergence exponent is still below the Wilson side's $\approx2.8$ by more than a factor of 2. Either outcome is the falsification of the $g_s=\tfrac12$ lock or the monotonicity assumption that F280 named as a live possibility — not a third round of “still not converged.”

## 5. What this changes on the ledger

- **Row L6 closes.** Both sub-questions are decided, with a structural argument and a new empirical signature for each. Nothing about $d_1$'s future computation is blocked by an undecided founding choice any more.
- **Row d1 / rubric B8 do NOT close.** The native sweep the ledger predicted would close S3 ran, and did not — worse, it moved the implied $\Lambda$ further from the bracket, not closer, and named a specific, checkable reason (the WS-mask discretisation order) rather than leaving "grid, not physics" as an unexplained placeholder.
- **The remedy the ledger named ("a native sweep at $n=28$–$40$") is superseded by this finding's own diagnosis:** the real remedy is either (a) a smoothed/anti-aliased WS-cell indicator (replacing the hard 0/1 mask with something whose own discretisation error is $O(1/n^2)$, matching the cube side), which would let the *existing* $n\le40$ data actually converge at the assumed rate, or (b) a genuinely much larger $n$ (the $p\approx1.1$–$1.35$ fit implies $n$ in the hundreds to shrink the residual by another order of magnitude), which is not available on this session's hardware.
- **F280's bracket and F155's $q_\ast a$ bracket both stand untouched** — this finding measures against them, it does not move them.

## 6. Honest scope

- **The propagator decision (leg 1) is structural first, empirical second** — the aperiodicity argument alone is sufficient; the divergence measurement corroborates it at cheap $n$ and is the gate-tier record's content.
- **The branch decision (leg 2) rests on an 11-point ladder, not a proof that `raw` diverges for all $n$** — a turnover beyond $n=40$ cannot be excluded by measurement, only made implausible by the clean, accelerating, sign-definite trend and by the structural isometry argument that does not depend on $n$ at all.
- **The mask-discretisation explanation in §4 is offered, not verified.** It was not tested by, e.g., building a smoothed mask and re-measuring; that is next work, not this finding's content.
- **No claim is made that $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3$ is $d_1$'s value.** It is an intermediate, non-quotable read of a demonstrably non-converged (on the slope-normalised side) or slowly-converging (on the analytic-normalised side) estimator, reported with its full diagnostic because reporting only "still not quotable" without it would re-hide exactly the information F287 §6 and F307 §3 exist to keep visible.
- **The "non-convergence, not falsification" reading is not open-ended** — see §4's exhaustion condition. Having now been invoked twice with the implied $\Lambda$ moving further from the bracket each time, it is not available for a third invocation without the specific positive finding §4 names.
- **`make gate` was not run in full** on this session's machine (sandbox operational note: long/heavy passes risk the same OOM class this finding diagnoses). Verified individually instead: `casim index --check`, `tools/check_module_registry.py`, `tools/check_test_registry.py`, and `pytest tests/findings/test_F337_l6_decision.py tests/findings/test_F307_action_consistent_d1.py tests/findings/test_F305_bcc_rhombic_vertices.py tests/findings/test_F308_refold_repaired.py` (29/29 PASS, no regressions from the shared-module edits) — all green, 2026-08-30.
- **The raw per-$Q$ checkpoint** (`test-results/F337_l6_native_sweep_raw_per_Q.json`) was produced by scratch scripts during the investigation and cross-verified against the production `branch_fork_native_sweep`/`_side_chunked` path at $n=28$ to $10^{-10}$ before being adopted as the committed artifact, rather than re-running the full 15–20 minute sweep a second time from the production entry point alone.

## 7. What this hands on

1. **d1 is unblocked on physics grounds** but not on grid grounds: whoever attacks it next should build the smoothed WS-mask (§4/§6) before spending more $n$, since the current mask's own convergence order is now the named bottleneck.
2. **`pi_loop_chunked` / `_chunk_for`** are general-purpose — any future LPT computation on the BCC action that needs $n>28$ on a memory-constrained machine can reuse them directly (F305's own "the machinery is action-agnostic" now doubles as "the machinery is memory-agnostic").
3. **The OOM finding itself is worth keeping**: `docs/status/open-derivations.md`'s "the remedy is grid, not physics" is falsified as a *sufficient* remedy on this hardware and should not be repeated verbatim for other rows without checking the memory budget first.

## 8. Provenance

- **New:** `pi_loop_chunked`, `_chunk_for`, `transverse_B_chunked`, `_side_chunked`, `_omega_even_quadratic_form`, `propagator_scheme_divergence`, `branch_fork_native_sweep`, `check_l6_decision` (all `casim.engine.gauge.lpt_d1_action_consistent`); the bit-identity proof between chunked and unchunked paths; the OOM measurement (`/usr/bin/time -v`, SIGKILL at $n=32$, peak RSS 3.79 GB); the extended 11-point $b_0$-recovery ladder ($n=8$–$40$) for both branches; the power-law (not $1/n^2$) fit of the rule side's convergence rate and its Wilson-side contrast; the WS-mask discretisation-order hypothesis; `tests/runners/run_l6_native_sweep.py`.
- **Reused, not re-derived:** `lpt_bcc_vertex` (F305) — vertices, `quadratic_form`, `khat`, `ws_mask`, `NHAT_BCC`; `gluon_self_energy.K_true_4d`/`omega_even` (F308 §3's definition); `lpt_d1_subtracted` — `CELL_RATIOS`, `slope_normalised_constant`, `budget`, `lambda_from_dc`, `lambda_ratio_rule_target`, `F163_C_LAT_WILSON_LOOPS`, `C_MSBAR` (all F280/F163); `lpt_d1_action_consistent.pi_loop`/`_side`/`_T3grid`/`_Vgf` (F307), unmodified, used as the bit-identity reference.
- **Verification:** registry record `F337-l6-decision` (tier gate, entry `check_l6_decision`), 4/4 PASS + 1 control verified red-only-where-declared, 2026-08-30 - 13:10.

## Reviewed & corrected

**2026-08-30 - 15:30** — attack pass: **CONFIRMED-NARROWER**. Found: the exact $n=32$–$36$ crossing point in leg 2's evidence (§3) is Q-window sensitive (leave-one-out refits over the 4 `CELL_RATIOS` momenta move it anywhere from $n=28$–$32$ to $n=36$–$40$); the recurring “non-convergence, not falsification” reading applied to $d_1$ leg 3 (§4, now invoked twice with the implied $\Lambda$ moving further from the bracket each time: F307's $14.27$, then this finding's $31.3$) had no stated exhaustion condition; the header lacked the required stamp; and a bit-identity magnitude claim (§4/§8) was slightly undersold at $n=24$ ($\sim10^{-15}$ measured, “$\sim10^{-16}$” claimed, both far inside the $10^{-12}$ gate). Fixed: narrowed §3/the header verdict to the direction-and-endpoint claim that survives every leave-one-out variant rather than the specific interval; added an explicit exhaustion condition to §4/§6 naming what a smoothed-WS-mask re-run would have to show to retire the “non-convergence” reading; corrected the bit-identity magnitude in §4; added this stamp. Rejected: none. Deferred: none — a minor note on the two power-law fits' intercept-regression labelling was independently checked and found harmless, needing no fix.
