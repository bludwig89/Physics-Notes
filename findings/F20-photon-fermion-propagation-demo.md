# Finding 20 — Wavepackets propagate across the BCC lattice at the group velocity the automaton's own dispersion predicts

> **[PARTIALLY SUPERSEDED 2026-08-04 by F306 — ledger S18-curl-residual-representation-artifact]**
>
> **DEAD:** Item (3) only -- the composite-photon leg, which used the sigma-bilinear photon of casim.engine.gauge.bilinear that S1-F69 retired on 2026-06-01 (helicity<->branch birefringent, excluded by GRB/AGN polarimetry, F65/F66/F67) and which F302 showed is not even an SO(3) 3-vector in its transpose form.
>
> **STILL LIVE:** Items (1) and (2), Weyl and Dirac real-space propagation, which were PROMOTED by their remediation to machine precision: Dirac packet drift agrees with <dw/dk_x> to 1.7e-15 wrap-free, and omega(k x_hat) = k c_lat is an exact tol-0 gate record. That is where the quantitative content of this finding now lives.
>
> **NOTE:** The photon of the model is the paired-spinor photon (casim.engine.gauge.photon, F67/F68/F69, CLAUDE.md Core Design Decision 5).
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


*Recorded 2026-05-22 - 13:42. Run: `tests/runners/run_propagation_demo.py` (demonstration + figure). Result: `test-results/propagation_demo_2026-05-22.json`. Figure: `test-results/figures/propagation_demo.png`.*

*Quantitative core (added 2026-08-03): `casim.engine.lattice.wavepacket`. Result: `test-results/F20_wavepacket_group_velocity.json`. Records: `F20-bcc-onaxis-dispersion-exact`, `F20-wavepacket-group-velocity` (both gate tier).*

**Reviewed:** 2026-08-03 — **OVERSTATED** ([independent review](../docs/reviews/F20-review-2026-08-03.md))
**Remediated:** 2026-08-03 — 11 applied · 1 rejected · 1 deferred · 1 escalated ([remediation](../docs/reviews/F20-remediation-2026-08-03.md))

## Question

Can excitations *exist naturally and move across* the lattice as localised
real-space packets, and does the measured centroid velocity match what the
automaton's own dispersion says it should be? Prior evidence was momentum-space
(dispersion, transversality, energy gates).

## Summary

**Yes, and to machine precision — but not against $c_\text{lat}$, and not on a
periodic box.**

Two things had to be got right before the demonstration became a measurement,
and the original version of this finding got neither:

1. **The right target.** A finite-width packet does not travel at $c_\text{lat}$.
   Its centroid velocity is the packet-weighted average of the *closed-form*
   group velocity, and for a **fixed** seed spinor there is a second effect —
   branch admixture — that roughly **doubles** the deficit.
2. **A wrap-free box.** On the original periodic $64^3$ box the packet wraps
   within 44 ticks; the arithmetic centroid then picks up a bias of the same
   order as the physics, and the box scan is monotone and reaches
   $1.024\,c_\text{lat}$ — *superluminal* — at $L_x = 192$.

With both corrected, the agreement is $10^{-15}$, not $10^{-2}$.

## The closed forms

Everything below is `casim.engine.lattice.wavepacket`.

**The exact on-axis identity.** Along a coordinate axis the two transverse
cosines are $\cos 0 = 1$ and the two transverse sines are $\sin 0 = 0$ — both
exactly representable — so the BCC Bloch scalar collapses:

$$u^\pm(k\hat x) = c_x\cdot1\cdot1 \pm s_x\cdot 0\cdot 0 = \cos(k\,c_\text{lat})
\qquad\Longrightarrow\qquad \boxed{\;\omega(k\hat x) = k\,c_\text{lat}\;}$$

for **both branches**, over the whole range $0\le k\le\pi/c_\text{lat}$. This is
an algebraic identity, not a small-$k$ limit: $\partial^2\omega/\partial k_x^2
\equiv 0$, so the on-axis lattice light cone is exactly straight and carries no
$k^2$ Lorentz-violating term whatsoever. Verified at **tolerance 0** — the
residual $|u^\pm - \cos(k\,c_\text{lat})|$ is bit-for-bit $0.0$ at 500 sample
points on both branches. The same residual along the body diagonal is $1.954$,
which is the control that keeps the exact check from being a tautology.

