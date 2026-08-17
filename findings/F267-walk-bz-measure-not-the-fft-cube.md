# F267 — The fermion walk's Brillouin zone is not the cubic FFT cube, and the gauge side's factor 4 does not transfer

**Date:** 2026-07-31 - 22:15
**Status:** established (5/5 checks; S1/S2/S3/S5 exact-or-machine, S4 quantitative).
**Test:** `tests/findings/test_F267_walk_bz_measure.py` → `test-results/F267_walk_bz_measure.json`
**Module:** `casim.engine.lattice.derive_walk_bz_measure`
**Closes:** F265 §9 item 5 (*"The √3 question … whether the fermion sector needs the same measure correction is **open** and is the natural next item"*) — roadmap **P3.1's spike**.

## 1. The question F265 left open

F265 fixed the gauge **action**. The eight BCC links are integer hops
$d\in\{\pm1\}^3$ on the conventional cubic cell of side 2, `np.roll` by $d$ is an
exact lattice translation, the lattice is
$\{n\in\mathbb Z^3 : n_x\equiv n_y\equiv n_z \bmod 2\}$ at index 4, the reciprocal
lattice is **fcc**, and the cube $(-\pi,\pi]^3$ therefore holds **4 copies** of one
Brillouin zone. So on the gauge side a BZ integral must restrict to `bcc_bz_mask`
or divide by 4.

The fermion walk hops differently. `bcc_fractional_shift` multiplies by
$\exp(i\,d\cdot k/\sqrt3)$ — a translation by $d/\sqrt3$, the BCC half-diagonal
normalised to **unit length** ($|d|/\sqrt3 = 1$). F265 noted this is "the same
lattice at a different unit of length ($q = k/\sqrt3$)", called the two
"consistent as a rescaling", and left open whether the fermion sector needs the
same measure correction.

**It does need one, it is not the gauge factor, and the "consistent rescaling"
reading does not survive contact with the code.**

## 2. §S1 — The walk's period is $\sqrt3\times$fcc, and neither of the two obvious candidates

Measured over 4000 random $k$, both helicity branches, as $\max|\Delta u|$ under a
shift $k \to k+G$:

| $G$ | $\max\lvert\Delta u\rvert$ | period? |
|---|---|---|
| $\pi(1,1,0)$ — **the gauge side's fcc period** | $1.372$ | **no** |
| $2\pi(1,0,0)$ — **the FFT grid's own period** | $1.934$ | **no** |
| $\sqrt3\,\pi(1,1,0)$ | $1.2\times10^{-15}$ | yes |
| $\sqrt3\,\pi(1,0,1)$ | $1.2\times10^{-15}$ | yes |
| $\sqrt3\,\pi(0,1,1)$ | $1.2\times10^{-15}$ | yes |

Algebraically this is immediate from $u^\pm = c_xc_yc_z \pm s_xs_ys_z$ with
$c_i=\cos(k_i/\sqrt3)$: shifting one $\kappa_i=k_i/\sqrt3$ by $\pi$ sends
$u\to-u$, and shifting **two** of them by $\pi$ leaves $u$ invariant — which is
exactly the fcc generator set in $\kappa$, i.e. $\sqrt3\times$fcc in $k$.

**The sharp consequence is the second row.** The cubic FFT cube's own periodicity
is not a symmetry of the walk operator, so **the cube is not a fundamental domain
of the walk** and there is no "$n$ copies" statement to divide by.

## 3. §S2 — The cube is $4/(3\sqrt3)$ of one zone: 76.98%

| | value |
|---|---|
| zone volume (in $\kappa$) | $2\pi^3$ |
| cubic FFT cube (in $\kappa$) | $1.539601\,\pi^3$ |
| ratio | $0.769800$ |
| closed form | $4/(3\sqrt3)$, residual $0$ |

Not a domain and **not an integer number of copies** — which is the structural
reason no integer correction factor exists. The gauge side got a clean 4 because
its hop is a lattice vector; the walk's is not.

## 4. §S3 — No doubler is introduced. F250 and the photon are safe.

Inside the cube, at $L=24,36,48$, for both branches:

| | count |
|---|---|
| $\omega = 0$ points | **1** (at $k=0$) |
| $\omega = \pi$ points | **0** |

So the mismatched domain does **not** manufacture spurious zeros. F250's all-$k$
gauge pole ("a unique BZ zero at $k=0$ ⇒ no gauge doubler") and the F69
paired-spinor photon built on it are untouched, and **D1 does not re-open** — which
was the outcome the roadmap's original P3.1 spike was gated on.

