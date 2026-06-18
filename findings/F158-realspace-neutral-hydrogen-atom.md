# F158 — U3: neutral hydrogen as one dynamic real-space object

**Date:** 2026-06-17 - 20:23
**Status:** Confirmed — 6/6 checks PASS (`test_F158_neutral_hydrogen.py`).
**Roadmap:** `roadmap-unified-real-space.md` U3 — closes "the neutral hydrogen system (p + e, Q=0) as a co-evolving real-space object".
**Modules:** scenarios `unified_hydrogen_atom.yaml` / `unified_hydrogen_atom_free.yaml`; uses `quark_dirac` (F136) + `nr_electron` (F156); `src/casim/particles/channel.py` (`quark_dirac` now honours `confine.dt`).
**Cross-references:** [[F156-realspace-em-bound-electron]] (the bound electron), [[F135-realspace-scalar-confinement]] / [[F136-colour-quark-confinement]] (the confined charged proton), [[F134-unified-real-space]] (U0 full-chain wiring), [[F148-modular-element-assembler]] / [[F157-manybody-nuclei-and-electron-clouds]] (the spectral atom counterpart).

## Result

A confined, charged proton (three colour Dirac quarks `uud`, held together by
the F135/F86 Lorentz-scalar confining Y-string) and a non-relativistic bound
electron (U2 `nr_electron`, relaxed into the proton's own Coulomb potential) are
put on **one** BCC lattice and co-evolve as a single neutral atom. Over the run
(L=24, 200 ticks):

- **net EM charge = 0 exactly** for the whole run (uud = +1, e = −1; < 10⁻¹²);
- **all four coupling loops live** (‖J_colour‖, ‖gluon A‖, ‖J_em‖, ‖photon α‖ > 0);
- **proton confined**: cluster RMS plateaus at ≈3.3 (vs the free control's
  monotonic dispersal) — the scalar string binds;
- **electron bound**: cloud RMS ≈4.0–4.4, bounded (vs free dispersal), and
  *larger* than the proton — the correct atomic structure (cloud surrounds
  nucleus);
- **electron tracks the proton**: the e–p centroid separation stays small
  (≲1.5) compared with the cloud radius — a concentric bound cloud;
- every channel norm conserved to ~10⁻¹³.

This is the first composite-neutral atom exhibited as a single co-evolving
real-space lattice object — the "universe in a bottle" milestone within the
compressed-scale substitution.

## Implementation note

The `quark_dirac` variable-mass (scalar-confinement) step now passes
`confine.dt` to `dirac_step_3d_bcc_varm_splitstep` (default 1.0, so existing
scenarios — e.g. `realspace_proton_1fm` — are bit-unchanged). At the larger
L=24 box the confining mass m_eff(x)=m+σ|x−R| grows large; the smaller Strang
timestep (dt=0.5) keeps the per-cell η↔χ rotation in its stable regime, so the
proton plateaus instead of dispersing. (`particle`-type Dirac stand-ins, F135,
were not modified.)

## Exactness tier

Tier-3 (qualitative/statistical): bounded-vs-free proton and electron radii,
concentric tracking, loop liveness. Neutrality and norm conservation are exact /
machine-precision. Compressed scale (the proton:orbit ~10⁴ physical size ratio
is U4, the block-spin multigrid); absolute fm/eV remain P6/scale-gated (F123).

## What remains (U4)

The honest physical atom — a proton ~10⁴× smaller than the orbit, the proton
entering the atomic-scale lattice as a block-spin-coarse-grained point charge
while its confinement runs on its own fine patch — is U4, the two-grid
multigrid, still the research frontier (`roadmap-unified-real-space.md`).