**Group velocity in closed form.** Since $\partial u/\partial k_x = -c_\text{lat}n_x$
and $\sqrt{1-u^2} = |n|$,

$$\frac{\partial\omega}{\partial k_x} = c_\text{lat}\,\hat n_x(\mathbf k),
\qquad
\frac{\partial\omega_\text{Dirac}}{\partial k_x}
 = \frac{c_\text{lat}\,n_\text{kin}\,n_x}{\sqrt{1-n_\text{kin}^2u^2}},
\quad n_\text{kin}=\sqrt{1-m^2}.$$

Both agree with central differences of the analytic dispersion at 30 random
off-axis $\mathbf k$ to $5\times10^{-11}$ — the $h^2$ floor.

**Finite-width packet velocity.** Two corrections, and the second is the one the
original text missed:

* *aperture / tilt* — off-axis modes have $\hat n_x < 1$;
* *branch admixture* — a **fixed** seed spinor $\chi_+(\mathbf k_0)$ is not an
  eigenspinor at $\mathbf k\neq\mathbf k_0$. Weight $(1-\hat n_x)/2$ lands on the
  opposite branch, which moves at $-v_x$.

$$\langle d\bar x/dt\rangle = c_\text{lat}\langle\hat n_x^2\rangle \ \ \text{(fixed seed)},
\qquad
c_\text{lat}\langle\hat n_x\rangle \ \ \text{(branch-pure seed)}.$$

The ratio of the two deficits is $(1-\langle\hat n_x^2\rangle)/(1-\langle\hat n_x\rangle)
= (1+\langle\hat n_x\rangle) - \mathrm{Var}(\hat n_x)/(1-\langle\hat n_x\rangle)$,
which is $1.981$ for this packet and $\to 2$ as the packet narrows in $k$.

## Results

Wrap-free box $256\times64\times64$, packet started at $x=60$, $\sigma=(6,10,10)$
as an **amplitude** width, $k_0 = 0.8\,\hat x$, 44 ticks. Boundary weight
$\le 4\times10^{-17}$ in every run, so nothing wraps.

| Packet | seed | measured drift | closed form | rel. residual |
|---|---|---|---|---|
| Dirac $m=0.3$ | branch-pure | 0.4654257818 | $\langle\partial\omega/\partial k_x\rangle$ | $\mathbf{1.7\times10^{-15}}$ |
| Dirac $m=0.5$ | branch-pure | 0.3485063259 | $\langle\partial\omega/\partial k_x\rangle$ | $\mathbf{1.6\times10^{-15}}$ |
| Weyl $m=0$ | branch-pure | 0.5723031484 | $c_\text{lat}\langle\hat n_x\rangle$ | $2.2\times10^{-12}$ |
| Weyl $m=0$ | fixed $\chi_+(k_0)$ | 0.5673504144 | $c_\text{lat}\langle\hat n_x^2\rangle$ | $2.6\times10^{-7}$ |

Reading the rows:

* **A branch-pure seed has no $\pm$beat, so the centroid velocity is an exact
  Ehrenfest statement** and the only error left is float64 FFT round-off. That is
  why the two Dirac rows sit at $10^{-15}$.
* The massless branch-pure row is one decade worse because the helicity projector
  $(I+\hat n\cdot\sigma)/2$ is **singular at $k=0$**, where $\omega=0$ and $\hat n$
  is undefined. The gapped walk has no such point. This is stated, not fitted.
* The fixed-seed row relaxes onto its closed form only *asymptotically*: the
  $\pm$branch beat at $2\omega$ dephases across the packet's $k$-spread. The
  first tick displacement is exactly $c_\text{lat}$; by tick 30 the per-tick
  displacement is within $6\times10^{-7}$ of $c_\text{lat}\langle\hat n_x^2\rangle$
  and by tick 40 within $1\times10^{-10}$. A least-squares slope over the *whole*
  window still carries the transient at the $\sim2\times10^{-4}$ level.

**Both legs move under perturbation**: $m: 0.3\to0.5$ moves measurement and
prediction together, $0.4654258\to0.3485063$.

## Interpretation

1. **Massless excitations propagate at the emergent light speed, and massive ones
   strictly below it** — but neither at $c_\text{lat}$ itself for a packet of
   finite width. The correct statement is that the packet moves at the
   packet-weighted closed-form group velocity, which is $c_\text{lat}$ only in the
   plane-wave limit.
