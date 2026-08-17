# Roadmap — CASIM as a Single Comprehensive Modeling Program

*Created 2026-07-29 - 19:42. **Rewritten 2026-07-31 - 19:40** against the tree as it stands after the C-roadmap (`roadmap-casim-consolidation.md`, C0–C9, **complete**). Supersedes the completed `deprecated/roadmap-standalone-program.md` (Phases A–G, which delivered the package layer).*

*This roadmap covers the arc from "a package that wraps kernels" to "one universe, one lattice, one clock."*

*Status 2026-08-01: **P0 and P2 are done; P1 is done bar P1r; P3's engine-architecture half — P3.2, P3.3, P3.4, P3.5, P3.6 — is COMPLETE and gated (F268/F269/F270); P6's instrument is built but its coverage problem is not reduced; P4 and P5 are unbuilt.** **Five of six structural blockers are now closed**: B6 by P2, and B2/B3/B4/B5 by the P3 pass. **B1 alone remains**, and it is P3.1 — the five cubic layers F265 named plus the F267 mode-sum audit, which is physics rather than engineering. The engine now has one clock, a typed exchange bus, one energy convention with a machine-class conservation gate, and a closed gravity loop; what it does not yet have is one lattice.*

*Sequencing note, superseded by events: the previous revision named P3.5 "the piece to ship next" because nothing in this roadmap could be falsified without it. That is done — a unified run now produces a number a gate can reject. **The critical path is now P3.1.***

---

## 1. Purpose and end state

**End state (decided 2026-07-29, unchanged):** a single simulation in which gauge, matter, and gravity sectors coexist on **one lattice** with **one clock**, configured declaratively and observable live. Not a launcher for per-sector scripts.

**Design decisions.** D1–D5 were taken at the start of this roadmap; D6–D11 were taken by the C-roadmap and **reverse D2**. All eleven now live in `docs/theory/key-decisions.md` §"Engineering decisions"; the D2 reversal is ledger record `S8-D2-reversed-casim-is-the-program` (kind `methodology`).

| # | Decision | Status |
|---|----------|--------|
| D1 | **BCC is the canonical universe topology.** Cubic kernels are reference implementations retained for regression. | Stands. Labelling done (C3.3); the `cubic.py` extraction and the channel-level port are **P3.1**, still open |
| D2 | ~~Flat `ca_*.py` kernels remain the single source of truth.~~ | **REVERSED by D6 at C9.** `ca-simulation/` is deleted; `casim` is the program |
| D3 | Two co-equal interfaces: declarative scenarios + CLI, and an interactive GUI. | Stands. Both exist; the schema they share is still v1 (**P4**) |
| D4 | Compute target: Apple Silicon now, rented/cloud GPU later. | Stands. Protocol built (D8); two device backends written, **neither has cleared the contract on real hardware** |
| D5 | Foundations first — P0–P2 precede P3. | **Honoured, and vindicated.** P0–P2 are done and P3 is now checkable in a way it was not |
| D6–D11 | CASIM is the program · constants own values · one numerics surface · declarative tests · cleanup-and-migration as one operation · every module registered | **All delivered** (C0–C9) |

---

## 2. Where we actually are

Measured 2026-07-31 by direct audit of the tree, not from documentation. Where a number is quoted from the original roadmap for comparison it is marked *(was)*.

### 2.1 Assets

| | |
|---|---|
| `src/casim/` | **73.2k LOC** — the whole program *(was 8.3k package + 40.6k kernels in a second tree)* |
| engine modules registered (D11) | **178.** `sector` and `reach` are populated on all 178; `findings` on **33**, `tests` on **132**, and **`exactness` on none** — the field exists and is empty, which is a P6 item, not a claim |
| channel types | **29**, across 6 channel modules |
| scenarios | **46** YAML |
| tests | **347 files / 80.2k LOC** (348 including `conftest.py`), all 347 covered by **350 declarative registry records** (D9) |
| result artifacts | **394** |
| findings | **261** files, max F266, **0 duplicate numbers** |
| constants registered (D7) | **43**, plus **10** `MeasuredConstant` records |
| gate | `make gate` — **14 checks, green** (C9 retired four; the count was 18 at C7) |

### 2.2 The two cross-cutting hazards: both closed

*Provenance.* $c_\text{lat}$'s ~74 independent literal re-definitions are gone. **Rogue literals: 202 → 0**, ratcheted — the 202 spanned `src/` *and* the now-deleted kernel tree, so today's measurement is "0 in `src/`"; `tests/` carries 272 as a declared, counted backlog. $\delta^*$ had no canonical owner and three local redefinitions; it is now one `Fraction(2,9)` in the registry and all three call sites import it. The three deliberately-plural constants ($f_\pi$, $\sin^2\theta_W$, $\cos3\delta^*$) kept their multiplicity on purpose, and `alpha_eff_star` is still a bracket with no scalar value. The live contradiction in `derive_generator_norm.py` (was `derive_generator_norm_from_F118.py`) was preserved with a `PRE-DECISION FRAMING` banner rather than deleted — its Schur-isotropy proof *is* the F255 content.

*Enforcement.* There is now CI (`.github/workflows/gate.yml`) and a Makefile. `pytest` runs the gate tier by construction: `tests/conftest.py` *excludes* what the registry says to exclude (`pytest_ignore_collect`) and `tests/casim/test_registry_entries.py` *parametrises* over the same records `casim test` runs, so the two cannot diverge. Superseded physics is a registry field (`tier: archive`), not an invisible test.

### 2.3 The six structural blockers, re-measured

