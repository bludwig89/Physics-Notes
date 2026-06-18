# Roadmap — Unified real-space integration: one lattice carrying a confined proton **and** an EM-bound electron

`2026-06-11 - 18:53`

**Purpose.** The matter-binding roadmap is complete *in pieces* — F122 (proton/neutron), F123 (SI scale), F125 (hydrogen) — but each is a **reduced spectral solve** (explicitly-correlated Gaussians for the baryon; a radial finite-difference Coulomb eigenproblem for the atom), not a single real-space lattice carrying all the objects at once. This roadmap takes the project from "the pieces all score against data" to the stated project goal: **a universe in a bottle** — one real-space CASIM lattice on which quarks, gluon, photon and electron co-evolve, a proton stays confined, and an electron is held in a bound cloud around it.

This is a planning document, hand-maintained, sitting alongside `next-steps.md`, `roadmap-matter-binding.md`, and `roadmap-scale-to-real-space.md` (which it depends on for the coarse-graining substitution).

---

## 0. The honest baseline — what already exists

The CASIM particle layer (`src/casim/particles/`, `roadmap-particle-layer.md`) and the engine's Tier-2 coupled channels (`src/casim/engine/coupled.py`) already implement **every coupling loop** needed, each individually audited:

| loop | source channel | field channel | back-reaction on matter | status |
|---|---|---|---|---|
| colour confinement | quark `ParticleChannel` publishes `J_colour` | `gluon_sourced` (`ca_gluon.gluon_sourced_step_bcc`, even F91) accumulates octet `A` | quark reads `A` via `su3_rotate_weyl_step_3d_bcc` | loops closed, tested |
| EM / Coulomb | particle publishes `J_em`, `rho_em` | `photon_sourced` (even-law `ca_photon_pair`, + open-Poisson `α(x)` Wilson angle) | particle reads `α` via `u1_wrap_*_step` | loops closed, tested |
| weak | doublet isospin current | `w_sourced` (`ca_wmu`, chiral) | `covariant_weyl_step` | E2E B1, tested |
| gravity (F64) | particle density | `gravity_dielectric` (`poisson_open`, `K=e^{2u}`) | rest-leg lapse mix `√A·m` | tested |

Two pilot scenarios already stack particles on one lattice: `particles_first_gen.yaml` (free electron + free u-quark + photon + gluon + gravity) and `proton_composite.yaml` (a stacked `uud` colour-singlet — but propagated by the **free** Weyl kernel, not held together by the gluon field). The block-spin RG `R_b` is a first-class engine op (F133, `Simulation.block_spin`), with `c_lat`, the dielectric lock and the F91 propagator classes proven invariant (F130).

**So the gap is not missing channels.** It is four specific things:

1. **No scenario runs the full chain together** — a confined `uud` proton *and* a photon sourced by its net charge *and* an electron bound by that photon, all on one lattice with every loop live.
2. **No demonstration that the loops actually bind in real time.** F122/F125 prove the *spectra* exist; they do not show that the gluon-sourced field holds three free-propagating quark wavepackets from dispersing, or that the proton's Coulomb `α(x)` holds an electron wavepacket in a stationary cloud. On the lattice, an uncoupled wavepacket simply disperses — binding has to be *exhibited*, not assumed.
3. **No unification readout** — an observer that measures the emergent diagnostics (proton RMS radius bounded vs free control; electron RMS radius about the proton centroid; system net charge → 0; loop-liveness).
4. **The scale-separation wall** (§2) — the physical reason a single *literal* lattice cannot hold both a 10⁻¹⁵ m proton and a 10⁻¹⁰ m orbit, and the multigrid substitution that gets around it.

---

## 1. Design principle — exhibit the mechanism, gate the magnitude

Follow the established project discipline (F122 §5, F125 §6): **structure is the prediction; absolute scale is P6/scale-gated.** A real-space integration milestone is "passed" when the *emergent binding mechanism* is exhibited and its qualitative signatures are correct (non-dispersing bound object, correct sign of the force, correct neutrality, the right loop carrying the binding). Absolute fm / eV numbers remain gated on P6 (F123) and on the coarse-graining scale factor (F133), exactly as in the reduced solves.

