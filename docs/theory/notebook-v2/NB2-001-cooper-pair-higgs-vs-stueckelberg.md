# NB2-001 — Is the model's Higgs-avoidance route checked against the 2012+ mass-proportional-coupling evidence?

**Date:** 2026-09-23 - 13:35 · **Thread:** T03 · **Cluster:** Pairing, 0 ⊕ 1
**Lineage:** NB-009 [RECON pp.5-6 batch, SOLID] · XCHECK pp.5-6 IMPROVES/ACTIVE (live pNGB
composite-Higgs program) and pp.62-72 CONFLICTS-DATA/SETTLED (Higgsless premise excluded by the
2012/2022 data) · CORR `notebook-correlation-pass-2026-09-23.md` (A.1, addendum below) · MODEL
F27, F34b, F41, F44, F69, F73, F352
**Disposition:** CLOSED-NEGATIVE (handoff item A#2) + CLOSED-LINEAGE (A.1 correction) + OPEN-HANDOFF (one new question)

## Where the notebook left it

pp.5-6, items 2/3/6: *"symmetry breaking is superconductor-like... two electrons pair up to create
a single Cooper pair, a spin-0 state... The Higgs is the Cooper pair, we presume."* [NB p.5-6] An
idle proposal under the same "spinor pair" heading NB-007 uses for the photon — the author reaches
for one mechanism, two applications (pair → photon, pair → Higgs), and does not develop either
quantitatively.

## Where the three passes left it

**[RECON]** NB-007/NB-009 read as a genuine, self-contained 2007 idea (SOLID, contamination-flagged
for adjacent literature exposure on the photon side only). No physics content disputed.

**[XCHECK]** Two separate verdicts land on two separate parts of this notebook page range. pp.5-6
(NB-009 specifically) is graded IMPROVES/ACTIVE: composite-Higgs (pseudo-Nambu-Goldstone) models are
a live, unexcluded 2020s research program, compositeness scale $f\gtrsim0.6$-$1.3$ TeV, continuing
published work through late 2023 — the *general idea* survives. Separately, pp.62-72 (NB-080, the
notebook's explicit "Weinberg-Salam without a Higgs field" program) is graded CONFLICTS-DATA/SETTLED:
the 2012 discovery and especially the 2022 confirmation that Higgs-like couplings track particle mass
across three orders of magnitude (*Nature* 607, 52-59) directly falsify any construction that puts
*no* dynamical scalar in at all. The synthesis's own ranked handoff item #1 asks whether the model's
hypercharge-on-$U(x)$ mechanism (decision 3) has ever been checked against this second, sharper
piece of evidence — filed as handoff §A item 2, status `open` as of this session's Phase 0 read.

**[CORR]** The existing A.1 pass (2026-09-23, same day, earlier in this session's reading order)
answers a narrower question — whether F69 (photon) and F41 (hypercharge/mass) share a mechanism —
correctly finding them independent, but states along the way that "the model didn't attempt [NB-009's]
unification and then have it diverge — it bypassed NB-009 altogether." That specific sentence is
wrong, corrected by addendum in place (see that file) rather than edited, because F73 exists.

## What the model already has

Search terms: `grep -ril "cooper.pair\|spin0.*bound.pair" findings`, `grep -rli yukawa
findings/F27*.md findings/F34b*.md findings/F44*.md findings/F41*.md`, `grep -rli "kappa.framework\|
mass-proportional" findings docs/claims`.

**F73** (`findings/F73-spin0-bound-pair-scalar.md`, 2026-06-01) is NB-009 built out, explicitly
citing pp.5-6 items 2/3/6 in its own header. It takes the antisymmetric spin-0 singlet of the F69
pairing (F69 took the symmetric spin-1 channel as the photon) and derives, from F46
($\Omega_\text{rest}(m)=\arcsin m$) and F69 (a bound pair's phase-per-tick is the constituent sum),
an exact composite-mass law

$$m_H = \sin(\arcsin m_1 + \arcsin m_2),$$

verified to $\le4\times10^{-51}$. This gives a kinematic ceiling ($m_H\le m_1+m_2$, strictly below
on the lattice — "negative binding energy" made quantitative) and a stability bound
($m_c\le1/\sqrt2$), but **not** the binding depth $E_b=(m_1+m_2)-m_H$ that would fix $m_H$ to
125.25 GeV — F73's own verdict: *"the missing input is genuine binding dynamics... the depth
$E_b$... is precisely the role the SM Higgs quartic $\lambda$ plays."* **F352** (2026-09-02) is the
one binding-dynamics route attempted since: RG-improved Bardeen-Hill-Lindner top compositeness,
anchored at the model's own derived UV cutoff (F79/F107, no free scale choice), and it returns a
quantified negative — $m_t=226.56$ GeV (+31.3%), $m_H=248.76$ GeV (+98.6%, essentially double).

**Separately — and this is the new synthesis this entry adds, not previously stated anywhere in
this form** — the model's mass sector has **no Yukawa mechanism at all**, elementary or otherwise.
F41's own text says so directly: *"F27 (chiral SU(2) mass from β-gauging — no Higgs Yukawa)."*
Reading F27 confirms why: the fermion mass parameter $m$ enters the mass step as a **bare, per-species
scalar** (`c_m = cos(m·dt)`, `s_m = sin(m·dt)`), with $U(x)\in SU(2)$ supplying only the *direction*
of the coupling (which doublet component), never its magnitude — $U(x)$ has no radial degree of
freedom because it is valued on the group manifold itself, not on the space of general $2\times2$
complex matrices. Separately, F34b/F44's Stueckelberg construction for $m_W,m_Z$ uses a *different*
scale $f=v/2$, fixed and non-dynamical by design (a genuine Stueckelberg field has no radial mode;
that is the whole point of the construction, and F73 says so explicitly: *"the radial (breathing)
mode... is removed"*). **These two masses — fermion $m$ and gauge-boson $f$ — are architecturally
independent parameters in this model,** unlike the Standard Model, where a single Higgs VEV $v$
sources both via $m_f=y_f v/\sqrt2$ and $m_W=gv/2$.

## What the field has now

2012 ATLAS/CMS Higgs discovery; 2022 combined ATLAS+CMS measurement of Higgs couplings tracking
particle mass across three orders of magnitude, the signature the $\kappa$-framework parametrizes
($\kappa_f\propto$ measured coupling / SM-predicted coupling, consistent with 1 for every fermion
and boson species measured) — *Nature* **607**, 52-59 (2022).

## The next step, taken

Algebra first, as the governing prompt requires, before reaching for any CASIM run — and the
algebra closes the question without one.

The handoff's question is whether the model's Higgs-avoidance mechanism "predicts (or accommodates)
a dynamical scalar resonance near 125 GeV with mass-proportional couplings." Two constructions exist
that could in principle be that resonance:

1. **The Stueckelberg radial mode** (F34b/F44), restored by hand: $f\to f+h(x)$. This is the
   textbook route to a $\kappa$-framework-compatible state — in any construction where
   $m_f=y_f\langle\phi\rangle$, restoring the radial mode automatically gives a linear coupling
   $g_{hff}=m_f/\langle\phi\rangle$, coupling *exactly* proportional to mass, for free, as an
   algebraic consequence of the same mechanism that sets the masses. **This route does not apply
   here.** The model's fermion mass $m$ is not sourced by $f$ at all (confirmed above — no Yukawa
   term exists connecting them), so restoring $h$ in the *gauge* sector's Stueckelberg field would
   give $h$ a coupling to $W,Z$ (from the kinetic term, standard) but **no mechanism links $h$ to
   any fermion**, mass-proportional or otherwise. The model's specific architectural choice to
   *not* have a Yukawa term is what breaks the textbook route, not merely the choice to omit the
   radial mode.
2. **F73's Cooper-pair channel.** This is a mass-formula construction, not a coupling/decay-channel
   construction: F73 gives $m_H$ as a function of two constituent masses, but builds no vertex
   coupling the composite state to an arbitrary third fermion species at all. There is no analogue
   of $g_{hff}\propto m_f$ to test here because no $g_{hff}$ of any form has been constructed for
   this object — testing the $\kappa$-framework signature against it is not currently possible, not
   because the answer is unfavorable but because the observable does not exist yet in the model.

**Result: the handoff question is answered, and the answer is structural, not numerical.** The
model has not checked itself against the mass-proportional-coupling evidence because it currently
has **no object with a coupling of the relevant type to check** — not the restored-radial-mode
route (blocked by the absence of any Yukawa mechanism, confirmed above) and not F73's Cooper pair
(no coupling-to-fermions construction exists for it at all). This is sharper than "not derived": it
identifies *which* missing piece of machinery (a Yukawa-type vertex, for either candidate) would
have to be built before the question could even be posed numerically.

## Correlations exposed

- The three-way independence this session's own A.1 pass establishes (F69 photon / F41 mass sector)
  extends to a fourth object: F73's Cooper-pair Higgs candidate is independent of *both* — it
  shares F69's pairing kinematics but touches neither F41's Stueckelberg mechanism nor any Yukawa
  structure, because none exists.
- This closes part of **T02**'s cluster question (Pairing, 0⊕1): the reason F73 cannot yet be
  confronted with the $\kappa$-framework data is a different obstruction than F352's binding-depth
  no-go — even with a correct binding depth in hand, F73 would still need a coupling-to-fermions
  construction built from scratch, since nothing like a Yukawa vertex exists anywhere in the tree
  to model it on.

## New questions opened

1. **Building a coupling for F73's composite.** What would a decay/coupling vertex for the F73
   Cooper-pair state look like in a model with no Yukawa mechanism at all? The natural candidate is
   some contact interaction inherited from the same gauge dynamics that binds it (cf. F74/F77's
   contact-well and NJL-gap constructions) rather than a fundamental Yukawa term — but nobody has
   built it. This is the concrete next step toward actually testing $\kappa_f$ against this model,
   flagged `LONG-RUN` scope (a genuine new derivation, not a rerun).
2. **Is the fermion/gauge-boson mass independence ($m$ vs. $f$) itself worth a claim card?** It is a
   structural fact about the model's electroweak sector, distinguishing it from the SM's single-VEV
   unification of the two mass sources, established here for the first time in this explicit form
   (previously implicit across F27/F34b/F41/F44's separate texts, never stated as one structural
   claim). Candidate for a D12 card if a future session confirms it is genuinely novel relative to
   the existing F27/F41/F44 cards and not already implied by one.

## Files touched

- `docs/theory/notebook-correlation-pass-2026-09-23.md` (addendum, append-only)
- `docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md` (this file)
- `docs/theory/notebook-sm-crosscheck-handoff.md` — item A#2 marked `CLOSED` below, in that file's
  own append-only table format
