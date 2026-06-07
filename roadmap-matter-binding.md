# Roadmap — Dynamical Matter & Binding: electrons, u/d quarks → protons, neutrons, atoms

**Date:** 2026-06-03 - 00:35
**Status:** Plan only — no code written. Sequencing + module/test specs + exactness targets + risk flags.
**Scope:** Carries the model from a *structurally complete* first generation (every Tier-A row in `first-gen-completeness.md` §5.1 closed) to *dynamical, real-time, mass-measured* matter and its bound states.

---

## Where we actually are (the honest baseline)

The pieces below already exist, and the roadmap builds **only** on them:

- **Dynamical fermions** — `ca_dirac.py` propagates Weyl/Dirac wavepackets on the BCC lattice with exact `arccos` dispersion, F27 chiral mass, zitterbewegung. The electron and the u/d quarks each *already have a real-time propagator and the correct charges* (F27, F34, F40, F41, F42).
- **Colour + confinement** — `ca_gluon.py` (F43, dynamical SU(3), $f^{abc}$ self-coupling) and `ca_cooling.py`/`ca_confinement.py` (F70). Confinement is a **prediction** — but **only 2D-exact** (area law by deterministic Weyl-torus quadrature). 3+1D string tension is not yet established.
- **The proton** — `ca_baryon.py` (F71) is an **operator-level** colour-singlet $B=\varepsilon_{abc}u^au^bd^c$: right quantum numbers, Fermi statistics, energetic-binding argument. It is **not** a dynamical (real-time, non-dispersing, mass-measured) bound state. F71's own scope note names that as the next step.
- **Two-body bound-state machinery** — `test_F74_bound_state_binding.py` (F74) is a real relative-coordinate lattice solver (Koster–Slater secular root + dense diagonalisation, agree to $1.3\times10^{-15}$). It handles a **contact** well in 3D and produces $E_b(g)$ exactly. This is the engine to generalise.
- **Scale / units** — **uncalibrated.** F83 proves a single fermion mass fixes only the ray $a(m_\text{lat})$, not $a$ itself; CO-1 (SI units) is flagged as the blocker for *all* absolute numbers. Proton mass / QCD scale are explicitly Tier-B-open.

So the gap is not "build the particles" — it is **make the bound states dynamical, push confinement to 3D, add the residual nuclear force, add the QED bound state, and pin one scale** so the masses and binding energies come out in MeV.

---

## The seven phases (dependency-ordered)

```
P0 single-particle certification ─┬─> P1 3D confinement ──> P2 dynamical baryon (p, then n) ─┬─> P4 nuclei (deuteron)
                                  │                                                          │
                                  └─> P5 QED bound state (atoms) <── (electron, EM photon)   │
P3 pion / chiral pseudoscalar ───────────────────────────────────────────────────────────────┘ (force carrier for P4)
P6 scale & SI units  ── cross-cutting, gates every absolute number in P2–P5
```

---

### P0 — Certify the single particles as *dynamical* objects (electron, u, d)

**Goal.** Promote "we have a stepper" to "we have a measured, non-dispersing, correctly-charged real-time electron / up / down." This is mostly *certification* of existing code, not new physics — the foundation everything else rests on.

**Build.**
- `model-tests/test_P0_dynamical_fermions.py`: launch a localised Gaussian wavepacket for each of $e, u, d$; measure (a) group velocity $v_g=\partial\omega/\partial k$ vs the exact BCC dispersion, (b) norm conservation over $\ge10^3$ ticks, (c) zitterbewegung frequency $2mc^2$, (d) charge/$T_3$/$Y$ via the existing registries, (e) the quark as a **colour-triplet** wavepacket under `ca_strong`/`ca_gluon`.
- A small `ca_wavepacket.py` helper (coherent-state builder + observables) if the harness doesn't already expose one.

**Exactness target.** Dispersion/group-velocity to the FFT floor ($\sim10^{-13}$); charges exact (rational). 

**Risk.** Low. Watch the CLAUDE.md numpy/scipy chiral-transform caveat — verify any new spinor reductions against a hand-rolled reference.

---

### P1 — 3+1D confinement (the binding force, for real)

**Goal.** F70's area law is a deterministic 2D result. A physical proton lives in 3D, where the string tension must come from a **Monte-Carlo** ensemble and there is a genuine **deconfinement transition**. Without this, P2's binding potential is borrowed from a lower dimension.

