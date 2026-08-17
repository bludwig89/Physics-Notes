# F307 — The $d_1$ estimator now runs **action-consistently on one code path**, each side on its own action and its own Brillouin zone; the number is **not quotable** at $n\le20$ ($b_0$ recovery $0.41$–$0.49$ on the BCC side), and the unified path exposed an **F272/F277-class refold still live** in `lpt_selfenergy`

**Date:** 2026-08-08 - 13:10
**Status:** Established (machinery + one defect), **NUMBER OPEN BY DESIGN** — 8/8 PASS + control, `casim test --id F307-action-consistent-d1` (PASS on the tree, 24.8 s; control **CONTROL**, journalled). Its S3 leg is the *quoting* gate and is **RED on purpose**.
**Module:** `casim.engine.gauge.lpt_d1_action_consistent` (`src/casim/engine/gauge/lpt_d1_action_consistent.py`)
**Script:** `tests/findings/test_F307_action_consistent_d1.py` (registry entry `check_action_consistent_d1`, tier **gate**)
**Results:** `test-results/F307_action_consistent_d1.json`
**Cross-references:** [[F305-bcc-rhombic-lpt-vertices]] (supplies the rule's vertices and its fundamental domain), [[F280-d1-subtracted-against-wilson]] (the budget this feeds and the slope-normalised estimator this reuses verbatim), [[F287-bgfield-apparatus-sound-post-F277]] (§6, the absolute-normalisation restriction; §5, the resolution floor), [[F272-bgfield-loop-refold-period]]/[[F277-qed-gluon-refold-period]] (the defect class §4 found a fifth instance of), [[F265-bcc-gauge-action-blindness]], [[F163-wilson-lattice-selfenergy-vertices-28p81-gate]], [[F155-qstar-self-energy-and-freeze-bracket]] (A0, the empty seagull).

---

## 1. What was blocking leg 3, and what is not blocking it any more

F280 reduced $d_1$ to one open leg — the rule's own 3-gluon + ghost vertex form factors, required to supply $\Delta C_\text{vertex}=-2.0160$ within $[-2.257,-1.446]$. Two things stood in the way, and they were different things:

1. **F287 §6:** the cubic quadrature is sound *for subtracted differences only*, and $d_1$ is absolute. F280's answer is the slope-normalised estimator $\hat C=2\langle\Pi/s-\ln(1/Q)\rangle$, exactly invariant under an overall measure factor. Reused here verbatim.
2. **F265:** the rule's vertices are not Wilson's. [[F305-bcc-rhombic-lpt-vertices]] now derives them.

With both discharged the estimator can be run **action-consistently** for the first time: vertices *and* propagator from the same action on each side, each integrated over its own genuine fundamental domain — the cube is the hypercubic Brillouin zone; the BCC zone is the Wigner–Seitz cell of the reciprocal lattice, exactly one quarter of the cube. What comes out,

$$\delta_\text{loops}=\hat C_\text{rule}-\hat C_\text{Wilson},$$

is the **full** loops difference — propagator face *and* vertex face together — which is the quantity F280's budget wants rather than only its leg 2.

## 2. S1 — the two actions really are on one path

The hypercubic branch of this module reproduces the established `lpt_selfenergy._pi_bgfield` **to $1.1\times10^{-15}$**, once that module's refold is removed (§4). That is the check that "one code path" is a fact and not a description: the same enumerator, contraction, gauge-fixing vertex, ghost sector and transverse projection produce Wilson's numbers when handed Wilson's loop word.

## 3. S3 — the number, and why it is **not** quoted

Slope-normalised, on the F280 `CELL_RATIOS` window (every $Q$ clearing the F287 §5 two-cell resolution floor):

| $n$ | $b_0$ rec. Wilson | $b_0$ rec. rule (projected) | $b_0$ rec. rule (unprojected) | $\delta_\text{loops}$ slope-norm. | $\delta_\text{loops}$ analytic-norm. |
|---:|---:|---:|---:|---:|---:|
| 12 | 1.1144 | 0.4134 | 0.5245 | $-0.24375$ | $-1.10817$ |
| 16 | 1.1406 | 0.4579 | 0.6056 | $-0.22380$ | $-1.46435$ |
| 20 | 1.1230 | 0.4911 | 0.6813 | $-0.29490$ | $-1.72212$ |
| $\to\infty$ ($1/n^2$) | | | | $\mathbf{-0.29248}$ | $\mathbf{-2.03140}$ |

**This does not clear the project's own bar for quoting a constant, and the finding says so rather than reporting the midpoint.** Three reasons, each visible in the table:

- the BCC side's $b_0$ recovery is $0.41$–$0.49$ and still climbing — F280/F287's standing diagnostic for "the measured slope is not yet the asymptotic log slope";
- the two normalisations **diverge** with $n$ ($-0.24\to-0.29$ against $-1.11\to-1.72$) where F280's leg 2 had them converging as $1/n^2$ and bracketing tightly. The half-spread here is $0.87$, twenty times leg 2's $0.044$;
- consequently the budget residual is meaningless as physics. For the record, feeding the midpoint $-1.1619$ into F280's leg-2 slot leaves $-1.8460$ in the leg-3 slot and implies $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=14.27$, **outside** F280's own $[1,7.98]$ band. That is not a falsification of the band. It is the estimator telling you it is not converged, and reading it as physics would be exactly the mistake F287 §6 exists to prevent.

**The cause is grid, not physics.** The Q window is squeezed from below by the resolution floor and from above by $O(Q^2)$ lattice contamination, and on the BCC side those bounds have not opened far enough apart by $n=20$. The remedy is a native sweep at $n=28$–$40$; the same integrand at $Q\in[0.35,1.0]$ — below the floor, so not quotable either, but on the other side of the squeeze — gives $b_0=9.67/10.94/11.56$ at $n=8/12/16$ (F305 §4). The two windows disagreeing by that much *is* the statement that neither is converged.

`check_action_consistent_d1` therefore returns `quotable: False` and its S3 leg is red. The record passes on S1 and S2 and is honest about S3.

## 4. The defect the unified path found

`lpt_selfenergy._pi_bgfield` — the module that produced the 2026-07-19 rule constants $\Lambda\approx2.06\to2.08$ — wraps the ghost and propagator momenta into $[-\pi,\pi)$. The propagator $\hat k^2$ is $2\pi$-periodic, so the wrap is harmless there. The **ghost form factor $2\sin(k/2)$ has period $4\pi$**, and the wrap flips its sign.

| $Q$ | wrapped $\Pi_{LL}$ | unwrapped $\Pi_{LL}$ | refold-free path |
|---:|---:|---:|---:|
| 0.8 | 0.180920 | 0.081404 | 0.081404 |
| 1.2 | 0.203421 | 0.103945 | 0.103945 |

The transverse components never disagreed — which is why this survived F277's sweep of four sites. Defect size $\approx0.0995$ in $\Pi_{LL}$ at $n=6$, $Q=0.8$; agreement on removal is $1.1\times10^{-15}$.

> **Narrowed 2026-08-08 - 15:40 — the reach of this defect is smaller than first stated, and the correction matters.** On a midpoint grid $k_\text{max}=\pi-\pi/n$, so $k+q$ leaves the cube **iff $Q>\pi/n$**. The wrap then flips the sign of one component of the ghost form factor $2\sin(k/2)$ — and the transverse projection contracts only $t_0^2$ and $t_1^2$, both blind to that sign. Measured: at $n=12$, $Q=0.3$ (which *does* clear $\pi/12=0.2618$) the wrapped and refold-free paths give **bitwise identical** $B=-0.298080107$, $\Delta$ exactly $0$. The original clause *"so the defect propagates into every constant that module produced"* was **too strong and is withdrawn**: the defect reaches a constant only where the $Q$ window clears $\pi/n$ **and** the observable is not quadratic in the flipped factor. It is still a real defect and S1 and its control stand unchanged — but it does **not** contaminate `d1_selfenergy_sweep`, and the 2026-07-19 rule constants are not impeached by it either (see §9).

This is the fifth instance of the F272 class. F277's own lesson was that it was in four places; the standing implication is that a refold is a property of *each* integrand's period and cannot be audited by grep.

**Control (D9).** `--param wrap_control=true` puts the $2\pi$ refold back into *this* path; S1 goes red. That is the right perturbation because S1's content is that being refold-free is what makes the two paths agree.

## 5. Honest scope

- **No value for $\delta_\text{loops}$, leg 3, $q_\ast a$ or $\alpha_s(M_Z)$ is claimed.** F280's bracket $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$ and F155's $q_\ast a\in[0.577,0.979]$ both **stand untouched**.
- **The budget arithmetic is unchanged and still an identity** (`closes_to_total`, `leg1_plus_leg3_is_anchor_fixed` both green). What is uncertain is the input, not the bookkeeping.
- **The rule side inherits F305 §5's declared gap:** this module uses the rhombic action's own quadratic form as the propagator, because LPT is only consistent that way. If the model decides the F26 rotation law is the gauge propagator at finite $a$, the rule side must be rebuilt, not rescaled.
- **The rule side also inherits F305 §4's fork.** Both branches are computed and reported; `phys` is the default only because its continuum limit is Yang–Mills.
- The refold defect is *demonstrated*, not repaired. Repairing `lpt_selfenergy` re-dates every number it produced and belongs to whoever owns that module's findings.

## 6. What this hands on

1. **One native sweep** at $n=28$–$40$ closes S3. Nothing else is in the way: the vertices exist, the domain is a genuine fundamental domain, the estimator is measure-invariant and the budget is wired. `casim test --id F307-action-consistent-d1 --param ns='(28,32,36)'`, or drive `delta_loops` directly.
2. **`lpt_selfenergy` needs the refold removed** and its July-19 constants re-dated. Until then the 2026-07-19 rule $\Lambda\approx2.08$ should not be cited.
3. **The two-window disagreement is itself a measurement** to make: mapping $b_0$ recovery across the whole $Q$ range at fixed $n$ locates the usable window instead of guessing at its edges.
4. **F280's leg 2 is now re-measurable with lattice vertices** rather than continuum ones, on this path, once S3 is green — which will also settle the sign tension between F280's $\Delta C_\text{prop}=-0.9919$ (rule below Wilson) and the truncated-vertex reading that put the rule above.

## 7. Provenance

- **New:** the action-consistent formulation (vertices and propagator from one action per side, each on its own fundamental domain); the shared-path implementation of the background-field loop for two actions; the $b_0$-recovery quoting gate and its deliberate red; the refold demonstration in `lpt_selfenergy` and its two-sided control.
- **Reused, not re-derived:** `lpt_d1_subtracted.slope_normalised_constant`, `CELL_RATIOS`, `budget`, `lambda_ratio_rule_target`, `F163_C_LAT_WILSON_LOOPS`, $C_{\overline{\rm MS}}=131/66$ (all F280/F163); `lpt_bcc_vertex` (F305); the Abbott gauge-fixing vertex structure and exact ghost form factor (F162, 2026-07-19).
- **External anchors (targets, not inputs):** $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$, Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40.
- **Verification:** registry record `F307-action-consistent-d1` (tier gate, entry `check_action_consistent_d1`), 8/8 PASS + control, 2026-08-08 - 13:10.

## 8. Verification amendment — 2026-08-08 - 14:05

Run on the tree. `casim test --id F307-action-consistent-d1` **PASS** (24.8 s);
`check_control_soundness.py --run` returns **CONTROL** — *"`--param wrap_control=True` reddens
exactly `['S1_refold_defect_demonstrated']` of 3 leg(s)"* — journalled in
`test-results/control-soundness.json`.

**Gate-tier grid.** The record runs at `ns = (8, 10)`, not the 12/16/20 ladder §3 quotes: the
cost is not the grid but `refold_defect`'s two calls into `lpt_selfenergy`'s brute-force
generator, so `_ls_pi_ll` is memoised (identical under this module's own `wrap_control`) and the
control's second pass reuses it. S3 is red at every grid tried — that statement does not depend
on the ladder. At `ns = (8, 10)` the b0-recovery deviation reads **0.690** and the midpoint
dLoops **−0.709**, against 0.587 and −1.162 on the 12/16/20 ladder: the two disagreeing by that
much across grids is itself §3's point, and is the reason no value is quoted.

## 9. `d1_selfenergy_sweep` landed — the pre-F265 rule has a converged digit, 20% above the lock

`run_d1_sweep.sh` completed 2026-08-08 - 13:32 (n = 8/12/16, ~78 min).  It measures a
**different object** from §3: the *pre-F265* rule — the F26 rotation-law propagator folded
against the hypercubic plaquette's Abbott vertices — not the action-consistent rhombic rule this
module builds.  Recording it here because it is the first converged number the $d_1$ chain has
produced, and because §4's defect turns out not to touch it.

| $n$ | Wilson $C$ (transverse-only) | rule $C$ | rule $Q$-spread |
|---:|---:|---:|---:|
| 8 | 10.42502 | 16.33105 | 0.2292 |
| 12 | 10.62762 | 16.52332 | 0.2856 |
| 16 | 10.70177 | 16.59794 | 0.3131 |
| $\to\infty$ ($1/n^2$) | **10.7927** | **16.6839** | |

Pairwise Richardson on the rule gives 16.6771 and 16.6939, so the limit is stable at
$\pm0.01$.  In $\Delta C$ units ($C/b_0$, $b_0=11$):

$$\Delta C_\text{rule}=\mathbf{1.5167},\qquad \Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=\mathbf{2.1348},\qquad d_1=0.10565,$$

against the $g_s=\tfrac12$ lock's requirement $\Delta C=1.14585$, $\Lambda=1.77344$,
$d_1=0.079818$ — an overshoot of $+0.371$ in $\Delta C$, $\times1.204$ in $\Lambda$.  The implied
matching scale is $q_\ast a=e^{11/42}/\Lambda=\mathbf{0.6087}$ against the registered
$q_\ast a_\text{implied}=0.7327$.

**It lands inside both standing brackets.**  F155's $q_\ast a\in[0.577,0.979]$ — near the bottom
edge, but inside.  F280's tadpole-free band $\Lambda\in[1,7.980]$ — comfortably inside, so the
falsifier F280 §7 wrote is **not** tripped and the monotonicity assumption survives.

**And the shortfall is inside the one acknowledged uncertainty.**  With F163's committed Wilson
loops-only constant, $\delta_\text{loops}=4.15379-1.51672=2.63708$ against F280's required
$3.00790$ — short by $0.371$, which is $91\%$ of the half-width $0.406$ that F280 already carries
on the leg-1/leg-3 split from F163's open $Q\to0$ extrapolation.  So this is **consistent with the
lock at the edge of the stated error**, not a falsification of it — and F163 item (a), the
cheapest open computation in the chain, is exactly what would decide.

**Three things stop this being the digit.**

1. **The $Q$-spread grows with $n$** — rule $0.229\to0.286\to0.313$, Wilson $0.312\to0.406\to0.460$.
   $Q$-flatness is the $b_0$-preservation signature, so a spread that *widens* as the grid refines
   says a residual log is entering, which is the opposite of clean convergence.  §4's defect was
   the obvious suspect and has been **excluded by measurement**, so this is unexplained.
2. **The sweep and F163 disagree about the same object.**  The sweep's Wilson transverse-only
   $\Delta C=0.981$ ($\Lambda=1.633$); F163's loops-only $\Delta C=4.154$ ($\Lambda=7.980$) — a
   factor $4.2$.  F163's own verdict calls its number an insufficient transversality-inference
   (*"$\Lambda\sim8.0$ vs target $28.81$ … the $\sim3\times$ gap is the genuine remaining
   computation"*), and F280 imports it to set leg 1.  `leg1 + leg3` is anchor-fixed, so neither the
   total nor the rule's requirement moves — but the budget's internal split does, substantially.
3. **It is the pre-F265 hybrid.**  F305 shows the rule's own gauge action is the 4-bond rhombus,
   and F305 §5 measures its quadratic form against $3\Omega_\text{even}^2$ at up to $86\%$ apart at
   generic $k$.  Until the model decides which object is its gauge action at finite $a$, this digit
   belongs to the hybrid, not to the rule.

