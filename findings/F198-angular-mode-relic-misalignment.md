# F198 — The F197 relic obstruction, computed: vacuum-misalignment of the $E_g$ **angular** mode under-produces by ~15 orders at the condensate scale ($\Omega\propto f^2$ needs $f\sim10^{13}$–$10^{16}$ GeV, but $f\sim v/2$); the **amplitude** mode via thermal freeze-out lands in the WIMP window — so the $E_g$ dark-matter relic is the heavy mode, not the light one

**Date:** 2026-06-30 - 20:05
**Numbering:** **F198** (re-checked; prior max F197).
**Status:** **Sharpens, does not close, the F197 obstruction; flips the candidate.** Standard ALP misalignment instantiated with the condensate's own parameters. The scaling is exact textbook physics; the scale numbers are order-of-magnitude (representative $g_*$, $\theta_i$). Honest negative result for the angular mode + a viable positive route for the amplitude mode. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F198_angular_misalignment.py` (self-contained, real arithmetic).
**Tests / results:** `tests/findings/test_F198_angular_misalignment.py` → `test-results/F198_angular_misalignment_test.json` (5/5); fork dump `test-results/F198_angular_misalignment.json`.
**Cross-references:** [[F197-first-excitation-dark-source]] (the obstruction this computes; F197 tentatively named the light angular mode the DM candidate — this finding corrects that to the amplitude mode), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ condensate and its angular mode), [[F73-spin0-bound-pair-scalar]] (the amplitude/Higgs-like mode at $\sim v/2$), [[F150-eg-sextic-brake-from-architecture]] / [[F154-residuals-A-B-built-and-solved]] (the sextic $\lambda_6$ that sets the angular-mode mass), [[F170-lepton-colour-scale-link]] / [[F44-stueckelberg-scale]] (the condensate scale $f\sim v/2$ or $\sim\Lambda_\text{QCD}$), [[F196-dilution-exponent-derived]] (the $\Omega_\Lambda$ coincidence — the dark-energy analog of this $\Omega_\text{DM}$ problem). External: standard ALP vacuum-misalignment relic (Preskill–Wise–Wilczek 1983; Arias et al. 2012); WIMP thermal freeze-out (Lee–Weinberg; "WIMP miracle").

---

## What F197 left open

F197 showed the $E_g$ second-shell condensate is the unique near-vacuum channel that can be both smooth-cosmic ($w=-1$ VEV) and clustering-galactic (gapped cold modes), and tentatively flagged the **light angular mode** (axion-like, mass set by the small IR sextic $\lambda_6$) as the natural dark-matter candidate. The single remaining obstruction was the **relic abundance**: why $\Omega_\text{DM}h^2\approx0.12$ (~5× baryons)? This finding computes it via the obvious mechanism for a light pseudo-Goldstone — **vacuum misalignment** — and gets an instructive answer.

## The misalignment calculation

The angular mode $\delta$ is frozen by Hubble friction until $3H\simeq m_a$, then oscillates as cold matter. The standard constant-mass ALP relic is
$$\rho_\text{osc}=\tfrac12 m_a^2 f^2\theta_i^2,\qquad \frac{n_a}{s}=\text{const after onset},\qquad \Omega_a h^2\propto m_a^{1/2}\,f^2\,\theta_i^2,$$
with $f$ the decay constant (the condensate amplitude) and $\theta_i$ the initial misalignment. The fork reproduces this scaling exactly (×4 mass → ×2 $\Omega$; ×2 $f$ → ×4; ×2 $\theta_i$ → ×4).

The decisive feature is $\Omega\propto f^2$: a **low** decay constant must be compensated by a **high** mass ($m_a\propto f^{-4}$ at fixed $\Omega$). The $E_g$ condensate's natural scale is the F73/F44 Stueckelberg value $f\simeq v/2=123$ GeV (or, via F170, $\sim\Lambda_\text{QCD}\sim0.3$ GeV) — both far too low.

| input | value | consequence |
|---|---|---|
| natural $f=v/2$ | $123$ GeV | $m_a$ for $\Omega_\text{DM}$: $8.4\times10^{28}$ GeV — **trans-Planckian** ($7\times10^9\,M_\text{Pl}$) |
| light mode ($\lambda_6=0.05$, $f=123$ GeV) | $m_a\approx27$ MeV | $\Omega h^2=6.9\times10^{-17}$ — **under-produces by $1.8\times10^{15}$** |
| axion-window mass | $m_a\sim1\ \mu\text{eV}$ | needs $f\approx1.2\times10^{13}$ GeV $=10^{11}\times$ the condensate scale |
| $\Omega=0.12$ contour | — | $f\sim10^{10}$–$10^{16}$ GeV across $m_a\in[\text{TeV},\ \mu\text{eV}]$ |