| # | Blocker | 2026-07-29 | 2026-07-31 |
|---|---------|-----------|-----------|
| B1 | **Topology partition** | 6 cubic-only, 10 BCC-only, 13 agnostic; engine hard-rejects mixing | **Unchanged, and re-framed by F265** — see §2.4. Still 6 cubic-only (`photon_pair`, `w_chiral`, `z_even`, `charge_photon`, `gauge_mc`, `refraction_2d`), 10 BCC-only, 13 agnostic; `simulation.py:71` still rejects mixing. Scenario split: 31 BCC / 15 cubic |
| B2 | **No engine clock** | `step()` takes no `dt`; each channel privately means something different by "a tick" | **CLOSED 2026-08-01 (P3.2, F268).** `casim.engine.core.clock`: channels declare `dt_native`/`dt_max`/`subcyclable`, the engine takes $\Delta t$ = the coarsest native step and sub-cycles the rest, ratio in exact rational arithmetic. Measured on the way in: **18 of 46 scenarios were desynchronised**, every flagship unified one included — the EM field advanced $\tfrac1{10}$ the physical time of the matter sourcing it. Those 18 run in `legacy` (bit-identical) with the desync now *written into their results*; promoting them to `strict` is physics work, deliberately unstarted |
| B3 | **Ordering load-bearing and unchecked** | YAML order = Gauss–Seidel; coupling by untyped string key; typo → silent `None` | **CLOSED 2026-08-01 (P3.3, F269).** `casim.engine.core.graph`: `provides`/`consumes`, build-time error on a dangling name, iterative Tarjan SCC, stable topological sort. Reference resolution is **structural** — any config string naming a sibling channel is an edge — after a curated key list was found to miss 45 of them across four key paths. Over 46 scenarios: **0 dangling names, 16 cycles, 1 violation, and that one is vacuous** (its edge carries no payload). Cycles resolved by a declared scheme (`gauss_seidel` / `jacobi`), never by line order |
| B4 | **No total-energy observable** | six incompatible energy conventions; nothing a coupled run could fail | **CLOSED 2026-08-01 (P3.5, F270, ledger S9).** One convention, $\tfrac12\sum(E^2+B^2)$, defined once. Found a *second* defect under the ½: `Channel.energy` mixes a dimensionless probability norm with an energy, so the additive quantity is a separate `energy_density` protocol. `TotalEnergy` observer gated; free photon, $L{=}16$, 1000 ticks → `max_rel_drift` $3.4\times10^{-14}$, class **machine**. 0 registry-declared baselines moved |
| B5 | **Gravity half-connected** | $T^{00}$ rest-leg only; no gauge channel reads $K$; colour-axis broadcast bug | **CLOSED 2026-08-01 (P3.4 + P3.6, F270).** Colour axis summed — the bug silently produced a *three-copy* gravitational field, one per colour, and reported success. `T00_dirac_kinetic` added (D-EM3; verified against $\tfrac12c^2\sin^2\!k\sum\lvert\psi\rvert^2$, not a threshold) and `T0i_dirac`. `Channel.read_K` + `photon_step_dielectric` close the gauge side: **light bends in the production engine**. Now **k-resolved with no free parameter** (F271, ledger S10) — exact for uniform $K$ ($4\times10^{-15}$), 2nd-order convergent, norm drift converging rather than plateauing. The eikonal $\omega_0$ mix is superseded; the deflection *coefficient* vs GR remains a fork-battery job |
| B6 | **The performance seam is decorative** | zero physics modules imported the backend; 266 `np.fft.*` call sites by the original regex count (C1 re-counted the *transform* subset as 161 across 32 files — the difference is `fftfreq`-class index arithmetic) | **CLOSED.** Direct `np.fft` transform calls in `src/`: **161 → 0**, ratcheted. One registry (`casim.numerics`, D8), **six** backends since P2.7 registered `jax`. The device hole is closed too: the 8 `jnp.fft` calls in `gauge/weak_wmu.py` are now counted by a `device_fft_call_sites` ratchet over `jnp\|jax.numpy\|cp\|cupy\|mx\|mlx.core\|torch` (baselined at 8, verified to trip on a 9th) and sit behind `casim.numerics.precision.require_float64`. **One acknowledged gap, by design:** `tests/` still has ~75 direct `np.fft` sites and the ratchet exempts `tests/` — a test asserting *against* the façade must be able to call numpy directly |

**So: five of six blockers are closed.** B6 was P2's; B2, B3, B4 and B5 fell to P3's engine-architecture pass on 2026-08-01 (F268/F269/F270). **B1 — the topology partition — is the one still open**, and it is the physics half of P3.1. That is not drift — it is D5 working as intended: the C-roadmap spent its budget making B1–B5 *checkable*, and the original text is explicit that "everything above exists to make this checkable."

### 2.4 What F265 changed about B1

**B1's framing was wrong, and the correction is load-bearing for P3.1.** F265 (2026-07-29, 12/12, established) found that the split "does not run between gauge and matter — it runs between **propagator and action**, inside each gauge sector."

- **Every gauge propagator was already BCC.** γ, W, Z and the gluon all evaluate $\omega^\pm$ from `bcc_dispersion(k/2, \pm)`. F91/F166/F250 rest on this and are untouched.
- **Every gauge action was simple-cubic**, built by collapsing the eight BCC links into three straight $\pm x,\pm y,\pm z$ composites and taking square plaquettes with `a2 = 4.0`.
- That composite construction is not merely inelegant, it is **blind**: it resolves $2N_s$ of $3N_s$ curvature-carrying directions, so **one third of the field strength was missing at every amplitude**, and its suspiciously *good* $O((ka)^3)$ Bianchi convergence was the symptom, not a virtue.
- Both actions have the **identical classical continuum limit** ($\sum_p(F_{\mu\nu}d_1^\mu d_2^\nu)^2 = 8F_{\mu\nu}F^{\mu\nu} = \sum_{\mu<\nu}(4F_{\mu\nu})^2$, exactly), which is why no normalisation check or $g_\text{lat}$ calibration could ever have caught it.
- The genuine BCC action is **6 rhombic plaquettes with $\langle110\rangle$ normals**, area $2\sqrt2$, one $O_h$ orbit, reconstructed in closed form from $\sum_p m_pm_p^{\mathsf T}=4\mathbb{I}$.

**Migrated into live code:** `casim.engine.gauge.bcc_action`, with `weak_wmu.plaquette_field_strength` and `gluon.plaquette_field_strength_su3_bcc` now on the genuine BCC plaquettes and the composite versions retained as `DEPRECATED (F265)` comparison objects.

**Five cubic layers F265 explicitly left open** (F265 §9, "Still cubic, explicitly open"). These are P3.1's real scope:

1. **`gauge/lpt_*`** — the entire one-loop chain is 4D hypercubic Wilson ($\hat k_\mu = 2\sin(k_\mu/2)$, `range(4)`). F155/F239 already name the BCC-BZ vertex computation as the one remaining production-grade job; §2's factor 4 says the BZ *measure* is wrong there too.
2. **`gauge/bgfield_loop`** — folds a BCC propagator against continuum vertices on the **cubic** BZ with a `mod 2π` wrap: over-counts the spatial measure by 4 and samples the wrong zone. `make_kgrid_bcc` now supplies the fix; it has not been applied or re-run.
3. **`gauge/hypercharge` is 2D despite its docstring** — it calls `dirac._weyl_half_step_2c`, which builds only `KX, KY`, so U(1)$_Y$ lives on the 2D $1/\sqrt2$ lattice. F265: "Promotion to 3D BCC is a physics job, not a rename."
4. **The Monte-Carlo actions** — F94 4D cubic, F146 3D cubic — to be rebuilt on the rhombic action.
5. **The $\sqrt3$ question, and this one is a derivation risk.** The link side is now the integer BCC lattice (hop $d$, `np.roll` exact) while the fermion walk uses $e^{ik\cdot d/\sqrt3}$ — a *fractional* shift, the same lattice at a different unit of length ($q=k/\sqrt3$). Consistent as a rescaling, **but the walk is evaluated on the cubic FFT cube, which per F265 §2 is 4 BZ copies.** Whether the fermion sector needs the same measure correction is **open**, and F265 calls it "the natural next item."

**What this does and does not de-risk.** P3.1's original spike question — "does the even-law photon's exactness survive on BCC?" — is answered in the affirmative for the *propagator*: it was never cubic, and F250 establishes the all-$k$ gauge pole with a unique BZ zero. Items 1–4 are then engineering with a known exact target (F265 §6 gives it: the composite resolves $2N_s$ of $3N_s$; a correct port resolves $3N_s-3$).

**Item 5 is not engineering.** It is exactly the kind of open derivation the original roadmap wanted a spike for, and it sits under the fermion sector rather than the gauge sector. **So P3.1 should still open with a spike — on the $\sqrt3$/BZ-measure question, not on the photon.** Also note F265's own middle bucket: a long list of results (F43/F33, F94, F146, F101/F102/F110, F86/F88 and hence F124/F235, and the $d_1$ chain F144/F151/F152/F154/F155/F162/F163/F239) are **not invalidated** but are re-scoped as "measured on an action that is blind to 1/3 of the curvature." Re-deriving them is a real, unscheduled body of work that this roadmap does not own and should not pretend to.

### 2.5 P6 measured: the instrument was built, the coverage problem was not reduced

The C-roadmap promised "P6 dissolves into C6 + C8 — reachability becomes a registry field rather than a survey." It delivered exactly that and no more. The table below is from **`docs/design/module-graph.json`** (`summary.reach`), computed from one import closure per channel module:

