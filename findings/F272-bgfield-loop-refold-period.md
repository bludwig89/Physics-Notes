# F272 — The background-field loop refolded k+q by a period the rule kernel does not have

*2026-08-01 - 02:30. Roadmap **P3.1**, item 2 of F265 §9. Corrects F265's prescription for this module.*
*Status: **established** (measured, fixed, grid-convergence verified). Supersedes one number in the F162 baseline.*

## 1. Claim

`gauge/bgfield_loop._Bcoeff_numeric` refolded the shifted momentum into the cubic
cell before evaluating either lattice kernel:

```python
kqw = ((kq + math.pi) % (2 * math.pi)) - math.pi
```

Refolding a lattice propagator is legitimate **only when you refold by one of its
own periods**, and the two kernels in this function do not share one.

* **Wilson** ($4\sum_\mu\sin^2(k_\mu/2)$) *is* $2\pi$-periodic per axis. For it the
  wrap is an exact no-op — measured to $2\times10^{-14}$.
* **The rule kernel is not.** $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$
  inherits the half-angle arguments, and its period lattice was measured to be
  $\sqrt3\times\text{fcc}$ — the F267 signature.

Measured shift-invariance of $\Omega_\text{even}$ (200 random $k$, max $|\Delta\omega|$):

| shift | result |
|---|---|
| $2\pi(1,0,0)$ | 3.56 — **not** a period |
| $4\pi(1,0,0)$ | 5.15 — **not** a period |
| $2\pi(1,1,0)$ (plain fcc) | 2.57 — **not** a period |
| $2\pi(1,1,1)$ | 2.74 — **not** a period |
| $\sqrt3\cdot2\pi(1,1,0)$ | $2.7\times10^{-15}$ — **PERIOD** |
| $\sqrt3\cdot2\pi(2,0,0)$ | $2.4\times10^{-15}$ — **PERIOD** |

So the wrap mapped $k+q$ to a **genuinely inequivalent momentum** and evaluated the
propagator there.

**No refold was needed at all.** $\Omega_\text{even}$ is a closed form, valid at any
$k$, so evaluating it at the unwrapped $k+q$ already returns the periodic-correct
value. Folding is an array-indexing device and there is no array here.

## 2. Why it survived, and why it was getting worse

A grid point crosses the cell face only when $Q>\pi/n$. The artifact is therefore
**invisible on a coarse grid and switches on as the grid is refined** — the opposite
of a convergent scheme, and the reason no one saw it.

Wrap-induced shift in `delta_rule` at $Q=0.3$:

| $n$ | $\pi/n$ | shift |
|---:|---:|---:|
| 10 | 0.314 | $-3.7\times10^{-15}$ (no crossing) |
| 14 | 0.224 | $+1.6\times10^{-2}$ |
| 18 | 0.175 | $+2.1\times10^{-2}$ |

## 3. What it cost: the function's entire claim

`lattice_b0_consistency` exists to show that $\Delta = B_\text{lat}-B_\text{cont}$ is
**$q$-flat**, because a residual log would make $\Delta$ grow like $\ln(1/Q)$ and
$q$-flatness is what establishes $b_0$ as propagator-independent. The wrap
manufactured a spurious $q$-dependence **indistinguishable from the very residual
log the test exists to detect**.

| quantity ($n=14$) | with wrap | without |
|---|---:|---:|
| `delta_rule` spread (the flatness gate) | $1.58\times10^{-2}$ | $\mathbf{2.96\times10^{-5}}$ |
| `delta_wilson` spread (control) | $1.80\times10^{-4}$ | $1.80\times10^{-4}$ |

A factor of **530**, and the rule kernel is now *flatter than Wilson*.

**The decisive evidence is grid-convergence**, not flatness at one $n$:

| `rule_shift_mean` | $n=14$ | $n=18$ | change |
|---|---:|---:|---:|
| with wrap (old) | $-0.008611$ | $-0.005071$ | **70%** |
| without (new) | $-0.012575$ | $-0.012591$ | **0.13%** |

The old number was not converging to anything. The new one is.

## 4. F265's prescription for this module was wrong

The roadmap carried F265's reading — *"over-counts the spatial measure by 4;
`make_kgrid_bcc` now supplies the fix"* — and the correct action was **not** to apply
it. `make_kgrid_bcc`'s `in_bz` mask marks the **fcc** BZ with weight $1/4$, and the
fcc lattice is *not* a period lattice of a $\sqrt3\cdot$fcc-periodic function (row 3
of the table in §1). Applying it would have inserted a spurious factor of 4 into a
quantity that had no factor-4 error.

This is the F267 lesson recurring in the gauge sector: F267 established that the
*fermion walk* has the $\sqrt3$-scaled period and that "the gauge factor 4 does not
transfer". **This finding shows the gluon rule kernel is in the same position** — so
the boundary F265 drew, between a gauge side with a clean fcc period and a fermion
side without one, does not run where F265 put it. Anything built on
`omega_even`/`K_true_4d` is on the $\sqrt3$ side.

**Nothing was multiplied by $3\sqrt3/4$ or by 4.** As F267 insists, the fix is to stop
doing an unjustified operation, not to add a compensating constant.

## 5. What did not move

* **$b_0=11$ is untouched.** `b0_gate_symbolic` is exact sympy on continuum vertices
  with no grid at all: tensor coefficient $22/3 = 20/3$ (gluon) $+\,2/3$ (ghost),
  transverse, calibration $g=1$. F162's G1 gate is unaffected.
* **The Wilson control is unchanged** to $2\times10^{-14}$ — which is what makes the
  removal safe rather than a change of result.
* **All three F162 gates still pass**; `b0_propagator_independent` and
  `rule_shift_small` remain true.
* **Exactly one committed number moves**: `F162_bgfield_loop.json`
  `G2.rule_shift_mean`, $-0.005071\to-0.012591$. Recorded as a supersession.

## 6. Open

`d1`/`q*` still is not pinned — F155's bracket stands, and this finding does not
touch it. The finite part needs the vertex form factors, and the $q^*$ pull-down to
0.733 remains the open vertex job. What changes is that the *propagator-driven* shift
feeding that bracket is now a grid-convergent number rather than a drifting one.

`lpt_*` (F265 §9 item 1) is 4-D hypercubic Wilson throughout and is **not** touched
here; it is its own session. Given §4, its BZ measure should be re-derived against the
$\sqrt3$ period rather than against F265's fcc reading.

## 7. Cross-references

`src/casim/engine/gauge/bgfield_loop.py` · [[F267]] (the $\sqrt3$ period, fermion
side) · F265 §9 item 2 (the prescription this corrects) · F162 (the $b_0$ gate, G1
untouched) · F155 (the $q^*$ bracket) · `tests/findings/test_F162_bgfield_loop.py`
