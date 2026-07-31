# C1 Complete — The Numerics Façade

*Started 2026-07-30 - 12:10, completed 13:20. Phase C1 of
`docs/roadmaps/roadmap-casim-consolidation.md`. Follows
`docs/status/C0-completion-overview.md`.*

**Status: C1.1–C1.6 complete.** `make gate` — 16 checks, 28.4 s, green.

C1.3 and C1.4 were paused mid-phase because a parallel session was executing
C2 on the same files (§"The pause", kept below as the record); they were
finished at 13:00 once that session landed and the tree went quiet.

**Headline number: direct `np.fft` transform calls went 161 → 0**, across 32
files, with zero attributable drift.

---

## What landed

### C1.1 — `src/casim/numerics/` (decision D8)

One import surface: `from casim.numerics import xp, fft, linalg, rng, chiral`.

**The unification is the point.** Before C1 there were *two* seams for the same
job and neither was load-bearing:

- `ca_fft` selected numpy/scipy/pyfftw with a module-level string and an
  `if/elif` in every wrapper — a **library** seam that every kernel used;
- `casim.lattice.backend` held an object registry with a seven-method
  protocol — a **device** seam that **zero physics modules imported** (its only
  importers were two tests and its own self-registration).

A GPU backend registered in the second would never have been reached by a
kernel calling the first. `casim.numerics.backends` is now the single registry,
and the library choices are backend *objects* alongside any device backend — so
`use("pyfftw")` and `use("cupy")` are the same kind of statement.

`ca_fft.py` was migrated with C0's tool (backup in `deprecated/code/ca_fft.py`,
shim at the old path until C9). `casim.lattice.backend` is now a shim too.

| Module | Contents |
|---|---|
| `fft` | the `ca_fft` API verbatim, plus **`rfftn`/`irfftn`** — the real-valued E and B fields were paying full complex transforms |
| `linalg` | `batched_matmul` (BLAS `zgemm`), `dagger`, and the optional-scipy surface behind named-caller errors |
| `rng` | one independent stream per named consumer, so adding a channel no longer perturbs every other channel's numbers |
| `chiral` | `cmul` / `su2_apply` on explicit real pairs, per the CLAUDE.md caveat |
| `backends` | numpy / scipy / pyfftw / cupy / mlx, registered on availability |

**`xp` is honest about what it is.** It is the array namespace and today it *is*
numpy. Genuinely swapping the array namespace — MLX or CuPy arrays flowing
through every kernel — is not a C1 change; it alters the type every `ca_*`
module receives and every `isinstance` check in the tree. What C1 makes
swappable is the **transform** layer, which is where the time goes. `xp` exists
to give the migration one name to move to now and a place to put real dispatch
later, and the docstring says exactly that rather than implying more.

**MLX cannot be auto-selected, by construction.** It is float32-backed: eps
1.2e-7, five orders above the `machine` class's 1e-12 gate. It refuses to
activate without `CASIM_ALLOW_FLOAT32=1`, and a test asserts that no device
backend can become active on its own. If it could, every `machine_precision`
claim in the project would quietly stop meaning anything.

### C1.2 — The contract, extended (and one claim retracted)

`tests/casim/test_fft_backend_equivalence.py` now also pins:

| Check | Why |
|---|---|
| `rfftn` == `fftn` half-spectrum, and `irfftn` round-trips | a half-spectrum still broadcasts and its norms still look plausible — a wrong substitution loses the high half of k-space silently |
| `batched_matmul` vs `einsum` **within 1e-14** | see below |
| `su2_apply` preserves both components, is norm-preserving, and `cmul` agrees with complex multiply | CLAUDE.md's specific hazard, as an assertion |
| `components_preserved` catches a *deliberately* dropped imaginary part | a detector nobody has watched fail is one nobody should trust |
| no device backend auto-selects | the float32 trap above |

**A claim I wrote and then had to retract.** The first draft of
`casim.numerics.linalg` said `batched_matmul` gives the same result as
`np.einsum` "to the last bit". Measured, it does not:

```
max |einsum - matmul|   ~9e-16 absolute
max relative            ~4e-16   (1-2 ULP)      optimize=True does not close it
```

BLAS sums in a different order. That is four orders below `MACHINE_FLOOR`, so
the substitution cannot move any gate the model asserts — but a call site
**cannot be swapped and then called bit-identical**. The roadmap's own risk row
says to record the tolerance rather than hide it, so the docstring states the
measured numbers and the test asserts a bound, not equality.