*Two populations, and the difference is real: the **module registry** holds **178** records, the **module graph** types **184** nodes as engine roles. The 6 extra are the fork sub-package `__init__.py` files, which the graph types `role: fork`. Counts below are the graph's.*

| role | driven | package-only | test-only | entry-script | unreferenced | total |
|---|---:|---:|---:|---:|---:|---:|
| kernel | **48** | 2 | **66** | 0 | 4 | 120 |
| fork | 2 | 0 | 23 | 0 | 28 | 53 |
| derivation | 0 | 0 | 2 | 9 | 0 | 11 |
| **total** | **50** | 2 | 91 | 9 | 32 | **184** |

**72 of 120 kernels are not driven by any channel** *(was "~67 of 106")*. The ratio is essentially unchanged; what changed is that it now has a definition, a value, and a query. Of the 28 unreferenced forks, **6 are `__init__.py` files** and 22 are real forks — and those 22 are **not** a defect: a rejected fork should not be in a channel; that is what makes it a falsification record.

**Two defects the P6 instrument itself has, and they belong to P6:**

- **`code-index.md`'s generated Reach column cannot show the table above.** Across its 178 engine rows it takes exactly **two** values — 47 `driven` / 131 `package-only` — with zero `test-only`, `unreferenced` or `entry-script`, because `registry.py` takes `reach` as a manifest-supplied string rather than from the graph. So the artifact a reader is pointed at disagrees with the graph (47 vs 50) *and* collapses four categories into one. **Fix this first**: it is the field P6's acceptance gate is written against, and it is currently the less informative of two sources that should be one.
- **`exactness` is empty on all 178 registry records.** The field exists, `code-index.md` renders a column for it, and nothing populates it. Since C8.4 showed the class vocabulary can be canonicalised (530/530 rows classified, 147 declared + 383 by numerical signature), the same three-rule ladder could populate this — which is what would let `casim test --exactness exact` select by module rather than only by test record.

### 2.6 Residual debt inherited from P1/C7, quantified

These are real, they are counted, and they are deliberately not hidden:

| | count | note |
|---|---:|---|
| `import_time_work` | **320** | P1.3's condition, unreduced. C7 fell 321 → 320 and declared its own acceptance criterion **NOT MET** rather than redefine it |
| `unfalsifiable` (manifest-derived) | **70** | C7 refused to re-derive this against the registry: "that would make the number improve without any test improving" |
| `no_assert` | **231** | from 232 |
| `legacy_script` (declared debt) | **47** | rose from 38 by *measurement*, not regression; the raise required a `--reason` |
| baseline drift FAILs | **28** | measured from `test-results/arming-journal.json`, not quoted from C7 (which said 12, then 15, mid-pass). Each needs a physics owner: accept the number or find the regression. Triage ran over **29** drifting records and split them **11 supersession candidates / 18 regression candidates** (`docs/status/baseline-provenance.md`); the 29th is F62, now decided `stale_by_design` and reporting `STALE`, which is why the live FAIL count is 28 |
| arming journal | 202 armed / 11 unarmed / **2 timeout** / **10 error** / 1 stale | Verdicts: 174 PASS, 28 FAIL, 12 ERROR, 11 SKIP, 1 STALE. **4** of the errors are `exit -9` memory kills, not logic (two `priority/` open-BC tests, `run_FC02_shapiro`, `run_FC04_deflection_dynamical`) |
| duplicate finding numbers | **0** | was 10; F200 → F266 closed the last genuine tie |

---

## 3. Target architecture

```
                    ┌──────────────────────────────────────────┐
                    │  Scenario v2 (YAML)  —  one universe      │   P4 — NOT BUILT
                    │  units · lattice · matter · events        │
                    │  couplings(typed) · expect · view · out   │
                    └───────────────┬──────────────────────────┘
                                    │  strict schema + cross-ref validation
      ┌─────────────────────────────┴─────────────────────────────┐
      │              casim.engine — one clock                     │   P3 — NOT BUILT
      │  dependency graph (topo-sorted, not registration order)   │
      │  dt reconciliation + sub-cycling                          │
      │  typed exchange bus: provides/consumes {J_em,J_col,T^μν}  │
      │  global conserved quantity + gate                         │
      └───┬──────────────────┬───────────────────┬───────────────┘
          │                  │                   │
   ┌──────┴─────┐    ┌───────┴──────┐    ┌───────┴───────┐
   │ constants  │    │  channels    │    │  numerics     │
   │ registry   │    │  29 types    │    │  numpy·scipy  │
   │  D7 ✓      │    │  6 cubic-only│    │  ·pyfftw ✓    │
   │  values    │    │  10 bcc-only │    │  ·mlx ·cupy   │
   └──────┬─────┘    └───────┬──────┘    └───────┬───────┘
          │                  │                   │
          └──────────────────┴───────────────────┘
                             │
                  ┌──────────┴───────────┐
                  │  casim.engine/       │  ← D6: this IS the source of truth
                  │  178 modules, by     │     (D2's second tree is deleted)
                  │  sector, on BCC      │
                  └──────────────────────┘
```

Three things this sketch asserts that are still not true: the exchange bus is **typed and validated at build time** (B3), the engine owns a **clock** rather than a tick counter (B2), and the scenario schema **validates** (P4). Everything below the engine box is built.

---

## 4. Phases

### P0 — Ground truth · **COMPLETE** (2026-07-30)

| | Deliverable | Status |
|---|---|---|
| P0.1 | Constants registry | **DONE**, and superseded by **D7**: the registry now owns *values*, not just provenance. 43 constants + 10 `MeasuredConstant` |
| P0.2 | Consistency test | **DONE, polarity flipped** (C2.4): from "every recorded site agrees" to "**no unregistered literal matching a registry value exists in `src/`**". Rogue literals 202 → 0 |
| P0.3 | Supersession ledger | **DONE.** `docs/theory/supersessions.yaml`, 8 records; gained a `baselines:` block (artifact provenance) and a `methodology` kind (the D2 reversal) |
| P0.4 | Tombstone superseded tests | **DONE, and its lesson became doctrine**: of 14 files an audit called superseded, exactly **one** was superseded wholesale. The marker became a registry field (`tier: archive`) at C7.3 |
| P0.5 | A gate that exists | **DONE.** `make gate` + `.github/workflows/gate.yml`; **14 checks, green** |

*Acceptance gate P0: **MET**.*

### P1 — Test and results consolidation · **COMPLETE, with two counters honestly left standing**

| | Deliverable | Status |
|---|---|---|
| P1.1 | Three tiers | **DONE**, and upgraded to a registry field at C7. `gate` 17 / `battery` 333 / `archive` 0. `tier: archive` is structurally uncollectable |
| P1.2 | Close the assertion deficit | **DONE by a better mechanism than the roadmap proposed.** No `tests/baselines/` directory was created: the tests already write to `test-results/*.json` and **those are committed, so HEAD *is* the baseline**. One operational caveat: the whole C-roadmap is currently uncommitted (757 dirty paths) and `test-results/arming-journal.json` is untracked, so "HEAD is the baseline" holds for the physics artifacts but the *provenance of this session* is not yet in git. 350 records: 83 `assertion`, 217 `result_dump`, 3 `scenario`, 47 `legacy_script` |
| P1.3 | Kill import-time side effects | **NOT DONE — 320, deliberately.** C7.4 made physics-at-import *structurally impossible for a migrated record* (a record names a module **and an entry function**), but converting the remaining ~300 files was declared the next session's work rather than rushed. C7 recorded its own criterion as NOT MET |
| P1.4 | Results manifest | **DONE.** The prefix heuristic (capped at 2, empty on 104 of 339 rows) was **deleted, not improved**; every row is a declared registry mapping. Residual, re-measured: **56 records** have manifest-linked artifacts they do not declare (`casim index` prints it every run) — C7's arming to-do, in the open. C8 recorded 52 |
| P1.5 | One exactness inventory | **DONE at 100%** (530/530, from 147). Three ordered rules, each recorded per row: `declared` 147, `record` 0, `signature` 383. Staleness **125 findings behind → 0**, and stays there because the header is generated |

