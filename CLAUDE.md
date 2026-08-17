# Your Role

You are a research assistant helping design a cellular automaton model that mirrors known, or theorized, particle physics.

# Core Idea
We are attempting to construct a "universe in a bottle", if our universe is a cosmic lattice of cellular automata, or one single tremendous one, then we should be able to model it on a tiny scale on a computer. That is the goal.

## Core Design Decisions
1. We are using Ludwig's SU(2) derivation instead of the standard model. 
2. From finding 25 and 26: 
> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf{E}, \mathbf{B})$ vector pair per unit of spatial wavenumber:
>
> $$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}$$
>
> where $\Omega = 2\omega(|\mathbf{k}|/2)$ is the rotation angle the $(\mathbf{E}, \mathbf{B})$ pair traverses per CA tick.
3. Hypercharge is included on U(x), avoiding any need for the Higgs field.
4. Gravity (Finding 64 → **F178**): the canonical/fundamental law is the **induced Einstein equation** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ (full stress-energy source; structural $G=a^2c^3/(8\pi\sqrt3\,\hbar)$, F79/F107). The single impedance-matched lattice **dielectric** $K=\exp(2GM/rc^2)$ ($A=1/K,\ B=K$, $AB\equiv1$) — the EM-connection route, *not* the rest-mass-sourced metric of F50/F52/F62 — is the **vacuum/weak-field representation** of that law: PPN $\beta=\gamma=1$, GR-identical (D-EM9), plus the emergent rotation-rate origin story. It is **not** the field equation inside matter: a single scalar forces anisotropic stress (F173), so with the full-tensor source the interior metric carries its second function and the dynamics are GR/TOV. Reclassified by F178: the energy-only $\nabla^2\ln K=-8\pi T^{00}$ (F106) is the static weak-field reduction, and the exact vacuum solution is Schwarzschild (the exponential $K$ is PPN-order only), so the F114 horizon-free black hole is superseded. Decision recorded in `docs/theory/key-decisions.md` and F178.
5. Photon (Findings 67/68/69): the electromagnetic photon is the **paired-spinor photon** — a bound pair of two spin-½ Weyl quanta ("only occurs as a pair"), each carrying $k/2$ on opposite chiral branches, so the pair rate is the helicity-symmetric $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$. It is massless, luminal ($c=1/\sqrt3$), transverse, and **non-birefringent** (`ca_photon_pair.py`; propagator = even law `ca_wmu._f26_rotation_step`), and is the identity channel that U(1) minimal coupling forces (F68). This **supersedes** the composite $\sigma$-bilinear photon of `ca_maxwell.py` (helicity↔branch, birefringent → excluded by GRB/AGN polarimetry, F65/F66/F67); the $\sigma$-bilinear *field construction* is retained only for the massive/non-Abelian sectors (W/Z/gluon), which are not under the polarimetry bound. **Propagator classification (F91, 2026-06-04):** the even-vs-chiral rotation law is set by the branch structure of each coupling — γ even (forced), W± chiral (forced; left-projector coupling, right-branch weight ≡ 0), Z even for its vector part with a mass-suppressed axial split, gluon **even** (forced; colour coupling is branch-blind). The BCC gluon propagator was migrated chiral→even on 2026-06-04 (`gluon_rotation_step_spectral_bcc`; the old chiral step retained as `gluon_rotation_step_spectral_bcc_chiral`).
6. We are operating under the philosophy of elegant design, that the universe can both be completely understood, and is elegant and simple in it's construction. 
7. Lepton shape-angle — **weight-as-phase is a founding principle** (F253/F255/F256, 2026-07-16): the charged-lepton condensate angle equals the second-shell $E_g$ **representation weight**, $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad (exact $O_h$, F175) — the canonical $E_g$-plane angle **is** the weight it carries. $\delta^*=\tfrac29$ is **primary**; the sextic clock coupling $\lambda_6=0.243$ (equivalently $W=6\lambda_6=1.46$) is an **output** via the F234 arrow $\lambda_6=|B|/(2e^6\cos\tfrac23)$, not a fit. Adopted because every alternative is closed: the angle is a genuine radian with $R{=}1$ forced by Schur-isotropy of the $E_g$ irrep metric (F255, derived not posited); a scale-free topological origin is excluded (F253, only holonomy is $2\pi/3$); and the dynamical Landau route cannot give exact $3\delta^*=Q$ (F256, independent sea-$B$/induced-$C$ origins ⇒ $1.7\times10^{-5}$ near-coincidence). The whole charged-lepton shape then follows from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ to $\le0.007\%$ with zero shape parameters. Supersedes F179/CN3. Decision recorded in `docs/theory/key-decisions.md`.
 
## Project Structure

**CASIM is the program** (decision **D6**, roadmap C9, 2026-07-31). There is one tree. The old flat-kernel directory and its 171 deprecation shims are **deleted** — every physics module now lives under `src/casim/engine/`, by sector, on the BCC base layer. Nothing imports a bare `ca_*` name; `docs/design/module-migration-manifest.yaml` maps all 171 old paths to their new ones if you meet a stale reference.

See `INDEX.md` for the full annotated map. In brief:

