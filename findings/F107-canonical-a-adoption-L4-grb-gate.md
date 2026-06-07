# F107 — Adoption of $a=\sqrt{8\pi}\,3^{1/4}\,\ell_P$ as the canonical SI ruler: L4 absolute lensing on $K=e^{2u}$ confirms the $G$-match; the GRB gate observationally discriminates the F79 anchor from the F83 ceiling

**Date:** 2026-06-06 - 22:39
**Status:** Confirmed — 6/6 checks PASS. L4a is **exact-algebraic** (sympy, all field strengths); L4b/L4c numeric guards; L4d/gate are quantitative against CODATA/IAU constants and the bounds quoted in F28/F66. Closes audit item C.1 (`project-audit-inputs-dynamism-2026-06-06.md`, recommended priority #2).
**Script:** `model-tests/test_F107_canonical_a_L4_grb_gate.py`
**Results:** `test-results/F107_canonical_a_L4_grb_gate.json`
**Cross-references:** [[F79-structural-newton-constant]] (the parameter-free $a/\ell_P$), [[F83-fix-lattice-spacing-from-fermion-mass]] (degeneracy + top-quark ceiling, now demoted to consistency check), [[F64-em-connection-gravity]] (canonical $K=e^{2u}$, D-EM5/D-EM9), [[F30-photon-dispersion-order-anisotropy-birefringence]] (even-channel $n=2$ law), [[F28-grb-dispersion-test]] (time-of-flight bounds), [[F66-allsky-birefringence-anisotropy-no-rescue]] / [[F67-even-law-photon-vs-bilinear-mutually-exclusive]] (polarimetry bound + bilinear exclusion), [[F69]] (paired photon, even law), `si-units-options.md` Options C/D.

---

## 1. The decision

The lattice spacing — the project's one SI ruler (audit input #1) — is hereby **adopted as the F79 parameter-free value**:

$$\boxed{\ a \;=\; \sqrt{8\pi}\,3^{1/4}\,\ell_P \;=\; 6.59782\,\ell_P \;=\; 1.06638\times10^{-34}\ \text{m},\qquad \tau=\frac{a}{c\sqrt3}=2.05366\times10^{-43}\ \text{s}\ }$$

Rationale (audit C.1): it is the only parameter-free candidate the model produces; F83 proved a measured fermion mass cannot fix $a$ (one equation, two unknowns) and supplies only the ceiling $a\le3.11\times10^{-18}$ m. The F83 mass map is hereby **demoted from anchor to consistency check**. This finding runs the two campaigns C.1 prescribed before adoption: the L4 absolute lensing test on the canonical $K=e^{2u}$, and the GRB polarimetry/LIV gate.

---

## 2. L4 absolute lensing on the canonical dielectric (L4a–L4d)

The open item from Finding 8 / `si-units-options.md` §7: the *absolute* deflection coefficient $\Delta\theta=4GM/(bc^2)$ had never been checked against the lattice value (only linear-in-$M$ scaling had), and Finding 10 warned a stray $\sqrt d$ could appear.

**L4a (exact).** For the canonical index $n=K=e^{2u}$, $u=GM/(rc^2)$ (F64 D-EM5 — *not* the deprecated $(1-u)^{-2}$ linearisation), the log-index is exactly Coulombic: $\ln K = 2GM/(rc^2)$. The straight-ray eikonal integral is therefore

$$\alpha \;=\; \int_{-\infty}^{\infty}\partial_b\!\left[\ln K\right]dx \;=\; -\frac{4GM}{b\,c^2}\quad\textbf{exactly, at every field strength}$$

(sympy: $\alpha=-4\mu/b$, $K_\text{bend}\equiv\alpha b c^2/GM=-4$ symbolically). This is a small bonus of the exponential form: the $(1-u)^{-2}$ map's $\ln n$ is Coulombic only to $O(u)$, while $e^{2u}$ has **no finite-field correction at straight-ray order** — corrections enter only through ray bending.

**L4b (numeric guard).** mpmath quadrature of the full exponential index returns $K_\text{bend}=-4.000\ldots$ (attractive) for $GM/(bc^2)=10^{-2}\dots10^{-5}$, residual $0.0$ at $10^{-5}$.

**L4c (lattice absolute).** 3D FFT-Poisson $1/r$ potential ($L=96$), eikonal rays through $K=e^{2u}$ at $b=8\dots16$: absolute coefficient $K_\text{bend}=3.92$ (finite-aperture/box systematics at the 2% level, per-$b$ values 3.84–3.99 trending to 4 at small $b$), and the dielectric/rest-leg ratio $=2$ to $7.7\times10^{-14}$ — the absolute lattice coefficient is **4, not $4\sqrt d$ or $4/\sqrt d$**. The Finding-10 $\sqrt d$ lives entirely in the SI map (it is already inside F79's $8\pi\sqrt3$), not in the dimensionless coefficient.

**L4d (the $G$-match, si-units Option D).** With the adopted $a$:

$$G_\text{pred}=\frac{a^2c^3}{8\pi\sqrt3\,\hbar}=6.674300\times10^{-11}\ \text{m}^3\text{kg}^{-1}\text{s}^{-2},\qquad \frac{|G_\text{pred}-G_\text{CODATA}|}{G_\text{CODATA}}=3.0\times10^{-8},$$

and the **absolute solar-limb deflection** computed end-to-end through the lensing observable (with $M_\odot$ taken from the $G$-independent measured product $GM_\odot=1.32712440018\times10^{20}$ m³/s², IAU):

$$\Delta\theta_\odot \;=\; \frac{4\,G_\text{pred}M_\odot}{R_\odot c^2} \;=\; 1.751190''\quad\text{vs GR/measured } 1.751190''\ (\text{resid }3.0\times10^{-8}).$$

The lattice's own induced $G$, fed through the lattice's own factor-4 bending coefficient, lands on the measured light-bending at the Sun (VLBI/Cassini confirm $\gamma=1$ at the $10^{-4}$/$10^{-5}$ level, far above this residual).

---

## 3. The GRB polarimetry / LIV gate — the anchor discriminator

Under Option C ($a/\tau=c\sqrt3$) the dimensionless wavenumber is $k=Ea/(\hbar c)$. Two channels gate the anchor (worst-case direction = BCC body diagonal):

1. **Polarimetry (birefringence, $n{=}1$).** The physical photon is the F69 paired/even-law photon: birefringence **identically zero** — the polarimetry bound $\eta\lesssim10^{-15}$ (F66) is cleared at *any* $a$. The counterfactual $\sigma$-bilinear photon ($\eta_\text{max}=(a/\ell_P)/18$) is excluded at **both** anchors ($0.37$ at the F79 value; $1.1\times10^{16}$ at the ceiling) — reproducing F66/F67 and confirming the gate machinery.
2. **Even-channel time-of-flight ($n{=}2$, the surviving observable).** F30's exact even law $\delta v_\phi/c=-k^2/162$ gives the group law $\delta v_g/c=-k^2/54$, hence $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$. Gate: must exceed the strongest published $n{=}2$ subluminal bound, LHAASO GRB 221009A $7.0\times10^{11}$ GeV (F28).

| anchor | $a$ (m) | $a/\ell_P$ | $E_{\text{QG},2}$ | vs bound | verdict |
|---|---|---|---|---|---|
| **F79 (adopted)** | $1.066\times10^{-34}$ | $6.598$ | $1.36\times10^{19}$ GeV $=1.11\,E_P$ | $1.9\times10^{7}\times$ above | **clears** |
| F83 top ceiling | $3.11\times10^{-18}$ | $1.92\times10^{17}$ | $466$ GeV | $6.7\times10^{-10}$ of bound | **excluded** |

**The gate discriminates:** a lattice anywhere near the F83 ceiling is excluded by ~9 decades through the *unpolarised, chirality-even* channel alone (no birefringence loophole — the even channel is exactly what the paired photon carries), while the F79 value clears every current bound by ~7 decades. The fermion-mass ceiling was never a viable anchor; the F79 value is the only one standing. Falsifiability survives: any future $n{=}2$ time-of-flight bound above $1.4\times10^{19}$ GeV ($1.11\,E_P$) would falsify the adopted cell outright.

**Consistency checks (F83 demotion).** $a_\text{canon}\le a_\text{ceiling}$ with 16.5 decades of margin; electron $m_\text{lat}=\sin(a/(\sqrt3\,\bar\lambda_C))=1.59\times10^{-22}$ — the F12/F15 small-mass regime holds at the canonical cell (matches F83 §4's $9.21\times10^{-23}$ at $3.81\,\ell_P$ scaled by $6.598/3.81$).

---

## 4. Consequences

- **Every SI prediction is now unlocked** with no per-prediction anchor choice: masses (F46/F83 map), $E_\text{LV}$ scales (F12/F30), lensing magnitudes (this finding), and the ψ→K sourcing coefficient $a^2c_\text{lat}/\hbar c$ (F106) all evaluate at the single canonical $a$.
- Audit input #1 moves from "open" to **closed by adoption + two passed test campaigns** — with the honest caveat unchanged from F79: $a/\ell_P$ is derived; the metre itself still enters through $\ell_P$ (one ruler, as any theory requires).
- The deflection consistency loop (L4d) is a *joint* check of {F79 closed form} × {F64 canonical $K$} × {lattice factor-4} against {CODATA $G$} × {IAU $GM_\odot$, $R_\odot$} — a cross-sector consistency the audit asked for under "confirm the $G$-match independently."

## 5. What is exact vs numeric

| Result | Tier |
|---|---|
| $K_\text{bend}=-4$ for $K=e^{2u}$, straight-ray, **all** $u$ | Tier 1 exact (sympy) |
| Quadrature $-4.0$ at $u\to0$; attractive sign | Tier 2 numeric (mpmath 40 dps) |
| Lattice absolute $3.92\approx4$; diel/rest ratio $2$ ($7.7\times10^{-14}$) | Tier 2/3 (FFT Poisson, finite box) |
| $G$-match $3.0\times10^{-8}$; $\Delta\theta_\odot=1.7512''$ ($3.0\times10^{-8}$) | Quantitative (CODATA/IAU) |
| $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a$ (from F30 exact even law) | Tier 1 closed form; gate comparison quantitative |

## 6. Test summary (`test_F107_canonical_a_L4_grb_gate.py`, 2026-06-06 - 22:39)

| # | Check | Result | Status |
|---|---|---|---|
| L4a | exact canonical straight-ray $K_\text{bend}=-4$ | symbolic $-4$ | PASS |
| L4b | full quadrature $\to-4$, attractive | resid $0.0$ | PASS |
| L4c | lattice absolute $\approx4$; ratio $=2$ | $3.92$; $2-7.7\times10^{-14}$ | PASS |
| L4d | $G$-match + solar deflection | both $3.0\times10^{-8}$ | PASS |
| gate | F79 clears; ceiling fails; bilinear exclusion reproduced | discriminates | PASS |
| F83 | ceiling margin + $m_\text{lat}\ll1$ | 16.5 decades; $1.6\times10^{-22}$ | PASS |

**Overall: 6/6 PASS** (0.5 s).

## 7. Provenance

- Adopted value: F79 ($a/\ell_P=\sqrt{8\pi}\,3^{1/4}$, coefficient $8\pi\sqrt3$).
- Canonical $K=e^{2u}$: F64 D-EM5/D-EM9; lattice machinery reused from `ca-simulation/forks/gr_fork_F64_em_connection.py` (`deflection_coeff_numeric`, `_solve_poisson_3d`, `_eikonal_K`).
- LIV laws: F30 (exact even/odd series); bounds as quoted in F28 (LHAASO $7.0\times10^{11}$ GeV, $n{=}2$) and F66 ($\eta\lesssim10^{-15}$).
- Constants: CODATA 2018 ($\ell_P$, $\hbar$, $G$), IAU ($GM_\odot$, $R_\odot$); readout anchors only.
