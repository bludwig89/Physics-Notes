# F249 — Quantitative QED comparison battery for the paired-spinor photon

**Date:** 2026-07-16 - 09:40
**Status:** Confirmed — 9/9 computed checks PASS (Tier A tree/classical + Tier B photon-precision), 3 Tier-C radiative items recorded as an honest reference ledger (the model has no interacting loop sector yet). Standalone runnable battery + pytest.
**Module / script:** `tests/findings/test_F249_qed_comparison_battery.py` (runs standalone: `python3 tests/findings/test_F249_qed_comparison_battery.py --json out.json`)
**Results:** `test-results/F249_qed_comparison_battery.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the object under test), [[F68-minimal-coupling-forces-even-photon]], [[F87-charge-coupling-paired-photon]] (Ward/Gauss/Coulomb machinery), [[F125-p5-hydrogen-atom-em-bound-state]] (Dirac fine structure; Lamb shift flagged open), [[F105-axial-photon-exactly-dispersionless]] (exact axial linearity), [[F28-grb-dispersion-test]] (LIV bound), [[F168-paired-photon-binding-gauge-protected]], [[F169-photon-interacting-two-body-wavefunction]] (the open loop/gauge-pole item this ledger points at).

---

## Purpose

Answer the question left open by the F69 review: does the paired-spinor photon reproduce **quantitative** electrodynamics, or only the qualitative photon? This battery confronts the actual `ca_*` modules with measured QED in three tiers, and is deliberately **honest about the gap** — radiative-precision observables the model cannot yet derive from loops are computed as reference values with the specific missing machinery named, not faked.

All reference constants are CODATA-2022 / PDG / measured (listed in the script's `REFERENCES` and §"Reference values" below). The battery uses closed-form `arccos` dispersion + real FFT/linear algebra only (no `eig` on chiral matrices, per CLAUDE.md).

## Tier A — tree / classical QED (the model computes)

| # | Check | Model | Target | Result |
|---|-------|-------|--------|:------:|
| A1 | photon masslessness $\Omega_\text{pair}(0)$ | $0$ | $0$ | exact, PASS |
| A2 | luminality $v_g=d\Omega/d\lvert k\rvert$ (k→0), all directions | $0.57735$ | $1/\sqrt3$ | PASS ($<10^{-4}$) |
| A3 | Lorentz isotropy: spread of phase speed over the sphere | $O(k^2)$, exp $=2.000$ | $\to0$ | PASS |
| A4 | Coulomb massless pole $D^{-1}=m^2+v^2k^2$ | $m^2=5.6\times10^{-7}$, $v^2=0.3331$ | $m^2=0$, $v^2=\tfrac13$ | PASS |
| A5 | Thomson cross section $\sigma_T$ from model $\alpha,m_e$ | $0.66525$ b | $0.66525$ b | PASS (rel $3\times10^{-9}$) |
| A6 | Ward identity / charge conservation $C\cdot(C\times B)$ | $1.7\times10^{-16}$ | $0$ | machine, PASS |

**A3 (Lorentz invariance).** The fractional spread of the phase speed $\Omega/\lvert k\rvert$ across 400 directions shrinks as $k^2$ (fitted exponent $2.000$; spread $1.5\times10^{-5}$ at $\lvert k\rvert=0.05$). Rotational — hence Lorentz — invariance is **restored exactly in the continuum limit**; anisotropy is a lattice artifact of order $(ka)^2$. This is the quantitative statement of how the discrete photon approaches the Lorentz-invariant one.

**A4 (Coulomb, not Yukawa).** The static Coulomb operator $\lvert C_\text{odd}(k)\rvert^2$ (F87 Gauss operator) fits $m^2+v^2k^2$ with $m^2\to0$ and $v^2\to\tfrac13=c_\text{lat}^2$. A **massless pole** ($m^2=0$) in 3-D *is* the $1/r$ Coulomb Green's function; a nonzero gap would give a screened Yukawa $e^{-mr}/r$. (Position-space $1/r$ fitting is spoiled by periodic-box/BZ-fold artifacts, so the physically meaningful object — the pole — is tested directly.) $\alpha$ sets the physical prefactor and is an **input**, not a prediction.

**A5 (Thomson).** $r_e=\alpha\hbar/(m_ec)$, $\sigma_T=\tfrac{8\pi}{3}r_e^2$. From the model's two inputs — $\alpha$ and the electron-mass anchor $m_e$ (F120/F121) — the classical (Thomson) scattering cross section reproduces CODATA $\sigma_T=0.66525$ barn to $3\times10^{-9}$. This is a tree-level QED number the inputs return by construction; it certifies the inputs are the physical ones and the low-energy scattering limit is right.

## Tier B — photon-sector precision vs measured bounds

| # | Check | Model | Bound / target | Result |
|---|-------|-------|----------------|:------:|
| B1 | vacuum birefringence (rate split, two polarisations) | $3.3\times10^{-16}$ | $0$ | machine, PASS |
| B2 | photon rest mass (gap at $k=0$) | $0$ | PDG $m_\gamma<10^{-18}$ eV | PASS |
| B3 | dispersion LIV order (body diagonal) | $O(k^3)$, exp $3.000$ | axis-aligned $=0$ | PASS |

**B1.** Two orthogonal linear polarisations of the same $k$ are evolved one tick through `photon_step_spectral`; their realised rotation rates differ by $3.3\times10^{-16}$ (machine zero) — no birefringence, confirmed *dynamically*, not just structurally. For contrast the split a single-branch (chiral) photon **would** carry is $5.8\times10^{-3}$ at $\lvert k\rvert=0.3$ on the body diagonal; that chiral photon is the one excluded by GRB/AGN polarimetry (F65/F66). The paired photon avoids it by construction.

**B3.** Axis-aligned dispersion is **exactly linear** (deviation $1.2\times10^{-15}$, confirming F105); Lorentz-violating dispersion is **anisotropic and $O(k^3)$**, i.e. suppressed by $(ka)^2$. This is consistent with GRB time-of-flight bounds, which F28 places ~15 decades below current sensitivity at the gravity-fixed cell size.

## Tier C — radiative precision (honest reference ledger)

These are the observables that decide whether *quantitative* QED emerges. The model supplies the tree vertex (F87) but has **no interacting loop sector**; F169 explicitly flagged the regularised gapless-Weyl vacuum polarisation / all-$k$ gauge pole as open. Each item below records the exact reference value and the specific machinery that must be built — none is faked as a pass.

| # | Observable | Reference value | Model status — missing machinery |
|---|-----------|-----------------|----------------------------------|
| C1 | electron $a_e=(g-2)/2$ | Schwinger $\alpha/2\pi=1.16141\times10^{-3}$; measured $1.159652\times10^{-3}$ (leading term already within $0.15\%$) | **Not computable.** Needs the one-loop vertex correction (electron emits+reabsorbs a paired photon; amputated 3-point function on the BCC walk). |
| C2 | running $\alpha(q^2)$: $\alpha(0)^{-1}=137.036\to\alpha(M_Z)^{-1}=128.927$ | measured | **Not computable.** Needs the photon self-energy $\Pi(q^2)$ (fermion bubble / vacuum polarisation). QCD running exists (F151/F152); QED vacuum polarisation does not. |
| C3 | Lamb shift $2s_{1/2}-2p_{1/2}=1057.845$ MHz | measured (Lundeen–Pipkin) | **Not computable.** Needs radiative self-energy + vacuum polarisation on the bound electron. In one-body Dirac–Coulomb the two levels are exactly degenerate (F125/I); this is the QFT-4 open item. |

## Verdict

The battery makes the F69-review conclusion quantitative and testable. The paired-spinor photon **quantitatively reproduces the tree/classical and photon-precision QED sector**: masslessness, luminality, the massless Coulomb pole (1/r, not Yukawa), the Thomson cross section from the model's own inputs, exact charge conservation (Ward), zero vacuum birefringence, and $O(k^3)$-suppressed anisotropic LIV consistent with GRB bounds. Lorentz invariance is exact in the continuum limit with $O((ka)^2)$ lattice corrections.

It does **not** yet reach radiative-precision QED — the electron anomalous moment, the running of $\alpha$, and the Lamb shift — because those require an interacting one-loop vertex / self-energy sector that has not been built. The single leading QED benchmark that can be *quoted* (Schwinger $\alpha/2\pi$) already sits within $0.15\%$ of the measured $a_e$, which sets the target the loop sector would have to hit. This is the honest state: **structurally and classically the photon translates to the real world; the loop sector is the remaining, unbuilt bridge to precision QED.**

## Reference values (sources)

CODATA 2022: $\alpha^{-1}=137.035999177(21)$; $a_e=1.15965218046(18)\times10^{-3}$; $\sigma_T=0.66524587$ b; $r_e=2.8179403262$ fm. PDG: $m_\gamma<10^{-18}$ eV. $(\alpha(M_Z^2))^{-1}=128.927(23)$. Lamb shift $2s_{1/2}-2p_{1/2}=1057.845(9)$ MHz (Lundeen–Pipkin 1981). Electron-mass anchor $m_e=0.51099895$ MeV (F120/F121).

## Files

- `tests/findings/test_F249_qed_comparison_battery.py` — the battery (standalone + pytest)
- `test-results/F249_qed_comparison_battery.json` — full numeric output
- `findings/F249-qed-comparison-battery.md` — this finding

---

*End of finding.*
