# Kernel coverage audit — addendum to roadmap §P6

*Created 2026-07-29 - 21:20*

An independent re-run of the "which kernels has `casim` never wired up" question,
done before `docs/roadmaps/roadmap-unified-program.md` §P6 was read. The two
agree on the headline number, which is the useful part; this document records the
corroboration, four sectors the §P6 table omits, one misclassification, and the
reachability criterion §P1.4 is asked to settle.

**No physics changed. No kernel was moved or edited.**

---

## 1. Corroboration

Method: every `ca-simulation/ca_*.py` stem word-boundary-matched against the
concatenated text of every `src/casim/**/*.py`.

| | Count |
|---|---|
| Kernels in `ca-simulation/` | 106 |
| Never named anywhere in `src/casim/` | **67** |
| §P6's independently-derived figure | **~67** |

Two independent passes landing on the same 67 means the gap is real and the
criterion is at least stable. §P6's list names 43 explicitly plus the
`ca_lpt_*` family in prose (6 more); 28 of my 67 are not named there, and four
kernels §P6 names (`ca_higgs`, `ca_weak`, `ca_hypercharge`, `ca_blockspin`) *are*
referenced from `src/casim` — consistent with §P6's own note that they are
"importable via shims but no channel drives them." Reachable-by-import and
driven-by-a-channel are different properties, which is precisely the ambiguity
below.

**Unwired ≠ untested.** 66 of the 67 have at least one test in `tests/`. This is
a packaging and coverage gap, not a correctness gap. The one exception is
recorded in §4.

---

## 2. Four sectors the §P6 table omits

§P6 tables six sectors (gravity/astro, QED precision, LPT, QCD running,
electroweak/Higgs, quantum info). These kernels fall outside all six:

### 2.1 Matter binding / bound states — 6 kernels, no sector row

`ca_atom` (F125 hydrogen + positronium, Dirac–Coulomb), `ca_element` (F148
modular element assembler), `ca_baryon_dynamics` (P2, the real-time three-body
proton), `ca_baryon_blockspin` (F140 coarse-grained baryon), `ca_nuclear_core`,
`ca_photon_bs` (F169, the paired photon's interacting two-body wavefunction —
the build F69/F74/F168 explicitly flagged as outstanding).

This is the whole `docs/roadmaps/roadmap-matter-binding.md` arc. It is *partly*
represented in `casim` by the particle layer's `two_grid_atom` / `element_atom`
channels, which is why it may have looked covered — but those are the later F195
block-spin construction, not these kernels. Whether F148's `ca_element` is
superseded by F195's `element_atom` or complementary to it is a **question this
audit cannot answer from the code** and should be settled by whoever owns F195.

### 2.2 Dynamical processes — 1 kernel

`ca_emission` — photon emission from atoms (rate + spectrum from the model's own
m_e and α). Turns static levels into observables; nothing drives it.

### 2.3 Applied / device physics — 2 kernels

`ca_superconductivity` (electrical superconductivity as the electric S-dual of
F86) and `ca_slowlight` (slow light / EIT as a direct test of the F26
rotation-rate picture — CLAUDE.md decision 2). Both are external-data
confrontations, which makes them high-value for the falsification suite.

### 2.4 Kernels belonging to sectors §P6 tables, but not named

- *Gravity/astro:* `ca_rotation` (Hartle slow-rotation frame dragging + moment
  of inertia, on the F181 two-function interior).
