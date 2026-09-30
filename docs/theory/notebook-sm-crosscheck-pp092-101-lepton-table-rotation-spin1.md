# Notebook × SM Cross-Check — pp. 92–101: Lepton-Doublet EM/Weak Table, Monopole/Confinement
# Analogies, Rotation-Matrix Tensor Products, Spin-1 Clebsch–Gordan, 3D "Dirac" Equation

*2026-09-22 - 23:40 · checks `notebook-reconstruction-09-lepton-table-rotation-spin1.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.92-97 | 92–97 | REINFORCES | SETTLED | The 8-component lepton EM/weak coupling table is exactly reproduced from Standard Model group theory alone; the monopole/confinement analogies are apt but explicitly non-rigorous, correctly left as tentative. |
| pp.98-101 | 98–101 | REINFORCES | SETTLED | Standard rotation-matrix and angular-momentum-addition (Clebsch–Gordan) algebra, with several genuine transcription slips found and fixed; the closing margin note (the Riemann–Silberstein vector reducing a spin-1 "Weyl-like" equation to vacuum Maxwell) is a well-established, independently verified piece of classical electrodynamics with continuing relevance in the modern photon-wavefunction literature. |

## What the field learned since 2007 that matters for this batch
- **Magnetic monopoles remain undetected, with steadily tightening limits.** MoEDAL at the LHC
  found no monopoles and set a collider mass limit around 3.9 TeV (for 1-10 times the Dirac
  charge); IceCube's 8-year search (2022) similarly found none, setting the strictest limits to
  date in its targeted speed range. Neither result changes the qualitative picture NB-121 invokes
  (no observed magnetic monopole), but both are genuine post-2007 tightenings of exactly that bound.
  [Search for Relativistic Magnetic Monopoles with Eight Years of IceCube Data (*Phys. Rev. Lett.* 128, 051101, 2022)](https://link.aps.org/doi/10.1103/PhysRevLett.128.051101) [A]; [MoEDAL experiment (overview)](https://en.wikipedia.org/wiki/MoEDAL_experiment) [D]
- **The Riemann–Silberstein vector / "photon wavefunction" formalism NB-129 rediscovers has an
  active continuing literature**, including 2020s applications to light-scattering and duality
  questions, building on Bialynicki-Birula's 2013 topical review establishing it as (in his words)
  "the best possible choice for the photon wave function." [The role of the Riemann-Silberstein vector in classical and quantum theories of electromagnetism (Bialynicki-Birula & Bialynicka-Birula, *J. Phys. A* 46, 053001, 2013)](https://iopscience.iop.org/article/10.1088/1751-8113/46/5/053001) [B]; [Stokes-anti-Stokes light scattering: a photon-wave-function approach (arXiv:2007.05357, 2020)](https://arxiv.org/pdf/2007.05357) [C]

## Per-build verdicts

### NB-120 (pp.92–97) — 8-Component Lepton-Doublet EM/Weak Coupling Table
- **Checked against:** reconstruction status `SOLID` (exactly reproduced from SM group theory
  alone, including two non-obvious cross-assignments, with no reference to the notebook's own table)
- **Claim (field terms):** of the 8 chiral × particle/antiparticle components of the electron and
  neutrino fields, exactly 2 couple to both EM and the weak $W$, 2 to EM only, 2 to $W$ only, and 2
  to neither — determined entirely by $(T_3,Y)$ quantum numbers ($Q=T_3+Y$ for EM, $T_3\neq0$ for
  $W$).
- **Anchor:** electroweak foundations — standard SM lepton quantum-number assignments and gauge
  coupling structure, unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — this bookkeeping is exactly as it was in the 1970s formulation of the SM.

### NB-121, NB-122 (p.97) — Monopole and Confinement Analogies
- **Checked against:** reconstruction status `NOT-TESTABLE` (both; apt but explicitly non-rigorous
  analogies, appropriately tentative language, not overclaimed by the author)
- **Claim (field terms):** loose analogies — the absent right-handed weak current is likened to the
  absent magnetic monopole (both "missing" states); quark confinement is likened to the
  integer-only quantization of orbital angular momentum.
- **Anchor:** the individual facts underlying each analogy are real (no observed monopole; quark
  confinement is an established, if not fully analytically solved, QCD phenomenon; $L$ is
  integer-only while spin may be half-integer) but the analogies themselves are not structural
  equivalences (a topological absence vs. a representation choice vs. a strong-coupling dynamical
  effect are three different kinds of "missing"), so there is no single anchor prediction to check.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** monopole non-detection has tightened considerably (see batch-level bullet); quark
  confinement remains understood only non-perturbatively (lattice QCD), with no first-principles
  analytic proof of the confining flux-tube picture — both facts unchanged in kind since 2007, only
  in precision.

### NB-123 (p.98) — $R_z\otimes R_z$ Rotation Tensor Product
- **Checked against:** reconstruction status `SOLID`
- **Claim / anchor:** none in SM/GR terms — a specific matrix computation (standard spin-1/2
  rotation generator and its tensor square), confirmed exact.
- **Verdict:** NEUTRAL · SETTLED

### NB-124, NB-125 (p.98) — $R_x,R_y$ Rotation Matrices (Transcription Errors Found and Corrected)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
  (both)
- **Claim / anchor:** none in SM/GR terms — pure matrix bookkeeping (explicit spin-1/2 rotation
  generators and their tensor products), with two independent transcription slips per build found
  and precisely quantified by the reconstruction (a sin/cos entry swap, and — for NB-124 — an
  additional exact factor-of-4 error in a double-angle simplification).
- **Verdict:** NEUTRAL · SETTLED

### NB-126 (p.99) — Real Spin-1 Cartesian Generators; Pauli Tensor Products
- **Checked against:** reconstruction status `SOLID`
- **Claim / anchor:** none distinct from standard angular-momentum algebra — confirms the standard
  $L=1$ generators satisfy $[S_i,S_j]=i\epsilon_{ijk}S_k$ with Casimir $S^2=2I$, and that the
  stated Pauli tensor products are correctly computed.
- **Verdict:** NEUTRAL · SETTLED (pure representation-theory bookkeeping; the load-bearing physical
  content — angular-momentum addition — is graded at NB-127, where it actually does work)

### NB-127 (pp.99–100) — Clebsch–Gordan Reduction $\tfrac12\otimes\tfrac12=1\oplus0$
### (Genuine Error Found and Corrected Two Independent Ways)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (a missing $1/\sqrt2$
  normalization on two of three new-basis spin matrices, confirmed both by external Clebsch–Gordan
  re-derivation and by the matrices' own failure to satisfy their stated $\mathfrak{su}(2)$ algebra
  until corrected)
- **Claim (field terms):** two spin-1/2 systems combine as $\tfrac12\otimes\tfrac12=1\oplus0$
  (a spin-1 triplet plus a spin-0 singlet), with the coupled-basis spin operators built from the
  *sum* of the two individual spins (not, as the page's prose imprecisely suggests, a direct
  transform of the *product* operators $\sigma_i\otimes\sigma_i$).
- **Anchor:** foundations — standard angular-momentum addition, the same Clebsch–Gordan structure
  underlying, e.g., how two spin-½ fermions combine into a spin-1 triplet state (the identical
  algebra already discussed in the pp.5-6 cross-check's composite-photon material).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — standard quantum mechanics since the 1920s-30s.

### NB-128 (pp.100–101) — Spin-1 "3D Dirac Equation" $\partial_t\psi_\pm=\mp c\,\mathbf S\cdot\nabla\psi_\pm$
- **Checked against:** reconstruction status `SOLID` (confirmed to build correctly and consistently
  on NB-127's own — uncorrected — new-basis matrices)
- **Claim (field terms):** a first-order evolution equation built from spin-1 (rather than spin-½)
  generators, structurally parallel to the Weyl equation.
- **Anchor:** foundations — this is the general "square-root-of-a-wave-equation" construction
  applied to spin-1, structurally standard (and, as NB-129 shows, exactly the right form for a
  vacuum Maxwell-equation reformulation once the correct/Cartesian generator basis is used).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-129 (p.101) — Margin Note: the Riemann–Silberstein Vector Solves Vacuum Maxwell
- **Checked against:** reconstruction status `SOLID` (an independently verifiable, exactly correct
  physical claim; the reconstruction adds the honest caveat that it requires the Cartesian, not
  NB-127's rotated, generator basis to reduce cleanly)
- **Claim (field terms):** the complex vector $\mathbf F=\mathbf E+i\mathbf B$ satisfies
  $\mathbf S\cdot\nabla\,\mathbf F=i(\nabla\times\mathbf F)$ (built from the spin-1 Cartesian
  generators), and substituting it into $\partial_t\mathbf F=-c\,\mathbf S\cdot\nabla\,\mathbf F$
  separates exactly into the source-free Ampère and Faraday equations.
- **Anchor:** classical electrodynamics / photon-wavefunction foundations — this is precisely the
  Riemann–Silberstein vector construction (Riemann 1861, Silberstein 1907), revived in the modern
  literature as arguably the most natural candidate for a single-photon "wavefunction," with a
  documented continuing research application in quantum optics and light-scattering theory.
- **Current status:** unchanged, exact classical electrodynamics; the "photon wavefunction"
  interpretation remains a live area of foundational and applied interest (not a claim in tension
  with any data — it is a reformulation of standard Maxwell/QED, not an extension of it).
- **Live work:** yes, in the sense of continued application and pedagogical/interpretational
  development (2013 topical review, 2016 and 2020 papers using the same formalism for duality and
  light-scattering questions respectively) — see the batch-level bullet.
- **Verdict:** REINFORCES · SETTLED (a non-standard [spin-1 wave-equation] route to a standard
  [vacuum Maxwell] result, exactly matching a genuine, independently pre-existing, still-cited
  classical-electrodynamics construction)
- **Hindsight:** the author's single unelaborated margin line ("if $\psi_+=E+iB$") lands, with
  hindsight, on a real and well-regarded piece of classical field theory that the broader physics
  community had already been (and continues) developing — not an idiosyncratic notebook guess.

## Reconstruction queries
None. All corrections in this batch (NB-124/125's rotation-matrix slips, NB-127's missing
normalization factor) are confirmed correct by this cross-check's independent read of the
underlying standard physics, and are internal notebook-fidelity questions rather than disputes with
external physics.

## Handoff items raised (mirrored into the handoff file)
None beyond what the reconstruction's own correlation-queue entry for NB-129 already covers
(a question for the model's own photon construction, which per protocol §2.3 this cross-check does
not itself evaluate or restate as a new item, since the reconstruction's correlation queue — a
different tracked document — already carries it).

## Contamination log
None. This run drew only on the reconstruction file and the sources cited above, fetched
in-session.

## Appendix — search queries used
- "Riemann-Silberstein vector photon wavefunction Bialynicki-Birula review 2020 2023 status"
- "magnetic monopole search MoEDAL IceCube 2023 2024 results no detection"

## Sources
- [Search for Relativistic Magnetic Monopoles with Eight Years of IceCube Data (*Phys. Rev. Lett.* 128, 051101, 2022)](https://link.aps.org/doi/10.1103/PhysRevLett.128.051101) [A]
- [MoEDAL experiment (overview)](https://en.wikipedia.org/wiki/MoEDAL_experiment) [D]
- [The role of the Riemann-Silberstein vector in classical and quantum theories of electromagnetism (Bialynicki-Birula & Bialynicka-Birula, *J. Phys. A* 46, 053001, 2013)](https://iopscience.iop.org/article/10.1088/1751-8113/46/5/053001) [B]
- [Stokes-anti-Stokes light scattering: a photon-wave-function approach (arXiv:2007.05357, 2020)](https://arxiv.org/pdf/2007.05357) [C]