2. **The on-axis cone is exactly straight.** $\omega(k\hat x) = k\,c_\text{lat}$
   to tolerance 0 is the strongest single result in this finding, and it is
   stronger than a $k\to0$ statement: there is *no* on-axis lattice dispersion at
   any $k$ in the Brillouin range.
3. **Wrapping, not physics, produced the original numbers.** The box scan on the
   original periodic protocol, identical physics, only $L_x$ varied and using the
   same arithmetic centroid: 0.575200 (64) → 0.579126 (96) → 0.583058 (128) →
   0.590922 (192) → 0.567340 (256, wrap-free). $L_x=192$ exceeds $c_\text{lat}$,
   which by itself proves the fitted slope is not a group velocity on the torus.

## Prior art

The Gaussian-wavepacket drift $v = (\nabla_k\omega)(k_0)$ with diffusion tensor
$D = \nabla\nabla\omega$ on this automaton is the source literature's own result —
Bisio, D'Ariano, Perinotti and Tosini, recorded in this repo at
`references/qca-papers-1-4-overview.md:193` (arXiv:1601.04842). Zitterbewegung
smearing from a mixed $\pm$energy seed is the central worked example of the 1D
Dirac QCA papers (arXiv:1212.2839, arXiv:1305.0461). The bilinear composite
photon is Paper 1 Eqs. 33/35, listed at `qca-papers-1-4-overview.md:403` as a
to-do *taken from* the literature.

So: **the construction is a reimplementation, not a discovery.** What is not in
the cited literature, as far as this session could establish, is the exact
on-axis identity on the 3D BCC walk and the branch-admixture factor
$\langle\hat n_x^2\rangle$ vs $\langle\hat n_x\rangle$ for a fixed seed spinor.
Those two are claimed as derived here; the rest is claimed only as built.

## Caveats and stated conventions

The review found five inputs that move the answer and were never declared. They
are declared now:

* **$\sigma$ is an amplitude width**: the envelope is $\exp(-\sum_i(x_i-c_i)^2/2\sigma_i^2)$.
  Reading it as a density width moves every number by $\sim1\%$.
* **Box and start position**: $256\times64\times64$, packet at $x=60$. Boundary
  weight is asserted $\le10^{-12}$; the original $64^3$ result is a torus artifact.
* **Estimator**: arithmetic centroid of $\rho = \sum_c|\psi_c|^2$. Not
  $\omega$-weighted.
* **Fit window**: the reported number is the mean per-tick displacement over the
  last 14 ticks, not a least-squares slope over the whole run. For a branch-pure
  seed the two agree exactly; for a fixed seed they differ at $2\times10^{-4}$.
* **Seed**: `branch-pure` (per-$k$ projector) or `fixed` ($\chi_+(k_0)$ everywhere).
  These are different claims with different closed forms.

Two things that were previously claimed as gates and are **not**:

* **Transversality $4.6\times10^{-17}$ was zero by construction.**
  `bilinear.EM_bilinears` applies `_transverse_part(G, n̂)` and the test then
  measures $\hat n\cdot E$. Worse, at this finding's own on-axis momentum
  $G = \hat n$ exactly, so $E_G$ and $B_G$ are *identically zero* and the residual
  is $0/0$. The misleading docstring is corrected (`bilinear.py`, 2026-08-03).
* **Poynting conservation $4.8\times10^{-14}$ was not measured on a moving
  packet.** It is computed by applying a global scalar phase with **no lattice
  step at all**, at a different momentum. The quantity actually tracked in item
  (3), $\sum_i|G^i(x)|^2$, is **not conserved**: it falls $1.000\to0.628$ over the
  44 ticks and $\to0.289$ by tick 100, identically at every box size. Fitting a
  line to the centroid of a density that has lost 37% of its weight is not an
  Ehrenfest group velocity, and the composite-photon "$0.5530$" is one arbitrary
  fit window (0.546 → 0.569 across windows, still climbing toward $c_\text{lat}$).

Retained from the original, and still true: the naive $\eta$-only Dirac seed
gives an 8.4% velocity error from zitterbewegung. The per-$k$ positive-energy
projector used here removes the residual admixture at $k\neq k_0$ as well, which
is what buys the last several orders of magnitude.

## Exactness

