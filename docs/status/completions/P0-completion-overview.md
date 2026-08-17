# P0 Complete — Ground Truth

*2026-07-30 - 08:52. Phase P0 of `docs/roadmaps/roadmap-unified-program.md`.*

P0 added no physics. It added the ability to **notice when physics changes** —
provenance for the model's constants, a machine-readable record of what
supersedes what, and the repository's first automated gate.

Run it with `make gate` (7.9 s).

---

## What existed before

| | Before P0 | After P0 |
|---|---|---|
| Automated enforcement | **none** — no CI, no Makefile, no tox | `make gate` + `.github/workflows/gate.yml`, 11 checks, 7.9 s |
| Constants with recorded provenance | 0 | 20 |
| Definition sites under regression | 1 (`G_LATTICE`) | 43 recorded, 31 statically enforced |
| Machine-readable supersessions | none (9 prose bullets, one a 2,582-character line) | 7 records, 14 test classifications |
| Superseded tests distinguishable from live | no marker, no skip, no tombstone | 13 banners + `superseded` / `historical_baseline` markers |

---

## Deliverables

### P0.1 — Constants registry (`src/casim/constants/`)

Five modules by sector, 20 constants. **The registry owns provenance, not
values** — per roadmap decision D2 the flat `ca_*.py` kernels remain the single
source of truth for what a constant *is*. What the kernels never recorded, and
this does: which finding fixed it, its exactness class, how it is derived, and
every place in the tree that re-defines it.

```python
from casim.constants import get, value, by_finding
get("delta_star").provenance     # ('F175', 'F253', 'F255', 'F256')
value("G_LATTICE")               # 0.004420970641441538
by_finding("F175")               # [cos3_delta_star, delta_star]
```

**Constants that legitimately disagree are registered separately rather than
reconciled.** This was the main design call. Three examples:

- `f_pi` is **three** constants — the 92.07 model anchor, the 92.4 PDG
  comparison target, and the 92.28 Γ-convention value. Collapsing the first two
  would turn a prediction into an input.
- `sin²θ_W` is **two** — the F45 UV cap $1/4$ and the F49 on-shell $2/9$,
  reconciled by F231. Both are correct at their own scale; before P0 nothing in
  code said which applied where.
- `cos 3δ*` is **two** — the derived $\cos(2/3) = 0.7858873$ and the empirical
  F93-O7 value $0.785874$. The $1.7\times10^{-5}$ gap between them *is* the
  near-coincidence F256 analyses. Merging them would erase the model's own
  honest caveat.

`alpha_eff_star` is stored as the **bracket** $[0.376, 0.411]$ with no value.
The frequently-quoted 0.39 is the midpoint of two scale choices, not an
independently determined number.

Two things fixed in passing: `a/ℓ_P` now resolves to the exact closed form
$\sqrt{8\pi}\,3^{1/4}$ rather than the 5-significant-figure `6.5978` that was
circulating (3.4×10⁻⁶ relative error), with the two truncated sites held to
their own precision; and the lattice↔MeV bridge `GeV_per_lattice_unit`, which
existed only as a code comment, is now a constant you can compute with.

### P0.2 — Consistency test (`tests/casim/test_constants_consistency.py`)

Reads the tree by **AST inspection, never import** — importing a
`tests/findings` module executes its physics and writes JSON, so a provenance
check that imported its subjects would be slow and destructive.

- 34 assertions: every recorded site still agrees; every cited path exists; the
  registry is well formed.
- Two sweeps that catch definitions the registry does not yet know about: a
  `c_lat` sweep (the worst-sprawled constant, ~74 definitions in two spellings)
  and an `f_pi` sweep that fails on any fourth value.
- An `ALLOWLIST` where every entry carries a reason.

**The sweep immediately found two definitions the earlier audit missed** —
`derive_velocity_addition.py` at $1/\sqrt2$ and `forks/curl_fork_cubic.py` at
$1.0$. Both are legitimate (a 2-D square lattice and a simple-cubic fork whose
emergent light speed is the quantity under test) and are now allowlisted with
reasons rather than sitting undetected.

### P0.3 — Supersession ledger (`docs/theory/supersessions.yaml`)

Seven records extracted from `key-decisions.md`, which stays as the human
narrative. Each record carries both sides of the supersession, the code and
tests affected, and — the field that matters most — **what survived**.

Almost nothing in this project is superseded wholesale. F62's gravity-source
claim died; its lapse-mix *sign convention* is production code. F52's
rest-mass sourcing died; its factor-2 discriminator is still canonical under
F178. F106's status changed from fundamental law to static weak-field
reduction; its equations did not change at all.

### P0.4 — Tombstones, at check-level granularity

