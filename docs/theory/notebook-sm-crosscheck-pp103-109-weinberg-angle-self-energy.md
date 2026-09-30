# Notebook × SM Cross-Check — pp. 103–109: sin²θ_W Numerology, EM/Yukawa Self-Energy,
# Classical Electron Radius, Ellipse Foci, W–S With Vector Bosons

*2026-09-22 - 23:55 · checks `notebook-reconstruction-10-weinberg-angle-self-energy.md` · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 1 verdict this run carries a CONFLICTS-DATA tag (NB-142); it restates
NB-080's already-cold-checked "masses without a dynamical Higgs field" premise (see
`notebook-sm-crosscheck-pp057-076-ws-without-higgs.md`) with the identical citation, so it is not
independently re-cold-checked here — see the note at NB-142 below. No other CONFLICTS/IMPROVES tags
in this run.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.103-104 | 103–104 | REINFORCES | SETTLED | The sin²θ_W numerology chain is exactly correct conditional algebra throughout; the notebook's own idle "coupling=3e ⟹ sin²θ_W=2/9" question is answered decisively by current precision data (no, it isn't realized in nature, off by more than 10σ). |
| pp.105 | 105 | REINFORCES | SETTLED | Classical EM/Yukawa self-energy integrals and physical-constant conversions check out against CODATA; one internal reference table remains genuinely underspecified. |
| pp.106 | 106 | REINFORCES | SETTLED | Newton's-method background math and the classical electron radius (with its convention-dependent factor of 2 correctly identified) both check out. |
| pp.107 | 107 | NEUTRAL | SETTLED | Pure analytic-geometry aside (ellipse foci); a transcription slip found and corrected, no SM/GR bearing. |
| pp.108-109 | 108–109 | CONFLICTS-DATA | SETTLED | The final vector-boson construction is standard, correct Yang–Mills minimal coupling; the accompanying conceptual observation restates the same "avoid the Higgs mechanism" tension already graded against the 2012 discovery at pp.62-72. |

## What the field learned since 2007 that matters for this batch
The weak mixing angle is now known to sub-per-mille precision in multiple renormalization schemes:
$\sin^2\theta_W^{\rm on\text{-}shell}=0.22342\pm0.00009$,
$\hat s_Z^2\,(\overline{MS})=0.23122\pm0.00006$, and the effective leptonic
$\sin^2\theta_{\ell,\rm eff}=0.23148\pm0.00013$ (all PDG). This lets the notebook's own p.104 idle
question — "is there any significance to $\sin^2\theta_W=2/9=0.2\overline2$?" — be answered
directly rather than left open: even in the closest scheme (on-shell), $2/9$ misses the measured
central value by more than 10 standard deviations, and misses the more commonly quoted
$\overline{MS}$ value by roughly 150 standard deviations. Nothing about this precision level is a
2007+ development in the sense of a qualitative discovery — the weak mixing angle was already known
to good precision in 2007 — but the sub-per-mille level now available leaves essentially no room
for a coincidence at the level the notebook's own arithmetic (working with $\sin^2\theta_W=0.232$,
two-decimal precision) could have distinguished at the time. [PDG 2024 review: Electroweak Model and Constraints on New Physics (*Phys. Rev. D* 110, 030001, 2024)](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-standard-model.pdf) [A]

## Per-build verdicts

### NB-130, NB-131, NB-132 (pp.103–104) — sin²θ_W Numerology Chain
- **Checked against:** reconstruction status `SOLID` (all three)
- **Claim (field terms):** correctly-computed conditional algebra for the neutral-charge operator
  and $W^\pm$ raising/lowering combinations at both the experimental $\sin^2\theta_W=0.232$ and
  the hypothetical $\sin\theta_W=\tfrac12$, plus the standard coupling-normalization identity
  $g=e/\sin\theta_W$.
- **Anchor:** electroweak foundations — standard Weinberg-angle bookkeeping, unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none for the algebra itself; see the batch-level bullet for the precision context
  bearing on NB-133 below.

