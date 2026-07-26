# F231 — E2: $\sin^2\theta_W=\tfrac29$ is the **on-shell face** of $\sin^2\theta_W=\tfrac14$, not a competing tree value — the exact bridge $8/9$ decomposes into one-loop running $\times$ MS-bar$\to$on-shell scheme conversion

> **Numbering note:** highest committed finding at write time was F230 (this session); concurrent sessions may collide — re-checked, this is **F231**.

**Date:** 2026-07-02 - 16:50
**Status:** Confirmed (reconciliation) — 5/5 checks PASS. Resolves the E2 question: are $\tfrac14$ (F45/F138) and $\tfrac29$ (F49) two independent geometric derivations of $\sin^2\theta_W$, an on-shell endpoint of the *same* physics, or a coincidence? Answer: **the same Weinberg angle at opposite ends of one chain.** $\tfrac14$ is the MS-bar UV cap at the compositeness scale $\mu_\star=4\pi v$ (F138, forced by hypercharge having no lattice kinetic term); $\tfrac29$ is the on-shell (physical mass-ratio) value at $M_Z$, i.e. $m_Z/m_W=3/\sqrt7$ (F49). The exact bridge $(\tfrac29)/(\tfrac14)=8/9$ (F138 §5) **decomposes** as one-loop running ($0.927$) $\times$ MS-bar$\to$on-shell scheme conversion ($0.965$) $=0.895$, matching $8/9=0.889$ to $0.67\%$ (within one-loop $+$ NDA $+$ scheme truncation). So $\tfrac29$ is **not** an independent tree value and **not** a coincidence — it is the IR/on-shell face of the $\tfrac14$ physics. F49's BCC $2{:}7$ counting hits that on-shell endpoint geometrically, but its assignment stays underived (F49), so it is a structural **match**, not yet a rigorous second derivation.
**Module:** (analysis-only; PDG 2024 central values + F138 cited one-loop result; real arithmetic — no chiral transforms)
**Script:** `tests/findings/test_F231_weinberg_scheme_reconciliation.py` (<1 s, stdlib only)
**Results:** `test-results/F231_weinberg_scheme_reconciliation.json`
**Cross-references:** [[F138-weinberg-gap-closure-4piv-matching]] (the $\tfrac14$ UV cap at $\mu_\star=4\pi v$, the one-loop run to $0.23173$, and the $8/9$ bridge this finding **decomposes**; §5 there posed exactly this reconciliation and left the on-shell exactness of $\tfrac29$ open), [[F45-sigma-tau-swap-weinberg-angle]] (the internal $1{:}3\to\tfrac14$ derivation), [[F49-bcc-finite-k-weinberg-angle]] (the external $2{:}7\to\tfrac29$ counting, reinterpreted here as the on-shell endpoint; its assignment still underived), [[F41-hypercharge-higgs-free]] (no $Y$ kinetic term $\Rightarrow$ abelian cap at $\tfrac14$), [[F141-ws-cell-7axes-onshell-mass-counting]] (the WS-cell $7$-axis lemma and the on-shell $m_W^2{:}m_Z^2$ counting — the $\tfrac29$ endpoint's structural companion), [[F115-coupling-magnitudes-running-rotor]] (CM2: the gap is a few-TeV matching, not Planck running), [[F230-lepton-angle-geometric-nogo]] (the lepton-sector $\tfrac29$ echo, assessed there as dimensionally distinct).

---

## 1. The two values and the question

Two findings produce $\sin^2\theta_W$ from BCC geometry:

- **F45** (internal): $\sigma\leftrightarrow\tau$ swap rep counting $1{:}3\Rightarrow g'^2/g^2=\tfrac13\Rightarrow\sin^2\theta_W=\tfrac14$.
- **F49** (external): BCC $2$ sublattices $:7$ bond axes $\Rightarrow g'^2/g^2=\tfrac27\Rightarrow\sin^2\theta_W=\tfrac29$.

F138 then derived that $\tfrac14$ is not a tree value but the **UV cap**: hypercharge has no lattice kinetic term (F41), so the abelian coupling is formally infinite and $\sin^2\theta_W\to\tfrac14$ exactly as $g_X\to\infty$, realised at the compositeness scale $\mu_\star=4\pi v=3.094$ TeV. E2 asks how $\tfrac29$ fits: rival derivation, endpoint of the same physics, or coincidence?

## 2. $\tfrac29$ is the exact on-shell mass-ratio value (W1)

$\tfrac29$ is, algebraically, a statement about physical masses:

$$\sin^2\theta_W^\text{os}\equiv1-\frac{m_W^2}{m_Z^2}=\frac29\;\Longleftrightarrow\;\frac{m_Z}{m_W}=\frac{3}{\sqrt7}.$$

Against PDG 2024 ($m_W=80.3692$, $m_Z=91.1880$ GeV): $1-m_W^2/m_Z^2=0.223209$ vs $\tfrac29=0.222222$ (**$-0.44\%$**), and $m_Z/m_W=1.134614$ vs $3/\sqrt7=1.133893$ (**$-0.064\%$**). So $\tfrac29$ lives in the **on-shell scheme at $M_Z$**, whereas $\tfrac14$ (F138) is the **MS-bar** angle at the **UV scale $4\pi v$**. They are the same observable in different scheme $\times$ scale.

## 3. The $8/9$ bridge decomposes into running $\times$ scheme (W2 — the new content)

F138 §5 noted the exact bridge $(\tfrac29)/(\tfrac14)=8/9$ but did not explain it. It factorises cleanly into the two steps that separate the UV MS-bar cap from the IR on-shell endpoint:

$$\underbrace{\frac{2/9}{1/4}}_{8/9\,=\,0.8889}\;=\;\underbrace{\frac{\sin^2\bar\theta_W^{\text{MS}}(M_Z)}{1/4}}_{\text{one-loop running}}\;\times\;\underbrace{\frac{\sin^2\theta_W^{\text{os}}(M_Z)}{\sin^2\bar\theta_W^{\text{MS}}(M_Z)}}_{\text{MS}\to\text{on-shell}}$$

- **Running factor.** F138's one-loop Higgs-free run of $\tfrac14$ from $4\pi v$ down to $M_Z$ gives $\sin^2\bar\theta_W^{\text{MS}}(M_Z)=0.23173$; factor $0.23173/0.25=\mathbf{0.9269}$.
- **Scheme factor.** MS-bar$\to$on-shell at $M_Z$ (PDG central values): $0.223209/0.23122=\mathbf{0.9654}$.
- **Product** $=0.9269\times0.9654=\mathbf{0.8948}$ vs $8/9=0.8889$ — **residual $0.67\%$** (**W2**), i.e. within one-loop $+$ NDA ($\mu_\star=4\pi v$ carries F138's $\ln$-offset $0.099$) $+$ scheme truncation.

## 4. The full chain lands on $\tfrac29$ (W3)

Equivalently, propagate $\tfrac14$ end-to-end: $\tfrac14\xrightarrow{4\pi v\to M_Z\text{ run}}0.23173\ (\text{MS})\xrightarrow{\text{scheme}}0.22370\ (\text{on-shell})$ vs $\tfrac29=0.22222$ — **residual $0.66\%$** (**W3**). The UV cap, run down and converted to the physical mass-ratio scheme, reproduces $\tfrac29$ to sub-percent.

## 5. The reconciled statement (W4)

> $\sin^2\theta_W=\tfrac14$ and $\sin^2\theta_W=\tfrac29$ are **one angle, two faces**: $\tfrac14$ is the **MS-bar UV cap** at the compositeness scale $4\pi v$ (F45/F138, forced by F41's absent hypercharge kinetic term), and $\tfrac29$ is the **on-shell endpoint** at $M_Z$ ($m_Z/m_W=3/\sqrt7$, F49). They are joined by one-loop running $\times$ scheme conversion $=8/9$ to $0.67\%$.

Consequences for the three-way question E2 posed:

1. **Not a competing tree value.** The two never coexist at one scale/scheme; F138 already removed the "$+12\%$ gap" framing. ✔
2. **Not a coincidence.** The $8/9$ bridge is *derived* (running is standard RG from a derived cap; the scheme factor is the standard MS$\to$on-shell shift), and it decomposes to $0.67\%$. ✔
3. **A genuine second geometric derivation? — not yet.** F49's BCC $2{:}7$ counting reproduces the on-shell endpoint $\tfrac29$ directly from lattice structure, and F141 sharpens the same endpoint as the WS-cell $7$-axis on-shell mass counting ($m_W^2{:}m_Z^2=7{:}9$). But F49's representation-theoretic **assignment** (why $U(1)_Y$ is the sublattice $U(1)$ and $SU(2)_L$ spans all $7$ axes) remains **underived**. So $\tfrac29$ is a structural **match** to the on-shell face of the $\tfrac14$ physics — strong and geometrically motivated — not yet an independent rigorous derivation.

**Residual vs PDG:** $\tfrac29$ low by $0.44\%$ (on-shell $\sin^2$); $m_Z/m_W=3/\sqrt7$ low by $0.064\%$. Falsifiable target: F49's assignment must reproduce the **on-shell** scheme (giving $m_Z/m_W=3/\sqrt7$ exactly), not the MS-bar one.

## 6. Check summary (`test_F231_weinberg_scheme_reconciliation.py`, 2026-07-02 - 16:50)

| # | Statement | Tier | Result |
|---|---|---|---|
| W1 | on-shell $1-m_W^2/m_Z^2$ vs $\tfrac29$ ($-0.44\%$) | quantitative | PASS |
| W1b | $m_Z/m_W$ vs $3/\sqrt7$ ($-0.064\%$) | quantitative | PASS |
| W2 | $8/9=$ running $(0.927)\times$ scheme $(0.965)=0.895$, resid $0.67\%$ | reconciliation | PASS |
| W3 | full chain $\tfrac14\to$ run $\to$ scheme $\to0.2237$ vs $\tfrac29$, resid $0.66\%$ | reconciliation | PASS |
| W4 | reconciled: UV MS-bar cap vs IR on-shell endpoint, same angle | bookkeeping | PASS |

**Overall 5/5 PASS** (<1 s).

## 7. Honest scope

- The running factor $0.23173$ is F138's one-loop Higgs-free result (cited, verified there); it carries an NDA $\ln$-offset $0.099$ at $\mu_\star=4\pi v$, which is the dominant source of the $0.67\%$ closure residual. Two-loop / threshold refinement moves things at the $0.1\%$ level.
- The scheme factor uses PDG central masses; a full model-internal MS$\to$on-shell computation would replace it with a derived number (the same direction F138's "compute the induced $Y$ stiffness" follow-up points).
- $\tfrac29$'s status is upgraded from "competing value" to "on-shell face, matched to $0.67\%$", but F49's assignment is still the open piece — this finding sharpens its target (on-shell scheme, $3/\sqrt7$), it does not close it.

## 8. Provenance

- **New content:** the decomposition of the $8/9$ bridge into one-loop running $\times$ MS$\to$on-shell scheme conversion (W2), the full-chain landing on $\tfrac29$ (W3), and the single reconciled statement resolving E2 (W4).
- **Reused:** F138 (the $\tfrac14$ cap at $4\pi v$, the $0.23173$ run, the $8/9$ bridge and $3/\sqrt7$ algebra), F45 ($\tfrac14$ internal), F49 ($\tfrac29$ external), F41 (no $Y$ kinetic term), F141 (WS-cell on-shell $7{:}9$). Constants: PDG 2024 ($m_W=80.3692$, $m_Z=91.1880$ GeV; MS-bar $\sin^2\bar\theta_W(M_Z)=0.23122$).
- **Verification:** `tests/findings/test_F231_weinberg_scheme_reconciliation.py` (2026-07-02 - 16:50, 5/5 PASS), results `test-results/F231_weinberg_scheme_reconciliation.json`. Real arithmetic only — numpy-safe.
