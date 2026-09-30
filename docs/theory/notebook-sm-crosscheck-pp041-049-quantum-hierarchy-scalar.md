# Notebook × SM Cross-Check — pp. 41–49: "Quantum Hierarchy Equations of a Free Scalar Field"

*2026-09-22 - 22:05 · checks `notebook-reconstruction-04-quantum-hierarchy-scalar.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.41-49 | 41–49 | REINFORCES | SETTLED | The author's own clean, careful redo of the pp.1-2 scalar-QFT opening; entirely standard free-field canonical quantization and Fock-space construction, with one genuine notebook error (a broken Fourier convention) already superseded here by the author's own correct version, and no new SM-external content beyond what batch 01 (pp.1-2, pp.9-11) already established. |

## What the field learned since 2007 that matters for this batch
Nothing new beyond what was already covered for the same underlying physics in the pp.1-2
cross-check (canonical quantization of a free scalar field remains unchanged, foundational QFT;
the 2012 Higgs discovery and the 2021 scalar-triviality theorem noted there apply here by the same
reasoning, not repeated). One item specific to this batch: NB-060's self-critique that
$\omega_k=\sqrt{k^2+m^2}$ is a non-local (pseudo-differential) operator in position space, and that
this motivates moving to a local, first-order Dirac-type equation, is exactly the standard
textbook reason relativistic quantum theory does not build interacting theories directly on top of
a "square-root Klein-Gordon" Hamiltonian — unchanged since long before 2007, and not something any
post-2007 development revises.

## Per-build verdicts

### NB-048–NB-051 (pp.41–43) — KG Lagrangian, Fourier Convention, H in k-Space, Mode Expansions
- **Checked against:** reconstruction status `SOLID` (all four; explicitly by reference to batch
  01's NB-001/002/003 verifications plus standard Itzykson–Zuber citations)
- **Claim (field terms):** identical content to batch 01's NB-001–003 (free real scalar field
  canonical quantization, corrected Fourier convention, k-space Hamiltonian), redone here more
  carefully by the author with a working convention throughout.
- **Anchor:** foundations — same anchor as the pp.1-2 cross-check (canonical quantization of a free
  relativistic scalar field).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none beyond what the pp.1-2 write-up already covers (2012 Higgs discovery as
  vindication of the real-scalar-field formalism; 2021 scalar-triviality theorem as adjacent
  context for the *interacting* case, not this free construction). Not re-argued here.

### NB-052, NB-053 (p.44) — Crossed-Out False Starts
- **Checked against:** reconstruction status `DEAD-END-AUTHOR-CALLED-IT` (both, with the specific
  index-mixing error diagnosed by the reconstruction)
- **Claim (field terms):** none — an abandoned, self-corrected calculation attempt.
- **Anchor:** none.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-054 (p.45) — Boxed Free-Field Hamiltonian in Ladder Operators ("Ludwig eq. 3")
- **Checked against:** reconstruction status `SOLID` (confirmed to machine precision, including a
  $k\to-k$ dummy-relabeling subtlety the reconstruction states precisely)
- **Claim (field terms):** $H=\tfrac12\int\omega_k(a_k^+a_k+a_ka_k^+)\,d^3k/((2\pi)^32\omega_k)$,
  the standard normal-mode free-field Hamiltonian in creation/annihilation operators.
- **Anchor:** foundations — same standard result as batch 01's NB-003, here in fully second-quantized
  (ladder-operator) form.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-055, NB-056 (p.46) — Lattice Discretization; Multi-Mode Oscillator Eigenstates
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** discretizing the mode sum to a finite lattice and writing the standard
  multi-mode harmonic-oscillator eigenvalue equation $H|n\rangle=[\sum_j(n_j+\tfrac12)\omega_j]|n\rangle$.
- **Anchor:** foundations — standard QFT/QM structural fact (quantized field = collection of
  independent harmonic oscillators).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-057 (p.47) — Fock-Coefficient / First-Quantized Wavefunction Normalization
- **Checked against:** reconstruction status `SOLID` (standard combinatorial identity, correctly
  stated; a framing error in the reconstruction's own first verification attempt was caught and
  corrected before any verdict was written)
- **Claim (field terms):** the standard map between a symmetrized first-quantized $N$-particle
  wavefunction and an occupation-number Fock state, via the combinatorial factor $N!/\prod_jn_j!$.
- **Anchor:** foundations — standard second-quantization bookkeeping (e.g. Peskin & Schroeder Ch. 2).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-058, NB-059 (pp.47–48) — Vacuum-Energy Phase Removal; Final Multiparticle Equation
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the standard phase redefinition $\psi'=e^{-iKt}\psi$ removes the
  (divergent, lattice-dependent) vacuum-energy constant $K=\sum_j\tfrac12\omega_j$, leaving the free
  multiparticle Schrödinger equation $i\partial_t\psi'_N=\sum_j\omega_{k_j}\psi'_N$.
- **Anchor:** foundations — standard vacuum-energy-subtraction bookkeeping, the same normal-ordering
  idea used throughout QFT (this is the finite-mode, first-quantized-language version of normal
  ordering $:H:\ =H-\langle0|H|0\rangle$).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-060 (pp.48–49) — Self-Critique: Non-Covariance, Non-Locality of $\sqrt{-\nabla^2+m^2}$
- **Checked against:** reconstruction status `NOT-TESTABLE` (accurate self-critique, not an
  independent claim to grade right/wrong)
- **Claim (field terms):** the free-particle relativistic energy operator $\sqrt{-\nabla^2+m^2}$ is
  a genuinely non-local (pseudo-differential) operator in position space, and the resulting
  equation is not manifestly Lorentz-covariant — a real limitation motivating a shift to a local,
  first-order (Dirac-type) formulation.
- **Anchor:** foundations — this is exactly the standard, textbook reason relativistic QM/QFT
  prefers the Dirac equation over a "square-root Klein-Gordon" approach for interacting theories.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — this has been standard, uncontroversial physics since well before 2007, and
  the author's own diagnosis here is accurate and is exactly what motivates the notebook's own
  subsequent turn to Dirac/Weyl spinor equations (pp.12+, batch 02/03).

### NB-061 (p.49) — Bose-Symmetric Wavefunction Requirement
- **Checked against:** reconstruction status `NOT-TESTABLE` (definitional/interpretive statement)
- **Claim (field terms):** the $N$-particle wavefunction must be symmetric under particle exchange
  for identical bosons, enforced by the (anti)commutation relations of the ladder operators.
- **Anchor:** foundations — the standard bosonic case of the spin-statistics connection (though the
  full spin-statistics *theorem*, tying this to spin, is not itself derived on this page — only the
  operator-algebra mechanics of enforcing exchange symmetry once bosonic statistics are assumed).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

## Reconstruction queries
None. All verdicts checked here are externally consistent with standard QFT.

## Handoff items raised (mirrored into the handoff file)
None this run — nothing in this batch goes beyond what pp.1-2's cross-check already covers or
raises a question distinct enough to warrant a new handoff entry.

## Contamination log
None. This run drew only on the reconstruction file; no fresh external sources were needed beyond
what the pp.1-2 write-up already established for the same underlying physics (canonical
quantization of a free scalar field), so no new searches were run this pass.

## Appendix — search queries used
None — this batch's SM/GR anchor (free-field canonical quantization) was already researched in
full for the pp.1-2 cross-check; re-running the same searches for the same unchanged textbook fact
was judged unnecessary rather than skipped by oversight.

## Sources
Carried over from `notebook-sm-crosscheck-pp001-002-quantum-scalars-i.md` (same anchor, no new
claims in this batch): [Tong, *Quantum Field Theory* lecture notes, §2](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html) [D]; [PDG 2025 Higgs boson listing](https://pdg.lbl.gov/2025/listings/rpp2025-list-higgs-boson.pdf) [A]; [Aizenman & Duminil-Copin, *Ann. of Math.* 194(1), 2021](https://projecteuclid.org/journals/annals-of-mathematics/volume-194/issue-1/Marginal-triviality-of-the-scaling-limits-of-critical-4D-Ising/10.4007/annals.2021.194.1.3.short) [B]