*Acceptance gate P1: **3 of 4 MET.** The fourth ("zero in RAN limbo") is met **structurally** — `validate()` refuses a record with no failure mode, and `DEBT` is a status, not a variant of PASS — while the manifest-derived `unfalsifiable` counter stays at 70 by explicit choice.*

**Two P1 items are still live work and are re-listed as P1r below.**

### P2 — Performance · **COMPLETE 2026-07-31 - 21:10** (P2.4's hardware claim excepted)

| | Deliverable | Status |
|---|---|---|
| P2.1 | pyfftw | **DONE and now live.** `casim.numerics.fft.describe()` reports `pyfftw (FFTW, 4 threads, plan cache on)`. Found a real bug wiring it: the six pyfftw call sites never passed `threads=`, so `set_workers` was documented and did nothing. Declared as the `fast` extra, never a hard dependency; the fallback is printed on every gate run |
| P2.2 | Make the seam real | **DONE, absorbed by C1 as D8.** 161 direct `np.fft` transform sites in 32 files → **0**, ratcheted. **84** `fftfreq`/`rfftfreq` sites in `src/casim` left on numpy deliberately (82 outside the façade; index arithmetic, no transform, no device). C1 recorded 83 |
| P2.3 | Allocation and caching | **DONE in substance.** `rfftn`/`irfftn`/`rfft`/`irfft` added and contract-pinned; `chiral_core` caching gives **1.94×** (`weyl_step`) and **1.74×** (`chiral_rs_step`). Two open sub-items: **`_FFT_OVERHEAD = 3.0` at `suite/tiers.py:40` is untouched**, and preallocated/in-place transform scratch was not done |
| P2.4 | Two accelerated backends | **PARTIAL — protocol done, hardware claim unproven.** Five backends registered (numpy, scipy, pyfftw, cupy, mlx); the equivalence contract exists and runs. Neither device backend has cleared it because **neither library is installed on any machine used so far**. MLX is additionally barred from auto-selecting: float32 eps $1.2\times10^{-7}$ is five orders above the `machine` gate |
| P2.5 | Gauge MC restructure | **DONE, profile-led. 2.06× at L=6, 2.38× at L=8, 2.59× with the reunitarisation cadence** (controlled A/B). `einsum`→BLAS `zgemm` (was 54% of a sweep), SVD→Gram-Schmidt `su3_reunitarise` (13.4→2.4 ms), `reunit_every` is a cadence. **Two of the four items were measured and declined:** the staple recompute is *physically required* (odd-parity staples move by 5.8 after the even half-sweep; caching breaks detailed balance) and `np.roll` is 7%, so halo buffers would give 1.07×. **The L=16–20 target is not met** — $L^4$ cost means 2.4× buys 1.24× in $L$, so the ceiling is ~15; the rest is P2.4's problem |
| P2.6 | Long-run operations | **DONE.** Checkpoints atomic (`.tmp-<pid>` + `os.replace`), compressed, and rotating by *tick* not mtime. `casim test --resume` reuses the newest suite dir and treats `suite_report.json` as the journal; `--redo` re-runs chosen items. Wall-time estimate in `--list` from measured anchors × cost ratio, labelled a lower bound. **The `blockspin_schedule`-on-resume bug is fixed** — it was silent-wrong, not merely missing, so any resumed block-spin result predating 2026-07-31 should be re-run |

*Acceptance gate P2 as originally written — "≥5× wall-clock on the reference set with bit-identical results; a second backend passes the seam regression; a 24-hour run survives a `kill -9` and resumes to the same trajectory" — scored honestly, **2 of 3 met and the third not measurable here**:*

| Criterion | Verdict |
|---|---|
| ≥5× wall-clock, **bit-identical** | **NOT MET, and partly incoherent as written.** Measured: 1.94×/1.74× (C1.4 caching), 2.06–2.59× (P2.5 `gauge_mc`). The pyfftw multiple has never been benchmarked on real hardware, and the sandbox cannot: `make install && make backend BENCH=1` on Ben's machine is where that number comes from. Note the two halves conflict — `batched_matmul` and every device backend are **1–2 ULP**, not bit-identical, so "≥5× *and* bit-identical" cannot both hold. The honest bar is "≥5× within the `machine` class", and P2.5 records its per-artifact deltas rather than claiming identity |
| A second backend clears the seam regression | **NOT MET on hardware, contract in place.** Six backends registered (numpy, scipy, pyfftw, cupy, mlx, **jax**); the equivalence contract runs and the JAX kernel has a machine-bound agreement test. Neither device library exists on any machine used so far, so the test skips — and a skip is the honest report, not a pass |
| A 24-hour run survives `kill -9` and resumes | **MET in mechanism, and now asserted.** Atomic write proved by a test that simulates a kill mid-write and asserts the previous checkpoint still loads; `blockspin_schedule` round-trips (it did not, silently); suite auto-resume verified end to end. Not yet exercised for a literal 24 hours — that is Ben's machine, not the sandbox |

*So P2 is closed as **built**, with its two unmeasurable claims named rather than assumed. The one thing that would close them both is a benchmark run on Apple Silicon.*

**P2.7 — Bring the JAX path inside the façade · DONE 2026-07-31.** `gauge/weak_wmu.py:755–799` has a live opt-in JAX path: `use_jax()` plus two `@jax.jit` kernels containing **8 `jnp.fft` calls** that bypass `casim.numerics` completely. Three consequences, none of them currently guarded:

1. **The D8 ratchet cannot see it.** `audit_numerics.py`'s regex matches `np`/`numpy` only, so a re-added *numpy* transform trips the ratchet and a JAX one does not. B6 is closed for numpy, not for devices.
2. **It is an unregistered sixth backend.** `casim.numerics.backends` has five (numpy, scipy, pyfftw, cupy, mlx) and a test asserts none can auto-activate; this path sits outside that registry, so the assertion does not cover it.
3. **It silently runs in complex64.** There is no `jax.config.update("jax_enable_x64", True)` anywhere in `src/`, so `use_jax(True)` runs the W propagator at float32 eps ($1.2\times10^{-7}$) — five orders above the `machine` gate — with **no `CASIM_ALLOW_FLOAT32` gate and no test**, which is exactly the protection MLX was given.

Either register it as a proper backend behind the equivalence contract and the float32 gate, or retire it. It should not stay as a third state. Note the original roadmap flagged this code positively (P2.4: "`ca_wmu.py:754-802` already has a JAX path … unreachable only because JAX is not a declared dependency") — the reachability was the good news; the precision hole was not noticed.

**Precision holds at complex128** — unchanged, and enforced for the five registered backends: none can auto-activate and a test asserts it. **P2.7 is the exception**, and it is the reason that sentence needs a qualifier.

---

### P1r — The two P1 items that are still work

*Small, mechanical, and both blocked on nothing. Listed separately because calling them "P1" implies they are done.*

**P1r.1 — `import_time_work` 320 → 0.** Give each test file an entry function and name it in its registry record. The structural mechanism exists (C7.4); this is the file-by-file application. Do it behind the baselines P1.2 provides — that was the original P1.3 discipline and it still applies. **This is the precondition for `pytest --collect-only`, `-k` filtering and `pytest -n` ever working**, which is in turn the precondition for the gate staying under two minutes as the suite grows.