**Build.**
- Extend `ca_cooling.py`/`ca_confinement.py` to 3D BCC SU(3): heat-bath / over-relaxation link updates, Wilson-loop and Polyakov-loop estimators, Creutz ratios.
- Measure $\sigma(\beta)$ and the static potential $V(R)=\sigma R + \mu - e/R$ (linear + Coulomb + constant); locate the deconfinement $\beta_c$.
- **Resource note (CLAUDE.md):** 3D MC will blow the 90 s sandbox. Ship `run_confinement_3d_mc.py` as a **user-run script** that dumps a Claude-readable JSON, mirroring the existing `run_confinement_mc.py`.

**Exactness target.** Tier-3 (statistical): string tension and the Coulomb coefficient to MC error bars; cross-check the strong-coupling expansion $\sigma\approx-\ln(\beta/18)$ at small $\beta$.

**Risk.** Medium. Autocorrelation / critical slowing near $\beta_c$; needs gradient-flow scale-setting (the F70 cooling driver already does the flow).

---

### P2 — The dynamical baryon: proton, then neutron

**Goal.** Replace F71's operator with a **real-time three-quark bound state** that does not disperse and has a **measured mass**. Then build the neutron ($udd$) and the $n$–$p$ splitting.

**Build.**
- Generalise the F74 two-body solver to **three bodies in Jacobi coordinates** ($\boldsymbol\rho,\boldsymbol\lambda$), reduced masses from the F27/F46 quark lattice masses, interacting through the **P1 confining + one-gluon-exchange** potential ($V=\sigma R - \tfrac{2\alpha_s}{3}\frac1R$ per pair, Casimir-scaled). New `ca_baryon_dynamics.py`.
- Solve the ground state two independent ways (secular root **and** dense diagonalisation, as F74 does) and demand agreement to machine precision; verify the wavepacket is **stationary / non-dispersing** in real time.
- **Neutron:** same solver with $uud\to udd$; the $n$–$p$ mass splitting $=$ (d–u quark-mass difference, F40 splitting ratios) $+$ EM self-energy (P5 machinery). Target sign and rough magnitude of $m_n-m_p=+1.29$ MeV (the neutron is heavier *despite* EM — the down–up mass gap must win; a real test of the F40 ratios).
- `model-tests/test_P2_baryon_bound_state.py`.

**Exactness target.** Solver-internal: machine precision (two methods agree). Physical proton mass: **Tier-B, gated on P6** — first as a ratio ($m_p/\sqrt\sigma$, the lattice-QCD nucleon-in-string-units number $\approx$ 3–4), then absolute once $\sigma$ is in MeV².

**Risk.** **High — this is the crux.** Two specific hazards, both already quantified in the model: (i) F74's "quantified near-no-go" — the model's *gauge* couplings bind far too weakly for deep binding; the proton's binding must come from **confinement (P1), not gluon exchange**, so P1 must be solid first. (ii) Constituent-quark vs current-quark mass: most of $m_p$ is glue/confinement energy, not $\sum m_q$ — the solver must source the bulk of the mass from the string, which is exactly what P1 provides.

---

### P3 — The pion (chiral pseudoscalar) — force carrier for nuclei  ✅ DONE 2026-06-06 (F103)

*Built: `ca-simulation/ca_meson.py` + `model-tests/test_P3_pion.py` (13/13 PASS). Pion delivered as the q̄q pseudoscalar Goldstone (chiral-limit m_π=0 exact; GMOR 0.39%; m_π²∝m₀ flat to 0.86%); σ chiral partner at 2m_c from the same single coupling; ρ contrast via KSRF; real-space relcoord bound state secular==dense to 1.3e-15. See F103.*


**Goal.** The residual nuclear force that binds nucleons is, at long range, **pion exchange**. The pion is the pseudoscalar Goldstone of chiral-symmetry breaking — the **spin-0 antisymmetric partner** of the F69 photon pairing, and the chiral partner already named in F73/F74. NJL (F77) *already* reproduces $m_\pi, f_\pi, \langle\bar qq\rangle$ self-consistently, so the calibration exists; this phase makes the pion a **dynamical** $q\bar q$ state.

