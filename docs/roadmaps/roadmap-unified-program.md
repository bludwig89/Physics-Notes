# Roadmap — CASIM as a Single Comprehensive Modeling Program

*Created 2026-07-29 - 19:42. Supersedes the completed `deprecated/roadmap-standalone-program.md` (Phases A–G, which delivered the package layer). This roadmap covers the next arc: from "a package that wraps kernels" to "one universe, one lattice, one clock."*

---

## 1. Purpose and end state

**End state (decided 2026-07-29):** a single simulation in which gauge, matter, and gravity sectors coexist on **one lattice** with **one clock**, configured declaratively and observable live. Not a launcher for per-sector scripts.

**Design decisions taken at the start of this roadmap:**

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | **BCC is the canonical universe topology.** Cubic kernels are demoted to reference implementations retained for regression. | Canon already lives on BCC: the $O_h$ second shell and $E_g$ weight $\delta^*=2/9$ (F175/F253/F255), the even-law gluon (F91), the true BZ being FCC with exactly two Weyl points per branch (F264), and all matter channels. Keeping the exact photon on cubic permanently splits the universe. |
| D2 | **Flat `ca-simulation/ca_*.py` kernels remain the single source of truth.** `casim` deepens its wrapping rather than absorbing them. | Protects 272 finding tests and every audited exactness claim. The cost is a permanent two-layer structure; the mitigation is P0's provenance layer, which makes the seam auditable. |
| D3 | **Two interfaces, co-equal: declarative scenarios + CLI, and an interactive GUI.** | Scenarios carry reproducibility and agent-driven work; the GUI carries intuition. Both must read the same scenario schema. |
| D4 | **Compute target: Apple Silicon now, rented/cloud GPU later.** | Forces a genuinely device-agnostic backend protocol with at least two live implementations, rather than a CUDA-shaped seam. |
| D5 | **Foundations first.** Provenance, test consolidation, and performance (P0–P2) precede the one-lattice work (P3). | You cannot tell whether a coupled universe is *right* without a conservation gate and single-sourced constants; and P3's validation runs need throughput that does not exist yet. |

---

## 2. Where we actually are

Measured 2026-07-29 by direct audit of the tree, not from documentation.

**Assets.** 106 `ca_*.py` kernels (40.6k LOC) + 47 forks; `casim` package (8.3k LOC) with a working engine, 29 registered channel types, 15 observers, YAML scenarios (46 shipped), checkpoint/resume with RNG round-trip, a real vispy+Qt live GUI (948 LOC), and a scaled test suite runner. 77.7k LOC of tests. 418 result artifacts. This is a large, working system — the problems below are integration problems, not absence of substance.

**The six structural blockers.**

