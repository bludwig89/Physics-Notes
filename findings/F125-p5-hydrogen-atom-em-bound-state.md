# F125 — P5: the atom — hydrogen as an electromagnetic bound state, Rydberg series + Dirac fine structure

**Date:** 2026-06-09 - 19:10
**Status:** Confirmed — 20/20 checks PASS. Machine-precision identities (positronium reduced-mass ratio, Sommerfeld == O((Zα)⁴) series, 2s½–2p½ Dirac degeneracy); grid-floor PREDICTIONs (−1/n² Rydberg series, Coulomb ℓ-degeneracy, node structure); quantitative PREDICTIONs (absolute −13.6 eV from m_e+α, Bohr radius, fine-structure splitting = 10.95 GHz, α⁴/α² scaling, numerical-Dirac == Sommerfeld). Closes the matter-binding roadmap (P0–P6).
**Module:** `ca-simulation/ca_atom.py`
**Script:** `tests/findings/test_P5_hydrogen.py` (~12 s)
**Results:** `test-results/P5_hydrogen.json`
**Cross-references:** [[higgs-free-su2-key-choice]] / F27 (the dynamical electron the atom binds), [[f87-charge-coupling-paired-photon]] / F69 (the EM U(1) paired-spinor photon — the binding channel), the F74 two-body solver (the engine this generalises contact→Coulomb), [[f123-p6-si-scale-matter]] / F121 / F120 (the electron mass anchor), `docs/roadmaps/roadmap-matter-binding.md` (P5).

---

## 1. The phase

P5 is the **atom**: an electron (P0, `ca_dirac.py`) bound to a nucleus by the **electromagnetic** channel — the F69 paired-spinor photon's U(1) minimal coupling, the long-range $-Z\alpha\hbar c/r$ Coulomb tail. This is the QED-sector counterpart of the strong-sector chain (P1–P4): the same two-body bound-state discipline (F74), now with an **attractive $1/r$** instead of a confining string or a contact/Yukawa well. It is independent of the QCD chain — it needs only P0 (the electron) and EM.

## 2. The engine — the attractive-$1/r$ analogue of F74

The reduced radial Schrödinger problem in Bohr-radius units $x=r/a_0$,

$$-\tfrac12 u''(x) + \Big[\frac{l(l+1)}{2x^2} - \frac1x\Big]u(x) = \varepsilon\,u(x),\qquad \varepsilon_n=-\frac1{2n^2},$$

is solved as a **real symmetric tridiagonal eigenproblem** (finite difference, $u(0)=u(x_{\max})=0$), the direct $1/r$ generalisation of the F74 contact solver. The dimensionless eigenvalues reproduce $E_n[\mathrm{Ry}]=2\varepsilon_n=-1/n^2$ to the grid floor (worst dev $1.6\times10^{-4}$ at the $1s$ cusp, converging as the grid refines), with the exact **Coulomb $\ell$-degeneracy** (the accidental SO(4) symmetry): the $n$-sublevels of different $\ell$ coincide to $\lesssim10^{-5}$ Ry. The $1s$ reduced radial function is $\propto x\,e^{-x}$ (slope $-1.00$), $\langle r\rangle_{1s}=1.500\,a_0$, and the node count is exactly $n-l-1$ across the series.

## 3. The headline — 13.6 eV from the electron mass and α alone

The absolute scale is **not** a new input. The physical Rydberg

$$\mathrm{Ry}=\tfrac12\,\mu c^2(Z\alpha)^2$$

is built from the model's own electron mass $m_e c^2=0.510999$ MeV (the P0/F120–F121 anchor) and the electromagnetic coupling $\alpha=1/137.036$. With the e–p reduced mass this gives $\mathrm{Ry}(\mathrm H)=13.598287$ eV — matching the reduced-mass CODATA value to $1.1\times10^{-12}$ — so the hydrogen ground state lands at $-13.596$ eV and the Bohr radius at $0.052947$ nm, with **no further input**. $\alpha$ is the one empirical EM number (the P5 analogue of P4's $g_A$); everything downstream is a prediction.

## 4. Positronium — the two-body de-risk

Before the heavy proton, the $e^+e^-$ problem reduces in the relative coordinate to the **same** $1/r$ solver with $\mu=m_e/2$. Because $\mathrm{Ry}\propto\mu$, every positronium level is **exactly half** the infinite-mass hydrogen value: the ratio $\mathrm{Ry}(\mathrm{Ps})/\mathrm{Ry}(\mathrm H_\infty)=0.5000000000$ to $10^{-9}$, ground state $-6.803$ eV, with its own clean $-1/n^2$ series. This certifies the two-body→relative-coordinate reduction is faithful.

