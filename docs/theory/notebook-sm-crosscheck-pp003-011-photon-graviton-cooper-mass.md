# Notebook × SM Cross-Check — pp. 3–11: Photon/Graviton Spin Structure, Superconductivity
# Analogy, Mass-from-Field-Energy

*2026-09-22 - 21:05 · checks `notebook-reconstruction-01-scalar-qft-opening.md` (NB-004–013;
NB-001–003, pp.1-2, were checked in a separate prior run) · protocol
`notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 2 verdicts (NB-009 IMPROVES, NB-013 CONFLICTS-DATA), 1 changed (NB-009's
Higgs-mass citation was the 2015 Run-1 combination, not PDG 2025's current headline average; fixed
to $125.20\pm0.11$ GeV; the compositeness-scale range was widened to match Khosa et al.'s reported
0.6–1.3 TeV spread). All other citations (composite-Higgs 2023/2022/2021 sources, lepton masses and
ratio) confirmed correct by an independent subagent with no access to this write-up's reasoning.

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.3 | 3 | REINFORCES | SETTLED | Photon-antisymmetric/graviton-symmetric is standard spin-1/spin-2 field theory; the tetrahedron/octahedron isomer counts are pure combinatorics with no SM anchor. |
| pp.5-6 | 5–6 | IMPROVES | ACTIVE | Paired-fermion photon is a genuine (minority, dormant) literature; "Higgs as Cooper pair" lands squarely on the live composite-Higgs research program addressing the naturalness problem. |
| pp.7 | 7 | NEUTRAL | SETTLED | Chemistry data table, verified accurate; out of SM scope. |
| pp.9-11 | 9–11 | CONFLICTS-DATA | SETTLED | EM energy density and the point-charge self-energy divergence are exactly standard; the specific "more interactions ⇒ more mass" ordering claim is cleanly falsified by same-interaction charged-lepton generations, even though the deeper mass-from-field-energy intuition is vindicated for hadrons by 2018 lattice QCD. |

## What the field learned since 2007 that matters for this batch
- **Composite Higgs / naturalness (pp.5-6, NB-009).** The Higgs boson's discovery (2012) opened
  the question the SM cannot itself answer — is it elementary, or a bound state of some new strong
  dynamics? — as a live, quantitative research program (pseudo-Nambu-Goldstone-boson composite
  Higgs models), specifically motivated by the naturalness/hierarchy problem. Global Bayesian fits
  against full LHC Run‑2 Higgs and resonance data find a compositeness scale bound of roughly
  $f\gtrsim0.6$–$1\,\text{TeV}$, not excluded. [Extending Global Fits of 4D Composite Higgs Models with Partially Composite Leptons (arXiv:2312.06027, 2023)](https://arxiv.org/pdf/2312.06027) [C]; [On the Impact of the LHC Run 2 Data on General Composite Higgs Scenarios (Khosa et al., *Adv. High Energy Phys.* 2022)](https://onlinelibrary.wiley.com/doi/10.1155/2022/8970837) [B]
- **Composite/paired-fermion photon (pp.5-6, NB-007).** Independently of this notebook, the
  "neutrino theory of light" (photon as a bound fermion–antifermion pair, de Broglie 1932, Jordan)
  was revived by W. A. Perkins through the 2010s with an explicit construction distinguishing a
  photon from its non-interacting "antiphoton." No paper on this specific line has appeared since
  ~2016 in general search; a 2016 response paper constrained Perkins' antiphoton-as-dark-matter
  application on cosmological grounds. [Composite Photon Theory Versus Elementary Photon Theory (Perkins, arXiv:1503.00661, 2015)](https://arxiv.org/pdf/1503.00661) [C]; [Constraints on the composite photon theory (*Mod. Phys. Lett. A* 31, 1675002, 2016)](https://ui.adsabs.harvard.edu/abs/2016MPLA...3175002L/abstract) [B]
- **Mass from field/binding energy (pp.9-11, NB-013).** The 2018 lattice-QCD decomposition of the
  proton's mass found that only ~9% comes from the quark (Higgs-Yukawa) masses themselves; the
  remaining ~90%+ comes from quark kinetic energy, gluon field energy, and the trace anomaly —
  i.e. the proton's mass is overwhelmingly *field energy*, essentially the modern, quantitative
  version of the intuition NB‑013 reaches for. [Proton Mass Decomposition from the QCD Energy‑Momentum Tensor (Yang et al., *Phys. Rev. Lett.* 121, 212001, 2018)](https://link.aps.org/pdf/10.1103/PhysRevLett.121.212001) [A]
- **Fermion mass hierarchy remains an open SM problem.** In contrast, the *inter-generation*
  hierarchy of elementary fermion masses (e.g. $m_\tau/m_e\approx3477$ for two leptons with
  *identical* gauge quantum numbers and interactions) is still explained by the SM only as a set of
  unexplained, freely-adjustable Yukawa couplings — there is no accepted derivation of it from
  first principles as of 2026. [PDG 2025 lepton summary table (masses)](https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf) [A]

## Per-build verdicts

### NB-004 (p.3) — "Photon Antisymmetric / Graviton Symmetric"
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the physical content of a massless spin-1 field is the antisymmetric
  field-strength 2-form $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$; the physical content of
  a massless spin-2 field is the symmetric metric perturbation $h_{\mu\nu}$.
- **Anchor:** foundations — structural (representation-theoretic) requirement on massless
  higher-spin fields, underlying both QED/electroweak gauge theory and linearized GR.
- **Current status:** unchanged structural fact; e.g. the general massless-spin-$s$ field-strength
  construction (spin-1 → 2-form, spin-2 → linearized Weyl tensor / symmetric $h_{\mu\nu}$) is
  standard higher-spin gauge theory. [Higher Spin Theory — Part I (Rahman, PoS Modave VIII 004)](https://pos.sissa.it/195/004/pdf) [C, lecture notes/proceedings — background for an uncontested structural fact]
- **Live work:** none — not an open question.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none relevant; unchanged since long before 2007.

### NB-005 (p.3) — Tetrahedron, 3 Particle Types, "Only 2" Isomers
- **Checked against:** reconstruction status `SOLID` (under the rotation-only reading)
- **Claim (field terms):** none in SM terms — this is a finite-group combinatorics exercise
  (edge-3-colourings of $K_4$ up to $A_4$) with a physical *motivation* (lattice connectivity for a
  hypothetical CA construction) but no SM-testable content itself.
- **Anchor:** none. Per protocol §4a, a build with no SM/GR anchor goes to NEUTRAL rather than
  being stretched.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a — pure combinatorics.

### NB-006 (p.3) — Octahedron, 2-Particle Case, "3 Only" Isomers
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim (field terms):** none recoverable (reconstruction could not reconstruct the specific
  counting rule from the transcription).
- **Anchor:** none.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-007 (p.5) — Spinor-Photon-Pair Mechanism
- **Checked against:** reconstruction status `SOLID-WITH-CORRECTION`
- **Claim (field terms):** the photon can be modeled as a bound state of two spin-½ fermions
  (helicity-correlated pair, $1/2\otimes1/2\to1\oplus0$), reproducing an effective spin-1 particle
  that "only occurs as a pair" (approximate, not exact, Bose statistics for the composite).
- **Anchor:** QED foundations — is the photon elementary (as in the SM) or composite? A genuine,
  long-standing alternative research line (neutrino theory of light: de Broglie 1932, Jordan;
  revived with an explicit modern construction by W. A. Perkins through the mid-2010s).
- **Current status:** the SM photon is elementary, confirmed to very high precision (no evidence of
  substructure in any QED process tested to date); composite-photon constructions are explicitly
  built to reproduce identical low-energy QED phenomenology, so they are not in tension with that
  precision record by design. [Composite Photon Theory Versus Elementary Photon Theory (Perkins, arXiv:1503.00661, 2015)](https://arxiv.org/pdf/1503.00661) [C]
- **Live work:** the specific 2015 construction's own most distinguishing prediction — an
  undetectable "antiphoton" serving as a dark-matter candidate — was directly constrained the
  following year on cosmological grounds (radiation-density and C-symmetry arguments); no paper
  in general search has continued this specific line since ~2016. [Constraints on the composite photon theory (*Mod. Phys. Lett. A* 31, 1675002, 2016)](https://ui.adsabs.harvard.edu/abs/2016MPLA...3175002L/abstract) [B]
- **Verdict:** REINFORCES · DORMANT (a non-standard route to standard QED phenomenology; live
  2010s, essentially inactive since ~2016 by this search)
- **Hindsight:** the specific correction the reconstruction already supplies (Pryce 1938: *exact*
  Bose statistics for the pair is impossible, so "only occurs as a pair" must mean
  *approximate/asymptotic* boson behavior, as for a Cooper pair) is the field's settled resolution
  of the objection the notebook's idea would otherwise run into. The one added post-2007 fact: the
  specific antiphoton/dark-matter extension Perkins built on this idea in 2015 looks disfavored by
  the 2016 cosmological-constraint paper — a data point the notebook's 2007 sketch could not have
  anticipated either way, since it never goes that far.

### NB-008 (pp.5–6) — Photon-as-Cooper-Pair Analogy; "Superconducting" Travel at c
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim (field terms):** none precise enough to check — no gap equation, order parameter, or
  scattering mechanism is specified for the proposed "vacuum superconductivity."
- **Anchor:** none specific enough to anchor to a named SM/GR prediction.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** the general *flavor* of this idea (vacuum behaving like a superfluid/condensate
  medium) is a genuine, still-active adjacent research area — superfluid-vacuum / analog-gravity
  programs (e.g. BEC analog-horizon experiments) — but NB-008 does not specify enough to connect to
  it as anything more than a loose family resemblance; not claimed here as support for the notebook
  build.

### NB-009 (p.6) — Higgs-as-Cooper-Pair; W/Z as Other Spinor-Photon States
- **Checked against:** reconstruction status `NOT-TESTABLE` (explicitly posed as open questions by
  the author)
- **Claim (field terms):** is the Higgs boson a composite bound state (a "Cooper pair" of more
  fundamental constituents) rather than an elementary scalar, and can the W/Z bosons be understood
  in the same paired-fermion framework as the photon?
- **Anchor:** Higgs sector / naturalness — whether the Higgs is elementary or composite is a
  recognized open question the SM cannot answer on its own, and the hierarchy/naturalness problem
  (why $m_H\ll M_{\rm Planck}$ without extreme fine-tuning) is exactly what composite-Higgs
  (pseudo-Nambu-Goldstone-boson) models are built to address.
- **Current status:** $m_H=125.20\pm0.11\,\text{GeV}$ (PDG 2025 world average, combining the 2015
  ATLAS+CMS Run-1 combination with newer ATLAS 2023 and CMS 2020 measurements), and current LHC
  Higgs-coupling data are consistent with an elementary SM Higgs to good precision, but do not rule
  out compositeness above roughly $f\gtrsim0.6$–$1.3\,\text{TeV}$ (scenario-dependent). [PDG 2025 Higgs boson listing](https://pdg.lbl.gov/2025/listings/rpp2025-list-higgs-boson.pdf) [A]
- **Live work:** composite/pNGB Higgs models remain an active, continuing research program with
  global fits against the full LHC dataset as recently as 2023, and dedicated projections for the
  HL-LHC. [Extending Global Fits of 4D Composite Higgs Models with Partially Composite Leptons (arXiv:2312.06027, 2023)](https://arxiv.org/pdf/2312.06027) [C]; [Probing composite Higgs boson substructure at the HL-LHC (arXiv:2105.01093, 2021)](https://arxiv.org/html/2105.01093) [B]
- **Verdict:** IMPROVES · ACTIVE
- **What would decide it:** direct measurement of Higgs self-coupling and precision di-Higgs rates
  at the HL-LHC (mid-2030s), and any discovery of the top-partner / vector resonances composite
  models predict near the TeV scale.
- **Hindsight:** in 2007 "is the Higgs composite" was an open theoretical curiosity with no data at
  all (the Higgs itself was undiscovered); it is now a quantitatively constrained open question with
  a specific excluded region and a specific future test. The notebook's very literal reading — a
  Cooper pair of the *same* paired spin-½ fermions posited for the photon (NB-007) — is not itself
  the mainstream construction (mainstream composite-Higgs models use new strongly-coupled
  constituents, not photon-building fermions), so this is graded as landing on the right *research
  question*, not a specific mainstream mechanism.

### NB-010 (p.7) — Heat-of-Combustion Table (chemistry aside)
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** none — a chemistry data table (combustion heats of alkanes), verified
  internally consistent by the reconstruction.
- **Anchor:** none — outside SM/GR/foundations scope entirely.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** n/a.

### NB-011 (p.9) — Sachs Motivation (narrative)
- **Checked against:** reconstruction status `NOT-TESTABLE`
- **Claim (field terms):** none — motivational prose introducing Mendel Sachs' unified
  electrogravity program, picked up in detail at pp.15-29 (batch 02, checked separately).
- **Anchor:** none in this build itself (deferred to batch 02's cross-check of the actual
  Lagrangian construction).
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** deferred to the pp.12-29 write-up, where Sachs' program's current standing is
  assessed directly.

### NB-012 (p.10) — EM Energy Density $\xi=\tfrac1{8\pi}(E^2+B^2)$
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** the electromagnetic field's energy density in Gaussian units is
  $\xi=\tfrac1{8\pi}(E^2+B^2)$, the $T^{00}$ component of the Maxwell stress-energy tensor.
- **Anchor:** QED/classical-EM foundations — the canonical stress-energy tensor of Maxwell theory,
  unchanged textbook physics (Jackson, *Classical Electrodynamics*, Ch. 6).
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** none relevant; classical result, untouched by any post-2007 development.

### NB-013 (p.11) — Point-Charge Self-Energy Divergence; Qualitative Mass Hierarchy
- **Checked against:** reconstruction status `NEEDS-WORK` (divergence itself SOLID; hierarchy claim
  explicitly non-quantitative per the author)
- **Claim (field terms), divergence:** the classical electrostatic self-energy of a point charge,
  $\int_{r_0}^\infty E^2\,dV=4\pi q^2/r_0$, diverges as the charge radius $r_0\to0$.
- **Claim (field terms), hierarchy:** particles with more distinct fundamental interactions
  (quarks: strong+weak+EM; charged leptons: weak+EM; neutrinos: weak only) should be qualitatively
  heavier, because each interaction contributes additional self-energy.
- **Anchor:** the divergence — QED foundations, the classical precursor to the electron
  self-energy problem QED renormalization solves. The hierarchy claim — the SM's fermion
  mass/flavor hierarchy, a recognized open problem (masses are free Yukawa parameters with no
  first-principles derivation).
- **Current status (divergence):** unchanged; the classical divergence is exactly why a point
  charge's self-energy needs regularization/renormalization in QED, standard textbook content.
- **Current status (hierarchy):** the *inter-family* ordering (quarks ≫ electron ≫ neutrinos) is
  qualitatively consistent with today's measured masses, but the mechanism proposed — mass set by
  *how many kinds* of interaction a particle has — is empirically falsified by the charged-lepton
  sector on its own: electron, muon and tau have **identical** SM gauge interactions (EM + weak
  only, no strong, for all three) yet span a factor of $\approx3477$ in mass
  ($m_e=0.511\,\text{MeV}$, $m_\tau=1776.93\,\text{MeV}$). Interaction *count* cannot be the
  mechanism if same-count particles differ by three and a half orders of magnitude. [PDG 2025 lepton summary table](https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf) [A]
- **Live work:** the flavor/mass-hierarchy puzzle itself remains an actively studied open SM
  problem (flavor symmetries, Froggatt-Nielsen-type models, extra dimensions), but none of that
  line rests on "interaction count," so it does not rescue the notebook's specific mechanism.
- **Verdict:** REINFORCES · SETTLED (the divergence) / **CONFLICTS-DATA** · SETTLED (the
  interaction-count mass-ordering mechanism, specifically)
- **Hindsight:** the notebook's deeper intuition — that mass can arise from a particle's field/
  binding energy rather than being a bare input — turns out to be *exactly* how most visible mass
  in the universe actually works, just not for the reason or the particles NB-013 names: 2018
  lattice QCD shows the proton's mass is only ~9% quark (Yukawa) mass, with the rest coming from
  quark kinetic energy, gluon field energy and the trace anomaly. That result vindicates
  "mass from field energy" as a real, dominant mechanism for *composite hadrons*; it says nothing
  about, and does not rescue, the *elementary*-fermion generation hierarchy NB-013 was reaching
  for, which is a separate and still-open problem. [Proton Mass Decomposition from the QCD Energy-Momentum Tensor (Yang et al., *Phys. Rev. Lett.* 121, 212001, 2018)](https://link.aps.org/pdf/10.1103/PhysRevLett.121.212001) [A]

## Reconstruction queries
None. All checked verdicts in this run (SOLID / SOLID-WITH-CORRECTION / NOT-TESTABLE) are
consistent with the external record.

## Handoff items raised (mirrored into the handoff file)
Two items — see `notebook-sm-crosscheck-handoff.md` §A (composite-Higgs / paired-photon
correlation question) and §C (none this run).

## Contamination log
None. This run drew only on the sources cited above, fetched in-session; no `findings/`,
`docs/claims/`, `src/`, or model-internal reference content was read.

## Appendix — search queries used
- "composite photon model exclusion limit fermion substructure photon compositeness bound 2020"
- "composite Higgs boson LHC Run 2 compositeness scale constraint 2023"
- "proton mass decomposition lattice QCD trace anomaly gluon field energy 2018"
- "Perkins composite photon neutrino theory of light 2020 2023 citations status"
- "composite photon theory Perkins 2022 2023 2024 arxiv new paper"
- "massless spin-1 antisymmetric field strength spin-2 symmetric metric perturbation gauge theory textbook citation"
- "composite Higgs pseudo-Nambu-Goldstone boson global fit 2024 2025 LHC constraints"
- "Constraints on the composite photon theory" Perkins Physics Letters arxiv

## Sources
- [Higher Spin Theory — Part I (Rahman, PoS Modave VIII 004)](https://pos.sissa.it/195/004/pdf) [C]
- [Composite Photon Theory Versus Elementary Photon Theory (Perkins, arXiv:1503.00661, 2015)](https://arxiv.org/pdf/1503.00661) [C]
- [Constraints on the composite photon theory (*Mod. Phys. Lett. A* 31, 1675002, 2016)](https://ui.adsabs.harvard.edu/abs/2016MPLA...3175002L/abstract) [B]
- [PDG 2025 Higgs boson listing (Particle Data Group)](https://pdg.lbl.gov/2025/listings/rpp2025-list-higgs-boson.pdf) [A]
- [Extending Global Fits of 4D Composite Higgs Models with Partially Composite Leptons (arXiv:2312.06027, 2023)](https://arxiv.org/pdf/2312.06027) [C]
- [On the Impact of the LHC Run 2 Data on General Composite Higgs Scenarios (Khosa et al., *Adv. High Energy Phys.* 2022)](https://onlinelibrary.wiley.com/doi/10.1155/2022/8970837) [B]
- [Probing composite Higgs boson substructure at the HL-LHC (arXiv:2105.01093, 2021)](https://arxiv.org/html/2105.01093) [B]
- [Proton Mass Decomposition from the QCD Energy-Momentum Tensor (Yang et al., *Phys. Rev. Lett.* 121, 212001, 2018)](https://link.aps.org/pdf/10.1103/PhysRevLett.121.212001) [A]
- [PDG 2025 lepton summary table (masses)](https://pdg.lbl.gov/2025/tables/rpp2025-sum-leptons.pdf) [A]
