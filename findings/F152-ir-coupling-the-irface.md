# F152 — The **IR face** of the strong coupling: the $\alpha_\text{eff}^\ast\approx0.39$ that F151-S5 split off is the gap-saturated frozen coupling — its scale is the dual-Meissner gluon mass, it sits on QCD's decoupling/saturating branch ($\hat\alpha(0)/\pi=0.97$, $m_g\approx0.5$ GeV), and it is the normalization F150's $\lambda_6$ inherits

**Date:** 2026-06-12 - 18:05
**Status:** Partial (an interpretation + a scale derivation + a branch identification; the value $\alpha_\text{eff}^\ast$ is *imported* from F151-S5/F145, not newly computed) — 5/5 checks PASS. **Setting:** the concurrent F151 (`scheme-constant-determined`, 13:55) determined the **UV face** of the shared strong-sector constant — the rule's coupling is the **V-scheme** coupling (tree-exact, from F110's static energy), the one-loop conversion to $\overline{\rm MS}$ is the *known* $a_1=(93-10n_f)/9$, and the residual is a matching scale $q_\ast$ inside a derived $\sqrt3$ band ($\Lambda^{(3)}=347$ MeV, FLAG to $1.1\%$). Its **S5 explicitly split off the IR face** as a *distinct* object: the self-consistent chiral-SB gap fixes $\alpha_\text{eff}^\ast=0.376$ ($m_D{=}0.532$) $/\,0.411$ ($m_V{=}0.727$) $\approx0.39$, "connected through the full running but not identical" to the UV constant. **This finding develops that IR face.** (J1) The IR coupling value is $\alpha_\text{eff}^\ast\approx0.39$, sharp ($\pm$few %). (J2) Its **scale** is the model's dual-Meissner gluon mass $m_D$: the gap-massive propagator freezes the running at $m_D$, with $m_D/\Lambda=O(1)$, so $\alpha(0)$ is **finite** — the model is on the **saturating/decoupling branch**, not the Landau-pole branch. (J3) That is the branch real QCD occupies: the process-independent charge saturates at $\hat\alpha(0)/\pi=0.97(4)$ *because* of a gluon mass gap $m_g=0.50(20)$ GeV, and the model **generates** that gap by mechanism (the dual superconductor *is* the IR saturation); $\alpha_\text{eff}^\ast\approx0.39$ lies in the continuum frozen-coupling range ($\sim0.3$–$0.5$, MOM/V/APT). (J4) **Correcting the F150/F145 "one shared number" framing** per F151-S5: $\lambda_6$ (F150) and χSB (F145/F77) both belong to **this** (IR) face, *not* to the UV scheme constant. (J5) The IR face is **not identical** to the UV constant; the residual is the full nonperturbative crossover solve that would yield $\alpha_\text{eff}^\ast$ without the F77 fit. See §7.
**Module:** `ca-simulation/ca_ir_coupling.py` (reuses `ca_alpha_s_running.py`)
**Script:** `tests/findings/test_F152_ir_coupling.py` (~2 s, numpy + stdlib)
**Results:** `test-results/F152_ir_coupling.json`
**Cross-references:** [[F151-scheme-constant-determined]] (the **UV face** — V-scheme, $a_1$, $q_\ast$ band; **S5 is the split this finding develops**; concurrent session, 13:55), [[F145-route-c-induced-njl-coupling]] (the self-consistent gap whose $\alpha_\text{eff}^\ast$ is the IR number; the gap-massive propagator $1/(K+M_g^2)$ that freezes the running), [[F150-eg-sextic-brake-from-architecture]] ($\lambda_6$ — reassigned here to the IR face), [[F88-colour-condensate-from-model]] / [[F117-gap-coupled-dielectric-gluon-propagator]] (the dual-Meissner mass $m_D$ — the freeze scale), [[F86-colour-dielectric-dual-superconductor]] ($\sigma=2\pi v^2$; confinement = IR-saturation gap), [[F77-njl-gap-rpa-selfconsistent]] ($M(0)=1.50$ constituent mass anchoring $\alpha_\text{eff}^\ast$), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the scale-setting now on the UV face, F151), [[F101-strong-coupling-sigma-compact-rotor]] (the Gaussian→confinement crossover = the residual solve), [[F146-emergent-su3-string-tension-into-bag]] ($\sqrt\sigma=0.42$ GeV anchor).

