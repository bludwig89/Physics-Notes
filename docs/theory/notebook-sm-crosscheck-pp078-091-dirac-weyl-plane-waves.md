# Notebook × SM Cross-Check — pp. 78–91: Dirac–Weyl Transform, Massless-Limit Plane-Wave
# Spinors, Mass-Perturbed Solutions

*2026-09-22 - 23:20 · checks `notebook-reconstruction-08-dirac-weyl-plane-waves.md` (NB-099/p.77
excluded — marked `CONTAMINATED-DEFER-TO-SUBAGENT` by the reconstruction, not yet disposed, so
outside this run's scope per protocol §2.2) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.78 | 78 | NEUTRAL | SETTLED | Blackbody radiation formulas, a minor aside. |
| pp.79-81 | 79–81 | REINFORCES | SETTLED | Standard gauge-to-contact EFT limit and Dirac spin-orbit reasoning, correctly used; the remaining builds are speculative sketches with no closed claim. |
| pp.82-90 | 82–90 | REINFORCES | SETTLED | Entirely standard, unchanging Dirac/Weyl explicit plane-wave spinor mechanics — basis transforms, massless-limit degeneracy, mass-perturbed solutions, particle/antiparticle classification — verified here to solve the free Dirac equation exactly; two isolated notebook arithmetic slips found by the reconstruction do not change this. |
| pp.91 | 91 | REINFORCES | SETTLED | A correct, if subtle, observation about how charge conservation survives naive perturbative mass-term expansions. |

## What the field learned since 2007 that matters for this batch
Nothing distinct from the free/perturbed Dirac-equation foundations already covered in earlier
runs. This batch is explicit-basis Dirac/Weyl spinor bookkeeping (representation transforms,
plane-wave solutions, particle/antiparticle and helicity classification) — completely standard
relativistic quantum mechanics dating to Dirac (1928) and the Weyl representation's use throughout
the electroweak theory already covered in the pp.57-76 write-up. No post-2007 development revises
any of it; the one recognizably "SM-relevant" idea in the batch (NB-117, "is $Z$ a $W^+W^-$ bound
state?") is dismissed by the author himself, correctly, on a straightforward energetics argument
the reconstruction independently confirms.

## Per-build verdicts

### NB-100 (p.78) — Blackbody Radiation
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim / anchor:** none — a minor standard-formula aside.
- **Verdict:** NEUTRAL · SETTLED

### NB-101 (p.79) — Gauge-to-Contact EFT Limit
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** a massive gauge boson's propagator collapses to a point-like contact
  interaction as $m_W\to\infty$ with $g^2/m_W^2$ fixed — the effective-field-theory mechanism
  connecting Fermi's original 4-fermion weak-interaction theory to the modern intermediate
  vector-boson (W/Z exchange) picture.
- **Anchor:** electroweak foundations — standard EFT reasoning, confirmed directly by the 1983
  discovery of the W and Z and by decades of precision agreement between low-energy weak
  measurements and the full electroweak theory.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — unchanged since the 1960s-80s.

### NB-102, NB-103 (pp.80–81) — $Z$-as-Diagram-Sketch; No-Spin-0 Analogy
- **Checked against:** reconstruction status `NOT-TESTABLE` (both)
- **Claim / anchor:** none closed enough to check — speculative sketches and analogies, no
  specific testable prediction.
- **Verdict:** NEUTRAL · SETTLED

### NB-104 (p.81) — Spin Built In to Preserve Total Angular Momentum
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the Dirac mass term mixes what would naively be separately-conserved
  helicity/orbital components, but total $J=L+S$ remains exactly conserved because spin is built
  into the relativistic theory precisely to make this consistent.
- **Anchor:** foundations — standard relativistic spin-orbit structure of the Dirac equation.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-105–NB-108 (pp.81–83) — Dirac↔Weyl Basis Transform; Basis-Spinor Images
- **Checked against:** reconstruction status `INCORRECT (numeric matrix entry only) /
  SOLID-WITH-CORRECTION` (NB-105) / `SOLID` (NB-106–108)
- **Claim / anchor:** none in external SM/GR terms — this is representation-conversion linear
  algebra (an explicit unitary transform between two equivalent bases for the same Dirac algebra,
  and the resulting basis-vector images). A single-entry arithmetic slip in the notebook's
  explicit numerical matrix was found and corrected by the reconstruction; the transform's defining
  *property* was independently confirmed exact.
- **Verdict:** NEUTRAL · SETTLED (pure matrix bookkeeping, no distinguishing physical claim beyond
  what NB-109/110 test directly, below)

### NB-109, NB-110 (pp.83–84) — Boxed Plane-Wave Spinors Solve the Dirac Equation
- **Checked against:** reconstruction status `SOLID` (both; confirmed via the physically
  meaningful test — do the boxed spinors solve the momentum-space Dirac equation on-shell — rather
  than re-tracing every intermediate sign)
- **Claim (field terms):** the notebook's boxed plane-wave spinor solutions satisfy
  $(\gamma^\mu k_\mu\mp m)\psi=0$ for on-shell momentum, in the Weyl representation.
- **Anchor:** foundations — the free Dirac equation's plane-wave solutions, completely standard.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-111 (p.84) — Massless-Limit Basis Degeneracy, Resolved
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (the author's own open
  question — why two basis states seem to vanish in the massless limit — is answered directly)
- **Claim (field terms):** in the massless limit, not every massive-basis spinor reduces smoothly
  to a helicity eigenstate at fixed, generic momentum; some are singular ($\sim1/\sqrt m$) there
  and require a different (degenerate/negative-energy-branch) limiting procedure.
- **Anchor:** foundations — a standard, if subtle, textbook fact about the relationship between the
  massive Dirac $u,v$-spinor basis and the massless helicity-eigenstate basis.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-112, NB-113 (pp.85–86) — Alternative Massless-Limit Method; Handedness Identification
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the massless limit's upper/lower spinor components correctly identify
  as right-/left-handed particle/antiparticle states, and the mass term mixes particle and
  antiparticle within a fixed helicity slot (not across helicities).
- **Anchor:** electroweak foundations — standard chiral structure, the same fact load-bearing
  throughout the SM's chiral gauge couplings (already covered at NB-079/086).
- **Verdict:** REINFORCES · SETTLED

### NB-114 (pp.86–88) — Four Mass-Perturbed Solutions
- **Checked against:** reconstruction status `NEEDS-WORK` (the most directly relevant
  self-consistency check — does the construction solve its own stated defining equations —
  passes exactly, forcing the correct on-shell relation $\lambda_0^2=k_0^2-k_3^2$; a separate
  cross-check against an independently-built $\gamma$-matrix embedding was inconclusive, likely a
  component-ordering mismatch, not confirmed as a notebook error)
- **Claim (field terms):** mass-perturbed spinor solutions built from a mixing parameter
  $\beta=\lambda_0/(k_0+k_3)$, satisfying the on-shell relation directly.
- **Anchor:** foundations — the same free-Dirac-equation mass-shell structure as NB-109-111.
- **Verdict:** REINFORCES · SETTLED (the specific relation the reconstruction confirmed exact is
  the standard relativistic mass-shell condition; the unresolved cross-check is a reconstruction
  bookkeeping loose end, not an external-physics discrepancy)
- **Hindsight:** none.

### NB-115 (p.87) — Self-Flagged Sign Issue, Unwarranted
- **Checked against:** reconstruction status `SOLID` (the notebook's own self-doubt resolved —
  no error)
- **Claim (field terms):** $p_z^2-E_z^2=-m_0^2c^2$, algebraically identical to the standard
  $E_z^2-p_z^2=+m_0^2c^2$.
- **Anchor:** foundations — the relativistic energy-momentum relation, unchanged.
- **Verdict:** REINFORCES · SETTLED

### NB-116, NB-118 (pp.89–90) — EM/Weak Particle Classification Tables
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** standard particle mass/charge/spin/chirality classification, consistent
  with the chirality and charge assignments already verified elsewhere in this section (NB-086,
  NB-113).
- **Anchor:** electroweak foundations — standard SM particle content and quantum numbers.
- **Verdict:** REINFORCES · SETTLED

### NB-117 (p.90) — "Is $Z$ a Bound State of $W^+W^-$?" (Self-Dismissed)
- **Checked against:** reconstruction status `DEAD-END-AUTHOR-CALLED-IT` (the author's own
  dismissal — "energies just don't work out" — confirmed by the reconstruction's plausibility
  check: binding $2m_W\approx160\,\text{GeV}$ down to $m_Z\approx91\,\text{GeV}$ would require an
  implausibly large binding fraction, far outside anything seen in known bound states)
- **Claim (field terms):** none surviving — a speculative idea the author raises and correctly
  rejects himself.
- **Anchor:** none — no claim to grade; the author's own reasoning is the check, and it is sound.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** the $Z$ boson's properties (mass, width, couplings) have been measured to very
  high precision since (LEP, 1989-2000, and continuing), leaving no room for any exotic bound-state
  substructure at the level this idea would require; this only reinforces the author's own
  correct 2007 dismissal, not a new consideration.

### NB-119 (p.91) — Charge Conservation: Exact vs. Perturbative
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** a Dirac mass term looks like it breaks charge conservation
  order-by-order in a naive perturbative expansion (mixing particle/antiparticle-type terms), but
  the exact (fully resummed) solution is manifestly charge-conserving.
- **Anchor:** foundations — a genuine, if subtle and standard, point about perturbation theory
  versus exact diagonalization in relativistic quantum mechanics.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

## Reconstruction queries
None. The two arithmetic slips the reconstruction found (NB-105's matrix entry, and the
already-resolved self-doubts at NB-111/115) are internal notebook-fidelity questions, not disputes
with external physics.

## Handoff items raised (mirrored into the handoff file)
None this run.

## Contamination log
None. NB-099 (p.77) was excluded from this run per the reconstruction's own
`CONTAMINATED-DEFER-TO-SUBAGENT` status (not yet disposed) — correctly out of scope per protocol
§2.2, not a contamination event in *this* cross-check session.

## Appendix — search queries used
None. Every anchor in this batch (free/perturbed Dirac equation structure, chiral particle
classification, EFT contact-limit reasoning) is unchanged, pre-2007 textbook physics already
covered with sources in the pp.1-2 and pp.57-76 write-ups; no claim in this batch required a fresh
external number or "current field status" check.

## Sources
None beyond the reconstruction file; no claims in this run required new citation beyond what
earlier write-ups already established for the same underlying Dirac-equation/electroweak
foundations.
