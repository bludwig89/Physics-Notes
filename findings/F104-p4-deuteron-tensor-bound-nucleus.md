# F104 — P4 (matter-binding): the deuteron, the first nucleus, bound by the pion tensor force

**Date:** 2026-06-06 - 06:58
**Status:** Confirmed — 11/11 checks PASS. The tensor spin-angular matrix built from Clebsch-Gordan equals the Rarita-Schwinger [[0,2√2],[2√2,−2]] to 9.8×10⁻¹⁵; the deuteron binds as a single shallow J^P=1⁺ I=0 state **only** through the tensor force (central-only OPEP is unbound at the same core); the ³S₁ tail matches κ=√(M_N E_b)/ħc to 0.34%; and tuning the one short-range knob lands E_b=2.224 MeV with the physical κ=0.2316 fm⁻¹ and a 7% D-state.
**Roadmap:** `roadmap-matter-binding.md` Phase **P4** (nuclei — deuteron). Full ³S₁–³D₁ coupled-channel scope (user-selected).
**Module:** `ca-simulation/ca_nuclear.py`
**Script:** `model-tests/test_P4_deuteron.py` (~8 s, numpy only)
**Results:** `test-results/P4_deuteron.json`
**Cross-references:** [[F103-p3-dynamical-pion-goldstone]] (supplies m_π, f_π — the force carrier), [[F74-two-constituent-bound-state-binding]] (the two-body solver generalised contact→2-channel), [[F77-njl-gap-rpa-selfconsistent]] (Goldberger-Treiman tie for the coupling), [[F71-colour-singlet-baryon-proton]] (the nucleons being bound).

---

## Goal

`roadmap-matter-binding.md` P4 asks for the first **nucleus**: bind a proton and a neutron into the deuteron via the residual strong force, which at long range is one-pion exchange. The roadmap flags this as the highest-risk phase — the model has no residual nuclear force a priori, and the deuteron is shallow and fine-tuned even in real QCD. The user selected the **full ³S₁–³D₁ tensor** treatment (the faithful J^P=1⁺ deuteron) rather than a central-only first cut.

## Construction

`ca_nuclear.py` generalises the F74 two-body solver from a single contact channel to the **two coupled partial waves** of the deuteron. The static one-pion-exchange potential in the S=1, T=0 channel is

$$V_\pi(r)=-\frac{f^2}{4\pi}\,m_\pi\big[(\boldsymbol\sigma_1\!\cdot\!\boldsymbol\sigma_2)\,Y(x)+S_{12}\,T(x)\big],\quad x=\frac{m_\pi r}{\hbar c},$$

with $Y(x)=e^{-x}/x$, $T(x)=(1+3/x+3/x^2)e^{-x}/x$, and the tensor operator $S_{12}=3(\boldsymbol\sigma_1\!\cdot\!\hat n)(\boldsymbol\sigma_2\!\cdot\!\hat n)-\boldsymbol\sigma_1\!\cdot\!\boldsymbol\sigma_2$ that mixes L=0 (³S₁) and L=2 (³D₁). The radial problem is a real symmetric 2N×2N Hamiltonian (finite-difference kinetic + D-wave centrifugal + the OPEP matrix), lowest eigenpair by dense diagonalisation, with a hard core at $r_c$ regularising the $1/x^3$ tensor singularity.