- `src/casim/` — **the whole program**
  - `numerics/` — **D8**: the only place numpy/scipy/FFT are imported. `from casim.numerics import xp, fft, linalg, rng`. `backends/` holds the device implementations.
  - `constants/` — **D7**: owns *values*, not just provenance. Import constants, never write literals.
  - `engine/` — **five sectors, and the sector is the directory.** Inside a sector, module names carry a **subsector prefix** (`qed_*`, `qi_*`, `running_*`, `gravity_*`, `lpt_*`, `blockspin_*`, `colour_*`, `derive_*`, `run_*`) so a flat directory stays readable. Follow the existing prefix; do not invent a sixth sector.
    - `core/` — the engine spine: `simulation`, `channel`, `channels`, `coupled`, `observers`, `tier3`, `spectral_matter`, `blockspin`, `entanglement_register`, `manybody`, `lpt_generator`, `_viz_*`
    - `lattice/` — `bcc.py` (**canonical base layer**), geometry, core, core_exact, blockspin*, multigrid, poisson_open, curved, si_scale. The simple-cubic/square code lives in `core.py`, `core_exact.py` and `geometry.cubic()/square()`, each banner-labelled **reference implementation, continuum-limit regression target, not canonical (D1)** — the extraction into a separate `cubic.py` is still open (C3.3 deferred it: a code *split* is not a file *move*), so **there is no `cubic.py`**
    - `gauge/` — `photon.py` (paired-spinor, **the** photon), `bilinear.py`/`bilinear_2d.py` (σ-bilinear construction: **W/Z/gluon only**, never the photon — F65–F69 banner is load-bearing), `weak*`, `hypercharge`, `charged_current`, `chiral_anomaly`, `gluon*`, `strong`, `su3_ladder`, `colour_*`, `confinement`, `cooling`, `link_hamiltonian`, `bcc_action`, `propagator`, `rotation`, `emission`, `minimal_coupling`, `charge_coupling`, `lpt_*`
    - `particles/` — `dirac`/`dirac_bcc`, `second_quant`, `baryon*`, `meson`, `nuclear*`, `atom`, `element`, `positronium`, `hyperfine`, `majorana`, `higgs`, `eg_sextic`, `induced_stiffness`, the `derive_*` lepton-shape/PMNS scripts, `_results_path`
    - `interactions/` — `gravity*`, astrophysics (`blackhole`, `qnm`, `inspiral`, `horizon_entropy`, `interior_metric`, `tolman`, `ns_eos`, `stellar`, `cosmology`, `darkmatter`, `raytrace`), `qed_*` (13), `running_*` (7), `qi_*` (5), `superconductivity`, `slowlight`, `vacuum_energy`, `unified`, `derive_*`
    - `forks/<sector>/` — the 47 recorded alternatives (`gravity/`, `gauge/`, `lattice/`, `particles/`, `electroweak/`, `darkmatter/`). A fork is a *tested and rejected* or live-exploratory branch; it preserves the falsification record and is **not** dead code. Loaded by file path or bare name, never as a package submodule — `import casim` puts `casim.FORK_DIRS` on `sys.path`; a **subprocess** that runs a fork must be handed `PYTHONPATH=src` explicitly.
    - `registry.py` — **D11**: the *single* module registry (name, path, sector, findings, exactness, reach, `reachable_from`, tests, results, role, status, origin). `casim index` consumes it. There is **no** per-subpackage registry — see §"Adding or changing an engine module".
  - `suite/ analysis/ io/ gui/ viz/ tests/ index/ cli.py` — the program layer
  - `lattice/ fields/ gravity/ particles/` (top level) — thin compatibility re-export packages; new code should import from `casim.engine.*` directly
- `tests/` — `registry/` (**D9**: `*.yaml`, one declarative record per test — the single specification), `casim/` (gate tier, default `pytest` target — but pytest misses the 3 `scenario` gate records; `make gate` is the barrier), `findings/` (test_F*.py), `priority/` (GR/QM/QFT battery), `runners/` (standalone run_* scripts), `falsification/` (spec briefs)
- `test-results/` — JSON result dumps, markdown summaries, and `figures/` (single merged location)
- `findings/` — one markdown file per physics finding (`F{N}-name.md`)
- `docs/claims/` — **D12**: one card per claim the project currently asserts (`CL{NNN}-slug.md`). See §"Claims" below; this is a *different object* from a finding and the distinction is load-bearing
- `papers/` — the paper series + claims/falsifiers summary
- `docs/` — everything else, by purpose: `theory/` (incl. `key-decisions.md`, `supersessions.yaml`), `roadmaps/` (incl. `next-steps.md`), `status/` (`project-status.md`, `changelog.md`, `exactness-inventory.md`), `audits/`, `design/` (incl. `module-graph.json`, `module-migration-manifest.yaml`)
- `references/` — external PDFs and research-summary markdown files only
- `scenarios/` — CASIM scenario YAMLs + RUN-GUIDE
- `tools/` — maintenance scripts. `run_gate.py` (the barrier), the `audit_*` ratchets (constants/numerics/tests) and `check_*` gates (`check_test_registry`, `check_module_registry`, `check_result_drift`, `check_deprecated`, `check_claims`), `gen_module_graph.py`, `gen_test_registry.py`, `gen_manifest.py`, `find_dead_code.py`, `arm_test_registry.py`, `triage_baselines.py`, `apply_supersession_banners.py`. The twelve migration-era tools (`migrate_module.py`, `gen_migration_manifest.py`, `route_numerics.py`, `check_shim_imports.py`, the `_c5_*` one-shots) were **retired to `deprecated/code/` at C9** — their subject no longer exists
- `deprecated/` — `code/` (the pre-clean original of all 171 migrated files, plus the retired migration tools), `tests/` (retired tests, each with a ledger reason), and superseded docs/plans. See its README for why each item landed there
- `.vendor/` — pre-installed sandbox Python packages (git-ignored); see below