**P1r.2 — Decide the 28 drift FAILs and the 23 undecided arming records** (11 `unarmed`, 10 `error`, 2 `timeout`). Each drift FAIL needs a physics owner: accept the new number (`git add`) or find the regression. Triage split the 29 drifting records **11 supersession candidates / 18 regression candidates** — and `docs/status/baseline-provenance.md` recommends an order (F182+F184 are one decision at two radii; `F64-em-connection` would confirm F178 keeps Schwarzschild in vacuum). Two have analysis but **not** a decision: `FG2`/`FG3` reproduce their deltas at HEAD to $10^{-15}$ from two independent directions (C5 via a pristine `git archive`, C7 via arming), which **points at** stale committed baselines rather than a regression — but C5 explicitly left the question open ("someone should decide whether the code regressed or the baselines were committed from a different configuration") and `baseline-provenance.md` still files both among the 18 regression candidates. Do not record them as closed until someone decides. Note the deliberate asymmetry: a `candidate` still reports `FAIL`, because if it suppressed failures the category would become a place to park inconvenient reds.

Then resume arming off-sandbox with `--budget 36000 --timeout 900 --retry-timeouts`, `--restore`, `--apply`. The 4 `exit -9` errors need memory, not patience. **`--restore` is not optional and is easy to forget**: a continued pass armed two records and silently left two modified baselines, and only the strict drift checker noticed. Order is always run → `--restore` → `--apply`.

> **Acceptance gate P1r:** `import_time_work` at 0 and the ratchet key retired; `casim test --tier gate` still green; arming journal has no `timeout` and no undecided `error`; every drift FAIL either accepted with a recorded reason or fixed; `make drift` still reports no tracked result JSON differing from HEAD.

---

### P3 — One lattice, one clock · **P3.2–P3.6 COMPLETE (2026-08-01). P3.1 and P3.7 remain.**

*The engine-architecture half is built and gated: the engine owns physical time (P3.2/F268), channels exchange typed quantities over a declared graph (P3.3/F269), and there is one energy convention with a machine-class global conservation gate plus a closed gravity loop (P3.4/P3.5/P3.6/F270). What remains in P3 is **physics**: P3.1's five cubic layers and the F267 mode-sum audit, plus P3.7, the declared cut line.*

*Everything in P0–P2 exists to make this checkable. It now is.*

**P3.1 — BCC unification (D1). Re-scoped by F265, and materially smaller than originally written.**

The original text made this "the largest single piece of work in this roadmap, and it is physics, not porting," and gated it on a spike that might have re-opened D1. **F265 moves the spike rather than removing it.** The gauge propagators were always BCC; F250 gives the all-$k$ gauge pole with a unique BZ zero; F265 fixed the gauge *action* and proved the composite construction was blind to a third of the curvature. So the photon is no longer the risk — but F265 §9 item 5 opened a new one in the fermion sector.

0. ~~**Spike first, on the $\sqrt3$/BZ-measure question**~~ — **DONE 2026-07-31, `findings/F267-walk-bz-measure-not-the-fft-cube.md`.** The answer: the walk's periodicity in $k$ is $\sqrt3\times$fcc, so **neither** the gauge side's fcc period **nor the FFT grid's own $2\pi$ period** is a period of the walk; the cube is $4/(3\sqrt3)=76.98\%$ of *one* zone — not a fundamental domain and not an integer number of copies, so **the gauge factor 4 does not transfer**. A delta translated by one hop spreads over 2274 of 4096 cells (exactly unitary), so the array points are **not** the walk's lattice sites and F265's "same lattice at a different unit of length" reading does not survive. **Two consequences for this phase.** (a) **The port is safe**: exactly one $\omega=0$ per branch and no $\omega=\pi$ inside the cube, so no doubler is introduced, F250 and the F69 photon are untouched, and **D1 does not re-open**. (b) **A new audit lands on P3.1**, below.
1. **Close the five residual cubic layers F265 named** (§2.4). Each is independently shippable and each is a finding.
   - **`bgfield_loop` — DONE 2026-08-01, [[F272]], but not as prescribed.** The prescription in §2.4 (*"the fix already exists in `make_kgrid_bcc`, unapplied"*) was **wrong**: that mask marks the fcc BZ, and `omega_even` is $\sqrt3\cdot$fcc-periodic, so applying it would have inserted a spurious factor of 4 into a quantity with no factor-4 error. The real defect was a `mod 2π` refold of $k+q$ by a period the rule kernel does not have. Flatness spread 1.58e-2 → 2.96e-5; the old number was not grid-convergent (70% shift n=14→18), the new one is (0.13%). $b_0=11$ untouched.
   - **`hypercharge` (2D → 3D BCC), the LPT chain, and the MC actions remain.** Given F273 §1, the LPT chain's BZ measure should be re-derived against the $\sqrt3$ period, **not** against F265's fcc reading.
   - **F265's factor-4 premise is now known to be wrong everywhere** — see F273 §1 — so any residual item that inherited it needs re-deriving rather than porting.
2. **Port the six cubic-only channel types' state layout**: `photon_pair`, then `w_chiral` and `z_even`, then `charge_photon`. Each port lands with a paired test asserting the BCC version reproduces the cubic one where they overlap.
3. **`gauge_mc` is a separate object** — $L^4$ links, and a Euclidean time axis its sweep treats specially (`lgt_fork_A_mc:469`, `if mu == t_axis:`, temporal links always free). Treat it as compute-once (the `spectral_matter` pattern), not co-evolving. Its action is also item 4 of (1).
4. **`refraction_2d`** is 2D by construction; decide explicitly whether it is a reference channel (like the cubic lattice code) or gets a 3D BCC form.
5. **Audit every $k$-space average (from F267). — STARTED 2026-08-01, [[F273]]; it is *not* a fermion-sector audit.** F273 §1 measured the raw, unhalved `bcc_dispersion` — the function the gauge side is built from — and found it is **also** $\sqrt3\cdot$fcc-periodic, so F265's clean-gauge/√3-fermion boundary does not exist. It also found the cube is a **biased** sub-region, not a partial one: $\langle\cot\omega\rangle$ vanishes *identically* over the true zone by symmetry but is a converged $+0.221$ on the cube — the difference is everything, not F267's 10.7–16.9%. `i2_lattice` (→ $B$ → $\lambda_6=0.243$) is **classified as a mode sum** and stands, but the classification exposes a structural tension between "the cube is the mode set" and "the crystal is BCC" that F273 §4 does **not** resolve and that is now the top P3.1 item. Coverage is partial: 56 sites found, 2 chains classified. Original text follows: Classify each as a **mode sum** — a trace over the operator's own eigenmodes, where the cube is *correct by construction* because it **is** the mode set — or a **continuum BZ integral**, where a cube grid-mean carries the measured **10.7%** ($\langle\omega\rangle$) to **16.9%** ($\langle1/\omega\rangle$) error. First entries: F100's $\sigma_\phi^2\to\gamma(\Omega)$ chain (whose *number* is plausibly the right mode sum while its *label* "Brillouin-zone average" is wrong), and the $d_1$ chain F144/F151/F152/F154/F155/F162/F163/F239, which F265 already re-scoped for the action. **Do not insert $3\sqrt3/4$ anywhere** — that would corrupt every mode sum in order to fix a label. This is a per-observable decision, not a patch.
6. **Extract the cubic reference into `engine/lattice/cubic.py`. — BLOCKED IN SANDBOX, handed back.** Measured: `core.py` is *100% cubic reference code*, so there is nothing to split out and the correct operation is a **rename**, not a split. This mount refuses `unlink`, so `git mv` cannot run here, and doing it by copy would leave two live copies of one module — the defect C9 spent itself eliminating. On Ben's machine: `git mv src/casim/engine/lattice/core.py src/casim/engine/lattice/cubic.py && git mv src/casim/engine/lattice/core_exact.py src/casim/engine/lattice/cubic_exact.py`, then repoint the **8** importers and the `ca_core`/`ca_core_exact` aliases in `src/casim/lattice/__init__.py`.

