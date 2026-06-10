# F123 — P6: SI absolute-scale closure for the matter sector — the canonical cell + a single f_π anchor put the nucleon at 3m_c within ~1 % of 938 MeV

**Date:** 2026-06-09 - 17:40
**Status:** Confirmed — 10/10 checks PASS. G0 PREDICTION (inherited from F107/F112, $3.0\times10^{-8}$); H1/H2/H3 matter-sector PREDICTIONs; H4/H6/H7/H8/G1 CONSISTENCY; H5 Tier-3 (one external coupling). Headline ($m_c$, $3m_c=m_p$, $f_\pi$) independently re-derived by direct loop-integral quadrature, agreeing with the module to 10 digits.
**Module:** `ca-simulation/ca_si_scale.py`
**Script:** `tests/findings/test_P6_si_scale.py` (~2 s)
**Results:** `test-results/P6_si_scale.json`
**Cross-references:** [[F107-canonical-a-adoption-L4-grb-gate]] (the geometric SI cell adopted here), [[F112-si-predictions-from-canonical-a]] (the gravity/EW registry this extends to the strong sector), [[F119-kg-scale-three-routes]] (the hierarchy: the cell fixes $a$, not the hadron scale $N$ — which this finding fixes with $f_\pi$), [[F77-njl-gap-rpa]] / [[F103-p3-dynamical-pion-goldstone]] (the dimensionless χSB spectrum anchored here), [[F122-p2-dynamical-baryon-three-body]] (the P2 nucleon whose absolute mass this delivers; resolves its $m_p/\sqrt\sigma$ overshoot), [[F97-baryon-phase-closure-no-go]] (mass is dynamical, not current-quark sum — made quantitative), [[F40-quark-Y-and-dynamical-chi-kinetic]] ($d$–$u$ gap in the $n$–$p$ splitting), [[F104-p4-deuteron-tensor-bound-nucleus]] (deuteron OPEP range now predicted).

---

## 1. What this closes

P2 (F122) produced the proton as a real three-body bound state but could only give a **ratio** $m_p/\sqrt\sigma$ — every absolute MeV was flagged "Tier-B, gated on P6." This finding implements P6 with the project's **current SI choice** and reads off the matter sector in absolute MeV, scoring each number against PDG. It also resolves F122's open flag: the apparent $m_p/\sqrt\sigma$ *overshoot* was an artefact of the non-relativistic Cornell solve with a light current quark; the $f_\pi$-anchored **constituent** route gives the nucleon mass directly and cleanly.

## 2. The SI choice (two independent anchors)

**Geometric cell (metre, second, $G$) — F79/F107, scored in F112.**

$$a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.59782\,\ell_P=1.06638\times10^{-34}\,\text{m},\quad \tau=\frac{a}{c\sqrt3}=2.05366\times10^{-43}\,\text{s},\quad G=\frac{a^2c^3}{8\pi\sqrt3\,\hbar}=6.6743\times10^{-11}$$

(CODATA to $3.0\times10^{-8}$). This fixes length, time and gravity but **not** the hadron mass scale: the cell's own energy unit $\hbar c/a=1.85\times10^{18}$ GeV sits ~18 orders above the GeV world — the F119 hierarchy. The hadron scale is therefore the one genuinely open number, and P6 fixes it with a single hadronic anchor.

**QCD / hadron scale (the strong-sector kilogram) — one number:**

$$f_\pi=92.07\ \text{MeV}\qquad(\text{the chiral-symmetry-breaking order parameter; user-selected}).$$

Every other strong-sector quantity is a **dimensionless model ratio** (the NJL/RPA spectrum of F77/F103, fixed by the dimensionless couplings $\{G\Lambda^2,\,m_0/\Lambda\}$) times this single scale. Only one dimensionful number enters the strong sector.

## 3. The headline — the nucleon mass from one anchor

With $f_\pi$ as the only dimensionful strong input, the NJL gap equation gives a **constituent** quark mass

