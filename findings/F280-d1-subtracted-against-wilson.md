# F280 — $d_1$ formulated **subtracted against the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$ anchor**: the master identity uses differences only, the slope-normalised estimator is **exactly** immune to the F272-class measure factor, and the open piece drops from "the whole number" to **one leg of three** — the vertex form factors must supply $\Delta C=-2.016$ (36.2%), with the propagator leg now measured at $-0.992\pm0.044$ and the tadpole-free band $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$ containing the required $1.7734$

**Date:** 2026-08-05 - 12:40
**Status:** Established (formulation + one leg measured) — **6/6 PASS** + control, `casim test --id F280-d1-subtracted` (~10 s). Executes `docs/status/completeness-2026-08-04.md` **gap #3**, whose *smallest next step* reads verbatim: *"Formulate $d_1$ **subtracted against the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ reference** — the gate F162's G3 already named — rather than settling the F267 fundamental domain first."*
**Module:** `casim.engine.gauge.lpt_d1_subtracted` (`src/casim/engine/gauge/lpt_d1_subtracted.py`)
**Script:** `tests/findings/test_F280_d1_subtracted.py` (registry entry `check_d1_subtracted`, tier **gate**)
**Cross-references:** [[F287-bgfield-apparatus-sound-post-F277]] (§6 — the restriction this discharges: *sound for subtracted differences, and $d_1$ is absolute*), [[F162-bgfield-self-energy-b0-gate]] (G3 — the Wilson-28.81 gate named as the reference), [[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the Wilson loops-only constant $C_\text{lat}=6.1386$ and the analytic $C_{\overline{\rm MS}}=131/66$ this quotes), [[F155-qstar-self-energy-and-freeze-bracket]] (A0 — the rule's seagull sector is *exactly* empty, which is what makes leg 1 structural), [[F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1]] (the exact $V\!\to\!\overline{\rm MS}$ factor $e^{11/42}$ and the propagator-vs-vertex *ratio* this converts into absolute numbers), [[F272-bgfield-loop-refold-period]]/[[F277-qed-gluon-refold-period]] (the spurious-measure-factor hazard the estimator is immune to), [[F267-walk-bz-measure-not-the-fft-cube]] (the domain hazard this does **not** address), [[F129-blockspin-free-photon]]/[[F130-blockspin-rg-gauge-gravity]] (near-perfect action — the sign of leg 2). External: Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40 ($\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$, SU(3) pure gauge).

---

## 1. The obstruction this is answering

F287 certified the F162 background-field apparatus SOUND and, in the same breath, forbade the one use $d_1$ needs:

> The apparatus is sound **for subtracted differences**, and $d_1$ must not be taken from this quadrature's absolute normalisation. It has to come either from settling the F267 fundamental domain, or from a **subtracted formulation against a known reference** — and F162's G3 already names the right reference, the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ gate.

The measured residue was an **absolute** $b_0$ recovery of $0.9551$ at $n=40$ rather than $1$. $d_1$ is a finite **absolute** constant, so the restriction bites exactly where the answer is wanted. Gap #3 chose the second exit over the first. This finding takes it.

## 2. Conventions (fixed once)

Transverse scalar, $a=1$, Feynman background gauge:

$$\Pi(q^2)=\frac{b_0}{16\pi^2}\Big[\ln\frac{1}{q^2}+C\Big],\qquad b_0=\tfrac{11}{3}C_A=11,$$

$$\Delta C\equiv C_\text{lat}-C_{\overline{\rm MS}},\quad C_{\overline{\rm MS}}=\tfrac{131}{66}\ \text{(F163, analytic dim reg)},\quad \frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{lat}}=e^{\Delta C/2},\quad d_1=\frac{11}{16\pi^2}\,\Delta C.$$

The required target is **derived, not written as 1.773**:

$$\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}=\frac{e^{11/42}}{q_\ast a}=\frac{1.299434}{0.7327}=\mathbf{1.773444},$$

