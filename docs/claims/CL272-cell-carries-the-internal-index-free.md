---
id: CL272
title: An internal tensor factor costs the model zero spatial directions and zero time directions — the spatial bound depends on the hop's anticommuting rank rather than on the cell dimension, and the enlarged commutant is entirely non-dispersive — so the cell permits the colour index freely, forces its shape, and does not force its existence
slug: cell-carries-the-internal-index-free
tier: supporting
kind: derivation
status: live
domain: [QFT, QCD, SR]
exactness: exact
findings: [F318, F317, F291, F313, F315, F289]
tests: [F318-cell-internal-index]
modules: [casim.engine.lattice.cell_internal_index]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL271
falsifier: stated
first_issued: '2026-08-16'
last_verified: '2026-08-16'
provenance: authored
review_state: authored
confidence: medium
---

# CL272 — The cell carries the internal index for free, and only in one shape

## Statement

Three questions were tangled inside CL271's residual (*that* the quark carries an internal
index). They have three different answers, each measured.

1. **PERMIT — free, on both sides of the signature.**
   *Space:* F291's selector needs the maximal mutually **anticommuting** subset inside the real
   span of the **hop's** traceless-Hermitian part — not the Clifford rank of the cell. Measured:
   one Weyl branch gives span 3 / rank 3; the model's branch-doubled Dirac cell gives span
   **6** / rank **3** (because $\tau_3\otimes\sigma_i$ *commutes* with $\mathbb 1\otimes\sigma_i$);
   an internal factor $\otimes\mathbb 1_N$ gives span 6 / rank 3 on a cell of dimension 12.
   *Time:* the commutant over generic momenta factorises exactly, $2\to18$ at $N=3$ (a factor
   $N^2$), and **every added element is non-dispersive** — literal `0.0`, against the update's
   $0.2846$ — so it is a global internal symmetry, not a second clock.

2. **SHAPE — forced.** A walk that genuinely *uses* five anticommuting generators on $\mathbb C^4$
   has $\ker J=\operatorname{coker}J=0$ at $d=5$, so both F291 selectors return **5**, not 3.
   Enlargements are not all alike: the ones that cost are exactly the ones that add an
   anticommuting generator to the hop, and neither of the model's two (branch doubling, internal
   tensoring) does.

3. **FORCE — not by the cell.** Every space- and time-side verdict is identical at $N=1$ and
   $N=3$ while the commutant dimension is not (2 vs 18). The cell is **indifferent**. What forces
   the index is **derived** Fermi statistics (F289): the totally antisymmetric subspace on one
   nodeless spatial level has dimension $\binom{2N}{n}$ — computed by explicit antisymmetrisation,
   not from the formula — and it is **0 for $n>2N$**. At $N=1$ the cap is **two**, so the tree's
   three-constituent bound state (F122 dynamical, F71 operator, F136 real-space) is impossible
   without an internal index.

## What it extends

Two of the pieces are elementary once stated — the Clifford rank $2k+1$, and the observation that
a non-dispersive commuting unitary is a symmetry rather than a flow. The $\varepsilon$/Pauli
argument in leg 3 is the oldest argument for colour (Greenberg 1964). **No new mathematics is
claimed.**

What is extended is two of the project's own results, in the direction of *removing* a stated
weakness from each:

- **F291 §3 flags its own weakest point:** *"Conditional on $s=2$. For $s=2^k$ the Clifford bound
  is $2k+1$, so a larger cell would relax this to $d\le2k+1$."* On that reading the model's
  $s=36$ quark cell would permit $d\le11$ and S1 would be gone. Measured here, it is not: the
  binding constraint is the hop's anticommuting rank, which the model's real cell does not move.
  F291's honest boundary — *"losing S3 **and** $s=2$ together would reopen the question"* — is
  not reached by anything the model actually does.
- **F313's $d_\text{time}=1$ needs one criterion it does not state**, once the cell carries an
  internal factor: a commuting unitary is a clock only if it **disperses**. Without it the
  enlarged commutant would read as $2N-1=5$ times at $N=3$. The contrast is not hypothetical —
  F313 §9's second commuting flow on the $s=4$ composite *was* dispersive, which is precisely why
  it was a candidate clock and why F315 had to kill it with interactions. The colour elements
  were never candidates.