## Sandbox Python dependencies (scipy / numpy / pyfftw / pytest)

Do **not** `pip install` these in the sandbox — proxy downloads are slow/flaky and
fail. They are already vendored in `.vendor/` (CPython 3.10, Linux aarch64). At the
start of any bash session that needs them, activate via `PYTHONPATH` — no download:

```bash
source "$PWD/.vendor/activate.sh"      # run from the repo root
python3 -m pytest tests/casim -q       # note: use `python3 -m pytest`, not bare `pytest`
                                       # (smoke check only — this misses the 3 scenario gate records; `make gate` is the barrier)
```

Equivalently: `export PYTHONPATH="$PWD/.vendor/py310-linux-aarch64:$PYTHONPATH"`.
Offline reinstall / adding packages: see `.vendor/README.md`. If a new package is
needed, add its cp310-aarch64 wheel to `.vendor/wheels/` first, then install with
`--no-index --find-links .vendor/wheels --target .vendor/py310-linux-aarch64`.

## Context

### Always load (small, always relevant)
- `INDEX.md` — master map: every directory, what lives in it, which index covers it
- `findings-index.md` — one-line index of all findings (~3k tokens). Search this first; then read only the specific `findings/F{N}-*.md` files you need.
- `project-status-index.md` — one-line per milestone (~1.4k tokens). Read full `docs/status/project-status.md` only if you need narrative detail on a specific entry.
- `tests-index.md` — test ↔ finding ↔ results-JSON map, generated from the test registry (so it is exact, not heuristic); check before writing or hunting for a test
- `code-index.md` — one row per engine module with its sector, findings, exactness class, reachability and test dependents (from the module registry, **D11**)
- `claims-index.md` — one line per claim card: what the project asserts *right now*, its status, and whether it has a falsifier (from `docs/claims/`, **D12**). **Read this before writing that the model "predicts" or "shows" anything** — a finding may be superseded without any claim changing, and a claim may be narrowed without any finding changing
- `docs-index.md` — one line per theory doc, paper, and reference summary
- `tail -n 150 docs/status/changelog.md` — recent changes (do NOT read the whole file; it is ~100k tokens)
- `src/casim/README.md` — CASIM documentation
- `scenarios/RUN-GUIDE.md` — scenario handles and benchmark speeds
- `docs/theory/key-decisions.md` §"Engineering decisions" — D1–D12 in one place; read before restructuring anything

### Load only when directly relevant (large — load targeted sections)
- `references/physics-notes-complete.md` (~44k tokens) — full theory notes; load only if the question requires foundational derivations not in a finding file
- `references/t-hooft-2015-cai-summary.md`
- `references/mohr-2010-maxwell-photon-wf-summary.md`
- `references/ostoma-trushyk-1999-summary.md`
- `references/qca-papers-1-4-overview.md`

### Finding files
Individual findings are in `findings/F{N}-name.md`. Use `grep -i "keyword" findings-index.md` to locate relevant ones, then read those files directly. Do not read all findings at once.
  
## How to work in the repo (post-C9 methods)

**Everything runs through `casim` or `make`.** `PYTHONPATH=src` is all the path setup needed — the Makefile exports it, and `tests/conftest.py` sets it for pytest.

```bash
make gate                      # THE barrier: provenance + ratchets + indexes + package suite. <2 min. Green before and after any change.
make indexes                   # = casim index — regenerate every index from the registries (C8)
make claims                    # = casim index --only claims + check_claims.py — the claim cards (D12)
make drift                     # numeric drift in result artifacts vs git HEAD, after re-running physics
make health registry numerics   # the ratchets: suite health, test-registry coverage, D8 compliance
make control                   # D9/H2 — run every declared negative control, require it to go RED (then commit the journal)
make control-todo              # gate-tier assertions with no control yet, with hints
make structure                 # module graph -> dead-code proposal -> deprecated/ accounting
```

**Tests are registry records, not scripts (D9).** `tests/registry/*.yaml` is the single specification and `casim test` is the only runner. `pytest` sees most of the gate tier but **not all of it** — see the barrier note below.

**`pytest` is not the barrier; `make gate` is (V-004, audit 2026-08-01).** Measured 2026-08-02: the gate tier holds **27 records** (24 `assertion` + 3 `scenario`). Bare `pytest tests/casim` collects **24** of them — 23 as ordinary test files, plus any entry-driven record routed through `tests/casim/test_registry_entries.py` (today exactly one, `F276-curved-weyl-ordering-second-order`). The three it **cannot** collect are `scenario-bcc-weyl`, `scenario-gluon-bcc` and `scenario-photon-pair`: `kind: scenario` records have `path: None` because they are YAML runs gated by `expect:`, and pytest has no way to reach them. Those three are precisely the records that run the engine on a lattice, i.e. the *physics* gates in the gate tier.

