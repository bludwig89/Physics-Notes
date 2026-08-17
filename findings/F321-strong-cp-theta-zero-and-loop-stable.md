# F321 — Strong CP: $\theta_\text{QCD}=0$ is a theorem of the rule's loop set, and loops cannot move it

**Date:** 2026-08-17 - 10:40
**Status:** Confirmed — 20/20 checks PASS (5 at literal `0.0`), 3/3 controls redden **disjoint** leg sets
**Module:** `src/casim/engine/gauge/colour_theta.py` (new)
**Tests:** record `F321-strong-cp` (tier gate), driver `tests/findings/test_F321_strong_cp.py`
**Results:** `test-results/F321_strong_cp.json`
**Cross-refs:** F53 (C/CP per species — the phase B11 misattributes), F43 (dynamical gluons), F265/F305/F307 (the rhombic BCC gauge action and its true vertices), F91 (even-vs-chiral propagator classification), F162 (background-field gluon self-energy), F27 (complex-mass step)
**Closes:** completeness row **B11**, and open-derivations **E9** in the sense stated in §6 — parameter **#19** stops being an independent input

---

## Summary

Completeness row B11 has carried the same residual for three reports: *"tree $3.3\times10^{-16}$; loops open."* Two things were wrong with it, and this finding addresses both.

**The accounting.** B11's evidence column names F53, but F53's P5 measures the **F27 complex-mass phase**, and F53's own Remaining section says strong CP *"is a separate phase in the gluon sector (F43), untouched here."* So the row's tree-level number was a statement about a different $\theta$; the row did not have tree-level evidence to build a loop question on top of.

**The physics.** In Euclidean signature the $\theta$-term is the **unique purely imaginary** gauge invariant — the weight is $e^{-S_\text{YM}+i\theta Q}$ — so *"the rule's Euclidean action is real"* and *"the rule contains no $\theta$-term"* are the same statement, and a loop-generated $\theta$ would have to show up as a generated imaginary part. Reality here is not a convention: it is a property of the rule's **loop set**. The rule's minimal gauge loop is the 4-bond rhombus, and its 20 oriented minimal loops (6 spatial $\times2$, 4 temporal $\times2$) are **closed under reversal**, so $\sum_\text{loops}\operatorname{Tr}U = 2\operatorname{Re}\sum\operatorname{Tr}U$ for **every** configuration.

Measured on Haar-random SU(3) configurations on a genuine 4-D BCC$\times$time lattice: $\operatorname{Im}S = 1.2\times10^{-14}$ at 99.7 % disorder, and $S$ is invariant under $U\to U^*$ while the one-sense loop functional is odd under it at **literal `0.0`**. Every position-space vertex coefficient is real at **literal `0.0`** at 2, 3 and 4 legs, colour indices sampled. Because the class of functions obeying $V(-k)=\overline{V(k)}$ is closed under products and under $q\to-q$ symmetric loop integration, the effective action obeys it at **every order** — which is precisely the item the 2026-06-29 audit flagged.

What this is **not**: a solution of the strong CP problem. Peccei–Quinn asks why a *free* parameter is tiny. This rule has no slot for that parameter, which is a different statement — contingent on the rule, and not a relaxation mechanism. And $\bar\theta = \theta + \arg\det M_q$: the first term closes here, the second is the quark mass texture (E6/E7) and **does not**.

---

## 1. What B11 actually cited

| | quantity | value | source |
|---|---|---|---|
| what B11's residual says | $\theta_\text{QCD}$ at tree level | $3.3\times10^{-16}$ | attributed to F53 |
| what F53 P5 measures | the **F27 complex-mass phase** $\theta(x)$ — one-tick eigenphase independence | $3.3\times10^{-16}$ | F53 P5(a) |
| what F53 says about strong CP | *"a separate phase in the gluon sector (F43), untouched here"* | — | F53 §Remaining, item 2 |

The number is real and correct; it is attached to the wrong object. This is the same shape as B12's Amendment 7 — a row whose residual was an accounting statement rather than a physics one.

The one-generation piece of F53 *is* relevant, but to $\bar\theta$'s **second** term, and this finding records it there (§5).

---

## 2. The premise: the loop set is closed under reversal (T0)

`lpt_bcc_vertex._loops_bcc` enumerates each minimal rhombus in **both senses**: 6 spatial orientations $\times$ 2 and 4 temporal $\times$ 2 = **20** oriented minimal loops. Checked combinatorially, up to translation and cyclic rotation of the based word:

| leg | statement | result |
|---|---|---|
| T0a | all 20 BCC minimal loops have their reverse in the set | 0 missing |
| T0b | the hypercubic reference set (12) likewise | 0 missing |

T0b matters: it makes T0a a measured property rather than a BCC accident, through the same code path.

**This is the load-bearing input, and it is what the first control removes.**

---

## 3. Reality, non-perturbatively (T1, T3)

