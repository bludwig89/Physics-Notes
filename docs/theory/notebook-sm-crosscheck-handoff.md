# Notebook × SM Cross-Check — Handoff

*Questions and research prompts raised by the SM cross-check (`notebook-sm-crosscheck-protocol.md`)
that belong to someone else: the model (via the operator's correlation pass or a `/finding`
session) or the cold reconstruction. **Nothing here is answered by the cross-check.** Append-only;
mark an item `CLOSED → <where>` when it is dealt with, never delete it.*

Created: 2026-09-22.

---

## A. Questions for the model

*Where a notebook idea sits against the live SM in a way the model may inherit, share, or already
answer. Phrased as questions; the cross-check has not looked at the model.*

| # | From | Raised | Question | Why it matters | Status |
|---|---|---|---|---|---|
| 1 | pp.5-6 | 2026-09-22 | The live composite-Higgs literature (pNGB Higgs, naturalness) and the dormant paired-fermion composite-photon literature (Perkins) are structurally distinct research programs in the field (different constituents, different mechanisms) even though the notebook (NB-007/NB-009) reaches for both under one "spinor-photon-pair" umbrella. Does the model's own photon (F67-F69, paired-spinor photon) or its Higgs-avoidance route (decision 3, hypercharge on U(x)) draw any structural connection between the two, or are they independent in the model too — and if independent, is the notebook's original intuition (one mechanism, two applications) actually wrong, or just not how the model ended up building it? | Clarifies whether a 2007 intuition the model may have inherited in spirit (paired-fermion origin for gauge/Higgs-sector particles) was kept as one mechanism or split into unrelated ones, which matters for how the model's own paired-spinor photon findings (F67-F69) should be described relative to this notebook. | **CLOSED → `docs/theory/notebook-correlation-pass-2026-09-23.md`** (2026-09-23): independent in the model — the photon is a literal bound pair of propagating fermions (F69); hypercharge/mass is a gauge-field extension absorbed via Stueckelberg (F41/F44), no bound state of any kind. NB-009's literal "same pair, two applications" unification was never attempted, and per the cross-check's own hindsight isn't the mainstream composite-Higgs mechanism either. 
| 2 | pp.62-72 | 2026-09-22 | The model's route to gauge-boson and fermion mass (CLAUDE.md decision 3: hypercharge on $U(x)$, avoiding a Higgs field entirely) is a different mechanism than this notebook's explicit "masses without a dynamical Higgs field" ansatz (NB-080), but both share the property of not positing an elementary Higgs scalar. The 2012 Higgs discovery and its 2022 confirmation that Higgs-like couplings track particle mass across three orders of magnitude (Nature 607, 52-59, 2022) is exactly the kind of evidence any "no elementary Higgs" construction needs to account for. Has the model's own hypercharge-on-$U(x)$ mechanism been checked against this specific evidence — i.e. does it predict (or accommodate) a dynamical scalar resonance near 125 GeV with mass-proportional couplings, or does it explain that observed particle some other way? | Clarifies whether the model's Higgs-avoidance route has a specific, checked answer to the strongest piece of evidence against "masses with no dynamical scalar" constructions in general, or whether this is still an open gap. | **CLOSED → `docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md`** (2026-09-23): checked, and the answer is structural rather than numerical. The model has **no Yukawa mechanism anywhere** (F41: "F27... no Higgs Yukawa" — the fermion mass $m$ is a bare per-species parameter, structurally decoupled from the Stueckelberg gauge-mass scale $f=v/2$), so restoring the Stueckelberg radial mode would not automatically give the textbook mass-proportional coupling the way it would in a standard pNGB construction. The model's own candidate scalar (F73, the Cooper-pair singlet of the F69 photon pairing — this *is* NB-009 built out, contra this session's own earlier A.1 pass, corrected by addendum) has exact kinematics but no coupling-to-fermions construction of any kind, so the $\kappa$-framework signature cannot be tested against it yet — not an unfavorable result, a missing piece of machinery (flagged as a new open question, not resolved here). |

## B. Paste-ready research prompts

*For ideas tagged IMPROVES / ACTIVE where a concrete calculation or comparison against a live
measurement could be run. Each prompt is self-contained.*

