# F172 — Is the one shared IR residual an *algebraic connection* or a *computed number*? A wide review: the "one number" is one IR fixed-point coupling dressed by exact lattice geometry, and the algebraic hypothesis splits cleanly — **well-motivated for the SHAPE residual** ($3\delta^*=Q$, with an exact $\pi/4$ anchor and a self-consistency structure), **weak for the SCALE/scheme residual** (which matches computed nonperturbative QCD quantities)

**Date:** 2026-06-29 - 21:40
**Numbering:** F171 taken by a concurrent session; this is **F172** (re-checked).
**Status:** Analysis / reframing (no new physics input; a structural verdict on an open problem) — 4/4 checks PASS. **What this establishes:** (i) the recurring "one nonperturbative residual" is **not one number** — its members are manifestly distinct values that are different *functions* of one IR fixed-point coupling $\alpha_\text{eff}^*$ plus **exact** lattice geometry; (ii) the algebraic-connection question therefore separates into a **SHAPE** residual (the lepton-condensate angle $3\delta^*$ / $\lambda_6$) and a **SCALE/scheme** residual ($\Lambda$ ratio, $q_\ast$, $d_1$, $\sqrt\sigma/f_\pi$), with **opposite** prospects; (iii) the shape residual has a genuine path to an exact algebraic value — an **exact $\pi/4$ anchor** at $m_e=0$ (F96), a **self-consistency** structure (the F92 method that already derived $45°$, $Q=2/3$, $\sqrt2$ exactly), and the target $3\delta^*=Q=\tfrac23$ rad (F150/F164); (iv) the scale/scheme residual looks **computed/transcendental** — it matches real-QCD quantities ($\hat\alpha(0)/\pi=0.97$, Deur–Brodsky–Roberts) that are measured, not algebraic, and its residual digit lives in the action-specific finite vertex constant $d_1$ that the F155 moment-insensitivity theorem makes non-algebraic. **Recommendation: stop treating them as "one number"; attack the shape angle as a self-consistency fixed point and the scheme constant as a separate computed integral.**
**Script:** `tests/findings/test_F172_residual_algebraic_or_computed.py` (~1 s, stdlib)
**Results:** `test-results/F172_residual_algebraic_or_computed.json`
**Cross-references:** [[F150-eg-sextic-brake-from-architecture]] (the "one residual cluster" framing this audits; the $3\delta^*=\cos Q$ target), [[F164-lambda6-derivation-attempt-and-relabel]] (the prior $\lambda_6$ attempt — found *not* a clean rational; both bracket rationals fail), [[F96-second-shell-Eg-gap-saturation]] (the **exact $3\delta=\pi/4$ at $m_e=0$** anchor), [[F92-per-constituent-phase-consistency]] (the self-consistency method that yields exact $45°$, $Q=2/3$, $\sqrt2$ — the template for an algebraic shape residual), [[F95-B-derived-C-localized]] ($B=-3\sqrt2 I_2\bar y^4$, $I_2=\langle\cot\omega\rangle_\text{BCC}=0.2202$ — a lattice constant), [[F145-route-c-induced-njl-coupling]] (Fierz $\tfrac29$ exact; $\alpha_\text{eff}^*$ nonperturbative), [[F151-scheme-constant-determined]]/[[F155-qstar-self-energy-and-freeze-bracket]]/[[F162-bgfield-self-energy-b0-gate]]/[[F163-wilson-lattice-selfenergy-vertices-28p81-gate]] (the scale/scheme constant; tadpole-free; $C_{\overline{\rm MS}}=131/66$ rational; $d_1$ moment-inaccessible), [[F152-ir-coupling-the-irface]]/[[F154-residuals-A-B-built-and-solved]] ($\alpha_\text{eff}^*\approx0.39$), [[F144-route-a-alpha-s-dimensional-transmutation]]/[[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]]/[[F170-lepton-colour-scale-link]] (the other cluster members). Roadmap: `docs/roadmaps/mass-magnitude-derivation-2026-06-29.md`.

---

## 1. The question

The roadmap (and F150) reduce the whole open magnitude/shape problem to "one nonperturbative IR number" shared across $\lambda_6$ (lepton brake), $\cos3\delta^*$ (condensate angle), $G/G_c$ (χSB point), $\sqrt\sigma/f_\pi$, the $\Lambda$ scheme constant, $\alpha_\text{eff}^*$ (IR coupling), $q_\ast/d_1$, and the lepton↔colour scale $O(1)$ (F170). **Could this be fixed by an exact mathematical/algebraic connection rather than a single computed number?** This finding reviews every member and gives a structural verdict.

## 2. The cluster is *not* one number — it is one coupling + exact geometry (C1)

The members are manifestly distinct values:

| member | value | finding |
|---|---|---|
| $\lambda_6$ ($E_g$ brake) | $0.243$ | F118/F150 |
| $\alpha_\text{eff}^*$ (IR coupling) | $\approx0.39$ | F152/F154 |
| $G/G_c$ (χSB point) | $1.277$ | F77/F145 |
| $\Lambda$ scheme ratio | $\approx1.78$ | F144/F151 |
| $\cos3\delta^*$ (angle) | $0.785874$ | F93/F150 |
| $m_\tau/\Lambda$ (scale $O(1)$) | $\approx3.4$ | F170 |

They cannot be "one number." What is shared is one *object* — the IR fixed-point coupling $\alpha_\text{eff}^*$ (the dual-Meissner-gap saturation value, F152) — and each member is a different **function** of $\alpha_\text{eff}^*$ dressed by **exact** lattice quantities (the Fierz $\tfrac29$, $I_2=\langle\cot\omega\rangle_\text{BCC}$, the $E_g$ second-shell harmonics, the V-scheme $a_1=\tfrac{11}3$). So the algebraic-connection question is really two questions: *(a) is $\alpha_\text{eff}^*$ algebraic?* and *(b) are the geometric dressings algebraic?* — and these have different answers for the shape vs the scale members.

## 3. The SHAPE residual: a genuine path to algebraic (C2, C3)

The lepton-condensate angle $\delta^*$ (equivalently $\lambda_6$, via $\cos3\delta^*=-B/2C$ with $B$ derived, F95) has three properties that point to an exact value:

1. **An exact algebraic anchor (F96, C2).** In the massless-electron texture $(m_h,m_\text{mid},0)$, Koide $Q=\tfrac23\iff 3\delta=\pi/4$ **exactly** ($\cos3\delta=1/\sqrt2$, sympy-exact). The physical angle $3\delta^*=38.2°$ is a *displacement* off this exact point carried by $m_e>0$.
2. **A self-consistency structure.** That displacement is set by $m_e$, which is itself set by the spectrum the angle generates — a fixed-point condition, the **same kind** the model has *already solved exactly*: F92 derived $45°$, $Q=2/3$, and the Fock $\sqrt2$ as unique consistency fixed points, **not** as computed constants. The model's track record is that its "residuals" in the *generation/condensate-geometry* sector keep collapsing to exact algebraic points.
3. **The target $3\delta^*=Q=\tfrac23$ rad (C3).** The physical angle satisfies $3\delta^*=Q$ to $2.1\times10^{-5}$ and $\cos3\delta^*=\cos(2/3)$ to $1.3\times10^{-5}$, tying the open shape residual to the **already-exact** Koide $Q=2/3$ (F92). *Caveat:* this equates a radian angle to a dimensionless ratio — dimensionally permissible but unusual; it is a target with a rationale (both are invariants of the same saturated $E_g$ condensate), not yet a theorem (F150/F164). The competing exact value $\pi/4=0.7854$ is numerically near $\cos(2/3)=0.7859$; only the self-consistency solve can decide which (if either) is exact.

**Assessment (shape): well-motivated.** A serious attempt should treat $3\delta^*$ as a self-consistency fixed point with the **exact F96 boundary condition** ($3\delta=\pi/4$ at $m_e=0$) — the same machinery that made $45°$/$Q$/$\sqrt2$ exact. If it closes, $3\delta^*=Q$ becomes a theorem and $\lambda_6$ follows algebraically, with *no* nonperturbative computation.

## 4. The SCALE/scheme residual: looks computed/transcendental (C4)

The other half — $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}$, $q_\ast$, $d_1$, $\sqrt\sigma/f_\pi$ — is a renormalization scheme-matching constant. Here the evidence runs the other way:

- **The model removes the *large* transcendental piece.** The rule is tadpole-free ($u_0\equiv1$), so Wilson's $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ is *structurally absent* (F151/F155); the ratio is $O(1)\approx1.78$. The continuum $\overline{\rm MS}$ constant is even **rational**, $C_{\overline{\rm MS}}=131/66$ (F163). This is the strongest in-model evidence *for* algebraicity of the scale residual.
- **But the residual digit is the computed kind.** What remains is the finite vertex constant $d_1$, and the F155 **moment-insensitivity theorem** proves the shift from the band top $q_\ast a\approx0.97$ to the implied $0.733$ lives entirely in the action-specific 3-gluon+ghost form-factor finite part — *not* accessible to any moment integral. That is exactly the structure of a computed lattice-PT constant (the Hasenfratz integral), generically transcendental.
- **Real-QCD analogues are computed, not algebraic.** The closest physical object — the process-independent IR fixed point $\hat\alpha(0)/\pi=0.97(4)$ with gluon mass $m_0=0.43(1)$ GeV (Deur–Brodsky–Roberts; Cui *et al.*) — is a *measured/computed* number with error bars. Only **Banks–Zaks** (perturbative conformal-window) fixed points are algebraic (the coupling is a ratio of $\beta$-function coefficients); the model's IR coupling is a **gap/saturation** value (dual Meissner), *not* a Banks–Zaks zero, so the algebraic route is not available unless the gap self-consistency happens to saturate at an exactly-determined point.