This keeps the integration honest about the two things the roadmap-scale-to-real-space.md table makes unavoidable: brute-force real space is ~45 decades off, and the proton and the Bohr orbit differ in size by ~5 decades.

---

## 2. The scale-separation wall (the deep constraint)

| object | size | cells across at canonical `a=1.07×10⁻³⁴ m` |
|---|---|---|
| proton | 1.7×10⁻¹⁵ m | ~1.6×10¹⁹ |
| Bohr orbit | 5.3×10⁻¹¹ m | ~5×10²³ |
| **ratio (orbit / proton)** | **~3×10⁴** | — |

Even ignoring the absolute cell count, **a lattice that resolves the proton's internal structure and the electron's orbit simultaneously needs ~10⁴–10⁵ cells across in each dimension** (≥10¹² cells in 3-D) — over the CASIM GUI ceiling and far over the sandbox. This is *intrinsic*, not a compute artifact: the strong and EM binding scales are physically separated.

**Consequence for the build.** A single literal lattice carrying the proton's quark structure *and* a true-scale electron orbit is not the first deliverable; it is U4, and it requires the block-spin multigrid (treat the confined proton as a coarse-grained point charge for the atomic-scale lattice). The earlier milestones (U0–U3) deliberately work at a **rescaled / compressed** scale where both objects fit in one tractable lattice — proving the mechanism co-exists and the loops are mutually consistent — with the scale separation restored only at U4.

---

## 3. Phases

```
U0 full coupled scenario + unification readout  ──►  U1 real-space confined proton
                                                          │
U2 real-space EM-bound electron ──────────────────────────┤
                                                          ▼
                                          U3 neutral hydrogen system (p + e, Q=0)
                                                          │
                                                          ▼
                                  U4 scale separation via block-spin multigrid (the goal)
```

### U0 — Wire the full chain on one lattice + a unification readout  *(buildable now)*

**Goal.** One scenario, every loop live: three colour quark `ParticleChannel`s (`uud`) + `gluon_sourced` (sources = the three quarks) + `photon_sourced` (sources = quarks **and** electron, with the Coulomb `α` sector on) + an electron `ParticleChannel` (`em: photon_field`) + a `gravity_dielectric` background. Add a `unification_readout` observer reporting, every N ticks:

- per-object centroid, norm (conservation), RMS radius;
- the three-quark cluster RMS radius (proton size proxy);
- the electron RMS radius **about the proton centroid** (orbit proxy);
- the system net EM charge `Σ q·‖ψ‖²` (neutrality proxy → 0 for `uud`+`e`);
- loop-liveness: `‖J_colour‖`, `‖gluon A‖`, `‖J_em‖`, `‖photon α‖` are non-zero (the currents are actually sourcing the fields and the fields are actually present).

**Exactness target.** Norm conservation per channel to the spectral floor (the kernels are unitary); the readout is diagnostic, not a precision claim.

**Risk.** Low — it is assembly of audited channels. Watch the CLAUDE.md chiral caveat for any new spinor reductions in the readout (use `density_field`, which is already real).

### U1 — Real-space confined proton  ✅ DONE 2026-06-11 (F135)

*Built: the F86/F70 confining string as a Lorentz-**scalar** position-dependent Dirac mass m_eff(x)=m+σ|x−R_cm| (MIT bag = F86 ε_c→0), via the new `dirac_step_3d_bcc_varm_splitstep` (uniform reduces to constant-m bit-for-bit; unitary) wired as a `confine` block on the `ParticleChannel`. Three massive Dirac constituents (Y-string toward the singlet COM) form a non-dispersing bound state — cluster RMS plateaus at ≈3.7 vs free dispersal to ~7–8. Key result: scalar confinement binds; a **vector** (phase-kick) potential of the same σ Klein-tunnels and does NOT bind (outcome (b) below, resolved). Open: colour×Dirac quark wiring + the live flux-tube field (vs the mean-field string) + U4 scale. See F135.*


