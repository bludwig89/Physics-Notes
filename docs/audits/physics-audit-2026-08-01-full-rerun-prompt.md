# Physics Audit V — complete re-run and consistency audit of CASIM

*Authored 2026-07-31 - 22:57. Audits the tree as it stands after changelog entry `2026-08-01 - 03:35` (F272/F273, P3.1 partial).*
*Supersedes `docs/audits/physics-audit-prompt.md` (2026-06-29, written against the pre-C9 `ca-simulation/` tree — every path in it is stale).*
*Designation: **V0–V9**. `V` is unused by the roadmaps (`C`, `P`), findings (`F`) and falsification briefs (`FA/FB/FC`), so audit items can be cited without collision.*

---

## 0. The instruction to the auditing session

You are conducting a **complete physics audit of CASIM**: every module, every sector, run rather than read where running is possible. The unified-program roadmap (`docs/roadmaps/roadmap-unified-program.md`) is mid-flight — P0/P1/P2 and P3.2–P3.6 are done, P3.1 is partial, P4/P5 are unbuilt — and that is exactly why this audit is being taken now. Five of six structural blockers closed in the last 48 hours (F268/F269/F270/F271) and two findings in the last six (F272/F273) reclassified a premise that four other findings were resting on. **Nobody has re-run the foundation since.**

Ben's stated priority, in his words: *"We need to fully rerun everything, especially the cubic/BCC lattice parts, and make sure our foundation and photon construction are still fully functional."*

So the two questions this audit exists to answer, above all others:

> **V-Q1.** Is the foundation — BCC walk unitarity → dispersion → $c_\text{lat}=1/\sqrt3$ → mass → the even rotation law — still exact, still self-consistent, and still what the code actually computes?
>
> **V-Q2.** Is the paired-spinor photon (F67/F68/F69, `casim.engine.gauge.photon`) still massless, luminal, transverse, non-birefringent and exact, **after** F265's action rebuild, F271's dielectric coupling, F270's energy convention change, and F272/F273's BZ reclassification?

Everything else in this document is in service of those two, or is the sweep that catches what they do not.

### 0.1 Authority — what you may and may not change

**You may:**

- Fix broken plumbing: stale import paths, dead file references in docs, a test that fails because a module moved, an index that is out of date, a registry record pointing at a renamed file.
- Regenerate anything generated (`make indexes`, `make graph`, `make registry-gen`).
- Add new tests, new registry records, new finding files.
- Write the report, the handoff script and the changelog entry.

**You may not:**

- Change a physics number, a derivation, a coefficient, or a constant's value.
- `git add` a drifted baseline. A drift is a **finding for the report**, with a recommended verdict; the decision is Ben's.
- Insert a BZ measure factor anywhere. See §0.2.
- Delete or rewrite a fork. A fork is a falsification record.
- Mark an item verified that you did not run. `SKIP` and `UNVERIFIED` are honest report entries; a claimed pass you did not observe is the one thing this audit cannot tolerate.

If you find a defect that is physics rather than plumbing, **stop, record it, and continue the audit**. Do not fix it and do not carry the fix forward into later stages — a repaired tree mid-audit means the later stages are auditing something different from the earlier ones.

### 0.2 Nine traps this project has already fallen into

Each of these cost a real session. They are listed here because the audit will walk straight through the same ground.

1. **Do not diff an artifact you did not re-run.** That proves nothing. C1's FFT routing moved two integer observables invisibly this way.
2. **Baseline drift below $1\times10^{-12}$ is the `machine` floor, not a change.** `tools/check_result_drift.py` runs strict at 1e-15 and will disagree with the runner; the runner is right unless the record sets `expect: {strict_floor: true}`.
3. **Order is always run → `--restore` → `--apply`.** An arming run rewrites committed baselines in place. Forgetting `--restore` has silently left modified baselines twice.
4. **Do not insert $3\sqrt3/4$, or 4, or any BZ measure factor.** F265's factor-4 premise is now known to be **wrong everywhere** (F273 §1: the raw `bcc_dispersion` is $\sqrt3\cdot$fcc-periodic, so plain fcc is a period of nothing in the tree). F272 is the worked example of applying the prescribed fix and it being wrong. Classify each $k$-space average; do not multiply.
5. **`git checkout -- <path>` fails on this mount** (needs `unlink`; a half-failed checkout strands a `.git/index.lock` it also cannot remove). Restore with `git show HEAD:<path> > <path>` — truncate in place, no unlink, index untouched.
6. **A single bash call is killed at ~45 s.** Run gate checks one at a time rather than through one `run_gate.py` invocation, and use the journalled/resumable tools for long passes.
7. **numpy/scipy on chiral transforms.** Check them first when a chiral result looks wrong — dropped real or imaginary components have bitten this project before. `casim.numerics.chiral` is the hand-written replacement and its equivalence contract covers real/imaginary preservation.
8. **A graph that cannot see half the couplings is more dangerous than registration order**, because registration order does not claim to be correct. F269's curated-key-list pass missed 45 edges; F271 fixed it structurally. If you build any dependency-style analysis in this audit, resolve references structurally.
9. **Claim your numbers and your sector, at the start.** Finding-number and file collisions between concurrent sessions have happened at F110, F129, F219, F229–F232, F262, and during C1/C2 and C5/C6 — each time because two sessions read the same max and both wrote it. Before doing any physics, append a claim to `docs/design/session-claims.yaml`: session handle, sector, one-line topic, and a 3–5 number block taken from `next_finding` (bump the pointer in the same edit). Fill in `used:` as you write each finding; release the claim at the end. Protocol: CLAUDE.md "Concurrency". `casim index` still prints the current max (**F273 at time of writing — the roadmap §2.1 still says F266 and the F267 changelog entry still says F267, so trust `casim index`, not the prose**), but the max is the *backstop*, not the reservation.