| # | Blocker | Evidence |
|---|---------|----------|
| B1 | **Topology partition.** Cubic-only (6): `photon_pair`, `w_chiral`, `z_even`, `charge_photon`, `gauge_mc`, `refraction_2d`. BCC-only (10): `weyl_bcc`, `quark_dirac`, `particle`, `composite`, `fermion_doublet`, `beta_decay`, `colour_bag`, `gluon_bcc`, `gluon_sourced`, `w_sourced`. (13 more are topology-agnostic, including `gravity_dielectric`, `nr_electron`, `element_atom`, and the spectral-matter trio.) Engine hard-rejects mixing. | `engine/simulation.py:69-74`, enforced at `:122`; workaround shipped as paired scenarios (`photon_beam_all_fields.yaml` + `bcc_fields_companion.yaml`) |
| B2 | **No clock.** One tick = one `step()` per channel in YAML order (Gauss–Seidel). Spectral kernels have $\Delta t \equiv 1$ baked into the exponent and cannot be sub-cycled; other channels carry their own free `dt` — 0.1 (`charge_photon`, `photon_sourced`), 0.2 (`nr_electron`), 1.0 (`gravity_dielectric`, `gluon_sourced`), 0.5 (the `two_grid_atom`/`element_atom` sub-lattices). `step()` takes no `dt`. | `simulation.py:174-183`, `:179-182`; `coupled.py:183`, `particles/channel.py:726,972,1388,1663,1674`, `channels.py:326` |
| B3 | **Ordering is load-bearing and unchecked.** "Register this BEFORE the fermion channel" is a docstring, not a constraint. Reordering YAML silently changes physics. Coupling is by untyped string key; a typo yields `None` and silently disables the loop. | `coupled.py:70-73,106`; silent-`None` sites `particles/channel.py:233-236,976-980,1034-1036` |
| B4 | **No total-energy observable.** Six incompatible energy conventions (Σ\|ψ\|², Σ(E²+B²) *without* the ½ that `coupled.field_energy` uses, Σ(K−1), `phi_field_energy`, mean plaquette, MeV). `NormConservation` reports per-channel drift only. **A coupled run currently has no conservation check that could falsify it.** | `channels.py:72` vs `coupled.py:35-37`; `observers.py:93-105`; `tier3.py:68-70` |
| B5 | **Gravity is half-connected.** $T^{00}$ is rest-leg only (a fast packet does not gravitate by its energy), scalar $\Phi$ only, no $T^{0i}$/$T^{ij}$. Back-reaction exists solely for massive lepton singlets; quarks never call `_grav_sqrtA`; **no gauge channel reads $K$, so light does not bend in the production engine.** Latent bug: `T00_dirac_rest` does not sum the leading colour axis, so a `quark_dirac` in `sources:` silently promotes gravity state to rank-4. | `ca_gravity.py:95-105` ("kinetic term … not yet in the production source"); `particles/channel.py:473,604-651`; `channels.py:255-262,289-316,328-331` |
| B6 | **The performance seam is decorative.** Zero physics modules import `casim.lattice.backend` — the only importers are two tests and its own self-registration. 18 non-test modules use `ca_fft` (a library seam, not a device seam); **38 modules call `np.fft.*` directly, across 266 call sites.** `pyfftw` is preferred by `ca_fft` but is not a declared dependency, so every run silently falls back to scipy. Swapping in a GPU backend today would change nothing. | `backend.py:77-104`; importers `tests/casim/test_backend.py:11`, `test_F134_phase4_completion.py:36`, `src/casim/lattice/chiral_core.py:168`; `chiral_core.py:31` bypasses its own seam; `pyproject.toml:12-20` |

**Two cross-cutting hazards.**

*Provenance.* $c_\text{lat}=1/\sqrt3$ has **~74 independent literal re-definitions** in two spellings — 67 of the `1/np.sqrt(3)` family and 7 hardcoded `0.5773502691896258`. `f_π` has four values in circulation (92.07 anchor / 92.4 target / 92.28 Γ-convention). `M(0)` lives in three unit systems with the lattice↔MeV bridge stated only in a comment. Most striking: **$\delta^*=2/9$ has no canonical owner** — it is redefined in `derive_generator_norm_from_F118.py:117`, `derive_lambda6_sextic.py:125`, and again in `tests/findings/test_F234_Wvc_triple_closed.py:35`, and $\lambda_6$ is nowhere a named module constant at all (it is recomputed in each derive script and compared against a literal `0.243` target inside a test). These are the constants the current lepton canon rests on. And `derive_generator_norm_from_F118.py:143-177` is live code that still asserts $\lambda_6$ is *assumed* and E1 is *open*, which the 2026-07-16 F253/F255/F256 decision reversed.

*Enforcement.* **There is no CI** — no `.github/workflows`, no Makefile, no tox. `pyproject.toml` sets `testpaths = ["tests/casim"]`, so bare `pytest` runs **6 files out of 340**. Of 272 finding tests, only 98 contain any `assert`; the rest print `PASS`/`FAIL` tokens that `src/casim/suite/runner.py:395-430` scrapes from stdout, and exit-0-with-no-token scores as `RAN` — neither pass nor fail. **At most ~36% of the findings suite can fail.** All 272 do real physics at *module import time*, so `pytest --collect-only` executes the suite. Tests for all five superseded physics families (σ-bilinear photon, F50/F52/F62 rest-mass gravity, F114 horizon-free BH, chiral gluon, F179/CN3) are still in the battery and are **indistinguishable from live tests** — no marker, no skip, no tombstone.

---

## 3. Target architecture