**If a port shows exactness does not survive, stop and record it as a finding** — a degraded photon is a worse outcome than a split lattice.

**P3.2 — A real clock (B2). · DONE 2026-08-01, `findings/F268-engine-clock-channel-desync.md`.** The engine owns physical time. Each channel declares `dt_max` (stability) and `dt_exact` (`1` for the spectral rotations whose $\Delta t$ is in the exponent, `None` for CFL-limited steppers). The engine picks a global $\Delta t$ and **sub-cycles** what needs it. Pull the ad-hoc internal sub-cycling out of channels and into the engine: `refraction_2d`'s `n_sub=4`, `element_atom`'s `hartree_every`/`gs_every`, `two_grid_atom`'s fine-then-coarse. Known free `dt` values to reconcile: 0.1 (`charge_photon`, `photon_sourced`), **0.2** (`nr_electron`, and `two_grid_atom`'s coarse grid at `particles/channel.py:1396`), 1.0 (`gravity_dielectric`, `gluon_sourced`), 0.5 (the remaining atom sub-lattices).

**P3.3 — Typed exchange bus (B3). · DONE 2026-08-01, `findings/F269-typed-exchange-bus-order-and-cycles.md`.** Channels declare `provides` and `consumes` (`J_em`, `J_colour`, `T00`, `A_mu`, `sqrt_A`, …). The engine builds a dependency graph and **topologically sorts** it, replacing registration-order Gauss–Seidel. An unsatisfied `consumes` is a build-time error, not a silent `None`. Cycles are resolved by an explicitly declared scheme (leapfrog / predictor–corrector), not by line order. **`casim.engine.core` has no `graph.py` or `bus.py` today** — this is new construction.

**P3.4 — Unified stress-energy (B5, part 1). · DONE 2026-08-01, F270.** One `T_munu(state) -> ndarray` protocol on `Channel`. **Fix the colour-axis broadcast bug in `T00_dirac_rest`** (`gravity.py:102`) — it still does not sum a leading axis, unlike `T00_field_energy` at `:115`, so a `quark_dirac` in `sources:` silently promotes gravity state to rank-4. Add the kinetic leg (its own docstring still flags it as fork-level and missing, and D-EM3 demands a fast packet gravitate by total energy). Extend beyond $T^{00}$: momentum density $T^{0i}$ at minimum, since a scalar $\Phi$ cannot represent a moving source.

**P3.5 — Global conservation and the acceptance observable (B4). · DONE 2026-08-01, F270, ledger S9.** One energy convention across all channels — start by resolving the ½ that `coupled.field_energy` has and `PhotonPairChannel.energy` does not. Then a `TotalEnergy` observer summing every channel plus interaction terms, gated in the suite. **Without it a unified run produces pictures nobody can falsify.** Note the shape of the enforcement is now available for free: make it a `kind: assertion` gate-tier registry record, and it cannot silently stop running.

**P3.6 — Close the gravity loop (B5, part 2). · DONE 2026-08-01 at eikonal order, F270.** Gauge channels read $K$ — light bends in the production engine, not only in a fork. Quark channels call `_grav_sqrtA`. Lift the massive-doublet/quark restriction in `casim.particles.channel` or document precisely why it stands.

**P3.7 — Multi-scale as a first-class concept.** `two_grid_atom` and `element_atom` nest a private sub-lattice and a private mini-engine inside one channel, making those sub-states invisible to gravity, to observers, and to the global block-spin. Promote nesting to an engine concept: a `Region` with its own refinement factor and an explicit, conservative interface to the parent lattice. This is what the proton:orbit ratio ($\sim10^4$–$10^5$) needs. **Natural cut line if time runs short.**

> **Acceptance gate P3:** one scenario runs the gauge sector, matter, and dynamic gravity on a single BCC lattice with a single clock, conserving total energy to the machine-precision class over ≥ 10³ ticks; reordering `channels:` in the YAML changes nothing; a dangling coupling name errors at build time; light measurably bends around a dynamically-sourced mass in the production engine.

---

### P4 — Scenario language v2 · **CHECKABLE CORE DONE 2026-07-31 (F274)**

*Update 2026-07-31 - 23:10: the strict schema, cross-reference validation, `extends:` templates, the `events:`/`expect:` blocks and the 46-scenario migration are built and gated (`tests/casim/test_scenario_schema_v2.py`, 12/12; `casim scenario-check` = 48/48). Acceptance gate P4 **4/4 MET**. Schema-complete-but-not-yet-engine-wired, by design (no baseline exposure): per-channel RNG seed streams, `expect:` run-verdict enforcement, non-periodic `boundaries:`. See F274.*


`load_scenario` still validates exactly two things: that the file parses to a mapping, and that `channels` is non-empty. **`withd: 1.5` is still silently ignored.** Measured: **0 of 46 scenarios** carry a `units:`, `events:`, `expect:`, `boundaries:`, `view:`, `extends:`, `sweep:` or `compute:` block, because none of those keys exist.

| Addition | What it buys | Note |
|---|---|---|
| **Strict schema** (JSON-Schema or pydantic) + cross-reference validation | Typos and dangling coupling targets error at load, not at tick 400 | The single highest-value item here |
| `units:` block | Nothing maps a cell to metres or a tick to seconds | `engine/lattice/si_scale` has the physics; the schema cannot say it |
| `events:` timeline | `blockspin: [{at: N}]` is still the only tick-triggered action | Enables inject-at-tick, pulse, measure, ramp |
| `expect:` gates | Per-scenario success criteria | **Partly delivered elsewhere:** the D9 test registry already carries `expect: {exactness, gates}` for its 3 `kind: scenario` records. P4 should adopt that vocabulary rather than invent a second one |
| `boundaries:` | Everything is periodic — no walls, absorbers, inflow/outflow, external-field region | |
| `extends:` + matter templates | "Put a hydrogen atom at (12,8,8)" instead of 6 hand-matched channels in the right order | The 46 YAMLs are copy-paste variants |
| `sweep:` / `seeds:` | No ensembles or parameter grids | **Partly delivered elsewhere:** `casim test --param k=v` already sweeps a *registry record*. P4 is the scenario-side equivalent |
| `view:` block | Camera, visible channels, colour mode, slice plane | So "press go" doesn't start from GUI defaults |
| `from: checkpoint.npz` | A scenario cannot start from a saved state; only `casim resume` can, bypassing the YAML | |
| `compute:` block | dtype, device, threads, memory cap | The device seam now exists to point it at (D8) |
| Per-channel seeds | **Still one global RNG** — `simulation.py:109` is `np.random.default_rng(self.seed)` | `casim.numerics.rng` already provides per-consumer streams; the engine does not use it. Cheap |

Migrate the 46 scenarios with a converter; keep v1 loading behind a deprecation warning for one cycle.

> **Acceptance gate P4:** every shipped scenario validates strictly; a deliberately misspelled key fails at load; `hydrogen.yaml` is under 20 lines via templates; one scenario file expresses a timed event and a pass/fail expectation.

---

### P5 — The GUI as a workbench · **CHECKABLE CORE DONE 2026-07-31 (F275)**

