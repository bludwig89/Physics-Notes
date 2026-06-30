# F179 — The $E_g$ sextic brake $\lambda_6$: the first-principles derivation attempt closes **negative**, so the charged-lepton spectrum is honestly relabelled as a **one-angle consistency fit** — but the fitted object is the *convention-independent* condensate angle $\delta^*$ (not the convention-laden $\lambda_6$), which is Koide-locked to $\delta^*=\tfrac29$ rad ($3\delta^*=Q=\tfrac23$) at $<1\sigma$, and granting that one relation fixes the whole spectrum to $0.01\%$

**Date:** 2026-06-29 - 15:40
**Status:** Resolved-as-relabel (audit C2 addressed; derivation **not** achieved, epistemic status corrected and sharpened) — 5/5 checks PASS. **What this finding does:** it answers the audit-2026-06-29 priority item C2 ("derive the sextic brake $C$ / $\lambda_6$ from the $E_g$ condensate dynamics, **or** honestly relabel the lepton spectrum as a one-parameter fit"). The derivation is attempted along the only open route (the F145 induced-coupling / F150 saturated-condensate solve) and **closes negative**: $\lambda_6$ cannot be reduced to a first-principles number in this work. The honest outcome is therefore the **relabel** — but a sharper one than the audit proposed, on three decisive numerical facts: **(i)** $\lambda_6$ is **not** a clean rational — the two recurring binding-block rationals that bracket the F118 fit, $\tfrac29$ (Fierz, F145) and $\tfrac14$ (rotor, F115), give condensate angles $10.25°$ and $13.40°$, **missing** the data $\delta^*=12.7328°$ by $2.48°$ and $0.67°$ respectively; so the "$\lambda_6\approx\tfrac14$" framing of F118/F119/F120 is misleading and the bare induced rational does **not** deliver the angle. **(ii)** The *convention-independent* invariant $\delta^*=\tfrac29$ rad (equivalently $3\delta^*=Q=\tfrac23$, F150) **is** satisfied — to $<1\sigma$ of the $m_\tau$ experimental error, the **same confidence class as the Koide relation itself** — but it equates a radian-valued angle to a dimensionless ratio, which can only be confirmed by the saturated-condensate solve, so it remains a **target with a rationale, not a derivation**. **(iii)** If the two candidate-exact condensate relations ($Q=\tfrac23$, derived F92; and $\delta^*=\tfrac29$ rad, the target) are *granted*, one mass anchor ($m_\tau$) fixes the **entire** charged-lepton spectrum ($m_\mu/m_\tau$, $m_e/m_\tau$) to $0.01\%$ — quantifying the spectrum as a **one-angle fit**, not a zero-parameter prediction. See §6.
**Module:** (analysis-only; reuses PDG masses + F92/F95/F118/F150 closed forms; no chiral transforms)
**Script:** `tests/findings/test_F179_lambda6_relabel.py` (~1 s, numpy + stdlib, real arithmetic only)
**Results:** `test-results/F179_lambda6_relabel.json`
**Cross-references:** [[F150-eg-sextic-brake-from-architecture]] (the source/kind closure and the sharpened target $\cos3\delta^*=\cos Q$ this finding **tests to $1\sigma$** and converts into an explicit relabel), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $\lambda_6=0.243\approx\tfrac14$ localization this finding **corrects**: $\tfrac14$ misses the angle by $0.67°$), [[F95-B-derived-C-localized]] (the **derived** cubic $B=-3\sqrt2\,I_2\bar y^4$ — the half that *is* a derivation), [[F92-per-constituent-phase-consistency]] ($Q=\tfrac23$ from equipartition — the **other** genuinely derived invariant; and the saturated-pair normalization the open solve needs), [[F96-second-shell-Eg-gap-saturation]] (the massless-electron exact limit $\delta=15°$ — the $\lambda_6$-independent endpoint), [[F120-electron-calibrated-spectrum]] (the "0.1% spectrum" claim this finding relabels; F120 §5 was already partly honest — this finding completes it), [[F119-kg-scale-three-routes]] (the *other* open input $N$; together $(N,\delta^*)$ are the two fitted lepton-sector numbers), [[F145-route-c-induced-njl-coupling]] (the induced-coupling route attempted here for the sextic), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] / [[F144-route-a-alpha-s-dimensional-transmutation]] (the shared IR-coupling residual cluster the open $\lambda_6$ joins).

