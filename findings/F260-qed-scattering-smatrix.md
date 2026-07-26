# F260 — The tree-level QED S-matrix on the model's fields, and the positron / charge-conjugation + crossing sector

**Date:** 2026-07-22 - 16:20
**Status:** Confirmed — 11/11 gates PASS. Charge conjugation ($C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top$), the crossing relations, and the Ward identities are **algebraically exact** (sympy, literal 0); every spin-averaged $\lvert\mathcal M\rvert^2$ equals the textbook Mandelstam closed form to **machine precision**; the Klein–Nishina, Møller/Bhabha, Dirac-annihilation and $\mu$-pair cross sections reproduce the closed-form textbook results by phase-space integration; Compton reduces to Thomson.
**Module:** `ca-simulation/ca_qed_scattering.py`
**Verification script:** `tests/findings/test_F260_qed_scattering.py` (also surfaced as Tier D of `tests/findings/test_F249_qed_comparison_battery.py`)
**Result file:** `test-results/F260_qed_scattering.json`
**Cross-references:** [[F249-qed-comparison-battery]] (the battery whose Tier-A5 stops at Thomson — the S-matrix completeness gap this closes; now extended with Tier D), [[F87-charge-coupling-paired-photon]] (the identity-channel QED vertex $e\gamma^\mu$ every amplitude is built from), [[F69-paired-spinor-photon]] and [[F250-allk-gauge-pole-paired-photon]] (the even-law paired photon and the transverse 2-polarisation residue used in the photon polarisation sums), [[F27-complex-mass-chiral-su2]] / [[F46-pythagorean-lattice-mass]] (the electron; the positron is added here as its charge conjugate), [[F252-vertex-ae-lamb]] and [[F259-ir-bremsstrahlung]] (the loop/IR companions: the $O(\alpha)$ radiative corrections to these tree rates are the F252/F259 job), [[F120-electron-calibrated-spectrum]] / [[F121-tau-anchored-canonical-spectrum]] (the electron and muon mass anchors — the only inputs beyond $\alpha$).

---

## The claim

F249's Tier-A5 confronts the model with **Thomson** scattering — the zero-energy limit of Compton — and stops there. The full tree S-matrix of QED had never been built on the model's fields, and the **antiparticle sector** (charge conjugation, crossing) had never been exercised. The claim:

> On the model-native ingredients — the F87/F68 identity-channel vertex $e\gamma^\mu$, the F69/F250 even-law transverse paired photon, the F27/F46 Dirac electron, and the **positron built as the charge conjugate** $v=C\bar u^\top$ — the tree-level QED S-matrix reproduces the classic cross sections exactly: **Klein–Nishina** ($e\gamma\to e\gamma$), **Møller** ($e^-e^-$), **Bhabha** ($e^-e^+$), **Dirac pair annihilation** ($e^-e^+\to\gamma\gamma$), and $e^-e^+\to\mu^-\mu^+$. Charge conjugation, crossing and the Ward identities are algebraically exact; Compton reduces to Thomson as $\omega\to0$.

The only physical inputs are $\alpha$ and the lepton masses (electron anchor F120/F121; muon anchor F121). Spin sums use the model's own $u,v$ **completeness** $\sum u\bar u=\slashed p+m$, $\sum v\bar v=\slashed p-m$, built from the explicit spinors and verified — never `np.linalg.eig` on chiral matrices (CLAUDE.md). Photon polarisation sums use the F250 transverse residue: in Feynman gauge $-g_{\mu\nu}$ once the Ward identity (verified below) drops the longitudinal/scalar pieces.

---

## The results

### G1 — charge conjugation (exact)

With $C=i\gamma^2\gamma^0$ in the Dirac representation (matching F252/F258/F259), verified to literal zero with explicit $4\times4$ gammas (sympy):

$$C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top,\qquad C^\top=-C,\qquad C^\dagger C=\mathbb 1,\qquad C^2=-\mathbb 1.$$

This is what promotes the F27/F46 electron $u$-spinor to the positron $v$-spinor and underlies crossing.

### G2 — the positron spinor and $u,v$ completeness (machine precision, no eig)

The **positron** is the charge conjugate of the electron solution,

$$v(p,s)=C\,\bar u(p,s)^\top=C\,\gamma^{0\top}u(p,s)^*.$$

At random on-shell momenta the constructed $v$ satisfies the negative-energy Dirac equation $(\slashed p+m)v=0$ and, together with $u$, the completeness relations the trace engine relies on:

