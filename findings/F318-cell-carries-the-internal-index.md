# F318 — The cell carries the internal index for free, and only in one shape: the bound F291 flagged as conditional on $s=2$ is **not** conditional on $s=2$, the commutant F313 counted grows by exactly $N^2$ **non-dispersive** elements, and what forces the index to exist is not the cell but Fermi statistics

**Date:** 2026-08-16 - 07:25
**Numbering:** **F318**, taken as `NEXT FREE NUMBER` (max+1; no gap closed). Session `keen-lucid-gell-mann-2`, sector `lattice`.
**Status:** Confirmed — **11/11 PASS** (1.1 s), **four** declared controls each verified red **and red only where declared** (the measured red-sets are recorded, not the expected ones — `internal_dispersive` reddens **three** legs, not the one anticipated). Four residuals are literal `0.0`; the rest are ≤ 2.3×10⁻¹⁶.
**Verdict:** F317's residual — *that* the quark carries an internal index — is **not closed, and is moved**. Three questions were tangled in it and they have different answers: the cell **permits** the index at zero cost, **forces its shape**, and does **not force its existence**. The forcing comes from the model's own derived Fermi statistics, and the input that remains is smaller and more concrete: *that the matter sector contains a three-constituent bound state.*
**Side effects on two existing findings, both strengthenings, neither a retraction:**
- **F291's self-flagged weakest point is removed.** Its §3 reads *"Conditional on $s=2$. For $s=2^k$ the Clifford bound is $2k+1$, so a larger cell would relax this to $d\le2k+1$."* Measured here: the model's actual $s=36$ quark cell does **not** relax it. The bound that S1 needs is the anticommuting rank of the **hop's own span**, which is 3 at every factor the model adds.
- **F313 needs one criterion it does not state, and now has it.** Its $d_\text{time}=1$ would read as $2N-1=5$ on a coloured cell, because the commutant grows. It does not, because every added element is **non-dispersive**. A commuting unitary is a clock only if it disperses.

