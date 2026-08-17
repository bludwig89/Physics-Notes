# F202 — Can the model source the lepton asymmetry resonant keV-DM production needs? Yes: all three Sakharov conditions are met by the model's own structure — L-violation is **derived** (F47 anti-linear Majorana step), CP violation is **available** (F53: C maximal, and the three-generation lepton sector carries 1 Dirac + 2 Majorana phases — F53's single-generation J=0 is the correct one-generation answer, not a no-go), and out-of-equilibrium + SU(2)_L sphalerons supply the rest; so the same heavy N₂,₃ sector (F201 texture) can produce both the baryon asymmetry and the ~10⁶×-larger late lepton asymmetry (the νMSM unification). The asymmetry's *size* (CP phases + N₂,₃ degeneracy) is the free, inherited residual

**Date:** 2026-06-30 - 22:30
**Numbering:** **F202** (re-checked; prior max F201).
**Status:** **Sakharov-conditions check passes structurally; magnitude not derived.** This certifies that the ingredients exist in the model's own established structure; it is not a Boltzmann computation of the asymmetry. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F202_leptogenesis_sakharov.py` (self-contained, real arithmetic).
**Tests / results:** `tests/findings/test_F202_leptogenesis_sakharov.py` → `test-results/F202_leptogenesis_sakharov_test.json` (5/5); fork dump `test-results/F202_leptogenesis_sakharov.json`.
**Cross-references:** [[F266-sterile-neutrino-dark-matter]] (resonant production needs a late lepton asymmetry — supplied here), [[F201-kev-sterile-from-eg-texture]] (the same M_R texture gives the keV DM sterile **and** the GeV N₂,₃ that do leptogenesis), [[F47-majorana-seesaw-higgs-free]] (the anti-linear Majorana step — intrinsic L-violation), [[F53-fg9-C-CP-per-species]] (C maximal; single-generation CP exact; CP is a three-generation effect), [[F75-three-generations-from-bcc-irrep-selection]] (the three generations that carry the CP phases), [[F41-hypercharge-higgs-free-su2]] (the SU(2)_L whose sphalerons convert L→B). External: νMSM ARS leptogenesis (Akhmedov–Rubakov–Smirnov 1998; Asaka–Shaposhnikov 2005); Sakharov 1967.

---

## The question

F200's resonant (Shi–Fuller) production of the keV sterile neutrino needs a primordial **lepton asymmetry** — and a large one, $\Delta L/s\sim10^{-4}$, about $10^6\times$ the baryon asymmetry. Part (b): can the model's intrinsic lepton-number violation (F47) source it, or must the asymmetry be imported?

Leptogenesis requires the three Sakharov conditions plus a way to share the asymmetry with baryons. This finding checks each against the model's **own** established structure.

## Condition 1 — L (B−L) violation: **derived**

F47's Majorana mass step is **anti-linear** (it couples $\chi$ to $\chi^*$), so lepton number is violated intrinsically — not by a posit, but by the only gauge-invariant mass a $Y=0$ singlet can have in the Higgs-free model. This is the prerequisite for any leptogenesis, and the model has it built in.

## Condition 2 — C and CP violation: **available** (three-generation)

F53 established that $C$ is **maximal** (the charged current couples to the left sector only) and that at **one** generation $CP$ is exact: the Jarlskog $J=0$ and the lone phase $\theta$ is pure gauge. Crucially, F53 §5 states this is the *correct one-generation answer*, not a deficiency — CP violation is a **three-generation** effect. The model has exactly three generations (F75), and the three-generation lepton sector with Majorana neutrinos carries physical CP phases:

| phases | count ($n=3$) |
|---|---|
| PMNS Dirac | $(n-1)(n-2)/2 = 1$ |
| Majorana | $n-1 = 2$ |
| total low-energy | **3** |

plus the heavy-sector phases that directly drive leptogenesis. So CP violation is *available* — and the leptonic Dirac phase $\delta_\text{CP}$ is now measured to be non-zero. The model neither forbids these phases nor predicts their magnitude.

## Condition 3 — out of equilibrium, and L → B: **available**

The DM sterile's Yukawa is feeble (F201: $M_D\sim$ eV → $y\sim10^{-11}$), so it never reaches thermal equilibrium (freeze-in); the two $\sim$GeV steriles $N_{2,3}$ oscillate out of equilibrium in the early universe (the ARS mechanism). The cosmological (QCA) arrow of time supplies the global departure. To share the asymmetry with baryons, the model's $SU(2)_L$ gauge structure (F27/F34/F41) gives **electroweak sphalerons** (B+L violation), which convert part of $L$ into the observed baryon asymmetry.

## Magnitude: both asymmetries from the same sector

| quantity | value |
|---|---|
| observed baryon asymmetry $Y_B=n_B/s$ | $8.7\times10^{-11}$ |
| late lepton asymmetry for resonant keV DM, $\Delta L/s$ | $\sim10^{-4}$ |
| ratio | $\sim10^{6}$ |

This $10^6$ gap is **not** a contradiction: in the νMSM the baryon asymmetry is fixed at sphaleron freeze-out ($T\sim130$ GeV), while the larger lepton asymmetry builds up *later* ($T$ down to $\sim100$ MeV), after sphalerons switch off, so it is never washed into baryons. Both are produced by the same $N_{2,3}$ via ARS oscillation leptogenesis. So one sterile sector — the heavy generations of the F201 texture — does double duty: baryogenesis and the DM-production asymmetry.

## What is derived vs available vs free

| Piece | Status |
|---|---|
| L (B−L) violation | **Derived** (F47 anti-linear Majorana) |
| C maximal | **Derived** (F53) |
| CP phases exist (3-gen: 1 Dirac + 2 Majorana) | **Available** (F53/F75; not forbidden, magnitude free) |
| out-of-equilibrium (feeble Yukawa + expansion) | **Available** |
| sphalerons for L→B | **Present** (SU(2)_L, F41) |
| same sector does baryogenesis + DM asymmetry | **Structural** (νMSM ARS) |
| asymmetry **magnitude** (CP-phase values, $N_{2,3}$ degeneracy) | **Free / inherited** — the νMSM resonance corner, not derived |

## Caveats (honest scope)

- This is a **conditions check**, not a Boltzmann computation: it certifies the ingredients exist in the model, not that a full kinetic calculation yields exactly $\Delta L/s\sim10^{-4}$.
- The large lepton asymmetry needs near-degenerate $N_{2,3}$ (resonant CP enhancement) and $O(1)$ CP phases — a specific corner of parameter space. The model **permits** it but does not **predict** the degeneracy or the phases; this fine-tuning is inherited from the νMSM, not solved here.
- The CP phases are not derived from the QCA rule; they are free entries of the 3×3 $M_D$/$M_R$.

## Relation to other findings

Completes the dark-matter line: **F200** needs a lepton asymmetry for resonant keV-sterile production, and this finding shows the model supplies all the ingredients — L-violation **derived** (F47), CP **available** (F53/F75), out-of-equilibrium + sphalerons present (F41) — with the same heavy $N_{2,3}$ sector of the **F201** texture doing both baryogenesis and the DM asymmetry. With F201 (the keV scale mechanism) and F202 (the asymmetry mechanism), the F200 sterile-neutrino dark matter is structurally complete up to two inherited free numbers: the overall Majorana scale / node-proximity (F201) and the CP-phase/degeneracy that set the asymmetry's size (F202) — the dark-matter counterpart of the single $\Omega_\Lambda$ coincidence that F196 left for dark energy.