**Goal.** Show the gluon-sourced field **binds** the three quarks: the cluster RMS radius stays bounded over a long run, vs a free-propagation control where it grows ballistically. This is the real-time analogue of F122's "purely discrete spectrum ⇒ non-dispersing."

**Honest hazard (already quantified in the model).** F74's "quantified near-no-go": the *gauge* (one-gluon-exchange) coupling binds far too weakly; in real QCD the proton is held by the **confining string**, not perturbative exchange. The linearised `gluon_sourced_step` is a one-gluon-exchange-level kernel — it may **not** confine on its own at sandbox amplitudes. Two honest outcomes, both findings:
- (a) it produces a bounded, slowed cluster → real-space confinement signature, document it;
- (b) it does not bind → quantify the dispersion rate vs free control, and record that the linearised sourced-gluon channel lacks the non-perturbative string (the F86/F94/F110 confinement sector, not the F43 linear kernel, is what's needed) — itself the expected result and a clean statement of the remaining work.

**Exactness target.** Tier-3 (qualitative/statistical): bounded-vs-ballistic RMS radius.

### U2 — Real-space EM-bound electron  *(attempt now)*

**Goal.** With a proton (or, first, a **static** `rho_em` point charge to de-risk) sourcing `photon_sourced`'s Coulomb `α(x)`, show the electron `ParticleChannel` is held in a bounded cloud vs a free control. The attractive sign is already wired (`φ_em = −φ_Poisson(ρ)`, like-charges repel ⇒ opposite-charges attract). Positronium-style two-body de-risk mirrors F125 §4.

**Exactness target.** Tier-3: bounded-vs-ballistic electron RMS radius about the charge; correct attractive sign.

**Risk.** Medium — the lattice Coulomb `1/r` short-distance regularisation (F125 §6) and the fact that, at honest scale, the Bohr orbit doesn't fit. Run at a **compressed** scale (large effective `α`, heavy electron) so the bound cloud fits the lattice; the magnitude is scale-gated, the *binding* is the deliverable.

### U3 Part 1 — scalar string on SU(3) colour quarks  ✅ DONE 2026-06-11 (F136)

*Built: `ColourDiracQuarkChannel` (`quark_dirac`) — a massive colour-triplet Dirac quark carrying the SU(3) gluon loop + the F135 scalar string + EM. A real `uud` proton (Q=+1) is confined in real space (cluster RMS ~3.7 vs free ~7), gluon loop live (J_colour→A). See F136.*

### U3 Part 2 — live colour-dielectric flux-tube field  ✅ DONE 2026-06-11 (F137)

*Built: `ColourBagChannel` (`colour_bag`) + `confine.field` — the posited geometric string replaced by a live F86 dielectric bag: the condensate f² melts where the quark colour charge sits (ρ=Σ‖J_colour‖, smeared by λ), the bag wall S=M_bag·f² confines the quarks. The proton digs its own bag (RMS ~2.95 vs free ~8). Static two-charge diagnostic: a connected flux tube with ~linear E(R) over R≲2λ (F86 dual-superconductor signature; exact σ=2πv²n is F86's BPS asymptote). Open: self-consistent dual-GL back-reaction vs the mean smear. See F137.*

### U3 — The neutral hydrogen system

**Goal.** Put U1's confined proton and U2's bound electron in one run and confirm: system net charge → 0, electron cloud tracks the proton centroid, both norms conserved, total field energy bounded. The first *composite-neutral atom* exhibited as a real-space lattice object (at compressed scale).

### U4 — Restore the scale separation via the block-spin multigrid  *(the goal; depends on F133 + Phase-1 RG)*

**Goal.** Defeat §2's wall. The electron orbit lives on an atomic-scale lattice; the proton — 10⁴–10⁵× smaller — enters that lattice as a **coarse-grained point source** (`rho_em` from a block-spin-reduced confined proton, F133 `R_b`). Conversely the proton's internal confinement runs on its own fine patch. This is a two-grid / adaptive-resolution CA step: the F133 `blockspin:` engine op nests the scales. Deliverable: a hydrogen atom whose orbit is at the right `a₀/a` ratio relative to a proton that is itself a faithfully coarse-grained confined object — the literal "universe in a bottle" within the renormalised-cell substitution that `roadmap-scale-to-real-space.md` Phase 1 legitimises.

**Risk.** High / research-open. Requires the Phase-1 RG (F130–F133) to be shown to commute with *both* binding sectors simultaneously, and a working two-grid coupling in the engine. This is the genuine frontier.

---

## 4. What each phase adds to the ledger

| phase | new artifact(s) | headline |
|---|---|---|
| U0 | `scenarios/unified_hydrogen.yaml`, `unification_readout` observer, `test_F134_*` | full chain live on one lattice; loops sourcing; norms conserved |
| U1 | run + (user-run script if needed) | real-space proton: bounded vs free control (or quantified gap → string sector needed) |
| U2 | run / static-charge de-risk | real-space electron bound by proton Coulomb `α`; attractive sign |
| U3 | combined scenario | neutral (Q=0) hydrogen as a co-evolving real-space object (compressed scale) |
| U4 | two-grid block-spin coupling | scale-separated atom — the project goal |

---

## 5. The two things most likely to break

1. **The linearised sourced-gluon channel does not confine (U1).** Confinement in this model is the F86 colour-dielectric / F94 lattice-gauge MC / F110 link-Hamiltonian non-perturbative string, *not* the F43 linear `gluon_sourced` kernel. If U1 shows dispersion, the fix is to drive the quark dynamics with the confinement sector (a `gauge_mc` / link-Hamiltonian-backed binding potential) rather than perturbative gluon exchange — exactly the F122 lesson, now in real space.
2. **Scale separation makes U3 a *compressed* atom, not a physical one (U4 is the real prize).** U0–U3 deliberately trade physical scale for tractability. The honest physical atom is U4 and is gated on the block-spin multigrid.

---

## 6. Status review 2026-06-15 - 01:50 — no U-phase flips; confinement basis firmer

Reviewed against findings F139–F155 and the production SU(3) static-potential runs
(`test-results/su3_static_potential_b{9,12}.json`). **No U-phase changes state**, but
the confinement substrate that U1/U3 stand on is now firmer:

- **U0** (full coupled scenario + `unification_readout`) — **still OPEN / un-started.**
  No `scenarios/unified_hydrogen.yaml` or `unification_readout` observer has landed.
- **U1** (real-space confined proton) — DONE (F135), unchanged; the F86 scalar-bag
  σ it uses is now **measured, not posited** (F146) and **confirmed at a second β**
  (b9: $\sigma a^2{=}0.264$; b12: $0.132$; right scaling trend) — so U1's installed
  confinement scale is now emergent and two-β-validated, but U1 itself was already
  marked done.
- **U2** (real-space EM-bound electron) — **still OPEN.** The F148 assembler uses the
  *spectral* F125 Coulomb solver, not a real-time lattice-bound electron wavepacket;
  the real-space binding demonstration is still un-built.
- **U3 Part 1/2** (SU(3) colour quarks / live dielectric bag) — DONE (F136/F137),
  unchanged. **U3 full** (neutral hydrogen as one co-evolving real-space object) —
  still OPEN.
- **U4** (block-spin multigrid scale separation) — **still OPEN / research-frontier.**
  F146 §4a closed the *σ-side* lattice-spacing carry (scale-invariant
  $R_\text{conf}\sqrt\sigma=1.11$), which de-risks the gauge↔Dirac match, but the
  actual two-grid engine coupling is unbuilt.

So this roadmap has **no item that closes** from the F139–F155 + production-run work;
the gains land in `roadmap-scale-to-real-space.md` Phase 3 (emergent σ, the IR-coupling
residual) instead. The standing pacing item here remains **U0** (buildable now) →
U2 → U3 → U4.

---

*Cross-references: F122 (spectral proton/neutron), F123 (SI scale / nucleon 3m_c), F125 (spectral hydrogen + fine structure), F130–F133 (block-spin RG + CASIM kernel), F43/F86/F94/F110 (gluon / confinement sectors), F64/F106 (dielectric gravity), F67/F69 (even-law photon), F146 (emergent two-β σ), `roadmap-matter-binding.md`, `roadmap-scale-to-real-space.md`, `roadmap-particle-layer.md`, `src/casim/particles/channel.py`, `src/casim/engine/coupled.py`.*

---

## 7. Status update 2026-06-17 - 20:23 — U2 + U3 CLOSED

Executed U0→U2→U3 (with Phase 2(iii) of `roadmap-scale-to-real-space.md` in
between). State changes:

- **U0** — confirmed already done (test_F134 3/3); no change.
- **U2 (real-space EM-bound electron) — ✅ DONE (F156, 4/4).** New `nr_electron`
  channel: a non-relativistic Schrödinger orbital (exactly-unitary split-step),
  relaxed into the Coulomb ground state. Bound RMS flat 2.51 over 400 ticks vs
  free dispersal to 18.3. This is the correct description (atomic e⁻ is
  non-relativistic); the relativistic vector-Coulomb path provably fails on a
  tractable lattice (pure-gauge increment / Zα→1 collapse / F135 null), and the
  fine structure stays with F125's spectral solve.
- **U3 (neutral hydrogen as one object) — ✅ DONE (F158, 6/6).** Confined `uud`
  proton (scalar Y-string) + F156 bound electron on one L=24 lattice: net
  charge 0 exactly, all four loops live, proton confined (RMS plateaus ≈3.3),
  electron bound and concentric (cloud ≈4 > nucleus), norms ~1e-13.
- **U1** — unchanged (done, F135).
- **U4 (block-spin multigrid scale separation) — still OPEN / research
  frontier.** The remaining item; everything U0–U3 is now closed.

The standing pacing item is now **U4** alone.

---

## 8. Status update 2026-06-17 - 20:23 — U4 first build (F159)

**U4 (block-spin multigrid scale separation) — FIRST BUILD LANDED (F159, 4/4).**
`ca-simulation/ca_multigrid.py`: the proton runs on a fine patch and enters the
coarse atomic lattice as an R_b coarse-grained point charge; b carries the scale
separation. R_b is charge-faithful (exact) and commutes with the orbit binding
(point-vs-resolved gap→0; E0 invariant under coarse spacing, spread 0.0027). The
two-grid atom at b=63000 represents a0/r_p = 4.28e4 (4.63 decades ≈ physical H)
on ~24/48-cell lattices. Production runner `run_u4_multigrid.py` does the
accurate large-L sweep. **Remaining U4:** the LIVE two-grid co-evolution as a
single CASIM engine run (the engine assumes one lattice/run) — the physics is
proven faithful; the engine nesting is the next build. With this, U0–U4 all have
working builds; U4's engine-level nesting is the one open extension.

---

## 9. Status update 2026-06-17 - 20:23 — U4 LIVE closed (F160); U0–U4 complete

**U4 LIVE two-grid engine run — DONE (F160, 5/5).** The one remaining U4 item —
both grids co-evolving in a single `Simulation.run()` — landed as the
`two_grid_atom` channel: a fine confined uud proton + a coarse electron, bridged
by a per-tick R_b charge reduction. Net charge 0 (machine), norms ~3e-14,
electron orbit resolved+stable (coarse RMS≈6.2), proton confined, represented
ratio ≈6e4 (≈4.8 decades ≈ physical H) — LIVE on tractable lattices
(`unified_hydrogen_multigrid.yaml`). The engine's one-lattice/run assumption is
sidestepped by encapsulating both sub-grids in the single channel; a future
per-channel-lattice engine generalisation is cosmetic (physics identical).

**The whole U0→U4 unified real-space chain is now closed.** Open frontier beyond
this roadmap: nuclear saturation (Phase-2) and the dynamical-processes layer
(emission/scattering/transport).