So: run `make gate` (which invokes `casim test --tier gate`) before and after any change. A green bare `pytest` has skipped the three physics gates and does not clear the barrier.

```bash
casim test --tier gate                 # the gate tier in full — a superset of what `pytest` collects
casim test --finding F234              # every record verifying one finding
casim test --sector lepton --kind assertion
casim test --id F234-Wvc-triple-closure
casim test --param delta_star=2/9      # re-run a record at a perturbed value and report the drift
casim test --control --tier gate       # verify the declared negative controls instead of running the records
casim test --scale smoke               # the full grouped battery (hours, not minutes)
```

A new test is a **record**, not a file that executes physics at import. Give it a `module:`, an `entry:` function, `params:`, a `kind:` and an `expect.exactness`. `legacy_script` is declared debt and is ratcheted down — do not add to it.

---

## Claims — the standing rule (decision D12)

> **Any algebraic or physics-tested claim or element that extends, derives, or contradicts anything in quantum mechanics, the Standard Model, general relativity, or special relativity gets a card in `docs/claims/` and a row in the registries it touches.**

The bar is *extends established physics*, not *is interesting*. An engine-wiring result, a numerical technique, a refactor or a status record does **not** get a card — and where a finding is judged not to clear the bar, that judgement is itself recorded (`docs/audits/consolidation-plan-2026-08-04.md` §5), so "no card" is a decision rather than an omission.

**A claim is not a finding, and confusing them is the failure this layer exists to prevent.**

| Object | Question it answers | Tense |
|---|---|---|
| `findings/F{N}-*.md` | What did we do, and what came out? | past — written once, superseded rather than rewritten |
| `docs/claims/CL{N}-*.md` | What do we assert, right now, and what would kill it? | **present** — narrowed, made contingent, or withdrawn as the model moves |

A finding that says `**Status:** Confirmed — 5/5 PASS` is *correct to keep saying that* even after the ledger supersedes it: it records what a session concluded. The **claim** resting on it is what has to move. Sixteen findings in this repo are named in a `superseded:` list while their own headers still read "Confirmed" — that is not a defect in the findings, it is the gap the cards fill.

### Writing or changing a card

1. **Copy `docs/claims/TEMPLATE.md`.** Take the next id from `next_claim` in `docs/claims/registry.yaml`. `CL` is its own namespace and does not overlap `F<N>`, `D<N>`, `S<N>` or `C0`–`C9`.
2. **Fill the front matter from the closed vocabularies** — `docs/claims/README.md` has each one with its meaning. There is no `unknown`: a claim whose status cannot be determined is `open` **with the gap named**, which is a state someone can act on.
3. **State the claim so a reader who disagrees knows what they are disagreeing with.** Numbers verbatim from the source; no rounding, no "approximately" the source did not say.
4. **`falsifier: none` requires the structural reason to be named in the section.** "Structural" is a reason only when the structure is named. Otherwise it is `unset`, which is ratcheted debt.
5. **`make claims`** (= `casim index --only claims` + `check_claims.py`), then `make gate`.

### What a card may and may not change

Writing or editing a card **never** edits a finding, a physics module, a test record, the exactness inventory or the supersession ledger. If the position changed because the *physics* changed, that is a research session with its own claim on `docs/design/session-claims.yaml` and its own finding number; the card is updated to match afterwards.

The inverse is the point of the layer: **a finding may be superseded without any claim changing, and a claim may be narrowed without any finding changing.** Neither event is visible in the other object.

### What the gate enforces

`tools/check_claims.py` runs in `make gate`. Closed vocabularies, unique contiguous ids, filename == `{id}-{slug}.md`, every `findings:` entry resolving to a real file, every backticked repo path existing, `rolls_up_to` resolving, withdrawn cards keeping a non-stub retraction record, and the three debt ratchets (`unreviewed-seed`, `falsifier: unset`, `exactness: unset` — these may fall, never rise).

**The rule that does real work:** a card with `status: live` **fails** when *every* finding it rests on is named in a `superseded:` list in the ledger. That is the machine-checkable form of "overstated". It deliberately does **not** fire on a *partial* supersession — the standing lesson of this repo is that almost nothing here is superseded wholesale (of 14 test files one audit called superseded, exactly one was), and a check that flagged partials would train people to ignore it.

### Do not archive the falsification record

`kind: no_go` cards and `status: withdrawn` cards are the **last** things that should ever leave the tree. A withdrawn claim that is deleted is a claim that gets re-made — CL023–CL027 are the horizon-free black hole and its four dependent falsifiers, published live between 2026-06-08 and 2026-08-02, and each card's `## Status & history` **is** the retraction record. A gate test asserts they survive. The same applies to negative results in `findings/`: they describe themselves in the vocabulary of obsolescence ("a four-avenue no-go", "$d=6$ and $d=9$ excluded"), so any keyword sweep for dead material surfaces them first and most confidently. **Do not run one.**

