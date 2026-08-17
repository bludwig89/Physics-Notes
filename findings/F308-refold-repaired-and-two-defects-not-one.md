# F308 — The `lpt_selfenergy` refold is **repaired**, and the audit found **two** independent folds where F307 reported one: the ghost-sum fold (large, on a branch nothing published used) and an **unperiodic rule-propagator fold** (small, on the branch every published rule constant used). The fold fires **iff $Q\ge\pi/n$**, which is why the committed $d_1$ sweep is clean at $n=8$ and moves only in 3 of its 24 rows

**Date:** 2026-08-11 - 12:40
**Status:** Established (repair + audit + closed-form firing condition) — repaired path agrees with F307's independent refold-free path to $6.8\times10^{-16}$; `F307-action-consistent-d1` still **PASS** and its control still **CONTROL** after the repair.
**Module:** `casim.engine.gauge.lpt_selfenergy` (repaired), `casim.engine.gauge.lpt_d1_action_consistent` (consumer updated)
**Runner:** `tests/runners/run_d1_selfenergy.py --refold-rerun` (the 3 affected rows, ~16 min native, instead of the full ~1.2 h sweep)
**Script:** `tests/findings/test_F308_refold_repaired.py` (registry entry `check_refold_repaired`, tier **gate**)
**Cross-references:** [[F307-action-consistent-d1-and-a-live-refold]] (§4, which demonstrated the defect and explicitly declined to repair it), [[F272-bgfield-loop-refold-period]] (the original: *"the background-field loop refolded $k+q$ by a period the rule kernel does not have"* — this finding shows that exact statement was still true inside `lpt_selfenergy`), [[F277-qed-gluon-refold-period]] (the four-site sweep, and its lesson that a fold cannot be audited by grep), [[F280-d1-subtracted-against-wilson]] / [[F305-bcc-rhombic-lpt-vertices]] (the $d_1$ budget and vertices this module feeds), [[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the Wilson-side constants, unaffected).

---

## 1. What F307 handed over

F307 §4 demonstrated a live fold in `lpt_selfenergy._pi_bgfield` and stated the remit plainly: *"The refold defect is demonstrated, not repaired. Repairing `lpt_selfenergy` re-dates every number it produced and belongs to whoever owns that module's findings."* Its §6 item 2 added: *"until then the 2026-07-19 rule $\Lambda\approx2.08$ should not be cited."*

This finding does the repair, and the audit it required changed the diagnosis.

## 2. The firing condition, in closed form

The loop grid is $k_j=(j+\tfrac12)\tfrac{2\pi}{n}-\pi$ and the external momentum is $q=(Q,0,0,0)$, so $k+q$ leaves $[-\pi,\pi)$ **only** on the top $1/n$ slice of the $k_0$ axis, and only when $Q$ exceeds the half-spacing:

$$\boxed{\ \text{the fold fires}\iff Q\ \ge\ \pi/n\ }$$

| $n$ | $\pi/n$ | fires at $Q\in\{0.1,0.15,0.2,0.3\}$? | grid fraction folded |
|---:|---:|---|---:|
| 8 | 0.3927 | **none** | 0 |
| 12 | 0.2618 | $Q=0.3$ | 8.3% |
| 16 | 0.1963 | $Q=0.2,\ 0.3$ | 6.25% each |

This is the reason the defect survived: it is invisible at small $Q$ and at coarse grids, i.e. exactly where a cheap sanity check gets run.

## 3. There were two folds, not one, and they behave oppositely

Measured at $n=6$ by running each branch with the fold in and out:

| branch | measured effect | mechanism |
|---|---|---|
| `fp='leading'`, any kernel | **large** — $C$ goes $32.78\to16.52$ at $Q{=}0.6$, $26.36\to16.98$ at $Q{=}0.8$ (a factor 2) | the ghost momentum factor is a **sum**, $2\sin(k/2)+2\sin((k{+}q)/2)$. Each term has period $4\pi$, so folding one flips its sign **relative** to the other and the sum becomes a difference |
| `fp='exact'`, `kernel='wilson'` | **exactly 0.0** | the exact form factor $2\sin((p{+}p')/2)$ takes a **global** sign under the shift, which cancels in the $t\otimes t$ contraction; Wilson's $\hat k^2$ is $2\pi$-periodic per axis |
| `fp='exact'`, `kernel='rule'` | **small but real** — $\lvert\Delta\Pi\rvert\approx2\times10^{-3}$, $\Delta C=0.008$ at $Q{=}0.6$ and $0.032$ at $Q{=}0.8$ | $K_\text{true,4d}=3\Omega_\text{even}^2+k_t^2$ has **no axis-wise period at all** — measured non-invariant under $2\pi$, $4\pi$ **and** $8\pi$ shifts (Ω_even is fcc-periodic; the time leg is continuum $k_t^2$). Folding evaluates the integrand at a **different physical momentum** |

**F307 measured the first row** (its `refold_defect` runs `fp='leading'`), and its §4 attribution — *"the ghost form factor $2\sin(k/2)$ has period $4\pi$, and the wrap flips its sign"* — is exactly right **for that branch**. The correction this finding makes is that the branch every published constant used, `fp='exact'`, is immune to that mechanism, and is contaminated instead by a **second, independent** fold in the rule propagator. That second one is F272's original defect verbatim, still resident four findings later.

**One correction to F307's §4 wording.** *"The transverse components never disagreed"* is approximate rather than exact: at $n=6,\ Q=0.8$ they disagree by $1.4\times10^{-4}$ (`leading`) and $2.1\times10^{-3}$ (`exact`). The asymmetry that made the defect invisible is real — $\Pi_{00}$ moves $\sim\!250\times$ more than $\Pi_{11}$ on the `leading` branch — but it is a ratio, not a zero.

## 4. The repair

`_wrap` is retained and documented as the **control path**; every production entry point (`_pi_gluon_loop`, `_pi_ghost_loop`, `_pi_bgfield`, `finite_constant_bgfield`) takes `refold: bool = False` and routes its momenta through `_folder(refold)`, so the module now has **one** switch rather than five call sites, and `refold=True` reproduces the pre-repair numbers exactly. Two of the five original sites were mathematical no-ops ($\hat k^2$ is $2\pi$-periodic; `_wrap` on the grid is the identity) and are documented as such rather than silently dropped — the point of F277's lesson is that "harmless here" is a *per-integrand* judgement that has to be written down.

`lpt_d1_action_consistent._ls_pi_ll` no longer monkeypatches `lpt_selfenergy._wrap`; it passes `refold=` instead. F307's demonstration therefore survives the repair of the thing it demonstrates, which is the outcome the falsification-record rule wants.

**Verification.**

| # | Statement | Result |
|---|---|---|
| R1 | repaired default $=$ F307's independent refold-free `pi_loop` at $Q=0.8,\ 1.2$ | $6.8\times10^{-16}$, $4.0\times10^{-16}$ |
| R2 | `F307-action-consistent-d1` still passes | **PASS**, 18.9 s |
| R3 | F307's control still reddens exactly its declared leg | **CONTROL** — `wrap_control=True` → `['S1_refold_defect_demonstrated']` |
| R4 | F307's `refold_defect` still fires at the size it published | `defect_size` $=0.099516$ (F307: $\approx0.0995$) |
| R5 | $n=8$ sweep rows bit-unchanged (fold never fires) | $\max\lvert\Delta\Pi\rvert=3.5\times10^{-18}$ |
| R6 | `seagull_tadpole` $Z_0$ unchanged at $n=8,12,16$ | identical to the committed sweep to $3\times10^{-17}$ |

Six of these are carried as a gate record, `F308-refold-repaired` (**6/6 PASS**, 23.6 s). Its control — `unrepair_control=true`, i.e. putting the fold back into the production default — reddens **exactly `R1`** and is journalled `CONTROL`. The measured red set is smaller than this finding's first draft expected (it predicted R1/R3/R6): R3 and R4 compare `refold=False` against `refold=True` explicitly and are blind to the default, and R6 runs below the $Q\ge\pi/n$ threshold where the two are equal by construction. The record carries the measured set, not the expected one.

## 5. Re-dating the constants — what moves and what does not

The committed artifact is `test-results/d1_selfenergy_sweep.json` (a native run, ~1.2 h, `fp='exact'`, $Q\in\{0.1,0.15,0.2,0.3\}$, $n\in\{8,12,16\}$).

- **The whole Wilson side stands.** $C=10.4250/10.6276/10.7018$, $\Lambda=1.6062/1.6210/1.6265$. The fold is provably a no-op on `fp='exact'`+`wilson` — mechanism in §3, measured 0.0.
- **The $n=8$ rule row stands**, $C=16.3311$, $\Lambda_\text{rule}=2.1008$ — verified bit-unchanged (R5), because $\pi/8>0.3$.
- **Three rule rows need a native re-run:** $(n{=}12,Q{=}0.3)$ and $(n{=}16,Q{=}0.2,0.3)$. `run_d1_selfenergy.py --refold-rerun` does exactly those and nothing else — 3 evaluations, ~16 min, against re-running 24.
- **Expected size, stated before the run so it can be wrong:** scaling the $n=6$ measurements by folded fraction gives $\Delta C\lesssim0.01$ per affected row, so $\Delta C_\text{mean}\lesssim0.005$ and $\Delta\Lambda/\Lambda=\Delta C/2b_0\lesssim0.02\%$. The rule $\Lambda$ trend $2.1008\to2.1192\to2.1264$ is **not** expected to move materially.
- **F307 §6's embargo can be narrowed, not lifted.** *"The 2026-07-19 rule $\Lambda\approx2.08$ should not be cited"* was the right call on the information F307 had. What the audit shows is that the contamination on the published branch is at the $10^{-4}$ level, not the factor-2 level — but the three rows are still un-re-run, so the correct statement is **"clean at $n=8$, pending at $n=12,16$"** rather than either "contaminated" or "fine".

## 6. What this does **not** touch

- **No $d_1$ number is claimed or moved.** F280's budget, its band $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$, F155's $q_\ast a\in[0.577,0.979]$ and F307's deliberate `quotable: False` all stand exactly as written. This finding repairs an integrand; it does not close a leg.
- **The cube-vs-fundamental-domain question (F267/F305 §5) is untouched.** Not folding is necessary, not sufficient: `_pi_bgfield` still averages the rule kernel over the **cube** with uniform measure, and §3 shows that kernel is not cube-periodic. That is the *domain* hazard, and it is F305's, not this finding's.
- **`particles/induced_stiffness.py` holds six fold sites** that this audit did not examine. It is another sector; flagged, not swept. Given that this is the fifth and sixth instance of the class, a sixth is a reasonable prior.

## 7. Provenance

- **New:** the $Q\ge\pi/n$ firing condition and its table; the two-mechanism split (sum-fold vs unperiodic-propagator) with the measured global-sign cancellation that makes `fp='exact'`+`wilson` exactly immune; the measured aperiodicity of `K_true_4d` under $2\pi/4\pi/8\pi$ axis shifts; the repair and its single-switch form; the row-level re-dating of the committed sweep and the targeted re-run.
- **Reused, not re-derived:** F307's `pi_loop` as the independent refold-free reference and its `refold_defect` as the control; F163's Wilson constants; `bgfield_loop._Bcoeff_numeric` as the continuum baseline.
- **Verification:** R1–R6 above, 2026-08-11 - 12:40.