```
                    ┌──────────────────────────────────────────┐
                    │  Scenario v2 (YAML)  —  one universe      │
                    │  units · lattice · matter · events        │
                    │  couplings(typed) · expect · view · out   │
                    └───────────────┬──────────────────────────┘
                                    │  strict schema + cross-ref validation
      ┌─────────────────────────────┴─────────────────────────────┐
      │                    casim.engine — one clock                │
      │  dependency graph (topo-sorted, not YAML order)             │
      │  dt reconciliation + sub-cycling                            │
      │  typed exchange bus:  provides/consumes  {J_em, J_col, T^μν}│
      │  global conserved quantity + gate                           │
      └───┬──────────────────┬───────────────────┬─────────────────┘
          │                  │                   │
   ┌──────┴─────┐    ┌───────┴──────┐    ┌───────┴───────┐
   │ constants  │    │  channels    │    │  backend      │
   │ registry   │    │  (BCC-native)│    │  numpy·pyfftw │
   │ + provenance│   │              │    │  ·mlx ·cupy   │
   └──────┬─────┘    └───────┬──────┘    └───────┬───────┘
          │                  │                   │
          └──────────────────┴───────────────────┘
                             │  thin, audited wrapping (D2)
                  ┌──────────┴───────────┐
                  │  ca-simulation/      │  ← single source of truth
                  │  106 kernels + forks │
                  └──────────────────────┘
```

Two things this sketch asserts that are not true today: the exchange bus is **typed and validated at build time** (B3), and the engine owns a **clock** rather than a tick counter (B2).

---

## 4. Phases

Each phase lists deliverables, concrete file-level actions, and an **acceptance gate** — a check that must pass before the phase is called done.

### P0 — Ground truth (provenance + tombstones + a gate that exists)

*Small, unglamorous, and everything else depends on it. Nothing here touches physics.*

**P0.1 — Constants registry.** New `src/casim/constants/` — one module per sector plus `registry.py`. Each entry is a record, not a float:

```python
Constant(
    symbol="delta_star", value=Fraction(2, 9), units="rad",
    exactness="exact",              # exact | machine | quantitative | bracketed
    provenance=("F175", "F253", "F255"),
    derivation="dim(E_g)/dim(T_1u⊗T_1u), exact O_h",
    supersedes=("F179-CN3",),
)
```

Seed it with the twelve audited constants: $a/\ell_P$ (computed as $\sqrt{8\pi}\,3^{1/4}$, **not** the truncated `6.5978`), `G_LATTICE` $=1/(72\pi)$, $c_\text{lat}=1/\sqrt3$, $\delta^*=2/9$, $\lambda_6$, $W=6\lambda_6$, $\alpha_\text{eff}^*$ (as the bracket `[0.376, 0.411]`, not a midpoint), $\Lambda^{(3)}$, $M(0)$, $f_\pi$, $\sin^2\theta_W$ (both faces — F45 UV $1/4$ and F49 on-shell $2/9$, with the F231 reconciliation attached), $\cos 3\delta^*$ (flagging that `0.785887` from $\delta^*$ and `0.785874` from F93 O7 data are *different objects* separated by the F256 $1.7\times10^{-5}$ near-coincidence).

Per D2 the kernels keep their literals. The registry earns its keep through **P0.2**.

**P0.2 — Consistency test (`tests/casim/test_constants_consistency.py`).** AST-walks `ca-simulation/` and `src/`, finds numeric literals matching a registry value within tolerance, and asserts agreement; flags known-divergent sites (the four `f_π` values, the two `cos3δ` values) against an explicit allowlist with a reason string. This converts ~74 scattered `c_lat` definitions from an invisible hazard into a single failing assertion the day one of them drifts.

**P0.3 — Supersession ledger.** `docs/theory/supersessions.yaml` — machine-readable, one record per supersession: `{superseded: [F50, F52, F62], by: F64, scope: "rest-mass-sourced metric", date: 2026-..., tests: [...]}`. Extract from the 9 prose bullets in `key-decisions.md` (the F253/F255/F256 entry alone is a single ~2,600-character line). `key-decisions.md` stays as the human narrative; the YAML becomes the machine face. Extend `tools/regen_indexes.py` to consume it and annotate `findings-index.md`.

**P0.4 — Tombstone superseded tests.** Register a `superseded` marker in `pyproject.toml`. Apply to the ~10 identified files, each carrying the ledger reason. `casim test` reports them in a separate section and excludes them from pass/fail. Also fix the live contradiction: `derive_generator_norm_from_F118.py:143-177` gets updated or tombstoned against the F253 decision.

