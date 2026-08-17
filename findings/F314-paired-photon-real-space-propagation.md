# Finding 314 — The paired-spinor photon propagates in real space at the closed-form pair group velocity

`2026-08-04 - 17:20`

*Module: `casim.engine.gauge.photon_packet`. Result: `test-results/F314_photon_packet_propagation.json`. Records: `F314-pair-group-velocity-closed-form`, `F314-photon-packet-propagation` (both gate tier). Tests: `tests/findings/test_F314_photon_packet_propagation.py` (10/10 PASS).*

**Status:** Confirmed. Closes the **DEFERRED** item of the F20 remediation (2026-08-03).

**Cross-references:** [[F20-photon-fermion-propagation-demo]] (the item this closes), [[F69-paired-spinor-photon]] (the pair law), [[F105-axial-photon-exactly-dispersionless]] (the on-axis identity, here guarded), [[F68-minimal-coupling-forces-even-photon]], [[F26-real-rotation-and-c-lat]], [[F306-curl-closes-at-k3-representation-artifact]].

## Question

F20 item (3) claimed "the photon exists and moves end-to-end". It made that claim
with the **σ-bilinear composite photon** (`casim.engine.gauge.bilinear`), which
`S1-F69-sigma-bilinear-photon` retired on 2026-06-01 — helicity↔branch, linearly
birefringent, excluded by GRB/AGN polarimetry (F65/F66/F67). The remediation
withdrew that leg and deferred its replacement, so the model was left in this
position:

> **The model had no real-space demonstration that its own photon propagates.**

The photon the model actually has is the paired-spinor photon (F67/F68/F69,
CLAUDE.md Core Design Decision 5), rotating the real $(\mathbf E,\mathbf B)$
doublet at $\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$.
Does *that* object cross the lattice, and does its centroid velocity match what
its own dispersion says it should?

## Summary

**Yes, and to $7.8\times10^{-16}$** — better than the Weyl leg of F20 and on par
with its Dirac legs, and against a closed form rather than against $c_\text{lat}$.

The two things F20's remediation had to fix for the fermion legs had to be fixed
here too, and a third appeared that the fermion case does not have:

1. **The right target.** A beam of finite transverse width does not travel at
   $c_\text{lat}$; it travels at the packet-weighted $\langle\partial\Omega_\text{pair}/\partial k_x\rangle$.
2. **A wrap-free box.**
3. **A sufficiently resolved carrier.** New here — see §"Being wrap-free is a
   condition on the carrier".

## The closed forms

Everything below is `casim.engine.gauge.photon_packet`.

**The pair group velocity, in general.** With $u^s=c_xc_yc_z+s\,s_xs_ys_z$ and
$\omega^s=\arccos u^s$ ($c_i=\cos(k_ic_\text{lat})$, $s_i=\sin(k_ic_\text{lat})$),
differentiation gives $\partial\omega^s/\partial k_i=c_\text{lat}\,g^s_i/\sqrt{1-(u^s)^2}$ with

$$g^s_x=s_xc_yc_z-s\,c_xs_ys_z,\quad
g^s_y=c_xs_yc_z-s\,s_xc_ys_z,\quad
g^s_z=c_xc_ys_z-s\,s_xs_yc_z.$$

Each constituent carries half the total momentum, so the chain rule contributes a
factor $\tfrac12$:

$$\boxed{\;\frac{\partial\Omega_\text{pair}}{\partial k_i}(\mathbf k)
=\frac{c_\text{lat}}{2}\left[\hat g^+_i(\mathbf k/2)+\hat g^-_i(\mathbf k/2)\right],
\qquad \hat g\equiv g/\sqrt{1-u^2}.\;}$$

Verified against a central difference of `pair_dispersion` at 30 random off-axis
$\mathbf k$ on **all three axes**: residuals $8.0\times10^{-11}$,
$3.4\times10^{-11}$, $9.1\times10^{-11}$ — the $h^2$ floor.

**On a coordinate axis, exactly $c_\text{lat}$.** On-axis $c_y=c_z=1$ and
$s_y=s_z=0$ exactly, so at the half-momentum

$$u^\pm(\tfrac{k}{2}\hat x)=\cos\!\left(\tfrac{k\,c_\text{lat}}{2}\right)$$

**bit-for-bit on both branches** — residual $0.0$ at 500 sample points, tolerance
$0$. Hence $\Omega_\text{pair}(k\hat x)=k\,c_\text{lat}$ and
$\partial\Omega_\text{pair}/\partial k_x=c_\text{lat}$ at *every* $k$ in the zone,
with zero curvature ($5.6\times10^{-10}$, the $h^2$ floor). This is F105's identity
in guarded form; the control that stops it being a tautology is the same residual
along the body diagonal, which is $0.723$.