---

## Building or changing a module — the five module-side registries

Everything below is enforced by `make gate`. Skipping a step does not produce a silent inconsistency; it produces a red check that names the file. The order that works is **write → register → test-record → `make indexes` → `make gate`**.

### 1. The module registry (D11) — `src/casim/engine/registry.py`

**There is exactly one module registry, and it is not per-subpackage.** It is populated from two sources:

- **`origin="manifest"`** — the 171 migrated kernels, read at import from `docs/design/module-migration-manifest.yaml`. That manifest is now a **frozen historical record**: its generator (`gen_migration_manifest.py`) was retired at C9 along with `migrate_module.py`. Do not add a record to it, and do not expect it to grow.
- **`origin="spine"`** — the hand-declared `_SPINE` tuple at the bottom of `registry.py`. **Every new module goes here.** `check_coverage()` walks the sector tree, so a new `.py` under `engine/<sector>/` with no record turns `make gate`'s module-registry check red immediately.

```python
# in _SPINE, src/casim/engine/registry.py
Module("gauge.my_thing", "src/casim/engine/gauge/my_thing.py", "gauge",
       findings=("F267",), exactness="exact", reach="driven",
       reachable_from=("photon_pair",), role="kernel", origin="spine"),
```

`sector` must be one of `core lattice gauge particles interactions forks numerics`; `exactness` (when set) must be in the closed `EXACTNESS_CLASSES` vocabulary; `status` carries `live | partial | fork_live | fork_unclaimed | dead_candidate`. Check with `make registry` and `python3 tools/check_module_registry.py`.

**Reachability is a query, not a survey** — `[m.name for m in reg.all_modules() if m.reach != "driven"]`. `make graph` regenerates `docs/design/module-graph.json`, which is where `reach`/`reachable_from` come from; run it after wiring a module into a channel.

### 2. The constants registry (D7) — `src/casim/constants/`

One module per sector (`geometry gravity lepton strong electroweak`) plus the `Constant`/`Site`/`MeasuredConstant` types in `__init__.py`. The **exported Python name is the registry symbol** — `_export()` generates the import surface, so a constant cannot be registered and then forgotten at the import line.

```python
from casim.constants import c_lat, G_LATTICE, delta_star, delta_star_f, endpoint
```

Rules that the gate enforces, and the reasoning behind each:

- **Exact constants resolve from closed form, never a decimal.** `√(8π)·3^(1/4)`, `1/√3`, `1/(72π)`, `Fraction(2, 9)`, `6·λ₆`. A truncated literal is a defect; C2 recorded the two it fixed and the 5×10⁻⁷ they moved.
- **A rational constant exports the `Fraction` under its symbol and a float under `<symbol>_f`.** Use the `Fraction` for exactness assertions and `sp.Rational` sites; use `_f` in array code (a `Fraction` in a numpy expression yields an object array). Getting this backwards silently downgrades an exact check to a float one.
- **Bracketed constants export no scalar.** `alpha_eff_star` requires `endpoint("alpha_eff_star", "lo"|"hi")`. A midpoint is a display convenience, never a result.
- **Values that coincide stay separate constants.** 2/9 is three unrelated constants (`delta_star`, `sin2_thetaW_onshell`, `c_fierz_colour`); `f_pi` is three; `cos3δ*` is two; 1/√3 is two (a speed and a momentum scale). Merging any of them turns a prediction into an input, and a test asserts the three-fold 2/9 split cannot be collapsed.
- **Every constant needs a `provenance` finding, an `exactness` class and a `derivation` string.** `register()` raises without them.
- **No unregistered literal may match a registry value.** `make constants` is the polarity-flipped sweep ("does any unregistered site exist?"); `make constants-report` names every rogue with its line and its candidate symbols. It deliberately reports *every* symbol a value could be and never picks one.
- **If a module must *compute* the number because that derivation is the physics under test**, declare a `MeasuredConstant` — kind `measured` (same quantity, different regime) or `coincidence` (different quantity, same number) — with a mandatory `reason`. Rewriting such a site to import the registry deletes the result it was measuring.
- **Record your `Site(path, name, kind=...)`** when a module binds a constant. `kind="import"` is asserted to be true, so a moved or renamed file must have its sites repointed — that is what went red for C5 and C6 after their migrations.

### 3. The test registry (D9) — `tests/registry/*.yaml`

One YAML per sector; `src/casim/tests/registry.py` loads them. `casim test` is the runner. `pytest` reaches the registry two ways — file-based `assertion` records by ordinary collection of their `path:`, and entry-driven records through `tests/casim/test_registry_entries.py`, which parametrises over `select(tier="gate")` records that name an `entry:` (`tests/conftest.py` hides those files so nothing runs twice under two contracts). **`kind: scenario` records have no `path:` and no `entry:`, so pytest cannot see them at all** — that is the 27-vs-24 gap in V-004. Use `casim test --tier gate` when you need the whole tier.

Field ownership matches the manifest convention: **`evidence:` is generated** and rewritten by `make registry-gen` on every run; **every other field is human-owned** and preserved across regeneration, keyed by `path:`.

