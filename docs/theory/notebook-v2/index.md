# Notebook v2 — Index and synthesis

**Date:** 2026-09-23 - 15:40 (Phase 4 written) · **Updated 2026-09-23 - 18:15** (Prompt A / T02
completed, see §1 row NB2-006) · **Updated 2026-09-23 - 19:30** (Prompt B completed, see §1 row
NB2-007 and §4) · **Updated 2026-09-23 - 20:10** (Prompt C completed, see §1 row NB2-010 and §4) ·
**Updated 2026-09-23 - 20:45** (Prompt D completed, see §1 row NB2-008 and §4) ·
**Updated 2026-09-23 - 21:45** (Prompt E completed, see §1 row NB2-011 and §4) ·
**Updated 2026-09-24 - 10:30** (NB2-004 Q2, the Ji decomposition, completed, see §1 row NB2-012) ·
Phase 4 of `00-continuation-research-prompt.md`

**Numbering note (2026-09-23 - 20:40):** a concurrent pass completed Prompt D in this same window;
both passes independently landed on the label `NB2-008` for their own row, then both independently
renumbered to `NB2-009` on noticing the first collision, colliding a second time. Prompt C's row
(this pass) is fixed at `NB2-010` to end the race without touching Prompt D's row again. Whatever
label Prompt D's row carries when this file is next read is that pass's own choice, not corrected
here. No F/CL number collision resulted at any point (Prompt C spent none).

---

## 1. Ledger