**Finite-width packet.** $\langle d\bar x/dt\rangle=\sum_k w(\mathbf k)\,\partial\Omega_\text{pair}/\partial k_x$
with $w=|\tilde F|^2/\sum|\tilde F|^2$ computed from the actual discrete seed, so
the lattice's periodic image sum and finite $k$-grid are carried exactly.

## Why "one-sided" is the photon's branch-pure seed

`photon_step_spectral` sends $\tilde F(\mathbf k)\to e^{-i\Omega_\text{pair}(\mathbf k)}\tilde F(\mathbf k)$
for $F\equiv\mathbf E+i\mathbf B$. $\Omega_\text{pair}$ is **even** in $\mathbf k$
(because $u^\pm(-\mathbf k)=u^\mp(\mathbf k)$ — the same algebra that makes the pair
non-birefringent), so a seed with spectral support at both $\pm\mathbf k_0$ carries
two groups with opposite $\nabla_k\Omega$ and splits. A seed whose analytic field
is supported on **one side only** has no partner, no beat, and its centroid velocity
is an exact Ehrenfest statement.

That is the photon's counterpart of the branch-pure spinor seed F20 needed for its
$10^{-15}$ rows, and it is what the deferred item asked for. It is also the
codebase's own beam convention (`gauge.photon.build_beam_packet`, F105): $\mathbf B$
is the *quadrature* of $\mathbf E$ within one Cartesian component.

## Results

Wrap-free box $128\times48\times48$, packet at $x=32$, $\sigma=(5,7,7)$ as an
**amplitude** width, carrier $k_0=2\pi\cdot24/128=1.178$ on the $x$-axis, 24 ticks.
Propagator: `gauge.photon.photon_step_spectral`, unmodified.

| Quantity | Value |
|---|---|
| measured asymptotic drift | $0.5728449064271057$ |
| closed form $\langle\partial\Omega_\text{pair}/\partial k_x\rangle$ | $0.5728449064271062$ |
| **relative residual** | $\mathbf{7.8\times10^{-16}}$ |
| least-squares slope, whole window | $0.5728449064271062$ (residual $0.0$) |
| first-tick vs asymptotic drift | $1.6\times10^{-14}$ |
| boundary weight | $1.6\times10^{-19}$ |
| energy drift $\sum(\lvert\mathbf E\rvert^2+\lvert\mathbf B\rvert^2)$ | $3.7\times10^{-15}$ |
| drift vs $c_\text{lat}$ | $-0.780\%$ (finite aperture) |
| polarisation-axis dependence | exactly $0.0$ |

Repeated on F20's own box and tick count — $256\times64\times64$, $x_0=60$,
$\sigma=(6,10,10)$, 44 ticks — the residual is $1.2\times10^{-15}$ with boundary
weight $2.7\times10^{-26}$.

Reading the rows:

* **There is no transient at all.** The first tick already moves at the asymptotic
  speed, and the whole-window least-squares slope agrees with the tail mean to
  $0.0$. This is the one-sided seed doing its work: unlike F20's fixed-spinor Weyl
  packet — which starts at exactly $c_\text{lat}$ and relaxes onto its closed form,
  leaving $2\times10^{-4}$ in a whole-window fit — this estimator carries no
  fit-window freedom, so there is no choice left to make.
* **Energy is conserved on the *moving* packet.** This is the gate F20's item (3)
  could not pass: its $\sum_i|G^i|^2$ fell $1.000\to0.628$ over 44 ticks and
  $\to0.289$ by tick 100, and the conservation figure it quoted came from a global
  scalar phase applied *with no lattice step at all*, at a different momentum.
* **The deficit is real physics, four decades above the tolerance.** A record that
  compared against $c_\text{lat}$ — which is what F20 did — would be measuring
  nothing.

**Perturbation moves both sides together**, on the same box, one parameter at a
time — the failure mode F20's photon leg did not have:

| perturbation | measured drift | closed form | residual |
|---|---|---|---|
| baseline $\sigma_\perp=7$, $m=24$ | $0.5728449064271$ | $0.5728449064271$ | $7.8\times10^{-16}$ |
| $\sigma_\perp:7\to6$ | $0.5712662920681$ | $0.5712662920681$ | $1.8\times10^{-15}$ |
| $m_\text{index}:24\to32$ | $0.5747630133826$ | $0.5747630133826$ | $1.2\times10^{-15}$ |

