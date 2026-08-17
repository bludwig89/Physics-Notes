# F273 — The mode-sum audit: every dispersion is √3·fcc-periodic, and the cube is a *biased* sub-region

*2026-08-01 - 03:20. Roadmap **P3.1** item 5, the audit F267 handed forward. Partial by design — see §5.*
*Status: **established** for the period lattices and the I₂ measurement. The classification of I₂ is argued, not proved, and §4 records a structural tension it exposes.*

## 1. The first result invalidates the audit's own premise

F265 drew a boundary: the **gauge** side has a clean fcc period and its cube
over-counts by exactly 4; the **fermion** walk (F267) has the √3-scaled period and
"the gauge factor 4 does not transfer". The audit was scoped to the fermion sector on
that basis.

Measured shift-invariance (300 random $k$, max $|\Delta\omega|$; `PERIOD` = $<10^{-12}$):

| function | $2\pi(1,1,0)$ (fcc) | $\sqrt3\cdot2\pi(1,1,0)$ |
|---|---:|---:|
| `bcc_dispersion(k)` — **raw walk, unhalved** | 0.673 — no | $1.4\times10^{-15}$ — **PERIOD** |
| `omega_even(k)=\omega^\pm(k/2)` — gluon rule | 2.887 — no | $3.0\times10^{-15}$ — **PERIOD** |

**Every dispersion in the tree is on the √3·fcc period lattice, including the raw
`bcc_dispersion` the gauge side is built from.** The plain fcc lattice is a period of
none of them. So F265's factor 4 never applied *anywhere* — not to the gauge side
either — and the boundary it drew does not exist. [[F272]] found the same thing from
the loop-integral side on the same day and independently.

**Consequence for the audit's scope: it is not a fermion-sector audit.** Every
$k$-space average built on any of these dispersions is in the same position.

## 2. What the cube actually is

The cubic FFT grid is not an unbiased sample of the true zone, and the bias is not
small:

| domain | $\langle u\rangle$ | $\langle\omega\rangle$ | $\langle\cot\omega\rangle$ |
|---|---:|---:|---:|
| true zone (MC over the √3·fcc primitive cell) | $-0.0015\,/+0.0012$ | $1.5725\,/\,1.5693$ ($\approx\pi/2$) | $-0.003\,/+0.004$ ($\approx0$) |
| cubic FFT grid, $L=24$ | $+0.1523$ | — | $+0.2191$ |
| cubic FFT grid, $L=32$ | $+0.1527$ | — | $+0.2202$ |

Over the true zone $u$ is symmetric about 0, so $\omega$ is symmetric about $\pi/2$;
since $\cot(\pi-\omega)=-\cot\omega$, **$\langle\cot\omega\rangle$ vanishes
identically** — by symmetry, not approximately. Over the cube it is $+0.221$ and
converging ($0.2157,\,0.2191,\,0.2202,\,0.2210$ at $L=16,24,32,48$).

**So this is not F267's 10.7–16.9% effect.** For a $\cot$-class moment the two
readings differ by *everything*: a finite converged number versus exact zero.

## 3. I₂ / B / λ₆ — the highest-stakes entry, and why it is a mode sum

`eg_sextic.i2_lattice` computes $I_2=\langle\cot\omega\rangle_\text{BCC}$ over the
cubic grid with $k=0$ excluded. It is load-bearing: `derive_lambda6_sextic` line 58
takes $B=-3\sqrt2\,I_2\,\bar y^4$, and the F234 arrow
$\lambda_6=|B|/(2e^6\cos\tfrac23)$ produces $\lambda_6=0.243$ — a **founding-principle
output** (CLAUDE.md decision 7).

**Classification: mode sum. The cube is correct by construction.** The argument:

* The CA is defined on an $L^3$ array. Its Fourier modes are exactly $k=2\pi n/L$ per
  axis — the cubic FFT grid — and that is the *complete, non-redundant* mode set of
  the finite system. There are $L^3$ of them and they are all distinct states.