### NB-133 (p.104) — "Coupling to $W^\pm=3e$" $\Rightarrow\sin^2\theta_W=2/9$ (Idle Numerology)
- **Checked against:** reconstruction status `SOLID` (the conditional algebra is exactly right;
  the reconstruction is explicit that this is presented in the notebook as idle "is there any
  significance to this?" speculation, not a derived prediction)
- **Claim (field terms):** *if* the charged-current coupling equals exactly $3e$, algebra alone
  forces $\sin^2\theta_W=2/9$ exactly — correct, unremarkable conditional arithmetic. The open
  question the notebook poses itself, not resolved on the page, is whether this condition (and
  hence $2/9$) has any physical significance.
- **Anchor:** electroweak precision physics — is the measured weak mixing angle equal to (or
  suggestively close to) the rational number $2/9$?
- **Current status:** no. Current PDG precision values put $\sin^2\theta_W$ at $0.22342\pm0.00009$
  (on-shell) to $0.23148\pm0.00013$ (effective leptonic) — none within many standard deviations of
  $2/9=0.\overline{2}=0.22222$.
- **Verdict:** REINFORCES · SETTLED (for the conditional algebra itself, which is exactly right)
- **Hindsight:** the notebook's own idle question is answered by data the author did not have
  precise enough access to distinguish in 2007: $2/9$ is not realized as the physical weak mixing
  angle in any standard renormalization scheme, at high confidence. This closes the specific
  question posed on the page; it says nothing about, and is not evidence for or against, any
  unrelated quantity that happens to share the same rational value in a completely different
  physical context (per protocol §2.3, this cross-check does not read or evaluate model-internal
  content, and the reconstruction file's own correlation-queue note about a decision elsewhere is
  not used here to form this verdict — see the contamination log below).

### NB-134 (p.104) — $Q_z$ at $\sin^2\theta_W=2/9$ (Self-Flagged Error, Confirmed Genuine)
- **Checked against:** reconstruction status `NEEDS-WORK` (two independent internal slips found —
  a $\sqrt{1/7}$-vs-$\sqrt{2/7}$ radical transcription error, and a $Q_z$ entry apparently copied
  from the wrong page — with the author's own hand-marked self-check confirmed to be a genuine,
  correctly-caught inconsistency)
- **Claim / anchor:** none beyond NB-133's already-graded premise — purely internal arithmetic
  given that hypothetical.
- **Verdict:** NEUTRAL · SETTLED

### NB-135, NB-136 (p.105) — Classical EM and Yukawa Self-Energy Integrals
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** the classical electrostatic self-energy integral
  $\int_{r_0}^\infty E^2\,dV=4\pi e^2/r_0$, and the Yukawa-potential self-energy integral reduced
  via the exponential-integral ($\mathrm{Ei}$) series identity.
- **Anchor:** none distinct from NB-013's (batch 01) treatment of the same classical self-energy
  divergence — pure, standard mathematical-physics integral identities, correctly invoked.
- **Verdict:** REINFORCES · SETTLED (consistent with, and not re-litigating, the NB-013 discussion
  of what this divergence does and doesn't imply about particle mass)
- **Hindsight:** none beyond what NB-013's write-up (pp.3-11 cross-check) already covers.

### NB-137 (p.105) — Ratio Table and Physical-Constant Bookkeeping
- **Checked against:** reconstruction status `NEEDS-WORK` ($M_W$ and $h$ conversions confirmed
  against CODATA; the $I(n)$ table and $k=1.39$ figure honestly flagged as unrecoverable from the
  page's surviving transcription, not asserted to be wrong)
- **Claim (field terms):** $M_W=80\,\text{GeV}\to1.43\times10^{-25}\,\text{kg}$;
  $h=6.626\times10^{-34}\,\text{J·s}$ — both standard physical-constant conversions.
- **Anchor:** none beyond standard constant values (CODATA), unchanged.
- **Verdict:** REINFORCES · SETTLED (for the two constants that could be checked; the
  underspecified table/ratio is a reconstruction-completeness question, not an external-physics
  discrepancy, so it does not pull the section tag down)
- **Hindsight:** none.

### NB-138 (p.106) — Newton's-Method Background Math
- **Checked against:** reconstruction status `SOLID`
- **Claim / anchor:** none — a generic numerical-methods aside, not a physics claim.
- **Verdict:** NEUTRAL · SETTLED

### NB-139 (p.106) — Classical Electron Radius
- **Checked against:** reconstruction status `SOLID` (the notebook's own factor-of-2 convention
  identified as a genuine, literature-documented alternative definition, not an error)
- **Claim (field terms):** $r_0=e^2/(2m_ec^2)\approx1.43\times10^{-15}\,\text{m}$, using a
  field-energy convention $\mathcal E=e^2/(2r_0)=m_ec^2$ that differs by a factor of 2 from the
  more commonly quoted CODATA classical electron radius $r_e=e^2/r_e=2.818\times10^{-15}\,\text{m}$.
- **Anchor:** foundations — both conventions for "the classical electron radius" are documented in
  standard references (e.g. Jackson's *Classical Electrodynamics*); this is a convention choice,
  not a physics discrepancy.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** the CODATA classical electron radius is essentially unchanged since 2007
  ($r_e=2.8179403262(13)\,\text{fm}$, current CODATA), so this build's arithmetic remains exactly
  as valid today as when written.

### NB-140 (p.107) — Ellipse Foci (Pure-Math Aside)
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION` (a transcribed equation
  describing a circle rather than an ellipse, corrected; a trivial $0.01$ rounding slip in the
  numeric example)
- **Claim / anchor:** none — pure analytic geometry, no SM/GR bearing (as the ledger's own section
  title notes: "pure-math aside").
- **Verdict:** NEUTRAL · SETTLED

### NB-141 (pp.108–109) — Promoting the Scalar Contact Term to a Vector Boson
- **Checked against:** reconstruction status `NEEDS-WORK` (the notebook's own stated intermediate
  reasoning step doesn't logically connect to what it writes next, but the final Lagrangian is
  standard and sound)
- **Claim (field terms):** the final construction —
  $g_0(\sigma_\mu\otimes\tau_0)W^{\mu+}\bar\nu_Le_L+\ldots$ — is structurally identical to the real
  Standard Model's charged-current Lagrangian: a fermion vector current dotted directly into a
  gauge field, the standard Yang–Mills minimal-coupling pattern.
- **Anchor:** electroweak foundations — minimal coupling of a gauge field to a matter current,
  completely standard, unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — the notebook's own silently-abandoned intermediate reasoning step (an
  incorrect attempt to build the vector coupling from a four-divergence) is not itself checked
  against external physics, since it plays no role in the construction actually used; the
  construction the page lands on is exactly right.

### NB-142 (p.109) — Weinberg-Angle "Kludge"; Why Should $W,B$ Be Massive?
- **Checked against:** reconstruction status `NOT-TESTABLE` (two accurate, standard conceptual
  observations, not closed derivations)
- **Claim (field terms):** (1) the Weinberg angle is the free rotation parameter accommodating
  $g'\neq g$ between independent $U(1)$ and $SU(2)$ couplings; (2) an unbroken gauge symmetry
  requires its gauge bosons to be massless, so asking why $W,B$ (which "couple only to themselves")
  should be massive is exactly the structural tension that motivates the Higgs mechanism — which,
  as the reconstruction notes explicitly, this notebook has been deliberately trying to avoid since
  pp.62-72 (NB-080).
- **Anchor:** Higgs sector / electroweak symmetry breaking — the identical anchor already graded in
  detail at NB-080 (pp.57-76 cross-check): is a dynamical Higgs-type mechanism required, or can
  gauge-boson masses be accommodated another way?
- **Current status / live work:** identical to NB-080 — see
  `notebook-sm-crosscheck-pp057-076-ws-without-higgs.md` for the full citations (the 2012 discovery
  and 2022 mass-coupling-proportionality confirmation, *Nature* 607, 52-59).
- **Verdict:** CONFLICTS-DATA · SETTLED (this build restates, in conceptual/prose form, the same
  premise already found in conflict with the post-2012 evidence; not a new independent claim, so
  graded consistently with NB-080 rather than re-researched)
- **Hindsight:** identical to NB-080's — see that write-up. This build is included here for
  completeness of section-level rollup, since the ledger tracks pp.108-109 as its own section.

## Reconstruction queries
None. All corrections in this batch (NB-134's radical/copied-value errors, NB-140's
circle-vs-ellipse transcription slip) are internal notebook-fidelity questions, independently
consistent with the external physics/math once corrected.

## Handoff items raised (mirrored into the handoff file)
None new this run — NB-133's "is $2/9$ significant" question is answered directly above using
external precision data alone, and does not raise a question for the model (per protocol §2.3, this
cross-check does not compare against, or raise questions about, model-internal content it has not
read for that purpose; the reconstruction's own correlation-queue file, a separate tracked
document, is where any model-facing version of that question belongs, and it already has one).

## Contamination log
**One instance, handled per protocol §2.3.** The reconstruction file's own "Correlation queue
additions" section (its final paragraph) explicitly names and quotes a model-internal decision
(described there as "decision 7," concerning an unrelated angle in the model's own lepton-mass
sector) when explaining why it queued a question for a later, separate correlation pass. This
cross-check session necessarily read that paragraph as part of reading the reconstruction file in
full (permitted per protocol rule 1). No content from it was used to form the NB-133 verdict above:
that verdict rests solely on comparing the notebook's own $2/9$ figure against external PDG
precision measurements of $\sin^2\theta_W$, a completely different physical quantity from whatever
the reconstruction's correlation-queue note refers to. Flagged here for transparency, as the
protocol requires when model context leaks into a permitted-to-read file.

## Appendix — search queries used
- "PDG 2025 weak mixing angle sin^2 theta_W on-shell MS-bar value effective"

## Sources
- [PDG 2024 review: Electroweak Model and Constraints on New Physics (*Phys. Rev. D* 110, 030001, 2024)](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-standard-model.pdf) [A]
- Cross-referenced from `notebook-sm-crosscheck-pp057-076-ws-without-higgs.md` (NB-142): [A detailed map of Higgs boson interactions by the ATLAS experiment ten years after the discovery (*Nature* 607, 52-59, 2022)](https://www.nature.com/articles/s41586-022-04893-w) [A]
