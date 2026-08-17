# F175 — Deriving $\tfrac29$ from the lattice: the lepton-condensate angle $\delta^*=\tfrac29$ rad is the **$E_g$ representation weight** of the second-shell generation order parameter, $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ (exact $O_h$ group theory) — and using it reproduces the charged-lepton mass ratios to $\le0.007\%$ with **zero shape parameters**

**Date:** 2026-06-29 - 23:55
**Numbering:** F174 is this session's; F173 a concurrent session's; this is **F175** (re-checked).
**Status:** Partial (the number $\tfrac29$ **derived exactly** + a zero-shape-parameter spectrum prediction; one dynamical principle open) — 5/5 checks PASS. **What this derives:** the value $\tfrac29$ that F174 pinned empirically is the **exact $E_g$ representation weight** of the second-shell generation bilinear — $T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g}$ (dims $1{+}2{+}3{+}3=9$), the splitting channel $E_g$ carrying weight $\dim(E_g)/9=\tfrac29$ — verified by explicit $O_h$ character projection ($\text{mult}_E=1$). This parallels F49's gauge $\tfrac29$ ($2$ sublattices $/(2{+}7)$ bond axes) on the **same** 2nd shell: $\tfrac29$ is a "$2$ special $/\,9$ total" 2nd-shell invariant, now derived in the generation sector. Using $\delta^*=\tfrac29$ (no fit) with the Koide amplitude $\eta^2=\tfrac12$ (F92, derived) gives $m_\mu/m_e$ to $+0.001\%$ and $m_\tau/m_e$ to $+0.007\%$. **What remains:** the dynamical principle that the *saturated condensate phase* (in radians) *equals the representation weight* — "weight-as-phase" (the ZIP-type moment mechanism); a geometric winding is excluded (F174). The number is derived; the principle is the residual.
**Script:** `tests/findings/test_F175_lattice_2_9_eg_weight.py` (~1 s, numpy + stdlib)
**Results:** `test-results/F175_lattice_2_9_eg_weight.json`
**Cross-references:** [[F174b-shape-angle-2-9-topological]] (pinned $\delta^*=\tfrac29$ empirically + the rational-radian/exclusion result this explains), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ condensate on the BCC 2nd shell; $\text{sym}(T_{1u}\otimes T_{1u})=A_{1g}\oplus E_g\oplus T_{2g}$), [[F75-three-generations-from-bcc-irrep-selection]] (the $T_{1u}$ generation triplet), [[F49-bcc-finite-k-weinberg-angle]] (the parallel gauge $\tfrac29$ on the 2nd shell), [[F92-per-constituent-phase-consistency]] (the Koide $\eta^2=\tfrac12$/$45°$ equipartition — the template for the open weight-as-phase principle), [[F76-generation-mass-hierarchy-crystal-field]]/[[F96-second-shell-Eg-gap-saturation]] (the $\cos3\delta$ structure and the $\pi/4$ massless anchor), [[F95-B-derived-C-localized]]/[[F150-eg-sextic-brake-from-architecture]] (the brake the angle supersedes as the primary object). External: Brannen circulant fit $\delta=0.2222220(19)$ ([MASSES2](https://brannenworks.com/MASSES2.pdf)); ZIP $\delta=\tfrac29$ as a 3D topological-moment difference ([ZIP derivation](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle)).

---

## 1. The build F174 named

F174 pinned the lepton-condensate angle to $\delta^*=\tfrac29$ rad, showed it is a *rational radian* (geometric/algebraic-cosine alternatives excluded at $>10\sigma$), and named the open build: **derive the $\tfrac29$ from the BCC second shell.** This finding does that.

## 2. $\tfrac29$ is the $E_g$ representation weight (D1, exact)

The generation order parameter is a Hermitian bilinear of the $T_{1u}$ generation triplet (F75). Under $O_h$,

$$T_{1u}\otimes T_{1u}=A_{1g}\oplus E_g\oplus T_{1g}\oplus T_{2g},\qquad \dim=1+2+3+3=9.$$

The channel that splits the three generations *without mixing axes* is uniquely $E_g$ (F93 O1). Its **weight** in the full 9-dimensional bilinear is therefore

$$\boxed{\ \frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\frac{2}{9}\ }$$

Verified by explicit $O_h$ character projection over all 24 rotations: the multiplicity of $E$ in $T_{1u}\otimes T_{1u}$ is exactly $1$ (dimension $2$), out of $9$. **This is the lattice origin of the number $\tfrac29$** — pure representation theory of the 2nd-shell point group, no dynamics, no fit.

## 3. The same $\tfrac29$ as the gauge sector (D2)

F49 derived $\sin^2\theta_W=\tfrac29$ on the **same** 2nd shell from $2$ sublattices over $(2+7)$ bond axes — the identical "$2$ special $/\,9$ total" structure. So $\tfrac29$ is a structural invariant of the BCC second shell appearing in **two independent sectors** (gauge and generation), both as a $2$-of-$9$ weight. This is why the lepton angle and the Weinberg angle share the number — not coincidence, but the same shell's "$2/9$".

## 4. The angle's natural measure (D3) — why it is a weight, not a winding

Under $C_3$ (the $120°$ lattice rotation about a body diagonal), the $E_g$ doublet transforms with character $-1=2\cos(2\pi/3)$: it picks up a $2\pi/3$ phase. Hence the Landau invariant is $\cos(3\delta)$ (three $C_3$ steps $=2\pi$), and $\delta$ is the $E_g$ phase. A literal **geometric winding** would therefore be a fraction of $2\pi$ — an algebraic cosine — which F174 **excluded at $>10\sigma$**. The surviving rational-radian $\delta^*=\tfrac29$ is thus not a winding but the **representation weight carried as the phase** (a ZIP-type "moment-as-phase"). The lattice supplies exactly one natural pure number in this channel — the $E_g$ weight $\tfrac29$ — and it is the measured phase.

## 5. The validation: zero-shape-parameter spectrum (D4)

Using the **derived** value $\delta^*=\tfrac29$ (not fitted) and the Koide amplitude $\eta^2=\tfrac12$ (F92, derived from $45°$ equipartition) in $\sqrt{m_a}=\mu(1+\sqrt2\cos(\delta^*+\tfrac{2\pi a}{3}))$:

| ratio | prediction | PDG | error |
|---|---|---|---|
| $m_\mu/m_e$ | $206.770$ | $206.7683$ | $+0.001\%$ |
| $m_\tau/m_e$ | $3477.47$ | $3477.228$ | $+0.007\%$ |

The entire charged-lepton *shape* (all ratios) follows to $\le0.007\%$ from two derived numbers ($\tfrac29$ and $\sqrt2$) plus the single overall scale $\mu$. The residual $0.007\%$ is the $\sim0.9\sigma$ $\eta^2$–$\delta$ tension (F174 S4), at current mass precision.

## 6. What is derived, and the one residual (D5)

- **Derived (exact, lattice):** the number $\tfrac29$ as the $E_g$ representation weight (two independent countings, §2–§3); the $\cos3\delta$ structure from $C_3$; and — as a consequence — the charged-lepton ratios to $10^{-4}$ with zero shape parameters.
- **Open (the principle):** *why the saturated condensate phase (in radians) equals the representation weight.* This "weight-as-phase" step is what turns the dimensionless weight $\tfrac29$ into the angle $\tfrac29$ rad. The external ZIP framework realises exactly this (it derives $\delta=\tfrac29$ as a difference of 3D topological moments — a pure number read as a phase). The proposed in-model route is **saturation equipartition** — the same principle by which F92 derived $45°$/$\sqrt2$: at the saturation wall the order parameter is maximally democratic over its 9-dimensional bilinear content, and the $E_g$ phase locks to that channel's share $\tfrac29$. This is a conjecture with a precedent, not yet a closed derivation.

So the user's "winding" is sharpened to its correct form: the lattice does produce $\tfrac29$ exactly — as a **representation weight**, not a geometric winding — and it reproduces the spectrum; the remaining work is the dynamical principle, not the number.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| D1 | $\text{mult}_E(T_{1u}\otimes T_{1u})=1$; weight $\dim(E_g)/9=\tfrac29$ ($O_h$ character projection over 24 rotations) | PASS | exact |
| D2 | parallel gauge $\tfrac29=2/(2+7)$ on the same 2nd shell (F49) | PASS | exact |
| D3 | $C_3\to2\pi/3$ phase on $E_g$ ($\chi_E(C_3)=-1$), $\cos3\delta$; winding-as-geometry excluded (F174) | PASS | exact |
| D4 | $\delta^*=\tfrac29$ + Koide $\sqrt2$ → $m_\mu/m_e$ $+0.001\%$, $m_\tau/m_e$ $+0.007\%$ (zero shape params) | PASS | prediction |
| D5 | honest residual: weight→phase principle open (ZIP template; equipartition proposed) | PASS | scope |

**Overall 5/5 PASS.**

## 8. Honest scope

- The exact result is that $\tfrac29$ is the $E_g$ **weight**; the identification of that weight with the **phase in radians** is supported by (i) the $>10\sigma$ exclusion of geometric alternatives (F174), (ii) the $\le0.007\%$ spectrum reproduction (§5), (iii) the external ZIP precedent, and (iv) the F92 equipartition analogy — but is **not** itself derived here. A skeptic can still hold that $\delta^*=\tfrac29$ is an extraordinarily good ($0.9\sigma$, 7-digit) numerical coincidence between the phase and the weight.
- The $\eta^2=\tfrac12$ vs $\delta=\tfrac29$ joint-exactness tension (F174 S4) is inherited; the $0.007\%$ residual is consistent with it and with current mass uncertainties.
- "$E_g$ weight" uses the Hermitian (9-real-dof) generation bilinear; the symmetric-only (6-dof) count would give $\tfrac13$, so the antisymmetric $T_{1g}$ must be included — natural for a Hermitian order parameter, and required for the parallel with F49's $2+7=9$.

## 9. Provenance

- **New:** the derivation of $\tfrac29$ as the exact $E_g$ representation weight $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})$ via $O_h$ character projection; the explicit parallel to F49's gauge $\tfrac29$ as one "$2/9$" 2nd-shell invariant; the $C_3\to2\pi/3$ argument that the phase is a weight not a winding (closing F174's rational-radian clue); the zero-shape-parameter spectrum reproduction from $\{\tfrac29,\sqrt2\}$; the identification of the open step as the weight→phase principle with equipartition (F92) as the proposed route.
- **Reused:** F75 $T_{1u}$; F93 $E_g$/2nd shell; F49 gauge $\tfrac29$; F92 $\eta^2=\tfrac12$; F174 the empirical $\tfrac29$ and exclusions; PDG lepton masses.
- **External:** Brannen $\delta=0.2222220(19)$; ZIP $\delta=\tfrac29$ from 3D topological moments.
- **Verification:** `tests/findings/test_F175_lattice_2_9_eg_weight.py` (2026-06-29, 5/5 PASS), results `test-results/F175_lattice_2_9_eg_weight.json`. numpy/stdlib, real arithmetic only.