### C1.5 — The D8 ratchet

`tools/audit_numerics.py --ratchet`, same shape as P1.3's:

Wired into `make gate`. Verified twice by regression: adding one
`import scipy.linalg` to a physics module gives `RATCHET FAILED — scipy 7 -> 8`,
and re-adding one `np.fft.fftn` gives
`RATCHET FAILED — direct np.fft transform calls 0 -> 1`. `make numerics LIST=1`
names what is left. The final counts and why they are split three ways are in
§"The D8 metric, restructured" below.

Exemptions are distinctions, not conveniences: `casim/numerics/**` is where
numpy is *supposed* to be imported; `tools/` and `tests/` are not physics
modules; and **sympy is not scipy** — 63 files do `import sympy as sp`, which an
earlier module-graph regex counted as scipy and reported **1,124 scipy sites
against 13 real ones**. That regex is fixed; miscounting is how a ratchet loses
its authority.

---

## The pause (resolved)

At 12:07 a scan showed **~25 kernel files in `ca-simulation/` and seven files
under `src/casim/` modified within the previous 40 minutes**, including a new
`src/casim/constants/measured.py` — which is C2.3's `MeasuredConstant` escape
hatch, verbatim from this roadmap. A parallel session is executing **C2** right
now. Confirmed with Ben.

The overlap is direct. C1.3's migration list is `ca_colour_dielectric`,
`ca_gluon_self_energy`, `ca_maxwell`, `ca_photon_pair`, `ca_wmu`,
`poisson_open`, `ca_multigrid` — and C2 is rewriting their constants. Migrating
a file another agent is mid-edit on would copy a **half-edited file into
`deprecated/code/` as "the pre-clean original"**, which is the one artifact in
this whole design that has to be trustworthy.

So C1.3 and C1.4 were deferred rather than attempted, and resumed at 13:00
once C2 landed and the tree went quiet. This is the
concurrent-session collision the roadmap's risk table names (F110, F129, F262,
and now this) — and the mitigation it prescribes is exactly what was applied:
**claim the sector before starting.**

---

## Gate state

`make gate` — **16 checks, 28.4 s, all green**, after `make c0 && make manifest`.

During the pause it read 10 of 15, and all five failures were traced rather
than assumed: two were C2's in-flight constants work (`A_OVER_LP`,
`A_OVER_LPLANCK` — truncations of the exact $\sqrt{8\pi}\,3^{1/4}$, which P0's
overview claimed were held to their own precision via a `Site.expected`
override that was in fact `None`), and three were derived indexes stale from
both sessions adding files. The constants failure was **verified pre-existing
by reproducing it with every C1 change stashed** — the check that stops a
"probably not mine" from becoming a wrong assumption.

---

## Findings worth keeping

**The `ca_fft` migration's "drift" was environmental, and proving that mattered.**
Three of 13 baselines moved. All three were at the FFT round-off floor
(2.1e-14 → 2.9e-14) or were `wall_seconds`. Re-running the same test against
the **un-migrated** `ca_fft` produced *identical* deltas — so the cause is that
the committed baselines were made with scipy's FFT and this machine has only
numpy.fft. Exactly the risk the roadmap names: "different FFT libraries differ
in the last bits — invisible in most codebases and fatal in one whose product
is a 1e-12 gate."

That produced two real fixes in `casim.baselines`:

- **`wall_seconds` was being reported as physics drift.** The volatile-key
  regex had `wall(_time|_s|_clock)?` but not `_seconds`. This is the same
  false-positive class P1 fixed for `total_elapsed_s` — the kind that trains
  people to ignore the checker.
- **A relative test at the round-off floor is meaningless.** 2.1e-14 → 2.9e-14
  is a 27% relative change and pure noise. `MACHINE_FLOOR = 1e-12` (quoted from
  `EXACTNESS_CLASSES`: "holds to the float/FFT round-off floor") now classifies
  a pair where *both* values are below it as `kind="floor"` rather than
  `"changed"`. Default is off, so nothing is weakened unless a caller opts in;
  floor deltas are still returned and counted, never dropped.

