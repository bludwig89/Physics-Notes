# F195 — Fully stable block-spin atom for a general element (Z, N)

**Date:** 2026-06-30 - 22:10
**Status:** Confirmed — 9/9 checks PASS (`test_F195_blockspin_element_atom.py`). Tier A certified on H → He → Li → C; Tier B (live quarks) smoke-certified on He.
**Roadmap:** `roadmap-unified-real-space.md` U4 — generalises the F160 live two-grid hydrogen atom to a general element.
**Modules:** `src/casim/particles/channel.py` (`ElementAtomChannel`, type `element_atom`; `AtomStabilityReadout` observer; `_spatial_orbitals`, `_gram_schmidt` helpers); reuses `ca-simulation/ca_multigrid.py` (`schrodinger_step`/`coarse_point_potential`) and `ca_manybody.aufbau_configuration`; `casim.gravity.solve_poisson_3d_open` (F64 kernel). Scenarios `stable_atom_{helium,lithium,carbon}.yaml` + matched `_free` controls.
**Cross-references:** [[F160-live-two-grid-multigrid-atom]] (the channel generalised), [[F159-u4-blockspin-multigrid-scale-separation]] (R_b charge-faithful, point-vs-resolved gap→0), [[F158-realspace-neutral-hydrogen-atom]], [[F157-manybody-nuclei-and-electron-clouds]] (the spectra/configurations mirrored live), [[F156-realspace-em-bound-electron]] (the split-step orbital), [[F148-modular-element-assembler]] (`build_element`), [[F136-colour-triplet-dirac-quark-confinement]] (the Tier-B confined nucleon), [[F133-blockspin-casim-engine]] (R_b).

## Result

A single CASIM channel (`element_atom`) co-evolves a multi-nucleon nucleus and
a multi-electron cloud for a general element **(Z, N)**, on two block-spin
(R_b)-coupled grids, in one `Simulation.run()`. It is the F160 two-grid
hydrogen atom generalised in three additions:

1. **Multi-nucleon fine patch → +Z coarse point.** The fine patch holds
   **A = Z+N** nucleon charge blobs (the first Z are protons, each integrating
   to +1; the N neutrons carry zero net charge). The summed charge density
   integrates to **exactly +Z** and is R_b-reduced to a single **+Z** coarse
   point source — faithful to F159 (the electron cannot resolve nuclear
   structure as a₀/r_nuc → ∞). This is **Tier A**, the physically correct
   statement for the *electron* sector. **Tier B** (He-capped) runs **3·A live
   `quark_dirac` quarks** grouped into A confined nucleons instead.

2. **Multi-electron coarse grid with Pauli filling.** The Z electrons fill the
   Aufbau configuration (`aufbau_configuration(Z)`) as **distinct spatial
   orbitals with Hund's rule** (He 1s² → 1 orbital; Li 1s²2s¹ → 2; C 1s²2s²2p²
   → 4, the two 2p singly occupied). Each orbital is an exactly-unitary F156
   split-step packet evolving in the **self-consistent mean field** = the +Z
   nuclear well **+** the live Hartree repulsion of all *other* electrons
   (`ρ_others,i = ρ_tot − |ψ_i|²`, mirroring `ca_manybody._hartree_potential`,
   evaluated live on the coarse grid each tick). **Pauli antisymmetry** is
   enforced by **Gram–Schmidt** orthonormalising the occupied orbitals each
   tick — the "helium needs the antisymmetriser" item F148/F157 flagged.

3. **Whole-atom stability readout + acceptance gate** (`atom_stability_readout`).

### Certified on the ladder (Tier A, ≥300-tick runs; results JSON `test-results/F195_blockspin_element_atom.json`)

| element | (Z,N) | orbitals (occ) | net charge | norm drift | max ⟨i\|j⟩ | cloud RMS reldrift | free max / bound max | decades |
|---|---|---|---|---|---|---|---|---|
| H  | (1,0) | 1s¹ (1)          | 2.2e-16 | 3.0e-15 | 0.0    | 0.059 | 3.8× | 5.07 |
| He | (2,2) | 1s² (2)          | −2.2e-16 | 7.4e-16 | 0.0    | 0.023 | 5.6× | 4.48 |
| Li | (3,4) | 1s² 2s¹ (2,1)    | 0.0     | 5.3e-16 | 1.8e-16 | 0.085 | 2.3× | 4.86 |
| C  | (6,6) | 1s² 2s² 2p² (2,2,1,1) | 0.0 | 7.9e-16 | 3.5e-15 | 0.141 | 3.7× | 4.65 |

- **Net charge ≡ 0 to machine precision** — Z protons (+Z) + Z electrons (−Z),
  the electron occupancies summing to Z exactly (integers).
- **Norms conserved to ~1e-15** — every orbital split-step is exactly unitary;
  Gram–Schmidt renormalises each orbital to unit norm, so the conserved scalar
  Σ occ_i = Z is held exactly.
- **Pauli orthogonality to ~1e-15** — the occupied orbitals stay mutually
  orthogonal across the whole run (He/H trivially: one orbital).
- **Every radius bounded over ≥300 ticks** — cloud RMS neither collapses
  sub-cell nor disperses; each individual shell stays well inside the box.
- **Cloud surrounds nucleus + tracks it** — the represented cloud radius is
  ≫ the nucleus radius and the cloud centroid sits on the nucleus
  (separation ~1e-4 cells ≪ cloud radius).