$$m_c=309.5\ \text{MeV},$$

so the nucleon as three constituents lands at

$$m_p\simeq 3m_c=928.5\ \text{MeV}\qquad(\text{PDG }938.27,\ -1.05\%).$$

This is **F97 made quantitative**: the nucleon mass *is* the dynamical (χSB) constituent mass — not the $\sim$1 % current-quark sum — and the P2 residual confinement/OGE/hyperfine binding is the remaining $\sim$1 %, since the constituent mass already absorbs the bulk. It is also the clean resolution of F122's $m_p/\sqrt\sigma$ overshoot: that number was a non-relativistic-Cornell artefact of using a *light current* quark in a linear well; anchoring on $f_\pi$ and using the *constituent* mass removes it.

## 4. The full scored registry

| # | Quantity | Model (MeV) | PDG | Dev | Tier |
|---|---|---|---|---|---|
| G0 | Newton $G$ (canonical cell) | $6.6743\times10^{-11}$ | CODATA | $3.0\times10^{-8}$ | PREDICTION |
| G1 | model $f_\pi$ vs physical | 92.58 | 92.07 | $+0.56\%$ | CONSISTENCY |
| H1 | constituent $m_c$ (vs $m_N/3$) | 309.5 | 312.97 | $+1.11\%$ | PREDICTION |
| **H2** | **nucleon $m_p\simeq3m_c$** | **928.5** | **938.27** | $\mathbf{-1.05\%}$ | **PREDICTION** |
| H3 | $m_n-m_p$ | $+1.51$ | $+1.293$ | $+0.22$ MeV | PREDICTION |
| H4 | pion $m_\pi$ | 139.7 | 138.04 | $+1.23\%$ | CONSISTENCY |
| H5 | rho $m_\rho$ (KSRF) | 781.2 | 775.26 | $+0.77\%$ | Tier-3 |
| H6 | sigma $m_\sigma$ (in $f_0(500)$ band) | 619.0 | $\sim$400–700 | in band | CONSISTENCY |
| H7 | $\langle\bar qq\rangle^{1/3}$ (sign/order) | $-247.7$ | $\sim-272$ | $+8.9\%$ | CONSISTENCY |
| H8 | deuteron OPEP range $1/m_\pi$ | 1.412 fm | 1.429 fm | $+1.22\%$ | CONSISTENCY |

The $n$–$p$ splitting (H3) is the sharpest matter-sector PREDICTION: it needs **no** QCD anchor — it is the F40 down–up *current*-mass gap ($+2.51$ MeV, neutron-heavier) beating the proton's larger EM self-energy ($-1.00$ MeV), sign positive, $+1.51$ MeV vs the measured $+1.293$.

## 5. The honest open edge

One strong-sector debt remains: the model carries **two** independent QCD calibrations — the F77 χSB scale ($f_\pi$) used here, and the P1 string tension $\sqrt\sigma$ (F70/F94) used in F122 — and connecting them from first principles (deriving the dimensionless ratio $\sqrt\sigma/f_\pi\approx4.6$) is not yet done. Until then $\sqrt\sigma$ is fixed by the same scale as a consistency statement, not an independent prediction. The geometric–hadron hierarchy itself ($\hbar c/a$ vs $f_\pi$, i.e. F119's $N$) is set by the anchor, not derived — the standard status of the hierarchy in any effective theory.

## 6. What P6 adds to the ledger

New module `ca-simulation/ca_si_scale.py`; new suite `tests/findings/test_P6_si_scale.py` (10/10). Exactness rows: Tier-3 #41 (the $f_\pi$-anchored nucleon $3m_c$), #42 (the absolute light-meson spectrum on one anchor). With P6 implemented for the matter sector, the matter-binding roadmap has P0, P1, P2, P3, P4 and (matter-sector) P6 all built; **P5 (atoms)** remains the one open phase, and the cross-cutting $\sqrt\sigma\leftrightarrow f_\pi$ unification is the remaining strong-scale debt.
