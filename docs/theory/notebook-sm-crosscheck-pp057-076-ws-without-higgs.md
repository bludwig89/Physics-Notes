# Notebook × SM Cross-Check — pp. 57–76: Dirac Matrix Gauging, Weinberg–Salam Without Higgs,
# Helical-Motion Mass Model

*2026-09-22 - 22:55 · checks `notebook-reconstruction-06-dirac-matrices-ws-opening.md` +
`notebook-reconstruction-07-weak-contact-terms-helical-mass.md` (pp.62-72 spans both batches, read
together per protocol §3) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 3 verdicts (NB-080 CONFLICTS-DATA, NB-081 IMPROVES, NB-093–095
IMPROVES), 1 changed. An independent subagent with no access to this write-up's reasoning confirmed
the ATLAS 2022 Nature paper, the Higgsless-models review, the Symmetry 2025 zitterbewegung review,
and the CDF/ATLAS/CMS W-mass characterization all say what is claimed; it found the LEGEND-200
half-life figure was the projected *sensitivity* ($2.8\times10^{26}$ yr), not the observed bound
($1.9\times10^{26}$ yr) — fixed throughout.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.57 | 57 | NEUTRAL | SETTLED | Photocopied textbook reference insert, not the author's own claim. |
| pp.59-60 | 59–60 | REINFORCES | SETTLED | Standard Dirac-matrix representation freedom and its gauging, correctly worked out. |
| pp.61 | 61 | REINFORCES | SETTLED | Restated, correct Standard Model weak-interaction facts. |
| pp.62-72 | 62–72 | CONFLICTS-DATA | SETTLED | The section's explicit premise — build electroweak gauge-boson masses without a dynamical Higgs field — is exactly the question the 2012 Higgs discovery and its 2022 mass-coupling-proportionality confirmation answered directly; the internal gauge-theory algebra explored along the way (Weinberg-angle relation, mass-matrix reconciliation) is itself correct and standard, and one build (the critique of dropping $\nu_R$) is a genuinely prescient structural observation given what the field has since learned about neutrino mass. |
| pp.73-74 | 73–74 | IMPROVES | ACTIVE | The helical/zitterbewegung-style mass model, once a genuine algebra slip is corrected, exactly reproduces the standard relativistic group-velocity formula — and the broader "mass from internal helical motion at $c$" idea is a real, still-debated (2025) minority research tradition, not a 2007-era curiosity the field has dropped. |
| pp.75 | 75 | REINFORCES | SETTLED | Accurately transcribed 1990s-era electroweak precision data, largely still valid — with one instructive post-2007 wrinkle (the 2022 CDF W-mass anomaly and its 2024 resolution) that this exact quantity later went through. |
| pp.76 | 76 | REINFORCES | SETTLED | Standard, correctly quoted Majorana-mass/Fermi-theory/V−A textbook material. |