**Verdict for the angular mode: misalignment fails at the condensate scale by ~15 orders.** A light $E_g$ angular mode is hopelessly under-abundant; reaching $\Omega_\text{DM}$ would require pushing $f$ up to the intermediate/GUT scale ($10^{13}$–$10^{16}$ GeV), which the electroweak/QCD-scale $E_g$ condensate does not supply. (The lattice *does* carry a near-Planckian fundamental scale via $a\sim6.6\,\ell_P$, so a *different*, high-scale lattice condensate could host such a mode — but that is not the lepton-mass $E_g$ condensate.)

## The amplitude mode rescues it — via freeze-out, not misalignment

The other gapped mode of the same condensate is the **heavy amplitude (Higgs-like) scalar** at $\sim v/2$ to TeV (F73). A heavy scalar does not misalign; it **thermally freezes out**. With an electroweak-strength annihilation coupling, $\langle\sigma v\rangle\sim g^4/(16\pi m^2)$ lands near the canonical thermal cross section $3\times10^{-26}\ \mathrm{cm^3/s}$:

| $m_\chi$ | $g$ | $\langle\sigma v\rangle$ (cm³/s) | $\Omega h^2$ |
|---|---|---|---|
| 3000 GeV | 1.0 | $2.6\times10^{-26}$ | **0.14** (≈ target) |
| 1000 GeV | 0.65 | … | $O(0.1)$ |
| 100–300 GeV | 0.3–0.65 | … | within ~1–2 orders, tunable |

The WIMP-miracle window $\Omega h^2\approx0.12$ is reachable for a TeV-scale amplitude mode with weak coupling — in stark contrast to the angular mode's 15-order misalignment miss.

## The corrected picture (updating F197)

- The $E_g$ sector's **dark-matter relic is the heavy amplitude mode** (WIMP-like thermal freeze-out), **not** the light angular mode (axion-like misalignment), reversing F197's tentative identification.
- The light angular mode is **under-abundant** — at most a sub-dominant component or, if very light and still frozen, a contribution to the $w=-1$ dark-energy budget (F196), not the cold dark matter.
- The clustering/collisionless properties established in F197 (gapped → cold, small $\lambda_6$ → collisionless, sources the local F64 dielectric) **still hold for the amplitude mode**; only the production mechanism and the mass scale change.

## What is derived vs computed vs posited

| Piece | Status |
|---|---|
| misalignment scaling $\Omega\propto m_a^{1/2}f^2\theta_i^2$ | **Derived** (standard; reproduced exactly) |
| angular mode at $f=v/2$ needs trans-Planckian $m_a$ | **Computed** (order-of-magnitude) |
| light angular mode under-produces by $\sim10^{15}$ | **Computed** |
| axion window needs $f\sim10^{13}$–$10^{16}$ GeV | **Computed** |
| amplitude mode hits the WIMP window | **Computed** (NDA $\langle\sigma v\rangle$; representative $m,g$) |
| relic identity = amplitude (not angular) mode | **Inferred** from the two computations |
| exact $\Omega_\text{DM}=0.26$ from a derived $(m_\chi,g)$ | **Open** — needs the amplitude mode's actual mass and couplings |

## Caveats (honest scope)

- Representative $g_*=80$, $\theta_i=1$, $s$-wave NDA cross section; the numbers are order-of-magnitude, not a fit. The **15-order** misalignment miss is far larger than any of these uncertainties, so the qualitative verdict is robust; the freeze-out "within ~1–2 orders" is genuinely tunable and only indicates the window is reachable.
- The amplitude mode's actual mass and annihilation channels are not derived here (they ride on F73's binding dynamics and the EW couplings); pinning $\Omega_\text{DM}=0.26$ requires them.
- Anharmonic/$\theta_i\to\pi$ enhancements give $O(1)$–few factors, not orders — they do not save the angular-mode route.

## Relation to other findings

Computes the **F197** relic obstruction and **flips its candidate**: the $E_g$ dark-matter relic is the heavy amplitude mode (freeze-out), not the light angular mode (misalignment), which under-produces by ~15 orders because $\Omega\propto f^2$ and the condensate scale $f\sim v/2$ (F44/F73/F170) is far below the $10^{13}$–$10^{16}$ GeV a light ALP would need. Uses **F150/F154**'s $\lambda_6$ for the angular-mode mass and **F73** for the amplitude mode. Leaves the precise $\Omega_\text{DM}=0.26$ (now a freeze-out $(m_\chi,g)$ determination) as the residual — the dark-matter analog of the **F196** $\Omega_\Lambda$ coincidence.
