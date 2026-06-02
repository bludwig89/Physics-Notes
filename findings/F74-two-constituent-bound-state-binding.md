# F74 — Dynamical two-constituent bound state: the binding depth, and why the F73 ceiling is robust

**Date:** 2026-06-01 - 18:30
**Status:** Confirmed (rigorous core) — 6/6 checks PASS; the 3D binding threshold matches the Watson integral to $1.7\times10^{-7}$ and the two independent bound-state methods agree to $1.3\times10^{-15}$. The **binding depth is produced as an explicit function $E_b(g)$**; the derivation is **complete up to one external number** (the contact coupling), which the model's gauge sector does not supply. 125 GeV is **not** conjured — the result is a quantified near-no-go for the simplest composite interpretation.
**Script:** `model-tests/test_F74_bound_state_binding.py` (~3 s, numpy only)
**Results:** `test-results/F74_bound_state_binding.json`
**Cross-references:** [[F73-spin0-bound-pair-scalar]] (the kinematic ceiling this completes), [[F69-paired-spinor-photon]] (the spin-1 sibling; this is the explicit "two-body binding dynamics" follow-up flagged there), [[F46-pythagorean-lattice-mass]] (the $m_\text{lat}=m_c c a/\hbar$ map), [[F64-em-connection-gravity]] (the $a\approx6.2\times10^{-35}$ m cell); McPhee notebook pp.5–6 (the "Cooper pair" / "negative binding energy").

---

## Goal

F73 derived the spin-0 bound pair's **kinematics** exactly ($m_H=\sin(\arcsin m_1+\arcsin m_2)\to 2m_c$) but left the **mass value** undetermined: it depends on the binding depth $E_b=(m_1+m_2)-m_H$, which is a *dynamical* quantity. This finding builds the dynamics — a real two-body bound-state solver — and produces $E_b$ as an explicit function of the interaction strength, then asks whether the model fixes that strength.

## The construction

In the rest frame (total momentum zero) the two-body problem reduces to a **one-body problem in the relative coordinate** on the 3-D cubic lattice, reduced mass $\mu=m_c/2$, hopping $t$, plus the minimal attractive channel — a single-site **contact well** of depth $g$. This is the lattice realisation of the NJL/BCS contact that pairs two spin-½ constituents into the spin-0 singlet (the same pairing F69 puts in the spin-1 channel for the photon):

$$H_\text{rel}=-t\!\!\sum_{\langle ij\rangle}\!|i\rangle\langle j|\;-\;g\,|0\rangle\langle0|,\qquad \varepsilon(\mathbf k)=2t\sum_{i}(1-\cos k_i)\in[0,12t].$$

The contact is **rank-1**, so the bound state below the band is the *exact* root of the Koster–Slater secular equation

$$1=g\left\langle\frac{1}{\varepsilon(\mathbf k)+E_b}\right\rangle_\text{BZ},\qquad E_b>0,\tag{$\ast$}$$

and the binding **onset** is the 3-D critical coupling

$$g_c=\frac{1}{\langle 1/\varepsilon(\mathbf k)\rangle_\text{BZ}}.\tag{$\ast\ast$}$$

## Results

**A — There is a real 3-D binding threshold (exact).** Unlike 1-D/2-D (where any attraction binds), in 3-D the BZ average $\langle1/\varepsilon\rangle$ is *finite* (the Watson integral), so a **minimum coupling is required to bind at all**:

$$g_c=\frac{2t}{W_3}=3.95678\,t,\qquad W_3=0.5054620\ldots$$

The quadrature (1/n Richardson-extrapolated, removing the $k=0$ integrable singularity) reproduces this to $1.7\times10^{-7}$.

**B — The binding-depth function $E_b(g)$.** Solving $(\ast)$ in the thermodynamic limit:

| $g/g_c$ | $E_b/t$ | | $g/g_c$ | $E_b/t$ |
|---|---|---|---|---|
| 1.00 | 0.000 | | 2.00 | 2.753 |
| 1.05 | 0.022 | | 3.00 | 6.453 |
| 1.20 | 0.271 | | 5.00 | 14.20 |
| 1.50 | 1.080 | | 10.0 | 33.95 |

