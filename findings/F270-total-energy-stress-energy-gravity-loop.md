# F270 — One energy convention, a global conservation gate, and the closed gravity loop

> **[PARTIALLY SUPERSEDED 2026-08-01 by F271 — ledger S10-F271-eikonal-dielectric-photon]**
>
> **DEAD:** Section 4's eikonal gauge-side dielectric coupling for the PHOTON channel -- a rotation about a single stated central rate omega0, which was a free parameter with an O(1), non-convergent error. Superseded by F271's k-resolved photon_step_dielectric. PhotonPairChannel no longer accepts grav_omega0.
>
> **STILL LIVE:** The one energy convention and the global conservation gate -- the rest of the finding -- and dielectric_mix_half itself, kept as a CONTROL: it is exactly orthogonal pointwise where the k-resolved form is only convergently so.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


*2026-08-01 - 00:10. Roadmap `roadmap-unified-program.md` **P3.4 / P3.5 / P3.6**, structural blocker **B5** (both parts) and **B4**.*
*Status: **established** (fixed, gated). One deliberately-labelled open item: the eikonal order of the gauge-side dielectric coupling.*

**Test record:** record `P3.4-P3.6-total-energy-and-gravity-loop` (tier gate) — `tests/casim/test_total_energy_and_gravity_loop.py`, T1–T10: one gauge-energy convention across the engine, agreement with the gravity source, global conservation to machine class, a missing energy leg reported rather than counted as zero, and the dielectric legs — T8 keeps `dielectric_mix_half` as the control this banner describes. Declared 2026-08-19.

## 1. B4 was two defects, not one (P3.5)

The roadmap recorded B4 as *"six incompatible energy conventions; nothing a
coupled run could fail"*, and diagnosed it as a missing ½. Measurement found the
factor **and a second, deeper mismatch underneath it**.

**The ½.** `PhotonPairChannel.energy` returned $\sum(E^2+B^2)$ while
`coupled.field_energy` returned $\tfrac12\sum(E^2+B^2)$ — exactly twice, for the
same field. Worse, `gravity.T00_field_energy` — the function that *sources
gravity* from a gauge field — always had the ½. **A field weighed half what it
cost.**

Decision (Ben, 2026-07-31): **the ½ wins.** It is the physical field energy
density, it is what already sourced gravity, and the alternative would have made
every engine-wide energy twice what any GR or QED comparison expects. There is
now one definition, in `channel.field_energy`, and `coupled.field_energy` *is that
same object* rather than an agreeing copy — asserted, because two definitions
that agree today are two definitions.

Baseline impact, measured before the change rather than discovered after:
**0 registry-declared baselines move.** 55 git-tracked result dumps carry an
absolute gauge energy and will move by exactly 2× **when re-run** — recorded as a
supersession with the factor stated, not as drift.

**The mismatch underneath.** `Channel.energy` is documented as "a conserved
positive scalar (norm / field energy)" and that slash is the bug: spinor channels
return $\sum|\psi|^2$, a dimensionless **probability norm**, while gauge channels
return an **energy**. Summing them is meaningless whichever way the ½ goes, so
unifying the ½ alone would not have produced a total energy.

`Channel.energy` is therefore kept as what it actually is — the conserved *drift
probe* — and a separate additive `Channel.energy_density(state)` added, in one
convention: $\tfrac12(E^2+B^2)$ for gauge, the F106-E5 rest leg $m|\Psi|^2$ for
matter. The `TotalEnergy` observer sums *that*.

**A channel that cannot express an energy density returns `None` and is listed
under `missing` — never counted as zero.** An absent leg and a vanishing leg are
different claims and only one is checkable; a total silently missing a term is
worse than no total, because it looks conserved.

Measured: free `photon_pair`, $L=16$, 1000 ticks — `max_rel_drift` $3.4\times10^{-14}$,
class **machine**, coverage 1/1.

## 2. The colour-axis broadcast bug (P3.4, B5 part 1)

`T00_dirac_rest` did not sum a leading component axis. `T00_field_energy`,
thirteen lines below, always did.

A colour-carrying spinor — a `quark_dirac` named in a `gravity_dielectric`
channel's `sources:` — has shape $(3,L,L,L)$. The returned density kept its colour
axis, broadcast against the $(L,L,L)$ potential, and **silently promoted the
entire gravity state to rank 4**. The run did not crash. It produced a three-copy
gravitational field, one per colour, and reported success.

Colour is not a spatial index; a quark does not gravitate three times. The axis is
now summed — the same contraction `T00_field_energy` performs for the $(8,L,L,L)$
gluon. **Rank-3 input is untouched, so no existing result moves**: the bug could
only fire in a configuration that had never been run, which is exactly why it
survived.

## 3. The kinetic leg, and $T^{0i}$ (P3.4)

`T00_dirac_rest`'s own docstring flagged the kinetic term as *"fork-level, not yet
in the production source"*, while **D-EM3 demands that a fast packet gravitate by
its total energy**. With only the rest leg, a packet boosted to relativistic
momentum sources *exactly the same gravity* as one at rest — mass–energy
equivalence was absent from the production gravity source.

`T00_dirac_kinetic` supplies it, using the same centred difference as `lap_nd` so
a gradient energy cannot disagree with the potential it sources. It is a separate,
additive function rather than folded into the rest leg, so every committed
rest-leg result stays reproducible and the two can be compared — which is what
makes the D-EM3 claim testable.

**Verified against its closed form, not a threshold.** A centred difference on
$\psi=\phi\,e^{ikx}$ gives $\sin k$ where the continuum gives $k$, so the boost
energy is