**Modules:** `src/casim/engine/lattice/cell_internal_index.py` (new)
**Test / results:** record `F318-cell-internal-index` (tier gate, entry `check_cell_internal_index`), driver `tests/findings/test_F318_cell_internal_index.py` → `test-results/F318_cell_internal_index.json`
**Cross-references:** [[F317-su3-structure-derived]] (the residual this attacks, and the attack it named), [[F291-why-three-plus-one-dimensions]] (S1/S2 and the conditionality removed here), [[F292-no-higher-multiple-of-three]], [[F313-time-signature]] (the time count and its minimal-cell scope), [[F315-V-does-not-survive-interaction]] (why the *branch* composite's second flow needed killing and the colour elements never did), [[F289-spin-statistics-connection]] (Fermi statistics derived, not imported — §D would be circular without it), [[F122-p2-dynamical-baryon-three-body]] / [[F71-colour-singlet-baryon-proton]] / [[F136-colour-triplet-dirac-quark-confinement]] (the three-constituent state §D consumes), [[F27-complex-mass-chiral-su2]] (the branch-coupling mass step).

---

## 0. Three questions that were being asked as one

F317 §10 named this attack in one sentence. Reading it carefully, it contains three questions with three different answers, and most of the value here is in refusing to merge them:

| | question | answer |
|---|---|---|
| **PERMIT** | does an internal factor cost the model anything? | **No — zero, on both the space and the time side.** §B, §C |
| **SHAPE** | if the cell is enlarged, must the enlargement be internal? | **The shape is forced.** An enlargement that adds an anticommuting generator to the hop moves $d$ from 3 to $2k+1$. §B4 |
| **FORCE** | does anything make the index *exist*? | **Not the cell.** The cell is measurably indifferent. §D3 |

---

## 1. §A — the naive bound, computed rather than quoted

`dimensionality.max_anticommuting_traceless_hermitian` **raises** for $s\neq2$, so F291's own general remark has never been run. Built here by Jordan–Wigner and verified constructively (mutually anticommuting, Hermitian, traceless, squaring to $\mathbb 1$, all residuals `0.0`):

| $s$ | Clifford rank | $2k+1$ |
|---:|---:|---:|
| 2 | 3 | 3 |
| 4 | 5 | 5 |
| 8 | 7 | 7 |

**A2.** On the naive reading, the model's $s=36$ quark cell would permit $d\le\lfloor2\log_2 36+1\rfloor=\mathbf{11}$, and F291's S1 would simply be gone. That is the worry F317 inherited, stated at full strength before it is answered.

---

## 2. §B — the naive bound is the wrong bound, and the right one does not move

A spatial direction cannot come from anywhere except the **hop**: the mass step is on-site and contributes no $k$-dependence, so it never enters $J$. And what S1 needs is not linear independence but **anticommutation** — F291 §2's own observation that *"anticommuting is Euclidean orthogonality in $\mathbb R^3$"*. So the quantity to measure is the maximal mutually anticommuting subset inside the real span of the hop's traceless-Hermitian part.

Measured over seven probe momenta:

| cell | span of the hop's traceless part | **anticommuting rank** | naive cell bound |
|---|---:|---:|---:|
| **B1** one Weyl branch ($s=2$) | 3 | **3** | 3 |
| **B2** branch-doubled, the model's massless Dirac cell ($s=4$) | **6** | **3** | 5 |
| **B3** $\otimes\,\mathbb 1_3$, i.e. with colour ($s=12$) | 6 | **3** | 8 |

**B2 is the result.** Branch doubling *widens the span* from 3 to 6 — the two chiralities carry different Bloch vectors, so both $\mathbb 1\otimes\sigma_i$ and $\tau_3\otimes\sigma_i$ appear — and yet adds **no** anticommuting direction, because $\tau_3\otimes\sigma_i$ **commutes** with $\mathbb 1\otimes\sigma_i$. Six linearly independent generators, three mutually anticommuting ones.

**B3 is the easy half.** An internal factor tensors $\mathbb 1_N$ onto every generator, which changes neither the span's dimension nor any commutator.

> **F291's flagged conditionality is therefore weaker than it needed to be.** S1 is not conditional on $s=2$; it is conditional on the *hop's anticommuting rank* being 3, and that is 3 for the model's real 36-dimensional quark cell. S2's cokernel argument rides on the same 3-dimensional target space and moves with it. F291's own honest boundary — *"losing S3 and $s=2$ together would reopen the question"* — is not reached by anything the model actually does.

### B4 — the converse, which is what stops all of that being vacuous

Take the five Clifford generators on $\mathbb C^4$ and build $A(\mathbf k)=u\mathbb 1+i\sum_a n_a(\mathbf k)\Gamma_a$. Unitarity is *exact* because the $\Gamma$'s anticommute, so $(\mathbf n\cdot\Gamma)^2=\lVert\mathbf n\rVert^2\mathbb 1$ (family unitarity residual $2.2\times10^{-16}$). Then $J$ is $5\times d$ and F291's two selectors read straight off it:

| $d$ | rank $J$ | $\dim\ker J$ | $\dim\operatorname{coker}J$ | both vanish? |
|---:|---:|---:|---:|---|
| 3 | 3 | 0 | 2 | no |
| 4 | 4 | 0 | 1 | no |
| **5** | **5** | **0** | **0** | **yes** |
| 6 | 5 | 1 | 0 | no |

**The selector returns 5, not 3.** So enlargements are genuinely not all alike. The ones that cost are exactly the ones that add an anticommuting generator to the hop — and neither of the model's two does.

---

## 3. §C — the time side, which could have broken and does not

F313 counts time directions by the commutant of the update. An internal factor **enlarges** that commutant, and a naive reading would therefore report several times on a coloured cell. Measured, over generic momenta:

| cell | commutant over many $\mathbf k$ |
|---|---:|
| one branch, $N=1$ | 1 |
| one branch, $N=3$ | 9 |
| branch-doubled, $N=1$ | 2 |
| **branch-doubled, $N=3$** (the model's quark cell shape) | **18** |

It factorises exactly: $\dim\mathcal C = \dim\mathcal C_{\text{branch}}\times N^2$. At $N=3$ the commutant is nine times larger, and a maximal abelian subalgebra of it would suggest $2N-1=5$ time directions.

**C2 is why that reading is wrong, and it is one measurement.** A commuting unitary is a *clock* only if its eigenphase depends on momentum:

$$\text{update: } \Big|\frac{\partial\phi}{\partial k}\Big| = 0.2846 \qquad\text{internal element: } \Big|\frac{\partial\phi}{\partial k}\Big| = \mathbf{0.0}\ \text{(literal)},$$

with the internal element commuting with the hop at literal `0.0` across every probe momentum. **A non-dispersive commuting unitary is a global internal symmetry, not a second time direction.** So F313's $d_\text{time}=1$ survives the internal factor — **given a criterion F313 does not state**, because it never had an internal factor to need it.

The contrast is not hypothetical, and it is the reason this section exists. F313 §9's second commuting flow on the $s=4$ composite **was** dispersive — that is exactly why it was a candidate clock, why F313 could only call it a *reading*, and why F315 had to go and kill it with interactions. The colour elements were never candidates. The declared control `internal_dispersive=true` puts a $k$-dependence into the internal factor and reproduces the F313 §9 situation: C2 goes red, and so do B3 and C1 with it.

---

## 4. §D — what forces the index, and it is not the cell

**D3, the honest negative, written as a check rather than a sentence.** Every space- and time-side verdict is *identical* at $N=1$ and $N=3$ (anticommuting rank 3 either way) while the commutant dimension is *not* (2 vs 18). The cell neither forbids nor requires the index. It is **indifferent**, and that is measured rather than conceded.

So the forcing must come from elsewhere, and it does. The spatial ground state of any binding kernel is nodeless, hence totally **symmetric**; the model's Fermi statistics is **derived** (F289 supplies the spin-statistics theorem's own two premises — $R(2\pi)=-\mathbb 1$ from the rotor, $\pi_1=S_n$ from the derived $d=3$ — so this is not an imported rule); therefore the whole antisymmetry must be carried by spin ⊗ internal. Building the antisymmetriser explicitly and taking its rank (**not** evaluating the binomial, which is the answer being checked):

| $N$ | one-particle states $2N$ | $\dim\Lambda^3$ | 3-constituent state exists? |
|---:|---:|---:|---|
| **1** | 2 | **0** | **no** |
| 2 | 4 | 4 | yes |
| 3 | 6 | 20 | yes |

$$\boxed{\ \text{spin alone caps a nodeless level at \textbf{two} identical constituents.}\ }$$

The tree *has* a three-constituent bound state — F122 builds it dynamically, F71 as an operator, F136 in real space — and at $N=1$ it does not exist. **So the internal index is forced to exist**, with $N\ge2$; F317 §6's $\Lambda^3$ singlet count (a singlet at exactly one $N$, and it is 3) then fixes $N=3$.

**The control that makes D2 a statement rather than a truism:** `n_constituents=2` reds D2 alone. At two constituents the $N=1$ cell is perfectly adequate — the spin singlet does the antisymmetrising — so the cap forces nothing. The forcing is a statement about **three**, and this is the check that says so.

---

## 5. Prior art, and what is actually new

| leg | prior art | what is new here |
|---|---|---|
| §A Clifford rank $2k+1$ | standard (Clifford algebra representation theory) | it is **run**, where the tree's own function raises for $s\neq2$ — F291 quotes the general answer without computing it |
| §B the gauge/anticommutation distinction | F291 §2 already says anticommuting is orthogonality in $\mathbb R^3$ | applying it to the **hop's span** rather than the cell, and measuring that branch doubling widens the span (3→6) **without** raising the rank. That is the load-bearing measurement and it removes F291's own flagged conditionality |
| §C dispersion distinguishes symmetries from flows | elementary once stated | F313 did not state it and did not need to; on a coloured cell it is exactly what stands between $d_\text{time}=1$ and $d_\text{time}=5$. The $0.2846$ vs literal `0.0` contrast is the statement |
| §D the Pauli/$\varepsilon$ colour argument | the oldest argument for colour (Greenberg 1964) | the antisymmetry premise is **derived in-tree** (F289), the occupancy dimension is **computed** by explicit antisymmetrisation across $N=1,2,3$ rather than quoted, and it is used to answer a *different* question — not "why three colours" but "why an index at all" |

**No new mathematics is claimed.** What is claimed is that three questions that had been asked as one have three different, measured answers.

---

## 6. Falsifiers

1. **Any step of the hop found to read the internal index.** Then B3 fails, the commutant shrinks, and — if the reading is $k$-dependent — C2 fails and a second clock appears. Made to fire: `internal_dispersive=true` reddens B3, C1 and C2 together.
2. **A model enlargement that adds an anticommuting generator to the hop.** B4 shows the selector then returns $2k+1$ rather than 3, and F291's S1∧S2 route no longer selects 3 — leaving S3 alone, which is F291's own stated boundary.
3. **A stable bound state in the tree with a number of constituents other than three**, or a three-constituent state whose spatial ground state is *not* nodeless. Either changes §D's arithmetic; `n_constituents=2` shows the argument is genuinely sensitive to the number.
4. **A demonstration that the model's cell is not a tensor product** — that colour is not a factor but is entangled with the walk's index. Everything above assumes the factorisation, which is how `strong.py` implements it.

---

## 7. What this closes, and what remains

**Closes.**

* F317's residual is **reshaped**: the cell permits the index at zero cost, forces its shape, and the index's *existence* is forced by derived Fermi statistics plus the model's three-constituent bound state.
* **F291's self-flagged weakest point.** "Conditional on $s=2$" becomes "conditional on the hop's anticommuting rank", measured at 3 on the model's real cell. F291 is left **bit-unchanged** (D12); its claim card carries the amendment.
* **F313 gains the criterion** its time count needs on a cell with an internal factor, and the criterion is satisfied at literal `0.0`.

**Remains, and is the honest headline.**

1. **The number three is not derived here.** §D consumes "the matter sector contains a three-constituent bound state". That is a smaller and more concrete input than "an internal index exists", and it is in-tree (F122/F71/F136) rather than in a table of hadron masses — but it is still an input, and F317 §6's own empirical leg is the same one. The two findings do **not** independently confirm each other; they consume the same fact.
2. **Why the cell is a tensor product at all** is untouched. Falsifier 4.
3. **Nothing here bears on B10's three closed routes** (anomaly, spatial-3, $\mathbb Z_3$), on the **X1** colour-normalisation fork, or on the $d=3$ result itself — §B *strengthens* F291's route rather than replacing it.
4. **§C's commutant is measured in momentum space over seven probe momenta**, not over F313's Laurent ring. The added elements are constants, hence degree-0 Laurent and local by F313's own definition, so the extension is expected to be exact — but it is not re-derived on that footing here.
