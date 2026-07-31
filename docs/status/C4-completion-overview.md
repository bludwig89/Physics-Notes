# C4 completion overview — sector migration: gauge fields

*2026-07-30 - 14:56. Phase C4 of `docs/roadmaps/roadmap-casim-consolidation.md`. Entry state: C3 complete, gauge sector claimed in the manifest. Verified with the vendored scipy/pytest env (`source .vendor/activate.sh`), so — unlike C3's first pass — the full pytest gate and the scipy kernels were exercised here.*

## Sector claim

Before any file moved, the gauge sector was claimed in the migration manifest under a new top-level `claims:` block (`claims.gauge = {session, phase: C4, timestamp}`), and `tools/gen_migration_manifest.py` was extended to preserve `claims` across regeneration (alongside `migrated`/`drift`/`dead_symbols`). This is the roadmap's concurrency guard made concrete — C5/C6 sessions can see the sector is taken.

## What landed

**All 31 `sector: gauge` records migrated into `engine/gauge/`** — γ/photon, W/Z/hypercharge, gluon/SU(3)/colour, the lattice-PT `lpt_*` family, confinement, cooling, the link Hamiltonian, and the two forks' consumers. Each is D10 (pre-clean original backed up under `deprecated/code/` with a header, cleaned copy at the new path, `DeprecationWarning` shim at the `ca-simulation/` source, manifest stamped). Migrations were done overwrite-only and **byte-faithful to `migrate_module.py`'s own SHIM/BACKUP templates**, because the sandbox mount blocks `unlink` (so the tool's abort/rollback would orphan files); every target is byte-identical to its original, which makes drift impossible by construction for the move itself.

**The two ledger cleanups were recorded structurally, not re-cut — because the code-level cleanup was already done at F69/F91.** This is the roadmap's own "migrate with the banner" pattern (P0.4's lesson: don't re-strip live algebra):

- **S1 — the σ-bilinear photon (`ca_maxwell` → `gauge/bilinear.py`).** The ledger says *only the photon attribution died; the σ-bilinear FIELD CONSTRUCTION survives for W/Z/gluon.* Verified: **no live channel attributes the σ-bilinear as the photon** (`photon_pair`→`PhotonPairChannel`, `charge_photon`→`ChargePhotonChannel`, `photon_sourced`→`PhotonSourcedChannel`; none is `ca_maxwell`), the module already carries the F65–F69 banner ("the physical photon is now the paired-spinor photon of `ca_photon_pair`… Do NOT use these helpers as the U(1) photon"), and its only consumers are W/Z/gluon code (`colour_dielectric`, `gluon`, two forks). So C4 records the supersession by **naming the target `bilinear.py`** (the role it now serves) and keeping the banner; the canonical photon is `ca_photon_pair` → `gauge/photon.py`. The pre-clean σ-bilinear construction is preserved in `deprecated/code/ca_maxwell.py`. Acceptance "σ-bilinear photon channel gone from live code, present in deprecated/code" is satisfied: it was gone at F69, and the original is in the backup.
- **S2 — the chiral→even gluon (`ca_gluon` → `gauge/gluon.py`).** Nothing stripped: `gluon_rotation_step_spectral_bcc` (even, canonical) and `gluon_rotation_step_spectral_bcc_chiral` both survive, the chiral one already labelled "RETIRED (F91)… Kept ONLY for historical comparison… NOT the gluon propagator." Byte-identical move.

**No P3.1 BCC physics port** — C4 moves and cleans files; the cubic→BCC physics port is the other roadmap's business and needs its derivation spike first.

**Import rewiring, including the string-import shim layer.** Every `src/casim` import statement of a migrated module (C1 `ca_fft` + C3 lattice/core + C4 gauge) was rewired to its engine path. The `casim.fields.*` re-export shims import kernels by **string** via `importlib.import_module` — a pattern the import-line rewriter and the C3.4 regex checker do not see — so `fields/em.py`, `fields/strong.py`, `fields/electroweak.py` were given an explicit old-name→engine-path `_PATHS` map (migrated kernels resolve to `casim.engine.gauge.*`; the C6 `ca_dual_gl_backreaction` stays on its bare name until it migrates). After this, every "…moved…" `DeprecationWarning` at import originates from a not-yet-migrated `ca-simulation` kernel (C5/C6) importing a migrated sibling — the intended transitional state, cleared at C9.

## Verification (full mode, vendored scipy + pytest)

- **`make gate`** — every check green **except the one pre-existing failure `test_backend.py::test_ca_fft_alias_delegates_to_the_active_library`**, which asserts the `ca_fft` backend equals `np.fft` bit-for-bit and fails only because the vendored env makes **scipy** the active FFT library (scipy≠numpy at round-off). It touches no C4 module, C2 already flagged it, and it belongs to the numerics-seam owner. `pytest tests/casim`: **112 passed, 1 pre-existing fail.**
- **Drift: C4 introduces zero.** Every gauge target is byte-identical to its original; the only result-JSON drift in the tree is the two pre-existing, documented files (`F233`, `wmu_phase3`). Result files rewritten by verification runs were restored to HEAD.
- **Gauge sector works end-to-end under scipy** — F91 pairing classification, FG7 gluon dynamics, F265 BCC gauge geometry, and **F110 link-Hamiltonian real-time (the scipy `link_hamiltonian` confinement path, 7/7)** all pass as scripts.
- **`casim list-channels` byte-identical**; module registry **58/58 covered** (31 gauge + 27 from C3); C3.4 shim-import checker clean; migration manifest current with the claim and all 31 stamps preserved.

## For Ben / handoff

- **C5 (particles) and C6 (interactions) remain.** Each must claim its sector in `claims:` before starting. When C5 migrates `ca_dirac`/`ca_dirac_bcc`/`ca_baryon`/`ca_higgs`, it must also update `fields/matter.py`'s importlib list (same `_PATHS` pattern used here for `fields/em|strong|electroweak.py`); `fields/entanglement.py` likewise when `ca_entanglement` moves at C6. The C3.4 checker is import-statement-based and does **not** catch the `importlib` string pattern — noted so it isn't missed.
- The `test_backend` FFT-backend-strictness failure and the pre-existing `F233`/`wmu_phase3` drift are still open for you, unchanged by C4.