**P0.5 — A gate that exists.** `.github/workflows/gate.yml` (or `make gate` if you'd rather not host it) running: the 6 `tests/casim` files, the new constants-consistency test, and a scenario smoke tier. Under two minutes. This is the first automated enforcement in the repo's history.

> **Acceptance gate P0:** the gate runs green on a clean checkout; every constant in the registry has a recorded finding; `casim test` visibly separates live from superseded; changing `G_LATTICE` in `ca_gravity.py` fails the gate.

---

### P1 — Test and results consolidation

*Turning 340 files that mostly cannot fail into a suite that can.*

**P1.1 — Three tiers, honestly labelled.**

| Tier | Contents | Invocation | Runtime target |
|------|----------|-----------|----------------|
| `gate` | asserting, exact/machine-precision, no I/O | `pytest` default | < 2 min |
| `battery` | full findings + priority + scenarios | `casim test` | hours, chunked |
| `archive` | superseded + exploratory | `casim test --archive` | on demand |

Redefine `pyproject.toml` `testpaths` to the `gate` set. Add `tests/runners` (45 files, currently covered by nothing) to `battery` explicitly rather than leaving it in an opt-in group nobody selects.

**P1.2 — Close the assertion deficit.** 173 findings files cannot fail. Two mechanics, applied by triage:

- *Baseline-diff harness.* Most of these already compute and dump a result dict. Add `tests/baselines/F###.json` and a shared `assert_matches_baseline(result, tol_class)` helper. A test that returns numbers now fails when the numbers move. This is mechanical and covers the majority.
- *Real assertions* for the ~30 tests whose claim is a clean algebraic identity.

Also fix the `PytestReturnNotNoneWarning` class (e.g. `test_F107_*` defines `test_`-named functions that return dicts — collected, never able to fail, and an error under pytest 8 defaults).

**P1.3 — Kill import-time side effects.** All 272 findings tests execute physics on import. Move module-level work into `main()` / fixtures. Do this file-by-file behind P1.2's baselines so a botched move is caught. This alone makes `--collect-only`, `-k` filtering, and parallel `pytest -n` usable — which is the precondition for the gate ever being fast.

**P1.4 — Results manifest.** Generate `test-results/manifest.json`: bidirectional result ↔ test ↔ finding, with mtime, the git SHA that produced it, and the constants-registry snapshot in force. Replaces `tests-index.md`'s prefix heuristic (`tools/regen_indexes.py:155-157`), which caps at 2 matches, leaves 104 of its 339 rows with an empty Results cell, and cannot see orphaned JSONs at all. Normalise the six naming conventions going forward; leave existing files, map them in the manifest.

**P1.5 — One exactness inventory.** `docs/status/exactness-inventory.md` is 1,118 hand-maintained lines whose tally header is stamped seven weeks staler than the newest findings. Generate the Tier 1/2/3 tables from the gate + baselines; keep hand-written prose for the appendices. Retire the disconnected `test-results/casim-exactness-inventory.md` split.

> **Acceptance gate P1:** `pytest` green in < 2 min; every findings test either asserts, diffs a baseline, or is tombstoned — zero in the "RAN" limbo; the manifest resolves every result file to an owning test; deliberately perturbing a physics constant fails a countable, named set of tests.

---

### P2 — Performance

*Ordered by return on effort. Steps 1–3 need no new hardware.*

**P2.1 — The free win.** Add `pyfftw` to `pyproject.toml`. `ca_fft.py:57-63` already prefers it and `set_workers` already exists (`ca_fft.py:92`); it is simply never installed, so every run today silently uses single-threaded scipy. Expect a straight multi-core multiple on the FFT-bound channels, which are the bulk of the propagating sector: `photon_pair`, `weyl_bcc`, `w_chiral`, `z_even`, `gluon_bcc`, `refraction_2d`.

**P2.2 — Make the seam real.** Migrate the direct `np.fft.*` work — 266 call sites across 38 modules — to `casim.lattice.backend`, highest value first:

| Priority | Site | Why |
|---|---|---|
| 1 | `ca-simulation/poisson_open.py:124-127` | 8× zero-padded grid, single-threaded, used by every gravity scenario |
| 2 | `ca-simulation/ca_multigrid.py:149,186,199` | ~3000 unthreaded transforms per `solve_hydrogen`; `_k2` rebuilt every call |
| 3 | `ca-simulation/ca_colour_dielectric.py` (23 sites) | heaviest single module |
| 4 | `ca-simulation/ca_gluon.py` (10 sites) | the 8-component octet, the heaviest per-tick state |

Separately — and not an `np.fft` site — `src/casim/lattice/chiral_core.py:31` imports `ca_fft` directly, bypassing the very seam it registers itself with. Fix it in the same pass.

Note this is a D2-compatible change: it swaps a function reference inside the kernels, not their physics, and P1's baselines catch any drift bit-for-bit.

**P2.3 — Allocation and caching.** Preallocated FFT scratch + in-place transforms (pyfftw supports this natively; directly attacks the `_FFT_OVERHEAD = 3.0` fudge at `src/casim/suite/tiers.py:40`). Extend the k-grid/dispersion caching that `ca_bcc` (`_weyl_cache`) and `ca_wmu` (`_disp_cache`) already do to modules that lack it — `chiral_core.weyl_step` rebuilds `make_kgrid_3d` *and* the full unitary on every call (`chiral_core.py:84-86`), a straight regression against the kernel it claims to match bit-for-bit. Use `rfftn`/`irfftn` for real-valued E and B fields, which currently pay full complex transforms.

**P2.4 — Two accelerated backends (D4).** The backend protocol is seven methods — six FFT entry points (`backend.py:97-102`) plus `chiral_transform` (`backend.py:104`) — and `_NumpyFftBackend` already proves the swap is regression-testable.

- *Now (Apple Silicon):* an MLX or JAX-metal backend. Generalise the existing pattern rather than reinventing it — `ca_wmu.py:754-802` already has a JAX path covering two functions, unreachable only because JAX is not a declared dependency.
- *Later (cloud):* a CuPy backend. Same protocol, no physics change.

Every backend must pass the `_NumpyFftBackend` regression — identical to `ca_fft` at the round-off floor.

**P2.5 — Gauge MC restructure.** `gauge_mc` is the worst scenario in the suite — `scenarios/RUN-GUIDE.md:31-46` records 6.0 s at L=6/40 sweeps against 0.8 s for `photon_pair` at L=16/40 (recorded smoke artifacts show 4.5–4.6 s at L=6 under the `tiers.py:93-96` override) — and it is not FFT-bound, so P2.2–P2.4 do nothing for it. Four changes: reuse `staple_field` across parities instead of recomputing per direction *and* parity (`ca-simulation/forks/lgt_fork_A_mc.py:268-274`); replace `np.einsum('...ij,...jk->...ik')` with `np.matmul`, which dispatches batched 3×3 to BLAS `zgemm` and einsum does not (`ca-simulation/ca_cooling.py:52`); eliminate the ~18 full-array `np.roll` copies per direction via halo buffers; replace the per-site batched `np.linalg.svd` reunitarization with Gram–Schmidt/Cayley at equal accuracy, and make `reunit_every` a cadence rather than a bool. Target: production ceiling from L=12 to L≈16–20.

**P2.6 — Long-run operations.** Today's checkpoint is a synchronous, uncompressed, non-atomic `np.savez` inside the tick loop (`simulation.py:306`) with no rotation — the likeliest way a multi-day run loses everything. Make it atomic (`.tmp` + rename), compressed, rotating, and asynchronous. Add suite-level auto-resume (currently a docstring at `src/casim/suite/runner.py:22` with no implementation; a 1000× run that dies at item 9 of 14 restarts from item 1, and the timestamped `out_dir` means it cannot even find its own checkpoints). Add a **wall-time model** to `src/casim/suite/tiers.py` alongside `mem_bytes` — `--list` predicts memory but not duration, so no one can size a multi-day run before launching it. Fix `simulation.py:324-332`, which drops `blockspin_schedule` on resume, silently skipping scheduled $R_b$ events.

**Precision:** hold everything at complex128. `float32` eps ($1.2\times10^{-7}$) is five orders above the `machine_precision` marker's $10^{-12}$ gate — that gate is not a tunable, it is the product. A `--precision` flag scoped to *non*-`machine_precision` scenarios (viz, density fields, statistically-averaged MC observables) is defensible later; a global one is not.

> **Acceptance gate P2:** ≥ 5× wall-clock on the reference scenario set with **bit-identical** results against P1 baselines; a second backend passes the seam regression; a 24-hour run survives a kill -9 and resumes to the same trajectory.

---

### P3 — One lattice, one clock

*The end state. Everything above exists to make this checkable.*

**P3.1 — BCC unification (D1).** The largest single piece of work in this roadmap, and it is physics, not porting.

1. *Spike first.* Derive the paired-spinor photon's even-law rotation on the BCC dispersion. F250 already establishes the all-$k$ gauge pole and the $k/2$ doubler folding; F264 establishes the true BZ is FCC with exactly two Weyl points per branch. The question the spike answers: does the exact even-law structure survive on BCC with the same exactness class, or does it degrade to machine precision?
2. Port `photon_pair`, then `w_chiral` and `z_even`, then `charge_photon`.
3. `gauge_mc` is a separate problem — it has no time coordinate and its `L⁴` links are a different object. Treat it as a compute-once channel (the `spectral_matter` pattern), not a co-evolving one.
4. Cubic kernels move to `casim/reference/`, retained and still tested as the regression target the BCC versions must reproduce in the continuum limit.

Each port lands with a paired test asserting the BCC version reproduces the cubic one where they overlap. **If the spike shows exactness does not survive, stop and re-open D1** — a degraded photon is a worse outcome than a split lattice.

**P3.2 — A real clock.** Engine owns physical time. Each channel declares `dt_max` (stability) and `dt_exact` (`1` for the spectral rotations whose $\Delta t$ is in the exponent, `None` for CFL-limited steppers). The engine picks a global $\Delta t$ and **sub-cycles** the channels that need it, rather than each channel privately meaning something different by "a tick." Pull the ad-hoc internal sub-cycling out of channels and into the engine: `refraction_2d`'s `n_sub=4` (`src/casim/engine/tier3.py:125`), `element_atom`'s `hartree_every`/`gs_every`, `two_grid_atom`'s fine-then-coarse.

**P3.3 — Typed exchange bus.** Channels declare `provides` and `consumes` (`J_em`, `J_colour`, `T00`, `A_mu`, `sqrt_A`, …). The engine builds a dependency graph and **topologically sorts** it, replacing YAML-order Gauss–Seidel. Unsatisfied `consumes` is a build-time error, not a silent `None`. Cycles are detected and resolved by an explicit declared scheme (leapfrog / predictor-corrector), not by whichever line came first in the file.

**P3.4 — Unified stress-energy.** One `T_munu(state) -> ndarray` protocol on `Channel`. Fix the colour-axis broadcast bug in `T00_dirac_rest` (`ca_gravity.py:95-105`) — unlike `T00_field_energy` two functions below it, it does not sum a leading axis, so a `quark_dirac` in `sources:` silently promotes gravity state to rank-4. Add the kinetic leg (the docstring already flags it as fork-level and missing). Extend beyond $T^{00}$: momentum density $T^{0i}$ at minimum, since a scalar $\Phi$ cannot represent a moving source.

**P3.5 — Global conservation and the acceptance observable.** One energy convention across all channels (start by resolving the `½` discrepancy between `channels.py:72` and `coupled.py:35-37`). A `TotalEnergy` observer summing every channel plus interaction terms. **This is the single most important deliverable in the roadmap**: without it, a unified run produces pictures nobody can falsify. Gate it in the suite.

**P3.6 — Close the gravity loop.** Gauge channels read $K$ — light bends in the production engine, not just in a fork. Quark channels call `_grav_sqrtA`. Lift the massive-doublet/quark restriction at `particles/channel.py:166-171` or document precisely why it stands.

**P3.7 — Multi-scale as a first-class concept.** `two_grid_atom` and `element_atom` nest a private sub-lattice and a private mini-engine inside one channel (`particles/channel.py:1459-1475`), making those sub-states invisible to gravity, to observers, and to the global block-spin. Promote nesting to an engine concept: a `Region` with its own refinement factor and an explicit, conservative interface to the parent lattice. This is what the proton:orbit ratio ($\sim10^4$–$10^5$) actually needs.

> **Acceptance gate P3:** one scenario runs the gauge sector, matter, and dynamic gravity on a single BCC lattice with a single clock, conserving total energy to the machine-precision class over ≥ 10³ ticks; reordering `channels:` in the YAML changes nothing; a dangling coupling name errors at build time; light measurably bends around a dynamically-sourced mass in the production engine.

---

### P4 — Scenario language v2

Everything a "configure and press go" universe needs that today's schema cannot say. The loader currently validates two things — that the file parses and that `channels` is non-empty — so `withd: 1.5` is silently ignored.

| Addition | What it buys |
|---|---|
| **Strict schema** (JSON-Schema or pydantic) + cross-reference validation | Typos and dangling coupling targets error at load, not at tick 400 |
| `units:` block | Nothing today maps a cell to metres or a tick to seconds |
| `events:` timeline | Today `blockspin: [{at: N}]` is the *only* tick-triggered action. Enables: inject at tick N, pulse a field, take a measurement, ramp a coupling |
| `expect:` gates | Per-scenario success criteria; the `TOL` dict is currently hard-coded at `src/casim/analysis/__init__.py:16-20` |
| `boundaries:` | Everything is periodic. No walls, absorbers, inflow/outflow, no external field region |
| `extends:` + matter templates | "Put a hydrogen atom at (12,8,8)" instead of hand-writing 6 channels with matched `sources`/`couplings` in the right order. The 46 YAMLs are copy-paste variants today |
| `sweep:` / `seeds:` | No ensembles or parameter grids; the suite runs each file once |
| `view:` block | Camera, visible channels, colour mode, slice plane — so "press go" doesn't start from GUI defaults |
| `from: checkpoint.npz` | A scenario cannot start from a saved state; only `casim resume` can, and it bypasses the YAML |
| `compute:` block | dtype, device, threads, memory cap — none expressible today |
| Per-channel seeds | One global RNG for everything (`simulation.py:108`) |

Migrate the 46 existing scenarios with a converter; keep v1 loading behind a deprecation warning for one cycle.

> **Acceptance gate P4:** every shipped scenario validates strictly; a deliberately misspelled key fails at load; `hydrogen.yaml` is under 20 lines via templates; one scenario file expresses a timed event and a pass/fail expectation.

---

### P5 — The GUI as a workbench

The GUI is real and working (vispy point clouds, live engine stepping, per-channel tints, Bloch-hue spinor mode, checkpoint/resume, sidebar observables). It is undersold — `cli.py:8,242` still calls it "Phase E (not yet implemented)."

**P5.1 — Consolidate viz.** Three generations coexist with line-for-line duplication: `render.density_to_rgba` reimplements `live_display.py:85-96` with identical colour stops; `render.point_cloud` duplicates `live_display.get_point_cloud`; `render.bloch_rgb` mirrors `spinor_color.py`. Retire `live_display.py` (no importers; its only entry is `start_live.sh`, and it pip-installs at import time) and `spinor_color.py` to `deprecated/`. Give `casim.viz` real content — a static-figure layer — rather than an import shim nothing imports.

**P5.2 — Interaction.** Place matter by clicking; edit parameters live (mass, couplings, thresholds) without the current destroy-and-rebuild-from-tick-0; volume slicing; frame/movie export; expose `steps_per_frame` (hard-coded 2 at `app.py:170`).

**P5.3 — Time.** A ring buffer of recent states enabling rewind and scrub. Today time only moves forward.

**P5.4 — Results browser.** There is no diff of two result JSONs, no time-series plotting, and no HTML reporting anywhere in `src/` or `tools/` (the tree's one HTML file, `papers/tools/ehd-lifter-calculator.html`, is unrelated). Add a compare view over the P1.4 manifest: pick two runs, see which observables moved. This is also the natural home for the findings ledger — click a finding, see its test, its result, its exactness class.

> **Acceptance gate P5:** one viz implementation; a full experiment (place matter → run → observe → export figure) without touching a YAML; two runs diffable side by side.

---

### P6 — Kernel coverage

**~67 of 106 kernels have no path from any channel** (the count moves by a few depending on whether re-export shims in `casim/fields/*` count as reachability — P1.4's manifest should settle the criterion once and report against it). Wrap by sector, using the existing compute-once `spectral_matter` pattern where the physics is a solve rather than an evolution.

| Sector | Kernels | Notes |
|--------|---------|-------|
| Gravity / astrophysics | `ca_blackhole`, `ca_qnm`, `ca_inspiral`, `ca_horizon_entropy`, `ca_interior_metric`, `ca_tolman`, `ca_ns_eos`, `ca_stellar`, `ca_cosmology`, `ca_darkmatter`, `ca_emergent_gravity`, `ca_raytrace` | **The largest gap**, and the sector with the most external-data confrontations. Note `ca_raytrace.py:91` still computes `F114_enlargement_pct` — superseded by F178 |
| QED precision | `ca_amu`, `ca_twoloop_ae`, `ca_bethe_log`, `ca_electron_self_energy`, `ca_vacuum_polarization`, `ca_qed_renormalization`, `ca_qed_scattering`, `ca_vertex_loop`, `ca_hyperfine`, `ca_positronium`, `ca_euler_heisenberg`, `ca_schwinger_pair`, `ca_casimir` | Almost all compute-once. F251/F252 and F257–F263 live here |
| Lattice perturbation theory | the whole `ca_lpt_*` family, `ca_link_hamiltonian`, `ca_bgfield_loop` | Compute-once |
| QCD running / spectroscopy | `ca_alpha_s_running`, `ca_su3_ladder`, `ca_gluon_self_energy`, `ca_gap_solve`, `ca_njl_induced_coupling`, `ca_scheme_constant` | Feeds the F151/F152/F154/F155 open bracket |
| Electroweak / Higgs | `ca_higgs`, `ca_weak`, `ca_hypercharge`, `ca_chiral_anomaly`, `ca_majorana` | Importable via shims but **no channel drives them; there is no Higgs channel at all** |
| Quantum info | `ca_quantum_algorithms`, `ca_bell_tsirelson`, `ca_decoherence_floor`, `ca_qc_si` | |

Also resolve `ca_blockspin` / `_dynamical` / `_binding`: the engine reimplemented block-averaging natively (`blockspin.py:49-62`) because `ca_blockspin.block_average` float-casts and drops the imaginary part. Either fix the kernel or formally deprecate it — right now both exist and only one is right.

> **Acceptance gate P6:** every non-deprecated kernel is reachable from a channel or a compute-once wrapper, and appears in the results manifest.

---

## 5. Sequencing

```
P0 ──┬──> P1 ──┬──> P3 ──> P4 ──> P5
     │         │
     └──> P2 ──┘         P6 (continuous, any time after P1)
```

- **P0 blocks everything.** Two weeks of unglamorous work that makes every later phase checkable.
- **P1 and P2 are independent** and can interleave. P2.1 (`pyfftw`) is an afternoon and speeds up P1's baseline generation, so do it first regardless.
- **P3 requires both.** It needs P1's baselines to prove the BCC ports are faithful, and P2's throughput to run the 10³-tick conservation gate.
- **P4 and P5 follow P3** — no point hardening a schema for an architecture still in motion.
- **P6 is background work**, parallelisable and a good fit for delegated sessions once P1 gives it a landing pattern.

**The critical path is P0 → P1 → P3.1.** Everything else can slip without moving the end state.

---

## 6. Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **BCC photon loses exactness.** The even-law paired photon's exactness may not survive the BCC dispersion. This would undercut D1 and, worse, the F69/F250 canon. | **High** | Spike P3.1 as a standalone derivation *before* any porting. Treat a negative result as a finding worth recording, and re-open D1 rather than accepting a degraded photon |
| **P1.3 breaks a verified result silently.** Moving import-time work into `main()` across 272 files will touch code nobody has read in months. | High | Strictly baseline-first: no file is restructured until P1.2 has recorded its numbers. Bit-for-bit comparison, one file at a time |
| **Backend migration changes results at round-off.** Different FFT libraries differ in the last bits; that is invisible in most codebases and fatal in one whose product is a $10^{-12}$ gate. | Medium | Every backend must clear the `_NumpyFftBackend` regression. Where a difference is real, record the tolerance rather than hiding it |
| **P0's registry becomes a second source of truth.** Two places to define a constant is worse than one. | Medium | The registry holds provenance and the consistency test; kernels stay authoritative for values (D2). If it starts drifting, invert: kernels import from the registry |
| **Scope. P3 is very large.** | Medium | P3.1–P3.5 are separately shippable; P3.7 (multi-scale regions) is the natural cut line if time runs short |
| **Concurrent-session collisions.** This has already happened twice (F110, F129) and F262 needed a manual renumber. | Low but recurring | The P0.3 ledger plus a max-F check in `regen_indexes.py` |

---

## 7. What this roadmap does not change

- **No physics decisions are reversed.** CLAUDE.md's seven core design decisions stand unchanged. D1 is an *engineering* decision to make BCC canonical in the software; it is downstream of F91/F175/F264, not a new claim.
- **The kernels keep their authority** (D2). This is a wrapping and provenance program, not a rewrite.
- **Superseded work is tombstoned, not deleted.** F50/F52/F62, F114, the σ-bilinear photon, the chiral gluon, and F179/CN3 remain runnable in `archive` — they are how the supersessions stay checkable.
- **The exactness bar does not move.** No global precision reduction; `exact` and `machine_precision` keep their current meanings.

---

*Cross-references: `docs/theory/key-decisions.md` (D1 to be recorded there), `docs/roadmaps/roadmap-unified-real-space.md` (F134–F137 arc, which P3.7 subsumes), `deprecated/roadmap-standalone-program.md` (Phases A–G, complete), `scenarios/SUITE-GUIDE.md`, `src/casim/README.md`.*