**Build.**
- `ca_meson.py`: $q\bar q$ relative-coordinate bound state (reuse the F74 engine, attractive channel from P1 + NJL contact F77). Extract $m_\pi$ (light, near-Goldstone) and the $\rho$ for contrast.
- Verify the **Gell-Mann–Oakes–Renner** relation $m_\pi^2 f_\pi^2 = -m_q\langle\bar qq\rangle$ against the F77 numbers.
- `model-tests/test_P3_pion.py`.

**Exactness target.** GMOR to the NJL solver's precision (F77 is machine-precision-internal); $m_\pi/f_\pi$ to the F77-calibrated values.

**Risk.** Medium. The Goldstone nature (light $m_\pi$) is the sharp check — if the pseudoscalar doesn't come out anomalously light, the chiral-breaking bookkeeping (F73/F77) is wrong.

---

### P4 — Nuclei: bind a proton + neutron → deuteron  ✅ DONE 2026-06-06 (F104, full ³S₁–³D₁ tensor)

*Built: `ca-simulation/ca_nuclear.py` + `model-tests/test_P4_deuteron.py` (11/11 PASS). Full coupled-channel OPEP with the pion tensor force: tensor ⟨S₁₂⟩ matrix = Rarita-Schwinger [[0,2√2],[2√2,−2]] to 9.8e-15; the deuteron binds ONLY via the tensor coupling (central-only unbound); single shallow J^P=1⁺ I=0 state, P_D≈7%, tuned to E_b=2.224 MeV / κ=0.2316 fm⁻¹. m_π/f_π from P3; g_A + short-range core are the flagged external/phenomenological inputs (the core is the roadmap-anticipated missing ingredient). See F104.*


**Goal.** The first **nucleus**. Residual strong force from P3 pion exchange (one-pion-exchange Yukawa potential $\propto e^{-m_\pi r}/r$), bind $p+n\to{}^2$H, measure the binding energy (physical target $\approx 2.2$ MeV — shallow, just-bound).

**Build.**
- `ca_nuclear.py`: nucleon–nucleon effective potential (OPEP tail from P3 + a short-range core); two-body solver (F74 engine again, now $1/r\cdot e^{-m_\pi r}$ channel) for the deuteron ground state; check it is **just barely bound** (no excited state), $J^\pi=1^+$, isospin-0.
- `model-tests/test_P4_deuteron.py`.

**Exactness target.** Tier-B. Realistically a **ratio / order-of-magnitude** result first (binding $\ll$ nucleon mass), tightened only after P6.

**Risk.** **Highest novelty / lowest guarantee.** The model has *no* residual nuclear force today — it is an emergent, fine-tuned, shallow effect even in real QCD. This is the phase most likely to expose a missing ingredient (short-range repulsive core, tensor force from pion $D$-wave). Treat a *bound, shallow, spin-1, isospin-0* deuteron as success; precise 2.2 MeV is a stretch goal.

---

### P5 — Atoms: electron bound to a nucleus by EM (hydrogen first)

**Goal.** The **atom** — an electron (P0) bound to a proton (P2) by the electromagnetic photon (F69 paired-spinor photon, the U(1) channel). Hydrogen ground state and spectrum.

**Build.**
- `ca_atom.py`: the electron Dirac field in the Coulomb field of a (first static, then dynamical-charge) proton — the **attractive $1/r$** analogue of the F74 contact solver. Extract the Bohr/Rydberg ground-state energy $-13.6$ eV and the $1/n^2$ Rydberg series; then **fine structure** from the Dirac (not Schrödinger) kinetic step the model already has.
- Two-body QED check first: **positronium** (electron + positron, both dynamical) as the clean two-body validation before the heavy proton.
- Multi-electron extension (helium) needs the Pauli antisymmetriser already validated in F71 (BS7) — flag as a stretch.
- `model-tests/test_P5_hydrogen.py`.

**Exactness target.** Non-relativistic spectrum to the lattice-dispersion floor; fine-structure $\propto\alpha^2$ as a **prediction** of the Dirac step (ties to the open QFT-1 $g\!-\!2$ / QFT-4 Lamb-shift items in `first-gen-completeness.md` §5.4).

