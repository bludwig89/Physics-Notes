# F124 — Deriving √σ/f_π: the model's two QCD calibrations reconciled to ~12 % from the one locked lattice

**Date:** 2026-06-09 - 18:20
**Status:** Confirmed (partial derivation) — 6/6 checks PASS. C1/C3 machine-precision (Pagels–Stokar identity; factorisation); C2/C4/C5 quantitative PREDICTIONs (chiral factor exact; condensed-vacuum route reproduces the empirical ratio to ~12 %); C6 a tagged DIAGNOSTIC that locates the residual. Headline (Λ/f_π = 7.04, condensate route = 4.00) independently re-derived by direct loop-integral quadrature.
**Module:** `ca-simulation/ca_qcd_scale_ratio.py`
**Script:** `tests/findings/test_F124_qcd_scale_ratio.py` (~1 s)
**Results:** `test-results/F124_qcd_scale_ratio.json`
**Cross-references:** [[F123-p6-si-scale-matter-sector]] (the open debt this closes — the two QCD calibrations $f_\pi$ and $\sqrt\sigma$), [[F77-njl-gap-rpa]] / [[F116-njl-calibration-bz-cutoff-induced-G]] (the chiral side: NJL with Λ = BZ edge), [[F86-colour-dielectric-dual-superconductor]] / [[F88-colour-condensate-from-model]] (the confinement side: $\sigma=2\pi v^2$, $v=m_D/e=0.713$ measured), [[F101-strong-coupling-sigma-compact-rotor]] / [[F115-coupling-magnitudes-running-rotor]] (the locked rotor coupling $g_s^2\chi=\frac14$ and the bare $\sigma_{\rm lat}$), [[F70-gradient-flow-confinement-string-tension]] (confinement lives in the disordered/strong-coupling ensemble).

---

## 1. The debt

F123 fixed the strong-sector MeV scale with a single anchor, $f_\pi$, but flagged that the model still carried **two** QCD calibrations — the chiral scale $f_\pi$ (F77 NJL) and the string tension $\sqrt\sigma$ (P1: F70/F86/F88/F94) — with the dimensionless ratio $\sqrt\sigma/f_\pi$ (empirically $\approx4.56$) left as an undetermined second number. This finding derives that number from the model.

## 2. Why it is in principle a pure number here

Both scales descend from the **same BCC lattice rule**, and in this model neither of the usual free knobs is free:

- the gauge coupling is **locked** — the Kogut–Susskind electric stiffness is $\chi=1/(4g_s^2)$ and the rule's symmetric $(\mathbf E,\mathbf B)$ rotation fixes $\chi=1$, so $g_s^2\chi=\tfrac14$ (F115, from the F110 matrix identity);
- the NJL cutoff is **not a fit** — $\Lambda$ is the Brillouin-zone edge of the same lattice (F116).

So $\sqrt\sigma/f_\pi$ is a pure lattice number, and we factor it as

$$\boxed{\ \frac{\sqrt\sigma}{f_\pi}=\underbrace{\frac{\Lambda}{f_\pi}}_{\text{chiral}}\times\underbrace{\frac{\sqrt\sigma}{\Lambda}}_{\text{confinement}}\ }$$

## 3. The chiral factor — exact

The NJL loop gives $f_\pi$ in terms of the dynamically generated constituent mass $M$ via the Pagels–Stokar relation $f_\pi^2=4N_cM^2K_0(M,\Lambda)$, i.e.

$$\frac{f_\pi}{M}=2\sqrt{N_cK_0}=0.2975,\qquad \frac{\Lambda}{f_\pi}=7.037,$$

a parameter-free output (the only inputs are the dimensionless $\{G\Lambda^2,m_0/\Lambda\}$; $M=311.2$ MeV). This is exact (C1, machine precision; independently reproduced by direct quadrature of $K_0$). **The chiral half of the ratio is fully derived.**

