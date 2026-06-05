# F102 — EM and SU(3) back-action on the particle layer (roadmap P2)

**Date:** 2026-06-05 - 19:25
**Status:** Confirmed — 8/8 P2 tests PASS; 6 gate residuals exact / machine precision
**Modules:** `ca-simulation/ca_minimal_coupling.py` (new); `src/casim/particles/channel.py` (wiring promoted source-only → coupled)
**Tests:** `tests/test_particle_layer.py` (P2 block, tests `test_P2_1` … `test_P2_8`)
**Results:** `test-results/F102_particle_backaction_P2.json`
**Cross-refs:** F27 (complex mass / chiral SU(2), "static gauge angle unobservable"), F31/F34 (W_μ covariant hopping + fermion vertex — the audited SU(2) rotate-then-step), F40/FG-3 (quark electroweak wiring + Ward-identity standard), F41/F42 (hypercharge Stueckelberg wrap), F43 (SU(3) colour sector), F64 (gravity dielectric / Poisson solver), F68 (paired-photon U(1) minimal coupling), F87 (charge→field source coupling)

---

## Summary

Phase P2 of [roadmap-particle-layer.md](../roadmap-particle-layer.md) promotes the
particle layer's **EM** and **strong** couplings from *source-only* (P1: the
particle drives the field but the field does not act back) to fully **two-way
coupled**. The back-action is implemented with two architectures already
audited elsewhere in the model — **nothing new is invented**, the constructions
are ported to the 3D BCC walk and verified at the F40/FG-3 Ward-identity level:

1. **U(1) Stueckelberg-form wrap** (the F41/F42 `kinetic_half_step_chi_u1y`
   architecture) — the electromagnetic / hypercharge minimal coupling. Gauge
   covariance is **exact** (6.5×10⁻¹⁷), the static angle is force-free (F27
   "pure gauge is unobservable"), and a *time-dependent* angle reproduces the
   electrostatic force as exact one-bin-per-tick Bloch acceleration.

2. **SU(3) site-local rotate-then-step** (the audited SU(2)
   `ca_wmu.covariant_weyl_step_3d_bcc` pattern) — the strong minimal coupling.
   The **global SU(3) Ward identity is exact** (3.1×10⁻¹⁶), matching the status
   of the audited W coupling (F34) and the FG-3 quark-electroweak gate.

A **Coulomb sector** is added to the sourced-photon channel: the charge density
ρ feeds the audited open-boundary Poisson solver (F64) to accumulate the A₀
Wilson-line angle α(x) that the wrap consumes — closing the field→particle loop
for electrostatics. The F27/F46 rest-mass step (P2c) is wired for **lepton
singlets** via the exact `dirac_step_3d_bcc_splitstep`; massive doublets and
quarks remain a later phase.

---

## Construction

### 1. U(1) wrap (`u1_wrap_weyl_step_3d_bcc`, `u1_wrap_dirac_step_3d_bcc`)

For a Weyl spinor ψ = (f, g) of charge q in a U(1) angle field α(x):

$$\tilde\psi(x) = e^{-iq\alpha(x)}\psi(x)\quad[\text{gauge-fix}],\qquad
\tilde\psi' = S_\text{free}[\tilde\psi]\quad[\text{exact unitary BCC step}],\qquad
\psi'(x) = e^{+iq\alpha(x)}\tilde\psi'(x)\quad[\text{restore frame}].$$

The vector charge q phases both chiralities identically, so the wrap commutes
with the F27 mass mixing — the same construction wraps the exact massive
`dirac_step_3d_bcc_splitstep` unchanged.

**Covariance (exact).** For any β(x):
$$S[\alpha+\beta]\!\left(e^{iq\beta}\psi\right) = e^{iq\beta}\,S[\alpha](\psi),$$
verified to **6.5×10⁻¹⁷** — the 3D-BCC port of the F41/F42 statement that a
static gauge angle is physically unobservable.

**Force law (exact).** A *time-dependent* angle α(x,t)=Σφ(x)dt inserts the
relative phase e^{−iqφ dt} between consecutive kinetic steps — the
electrostatic force. For an integer-charge uniform gradient
α_n(x)=n·(2π/L)·x (single-valued on the torus), each tick shifts every
momentum mode by exactly one k-bin in the −q∇α direction (Bloch acceleration);
the rolled spectrum matches to **1.0×10⁻¹⁵**, sign included.

### 2. SU(3) rotate-then-step (`su3_rotate_weyl_step_3d_bcc`)

For a colour triplet q = (q_r, q_g, q_b) in an octet potential A^a(x):

$$\tilde q(x) = V(x)\,q(x),\quad V(x)=\exp\!\big(i\,\varepsilon\,A^a(x)\,T^a\big)\in\mathrm{SU}(3),
\qquad q'_c = S_\text{free}[\tilde q_c]\ \text{per colour }c,$$

