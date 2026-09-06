# F338 — B10 after F325: the odd-$N_c$ bracket does not narrow further — one previously-untested candidate route closed, one mod-16 lead flagged (not derived), and the residual confirmed generic against the external literature

**Date:** 2026-08-31 - 15:10
**Numbering:** **F338**, taken as `NEXT FREE NUMBER` (`casim index` → max `F337`, no gaps; F338 confirmed free before writing). Session `steady-quiet-witten`, sector `gauge`.
**Status:** Confirmed — **4/4 PASS**, four declared controls each verified red **and red only where declared** (`casim test --id F338-ncolour-ceiling --control`). *(Note on what "4/4 PASS" certifies, added on review: all four are code-correctness checks — G0 a regression on `witten_scan`, G1 a citation-table lookup, G2 an elementary count, and G3 a check that the flagged mod-16 arithmetic correctly reads its own modulus parameter. None of the four, including G3, verifies a physics claim about the colour bracket beyond what §§2–5 already state; G3's physical premise stays explicitly unverified — see `declarations.g3_mod16_premise_verified: False` — and is excluded from the pass tally for that reason.)*
**Verdict:** Row **B10** stays **PARTIAL**, unchanged from F325's own re-grading. This finding does **not** narrow the bracket $\{3,5,7,9,11,\dots\}$ F324/F325 left B10 with, and says so before anything else. What it adds: (1) a candidate route nobody in this tree had checked — a $\pi_4$-type global anomaly on the **colour** group $SU(N_c)$ itself, distinct from the already-used $SU(2)_L$ route — is closed by citation ($\pi_4(SU(N))=0$ for every $N\ge3$, standard homotopy-of-Lie-groups fact); (2) an exact elementary count, that the model's own per-generation Weyl fermion content is $4(N_c+1)$, equal to $16$ precisely at $N_c=3$; (3) a **flagged, explicitly unverified** mod-16 lead (García-Etxebarria–Montero; Wang) that, *if* its physical premise generalises to this model's arbitrary-$N_c$ content, would narrow the bracket to $\{3,7,11,15,\dots\}$ — named as the single most concrete next step, not claimed as a result; and (4) an external cross-check: the **general** (non-lattice, arbitrary-$N_c$) chiral-gauge-theory literature has no further theoretical selector either, confirming the residual is generic to this shape of theory, not a defect of this particular lattice/CA construction.
**Modules:** `src/casim/engine/gauge/derive_ncolour_ceiling.py` (new)
**Test / results:** record `F338-ncolour-ceiling` (tier gate, entry `check_ncolour_ceiling`), driver `tests/findings/test_F338_ncolour_ceiling.py` → `test-results/F338_ncolour_ceiling.json`
**Cross-references:** [[F324-ncolour-bracket-closed]] (the surviving lower leg, `witten_scan` imported unmodified), [[F325-x1-resolved-branch-b-adopted]] (the withdrawal this finding starts from), [[F293-why-three-colours]] (the three closed routes R1–R3, not re-attacked), [[F298-casimir-ladder-c7-rerun]] (the withdrawn upper leg), [[F317-su3-structure-derived]] (Sec 10's "internal index is still an input", untouched), [[F75-three-generations-from-bcc-irrep-selection]] (the $n_\text{gen}$ odd premise).
**Claim:** none — this finding does not narrow B10's bracket or assert any new physics prediction; it closes one candidate route by citation, flags one unverified arithmetic coincidence, and cross-checks the residual against the external literature. Any claim card covering the odd-$N_c$ bracket or the surviving Witten-parity leg belongs to F324/F325, unmoved by this finding. Declared 2026-08-31.
**Checked:** 2026-08-31 — 10 PASS / 3 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED**

---

## 0. Where this picks up, stated before anything else

F325 (2026-08-18) resolved the X1 colour-normalisation fork and, as a consequence, **withdrew** F324's upper constraint: the C7 identity's "well-defined only for $N_c\le3$" (CN19) was a property of a mixed-operator matching, not a selector. What survives is F324's **lower** leg only — the $\pi_4(SU(2))=\mathbb Z_2$ Witten global anomaly on the model's own derived chiral $SU(2)_L$ (prior art, Bär & Wiese 2001) — so B10 closes on

$$\{N_c\text{ odd},\ N_c\neq1\}\;=\;\{3,5,7,9,11,\dots\}$$

with $N_c=3$ favoured by F293 §4's 28.3-decade confinement-scale lever and by nothing structural. This session's task was to find a structural selector narrowing that bracket to $\{3\}$ alone, or to document it as the honest ceiling. **The bracket is not narrowed here.** Three things are new, and none of them is a derivation of 3.

---

## 1. What was tried and closed as dead ends before anything new (not re-derived; confirmed against the ledger)

The four previously-identified routes were **not** re-attacked, per the standing instruction and F293/F303/F325's own closures:

* **Anomaly cancellation (F293 R1).** Circular in this model — $Y_Q$ is not independently given; it comes out of the same nullspace, proportional to $N_c$.
* **Spatial-3 identification (F293 R2).** Excluded: $[C_3,\lambda^a]\neq0$, so an axis-identified colour would be observable.
* **$\mathbb Z_3$-centre route (F293 R3).** Circular — the tree introduces $\mathbb Z_3$ *as* $SU(3)$'s centre.
* **F303's $n\,C_F=4$ three-link-plaquette route.** Dead by exhaustive enumeration — BCC nearest-neighbour hops cannot close a 3-hop loop (0 of $8^3$ triples).
* **F325/CN19's C7 upper bound.** Withdrawn as a mixed-matching artefact.

I additionally verified via literature search (§4 below) that the standard textbook route — matching electric-charge quantisation against the model's own hypercharge nullspace — is exactly what F293 R1 already closed as circular, and is not a new avenue.

---

## 2. G0 — the current bracket, recomputed rather than quoted

`witten_scan` (F324's own function, imported unmodified) allows $N_c=1$ too: $D_\text{gen}=N_c+1=2$ is even for any $n_\text{gen}$, so the $\mathbb Z_2$ parity is vacuously satisfied there. The parity leg alone never excluded $N=1$. $N_c\neq1$ is a **separate, still-standing** premise — that a non-trivial colour sector exists at all (F317 §0 item (i), "the quark carries an internal index at all — still an input"; F318's residual). F324 §3 U1b implemented that premise's $N=1$ edge *through* the now-withdrawn C7 ladder convention, but the premise itself is prior to and independent of that implementation, and F325 withdrew only the C7 identity's upper-bound content, not this premise. So $N_c=1$ is dropped here on that still-standing ground, explicitly not via the withdrawn C7 apparatus.

**G0 (exact, over the scanned range).** $\{N_c : \text{witten\_scan consistent}\}\setminus\{1\} = \{3,5,7,9\}$ over $N=1..10$ — reproducing F325's ledger conclusion directly from code rather than by quoting it, and confirming the withdrawal is correctly reflected outside the finding's own prose.

---

## 3. G1 — a previously-untested candidate route, closed by citation: does the colour group itself carry a global anomaly?

The surviving lower leg uses $\pi_4(SU(2))=\mathbb Z_2$ on the **weak** group $SU(2)_L$. A natural further question, not previously asked in this tree: does the **colour** group $SU(N_c)$ carry an *analogous* $\pi_4$ global anomaly of its own, which might bite at some $N_c$ and not others?

**No.** $\pi_4(SU(N))=0$ identically for every $N\ge3$ (Bott 1959; standard homotopy-of-Lie-groups fact, tabulated e.g. in Mimura & Toda, *Topology of Lie Groups I, II*, Springer 1991); only $SU(2)$ carries the non-trivial $\mathbb Z_2$. This is a **cited** mathematical fact, not computed in this tree — on the same footing as this tree's other cited-not-derived facts (BDPT uniqueness, F326). It closes a candidate that had never been explicitly examined and ruled out, rather than leaving it as a silent gap: the colour gauge group cannot supply a second, independent $\pi_4$-type constraint at any $N_c\ge3$.

---

## 4. G2 — an exact per-generation fermion count, and G3 — a flagged, unverified mod-16 lead

**G2 (exact).** The model's own per-generation Weyl fermion content — $N_c$ quark doublets ($2N_c$ Weyl components), $2N_c$ right-handed quark singlets, one lepton doublet (2), $e_R$ (1), and a right-handed neutrino (1, F47's Majorana step) — totals exactly

$$4(N_c+1),$$

which equals **16 precisely at $N_c=3$**. This is elementary dimension arithmetic, exact over $\mathbb Z$, and by itself carries no topological content.

**G3 — flagged, not verified, not claimed as a result.** The coincidence that the SM's well-known "16 Weyl fermions per generation" (García-Etxebarria & Montero, *Dai-Freed anomalies in particle physics*, 1808.00009; Wang, *Anomaly and Cobordism Constraints Beyond Grand Unification: Energy Hierarchy*, 2008.06499 — the paper that actually defines the $X=5(B-L)-4Y$ generator used below) equals exactly $4(N_c+1)$ at $N_c=3$ is striking enough to record. *(Correction on review, 2026-08-31: an earlier draft of this section and of the module's docstring/caveat string cited "Wang–Wen–Witten 1810.00844" for this content. That paper, "A New SU(2) Anomaly," concerns a distinct SU(2)/Sp(2N) global anomaly on non-spin manifolds and says nothing about the Standard Model, hypercharge, $B-L$, or a fermion-count mod-16 condition — it was misattributed. The correct source for the $X=5(B-L)-4Y$ generator and the associated mod-16 condition is Wang, 2008.06499; 1810.00844 remains correctly cited elsewhere in this tree, e.g. F324's isospin-3/2 caveat, and is untouched there.)* *If* the associated Pin$^+$/Dai-Freed mod-16 anomaly generalises to the bare condition "the total Weyl-fermion count, summed over generations, is a multiple of 16" for this model's general-$N_c$ content, then since any odd $n_\text{gen}$ is invertible mod 4,

$$n_\text{gen}\cdot4(N_c+1)\equiv0\ (\mathrm{mod}\ 16)\iff N_c\equiv3\ (\mathrm{mod}\ 4),$$

narrowing the odd bracket to $\{3,7,11,15,\dots\}$ and excluding $\{5,9,13,\dots\}$ — a real narrowing, **if the premise holds**.

**It is not verified here, and the reason is stated rather than glossed over.** The actual Pin$^+$ invariant (Wang, 2008.06499) is built from a specific discrete symmetry generator $X=5(B-L)-4Y$, whose coefficients ($5$, $-4$) are fixed by the $N_c=3$ Standard Model content. Nothing in this session re-derives $X$'s own $N_c$-dependence for this model's nullspace, and the cited "16" is derived for $N_c=3$ specifically — it is not shown in the source literature to generalise as a bare fermion count for other $N_c$. Treating "total count $\equiv0\pmod{16}$" as the correct general-$N_c$ statement of the anomaly is an assumption, not a re-derivation, and a hostile reading could be wrong about which invariant actually generalises (it could, for instance, depend on $N_c$ in a way that does not reduce to a bare count at all).

**Disposition.** Recorded as a flagged coincidence in the sense F300 §5 uses the term for its own $2\pi\sqrt3$ reciprocal-lattice observation — kept **out of the pass count** (the `declarations` field, not a check), and named as the single most concrete, well-defined next step for a session with the primary references in hand: recompute $X$'s $N_c$-dependence on this model's own hypercharge nullspace and check what the Pin$^+$ bordism invariant actually says for general $N_c$, rather than assuming the bare-count generalisation.

---

## 5. External cross-check against the general (non-lattice) literature

Search terms used: "SU(N) colour number selection lattice gauge symmetry", "Witten anomaly gauge group rank selection", plus follow-ups on the mod-16 anomaly and on generic-$N_c$ 't Hooft anomaly matching.

| Source | Finding |
|---|---|
| Bär & Wiese, Nucl. Phys. **B609** (2001) 225 (hep-ph/0105258) — the prior art for this tree's own surviving leg | Low-energy pion physics alone cannot determine whether $N_c=3,5,7,\dots$; only high-energy observables (the Drell ratio) or $\eta\to\pi^+\pi^-\gamma$ can distinguish them experimentally. The paper's own $N_c$-odd argument is offered as the theoretical ceiling, not a stepping stone to $N_c=3$. |
| Tanizaki, JHEP08(2018)171 | The discrete 't Hooft anomaly of massless QCD is derived for **generic** $N_c$ and $N_f$; its no-go theorem on exotic chiral-symmetry-breaking phases applies uniformly and does not distinguish $N_c=3$ from other values. |
| hep-ph/0009242, "On the number of colours in QCD" | The textbook $\pi^0\to2\gamma$ argument for $N_c=3$ does **not**, in fact, constrain $N_c$ at all once the correct colour-dependent quark charges are used. |

**Conclusion.** The residual this session set out to close — no known mechanism narrows an odd $N_c$ beyond $\{3,5,7,\dots\}$ short of a measured observable — is **not a defect specific to this lattice/CA construction**. It reproduces exactly in the general, non-lattice, arbitrary-$N_c$ chiral-gauge-theory literature, where $N_c$ is likewise pinned only by experiment (the Drell ratio, hadronic decay rates; this model's own analogue is F293 §4's confinement-scale lever). This is worth recording precisely because it distinguishes "this model has a gap" from "this is where the anomaly-based approach runs out, for any theory of this shape" — the honest reading is the second.

---

## 6. Declared controls (D9/H2), measured

| control | measured reds | what it breaks |
|---|---|---|
| `su3_pi4_order_override=2` | G1 | falsely claims $SU(3)$ carries the $\pi_4$ obstruction (order 2, matching $SU(2)$'s) — the check must catch that this contradicts "only $N=2$ carries it," confirming it reads the table rather than hard-coding the answer |
| `include_nu_r=false` | G2 | drops the right-handed neutrino — the per-generation count at $N_c=3$ falls from 16 to 15, breaking the fixed (not conditional) expectation |
| `assumed_anomaly_modulus=8` | G3 | re-runs G3's own flagged arithmetic at a different modulus; the comparison is against a fixed expectation ($N_c=3\bmod4$, the modulus-16 result), so a different modulus must turn it red |
| `n_gen=2` | G0, G3 | breaks F324's premise (i) via `witten_scan`'s own already-tested control; G3 also reddens because $n_\text{gen}=2$ is no longer coprime to the modulus, breaking the exact $N_c\equiv3\pmod4$ reduction that holds for any *odd* $n_\text{gen}$ |

`casim test --id F338-ncolour-ceiling --control`: **4/4 CONTROL, each reddening exactly the declared leg set and no other.**

---

## 7. What this closes, and what remains

**Closes.**

* A previously-unexamined candidate route (a colour-group-native $\pi_4$ anomaly) — by citation, exactly, rather than leaving it as a silent gap.
* The question of whether the residual is a defect of this specific lattice/CA construction — externally, it is not; it is generic to any chiral gauge theory of this general shape.

**Does not close.** The bracket. $N_c=3$ remains selected only by F293 §4's empirical confinement-scale lever, exactly as after F325.

**Remains, and is the honest headline.**

1. **G3's premise is the single most concrete next step**, and it is a well-defined one: recompute the discrete symmetry generator $X=5(B-L)-4Y$ (or whatever the correct general-$N_c$ analogue is) on this model's own nullspace, and determine what the Pin$^+$/Dai-Freed bordism invariant actually requires for general $N_c$ — not assumed here to be a bare fermion count.
2. **If G3's premise is confirmed**, the bracket narrows to $\{3,7,11,15,\dots\}$, still not $\{3\}$ alone, and a further route would be needed to close the remaining gap.
3. **If no further selector is ever found** (consistent with §5's external check), the honest final state of row B10 is: $N_c$ odd, $N_c\neq1$, favoured empirically at 3 by a 28.3-decade confinement-scale argument, with the anomaly-based approach exhausted — matching the general state of the field, not a lattice-specific shortfall.

---

## 8. Falsifiers

1. **G1's citation is wrong.** If $\pi_4(SU(N))\neq0$ for some $N\ge3$ (it does not, but if a computational error in the cited literature were found), the colour group would carry its own selector and this finding's closure of that route would be wrong.
2. **G0's regression check fails** if `witten_scan` is ever modified in a way that changes its odd-$N_c$ output — this module would need re-verification against the new function. This is the only falsifier with a concrete, checkable trigger condition.
3. **The external literature is superseded** by a paper containing a genuine further theoretical selector for $N_c$ that this session's search (Bär & Wiese 2001, Tanizaki 2018, hep-ph/0009242, plus targeted searches on "SU(N) colour number selection," "Witten anomaly gauge group rank selection," and the mod-16 anomaly literature, all run 2026-08-31) did not surface. Concrete check for a future session: re-run the same four search terms against arXiv/INSPIRE and scan citations of Bär & Wiese (2001) and Tanizaki (2018) for any 2019–present paper claiming a further $N_c$ discriminator; absence of such a paper on a re-run is *evidence for*, not proof of, the residual staying generic.

**Not a falsifier of this finding** (recorded separately so it is not miscounted as one): **G3's premise turning out correct** (§7 item 1) — this would *promote* the grade by narrowing the bracket to $\{3,7,11,15,\dots\}$, not falsify anything stated here, since G3 is explicitly flagged and not claimed as a result in the first place.


## Reviewed & corrected

**2026-08-31 - 16:40** — attack pass: **CONFIRMED** (cold `general-purpose` subagent, 13-attack checklist, independently re-verified). Found: no circularity, input-laundering, exactness-inflation, tolerance-shopping, numerology, scope-creep, supersession, test-integrity, or falsifiability defect that changes the finding's central (negative) claim; all four declared controls independently re-run and confirmed reddening exactly their declared legs; `witten_scan`'s odd-$N_c$ pattern independently confirmed to $N=30$. Two real but narrow defects found and fixed: (1) the mod-16/$X=5(B-L)-4Y$ content in §4, the header, and the module's docstring/caveat string misattributed part of its citation to "Wang–Wen–Witten 1810.00844" — that paper ("A New SU(2) Anomaly") is unrelated to the Standard Model or fermion counting; corrected to García-Etxebarria & Montero (1808.00009) for the 16-fermion/generation content and Wang (2008.06499) for the $X=5(B-L)-4Y$ generator and the mod-16 condition itself, verified against both papers directly; `test-results/F338_ncolour_ceiling.json` regenerated from the corrected module, all 4/4 PASS and all 4 controls unchanged. (2) The Status line's "4/4 PASS" and the falsifiers list (§8) could read as certifying more than they do — added an explicit note on what the four checks certify (code correctness, not G3's physics) and separated "G3's premise turning out correct" out of the falsifier list into its own non-falsifier note, per the reviewer's WEAKENS finding. Rejected: none. Deferred: none — G3's premise (recomputing $X$'s general-$N_c$ form) was already correctly deferred as the finding's own named next step (§7 item 1), not a defect of this finding.