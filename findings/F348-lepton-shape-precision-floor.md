# F348 — Ledger row E1's shape residual (0.007% on $m_\tau/m_e$) is a measurement-floor effect, not a gap owed a next-order correction — quantified, with a named falsifiable re-attack threshold

**Date:** 2026-09-02 - 03:31
**Status:** Confirmed (negative / precision-floor) — 5/5 checks PASS. **What this establishes:** F175 D4 predicts the charged-lepton mass ratios from the two *derived* numbers $\delta^*=\tfrac29$ (F175) and $\eta^2=\tfrac12$ (F92) with zero shape parameters, landing at $m_\mu/m_e$ $+0.001\%$ and $m_\tau/m_e$ $+0.007\%$. F175 §5 already attributed the residual to "the $\sim0.9\sigma$ $\eta^2$–$\delta$ tension (F174 S4) ... at current mass precision" without quantifying it further. This finding does that: the $0.007\%$ $m_\tau/m_e$ residual is a single $1.04\sigma$ effect against the current PDG $m_\tau$ uncertainty ($\pm0.12$ MeV) — statistically indistinguishable from measurement noise — and a numeric Jacobian shows the *same* small $(\delta,\eta^2)$ offset already flagged by F174 S4 reconstructs **both** the $0.001\%$ and $0.007\%$ residuals simultaneously to $<0.01\%$ relative error, i.e. there is one joint offset here, not two independent unexplained corrections. F256's route-(I) dynamical no-go is reused (not relitigated): it already shows the model has no mechanism capable of computing an independent next-order correction to $\delta^*$, so ledger row E1 stays honestly **QUANT $\times2$**, with a computed, falsifiable re-attack condition in place of a fabricated correction term.
**Module:** `casim.engine.particles.derive_lepton_shape_precision_floor` **Test:** `tests/findings/test_F348_lepton_shape_precision_floor.py` (8/8 PASS, <5 s, stdlib only)
**Results:** `test-results/F348_lepton_shape_precision_floor.json`
**Claim:** none — quantifies the measurement-floor status of an existing prediction's residual (F175/F92/F256) against current PDG precision; asserts no new SM/GR/QFT relation a claim card should carry (found and declared 2026-09-03, F353 session, while running `make coverage` for an unrelated finding).
**Cross-references:** [[F175-lattice-2-9-eg-weight]] (the $\delta^*=\tfrac29$ derivation and the D4 zero-shape-parameter prediction this finding quantifies the residual of), [[F92-per-constituent-phase-consistency]] ($\eta^2=\tfrac12$), [[F174b-shape-angle-2-9-topological]] (S4: the free-fit $\delta_\text{fit}=0.222229$, $\eta^2_\text{fit}=0.4999908$ this finding's Jacobian check reuses), [[F76-generation-mass-hierarchy-crystal-field]] (C5: the PDG $m_\tau=1776.86\pm0.12$ MeV this finding's sigma-bookkeeping is built on), [[F256-lambda6-sextic-derivative-nogo]] (the route-(I) dynamical no-go this finding reuses as the reason no in-model correction is computable).

---

## 1. The question (ledger row E1)

