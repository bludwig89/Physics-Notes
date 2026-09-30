# Notebook × SM Cross-Check — pp. 12–29: Weyl Representation, Riemannian Background,
# Sachs Electrogravity Lagrangian

*2026-09-22 - 21:35 · checks `notebook-reconstruction-02-weyl-and-sachs-lagrangian.md` +
`notebook-reconstruction-02b-nb028-theta-curved.md` (per protocol §3, batch 02b's corrections are
read together with batch 02) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 2 verdicts (NB-037 and NB-038, both IMPROVES), 0 changed. An
independent subagent with no access to this write-up's reasoning confirmed all four ECSK citations
(the 2024 *Phys. Lett. B* tabletop-test paper, the 2020 *JHEP* mimetic-ECSK paper, the 2025
Chishtie exclusion preprint, and the "contested, not consensus" characterization of that preprint)
say what is claimed here.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.12-13 | 12–13 | REINFORCES | SETTLED | Massive/massless Weyl-basis Dirac equations, exactly standard. |
| pp.14 | 14 | NEUTRAL | SETTLED | Riemannian-geometry definitions, textbook background, no independent claim. |
| pp.15-29 | 15–29 | IMPROVES | ACTIVE | The Sachs-formalism machinery itself (tetrad/2-spinor Lagrangian, Palatini first-order GR, Noether currents) is standard, correctly used GR/QFT technique; the one genuinely distinguishing physics result the author reaches (NB-037/038, torsion sourced by spinor spin density) lands exactly on Einstein–Cartan–Sciama–Kibble theory, a real, still-live (though empirically unconfirmed) extension of GR. Sachs' own further claim — that this construction unifies electromagnetism with gravity in a single field — is not supported by outside analysis of his formalism and has seen essentially no continuation since the mid-2010s. |