### 0.3 Sandbox reality and the handoff contract

The sandbox kills a bash call at ~45 s and cannot run the full battery, `gauge_mc` at production $L$, or a 24-hour resume test. Therefore this audit has **two tiers**, and the split is declared per item below:

- **Tier S (sandbox)** — runs here, now, in this session. `make gate` check-by-check, `casim test --tier gate`, targeted `--finding` and `--sector` selections, algebraic/sympy re-derivations, static analysis.
- **Tier B (Ben's machine)** — emitted as **one runnable script**, `tools/audit_v_battery.sh`, plus a manifest of the JSON artifacts it will write into `test-results/audit-v/`. The next session reads those JSONs and completes the report. Nothing in Tier B is reported as verified until its JSON exists and has been read.

Start every bash session with the vendored packages:

```bash
cd <repo root>
source "$PWD/.vendor/activate.sh"      # no download; CPython 3.10 linux-aarch64
export PYTHONPATH="$PWD/src:$PYTHONPATH"
python3 -m pytest ... # note: `python3 -m pytest`, never bare `pytest`
```

Do **not** `pip install` scipy/numpy/pyfftw/pytest — proxy downloads fail. See `.vendor/README.md`.

---

## V0 — Load context and establish the starting state

**Tier S. Do this before anything else.**

```bash
cat INDEX.md
cat findings-index.md
cat code-index.md
cat tests-index.md
cat project-status-index.md
tail -n 200 docs/status/changelog.md          # NOT the whole file (~100k tokens)
cat docs/theory/key-decisions.md              # D1–D11 + the physics decisions
cat docs/theory/supersessions.yaml
head -120 docs/status/exactness-inventory.md
sed -n '1,140p' docs/roadmaps/roadmap-unified-program.md
```

Then read, in full, the six findings that changed the ground under this audit in the last week:

`F265` (BCC gauge geometry — the action was blind to ⅓ of the curvature), `F267` (the walk's BZ is not the FFT cube), `F268` (engine clock), `F269` (typed exchange bus), `F270` (one energy convention + gravity loop), `F271` (k-resolved dielectric coupling), `F272` (the `bgfield_loop` refold bug), `F273` (the mode-sum audit; F265's factor-4 premise is wrong everywhere).

**Record the starting state as a table in the report.** Every number below is a claim from the roadmap or changelog that you should *verify*, not copy:

| Quantity | Claimed | Measured by you |
|---|---|---|
| `make gate` checks green | 14 |  |
| `pytest tests/casim` | 176 passed / 2 skipped |  |
| `casim index --check` | clean |  |
| `make drift` | no tracked JSON differs from HEAD |  |
| engine modules registered (D11) | 178 (194 `.py` on disk — reconcile) |  |
| test registry records | 356 |  |
| gate-tier records | 22 |  |
| findings files / max number / duplicates | 268 / **F273** / 0 (roadmap §2.1 says 261 / F266 — stale) |  |
| scenarios | 46 |  |
| result artifacts | 394 |  |
| constants registered (D7) | 43 + 10 `MeasuredConstant` |  |
| rogue literals in `src/` | 0 |  |
| `import_time_work` | 320 |  |
| `legacy_script` (declared debt) | 47 |  |
| drift FAILs outstanding (P1r.2) | 28, plus 23 undecided arming records |  |

**If the gate is red before you touch anything, that is audit finding V-001** and the rest of the audit is conducted against a known-red baseline, stated as such.

---

## V1 — Reproduce the barrier, check by check

**Tier S.** Run each gate check as its own bash call (the 45 s limit). Record wall time and verdict for each.

```bash
python3 tests/casim/test_constants_consistency.py          # D7: no unregistered literal
python3 tests/casim/test_supersession_ledger.py            # ledger is true
python3 tools/apply_supersession_banners.py --check
python3 tools/audit_tests.py --ratchet
python3 tools/audit_numerics.py --ratchet                  # D8
python3 tools/audit_constants.py --ratchet                 # D7 sprawl
python3 tools/check_test_registry.py
python3 tools/gen_test_registry.py --check
python3 -m casim.cli index --check                         # C8: 7 targets + finding-number integrity
python3 tools/gen_module_graph.py --check
python3 tools/check_deprecated.py
python3 tools/check_module_registry.py                     # D11
python3 -m pytest tests/casim -q -m "not superseded and not slow"
python3 -m casim.cli test --tier gate
```

Also capture, because they are cheap and they are the two things nobody prints:

```bash
python3 -c "from casim.numerics import fft; print(fft.describe())"
python3 -m casim.cli backend
python3 tools/audit_numerics.py --list | head -40
python3 tools/audit_constants.py --list | head -40
```

**V1 checks to make beyond "is it green":**

- **V1.1** The `device_fft_call_sites` ratchet is baselined at 8 (the `jnp.fft` calls in `gauge/weak_wmu.py`). Confirm the count is still 8 and that `casim.numerics.precision.require_float64` still guards them. Confirm `precision.MACHINE_GATE == casim.baselines.MACHINE_FLOOR` — two copies of 1e-12 that can drift apart would measure a device path against a different bar than the results.
- **V1.2** `pytest` and `casim test --tier gate` must select the same objects by construction (`tests/conftest.py` `pytest_ignore_collect` + `tests/casim/test_registry_entries.py` parametrising over the same records). **Verify this empirically**, do not accept it structurally: compare the two selections and report any record in one and not the other.
- **V1.3** 194 `.py` files under `src/casim/engine/` vs 178 registry records vs 184 graph nodes. The roadmap explains 6 of the gap as fork `__init__.py` files. **Account for every remaining file by name.** `check_module_registry.py` should be catching this; if it is green with a gap, the check has a hole and that is a finding.

---

## V2 — The foundation: BCC walk, unitarity, dispersion, $c_\text{lat}$

**This is V-Q1. Tier S for the algebra and the small runs; Tier B for anything above $L=32$.**

Modules: `casim.engine.lattice.bcc`, `.core`, `.core_exact`, `.geometry`, `.derive_walk_bz_measure`, `.si_scale`.
Findings: the early F01–F30 chain, F25/F26 (the rotation law and $c_\text{lat}$), F105 (all-$k$ on-axis exactness), F83/F232 (lattice spacing), F107 (canonical cell), F267/F273 (the BZ question).

**V2.1 — Unitarity forces the dispersion.** Re-derive symbolically (sympy, not numerically) that the BCC walk unitarity condition $u^2+|\tilde n|^2=1$ forces $\Omega(k)$ as implemented. Check the sign convention against F26. Report whether the code's `bcc_dispersion` is the algebraic consequence or a separately-written expression that merely agrees.

**V2.2 — $c_\text{lat}=1/\sqrt3$ exactly.** Confirm $c_\text{lat}=d\Omega/d|k|\big|_{|k|\to0}$ with $\Omega=2\omega(|k|/2)$ (Design Decision 2), symbolically. Confirm the constants registry exports it as a closed form and not a decimal, and that the **two** deliberately-separate $1/\sqrt3$ constants (a speed and a momentum scale) are still separate — a test asserts they cannot be merged; confirm that test runs.

**V2.3 — F105 all-$k$ on-axis.** $\Omega(k\hat x)=|k|/\sqrt3$ at **all** $k$, not just small $k$. Re-run and confirm to machine class. This is the single most load-bearing exactness claim in the lattice sector and it is what makes the photon luminal at every wavenumber rather than only in the IR.

**V2.4 — Doublers.** Re-run F267's S3 measurement at $L=24,36,48$ and, if Tier B allows, $L=64$: exactly one $\omega=0$ point (at $k=0$) and zero $\omega=\pi$ points inside the cube, both branches. **If a doubler appears at any $L$, stop the audit and escalate** — F250's all-$k$ gauge pole and the F69 photon both rest on this, and D1 re-opens.

**V2.5 — The cubic reference layer.** `core.py` and `core_exact.py` are 100% cubic reference code carrying the banner *"reference implementation, continuum-limit regression target, not canonical (D1)"*. Verify (a) the banner is present and accurate on every cubic entry point, (b) the cubic kernels still reproduce their continuum-limit regression targets, (c) **the rename to `cubic.py`/`cubic_exact.py` is still outstanding** and the 8 importers plus the `ca_core`/`ca_core_exact` aliases in `src/casim/lattice/__init__.py` are still pointing at the old names. This is P3.1 item 6, blocked in the sandbox by the `unlink` restriction — put the exact `git mv` commands in the handoff script, do not attempt it by copy.

**V2.6 — Cubic ↔ BCC agreement where they overlap.** For every observable computed both ways, report the agreement and its exactness class. Where a cubic and a BCC result disagree beyond the machine floor, say which one the physics claim rests on.

---

## V3 — The photon construction, end to end

**This is V-Q2. Tier S for everything except the long propagation runs.**

Module: `casim.engine.gauge.photon` (the paired-spinor photon — **the** photon). Comparison objects: `gauge.bilinear` / `bilinear_2d` (σ-bilinear construction, **W/Z/gluon only**, never the photon — the F65–F69 banner is load-bearing), `gauge.photon_bound_state`, `gauge.rotation`, `gauge.propagator`, `gauge.minimal_coupling`, `gauge.charge_coupling`.

Tests to re-run, all of them, individually:

```
tests/findings/test_f26_rotation_law.py
tests/findings/test_F67_option1_even_law_photon.py
tests/findings/test_F68_minimal_coupling_forces_even_photon.py
tests/findings/test_F69_paired_photon.py
tests/findings/test_F87_charge_coupling_paired_photon.py
tests/findings/test_F89_singlet_bilinear_is_paired_photon.py
tests/findings/test_FG6_two_helicity_photon.py
tests/findings/test_F129_blockspin_free_photon.py
tests/findings/test_F168_paired_photon_binding.py
tests/findings/test_F169_photon_bound_state.py
tests/findings/test_F250_allk_gauge_pole.py
tests/findings/test_SR5_photon_frame_invariance.py
tests/findings/test_su2_photon_bridge.py
```
or, preferably, by selection so the registry is the specification:
```bash
python3 -m casim.cli test --finding F67 --finding F68 --finding F69
python3 -m casim.cli test --finding F250 --finding F129 --finding F168 --finding F169
```

**V3.1 — $\Omega_\text{pair}=\Omega_\text{even}$ exactly.** Confirm $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$ equals the even law symbolically, at all $k$, not numerically at sample points. Confirm the propagator actually invoked by `gauge.photon` is `wmu._f26_rotation_step` (the even law) and nothing else.

**V3.2 — Non-birefringence, and how it is established.** Report whether non-birefringence is *derived* or only *verified numerically*, and state precisely what would make it birefringent. Then check the GRB/AGN polarimetry bound (F65/F66/F67) is still quoted with a source and that the paired photon's birefringence — which should be identically zero, not merely small — is what the model claims. If the claim is "identically zero", the test must assert zero, not a tolerance.

**V3.3 — Masslessness, luminality, transversality.** Re-run each as its own assertion at multiple $L$ and multiple $k$, including $k$ near the zone edge. Luminal means $c=1/\sqrt3$ at **all** $k$ (V2.3), not in the IR limit.

**V3.4 — The four things that changed under the photon since it was last audited.** Each is a specific regression risk; check each explicitly:

- **F270 (energy convention).** `PhotonPairChannel.energy` was exactly **twice** `coupled.field_energy`; the ½ won and the two are now bound to the same object. **55 tracked dumps move by exactly 2× when re-run.** Verify: (a) the definitions are one object, not two agreeing copies; (b) every one of those 55 dumps that you re-run moves by exactly 2×, and any that moves by something *other* than 2× is a finding; (c) the supersession record for this exists and is accurate.
- **F271 (k-resolved dielectric).** `photon_step_dielectric` replaced the eikonal $\omega_0$ mix. Verify the four claims: a uniform dielectric is exact (~4e-15, every mode slowed by exactly $1/K$); Weyl-symmetric ordering makes the evolution exactly orthogonal so norm drift **converges** ($1/n^3$) rather than plateauing at 1.1e-5; the Strang order is **2.00**, not 1; and **no free parameter** survives. Then check the honest refusals held: the gradient-index bend ratio runs 1.455 / 1.092 / 0.959 at σ = 2.5 / 4.0 / 6.0 and the test asserts direction, linearity and the exact-zero baseline **only**. If someone has since tightened that assertion onto 1.25, it is pinning a narrow-packet artifact.
- **F271 handoff, unfixed.** Both defects F271 fixed are **still present** in `lattice.curved._half_step_dH`, and therefore in every F64-fork variable-c result. Confirm this is still true and quantify what it means for the F64 fork's published numbers.
- **F272/F273 (BZ reclassification).** The photon chain must be checked for any $k$-space average that F273's audit has not yet classified. `photon_bound_state` has **2 unclassified sites**. Classify them (see V4.3).

**V3.5 — Block-spin.** F129/F130 give $[R_b, R(\Omega)]=0$ for the free even law. F271 added an honest refusal: **a gravitating photon under block-spin now raises**, because $\Omega_b(\kappa)=\Omega(\kappa/b)$ and the dielectric's coarse-graining have not been shown to commute. Confirm the raise is still there and has not been quietly softened to a warning. Then answer the open question the 2026-06-29 audit asked and nobody closed: **does $[R_b,\text{evolution}]=0$ hold for the *sourced* (matter-coupled) propagators, or only the free ones?**

**V3.6 — The σ-bilinear boundary.** Grep the whole tree for any path where `bilinear`/`bilinear_2d` reaches the photon. The F65–F69 banner exists because the composite σ-bilinear photon is birefringent and excluded by polarimetry. One import is a critical finding.

---

## V4 — The cubic/BCC partition (B1) and the BZ question

**The one structural blocker still open. Tier S, and it is mostly analysis.**

**V4.1 — Re-measure the partition.** The roadmap claims: 6 cubic-only channels (`photon_pair`, `w_chiral`, `z_even`, `charge_photon`, `gauge_mc`, `refraction_2d`), 10 BCC-only, 13 agnostic; `simulation.py:71` hard-rejects mixing; scenario split 31 BCC / 15 cubic. **Measure it yourself** and report drift from those numbers. Note the awkwardness the roadmap does not flag: `photon_pair` is listed as a **cubic-only channel** while F265 establishes every gauge *propagator* was always BCC. Resolve that apparent contradiction explicitly — is it the state layout, the channel's grid, or the roadmap's label that is cubic?

**V4.2 — The five residual cubic layers.** Status per F265 §9 / P3.1:

| # | Layer | Status to verify |
|---|---|---|
| 1 | `gauge/lpt_*` (7 modules) | 4D hypercubic Wilson, $\hat k_\mu=2\sin(k_\mu/2)$, `range(4)`. Still cubic. **Its BZ measure must be re-derived against the $\sqrt3$ period, not F265's fcc reading** (F273 §1) |
| 2 | `gauge/bgfield_loop` | **Fixed, F272** — but not as prescribed. Verify the fix: flatness 1.58e-2 → 2.96e-5, grid-convergence 70% → 0.13% between n=14 and n=18, $b_0=11$ untouched, and exactly one committed number moved (`F162.G2.rule_shift_mean` −0.005071 → −0.012591) |
| 3 | `gauge/hypercharge` | **Is 2D despite its docstring** — calls `dirac._weyl_half_step_2c`, which builds only `KX, KY`, so U(1)$_Y$ lives on the 2D $1/\sqrt2$ lattice. Confirm still true. Assess what F41/F42/F138/F143 inherit from this |
| 4 | The MC actions | F94 4D cubic, F146 3D cubic; to be rebuilt on the rhombic action. Confirm unstarted |
| 5 | The $\sqrt3$ question | **Answered by F267 and reframed by F273.** See V4.3 |

**V4.3 — The mode-sum audit, and the tension it exposes.** This is now the **top P3.1 item** and it is the most consequential single question in this audit.

F273 found: the raw, unhalved `bcc_dispersion` — what the gauge side is built from — is **also** $\sqrt3\cdot$fcc-periodic. So F265's boundary between a clean gauge side and a $\sqrt3$ fermion side **does not exist**, and the factor 4 never applied anywhere. Worse, the cube is a **biased** sub-region, not merely a partial one: over the true zone $\langle u\rangle=0$ by symmetry, so $\omega$ is symmetric about $\pi/2$ and $\langle\cot\omega\rangle$ vanishes *identically*; over the cubic grid $\langle u\rangle=+0.152$ and $\langle\cot\omega\rangle=+0.221$, converging.

`i2_lattice` $=\langle\cot\omega\rangle$ feeds $B=-3\sqrt2\,I_2\bar y^4$ and hence the F234 arrow $\lambda_6=0.243$ — a **founding-principle output** (Design Decision 7). F273 classified it as a mode sum and it stands, but left the tension unresolved:

> **Reading 1** — the array is the physical lattice, its $L^3$ Fourier modes *are* the cubic grid, every mode sum is right, and "Brillouin zone" should be retired from these docstrings.
> **Reading 2** — the BCC crystal is physical, the array is an unfaithful discretisation, and $I_2$'s entire nonzero value, hence $B$, hence $\lambda_6$, is a sampling artifact — because the unbiased answer is exactly **zero**.

**Reading 2 would demolish the lepton sextic chain.** That is not an argument against it. This audit's job is not to decide the question — it is to (a) state precisely what evidence would settle it, (b) enumerate every result that hangs on each reading, and (c) recommend the decisive test. Note that Design Decision 7 makes $\delta^*=2/9$ **primary** and $\lambda_6$ an **output** via the F234 arrow, so a Reading-2 outcome may be survivable in a way F273 does not spell out — check whether it is, and say so either way.

**V4.4 — Complete F273's coverage.** F273 found **56 candidate $k$-space averages** and classified **2 chains**. Unclassified: `lpt_*` (14 sites), the QED pair (6), the tadpole moments (3), `photon_bound_state` (2), and F100's own $\sigma_\phi^2\to\gamma(\Omega)$ chain. Classify as many as the session allows, in that order (`photon_bound_state` first — it is in the photon chain, V-Q2). For each: **mode sum** (the cube is correct by construction) or **continuum BZ integral** (the cube grid-mean carries 10.7% on $\langle\omega\rangle$ to 16.9% on $\langle1/\omega\rangle$, or *everything* for a cot-class moment). Record each classification with its evidence. **Multiply nothing.**

**V4.5 — The re-scoped middle bucket.** F265 named a list of results that are *not invalidated* but are re-scoped as "measured on an action blind to ⅓ of the curvature": F43/F33, F94, F146, F101/F102/F110, F86/F88 and hence F124/F235, and the $d_1$ chain (F144/F151/F152/F154/F155/F162/F163/F239). Verify each of those finding files carries an accurate scope note. A finding that still claims an unqualified number is a documentation defect and a fix you are authorised to make.

---

## V5 — Sector-by-sector re-run

**Tier S where it fits, Tier B otherwise.** Work sector by sector, in this order. For each sector: run the gate tier, then the battery tier if it fits, then re-run the sector's result dumps and diff **only** what you re-ran.

```bash
python3 -m casim.cli test --sector lattice
python3 -m casim.cli test --sector core
python3 -m casim.cli test --sector gauge
python3 -m casim.cli test --sector particles
python3 -m casim.cli test --sector interactions
python3 -m casim.cli test --sector forks
```

Sector-specific checks:

- **lattice** — V2 covers most of it. Add: `multigrid`, `poisson_open`, `blockspin*` (F130–F134, F140), `curved` (**carries F271's two unfixed defects**), `si_scale` (F107/F123).
- **core** — the four brand-new modules: `clock` (F268), `graph` (F269), plus `channel`/`channels`/`coupled` under F270's energy convention. Specifically verify: the 18 desynchronised scenarios still run in `legacy` **bit-identically** and still write `clock.synchronous: false` into their results; the exact-rational `dt` arithmetic still refuses the float trap (`1.0/0.1 = 9.999999999999998`); `build_graph`'s **structural** reference resolution still finds all 45 edges across the four key paths; the one surviving vacuous ordering violation (`unified_hydrogen_free`, `couplings: {}`) is still vacuous — both orderings bit-identical across all 22 state arrays.
- **gauge** — V3 and V4 cover the photon and the actions. Add: `weak*`, `weak_z`, `charged_current` (F54: is V−A explicit? is CKM present or is its absence stated?), `chiral_anomaly`, `gluon*` (F91: the chiral→even migration of 2026-06-04 — is the even law **forced** for gluons or merely consistent?), `strong`, `su3_ladder`, `colour_*`, `confinement`, `cooling`, `bcc_action` (F265's rhombic plaquettes: 6, $\langle110\rangle$ normals, area $2\sqrt2$, one $O_h$ orbit, $\sum_p m_pm_p^{\mathsf T}=4\mathbb I$ — re-derive this in closed form), `hypercharge` (still 2D, V4.2).
- **particles** — `dirac`/`dirac_bcc`, `second_quant`, the lepton-shape `derive_*` chain (Design Decision 7: $\delta^*=2/9$ primary, $\lambda_6$ output, shape to ≤0.007% with **zero shape parameters** — re-run and confirm the residual), `eg_sextic`, `induced_stiffness`, baryon/meson/nuclear/atom/element, `positronium`, `hyperfine`, `majorana`, `higgs`.
- **interactions** — `gravity*` (Design Decision 4: the induced Einstein equation is canonical; the exponential $K$ is the **vacuum/weak-field representation**, PPN-order only; the exact vacuum solution is Schwarzschild and **F114's horizon-free black hole is superseded by F178** — verify no live module or paper still claims the horizon-free BH as current), the astrophysics set, `qed_*` (13), `running_*` (7), `qi_*` (5), `superconductivity`, `slowlight`, `vacuum_energy`, `unified`.
- **forks** — 47 recorded alternatives across 6 sub-sectors. **Do not run these for physics; run them to confirm they still load and that their falsification records are intact.** Remember a fork is loaded by file path or bare name, never as a package submodule, and a subprocess running one needs `PYTHONPATH=src` handed to it explicitly.

---

## V6 — Cross-sector consistency

**Tier S. This is where a per-sector-green tree can still be wrong.**

- **V6.1 — One $c$.** Photon speed, gravitational-wave speed (F180: $c_\text{grav}=c_\text{lat}=1/\sqrt3$, GW170817 residual ≤3e-83), strong-sector propagation, and the fermion walk's group velocity. Confirm all four are the same object from the constants registry, not four agreeing numbers.
- **V6.2 — One energy.** F270 established $\tfrac12\sum(E^2+B^2)$ defined once in `channel.field_energy`. Re-run the conservation gate: free photon, $L=16$, 1000 ticks, `max_rel_drift` should be ~3.4e-14, class `machine`. Then check the deeper point holds: `Channel.energy` is a **drift probe** (it mixes a dimensionless probability norm with an energy) and `energy_density` is the additive quantity; `TotalEnergy` reports a channel with no expressible energy leg under `missing` rather than counting it as zero.
- **V6.3 — One clock.** Confirm the engine's $\Delta t$ reconciliation and that no channel has re-acquired a private `dt`. The three build-time errors (non-dividing `dt_native`, non-subcyclable channel needing sub-cycling, step above its own CFL ceiling) must all still fire. A config may lower a ceiling, never raise it.
- **V6.4 — Gauss's law in the coupled theory.** F87 proves U(1) conservation; F43/FG-7 builds SU(3). **Is Gauss's law exactly conserved in the coupled EM+matter+strong theory, or only sector by sector?** This question was asked in the 2026-06-29 audit and has not been answered. Read `gauge/minimal_coupling.py` and test it in a coupled scenario. Also check whether the F87 residual (~2e-12 over 100 ticks) **grows with lattice size** — is it bounded?
- **V6.5 — Charge quantisation.** Quarks $\pm1/3,\pm2/3$; leptons $0,\pm1$. Derived from the U(1)$_Y$ structure, or put in by hand? Say which, with the file and line.
- **V6.6 — Gravity closes on matter.** F270's `T00_dirac_kinetic` must satisfy D-EM3 (a fast packet gravitates by total energy) — verify against its closed form $\tfrac12c^2\sin^2\!k\sum|\psi|^2$, i.e. the ratio constant across $k$ to <1e-4 and tending to 1 with envelope width, **not** against a threshold. Confirm the colour-axis sum bug in `T00_dirac_rest` is fixed and that a coloured `quark_dirac` in a `sources:` map no longer produces a three-copy gravitational field.
- **V6.7 — CP and CKM.** F53 gives Jarlskog $J(1)=0$ and $\theta$ pure gauge. Is that a *consequence* of having no CKM phase, or a *prediction* that the CKM phase is zero? If the latter, it conflicts with measured CP violation in the kaon and B systems and must be stated as an open conflict, not a result.
- **V6.8 — Three generations.** $g_*=48=16\times3$. Where is the prediction that there are exactly three? Is the 3 derived (F75, $\dim T_{1u}$) or input? If input, F79's structural $G$ inherits that status.

---

## V7 — Constants, exactness, and the empty field

**Tier S.**

- **V7.1** Walk all 43 registered constants (7 geometry, 2 gravity, 7 lepton, 25 strong, 2 electroweak, 1 in `__init__`) plus the 10 `MeasuredConstant` records. For each: does it have a `provenance` finding, an `exactness` class and a `derivation` string; does an exact constant resolve from a **closed form** rather than a truncated decimal; does a rational export both the `Fraction` and the `<symbol>_f` float; does a bracketed constant (`alpha_eff_star`) correctly export **no scalar**.
- **V7.2** The deliberate pluralities must still be plural: **2/9 is three unrelated constants** (`delta_star`, `sin2_thetaW_onshell`, `c_fierz_colour`), $f_\pi$ is three, $\cos3\delta^*$ is two, $1/\sqrt3$ is two. Confirm the test asserting the three-fold 2/9 split cannot be collapsed still runs and still fails when you deliberately collapse it. Merging any of them turns a prediction into an input.
- **V7.3** Every `Site(path, name, kind="import")` must still resolve — this is what went red after the C5 and C6 migrations. Run the sweep and report.
- **V7.4** `exactness` is **empty on all 178 module registry records** while `code-index.md` renders a column for it. And `code-index.md`'s generated `Reach` column takes only two values (47 `driven` / 131 `package-only`) while the module graph types four categories and counts 50 driven. **The artifact a reader is pointed at disagrees with the graph.** Both are P6 defects; report them with a recommended fix, and fix the `Reach` column if it is plumbing rather than physics (it is: `registry.py` takes `reach` as a manifest string instead of from the graph).
- **V7.5** Re-run `make health`, `make registry`, `make numerics`, `make structure`. Report every ratchet's value against its baseline. `import_time_work` at 320 is a **declared, unmet** acceptance criterion (P1.3/P1r.1) — confirm it has not silently been re-baselined.

---

## V8 — Claims against measurement

**Tier S for the table; Tier B for anything needing a re-run.**

Rebuild this table from the *current* tree. For each row: (a) is it a genuine zero-parameter prediction, (b) what is the residual against the current measured value, (c) is the residual consistent with expected $O(a^2)$ lattice corrections, (d) **has it moved since it was last recorded, and did anything in V1–V7 move it?**

| Quantity | Finding | Last recorded | Re-check |
|---|---|---|---|
| $c_\text{lat}=1/\sqrt3$ | F25/F26 | exact | prediction or definition? |
| $c_\text{grav}=c_\text{lat}$ | F180 | GW170817 residual ≤3e-83 | |
| $\sin^2\theta_W(M_Z)=0.23173$ | F138 | +0.22% | is the RGE borrowed from SM? is the scheme matching justified? |
| $\alpha_s(M_Z)$ | F144 | +1.3% (1-loop) | what sets the one free parameter? |
| Charged-lepton spectrum | F253/F255/F256 + F234 | ≤0.007%, zero shape parameters | **re-run; this is Design Decision 7** |
| $\lambda_6=0.243$ / $W=6\lambda_6=1.46$ | F234 | output, not fit | **hangs on V4.3's Reading 1** |
| $m_n-m_p$ | F122 | +1.51 MeV vs 1.293 measured | is +17% explained? |
| Nucleon at $3m_c$ | F123 | −1.05% | is $f_\pi$ the only free input? |
| H ground state | F125 | −13.596 eV, Ry to 1.1e-12 of CODATA | from a solver or the full CA? |
| Deuteron $E_b$ | F104/F113/F126 | 0.34% | how many parameters tuned? |
| $\sqrt\sigma/f_\pi$ | F124 | 12–29% | accepted or under active work? |
| $2\Delta/kT_c$, $\Delta C/C_n$ | F210 | machine precision | |
| $T_c$, 7 elements | F211 | mean 14% | |
| $\rho_\Lambda$ | F193/F196 | 0.10 dex; leftover $=\Omega_\Lambda\approx0.69$ | |
| BH shadow | F114 | +4.63% | **F114 is superseded by F178** — is this claim withdrawn everywhere? |
| Alcubierre warp | F204 | structurally excluded | |
| $m_W$, $m_Z$ | F118/F138 | | are they predicted and compared to 80.377 / 91.188 GeV? |
| $g-2$ | — | | is it computable? has it been attempted? |
| CKM matrix | — | | derived, or absent-and-stated? |
| Neutrino masses | F47 + F216 | | non-zero? what sets the scale? is the seesaw completed? |

Rows with a blank "last recorded" are the ones the 2026-06-29 audit flagged as **omissions**. Check whether each is now addressed, still open-and-acknowledged, or still open-and-unacknowledged. The third category is the one that matters.

---

## V9 — Verify the audit

**Do not skip this. Tier S.**

1. **Re-run a random 10% sample** of everything you reported as passing, and confirm the verdicts reproduce. A verdict you cannot reproduce twice is not a verdict.
2. **Check your own arithmetic** programmatically — every percentage, every dex, every ratio in the report.
3. **Confirm you left the tree clean:** `git status` should show only the files you intended (the report, the handoff script, the changelog entry, regenerated indexes, and any plumbing fixes). **No modified baselines.** If an arming or sweep run touched one, `--restore` it.
4. **Re-run the full gate one final time** and confirm it is in the same state you found it, or better, and never worse without an explanation.
5. **Spawn a verification subagent** with the report and the raw command output, and the single instruction: *find every claim in this report that the evidence does not support.* Fold its findings in.

---

## Deliverables

1. **`docs/audits/physics-audit-report-2026-08-01.md`** — the report. Structure:

```markdown
# Physics Audit V — Report

## Executive summary
[3–5 sentences. The verdict on V-Q1 (foundation) and V-Q2 (photon) goes first.]

## V-Q1 verdict — the foundation
## V-Q2 verdict — the photon construction

## Starting state (measured, vs claimed)
## Critical issues — blocks a physics claim
## Algebraic and mathematical errors
## Logical gaps — "derived" claims that are assumed
## Inconsistencies between findings
## Omissions — physics absent or unaddressed (note which are already acknowledged)
## Documentation and labelling defects
## Ratchets and debt — measured
## Verified correct — explicitly checked and found sound
## UNVERIFIED — what this audit could not run, and why
## Recommended priority order
```

The **UNVERIFIED** section is mandatory and is not a failure. An audit that hides its coverage gap is worth less than one that names it.

2. **`tools/audit_v_battery.sh`** — the Tier-B handoff. One runnable script, resumable, journalled, writing one JSON per item into `test-results/audit-v/`. Must include: the full `casim test --scale smoke` battery; `gauge_mc` at production $L$; the 55 F270-affected dumps re-run; a `make drift` pass afterwards; the two `git mv` commands for V2.5 (commented, for Ben to run deliberately); and `--restore` before any `--apply`. Head it with the exact `.vendor/activate.sh` preamble and an estimated wall time per item.

3. **`test-results/audit-v/MANIFEST.md`** — what each Tier-B JSON will contain and which V-item it closes, so the next session can complete the report without re-deriving the plan.

4. **Findings** for anything genuinely new, at `findings/F{N}-name.md`. `{N}` comes from the block you reserved on `docs/design/session-claims.yaml` at session start (§9) — take the lowest one not yet in your `used:` map, and record it there in the same edit.

5. **A changelog entry** at `docs/status/changelog.md`, stamped `yyyy-mm-dd - hh:mm`, one paragraph per substantive result — and per this project's own convention, **record the negative results and the things you measured and declined**, not only what passed.

6. **`make indexes && make gate`** green, or a stated explanation of why not.

---

## Appendix — the six design decisions this audit is auditing against

Restated from `CLAUDE.md` so the auditing session cannot drift from them:

1. **Ludwig's SU(2) derivation**, not the Standard Model.
2. $c_\text{lat}=d\Omega/d|\mathbf k|\big|_{|\mathbf k|\to0}$ with $\Omega=2\omega(|\mathbf k|/2)$ — the **angular rotation rate of the real $(\mathbf E,\mathbf B)$ pair per unit spatial wavenumber**, not the propagation rate of a complex phase.
3. **Hypercharge on $U(x)$** — no Higgs field.
4. **Gravity:** the induced Einstein equation $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ is canonical (F178). The impedance-matched dielectric $K=\exp(2GM/rc^2)$, $AB\equiv1$, is the **vacuum/weak-field representation** — PPN $\beta=\gamma=1$, GR-identical — and **not** the field equation inside matter. F114's horizon-free black hole is **superseded**; the exact vacuum solution is Schwarzschild.
5. **Photon:** the paired-spinor photon (F67/F68/F69) — massless, luminal, transverse, **non-birefringent**, even law, the identity channel U(1) minimal coupling forces. It **supersedes** the σ-bilinear photon, which is retained for W/Z/gluon only. Propagator classes per F91: γ even (forced), W± chiral (forced), Z even with a mass-suppressed axial split, gluon even (forced).
6. **Elegant design** — the universe is completely understandable and simple in construction.
7. **Lepton shape angle:** weight-as-phase is a founding principle. $\delta^*=\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$ rad is **primary**; $\lambda_6=0.243$ is an **output** via the F234 arrow. The whole charged-lepton shape follows from $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ to ≤0.007% with zero shape parameters.

**Preference order for any claim, unchanged:** algebraic exactness first, then machine-precision exactness. Always attempt to derive before introducing new physics.