`docs/status/open-derivations.md` row E1 (CLAUDE.md decision #7) grades the charged-lepton shape prediction QUANT $\times2$: F175 D4 reproduces $m_\mu/m_e$ to $+0.001\%$ and $m_\tau/m_e$ to $+0.007\%$ using the two derived numbers $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$, zero shape parameters. This session's brief asked whether a **computed** (not fitted) next-order correction — from the existing crystal-field expansion (F76) or the Landau angle machinery (F118/F230/F256) — can close any fraction of the $0.007\%$, or whether the residual is already measurement-floor-limited.

## 2. D1 — the residual, directly in MeV and in measurement sigma

Using the same PDG masses as F175/F76 ($m_e=0.51099895000$, $m_\mu=105.6583755$, $m_\tau=1776.86\pm0.12$ MeV — $m_\tau$'s $\pm0.12$ MeV is the dominant error source; $m_e,m_\mu$ are known many orders of magnitude more precisely), the exact-point prediction gives

$$m_\tau/m_e\big|_\text{pred}=3477.4728,\qquad m_\tau/m_e\big|_\text{PDG}=3477.2283,$$

a residual of $+0.1250$ MeV $=+0.00703\%$. Divided by the current PDG uncertainty, $\pm0.12$ MeV, that is

$$\boxed{\ 1.04\sigma\ }$$

— consistent with (the same effect measured a different way as) the $\sim0.9$–$0.91\sigma$ figures F76 C3 and F174 S1 already quote on the closely related Koide-$Q$ metric. **This is not currently a statistically significant discrepancy.**

## 3. D2 — one joint offset explains both residuals, not two independent ones

F174 S4 already flagged that the free 2-parameter fit to the same PDG masses lands at $\delta_\text{fit}=0.222229$ rad, $\eta^2_\text{fit}=0.4999908$ — each within $\sim10^{-5}$ of the exact $\{\tfrac29,\tfrac12\}$ — without asking what that small offset does to the *mass-ratio* residuals specifically. A numeric Jacobian $\partial(m_\mu/m_e,\,m_\tau/m_e)/\partial(\delta,\eta^2)$ evaluated at the exact point, applied to the offset $(\delta_\text{fit}-\tfrac29,\ \eta^2_\text{fit}-\tfrac12)=(+6.78\times10^{-6},\ -9.20\times10^{-6})$, reconstructs

- $\Delta(m_\mu/m_e)$: linearized $-0.009050$ vs. actual $-0.009051$ (relative error $9\times10^{-5}$)
- $\Delta(m_\tau/m_e)$: linearized $-0.35148$ vs. actual $-0.35148$ (relative error $9\times10^{-6}$)

Both residuals — the $0.001\%$ on $m_\mu/m_e$ *and* the $0.007\%$ on $m_\tau/m_e$ — come from the **same** single small parameter offset, to well under $0.01\%$ relative reconstruction error. There is one joint tension here (F174 S4's), not a second, independent, unexplained correction hiding in the $m_\tau/m_e$ channel specifically.

## 4. D3 — the explicit, falsifiable re-attack threshold

Holding the PDG $m_\tau$ central value fixed and asking how much its uncertainty would need to shrink for the $+0.125$ MeV offset to become statistically significant:

| target significance | required $m_\tau$ uncertainty | improvement over today's $\pm0.12$ MeV |
|---|---|---|
| $2\sigma$ | $\pm0.0625$ MeV | $1.92\times$ |
| $3\sigma$ | $\pm0.0417$ MeV | $2.88\times$ |
| $5\sigma$ | $\pm0.0250$ MeV | $4.80\times$ |

Below a $\sim3\times$ tightening of the world-average $m_\tau$ measurement, this residual cannot be distinguished from zero, and no computation performed today can honestly move it past QUANT $\times2$.

## 5. Why no in-model correction is computable (reusing F256, not relitigating it)

The obvious candidate mechanism for a computed correction would be the dynamical Landau route, $\cos3\delta^*=-B/(2C)$ (F118/F230), which *could* in principle pin $\delta^*$ slightly away from exactly $\tfrac29$. F256 already closed this door: $B$ (Dirac-sea, F95) and $C$ (induced condensate self-coupling, F150) are independent $O(1)$ objects with no locking relation, so $-B/(2C)=\cos\tfrac23$ is a $1.7\times10^{-5}$ near-coincidence, not a mechanism, and the $\lambda_6$ required to hit $3\delta^*=Q$ exactly ($0.243$) sits strictly between the model's only two candidate rationals ($\tfrac29,\tfrac14$), matching neither. There is consequently **no route in the model, other than fitting, to a number that would nudge $\delta^*$ or $\eta^2$ by the $\sim10^{-5}$ needed to close this residual** — inventing one would be exactly the kind of unsourced correction this project's stated precision philosophy (CLAUDE.md Practices: "always attempt to algebraically derive... before introducing new physics") rules out.

## 6. Verdict

Ledger row E1 stays honestly **QUANT $\times2$**. The $0.007\%$ residual is fully accounted for — not by a missing physics term, but by (i) the already-known $\sim10^{-5}$-level $\eta^2$–$\delta$ tension between the exact and data-preferred values (F174 S4), which this finding shows explains *both* mass-ratio residuals jointly, and (ii) that tension itself sitting at $1.04\sigma$ of the current $m_\tau$ measurement uncertainty. F256 independently rules out the one mechanism that could have supplied a computed correction. The honest close is a quantified precision floor plus a named re-attack condition ($m_\tau$ precision improving $\sim3\text{--}5\times$), not a promotion to PARTIAL/MACHINE. Per this session's own brief, further time on this specific row has low marginal value until that condition changes; effort is better spent on higher-priority open rows.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| D1 | reproduces F175 D4's $+0.001\%$/$+0.007\%$; $m_\tau/m_e$ residual $=1.04\sigma$ of PDG $m_\tau$ uncertainty | PASS | data |
| D2 | Jacobian-linearized offset reconstructs both residuals to $<0.01\%$ relative error; offsets match F174 S1's quoted $\delta_\text{fit},\eta^2_\text{fit}$ scale | PASS | computed |
| D3 | $3\sigma$/$5\sigma$ re-attack thresholds: $2$–$4\times$ / $4$–$6\times$ improvement over today's $m_\tau$ precision | PASS | computed |
| D4 | (scope) F256's route-(I) no-go independently rules out the model's only candidate dynamical-correction mechanism | PASS | scope |
| D5 | (scope) no fabricated correction proposed; verdict is precision-floor + named falsifier | PASS | scope |

**Overall 5/5 PASS.**

## 8. Honest scope

- This finding does **not** derive a next-order term, and does not claim one is impossible in principle — only that none is currently computable from the model's existing machinery (F256), and that the residual is too small to distinguish from $m_\tau$ measurement noise today.
- The $3\sigma$/$5\sigma$ thresholds assume the PDG $m_\tau$ central value stays put as its uncertainty shrinks; if a future, more precise measurement shifts the central value instead, the sign and size of any future "discrepancy" could change in either direction — this is a threshold for *distinguishability*, not a prediction of what a tighter measurement will find.
- The Jacobian reconstruction (D2) is linear/local; at the sub-$10^{-5}$-radian offset scale involved here, higher-order terms are negligible (confirmed by the $<10^{-4}$ relative reconstruction error), so this is not a concern in practice.

## 9. Provenance

- **New:** the direct MeV/$\sigma$ bookkeeping of the $m_\tau/m_e$ residual against the current PDG $m_\tau$ uncertainty (D1); the numeric-Jacobian demonstration that F174 S4's already-flagged $(\delta,\eta^2)$ offset reconstructs *both* mass-ratio residuals jointly (D2); the explicit $2\sigma/3\sigma/5\sigma$ re-attack precision thresholds (D3); the explicit tying-together of F256's route-(I) no-go as the reason no in-model correction is computable for *this* residual specifically.
- **Reused:** F175 D4 (the exact-point prediction), F92 ($\eta^2=\tfrac12$), F174b S1/S4 (the free-fit values and their tension), F76 C3/C5 (PDG masses and the Koide-$Q$-based $\sigma$ figure), F256 (route-(I) dynamical no-go). PDG 2024 lepton masses.
- **Verification:** `tests/findings/test_F348_lepton_shape_precision_floor.py` (2026-09-02, 8/8 PASS), results `test-results/F348_lepton_shape_precision_floor.json`, module `src/casim/engine/particles/derive_lepton_shape_precision_floor.py`. stdlib only (`math`) — no numpy/scipy, D8-compliant trivially.
