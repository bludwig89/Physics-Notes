# F349 — F339's α_em reopening-condition characterization corroborated by an independent, previously-uncited evidence line: exact all-orders zero-stiffness theorems (F143/F147) corroborate avenue A on a related but distinct pre-mixing object, and the exhausted condensate-sector programme (F41/F149/F153) narrows avenue D's residual attack surface

**Date:** 2026-09-02 - 14:20
**Status:** Confirmed (independent convergent-evidence check, not a derivation) — 6/6 checks PASS.
**Reviewed:** 2026-09-02 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F349-review-2026-09-02.md))
**Script:** `tests/findings/test_F349_alpha_em_convergent_stiffness_evidence.py`
**Results:** `test-results/F349_alpha_em_convergent_stiffness_evidence.json`
**Cross-references:** [[F127-alpha-em-derivation-four-avenue-nogo]] (the original no-go), [[F339-alpha-em-nogo-reopening-conditions]] (the characterization this corroborates and narrows — re-read in full, not summarized), [[F41-hypercharge-higgs-free-su2]] (U(1)_Y is Stueckelberg-absorbed, no bare kinetic term — machine-precision, 7/7), [[F143-wrap-loop-stiffness-nogo]] (transverse channel exactly zero at all orders, all scales — the strongest single result used here), [[F147-walk-loop-rigidity-channel-equality]] (one-tick rigidity, all gauge channels, exact), [[F149-condensate-channel-splitting-content-nogo]] and [[F153-diamagnetic-chargeblind-splitting-paramagnetic]] (the condensate-sector programme's own exhaustion), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the non-perturbative $E_g$ sector everything above says must own the stiffness, and whose own coupling is $O(1)$, i.e. outside every perturbative proxy used above).

---

## 1. What this finding is and is not

This session's task (per `docs/status/completeness-2026-08-20-prompts.md`-style D#14 framing) was to re-examine F127's four-avenue $\alpha_\text{em}$ no-go: for each avenue, name the assumption whose failure would reopen it, and check it against the post-F127 ledger. That work turned out to already exist: **F339 (2026-08-31), reviewed the same day** (`docs/reviews/F339-review-2026-08-31.md`, verdict CONFIRMED-NARROWER after a correction), already answers exactly this question, avenue by avenue, and is cited by claim card `docs/claims/CL113-*.md`.

Independent research for this finding (before F339 was found in the tree) had already assembled a second, disjoint evidence trail bearing on the same two avenues F339 calls avenue A and avenue D — built from `findings/F41`, `F138`, `F143`, `F147`, `F149`, `F153` (all dated 2026-06-08 through 2026-06-12, i.e. **all predate F339 by ten weeks** and were available to it). **None of the four were cited in `findings/F339-*.md` or `docs/claims/CL113-*.md` as of 2026-08-31** (verified mechanically against F339's finding text, §3; CL113 is a living claim card and is updated by this finding, §Files, to cite F349 and this evidence — so the check in §3 is against F339's own dated, unedited finding text, not against CL113's current, now-updated state). F339's avenue A used F251/F277 (vacuum-polarization transversality, computed in-model); its avenue D used F165/F279 (hypercharge charge-*ratio* rank-6-of-7 counting). The wrap-loop/walk-loop family used here is a **third, independent, technically disjoint route** — it attacks whether *any* lattice fermion loop can dynamically generate the coupling's absolute stiffness at all — and it reaches its own, in places *stronger*, conclusions by machine-precision computation rather than one-loop tensor algebra. This finding documents the convergence, and in one place (§5) narrows F339 §6 item 2's "unattempted" characterization to something more precise: *partially* attempted, at the perturbative-proxy level, and explicitly exhausted there.

**No new number is claimed for $\alpha_\text{em}$, and the ledger grade does not move.** This is a citation/evidence-completeness pass, in the same spirit as F339 itself.

## 2. Avenue A, independently corroborated

F127's avenue A argued from a Ward-identity heuristic ($\Pi^{\mu\nu}(0)=0$) that the Sakharov-style induced-coupling mechanism fails. F339 narrowed this using F251/F277's in-model, one-loop, symbolic verification that the fermion bubble's $\Pi^{\mu\nu}$ actually takes the transverse form.

**F143 and F147 go further, on a different construction (the Peierls-gauged walk/wrap, not the momentum-space fermion bubble), and reach an exact, non-perturbative, all-orders statement:**

- F143 §2 (`test-results/F143_wrap_loop_stiffness_test.json`, check A): the transverse (field-strength) coupling of the $U(1)_Y$ wrap to the fermion kinetic sea is a **unitary conjugation** for any static gauge field, so the induced transverse stiffness is exactly zero **at all orders and all scales**, not merely at one loop or at $q\to0$. Measured residual: max eigenphase shift $1.33\times10^{-15}$ — machine precision, not an asymptotic bound.
- F147 §2 (`test-results/F147_induced_stiffness_loop.json`, check L6): the free one-tick sea's static response is exactly zero in **every** gauge channel (vector/SU(2) and staggered/hypercharge alike), from an explicit spectral-closure mechanism ($\theta\to\pi-\theta$ symmetry pairing filled states to a constant sum), residual $<10^{-11}$ at field strengths up to $\varepsilon=0.3$.
- F149 §2 (check N4, `test-results/F149_condensate_channel_splitting.json`): this rigidity **survives turning on a Dirac mass** (proxy for the EWSB condensate coupling), residual $2.1\times10^{-11}$ at $m=0.4$ — so it is not a massless-limit artifact.

This is, in its own right, strictly stronger than "the one-loop bubble happens to be transverse": it is a structural theorem (unitary conjugation / spectral symmetry) that holds independent of the loop order or the fermion mass. **Scope caveat, stated precisely rather than glossed over:** F143/F147 compute the stiffness of the *raw* $U(1)_Y$/vector wrap channels — the pre-mixing hypercharge and $SU(2)_L$ Cartan gauge fields, on the walk/Peierls construction — not literally F251/F277's object, which is the *physical*, post-mixing photon's $\Pi^{\mu\nu}$ computed from the F69 paired-spinor construction. The two are related (the physical photon is the appropriate $(W^3,B)$ rotation of exactly these Cartan channels, F35/F44) but are not the same calculation on the same object, and this finding does not attempt the rotation that would make them formally identical. So the fair statement is: **an independent, unrelated mechanism (unitary conjugation on the pre-mixing wrap/walk construction) reaches the same qualitative conclusion — no fermion-loop-induced stiffness — as F251/F277's direct computation on the physical photon**, corroboration rather than a strict logical subsumption or replacement of F339's argument. (Neither line touches F339's own residual — a hypothetical binding-scale form-factor effect on the *paired-spinor photon itself* is a distinct physical mechanism from any fermion-sea loop rigidity theorem, pre- or post-mixing, and remains exactly as open as F339 left it.)

## 3. Citation-gap check

`grep -c "F143\|F147\|F149\|F153" findings/F339-alpha-em-nogo-reopening-conditions.md` returns 0 for all four names (check G1). F339's finding file is a dated, already-reviewed historical record (`docs/reviews/F339-review-2026-08-31.md`) and this finding does not edit it — consistent with project convention that findings are superseded, not rewritten. The check is against that file specifically, not against `docs/claims/CL113-*.md`, because CL113 *is* edited by this finding (§9) to add F349 and, in its evidence prose, F143/F147/F149/F153 — checking CL113 here would just re-detect this finding's own edit rather than the historical gap. This is exactly parallel to F339 §5's own "zero mentions" check on avenue C — recorded so a later session does not have to re-search to confirm the gap, and falsifiable (if a later grep against F339's finding file finds a hit, this finding's premise needs revisiting).

## 4. Avenue D, independently narrowed by structural exhaustion, not just ratio-counting

F339's avenue D treatment (F165/F279) shows the hypercharge system fixes charge **ratios** ($y_Q:y_u:y_d:y_L:y_e:y_\nu$), rank 6 of 7, with the overall normalization $y_Q=\tfrac16$ fixed by convention — a discrete-assignment result, orthogonal to dynamics.

The wrap/walk-loop family answers a *different* question directly on point with F127's own avenue-D framing ("the Peierls coupling $q$ is independent of $Z$, $c$, curl normalization — no constraint found"): **can any lattice dynamical mechanism generate $q$'s absolute scale?**

- **Structural premise (F41, 7/7 machine-precision).** $U(1)_Y$ has no independent lattice kinetic term at all — it rides on $U(x)$ as a Stueckelberg phase, eaten by the $Z$'s longitudinal mode. There is therefore no analogue of F110/F115-CM3's $g_s^2\chi=\tfrac14$ rotor-stiffness lock available *by construction* for the abelian sector: that lock requires a bare kinetic term to normalize against, and none exists.
- **Fermion-loop route: exhausted, exact zero (§2 above).** F143's all-orders conjugation no-go and F147's one-tick rigidity theorem jointly close the only remaining candidate mechanism (a fermion-loop-induced kinetic term) at the free-sea level, for every channel.
- **Condensate-sector route: attempted, and explicitly found not to yield a clean number even for the weaker ratio question.** F149 (§3–4) and F153 (§3–5) run the only viable remaining mechanism — the EWSB condensate, proxied by a Dirac mass $m$ coupled through the same wrap — and find: the mass-driven channel splitting exists and turns on $\propto m^2$ (F149 N6), but (a) the small-$\tilde q$ ratio $R(m)\equiv\chi_\text{vec}/\chi_\text{stag}$ is not cleanly extractable in the two-tick sea (F153 N1: cone/cut contamination exceeds the signal, $0.148$ artifact vs. $0.114$ signal, and the sign flips with $\tilde q$ direction), (b) the vector stiffness does not decompose into a clean 7- or 8-fold channel count (F153 M1), and (c) — decisively for scope — **the physical condensate coupling is $O(1)$** (F153 P1: $E_g$ amplitude at the lepton point $e=0.728$), which is outside the small-$m$ perturbative regime every one of these checks used. Closing this route for real requires the non-perturbative F118 self-consistent $(W,v,c)$ solution propagated into the wrap-stiffness channel — a calculation nobody has attempted, at any avenue, for any purpose (F118 itself solves the *lepton mass* sector, not gauge stiffness).

**Net effect on avenue D's residual attack surface.** F339 §6 item 2 states the F127-avenue-F vertex/overlap-integral calculation ("derive the effective vertex from the composite photon bilinear, F89, against an external fermion") has not been attempted by any session. That is correct for the *literal* F89 construction. But a closely related calculation — the induced wrap/vertex stiffness via lattice fermion loops, both perturbative-free (F143/F147, exact zero) and perturbative-massive-proxy (F149/F153, exhausted without a clean result) — **has** been attempted, twice over, and both attempts terminated in decisive negatives rather than silence. The honest residual attack surface for avenue D is therefore narrower than "an unattempted vertex calculation": it is specifically **the non-perturbative $E_g$ condensate self-energy at its own $O(1)$ operating point**, propagated through the same wrap-stiffness channel these findings already built the machinery for. This is a real, previously-unattempted calculation — but it is a much narrower and better-characterized target than F339 §6 left it, and it inherits F118's difficulty (a genuine strongly-coupled non-perturbative problem), not a routine loop integral.

## 5. Avenues B, C, E, F — unchanged

Nothing in the F41/F143/F147/F149/F153 line bears on avenue B (F339's $\mu_\star=4\pi v$ / ledger-row-D#17 reclassification stands untouched) or avenue C (the Dirac-monopole/topological route remains genuinely unexplored — re-confirmed by the same zero-mentions grep as F339 §5, extended here to also check for "soliton", still zero hits). Avenue E's numerical coincidence ($1/\alpha(\Lambda)=64=z_\text{NN}^2$, 1.14% agreement) and avenue F's diagnosis are unaffected; no new candidate for the bare $64$ emerged from this search.

**External calibration (why 1.14% is not close enough to update anything).** CODATA 2022 gives $1/\alpha = 137.035999177(21)$, a relative uncertainty of $1.6\times10^{-10}$ — eight orders of magnitude tighter than avenue E's 1.14% coincidence. This is the standard cautionary bar in this specific sub-field: attempts to derive $\alpha$ from small integers or pure numerology have a long, specifically bad track record (Eddington's 1929–1944 attempts to derive $1/\alpha=136$, later "corrected" to 137, from group-theoretic arguments are the canonical example, now regarded as numerology rather than physics). Avenue E is recorded as exactly what F127 already called it — an observation, not a derivation — and this finding adds no argument that would promote it.

## 6. Verdict

F339's characterization stands, and is now corroborated by a second, independent, machine-precision evidence line for avenues A and D specifically. Combined:

- **Avenue A**: closed by F251/F277's in-model one-loop transversality on the physical photon, now corroborated (not logically subsumed — see §2's scope caveat, the two computations are on related but distinct pre-/post-mixing objects) by F143/F147's exact non-perturbative rigidity theorems on the raw wrap channels. The only residual is F339's compositeness/form-factor loophole on the paired-spinor photon itself — untouched by either line, genuinely open, and named already.
- **Avenue B**: closed for the purpose of deriving $\alpha$; reclassified (F138/F339) as ledger row D#17's question (deriving $v$), not D#14's.
- **Avenue C**: genuinely unexplored (Dirac-monopole/topological route) — the one true fifth-avenue candidate, per F339, unchanged here.
- **Avenue D**: the fermion-loop sub-route is now closed *exactly* (not just "no constraint found") by F41 (structural: no kinetic term exists) and F143/F147 (dynamical: even if one could exist, the loop gives zero); the condensate sub-route is attempted and exhausted at the perturbative-proxy level (F149/F153), leaving a single, precisely named, non-perturbative residual (F118's own $O(1)$ self-energy) as the only unclosed door — narrower than F339's "vertex/overlap-integral calculation, unattempted."

$\alpha_\text{em}$ remains `OPEN` / the model's last irreducible dimensionless input. The grade this finding supports is: **F339's `OPEN, four reopening conditions named, two unattempted attack surfaces named` is corroborated, with avenue D's residual attack surface narrowed from "an unattempted vertex calculation" to "the non-perturbative $E_g$ condensate self-energy specifically" — a harder but better-defined target.**

## 7. Check summary (6/6)

| Check | Statement | Tier | Result |
|---|---|---|---|
| G1 | F143/F147/F149/F153 not cited in F339 or CL113 (grep, 4 names × 2 files) | mechanical | 0 hits, all 8 |
| G2 | F143 check A: max eigenphase shift matches quoted $1.33\times10^{-15}$, PASS in source JSON | artifact-verified | exact match |
| G3 | F147 check L6: one-tick $\chi$ = 0 (both channels), PASS in source JSON | artifact-verified | exact match |
| G4 | F149 check N4: massive one-tick rigidity residual $2.1\times10^{-11}$ at $m=0.4$, PASS in source JSON | artifact-verified | exact match |
| G5 | F153 checks D2 (charge-blind, $1.11\times10^{-10}$) and P1 ($E_g$ amplitude $e=0.728$, O(1)) match quoted values, PASS in source JSON | artifact-verified | exact match |
| G6 | Independent rational recomputation: F147 N9 ($t^2=1/4$, $\sin^2\theta_W^\text{free}=1/5$, gap $=8/7$) and F149 N8 (bare $1/4$; SM content $t^2=3/5$, $\sin^2\theta_W=3/8$, gap $10/21$) reproduced from stated bare/SM charge assignments via exact `fractions.Fraction` arithmetic | exact rational | exact |

## 8. Honest scope

- This is a citation-completeness and cross-verification pass, not new physics. Every quoted number is pulled from an existing, already-PASSing test-results JSON (G2–G5) or independently recomputed from stated charge assignments using exact rational arithmetic (G6) — nothing here re-runs the underlying lattice computations.
- The "citation gap" (§3) is a fact about the current tree's cross-references, not a claim that F339's physics is wrong — F339's own conclusions for avenues A and D are corroborated, not contradicted, by this second line.
- §4's narrowing of avenue D's residual attack surface is a scoping statement (what the target calculation is), not a claim that the calculation has been done or is easy — F118's own $O(1)$ condensate coupling means it is explicitly a non-perturbative problem, harder than anything the perturbative-proxy findings (F149/F153) attempted.
- The CODATA figure and Eddington-history note (§5) are external, sourced context requested by the originating prompt, not model results.

## 9. Files

- `findings/F349-alpha-em-induced-stiffness-convergent-evidence.md` — this finding
- `tests/findings/test_F349_alpha_em_convergent_stiffness_evidence.py` — G1–G6
- `test-results/F349_alpha_em_convergent_stiffness_evidence.json` — full output
