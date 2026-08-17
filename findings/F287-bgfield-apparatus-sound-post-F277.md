# F287 — The F162 background-field apparatus is **sound** post-F272/F277: $b_0=11$ is now recovered **numerically** as well as symbolically, and the one thing it must not be used for is an **absolute** constant — which is exactly what $d_1$ is

*2026-08-02 - 12:38. Discharges the prerequisite named in `docs/status/completeness-2026-08-02.md` **gap #2** ("Re-establish that the F162 apparatus is sound post-F277 before computing anything with it. That verification is a prerequisite, not a detour").*
*Status: **established** (measured, grid-convergent, guarded). Verdict on [[F162]]: **SOUND**. Extends [[F272]]/[[F277]] period-lattice work to the 4D kernel and adds a resolution-floor hazard.*

## 1. Verdict

The apparatus is sound. Every F162 gate passes, the defect F272/F277 chased is
absent everywhere it could be, the subtracted shift is grid-**convergent** and
not merely flat, and $b_0=11$ is now recovered from the numeric quadrature to
95% — a tie between F162's G1 (exact, symbolic) and G2 (numeric) that F162 never
made. $d_1$ may be computed with this machinery, **subject to one restriction
that is load-bearing for gap #2** (§6).

| | |
|---|---|
| F162 gates | **3/3 PASS** (G1 exact $b_0=11$, G2 lattice$=$continuum, G3 scope) |
| F287 apparatus checks | **6/6 PASS** |
| Slope tests (D1/D2) | $n=26,32$ complete; $n=40$ handed to Ben's machine (§7) |

## 2. No refold survives, and the 4D statement is stronger than F277's

A full-tree source sweep for modular refolds returns only the two sites F277
**deliberately** kept — `lpt_selfenergy.py:76` and `lpt_wilson_selfenergy.py:186`,
whose Wilson $\hat k^2$ genuinely *is* $2\pi$-periodic per axis. `bgfield_loop`
is clean, and the gate-tier guards T3/T4/T5 in
`tests/casim/test_bz_period_lattices.py` already pin it at source level and for
grid-convergence.

F277's period table is a **3D spatial** statement. `_Bcoeff_numeric` evaluates the
**4D** kernel $K=3\,\Omega_\text{even}^2+k_t^2$, so I measured it there. 200 random
$k$, $\max\lvert\Delta K\rvert$:

| shift | result |
|---|---|
| $2\pi(1,0,0,0)$ — the refold | **76.49** — not a period |
| $2\pi(1,1,0,0)$ — plain fcc | **36.51** — not a period |
| $\sqrt3\cdot2\pi(1,1,0,0)$ | $1.4\times10^{-14}$ — **PERIOD** |
| $\sqrt3\cdot2\pi(2,0,0,0)$ | $2.1\times10^{-14}$ — **PERIOD** |
| $2\pi(0,0,0,1)$ — **the time leg** | **78.80** — not a period |

The new row is the last one. The Euclidean-time leg is continuum $k_t^2$, which
has **no period at all**, so in the 4D integrand the refold sent $k+q$ to an
inequivalent momentum in **four** directions, not three. Any future module that
folds this kernel is wrong in time even if it gets the spatial lattice right.

## 3. Convergence, not flatness — the F272/F277 discriminator

Flatness alone was passing while the bug was live; convergence is what settles it.
Subtracted shift $\Delta=B_\text{lat}-B_\text{cont}$, $Q\in\{0.1,0.15,0.2,0.3\}$:

| $n$ | rule mean | rule spread | wilson mean | wilson spread |
|---:|---:|---:|---:|---:|
| 10 | $-1.254335\times10^{-2}$ | $2.523\times10^{-5}$ | $-7.895233\times10^{-2}$ | $1.226\times10^{-4}$ |
| 14 | $-1.257490\times10^{-2}$ | $2.963\times10^{-5}$ | $-7.875603\times10^{-2}$ | $1.801\times10^{-4}$ |
| 18 | $-1.259105\times10^{-2}$ | $3.686\times10^{-5}$ | $-7.869058\times10^{-2}$ | $1.593\times10^{-4}$ |
| 22 | $-1.259785\times10^{-2}$ | $2.761\times10^{-5}$ | $-7.867382\times10^{-2}$ | $8.030\times10^{-5}$ |
| 26 | $-1.260012\times10^{-2}$ | $1.783\times10^{-5}$ | $-7.867652\times10^{-2}$ | $6.929\times10^{-5}$ |