- **Bounded-vs-ballistic exhibited, not asserted** — the matched `_free`
  control (no nuclear well, no e–e field) disperses to 2.3–5.6× the bound cloud
  RMS while the bound run stays flat.
- **Represented a₀/r_nuc ≈ 4.5–5.1 decades**, carried by the block factor
  b = 30000 on tractable lattices (fine 12, coarse 28).

### Tier B (He) — live A-body fine patch (smoke-certified)

12 live `quark_dirac` quarks (2 protons uud + 2 neutrons udd), each nucleon
confined by the F135 scalar Y-string: net charge −9e-14, norm drift 4e-14,
**nucleus charge from the live `rho_em` = +2.000** (R_b-reduced to the +2 coarse
well), the quarks **loop-live** (‖J_em‖ ≈ 6.6, Σ‖rho_em‖ = 6.000 = 3·A·⅔). The
nucleus cluster RMS stays bounded within the fine patch (< 5 of 12 cells), but
**breathes ~50 %** over 80 ticks. At the time of writing this was attributed to
the inter-nucleon one-boson-exchange binding (σ F126 + ω F128 + π-tensor F104 +
quark-Pauli core F113) being unwired in Tier B.

**Update (F206, 2026-06-30):** the inter-nucleon OBE binding is now **wired and
certified** — the A nucleons are mutually bound to a bounded equilibrium set by
the model's own repulsive core (`_setup_nn_potential` + `_apply_nn_binding`,
exactly-unitary scalar-mass; deuteron + He-4, 6/6 PASS). [[F206-tierB-internucleon-nn-binding]]
also showed the ~50 % "breathing" is in fact **intra-nucleon** blob spread (the
single-nucleon F136 Y-string softening; com-RMS, the genuine inter-nucleon
coordinate, drifts only −6.5 % unbound). The remaining Tier-B frontier is
therefore single-nucleon confinement stiffness, not inter-nucleon binding.
Tier A is the certified electron-sector path for the full ladder.

## Mechanism — why it is "fully stable"

The atom is **two unitary evolutions glued by an exact, charge-faithful R_b
reduction**:

- The nuclear charge enters the electron sector only as its **total +Z**
  (F159: the point-vs-resolved binding gap → 0 as a₀/r_nuc grows), so the
  electron never needs to resolve A nucleons — it sees a +Z point. Net charge
  is therefore an integer identity, exact to machine precision.
- Each electron orbital is propagated by the **exactly-unitary Strang
  split-step** (F156) in a *real* potential, so its norm is conserved to the
  FFT floor regardless of the mean field. The conserved scalar is the integer
  electron count Z.
- **Pauli** is the genuinely new engineering: without orthogonalising the
  occupied orbitals, two electrons collapse into the same 1s and helium is
  wrong. Live Gram–Schmidt (the proper Hermitian inner product Σ ψ_i* ψ_j) is
  the antisymmetriser; because the orbitals start as self-consistent eigenstates
  and stay stationary, the GS corrections are ~1e-15 and never destabilise.
- The **live Hartree mean field** (e–e repulsion, like-charge sign per F156's
  `φ_em = −φ_Poisson(ρ)`) is recomputed on the coarse grid each cadence from the
  current orbitals; Poisson linearity lets the per-orbital self-interaction
  removal cost one total solve plus one per orbital.

The deeper coarse coupling (k = 0.6) that certifies the *whole* ladder is a
**representation choice** (the coarse spacing/coupling is P6/scale-gated, F123):
it keeps the diffuse Li 2s bound inside the tractable box. Structure (shells,
Hund filling, neutrality, the surrounds-and-tracks geometry) and the represented
scale ratio are the deliverable; absolute fm/eV stay P6-gated.

## Consistency with the F157 spectra

The live configurations reproduce the F157 *structure*: He closed shell 1s²
(spectral IP 24.0 eV, CODATA 24.59) over a closed 2p2n nucleus (spectral α
−30.1 MeV, exp −28.3, 6 %); Li opens 2s¹; C fills 2p² by Hund (two singly
occupied p orbitals, kept orthogonal live). The live run is consistent with the
F157 spectra as *structure* — it does not re-derive the absolute eV/MeV (those
are the F125/F157 spectral solves; here they are P6-gated).

## Scope — what is certified vs wired

- **Certified (machine-precision + Tier-3 bounded):** the full electron-sector
  stability of H, He, Li, C — net charge, norms, Pauli orthogonality, bounded
  radii over long runs, surrounds-and-tracks geometry, bounded-vs-free control,
  represented scale.
- **Smoke-certified:** Tier B He (12 live confined quarks; loop-live, +Z from
  `rho_em`, net charge + norms machine-precision, cluster bounded within the
  patch).
- **Certified (F206):** Tier B inter-nucleon binding (NN OBE) — the A nucleons
  bind to a bounded, core-limited equilibrium (deuteron + He-4, exactly unitary).
  The residual ~50 % breathing is intra-nucleon (F136 confinement), not the OBE.
- **Wired, not certified:** d/f angular seeds beyond carbon. Open shells heavier than
  carbon and a fully *converged* live SCF for diffuse valence shells without the
  representation-deepening of the coarse well remain the frontier (the F157
  "heavy A overbinds / SCF is the frontier" line, here for the live electron
  sector).

## Reproduce

```bash
PYTHONPATH=src python tests/findings/test_F195_blockspin_element_atom.py
PYTHONPATH=src python -m casim.cli run scenarios/stable_atom_helium.yaml
PYTHONPATH=src python -m casim.cli run scenarios/stable_atom_helium_free.yaml
```