1. **[pp.1-2, 2026-09-22]** The rigorous 2021 proof that the continuum limit of the 4D
   $\lambda\phi^4$ scalar field theory is trivial (Aizenman & Duminil-Copin, *Ann. of Math.*
   194(1), 2021 — Gaussian scaling limit, no surviving interaction; a 2023 preprint,
   arXiv:2310.18414, found the proof depends on a positivity assumption on the UV coupling that is
   not universal, so the result is closed for the mainline case but not airtight at the edges) is a
   structural constraint on any lattice/CA construction whose continuum limit produces a
   self-interacting real scalar sector. Prompt for a model session: does any of the model's scalar
   sectors — in particular the $E_g$ sextic clock coupling ($\lambda_6$, decision 7 / F234 /
   F253–F256) or the Higgs-avoidance route via hypercharge on $U(x)$ (decision 3) — take a
   continuum limit that is a $\lambda\phi^4$-type (or higher-order polynomial) scalar theory in 4D,
   and if so, does the triviality theorem constrain it (e.g. force the effective coupling to zero,
   or place it outside the theorem's scope because the lattice construction keeps a nonzero cutoff,
   or because the relevant field is not a genuine scalar order parameter in the Ising-universality
   sense)? This is a question about the model, not something this cross-check has evaluated.

2. **[pp.35-36, 2026-09-22]** Three genuinely active (2020s) research programs independently
   pursue the "dependency/rules define geometry, geometry/dimension emerges from a discrete
   structure" thesis this notebook states qualitatively at pp.35-36 (NB-043/044): causal set
   theory's Myrheim–Meyer dimension estimator (derives an effective spacetime dimension from a
   discrete causal-order relation), the Wolfram Physics Project (hypergraph rewriting rules
   claimed to generate emergent space, dimension, and GR/QM-like dynamics in a continuum limit),
   and 't Hooft's cellular-automaton interpretation of quantum mechanics (most recently, Elze
   2025, arXiv:2504.06883, deriving the Dirac equation and mass from permutations of discrete
   automaton states). Prompt for a model session: does the model's own emergent-dimensionality /
   lattice-choice reasoning (why BCC, why 3+1 dimensions specifically) draw on, parallel, or
   diverge from any of these three programs' specific arguments for how dimension is supposed to
   emerge from discrete connectivity — and if the model has never compared itself to this
   literature, would doing so strengthen or complicate the emergent-dimension part of its own
   story? This is a question about the model, not something this cross-check has evaluated.

3. **[pp.110-124, 2026-09-23]**
   **CLOSED → `docs/theory/notebook-correlation-pass-2026-09-23-celestial-holography.md`**
   (2026-09-23): yes, concretely — F397's `t1_spinor` (null 4-vector → 2-spinor with
   $\psi\psi^\dagger=\sigma\cdot N$) is the identical Penrose null-vector/spinor object celestial
   holography's $(energy,\,z)$ parametrization uses, gate-tested to $10^{-13}$, though it is a local
   per-momentum construction (not yet built out to null infinity) and not how the engine actually
   propagates the photon (that's Cartesian $\vec k$-space FFT). Celestial holography, not AdS/CFT,
   is the structurally relevant comparison for a future F178 asymptotic description (F193/F241 pin
   the vacuum CC at/near zero, never negative; the model's flat-asymptotic sectors — F183, F189,
   F228 — are exactly celestial holography's target regime) — but this is an open, unstarted
   direction: zero hits for BMS/null-infinity/soft-theorem language in the corpus, and the model's
   existing holography (F190/F196, horizon-area entropy) is a different axis (finite-region, not
   asymptotic) that would sit alongside a celestial description, not replace it.

   Original prompt (kept verbatim per the file's append-only rule): Celestial holography (active 2020s quantum-gravity research,
   comprehensively reviewed in arXiv:2310.04932 (2023) and revisited in *PRL* 133, 241601 (2024))
   represents a null light-ray direction at null infinity by its energy and a stereographic
   complex coordinate $(z,\bar z)$ on a "celestial sphere" — structurally the same object this
   notebook builds independently at pp.110-124 (a spinor/null direction represented by a
   stereographic coordinate $\zeta$). Prompt for a model session: does the model's own treatment
   of null vectors/light-cone structure (e.g. anywhere it represents a null direction or a
   massless particle's momentum via a spinor ratio or stereographic-type coordinate) have any
   structural point of contact with the celestial-sphere parametrization, and if the model ever
   needs an asymptotic/holographic description of its own gravity sector (Finding F178's induced
   Einstein equation), is celestial holography's flat-space approach a relevant comparison point
   (as opposed to AdS/CFT-style holography, which needs a negative cosmological constant the
   model's own universe does not have)? This is a question about the model, not something this
   cross-check has evaluated.

## C. Reconstruction queries

*Places where the cross-check suspects a reconstruction verdict is wrong or incomplete. For the
reconstruction session to adjudicate — the cross-check does not edit its files.*

| # | NB-ID | Raised | Query | Evidence |
|---|---|---|---|---|