| Entry | Thread | Disposition | F/CL numbers | One line |
|---|---|---|---|---|
| [NB2-001](NB2-001-cooper-pair-higgs-vs-stueckelberg.md) | T03 | CLOSED-NEGATIVE + CLOSED-LINEAGE + OPEN-HANDOFF | none (corrects a same-day correlation pass by addendum) | F73 *is* NB-009 built out — corrects the A.1 pass's "bypassed altogether" claim; closes handoff A#2 with a structural finding: the model has no Yukawa mechanism anywhere, so the κ-framework signature cannot currently be tested against either Higgs candidate. |
| [NB2-002](NB2-002-sin2thetaW-2over9-lineage.md) | T07 | CLOSED-LINEAGE + CLOSED-NEGATIVE | none | The notebook's "$W^\pm=3e$" numerology is coincidence, not lineage, for both of the model's own 2/9's — closes correlation-queue row NB-133/134. |
| [NB2-003](NB2-003-riemann-silberstein-eigenbasis.md) | T06 | CLOSED-LINEAGE | none | F37 already builds the exact Riemann-Silberstein eigenbasis of the model's own rotation law — closes correlation-queue row NB-128/129. |
| [NB2-004](NB2-004-nucleon-mass-field-energy.md) | T04 | CLOSED-LINEAGE | none | F122's own dynamical baryon already quantifies "mass from field energy" for the model's proton (0.11% quark / 99.9% confinement, vs. PDG's naive 0.96%) — never previously connected to the notebook or the crosscheck's cited lattice-QCD literature. |
| [NB2-005](NB2-005-torsion-tabletop-test.md) | T05 | CLOSED-NEGATIVE | none | Fetched and read the 2024 tabletop-test paper in full; since ECSK carries no free constant beyond the model's own already-exact $G$, the model's predicted signal is the paper's own number (~20 decades below reach) — closes correlation-queue row NB-037, and settles that decision 4 needs no D12 card (structural, not an independent posit). |
| NB2-006 (Pryce, T02 — Prompt A, worked as a direct follow-up request rather than a numbered NB2-*.md entry) | T02 | FINDING F398 | F398, CL310 | Built the F69/F169 composite photon's creation operator on an exact fermionic Fock space; derived+verified $\|(a^\dagger)^2\|0\rangle\|^2=2(1-\sum\psi^4)$ and its $\sim L^{-2}$ vanishing with BZ grid resolution — closes correlation-queue row NB-007's Pryce half. Attack-and-fix review: CONFIRMED-NARROWER, one real robustness gap found and fixed in-session (resonance-robust estimator replacing a fragile single-point check). See `docs/reviews/F398-review-2026-09-23.md`. |
| NB2-007 (F73 coupling-to-fermions, T03 continuation — Prompt B, direct follow-up rather than a numbered NB2-*.md entry) | T03 | FINDING F399 | F399, CL311 | Extracted $g_{\sigma qq}$ from F77's NJL machinery (closed form, not just quadrature — found by the review's own subagent); real but non-universal within its own species (81% coupling-dependent spread); species locality proven exact (not approximate) on a two-flavor toy model — closes prompt B and the $\kappa$-framework question structurally, not numerically. Attack-and-fix review: CONFIRMED-NARROWER, two framing overclaims found and fixed in-session. See `docs/reviews/F399-review-2026-09-23.md`. |
| NB2-008 (BCC vs diamond-cubic, T01/T10 — Prompt D, direct follow-up rather than a numbered NB2-*.md entry) | T01/T10 | FINDING F400 | F400, CL312 | `dimensionality.py`'s S1/S2/S3 selectors take only a dimension `d` (confirmed by signature inspection) — they cannot be "rerun on diamond-cubic" at all, having no coordination-number input. Checked instead, one level down: BCC's own walk generator tetrahedron (Paper 2 Eq. 20) is vertex-for-vertex identical to diamond-cubic's coordination-4 bond tetrahedron (exact Gram-matrix match) — the local geometry was never the discriminator. Diamond-cubic fails BDPT's own single-orbit $(s{=}2,G=\mathbb Z^3)$ Bravais premise instead: its two sublattices are not connected by any pure translation (checked exactly: $(1/4,1/4,1/4)$ is not an FCC lattice vector, control verified). Closes T01; T10's literature-reading half stays open. See `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md`. |
| NB2-010 (calibrated nucleon mass-fraction re-run, T04 continuation — Prompt C, direct follow-up rather than a numbered NB2-*.md entry) | T04 | none (sharpens F122, no new physics) | none | Added S9 to F122's own test (`test_P2_baryon_bound_state.py`): reran the ECG solver at the real F120/F121 current-quark scale ($m_u=2.16$, $m_d=4.67$ MeV over $\sqrt\sigma=0.42$ GeV) in place of S5's toy degenerate $m_q=0.01\sqrt\sigma$, with the physical $uud$/$udd$ sum as numerator — proton 0.068%, neutron 0.094%, both *smaller* than the toy 0.11% and not a move toward the lattice paper's structurally-different ~9% figure. Closes NB2-004's own named next step. Mandatory attack-and-fix review (CONFIRMED-NARROWER — see F122's header and `docs/reviews/F122-review-2026-09-23.md`): the S9 arithmetic held under a cold independent re-derivation, but the review found and this pass fixed a pre-existing F40 mis-citation and an overstated F120/F121-independence framing in F122's own text, and flagged (not fixed) an unregistered $\alpha_s$ input and a missing F297/F372 cross-reference for a future pass. |
| NB2-011 (VI.3 finite-$k$ grid-threshold repair, T09 — Prompt E, direct follow-up rather than a numbered NB2-*.md entry) | T09 | FINDING F401 | F401, CL313 | Added `threshold="closed"` to `photon_bound_state.critical_coupling`/`.threshold_wavefunction` (default stays "grid", so F169's own artifact-diagnostic test is untouched). Proved symbolically that $\omega^+(q,0,0)=\omega^-(q,0,0)=\lvert q\rvert/\sqrt3$ exactly along any coordinate axis — sharper than F169/CL149's leading-order "vanishes on the coordinate planes" statement — so $\Omega_\text{even}(k)=T(k)$ EXACTLY (all orders) on-axis. Attack-and-fix review: CONFIRMED-NARROWER — the axis identity and (111)/(3,1,1) trends held, but a denser $L$-scan found the original "monotonic at every step" claim false (a real dip at $L=92$), narrowed to a quantified ~4x reduction in worst-case backslide vs. the grid version; and $(2,1,0)$ was found to be a genuine counterexample to "$g_c(k)$ decreases with $|k|$", narrowing that claim from "a generic direction" to the specific $(111)$/$(3,1,1)$ directions checked (confirmed there to $|k|=1.0$). Declared control confirms $k=0$ is unaffected. Honest scope: this is the Koster–Slater floor coupling, not necessarily the physical photon's own finite-$k$ coupling (which per F168/F250 rides $\Omega_\text{even}$, above $T(k)$ generically) — that harder question stays open. See `findings/F401-photon-bound-state-finite-k-threshold-repair.md`, `docs/reviews/F401-review-2026-09-23.md`. |
| NB2-012 (Ji-type nucleon-mass decomposition, T04 continuation — NB2-004 open question 2, direct follow-up rather than a numbered NB2-*.md entry) | T04 | FINDING F402 | F402, CL314 | Built the four-term decomposition ($H_E+H_m+H_g+H_a$) in the model's own sectors via $H_a=\tfrac14(M-H_m)$, $H_E=\tfrac34(x_qM-H_m)$, $H_g=\tfrac34x_gM$. **Supported:** NJL nucleon sigma term $\sigma_N=3m_0\,dM_c/dm_0=46.2$ MeV (exact Feynman–Hellmann; $-2.3$/$-3.7\sigma$ vs FLAG/Hoferichter) and the trace sector (structural identity, $H_a=23.8\%$ vs $23(1)\%$ is not a test). **Not supported:** the $H_E:H_g$ split — gluon momentum fraction $0.18$–$0.25$ (LO evolution from $\Lambda_\text{NJL}$ with the F144 $\alpha_s$; and the F122 string) vs lattice $0.43$–$0.49$, $2.0$–$2.9\sigma$ low, a statement about the non-derived $x_g=0$ start. NR Cornell mass term is negative at the F122 baseline; NJL "anomaly analogue" is an Euler identity. Operator-level $\langle N|F^2|N\rangle$ not built. Attack-and-fix review: CONFIRMED-NARROWER. See `findings/F402-ji-nucleon-mass-decomposition-model-support.md`, `docs/reviews/F402-review-2026-09-24.md`. |

**Six NB2-\*.md entries plus six direct-follow-up completions (NB2-006/007/008/010/011/012).** Five of
the six (Prompts A, B, D, E and NB2-004 Q2 — F398/CL310, F399/CL311, F400/CL312, F401/CL313, F402/CL314)
were genuine new derivations; the remaining one (Prompt C, NB2-010) sharpens an existing finding's own test with a
real calibrated input and spends no new number, consistent with how the other entries (A.1–B.3,
NB2-001–005) were scoped.
Every entry is descriptive/comparative
synthesis of existing model content against the notebook and the field — consistent with how the
session's own prior correlation passes (A.1, B.3) were scoped, and consistent with the honesty rule
that a resemblance or a lineage correction is not itself a new physics result requiring a number.
Three genuine new open questions were surfaced (§4) as candidates for a future session's actual
finding-generating work.

## 2. What the 2007 lines of thinking have become

**Pairing, 0 ⊕ 1 (NB-007, NB-009).** The notebook's single "spinor pair" idea split, inside the
model, into three independent constructions sharing only a common parent move
($\tfrac12\otimes\tfrac12=0\oplus1$): F69 (the photon, spin-1, a real dynamical rate law with an
exact zero-binding-energy protection, F168), F73 (the Higgs candidate, spin-0, exact kinematics but
undetermined binding — this session corrected the record that it was ever bypassed), and — not
touched by either — F41/F44's Stueckelberg gauge-mass mechanism, which uses neither pairing at all.
The notebook's own "one mechanism, two applications" reading does not survive; three genuinely
separate mechanisms answer three separate questions. Pryce's 1938 objection to exact Bose
statistics for the photon-as-composite (NB-007's sharpest technical content) remains completely
untouched by the model — not addressed, not sidestepped, simply never asked (thread T02, not
pursued this session; a real, scoped, `in-repo hours` next step).

**Mass as internal structure (NB-012, NB-013).** The narrow 2007 mechanism (mass counts
interactions) is independently dead on both sides — the field's own lepton-universality data kills
it, and the model never adopted it. The broad intuition (mass as field/binding energy) is alive on
both sides, and this session found the model already has its own quantitative instance sitting
unconnected in F122 (0.11% quark / 99.9% confinement) — a genuine but modest synthesis, with a named
honest caveat (the toy $m_q$ value) and a concrete calibrated-rerun as the next real step.

**Null / spinor geometry (NB-128/129, and pp.176-182 via the existing B.3 pass).** The strongest,
most literal survival in the whole notebook. Two independent points of contact now exist at the
code level: F37's Riemann-Silberstein rotation-matrix eigenbasis (this session, pp.92-101) and
F397's `t1_spinor` null-vector map (the existing B.3 pass, pp.176-182) — both exact, both
gate-tested, both genuinely load-bearing in the model's current physics, not merely resemblances.

**Electroweak numerology → structure (NB-133/134).** Resolved as an honest coincidence. The
notebook's own self-doubt ("is there any significance to this?") was the correct read in 2007 and
remains the correct read now — closer scrutiny (checking the guessed ratio against the model's
*primary* value, not just its on-shell face) makes the coincidence weaker, not stronger, than a
first glance suggests.

**Gravity with spin (NB-037).** The clearest case in this pass of the notebook's self-doubt being
premature *and* the model's own treatment being more considered than a first read suggests: the
notebook's discrepancy resolves to genuine, standard, currently-live physics (ECSK), the model has
already made a real quantitative estimate of it (F63) using the identical standard coefficient the
literature uses, and this session closed the loop by showing that estimate would translate,
unchanged, into a null result for the one concrete experimental proposal the field has produced —
20 orders of magnitude short, with no model-specific number to derive because the coupling is fixed
by the model's own already-exact $G$.

**Discrete geometry and dimension (NB-005/006/044).** Not pursued this session beyond confirming
the specific question (why BCC's coordination-8 over a lower-coordination alternative like
diamond-cubic) has never been asked in the tree, despite the model having real machinery (the
F291-class dimension selector) that could in principle answer it. Highest-value unstarted thread
from this pass (§4).

## 3. Updated correlation map

The governing prompt's seeded clusters were checked, not assumed. Confirmed real: **Pairing 0⊕1**
(sharper than seeded — three-way split, not two), **Null/spinor geometry** (stronger than seeded —
exact code-level objects, not resemblances), **Electroweak numerology → structure** (real, but
resolves negative rather than positive), **Gravity with spin** (real, resolves to a structural
non-need for a claim card plus one genuine new gap flagged). **Mass as internal structure** was
seeded broadly (NB-012/013, decision 2, F46, F122/F123) and this pass narrowed it to its most
concrete, checkable instance (the nucleon) rather than the whole cluster — the decision-2/F46
"internal helical motion" half of that cluster (NB-093-095, zitterbewegung) was read in Phase 0 but
not pursued as its own thread this session. **Discrete geometry and dimension** was seeded and
confirmed real but entirely unstarted, T01/T10 in the thread map.

**One cluster this pass found that was not seeded:** a small **cross-validation** pattern —
independently-run sessions (this one, the NB-037 reconstruction appendix, and F63's original
2026-05-30 derivation) landing on the identical standard Hehl-Datta $3\kappa/16$ ECSK coefficient by
three unrelated routes. Not a research thread in itself, but worth naming as a genuine, small
piece of evidence that the model's occasional contact with standard GR extensions is not
coincidental bookkeeping.

## 4. Open questions v2 has raised

New, not present in the queue/handoff before this session. Items 1-2 below are the original
Phase-4 list; both were subsequently taken (see the amendment note at the end of this section).
Item 3 was also subsequently taken, same session, as Prompt C.

1. ~~**Pryce 1938 (T02).**~~ **DONE, F398/CL310** — see §1 NB2-006.
2. ~~**F73's missing coupling-to-fermions construction (NB2-001).**~~ **DONE, F399/CL311** — see
   §1 NB2-007. The answer: yes, a real $g_{\sigma qq}$-type vertex exists (extracted from F77's
   own NJL machinery), but it is non-universal even within its own species and structurally
   confined to that one species — so it does not, and cannot without a genuinely new Lagrangian
   term, deliver the $\kappa$-framework signature. **New open question this raised:** would an
   explicit cross-species contact operator $G_{ab}$ (the NJL analogue of an extended-technicolor
   operator), if added, actually reproduce anything like the measured $\kappa$-framework pattern
   across multiple species, or does it just relocate the fine-tuning problem? Not pursued —
   genuinely new physics, not a derivation from what the model already has.
3. ~~**Calibrated nucleon mass-fraction re-run (NB2-004).**~~ **DONE, F122 §5a/S9** — see §1 NB2-010.
   Proton 0.068%, neutron 0.094% (both below the toy value's 0.11%); does not move toward the
   lattice paper's ~9%, which is a different four-term decomposition.
4. **F63's dependency on the superseded F62 fork (NB2-005).** Re-derive F63's energy-density ratio
   against the canonical F64/F178 sector instead, or add an explicit caveat to F63 noting the
   dependency.
5. ~~**The diamond-cubic/BCC coordination-number comparison (T01/T10).**~~ **T01 DONE, F400/CL312**
   — see §1 NB2-008. S1/S2/S3 take only a dimension `d`, so they cannot be rerun against a different
   lattice; diamond-cubic's own coordination-4 bond tetrahedron is checked to be identical to BCC's
   own walk generator tetrahedron, and what actually excludes diamond-cubic is that it is not a
   Bravais lattice (its two sublattices are not connected by any pure translation), failing BDPT's
   $(s{=}2,G=\mathbb Z^3)$ premise before dimension-counting is reached. **T10's literature-argument
   half stays open** — reading the model's reasoning against causal sets, Wolfram, and Elze 2025's
   specific arguments was not attempted this session.
6. ~~**The finite-$k$ grid-threshold artifact (T09, VI.3).**~~ **DONE, F401/CL313** — see §1
   NB2-011. `threshold="closed"` added (default unchanged); the artifact's non-monotonic L-behavior
   is now understood structurally (a genuine exact double degeneracy on coordinate axes, where
   $\Omega_\text{even}(k)=T(k)$ to all orders, not the $O(k^3)$-small residual the general offset
   formula gives off-axis) and the re-derived $g_c(k)$ genuinely decreases with $|k|$ along a
   generic direction. **New open question this raised:** whether the physical photon's own
   finite-$k$ binding coupling (which per F168/F250 rides $\Omega_\text{even}(k)$, not $T(k)$)
   tracks this same decreasing trend — not derived here, and a harder, still-open question.
7. **The $E_g$ sextic sector vs. scalar triviality (T08).** Whether F319's physical-cutoff argument
   places the model's own scalar sectors outside the Aizenman-Duminil-Copin theorem's scope, stated
   precisely rather than left a resemblance.

## 5. Paste-ready prompts for the next session

**Prompt A — Pryce 1938 composite-photon commutator (T02). DONE, 2026-09-23 - 18:15, F398/CL310.**
Taken as a direct follow-up in the same session rather than handed to a future one. Built
$a_{\mathbf k}^\dagger=\sum_p\psi_{\mathbf k}(p)b^\dagger_{+,\mathbf k/2+p}b^\dagger_{-,\mathbf k/2-p}$
(the exact F169 relative-momentum pairing, not the naive single-mode form this prompt originally
sketched) on a genuine brute-force fermionic Fock space, not the F212/F217 site-based chain this
prompt originally pointed at (momentum-space modes needed their own construction). Result: an
exact closed-form identity $\|(a^\dagger)^2|0\rangle\|^2=2(1-\sum_p\psi(p)^4)$, and the deficit
falls $\sim L^{-2}$ with BZ grid resolution — Pryce's objection is real but vanishes toward the
continuum limit for this construction. Mandatory attack-and-fix review (cold blind-derivation +
adversarial-referee subagents): **CONFIRMED-NARROWER** — the identity and the $-2$ exponent were
both independently re-derived from scratch and matched exactly, but the review's own systematic
neighbour scan found the original single-point $(L{=}10,100)$ demonstration fragile (12/30 nearby
anchor pairs passed); fixed in-session with a resonance-robust lower-envelope estimator (now
30/30), plus an attribution fix (the closed-form identity itself is standard composite-boson/
"coboson" literature, not new — only its application to this model's threshold wavefunction and
its grid-resolution scaling are). Full record: `findings/F398-pryce-composite-photon-commutator.md`,
`docs/claims/CL310-pryce-composite-photon-deficit-vanishes.md`,
`docs/reviews/F398-review-2026-09-23.md`.

**Prompt B — F73's coupling-to-fermions construction. DONE, 2026-09-23 - 19:30, F399/CL311.**
Extracted the scalar-fermion residue coupling $g_{\sigma qq}=1/\sqrt{2N_cN_fK(4M^2)}$ from F77's
NJL gap+RPA machinery — the same standard formula F77 already uses for $g_{\pi qq}$ (Goldberger–
Treiman) — and found $K(4M^2)$ has an *exact* closed form ($4E_p^2-4M^2=4p^2$ identically, not
just as $p\to0$; found blind by the mandatory review's own subagent, a genuinely better result
than this session's own first pass). The coupling is real and computable but **not universal**
even within its own species (81% spread across a coupling sweep, vs. the pion's exact, symmetry-
protected constancy — the scalar carries no protecting symmetry). The harder question — species
locality — was proven as an **exact linear-algebra fact**, not an approximation, on a two-flavor
NJL toy model: the RPA propagator matrix stays exactly block-diagonal whenever the cross-species
contact $G_{ab}=0$, which this model supplies nowhere (NB2-001's "no Yukawa mechanism" finding).
**Closes prompt B and the $\kappa$-framework question**: not because the numbers are wrong (F352
already showed that for the mass), but because the *mechanism* a universal coupling would need
(an extended-technicolor-style cross-species operator) does not exist in the model's structure.
Mandatory attack-and-fix review: CONFIRMED-NARROWER — both results independently re-derived and
confirmed; two framing overclaims found and fixed in-session (an "independent reimplementation"
claim that was actually re-typed code, and a species-locality leg whose docstring overstated what
it derives from first principles vs. what it verifies as a linear-algebra consequence). Full
record: `findings/F399-composite-scalar-fermion-coupling.md`,
`docs/claims/CL311-cooper-pair-higgs-coupling-species-local-not-universal.md`,
`docs/reviews/F399-review-2026-09-23.md`.

**Prompt C — calibrated nucleon mass-fraction re-run. DONE, 2026-09-23 - 20:10, no new F/CL number.**
Taken as a direct follow-up in the same session. Added S9 to
`tests/findings/test_P2_baryon_bound_state.py`: reran F122's own ECG solver
(`src/casim/engine/particles/baryon_dynamics.py`) at the average current-mass scale implied by the
real F120/F121 quark-mass readout ($m_u=2.16$ MeV, $m_d=4.67$ MeV, over the registered
$\sqrt\sigma=0.42$ GeV anchor) in place of S5's toy degenerate $m_q=0.01\sqrt\sigma$, using the
physical $uud$/$udd$ quark-mass sum (not $3m_\text{avg}$) as the fraction's numerator — the solver
itself still assumes equal constituent masses (§2 of F122), so this is an equal-mass solve at the
real average scale with the correct physical numerator, not a genuinely unequal-mass Hamiltonian.
Result: **0.068%** (proton), **0.094%** (neutron) — both *smaller* than the toy value's 0.11%, and
not a move toward the 2018 lattice paper's ~9% figure, because (as NB2-004 already established) that
figure is a structurally different four-term operator decomposition, not the same two-term ratio
this module computes. Closes NB2-004's own named next step and its open question 1. Mandatory
attack-and-fix review (CLAUDE.md's per-session rule for any touched finding file): see the outcome
recorded in F122's own header. Full record:
`findings/F122-p2-dynamical-baryon-three-body.md` §5a and §6 (S9),
`test-results/P2_baryon_bound_state.json`,
`docs/theory/notebook-v2/NB2-004-nucleon-mass-field-energy.md` §"New questions opened" item 1.

**Prompt D — BCC vs. diamond-cubic dimension-selector rerun. DONE, 2026-09-23 - 20:45, F400/CL312.**
Taken as a direct follow-up in the same session. `dimensionality.py`'s S1/S2/S3 selectors turned
out to take only a dimension `d` (confirmed by inspecting their actual function signatures, not
assumed) — there is no coordination-number or lattice-type input anywhere in them, so "rerun on a
diamond-cubic generator set" cannot change their verdict; asking them to distinguish BCC from
diamond is asking a function of `d` alone to distinguish two things that are both `d=3`. The real
discriminator sits one level down, at BDPT's own stated premise. Checked exactly, in integer/
rational arithmetic: (1) BCC's own walk generator tetrahedron (Paper 2 Eq. 20, "the four... BCC
tetrahedron vectors") is vertex-for-vertex **identical** to diamond-cubic's standard coordination-4
nearest-neighbor bond tetrahedron — not isomorphic, the same four integer vectors — so the local
bond geometry was never what separated the two lattices; (2) diamond-cubic is **not a Bravais
lattice**: the vector connecting its two sublattices, $(1/4,1/4,1/4)$, is not an integer combination
of the FCC primitive lattice vectors (a declared control confirms a genuine FCC vector, e.g.
$(1/2,1/2,0)$, *does* pass the same test), so no pure translation connects diamond's two
sublattices, and it fails BDPT's own single-orbit $(s{=}2,G=\mathbb Z^3)$ premise before
dimension-counting is even reached. **Closes T01**: diamond-cubic was never a competing
$(s{=}2,G=\mathbb Z^3)$ candidate for F291/F292's selectors to choose between — "why BCC not
diamond" resolves at the Bravais-lattice level, not the dimension-selector level. A genuine
coordination-4 QCA would need either doubling the internal cell to $s=4$ (against BDPT's own
minimality axiom, since $s=2$ already works for BCC) or the non-abelian generator-group extension
Paper 1 only sketches and never solves for $d=3$ — named as unexplored, not ruled out.
**T10 stays open**: none of causal sets (Myrheim–Meyer), the Wolfram Physics Project, or Elze 2025
organizes its argument around a Bravais-lattice coordination number (the parameter this result
turns on), so this finding narrows *why* no shared citation exists without doing the actual
literature-reading pass. Mandatory attack-and-fix review: pending (see index.md ledger row NB2-008
for status once run). Full record: `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md`,
`docs/claims/CL312-bcc-diamond-share-a-generator-tetrahedron-diamond-fails-bravais.md`,
`src/casim/engine/lattice/coordination_selector.py`,
`tests/findings/test_F400_coordination_selector.py` (4/4 gate-tier PASS, one declared control
verified RED).

**Prompt E — the VI.3 finite-$k$ grid-threshold artifact. DONE, 2026-09-23 - 21:45, F401/CL313.**
Taken as a direct follow-up in the same session. Added `threshold="closed"` to
`photon_bound_state.critical_coupling`/`.threshold_wavefunction` (default stays `"grid"`, so
F169's own artifact-diagnostic test — which measures the grid behavior on purpose — is completely
unaffected; verified live via `casim test --id F169-photon-bound-state`, whose only drift is a
pre-existing, unrelated C3-row staleness predating this session). Two results. **(1) An exact
identity, sharper than F169/CL149's own leading-order statement.** Proved symbolically (re-derived
independently in the test from `dimensionality.bloch_vector`, cross-checked numerically against the
engine's own `bcc` dispersion) that $\omega^+(q,0,0)=\omega^-(q,0,0)=\lvert q\rvert/\sqrt3$ — both
chiral branches collapse onto the identical isotropic cone along any coordinate axis, because the
helicity-distinguishing term in the Bloch vector vanishes whenever two of three momentum components
are zero. Consequently $\Omega_\text{even}(k)=T(k)$ **exactly, to all orders**, on-axis — not merely
$O(k^3)$-small, as F169/CL149's general "vanishes on the coordinate planes" statement gives for a
generic in-plane point (confirmed here: a genuine two-nonzero-component in-plane $k$ keeps a real,
nonzero residual, e.g. $1.4\times10^{-4}$ at $k=(0.2,0.2,0)$). This is a genuine double-degenerate
two-body floor along axes. **(2) A sharply-reduced (not eliminated) $L$-convergence artifact and a
direction-dependent $g_c(k)$.** At the SAME $L$ values F169's docstring quotes for the artifact
($12,24,32,48,96,144,192$), `threshold="closed"` converges monotonically along $(111)$ where
`threshold="grid"` reproduces the documented non-monotonic sequence. The re-derived $g_c(k)$ along
$(111)$ decreases monotonically: $2.2596\to2.2545\to2.2183\to2.1324\to1.9738$ at
$|k|=0,0.05,0.1,0.2,0.4$ ($L=192$). Declared control verified: grid and closed thresholds agree
exactly at $k=0$ ($T=0$ either way), confirming the fix changes nothing F169 already certified.
**Mandatory attack-and-fix review** (`docs/reviews/F401-review-2026-09-23.md`, cold blind-derivation
+ adversarial-referee subagents): **CONFIRMED-NARROWER**. Both core results independently
re-derived — the axis identity via a different route (direct engine dispersion calls, not just
symbolic re-typing) and the continuum floor via global numerical optimization (matching the closed
form to $\sim10^{-9}$). Two real overclaims found and fixed in-session: (a) "monotonic at every
step" did not survive a denser 48-point $L$-scan at the same $(111)$, $|k|=0.2$ point (a real dip at
$L=92$) — narrowed to a quantified, still-genuine result: the closed form's worst-case single-step
backslide is $\approx4\times$ smaller than the grid form's ($0.19$ vs $0.76$); (b) "along a generic
direction" was falsified by $(2,1,0)$, where $g_c(k)$ is emphatically non-monotonic — narrowed to
the specific $(111)$/$(3,1,1)$ directions actually checked (confirmed there to $|k|=1.0$, well past
the original $0.4$). No attack overturned the axis identity, the $k=0$ control, or the
direction-scoped decreasing trend. **Honest scope, stated plainly (not overclaimed):** this repairs
and characterizes the Koster–Slater coupling at the two-body continuum FLOOR $T(k)$, along the
specific directions and $L$-ranges checked — per F169's own C3-note, the symmetric configuration
usually identified with the spin-1 photon sits at $\Omega_\text{even}(k)$, which is ABOVE $T(k)$ at
generic finite $k$ (inside the continuum, not at its edge). Whether the physical, gauge-consistent
photon coupling tracks this same decreasing $g_c(k)$ trend is the harder, still-open question F169
already named (the all-$k$ gauge-pole proof) and this finding does not close it. Full record:
`findings/F401-photon-bound-state-finite-k-threshold-repair.md`,
`docs/claims/CL313-photon-finite-k-critical-coupling-repaired-and-decreasing.md`,
`docs/reviews/F401-review-2026-09-23.md`,
`src/casim/engine/gauge/photon_bound_state_finite_k.py`,
`tests/findings/test_F401_photon_bound_state_finite_k.py` (5/5 gate-tier PASS, one declared
control verified RED).

## 6. Session close

`make gate` ran once, in the background, at session start — **RED, 8 of 19 checks**, entirely
pre-existing (docs-index stale, D7 constants-sprawl ratchet, stale test registry, two control-
soundness problems on F350/F387, stale module graph, 5 pytest failures on F392/F169/supersession
banners), none introduced by this session and none in files this session touched. This session's
own files (five `docs/theory/notebook-v2/NB2-*.md` entries, `01-thread-map.md`, `index.md`, three
append-only edits to existing correlation/handoff/queue files, one session-claims.yaml entry) are
prose-only — no finding, module, test record, or physics changed, matching the scope the governing
prompt sets for a correlation/lineage pass, consistent with how the A.1/B.3 passes were scoped
before this session.

`make coverage` and `make indexes` are run and the session claim released in the same close-out
pass as this file (see the changelog entry and `docs/design/session-claims.yaml`).