## Being wrap-free is a condition on the carrier, not only on the box

The new failure mode, and it is sharp. The seed is one-sided only up to the
Gaussian tail of its own carrier: the residual backward weight is
$\exp(-4k_0^2\sigma_x^2)$, and that tail runs *backwards* at $-c_\text{lat}$, so it
reaches the boundary long before the packet does.

At $k_0\sigma_x=3.14$ — the "$\gtrsim 3$" that `build_beam_packet`'s docstring
suggests — on the same box, with the same physics and everything else unchanged:

| $k_0\sigma_x$ | boundary weight | relative residual |
|---|---|---|
| $3.14$ | $1.8\times10^{-8}$ | $1.1\times10^{-6}$ |
| $5.89$ | $1.6\times10^{-19}$ | $7.8\times10^{-16}$ |

Six decades, from the carrier alone. The undersampled run is retained in the
result artifact as an explicit negative control, and the gate asserts
$k_0\sigma_\text{axis}\ge5$.

## What this upgrades in F105

F105 established $\Omega_\text{pair}(k\hat x)=|k|/\sqrt3$ algebraically and
demonstrated the beam consequence numerically on a **periodic** box, quoting the
aperture deficit through the small-angle approximation
$\Delta v/v\approx1/(2(k_0\sigma_\perp)^2)$: "predicted 2.3%, measured 2.5%".

The exact statement is the sum $\sum_k w(\mathbf k)\,\partial\Omega_\text{pair}/\partial k_x$.
Scored against it, the approximation is the right order and the right scaling and
is **wrong by 5.8% of the deficit** (predicted $0.7352\%$ vs exact $0.7804\%$).
That gap is the whole distance between a percent-level demonstration and a
$10^{-16}$ gate. F105's algebra is unchanged and its conclusions stand; only its
beam-optics number is superseded by the exact form.

## Defect found in a neighbouring module

`lattice.wavepacket.weyl_group_velocity` returns $c_\text{lat}\hat n_i$ and its
docstring states $\partial\omega/\partial k_i=c_\text{lat}\hat n_i$ as a general
identity. **It holds for $i=x$ only.** Measured against a central difference of the
analytic dispersion at 200 random $\mathbf k$:

| axis | $\lvert\partial u/\partial k_i + c_\text{lat}n_i\rvert$ | verdict |
|---|---|---|
| $x$ | $1.2\times10^{-10}$ | identity holds; $g_x\equiv n_x$ |
| $y$ | $0.722$ | $g_y=-s\,n_y$ — a **sign flip** |
| $z$ | $0.407$ | $g_z$ is not $\pm n_z$; the second term of $n_z$ carries the opposite sign to the one differentiation produces |

The $n$-vector is correct ($u^2+|n|^2-1=4.4\times10^{-16}$); it is simply not
$\nabla u$ away from the $x$-axis. **No F20 number is affected** — every call site
there passes `axis=0` — but the general statement in the docstring and in F20's
"The closed forms" section is wrong as written.

**Not patched here.** `lattice/` is another sector, and the F20 remediation belongs
to a released claim. This finding reports the measurement and the correct general
form; the fix is one docstring and one narrowed signature. Recorded in
`docs/roadmaps/next-steps.md`.

## An open question this demonstration surfaces

Reported because it was measured, and **nothing is concluded from it.**

The codebase's photon-beam convention takes $\mathbf B$ to be the *quadrature* of
$\mathbf E$ within one Cartesian component. Seeded that way, the packet propagates
exactly as above. Seeded instead as a textbook **in-phase** transverse mode —
$\tilde{\mathbf E}\parallel\hat e_1(\mathbf k)$, $\tilde{\mathbf B}=\hat k\times\tilde{\mathbf E}$,
Hermitian, i.e. $\mathbf E\perp\mathbf B$ and in phase, a real linearly polarised
travelling wave in the Maxwell sense — the same law gives:

| | net drift | rms width, end/start |
|---|---|---|
| one-sided (codebase convention) | $0.5728449$ | $\approx1$ |
| in-phase transverse (Maxwell reading) | $1.0\times10^{-8}$ | $3.37$ |

The in-phase seed has spectral support at both $\pm\mathbf k_0$; $\Omega_\text{pair}$
is even, so the two halves carry opposite $\nabla_k\Omega$ and the packet separates
into counter-propagating halves with no net motion.