Relative step $n=22\to26$: **rule $1.80\times10^{-4}$**, wilson $3.42\times10^{-5}$.
Sign-stable throughout. Contrast the recorded refolded behaviour (S11-F272): the
mean moved **70%** between $n=14$ and $n=18$. It now moves 0.018%.

Two independent confirmations fall out:

* The $n=18$ rule mean, $-0.0125910487428$, reproduces the value the F162 test
  itself writes, $-0.0125910487433$, to $5\times10^{-13}$ — through a **different
  (chunked) integrator**, so this is not the same code agreeing with itself.
* That value is exactly the one **S11-F272 predicted** for the baseline
  ($-0.005071\to-0.012591$). The stale-by-design baseline is confirmed, not just
  asserted.

The Wilson control converges to $3.4\times10^{-5}$ and its mean is unchanged to
$1.4\times10^{-12}$ against the committed value — the no-op it must be.

## 4. The new tie: $b_0=11$ recovered **numerically**

F162's G1 (exact $b_0=11$) and G2 (numeric $q$-flatness) were never connected.
They can be. With $q=(Q,0,0,0)$ the transverse structure gives

$$\Pi_{00}-\Pi_{11}=-\frac{b_0}{16\pi^2}\,Q^2\ln\frac{\Lambda^2}{Q^2}
\quad\Longrightarrow\quad
\frac{d(-B_\text{cont})}{d\ln(1/Q)}=\frac{2b_0}{16\pi^2}=0.139317\ \ (b_0=11).$$

Measured at **resolved** $Q$ (§5); sweep complete on Ben's machine:

| $n$ | $\min Q/$spacing | abs $b_0$ recovery | rule/cont | wilson/cont |
|---:|---:|---:|---:|---:|
| 26 | 2.07 | 0.9487 | 1.0030325 | 0.9840125 |
| 32 | 2.14 | 0.9521 | 1.0021254 | 0.9884762 |
| 40 | 2.23 | **0.9551** | **1.0014117** | 0.9919819 |

Two readings, and the second is the sharp one:

* **Absolute** — the quadrature returns $b_0=10.44,\,10.47,\,10.51$, i.e. 95% of 11
  and monotonically rising. The loop is numerically the loop the symbolic gate
  certifies.
* **Ratio** — $b_0^\text{lat}/b_0^\text{cont}$ on the *same* grid at the *same* $Q$,
  where grid and domain artifacts cancel. Universality says this is **exactly 1**.

Neither ratio is 1 at finite grid, and neither should be — both kernels carry
discretisation corrections. What the sweep shows is that both **vanish as a power
law in the grid spacing**, so both extrapolate to exactly 1:

| $n$ | rule deficit | wilson deficit | wilson/rule |
|---:|---:|---:|---:|
| 26 | $3.033\times10^{-3}$ | $1.599\times10^{-2}$ | 5.27× |
| 32 | $2.125\times10^{-3}$ | $1.152\times10^{-2}$ | 5.42× |
| 40 | $1.412\times10^{-3}$ | $8.018\times10^{-3}$ | 5.68× |

$$\text{rule}\sim n^{-1.77},\qquad \text{wilson}\sim n^{-1.60}\qquad\longrightarrow\ 0.$$

So $b_0^\text{lat}=b_0^\text{cont}$ holds for **both** kernels in the continuum
limit — the F277 §4 `b0_slope_ratio` identity recovered, in the shape it actually
takes on a finite grid.

**And the rule beats Wilson by 5.3–5.7× at every grid.** That is the F129/F130
**near-perfect action** appearing directly in the $b_0$ log slope: the rule's
propagator is so close to the continuum that its discretisation error in a
*running-coupling* observable is over five times smaller than Wilson's. It is an
independent sighting of the same property F162 §3 invoked to explain why the
rule's propagator-driven shift is $\approx0$ — measured here in a different
quantity.

## 5. A second hazard of the same family: the resolution floor