$S=-\sum_\text{loops}\operatorname{Tr}U_\text{loop}$ is computed and returned **complex** — never `Re()`-projected — so $\operatorname{Im}S$ is a measurement. On three Haar-random SU(3) configurations, $4^4$ sites, five link fields (4 spatial $\langle111\rangle$ axes + Euclidean time):

| leg | statement | result |
|---|---|---|
| T1a | $\operatorname{Im}S=0$ — **and in Euclidean signature this *is* $\theta_\text{QCD}=0$**, non-perturbatively | $1.2\times10^{-14}$ |
| T1b | the configurations are genuinely disordered ($\operatorname{Re}S$ far below its ordered limit) | 0.9970 |
| T1c | $S$ is CP-invariant | $2.9\times10^{-14}$ |
| T1d | $S$ is P-invariant | $3.2\times10^{-14}$ |
| T3a | both projections are exact: $\sum_i d_id_i^{\mathsf T}=4I$ (4 $\langle111\rangle$ temporal rhombi), $M^{\mathsf T}M=4I$ (6 $\langle110\rangle$ spatial) | `0.0`, `0.0` |
| T3b | the clover $Q=\sum_a\mathbf E^a\!\cdot\!\mathbf B^a$ is **non-zero** | 2.078 |
| T3c | injecting $\theta$ by hand gives $\operatorname{Im}S = -\theta\sum Q$ **exactly**, over $\theta\in\{0.1,0.3,-0.7,2.0\}$ | `0.0` |
| T3d | $S$ invariant under $U\to U^*$; the one-sense loop functional **odd** under it | $2.5\times10^{-14}$; **`0.0`** |

T3b and T3c are the non-vacuity legs and they are not optional. Without them "$\operatorname{Im}S=0$" could be a statement about an operator this lattice does not carry. T3c settles it the strongest way available: the *slope* of $\operatorname{Im}S$ in $\theta$ is exactly the topological charge, so T1a has full sensitivity and its zero is a measurement.

T3d is the exact discrete-symmetry face. $U\to U^*$ needs no point-group bookkeeping, which is why it and not parity carries the load — see §7.

---

## 4. Reality perturbatively, hence at every loop order (T2)

$V(-k)=\overline{V(k)}$ for all $k$ is equivalent to every position-space coefficient being real, which is the cheaper and stronger form. Sampling axis tuples **and colour indices**:

| leg | statement | $\max\lvert\operatorname{Im}c\rvert$ |
|---|---|---|
| T2a | 2-point, BCC rhombic action | **`0.0`** |
| T2b | 3-point — the vertex the 2026-06-29 audit's G1 caveat named as unanalysed | **`0.0`** |
| T2c | 4-point | **`0.0`** |
| T2d | 3-point, hypercubic reference path | **`0.0`** |
| T2e | sampled coefficients are $O(1)$ and the samples are non-empty | 0.5 / 0.5 / 0.25 |

**The loop statement.** Functions obeying $V(-k)=\overline{V(k)}$ are closed under products, and under integration of an internal momentum with a $q\to-q$ symmetric measure. The propagator is the inverse of a 2-point function in the same class. Therefore every term the loop expansion builds is in the class, the effective action $\Gamma$ is real in position space, and **no loop at any order generates an imaginary part** — i.e. no loop generates $\theta$. That is the audit's item, and it is closed by a closure property rather than diagram by diagram.

**The audit's G1 caveat, specifically.** It worried that the SU(3) self-coupling might carry a chiral component that the free-propagator argument missed. Two things answer it. (i) The self-coupling's vertices are objects in **colour** space with no spinor index at all, so "branch structure" is not a property they can have; branch sensitivity can only enter through a quark loop, and the quark colour current is vector-like. (ii) Independently of that, whatever the vertices are, they are **real** — T2b/T2c — and reality is what forbids $\theta$.

---

## 5. The fermion side, and where the problem actually lives (T5)

The physical invariant is $\bar\theta = \theta + \arg\det M_q$.

| leg | statement | result |
|---|---|---|
| T5a | at one generation $\arg\det M_q$ is independent of the F27 phase over $\{0,\pi/3,\pi/2,2,\pi\}$ | $1.5\times10^{-17}$ |
| T5b | and it is not merely constant, it is **zero** | `0.0` |
| T5c | $\bar\theta=\theta_\text{QCD}+\arg\det M_q$; first term closed, second **open (E6/E7)** | recorded |

A correction to how F53's number is usually quoted: F53 gives the off-diagonal **product** $(ime^{+i\theta})(ime^{-i\theta})=-m^2$. The determinant of an off-diagonal $2\times2$ is *minus* that product, so $\det=+m^2$ and $\arg\det M=0$ — not merely $\theta$-independent. So at one generation $\bar\theta = 0+0$ exactly, and the two zeros come from different places: $\theta_\text{QCD}$ from §3–§4, $\arg\det M_q$ from here.

