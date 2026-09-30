# NB2-004 — Does the model's own dynamical baryon confirm "mass from field energy" the way lattice QCD does?

**Date:** 2026-09-23 - 14:45 · **Thread:** T04 · **Cluster:** Mass as internal structure
**Lineage:** NB-012/NB-013 [RECON pp.9-11] · XCHECK pp.9-11 IMPROVES+CONFLICTS split (SETTLED) ·
CORR none yet (new) · MODEL F97, F122, F123
**Disposition:** CLOSED-LINEAGE (with one honest caveat; the named next steps were taken —
§"New questions opened" item 1 **2026-09-23 - 20:10**, item 2 **2026-09-24**, F402)

## Where the notebook left it

pp.9-11 (NB-012/NB-013): the EM field self-energy $\xi=(8\pi)^{-1}(E^2+B^2)$ and its divergence as
$r_0\to0$, used to motivate "mass from field energy" as a research direction — explicitly flagged
by the author as not yet quantitative [NB p.10-11].

## Where the three passes left it

**[XCHECK]** Split verdict, both halves SETTLED. The *broad* intuition — a particle's mass can arise
from field/binding energy rather than a bare input — is vindicated for composite hadrons by a real
external result: a 2018 lattice-QCD decomposition of the proton mass finds only ~9% from quark
(Higgs-Yukawa) mass, the rest from field energy and the trace anomaly. Separately, the *narrow*
mechanism the notebook actually proposes on these pages — that a particle's mass is set by *how
many kinds* of interaction it has — is cleanly falsified by the charged-lepton sector alone
(electron/muon/tau share identical SM gauge interactions, span ×3477 in mass); that narrower claim
is not rescued by the hadron vindication.

## What the model already has

Search terms: `grep -rli "trace anomaly\|mass decomposition\|quark condensate.*nucleon" findings`
→ nothing directly on point; located the actual content by reading F122/F123 and their result JSON
directly (`test-results/P2_baryon_bound_state.json`) rather than by keyword — the model's own
version of this result exists but uses none of the crosscheck's vocabulary (no hit on "trace
anomaly," "field energy," or "lattice QCD decomposition" anywhere near it), which is why the
keyword search alone found nothing.

**The model already has this, quantified, and already cites the correct real-world comparison —
just never connected to the notebook or the lattice-QCD literature the crosscheck names.** F122
(the dynamical, real-time three-quark bound state) reports, in the current-quark-mass limit
($m_q=0.01\sqrt\sigma$, a chosen small/toy value, not the model's own calibrated light-quark
masses): *"the quark-mass sum is 0.11% of the bound-state mass; the remaining ~99.9% is the
confining string + kinetic energy... This reproduces F97's no-go statement (PDG current-quark sum
is 0.96% of $m_p$...) as an explicit dynamical number: the proton's mass is the string, not the
constituents."* This is exactly the notebook's NB-012/013 intuition, made dynamical and quantitative
by a genuine bound-state solve (S2/S3: a converged, discrete, non-dispersing ground state — not an
assumption) rather than a static energetic argument (F97) or the 2007 divergent-self-energy sketch.

## The next step, taken

Pure synthesis and one honesty check — no new CASIM run.

