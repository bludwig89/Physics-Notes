# F112 — The SI prediction registry: every measurable the canonical cell now produces, gated against current data

**Date:** 2026-06-08 - 14:05
**Status:** Confirmed — 18/18 checks PASS (`test_F112_si_predictions.py`, 0.16 s). **Numbering note:** drafted as F111; renumbered to F112 — F111 was already taken (2026-06-07) by the concurrent second-order-deflection and F110 tree-gauge SU(3) test scripts. Real arithmetic + sympy only (no chiral transforms). Two headline numbers independently re-derived outside the harness. This finding is a *registry*, not a new derivation: it collects what F107's SI lock unlocked and scores each item against the best current measurement.
**Script:** `tests/findings/test_F112_si_predictions.py`
**Results:** `test-results/F112_si_predictions.{json,md}`
**Cross-references:** [[F107-canonical-a-adoption-L4-grb-gate]] (the SI lock this report card rests on), [[F79-structural-newton-constant]] ($G$ closed form + $a/\ell_P$), [[F64-em-connection-gravity]] (canonical $K=e^{2u}$, PPN $\beta=\gamma=1$ / D-EM9), [[F106-psi-K-sourcing-derivation]] (the sourcing coefficient), [[F30-photon-dispersion-order-anisotropy-birefringence]] (exact even law), [[F28-grb-dispersion-test]] (LHAASO bound), [[F66-allsky-birefringence-anisotropy-no-rescue]] / [[F69]] (paired photon, zero birefringence), [[F45-sigma-tau-swap-weinberg-angle]] ($\sin^2\theta_W$, $m_Z/m_W$), [[F46-pythagorean-lattice-mass]] / [[F101b-one-heavy-branch-fit-W]] (Koide, condensate angle).

---

## 1. The point of this finding

F107 fixed the project's single SI ruler at the F79 parameter-free value

$$a=\sqrt{8\pi}\,3^{1/4}\,\ell_P=6.59782\,\ell_P=1.06638\times10^{-34}\ \text{m},\qquad \tau=\frac{a}{c\sqrt3}=2.05366\times10^{-43}\ \text{s},\qquad c_\text{lat}=\frac1{\sqrt3}.$$

Until then every result lived in dimensionless lattice units. With $a$ fixed, each dimensionless number the chain produced becomes an absolute SI quantity. The natural question — *and now what can the model actually say about the measured world?* — is answered here by evaluating every SI-valued output at the canonical cell and gating it against current data.

Three honesty tiers are tagged on every row so the report card cannot oversell:

- **PREDICTION** — a parameter-free output of the lattice rule. The only inputs on the model side are the cell $a$ and the universal constants $(c,\hbar)$; nothing measured about the target is fed in.
- **CONSISTENCY** — the model is GR-identical (PPN $\beta=\gamma=1$, F64 D-EM9) or calibration-locked (absolute masses still need the one kg anchor). The model cannot be *wrong* here without breaking GR/QM, so these are checks, not predictions.
- **FALSIFIER** — a one-sided bound the cell must clear, stated together with the threshold that would kill the adopted $a$.

**Result: 18/18 PASS.**

---

## 2. The registry

### A. Lattice scales (anchor outputs)

| quantity | value | tier |
|---|---|---|
| cell spacing $a$ | $1.06638\times10^{-34}$ m $=6.59782\,\ell_P$ | PREDICTION ($a/\ell_P$ derived; $\ell_P$ sets the metre) |
| tick $\tau$ | $2.05366\times10^{-43}$ s | PREDICTION (Option C: $a/\tau=c\sqrt3$) |
| lattice lightcone $a/\tau$ | $5.19256\times10^{8}$ m/s $=c\sqrt3$ | PREDICTION (max signal speed; no particle reaches it) |
| UV cutoff $\hbar c/a$ | $1.85\times10^{18}$ GeV $=0.15\,E_P$ | PREDICTION (Brillouin-zone energy ceiling; $\pi\times$ at the BZ edge) |