## 5. §S5 — The array points are not the walk's lattice sites

Translate a delta at the origin by one BCC hop, $L=16$:

| | value |
|---|---|
| peak amplitude | $0.3920$ |
| probability in the largest cell | $0.1536$ |
| cells with $\lvert a\rvert > 10^{-3}$ | **2274 of 4096** |
| $\sum\lvert a\rvert^2$ (unitarity) | $1.0$ |

A nearest-neighbour lattice hop would give exactly **1** cell. The walk is a
**band-limited fractional translation** — exactly unitary, but not a hop on the
array. `bcc_fractional_shift`'s own docstring says as much ("8 `np.roll` calls …
would give the wrong operator anyway"); what is new here is the consequence.

**This is what kills the "same lattice at a different unit of length" reading.** A
rescaling $q=k/\sqrt3$ has to be matched by a rescaling of the real-space
spacing. Both sectors index the *same array at the same spacing*, so the walk is
not the integer-hop walk in other units — it is a different operator on the full
$L^3$ array, while the gauge side lives on the $L^3/4$ BCC sublattice.

## 6. §S4 — What it costs: 10.7% and 16.9%

Cube grid-mean vs the mean over a true fundamental domain of the walk's own
periodicity lattice (Monte-Carlo, $4\times10^5$ points $\times$ 3 seeds, $L=48$ for
the cube):

| observable | cube grid-mean | domain mean | relative error |
|---|---|---|---|
| $\langle\omega\rangle$ | $1.402645$ | $1.570815 \pm 0.00035$ | **10.7%** |
| $\langle 1/\omega\rangle$ | $0.891861$ | $0.763011 \pm 0.00092$ | **16.9%** |

The second is the moment **F100** uses for the vacuum plaquette flux,
$\sigma_\phi^2 = (1/V)\sum_{k\neq0} 1/(2\Omega(k))$, described there as *"the
Brillouin-zone average of the rule's inverse dispersion"*.

## 7. The distinction that makes this a finding and not a bug report

**For an observable that is a trace over the operator's own eigenmodes** — a
vacuum fluctuation sum, a density of states on the finite grid — **the cube is
correct by construction.** It *is* the mode set: every grid mode appears exactly
once, nothing is over- or under-counted, and the operator is exactly unitary
(§S5). No correction applies.

**The 10–17% error appears only** when a cube grid-mean is used as a stand-in for
a *continuum BZ integral* of the BCC Weyl dispersion, or compared against a
differently-discretised calculation.

So F100's **number** is plausibly the right mode sum for the rule as implemented;
its **label** ("Brillouin-zone average") is wrong. Which of the two categories a
given observable falls into has to be decided per observable — and that is the
work this finding hands forward, **not** something to fix by inserting a factor.
Inserting $3\sqrt3/4$ anywhere would be the wrong move: it would corrupt every
mode sum in order to fix a label.

## 8. Bearing on the roadmap

- **P3.1's spike is answered.** The photon is not the risk (§S3), so the BCC port
  is engineering; but the *fermion* sector carries an unresolved measure question
  that F265 correctly flagged as "the natural next item".
- **The audit that P3.1 now owns:** classify every existing $k$-space average in
  the fermion sector as *mode sum* (correct as-is) or *BZ integral* (carries the
  10–17%). F100's $\sigma_\phi^2 \to \gamma(\Omega)$ chain is the first entry, and
  the $d_1$ chain (F144/F151/F152/F154/F155/F162/F163/F239) should be checked for
  the same pattern since F265 already re-scoped it for the action.
- **Not a new free parameter.** Nothing here introduces one; it reclassifies
  existing numbers.

## 9. Exactness summary

| check | claim | class |
|---|---|---|
| S1 | $\sqrt3\times$fcc are periods; fcc and $2\pi$ cubic are not | machine ($1.2\times10^{-15}$) / exact ($O(1)$ separation) |
| S2 | cube/zone $= 4/(3\sqrt3)$ | **exact** (closed form, residual 0) |
| S3 | 1 zero, 0 $\pi$-points per branch, $L=24,36,48$ | **exact** (integer counts) |
| S4 | 10.7% / 16.9% measure error | quantitative (MC, sd quoted) |
| S5 | 2274/4096 cells; unitarity $1.0$ | machine |

*Cross-references: `findings/F265-bcc-gauge-action-blindness.md` §2 and §9 item 5, `findings/F250-allk-gauge-pole.md`, `findings/F264-*` (BZ census), `findings/F100-*` (the $1/\Omega$ moment), `docs/roadmaps/roadmap-unified-program.md` §P3.1.*
