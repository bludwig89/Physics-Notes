# Correlation pass — handoff item B.3 (celestial holography vs. the model's null-vector/spinor machinery)

*2026-09-23 · answers `notebook-sm-crosscheck-handoff.md` §B item 3 · sources:
[F397](../../findings/F397-notebook-factorization-route-pp176-182.md) (`src/casim/engine/gauge/factorization.py`),
[F178](../../findings/F178-gravity-full-tensor-adoption.md), [F190](../../findings/F190-horizon-entropy-lattice-microstates.md),
[F193](../../findings/F193-ontic-vacuum-gravitates-as-zero.md), [F196](../../findings/F196-dilution-exponent-derived.md),
[F241](../../findings/F241-omega-lambda-o1-residual-anthropic.md), F26/F180 (c_lat, light-cone speed),
`docs/theory/notebook-sm-crosscheck-pp110-124-what-is-a-spinor.md` (NB-149 verdict),
`src/casim/engine/core/_viz_spinor_color.py`*

## The question

Celestial holography represents a null light-ray direction at null infinity by its energy and a
stereographic complex coordinate $(z,\bar z)$ on a "celestial sphere" — structurally the same
object the notebook builds independently at pp.110-124/176-182 (a spinor/null direction
represented by a stereographic coordinate $\zeta$). (1) Does the model's own treatment of null
vectors/light-cone structure have a structural point of contact with the celestial-sphere
parametrization? (2) If the model ever needs an asymptotic/holographic description of its own
gravity sector (F178's induced Einstein equation), is celestial holography's flat-space approach a
relevant comparison point, as opposed to AdS/CFT (which needs $\Lambda<0$)?

## Answer

**(1) Yes, concretely — the model already has the identical algebraic object in code, not just at
the notebook level.** `t1_spinor` in `src/casim/engine/gauge/factorization.py` (F397, closing
notebook pp.176–182) maps a future-null 4-vector $N=(N_0,\vec N)$ to a 2-spinor
$\psi=(\alpha,\beta)$ with $\psi\psi^\dagger=\sigma\cdot N$, free up to the phase $e^{i\theta}$ —
exactly Penrose's null-vector/spinor correspondence, exactly the notebook's pp.110-124
stereographic-projection object (NB-149, graded IMPROVES/ACTIVE by the cross-check), and exactly
what celestial holography calls representing a light ray by its energy $\omega=N_0$ and a
stereographic coordinate on the celestial sphere. The ratio $\zeta=\beta/\alpha$ *is* the
celestial $z$ for that direction, at fixed "energy" $N_0$; F397's own free phase $\theta$ is the
same little-group/helicity freedom celestial amplitudes carry. This is exact and gate-tested (F397
verified $\psi\psi^\dagger=\sigma\cdot N$ to $10^{-13}$), not an approximation.

Two caveats keep this from being more than a structural echo today:

- **It is a local, per-momentum construction, not an asymptotic one.** F397's $N$ is any future-null
  4-vector evaluated at a point; celestial holography's $z$ is specifically the direction data of a
  massless particle's momentum *as it reaches null infinity* ($\mathscr I^\pm$), used to build
  correlators of a putative 2D CFT living on the celestial sphere. The model has the spinor↔null-vector
  dictionary; it has not built the asymptotic (scri-level) structure on top of it.
- **It is not how the engine actually propagates the photon.** The photon's physical dispersion and
  polarization (F26/F69/F91) are computed directly in Cartesian lattice $\vec k$-space via FFT —
  `casim.numerics.fft` — never via a spinor-ratio coordinate. The only place a stereographic map
  appears elsewhere in the codebase is `_viz_spinor_color.py::make_bloch_legend`, and that projects
  the field's *internal* chirality/polarization state (an $(f,g)$ Weyl spinor) onto a Bloch-sphere
  color legend for visualization — a different spinor than F397's momentum-direction $\psi$, and not
  physics, just a plotting convenience. So the celestial-type object exists in the model as a proven
  algebraic identity (F397/T1) and as a notebook-level ancestor (pp.110-124), but it is not yet load-bearing
  machinery anywhere the engine actually runs.

**(2) Celestial holography, not AdS/CFT, is the structurally relevant comparison — but this is
presently an open direction with zero engagement in the model, not a result.**

- AdS/CFT is ruled out on the model's own terms, independent of the prompt's premise: F193 derives
  the CA-native ontic vacuum's contribution to the cosmological constant as **exactly zero**, and
  F241 treats the observed residual $\Omega_\Lambda\approx0.685$ as an undetermined $O(1)$ anthropic
  factor — never negative in either piece. A model whose vacuum energy is pinned at (or arbitrarily
  close to) zero has no AdS phase to hang a CFT dual on.
- Celestial holography targets exactly the regime the model's isolated-system sectors already live
  in: asymptotically flat spacetime around a compact source. F183 (Schwarzschild/Kerr exterior),
  F189 (GW150914 inspiral phasing), and F228 (the stable graviton–graviton geon) are all
  flat-asymptotic constructions on the F178 induced-Einstein-equation sector, and the model's own
  light cone there is the same lattice one used everywhere else ($c_\text{lat}=c_\text{grav}=1/\sqrt3$,
  F26/F180) — there is no separate "gravity light cone" to reconcile with a celestial null infinity.
- The model already has a holography result, but it answers a different question than celestial
  holography does. F190/F196 (Bekenstein–Hawking entropy $S=A/4$ from counting F107 horizon lattice
  cells, dilution exponent $p=2$ derived) is finite-region/area-law holography — a horizon's interior
  microstates vs. its boundary area, the Ryu–Takayanagi/entanglement family. Celestial holography is
  asymptotic/S-matrix holography — null-infinity scattering data organized as a 2D CFT. These are not
  competing descriptions of the same object; GR itself is understood to admit both simultaneously,
  so adopting celestial holography later would sit alongside F190/F196, not replace or contradict them.
- A direct search of the finding/claim corpus for BMS symmetry, null infinity, asymptotically-flat
  holography, or soft theorems returns **zero hits** outside the cross-check's own documents — this
  axis has not been touched. So the honest status is: the model has, by construction (Penrose's
  null-vector/spinor correspondence via F397), the *exact algebraic starting point* celestial
  holography also uses, and independently has no reason to prefer AdS/CFT (F193/F241) — but nothing
  in the model currently computes a BMS supertranslation, a soft theorem, or a celestial-CFT
  correlator. The comparison point is real; the program is not yet started.

**If this is pursued later**, the natural first concrete step is not a new formalism but reusing
existing machinery: take the model's own massless dispersion (F26/F69, the paired-spinor photon)
and F397's T1 map on an asymptotically flat background (e.g. the F183 Schwarzschild exterior or the
F228 geon), express outgoing lattice photon/graviton momenta via F397's $\zeta$, and check whether
their amplitudes satisfy the leading soft-photon/soft-graviton Ward identities that anchor celestial
holography — a falsifiable first test rather than a structural-resemblance claim, and the kind of
follow-up this correlation pass does not itself attempt.

## Status

Descriptive/comparative — no new quantitative claim tested against data, so no new finding number
or test record (same treatment as handoff item A.1). Recorded here for the record; the handoff item
is marked closed below.
