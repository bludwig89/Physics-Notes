# F77 — Self-consistent NJL gap + RPA: one coupling fixes both $m_c$ and $E_b$, and it confirms the F74 ceiling

**Date:** 2026-06-01 - 20:05
**Status:** Confirmed — 14/14 checks PASS. The two chiral-limit theorems (Goldstone $m_\pi=0$ and the NJL relation $m_\sigma=2m_c$) reproduce to machine precision ($2.3\times10^{-14}$), the polarization split identity is exact ($1.8\times10^{-16}$), and the canonical SU(2) fit reproduces the **measured** $m_c$, $f_\pi$, $m_\pi$ and $\langle\bar qq\rangle$ to within $0.2$–$4\%$. The F74 follow-up is answered.
**Script:** `model-tests/test_F77_njl_gap_rpa.py` (~1–2 s, numpy only)
**Results:** `test-results/F77_njl_gap_rpa.json`
**Cross-references:** [[F74-two-constituent-bound-state-binding]] (the external-$m_c$ contact solver this replaces and the exact follow-up it flagged), [[F73-spin0-bound-pair-scalar]] (the $m_H\to2m_c$ kinematic ceiling), [[F69-paired-spinor-photon]] (the spin-1 sibling channel), [[F46-pythagorean-lattice-mass]] (the $m_\text{lat}$ map), [[F78-koide-amplitude-from-cooper-pair]] / [[F80-one-45deg-em-saturation-koide]] (the *generation-space* application of this same Cooper-pair/condensate dynamics — see thread note).

> **Pairing-thread note.** F77 fixes the *magnitude* of the dynamical constituent mass $m_c$ (one coupling $G$ sets both the gap and $m_\sigma=2m_c$). The *same* Cooper-pair/condensate machinery, applied in **generation space**, is the subject of F78/F80: there the constituent amplitude $\sqrt m=y$ is the $T_{1u}$ vector (F78, $m=y^2$ from the pair bilinear), and the bound-pair stability cap invoked here ($\arcsin m_c=45°$, F73) turns out to be the *same* SO(2) equipartition as the charged-lepton Koide point $Q=\tfrac23$ (F80). So F73/F74/F77 (constituent-level pairing) and F76/F78/F80 (generation-level Koide) are one thread: **mass is an SO(2) rotation, and 45° equipartition appears once at each level.**

---

## Goal

F74 produced the binding depth $E_b(g)$ from a **non-relativistic single-site contact** secular equation, but with the constituent mass $m_c$ put in **by hand** and the NJL identity $m_\sigma=2m_c$ used only as an external *reference*. It therefore could not test the real question, which F74 flagged verbatim as the next build:

> *A self-consistent NJL gap + RPA implementation (rather than the analytic $m_\sigma=2m_c$ reference used here) would let the same coupling fix both $m_c$ and $E_b$, testing whether criticality lands anywhere near the EW scale.*

This finding does exactly that: a single coupling $G$ both **dynamically generates** $m_c$ (the gap equation / chiral-symmetry breaking) **and**, summed in the $q\bar q$ ladder, fixes the scalar pole $m_\sigma$ — hence the binding $E_b=2m_c-m_\sigma$. No external input remains.

## Construction (standard SU(2) NJL, $N_c=3$, $N_f=2$)

A single contact coupling $G$ in $\mathcal L=\bar\psi(i\slashed\partial-m_0)\psi+G[(\bar\psi\psi)^2+(\bar\psi i\gamma_5\vec\tau\psi)^2]$.

**1 — Gap equation (Hartree / Dyson–Schwinger):** the same $G$ generates a constituent mass from the chiral condensate,

$$M=m_0+4G\,N_cN_f\,M\,I_1(M),\qquad I_1(M)=\frac{1}{2\pi^2}\int_0^\Lambda\frac{p^2\,dp}{\sqrt{p^2+M^2}}.$$

