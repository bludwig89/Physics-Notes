% A Universe in a Bottle — Claims and Falsifiers
% B. Ludwig (independent researcher)
% 2026-06-08

## One-page summary

A deterministic **quantum cellular automaton (QCA)** on a body-centred-cubic (BCC) lattice is proposed as the physical vacuum. The free dynamics are *forced* (not chosen) by the Bisio–D'Ariano–Perinotti–Tosini uniqueness theorem: in 3D the minimal non-trivial one-particle QCA is the Weyl walk on the BCC lattice. From one reinterpretation — **the speed of light is the angular rotation rate of a real $(\mathbf E,\mathbf B)$ pair per unit wavenumber**, $c_\text{lat}=1/\sqrt3$ — the model recovers Maxwell's equations (as a linearised rotation), the Einstein mass shell (as a spherical-Pythagorean identity), and, with gauge structure added, the Standard-Model sectors and gravity. Every structural claim is verified numerically to machine precision (residuals $10^{-14}$–$10^{-16}$) or as exact rationals, in a public test suite. An eleven-paper series gives the full construction.

## Core claims (each a deviation from, or derivation of, the Standard Model)

1. **Light is a rotation rate, not a phase velocity** ($c_\text{lat}=d\Omega/d|\mathbf k|=1/\sqrt3$). Maxwell's curl law is its $O(\Omega)$ linearisation; energy conservation is geometric (length-preserving rotation).
2. **The photon is a bound pair of two spin-½ Weyl quanta** (de Broglie's neutrino theory of light), not a fundamental spin-1 boson — massless, luminal, transverse, and **exactly non-birefringent**.
3. **Mass without a Higgs field**: a chiral-$SU(2)$ complex-mass step carries weak isospin as an exact gauge symmetry (Ward identity to $1.1\times10^{-17}$); the would-be Higgs direction is pure gauge. Hypercharge rides the same field.
4. **Exactly three fermion generations** — a theorem about the cubic point group $O_h$ (maximal single-valued irrep $T_{1u}$ is 3-dimensional; no 4-dimensional one exists), realised by the scalar mass selecting the odd-parity triplet. **A fourth is forbidden.**
5. **The Koide relation $Q=\tfrac23$** is an exact $45^\circ$ equipartition of the cubic amplitude $\sqrt m$ ($Q(\phi)=1/3\cos^2\phi$); electromagnetism selects the colour-free charged leptons to sit there.
6. **Confinement** is exact in 2D (area law, $\sigma=-\ln w(\beta)>0$ for all $\beta$); in 3+1D it is a colour-dielectric dual superconductor cross-checked against gauge Monte-Carlo, governed by $\mathbb Z_3$ centre-phase closure.
7. **The Weinberg angle is derived**: $\sin^2\theta_W=\tfrac14$ from BCC swap geometry ($m_Z/m_W=2/\sqrt3$, zero parameters).
8. **Gravity is one impedance-matched lattice dielectric** $K=e^{2GM/rc^2}$ (reciprocal lock $AB\equiv1$): GR-identical PPN ($\beta=\gamma=1$), and **Newton's constant is structural**, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, fixing $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$.
9. **Black holes are horizon-free** dielectric condensates (exponential metric): no event horizon, no standard Hawking glow, an information-paradox-free unitary substrate.

## Headline verified numbers

| Quantity | Model | Reference / status |
|---|---|---|
| $c_\text{lat}$ | $1/\sqrt3=0.5773503$ | rotation-rate slope (axis & body diagonal) |
| $\sin^2\theta_W$ → $m_Z/m_W$ | $\tfrac14$ → $2/\sqrt3=1.1547$ | zero parameters; $1.77\%$ from PDG |
| Koide $Q$ | $0.6666605$ | $0.91\sigma$ from $\tfrac23$; predicts $m_\tau=1776.97$ MeV ($6\times10^{-5}$) |
| $a/\ell_P$; $G$ | $6.5978$; $6.6743\times10^{-11}$ | matches CODATA to $3\times10^{-8}$ |
| BH shadow / Schwarzschild | $2e/3\sqrt3=1.0463$ | $+4.63\%$ (throat $e$, photon sphere $2\sqrt e$) |
| Deuteron $E_b$, $\kappa$ | $2.224$ MeV, $0.2316$ fm$^{-1}$ | bound **only** by pion tensor force |

## Falsifiable predictions (with thresholds)

- **Photon-ring imaging.** The black-hole shadow is **$4.63\%$ larger** than Schwarzschild (M87\*: $41.5\,\mu$as; Sgr A\*: $55.7\,\mu$as). A horizon-scale shadow excluding $+4.63\%$ at few-percent photon-ring precision (ngEHT / space-VLBI) **falsifies the model**.
- **Quantum-gravity dispersion.** A quadratic ($n=2$) vacuum dispersion with energy scale $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV. **Any measured $n=2$ time-of-flight bound above $1.36\times10^{19}$ GeV kills the adopted lattice cell.**
- **Vacuum birefringence.** The physical (paired) photon is **exactly non-birefringent**; a confirmed first-order vacuum birefringence in GRB/AGN polarimetry would contradict it (and would, conversely, revive the excluded chiral construction).
- **Gravitational-wave echoes.** Horizon-free ⇒ ringdowns reflect into **late-time echoes** (LIGO/Virgo/KAGRA, LISA). A confirmed true absorbing horizon with no echoes falsifies the picture.
- **Strong-field light bending.** Second-order deflection coefficient $4\pi$ (vs Schwarzschild $15\pi/4$); a measurement consistent with $15\pi/4$ but excluding $4\pi$ falsifies it.
- **No event horizon / no thermal Hawking spectrum.** Detection of a thermal Hawking spectrum from an astrophysical horizon would contradict the model.
- **Mercury precession.** The nonlinear completion is fixed by $\beta=1$ (42.98″/cy); the naive linear dielectric ($\beta=\tfrac12$, 50.1″/cy) is already excluded — the model is committed to the exponential form.

## Reproducibility

Every claim above runs in a public test suite to the stated residual; the lattice cell, couplings, and metric carry **no free fit parameters** in the structural sector. Source, tests, and per-finding write-ups accompany the papers.

*Full series (11 papers) and this summary: see the accompanying `papers/` directory. Contact: benludwig6382@gmail.com.*