## What the field learned since 2007 that matters for this batch
- **The Higgs boson was discovered (2012) and its couplings shown to track particle mass across
  three orders of magnitude (2018 preliminary, 2022 definitive).** This is the single most
  consequential fact for pp.62-72: a genuinely dynamical scalar exists, and its interaction
  strength with each particle is proportional to that particle's mass exactly as the Higgs
  mechanism (and nothing else known) predicts — direct evidence against any construction that
  generates gauge-boson and fermion masses by hand, with no dynamical scalar at all. [A detailed map of Higgs boson interactions by the ATLAS experiment ten years after the discovery (*Nature* 607, 52-59, 2022)](https://www.nature.com/articles/s41586-022-04893-w) [A]
- **"Higgsless" electroweak model-building became a real, named, and ultimately disfavored research
  program between 2003–2012** (extra-dimensional unitarization via new spin-1 resonances, no
  fundamental scalar) — precisely the kind of explicit alternative this notebook explores a
  simplified version of — and the 2012 discovery is explicitly recorded in the literature as having
  "posed significant challenges" that pure Higgsless constructions have not overcome. [Electroweak Symmetry Breaking and the Higgs Boson (arXiv:1512.08749, 2015 review)](https://arxiv.org/pdf/1512.08749) [B]
- **Neutrino mass (already established by 1998–2001 oscillation experiments, well before this
  notebook was written) still has no settled explanation for whether it requires a right-handed
  neutrino at all** — the Dirac/Majorana question. Direct-search limits keep tightening: the
  combined LEGEND-200 + GERDA + Majorana Demonstrator 2025 result gives an observed half-life
  bound $T_{1/2}>1.9\times10^{26}$ years (90% CL; the projected sensitivity was $2.8\times10^{26}$
  years) on neutrinoless double-beta decay in $^{76}$Ge, still finding no evidence either way. [First Results on the Search for Lepton Number Violating Neutrinoless Double Beta Decay with the LEGEND-200 Experiment (*Phys. Rev. Lett.*, 2025; arXiv:2505.10440)](https://arxiv.org/pdf/2505.10440) [A]
- **The W-boson mass itself became a genuine post-2007 precision-physics story.** CDF's 2022
  measurement disagreed with the Standard Model prediction by about 7σ; independent 2024 ATLAS and
  CMS measurements came back consistent with the SM, substantially resolving the tension. [W mass snaps back (*CERN Courier*, 2024, summarizing the 2024 ATLAS/CMS results)](https://cerncourier.com/a/w-mass-snaps-back/) [B]; [PDG 2025 review: Mass and Width of the W Boson](https://ccwww.kek.jp/pdg/2025/reviews/rpp2025-rev-w-mass.pdf) [A]
- **Zitterbewegung-style "mass from internal helical/circular motion at $c$" electron models
  remain a live, if minority, foundational-physics research topic**, with a 2025 peer-reviewed
  critical review assessing several such models' compatibility with Dirac theory, special
  relativity and data. [Critical Review of Zitterbewegung Electron Models (Fleury & Rousselle, *Symmetry* 17, 360, 2025)](https://www.mdpi.com/2073-8994/17/3/360) [B]

## Per-build verdicts

### NB-075 (p.57) — Sakurai Textbook Insert
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim (field terms):** none — a photocopied reference page, not the author's own work.
- **Anchor:** none.
- **Verdict:** NEUTRAL · SETTLED

### NB-076, NB-077, NB-078 (pp.59–60) — Dirac Matrix Non-Uniqueness and Gauging
- **Checked against:** reconstruction status `SOLID` (all three)
- **Claim (field terms):** the standard Dirac Clifford algebra $\{\alpha_i,\alpha_j\}=2\delta_{ij}I$,
  $\{\alpha_i,\beta\}=0$ admits a continuous family of equivalent representations (any
  $\beta=(a\sigma_1+b\sigma_2)\otimes\sigma_0$ with $a^2+b^2=1$), and this freedom survives a local
  phase ("gauge") transformation on one tensor factor.
- **Anchor:** foundations — representation freedom of the Dirac algebra, a standard structural fact
  (the specific matrix representation chosen for $\gamma$-matrices is a convention, not physics —
  Dirac, Weyl, Majorana representations are all unitarily equivalent).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — unchanged since the 1920s-30s.

### NB-079 (p.61) — Weak Interaction Facts
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** $W^\pm,Z$ couple only to left-handed fermions (in the massless limit);
  the photon couples to electric charge; a mass term requires mixing left- and right-handed
  components.
- **Anchor:** electroweak foundations — the chiral structure of the SM's gauge couplings and the
  mass mechanism, standard and unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-080 (p.62) — Weinberg–Salam Lagrangian Without a Higgs Field
- **Checked against:** reconstruction status `SOLID` (as a correctly-assembled gauge-theory
  framework; the reconstruction explicitly notes the author's own stated intent is to explore what
  happens *without* a dynamical Higgs mechanism generating the mass terms)
- **Claim (field terms), structural:** the $SU(2)\times U(1)$ field strengths and covariant
  derivatives are correctly assembled.
- **Claim (field terms), physical premise:** electroweak gauge-boson (and fermion) masses can be
  generated by explicit, hand-inserted (non-dynamical) mass terms rather than by spontaneous
  symmetry breaking of a scalar field.
- **Anchor:** Higgs sector / electroweak symmetry breaking — is a fundamental scalar field required
  to generate SM particle masses, or can the SM's masses arise without one? In 2007 this was a
  genuinely open experimental question (the Higgs boson was undiscovered).
- **Current status:** a scalar resonance with mass $125.20\pm0.11\,\text{GeV}$ was discovered in
  2012 and its couplings to $W$, $Z$, top, bottom, tau, and (emerging) muon confirmed proportional
  to each particle's mass across three orders of magnitude, at roughly 5-12% precision per channel
  — exactly the signature a dynamical Higgs mechanism predicts and no purely explicit-mass-term
  construction predicts on its own. [A detailed map of Higgs boson interactions (*Nature* 607, 2022)](https://www.nature.com/articles/s41586-022-04893-w) [A]
- **Live work:** the general question of *why* electroweak symmetry breaks the way it does (is the
  Higgs elementary or composite? see the pp.5-6 cross-check) remains open and active, but the much
  narrower question this build's stated premise addresses — can EWSB be achieved with **no**
  dynamical scalar at all — is not a live mainstream line; "Higgsless" model-building as a distinct
  program was active roughly 2003–2012 and has not recovered a compelling candidate since the
  discovery. [Electroweak Symmetry Breaking and the Higgs Boson (arXiv:1512.08749, 2015)](https://arxiv.org/pdf/1512.08749) [B]
- **Verdict:** REINFORCES · SETTLED (the gauge-theory framework itself, correctly assembled) /
  **CONFLICTS-DATA** · SETTLED (the specific premise of generating masses with no dynamical Higgs
  field at all)
- **Hindsight:** in 2007 "explore EWSB without a Higgs" was a live, reasonable thing to try — it is
  exactly what a real, named research program (Higgsless models) was doing in parallel at the time.
  The single most consequential thing the field learned since is that nature did not go that route:
  a dynamical scalar is there, and it behaves like the textbook Higgs, not like an ad hoc mass
  insertion. This does not mean every individual algebraic step in pp.62-72 is wrong — most of them
  are correct, standard gauge-theory bookkeeping, as graded per-build below — only that the
  section's organizing premise has since been tested and found not to describe nature.

### NB-081 (p.62) — Critique of Dropping $\nu_R$
- **Checked against:** reconstruction status `SOLID` (accurate structural observation)
- **Claim (field terms):** the minimal SM's choice to omit a right-handed neutrino field (and treat
  $e_R$ as an isospin singlet with no left-right doublet partner) breaks the manifest
  left-right/doublet symmetry between the lepton and "neutrino" sectors, and is a physical
  assumption (neutrinos exactly massless), not a symmetry requirement.
- **Anchor:** neutrino sector — whether right-handed neutrinos exist (and, if neutrino mass is
  Majorana rather than Dirac, whether they are even needed) is a recognized, still-open SM
  extension question, sharpened considerably since 2007 even though the underlying fact (neutrinos
  have mass) was already established by 1998-2001 oscillation data.
- **Current status:** neutrino mass is confirmed (oscillation data); the absolute mass scale is now
  bounded below ~0.45 eV (KATRIN, 90% CL) and the Dirac-vs-Majorana question remains fully open,
  with no confirmed detection of neutrinoless double-beta decay as of 2025.
- **Live work:** yes — LEGEND-200 (2025, observed bound $T_{1/2}>1.9\times10^{26}$ yr at 90% CL),
  nEXO, and related experiments are actively searching, with continuously improving half-life
  bounds. [First Results ... LEGEND-200 (*PRL*, 2025)](https://arxiv.org/pdf/2505.10440) [A]
- **Verdict:** IMPROVES · ACTIVE (correctly identifies a real structural gap in the minimal SM —
  whether $\nu_R$/right-handed neutrino structure exists — that the field has since confirmed is
  physically necessary in some form once neutrino mass is taken seriously, even though the specific
  form, Dirac or Majorana, is unresolved)
- **What would decide it:** a positive neutrinoless double-beta decay signal (would establish
  Majorana nature, disfavoring a simple $\nu_R$ addition as the whole story) versus continued null
  results pushing the bound higher, combined with direct mass-scale measurements (KATRIN, Project 8).
- **Hindsight:** the author's 2007 objection ("destroys the basic symmetry... stupid") reads, with
  hindsight, less like a stylistic complaint and more like an early instance of exactly the
  structural argument that motivates every serious neutrino-mass extension of the SM today (seesaw
  models, left-right symmetric models) — though the notebook itself does not develop this into a
  specific testable mechanism here.

### NB-082, NB-083 (pp.63–64) — Weinberg-Angle Relation; a Located and Fixed Sign Error
- **Checked against:** reconstruction status `SOLID` (the $g'/g=\tan\theta$ and $e=2g\sin\theta$
  results) / `SOLID-WITH-CORRECTION` (the $\beta$ formula, sign corrected by the reconstruction)
- **Claim (field terms):** the $W^3$-$B$ mixing rotation that defines the physical $Z$ and photon
  fields requires $g'/g=\tan\theta_W$ (for the photon to decouple from $\nu_L$) and
  $e=2g\sin\theta_W$ (for the photon's coupling to $e_L$ to equal the electric charge) —
  both standard, textbook electroweak relations.
- **Anchor:** electroweak foundations — the Weinberg-angle relations connecting $g,g',\theta_W,e$,
  completely standard and unchanged.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — these relations are unchanged since Glashow-Weinberg-Salam (1960s-70s).

### NB-084 (pp.65–66) — Two $m_Z^2$ Formulas, Reconciled
- **Checked against:** reconstruction status `SOLID` (upgraded from a provisional NEEDS-WORK; both
  formulas confirmed, and the apparent tension between them fully explained)
- **Claim (field terms):** treating $W^3,W^0$ as independently massive gives an extra
  photon-$Z$ mixing term that must vanish for electromagnetism to stay unbroken; demanding that
  vanish (photon massless by construction) reproduces the standard $m_Z^2=m_W^2/\cos^2\theta_W$.
- **Anchor:** electroweak foundations — this is, in effect, a from-scratch illustration of *why* a
  single Higgs-doublet vacuum expectation value gives exactly one massless (photon) and one massive
  ($Z$) eigenvalue automatically, whereas positing gauge-boson masses independently does not
  guarantee this and leaves an unwanted cross-term to explain away by hand.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none for the relation itself; this build is, incidentally, a clean internal
  illustration of exactly why NB-080's "masses without a Higgs" premise runs into trouble —
  matching what the field's subsequent data confirmed (see NB-080 above).

### NB-085 (p.67) — Isospin/Spin Coupling Projector (Sign Error Found)
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
- **Claim (field terms):** none in SM/GR terms beyond what NB-082-084 already cover — an internal
  sign slip in a projection-matrix identity ($\tfrac12(\tau_0+\tau_3)$ should be
  $\tfrac12(\tau_0-\tau_3)$ for the stated projector), corrected by the reconstruction.
- **Anchor:** none distinct from the surrounding builds (pure matrix-identity bookkeeping).
- **Verdict:** NEUTRAL · SETTLED

### NB-086 (p.67) — Chiral Structure of the Mass Term
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** $\bar\psi\psi=\bar\psi_L\psi_R+\bar\psi_R\psi_L$ — a Dirac mass term only
  connects opposite-chirality components.
- **Anchor:** foundations — standard, load-bearing SM fact (this is exactly why a chiral gauge
  theory like the SM cannot simply write down fermion mass terms without something that connects
  $L$ and $R$, motivating the Higgs Yukawa mechanism).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none.

### NB-087, NB-089 (pp.68, 70) — Kinetic-Term Bookkeeping Hazard; Self-Abandoned Notation
- **Checked against:** reconstruction status `SOLID` (accurate self-critique) / `DEAD-END-AUTHOR-CALLED-IT`
- **Claim (field terms):** none distinct — standard multi-gauge-group Lagrangian bookkeeping
  hazards, correctly self-diagnosed and abandoned by the author.
- **Anchor:** none beyond NB-080's general framework.
- **Verdict:** NEUTRAL · SETTLED

### NB-088, NB-090, NB-092 (pp.69, 71, 72) — Proposed $B_\mu$ Neutral-Current Field; $\mu$-Decay Speculation
- **Checked against:** reconstruction status `NOT-TESTABLE` / `SOLID` (construction) / `NOT-TESTABLE`
- **Claim (field terms):** a speculative second $U(1)$ field introduced ad hoc to generate neutral
  currents and, later, to mediate muon decay, with no propagator or amplitude worked out.
- **Anchor:** none sharp enough to check against external physics — these are self-acknowledged
  sketches, not closed claims (the SM's actual $Z$ boson, arising from the same $W^3$-$B$ mixing
  already checked at NB-082-084, is of course the real mechanism, but that is not what these builds
  themselves assert or test).
- **Verdict:** NEUTRAL · SETTLED

### NB-091 (pp.71–72) — Dynamical $W$ Exchange Required for $\mu$ Decay, Not a Mass-Like Contact Term
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** a process like $\mu^-\to e^-+\bar\nu_e+\nu_\mu$, which changes particle
  flavor content across four external legs, requires a genuinely dynamical (propagating)
  intermediate boson, not merely a static two-point mass-like term.
- **Anchor:** electroweak foundations — this is exactly the historical logic that moved the field
  from Fermi's point-like 4-fermion contact theory to the intermediate vector boson picture (W
  boson), confirmed directly by the 1983 UA1/UA2 discovery of the $W$ and $Z$.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none — this reasoning has been settled, confirmed physics since 1983.

### NB-093, NB-094, NB-095 (pp.73–74) — Helical-Motion Mass Model: Error Found, Corrected to a
### Standard (and Independently Live) Result
- **Checked against:** reconstruction status `SOLID` (NB-093) / `DEAD-END-AUTHOR-CALLED-IT`
  (NB-094, unchanged) / `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION` (NB-095, upgraded from
  a provisional NEEDS-WORK)
- **Claim (field terms):** modeling a particle as moving at fixed speed $|\vec v|=c$ along a helix,
  with rest mass related to the helix's rotation frequency, and asking what the *forward* (group)
  velocity is once relativistic momentum is used correctly. The notebook's own algebra, once a
  dropped factor of $c^2$ is corrected, gives $v^2=c^2(1-E_0^2/E^2)$.
- **Anchor:** foundations / electron structure — (1) the corrected formula is exactly the standard
  relativistic group-velocity relation $v_{\rm group}=c\sqrt{1-E_0^2/E^2}=dE/dp$, unchanged
  textbook SR; (2) the broader motivating idea — that a particle's rest mass/inertia arises from an
  internal helical or circular motion at the speed of light — is the "zitterbewegung" family of
  electron models (going back to Schrödinger 1930, revived by Hestenes and others), a genuine,
  still-active foundational-physics research topic, not mainstream SM physics but not excluded by
  data either (it is explicitly built to reduce to standard Dirac-equation predictions).
- **Current status:** the corrected kinematic formula is unchanged, standard SR; the zitterbewegung
  electron-structure program remains a minority topic under active methodological debate.
- **Live work:** yes — a February 2025 peer-reviewed critical review assesses multiple current
  zitterbewegung electron models against Dirac theory, SR, and data, finding a mix of strengths and
  limitations rather than outright exclusion. [Critical Review of Zitterbewegung Electron Models (*Symmetry* 17, 360, 2025)](https://www.mdpi.com/2073-8994/17/3/360) [B]
- **Verdict:** REINFORCES · SETTLED (the specific corrected kinematic formula, which is just
  standard SR) / **IMPROVES** · ACTIVE (the broader "mass from internal helical motion at $c$"
  idea this build's ansatz instantiates)
- **What would decide it:** no sharp, near-term distinguishing experimental test is identified in
  the current literature for zitterbewegung-type electron-structure models generally; they are
  assessed on internal consistency with Dirac theory and SR, per the 2025 review.
- **Hindsight:** the author's own "way way — no good" self-doubt was well-placed (there was a real
  algebra error), but the underlying physical picture he was reaching for is not a 2007-era dead
  end — it is a specific instance of a still-debated foundational research question about electron
  structure that the field has neither confirmed nor excluded.

### NB-096 (p.75) — Ferbel Reference Data
- **Checked against:** reconstruction status `SOLID` (accurate reference data, correctly transcribed)
- **Claim (field terms):** transcribed 1990s-era electroweak precision values, including
  $m_W=80.22\pm0.26\,\text{GeV}$, $m_Z=91.187\pm0.007\,\text{GeV}$, $\sin^2\theta_W=0.232\pm0.009$.
- **Anchor:** electroweak precision physics — standard reference quantities, most essentially
  unchanged, though $m_W$ specifically became the subject of a major post-2007 controversy.
- **Current status:** $m_Z=91.1876\,\text{GeV}$ (PDG) matches the quoted value closely;
  $\sin^2\theta_W\approx0.2312$ ($\overline{MS}$) is in the quoted value's neighborhood;
  $m_W$: the SM now predicts $m_W=80{,}353\pm6\,\text{MeV}$, close to (if slightly below) the
  quoted $80{,}220\pm260\,\text{MeV}$, both well within the same ballpark.
- **Live work / hindsight:** $m_W$ went through a genuine post-2007 scare — CDF's 2022 measurement
  disagreed with the SM prediction by roughly 7σ, the most serious electroweak precision anomaly in
  decades — before independent 2024 ATLAS and CMS measurements came back consistent with the SM,
  substantially resolving the tension. This is exactly the kind of thing the notebook (2007) could
  not have anticipated either way; the reference table it transcribed turned out to sit
  comfortably within the range the field eventually settled back on. [W mass snaps back (*CERN Courier*, 2024)](https://cerncourier.com/a/w-mass-snaps-back/) [B]; [PDG 2025 W-boson mass review](https://ccwww.kek.jp/pdg/2025/reviews/rpp2025-rev-w-mass.pdf) [A]
- **Verdict:** REINFORCES · SETTLED

### NB-097, NB-098 (p.76) — Majorana Mass Structure; Fermi Theory; V−A
- **Checked against:** reconstruction status `SOLID` (both)
- **Claim (field terms):** standard Majorana mass-matrix structure; Fermi coupling
  $G_F=1.167\times10^{-5}\,\text{GeV}^{-2}$; V$-$A weak current structure.
- **Anchor:** electroweak/neutrino foundations — $G_F$ is unchanged, precisely measured
  ($1.1664\times10^{-5}\,\text{GeV}^{-2}$, PDG); V$-$A structure is confirmed, foundational SM
  physics. The Majorana mass-matrix structure quoted here is the same structural question flagged
  as ACTIVE at NB-081/the batch-level bullets (is neutrino mass Dirac or Majorana) — not re-graded
  separately here to avoid double-counting.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none beyond what NB-081 already covers for the Majorana question.

## Reconstruction queries
None. All corrections the reconstruction made in this stretch (the NB-083 $\beta$ sign, the
NB-085 projector sign, the NB-095 dropped $c^2$ factor) are independently confirmed consistent with
standard electroweak theory and special relativity respectively.

## Handoff items raised (mirrored into the handoff file)
One item — see `notebook-sm-crosscheck-handoff.md` §A (a question about whether the model's own
route to gauge-boson/fermion mass, which per CLAUDE.md decision 3 avoids a Higgs field entirely via
hypercharge on $U(x)$, has ever been checked against the 2012+/2022 Higgs-discovery evidence this
cross-check surfaces for NB-080 — since that evidence is exactly the kind of thing a "no elementary
Higgs" construction needs to account for, whatever its specific mechanism).

## Contamination log
None. This run drew only on the two reconstruction files and the sources cited above, fetched
in-session.

## Appendix — search queries used
- "Higgsless electroweak symmetry breaking models excluded LHC Higgs discovery 2012 status 2020"
- "ATLAS CMS combined Higgs coupling mass proportionality measurement 2022 precision"
- (WebFetch) atlas.cern/updates/briefing/combined-measurements-higgs-boson
- "ATLAS Nature 2022 \"detailed map of Higgs boson interactions\" ten years discovery paper"
- "CDF 2022 W boson mass anomaly measurement tension ATLAS CMS 2024 resolution combined value"
- "zitterbewegung electron helical motion mass model Hestenes review 2020 2023"
- "neutrinoless double beta decay Majorana neutrino search 2023 2024 experiment status LEGEND nEXO"
- "\"Critical Review of Zitterbewegung Electron Models\" Symmetry 2025 conclusion abstract"

## Sources
- [A detailed map of Higgs boson interactions by the ATLAS experiment ten years after the discovery (*Nature* 607, 52-59, 2022)](https://www.nature.com/articles/s41586-022-04893-w) [A]
- [Electroweak Symmetry Breaking and the Higgs Boson (arXiv:1512.08749, 2015 review)](https://arxiv.org/pdf/1512.08749) [B]
- [First Results on the Search for Lepton Number Violating Neutrinoless Double Beta Decay with the LEGEND-200 Experiment (*Phys. Rev. Lett.*, 2025; arXiv:2505.10440)](https://arxiv.org/pdf/2505.10440) [A]
- [W mass snaps back (*CERN Courier*, 2024)](https://cerncourier.com/a/w-mass-snaps-back/) [B]
- [PDG 2025 review: Mass and Width of the W Boson](https://ccwww.kek.jp/pdg/2025/reviews/rpp2025-rev-w-mass.pdf) [A]
- [Critical Review of Zitterbewegung Electron Models (Fleury & Rousselle, *Symmetry* 17, 360, 2025)](https://www.mdpi.com/2073-8994/17/3/360) [B]
