# F235 — $\sqrt\sigma/f_\pi$ scale-setting: the exact chiral factor $7.04$ stands, the $+12\%$ confinement-factor residual is **not** removable by any principled BCC Brillouin-zone cutoff, and it is the **same** strong-sector one-loop constant $d_1$ that E3 ($N$) and Q2 ($\alpha_s$ scheme) reduce to — so Q1, Q2 and E3 are one open number, not three

**Date:** 2026-07-02 - 23:55
**Numbering:** F229–F232 taken by a concurrent session; this session adds F233 (E3), F234 (E4), and this **F235** (Q1) (re-checked after collision).
**Status:** Partial + honest negative — 4/4 checks PASS (`test_F235_sqrt_sigma_fpi_scale_setting.py`, <1 s, stdlib). **This executes open-derivations prompt Q1 (#8).** The prompt asks to push $\sqrt\sigma/f_\pi$ (F124: $4.00$ axis vs empirical $4.56$, $+12\%$) below $5\%$ by deriving the scale-setting factor from strong-coupling running (F144 $\alpha_s$ + F86 $\sigma$), *or* to document the missing factor. Result: **the residual does not close to $<5\%$ from a cutoff-convention choice** — the value $\Lambda_\text{eff}=2.758/a$ needed to hit $4.56$ lies *below* even the per-axis BZ edge $\pi/a=3.14$ and far below every equal-volume BCC Debye radius, so no principled Brillouin-zone cutoff reaches it. The residual is a genuine **scale-setting** object, and F124 §5 / F144-A4 already identify it as *the same* one-loop matching constant $d_1$ (equiv. $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$) that E3 (F233) and Q2 (F154) reduce to. **Verdict: Q1 does not close independently; it merges with E3+Q2 into the single constant $d_1$ — the F162 background-field computation would close all three at once.**
**Script:** `tests/findings/test_F235_sqrt_sigma_fpi_scale_setting.py`
**Results:** `test-results/F235_sqrt_sigma_fpi_scale_setting.json`
**Cross-references:** [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the $7.04\times0.569$ factorisation and the §5 scale-setting diagnosis reproduced and sharpened here), [[F86-colour-dielectric-dual-superconductor]] / [[F88-colour-condensate-from-model]] ($\sigma=2\pi v^2$, $v=0.713$), [[F146-emergent-su3-string-tension-into-bag]] (the model's own 3D SU(3) $\sigma a^2\approx0.31$, and why the $\sqrt\sigma=0.42$ GeV anchor cannot double as a *ratio* derivation), [[F144-route-a-alpha-s-dimensional-transmutation]] (A4: the same $d_1$/$\Lambda$-ratio $1.78$), [[F154-residuals-A-B-built-and-solved]] (Q2 Residual A = the same $q_\ast$/$d_1$ integral), [[F162-bgfield-self-energy-b0-gate]] (the one-loop computation that would close $d_1$), [[F233-mass-scale-N-transmutation-supersedes-F119]] (E3 — same session, same $d_1$).

---

## 1. What the prompt asked

Q1: *"Derive the $\sqrt\sigma/f_\pi$ scale-setting factor from strong-coupling running (link F144 $\alpha_s$ + F86 $\sigma$). Acceptance: $<5\%$ from the lattice with no new anchor, or a documented account of the missing scale-setting factor."*

## 2. The factorisation (reproduced) and where the residual lives

$$\frac{\sqrt\sigma}{f_\pi}=\underbrace{\frac{\Lambda}{f_\pi}}_{7.037\ \text{(exact, Pagels–Stokar)}}\times\underbrace{\frac{\sqrt\sigma}{\Lambda}}_{\text{confinement}},\qquad \sqrt\sigma=\sqrt{2\pi}\,v,\ v=0.713.$$

The chiral factor is machine-exact and closed (F124 C1/C2) — **half the ratio is fully derived and nothing here touches it.** The whole residual is the confinement factor $\sqrt\sigma/\Lambda$:

| cutoff $\Lambda$ | $\Lambda a$ | $\sqrt\sigma/\Lambda$ | $\sqrt\sigma/f_\pi$ | dev vs $4.56$ |
|---|---|---|---|---|
| per-axis $\pi/a$ | $3.1416$ | $0.5689$ | $4.003$ | $-12.2\%$ |
| equal-vol sphere $(6\pi^2)^{1/3}/a$ | $3.898$ | $0.4585$ | $3.227$ | $-29.2\%$ |
| BCC 2-atom Debye $(12\pi^2)^{1/3}/a$ | $4.914$ | $0.3637$ | $2.560$ | $-43.9\%$ |

## 3. The honest negative: no cutoff convention closes it

To reach the empirical $4.56$ one needs $\sqrt\sigma/\Lambda=0.648$, i.e.

$$\Lambda_\text{eff}=\frac{\sqrt{2\pi}\,v}{0.648}=2.758/a.$$

This is **below** the *smallest* principled Brillouin-zone cutoff (the per-axis edge $\pi/a=3.14$) and far below every equal-volume radius. **No BCC-BZ cutoff convention lands the ratio within $5\%$** — the closest, the per-axis edge, still sits $-12\%$ low. So the residual is *not* a cutoff-convention ambiguity that a better geometric choice removes; it is a true scale-setting factor. (The emergent-$\sigma$ route of F146 cannot rescue Q1 either: its $\sigma a^2\approx0.31$ is measured at $\beta=9$, and turning it into a physical ratio requires the external $\sqrt\sigma=0.42$ GeV anchor — circular for a *ratio* derivation.)

## 4. The residual is the shared $d_1$ (the unification)

F124 §5 already located this: taking $\sqrt\sigma$ from the **bare rotor** at its locked weak coupling gives $\sqrt\sigma/f_\pi\approx1.0$, a factor $\sim4$ below the condensed-vacuum $4.0$ — "precisely the QCD scale-setting / dimensional transmutation," and F124 wrote that this factor "contains this $1.78$ plus the BZ-edge convention." That $1.78$ is exactly F144-A4's $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}$ and F154's Residual-A $q_\ast$ integral. Hence:

$$\boxed{\;\text{Q1 }(\sqrt\sigma/f_\pi)\ \text{residual}\ =\ \text{Q2 }(\alpha_s\text{ scheme})\ =\ \text{E3 }(N)\ =\ \text{the one one-loop background-field constant }d_1.\;}$$

The $+12\%$ that survives after the main scale-setting is the tail of the same continuum-matching object; it is not an independent Q1 knob. Computing $d_1$ (the F162 programme: $b_0=\tfrac{11}3C_A$ already exact, the finite digit gated by the vertex form factors) closes Q1, Q2 and E3 **simultaneously**.

## 5. Checks (`test_F235_sqrt_sigma_fpi_scale_setting.py`, 2026-07-02 - 23:55)

| # | Statement | Result | Tier |
|---|---|---|---|
| C1 | reproduce F124 ($4.00$ axis, $3.23$ sphere) | $4.003$ / $3.227$ | machine |
| C2 | no principled BCC-BZ cutoff within $5\%$ ($\Lambda_\text{eff}=2.758/a<\pi/a$) | closest $-12.2\%$ | honest negative |
| C3 | residual is a scale-setting factor ($1.139$ axis) | $1.14$ | DIAGNOSTIC |
| C4 | same $d_1$ as E3 (F233/F144) and Q2 (F154) | recorded | ledger |

**Overall 4/4 PASS.**

## 6. Ledger impact

Q1 does not reach the prompt's $<5\%$ target as an independent derivation, and the honest reason is now pinned: the confinement-factor residual is the shared strong-sector matching constant $d_1$, not a cutoff choice. Re-tag Q1 **OPEN → merges with Q2/E3** (one constant $d_1$, closable by F162). The chiral half ($\Lambda/f_\pi=7.04$) remains exactly derived.

## 7. Provenance

- New: the explicit demonstration that *no* principled BCC Brillouin-zone cutoff lands $\sqrt\sigma/f_\pi$ within $5\%$ ($\Lambda_\text{eff}=2.758/a$ is sub-edge); the sharpening of F124 §5's diagnosis into the three-way Q1=Q2=E3 unification via $d_1$; the note that the F146 emergent-$\sigma$ route is circular for a ratio.
- Reused: F124 factorisation and $v=0.713$; F144-A4 / F154 $d_1$ framing; standard BZ/Debye cutoff geometry.
- Verification: `tests/findings/test_F235_sqrt_sigma_fpi_scale_setting.py` (2026-07-02 - 23:55, 4/4 PASS), results `test-results/F235_sqrt_sigma_fpi_scale_setting.json`.
