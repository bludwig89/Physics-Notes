# F323 — The lattice anisotropy is derived, not chosen, and F299's d=4 Casimir successor runs

**Date:** 2026-08-17 - 22:05
**Session:** `keen-lucid-symanzik`
**Sector:** gauge
**Status:** Confirmed — 28/28 PASS, **five** declared controls each verified `CONTROL` on a distinct measured red set
**Module:** `src/casim/engine/gauge/bcc_action.py`
**Test record:** record `gauge-bcc-mc-d4` (tier gate, `casim test --id gauge-bcc-mc-d4`) — the five declared controls are F323's own content: `hypercubic_anisotropy` reddens X1c/X1d (the derived BCC ratio against the textbook one) and `unsymmetrised_reps` reddens K1a (F299's d=4 Casimir characters). Field renamed from `**Record:**` on 2026-08-19 so `check_finding_records.py` and `make coverage` can read it.
**Script:** `tests/findings/test_bcc_gauge_mc_d4.py` (driver only; the contract is the record)
**Battery:** `run-bcc-confinement-d4` → `tests/runners/run_bcc_confinement_d4.py --casimir`
**Results:** `test-results/bcc_gauge_mc_d4.json`, `test-results/bcc_confinement_d4.{json,md}`
**Cross-references:** F265 (the BCC action and its exact simple-cubic kernel), F313/F316 (the update's commutant; primitivity), F291 (the spatial selectors), F299 (the Casimir discriminator and the successor spec), F298 (the Casimir ladder), F94 (the superseded hypercubic d=4 leg — ledger `S20`), F284 (the ratio `r = 1/c_lat`), F311 (F94's baseline adjudication)

---

## 1. What this closes

The predecessor session added a 3+1D sampler and Wilson loops to `bcc_action.py`
and left two things explicitly open. Both are now closed, and one prior claim of
the tree's is corrected.

1. **The anisotropy was a flagged convention.** `beta_t = beta_s`, i.e.
   `xi = a_s/a_t = 1`, was carried as a stated non-derivation. It is derived here.
2. **F299's d=4 successor was specified and unrun.** F299's own "Remains" item 2
   reads: *"Run F94 at `beta in [5.8, 6.2]` with the three character polynomials
   above and measure where Casimir scaling gives way to screening. No new
   sampling; parameters in `mc_reach()`."* It now runs.
3. **Completeness row H8 is stale on one point.** It records *"F299's claimed
   gate record does not exist."* It was armed 2026-08-07 and passes. Recorded
   here so the next completeness sweep can drop that clause; nothing else in H8
   is contradicted.

---

## 2. The anisotropy, derived

The derivation has two halves that do different jobs, and conflating them is the
error to avoid.

### 2.1 What licenses a *fixed* `a_t` — primitivity, and it supplies no value

On an ordinary anisotropic lattice `a_t` is a tunable and one takes `a_t -> 0`.
Here it is not. F313 proves the update `A` is the **fundamental** unit of
`ker(det)`, and the review's blind agent proved it **primitive** — there is no
local half-tick, so the tick has no root inside the local homogeneous algebra and
cannot be refined. `a_t` is therefore a fixed quantity to be *computed*, not a
limit to be taken.

This is the load-bearing use of F313 in this finding, and it is worth being
precise that it is the *only* one: primitivity licenses the question and does not
answer it. The previous session's speculation that primitivity might *fix* `a_t`
is withdrawn here in favour of this weaker and correct statement.

### 2.2 What fixes its value — isotropy of the weak-field limit

Expand the two loop classes to `O(Phi^2)` with a physical step `lambda` per unit
integer coordinate. Two independent closure identities of the BCC geometry do the
work, and both are exact over `Z`:

| identity | vectors | value |
|---|---|---|
| `sum_p m_p m_p^T` | the 6 `<110>` rhombus half-normals (F265) | `4 I` |
| `sum_a a a^T` | the 4 `<111>` link axes | `4 I` |

With `Phi_p = 2 m_p . f` and `|f| = |B|` (the module's own reconstruction
relation), and `Phi = g lambda a_t (a . E)` for the mixed rectangle:

```
  6 rhombi   sum (1 - Re tr P/N)  ->  8 g^2 lambda^4 |B|^2
  4 mixed    sum (1 - Re tr P/N)  ->  2 g^2 lambda^2 a_t^2 |E|^2
```

Euclidean isotropy is equality of the `E^2` and `B^2` coefficients, hence

> **`beta_t / beta_s = 4 lambda^2 / a_t^2`.**

