# F253 — E1: the weight→phase principle behind $\delta^*=\tfrac29$ rad **reduces to one named normalization** (POSIT-N: the $E_g$ generator norm) and the **topological escape is excluded** — the only $E_g$ holonomy on the BCC 2nd shell is $2\pi/3$, and $\tfrac29$ is a representation multiplicity, not a holonomy

**Date:** 2026-07-16 - 16:55
**Numbering:** frontier was F252 (F248–F252 = concurrent QED/graviton batch); this is **F253**. Attempts open-derivations **E1** (the last deep EW/lepton target; `open-derivations-prompts-v2.md` Part 3).
**Status:** Confirmed (negative / sharpened, with a new exclusion) — 5/5 checks PASS. **What this does:** takes the two routes the E1 prompt names — *saturation equipartition (F92)* and *a BCC 2nd-shell topological-moment computation* — and runs both to a definite conclusion. (A) The equipartition route **collapses the whole "weight→phase" residual to a single named posit**, POSIT-N: *the $E_g$ order-parameter generator is unit-normalized so the full-bilinear democratic phase budget equals one radian*. Given POSIT-N (and unit amplitude), $\delta^*=\tfrac29$ rad follows **exactly**; without it $\delta=\text{(weight)}\times R$ is scale-degenerate. POSIT-N is **not** supplied by any $O(1)$ saturation amplitude. (B) The topological route **closes negative and, more usefully, excludes itself**: the only genuine $E_g$ **holonomy** the BCC 2nd shell produces is $2\pi/3$ (a rational multiple of $\pi$); $\tfrac29$ enters *only* as a representation **multiplicity** $\dim E_g/\dim(T_{1u}\otimes T_{1u})$, which is scale-free and therefore cannot *be* a radian without the same POSIT-N. $\tfrac29$ rad is not any low-order symmetry-quantized phase $2\pi p/q$. **Net:** E1 does not close positive, but F230's vague "a radian needs a missing dynamical scale" is now **named concretely** (the $E_g$ generator normalization) and the one route that could have delivered $\tfrac29$ *scale-free* (a topological moment) is **ruled out**. This converges with F179 (induced-coupling), F199 (BPS) and F230 (crystal-field) — four independent routes, one terminus.
**Script:** `ca-simulation/derive_weight_as_phase.py` (analysis; sympy exact + real numpy, no chiral transforms)
**Test:** `tests/findings/test_F253_weight_as_phase_scale_nogo.py` (5/5, <4 s)
**Results:** `test-results/F253_weight_as_phase_scale_nogo.json`
**Cross-references:** [[F175-lattice-2-9-eg-weight]] (derives the *number* $\tfrac29$ as the exact $E_g$ weight and flags this exact residual — "why the saturated condensate phase in radians equals the representation weight"), [[F230-lepton-angle-geometric-nogo]] (the crystal-field no-go and the radian-vs-ratio framing this sharpens and names), [[F199-angular-self-duality-derivation-forced-posit]] (the BPS-route structural no-go; $Q$ is $\delta$-blind ⇒ no second kinematic relation), [[F179-lambda6-derivation-attempt-and-relabel]] (the induced-coupling relabel), [[F92-per-constituent-phase-consistency]] (the equipartition template — $45°$/$\sqrt2$ from two mass laws — extended here to the generation azimuth), [[F234-Wvc-triple-closed-delta-2-9-pins-brake]] (E4 ⊂ E1: given this angle, $\lambda_6=0.243$ is pinned — so this is the *last* EW/lepton open item), [[F96-second-shell-Eg-gap-saturation]] (the exact massless endpoint $3\delta=\pi/4$), [[F49-bcc-finite-k-weinberg-angle]] (the parallel gauge $\tfrac29$ as a *ratio*, dimensionally distinct from a radian). External: Brannen circulant $\delta=0.2222220(19)$; ZIP "$\delta=\tfrac29$ as a difference of 3D topological moments" (assessed in §4).

---

## 1. The target, stated exactly

The charged-lepton spectrum is one angular Landau potential (F93/F95/F118)

$$F(\delta)=B\cos3\delta+C\cos^{2}3\delta,\qquad \cos3\delta^{*}=-\frac{B}{2C},$$