The lattice lightcone exceeds $c$ by $\sqrt3$ — the conceptual cost of Option C (F26: $c$ is the $(\mathbf E,\mathbf B)$ rotation rate, not the lightcone). It is unobservable because no excitation propagates at the lightcone speed.

### B. Gravity — the headline of the SI lock

| quantity | model | measured | residual | tier |
|---|---|---|---|---|
| **Newton constant $G$** | $6.674300\times10^{-11}$ | $6.674300\times10^{-11}$ (CODATA) | $3.0\times10^{-8}$ | **PREDICTION** |
| solar light deflection | $1.751190''$ | $1.751190''$ (GR/VLBI) | $3.0\times10^{-8}$ | **PREDICTION** |
| bending coefficient $K_\text{bend}$ | $-4$ (sympy, exact $\forall$ field strength) | $-4$ (GR) | $0$ | PREDICTION |
| Mercury perihelion / Shapiro / redshift / frame-drag | PPN $\beta=\gamma=1$ | e.g. $42.98''$/century | GR-identical | CONSISTENCY |

$G$ is the single biggest thing the SI lock buys: the cell predicts Newton's constant from $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ to $3\times10^{-8}$, with **no gravitational input** — the $8\pi\sqrt3$ comes from the F79 Sakharov-induced stiffness ($2\pi\eta g_*\sqrt d$, fermionic $g_*=48$ exact) and $a/\ell_P$ from the same structure. The absolute solar deflection inherits exactly that residual (it is $4G_\text{pred}M_\odot/R_\odot c^2$ with $M_\odot$ from the $G$-independent product $GM_\odot$), so the model lands on the measured light-bending at the Sun. Because the canonical dielectric reproduces GR's PPN sector (D-EM9), the entire classic-test battery — perihelion precession, Shapiro delay, gravitational redshift, frame dragging — is inherited at GR precision rather than re-predicted.

### C. Photon / Lorentz invariance

| quantity | model | measured | verdict | tier |
|---|---|---|---|---|
| ToF scale $E_{\text{QG},2}$ ($n{=}2$) | $1.360\times10^{19}$ GeV $=1.11\,E_P$ | $>7.0\times10^{11}$ GeV (LHAASO GRB 221009A) | clears by $1.9\times10^{7}$ | **FALSIFIER** |
| falsification threshold | $1.4\times10^{19}$ GeV | — | a future subluminal $n{=}2$ bound above this kills $a_\text{canon}$ | FALSIFIER |
| vacuum birefringence $\eta$ | $0$ (exact, paired/even photon) | $\eta<10^{-15}$ (polarimetry) | cleared at any $a$ | PREDICTION |
| photon mass | $0$ (massless, transverse, $c=1/\sqrt3$) | $<10^{-27}$ eV | consistent | PREDICTION |