*Update 2026-07-31 - 23:10: the display-independent half is built and gated. P5.1 viz consolidation (`casim.viz` is now the single static-figure/colour-map API; `_viz_live_display` banner-retired; `casim.viz.density_to_rgba is casim.gui.render.density_to_rgba` asserted) and the P5.4 headless results-compare (`casim compare`, over `casim.baselines.compare`) landed; `cli.py`'s "Phase E (not yet implemented)" line is gone. Two of three acceptance clauses (one viz implementation; two runs diffable) **MET headlessly**. The interactive half — P5.2 click-to-place / live edits, P5.3 ring-buffer rewind, the GUI compare view, and the `git mv` retirement of `_viz_live_display` — needs a display and `casim[gui]`, and is specified in `docs/roadmaps/p5-gui-workbench-handback.md`. See F275.*


The GUI is real and working (vispy point clouds, live engine stepping, per-channel tints, Bloch-hue spinor mode, checkpoint/resume, sidebar observables) and still undersold: **`cli.py:8` still says "Phase E (not yet implemented)."** One line.

**P5.1 — Consolidate viz.** The legacy modules were *moved*, not retired — `engine/core/{_viz_legacy,_viz_live_display,_viz_spinor_color,_viz_tick_heatmap}.py` — and `gui/render.py:21` still reimplements `_viz_live_display.py:88`'s `density_to_rgba` with identical colour stops. **But the four are not one category, and the roadmap's "three generations" framing hides that:**

- `_viz_live_display` is imported by **nothing** — the module graph gives it `reach: unreferenced` with an empty importer list, and the registry marks it `status: dead_candidate` (the registry's own `reach` still says `package-only`, which is the §2.5 instrument defect). So the module `render.py` duplicates is the one that can simply go;
- `_viz_spinor_color` is `driven (15 ch)` — **production code**, not a retirable generation;
- `_viz_tick_heatmap` (3 tests) and `_viz_legacy` (1 test) are test-only: retire them **behind their registry records**.

Then give `casim.viz` real content — it is a **13-line import shim nothing imports**.

**P5.2 — Interaction.** Place matter by clicking; edit parameters live (mass, couplings, thresholds) without destroy-and-rebuild-from-tick-0; volume slicing; frame/movie export; expose `steps_per_frame` (still defaulted to 2 at `gui/app.py:170`, not settable from a scenario).

**P5.3 — Time.** A ring buffer of recent states enabling rewind and scrub. Today time only moves forward.

**P5.4 — Results browser.** No *user-facing* diff of two arbitrary runs, no time-series plotting, and no HTML reporting anywhere in `src/casim`. (Two machine-facing differs do exist and should be reused, not duplicated: `tests/runner._diff_against_head` — the `result_dump` failure mode — and `tools/check_result_drift.py`.) Add a compare view over the P1.4 manifest: pick two runs, see which observables moved. **The data model for this is now much better than when P5 was written** — `code-index.md`, `tests-index.md` and `findings-index.md` are generated from registries, so "click a finding, see its test, its result, its exactness class" is a join over declared fields rather than a heuristic.

> **Acceptance gate P5:** one viz implementation; a full experiment (place matter → run → observe → export figure) without touching a YAML; two runs diffable side by side.

---

### P6 — Kernel coverage · **INSTRUMENT BUILT, COVERAGE UNCHANGED**

The measurement is now a registry field rather than a survey (§2.5) — that was C6+C8's contribution and it is done, **with one gap worth fixing first** (see §2.5's note on `code-index.md`). **The underlying gap is not reduced: 72 of 120 kernels are not channel-driven** *(was ~67 of 106)*. Wrap by sector, using the compute-once `spectral_matter` pattern where the physics is a solve rather than an evolution.

**One correction to the original text's sector ranking:** it called gravity/astrophysics "the largest gap." Measured, **QED precision is** — 13 undriven of 13, with zero channels reaching any of it, against gravity's 12 of 15.

Measured per sector, 2026-07-31 (`driven` / `undriven` / total):

| Sector | driven | **undriven** | total | Notes |
|--------|---:|---:|---:|---|
| **QED precision** — `interactions/qed_*` | 0 | **13** | 13 | **The largest single undriven sector.** All compute-once; F251/F252 and F257–F263 live here. Zero channel reaches any of it |
| **Gravity / astrophysics** — `interactions/{gravity*,blackhole,qnm,inspiral,horizon_entropy,interior_metric,tolman,ns_eos,stellar,cosmology,darkmatter,raytrace}` | 3 | **12** | 15 | The sector with the most external-data confrontations. `gravity`, `gravity_backreaction`, `gravity_emqg` are driven; the whole astrophysics tail is `test-only` |
| **Lattice PT** — `gauge/{lpt_*,bgfield_loop,link_hamiltonian}`, `core/lpt_generator` | 0 | **8** | 8 | Compute-once. Also carries two of F265's five cubic layers (§2.4) |
| **QCD running / spectroscopy** — `interactions/running_*`, `gauge/{gluon_self_energy,su3_ladder}` | 1 | **8** | 9 | Feeds the F151/F152/F154/F155 open bracket. Only `running_scale_ratio` is driven |
| **Quantum info** — `interactions/qi_*` | 2 | **4** | 6 | `qi_entanglement` and `qi_noise` are driven |
| **Electroweak / Higgs** | 5 | **3** | 8 | **The original text's "no channel drives them" is now wrong for most of this sector** — `w_chiral`, `z_even`, `w_sourced` and `beta_decay` reach `weak`, `weak_wmu`, `weak_z`, `hypercharge` and `charged_current`. What remains: **there is still no Higgs channel** (`higgs` is `package-only`), `chiral_anomaly` and `majorana` are `test-only`, and `hypercharge` is 2D (F265 §9 item 3) |
| Forks | 2 | 51 | 53 | **Exempt** — see the acceptance gate |
| Everything else in `engine/` | 37 | 35 | 72 | Includes the 9 `entry-script` derivation scripts, which are meant to be run, not imported |

**Resolved since the original text:** `ca_blockspin.block_average`'s float-cast that silently dropped the imaginary part was fixed at C3.3 — dtype-preserving, real input bit-identical to the old behaviour, complex input keeps $\mathrm{Im}(f)$, no result moved. `raytrace`'s `F114_enlargement_pct` was **kept deliberately**, not cut: it is a live dict key in `eht_predictions()`, `test_F186_shadow_raytrace.py` T2 asserts on it, and it is a key in a committed baseline. The ledger note went from "STALE, flagged for P6" to "RESOLVED at C6."

> **Acceptance gate P6:** every non-deprecated kernel is reachable from a channel or a compute-once wrapper, and `code-index.md`'s generated reach column shows it. **Forks are exempt by definition** — a rejected fork not being channel-driven is the point.

---

## 5. Sequencing

```
        ┌── P1r.2 (drift decisions) ── do BEFORE P3, so a new drift is distinguishable
        ├── P1r.1 (import-time work)  ── independent, mechanical
        │
DONE ───┼── P3.1 spike ✓ F267 (√3 / BZ measure — no doubler, D1 safe)
P0      │      └─> P3.1 ──> P3.2 ──> P3.3 ──> P3.4 ──> P3.6 ──> P4 ──> P5
P1−P1r  │             │       (clock)  (bus)  (T^μν) (gravity)
P2.1−4  │             └─> P3.5 (total energy)  ── PULL FORWARD: needs only the
B6      │                                          energy-convention decision
P2.5−7  │
        │
        └── P6 ── fix its own instrument first, then kernel coverage; parallelisable
```

*P3.7 (multi-scale Regions) is deliberately off this diagram — it is the cut line.*

