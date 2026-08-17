# F121 — The τ adopted as the canonical mass-scale anchor: wall-pinned ⇒ exactly δ-stable, so it contributes zero anchor error and gives the standard lepton/kg readout (m_μ to −0.00 %, m_e to −0.06 %)

**Date:** 2026-06-09 - 17:05
**Status:** Confirmed — 5/5 checks PASS (`test_F121_tau_anchored_canonical_spectrum.py`, <1 s). Pure math (no scipy, per CLAUDE.md). Adopts the τ as the standard mass-scale anchor in place of the electron, per the F120 robustness lesson.
**Script:** `tests/findings/test_F121_tau_anchored_canonical_spectrum.py`
**Results:** `test-results/F121_tau_anchored_canonical_spectrum.json`
**Cross-references:** [[F120-electron-calibrated-spectrum]] (the electron-anchor instability this fixes), [[F119-kg-scale-three-routes]] (the single open scale $N$ and the angle $\lambda_6$), [[F101b-one-heavy-branch-fit-W]] (the wall-pinning $y_\tau=1$), [[F78-koide-amplitude-from-cooper-pair]] (Koide, $m=y^2$).

---

## 1. Why the τ is the right anchor

The lepton shape is the $E_g$ condensate at angle $\delta$ with equipartition $A=\sqrt2\bar y$, masses $m_a=y_a^2$, heaviest wall-pinned: $m_\tau^\text{cond}=1$ for **all** $\delta$. So anchoring the single scale on the τ gives $N_\tau=m_\tau^\text{measured}$ with **exactly zero** angle sensitivity ($|\partial\ln m_\tau/\partial\delta|<10^{-6}$, T2) — the anchor adds no error and every prediction's residual is purely the angle's. The electron, by contrast, sits at the condensate node ($\sim10\times$ more δ-sensitive, F120). The τ is therefore the robust canonical anchor.

## 2. The canonical τ-anchored readout (measured angle δ = 12.733°)

| lepton | predicted (MeV) | predicted (kg) | PDG (MeV) | error |
|---|---|---|---|---|
| $e$ | 0.51069 | $9.1038\times10^{-31}$ | 0.510999 | **−0.06 %** |
| $\mu$ | 105.6575 | $1.8835\times10^{-28}$ | 105.6584 | **−0.00 %** |
| $\tau$ | 1776.86 *(anchor)* | $3.1675\times10^{-27}$ | 1776.86 | — |

Both lighter leptons are reproduced from $m_\tau$ plus the shape to ≤0.06 %. Koide $Q=2/3$ holds geometrically (T4: condensate $0.666667$, data $0.666661$).

## 3. Robustness vs the electron anchor (model angle, λ₆ = ¼ → δ = 13.36°)

| anchor | predicts $m_\mu$ | error |
|---|---|---|
| **τ** (wall, δ-stable) | 111.5 MeV | **+5.5 %** |
| $e$ (node) | 215.5 MeV | +104 % |

With the model's own first-principles angle, the τ anchor holds $m_\mu$ to ~5 % (the bare $\lambda_6$ error), while electron-anchoring blows up to +104 %. The τ-anchored band is set by the one open angle, not amplified by the anchor.

## 4. Full fermion table in kg (canonical, τ-anchored)

Leptons predicted by the shape (≤0.06 % at the measured angle); quark masses are the measured values converted to kg — a **consistency** readout, since the model fits the quark texture rather than predicting it:

| fermion | mass (kg) | tier |
|---|---|---|
| electron | $9.1038\times10^{-31}$ | predicted |
| muon | $1.8835\times10^{-28}$ | predicted |
| tau | $3.1675\times10^{-27}$ | anchor |
| up | $3.85\times10^{-30}$ | consistency |
| down | $8.33\times10^{-30}$ | consistency |
| strange | $1.67\times10^{-28}$ | consistency |
| charm | $2.26\times10^{-27}$ | consistency |
| bottom | $7.45\times10^{-27}$ | consistency |
| top | $3.08\times10^{-25}$ | consistency |

## 5. Status of inputs

Unchanged from F119: the irreducible open inputs are exactly **two** — the overall scale $N$ (here $=m_\tau$, the anchor) and the angle $\lambda_6$ (whose exact value is the F118/F119 residual). Everything else (the ratios, Koide $Q=2/3$, the kg conversion) is the derived shape plus the locked cell. **The τ-anchored readout above is adopted as the standard mass-sector output going forward.**

## 6. Test summary (`test_F121_tau_anchored_canonical_spectrum.py`, 2026-06-09 - 17:05)

| Check | Statement | Result | Status |
|---|---|---|---|
| T1 | canonical τ-anchored spectrum (measured angle) | $m_\mu$ −0.00 %, $m_e$ −0.06 % | PASS |
| T2 | τ exactly δ-stable; robust vs electron | $5.5\%$ vs $104\%$ (model angle) | PASS |
| T3 | full fermion kg table | leptons ≤0.06 % | PASS |
| T4 | Koide $Q=2/3$ | $0.666667$ | PASS |
| V | verdict / adoption | — | PASS |

**Overall 5/5 PASS** (<1 s).

## 7. Provenance

- New content: adoption of the τ as the canonical anchor; the δ-stability proof for the wall-pinned τ vs the node-sitting electron; the canonical τ-anchored lepton spectrum and full fermion kg table.
- Machinery: the F101 condensate shape; PDG 2024 masses; CODATA 2018 constants and the F79/F107 locked cell.
- Verification: `tests/findings/test_F121_tau_anchored_canonical_spectrum.py` (2026-06-09 - 17:05, 5/5 PASS), results `test-results/F121_tau_anchored_canonical_spectrum.json`.