**Risk.** Medium. The Coulomb $1/r$ on a lattice has known short-distance regularisation issues; the bound-state energy is sensitive to the lattice spacing $a$ (so P5's absolute numbers also lean on P6). Positronium-first de-risks this.

---

### P6 — Scale & SI units (cross-cutting; gates every absolute MeV)

**Goal.** Turn ratios into physical masses/energies. **Everything absolute in P2–P5 depends on this.**

**Build / decide.**
- Resolve **CO-1** (`si-units-options.md`) — pick the second anchor F83 proved is required (mass alone fixes only the ray $a(m_\text{lat})$). Candidates: the F59/F61 induced-gravity cell $a\approx3.81\,\ell_P$ (Option C), or a measured mass + the lattice lightcone $a/\tau=c\sqrt d$ (Option D).
- Set the **QCD scale** by matching one hadronic quantity (e.g. $\sqrt\sigma$ from P1, or $f_\pi$ from F77) to its physical value, then *predict* the rest (proton, neutron, deuteron, hydrogen) and compare to data.

**Exactness target.** This is the certification ledger — each predicted physical number gets an `exactness-inventory.md` row with its measured counterpart.

**Risk.** Conceptual, not numerical: one wrong anchor choice rescales every downstream number. Do P6 *before* publishing any absolute mass, *after* the ratios in P2–P5 are solid.

---

## Suggested execution order (and why)

1. **P0** — cheap, unblocks confidence in everything (certify the particles).
2. **P1** — the binding force; **P2 cannot give a real proton mass without it.** Heaviest compute → user-run script.
3. **P3** in parallel with P1/P2 — independent (NJL F77 already calibrated); needed before P4.
4. **P2** — the dynamical proton + neutron; the headline result.
5. **P4** — deuteron; highest risk, attempt only after P2+P3.
6. **P5** — atoms; independent of the QCD chain (needs only P0 + EM), can run alongside P2.
7. **P6** — fold in continuously; *required* before any absolute mass/binding claim leaves the lab.

## What each phase would add to the ledger

| Phase | New module(s) | New test suite | New finding(s) | Headline claim |
|---|---|---|---|---|
| P0 | `ca_wavepacket.py` | `test_P0_dynamical_fermions.py` | F-dyn-fermions | $e,u,d$ as measured non-dispersing wavepackets |
| P1 | 3D ext. of `ca_cooling`/`ca_confinement` | `test_P1_confinement_3d.py` (+ user MC script) | F-3D-confinement | 3+1D string tension + deconfinement $\beta_c$ |
| P2 | `ca_baryon_dynamics.py` | `test_P2_baryon_bound_state.py` | F-dynamical-proton, F-neutron | real-time proton/neutron, $m_p/\sqrt\sigma$, $n$–$p$ sign |
| P3 | `ca_meson.py` | `test_P3_pion.py` | F-pion-goldstone | dynamical pion, GMOR vs F77 |
| P4 | `ca_nuclear.py` | `test_P4_deuteron.py` | F-deuteron | first bound nucleus (shallow, $1^+$, $I=0$) |
| P5 | `ca_atom.py` | `test_P5_hydrogen.py` | F-hydrogen, F-positronium | bound atom, Rydberg series, fine structure |
| P6 | — (`si-units-options.md`) | inventory rows | F-scale-fixed | absolute MeV for all of the above |

---

## The two things most likely to break

1. **Proton mass is confinement energy, not constituent mass (P1→P2).** If 3D confinement (P1) doesn't produce a robust linear potential, the dynamical baryon (P2) will sit near $\sum m_q$ — far too light. P1 is therefore the true critical path, not P2. F74 already warns the gauge couplings bind too weakly; the string must do the work.
2. **The residual nuclear force may not be there yet (P4).** Binding nucleons into nuclei needs an emergent OPEP tail *and* a short-range core. The model has neither today. P4 is the phase most likely to reveal a genuinely missing ingredient rather than a calibration gap — and that would itself be a finding.

---

*Cross-references: F70 (2D confinement), F71 (operator proton), F73/F74 (bound-state kinematics + two-body solver), F77 (NJL $m_\pi/f_\pi/\langle\bar qq\rangle$), F40/F42 (quark mass + Y), F69 (EM photon), F83 (lattice spacing), `first-gen-completeness.md` §5.3–5.4 (open Tier-B / QFT items), `si-units-options.md` (CO-1).*