My first slope attempt returned $b_0=4.06$ — 37% of true — and I nearly recorded
it as an apparatus defect. It was my test that was broken, not the apparatus:
at $n=26$ the grid spacing is $2\pi/n=0.2417$ and every $Q$ I had chosen
($0.08$–$0.22$) sat **below one cell**, so the IR end of the log window
$Q\ll k\ll\Lambda$ did not exist. The linear fit residual was $1.0\times10^{-3}$ —
it looked fine.

That is the **same failure family as the refold**: a confidently wrong number
from a well-behaved-looking fit. It is recorded, not deleted — `b0_log_slope` is
kept at its original ill-posed $Q$ and the check asserts the pathology
**reproduces**, so a future session cannot rediscover 4.06 and believe it.

> **Resolution floor: probe this apparatus only at $Q\gtrsim2\cdot(2\pi/n)$.**

## 6. The restriction that matters for $d_1$ (gap #2)

The absolute recovery is **0.9521, not 1**, and still moving. The subtracted and
ratio quantities are clean to $10^{-3}$–$10^{-5}$; the absolute normalisation is
not. The cause is the one F277 §8 left open: the midpoint cube $[-\pi,\pi]^4$ is
**not a fundamental domain** of a $\sqrt3$-fcc-periodic function. Everything in
F162 and F277 is a *subtracted* lattice$-$continuum difference on a common
domain, which is precisely why those results hold regardless — and equally why
the absolute number does not.

**$d_1$ is a finite absolute constant.** So the operative conclusion for gap #2 is:

> The apparatus is sound **for subtracted differences**, and $d_1$ must not be
> taken from this quadrature's absolute normalisation. It has to come either from
> settling the F267 fundamental domain, or from a **subtracted formulation against
> a known reference** — and F162's G3 already names the right reference, the
> Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_L=28.81$ gate.

That is not a new obstruction; it is the existing open item, now **quantified**
(5% at $n=32$) and shown to bear directly on the one computation gap #2 wants.
F155's bracket $q_\ast a\in[1/\sqrt3,\sim0.97]$ stands, untouched.

## 7. Open

* ~~**$n=40$ slope leg not run.**~~ **CLOSED 2026-08-02 - 14:05**, run on Ben's
  machine. The prediction this finding recorded from the $n=26/32$ trend — "abs
  recovery $\gtrsim0.954$, rule/cont $\to1$ within $\sim1.5\times10^{-3}$" — came
  in at **0.9551** and **$1.4117\times10^{-3}$**. Both held.

  The run surfaced a defect in *this finding's own test*, not in the physics: the
  first version of `run_f287_slope.py` asserted a flat $5\times10^{-3}$ on the
  **Wilson** ratio, and that assert had never executed in-sandbox because the
  $n=40$ leg was killed before reaching it. The threshold was wrong on its face —
  Wilson was already at 0.9840 and 0.9885 in the two grids that *had* completed.
  The fix is not a looser tolerance but a **correctly shaped claim**: the
  assertion is now on monotone power-law convergence of both deficits to zero,
  plus the rule-beats-Wilson ordering, which is what the data actually says
  (§4). `verify()` is factored out as a pure function of the measured rows so it
  can be exercised against the committed JSON without re-running the quadrature —
  the mistake was shipping an assertion nothing had run.
* **The BZ fundamental domain** (F277 §8, F272 §4) remains the open item, now with
  a number on it. F267 is where it has to be settled.
* **`bgfield_loop.py` imports numpy directly**, violating D8. Not touched here —
  it is a routing change, not physics, and this session did not own a numerics
  claim. Flagged for the numerics ratchet.

## 8. Cross-references

[[F162]] (the apparatus under test — verdict SOUND) · [[F272]] (the defect, and
S11's predicted baseline, confirmed here) · [[F277]] (the four sibling sites; §4
slope-ratio method reused) · [[F267]] ($\sqrt3$ period lattice; where the domain
must be settled) · [[F155]] (the $q_\ast$ bracket, unmoved) · [[F151]] · [[F239]] ·
`docs/status/completeness-2026-08-02.md` gap #2 ·
`tests/casim/test_bz_period_lattices.py` T3–T5 ·
`docs/theory/supersessions.yaml` S11, S12