| Result | Class | Tolerance | Record |
|---|---|---|---|
| $u^\pm(k\hat x) = \cos(k\,c_\text{lat})$ | **exact** | 0 | `F20-bcc-onaxis-dispersion-exact` |
| $\omega(k\hat x) = k\,c_\text{lat}$ | machine | $2\epsilon/\sin(\pi/(n_k{-}1))$, derived | same |
| $\partial\omega/\partial k_x = c_\text{lat}\hat n_x$ | machine | $10^{-8}$ vs central difference | same |
| Dirac packet drift $=\langle\partial\omega/\partial k_x\rangle$ | machine | $10^{-12}$ | `F20-wavepacket-group-velocity` |
| Weyl fixed-seed drift $= c_\text{lat}\langle\hat n_x^2\rangle$ | quant | $10^{-6}$ | same |
| Composite-photon velocity | **withdrawn** | — | superseded construction |

## Corrections

**2026-08-03 - 20:40** — per [independent review 2026-08-03](../docs/reviews/F20-review-2026-08-03.md),
verdict **OVERSTATED** (2 PASS · 2 WEAKENS · 9 FAIL).

| Was | Now | Why | Attack |
|---|---|---|---|
| "Weyl fermion 0.5752 vs $1/\sqrt3$, **0.37%**" | Wrap-free 0.5673504 vs $c_\text{lat}\langle\hat n_x^2\rangle$, $2.6\times10^{-7}$ | The 0.37% was a $+1.4\%$ torus-wrap bias cancelling a real $-1.74\%$ deficit, measured against the wrong target | 5, 12 |
| "Dirac $m{=}0.3$ 0.4667 vs $d\omega/dk$, **1.06%**" | Branch-pure 0.4654257818, residual $1.7\times10^{-15}$ | Same box defect, plus a residual $\pm$energy admixture the $k_0$-only eigenmode seed does not remove | 5, 12 |
| "off-axis modes have $\partial\omega/\partial k_x < 1/\sqrt3$" (tilt alone) | Tilt **and** fixed-spinor branch admixture: $c_\text{lat}\langle\hat n_x^2\rangle$, not $c_\text{lat}\langle\hat n_x\rangle$ | The stated mechanism was wrong by a factor of $1.98$ in the deficit | 12 |
| "the momentum-space gates … are at machine precision" | The dispersion residual is $2.1\times10^{-3}$; transversality and Poynting are identities, not measurements | Exactness inflation; the transversality figure is $0/0$ on an identically-zero field at this finding's own momentum | 3, 4 |
| "$\omega=k_x/\sqrt3$ … exactly linear" (prose only) | Registered at **tolerance 0** with an off-axis control, plus zero curvature | The strongest result here was stated and never guarded — under-claiming is a defect too | 3 |
| "it conserves Poynting energy during the motion" | $\sum_i\lvert G^i\rvert^2$ falls $1.000\to0.628$ over the run | The conservation number came from a different object at a different momentum, propagated by a scalar phase with no lattice step | — |
| "All three excitations traverse the lattice at the emergent light speed" | Massless *approach* it; massive is strictly below; the composite-photon leg is withdrawn | Widest statement, unsupported by the body, and it contradicted its own next clause | 10 |
| no test record; `legacy_script` "runs and cannot fail" | Two gate records with real `entry`/`params`/`expect`, and `findings: [F20]` on the runner | `casim test --finding F20` selected nothing | 7, 8 |
| JSON written at module level | Guarded behind `__main__`; duplicate side-copy removed | An import walk would overwrite the committed baseline | 8 |
| `SQRT3 = np.sqrt(3.0)` | `SQRT3 = 1.0/c_lat` from `casim.constants` | D7: rogue literal reproducing a registry value | 1 |
| no prior-art section | `## Prior art` separating "built" from "derived" | Bisio et al. drift/diffusion is the repo's own recorded reference | 11 |

**Confirmed unchanged by the review.** The runner reproduces bit-for-bit at 15
significant figures — both a blind agent working only from the engine modules and
the adversarial referee re-implemented it and got
`0.575200387246309 / 0.46673254042763357 / 0.5530258723673788` exactly. The
comparison targets were never circular (attack 1 PASS): $1/\sqrt3$ is a closed
form and `vg_dirac_pred` is a central difference of the analytic dispersion, not
a frozen script output. The blind agent derived the on-axis identity and both
closed-form group velocities **independently**, from the engine's update rules,
without reading this finding — that is the strongest support available, and this
finding now states it.