---

## 1. The audit item and the two admissible outcomes

Audit-2026-06-29, priority fix #2 (Critical, C2):

> **Derive the sextic brake $C$ ($\lambda_6$) from the $E_g$ condensate dynamics, or honestly relabel the lepton spectrum as a one-parameter fit. This is the single most impactful open coefficient.**

The lepton mass texture reduces (F93/F95/F118) to one angular Landau potential
$F(\delta)=B\cos3\delta+C\cos^23\delta$, minimised at $\cos3\delta^*=-B/(2C)$, with $B$ **derived** (F95, closed form $B=-3\sqrt2\,I_2\bar y^4$, $I_2=0.2202$ a lattice constant) and $C=\lambda_6 e^6$ the open coefficient. This finding pursues the derivation and, on its failure, performs the relabel — with the maximum precision the existing closed forms allow.

## 2. The derivation attempt and why it closes negative

**Source and kind are already closed (F150):** two independent no-gos (F95 per-axis scaling/sign + F147 one-tick rigidity) force $C$ to be a **condensate self-interaction**, not a free-sea loop; and F145 fixes its **kind** as an **induced coupling** (integrate out the dual-Meissner binding exchange, Fierz-project onto the symmetry-allowed $E_g$ clock invariant $\mathrm{Re}(\Phi^3)^2=e^6\cos^23\delta$). What remains is the **magnitude** — the flavor-resolved **saturated-condensate pairing solve** that measures the order parameter's induced cubic and sextic self-couplings at the unit-budget amplitude.

**Why it cannot be reduced to a number here.** The induced quartic Fierz coefficient is the clean rational $\tfrac29$ (F145). If the induced *sextic* were the same kind of bare rational, $\lambda_6$ would land on one of the binding-block rationals. It does **not** (D2, §3): the bracket rationals $\tfrac29$ and $\tfrac14$ both **fail** to reproduce the measured angle, by $2.48°$ and $0.67°$. Therefore $\lambda_6=0.243$ carries a **non-rational saturation normalization** — exactly the nonperturbative IR factor that the F124/F144/F145 cluster also carries and that no finding has yet computed (F144 reaches it only as the uncomputed scheme constant $\Lambda\approx1.8$). The induced-coupling route **constrains the character** of $\lambda_6$ ($O(1)$, sourced by the binding block) but **does not deliver its value**. The derivation closes negative.

## 3. D2 — $\lambda_6$ is not a clean rational (the "$\approx\tfrac14$" framing is misleading)

At fixed (derived) $B$ and amplitude, $\cos3\delta^*=-B/(2C)\propto1/\lambda_6$. Calibrating off the F118 data point ($\lambda_6=0.243\leftrightarrow\cos3\delta^*=0.785874$):

| $\lambda_6$ hypothesis | source | $\cos3\delta^*$ | $\delta^*$ | miss vs data |
|---|---|---|---|---|
| $\tfrac29=0.2222$ | Fierz (F145/F49) | $0.85935$ | $10.252°$ | $-2.481°$ |
| $0.243$ (fit) | F118 | $0.78587$ | $12.7328°$ | — (data) |
| $\tfrac14=0.2500$ | rotor $g_s^2\chi$ (F115/F45) | $0.76387$ | $13.398°$ | $+0.665°$ |