Neither finding is retracted or edited; both are strengthened (D12).

## Evidence

Record `F318-cell-internal-index` (tier gate, entry `check_cell_internal_index`), **11/11 PASS**,
1.1 s.

| leg | statement | value |
|---|---|---|
| A1 | Clifford rank $2k+1$ at $s=2,4,8$, built and checked for maximality | 3, 5, 7 |
| A2 | the naive bound at the model's $s=36$ quark cell | 11 |
| B1 | one Weyl branch: span / anticommuting rank | 3 / **3** |
| B2 | branch-doubled Dirac cell: span / rank (naive bound 5) | **6** / **3** |
| B3 | $\otimes\mathbb 1_3$, cell dimension 12: span / rank (naive bound 8) | 6 / **3** |
| B4 | converse — a genuine 5-generator walk on $\mathbb C^4$ selects $d$ | **5** (unitarity $2.2\times10^{-16}$) |
| C1 | commutant over generic momenta, $N=1\to N=3$ | 2 → **18** $=2N^2$ |
| C2 | update dispersion vs internal-element dispersion | $0.2846$ vs **`0.0`** (commutes at `0.0`) |
| D1 | 3-constituent antisymmetric state at $N=3$ | $\dim=20$ |
| D2 | ... and at $N=1$ | $\dim=\mathbf 0$ — excluded |
| D3 | verdicts identical at $N=1$ and $N=3$; commutant not | 3 = 3; 2 ≠ 18 |

**Four declared controls, each verified red and red only where declared:**
`internal_dispersive=true` → B3+C1+C2 (**the measured set, not the anticipated one** — C2 alone
was expected); `n_constituents=2` → D2; `max_clifford_k=1` → A1; `n_int=1` → D1, with every space
and time leg staying green, which is leg 3's indifference visible in one run.

## Falsifier

1. **Any step of the hop found to read the internal index.** Made to fire: `internal_dispersive=true`
   reddens three legs together.
2. **A model enlargement that adds an anticommuting generator to the hop.** B4 shows the selector
   then returns $2k+1$ rather than 3, leaving F291's S3 alone — F291's own stated boundary.
3. **A stable tree bound state with a number of constituents other than three**, or a
   three-constituent state whose spatial ground state is not nodeless. `n_constituents=2` shows
   the argument is genuinely sensitive to the number.
4. **A demonstration that the cell is not a tensor product** — that colour is entangled with the
   walk's index rather than factorised. Everything above assumes the factorisation, which is how
   `strong.py` implements it.

## Status & history

**2026-08-16 — first issued** with F318, the same day as CL271, to which it rolls up.

`status: live`, `confidence: medium`. The reason is stated rather than implied: leg 3 consumes
*"the matter sector contains a three-constituent bound state"*, and **CL271's own leg for $N=3$
consumes the same fact**. The two cards therefore do **not** independently confirm each other,
and a reader must not count them twice. The number three is not derived by either.

§C's commutant is measured in momentum space over seven probe momenta rather than over F313's
Laurent ring. The added elements are constants, hence degree-0 Laurent and local by F313's own
definition, so the extension is expected to be exact — but it is not re-derived on that footing.

## Sources

- `findings/F318-cell-carries-the-internal-index.md` — the finding, §5 stating prior art leg by leg
- `src/casim/engine/lattice/cell_internal_index.py` — the module
- `tests/findings/test_F318_cell_internal_index.py`, record `F318-cell-internal-index` → `test-results/F318_cell_internal_index.json`
- **CL271** — the card whose residual this reshapes; [[F317-su3-structure-derived]]
- [[F291-why-three-plus-one-dimensions]] (and **CL246**), [[F313-time-signature]] (and **CL269**), [[F315-V-does-not-survive-interaction]], [[F289-spin-statistics-connection]], [[F122-p2-dynamical-baryon-three-body]]
- External: Greenberg, *Phys. Rev. Lett.* **13** (1964) 598