**A shim defect that would have broken every later migration.** C0's shim
template imported the target without putting `src/` on `sys.path`. Twelve-plus
test files do `sys.path.insert(0, "ca-simulation")` and import a kernel with no
reference to `src/` anywhere, relying on `PYTHONPATH`. Every one would have
started failing with `ModuleNotFoundError: casim` the moment its kernel moved —
a breakage caused entirely by the move. The shim now walks up to find
`src/casim` itself. Verified: `ca_fft` imports through the shim with
`PYTHONPATH` unset.

**Two `tests/runners` files fail for pre-existing CWD reasons.**
`run_10x_tests.py` and `run_propagation_demo.py` fail identically with the
original `ca_fft`. They are two of the 45 files P1 discovered had never been run
at all.

---

## Files

**New**

```
src/casim/numerics/{__init__,fft,backends,linalg,rng,chiral}.py
tools/audit_numerics.py                 D8 ratchet
tools/numerics_health_baseline.json     high-water mark
tools/_batch_verify.py                  resumable test batches (temporary)
deprecated/code/ca_fft.py               pre-clean original
docs/status/C1-completion-overview.md
```

**Modified**

```
src/casim/lattice/backend.py            now a shim onto casim.numerics.backends
src/casim/baselines.py                  MACHINE_FLOOR, floor kind, wall_seconds
tools/migrate_module.py                 shim sys.path bootstrap; floor-aware drift
tools/gen_module_graph.py               scipy regex (sp. is sympy)
tools/run_gate.py                       D8 ratchet check
tests/casim/test_fft_backend_equivalence.py   5 new checks
tests/casim/test_backend.py             library name, no cross-file state leak
Makefile                                `make numerics`
ca-simulation/ca_fft.py                 deprecation shim
```

---

## What C1 does not own

| Item | Status |
|---|---|
| **≥3× wall-clock** on the reference set | **not measurable here.** scipy and pyfftw would not install (35 MB over a throttled link, repeated timeouts), so this machine has numpy.fft only. The threading P2.1 wired is real but unexercised. C1.4's caching gives a measured 1.7–1.9× on the two chiral steppers; that is a component, not the phase target. |
| A second backend clearing the contract | **not provable here.** MLX and CuPy are written and register on availability; neither library exists on a Linux sandbox with no GPU. The contract they must clear is in place and runs. |
| 167 files still importing numpy directly | by design — they clear at **C3–C6** as each file moves into the package. D8's end state is a C9 property, not a C1 one. |
| 42 files importing `ca_fft` | transitional and seam-routed; same C3–C6 clearance. |

The honest summary: **the seam is real, enforced, and now actually used by
every transform in the tree — but its speed claim is untested on this
machine.** Reporting a 3× that was never measured would be the kind of
tidy-looking claim P0 was built to prevent.

## Next

1. **C3** — engine skeleton and the BCC base layer. C1 and C2 are both in, so
   the two substitutions `migrate_module.py` stages (numerics and constants)
   are now real and every later migration gets them for free.
2. On Ben's machine, `make install` (which pulls `.[fast]`) then
   `make backend BENCH=1` — that is where the P2.1/C1 throughput claim actually
   gets its number.
3. **Agree a sector-claim protocol before the next parallel run.** Two sessions
   writing the same files with no lock is the one risk in this roadmap that has
   now fired four times.

---

## C1.3 — Routing the transform calls (completed 2026-07-30 - 13:05)

**161 `np.fft.*` transform sites in 32 files → 0.** Done by
`tools/route_numerics.py`, which substitutes mechanically and then *proves*
three things: the file still parses, no `np.fft.<transform>` survives, and
every substituted name resolves on the façade — checked against the real
module, so a rename in `casim.numerics.fft` cannot leave the tool silently
rewriting calls to something that is not there.

Two deliberate non-targets. **`fftfreq`/`rfftfreq` stay on numpy** (83 sites):
pure index arithmetic, no transform, no threads, no device — routing them adds
diff noise and changes nothing about the seam. And `casim/numerics/` itself,
which is where numpy is supposed to be called.

Binding by location: `ca-simulation/**` gets `import ca_fft as _fft`, the idiom
`ca_bcc`/`ca_gluon`/`ca_wmu` already used and now a shim onto the façade that
also bootstraps `sys.path`; `src/casim/**` gets
`from casim.numerics import fft as _fft` directly. The four `src/casim` files
still importing `ca_fft` (`engine/blockspin`, `engine/coupled`,
`lattice/__init__`) were moved to the façade in the same pass —
`casim.lattice.ca_fft` keeps its public *name* because callers import it, but
now resolves to `casim.numerics.fft` rather than being a second independent
route to numpy.