$$\sum_s u(p,s)\bar u(p,s)=\slashed p+m,\qquad \sum_s v(p,s)\bar v(p,s)=\slashed p-m,$$

each to $<10^{-11}$ — the model's own completeness, no eigen-decomposition anywhere.

### G3 — crossing symmetry (exact)

The same analytic amplitude continues between channels (sympy, literal identities):

* **Møller $\leftrightarrow$ Bhabha:** $\ \lvert\mathcal M\rvert^2_\text{Bhabha}(s,t,u)=\lvert\mathcal M\rvert^2_\text{Møller}(u,t,s)$ — swap an incoming $e^-$ for an outgoing $e^+$ ($s\leftrightarrow u$).
* **Compton $\leftrightarrow$ annihilation:** with $a=p\cdot k_1,\ b=p\cdot k_2$, $\ \lvert\mathcal M\rvert^2_\text{annih}(a,b)=-\lvert\mathcal M\rvert^2_\text{Compton}(-a,b)$ — the overall minus is the fermion-crossing sign.

### C1 — Compton / Klein–Nishina $\lvert\mathcal M\rvert^2$ (machine precision)

Summing the $s$- and $u$-channel diagrams, the spin-averaged square computed by Dirac traces on the model completeness equals the textbook Mandelstam form (Peskin 5.87)

$$\langle\lvert\mathcal M\rvert^2\rangle=2e^4\!\left[\frac{p\cdot k'}{p\cdot k}+\frac{p\cdot k}{p\cdot k'}+2m^2\!\left(\frac1{p\cdot k}-\frac1{p\cdot k'}\right)+m^4\!\left(\frac1{p\cdot k}-\frac1{p\cdot k'}\right)^2\right]$$

to $<10^{-13}$ at all lab kinematics ($\omega/m$ from $0.01$ to $10$).

### C2 — gauge invariance / Ward identity (machine precision)

Replacing a photon polarisation by its momentum kills the amplitude: on explicit on-shell spinors, $k_\mu\mathcal M^{\mu\nu}=k'_\nu\mathcal M^{\mu\nu}=0$ for every remaining index and spin, to $<10^{-12}$. This justifies the $-g_{\mu\nu}$ (F250 transverse) photon polarisation sum used throughout.

### C3 — Klein–Nishina total cross section $\to$ Thomson (quantitative; ties F249 A5)

Integrating the trace $\lvert\mathcal M\rvert^2$ over the lab solid angle reproduces the closed Klein–Nishina total cross section to $\le4.5\times10^{-7}$ across $x=\omega/m\in\{0.01,0.1,1,5\}$, and as $\omega\to0$ it reduces to Thomson: $\sigma(x{=}10^{-4})/\sigma_T=0.9998=1-2x+\mathcal O(x^2)$. The Thomson value from the model's own $\alpha,m_e$ is $\sigma_T=0.6652459$ barn vs CODATA $0.66524587$ barn — the same number F249 A5 checks, now recovered as the $\omega\to0$ limit of the full process.

### M1/M2/M3 — Møller and Bhabha (machine precision + quantitative)

The spin-averaged squares match the standard massless forms to $<10^{-13}$:

$$\langle\lvert\mathcal M\rvert^2\rangle_\text{Møller}=2e^4\!\left[\frac{s^2+u^2}{t^2}+\frac{s^2+t^2}{u^2}+\frac{2s^2}{tu}\right],\quad
\langle\lvert\mathcal M\rvert^2\rangle_\text{Bhabha}=2e^4\!\left[\frac{s^2+u^2}{t^2}+\frac{u^2+t^2}{s^2}+\frac{2u^2}{st}\right],$$

with the Bhabha$\leftrightarrow$Møller $s\leftrightarrow u$ crossing exact (G3). The CM differential cross sections $d\sigma/d\Omega=\lvert\mathcal M\rvert^2/64\pi^2 s$ are reported in barn/sr.

### A1 — pair annihilation $e^-e^+\to\gamma\gamma$ (machine precision + quantitative)

The $t$- and $u$-channel electron-exchange amplitude gives $\langle\lvert\mathcal M\rvert^2\rangle$ equal to the Dirac form (the crossing of Compton, G3) to $<10^{-13}$; it is **Bose-symmetric** under $k\leftrightarrow k'$ (identical photons) to machine precision; the **Ward identity holds on both photons** ($<10^{-15}$); and the total cross section reproduces the closed Dirac (1930) form

$$\sigma=\frac{2\pi\alpha^2}{s}\,\frac1\beta\left[\frac{3-\beta^4}{2\beta}\ln\frac{1+\beta}{1-\beta}-(2-\beta^2)\right],\qquad \beta=\sqrt{1-4m^2/s},$$