**Rejected.** Recommendation 6 of the review — re-triage
`docs/status/exactness-inventory.md:1850/1870/1903` — is rejected as stated: those
rows are auto-generated from `test-results/manifest.json` by `casim index` and are
not hand-editable, so "re-triaging" them means editing generated output. The
underlying complaint (protocol numbers presented as physics residuals with an
empty finding column) is real and is addressed at the source instead: the rows
now carry `findings: [F20]` through the runner record, and the numbers they quote
are labelled in this finding as protocol numbers on a wrapped box.

## Status

**Live** for items (1) and (2) — the Weyl and Dirac legs, now at machine
precision with two gate records.

**Withdrawn** for item (3), the composite photon. The construction is the retired
σ-bilinear one.

Open, and carried forward:

* **ESCALATED to Ben.** Adding F20 to `docs/theory/supersessions.yaml` under
  `S1-F69-sigma-bilinear-photon`, with per-item DEAD/LIVE text, is a
  supersessions edit and therefore not something a remediation session does on its
  own authority. F17 and F18 were added to that ledger entry and retired to
  `deprecated/findings/` on 2026-08-03; F20 is the third file in the family and
  was left out. Note also that the F302 survey line stating `bilinear_G` has zero
  live consumers is wrong — `tests/runners/run_propagation_demo.py:193-197`
  hand-rolls the identical algebra.
* ~~**DEFERRED.** Redo the propagation demonstration with the **paired-spinor**
  photon (`casim.engine.gauge.photon`) so the "a photon exists and moves" claim
  is made with the photon the model actually has.~~ **CLOSED 2026-08-04 by
  [[F314-paired-photon-real-space-propagation]]** (`casim.engine.gauge.photon_packet`,
  two gate records). Wrap-free box, one-sided seed, measured against the
  closed-form packet-weighted $\langle\partial\Omega_\text{pair}/\partial k_x\rangle$:
  residual $7.8\times10^{-16}$, energy conserved to $3.7\times10^{-15}$ on the
  moving packet. Item (3)'s claim is now made with the photon the model has, and
  the two gates F20's photon leg failed — conservation during motion, and a target
  that is not $c_\text{lat}$ — are both green there.
* **Latent defect in this finding's own module, flagged 2026-08-04 by F314 and
  NOT patched.** `lattice.wavepacket.weyl_group_velocity` returns
  $c_\text{lat}\hat n_i$ and §"The closed forms" above states
  $\partial\omega/\partial k_i = c_\text{lat}\hat n_i$ as a general identity. It
  holds for $i=x$ **only**: $g_y=-s\,n_y$ (a sign flip) and $g_z$ is not $\pm n_z$
  at all, because the $n$-vector is $\nabla u$ only on the $x$-axis. Residuals
  against a central difference at 200 random $\mathbf k$: $1.2\times10^{-10}$ (x),
  $0.722$ (y), $0.407$ (z). **No number in F20 moves** — every call site here
  passes `axis=0` — but the docstring and the prose above are wrong as written.
  The correct general form is in
  [[F314-paired-photon-real-space-propagation]] §"Defect found in a neighbouring
  module"; the fix is one docstring and one narrowed signature, in `lattice/`.
* The pre-C9 module names in the original text (`ca_bcc.py`, `ca_dirac_bcc.py`,
  `ca_maxwell.py`) are repointed; the dead wikilink
  `[[finding-17-poynting-energy-conservation]]` matched no file anywhere in the
  tree and is now pointed at the deprecated file.

## Cross-references

- Fermion substrate: `casim.engine.lattice.bcc` (Weyl),
  `casim.engine.particles.dirac_bcc` (Dirac). Closed forms and the wrap-free run:
  `casim.engine.lattice.wavepacket`.
- Composite photon (superseded construction): `casim.engine.gauge.bilinear`;
  see [[F302-sigma-bilinear-so3-covariance]] and ledger
  `S1-F69-sigma-bilinear-photon`.
- Momentum-space companions, both retired to `deprecated/findings/` on 2026-08-03:
  [[F17-poynting-energy-conservation]], [[F18-mohr-c5-c6-build]].
- $c_\text{lat}$ as a rotation rate: [[F26-real-rotation-and-c-lat]] — the on-axis
  identity above is the exact statement of the $k$-linearity that F26 assumes.
- Curl-equation follow-up: [[F21-curl-residual-geometry-independence]].