The emergent light cone closes it. One tick moves amplitude one hop; the hop has
length `lambda sqrt3`; the emergent signal speed is `c_lat`, a **group** velocity
and not the raw hop rate. In units `c = 1`, `a_t = c_lat lambda sqrt3`, so

> **`beta_t/beta_s = 4/(3 c_lat^2) = 4`  and  `xi = 1/c_lat = sqrt3`**, exact at
> the model's `c_lat^2 = 1/3`.

### 2.3 The number that is actually new

On a hypercubic lattice the standard relation is `beta_t/beta_s = xi^2`. Here it
is **`(4/3) xi^2`**. The `4/3` is BCC geometric content — traceable to the
rhombus carrying `|d1 x d2| = 2 sqrt2` against the mixed rectangle's `|d| = sqrt3`
— and a naive hypercubic substitution would have been wrong by a third. That
factor is leg `X1d` and it is what control `hypercubic_anisotropy=true` reddens.

Two consistency notes, neither of them a new number:

- `a_t^2 = c_lat^2 * 3 = 1`, so **in the integer cubic embedding `a_t = lambda`
  exactly**: the lattice is isotropic in *coordinate* units and the whole
  anisotropy is the `<111>` hop length. This is why the predecessor's `a_t = 1`
  default was accidentally right while its `beta_t = beta_s` was wrong.
- `xi = 1/c_lat = 3^(1/2)` reproduces **F284's `r = 1/c_lat`** by a route that
  never mentions cosmology. That is a cross-check on both, not a new result.

### 2.4 Measured, not just derived

A constant-`F` abelian configuration is put on the lattice (linear potential
`A_nu(X) = (1/2) X^mu F_mu_nu`, for which the midpoint rule is exact, so the link
phase is exactly `(g/2) X^mu F_mu_nu H^nu` — the `H F H` term drops by
antisymmetry). Reading `S_B/S_E` at equal field magnitude:

| `g` | measured `beta_t/beta_s` | residual | residual/`g^2` |
|---|---|---|---|
| 4.0e-3 | 3.999996000141 | 9.9996e-7 | **0.0625** |
| 2.0e-3 | 3.999998999398 | 2.5015e-7 | **0.0625** |
| 1.0e-3 | 3.999999745537 | 6.3616e-8 | 0.0636 |

The truncation coefficient is **exactly `1/16`**, held to four digits over a
factor two in `g`, so the deviation is a closed-form quartic term and not noise.
One Richardson step removes it: the extrapolated ratio is `3.99999999908`,
residual `2.3e-10` (leg `X1c`). The `g -> 0` limit is the identity.

---

## 3. F299's d=4 Casimir successor

### 3.1 Two engine gaps, not physics, were what blocked it

- **The three character polynomials had never been applied to a loop matrix.**
  They live in `casimir_scaling.mc_reach` as expressions in the three *torus
  eigenvalues*, verified against a 2D quadrature — never against a Wilson loop
  in any dimension.
- **No function returned the traces needed to evaluate them.**
  `lgt_fork_A_mc.wilson_loop_planar` ends on `np.real(np.trace(acc))/3` averaged
  over sites, so the matrix field is local and discarded;
  `polyakov_loop_field` returns `Tr W` only, i.e. the first power.

`wilson_loop_traces_rt` supplies `Tr W`, `Tr W^2`, `Tr W^3` from a genuine
`R x T` loop matrix, and `higher_rep_loop_table` builds the reps from them.
The extra cost over the fundamental is two matrix products — F299's *"no new
sampling — the same configurations, a different trace"* is met literally.

### 3.2 The cross-check the tree had never run

F299's polynomials were verified against `rep_character`, the Jacobi–Trudi
determinant that **produced** them. That is self-consistency: it cannot catch a
wrong symmetrisation, because both sides would carry it. Here they are checked
against **explicit representation matrices** — `Sym^2` and `Sym^3` by
symmetric-subspace isometry from the fundamental, and the adjoint by
`Ad(U)_ab = 2 tr(T_a U T_b U^dag)`:

| rep | polynomial | explicit construction | dim | worst residual |
|---|---|---|---|---|
| 6 | `[(Tr W)^2 + Tr W^2]/2` | `Sym^2` isometry | 6 | 1.24e-16 |
| 8 | `Tr W . Tr W^dag - 1` | `Ad(U)_ab = 2 tr(T_a U T_b U^dag)` | 8 | 4.62e-16 |
| 10 | `[(Tr W)^3 + 3 Tr W Tr W^2 + 2 Tr W^3]/6` | `Sym^3` isometry | 10 | 4.44e-16 |