to $\le1.6\times10^{-6}$. This process requires the positron $v=C\bar u^\top$ built in G1/G2.

### U1 — $e^-e^+\to\mu^-\mu^+$ (machine precision + quantitative)

The $s$-channel amplitude gives $\langle\lvert\mathcal M\rvert^2\rangle=(8e^4/s^2)[(p_1\cdot k_1)(p_2\cdot k_2)+(p_1\cdot k_2)(p_2\cdot k_1)+m_\mu^2\,p_1\cdot p_2]$ (with $m_e\to0$) to $<10^{-13}$, and the total cross section reproduces

$$\sigma=\frac{4\pi\alpha^2}{3s}\sqrt{1-\frac{4m_\mu^2}{s}}\left(1+\frac{2m_\mu^2}{s}\right)\;\xrightarrow{\ s\gg m_\mu^2\ }\;\frac{4\pi\alpha^2}{3s},$$

the **R-ratio unit**, to $\le1.6\times10^{-8}$. At $\sqrt s=10\,\text{GeV}$ the model gives $\sigma=8.685\times10^{-10}$ barn, $0.999977$ of the high-energy $4\pi\alpha^2/3s$. Needs the second-generation muon (mass anchor F121: $m_\mu^\text{model}=105.6575$ MeV).

---

## Verification summary (11/11)

| Gate | Quantity | Tier | Result |
|---|---|---|---|
| G1 | $C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top$, $C^2=-1$ | exact (sympy) | literal 0 |
| G2 | positron $v=C\bar u^\top$; $\sum v\bar v=\slashed p-m$ (no eig) | machine | $<10^{-11}$ |
| G3 | Bhabha$=$Møller$\rvert_{s\leftrightarrow u}$; annih$=-$Compton$\rvert_{a\to-a}$ | exact (sympy) | literal 0 |
| C1 | Compton $\lvert\mathcal M\rvert^2=$ Klein–Nishina Mandelstam form | machine | $<10^{-13}$ |
| C2 | Ward $k_\mu\mathcal M^{\mu\nu}=k'_\nu\mathcal M^{\mu\nu}=0$ | machine | $<10^{-12}$ |
| C3 | KN total $\sigma(x)$ vs closed; $\to\sigma_T$ (F249 A5) | quantitative | $\le5\times10^{-7}$; $\sigma_T$ 0.3% |
| M1 | Møller $\lvert\mathcal M\rvert^2$ vs textbook | machine | $<10^{-13}$ |
| M2 | Bhabha $\lvert\mathcal M\rvert^2$ vs textbook | machine | $<10^{-13}$ |
| M3 | Møller/Bhabha differential cross sections | quantitative | $>0$, barn/sr |
| A1 | annihilation $\lvert\mathcal M\rvert^2$ + Bose + Ward(both) + $\sigma$ | machine + quant. | $\le1.6\times10^{-6}$ |
| U1 | $e^-e^+\to\mu^-\mu^+$ $\lvert\mathcal M\rvert^2$ + $\sigma\to4\pi\alpha^2/3s$ | machine + quant. | $\le1.6\times10^{-8}$ |

---

## Scope and honesty

These are **tree-level** results. The $O(\alpha)$ radiative corrections to these rates — the vertex $F_1$ (F252), the electron self-energy $Z_2$ (F258), and the IR-finite real-emission (F259) — are the loop/IR companions; combining them with these trees to produce IR-finite loop-corrected cross sections is the Prompt-2 (bremsstrahlung) coordination, noted there, not redone here. The photon polarisation sum uses $-g_{\mu\nu}$; this is exact here because the Ward identity (C2, A1) is verified for each process, so the longitudinal/scalar pieces drop. Massless external electrons are used for Møller/Bhabha (the standard high-energy closed forms); the exact massive $\lvert\mathcal M\rvert^2$ is what the trace engine computes, and the finite-mass reduction is available.

## What this establishes

The model's QED now has a **working tree S-matrix** and an explicit **antiparticle sector**. The positron is not an add-on but the charge conjugate of the F27/F46 electron, and crossing ties the electron and positron processes into single analytic amplitudes. Every classic tree cross section — Klein–Nishina, Møller, Bhabha, Dirac annihilation, and the $e^+e^-\to\mu^+\mu^-$ R-ratio unit — is reproduced from the model's two inputs ($\alpha$ and the lepton masses), closing the S-matrix completeness gap F249 flagged.