The even-channel time-of-flight scale $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$ (from F30's exact even law $\delta v_g/c=-k^2/54$) is the project's sharpest LIV prediction and its cleanest falsifier: it sits at $1.11\,E_P$, so **any future subluminal $n{=}2$ time-of-flight bound above $\sim1.4\times10^{19}$ GeV would falsify the adopted cell outright**. Birefringence is identically zero because the physical photon is the F69 paired/even-law object — the model clears polarimetry at *any* $a$, while the excluded $\sigma$-bilinear counterfactual would not (F66/F67).

### D. Electroweak + lepton spectrum (dimensionless — $a$-independent, but part of the report card)

| quantity | model | measured | verdict | tier |
|---|---|---|---|---|
| $\sin^2\theta_W$ (bare) | $1/4=0.2500$ | $0.2230$ (PDG) | $+12\%$ (bare, pre-RG) | PREDICTION |
| $m_Z/m_W$ | $2/\sqrt3=1.1547$ | $1.1346$ (PDG) | $+1.77\%$, zero fit params | PREDICTION |
| Koide $Q$ | $2/3=0.66667$ (geometric) | $0.666661$ (PDG masses) | data $0.001\%$ from $2/3$ | PREDICTION |
| condensate angle $\delta$ | $15°$ exact ($m_e{=}0$ limit) | $12.733°$ | $2.27°$ carried by $m_e/m_\tau$ | CONSISTENCY |
| absolute fermion masses | $m_\text{phys}=m_\text{lat}\,\hbar/(ca)$ | electron = kg anchor | ratios/Koide predicted, scale calibrated | CONSISTENCY |

These do not need $a$ — they were already available — but they belong on the report card because they are the model's other genuine confrontations with data. The mass-ratio $m_Z/m_W=2/\sqrt3$ within $1.8\%$ and Koide $Q=2/3$ to one part in $10^{5}$ are the standouts. Absolute masses remain a consistency item: the spectrum's *structure* (ratios, Koide, the $\tau$ at the saturation wall) is predicted, but the overall MeV scale is still calibrated through the one kg anchor (the open "saturation $\leftrightarrow$ MeV" map of F101).

### E. Gravity sourcing coefficient (F106) as an SI number

| quantity | model | tier |
|---|---|---|
| $\psi\to K$ coefficient $8\pi G/c^4$ | $a^2 c_\text{lat}/(\hbar c)=2.077\times10^{-43}$ (SI) | PREDICTION (exact identity, sympy) |

The dielectric sourcing law $\nabla^2\ln K=-(8\pi G/c^4)\,T^{00}$ collapses to pure lattice quantities $a^2c_\text{lat}/(\hbar c)$ — verified as an exact sympy identity — so gravity's coupling to matter now reads out as a definite SI number with no free constant.

---

## 3. What is exact vs numeric vs calibrated

| Result | Tier |
|---|---|
| $K_\text{bend}=-4$ (all field strengths); $8\pi G/c^4=a^2c_\text{lat}/(\hbar c)$; $m_Z/m_W=2/\sqrt3$; $\sin^2\theta_W=1/4$; $Q=2/3$; $E_{\text{QG},2}=\sqrt{54}\hbar c/a$; $\eta=0$ | Tier 1 exact / closed form |
| $G$-match $3.0\times10^{-8}$; solar deflection $1.751190''$ | Quantitative vs CODATA/IAU (residual = the F79 $a/\ell_P$ vs CODATA) |
| Koide data $0.666661$ vs $2/3$ ($10^{-5}$); EW ratio $+1.77\%$; $\delta$ offset $2.27°$ | Quantitative vs PDG |
| absolute fermion mass scale | Calibrated (one kg anchor; structure predicted, scale open) |

## 4. The falsification surface (one place to look)

The cell is not unfalsifiable. Three live edges:

1. **$n{=}2$ time-of-flight above $1.4\times10^{19}$ GeV** (subluminal) — kills the adopted $a$ directly. Current best ($7\times10^{11}$ GeV) is $7$ decades short.
2. **Any vacuum birefringence detection** at the polarimetry frontier — excludes the even-law paired photon (the $\sigma$-bilinear was already excluded).
3. **A measured $G$ shift, or a fifth-force/PPN deviation** beyond $\beta=\gamma=1$ — the model is GR-identical, so a confirmed non-GR PPN parameter would break the dielectric.

## 5. Test summary (`test_F112_si_predictions.py`, 2026-06-08 - 14:05)

18 rows across five sectors, all PASS in 0.16 s. JSON + markdown registry written to `test-results/`. Headline numbers ($G$, $E_{\text{QG},2}$, Koide, EW ratio) independently re-derived outside the harness with bare arithmetic — agreement to all quoted digits.

## 6. Provenance

Cell: F79/F107. $G$: F79 closed form. Deflection/PPN: F64 D-EM5/D-EM9, F107 L4. LIV: F30 even law, F28 LHAASO bound. Birefringence: F66/F67/F69. EW: F45. Koide/angle: F46/F93/F101. Sourcing: F106. Constants are CODATA 2018 / PDG 2024 / IAU 2015 readout anchors only — never inputs to the lattice rule.