with $e^{11/42}$ the exact $V\!\to\!\overline{\rm MS}$ leg of F239 ($a_1(6)=\tfrac{11}3$, $b_0^\alpha=7/4\pi$) and $q_\ast a$ the registered `q_star_a_implied`. Equivalently $d_1^\text{rule}=0.079818$ against $d_1^{W}=0.468198$.

## 3. S1 — the master identity: every term is a difference

Wilson's one-loop constant splits into loops and the contact seagull + Haar measure. The rule's seagull sector is **exactly empty** — F155-A0, $u_0\equiv1$ — so the rule carries the first term alone:

$$\Delta C_W=\Delta C_W^\text{loops}+T_W,\qquad \Delta C_\text{rule}=\Delta C_\text{rule}^\text{loops}.$$

Subtracting and exponentiating gives the formulation gap #3 asked for:

$$\boxed{\;\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}=28.8086\;\exp\!\Big[-\tfrac12\big(T_W+\delta_\text{loops}\big)\Big],\qquad \delta_\text{loops}\equiv\Delta C_W^\text{loops}-\Delta C_\text{rule}^\text{loops}.\;}$$

Both bracketed terms are **differences**: $T_W$ is Wilson-internal, $\delta_\text{loops}$ is lattice-minus-lattice on a common grid. **No absolute lattice normalisation appears anywhere in the formula.** That is the whole point, and it is what F287 §6 permits. Verified as an identity against the direct form $e^{\Delta C_\text{rule}/2}$ to residual $6.7\times10^{-16}$.

## 4. S2 — why the subtraction is *legal*: the slope-normalised estimator

The hazard F272/F277/F265 identified is a spurious **multiplicative measure factor** on the loop integral — F272 says applying `make_kgrid_bcc` to this integrand *"would have inserted a spurious factor."* Estimate the constant by dividing by the log slope **measured on the same grid** rather than by the analytic $2b_0/16\pi^2$:

$$s=\frac{d\Pi}{d\ln(1/Q)}\ \text{(measured)},\qquad \hat c=\frac{\Pi}{s}-\ln\frac1Q,\qquad \hat C=2\hat c.$$

Under $\Pi\to\lambda\Pi$ the slope goes $s\to\lambda s$, so **$\hat C$ is exactly invariant** while the analytic-normalisation constant drifts by the closed form $2(\lambda-1)\langle\ln(1/Q)\rangle+(\lambda-1)C_0$. Measured at $\lambda=3.7$: invariant drift $3.1\times10^{-15}$, analytic drift $12.6185494248$ against the closed form $12.6185494248$ — agreement to $<10^{-12}$.

**Honest scope, stated as sharply as the result.** Slope normalisation immunises against a measure *factor*. It does **not** immunise against integrating over a *region* inequivalent to a fundamental domain: such a region changes the log part and the constant part differently, and no normalisation undoes that. F267 is still open. What the two together buy is that the F272-class hazard is **closed algebraically**, and the F267-class hazard is **bounded** by the measured $Q$-flatness and grid convergence of the subtracted quantities rather than assumed away.

## 5. S3 — the propagator leg, measured in **absolute** $\Delta C$ units

$\delta_\text{loops}$ has a propagator face (rule vs Wilson at continuum vertices) and a vertex face. F239 could only report the propagator face as a *ratio* to Wilson's ($0.11$–$0.16$), explicitly declining an absolute number because the $b_0$ normalisation was not in hand. In the subtracted formulation it is, because the normalisation cancels.

All $Q$ are placed at multiples of the **F287 §5 resolution floor** $Q\gtrsim2\cdot(2\pi/n)$ — the hazard that once returned $b_0=4.06$ from a fit whose residual looked fine.

| $n$ | slope-normalised | analytic-normalised | $s_\text{rule}/s_W$ |
|---:|---:|---:|---:|
| 16 | $-1.24797$ | $-0.98415$ | 1.04268 |
| 20 | $-1.17297$ | $-0.97109$ | 1.02651 |
| 24 | $-1.12955$ | $-0.96413$ | 1.01805 |
| $\to\infty$ (Richardson, $1/n^2$) | $\mathbf{-1.03580}$ | $\mathbf{-0.94805}$ | $\to1$ |