Monotonic, and $E_b\to0$ continuously as $g\to g_c^+$.

**C — Two independent methods agree (machine precision).** On a finite $L=12$ lattice, the secular root of $(\ast)$ and a full dense diagonalisation of $H_\text{rel}$ give the same ground-state energy $E_0=-2.7896190632\,t$ to $1.3\times10^{-15}$. The solver is therefore exact, not approximate.

**D — The F73 ceiling is recovered dynamically.** At threshold $E_b\to0\Rightarrow M=2m_c-E_b\to 2m_c$: the F73 kinematic ceiling is the *threshold/critical* case of the dynamics, not an assumption. This is the dynamical analogue of the NJL mean-field theorem $m_\sigma=2m_c$ (the composite sits exactly at the two-constituent threshold; the pseudoscalar partner is the massless Goldstone that becomes $W_L/Z_L$).

## The honest verdict — a quantified near-no-go

To make a 125.25 GeV scalar from a $t\bar t$ pair needs a binding fraction $\beta\equiv E_b/(2m_c)=1-\tfrac{125.25}{2\times172.57}=0.637$. Two facts make this hard, and both are now quantified:

1. **The model's own gauge sector binds far too weakly.** Photon/$Z$ exchange (positronium-like) supplies only $\beta\sim\alpha^2/8\approx7\times10^{-6}$ — about $10^{5}\times$ short of $0.637$. A *naturally* bound pair therefore stays pinned at the ceiling $M=2m_c$. There is no $0.64$-deep binding anywhere in the gauge couplings.

2. **A contact deep-binding requires criticality fine-tuning (the hierarchy problem, in the model's language).** Using the F46 map ($m_\text{lat}=m_c c a/\hbar$, $t=\hbar^2/m_c a^2\Rightarrow t/m_c c^2=1/m_\text{lat}^2$), the *physical* binding fraction is $\beta=(E_b/t)\,m_\text{lat}^2/2$. At the F64 cell every EW constituent has $m_\text{lat}\sim4\times10^{-17}$, so a physical sub-threshold binding ($0<\beta<1$) needs the coupling tuned to within $\sim m_\text{lat}^2\sim10^{-33}$ of $g_c$. Generic contact dynamics at the Planck cell give either $\beta\approx0$ (ceiling) or $\beta\gg1$ (unphysical collapse) — the binding scale is acutely UV-sensitive. This is the Higgs hierarchy/naturalness problem appearing intrinsically; the model does not evade it.

**Conclusion.** The binding machinery is built and the binding depth $E_b(g)$ is produced rigorously. The derivation is **complete up to a single external input — the strong contact coupling** — and the simulation shows that input is *not* present in the model's gauge sector and would require either criticality fine-tuning or genuinely new strong dynamics. So:

- **Predicted by the model:** the channel (spin-0 singlet sibling of the F69 photon), the exact kinematics (F73), the existence of a 3-D binding threshold $g_c$, and the ceiling $M=2m_c$ for any naturally-bound pair.
- **Still external:** the coupling/depth that would push $M$ down to 125 GeV. The model gives no natural mechanism for it; a light composite Higgs is therefore a fine-tuning or new-dynamics statement, not an output.

This is a genuine (if negative) completion: it converts F73's "needs binding dynamics" into the sharp result *"the binding dynamics available to the model cannot do it without fine-tuning,"* and isolates exactly what new ingredient a composite-Higgs version of this model would require.

## Scope / next

- The NR contact solver is quantitative near threshold ($\beta\ll1$); the deep-binding regime ($\beta\sim0.6$) is **relativistic** and beyond NR validity — a lattice **Bethe–Salpeter / ladder** treatment with the full F46 dispersion is the remaining hard build, and is where any genuine 125 GeV claim would have to be earned.
- A self-consistent NJL gap + RPA implementation (rather than the analytic $m_\sigma=2m_c$ reference used here) would let the *same* coupling fix both $m_c$ and $E_b$, testing whether criticality lands anywhere near the EW scale.

## Files
- Script: `model-tests/test_F74_bound_state_binding.py`
- Results: `test-results/F74_bound_state_binding.json`
