# Notebook × SM Cross-Check — pp. 1–2: Quantum Scalars I

*2026-09-22 - 20:52 · checks `notebook-reconstruction-01-scalar-qft-opening.md` (NB-001–003 only;
the rest of batch 01 — pp.3, pp.5-6, pp.7, pp.9-11 — is a separate ledger row and not covered by
this run) · protocol `notebook-sm-crosscheck-protocol.md`*
**Cold-checked:** 2026-09-22, 0 verdicts (no CONFLICTS or IMPROVES tags in this run, so no cold
check was owed; see §6 of the protocol)

## Summary
| Section | Pages | SM relation | Field status | One line |
|---|---|---|---|---|
| pp.1-2 | 1–2 | REINFORCES | SETTLED | Free-scalar canonical quantization, exactly standard; one scratch-page normalization slip, no physics content either way. |

## What the field learned since 2007 that matters for this batch
- The Higgs boson was discovered (2012) and its mass measured to 0.2% precision,
  $m_H = 125.09 \pm 0.21\,\text{GeV}$ (ATLAS+CMS Run‑1 combination) — the first time a *fundamental*
  scalar field (as opposed to a scalar order parameter like the superconducting gap) has been
  directly observed. It obeys the same real-scalar kinetic/mass structure NB‑001 writes down (each
  of the Higgs doublet's four real components starts life as exactly this Lagrangian before
  electroweak symmetry breaking). [PDG 2025 Higgs boson listing (Particle Data Group)](https://pdg.lbl.gov/2025/listings/rpp2025-list-higgs-boson.pdf) [A]
- Whether the *free* (non-interacting) real scalar field is the only rigorously well-defined limit of
  scalar QFT in 4D was tightened considerably after 2007: Aizenman and Duminil-Copin proved
  (2021, *Annals of Mathematics*) that the continuum scaling limit of the critical 4D Ising/$\lambda\phi^4$
  model is Gaussian — i.e. "trivial," with no surviving interaction — extending the older
  Aizenman/Fröhlich hyperscaling arguments to a full proof. [Marginal triviality of the scaling limits of critical 4D Ising and λφ⁴ models (Aizenman & Duminil-Copin, *Ann. of Math.* 194(1), 2021)](https://projecteuclid.org/journals/annals-of-mathematics/volume-194/issue-1/Marginal-triviality-of-the-scaling-limits-of-critical-4D-Ising/10.4007/annals.2021.194.1.3.short) [B]
- That triviality result was itself found to rest on an assumption (positivity of the UV scalar
  self-coupling) that a 2023 preprint showed is not universal — so "is 4D $\phi^4$ QFT trivial"
  remains open at the edges even though the mainline case is closed. [A loophole in the proofs of asymptotic freedom and quantum triviality (arXiv:2310.18414, 2023)](https://arxiv.org/html/2310.18414) [C]
- None of the above bears on NB‑001/003 directly, because the notebook's field here is strictly
  *free* ($\mathcal L=\tfrac12(\partial\phi)^2-\tfrac12m^2\phi^2$, no $\lambda\phi^4$ term) — the free
  theory was already rigorously constructed decades before 2007 and triviality is a statement about
  the *interacting* continuum limit. It is relevant context for later builds in this notebook that do
  propose self-interacting scalar sectors (flagged in the handoff below).

## Per-build verdicts

### NB-001 (p.1) — KG Lagrangian and Hamiltonian for a Real Scalar Field
- **Checked against:** reconstruction status `SOLID`
- **Claim (field terms):** A free real scalar field obeying the Klein–Gordon equation follows from
  $\mathcal L=\tfrac12(\partial^\mu\phi)(\partial_\mu\phi)-\tfrac12m^2\phi^2$ by the Euler–Lagrange
  equations, with canonical momentum $\pi=\dot\phi$ and Hamiltonian density
  $\mathcal H=\tfrac12(\pi^2+(\nabla\phi)^2+m^2\phi^2)$.
- **Anchor:** foundations — the canonical (Lagrangian → Hamiltonian) formulation of a free
  relativistic scalar field; the base construction every SM field theory is built from (each
  component of the Higgs doublet reduces to exactly this before electroweak symmetry breaking).
- **Current status:** unchanged textbook content; e.g. [Tong, *Quantum Field Theory* lecture notes, §2](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html) [D] gives the identical Lagrangian, EL equation and Legendre transform.
- **Live work:** none — this is closed, foundational mathematics, not an open research question.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** Nothing that changes this specific construction. The 2012 Higgs discovery is the
  closest thing to "news" for a real scalar field, and it *confirms* rather than revises this
  formalism — see the batch-level bullet above.

### NB-002 (p.1 vs p.42, NB-049) — Fourier-Mode Convention
- **Checked against:** reconstruction status `INCORRECT (as transcribed) / SOLID-WITH-CORRECTION`
- **Claim (field terms):** normalization convention for the momentum-space expansion of a free
  scalar field, $\phi_k\propto(2\omega_k)^{-1/2}\widehat\phi(k)$ — the standard relativistically
  normalized mode convention used before introducing ladder operators.
- **Anchor:** none. This is bookkeeping — a $(2\pi)$-power/normalization choice, not a physical
  prediction or structural requirement. Per protocol §4a, builds with no anchor go straight to
  NEUTRAL rather than being stretched to fit REINFORCES.
- **Current status:** n/a (notational convention, not a measured or theorem-level claim).
- **Live work:** n/a.
- **Verdict:** NEUTRAL · SETTLED
- **Hindsight:** Nothing relevant — this is a page-1 scratch-page slip in a $(2\pi)^{3/2}$ power
  that the notebook's own author catches and fixes 40 pages later (NB-049); it never entered any
  physical result. No amount of post-2007 physics bears on which power of $2\pi$ belongs in a
  Fourier convention.

### NB-003 (pp.1–2) — H in k-Space, Continued to a Closed Form
- **Checked against:** reconstruction status `SOLID` (unfinished in the notebook, closed by the
  reconstruction and shown to match the author's own later redo at p.43/NB-050)
- **Claim (field terms):** substituting the Fourier-mode expansions of $\pi,\phi,\nabla\phi$ into
  $H=\int\mathcal H\,d^3x$ and performing the $x$-integral collapses the double $k,p$ integral, via
  momentum-conserving delta function, onto the standard normal-mode Hamiltonian
  $H=\tfrac12\int d^3k\,[\pi_k\pi_{-k}+(k^2+m^2)\phi_k\phi_{-k}]$ — the form that diagonalizes into
  $H=\sum_k\omega_k(a_k^\dagger a_k+\tfrac12)$ once ladder operators are introduced.
- **Anchor:** foundations — same construction as NB-001, one step further: the mode-diagonalization
  step of canonical quantization that produces the particle (Fock-space) interpretation.
- **Current status:** unchanged textbook content; matches, e.g., the derivation in [Tong, §2.3](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html) [D] once the standard convention (not the p.1 scratch convention) is used.
- **Live work:** none.
- **Verdict:** REINFORCES · SETTLED
- **Hindsight:** Nothing relevant beyond the batch-level note above; this remains the standard route
  from a classical free-field Hamiltonian to its diagonal (particle) form, untouched by any 2007+
  development.

## Reconstruction queries
None. The reconstruction's own verdicts on NB-001–003 (SOLID, SOLID-WITH-CORRECTION, SOLID) are
consistent with the external record and are not disputed here.

## Handoff items raised (mirrored into the handoff file)
One paste-ready research prompt raised — see `notebook-sm-crosscheck-handoff.md` §B, item 1 — on
whether the model's own self-interacting scalar sector(s) (e.g. the $E_g$ sextic clock coupling)
sit anywhere near the 4D scalar-triviality literature this batch surfaced. Not a claim about the
model; the cross-check has not looked at the model's derivation, per §2.3 of the protocol.

## Contamination log
None. NB-001–003 are outside the contamination window the reconstruction flagged for this batch
(that note applies only to NB-007–009); no model-internal file was read to form these verdicts.

## Appendix — search queries used
- "canonical quantization free scalar field Klein-Gordon textbook standard 2020 review"
- "Aizenman Duminil-Copin proof triviality phi^4 four dimensions 2021"
- "PDG 2024 Higgs boson mass value GeV combined ATLAS CMS"

## Sources
- [Tong, *Quantum Field Theory* lecture notes (Cambridge), §2 "Free Fields"](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html) [D]
- [PDG 2025 Higgs boson listing (Particle Data Group)](https://pdg.lbl.gov/2025/listings/rpp2025-list-higgs-boson.pdf) [A]
- [Aizenman & Duminil-Copin, "Marginal triviality of the scaling limits of critical 4D Ising and λφ⁴ models," *Annals of Mathematics* 194(1), 2021](https://projecteuclid.org/journals/annals-of-mathematics/volume-194/issue-1/Marginal-triviality-of-the-scaling-limits-of-critical-4D-Ising/10.4007/annals.2021.194.1.3.short) [B]
- ["A loophole in the proofs of asymptotic freedom and quantum triviality," arXiv:2310.18414 (2023)](https://arxiv.org/html/2310.18414) [C]
