# FB08 — NN short-range repulsive core, derived

**Tier:** B — quantitative confrontation
**Falsification power:** ★★★ (closes the one tuned knob F104 exposed; structural)
**Model element under test:** the F113 derivation of the NN hard core from quark Pauli + chromomagnetic interaction.
**Supersedes:** new

## Hypothesis (derived, no tuned wall)
The NN short-range repulsion is the quark-Pauli + chromomagnetic (one-gluon-exchange) effect:

  core height `+341.8 MeV` (exact given the chromomagnetic coupling g_cm),

replacing the hand-tuned hard core of F104. Combined with F126 σ attraction and ω repulsion, the derived core (no hard wall) returns the physical deuteron `E_b=2.224 MeV`, `κ=0.2316 fm⁻¹`.

## Measured target + source
- Phenomenological NN potentials (Argonne v18, etc.): strong short-range repulsion (~GeV-scale wall inside ~0.5 fm); the deuteron observables it must be consistent with.

## Falsification criterion
Falsified if:
1. The quark-Pauli + chromomagnetic mechanism gives the wrong sign (attractive) or wrong scale for the short-range core, **or**
2. With the derived core (no tuned wall) the deuteron no longer binds at the physical E_b/κ.

## CASIM build & run
Quark-level Pauli + chromomagnetic computation feeding the NN potential.
1. Numerical: compute the six-quark Pauli-blocking + chromomagnetic interaction energy at short NN separation; confirm `+341.8 MeV` height given g_cm, correct (repulsive) sign.
2. Feed the derived core into the FB07 deuteron solve (no hard wall); confirm physical `E_b=2.224 MeV`, `κ=0.2316 fm⁻¹`.

## Pass/fail gate
- PASS: derived core `+341.8 MeV` repulsive AND deuteron binds at physical values with it.
- FALSIFIED: wrong sign/scale, or deuteron fails to bind with the derived core.

## Provenance
F113 (NN short-range repulsive core, 7/7 PASS), F126 (σ attraction), F104 (deuteron).
