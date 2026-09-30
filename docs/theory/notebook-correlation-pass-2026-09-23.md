# Correlation pass — handoff item A.1 (paired-spinor photon vs. Higgs-avoidance route)

*2026-09-23 · answers `notebook-sm-crosscheck-handoff.md` §A item 1 · sources: [F41](../../findings/F41-hypercharge-higgs-free-su2.md), [F69](../../findings/F69-paired-spinor-photon.md), [F44](../../findings/F44-higgs-free-mA-zero-from-rank1-stueckelberg.md), `docs/theory/key-decisions.md` decisions 3 and 5, `notebook-sm-crosscheck-pp003-011-photon-graviton-cooper-mass.md` (NB-007/NB-009 verdicts)*

## The question

The live composite-Higgs literature (pNGB Higgs, naturalness) and the dormant paired-fermion
composite-photon literature (Perkins) are structurally distinct research programs even though the
notebook (NB-007/NB-009) reaches for both under one "spinor-photon-pair" umbrella. Does the
model's own photon (F67–F69) or its Higgs-avoidance route (decision 3, hypercharge on U(x)) draw
any structural connection between the two, or are they independent in the model too — and if
independent, is the notebook's original intuition (one mechanism, two applications) actually
wrong, or just not how the model ended up building it?

## Answer

**Independent.** The two constructions are mechanistically unrelated in the model.

**The photon (F67–F69)** is NB-007's idea, kept and formalized: a bound pair of two *propagating*
spin-½ Weyl quanta, one per chiral branch, each carrying $k/2$, whose combined rate is the
constituent sum $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$. This is a genuine composite of
two on-shell fermionic degrees of freedom — structurally the same idea as the de
Broglie/Jordan/Perkins "neutrino theory of light" line.

**Hypercharge/mass (F41, decision 3)** is not a bound state of anything. The existing SU(2)_L
pure-gauge field $U(x)$ already present in the F27 chiral mass step is extended to also carry a
diagonal U(1)_Y phase, $U(x)\to U(x)\cdot D(\alpha)$. No new particle content, no pairing of
constituents — it is an enlargement of a gauge connection. The extra phase degree of freedom is
eaten by the Z as its longitudinal mode via Stueckelberg (F34b/F44), and $m_A=0$ falls out
structurally from the resulting rank-1 mass matrix.

**The one genuine echo:** the retired σ-bilinear ($\phi^\dagger\sigma^i\psi$, a fermion-current
*bilinear*, not a bound pair of propagating particles) is kept in the model specifically for
W/Z/gluon fields (F69, "What was retired, and what was kept"). So there is a weak, general sense
in which "gauge bosons are built from fermion-bilinear constructions" persists across the gauge
sector — but this is a looser idea than NB-007's literal bound pair, and it never touches the
Higgs/mass mechanism: W and Z get *mass* from Stueckelberg absorption of a gauge phase, not from
any fermion pairing.

**Was the notebook's intuition wrong?** Not wrong exactly — composite Higgs (pNGB models) remains
a live, unexcluded research program, so "Higgs as a bound state" survives as a legitimate idea in
the field. What doesn't survive, in the literature or in the model, is the specific *unification*
NB-009 reaches for: the *same* photon-building fermion pair reappearing as the Higgs. The
cross-check's own hindsight on NB-009 makes this point independently of the model — mainstream
composite-Higgs models use new strongly-coupled constituents, not photon-forming fermions, so even
the field itself never took NB-009's literal reading.

Internally, the model didn't attempt that unification and then have it diverge — it bypassed
NB-009 altogether. F41's Higgs-avoidance route requires no composite or elementary scalar of any
kind, paired-fermion or otherwise. So: NB-007 was kept and built out; NB-009 was never pursued as
stated, replaced by a structurally unrelated mechanism (gauge extension + Stueckelberg) that
answers the same "how do gauge bosons/fermions get mass without an elementary Higgs" question a
different way.

## Addendum (2026-09-23 - 13:30, Notebook v2 / NB2-001)

**The claim above that "the model bypassed NB-009 altogether" is wrong, and the record is
corrected here rather than in the body above, per this file's append-only rule.**

`findings/F73-spin0-bound-pair-scalar.md` (2026-06-01, predates this pass by three months) is
exactly NB-009 pursued as stated: it builds the antisymmetric spin-0 singlet of the *same* F69
pairing this pass already discusses, cites the same notebook lines this pass quotes ("the Higgs is
the Cooper pair, we presume," pp.5-6 items 2/3/6), and derives an exact composite-mass law
$m_H=\sin(\arcsin m_1+\arcsin m_2)$ from F46+F69 with no new dynamical assumption. So the model
*did* attempt NB-009's literal "same pair, two applications" unification — F73 is that attempt, not
an absence of one. What is true, and is the corrected form of this addendum's headline claim: F73's
attempt is **kinematically complete and dynamically incomplete** — it predicts a ceiling
($m_H\le m_1+m_2$) and a channel identity, not the binding depth that would fix $m_H=125.25$ GeV,
and F352 (2026-09-02) closes the one binding route so far attempted (RG-improved BHL top
compositeness) as a quantified negative ($m_H=248.76$ GeV, +98.6%).

This changes the answer to §2's "was the notebook's intuition wrong?" question in one respect: it
was not bypassed, it was tried and left incomplete — a live, open thread, not a closed one. It does
**not** change this file's main finding (the two mechanisms — F69's photon and F41/F44's
Stueckelberg gauge-boson-mass route — are independent constructions); F73 is a *third*, separate
construction (the same pairing's spin-0 channel) that also never touches F41/F44's Stueckelberg
mass mechanism, so the three-way independence claim in this file's "The one genuine echo" paragraph
stands, now with F73 named as the thing NB-009 actually became. Full adjudication, including the
still-open handoff item A#2 (κ-framework mass-proportional couplings), in
`docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md`.