So the two $(\mathbf E,\mathbf B)$ identifications are **visibly different objects**
under the even pair law. Which of them is the physical electromagnetic field is
exactly the question the curl family F21/F23/F25/**F306** is open on — F306 having
just established that the σ-bilinear curl equation closes at $O(k^3)$ *once
$\mathbf E$ and $\mathbf B$ are read as analytic amplitudes rather than as the real
quadrature pair*, which is the same distinction appearing here in real space rather
than in a residual. This finding does not adjudicate it; it records that the
question has a clean, cheap real-space diagnostic
(`run_inphase_transverse_packet`), and that the diagnostic is in the result
artifact. Flagged for Ben in `docs/roadmaps/next-steps.md`.

## What this does and does not show

**Does.** The model's actual photon — the paired-spinor photon of F67/F68/F69,
propagated by its own unmodified even law — exists as a localised real-space
packet, crosses the lattice wrap-free, conserves its energy while doing so, and
moves at the velocity its own dispersion predicts to $8\times10^{-16}$, with the
finite-aperture deficit resolved exactly rather than approximated.

**Does not.** This is an **on-axis** measurement, and on a coordinate axis
$\omega^+=\omega^-$, so $\Omega^\pm_\text{split}=2\omega^\pm(k/2)$ coincide with
$\Omega_\text{pair}$ exactly. **The retired σ-bilinear photon would give the same
drift here.** This run therefore does *not* discriminate the pair law from a
single-branch law; that discrimination is off-axis and is F65/F66's, already
settled in momentum space. Two related numbers measured in passing, both off-axis
along the body diagonal: the pair law and a single-branch law differ in speed at
the $5\times10^{-5}$ level ($0.3226312$ vs $0.3226157$ per axis component), while
the two branches give the *same* speed as each other to $6.3\times10^{-16}$ — no
birefringent time-of-flight along that symmetry direction, consistent with F30's
"the linear term is chiral, not a net time-of-flight effect".

Nor does it re-derive the photon: `gauge.photon` is used unmodified. This module
owns only the seed, the estimator, and the closed-form target.

## Prior art

The Gaussian-wavepacket drift $v=(\nabla_k\omega)(k_0)$ on this automaton is the
source literature's own result — Bisio, D'Ariano, Perinotti and Tosini,
`references/qca-papers-1-4-overview.md:193` (arXiv:1601.04842) — and F20 records it
for the fermion legs. What is claimed as derived here is the closed form
$\partial\Omega_\text{pair}/\partial k_i=\tfrac{c_\text{lat}}{2}[\hat g^+_i+\hat g^-_i](\mathbf k/2)$
for the *pair* rate, its exact on-axis value, and the carrier condition
$k_0\sigma_\text{axis}\gtrsim5$ that one-sidedness requires on a lattice. The rest
is claimed only as built.

## Exactness

| Result | Class | Tolerance | Record |
|---|---|---|---|
| $u^\pm(\tfrac k2\hat x)=\cos(\tfrac{k\,c_\text{lat}}{2})$, both branches | **exact** | 0 | `F314-pair-group-velocity-closed-form` |
| $\Omega_\text{pair}(k\hat x)=k\,c_\text{lat}$ | machine | $2\epsilon/\sin(\pi/(n_k{-}1))$, derived | same |
| $\partial\Omega_\text{pair}/\partial k_x=c_\text{lat}$ on-axis, all $k$ | machine | $10^{-10}$ | same |
| $\partial\Omega_\text{pair}/\partial k_i$ vs central difference, $i=x,y,z$ | machine | $10^{-8}$ | same |
| packet drift $=\langle\partial\Omega_\text{pair}/\partial k_x\rangle$ | machine | $10^{-12}$, derived | `F314-photon-packet-propagation` |
| $\sum(\lvert\mathbf E\rvert^2+\lvert\mathbf B\rvert^2)$ on the moving packet | machine | $10^{-12}$ | same |
| polarisation independence of the drift | **exact** | 0 | same |

The $10^{-12}$ is pre-registered and derived, not read off: at the asserted wrap
ceiling $\varepsilon\le10^{-15}$ the arithmetic-centroid bias is $\varepsilon L/v=2.2\times10^{-13}$
relative, and the float64 FFT round-off floor over 24 spectral rotations is the same
order. The residual lands three decades below both.

## Artifacts

- `src/casim/engine/gauge/photon_packet.py` — the module (registry `gauge.photon_packet`, `_SPINE`)
- `tests/findings/test_F314_photon_packet_propagation.py` — 10/10 PASS
- `test-results/F314_photon_packet_propagation.json` — closed forms, gate run, $L{=}256$ production run, undersampled-carrier control, in-phase diagnostic
- `casim test --finding F314`