Two `np.fft.rfft` sites in `ca_casimir.py` needed `rfft`/`irfft`, which the
façade did not have. Added to all five backends rather than left as an
exception.

**Verification.** 111 package tests pass; the four scenarios that exercise the
routed kernels run; and every result artifact was diffed. Two showed
significant drift and **neither is C1.3's**:

| Artifact | Cause |
|---|---|
| `F233_mass_scale_N_transmutation.json` (5e-7) | **C2's**, and correct — `A_OVER_LP` went from the truncated `6.59782` to the exact closed form, a 2.5e-6 relative change that propagates. `ca_alpha_s_running.py` is not in C1.3's routed list. |
| `wmu_phase3.json` (20% `ym_action`) | **pre-existing uncommitted work**, flagged to Ben in the P1 overview with these exact numbers. |

15 further artifacts were rewritten by the verification sweep with no
significant change and were restored, so the working tree carries no spurious
diffs.

## C1.4 — Caching (completed 2026-07-30 - 13:15)

`chiral_core.weyl_step` rebuilt `make_kgrid_3d` **and** the full 2×2 unitary on
every call; `_chiral_branch_rates` rebuilt the k-grid, both dispersion
branches, the Nyquist mask and four transcendental tables on every call. That
was a straight regression against the very kernels the module mirrors —
`ca_bcc` has had `_weyl_cache` and `ca_wmu` `_disp_cache` all along.

None of it depends on the field being propagated, only on
`(shape, sign, block)`.

| | before | after | |
|---|---|---|---|
| `weyl_step` | 4.71 ms | **2.43 ms** | 1.94× |
| `chiral_rs_step` | 13.78 ms | **7.94 ms** | 1.74× |

*(L=32, complex128, numpy.fft, 20-call mean.)*

**The cache changes nothing, and that is asserted rather than assumed.** The
agreement with the audited kernels is *identical* before and after
(`1.4043333874306805e-15` and `1.7763568394002505e-15`, to every digit).
Cached arrays are marked **read-only**, so a caller that mutates one gets a
loud `ValueError` instead of silently corrupting every later tick.
`tests/casim/test_chiral_core_caching.py` pins all of it, including that four
distinct geometries produce four distinct cache entries — a key collision would
serve one geometry's unitary to another.

**A second false claim retracted.** `chiral_core` said it matched
`ca_bcc.weyl_step_3d_bcc` and `ca_wmu.w_propagation_step_chiral`
**"bit-for-bit"**. It does not, and never did: explicit-real multiplication
associates differently from numpy's complex multiply, giving 1.4e-15 and
1.8e-15 — a few ULP, three orders below `MACHINE_FLOOR`, so harmless, but
"bit-for-bit" is a specific claim and this is not it. Verified pre-existing by
measuring with the C1.4 change stashed. The docstrings now state the measured
numbers and a test asserts them, so a change that makes them worse is visible
instead of hidden behind a word.

## The D8 metric, restructured

C1.3 raised the `ca_fft` import count 17 → 42, because 25 kernels traded a
*worse* dependency (direct `np.fft`) for a *better* one (the seam). A single
number that goes **up** while the tree gets **better** is a number nobody would
trust again, so the ratchet now tracks them apart:

```
direct np.fft transform calls        0   <- C1.3's metric; hard 0, ratcheted
files importing numpy/scipy/ca_fft 167
  numpy   167     ca_fft  42 (transitional: routes through the seam)   scipy 7
```

`ca_fft` is exempt from the ratchet *with the reason recorded in the tool* and
becomes `from casim.numerics import fft` as each file moves at C3–C6. Verified:
re-adding one `np.fft.fftn` to `ca_bcc.py` trips it (`0 -> 1`).

**One ratchet was deliberately re-baselined.** `import_time_work` rose 320 →
321 when `test_chiral_core_caching.py` landed. Every test file here needs a
module-level `sys.path` preamble before it can import a kernel, so *adding any
new test* raises that count even when the file is a model citizen — asserting,
falsifiable, no physics at import. The two counts carrying the real signal,
`unfalsifiable` (70) and `no_assert` (232), did not move. The baseline was
moved rather than the file contorted to dodge a proxy, and the reasoning is
recorded in `audit_tests.py` itself so it does not read as goalpost-shifting.
