# Next-session prompt — build the **fully stable blockspin atom**: multi-nucleon nucleus + multi-electron shells, general (Z,N)

`2026-06-30 - 18:45` — handoff. Paste the **PROMPT** block below into a fresh session. Everything it needs is in this repo; exact paths/handles are in §Reference.

**Goal.** Lift the live two-grid atom from **hydrogen only** (F160, one `uud` proton + one electron) to a **general element (Z,N)**: a bound multi-nucleon nucleus on the fine patch, block-spin (R_b) reduced to a `+Z` point charge on the coarse grid, with **Z Pauli-filled electron shells** bound around it — all co-evolving in one `Simulation.run()`, **net charge → 0**, and **stable** (every radius bounded, every norm conserved) over a long run. Verify on the ladder **H → He → Li/C**.

**Why this is the right next step (the honest gap).** The pieces exist but have never been run together live:
- F160 `two_grid_atom` is the live multigrid atom — but hardcoded to **one** `uud` proton and **one** electron orbital.
- F157 `ca_manybody.py` has the multi-nucleon A-body cluster (α-particle −30.1 MeV) and the multi-electron Hartree cloud (He IP 24.0 eV) — but only as **spectral/variational** solves, not a live lattice scenario.
- F148 `build_element(Z,N)` composes them — but the Z≥2 / A≥2 paths route through the spectral solvers, not a CASIM run.

So the deliverable is **not new physics** — it is generalising the audited F160 channel and wiring the F157 many-body content into it, then proving the assembled object is *stable* on the lattice.

---

## PROMPT (paste this)