**This is where the plan changed on contact with the repo.** The roadmap
inherited an audit claim that ~14 test files covered superseded physics and
should be marked. On inspection, **exactly one was superseded wholesale**
(`test_F114_dielectric_black_hole.py`). Of the rest: eleven were partial — a
dead verdict wrapped around live, load-bearing algebra — one was a deliberate
historical baseline, and several were false positives that merely matched a
keyword. `test_F91_pairing_classification.py`, flagged as superseded, *is* the
supersession authority.

Blanket-marking those twelve would have silently retired working coverage. That
would have been worse than the status quo, because it would have looked tidy.

So the unit of supersession is a **check**, not a file:

- `@pytest.mark.superseded` + `addopts = "-m 'not superseded'"` → applies to the
  one fully-superseded file.
- **Docstring banners** naming DEAD and STILL LIVE checks → the other twelve
  keep running. Banners work where markers cannot: 166 of the 272 findings tests
  have no `def test_` at all, so a marker would be invisible to exactly the
  files that most need labelling.
- `tools/apply_supersession_banners.py` generates them from the ledger,
  idempotently, refusing to write if the result would not parse.

Also resolved: `derive_generator_norm_from_F118.py`, which was live code
asserting that λ₆ is *assumed* and E1 is *open* — reversed by the 2026-07-16
decision. Rather than delete it, it now carries a `PRE-DECISION FRAMING` banner.
Its Schur-isotropy proof is the F255 content and stands; its circularity
argument is real, and is precisely *why* the F234 arrow was reversed. That is
worth recording, not erasing.

### P0.5 — The gate

`tools/run_gate.py`, wired to `make gate` and a GitHub Actions workflow.

Three constraints, each learned from the audit:

1. **Fast** — 7.9 s. Long physics stays in `casim test`.
2. **Cannot silently pass.** `casim test` skips every pytest-style file when
   pytest is missing and still reports success. This gate runs its own checks
   standalone in that case and says loudly that it is in reduced mode.
3. **Asserts, never scrapes.** No counting `PASS`/`FAIL` tokens in stdout.

The CI workflow ends with a step that *perturbs `G_LATTICE` and requires the
gate to fail* — a gate nobody has watched fail is a gate nobody should trust.

---

## Acceptance gate — verified

| Criterion | Result |
|---|---|
| Gate green on a clean tree | **PASS** — 11 checks, 7.9 s |
| Every registry constant has a recorded finding | **PASS** — 20/20; enforced |
| Superseded work separated from live | **PASS** — 1 marked, 12 bannered, 1 baseline |
| Perturbing `G_LATTICE` fails the gate | **PASS** — exit 1, names the constant, its provenance, and its derivation |
| Stale banner fails the gate | **PASS** — exit 1 |
| Removed banner fails the gate | **PASS** — exit 1 |
| Orphan banner (tombstone absent from the ledger) fails | **PASS** — exit 1 |

All four negative tests were run against the live tree and the tree restored;
`git diff` confirms the 13 test-file changes are purely additive (153
insertions, 13 docstring-line restructures, zero content removed).

---

## Files

**New**

```
src/casim/constants/{__init__,geometry,gravity,lepton,strong,electroweak}.py
tests/casim/test_constants_consistency.py
tests/casim/test_supersession_ledger.py
tools/apply_supersession_banners.py
tools/run_gate.py
docs/theory/supersessions.yaml
Makefile
.github/workflows/gate.yml
```

**Modified**

```
pyproject.toml            superseded / historical_baseline markers; addopts
tests/conftest.py         marker registration
13 × tests/findings/*.py  supersession banners (additive only)
ca-simulation/derive_generator_norm_from_F118.py   pre-decision framing banner
```

Indexes regenerated. No physics module's behaviour changed.

---

## Known limitations

- **Reduced mode is real.** Without pytest, `test_field_dump_vtk.py` and
  `test_gui_render_spinor.py` are skipped (no `__main__`). CI runs pytest
  explicitly so this path never hides a failure there, but a local `make gate`
  on a bare interpreter is genuinely narrower and says so.
- **12 of 43 sites are not statically checkable** — re-exports, function default
  arguments (`gap_solve(..., Lam3=0.347)`), and values computed at runtime. They
  are recorded for provenance but not enforced. The gate prints the coverage
  number so it is visible rather than assumed.
- **The registry could become a second source of truth.** Mitigated by P0.2, but
  if it starts drifting the right fix is to invert the dependency and have
  kernels import from the registry.
- **`ca_raytrace.py` still computes `F114_enlargement_pct`**, a superseded
  quantity. Recorded in the ledger and deferred to P6.

---

## Next

Critical path is **P0 → P1 → P3.1**. P1 (test and results consolidation) is
next: three honest tiers, closing the assertion deficit in the 174 findings
tests that cannot currently fail, killing import-time side effects, and the
results manifest. P2.1 (add `pyfftw` to `pyproject.toml`) is an afternoon and
speeds up P1's baseline generation, so it is worth doing first regardless.