There is a finite **critical coupling** (the NJL analogue of F74's binding threshold $g_c$),

$$\boxed{\,G_c\Lambda^2=\frac{\pi^2}{N_cN_f}=\frac{\pi^2}{6}=1.644934\,}$$

below which chiral symmetry is unbroken ($M=m_0$, no dynamical mass).

**2 — RPA / ladder mesons:** the same $G$ summed in the $q\bar q$ ladder gives the bound-state poles $1-2G\,\Pi_M(q^2)=0$ with

$$\Pi_\text{PS}(q^2)=2N_cN_f\big[I_1+q^2K\big],\quad
\Pi_\text{S}(q^2)=2N_cN_f\big[I_1+(q^2-4M^2)K\big],\quad
K(q^2)=\frac{1}{2\pi^2}\int_0^\Lambda\frac{p^2\,dp}{E_p(4E_p^2-q^2)}.$$

The scalar $\sigma$ is the spin-0 partner of F73/F74; its pole fixes $E_b=2m_c-m_\sigma$.

## Results

**A — Theorems, machine precision, no fitting.** In the chiral limit ($m_0=0$) the pion is the exact Goldstone boson ($1-2G\Pi_\text{PS}(0)=0$ is *identically* the gap equation; residual $2.3\times10^{-14}$) and the scalar sits exactly at threshold,

$$m_\sigma=2m_c\quad(\text{residual }2.3\times10^{-14}),$$

reproducing the NJL mean-field theorem — and thereby the **F73 kinematic ceiling** — as an *output* of the same coupling that made $m_c$. The polarization split $\Pi_S-\Pi_\text{PS}=-8N_cN_fM^2K$ holds to $1.8\times10^{-16}$.

**B — Validated against the real world.** The canonical SU(2) fit ($\Lambda=651.5$ MeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV) reproduces the measured QCD numbers, which is how we know the normalisation/prefactors are physical:

| quantity | model | measured | resid |
|---|---|---|---|
| $m_c=M$ | 311 MeV | $\sim$325 | 4.2% |
| $f_\pi$ | 92.6 MeV | 92.4 | 0.2% |
| $m_\pi$ | 140.5 MeV | 135–138 | 4.1% |
| $\langle\bar qq\rangle^{1/3}$ | $-249$ MeV | $\sim-250$ | 0.4% |

GMOR ($m_\pi^2f_\pi^2=-m_0\langle\bar qq\rangle$, 0.4%) and Goldberger–Treiman ($g_{\pi qq}f_\pi=M$, 1.1%) also hold.

**C — The F74 follow-up, answered.** Scanning $G$ from $1.02\,G_c$ to $10\,G_c$, in both the chiral limit and at $m_0=5.5$ MeV, the self-consistent scalar **always** satisfies

$$\frac{m_\sigma}{2m_c}\ge1\quad\Longrightarrow\quad E_b=2m_c-m_\sigma\le0.$$

In the chiral limit the ratio is exactly $1$ at every coupling; with $m_0>0$ it is $\ge1$. The NJL $\sigma$ is therefore a **threshold resonance, not a sub-threshold deep-bound state**. Critically, raising $G$ does not lower the ratio — it scales $m_c$ and $m_\sigma$ up *together* at fixed ratio — and lowering $G\to G_c$ sends $m_c\to0$ and $m_\sigma\to0$ together, also at fixed ratio $1$. There is no direction in coupling space that produces sub-threshold binding.

## Verdict

The electroweak target is

$$\frac{m_H}{2m_t}=\frac{125.25}{2\times172.57}=0.363,$$

which lives in the region $m_\sigma/(2m_c)<1$ that the self-consistent NJL **cannot reach** with a single coupling. This **confirms F74's near-no-go and removes its one external input**: it is no longer "complete up to the contact coupling" — the coupling is now the *same* dynamical-mass coupling, and it pins the scalar at or above the $2m_c$ ceiling. A 125 GeV scalar from a $t\bar t$ pair would need sub-threshold binding ($\beta=0.637$) that the dynamical-mass mechanism structurally does not supply.

- **Predicted by the model:** dynamical $m_c$ from one coupling above $G_c\Lambda^2=\pi^2/6$; the Goldstone pion; the scalar pinned at the ceiling $m_\sigma\ge2m_c$ for every coupling; the whole measured light-meson sector as a cross-check.
- **Still external (sharper than F74):** any sub-threshold deep binding. It is absent not just from the gauge sector (F74) but from the dynamical-mass (NJL/RPA) sector too — at *mean-field/RPA* order. The only remaining hiding place is a genuinely relativistic **Bethe–Salpeter ladder beyond RPA**, which is the precise remaining build.

## Scope / next

- RPA is the leading large-$N_c$ (mean-field) ladder; it pins $m_\sigma$ at threshold by construction. A full **Bethe–Salpeter** treatment with the F46 lattice dispersion, plus the $\sigma$ width above threshold (the bubble's imaginary part for $q^2>4M^2$), is where any genuine 125 GeV claim would still have to be earned.
- Above threshold the scalar is a broad resonance; quantifying its width via $\mathrm{Im}\,K(q^2>4M^2)$ is a small extension of this script.

## Files
- Script: `model-tests/test_F77_njl_gap_rpa.py`
- Results: `test-results/F77_njl_gap_rpa.json`