Both series are monotone and converge as $1/n^2$; they differ only through the finite-grid split of the two kernels' measured slopes, which F287 §4 shows vanishes as a power law. Neither normalisation is privileged, so the leg is quoted as their midpoint with the half-spread as the uncertainty:

$$\Delta C_\text{prop}=\mathbf{-0.9919\pm0.0439}.$$

The sign is the one the near-perfect action requires (F129/F130): the rule's finite constant sits **below** Wilson's.

## 6. S4/S6 — the budget: the open piece is now one leg of three

Required total shift from Wilson, $\Delta C_\text{rule}-\Delta C_W=1.14585-6.72135=-5.57550$:

| leg | $\Delta C$ | share | status |
|---|---:|---:|---|
| 1. Wilson seagull + Haar measure **absent** (F155-A0) | $-2.5676$ | 46.1% | **structural** — $u_0\equiv1$ exactly; magnitude $=$ anchor $-$ F163 loops-only |
| 2. propagator face | $-0.9919\pm0.0439$ | 17.8% | **MEASURED** here, grid-convergent |
| 3. rule 3-gluon $+$ ghost **vertex form factors** | $-2.0160$ | 36.2% | **OPEN** |
| total | $-5.5755$ | 100% | |

The arithmetic that matters, and it is machine-checked (`leg1_plus_leg3_is_anchor_fixed`): **leg 1 $+$ leg 3 $=$ total $-$ leg 2 independently of $\Delta C_W^\text{loops}$.** So F163's open $Q\to0$ high-resolution extrapolation — its own item (a) — cannot move the total or leg 2. It only redistributes between legs 1 and 3. Carrying F163's stated spread ($\Lambda_\text{loops}\sim6$–$9$) through gives

$$\Delta C_\text{vertex}\in[-2.257,\,-1.446].$$

Restricted to $\delta_\text{loops}$ alone (required $-3.0079$), the propagator face is $33.0\%$ and the vertex face $67.0\%$ — **F239's "vertex-dominated" verdict, now with numbers on both sides instead of a ratio on one.**

## 7. S5 — the tadpole-free band, and the falsifier

Because the rule's seagull is exactly empty and its action is nearer the continuum than Wilson's (F129/F130; F287 §4 *measures* the rule's $b_0$ discretisation error at $5.3$–$5.7\times$ smaller than Wilson's at every grid), the answer is bracketed **before** the vertex computation exists:

$$0\le\Delta C_\text{rule}^\text{loops}\le\Delta C_W^\text{loops}\quad\Longrightarrow\quad \frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}\in[1,\;7.980].$$

The required $1.7734$ sits **inside**, at 11.1% of the band. Wilson's $28.8086$ is above the band top by $3.61\times$ — structurally excluded, as A0 requires.

> **Falsifier.** A completed rule vertex computation returning $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ outside $[1,7.98]$ falsifies either the $g_s=\tfrac12$ lock or the monotonicity assumption, and the two are distinguished by *which* edge is crossed: below 1 means $\Delta C_\text{rule}^\text{loops}<0$ (assumption), above 7.98 means it exceeds Wilson's loops-only constant (lock). Equivalently, the vertex leg must land in $[-2.257,-1.446]$.

The monotonicity step is an **assumption, named as one**, not a theorem. It is labelled as such in the module and in the check.

## 8. Checks (`check_d1_subtracted`, 2026-08-05 - 12:40)

| # | Statement | Result | Tier |
|---|---|---|---|
| S1 | master identity $\Lambda=28.8086\,e^{-(T_W+\delta_\text{loops})/2}$ closes against the direct form; residual $6.7\times10^{-16}$ | PASS | exact (bookkeeping) |
| S2 | $\hat C$ exactly invariant under a measure factor ($3.1\times10^{-15}$); analytic-normalised constant drifts by its closed form ($12.6185494248$, matched $<10^{-12}$) | PASS | exact |
| S3 | propagator leg monotone, $1/n^2$-convergent, $-1.20<\Delta C_\text{prop}<-0.80$, half-spread $<0.10$ | PASS | quantitative |
| S4 | three-leg budget closes to $0.0$; leg1$+$leg3 anchor-fixed | PASS | exact |
| S5 | target $1.7734$ inside $[1,7.980]$; Wilson $28.8086$ excluded | PASS | bracketed |
| S6 | open vertex leg is a **minority** share ($36.2\%<50\%$) of the required shift | PASS | bracketed |