```yaml
- id: F234-Wvc-triple-closed
  path: tests/findings/test_F234_Wvc_triple_closed.py
  kind: assertion            # assertion | result_dump | scenario | legacy_script
  tier: gate                 # gate | battery | archive
  sector: particles
  findings: [F234]
  module: casim.engine.particles.derive_lambda6_sextic
  entry: check_triple_closure
  params: {delta_star: 2/9}
  expect: {exactness: exact, tol: 0}
  results: [test-results/F234_Wvc_triple_closed.json]
```

- **`validate()` refuses a record with no failure mode.** A `legacy_script` is *labelled* debt; anything else must be able to fail. There is no third state, which is what closed P1's "RAN limbo".
- **A gate-tier `assertion` record declares a `control:` — a perturbation under which it MUST go red (D9/H2, 2026-08-07).** `validate()` refusing a record with *no declared failure mode* does not establish that the declared one can trip; F22's headline check was `x − (1 − 2(1−x)/2)`, identically zero for any expression, and it was green for months. A control names the perturbation and the legs it reddens:

```yaml
  control:
    - params: {linear_control: true}      # applied exactly as `casim test --param` would
      reds:   [G10-3, G10-4, G10-5, G10-6]   # these MUST go red; leg tags, resolved against the payload
      reason: dispersion replaced by exactly linear c|k|, so every lattice correction must vanish
      # only: false      # opt out of "and nothing else goes red", and say why in reason
```

- **Whether a record CAN fail is measured, not inferred — `make can-fail`.** Never decide it by reading the code or an AST: a dispatch table (`for name, fn in CHECKS: fn()`) presents one Call node on a loop variable, and that alone made three records read as "cannot fail" while they held 41, 39 and 30 reachable asserts (completeness Amendment 3). `casim.tests.runner.probe_can_fail` traces a real run and reports which `assert`/`raise` lines executed, plus whether the payload carries a verdict key — both are failure routes. Journalled to `test-results/can-fail.json` (**commit it**); `check_finding_records.py` prefers the measurement over its own static walk and says which answered. A timeout is **INCONCLUSIVE**, never cannot-fail. If you need to know whether a check can fail, **break it and watch**: import the module, corrupt one dependency it asserts on, confirm `AssertionError` propagates. Three lines, decisive.
  `make control` runs them and journals the verdicts to `test-results/control-soundness.json` (**commit it**); `make gate` then checks *statically* that every control is well-formed and carries a `CONTROL` verdict at the current code **fingerprint**, so touching a driver turns the gate red naming the record. Verdicts are `CONTROL` / `LEAK` (perturbation applied, still green) / `SPILL` (reddened legs it did not declare) / `INVALID` (leg absent, already red, or the driver crashed instead of failing) / `NOCTRL` (debt). **Write the MEASURED set into `reds:`, not the set you expected** — the seeding pass corrected two findings' own prose this way. A record with no control is counted debt (`gate_assertion_no_control`, ratcheted to zero); `make control-todo` lists them with the keyword arguments each entry point already accepts.
- **`sector` uses the module-sector vocabulary**, not a physics grouping. The physics grouping is `--finding`, which is exact rather than inferred.
- **A `result_dump` record fails by baseline diff against git HEAD.** Declaring the artifact is what arms it — but a promotion is only *proved* when a run actually rewrites that file; the runner's mtime guard reports the rest as `SKIP`, never a false `PASS`. `tools/arm_test_registry.py` does that pass and journals every verdict.
- **After any arming or sweep run: `--restore`, then `--apply`.** An arming run rewrites committed baselines in place, and forgetting `--restore` leaves modified baselines the strict drift checker will flag.
- **A sweep never writes a baseline.** `casim test --param k=v` runs in a temp dir and diffs in memory.
- **Baseline drift below 1×10⁻¹² is the `machine` floor, not a change.** The runner reports sub-floor deltas separately; `tools/check_result_drift.py` runs strict at 1e-15 and will disagree. Only `expect: {strict_floor: true}` overrides.
- **A baseline that is out of date *because the physics improved*** goes in `docs/theory/supersessions.yaml`'s `baselines:` block as `stale_by_design` (reports `STALE`, needs `clears_by:`) — not as `candidate`, which still reports `FAIL` on purpose so the category cannot become a parking lot. `tools/triage_baselines.py` splits the queue; `docs/status/baseline-provenance.md` is the standing decision list.

### 4. The numerics façade (D8) — `src/casim/numerics/`

```python
from casim.numerics import xp, fft, linalg, rng, chiral
```

No physics module imports `numpy`, `scipy`, or an FFT library directly; `make numerics` ratchets the count and `LIST=1` names the offenders. What is there:

- `fft` — `fftn/ifftn/fft2/ifft2/fft/ifft/rfft/irfft`, plus **`rfftn`/`irfftn`** (use them for real-valued **E** and **B**; a full complex transform on real data is wasted work).
- `linalg` — `batched_matmul` (BLAS `zgemm`; **not** bit-identical to `np.einsum` — 1–2 ULP, measured and documented, four orders below the floor), `dagger`.
- `rng` — one independent stream per named consumer, so adding a channel does not perturb every other channel's numbers.
- `chiral` — `cmul` / `su2_apply` on **explicit real pairs**. This is the hand-written answer to the standing chiral-transform hazard; the equivalence contract asserts both components survive.
- `backends` — numpy / scipy / pyfftw / cupy / mlx, one registry. `CASIM_BACKEND=pyfftw` selects at startup.