* $\omega$ being $\sqrt3\cdot$fcc-periodic is a statement about the *function*, not
  about the mode set. Two grid points related by a period are still two distinct
  modes of the finite system, and a trace counts both.
* $I_2$ enters as a Taylor coefficient of the **sea energy** $-\sum_k\Omega(k;m)$,
  which on this lattice is literally a sum over those $L^3$ modes.
* As $L\to\infty$ the grid densely fills the **cube**, so the thermodynamic limit of
  the trace is the cube average — and the measured convergence
  ($0.2157\to0.2210$) is exactly that, not a drift toward zero.

The label is nevertheless wrong. The docstrings say "full-BZ" and
"$\langle\cot\omega\rangle_\text{BCC}$"; it is neither a BZ average nor a BCC-zone
average. **This is precisely the mislabelling F267 predicted for F100** — right
number, wrong name — now confirmed in a second, independent chain.

**Nothing was multiplied by anything.** The correction is to the label.

## 4. The tension this exposes, which is NOT resolved here

Section 3's argument proves the cube is the mode set of the *array*. But it also says
the physically meaningful zone of this system is the **cube**, not the rhombic
dodecahedron — while the dispersion's period lattice is $\sqrt3\cdot$fcc. **A genuine
BCC crystal cannot have both.**

That is F267 S5 restated from the observable side: "the array points are **not** the
walk's lattice sites… a rescaling $q=k/\sqrt3$ has to be matched by a rescaling of
the real-space spacing, and both sectors index the same array at the same spacing."

Two readings, and this finding does not choose between them:

1. **The array is the physical lattice** and the $\sqrt3$ is a redundancy of the
   closed form. Then every mode sum is right, D1's "BCC" is a statement about the
   *hop structure* rather than the *crystal*, and the word "Brillouin zone" should be
   retired from these docstrings.
2. **The BCC crystal is physical** and the cubic array is an unfaithful discretisation
   of it. Then the mode sums are sampling a biased sub-region, and $I_2$'s entire
   nonzero value — hence $B$, hence $\lambda_6=0.243$ — is an artifact of that bias,
   since the unbiased answer is exactly zero.

Reading 2 would demolish the lepton sextic chain. That is not an argument against it,
but it *is* a reason to decide it deliberately rather than in passing. **Deciding it
is the next item on P3.1, and it is more fundamental than the four remaining cubic
layers.**

## 5. Coverage — partial, deliberately

56 candidate $k$-space averages were located (modules that both average over a
$k$-grid and use a dispersion). This finding classifies the chain the roadmap named
first and the one that turned out to be load-bearing. **Unclassified and outstanding:**
the `lpt_*` chain (14 sites), `qed_vacuum_polarization` / `qed_electron_self_energy`
(6), `gluon_self_energy` tadpole moments (3), `photon_bound_state` (2), and F100's own
$\sigma_\phi^2\to\gamma(\Omega)$ chain, which F267 named first and which §1 now shows
is in the same position as everything else.

Each is a per-observable decision of the §3 kind: *is this a trace over the
operator's own modes, or a stand-in for a continuum integral?* **Do not insert
$3\sqrt3/4$, or 4, anywhere** — §1 shows the factor-4 premise was wrong even where
F265 asserted it.

## 6. Cross-references

`src/casim/engine/particles/eg_sextic.py` (`i2_lattice`, `_bz_omegas`, `_f_of_m`) ·
`src/casim/engine/particles/derive_lambda6_sextic.py` line 58 · [[F267]] (the √3
period, fermion side) · [[F272]] (the same conclusion from the loop integral) · F265
§9 item 5 (the premise §1 corrects) · F95/F118 ($B$) · F234 (the $\lambda_6$ arrow) ·
`tests/casim/test_bz_period_lattices.py`
