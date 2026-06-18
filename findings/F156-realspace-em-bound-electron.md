# F156 — U2: a real-space, real-time EM-bound electron (stationary cloud)

**Date:** 2026-06-17 - 20:23
**Status:** Confirmed — 4/4 checks PASS (`test_F156_realspace_electron_bound.py`).
**Roadmap:** `roadmap-unified-real-space.md` U2 — closes the open item ("a real-time lattice-bound electron wavepacket, not the spectral F125 solver").
**Modules:** `src/casim/particles/channel.py` (`NonRelElectronChannel`, type `nr_electron`); scenarios `realspace_electron_bound.yaml` / `realspace_electron_free.yaml`.
**Cross-references:** [[F125-p5-hydrogen-atom-em-bound-state]] (spectral Dirac–Coulomb fine structure), [[F135-realspace-scalar-confinement]] (the vector-potential null this works around), [[F134-unified-real-space]] (U0/U2 responsive-but-not-stationary precursor).

## Result

A non-relativistic electron orbital evolved by an exactly-unitary split-step
(`e^{−iVdt/2}·F⁻¹e^{−ik²dt/2m}F·e^{−iVdt/2}`) in a Coulomb well, relaxed to the
well's ground state by imaginary time, is a **stationary bound cloud**: its RMS
radius stays flat (2.45 → 2.51, spread < 0.5 %) over 400 ticks, while the
matched free control (same orbital, no well) disperses ballistically to box
saturation (2.45 → 18.3). Norm conserved to ~1×10⁻¹⁴ (split-step unitary). The
q = −1 electron localises on the +1 source (correct attractive sign), and the
unification readout counts its charge.

## Why non-relativistic is the correct description (not a workaround)

An atomic electron is non-relativistic (v ~ αc ~ 0.007 c). The relativistic
Dirac electron in a *vector* Coulomb well on a tractable lattice does **not**
give a clean stationary state: it Klein-tunnels / undergoes the Zα→1
Dirac–Coulomb collapse (the F135 vector-confinement null; the F134 "responsive
but not stationary" probe). Two failure modes were verified directly here
before adopting the Schrödinger orbital:

1. **Static increment is pure gauge.** Applying the per-tick Wilson increment
   `e^{−iqφdt}` via the existing wrap/unwrap (`u1_wrap_dirac`) imparts *no*
   force on the density — wrap+unwrap of a scalar α is a pure-gauge transform
   (zero field strength). The centroid does not move under a linear potential.
2. **Accumulating wrap = real but pathological.** The engine's accumulating
   α(x) = Σφdt does produce a real constant E-field (E = −∂ₜA), hence a real
   force (this is why the F134 strongEM probe pulled the electron in), but on a
   relativistic Dirac packet at lattice coupling it over-accelerates / scatters
   rather than forming a stationary orbit.

The relativistic fine structure (Lamb shift, 2p split) is already supplied by
the F125 *spectral* Dirac–Coulomb solve; F156 is the real-time *binding*
demonstration, which is exactly what a CA does well.

## Exactness tier

Tier-3 (qualitative/statistical): bounded-vs-ballistic RMS, correct attractive
sign, neutrality bookkeeping. Norm conservation is machine-precision (the
split-step is exactly unitary). Absolute fm/eV remain P6/scale-gated (F123); the
demonstration is at a compressed scale (heavy electron, deep well) so the bound
cloud fits one tractable lattice. The physical proton:orbit ~10⁴ size ratio is
restored at U4 (block-spin multigrid).