`np.fftfreq`/`rfftfreq` deliberately stay on numpy (index arithmetic, no transform). **`xp` is honest**: it is the array namespace and today it *is* numpy — a name to move to now, with real dispatch later. **Precision holds at complex128**; MLX is float32-backed and refuses to activate without `CASIM_ALLOW_FLOAT32=1`, because the 10⁻¹² gate is the product, not a tunable. Cache k-grids and unitaries keyed on `(shape, sign, block)` and mark cached arrays read-only — that is the `_weyl_cache`/`_disp_cache` pattern, worth ~1.8×.

### 5. Result artifacts and paths

- **Never write a working-directory-relative artifact path.** `"../test-results/x.json"` only resolves from the directory the file used to live in. Walk up from `__file__` — `casim.engine.particles._results_path` is the pattern (it deliberately does not import the suite layer, which would invert the dependency direction).
- **Guard the write behind `__main__`.** A module that runs its derivation *and writes its JSON* at import will silently overwrite a committed baseline the moment anything walks the package — `pkgutil`, pytest collection, coverage, `casim index`.
- **Do not diff an artifact you did not re-run.** That proves nothing, and it is how C1's FFT routing moved two integer observables invisibly.

### Adding a module — the checklist

1. Put the file under the right `engine/<sector>/` with the sector's naming prefix.
2. Import constants from `casim.constants` and numerics from `casim.numerics`. No literals, no `import numpy`.
3. Add a `Module(...)` to `_SPINE` in `src/casim/engine/registry.py`.
4. Add `Site(...)` entries to the constants it binds.
5. Write a test as a **registry record** with a real `kind` and `expect.exactness` — not a script that does physics at import.
6. If it is reachable from a channel, register the channel and re-run `make graph`.
7. `make indexes && make gate`. Then the changelog entry, the finding file, and `docs/status/exactness-inventory.md` if a new exactness claim landed.

### Concurrency — claim your TOPIC at session start, take a NUMBER at write time

Finding-number and test-ID collisions between parallel sessions have happened at F110, F129, F219, F229–F232, F262, and during C1/C2 and C5/C6. Every one had the same shape: two sessions each read the same "max finding number", each wrote the next one, and the loser found out afterwards. **Reading the max is not a reservation.**

**The two jobs are separate, and bundling them was the defect (revision 2, 2026-08-05).** Advertising your topic and sector has to happen at *session start* — its entire value is warning a parallel session off before either has done the work. Allocating a finding number cannot happen then, because nobody knows at session start how many findings a question will produce. The old protocol forced the second onto the first's clock, so every session guessed "3 to 5", most landed one, and the remainder stranded as gaps: seventeen interior gaps between F291 and F314 by 2026-08-04, each costing a hand-written declaration for a number nobody ever used.

**The claim board is `docs/design/session-claims.yaml`.** Its `about:` block holds the full schema. The protocol:

1. **Before any research, open a claim — with no numbers.** As soon as a question is posed or a model element is picked up, append a claim with your session handle, `status: open`, your sector, and a one-line topic. There is no `findings:` field and no block to size. This is one small append and it is the whole collision-avoidance mechanism.
2. **Claim your sector in the same entry**, and work in one sector. Rewire only files you own — a file importing another sector's module is still *your* file if it lives in your sector.
3. **Take a number only when you write the file, one at a time.** Run `casim index` and read the **`NEXT FREE NUMBER`** line. That is the lowest number declared `status: free` in `docs/design/finding-numbers.yaml` — a number nobody ever wrote at. In **one edit**: create `findings/F{N}-....md`, add `{N}: findings/F{N}-....md` to your claim's `used:` map, and **delete that number's `free` entry from `finding-numbers.yaml`**. Deleting the entry *is* the act of spending the number. Need a second finding? Repeat then, not now.
4. **Lowest free, not max+1.** The allocator hands back numbers below the maximum on purpose: the old scheme left a 22-number backlog (F280 upward), and ordinary work drains it. A finding landing at F280 on 2026-08-05 is expected, not a mistake. `casim index --check` **fails** if a `status: free` entry names a number whose file now exists — that is a spent number still advertising itself as available, which is how two sessions get handed the same one.
5. **Release at session end.** Set `released:` and a `release_note:` saying what landed. There is no "reserved but not used" to report — nothing was reserved. Released claims stay on the board; it is also the collision history.
6. **Retakability is declared, never inferred.** "No file exists" does not mean free. F219 and F229 have no file and are **not** retakable: the changelog records them as abandoned after a collision, so a reader chasing that citation must not land on unrelated physics. Only `status: free` is free; `resolved` and `retired` are not.

Writing a finding at `F<N>` claims the `F<N>-*` **test-ID namespace** with it, so a registry record `id: F280-something` needs no separate reservation. List a test ID explicitly on the board only when it does *not* derive from a number you hold — `run-*`, `fork-*`, `scenario-*`, or an `F<N>-*` on someone else's number.

