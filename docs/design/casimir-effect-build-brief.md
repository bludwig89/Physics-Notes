# Build Brief / Next-Session Prompt — The Casimir Effect in the BCC Weyl-QCA Model

**Type:** design brief + handoff prompt (promote to a finding when computed)
**Date:** 2026-06-30 - 21:01
**Research phase complete:** see `references/casimir-force-literature-and-model-integration.md` (literature + integration analysis). Read it first.
**Precedent to mirror:** `docs/design/alcubierre-warp-structural-test.md` → promoted to [[F204]]. Same shape: confront a known result with the model's already-derived constraints, compute, record.

---

## Copy-paste prompt for the next session

> You are continuing the Physics Notes project. Build and test the Casimir effect inside the BCC Weyl-QCA model, then write it up as a finding. The research phase is done — read `references/casimir-force-literature-and-model-integration.md` and this brief before coding. Do **not** introduce new physics; the photon ([[F69]]), the dispersion ([[F26]]), the cell scale ([[F107]]), the beable gravity source ([[F178]]/[[F193]]) are all already derived. Your job is to (1) compute the static Casimir energy on the lattice and recover the continuum law, (2) settle the consistency question with [[F193]] (does the Casimir energy gravitate, and as what), and (3) evaluate the two model-specific predictions (Archimedes weighing, dynamical-Casimir pair emission). Follow CLAUDE.md: closed-form/audited dispersion only — **no `np.linalg.eig` on chiral matrices** (build the mode sum from the [[F26]] closed form). Algebraic exactness first, then machine precision. Re-check the max F-number before numbering (concurrent sessions; current max is **F206**, so take the next free number ≥ F207). Add a changelog entry, an exactness-inventory row, and run `python3 tools/regen_indexes.py` at the end.

---

## Objective

Show the model reproduces the measured Casimir force *and* that doing so is consistent with [[F193]] (homogeneous zero-point energy does not gravitate), by computing the force in the **source/van der Waals channel** ($H_\text{int}$ = [[F69]] photon coupled to matter), not from a gravitating vacuum sum. Then quantify the two predictions that go beyond reproduction.

## The integration thesis to test (from the research phase)

1. **Reproduction.** Lattice mode-difference of the [[F69]] paired-spinor photon between bounded and free regions → continuum limit $F/A=-\pi^2\hbar c/240\,L^4$.
2. **Consistency with [[F193]].** Gravitating ≠ force. The force is a beable/$H_\text{int}$ effect; the homogeneous $\sum\tfrac12\hbar\omega$ stays a non-gravitating superimposable. Jaffe (2005) / Nikolić (2016) make the source picture the fundamental one — the model sits on the consensus side.
3. **Archimedes prediction.** The Casimir energy is van der Waals *binding energy* of the matter → **beable → gravitates as $\Delta m=E_C/c^2$**, not as "weighable vacuum modes." Compute whether this is numerically distinguishable from the SEP-vacuum-buoyancy prediction (Calloni et al.) in the Archimedes design.
4. **Dynamical Casimir prediction.** A modulated boundary emits [[F69]] quanta **in pairs** ("only occurs as a pair") — check the pair-correlation / two-mode structure.

## Concrete checks to implement (suggested tiers, mirror F-finding style)

| # | Check | Method | Target / gate |
|---|---|---|---|
| C1 | Static Casimir energy, 1D scalar warm-up | mode sum minus integral on a length-$L$ chain, cell $a$ | recover $-\pi\hbar c/24L^2$ (1D) to continuum |
| C2 | 3D EM (perfect plates) via [[F69]] dispersion | sum [[F26]] photon modes between plates − free space; $a$ = UV cutoff | $-\pi^2\hbar c/240L^4$ in $a/L\to0$, within ~1% |
| C3 | Lattice signature | leading correction in $a/L$ | quote the $\mathcal{O}((a/L)^2)$ coefficient (the model's falsifier) |
| C4 | Source-channel consistency | confirm the force comes from $H_\text{int}$ (charge-current), force $\to0$ as coupling $\to0$ (Jaffe limit) | qualitative + scaling check vs. [[F193]] superimposable |
| G1 | Archimedes: does $E_C$ gravitate? | feed $E_C$ as beable $T^{00}$ into the [[F178]]/[[F106]] dielectric source ($\nabla^2\ln K=-8\pi T^{00}$) | weight change $=E_C/c^2$; compare to vacuum-buoyancy magnitude |
| D1 | Dynamical Casimir | drive a boundary in `ca_photon_pair`; count emitted quanta | photons emitted in **F69 pairs**; two-mode correlation present |

Start with C1 (1D scalar) to validate the mode-sum machinery cheaply, then C2/C3 with the real [[F69]] dispersion. G1 and D1 are the distinctive-prediction tiers; C-tier alone is enough for a first finding if G/D run long.

## Repo hooks (already verified)

- Photon: `ca-simulation/ca_photon_pair.py` — paired-spinor [[F69]] photon; dispersion `Ω_pair(k)=ω⁺(k/2)+ω⁻(k/2)≡Ω_even`; propagator = `ca_wmu._f26_rotation_step`; $c=1/\sqrt3$. Build the Casimir mode sum on this dispersion.
- Cell scale: [[F107]] $a=\sqrt{8\pi}\,3^{1/4}\ell_P\approx1.07\times10^{-34}$ m (the UV regulator).
- Gravity source: [[F178]] full-tensor / [[F106]] $\nabla^2\ln K=-8\pi T^{00}$ (ca_gravity.py) for G1; [[F193]] for the beable-vs-superimposable distinction.
- Prior proposal this supersedes: `deprecated/lattice-vs-spacetime-tests.md` QG-3 (PROPOSED, never built).
- Conventions: new finding `findings/F{N}-casimir-*.md`; test `tests/findings/test_F{N}_casimir.py`; results JSON in `test-results/`; datestamp `yyyy-mm-dd - hh:mm`; escape `|` as `\|` in tables; markdown math in files / unicode to the user.

## Deliverables for that session

1. `ca-simulation/ca_casimir.py` (or extend `ca_photon_pair.py`) — the mode-sum + continuum-limit machinery.
2. `tests/findings/test_F{N}_casimir.py` + `test-results/F{N}_casimir.json`.
3. `findings/F{N}-casimir-*.md` — the finding (reproduction + [[F193]] consistency + whichever of G1/D1 completed).
4. Changelog entry, exactness-inventory row, `regen_indexes.py` run.

## Caveats to respect (do not overclaim)

- "Casimir energy gravitates as binding energy" is a *reasoned* integration, **not yet computed** — G1 must derive it before the finding states it.
- Whether the model's Archimedes prediction is distinguishable from SEP-vacuum-buoyancy is **unknown** — compute before claiming a "first lab gravity test."
- Real-material corrections (Drude/plasma, temperature, roughness, the graphene puzzle) are QED matter-modeling, **not** foundational tests — keep them out of the core gate.
- numpy/scipy on chiral transforms is unreliable (CLAUDE.md) — audited closed-form dispersion only.
