# F277 — The F272 refold defect was in four places, and in vacuum polarization it flipped a sign

*2026-08-02 - 07:19. Closes audit-V item **V-023** (`docs/audits/physics-audit-report-2026-08-01.md` §V4.4).*
*Status: **established** (measured, fixed, grid-convergence verified, guarded). Extends [[F272]] to the QED and gluon sectors.*

## 1. Claim

F272 removed `((k+π) % 2π) − π` from `gauge/bgfield_loop._Bcoeff_numeric` because
the rule kernel's period lattice is $\sqrt3\cdot$fcc (F267), not $2\pi$ per axis, so
the wrap sent $k+q$ to a **genuinely inequivalent momentum**. Audit V found the
identical line still live in three more modules. A full-tree sweep in this session
found a **fourth**, in a runner the audit did not scan:

| site | branch | status |
|---|---|---|
| `interactions/qed_vacuum_polarization.py:292` (`_fermion_B`) | `kernel='rule'` | **fixed** |
| `interactions/qed_electron_self_energy.py:430` (`_selfenergy_AB`) | `kernel='rule'` | **fixed** |
| `gauge/gluon_self_energy.py:173` (`_bubble`) | **unconditional** | **fixed** |
| `tests/runners/run_d1_vertex_formfactor.py:135` (`_Bcoeff_lattice_ff`) | both kernels | **fixed** (new; not in the audit's list) |

All four evaluate the same kernel, $K = 3\,\Omega_\text{even}^2 + k_t^2$. Measured
shift-invariance of $K$, 200 random $k$, $\max\lvert\Delta K\rvert$:

| shift | result |
|---|---|
| $2\pi(1,0,0)$ — the refold | **71.58** — not a period |
| $2\pi(1,1,0)$ — plain fcc | **34.59** — not a period |
| $\sqrt3\cdot2\pi(1,1,0)$ | $1.4\times10^{-14}$ — **PERIOD** |
| $\sqrt3\cdot2\pi(2,0,0)$ | $1.9\times10^{-14}$ — **PERIOD** |

**No refold was needed anywhere.** $K$ is a closed form valid at any $k$, so the
unwrapped shift already returns the periodic-correct value. Folding is an
array-indexing device and there is no array being indexed at any of the four sites.

## 2. Vacuum polarization: the sign was wrong

$\Delta = B_\text{rule} - B_\text{cont}$ at $Q=0.3$. The refold's damage switches on
exactly at $Q > \pi/n$, which is $n \gtrsim 10$ here:

| $n$ | with refold | without |
|---:|---:|---:|
| 10 | $-2.0182\times10^{-3}$ | $-2.0182\times10^{-3}$ |
| 14 | $\mathbf{+8.578\times10^{-3}}$ ← **sign flip** | $-2.0916\times10^{-3}$ |
| 18 | $+1.1930\times10^{-2}$ | $-2.1151\times10^{-3}$ |
| 22 | $+1.2455\times10^{-2}$ | $-2.1209\times10^{-3}$ |
| 26 | $+1.2055\times10^{-2}$ | $-2.1214\times10^{-3}$ |

The refolded quantity changes sign between $n=10$ and $n=14$ and settles at the
**opposite sign and ~6× the magnitude**. Without it, $\Delta$ converges monotonically
to $-2.1214\times10^{-3}$ (0.02% between $n=22$ and $n=26$). This reproduces F272's
diagnostic signature term for term, at the same $Q=0.3$ and the same threshold.

**What it cost was the function's claim.** `lattice_b0_consistency` exists to show
$\Delta$ is $q$-flat, because a residual log would make $\Delta$ grow like
$\ln(1/Q)$ and $q$-flatness is what establishes $b_0^\text{QED}$ as
propagator-independent. At the shipped $n=24$:

| quantity | with refold | without |
|---|---:|---:|
| `delta_spread` (the flatness gate) | $1.4484\times10^{-2}$ | $\mathbf{1.685\times10^{-5}}$ |
| `delta_mean` | $+3.865\times10^{-3}$ | $-2.110\times10^{-3}$ |

A factor of **859** in the spread, and the mean's sign flips. As in F272, the wrap
manufactured a spurious $q$-dependence indistinguishable from the very residual log
the test exists to detect — and it did so while the test still reported PASS,
because the tolerance is $5\times10^{-2}$.

## 3. Electron self-energy: milder, and now flat

The shift is $KX-P$ with small $P$, so fewer grid points cross the face. $\mathrm{d}A$
drifted with refinement instead of converging; $\mathrm{d}B$ was nearly stable:

| $n$ | $\mathrm{d}A$ refold | $\mathrm{d}A$ fixed | $\mathrm{d}B$ refold | $\mathrm{d}B$ fixed |
|---:|---:|---:|---:|---:|
| 10 | $2.290\times10^{-4}$ | $2.290\times10^{-4}$ | $1.9991\times10^{-3}$ | $1.9991\times10^{-3}$ |
| 18 | $5.987\times10^{-4}$ | $2.200\times10^{-4}$ | $2.0729\times10^{-3}$ | $1.9963\times10^{-3}$ |
| 26 | $5.940\times10^{-4}$ | $2.215\times10^{-4}$ | $2.0660\times10^{-3}$ | $1.9920\times10^{-3}$ |

$P$-flatness at the shipped $n=20$: `dA_spread` $3.804\times10^{-4}\to
8.977\times10^{-6}$ (**42×**), `dB_spread` $8.531\times10^{-5}\to7.392\times10^{-6}$
(**12×**).

## 4. The gluon bubble: b₀ universality goes to five digits

`gluon_self_energy._bubble` takes no `kernel` argument — it computes `lat` and `cont`
in one pass — so **every call was contaminated**, not just a `rule` branch.

| quantity | with refold | without |
|---|---:|---:|
| `d1_bubble` ($n=40$, $p=0.2$) | $0.166468$ | $0.165091$ |
| `convergence_spread` | $1.766\times10^{-4}$ | $9.920\times10^{-5}$ |
| `b0_slope_ratio` (lattice/continuum log-slope) | $0.9933321$ | $\mathbf{1.0000542}$ |

The slope ratio is the sharp one. Universality of $b_0$ says the lattice bubble must
run with the continuum's log-slope **exactly**; the refold put it 0.67% off, and
removing it lands the ratio on 1 to $5.4\times10^{-5}$. That is a derived identity
recovered, not a tolerance met.

## 5. The fourth site, and why its effect is small

`run_d1_vertex_formfactor._Bcoeff_lattice_ff` wrapped $k+q$ before **both** kernels.
For `wilson` that is an exact no-op — the Wilson control is unchanged to
$2\times10^{-13}$, which is what makes the removal safe rather than a change of
result, exactly as in F272. For `rule` it moves $C_\text{vg}$ by $+6.3\times10^{-4}$
at $n=24$ and $+6.5\times10^{-4}$ at $n=32$ — a $3\times10^{-5}$ relative shift, three
orders below the effect in `_bubble`.

| $n$ | wilson old → new | rule old → new |
|---:|---|---|
| 24 | $18.361710 \to 18.361710$ ($+2.3\times10^{-13}$) | $21.578282 \to 21.578910$ |
| 32 | $18.364254 \to 18.364254$ ($+1.4\times10^{-14}$) | $21.590674 \to 21.591326$ |

**Why so small here and not in `_bubble`:** this integrand carries the leg cosine
form factor `_cos_formfactor`, which vanishes toward the zone face — precisely the
region the refold corrupts. The damping is not a defence (the line was still wrong);
it is the explanation for why the same defect has a three-order range of severity
across the four sites, and therefore why a value-only test on any one of them is not
a reliable detector.

## 6. What did not move

* **$b_0^\text{QED} = 4/3$ and $b_0 = 11$ are untouched.** Both gates are exact sympy
  on continuum vertices with no grid at all. `F251.P2_b0_QED`, `F251.P1_ward`,
  `F258.S0`–`S4` and `d1.b0_gate` are all unchanged.
* **Every affected test still passes**: F251 5/5, F258 6/6, F252, F261, F249, F264
  (19 checks), F155, F239. 33 checks re-run, 0 failures, 0 tolerance relaxations.
* **The Wilson control is unchanged** at every site that has one — $2\times10^{-13}$
  in the d₁ runner, $\sim10^{-14}$ for the `lpt_*` kernels.
* **`lpt_selfenergy.py:76` and `lpt_wilson_selfenergy.py:186` are deliberately NOT
  changed.** Their Wilson $\hat k^2$ genuinely *is* $2\pi$-periodic per axis, so their
  wrap is an exact no-op and the cubic cell is its true zone (audit V4.4). Removing a
  correct fold would be the same class of error in the other direction.

## 7. The guard

The defect is a **line, not a value** — it is invisible until $Q > \pi/n$, so a
value-only test passes on a coarse grid while the bug is present. That is how it
survived F272's own fix in three sibling modules. `tests/casim/test_bz_period_lattices.py`
(gate tier) gains four tests:

* **T6** — source-level: no modular refold survives in `_fermion_B`,
  `_selfenergy_AB` or `_bubble` (docstrings and `#` comments stripped, since all
  three now carry a comment explaining the removal).
* **T7** — vacuum polarization $\Delta$ is negative, $q$-flat to $<10^{-4}$, and
  grid-convergent between $n=10$ and $n=14$. The **sign** is asserted, because it is
  the sharpest available discriminator.
* **T8** — self-energy `dA_spread`/`dB_spread` $< 5\times10^{-5}$.
* **T9** — gluon bubble log-slope ratio within $5\times10^{-3}$ of 1.

T1 already pins the $\sqrt3\cdot$fcc period lattice these all rest on.

## 8. Open

* **`test-results/d1_vertex_formfactor.json` is not regenerated.** Its committed grid
  is $n \in \{24,32,48\}$ and the $n=48$ leg needs ~2.7 GB for the rank-3 vertex
  tensor and ~90 s per kernel — it OOMs and overruns the sandbox's 45 s cap. Recorded
  as `stale_by_design` in `docs/theory/supersessions.yaml` under **S12**, with the
  $n=24/32$ shifts above as the measured expectation. Clears with one run on Ben's
  machine:

  ```bash
  PYTHONPATH=src python3 tests/runners/run_d1_vertex_formfactor.py
  ```

* **`bgfield_loop.py:261`'s integration domain** is still not re-derived (audit V4.4:
  "BZ integral, biased cube — the refold was fixed by F272, the *domain* was not").
  The same question applies to all four sites fixed here: the midpoint cube
  $[-\pi,\pi]^4$ is not a fundamental domain of a $\sqrt3\cdot$fcc-periodic function.
  Every result in this finding is a **subtracted** lattice−continuum difference on a
  common domain, which is what makes the comparison meaningful regardless; but the
  absolute BZ measure for rule-kernel integrals remains the open item F272 §4 named,
  and F267 is the place it has to be settled.

* **$d_1$/$q^*$ still is not pinned.** F155's bracket stands. What changes is that the
  bubble leg feeding it now runs at the continuum log-slope to $5\times10^{-5}$
  instead of 0.67% off.

## 9. Cross-references

[[F272]] (the same defect, `bgfield_loop`, the worked precedent) ·
[[F267]] ($\sqrt3$ period lattice, fermion side) ·
[[F162]] ($b_0=11$ gate, untouched) · [[F251]] · [[F258]] · [[F155]] ·
audit V-023 (`docs/audits/physics-audit-report-2026-08-01.md` §V4.4) ·
`tests/casim/test_bz_period_lattices.py` T6–T9 ·
`docs/theory/supersessions.yaml` S12