**What the residual race is, honestly.** The window between reading `NEXT FREE NUMBER` and writing the file is no longer covered by a reservation. It is now seconds rather than the whole session, and a collision inside it produces a **duplicate**, which `casim index` already refuses loudly. The old window was hours and its failure mode was a silent gap, which nothing refused. That trade is the point of the change. The older `claims:` block in `docs/design/module-migration-manifest.yaml` is the migration-era sector board and is kept as history; new claims go in `session-claims.yaml`.

### Sandbox operational notes

- **`git checkout -- <path>` may fail** on this mount (it needs `unlink`, and a half-failed checkout strands a `.git/index.lock` it also cannot remove). Restore a file with `git show HEAD:<path> > <path>` — truncate in place, no unlink, index untouched.
- **A single bash call is killed at ~45 s.** Verify gate checks one at a time rather than through one `run_gate.py` run, and use resumable/journalled tools for long passes.
- Long physics runs belong on Ben's machine: hand back a script or `casim` parameters that emit a JSON for the next session to read.

## Practices

Use the important elements of a new theory, it must explain existing scientific measurements (not necessarily other theories), and either explain them better or extend beyond them. Our strong preference is for equations and predictions to be to algebraic exactness, then machine-precision exactness.

- Always attempt to algebraically derive new elements or functionaltiy before introducting new physics.
- Use CASIM now when possible, when sandbox timeout is exceeded, give the user a script or run parameters for CASIM to return a json or result file for Claude to read.

- Be aware that using numpy or scipy on chiral transforms may not produce desired results. Check them first when troubleshooting. If they are returning wrong results or droping the real or imaginary elements, begin writing our own library of functions from scratch so we know what they are doing. `casim.numerics` (D8) is the right place to own a hand-written replacement, and its equivalence contract specifically covers real/imaginary preservation.
- Use Markdown math to write equations in markdown files, use unicode characters when responding to the user. 
- **Pipes in tables:** a literal `|` (e.g. `|k|` for a magnitude, `|ψ|²`, or absolute-value bars) breaks Markdown tables because `|` is the column delimiter. Inside any table cell — including finding titles that get pulled into `findings-index.md` — escape it as `\|` (`\|k\|`), or use the LaTeX forms `\lvert k\rvert` / `\lVert k\rVert`. The index regen script auto-escapes `|`→`\|` in summaries, but write finding **titles and body tables** safely so they don't break on first render.
- For all new entries to files, include a date & time stamp of the format `yyyy-mm-dd - hh:mm`

- Include a `docs/status/changelog.md` file entry for documenting non-trivial software changes and decisions, make them short, one-paragraph.
- Keep a short table of what tests and equations are exact and which ones run to machine precision in `docs/status/exactness-inventory.md`.
- Document any new physics finds, or possible new finds, to the Findings folder with each new finding being a new markdown file. Use the convention `F99-name.md`.
## Index maintenance

`findings-index.md`, `project-status-index.md`, `tests-index.md`, `code-index.md`, `claims-index.md` and `docs-index.md` are compact indexes used to keep context usage low. Since roadmap C8 they are generated **from the registries** — the module registry (`casim.engine.registry`, D11) and the test registry (`tests/registry/*.yaml`, D9) — not scraped from the filesystem, together with `test-results/manifest.json` and the generated blocks of `docs/status/exactness-inventory.md`. Regenerate after any session that adds findings, tests, modules or docs:

```bash
make indexes                  # = casim index   (all eight targets)
casim index --check           # exit 1 if anything is stale; `make gate` runs this
casim index --only tests      # one target: findings,status,tests,code,docs,results,exactness,claims
```

`casim index` also **refuses** a finding number that is used twice, or a gap in `findings/`, unless it is declared in `docs/design/finding-numbers.yaml` with a reason. The ten C8.2 collisions are resolved (2026-07-31): duplicates are at **0**, gaps at 16 declared, max **F266**. Numbers have collided across concurrent sessions repeatedly, so when you add a finding: check the max first — `casim index` prints it — and if a collision genuinely has to stand, declare it. A *stale* declaration (an exception for a duplicate that no longer exists) also fails, except where `status: resolved` records a renumbering.

`tools/regen_indexes.py` and `tools/gen_exactness_inventory.py` are deprecation shims onto `casim index`.

INDEX.md is hand-maintained — update it only when the directory layout itself changes.

## Physics decisions in code — where things live now

Decision 4 and 5 above name modules by their pre-C9 flat names. Current homes:

| Referred to as | Now |
|---|---|
| `ca_photon_pair.py` | `casim.engine.gauge.photon` |
| `ca_maxwell.py` (σ-bilinear construction) | `casim.engine.gauge.bilinear` |
| `ca_wmu._f26_rotation_step` | `casim.engine.gauge.wmu._f26_rotation_step` |
| `ca_gluon.gluon_rotation_step_spectral_bcc` | `casim.engine.gauge.gluon.gluon_rotation_step_spectral_bcc` |
| `ca_gravity.py` | `casim.engine.interactions.gravity` |
| `ca_stellar.py` | `casim.engine.interactions.stellar` |
| `ca_bcc.py` | `casim.engine.lattice.bcc` |