> You are continuing the "universe in a bottle" QCA project (read `CLAUDE.md` first). Read findings **F160** (live two-grid hydrogen — the channel you will generalise), **F159** (the R_b multigrid + charge-faithfulness proof), **F158** (single-lattice neutral H), **F157** (multi-nucleon A-body cluster + multi-electron Hartree, the many-body content), **F156** (the non-rel bound-electron split-step), **F148** (the `build_element(Z,N)` assembler), and skim `docs/roadmaps/roadmap-unified-real-space.md` (U4) + `roadmap-scale-to-real-space.md` §2 (the scale-separation wall). Your job: **build a fully stable blockspin atom for a general element (Z,N)** and certify it on **H → He → Li/C**. Work to the project discipline: exhibit the mechanism, machine-precision the conserved quantities (charge, norms), Tier-3 the radii/binding; absolute fm/eV stay P6/scale-gated (F123). Document as a NEW finding — **check `findings-index.md` for the next free F-number first** (concurrent sessions have been taking numbers; the matter-sector line is at F161, the gravity/dark line is at ~F200, so verify before you write).
>
> **What already works — reuse verbatim, do NOT re-derive:**
> - `ColourDiracQuarkChannel` (`quark_dirac`, F136) — a confined colour Dirac quark (F135 scalar Y-string + SU(3) gluon loop + EM `rho_em`). Three of them = one confined nucleon.
> - `NonRelElectronChannel` (`nr_electron`, F156) — the exactly-unitary split-step electron orbital; `ca_multigrid.schrodinger_step` / `schrodinger_relax` / `coarse_point_potential` are the live coarse-grid helpers.
> - `TwoGridAtomChannel` (`two_grid_atom`, F160) — the per-tick loop you are generalising: step fine proton → R_b-reduce its `rho_em` to a coarse point well → step the electron. **Charge under R_b is conserved exactly** (F159: 1.000000).
> - `ca_manybody.electron_cloud_hartree(Z)` / `nuclear_binding_Abody(Z,N)` / `aufbau_configuration(Z)` (F157) — the many-body **spectra/configurations** you will mirror live.
>
> **Build — three additions, in order:**
>
> **(1) Multi-nucleon fine patch → `+Z` coarse point charge.** Generalise the fine sector of `TwoGridAtomChannel` from one `uud` (the hardcoded `_FINE`) to **A = Z+N nucleons** (Z protons `uud`, N neutrons `udd`). Two honest design tiers — do the cheaper one first, state which you used:
>   - **Tier A (recommended first): coarse-grained nucleus.** The nucleus's *internal* binding is already established per-nucleon (F136) and as an A-body bound state (F157, α −30.1 MeV). On the fine patch, place A nucleon charge blobs in a bound configuration whose net `rho_em` integrates to **exactly +Z** (the N neutrons contribute 0 net), R_b-reduce that to a single `+Z` coarse point source. This is faithful to F159 (the electron cannot resolve nuclear structure — point-vs-resolved gap → 0 as a₀/r_nuc grows) and is the physically correct statement for the **electron** sector.
>   - **Tier B (stretch, if the sandbox allows): live A-body fine patch.** Run 3·A `quark_dirac` quarks grouped into A colour-singlet nucleons, with the model NN one-boson-exchange (σ F126 + ω F128 + π-tensor F104 + F113 quark-Pauli core) supplying the inter-nucleon binding, and confirm the **cluster RMS is bounded vs a free control** (the F135/F158 confinement signature, now for the whole nucleus). If 3·A quarks blow the sandbox, cap at He-4 (A=4, 12 quarks) and fall back to Tier A for Li/C — document the cap.
>
> **(2) Multi-electron coarse grid with Pauli filling (the real new engineering).** Generalise the coarse sector from one orbital to **Z orbitals** in the Aufbau configuration (`aufbau_configuration(Z)`; capacities 2,6,10,14). Each orbital is an `nr_electron`-style split-step packet stepped in the **self-consistent mean field** = nuclear `+Z` point well **+** the Hartree potential of all *other* electrons (mirror `ca_manybody._hartree_potential` but evaluate it live on the coarse grid each tick). Enforce **Pauli antisymmetry** by keeping the occupied orbitals mutually orthogonal — Gram–Schmidt the set each tick (or every few ticks) — this is the "helium needs the Pauli antisymmetriser" item F148/F157 flagged. Sign check: like-charge electron–electron repulsion + nuclear attraction, as in F156's `φ_em = −φ_Poisson(ρ)`.
>
> **(3) A stability readout + acceptance gate.** Extend `TwoGridReadout` (or add `atom_stability_readout`) to report, every N ticks, for the WHOLE atom: net charge `Z·(+1) + Z·(−1) → 0`; nucleus RMS (fine) bounded vs free control; each electron-shell RMS bounded (not collapsed sub-cell, not dispersing to box) + total cloud RMS **> nucleus RMS** (cloud surrounds nucleus); cloud centroid tracks nucleus centroid (separation ≪ cloud radius); the represented a₀/r_nuc decades (the b-carried scale ratio); all norms conserved to ~1e-13; loop-liveness (‖J_colour‖,‖A‖,‖J_em‖,‖α‖ > 0 if Tier B). **"Fully stable" is PASS iff** net charge ≡ 0 (machine precision), every norm conserved, every radius bounded over a long run (≥ a few hundred ticks), and the cloud-surrounds-nucleus + tracking geometry holds.
>
> **Scenarios + verification ladder.** Add CASIM scenario YAMLs (mirror `scenarios/unified_hydrogen_multigrid.yaml`): `stable_atom_helium.yaml`, `stable_atom_lithium.yaml`, `stable_atom_carbon.yaml`, each with a matched `_free.yaml` control (no nuclear well, no e–e field) so bounded-vs-ballistic is exhibited, not asserted. Verify on the ladder: **H (re-confirm F160 unchanged) → He (closed shell 1s², closed nucleus 2p2n — the clean "fully stable" target) → Li (open 2s¹) → C (open 2p²; Hund filling)**. Cross-check the live binding ordering against the F157 spectral numbers (He IP 24.0 eV, α −30.1 MeV) — they are the *spectra* the live run should be consistent with (structure, not absolute eV).
>
> **Deliverables:** the generalised channel (a new `multi_atom` / `element_atom` type alongside `two_grid_atom`, or a backward-compatible generalisation — keep `unified_hydrogen_multigrid.yaml` bit-unchanged), the readout/observer, the scenario YAMLs + controls, `tests/findings/test_F<n>_*.py` (target ≥ He passing all gates; Li/C as far as the sandbox reaches — be explicit about what's certified vs wired), the results JSON in `test-results/`, a finding `findings/F<n>-*.md`, exactness rows in `docs/status/exactness-inventory.md`, a one-paragraph `docs/status/changelog.md` entry (`yyyy-mm-dd - hh:mm` stamp), `python3 tools/regen_indexes.py`, and a memory pointer. **Be honest about scope:** if He is fully stable but Li/C only run partially (sandbox / SCF convergence), say exactly how far each got. If the live Hartree mean field doesn't converge for open shells, quantify the failure and record it (that is itself the finding's frontier statement, like F157's "heavy A overbinds — saturation open").
>
> **Watch the CLAUDE.md caveats:** real diagnostics only (`density_field` is already real — don't reduce chiral spinors yourself; check numpy/scipy on any new complex/chiral op before trusting it). Use Markdown math in files, unicode when replying to the user.

---

## Reference (exact paths, handles, numbers)

**Findings:** `F160-live-two-grid-atom` (the channel to generalise), `F159-u4-blockspin-multigrid-scale-separation` (R_b charge-faithful, point-vs-resolved gap→0), `F158-realspace-neutral-hydrogen-atom` (single-lattice neutral H), `F157-manybody-nuclei-and-electron-clouds` (A-body cluster + Hartree, the many-body content), `F156-realspace-em-bound-electron` (split-step orbital), `F148-modular-element-assembler` (`build_element`), `F136-colour-triplet-dirac-quark-confinement` + `F135-realspace-scalar-confinement` (the confined nucleon), `F133-blockspin-casim-engine-kernel` (R_b op), `F104`/`F126`/`F128`/`F113` (the NN one-boson-exchange, for Tier B).

**Modules / handles:**
- `src/casim/particles/channel.py` — `TwoGridAtomChannel` (type `two_grid_atom`, ~L1364), `NonRelElectronChannel` (`nr_electron`, ~L692), `ColourDiracQuarkChannel` (`quark_dirac`, ~L527), `TwoGridReadout` (~L1517). Channel `_FINE` hardcodes the single `uud` — that is what generalises.
- `ca-simulation/ca_multigrid.py` — `schrodinger_step`, `schrodinger_relax`, `coarse_point_potential`, `block_average_field`-based reduction, `_rms`.
- `ca-simulation/ca_manybody.py` — `electron_cloud_hartree(Z, alpha, m_e_MeV)`, `nuclear_binding_Abody(Z, N, anchor_Eb)`, `aufbau_configuration(Z)`, `_hartree_potential(rho, r, h)`, `_radial_eigen(...)`.
- `ca-simulation/ca_element.py` — `build_element(Z, N)`, `Nucleus`, `ElectronCloud`, `Element`.
- Scenario template: `scenarios/unified_hydrogen_multigrid.yaml` (b=30000, fine L=12, coarse L=32). RUN-GUIDE: `scenarios/RUN-GUIDE.md`.

**Targets (falsification-sharp where they exist):**
- Net charge ≡ 0 to machine precision (integer Z·(+1) + Z·(−1)); norms conserved ~1e-13 (kernels are exactly unitary).
- He-4: nucleus bound (F157 α −30.1 MeV, exp −28.3, 6%); electron cloud bound, IP 24.0 eV (CODATA 24.59); `stable = True` end-to-end (F157 already certifies the *spectral* He — the live run must reproduce the *structure*).
- Represented scale ratio: a₀/r_nuc decades carried by b (F160 reached ~4.8 decades for H; nuclei are slightly larger than the proton so the ratio shifts — report it, don't target a fixed number).
- Cloud RMS > nucleus RMS, cloud centroid tracks nucleus (F158: e-p separation ≲1.5 vs cloud ~4).

**Pitfalls / hazards (already quantified in the model):**
- **Open shells (Li/C) need Hund/Aufbau filling and a converging live Hartree field** — F157 notes heavy systems overbind / the SCF is the frontier. He (closed shell) is the clean PASS; treat Li/C as the stretch and be explicit.
- **Tier B (live A-body quarks) is compute-heavy** — 3·A `quark_dirac` quarks. Cap at He-4 (12 quarks) and use Tier A (coarse-grained `+Z` point nucleus) for the electron-sector certification of Li/C.
- **Pauli antisymmetry is the genuinely new piece** — without orthogonalising the occupied orbitals, two "electrons" collapse into the same 1s and helium is wrong. Gram–Schmidt the live orbital set.
- **The electron is non-relativistic** (v~αc) — keep the F156 Schrödinger split-step; do NOT use a relativistic Dirac electron in a vector Coulomb well (F156/F135: Klein tunnels / Zα→1 collapse). Relativistic fine structure stays in the F125 spectral solve.
- **Don't break F160** — keep `unified_hydrogen_multigrid.yaml` and the `two_grid_atom` H path bit-unchanged (regression-test it).