## 5. Fine structure — from the Dirac, not the Schrödinger, operator

The relativistic splitting is a **prediction of the Dirac kinetic operator**. The exact Dirac–Coulomb (Sommerfeld) spectrum

$$E_{n,\kappa}=mc^2\Big[1+\Big(\frac{Z\alpha}{n_r+\gamma}\Big)^2\Big]^{-1/2},\quad \gamma=\sqrt{\kappa^2-(Z\alpha)^2},\ n_r=n-|\kappa|$$

(a) matches its own $O((Z\alpha)^4)$ expansion $E_b\approx-\tfrac12 mc^2(Z\alpha)^2/n^2[1+(Z\alpha)^2/n^2(n/(j+\tfrac12)-\tfrac34)]$ to $5\times10^{-10}$; (b) puts $1s_{1/2}$ at $-13.605874$ eV (CODATA Ry $13.605693$, the rest the $O(\alpha^4)$ Dirac shift); and (c) is reproduced by a **hand-rolled numerical radial-Dirac integrator** (RK4, inward+outward Wronskian matching of the large/small components $G,F$) for $1s_{1/2}$, $2p_{1/2}$, $2p_{3/2}$ to $\le1.3\times10^{-6}$ relative to the binding — so the splitting is a genuine solve, not just the closed form.

The defining signatures both hold:

- **The $2p_{3/2}-2p_{1/2}$ splitting** is $45.28\ \mu\text{eV}=10.95$ GHz (measured $\approx10.969$ GHz, $0.18\%$), and scales as $\alpha^4$ absolute (fitted slope $4.0001$) / $\alpha^2$ relative to the binding (slope $2.0000$) — the textbook fine-structure law.
- **The Lamb shift is beyond Dirac:** in pure Dirac–Coulomb $2s_{1/2}$ and $2p_{1/2}$ (same $|\kappa|=1$) are **exactly degenerate** (to $10^{-14}$). The observed $2s$–$2p$ Lamb shift is a radiative QED effect (vacuum polarisation + self-energy) — the open **QFT-4** item in `first-gen-completeness.md` §5.4 — not part of the one-body Dirac problem.

## 6. Honest calibration

Inputs are $m_e$ (model anchor, P0/F120–F121), $\alpha$ (the one empirical EM coupling), and $m_p$ (the $0.05\%$ reduced-mass shift). The **predictions** are the $-1/n^2$ series, the Coulomb $\ell$-degeneracy, the absolute 13.6 eV, the $\alpha^2$ fine structure, and the Dirac $2s$–$2p$ degeneracy. A full 3-D real-space lattice Coulomb solve carries the known short-distance $1/r$ regularisation issue and leans on the lattice spacing $a$ (P6); the partial-wave-reduced radial solver used here is the standard accurate route, and positronium-first confirms the reduction.

## 7. What it closes

With P5 built, the matter-binding roadmap is complete: **P0** (electron/u/d), **P1** (3-D confinement), **P2** (proton/neutron), **P3** (pion), **P4** (deuteron), **P5** (atom), **P6** (SI scale). The model carries one electron through to a hydrogen atom with the right ground-state energy, the right spectrum, and the right relativistic fine structure — from a single EM coupling.

## 8. Test ledger (20/20)

A — positronium ratio $=\tfrac12$ (machine), ground $-6.803$ eV, $1/n^2$ series. B — $E_n[\mathrm{Ry}]=-1/n^2$, $n{=}1\text{–}5$. C — $\ell$-degeneracy. D — $\mathrm{Ry}$ vs reduced-mass CODATA ($10^{-12}$), ground $-13.6$ eV, $a_0=0.0529$ nm. E — $\langle r\rangle_{1s}=1.5a_0$, $1s\sim xe^{-x}$, node count $n{-}l{-}1$. F — Sommerfeld == $O((Z\alpha)^4)$ series; $1s_{1/2}$ == CODATA Ry. G — numerical Dirac == Sommerfeld. H — splitting $=10.95$ GHz; $\alpha^4$/$\alpha^2$ scaling. I — $2s_{1/2}$ == $2p_{1/2}$ (machine). J — grid convergence.