At three generations $\arg\det M_q$ is set by the quark mass texture, which is open-derivations **E6** (6 quark masses) and **E7** (4 CKM parameters). Nothing here closes it, and the honest reading of the row is in §6.

---

## 6. What changes in the ledger, stated narrowly

$\theta_\text{QCD}$ was ledger parameter **#19**, an independent input. It is no longer independent: the rule fixes it at zero, and the entire strong-CP question becomes a **function of the quark mass texture**. That is a parameter-count result — one input removed, no new one added — and it is *not* a prediction of $\bar\theta$'s value, because the texture is not derived.

Two ways this could still be wrong, both nameable:

1. **The action fork.** `lpt_bcc_vertex`'s HONEST SCOPE says the F26 rotation law and the rhombic plaquette action agree in the continuum and **disagree at finite momentum**, and does not choose. So §3–§4 are statements about one branch. Block T4 runs the parity argument on the other: the F26 **even** law is P-even (T4a, `0.0`) while the retained **chiral** law is not (T4b, 1.98), and F91's *"gluon even (forced)"* is what puts the rule on the P-even branch. $\theta\,\mathbf E\!\cdot\!\mathbf B$ is P-odd, so it is excluded on that branch too. The conclusion survives the fork instead of presupposing its resolution — but "survives on both branches" is weaker than "derived on the settled branch", and the fork is still open.
2. **Non-perturbative $\theta$-vacua.** §4 is an all-orders statement about the loop expansion; §3 is configuration-by-configuration and so is not perturbative at all. Neither addresses whether the rule's Hilbert space carries distinct $\theta$-sectors that a real action could still select between. That is not measured here.

---

## 7. Measured and deliberately **not** used

The clover's finite-$a$ parity eigenvalue. `parity_map` is an exact symmetry of the action (T1d, $3.2\times10^{-14}$), but the reconstructed clover $Q$ does **not** map to $-Q$ under it at finite lattice spacing: the relative defect measured 0.42–0.83 and **does not fall** as the field weakens (field scale 1.0 → 0.03), and no match exists under orientation-permutation with sign and translation either. So the familiar *"$\mathbf E\!\cdot\!\mathbf B$ is P-odd"* is used here as a **continuum** statement only, and every load-bearing leg rests on reality / $U\to U^*$ instead. Making the rhombic clover a parity eigenstate at finite $a$ is open, and is the natural next step for this module.

Recording this is the point: the first draft of this finding had P-oddness of $Q$ as a load-bearing leg, and it is false at finite $a$.

---

## 8. The controls, and what the second one found

Three declared controls, **disjoint** measured red sets — each of the three results rests on a different object:

| control | perturbation | reddens | why |
|---|---|---|---|
| 1 | `reverse_senses=false` | T1a, T1c, T1d, T3d | drop the reversed half of the loop set and $\operatorname{Im}S\ne0$: reality is a property of the **loop set** |
| 2 | `vertex_one_sense=true` | T2b, T2c | the same structural input on the **vertices**, reached independently |
| 3 | `flat_links=true` | T1b, T3b | with identity links there is nothing to measure: the **non-vacuity** legs must fail |

**Control 2 found a defect in this finding's own first draft.** The first `vertex_reality_defect` sampled momenta at `lpt_bcc_vertex.terms`'s hardcoded colour assignment $[T^0,T^1,T^2]$, and under control 2 it stayed **green** — the one-sense loop set passed a reality test while its action's imaginary part was a plainly visible $O(A^3)$ (measured: field scale halved ⇒ $\operatorname{Im}S$ down $\times0.09$). The imaginary part lives in the antisymmetric $f^{abc}$ structure, which a fixed-index probe cannot see. `_terms_colour` samples colour indices, and control 2 now reddens T2b/T2c as it should. This is exactly the failure mode D9/H2 exists to catch, and it was caught by the mechanism rather than by review.

---

## 9. Exactness

- **Literal `0.0`:** vertex coefficient reality at 2, 3, 4 legs (T2a–c) and on the hypercubic path (T2d); the $\theta$-linearity of $\operatorname{Im}S$ (T3c); the oddness of the one-sense functional under $U\to U^*$ (T3d); the two $4I$ projections (T3a); the even-law parity defect (T4a).
- **Exact combinatorics:** reversal closure of the 20-loop and 12-loop sets (T0a/T0b).
- **Machine precision:** $\operatorname{Im}S$ $1.2\times10^{-14}$; CP and P invariance of $S$ $2.9$/$3.2\times10^{-14}$; $\arg\det M_q$ spread $1.5\times10^{-17}$.
- **Not exact, and named:** the action fork (§6.1), non-perturbative $\theta$-sectors (§6.2), the clover parity eigenvalue at finite $a$ (§7), and $\arg\det M_q$ at three generations (§5).
