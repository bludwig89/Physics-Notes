# F201 — Does the lattice prefer a keV sterile? The F93/F76 Z₃ (E_g) generation texture, applied to the F47 Majorana matrix M_R, has cancellation nodes where one eigenvalue → 0 — so **one light sterile is structural** (the generation nearest a node, exactly as the electron is the lightest charged lepton); with overall scale M_R0 ~ GeV and a node-proximity δ_ν ≈ 0.14°, it lands M₁ ≈ 5.6 keV and M₃ ≈ 5.6 GeV (the νMSM split). keV is not pinned, but its smallness is no longer mysterious

**Date:** 2026-06-30 - 22:00
**Numbering:** **F201** (re-checked; prior max F200).
**Status:** **Mechanism for one light sterile, derived from the existing texture; the keV value accommodated (two inputs).** The texture and its node are exact; the charged-lepton reproduction is the known F76/F93 result; the keV landing requires the overall scale M_R0 and a node-proximity. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F201_kev_from_eg_texture.py` (self-contained, real arithmetic).
**Tests / results:** `tests/findings/test_F201_kev_from_eg_texture.py` → `test-results/F201_kev_from_eg_texture_test.json` (5/5); fork dump `test-results/F201_kev_from_eg_texture.json`.
**Cross-references:** [[F266-sterile-neutrino-dark-matter]] (the keV sterile whose scale this addresses), [[F47-majorana-seesaw-higgs-free]] (the M_R the texture is applied to; the 3×3 sterile spectrum), [[F93-orthorhombic-Eg-vacuum]] / [[F76-generation-mass-hierarchy-crystal-field]] (the Z₃/E_g texture √m_a = M_0[1+√2cos(δ+2πa/3)] and its angle), [[F75-three-generations-from-bcc-irrep-selection]] (three generations of the same singlet), [[F92-per-constituent-phase-consistency]] (the √2 equipartition amplitude). External: νMSM mass split (keV DM sterile + GeV heavy steriles).

---

## The question

F200 identified the dark-matter relic as the F47 keV sterile neutrino but left its keV mass as a free eigenvalue of the 3×3 Majorana matrix M_R. Part (a) of the follow-up: does anything in the lattice *prefer* a keV eigenvalue, or is it as unexplained as in the bare νMSM?

## The mechanism: the generation texture has cancellation nodes

The charged-lepton masses follow the F76/F93 Z₃ (E_g-condensate) texture
$$\sqrt{m_a}=M_0\big[\,1+\sqrt2\cos(\delta+\tfrac{2\pi a}{3})\,\big],\qquad a=0,1,2,$$
the crystal field that splits the F75 $T_{1u}$ generation triplet. The right-handed Majorana sector is **three copies of the same singlet on the same BCC lattice**, so M_R should carry the *same* texture — with its own condensate angle $\delta_\nu$ (a different sector may sit at a different angle).

This texture has **Z₃ cancellation nodes**: where $1+\sqrt2\cos\phi=0$, i.e. $\phi=135°$, one $\sqrt{M_a}\to0$, so that eigenvalue is parametrically light. A light sterile is therefore the generation that sits *nearest a node* — structurally the same reason the electron is the lightest charged lepton.

**Reproduction check.** At the charged-lepton angle $\delta_e=12.73°$ the texture gives mass ratios $[2.875\times10^{-4},\,5.946\times10^{-2},\,1]$ versus the observed $[2.876\times10^{-4},\,5.946\times10^{-2},\,1]$ — the known F76/F93 agreement, confirming the texture is the right object.

## A light sterile is natural; keV needs two inputs

Scanning $\delta_\nu$ toward the node, the lightest-to-heaviest eigenvalue ratio collapses:

| $\delta_\nu$ | $M_\text{min}/M_\text{max}$ |
|---|---|
| 60° (anti-node) | $5.9\times10^{-2}$ |
| 130° | $1.5\times10^{-3}$ |
| 134° | $5.5\times10^{-5}$ |
| 134.9° | $5.4\times10^{-7}$ |
| 134.99° | $5.4\times10^{-9}$ |

To realise the νMSM split $M_1/M_3\sim10^{-6}$ requires $\delta_\nu=134.86°$ — a proximity of $2.4\times10^{-3}$ rad ($\approx0.14°$) to the node. With the overall scale set to the νMSM heavy-sterile value $M_{R0}\sim1$ GeV, the texture lands:
$$M_1\approx5.6\ \text{keV (the DM sterile)},\qquad M_3\approx5.6\ \text{GeV (the heavy steriles)}.$$

So the **hierarchy is structural** (a node of the same texture that orders charged leptons), and the keV value is **accommodated** with two inputs: the overall scale $M_{R0}\sim$ GeV and the node-proximity $\delta_\nu\approx0.14°$. The tuning is modest ($\sim10^{-3}$ rad), not the $10^{-6}$ one might fear — because the suppression is on $\sqrt M$, so a $10^{-3}$ angular proximity yields a $10^{-6}$ mass ratio.

## What is derived vs computed vs accommodated

| Piece | Status |
|---|---|
| M_R carries the F93 Z₃/E_g texture (same singlet, same lattice) | **Argued** (structural; not a new posit) |
| Z₃ node at 135° where one eigenvalue → 0 | **Derived** (exact: $1+\sqrt2\cos135°=0$) |
| texture reproduces charged-lepton hierarchy at $\delta_e$ | **Computed** (matches data to $10^{-4}$; known F76/F93) |
| near-node → parametrically light eigenvalue | **Computed** (monotone collapse) |
| $M_{R0}\sim$ GeV, $\delta_\nu\approx0.14°$ → keV + GeV (νMSM split) | **Computed**, conditional on the two inputs |
| overall scale $M_{R0}\sim$ GeV | **Accommodated** (νMSM heavy scale, not derived) |
| the node-proximity $\delta_\nu$ | **Accommodated** (free angle, modest tuning) |

## Caveats (honest scope)

- That M_R inherits the *same* angle-texture as the charged leptons is a structural argument (same field, same lattice), not a derivation from the QCA rule; the neutrino sector is allowed its own $\delta_\nu$.
- keV is **not pinned**: it needs the overall scale and the node-proximity. The advance is that the *smallness* (a $10^{-6}$ hierarchy) is now natural — it is one node-proximity, not a $10^{-6}$ fine-tuning.
- The overall scale $M_{R0}\sim$ GeV is the νMSM heavy-sterile scale, itself not derived here.

## Relation to other findings

Addresses the keV-scale residual of **F200** using the **F93/F76** Z₃/E_g texture (validated on the **F75** charged-lepton triplet) applied to the **F47** Majorana matrix. Result: one light sterile is structural (a Z₃ node), so the νMSM keV DM scale and the GeV heavy-sterile scale emerge together from one texture plus an overall scale. Pairs with **F202** (whether the same sector sources the lepton asymmetry resonant production needs). The remaining inputs ($M_{R0}$, $\delta_\nu$) are the dark-matter analog of where the rest of the program sits: identity and mechanism settled, one scale/angle outstanding.