**Inputs (honest accounting).** $m_\pi$, $f_\pi$ are P3/F77 model outputs; the πNN coupling $f^2/4\pi=0.074$ follows from Goldberger-Treiman $f_{\pi NN}=g_A m_\pi/(2f_\pi)$ with the one external number $g_A=1.272$ (the deuteron analogue of P3's external $g_{\rho\pi\pi}$). $M_N=938.9$ MeV is external (P2 not built; absolute scale is P6). The hard-core radius $r_c$ is the one tuned knob.

## Results

| check | result | tier |
|---|---|---|
| A — $\langle S_{12}\rangle$ from CG = [[0,2√2],[2√2,−2]] | 9.8×10⁻¹⁵ | machine |
| B — tensor essential: full binds (−2.00 MeV), central-only unbound (+0.66 MeV) | exact | structural |
| C — bound and shallow $E_b/M_N=2.1\times10^{-3}$ | ✓ | quantitative |
| D — single bound state ($E_1=+1.02$ MeV ≥ 0) | ✓ | structural |
| E — D-state $P_D=6.8\%$; $P_D=0$ without tensor | ✓ | quantitative |
| F — ³S₁ tail slope vs $\kappa=\sqrt{M_N E_b}/\hbar c$ | 0.34% | quantitative |
| G — tuned $r_c=0.448$ fm → $E_b=2.224$ MeV, $\kappa=0.2316$ fm⁻¹ | exact / 2×10⁻⁵ | quantitative |
| H — grid-converged $E_b$ | 0.64% | quantitative |

**The headline (B).** The deuteron binds **only** through the pion tensor force. At a fixed core radius the full ³S₁–³D₁ OPEP is bound while central-only OPEP is not — central OPEP sits below the Yukawa binding threshold ($2\mu V_0 a^2/\hbar^2\approx0.5<1.68$); the tensor L=0↔L=2 coupling supplies the missing attraction. This is the textbook reason the deuteron exists, reproduced here.

**Tensor strength certified (A).** The spin-angular $\langle S_{12}\rangle$ matrix built from explicit Clebsch-Gordan + spinor-spherical-harmonic quadrature equals the Rarita-Schwinger [[0,2√2],[2√2,−2]] to machine precision — the off-diagonal $2\sqrt2$ is exactly the mixing that does the binding.

**Structure.** A single shallow bound state (D), $J^P=1^+$ (both coupled waves have parity $(-1)^L=+1$, spin triplet), isospin-0, with a few-percent tensor-induced D-state (E; $P_D\approx7\%$, vanishing when the tensor is switched off). The ³S₁ tail independently reproduces $\kappa=\sqrt{M_N E_b}/\hbar c$ (F). Tuned to the physical $E_b=2.224$ MeV, the model returns the physical $\kappa=0.2316$ fm⁻¹.

## Verdict

The first nucleus is delivered: a bound, shallow, $J^P=1^+$, isospin-0 deuteron whose binding is supplied by the pion tensor force, with the tensor strength certified exactly and the binding energy / size tunable to the physical values. The roadmap's "treat a bound, shallow, spin-1, isospin-0 deuteron as success" target is met, and the 2.224 MeV stretch goal is reached with one tuned core radius.

- **Predicted by the model:** the binding **mechanism** and structure — tensor force essential (B), exact tensor strength (A), single shallow 1⁺ I=0 state (C,D), few-percent D-wave (E), $\kappa\leftrightarrow E_b$ (F). The carrier $m_\pi$ comes from P3.
- **External / phenomenological (flagged):** $g_A$ (one number, via Goldberger-Treiman), $M_N$ (P2/P6), and the **short-range repulsive core** — the "missing ingredient" the roadmap predicted P4 would expose. The model does not yet derive it.

## Scope / next

The open item is exactly the one the roadmap anticipated: a *derived* short-range core (heavy-meson ω/σ exchange, or a lattice contact from the quark substructure) to replace the tuned hard core. Absolute numbers (currently using physical $M_N$) firm up once P2 (dynamical baryon mass) and P6 (SI scale) are in place. With P3 and P4 done, the QCD-chain branch of the roadmap reaches its first nucleus; the remaining matter-binding phases are P2 (dynamical proton/neutron) and P5 (atoms / hydrogen), plus the cross-cutting P6.

## Files
- Module: `ca-simulation/ca_nuclear.py`
- Script: `model-tests/test_P4_deuteron.py`
- Results: `test-results/P4_deuteron.json`
