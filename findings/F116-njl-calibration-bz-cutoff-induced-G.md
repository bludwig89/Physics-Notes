# F116 — NJL calibration: the cutoff $\Lambda$ is the Brillouin-zone edge (not a fit), the contact $G$ is an induced coupling from the confining colour dielectric, and the three F77 numbers reduce to one ruler plus two dimensionless inputs

**Date:** 2026-06-08 - 15:10
**Status:** Partial — structural reduction + a runnable lattice-BZ re-derivation; the precise dimensionless values remain a fit/mechanism. 4/4 check blocks (NJ1 accounting; NJ2 lattice-BZ chiral SB; NJ3 chiral-limit Goldstone exact $3.6\times10^{-15}$; NJ4 induced-$G$ order of magnitude). Addresses audit C.6 (`project-audit-inputs-dynamism-2026-06-06.md`, open input #6).
**Script:** `model-tests/test_F116_njl_lattice_calibration.py` (~2 s, numpy)
**Results:** `test-results/F116_njl_lattice_calibration.json`
**Cross-references:** [[F77-njl-gap-rpa-selfconsistent]] (the calibration $\{\Lambda,G\Lambda^2,m_0\}$ this re-derives; $G_c\Lambda^2=\pi^2/6$), [[F88-colour-condensate-from-model]] (the dual-Meissner/dielectric scale $M_g$ that induces $G$; $v=m_D/e=0.713$), [[F86-colour-dielectric-dual-superconductor]] ($\sigma=2\pi v^2$), [[F115-coupling-magnitudes-running-rotor]] ($g_s$ rotor lock used in the induced-$G$ estimate), [[F107-canonical-a-adoption-L4-grb-gate]] (the SI ruler that absorbs $\Lambda$), [[F46-pythagorean-lattice-mass]] (the lattice dispersion the BZ integral uses).

---

## 1. What this addresses

Audit input #6: *"NJL calibration $\Lambda=651.5$ MeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV — fitted to measured $m_c/f_\pi/m_\pi/\langle\bar qq\rangle$."* The audit's three sub-avenues (C.6): (1) $\Lambda$ is the lattice/BZ edge, not free; (2) $G$ is induced by integrating out the confining dielectric (Sakharov logic); (3) $m_0$ belongs to the orthorhombic-texture machinery. This finding executes (1) as a runnable re-derivation, (2) as a mechanism + order-of-magnitude, and flags (3).

## 2. NJ1 — the three numbers are one ruler plus two dimensionless inputs

F77's calibration is, dimensionally, **one scale and two pure numbers**:

$$\{\Lambda=651.5\ \text{MeV}\}\ +\ \Big\{\hat g\equiv G\Lambda^2=2.10,\quad \hat m_0\equiv m_0/\Lambda=8.4\times10^{-3}\Big\}.$$

$\Lambda$ is a **ruler** — it sets MeV from lattice units, exactly the role the lattice spacing $a$ plays, and the audit closed the "one ruler" reduction at C.1/F107. Moreover $\Lambda$ is *not even an independent ruler*: it is the chiral-symmetry-breaking scale, $\Lambda/(4\pi f_\pi)=651.5/1161=0.561$, i.e. $\Lambda\sim$ the chiral scale set by $f_\pi$. So NJL adds **two genuine dimensionless inputs**, not three. Their structural content:

- $\hat g=G\Lambda^2=2.10$ measured against the **exact** critical value $G_c\Lambda^2=\pi^2/(N_cN_f)=\pi^2/6=1.645$ (F77): $G/G_c=1.277$. The theory sits 28% above critical — the near-critical structure F74/F77 already flagged.
- $\hat m_0=m_0/\Lambda$ — the current-quark texture (§5).

## 3. NJ2 — lattice-BZ gap equation: $\Lambda\to$ the zone (runnable)

The continuum NJL gap equation $M=m_0+4G N_cN_f M\,I_1(M)$ uses a sharp 3-momentum cutoff $I_1(M)=\tfrac1{2\pi^2}\int_0^\Lambda \tfrac{p^2dp}{\sqrt{p^2+M^2}}$. We replace it with an integral over the **Brillouin zone**, $I_1(M)=\big\langle1/\sqrt{K(k)+M^2}\big\rangle_\text{BZ}$ with the lattice dispersion $K(k)=\sum_i 2(1-\cos k_i)$ (single pole at $k=0$, $\to k^2$ in the IR), $k_i\in(-\pi,\pi]$. There is **no free $\Lambda$** — the zone edge $\pi$ is the regulator.

On a $48^3$ zone the gap equation has a finite **critical coupling** $g_c=1/I_1(0)=2.196$ (dimensionless lattice $g\equiv4N_cN_fG$), the BZ analogue of $G_c\Lambda^2=\pi^2/6$. Below $g_c$ the only solution is $M=0$ (unbroken); above $g_c$ a dynamical constituent mass switches on continuously (second-order transition):

| $g/g_c$ | 0.80 | 0.90 | 0.95 | 1.05 | 1.10 | 1.30 | 1.60 |
|---|---|---|---|---|---|---|---|
| $M_\text{dyn}$ | 0 | 0 | 0 | 0.555 | 0.840 | 1.654 | 2.593 |

The transition is continuous ($M\to0$ as $g\to g_c^+$); the onset carries a 3D infrared logarithm ($\langle K^{-3/2}\rangle$ is log-divergent), so $M^2$ is not strictly linear in $g-g_c$ — the physical statement is a continuous second-order chiral transition. **Chiral symmetry breaking is reproduced with the BZ as cutoff**, confirming the audit's claim that $\Lambda$ is the zone, not a fit knob.

## 4. NJ3 — the chiral-limit Goldstone survives the lattice cutoff (exact)

In the chiral limit ($m_0=0$) the RPA pseudoscalar pole condition $1-2G\,\Pi_\text{PS}(0)=0$ with $\Pi_\text{PS}(0)=2N_cN_f I_1(M)$ is **identically** the gap equation $1=4GN_cN_f I_1(M)$. With BZ regularization the residual is $|1-2G\Pi_\text{PS}(0)|=3.6\times10^{-15}$ at the self-consistent $M$ — the pion sits at $q^2=0$ to machine precision. **The F77 Goldstone theorem is independent of how the loop is cut off**; moving $\Lambda\to$ zone changes nothing about the exact massless pion. This is the load-bearing consistency check that licenses the $\Lambda\to$ BZ replacement.

## 5. NJ4 — $G$ is an induced coupling (mechanism + order of magnitude)

$G$ is not fundamental. Fierzing one-gluon exchange into the scalar $q\bar q$ channel, with the gluon truncated at the colour-dielectric (dual-Meissner) mass $M_g$ of F86/F88, gives the induced contact

$$G\ \sim\ \frac{N_c^2-1}{2N_c^2}\,\frac{g_s^2}{M_g^2}\ =\ \frac49\,\frac{g_s^2}{M_g^2}\qquad(\text{SU(3) Fierz}=4/9).$$

This is the same Sakharov/induced logic the gravity sector (F57–F61/F79) and the condensate angle (F95) already use. Taking $g_s$ from the rotor lock (F115 CM3, $g_s=\tfrac12$ in the rule normalisation), reproducing the measured $\hat g=G\Lambda^2=2.10$ requires $\Lambda/M_g=4.35$, i.e. a confinement (dielectric) mass a factor $\sim4$ **below** the NJL cutoff — physically exactly where the dual-Meissner scale should sit relative to the chiral scale. So the mechanism is identified and gives $\hat g=O(1\text{–few})$ naturally; the precise $2.10$ needs the full momentum-dependent Fierz reduction (the gluon/dielectric propagator integrated against the lattice loop), which is the open coefficient. The bridge to build on is F88's measured $v=m_D/e=0.713$, $\sigma_\text{F86}=2\pi v^2$.

## 6. $m_0$ — flagged to the texture machinery

The current quark mass $m_0$ (the second dimensionless input) is in the same class as the lepton masses: the orthorhombic $E_g$ condensate texture (F92/F93/F95/F108/F109) extended to the quark sector. The F97 baryon no-go shows the *binding* side uses centre closure, not phase kinematics — but the current-mass texture is still the condensate's job. Not derived here; correctly flagged as the quark-sector extension of the open lepton-spectrum problem (audit #2/#3).

## 7. Net effect on the open ledger

| NJL input | Before | After F116 |
|---|---|---|
| $\Lambda=651.5$ MeV | "fitted cutoff" | a **ruler** ($=$ chiral scale $\sim4\pi f_\pi$); not independent; BZ edge plays its role (NJ1/NJ2) |
| $G\Lambda^2=2.10$ | "fitted" | **induced** by the F86/F88 dielectric, $G\sim\tfrac49 g_s^2/M_g^2$; $G/G_c=1.28$; $O(1)$ from the mechanism (NJ4); exact coefficient open |
| $m_0=5.5$ MeV | "fitted" | quark-sector orthorhombic texture (F92–F109); flagged |

The calibration is reduced from **three fitted numbers** to **one ruler (shared with $a$) + two dimensionless inputs**, with the cutoff structurally re-identified (zone, not knob), the Goldstone theorem shown cutoff-independent, and $G$'s mechanism (induced from confinement) identified. What remains genuinely open: the exact dimensionless $\hat g$ (a Fierz-reduction coefficient) and $\hat m_0$ (the quark texture).

## 8. Check summary (4/4)

| Check | Statement | Tier | Residual/result |
|---|---|---|---|
| NJ1 | $\{\Lambda,G\Lambda^2,m_0\}=$ 1 ruler + 2 dimensionless; $G/G_c=1.28$; $\Lambda\sim4\pi f_\pi$ | accounting | exact |
| NJ2 | lattice-BZ gap equation: finite $g_c=2.196$, continuous chiral SB, no free $\Lambda$ | numeric | $M{=}0$ below, $M{>}0$ above |
| NJ3 | chiral-limit Goldstone $1-2G\Pi_\text{PS}(0)=0$ with BZ cutoff (pion at $q^2{=}0$) | exact/machine | $3.6\times10^{-15}$ |
| NJ4 | induced $G\sim\tfrac49 g_s^2/M_g^2$; reproduces $\hat g$ at $\Lambda/M_g=4.35$ | order of magnitude | mechanism OK |

## 9. Honest scope

- NJ2 uses a simple cubic lattice dispersion $K=\sum2(1-\cos k_i)$, not the exact BCC/F46 dispersion; the structural results (finite $g_c$, continuous chiral SB, $\Lambda\to$ zone) are dispersion-robust, but the *numerical* $g_c=2.196$ is grid/dispersion-specific, not the BCC value. Doublers of the naive term rescale the effective $N_f$; they do not change the existence of $g_c$ or the Goldstone identity.
- NJ4 is an order-of-magnitude mechanism, not a closed coefficient. The Fierz factor $4/9$ and $g_s$-normalisation carry $O(1)$ convention dependence; the claim is "$\hat g=O(1)$ from integrating out the dielectric," not "$\hat g=2.10$ derived."
- $\Lambda$ as "the chiral scale, not a fundamental cutoff" is the right reading because the fundamental BCC zone edge is Planckian ($\sim10^{18}$ GeV), nine decades above $651$ MeV; the NJL is an *effective* theory whose cutoff is the emergent second-shell/chiral scale.

## 10. Provenance

- New content: the dimensional reduction (NJ1), the lattice-BZ gap-equation re-derivation with $\Lambda\to$ zone (NJ2), the cutoff-independent Goldstone check (NJ3), and the induced-$G$ mechanism/estimate (NJ4).
- Reused: F77 gap+RPA structure and $G_c\Lambda^2=\pi^2/6$; F88 dielectric scale; F115 $g_s$ lock; F107 ruler.
- Verification: `model-tests/test_F116_njl_lattice_calibration.py` (2026-06-08, 4/4 PASS), results `test-results/F116_njl_lattice_calibration.json`.