- **P0, P2.1–P2.4 and B6 are done; P1 is done bar P1r.** Nothing is blocked on foundations any more, which is the whole point of having spent C0–C9 on them. P2's *acceptance gate* is still NOT MET — P2.5 and P2.6 were never started and the throughput multiple was never benchmarked.
- **P3.2–P3.6 are done (2026-08-01).** The engine owns physical time, channels exchange typed quantities over a declared graph, there is one energy convention with a gated machine-class total, and the gravity loop is closed on the gauge side at eikonal order. Every behaviour change is opt-in per scenario, so no committed baseline moved.
- **P3.1 is now the critical path, and it is all that is left of P3 bar the cut line.** Its spike is closed (F267): the photon is safe and D1 stands, and the phase inherited a new per-observable audit (P3.1 item 5). Next is F265's five cubic layers, each a self-contained finding — `hypercharge` (2D→3D BCC) and `bgfield_loop` (the fix already exists in `make_kgrid_bcc`, unapplied) first.
- **Two of the three items that fell out of P3.2–P3.6 are now closed (2026-08-01).**
  - **Ordering violations — resolved, and 4 of 5 were false positives.** The quarks consume the bag via `confine: {field: bag}`, so bag↔quark is a genuine leapfrog cycle and the declared order is correct; syncing them would have converted a leapfrog into a lag. An exhaustive audit found the detector was missing **45 edges across four key paths**, so `build_graph` now resolves references *structurally* (any config string naming a sibling), not from a curated key list. Cycles 13 → 16, violations 5 → 1. The survivor, `unified_hydrogen_free`, is **vacuous**: its matter publishes no currents, so the edge carries no payload and both orders are bit-identical. F269.
  - **The gauge-side dielectric coupling — resolved, k-resolved, no free parameter.** `photon_step_dielectric` lifts the audited variable-c Strang split to the 3-D (E,B) pair, with two derived corrections (Weyl operator ordering; the h² term). Uniform K is **exact** (4e-15), convergence exponent **2.00**, norm drift converges instead of plateauing, ω₀ eliminated. **F271**, ledger S10.
- **Still unstarted:** promoting the **18 desynchronised scenarios** from `legacy` to `strict` (the EM sector speeds up 10× relative to matter — F268); the **deflection coefficient** against GR's 4GM/c²b, which needs the F64 fork's battery rather than a gate test (F271 §5); and the fact that **both defects F271 fixed are also present in `lattice.curved._half_step_dH`**, hence in every fork variable-c result.
- **P2.6 is cheap and prevents data loss.** Do it before the first multi-day run, not after. The `blockspin_schedule`-dropped-on-resume bug is a one-line fix that currently makes long resumed runs silently wrong.
- **P2.7 is small and is a correctness hole, not a performance one.** An opt-in complex64 path with no gate and no test is the one thing in the numerics layer that could quietly violate the $10^{-12}$ product.
- **P6's first task is its own instrument** — make `code-index.md`'s Reach column agree with the module graph before using it to measure anything.
- **P1r.1 is independent** and pays for itself as soon as the suite grows.
- **P4 and P5 follow P3** — no point hardening a schema for an architecture still in motion. Two P4 items are exceptions and can land any time: **strict schema validation** and **per-channel seeds**.
- **P6 is background work.**

**Critical path: P3.1 → P4 → P5.** P3.2–P3.6 are behind us, so the engine no longer moves under P4's feet; the remaining risk in P3 is entirely B1, the topology partition. Everything else can slip a session without moving the end state. **P3.7 remains the cut line.**

---

## 6. Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **BCC photon loses exactness.** | **Downgraded from High to Low** | F265 established the gauge *propagators* were always BCC; F250 gives the all-$k$ gauge pole with a unique BZ zero. The residual risk is in the four cubic *action* layers, where F265 already showed both actions share an exact continuum limit. Still: record a negative result as a finding rather than accepting a degraded photon |
| **The four *portable* layers turn out to be entangled** — LPT, the BZ fold, the MC actions and 2D hypercharge (items 1–4 of F265's five; item 5 is a derivation question, not a layer) may not be independently portable | Medium | Each is separately testable, and F265's §6 rank count gives an exact target (the composite resolves $2N_s$ of $3N_s$; a correct port resolves $3N_s-3$). Take them one finding at a time |
| **A P3 change breaks a verified result silently** | Medium | Much lower than when this was written. HEAD is the baseline, `make drift` is green, 350 records have declared failure modes, and `casim test --param` sweeps without writing a baseline. The remaining exposure is the **28 undecided drift FAILs** — decide them (P1r.2) *before* starting P3, so a new drift is distinguishable from an old one |
| **P1r.1 (320 files) breaks something** | Medium | Strictly baseline-first, one file at a time — the original P1.3 discipline. The registry now names an entry function per record, so the target shape is unambiguous |
| **The device backends never get validated** | Medium | Neither MLX nor CuPy has run on real hardware. Until one clears the equivalence contract, D4 is a protocol claim, not a capability. Run `make install && make backend BENCH=1` on the Apple Silicon machine — that is where the P2.1/P2.4 throughput number actually comes from |
| **Scope. P3 is very large.** | Medium | P3.1–P3.6 are separately shippable; **P3.7 is the cut line** |
| **The JAX path is used before P2.7 lands** — `use_jax(True)` silently drops the W propagator to complex64 with no gate and no test | Medium | Do P2.7 first, or make `use_jax` raise until it is registered. This is the only place in the tree where opting into a device silently changes the precision class |
| **P6 is measured against the wrong artifact** — `code-index.md`'s Reach column has 2 of 5 categories and disagrees with the graph by 3 modules | Low | Fix the instrument before the coverage work; it is a one-source-of-truth problem, not a physics one |
| **Concurrent-session collisions** | Low but recurring | Happened at F110, F129, F262, and again during C1 (two sessions editing the same 25 kernels). `casim index` now refuses a duplicate finding number, and duplicates are at **0**. Claim a sector before starting |

---

## 7. What this roadmap does not change

- **No physics decisions are reversed.** CLAUDE.md's seven core design decisions stand. D1 is an *engineering* decision to make BCC canonical in the software; it is downstream of F91/F175/F264/F265, not a new claim.
- **The exactness bar does not move.** `exact` and `machine` keep their meanings; complex128 throughout; the $10^{-12}$ gate is the product, not a tunable — and it is now the reason no device backend may auto-activate.
- **Superseded work is preserved, not deleted.** F50/F52/F62, F114, the σ-bilinear photon, the chiral gluon, F179/CN3 and the composite-SC field strength all stay checkable — in `tier: archive`, in `deprecated/code/`, or as explicitly-banner'd comparison objects. That is how the supersessions stay honest.
- **Forks keep their falsification value.** A rejected fork is a recorded negative result, not dead code — which is why P6's acceptance gate exempts them.
- **What D2's reversal did *not* change:** the kernels' authority over their own physics. D6 moved 171 files and changed no result; every migration was proved against a committed baseline and rolled back on drift.

---

*Cross-references: `docs/theory/key-decisions.md` §"Engineering decisions" (D1–D11), `docs/theory/supersessions.yaml`, `docs/roadmaps/roadmap-casim-consolidation.md` (C0–C9, **complete**), `docs/status/{P0,P1,C0,C1,C2,C3,C4,C5,C6,C7,C8}-completion-overview.md`, `docs/status/C9-readiness.md`, `docs/status/baseline-provenance.md` (the drift decision queue), `findings/F265-bcc-gauge-action-blindness.md` (which re-frames B1), `docs/roadmaps/roadmap-unified-real-space.md` (F134–F137 arc, which P3.7 subsumes), `scenarios/RUN-GUIDE.md`, `src/casim/README.md`.*