**Is this the same comparison the 2018 lattice paper makes?** No, and that distinction matters.
F122's own cited comparison (0.11% model vs. 0.96% PDG) is a **naive same-style ratio**: sum of
current-quark rest masses over total baryon mass, on both sides. The crosscheck's cited 2018 result
uses a different, more structured operator decomposition (quark mass/condensate term, quark
kinetic+potential energy, gluon field energy, and the trace anomaly, evaluated as separate QCD
Hamiltonian matrix elements) that arrives at a *different* number (~9%) for what sounds like the
same question — the two "quark contributions" are not the same observable. F122's 0.11%-vs-0.96%
comparison is honest and correctly labeled in its own text; it should not be read against the
lattice paper's ~9% figure, and this entry does not attempt to reconcile them, because doing so
would compare two different operators as if they were one (exactly the "resemblance is not a
derivation" failure mode the governing prompt warns against).

**Is the model's 0.11% itself a prediction, or an assumption?** An honest caveat F122's own text
states but does not emphasize: $m_q=0.01\sqrt\sigma$ is a chosen small value for a *limiting-case*
check (confirming confinement dominance survives even at the lightest quark masses considered), not
the model's own calibrated u/d quark mass from F120/F121's locked spectrum. So 0.11% is a
demonstration that the qualitative conclusion is robust in that limit, not a from-first-principles
prediction to be compared digit-for-digit against 0.96% or 9%. **The genuinely open step** — not
taken here, named for a future session — is re-running F122's own ECG solver with the model's actual
calibrated F120/F121 light-quark masses in place of the toy $0.01\sqrt\sigma$, and reporting the
resulting quark-mass fraction as a real, calibrated number rather than a limiting case.

## Correlations exposed

- Connects **T04**'s cluster (Mass as internal structure) to F97's existing no-go and F122's
  existing dynamical confirmation — a link that existed in the tree already (F122 cites F97
  directly) but had never been read against the notebook or the crosscheck's lattice-QCD citation
  until this entry.
- The honesty caveat above (toy vs. calibrated $m_q$) is itself a small, concrete residual worth
  flagging for **F122** the finding, independent of the notebook: its own S5 check target (<2% of
  $M$) is loose enough that both the toy value and a calibrated one would likely pass, so this is
  not a finding-integrity problem — just an opportunity to sharpen an existing result.

## New questions opened

1. ~~**A calibrated re-run.**~~ **DONE, 2026-09-23 - 20:10** (notebook-v2 prompt C, same session,
   taken as a direct follow-up rather than handed to a future one). Added S9 to
   `tests/findings/test_P2_baryon_bound_state.py`: reruns F122's own ECG solver at the average
   current-mass scale implied by the real F120/F121 quark-mass readout ($m_u=2.16$, $m_d=4.67$ MeV
   over $\sqrt\sigma=0.42$ GeV) in place of the toy degenerate $m_q=0.01\sqrt\sigma$, with the
   physical $uud$/$udd$ quark-mass sum (not $3m_\text{avg}$) as the numerator. Result: **0.068%**
   (proton), **0.094%** (neutron) — both *smaller* than the toy value's 0.11%, not a move toward the
   lattice paper's ~9%, because that figure is a structurally different four-term operator
   decomposition (§"Is this the same comparison" above already established this; the calibrated
   rerun does not change that answer, it only replaces the toy input with a real one on the *same*
   two-term ratio). Caveat carried into F122 §5a: the solver's Jacobi-coordinate engine assumes
   equal constituent masses, so this is an equal-mass solve at the average current scale with the
   correct physical numerator, not a genuinely unequal-mass three-body Hamiltonian. Full record:
   `findings/F122-p2-dynamical-baryon-three-body.md` §5a/§6 (S9), `test-results/
   P2_baryon_bound_state.json`.
2. ~~**Building the fuller (Ji-type) decomposition.**~~ **DONE, 2026-09-24, F402/CL314.** Built in
   the model's own sectors (NJL constituent nucleon, F122 Cornell string, F144/F152 $\alpha_s$) via
   the sum-rule + momentum-fraction route ($H_a=\tfrac14(M-H_m)$, $H_E=\tfrac34(x_qM-H_m)$,
   $H_g=\tfrac34x_gM$). **Supported:** the quark-mass term (NJL $\sigma_N=46.2$ MeV, exact
   Feynman–Hellmann; $-2.3$ to $-3.7\sigma$ below the measured sigma term) and, structurally, the
   trace sector ($H_a=23.8\%$ vs $23(1)\%$ — an identity, not a test). **Not supported:** the
   quark-energy / gluon-energy split — the model's gluon momentum fraction at 2 GeV is $0.18$–$0.25$
   (two routes) vs the lattice $0.43$–$0.49$, $2.0$–$2.9\sigma$ low, a statement about the non-derived
   $x_g=0$ start at $\Lambda_\text{NJL}$. The non-relativistic Cornell solver gives a *negative* mass
   term at the F122 baseline. **Not built:** the operator-level $\langle N|F^2|N\rangle$ separation of
   $H_g$ from $H_a$. Full record: `findings/F402-ji-nucleon-mass-decomposition-model-support.md`,
   `docs/reviews/F402-review-2026-09-24.md`.

## Files touched

- `docs/theory/notebook-v2/NB2-004-nucleon-mass-field-energy.md` (this file)