---

## 1. Two faces, not one

F144-A4, F145-N5, F124 §5 and F150 §4 each met "one nonperturbative number" and conjectured it was shared. The concurrent **F151 resolved the structure**: it is **two** objects, connected by the running but not identical.

| face | what it is | status |
|---|---|---|
| **UV** | the rule→$\overline{\rm MS}$ scheme constant | **determined (F151):** V-scheme + $a_1=\tfrac{11}{3}$ exact + $q_\ast$ in a $\sqrt3$ band; $\Lambda^{(3)}=347$ MeV |
| **IR** | the gap-saturated effective coupling $\alpha_\text{eff}^\ast$ | **this finding:** value $\approx0.39$, scale $m_D$, saturating branch |

F151-S5 stated the IR value and flagged it as a distinct target. This finding gives that IR face its physical content: *what it is* (a frozen, gap-saturated coupling), *at what scale* (the gluon mass gap), *on which branch* (decoupling), and *what it owns* (χSB and $\lambda_6$).

## 2. J1 — the IR coupling value

From the self-consistent resolved chiral-SB gap (F145 kernel, constituent mass $M(0)=1.50$ = F77), the IR effective coupling is

$$\alpha_\text{eff}^\ast=0.376\ (m_D{=}0.532,\ \text{F88})\ /\ 0.411\ (m_V{=}0.727,\ \text{F117}),\qquad \langle\alpha_\text{eff}^\ast\rangle\approx0.39,$$

sharp and stable ($\pm$few % across the F88↔F117 MC spread, $\approx9\%$). This is **the IR coupling** — the strong-coupling-crossover value at which the condensate forms. (Imported from F151-S5/F145; this finding interprets and places it, it does not recompute it.)

## 3. J2 — the scale is the gluon mass gap; the branch is saturating

The freeze scale is not free. The gap-massive gluon propagator $1/(K+m_D^2)$ stops the running once $\mu\lesssim m_D$ — gluon decoupling — so the freeze scale **is** the dual-Meissner mass $m_D$. With the rule's running $\Lambda^{(3)}=0.49$ GeV and the gap at $m_D\sim\sqrt\sigma=O(0.3$–$0.5)$ GeV,

$$\frac{m_D}{\Lambda}=O(1)\quad(0.86;\ \text{continuum }m_g/\Lambda=1.02)\ \Longrightarrow\ \alpha(0)\ \text{finite}.$$

A finite $\alpha(0)$ is the **saturating/decoupling branch** — the model does not run into a Landau pole; the same mass gap that confines (dual superconductor) screens the IR coupling.

## 4. J3 — the branch real QCD occupies (continuum grounding)

Real QCD's process-independent charge **saturates** at $\hat\alpha(0)/\pi=0.97(4)$ [Cui–Zhang–Binosi–Roberts, lattice], *caused* by a gluon mass gap $m_g=0.50(20)$ GeV. The model produces that gap from its own dynamics ($m_D$, F88/F117) at the same $\approx0.5$ GeV scale, so it is on the correct branch **by mechanism** — confinement and IR saturation are the *same* gap, not two fits. Quantitatively $\alpha_\text{eff}^\ast\approx0.39$ sits squarely in the continuum frozen-coupling window ($\sim0.3$–$0.5$ in MOM/V/APT schemes). (The process-independent $\hat\alpha(0)=0.97\pi\approx3.05$ is a *larger-normalization* scheme; only the scheme-free statement — gap-driven saturation at an $O(0.4)$ frozen coupling — is claimed as a match.)

## 5. J4 — $\lambda_6$ lives on the IR face (correcting F150 §4)

F150 §4 placed the $E_g$ brake $\lambda_6$ in "the same single IR-coupling normalization" as F124/F144/F145, before F151 split the faces. With the split, the assignment sharpens: $\lambda_6$ is fixed in the **saturation regime** (F95/F118 require the saturated internal amplitude), so it belongs to the **IR face**, alongside χSB (F145/F77) — *not* to the UV scheme constant (which F151 determined cleanly with $a_1$). So the IR face owns two physical residuals (χSB and $\lambda_6$); the UV face owns the scale-setting. This is the corrected ledger.

## 6. J5 — relation to the UV face, and the residual