**Overall 6/6 PASS**, ~10 s.

**Control (D9).** `casim test --id F280-d1-subtracted --param lambda_wilson=1.0` — with no Wilson scheme gap the seagull leg changes sign, the band collapses below the target, and **S5 and S6 go red**. Verified. The record's two parameters are precisely its two external/quoted inputs, so the perturbation attacks the thing the record is asserting rather than a decoration.

## 9. Honest scope

- **Nothing new is integrated.** The integrand is `bgfield_loop._Bcoeff_numeric` (refold-free since F272) and the Wilson-side numbers are F163's committed artifact. What is new is the bookkeeping that makes them a statement about $d_1$, plus the absolute conversion of the propagator leg.
- **Leg 1's magnitude is not independently computed.** It is the anchor minus F163's loops-only constant. Its *structural* content — that the rule has no such leg at all — is F155-A0 and is exact; its *number* inherits F163's open $Q\to0$ extrapolation, which is why the leg1/leg3 split carries the $[-2.257,-1.446]$ width while the total does not.
- **F267 is untouched.** This finding removes the F272-class factor hazard from the $d_1$ route and says so; it does not settle which region of the rule kernel's $\sqrt3$-fcc period lattice the cube samples. Gap #3 asked for the subtracted route *instead of* settling F267, and that is what was done.
- **$C_{\overline{\rm MS}}=131/66$ is F163's analytic dim-reg result, reused, not re-derived.**
- The two normalisations of leg 2 differ by 8.5% at the extrapolated limit. That spread is reported as the uncertainty rather than resolved by choosing one, because choosing one is exactly the move F287 §6 warns against.

## 10. What this hands on

1. **The one remaining computation is now specified numerically:** the rule's own $\cos(k/2)$-dressed 3-gluon $+$ ghost vertex form factors must supply $\Delta C_\text{vertex}=-2.016$, within $[-2.257,-1.446]$. Before this, the target was "whatever makes $q_\ast a=0.733$."
2. **The cheapest way to narrow it is not new physics but F163's item (a)** — the $Q\to0$ high-resolution extrapolation of Wilson's loops-only $C_\text{lat}$ (`run_lpt_wilson_selfenergy.py`, $n=64$–$128$, native). It cannot move the total; it halves the width on the leg 3 target.
3. **The $[1,7.98]$ band is publishable as a bracket now**, with a named assumption and a two-sided falsifier, which is a stronger statement than F155's $q_\ast a\in[1/\sqrt3,0.97]$ because it is expressed in the quantity the tension is measured in.

## 11. Provenance

- **New:** the subtracted master identity (every term a difference); the slope-normalised estimator and its exact measure-invariance with the closed-form drift of the analytic alternative; the absolute $\Delta C$ conversion of the propagator leg with its $1/n^2$ Richardson limit under both normalisations; the three-leg budget and the proof that leg1$+$leg3 is anchor-fixed; the tadpole-free band and its two-sided falsifier; `lambda_ratio_rule_target` deriving $1.7734$ from $e^{11/42}$ and the registered $q_\ast a$ rather than writing the number.
- **Reused:** `bgfield_loop._Bcoeff_numeric` (F162/F287); `lpt_wilson_selfenergy.B0_INV_G2`, `LAMBDA_RATIO_WILSON_SU3`; F163's committed `lambda_status` ($C_\text{lat}=6.138643$, $C_{\overline{\rm MS}}=131/66$); F155-A0; F239's $e^{11/42}$; F287 §4 slope data and §5 resolution floor.
- **External anchors (targets, not inputs):** $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.8086$ (Kawai–Nakayama–Seo, *Nucl. Phys.* **B189** (1981) 40).
- **Verification:** registry record `F280-d1-subtracted` (tier gate, entry `check_d1_subtracted`), 6/6 PASS + control, 2026-08-05 - 12:40.