using the audited `ca_gluon._su3_expmap_field` and the colour-blind kinetic
step. This is the SU(2) `covariant_weyl_step_3d_bcc` architecture with the
Gell-Mann generators in place of the Pauli ones.

**Global Ward identity (exact).** For constant V ∈ SU(3):
$$V\cdot S_A(q) = S_{VAV^\dagger}(V q),$$
with the potential transforming in the adjoint
A^aT^a → V(A^aT^a)V† (re-projected exactly via A'^a = 2 tr(T^aH'),
tr(T^aT^b)=δ_ab/2). Verified to **3.1×10⁻¹⁶**. The local Ward identity is O(a),
as for every improved lattice-fermion action — identical status to the audited
W coupling (F34/FG-3).

### 3. Coulomb sector (`PhotonSourcedChannel`)

The sourced-photon channel now also accumulates the A₀ Wilson line:
φ_em = −φ_Poisson(ρ) from the audited open-boundary Poisson solver
(`casim.gravity.solve_poisson_3d_open`, the F64 kernel), and α += φ_em·dt each
tick. The sign convention φ_em = −φ_Poisson(ρ) places a positive charge in
φ_em > 0 so like charges repel under the wrap phase e^{−iqφ dt}. Quark
ParticleChannels consume the gluon potential A (accumulated as A += E, mirroring
the audited `w_sourced` channel) as the SU(3) rotation above.

---

## Gate results (`test-results/F102_particle_backaction_P2.json`)

| Check | Quantity | Residual | Tier |
|---|---|---|---|
| P2-1 | U(1) wrap, α≡0, bit-identical to free step | $0.0$ | 1 |
| P2-2 | **U(1) exact gauge covariance** (any β) | $6.5\times10^{-17}$ | machine ε |
| P2-3 | U(1) unitarity, 50 dynamic-α ticks | $7.1\times10^{-15}$ | machine ε |
| P2-4 | Bloch-acceleration force law, both signs of q | $1.0\times10^{-15}$ | machine ε |
| P2-5 | SU(3) wrap, A≡0, bit-identical + unitarity (20 ticks) | $0.0$ / $2.4\times10^{-15}$ | 1 / machine ε |
| P2-6 | **SU(3) global Ward identity** (Haar V) | $3.1\times10^{-16}$ | machine ε |
| P2-7 | Massive lepton singlet = exact BCC Dirac step, bit-identical | $0.0$ | 1 |
| P2-8 | Two-way end-to-end (e⁻ + Coulomb photon + u-quark + gluon) norms conserved | $<10^{-10}$ | machine ε |

(Supporting: the Haar V used in P2-6 is unitary to 4.4×10⁻¹⁶ and det V = 1 to
4.5×10⁻¹⁶, so the test exercises a genuine SU(3) element.)

**Gate met.** The roadmap P2 gate is "Ward identities at the F40/FG-3 level."
The U(1) gauge-covariance identity and the SU(3) global Ward identity both hold
at machine precision; the local Ward identity is O(a), exactly as in F40/FG-3.

---

## What this adds to the model

1. **Closed field↔particle loops for EM and strong.** A charged particle now
   both sources the photon/gluon field *and* feels its back-action through the
   same audited covariant step — the modular promise of the particle layer, now
   with three of the four forces two-way coupled (weak was already coupled in
   P1; gravity stays background pending a ψ→K sourcing derivation).

2. **Electrostatics from the Wilson line.** The Coulomb force is not bolted on:
   it is the time-derivative of the A₀ angle the wrap already consumes, fed by
   the same F64 Poisson solver used for gravity — one solver, two forces.

3. **No new physics.** Every propagation, source, and rotation call is an
   existing audited kernel; P2 is the wiring + the covariance/Ward audit. The
   constructions are the F41/F42 (U(1)) and F31/F34 (SU(2)→SU(3)) architectures
   ported to 3D BCC.

---

## Scope / open items

- **Local** (not just global) Ward identity is O(a) — the standard lattice
  status; an exactly site-local non-Abelian conserved current would need a
  Wilson-line-improved current operator (not required by the P2 gate).
- Massive **doublets and quarks** (F27/F46 mass with isospin/colour structure)
  are deferred — P2c wires the exact Dirac step for lepton singlets only.
- Dynamical **matter-sourced gravity** (ψ → K) is still research-gated; gravity
  remains a background F64 dielectric in the readouts.
- The Coulomb α uses the open-boundary Poisson solver on the cubic FFT grid that
  the `photon_sourced`/`charge_photon` channels already run on; mixed-topology
  scenarios stay refused by `LatticeSpec`.