**Assessment (scale): weak.** Likely a computed $O(1)$. The one escape is if $\alpha_\text{eff}^*$ is pinned by an exact gap self-consistency — worth checking, but no current evidence.

## 5. Verdict

> **The algebraic-connection hypothesis is well-motivated for the SHAPE residual and weak for the SCALE/scheme residual.** They are different functions of one IR coupling, and conflating them as "one number" (F150) hides that one half may be exactly algebraic while the other is a computed constant.

The single most promising concrete target: **derive $3\delta^*$ as a self-consistency fixed point** (F92 method) anchored on the exact $3\delta=\pi/4$ at $m_e=0$ (F96). Success makes $3\delta^*=Q$ a theorem and $\lambda_6$ algebraic; it would *not* close the scheme constant, which should be pursued separately as the (probably transcendental) lattice integral F162/F163 are already computing.

This also sharpens F150's "one number owns all": the *coupling* is shared, but the **shape dressing is plausibly algebraic** (geometry + self-consistency) while the **scale dressing is plausibly computed** (scheme matching). The two open problems are not the same problem.

## 6. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| C1 | cluster members are distinct (spread $>1$) ⇒ one coupling + geometry, not one number | PASS | structural |
| C2 | exact shape anchor (F96): $3\delta=\pi/4$, $\cos3\delta=1/\sqrt2$ at $m_e=0$ | PASS | exact |
| C3 | shape target $3\delta^*=Q=\tfrac23$ rad to $2.1\times10^{-5}$; $\cos3\delta^*=\cos(2/3)$ to $1.3\times10^{-5}$ | PASS | target |
| C4 | scale residual: rational pieces ($11/3$, $131/66$, $2/9$, $1/4$, $1/16\pi$) exact, but digit $=d_1$ (moment-inaccessible, computed); QCD analogue $\hat\alpha(0)/\pi=0.97$ measured | PASS | assessment |

**Overall 4/4 PASS.**

## 7. Honest scope

- This is an **analysis/reframing** finding: it introduces no new physics input and does not perform the saturated-condensate solve. Its content is the structural split (shape vs scale), the catalogue of which pieces are already exact rationals, and the verdict on where algebraicity is plausible.
- The $3\delta^*=Q$ "target" is exactly that — F150/F164 flag it as a target with a rationale, and the radian-angle-equals-ratio form means only the self-consistency solve can confirm it. This finding does not upgrade it to a theorem; it argues it is the *right place to try*.
- "Algebraic" here means expressible in closed form from the model's exact constants ($\pi$, $\sqrt2$, small rationals, $I_2$); it does not assert *rational*. F164's result that $\lambda_6$ is not a clean rational is consistent with an algebraic-but-irrational value (e.g. via $\cos(2/3)$ or $I_2$).

## 8. Provenance

- **New:** the structural decomposition "one coupling + exact geometry" with the explicit distinct-values table; the shape/scale split of the algebraic hypothesis; the identification of the exact F96 $\pi/4$ anchor and the F92 self-consistency template as the route for the shape residual; the external grounding that the scale residual matches *computed* (not algebraic) QCD quantities and only Banks–Zaks fixed points are algebraic.
- **Reused:** F96 exact texture algebra; F92 fixed-point method; F95 $B$/$I_2$; F150/F164 the $3\delta^*=Q$ target and the $\lambda_6$ non-rational result; F151/F155/F162/F163 the tadpole-free scheme constant and $131/66$; F152/F154 $\alpha_\text{eff}^*$; PDG lepton masses.
- **External:** process-independent IR fixed point $\hat\alpha(0)/\pi=0.97(4)$ (Deur–Brodsky–Roberts; Cui *et al.*, [arXiv:1801.10164](https://arxiv.org/pdf/1801.10164), [arXiv:1912.08232](https://arxiv.org/pdf/1912.08232)); Banks–Zaks conformal-window fixed points algebraic in the conformal expansion ([arXiv:2008.12223](https://ar5iv.labs.arxiv.org/html/2008.12223)); Koide $Q=2/3$ empirically exact, underived ([Koide overview](https://johncarlosbaez.wordpress.com/2021/04/04/the-koide-formula/)).
- **Verification:** `tests/findings/test_F172_residual_algebraic_or_computed.py` (2026-06-29, 4/4 PASS), results `test-results/F172_residual_algebraic_or_computed.json`. Stdlib only — numpy-safe.