## What the field learned since 2007 that matters for this batch
- **Torsion gravity (ECSK) now has a proposed terrestrial test.** A 2023/2024 paper (published in
  *Physics Letters B*) proposes a tabletop spin-polarization reflection/transmission experiment
  specifically designed to distinguish Einstein–Cartan torsion from ordinary GR — a concrete,
  particle-physics-scale test that did not exist in 2007. [Signature of Einstein-Cartan theory (*Phys. Lett. B* 849, 138431, 2024; arXiv:2309.11536)](https://arxiv.org/pdf/2309.11536) [B]
- **Equivalence-principle tests have tightened by ~3 orders of magnitude since 2007.** The
  MICROSCOPE satellite mission (final results ~2022) measured the universality of free fall to
  $\Delta a/a<10^{-15}$, the most precise EP test to date; this is exactly the kind of measurement
  that constrains torsion-matter coupling in Einstein-Cartan-type extensions. [Theoretical and experimental basis for excluding Einstein-Cartan theory within the USMEG-EFT framework (arXiv:2509.08848, 2025)](https://arxiv.org/pdf/2509.08848) [C — single-author, not-yet-peer-reviewed preprint; cited here only for the MICROSCOPE bound it reports, not for its exclusion conclusion, which is contested below]
- **A 2025 preprint claims Einstein-Cartan theory is now excluded**, combining the MICROSCOPE bound
  with a theoretical argument that spin-torsion coupling generates uncontrolled four-fermion
  divergences. This is a single-author arXiv preprint, not yet peer-reviewed, and its claim is in
  active tension with 2020–2024 published work (including the tabletop-test proposal above and a
  2020 *JHEP* mimetic-ECSK construction) that continues to treat the theory as viable and worth
  testing further — i.e. the field has not converged on exclusion. [same arXiv:2509.08848] [C]; [Mimetic Einstein-Cartan-Sciama-Kibble (ECSK) gravity (*JHEP* 10, 150, 2020)](https://link.springer.com/article/10.1007/JHEP10(2020)150) [B]
- **Sachs' specific electromagnetism-from-gravity identification has an outside critical
  assessment.** A published critique of Sachs'-type "unified field theory" constructions
  (evaluating the claim that an antisymmetric piece of a generalized metric/connection field is
  genuinely the electromagnetic field) concludes the identification is not supported by their
  analysis. This predates 2007 but is the most direct external verdict on exactly what pp.15–29
  builds toward, and no rebuttal or revival specific to Sachs' program was found in 2020s search.
  [Clifford Valued Differential Forms, Algebraic Spinor Fields, Gravitation, Electromagnetism and "Unified" Theories (Rodrigues et al., arXiv:math-ph/0311001)](https://arxiv.org/pdf/math-ph/0311001) [B]
- **Where independently checked, Sachs' formalism reduces to ordinary GR, not something new.** For
  the spherically symmetric static (Schwarzschild-type) case, an independent author found Sachs'
  quaternionic field equations reduce to equations "identical to the corresponding Schwarzschild
  equations" — i.e. no deviation from GR in the one regime checked, and no new observable
  prediction there either. [Schwarzschild Solution of the Generally Covariant Quaternionic Field Equations of Sachs (*Eur. Phys. J. Plus* 126, 16, 2011; arXiv:1010.3630)](https://arxiv.org/pdf/1010.3630) [B]

## Per-build verdicts

### NB-014, NB-015 (pp.12–13) — Massive and Massless Weyl-Basis Dirac Equations
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the coupled Weyl-basis equations for $(\psi_+,\psi_-)$ reproduce the
  correct relativistic dispersion $E^2=p^2c^2+m_0^2c^4$ for $m_0\neq0$, and decouple into two
  independent helicity (chiral) equations for $m_0=0$.
- **Anchor:** foundations — the Weyl-basis form of the Dirac equation, the same construction used
  throughout electroweak theory (left/right chiral fermion fields) and confirmed to be a legitimate
  "square root" of the Klein-Gordon dispersion relation.
- **Current status:** unchanged, standard.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — standard since the 1920s-30s (Weyl 1929), untouched by any 2007+ development.

### NB-016 (p.14) — Riemannian Geometry Background
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim (field terms):** none — definitional metric-tensor/local-flatness background.
- **Anchor:** none (definitional).
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-017, NB-019, NB-020 (pp.15–17) — Tetrad/2-Spinor Metric Identity; Covariant Derivative Form
- **Checked against:** reconstruction status `SOLID` (NB-017), `SOLID-WITH-CORRECTION` /
  `NOT-TESTABLE` (NB-019, split between the core identity and Sachs' own quoted forms), `SOLID` /
  `NOT-TESTABLE` (NB-020, split the same way; the specific $\Omega^{(\chi)}_\rho$ formula was later
  tested in 02b §7.4 and found to need a sign fix relative to the notebook's own convention)
- **Claim (field terms):** a 2-spinor object $q^\mu$ built from Pauli matrices reproduces the
  Minkowski metric via $g^{\mu\nu}=-\tfrac12(q^\mu\tilde q^\nu+q^\nu\tilde q^\mu)$, and matter
  fields couple to curvature through a minimal spin-connection covariant derivative
  $\partial_\mu+\Omega_\mu$.
- **Anchor:** foundations — this is the standard tetrad (vierbein)/2-spinor formalism for coupling
  spinor matter to curved spacetime (Weyl 1929; Infeld–van der Waerden 1933; standard in every
  modern GR-with-fermions treatment, e.g. loop quantum gravity's Ashtekar variables and ordinary
  QFT-in-curved-spacetime), not something unique to Sachs' presentation.
- **Current status:** unchanged, standard technique; this is how any spinor field (electron,
  quark, neutrino) is coupled to gravity in both mainstream GR and any spinor-based lattice/CA
  construction.
- **Verdict:** REINFORCES · SETTLED (the general tetrad/2-spinor technique). Sachs' own directly
  quoted book equations ((3.60)/(3.62)/(3.77)/(3.88)) remain **NOT-TESTABLE as citations** —
  unverifiable without his book, and the reconstruction's own later pass (02b §7.4) found two of
  them ((3.77) and p.15's (3.88)) do not match the sign convention the notebook's own
  $\eta_{;\mu}=\partial_\mu\eta+\Omega_\mu\eta$ needs — a reconstruction-internal correctness
  question about accurately quoting Sachs, not an external SM/GR claim, so not re-graded here.
- **Hindsight:** none for the general technique (unchanged); see the batch-level bullets above for
  Sachs' own specific unification claim.

### NB-018, NB-021, NB-025, NB-026, NB-031, NB-033, NB-034, NB-036 (pp.16–28) — 2-Spinor
### Lagrangian Construction, Euler–Lagrange Bookkeeping, Noether Current
- **Checked against:** reconstruction status `SOLID` (all)
- **Claim (field terms):** a real (Hermitian) 2-spinor kinetic Lagrangian is built by symmetrizing
  $i\eta^+q^\mu\partial_\mu\eta$ with its conjugate; because this Lagrangian is *linear* in
  $\dot\eta$, its naive canonical Hamiltonian identically vanishes (NB-025) — the well-known
  first-order-fermion Hamiltonian pathology, requiring the symmetrized/constrained treatment used
  throughout (this is the same reason the free Dirac Lagrangian needs care in its canonical
  formulation, standard since Dirac's own 1950s work on constrained Hamiltonian systems); the
  resulting Euler–Lagrange equations, matter current
  $\partial\mathcal L/\partial\Omega_\rho\propto\eta^+q^\rho\eta$ (the 2-spinor analog of the Dirac
  vector current $\bar\psi\gamma^\rho\psi$), and Hermiticity-based equation-of-motion collapse
  (NB-034) are all standard field-theory bookkeeping for a first-order fermion Lagrangian.
- **Anchor:** foundations — standard QFT technique for constructing a real fermionic Lagrangian and
  its conserved current, the same machinery (in different notation) used for the Dirac field
  throughout the SM.
- **Verdict:** REINFORCES · SETTLED (as a group; no individual build in this group makes a
  claim that diverges from standard technique).
- **Hindsight:** none — standard, unchanged.

### NB-019 (core identity), NB-032, NB-035 (pp.16, 23–28) — Trace-Derivative / Matrix-Calculus
### Identities
- **Checked against:** reconstruction status `SOLID` (all; NB-032 also carries a
  `SOLID-WITH-CORRECTION` for one $(-g)^{1/2}$ power-counting slip, fixed in 02b §7.2)
- **Claim (field terms):** none in SM/GR terms — these are generic linear-algebra lemmas
  ($\partial\,\mathrm{Tr}(AB)/\partial B=A^T$ and its variants) used as calculational machinery for
  the variations above, not physical claims themselves.
- **Anchor:** none — pure mathematics, no SM/GR-testable content (protocol §4a: no anchor → NEUTRAL).
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-022, NB-023, NB-024 (pp.18–19) — Einstein Equation Component; Palatini First-Order GR
- **Checked against:** reconstruction status `SOLID` (NB-022, NB-023), `DEAD-END-AUTHOR-CALLED-IT` (NB-024)
- **Claim (field terms):** $T_{00}=\tfrac1{8\pi}G_{00}$ follows directly from the Einstein equation
  $G_{\mu\nu}=8\pi T_{\mu\nu}$ restricted to the $00$-component; treating the connection and metric
  (or $\Omega$ and $q$) as independent variables in a first-order Hamiltonian is the standard
  Palatini trick.
- **Anchor:** GR foundations — the Einstein field equation and the first-order (Palatini)
  reformulation of GR, both completely standard.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none relevant.

### NB-027, NB-028 (p.21) — Covariant Stress-Tensor Curvature Coupling
- **Checked against:** reconstruction status `SOLID` (originally; 02b found a sign error in the
  flat-space $\Theta^{\mu\nu}$ these two builds feed from — see the errata note below), corrected
  to `SOLID-WITH-CORRECTION`
- **Claim (field terms):** replacing ordinary with covariant derivatives in the matter
  stress-energy tensor ($\eta_{;\mu}$ in place of $\partial_\mu\eta$) is the standard minimal-coupling
  route by which a stress tensor picks up curvature dependence.
- **Anchor:** GR foundations — minimal coupling of matter stress-energy to curvature, standard.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none relevant. (Note: 02b found the immediately preceding flat-space step,
  NB-026/027's own $\Theta^{00}$, carries a sign error making it identically zero for a plane wave —
  a reconstruction-internal correction, not a change to the external physics anchor these two
  builds rest on.)

### NB-029, NB-030 (pp.21–22) — Scalar Toy-Matter Lagrangian ($i$-Factor Slip)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
- **Claim (field terms):** same free real scalar field as NB-001 (batch 01), here as a toy test
  case for the $\Theta^{\mu\nu}$ machinery; the transcribed form carries a spurious factor of $i$,
  corrected by the reconstruction.
- **Anchor:** none beyond what was already checked at NB-001 (batch 01) — this is an internal
  arithmetic slip in copying the standard real-scalar Lagrangian, not a distinct physical claim.
- **Verdict:** NEUTRAL · SETTLED (already covered substantively under NB-001)
- **Hindsight:** n/a.

### NB-037, NB-038 (pp.28–29) — Torsion Sourced by Spinor Spin Density (Einstein–Cartan–Sciama–Kibble)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION (resolved)` for both, per
  `notebook-reconstruction-02b-nb028-theta-curved.md` §8–9 (originally `NEEDS-WORK` in batch 02)
- **Claim (field terms), corrected form:** varying a first-order (Palatini-type) gravitational
  action with independent connection $\Omega_\mu$ in the presence of spin-½ matter does **not**
  force the connection's antisymmetric (torsion) part to zero; instead torsion is algebraically
  sourced by the matter's spin density, $T^{\rho ab}=\kappa S^{\rho ab}$ with $S^{\rho ab}$ built
  from the totally antisymmetric (axial) fermion bilinear. In vacuum, or for spin-density-free
  matter, torsion vanishes and the connection reduces to the ordinary torsion-free (Levi-Civita)
  relation.
- **Anchor:** GR foundations — is spacetime torsion-free (standard GR/Riemannian assumption) or
  does fermionic spin density source torsion (Einstein–Cartan–Sciama–Kibble theory, Kibble 1961,
  Sciama 1964)? A well-established, mathematically consistent extension of GR, empirically
  unconfirmed because its effects (an ultra-short-range fermion-fermion contact interaction,
  $\sim GJ^5\!\cdot\!J^5$) are negligible except at densities far beyond anything tested to date.
- **Current status:** ECSK is textbook-standard as a *mathematical* generalization of GR (any
  Palatini-type first-order gravity with fermionic matter naturally produces it); it remains
  *empirically* untested — current bounds (from equivalence-principle tests) constrain but do not
  exclude it outright, and its status is contested even among specialists (see the 2025 preprint
  vs. the 2020/2023 constructive and test-proposal work in the batch-level bullets above).
- **Live work:** yes — a 2023/2024 published paper proposes a concrete tabletop test; a 2020 *JHEP*
  paper builds a mimetic ECSK extension; a single 2025 preprint argues for exclusion, contested by
  the continuing 2020–2024 work. [Signature of Einstein-Cartan theory (arXiv:2309.11536, *Phys. Lett. B* 2024)](https://arxiv.org/pdf/2309.11536) [B]
- **Verdict:** IMPROVES · ACTIVE (the notebook's own specific derivation, once corrected, lands
  exactly on a genuine, still-open extension of GR — not excluded, named research line, addresses
  a real structural question GR alone does not answer, namely how geometry responds to intrinsic
  spin rather than only to energy-momentum)
- **What would decide it:** the proposed tabletop spin-polarization test (arXiv:2309.11536);
  further equivalence-principle precision; any future clean theoretical resolution of the
  four-fermion-divergence objection the 2025 preprint raises.
- **Hindsight:** the author's own self-diagnosis ("not good!") was premature by the field's own
  later standards — this is now recognized (since 1961/1964, well before this notebook, but
  apparently not connected by the author at the time) as the standard, not pathological, behavior
  of first-order gravity with fermionic matter. What's genuinely post-2007: torsion gravity has
  gone from a purely formal curiosity to something with a concrete, if still speculative, proposed
  laboratory test.

## Reconstruction queries
None beyond what the reconstruction's own 02b pass already resolved (NB-019/020/032's sign and
power-counting corrections, NB-026-028's sign correction, NB-037/038's completion) — this
cross-check finds those corrected forms externally consistent and has no further dispute with the
reconstruction's verdicts.

## Handoff items raised (mirrored into the handoff file)
One item — see `notebook-sm-crosscheck-handoff.md` §C (a reconstruction-adjacent observation, not
a question about the model): the reconstruction's own NB-037/038 write-up (02b §8.6) notes the
Hehl–Datta ECSK contact term and a possible route to recovering electromagnetism from the
connection's U(1)/trace direction if a Maxwell kinetic term is added by hand. That is the
reconstruction's own physics content, already fully worked out there — nothing further for this
cross-check to add, so no handoff item was raised beyond what is already in that file. (No table
row added this run.)

## Contamination log
None. This run drew on the two reconstruction files (as directed by protocol §1) plus the sources
listed below, fetched in-session. No `findings/`, `docs/claims/`, `src/`, or model-specific
reference content was read. One reconstruction passage (02b §8.6, "Model relevance") explicitly
discusses how the repo's own gravity sector (torsion-free) relates to this result; per firewall
rule 3 this was read (it is inside the permitted reconstruction file) but deliberately **not**
used to form any verdict above — the SM-relation and field-status tags for NB-037/038 rest solely
on the external ECSK literature cited, not on how the model uses or avoids torsion.

## Appendix — search queries used
- "Mendel Sachs unified field theory general relativity quaternion current status reception physics"
- "Einstein-Cartan Sciama Kibble torsion gravity spin experimental constraint test 2020 2023"
- "\"Sachs\" unified field theory quaternion gravity electromagnetism 2020 2021 2022 2023 paper arxiv"
- (WebFetch) arxiv.org/abs/2509.08848 — Chishtie 2025 Einstein-Cartan exclusion claim
- (WebFetch) arxiv.org/abs/2309.11536 — Einstein-Cartan tabletop signature paper
- (WebFetch) arxiv.org/abs/1010.3630 — Sachs quaternionic Schwarzschild solution

## Sources
- [Signature of Einstein-Cartan theory (*Phys. Lett. B* 849, 138431, 2024; arXiv:2309.11536)](https://arxiv.org/pdf/2309.11536) [B]
- [Theoretical and experimental basis for excluding Einstein-Cartan theory within the USMEG-EFT framework (arXiv:2509.08848, 2025)](https://arxiv.org/pdf/2509.08848) [C]
- [Mimetic Einstein-Cartan-Sciama-Kibble (ECSK) gravity (*JHEP* 10, 150, 2020)](https://link.springer.com/article/10.1007/JHEP10(2020)150) [B]
- [Clifford Valued Differential Forms, Algebraic Spinor Fields, Gravitation, Electromagnetism and "Unified" Theories (Rodrigues et al., arXiv:math-ph/0311001)](https://arxiv.org/pdf/math-ph/0311001) [B]
- [Schwarzschild Solution of the Generally Covariant Quaternionic Field Equations of Sachs (*Eur. Phys. J. Plus* 126, 16, 2011; arXiv:1010.3630)](https://arxiv.org/pdf/1010.3630) [B]
- [Mendel Sachs (Wikipedia, for the theory's general reception summary only — background, not used for any specific number)](https://en.wikipedia.org/wiki/Mendel_Sachs) [D]
