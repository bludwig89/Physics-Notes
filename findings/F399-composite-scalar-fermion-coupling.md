# F399 — Does the F73 Cooper-pair Higgs candidate have a natural coupling to fermions? A real, computable residue coupling that is not universal, and species locality proven exactly

**Date:** 2026-09-23 - 18:55
**Status:** Confirmed — 4/4 gate legs PASS (one machine, three quantitative/exact), two independent declared negative controls verified sound (each reddens exactly its own leg, no spill).
**Reviewed:** 2026-09-23 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F399-review-2026-09-23.md)) — both results independently re-derived blind, including a genuinely better closed form for $K(4M^2)$ than this finding originally had (fixed in this same session, machine precision replacing $\sim7\times10^{-6}$ quadrature error); two framing overclaims found and corrected (the gap-equation reimplementation is re-typed, not algorithmically independent; the species-locality leg verifies a linear-algebra consequence of an asserted, standard field-theory fact, not a from-scratch re-derivation of it) — neither affects the physics conclusions.
**Module:** `src/casim/engine/particles/derive_composite_scalar_fermion_coupling.py`
**Test record:** `F399-composite-scalar-fermion-coupling` (gate, quantitative)
**Results:** `test-results/F399_composite_scalar_fermion_coupling.json`
**Claim:** CL311
**Cross-references:** [[F73-spin0-bound-pair-scalar]] (the Cooper-pair Higgs candidate this builds a coupling for), [[F74-two-constituent-bound-state-binding]] (the contact-well binding machinery), [[F77-njl-gap-rpa-selfconsistent]] (the NJL gap+RPA construction this module extracts $g_{\sigma qq}$ from, independently reimplemented and cross-checked), [[F352-higgs-bhl-compositeness-rg-negative]] (the mass-value no-go this complements with a coupling-universality no-go); `docs/theory/notebook-v2/NB2-001-cooper-pair-higgs-vs-stueckelberg.md` (the "missing coupling-to-fermions construction" question this answers, and its "no Yukawa mechanism anywhere" finding this extends); `docs/theory/notebook-v2/index.md` §5 Prompt B.

---

## The question

F73 gives the model's Cooper-pair Higgs candidate exact kinematics — $m_H=\sin(\arcsin m_1+\arcsin m_2)$ — but no construction for how the composite would couple to (and decay to) an arbitrary Standard-Model fermion pair. NB2-001 found that the model's mass sector has no Yukawa mechanism at all, and flagged the concrete missing piece: *"what would a Yukawa-free model's version of a $g_{hff}$ vertex even look like, built from the same contact dynamics as F74/F77?"* This finding builds it, and asks the harder question the construction immediately raises: even where a coupling exists, is there any route to it being **universal** — proportional to each fermion's own mass, the $\kappa$-framework signature — the way an elementary Higgs's Yukawa sector is?

## What the model already has