`chi_8` is written with `Tr W^dag` rather than `|Tr W|^2` deliberately. The
identity `Tr(W^dag) = conj(Tr W)` is unconditional, but the adjoint character
equalling `|chi_F|^2 - 1` is a statement about SU(3), so the conjugate is written
out to keep the group assumption visible.

`C_2(R)/C_F` is computed from the Dynkin labels rather than tabulated, and
reproduces F299's table exactly over `Q`: **1, 5/2, 9/4, 9/2** (leg `K1c`).

### 3.3 First measurement — PRELIMINARY, and labelled so

`L = Lt = 6`, SU(3), `beta_s = 5.9` (F299's scaling window), `beta_t` from the
derived ratio, **3 configurations**:

| `R x T` | `sigma_6/sigma_3` | 5/2 | `sigma_8/sigma_3` | 9/4 | `sigma_10/sigma_3` | 9/2 |
|---|---:|---:|---:|---:|---:|---:|
| 2 x 2 | 2.4660 | 2.5 | 2.2243 | 2.25 | 4.3776 | 4.5 |
| 3 x 2 | 2.5091 | 2.5 | 2.2351 | 2.25 | 4.6677 | 4.5 |
| 2 x 3 | 2.6450 | 2.5 | 2.3196 | 2.25 | 5.1413 | 4.5 |
| 3 x 3 | 2.2838 | 2.5 | 2.1388 | 2.25 | 3.6318 | 4.5 |

Read narrowly: at the smaller loops all three rungs sit within a few percent of
the exact Casimir line (`-1.4%`, `-1.2%`, `-2.7%` at `2 x 2`), and at the largest
available loop all three fall **below** it, most steeply for the decuplet
(`-19%`). A downward departure at larger `R` for the higher reps is the sign
screening would have, and the triality-0 reps are the ones that must break.

**This is not a claim.** Three configurations, no error estimate, a `6^4` lattice
and `R <= 3`; the `2 x 3` versus `3 x 2` asymmetry is by itself larger than the
effect being read at `3 x 3`, which is the honest measure of how little this
resolves. What is established is that the *measurement now exists and is
correctly normalised*; where Casimir scaling gives way to screening needs the
production run, and that is a battery record.

---

## 4. What is NOT claimed

- **No area law and no string tension.** Completeness row B7's residual is a
  missing transfer matrix with positivity — `reflection positiv`, `Osterwalder`,
  `Schrader` and `cluster expansion` return zero hits repo-wide — and no amount
  of sampling supplies one. Nothing here moves that.
- **`c_lat` is an input**, not re-derived.
- **The anisotropy matching is TREE LEVEL.** Isotropy of the classical
  weak-field limit fixes the *bare* couplings. Radiative corrections to the
  anisotropy — the Karsch coefficients of the hypercubic literature — are not
  computed, and at a working `beta` they are not negligible.
- **The screening crossover is not located.** §3.3 is preliminary and says so.
- **Casimir scaling is not asserted to hold asymptotically.** It must not, for
  triality 0; that is the physics being looked for.

## 5. Falsifiers

1. A production run in `beta in [5.8, 6.2]` that reproduces `beta_t/beta_s = 4`'s
   isotropy prediction *worse* than the hypercubic `xi^2 = 3` would falsify §2 —
   the two differ by a third and are not close.
2. A measured `sigma_6/sigma_3` that stabilises away from `5/2` at intermediate
   `R` with adequate statistics, while `sigma_8` and `sigma_10` stay *on* the
   Casimir line, would contradict the triality reading rather than support it.
3. If the `g^2` truncation coefficient in §2.4 is not `1/16` on a finer grid, the
   `O(Phi^2)` expansion in §2.2 has a missing term and the ratio is not `4`.

## 6. Sources

- `src/casim/engine/gauge/bcc_action.py` — `anisotropy_from_c_lat`,
  `constant_field_links_4d`, `weak_field_isotropy`, `bcc_closure_identities`,
  `wilson_loop_traces_rt`, `rep_character_from_traces`, `sym_power_rep`,
  `adjoint_rep`, `character_identity_residual`, `higher_rep_loop_table`,
  `casimir_scaling_from_loops`, `check_bcc_gauge_mc`
- `findings/F299-casimir-scaling-discriminator-reinstated.md` §4 and "Remains" 2
- `findings/F313-one-time-dimension-from-the-update-commutant.md`,
  `docs/reviews/F313-review-2026-08-13.md` (primitivity)
- `findings/F265-bcc-gauge-geometry.md` (the `sum_p m_p m_p^T = 4 I` identity)
- `docs/theory/supersessions.yaml` `S20` (F94's hypercubic action)