Both flanking rationals miss the angle by a physically resolvable amount. The proximity "$\lambda_6\approx\tfrac14$" carried since F118/F119/F120 is an artifact of the convention-laden $e^6$ normalisation: $\tfrac14$ corresponds to $\delta=13.40°$, and (F120-C3) electron-anchored it throws $m_\mu$ off by $+104\%$. **$\lambda_6$ is the wrong object to call "nearly derived."**

## 4. D3 — the convention-independent target *is* satisfied, at Koide confidence

The correct invariant is the ratio $\cos3\delta^*=-B/(2C)$, i.e. the angle $\delta^*$ itself. From the PDG $Z_3$ decomposition (real arithmetic, assignment-independent $\cos3\delta$):

$$A/\bar y=1.414201\ (\sqrt2),\quad Q=0.666661\ (\tfrac23),\quad
\cos3\delta^*=0.785874,\quad \delta^*=12.7328°,\quad 3\delta^*=0.666689\ \text{rad}.$$

The F150 sharpened target $3\delta^*=Q=\tfrac23$ rad (i.e. $\delta^*=\tfrac29$ rad):

$$|3\delta^*-Q|=2.8\times10^{-5},\qquad
\cos3\delta^*-\cos\tfrac23=-1.4\times10^{-5}.$$

**Crucially, this is within experimental error.** Propagating the PDG $m_\tau$ uncertainty ($\pm0.12$ MeV) gives $\sigma(\cos3\delta^*)=1.55\times10^{-5}$, so the deviation from $\cos\tfrac23$ is $-0.89\sigma$ — the relation $3\delta^*=Q$ is **satisfied to $<1\sigma$, the same confidence class as the Koide relation itself** (which is $\sim0.9\sigma$, $m_\tau$-limited). It is a genuine, currently-satisfied, falsifiable relation between two *independent* invariants of the one condensate ($Q$ fixes the magnitude ratio $A/\bar y$ and is $\delta$-blind; $\delta^*$ is the orthogonal phase DOF).

**But it is not a derivation.** $3\delta^*$ is an angle in radians; $Q$ is a dimensionless mass ratio. Equating them is precisely the kind of identity that only the saturated-condensate solve can confirm or refute — F150 §5 flagged this and this finding confirms the flag holds. The honest status of $\delta^*=\tfrac29$ rad is **target with a rationale**.

## 5. The other genuinely derived endpoint ($\delta=15°$) bounds the claim

F96's exact massless-electron texture algebra forces $Q=\tfrac23\iff\delta=15°$ ($\cos3\delta=1/\sqrt2$) — a real derivation, but only in the $m_e\to0$ limit. The physical $\delta^*=12.7328°$ is the $m_e>0$ displacement of that endpoint. So the angle is **bracketed by two derived statements** ($\delta=15°$ at $m_e=0$; $\delta\to$ the brake value as $m_e$ turns on) but its exact physical value is the brake, i.e. the open $\lambda_6$.

## 6. D4 — the prediction content, made quantitative (the relabel)

Grant the two candidate-exact condensate relations and nothing else about the leptons:

- $A/\bar y=\sqrt2$ ($\Rightarrow Q=\tfrac23$) — **derived** (F92, equipartition);
- $\delta^*=\tfrac29$ rad ($\Rightarrow3\delta^*=Q$) — the **target** (F150, $<1\sigma$);
- one mass anchor $m_\tau$ — the open scale $N$ (F119).

Then $y_a=\bar y+A\cos(\delta^*+2\pi a/3)$, $m_a=y_a^2$ predicts the whole spectrum:

| ratio | predicted | PDG | error |
|---|---|---|---|
| $m_\mu/m_\tau$ | $5.94599\times10^{-2}$ | $5.94635\times10^{-2}$ | $-0.01\%$ |
| $m_e/m_\tau$ | $2.87565\times10^{-4}$ | $2.87585\times10^{-4}$ | $-0.01\%$ |

So the lepton spectrum is, stated honestly:

> **a one-angle consistency fit.** Two of its structural inputs are genuinely **derived** — the generation count $3$ (F75) and the Koide magnitude $Q=\tfrac23$ (F92, equipartition). One is a **calibration** — the overall scale $N$ (F119). One is a **fit with a Koide-locked target value** — the condensate angle $\delta^*$, equal to $\tfrac29$ rad to $<1\sigma$ but **not derived**. Granting the target value, one anchor reproduces the spectrum to $0.01\%$. **This is not a zero-parameter prediction** — it is a $0.01\%$-accurate fit of two mass ratios to **one** Koide-locked angle plus one scale.

## 7. What this settles, and the residual (unchanged in kind)

**Settled (corrections to the record):** (i) the derivation of $\lambda_6$ is **not** achieved — audit C2's first option is closed negative; (ii) the "$\lambda_6\approx\tfrac14$" framing is **misleading** and is replaced by the convention-independent angle $\delta^*$; (iii) the honest label of the lepton spectrum is **one-angle fit**, quantified at $0.01\%$ (D4), with the derived/calibrated/fitted inputs itemised (D5). **Unchanged residual:** the single shared nonperturbative IR-coupling normalization at the saturation/confinement scale (F124/F144/F145/F150 cluster) — whichever computation delivers it ($\sqrt\sigma/f_\pi$, the $\Lambda$ scheme constant, $G/G_c$, **or** $\lambda_6$) delivers all four. The deepest open lepton-sector statement is therefore sharp and singular: **is $\delta^*=\tfrac29$ rad exact?** — answerable only by the saturated-condensate induced-coupling solve (F92 §6 / F95 §7 / F118 §7 / F150 §7), which this finding does not perform.

## 8. Check summary (`test_F179_lambda6_relabel.py`, 2026-06-29 - 15:38)

| Check | Statement | Tier | Result |
|---|---|---|---|
| D1 | condensate invariants: $A/\bar y=\sqrt2$, $Q=\tfrac23$, $\cos3\delta^*=0.785874$, $\delta^*=12.7328°$ | data | PASS |
| D2 | $\lambda_6$ not rational: $\tfrac29\to10.25°$, $\tfrac14\to13.40°$ both miss $12.7328°$ | structural | PASS |
| D3 | target $3\delta^*=Q=\tfrac23$ rad satisfied to $-0.89\sigma$ ($m_\tau$ error) | target | PASS |
| D4 | granting $(Q,\delta^*)$ + 1 anchor $\Rightarrow$ spectrum to $0.01\%$ | prediction-content | PASS |
| D5 | verdict: derivation negative $\Rightarrow$ relabel; inputs itemised | bookkeeping | PASS |

**Overall 5/5 PASS** (~1 s).

## 9. Provenance

- **New content:** the explicit negative close of the $\lambda_6$ derivation; the demonstration (D2) that neither bracket rational reproduces the angle (correcting the "$\approx\tfrac14$" framing); the $1\sigma$ experimental-error test of the $3\delta^*=Q$ target (D3); the quantified one-angle prediction content $0.01\%$ (D4); and the itemised relabel of the lepton spectrum (D5).
- **Reused:** F95 derived $B$; F92 $Q=\tfrac23$ equipartition and the saturated-pair normalization; F118 $\lambda_6$/$W$ localization; F150 source/kind closure and the $\cos3\delta^*=\cos Q$ target; F96 massless-electron $\delta=15°$ endpoint; F120 anchoring sensitivity; PDG masses ($m_e=0.51099895$, $m_\mu=105.6583755$, $m_\tau=1776.86\pm0.12$ MeV).
- **Verification:** `tests/findings/test_F179_lambda6_relabel.py` (2026-06-29 - 15:38, 5/5 PASS), results `test-results/F179_lambda6_relabel.json`. Real arithmetic only — no chiral transforms, numpy-safe.