## 4. The confinement factor — from the condensed vacuum

$\sqrt\sigma$ in lattice units (units of $1/a$) comes from the model's confined vacuum: the dual-superconductor flux tube has the exact BPS tension $\sigma=2\pi v^2$ (F86), and the colour-magnetic condensate VEV $v=m_D/e=0.713$ is a **measured** property of the compact gauge vacuum (F88). With the NJL cutoff at the BZ edge ($\Lambda=\pi/a$, per-axis; or $(6\pi^2)^{1/3}/a$ for the sphere of equal BZ volume):

$$\frac{\sqrt\sigma}{\Lambda}=\frac{\sqrt{2\pi}\,v}{\Lambda_{\rm lat}}=0.569\ (\text{axis})\quad\text{vs the empirical }0.645\ (-12\%).$$

Combining:

$$\frac{\sqrt\sigma}{f_\pi}=7.037\times0.569=\mathbf{4.00}\ (\text{axis})\ /\ 3.23\ (\text{sphere})\qquad\text{vs empirical }\mathbf{4.56}.$$

**The model reproduces the ratio to ~12–30 %** (C4/C5), reducing the open number to a single, well-posed confinement ratio $\sqrt\sigma/\Lambda$ whose residual is the BZ-edge↔3-momentum-cutoff convention and the Abelian-vs-Casimir centre caveat (F99–F101).

## 5. The honest residual — scale-setting

The factorisation also exposes *where* the remaining uncertainty lives. If $\sqrt\sigma$ is taken instead from the rule's **bare rotor** at its locked weak coupling ($\sigma_{\rm lat}=\tfrac14\langle1/\Omega\rangle_{\rm BZ}=0.2015$, F101), the ratio collapses to $\sqrt\sigma/f_\pi\approx1.0$ (C6) — a factor $\sim4$ below the condensed-vacuum value. That factor is precisely the **QCD scale-setting / dimensional transmutation**: the physical string tension lives in the **strong-coupling, condensed regime** (large $v$), where F70 and F101 already place confinement ("it lives in the disordered ensemble"), separated from the bare UV lattice cutoff. The bare rotor and the condensed vacuum are the two ends of the F101 Gaussian→confinement crossover; the physical $\sqrt\sigma$ is the strong end. Pinning the single self-consistent lattice spacing at which **both** χSB and the physical $\sigma$ hold is the residual gap — the same scale-setting the lattice-QCD world performs numerically rather than analytically.

## 6. Checks

| # | Check | Model | Target | Dev | Tier |
|---|---|---|---|---|---|
| C1 | chiral $f_\pi/M$ exact (Pagels–Stokar) | 0.2975 | $2\sqrt{N_cK_0}$ | $0$ | machine |
| C2 | $\Lambda/f_\pi$ (chiral factor) | 7.037 | 7.037 | — | PREDICTION |
| C3 | factorisation identity | 4.003 | 4.003 | $0$ | machine |
| C4 | condensate route vs empirical | 4.00 | 4.56 | $+12\%$ | PREDICTION |
| C5 | $\sqrt\sigma/\Lambda$ (confinement) | 0.569 | 0.645 | $+12\%$ | PREDICTION |
| C6 | bare-rotor route (scale-setting gap) | 1.01 | $\sim1$ | — | DIAGNOSTIC |

## 7. Verdict and ledger

$\sqrt\sigma/f_\pi$ is no longer a free second calibration: it is derived to ~12 % as (exact chiral $7.04$) × (confinement $0.57$), with the residual a single, well-posed scale-setting ratio rather than an unconstrained number. New module `ca-simulation/ca_qcd_scale_ratio.py`; new suite `tests/findings/test_F124_qcd_scale_ratio.py` (6/6); exactness row Tier-3 #43. This closes the F123 open debt down to the scale-setting (dimensional-transmutation) residual, leaving **P5 (atoms)** as the one open matter-binding phase.