$$\Delta u_\text{kin}=\tfrac12 c^2\sin^2\!k\sum|\psi|^2$$

up to a $k$-**independent** envelope-averaging factor tending to 1 as the packet
widens. Both halves are measured:

| $L$, width | $k=0.4$ | $k=0.8$ | $k=1.2$ |
|---|---:|---:|---:|
| 32, $w=72$ | 0.97254 | 0.97255 | 0.97259 |
| 40, $w=128$ | 0.98719 | 0.98434 | 0.98442 |

The ratio to the prediction is constant across $k$ to $<10^{-4}$ — so the
$\sin^2 k$ law is exact — and moves toward 1 with envelope width — so the residual
is the envelope, not a wrong coefficient.

`T0i_dirac` adds the momentum density $T^{0i}=c\,\mathrm{Im}(\psi^\dagger\partial_i\psi)$,
because a scalar $\Phi$ sourced from $T^{00}$ alone knows a packet's *location*
but not its *motion*: the gravitomagnetic sector is structurally absent rather
than small. Verified to vanish at rest (to $10^{-12}$) and to point along the
boost with transverse components below $10^{-9}$ of the longitudinal one.

## 4. The gravity loop closes on the gauge side (P3.6, B5 part 2)

B5 recorded that **no gauge channel reads $K$**. Gravity was sourced by matter and
read back by matter; the gauge sector sat outside the loop entirely, so light did
not bend in the production engine at all — deflection existed only in
`forks/gravity/gr_fork_F64_em_connection.py`.

`Channel.read_K` is the read side, available to every channel. `dielectric_mix_half`
is the gauge-sector counterpart of `lapse_mix_half`: the F64 dielectric
renormalises the local rotation rate of the real $(E,B)$ pair, applied as a
rotation **in the $(E,B)$ plane**

$$\begin{pmatrix}E\\B\end{pmatrix}\leftarrow
\begin{pmatrix}\cos\delta & -\sin\delta\\ \sin\delta & \cos\delta\end{pmatrix}
\begin{pmatrix}E\\B\end{pmatrix},\qquad
\delta(x)=\tfrac{\Delta t}{2}\,\omega_0\!\left(\tfrac{1}{K(x)}-1\right)$$

used Strang-wise around the homogeneous spectral step.

Two properties make it safe, and both are asserted:

* **Exactly norm-preserving.** A real orthogonal rotation at every site, so
  $E^2+B^2$ is conserved *pointwise*, not merely in sum (measured $3.6\times10^{-15}$).
  The dielectric cannot manufacture or leak field energy, so the P3.5 total-energy
  gate stays meaningful with gravity on.
* **Exactly the identity at $K\equiv1$.** $\delta\equiv0$, bit-identical to the
  pre-P3.6 engine. No committed result moves.

Measured on a lensing scenario ($L=24$, $M=6$, 50 ticks): photon energy drift
$9.1\times10^{-15}$, and $\max|E_\text{grav}-E_\text{flat}| = 0.20$ — gravity
demonstrably acts on the gauge field, unitarily, outside the fork.

$\omega_0$ is **required, never defaulted**. A silently-chosen central rate is a
fitted parameter wearing a default's clothing; the channel raises if it is absent.

### The open item, stated plainly

**This is the eikonal (leading-order) coupling and it is labelled as such.**
$\omega_0$ is a single representative rotation rate, so the mix is exact only in
the geometric-optics limit where the packet is narrow in $k$. The true rate
difference is $k$-dependent ($\Omega(k)/K$ versus $\Omega(k)$), and a
position-dependent, $k$-dependent rate cannot be applied by one homogeneous FFT —
which is precisely why the spectral BCC kernels were called homogeneous and
deflection was left fork-only in the first place.

The exact treatment needs either a variable-$c$ stepper of the
`weyl_step_2d_varc_strang` kind lifted to 3-D $(E,B)$, or a multiplicative
operator split with a $k$-resolved local rate. **That derivation is open and is
not claimed here.** What is claimed is narrower and checkable: the production
engine closes the loop at eikonal order, deflection is measurable outside the
fork, and the coupling is unitary.

## Evidence

`tests/casim/test_total_energy_and_gravity_loop.py`, 10 checks, gate tier,
`expect: {exactness: machine, tol: 1e-12}`.

| # | Check | Result |
|---|---|---|
| T1 | all four gauge channels use the one ½ convention; `coupled.field_energy` **is** the same object | exact |
| T2 | channel energy equals the T⁰⁰ that sources gravity from it | exact |
| T3 | total energy over 1000 ticks | 3.4e-14, class `machine` |
| T4 | a missing energy leg is reported, not counted as zero | exact |
| T5 | colour axis summed; rank-3 input untouched | exact |
| T6 | kinetic leg follows $\tfrac12c^2\sin^2\!k$; rest leg stays boost-blind | <1e-4 across $k$ |
| T7 | $T^{0i}$ vanishes at rest, points along the boost | 1e-12 / 1e-9 |
| T8 | dielectric mix pointwise unitary; $K\equiv1$ exact identity | 1e-13 |
| T9 | light responds to gravity in the production engine, unitarily | drift 1e-12, Δ 0.2 |
| T10 | an implicit $\omega_0$ is refused | exact |

## Cross-references

`docs/roadmaps/roadmap-unified-program.md` §P3.4–P3.6 · F64, F106 (the sourcing
law), F62 (lapse-mix sign), D-EM3 · [[F268]] · [[F269]] ·
`forks/gravity/gr_fork_F64_em_connection.py` (the exact-deflection test bed)