F77 (self-consistent NJL gap + RPA) already builds a single contact coupling $G$ that dynamically generates a constituent mass $M$ (the gap equation) and, in the *same* RPA ladder, the scalar ($\sigma$, F73's channel) and pseudoscalar (pion) meson poles. F77 already extracts and validates the pion's residue coupling, $g_{\pi qq}=1/\sqrt{2N_cN_fK(0)}$, via the standard NJL formula, and confirms Goldberger–Treiman ($g_{\pi qq}f_\pi=M$) to $1.1\%$ against real QCD data. F77 never extracts the analogous scalar coupling, $g_{\sigma qq}$ — this is the piece this finding adds.

## Construction

The scalar-fermion residue coupling, by the same derivation F77 already uses for the pion (the residue of the RPA-resummed propagator $D_\sigma=2G/(1-2G\Pi_S(q^2))$ at its own pole):

$$g_{\sigma qq}=\frac{1}{\sqrt{2N_cN_fK(4M^2)}},\qquad K(q^2)=\frac{1}{2\pi^2}\int_0^\Lambda\frac{p^2\,dp}{E_p(4E_p^2-q^2)}.$$

Evaluated exactly at the $\sigma$'s own pole $q^2=4M^2$ — its marginal-binding threshold, F73/F74/F77's own $m_\sigma=2M$ theorem. The module reimplements F77's gap equation and loop integrals independently (not by importing the `tests/findings/` legacy script), doubling as a cross-check of F77's own published numbers.

## Result 1 (positive) — the coupling exists, is finite, and is genuinely non-universal

**$K(4M^2)$ has a closed form, and it is finite.** At $q^2=4M^2$ exactly, $4E_p^2-q^2=4E_p^2-4M^2=4p^2$ **identically for every $p$** (not just as $p\to0$), since $E_p^2-M^2=p^2$ by definition — so the bubble integral collapses to an elementary form,

$$K(4M^2)=\frac{1}{8\pi^2}\int_0^\Lambda\frac{dp}{E_p}=\frac{1}{8\pi^2}\ln\!\left(\frac{\Lambda+\sqrt{\Lambda^2+M^2}}{M}\right),$$

no singularity anywhere despite sitting exactly at the two-constituent production threshold — $g_{\sigma qq}$ is a well-defined, computable, **machine-precision** number, not zero or infinite at the marginal-binding point, and not merely "finite by quadrature" (leg `sigma_coupling_finite`; the closed form agrees with the quadrature evaluation to $7.1\times10^{-6}$, itself now a genuine second, algorithmically independent method — see "Correction from the attack-and-fix review" below).

**At F77's canonical fit** ($\Lambda=651.5$ MeV, $G\Lambda^2=2.10$, $m_0=5.5$ MeV — reproduced here, $M=311.2$ MeV, $f_\pi=92.58$ MeV, Goldberger–Treiman residual exactly $0.0$ using the closed forms throughout): $g_{\sigma qq}=2.1052$, compared with $g_{\pi qq}=3.3614$ (leg `reproduces_f77_fit`).

**The coupling is not protected by any symmetry, and it shows.** The pion's Goldberger–Treiman ratio $g_{\pi qq}f_\pi/M=1$ is a chiral-symmetry theorem — exact and coupling-independent, confirmed here to a spread of $6.2\times10^{-12}$ across a five-point coupling sweep ($G\Lambda^2\in\{1.8,2.10,3.0,5.0,10.0\}$; the review independently re-ran a wider 14-point sweep, $G\Lambda^2\in[1.7,50]$, and found the *scalar* spread grows to $96.5\%$ — the effect is robust, not an artifact of the specific five points chosen). The scalar's own analogous ratio $g_{\sigma qq}f_\pi/M$ has **no such protection**: it ranges from $0.746$ down to $0.142$ over the declared sweep, an $81\%$ spread (leg `sigma_coupling_not_universal`). The $\sigma$ is not a Goldstone boson; nothing in the model's structure fixes its coupling to a mass-proportional value even within its own constituent species.

**Correction from the attack-and-fix review (2026-09-23).** The original version of this finding used numerical quadrature only for $K(4M^2)$ and described the whole module as an "independent reimplementation" of F77's gap equation and loop integrals. The review (below) found this overstated: the gap-equation/quadrature machinery is re-typed from F77's own script, not an algorithmically different method, so it catches transcription error but not a shared algorithmic bug. **Fixed in this same session:** the closed form for $K(4M^2)$ above (independently derived blind by the review's own subagent, and independently re-verified by the referee) is now the module's primary computation, with quadrature retained as a genuine second method (closed-form-vs-quadrature agreement is now itself a gate leg), and the module/finding text no longer claims blanket algorithmic independence for the gap-equation reimplementation. Full detail: `docs/reviews/F399-review-2026-09-23.md`.

## Result 2 (negative, the one that closes prompt B) — species locality is exact, not approximate

The harder question is not whether $g_{\sigma qq}$ *can* be tuned to look mass-proportional for one species — it is whether the SAME composite could couple to a **different** species at all. Generalizing to a two-flavor NJL Lagrangian with a general contact matrix $G_{ab}$, the RPA-resummed meson propagator matrix is

$$D=\left[(2G)^{-1}-\Pi\right]^{-1},$$

and $\Pi$ is **asserted block-diagonal**, not derived from a from-scratch two-species loop calculation: a fermion loop of species $a$ contributes only to $\Pi_{aa}$ — there is no one-loop Feynman diagram connecting a $(\bar\psi_a\psi_a)$ vertex to a $(\bar\psi_b\psi_b)$ vertex without an explicit cross-species contact term $G_{ab}$ already present in the Lagrangian, a standard field-theory (Wick's-theorem) fact this finding states rather than re-proves from a raw loop diagram. **What the `species_locality_exact` leg actually verifies** (the attack-and-fix review's attack 4 sharpened this) is the *linear-algebra consequence* of that structure — that inverting a genuinely block-diagonal input matrix stays exactly block-diagonal, i.e. that the code correctly implements matrix inversion with no bug, confirmed both directly (off-diagonal entries **exactly** $0.0$, not small — leg `species_locality_exact`) and by contrast (the `G_ab`-nonzero control below, where the *same* code correctly detects genuine mixing). Built explicitly here on a toy two-species model (constituent scales $M_a=0.311$, $M_b=172.5$ GeV, each with its own coupling $G_{aa}, G_{bb}$): a $\sigma$ built purely from species $a$'s own condensate has, given the standard field-theory fact above, **identically zero** tree/RPA-level coupling to species $b$ for any values of $G_{aa}$, $G_{bb}$, $M_a$, $M_b$ — an algebraic consequence of the block structure once $G_{ab}=0$, not a small-coupling approximation.

**This model supplies no $G_{ab}$ term for any $a\ne b$, anywhere.** NB2-001 already established there is no Yukawa mechanism of any kind in the electroweak sector; this finding shows precisely what such a mechanism would have to look like structurally (an explicit cross-species 4-fermion contact vertex, the NJL analogue of extended-technicolor's cross-generation operators) and confirms none exists in the tree.

## Verified negative controls (two, each isolated)

1. **`channel="PS"`** (checks the pseudoscalar ratio instead of the scalar one): the pion ratio genuinely *is* universal, so the leg (which requires $>50\%$ spread) correctly goes red — spread collapses to $6.2\times10^{-12}$. Reddens **only** `sigma_coupling_not_universal`.
2. **`G_ab=0.01`** (a nonzero cross-species contact in the toy model): the propagator matrix genuinely mixes, off-diagonal residual $0.10$ instead of exactly $0$ — precisely the missing ingredient a real universal coupling would need. Reddens **only** `species_locality_exact`.

## What this closes, and what remains open

**Closes** Notebook v2 prompt B and NB2-001's "new question opened" #1. The model *can* build a real, finite, computable coupling from a Cooper-pair composite to its own constituent fermion species (via the same standard NJL machinery F77 already validates against real QCD data) — but that coupling is (a) not mass-proportional even within one species, unlike the protected Goldstone case, and (b) structurally incapable of reaching a second species without an explicit new 4-fermion vertex the model does not have. **The $\kappa$-framework mass-proportional-coupling signature (handoff item A#2) cannot be built from this route either** — not because the numbers come out wrong (F352 already showed that for the mass, via a different route), but because the mechanism that would be needed (species-universal condensate coupling, as in extended technicolor) is absent from the model's structure at a more basic level than any single number.

**What remains open:** whether a genuinely *new* piece of physics — an explicit cross-species contact operator, unmotivated by anything currently in the tree — could be added to close this gap, is a model-extension question, not a derivation from what exists. Not pursued here, consistent with this session's "algebra first, no new physics beyond what's needed" discipline.

## Files

- Module: `src/casim/engine/particles/derive_composite_scalar_fermion_coupling.py` (`gap_solve`, `f_pi_of`, `g_pi_qq`, `g_sigma_qq`, `two_flavour_propagator_matrix`, `check_composite_scalar_fermion_coupling`)
- Test record: `F399-composite-scalar-fermion-coupling` (`tests/registry/particles.yaml`)
- Results: `test-results/F399_composite_scalar_fermion_coupling.json`