Per F151-S5, the IR face is **connected to the UV constant through the full running but is not identical** to it: locating $\alpha_\text{eff}^\ast$ on the perturbative running is pole-dominated and unreliable; it is a genuinely nonperturbative (strong-coupling-crossover) quantity. The residual is therefore the **full self-consistent crossover solve** — the $M(k)$ gap equation / the F101 Gaussian→confinement crossover — which would yield $\alpha_\text{eff}^\ast$ (and hence $m_c$, $f_\pi$, $\lambda_6$) without the F77 fit. That solve is the single open computation of the IR face, just as the one-loop background-field $q_\ast$ integral is the single open computation of the UV face (F151 §8).

## 7. What this finding is and is not

- **Is:** the physical interpretation of F151-S5's IR number — value $\alpha_\text{eff}^\ast\approx0.39$, **scale** = the dual-Meissner gluon mass gap (freeze derivation), **branch** = saturating/decoupling with continuum grounding ($\hat\alpha(0)$, $m_g$, the frozen-coupling window), and the **reassignment** of $\lambda_6$/χSB to this face (correcting the pre-F151 "one number" framing).
- **Is not:** a new computation of $\alpha_\text{eff}^\ast$ (it is F151-S5/F145's), nor of the UV scheme constant (F151's), nor of the crossover solve (the residual).

## 8. Check summary (`test_F152_ir_coupling.py`, 2026-06-12 - 18:03)

| Check | Statement | Tier | Result |
|---|---|---|---|
| J1 | $\alpha_\text{eff}^\ast=0.376/0.411\approx0.39$, spread $\approx9\%$ | imported (F151-S5/F145) | PASS |
| J2 | $m_D/\Lambda=0.86$, $m_g/\Lambda=1.02$; $\alpha(0)$ finite ⇒ saturating branch | numeric | PASS |
| J3 | continuum $\hat\alpha(0)/\pi=0.97(4)$, $m_g=0.5(2)$ GeV; gap matches; $\alpha_\text{eff}^\ast\in[0.3,0.5]$ | grounding | PASS |
| J4 | $\lambda_6$ (F150) + χSB (F145/F77) on the IR face, not the UV scheme constant | ledger | PASS |
| J5 | IR face $\ne$ UV constant (F151-S5); residual = crossover solve | structural | PASS |

**Overall 5/5 PASS** (~2 s).

## 9. Honest scope

- The IR value $\alpha_\text{eff}^\ast$ is **imported** from F151-S5/F145; this finding contributes its scale, branch, and continuum placement, not its computation.
- $m_D\sim\sqrt\sigma$ is an $O(1)$ cross-lattice proxy ($m_D$ measured in the F88 U(1) surrogate at $\beta=1.8$; SU(3) ensembles differ by $O(1)$); the robust content is the *branch* and $m_D/\Lambda=O(1)$.
- The continuum $\hat\alpha(0)=0.97\pi$ is a different scheme from $\alpha_\text{eff}^\ast$; only the qualitative gap-driven-saturation statement and the $O(0.4)$ frozen-coupling magnitude are claimed.
- The residual (the crossover solve) is genuinely open; this finding is interpretive consolidation built on F151's determination, not a new nonperturbative result.

## 10. Provenance

- **New content:** the development of F151-S5's IR face — freeze-scale = $m_D$ (derivation), saturating/decoupling-branch placement with continuum grounding ($\hat\alpha(0)$, $m_g$, frozen-coupling window), and the reassignment of $\lambda_6$/χSB to the IR face (correcting the pre-F151 framing).
- **Reused:** F151-S5 $\alpha_\text{eff}^\ast$, F145 gap/propagator, F144 running (`ca_alpha_s_running`), F88/F117 $m_D$, F86 $\sigma=2\pi v^2$, F146 $\sqrt\sigma$ anchor.
- **External anchors (targets, not inputs):** $\hat\alpha(0)/\pi=0.97(4)$ [Cui–Zhang–Binosi–Roberts, arXiv:1912.08232]; $m_g\approx0.5(2)$ GeV [Landau-gauge lattice, arXiv:1002.4151 / 1010.1975]; continuum frozen coupling $\sim0.3$–$0.5$ (MOM/V/APT).
- **Verification:** `tests/findings/test_F152_ir_coupling.py` (2026-06-12 - 18:03, 5/5 PASS), results `test-results/F152_ir_coupling.json`.