- *QCD running:* `ca_ir_coupling` (F152's IR face), `ca_qstar_logmoment`,
  `ca_eg_sextic_coupling` (the λ₆ saturated-condensate solve), `ca_induced_stiffness`.
- *QED precision:* `ca_ir_bremsstrahlung` (F259, the Bloch–Nordsieck
  cancellation), `ca_propagator`, `ca_vacuum_energy`, `ca_casimir_materials`.

---

## 3. One misclassification: `ca_link_hamiltonian` is not compute-once

§P6 files it under "Lattice perturbation theory — Compute-once". Its public API
is `evolve_krylov`, `evolve_dense`, `energy_expect`, `plaquette_cos_expect` —
**real-time Hamiltonian evolution**, and F110's stated purpose was to promote the
confinement sector *out of* frozen-link Euclidean measurement into real time.

This matters for how it gets wrapped. It is the single most genuinely tickable
unwired kernel in the tree, and the engine has no real-time gauge channel at all:
`gauge_mc` (Tier-3) is Euclidean Monte Carlo on frozen links. A
`link_hamiltonian` channel would be the first real-time confinement channel, not
another compute-once wrapper.

Scanning all 67 for step-shaped entry points (`*_step`, `evolve*`, `advance*`)
turns up only four candidates for genuine channels:

| Kernel | Entry points | Verdict |
|--------|--------------|---------|
| `ca_link_hamiltonian` | `evolve_krylov`, `evolve_dense` | **Wrap as a channel** — see above |
| `ca_cooling` | `wilson_flow_step_euler_2d`, `wilson_flow_step_rk3_*` | Better as a *filter/observer* on the gluon channel than a channel; also already indirectly reachable (§5) |
| `ca_inspiral` | `evolve_chirp` | Compute-once in practice (post-Newtonian phasing, not a lattice tick) |
| `ca_unified` | `unified_step` | **Do not wrap** — see §4 |

Everything else in the 67 is a solve, and the existing `spectral_matter`
compute-once pattern (`njl_meson` / `njl_nucleon` / `string_tension`) is the
right shape for it, exactly as §P6 says.

---

## 4. Two items for tombstoning rather than wrapping

**`ca_unified.py` implements a deprecated proposition.** Its docstring cites
`ca-unified-proposition.md`, which now lives in `deprecated/`. It couples a
Mexican-hat Higgs Φ to the Dirac fermion by Yukawa — and CLAUDE.md decision 3
puts hypercharge on U(x) precisely to avoid needing a Higgs field. So this is a
kernel superseded **by a recorded design decision**, not merely unwired. It has
6 tests still running unmarked in the battery, which is the exact failure mode
§P6 flags for the five superseded families ("indistinguishable from live tests —
no marker, no skip, no tombstone"). Recommend adding it as a sixth entry there.

**`ca_casimir_materials.py` has zero tests anywhere in the tree** — the only
kernel of the 106 with none. It also has no `main()`, so it is not reachable
from the standalone-script half of the suite either. Either it is dead code from
the `ca_casimir` session or it is untested physics; both warrant a decision.

---

## 5. The reachability criterion (input to §P1.4)

§P6 notes the count "moves by a few depending on whether re-export shims in
`casim/fields/*` count as reachability" and asks P1.4 to settle it. A concrete
case that decides the question:

`ca_cooling` is not named anywhere in `src/casim` — but
`ca-simulation/forks/lgt_fork_A_mc.py` imports it, and `src/casim` *does*
reference `lgt_fork_A_mc` (the `gauge_mc` channel). So `ca_cooling` executes
during a `casim run` while being invisible to a direct-reference scan.

Three candidate criteria, which give three different numbers:

| Criterion | Meaning | Count unreachable |
|---|---|---|
| Direct textual reference from `src/casim` | what this audit and §P6 measured | 67 |
| Transitive import closure from any channel | what actually executes | 66 (`ca_cooling` moves) |
| **Driven by a registered channel or compute-once wrapper** | what P6's acceptance gate wants | ≥ 67 — the four §P6 names (`ca_higgs`, `ca_weak`, `ca_hypercharge`, `ca_blockspin`) rejoin the unreachable set |

The third is the criterion that matches §P6's acceptance gate, and it is the
*least* flattering of the three. Recommend P1.4's manifest measure that one, and
report the transitive closure separately as a coverage-vs-liveness distinction.

---

## 6. Suggested sequencing within §P6

Ordered by external-confrontation value per unit of work, since every one of
these kernels already passes its own tests and the work is wrapping:

1. **`ca_link_hamiltonian` as a real-time gauge channel** — the only structural
   addition on the list; gives the engine real-time confinement.
2. **Gravity / astrophysics** — §P6 already calls it the largest gap and the
   sector with the most external-data confrontations. `casim.gravity` currently
   re-exports only `ca_gravity` / `poisson_open` / `ca_curved` / `ca_emqg`, so
   the entire F178/F181 GR battery is invisible to the program.
3. **Applied physics (`ca_slowlight`, `ca_superconductivity`)** — small, and
   both confront measured data directly.
4. **QED precision** — 15 kernels, near-identical compute-once shape, so it
   mechanises well once one is done.
5. **Matter binding** — needs the F148-vs-F195 supersession question answered
   first (§2.1).
6. **LPT family** — lowest value. These are Feynman-rule derivation machinery;
   they belong in tests, and wrapping them into the engine may be the wrong
   move regardless of the acceptance gate's wording.

---

*Cross-references: `docs/roadmaps/roadmap-unified-program.md` §P1.4, §P6;
`docs/audits/project-audit-inputs-dynamism-2026-06-06.md`;
`deprecated/ca-unified-proposition.md`; `deprecated/README.md`.*