with $B<0$ derived (F95 sea loop, $B=-0.0569$) and $C=\lambda_6 e^{6}>0$ open. The data sit at $\delta^{*}=0.22223$ rad, i.e. $\delta^{*}=\tfrac29$ rad to $0.003\%$ ($3\delta^{*}=\tfrac23=Q$), where **$\tfrac29$ is the exact $E_g$ representation weight**

$$\frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\frac{2}{9}\qquad(T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g},\ 1{+}2{+}3{+}3=9)$$

— reproduced here by an independent $O_h$ character projection ($\mathrm{mult}_E=1$, check **W1**). The *number* is derived (F175). The open **principle** is the bridge: **why does the saturated-condensate phase, measured in radians, equal that dimensionless weight?** F230 sharpened the obstruction to a dimensional one — *a radian cannot equal a pure ratio without a scale*. This finding attacks the two routes the E1 prompt proposes to supply that scale.

## 2. Route A — saturation equipartition reduces E1 to one named posit (POSIT-N)

Model the generation order parameter as a unit vector $\Psi$ in the 9-dim Hermitian bilinear $T_{1u}\otimes T_{1u}$ (9 real dof), with the orthogonal channel split $\{A_{1g}{:}1,\,E_g{:}2,\,T_{1g}{:}3,\,T_{2g}{:}3\}$. "Saturation" is maximal democracy — $|\Psi_i|^2=\tfrac19$ on each basis state (max entropy on the 9-simplex, the direct analogue of F92's unitarity-filling wall). The $E_g$ channel then carries weight $\tfrac29$, exactly as in F175.

Turning that weight into the **azimuth** $\delta$ requires one extra statement, which we isolate as

> **POSIT-N.** The $E_g$ rotation generator is normalized so that a unit-amplitude democratic condensate sweeps unit arc-length per unit weight — equivalently, *the full-bilinear democratic phase budget is one radian.*

With POSIT-N (and unit amplitude $R=1$), the arc swept in the $E_g$ channel is $\text{weight}\times R=\tfrac29\times1$, so

$$\boxed{\ \delta^{*}=\tfrac29\ \text{rad (exact)}\ }\qquad\text{(check W3)}.$$

Without POSIT-N the same construction gives only $\delta=\tfrac29\,R$ with $R$ a free generator-norm/amplitude ratio — **scale-degenerate**, exactly F230's residual. So equipartition does **not** dissolve the obstruction; it *localizes* it: the entire weight→phase gap is the single constant $R$, and POSIT-N is the choice $R=1$.

**Is POSIT-N derivable from saturation?** No (check **W4**). $R=1$ is required, but no $O(1)$ combination of the saturation data — the amplitude $e\approx0.733$ (F92/F234), the Fock $\sqrt2$, the unitarity product $\sqrt2\,e^{2}=0.760$, $e^{2}=0.537$, $1/e=1.364$ — equals $1$. The radian is the scale-free angle unit itself; "budget $=1$ rad" is a normalization of the $E_g$ generator, not an output of the wall. This is the precise, named form of F230's "missing dynamical scale."

## 3. Route B — the topological escape is excluded

A genuine **topological moment** (winding number / holonomy) is *intrinsically* a phase (arc$/$radius), so if $\tfrac29$ rad arose as a holonomy it would beat the obstruction **without** POSIT-N. It does not.

Building the real $E_g$ basis $(d_{z^2},d_{x^2-y^2})$ on the six BCC 2nd-shell axis sites $\{\pm\hat x,\pm\hat y,\pm\hat z\}$ and acting with the body-diagonal $C_3$ (cyclic $x\!\to\!y\!\to\!z$), the induced rotation in the $E_g$ plane is **exactly $2\pi/3$** (check **W5**) — the origin of the $\cos3\delta$ invariant. This is the *only* genuine $E_g$ holonomy the shell supplies, and it is a rational multiple of $\pi$ ($\tfrac13$ of a turn). The number $\tfrac29$ appears **only** as a representation multiplicity (a dimension ratio), which carries no intrinsic radian scale. And $\tfrac29$ rad $=0.2222$ is **not** any low-order symmetry-quantized phase $2\pi p/q$ ($q\le24$; nearest is $2\pi/28=0.2244$, neither equal nor symmetry-natural). Any *difference* of such holonomies is still a multiple of $2\pi/3$; any difference of *multiplicities* is still dimensionless. **A lattice holonomy equal to $\tfrac29$ rad does not exist.**

## 4. The external ZIP "topological moment" claim, assessed

The ZIP write-up derives $\delta=\tfrac29$ as a *difference of 3D topological moments*. §3 shows why this is not a counterexample in-model: a moment difference is a dimensionless integer/rational, so its identification with a **radian** re-imports exactly POSIT-N. ZIP obtains the *number* $\tfrac29$ (consistent with the $E_g$ weight of §1) but not a scale-free radian; it is the topological *restatement* of the weight, not a derivation of the weight-as-phase bridge.

## 5. What moved

- **New:** the equipartition residual is reduced from a conjecture to **one named constant** — POSIT-N, the $E_g$ generator normalization ($R=1$) — and shown non-derivable from the saturation data (§2, W3/W4). The **topological route is excluded** by an explicit BCC-2nd-shell holonomy computation ($2\pi/3$ only) plus a quantized-phase sweep (§3, W5): the one mechanism that could have supplied a *scale-free* $\tfrac29$ rad is closed. The ZIP claim is placed (§4).
- **Reused:** F175 ($\tfrac29$ = $E_g$ weight; here re-derived independently), F92 (equipartition template), F230/F199/F179 (the three prior no-gos this converges with), F49/F93/F95/F96/F118/F234 (the surrounding structure).
- **Status of $\delta^{*}=\tfrac29$:** a Koide-confidence **target** ($-0.89\sigma$; spectrum to $\le0.007\%$ once granted, F175/F234), whose derivation now reduces to **one** first-principles input — a lattice reason for $R=1$ (the $E_g$ generator norm). Four independent routes (crystal-field, BPS, induced-coupling, equipartition/topological) reach this same single missing input.

## 6. Check summary (`test_F253_weight_as_phase_scale_nogo.py`, 2026-07-16 - 16:55)

| # | Statement | Tier | Result |
|---|---|---|---|
| W1 | $\dim E_g/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ ($O_h$ projection, $\mathrm{mult}_E=1$) | exact | PASS |
| W2 | measured azimuth $\delta_\text{meas}=\tfrac29$ rad to $<0.01\%$ | data/target | PASS |
| W3 | equipartition: POSIT-N $\Rightarrow\delta^{*}=\tfrac29$ rad exact; else $\delta=\tfrac29 R$ free | structural | PASS |
| W4 | POSIT-N ($R=1$) not supplied by any $O(1)$ saturation amplitude | negative | PASS |
| W5 | only $E_g$ holonomy $=2\pi/3$; $\tfrac29$ is a multiplicity, not a quantized phase | exclusion | PASS |

**Overall 5/5 PASS** (<4 s).

## 7. Verdict

E1 **does not close positive**. The saturation-equipartition route reproduces $\delta^{*}=\tfrac29$ rad *exactly* but only after one explicitly named normalization — POSIT-N, the $E_g$ order-parameter generator norm ($R=1$, "democratic phase budget $=1$ rad") — which is not an output of the saturation dynamics. The BCC 2nd-shell topological-moment route is **excluded**: the lattice's only $E_g$ holonomy is $2\pi/3$, and $\tfrac29$ enters solely as a scale-free representation multiplicity, so no topological moment yields $\tfrac29$ *radians* without re-importing POSIT-N. The sharpened statement — *E1 = the single constant $R$ (the $E_g$ generator normalization); topological/scale-free origins are ruled out* — is the advance over F230, and it converges with F179/F199 on one terminus.

## 8. Provenance

- **New content:** the POSIT-N localization of the equipartition residual (§2); the explicit BCC-2nd-shell $E_g$-holonomy computation and quantized-phase exclusion (§3); the ZIP assessment (§4).
- **Reused:** F175, F92, F230, F199, F179, F49, F93/F95/F96/F118/F234. PDG masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86$ MeV).
- **Verification:** `tests/findings/test_F253_weight_as_phase_scale_nogo.py` (2026-07-16 - 16:55, 5/5 PASS), results `test-results/F253_weight_as_phase_scale_nogo.json`, script `ca-simulation/derive_weight_as_phase.py`. Real/exact arithmetic — numpy-safe.
